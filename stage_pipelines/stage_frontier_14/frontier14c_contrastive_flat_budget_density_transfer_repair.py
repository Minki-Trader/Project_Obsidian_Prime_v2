from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_12 import frontier12b_trade_shape_duration_label_proxy_scout as f12b
from stage_pipelines.stage_frontier_14 import frontier14b_daily_session_opportunity_budget_proxy_scout as f14b


STAGE_ID = f14b.STAGE_ID
RUN_ID = "frontier14C_contrastive_flat_budget_density_transfer_repair_v1"
RUN_NUMBER = "frontier14C"
PARENT_RUN_ID = f14b.RUN_ID
NEXT_STRICT_RUN_ID = "frontier14D_grok_pre_expensive_daily_session_opportunity_budget_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier14D_stage_closeout_daily_session_opportunity_budget_onnx_scout_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_14/frontier14c_contrastive_flat_budget_density_transfer_repair.py")
F14B_FINAL = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_decision.json"

LABEL_ORDER = f04d.LABEL_ORDER
REPAIR_MODEL_IDS = {"logreg_l2_c0p5_plain_argmax"}


@dataclass(frozen=True)
class RepairPolicy:
    policy_id: str
    flat_multiplier: int
    flat_selection_rule: str
    include_skip_context_flats: bool
    boundary: str


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    parent_final = read_json(F14B_FINAL)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    variants = f14b.build_variants()
    policies = build_repair_policies()
    result = train_and_evaluate(full, raw, feature_order, variants, policies)
    final = build_final(created_at, result, variants, policies, source_integrity, feature_order, parent_final)
    artifacts = write_artifacts(result, final, variants, policies)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_repair_policies() -> list[RepairPolicy]:
    return [
        RepairPolicy(
            policy_id="flat4x_safest",
            flat_multiplier=4,
            flat_selection_rule="lowest_opportunity_utility_then_time(가장 낮은 기회 효용 뒤 시간순)",
            include_skip_context_flats=True,
            boundary="no_label_quota_or_horizon_change_no_threshold_search(라벨 할당량/보유기간 변경 없음, 임계값 탐색 없음)",
        ),
        RepairPolicy(
            policy_id="flat8x_safest",
            flat_multiplier=8,
            flat_selection_rule="lowest_opportunity_utility_then_time(가장 낮은 기회 효용 뒤 시간순)",
            include_skip_context_flats=True,
            boundary="no_label_quota_or_horizon_change_no_threshold_search(라벨 할당량/보유기간 변경 없음, 임계값 탐색 없음)",
        ),
        RepairPolicy(
            policy_id="flat16x_safest",
            flat_multiplier=16,
            flat_selection_rule="lowest_opportunity_utility_then_time(가장 낮은 기회 효용 뒤 시간순)",
            include_skip_context_flats=True,
            boundary="no_label_quota_or_horizon_change_no_threshold_search(라벨 할당량/보유기간 변경 없음, 임계값 탐색 없음)",
        ),
    ]


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[f14b.OpportunityVariant],
    policies: list[RepairPolicy],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values(피처 행렬에 NaN 또는 무한값이 있습니다).")
    sample_indices = np.concatenate(
        [
            np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
            for split in ("train", "validation", "oos")
        ]
    )
    specs = [spec for spec in f04d.MODEL_SPECS if spec.model_id in REPAIR_MODEL_IDS]
    if not specs:
        raise RuntimeError("No repair model specs selected(수리 모델 사양이 선택되지 않았습니다).")

    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    oracle_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    target_diagnostics: list[dict[str, Any]] = []
    label_model_density_rows: list[dict[str, Any]] = []
    training_subset_rows: list[dict[str, Any]] = []
    candidate_policy: dict[str, str] = {}

    for variant in variants:
        path = f14b.opportunity_path_arrays(full, raw, variant)
        labels, oracle_signal, diagnostics = f14b.build_opportunity_labels(full, path, variant)
        target_diagnostics.append({"target_id": variant.variant_id, **json_ready(asdict(variant)), **diagnostics})
        distribution_rows.extend(f12b.label_distribution(full, labels, variant))
        oracle_metrics.extend(
            f12b.evaluate_all_splits(
                full,
                oracle_signal,
                path["fwd_return"],
                variant,
                "oracle_opportunity_budget_replay(오라클 기회 예산 재생)",
                "oracle",
            )
        )
        for policy in policies:
            train_indices, subset_diag = select_training_subset(full, path, labels, variant, policy)
            training_subset_rows.append(subset_diag)
            missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_indices]))
            if missing:
                skipped_rows.append(
                    {
                        "target_id": variant.variant_id,
                        "repair_policy_id": policy.policy_id,
                        "reason": f"missing_train_classes={missing}",
                        "repair_boundary": policy.boundary,
                    }
                )
                continue
            for spec in specs:
                short_model_id = f12b.MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:10])
                candidate_id = f"{variant.variant_id}__{policy.policy_id}__{short_model_id}"
                model_instance_id = f"f14c_{candidate_id}"
                candidate_policy[candidate_id] = policy.policy_id
                model = clone(spec.estimator)
                model.fit(x_all[train_indices], labels[train_indices])
                probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
                pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
                signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

                target_dir = MODEL_DIR / variant.variant_id / policy.policy_id
                io_path(target_dir).mkdir(parents=True, exist_ok=True)
                model_path = target_dir / f"{model_instance_id}.joblib"
                onnx_path = target_dir / f"{model_instance_id}.onnx"
                joblib.dump(model, io_path(model_path))
                export_meta = export_sklearn_to_onnx_zipmap_disabled(
                    model,
                    onnx_path,
                    feature_count=x_all.shape[1],
                    target_opset=12,
                    drop_label_output=False,
                )
                parity = check_onnxruntime_probability_parity(
                    model,
                    onnx_path,
                    x_all[sample_indices],
                    class_order=LABEL_ORDER,
                    tolerance=1e-5,
                )
                parity_rows.append(
                    {
                        "candidate_id": candidate_id,
                        "target_id": variant.variant_id,
                        "repair_policy_id": policy.policy_id,
                        "model_id": spec.model_id,
                        "model_instance_id": model_instance_id,
                        "onnx_path": onnx_path.as_posix(),
                        "onnx_sha256": export_meta["sha256"],
                        "joblib_path": model_path.as_posix(),
                        "joblib_sha256": sha256_file(model_path),
                        "parity_passed": bool(parity["passed"]),
                        "parity_max_abs_diff": parity["max_abs_diff"],
                        "parity_mean_abs_diff": parity["mean_abs_diff"],
                        "rows_checked": parity["rows"],
                        "input_name": parity["input_name"],
                        "output_names": "|".join(parity["output_names"]),
                    }
                )
                classification_rows.extend(
                    add_policy_id(
                        f12b.classification_metrics(
                            full, labels, pred_label, variant, spec.model_id, model_instance_id, candidate_id
                        ),
                        policy.policy_id,
                    )
                )
                split_rows = add_policy_id(
                    f12b.evaluate_all_splits(
                        full,
                        signal,
                        path["fwd_return"],
                        variant,
                        "argmax_contrastive_flat_budget_model_signal(최대확률 대비 평면예산 모델 신호)",
                        candidate_id,
                        model_id=spec.model_id,
                        model_instance_id=model_instance_id,
                    ),
                    policy.policy_id,
                )
                model_metrics.extend(split_rows)
                subperiod_metrics.extend(
                    add_policy_id(
                        f12b.evaluate_subperiods(
                            full,
                            signal,
                            path["fwd_return"],
                            variant,
                            candidate_id,
                            spec.model_id,
                            model_instance_id,
                        ),
                        policy.policy_id,
                    )
                )
                label_model_density_rows.extend(
                    add_policy_id(
                        f14b.density_gap_rows(
                            full, oracle_signal, signal, variant, candidate_id, spec.model_id, model_instance_id
                        ),
                        policy.policy_id,
                    )
                )

    candidate_summary = f12b.build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows)
    for row in candidate_summary:
        row["repair_policy_id"] = candidate_policy.get(str(row.get("candidate_id")), "")
        row["repair_boundary"] = "contrastive_flat_training_subset_only(대비 평면 학습 부분 표본만 변경)"
    return {
        "model_metrics": model_metrics,
        "subperiod_metrics": subperiod_metrics,
        "oracle_metrics": oracle_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": distribution_rows,
        "skipped": skipped_rows,
        "target_diagnostics": target_diagnostics,
        "candidate_summary": candidate_summary,
        "label_model_density_gap": label_model_density_rows,
        "training_subset_diagnostics": training_subset_rows,
    }


def select_training_subset(
    full: pd.DataFrame,
    path: dict[str, np.ndarray],
    labels: np.ndarray,
    variant: f14b.OpportunityVariant,
    policy: RepairPolicy,
) -> tuple[np.ndarray, dict[str, Any]]:
    split = full["split"].astype(str).to_numpy()
    train_mask = split == "train"
    timestamps = pd.to_datetime(full["timestamp"], errors="raise")
    buckets = f14b.opportunity_buckets(full, timestamps, variant)
    day_groups = timestamps.dt.strftime("%Y-%m-%d").astype(str).to_numpy()
    safe_score = np.maximum(path["long_utility"], path["short_utility"])

    selected: list[int] = []
    opportunity_idx = np.flatnonzero(train_mask & (labels != 1))
    selected.extend(int(idx) for idx in opportunity_idx)
    selected_flat = 0
    selected_skip_flat = 0
    bucket_count = 0

    for bucket in sorted(set(str(item) for item in buckets if str(item) != "skip")):
        bucket_count += 1
        bucket_mask = train_mask & (labels == 1) & (buckets == bucket)
        choice = choose_safest_indices(bucket_mask, safe_score, timestamps, variant.quota_per_bucket * policy.flat_multiplier)
        selected.extend(int(idx) for idx in choice)
        selected_flat += int(len(choice))

    if policy.include_skip_context_flats:
        for day in sorted(set(str(item) for item in day_groups)):
            skip_mask = train_mask & (labels == 1) & (buckets == "skip") & (day_groups == day)
            choice = choose_safest_indices(skip_mask, safe_score, timestamps, variant.quota_per_bucket * policy.flat_multiplier)
            selected.extend(int(idx) for idx in choice)
            selected_skip_flat += int(len(choice))

    train_indices = np.array(sorted(set(selected)), dtype="int64")
    label_values = labels[train_indices] if len(train_indices) else np.array([], dtype="int64")
    return train_indices, {
        "target_id": variant.variant_id,
        "repair_policy_id": policy.policy_id,
        "flat_multiplier": policy.flat_multiplier,
        "include_skip_context_flats": bool(policy.include_skip_context_flats),
        "bucket_count": bucket_count,
        "train_rows_selected": int(len(train_indices)),
        "train_opportunity_rows_selected": int(len(opportunity_idx)),
        "train_flat_rows_selected": int(selected_flat),
        "train_skip_flat_rows_selected": int(selected_skip_flat),
        "train_short_count": int((label_values == 0).sum()),
        "train_flat_count": int((label_values == 1).sum()),
        "train_long_count": int((label_values == 2).sum()),
        "train_opportunity_fraction": float((label_values != 1).sum() / len(label_values)) if len(label_values) else 0.0,
        "selection_rule": policy.flat_selection_rule,
        "repair_boundary": policy.boundary,
    }


def choose_safest_indices(
    mask: np.ndarray,
    safe_score: np.ndarray,
    timestamps: pd.Series,
    limit: int,
) -> np.ndarray:
    idx = np.flatnonzero(mask)
    if len(idx) == 0 or limit <= 0:
        return np.array([], dtype="int64")
    stamp_ns = timestamps.iloc[idx].astype("int64").to_numpy()
    finite_score = np.nan_to_num(safe_score[idx], nan=np.inf, posinf=np.inf, neginf=-np.inf)
    order = np.lexsort((idx, stamp_ns, finite_score))
    return idx[order[: min(limit, len(idx))]]


def add_policy_id(rows: list[dict[str, Any]], policy_id: str) -> list[dict[str, Any]]:
    return [{**row, "repair_policy_id": policy_id} for row in rows]


def build_final(
    created_at: str,
    result: dict[str, Any],
    variants: list[f14b.OpportunityVariant],
    policies: list[RepairPolicy],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    parent_final: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    best = candidate_summary[0] if candidate_summary else {}
    status = (
        "density_transfer_strict_scout_clue_needs_grok_pre_expensive_no_authority"
        if strict_rows
        else (
            "density_transfer_preserved_clue_ready_for_closeout_no_authority"
            if preserved_rows
            else "density_transfer_negative_memory_ready_for_closeout_no_authority"
        )
    )
    judgment = (
        "strict_scout_clue_candidate(엄격 탐색 단서 후보)"
        if strict_rows
        else (
            "preserved_clue_candidate(보존 단서 후보)"
            if preserved_rows
            else "negative_memory_candidate(부정 기억 후보)"
        )
    )
    next_run_id = NEXT_STRICT_RUN_ID if strict_rows else NEXT_CLOSEOUT_RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "strict_scout_clue_rows": len(strict_rows),
        "preserved_clue_rows": len(preserved_rows),
        "candidate_row_count": len(candidate_summary),
        "best_candidate_row": best,
        "variant_count": len(variants),
        "repair_policy_count": len(policies),
        "model_ids_used": sorted(REPAIR_MODEL_IDS),
        "parent_status": parent_final.get("status", ""),
        "parent_judgment": parent_final.get("judgment", ""),
        "parent_best_candidate_row": parent_final.get("best_candidate_row", {}),
        "source_integrity": source_integrity,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "data_integrity": data_integrity_record(source_integrity),
        "model_validation": model_validation_record(best),
        "artifact_lineage": artifact_lineage_record(parent_final),
        "repair_boundary": "same_quota_same_hold_same_argmax_plain_lr_subset_repair(같은 할당량/보유기간/최대확률, 평범 로지스틱 학습 표본 수리)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": (
            "not_run_requires_grok_pre_expensive_if_strict(엄격 단서가 있으면 Grok 비싼 검증 전 검토 필요)"
            if strict_rows
            else "not_run_closeout_review_first(미실행, 먼저 마감 검토)"
        ),
        "mt5_status": "not_run_proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
    }


def data_integrity_record(source_integrity: dict[str, Any]) -> dict[str, Any]:
    return {
        "data_source": f03b.DATASET_PATH.as_posix(),
        "time_axis": "US100 M5 closed-bar timestamp order(US100 5분봉 확정봉 시각 순서)",
        "sample_scope": "Tier A train/validation/OOS fixed split(티어 A 학습/검증/표본밖 고정 분할)",
        "feature_label_boundary": "features use closed bars; labels use future path only as supervised target(피처는 확정봉, 라벨은 감독 표적으로만 미래 경로 사용)",
        "repair_boundary": "training subset changed after F14B; label quota and hold unchanged(F14B 뒤 학습 표본만 변경, 라벨 할당량과 보유기간 유지)",
        "leakage_risk": "no validation/OOS recalibration and no threshold search(검증/표본밖 재보정 없음, 임계값 탐색 없음)",
        "data_hash_or_identity": source_integrity,
        "integrity_judgment": "usable_with_repair_boundary(수리 경계 포함 사용 가능)",
    }


def model_validation_record(best: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fixed sklearn-to-ONNX 3-class argmax plain logistic(고정 sklearn-to-ONNX 3클래스 최대확률 평범 로지스틱)",
        "target_and_label": "F14B daily/session opportunity budget labels unchanged(F14B 일/세션별 기회 예산 라벨 유지)",
        "selection_metric": "strict/preserved scout clue plus aspiration distance(엄격/보존 탐색 단서와 목표 거리)",
        "threshold_policy": "argmax_only_no_threshold_search(최대확률 전용, 임계값 탐색 없음)",
        "overfit_risk": "three capped flat-subset policies only(상한 있는 평면 부분 표본 정책 3개만)",
        "comparison_baseline": "Frontier14B parent proxy result(프론티어14B 부모 프록시 결과)",
        "validation_judgment": "exploratory_repair(탐색 수리)",
        "best_candidate": best.get("candidate_id", "none"),
    }


def artifact_lineage_record(parent_final: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": [f03b.DATASET_PATH.as_posix(), f03b.FEATURE_ORDER_PATH.as_posix(), F14B_FINAL.as_posix()],
        "parent_run": parent_final.get("run_id", PARENT_RUN_ID),
        "producer": SCRIPT_PATH.as_posix(),
        "consumer": REPORT_PATH.as_posix(),
        "availability": "generated_ignored_models_with_manifest(모델은 ignore 경로에 생성되고 manifest로 추적)",
        "lineage_judgment": "connected_with_repair_boundary(수리 경계 포함 연결)",
    }


def write_artifacts(
    result: dict[str, Any],
    final: dict[str, Any],
    variants: list[f14b.OpportunityVariant],
    policies: list[RepairPolicy],
) -> dict[str, Path]:
    artifacts = {
        "variant_manifest": RUN_ROOT / "variant_manifest.csv",
        "repair_manifest": RUN_ROOT / "repair_manifest.csv",
        "training_subset_diagnostics": RUN_ROOT / "training_subset_diagnostics.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "oracle_metrics": RUN_ROOT / "oracle_metrics.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "label_model_density_gap": RUN_ROOT / "label_model_density_gap.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.json",
        "skipped": RUN_ROOT / "skipped.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["variant_manifest"], [asdict(variant) for variant in variants])
    write_csv(artifacts["repair_manifest"], [asdict(policy) for policy in policies])
    write_csv(artifacts["training_subset_diagnostics"], result["training_subset_diagnostics"])
    write_csv(artifacts["label_distribution"], result["label_distribution"])
    write_csv(artifacts["oracle_metrics"], result["oracle_metrics"])
    write_csv(artifacts["model_metrics"], result["model_metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["label_model_density_gap"], result["label_model_density_gap"])
    write_csv(artifacts["skipped"], result["skipped"])
    write_json(artifacts["target_diagnostics"], result["target_diagnostics"])
    write_json(artifacts["final_decision"], final)
    write_json(
        artifacts["run_manifest"],
        {
            **final,
            "script_path": SCRIPT_PATH.as_posix(),
            "script_sha256": sha256_file(SCRIPT_PATH),
            "parent_final": artifact_identity(F14B_FINAL),
            "dataset": artifact_identity(f03b.DATASET_PATH),
            "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
            "artifacts": {key: path.as_posix() for key, path in artifacts.items()},
        },
    )
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    parent = final["parent_best_candidate_row"]
    text = f"""# Frontier14C Contrastive Flat Budget Repair(프론티어14C 대비 평면예산 수리)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F14B(F14B)의 quota label(할당량 라벨)과 hold(보유기간)는 유지하고, plain logistic ONNX(평범 로지스틱 온엑스)의 train subset(학습 부분 표본)만 safest flat rows(가장 안전한 평면 행)로 제한했습니다.

Effect(효과): label-side density(라벨 쪽 밀도)는 그대로 두고, 모델이 기회 라벨을 너무 적게 전달하던 문제만 분리해서 시험했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`

## Parent Comparison(부모 비교)

- F14B best(F14B 최고): `{parent.get('candidate_id', 'none')}`
- F14B validation/OOS density(F14B 검증/표본밖 밀도): `{fmt(parent.get('validation_trades_per_day'))}` / `{fmt(parent.get('oos_trades_per_day'))}`
- F14C validation/OOS density(F14C 검증/표본밖 밀도): `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('oos_trades_per_day'))}`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- training subset diagnostics(학습 부분 표본 진단): `{artifacts['training_subset_diagnostics'].as_posix()}`
- label/model density gap(라벨/모델 밀도 격차): `{artifacts['label_model_density_gap'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    f03b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {RUN_ID}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            f"next_run_id: {final['next_run_id']}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "",
        ]
    )


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier14C(프론티어14C)는 F14B(F14B) 라벨을 유지하고 contrastive flat training subset(대비 평면 학습 부분 표본) 수리를 실행했습니다.

Effect(효과): best candidate(최고 후보) `{best.get('candidate_id', 'none')}`의 PF/density/DD(수익 팩터/밀도/손실폭)를 기록했고, WFO/MT5(워크포워드/메타트레이더5)와 authority claim(권위 주장)은 아직 하지 않았습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier14 Selection Status(프론티어14 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최고 후보): `{best.get('candidate_id', 'none')}`

Best validation/OOS PF-density-DD(최고 검증/표본밖 수익 팩터-밀도-손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%` and `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`

Key artifacts(핵심 산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['training_subset_diagnostics'].as_posix()}`
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier14 Review Index(프론티어14 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{f14b.PARENT_RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용).
- `{PARENT_RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) `0`, preserved rows(보존 행) `2`.
- `{RUN_ID}`: contrastive flat repair(대비 평면 수리), strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`.
- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier14C Required Gate Coverage Audit(프론티어14C 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): capped contrastive flat policies(상한 있는 대비 평면 정책) executed(실행됨)
- kpi_contract_audit(KPI 계약 감사): validation/OOS PF-density-DD and subperiod DD(검증/표본밖 수익 팩터-밀도-손실폭과 하위기간 손실폭) recorded(기록됨)
- data_integrity_gate(데이터 무결성 게이트): `{final['data_integrity']['integrity_judgment']}`
- model_validation_gate(모델 검증 게이트): `{final['model_validation']['validation_judgment']}`
- artifact_lineage_gate(산출물 계보 게이트): `{final['artifact_lineage']['lineage_judgment']}`
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "density_transfer_repair(밀도 전달 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};plain_lr_subset_repair;no_wfo_no_mt5_no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "proxy_repair_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(final["best_candidate_row"]),
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "result_path": REPORT_PATH.as_posix(),
        "final_decision_path": artifacts["final_decision"].as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "density_transfer_repair(밀도 전달 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "same_quota_same_hold_plain_lr_subset_no_threshold_no_wfo_no_mt5_no_authority(같은 할당량/보유기간, 평범 로지스틱 부분 표본, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_density_transfer_repair",
            "subrun_id": f"{RUN_ID}__tier_a_density_transfer_repair",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "density_transfer_proxy_repair_not_runtime(밀도 전달 프록시 수리, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 짝 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"worst_sub_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(rows)).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "inf"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())

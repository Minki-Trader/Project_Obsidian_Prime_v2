from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
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


STAGE_ID = f07b.STAGE_ID
RUN_ID = "frontier07C_class_prior_density_bridge_repair_v1"
RUN_NUMBER = "frontier07C"
PARENT_RUN_ID = f07b.RUN_ID
NEXT_CLUE_RUN_ID = "frontier07D_grok_pre_expensive_risk_label_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier07D_stage_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
F07B_SUMMARY = STAGE_ROOT / "02_runs" / f07b.RUN_ID / "candidate_summary.csv"
F07B_REFERENCE_METRICS = STAGE_ROOT / "02_runs" / f07b.RUN_ID / "reference_model_metrics.csv"

LABEL_ORDER = f04d.LABEL_ORDER
REPAIR_TARGET_COUNT = 4


@dataclass(frozen=True)
class RepairModelSpec:
    model_id: str
    directional_weight: float
    estimator: Pipeline


REPAIR_MODEL_SPECS = tuple(
    RepairModelSpec(
        model_id=f"logreg_l2_c0p5_dirw{weight:.2f}_argmax".replace(".", "p"),
        directional_weight=weight,
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        C=0.5,
                        random_state=17,
                        solver="lbfgs",
                        class_weight={0: weight, 1: 1.0, 2: weight},
                    ),
                ),
            ]
        ),
    )
    for weight in (1.25, 1.50, 1.75, 2.00)
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    selected_variants = select_repair_variants(full, raw)
    result = train_repair_models(full, raw, feature_order, selected_variants)
    final = build_final(result, source_integrity, feature_order, selected_variants)
    artifacts = write_artifacts(result, final, selected_variants)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "strict_scout_clue_rows": final["strict_scout_clue_rows"],
        "preserved_clue_rows": final["preserved_clue_rows"],
        "best_candidate": final["best_candidate_row"].get("candidate_id"),
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def select_repair_variants(full: pd.DataFrame, raw: pd.DataFrame) -> list[f07b.RiskLabelVariant]:
    all_variants = {variant.variant_id: variant for variant in f07b.build_variants(full, raw)}
    if not f07b.path_exists(F07B_SUMMARY):
        raise FileNotFoundError(F07B_SUMMARY)
    summary = pd.read_csv(str(io_path(F07B_SUMMARY)), encoding="utf-8-sig")
    pool = summary[
        summary["preserved_clue_pass"].astype(bool)
        & summary["learnability_pass"].astype(bool)
    ].sort_values(["validation_oos_score_sum", "oos_dd_risk_percent"], ascending=[True, True])
    selected: list[f07b.RiskLabelVariant] = []
    seen: set[str] = set()
    for target_id in pool["target_id"]:
        target = str(target_id)
        if target in seen or target not in all_variants:
            continue
        selected.append(all_variants[target])
        seen.add(target)
        if len(selected) >= REPAIR_TARGET_COUNT:
            break
    if not selected:
        raise RuntimeError("No preserved Frontier07B variants available for capped repair.")
    return selected


def train_repair_models(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[f07b.RiskLabelVariant],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    path = f07b.path_arrays(full, raw, f07b.HORIZON_BARS)
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate([
        np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
        for split in ("train", "validation", "oos")
    ])

    candidate_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    label_distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []

    for variant_index, variant in enumerate(variants, start=1):
        labels, _, diagnostics = f07b.build_risk_labels(path, variant)
        label_distribution_rows.extend(f07b.label_distribution(full, labels, variant.variant_id, "risk_label_repair_candidate(위험 라벨 수리 후보)"))
        for spec_index, spec in enumerate(REPAIR_MODEL_SPECS, start=1):
            rows = fit_repair_target(
                full=full,
                x_all=x_all,
                labels=labels,
                fwd_return=path["fwd_return"],
                variant=variant,
                train_mask=train_mask,
                sample_indices=sample_indices,
                model_spec=spec,
                model_instance_id=f"v{variant_index:02d}_rw{spec_index:02d}",
                model_dir=MODEL_DIR / f"v{variant_index:02d}",
                extra={f"diagnostic_{key}": value for key, value in diagnostics.items()},
                classification_rows=classification_rows,
                parity_rows=parity_rows,
                skipped_rows=skipped_rows,
            )
            candidate_metrics.extend(rows)

    references = reference_pack()
    candidate_summary = f07b.build_candidate_summary(candidate_metrics, classification_rows, parity_rows, references)
    return {
        "candidate_metrics": candidate_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": label_distribution_rows,
        "skipped": skipped_rows,
        "candidate_summary": candidate_summary,
        "references": references,
    }


def fit_repair_target(
    *,
    full: pd.DataFrame,
    x_all: np.ndarray,
    labels: np.ndarray,
    fwd_return: np.ndarray,
    variant: f07b.RiskLabelVariant,
    train_mask: np.ndarray,
    sample_indices: np.ndarray,
    model_spec: RepairModelSpec,
    model_instance_id: str,
    model_dir: Path,
    extra: dict[str, Any],
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    skipped_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
    if missing:
        skipped_rows.append({"target_id": variant.variant_id, "model_id": model_spec.model_id, "reason": f"missing_train_classes={missing}"})
        return []
    model = clone(model_spec.estimator)
    model.fit(x_all[train_mask], labels[train_mask])
    probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
    pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
    signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

    io_path(model_dir).mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"{model_instance_id}.joblib"
    onnx_path = model_dir / f"{model_instance_id}.onnx"
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
    parity_rows.append({
        "target_id": variant.variant_id,
        "target_kind": "risk_label_candidate(위험 라벨 후보)",
        "model_id": model_spec.model_id,
        "model_instance_id": model_instance_id,
        "directional_weight": model_spec.directional_weight,
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": export_meta["sha256"],
        "joblib_path": model_path.as_posix(),
        "joblib_sha256": sha256_file(model_path),
        "parity_passed": bool(parity["passed"]),
        "parity_max_abs_diff": parity["max_abs_diff"],
        "parity_mean_abs_diff": parity["mean_abs_diff"],
        "rows_checked": parity["rows"],
    })
    for split in ("train", "validation", "oos"):
        split_mask = full["split"].astype(str).eq(split).to_numpy()
        y_true = labels[split_mask]
        y_pred = pred_label[split_mask]
        classification_rows.append({
            "target_id": variant.variant_id,
            "target_kind": "risk_label_candidate(위험 라벨 후보)",
            "model_id": model_spec.model_id,
            "model_instance_id": model_instance_id,
            "directional_weight": model_spec.directional_weight,
            "split": split,
            "rows": int(split_mask.sum()),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)),
            "pred_short": int((y_pred == 0).sum()),
            "pred_flat": int((y_pred == 1).sum()),
            "pred_long": int((y_pred == 2).sum()),
            "true_short": int((y_true == 0).sum()),
            "true_flat": int((y_true == 1).sum()),
            "true_long": int((y_true == 2).sum()),
        })
    rows = f07b.evaluate_model_signal(
        full,
        signal,
        fwd_return,
        variant,
        variant.variant_id,
        "risk_label_candidate(위험 라벨 후보)",
        model_spec.model_id,
        model_instance_id,
    )
    for row in rows:
        row["directional_weight"] = model_spec.directional_weight
        row["repair_contract"] = "class_prior_density_bridge_argmax_only(클래스 사전분포 밀도 브리지, 최대확률 전용)"
        row.update(extra)
    return rows


def reference_pack() -> dict[str, Any]:
    if not f07b.path_exists(F07B_REFERENCE_METRICS):
        raise FileNotFoundError(F07B_REFERENCE_METRICS)
    refs = pd.read_csv(str(io_path(F07B_REFERENCE_METRICS)), encoding="utf-8-sig")
    label_v1 = refs[refs["target_id"].eq("label_v1_argmax_reference")]
    return {
        "label_v1_argmax": f07b.best_model_summary(label_v1, "label_v1_argmax_reference"),
        "frontier04_locked_path_trainable": f07b.parse_report_reference(f07b.F04D_REPORT, "frontier04D_locked_path_argmax_reference"),
        "frontier06_best_selective": f07b.parse_report_reference(f07b.F06B_REPORT, "frontier06B_best_selective_reference"),
    }


def build_final(
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    variants: list[f07b.RiskLabelVariant],
) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if row.get("strict_scout_clue_pass")))
    preserved_rows = int(sum(1 for row in candidates if row.get("preserved_clue_pass")))
    best = candidates[0] if candidates else {}
    if strict_rows:
        status = "class_prior_density_bridge_strict_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run = NEXT_CLUE_RUN_ID
    elif preserved_rows:
        status = "class_prior_density_bridge_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "class_prior_density_bridge_no_repair_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "repair_scope": "capped repair: top 4 Frontier07B preserved variants x 4 directional weights(상한 있는 수리: 전선07B 보존 변형 4개 x 방향 가중치 4개)",
        "variant_count": len(variants),
        "model_count": len(REPAIR_MODEL_SPECS) * len(variants),
        "strict_scout_clue_rows": strict_rows,
        "preserved_clue_rows": preserved_rows,
        "best_candidate_row": best,
        "references": result["references"],
        "data_integrity": {
            **source_integrity,
            "feature_label_boundary": "same Frontier07B labels and fixed feature_set_v2; repair changes class prior weight only(같은 전선07B 라벨과 고정 피처 세트 v2, 수리는 클래스 사전 가중치만 변경)",
            "split_boundary": "models fit train only; validation/OOS read only(모델은 학습만 적합, 검증/표본밖은 판독 전용)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        "model_validation": {
            "repair_axis": "directional class-prior bridge between plain and balanced logreg(기본/균형 로지스틱 회귀 사이 방향 클래스 사전분포 브리지)",
            "threshold_policy": "argmax only, no searched threshold(최대확률 전용, 탐색 임계값 없음)",
            "validation_judgment": "exploratory(탐색)",
        },
        "runtime_parity": {
            "onnx_parity": "checked for each repair model(각 수리 모델에서 확인)",
            "runtime_claim_boundary": "research_only_no_mt5(연구 전용, MT5 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f07b.F07B_REPORT.as_posix() if hasattr(f07b, "F07B_REPORT") else F07B_SUMMARY.as_posix()],
            "producer": "stage_pipelines/stage_frontier_07/frontier07c_class_prior_density_bridge_repair.py",
            "consumer": next_run,
            "availability": "ignored_run_artifacts_with_tracked_report(무시 실행 산출물 + 추적 보고서)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "feature_order_hash": ordered_hash(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any], variants: list[f07b.RiskLabelVariant]) -> dict[str, Path]:
    artifacts = {
        "selected_variants": RUN_ROOT / "selected_repair_variants.csv",
        "candidate_metrics": RUN_ROOT / "repair_model_metrics.csv",
        "candidate_summary": RUN_ROOT / "repair_candidate_summary.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "skipped": RUN_ROOT / "skipped_targets.csv",
        "integrity": RUN_ROOT / "integrity.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    pd.DataFrame([variant.__dict__ for variant in variants]).to_csv(str(io_path(artifacts["selected_variants"])), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["candidate_metrics"]).to_csv(str(io_path(artifacts["candidate_metrics"])), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["candidate_summary"]).to_csv(str(io_path(artifacts["candidate_summary"])), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["classification_metrics"]).to_csv(str(io_path(artifacts["classification_metrics"])), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["onnx_parity"]).to_csv(str(io_path(artifacts["onnx_parity"])), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["label_distribution"]).to_csv(str(io_path(artifacts["label_distribution"])), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["skipped"]).to_csv(str(io_path(artifacts["skipped"])), index=False, encoding="utf-8-sig")
    f07b.write_json(artifacts["integrity"], final["data_integrity"])
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_07/frontier07c_class_prior_density_bridge_repair.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_07/frontier07c_class_prior_density_bridge_repair.py")),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if f07b.path_exists(path) and name != "run_manifest"
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    f07b.write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier07C Class Prior Density Bridge Repair Report(전선07C 클래스 사전분포 밀도 브리지 수리 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier07B(전선07B)의 preserved variants(보존 변형) 상위 4개에 directional class-prior weights(방향 클래스 사전분포 가중치) 1.25~2.00을 적용해 argmax-only(최대확률 전용) repair(수리)를 실행했습니다.

Effect(효과): threshold search(임계값 탐색) 없이 sparse plain model(희소 기본 모델)과 overactive balanced model(과활성 균형 모델) 사이의 density bridge(밀도 브리지)를 시험했습니다.

## Best Repair Read(최상위 수리 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- strict_scout_clue_pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass', False)}`
- preserved_clue_pass(보존 단서 통과): `{best.get('preserved_clue_pass', False)}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{f07b.fmt(best.get('validation_profit_factor'))}` / `{f07b.fmt(best.get('validation_trades_per_day'))}/day` / `{f07b.fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{f07b.fmt(best.get('oos_profit_factor'))}` / `{f07b.fmt(best.get('oos_trades_per_day'))}/day` / `{f07b.fmt(best.get('oos_dd_risk_percent'))}%`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed', False)}`

## Result Boundary(결과 경계)

- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- repair scope(수리 범위): `{final['repair_scope']}`
- runtime boundary(런타임 경계): `{final['runtime_parity']['runtime_claim_boundary']}`

## Artifacts(산출물)

- repair candidate summary(수리 후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- repair model metrics(수리 모델 지표): `{artifacts['candidate_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 실행 전 검토), 없으면 stage closeout(단계 마감)로 넘기는 것입니다. Effect(효과)는 같은 수리를 반복하지 않고 capped repair(상한 있는 수리) 원칙을 지키는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    f07b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": final["status"],
        "current_judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": final["created_at_utc"],
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    f07b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    f07b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final))
    f07b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    for row in ledger_rows(final, artifacts):
        f07b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f07b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )


def current_state_text(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier07C(전선07C)는 class-prior density bridge repair(클래스 사전분포 밀도 브리지 수리)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{best.get('candidate_id', 'none')}` with strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}` and preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`.

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 실행 전 검토), 없으면 stage closeout(단계 마감)을 여는 것입니다. Effect(효과)는 capped repair(상한 있는 수리)를 반복하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any]) -> str:
    return f"""# Stage Frontier 07 Selection Status(전선 07단계 선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{RUN_ID}`

Judgment(판정): `{final['judgment']}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "risk_label_repair(위험 라벨 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["strict_scout_clue_rows"]),
        "claim_boundary": "class_prior_repair_no_threshold_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_class_prior_repair",
        "subrun_id": f"{RUN_ID}__tier_a_class_prior_repair",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "risk_label_repair_not_runtime(위험 라벨 수리, 런타임 아님)",
        "primary_kpi": f07b.primary_kpi_text(best),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "class_prior_repair_only(클래스 사전분포 수리 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can class-prior bridge recover density without threshold search?(클래스 사전분포 브리지가 임계값 탐색 없이 밀도를 회복할 수 있는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier07b_preserved_clue_to_frontier07c_capped_repair(전선07B 보존 단서에서 전선07C 상한 수리)",
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "risk_label_repair(위험 라벨 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_class_prior_repair",
            "subrun_id": f"{RUN_ID}__tier_a_class_prior_repair",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "risk_label_repair_not_runtime(위험 라벨 수리, 런타임 아님)",
            "primary_kpi": f07b.primary_kpi_text(best),
            "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())

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


STAGE_ID = "stage_frontier_14__daily_session_opportunity_budget_onnx_scout"
RUN_ID = "frontier14B_daily_session_opportunity_budget_proxy_scout_v1"
RUN_NUMBER = "frontier14B"
PARENT_RUN_ID = "frontier14A_stage_open_daily_session_opportunity_budget_onnx_scout_v1"
NEXT_STRICT_RUN_ID = "frontier14C_grok_pre_expensive_daily_session_opportunity_budget_review_v1"
NEXT_REPAIR_RUN_ID = "frontier14C_daily_session_opportunity_budget_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_14/frontier14b_daily_session_opportunity_budget_proxy_scout.py")
STAGE_OPEN_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f12b.LABEL_NAMES
MODEL_ID_SHORT = f12b.MODEL_ID_SHORT
UTILITY_COST_MULTIPLIER = 1.0
MAE_PENALTY = 0.65
EARLY_MAE_PENALTY = 0.35
MIN_POSITIVE_UTILITY = 0.0


@dataclass(frozen=True)
class OpportunityVariant:
    variant_id: str
    bucket_rule: str
    quota_per_bucket: int
    hold_bars: int
    early_window_bars: int
    target_multiplier: float
    adverse_cap_multiplier: float
    early_adverse_cap_multiplier: float
    recovery_floor_multiplier: float
    utility_cost_multiplier: float
    mae_penalty: float
    early_mae_penalty: float
    min_positive_utility: float
    tie_break: str


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_open = read_json(STAGE_OPEN_SUMMARY)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    variants = build_variants()
    result = train_and_evaluate(full, raw, feature_order, variants)
    final = build_final(created_at, result, variants, source_integrity, feature_order, stage_open)
    artifacts = write_artifacts(result, final, variants)
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


def build_variants() -> list[OpportunityVariant]:
    specs = [
        ("f14b_day_q6_h8", "broker_day(브로커 일자)", 6, 8, 2),
        ("f14b_cash_q8_h8", "broker_day_x_cash_session(브로커 일자와 현금장 세션)", 8, 8, 2),
        ("f14b_cash_q10_h12", "broker_day_x_cash_session(브로커 일자와 현금장 세션)", 10, 12, 3),
    ]
    return [
        OpportunityVariant(
            variant_id=variant_id,
            bucket_rule=bucket_rule,
            quota_per_bucket=quota,
            hold_bars=hold,
            early_window_bars=early,
            target_multiplier=1.0,
            adverse_cap_multiplier=1.0,
            early_adverse_cap_multiplier=1.0,
            recovery_floor_multiplier=0.0,
            utility_cost_multiplier=UTILITY_COST_MULTIPLIER,
            mae_penalty=MAE_PENALTY,
            early_mae_penalty=EARLY_MAE_PENALTY,
            min_positive_utility=MIN_POSITIVE_UTILITY,
            tie_break="earliest_timestamp_then_larger_abs_utility(빠른 시각 후 큰 절대 효용)",
        )
        for variant_id, bucket_rule, quota, hold, early in specs
    ]


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[OpportunityVariant],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values(피처 행렬 NaN 또는 무한대).")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate([
        np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
        for split in ("train", "validation", "oos")
    ])
    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    oracle_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    target_diagnostics: list[dict[str, Any]] = []
    label_model_density_rows: list[dict[str, Any]] = []

    for variant in variants:
        path = opportunity_path_arrays(full, raw, variant)
        labels, oracle_signal, diagnostics = build_opportunity_labels(full, path, variant)
        target_diagnostics.append({"target_id": variant.variant_id, **json_ready(asdict(variant)), **diagnostics})
        distribution_rows.extend(f12b.label_distribution(full, labels, variant))
        oracle_metrics.extend(f12b.evaluate_all_splits(
            full,
            oracle_signal,
            path["fwd_return"],
            variant,
            "oracle_opportunity_budget_replay(오라클 기회 예산 재생)",
            "oracle",
        ))
        missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
        if missing:
            skipped_rows.append({
                "target_id": variant.variant_id,
                "reason": f"missing_train_classes={missing}",
                "label_boundary": "pre_registered_quota_future_path_label_not_runtime(사전 등록 할당 미래 경로 라벨, 런타임 아님)",
            })
            continue
        for spec in f04d.MODEL_SPECS:
            candidate_id = f"{variant.variant_id}__{MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:10])}"
            model_instance_id = f"f14b_{candidate_id}"
            model = clone(spec.estimator)
            model.fit(x_all[train_mask], labels[train_mask])
            probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
            pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
            signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")
            target_dir = MODEL_DIR / variant.variant_id
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
            parity_rows.append({
                "candidate_id": candidate_id,
                "target_id": variant.variant_id,
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
            })
            classification_rows.extend(f12b.classification_metrics(
                full, labels, pred_label, variant, spec.model_id, model_instance_id, candidate_id
            ))
            split_rows = f12b.evaluate_all_splits(
                full,
                signal,
                path["fwd_return"],
                variant,
                "argmax_opportunity_budget_model_signal(최대확률 기회 예산 모델 신호)",
                candidate_id,
                model_id=spec.model_id,
                model_instance_id=model_instance_id,
            )
            model_metrics.extend(split_rows)
            subperiod_metrics.extend(f12b.evaluate_subperiods(
                full, signal, path["fwd_return"], variant, candidate_id, spec.model_id, model_instance_id
            ))
            label_model_density_rows.extend(density_gap_rows(full, oracle_signal, signal, variant, candidate_id, spec.model_id, model_instance_id))

    candidate_summary = f12b.build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows)
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
    }


def opportunity_path_arrays(full: pd.DataFrame, raw: pd.DataFrame, variant: OpportunityVariant) -> dict[str, np.ndarray]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    base = raw["log_close"].to_numpy(dtype="float64")[raw_indexes]
    log_close = raw["log_close"].to_numpy(dtype="float64")
    log_high = raw["log_high"].to_numpy(dtype="float64")
    log_low = raw["log_low"].to_numpy(dtype="float64")
    high_steps = np.vstack([log_high[raw_indexes + step] - base for step in range(1, variant.hold_bars + 1)])
    low_steps = np.vstack([base - log_low[raw_indexes + step] for step in range(1, variant.hold_bars + 1)])
    early_end = min(variant.early_window_bars, variant.hold_bars)
    fwd_return = log_close[raw_indexes + variant.hold_bars] - base
    long_mae = np.nanmax(low_steps, axis=0)
    short_mae = np.nanmax(high_steps, axis=0)
    early_long_mae = np.nanmax(low_steps[:early_end], axis=0)
    early_short_mae = np.nanmax(high_steps[:early_end], axis=0)
    long_utility = (
        fwd_return
        - variant.mae_penalty * long_mae
        - variant.early_mae_penalty * early_long_mae
        - variant.utility_cost_multiplier * f12b.scout.ROUGH_COST_LOG_RETURN
    )
    short_utility = (
        -fwd_return
        - variant.mae_penalty * short_mae
        - variant.early_mae_penalty * early_short_mae
        - variant.utility_cost_multiplier * f12b.scout.ROUGH_COST_LOG_RETURN
    )
    return {
        "long_mfe": np.nanmax(high_steps, axis=0),
        "long_mae": long_mae,
        "short_mfe": np.nanmax(low_steps, axis=0),
        "short_mae": short_mae,
        "early_long_mae": early_long_mae,
        "early_short_mae": early_short_mae,
        "fwd_return": fwd_return,
        "long_utility": long_utility,
        "short_utility": short_utility,
    }


def build_opportunity_labels(
    full: pd.DataFrame,
    path: dict[str, np.ndarray],
    variant: OpportunityVariant,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    labels = np.ones(len(full), dtype="int64")
    signal = np.zeros(len(full), dtype="int8")
    timestamps = pd.to_datetime(full["timestamp"], errors="raise")
    buckets = opportunity_buckets(full, timestamps, variant)
    selected_entries = 0
    selected_buckets = 0
    bucket_sizes: list[int] = []
    for bucket in sorted(set(str(item) for item in buckets if str(item) != "skip")):
        row_idx = np.flatnonzero(buckets == bucket)
        if len(row_idx) == 0:
            continue
        bucket_sizes.append(len(row_idx))
        entries: list[tuple[float, pd.Timestamp, int, int]] = []
        for idx in row_idx:
            long_u = float(path["long_utility"][idx])
            short_u = float(path["short_utility"][idx])
            timestamp = timestamps.iloc[int(idx)]
            if math.isfinite(long_u) and long_u > variant.min_positive_utility:
                entries.append((-long_u, timestamp, int(idx), 1))
            if math.isfinite(short_u) and short_u > variant.min_positive_utility:
                entries.append((-short_u, timestamp, int(idx), -1))
        entries.sort(key=lambda item: (item[0], item[1], item[2], -item[3]))
        used_rows: set[int] = set()
        bucket_selected = 0
        for _, _, idx, side in entries:
            if idx in used_rows:
                continue
            signal[idx] = side
            labels[idx] = 2 if side > 0 else 0
            used_rows.add(idx)
            bucket_selected += 1
            selected_entries += 1
            if bucket_selected >= variant.quota_per_bucket:
                break
        if bucket_selected:
            selected_buckets += 1
    diagnostics = {
        "label_boundary": "pre_registered_quota_future_path_label_not_runtime(사전 등록 할당 미래 경로 라벨, 런타임 아님)",
        "oracle_long_count": int((signal == 1).sum()),
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "selected_entries": int(selected_entries),
        "selected_buckets": int(selected_buckets),
        "bucket_count": int(len(set(str(item) for item in buckets if str(item) != "skip"))),
        "mean_bucket_size": float(np.mean(bucket_sizes)) if bucket_sizes else 0.0,
        "mean_long_utility": float(np.nanmean(path["long_utility"])),
        "mean_short_utility": float(np.nanmean(path["short_utility"])),
        "label_long_short_balance": float((signal == 1).sum() / max(1, int((signal != 0).sum()))),
    }
    return labels, signal, diagnostics


def opportunity_buckets(full: pd.DataFrame, timestamps: pd.Series, variant: OpportunityVariant) -> np.ndarray:
    day = timestamps.dt.strftime("%Y-%m-%d").astype(str).to_numpy()
    if variant.variant_id.startswith("f14b_day"):
        return np.array([f"day_{item}" for item in day], dtype=object)
    cash = pd.to_numeric(full["is_us_cash_open"], errors="coerce").fillna(0.0).to_numpy(dtype="float64") > 0
    buckets = np.array(["skip"] * len(full), dtype=object)
    buckets[cash] = np.array([f"cash_{item}" for item in day[cash]], dtype=object)
    return buckets


def density_gap_rows(
    full: pd.DataFrame,
    label_signal: np.ndarray,
    model_signal: np.ndarray,
    variant: OpportunityVariant,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        timestamps = pd.to_datetime(full.loc[mask, "timestamp"], errors="raise").reset_index(drop=True)
        days = f12b.scout.count_scope_days(timestamps) if len(timestamps) else 0
        label_count = int((label_signal[mask] != 0).sum())
        model_count = int((model_signal[mask] != 0).sum())
        rows.append({
            "candidate_id": candidate_id,
            "target_id": variant.variant_id,
            "model_id": model_id,
            "model_instance_id": model_instance_id,
            "split": split,
            "days_in_scope": days,
            "label_opportunity_count": label_count,
            "model_trade_count": model_count,
            "label_opportunities_per_day": float(label_count / days) if days else 0.0,
            "model_trades_per_day": float(model_count / days) if days else 0.0,
            "model_minus_label_density": float((model_count - label_count) / days) if days else 0.0,
        })
    return rows


def build_final(
    created_at: str,
    result: dict[str, Any],
    variants: list[OpportunityVariant],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_open: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    best = candidate_summary[0] if candidate_summary else {}
    status = "opportunity_budget_strict_scout_clue_no_authority" if strict_rows else (
        "opportunity_budget_preserved_clue_no_authority" if preserved_rows else "opportunity_budget_no_strict_clue_no_authority"
    )
    judgment = "strict_scout_clue_candidate(엄격 탐색 단서 후보)" if strict_rows else (
        "preserved_clue_candidate(보존 단서 후보)" if preserved_rows else "negative_memory_candidate(부정 기억 후보)"
    )
    next_run_id = NEXT_STRICT_RUN_ID if strict_rows else NEXT_REPAIR_RUN_ID
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
        "model_count": len(f04d.MODEL_SPECS),
        "stage_open_status": stage_open.get("status", ""),
        "source_integrity": source_integrity,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "data_integrity": data_integrity_record(source_integrity),
        "model_validation": model_validation_record(best),
        "artifact_lineage": artifact_lineage_record(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_if_strict(엄격 단서가 있으면 그록 비싼 검증 전 검토 필요)",
        "mt5_status": "not_run_proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
    }


def data_integrity_record(source_integrity: dict[str, Any]) -> dict[str, Any]:
    return {
        "data_source": f03b.DATASET_PATH.as_posix(),
        "time_axis": "US100 M5 closed-bar timestamp order(US100 5분봉 확정봉 시각 순서)",
        "sample_scope": "Tier A train/validation/OOS fixed split(티어 A 학습/검증/표본밖 고정 분할)",
        "feature_label_boundary": "features use closed bars; labels use future path only as supervised target(피처는 확정봉, 라벨은 감독 표적으로만 미래 경로 사용)",
        "split_boundary": "no validation/OOS recalibration(검증/표본밖 재보정 없음)",
        "leakage_risk": "quota retuning after metrics is forbidden(지표 확인 뒤 할당량 재조정 금지)",
        "data_hash_or_identity": source_integrity,
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }


def model_validation_record(best: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fixed sklearn-to-ONNX 3-class argmax(고정 sklearn-to-ONNX 3클래스 최대확률)",
        "target_and_label": "daily/session opportunity budget labels(일별/세션별 기회 예산 라벨)",
        "split_method": "fixed train/validation/OOS split(고정 학습/검증/표본밖 분할)",
        "selection_metric": "strict/preserved scout clue plus aspiration distance(엄격/보존 탐색 단서와 목표 거리)",
        "threshold_policy": "argmax_only_no_threshold_search(최대확률 전용, 임계값 탐색 없음)",
        "overfit_risk": "three pre-registered quota variants only(사전 등록 할당 변형 3개만)",
        "calibration_risk": "probabilities used for argmax ranking only(확률은 최대확률 순위로만 사용)",
        "comparison_baseline": "Frontier13 reference-only sparse surface(프론티어13 참조 전용 희소 표면)",
        "validation_judgment": "exploratory(탐색)",
        "best_candidate": best.get("candidate_id", "none"),
    }


def artifact_lineage_record() -> dict[str, Any]:
    return {
        "source_inputs": [f03b.DATASET_PATH.as_posix(), f03b.FEATURE_ORDER_PATH.as_posix(), STAGE_OPEN_SUMMARY.as_posix()],
        "producer": SCRIPT_PATH.as_posix(),
        "consumer": REPORT_PATH.as_posix(),
        "availability": "generated_ignored_with_manifest_for_models(모델은 생성되고 목록으로 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
    }


def write_artifacts(
    result: dict[str, Any],
    final: dict[str, Any],
    variants: list[OpportunityVariant],
) -> dict[str, Path]:
    artifacts = {
        "variant_manifest": RUN_ROOT / "variant_manifest.csv",
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
    write_json(artifacts["run_manifest"], {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "stage_open_summary": artifact_identity(STAGE_OPEN_SUMMARY),
        "dataset": artifact_identity(f03b.DATASET_PATH),
        "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
        "artifacts": {key: path.as_posix() for key, path in artifacts.items()},
    })
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier14B Daily/Session Opportunity Budget Proxy Scout(프론티어14B 일별/세션별 기회 예산 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): pre-registered quota labels(사전 등록 할당 라벨) 3개와 fixed argmax ONNX models(고정 최대확률 온엑스 모델)를 학습/평가했습니다.

Effect(효과): label-side opportunity density(라벨 쪽 기회 빈도)와 model argmax density(모델 최대확률 빈도)를 분리해서 upstream frequency label(상류 빈도 라벨)이 모델로 전달되는지 측정했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- label/model density gap(라벨/모델 빈도 격차): `{artifacts['label_model_density_gap'].as_posix()}`
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
    return "\n".join([
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
    ])


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

Action(행동): Frontier14B(프론티어14B)는 daily/session opportunity budget labels(일별/세션별 기회 예산 라벨)를 ONNX proxy scout(온엑스 프록시 탐색)로 시험했습니다.

Effect(효과): best candidate(최고 후보) `{best.get('candidate_id', 'none')}`의 validation/OOS PF-density-DD(검증/표본밖 수익 팩터-빈도-손실폭)와 label/model density gap(라벨/모델 빈도 격차)을 기록했고, authority claim(권위 주장)은 하지 않았습니다.

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

Best validation/OOS PF-density-DD(최고 검증/표본밖 수익 팩터-빈도-손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%` and `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`

Key artifacts(핵심 산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['label_model_density_gap'].as_posix()}`
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier14 Review Index(프론티어14 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{PARENT_RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용).
- `{RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`.
- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier14B Required Gate Coverage Audit(프론티어14B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): pre-registered quota variants(사전 등록 할당 변형) executed(실행됨)
- kpi_contract_audit(KPI 계약 감사): validation/OOS PF-density-DD and subperiod DD(검증/표본밖 수익 팩터-빈도-손실폭과 하위기간 손실폭) recorded(기록됨)
- data_integrity_gate(데이터 무결성 게이트): `{final['data_integrity']['integrity_judgment']}`
- model_validation_gate(모델 검증 게이트): `{final['model_validation']['validation_judgment']}`
- artifact_lineage_gate(산출물 계보 게이트): `{final['artifact_lineage']['lineage_judgment']}`
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "daily_session_opportunity_budget_proxy_scout(일별/세션별 기회 예산 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_wfo_no_mt5_no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "proxy_scout_no_wfo_no_mt5_no_authority_goal_claim",
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
        "scoreboard_lane": "daily_session_opportunity_budget_proxy_scout(일별/세션별 기회 예산 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "pre_registered_quota_argmax_only_no_threshold_no_wfo_no_mt5_no_authority(사전 등록 할당, 최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_opportunity_budget_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_opportunity_budget_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "opportunity_budget_proxy_not_runtime(기회 예산 프록시, 런타임 아님)",
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

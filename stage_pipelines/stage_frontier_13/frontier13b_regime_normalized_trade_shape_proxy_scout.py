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


STAGE_ID = "stage_frontier_13__regime_normalized_trade_shape_onnx_scout"
RUN_ID = "frontier13B_regime_normalized_trade_shape_proxy_scout_v1"
RUN_NUMBER = "frontier13B"
PARENT_RUN_ID = "frontier13A_stage_open_regime_normalized_trade_shape_onnx_scout_v1"
NEXT_STRICT_RUN_ID = "frontier13C_grok_pre_expensive_regime_normalized_review_v1"
NEXT_REPAIR_RUN_ID = "frontier13C_regime_normalized_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_13/frontier13b_regime_normalized_trade_shape_proxy_scout.py")
STAGE_OPEN_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"

LABEL_ORDER = f04d.LABEL_ORDER
HOLD_MAX_BARS = 12
SCALE_QUANTILE = 0.90
GLOBAL_FALLBACK_MIN_ROWS = 80


@dataclass(frozen=True)
class RegimeVariant:
    variant_id: str
    scheme_id: str
    hold_bars: int
    early_window_bars: int
    target_multiplier: float
    adverse_cap_multiplier: float
    early_adverse_cap_multiplier: float
    recovery_floor_multiplier: float
    score_margin_multiplier: float
    scale_quantile: float
    base_scale_log_return: float
    bucket_count: int


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_open = read_json(STAGE_OPEN_SUMMARY)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    variants, bucket_tables = build_variants(full, raw)
    result = train_and_evaluate(full, raw, feature_order, variants, bucket_tables)
    final = build_final(created_at, result, variants, source_integrity, feature_order, stage_open)
    artifacts = write_artifacts(result, final, variants, bucket_tables)
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


def build_variants(full: pd.DataFrame, raw: pd.DataFrame) -> tuple[list[RegimeVariant], dict[str, list[dict[str, Any]]]]:
    specs = [
        ("cash_vol_h6", 6, 2, 0.72, 0.42, 0.24, 0.08, 0.06),
        ("session_trend_h9", 9, 3, 0.86, 0.52, 0.30, 0.10, 0.08),
        ("vol_squeeze_h12", 12, 4, 1.00, 0.62, 0.36, 0.12, 0.10),
    ]
    variants: list[RegimeVariant] = []
    bucket_tables: dict[str, list[dict[str, Any]]] = {}
    for scheme, hold, early, target, cap, early_cap, recovery, margin in specs:
        fwd = hold_return(full, raw, hold)
        buckets = regime_buckets(full, scheme)
        scales, table, global_scale = train_only_bucket_scales(full, fwd, buckets, scheme, hold)
        variant_id = (
            f"f13b_{scheme}_t{target:.2f}_cap{cap:.2f}_ecap{early_cap:.2f}_rec{recovery:.2f}"
        ).replace(".", "p")
        bucket_tables[variant_id] = table
        variants.append(
            RegimeVariant(
                variant_id=variant_id,
                scheme_id=scheme,
                hold_bars=hold,
                early_window_bars=early,
                target_multiplier=target,
                adverse_cap_multiplier=cap,
                early_adverse_cap_multiplier=early_cap,
                recovery_floor_multiplier=recovery,
                score_margin_multiplier=margin,
                scale_quantile=SCALE_QUANTILE,
                base_scale_log_return=global_scale,
                bucket_count=len(set(buckets)),
            )
        )
    return variants, bucket_tables


def hold_return(full: pd.DataFrame, raw: pd.DataFrame, hold: int) -> np.ndarray:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    return log_close[raw_indexes + hold] - log_close[raw_indexes]


def regime_buckets(full: pd.DataFrame, scheme: str) -> np.ndarray:
    train = full["split"].astype(str).eq("train").to_numpy()
    vol = pd.to_numeric(full["atr_14_over_atr_50"], errors="coerce").fillna(1.0).to_numpy(dtype="float64")
    trend = np.abs(pd.to_numeric(full["di_spread_14"], errors="coerce").fillna(0.0).to_numpy(dtype="float64"))
    squeeze = pd.to_numeric(full["bb_squeeze"], errors="coerce").fillna(0.0).to_numpy(dtype="float64") > 0
    cash = pd.to_numeric(full["is_us_cash_open"], errors="coerce").fillna(0.0).to_numpy(dtype="float64") > 0
    early = pd.to_numeric(full["is_first_30m_after_open"], errors="coerce").fillna(0.0).to_numpy(dtype="float64") > 0
    late = pd.to_numeric(full["is_last_30m_before_cash_close"], errors="coerce").fillna(0.0).to_numpy(dtype="float64") > 0
    vol_bucket = quantile_bucket(vol, train, 3, "vol")
    trend_bucket = quantile_bucket(trend, train, 3, "trend")
    if scheme == "cash_vol_h6":
        return np.array([f"cash{int(c)}_{v}" for c, v in zip(cash, vol_bucket)], dtype=object)
    if scheme == "session_trend_h9":
        session = np.where(early, "early", np.where(late, "late", np.where(cash, "cash", "off")))
        return np.array([f"{s}_{t}" for s, t in zip(session, trend_bucket)], dtype=object)
    if scheme == "vol_squeeze_h12":
        return np.array([f"{v}_squeeze{int(s)}" for v, s in zip(vol_bucket, squeeze)], dtype=object)
    raise ValueError(f"Unknown scheme(알 수 없는 방식): {scheme}")


def quantile_bucket(values: np.ndarray, train_mask: np.ndarray, bucket_count: int, prefix: str) -> np.ndarray:
    train_values = values[train_mask]
    cuts = np.nanquantile(train_values[np.isfinite(train_values)], np.linspace(0, 1, bucket_count + 1)[1:-1])
    bucket = np.digitize(values, cuts, right=False)
    return np.array([f"{prefix}{int(item)}" for item in bucket], dtype=object)


def train_only_bucket_scales(
    full: pd.DataFrame,
    fwd: np.ndarray,
    buckets: np.ndarray,
    scheme: str,
    hold: int,
) -> tuple[np.ndarray, list[dict[str, Any]], float]:
    train = full["split"].astype(str).eq("train").to_numpy()
    abs_train = np.abs(fwd[train])
    global_scale = float(np.nanquantile(abs_train[np.isfinite(abs_train)], SCALE_QUANTILE))
    if not math.isfinite(global_scale) or global_scale <= 0:
        raise RuntimeError("Invalid global train scale(전역 학습 척도 오류).")
    table: list[dict[str, Any]] = []
    scale_by_bucket: dict[str, float] = {}
    for bucket in sorted(set(str(item) for item in buckets)):
        mask = train & (buckets.astype(str) == bucket)
        count = int(mask.sum())
        if count >= GLOBAL_FALLBACK_MIN_ROWS:
            scale = float(np.nanquantile(np.abs(fwd[mask]), SCALE_QUANTILE))
            source = "bucket_train_quantile(버킷 학습 분위수)"
        else:
            scale = global_scale
            source = "global_fallback(전역 대체)"
        if not math.isfinite(scale) or scale <= 0:
            scale = global_scale
            source = "global_fallback_invalid_bucket(버킷 오류 전역 대체)"
        scale_by_bucket[bucket] = scale
        table.append({
            "scheme_id": scheme,
            "hold_bars": hold,
            "bucket": bucket,
            "train_rows": count,
            "scale_log_return": scale,
            "scale_source": source,
        })
    scales = np.array([scale_by_bucket.get(str(bucket), global_scale) for bucket in buckets], dtype="float64")
    return scales, table, global_scale


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[RegimeVariant],
    bucket_tables: dict[str, list[dict[str, Any]]],
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

    for variant in variants:
        buckets = regime_buckets(full, variant.scheme_id)
        scales = scale_array_for_variant(full, raw, variant, buckets, bucket_tables[variant.variant_id])
        path = regime_shape_path_arrays(full, raw, variant, scales)
        labels, oracle_signal, diagnostics = build_regime_shape_labels(path, variant)
        target_diagnostics.append({"target_id": variant.variant_id, **json_ready(asdict(variant)), **diagnostics})
        distribution_rows.extend(f12b.label_distribution(full, labels, variant))
        oracle_metrics.extend(f12b.evaluate_all_splits(
            full,
            oracle_signal,
            path["fwd_return"],
            variant,
            "oracle_regime_label_replay(오라클 레짐 라벨 재생)",
            "oracle",
        ))
        missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
        if missing:
            skipped_rows.append({
                "target_id": variant.variant_id,
                "reason": f"missing_train_classes={missing}",
                "label_boundary": "train_only_regime_scale(학습 전용 레짐 척도)",
            })
            continue
        for spec in f04d.MODEL_SPECS:
            candidate_id = f"{variant.variant_id}__{f12b.MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:10])}"
            model_instance_id = f"f13b_{candidate_id}"
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
                "argmax_regime_model_signal(최대확률 레짐 모델 신호)",
                candidate_id,
                model_id=spec.model_id,
                model_instance_id=model_instance_id,
            )
            model_metrics.extend(split_rows)
            subperiod_metrics.extend(f12b.evaluate_subperiods(
                full, signal, path["fwd_return"], variant, candidate_id, spec.model_id, model_instance_id
            ))

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
    }


def scale_array_for_variant(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    variant: RegimeVariant,
    buckets: np.ndarray,
    table: list[dict[str, Any]],
) -> np.ndarray:
    scale_by_bucket = {str(row["bucket"]): float(row["scale_log_return"]) for row in table}
    global_scale = variant.base_scale_log_return
    return np.array([scale_by_bucket.get(str(bucket), global_scale) for bucket in buckets], dtype="float64")


def regime_shape_path_arrays(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    variant: RegimeVariant,
    scales: np.ndarray,
) -> dict[str, np.ndarray]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    base = raw["log_close"].to_numpy(dtype="float64")[raw_indexes]
    log_close = raw["log_close"].to_numpy(dtype="float64")
    log_high = raw["log_high"].to_numpy(dtype="float64")
    log_low = raw["log_low"].to_numpy(dtype="float64")
    high_steps = np.vstack([log_high[raw_indexes + step] - base for step in range(1, variant.hold_bars + 1)])
    low_steps = np.vstack([base - log_low[raw_indexes + step] for step in range(1, variant.hold_bars + 1)])
    early_end = min(variant.early_window_bars, variant.hold_bars)
    return {
        "long_mfe": np.nanmax(high_steps, axis=0),
        "long_mae": np.nanmax(low_steps, axis=0),
        "short_mfe": np.nanmax(low_steps, axis=0),
        "short_mae": np.nanmax(high_steps, axis=0),
        "early_long_mae": np.nanmax(low_steps[:early_end], axis=0),
        "early_short_mae": np.nanmax(high_steps[:early_end], axis=0),
        "fwd_return": log_close[raw_indexes + variant.hold_bars] - base,
        "scale": scales,
    }


def build_regime_shape_labels(path: dict[str, np.ndarray], variant: RegimeVariant) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    scale = np.maximum(path["scale"], 1e-12)
    target = scale * variant.target_multiplier
    cap = scale * variant.adverse_cap_multiplier
    early_cap = scale * variant.early_adverse_cap_multiplier
    recovery = scale * variant.recovery_floor_multiplier
    score_margin = scale * variant.score_margin_multiplier
    long_score = (
        path["long_mfe"] / target
        - 0.85 * path["long_mae"] / cap
        - 0.45 * path["early_long_mae"] / early_cap
        + path["fwd_return"] / scale
    )
    short_score = (
        path["short_mfe"] / target
        - 0.85 * path["short_mae"] / cap
        - 0.45 * path["early_short_mae"] / early_cap
        - path["fwd_return"] / scale
    )
    long_ok = (
        (path["long_mfe"] >= target)
        & (path["long_mae"] <= cap)
        & (path["early_long_mae"] <= early_cap)
        & (path["fwd_return"] >= recovery)
        & ((long_score - short_score) >= score_margin)
    )
    short_ok = (
        (path["short_mfe"] >= target)
        & (path["short_mae"] <= cap)
        & (path["early_short_mae"] <= early_cap)
        & (path["fwd_return"] <= -recovery)
        & ((short_score - long_score) >= score_margin)
    )
    signal = np.zeros(len(path["fwd_return"]), dtype="int8")
    signal[long_ok] = 1
    signal[short_ok] = -1
    conflict = long_ok & short_ok
    if conflict.any():
        signal[conflict] = np.where(long_score[conflict] > short_score[conflict], 1, -1)
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    diagnostics = {
        "label_boundary": "train_only_regime_scale_future_path_label_not_runtime(학습 전용 레짐 척도 미래 경로 라벨, 런타임 아님)",
        "oracle_long_count": int((signal == 1).sum()),
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "conflict_count": int(conflict.sum()),
        "mean_scale": float(np.nanmean(scale)),
        "mean_long_score": float(np.nanmean(long_score)),
        "mean_short_score": float(np.nanmean(short_score)),
    }
    return labels, signal, diagnostics


def build_final(
    created_at: str,
    result: dict[str, Any],
    variants: list[RegimeVariant],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_open: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    best = candidate_summary[0] if candidate_summary else {}
    status = "regime_normalized_strict_scout_clue_no_authority" if strict_rows else (
        "regime_normalized_preserved_clue_no_authority" if preserved_rows else "regime_normalized_no_strict_clue_no_authority"
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
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_if_strict(엄격 단서가 있으면 그록 비싼 검증 전 검토 필요)",
        "mt5_status": "not_run_proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
    }


def write_artifacts(
    result: dict[str, Any],
    final: dict[str, Any],
    variants: list[RegimeVariant],
    bucket_tables: dict[str, list[dict[str, Any]]],
) -> dict[str, Path]:
    artifacts = {
        "variant_manifest": RUN_ROOT / "variant_manifest.csv",
        "bucket_scales": RUN_ROOT / "bucket_scales.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "oracle_metrics": RUN_ROOT / "oracle_metrics.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.json",
        "skipped": RUN_ROOT / "skipped.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    bucket_rows = [row for rows in bucket_tables.values() for row in rows]
    write_csv(artifacts["variant_manifest"], [asdict(variant) for variant in variants])
    write_csv(artifacts["bucket_scales"], bucket_rows)
    write_csv(artifacts["label_distribution"], result["label_distribution"])
    write_csv(artifacts["oracle_metrics"], result["oracle_metrics"])
    write_csv(artifacts["model_metrics"], result["model_metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
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
    text = f"""# Frontier13B Regime-Normalized Trade Shape Proxy Scout(프론티어13B 레짐 정규화 거래 형상 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): train-only regime bucket scales(학습 전용 레짐 버킷 척도)로 3개 label variants(라벨 변형)를 만들고 fixed argmax ONNX models(고정 최대확률 온엑스 모델)을 학습했습니다.

Effect(효과): F12(프론티어12)의 sparse low-DD surface(희소한 낮은 손실폭 표면)가 regime scale(레짐 척도)로 density/PF/DD(빈도/수익 팩터/손실폭)를 동시에 개선하는지 측정했습니다.

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
- bucket scales(버킷 척도): `{artifacts['bucket_scales'].as_posix()}`
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

Action(행동): Frontier13B(프론티어13B)는 regime-normalized trade-shape labels(레짐 정규화 거래 형상 라벨)를 ONNX proxy scout(온엑스 프록시 탐색)로 시험했습니다.

Effect(효과): best candidate(최고 후보) `{best.get('candidate_id', 'none')}`의 validation/OOS PF-density-DD(검증/표본밖 수익 팩터-빈도-손실폭)를 기록했고, authority claim(권위 주장)은 하지 않았습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier13 Selection Status(프론티어13 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최고 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier13 Review Index(프론티어13 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `frontier13A_stage_open_regime_normalized_trade_shape_onnx_scout_v1`: stage open(단계 개방), Grok accepted(그록 수용).
- `{RUN_ID}`: regime-normalized proxy scout(레짐 정규화 프록시 탐색), no WFO/MT5(WFO/MT5 없음).
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier13B Required Gate Coverage Audit(프론티어13B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- data_integrity_gate(데이터 무결성 게이트): train-only regime scales(학습 전용 레짐 척도) recorded(기록됨).
- model_validation_gate(모델 검증 게이트): ONNX parity(온엑스 동등성), classification metrics(분류 지표), validation/OOS metrics(검증/표본밖 지표) recorded(기록됨).
- artifact_lineage_gate(산출물 계보 게이트): run manifest(실행 목록), model hashes(모델 해시), ONNX hashes(온엑스 해시) recorded(기록됨).
- paired_tier_gate(짝 티어 게이트): Tier A separate(티어 A 분리) computed(계산됨), Tier B and combined(티어 B와 합산)은 missing_required(필수 누락)로 기록됨.
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "regime_normalized_trade_shape_proxy_scout(레짐 정규화 거래 형상 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_wfo_no_mt5_no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "proxy_scout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(best),
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "best_candidate_id": best.get("candidate_id", ""),
        "best_validation_pf": best.get("validation_profit_factor", ""),
        "best_validation_density": best.get("validation_trades_per_day", ""),
        "best_validation_dd": best.get("validation_dd_risk_percent", ""),
        "best_oos_pf": best.get("oos_profit_factor", ""),
        "best_oos_density": best.get("oos_trades_per_day", ""),
        "best_oos_dd": best.get("oos_dd_risk_percent", ""),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "regime_normalized_trade_shape_proxy_scout(레짐 정규화 거래 형상 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "train_only_regime_scale_argmax_only_no_threshold_no_wfo_no_mt5_no_authority(학습 전용 레짐 척도, 최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_regime_normalized_trade_shape_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_regime_normalized_trade_shape_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "regime_normalized_trade_shape_proxy_not_runtime(레짐 정규화 거래 형상 프록시, 런타임 아님)",
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

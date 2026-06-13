from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_04__path_aware_cost_dd_event_labeling"
RUN_ID = "frontier04B_path_aware_label_proxy_scout_v1"
RUN_NUMBER = "frontier04B"
PARENT_RUN_ID = "frontier04A_stage_open_path_aware_cost_dd_event_labeling_v1"
NEXT_CLUE_RUN_ID = "frontier04C_grok_pre_trainable_transfer_review_v1"
NEXT_NEGATIVE_RUN_ID = "frontier04C_path_label_negative_memory_or_repair_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

MODEL_INPUT_DATASET = f03b.DATASET_PATH
FEATURE_ORDER_PATH = f03b.FEATURE_ORDER_PATH
RAW_US100 = Path("data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv")
RAW_US100_MANIFEST = RAW_US100.with_name("bars_us100_m5_mt5api_raw.manifest.json")

SCALE_QUANTILE = 0.90
HORIZONS = (12, 18)
TARGET_STOP_PAIRS = (
    (0.8, 0.6),
    (1.0, 0.7),
    (1.2, 0.8),
)
SCOUT_DENSITY_LOW = 4.5
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_LOW = 1.2


@dataclass(frozen=True)
class PathVariant:
    variant_id: str
    horizon_bars: int
    target_multiplier: float
    stop_multiplier: float
    scale_quantile: float
    target_log_return: float
    stop_log_return: float
    base_scale_log_return: float


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    frame, raw, integrity = load_and_align()
    variants = build_variants(frame, raw)
    metrics, reason_rows = evaluate_variants(frame, raw, variants)
    summary = build_candidate_summary(metrics)
    final = build_final(summary, metrics, integrity, variants)
    artifacts = write_artifacts(frame, raw, integrity, variants, metrics, summary, reason_rows, final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "path_joint_success_rows": final["path_joint_success_rows"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def load_and_align() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    model = pd.read_parquet(
        io_path(MODEL_INPUT_DATASET),
        columns=["timestamp", "split", "future_log_return_12"],
    ).sort_values("timestamp").reset_index(drop=True)
    raw = pd.read_csv(
        io_path(RAW_US100),
        usecols=[
            "time_open_unix",
            "time_close_unix",
            "open",
            "high",
            "low",
            "close",
            "price_basis",
            "timezone_status",
        ],
    )
    raw = raw.sort_values("time_close_unix").reset_index(drop=True)
    raw["raw_index"] = np.arange(len(raw), dtype=np.int64)
    raw["broker_clock_open_key"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw["broker_clock_close_key"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    for column in ("open", "high", "low", "close"):
        raw[column] = pd.to_numeric(raw[column], errors="coerce").astype("float64")
    raw["log_close"] = np.log(raw["close"].to_numpy(dtype="float64"))
    raw["log_high"] = np.log(raw["high"].to_numpy(dtype="float64"))
    raw["log_low"] = np.log(raw["low"].to_numpy(dtype="float64"))

    merged = model.merge(
        raw[["broker_clock_close_key", "raw_index", "open", "high", "low", "close"]],
        left_on="timestamp",
        right_on="broker_clock_close_key",
        how="left",
        validate="one_to_one",
    )
    merged["raw_index"] = merged["raw_index"].astype("Int64")
    raw_indexes = merged["raw_index"].dropna().astype("int64").to_numpy()
    raw_len = len(raw)
    missing_future = {f"h{h}": int((raw_indexes + h >= raw_len).sum()) for h in HORIZONS}
    fwd12 = np.full(len(merged), np.nan, dtype="float64")
    valid_index = merged["raw_index"].notna().to_numpy()
    valid_raw_indexes = merged.loc[valid_index, "raw_index"].astype("int64").to_numpy()
    fwd12[valid_index] = raw["log_close"].to_numpy()[valid_raw_indexes + 12] - raw["log_close"].to_numpy()[valid_raw_indexes]
    fwd12_diff = np.abs(fwd12 - pd.to_numeric(merged["future_log_return_12"], errors="coerce").to_numpy(dtype="float64"))

    integrity = {
        "data_source": {
            "model_input_dataset": MODEL_INPUT_DATASET.as_posix(),
            "raw_us100": RAW_US100.as_posix(),
            "raw_manifest": RAW_US100_MANIFEST.as_posix(),
        },
        "time_axis": (
            "model timestamp(모델 타임스탬프) is matched to raw time_close_unix as "
            "broker_clock_close_key(브로커 시계 종가 키); timezone_status remains unresolved, "
            "so this is not a direct UTC market-session claim(직접 UTC 세션 주장 아님)."
        ),
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "model_rows": int(len(merged)),
            "raw_rows": int(len(raw)),
            "start_timestamp": str(merged["timestamp"].iloc[0]),
            "end_timestamp": str(merged["timestamp"].iloc[-1]),
            "split_counts": {str(k): int(v) for k, v in merged["split"].astype(str).value_counts().items()},
            "tier_a": "model input rows plus raw US100 OHLC(모델 입력 행 + 원천 US100 OHLC)",
            "tier_b": "missing_required(필수 누락)",
        },
        "missing_or_duplicate_check": {
            "model_duplicate_timestamps": int(merged["timestamp"].duplicated().sum()),
            "raw_duplicate_close_keys": int(raw["broker_clock_close_key"].duplicated().sum()),
            "missing_raw_matches": int(merged["raw_index"].isna().sum()),
            "missing_future_paths": missing_future,
        },
        "feature_label_boundary": (
            "labels use only raw future OHLC after the current closed bar(현재 종료봉 이후 원천 미래 OHLC만 사용); "
            "feature_set_v2 columns are not loaded into label construction(피처 컬럼은 라벨 생성에 로드하지 않음)."
        ),
        "split_boundary": "train split(학습 분할) only supplies the p90 scale; validation/OOS(검증/표본밖)는 평가 전용입니다.",
        "leakage_risk": (
            "path labels are oracle labels(미래 경로를 아는 라벨) and cannot be interpreted as runtime signals(런타임 신호). "
            "current bar high/low is excluded by starting at t+1(현재 봉 고저는 t+1 시작으로 제외)."
        ),
        "data_hash_or_identity": {
            "model_input_dataset_sha256": sha256_file(MODEL_INPUT_DATASET),
            "raw_us100_sha256": sha256_file(RAW_US100),
            "raw_manifest_sha256": sha256_file(RAW_US100_MANIFEST),
            "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH),
            "fwd12_max_abs_diff_vs_model": float(np.nanmax(fwd12_diff)),
            "fwd12_p99_abs_diff_vs_model": float(np.nanquantile(fwd12_diff, 0.99)),
        },
        "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
    }
    failure_values = [
        integrity["missing_or_duplicate_check"]["model_duplicate_timestamps"],
        integrity["missing_or_duplicate_check"]["raw_duplicate_close_keys"],
        integrity["missing_or_duplicate_check"]["missing_raw_matches"],
        *integrity["missing_or_duplicate_check"]["missing_future_paths"].values(),
    ]
    if any(value != 0 for value in failure_values):
        integrity["integrity_judgment"] = "invalid(무효)"
    if not np.isfinite(integrity["data_hash_or_identity"]["fwd12_max_abs_diff_vs_model"]) or integrity["data_hash_or_identity"]["fwd12_max_abs_diff_vs_model"] > 1e-7:
        integrity["integrity_judgment"] = "invalid(무효)"
    return merged, raw, integrity


def build_variants(frame: pd.DataFrame, raw: pd.DataFrame) -> list[PathVariant]:
    variants: list[PathVariant] = []
    raw_indexes = frame["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    train_mask = frame["split"].astype(str).eq("train").to_numpy()
    for horizon in HORIZONS:
        fwd = log_close[raw_indexes + horizon] - log_close[raw_indexes]
        base_scale = float(np.nanquantile(np.abs(fwd[train_mask]), SCALE_QUANTILE))
        for target_mult, stop_mult in TARGET_STOP_PAIRS:
            variant_id = (
                f"f04b_path_h{horizon}_t{target_mult:.2f}_s{stop_mult:.2f}_"
                f"trainp{int(SCALE_QUANTILE * 100)}"
            ).replace(".", "p")
            variants.append(
                PathVariant(
                    variant_id=variant_id,
                    horizon_bars=horizon,
                    target_multiplier=target_mult,
                    stop_multiplier=stop_mult,
                    scale_quantile=SCALE_QUANTILE,
                    target_log_return=base_scale * target_mult,
                    stop_log_return=base_scale * stop_mult,
                    base_scale_log_return=base_scale,
                )
            )
    return variants


def evaluate_variants(
    frame: pd.DataFrame,
    raw: pd.DataFrame,
    variants: list[PathVariant],
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    metric_rows: list[dict[str, Any]] = []
    reason_rows: list[dict[str, Any]] = []
    raw_indexes = frame["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    for variant in variants:
        fwd_return = log_close[raw_indexes + variant.horizon_bars] - log_close[raw_indexes]
        path_signal, path_reasons, first_steps = path_event_signal(frame, raw, variant)
        close_signal = np.zeros(len(frame), dtype="int8")
        close_signal[fwd_return > variant.target_log_return] = 1
        close_signal[fwd_return < -variant.target_log_return] = -1
        for comparison_kind, signal, reasons in (
            ("path_label(경로 라벨)", path_signal, path_reasons),
            ("close_return_baseline(종가 수익률 기준)", close_signal, np.full(len(frame), "close_return_threshold(종가 수익률 임계값)", dtype=object)),
        ):
            for split in ("train", "validation", "oos"):
                metric_rows.append(evaluate_split(frame, signal, fwd_return, split, variant, comparison_kind, reasons, first_steps))
        unique_reasons, counts = np.unique(path_reasons, return_counts=True)
        for reason, count in zip(unique_reasons, counts):
            reason_rows.append(
                {
                    "variant_id": variant.variant_id,
                    "reason": str(reason),
                    "count": int(count),
                    "fraction": float(count / len(path_reasons)),
                }
            )
    return pd.DataFrame(metric_rows), reason_rows


def path_event_signal(
    frame: pd.DataFrame,
    raw: pd.DataFrame,
    variant: PathVariant,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    raw_indexes = frame["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    log_high = raw["log_high"].to_numpy(dtype="float64")
    log_low = raw["log_low"].to_numpy(dtype="float64")
    signal = np.zeros(len(frame), dtype="int8")
    reasons = np.full(len(frame), "timeout_flat(시간 만료 플랫)", dtype=object)
    first_steps = np.zeros(len(frame), dtype="int16")
    for row_index, raw_index in enumerate(raw_indexes):
        base = float(log_close[raw_index])
        long_state: str | None = None
        short_state: str | None = None
        long_step = 9999
        short_step = 9999
        for step in range(1, variant.horizon_bars + 1):
            path_index = raw_index + step
            up = float(log_high[path_index] - base)
            down = float(log_low[path_index] - base)
            if long_state is None:
                long_target = up >= variant.target_log_return
                long_stop = down <= -variant.stop_log_return
                if long_target and long_stop:
                    long_state = "ambiguous"
                    long_step = step
                elif long_target:
                    long_state = "win"
                    long_step = step
                elif long_stop:
                    long_state = "loss"
                    long_step = step
            if short_state is None:
                short_target = down <= -variant.target_log_return
                short_stop = up >= variant.stop_log_return
                if short_target and short_stop:
                    short_state = "ambiguous"
                    short_step = step
                elif short_target:
                    short_state = "win"
                    short_step = step
                elif short_stop:
                    short_state = "loss"
                    short_step = step
            if long_state is not None and short_state is not None:
                break
        long_win = long_state == "win"
        short_win = short_state == "win"
        if long_win and not short_win:
            signal[row_index] = 1
            reasons[row_index] = "long_target_before_stop(롱 목표 선행)"
            first_steps[row_index] = long_step
        elif short_win and not long_win:
            signal[row_index] = -1
            reasons[row_index] = "short_target_before_stop(숏 목표 선행)"
            first_steps[row_index] = short_step
        elif long_win and short_win:
            if long_step < short_step:
                signal[row_index] = 1
                reasons[row_index] = "both_success_long_earlier(양쪽 성공 롱 선행)"
                first_steps[row_index] = long_step
            elif short_step < long_step:
                signal[row_index] = -1
                reasons[row_index] = "both_success_short_earlier(양쪽 성공 숏 선행)"
                first_steps[row_index] = short_step
            else:
                reasons[row_index] = "both_success_same_step_flat(양쪽 성공 같은 봉 플랫)"
                first_steps[row_index] = long_step
        elif long_state == "ambiguous" or short_state == "ambiguous":
            reasons[row_index] = "same_bar_ambiguous_flat(동일 봉 모호 플랫)"
            first_steps[row_index] = min(long_step, short_step)
    return signal, reasons, first_steps


def evaluate_split(
    frame: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    split: str,
    variant: PathVariant,
    comparison_kind: str,
    reasons: np.ndarray,
    first_steps: np.ndarray,
) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy()
    split_signal = signal[split_mask].astype("int8")
    trade_mask = split_signal != 0
    pnl = (
        split_signal.astype("float64") * fwd_return[split_mask]
        - trade_mask.astype("float64") * scout.ROUGH_COST_LOG_RETURN
    )
    trade_pnl = pnl[trade_mask]
    trade_times = frame.loc[split_mask].loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    days = scout.count_scope_days(frame.loc[split_mask, "timestamp"])
    trade_count = int(trade_mask.sum())
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(30, int(math.ceil(days)))
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    density_distance = scout.density_axis_distance(trades_per_day)
    pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], trade_count, sparse_flag, pf999_sparse_flag)
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    grok_density_pass = SCOUT_DENSITY_LOW <= trades_per_day <= SCOUT_DENSITY_HIGH
    grok_pf_pass = metrics["profit_factor"] > SCOUT_PF_LOW and metrics["net_profit"] > 0 and not pf999_sparse_flag
    grok_dd_pass = dd_risk < scout.DD_TARGET_PERCENT
    reason_split = reasons[split_mask]
    first_step_split = first_steps[split_mask]
    return {
        "variant_id": variant.variant_id,
        "comparison_kind": comparison_kind,
        "split": split,
        "tier_scope": "Tier A(티어 A)",
        "record_view": "Tier A separate(티어 A 분리)",
        "horizon_bars": variant.horizon_bars,
        "scale_quantile": variant.scale_quantile,
        "base_scale_log_return": variant.base_scale_log_return,
        "target_multiplier": variant.target_multiplier,
        "stop_multiplier": variant.stop_multiplier,
        "target_log_return": variant.target_log_return,
        "stop_log_return": variant.stop_log_return,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "long_trade_count": int((split_signal == 1).sum()),
        "short_trade_count": int((split_signal == -1).sum()),
        "flat_count": int((split_signal == 0).sum()),
        "same_bar_ambiguous_count": int((np.char.find(reason_split.astype(str), "same_bar_ambiguous") >= 0).sum()),
        "both_success_same_step_flat_count": int((np.char.find(reason_split.astype(str), "both_success_same_step") >= 0).sum()),
        "mean_first_event_step": float(np.mean(first_step_split[trade_mask])) if trade_count else 0.0,
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "dd_risk_percent": dd_risk,
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": bool(pf999_sparse_flag),
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": density_distance + pf_distance + dd_distance + smoothness_distance,
        "grok_density_pass": bool(grok_density_pass),
        "grok_pf_pass": bool(grok_pf_pass),
        "grok_dd_pass": bool(grok_dd_pass),
        "grok_joint_pass": bool(grok_density_pass and grok_pf_pass and grok_dd_pass),
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
        "label_semantics": "event_first_tplus1_same_bar_flat_timeout_flat(이벤트 우선 t+1, 동일 봉 모호 플랫, 시간 만료 플랫)",
    }


def build_candidate_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "variant_id",
        "comparison_kind",
        "horizon_bars",
        "scale_quantile",
        "base_scale_log_return",
        "target_multiplier",
        "stop_multiplier",
        "target_log_return",
        "stop_log_return",
    ]
    metric_cols = [
        "trade_count",
        "days_in_scope",
        "trades_per_day",
        "long_trade_count",
        "short_trade_count",
        "flat_count",
        "same_bar_ambiguous_count",
        "both_success_same_step_flat_count",
        "mean_first_event_step",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "max_drawdown_percent",
        "max_monthly_drawdown_percent",
        "dd_risk_percent",
        "underwater_ratio",
        "max_loss_streak",
        "equity_trend_r2",
        "sparse_flag",
        "pf999_sparse_flag",
        "density_axis_distance",
        "pf_axis_distance",
        "dd_axis_distance",
        "smoothness_axis_distance",
        "aspiration_distance_score",
        "grok_density_pass",
        "grok_pf_pass",
        "grok_dd_pass",
        "grok_joint_pass",
    ]
    rows: list[dict[str, Any]] = []
    for _, group in metrics.groupby(keys, sort=False):
        row = {key: group.iloc[0][key] for key in keys}
        for split in ("train", "validation", "oos"):
            split_row = group.loc[group["split"].eq(split)].iloc[0]
            for column in metric_cols:
                row[f"{split}_{column}"] = split_row[column]
        row["validation_oos_joint_pass"] = bool(row["validation_grok_joint_pass"] and row["oos_grok_joint_pass"])
        row["validation_oos_density_pass"] = bool(row["validation_grok_density_pass"] and row["oos_grok_density_pass"])
        row["validation_oos_pf_pass"] = bool(row["validation_grok_pf_pass"] and row["oos_grok_pf_pass"])
        row["validation_oos_dd_pass"] = bool(row["validation_grok_dd_pass"] and row["oos_grok_dd_pass"])
        row["validation_oos_distance_sum"] = float(row["validation_aspiration_distance_score"] + row["oos_aspiration_distance_score"])
        rows.append(row)
    return pd.DataFrame(rows)


def build_final(
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    integrity: dict[str, Any],
    variants: list[PathVariant],
) -> dict[str, Any]:
    path_rows = summary.loc[summary["comparison_kind"].eq("path_label(경로 라벨)")].copy()
    success_rows = path_rows.loc[path_rows["validation_oos_joint_pass"]].copy()
    top = path_rows.sort_values(
        ["validation_oos_joint_pass", "validation_oos_distance_sum", "oos_dd_risk_percent"],
        ascending=[False, True, True],
    ).head(10)
    best = dict(top.iloc[0]) if len(top) else {}
    if integrity["integrity_judgment"].startswith("invalid"):
        status = "invalid_setup_alignment_failed_no_authority"
        judgment = "invalid setup(무효 설정)"
        next_run_id = NEXT_NEGATIVE_RUN_ID
    elif len(success_rows):
        status = "scout_clue_found_no_authority"
        judgment = "seed_surface(씨앗 표면)"
        next_run_id = NEXT_CLUE_RUN_ID
    else:
        status = "no_joint_path_proxy_success_no_authority"
        judgment = "negative_memory_or_repair_needed(부정 기억 또는 수리 필요)"
        next_run_id = NEXT_NEGATIVE_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run_id,
        "created_at_utc": utc_now(),
        "variant_count": len(variants),
        "metric_rows": int(len(metrics)),
        "summary_rows": int(len(summary)),
        "path_joint_success_rows": int(len(success_rows)),
        "best_path_row": json_ready(best),
        "integrity": integrity,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(
    frame: pd.DataFrame,
    raw: pd.DataFrame,
    integrity: dict[str, Any],
    variants: list[PathVariant],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    reason_rows: list[dict[str, Any]],
    final: dict[str, Any],
) -> dict[str, Any]:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    alignment_path = RUN_ROOT / "alignment.json"
    integrity_path = RUN_ROOT / "integrity.json"
    variants_path = RUN_ROOT / "variants.csv"
    metrics_path = RUN_ROOT / "metrics.csv"
    summary_path = RUN_ROOT / "summary.csv"
    top_path = RUN_ROOT / "top.csv"
    reasons_path = RUN_ROOT / "reasons.csv"
    manifest_path = RUN_ROOT / "run_manifest.json"
    write_json(alignment_path, alignment_manifest(frame, raw, integrity))
    write_json(integrity_path, integrity)
    pd.DataFrame([asdict(variant) for variant in variants]).to_csv(io_path(variants_path), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(metrics_path), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(summary_path), index=False, encoding="utf-8-sig")
    top = summary.loc[summary["comparison_kind"].eq("path_label(경로 라벨)")].sort_values(
        ["validation_oos_joint_pass", "validation_oos_distance_sum", "oos_dd_risk_percent"],
        ascending=[False, True, True],
    ).head(20)
    top.to_csv(io_path(top_path), index=False, encoding="utf-8-sig")
    pd.DataFrame(reason_rows).to_csv(io_path(reasons_path), index=False, encoding="utf-8-sig")
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_04/frontier04b_path_aware_label_proxy_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_04/frontier04b_path_aware_label_proxy_scout.py")),
        "stage355_precedent": "stage_pipelines/stage355/materialize_density_recovery_label_inputs_without_db.py:first_barrier_labels",
        "label_semantics_contract": {
            "event_order": "event_first(이벤트 우선)",
            "path_start": "t_plus_1_after_current_closed_bar(현재 종료봉 이후 t+1)",
            "same_bar_ambiguity": "flat_no_trade(플랫, 거래 없음)",
            "timeout": "flat_no_trade(플랫, 거래 없음)",
            "cost_deduction": "rough log-return cost deducted once per selected trade(선택 거래마다 대략 로그 수익률 비용 1회 차감)",
            "pnl_basis": "horizon close-return proxy PnL, not runtime exit(수평선 종가 프록시 손익, 런타임 청산 아님)",
        },
        "outputs": {
            "alignment_manifest": {"path": alignment_path.as_posix(), "sha256": sha256_file(alignment_path)},
            "data_integrity_summary": {"path": integrity_path.as_posix(), "sha256": sha256_file(integrity_path)},
            "label_variant_manifest": {"path": variants_path.as_posix(), "sha256": sha256_file(variants_path)},
            "label_variant_metrics": {"path": metrics_path.as_posix(), "sha256": sha256_file(metrics_path)},
            "label_variant_summary": {"path": summary_path.as_posix(), "sha256": sha256_file(summary_path)},
            "top_path_label_scout_rows": {"path": top_path.as_posix(), "sha256": sha256_file(top_path)},
            "path_label_reason_counts": {"path": reasons_path.as_posix(), "sha256": sha256_file(reasons_path)},
            "report": {"path": REPORT_PATH.as_posix()},
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(manifest_path, manifest)
    return {
        "alignment_manifest": alignment_path,
        "data_integrity_summary": integrity_path,
        "label_variant_manifest": variants_path,
        "label_variant_metrics": metrics_path,
        "label_variant_summary": summary_path,
        "top_path_label_scout_rows": top_path,
        "path_label_reason_counts": reasons_path,
        "run_manifest": manifest_path,
    }


def alignment_manifest(frame: pd.DataFrame, raw: pd.DataFrame, integrity: dict[str, Any]) -> dict[str, Any]:
    return {
        "join_key": "timestamp == broker_clock_close_key(timestamp from raw time_close_unix)",
        "time_axis_boundary": integrity["time_axis"],
        "model_rows": int(len(frame)),
        "raw_rows": int(len(raw)),
        "matched_rows": int(frame["raw_index"].notna().sum()),
        "missing_rows": int(frame["raw_index"].isna().sum()),
        "first_model_timestamp": str(frame["timestamp"].iloc[0]),
        "first_raw_index": int(frame["raw_index"].iloc[0]),
        "last_model_timestamp": str(frame["timestamp"].iloc[-1]),
        "last_raw_index": int(frame["raw_index"].iloc[-1]),
        "raw_close_key_duplicates": int(raw["broker_clock_close_key"].duplicated().sum()),
        "model_timestamp_duplicates": int(frame["timestamp"].duplicated().sum()),
        "fwd12_max_abs_diff_vs_model": integrity["data_hash_or_identity"]["fwd12_max_abs_diff_vs_model"],
        "fwd12_p99_abs_diff_vs_model": integrity["data_hash_or_identity"]["fwd12_p99_abs_diff_vs_model"],
        "integrity_judgment": integrity["integrity_judgment"],
    }


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final.get("best_path_row", {})
    best_lines = "No path row(경로 행 없음)."
    if best:
        best_lines = (
            f"- variant(변형): `{best.get('variant_id')}`\n"
            f"- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): "
            f"`{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk_percent'))}%`\n"
            f"- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): "
            f"`{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk_percent'))}%`\n"
            f"- joint pass(동시 통과): `{best.get('validation_oos_joint_pass')}`"
        )
    text = f"""# Frontier04B Path-Aware Label Proxy Scout Report(전선04B 경로 인식 라벨 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier04B(전선04B)는 raw US100 OHLC(원천 US100 시가/고가/저가/종가)를 model input rows(모델 입력 행)에 정렬하고, p90 train scale(학습 90분위 척도)의 path event labels(경로 이벤트 라벨)을 proxy-only(프록시 전용)로 계산했습니다.

Effect(효과): ONNX(온엑스), WFO(워크포워드), MT5(메타트레이더5) 전에 label axis(라벨 축)이 density/PF/DD(밀도/수익 팩터/손실폭)를 동시에 만족할 수 있는지 좁게 확인했습니다.

## Data Integrity(데이터 무결성)

- integrity_judgment(무결성 판정): `{final['integrity']['integrity_judgment']}`
- time_axis(시간축): {final['integrity']['time_axis']}
- feature_label_boundary(피처-라벨 경계): {final['integrity']['feature_label_boundary']}
- leakage_risk(누수 위험): {final['integrity']['leakage_risk']}

## Best Path Row(최상위 경로 행)

{best_lines}

## Grok Bounds(그록 경계)

- proxy-only gate(프록시 전용 게이트): satisfied(충족), no ONNX/WFO/MT5(온엑스/WFO/MT5 없음).
- OHLC alignment preflight(원천 OHLC 정렬 사전 점검): `{artifacts['alignment_manifest'].as_posix()}`.
- controlled comparison(통제 비교): `{artifacts['label_variant_summary'].as_posix()}` includes path label(경로 라벨) and close-return baseline(종가 수익률 기준).
- Stage355 precedent(Stage355 선례): run manifest(실행 목록)에 `first_barrier_labels`를 인용했습니다.

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 Grok pre-expensive review(그록 사전 고비용 검토)를 열어 이 seed surface(씨앗 표면)를 trainable transfer(학습 가능 전달)로 넘길지 묻는 것입니다. Effect(효과)는 proxy oracle(프록시 오라클)을 ONNX promise(온엑스 약속)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    import yaml

    now = final["created_at_utc"]
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
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    for row in ledger_rows(final, artifacts):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: path-aware label proxy scout(경로 인식 라벨 프록시 탐색) recorded `{final['path_joint_success_rows']}` joint path rows(동시 경로 행). Effect(효과): trainable transfer(학습 가능 전달) 전 Grok review(그록 검토)로 넘길 근거를 만들었습니다.\n",
    )
    if final["path_joint_success_rows"] == 0:
        f03b.append_once(
            f03b.NEGATIVE_RESULT_REGISTER,
            RUN_ID,
            f"- `{RUN_ID}`: no validation+OOS joint path row(검증+표본밖 동시 경로 행 없음). Effect(효과): threshold-only retry(임계값 전용 재시도) 대신 repair/negative-memory decision(수리/부정 기억 결정)으로 넘깁니다.\n",
        )


def current_state_text(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier04B(전선04B)는 path-aware label proxy scout(경로 인식 라벨 프록시 탐색)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{final.get('best_path_row', {}).get('variant_id', 'none')}` with path_joint_success_rows(동시 경로 성공 행) `{final['path_joint_success_rows']}`.

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 Grok pre-expensive review(그록 사전 고비용 검토)를 여는 것입니다. Effect(효과)는 proxy clue(프록시 단서)를 ONNX(온엑스)나 WFO/MT5(워크포워드/메타트레이더5) 주장으로 과장하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final.get("best_path_row", {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "label_proxy_scout(라벨 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"path_joint_success_rows={final['path_joint_success_rows']};no_authority",
        "work_family": "alpha_exploration(알파 탐색)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["path_joint_success_rows"]),
        "claim_boundary": "proxy_only_no_onnx_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_path_label_proxy",
        "subrun_id": f"{RUN_ID}__tier_a_path_label_proxy",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "path_label_proxy_oracle_not_runtime(경로 라벨 프록시 오라클, 런타임 아님)",
        "primary_kpi": (
            f"best={best.get('variant_id', 'none')};"
            f"val_pf={fmt(best.get('validation_profit_factor'))};"
            f"oos_pf={fmt(best.get('oos_profit_factor'))};"
            f"oos_density={fmt(best.get('oos_trades_per_day'))};"
            f"oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
        ),
        "guardrail_kpi": "no_model_training_no_onnx_no_wfo_no_mt5_no_authority(모델 학습/온엑스/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "proxy_only_label_scout(프록시 전용 라벨 탐색)",
        "reopen_condition": final["next_run_id"],
        "question": "Can path-aware labels reduce the Frontier03 close-return DD trap?(경로 인식 라벨이 전선03 종가 수익률 손실폭 함정을 줄일 수 있는가?)",
        "skill_family": "alpha_exploration(알파 탐색)",
        "lineage_summary": "raw_ohlc_alignment_to_path_label_proxy_metrics(원천 OHLC 정렬에서 경로 라벨 프록시 지표)",
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final.get("best_path_row", {})
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "label_proxy_scout(라벨 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_model_training_no_onnx_no_wfo_no_mt5_no_authority(모델 학습/온엑스/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_path_label_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_path_label_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "path_label_proxy_oracle_not_runtime(경로 라벨 프록시 오라클, 런타임 아님)",
            "primary_kpi": (
                f"best={best.get('variant_id', 'none')};"
                f"val_pf={fmt(best.get('validation_profit_factor'))};"
                f"val_density={fmt(best.get('validation_trades_per_day'))};"
                f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
                f"oos_pf={fmt(best.get('oos_profit_factor'))};"
                f"oos_density={fmt(best.get('oos_trades_per_day'))};"
                f"oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
            ),
            "notes": f"path_joint_success_rows={final['path_joint_success_rows']};no_authority",
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


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return str(number)
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())

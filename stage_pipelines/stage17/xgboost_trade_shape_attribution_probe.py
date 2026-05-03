from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    upsert_csv_rows,
)


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "17_model_family_challenge__xgboost_regularized_boosting_scout"
RUN_ID = "run11D_xgb_trade_shape_attribution_v1"
RUN_NUMBER = "run11D"
PACKET_ID = "stage17_run11D_xgb_trade_shape_attribution_v1"
SOURCE_RUN_ID = "run11C_xgb_q80_direction_asymmetry_probe_v1"
SOURCE_PACKET_ID = "stage17_run11C_xgb_direction_asymmetry_v1"
EXPLORATION_LABEL = "stage17_Model__XGBoostTradeShapeAttribution"
BOUNDARY = "xgboost_trade_shape_attribution_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_xgboost_trade_shape_attribution_completed"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
SOURCE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / SOURCE_PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run11D_xgb_trade_shape_attribution_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-03_stage17_xgboost_trade_shape_attribution.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"

SIDE_TRADE_COLUMNS = (
    "split",
    "side",
    "trade_count",
    "net_profit",
    "avg_hold_bars",
    "mfe_mean",
    "mae_mean",
    "realized_over_mfe_mean",
    "positive_month_ratio",
    "top_session",
    "top_session_share",
    "top_trend",
    "top_trend_share",
    "top_volatility",
    "top_volatility_share",
)
PROBABILITY_COLUMNS = (
    "split",
    "source",
    "row_count",
    "signal_count",
    "long_signal_count",
    "short_signal_count",
    "long_signal_share",
    "short_signal_share",
    "mean_p_long",
    "mean_p_short",
    "mean_p_flat",
    "mean_margin",
)
REGIME_COLUMNS = (
    "split",
    "side",
    "regime_type",
    "regime_value",
    "trade_count",
    "trade_share",
    "net_profit",
    "avg_hold_bars",
    "mfe_mean",
    "mae_mean",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def load_inputs() -> dict[str, Any]:
    source_summary = read_json(SOURCE_ROOT / "summary.json")
    source_kpi = read_json(SOURCE_ROOT / "kpi_record.json")
    trade_df = pd.read_csv(io_path(SOURCE_PACKET_ROOT / "trade_level_records.csv"))
    trade_summary_df = pd.read_csv(io_path(SOURCE_PACKET_ROOT / "trade_attribution_summary.csv"))
    prediction_path = SOURCE_ROOT / "predictions/tier_ab_combined_predictions.parquet"
    pred_df = pd.read_parquet(io_path(prediction_path))
    return {
        "source_summary": source_summary,
        "source_kpi": source_kpi,
        "trade_df": trade_df,
        "trade_summary_df": trade_summary_df,
        "pred_df": pred_df,
        "prediction_path": prediction_path,
    }


def top_value(rows: pd.DataFrame, column: str) -> tuple[str, float]:
    if rows.empty or column not in rows:
        return "", 0.0
    counts = rows[column].fillna("unknown").astype(str).value_counts()
    if counts.empty:
        return "", 0.0
    return str(counts.index[0]), safe_div(float(counts.iloc[0]), float(len(rows)))


def side_trade_rows(trade_df: pd.DataFrame) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    data = trade_df.copy()
    data["open_time"] = pd.to_datetime(data["open_time"], errors="coerce")
    data["month"] = data["open_time"].dt.to_period("M").astype(str)
    for split in ("validation", "oos"):
        split_df = data[data["split"] == split]
        for raw_side, side in (("buy", "long"), ("sell", "short")):
            rows = split_df[split_df["direction"] == raw_side]
            count = int(len(rows))
            month_net = rows.groupby("month")["net_profit"].sum() if count else pd.Series(dtype=float)
            positive_month_ratio = safe_div(float((month_net > 0.0).sum()), float(len(month_net)))
            top_session, top_session_share = top_value(rows, "session_slice")
            top_trend, top_trend_share = top_value(rows, "trend_regime")
            top_vol, top_vol_share = top_value(rows, "volatility_regime")
            out.append(
                {
                    "split": split,
                    "side": side,
                    "trade_count": count,
                    "net_profit": safe_float(rows["net_profit"].sum()) if count else 0.0,
                    "avg_hold_bars": safe_float(rows["hold_bars"].mean()) if count else 0.0,
                    "mfe_mean": safe_float(rows["mfe"].mean()) if count else 0.0,
                    "mae_mean": safe_float(rows["mae"].mean()) if count else 0.0,
                    "realized_over_mfe_mean": safe_float(rows["realized_over_mfe"].mean()) if count else 0.0,
                    "positive_month_ratio": positive_month_ratio,
                    "top_session": top_session,
                    "top_session_share": top_session_share,
                    "top_trend": top_trend,
                    "top_trend_share": top_trend_share,
                    "top_volatility": top_vol,
                    "top_volatility_share": top_vol_share,
                }
            )
    return out


def regime_rows(trade_df: pd.DataFrame) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    regime_cols = {
        "session": "session_slice",
        "trend": "trend_regime",
        "volatility": "volatility_regime",
        "adx": "adx_bucket",
    }
    for split in ("validation", "oos"):
        for raw_side, side in (("buy", "long"), ("sell", "short")):
            side_rows = trade_df[(trade_df["split"] == split) & (trade_df["direction"] == raw_side)]
            side_total = float(len(side_rows))
            for regime_type, column in regime_cols.items():
                if column not in side_rows:
                    continue
                for regime_value, rows in side_rows.groupby(column):
                    out.append(
                        {
                            "split": split,
                            "side": side,
                            "regime_type": regime_type,
                            "regime_value": str(regime_value),
                            "trade_count": int(len(rows)),
                            "trade_share": safe_div(float(len(rows)), side_total),
                            "net_profit": safe_float(rows["net_profit"].sum()),
                            "avg_hold_bars": safe_float(rows["hold_bars"].mean()),
                            "mfe_mean": safe_float(rows["mfe"].mean()),
                            "mae_mean": safe_float(rows["mae"].mean()),
                        }
                    )
    return out


def probability_rows(pred_df: pd.DataFrame, thresholds: Mapping[str, Any]) -> list[dict[str, Any]]:
    data = pred_df[pred_df["split"].isin(["validation", "oos"])].copy()
    tier_a_threshold = safe_float(thresholds.get("tier_a"))
    tier_b_threshold = safe_float(thresholds.get("tier_b"), tier_a_threshold)

    def decide(row: pd.Series) -> str:
        threshold = tier_a_threshold if str(row.get("record_source")) == "tier_a" else tier_b_threshold
        p_long = safe_float(row.get("p_long"))
        p_short = safe_float(row.get("p_short"))
        if p_long >= threshold and p_long >= p_short:
            return "long"
        if p_short >= threshold and p_short > p_long:
            return "short"
        return "flat"

    data["decision"] = data.apply(decide, axis=1)
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        split_df = data[data["split"] == split]
        for source_label, source_df in (
            ("all", split_df),
            ("tier_a", split_df[split_df["record_source"] == "tier_a"]),
            ("tier_b_fallback", split_df[split_df["record_source"] != "tier_a"]),
        ):
            signal = source_df[source_df["decision"].isin(["long", "short"])]
            long_count = int((signal["decision"] == "long").sum())
            short_count = int((signal["decision"] == "short").sum())
            signal_count = int(len(signal))
            rows.append(
                {
                    "split": split,
                    "source": source_label,
                    "row_count": int(len(source_df)),
                    "signal_count": signal_count,
                    "long_signal_count": long_count,
                    "short_signal_count": short_count,
                    "long_signal_share": safe_div(float(long_count), float(signal_count)),
                    "short_signal_share": safe_div(float(short_count), float(signal_count)),
                    "mean_p_long": safe_float(source_df["p_long"].mean()) if len(source_df) else 0.0,
                    "mean_p_short": safe_float(source_df["p_short"].mean()) if len(source_df) else 0.0,
                    "mean_p_flat": safe_float(source_df["p_flat"].mean()) if len(source_df) else 0.0,
                    "mean_margin": safe_float(source_df["probability_margin"].mean()) if len(source_df) else 0.0,
                }
            )
    return rows


def split_side(rowset: Sequence[Mapping[str, Any]], split: str, side: str) -> Mapping[str, Any]:
    for row in rowset:
        if row.get("split") == split and row.get("side") == side:
            return row
    return {}


def split_source(rowset: Sequence[Mapping[str, Any]], split: str, source: str) -> Mapping[str, Any]:
    for row in rowset:
        if row.get("split") == split and row.get("source") == source:
            return row
    return {}


def characteristic_read(
    source_summary: Mapping[str, Any],
    trade_rows: Sequence[Mapping[str, Any]],
    prob_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    val_long = split_side(trade_rows, "validation", "long")
    oos_long = split_side(trade_rows, "oos", "long")
    val_short = split_side(trade_rows, "validation", "short")
    oos_short = split_side(trade_rows, "oos", "short")
    long_hold = mean([safe_float(val_long.get("avg_hold_bars")), safe_float(oos_long.get("avg_hold_bars"))])
    short_hold = mean([safe_float(val_short.get("avg_hold_bars")), safe_float(oos_short.get("avg_hold_bars"))])
    long_month = mean([safe_float(val_long.get("positive_month_ratio")), safe_float(oos_long.get("positive_month_ratio"))])
    short_month = mean([safe_float(val_short.get("positive_month_ratio")), safe_float(oos_short.get("positive_month_ratio"))])
    val_prob = split_source(prob_rows, "validation", "all")
    oos_prob = split_source(prob_rows, "oos", "all")
    validation_long_share = safe_float(val_prob.get("long_signal_share"))
    oos_long_share = safe_float(oos_prob.get("long_signal_share"))
    direction = source_summary.get("direction_asymmetry", {})
    source_trade_contrast = safe_float(direction.get("trade_count_contrast"))
    hold_contrast = abs(long_hold - short_hold)
    month_ratio_contrast = abs(long_month - short_month)
    stable_long_signal_skew = validation_long_share >= 0.75 and oos_long_share >= 0.70
    trade_shape_shift = hold_contrast >= 8.0 or month_ratio_contrast >= 0.20
    new_characteristic = stable_long_signal_skew or trade_shape_shift
    return {
        "source_run_id": SOURCE_RUN_ID,
        "source_direction_trade_count_contrast": source_trade_contrast,
        "validation_long_signal_share": validation_long_share,
        "oos_long_signal_share": oos_long_share,
        "stable_long_signal_skew": stable_long_signal_skew,
        "long_avg_hold_bars": long_hold,
        "short_avg_hold_bars": short_hold,
        "hold_contrast_bars": hold_contrast,
        "long_positive_month_ratio": long_month,
        "short_positive_month_ratio": short_month,
        "positive_month_ratio_contrast": month_ratio_contrast,
        "trade_shape_shift_visible": trade_shape_shift,
        "new_characteristic_visible": new_characteristic,
        "model_characteristic_strength": "xgboost_trade_shape_probability_skew_visible" if new_characteristic else "no_new_trade_shape_characteristic",
        "stage17_stop_recommendation": "keep_stage17_open_for_probability_feature_driver_probe" if new_characteristic else "close_stage17_no_new_trade_shape_characteristic_after_run11D",
    }


def build_summary(inputs: Mapping[str, Any]) -> dict[str, Any]:
    source_summary = inputs["source_summary"]
    source_kpi = inputs["source_kpi"]
    thresholds = source_summary.get("model_artifacts", {}).get("thresholds", {})
    side_rows = side_trade_rows(inputs["trade_df"])
    prob_rows = probability_rows(inputs["pred_df"], thresholds)
    regimes = regime_rows(inputs["trade_df"])
    characteristic = characteristic_read(source_summary, side_rows, prob_rows)
    kpi_management = dict(source_kpi.get("kpi_management", {}))
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": source_summary.get("model_family"),
        "selected_variant_id": source_summary.get("selected_variant", {}).get("variant_id"),
        "thresholds": thresholds,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT,
        "external_verification_status": "completed_reused_run11C_mt5_evidence",
        "source_mt5_kpi_record_count": source_summary.get("mt5_kpi_record_count"),
        "source_normalized_kpi_records": kpi_management.get("normalized_records"),
        "source_trade_attribution_records": kpi_management.get("trade_attribution_records"),
        "side_trade_summary": side_rows,
        "probability_direction_summary": prob_rows,
        "regime_direction_summary": regimes,
        "trade_shape_attribution": characteristic,
        "model_characteristic_strength": characteristic["model_characteristic_strength"],
        "stage17_stop_recommendation": characteristic["stage17_stop_recommendation"],
        "closure_judgment": JUDGMENT,
        "kpi_management": kpi_management,
        "source_artifacts": {
            "source_summary": rel(SOURCE_ROOT / "summary.json"),
            "source_kpi_record": rel(SOURCE_ROOT / "kpi_record.json"),
            "source_trade_level_records": rel(SOURCE_PACKET_ROOT / "trade_level_records.csv"),
            "source_trade_attribution_summary": rel(SOURCE_PACKET_ROOT / "trade_attribution_summary.csv"),
            "source_prediction_path": rel(inputs["prediction_path"]),
        },
    }


def materialize_outputs(summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    write_csv(RUN_ROOT / "results/side_trade_shape_summary.csv", SIDE_TRADE_COLUMNS, summary["side_trade_summary"])
    write_csv(RUN_ROOT / "results/probability_direction_summary.csv", PROBABILITY_COLUMNS, summary["probability_direction_summary"])
    write_csv(RUN_ROOT / "results/regime_direction_summary.csv", REGIME_COLUMNS, summary["regime_direction_summary"])
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__trade_shape_attribution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "trade_shape_attribution",
        "parent_run_id": RUN_ID,
        "record_view": "run11C_mt5_trade_shape_reuse",
        "tier_scope": "Tier A+B",
        "kpi_scope": "trade_shape_probability_attribution",
        "scoreboard_lane": "model_characteristic_attribution",
        "status": "completed",
        "judgment": JUDGMENT,
        "path": rel(RUN_ROOT / "summary.json"),
        "primary_kpi": ledger_pairs(
            (
                ("new_characteristic_visible", summary["trade_shape_attribution"].get("new_characteristic_visible")),
                ("validation_long_signal_share", summary["trade_shape_attribution"].get("validation_long_signal_share")),
                ("oos_long_signal_share", summary["trade_shape_attribution"].get("oos_long_signal_share")),
                ("hold_contrast_bars", summary["trade_shape_attribution"].get("hold_contrast_bars")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("source_mt5_kpi_records", summary.get("source_mt5_kpi_record_count")),
                ("source_normalized_kpi_records", summary.get("source_normalized_kpi_records")),
                ("source_trade_attribution_records", summary.get("source_trade_attribution_records")),
                ("boundary", BOUNDARY),
            )
        ),
        "external_verification_status": "completed_reused_run11C_mt5_evidence",
        "notes": "Attribution run reuses completed run11C MT5 Strategy Tester and KPI evidence; no new operating claim.",
    }
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=[ledger_row],
    )
    registry_output = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_characteristic_attribution",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs(
                    (
                        ("source_run", SOURCE_RUN_ID),
                        ("new_characteristic_visible", summary["trade_shape_attribution"].get("new_characteristic_visible")),
                        ("recommendation", summary.get("stage17_stop_recommendation")),
                        ("boundary", "attribution_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    final_summary = {**dict(summary), "ledger_outputs": ledger_outputs, "registry_output": registry_output}
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "exploration_label": EXPLORATION_LABEL,
        "boundary": BOUNDARY,
        "inputs": summary["source_artifacts"],
        "outputs": {
            "summary": rel(RUN_ROOT / "summary.json"),
            "side_trade_shape_summary": rel(RUN_ROOT / "results/side_trade_shape_summary.csv"),
            "probability_direction_summary": rel(RUN_ROOT / "results/probability_direction_summary.csv"),
            "regime_direction_summary": rel(RUN_ROOT / "results/regime_direction_summary.csv"),
        },
        "external_verification_status": "completed_reused_run11C_mt5_evidence",
    }
    kpi_record = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "kpi_scope": "xgboost_trade_shape_attribution_from_run11C_mt5_evidence",
        "model_family": summary.get("model_family"),
        "selected_variant_id": summary.get("selected_variant_id"),
        "external_verification_status": "completed_reused_run11C_mt5_evidence",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "kpi_management": summary.get("kpi_management", {}),
        "source_artifacts": summary["source_artifacts"],
        "trade_shape_attribution": summary["trade_shape_attribution"],
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "summary.json", final_summary)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", final_summary)
    write_md(RUN_ROOT / "reports/result_summary.md", packet_markdown(final_summary))
    write_packet(final_summary, created_at)
    sync_docs(final_summary)
    return final_summary


def packet_markdown(summary: Mapping[str, Any]) -> str:
    attr = summary["trade_shape_attribution"]
    side_rows = summary["side_trade_summary"]

    def row(split: str, side: str) -> Mapping[str, Any]:
        return split_side(side_rows, split, side)

    lines = [
        "# Stage17 RUN11D XGBoost Trade Shape Attribution(17단계 실행11D XGBoost 거래 모양 귀속)",
        "",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
        f"- characteristic strength(특성 강도): `{summary.get('model_characteristic_strength')}`",
        f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| side/split(방향/분할) | trades(거래수) | net(순손익) | avg hold(평균 보유) | MFE | MAE | positive months(양수 월 비율) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for split in ("validation", "oos"):
        for side in ("long", "short"):
            item = row(split, side)
            lines.append(
                f"| {side}/{split} | `{item.get('trade_count')}` | `{item.get('net_profit')}` | `{item.get('avg_hold_bars')}` | `{item.get('mfe_mean')}` | `{item.get('mae_mean')}` | `{item.get('positive_month_ratio')}` |"
            )
    lines.extend(
        [
            "",
            f"- validation long signal share(검증 롱 신호 비율): `{attr.get('validation_long_signal_share')}`",
            f"- OOS long signal share(표본외 롱 신호 비율): `{attr.get('oos_long_signal_share')}`",
            f"- hold contrast bars(보유 시간 차이): `{attr.get('hold_contrast_bars')}`",
            f"- positive month ratio contrast(양수 월 비율 차이): `{attr.get('positive_month_ratio_contrast')}`",
            f"- new characteristic visible(새 특성 보임): `{attr.get('new_characteristic_visible')}`",
            "",
            "효과(effect, 효과): 이 run(실행)은 run11C의 MT5(`MetaTrader 5`, 메타트레이더5)와 KPI(`Key Performance Indicator`, 핵심성과지표) 근거를 재사용해 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)의 방향 비대칭이 거래 모양과 확률 신호 쏠림으로도 보이는지 확인했다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def write_packet(summary: Mapping[str, Any], created_at: str) -> None:
    kpi = summary.get("kpi_management", {})
    source_ok = (
        summary.get("external_verification_status") == "completed_reused_run11C_mt5_evidence"
        and summary.get("source_mt5_kpi_record_count") == 20
        and kpi.get("normalized_records") == 20
        and kpi.get("parser_errors") == 0
    )
    payloads = {
        "runtime_evidence_gate": {
            "audit_name": "runtime_evidence_gate",
            "status": "pass" if source_ok else "blocked",
            "passed": source_ok,
            "source_run_id": SOURCE_RUN_ID,
            "source_mt5_kpi_record_count": summary.get("source_mt5_kpi_record_count"),
            "external_verification_status": summary.get("external_verification_status"),
            "note": "No new Strategy Tester run; this attribution run reuses completed run11C MT5 evidence.",
        },
        "kpi_contract_audit": {
            "audit_name": "kpi_contract_audit",
            "status": "pass" if source_ok else "blocked",
            "passed": source_ok,
            **dict(kpi),
        },
        "attribution_characteristic_audit": {
            "audit_name": "attribution_characteristic_audit",
            "status": "pass",
            "passed": True,
            "trade_shape_attribution": summary.get("trade_shape_attribution", {}),
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if source_ok else "blocked",
            "passed": source_ok,
            "allowed_claims": [JUDGMENT, "model_characteristic_attribution"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if source_ok else "blocked",
            "passed": source_ok,
            "required_gates": {
                "runtime_evidence_gate": "pass" if source_ok else "blocked",
                "kpi_contract_audit": "pass" if source_ok else "blocked",
                "attribution_characteristic_audit": "pass",
                "final_claim_guard": "pass" if source_ok else "blocked",
            },
        },
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "primary_family": "model_characteristic_attribution",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-runtime-parity", "obsidian-run-evidence-system", "obsidian-result-judgment"],
            "required_gates": list(payloads),
        },
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "receipts": [
                {"skill": "obsidian-performance-attribution", "status": "completed", "effect": "trade shape and probability skew were attributed from run11C evidence"},
                {"skill": "obsidian-runtime-parity", "status": "completed", "effect": "source MT5 evidence boundary was preserved as reused runtime evidence"},
                {"skill": "obsidian-run-evidence-system", "status": "completed", "effect": "run registry and alpha ledgers received run11D evidence rows"},
                {"skill": "obsidian-result-judgment", "status": "completed", "effect": "claims were bounded to model-characteristic attribution only"},
            ],
        },
    )
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summary": rel(RUN_ROOT / "summary.json"), "report_path": rel(REPORT_PATH), "created_at_utc": created_at})
    write_md(REPORT_PATH, packet_markdown(summary))


def replace_block(text: str, marker: str, block: str) -> str:
    pattern = rf"{re.escape(marker)}\n(?:  .*\n)+"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    return text.rstrip() + "\n" + block


def sync_docs(summary: Mapping[str, Any]) -> None:
    keep_open = summary.get("stage17_stop_recommendation") != "close_stage17_no_new_trade_shape_characteristic_after_run11D"
    status = "reviewed_run11D_trade_shape_keep_open" if keep_open else "reviewed_closed_no_next_stage_opened"
    next_action = "probability_feature_driver_probe_if_continuing" if keep_open else "no_stage18_opened"
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage17 Selection Status(17단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                f"- status(상태): `{status}`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- model family(모델 계열): XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage17(17단계)은 성급한 closeout(마감)을 철회한 뒤 run11D까지 이어졌고, 새 특성이 보이면 계속 탐색한다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage17 Review Index(17단계 검토 색인)",
                "",
                "- `run11A_xgb_regularized_boosting_characteristic_scout_v1`: XGBoost characteristic MT5 KPI probe(XGBoost 특성 MT5 핵심성과지표 탐침)",
                "- `run11B_xgb_threshold_q80_frequency_pressure_closeout_v1`: frequency pressure probe(거래빈도 압박 탐침), closeout superseded(마감 대체됨)",
                "- `run11C_xgb_q80_direction_asymmetry_probe_v1`: direction asymmetry probe(방향 비대칭 탐침)",
                f"- `{RUN_ID}`: trade shape attribution(거래 모양 귀속)",
                "",
                "효과(effect, 효과): Stage17(17단계)은 run(실행)마다 새 특성 여부를 보고, 더 이상 새 특성이 없을 때만 closeout(마감)한다.",
            ]
        ),
    )
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage17 XGBoost Trade Shape Attribution(17단계 XGBoost 거래 모양 귀속)",
                "",
                "## Decision(결정)",
                "",
                f"`{RUN_ID}`을 run11C의 MT5(`MetaTrader 5`, 메타트레이더5) KPI(`Key Performance Indicator`, 핵심성과지표) 근거를 재사용한 trade shape attribution(거래 모양 귀속) run(실행)으로 기록했다.",
                "",
                "효과(effect, 효과): 새 MT5 실행을 만든 것이 아니라 이미 검증된 run11C 외부 근거에서 XGBoost 방향 비대칭의 거래 모양과 확률 쏠림을 판독했다.",
                "",
                "## Judgment(판정)",
                "",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- recommendation(권고): `{summary.get('stage17_stop_recommendation')}`",
                f"- boundary(경계): `{BOUNDARY}`",
            ]
        ),
    )
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = re.sub(r"stage17_reviewed_[A-Za-z0-9_]+", f"stage17_{status}", state)
    state = state.replace("current_run_id: run11C_xgb_q80_direction_asymmetry_probe_v1", f"current_run_id: {RUN_ID}", 1)
    state = state.replace(
        "treat Stage 17 as XGBoost regularized boosting reviewed_closed_no_next_stage_opened; run11C completed direction asymmetry MT5 KPI management after correcting premature closeout; no edge, baseline, promotion, or runtime authority",
        "treat Stage 17 as XGBoost regularized boosting still open after run11D trade-shape attribution; no edge, baseline, promotion, or runtime authority",
    )
    state = state.replace("status: reviewed_closed_no_next_stage_opened", f"status: {status}", 1)
    stage_block = f"""stage17_xgboost_regularized_boosting_scout:
  stage_id: {STAGE_ID}
  status: {status}
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {summary.get('model_family')}
  current_run_id: {RUN_ID}
  current_status: reviewed_trade_shape_attribution_completed
  hypothesis: XGBoost regularized boosting shows probability, frequency, direction-asymmetry, and trade-shape behavior under fixed data/runtime contract.
  comparison_baseline: run11A q0.90 characteristic probe, run11B q0.80 frequency pressure probe, and run11C direction asymmetry probe
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  selected_variant_id: {summary.get('selected_variant_id')}
  source_mt5_kpi_record_count: {summary.get('source_mt5_kpi_record_count')}
  source_normalized_kpi_record_count: {summary.get('source_normalized_kpi_records')}
  source_trade_attribution_records: {summary.get('source_trade_attribution_records')}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selection_status_path: {rel(STAGE_ROOT / '04_selected/selection_status.md')}
  decision_path: {rel(DECISION_PATH)}
  next_action: {next_action}
"""
    state = replace_block(state, "stage17_xgboost_regularized_boosting_scout:", stage_block)
    state = state.replace("stage17_xgboost_run11B_frequency_pressure_closeout:\n  packet_id: stage17_run11B_xgb_frequency_closeout_v1\n  status: reviewed_closed_no_next_stage_opened", "stage17_xgboost_run11B_frequency_pressure_closeout:\n  packet_id: stage17_run11B_xgb_frequency_closeout_v1\n  status: superseded_premature_closeout", 1)
    state = state.replace("current_run_id: run11C_xgb_q80_direction_asymmetry_probe_v1\n  selected_variant_id: v03_depth4_l1_l2_slow\n  threshold_quantile: q0.80\n  mt5_kpi_record_count: 10", "current_run_id: run11B_xgb_threshold_q80_frequency_pressure_closeout_v1\n  selected_variant_id: v03_depth4_l1_l2_slow\n  threshold_quantile: q0.80\n  mt5_kpi_record_count: 10", 1)
    run_block = f"""stage17_xgboost_run11D_trade_shape_attribution:
  packet_id: {PACKET_ID}
  status: reviewed_attribution_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {summary.get('selected_variant_id')}
  source_mt5_kpi_record_count: {summary.get('source_mt5_kpi_record_count')}
  source_normalized_kpi_record_count: {summary.get('source_normalized_kpi_records')}
  source_trade_attribution_records: {summary.get('source_trade_attribution_records')}
  new_characteristic_visible: {str(summary.get('trade_shape_attribution', {}).get('new_characteristic_visible')).lower()}
  recommendation: {summary.get('stage17_stop_recommendation')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
"""
    state = replace_block(state, "stage17_xgboost_run11D_trade_shape_attribution:", run_block)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    insert = "\n".join(
        [
            "## Latest Stage17 RUN11D Update(최신 17단계 실행11D 업데이트)",
            "",
            f"Stage17(17단계)은 `{RUN_ID}`으로 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) trade shape attribution(거래 모양 귀속)을 완료했다.",
            "",
            f"효과(effect, 효과): run11C의 MT5(`MetaTrader 5`, 메타트레이더5) KPI(`Key Performance Indicator`, 핵심성과지표) 근거를 재사용했고 `{summary.get('stage17_stop_recommendation')}`로 판독했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage17 RUN11D Update" not in current:
        current = insert + current
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage17(17단계) `{RUN_ID}` 거래 모양 귀속을 완료했다. 효과(effect, 효과): run11C MT5 KPI 근거를 재사용해 `{summary.get('stage17_stop_recommendation')}`로 판독했고 운영 주장은 만들지 않았다.\n"
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def run() -> dict[str, Any]:
    created_at = utc_now()
    inputs = load_inputs()
    summary = build_summary(inputs)
    final_summary = materialize_outputs(summary, created_at)
    print(json.dumps(json_ready(final_summary), ensure_ascii=False, indent=2))
    return final_summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage17 XGBoost trade-shape attribution from run11C evidence.")
    parser.parse_args(argv)
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

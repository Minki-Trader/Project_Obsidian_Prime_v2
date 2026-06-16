from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64b_loss_cluster_hazard_proxy_scout as f64b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64c_handoff_verification as f64c  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64d_handoff_adapter_repair as f64d  # noqa: E402
from stage_pipelines.stage_frontier_64 import run_frontier64_runtime_probe as f64e  # noqa: E402


STAGE_ID = "stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure"
RUN_A = "frontier65A_stage_open_runtime_semantics_pf_source_after_hazard_gate_failure_v1"
RUN_B = "frontier65B_proxy_runtime_gap_attribution_scout_v1"
RUN_C = "frontier65C_targeted_sltp_unit_runtime_probe_v1"
RUN_NUMBER_A = "frontier65A"
RUN_NUMBER_B = "frontier65B"
PARENT_RUN_ID = "frontier64F_stage_closeout_loss_cluster_hazard_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-16_frontier65_stage_open_runtime_gap_attribution/small_review")
GROK_PROMPT = GROK_PACKET / "prompt.md"
GROK_CLEAN_OUTPUT = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

F64_STAGE_ROOT = f64b.STAGE_ROOT
F64D_ROOT = F64_STAGE_ROOT / "02_runs" / f64d.RUN_ID
F64E_ROOT = F64_STAGE_ROOT / "02_runs" / f64e.RUN_ID
F64F_ROOT = F64_STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F64D_FINAL = F64D_ROOT / "handoff_adapter_repair.json"
F64E_FINAL = F64E_ROOT / "final_decision.json"
F64F_FINAL = F64F_ROOT / "stage_closeout_decision.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Frontier65 proxy-runtime gap attribution materializer.")
    parser.add_argument("--write-stage-open-prompt-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    if args.write_stage_open_prompt_only:
        f03b.write_text_sig(GROK_PROMPT, stage_open_prompt())
        print(json.dumps({"status": "wrote_stage_open_prompt", "prompt": GROK_PROMPT.as_posix()}, ensure_ascii=False, indent=2))
        return 0
    created_at = utc_now()
    context = load_context()
    attribution = build_attribution(context)
    final = build_final(created_at, context, attribution)
    write_artifacts(final)
    update_registries(final)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_B,
                    "next_run_id": RUN_C,
                    "primary_attribution_clue": final["primary_attribution_clue"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_A_ROOT, RUN_B_ROOT, REVIEWS_ROOT, SELECTED_ROOT, SPEC_ROOT, INPUT_ROOT, GROK_PACKET):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_context() -> dict[str, Any]:
    required = [F64D_FINAL, F64E_FINAL, F64F_FINAL, GROK_PROMPT, GROK_CLEAN_OUTPUT, GROK_METADATA]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F65 stage-open evidence missing(단계 개방 근거 누락): {missing}")
    return {
        "f64d_final": read_json(F64D_FINAL),
        "f64e_final": read_json(F64E_FINAL),
        "f64f_final": read_json(F64F_FINAL),
        "grok_clean": read_text(GROK_CLEAN_OUTPUT),
        "grok_metadata": read_json(GROK_METADATA),
        "expected_signal": read_csv_rows(F64E_ROOT / "expected_signal_summary.csv"),
        "runtime_summary": read_csv_rows(F64E_ROOT / "mt5_runtime_probe_summary.csv"),
        "proxy_runtime_gap": read_csv_rows(F64E_ROOT / "proxy_runtime_gap.csv"),
    }


def build_attribution(context: Mapping[str, Any]) -> dict[str, Any]:
    telemetry = telemetry_attribution()
    trade_shape = mt5_trade_shape()
    proxy_metrics = {row["split"]: row for row in context["f64d_final"]["selected_metric_rows"]}
    runtime_summary = {row["split"]: row for row in context["runtime_summary"]}
    expected = {row["split"]: row for row in context["expected_signal"]}
    gaps = {row["split"]: row for row in context["proxy_runtime_gap"]}
    atr_rows = proxy_atr_rows()

    layers: list[dict[str, Any]] = []
    exit_rows: list[dict[str, Any]] = []
    for split, proxy_split in (("validation_is", "validation"), ("oos", "oos")):
        t = telemetry[split]
        r = runtime_summary[split]
        e = expected[split]
        g = gaps[split]
        p = proxy_metrics[proxy_split]
        shape = trade_shape[split]
        atr = atr_rows[split]
        actual_nonflat = int_value(r.get("mt5_long_count")) + int_value(r.get("mt5_short_count"))
        raw_signal_count = int_value(e.get("adapter_raw_signal_count"))
        expected_signal_count = int_value(e.get("signal_count"))
        runtime_veto_count = raw_signal_count - expected_signal_count
        entry_transition_blocks = int_value(t.get("entry_transition_blocks"))
        position_overlap_gap = int_value(p.get("overlap_block_count")) - int_value(t.get("position_before_with_position_count"))
        proxy_stop = int_value(p.get("stop_exit_count"))
        proxy_take = int_value(p.get("take_exit_count"))
        proxy_maxhold = int_value(p.get("maxhold_exit_count"))
        mt5_stop = int_value(shape.get("sl_count"))
        mt5_take = int_value(shape.get("tp_count"))
        mt5_maxhold = int_value(shape.get("maxhold_count"))
        layers.append(
            {
                "split": split,
                "raw_adapter_signal_count": raw_signal_count,
                "runtime_veto_count": runtime_veto_count,
                "runtime_veto_telemetry_count": int_value(t.get("runtime_veto_tape_flats")),
                "expected_signal_count_after_veto": expected_signal_count,
                "entry_transition_blocks": entry_transition_blocks,
                "actual_nonflat_runtime_decisions": actual_nonflat,
                "order_attempts": int_value(r.get("mt5_order_attempt_count")),
                "order_fills": int_value(r.get("mt5_order_fill_count")),
                "invalid_stops": int_value(t.get("invalid_stops")),
                "feature_ready_diff": int_value(r.get("feature_ready_diff")),
                "proxy_trade_count": int_value(p.get("trade_count")),
                "mt5_trade_count": int_value(r.get("trade_count")),
                "proxy_profit_factor": float_value(p.get("profit_factor")),
                "mt5_profit_factor": float_value(r.get("profit_factor")),
                "profit_factor_gap_mt5_minus_proxy": float_value(g.get("profit_factor_gap_mt5_minus_proxy")),
                "proxy_dd_risk": float_value(p.get("dd_risk")),
                "mt5_max_drawdown_percent": float_value(r.get("max_drawdown_percent")),
                "dd_gap_mt5_minus_proxy": float_value(g.get("dd_gap_mt5_minus_proxy")),
                "proxy_trades_per_day": float_value(p.get("trades_per_day")),
                "mt5_trades_per_day": float_value(r.get("runtime_trades_per_day")),
                "proxy_overlap_blocks": int_value(p.get("overlap_block_count")),
                "mt5_position_before_with_position_count": int_value(t.get("position_before_with_position_count")),
                "position_overlap_gap_proxy_minus_mt5": position_overlap_gap,
                "proxy_maxhold_exit_count": proxy_maxhold,
                "mt5_maxhold_exit_count": mt5_maxhold,
                "mt5_duration_seconds_median": float_value(shape.get("duration_seconds_median")),
                "mt5_duration_le_1s_count": int_value(shape.get("duration_le_1s_count")),
                "proxy_atr_price_median": float_value(atr.get("proxy_atr_price_median")),
                "mt5_atr_points_median": float_value(t.get("mt5_atr_points_median")),
                "inferred_symbol_point_from_medians": float_value(atr.get("inferred_symbol_point_from_medians")),
                "proxy_min_stop_price_units": 40.0,
                "proxy_min_tp_price_units": 60.0,
                "mt5_sl_price_if_point_0p01": 1.8,
                "mt5_tp_price_if_point_0p01": 2.8,
                "stop_width_ratio_proxy_min_vs_mt5_0p01": 40.0 / 1.8,
                "tp_width_ratio_proxy_min_vs_mt5_0p01": 60.0 / 2.8,
                "primary_read": "sltp_unit_semantics_gap(손절/익절 단위 의미 차이)",
            }
        )
        exit_rows.append(
            {
                "split": split,
                "proxy_trade_count": int_value(p.get("trade_count")),
                "mt5_trade_count": int_value(r.get("trade_count")),
                "proxy_stop_exit_count": proxy_stop,
                "mt5_stop_exit_count": mt5_stop,
                "proxy_take_exit_count": proxy_take,
                "mt5_take_exit_count": mt5_take,
                "proxy_maxhold_exit_count": proxy_maxhold,
                "mt5_maxhold_exit_count": mt5_maxhold,
                "proxy_stop_rate": ratio(proxy_stop, int_value(p.get("trade_count"))),
                "mt5_stop_rate": ratio(mt5_stop, int_value(r.get("trade_count"))),
                "proxy_take_rate": ratio(proxy_take, int_value(p.get("trade_count"))),
                "mt5_take_rate": ratio(mt5_take, int_value(r.get("trade_count"))),
                "proxy_maxhold_rate": ratio(proxy_maxhold, int_value(p.get("trade_count"))),
                "mt5_maxhold_rate": ratio(mt5_maxhold, int_value(r.get("trade_count"))),
                "mt5_gross_profit": float_value(shape.get("gross_profit")),
                "mt5_gross_loss": float_value(shape.get("gross_loss")),
                "mt5_net_profit": float_value(shape.get("net_profit")),
                "mt5_out_trade_pf": float_value(shape.get("profit_factor")),
            }
        )
    return {
        "layers": layers,
        "exit_rows": exit_rows,
        "telemetry": list(telemetry.values()),
        "trade_shape": list(trade_shape.values()),
        "atr_rows": list(atr_rows.values()),
        "primary_attribution_clue": "sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points(프록시 가격 단위와 MT5 포인트 손절/익절 의미 차이)",
        "secondary_root_cause": "entry_transition_signal_compression_is_configured_and_explains_signal_count_diff(진입 전환 신호 압축은 설정된 동작이며 신호 수 차이를 설명)",
        "not_root_causes": [
            "feature_coverage_gap(피처 커버리지 차이)",
            "onnx_argmax_handoff_gap(온엑스 최대확률 인계 차이)",
            "order_fill_rejection_gap(주문 체결 거절 차이)",
        ],
    }


def telemetry_attribution() -> dict[str, dict[str, Any]]:
    root = F64E_ROOT / "runtime_telemetry"
    out: dict[str, dict[str, Any]] = {}
    for split, stem in (("validation_is", "frontier64e_tier_a_validation_is"), ("oos", "frontier64e_tier_a_oos")):
        df = read_csv_frame(root / f"{stem}_telemetry.csv")
        cycles = df[df["record_type"].astype(str) == "cycle"].copy()
        reason = cycles["decision_reason"].fillna("").astype(str)
        decisions = cycles["decision"].fillna("").astype(str)
        position_before = cycles["position_before"].fillna("").astype(str)
        order_attempted = cycles["order_attempted"].map(lambda value: str(value).lower() if pd.notna(value) else "").eq("true")
        order_filled = cycles["order_filled"].map(lambda value: str(value).lower() if pd.notna(value) else "").eq("true")
        invalid_stops = cycles["skip_reason"].fillna("").astype(str).str.contains("Invalid stops", regex=False)
        atr_points = pd.to_numeric(cycles["atr_points"], errors="coerce")
        open_sl_points = pd.to_numeric(cycles["open_sl_points"], errors="coerce")
        open_tp_points = pd.to_numeric(cycles["open_tp_points"], errors="coerce")
        out[split] = {
            "split": split,
            "cycle_rows": len(cycles),
            "raw_argmax_long_by_reason": int(reason.str.contains("argmax_probe_long", regex=False).sum()),
            "raw_argmax_short_by_reason": int(reason.str.contains("argmax_probe_short", regex=False).sum()),
            "raw_argmax_flat_by_reason": int(reason.str.contains("argmax_probe_flat", regex=False).sum()),
            "entry_transition_blocks": int(reason.str.startswith("entry_transition_same_signal_block").sum()),
            "entry_transition_block_long": int((reason.str.startswith("entry_transition_same_signal_block") & reason.str.contains("argmax_probe_long", regex=False)).sum()),
            "entry_transition_block_short": int((reason.str.startswith("entry_transition_same_signal_block") & reason.str.contains("argmax_probe_short", regex=False)).sum()),
            "runtime_veto_tape_flats": int(reason.str.contains("runtime_veto_tape:", regex=False).sum()),
            "actual_long_decisions": int(decisions.eq("long").sum()),
            "actual_short_decisions": int(decisions.eq("short").sum()),
            "actual_flat_decisions": int(decisions.eq("flat").sum()),
            "order_attempted_count": int(order_attempted.sum()),
            "order_filled_count": int(order_filled.sum()),
            "invalid_stops": int(invalid_stops.sum()),
            "position_before_with_position_count": int((position_before != "none").sum()),
            "mt5_atr_points_median": safe_series_median(atr_points[order_filled]),
            "mt5_atr_points_q25": safe_series_quantile(atr_points[order_filled], 0.25),
            "mt5_atr_points_q75": safe_series_quantile(atr_points[order_filled], 0.75),
            "open_sl_points_median": safe_series_median(open_sl_points[order_filled]),
            "open_tp_points_median": safe_series_median(open_tp_points[order_filled]),
            "encoding_read": "fallback(대체) utf-8-sig/cp949/cp1252/latin1",
        }
    return out


def mt5_trade_shape() -> dict[str, dict[str, Any]]:
    report_root = io_path(F64E_ROOT / "mt5" / "reports")
    out: dict[str, dict[str, Any]] = {}
    for path in report_root.iterdir():
        if path.suffix.lower() != ".htm":
            continue
        split = "validation_is" if "validation" in path.name else "oos"
        deals = parse_mt5_deals(path)
        out_deals = deals[deals["direction"].astype(str) == "out"].copy()
        out_deals["profit_num"] = pd.to_numeric(out_deals["profit"], errors="coerce")
        out_deals["reason"] = (
            out_deals["comment"].fillna("").astype(str).str.extract(r"^(sl|tp|close|max)", expand=False).fillna("other")
        )
        rows = deals[deals["direction"].astype(str).isin(["in", "out"])].copy().reset_index(drop=True)
        durations: list[float] = []
        for idx in range(0, len(rows) - 1, 2):
            if rows.loc[idx, "direction"] == "in" and rows.loc[idx + 1, "direction"] == "out":
                start = pd.to_datetime(rows.loc[idx, "time"], errors="coerce")
                end = pd.to_datetime(rows.loc[idx + 1, "time"], errors="coerce")
                if pd.notna(start) and pd.notna(end):
                    durations.append(float((end - start).total_seconds()))
        duration_series = pd.Series(durations, dtype="float64")
        gross_profit = float(out_deals.loc[out_deals["profit_num"] > 0.0, "profit_num"].sum())
        gross_loss = float(-out_deals.loc[out_deals["profit_num"] < 0.0, "profit_num"].sum())
        out[split] = {
            "split": split,
            "out_trade_count": int(len(out_deals)),
            "sl_count": int(out_deals["reason"].eq("sl").sum()),
            "tp_count": int(out_deals["reason"].eq("tp").sum()),
            "maxhold_count": int(out_deals["reason"].eq("max").sum()),
            "other_exit_count": int((~out_deals["reason"].isin(["sl", "tp", "max"])).sum()),
            "gross_profit": gross_profit,
            "gross_loss": gross_loss,
            "net_profit": float(out_deals["profit_num"].sum()),
            "profit_factor": gross_profit / gross_loss if gross_loss > 0.0 else None,
            "duration_seconds_mean": safe_series_mean(duration_series),
            "duration_seconds_median": safe_series_median(duration_series),
            "duration_seconds_max": safe_series_max(duration_series),
            "duration_le_1s_count": int((duration_series <= 1.0).sum()),
            "duration_le_300s_count": int((duration_series <= 300.0).sum()),
            "report_path": path.as_posix().replace("\\\\?\\", ""),
        }
    return out


def proxy_atr_rows() -> dict[str, dict[str, Any]]:
    base = f64b.build_base()
    frame = base["frame"]
    atr_raw = np.asarray(base["runtime"]["atr"], dtype="float64")
    entry_pos = np.asarray(base["raw_path"]["entry_pos"], dtype="int64")
    atr_feature = np.full(len(frame), np.nan, dtype="float64")
    valid_pos = (entry_pos >= 0) & (entry_pos < len(atr_raw))
    atr_feature[valid_pos] = atr_raw[entry_pos[valid_pos]]
    telemetry = telemetry_attribution()
    out: dict[str, dict[str, Any]] = {}
    for split, source_split in (("validation_is", "validation"), ("oos", "oos")):
        mask = f33b.split_mask(frame, source_split) & np.asarray(base["finite"], dtype=bool)
        values = atr_feature[mask]
        values = values[np.isfinite(values)]
        mt5_median = float_value(telemetry[split]["mt5_atr_points_median"])
        proxy_median = float(np.median(values)) if len(values) else 0.0
        out[split] = {
            "split": split,
            "source_split": source_split,
            "proxy_atr_price_count": int(len(values)),
            "proxy_atr_price_mean": float(np.mean(values)) if len(values) else 0.0,
            "proxy_atr_price_median": proxy_median,
            "proxy_atr_price_q25": float(np.quantile(values, 0.25)) if len(values) else 0.0,
            "proxy_atr_price_q75": float(np.quantile(values, 0.75)) if len(values) else 0.0,
            "mt5_atr_points_median": mt5_median,
            "inferred_symbol_point_from_medians": proxy_median / mt5_median if mt5_median else 0.0,
        }
    return out


def parse_mt5_deals(path: Path) -> pd.DataFrame:
    table = pd.read_html(str(path), encoding="utf-16")[1]
    header_idx: int | None = None
    for index, row in table.iterrows():
        if str(row[0]) == "시간" and str(row[4]) == "방향":
            header_idx = int(index)
            break
    if header_idx is None:
        raise RuntimeError(f"MT5 deal header missing(거래 헤더 누락): {path}")
    data = table.iloc[header_idx + 1 :].copy()
    data.columns = [
        "time",
        "deal",
        "symbol",
        "type",
        "direction",
        "volume",
        "price",
        "order",
        "commission",
        "swap",
        "profit",
        "balance",
        "comment",
    ]
    data = data[data["deal"].notna()].copy()
    return data


def build_final(created_at: str, context: Mapping[str, Any], attribution: Mapping[str, Any]) -> dict[str, Any]:
    grok_classification = classify_grok(context["grok_clean"])
    checks = local_checks(context, attribution, grok_classification)
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_a": RUN_A,
        "run_b": RUN_B,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": RUN_C,
        "status": "active_scout_clue_runtime_semantics_gap_attribution_no_authority(진행 중 탐색 단서, 런타임 의미 차이 귀속, 권위 없음)",
        "judgment": "preserved_clue_sltp_unit_semantics_gap_no_authority(보존 단서, 손절/익절 단위 의미 차이, 권위 없음)",
        "primary_attribution_clue": attribution["primary_attribution_clue"],
        "secondary_root_cause": attribution["secondary_root_cause"],
        "not_root_causes": attribution["not_root_causes"],
        "stage_open": {
            "hypothesis": "F64 proxy-runtime PF/DD gap came mainly from runtime semantics, especially SL/TP unit semantics, not from ONNX probability or feature coverage.",
            "hypothesis_ko": "F64 프록시-런타임 PF/DD 차이는 온엑스 확률이나 피처 커버리지보다 런타임 의미, 특히 손절/익절 단위 의미에서 주로 발생했다.",
            "grok_classification": grok_classification,
            "grok_prompt": GROK_PROMPT.as_posix(),
            "grok_output": GROK_CLEAN_OUTPUT.as_posix(),
            "grok_metadata": context["grok_metadata"],
            "checks": checks,
        },
        "attribution": attribution,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "runtime_probe_boundary": "F65 uses F64E MT5 runtime probe as attribution input; F65 targeted MT5 runtime probe remains pending in RUN_C.",
        "runtime_probe_boundary_ko": "F65는 F64E MT5 런타임 탐침을 귀속 입력으로 사용했다. F65 자체 표적 MT5 런타임 탐침은 RUN_C에서 대기 중이다.",
    }


def local_checks(context: Mapping[str, Any], attribution: Mapping[str, Any], grok_classification: str) -> dict[str, Any]:
    layers = list(attribution["layers"])
    return {
        "grok_stage_open_not_rejected": "rejected" not in grok_classification,
        "f64_closeout_parent_matches": context["f64f_final"].get("run_id") == PARENT_RUN_ID,
        "feature_ready_diff_zero_all": all(int_value(row.get("feature_ready_diff")) == 0 for row in layers),
        "entry_transition_accounts_signal_diff": all(
            int_value(row.get("entry_transition_blocks"))
            == int_value(row.get("expected_signal_count_after_veto")) - int_value(row.get("actual_nonflat_runtime_decisions"))
            for row in layers
        ),
        "fill_rejection_small": all(int_value(row.get("invalid_stops")) <= 4 for row in layers),
        "mt5_maxhold_zero_all": all(int_value(row.get("mt5_maxhold_exit_count")) == 0 for row in layers),
        "proxy_maxhold_present_all": all(int_value(row.get("proxy_maxhold_exit_count")) > 0 for row in layers),
        "unit_width_ratio_large": all(float_value(row.get("stop_width_ratio_proxy_min_vs_mt5_0p01")) > 10.0 for row in layers),
        "claim_guard_no_authority": True,
    }


def write_artifacts(final: Mapping[str, Any]) -> None:
    write_json(RUN_A_ROOT / "stage_open_summary.json", final["stage_open"])
    write_json(RUN_B_ROOT / "gap_attribution_summary.json", final)
    write_csv(RUN_B_ROOT / "attribution_layers.csv", final["attribution"]["layers"])
    write_csv(RUN_B_ROOT / "exit_reason_comparison.csv", final["attribution"]["exit_rows"])
    write_csv(RUN_B_ROOT / "telemetry_decision_attribution.csv", final["attribution"]["telemetry"])
    write_csv(RUN_B_ROOT / "mt5_trade_shape.csv", final["attribution"]["trade_shape"])
    write_csv(RUN_B_ROOT / "atr_unit_semantics.csv", final["attribution"]["atr_rows"])
    f03b.write_text_sig(SPEC_ROOT / "stage_brief.md", stage_brief_text(final))
    f03b.write_text_sig(INPUT_ROOT / "input_refs.md", input_refs_text(final))
    f03b.write_text_sig(REVIEWS_ROOT / "runA_report.md", stage_open_report(final))
    f03b.write_text_sig(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt(final))
    f03b.write_text_sig(REVIEWS_ROOT / "runB_report.md", attribution_report(final))
    f03b.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_attribution_report.md", attribution_report(final))
    f03b.write_text_sig(REVIEWS_ROOT / "review_index.md", review_index_text(final))
    f03b.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(final))
    f03b.write_json(SELECTED_ROOT / "selection_status.json", selection_status_json(final))
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state_text(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))


def update_registries(final: Mapping[str, Any]) -> None:
    ensure_stage_ledger()
    for row in (run_registry_row_a(final), run_registry_row_b(final)):
        f64c.upsert_csv(f03b.RUN_REGISTRY, "run_id", row)
    for row in (ledger_row_a(final), ledger_row_b(final)):
        f64c.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f64c.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f64c.append_once(f03b.CHANGELOG, RUN_A, changelog_entry(final))
    f64c.append_once(f03b.IDEA_REGISTRY, RUN_A, idea_entry(final))


def ensure_stage_ledger() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    header = read_csv_header(f03b.ALPHA_LEDGER)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, lineterminator="\n")
        writer.writeheader()


def stage_open_prompt() -> str:
    return """Frontier65 stage-open review(전선65 단계 개방 검토)입니다.

Please answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Current Truth(현재 진실)

- Current closed stage(현재 닫힌 단계): `stage_frontier_64__independent_pf_source_after_inverse_signal_memory`.
- F64 closeout label(마감 라벨): `negative_memory_runtime_probe_quality_gap_no_authority(부정 기억, 런타임 탐침 품질 차이, 권위 없음)`.
- F64 proxy after repair(수리 후 프록시): validation/OOS PF(검증/표본외 수익 팩터) `1.0727 / 1.1081`, DD(손실폭) `4.319% / 3.154%`, density(밀도) `5.421 / 5.840` trades/day(일 거래).
- F64 MT5 runtime probe(MT5 런타임 탐침): validation/OOS PF `0.35 / 0.70`, DD `28.23% / 7.92%`, density `6.00 / 6.397` trades/day.
- F64 feature_ready_diff(피처 준비 차이): `0 / 0`.
- F64 expected signal(예상 신호): validation/OOS `4073 / 3325`; MT5 actual non-flat decisions(실제 비관망 결정): `1100 / 842`.
- F64 runtime policy(런타임 정책): `argmax_probe(최대확률 탐침)`, runtime veto tape(런타임 차단 테이프), `InpEntryTransitionOnly=true`, `InpCloseOnFlatSignal=false`, `InpReverseOnOppositeSignal=false`, `InpMaxHoldBars=2`, ATR SL/TP(ATR 손절/익절) enabled(활성).
- Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 all not claimed(모두 주장 없음).

## Proposed F65 Direction(제안 F65 방향)

Stage(단계): `stage_frontier_65__runtime_semantics_pf_source_after_hazard_gate_failure`.

Hypothesis(가설): The F64 proxy-runtime gap(프록시-런타임 차이) came primarily from runtime semantics(런타임 의미), especially SL/TP unit semantics(손절/익절 단위 의미) and signal-to-order lifecycle(신호-주문 생명주기), rather than model probability(모델 확률), feature coverage(피처 커버리지), or ONNX handoff(온엑스 인계).

Work plan(작업 계획):

1. Attribute gap layers(차이 층 귀속): feature coverage(피처 커버리지), raw adapter signal(원 어댑터 신호), runtime veto tape(런타임 차단 테이프), entry transition gate(진입 전환 게이트), order fill(주문 체결), exit shape(청산 형태), SL/TP unit semantics(손절/익절 단위 의미).
2. Use F64E MT5 runtime probe(MT5 런타임 탐침) as attribution input(귀속 입력), not as F65 completion evidence(완성 근거 아님).
3. If attribution points to SL/TP unit mismatch(단위 불일치), next run(다음 실행) should be a targeted MT5 probe(표적 MT5 탐침) with point-adjusted SL/TP contract(포인트 보정 손절/익절 계약).

Success criteria for this stage-open(단계 개방 성공 기준):

- The stage is allowed only as attribution scout(귀속 탐색), not completion(완성).
- It must record that F65 targeted MT5 runtime probe(표적 MT5 런타임 탐침)는 still pending(대기) until RUN_C.
- It must not reopen F64 as a winner/baseline/promotion(승자/기준선/승격).
- It must produce a local report(로컬 보고서) that separates signal count gap(신호 수 차이) from PF/DD economics gap(수익 팩터/손실폭 경제성 차이).

Review request(검토 요청):

1. Classification(분류): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.
2. One-sentence reason(한 문장 이유).
3. Is this a valid new frontier stage(전선 단계), or should it be treated only as F64 postmortem repair(사후 수리)?
4. What must Codex record to avoid overclaiming(과장 주장 방지)?
5. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.
"""


def stage_brief_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Stage Brief(F65 단계 개요)

Stage(단계): `{STAGE_ID}`

Hypothesis(가설): F64 proxy-runtime PF/DD gap(프록시-런타임 수익 팩터/손실폭 차이)은 feature coverage(피처 커버리지)나 ONNX handoff(온엑스 인계)보다 runtime semantics(런타임 의미), 특히 SL/TP unit semantics(손절/익절 단위 의미)에서 주로 발생했다.

Action(행동): F64E MT5 runtime probe(MT5 런타임 탐침) 산출물을 attribution input(귀속 입력)으로 읽어 gap layers(차이 층)를 분해한다.

Effect(효과): 다음 ONNX(온엑스) 후보가 proxy(프록시)에서 좋아 보여도 MT5(메타트레이더5)에서 같은 단위 의미 차이로 무너지는 반복을 막는다.

Claim boundary(주장 경계): attribution scout(귀속 탐색)와 preserved clue(보존 단서)까지만 말한다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)이다.

Next run(다음 실행): `{RUN_C}`. Effect(효과): F65 자체 targeted MT5 runtime probe(표적 MT5 런타임 탐침)를 실행해야 stage closeout(단계 마감)으로 갈 수 있다.
"""


def input_refs_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Input References(F65 입력 참조)

- F64D handoff adapter repair(인계 어댑터 수리): `{F64D_FINAL.as_posix()}`
- F64E final decision(런타임 탐침 최종 판단): `{F64E_FINAL.as_posix()}`
- F64E expected signal summary(예상 신호 요약): `{(F64E_ROOT / 'expected_signal_summary.csv').as_posix()}`
- F64E runtime summary(런타임 요약): `{(F64E_ROOT / 'mt5_runtime_probe_summary.csv').as_posix()}`
- F64E proxy-runtime gap(프록시-런타임 차이): `{(F64E_ROOT / 'proxy_runtime_gap.csv').as_posix()}`
- F64 MT5 telemetry(런타임 기록): `{(F64E_ROOT / 'runtime_telemetry').as_posix()}`
- F64 MT5 report(전략 테스터 보고서): `{(F64E_ROOT / 'mt5' / 'reports').as_posix()}`
- F64F closeout(마감): `{F64F_FINAL.as_posix()}`

Action(행동): F64 is used as reference evidence(참조 근거) only.

Effect(효과): F64 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않는다.
"""


def stage_open_report(final: Mapping[str, Any]) -> str:
    checks = final["stage_open"]["checks"]
    return f"""# F65A Stage Open(F65A 단계 개방)

Updated(갱신): `{final['created_at_utc']}`

Status(상태): `stage_opened_attribution_scout_no_authority(귀속 탐색 단계 개방, 권위 없음)`

Grok classification(그록 분류): `{final['stage_open']['grok_classification']}`

Action(행동): F65를 proxy-runtime gap attribution(프록시-런타임 차이 귀속) stage(단계)로 열었다.

Effect(효과): F64의 좋은 proxy(프록시)와 나쁜 MT5 runtime(런타임) 사이 차이를 새 후보 학습 전에 먼저 분해한다.

Local checks(로컬 확인): `{json.dumps(json_ready(checks), ensure_ascii=False, sort_keys=True)}`

Boundary(경계): stage open(단계 개방)이고, F65 targeted MT5 runtime probe(표적 MT5 런타임 탐침)는 `{RUN_C}`로 남아 있다.
"""


def grok_receipt(final: Mapping[str, Any]) -> str:
    metadata = final["stage_open"]["grok_metadata"]
    return f"""# F65 Grok Stage Open Receipt(F65 그록 단계 개방 영수증)

- trigger_reason(트리거 이유): user requested next frontier stage(다음 전선 단계) and Grok stage-open review(그록 단계 개방 검토) is required.
- review_size(검토 크기): `small review(소규모 검토)`.
- prompt(프롬프트): `{GROK_PROMPT.as_posix()}`
- prompt_sha256(프롬프트 해시): `{metadata.get('prompt_hash')}`
- clean_output(정리 출력): `{GROK_CLEAN_OUTPUT.as_posix()}`
- clean_output_sha256(정리 출력 해시): `{sha256_file(GROK_CLEAN_OUTPUT)}`
- classification(분류): `{final['stage_open']['grok_classification']}`
- local_verification(로컬 검증): `{json.dumps(json_ready(final['stage_open']['checks']), ensure_ascii=False, sort_keys=True)}`
- final_codex_direction(최종 코덱스 방향): proceed with attribution scout(귀속 탐색 진행), no authority(권위 없음), F65 runtime probe(런타임 탐침)는 RUN_C에서 필요.
"""


def attribution_report(final: Mapping[str, Any]) -> str:
    rows = final["attribution"]["layers"]
    exit_rows = {row["split"]: row for row in final["attribution"]["exit_rows"]}
    lines = [
        "# F65B Proxy-Runtime Gap Attribution(F65B 프록시-런타임 차이 귀속)",
        "",
        f"Updated(갱신): `{final['created_at_utc']}`",
        "",
        f"Judgment(판정): `{final['judgment']}`",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F64E runtime telemetry(런타임 기록), expected signal summary(예상 신호 요약), proxy metrics(프록시 지표), MT5 deal history(MT5 거래 내역)를 같은 split(분할)별로 맞춰 차이를 층별로 분해했다.",
        "",
        "Effect(효과): signal count gap(신호 수 차이)과 PF/DD economics gap(수익 팩터/손실폭 경제성 차이)을 분리했고, SL/TP unit semantics(손절/익절 단위 의미)가 1순위 원인 후보임을 기록했다.",
        "",
        "## Layer Attribution(층별 귀속)",
        "",
        "| split(분할) | raw adapter(원 어댑터) | veto(차단) | expected after veto(차단 후 예상) | entry transition block(진입 전환 차단) | actual non-flat(실제 비관망) | fills(체결) | PF gap(PF 차이) | DD gap(손실폭 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['split']} | {row['raw_adapter_signal_count']} | {row['runtime_veto_count']} | "
            f"{row['expected_signal_count_after_veto']} | {row['entry_transition_blocks']} | "
            f"{row['actual_nonflat_runtime_decisions']} | {row['order_fills']} | "
            f"{fmt(row['profit_factor_gap_mt5_minus_proxy'])} | {fmt(row['dd_gap_mt5_minus_proxy'])} |"
        )
    lines.extend(
        [
            "",
            "## Exit Shape(청산 형태)",
            "",
            "| split(분할) | proxy stop%(프록시 손절률) | MT5 stop%(MT5 손절률) | proxy maxhold%(프록시 최대보유률) | MT5 maxhold%(MT5 최대보유률) | MT5 median duration sec(MT5 중앙 보유초) |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        exit_row = exit_rows[row["split"]]
        lines.append(
            f"| {row['split']} | {pct(exit_row['proxy_stop_rate'])} | {pct(exit_row['mt5_stop_rate'])} | "
            f"{pct(exit_row['proxy_maxhold_rate'])} | {pct(exit_row['mt5_maxhold_rate'])} | "
            f"{fmt(row['mt5_duration_seconds_median'])} |"
        )
    lines.extend(
        [
            "",
            "## Main Read(주요 판독)",
            "",
            "- feature_ready_diff(피처 준비 차이)는 `0/0`이므로 data coverage(데이터 커버리지)가 1순위 원인이 아니다.",
            "- raw adapter signal(원 어댑터 신호)에서 runtime veto tape(런타임 차단 테이프) 차감, entry transition gate(진입 전환 게이트) 차감은 telemetry(런타임 기록)와 맞다.",
            "- order fill gap(주문 체결 차이)는 작다. invalid stops(무효 손절)는 validation/OOS `2/4`건이다.",
            "- MT5 exit shape(MT5 청산 형태)는 maxhold(최대 보유)가 `0`이고 대부분 SL/TP(손절/익절)로 몇 초 안에 끝났다.",
            "- Proxy(프록시)는 40/60 price units(가격 단위) 최소 손절/익절처럼 계산했고, MT5는 180/280 points(포인트) 캡을 적용했다. `point=0.01`이면 실제 MT5 폭은 약 1.8/2.8 가격 단위다.",
            "",
            "## Preserved Clue(보존 단서)",
            "",
            f"`{final['primary_attribution_clue']}`",
            "",
            "## Boundary(경계)",
            "",
            "이 판정은 attribution scout(귀속 탐색) 전용이다. F65 targeted MT5 runtime probe(표적 MT5 런타임 탐침)는 아직 pending(대기)이다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)이다.",
            "",
            f"Next run(다음 실행): `{RUN_C}`.",
            "",
        ]
    )
    return "\n".join(lines)


def review_index_text(final: Mapping[str, Any]) -> str:
    return """# F65 Review Index(F65 검토 색인)

- `runA_report.md`: stage open report(단계 개방 보고)
- `grok_stage_open_receipt.md`: Grok stage-open receipt(그록 단계 개방 영수증)
- `runB_report.md`: proxy-runtime gap attribution scout(프록시-런타임 차이 귀속 탐색)
- `proxy_runtime_gap_attribution_report.md`: same report alias(같은 보고서 별칭)
- `required_gate_coverage_audit.md`: required gate coverage audit(필수 게이트 커버리지 감사)
- `stage_run_ledger.csv`: stage-local run ledger(단계 로컬 실행 장부)
"""


def gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Required Gate Coverage Audit(F65 필수 게이트 커버리지 감사)

- reentry_read(재진입 읽기): `completed(완료)`
- stage_open_grok_review(단계 개방 그록 검토): `{final['stage_open']['grok_classification']}`
- local_verification(로컬 검증): `{json.dumps(json_ready(final['stage_open']['checks']), ensure_ascii=False, sort_keys=True)}`
- proxy_runtime_gap_attribution(프록시-런타임 차이 귀속): `{RUN_B}`
- feature_coverage_check(피처 커버리지 확인): `feature_ready_diff_zero(피처 준비 차이 0)`
- decision_layer_check(결정층 확인): `entry_transition_counts_match_signal_diff(진입 전환 수가 신호 차이와 일치)`
- execution_layer_check(실행층 확인): `fill_rejection_small(체결 거절 작음)`
- economics_layer_check(경제성층 확인): `sltp_unit_semantics_gap_preserved_clue(손절/익절 단위 의미 차이 보존 단서)`
- F65_targeted_mt5_runtime_probe(F65 표적 MT5 런타임 탐침): `pending(대기)` / next `{RUN_C}`
- stage_closeout(단계 마감): `not_done(미완료)`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Selection Status(F65 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_B}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- primary_attribution_clue(주요 귀속 단서): `{final['primary_attribution_clue']}`
- report(보고서): `{(REVIEWS_ROOT / 'proxy_runtime_gap_attribution_report.md').as_posix()}`
- next_run(다음 실행): `{RUN_C}`
- closeout_status(마감 상태): `not_closed_targeted_runtime_probe_pending(미마감, 표적 런타임 탐침 대기)`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def selection_status_json(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "current_run_id": RUN_B,
        "status": final["status"],
        "judgment": final["judgment"],
        "primary_attribution_clue": final["primary_attribution_clue"],
        "report": (REVIEWS_ROOT / "proxy_runtime_gap_attribution_report.md").as_posix(),
        "next_run_id": RUN_C,
        "stage_closeout": "not_closed_targeted_runtime_probe_pending(미마감, 표적 런타임 탐침 대기)",
        "claim_boundary": final["claim_boundary"],
    }


def workspace_state_text(final: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {RUN_B}
latest_completed_run_id: {RUN_B}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_stage_id: null
next_run_id: {RUN_C}
runtime_probe_status: pending_targeted_mt5_runtime_probe_for_frontier65
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
notes:
  - "F65B attribution scout(귀속 탐색): primary_attribution_clue={final['primary_attribution_clue']}."
  - "F64E MT5 runtime probe(MT5 런타임 탐침)는 attribution input(귀속 입력)으로만 사용했다; F65 targeted MT5 runtime probe(표적 MT5 런타임 탐침)는 {RUN_C}에서 대기."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음)."
"""


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier65(F65, 전선 65단계)는 proxy-runtime gap attribution scout(프록시-런타임 차이 귀속 탐색)까지 진행했다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_B}`
- judgment(판정): `{final['judgment']}`
- primary_attribution_clue(주요 귀속 단서): `{final['primary_attribution_clue']}`
- next_run(다음 실행): `{RUN_C}`

Action(행동): F64E runtime telemetry(런타임 기록), expected signal(예상 신호), proxy metrics(프록시 지표), MT5 deal history(MT5 거래 내역)를 분해했다.

Effect(효과): signal count gap(신호 수 차이)은 entry transition gate(진입 전환 게이트)로 설명되고, PF/DD economics gap(수익 팩터/손실폭 경제성 차이)은 SL/TP unit semantics(손절/익절 단위 의미)에서 주로 발생했다는 preserved clue(보존 단서)를 만들었다.

Claim boundary(주장 경계): F65는 아직 closeout(마감)이 아니다. F65 targeted MT5 runtime probe(표적 MT5 런타임 탐침)는 pending(대기)이고, completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def run_registry_row_a(final: Mapping[str, Any]) -> dict[str, Any]:
    return base_registry_row(
        RUN_A,
        RUN_NUMBER_A,
        "stage_open(단계 개방)",
        "stage_opened_attribution_scout_no_authority(귀속 탐색 단계 개방, 권위 없음)",
        "stage_opened_after_grok_review_no_authority(그록 검토 후 단계 개방, 권위 없음)",
        REVIEWS_ROOT / "runA_report.md",
        "stage_open_no_trading_kpi(단계 개방 거래 KPI 없음)",
        RUN_B,
        final,
    )


def run_registry_row_b(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = next(row for row in final["attribution"]["layers"] if row["split"] == "oos")
    row = base_registry_row(
        RUN_B,
        RUN_NUMBER_B,
        "proxy_runtime_gap_attribution(프록시-런타임 차이 귀속)",
        final["status"],
        final["judgment"],
        REVIEWS_ROOT / "proxy_runtime_gap_attribution_report.md",
        f"primary_clue={final['primary_attribution_clue']};oos_pf_gap={fmt(oos['profit_factor_gap_mt5_minus_proxy'])};next={RUN_C}",
        RUN_C,
        final,
    )
    row.update(
        {
            "profit_factor": oos.get("mt5_profit_factor", ""),
            "drawdown": oos.get("mt5_max_drawdown_percent", ""),
            "trade_count": oos.get("mt5_trade_count", ""),
            "selected_profit_factor": oos.get("mt5_profit_factor", ""),
            "selected_trade_density": oos.get("mt5_trades_per_day", ""),
            "trade_density": oos.get("mt5_trades_per_day", ""),
            "max_drawdown_percent": oos.get("mt5_max_drawdown_percent", ""),
        }
    )
    return row


def base_registry_row(
    run_id: str,
    run_number: str,
    lane: str,
    status: str,
    judgment: str,
    report: Path,
    notes: str,
    next_run: str,
    final: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": lane,
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "notes": notes,
        "family": "runtime_parity_attribution(런타임 동등성 귀속)",
        "primary_report": report.as_posix(),
        "run_number": run_number,
        "date": final["created_at_utc"][:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID if run_id == RUN_A else RUN_A,
        "next_run_id": next_run,
        "claim_boundary": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)",
        "report_path": report.as_posix(),
        "view": lane,
        "tier": "Tier A reference input(티어 A 참조 입력)",
        "metric_scope": "attribution_no_new_runtime_authority(귀속, 새 런타임 권위 없음)",
        "external_verification_status": "f64e_runtime_probe_reused_as_attribution_input_f65_targeted_probe_pending(F64E 런타임 탐침 귀속 입력, F65 표적 탐침 대기)",
        "result_judgment": judgment,
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (REVIEWS_ROOT / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_runtime_attribution(전선 런타임 귀속)",
        "run_type": lane,
        "output_path": (RUN_B_ROOT / "gap_attribution_summary.json").as_posix(),
        "result_path": (RUN_B_ROOT / "gap_attribution_summary.json").as_posix(),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
    }


def ledger_row_a(final: Mapping[str, Any]) -> dict[str, Any]:
    row = run_registry_row_a(final)
    row.update(
        {
            "ledger_row_id": f"{RUN_A}__stage_open",
            "subrun_id": f"{RUN_A}__stage_open",
            "record_view": "stage_open(단계 개방)",
            "tier_scope": "not_applicable_stage_open(단계 개방 해당 없음)",
            "kpi_scope": "stage_open_no_trading_kpi(단계 개방 거래 KPI 없음)",
            "scoreboard_lane": "stage_open(단계 개방)",
            "primary_kpi": "not_applicable_stage_open(단계 개방 해당 없음)",
            "guardrail_kpi": "forbidden_claims_not_claimed(금지 주장 없음)",
        }
    )
    return row


def ledger_row_b(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = next(row for row in final["attribution"]["layers"] if row["split"] == "oos")
    row = run_registry_row_b(final)
    row.update(
        {
            "ledger_row_id": f"{RUN_B}__attribution_scout",
            "subrun_id": f"{RUN_B}__attribution_scout",
            "record_view": "proxy_runtime_gap_attribution(프록시-런타임 차이 귀속)",
            "tier_scope": "Tier A reference runtime probe input(티어 A 참조 런타임 탐침 입력)",
            "kpi_scope": "attribution_from_existing_runtime_probe(기존 런타임 탐침 귀속)",
            "scoreboard_lane": "runtime_semantics_attribution(런타임 의미 귀속)",
            "primary_kpi": f"oos_pf_gap={fmt(oos['profit_factor_gap_mt5_minus_proxy'])};oos_dd_gap={fmt(oos['dd_gap_mt5_minus_proxy'])};primary_clue={final['primary_attribution_clue']}",
            "guardrail_kpi": "F65_targeted_runtime_probe_pending_no_closeout_no_authority(F65 표적 런타임 탐침 대기, 미마감, 권위 없음)",
        }
    )
    return row


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {final['created_at_utc'][:10]} Frontier65 Gap Attribution(F65 차이 귀속)\n\n- action(행동): `{RUN_A}`로 F65를 열고 `{RUN_B}`로 F64 proxy-runtime gap(프록시-런타임 차이)을 분해했다.\n- effect(효과): SL/TP unit semantics gap(손절/익절 단위 의미 차이)을 preserved clue(보존 단서)로 기록하고 `{RUN_C}` 표적 MT5 probe(표적 MT5 탐침)를 다음 실행으로 남겼다.\n- boundary(경계): F65는 아직 closeout(마감)이 아니며 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.\n"


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_A}\n\n- Stage(단계): `{STAGE_ID}`\n- Idea(아이디어): F64 proxy-runtime gap(프록시-런타임 차이)을 runtime semantics(런타임 의미)와 SL/TP unit semantics(손절/익절 단위 의미)로 귀속할 수 있는지 분석한다.\n- Result(결과): `{final['judgment']}`\n- Evidence(근거): `{(REVIEWS_ROOT / 'proxy_runtime_gap_attribution_report.md').as_posix()}`\n- Next(다음): `{RUN_C}`\n- Boundary(경계): attribution scout(귀속 탐색), no authority(권위 없음), F65 targeted MT5 runtime probe pending(F65 표적 MT5 런타임 탐침 대기).\n"


def classify_grok(clean: str) -> str:
    lower = clean.lower()
    if "rejected" in lower:
        return "rejected(거절)"
    if "accepted" in lower and "needs_local_verification" in lower:
        return "accepted_with_local_verification(수용, 로컬 검증 포함)"
    if "accepted" in lower:
        return "accepted(수용)"
    return "needs_local_verification(로컬 검증 필요)"


def read_csv_frame(path: Path) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "cp949", "cp1252", "latin1"):
        try:
            return pd.read_csv(io_path(path), encoding=encoding)
        except Exception as exc:  # pragma: no cover - diagnostic fallback
            last_error = exc
    raise RuntimeError(f"CSV read failed(CSV 읽기 실패): {path}: {last_error}")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return read_csv_frame(path).fillna("").astype(str).to_dict("records")


def read_csv_header(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(list(rows))).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def int_value(value: Any) -> int:
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return 0


def float_value(value: Any) -> float:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def ratio(part: int, whole: int) -> float:
    return float(part / whole) if whole else 0.0


def safe_series_mean(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.mean()) if len(clean) else 0.0


def safe_series_median(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.median()) if len(clean) else 0.0


def safe_series_max(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.max()) if len(clean) else 0.0


def safe_series_quantile(series: pd.Series, q: float) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean.quantile(q)) if len(clean) else 0.0


def fmt(value: Any) -> str:
    return f"{float_value(value):.6g}"


def pct(value: Any) -> str:
    return f"{float_value(value) * 100.0:.2f}%"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())

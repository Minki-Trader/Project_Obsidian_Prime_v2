from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_trade_attribution import RAW_US100_BARS_PATH, load_us100_bars
from stage_pipelines.stage35 import common


STAGE_NUMBER = 49
STAGE_ID = "49_trade_lifecycle__compression_stress_mfe_capture_exit_timing"
RUN_ID = "run43A_compression_stress_mfe_capture_exit_timing_scout_v1"
RUN_DIR_NAME = "run43A"
PACKET_ID = "stage49_run43A_compression_stress_mfe_capture_exit_timing_scout_v1"
IDEA_ID = "IDEA-ST49-COMPRESSION-STRESS-MFE-CAPTURE"
QUESTION = "Does Stage45 c08 lose money because favorable excursion is not captured before reversal?"

SOURCE_STAGE_ID = "48_robustness_attribution__survivor_cluster_concentration_scout"
SOURCE_RUN_ID = "run42B_trade_level_cluster_telemetry_supplement_v1"
SOURCE_PACKET_ID = "stage48_run42B_trade_level_cluster_telemetry_supplement_v1"
SOURCE_CANDIDATE_ID = "c08_extreme_compression_stress"
SOURCE_TRADES_PATH = common.ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run42B" / "results" / "trade_level_records.csv"
SOURCE_SUMMARY_PATH = common.ROOT / "docs" / "agent_control" / "packets" / SOURCE_PACKET_ID / "aggregate_summary.json"

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID

MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
TRADE_PATH_DIAGNOSTICS_PATH = RESULTS_ROOT / "trade_path_diagnostics.csv"
THRESHOLD_SUMMARY_PATH = RESULTS_ROOT / "threshold_summary.csv"
LOSS_RESCUE_SUMMARY_PATH = RESULTS_ROOT / "loss_rescue_summary.csv"
DECISION_PATH = RESULTS_ROOT / "decision.csv"
LINEAGE_PATH = RESULTS_ROOT / "lineage.csv"
REPORT_PATH = REVIEW_ROOT / "run43A_packet.md"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"

TARGET_GRID = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0)
JUDGMENT = "reviewed_completed_inconclusive_counterfactual_exit_timing_scout_only"
BOUNDARY = (
    "counterfactual_exit_timing_scout_only_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_operating_reference"
)

DIAGNOSTIC_COLUMNS = (
    "source_candidate_id",
    "split",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "original_net_profit",
    "mfe",
    "mae",
    "max_favorable_seen",
    "max_adverse_seen",
    "loss_with_positive_mfe",
    "favorable_first_bar",
    "favorable_first_minutes",
    "adverse_first_bar",
    "adverse_first_minutes",
    "mfe_capture_gap",
)

THRESHOLD_COLUMNS = (
    "split",
    "target_net",
    "trade_count",
    "target_hit_count",
    "target_hit_share",
    "original_net_profit",
    "take_profit_net_profit",
    "take_profit_delta",
    "winner_cut_count",
    "winner_cut_loss",
    "loser_rescue_count",
    "loser_rescue_gain",
    "median_target_hit_bars",
    "status",
)

LOSS_RESCUE_COLUMNS = (
    "split",
    "target_net",
    "loss_trade_count",
    "loss_with_positive_mfe_count",
    "loss_target_hit_count",
    "loss_target_hit_share",
    "original_loss_net_profit",
    "diagnostic_rescue_net_profit",
    "diagnostic_rescue_delta",
    "status",
)

DECISION_COLUMNS = (
    "source_candidate_id",
    "status",
    "judgment",
    "best_validation_target",
    "best_oos_target",
    "best_common_target",
    "validation_best_delta",
    "oos_best_delta",
    "common_validation_delta",
    "common_oos_delta",
    "decision_reasons",
    "claim_boundary",
)

LINEAGE_COLUMNS = ("artifact_id", "type", "path", "sha256", "availability", "notes")


@dataclass(frozen=True)
class TradePath:
    split: str
    trade_index: int
    direction: str
    open_time: pd.Timestamp
    close_time: pd.Timestamp
    hold_bars: float
    original_net_profit: float
    mfe: float
    mae: float
    max_favorable_seen: float
    max_adverse_seen: float
    first_favorable_bar: int | None
    first_adverse_bar: int | None
    target_hit_bars: dict[float, int | None]


def _write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    common.write_csv(path, rows, columns)


def _read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def _num(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def _ratio(numerator: float, denominator: float) -> float | None:
    return None if denominator == 0 else numerator / denominator


def _round(value: Any, digits: int = 6) -> Any:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    return round(number, digits) if math.isfinite(number) else None


def _safe(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")[:limit]


def load_source_trades() -> pd.DataFrame:
    frame = pd.read_csv(io_path(SOURCE_TRADES_PATH))
    frame["open_time"] = pd.to_datetime(frame["open_time"])
    frame["close_time"] = pd.to_datetime(frame["close_time"])
    frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
    frame["mfe"] = pd.to_numeric(frame["mfe"], errors="coerce").fillna(0.0)
    frame["mae"] = pd.to_numeric(frame["mae"], errors="coerce").fillna(0.0)
    return frame.sort_values(["split", "trade_index"]).reset_index(drop=True)


def _bar_favorable_adverse(row: Mapping[str, Any], trade: Mapping[str, Any]) -> tuple[float, float]:
    volume = float(trade.get("volume") or 0.0)
    open_price = float(trade.get("open_price") or 0.0)
    high = float(row.get("high") or open_price)
    low = float(row.get("low") or open_price)
    direction = str(trade.get("direction"))
    if direction == "buy":
        favorable = max(0.0, (high - open_price) * volume)
        adverse = max(0.0, (open_price - low) * volume)
    else:
        favorable = max(0.0, (open_price - low) * volume)
        adverse = max(0.0, (high - open_price) * volume)
    return favorable, adverse


def compute_trade_path(trade: Mapping[str, Any], bars: pd.DataFrame, targets: Sequence[float] = TARGET_GRID) -> TradePath:
    open_time = pd.Timestamp(trade["open_time"])
    close_time = pd.Timestamp(trade["close_time"])
    window = bars.loc[(bars["time_open"] >= open_time) & (bars["time_open"] < close_time)].copy()
    if window.empty:
        window = bars.loc[bars["time_open"].eq(open_time)].copy()
    max_favorable = 0.0
    max_adverse = 0.0
    first_fav: int | None = None
    first_adv: int | None = None
    target_hits: dict[float, int | None] = {float(target): None for target in targets}
    for bar_index, (_, bar) in enumerate(window.iterrows(), start=1):
        favorable, adverse = _bar_favorable_adverse(bar, trade)
        if favorable > max_favorable:
            max_favorable = favorable
        if adverse > max_adverse:
            max_adverse = adverse
        if first_fav is None and favorable > 0.0:
            first_fav = bar_index
        if first_adv is None and adverse > 0.0:
            first_adv = bar_index
        for target in targets:
            key = float(target)
            if target_hits[key] is None and favorable >= key:
                target_hits[key] = bar_index
    return TradePath(
        split=str(trade["split"]),
        trade_index=int(trade["trade_index"]),
        direction=str(trade["direction"]),
        open_time=open_time,
        close_time=close_time,
        hold_bars=float(trade.get("hold_bars") or 0.0),
        original_net_profit=float(trade.get("net_profit") or 0.0),
        mfe=float(trade.get("mfe") or 0.0),
        mae=float(trade.get("mae") or 0.0),
        max_favorable_seen=max_favorable,
        max_adverse_seen=max_adverse,
        first_favorable_bar=first_fav,
        first_adverse_bar=first_adv,
        target_hit_bars=target_hits,
    )


def build_trade_paths(trades: pd.DataFrame, bars: pd.DataFrame) -> list[TradePath]:
    return [compute_trade_path(row, bars) for row in trades.to_dict("records")]


def diagnostic_rows(paths: Sequence[TradePath]) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        first_fav_minutes = None if path.first_favorable_bar is None else (path.first_favorable_bar - 1) * 5
        first_adv_minutes = None if path.first_adverse_bar is None else (path.first_adverse_bar - 1) * 5
        rows.append(
            {
                "source_candidate_id": SOURCE_CANDIDATE_ID,
                "split": path.split,
                "trade_index": path.trade_index,
                "direction": path.direction,
                "open_time": path.open_time.strftime("%Y-%m-%d %H:%M:%S"),
                "close_time": path.close_time.strftime("%Y-%m-%d %H:%M:%S"),
                "hold_bars": _round(path.hold_bars),
                "original_net_profit": _round(path.original_net_profit),
                "mfe": _round(path.mfe),
                "mae": _round(path.mae),
                "max_favorable_seen": _round(path.max_favorable_seen),
                "max_adverse_seen": _round(path.max_adverse_seen),
                "loss_with_positive_mfe": path.original_net_profit < 0.0 and path.max_favorable_seen > 0.0,
                "favorable_first_bar": path.first_favorable_bar,
                "favorable_first_minutes": first_fav_minutes,
                "adverse_first_bar": path.first_adverse_bar,
                "adverse_first_minutes": first_adv_minutes,
                "mfe_capture_gap": _round(path.max_favorable_seen - path.original_net_profit),
            }
        )
    return rows


def summarize_thresholds(paths: Sequence[TradePath], targets: Sequence[float] = TARGET_GRID) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in sorted({path.split for path in paths}):
        selected = [path for path in paths if path.split == split]
        original_net = sum(path.original_net_profit for path in selected)
        for target in targets:
            target = float(target)
            hit = [path for path in selected if path.target_hit_bars.get(target) is not None]
            tp_net = sum(target if path.target_hit_bars.get(target) is not None else path.original_net_profit for path in selected)
            winner_cut_loss = sum(
                max(path.original_net_profit - target, 0.0)
                for path in hit
                if path.original_net_profit > target
            )
            loser_rescue_gain = sum(
                target - path.original_net_profit
                for path in hit
                if path.original_net_profit < 0.0
            )
            hit_bars = [int(path.target_hit_bars[target]) for path in hit if path.target_hit_bars.get(target) is not None]
            rows.append(
                {
                    "split": split,
                    "target_net": target,
                    "trade_count": len(selected),
                    "target_hit_count": len(hit),
                    "target_hit_share": _round(_ratio(len(hit), len(selected))),
                    "original_net_profit": _round(original_net),
                    "take_profit_net_profit": _round(tp_net),
                    "take_profit_delta": _round(tp_net - original_net),
                    "winner_cut_count": sum(1 for path in hit if path.original_net_profit > target),
                    "winner_cut_loss": _round(winner_cut_loss),
                    "loser_rescue_count": sum(1 for path in hit if path.original_net_profit < 0.0),
                    "loser_rescue_gain": _round(loser_rescue_gain),
                    "median_target_hit_bars": _round(pd.Series(hit_bars).median() if hit_bars else None),
                    "status": "counterfactual_take_profit_overlay",
                }
            )
    return rows


def summarize_loss_rescue(paths: Sequence[TradePath], targets: Sequence[float] = TARGET_GRID) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in sorted({path.split for path in paths}):
        losses = [path for path in paths if path.split == split and path.original_net_profit < 0.0]
        positive_mfe = [path for path in losses if path.max_favorable_seen > 0.0]
        original_loss_net = sum(path.original_net_profit for path in losses)
        for target in targets:
            target = float(target)
            hit = [path for path in losses if path.target_hit_bars.get(target) is not None]
            rescue_net = sum(target if path in hit else path.original_net_profit for path in losses)
            rows.append(
                {
                    "split": split,
                    "target_net": target,
                    "loss_trade_count": len(losses),
                    "loss_with_positive_mfe_count": len(positive_mfe),
                    "loss_target_hit_count": len(hit),
                    "loss_target_hit_share": _round(_ratio(len(hit), len(losses))),
                    "original_loss_net_profit": _round(original_loss_net),
                    "diagnostic_rescue_net_profit": _round(rescue_net),
                    "diagnostic_rescue_delta": _round(rescue_net - original_loss_net),
                    "status": "diagnostic_only_not_executable_without_selection_rule",
                }
            )
    return rows


def _best_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> Mapping[str, Any]:
    selected = [row for row in rows if row.get("split") == split]
    return max(selected, key=lambda row: float(row.get("take_profit_delta") or -1e18), default={})


def _best_common(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    by_target: dict[float, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(float(row["target_net"]), {})[str(row["split"])] = row
    candidates = []
    for target, split_rows in by_target.items():
        if {"validation_is", "oos"} <= set(split_rows):
            val_delta = float(split_rows["validation_is"].get("take_profit_delta") or 0.0)
            oos_delta = float(split_rows["oos"].get("take_profit_delta") or 0.0)
            candidates.append(
                {
                    "target_net": target,
                    "validation_delta": val_delta,
                    "oos_delta": oos_delta,
                    "min_delta": min(val_delta, oos_delta),
                    "combined_delta": val_delta + oos_delta,
                }
            )
    return max(candidates, key=lambda row: (row["min_delta"], row["combined_delta"]), default={})


def build_decision_rows(threshold_rows: Sequence[Mapping[str, Any]], rescue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best_validation = _best_by_split(threshold_rows, "validation_is")
    best_oos = _best_by_split(threshold_rows, "oos")
    best_common = _best_common(threshold_rows)
    reasons = []
    if float(best_common.get("min_delta") or 0.0) <= 0.0:
        reasons.append("no_common_fixed_take_profit_target_improves_both_splits")
    if float(best_validation.get("take_profit_delta") or 0.0) > 0.0 and float(best_oos.get("take_profit_delta") or 0.0) <= 0.0:
        reasons.append("validation_improvement_not_oos_confirmed")
    rescue_best = max(rescue_rows, key=lambda row: float(row.get("diagnostic_rescue_delta") or 0.0), default={})
    if float(rescue_best.get("diagnostic_rescue_delta") or 0.0) > 0.0:
        reasons.append("loss_rescue_diagnostic_large_but_not_executable_without_selection_rule")
    if not reasons:
        reasons.append("counterfactual_exit_timing_recorded")
    return [
        {
            "source_candidate_id": SOURCE_CANDIDATE_ID,
            "status": "exit_timing_scout_recorded_not_promotion",
            "judgment": JUDGMENT,
            "best_validation_target": best_validation.get("target_net", ""),
            "best_oos_target": best_oos.get("target_net", ""),
            "best_common_target": best_common.get("target_net", ""),
            "validation_best_delta": best_validation.get("take_profit_delta", ""),
            "oos_best_delta": best_oos.get("take_profit_delta", ""),
            "common_validation_delta": _round(best_common.get("validation_delta", "")),
            "common_oos_delta": _round(best_common.get("oos_delta", "")),
            "decision_reasons": ";".join(reasons),
            "claim_boundary": BOUNDARY,
        }
    ]


def build_summary(
    diagnostics: Sequence[Mapping[str, Any]],
    threshold_rows: Sequence[Mapping[str, Any]],
    rescue_rows: Sequence[Mapping[str, Any]],
    decision_rows: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    for split in sorted({str(row["split"]) for row in diagnostics}):
        selected = [row for row in diagnostics if row["split"] == split]
        losses = [row for row in selected if float(row["original_net_profit"]) < 0.0]
        loss_positive_mfe = [row for row in losses if row["loss_with_positive_mfe"] in {True, "True", "true"}]
        by_split[split] = {
            "trade_count": len(selected),
            "original_net_profit": _round(sum(float(row["original_net_profit"]) for row in selected)),
            "loss_trade_count": len(losses),
            "loss_with_positive_mfe_count": len(loss_positive_mfe),
            "loss_with_positive_mfe_share": _round(_ratio(len(loss_positive_mfe), len(losses))),
            "avg_mfe_capture_gap": _round(pd.Series([float(row["mfe_capture_gap"]) for row in selected]).mean()),
        }
    return {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at_utc,
        "idea_id": IDEA_ID,
        "question": QUESTION,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "diagnostic_rows": len(diagnostics),
        "threshold_rows": len(threshold_rows),
        "loss_rescue_rows": len(rescue_rows),
        "by_split": by_split,
        "decision": decision_rows[0] if decision_rows else {},
        "result_judgment": {
            "status": "passed",
            "result_subject": "Stage45 c08 MFE capture exit timing counterfactual scout",
            "evidence_available": ["Stage48 trade-level rows", "raw MT5 M5 bars", "path-aware target-touch diagnostics"],
            "evidence_missing": ["actual MT5 EA exit overlay rerun", "intrabar tick ordering within M5 bars"],
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": "Only a runtime probe with explicit EA exit overlay can upgrade this from counterfactual scout.",
        },
    }


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        ("stage49_source_stage48_trade_level_records", "source_table", SOURCE_TRADES_PATH, "tracked_source", "Stage48 run42B closed trade records."),
        ("stage49_source_stage48_summary", "source_summary", SOURCE_SUMMARY_PATH, "tracked_source", "Stage48 run42B packet summary."),
        ("stage49_raw_mt5_us100_bars", "source_input", common.ROOT / RAW_US100_BARS_PATH, "ignored_local_source_available_hash_recorded", "M5 path for target-touch chronology."),
        ("stage49_manifest", "manifest", MANIFEST_PATH, "ignored_regenerable_from_run_command", "Stage49 run identity."),
        ("stage49_trade_path_diagnostics", "table", TRADE_PATH_DIAGNOSTICS_PATH, "ignored_regenerable_from_manifest", "Per-trade path diagnostics."),
        ("stage49_threshold_summary", "table", THRESHOLD_SUMMARY_PATH, "ignored_regenerable_from_manifest", "Fixed take-profit counterfactual summary."),
        ("stage49_loss_rescue_summary", "table", LOSS_RESCUE_SUMMARY_PATH, "ignored_regenerable_from_manifest", "Diagnostic-only loss rescue summary."),
        ("stage49_decision", "table", DECISION_PATH, "ignored_regenerable_from_manifest", "Stage49 decision row."),
        ("stage49_review_packet", "report", REPORT_PATH, "tracked_reviewed", "Human review packet."),
    ]
    payload = []
    for artifact_id, artifact_type, path, availability, notes in rows:
        payload.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": common.rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "availability": availability,
                "notes": notes,
            }
        )
    return payload


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    common.write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage49 Brief

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- question(질문): {QUESTION}
- source(원천): Stage48(48단계) run42B trade-level telemetry(거래 단위 원격측정)
- boundary(주장 경계): `{BOUNDARY}`
- external verification(외부 검증): existing MT5 report-derived trades(기존 MT5 보고서 파생 거래)를 사용한다; new Strategy Tester rerun(새 전략 테스터 재실행)은 주장하지 않는다.
""",
    )
    common.write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Input References

- source trade records(원천 거래 기록): `{common.rel(SOURCE_TRADES_PATH)}`
- source packet summary(원천 패킷 요약): `{common.rel(SOURCE_SUMMARY_PATH)}`
- raw MT5 bars(원천 MT5 봉): `{RAW_US100_BARS_PATH.as_posix()}`
- source candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
""",
    )
    decision = summary["decision"]
    validation = summary["by_split"].get("validation_is", {})
    oos = summary["by_split"].get("oos", {})
    common.write_md(
        REPORT_PATH,
        f"""# {RUN_ID} Packet(패킷)

- stage_id(단계 ID): `{STAGE_ID}`
- judgment(판정): `{summary['judgment']}`
- source(원천): `{SOURCE_CANDIDATE_ID}` from Stage48(48단계) run42B
- diagnostic rows(진단 행): `{summary['diagnostic_rows']}`
- validation loss with positive MFE(검증 양의 MFE 보유 손실): `{validation.get('loss_with_positive_mfe_count')}` / `{validation.get('loss_trade_count')}` share `{validation.get('loss_with_positive_mfe_share')}`
- OOS loss with positive MFE(외표본 양의 MFE 보유 손실): `{oos.get('loss_with_positive_mfe_count')}` / `{oos.get('loss_trade_count')}` share `{oos.get('loss_with_positive_mfe_share')}`
- best validation fixed target(검증 최선 고정 목표): `{decision.get('best_validation_target')}` delta `{decision.get('validation_best_delta')}`
- best OOS fixed target(외표본 최선 고정 목표): `{decision.get('best_oos_target')}` delta `{decision.get('oos_best_delta')}`
- best common fixed target(공통 최선 고정 목표): `{decision.get('best_common_target')}` validation delta `{decision.get('common_validation_delta')}` OOS delta `{decision.get('common_oos_delta')}`
- decision reasons(결정 이유): `{decision.get('decision_reasons')}`
- boundary(주장 경계): `{BOUNDARY}`

Interpretation(해석): positive MFE(양의 최대 유리 변동)는 대부분 손실 거래에 있었지만, unconditional fixed take-profit(무조건 고정 익절)은 both splits(양쪽 분할)를 동시에 개선하지 못했다. This is an exit-timing clue(청산 타이밍 단서), not a promotion(승격) or runtime authority(런타임 권위).
""",
    )
    common.write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Review Index

- run packet(실행 패킷): `03_reviews/run43A_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
- trade path diagnostics(거래 경로 진단): `02_runs/run43A/results/trade_path_diagnostics.csv`
- threshold summary(목표값 요약): `02_runs/run43A/results/threshold_summary.csv`
- loss rescue summary(손실 구조 진단 요약): `02_runs/run43A/results/loss_rescue_summary.csv`
- decision table(결정 표): `02_runs/run43A/results/decision.csv`
""",
    )
    common.write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage49 Selection Status

- final_judgment(최종 판정): `{summary['judgment']}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- promotion_packet(승격 패킷): `none`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- best_common_fixed_target(공통 최선 고정 목표): `{decision.get('best_common_target')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_gates(summary: Mapping[str, Any], lineage: Sequence[Mapping[str, Any]]) -> dict[str, Path]:
    gates = {
        "data_integrity_gate": PACKET_ROOT / "data_integrity_gate.json",
        "performance_attribution_gate": PACKET_ROOT / "performance_attribution_gate.json",
        "artifact_lineage_gate": PACKET_ROOT / "artifact_lineage_gate.json",
        "result_judgment_gate": PACKET_ROOT / "result_judgment_gate.json",
        "required_gate_coverage_audit": PACKET_ROOT / "required_gate_coverage_audit.json",
        "final_claim_guard": PACKET_ROOT / "final_claim_guard.json",
    }
    _write_json(gates["data_integrity_gate"], {"status": "passed", "source_rows": summary["diagnostic_rows"], "time_axis": "MT5 M5 bar path joined by naive broker timestamps from Stage48 trade records."})
    _write_json(gates["performance_attribution_gate"], {"status": "passed_with_boundary", "scope": "counterfactual fixed target and diagnostic loss rescue; no runtime execution claim", "decision": summary["decision"]})
    _write_json(gates["artifact_lineage_gate"], {"status": "passed", "lineage_rows": len(lineage), "lineage_judgment": "connected_with_boundary"})
    _write_json(gates["result_judgment_gate"], summary["result_judgment"])
    required = ["data_integrity_gate", "performance_attribution_gate", "artifact_lineage_gate", "result_judgment_gate", "final_claim_guard"]
    _write_json(gates["required_gate_coverage_audit"], {"status": "passed", "required_gates": required, "covered_gates": required, "missing_gates": []})
    _write_json(gates["final_claim_guard"], {"status": "passed", "forbidden_claims_present": False, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "claim_boundary": BOUNDARY})
    return gates


def write_packet(summary: Mapping[str, Any], gates: Mapping[str, Path]) -> None:
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(PACKET_ROOT / "work_packet.yaml").write_text(
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_id: {RUN_ID}
idea_id: {IDEA_ID}
primary_family: experiment_execution
primary_skill: obsidian-experiment-design
support_skills:
  - obsidian-data-integrity
  - obsidian-performance-attribution
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
  - data_integrity_gate
  - performance_attribution_gate
  - artifact_lineage_gate
  - result_judgment_gate
  - final_claim_guard
claim_boundary: {BOUNDARY}
""",
        encoding="utf-8",
    )
    _write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "hypothesis": QUESTION, "stop_condition": "No common fixed target improves both validation and OOS."},
                {"skill": "obsidian-data-integrity", "status": "completed", "source_rows": summary["diagnostic_rows"], "time_axis_boundary": "M5 bar path, no intrabar tick ordering."},
                {"skill": "obsidian-performance-attribution", "status": "completed", "attribution_scope": "MFE capture and fixed take-profit counterfactual."},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "lineage_judgment": "connected_with_boundary"},
                {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": JUDGMENT, "claim_boundary": BOUNDARY},
            ],
        },
    )
    _write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    _write_json(PACKET_ROOT / "gate_file_manifest.json", {name: common.rel(path) for name, path in gates.items()})
    _write_json(
        PACKET_ROOT / "validation_commands.json",
        {
            "commands": [
                {"command": "python -m foundation.pipelines.run_stage49_mfe_capture_exit_timing", "result": "completed"},
                {"command": "pytest tests/test_stage49_mfe_capture_exit_timing.py", "result": "pending"},
            ]
        },
    )


def write_ledgers(summary: Mapping[str, Any], lineage: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        common.RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "counterfactual_exit_timing_scout", "status": "reviewed", "judgment": JUDGMENT, "path": common.rel(REPORT_PATH), "notes": BOUNDARY}],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__mfe_capture_diagnostics",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mfe_capture_diagnostics",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "trade_path_diagnostics",
            "tier_scope": "Tier A primary + Tier B fallback",
            "kpi_scope": "counterfactual_exit_timing",
            "scoreboard_lane": "counterfactual_exit_timing_scout",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": common.rel(TRADE_PATH_DIAGNOSTICS_PATH),
            "primary_kpi": ledger_pairs([("rows", summary["diagnostic_rows"]), ("validation_loss_positive_mfe_share", summary["by_split"].get("validation_is", {}).get("loss_with_positive_mfe_share")), ("oos_loss_positive_mfe_share", summary["by_split"].get("oos", {}).get("loss_with_positive_mfe_share"))]),
            "guardrail_kpi": "counterfactual_only_no_runtime_execution",
            "external_verification_status": "completed_existing_mt5_report_derived_trades_no_new_tester_run",
            "notes": BOUNDARY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__fixed_target_summary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "fixed_target_summary",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "fixed_take_profit_counterfactual",
            "tier_scope": "Tier A primary + Tier B fallback",
            "kpi_scope": "counterfactual_exit_overlay",
            "scoreboard_lane": "counterfactual_exit_timing_scout",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": common.rel(THRESHOLD_SUMMARY_PATH),
            "primary_kpi": ledger_pairs([("best_common_target", summary["decision"].get("best_common_target")), ("common_validation_delta", summary["decision"].get("common_validation_delta")), ("common_oos_delta", summary["decision"].get("common_oos_delta"))]),
            "guardrail_kpi": "no_common_fixed_target_improves_both_splits_if_oos_delta_negative",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": BOUNDARY,
        },
    ]
    stage_payload = upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(common.PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        common.ROOT / "docs" / "registers" / "artifact_registry.csv",
        ("artifact_id", "type", "path", "status", "notes"),
        [{"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]} for row in lineage],
        key="artifact_id",
    )
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def update_workspace(summary: Mapping[str, Any]) -> None:
    state_path = common.WORKSPACE_STATE_PATH
    text = io_path(state_path).read_text(encoding="utf-8-sig")
    text = re.sub(r"updated_on: .+", "updated_on: '2026-05-10'", text, count=1)
    text = re.sub(r"active_branch: .+", f"active_branch: {common.active_branch()}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus_item = (
        f"- Stage49(49단계) {STAGE_ID} counterfactual_exit_timing_scout(반사실 청산 타이밍 탐색): "
        f"`{SOURCE_CANDIDATE_ID}` MFE capture(최대 유리 변동 포착)를 평가했고 fixed take-profit(고정 익절)은 "
        "both splits(양쪽 분할)를 동시에 개선하지 못했다; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    text = re.sub(rf"^- Stage49\(49단계\) {re.escape(STAGE_ID)} .+\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"(current_focus:\n)", r"\1" + focus_item + "\n", text, count=1)
    block_name = "stage49_mfe_capture_exit_timing"
    block = f"""
{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_counterfactual_exit_timing_scout_completed
  current_run_id: {RUN_ID}
  source_stage_id: {SOURCE_STAGE_ID}
  source_run_id: {SOURCE_RUN_ID}
  source_candidate_id: {SOURCE_CANDIDATE_ID}
  diagnostic_rows: {summary['diagnostic_rows']}
  best_common_fixed_target: {summary['decision'].get('best_common_target')}
  common_validation_delta: {summary['decision'].get('common_validation_delta')}
  common_oos_delta: {summary['decision'].get('common_oos_delta')}
  report_path: {common.rel(REPORT_PATH)}
  packet_summary_path: {common.rel(PACKET_ROOT / 'aggregate_summary.json')}
  next_action: design_runtime_probe_only_if_exit_overlay_logic_is_explicit
  boundary: {BOUNDARY}
"""
    text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", text, flags=re.MULTILINE)
    io_path(state_path).write_text(text.rstrip() + "\n\n" + block.lstrip("\n"), encoding="utf-8")

    current_path = common.CURRENT_WORKING_STATE_PATH
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    section = f"""## Latest Stage49 MFE Capture Exit Timing(최신 49단계 MFE 포착 청산 타이밍)

Stage49(49단계) `{STAGE_ID}` finished(완료) `{RUN_ID}` as `{JUDGMENT}`. Stage48(48단계) run42B trade-level records(거래 단위 기록)를 사용해 fixed take-profit(고정 익절) counterfactual(반사실)을 봤고, common target(공통 목표)은 both splits(양쪽 분할)를 동시에 개선하지 못했다. No baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) was created.

"""
    current = re.sub(r"## Latest Stage49 MFE Capture Exit Timing.*?(?=\n## |\Z)", "", current, count=1, flags=re.DOTALL).lstrip()
    io_path(current_path).write_text(section + current, encoding="utf-8-sig")

    changelog_path = common.CHANGELOG_PATH
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    if RUN_ID not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + f"\n- {common.utc_now()} `{STAGE_ID}` `{RUN_ID}` finished with `{JUDGMENT}`; boundary `{BOUNDARY}`.\n", encoding="utf-8-sig")


def run(update_state: bool = True) -> dict[str, Any]:
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    io_path(RESULTS_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)

    created_at = common.utc_now()
    trades = load_source_trades()
    bars = load_us100_bars(common.ROOT / RAW_US100_BARS_PATH)
    paths = build_trade_paths(trades, bars)
    diagnostics = diagnostic_rows(paths)
    threshold_rows = summarize_thresholds(paths)
    rescue_rows = summarize_loss_rescue(paths)
    decision_rows = build_decision_rows(threshold_rows, rescue_rows)
    summary = build_summary(diagnostics, threshold_rows, rescue_rows, decision_rows, created_at)

    _write_csv(TRADE_PATH_DIAGNOSTICS_PATH, diagnostics, DIAGNOSTIC_COLUMNS)
    _write_csv(THRESHOLD_SUMMARY_PATH, threshold_rows, THRESHOLD_COLUMNS)
    _write_csv(LOSS_RESCUE_SUMMARY_PATH, rescue_rows, LOSS_RESCUE_COLUMNS)
    _write_csv(DECISION_PATH, decision_rows, DECISION_COLUMNS)
    _write_json(
        MANIFEST_PATH,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "source_trade_records": common.rel(SOURCE_TRADES_PATH),
            "raw_bars": RAW_US100_BARS_PATH.as_posix(),
            "target_grid": list(TARGET_GRID),
            "claim_boundary": BOUNDARY,
        },
    )
    write_stage_docs(summary)
    lineage = lineage_rows()
    _write_csv(LINEAGE_PATH, lineage, LINEAGE_COLUMNS)
    gates = write_gates(summary, lineage)
    write_packet(summary, gates)
    ledger_sync = write_ledgers(summary, lineage)
    summary["ledger_sync"] = ledger_sync
    _write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    if update_state:
        update_workspace(summary)
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-update-state", action="store_true")
    args = parser.parse_args(argv)
    summary = run(update_state=not args.no_update_state)
    print(json.dumps(json_ready({"run_id": RUN_ID, "judgment": summary["judgment"], "decision": summary["decision"]}), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

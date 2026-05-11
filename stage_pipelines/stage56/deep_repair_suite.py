from __future__ import annotations

import argparse
import csv
import json
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.alpha import scout_runner as alpha_scout_runner  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.mt5.runtime_artifacts import write_json  # noqa: E402
from stage_pipelines.stage10 import logreg_mt5_scout as logreg_scout  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE_NUMBER = 56
RUN_NUMBER = "run50D"
PARENT_RUN_ID = "run50D_stage56_deep_repair_suite_v1"
PACKET_ID = "stage56_run50D_deep_repair_suite_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__DeepDenseRepair"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
REPORT_PATH = REVIEWS_ROOT / "run50D_deep_repair_suite.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50D_deep_repair_suite_summary.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0

D38H10_REFERENCE = {
    "variant_id": "run50C_d38h10",
    "routed_validation_trades_per_day": 4.464481,
    "routed_oos_trades_per_day": 3.446154,
    "routed_validation_profit_factor": 1.07,
    "routed_oos_profit_factor": 1.13,
    "routed_validation_net_profit": 190.38,
    "routed_oos_net_profit": 302.10,
    "routed_oos_drawdown": 179.28,
}


@dataclass(frozen=True)
class RepairVariant:
    variant_id: str
    group: str
    tier_a_short_threshold: float
    tier_a_long_threshold: float
    tier_a_min_margin: float
    tier_b_short_threshold: float
    tier_b_long_threshold: float
    tier_b_min_margin: float
    max_hold_bars: int
    session_slice_id: str | None = None
    tier_b_allowed_subtypes: tuple[str, ...] = ()
    notes: str = ""

    @property
    def run_id(self) -> str:
        return f"{RUN_NUMBER}_{self.variant_id}_logreg_deep_v1"

    @staticmethod
    def _threshold_id(prefix: str, short_threshold: float, long_threshold: float, min_margin: float) -> str:
        short_bp = int(round(short_threshold * 1000))
        long_bp = int(round(long_threshold * 1000))
        margin_bp = int(round(min_margin * 1000))
        return f"{prefix}s{short_bp:03d}_l{long_bp:03d}_m{margin_bp:03d}"

    @property
    def tier_a_threshold_id(self) -> str:
        return self._threshold_id(
            f"stage56_{self.variant_id}_a_",
            self.tier_a_short_threshold,
            self.tier_a_long_threshold,
            self.tier_a_min_margin,
        )

    @property
    def tier_b_threshold_id(self) -> str:
        return self._threshold_id(
            f"stage56_{self.variant_id}_b_",
            self.tier_b_short_threshold,
            self.tier_b_long_threshold,
            self.tier_b_min_margin,
        )


DEFAULT_VARIANTS: tuple[RepairVariant, ...] = (
    RepairVariant("d370h10", "dense", 0.370, 0.370, 0.0, 0.370, 0.370, 0.0, 10, notes="lower threshold density pressure"),
    RepairVariant("d375h10", "dense", 0.375, 0.375, 0.0, 0.375, 0.375, 0.0, 10, notes="between d37h09 and d38h10"),
    RepairVariant("d375h11", "dense", 0.375, 0.375, 0.0, 0.375, 0.375, 0.0, 11, notes="density plus longer hold"),
    RepairVariant("d380h09", "dense", 0.380, 0.380, 0.0, 0.380, 0.380, 0.0, 9, notes="d38 shorter hold"),
    RepairVariant("d385h10", "dense", 0.385, 0.385, 0.0, 0.385, 0.385, 0.0, 10, notes="quality pressure around d38h10"),
    RepairVariant("d385h11", "dense", 0.385, 0.385, 0.0, 0.385, 0.385, 0.0, 11, notes="quality pressure plus longer hold"),
    RepairVariant("d390h10", "dense", 0.390, 0.390, 0.0, 0.390, 0.390, 0.0, 10, notes="upper bracket quality pressure"),
    RepairVariant("d38long37short39h10", "balance", 0.390, 0.370, 0.0, 0.390, 0.370, 0.0, 10, notes="long-friendly balance probe"),
    RepairVariant("d38short37long39h10", "balance", 0.370, 0.390, 0.0, 0.370, 0.390, 0.0, 10, notes="short-friendly balance probe"),
    RepairVariant("d38m005h10", "balance", 0.380, 0.380, 0.005, 0.380, 0.380, 0.005, 10, notes="probability margin filter"),
    RepairVariant("d38h10_b040", "fallback", 0.380, 0.380, 0.0, 0.400, 0.400, 0.0, 10, notes="stricter Tier B fallback"),
    RepairVariant("d38h10_b042", "fallback", 0.380, 0.380, 0.0, 0.420, 0.420, 0.0, 10, notes="strict Tier B fallback"),
    RepairVariant(
        "d38h10_bmacro",
        "fallback",
        0.380,
        0.380,
        0.0,
        0.400,
        0.400,
        0.0,
        10,
        tier_b_allowed_subtypes=("B_macro_missing",),
        notes="Tier B macro-missing permission only",
    ),
    RepairVariant(
        "d38h10_bmixed",
        "fallback",
        0.380,
        0.380,
        0.0,
        0.400,
        0.400,
        0.0,
        10,
        tier_b_allowed_subtypes=("B_mixed_partial_context",),
        notes="Tier B mixed partial-context permission only",
    ),
    RepairVariant(
        "d38h10_bcoremixed",
        "fallback",
        0.380,
        0.380,
        0.0,
        0.400,
        0.400,
        0.0,
        10,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes="Tier B core or mixed permission",
    ),
    RepairVariant("d38h10_early", "session", 0.380, 0.380, 0.0, 0.380, 0.380, 0.0, 10, session_slice_id="early", notes="early cash-session slice"),
    RepairVariant("d38h10_mid", "session", 0.380, 0.380, 0.0, 0.380, 0.380, 0.0, 10, session_slice_id="mid", notes="mid cash-session slice"),
    RepairVariant("d38h10_late", "session", 0.380, 0.380, 0.0, 0.380, 0.380, 0.0, 10, session_slice_id="late", notes="late cash-session slice"),
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _configure_stage56_identity(variant: RepairVariant, run_output_root: Path) -> None:
    common_run_root = f"Project_Obsidian_Prime_v2/stage56/{PARENT_RUN_ID}/{variant.variant_id}"
    logreg_scout.STAGE_ID = STAGE_ID
    logreg_scout.RUN_NUMBER = RUN_NUMBER
    logreg_scout.RUN_ID = variant.run_id
    logreg_scout.EXPLORATION_LABEL = f"{EXPLORATION_LABEL}__{variant.variant_id}"
    logreg_scout.DEFAULT_RUN_OUTPUT_ROOT = run_output_root
    logreg_scout.STAGE_RUN_LEDGER_PATH = STAGE_RUN_LEDGER_PATH
    logreg_scout.COMMON_RUN_ROOT = common_run_root
    alpha_scout_runner.configure_run_identity(
        run_number=RUN_NUMBER,
        run_id=variant.run_id,
        exploration_label=logreg_scout.EXPLORATION_LABEL,
        common_run_root=common_run_root,
        stage_id=STAGE_ID,
    )

    def build_stage56_context(
        *,
        run_output_root: Path,
        common_files_root: Path,
        terminal_data_root: Path,
        tester_profile_root: Path,
    ) -> alpha_scout_runner.ScoutRunContext:
        return alpha_scout_runner.build_run_context(
            stage_id=STAGE_ID,
            stage_number=STAGE_NUMBER,
            run_number=RUN_NUMBER,
            run_id=variant.run_id,
            exploration_label=logreg_scout.EXPLORATION_LABEL,
            output_root=run_output_root,
            common_run_root=common_run_root,
            common_files_root=common_files_root,
            terminal_data_root=terminal_data_root,
            tester_profile_root=tester_profile_root,
        )

    logreg_scout.build_scout_context = build_stage56_context


def _run_variant(
    variant: RepairVariant,
    *,
    attempt_mt5: bool,
    routed_fallback_enabled: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    force: bool,
) -> dict[str, Any]:
    run_output_root = RUN_ROOT / variant.variant_id
    summary_path = run_output_root / "summary.json"
    if summary_path.exists() and not force:
        return {
            "status": "skipped_existing",
            "variant_id": variant.variant_id,
            "run_id": variant.run_id,
            "summary_path": summary_path.as_posix(),
            "external_verification_status": _read_json(summary_path).get("external_verification_status"),
        }

    _configure_stage56_identity(variant, run_output_root)
    tier_a_rule = logreg_scout.threshold_rule_from_values(
        threshold_id=variant.tier_a_threshold_id,
        short_threshold=variant.tier_a_short_threshold,
        long_threshold=variant.tier_a_long_threshold,
        min_margin=variant.tier_a_min_margin,
    )
    tier_b_rule = logreg_scout.threshold_rule_from_values(
        threshold_id=variant.tier_b_threshold_id,
        short_threshold=variant.tier_b_short_threshold,
        long_threshold=variant.tier_b_long_threshold,
        min_margin=variant.tier_b_min_margin,
    )
    return logreg_scout.run_stage10_logreg_mt5_scout(
        model_input_path=logreg_scout.DEFAULT_MODEL_INPUT_PATH,
        feature_order_path=logreg_scout.DEFAULT_FEATURE_ORDER_PATH,
        tier_b_model_input_path=logreg_scout.DEFAULT_TIER_B_MODEL_INPUT_PATH,
        tier_b_feature_order_path=logreg_scout.DEFAULT_TIER_B_FEATURE_ORDER_PATH,
        raw_root=logreg_scout.DEFAULT_RAW_ROOT,
        training_summary_path=logreg_scout.DEFAULT_TRAINING_SUMMARY_PATH,
        stage07_model_path=logreg_scout.DEFAULT_STAGE07_MODEL_PATH,
        run_output_root=run_output_root,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        max_hold_bars=variant.max_hold_bars,
        tier_a_threshold_rule=tier_a_rule,
        tier_b_threshold_rule=tier_b_rule,
        routed_fallback_enabled=routed_fallback_enabled,
        session_slice_id=variant.session_slice_id,
        tier_b_fallback_allowed_subtypes=variant.tier_b_allowed_subtypes or None,
        attempt_mt5=attempt_mt5,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
    )


def _record_by_view(summary: Mapping[str, Any], record_view: str) -> Mapping[str, Any]:
    for record in summary.get("mt5_kpi_records", []):
        if str(record.get("record_view")) == record_view:
            return record
    return {}


def _metric(summary: Mapping[str, Any], record_view: str, metric: str) -> Any:
    record = _record_by_view(summary, record_view)
    metrics = record.get("metrics", {}) if isinstance(record, Mapping) else {}
    return metrics.get(metric) if isinstance(metrics, Mapping) else None


def _per_day(trades: Any, days: float) -> float | None:
    if trades is None:
        return None
    try:
        return float(trades) / days
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _compact(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (tuple, list)):
        return ";".join(str(item) for item in value)
    return str(value)


def _runtime_judgment(row: Mapping[str, Any]) -> str:
    if row.get("external_verification_status") != "completed":
        return "blocked_or_unverified_no_actual_mt5_closed_trade_basis"
    validation_net = _float(row.get("routed_validation_net_profit"))
    oos_net = _float(row.get("routed_oos_net_profit"))
    validation_pf = _float(row.get("routed_validation_profit_factor"))
    oos_pf = _float(row.get("routed_oos_profit_factor"))
    validation_density = _float(row.get("routed_validation_trades_per_day"))
    oos_density = _float(row.get("routed_oos_trades_per_day"))
    density_floor = min(validation_density, oos_density)
    pf_floor = min(validation_pf, oos_pf)
    if validation_net <= 0.0 or oos_net <= 0.0:
        return "quality_failed_actual_routed_mt5"
    if density_floor >= 5.0 and pf_floor >= 1.10:
        return "strong_selected_research_baseline_candidate_actual_routed_mt5"
    if density_floor >= 5.0 and pf_floor >= 1.05:
        return "selected_research_baseline_candidate_actual_routed_mt5"
    if density_floor >= 3.0 and pf_floor >= 1.05:
        return "weak_dense_engine_candidate_actual_routed_mt5"
    if density_floor < 3.0:
        return "density_failed_actual_routed_mt5"
    return "quality_or_density_inconclusive_actual_routed_mt5"


def _summary_rows(results: Sequence[Mapping[str, Any]], variants: Sequence[RepairVariant]) -> list[dict[str, Any]]:
    variant_by_id = {variant.variant_id: variant for variant in variants}
    rows: list[dict[str, Any]] = []
    for result in results:
        variant_id = str(result.get("variant_id") or "")
        variant = variant_by_id.get(variant_id)
        summary_path = Path(str(result.get("summary_path") or "")) if result.get("summary_path") else None
        summary = _read_json(summary_path) if summary_path and summary_path.exists() else {}
        threshold = summary.get("selected_threshold", {}) if isinstance(summary, Mapping) else {}
        route_coverage = summary.get("route_coverage", {}) if isinstance(summary, Mapping) else {}
        routed_validation_trades = _metric(summary, "mt5_routed_total_validation_is", "trade_count")
        routed_oos_trades = _metric(summary, "mt5_routed_total_oos", "trade_count")
        routed_validation_per_day = _per_day(routed_validation_trades, VALIDATION_DAYS)
        routed_oos_per_day = _per_day(routed_oos_trades, OOS_DAYS)
        row: dict[str, Any] = {
            "variant_id": variant_id,
            "group": "" if variant is None else variant.group,
            "run_id": str(result.get("run_id") or summary.get("run_id") or (variant.run_id if variant else "")),
            "external_verification_status": summary.get("external_verification_status", result.get("external_verification_status", "")),
            "threshold_id": threshold.get("threshold_id", "") if isinstance(threshold, Mapping) else "",
            "tier_a_short_threshold": "" if variant is None else variant.tier_a_short_threshold,
            "tier_a_long_threshold": "" if variant is None else variant.tier_a_long_threshold,
            "tier_a_min_margin": "" if variant is None else variant.tier_a_min_margin,
            "tier_b_short_threshold": "" if variant is None else variant.tier_b_short_threshold,
            "tier_b_long_threshold": "" if variant is None else variant.tier_b_long_threshold,
            "tier_b_min_margin": "" if variant is None else variant.tier_b_min_margin,
            "max_hold_bars": threshold.get("max_hold_bars", variant.max_hold_bars if variant else "") if isinstance(threshold, Mapping) else "",
            "session_slice_id": "" if variant is None or variant.session_slice_id is None else variant.session_slice_id,
            "tier_b_allowed_subtypes": "" if variant is None else _compact(variant.tier_b_allowed_subtypes),
            "tier_a_validation_closed_trades": _metric(summary, "mt5_tier_a_only_validation_is", "trade_count"),
            "tier_a_validation_net_profit": _metric(summary, "mt5_tier_a_only_validation_is", "net_profit"),
            "tier_a_validation_profit_factor": _metric(summary, "mt5_tier_a_only_validation_is", "profit_factor"),
            "tier_a_oos_closed_trades": _metric(summary, "mt5_tier_a_only_oos", "trade_count"),
            "tier_a_oos_net_profit": _metric(summary, "mt5_tier_a_only_oos", "net_profit"),
            "tier_a_oos_profit_factor": _metric(summary, "mt5_tier_a_only_oos", "profit_factor"),
            "tier_b_validation_closed_trades": _metric(summary, "mt5_tier_b_fallback_only_validation_is", "trade_count"),
            "tier_b_validation_net_profit": _metric(summary, "mt5_tier_b_fallback_only_validation_is", "net_profit"),
            "tier_b_validation_profit_factor": _metric(summary, "mt5_tier_b_fallback_only_validation_is", "profit_factor"),
            "tier_b_oos_closed_trades": _metric(summary, "mt5_tier_b_fallback_only_oos", "trade_count"),
            "tier_b_oos_net_profit": _metric(summary, "mt5_tier_b_fallback_only_oos", "net_profit"),
            "tier_b_oos_profit_factor": _metric(summary, "mt5_tier_b_fallback_only_oos", "profit_factor"),
            "routed_validation_closed_trades": routed_validation_trades,
            "routed_validation_trades_per_day": "" if routed_validation_per_day is None else f"{routed_validation_per_day:.6f}",
            "routed_validation_net_profit": _metric(summary, "mt5_routed_total_validation_is", "net_profit"),
            "routed_validation_profit_factor": _metric(summary, "mt5_routed_total_validation_is", "profit_factor"),
            "routed_validation_drawdown": _metric(summary, "mt5_routed_total_validation_is", "max_drawdown_amount"),
            "routed_validation_short_trades": _metric(summary, "mt5_routed_total_validation_is", "short_trade_count"),
            "routed_validation_long_trades": _metric(summary, "mt5_routed_total_validation_is", "long_trade_count"),
            "routed_oos_closed_trades": routed_oos_trades,
            "routed_oos_trades_per_day": "" if routed_oos_per_day is None else f"{routed_oos_per_day:.6f}",
            "routed_oos_net_profit": _metric(summary, "mt5_routed_total_oos", "net_profit"),
            "routed_oos_profit_factor": _metric(summary, "mt5_routed_total_oos", "profit_factor"),
            "routed_oos_drawdown": _metric(summary, "mt5_routed_total_oos", "max_drawdown_amount"),
            "routed_oos_short_trades": _metric(summary, "mt5_routed_total_oos", "short_trade_count"),
            "routed_oos_long_trades": _metric(summary, "mt5_routed_total_oos", "long_trade_count"),
            "routed_validation_b_fallback_bars": _metric(summary, "mt5_routed_tier_b_fallback_used_validation_is", "route_bars"),
            "routed_oos_b_fallback_bars": _metric(summary, "mt5_routed_tier_b_fallback_used_oos", "route_bars"),
            "route_coverage_by_split": json.dumps(route_coverage.get("by_split", {}), ensure_ascii=False, sort_keys=True) if isinstance(route_coverage, Mapping) else "",
            "error": result.get("error", ""),
            "summary_path": str(summary_path.as_posix()) if summary_path else "",
            "notes": "" if variant is None else variant.notes,
        }
        row["judgment"] = _runtime_judgment(row)
        rows.append(row)
    return rows


def _candidate_score(row: Mapping[str, Any]) -> tuple[float, float, float, float, float]:
    if row.get("external_verification_status") != "completed":
        return (-1.0, 0.0, 0.0, 0.0, 0.0)
    validation_net = _float(row.get("routed_validation_net_profit"))
    oos_net = _float(row.get("routed_oos_net_profit"))
    density_floor = min(
        _float(row.get("routed_validation_trades_per_day")),
        _float(row.get("routed_oos_trades_per_day")),
    )
    pf_floor = min(
        _float(row.get("routed_validation_profit_factor")),
        _float(row.get("routed_oos_profit_factor")),
    )
    drawdown = max(_float(row.get("routed_validation_drawdown")), _float(row.get("routed_oos_drawdown")))
    net_total = validation_net + oos_net
    pass_rank = 0.0
    if validation_net > 0.0 and oos_net > 0.0 and density_floor >= 5.0 and pf_floor >= 1.05:
        pass_rank = 4.0
    elif validation_net > 0.0 and oos_net > 0.0 and density_floor >= 3.0 and pf_floor >= 1.05:
        pass_rank = 3.0
    elif validation_net > 0.0 and oos_net > 0.0:
        pass_rank = 2.0
    elif validation_net > 0.0 or oos_net > 0.0:
        pass_rank = 1.0
    return (pass_rank, pf_floor, density_floor, net_total, -drawdown)


def _best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    verified = [row for row in rows if row.get("external_verification_status") == "completed"]
    if not verified:
        return None
    return max(verified, key=_candidate_score)


def _is_stronger_than_d38h10(row: Mapping[str, Any]) -> bool:
    validation_net = _float(row.get("routed_validation_net_profit"))
    oos_net = _float(row.get("routed_oos_net_profit"))
    if validation_net <= 0.0 or oos_net <= 0.0:
        return False
    density_floor = min(
        _float(row.get("routed_validation_trades_per_day")),
        _float(row.get("routed_oos_trades_per_day")),
    )
    pf_floor = min(
        _float(row.get("routed_validation_profit_factor")),
        _float(row.get("routed_oos_profit_factor")),
    )
    total_net = validation_net + oos_net
    drawdown = max(_float(row.get("routed_validation_drawdown")), _float(row.get("routed_oos_drawdown")))
    ref_drawdown = max(
        292.33,
        D38H10_REFERENCE["routed_oos_drawdown"],
    )
    ref_pf_floor = min(
        D38H10_REFERENCE["routed_validation_profit_factor"],
        D38H10_REFERENCE["routed_oos_profit_factor"],
    )
    ref_total_net = D38H10_REFERENCE["routed_validation_net_profit"] + D38H10_REFERENCE["routed_oos_net_profit"]
    return (
        density_floor >= 3.0
        and pf_floor >= ref_pf_floor + 0.02
        and total_net >= ref_total_net + 20.0
        and drawdown <= ref_drawdown
    )


def _final_candidate_judgment(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = _best_row(rows)
    if best is None:
        return {
            "stage56_judgment": "blocked",
            "best_variant": None,
            "reason": "no completed actual MT5 routed evidence",
        }
    selected_candidates = [
        row
        for row in rows
        if row.get("judgment") in {
            "selected_research_baseline_candidate_actual_routed_mt5",
            "strong_selected_research_baseline_candidate_actual_routed_mt5",
        }
    ]
    if selected_candidates:
        selected = max(selected_candidates, key=_candidate_score)
        return {
            "stage56_judgment": "selected_research_baseline",
            "best_variant": dict(selected),
            "reason": "actual routed MT5(실제 라우팅 MT5) validation/OOS(검증/표본외)가 preferred density(선호 밀도)와 PF floor(수익 팩터 하한)를 충족",
        }
    stronger_candidates = [row for row in rows if _is_stronger_than_d38h10(row)]
    if stronger_candidates:
        selected = max(stronger_candidates, key=_candidate_score)
        return {
            "stage56_judgment": "stronger_baseline_candidate_only",
            "best_variant": dict(selected),
            "reason": "stronger quality/net candidate(품질/순손익 강화 후보)이지만 selected baseline preferred density target(선택 기준선 선호 밀도 목표) 미달",
        }
    return {
        "stage56_judgment": "no_dense_engine_found",
        "best_variant": dict(best),
        "reason": "deep repair suite(조밀 보정 묶음)가 selected or stronger dense actual routed MT5 candidate(선택 또는 강화 조밀 실제 라우팅 MT5 후보)를 만들지 못함",
    }


def _write_report(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any], *, attempt_mt5: bool) -> None:
    best = final_read.get("best_variant")
    best_line = "`none`" if not isinstance(best, Mapping) else f"`{best.get('variant_id')}` / `{best.get('judgment')}`"
    lines = [
        "# Run50D Deep Repair Suite(50D 조밀 보정 묶음)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`",
        f"- mt5_attempted(MT5 시도): `{bool(attempt_mt5)}`",
        f"- final_read(최종 판독): `{final_read.get('stage56_judgment')}`",
        f"- best_variant(최선 변형): {best_line}",
        "- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`",
        "",
        "## Design(설계)",
        "",
        "- action(행동): d38h10 주변 threshold(임계값), hold(보유), margin(마진), long/short balance(롱/숏 균형), Tier B fallback subtype(Tier B 대체 하위유형), session slice(세션 절편)를 실제 MT5(메타트레이더5)로 다시 실행했다.",
        "- effect(효과): previous closeout(이전 종료) `baseline_candidate_only(기준선 후보 전용)`을 보존하면서, 같은 Stage56 target contract(목표 계약)에 더 강한 증거를 붙인다.",
        "- acceptance(수용): selected_research_baseline(선택 연구 기준선)은 actual routed MT5(실제 라우팅 MT5) validation/OOS(검증/표본외) 모두 양수, PF(수익 팩터) >= 1.05, preferred density(선호 밀도) 5~10 trades/day(거래/일)에 근접 또는 충족해야 한다.",
        "- comparison(비교): d38h10 reference(참조)는 routed validation(라우팅 검증) 4.464481/day PF 1.07, routed OOS(라우팅 표본외) 3.446154/day PF 1.13, total net(총 순손익) 492.48이다.",
        "",
        "## Results(결과)",
        "",
        "| variant(변형) | group(묶음) | routed validation/day(라우팅 검증/일) | routed OOS/day(라우팅 표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {group} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} | `{judgment}` |".format(
                variant=row.get("variant_id", ""),
                group=row.get("group", ""),
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Final Read(최종 판독)",
            "",
            f"- judgment(판정): `{final_read.get('stage56_judgment')}`",
            f"- reason(이유): {final_read.get('reason')}",
            "- effect(효과): 이 판독은 research baseline selection(연구 기준선 선택) 안에서만 유효하고, live readiness(실거래 준비)나 runtime authority(런타임 권위)를 만들지 않는다.",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8-sig")


def _ledger_parent_row(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    best = final_read.get("best_variant")
    best_map = best if isinstance(best, Mapping) else {}
    completed_count = sum(1 for row in rows if row.get("external_verification_status") == "completed")
    status = "completed" if completed_count else "blocked"
    primary_kpi = ledger_pairs(
        (
            ("judgment", final_read.get("stage56_judgment")),
            ("best_variant", best_map.get("variant_id")),
            ("routed_validation_trades_per_day", best_map.get("routed_validation_trades_per_day")),
            ("routed_oos_trades_per_day", best_map.get("routed_oos_trades_per_day")),
            ("routed_validation_pf", best_map.get("routed_validation_profit_factor")),
            ("routed_oos_pf", best_map.get("routed_oos_profit_factor")),
            ("routed_validation_net", best_map.get("routed_validation_net_profit")),
            ("routed_oos_net", best_map.get("routed_oos_net_profit")),
        )
    )
    guardrail_kpi = ledger_pairs(
        (
            ("completed_variants", completed_count),
            ("variant_count", len(rows)),
            ("reference", "run50C_d38h10"),
            ("boundary", "research_baseline_selection_only"),
            ("no_operating_claim", True),
        )
    )
    return {
        "ledger_row_id": f"{PARENT_RUN_ID}__parent_review",
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "subrun_id": "parent_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage56_deep_repair_parent_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage56_baseline_selection",
        "scoreboard_lane": "runtime_probe",
        "status": status,
        "judgment": str(final_read.get("stage56_judgment")),
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": primary_kpi,
        "guardrail_kpi": guardrail_kpi,
        "external_verification_status": "completed" if completed_count else "blocked",
        "notes": ledger_pairs((("reason", final_read.get("reason")), ("actual_routed_total_only", True))),
    }


def _write_parent_rows(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    parent_row = _ledger_parent_row(rows, final_read)
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage56_deep_dense_repair_suite",
                "status": "reviewed" if parent_row["status"] == "completed" else "blocked",
                "judgment": str(final_read.get("stage56_judgment")),
                "path": REPORT_PATH.as_posix(),
                "notes": ledger_pairs(
                    (
                        ("variant_count", len(rows)),
                        ("best_variant", (final_read.get("best_variant") or {}).get("variant_id") if isinstance(final_read.get("best_variant"), Mapping) else None),
                        ("boundary", "research_baseline_selection_only_no_operating_claim"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return {
        "stage_run_ledger": stage_payload,
        "project_alpha_run_ledger": project_payload,
        "run_registry": registry_payload,
    }


def _file_hash(path: Path) -> str | None:
    return sha256_file_lf_normalized(path) if path.exists() else None


def _write_aggregate_summary(
    results: Sequence[Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "completed" if any(row.get("external_verification_status") == "completed" for row in rows) else "blocked",
        "final_read": final_read,
        "d38h10_reference": D38H10_REFERENCE,
        "variant_rows": [dict(row) for row in rows],
        "variant_payloads": [dict(result) for result in results],
        "artifacts": {
            "report_path": REPORT_PATH.as_posix(),
            "results_csv_path": RESULTS_CSV_PATH.as_posix(),
            "ledger_payload": dict(ledger_payload),
        },
        "artifact_hashes": {
            "report_sha256": _file_hash(REPORT_PATH),
            "results_csv_sha256": _file_hash(RESULTS_CSV_PATH),
        },
        "boundary": "research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
    }
    write_json(AGGREGATE_SUMMARY_PATH, payload)


def _select_variants(
    *,
    selected_ids: Iterable[str] | None,
    selected_groups: Iterable[str] | None,
    max_variants: int | None,
) -> tuple[RepairVariant, ...]:
    selected = list(DEFAULT_VARIANTS)
    if selected_groups:
        wanted_groups = {group.strip() for group in selected_groups if group.strip()}
        selected = [variant for variant in selected if variant.group in wanted_groups]
    if selected_ids:
        wanted = {variant_id.strip() for variant_id in selected_ids if variant_id.strip()}
        selected = [variant for variant in selected if variant.variant_id in wanted]
        missing = sorted(wanted.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if not selected:
        raise ValueError("At least one variant is required.")
    return tuple(selected)


def _split_values(values: Sequence[str]) -> tuple[str, ...]:
    parts: list[str] = []
    for value in values:
        parts.extend(part.strip() for part in str(value).split(",") if part.strip())
    return tuple(parts)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 deep dense repair MT5 suite.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--disable-routed-fallback", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true", default=True)
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--groups", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--common-files-root", default=str(logreg_scout.DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(logreg_scout.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(logreg_scout.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    variants = _select_variants(
        selected_ids=_split_values(args.variant_id),
        selected_groups=_split_values(args.groups),
        max_variants=args.max_variants,
    )
    results: list[dict[str, Any]] = []
    for variant in variants:
        try:
            result = _run_variant(
                variant,
                attempt_mt5=bool(args.attempt_mt5),
                routed_fallback_enabled=not bool(args.disable_routed_fallback),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                force=bool(args.force),
            )
            result["variant_id"] = variant.variant_id
            result["variant_spec"] = {
                "group": variant.group,
                "tier_a_short_threshold": variant.tier_a_short_threshold,
                "tier_a_long_threshold": variant.tier_a_long_threshold,
                "tier_a_min_margin": variant.tier_a_min_margin,
                "tier_b_short_threshold": variant.tier_b_short_threshold,
                "tier_b_long_threshold": variant.tier_b_long_threshold,
                "tier_b_min_margin": variant.tier_b_min_margin,
                "max_hold_bars": variant.max_hold_bars,
                "session_slice_id": variant.session_slice_id,
                "tier_b_allowed_subtypes": list(variant.tier_b_allowed_subtypes),
            }
        except Exception as exc:  # pragma: no cover - keeps long MT5 batches auditable.
            error_path = RUN_ROOT / variant.variant_id / "error.json"
            error_payload = {
                "variant_id": variant.variant_id,
                "run_id": variant.run_id,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            }
            write_json(error_path, error_payload)
            result = {
                "status": "error",
                "variant_id": variant.variant_id,
                "run_id": variant.run_id,
                "external_verification_status": "blocked",
                "error": str(exc),
                "error_path": error_path.as_posix(),
            }
            if not args.continue_on_error:
                results.append(result)
                break
        results.append(dict(result))
    rows = _summary_rows(results, variants)
    _write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    final_read = _final_candidate_judgment(rows)
    _write_report(rows, final_read, attempt_mt5=bool(args.attempt_mt5))
    ledger_payload = _write_parent_rows(rows, final_read)
    _write_aggregate_summary(results, rows, final_read, ledger_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": PARENT_RUN_ID,
                "final_read": final_read,
                "results_csv_path": RESULTS_CSV_PATH.as_posix(),
                "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


SUMMARY_COLUMNS = (
    "variant_id",
    "group",
    "run_id",
    "external_verification_status",
    "threshold_id",
    "tier_a_short_threshold",
    "tier_a_long_threshold",
    "tier_a_min_margin",
    "tier_b_short_threshold",
    "tier_b_long_threshold",
    "tier_b_min_margin",
    "max_hold_bars",
    "session_slice_id",
    "tier_b_allowed_subtypes",
    "tier_a_validation_closed_trades",
    "tier_a_validation_net_profit",
    "tier_a_validation_profit_factor",
    "tier_a_oos_closed_trades",
    "tier_a_oos_net_profit",
    "tier_a_oos_profit_factor",
    "tier_b_validation_closed_trades",
    "tier_b_validation_net_profit",
    "tier_b_validation_profit_factor",
    "tier_b_oos_closed_trades",
    "tier_b_oos_net_profit",
    "tier_b_oos_profit_factor",
    "routed_validation_closed_trades",
    "routed_validation_trades_per_day",
    "routed_validation_net_profit",
    "routed_validation_profit_factor",
    "routed_validation_drawdown",
    "routed_validation_short_trades",
    "routed_validation_long_trades",
    "routed_oos_closed_trades",
    "routed_oos_trades_per_day",
    "routed_oos_net_profit",
    "routed_oos_profit_factor",
    "routed_oos_drawdown",
    "routed_oos_short_trades",
    "routed_oos_long_trades",
    "routed_validation_b_fallback_bars",
    "routed_oos_b_fallback_bars",
    "route_coverage_by_split",
    "judgment",
    "error",
    "summary_path",
    "notes",
)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

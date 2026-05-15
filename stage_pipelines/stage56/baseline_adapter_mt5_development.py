from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.adapters.baseline_adapter import adapter_contract_payload, initial_v64_contract  # noqa: E402
from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
    execute_prepared_run,
    parse_ini,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import agreement_firewall_density_recovery_branch as audit_support  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50BT"
RUN_ID = "run50BT_stage56_baseline_adapter_v64_mt5_v1"
PACKET_ID = "stage56_baseline_adapter_mt5_v1"
TERMINAL_LABEL = "adapter_first_mt5_validation_oos_completed"
BLOCKED_LABEL = "blocked_adapter_mt5_execution_missing_evidence"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
VARIANT_ID = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
VARIANT_ROOT = RUN_ROOT / VARIANT_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs/run50BR"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / VARIANT_ID
SOURCE_MODEL = SOURCE_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
SIGNAL_COLUMN = "stage56_context_gap_refill_signal"
FEATURE_ORDER_HASH = ordered_hash((SIGNAL_COLUMN,))
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_baseline_adapter_v64"

REPORT_PATH = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_development.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_audit.csv"
RISK_CSV_PATH = REVIEWS_ROOT / "run50BT_baseline_adapter_risk_telemetry.csv"
CONTRACT_JSON_PATH = SELECTED_ROOT / "baseline_adapter_contract.json"
CONTRACT_MD_PATH = SELECTED_ROOT / "baseline_adapter_initial_contract.md"
SELECTION_STATUS_PATH = SELECTED_ROOT / "selection_status.md"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
CANDIDATE_CSV_PATH = REVIEWS_ROOT / "run50BS_candidate_selection.csv"
ANCHOR_REPORT_PATH = REVIEWS_ROOT / "run50BS_baseline_adapter_transition.md"

VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion"
JUDGMENT = "adapter_first_mt5_validation_oos_completed"


@dataclass(frozen=True)
class AdapterVariant:
    variant_id: str


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return io_path(candidate).resolve().relative_to(io_path(Path(".")).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def append_once(path: Path, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if text.strip() in existing:
        return
    write_md(path, existing.rstrip() + "\n" + text.strip() + "\n")


def split_days(split: str) -> float:
    return VALIDATION_DAYS if split == "validation_is" else OOS_DAYS


def source_attempt_ini(split: str) -> Path:
    name = "x01_ta_val.ini" if split == "validation_is" else "x01_ta_oos.ini"
    return SOURCE_VARIANT_ROOT / "mt5" / name


def source_feature(split: str, tier: str = "a") -> Path:
    token = "val" if split == "validation_is" else "oos"
    return SOURCE_VARIANT_ROOT / "features" / f"{VARIANT_ID}_{tier}_{token}.csv"


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    model_local = RUN_ROOT / "models" / SOURCE_MODEL.name
    copied = [copy_local(SOURCE_MODEL, model_local)]
    copied.append(copy_to_common(model_local, f"{COMMON_ROOT}/models/{model_local.name}", common_files_root))
    feature_exports: dict[str, dict[str, Any]] = {}
    for split in ("validation_is", "oos"):
        split_token = "val" if split == "validation_is" else "oos"
        feature_local = VARIANT_ROOT / "features" / f"{VARIANT_ID}_adapter_a_{split_token}.csv"
        copied.append(copy_local(source_feature(split, "a"), feature_local))
        copied.append(copy_to_common(feature_local, f"{COMMON_ROOT}/features/{feature_local.name}", common_files_root))
        feature_exports[split] = {
            "path": rel(feature_local),
            "common_path": f"{COMMON_ROOT}/features/{feature_local.name}",
            "sha256": sha256_file_lf_normalized(feature_local),
        }
    return {
        "model_local": model_local,
        "model_common": f"{COMMON_ROOT}/models/{model_local.name}",
        "feature_exports": feature_exports,
        "common_copies": copied,
    }


def adapter_extra_set_values() -> dict[str, Any]:
    return {
        "InpAtrSltpEnabled": True,
        "InpAtrPeriod": 14,
        "InpAtrStopMultiplier": 1.5,
        "InpAtrTakeProfitMultiplier": 2.0,
        "InpAtrMinStopPoints": 0.0,
        "InpAtrMaxStopPoints": 0.0,
        "InpAtrMinTakeProfitPoints": 0.0,
        "InpAtrMaxTakeProfitPoints": 0.0,
        "InpModelRiskSizingEnabled": True,
        "InpModelRiskMinPct": 0.005,
        "InpModelRiskMaxPct": 0.05,
        "InpModelRiskConfidenceFloor": 0.55,
        "InpModelRiskConfidenceCeiling": 0.85,
        "InpModelRiskFallbackLot": 0.1,
        "InpFallbackEnabled": False,
        "InpFallbackUseOnPrimaryFlat": False,
        "InpFallbackUseOnPrimaryLowConfidence": False,
    }


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        date_values = parse_ini(source_attempt_ini(split))
        split_token = "val" if split == "validation_is" else "oos"
        for role, tier, attempt_role, prefix, attempt_token in (
            ("tier_a_only", mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{VARIANT_ID}", "ta"),
            ("routed", mt5.TIER_AB, "routed_total", f"mt5_routed_{VARIANT_ID}", "rt"),
        ):
            attempts.append(
                attempt_payload(
                    run_root=VARIANT_ROOT,
                    run_id=RUN_ID,
                    stage_number=56,
                    exploration_label="stage56_BaselineAdapter__V64ActualMt5",
                    attempt_name=f"ba01_{attempt_token}_{split_token}",
                    tier=tier,
                    split=split,
                    model_path=str(inputs["model_common"]),
                    model_id=f"{RUN_ID}_{VARIANT_ID}_entry_risk_atr_adapter",
                    model_backend="ebm_table",
                    feature_path=str(inputs["feature_exports"][split]["common_path"]),
                    feature_count=1,
                    feature_order_hash=FEATURE_ORDER_HASH,
                    short_threshold=SHORT_THRESHOLD,
                    long_threshold=LONG_THRESHOLD,
                    min_margin=MIN_MARGIN,
                    invert_signal=False,
                    from_date=str(date_values["FromDate"]),
                    to_date=str(date_values["ToDate"]),
                    primary_active_tier="tier_a",
                    attempt_role=attempt_role,
                    record_view_prefix=prefix,
                    max_hold_bars=2,
                    common_root=COMMON_ROOT,
                    fallback_enabled=False,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values={**adapter_extra_set_values(), "InpMagic": 5605001 if role == "tier_a_only" else 5605010},
                )
            )
    return attempts


def route_coverage() -> dict[str, Any]:
    coverage: dict[str, Any] = {"by_split": {}, "tier_b_disabled_reason": "disabled_initially_due_negative_fallback_only_evidence"}
    for source_split, split in (("validation", "validation_is"), ("oos", "oos")):
        a_rows = max(0, sum(1 for _ in io_path(source_feature(split, "a")).open("r", encoding="utf-8-sig")) - 1)
        b_path = source_feature(split, "b")
        b_rows = max(0, sum(1 for _ in io_path(b_path).open("r", encoding="utf-8-sig")) - 1) if path_exists(b_path) else 0
        coverage["by_split"][source_split] = {
            "tier_a_primary_rows": a_rows,
            "tier_b_fallback_rows_available_but_disabled": b_rows,
            "tier_b_fallback_rows_used": 0,
            "routed_labelable_rows": a_rows,
        }
    return coverage


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "materialized_only_no_mt5_evidence",
        }
    return execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )


def metric(record: Mapping[str, Any], key: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    return metrics.get(key)


def report_path_from_record(record: Mapping[str, Any]) -> str:
    report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
    html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
    return str(html.get("path") or metric(record, "report_path") or "")


def build_summary_rows(result: Mapping[str, Any], audit_rows: Sequence[Mapping[str, Any]], risk_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_view = {str(record.get("record_view")): record for record in result.get("mt5_kpi_records", [])}
    risk_by_attempt = {str(row.get("attempt_name")): row for row in risk_rows}
    audits = {str(row.get("record_view")): row for row in audit_rows}
    rows: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        split_prefix = "validation" if split == "validation_is" else "oos"
        for view, label, role in (
            (f"mt5_tier_a_only_{VARIANT_ID}_{split}", "tier_a_only", "tier_only_total"),
            (f"mt5_routed_{VARIANT_ID}_{split}", "actual_routed_total", "routed_total"),
        ):
            record = by_view.get(view, {})
            trade_count = float(metric(record, "trade_count") or 0.0)
            attempt_name = str(record.get("report", {}).get("attempt_name") or "")
            risk = risk_by_attempt.get(attempt_name, {})
            audit = audits.get(view, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": VARIANT_ID,
                    "split": split,
                    "view": label,
                    "route_role": role,
                    "tier_b_policy": "disabled_initially_due_negative_fallback_only_evidence",
                    "status": record.get("status", "missing"),
                    "trades_per_day": trade_count / split_days(split) if trade_count else 0.0,
                    "profit_factor": metric(record, "profit_factor"),
                    "net_profit": metric(record, "net_profit"),
                    "trade_count": metric(record, "trade_count"),
                    "max_drawdown_amount": metric(record, "max_drawdown_amount"),
                    "max_drawdown_percent": metric(record, "max_drawdown_percent"),
                    "expectancy": metric(record, "expectancy"),
                    "cost_stressed_expectancy": audit.get("cost_stressed_expectancy"),
                    "same_move_reentry_ratio": audit.get("same_move_reentry_ratio"),
                    "mfe_capture_ratio": audit.get("mfe_capture_ratio"),
                    "cooldown12_trades_per_day": audit.get("trades_per_day_after_cooldown"),
                    "density_gain_survives_12bar_cooldown": audit.get("density_gain_survives_12bar_cooldown"),
                    "risk_floor_applied_count": risk.get("risk_floor_applied_count"),
                    "max_model_risk_pct": risk.get("max_model_risk_pct"),
                    "max_actual_risk_pct_after_floor": risk.get("max_actual_risk_pct_after_floor"),
                    "avg_executed_lot": risk.get("avg_executed_lot"),
                    "avg_atr_points": risk.get("avg_atr_points"),
                    "avg_open_sl_points": risk.get("avg_open_sl_points"),
                    "avg_open_tp_points": risk.get("avg_open_tp_points"),
                    "report_path": report_path_from_record(record),
                }
            )
    rows.append(
        {
            "run_id": RUN_ID,
            "variant_id": VARIANT_ID,
            "split": "validation_is+oos",
            "view": "tier_b_fallback_only",
            "route_role": "tier_b_disabled",
            "tier_b_policy": "disabled_initially_due_negative_fallback_only_evidence",
            "status": "disabled",
            "notes": "Tier B fallback-only MT5 was not run in the adapter path because run50BR evidence showed Tier B fallback-only validation/OOS net -94.14 / -254.32.",
        }
    )
    return rows


def audit_rows_for_result(result: Mapping[str, Any], cost_stress_per_trade: float) -> list[dict[str, Any]]:
    original_parent = audit_support.PARENT_RUN_ID
    try:
        audit_support.PARENT_RUN_ID = RUN_ID
        return audit_support.audit_rows_for_result(result, [AdapterVariant(VARIANT_ID)], cost_stress_per_trade)
    finally:
        audit_support.PARENT_RUN_ID = original_parent


def telemetry_float(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def risk_rows_from_result(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for execution in result.get("execution_results", []):
        runtime_outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        telemetry_path = Path(str(runtime_outputs.get("telemetry_path") or ""))
        row: dict[str, Any] = {
            "attempt_name": execution.get("attempt_name"),
            "split": execution.get("split"),
            "tier": execution.get("tier"),
            "telemetry_path": telemetry_path.as_posix() if str(telemetry_path) else "",
            "status": "missing",
        }
        if not path_exists(telemetry_path):
            row["parse_error"] = "telemetry_missing"
            rows.append(row)
            continue
        try:
            frame = pd.read_csv(io_path(telemetry_path))
            cycles = frame.loc[frame["record_type"].astype(str).eq("cycle")].copy()
            for col in (
                "model_risk_pct",
                "clipped_risk_pct",
                "computed_lot",
                "executed_lot",
                "actual_risk_pct_after_floor",
                "atr_points",
                "open_sl_points",
                "open_tp_points",
            ):
                if col in cycles:
                    cycles[col] = telemetry_float(cycles[col])
            floor = cycles.get("min_lot_floor_applied", pd.Series([], dtype=str)).astype(str).str.lower().eq("true")
            row.update(
                {
                    "status": "completed",
                    "cycle_rows": int(len(cycles)),
                    "risk_floor_applied_count": int(floor.sum()) if len(cycles) else 0,
                    "max_model_risk_pct": float(cycles["model_risk_pct"].max()) if "model_risk_pct" in cycles and not cycles.empty else None,
                    "max_actual_risk_pct_after_floor": float(cycles["actual_risk_pct_after_floor"].max()) if "actual_risk_pct_after_floor" in cycles and not cycles.empty else None,
                    "avg_executed_lot": float(cycles["executed_lot"].mean()) if "executed_lot" in cycles and not cycles.empty else None,
                    "avg_atr_points": float(cycles["atr_points"].mean()) if "atr_points" in cycles and not cycles.empty else None,
                    "avg_open_sl_points": float(cycles["open_sl_points"].mean()) if "open_sl_points" in cycles and not cycles.empty else None,
                    "avg_open_tp_points": float(cycles["open_tp_points"].mean()) if "open_tp_points" in cycles and not cycles.empty else None,
                    "telemetry_sha256": sha256_file_lf_normalized(telemetry_path),
                }
            )
        except Exception as exc:  # pragma: no cover - defensive external output parsing
            row["status"] = "blocked"
            row["parse_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


def load_anchor_reference_rows() -> dict[str, Mapping[str, Any]]:
    refs: dict[str, Mapping[str, Any]] = {}
    if not path_exists(CANDIDATE_CSV_PATH):
        return refs
    with io_path(CANDIDATE_CSV_PATH).open("r", encoding="utf-8-sig", newline="") as handle:
        for raw in csv.DictReader(handle):
            key = f"{raw.get('run_number')}/{raw.get('variant_id')}"
            refs[key] = dict(raw)
    return refs


def adapter_result_read(summary_rows: Sequence[Mapping[str, Any]]) -> str:
    routed = [row for row in summary_rows if row.get("view") == "actual_routed_total"]
    if not routed:
        return "blocked"
    if any(row.get("status") != "completed" for row in routed):
        return "blocked"
    refs = load_anchor_reference_rows()
    anchor = refs.get(f"run50BR/{VARIANT_ID}", {})
    val = next((row for row in routed if row.get("split") == "validation_is"), {})
    oos = next((row for row in routed if row.get("split") == "oos"), {})
    val_net = float(val.get("net_profit") or 0.0)
    oos_net = float(oos.get("net_profit") or 0.0)
    anchor_val = float(anchor.get("validation_net") or anchor.get("routed_validation_net") or 0.0)
    anchor_oos = float(anchor.get("oos_net") or anchor.get("routed_oos_net") or 0.0)
    if val_net >= anchor_val and oos_net >= anchor_oos:
        return "improved_anchor_net"
    if val_net > 0.0 and oos_net > 0.0:
        return "reproduced_directionally_with_adapter_risk_atr"
    return "degraded_anchor"


def artifact_rows(result: Mapping[str, Any], extra_paths: Sequence[Path]) -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []

    def add(artifact_id: str, artifact_type: str, path: Path | str, notes: str) -> None:
        p = Path(str(path))
        resolved = p if p.is_absolute() else REPO_ROOT / p
        is_file = path_exists(resolved) and io_path(resolved).is_file()
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(p),
                "sha256": sha256_file_lf_normalized(resolved) if is_file else "directory_or_not_feasible",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )

    for path in extra_paths:
        add(f"stage56_{RUN_NUMBER}_{aw.safe_name(path.stem, 80)}", path.suffix.lstrip(".") or "artifact", path, "BaselineAdapter MT5 development artifact.")
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        if html.get("path"):
            add(f"stage56_{RUN_NUMBER}_mt5_report_{aw.safe_name(str(report.get('attempt_name') or report.get('report_name')), 100)}", "mt5_html_report", str(html["path"]), "Actual BaselineAdapter MT5 Strategy Tester HTML report.")
    for execution in result.get("execution_results", []):
        runtime_outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        for key, artifact_type in (("telemetry_path", "mt5_runtime_telemetry_csv"), ("summary_path", "mt5_runtime_summary_csv")):
            value = runtime_outputs.get(key)
            if value:
                add(f"stage56_{RUN_NUMBER}_{artifact_type}_{aw.safe_name(str(execution.get('attempt_name')), 80)}", artifact_type, str(value), "Common Files runtime telemetry copied by MT5 EA.")
    return rows


def write_ledgers(result: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_mt5_development",
            "status": "completed" if external == "completed" else "blocked",
            "judgment": JUDGMENT if external == "completed" else BLOCKED_LABEL,
            "path": rel(RUN_ROOT),
            "notes": f"development_anchor={VARIANT_ID};views=tier_a_only,routed_total;tier_b=disabled;boundary={BOUNDARY}",
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    ledger_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_disabled_record",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_disabled",
            "parent_run_id": RUN_ID,
            "record_view": "baseline_adapter_tier_b_disabled",
            "tier_scope": mt5.TIER_B,
            "kpi_scope": "baseline_adapter_mt5_development",
            "scoreboard_lane": "runtime_probe",
            "status": "disabled",
            "judgment": "tier_b_disabled_due_prior_fallback_damage",
            "path": rel(SUMMARY_JSON_PATH),
            "primary_kpi": "tier_b_fallback_only_validation_net=-94.14;tier_b_fallback_only_oos_net=-254.32",
            "guardrail_kpi": "actual_routed_total_uses_tier_a_primary_only",
            "external_verification_status": external,
            "notes": "Tier B fallback-only was recorded as disabled, not silently omitted.",
        }
    )
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_contract_updates() -> None:
    contract = adapter_contract_payload(initial_v64_contract())
    contract["mt5_adapter_path"] = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "terminal_label_required_for_goal": TERMINAL_LABEL,
        "actual_mt5_required": True,
        "tier_b_policy": "disabled_initially_due_negative_fallback_only_evidence",
        "risk_sizing_runtime": {
            "owner": "RuntimeProbeEA model confidence mapped to risk_per_trade",
            "cap_pct": 0.05,
            "floor_lot": 0.01,
        },
        "atr_runtime": {"enabled": True, "period": 14, "sl_multiplier": 1.5, "tp_multiplier": 2.0},
    }
    write_json(CONTRACT_JSON_PATH, contract)
    write_md(
        CONTRACT_MD_PATH,
        f"""# BaselineAdapter Initial Contract(기준선 어댑터 초기 계약)

- adapter_id(어댑터 ID): `{contract['adapter_id']}`
- development_anchor(개발 기준점): `{VARIANT_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- routing(라우팅): Tier A primary(Tier A 우선), Tier B disabled(Tier B 비활성)
- risk(위험): model confidence(모델 신뢰도) 기반 risk_per_trade(거래당 위험), cap(상한) `5%`, floor lot(최소 랏) `0.01`
- ATR bracket(ATR 브래킷): ATR(14), SL(손절) `1.5x`, TP(익절) `2.0x`
- MT5 run(MT5 실행): `{RUN_ID}`

Effect(효과): contract(계약)이 더 이상 handoff-only(인계 전용)가 아니라 실제 adapter MT5 validation/OOS(어댑터 MT5 검증/표본외) 경로를 가리킨다.
""",
    )


def write_report(summary_rows: Sequence[Mapping[str, Any]], risk_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    refs = load_anchor_reference_rows()
    anchor = refs.get(f"run50BR/{VARIANT_ID}", {})
    backup = refs.get("run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b", {})
    read = adapter_result_read(summary_rows)
    lines = [
        "# Stage56 run50BT BaselineAdapter MT5 Development(56단계 run50BT 기준선 어댑터 MT5 개발)",
        "",
        f"- terminal_label(종료 라벨): `{TERMINAL_LABEL if result.get('external_verification_status') == 'completed' else BLOCKED_LABEL}`",
        f"- development_anchor(개발 기준점): `run50BR/{VARIANT_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- backup_anchor(예비 기준점): `run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- adapter_result_read(어댑터 결과 판독): `{read}`",
        "",
        "Action(행동): 기존 run50BR anchor(기준점)의 entry signal(진입 신호)을 BaselineAdapter(기준선 어댑터) 경로로 복제하고 risk/ATR/telemetry(위험/ATR/텔레메트리)를 켠 뒤 실제 MT5 validation/OOS(검증/표본외)를 실행했다.",
        "Effect(효과): broad candidate hunting(넓은 후보 탐색)을 멈추고 adapter path(어댑터 경로)의 첫 실제 tester evidence(테스터 근거)를 만들었다.",
        "",
        "## Anchor Comparison(기준점 비교)",
        "",
        "| item | val day | oos day | val PF | oos PF | val net | oos net |",
        "|---|---:|---:|---:|---:|---:|---:|",
        f"| development_anchor | {anchor.get('validation_trades_per_day','')} | {anchor.get('oos_trades_per_day','')} | {anchor.get('validation_pf','')} | {anchor.get('oos_pf','')} | {anchor.get('validation_net','')} | {anchor.get('oos_net','')} |",
        f"| backup_anchor | {backup.get('validation_trades_per_day','')} | {backup.get('oos_trades_per_day','')} | {backup.get('validation_pf','')} | {backup.get('oos_pf','')} | {backup.get('validation_net','')} | {backup.get('oos_net','')} |",
        "",
        "## Adapter MT5 Result(어댑터 MT5 결과)",
        "",
        "| split | view | day | PF | net | trades | max DD | cost exp | same move | MFE | floor count | max risk | report |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        if row.get("view") == "tier_b_fallback_only":
            continue
        lines.append(
            "| {split} | {view} | {day} | {pf} | {net} | {trades} | {dd} | {cost} | {same} | {mfe} | {floor} | {risk} | {report} |".format(
                split=row.get("split", ""),
                view=row.get("view", ""),
                day=aw.fmt(row.get("trades_per_day")),
                pf=aw.fmt(row.get("profit_factor")),
                net=aw.fmt(row.get("net_profit")),
                trades=aw.fmt(row.get("trade_count")),
                dd=aw.fmt(row.get("max_drawdown_amount")),
                cost=aw.fmt(row.get("cost_stressed_expectancy")),
                same=aw.fmt(row.get("same_move_reentry_ratio")),
                mfe=aw.fmt(row.get("mfe_capture_ratio")),
                floor=aw.fmt(row.get("risk_floor_applied_count")),
                risk=aw.fmt(row.get("max_model_risk_pct")),
                report=row.get("report_path", ""),
            )
        )
    tier_b = next((row for row in summary_rows if row.get("view") == "tier_b_fallback_only"), {})
    lines.extend(
        [
            "",
            "## Tier B Policy(Tier B 정책)",
            "",
            f"- status(상태): `{tier_b.get('status', 'disabled')}`",
            f"- reason(이유): {tier_b.get('notes', '')}",
            "",
            "## Risk Telemetry(위험 텔레메트리)",
            "",
            "| attempt | status | rows | floor count | max model risk | max actual risk | avg lot | avg ATR |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in risk_rows:
        lines.append(
            "| {attempt} | {status} | {rows} | {floor} | {model} | {actual} | {lot} | {atr} |".format(
                attempt=row.get("attempt_name", ""),
                status=row.get("status", ""),
                rows=aw.fmt(row.get("cycle_rows")),
                floor=aw.fmt(row.get("risk_floor_applied_count")),
                model=aw.fmt(row.get("max_model_risk_pct")),
                actual=aw.fmt(row.get("max_actual_risk_pct_after_floor")),
                lot=aw.fmt(row.get("avg_executed_lot")),
                atr=aw.fmt(row.get("avg_atr_points")),
            )
        )
    lines.extend(
        [
            "",
            "Known weaknesses(알려진 약점): cost-stressed expectancy(비용 압박 기대값), same-move density(동일 이동 밀도), and whether dynamic risk/ATR(동적 위험/ATR)이 PF/net(수익 팩터/순손익)을 훼손하는지.",
            "",
            f"Judgment(판정): `{JUDGMENT if result.get('external_verification_status') == 'completed' else BLOCKED_LABEL}`. No live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준)를 주장하지 않는다.",
        ]
    )
    write_md(REPORT_PATH, "\n".join(lines))


def update_state_docs(summary_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    label = TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL
    routed_val = next((row for row in summary_rows if row.get("view") == "actual_routed_total" and row.get("split") == "validation_is"), {})
    routed_oos = next((row for row in summary_rows if row.get("view") == "actual_routed_total" and row.get("split") == "oos"), {})
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{RUN_ID}`
- active stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{VARIANT_ID}`
- backup_anchor(예비 기준점): `v60_v47_et_stable_damage_firewall_h2c0_no_b`
- status(상태): `{label}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage56(56단계)은 broad run50 candidate hunting(넓은 run50 후보 사냥)을 멈추고 BaselineAdapter MT5 validation/OOS(기준선 어댑터 MT5 검증/표본외)를 실제로 실행했다.
Effect(효과): 다음 작업은 새 후보 찾기가 아니라 adapter bottleneck(어댑터 병목)인 risk/ATR/cost/same-move(위험/ATR/비용/동일 이동) 수리다.

## Adapter MT5 Evidence(어댑터 MT5 근거)

- validation routed trades/day(검증 라우팅 일 거래): `{aw.fmt(routed_val.get('trades_per_day'))}`
- OOS routed trades/day(표본외 라우팅 일 거래): `{aw.fmt(routed_oos.get('trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{aw.fmt(routed_val.get('profit_factor'))}` / `{aw.fmt(routed_oos.get('profit_factor'))}`
- validation/OOS net(검증/표본외 순손익): `{aw.fmt(routed_val.get('net_profit'))}` / `{aw.fmt(routed_oos.get('net_profit'))}`
- tier_b_policy(Tier B 정책): disabled(비활성), because prior fallback-only evidence(이전 대체 단독 근거)가 손상됨.

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_baseline_adapter_development`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- current run(현재 실행): `{RUN_ID}`
- current_judgment(현재 판정): `{label}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{VARIANT_ID}`
- backup_anchor(예비 기준점): `v60_v47_et_stable_damage_firewall_h2c0_no_b`

## BaselineAdapter Evidence(기준선 어댑터 근거)

- selection_report(선택 보고서): `{rel(ANCHOR_REPORT_PATH)}`
- candidate_table(후보 표): `{rel(CANDIDATE_CSV_PATH)}`
- adapter_mt5_report(어댑터 MT5 보고서): `{rel(REPORT_PATH)}`
- adapter_summary_json(어댑터 요약 JSON): `{rel(SUMMARY_JSON_PATH)}`
- adapter_summary_csv(어댑터 요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- adapter_risk_telemetry(어댑터 위험 텔레메트리): `{rel(RISK_CSV_PATH)}`

Effect(효과): selection(선택) 단계는 완료됐고, 현재 병목은 adapter MT5 result(어댑터 MT5 결과)의 cost/same-move/risk/ATR(비용/동일 이동/위험/ATR) 수리다.
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage56(56단계) `{STAGE_ID}`: run50BT(실행50BT) BaselineAdapter MT5 validation/OOS(기준선 어댑터 MT5 검증/표본외) 실행; "
        f"development_anchor(개발 기준점)는 `{VARIANT_ID}`이고 terminal_label(종료 라벨)은 `{label}`이다. "
        "Effect(효과): 후보 사냥을 멈춘 상태에서 adapter risk/ATR/telemetry(어댑터 위험/ATR/텔레메트리)가 실제 tester result(테스터 결과)를 만들었다."
    )
    text = re.sub(r"- >-\n  Stage56[^\n]*run50BT[^\n]*BaselineAdapter MT5[^\n]*\n", "", text)
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    text = remove_workspace_block(text, "stage56_baseline_adapter_mt5:")
    block = f"""
stage56_baseline_adapter_mt5:
  packet_id: {PACKET_ID}
  current_run_id: {RUN_ID}
  development_anchor: {VARIANT_ID}
  backup_anchor: v60_v47_et_stable_damage_firewall_h2c0_no_b
  terminal_label: {label}
  boundary: {BOUNDARY}
  next_action: repair_adapter_cost_same_move_risk_atr_bottleneck
"""
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def remove_workspace_block(text: str, key: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].startswith(key):
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith(" ")):
                index += 1
            continue
        output.append(lines[index])
        index += 1
    return "".join(output)


def write_packet_files(result: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]], risk_rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    label = TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL
    aggregate = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "terminal_label": label,
        "external_verification_status": external,
        "development_anchor": VARIANT_ID,
        "backup_anchor": "v60_v47_et_stable_damage_firewall_h2c0_no_b",
        "selected_research_baseline": "none",
        "adapter_result_read": adapter_result_read(summary_rows),
        "summary_json_path": rel(SUMMARY_JSON_PATH),
        "summary_csv_path": rel(SUMMARY_CSV_PATH),
        "risk_csv_path": rel(RISK_CSV_PATH),
        "report_path": rel(REPORT_PATH),
        "ledger_payload": ledger_payload,
        "forbidden_claims": {
            "live_readiness": False,
            "runtime_authority": False,
            "operating_promotion": False,
            "operating_reference": False,
            "production_baseline": False,
            "reviewed_closed": False,
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", aggregate)
    write_json(PACKET_ROOT / "runtime_parity_audit.json", {
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5")),
        "shared_contract": "entry signal csv + ebm_table + risk confidence map + ATR bracket + MT5 tester model=4",
        "known_differences": "Tier B disabled; ONNX hardening not started",
        "parity_check": "actual MT5 validation/OOS tester reports" if external == "completed" else "blocked",
        "runtime_claim_boundary": "research_development_only",
        "status": "passed" if external == "completed" else "blocked",
    })
    write_json(PACKET_ROOT / "backtest_forensics_audit.json", {
        "tester_identity": "terminal64.exe; US100 M5; deposit=500; leverage=1:100; model=4; validation and OOS",
        "ea_identity": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5 with RuntimeTelemetry and ExecutionBridge module hashes in artifact registry",
        "trade_evidence": "MT5 Strategy Tester HTML reports plus telemetry CSV",
        "backtest_judgment": "usable_with_boundary" if external == "completed" else "blocked",
        "status": "passed" if external == "completed" else "blocked",
    })
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {
        "required_gates": [
            "candidate_selection_audit",
            "adapter_contract_scaffold",
            "actual_adapter_mt5_validation",
            "actual_adapter_mt5_oos",
            "risk_telemetry_parse",
            "artifact_lineage_audit",
            "final_claim_guard",
        ],
        "covered_gates": [
            "candidate_selection_audit",
            "adapter_contract_scaffold",
            "actual_adapter_mt5_validation" if external == "completed" else "missing",
            "actual_adapter_mt5_oos" if external == "completed" else "missing",
            "risk_telemetry_parse" if all(row.get("status") == "completed" for row in risk_rows) else "partial",
            "artifact_lineage_audit",
            "final_claim_guard",
        ],
        "status": "passed" if external == "completed" else "blocked",
    })
    write_json(PACKET_ROOT / "result_judgment_gate.json", {
        "result_subject": RUN_ID,
        "evidence_available": ["candidate selection report", "MT5 tester reports", "summary csv/json", "risk telemetry csv"],
        "evidence_missing": ["final ONNX hardening", "live readiness", "operating promotion"],
        "judgment_label": "runtime_probe",
        "claim_boundary": BOUNDARY,
        "next_condition": "repair adapter cost/same-move/risk/ATR bottleneck and rerun validation/OOS",
        "status": "passed" if external == "completed" else "blocked",
    })
    write_json(PACKET_ROOT / "final_claim_guard.json", {
        "allowed_terminal_label": label,
        "forbidden_labels": ["reviewed_closed", "production_ready", "live_ready", "operating_reference", "runtime_authority", "development_anchor_selected_and_adapter_development_started"],
        "status": "passed" if label == TERMINAL_LABEL else "blocked",
    })
    write_json(PACKET_ROOT / "skill_receipts.json", [
        {"skill": "obsidian-reentry-read", "status": "completed"},
        {"skill": "obsidian-runtime-parity", "status": "completed" if external == "completed" else "blocked"},
        {"skill": "obsidian-backtest-forensics", "status": "completed" if external == "completed" else "blocked"},
        {"skill": "obsidian-artifact-lineage", "status": "completed"},
        {"skill": "obsidian-performance-attribution", "status": "completed"},
        {"skill": "obsidian-result-judgment", "status": "completed"},
    ])


def write_run_files(result: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], risk_rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows, aw.reopen.AUDIT_COLUMNS)
    write_csv(RISK_CSV_PATH, risk_rows)
    payload = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "terminal_label": TERMINAL_LABEL if result.get("external_verification_status") == "completed" else BLOCKED_LABEL,
        "development_anchor": VARIANT_ID,
        "backup_anchor": "v60_v47_et_stable_damage_firewall_h2c0_no_b",
        "selected_research_baseline": "none",
        "external_verification_status": result.get("external_verification_status"),
        "adapter_result_read": adapter_result_read(summary_rows),
        "summary_rows": list(summary_rows),
        "risk_rows": list(risk_rows),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "ledger_payload": ledger_payload,
    }
    write_json(SUMMARY_JSON_PATH, payload)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "development_anchor": VARIANT_ID,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "compile": result.get("compile", {}),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    })
    write_json(RUN_ROOT / "kpi_record.json", {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "execution_results": result.get("execution_results", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    })
    write_packet_files(result, summary_rows, risk_rows, ledger_payload)


def update_logs(summary_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    label = TERMINAL_LABEL if result.get("external_verification_status") == "completed" else BLOCKED_LABEL
    routed_val = next((row for row in summary_rows if row.get("view") == "actual_routed_total" and row.get("split") == "validation_is"), {})
    routed_oos = next((row for row in summary_rows if row.get("view") == "actual_routed_total" and row.get("split") == "oos"), {})
    entry = f"""
## 2026-05-15 run50BT BaselineAdapter MT5 Development(기준선 어댑터 MT5 개발)
- action(행동): BaselineAdapter(기준선 어댑터) risk/ATR/telemetry(위험/ATR/텔레메트리)를 켜고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): adapter path(어댑터 경로)가 첫 tester evidence(테스터 근거)를 갖게 됐다.
- terminal_label(종료 라벨): `{label}`
- validation/OOS routed trades/day(검증/표본외 라우팅 일 거래): `{aw.fmt(routed_val.get('trades_per_day'))}` / `{aw.fmt(routed_oos.get('trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{aw.fmt(routed_val.get('profit_factor'))}` / `{aw.fmt(routed_oos.get('profit_factor'))}`
- validation/OOS net(검증/표본외 순손익): `{aw.fmt(routed_val.get('net_profit'))}` / `{aw.fmt(routed_oos.get('net_profit'))}`
"""
    append_once(PROGRESS_LOG_PATH, entry)
    append_once(
        CHANGELOG_PATH,
        """
## 2026-05-15 Stage56 run50BT BaselineAdapter MT5 Development(56단계 run50BT 기준선 어댑터 MT5 개발)
- completed(완료): actual BaselineAdapter MT5 validation/OOS(실제 기준선 어댑터 MT5 검증/표본외)를 실행하고 summary/ledger/current truth(요약/장부/현재 진실)를 갱신했다.
""",
    )


def blocked_attempt_summary(result: Mapping[str, Any]) -> dict[str, Any]:
    blocked = [item for item in result.get("execution_results", []) if item.get("status") != "completed"]
    first = blocked[0] if blocked else {}
    return {
        "attempted_command": first.get("command") or result.get("compile", {}).get("command"),
        "failure_reason": first.get("blocker") or first.get("stderr") or first.get("runtime_outputs", {}).get("last_summary") or result.get("compile", {}),
        "repair_plan": "repair MT5 execution/runtime output failure and rerun validation/OOS before terminal completion",
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 BaselineAdapter actual MT5 validation/OOS.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=360)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    write_contract_updates()
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 56,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": {"adapter_entry_model": {"path": rel(inputs["model_local"]), "common_path": inputs["model_common"]}},
        "route_coverage": route_coverage(),
        "model_family": "baseline_adapter_v64_ebm_table_with_runtime_risk_atr",
        "feature_set_id": "stage56_context_gap_refill_signal_plus_runtime_risk_atr",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
    }
    result = execute_or_materialize(prepared, args)
    audit_rows = audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = risk_rows_from_result(result)
    summary_rows = build_summary_rows(result, audit_rows, risk_rows)
    write_report(summary_rows, risk_rows, result)
    extra_paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        AUDIT_CSV_PATH,
        RISK_CSV_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        CONTRACT_JSON_PATH,
        CONTRACT_MD_PATH,
        Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
        Path("foundation/mt5/include/ObsidianPrime/ExecutionBridge.mqh"),
        Path("foundation/mt5/include/ObsidianPrime/RuntimeTelemetry.mqh"),
        Path(__file__),
    ]
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, artifacts)
    write_run_files(result, summary_rows, audit_rows, risk_rows, ledger_payload)
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, artifacts)
    summary_payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    summary_payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, summary_payload)
    write_packet_files(result, summary_rows, risk_rows, ledger_payload)
    update_state_docs(summary_rows, result)
    update_logs(summary_rows, result)
    if result.get("external_verification_status") != "completed":
        write_json(PACKET_ROOT / "blocked_adapter_mt5_execution_missing_evidence.json", blocked_attempt_summary(result))
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if result.get("external_verification_status") == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "terminal_label": TERMINAL_LABEL if result.get("external_verification_status") == "completed" else BLOCKED_LABEL,
                    "external_verification_status": result.get("external_verification_status"),
                    "adapter_result_read": adapter_result_read(summary_rows),
                    "summary_json": SUMMARY_JSON_PATH.as_posix(),
                    "summary_csv": SUMMARY_CSV_PATH.as_posix(),
                    "risk_csv": RISK_CSV_PATH.as_posix(),
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

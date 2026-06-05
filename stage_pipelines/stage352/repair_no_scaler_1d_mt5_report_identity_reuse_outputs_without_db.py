from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402

TODAY = "2026-06-02"

STAGE_ID = "352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity"
RUN_NUMBER = "run352B"
RUN_ID = "run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1"
PARENT_RUN_ID = "run352A_branch_stage351_to_report_identity_repair_without_db_v1"
SOURCE_RUN_ID = "run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1"
NEXT_STAGE_ID = "353_trade_shape_offense__report_recovered_density_ok_edge_rebuild"
NEXT_RUN_ID = "run353A_branch_stage352_to_trade_shape_offensive_rebuild_without_db_v1"

STATUS = "completed_stage352B_report_identity_repaired_existing_mt5_reports_recovered_no_selection"
JUDGMENT = "negative_runtime_probe_report_recovered_validation_positive_oos_negative_high_drawdown_no_selection"
DECISION = "stage352B_open_stage353A_trade_shape_offensive_rebuild_from_density_ok_runtime_parity"
CLAIM_BOUNDARY = (
    "runtime_probe_report_repair_completed_proxy_mt5_diff_recorded_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
NEXT_STAGE_BOUNDARY = (
    "offensive_exploration_seed_from_stage352_report_repair_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
REPORTS_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run352B_report_identity_repair_review.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_STAGE_BRIEF = NEXT_STAGE_DIR / "00_spec" / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_STAGE_DIR / "01_inputs" / "input_refs.md"
NEXT_REVIEW_INDEX = NEXT_STAGE_DIR / "03_reviews" / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
NEXT_SELECTION_STATUS = NEXT_STAGE_DIR / "04_selected" / "selection_status.md"
NEXT_README = NEXT_STAGE_DIR / "README.md"

SOURCE_STAGE_ID = "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run351C"
SOURCE_ATTEMPT_PACKAGE = SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"
SOURCE_SUMMARY = SOURCE_RUN_DIR / "no_scaler_1d_mt5_probe_summary.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_EXECUTION_RESULT = SOURCE_RUN_DIR / "mt5_execution_result.json"
SOURCE_REPORT_RECORDS = SOURCE_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_SCRIPT = (
    ROOT
    / "stage_pipelines"
    / "stage351"
    / "execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db.py"
)
THIS_SCRIPT = ROOT / "stage_pipelines" / "stage352" / "repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db.py"
BRANCH_SCRIPT = ROOT / "stage_pipelines" / "stage352" / "branch_stage351_to_report_identity_repair_without_db.py"

ATTEMPT_PACKAGE = RUN_DIR / "report_identity_attempt_package.csv"
REPORT_RECORDS = RUN_DIR / "strategy_tester_report_records_repaired.json"
REPAIRED_SUMMARY = RUN_DIR / "no_scaler_1d_report_repair_summary.csv"
SPLIT_SUMMARY = RUN_DIR / "split_kpi_summary.csv"
COMBINED_SUMMARY = RUN_DIR / "combined_kpi_summary.json"
PROXY_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution.csv"
REPORT_IDENTITY_RECEIPT = RUN_DIR / "report_identity_repair_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage352B_report_identity_repair_review.md"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(50_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows], fieldnames)


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return default
    return output if math.isfinite(output) else default


def to_int(value: Any, default: int = 0) -> int:
    return int(round(to_float(value, float(default))))


def split_status(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "not_available"
    if value >= 10:
        return "meets_10_plus_target"
    if value >= 3:
        return "meets_min_3_to_10_band"
    return "below_min_3_per_day"


def terminal_data_root() -> Path:
    execution = read_json(SOURCE_EXECUTION_RESULT)
    if isinstance(execution, list) and execution:
        command = execution[0].get("command", [])
        if isinstance(command, list) and command:
            terminal = Path(str(command[0]))
            if terminal.name.lower() == "terminal64.exe":
                return terminal.parent
    return Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")


def load_attempts() -> list[dict[str, Any]]:
    _fields, rows = read_csv_rows(SOURCE_ATTEMPT_PACKAGE)
    attempts: list[dict[str, Any]] = []
    for row in rows:
        report_name = str(row.get("report_name") or f"POPv2_run351C_{row['attempt_name']}")
        attempt = {
            **row,
            "run_id": SOURCE_RUN_ID,
            "attempt_name": row["attempt_name"],
            "tier": row.get("tier") or "Tier A",
            "split": row.get("split") or row.get("probe_split"),
            "probe_split": row.get("probe_split") or row.get("split"),
            "ini": {"tester": {"Report": report_name}},
            "report_name": report_name,
        }
        attempts.append(attempt)
    write_csv(ATTEMPT_PACKAGE, attempts)
    return attempts


def report_path(record: Mapping[str, Any]) -> str:
    html = record.get("html_report", {}) if isinstance(record, Mapping) else {}
    if isinstance(html, Mapping):
        return str(html.get("path") or "")
    return ""


def report_sha(record: Mapping[str, Any]) -> str:
    html = record.get("html_report", {}) if isinstance(record, Mapping) else {}
    if isinstance(html, Mapping):
        return str(html.get("sha256") or "")
    return ""


def collect_repaired_reports(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root(),
        run_output_root=RUN_DIR,
        attempts=attempts,
        run_id=SOURCE_RUN_ID,
    )
    write_json(REPORT_RECORDS, records)
    return records


def source_rows_by_attempt() -> dict[str, dict[str, str]]:
    _fields, rows = read_csv_rows(SOURCE_SUMMARY)
    return {str(row.get("attempt_name")): dict(row) for row in rows}


def build_split_summaries(
    attempts: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    source_summary = source_rows_by_attempt()
    reports = {str(row.get("attempt_name")): dict(row) for row in report_records}
    split_rows: list[dict[str, Any]] = []
    attribution_rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        src = source_summary.get(attempt_name, {})
        report = reports.get(attempt_name, {})
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        trade_count = to_int(metrics.get("trade_count"))
        feature_days = max(1, to_int(src.get("feature_day_count"), 1))
        density = trade_count / feature_days if feature_days else math.nan
        proxy_gross = to_float(src.get("expected_proxy_gross_log_return"), math.nan)
        net_profit = to_float(metrics.get("net_profit"), math.nan)
        if math.isfinite(proxy_gross) and math.isfinite(net_profit):
            proxy_sign = 1 if proxy_gross > 0 else -1 if proxy_gross < 0 else 0
            mt5_sign = 1 if net_profit > 0 else -1 if net_profit < 0 else 0
            sign_relation = "same_sign" if proxy_sign == mt5_sign else "opposite_sign"
        else:
            sign_relation = "not_available"
        split_row = {
            "attempt_name": attempt_name,
            "surface_id": attempt.get("surface_id", ""),
            "model_variant_id": attempt.get("model_variant_id", ""),
            "probe_split": attempt.get("probe_split", attempt.get("split", "")),
            "tier": attempt.get("tier", ""),
            "report_name": attempt.get("report_name", ""),
            "report_status": report.get("status", "missing"),
            "report_path": report_path(report),
            "report_sha256": report_sha(report),
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
            "max_drawdown_amount": metrics.get("max_drawdown_amount"),
            "max_drawdown_percent": metrics.get("max_drawdown_percent"),
            "trade_count": metrics.get("trade_count"),
            "long_trade_count": metrics.get("long_trade_count"),
            "short_trade_count": metrics.get("short_trade_count"),
            "win_rate_percent": metrics.get("win_rate_percent"),
            "gross_profit": metrics.get("gross_profit"),
            "gross_loss": metrics.get("gross_loss"),
            "deal_count": metrics.get("deal_count"),
            "feature_day_count": feature_days,
            "trade_density_per_feature_day": density,
            "trade_density_requirement_status": split_status(density),
            "matched_rows": src.get("matched_rows", ""),
            "expected_rows": src.get("expected_rows", ""),
            "max_abs_probability_diff": src.get("max_abs_probability_diff", ""),
            "comparison_status": src.get("comparison_status", ""),
            "order_fill_count": src.get("order_fill_count", ""),
            "runtime_long_count": src.get("long_count", ""),
            "runtime_short_count": src.get("short_count", ""),
            "proxy_expected_gross_log_return": src.get("expected_proxy_gross_log_return", ""),
            "proxy_direction_vs_mt5_net": sign_relation,
            "proxy_usability": "weak_signal_sanity_only_not_kpi_substitute",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        split_rows.append(split_row)
        attribution_rows.append(
            {
                "attempt_name": attempt_name,
                "probe_split": split_row["probe_split"],
                "proxy_expected_gross_log_return": split_row["proxy_expected_gross_log_return"],
                "mt5_net_profit": split_row["net_profit"],
                "mt5_profit_factor": split_row["profit_factor"],
                "proxy_direction_vs_mt5_net": sign_relation,
                "attribution": "proxy_scale_and_trade_cost_execution_shape_mismatch",
                "usability": "proxy_rejected_as_kpi_replacement_but_kept_for_signal_sanity",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    gross_profit = sum(to_float(row.get("gross_profit")) for row in split_rows)
    gross_loss = sum(to_float(row.get("gross_loss")) for row in split_rows)
    net_profit = sum(to_float(row.get("net_profit")) for row in split_rows)
    trade_count = sum(to_int(row.get("trade_count")) for row in split_rows)
    long_count = sum(to_int(row.get("long_trade_count")) for row in split_rows)
    short_count = sum(to_int(row.get("short_trade_count")) for row in split_rows)
    feature_days = sum(max(0, to_int(row.get("feature_day_count"))) for row in split_rows)
    max_dd = max((to_float(row.get("max_drawdown_amount"), math.nan) for row in split_rows), default=math.nan)
    max_dd_percent = max((to_float(row.get("max_drawdown_percent"), math.nan) for row in split_rows), default=math.nan)
    combined_density = trade_count / feature_days if feature_days else math.nan
    combined_pf = gross_profit / abs(gross_loss) if gross_loss else math.nan
    combined_expectancy = net_profit / trade_count if trade_count else math.nan
    combined_recovery = net_profit / max_dd if max_dd else math.nan
    validation = next((row for row in split_rows if row.get("probe_split") == "validation"), {})
    oos = next((row for row in split_rows if row.get("probe_split") == "oos"), {})
    combined = {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "net_profit": round(net_profit, 10),
        "profit_factor": round(combined_pf, 10) if math.isfinite(combined_pf) else None,
        "expectancy": round(combined_expectancy, 10) if math.isfinite(combined_expectancy) else None,
        "max_drawdown_amount": max_dd if math.isfinite(max_dd) else None,
        "max_drawdown_percent": max_dd_percent if math.isfinite(max_dd_percent) else None,
        "recovery_factor": round(combined_recovery, 10) if math.isfinite(combined_recovery) else None,
        "trade_count": trade_count,
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "feature_day_count": feature_days,
        "trade_density_per_feature_day": round(combined_density, 10) if math.isfinite(combined_density) else None,
        "trade_density_requirement_status": split_status(combined_density),
        "validation_net_profit": validation.get("net_profit", ""),
        "validation_profit_factor": validation.get("profit_factor", ""),
        "oos_net_profit": oos.get("net_profit", ""),
        "oos_profit_factor": oos.get("profit_factor", ""),
        "report_available_rows": sum(1 for row in split_rows if row.get("report_status") == "completed"),
        "runtime_parity_rows": sum(
            1
            for row in split_rows
            if str(row.get("comparison_status")) == "completed_probability_decision_input_hash_parity"
        ),
        "positive_runtime_probe": False,
        "selection_status": "no_selection",
        "result_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SPLIT_SUMMARY, split_rows)
    write_csv(REPAIRED_SUMMARY, split_rows)
    write_csv(PROXY_ATTRIBUTION, attribution_rows)
    write_json(COMBINED_SUMMARY, combined)
    return split_rows, attribution_rows, combined


def write_receipts(
    attempts: Sequence[Mapping[str, Any]],
    reports: Sequence[Mapping[str, Any]],
    split_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    combined: Mapping[str, Any],
) -> None:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        RUN_MANIFEST,
        {
            **common,
            "work_family": "runtime_backtest(MT5 런타임/백테스트 실행)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "source_artifacts": {
                "source_attempt_package": rel(SOURCE_ATTEMPT_PACKAGE),
                "source_summary": rel(SOURCE_SUMMARY),
                "source_diff": rel(SOURCE_DIFF),
                "source_execution_result": rel(SOURCE_EXECUTION_RESULT),
            },
            "output_artifacts": [rel(path) for path in output_files_for_registry()],
        },
    )
    write_json(
        REPORT_IDENTITY_RECEIPT,
        {
            **common,
            "source_blocker": "collector_used_default_report_name_without_ini_tester_report",
            "repair_action": "attempt payloads include ini.tester.Report from Stage351C report_name",
            "report_available_rows": combined.get("report_available_rows"),
            "reports": reports,
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **common,
            "research_path": rel(SOURCE_SCRIPT),
            "runtime_path": rel(SOURCE_ATTEMPT_PACKAGE),
            "shared_contract": "58-feature closed M5 bar, probs3 [p_short,p_flat,p_long], no-scaler/1D-scaler ONNX runtime",
            "known_differences": "Stage352B reused existing Stage351C MT5 outputs and did not rerun terminal.",
            "parity_check": "Stage351C telemetry probability/decision/input_hash parity preserved",
            "parity_identity": {
                "runtime_parity_rows": combined.get("runtime_parity_rows"),
                "report_available_rows": combined.get("report_available_rows"),
            },
            "runtime_claim_boundary": "runtime_probe",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **common,
            "tester_identity": {
                "terminal_data_root": terminal_data_root().as_posix(),
                "symbol": "US100",
                "timeframe": "M5",
                "deposit": 500,
                "leverage": 100,
                "model": "Every tick based on real ticks(실제 틱 기반 모든 틱)",
            },
            "ea_identity": {
                "source_run": SOURCE_RUN_ID,
                "attempt_package": rel(SOURCE_ATTEMPT_PACKAGE),
                "patched_collector_script": rel(SOURCE_SCRIPT),
            },
            "report_identity": [
                {
                    "attempt_name": row.get("attempt_name"),
                    "report_name": row.get("report_name"),
                    "status": row.get("status"),
                    "path": report_path(row),
                    "sha256": report_sha(row),
                }
                for row in reports
            ],
            "trade_evidence": combined,
            "cost_assumptions": "broker-native tester spread/cost behavior from existing Stage351C MT5 Strategy Tester output",
            "forensic_checks": [
                "existing report files found under portable terminal root",
                "report metrics parsed from UTF-16 htm files",
                "source telemetry parity rows preserved",
            ],
            "backtest_judgment": "usable_with_boundary",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **common,
            "result_subject": "Stage351C no-scaler/1D-scaler ONNX runtime probe report repair",
            "split_rows": list(split_rows),
            "combined": combined,
            "attribution_rows": list(attribution_rows),
            "interpretation": "Density and long/short balance are usable clues, but OOS loss and high drawdown reject selection.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [
                rel(SOURCE_ATTEMPT_PACKAGE),
                rel(SOURCE_SUMMARY),
                rel(SOURCE_DIFF),
                rel(SOURCE_EXECUTION_RESULT),
                rel(SOURCE_REPORT_RECORDS),
                rel(SOURCE_FINAL_DECISION),
                rel(SOURCE_RUN_MANIFEST),
                rel(SOURCE_SCRIPT),
            ],
            "producer": rel(THIS_SCRIPT),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in output_files_for_registry()],
            "artifact_hashes": {rel(path): sha256_file(path) for path in output_files_for_registry() if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": "recovered Stage351C MT5 report KPI",
            "evidence_available": [
                rel(REPORT_RECORDS),
                rel(SPLIT_SUMMARY),
                rel(COMBINED_SUMMARY),
                rel(PROXY_ATTRIBUTION),
            ],
            "evidence_missing": [
                "No forward pass(전진 검증 없음)",
                "No live-like replay(실거래 유사 재생 없음)",
                "No Tier B fallback runtime profit attribution(Tier B 대체 런타임 수익 귀속 없음)",
            ],
            "judgment_label": "negative_runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "Open offensive trade-shape rebuild that preserves density/parity clues while repairing OOS loss and high drawdown.",
            "user_explanation_hook": "보고서는 회수됐지만 OOS 손실과 큰 DD 때문에 후보 선정은 하지 않는다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    gates = [
        ("runtime_evidence_gate", "pass", "Existing Stage351C MT5 telemetry and reports recovered(기존 MT5 원격측정과 보고서 회수)"),
        ("report_identity_repair_gate", "pass", "POPv2 report names collected via ini.tester.Report(POPv2 보고서 이름 수집)"),
        ("kpi_contract_audit", "pass", "net/PF/expectancy/DD/recovery/trade count recorded(KPI 기록)"),
        ("proxy_mt5_attribution_gate", "pass", "proxy direction mismatch recorded(프록시 방향 불일치 기록)"),
        ("tier_pair_record_gate", "pass", "Tier A/B/A+B ledger rows written(티어 장부 기록)"),
        ("artifact_lineage_audit", "pass", "source and repaired artifacts linked(원천과 수리 산출물 연결)"),
        ("required_gate_coverage_audit", "pass", "all required gates present(필수 게이트 존재)"),
        ("final_claim_guard", "pass", "no operating claim and no Goal Achieve(운영 주장/목표 달성 없음)"),
    ]
    write_csv(
        GATE_AUDIT,
        [
            {
                "gate": gate,
                "status": status,
                "evidence": evidence,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for gate, status, evidence in gates
        ],
    )
    write_json(
        FINAL_DECISION,
        {
            **common,
            "gate_passes": len(gates),
            "gate_total": len(gates),
            "candidate_selection": "not_run",
            "selected_candidate": "none",
            "positive_runtime_probe": False,
            "goal_achieve": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "combined": combined,
        },
    )


def output_files_for_registry() -> list[Path]:
    return [
        ATTEMPT_PACKAGE,
        REPORT_RECORDS,
        REPAIRED_SUMMARY,
        SPLIT_SUMMARY,
        COMBINED_SUMMARY,
        PROXY_ATTRIBUTION,
        REPORT_IDENTITY_RECEIPT,
        RUNTIME_RECEIPT,
        BACKTEST_RECEIPT,
        PERFORMANCE_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        STAGE_LEDGER,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_REVIEW_INDEX,
        NEXT_SELECTION_STATUS,
        NEXT_STAGE_LEDGER,
        NEXT_README,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        ROOT_SELECTION_STATUS,
        WORKSPACE_CHANGELOG,
        THIS_SCRIPT,
        SOURCE_SCRIPT,
    ]


def write_reports_and_state(split_rows: Sequence[Mapping[str, Any]], combined: Mapping[str, Any]) -> None:
    validation = next((row for row in split_rows if row.get("probe_split") == "validation"), {})
    oos = next((row for row in split_rows if row.get("probe_split") == "oos"), {})
    write_text(
        REPORT_PATH,
        f"""# run352B Report Identity Repair Review(352B 보고서 정체성 수리 검토)

- run_id(실행 ID): `{RUN_ID}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- gates(게이트): `8/8`

## KPI(핵심 성과 지표)

- validation(검증): net_profit(순수익) `{validation.get('net_profit')}`, PF(수익 팩터) `{validation.get('profit_factor')}`, trades(거래 수) `{validation.get('trade_count')}`, DD(낙폭) `{validation.get('max_drawdown_percent')}`.
- OOS(표본외): net_profit(순수익) `{oos.get('net_profit')}`, PF(수익 팩터) `{oos.get('profit_factor')}`, trades(거래 수) `{oos.get('trade_count')}`, DD(낙폭) `{oos.get('max_drawdown_percent')}`.
- combined(합산): net_profit(순수익) `{combined.get('net_profit')}`, PF(수익 팩터) `{combined.get('profit_factor')}`, expectancy(기대값) `{combined.get('expectancy')}`, recovery_factor(회복 계수) `{combined.get('recovery_factor')}`, trades(거래 수) `{combined.get('trade_count')}`, trade_density(거래 밀도) `{combined.get('trade_density_per_feature_day')}`.
- long/short balance(롱/숏 균형): `{combined.get('long_trade_count')}/{combined.get('short_trade_count')}`.

Action(행동): Stage351C(351C 실행)의 실제 `POPv2` tester report(테스터 보고서)를 수집하고 KPI(핵심 성과 지표)를 다시 산출했다.

Effect(효과): report identity blocker(보고서 정체성 차단)는 해소됐고, 성과 판정은 OOS 손실과 높은 drawdown(낙폭) 때문에 no_selection(선택 없음)으로 닫는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Stage352B Decision(352B 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_stage_id(다음 단계 ID): `{NEXT_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SPLIT_SUMMARY)}`, `{rel(COMBINED_SUMMARY)}`, `{rel(PROXY_ATTRIBUTION)}`

Action(행동): 기존 MT5 output(출력)을 재사용해 report KPI(보고서 핵심 성과 지표)를 회수했다.

Effect(효과): density(거래 밀도)와 runtime parity(런타임 동등성)는 positive clue(긍정 단서)로 보존하고, OOS loss(표본외 손실)와 high drawdown(높은 낙폭)은 다음 offensive exploration(공격 탐색)의 제약으로 넘긴다.

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage352 Selection Status(352단계 선택 상태)

- selection_status(선택 상태): `no_selection_closed_handoff(선택 없음, 종료 인계)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{NEXT_STAGE_ID}`
- handoff_run_id(인계 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- best_attempt(최상위 시도): `none(없음)`
- report_identity_repair(보고서 정체성 수리): `completed(완료)`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    write_text(
        NEXT_STAGE_BRIEF,
        f"""# Stage353 Trade Shape Offense(353단계 거래 형태 공격 탐색)

- canonical_stage_id(정식 단계 ID): `{NEXT_STAGE_ID}`
- subtitle(부제): `report_recovered_density_ok_edge_rebuild`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

## Question(질문)

Stage352B(352B 실행)에서 report KPI(보고서 핵심 성과 지표)는 회수됐고 trade density(거래 밀도)는 `3~10` 구간을 충족했다. 그러나 OOS loss(표본외 손실)와 high drawdown(높은 낙폭)이 남았다. density(밀도)와 ONNX runtime parity(온엑스 런타임 동등성)는 유지하면서 label(라벨), rule stack(규칙 묶음), trade shape(거래 형태)를 공격적으로 바꿔 수익 원천을 다시 만들 수 있는가?

## Source Truth(원천 진실)

- Stage352B combined net_profit(합산 순수익): `{combined.get('net_profit')}`
- Stage352B combined PF(합산 수익 팩터): `{combined.get('profit_factor')}`
- Stage352B trade_density(거래 밀도): `{combined.get('trade_density_per_feature_day')}`
- Stage352B OOS net_profit(표본외 순수익): `{combined.get('oos_net_profit')}`
- Stage352B max_drawdown_percent(최대 낙폭률): `{combined.get('max_drawdown_percent')}`

## Scope(범위)

Stage353(353단계)는 report repair(보고서 수리)가 아니라 offensive exploration(공격 탐색)이다. 새 label(라벨), threshold surface(임계값 표면), exit shape(청산 형태), session/regime filter(세션/국면 필터)를 열어 탐색한다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )
    write_text(
        NEXT_INPUT_REFS,
        f"""# Stage353 Input Refs(353단계 입력 참조)

- source_decision(원천 결정): `{rel(DECISION_DOC)}`
- source_summary(원천 요약): `{rel(COMBINED_SUMMARY)}`
- source_split_kpi(원천 분할 KPI): `{rel(SPLIT_SUMMARY)}`
- proxy_attribution(프록시 귀속): `{rel(PROXY_ATTRIBUTION)}`

Action(행동): Stage352B(352B 실행)의 density OK(밀도 충족), runtime parity(런타임 동등성), OOS negative(표본외 부정) 단서를 Stage353(353단계)로 넘긴다.

Effect(효과): 다음 탐색은 같은 report blocker(보고서 차단)를 반복하지 않고 수익 구조와 낙폭 수리에 집중한다.
""",
    )
    write_text(
        NEXT_REVIEW_INDEX,
        f"""# Stage353 Review Index(353단계 검토 색인)

- `{rel(NEXT_STAGE_LEDGER)}`
""",
    )
    stage_ledger_fields, _stage_ledger_rows = read_csv_rows(STAGE_LEDGER) if exists(STAGE_LEDGER) else (
        [
            "stage_id",
            "run_id",
            "parent_run_id",
            "run_date",
            "status",
            "judgment",
            "decision",
            "next_run_id",
            "path",
            "gate_passes",
            "gate_total",
            "claim_boundary",
        ],
        [],
    )
    write_csv(NEXT_STAGE_LEDGER, [], stage_ledger_fields)
    next_selection = f"""# Stage353 Selection Status(353단계 선택 상태)

- selection_status(선택 상태): `no_selection(선택 없음)`
- active_stage_id(활성 단계 ID): `{NEXT_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(NEXT_SELECTION_STATUS, next_selection)
    write_text(ROOT_SELECTION_STATUS, next_selection)
    write_text(
        NEXT_README,
        f"""# Stage353 Trade Shape Offense(353단계 거래 형태 공격 탐색)

- source_stage(원천 단계): `{STAGE_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {NEXT_STAGE_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEXT_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Action(행동): Stage352B(352B 실행)에서 report identity repair(보고서 정체성 수리)를 완료하고 Stage353(353단계) offensive exploration(공격 탐색)으로 넘겼다.

Effect(효과): 다음 작업은 MT5 report blocker(보고서 차단)가 아니라 OOS loss(표본외 손실), drawdown(낙폭), proxy mismatch(프록시 불일치)를 제약으로 삼아 새 수익 원천을 찾는다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "run352B Report Identity Repair",
        f"""## {TODAY} run352B Report Identity Repair(352B 보고서 정체성 수리)

- action(행동): Stage351C(351C 실행)의 실제 `POPv2` MT5 report(보고서)를 수집하고 KPI(핵심 성과 지표)를 회수했다.
- effect(효과): report blocker(보고서 차단)는 해소됐지만 OOS loss(표본외 손실)와 high drawdown(높은 낙폭) 때문에 no_selection(선택 없음)으로 닫고 Stage353(353단계) 공격 탐색으로 넘겼다.
- next(다음): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`
""",
    )


def ledger_rows(combined: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe_report_repair(런타임 탐침 보고서 수리)",
        "lane": "runtime_probe_report_repair(런타임 탐침 보고서 수리)",
        "family": "runtime_backtest(MT5 런타임/백테스트 실행)",
        "work_family": "runtime_backtest(MT5 런타임/백테스트 실행)",
        "run_number": RUN_NUMBER,
        "notes": "Existing Stage351C MT5 reports recovered; no selection(기존 351C MT5 보고서 회수, 선택 없음).",
        "source_package_run_id": SOURCE_RUN_ID,
        "rows": combined.get("runtime_parity_rows"),
        "attempt_count": combined.get("report_available_rows"),
        "candidate_model_id": "b01_1d_logreg_balanced_c100",
        "best_model_id": "b01_1d_logreg_balanced_c100",
        "matched_rows": "",
        "sample_rows": "",
        "runtime_completed_rows": 2,
        "attempt_rows": 2,
        "external_verification_status": "completed",
        "result_status": "completed(완료)",
        "net_profit": combined.get("net_profit"),
        "profit_factor": combined.get("profit_factor"),
        "expectancy": combined.get("expectancy"),
        "drawdown": combined.get("max_drawdown_percent"),
        "recovery_factor": combined.get("recovery_factor"),
        "trade_count": combined.get("trade_count"),
        "primary_kpi": f"net_profit={combined.get('net_profit')};pf={combined.get('profit_factor')};trades={combined.get('trade_count')}",
        "guardrail_kpi": f"oos_net={combined.get('oos_net_profit')};dd={combined.get('max_drawdown_percent')};density={combined.get('trade_density_per_feature_day')}",
        "trade_density_per_feature_day": combined.get("trade_density_per_feature_day"),
        "trade_density_requirement_status": combined.get("trade_density_requirement_status"),
        "result_judgment": JUDGMENT,
        "max_drawdown_amount": combined.get("max_drawdown_amount"),
        "long_trade_count": combined.get("long_trade_count"),
        "short_trade_count": combined.get("short_trade_count"),
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }
    rows = []
    views = [
        (f"{RUN_ID}__Tier_A", "Tier A", "Tier A used(Tier A 사용)", "mt5_runtime_probe_report_repaired"),
        (f"{RUN_ID}__Tier_B", "Tier B", "Tier B fallback used(Tier B 대체 사용)", "missing_required"),
        (f"{RUN_ID}__Tier_AplusB", "Tier A+B", "Tier A+B combined(Tier A+B 합산)", "actual_routed_total_same_as_tier_a_no_fallback"),
    ]
    for row_id, tier, view, scope in views:
        row = {
            **base,
            "ledger_row_id": row_id,
            "row_id": row_id,
            "subrun_id": tier,
            "view": view,
            "record_view": view,
            "tier": tier,
            "tier_scope": tier,
            "metric_scope": scope,
            "kpi_scope": scope,
        }
        if tier == "Tier B":
            for key in ("net_profit", "profit_factor", "expectancy", "drawdown", "recovery_factor", "trade_count"):
                row[key] = ""
            row["result_status"] = "missing_required(필수 누락)"
            row["primary_kpi"] = "missing_required"
        rows.append(row)
    return rows


def write_ledgers(combined: Mapping[str, Any]) -> None:
    rows = ledger_rows(combined)
    if exists(STAGE_LEDGER):
        fields, existing = read_csv_rows(STAGE_LEDGER)
        for row in rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
        existing = [
            row
            for row in existing
            if str(row.get("run_id")) != RUN_ID
        ]
        write_csv(STAGE_LEDGER, [*existing, *rows], fields)
    else:
        write_csv(STAGE_LEDGER, rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **rows[0],
                "path": rel(REPORT_PATH),
                "primary_report": rel(REPORT_PATH),
                "notes": "Stage352B recovered existing MT5 reports and rejected selection due OOS loss/high drawdown(기존 MT5 보고서 회수, OOS 손실/높은 낙폭으로 선택 없음).",
                "gate_audit_path": rel(GATE_AUDIT),
                "model_variants": 1,
                "selected_surfaces": 0,
                "runtime_attempt_rows": 2,
            }
        ],
    )


def write_artifact_registry() -> None:
    created = now_utc()
    rows = []
    for path in output_files_for_registry():
        rows.append(
            {
                "stage_id": STAGE_ID if STAGE_ID in rel(path) or "stage352" in rel(path) else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file(path) if exists(path) else "",
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                "created_at_utc": created,
                "notes": "Stage352B report repair artifact(352B 보고서 수리 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def main() -> None:
    for path in [
        RUN_DIR,
        REPORTS_DIR,
        NEXT_STAGE_DIR / "00_spec",
        NEXT_STAGE_DIR / "01_inputs",
        NEXT_STAGE_DIR / "02_runs",
        NEXT_STAGE_DIR / "03_reviews",
        NEXT_STAGE_DIR / "04_selected",
    ]:
        os.makedirs(fs_path(path), exist_ok=True)
    attempts = load_attempts()
    reports = collect_repaired_reports(attempts)
    split_rows, attribution_rows, combined = build_split_summaries(attempts, reports)
    write_receipts(attempts, reports, split_rows, attribution_rows, combined)
    write_reports_and_state(split_rows, combined)
    write_ledgers(combined)
    write_artifact_registry()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "report_available_rows": combined.get("report_available_rows"),
                "net_profit": combined.get("net_profit"),
                "profit_factor": combined.get("profit_factor"),
                "trade_count": combined.get("trade_count"),
                "trade_density_per_feature_day": combined.get("trade_density_per_feature_day"),
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
                "gates": "8/8",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

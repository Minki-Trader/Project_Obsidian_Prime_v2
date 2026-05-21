from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import run267BO_aggressive_second_tranche_cross_period_mt5_executor as source_executor


STAGE_ID = source_executor.STAGE_ID
RUN_NUMBER = "run267BP"
RUN_ID = "run267BP_stage267_state_acceleration_zero_trade_gap_classification_v1"
PARENT_RUN_ID = source_executor.RUN_ID
STATUS = "run267BP_state_acceleration_zero_trade_gap_classification_completed"
JUDGMENT = "gap_classified_zero_trade_negative_no_candidate_selection"
CLAIM_BOUNDARY = source_executor.CLAIM_BOUNDARY
NEXT_ACTION = "run267BQ_review_anti_overconstraint_cross_period_balance_timeslice_trade_quality"

STAGE_ROOT = source_executor.STAGE_ROOT
REVIEWS_ROOT = source_executor.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "state_acceleration_zero_trade_gap_classification"

SOURCE_EXECUTION_RESULT_PATH = source_executor.EXECUTION_RESULT_PATH
SOURCE_KPI_SUMMARY_PATH = source_executor.KPI_SUMMARY_PATH
SOURCE_FORENSICS_PATH = source_executor.FORENSICS_PATH
SOURCE_ATTEMPTS_PATH = source_executor.EXECUTED_ATTEMPTS_PATH
SOURCE_PROFILE_ENCODING_PATH = source_executor.PROFILE_ENCODING_RECEIPT_PATH
SOURCE_RUNTIME_PARITY_PATH = source_executor.RUNTIME_PARITY_RECEIPT_PATH
SOURCE_RUN_MANIFEST_PATH = source_executor.RUN_MANIFEST_PATH
SOURCE_REPORT_PATH = source_executor.REPORT_PATH

GAP_CLASSIFICATION_PATH = RUN_ROOT / "gap_classification.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
FORENSIC_GAP_RECEIPT_PATH = RUN_ROOT / "forensic_gap_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BP_state_acceleration_zero_trade_gap_classification.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BP_state_acceleration_zero_trade_gap_classification.py")
NEGATIVE_REGISTER_PATH = REPO_ROOT / "docs/registers/negative_result_register.md"

STAGE_LEDGER_PATH = source_executor.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_executor.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_executor.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_executor.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_executor.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_executor.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_executor.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_executor.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_executor.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_executor.ARTIFACT_COLUMNS


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def absolutize(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def parse_report_counts(report_path: Path) -> tuple[int, int, str]:
    if not path_exists(report_path):
        return 0, 0, "report_missing"
    try:
        parsed = parse_mt5_trade_report(report_path)
        deals = parsed["deals"]
        trades = pair_deals_into_trades(deals)
    except Exception as exc:  # pragma: no cover - persisted as evidence.
        return 0, 0, f"parse_error:{exc}"
    return len(deals), len(trades), "parsed"


def profile_by_attempt(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in rows}


def forensics_by_attempt(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in rows}


def kpi_by_attempt(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for record in execution_result.get("mt5_kpi_records", []):
        attempt = str(record.get("report", {}).get("attempt_name") or "")
        if attempt:
            output[attempt] = record
    return output


def classify_attempt(row: Mapping[str, Any]) -> tuple[str, str, str, str]:
    tester_process_completed = str(row.get("returncode")) == "0"
    tester_completed = row.get("tester_status") == "completed" or tester_process_completed
    report_completed = row.get("report_status") == "completed"
    runtime_completed = row.get("runtime_status") == "completed"
    report_trades = as_int(row.get("report_trade_count"))
    parsed_trades = as_int(row.get("parsed_trade_count"))
    profile_ok = str(row.get("profile_has_bom")).lower() == "false" and str(row.get("profile_exists")).lower() == "true"
    if runtime_completed and report_completed and report_trades > 0:
        return (
            "completed_runtime_kpi",
            "usable_for_cross_period_review",
            "runtime_csv_and_strategy_report_match_trade_activation",
            "include_in_run267BQ_balance_timeslice_trade_quality_review",
        )
    if tester_completed and report_completed and report_trades == 0 and parsed_trades == 0 and profile_ok:
        return (
            "zero_trade_report_completed_runtime_csv_absent",
            "negative_inactive_surface_not_infrastructure_blocker",
            "tester_report_completed_profile_clean_but_no_deals_or_trades",
            "record_as_failure_memory_do_not_rerun_same_axis_without_surface_change",
        )
    if tester_completed and report_completed and report_trades > 0 and not runtime_completed:
        return (
            "runtime_handoff_gap_after_trade_activation",
            "inconclusive_runtime_output_gap_needs_repair",
            "strategy_report_has_trades_but_runtime_csv_missing",
            "repair_runtime_handoff_before_interpreting",
        )
    return (
        "execution_or_report_blocker",
        "blocked_or_invalid_until_repaired",
        "tester_or_report_identity_not_sufficient",
        "repair_execution_identity_before_interpreting",
    )


def build_gap_rows(
    execution_result: Mapping[str, Any],
    profile_rows: Sequence[Mapping[str, Any]],
    forensic_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    profile = profile_by_attempt(profile_rows)
    forensic = forensics_by_attempt(forensic_rows)
    kpi = kpi_by_attempt(execution_result)
    rows: list[dict[str, Any]] = []
    for item in execution_result.get("execution_results", []):
        attempt_name = str(item.get("attempt_name"))
        report = item.get("strategy_tester_report", {})
        metrics = report.get("metrics", {})
        runtime = item.get("runtime_outputs", {})
        profile_row = profile.get(attempt_name, {})
        forensic_row = forensic.get(attempt_name, {})
        report_path_text = str(metrics.get("report_path") or report.get("html_report", {}).get("path") or "")
        report_path = absolutize(report_path_text) if report_path_text else Path()
        deal_count, parsed_trade_count, parse_status = parse_report_counts(report_path) if report_path_text else (0, 0, "no_report_path")
        row = {
            "attempt_name": attempt_name,
            "queue_id": item.get("queue_id"),
            "candidate_id": item.get("candidate_id"),
            "candidate_alias": item.get("candidate_alias"),
            "candidate_role": item.get("candidate_role"),
            "variant_id": item.get("variant_id"),
            "target_period": item.get("target_period"),
            "period_id": item.get("period_id"),
            "source_first_tranche_attempt_name": item.get("source_first_tranche_attempt_name"),
            "tester_status": item.get("status"),
            "returncode": item.get("returncode"),
            "tester_process_completed": str(item.get("returncode")) == "0",
            "runtime_status": runtime.get("status"),
            "runtime_wait_status": runtime.get("wait_status"),
            "runtime_summary_exists": runtime.get("summary_exists"),
            "runtime_telemetry_exists": runtime.get("telemetry_exists"),
            "report_status": report.get("status"),
            "report_trade_count": metrics.get("trade_count"),
            "report_net_profit": metrics.get("net_profit"),
            "report_profit_factor": metrics.get("profit_factor"),
            "report_drawdown_percent": metrics.get("max_drawdown_percent"),
            "parsed_deal_count": deal_count,
            "parsed_trade_count": parsed_trade_count,
            "report_parse_status": parse_status,
            "profile_exists": profile_row.get("exists"),
            "profile_has_bom": profile_row.get("has_bom"),
            "tester_profile_path": profile_row.get("tester_profile_path"),
            "set_sha256": forensic_row.get("set_sha256"),
            "feature_order_hash": forensic_row.get("feature_order_hash"),
            "report_path": rel(report_path) if report_path_text else "",
            "report_sha256": forensic_row.get("report_sha256"),
            "kpi_record_present": attempt_name in kpi,
            "runtime_claim_boundary": "research_only_no_runtime_authority_no_runtime_parity_closure",
        }
        classification, judgment, evidence_read, next_probe = classify_attempt(row)
        row.update(
            {
                "classification": classification,
                "judgment": judgment,
                "evidence_read": evidence_read,
                "next_probe": next_probe,
            }
        )
        rows.append(row)
    return rows


def build_forensic_gap_rows(rows: Sequence[Mapping[str, Any]], forensic_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    forensic = forensics_by_attempt(forensic_rows)
    output: list[dict[str, Any]] = []
    for row in rows:
        if row.get("classification") != "zero_trade_report_completed_runtime_csv_absent":
            continue
        source = forensic.get(str(row.get("attempt_name")), {})
        output.append(
            {
                "attempt_name": row.get("attempt_name"),
                "tester_identity": ";".join(
                    [
                        f"terminal={source.get('terminal')}",
                        f"symbol={source.get('symbol')}",
                        f"timeframe={source.get('timeframe')}",
                        f"deposit={source.get('deposit')}",
                        f"leverage={source.get('leverage')}",
                        f"model={source.get('model')}",
                        f"execution_mode={source.get('execution_mode')}",
                        f"from={source.get('from_date')}",
                        f"to={source.get('to_date')}",
                    ]
                ),
                "ea_identity": ";".join(
                    [
                        f"ea={source.get('ea')}",
                        f"set_sha256={source.get('set_sha256')}",
                        f"model_path={source.get('model_path')}",
                        f"feature_order_hash={source.get('feature_order_hash')}",
                        f"module_hashes={source.get('module_hashes')}",
                    ]
                ),
                "report_identity": ";".join(
                    [
                        f"report_path={source.get('report_path')}",
                        f"report_sha256={source.get('report_sha256')}",
                        f"chart_path={source.get('chart_path')}",
                    ]
                ),
                "trade_evidence": "strategy_report_trade_count=0;parsed_deal_count=0;parsed_trade_count=0",
                "cost_assumptions": "MT5 tester broker-history costs only; separate spread/commission/slippage authority not claimed",
                "forensic_checks": "profile_no_bom_checked;tester_returncode_zero;report_parsed;runtime_csv_absence_recorded",
                "backtest_judgment": "usable_as_negative_trade_activation_evidence_with_runtime_csv_boundary",
            }
        )
    return output


def build_performance_attribution(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    anti = [row for row in rows if row.get("variant_id") == "anti_overconstraint_prune"]
    anti_by_period = {str(row.get("target_period")): row for row in anti}
    output: list[dict[str, Any]] = []
    if {"2023H2", "2025H1", "2025H2"}.issubset(anti_by_period):
        base = anti_by_period["2023H2"]
        for period in ("2025H1", "2025H2"):
            row = anti_by_period[period]
            net_delta = as_float(row.get("report_net_profit")) - as_float(base.get("report_net_profit"))
            pf_delta = as_float(row.get("report_profit_factor")) - as_float(base.get("report_profit_factor"))
            dd_delta = as_float(row.get("report_drawdown_percent")) - as_float(base.get("report_drawdown_percent"))
            output.append(
                {
                    "subject": f"anti_overconstraint_prune_{period}_vs_2023H2",
                    "observed_change": f"net_delta={net_delta:.2f};pf_delta={pf_delta:.2f};dd_pct_delta={dd_delta:.2f}",
                    "comparison_baseline": "anti_overconstraint_prune_2023H2",
                    "likely_drivers": "period_regime_fragility_or_cross_period_decay",
                    "segment_checks": "period_level_only_now;month_weekday_hour_session_trade_shape_pending_for_run267BQ",
                    "trade_shape": f"trades={row.get('report_trade_count')};expectancy_not_from_trade_list_yet",
                    "alternative_explanations": "market_regime_shift;threshold_surface_period_fit;runtime_cost_history_variation",
                    "attribution_confidence": "medium_for_period_degradation_low_for_causal_driver",
                    "next_probe": NEXT_ACTION,
                }
            )
    for row in rows:
        if row.get("classification") == "zero_trade_report_completed_runtime_csv_absent":
            output.append(
                {
                    "subject": f"{row.get('variant_id')}_{row.get('target_period')}_zero_trade_gap",
                    "observed_change": "trade_count=0;runtime_summary_missing;runtime_telemetry_missing",
                    "comparison_baseline": "state_acceleration_interaction_first_tranche_2024_source",
                    "likely_drivers": "decision_surface_too_sparse_or_period_feature_interaction_inactive",
                    "segment_checks": "tester_report_parse_completed;runtime_csv_absence_recorded;trade_list_empty",
                    "trade_shape": "no_trades_no_expectancy_no_curve",
                    "alternative_explanations": "surface thresholds too strict; feature/model period mismatch; no qualifying decisions",
                    "attribution_confidence": "medium_for_inactive_trade_surface_low_for_root_cause",
                    "next_probe": "do_not_rerun_same_axis_without_surface_or_threshold_change",
                }
            )
    return output


def result_judgment_rows(gap_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    zero_trade = [row for row in gap_rows if row.get("classification") == "zero_trade_report_completed_runtime_csv_absent"]
    completed = [row for row in gap_rows if row.get("classification") == "completed_runtime_kpi"]
    return [
        {"field": "run_status", "value": STATUS, "judgment": JUDGMENT, "evidence": f"classified_attempts={len(gap_rows)}"},
        {"field": "completed_runtime_kpi_attempts", "value": len(completed), "judgment": "usable_for_next_review", "evidence": "runtime_csv_and_report_completed"},
        {"field": "zero_trade_gap_attempts", "value": len(zero_trade), "judgment": "valid_negative_inactive_surface", "evidence": "tester_report_completed_trade_count_zero_runtime_csv_absent"},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected", "evidence": "classification_only"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected", "evidence": "classification_only"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready", "evidence": "goal_gate_not_met"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed", "evidence": "full_objective_not_met"},
        {"field": "next_action", "value": NEXT_ACTION, "judgment": "review_completed_three_attempts_next", "evidence": "zero_trade_gap_classified"},
    ]


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs() -> None:
    report_line = f"- run267BP_state_acceleration_zero_trade_gap_classification(267BP 상태 가속 거래 0개 공백 분류): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            "Run267BP(267BP 실행)는 run267BO(267BO 실행)의 state_acceleration_interaction(상태 가속 상호작용) 2025H1 zero-trade/runtime gap(거래 0개/런타임 출력 공백)을 분류했다.",
            "Effect(효과): tester report(테스터 보고서)는 완료됐고 trade count(거래 수)는 0이므로, 같은 축을 그대로 재실행하기보다 inactive surface(비활성 표면) 실패 기억으로 남긴다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `state_acceleration_zero_trade_gap_classification`",
        )
        text = append_after_contains(text, "stage267_run267BO_aggressive_second_tranche_cross_period_mt5_execution.md", report_line)
        text = append_block_once(text, "Run267BP(267BP 실행)는", block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BP(267BP 실행) state acceleration zero-trade gap classification(상태 가속 거래 0개 공백 분류) `{STATUS}`. "
        "Effect(효과): run267BO(267BO 실행)의 partial(부분 완료)을 실행 장애로 뭉개지 않고, 3개 anti_overconstraint_prune(과제약 제거) 완료 행과 1개 inactive surface(비활성 표면) 행으로 나눴다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267BP_state_acceleration_zero_trade_gap_classification_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_negative_register() -> None:
    row = (
        "| `NR-032` | `IDEA-ST267-S264-AIH-STATE-ACCELERATION-INTERACTION` | "
        "state_acceleration_interaction(상태 가속 상호작용)이 2025H1 cross-period(확장 기간) 대조군에서 trade activation(거래 활성화)을 만들 수 있다 | "
        "run267BP(267BP 실행)에서 tester report(테스터 보고서)는 completed(완료)였지만 trade count(거래 수)가 `0`이고 runtime CSV(런타임 CSV)가 없어서 inactive surface(비활성 표면)로 분류했다 | "
        "state acceleration(상태 가속) 아이디어는 버리지 않지만 같은 threshold/surface(임계값/표면) 그대로 재실행하지 않는다 | "
        "feature surface(피처 표면), threshold(임계값), 또는 routing density(라우팅 밀도)를 바꿔 trade activation(거래 활성화)이 먼저 증명될 때 |"
    )
    text = io_path(NEGATIVE_REGISTER_PATH).read_text(encoding="utf-8-sig")
    if "`NR-032`" not in text:
        text = text.rstrip() + "\n" + row + "\n"
        write_md(NEGATIVE_REGISTER_PATH, text)


def update_ledgers_and_artifacts(created_at: str, gap_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]]) -> None:
    zero_count = sum(1 for row in gap_rows if row.get("classification") == "zero_trade_report_completed_runtime_csv_absent")
    completed_count = sum(1 for row in gap_rows if row.get("classification") == "completed_runtime_kpi")
    notes = f"completed_runtime_kpi={completed_count};zero_trade_gap={zero_count};next_action={NEXT_ACTION};selected_candidate=none."
    stage_row = {
        "row_id": "stage267_run267BP_state_acceleration_zero_trade_gap_classification",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "state_acceleration_zero_trade_gap_classification",
        "tier_scope": "Tier A aggressive second tranche classification; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "gap_classification_and_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "mt5_report_classification_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_state_acceleration_zero_trade_gap_classification",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__state_acceleration_zero_trade_gap_classification",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "state_acceleration_zero_trade_gap_classification",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "state_acceleration_zero_trade_gap_classification",
        "tier_scope": "Tier A aggressive second tranche classification; true fallback blocked",
        "kpi_scope": "gap_classification_performance_attribution",
        "scoreboard_lane": "gap_classification_and_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"completed_runtime_kpi={completed_count};zero_trade_gap={zero_count};attribution_rows={len(attribution_rows)}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed_for_run267BO_mt5_report_classification",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    entries = (
        ("stage267_run267BP_producer", "producer_script", PRODUCER_PATH, "Classifies run267BO zero-trade/runtime gap."),
        ("stage267_run267BP_source_execution_result", "source_execution_result", SOURCE_EXECUTION_RESULT_PATH, "Source run267BO execution result."),
        ("stage267_run267BP_source_kpi_summary", "source_kpi_summary", SOURCE_KPI_SUMMARY_PATH, "Source run267BO KPI summary."),
        ("stage267_run267BP_source_forensics", "source_forensics", SOURCE_FORENSICS_PATH, "Source run267BO backtest forensics."),
        ("stage267_run267BP_source_profile_encoding", "source_profile_encoding", SOURCE_PROFILE_ENCODING_PATH, "Source run267BO no-BOM profile receipt."),
        ("stage267_run267BP_gap_classification", "gap_classification", GAP_CLASSIFICATION_PATH, "Attempt-level gap classification."),
        ("stage267_run267BP_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Period degradation and zero-trade attribution."),
        ("stage267_run267BP_forensic_gap_receipt", "forensic_gap_receipt", FORENSIC_GAP_RECEIPT_PATH, "Backtest forensic receipt for zero-trade gap."),
        ("stage267_run267BP_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment receipt."),
        ("stage267_run267BP_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BP_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BP_report", "review_report", REPORT_PATH, "User-facing report."),
        ("stage267_run267BP_negative_register", "negative_result_register", NEGATIVE_REGISTER_PATH, "Negative result memory row NR-032."),
    )
    existing = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes_text,
        }
        for artifact_id, artifact_type, path, notes_text in entries
    ]
    replacement_ids = {row["artifact_id"] for row in rows}
    merged = [row for row in existing if row.get("artifact_id") not in replacement_ids]
    merged.extend(rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def report_markdown(gap_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage267 run267BP State Acceleration Zero-trade Gap Classification(상태 가속 거래 0개 공백 분류)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- attempts_classified(분류 시도): `{len(gap_rows)}`",
        f"- completed_runtime_kpi(완료 런타임 KPI): `{sum(1 for row in gap_rows if row.get('classification') == 'completed_runtime_kpi')}`",
        f"- zero_trade_gap(거래 0개 공백): `{sum(1 for row in gap_rows if row.get('classification') == 'zero_trade_report_completed_runtime_csv_absent')}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BO(267BO 실행)의 partial(부분 완료)을 attempt(시도) 단위로 다시 분류했다.",
        "Effect(효과): state_acceleration_interaction(상태 가속 상호작용)은 infrastructure blocker(인프라 차단)가 아니라 zero-trade inactive surface(거래 0개 비활성 표면)로 기록하고, anti_overconstraint_prune(과제약 제거) 3개 완료 행만 다음 curve/time-slice/trade-quality(곡선/시간구간/거래품질) 검토로 넘긴다.",
        "",
        "## Attempt Classification(시도 분류)",
        "",
        "| attempt(시도) | variant(변형) | period(기간) | report trades(보고서 거래) | runtime(런타임) | classification(분류) | judgment(판정) |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in gap_rows:
        lines.append(
            "| `{attempt}` | `{variant}` | `{period}` | {trades} | `{runtime}` | `{classification}` | `{judgment}` |".format(
                attempt=row.get("attempt_name", ""),
                variant=row.get("variant_id", ""),
                period=row.get("target_period", ""),
                trades=row.get("report_trade_count", ""),
                runtime=row.get("runtime_status", ""),
                classification=row.get("classification", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Attribution(성과 귀속)",
            "",
            "| subject(대상) | observed_change(관측 변화) | confidence(신뢰도) | next_probe(다음 확인) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in attribution_rows:
        lines.append(
            "| `{subject}` | {change} | `{confidence}` | `{next_probe}` |".format(
                subject=row.get("subject", ""),
                change=row.get("observed_change", ""),
                confidence=row.get("attribution_confidence", ""),
                next_probe=row.get("next_probe", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 classification(분류)과 attribution(귀속)이며 candidate selection(후보 선택)이 아니다.",
            "- zero-trade(거래 0개)는 실패 기억으로 유효하지만 runtime parity closure(런타임 동등성 폐쇄)를 뜻하지 않는다.",
            "- ONNX conversion(ONNX 변환), ONNX parity(ONNX 동등성), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- gap_classification(공백 분류): `{rel(GAP_CLASSIFICATION_PATH)}`",
            f"- performance_attribution(성과 귀속): `{rel(PERFORMANCE_ATTRIBUTION_PATH)}`",
            f"- forensic_gap_receipt(포렌식 공백 영수증): `{rel(FORENSIC_GAP_RECEIPT_PATH)}`",
            f"- negative_result_register(부정 결과 등록부): `{rel(NEGATIVE_REGISTER_PATH)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
        ]
    )
    return "\n".join(lines)


def run() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(SOURCE_EXECUTION_RESULT_PATH)
    profile_rows = read_csv(SOURCE_PROFILE_ENCODING_PATH)
    forensic_rows = read_csv(SOURCE_FORENSICS_PATH)
    gap_rows = build_gap_rows(execution_result, profile_rows, forensic_rows)
    forensic_gap_rows = build_forensic_gap_rows(gap_rows, forensic_rows)
    attribution_rows = build_performance_attribution(gap_rows)
    judgment_rows = result_judgment_rows(gap_rows)
    write_csv(
        GAP_CLASSIFICATION_PATH,
        gap_rows,
        (
            "attempt_name",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "variant_id",
            "target_period",
            "period_id",
            "source_first_tranche_attempt_name",
            "tester_status",
            "returncode",
            "tester_process_completed",
            "runtime_status",
            "runtime_wait_status",
            "runtime_summary_exists",
            "runtime_telemetry_exists",
            "report_status",
            "report_trade_count",
            "report_net_profit",
            "report_profit_factor",
            "report_drawdown_percent",
            "parsed_deal_count",
            "parsed_trade_count",
            "report_parse_status",
            "profile_exists",
            "profile_has_bom",
            "tester_profile_path",
            "set_sha256",
            "feature_order_hash",
            "report_path",
            "report_sha256",
            "kpi_record_present",
            "runtime_claim_boundary",
            "classification",
            "judgment",
            "evidence_read",
            "next_probe",
        ),
    )
    write_csv(
        PERFORMANCE_ATTRIBUTION_PATH,
        attribution_rows,
        (
            "subject",
            "observed_change",
            "comparison_baseline",
            "likely_drivers",
            "segment_checks",
            "trade_shape",
            "alternative_explanations",
            "attribution_confidence",
            "next_probe",
        ),
    )
    write_csv(
        FORENSIC_GAP_RECEIPT_PATH,
        forensic_gap_rows,
        (
            "attempt_name",
            "tester_identity",
            "ea_identity",
            "report_identity",
            "trade_evidence",
            "cost_assumptions",
            "forensic_checks",
            "backtest_judgment",
        ),
    )
    write_csv(RESULT_JUDGMENT_PATH, judgment_rows, ("field", "value", "judgment", "evidence"))
    update_negative_register()
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "attempts_classified": len(gap_rows),
        "completed_runtime_kpi_count": sum(1 for row in gap_rows if row.get("classification") == "completed_runtime_kpi"),
        "zero_trade_gap_count": sum(1 for row in gap_rows if row.get("classification") == "zero_trade_report_completed_runtime_csv_absent"),
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "execution_result": rel(SOURCE_EXECUTION_RESULT_PATH),
            "kpi_summary": rel(SOURCE_KPI_SUMMARY_PATH),
            "forensics": rel(SOURCE_FORENSICS_PATH),
            "profile_encoding": rel(SOURCE_PROFILE_ENCODING_PATH),
            "runtime_parity": rel(SOURCE_RUNTIME_PARITY_PATH),
            "run_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
            "report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
            "gap_classification": rel(GAP_CLASSIFICATION_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "forensic_gap_receipt": rel(FORENSIC_GAP_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_json(RUN_MANIFEST_PATH, manifest)
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "sources": manifest["sources"],
            "outputs": manifest["outputs"],
            "lineage_judgment": "connected_with_zero_trade_boundary",
        },
    )
    write_md(REPORT_PATH, report_markdown(gap_rows, attribution_rows))
    update_ledgers_and_artifacts(created_at, gap_rows, attribution_rows)
    update_current_truth_docs()
    return manifest


def main() -> int:
    manifest = run()
    print(
        json.dumps(
            {
                "status": manifest["status"],
                "attempts_classified": manifest["attempts_classified"],
                "completed_runtime_kpi_count": manifest["completed_runtime_kpi_count"],
                "zero_trade_gap_count": manifest["zero_trade_gap_count"],
                "selected_candidate": manifest["selected_candidate"],
                "selected_research_baseline": manifest["selected_research_baseline"],
                "onnx_readiness": manifest["onnx_readiness"],
                "goal_achieve": manifest["goal_achieve"],
                "next_action": manifest["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage310 import execute_runtime_positive_fragment_allocation_mt5_probe as e310  # noqa: E402


STAGE_ID = "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild"
RUN_ID = "run321B_execute_post_controller_profit_curve_mt5_probe_v1"
RUN_NUMBER = "run321B"
SOURCE_RUN_ID = "run321A_design_post_controller_profit_curve_rebuild_packet_v1"
PARENT_RUN_ID = "run320C_review_validation_pocket_drawdown_controller_mt5_probe_v1"
STATUS_PREPARED = "prepared_post_controller_profit_curve_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-26"
EXPLORATION_LABEL = "stage321_Model__PostControllerProfitCurveReplay"
SIGNAL_COLUMN = "run321b_route_signal"
FEATURE_ORDER = (SIGNAL_COLUMN,)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage321/run321B_post_controller_profit_curve"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN321A = STAGE_ROOT / "02_runs" / "run321A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"
MT5_QUEUE = RUN321A / "mt5_probe_queue.csv"
SOURCE_MANIFEST = RUN321A / "candidate_payload_manifest.csv"
SOURCE_RUN_MANIFEST = RUN321A / "run_manifest.json"
SOURCE_REPORT = REVIEWS / "run321A_materialization.md"
PRODUCER = Path("stage_pipelines/stage321/execute_post_controller_profit_curve_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run321B_mt5_probe.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def classify_status(result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(result.get("attempts", []))) or 0)
    if materialize_only:
        return (
            STATUS_PREPARED,
            "post_controller_profit_curve_runtime_probe_prepared_no_external_execution",
            "out_of_scope_by_claim_materialize_only",
            "run321B_execute_post_controller_profit_curve_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if planned and completed_exec >= planned and len(kpis) >= planned:
        return (
            "completed_post_controller_profit_curve_mt5_probe_no_selection",
            "runtime_probe_completed_requires_profit_curve_review_no_selection",
            "completed",
            "run321C_review_post_controller_profit_curve_mt5_probe",
        )
    if kpis:
        return (
            "partial_post_controller_profit_curve_mt5_probe_no_selection",
            "runtime_probe_partial_requires_continuation_or_review_no_selection",
            "partial_or_blocked",
            "run321B_continue_post_controller_profit_curve_mt5_probe",
        )
    return (
        "blocked_post_controller_profit_curve_mt5_probe_no_kpi",
        "runtime_probe_blocked_no_kpi_no_selection",
        "blocked_or_invalid",
        "run321B_repair_or_block_post_controller_profit_curve_mt5_probe",
    )


def report_markdown(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> str:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed = sum(1 for item in execution_results if item.get("status") == "completed")
    blocked = sum(1 for item in execution_results if item.get("status") == "blocked")
    return "\n".join(
        [
            "# run321B Post Controller Profit Curve MT5 Probe(321B 제어기 이후 수익 곡선 MT5 탐침)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- stage_id(단계 ID): `{STAGE_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- external_verification_status(외부 검증 상태): `{external_status}`",
            f"- attempts(시도): `{len(execution_results)}/{len(attempts)}`",
            f"- completed_attempts(완료 시도): `{completed}`",
            f"- blocked_attempts(차단 시도): `{blocked}`",
            f"- mt5_kpi_records(MT5 KPI 기록): `{len(kpis)}`",
            f"- feature_order(피처 순서): `{'|'.join(FEATURE_ORDER)}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            "Effect(효과): run321A(321A 실행)의 consensus/union route_signal_value(합의/합집합 경로 신호)를 MT5 tester(MT5 테스터)에 넣어 실제 수익과 곡선을 확인한다.",
            "",
            f"`{e310.BOUNDARY}`",
        ]
    )


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    attempt_count = len(result.get("attempts", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    base = e310.runner.prev.e295.e294.base.base
    ledger.upsert_csv_rows(RUN_REGISTRY, base.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_controller_profit_curve_mt5_probe", "status": status, "judgment": judgment, "path": base.rel(REPORT), "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}."}], key="run_id")
    ledger.upsert_csv_rows(ALPHA_LEDGER, base.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__mt5_probe", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "post_controller_profit_curve_mt5_probe", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "kpi_scope": "runtime_probe", "scoreboard_lane": "post_controller_profit_curve", "status": status, "judgment": judgment, "path": base.rel(REPORT), "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed", "external_verification_status": external_status, "notes": f"next_action={next_action}."}], key="ledger_row_id")
    ledger.upsert_csv_rows(STAGE_LEDGER, e310.runner.prev.e295.e294.base.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__mt5_probe", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_controller_profit_curve_mt5_probe", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "runtime_probe", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_no_candidate_no_onnx", "report_path": base.rel(REPORT), "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count}."}], key="row_id")


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    base = e310.runner.prev.e295.e294.base.base

    def save_md(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        base.io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")

    selected = base.io_path(SELECTED).read_text(encoding="utf-8-sig") if base.path_exists(SELECTED) else ""
    selected = e310.replace_first_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = e310.replace_first_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = e310.replace_first_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected = base.append_once(selected, "run321B_report", f"- run321B_report(321B 보고서): `{base.rel(REPORT)}`")
    selected = base.append_once(selected, "run321B_execution_result", f"- run321B_execution_result(321B 실행 결과): `{base.rel(EXECUTION_RESULT)}`")
    save_md(SELECTED, selected)

    review_index = base.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if base.path_exists(REVIEW_INDEX) else "# Stage321 Review Index(321단계 검토 색인)\n"
    review_index = base.append_once(review_index, "run321B_report", f"- run321B_report(321B 보고서): `{base.rel(REPORT)}`\n- run321B_execution_result(321B 실행 결과): `{base.rel(EXECUTION_RESULT)}`\n- run321B_mt5_kpi_summary(321B MT5 KPI 요약): `{base.rel(MT5_KPI_SUMMARY)}`")
    save_md(REVIEW_INDEX, review_index)

    current = base.io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if base.path_exists(CURRENT_STATE) else ""
    current = e310.replace_first_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = e310.replace_first_prefix(current, "- status(", f"- status(상태): `{status}`")
    current = e310.replace_first_prefix(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = base.append_once(current, "run321B_summary", f"- run321B_summary(321B 요약): post-controller profit curve MT5 probe(제어기 이후 수익 곡선 MT5 탐침)를 실행했다. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.")
    save_md(CURRENT_STATE, current)

    workspace = base.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if base.path_exists(WORKSPACE_STATE) else ""
    workspace = base.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = base.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage321(321단계) run321B(321B 실행) post-controller profit curve MT5 probe(제어기 이후 수익 곡선 MT5 탐침) `{RUN_ID}`. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 기록했고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    workspace = base.prepend_focus(workspace, focus, RUN_ID)
    save_md(WORKSPACE_STATE, workspace)

    changelog = base.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if base.path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = base.append_once(changelog, RUN_ID, f"## {UPDATED_ON} run321B Post-controller profit curve MT5 probe(321B 제어기 이후 수익 곡선 MT5 탐침)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 기록했다.\n")
    save_md(CHANGELOG, changelog)


def configure() -> None:
    replacements = {name: value for name, value in globals().items() if name.isupper()}
    replacements.update(
        {
            "RUN310A": RUN321A,
            "classify_status": classify_status,
            "report_markdown": report_markdown,
            "upsert_ledgers": upsert_ledgers,
            "update_docs": update_docs,
        }
    )
    for name, value in replacements.items():
        setattr(e310, name, value)


def main(argv: Sequence[str] | None = None) -> None:
    configure()
    e310.main(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    main()

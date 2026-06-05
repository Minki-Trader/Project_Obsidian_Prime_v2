from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import path_exists  # noqa: E402
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import materialize_runtime_positive_side_stability_gb_repair_runtime_probe_package_without_db as gg  # noqa: E402


TODAY = "2026-05-31"
STAGE_ID = gg.STAGE_ID
RUN_NUMBER = "run337GH"
RUN_ID = "run337GH_execute_runtime_positive_side_stability_gb_repair_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = gg.RUN_ID
NEXT_RUN_ID = "run337GI_review_runtime_positive_side_stability_gb_repair_mt5_runtime_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage337GH_runtime_positive_side_stability_gb_repair_mt5_runtime_probe_executed_review_required_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337GH_runtime_positive_side_stability_gb_repair_mt5_runtime_probe_attempt_missing_or_failed_outputs_no_forward_decision"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage337GH_open_run337GI_review_runtime_positive_side_stability_gb_repair_mt5_runtime_probe"
DECISION_BLOCKED = "stage337GH_open_run337GI_review_or_repair_mt5_runtime_probe_attempt"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GH_runtime_positive_side_stability_gb_repair_mt5_runtime_probe_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEWS_DIR = gg.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GH_runtime_positive_side_stability_gb_repair_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GH_runtime_positive_side_stability_gb_repair_mt5_runtime_probe.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "runtime_positive_side_stability_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    gg.FINAL_DECISION,
    gg.GATE_AUDIT,
    gg.EXECUTION_QUEUE,
    gg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    gg.EXPECTED_PROBABILITY_TAPE,
    gg.COMMON_FILES_SYNC,
    gg.TESTER_SET_MANIFEST,
    gg.TESTER_INI_MANIFEST,
    gg.MODEL_HANDOFF_MANIFEST,
    gg.FEATURE_MATRIX_MANIFEST,
    fa.PORTABLE_EA_EX5,
)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    BACKTEST_FORENSICS_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    gg.SELECTED_STATUS,
    gg.WORKSPACE_STATE,
    gg.CURRENT_STATE,
    gg.CHANGELOG,
    gg.STAGE_BRIEF,
    Path(__file__),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337GH runtime positive side stability MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(fa.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(fa.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(fa.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(fa.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=480)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    parser.add_argument("--attempt-limit", type=int, default=5)
    return parser.parse_args()


def rel(path: Path | str) -> str:
    return gg.aw.rel(path)


def runtime_identity(attempt_rows: int) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "stage337GH_runtime_identity",
            "terminal_path": fa.DEFAULT_TERMINAL.as_posix(),
            "terminal_exists": path_exists(fa.DEFAULT_TERMINAL),
            "common_files_root": fa.DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": fa.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "terminal_data_root": fa.DEFAULT_TERMINAL_DATA_ROOT.as_posix(),
            "portable_ea_ex5": fa.PORTABLE_EA_EX5.as_posix(),
            "portable_ea_ex5_exists": path_exists(fa.PORTABLE_EA_EX5),
            "portable_ea_ex5_sha256": gg.aw.sha256_file(fa.PORTABLE_EA_EX5) if path_exists(fa.PORTABLE_EA_EX5) else "",
            "attempt_rows": attempt_rows,
            "tester_model": "4 real ticks(실제 틱)",
            "deposit": "500",
            "leverage": "1:100",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    gg_final = fb.read_json(gg.FINAL_DECISION)
    completed = fb.as_int(summary.get("runtime_completed_rows")) > 0
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": DECISION_COMPLETED if completed else DECISION_BLOCKED,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fb.fail_if_missing(INPUT_FILES)),
        "gg_next_action": gg_final.get("next_action", ""),
        "gg_failed_gate_rows": sum(1 for row in fb.read_csv(gg.GATE_AUDIT) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    attempt_or_block_recorded = final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(gg.RUNTIME_PROBE_ATTEMPT_PACKAGE), "required GG package inputs exist(필수 GG 패키지 입력 존재)"),
        ("parent_gg_gates_passed", final["gg_failed_gate_rows"] == 0, str(final["gg_failed_gate_rows"]), "0", rel(gg.GATE_AUDIT), "GG gates passed(GG 게이트 통과)"),
        ("parent_next_action_matches", final["gg_next_action"] == RUN_ID, str(final["gg_next_action"]), RUN_ID, rel(gg.FINAL_DECISION), "GH follows GG next action(GH가 GG 다음 행동을 따름)"),
        ("mt5_attempt_or_block_recorded", attempt_or_block_recorded, f"execution={final['execution_result_rows']};attempts={final['attempt_rows']}", "execution rows equal attempts", rel(MT5_EXECUTION_RESULT), "MT5 attempt or blocker recorded(MT5 시도 또는 차단 기록)"),
        ("runtime_output_copy_recorded", final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2, str(final["runtime_output_copy_rows"]), ">= attempts*2", rel(RUNTIME_OUTPUT_COPY), "runtime output copy audit exists(런타임 출력 복사 감사 존재)"),
        ("comparison_summary_materialized", final["summary_rows"] == final["attempt_rows"], f"summary={final['summary_rows']};attempts={final['attempt_rows']}", "summary rows equal attempts", rel(EXECUTION_SUMMARY), "proxy-MT5 comparison summary exists(프록시-MT5 비교 요약 존재)"),
        ("diff_or_blocker_materialized", final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0, f"diff={final['diff_rows']};runtime_completed={final['runtime_completed_rows']}", "diff rows or blocker", rel(PROXY_MT5_DIFF), "diff rows or blocker state recorded(차이 행 또는 차단 상태 기록)"),
        ("forensics_identity_recorded", path_exists(RUNTIME_IDENTITY), "present", "present", rel(RUNTIME_IDENTITY), "tester identity recorded(테스터 정체성 기록)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "no operating claim from runtime probe(런타임 탐침에서 운영 주장 없음)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    runtime = {
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(ATTEMPT_PACKAGE),
        "shared_contract": "GG feature matrix, expected tape, set/ini, ONNX handoff(GG 피처 행렬, 예상 테이프, 설정, ONNX 인계)",
        "parity_check": f"matched_rows={final['matched_rows']};mismatch_rows={final['mismatch_rows']};runtime_completed={final['runtime_completed_rows']}",
        "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "US100 M5 Deposit=500 Leverage=1:100 Model=4 real ticks(US100 M5 예수금 500 레버리지 1:100 실제 틱)",
        "report_identity": rel(STRATEGY_TESTER_REPORTS),
        "trade_evidence": f"report_rows={final['report_rows']};runtime_completed={final['runtime_completed_rows']}",
        "backtest_judgment": "review_required(검토 필요)" if final["runtime_completed_rows"] else "blocked(차단)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "summary": rel(EXECUTION_SUMMARY),
        "diff": rel(PROXY_MT5_DIFF),
        "runtime_completed_rows": final["runtime_completed_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "allowed_use": "runtime probe review only(런타임 탐침 검토 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "decision": final["decision"],
        "next_condition": final["next_action"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        fb.write_json(RUNTIME_RECEIPT, runtime),
        fb.write_json(BACKTEST_FORENSICS_RECEIPT, forensics),
        fb.write_json(PERFORMANCE_RECEIPT, performance),
        fb.write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): gg.aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and gg.aw.io_path(path).is_file()
        },
        "registry_links": [rel(gg.RUN_REGISTRY), rel(gg.ALPHA_LEDGER), rel(gg.STAGE_LEDGER), rel(gg.ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_GG_package_to_GH_runtime_probe(GG 패키지를 GH 런타임 탐침에 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(fb.write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GH MT5 Runtime Probe(337단계 337GH MT5 런타임 탐침)

## Conclusion(결론)

run337GH(337GH 실행)는 run337GG(337GG 실행)의 runtime positive side stability repair package(런타임 긍정 방향 안정 수리 패키지)를 MT5 terminal(MT5 터미널)에 시도했다.

Action(행동): Strategy Tester(전략 테스터)를 attempt(시도)별로 실행하거나 blocker(차단 사유)를 기록했다. Effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime output(MT5 런타임 출력)을 다음 GA review(GA 검토)에서 비교할 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- report_rows(보고서 행): `{final['report_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return gg.aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GH Decision(337GH 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(MT5_EXECUTION_RESULT)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침)를 시도하고 결과 또는 blocker(차단 사유)를 기록했다.
Effect(효과): 다음 GA review(GA 검토)가 proxy-vs-MT5 diff(프록시-MT5 차이), attribution(귀속), usability(활용 가능성)을 판정할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return gg.aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = gg.aw.read_text_lossless(gg.WORKSPACE_STATE)
    workspace = fb.replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = fb.replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = fb.replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GH focus complete: run337GH(337GH 실행)는 `{final['status']}`로 MT5 runtime probe(MT5 런타임 탐침)를 시도했다. "
        f"Effect(효과): attempts(시도) `{final['attempt_rows']}`, runtime completed(런타임 완료) `{final['runtime_completed_rows']}`, matched rows(일치 행) `{final['matched_rows']}`, mismatches(불일치) `{final['mismatch_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337GH focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337GH focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(gg.aw.write_text_lossless(gg.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = gg.aw.read_text_lossless(gg.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GH MT5 Runtime Probe(MT5 런타임 탐침)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- report_rows(보고서 행): `{final['report_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): MT5 external check(MT5 외부 확인)를 실제로 시도하고 GA review(GA 검토)로 넘긴다. 운영 주장은 닫는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GG Runtime Probe Package", section, "run337GH MT5 Runtime Probe")
    artifacts.append(gg.aw.write_text_lossless(gg.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GH(337GH 실행)는 runtime probe(런타임 탐침) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(gg.aw.write_text_lossless(gg.SELECTED_STATUS, selection, True))

    brief, brief_bom = gg.aw.read_text_lossless(gg.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337GH(337GH 실행) `{final['status']}`. "
        f"Effect(효과): MT5 attempts(MT5 시도) `{final['attempt_rows']}`, runtime completed(런타임 완료) `{final['runtime_completed_rows']}`, matched rows(일치 행) `{final['matched_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(gg.aw.write_text_lossless(gg.STAGE_BRIEF, fb.upsert_single_line(brief, "run337GH(337GH 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = gg.aw.read_text_lossless(gg.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337GH(337GH 실행) `{final['status']}`. "
        f"Effect(효과): MT5 runtime probe(MT5 런타임 탐침)를 시도하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(gg.aw.write_text_lossless(gg.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337GH", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_side_stability_gb_repair_mt5_runtime_probe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};runtime_completed={final['runtime_completed_rows']};matched={final['matched_rows']};mismatch={final['mismatch_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_backtest_forensics_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_side_stability_gb_repair_mt5_runtime_probe(런타임 긍정 방향 안정 수리 MT5 런타임 탐침)",
        "tier_scope": "Tier A inner holdout MT5 runtime probe(Tier A 내부 보류 MT5 런타임 탐침)",
        "kpi_scope": "runtime_probe_only_no_forward_goal(런타임 탐침 전용, 전진/목표 없음)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_completed={final['runtime_completed_rows']};matched={final['matched_rows']};mismatch={final['mismatch_rows']}",
        "guardrail_kpi": "no_selection;no_forward;no_goal;review_required",
        "external_verification_status": "attempted",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_backtest_forensics_performance_attribution",
        "evidence_scope": "MT5 tester attempts, telemetry, reports, proxy diff",
        "kpi_scope": "runtime_probe_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_runtime_probe",
        "family": "runtime_positive_side_stability_gb_repair_mt5_runtime_probe",
        "question": "do GG ONNX runtime packages execute in MT5 and match expected probabilities",
        "metric_scope": "runtime_telemetry_proxy_diff_tester_reports",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gg.RUN_REGISTRY, gg.aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gg.ALPHA_LEDGER, gg.aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gg.STAGE_LEDGER, gg.aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def configure_execution_engine() -> None:
    replacements = {
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_COMPLETED": STATUS_COMPLETED,
        "STATUS_BLOCKED": STATUS_BLOCKED,
        "JUDGMENT_COMPLETED": JUDGMENT_COMPLETED,
        "JUDGMENT_BLOCKED": JUDGMENT_BLOCKED,
        "DECISION_COMPLETED": DECISION_COMPLETED,
        "DECISION_BLOCKED": DECISION_BLOCKED,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "TELEMETRY_COPY_DIR": TELEMETRY_COPY_DIR,
        "REPORT_COPY_DIR": REPORT_COPY_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "SELECTED_STATUS": gg.SELECTED_STATUS,
        "STAGE_BRIEF": gg.STAGE_BRIEF,
        "WORKSPACE_STATE": gg.WORKSPACE_STATE,
        "CURRENT_STATE": gg.CURRENT_STATE,
        "CHANGELOG": gg.CHANGELOG,
        "RUN_REGISTRY": gg.RUN_REGISTRY,
        "ALPHA_LEDGER": gg.ALPHA_LEDGER,
        "ARTIFACT_REGISTRY": gg.ARTIFACT_REGISTRY,
        "STAGE_LEDGER": gg.STAGE_LEDGER,
        "FA_FINAL": gg.FINAL_DECISION,
        "FA_GATES": gg.GATE_AUDIT,
        "FA_QUEUE": gg.EXECUTION_QUEUE,
        "FA_ATTEMPT_PACKAGE": gg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
        "FA_EXPECTED_TAPE": gg.EXPECTED_PROBABILITY_TAPE,
        "FA_COMMON_SYNC": gg.COMMON_FILES_SYNC,
        "FA_TESTER_SET": gg.TESTER_SET_MANIFEST,
        "FA_TESTER_INI": gg.TESTER_INI_MANIFEST,
        "FA_MODEL_HANDOFF": gg.MODEL_HANDOFF_MANIFEST,
        "FA_FEATURE_MANIFEST": gg.FEATURE_MATRIX_MANIFEST,
        "DEFAULT_TERMINAL": fa.DEFAULT_TERMINAL,
        "DEFAULT_COMMON_FILES": fa.DEFAULT_COMMON_FILES,
        "DEFAULT_TESTER_PROFILE_ROOT": fa.DEFAULT_TESTER_PROFILE_ROOT,
        "DEFAULT_TERMINAL_DATA_ROOT": fa.DEFAULT_TERMINAL_DATA_ROOT,
        "PORTABLE_EA_EX5": fa.PORTABLE_EA_EX5,
        "ATTEMPT_PACKAGE": ATTEMPT_PACKAGE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "EXECUTION_SUMMARY": EXECUTION_SUMMARY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "TELEMETRY_SKIP_SUMMARY": TELEMETRY_SKIP_SUMMARY,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "BACKTEST_FORENSICS_RECEIPT": BACKTEST_FORENSICS_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "PERFORMANCE_RECEIPT": PERFORMANCE_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
    }
    for name, value in replacements.items():
        setattr(fb, name, value)
    fb.parse_args = parse_args
    fb.runtime_identity = runtime_identity
    fb.make_final = make_final
    fb.build_gates = build_gates
    fb.build_receipts = build_receipts
    fb.write_report = write_report
    fb.write_decision = write_decision
    fb.update_docs = update_docs
    fb.update_registers = update_registers


def main() -> int:
    configure_execution_engine()
    return fb.main()


if __name__ == "__main__":
    raise SystemExit(main())

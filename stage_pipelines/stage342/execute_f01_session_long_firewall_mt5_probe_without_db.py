from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage339 import execute_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db as ebase  # noqa: E402
from stage_pipelines.stage342 import materialize_f01_session_long_firewall_mt5_probe_package_without_db as pkg  # noqa: E402


TODAY = "2026-06-01"
RUN_NUMBER = "run342C"
RUN_ID = "run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run342D_review_f01_session_long_firewall_mt5_probe_without_db_v1"
STATUS_COMPLETED = "completed_stage342C_f01_session_long_firewall_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage342C_f01_session_long_firewall_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_COMPLETED = "mt5_f01_session_long_firewall_probe_outputs_available_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_f01_session_long_firewall_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage342C_open_run342D_review_f01_session_long_firewall_probe"
DECISION_BLOCKED = "stage342C_open_run342D_review_or_repair_f01_session_long_firewall_probe"
CLAIM_BOUNDARY = (
    "research_development_f01_session_long_firewall_mt5_runtime_probe_attempt_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run342C_f01_session_long_firewall_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage342C_f01_session_long_firewall_mt5_probe.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "f01_session_long_firewall_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    pkg.FINAL_DECISION,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.EXPECTED_PROBABILITY_TAPE,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.TESTER_IDENTITY_CONTRACT,
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
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row("parent_342B_gates_passed", "passed" if final["parent_gate_passed"] else "failed", ebase.rel(pkg.GATE_AUDIT), "run342B(342B 실행) package gate(패키지 게이트)를 이어받는다."),
            gate_row("mt5_attempts_recorded", "passed" if final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0 else "failed", ebase.rel(MT5_EXECUTION_RESULT), "각 attempt(시도)의 MT5 실행 결과를 기록한다."),
            gate_row("runtime_outputs_completed", "passed" if final["runtime_completed_rows"] == final["attempt_rows"] else "failed", ebase.rel(RUNTIME_OUTPUT_COPY), "모든 telemetry(런타임 기록)를 복사한다."),
            gate_row("strategy_tester_reports_collected", "passed" if final["report_completed_rows"] == final["attempt_rows"] else "failed", ebase.rel(STRATEGY_TESTER_REPORTS), "각 Strategy Tester report(전략 테스터 보고서)를 수집한다."),
            gate_row("comparison_summary_materialized", "passed" if final["summary_rows"] == final["attempt_rows"] else "failed", ebase.rel(EXECUTION_SUMMARY), "proxy-MT5 summary(프록시-MT5 요약)를 만든다."),
            gate_row("exact_runtime_parity_reached", "passed" if final["matched_rows"] == final["expected_rows"] and final["mismatch_rows"] == 0 else "failed", ebase.rel(PROXY_MT5_DIFF), "expected tape(예상 테이프)와 MT5 telemetry(MT5 기록)의 parity(동등성)를 확인한다."),
            gate_row("forensics_identity_recorded", "passed" if ebase.exists(RUNTIME_IDENTITY) else "failed", ebase.rel(RUNTIME_IDENTITY), "tester identity(테스터 정체성)를 기록한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", ebase.rel(FINAL_DECISION), "runtime probe(런타임 탐침)를 selection(선정), operating promotion(운영 승격), Goal Achieve(목표 달성)로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", ebase.rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다."),
        ]
    )


def build_summary(
    args: Any,
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    parent_final = ebase.read_json_direct(pkg.FINAL_DECISION)
    parent_gates = ebase.read_csv_direct(pkg.GATE_AUDIT)
    completed_runtime = sum(1 for row in summaries if str(row.get("runtime_status", "")) == "completed")
    completed_reports = sum(1 for row in report_records if str(row.get("status", "")) == "completed")
    expected_rows = sum(ebase.base.as_int(row.get("expected_rows")) for row in summaries)
    matched_rows = sum(ebase.base.as_int(row.get("matched_rows")) for row in summaries)
    mismatches = sum(
        ebase.base.as_int(row.get("expected_missing_rows"))
        + ebase.base.as_int(row.get("hash_mismatch_rows"))
        + ebase.base.as_int(row.get("probability_mismatch_rows"))
        + ebase.base.as_int(row.get("decision_mismatch_rows"))
        for row in summaries
    )
    exact_parity_rows = sum(
        1
        for row in summaries
        if str(row.get("comparison_status", "")) == "completed_exact_proxy_mt5_parity_reached_feature_last"
    )
    completed = completed_runtime == len(attempts) and completed_reports == len(attempts)
    status = STATUS_COMPLETED if completed else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    decision = DECISION_COMPLETED if completed else DECISION_BLOCKED
    best = ebase.base.best_attempt_from_summaries(summaries)
    ebase.write_csv_direct(
        RUNTIME_IDENTITY,
        pd.DataFrame(
            [
                {
                    "identity_id": "stage342C_runtime_identity",
                    "terminal_path": str(args.terminal_path),
                    "terminal_exists": ebase.exists(Path(args.terminal_path)),
                    "common_files_root": str(args.common_files_root),
                    "tester_profile_root": str(args.tester_profile_root),
                    "terminal_data_root": str(args.terminal_data_root),
                    "portable_ea_ex5": pkg.PORTABLE_EA_EX5.as_posix(),
                    "portable_ea_ex5_exists": ebase.exists(pkg.PORTABLE_EA_EX5),
                    "portable_ea_ex5_sha256": pkg.aw.sha256_file(pkg.PORTABLE_EA_EX5) if ebase.exists(pkg.PORTABLE_EA_EX5) else "",
                    "attempt_rows": len(attempts),
                    "tester_model": "4 real ticks(실제 틱)",
                    "deposit": "500",
                    "leverage": "1:100",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempts),
        "execution_result_rows": len(execution_results),
        "runtime_completed_rows": completed_runtime,
        "report_rows": len(report_records),
        "report_completed_rows": completed_reports,
        "summary_rows": len(summaries),
        "diff_rows": len(diffs),
        "expected_rows": expected_rows,
        "matched_rows": matched_rows,
        "mismatch_rows": mismatches,
        "exact_parity_rows": exact_parity_rows,
        "runtime_output_copy_rows": len(copy_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if row.get("exists") is True),
        "mt5_execution_attempted": "yes",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "completed(완료)" if completed else "blocked(차단)",
        "parent_gate_passed": bool(ebase.passed_status_direct(parent_gates["status"]).all()),
        "parent_goal_achieve": parent_final.get("goal_achieve", "not_claimed"),
        "best_attempt_name": best.get("attempt_name", ""),
        "best_model_id": best.get("model_id", ""),
        "best_net_profit": ebase.base.as_float(best.get("net_profit")),
        "best_profit_factor": ebase.base.as_float(best.get("profit_factor")),
        "best_expectancy": ebase.base.as_float(best.get("expectancy")),
        "best_recovery_factor": ebase.base.as_float(best.get("recovery_factor")),
        "best_max_drawdown_amount": ebase.base.as_float(best.get("max_drawdown_amount")),
        "best_trade_count": ebase.base.as_int(best.get("trade_count")),
        "best_long_trade_count": ebase.base.as_int(best.get("long_trade_count")),
        "best_short_trade_count": ebase.base.as_int(best.get("short_trade_count")),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    receipt_base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    ebase.write_json_direct(
        RUNTIME_RECEIPT,
        {
            **receipt_base,
            "research_path": ebase.rel(pkg.EXPECTED_PROBABILITY_TAPE),
            "runtime_path": ebase.rel(RUNTIME_OUTPUT_COPY),
            "shared_contract": ebase.rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "side filter(사이드 필터)는 probability(확률)는 유지하고 decision(결정)만 flat(관망)으로 바꿀 수 있다.",
            "parity_check": ebase.rel(PROXY_MT5_DIFF),
            "parity_identity": ebase.rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    ebase.write_json_direct(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **receipt_base,
            "tester_identity": ebase.rel(RUNTIME_IDENTITY),
            "report_records": ebase.rel(STRATEGY_TESTER_REPORTS),
            "attempt_count": final["attempt_rows"],
            "report_completed_rows": final["report_completed_rows"],
            "best_attempt_name": final["best_attempt_name"],
            "best_net_profit": final["best_net_profit"],
            "best_profit_factor": final["best_profit_factor"],
            "effect": "Strategy Tester(전략 테스터) 출력과 side filter(사이드 필터) 설정 정체성을 함께 남긴다.",
        },
    )
    ebase.write_json_direct(
        PERFORMANCE_RECEIPT,
        {
            **receipt_base,
            "summary": ebase.rel(EXECUTION_SUMMARY),
            "proxy_mt5_diff": ebase.rel(PROXY_MT5_DIFF),
            "best_attempt_name": final["best_attempt_name"],
            "best_net_profit": final["best_net_profit"],
            "best_profit_factor": final["best_profit_factor"],
            "best_recovery_factor": final["best_recovery_factor"],
            "best_trade_count": final["best_trade_count"],
            "effect": "session-long firewall(세션 롱 방화벽)의 MT5 KPI(MT5 핵심 성과 지표)를 review(검토)로 넘긴다.",
        },
    )
    ebase.write_json_direct(
        JUDGMENT_RECEIPT,
        {
            **receipt_base,
            "result_judgment": final["judgment"],
            "external_verification_status": final["external_verification_status"],
            "candidate_selection": "not_run",
            "goal_achieve": "not_claimed",
        },
    )
    ebase.write_json_direct(
        CLAIM_RECEIPT,
        {
            **receipt_base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    ebase.write_json_direct(
        LINEAGE_RECEIPT,
        {
            **receipt_base,
            "source_inputs": [ebase.rel(path) for path in INPUT_FILES],
            "producer": ebase.rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [ebase.base.display_path(path) for path in ebase.base.artifact_paths() if ebase.exists(path)],
            "artifact_hashes": {ebase.base.display_path(path): pkg.aw.sha256_file(path) for path in ebase.base.artifact_paths() if ebase.exists(path)},
            "registry_links": [ebase.rel(RUN_REGISTRY), ebase.rel(PROJECT_LEDGER), ebase.rel(STAGE_LEDGER), ebase.rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_runtime_probe_boundary(런타임 탐침 경계로 연결됨)",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run342C F01 Session-Long Firewall MT5 Probe(342C F01 세션 롱 방화벽 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- report_completed_rows(보고서 완료 행): `{final['report_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- best_long_short(최고 롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run342B(342B 실행)의 control(대조), early-long firewall(초반 롱 방화벽), overfilter negative control(과필터 부정 대조)을 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(런타임 기록)를 expected tape(예상 테이프)와 비교했다.

## Effect(효과)

run342D(342D 실행)는 session-long firewall(세션 롱 방화벽)이 q01/q09(큐01/큐09)의 net profit(순수익), profit factor(수익 팩터), recovery factor(회복 계수), drawdown(낙폭), trade shape(거래 형태)에 실제로 도움이 되는지 검토할 수 있다.

## Boundary(경계)

run342C(342C 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage342C Decision(342C 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{ebase.rel(MT5_EXECUTION_RESULT)}`, `{ebase.rel(EXECUTION_SUMMARY)}`, `{ebase.rel(PROXY_MT5_DIFF)}`

Action(행동): session-long firewall(세션 롱 방화벽)을 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
Effect(효과): run342D(342D 실행)가 KPI(핵심 성과 지표), side filter effect(사이드 필터 효과), proxy-MT5 diff(프록시-MT5 차이)를 판정할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`

## Effect(효과)

run342C(342C 실행)는 MT5 runtime probe(MT5 런타임 탐침)를 시도했다. run342D(342D 실행)는 결과를 검토해 positive clue(긍정 단서), failure memory(실패 기억), next offensive seed(다음 공격 탐색 씨앗)를 나눠야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 결과를 바로 selection(선정)으로 오해하지 않고 review(검토)로 넘긴다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
current_decision: {final['decision']}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    ebase.write_bom_text_direct(REPORT_PATH, report)
    ebase.write_bom_text_direct(DECISION_DOC, decision)
    ebase.write_bom_text_direct(CURRENT_WORKING_STATE, current)
    ebase.write_bom_text_direct(SELECTION_STATUS, selection)
    ebase.write_bom_text_direct(ROOT_SELECTION_STATUS, selection)
    ebase.write_bom_text_direct(WORKSPACE_STATE, workspace)
    marker = f"run342C {RUN_ID}"
    ebase.append_text_once_direct(
        STAGE_BRIEF,
        marker,
        f"""## run342C F01 Session-Long Firewall MT5 Probe(342C F01 세션 롱 방화벽 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- effect(효과): Stage342(342단계) package(패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.
""",
    )
    ebase.append_text_once_direct(
        STAGE_README,
        marker,
        f"""## run342C F01 Session-Long Firewall MT5 Probe(342C F01 세션 롱 방화벽 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- summary(요약): `{ebase.rel(EXECUTION_SUMMARY)}`
- diff(차이): `{ebase.rel(PROXY_MT5_DIFF)}`
- effect(효과): run342D(342D 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.
""",
    )
    changelog = f"""## {TODAY} run342C F01 Session-Long Firewall MT5 Probe(F01 세션 롱 방화벽 MT5 탐침)

- action(행동): session-long firewall(세션 롱 방화벽) `{final['attempt_rows']}`개를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
- effect(효과): matched_rows(일치 행) `{final['matched_rows']}/{final['expected_rows']}`, best_attempt(최고 시도) `{final['best_attempt_name']}`를 기록했다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    ebase.append_text_once_direct(ROOT_CHANGELOG, marker, changelog)
    ebase.append_text_once_direct(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": ebase.rel(FINAL_DECISION),
        "report_path": ebase.rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    ebase.append_or_replace_csv_direct(RUN_REGISTRY, ["run_id"], base_row)
    rows = [
        {
            **base_row,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe",
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": final["judgment"],
        },
        {
            **base_row,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base_row,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    for row in rows:
        ebase.append_or_replace_csv_direct(PROJECT_LEDGER, ["run_id", "view"], row)
        ebase.append_or_replace_csv_direct(STAGE_LEDGER, ["run_id", "view"], row)


def configure_ebase() -> None:
    replacements = {
        "pkg": pkg,
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "STAGE_DIR": STAGE_DIR,
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
        "REVIEW_DIR": REVIEW_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "SELECTION_STATUS": SELECTION_STATUS,
        "STAGE_BRIEF": STAGE_BRIEF,
        "STAGE_README": STAGE_README,
        "STAGE_LEDGER": STAGE_LEDGER,
        "RUN_REGISTRY": RUN_REGISTRY,
        "PROJECT_LEDGER": PROJECT_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_WORKING_STATE": CURRENT_WORKING_STATE,
        "ROOT_CHANGELOG": ROOT_CHANGELOG,
        "WORKSPACE_CHANGELOG": WORKSPACE_CHANGELOG,
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
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
        "make_gates": make_gates,
        "build_summary": build_summary,
        "write_receipts": write_receipts,
        "write_docs": write_docs,
        "write_registers": write_registers,
    }
    for key, value in replacements.items():
        setattr(ebase, key, value)


def main() -> None:
    configure_ebase()
    ebase.main()


if __name__ == "__main__":
    main()

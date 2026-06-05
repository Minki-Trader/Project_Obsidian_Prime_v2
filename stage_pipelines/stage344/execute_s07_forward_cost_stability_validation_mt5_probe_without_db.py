from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage342 import (  # noqa: E402
    execute_f01_session_long_firewall_mt5_probe_without_db as runner,
)
from stage_pipelines.stage342 import (  # noqa: E402
    materialize_f01_session_long_firewall_mt5_probe_package_without_db as base_pkg,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as pkg,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_directional_long_supply_quality_surface_package_without_db as source_pkg,
)


BASE_BUILD_SUMMARY = runner.build_summary
BASE_WRITE_RECEIPTS = runner.write_receipts
HELPER = runner.ebase

setattr(pkg, "EXPECTED_PROBABILITY_TAPE", pkg.EXPECTED_TAPE)
setattr(pkg, "aw", base_pkg.aw)
setattr(pkg, "DEFAULT_COMMON_FILES", source_pkg.DEFAULT_COMMON_FILES)
setattr(pkg, "DEFAULT_TERMINAL", source_pkg.DEFAULT_TERMINAL)
setattr(pkg, "DEFAULT_TESTER_PROFILE_ROOT", source_pkg.DEFAULT_TESTER_PROFILE_ROOT)
setattr(pkg, "DEFAULT_PORTABLE_ROOT", source_pkg.DEFAULT_PORTABLE_ROOT)
setattr(pkg, "EA_BINARY", source_pkg.EA_BINARY)
setattr(pkg, "PORTABLE_EA_EX5", source_pkg.PORTABLE_EA_EX5)

TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344H"
RUN_ID = "run344H_execute_s07_forward_cost_stability_validation_mt5_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run344I_review_s07_forward_cost_stability_validation_mt5_probe_without_db_v1"
STATUS_COMPLETED = "completed_stage344H_s07_forward_cost_stability_validation_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage344H_s07_forward_cost_stability_validation_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_COMPLETED = "mt5_s07_forward_cost_stability_validation_outputs_available_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_s07_forward_cost_stability_validation_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage344H_open_run344I_review_s07_forward_cost_stability_validation_probe"
DECISION_BLOCKED = "stage344H_open_run344I_review_or_repair_s07_forward_cost_stability_validation_probe"
CLAIM_BOUNDARY = (
    "research_development_s07_forward_cost_stability_validation_mt5_runtime_probe_attempt_only_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344H_s07_forward_cost_stability_validation_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344H_s07_forward_cost_stability_validation_mt5_probe.md"
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
EXECUTION_SUMMARY = RUN_DIR / "s07_forward_cost_stability_mt5_probe_summary.csv"
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
    pkg.GATE_AUDIT,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.EXPECTED_TAPE,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.COST_STRESS_CONTRACT,
    pkg.SESSION_REGIME_PLAN,
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
            gate_row("parent_run344G_package_gates_passed", "passed" if final["parent_gate_passed"] else "failed", HELPER.rel(pkg.GATE_AUDIT), "run344G package(패키지) gate(게이트)를 이어받음"),
            gate_row("mt5_attempts_recorded", "passed" if final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] == 3 else "failed", HELPER.rel(MT5_EXECUTION_RESULT), "세 개 validation attempt(검증 시도)의 MT5 실행 기록을 남김"),
            gate_row("runtime_outputs_completed", "passed" if final["runtime_completed_rows"] == final["attempt_rows"] else "failed", HELPER.rel(RUNTIME_OUTPUT_COPY), "telemetry(텔레메트리) 출력 복사를 완료"),
            gate_row("strategy_tester_reports_collected", "passed" if final["report_completed_rows"] == final["attempt_rows"] else "failed", HELPER.rel(STRATEGY_TESTER_REPORTS), "Strategy Tester report(전략 테스터 보고서)를 수집"),
            gate_row("comparison_summary_materialized", "passed" if final["summary_rows"] == final["attempt_rows"] else "failed", HELPER.rel(EXECUTION_SUMMARY), "proxy-MT5 summary(프록시-MT5 요약)를 생성"),
            gate_row("exact_runtime_parity_reached", "passed" if final["matched_rows"] == final["expected_rows"] and final["mismatch_rows"] == 0 else "failed", HELPER.rel(PROXY_MT5_DIFF), "expected tape(예상 테이프)와 MT5 telemetry(MT5 텔레메트리)의 동등성을 확인"),
            gate_row("forensics_identity_recorded", "passed" if HELPER.exists(RUNTIME_IDENTITY) else "failed", HELPER.rel(RUNTIME_IDENTITY), "tester identity(테스터 정체성)를 기록"),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", HELPER.rel(FINAL_DECISION), "runtime probe(런타임 탐침)를 운영 주장으로 올리지 않음"),
            gate_row("required_gate_coverage_audit_written", "passed", HELPER.rel(GATE_AUDIT), "필수 게이트 커버리지 감사를 기록"),
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
    final = BASE_BUILD_SUMMARY(args, attempts, execution_results, report_records, summaries, diffs, copy_rows)
    final["source_package_run_id"] = SOURCE_PACKAGE_RUN_ID
    final["next_run_id"] = NEXT_RUN_ID
    if HELPER.exists(RUNTIME_IDENTITY):
        identity = HELPER.read_csv_direct(RUNTIME_IDENTITY)
        if "identity_id" in identity.columns:
            identity["identity_id"] = "stage344H_runtime_identity"
        HELPER.write_csv_direct(RUNTIME_IDENTITY, identity)
    return final


def write_receipts(final: Mapping[str, Any]) -> None:
    BASE_WRITE_RECEIPTS(final)
    if HELPER.exists(RUNTIME_RECEIPT):
        payload = HELPER.read_json_direct(RUNTIME_RECEIPT)
        payload["source_package_run_id"] = SOURCE_PACKAGE_RUN_ID
        payload["runtime_claim_boundary"] = "runtime_probe(런타임 탐침)"
        HELPER.write_json_direct(RUNTIME_RECEIPT, payload)


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344H s07 Forward/Cost/Stability MT5 Probe(344H s07 전진/비용/안정성 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run344G validation package(검증 패키지)의 s07/s05/s01 세 시도를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고, expected tape(예상 테이프)와 telemetry(텔레메트리)를 비교한다.

## Effect(효과)

run344I review(검토)가 비용 압박, 세션/국면 안정성, anchor/s05/s07 대조를 실제 MT5 근거 위에서 판단할 수 있다.

## Boundary(경계)

이 run(실행)은 runtime probe(런타임 탐침)이다. selection(선정), forward pass(전진 통과), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344H MT5 Probe Decision(344H MT5 탐침 결정)

- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{HELPER.rel(EXECUTION_SUMMARY)}`, `{HELPER.rel(PROXY_MT5_DIFF)}`, `{HELPER.rel(STRATEGY_TESTER_REPORTS)}`

Action(행동): s07 validation package(s07 검증 패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 실행한다.
Effect(효과): run344I가 cost/session/regime(비용/세션/국면) review(검토)를 할 수 있다.

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

run344H MT5 runtime probe(런타임 탐침)가 완료되었고, 다음은 run344I review(검토)이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_probe(최근 탐침): `{RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 근거를 review(검토)로 넘기고 운영 선정은 닫지 않는다.
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
    pkg.write_text(REPORT_PATH, report)
    pkg.write_text(DECISION_DOC, decision)
    pkg.write_text(CURRENT_WORKING_STATE, current)
    pkg.write_text(SELECTION_STATUS, selection)
    pkg.write_text(ROOT_SELECTION_STATUS, selection)
    pkg.write_text(WORKSPACE_STATE, workspace)
    marker = f"run344H {RUN_ID}"
    pkg.append_text_once(STAGE_BRIEF, marker, f"""## run344H s07 Validation MT5 Probe(344H s07 검증 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- effect(효과): run344I review(검토)를 열었다.
""")
    pkg.append_text_once(STAGE_README, marker, f"""## run344H s07 Validation MT5 Probe(344H s07 검증 MT5 탐침)

- report(보고서): `{HELPER.rel(REPORT_PATH)}`
- summary(요약): `{HELPER.rel(EXECUTION_SUMMARY)}`
- diff(차이): `{HELPER.rel(PROXY_MT5_DIFF)}`
- effect(효과): MT5 runtime evidence(런타임 근거)를 생성했다.
""")
    changelog = f"""## {TODAY} run344H s07 Validation MT5 Probe(s07 검증 MT5 탐침)

- action(행동): s07/s05/s01 검증 패키지를 MT5 Strategy Tester(MT5 전략 테스터)로 실행했다.
- effect(효과): 비용/세션/국면 review(검토)를 위한 런타임 근거를 만들었다.
- boundary(경계): 운영 승격/런타임 권위/목표 달성은 주장하지 않는다.
"""
    pkg.append_text_once(ROOT_CHANGELOG, marker, changelog)
    pkg.append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": HELPER.rel(FINAL_DECISION),
        "report_path": HELPER.rel(REPORT_PATH),
        "path": HELPER.rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base_row,
        "lane": "runtime_probe(MT5 런타임 탐침)",
        "family": "runtime_backtest(MT5/런타임 백테스트)",
        "primary_report": HELPER.rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "s07 validation MT5 runtime probe(s07 검증 MT5 런타임 탐침); review required(검토 필요).",
        "candidate_model_id": final["best_model_id"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "drawdown": final["best_max_drawdown_amount"],
        "recovery_factor": final["best_recovery_factor"],
        "trade_count": final["best_trade_count"],
        "expectancy": final["best_expectancy"],
        "attempt_count": final["attempt_rows"],
        "matched_rows": final["matched_rows"],
        "result_status": final["judgment"],
    }
    pkg.append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    rows = [
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_runtime_probe",
            "kpi_scope": "mt5_runtime_probe",
            "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
            "candidate_model_id": final["best_model_id"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_max_drawdown_amount"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": final["judgment"],
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"drawdown={final['best_max_drawdown_amount']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']}",
            "external_verification_status": final["external_verification_status"],
            "notes": "MT5 runtime probe complete(런타임 탐침 완료), review required(검토 필요), no selection(선정 없음).",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이번 MT5 probe(탐침) 범위 밖.",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
            "candidate_model_id": final["best_model_id"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_max_drawdown_amount"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"drawdown={final['best_max_drawdown_amount']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']}",
            "external_verification_status": final["external_verification_status"],
            "notes": "Tier B(티어 B)가 없으므로 combined(합산)는 Tier A와 같은 경계.",
        },
    ]
    pkg.append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], rows)
    pkg.append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], rows)


def configure_runner() -> None:
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
        "ROOT_SELECTION_STATUS": ROOT_SELECTION_STATUS,
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
        setattr(runner, key, value)


def main() -> None:
    configure_runner()
    runner.configure_ebase()
    runner.ebase.main()


if __name__ == "__main__":
    main()

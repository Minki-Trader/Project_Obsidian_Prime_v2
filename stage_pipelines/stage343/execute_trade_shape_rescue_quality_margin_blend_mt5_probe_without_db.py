from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage342 import execute_f01_session_long_firewall_mt5_probe_without_db as runner  # noqa: E402
from stage_pipelines.stage343 import (  # noqa: E402
    materialize_trade_shape_rescue_quality_margin_blend_package_without_db as pkg,
)


BASE_BUILD_SUMMARY = runner.build_summary
BASE_WRITE_RECEIPTS = runner.write_receipts

HELPER = runner.ebase

TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run343E"
RUN_ID = "run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1"
STATUS_COMPLETED = "completed_stage343E_trade_shape_rescue_quality_margin_blend_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage343E_trade_shape_rescue_quality_margin_blend_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_COMPLETED = "mt5_trade_shape_rescue_quality_margin_blend_probe_outputs_available_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_trade_shape_rescue_quality_margin_blend_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage343E_open_run343F_review_trade_shape_rescue_quality_margin_blend_probe"
DECISION_BLOCKED = "stage343E_open_run343F_review_or_repair_trade_shape_rescue_quality_margin_blend_probe"
CLAIM_BOUNDARY = (
    "research_development_trade_shape_rescue_quality_margin_blend_mt5_runtime_probe_attempt_only_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run343E_trade_shape_rescue_quality_margin_blend_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage343E_trade_shape_rescue_quality_margin_blend_mt5_probe.md"
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
EXECUTION_SUMMARY = RUN_DIR / "trade_shape_rescue_quality_margin_blend_mt5_probe_summary.csv"
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
            gate_row(
                "parent_343D_package_gates_passed",
                "passed" if final["parent_gate_passed"] else "failed",
                HELPER.rel(pkg.GATE_AUDIT),
                "run343D(343D 실행) package gate(패키지 게이트)를 이어받는다.",
            ),
            gate_row(
                "mt5_attempts_recorded",
                "passed" if final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0 else "failed",
                HELPER.rel(MT5_EXECUTION_RESULT),
                "각 attempt(시도)의 MT5(메타트레이더5) 실행 결과를 기록한다.",
            ),
            gate_row(
                "runtime_outputs_completed",
                "passed" if final["runtime_completed_rows"] == final["attempt_rows"] else "failed",
                HELPER.rel(RUNTIME_OUTPUT_COPY),
                "모든 telemetry(런타임 기록)를 복사한다.",
            ),
            gate_row(
                "strategy_tester_reports_collected",
                "passed" if final["report_completed_rows"] == final["attempt_rows"] else "failed",
                HELPER.rel(STRATEGY_TESTER_REPORTS),
                "각 Strategy Tester report(전략 테스터 보고서)를 수집한다.",
            ),
            gate_row(
                "comparison_summary_materialized",
                "passed" if final["summary_rows"] == final["attempt_rows"] else "failed",
                HELPER.rel(EXECUTION_SUMMARY),
                "proxy-MT5 summary(프록시-MT5 요약)를 만든다.",
            ),
            gate_row(
                "exact_runtime_parity_reached",
                "passed" if final["matched_rows"] == final["expected_rows"] and final["mismatch_rows"] == 0 else "failed",
                HELPER.rel(PROXY_MT5_DIFF),
                "expected tape(예상 테이프)와 MT5 telemetry(MT5 기록)의 row-level parity(행 단위 동등성)를 확인한다.",
            ),
            gate_row(
                "forensics_identity_recorded",
                "passed" if HELPER.exists(RUNTIME_IDENTITY) else "failed",
                HELPER.rel(RUNTIME_IDENTITY),
                "tester identity(테스터 정체성)를 기록한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed" if no_forbidden else "failed",
                HELPER.rel(FINAL_DECISION),
                "runtime probe(런타임 탐침)를 selection(선정), operating promotion(운영 승격), Goal Achieve(목표 달성)로 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                HELPER.rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
            ),
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
    if HELPER.exists(RUNTIME_IDENTITY):
        identity = HELPER.read_csv_direct(RUNTIME_IDENTITY)
        if "identity_id" in identity.columns:
            identity["identity_id"] = "stage343E_runtime_identity"
        HELPER.write_csv_direct(RUNTIME_IDENTITY, identity)
    return final


def write_receipts(final: Mapping[str, Any]) -> None:
    BASE_WRITE_RECEIPTS(final)
    runtime_payload = HELPER.read_json_direct(RUNTIME_RECEIPT)
    runtime_payload["source_package_run_id"] = SOURCE_PACKAGE_RUN_ID
    runtime_payload["runtime_claim_boundary"] = "runtime_probe(런타임 탐침)" if final["runtime_completed_rows"] else "blocked(차단)"
    HELPER.write_json_direct(RUNTIME_RECEIPT, runtime_payload)
    lineage_payload = HELPER.read_json_direct(LINEAGE_RECEIPT)
    lineage_payload["source_inputs"] = [HELPER.rel(path) for path in INPUT_FILES]
    lineage_payload["producer"] = HELPER.rel(Path(__file__))
    lineage_payload["lineage_judgment"] = "connected_with_trade_shape_rescue_runtime_probe_boundary(거래 형태 복구 런타임 탐침 경계로 연결)"
    HELPER.write_json_direct(LINEAGE_RECEIPT, lineage_payload)


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run343E Trade Shape Rescue Quality Margin Blend MT5 Probe(343E 거래 형태 복구 품질 마진 혼합 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- report_completed_rows(보고서 완료 행): `{final['report_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_expectancy(최고 기대값): `{final['best_expectancy']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 시도 낙폭): `{final['best_max_drawdown_amount']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- best_long_short(최고 롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run343D(343D 실행)의 trade shape rescue(거래 형태 복구) package(패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고, expected tape(예상 테이프)와 telemetry(런타임 기록)를 비교했다.

## Effect(효과)

run343F(343F 실행)가 net profit(순수익), profit factor(수익 팩터), expectancy(기대값), drawdown(낙폭), recovery factor(회복 계수), trade count(거래수), long/short balance(롱/숏 균형), proxy-MT5 diff(프록시-MT5 차이)를 실제 runtime evidence(런타임 근거)로 검토할 수 있다.

## Boundary(경계)

run343E(343E 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage343E MT5 Probe Decision(343E MT5 탐침 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{HELPER.rel(MT5_EXECUTION_RESULT)}`, `{HELPER.rel(EXECUTION_SUMMARY)}`, `{HELPER.rel(PROXY_MT5_DIFF)}`

Action(행동): trade shape rescue(거래 형태 복구) package(패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
Effect(효과): run343F(343F 실행)가 KPI(핵심 성과 지표), side filter effect(사이드 필터 효과), proxy-MT5 diff(프록시-MT5 차이)를 판정할 수 있다.

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

run343E(343E 실행)는 trade shape rescue(거래 형태 복구) package(패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다. run343F(343F 실행)는 결과를 검토해 preserved clue(보존 단서), failure memory(실패 기억), next offensive seed(다음 공격 탐색 씨앗)를 분리한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 343 Selection Status(343단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 result(MT5 결과)를 바로 selection(선정)으로 오해하지 않고 review(검토)로 넘긴다.
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
    HELPER.write_bom_text_direct(REPORT_PATH, report)
    HELPER.write_bom_text_direct(DECISION_DOC, decision)
    HELPER.write_bom_text_direct(CURRENT_WORKING_STATE, current)
    HELPER.write_bom_text_direct(SELECTION_STATUS, selection)
    HELPER.write_bom_text_direct(ROOT_SELECTION_STATUS, selection)
    HELPER.write_bom_text_direct(WORKSPACE_STATE, workspace)
    marker = f"run343E {RUN_ID}"
    HELPER.append_text_once_direct(
        STAGE_BRIEF,
        marker,
        f"""## run343E Trade Shape Rescue MT5 Probe(343E 거래 형태 복구 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- effect(효과): run343D package(343D 패키지)를 실제 MT5(메타트레이더5) 근거로 바꾼다.
""",
    )
    HELPER.append_text_once_direct(
        STAGE_README,
        marker,
        f"""## run343E Trade Shape Rescue MT5 Probe(343E 거래 형태 복구 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- summary(요약): `{HELPER.rel(EXECUTION_SUMMARY)}`
- diff(차이): `{HELPER.rel(PROXY_MT5_DIFF)}`
- effect(효과): run343F(343F 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.
""",
    )
    changelog = f"""## {TODAY} run343E Trade Shape Rescue MT5 Probe(거래 형태 복구 MT5 탐침)

- action(행동): trade shape rescue(거래 형태 복구) `{final['attempt_rows']}`개를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
- effect(효과): matched_rows(일치 행) `{final['matched_rows']}/{final['expected_rows']}`, best_attempt(최고 시도) `{final['best_attempt_name']}`를 기록했다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    HELPER.append_text_once_direct(ROOT_CHANGELOG, marker, changelog)
    HELPER.append_text_once_direct(WORKSPACE_CHANGELOG, marker, changelog)


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
        "primary_artifact": HELPER.rel(FINAL_DECISION),
        "report_path": HELPER.rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    HELPER.append_or_replace_csv_direct(
        RUN_REGISTRY,
        ["run_id"],
        {
            **base_row,
            "lane": "runtime_probe(MT5 런타임 탐침)",
            "path": HELPER.rel(FINAL_DECISION),
            "family": "runtime_backtest(MT5/런타임/백테스트 실행)",
            "notes": "Trade shape rescue quality margin blend(거래 형태 복구 품질 마진 혼합) MT5 runtime probe(런타임 탐침), review required(검토 필요).",
            "primary_report": HELPER.rel(REPORT_PATH),
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "candidate_model_id": final.get("best_model_id", ""),
            "result_status": final["judgment"],
            "sample_rows": final["expected_rows"],
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
        },
    )
    rows = [
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "mt5_runtime_probe",
            "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
            "path": HELPER.rel(REPORT_PATH),
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"drawdown={final['best_max_drawdown_amount']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']}",
            "external_verification_status": final["external_verification_status"],
            "notes": "MT5 runtime probe(MT5 런타임 탐침) complete, review required(검토 필요), no selection(선정 없음).",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe",
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_max_drawdown_amount"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "candidate_model_id": final["best_model_id"],
            "result_status": final["judgment"],
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
            "path": HELPER.rel(REPORT_PATH),
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이 MT5 probe(MT5 탐침)의 범위 밖이므로 missing_required(필수 누락)로 기록한다.",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "runtime_probe(MT5 런타임 탐침)",
            "path": HELPER.rel(REPORT_PATH),
            "primary_kpi": f"net_profit={final['best_net_profit']};pf={final['best_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"drawdown={final['best_max_drawdown_amount']};long_short={final['best_long_trade_count']}/{final['best_short_trade_count']}",
            "external_verification_status": final["external_verification_status"],
            "notes": "Tier B(티어 B)가 없으므로 combined(합산)는 Tier A(티어 A)와 동일 경계로 기록한다.",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "attempt_count": final["attempt_rows"],
            "matched_rows": final["matched_rows"],
            "net_profit": final["best_net_profit"],
            "profit_factor": final["best_profit_factor"],
            "expectancy": final["best_expectancy"],
            "drawdown": final["best_max_drawdown_amount"],
            "recovery_factor": final["best_recovery_factor"],
            "trade_count": final["best_trade_count"],
            "candidate_model_id": final["best_model_id"],
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    for row in rows:
        HELPER.append_or_replace_csv_direct(PROJECT_LEDGER, ["run_id", "view"], row)
        HELPER.append_or_replace_csv_direct(STAGE_LEDGER, ["run_id", "view"], row)


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

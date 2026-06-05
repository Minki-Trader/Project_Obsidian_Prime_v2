from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import execute_trade_count_recovery_expansion_mt5_probe_without_db as base
from stage_pipelines.stage338 import materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db as pkg


TODAY = "2026-06-01"
RUN_NUMBER = "run338N"
RUN_ID = "run338N_execute_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run338O_review_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_without_db_v1"
STATUS_COMPLETED = "completed_stage338N_lifecycle_exit_side_balance_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage338N_lifecycle_exit_side_balance_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_COMPLETED = "mt5_lifecycle_exit_side_balance_probe_outputs_available_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_lifecycle_exit_side_balance_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage338N_open_run338O_review_lifecycle_exit_side_balance_probe"
DECISION_BLOCKED = "stage338N_open_run338O_review_or_repair_lifecycle_exit_side_balance_probe"
CLAIM_BOUNDARY = (
    "research_development_lifecycle_exit_side_balance_mt5_runtime_probe_attempt_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338N_lifecycle_probe.md"
DECISION_DOC = base.ROOT / "docs" / "decisions" / f"{TODAY}_stage338N_lifecycle_probe.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = base.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = base.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = base.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = base.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = base.ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = base.ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = base.ROOT / "docs" / "workspace" / "changelog.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "lifecycle_exit_mt5_probe_summary.csv"
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


def rel(path: Path | str) -> str:
    return base.rel(path)


def exists(path: Path | str) -> bool:
    return base.exists(path)


def ensure_parent(path: Path) -> None:
    pkg.io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv_direct(path: Path) -> pd.DataFrame:
    return pd.read_csv(pkg.io(path), encoding="utf-8-sig")


def write_csv_direct(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(pkg.io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def read_json_direct(path: Path) -> Any:
    return json.loads(pkg.io(path).read_text(encoding="utf-8-sig"))


def write_json_direct(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    pkg.io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_bom_text_direct(path: Path, text: str) -> Path:
    ensure_parent(path)
    pkg.io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def append_text_once_direct(path: Path, marker: str, text: str) -> None:
    current = pkg.io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text_direct(path, next_text)


def append_or_replace_csv_direct(path: Path, key_columns: list[str] | tuple[str, ...], row: Mapping[str, Any]) -> None:
    frame = read_csv_direct(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv_direct(path, frame[ordered])


def passed_status_direct(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin({"passed", "pass", "true", "1", "ok", "completed"})


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
            gate_row("parent_338M_gates_passed", "passed" if final["parent_gate_passed"] else "failed", rel(pkg.GATE_AUDIT), "run338M(338M 실행) package gate(패키지 게이트)를 이어받는다."),
            gate_row("mt5_attempts_recorded", "passed" if final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0 else "failed", rel(MT5_EXECUTION_RESULT), "각 attempt(시도)의 실행 결과를 기록한다."),
            gate_row("runtime_outputs_completed", "passed" if final["runtime_completed_rows"] == final["attempt_rows"] else "failed", rel(RUNTIME_OUTPUT_COPY), "모든 telemetry(런타임 기록)를 복사한다."),
            gate_row("strategy_tester_reports_collected", "passed" if final["report_completed_rows"] == final["attempt_rows"] else "failed", rel(STRATEGY_TESTER_REPORTS), "각 Strategy Tester report(전략 테스터 보고서)를 수집한다."),
            gate_row("comparison_summary_materialized", "passed" if final["summary_rows"] == final["attempt_rows"] else "failed", rel(EXECUTION_SUMMARY), "proxy-MT5 summary(프록시-MT5 요약)를 만든다."),
            gate_row("exact_runtime_parity_reached", "passed" if final["matched_rows"] == final["expected_rows"] and final["mismatch_rows"] == 0 else "failed", rel(PROXY_MT5_DIFF), "expected tape(예상 테이프)와 MT5 telemetry(MT5 기록)가 정확히 맞는지 확인한다."),
            gate_row("forensics_identity_recorded", "passed" if exists(RUNTIME_IDENTITY) else "failed", rel(RUNTIME_IDENTITY), "tester identity(테스터 정체성)를 기록한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(FINAL_DECISION), "runtime probe(런타임 탐침)를 선정/운영/목표 달성으로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 기록한다."),
        ]
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338N Lifecycle Exit Side Balance MT5 Probe(생명주기 청산 방향 균형 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338M(338M 실행)의 lifecycle/exit package(생명주기/청산 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(런타임 기록)를 expected tape(예상 테이프)와 비교했다.

Effect(효과): 회복 계수(recovery factor, 회복 계수), 낙폭(drawdown, 낙폭), 방향 균형(side balance, 방향 균형)이 실행 생명주기(lifecycle, 생명주기)로 개선되는지 검토할 근거를 만든다.

## Boundary(경계)

run338N(338N 실행)은 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338N Decision(338N 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(MT5_EXECUTION_RESULT)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`

Action(행동): lifecycle/exit(생명주기/청산) 변형을 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.

Effect(효과): run338O(338O 실행)이 KPI(핵심 성과 지표), trade count(거래수), recovery factor(회복 계수), proxy-MT5 diff(프록시-MT5 차이)를 판정할 수 있다.

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

run338N(338N 실행)은 MT5 runtime probe(MT5 런타임 탐침)를 실행했다. run338O(338O 실행)은 결과를 검토해 lifecycle/exit(생명주기/청산) 변형이 운영 후보로 갈 수 있는지 판정해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

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

Effect(효과): 실행 결과를 바로 선정으로 오해하지 않게 한다.
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
    base.write_bom_text(REPORT_PATH, report)
    base.write_bom_text(DECISION_DOC, decision)
    base.write_bom_text(CURRENT_WORKING_STATE, current)
    base.write_bom_text(SELECTION_STATUS, selection)
    base.write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run338N {RUN_ID}"
    base.append_text_once(STAGE_BRIEF, marker, f"""## run338N Lifecycle Exit MT5 Probe(생명주기 청산 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- effect(효과): lifecycle/exit(생명주기/청산) 변형을 실제 MT5(메타트레이더5) 근거로 바꿨다.
""")
    base.append_text_once(STAGE_README, marker, f"""## run338N Lifecycle Exit MT5 Probe(생명주기 청산 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- summary(요약): `{rel(EXECUTION_SUMMARY)}`
- diff(차이): `{rel(PROXY_MT5_DIFF)}`
- effect(효과): Stage338(338단계)이 package(패키지)에서 lifecycle runtime evidence(생명주기 런타임 근거)로 이동했다.
""")
    changelog = f"""## {TODAY} run338N Lifecycle Exit MT5 Probe(생명주기 청산 MT5 탐침)

- action(행동): lifecycle/exit(생명주기/청산) `{final['attempt_rows']}`개를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.
- effect(효과): matched_rows(일치 행) `{final['matched_rows']}/{final['expected_rows']}`, best_attempt(최고 시도) `{final['best_attempt_name']}`를 기록했다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    base.append_text_once(ROOT_CHANGELOG, marker, changelog)
    base.append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def configure_base() -> None:
    replacements = {
        "aw": pkg.aw,
        "pkg": pkg,
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "STAGE_DIR": STAGE_DIR,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": pkg.RUN_ID,
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
        "read_csv": read_csv_direct,
        "write_csv": write_csv_direct,
        "read_json": read_json_direct,
        "write_json": write_json_direct,
        "write_bom_text": write_bom_text_direct,
        "append_text_once": append_text_once_direct,
        "append_or_replace_csv": append_or_replace_csv_direct,
        "passed_status": passed_status_direct,
        "make_gates": make_gates,
        "write_docs": write_docs,
    }
    for key, value in replacements.items():
        setattr(base, key, value)


def main() -> None:
    configure_base()
    base.main()


if __name__ == "__main__":
    main()

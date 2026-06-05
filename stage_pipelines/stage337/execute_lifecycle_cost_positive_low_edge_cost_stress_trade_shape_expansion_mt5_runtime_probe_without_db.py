from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    execute_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_mt5_runtime_probe_without_db as execute_base,
)
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_runtime_probe_package_without_db as iz,
)
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_runtime_probe_package_without_db as package_base,
)


aw = iz.aw

TODAY = "2026-06-01"
STAGE_ID = iz.STAGE_ID
STAGE_DIR = iz.STAGE_DIR
RUN_NUMBER = "run337JA"
RUN_ID = "run337JA_execute_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = iz.RUN_ID
NEXT_RUN_ID = "run337JB_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_mt5_runtime_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage337JA_positive_low_edge_expansion_mt5_runtime_probe_executed_review_required_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337JA_positive_low_edge_expansion_mt5_runtime_probe_attempt_missing_or_failed_outputs_no_forward_decision"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage337JA_open_run337JB_review_positive_low_edge_expansion_mt5_runtime_probe"
DECISION_BLOCKED = "stage337JA_open_run337JB_review_or_repair_positive_low_edge_expansion_mt5_runtime_probe_attempt"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DEFAULT_TESTER_PROFILE_ROOT = package_base.DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = package_base.DEFAULT_PORTABLE_ROOT

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JA_positive_low_edge_expansion_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JA_positive_low_edge_expansion_mt5_runtime_probe.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "positive_low_edge_expansion_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    iz.FINAL_DECISION,
    iz.GATE_AUDIT,
    iz.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    iz.EXPECTED_PROBABILITY_TAPE,
    iz.COMMON_FILES_SYNC,
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
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def configure_execute_engine() -> None:
    parent_package = SimpleNamespace(
        aw=aw,
        STAGE_ID=STAGE_ID,
        STAGE_DIR=STAGE_DIR,
        RUN_ID=iz.RUN_ID,
        FINAL_DECISION=iz.FINAL_DECISION,
        GATE_AUDIT=iz.GATE_AUDIT,
        RUNTIME_PROBE_ATTEMPT_PACKAGE=iz.RUNTIME_PROBE_ATTEMPT_PACKAGE,
        EXPECTED_PROBABILITY_TAPE=iz.EXPECTED_PROBABILITY_TAPE,
        COMMON_FILES_SYNC=iz.COMMON_FILES_SYNC,
        RUNTIME_PARITY_CONTRACT=iz.RUNTIME_PARITY_CONTRACT,
        TESTER_IDENTITY_CONTRACT=iz.TESTER_IDENTITY_CONTRACT,
        DEFAULT_PORTABLE_ROOT=package_base.DEFAULT_PORTABLE_ROOT,
        DEFAULT_TERMINAL=package_base.DEFAULT_TERMINAL,
        DEFAULT_METAEDITOR=package_base.DEFAULT_METAEDITOR,
        DEFAULT_COMMON_FILES=package_base.DEFAULT_COMMON_FILES,
        PORTABLE_EA_EX5=package_base.PORTABLE_EA_EX5,
        EA_BINARY=package_base.EA_BINARY,
    )
    execute_base.__file__ = __file__
    execute_base.ir = parent_package
    execute_base.aw = aw
    execute_base.TODAY = TODAY
    execute_base.STAGE_ID = STAGE_ID
    execute_base.STAGE_DIR = STAGE_DIR
    execute_base.RUN_NUMBER = RUN_NUMBER
    execute_base.RUN_ID = RUN_ID
    execute_base.PARENT_RUN_ID = PARENT_RUN_ID
    execute_base.NEXT_RUN_ID = NEXT_RUN_ID
    execute_base.STATUS_COMPLETED = STATUS_COMPLETED
    execute_base.STATUS_BLOCKED = STATUS_BLOCKED
    execute_base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    execute_base.JUDGMENT_BLOCKED = JUDGMENT_BLOCKED
    execute_base.DECISION_COMPLETED = DECISION_COMPLETED
    execute_base.DECISION_BLOCKED = DECISION_BLOCKED
    execute_base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    execute_base.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
    execute_base.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
    execute_base.RUN_DIR = RUN_DIR
    execute_base.MT5_DIR = MT5_DIR
    execute_base.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    execute_base.REPORT_COPY_DIR = REPORT_COPY_DIR
    execute_base.REVIEW_DIR = REVIEW_DIR
    execute_base.REPORT_PATH = REPORT_PATH
    execute_base.DECISION_DOC = DECISION_DOC
    execute_base.RUN_REGISTRY = RUN_REGISTRY
    execute_base.PROJECT_LEDGER = PROJECT_LEDGER
    execute_base.STAGE_LEDGER = STAGE_LEDGER
    execute_base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    execute_base.WORKSPACE_STATE = WORKSPACE_STATE
    execute_base.CURRENT_WORKING_STATE = CURRENT_WORKING_STATE
    execute_base.SELECTION_STATUS = SELECTION_STATUS
    execute_base.STAGE_BRIEF = STAGE_BRIEF
    execute_base.ROOT_CHANGELOG = ROOT_CHANGELOG
    execute_base.WORKSPACE_CHANGELOG = WORKSPACE_CHANGELOG
    execute_base.ATTEMPT_PACKAGE = ATTEMPT_PACKAGE
    execute_base.TERMINAL_PROCESS_AUDIT = TERMINAL_PROCESS_AUDIT
    execute_base.MT5_EXECUTION_RESULT = MT5_EXECUTION_RESULT
    execute_base.STRATEGY_TESTER_REPORTS = STRATEGY_TESTER_REPORTS
    execute_base.EXECUTION_SUMMARY = EXECUTION_SUMMARY
    execute_base.PROXY_MT5_DIFF = PROXY_MT5_DIFF
    execute_base.TELEMETRY_SKIP_SUMMARY = TELEMETRY_SKIP_SUMMARY
    execute_base.RUNTIME_OUTPUT_COPY = RUNTIME_OUTPUT_COPY
    execute_base.RUNTIME_IDENTITY = RUNTIME_IDENTITY
    execute_base.BACKTEST_FORENSICS_RECEIPT = BACKTEST_FORENSICS_RECEIPT
    execute_base.RUNTIME_RECEIPT = RUNTIME_RECEIPT
    execute_base.PERFORMANCE_RECEIPT = PERFORMANCE_RECEIPT
    execute_base.JUDGMENT_RECEIPT = JUDGMENT_RECEIPT
    execute_base.LINEAGE_RECEIPT = LINEAGE_RECEIPT
    execute_base.CLAIM_RECEIPT = CLAIM_RECEIPT
    execute_base.GATE_AUDIT = GATE_AUDIT
    execute_base.FINAL_DECISION = FINAL_DECISION
    execute_base.RUN_MANIFEST = RUN_MANIFEST
    execute_base.INPUT_FILES = INPUT_FILES
    execute_base.OUTPUT_FILES = OUTPUT_FILES
    execute_base.runtime_identity = runtime_identity
    execute_base.make_gates = make_gates
    execute_base.write_receipts = write_receipts
    execute_base.write_docs = write_docs
    execute_base.update_registers = update_registers


def runtime_identity(attempt_rows: int, args: Any) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "identity_id": "stage337JA_runtime_identity",
                "terminal_path": str(args.terminal_path),
                "terminal_exists": exists(Path(args.terminal_path)),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "terminal_data_root": str(args.terminal_data_root),
                "portable_ea_ex5": package_base.PORTABLE_EA_EX5.as_posix(),
                "portable_ea_ex5_exists": exists(package_base.PORTABLE_EA_EX5),
                "portable_ea_ex5_sha256": sha(package_base.PORTABLE_EA_EX5) if exists(package_base.PORTABLE_EA_EX5) else "",
                "repo_ea_binary": package_base.EA_BINARY.as_posix(),
                "repo_ea_binary_exists": exists(package_base.EA_BINARY),
                "repo_ea_binary_sha256": sha(package_base.EA_BINARY) if exists(package_base.EA_BINARY) else "",
                "attempt_rows": attempt_rows,
                "tester_symbol": "US100",
                "tester_timeframe": "M5",
                "tester_model": "4 real ticks(실제 틱)",
                "deposit": "500",
                "leverage": "1:100",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(iz.GATE_AUDIT)
    attempt_or_block = final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
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
            gate_row("parent_iz_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(iz.GATE_AUDIT), "IZ package(IZ 패키지) gate(게이트)가 통과한 뒤에만 JA execution(JA 실행)을 시작한다."),
            gate_row("mt5_attempt_or_block_recorded", "passed" if attempt_or_block else "failed", rel(MT5_EXECUTION_RESULT), "각 attempt(시도)의 MT5 output(MT5 출력) 또는 blocker(차단 사유)를 기록한다."),
            gate_row("runtime_output_copy_recorded", "passed" if final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2 else "failed", rel(RUNTIME_OUTPUT_COPY), "telemetry/summary(런타임 기록/요약) 복사 감사를 남긴다."),
            gate_row("comparison_summary_materialized", "passed" if final["summary_rows"] == final["attempt_rows"] else "failed", rel(EXECUTION_SUMMARY), "proxy-MT5 summary(프록시-MT5 요약)를 만든다."),
            gate_row("diff_or_blocker_materialized", "passed" if final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0 else "failed", rel(PROXY_MT5_DIFF), "diff rows(차이 행) 또는 blocker state(차단 상태)를 기록한다."),
            gate_row("forensics_identity_recorded", "passed" if exists(RUNTIME_IDENTITY) else "failed", rel(RUNTIME_IDENTITY), "tester identity(테스터 정체성)를 기록한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(FINAL_DECISION), "selection/forward/runtime authority/Goal(선택/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(ATTEMPT_PACKAGE),
            "shared_contract": rel(iz.RUNTIME_PARITY_CONTRACT),
            "known_differences": "proxy expected value(프록시 예상값)는 신호 점검이고 MT5(메타트레이더5)는 broker lifecycle execution(브로커 생명주기 실행)이다.",
            "parity_check": rel(PROXY_MT5_DIFF),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침) only, no authority(권위 없음)",
            "attempt_rows": final["attempt_rows"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "comparison_status": final["comparison_status"],
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(RUNTIME_IDENTITY),
            "ea_identity": rel(iz.TESTER_IDENTITY_CONTRACT),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": {
                "net_profit": final["net_profit"],
                "profit_factor": final["profit_factor"],
                "trade_count": final["trade_count"],
                "drawdown": final["max_drawdown_amount"],
            },
            "cost_assumptions": "IZ .set(IZ 설정) fixed lot(고정 랏) 0.10, argmax probe(최대확률 탐침), no threshold tuning(임계값 조정 없음)",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "backtest_judgment": "usable_with_boundary(경계 조건부 사용 가능)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "summary": rel(EXECUTION_SUMMARY),
            "diff": rel(PROXY_MT5_DIFF),
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "net_profit": final["net_profit"],
            "profit_factor": final["profit_factor"],
            "expectancy": final["expectancy"],
            "recovery_factor": final["recovery_factor"],
            "trade_count": final["trade_count"],
            "allowed_use": "runtime probe review only(런타임 탐침 검토 전용)",
            "forbidden_use": "Forward Passed/Failed or Goal claim(전진 통과/실패 또는 목표 주장)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": final["decision"],
            "next_run_id": NEXT_RUN_ID,
            "judgment_class": "inconclusive(불충분)" if final["runtime_completed_rows"] == 0 else "runtime_probe_review_required(런타임 탐침 검토 필요)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 해시 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
        },
    )


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JA Positive Low-Edge Cost-Stress MT5 Runtime Probe(run337JA 양성 저마진 비용압박 MT5 런타임 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- trade_count(거래수): `{final['trade_count']}`
- blocker(차단 사유): `{final['blocker']}`

## Action(행동)

IZ package(IZ 패키지)의 cost-stress ONNX(비용압박 ONNX) 후보를 MT5 runtime probe(MT5 런타임 탐침)로 실행하거나 차단 사유를 기록했다.
Effect(효과): proxy expected value(프록시 예상값)가 MT5 output(MT5 출력) 또는 blocker(차단 사유)와 연결된다.

## Boundary(경계)

이번 실행은 runtime probe attempt(런타임 탐침 시도)만 뜻한다. Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

## Next(다음)

`{NEXT_RUN_ID}`에서 runtime evidence(런타임 근거), proxy-MT5 diff(프록시-MT5 차이), repair need(수리 필요)를 검토한다.
"""
    decision = f"""# {TODAY} Stage337JA Decision(337JA 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`, `{rel(MT5_EXECUTION_RESULT)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침)를 실행하거나 차단 사유를 기록했다.
Effect(효과): proxy(프록시)를 MT5 runtime evidence(MT5 런타임 근거) 없이 운영 주장으로 올리지 않게 한다.

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

JA는 MT5 runtime probe(MT5 런타임 탐침)를 시도했고, 이제 JB review(JB 검토)가 diff(차이)와 blocker(차단 사유)를 판정해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선택 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['primary_model_id']}`
- mt5_runtime_probe(MT5 런타임 탐침): `attempted(시도됨)`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 attempt(MT5 시도)를 operating promotion(운영 승격)으로 오해하지 않게 한다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run337JA {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JA MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): proxy(프록시)를 MT5 runtime evidence(MT5 런타임 근거) 또는 blocker(차단 사유)에 연결했다.
""",
    )
    changelog_entry = f"""## {TODAY} run337JA MT5 Runtime Probe(MT5 런타임 탐침)

- action(행동): MT5 runtime probe(MT5 런타임 탐침)를 `{final['attempt_rows']}`개 시도했다.
- effect(효과): runtime_completed_rows(런타임 완료 행) `{final['runtime_completed_rows']}`, matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`를 기록했다.
- boundary(경계): selected model(선택 모델), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
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
    write_csv(path, frame[ordered])


def update_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    rows = [
        {
            **base_row,
            "view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_attempt",
            "candidate_model_id": final["primary_model_id"],
            "net_profit": final["net_profit"],
            "profit_factor": final["profit_factor"],
            "expectancy": final["expectancy"],
            "drawdown": final["max_drawdown_amount"],
            "recovery_factor": final["recovery_factor"],
            "trade_count": final["trade_count"],
            "long_trade_count": final["long_trade_count"],
            "short_trade_count": final["short_trade_count"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "result_status": final["judgment"],
        },
        {
            **base_row,
            "view": "Tier B fallback used(Tier B 대체 사용)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base_row,
            "view": "actual routed total(실제 라우팅 전체)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    configure_execute_engine()
    execute_base.main()


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage340 import materialize_f01_local_floor_pressure_mt5_probe_package_without_db as src


TODAY = "2026-06-01"

STAGE_ID = src.STAGE_ID
SOURCE_STAGE_ID = src.SOURCE_STAGE_ID
STAGE_DIR = src.STAGE_DIR
SOURCE_STAGE_DIR = src.SOURCE_STAGE_DIR

RUN_NUMBER = "run340F"
RUN_ID = "run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = "run340E_review_f01_local_floor_pressure_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run340G_execute_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1"

STATUS = "completed_stage340F_f01_close_on_flat_false_pressure_probe_package_materialized_no_selection"
JUDGMENT = "f01_close_on_flat_false_pressure_mt5_probe_package_ready_runtime_execution_required_no_selection"
DECISION = "stage340F_open_run340G_execute_f01_close_on_flat_false_pressure_probe"
CLAIM_BOUNDARY = (
    "research_development_f01_close_on_flat_false_pressure_runtime_probe_package_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run340F_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage340F_f01_close_on_flat_false_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run340E"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_QUEUE = PARENT_RUN_DIR / "run340F_queue.csv"
PARENT_SCORECARD = PARENT_RUN_DIR / "f01_pressure_review_scorecard.csv"

SOURCE_PACKAGE_DIR = src.SOURCE_PACKAGE_DIR
SOURCE_FEATURE_MATRIX = src.SOURCE_FEATURE_MATRIX
SOURCE_EXPECTED_TAPE = src.SOURCE_EXPECTED_TAPE
SOURCE_MODEL_MANIFEST = src.SOURCE_MODEL_MANIFEST
SOURCE_MODEL_PATH = src.SOURCE_MODEL_PATH
SOURCE_ATTEMPT_PACKAGE = src.SOURCE_ATTEMPT_PACKAGE
SOURCE_ATTEMPT_NAME = src.SOURCE_ATTEMPT_NAME

DEFAULT_COMMON_FILES = src.DEFAULT_COMMON_FILES
DEFAULT_TERMINAL = src.DEFAULT_TERMINAL
DEFAULT_TESTER_PROFILE_ROOT = src.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = src.DEFAULT_PORTABLE_ROOT
EA_BINARY = src.EA_BINARY
PORTABLE_EA_EX5 = src.PORTABLE_EA_EX5
aw = src.aw

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage340/{RUN_NUMBER}_f01_close_on_flat_false_pressure_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage340_F01CloseOnFlatFalsePressure__ONNX"
MAGIC_BASE = 3407600

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_TAPE
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
VARIANT_PREVIEW = RUN_DIR / "variant_preview.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN340G_EXECUTION_QUEUE = RUN_DIR / "run340G_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = src.WORKSPACE_STATE
CURRENT_WORKING_STATE = src.CURRENT_WORKING_STATE
ROOT_CHANGELOG = src.ROOT_CHANGELOG
WORKSPACE_CHANGELOG = src.WORKSPACE_CHANGELOG
RUN_REGISTRY = src.RUN_REGISTRY
PROJECT_LEDGER = src.PROJECT_LEDGER
ARTIFACT_REGISTRY = src.ARTIFACT_REGISTRY


def output_paths() -> list[Path]:
    return [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        VARIANT_PREVIEW,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        TESTER_IDENTITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUNTIME_PARITY_CONTRACT,
        RUN340G_EXECUTION_QUEUE,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        RUNTIME_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def build_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gate_passed = False
    if PARENT_GATE_AUDIT.exists():
        parent_gates = src.base.read_csv(PARENT_GATE_AUDIT)
        parent_gate_passed = parent_gates["status"].astype(str).str.lower().eq("passed").all()
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
    )
    preview = src.base.read_csv(VARIANT_PREVIEW) if VARIANT_PREVIEW.exists() else pd.DataFrame()
    all_close_false = bool(preview["close_on_flat"].astype(str).str.lower().eq("false").all()) if not preview.empty else False
    return pd.DataFrame(
        [
            gate_row("parent_340E_gates_passed", "passed" if parent_gate_passed else "failed", src.base.rel(PARENT_GATE_AUDIT), "run340E(340E 실행) review gate(검토 게이트)를 이어받는다."),
            gate_row("feature_matrix_reused", "passed" if FEATURE_MATRIX.exists() and summary["package_rows"] > 0 else "failed", src.base.rel(FEATURE_MATRIX_MANIFEST), "feature matrix(피처 행렬)를 f01(에프01) 수정 압박 패키지로 복사한다."),
            gate_row("close_on_flat_false_variants_materialized", "passed" if summary["attempt_count"] >= 10 and all_close_false else "failed", src.base.rel(VARIANT_PREVIEW), "모든 pressure variant(압박 변형)를 close_on_flat=False(평탄 청산 꺼짐)로 만든다."),
            gate_row("expected_tape_written", "passed" if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"] else "failed", src.base.rel(EXPECTED_TAPE_INDEX), "expected tape(예상 테이프)를 변형별로 만든다."),
            gate_row("common_files_synced", "passed" if summary["common_sync_missing"] == 0 else "failed", src.base.rel(COMMON_FILES_SYNC), "Common Files(공용 파일) 인계를 확인한다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["set_rows"] == summary["attempt_count"] and summary["ini_rows"] == summary["attempt_count"] else "failed", src.base.rel(TESTER_INI_MANIFEST), "tester set/ini(테스터 설정 파일)를 만든다."),
            gate_row("runtime_parity_contract_written", "passed" if RUNTIME_PARITY_CONTRACT.exists() else "failed", src.base.rel(RUNTIME_PARITY_CONTRACT), "runtime parity(런타임 동등성) 계약을 남긴다."),
            gate_row("tester_identity_visible", "passed" if summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"] else "failed", src.base.rel(TESTER_IDENTITY_CONTRACT), "MT5(메타트레이더5) 실행 가시성을 확인한다."),
            gate_row("run340G_queue_opened", "passed" if RUN340G_EXECUTION_QUEUE.exists() else "failed", src.base.rel(RUN340G_EXECUTION_QUEUE), "다음 MT5 runtime probe(MT5 런타임 탐침) 대기열을 연다."),
            gate_row("no_forbidden_selection_or_goal_claim", "passed" if no_forbidden else "failed", src.base.rel(FINAL_DECISION), "패키지를 selection(선정)이나 Goal Achieve(목표 달성)로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", src.base.rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 기록한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    receipt_base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": src.base.now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    src.base.write_json(
        DATA_RECEIPT,
        {
            **receipt_base,
            "feature_matrix": src.base.rel(FEATURE_MATRIX),
            "rows": summary["package_rows"],
            "source_attempt_name": SOURCE_ATTEMPT_NAME,
            "effect": "data(데이터)는 바꾸지 않고 f01(에프01)의 close_on_flat=False(평탄 청산 꺼짐) 실행 의미만 복구한다.",
        },
    )
    src.base.write_json(
        MODEL_RECEIPT,
        {
            **receipt_base,
            "model_training": "not_run(실행 안 함)",
            "source_model": src.base.rel(SOURCE_MODEL_PATH),
            "model_handoff": src.base.rel(MODEL_HANDOFF_MANIFEST),
            "effect": "같은 ONNX(온엑스)를 재사용해 threshold/min_margin/hold(임계값/최소 마진/보유) 효과만 분리한다.",
        },
    )
    src.base.write_json(
        RUNTIME_RECEIPT,
        {
            **receipt_base,
            "research_path": src.base.rel(EXPECTED_TAPE),
            "runtime_path": src.base.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": src.base.rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "close_on_flat restored to source False(평탄 청산을 원본 False로 복구)",
            "parity_check": "deferred_to_run340G(340G 실행으로 이연)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    src.base.write_json(
        CLAIM_RECEIPT,
        {
            **receipt_base,
            "candidate_selection": "not_run(실행 안 함)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    )
    inputs = [
        PARENT_FINAL_DECISION,
        PARENT_QUEUE,
        PARENT_SCORECARD,
        SOURCE_FEATURE_MATRIX,
        SOURCE_EXPECTED_TAPE,
        SOURCE_MODEL_MANIFEST,
        SOURCE_MODEL_PATH,
        SOURCE_ATTEMPT_PACKAGE,
    ]
    existing_outputs = [path for path in output_paths() if path.exists()]
    src.base.write_json(
        LINEAGE_RECEIPT,
        {
            **receipt_base,
            "source_inputs": [src.base.rel(path) for path in inputs],
            "producer": src.base.rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [src.base.rel(path) for path in existing_outputs],
            "artifact_hashes": {src.base.rel(path): src.base.sha256_file(path) for path in existing_outputs if path.is_file()},
            "registry_links": [src.base.rel(RUN_REGISTRY), src.base.rel(PROJECT_LEDGER), src.base.rel(STAGE_LEDGER), src.base.rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    src.base.write_json(
        RUN_MANIFEST,
        {**receipt_base, "command": f"python {src.base.rel(Path(__file__))}", "outputs": [src.base.rel(path) for path in existing_outputs]},
    )


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run340F F01 Close-On-Flat False Pressure Probe Package(340F F01 평탄 청산 꺼짐 압박 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- feature_rows(피처 행): `{summary['package_rows']}`
- expected_rows(예상 행): `{summary['expected_rows']}`
- source_attempt(원천 시도): `{SOURCE_ATTEMPT_NAME}`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `{summary['preview_max_signal_trade_count']}`
- preview_best_signal_side_balance(미리보기 최고 신호 방향 균형): `{summary['preview_best_signal_side_balance']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run340E(340E 실행)의 corrected queue(수정 대기열)를 사용해 f01(에프01) pressure variants(압박 변형) 10개를 close_on_flat=False(평탄 청산 꺼짐)로 MT5(메타트레이더5) package(패키지)화했다.

## Effect(효과)

run340G(340G 실행)가 source f01(원본 f01)의 lifecycle semantics(생명주기 의미)를 보존한 exact control(정확 대조)과 압박 변형을 바로 Strategy Tester(전략 테스터)에서 확인할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage340F Probe Package Decision(340F 탐침 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{src.base.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- queue(대기열): `{src.base.rel(RUN340G_EXECUTION_QUEUE)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): f01(에프01) close_on_flat=False(평탄 청산 꺼짐) 압박 MT5(메타트레이더5) 패키지를 만들었다.

Effect(효과): run340G(340G 실행)가 외부 검증(external verification, 외부 검증)을 바로 수행할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage340 Selection Status(340단계 선정 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- source_attempt(원천 시도): `{SOURCE_ATTEMPT_NAME}`
- close_on_flat(평탄 청산): `False(꺼짐)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 실행 전 패키지를 운영 모델로 오해하지 않게 한다.
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run340F(340F 실행)는 f01(에프01) close_on_flat=False(평탄 청산 꺼짐) 압박 MT5 package(MT5 패키지)를 만들었다. run340G(340G 실행)는 이 package(패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침)로 실행해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    src.base.write_bom_text(REPORT_PATH, report)
    src.base.write_bom_text(DECISION_DOC, decision)
    src.base.write_bom_text(SELECTION_STATUS, selection)
    src.base.write_bom_text(CURRENT_WORKING_STATE, current)
    src.base.write_bom_text(WORKSPACE_STATE, workspace)
    marker = RUN_ID
    src.base.append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run340F F01 Close-On-Flat False Pressure Package(340F F01 평탄 청산 꺼짐 압박 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): f01(에프01)의 원본 lifecycle semantics(생명주기 의미)를 복구한 MT5(메타트레이더5) 압박 탐침 준비를 만든다.
""",
    )
    src.base.append_text_once(
        STAGE_README,
        marker,
        f"""## run340F F01 Close-On-Flat False Pressure Package(340F F01 평탄 청산 꺼짐 압박 패키지)

- run_id(실행 ID): `{RUN_ID}`
- queue(대기열): `{src.base.rel(RUN340G_EXECUTION_QUEUE)}`
- effect(효과): Stage340(340단계) 탐색을 corrected MT5 run(수정 MT5 실행)으로 이어간다.
""",
    )
    changelog = f"""## {TODAY} run340F F01 Close-On-Flat False Pressure Package(F01 평탄 청산 꺼짐 압박 패키지)

- action(행동): f01(에프01) close_on_flat=False(평탄 청산 꺼짐) 압박 변형 `{summary['attempt_count']}`개를 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run340G(340G 실행)가 exact control(정확 대조) 복구 여부와 MT5 KPI(MT5 핵심 성과 지표)를 검증할 수 있다.
- boundary(경계): package only(패키지 전용), selected model(선정 모델)과 Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    src.base.append_text_once(ROOT_CHANGELOG, marker, changelog)
    src.base.append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def configure() -> None:
    replacements = {
        "TODAY": TODAY,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS": STATUS,
        "JUDGMENT": JUDGMENT,
        "DECISION": DECISION,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "SET_DIR": SET_DIR,
        "INI_DIR": INI_DIR,
        "MODEL_DIR": MODEL_DIR,
        "FEATURE_DIR": FEATURE_DIR,
        "EXPECTED_DIR": EXPECTED_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "PARENT_RUN_DIR": PARENT_RUN_DIR,
        "PARENT_FINAL_DECISION": PARENT_FINAL_DECISION,
        "PARENT_GATE_AUDIT": PARENT_GATE_AUDIT,
        "PARENT_QUEUE": PARENT_QUEUE,
        "PARENT_SCORECARD": PARENT_SCORECARD,
        "COMMON_ROOT": COMMON_ROOT,
        "COMMON_FEATURE_DIR": COMMON_FEATURE_DIR,
        "COMMON_MODEL_DIR": COMMON_MODEL_DIR,
        "COMMON_TELEMETRY_DIR": COMMON_TELEMETRY_DIR,
        "EXPLORATION_LABEL": EXPLORATION_LABEL,
        "MAGIC_BASE": MAGIC_BASE,
        "FEATURE_MATRIX": FEATURE_MATRIX,
        "FEATURE_MATRIX_MANIFEST": FEATURE_MATRIX_MANIFEST,
        "EXPECTED_TAPE": EXPECTED_TAPE,
        "EXPECTED_PROBABILITY_TAPE": EXPECTED_PROBABILITY_TAPE,
        "EXPECTED_TAPE_INDEX": EXPECTED_TAPE_INDEX,
        "VARIANT_PREVIEW": VARIANT_PREVIEW,
        "MODEL_HANDOFF_MANIFEST": MODEL_HANDOFF_MANIFEST,
        "COMMON_FILES_SYNC": COMMON_FILES_SYNC,
        "TESTER_SET_MANIFEST": TESTER_SET_MANIFEST,
        "TESTER_INI_MANIFEST": TESTER_INI_MANIFEST,
        "RUNTIME_PROBE_ATTEMPT_PACKAGE": RUNTIME_PROBE_ATTEMPT_PACKAGE,
        "TESTER_IDENTITY_CONTRACT": TESTER_IDENTITY_CONTRACT,
        "PROXY_MT5_COMPARISON_CONTRACT": PROXY_MT5_COMPARISON_CONTRACT,
        "RUNTIME_PARITY_CONTRACT": RUNTIME_PARITY_CONTRACT,
        "RUN340D_EXECUTION_QUEUE": RUN340G_EXECUTION_QUEUE,
        "DATA_RECEIPT": DATA_RECEIPT,
        "MODEL_RECEIPT": MODEL_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "output_paths": output_paths,
        "build_gates": build_gates,
        "write_receipts": write_receipts,
        "write_docs": write_docs,
    }
    for key, value in replacements.items():
        setattr(src, key, value)


def main() -> None:
    configure()
    src.main()


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage342 import materialize_f01_session_long_firewall_mt5_probe_package_without_db as base  # noqa: E402


TODAY = "2026-06-01"
DEFAULT_COMMON_FILES = base.DEFAULT_COMMON_FILES
DEFAULT_TERMINAL = base.DEFAULT_TERMINAL
DEFAULT_TESTER_PROFILE_ROOT = base.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = base.DEFAULT_PORTABLE_ROOT
EA_BINARY = base.EA_BINARY
PORTABLE_EA_EX5 = base.PORTABLE_EA_EX5
aw = base.aw
RUN_NUMBER = "run342E"
RUN_ID = "run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = "run342D_review_f01_session_long_firewall_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1"
STATUS = "completed_stage342E_soft_session_long_firewall_mt5_probe_package_materialized_no_selection"
JUDGMENT = "soft_session_long_firewall_mt5_probe_package_ready_runtime_execution_required_no_selection"
DECISION = "stage342E_open_run342F_execute_soft_session_long_firewall_probe"
CLAIM_BOUNDARY = (
    "research_development_soft_session_long_firewall_runtime_probe_package_only_no_mt5_execution_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_ID = base.STAGE_ID
STAGE_DIR = base.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run342E_soft_session_long_firewall_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage342E_soft_session_long_firewall_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run342D"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_QUEUE = PARENT_RUN_DIR / "run342E_soft_session_long_firewall_probe_queue.csv"
PARENT_HANDOFF = PARENT_RUN_DIR / "artifact_lineage_receipt.json"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage342/{RUN_NUMBER}_soft_session_long_firewall_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage342_F01SoftSessionLongFirewall__ONNX"
MAGIC_BASE = 3429000

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_TAPE
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
SIDE_FILTER_EXPECTED_AUDIT = RUN_DIR / "side_filter_expected_decision_audit.csv"
VARIANT_PREVIEW = RUN_DIR / "variant_preview.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN342F_EXECUTION_QUEUE = RUN_DIR / "run342F_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

ATTEMPT_NAME_MAP = {
    "e01_q01_control_no_filter": "e01_q01_ctl",
    "e02_q09_control_no_filter": "e02_q09_ctl",
    "e03_q01_block_early_long_0_45": "e03_q01_blk_early45",
    "e04_q09_block_early_long_0_45": "e04_q09_blk_early45",
    "e05_q01_block_early_long_0_75": "e05_q01_blk_early75",
    "e06_q09_block_early_long_0_75": "e06_q09_blk_early75",
    "e07_q09_block_early_all_0_45_negative_control": "e07_q09_blk_early_all45",
}


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def output_paths() -> list[Path]:
    return [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        SIDE_FILTER_EXPECTED_AUDIT,
        VARIANT_PREVIEW,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        TESTER_IDENTITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUNTIME_PARITY_CONTRACT,
        RUN342F_EXECUTION_QUEUE,
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
        SELECTION_STATUS,
        ROOT_SELECTION_STATUS,
        STAGE_LEDGER,
        Path(__file__),
    ]


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def build_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gate_passed = False
    if base.path_is_file(PARENT_GATE_AUDIT):
        parent_gates = base.read_csv(PARENT_GATE_AUDIT)
        parent_gate_passed = bool(parent_gates["status"].astype(str).str.lower().eq("passed").all())
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["mt5_execution"] == "not_run"
    )
    return pd.DataFrame(
        [
            gate_row("parent_342D_gates_passed", "passed" if parent_gate_passed else "failed", base.rel(PARENT_GATE_AUDIT), "run342D(342D 실행) review gate(검토 게이트)를 이어받는다."),
            gate_row(
                "feature_matrix_reused_timestamp_safe",
                "passed" if base.path_is_file(FEATURE_MATRIX) and summary["package_rows"] > 0 and summary["feature_count"] == 53 else "failed",
                base.rel(FEATURE_MATRIX_MANIFEST),
                "feature matrix(피처 행렬)를 새로 만들지 않고 timestamp-safe(시점 안전)하게 재사용한다.",
            ),
            gate_row(
                "expected_tape_soft_side_filter_materialized",
                "passed" if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"] and summary["side_filter_blocked_rows"] > 0 else "failed",
                base.rel(SIDE_FILTER_EXPECTED_AUDIT),
                "soft side filter(부드러운 사이드 필터) 후 decision(결정)을 expected tape(예상 테이프)에 반영한다.",
            ),
            gate_row("common_files_synced", "passed" if summary["common_sync_missing"] == 0 else "failed", base.rel(COMMON_FILES_SYNC), "MT5 Common Files(MT5 공용 파일) 인계를 확인한다."),
            gate_row(
                "tester_set_ini_materialized",
                "passed"
                if summary["set_rows"] == summary["attempt_count"]
                and summary["ini_rows"] == summary["attempt_count"]
                and summary["side_filter_set_rows"] == summary["side_filter_attempt_count"]
                else "failed",
                base.rel(TESTER_SET_MANIFEST),
                "tester set/ini(테스터 설정 파일)와 soft filter(부드러운 필터) 파라미터를 만든다.",
            ),
            gate_row("runtime_parity_contract_written", "passed" if base.path_is_file(RUNTIME_PARITY_CONTRACT) and base.path_is_file(PROXY_MT5_COMPARISON_CONTRACT) else "failed", base.rel(RUNTIME_PARITY_CONTRACT), "runtime parity(런타임 동등성) 비교 계약을 남긴다."),
            gate_row(
                "tester_identity_visible",
                "passed"
                if summary["terminal_exists"]
                and summary["common_files_exists"]
                and summary["ea_binary_exists"]
                and summary["portable_ea_exists"]
                else "failed",
                base.rel(TESTER_IDENTITY_CONTRACT),
                "MT5(메타트레이더5) 실행 가시성을 확인한다.",
            ),
            gate_row("run342F_queue_opened", "passed" if base.path_is_file(RUN342F_EXECUTION_QUEUE) else "failed", base.rel(RUN342F_EXECUTION_QUEUE), "다음 MT5 runtime probe(MT5 런타임 탐침) queue(대기열)를 연다."),
            gate_row("no_forbidden_selection_or_goal_claim", "passed" if no_forbidden else "failed", base.rel(CLAIM_RECEIPT), "package(패키지)를 selection(선정)이나 Goal Achieve(목표 달성)로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", base.rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다."),
        ]
    )


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run342E Soft Session-Long Firewall Probe Package(342E 부드러운 세션 롱 방화벽 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- side_filter_attempts(사이드 필터 시도): `{summary['side_filter_attempt_count']}`
- feature_rows(피처 행): `{summary['package_rows']}`
- feature_count(피처 수): `{summary['feature_count']}`
- expected_rows(예상 행): `{summary['expected_rows']}`
- side_filter_blocked_rows(사이드 필터 차단 행): `{summary['side_filter_blocked_rows']}`
- blocked_long_rows(차단 롱 행): `{summary['side_filter_blocked_long_rows']}`
- blocked_short_rows(차단 숏 행): `{summary['side_filter_blocked_short_rows']}`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `{summary['preview_max_signal_trade_count']}`
- preview_min_signal_trade_count(미리보기 최소 신호 거래수): `{summary['preview_min_signal_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run342D(342D 실행)의 soft-window queue(부드러운 구간 대기열)를 MT5 package(MT5 패키지)로 만들었다.
Effect(효과): hard 0~110 early-long block(강한 0~110 초반 롱 차단)의 거래수 비용을 0~45, 0~75분 변형으로 줄일 수 있는지 MT5(메타트레이더5)에서 바로 시험할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage342E Soft Probe Package Decision(342E 부드러운 탐침 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{base.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- queue(대기열): `{base.rel(RUN342F_EXECUTION_QUEUE)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): softer session-long firewall(부드러운 세션 롱 방화벽) MT5 probe package(MT5 탐침 패키지)를 만들었다.
Effect(효과): run342F(342F 실행)가 trade count(거래수), PF(수익 팩터), long/short balance(롱/숏 균형)의 절충점을 확인할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- soft_firewall_attempts(부드러운 방화벽 시도): `{summary['side_filter_attempt_count']}`
- preserved_positive_clue(보존 긍정 단서): `e04_q09_blk_early_long`
- next_probe(다음 탐침): `soft_session_long_firewall(부드러운 세션 롱 방화벽)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): package(패키지) 완료를 selection(선정)으로 오해하지 않게 한다.
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

run342E(342E 실행)는 softer session-long firewall(부드러운 세션 롱 방화벽) MT5 package(MT5 패키지)를 만들었다. run342F(342F 실행)는 이 package(패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침)로 실행해야 한다.

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
    base.write_bom_text(REPORT_PATH, report)
    base.write_bom_text(DECISION_DOC, decision)
    base.write_bom_text(SELECTION_STATUS, selection)
    base.write_bom_text(ROOT_SELECTION_STATUS, selection)
    base.write_bom_text(CURRENT_WORKING_STATE, current)
    base.write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run342E {RUN_ID}"
    base.append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run342E Soft Session-Long Firewall Package(342E 부드러운 세션 롱 방화벽 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- side_filter_blocked_rows(사이드 필터 차단 행): `{summary['side_filter_blocked_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): hard firewall(강한 방화벽)의 수익 단서를 soft-window(부드러운 구간) MT5 실행으로 넘긴다.
""",
    )
    base.append_text_once(
        STAGE_README,
        marker,
        f"""## run342E Soft Session-Long Firewall Package(342E 부드러운 세션 롱 방화벽 패키지)

- run_id(실행 ID): `{RUN_ID}`
- queue(대기열): `{base.rel(RUN342F_EXECUTION_QUEUE)}`
- effect(효과): Stage342(342단계)가 soft-window(부드러운 구간) MT5 실행 단계로 넘어갈 수 있다.
""",
    )
    changelog = f"""## {TODAY} run342E Soft Session-Long Firewall Package(부드러운 세션 롱 방화벽 패키지)

- action(행동): q01/q09(큐01/큐09) control(대조), 0~45/0~75 long block(롱 차단), soft overfilter negative control(부드러운 과필터 부정 대조)을 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run342F(342F 실행)가 hard firewall(강한 방화벽)의 거래수/균형 비용을 줄일 수 있는지 확인한다.
- boundary(경계): package only(패키지 전용), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).
"""
    base.append_text_once(ROOT_CHANGELOG, marker, changelog)
    base.append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    final = {
        **dict(summary),
        "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
        "gate_total": int(len(gates)),
        "created_at_utc": now_utc(),
    }
    base.write_json(FINAL_DECISION, final)
    base.write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": f"python -B {base.rel(Path(__file__))}",
            "inputs": [
                base.rel(PARENT_FINAL_DECISION),
                base.rel(PARENT_QUEUE),
                base.rel(base.SOURCE_FEATURE_MATRIX),
                base.rel(base.SOURCE_EXPECTED_TAPE),
                base.rel(base.SOURCE_ATTEMPT_PACKAGE),
                base.rel(base.SOURCE_MODEL_MANIFEST),
            ],
            "outputs": [base.rel(path) for path in output_paths() if base.path_exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    receipt_base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    base.write_json(
        DATA_RECEIPT,
        {
            **receipt_base,
            "data_source": base.rel(FEATURE_MATRIX),
            "time_axis": "M5 bar close timestamp(5분봉 종가 시각)",
            "sample_scope": "FPMarkets US100 M5 inner-holdout runtime collapsed probe(내부 보류 런타임 축약 탐침)",
            "missing_or_duplicate_check": base.rel(FEATURE_MATRIX_MANIFEST),
            "feature_label_boundary": "no labels joined; side filter uses current feature row only(라벨 결합 없음, 사이드 필터는 현재 피처 행만 사용)",
            "split_boundary": "inner_holdout_runtime_collapsed_probe(내부 보류 런타임 축약 탐침)",
            "leakage_risk": "feature_index/window misuse(피처 인덱스/구간 오사용); guarded by expected audit(예상 감사 파일로 방어)",
            "data_hash_or_identity": base.sha256_file(FEATURE_MATRIX),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    base.write_json(
        MODEL_RECEIPT,
        {
            **receipt_base,
            "model_training": "not_run(실행 없음)",
            "source_model_manifest": base.rel(base.SOURCE_MODEL_MANIFEST),
            "model_handoff": base.rel(MODEL_HANDOFF_MANIFEST),
            "effect": "기존 ONNX(온엑스)를 재사용하고 soft side filter(부드러운 사이드 필터) 파라미터 효과만 분리한다.",
        },
    )
    base.write_json(
        RUNTIME_RECEIPT,
        {
            **receipt_base,
            "research_path": base.rel(EXPECTED_TAPE),
            "runtime_path": base.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": base.rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "probabilities(확률)는 원본 ONNX(온엑스)와 같고 decision(결정)은 soft side filter(부드러운 사이드 필터) 후 flat(관망)으로 바뀔 수 있다.",
            "parity_check": "deferred_to_run342F telemetry-vs-expected tape(342F 기록 대 예상 테이프)",
            "parity_identity": base.rel(TESTER_IDENTITY_CONTRACT),
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    base.write_json(
        CLAIM_RECEIPT,
        {
            **receipt_base,
            "candidate_selection": "not_run(실행 없음)",
            "mt5_execution": "not_run(실행 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    )
    existing_outputs = [path for path in output_paths() if base.path_exists(path) and path != LINEAGE_RECEIPT]
    base.write_json(
        LINEAGE_RECEIPT,
        {
            **receipt_base,
            "source_inputs": [
                base.rel(PARENT_FINAL_DECISION),
                base.rel(PARENT_QUEUE),
                base.rel(PARENT_HANDOFF),
                base.rel(base.SOURCE_FEATURE_MATRIX),
                base.rel(base.SOURCE_EXPECTED_TAPE),
                base.rel(base.SOURCE_ATTEMPT_PACKAGE),
                base.rel(base.SOURCE_MODEL_MANIFEST),
                base.rel(base.SOURCE_PARENT_FINAL),
            ],
            "producer": base.rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [base.rel(path) for path in existing_outputs],
            "artifact_hashes": {base.rel(path): base.sha256_file(path) for path in existing_outputs if base.path_is_file(path)},
            "registry_links": [base.rel(RUN_REGISTRY), base.rel(PROJECT_LEDGER), base.rel(STAGE_LEDGER), base.rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )


def write_artifact_registry() -> None:
    rows = []
    for path in output_paths():
        if not base.path_is_file(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": base.rel(path),
                "artifact_path": base.rel(path),
                "sha256": base.sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "notes": "run342E soft session-long firewall package artifact(342E 부드러운 세션 롱 방화벽 패키지 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    base.append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], rows)


def configure_base() -> None:
    replacements = {
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
        "SELECTION_STATUS": SELECTION_STATUS,
        "STAGE_LEDGER": STAGE_LEDGER,
        "PARENT_RUN_DIR": PARENT_RUN_DIR,
        "PARENT_FINAL_DECISION": PARENT_FINAL_DECISION,
        "PARENT_GATE_AUDIT": PARENT_GATE_AUDIT,
        "PARENT_QUEUE": PARENT_QUEUE,
        "PARENT_HANDOFF": PARENT_HANDOFF,
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
        "SIDE_FILTER_EXPECTED_AUDIT": SIDE_FILTER_EXPECTED_AUDIT,
        "VARIANT_PREVIEW": VARIANT_PREVIEW,
        "MODEL_HANDOFF_MANIFEST": MODEL_HANDOFF_MANIFEST,
        "COMMON_FILES_SYNC": COMMON_FILES_SYNC,
        "TESTER_SET_MANIFEST": TESTER_SET_MANIFEST,
        "TESTER_INI_MANIFEST": TESTER_INI_MANIFEST,
        "RUNTIME_PROBE_ATTEMPT_PACKAGE": RUNTIME_PROBE_ATTEMPT_PACKAGE,
        "TESTER_IDENTITY_CONTRACT": TESTER_IDENTITY_CONTRACT,
        "PROXY_MT5_COMPARISON_CONTRACT": PROXY_MT5_COMPARISON_CONTRACT,
        "RUNTIME_PARITY_CONTRACT": RUNTIME_PARITY_CONTRACT,
        "RUN342C_EXECUTION_QUEUE": RUN342F_EXECUTION_QUEUE,
        "DATA_RECEIPT": DATA_RECEIPT,
        "MODEL_RECEIPT": MODEL_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_WORKING_STATE": CURRENT_WORKING_STATE,
        "ROOT_CHANGELOG": ROOT_CHANGELOG,
        "WORKSPACE_CHANGELOG": WORKSPACE_CHANGELOG,
        "RUN_REGISTRY": RUN_REGISTRY,
        "PROJECT_LEDGER": PROJECT_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "ROOT_SELECTION_STATUS": ROOT_SELECTION_STATUS,
        "ATTEMPT_NAME_MAP": ATTEMPT_NAME_MAP,
        "output_paths": output_paths,
        "build_gates": build_gates,
        "write_docs": write_docs,
        "write_final": write_final,
        "write_receipts": write_receipts,
        "write_artifact_registry": write_artifact_registry,
    }
    for key, value in replacements.items():
        setattr(base, key, value)


def main() -> None:
    configure_base()
    base.main()


if __name__ == "__main__":
    main()

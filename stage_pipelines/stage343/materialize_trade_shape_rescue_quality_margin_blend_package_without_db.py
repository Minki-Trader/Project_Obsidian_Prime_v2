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

from stage_pipelines.stage342 import (  # noqa: E402
    materialize_f01_session_long_firewall_mt5_probe_package_without_db as base,
)


TODAY = "2026-06-01"
DEFAULT_COMMON_FILES = base.DEFAULT_COMMON_FILES
DEFAULT_TERMINAL = base.DEFAULT_TERMINAL
DEFAULT_TESTER_PROFILE_ROOT = base.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = base.DEFAULT_PORTABLE_ROOT
EA_BINARY = base.EA_BINARY
PORTABLE_EA_EX5 = base.PORTABLE_EA_EX5
aw = base.aw

STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"
SOURCE_STAGE_ID = "342_session_long_firewall__early_long_filter_mt5_probe"
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID

RUN_NUMBER = "run343D"
RUN_ID = "run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1"
PARENT_RUN_ID = "run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1"
STATUS = "completed_stage343D_trade_shape_rescue_quality_margin_blend_package_materialized_no_selection"
JUDGMENT = "trade_shape_rescue_quality_margin_blend_package_ready_runtime_execution_required_no_selection"
DECISION = "stage343D_open_run343E_execute_trade_shape_rescue_quality_margin_blend_probe"
CLAIM_BOUNDARY = (
    "research_development_trade_shape_rescue_quality_margin_blend_runtime_probe_package_only_"
    "no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run343D_trade_shape_rescue_quality_margin_blend_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage343D_trade_shape_rescue_quality_margin_blend_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run343C"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SEED_QUEUE = PARENT_RUN_DIR / "run343D_trade_shape_rescue_quality_margin_blend_queue.csv"
PARENT_QUEUE = RUN_DIR / "run343D_materialization_queue.csv"
PARENT_HANDOFF = PARENT_RUN_DIR / "artifact_lineage_receipt.json"

SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run342H"
SOURCE_FEATURE_MATRIX = SOURCE_PACKAGE_DIR / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = SOURCE_PACKAGE_DIR / "expected" / "expected_tape.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_PACKAGE_DIR / "runtime_probe_attempt_package.csv"
SOURCE_MODEL_MANIFEST = SOURCE_PACKAGE_DIR / "model_handoff_manifest.csv"
SOURCE_PARENT_FINAL = SOURCE_PACKAGE_DIR / "final_decision.json"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage343/{RUN_NUMBER}_trade_shape_rescue_quality_margin_blend_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage343_TradeShapeRescue__QualityMarginBlendONNX"
MAGIC_BASE = 3431000

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
RUN343E_EXECUTION_QUEUE = RUN_DIR / "run343E_queue.csv"
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
    "d01_h04_profit_anchor_blk45": "d01_h04_anchor45",
    "d02_h02_shape_control_no_filter": "d02_h02_shape_ctl",
    "d03_h03_shape_control_no_filter": "d03_h03_shape_ctl",
    "d04_q02_partial_block_0_15": "d04_q02_blk15",
    "d05_q02_partial_block_0_30": "d05_q02_blk30",
    "d06_q04_margin015_block_0_15": "d06_q04_m015_blk15",
    "d07_q04_margin015_block_0_30": "d07_q04_m015_blk30",
    "d08_q10_s555_no_filter": "d08_q10_s555_ctl",
    "d09_q10_s555_block_0_15": "d09_q10_s555_blk15",
    "d10_q02_block_0_60": "d10_q02_blk60",
}


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def output_paths() -> list[Path]:
    return [
        PARENT_QUEUE,
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
        RUN343E_EXECUTION_QUEUE,
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


def detailed_queue_rows() -> list[dict[str, Any]]:
    boundary = CLAIM_BOUNDARY
    return [
        {
            "queue_id": "d01_h04_profit_anchor_blk45",
            "next_run_id": RUN_ID,
            "priority": "P0",
            "source_attempt": "h04_q02_l515_blk45",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,45",
            "block_short_range": "",
            "role": "profit_anchor_control(수익 앵커 대조)",
            "expected_effect": "h04(342H 수익 최고)의 숏 중심 수익 품질을 그대로 재확인한다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d02_h02_shape_control_no_filter",
            "next_run_id": RUN_ID,
            "priority": "P0",
            "source_attempt": "h02_q04_m015_ctl",
            "side_filter_enabled": False,
            "feature_index": -1,
            "feature_name": "",
            "block_long_range": "",
            "block_short_range": "",
            "role": "trade_shape_control(거래 형태 대조)",
            "expected_effect": "h02(342H 거래 형태 우수)의 롱 공급과 방향 균형을 대조군으로 유지한다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d03_h03_shape_control_no_filter",
            "next_run_id": RUN_ID,
            "priority": "P1",
            "source_attempt": "h03_q05_m02_ctl",
            "side_filter_enabled": False,
            "feature_index": -1,
            "feature_name": "",
            "block_long_range": "",
            "block_short_range": "",
            "role": "strict_margin_shape_control(엄격 마진 거래 형태 대조)",
            "expected_effect": "h03(엄격 마진 대조)로 마진 강화가 거래수와 수익 품질에 주는 손상을 확인한다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d04_q02_partial_block_0_15",
            "next_run_id": RUN_ID,
            "priority": "P0",
            "source_attempt": "h01_q02_l515_ctl",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,15",
            "block_short_range": "",
            "role": "partial_long_rescue(부분 롱 복구)",
            "expected_effect": "h04의 0~45분 롱 차단을 0~15분으로 완화해 수익 앵커와 롱 복구의 중간점을 본다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d05_q02_partial_block_0_30",
            "next_run_id": RUN_ID,
            "priority": "P0",
            "source_attempt": "h01_q02_l515_ctl",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,30",
            "block_short_range": "",
            "role": "medium_long_rescue(중간 롱 복구)",
            "expected_effect": "0~30분 롱 차단으로 h04보다 완만한 방화벽이 trade count(거래수)를 되살리는지 본다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d06_q04_margin015_block_0_15",
            "next_run_id": RUN_ID,
            "priority": "P1",
            "source_attempt": "h02_q04_m015_ctl",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,15",
            "block_short_range": "",
            "role": "margin_shape_rescue_soft_block(마진 거래 형태 완화 차단)",
            "expected_effect": "h02의 거래 형태 장점을 보존하면서 초반 15분 약한 롱만 줄인다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d07_q04_margin015_block_0_30",
            "next_run_id": RUN_ID,
            "priority": "P1",
            "source_attempt": "h02_q04_m015_ctl",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,30",
            "block_short_range": "",
            "role": "margin_shape_rescue_medium_block(마진 거래 형태 중간 차단)",
            "expected_effect": "h02 표면에서 0~30분 차단이 trade shape(거래 형태)와 PF(수익 팩터)를 같이 살리는지 본다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d08_q10_s555_no_filter",
            "next_run_id": RUN_ID,
            "priority": "P2",
            "source_attempt": "h08_q10_s555_blk45",
            "side_filter_enabled": False,
            "feature_index": -1,
            "feature_name": "",
            "block_long_range": "",
            "block_short_range": "",
            "role": "short_threshold_cost_stress_control(숏 임계값 비용 압박 대조)",
            "expected_effect": "h08의 높은 숏 임계값을 유지하되 롱 방화벽을 제거해 숏 집중 완화와 롱 복구를 분리한다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d09_q10_s555_block_0_15",
            "next_run_id": RUN_ID,
            "priority": "P2",
            "source_attempt": "h08_q10_s555_blk45",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,15",
            "block_short_range": "",
            "role": "short_threshold_partial_long_block(숏 임계값 부분 롱 차단)",
            "expected_effect": "높은 숏 임계값과 0~15분 롱 차단을 결합해 cost stress(비용 압박)에 강한 생존 진입을 본다.",
            "claim_boundary": boundary,
        },
        {
            "queue_id": "d10_q02_block_0_60",
            "next_run_id": RUN_ID,
            "priority": "P2",
            "source_attempt": "h01_q02_l515_ctl",
            "side_filter_enabled": True,
            "feature_index": 37,
            "feature_name": "minutes_from_cash_open",
            "block_long_range": "0,60",
            "block_short_range": "",
            "role": "overblock_negative_control(과차단 부정 대조)",
            "expected_effect": "0~60분 과차단으로 롱 복구가 사라질 때 수익 품질만 남는지 확인한다.",
            "claim_boundary": boundary,
        },
    ]


def materialize_parent_queue() -> None:
    seed = base.read_csv(base.required(SOURCE_SEED_QUEUE)).fillna("")
    if seed.empty:
        raise RuntimeError("run343D seed queue is empty")
    if not seed["next_run_id"].astype(str).eq(RUN_ID).all():
        raise RuntimeError("run343D seed queue next_run_id mismatch")
    source_package = base.read_csv(base.required(SOURCE_ATTEMPT_PACKAGE)).fillna("")
    available = set(source_package["attempt_name"].astype(str))
    rows = detailed_queue_rows()
    missing = sorted({str(row["source_attempt"]) for row in rows} - available)
    if missing:
        raise RuntimeError(f"missing source attempts: {missing}")
    base.write_csv(PARENT_QUEUE, pd.DataFrame(rows))


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def passed_csv(path: Path) -> bool:
    if not base.path_is_file(path):
        return False
    frame = base.read_csv(path)
    return bool(frame["status"].astype(str).str.lower().eq("passed").all())


def build_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["mt5_execution"] == "not_run"
    )
    return pd.DataFrame(
        [
            gate_row(
                "parent_343C_gates_passed",
                "passed" if passed_csv(PARENT_GATE_AUDIT) else "failed",
                base.rel(PARENT_GATE_AUDIT),
                "run343C(343C 실행)의 review gate(검토 게이트)를 이어받는다.",
            ),
            gate_row(
                "source_342H_package_available",
                "passed"
                if base.path_is_file(SOURCE_ATTEMPT_PACKAGE)
                and base.path_is_file(SOURCE_EXPECTED_TAPE)
                and base.path_is_file(SOURCE_FEATURE_MATRIX)
                else "failed",
                base.rel(SOURCE_ATTEMPT_PACKAGE),
                "run342H(342H 실행)의 ONNX(온엑스), feature(피처), expected tape(예상 테이프)를 재사용한다.",
            ),
            gate_row(
                "trade_shape_materialization_queue_written",
                "passed" if base.path_is_file(PARENT_QUEUE) and summary["attempt_count"] == 10 else "failed",
                base.rel(PARENT_QUEUE),
                "seed queue(씨앗 대기열)를 실제 MT5 package(MT5 패키지) 변형 10개로 바꾼다.",
            ),
            gate_row(
                "feature_matrix_reused_timestamp_safe",
                "passed" if base.path_is_file(FEATURE_MATRIX) and summary["package_rows"] > 0 and summary["feature_count"] == 53 else "failed",
                base.rel(FEATURE_MATRIX_MANIFEST),
                "feature matrix(피처 행렬)를 새로 만들지 않고 timestamp-safe(시점 안전) 재사용으로 제한한다.",
            ),
            gate_row(
                "expected_tape_trade_shape_rescue_materialized",
                "passed"
                if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"]
                and summary["side_filter_blocked_rows"] > 0
                else "failed",
                base.rel(SIDE_FILTER_EXPECTED_AUDIT),
                "partial long rescue(부분 롱 복구)와 negative control(부정 대조)을 expected tape(예상 테이프)에 반영한다.",
            ),
            gate_row(
                "tester_set_ini_materialized",
                "passed"
                if summary["set_rows"] == summary["attempt_count"]
                and summary["ini_rows"] == summary["attempt_count"]
                and summary["side_filter_set_rows"] == summary["side_filter_attempt_count"]
                else "failed",
                base.rel(TESTER_SET_MANIFEST),
                "MT5 Strategy Tester(MT5 전략 테스터)가 같은 조건으로 실행할 set/ini(설정 파일)를 만든다.",
            ),
            gate_row(
                "common_files_synced",
                "passed" if summary["common_sync_missing"] == 0 else "failed",
                base.rel(COMMON_FILES_SYNC),
                "MT5 Common Files(MT5 공용 파일) handoff(인계)를 확인한다.",
            ),
            gate_row(
                "runtime_parity_contract_written",
                "passed" if base.path_is_file(RUNTIME_PARITY_CONTRACT) and base.path_is_file(PROXY_MT5_COMPARISON_CONTRACT) else "failed",
                base.rel(RUNTIME_PARITY_CONTRACT),
                "proxy(프록시)와 MT5 runtime(런타임)의 비교 계약을 남긴다.",
            ),
            gate_row(
                "tester_identity_visible",
                "passed"
                if summary["terminal_exists"]
                and summary["common_files_exists"]
                and summary["ea_binary_exists"]
                and summary["portable_ea_exists"]
                else "failed",
                base.rel(TESTER_IDENTITY_CONTRACT),
                "terminal(터미널), EA(전문가 자문), Common Files(공용 파일) 경로를 실행 전에 보이게 한다.",
            ),
            gate_row(
                "run343E_queue_opened",
                "passed" if base.path_is_file(RUN343E_EXECUTION_QUEUE) else "failed",
                base.rel(RUN343E_EXECUTION_QUEUE),
                "다음 MT5 runtime probe(MT5 런타임 탐침) 대기열을 연다.",
            ),
            gate_row(
                "no_forbidden_selection_or_goal_claim",
                "passed" if no_forbidden else "failed",
                base.rel(CLAIM_RECEIPT),
                "package(패키지)를 selection(선정), promotion(승격), Goal Achieve(목표 달성)로 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                base.rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
            ),
        ]
    )


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run343D Trade Shape Rescue Quality Margin Blend Package(343D 거래 형태 복구 품질 마진 혼합 패키지)

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

run342H(342H 실행)의 best profit clue(최고 수익 단서)와 trade shape clue(거래 형태 단서)를 Stage343(343단계) 전용 package(패키지)로 만들었다.

## Effect(효과)

run343E(343E 실행)가 MT5(메타트레이더5)에서 profit anchor(수익 앵커), shape control(거래 형태 대조), partial long rescue(부분 롱 복구), cost stress(비용 압박)를 같은 runtime contract(런타임 계약)로 비교할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no forward(전진 검증 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage343D Package Decision(343D 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{base.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- materialization_queue(구체화 대기열): `{base.rel(PARENT_QUEUE)}`
- execution_queue(실행 대기열): `{base.rel(RUN343E_EXECUTION_QUEUE)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage342(342단계)에서 무거워진 early-long quality margin(초반 롱 품질 마진) 흐름을 Stage343D(343D 실행)의 trade shape rescue(거래 형태 복구) package(패키지)로 분기했다.
Effect(효과): 다음 작업은 run343E(343E 실행)만 좁게 실행하면 되며, Stage342(342단계) 전체를 다시 끌고 가지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 343 Selection Status(343단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- source_package(원천 패키지): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- best_profit_clue(최고 수익 단서): `h04_q02_l515_blk45`
- trade_shape_clue(거래 형태 단서): `h02_q04_m015_ctl`
- next_probe(다음 탐침): `trade_shape_rescue_quality_margin_blend(거래 형태 복구 품질 마진 혼합)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage343(343단계)은 MT5 runtime probe(MT5 런타임 탐침) 전의 package ready(패키지 준비) 상태다.
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

run343D(343D 실행)는 Stage342(342단계)에서 무거워진 흐름을 더 좁은 MT5 package(MT5 패키지)로 분기했다. run343E(343E 실행)는 이 package(패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침)로 실행해야 한다.

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

    base.append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## run343D Trade Shape Rescue Package(343D 거래 형태 복구 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- side_filter_blocked_rows(사이드 필터 차단 행): `{summary['side_filter_blocked_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): Stage343(343단계)이 trade shape rescue(거래 형태 복구) MT5 runtime probe(MT5 런타임 탐침) 준비 단계로 넘어간다.
""",
    )
    base.append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run343D Trade Shape Rescue Package(343D 거래 형태 복구 패키지)

- run_id(실행 ID): `{RUN_ID}`
- queue(대기열): `{base.rel(RUN343E_EXECUTION_QUEUE)}`
- effect(효과): Stage342(342단계)의 무거운 탐색을 Stage343(343단계)의 좁은 런타임 탐침 실행으로 분기한다.
""",
    )
    changelog = f"""## {TODAY} run343D Trade Shape Rescue Package(거래 형태 복구 패키지)

- action(행동): run342H(342H 실행)의 h04 profit anchor(수익 앵커), h02/h03 shape controls(거래 형태 대조), partial long rescue(부분 롱 복구), cost stress(비용 압박) 변형 `{summary['attempt_count']}`개를 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run343E(343E 실행)가 Stage342(342단계)를 다시 무겁게 열지 않고 trade shape(거래 형태) 복구 여부만 런타임에서 본다.
- boundary(경계): package only(패키지 전용), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).
"""
    base.append_text_once(ROOT_CHANGELOG, RUN_ID, changelog)
    base.append_text_once(WORKSPACE_CHANGELOG, RUN_ID, changelog)


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    final = {
        **dict(summary),
        "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
        "gate_total": int(len(gates)),
        "source_seed_queue": base.rel(SOURCE_SEED_QUEUE),
        "source_package_run_id": "run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1",
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
                base.rel(PARENT_GATE_AUDIT),
                base.rel(SOURCE_SEED_QUEUE),
                base.rel(PARENT_QUEUE),
                base.rel(SOURCE_FEATURE_MATRIX),
                base.rel(SOURCE_EXPECTED_TAPE),
                base.rel(SOURCE_ATTEMPT_PACKAGE),
                base.rel(SOURCE_MODEL_MANIFEST),
            ],
            "outputs": [base.rel(path) for path in output_paths() if base.path_exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def stage_rows(gates: pd.DataFrame, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": base.rel(FINAL_DECISION),
        "report_path": base.rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": "logreg_balanced_c025_stage343D_trade_shape_rescue_pack",
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "recovery_factor": "",
        "trade_count": "",
        "result_status": "mt5_probe_package_ready_runtime_execution_required(MT5 탐침 패키지 준비, 런타임 실행 필요)",
        "sample_rows": summary["package_rows"],
        "feature_count": summary["feature_count"],
        "matched_rows": "",
        "expectancy": "",
        "attempt_count": summary["attempt_count"],
    }
    return [
        {
            **base_row,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "runtime_probe_package_only_no_new_kpi",
        },
        {
            **base_row,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "candidate_model_id": "",
            "sample_rows": "",
            "feature_count": "",
            "attempt_count": "",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base_row,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
        },
    ]


def write_registries(gates: pd.DataFrame, summary: Mapping[str, Any]) -> None:
    rows = stage_rows(gates, summary)
    base.append_or_replace_csv(STAGE_LEDGER, ["run_id", "tier", "view"], rows)
    project_rows = []
    for row in rows:
        project_rows.append(
            {
                **row,
                "ledger_row_id": f"{RUN_ID}__{row['tier']}",
                "subrun_id": row["tier"],
                "record_view": row["view"],
                "tier_scope": row["tier"],
                "kpi_scope": row["metric_scope"],
                "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
                "path": base.rel(REPORT_PATH),
                "primary_kpi": f"attempt_count={summary['attempt_count']};side_filter_blocked_rows={summary['side_filter_blocked_rows']}",
                "guardrail_kpi": "MT5 KPI not run(MT5 핵심 성과 지표 미실행)",
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "notes": "Package only(패키지 전용); run343E must execute MT5 runtime probe(343E에서 MT5 런타임 탐침 실행 필요).",
            }
        )
    base.append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    base.append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe_package(런타임 탐침 패키지)",
                "family": "runtime_backtest",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": base.rel(FINAL_DECISION),
                "notes": "Trade shape rescue quality margin blend(거래 형태 복구 품질 마진 혼합) package only(패키지 전용).",
                "primary_report": base.rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": summary["package_rows"],
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": base.rel(REPORT_PATH),
                "primary_artifact": base.rel(FINAL_DECISION),
                "candidate_model_id": "logreg_balanced_c025_stage343D_trade_shape_rescue_pack",
                "result_status": "mt5_probe_package_ready_runtime_execution_required(MT5 탐침 패키지 준비, 런타임 실행 필요)",
                "sample_rows": summary["package_rows"],
                "feature_count": summary["feature_count"],
                "attempt_count": summary["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "runtime_probe_package_only_no_new_kpi",
            }
        ],
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
            "sample_scope": "FPMarkets US100 M5 inner-holdout runtime probe(내부 보류 런타임 탐침)",
            "missing_or_duplicate_check": base.rel(FEATURE_MATRIX_MANIFEST),
            "feature_label_boundary": "no labels joined; side filter uses current feature row only(라벨 결합 없음, 사이드 필터는 현재 피처 행만 사용)",
            "split_boundary": "inner_holdout_runtime_collapsed_probe(내부 보류 런타임 축약 탐침)",
            "leakage_risk": "feature_index/window misuse(피처 인덱스/구간 오사용); guarded by side_filter_expected_decision_audit(사이드 필터 예상 결정 감사)",
            "data_hash_or_identity": base.sha256_file(FEATURE_MATRIX),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    base.write_json(
        MODEL_RECEIPT,
        {
            **receipt_base,
            "model_training": "not_run(실행 없음)",
            "source_model_manifest": base.rel(SOURCE_MODEL_MANIFEST),
            "model_handoff": base.rel(MODEL_HANDOFF_MANIFEST),
            "effect": "기존 ONNX(온엑스)를 재사용하고 threshold/margin/side filter(임계값/마진/사이드 필터) 실행 의미만 분리한다.",
        },
    )
    base.write_json(
        RUNTIME_RECEIPT,
        {
            **receipt_base,
            "research_path": base.rel(EXPECTED_TAPE),
            "runtime_path": base.rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": base.rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "probabilities(확률)는 원천 ONNX(온엑스)와 같고 decision(결정)은 side filter(사이드 필터)에서 flat(관망)으로 바뀔 수 있다.",
            "parity_check": "deferred_to_run343E telemetry-vs-expected tape(343E 기록 대 예상 테이프)",
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
                base.rel(PARENT_GATE_AUDIT),
                base.rel(PARENT_HANDOFF),
                base.rel(SOURCE_SEED_QUEUE),
                base.rel(PARENT_QUEUE),
                base.rel(SOURCE_FEATURE_MATRIX),
                base.rel(SOURCE_EXPECTED_TAPE),
                base.rel(SOURCE_ATTEMPT_PACKAGE),
                base.rel(SOURCE_MODEL_MANIFEST),
                base.rel(SOURCE_PARENT_FINAL),
            ],
            "producer": base.rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [base.rel(path) for path in existing_outputs],
            "artifact_hashes": {base.rel(path): base.sha256_file(path) for path in existing_outputs if base.path_is_file(path)},
            "registry_links": [base.rel(RUN_REGISTRY), base.rel(PROJECT_LEDGER), base.rel(STAGE_LEDGER), base.rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령 재현 가능)",
            "lineage_judgment": "connected_with_package_boundary(패키지 경계로 연결)",
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
                "notes": "run343D trade shape rescue quality margin blend package artifact(343D 거래 형태 복구 품질 마진 혼합 패키지 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    base.append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], rows)


def configure_base() -> None:
    replacements = {
        "STAGE_ID": STAGE_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "PARENT_STAGE_ID": STAGE_ID,
        "STAGE_DIR": STAGE_DIR,
        "SOURCE_STAGE_DIR": SOURCE_STAGE_DIR,
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
        "REVIEW_DIR": REVIEW_DIR,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "SELECTION_STATUS": SELECTION_STATUS,
        "STAGE_BRIEF": STAGE_BRIEF,
        "STAGE_README": STAGE_README,
        "STAGE_LEDGER": STAGE_LEDGER,
        "PARENT_RUN_DIR": PARENT_RUN_DIR,
        "PARENT_FINAL_DECISION": PARENT_FINAL_DECISION,
        "PARENT_GATE_AUDIT": PARENT_GATE_AUDIT,
        "PARENT_QUEUE": PARENT_QUEUE,
        "PARENT_HANDOFF": PARENT_HANDOFF,
        "SOURCE_PACKAGE_DIR": SOURCE_PACKAGE_DIR,
        "SOURCE_FEATURE_MATRIX": SOURCE_FEATURE_MATRIX,
        "SOURCE_EXPECTED_TAPE": SOURCE_EXPECTED_TAPE,
        "SOURCE_ATTEMPT_PACKAGE": SOURCE_ATTEMPT_PACKAGE,
        "SOURCE_MODEL_MANIFEST": SOURCE_MODEL_MANIFEST,
        "SOURCE_PARENT_FINAL": SOURCE_PARENT_FINAL,
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
        "RUN342C_EXECUTION_QUEUE": RUN343E_EXECUTION_QUEUE,
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
        "write_registries": write_registries,
        "write_receipts": write_receipts,
        "write_artifact_registry": write_artifact_registry,
    }
    for key, value in replacements.items():
        setattr(base, key, value)


def main() -> None:
    materialize_parent_queue()
    configure_base()
    base.main()


if __name__ == "__main__":
    main()

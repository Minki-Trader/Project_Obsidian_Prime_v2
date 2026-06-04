from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import (  # noqa: E402
    attach_mt5_report_metrics,
    collect_mt5_strategy_report_artifacts,
    copy_to_common_files,
    mt5_runtime_module_hashes,
    remove_existing_mt5_report_artifacts,
    sha256_file,
)
from foundation.mt5.terminal_runner import run_mt5_tester, wait_for_mt5_runtime_outputs  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import package_density_restore_stress_candidate_runtime_probe_without_db as bd_package  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as runtime_base  # noqa: E402
from stage_pipelines.stage364 import review_density_restore_forward_regime_stress_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BJ"
RUN_ID = "run364BJ_implement_h19_opposite_margin_runtime_guard_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
NEXT_RUN_ID_COMPLETED = "run364BK_review_h19_opposite_margin_runtime_probe_without_db_v1"
NEXT_RUN_ID_BLOCKED = "run364BK_repair_or_execute_h19_opposite_margin_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364BJ_h19_opposite_margin_runtime_guard_packaged_mt5_probe_attempted_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364BJ_h19_opposite_margin_runtime_guard_packaged_mt5_probe_blocked_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_for_h19_guard_review_required_no_authority"
JUDGMENT_BLOCKED = "runtime_guard_support_compiled_but_mt5_probe_outputs_missing_or_blocked_no_authority"
CLAIM_BOUNDARY = (
    "research_development_runtime_guard_support_and_probe_attempt_only_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

ATTEMPT_NAME = "run364BJ_h19_opp_margin_bh02"
REPORT_NAME = "OPv2_run364BJ_h19_opp_margin_bh02"
EXPLORATION_LABEL = "stage364_DensityRestoreForwardRegime__H19OppositeMarginRuntimeGuard"
MODEL_ID = runtime_base.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin_h19_opposite_guard"

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
EA_GUARD_SUPPORT_AUDIT = RUN_DIR / "ea_guard_support_audit.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = COMPILE_DIR / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
RUNTIME_OUTPUT_VALIDATION = RUN_DIR / "runtime_output_validation.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BJ_h19_opposite_margin_runtime_guard.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BJ_h19_opposite_margin_runtime_guard.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
MT5_INPUT_CONTRACT = ROOT / "docs" / "contracts" / "mt5_ea_input_order_contract_fpmarkets_v2.md"

PARENT_FINAL = parent.FINAL_DECISION
PARENT_GATE_AUDIT = parent.GATE_AUDIT
PARENT_QUEUE = parent.RUN364BJ_IMPLEMENTATION_QUEUE
PARENT_SELECTED = parent.PARENT_SELECTED
PARENT_TRADE_TAPE = parent.PARENT_SELECTED.parent / "expected_tapes" / "selected_trade_tape.csv"
PARENT_REPORT = parent.REPORT_PATH
SOURCE_FEATURE_MATRIX = runtime_base.FEATURE_MATRIX
SOURCE_FEATURE_ORDER = runtime_base.FEATURE_ORDER
SOURCE_ONNX = runtime_base.SOURCE_ONNX
SOURCE_PROBABILITY_TAPE = bd_package.SOURCE_PROBABILITY_TAPE
SOURCE_EA = runtime_base.EA_SOURCE
SOURCE_EA_BINARY = runtime_base.EA_BINARY
PORTABLE_EA_EX5 = runtime_base.PORTABLE_EA_EX5
DEFAULT_METAEDITOR = runtime_base.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_TERMINAL = runtime_base.DEFAULT_TERMINAL
DEFAULT_COMMON_FILES = runtime_base.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = runtime_base.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = runtime_base.DEFAULT_PORTABLE_ROOT

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_h19_opposite_margin_runtime_guard"
COMMON_FEATURE = f"{COMMON_ROOT}/features/density_lift_trade_shape_features.csv"
COMMON_MODEL = f"{COMMON_ROOT}/models/{MODEL_ID}.onnx"
COMMON_FEATURE_ORDER = f"{COMMON_ROOT}/config/feature_order.json"
COMMON_PROBABILITY = f"{COMMON_ROOT}/expected/density_restore_probability_tape.csv"
COMMON_TRADE = f"{COMMON_ROOT}/expected/bh02_h19_opp_margin_expected_trade_tape.csv"
COMMON_SELECTED = f"{COMMON_ROOT}/config/selected_proxy_candidate.json"
COMMON_POLICY = f"{COMMON_ROOT}/config/runtime_policy_config.json"
COMMON_TELEMETRY = f"{COMMON_ROOT}/telemetry/{ATTEMPT_NAME}_telemetry.csv"
COMMON_SUMMARY = f"{COMMON_ROOT}/telemetry/{ATTEMPT_NAME}_summary.csv"

INPUT_FILES = [
    PARENT_FINAL,
    PARENT_GATE_AUDIT,
    PARENT_QUEUE,
    PARENT_SELECTED,
    PARENT_TRADE_TAPE,
    PARENT_REPORT,
    bd_package.RUNTIME_POLICY_CONFIG,
    bd_package.TESTER_SET_MANIFEST,
    SOURCE_FEATURE_MATRIX,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_PROBABILITY_TAPE,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    EA_GUARD_SUPPORT_AUDIT,
    RUNTIME_POLICY_CONFIG,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    RUNTIME_OUTPUT_VALIDATION,
    STRATEGY_TESTER_REPORTS,
    RUNTIME_OUTPUT_COPY,
    PROXY_MT5_DIFF,
    RUNTIME_PARITY_CONTRACT,
    TESTER_IDENTITY_CONTRACT,
    BACKTEST_RECEIPT,
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
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, COMPILE_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(io_path(path), exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364BJ inputs(364BJ 입력 누락): " + ", ".join(missing))
    parent_final = read_json(PARENT_FINAL)
    selected = read_json(PARENT_SELECTED)
    bd_policy = read_json(bd_package.RUNTIME_POLICY_CONFIG)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {parent_final.get('next_run_id')} != {RUN_ID}")
    if parent_final.get("runtime_support_gap") is not True:
        raise RuntimeError("parent does not require runtime guard support(부모가 런타임 가드 지원을 요구하지 않음)")
    gates = read_rows(PARENT_GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gates are not fully passed(부모 게이트가 모두 통과가 아님)")
    if selected.get("variant_id") != parent_final.get("selected_variant_id"):
        raise RuntimeError("selected candidate mismatch(선택 후보 불일치)")
    return parent_final, selected, bd_policy


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": input_role(path),
            "effect": "BJ 런타임 가드 구현과 패키지 입력 계보(lineage, 계보)를 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def input_role(path: Path | str) -> str:
    text = rel(path)
    if "run364BI" in text:
        return "BI runtime gap review(BI 런타임 차이 검토)"
    if "run364BH" in text:
        return "BH selected proxy clue(BH 선택 프록시 단서)"
    if "run364BD" in text:
        return "baseline runtime policy package(BD 기준 런타임 정책 패키지)"
    if "foundation/mt5" in text:
        return "EA runtime source(EA 런타임 소스)"
    return "runtime package input(런타임 패키지 입력)"


def audit_ea_guard_support() -> list[dict[str, Any]]:
    text = io_path(SOURCE_EA).read_text(encoding="utf-8-sig")
    contract = io_path(MT5_INPUT_CONTRACT).read_text(encoding="utf-8-sig")
    checks = [
        ("input_enabled", "InpTimeMarginGuardEnabled", text, True),
        ("input_side", "InpTimeMarginGuardSide", text, True),
        ("input_hour_start", "InpTimeMarginGuardStartHour", text, True),
        ("input_hour_end", "InpTimeMarginGuardEndHour", text, True),
        ("input_basis", "InpTimeMarginGuardBasis", text, True),
        ("input_min_margin", "InpTimeMarginGuardMinMargin", text, True),
        ("opposite_basis_logic", "p_long - p_short", text, True),
        ("guard_reason", "time_margin_guard:hour=", text, True),
        ("contract_documented", "Runtime time-margin guard", contract, True),
    ]
    rows = []
    for check_id, token, source_text, required in checks:
        rows.append(
            {
                "run_id": RUN_ID,
                "check_id": check_id,
                "token": token,
                "present": token in source_text,
                "required": required,
                "status": "passed" if token in source_text else "failed",
                "effect": "EA가 h19 opposite-margin guard(19시 반대마진 가드)를 같은 의미로 표현할 수 있는지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EA_GUARD_SUPPORT_AUDIT, rows)
    return rows


def date_bounds(probability: pd.DataFrame) -> tuple[str, str, str, str]:
    column = "timestamp_utc" if "timestamp_utc" in probability.columns else "bar_time_server"
    timestamps = pd.to_datetime(probability[column], utc=True)
    first = pd.Timestamp(timestamps.min()).tz_convert("UTC")
    last = pd.Timestamp(timestamps.max()).tz_convert("UTC")
    return (
        first.strftime("%Y.%m.%d %H:%M:%S"),
        last.strftime("%Y.%m.%d %H:%M:%S"),
        first.strftime("%Y.%m.%d"),
        (last + pd.Timedelta(days=1)).strftime("%Y.%m.%d"),
    )


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(DEFAULT_COMMON_FILES, local_path, common_path)
    return {
        "run_id": RUN_ID,
        "sync_id": sync_id,
        "source_path": rel(local_path),
        "common_path": common_path,
        "absolute_path": result["absolute_path"],
        "sha256": result["sha256"],
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_runtime_policy(selected: Mapping[str, Any], bd_policy: Mapping[str, Any]) -> dict[str, Any]:
    decision = dict(bd_policy.get("decision_surface", {}))
    decision.update(
        {
            "InpTimeMarginGuardEnabled": True,
            "InpTimeMarginGuardSide": "long",
            "InpTimeMarginGuardStartHour": 19,
            "InpTimeMarginGuardEndHour": 20,
            "InpTimeMarginGuardBasis": "opposite",
            "InpTimeMarginGuardMinMargin": as_float(selected.get("margin_min"), 0.002),
        }
    )
    policy = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_policy": rel(bd_package.RUNTIME_POLICY_CONFIG),
        "selected_variant_id": selected.get("variant_id"),
        "output_contract": OUTPUT_CONTRACT,
        "decision_surface": decision,
        "exact_guard": {
            "research_semantic": "entry_hour == 19, side == long, p_long - p_short < 0.002 blocks entry",
            "runtime_semantic": "InpTimeMarginGuardEnabled=true, side=long, hour=[19,20), basis=opposite, min_margin=0.002",
            "timestamp_boundary": "closed M5 target time only(닫힌 M5 대상 시간만)",
        },
        "expected_proxy": {
            "net_profit": selected.get("net_profit"),
            "profit_factor": selected.get("profit_factor"),
            "expectancy": selected.get("expectancy"),
            "trade_count": selected.get("trade_count"),
            "density": selected.get("trade_density_per_business_day"),
            "max_closed_drawdown_amount": selected.get("max_closed_drawdown_amount"),
            "recovery_factor": selected.get("recovery_factor"),
            "long_trade_count": selected.get("long_trade_count"),
            "short_trade_count": selected.get("short_trade_count"),
        },
        "mt5_execution": "attempted_by_run364BJ",
        "runtime_authority": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, policy)
    return policy


def build_package(selected: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    probability = pd.read_csv(io_path(SOURCE_PROBABILITY_TAPE))
    first_time, last_time, from_date, to_date = date_bounds(probability)
    feature_order_payload = read_json(SOURCE_FEATURE_ORDER)
    feature_order = feature_order_payload["feature_columns"]
    feature_order_hash = feature_order_payload["feature_order_hash"]
    decision = policy["decision_surface"]

    sync_rows = [
        copy_common(SOURCE_FEATURE_MATRIX, COMMON_FEATURE, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_ONNX, COMMON_MODEL, "common_primary_onnx", "ONNX(온엑스) 모델을 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_FEATURE_ORDER, COMMON_FEATURE_ORDER, "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_PROBABILITY_TAPE, COMMON_PROBABILITY, "common_expected_probability_tape", "expected probability tape(예상 확률 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(PARENT_TRADE_TAPE, COMMON_TRADE, "common_expected_trade_tape", "BH selected expected trade tape(BH 선택 예상 거래 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(PARENT_SELECTED, COMMON_SELECTED, "common_selected_candidate", "selected candidate(선택 후보)를 Common Files(공용 파일)에 복사한다."),
        copy_common(RUNTIME_POLICY_CONFIG, COMMON_POLICY, "common_runtime_policy", "runtime policy(런타임 정책)를 Common Files(공용 파일)에 복사한다."),
    ]
    write_csv(COMMON_FILES_SYNC, sync_rows)

    set_path = SET_DIR / "OPv2_run364BJ.set"
    ini_path = INI_DIR / "OPv2_run364BJ.ini"
    set_values = {
        "InpRunId": f"{RUN_ID}_{ATTEMPT_NAME}",
        "InpExplorationLabel": EXPLORATION_LABEL,
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_h19_opposite_margin",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": COMMON_FEATURE,
        "InpFeatureCount": len(feature_order),
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": False,
        "InpModelPath": COMMON_MODEL,
        "InpModelId": MODEL_ID,
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpModelUseMatrixTensor": False,
        "InpFeatureOrderHash": feature_order_hash,
        "InpFallbackEnabled": False,
        "InpShortThreshold": as_float(decision.get("InpShortThreshold"), 0.45),
        "InpLongThreshold": as_float(decision.get("InpLongThreshold"), 0.0),
        "InpMinMargin": as_float(decision.get("InpMinMargin"), -0.000562137088),
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpSideFilterEnabled": bool(decision.get("InpSideFilterEnabled", True)),
        "InpSideFilterFeatureIndex": int(decision.get("InpSideFilterFeatureIndex", bd_package.SIDE_FILTER_FEATURE_INDEX)),
        "InpFallbackSideFilterFeatureIndex": -1,
        "InpBlockShortFeatureRange": False,
        "InpBlockLongFeatureRange": bool(decision.get("InpBlockLongFeatureRange", True)),
        "InpBlockLongFeatureMin": as_float(decision.get("InpBlockLongFeatureMin"), 40.0),
        "InpBlockLongFeatureMax": as_float(decision.get("InpBlockLongFeatureMax"), bd_package.SIDE_FILTER_BLOCK_MAX),
        "InpBlockPremarketShort": bool(decision.get("InpBlockPremarketShort", True)),
        "InpPremarketStartHour": int(decision.get("InpPremarketStartHour", 12)),
        "InpPremarketEndHour": int(decision.get("InpPremarketEndHour", 17)),
        "InpMarchNonHour16MarginFilter": bool(decision.get("InpMarchNonHour16MarginFilter", True)),
        "InpMarchFilterMonth": int(decision.get("InpMarchFilterMonth", 3)),
        "InpMarchFilterBlockedHour": int(decision.get("InpMarchFilterBlockedHour", 16)),
        "InpMarchFilterAbsMarginMin": as_float(decision.get("InpMarchFilterAbsMarginMin"), 0.10),
        "InpEntryMarginFloor": as_float(decision.get("InpEntryMarginFloor"), 0.00025),
        "InpTimeMarginGuardEnabled": True,
        "InpTimeMarginGuardSide": "long",
        "InpTimeMarginGuardStartHour": 19,
        "InpTimeMarginGuardEndHour": 20,
        "InpTimeMarginGuardBasis": "opposite",
        "InpTimeMarginGuardMinMargin": as_float(selected.get("margin_min"), 0.002),
        "InpAllowTrading": True,
        "InpFixedLot": 0.1,
        "InpMagic": 36426001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": int(decision.get("InpMaxHoldBars", 6)),
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpExitRiskOverlayEnabled": False,
        "InpAtrSltpEnabled": False,
        "InpModelRiskSizingEnabled": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": COMMON_TELEMETRY,
        "InpSummaryCsvPath": COMMON_SUMMARY,
    }
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date=from_date,
            to_date=to_date,
            report=REPORT_NAME,
        ),
        ini_path,
        set_file_path=Path(set_path.name),
    )
    package = {
        "set_path": set_path,
        "ini_path": ini_path,
        "set_values": set_values,
        "set_payload": set_payload,
        "ini_payload": ini_payload,
        "first_time": first_time,
        "last_time": last_time,
        "from_date": from_date,
        "to_date": to_date,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "probability_rows": int(len(probability)),
        "common_sync_rows": len(sync_rows),
        "common_sync_missing": sum(1 for row in sync_rows if not Path(row["absolute_path"]).exists()),
    }
    write_csv(
        TESTER_SET_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "time_margin_guard_enabled": True,
                "time_margin_guard_side": "long",
                "time_margin_guard_hours": "19-20",
                "time_margin_guard_basis": "opposite",
                "time_margin_guard_min_margin": as_float(selected.get("margin_min"), 0.002),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_INI_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "symbol": ini_payload["tester"].get("Symbol"),
                "period": ini_payload["tester"].get("Period"),
                "model": ini_payload["tester"].get("Model"),
                "deposit": ini_payload["tester"].get("Deposit"),
                "leverage": ini_payload["tester"].get("Leverage"),
                "from_date": from_date,
                "to_date": to_date,
                "report": REPORT_NAME,
                "set_file": set_path.name,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "model_id": MODEL_ID,
                "variant_id": selected.get("variant_id"),
                "tier": "Tier A",
                "split": "validation_oos_h19_opposite_margin",
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "set_name": set_path.name,
                "ini_name": ini_path.name,
                "report_name": REPORT_NAME,
                "common_telemetry_path": COMMON_TELEMETRY,
                "common_summary_path": COMMON_SUMMARY,
                "runtime_telemetry_expected": COMMON_TELEMETRY,
                "runtime_summary_expected": COMMON_SUMMARY,
                "required_outputs": "runtime telemetry, runtime summary, strategy tester report(런타임 기록, 런타임 요약, 전략 테스터 보고서)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "contract_id": "tester_identity",
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "terminal": DEFAULT_TERMINAL.as_posix(),
                "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "symbol": "US100",
                "timeframe": "M5",
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "report_name": REPORT_NAME,
                "effect": "MT5 KPI(핵심 성과 지표) 비교 기준을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return package


def compile_and_sync() -> tuple[dict[str, Any], dict[str, Any]]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    write_json(COMPILE_RESULT, result)
    sync_payload = {
        "run_id": RUN_ID,
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_binary": PORTABLE_EA_EX5.as_posix(),
        "compile_status": result.get("status"),
        "copied": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if result.get("status") == "completed" and exists(SOURCE_EA_BINARY):
        os.makedirs(io_path(PORTABLE_EA_EX5.parent), exist_ok=True)
        shutil.copy2(io_path(SOURCE_EA_BINARY), io_path(PORTABLE_EA_EX5))
        sync_payload.update(
            {
                "copied": True,
                "source_sha256": sha(SOURCE_EA_BINARY),
                "portable_sha256": sha(PORTABLE_EA_EX5),
                "effect": "compiled EA binary(컴파일된 EA 바이너리)를 portable tester(포터블 테스터)에 동기화한다.",
            }
        )
    else:
        sync_payload.update(
            {
                "blocker": result.get("blocker", "compile_failed_or_binary_missing"),
                "effect": "compile failure(컴파일 실패)를 런타임 탐침 주장 경계에 기록한다.",
            }
        )
    write_json(PORTABLE_EA_SYNC, sync_payload)
    return result, sync_payload


def terminal_processes() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
    payload: Any = []
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            if isinstance(payload, Mapping):
                payload = [payload]
        except json.JSONDecodeError:
            payload = proc.stdout.strip()
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "processes": payload,
        "status": "no_terminal64_process" if not payload else "terminal64_process_present",
        "effect": "terminal64.exe process(터미널 프로세스) 충돌 여부를 확인한다.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage364BJ h19 opposite-margin runtime guard package and MT5 probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    return parser.parse_args()


def clean_runtime_outputs(common_files_root: Path) -> None:
    for common_path in [COMMON_TELEMETRY, COMMON_SUMMARY]:
        target = common_files_root / Path(common_path)
        if exists(target):
            io_path(target).unlink()


def execute_mt5_probe(args: argparse.Namespace, package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    attempt = read_rows(RUNTIME_PROBE_ATTEMPT_PACKAGE)[0]
    attempt["ini"] = {"tester": {"Report": attempt.get("report_name", REPORT_NAME)}}
    attempt["set"] = {"path": attempt.get("set_path", "")}
    terminal_probe = terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    results: list[dict[str, Any]] = []
    runtime_outputs: dict[str, Any] = {"status": "blocked", "blocker": "not_attempted"}
    report_records: list[dict[str, Any]] = []
    copy_rows: list[dict[str, Any]] = []
    if compile_result.get("status") != "completed" or portable_sync.get("copied") is not True:
        results.append({"attempt_name": ATTEMPT_NAME, "status": "blocked", "blocker": "compile_or_portable_sync_failed", "claim_boundary": CLAIM_BOUNDARY})
    elif terminal_probe.get("status") != "no_terminal64_process":
        results.append({"attempt_name": ATTEMPT_NAME, "status": "blocked", "blocker": "terminal64_process_present", "terminal_probe": terminal_probe, "claim_boundary": CLAIM_BOUNDARY})
    else:
        common_root = Path(args.common_files_root)
        tester_profile_root = Path(args.tester_profile_root)
        terminal_data_root = Path(args.terminal_data_root)
        clean_runtime_outputs(common_root)
        remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
        profile_ini = tester_profile_root / attempt["ini_name"]
        profile_set = tester_profile_root / attempt["set_name"]
        try:
            tester_result = run_mt5_tester(
                Path(args.terminal_path),
                ROOT / attempt["ini_path"],
                set_path=ROOT / attempt["set_path"],
                tester_profile_set_path=profile_set,
                tester_profile_ini_path=profile_ini,
                timeout_seconds=args.timeout_seconds,
                terminal_extra_args=["/portable"],
            )
        except subprocess.TimeoutExpired as exc:
            tester_result = {
                "status": "blocked",
                "command": exc.cmd,
                "returncode": None,
                "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                "blocker": "terminal_timeout",
            }
        runtime_outputs = wait_for_mt5_runtime_outputs(
            common_root,
            attempt,
            timeout_seconds=args.wait_timeout_seconds,
            poll_seconds=2.0,
        )
        if runtime_outputs.get("status") != "completed":
            tester_result["status"] = "blocked"
            tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
        report_records = collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=[attempt],
            run_id=RUN_ID,
        )
        attach_mt5_report_metrics([tester_result], report_records)
        results.append({**tester_result, "attempt_name": ATTEMPT_NAME, "runtime_outputs": runtime_outputs, "claim_boundary": CLAIM_BOUNDARY})
    write_json(MT5_EXECUTION_RESULT, results)
    write_json(RUNTIME_OUTPUT_VALIDATION, runtime_outputs)
    write_json(STRATEGY_TESTER_REPORTS, report_records)

    common_root = Path(args.common_files_root)
    for common_path, suffix in [(COMMON_TELEMETRY, "telemetry"), (COMMON_SUMMARY, "summary")]:
        source = common_root / Path(common_path)
        target = TELEMETRY_COPY_DIR / f"{ATTEMPT_NAME}_{suffix}.csv"
        copied = False
        if exists(source):
            os.makedirs(io_path(target.parent), exist_ok=True)
            shutil.copy2(io_path(source), io_path(target))
            copied = True
        copy_rows.append(
            {
                "run_id": RUN_ID,
                "copy_id": f"{ATTEMPT_NAME}_{suffix}",
                "source_path": source.as_posix(),
                "target_path": rel(target),
                "source_exists": exists(source),
                "copied": copied,
                "sha256": sha(target) if exists(target) else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_OUTPUT_COPY, copy_rows)
    return results, runtime_outputs, report_records, copy_rows


def metric_from_report(report_records: Sequence[Mapping[str, Any]], key: str) -> Any:
    for record in report_records:
        metrics = record.get("metrics") or {}
        if key in metrics:
            return metrics.get(key)
    return ""


def build_proxy_mt5_diff(selected: Mapping[str, Any], runtime_outputs: Mapping[str, Any], report_records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    last_summary = runtime_outputs.get("last_summary") if isinstance(runtime_outputs, Mapping) else {}
    if not isinstance(last_summary, Mapping):
        last_summary = {}
    rows = [
        {
            "run_id": RUN_ID,
            "attempt_name": ATTEMPT_NAME,
            "selected_variant_id": selected.get("variant_id"),
            "proxy_net_profit": selected.get("net_profit"),
            "proxy_profit_factor": selected.get("profit_factor"),
            "proxy_trade_count": selected.get("trade_count"),
            "proxy_density": selected.get("trade_density_per_business_day"),
            "proxy_expectancy": selected.get("expectancy"),
            "mt5_net_profit": metric_from_report(report_records, "net_profit"),
            "mt5_profit_factor": metric_from_report(report_records, "profit_factor"),
            "mt5_trade_count": metric_from_report(report_records, "trade_count"),
            "runtime_model_ok_count": last_summary.get("model_ok_count", ""),
            "runtime_feature_ready_count": last_summary.get("feature_ready_count", ""),
            "runtime_status": runtime_outputs.get("status", "blocked") if isinstance(runtime_outputs, Mapping) else "blocked",
            "usability": "mt5_kpi_review_ready(테스터 KPI 검토 준비)" if metric_from_report(report_records, "net_profit") != "" else "probe_attempt_recorded_kpi_missing(탐침 시도 기록, KPI 누락)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(PROXY_MT5_DIFF, rows)
    return rows


def write_contracts(policy: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> None:
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "research_path": rel(parent.PARENT_SELECTED),
                "runtime_path": rel(TESTER_SET_MANIFEST),
                "shared_contract": "closed M5 bar probabilities, p_short/p_flat/p_long, threshold_margin, h19 opposite-margin guard(닫힌 5분봉 확률, 3확률, 임계값 마진, 19시 반대마진 가드)",
                "known_differences": "Strategy Tester cost/fill can differ from closed-trade proxy until BJ output is reviewed(전략 테스터 비용/체결은 BJ 출력 검토 전까지 프록시와 다를 수 있음)",
                "parity_check": "EA compile, Common Files sync, set/ini package, terminal attempt(EA 컴파일, 공용 파일 동기화, 설정/INI 패키지, 터미널 시도)",
                "parity_identity": json.dumps(mt5_runtime_module_hashes(), ensure_ascii=False),
                "runtime_claim_boundary": "runtime_probe_attempt_only(런타임 탐침 시도 전용)",
            }
        ],
    )


def final_payload(
    selected: Mapping[str, Any],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    execution_results: Sequence[Mapping[str, Any]],
    runtime_outputs: Mapping[str, Any],
    report_records: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    runtime_completed = runtime_outputs.get("status") == "completed" if isinstance(runtime_outputs, Mapping) else False
    report_ready = any((record.get("metrics") or {}).get("status") in ("parsed", "completed") for record in report_records)
    completed = runtime_completed or report_ready
    next_run_id = NEXT_RUN_ID_COMPLETED if completed else NEXT_RUN_ID_BLOCKED
    first_result = dict(execution_results[0]) if execution_results else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": f"stage364BJ_open_{next_run_id}",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_variant_id": selected.get("variant_id"),
        "expected_proxy_net_profit": selected.get("net_profit"),
        "expected_proxy_profit_factor": selected.get("profit_factor"),
        "expected_proxy_trade_count": selected.get("trade_count"),
        "expected_proxy_density": selected.get("trade_density_per_business_day"),
        "compile_status": compile_result.get("status"),
        "portable_ea_copied": portable_sync.get("copied"),
        "mt5_execution_status": first_result.get("status", "not_attempted"),
        "mt5_blocker": first_result.get("blocker", ""),
        "runtime_output_status": runtime_outputs.get("status", "blocked") if isinstance(runtime_outputs, Mapping) else "blocked",
        "strategy_report_status": report_records[0].get("status", "missing") if report_records else "missing",
        "runtime_output_copy_rows": len(copy_rows),
        "new_model_training": "not_run",
        "new_mt5_execution": "attempted",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def gate_rows(compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any], runtime_outputs: Mapping[str, Any], report_records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    compile_ok = compile_result.get("status") == "completed"
    sync_ok = portable_sync.get("copied") is True
    runtime_attempted = exists(MT5_EXECUTION_RESULT)
    runtime_ok = runtime_outputs.get("status") == "completed" if isinstance(runtime_outputs, Mapping) else False
    report_ok = any(record.get("status") not in ("", "missing") for record in report_records)
    required = [
        ("code_surface_audit", exists(EA_GUARD_SUPPORT_AUDIT) and all(row.get("status") == "passed" for row in read_rows(EA_GUARD_SUPPORT_AUDIT)), "EA 입력과 계약 문서가 새 guard(가드)를 포함한다."),
        ("metaeditor_compile_gate", compile_ok, "MetaEditor compile(메타에디터 컴파일)이 통과해야 런타임 패키지를 주장할 수 있다."),
        ("portable_sync_gate", sync_ok, "compiled EX5(컴파일된 EX5)를 portable tester(포터블 테스터)에 동기화한다."),
        ("tester_identity_gate", exists(TESTER_SET_MANIFEST) and exists(TESTER_INI_MANIFEST), "US100 M5 real ticks(실제 틱), deposit 500(예치금 500), leverage 100(레버리지 100)을 고정한다."),
        ("runtime_execution_attempt_gate", runtime_attempted, "MT5 Strategy Tester(전략 테스터) 실행을 시도하거나 차단 로그를 남긴다."),
        ("runtime_evidence_gate", runtime_ok, "runtime telemetry/summary(런타임 기록/요약)가 있어야 완료 증거가 된다."),
        ("strategy_report_gate", report_ok, "전략 테스터 보고서가 있어야 MT5 KPI를 읽는다."),
        ("proxy_mt5_diff_gate", exists(PROXY_MT5_DIFF), "proxy expected value(프록시 예상값)와 MT5 출력 차이 기록을 만든다."),
        ("final_claim_guard", True, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 금지한다."),
        ("required_gate_coverage_audit", True, "필수 게이트(required gates, 필수 게이트)를 closeout(종료 기록)에 연결한다."),
    ]
    rows = []
    for gate, passed, effect in required:
        rows.append(
            {
                "run_id": RUN_ID,
                "gate": gate,
                "status": "passed" if passed else "failed",
                "evidence_path": rel(GATE_AUDIT if gate == "required_gate_coverage_audit" else RUN_DIR),
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "tester_output": rel(STRATEGY_TESTER_REPORTS),
            "execution_result": rel(MT5_EXECUTION_RESULT),
            "forensic_boundary": "compile and execution attempt recorded; KPI review remains next if output exists(컴파일과 실행 시도 기록, 출력 있으면 KPI 검토는 다음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(PARENT_SELECTED),
            "runtime_path": [rel(SOURCE_EA), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST)],
            "shared_contract": "h19 long opposite margin guard(19시 롱 반대마진 가드)",
            "known_differences": "MT5 cost/fill/position sequence requires tester output review(MT5 비용/체결/포지션 순서는 테스터 출력 검토 필요)",
            "parity_check": [rel(EA_GUARD_SUPPORT_AUDIT), rel(RUNTIME_PARITY_CONTRACT), rel(PROXY_MT5_DIFF)],
            "runtime_claim_boundary": "runtime_probe_attempt_only(런타임 탐침 시도 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "proxy_candidate": selected.get("variant_id"),
            "proxy_kpi": {
                "net_profit": selected.get("net_profit"),
                "profit_factor": selected.get("profit_factor"),
                "trade_count": selected.get("trade_count"),
                "density": selected.get("trade_density_per_business_day"),
            },
            "mt5_diff_path": rel(PROXY_MT5_DIFF),
            "attribution_boundary": "diff attribution waits for parsed MT5 KPI(차이 귀속은 파싱된 MT5 KPI 이후)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "h19 opposite-margin runtime guard support and probe attempt(19시 반대마진 런타임 가드 지원과 탐침 시도)",
            "evidence_available": [rel(EA_GUARD_SUPPORT_AUDIT), rel(COMPILE_RESULT), rel(MT5_EXECUTION_RESULT), rel(PROXY_MT5_DIFF)],
            "evidence_missing": [] if final.get("runtime_output_status") == "completed" else ["runtime summary or tester KPI may be missing(런타임 요약 또는 테스터 KPI 누락 가능)"],
            "judgment_label": final.get("judgment"),
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": final.get("next_run_id"),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": final.get("judgment"),
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve", "forward_passed"],
            "effect": "BJ를 runtime probe attempt(런타임 탐침 시도)로만 닫고 운영 주장은 막는다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": final.get("next_run_id"),
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
            "availability": "tracked_or_manifested_after_commit(커밋 후 추적 또는 목록화)",
            "lineage_judgment": "connected_with_runtime_attempt_boundary(런타임 시도 경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def sync_stage_brief_header(next_run_id: str) -> None:
    if not STAGE_BRIEF.exists():
        return
    text = STAGE_BRIEF.read_text(encoding="utf-8-sig")
    marker = "Current active run("
    lines = []
    replaced = False
    for line in text.splitlines():
        if line.startswith(marker):
            lines.append(f"Current active run(현재 활성 실행): `{next_run_id}`")
            replaced = True
        else:
            lines.append(line)
    if replaced:
        write_text(STAGE_BRIEF, "\n".join(lines) + "\n", bom=True)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    diff_rows = read_rows(PROXY_MT5_DIFF) if exists(PROXY_MT5_DIFF) else []
    support_rows = read_rows(EA_GUARD_SUPPORT_AUDIT)
    report = f"""# run364BJ h19 opposite-margin runtime guard(364BJ 19시 반대마진 런타임 가드)

## Scope(범위)
- Parent(부모): `{PARENT_RUN_ID}`
- Candidate(후보): `{final['selected_variant_id']}`
- New model training(새 모델 학습): not run(미실행)
- MT5 execution(메타트레이더5 실행): `{final['new_mt5_execution']}`
- Operating claim(운영 주장): not claimed(주장 안 함)

## Result(결과)
EA(`Expert Advisor`, 전문가 자문)에 generic time-margin guard(범용 시간-마진 가드)를 추가하고, BJ `.set/.ini` package(설정/INI 패키지)를 만들었다. 효과는 BH proxy rule(BH 프록시 규칙) `hour 19 long p_long-p_short < 0.002`를 MT5에서 같은 의미로 켤 수 있게 한 것이다.

Compile status(컴파일 상태): `{final['compile_status']}`. Portable sync(포터블 동기화): `{final['portable_ea_copied']}`.

Runtime output status(런타임 출력 상태): `{final['runtime_output_status']}`. Strategy report status(전략 보고서 상태): `{final['strategy_report_status']}`.

## Support Audit(지원 감사)
{markdown_table(support_rows, ['check_id', 'present', 'status', 'effect'], 12)}

## Proxy vs MT5(프록시 대 MT5)
{markdown_table(diff_rows, ['proxy_net_profit', 'proxy_profit_factor', 'proxy_trade_count', 'mt5_net_profit', 'mt5_profit_factor', 'mt5_trade_count', 'usability'], 4)}

## Gates(게이트)
{markdown_table(gates, ['gate', 'status', 'effect'], 12)}
"""
    write_text(REPORT_PATH, report, bom=True)
    decision_doc = f"""# {TODAY} Stage364BJ decision(결정)

Decision(결정): `{final['decision']}`

Judgment(판정): `{final['judgment']}`

Effect(효과): h19 opposite-margin guard(19시 반대마진 가드)를 EA 런타임 입력과 `.set` 패키지로 표현 가능하게 만들었다. MT5 output(메타트레이더5 출력)이 부족하면 다음 실행은 repair/execute(수리/실행)로 간다.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""
    write_text(DECISION_DOC, decision_doc, bom=True)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{final['next_run_id']}`

Current truth(현재 진실): `run364BJ` added exact h19 opposite-margin runtime guard support(정확 19시 반대마진 런타임 가드 지원) and attempted the narrow MT5 runtime probe(좁은 MT5 런타임 탐침 시도). Compile status(컴파일 상태) `{final['compile_status']}`, runtime output status(런타임 출력 상태) `{final['runtime_output_status']}`.

Selected clue(선택 단서): `bh02_long_h19_margin_opp_0020` proxy net `{final['expected_proxy_net_profit']}`, PF `{final['expected_proxy_profit_factor']}`, trades `{final['expected_proxy_trade_count']}`, density `{final['expected_proxy_density']}`.

Next action(다음 행동): `{final['next_run_id']}`.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(CURRENT_WORKING_STATE, current, bom=True)
    workspace_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {final['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
"""
    write_text(WORKSPACE_STATE, workspace_state, bom=False)
    selection = f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{final['next_run_id']}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe candidate(런타임 탐침 후보): `{final['selected_variant_id']}`

Status(상태): `{final['judgment']}`

Proxy KPI(프록시 KPI): net `{final['expected_proxy_net_profit']}`, PF `{final['expected_proxy_profit_factor']}`, trades `{final['expected_proxy_trade_count']}`, density `{final['expected_proxy_density']}`.

Runtime package(런타임 패키지): compile `{final['compile_status']}`, portable sync `{final['portable_ea_copied']}`, MT5 execution status `{final['mt5_execution_status']}`, runtime output `{final['runtime_output_status']}`.

Next action(다음 행동): `{final['next_run_id']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
"""
    write_text(SELECTION_STATUS, selection, bom=True)
    sync_stage_brief_header(str(final["next_run_id"]))
    append_text_once(REVIEW_INDEX, "<!-- run364BJ -->", f"\n<!-- run364BJ -->\n- `{RUN_ID}`: h19 opposite-margin runtime guard(19시 반대마진 런타임 가드) -> `{REPORT_PATH.relative_to(ROOT).as_posix()}`\n")
    append_text_once(STAGE_README, "<!-- run364BJ -->", f"\n<!-- run364BJ -->\n## run364BJ h19 opposite-margin runtime guard(19시 반대마진 런타임 가드)\n\n`{final['judgment']}`. Next(다음): `{final['next_run_id']}`.\n")
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364BJ -->", f"\n<!-- run364BJ -->\n- {final['created_at_utc']} `{RUN_ID}` added EA time-margin guard(EA 시간-마진 가드 추가), packaged exact h19 opposite-margin candidate(정확 19시 반대마진 후보 패키지), and attempted MT5 runtime probe(MT5 런타임 탐침 시도).\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364BJ_h19_opposite_margin_runtime_guard -->", f"\n<!-- run364BJ_h19_opposite_margin_runtime_guard -->\n- Idea(아이디어): h19 opposite-margin runtime guard(19시 반대마진 런타임 가드). Effect(효과): proxy clue(프록시 단서)를 MT5에서 같은 의미로 시험 가능하게 한다.\n")
    if str(final.get("status", "")).startswith("blocked"):
        append_text_once(NEGATIVE_RESULT_REGISTER, "<!-- run364BJ_probe_blocker -->", f"\n<!-- run364BJ_probe_blocker -->\n- Blocker memory(차단 기억): `{final.get('mt5_blocker') or final.get('runtime_output_status')}`. Effect(효과): 다음 실행이 같은 외부 검증 누락을 말로만 반복하지 않게 한다.\n")


def ledger_rows(final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "net_profit": final["expected_proxy_net_profit"],
        "profit_factor": final["expected_proxy_profit_factor"],
        "trade_count": final["expected_proxy_trade_count"],
        "trade_density_per_feature_day": final["expected_proxy_density"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "evidence_boundary": "runtime_guard_support_and_mt5_probe_attempt(런타임 가드 지원과 MT5 탐침 시도)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "next_action": final["next_run_id"],
        "question": "Can h19 opposite-margin proxy rule be executed with exact MT5 semantics?(19시 반대마진 프록시 규칙을 정확 MT5 의미로 실행할 수 있는가?)",
    }
    run_rows = [{**common, "lane": "runtime_probe_attempt(런타임 탐침 시도)", "path": rel(FINAL_DECISION)}]
    stage_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe_attempt"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe_attempt"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
            "row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": scope,
            "path": rel(FINAL_DECISION),
        }
        if scope == "missing_required":
            row.update({"net_profit": "", "profit_factor": "", "trade_count": "", "trade_density_per_feature_day": "", "notes": "Tier B fallback was not used in this exact guard probe(Tier B 대체는 이번 정확 가드 탐침에서 미사용)."})
        stage_rows.append(row)
    return run_rows, stage_rows, stage_rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    run_rows, stage_rows, project_rows = ledger_rows(final)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], stage_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=True)
    bd_package.repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path) if exists(path) and Path(path).is_file() else ""} for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    created_at = now_utc()
    _, selected, bd_policy = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    support_rows = audit_ea_guard_support()
    policy = build_runtime_policy(selected, bd_policy)
    package = build_package(selected, policy)
    compile_result, portable_sync = compile_and_sync()
    execution_results, runtime_outputs, report_records, copy_rows = execute_mt5_probe(args, package, compile_result, portable_sync)
    build_proxy_mt5_diff(selected, runtime_outputs, report_records)
    write_contracts(policy, package, compile_result, portable_sync)
    gates = gate_rows(compile_result, portable_sync, runtime_outputs, report_records)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(selected, compile_result, portable_sync, execution_results, runtime_outputs, report_records, copy_rows, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    write_docs(final, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

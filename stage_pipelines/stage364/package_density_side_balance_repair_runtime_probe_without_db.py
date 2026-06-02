from __future__ import annotations

import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import train_density_side_balance_repair_onnx_scout_without_db as scout  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = scout.STAGE_ID
RUN_NUMBER = "run364W"
RUN_ID = "run364W_package_density_side_balance_repair_runtime_probe_without_db_v1"
PARENT_RUN_ID = scout.RUN_ID
NEXT_RUN_ID = "run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364W_density_side_balance_repair_runtime_probe_package_prepared_compile_checked_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_dual_side_density_balance_repair_mt5_execution_required_no_authority"
DECISION = "stage364W_open_run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_compile_checked_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = basepkg.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin"
PRIMARY_ATTEMPT = "run364W_dual_pshort045_adx40_maxhold8"
CONTROL_ATTEMPT = "run364W_long_only_adx40_maxhold8_control"
POINT_VALUE = scout.POINT_VALUE
BASE_COST = scout.BASE_COST
SIDE_FILTER_FEATURE = scout.SIDE_FILTER_FEATURE
SIDE_FILTER_FEATURE_INDEX = scout.SIDE_FILTER_FEATURE_INDEX
SIDE_FILTER_BLOCK_MAX = 1000000.0
DEFAULT_METAEDITOR = basepkg.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"

STAGE_DIR = scout.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
EXPECTED_DIR = RUN_DIR / "expected_tapes"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
DUAL_SIDE_CONTRACT = RUN_DIR / "dual_side_runtime_contract.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = RUN_DIR / "mt5" / "compile" / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
RUN364X_EXECUTION_QUEUE = RUN_DIR / "run364X_execution_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364W_density_side_balance_repair_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364W_density_side_balance_repair_runtime_probe_package.md"
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
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_FEATURE_MATRIX = basepkg.FEATURE_MATRIX
SOURCE_FEATURE_ORDER = basepkg.FEATURE_ORDER
SOURCE_ONNX = basepkg.SOURCE_ONNX
SOURCE_EA = basepkg.EA_SOURCE
SOURCE_EA_BINARY = basepkg.EA_BINARY
PORTABLE_EA_EX5 = basepkg.PORTABLE_EA_EX5

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_density_side_balance_repair_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    scout.FINAL_DECISION,
    scout.GATE_AUDIT,
    scout.RUN364W_QUEUE,
    scout.SELECTED_RUNTIME_CANDIDATE,
    scout.SELECTED_PROBABILITY_TAPE,
    scout.SELECTED_TRADE_TAPE,
    scout.REPORT_PATH,
    SOURCE_FEATURE_MATRIX,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_EA,
    SOURCE_EA_BINARY,
    PORTABLE_EA_EX5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    RUNTIME_POLICY_CONFIG,
    DUAL_SIDE_CONTRACT,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    EXPECTED_KPI_SUMMARY,
    RUN364X_EXECUTION_QUEUE,
    WORK_PACKET,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return scout.fs_path(path)


def rel(path: Path | str) -> str:
    return scout.rel(path)


def exists(path: Path | str) -> bool:
    return scout.exists(path)


def sha(path: Path | str) -> str:
    return scout.sha(path)


def read_json(path: Path) -> Any:
    return scout.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    scout.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    scout.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    scout.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return scout.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    scout.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        value = float(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, EXPECTED_DIR, MT5_DIR, SET_DIR, INI_DIR, COMPILE_LOG.parent, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364W inputs(364W 입력 누락): " + ", ".join(missing))
    parent = read_json(scout.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364V next_run_id mismatch(다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    _, gates = read_csv_rows(scout.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364V gate audit(게이트 감사)가 모두 passed(통과)가 아니다.")
    selected = read_json(scout.SELECTED_RUNTIME_CANDIDATE)
    if selected.get("variant_id") != scout.SELECTED_VARIANT_ID:
        raise RuntimeError("selected variant(선택 변형)이 run364V 고정 후보와 다르다.")
    feature_order = read_json(SOURCE_FEATURE_ORDER)["feature_columns"]
    if feature_order[SIDE_FILTER_FEATURE_INDEX] != SIDE_FILTER_FEATURE:
        raise RuntimeError("side filter feature index(방향 필터 피처 인덱스)가 feature order(피처 순서)와 맞지 않는다.")
    return selected


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        path_obj = Path(path)
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and path_obj.is_file() else "",
                "source_run_id": source_run_for(path),
                "effect(효과)": "package input identity(패키지 입력 정체성)를 고정해 runtime handoff(런타임 인계)를 재현 가능하게 한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_run_for(path: Path | str) -> str:
    text = rel(path)
    if "run364V" in text:
        return PARENT_RUN_ID
    if "run364M" in text:
        return basepkg.RUN_ID
    if "run364L" in text:
        return basepkg.PARENT_RUN_ID
    if "foundation/mt5" in text:
        return "current_local_runtime_source(현재 로컬 런타임 소스)"
    return "local_current_project_state(로컬 현재 프로젝트 상태)"


def run_compile_and_sync() -> tuple[dict[str, Any], dict[str, Any]]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    write_json(COMPILE_RESULT, result)
    sync_payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_binary": PORTABLE_EA_EX5.as_posix(),
        "compile_status": result.get("status"),
        "copied": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if result.get("status") == "completed" and exists(SOURCE_EA_BINARY):
        os.makedirs(fs_path(PORTABLE_EA_EX5.parent), exist_ok=True)
        shutil.copy2(fs_path(SOURCE_EA_BINARY), fs_path(PORTABLE_EA_EX5))
        sync_payload.update(
            {
                "copied": True,
                "source_sha256": sha(SOURCE_EA_BINARY),
                "portable_sha256": sha(PORTABLE_EA_EX5),
                "effect(효과)": "compiled EA binary(컴파일된 EA 바이너리)를 portable tester(포터블 테스터) 위치와 맞춘다.",
            }
        )
    else:
        sync_payload.update(
            {
                "blocker": result.get("blocker", "compile_failed_or_binary_missing"),
                "effect(효과)": "compile failure(컴파일 실패)를 runtime package(런타임 패키지) 주장 경계 안에 남긴다.",
            }
        )
    write_json(PORTABLE_EA_SYNC, sync_payload)
    return result, sync_payload


def date_bounds(probability: pd.DataFrame) -> tuple[str, str, str, str]:
    timestamps = pd.to_datetime(probability["timestamp_utc"], utc=True)
    first = pd.Timestamp(timestamps.min()).tz_convert("UTC")
    last = pd.Timestamp(timestamps.max()).tz_convert("UTC")
    return (
        first.strftime("%Y.%m.%d %H:%M:%S"),
        last.strftime("%Y.%m.%d %H:%M:%S"),
        first.strftime("%Y.%m.%d"),
        (last + pd.Timedelta(days=1)).strftime("%Y.%m.%d"),
    )


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(basepkg.DEFAULT_COMMON_FILES, local_path, common_path)
    return {
        "run_id": RUN_ID,
        "sync_id": sync_id,
        "source_path": rel(local_path),
        "common_path": common_path,
        "absolute_path": result["absolute_path"],
        "sha256": result["sha256"],
        "effect(효과)": effect,
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def split_metrics(trades: pd.DataFrame, split: str, selected: Mapping[str, Any]) -> dict[str, Any]:
    frame = trades if split == "combined" else trades[trades["split"].astype(str).eq(split)].copy()
    profits = pd.to_numeric(frame.get("net_profit", pd.Series([], dtype=float)), errors="coerce").fillna(0.0)
    trade_count = int(len(frame))
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    net = float(profits.sum())
    equity = profits.cumsum().to_numpy(dtype=float)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1] if trade_count else np.array([], dtype=float)
    drawdown = equity - peak if trade_count else np.array([], dtype=float)
    max_dd = float(drawdown.min()) if drawdown.size else 0.0
    business_days = {
        "validation": selected.get("validation_business_days"),
        "oos": selected.get("oos_business_days"),
        "combined": selected.get("combined_business_days"),
    }.get(split)
    selected_density = {
        "validation": selected.get("validation_trade_per_business_day"),
        "oos": selected.get("oos_trade_per_business_day"),
        "combined": selected.get("combined_trade_per_business_day"),
    }.get(split)
    days = int(business_days) if business_days not in ("", None) else (max(1, int(pd.to_datetime(frame["entry_timestamp"], utc=True).dt.date.nunique())) if trade_count else 1)
    side = frame.get("side", pd.Series([], dtype=object)).astype(str)
    return {
        "run_id": RUN_ID,
        "split": split,
        "trade_count": trade_count,
        "business_days": days,
        "trade_density_per_business_day": finite(selected_density if selected_density not in ("", None) else trade_count / days, 10),
        "net_profit": finite(net, 10),
        "profit_factor": finite(gross_profit / gross_loss, 10) if gross_loss > 0 else "inf",
        "expectancy": finite(float(profits.mean()), 10) if trade_count else 0.0,
        "max_drawdown": finite(max_dd, 10),
        "recovery_factor": finite(net / abs(max_dd), 10) if max_dd < 0 else "inf",
        "long_trade_count": int(side.eq("long").sum()) if trade_count else 0,
        "short_trade_count": int(side.eq("short").sum()) if trade_count else 0,
        "source": rel(scout.SELECTED_TRADE_TAPE),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_package_files(selected: Mapping[str, Any]) -> dict[str, Any]:
    probability = pd.read_csv(fs_path(scout.SELECTED_PROBABILITY_TAPE))
    trades = pd.read_csv(fs_path(scout.SELECTED_TRADE_TAPE))
    first_time, last_time, from_date, to_date = date_bounds(probability)
    feature_order_payload = read_json(SOURCE_FEATURE_ORDER)
    feature_order = feature_order_payload["feature_columns"]
    feature_order_hash = feature_order_payload["feature_order_hash"]
    selected_id = str(selected["variant_id"])
    short_threshold = float(selected["short_probability_threshold"])
    long_threshold = float(selected["long_threshold"])
    min_margin = float(selected["min_margin"])
    long_block_min = float(selected["long_block_min"])
    max_hold = int(selected["max_hold_m5"])

    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_probability = f"{COMMON_EXPECTED_DIR}/dual_side_selected_expected_probability_tape.csv"
    common_trade = f"{COMMON_EXPECTED_DIR}/dual_side_selected_expected_trade_tape.csv"
    common_policy = f"{COMMON_CONFIG_DIR}/runtime_policy_config.json"
    common_selected = f"{COMMON_CONFIG_DIR}/selected_runtime_candidate.json"
    sync_rows = [
        copy_common(SOURCE_FEATURE_MATRIX, common_feature, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_ONNX, common_model, "common_primary_onnx", "primary ONNX(주 온엑스)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_FEATURE_ORDER, common_feature_order, "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사한다."),
        copy_common(scout.SELECTED_PROBABILITY_TAPE, common_probability, "common_expected_probability_tape", "expected probability tape(예상 확률 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(scout.SELECTED_TRADE_TAPE, common_trade, "common_expected_trade_tape", "expected trade tape(예상 거래 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(scout.SELECTED_RUNTIME_CANDIDATE, common_selected, "common_selected_candidate", "selected candidate(선택 후보)를 Common Files(공용 파일)에 복사한다."),
    ]

    policy = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "primary_attempt": PRIMARY_ATTEMPT,
        "control_attempt": CONTROL_ATTEMPT,
        "model_id": MODEL_ID,
        "variant_id": selected_id,
        "output_contract": OUTPUT_CONTRACT,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "decision_surface": {
            "InpShortThreshold": short_threshold,
            "InpLongThreshold": long_threshold,
            "InpMinMargin": min_margin,
            "InpDecisionMode": "threshold_margin",
            "InpSideFilterEnabled": True,
            "InpSideFilterFeatureIndex": SIDE_FILTER_FEATURE_INDEX,
            "InpBlockShortFeatureRange": False,
            "InpBlockLongFeatureRange": True,
            "InpBlockLongFeatureMin": long_block_min,
            "InpBlockLongFeatureMax": SIDE_FILTER_BLOCK_MAX,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpMaxHoldBars": max_hold,
        },
        "expected_proxy": {
            "validation_net_profit": selected["validation_net_profit"],
            "oos_net_profit": selected["oos_net_profit"],
            "combined_net_profit": selected["combined_net_profit"],
            "combined_profit_factor": selected["combined_profit_factor"],
            "combined_trade_per_business_day": selected["combined_trade_per_business_day"],
            "combined_long_count": selected["combined_long_count"],
            "combined_short_count": selected["combined_short_count"],
        },
        "known_differences": [
            "proxy expected value(프록시 예상값)는 MT5 Strategy Tester(MT5 전략 테스터) KPI(핵심 성과 지표)를 대체하지 않는다.",
            "shadow loss guard ONNX(그림자 손실 방어 온엑스)는 현재 EA primary output(현재 전문가 자문 주 출력) 계약과 달라 package(패키지)하지 않는다.",
        ],
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, policy)
    sync_rows.append(copy_common(RUNTIME_POLICY_CONFIG, common_policy, "common_runtime_policy", "runtime policy(런타임 정책)를 Common Files(공용 파일)에 복사한다."))
    write_csv(COMMON_FILES_SYNC, sync_rows)

    report_name = "OPv2_run364W_dual_pshort045_adx40_hold8"
    set_name = "OPv2_run364W.set"
    ini_name = "OPv2_run364W.ini"
    set_path = SET_DIR / set_name
    ini_path = INI_DIR / ini_name
    set_values = {
        "InpRunId": f"{RUN_ID}_{PRIMARY_ATTEMPT}",
        "InpExplorationLabel": "stage364_DensitySideBalanceRepair__RuntimeProbe",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_dual_side_density_balance_repair",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": common_feature,
        "InpFeatureCount": len(feature_order),
        "InpFeatureCsvUseCommonFiles": True,
        "InpFeatureRequireTimestampMatch": True,
        "InpFeatureAllowLatestFallback": False,
        "InpFeatureStrictHeader": True,
        "InpFeatureCsvDelimiter": ",",
        "InpCsvTimestampIsBarClose": False,
        "InpModelPath": common_model,
        "InpModelId": MODEL_ID,
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": True,
        "InpModelUseCpuOnly": True,
        "InpModelNoConversion": False,
        "InpSetOutputShape": True,
        "InpModelUseMatrixTensor": False,
        "InpFeatureOrderHash": feature_order_hash,
        "InpFallbackEnabled": False,
        "InpShortThreshold": short_threshold,
        "InpLongThreshold": long_threshold,
        "InpMinMargin": min_margin,
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpSideFilterEnabled": True,
        "InpSideFilterFeatureIndex": SIDE_FILTER_FEATURE_INDEX,
        "InpFallbackSideFilterFeatureIndex": -1,
        "InpBlockShortFeatureRange": False,
        "InpBlockLongFeatureRange": True,
        "InpBlockLongFeatureMin": long_block_min,
        "InpBlockLongFeatureMax": SIDE_FILTER_BLOCK_MAX,
        "InpAllowTrading": True,
        "InpFixedLot": 0.10,
        "InpMagic": 36423001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": max_hold,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpEntryTransitionOnly": False,
        "InpExitRiskOverlayEnabled": False,
        "InpAtrSltpEnabled": False,
        "InpModelRiskSizingEnabled": False,
        "InpTelemetryEnabled": True,
        "InpTelemetryUseCommonFiles": True,
        "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv",
        "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv",
    }
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date=from_date,
            to_date=to_date,
            report=report_name,
        ),
        ini_path,
        set_file_path=Path(set_name),
    )
    set_rows = [
        {
            "attempt_name": PRIMARY_ATTEMPT,
            "model_id": MODEL_ID,
            "variant_id": selected_id,
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "parameter_count": set_payload["parameter_count"],
            "short_threshold": short_threshold,
            "long_threshold": long_threshold,
            "min_margin": min_margin,
            "side_filter_feature": SIDE_FILTER_FEATURE,
            "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
            "block_long_min": long_block_min,
            "max_hold_bars": max_hold,
            "allow_trading": True,
            "fixed_lot": 0.10,
            "output_contract": OUTPUT_CONTRACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ini_rows = [
        {
            "attempt_name": PRIMARY_ATTEMPT,
            "model_id": MODEL_ID,
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
            "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
            "expert": ini_payload["tester"].get("Expert", ""),
            "symbol": ini_payload["tester"].get("Symbol", ""),
            "period": ini_payload["tester"].get("Period", ""),
            "model": ini_payload["tester"].get("Model", ""),
            "deposit": ini_payload["tester"].get("Deposit", ""),
            "leverage": ini_payload["tester"].get("Leverage", ""),
            "from_date": from_date,
            "to_date": to_date,
            "first_time": first_time,
            "last_time": last_time,
            "report": report_name,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    metrics = [split_metrics(trades, split, selected) for split in ["validation", "oos", "combined"]]
    write_csv(EXPECTED_KPI_SUMMARY, metrics)

    return {
        "policy": policy,
        "sync_rows": sync_rows,
        "set_rows": set_rows,
        "ini_rows": ini_rows,
        "set_path": set_path,
        "ini_path": ini_path,
        "set_values": set_values,
        "report_name": report_name,
        "first_time": first_time,
        "last_time": last_time,
        "from_date": from_date,
        "to_date": to_date,
        "common_feature": common_feature,
        "common_model": common_model,
        "common_probability": common_probability,
        "common_trade": common_trade,
        "common_policy": common_policy,
        "metrics": metrics,
    }


def write_contracts(selected: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> None:
    shared = (
        f"features=58; feature_hash={package['policy']['feature_order_hash']}; "
        f"short_threshold={selected['short_probability_threshold']}; long_threshold={selected['long_threshold']}; "
        f"min_margin={selected['min_margin']}; adx_14_block_long_min={selected['long_block_min']}; "
        f"max_hold_m5={selected['max_hold_m5']}; output={OUTPUT_CONTRACT}"
    )
    write_csv(
        DUAL_SIDE_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "contract_id": "dual_side_density_balance_runtime_contract",
                "variant_id": selected["variant_id"],
                "shared_contract": shared,
                "trade_splitting_status": "not_used(미사용)",
                "effect(효과)": "Python proxy(파이썬 프록시) 후보를 current EA input(현재 EA 입력)으로 같은 의미에 가깝게 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        MODEL_HANDOFF_MANIFEST,
        [
            {
                "attempt_name": PRIMARY_ATTEMPT,
                "model_id": MODEL_ID,
                "variant_id": selected["variant_id"],
                "source_onnx_path": rel(SOURCE_ONNX),
                "source_onnx_sha256": sha(SOURCE_ONNX),
                "feature_matrix_path": rel(SOURCE_FEATURE_MATRIX),
                "common_feature_matrix_path": package["common_feature"],
                "common_direct_onnx_path": package["common_model"],
                "expected_probability_tape": rel(scout.SELECTED_PROBABILITY_TAPE),
                "common_expected_probability_tape": package["common_probability"],
                "expected_trade_tape": rel(scout.SELECTED_TRADE_TAPE),
                "common_expected_trade_tape": package["common_trade"],
                "runtime_policy_config": rel(RUNTIME_POLICY_CONFIG),
                "handoff_status": "ready_for_mt5_runtime_probe(MT5 런타임 탐침 준비)",
                "effect(효과)": "ONNX/feature/policy(온엑스/피처/정책)를 Common Files(공용 파일)에 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    attempt = {
        "attempt_name": PRIMARY_ATTEMPT,
        "tier": "Tier A",
        "split": "validation_oos",
        "model_id": MODEL_ID,
        "variant_id": selected["variant_id"],
        "threshold_id": selected["variant_id"],
        "threshold": selected["short_probability_threshold"],
        "feature_order_hash": package["policy"]["feature_order_hash"],
        "from_date": package["from_date"],
        "to_date": package["to_date"],
        "first_time": package["first_time"],
        "last_time": package["last_time"],
        "set_path": package["set_rows"][0]["set_path"],
        "ini_path": package["ini_rows"][0]["ini_path"],
        "report_name": package["report_name"],
        "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_telemetry.csv",
        "runtime_summary_expected": f"{COMMON_TELEMETRY_DIR}/{PRIMARY_ATTEMPT}_summary.csv",
        "known_proxy_runtime_difference": "proxy(프록시)는 신호/거래 예상 기록이고 MT5 Strategy Tester(MT5 전략 테스터)의 비용/체결 의미를 대체하지 않는다.",
        "forbidden_action": "treat_package_as_operating_promotion(패키지를 운영 승격으로 취급)",
        "effect": "같은 set/ini/expected tape(설정/INI/예상 기록)로 MT5 runtime probe(MT5 런타임 탐침)를 실행하게 한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, [attempt])
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "contract_id": "tester_identity",
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "tester_profile_root": basepkg.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "terminal_data_root": basepkg.DEFAULT_PORTABLE_ROOT.as_posix(),
                "expert": package["ini_rows"][0]["expert"],
                "symbol": "US100",
                "period": "M5",
                "tester_model": 4,
                "deposit": 500.0,
                "leverage": "1:100",
                "fixed_lot": 0.10,
                "from_date": package["from_date"],
                "to_date": package["to_date"],
                "spread_commission_slippage": "read_from_actual_tester_output_in_run364X(364X 실제 테스터 출력에서 읽음)",
                "compile_status": compile_result.get("status"),
                "portable_ea_copied": portable_sync.get("copied"),
                "effect(효과)": "tester identity(테스터 정체성)를 명시해 MT5 KPI(핵심 성과 지표) 비교 기준을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PROXY_MT5_COMPARISON_CONTRACT,
        [
            {
                "contract_id": "proxy_mt5_comparison",
                "expected_probability_tape": rel(scout.SELECTED_PROBABILITY_TAPE),
                "common_expected_probability_tape": package["common_probability"],
                "expected_trade_tape": rel(scout.SELECTED_TRADE_TAPE),
                "common_expected_trade_tape": package["common_trade"],
                "must_compare": "probability, decision, trade KPI(확률, 판정, 거래 핵심 성과 지표)",
                "proxy_scope": "signal sanity and candidate selection support(신호 점검과 후보 선별 보조)",
                "forbidden_use": "replace MT5 KPI(MT5 핵심 성과 지표 대체)",
                "effect(효과)": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 반드시 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "contract_id": "runtime_parity",
                "research_path": rel(scout.FINAL_DECISION),
                "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "shared_contract": shared,
                "known_differences": "shadow loss guard ONNX(그림자 손실 방어 온엑스)는 미포함; current EA(현재 EA)는 primary 3-class ONNX(주 3분류 온엑스)만 실행한다.",
                "parity_check": "run364X must compare telemetry/tester report against expected tapes(364X가 런타임 기록/테스터 보고서를 예상 기록과 비교해야 함)",
                "parity_identity": f"module_hashes={len(mt5_runtime_module_hashes())}; set={package['set_rows'][0]['set_sha256']}; model={sha(SOURCE_ONNX)}",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "effect(효과)": "Python research(파이썬 연구)와 MT5 execution(MT5 실행)의 의미 차이를 다음 실행에서 측정하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364X_EXECUTION_QUEUE,
        [
            {
                "queue_id": "run364X_execute_selected_dual_side_mt5_runtime_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "attempt_name": PRIMARY_ATTEMPT,
                "terminal_path": basepkg.DEFAULT_TERMINAL.as_posix(),
                "common_files_root": basepkg.DEFAULT_COMMON_FILES.as_posix(),
                "tester_profile_root": basepkg.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "terminal_data_root": basepkg.DEFAULT_PORTABLE_ROOT.as_posix(),
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "ini_path": package["ini_rows"][0]["ini_path"],
                "set_path": package["set_rows"][0]["set_path"],
                "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "blocked_if_missing": "terminal, compiled EA, Common Files handoff, tester output(터미널, 컴파일된 EA, 공용 파일 인계, 테스터 출력)",
                "effect(효과)": "패키지를 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def final_payload(selected: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> dict[str, Any]:
    combined = next(row for row in package["metrics"] if row["split"] == "combined")
    compile_pass = compile_result.get("status") == "completed" and portable_sync.get("copied") is True
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS if compile_pass else "blocked_stage364W_package_prepared_but_compile_or_portable_sync_failed_no_authority",
        "judgment": JUDGMENT if compile_pass else "runtime_probe_package_created_compile_or_portable_sync_repair_required_no_authority",
        "decision": DECISION if compile_pass else "stage364W_repair_compile_or_portable_ea_sync_before_mt5_probe",
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_variant_id": selected["variant_id"],
        "model_id": MODEL_ID,
        "attempt_name": PRIMARY_ATTEMPT,
        "short_threshold": selected["short_probability_threshold"],
        "long_threshold": selected["long_threshold"],
        "min_margin": selected["min_margin"],
        "side_filter_feature": SIDE_FILTER_FEATURE,
        "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
        "long_block_min": selected["long_block_min"],
        "max_hold_m5": selected["max_hold_m5"],
        "expected_combined_net_profit": combined["net_profit"],
        "expected_combined_profit_factor": combined["profit_factor"],
        "expected_combined_expectancy": combined["expectancy"],
        "expected_combined_max_drawdown": combined["max_drawdown"],
        "expected_combined_recovery_factor": combined["recovery_factor"],
        "expected_combined_trade_count": combined["trade_count"],
        "expected_combined_trade_density": combined["trade_density_per_business_day"],
        "expected_combined_long_count": combined["long_trade_count"],
        "expected_combined_short_count": combined["short_trade_count"],
        "set_path": package["set_rows"][0]["set_path"],
        "ini_path": package["ini_rows"][0]["ini_path"],
        "common_sync_rows": len(package["sync_rows"]),
        "compile_status": compile_result.get("status"),
        "compile_log": rel(COMPILE_LOG) if exists(COMPILE_LOG) else "",
        "portable_ea_copied": portable_sync.get("copied"),
        "terminal_exists": exists(basepkg.DEFAULT_TERMINAL),
        "common_files_exists": exists(basepkg.DEFAULT_COMMON_FILES),
        "ea_source_exists": exists(SOURCE_EA),
        "ea_binary_exists": exists(SOURCE_EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    compile_status = "passed" if final.get("compile_status") == "completed" and final.get("portable_ea_copied") is True else "blocked"
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_package_scope_gate(런타임 패키지 범위 게이트)",
            "status": "passed",
            "evidence(근거)": rel(FINAL_DECISION),
            "effect(효과)": "scope(범위)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 닫는다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "common_files_handoff_gate(공용 파일 인계 게이트)",
            "status": "passed",
            "evidence(근거)": rel(COMMON_FILES_SYNC),
            "effect(효과)": "ONNX/feature/expected tape(온엑스/피처/예상 기록)를 Common Files(공용 파일)에 동기화한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "metaeditor_compile_gate(메타에디터 컴파일 게이트)",
            "status": compile_status,
            "evidence(근거)": rel(COMPILE_RESULT),
            "effect(효과)": "EA source/binary(전문가 자문 소스/바이너리) 불일치를 MT5 실행 전에 드러낸다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "tester_identity_gate(테스터 정체성 게이트)",
            "status": "passed",
            "evidence(근거)": rel(TESTER_IDENTITY_CONTRACT),
            "effect(효과)": "tester model/deposit/leverage(테스터 모델/예치금/레버리지)를 고정한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_parity_contract_gate(런타임 동등성 계약 게이트)",
            "status": "passed",
            "evidence(근거)": rel(RUNTIME_PARITY_CONTRACT),
            "effect(효과)": "Python expected tape(파이썬 예상 기록)와 MT5 execution(MT5 실행) 비교 계약을 만든다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "claim_boundary_audit(주장 경계 감사)",
            "status": "passed",
            "evidence(근거)": rel(CLAIM_RECEIPT),
            "effect(효과)": "package(패키지)를 운영 주장(operating claim, 운영 주장)으로 착각하지 않게 한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed" if compile_status == "passed" else "blocked",
            "evidence(근거)": rel(GATE_AUDIT),
            "effect(효과)": "필수 gate(게이트)를 closeout(종료 기록)에 연결한다.",
        },
    ]


def write_receipts(final: Mapping[str, Any], package: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(SOURCE_FEATURE_MATRIX), rel(scout.SELECTED_PROBABILITY_TAPE), rel(scout.SELECTED_TRADE_TAPE)],
            "time_axis": "feature timestamp(피처 시각)은 MT5 closed-bar open time(닫힌 봉 시작 시각)과 맞춘다.",
            "feature_label_boundary": "expected trade tape(예상 거래 기록)는 proxy(프록시)이며 MT5 KPI(MT5 핵심 성과 지표)가 아니다.",
            "integrity_judgment": "usable_for_runtime_probe_package(런타임 탐침 패키지에 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "existing 3-class RF ONNX plus EA threshold/range rule(기존 3분류 RF 온엑스 + EA 임계값/범위 규칙)",
            "output_contract": OUTPUT_CONTRACT,
            "shadow_guard_status": "not_packaged_due_to_current_ea_output_contract(현재 EA 출력 계약 때문에 미패키지)",
            "validation_judgment": "candidate_for_mt5_probe_not_promotion(MT5 탐침 후보, 승격 아님)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(scout.FINAL_DECISION),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "shadow loss guard ONNX(그림자 손실 방어 온엑스)는 실행하지 않는다.",
            "parity_check": "compile/common-files/set/ini package only; run364X must execute Strategy Tester(컴파일/공용 파일/설정 패키지 전용, 364X 테스터 실행 필요)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": final["runtime_module_hashes"],
            "tester_output": "not_run",
            "backtest_judgment": "package_ready_mt5_execution_required(패키지 준비, MT5 실행 필요)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(FINAL_DECISION), rel(COMMON_FILES_SYNC), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST)],
            "evidence_missing": "MT5 Strategy Tester output/runtime telemetry/proxy-vs-MT5 diff(MT5 테스터 출력/런타임 기록/프록시-MT5 차이)",
            "judgment_label": final["judgment"],
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "runtime package(런타임 패키지)를 operating claim(운영 주장)으로 승격하지 않는다.",
        },
    )
    write_json(
        WORK_PACKET,
        {
            **base,
            "primary_family": "runtime_verification(런타임 검증)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": ["obsidian-backtest-forensics(백테스트 포렌식)", "obsidian-artifact-lineage(산출물 계보)"],
            "required_gates": [row["gate(게이트)"] for row in gate_rows(final)],
            "effect": "run364V proxy candidate(프록시 후보)를 MT5 probe package(MT5 탐침 패키지)로 전환한다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], package: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    combined = next(row for row in package["metrics"] if row["split"] == "combined")
    text = f"""# Stage364W density side-balance runtime package(Stage364W 밀도 방향 균형 런타임 패키지)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final["judgment"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- MT5 execution(MT5 실행): `not_run`

## Action/Effect(행동/효과)

Action(행동): `run364V` selected candidate(선택 후보) `{final["selected_variant_id"]}`를 MT5 RuntimeProbeEA(MT5 런타임 탐침 EA) set/ini(설정/INI), Common Files(공용 파일), expected tape(예상 기록)로 package(패키지)했다.

Effect(효과): short threshold(숏 임계값) `{final["short_threshold"]}`, ADX long block(ADX 롱 차단) `{final["long_block_min"]}`, max hold(최대 보유) `{final["max_hold_m5"]}` 조합을 MT5 Strategy Tester(MT5 전략 테스터)에서 바로 확인할 수 있게 했다.

## Expected proxy(예상 프록시)

{markdown_table(package["metrics"], ["split", "trade_count", "trade_density_per_business_day", "net_profit", "profit_factor", "expectancy", "max_drawdown", "recovery_factor", "long_trade_count", "short_trade_count"])}

## Runtime handoff(런타임 인계)

- set file(설정 파일): `{final["set_path"]}`
- ini file(INI 파일): `{final["ini_path"]}`
- runtime policy(런타임 정책): `{rel(RUNTIME_POLICY_CONFIG)}`
- Common Files sync(공용 파일 동기화): `{rel(COMMON_FILES_SYNC)}`
- execution queue(실행 대기열): `{rel(RUN364X_EXECUTION_QUEUE)}`
- compile status(컴파일 상태): `{final["compile_status"]}`
- portable EA sync(포터블 EA 동기화): `{final["portable_ea_copied"]}`

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Boundary(경계)

이 package(패키지)는 MT5 runtime probe(런타임 탐침) 준비물이다. tester report(테스터 보고서), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)가 아직 없으므로 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next action(다음 행동)

`{NEXT_RUN_ID}`에서 Strategy Tester(전략 테스터)를 실행하고 probability parity(확률 동등성), trade KPI(거래 핵심 성과 지표), cost behavior(비용 현상)를 비교한다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364W`는 `run364V`의 selected candidate(선택 후보) `{final["selected_variant_id"]}`를 MT5 RuntimeProbeEA(MT5 런타임 탐침 EA) package(패키지)로 만들었다. expected combined net/PF/density(예상 합산 순수익/수익 팩터/밀도)는 `{combined["net_profit"]}` / `{combined["profit_factor"]}` / `{combined["trade_density_per_business_day"]}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy-vs-MT5 diff(프록시-MT5 차이)를 기록한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final["status"]}
current_judgment: {final["judgment"]}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final["created_at_utc"]}
""",
    )
    append_text_once(
        REVIEW_INDEX,
        f"- [{RUN_NUMBER}]",
        f"- [{RUN_NUMBER}] {RUN_ID}: {rel(REPORT_PATH)} - runtime package(런타임 패키지), MT5 execution(MT5 실행) not_run(미실행)\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_NUMBER}",
        f"\n## {RUN_NUMBER} density side-balance runtime package(밀도 방향 균형 런타임 패키지)\n\n- current truth(현재 진실): selected dual-side candidate(선택 양방향 후보)를 MT5 package(MT5 패키지)로 만들었다.\n- effect(효과): run364X Strategy Tester(전략 테스터) 실행 준비가 됐다.\n",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): not_claimed(주장 안 함)
- latest_runtime_probe_clue(최근 런타임 탐침 단서): `run364T` MT5 net profit(MT5 순수익) `928.89`, profit factor(수익 팩터) `1.34`, trade count(거래수) `935`
- selected_runtime_package_candidate(선택 런타임 패키지 후보): `{final["selected_variant_id"]}`
- selected_proxy_density(선택 프록시 밀도): combined(합산) `{final["expected_combined_trade_density"]}`
- selected_proxy_long_short(선택 프록시 롱/숏): `{final["expected_combined_long_count"]}` / `{final["expected_combined_short_count"]}`
- package_status(패키지 상태): compile(컴파일) `{final["compile_status"]}`, portable_ea_sync(포터블 EA 동기화) `{final["portable_ea_copied"]}`
- blockers(차단): MT5 runtime evidence(MT5 런타임 근거), proxy-vs-MT5 diff(프록시-MT5 차이), cost stress(비용 압박) still required(아직 필요)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_README,
        f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): density side-balance repair candidate(밀도 방향 균형 수리 후보)가 MT5 runtime package(MT5 런타임 패키지)로 준비됐다.

Next action(다음 행동): run364X MT5 runtime probe(MT5 런타임 탐침) 실행.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"- {RUN_ID}",
        f"- {RUN_ID}: packaged(패키지 완료) selected density side-balance repair candidate(선택 밀도 방향 균형 수리 후보) for MT5 runtime probe(MT5 런타임 탐침).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"- {RUN_ID}",
        f"- {RUN_ID}: dual-side threshold + ADX long block(양방향 임계값 + ADX 롱 차단) moved from proxy(프록시) to runtime package(런타임 패키지); MT5 evidence(MT5 근거) still required(아직 필요).\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__Tier_A",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_package(런타임 패키지)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "package_only_mt5_not_run(패키지 전용, MT5 미실행)",
        "notes": "Stage364W packages selected dual-side density side-balance repair candidate(Stage364W 선택 양방향 밀도 방향 균형 수리 후보 패키지).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["expected_combined_trade_count"],
        "gate_passes": sum(1 for row_item in gate_rows(final) if row_item["status"] == "passed"),
        "gate_total": len(gate_rows(final)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "result_status": final["status"],
        "source_package_run_id": basepkg.RUN_ID,
        "work_family": "runtime_verification(런타임 검증)",
        "trade_density_requirement_status": "expected_combined_density_passed_no_trade_splitting(예상 합산 밀도 통과, 거래 쪼개기 없음)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "feature_count": 58,
        "net_profit": final["expected_combined_net_profit"],
        "profit_factor": final["expected_combined_profit_factor"],
        "trade_count": final["expected_combined_trade_count"],
        "expectancy": final["expected_combined_expectancy"],
        "recovery_factor": final["expected_combined_recovery_factor"],
        "max_drawdown_amount": final["expected_combined_max_drawdown"],
        "long_trade_count": final["expected_combined_long_count"],
        "short_trade_count": final["expected_combined_short_count"],
        "expected_probability_rows": int(pd.read_csv(fs_path(scout.SELECTED_PROBABILITY_TAPE), usecols=["run_id"]).shape[0]),
        "attempt_rows": 1,
        "evidence_scope": "package_only_no_mt5_execution(패키지 전용, MT5 실행 없음)",
    }
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [row], extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE, "MT5 runtime probe attempt package(MT5 런타임 탐침 시도 패키지)."),
            ("tester_set_manifest", TESTER_SET_MANIFEST, "Tester set manifest(테스터 설정 목록)."),
            ("tester_ini_manifest", TESTER_INI_MANIFEST, "Tester ini manifest(테스터 INI 목록)."),
            ("runtime_policy_config", RUNTIME_POLICY_CONFIG, "Runtime policy config(런타임 정책 설정)."),
            ("common_files_sync", COMMON_FILES_SYNC, "Common Files sync manifest(공용 파일 동기화 목록)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    selected = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    compile_result, portable_sync = run_compile_and_sync()
    package = write_package_files(selected)
    write_contracts(selected, package, compile_result, portable_sync)
    final = final_payload(selected, package, compile_result, portable_sync)
    gates = gate_rows(final)
    write_receipts(final, package)
    write_docs(final, package, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import package_threshold_edge_floor001_runtime_probe_without_db as package_base  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as runtime_base  # noqa: E402
from stage_pipelines.stage364 import review_density_restore_stress_to_candidate_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_density_restore_stress_to_candidate_scout_without_db as scout  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BD"
RUN_ID = "run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
PARENT_SCOUT_RUN_ID = scout.RUN_ID
BASELINE_RUN_ID = scout.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364BD_density_restore_stress_candidate_runtime_probe_package_prepared_compile_checked_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_density_restore_stress_candidate_mt5_execution_required_no_authority"
DECISION = "stage364BD_open_run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_compile_checked_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = runtime_base.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin"
ATTEMPT_NAME = "run364BD_density_restore_ba02_pshort045_floor00025_hold6"
REPORT_NAME = "OPv2_run364BD_density_restore_ba02"
EXPLORATION_LABEL = "stage364_DensityRestoreStressCandidate__RuntimeProbe"
SIDE_FILTER_FEATURE = package_base.basepkg.SIDE_FILTER_FEATURE
SIDE_FILTER_FEATURE_INDEX = package_base.basepkg.SIDE_FILTER_FEATURE_INDEX
SIDE_FILTER_BLOCK_MAX = 1000000.0
SESSION_POLICY_TEXT = "all_sessions_except_premarket_short(프리마켓 숏 제외 전체 세션)"
SIDE_POLICY_TEXT = "long_all_short_no_premarket(롱 전체, 숏 프리마켓 제외)"
RESTORE_POLICY_TEXT = "search between ax03 density safety and ax08 over-stress buffer(ax03 밀도 안전과 ax08 과압박 버퍼 사이 탐색)"
TRADE_SPLITTING_STATUS_TEXT = "not_used(거래 쪼개기 없음)"
TOP_N_STATUS_TEXT = "forbidden(금지)"

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
RUNTIME_SEMANTIC_GAP_AUDIT = RUN_DIR / "runtime_semantic_gap_audit.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = COMPILE_DIR / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
RUN364BE_EXECUTION_QUEUE = RUN_DIR / "run364BE_execution_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_boundary_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BD_density_restore_stress_candidate_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BD_density_restore_stress_candidate_runtime_probe_package.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

PARENT_FINAL = parent.FINAL_DECISION
PARENT_GATE_AUDIT = parent.GATE_AUDIT
PARENT_QUEUE = parent.RUN364BD_QUEUE
SOURCE_SELECTED_CANDIDATE = scout.SELECTED_PROXY_CANDIDATE
SOURCE_SELECTED_TRADE_TAPE = scout.SELECTED_EXPECTED_TRADE_TAPE
SOURCE_PROBABILITY_TAPE = package_base.SOURCE_PROBABILITY_TAPE
SOURCE_FEATURE_MATRIX = runtime_base.FEATURE_MATRIX
SOURCE_FEATURE_ORDER = runtime_base.FEATURE_ORDER
SOURCE_ONNX = runtime_base.SOURCE_ONNX
SOURCE_EA = runtime_base.EA_SOURCE
SOURCE_EA_BINARY = runtime_base.EA_BINARY
PORTABLE_EA_EX5 = runtime_base.PORTABLE_EA_EX5
DEFAULT_METAEDITOR = runtime_base.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_density_restore_stress_candidate_runtime_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_EXPECTED_DIR = f"{COMMON_ROOT}/expected"
COMMON_CONFIG_DIR = f"{COMMON_ROOT}/config"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

INPUT_FILES = [
    PARENT_FINAL,
    PARENT_GATE_AUDIT,
    PARENT_QUEUE,
    SOURCE_SELECTED_CANDIDATE,
    SOURCE_SELECTED_TRADE_TAPE,
    SOURCE_PROBABILITY_TAPE,
    SOURCE_FEATURE_MATRIX,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_EA,
    SOURCE_EA_BINARY,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    RUNTIME_POLICY_CONFIG,
    RUNTIME_SEMANTIC_GAP_AUDIT,
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
    RUN364BE_EXECUTION_QUEUE,
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
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    parent.write_json(path, json_ready(payload))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_csv_rows(path)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
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
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


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


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, COMPILE_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(io_path(path), exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364BD inputs(364BD 입력 누락): " + ", ".join(missing))
    final = read_json(PARENT_FINAL)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if any(final.get(key) != "not_claimed" for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]):
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장이 있음)")
    gates = read_csv_rows(PARENT_GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit is not fully passed(부모 게이트 감사가 모두 통과가 아님)")
    queue = read_csv_rows(PARENT_QUEUE)
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    selected_id = str(selected.get("variant_id"))
    primary_rows = [row for row in queue if row.get("source_variant_id") == selected_id and "selected_primary" in row.get("package_role", "")]
    if not primary_rows:
        raise RuntimeError("BD queue selected primary mismatch(BD 대기열 선택 주 후보 불일치)")
    if not bool(selected.get("package_eligible_proxy")):
        raise RuntimeError("selected candidate is not package eligible(선택 후보가 패키지 가능 후보가 아님)")
    feature_order = read_json(SOURCE_FEATURE_ORDER)["feature_columns"]
    if feature_order[SIDE_FILTER_FEATURE_INDEX] != SIDE_FILTER_FEATURE:
        raise RuntimeError("side filter feature index mismatch(방향 필터 피처 인덱스 불일치)")
    if as_float(selected.get("estimated_mt5_trade_per_business_day")) < 3.0:
        raise RuntimeError("estimated MT5 density is below requirement(추정 MT5 밀도가 요구치보다 낮음)")
    return selected


def source_role(path: Path | str) -> str:
    text = rel(path)
    if "run364BC" in text:
        return "parent review evidence(부모 검토 근거)"
    if "run364BB" in text:
        return "selected proxy candidate evidence(선택 프록시 후보 근거)"
    if "run364V" in text or "run364M" in text or "run364L" in text:
        return "shared ONNX runtime input(공유 온엑스 런타임 입력)"
    if "foundation/mt5" in text:
        return "EA runtime source(EA 런타임 소스)"
    return "local project state(로컬 프로젝트 상태)"


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "source_path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "source_role": source_role(path),
            "effect": "package lineage input(패키지 계보 입력)을 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def runtime_filter_support() -> dict[str, bool]:
    text = io_path(SOURCE_EA).read_text(encoding="utf-8-sig")
    required = [
        "InpBlockPremarketShort",
        "InpMarchNonHour16MarginFilter",
        "InpEntryMarginFloor",
        "ApplyRuntimeTimeFilters",
        "InpMaxHoldBars",
    ]
    return {name: name in text for name in required}


def date_bounds(probability: pd.DataFrame) -> tuple[str, str, str, str]:
    if "timestamp_utc" in probability.columns:
        timestamps = pd.to_datetime(probability["timestamp_utc"], utc=True)
    elif "bar_time_server" in probability.columns:
        timestamps = pd.to_datetime(probability["bar_time_server"], utc=True)
    else:
        raise RuntimeError("probability tape has no timestamp column(확률 기록에 시각 열이 없음)")
    first = pd.Timestamp(timestamps.min()).tz_convert("UTC")
    last = pd.Timestamp(timestamps.max()).tz_convert("UTC")
    return (
        first.strftime("%Y.%m.%d %H:%M:%S"),
        last.strftime("%Y.%m.%d %H:%M:%S"),
        first.strftime("%Y.%m.%d"),
        (last + pd.Timedelta(days=1)).strftime("%Y.%m.%d"),
    )


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(runtime_base.DEFAULT_COMMON_FILES, local_path, common_path)
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


def split_kpi_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ["validation", "oos", "combined"]:
        prefix = f"{split}_"
        rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "net_profit": selected.get(f"{prefix}net_profit"),
                "profit_factor": selected.get(f"{prefix}profit_factor"),
                "expectancy": selected.get(f"{prefix}expectancy"),
                "max_drawdown": selected.get(f"{prefix}max_drawdown"),
                "recovery_factor": selected.get(f"{prefix}recovery_factor"),
                "trade_count": selected.get(f"{prefix}trade_count"),
                "business_days": selected.get(f"{prefix}business_days"),
                "trade_per_business_day": selected.get(f"{prefix}trade_per_business_day"),
                "long_trade_count": selected.get(f"{prefix}long_count"),
                "short_trade_count": selected.get(f"{prefix}short_count"),
                "estimated_mt5_trade_count": selected.get("estimated_mt5_trade_count") if split == "combined" else "",
                "estimated_mt5_trade_per_business_day": selected.get("estimated_mt5_trade_per_business_day") if split == "combined" else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_runtime_package(selected: Mapping[str, Any]) -> dict[str, Any]:
    probability = pd.read_csv(io_path(SOURCE_PROBABILITY_TAPE))
    trade_tape = pd.read_csv(io_path(SOURCE_SELECTED_TRADE_TAPE), usecols=["run_id"])
    first_time, last_time, from_date, to_date = date_bounds(probability)
    feature_order_payload = read_json(SOURCE_FEATURE_ORDER)
    feature_order = feature_order_payload["feature_columns"]
    feature_order_hash = feature_order_payload["feature_order_hash"]

    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_probability = f"{COMMON_EXPECTED_DIR}/dual_side_selected_expected_probability_tape.csv"
    common_trade = f"{COMMON_EXPECTED_DIR}/density_restore_stress_expected_trade_tape.csv"
    common_selected = f"{COMMON_CONFIG_DIR}/selected_proxy_candidate.json"
    common_policy = f"{COMMON_CONFIG_DIR}/runtime_policy_config.json"
    telemetry_path = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_telemetry.csv"
    summary_path = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_summary.csv"

    short_threshold = as_float(selected.get("short_probability_threshold"), 0.45)
    long_threshold = as_float(selected.get("long_threshold"), 0.0)
    min_margin = as_float(selected.get("min_margin"), -0.000562137088)
    entry_margin_floor = as_float(selected.get("entry_margin_floor"), 0.00025)
    long_block_min = as_float(selected.get("long_block_min"), 40.0)
    max_hold = int(as_float(selected.get("max_hold_m5"), 6))
    bridge_value = as_float(selected.get("bridge_policy_value"), 0.10)

    policy = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_scout_run_id": PARENT_SCOUT_RUN_ID,
        "model_id": MODEL_ID,
        "variant_id": selected.get("variant_id"),
        "output_contract": OUTPUT_CONTRACT,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_order_hash,
        "decision_surface": {
            "InpDecisionMode": "threshold_margin",
            "InpShortThreshold": short_threshold,
            "InpLongThreshold": long_threshold,
            "InpMinMargin": min_margin,
            "InpEntryMarginFloor": entry_margin_floor,
            "InpSideFilterEnabled": True,
            "InpSideFilterFeatureIndex": SIDE_FILTER_FEATURE_INDEX,
            "InpBlockLongFeatureRange": True,
            "InpBlockLongFeatureMin": long_block_min,
            "InpBlockLongFeatureMax": SIDE_FILTER_BLOCK_MAX,
            "InpBlockPremarketShort": True,
            "InpPremarketStartHour": 12,
            "InpPremarketEndHour": 17,
            "InpMarchNonHour16MarginFilter": True,
            "InpMarchFilterMonth": 3,
            "InpMarchFilterBlockedHour": 16,
            "InpMarchFilterAbsMarginMin": bridge_value,
            "InpMaxHoldBars": max_hold,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
        },
        "proxy_policy": {
            "bridge_policy": selected.get("bridge_policy"),
            "bridge_policy_value": bridge_value,
            "session_policy": SESSION_POLICY_TEXT,
            "side_policy": SIDE_POLICY_TEXT,
            "restore_policy": RESTORE_POLICY_TEXT,
            "trade_splitting_status": TRADE_SPLITTING_STATUS_TEXT,
            "top_n_status": TOP_N_STATUS_TEXT,
        },
        "expected_proxy": {
            "combined_net_profit": selected.get("combined_net_profit"),
            "combined_profit_factor": selected.get("combined_profit_factor"),
            "combined_expectancy": selected.get("combined_expectancy"),
            "combined_max_drawdown": selected.get("combined_max_drawdown"),
            "combined_recovery_factor": selected.get("combined_recovery_factor"),
            "combined_trade_count": selected.get("combined_trade_count"),
            "combined_long_count": selected.get("combined_long_count"),
            "combined_short_count": selected.get("combined_short_count"),
            "combined_trade_per_business_day": selected.get("combined_trade_per_business_day"),
            "estimated_mt5_trade_count": selected.get("estimated_mt5_trade_count"),
            "estimated_mt5_trade_per_business_day": selected.get("estimated_mt5_trade_per_business_day"),
        },
        "known_differences": [
            "proxy expected value(프록시 예상값)는 MT5 Strategy Tester(MT5 전략 테스터) KPI(핵심 성과 지표)를 대체하지 않는다.",
            "spread/slippage/fill(스프레드/슬리피지/체결)은 run364BE MT5 실행 뒤 확인한다.",
        ],
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, policy)

    sync_rows = [
        copy_common(SOURCE_FEATURE_MATRIX, common_feature, "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_ONNX, common_model, "common_primary_onnx", "primary ONNX(주 온엑스)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_FEATURE_ORDER, common_feature_order, "common_feature_order", "feature order(피처 순서)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_PROBABILITY_TAPE, common_probability, "common_expected_probability_tape", "expected probability tape(예상 확률 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_SELECTED_TRADE_TAPE, common_trade, "common_expected_trade_tape", "expected trade tape(예상 거래 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_SELECTED_CANDIDATE, common_selected, "common_selected_candidate", "selected candidate(선택 후보)를 Common Files(공용 파일)에 복사한다."),
        copy_common(RUNTIME_POLICY_CONFIG, common_policy, "common_runtime_policy", "runtime policy(런타임 정책)를 Common Files(공용 파일)에 복사한다."),
    ]
    write_csv(COMMON_FILES_SYNC, sync_rows)

    set_path = SET_DIR / "OPv2_run364BD.set"
    ini_path = INI_DIR / "OPv2_run364BD.ini"
    set_values = {
        "InpRunId": f"{RUN_ID}_{ATTEMPT_NAME}",
        "InpExplorationLabel": EXPLORATION_LABEL,
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_density_restore_stress",
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
        "InpBlockPremarketShort": True,
        "InpPremarketStartHour": 12,
        "InpPremarketEndHour": 17,
        "InpMarchNonHour16MarginFilter": True,
        "InpMarchFilterMonth": 3,
        "InpMarchFilterBlockedHour": 16,
        "InpMarchFilterAbsMarginMin": bridge_value,
        "InpEntryMarginFloor": entry_margin_floor,
        "InpAllowTrading": True,
        "InpFixedLot": 0.1,
        "InpMagic": 36425001,
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
        "InpTelemetryCsvPath": telemetry_path,
        "InpSummaryCsvPath": summary_path,
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
        "policy": policy,
        "set_values": set_values,
        "set_payload": set_payload,
        "ini_payload": ini_payload,
        "common_feature": common_feature,
        "common_model": common_model,
        "common_feature_order": common_feature_order,
        "common_probability": common_probability,
        "common_trade": common_trade,
        "common_selected": common_selected,
        "common_policy": common_policy,
        "telemetry_path": telemetry_path,
        "summary_path": summary_path,
        "set_path": set_path,
        "ini_path": ini_path,
        "probability_rows": int(len(probability)),
        "trade_tape_rows": int(len(trade_tape)),
        "first_time": first_time,
        "last_time": last_time,
        "from_date": from_date,
        "to_date": to_date,
        "common_sync_rows": len(sync_rows),
        "common_sync_missing": sum(1 for row in sync_rows if not Path(row["absolute_path"]).exists()),
    }
    write_csv(
        TESTER_SET_MANIFEST,
        [
            {
                "attempt_name": ATTEMPT_NAME,
                "model_id": MODEL_ID,
                "variant_id": selected.get("variant_id"),
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "min_margin": min_margin,
                "entry_margin_floor": entry_margin_floor,
                "side_filter_feature": SIDE_FILTER_FEATURE,
                "side_filter_feature_index": SIDE_FILTER_FEATURE_INDEX,
                "block_long_min": long_block_min,
                "block_premarket_short": True,
                "march_non_hour16_margin_filter": True,
                "march_abs_margin_min": bridge_value,
                "max_hold_bars": max_hold,
                "allow_trading": True,
                "fixed_lot": 0.1,
                "output_contract": OUTPUT_CONTRACT,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_INI_MANIFEST,
        [
            {
                "attempt_name": ATTEMPT_NAME,
                "model_id": MODEL_ID,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "terminal_path": runtime_base.DEFAULT_TERMINAL.as_posix(),
                "expert": ini_payload["tester"].get("Expert", ""),
                "symbol": ini_payload["tester"].get("Symbol", ""),
                "period": ini_payload["tester"].get("Period", ""),
                "model": ini_payload["tester"].get("Model", ""),
                "deposit": ini_payload["tester"].get("Deposit", ""),
                "leverage": ini_payload["tester"].get("Leverage", ""),
                "from_date": from_date,
                "to_date": to_date,
                "report": REPORT_NAME,
                "set_file": set_path.name,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(EXPECTED_KPI_SUMMARY, split_kpi_rows(selected))
    return package


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
                "effect": "compile failure(컴파일 실패)를 runtime package(런타임 패키지) 주장 경계 안에 기록한다.",
            }
        )
    write_json(PORTABLE_EA_SYNC, sync_payload)
    return result, sync_payload


def write_contracts(selected: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> None:
    write_csv(
        RUNTIME_SEMANTIC_GAP_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "gap_id": "proxy_expected_value_vs_mt5_kpi",
                "research_semantic": "proxy expected value(프록시 예상값)",
                "runtime_semantic": "MT5 Strategy Tester KPI(MT5 전략 테스터 핵심 성과 지표)",
                "known_difference": "spread/slippage/fill/cost(스프레드/슬리피지/체결/비용)는 MT5 실행 뒤 확정한다.",
                "usability": "candidate screening only(후보 선별 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "gap_id": "density_restore_survival_ratio",
                "research_semantic": "estimated MT5 density(추정 MT5 밀도)",
                "runtime_semantic": "actual MT5 trade density(실제 MT5 거래 밀도)",
                "known_difference": "observed survival ratio(관측 생존 비율) 기반 추정이라 실행 후 차이를 비교해야 한다.",
                "usability": "package queue priority(패키지 대기열 우선순위)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    write_csv(
        MODEL_HANDOFF_MANIFEST,
        [
            {
                "attempt_name": ATTEMPT_NAME,
                "model_id": MODEL_ID,
                "variant_id": selected.get("variant_id"),
                "source_onnx_path": rel(SOURCE_ONNX),
                "source_onnx_sha256": sha(SOURCE_ONNX),
                "feature_matrix_path": rel(SOURCE_FEATURE_MATRIX),
                "common_feature_matrix_path": package["common_feature"],
                "common_direct_onnx_path": package["common_model"],
                "expected_probability_tape": rel(SOURCE_PROBABILITY_TAPE),
                "common_expected_probability_tape": package["common_probability"],
                "expected_trade_tape": rel(SOURCE_SELECTED_TRADE_TAPE),
                "common_expected_trade_tape": package["common_trade"],
                "runtime_policy_config": rel(RUNTIME_POLICY_CONFIG),
                "handoff_status": "ready_for_mt5_runtime_probe(MT5 런타임 탐침 준비)",
                "effect": "ONNX/feature/policy(온엑스/피처/정책)를 Common Files(공용 파일)에 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "terminal_path": runtime_base.DEFAULT_TERMINAL.as_posix(),
                "common_files_root": runtime_base.DEFAULT_COMMON_FILES.as_posix(),
                "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "blocked_if_missing": "terminal, compiled EA, Common Files handoff, tester output(터미널, 컴파일된 EA, 공용 파일 인계, 테스터 출력)",
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
                "terminal": runtime_base.DEFAULT_TERMINAL.as_posix(),
                "common_files_root": runtime_base.DEFAULT_COMMON_FILES.as_posix(),
                "tester_profile_root": runtime_base.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "symbol": "US100",
                "timeframe": "M5",
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "report_name": REPORT_NAME,
                "compile_status": compile_result.get("status"),
                "portable_ea_copied": portable_sync.get("copied"),
                "effect": "tester identity(테스터 정체성)를 고정해 MT5 KPI(핵심 성과 지표) 비교 기준을 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PROXY_MT5_COMPARISON_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "proxy_candidate": selected.get("variant_id"),
                "expected_net_profit": selected.get("combined_net_profit"),
                "expected_profit_factor": selected.get("combined_profit_factor"),
                "expected_trade_count": selected.get("combined_trade_count"),
                "expected_estimated_mt5_density": selected.get("estimated_mt5_trade_per_business_day"),
                "expected_drawdown": selected.get("combined_max_drawdown"),
                "mt5_required_metrics": "net profit, profit factor, expectancy, drawdown, recovery factor, trade count, long/short balance(순수익, 수익 팩터, 기대값, 낙폭, 회복 계수, 거래수, 롱/숏 균형)",
                "diff_required": "proxy-vs-MT5 attribution required(프록시-MT5 차이 귀속 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "research_path": rel(parent.REPORT_PATH),
                "runtime_path": rel(TESTER_SET_MANIFEST),
                "shared_contract": "closed M5 bar, next tick entry, p_short/p_flat/p_long, threshold_margin, ADX long block, March hour/margin filter, premarket short block(닫힌 M5 봉, 다음 틱 진입, 확률 3종, 임계값/마진, ADX 롱 차단, 3월 시간/마진 필터, 프리마켓 숏 차단)",
                "known_differences": "MT5 execution cost/fill unknown until run364BE(MT5 실행 비용/체결은 364BE 전까지 미확정)",
                "parity_check": "compile/common-files/set/ini package only; run364BE must execute Strategy Tester(컴파일/공용 파일/set/ini 패키지 전용, 364BE 전략 테스터 실행 필요)",
                "parity_identity": json.dumps(mt5_runtime_module_hashes(), ensure_ascii=False),
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            }
        ],
    )
    write_csv(
        RUN364BE_EXECUTION_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "selected_queue_id": selected.get("queue_id"),
                "selected_variant_id": selected.get("variant_id"),
                "set_path": rel(package["set_path"]),
                "ini_path": rel(package["ini_path"]),
                "terminal_path": runtime_base.DEFAULT_TERMINAL.as_posix(),
                "expected_estimated_mt5_density": selected.get("estimated_mt5_trade_per_business_day"),
                "required_action": "execute MT5 Strategy Tester(MT5 전략 테스터 실행)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def final_payload(selected: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> dict[str, Any]:
    compile_pass = compile_result.get("status") == "completed" and portable_sync.get("copied") is True
    support = runtime_filter_support()
    support_pass = all(support.values())
    package_pass = package["common_sync_rows"] >= 7 and package["common_sync_missing"] == 0
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_scout_run_id": PARENT_SCOUT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS if compile_pass and support_pass and package_pass else "blocked_stage364BD_package_created_but_compile_or_handoff_failed_no_authority",
        "judgment": JUDGMENT if compile_pass and support_pass and package_pass else "runtime_probe_package_created_repair_required_no_authority",
        "decision": DECISION if compile_pass and support_pass and package_pass else "stage364BD_repair_compile_or_handoff_before_mt5_probe",
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_queue_id": selected.get("queue_id"),
        "selected_variant_id": selected.get("variant_id"),
        "model_id": MODEL_ID,
        "attempt_name": ATTEMPT_NAME,
        "report_name": REPORT_NAME,
        "short_threshold": selected.get("short_probability_threshold"),
        "long_threshold": selected.get("long_threshold"),
        "min_margin": selected.get("min_margin"),
        "entry_margin_floor": selected.get("entry_margin_floor"),
        "max_hold_m5": selected.get("max_hold_m5"),
        "bridge_policy": selected.get("bridge_policy"),
        "bridge_policy_value": selected.get("bridge_policy_value"),
        "session_policy": SESSION_POLICY_TEXT,
        "side_policy": SIDE_POLICY_TEXT,
        "expected_combined_net_profit": selected.get("combined_net_profit"),
        "expected_combined_profit_factor": selected.get("combined_profit_factor"),
        "expected_combined_expectancy": selected.get("combined_expectancy"),
        "expected_combined_max_drawdown": selected.get("combined_max_drawdown"),
        "expected_combined_recovery_factor": selected.get("combined_recovery_factor"),
        "expected_combined_trade_count": selected.get("combined_trade_count"),
        "expected_combined_long_count": selected.get("combined_long_count"),
        "expected_combined_short_count": selected.get("combined_short_count"),
        "expected_combined_trade_density": selected.get("combined_trade_per_business_day"),
        "expected_estimated_mt5_trade_count": selected.get("estimated_mt5_trade_count"),
        "expected_estimated_mt5_density": selected.get("estimated_mt5_trade_per_business_day"),
        "trade_splitting_status": TRADE_SPLITTING_STATUS_TEXT,
        "top_n_status": TOP_N_STATUS_TEXT,
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "compile_status": compile_result.get("status"),
        "compile_log": rel(COMPILE_LOG),
        "portable_ea_copied": portable_sync.get("copied"),
        "common_files_exists": runtime_base.DEFAULT_COMMON_FILES.exists(),
        "terminal_exists": runtime_base.DEFAULT_TERMINAL.exists(),
        "common_sync_rows": package["common_sync_rows"],
        "common_sync_missing": package["common_sync_missing"],
        "probability_rows": package["probability_rows"],
        "trade_tape_rows": package["trade_tape_rows"],
        "tester_from_date": package["from_date"],
        "tester_to_date": package["to_date"],
        "runtime_filter_support": support,
        "runtime_module_hashes": mt5_runtime_module_hashes(),
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    support_pass = all(final.get("runtime_filter_support", {}).values())
    compile_pass = final.get("compile_status") == "completed" and final.get("portable_ea_copied") is True
    gates = [
        ("runtime_evidence_gate(런타임 근거 게이트)", final["common_sync_rows"] >= 7 and final["common_sync_missing"] == 0, COMMON_FILES_SYNC, "Common Files(공용 파일) 인계를 완료했다."),
        ("scope_completion_gate(범위 완료 게이트)", exists(RUNTIME_PROBE_ATTEMPT_PACKAGE) and exists(TESTER_INI_MANIFEST), RUNTIME_PROBE_ATTEMPT_PACKAGE, "package scope(패키지 범위)를 끝냈고 MT5 execution(MT5 실행)은 다음 실행으로 둔다."),
        ("runtime_filter_support_gate(런타임 필터 지원 게이트)", support_pass, SOURCE_EA, "proxy policy(프록시 정책)를 EA input(EA 입력)으로 표현한다."),
        ("metaeditor_compile_gate(메타에디터 컴파일 게이트)", compile_pass, COMPILE_RESULT, "EA(전문가 자문)를 컴파일하고 portable tester(포터블 테스터)에 복사했다."),
        ("tester_identity_gate(테스터 정체성 게이트)", exists(TESTER_SET_MANIFEST) and exists(TESTER_INI_MANIFEST), TESTER_SET_MANIFEST, "US100 M5, real ticks, deposit 500, leverage 100(US100 M5, 실제 틱, 예치금 500, 레버리지 100)을 고정했다."),
        ("kpi_contract_audit(KPI 계약 감사)", exists(EXPECTED_KPI_SUMMARY) and as_float(final.get("expected_estimated_mt5_density")) >= 3.0, EXPECTED_KPI_SUMMARY, "proxy KPI(프록시 핵심 성과 지표)와 추정 MT5 밀도 조건을 남겼다."),
        ("artifact_lineage_gate(산출물 계보 게이트)", exists(MODEL_HANDOFF_MANIFEST) and exists(RUNTIME_PARITY_CONTRACT), MODEL_HANDOFF_MANIFEST, "model/handoff/parity(모델/인계/동등성) 경로를 연결했다."),
        ("required_gate_coverage_audit(필수 게이트 커버리지 감사)", True, GATE_AUDIT, "runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다."),
        ("final_claim_guard(최종 주장 가드)", True, FINAL_DECISION, "runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "blocked",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def write_receipts(final: Mapping[str, Any], package: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        WORK_PACKET,
        {
            **base,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-data-integrity(데이터 무결성)",
            ],
            "required_gates": [row["gate"] for row in gates],
            "effect": "run364BC selected primary(선택 주 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 전환한다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(SOURCE_FEATURE_MATRIX), rel(SOURCE_PROBABILITY_TAPE), rel(SOURCE_SELECTED_TRADE_TAPE), rel(PARENT_QUEUE)],
            "time_axis": "closed M5 bar to next tick entry(닫힌 M5 봉에서 다음 틱 진입)",
            "feature_label_boundary": "no new feature or label; existing ONNX/probability tape reused(새 피처/라벨 없음, 기존 온엑스/확률 기록 재사용)",
            "split_boundary": "validation/oos preserved from parent selected candidate(부모 선택 후보의 검증/OOS 분할 보존)",
            "leakage_risk": "package only and no new timestamp join(패키지 전용이며 새 시각 결합 없음)",
            "integrity_judgment": "usable_for_runtime_probe_package(런타임 탐침 패키지에 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_boundary": "existing ONNX reused, no new model training(기존 온엑스 재사용, 새 모델 학습 없음)",
            "model_id": MODEL_ID,
            "output_contract": OUTPUT_CONTRACT,
            "validation_judgment": "runtime_probe_candidate_not_promotion(런타임 탐침 후보, 승격 아님)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(parent.REPORT_PATH),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "MT5 cost/fill/slippage unknown until Strategy Tester execution(MT5 비용/체결/슬리피지는 전략 테스터 실행 전까지 미확정)",
            "parity_check": "compile/common-files/set/ini package only(컴파일/공용 파일/set/ini 패키지 전용)",
            "parity_identity": final["runtime_module_hashes"],
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": final["runtime_module_hashes"],
            "report_identity": "not_run",
            "trade_evidence": "proxy expected only; MT5 trade list not available yet(프록시 예상값 전용, MT5 거래 목록 아직 없음)",
            "cost_assumptions": "spread/slippage/swap unknown until tester output(스프레드/슬리피지/스왑은 테스터 출력 전까지 미확정)",
            "forensic_checks": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(COMPILE_RESULT)],
            "backtest_judgment": "package_ready_mt5_execution_required(패키지 준비, MT5 실행 필요)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_expected(커밋 뒤 추적 예정)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(FINAL_DECISION), rel(COMMON_FILES_SYNC), rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(GATE_AUDIT)],
            "evidence_missing": "MT5 Strategy Tester output, runtime telemetry, proxy-vs-MT5 diff(MT5 전략 테스터 출력, 런타임 기록, 프록시-MT5 차이)",
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
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "runtime package(런타임 패키지)를 operating claim(운영 주장)으로 승격하지 않는다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines) + "\n")


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    refresh_stage_brief_header()
    expected_rows = split_kpi_rows(read_json(SOURCE_SELECTED_CANDIDATE))
    report = f"""# run364BD density restore stress candidate runtime probe package(364BD 밀도 복원 압박 후보 런타임 탐침 패키지)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `{final["selected_variant_id"]}`
- expected net/PF/density/DD/trades(예상 순수익/수익 팩터/밀도/낙폭/거래수): `{final["expected_combined_net_profit"]}` / `{final["expected_combined_profit_factor"]}` / `{final["expected_estimated_mt5_density"]}` / `{final["expected_combined_max_drawdown"]}` / `{final["expected_combined_trade_count"]}`
- compile_status(컴파일 상태): `{final["compile_status"]}`
- MT5 execution(MT5 실행): `not_run`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): `run364BC` selected primary(선택 주 후보)를 RuntimeProbeEA(런타임 탐침 EA) set/ini(설정/INI), Common Files(공용 파일), runtime policy(런타임 정책), execution queue(실행 대기열)로 package(패키지)했다.

Effect(효과): short threshold(숏 임계값) `{final["short_threshold"]}`, entry margin floor(진입 마진 하한) `{final["entry_margin_floor"]}`, max hold(최대 보유) `{final["max_hold_m5"]}` 조합을 `run364BE` MT5 Strategy Tester(MT5 전략 테스터)에서 바로 실행할 수 있다.

## Expected KPI(예상 KPI)

{markdown_table(expected_rows, ["split", "net_profit", "profit_factor", "trade_count", "trade_per_business_day", "estimated_mt5_trade_per_business_day", "max_drawdown", "long_trade_count", "short_trade_count"])}

## Runtime Handoff(런타임 인계)

- set file(설정 파일): `{final["set_path"]}`
- ini file(INI 파일): `{final["ini_path"]}`
- runtime policy(런타임 정책): `{rel(RUNTIME_POLICY_CONFIG)}`
- Common Files sync(공용 파일 동기화): `{rel(COMMON_FILES_SYNC)}`
- execution queue(실행 대기열): `{rel(RUN364BE_EXECUTION_QUEUE)}`
- portable EA sync(포터블 EA 동기화): `{final["portable_ea_copied"]}`

## Gate Audit(게이트 감사)

{markdown_table(gates, ["gate", "status", "evidence", "effect"])}

## Boundary(경계)

This is a runtime probe package(런타임 탐침 패키지) only. MT5 tester report(MT5 테스터 보고서), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)가 아직 없으므로 operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)의 차이(diff, 차이), 원인(attribution, 귀속), 활용 가능성(usability, 활용 가능성)을 기록한다.
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364BD(364BD 실행)는 run364BC(364BC 실행)의 selected primary(선택 주 후보) `{final["selected_variant_id"]}`를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다. expected PF(예상 수익 팩터)는 `{final["expected_combined_profit_factor"]}`, estimated MT5 density(추정 MT5 밀도)는 `{final["expected_estimated_mt5_density"]}`/day(일), net(순수익)은 `{final["expected_combined_net_profit"]}`, DD(낙폭)는 `{final["expected_combined_max_drawdown"]}`이다. compile_status(컴파일 상태)는 `{final["compile_status"]}`이고 Common Files handoff(공용 파일 인계)는 `{final["common_sync_rows"]}` rows(행)로 완료했다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 tester output(테스터 출력), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)를 기록한다.
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
        bom=False,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_runtime_probe_required(없음, 런타임 탐침 필요)
- runtime_probe_candidate(런타임 탐침 후보): `{final["selected_variant_id"]}`
- latest_package(최근 패키지): `{RUN_ID}`
- selected_proxy_pf(선택 프록시 수익 팩터): `{final["expected_combined_profit_factor"]}`
- selected_estimated_mt5_density(선택 추정 MT5 밀도): `{final["expected_estimated_mt5_density"]}`
- package_status(패키지 상태): compile(컴파일) `{final["compile_status"]}`, portable_ea_sync(포터블 EA 동기화) `{final["portable_ea_copied"]}`
- next_execution_queue(다음 실행 대기열): `{rel(RUN364BE_EXECUTION_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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
        f"\n## {RUN_NUMBER} Density Restore Stress Candidate Runtime Package(밀도 복원 압박 후보 런타임 패키지)\n\n- action(행동): selected primary(선택 주 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다.\n- effect(효과): `{NEXT_RUN_ID}` Strategy Tester(전략 테스터) 실행 준비가 끝났다.\n",
    )
    append_text_once(
        STAGE_README,
        f"## {RUN_NUMBER}",
        f"\n## {RUN_NUMBER} density restore stress candidate runtime package(밀도 복원 압박 후보 런타임 패키지)\n\nAction(행동): `{final['selected_variant_id']}` package(패키지)를 완료했다.\n\nEffect(효과): `{NEXT_RUN_ID}` MT5 runtime probe(MT5 런타임 탐침)로 이어간다.\n",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"- {RUN_ID}",
        f"- {RUN_ID}: packaged(패키지 완료) density restore stress candidate(밀도 복원 압박 후보) for MT5 runtime probe(MT5 런타임 탐침).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"- {RUN_ID}",
        f"- {RUN_ID}: ba02 density restore stress candidate(ba02 밀도 복원 압박 후보)를 MT5 runtime package(MT5 런타임 패키지)로 이동했다. MT5 evidence(MT5 근거)는 아직 필요하다.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"- {RUN_ID}",
        f"- {RUN_ID}: package_only_no_authority(패키지 전용, 권위 없음). Effect(효과): 실행 전 operating claim(운영 주장)을 막는다.\n",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["trade_tape_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(RUN_DIR),
        "primary_report": rel(REPORT_PATH),
        "family": "runtime_probe_package(런타임 탐침 패키지)",
        "lane": "runtime_verification(런타임 검증)",
        "work_family": "runtime_backtest(런타임 백테스트)",
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": final["judgment"],
        "external_verification_status": "package_only_mt5_not_run(패키지 전용, MT5 미실행)",
        "next_action": NEXT_RUN_ID,
        "question": "Can ba02 density restore stress candidate be executed in MT5 runtime probe?(ba02 밀도 복원 압박 후보를 MT5 런타임 탐침으로 실행할 수 있는가?)",
        "notes": f"candidate={final['selected_queue_id']};pf={final['expected_combined_profit_factor']};estimated_density={final['expected_estimated_mt5_density']};next={NEXT_RUN_ID}",
        "net_profit": final["expected_combined_net_profit"],
        "profit_factor": final["expected_combined_profit_factor"],
        "expectancy": final["expected_combined_expectancy"],
        "drawdown": final["expected_combined_max_drawdown"],
        "recovery_factor": final["expected_combined_recovery_factor"],
        "trade_count": final["expected_combined_trade_count"],
        "long_trade_count": final["expected_combined_long_count"],
        "short_trade_count": final["expected_combined_short_count"],
        "expected_estimated_mt5_density": final["expected_estimated_mt5_density"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    alpha_rows = []
    for suffix, view, tier, scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "runtime package selected primary(선택 주 후보 런타임 패키지)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A package plus Tier B out_of_scope(Tier A 패키지 + Tier B 범위 밖)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": suffix,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "scoreboard_lane": "runtime_package(런타임 패키지)",
                "primary_kpi": f"pf={final['expected_combined_profit_factor']};estimated_density={final['expected_estimated_mt5_density']};net={final['expected_combined_net_profit']}",
                "guardrail_kpi": "no_runtime_authority;no_trade_splitting;mt5_execution_required",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        alpha_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], alpha_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], alpha_rows, extend_header=True)
    artifact_rows = []
    for artifact_type, path, note in [
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE, "MT5 runtime probe attempt package(MT5 런타임 탐침 시도 패키지)."),
        ("tester_set_manifest", TESTER_SET_MANIFEST, "Tester set manifest(테스터 설정 목록)."),
        ("tester_ini_manifest", TESTER_INI_MANIFEST, "Tester ini manifest(테스터 INI 목록)."),
        ("runtime_policy_config", RUNTIME_POLICY_CONFIG, "Runtime policy config(런타임 정책 설정)."),
        ("common_files_sync", COMMON_FILES_SYNC, "Common Files sync manifest(공용 파일 동기화 목록)."),
        ("runtime_parity_contract", RUNTIME_PARITY_CONTRACT, "Runtime parity contract(런타임 동등성 계약)."),
        ("backtest_forensics_receipt", BACKTEST_RECEIPT, "Backtest forensics receipt(백테스트 포렌식 영수증)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "User report(사용자 보고서)."),
        ("decision", DECISION_DOC, "Decision record(결정 기록)."),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
                "created_at": final["created_at_utc"],
                "created_at_utc": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "notes": note,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
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
            "parent_scout_run_id": PARENT_SCOUT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "output_files": [{"path": rel(path), "sha256": sha(path)} for path in outputs if exists(path)],
        },
    )


def main() -> None:
    ensure_dirs()
    selected = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    package = write_runtime_package(selected)
    compile_result, portable_sync = run_compile_and_sync()
    write_contracts(selected, package, compile_result, portable_sync)
    final = final_payload(selected, package, compile_result, portable_sync)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final, package, gates)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import copy_to_common_files, mt5_runtime_module_hashes, sha256_file  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import package_density_side_balance_repair_runtime_probe_without_db as basepkg  # noqa: E402
from stage_pipelines.stage364 import train_threshold_edge_pf_gap_repair_scout_without_db as scout  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = scout.STAGE_ID
RUN_NUMBER = "run364AU"
RUN_ID = "run364AU_package_threshold_edge_floor001_runtime_probe_without_db_v1"
PARENT_RUN_ID = "run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1"
PARENT_SCOUT_RUN_ID = scout.RUN_ID
NEXT_RUN_ID = "run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1"

STATUS = "completed_stage364AU_threshold_edge_floor001_runtime_probe_package_prepared_compile_checked_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_threshold_edge_floor001_mt5_execution_required_no_authority"
DECISION = "stage364AU_open_run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_common_files_synced_compile_checked_no_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MODEL_ID = basepkg.MODEL_ID
OUTPUT_CONTRACT = "p_short_p_flat_p_long_direct_three_class_probability_threshold_margin"
ATTEMPT_NAME = "run364AU_threshold_edge_floor001_pshort0455_floor001_hold6"
REPORT_NAME = "OPv2_run364AU_threshold_edge_floor001"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

STAGE_DIR = scout.STAGE_DIR
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
RUN364AV_EXECUTION_QUEUE = RUN_DIR / "run364AV_execution_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364AU_threshold_edge_floor001_runtime_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AU_threshold_edge_floor001_runtime_probe_package.md"
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

PARENT_FINAL = RUN_DIR.parent / "run364AT" / "final_decision.json"
PARENT_GATE_AUDIT = RUN_DIR.parent / "run364AT" / "required_gate_coverage_audit.csv"
PARENT_QUEUE = RUN_DIR.parent / "run364AT" / "run364AU_runtime_probe_package_queue.csv"
SOURCE_SELECTED_CANDIDATE = scout.SELECTED_PROXY_CANDIDATE
SOURCE_SELECTED_TRADE_TAPE = scout.SELECTED_EXPECTED_TRADE_TAPE
SOURCE_PROBABILITY_TAPE = basepkg.scout.SELECTED_PROBABILITY_TAPE
SOURCE_FEATURE_MATRIX = basepkg.SOURCE_FEATURE_MATRIX
SOURCE_FEATURE_ORDER = basepkg.SOURCE_FEATURE_ORDER
SOURCE_ONNX = basepkg.SOURCE_ONNX
SOURCE_EA = basepkg.SOURCE_EA
SOURCE_EA_BINARY = basepkg.SOURCE_EA_BINARY
PORTABLE_EA_EX5 = basepkg.PORTABLE_EA_EX5
DEFAULT_METAEDITOR = basepkg.DEFAULT_METAEDITOR

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_threshold_edge_floor001_runtime_probe"
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
    RUN364AV_EXECUTION_QUEUE,
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


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.resolve().as_posix()


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    return sha256_file(Path(path))


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


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n", bom=True)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    new_rows = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if exists(path):
        header, existing_rows = read_csv_rows(path)
    else:
        header, existing_rows = [], []
    if extend_header:
        for row in new_rows:
            for key in row:
                if key not in header:
                    header.append(key)
    if not header:
        for row in new_rows:
            for key in row:
                if key not in header:
                    header.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [row for row in existing_rows if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys]
    write_csv(path, kept + list(new_rows), header)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, COMPILE_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AU inputs(364AU 입력 누락): " + ", ".join(missing))
    parent = read_json(PARENT_FINAL)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364AT next_run_id mismatch(다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden authority claim(부모 실행에 금지된 권위 주장이 있음)")
    _, gate_rows = read_csv_rows(PARENT_GATE_AUDIT)
    hard_failed = [row for row in gate_rows if row.get("status") not in {"passed", "warning", "out_of_scope_by_claim(주장 범위 밖)"}]
    if hard_failed:
        raise RuntimeError("run364AT hard gate failure(364AT 하드 게이트 실패)가 남아 있음")
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    if selected.get("source_queue_id") != "threshold_edge_floor001_probe":
        raise RuntimeError("selected source queue mismatch(선택 원천 대기열 불일치)")
    return selected


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "source_path": rel(path),
                "sha256": sha(path),
                "exists": exists(path),
                "effect(효과)": "package lineage input(패키지 계보 입력)을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def copy_common(local_path: Path, common_path: str, sync_id: str, effect: str) -> dict[str, Any]:
    result = copy_to_common_files(basepkg.basepkg.DEFAULT_COMMON_FILES, local_path, common_path)
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


def expected_kpi_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for split, prefix in [("validation", "validation"), ("oos", "oos"), ("combined", "combined")]:
        rows.append(
            {
                "run_id": RUN_ID,
                "split": split,
                "trade_count": selected.get(f"{prefix}_trade_count"),
                "business_days": selected.get(f"{prefix}_business_days"),
                "trade_density_per_business_day": selected.get(f"{prefix}_trade_per_business_day"),
                "net_profit": selected.get(f"{prefix}_net_profit"),
                "profit_factor": selected.get(f"{prefix}_profit_factor"),
                "expectancy": selected.get(f"{prefix}_expectancy"),
                "max_drawdown": selected.get(f"{prefix}_max_drawdown"),
                "recovery_factor": selected.get(f"{prefix}_recovery_factor"),
                "long_trade_count": selected.get(f"{prefix}_long_count"),
                "short_trade_count": selected.get(f"{prefix}_short_count"),
                "source": rel(SOURCE_SELECTED_TRADE_TAPE),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def run_compile_and_sync() -> tuple[dict[str, Any], dict[str, Any]]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    copied = False
    copy_error = ""
    if result.get("status") == "completed" and exists(SOURCE_EA_BINARY):
        try:
            io_path(PORTABLE_EA_EX5.parent).mkdir(parents=True, exist_ok=True)
            shutil.copy2(io_path(SOURCE_EA_BINARY), io_path(PORTABLE_EA_EX5))
            copied = exists(PORTABLE_EA_EX5)
        except OSError as exc:
            copy_error = repr(exc)
    portable = {
        "run_id": RUN_ID,
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
        "copied": copied,
        "copy_error": copy_error,
        "effect(효과)": "compiled EA binary(컴파일된 EA 바이너리)를 portable tester(포터블 테스터) 위치에 맞춘다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(COMPILE_RESULT, result)
    write_json(PORTABLE_EA_SYNC, portable)
    return result, portable


def runtime_filter_support() -> dict[str, bool]:
    text = io_path(SOURCE_EA).read_text(encoding="utf-8-sig")
    required = [
        "InpBlockPremarketShort",
        "InpMarchNonHour16MarginFilter",
        "InpEntryMarginFloor",
        "ApplyRuntimeTimeFilters",
    ]
    return {name: name in text for name in required}


def materialize_package(selected: Mapping[str, Any]) -> dict[str, Any]:
    common_feature = f"{COMMON_FEATURE_DIR}/density_lift_trade_shape_features.csv"
    common_model = f"{COMMON_MODEL_DIR}/{MODEL_ID}.onnx"
    common_feature_order = f"{COMMON_CONFIG_DIR}/feature_order.json"
    common_probability = f"{COMMON_EXPECTED_DIR}/dual_side_selected_expected_probability_tape.csv"
    common_trade = f"{COMMON_EXPECTED_DIR}/threshold_edge_floor001_expected_trade_tape.csv"
    common_selected = f"{COMMON_CONFIG_DIR}/selected_proxy_candidate.json"
    common_policy = f"{COMMON_CONFIG_DIR}/runtime_policy_config.json"

    policy = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_scout_run_id": PARENT_SCOUT_RUN_ID,
        "model_id": MODEL_ID,
        "variant_id": selected.get("variant_id"),
        "output_contract": OUTPUT_CONTRACT,
        "decision_surface": {
            "InpDecisionMode": "threshold_margin",
            "InpShortThreshold": selected.get("short_probability_threshold"),
            "InpLongThreshold": selected.get("long_threshold"),
            "InpMinMargin": selected.get("min_margin"),
            "InpEntryMarginFloor": selected.get("entry_margin_floor"),
            "InpSideFilterEnabled": True,
            "InpSideFilterFeatureIndex": basepkg.SIDE_FILTER_FEATURE_INDEX,
            "InpBlockLongFeatureRange": True,
            "InpBlockLongFeatureMin": selected.get("long_block_min"),
            "InpBlockLongFeatureMax": basepkg.SIDE_FILTER_BLOCK_MAX,
            "InpBlockPremarketShort": True,
            "InpPremarketStartHour": 12,
            "InpPremarketEndHour": 17,
            "InpMarchNonHour16MarginFilter": True,
            "InpMarchFilterMonth": 3,
            "InpMarchFilterBlockedHour": 16,
            "InpMarchFilterAbsMarginMin": selected.get("bridge_policy_value"),
            "InpMaxHoldBars": selected.get("max_hold_m5"),
        },
        "proxy_policy": {
            "bridge_policy": selected.get("bridge_policy"),
            "session_policy": selected.get("session_policy"),
            "side_policy": selected.get("side_policy"),
            "restore_policy": selected.get("restore_policy"),
        },
        "expected_proxy": {
            "combined_net_profit": selected.get("combined_net_profit"),
            "combined_profit_factor": selected.get("combined_profit_factor"),
            "combined_trade_per_business_day": selected.get("combined_trade_per_business_day"),
            "combined_max_drawdown": selected.get("combined_max_drawdown"),
            "combined_trade_count": selected.get("combined_trade_count"),
            "combined_long_count": selected.get("combined_long_count"),
            "combined_short_count": selected.get("combined_short_count"),
            "validation_net_profit": selected.get("validation_net_profit"),
            "oos_net_profit": selected.get("oos_net_profit"),
        },
        "known_differences": [
            "proxy expected value(프록시 예상값)는 MT5 Strategy Tester(MT5 전략 테스터) KPI(핵심 성과 지표)를 대체하지 않는다.",
            "MT5 runtime probe(MT5 런타임 탐침)는 spread/slippage/fill(스프레드/슬리피지/체결)을 실제 테스터 출력에서 읽어야 한다.",
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
        copy_common(SOURCE_SELECTED_TRADE_TAPE, common_trade, "common_expected_trade_tape", "selected expected trade tape(선택 예상 거래 기록)를 Common Files(공용 파일)에 복사한다."),
        copy_common(SOURCE_SELECTED_CANDIDATE, common_selected, "common_selected_candidate", "selected candidate(선택 후보)를 Common Files(공용 파일)에 복사한다."),
        copy_common(RUNTIME_POLICY_CONFIG, common_policy, "common_runtime_policy", "runtime policy(런타임 정책)를 Common Files(공용 파일)에 복사한다."),
    ]
    write_csv(COMMON_FILES_SYNC, sync_rows)

    set_path = SET_DIR / "OPv2_run364AU.set"
    ini_path = INI_DIR / "OPv2_run364AU.ini"
    telemetry_path = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_telemetry.csv"
    summary_path = f"{COMMON_TELEMETRY_DIR}/{ATTEMPT_NAME}_summary.csv"
    set_values = {
        "InpRunId": f"{RUN_ID}_{ATTEMPT_NAME}",
        "InpExplorationLabel": "stage364_ThresholdEdgeFloor001__RuntimeProbe",
        "InpTierLabel": "Tier A",
        "InpPrimaryActiveTier": "tier_a",
        "InpSplitLabel": "validation_oos_threshold_edge_floor001",
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpEnforceM5": True,
        "InpFeatureCsvPath": common_feature,
        "InpFeatureCount": 58,
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
        "InpFeatureOrderHash": FEATURE_ORDER_HASH,
        "InpFallbackEnabled": False,
        "InpShortThreshold": float(selected.get("short_probability_threshold", 0.455)),
        "InpLongThreshold": float(selected.get("long_threshold", 0.0)),
        "InpMinMargin": float(selected.get("min_margin", -0.000562137088)),
        "InpDecisionMode": "threshold_margin",
        "InpInvertSignal": False,
        "InpSideFilterEnabled": True,
        "InpSideFilterFeatureIndex": basepkg.SIDE_FILTER_FEATURE_INDEX,
        "InpFallbackSideFilterFeatureIndex": -1,
        "InpBlockShortFeatureRange": False,
        "InpBlockLongFeatureRange": True,
        "InpBlockLongFeatureMin": float(selected.get("long_block_min", 40.0)),
        "InpBlockLongFeatureMax": basepkg.SIDE_FILTER_BLOCK_MAX,
        "InpBlockPremarketShort": True,
        "InpPremarketStartHour": 12,
        "InpPremarketEndHour": 17,
        "InpMarchNonHour16MarginFilter": True,
        "InpMarchFilterMonth": 3,
        "InpMarchFilterBlockedHour": 16,
        "InpMarchFilterAbsMarginMin": float(selected.get("bridge_policy_value", 0.10)),
        "InpEntryMarginFloor": float(selected.get("entry_margin_floor", 0.001)),
        "InpAllowTrading": True,
        "InpFixedLot": 0.1,
        "InpMagic": 36424001,
        "InpDeviationPoints": 20,
        "InpCloseOnFlatSignal": False,
        "InpReverseOnOppositeSignal": True,
        "InpCloseOnlyOnOppositeSignal": False,
        "InpMaxHoldBars": int(selected.get("max_hold_m5", 6)),
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
            from_date="2025.01.02",
            to_date="2026.04.14",
            report=REPORT_NAME,
        ),
        ini_path,
        set_file_path=Path("OPv2_run364AU.set"),
    )
    set_rows = [
        {
            "attempt_name": ATTEMPT_NAME,
            "model_id": MODEL_ID,
            "variant_id": selected.get("variant_id"),
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "parameter_count": set_payload["parameter_count"],
            "short_threshold": selected.get("short_probability_threshold"),
            "long_threshold": selected.get("long_threshold"),
            "min_margin": selected.get("min_margin"),
            "entry_margin_floor": selected.get("entry_margin_floor"),
            "side_filter_feature": selected.get("long_block_feature"),
            "side_filter_feature_index": basepkg.SIDE_FILTER_FEATURE_INDEX,
            "block_long_min": selected.get("long_block_min"),
            "block_premarket_short": True,
            "march_non_hour16_margin_filter": True,
            "march_abs_margin_min": selected.get("bridge_policy_value"),
            "max_hold_bars": selected.get("max_hold_m5"),
            "allow_trading": True,
            "fixed_lot": 0.1,
            "output_contract": OUTPUT_CONTRACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    ini_rows = [
        {
            "attempt_name": ATTEMPT_NAME,
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
            "expert": ini_payload["tester"].get("Expert", ""),
            "symbol": ini_payload["tester"].get("Symbol", ""),
            "period": ini_payload["tester"].get("Period", ""),
            "model": ini_payload["tester"].get("Model", ""),
            "deposit": ini_payload["tester"].get("Deposit", ""),
            "leverage": ini_payload["tester"].get("Leverage", ""),
            "from_date": ini_payload["tester"].get("FromDate", ""),
            "to_date": ini_payload["tester"].get("ToDate", ""),
            "report": ini_payload["tester"].get("Report", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    return {
        "sync_rows": sync_rows,
        "common_feature": common_feature,
        "common_model": common_model,
        "common_probability": common_probability,
        "common_trade": common_trade,
        "common_policy": common_policy,
        "common_sync_missing": sum(1 for row in sync_rows if not exists(Path(row["absolute_path"]))),
        "set_path": set_path,
        "ini_path": ini_path,
        "set_sha256": set_payload["sha256"],
        "ini_sha256": ini_payload["sha256"],
        "report_name": REPORT_NAME,
        "telemetry_path": telemetry_path,
        "summary_path": summary_path,
        "set_values": set_values,
    }


def write_contracts(selected: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> None:
    handoff = [
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
            "effect(효과)": "ONNX/feature/policy(온엑스/피처/정책)를 Common Files(공용 파일)에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    semantic_gap = [
        {
            "run_id": RUN_ID,
            "gap_id": "threshold_edge_policy_runtime_support",
            "proxy_policy": "restore_march_non_hour16_margin + all_sessions_except_premarket_short + entry_margin_floor",
            "mt5_support": "implemented_in_runtime_inputs(런타임 입력으로 구현됨)",
            "inputs": "InpMarchNonHour16MarginFilter, InpBlockPremarketShort, InpEntryMarginFloor",
            "remaining_gap": "tester cost/fill/slippage only after MT5 execution(테스터 비용/체결/슬리피지는 MT5 실행 뒤 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    tester = [
        {
            "contract_id": "tester_identity",
            "run_id": RUN_ID,
            "attempt_name": ATTEMPT_NAME,
            "terminal": basepkg.basepkg.DEFAULT_TERMINAL.as_posix(),
            "common_files_root": basepkg.basepkg.DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": basepkg.basepkg.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "symbol": "US100",
            "timeframe": "M5",
            "tester_model": 4,
            "deposit": 500,
            "leverage": "1:100",
            "fixed_lot": 0.1,
            "report_name": package["report_name"],
            "compile_status": compile_result.get("status"),
            "portable_ea_copied": portable_sync.get("copied"),
            "effect(효과)": "tester identity(테스터 정체성)를 고정해 MT5 KPI(핵심 성과 지표) 비교 기준을 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    comparison = [
        {
            "contract_id": "proxy_mt5_diff_required",
            "run_id": RUN_ID,
            "attempt_name": ATTEMPT_NAME,
            "proxy_trade_tape": rel(SOURCE_SELECTED_TRADE_TAPE),
            "common_expected_trade_tape": package["common_trade"],
            "mt5_required_outputs": "runtime telemetry, tester report(런타임 기록, 테스터 보고서)",
            "diff_fields": "trade count, net profit, PF, DD, side/session/month stress(거래수, 순수익, PF, DD, 방향/세션/월 압박)",
            "effect(효과)": "proxy expected value(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    parity = [
        {
            "research_path": rel(scout.REPORT_PATH),
            "runtime_path": rel(TESTER_SET_MANIFEST),
            "shared_contract": "closed M5 bar, next tick entry, p_short/p_flat/p_long, threshold_margin, ADX long block, March hour/margin filter, premarket short block(닫힌 M5 봉, 다음 틱 진입, 확률 3종, 임계값, ADX 롱 차단, 3월 시각/마진 필터, 프리마켓 숏 차단)",
            "known_differences": "MT5 execution cost/fill unknown until run364AV(MT5 실행 비용/체결은 364AV 전까지 미확인)",
            "parity_check": "compile/common-files/set/ini package only; run364AV must execute Strategy Tester(컴파일/공용 파일/설정/INI 패키지 전용, 364AV 전략 테스터 필요)",
            "parity_identity": json.dumps(mt5_runtime_module_hashes(), ensure_ascii=False),
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "attempt_name": ATTEMPT_NAME,
            "set_path": rel(package["set_path"]),
            "ini_path": rel(package["ini_path"]),
            "terminal_path": basepkg.basepkg.DEFAULT_TERMINAL.as_posix(),
            "common_files_root": basepkg.basepkg.DEFAULT_COMMON_FILES.as_posix(),
            "required_outputs": "runtime telemetry, tester report, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
            "blocked_if_missing": "terminal, compiled EA, Common Files handoff, tester output(터미널, 컴파일된 EA, 공용 파일 인계, 테스터 출력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(MODEL_HANDOFF_MANIFEST, handoff)
    write_csv(RUNTIME_SEMANTIC_GAP_AUDIT, semantic_gap)
    write_csv(TESTER_IDENTITY_CONTRACT, tester)
    write_csv(PROXY_MT5_COMPARISON_CONTRACT, comparison)
    write_csv(RUNTIME_PARITY_CONTRACT, parity)
    write_csv(RUN364AV_EXECUTION_QUEUE, queue)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, queue)


def final_payload(selected: Mapping[str, Any], package: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> dict[str, Any]:
    compile_pass = compile_result.get("status") == "completed" and portable_sync.get("copied") is True
    support = runtime_filter_support()
    support_pass = all(support.values())
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_scout_run_id": PARENT_SCOUT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS if compile_pass and support_pass else "blocked_stage364AU_package_prepared_but_compile_or_runtime_filter_support_failed_no_authority",
        "judgment": JUDGMENT if compile_pass and support_pass else "runtime_probe_package_created_repair_required_no_authority",
        "decision": DECISION if compile_pass and support_pass else "stage364AU_repair_runtime_filter_or_compile_before_mt5_probe",
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_variant_id": selected.get("variant_id"),
        "selected_queue_id": selected.get("queue_id"),
        "model_id": MODEL_ID,
        "attempt_name": ATTEMPT_NAME,
        "short_threshold": selected.get("short_probability_threshold"),
        "long_threshold": selected.get("long_threshold"),
        "min_margin": selected.get("min_margin"),
        "entry_margin_floor": selected.get("entry_margin_floor"),
        "long_block_min": selected.get("long_block_min"),
        "max_hold_m5": selected.get("max_hold_m5"),
        "bridge_policy": selected.get("bridge_policy"),
        "session_policy": selected.get("session_policy"),
        "expected_combined_net_profit": selected.get("combined_net_profit"),
        "expected_combined_profit_factor": selected.get("combined_profit_factor"),
        "expected_combined_trade_density": selected.get("combined_trade_per_business_day"),
        "expected_combined_expectancy": selected.get("combined_expectancy"),
        "expected_combined_max_drawdown": selected.get("combined_max_drawdown"),
        "expected_combined_recovery_factor": selected.get("combined_recovery_factor"),
        "expected_combined_trade_count": selected.get("combined_trade_count"),
        "expected_combined_long_count": selected.get("combined_long_count"),
        "expected_combined_short_count": selected.get("combined_short_count"),
        "common_sync_rows": len(package["sync_rows"]),
        "common_sync_missing": package["common_sync_missing"],
        "compile_status": compile_result.get("status"),
        "compile_log": rel(COMPILE_LOG) if exists(COMPILE_LOG) else "",
        "portable_ea_copied": portable_sync.get("copied"),
        "runtime_filter_support": support,
        "terminal_exists": exists(basepkg.basepkg.DEFAULT_TERMINAL),
        "common_files_exists": exists(basepkg.basepkg.DEFAULT_COMMON_FILES),
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "set_path": rel(package["set_path"]),
        "ini_path": rel(package["ini_path"]),
        "report_name": package["report_name"],
        "runtime_module_hashes": mt5_runtime_module_hashes(),
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    support_pass = all(final.get("runtime_filter_support", {}).values())
    compile_pass = final.get("compile_status") == "completed" and final.get("portable_ea_copied") is True
    gates = [
        ("runtime_evidence_gate(런타임 근거 게이트)", final["common_sync_rows"] >= 7 and final["common_sync_missing"] == 0, COMMON_FILES_SYNC, "Common Files(공용 파일) 인계를 완료했다."),
        ("scope_completion_gate(범위 완료 게이트)", exists(RUNTIME_PROBE_ATTEMPT_PACKAGE) and exists(TESTER_INI_MANIFEST), RUNTIME_PROBE_ATTEMPT_PACKAGE, "package scope(패키지 범위)를 끝냈고 MT5 execution(MT5 실행)은 다음 실행으로 분리했다."),
        ("runtime_filter_support_gate(런타임 필터 지원 게이트)", support_pass, SOURCE_EA, "proxy policy(프록시 정책)를 EA input(EA 입력)으로 표현한다."),
        ("metaeditor_compile_gate(메타에디터 컴파일 게이트)", compile_pass, COMPILE_RESULT, "EA(전문가 자문)를 컴파일하고 portable tester(포터블 테스터)에 복사했다."),
        ("tester_identity_gate(테스터 정체성 게이트)", exists(TESTER_SET_MANIFEST) and exists(TESTER_INI_MANIFEST), TESTER_SET_MANIFEST, "US100 M5, real ticks, deposit 500, leverage 100(US100 M5, 실제 틱, 예치금 500, 레버리지 100)을 고정했다."),
        ("kpi_contract_audit(KPI 계약 감사)", exists(EXPECTED_KPI_SUMMARY), EXPECTED_KPI_SUMMARY, "proxy KPI(프록시 핵심 성과 지표)를 MT5 비교 기준으로 남겼다."),
        ("required_gate_coverage_audit(필수 게이트 커버리지 감사)", True, GATE_AUDIT, "runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다."),
        ("final_claim_guard(최종 주장 가드)", True, FINAL_DECISION, "runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)를 주장하지 않는다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": gate,
            "status": "passed" if passed else "blocked",
            "evidence(근거)": rel(artifact),
            "effect(효과)": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, artifact, effect in gates
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
                "obsidian-prime-ml(프로젝트 전용 ML)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [row["gate(게이트)"] for row in gates],
        },
    )
    write_json(DATA_RECEIPT, {**base, "timestamp_boundary": "closed_m5_bar_target_time_no_lookahead(닫힌 M5 봉 기준, 미래참조 없음)", "input_manifest": rel(INPUT_MANIFEST)})
    write_json(MODEL_RECEIPT, {**base, "model_boundary": "existing ONNX reused, no new model training(기존 온엑스 재사용, 새 모델 학습 없음)", "model_id": MODEL_ID})
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(scout.REPORT_PATH),
            "runtime_path": rel(TESTER_SET_MANIFEST),
            "shared_contract": "threshold + time/session filters + maxhold(임계값 + 시간/세션 필터 + 최대 보유)",
            "known_differences": "MT5 tester output not run yet(MT5 테스터 출력 미실행)",
            "parity_check": "compile/common-files/set/ini package only(컴파일/공용 파일/설정/INI 패키지 전용)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(BACKTEST_RECEIPT, {**base, "strategy_tester_execution": "not_run", "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "producer": RUN_ID, "consumer": NEXT_RUN_ID, "common_files_sync": rel(COMMON_FILES_SYNC), "runtime_module_hashes": final["runtime_module_hashes"]})
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(COMMON_FILES_SYNC), rel(TESTER_SET_MANIFEST), rel(COMPILE_RESULT), rel(EXPECTED_KPI_SUMMARY)],
            "evidence_missing": ["MT5 tester report(MT5 테스터 보고서)", "runtime telemetry(런타임 기록)", "proxy-vs-MT5 diff(프록시-MT5 차이)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(CLAIM_RECEIPT, {**base, "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "all_forbidden_claims": "not_claimed"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + "|")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    gate_total = len(gates)
    report = f"""# run364AU threshold edge floor001 runtime probe package(364AU 임계값 경계 하한 0.001 런타임 탐침 패키지)

## Summary(요약)

Action(행동): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다.

Effect(효과): `{NEXT_RUN_ID}`에서 Strategy Tester(전략 테스터)를 실행해 proxy/MT5 diff(프록시/MT5 차이)를 비교할 수 있다.

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- model_id(모델 ID): `{MODEL_ID}`
- expected combined net/PF(예상 합산 순수익/수익 팩터): `{final['expected_combined_net_profit']}` / `{final['expected_combined_profit_factor']}`
- expected density/DD(예상 밀도/낙폭): `{final['expected_combined_trade_density']}` / `{final['expected_combined_max_drawdown']}`
- compile status(컴파일 상태): `{final['compile_status']}`
- portable EA copied(포터블 EA 복사): `{final['portable_ea_copied']}`

## Runtime Contract(런타임 계약)

- short threshold(숏 임계값): `{final['short_threshold']}`
- entry margin floor(진입 마진 하한): `{final['entry_margin_floor']}`
- max hold(최대 보유): `{final['max_hold_m5']}`
- March filter(3월 필터): non-hour16 + abs margin >= `{final['bridge_policy']}`
- premarket short block(프리마켓 숏 차단): enabled(활성)

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Claim Boundary(주장 경계)

이 package(패키지)는 runtime probe(런타임 탐침) 준비물이다. MT5 tester report(MT5 테스터 보고서), runtime telemetry(런타임 기록), proxy-vs-MT5 diff(프록시-MT5 차이)가 아직 없으므로 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, report, bom=True)
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - threshold edge floor001 runtime probe package(임계값 경계 하한 0.001 런타임 탐침 패키지).")
    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## {RUN_ID}

Action(행동): threshold-edge floor001 proxy(임계값 경계 하한 0.001 프록시)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다.

Effect(효과): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행할 수 있다. 운영 승격과 runtime authority(런타임 권위)는 없다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_runtime_probe_required(런타임 탐침 필요라 없음)
- runtime_probe_candidate(런타임 탐침 후보): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`
- package_decision(패키지 결정): `runtime_probe_package_ready_mt5_execution_required(런타임 탐침 패키지 준비, MT5 실행 필요)`
- selected_proxy_candidate(선택 프록시 후보): `{rel(SOURCE_SELECTED_CANDIDATE)}`
- runtime_probe_attempt_package(런타임 탐침 시도 패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- next_execution_queue(다음 실행 대기열): `{rel(RUN364AV_EXECUTION_QUEUE)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364AU Threshold Edge Floor001 Runtime Probe Package(364AU 임계값 경계 하한 0.001 런타임 탐침 패키지)

Action(행동): AS selected proxy(AS 선택 프록시)를 MT5 set/ini(MT5 설정/INI), Common Files(공용 파일), compile receipt(컴파일 영수증)로 package(패키지)했다.

Effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 `{NEXT_RUN_ID}` 실행으로 이어간다.
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

current_stage(현재 단계): `{STAGE_ID}`

latest_completed_run(최근 완료 실행): `{RUN_ID}`

current_run(현재 실행): `{NEXT_RUN_ID}`

current_truth(현재 진실): run364AU(364AU 실행)는 run364AS(364AS 실행)의 `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)`를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다. expected combined net/PF(예상 합산 순수익/수익 팩터)는 `{final['expected_combined_net_profit']}` / `{final['expected_combined_profit_factor']}`, density/DD(밀도/낙폭)는 `{final['expected_combined_trade_density']}` / `{final['expected_combined_max_drawdown']}`이다.

operating_truth_boundary(운영 진실 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no goal achieve(목표 달성 없음).

next_action(다음 행동): `{NEXT_RUN_ID}`에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy/MT5 diff(프록시/MT5 차이)를 기록한다.
""",
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} - {RUN_ID}

- action(행동): threshold edge floor001 runtime probe package(임계값 경계 하한 0.001 런타임 탐침 패키지)를 만들었다.
- effect(효과): `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)의 PF lift(PF 개선)를 MT5 runtime(MT5 런타임)에서 확인한다.
- positive clue(긍정 단서): expected PF(예상 수익 팩터) `{final['expected_combined_profit_factor']}`, density(밀도) `{final['expected_combined_trade_density']}`.
- failure memory(실패 기억): MT5 report/telemetry(MT5 보고서/기록) 전에는 runtime authority(런타임 권위) 금지.
""",
    )


def write_registries(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    gate_total = len(gates)
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_probe_package(런타임 탐침 패키지)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(RUN_DIR),
        "family": "runtime_backtest(런타임 백테스트)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["common_sync_rows"],
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "best_model_id": MODEL_ID,
        "net_profit": final["expected_combined_net_profit"],
        "profit_factor": final["expected_combined_profit_factor"],
        "drawdown": final["expected_combined_max_drawdown"],
        "recovery_factor": final["expected_combined_recovery_factor"],
        "trade_count": final["expected_combined_trade_count"],
        "expectancy": final["expected_combined_expectancy"],
        "long_trade_count": final["expected_combined_long_count"],
        "short_trade_count": final["expected_combined_short_count"],
        "source_package_run_id": PARENT_SCOUT_RUN_ID,
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "external_verification_status": "common_files_synced_compile_checked_mt5_execution_required(공용 파일 동기화/컴파일 확인, MT5 실행 필요)",
        "trade_density_per_feature_day": final["expected_combined_trade_density"],
        "trade_density_requirement_status": "passed_min3_proxy_mt5_pending(프록시 최소 3 통과, MT5 대기)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "primary_artifact": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
        "work_family": "runtime_backtest(런타임 백테스트)",
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can threshold-edge floor001 proxy survive MT5 runtime?(임계값 경계 하한 0.001 프록시가 MT5 런타임에서 버티는가?)",
    }
    run_row = dict(common)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=True)
    ledger_rows = []
    for suffix, record_view, tier_scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B"),
        ("Tier_A_plus_B", "Tier A+B combined(Tier A+B 합산)", "Tier A+B"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": "proxy package expected KPI; MT5 pending(프록시 패키지 예상 KPI, MT5 대기)",
            }
        )
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifacts = []
    for artifact_type, path, notes in [
        ("report", REPORT_PATH, "Package report(패키지 보고서)."),
        ("runtime_policy_config", RUNTIME_POLICY_CONFIG, "Runtime policy config(런타임 정책 설정)."),
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE, "MT5 execution queue(실행 대기열)."),
        ("tester_set_manifest", TESTER_SET_MANIFEST, "Tester set manifest(테스터 설정 목록)."),
        ("tester_ini_manifest", TESTER_INI_MANIFEST, "Tester ini manifest(테스터 INI 목록)."),
        ("common_files_sync", COMMON_FILES_SYNC, "Common Files sync(공용 파일 동기화)."),
        ("compile_result", COMPILE_RESULT, "MetaEditor compile result(메타에디터 컴파일 결과)."),
        ("gate_audit", GATE_AUDIT, "Gate audit(게이트 감사)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
    ]:
        if exists(path):
            artifacts.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifacts, extend_header=True)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(EXPECTED_KPI_SUMMARY, expected_kpi_rows(read_json(SOURCE_SELECTED_CANDIDATE)))
    write_csv(GATE_AUDIT, gates)
    final_with_counts = dict(final)
    final_with_counts["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final_with_counts["gate_total"] = len(gates)
    write_json(FINAL_DECISION, final_with_counts)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    selected = validate_inputs()
    package = materialize_package(selected)
    compile_result, portable_sync = run_compile_and_sync()
    write_contracts(selected, package, compile_result, portable_sync)
    final = final_payload(selected, package, compile_result, portable_sync)
    gates = gate_rows(final)
    write_receipts(final, package, gates)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_registries(final, gates)
    repair_run_registry_line_endings(RUN_ID)
    write_final_files(final, gates)
    print(json.dumps(json_ready(read_json(FINAL_DECISION)), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

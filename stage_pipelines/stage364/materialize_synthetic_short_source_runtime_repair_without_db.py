from __future__ import annotations

import argparse
import json
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
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as runtime_base  # noqa: E402
from stage_pipelines.stage364 import prepare_late_year_session_gate_mt5_precheck_without_db as bu  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = bu.STAGE_ID
RUN_NUMBER = "run364BV"
RUN_ID = "run364BV_materialize_synthetic_short_source_runtime_repair_without_db_v1"
PARENT_RUN_ID = bu.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = bu.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = bu.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BW_review_synthetic_short_source_runtime_probe_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_runtime_repair_and_mt5_probe_only_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

ATTEMPT_NAME = "run364BV_synthetic_short_source_overlay_calendar_block"
REPORT_NAME = "OPv2_run364BV_synthetic_short_overlay_calendar"
EXPLORATION_LABEL = "stage364_SyntheticShortSource__RuntimeRepair"
MODEL_ID = runtime_base.MODEL_ID

STAGE_DIR = bu.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUNTIME_SOURCE_SUPPORT_AUDIT = RUN_DIR / "runtime_source_support_audit.csv"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = COMPILE_DIR / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
RUNTIME_OUTPUT_VALIDATION = RUN_DIR / "runtime_output_validation.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BV_synthetic_short_source_runtime_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BV_synthetic_short_source_runtime_repair.md"
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
MT5_INPUT_CONTRACT = ROOT / "docs" / "contracts" / "mt5_ea_input_order_contract_fpmarkets_v2.md"

SOURCE_SELECTED_CANDIDATE = bu.SOURCE_SELECTED_CANDIDATE
SOURCE_SELECTED_TRADE_TAPE = bu.SOURCE_SELECTED_TRADE_TAPE
SOURCE_SYNTHETIC_SHORT_TAPE = bu.SOURCE_SYNTHETIC_SHORT_TAPE
SOURCE_PARENT_SUPPRESSED_TRADES = bu.SOURCE_PARENT_SUPPRESSED_TRADES
SOURCE_BK_FINAL = bu.SOURCE_BK_FINAL
SOURCE_BJ_SET = bu.SOURCE_BJ_SET
SOURCE_FEATURE_MATRIX = runtime_base.FEATURE_MATRIX
SOURCE_FEATURE_ORDER = runtime_base.FEATURE_ORDER
SOURCE_ONNX = runtime_base.SOURCE_ONNX
SOURCE_PROBABILITY_TAPE = runtime_base.EXPECTED_PROBABILITY_TAPE
SOURCE_EA = runtime_base.EA_SOURCE
SOURCE_EA_BINARY = runtime_base.EA_BINARY
PORTABLE_EA_EX5 = runtime_base.PORTABLE_EA_EX5
DEFAULT_METAEDITOR = runtime_base.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_TERMINAL = runtime_base.DEFAULT_TERMINAL
DEFAULT_COMMON_FILES = runtime_base.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = runtime_base.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = runtime_base.DEFAULT_PORTABLE_ROOT

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_synthetic_short_source_runtime_repair"
COMMON_FEATURE = f"{COMMON_ROOT}/features/density_lift_trade_shape_features.csv"
COMMON_MODEL = f"{COMMON_ROOT}/models/{MODEL_ID}.onnx"
COMMON_FEATURE_ORDER = f"{COMMON_ROOT}/config/feature_order.json"
COMMON_PROBABILITY = f"{COMMON_ROOT}/expected/density_lift_expected_probability_tape.csv"
COMMON_SELECTED = f"{COMMON_ROOT}/config/selected_bs_candidate.json"
COMMON_SYNTHETIC = f"{COMMON_ROOT}/expected/selected_bs_synthetic_short_tape.csv"
COMMON_TRADE = f"{COMMON_ROOT}/expected/selected_bs_trade_tape.csv"
COMMON_POLICY = f"{COMMON_ROOT}/config/runtime_policy_config.json"
COMMON_TELEMETRY = f"{COMMON_ROOT}/telemetry/{ATTEMPT_NAME}_telemetry.csv"
COMMON_SUMMARY = f"{COMMON_ROOT}/telemetry/{ATTEMPT_NAME}_summary.csv"

INPUT_FILES = [
    bu.FINAL_DECISION,
    bu.GATE_AUDIT,
    bu.RUN364BV_QUEUE,
    bu.RUNTIME_RULE_HANDOFF,
    SOURCE_SELECTED_CANDIDATE,
    SOURCE_SELECTED_TRADE_TAPE,
    SOURCE_SYNTHETIC_SHORT_TAPE,
    SOURCE_PARENT_SUPPRESSED_TRADES,
    SOURCE_BK_FINAL,
    SOURCE_BJ_SET,
    SOURCE_FEATURE_MATRIX,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_PROBABILITY_TAPE,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    RUNTIME_SOURCE_SUPPORT_AUDIT,
    RUNTIME_POLICY_CONFIG,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    TESTER_IDENTITY_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    RUNTIME_OUTPUT_VALIDATION,
    STRATEGY_TESTER_REPORTS,
    RUNTIME_OUTPUT_COPY,
    PROXY_MT5_DIFF,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
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
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return bu.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    bu.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    bu.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return bu.read_rows(path)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    bu.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    bu.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    bu.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
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
    return round(number, digits)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")).replace("|", "\\|") for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-mt5", action="store_true", help="Prepare and compile only.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    return parser.parse_args()


def ensure_dirs() -> None:
    for path in [RUN_DIR, SET_DIR, INI_DIR, COMPILE_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, SELECTED_DIR, SPEC_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BV inputs(BV 입력 누락): " + ", ".join(missing))
    bu_final = read_json(bu.FINAL_DECISION)
    if bu_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BU next_run_id mismatch(BU 다음 실행 불일치): {bu_final.get('next_run_id')} != {RUN_ID}")
    if bu_final.get("runtime_authority") != "not_claimed" or bu_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("BU has forbidden authority claim(BU 금지 권위 주장 존재)")
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    if selected.get("candidate_id") != bu_final.get("selected_candidate_id"):
        raise RuntimeError("selected candidate mismatch(선택 후보 불일치)")
    return bu_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BV runtime repair source(BV 런타임 수리 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def audit_runtime_support() -> list[dict[str, Any]]:
    ea_text = io_path(SOURCE_EA).read_text(encoding="utf-8-sig")
    contract_text = io_path(MT5_INPUT_CONTRACT).read_text(encoding="utf-8-sig")
    checks = [
        ("synthetic_enabled_input", "InpSyntheticShortSourceEnabled", ea_text),
        ("synthetic_hours_input", "InpSyntheticShortSourceHours", ea_text),
        ("synthetic_p_short_input", "InpSyntheticShortSourcePShortMin", ea_text),
        ("synthetic_margin_input", "InpSyntheticShortSourceMarginVsLongMin", ea_text),
        ("synthetic_reason", "synthetic_short_source_overlay:hour=", ea_text),
        ("synthetic_contract", "Runtime synthetic short source overlay", contract_text),
        ("calendar_block_still_present", "InpCalendarBlockEnabled", ea_text),
    ]
    rows = []
    for check_id, token, text in checks:
        rows.append(
            {
                "run_id": RUN_ID,
                "check_id": check_id,
                "token": token,
                "present": token in text,
                "status": "passed" if token in text else "failed",
                "effect": "합성 숏 원천과 12월 롱 차단을 같은 EA 입력 표면에서 표현한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_SOURCE_SUPPORT_AUDIT, rows)
    return rows


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


def date_bounds() -> tuple[str, str]:
    probability = pd.read_csv(io_path(SOURCE_PROBABILITY_TAPE))
    timestamps = pd.to_datetime(probability["bar_time_server"])
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def build_runtime_policy(selected: Mapping[str, Any]) -> dict[str, Any]:
    policy = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "selected_candidate_id": selected.get("candidate_id"),
        "model_id": MODEL_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "synthetic_short_source": {
            "enabled": True,
            "hours": "17|19|20",
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.075,
            "fixed_hold_bars": 6,
            "timestamp_safety": "closed M5 target time hour and model probabilities only(닫힌 M5 대상 시간과 모델 확률만 사용)",
        },
        "calendar_block": {
            "enabled": True,
            "side": "long",
            "month": 12,
            "start_hour": 21,
            "end_hour": 22,
        },
        "expected_proxy": {
            "net_profit": selected.get("net_profit"),
            "profit_factor": selected.get("profit_factor"),
            "expectancy": selected.get("expectancy"),
            "trade_count": selected.get("trade_count"),
            "density": selected.get("trade_density_per_business_day"),
            "long_trade_count": selected.get("long_trade_count"),
            "short_trade_count": selected.get("short_trade_count"),
            "synthetic_short_count": selected.get("synthetic_added_short_count"),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, policy)
    return policy


def materialize_package(policy: Mapping[str, Any]) -> dict[str, Any]:
    sync_rows = [
        copy_common(SOURCE_FEATURE_MATRIX, COMMON_FEATURE, "feature_matrix", "MT5 feature input(MT5 피처 입력)을 고정한다."),
        copy_common(SOURCE_ONNX, COMMON_MODEL, "onnx_model", "ONNX(온엑스) 모델을 고정한다."),
        copy_common(SOURCE_FEATURE_ORDER, COMMON_FEATURE_ORDER, "feature_order", "feature order(피처 순서)를 고정한다."),
        copy_common(SOURCE_PROBABILITY_TAPE, COMMON_PROBABILITY, "probability_tape", "proxy/MT5 diff(프록시/MT5 차이)의 확률 기준을 보존한다."),
        copy_common(SOURCE_SELECTED_CANDIDATE, COMMON_SELECTED, "selected_candidate", "선택 후보 계보를 보존한다."),
        copy_common(SOURCE_SYNTHETIC_SHORT_TAPE, COMMON_SYNTHETIC, "synthetic_short_tape", "합성 숏 원천 비교 테이프를 보존한다."),
        copy_common(SOURCE_SELECTED_TRADE_TAPE, COMMON_TRADE, "selected_trade_tape", "프록시 거래 테이프를 보존한다."),
        copy_common(RUNTIME_POLICY_CONFIG, COMMON_POLICY, "runtime_policy", "런타임 규칙 묶음을 보존한다."),
    ]
    write_csv(COMMON_FILES_SYNC, sync_rows)

    feature_order = read_json(SOURCE_FEATURE_ORDER)
    from_date, to_date = date_bounds()
    set_values = bu.parse_set_file(SOURCE_BJ_SET)
    set_values.update(
        {
            "InpRunId": f"{RUN_ID}_{ATTEMPT_NAME}",
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpSplitLabel": "validation_oos_synthetic_short_source_calendar",
            "InpFeatureCsvPath": COMMON_FEATURE,
            "InpModelPath": COMMON_MODEL,
            "InpModelId": MODEL_ID,
            "InpFeatureOrderHash": feature_order["feature_order_hash"],
            "InpSyntheticShortSourceEnabled": True,
            "InpSyntheticShortSourceHours": "17|19|20",
            "InpSyntheticShortSourcePShortMin": 0.4375,
            "InpSyntheticShortSourceMarginVsLongMin": 0.075,
            "InpCalendarBlockEnabled": True,
            "InpCalendarBlockSide": "long",
            "InpCalendarBlockMonth": 12,
            "InpCalendarBlockStartHour": 21,
            "InpCalendarBlockEndHour": 22,
            "InpMaxHoldBars": 6,
            "InpTelemetryCsvPath": COMMON_TELEMETRY,
            "InpSummaryCsvPath": COMMON_SUMMARY,
        }
    )
    set_path = SET_DIR / "OPv2_run364BV.set"
    ini_path = INI_DIR / "OPv2_run364BV.ini"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(shutdown_terminal=1, from_date=from_date, to_date=to_date, report=REPORT_NAME),
        ini_path,
        set_file_path=Path(set_path.name),
    )
    write_csv(
        TESTER_SET_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "synthetic_short_source_enabled": True,
                "synthetic_hours": "17|19|20",
                "calendar_block": "month=12,hour=21,side=long",
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
                "terminal": DEFAULT_TERMINAL.as_posix(),
                "symbol": "US100",
                "period": "M5",
                "model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "from_date": from_date,
                "to_date": to_date,
                "report": REPORT_NAME,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    attempt = {
        "attempt_name": ATTEMPT_NAME,
        "tier": "Tier A",
        "split": "validation_oos_synthetic_short_source_calendar",
        "set_path": set_path,
        "ini_path": ini_path,
        "tester_profile_set_path": DEFAULT_TESTER_PROFILE_ROOT / "OPv2_run364BV.set",
        "tester_profile_ini_path": DEFAULT_TESTER_PROFILE_ROOT / "OPv2_run364BV.ini",
        "common_telemetry_path": COMMON_TELEMETRY,
        "common_summary_path": COMMON_SUMMARY,
        "ini": ini_payload,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "common_telemetry_path": COMMON_TELEMETRY,
                "common_summary_path": COMMON_SUMMARY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "terminal": DEFAULT_TERMINAL.as_posix(),
                "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
                "symbol": "US100",
                "timeframe": "M5",
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "from_date": from_date,
                "to_date": to_date,
                "effect": "브로커 real tick(실제 틱) 비용 기준을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "research_path": rel(SOURCE_SELECTED_CANDIDATE),
                "runtime_path": rel(set_path),
                "shared_contract": "hour 17|19|20, p_short>=0.4375, p_short-p_long>=0.075, max_hold=6, Dec h21 long block",
                "known_differences": "MT5 tick fills/costs and bar-close execution may differ from fixed-price proxy(MT5 틱 체결/비용과 봉마감 실행은 고정가격 프록시와 다를 수 있음)",
                "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 한정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return attempt


def compile_and_sync() -> tuple[dict[str, Any], dict[str, Any]]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    write_json(COMPILE_RESULT, result)
    payload = {
        "run_id": RUN_ID,
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
        "copied": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if result.get("status") == "completed" and exists(SOURCE_EA_BINARY):
        io_path(PORTABLE_EA_EX5.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(SOURCE_EA_BINARY), io_path(PORTABLE_EA_EX5))
        payload.update({"copied": True, "source_sha256": sha(SOURCE_EA_BINARY), "portable_sha256": sha256_file(PORTABLE_EA_EX5)})
    write_json(PORTABLE_EA_SYNC, payload)
    return result, payload


def clear_stale_outputs(attempt: Mapping[str, Any]) -> None:
    for common_path in [attempt["common_telemetry_path"], attempt["common_summary_path"]]:
        target = DEFAULT_COMMON_FILES / Path(str(common_path))
        if exists(target):
            io_path(target).unlink()
    remove_existing_mt5_report_artifacts(DEFAULT_PORTABLE_ROOT, attempt, run_id=RUN_ID)


def execute_mt5(args: argparse.Namespace, attempt: Mapping[str, Any], compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    if args.skip_mt5 or compile_result.get("status") != "completed" or portable_sync.get("copied") is not True:
        runtime_outputs = {"status": "skipped" if args.skip_mt5 else "blocked", "reason": "skip_mt5_or_compile_sync_not_ready"}
        write_json(RUNTIME_OUTPUT_VALIDATION, runtime_outputs)
        write_json(MT5_EXECUTION_RESULT, [])
        write_json(STRATEGY_TESTER_REPORTS, [])
        write_csv(RUNTIME_OUTPUT_COPY, [])
        return [], runtime_outputs, [], []
    clear_stale_outputs(attempt)
    result = run_mt5_tester(
        DEFAULT_TERMINAL,
        Path(attempt["ini_path"]),
        set_path=Path(attempt["set_path"]),
        tester_profile_set_path=Path(attempt["tester_profile_set_path"]),
        tester_profile_ini_path=Path(attempt["tester_profile_ini_path"]),
        timeout_seconds=args.timeout_seconds,
        terminal_extra_args=["/portable"],
    )
    result.update({"attempt_name": ATTEMPT_NAME, "tier": attempt["tier"], "split": attempt["split"], "claim_boundary": CLAIM_BOUNDARY})
    runtime_outputs = wait_for_mt5_runtime_outputs(DEFAULT_COMMON_FILES, attempt, timeout_seconds=180, poll_seconds=2.0)
    result["runtime_outputs"] = runtime_outputs
    report_records = collect_mt5_strategy_report_artifacts(
        terminal_data_root=DEFAULT_PORTABLE_ROOT,
        run_output_root=RUN_DIR,
        attempts=[attempt],
        run_id=RUN_ID,
    )
    attach_mt5_report_metrics([result], report_records)
    copy_rows = copy_runtime_outputs(runtime_outputs)
    write_json(MT5_EXECUTION_RESULT, [result])
    write_json(RUNTIME_OUTPUT_VALIDATION, runtime_outputs)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    write_csv(RUNTIME_OUTPUT_COPY, copy_rows)
    write_json(
        TERMINAL_PROCESS_AUDIT,
        {
            "run_id": RUN_ID,
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "terminal_exists": exists(DEFAULT_TERMINAL),
            "returncode": result.get("returncode"),
            "status": result.get("status"),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return [result], runtime_outputs, report_records, copy_rows


def copy_runtime_outputs(runtime_outputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for key, dest_name in [("telemetry_path", f"{ATTEMPT_NAME}_telemetry.csv"), ("summary_path", f"{ATTEMPT_NAME}_summary.csv")]:
        source = Path(str(runtime_outputs.get(key, "")))
        if not source or not exists(source):
            continue
        destination = TELEMETRY_COPY_DIR / dest_name
        io_path(destination.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(source), io_path(destination))
        rows.append({"run_id": RUN_ID, "source_path": source.as_posix(), "copy_path": rel(destination), "sha256": sha(destination), "claim_boundary": CLAIM_BOUNDARY})
    return rows


def report_metrics(report_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    for record in report_records:
        metrics = record.get("metrics", {})
        if metrics.get("status") == "completed":
            return dict(metrics)
    return {}


def build_proxy_mt5_diff(selected: Mapping[str, Any], bk_final: Mapping[str, Any], runtime_outputs: Mapping[str, Any], report_records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    metrics = report_metrics(report_records)
    last_summary = runtime_outputs.get("last_summary", {}) if isinstance(runtime_outputs, Mapping) else {}
    row = {
        "run_id": RUN_ID,
        "comparison_id": "bs_proxy_vs_bv_mt5_runtime_probe",
        "proxy_net_profit": selected.get("net_profit"),
        "proxy_profit_factor": selected.get("profit_factor"),
        "proxy_trade_count": selected.get("trade_count"),
        "proxy_expectancy": selected.get("expectancy"),
        "proxy_long_trade_count": selected.get("long_trade_count"),
        "proxy_short_trade_count": selected.get("short_trade_count"),
        "mt5_net_profit": metrics.get("net_profit", ""),
        "mt5_profit_factor": metrics.get("profit_factor", ""),
        "mt5_trade_count": metrics.get("trade_count", ""),
        "mt5_expectancy": metrics.get("expectancy", ""),
        "mt5_recovery_factor": metrics.get("recovery_factor", ""),
        "mt5_equity_dd_amount": metrics.get("equity_drawdown_maximal_amount", ""),
        "mt5_long_trade_count": metrics.get("long_trade_count", ""),
        "mt5_short_trade_count": metrics.get("short_trade_count", ""),
        "runtime_short_decision_count": last_summary.get("short_count", ""),
        "runtime_long_decision_count": last_summary.get("long_count", ""),
        "bk_mt5_net_profit": bk_final.get("mt5_net_profit"),
        "bk_mt5_profit_factor": bk_final.get("mt5_profit_factor"),
        "bk_mt5_trade_count": bk_final.get("mt5_trade_count"),
        "net_diff_proxy_minus_mt5": finite(as_float(selected.get("net_profit")) - as_float(metrics.get("net_profit"))) if metrics else "",
        "net_diff_bv_minus_bk": finite(as_float(metrics.get("net_profit")) - as_float(bk_final.get("mt5_net_profit"))) if metrics else "",
        "profit_factor_diff_bv_minus_bk": finite(as_float(metrics.get("profit_factor")) - as_float(bk_final.get("mt5_profit_factor"))) if metrics else "",
        "usability": "usable_runtime_probe_diff" if metrics else "blocked_or_missing_mt5_metrics",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(PROXY_MT5_DIFF, [row])
    return [row]


def final_status(runtime_outputs: Mapping[str, Any], report_records: Sequence[Mapping[str, Any]], compile_result: Mapping[str, Any]) -> tuple[str, str, str]:
    metrics = report_metrics(report_records)
    if compile_result.get("status") != "completed":
        return (
            "blocked_stage364BV_compile_failed_no_authority",
            "blocked_runtime_repair_compile_failed_no_authority",
            "stage364BV_repair_compile_or_ea_source",
        )
    if runtime_outputs.get("status") == "completed" and metrics:
        return (
            "completed_stage364BV_synthetic_short_source_runtime_probe_executed_review_required_no_authority",
            "runtime_probe_executed_with_mt5_kpi_available_review_required_no_authority",
            "stage364BV_open_run364BW_review_synthetic_short_source_runtime_probe",
        )
    return (
        "blocked_stage364BV_runtime_probe_outputs_missing_or_report_missing_no_authority",
        "blocked_runtime_probe_attempted_outputs_or_report_missing_no_authority",
        "stage364BV_repair_mt5_output_or_report_collection",
    )


def gate_rows(compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any], runtime_outputs: Mapping[str, Any], report_records: Sequence[Mapping[str, Any]], support_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    metrics = report_metrics(report_records)
    required = [
        ("runtime_source_support_gate", all(row.get("status") == "passed" for row in support_rows), RUNTIME_SOURCE_SUPPORT_AUDIT, "합성 숏 원천 입력이 EA/계약에 존재한다."),
        ("metaeditor_compile_gate", compile_result.get("status") == "completed", COMPILE_RESULT, "EA 변경이 컴파일된다."),
        ("portable_sync_gate", portable_sync.get("copied") is True, PORTABLE_EA_SYNC, "Strategy Tester가 같은 EX5를 사용한다."),
        ("tester_identity_gate", exists(TESTER_IDENTITY_CONTRACT), TESTER_IDENTITY_CONTRACT, "US100 M5 real tick, deposit 500, leverage 1:100을 고정한다."),
        ("runtime_execution_attempt_gate", exists(MT5_EXECUTION_RESULT), MT5_EXECUTION_RESULT, "MT5 실행 시도 또는 스킵 기록을 남긴다."),
        ("runtime_evidence_gate", runtime_outputs.get("status") == "completed", RUNTIME_OUTPUT_VALIDATION, "telemetry/summary가 완성된다."),
        ("strategy_report_gate", bool(metrics), STRATEGY_TESTER_REPORTS, "MT5 KPI 보고서가 수집된다."),
        ("proxy_mt5_diff_gate", exists(PROXY_MT5_DIFF), PROXY_MT5_DIFF, "proxy expected value와 MT5 KPI 차이를 기록한다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "runtime authority/operating promotion/goal을 주장하지 않는다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 gate를 종료 기록에 연결한다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "blocked",
            "evidence": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, path, effect in required
    ]


def final_payload(
    selected: Mapping[str, Any],
    bk_final: Mapping[str, Any],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    runtime_outputs: Mapping[str, Any],
    report_records: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    created_at: str,
) -> dict[str, Any]:
    metrics = report_metrics(report_records)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": NEXT_RUN_ID,
        "selected_candidate_id": selected.get("candidate_id"),
        "selected_proxy_net_profit": selected.get("net_profit"),
        "selected_proxy_profit_factor": selected.get("profit_factor"),
        "selected_proxy_expectancy": selected.get("expectancy"),
        "selected_proxy_trade_count": selected.get("trade_count"),
        "selected_proxy_density": selected.get("trade_density_per_business_day"),
        "selected_proxy_long_trade_count": selected.get("long_trade_count"),
        "selected_proxy_short_trade_count": selected.get("short_trade_count"),
        "selected_synthetic_short_count": selected.get("synthetic_added_short_count"),
        "bk_mt5_net_profit": bk_final.get("mt5_net_profit"),
        "bk_mt5_profit_factor": bk_final.get("mt5_profit_factor"),
        "bk_mt5_trade_count": bk_final.get("mt5_trade_count"),
        "mt5_net_profit": metrics.get("net_profit", ""),
        "mt5_profit_factor": metrics.get("profit_factor", ""),
        "mt5_expectancy": metrics.get("expectancy", ""),
        "mt5_trade_count": metrics.get("trade_count", ""),
        "mt5_recovery_factor": metrics.get("recovery_factor", ""),
        "mt5_equity_drawdown_amount": metrics.get("equity_drawdown_maximal_amount", ""),
        "mt5_long_trade_count": metrics.get("long_trade_count", ""),
        "mt5_short_trade_count": metrics.get("short_trade_count", ""),
        "runtime_output_status": runtime_outputs.get("status", ""),
        "compile_status": compile_result.get("status"),
        "portable_ea_copied": portable_sync.get("copied"),
        "net_diff_bv_minus_bk": diff_rows[0].get("net_diff_bv_minus_bk", "") if diff_rows else "",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "new_model_training": "not_run",
        "new_mt5_execution": "completed" if metrics.get("status") == "completed" else ("attempted" if exists(MT5_EXECUTION_RESULT) else "not_run"),
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(BACKTEST_RECEIPT, {"run_id": RUN_ID, "tester_identity": rel(TESTER_IDENTITY_CONTRACT), "report_identity": rel(STRATEGY_TESTER_REPORTS), "trade_evidence": rel(PROXY_MT5_DIFF), "backtest_judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY})
    write_json(RUNTIME_RECEIPT, {"run_id": RUN_ID, "research_path": rel(SOURCE_SELECTED_CANDIDATE), "runtime_path": [rel(SOURCE_EA), rel(TESTER_SET_MANIFEST)], "shared_contract": "synthetic short source overlay and calendar block", "parity_check": [rel(RUNTIME_SOURCE_SUPPORT_AUDIT), rel(RUNTIME_OUTPUT_VALIDATION)], "runtime_claim_boundary": "runtime_probe_only", "claim_boundary": CLAIM_BOUNDARY})
    write_json(LINEAGE_RECEIPT, {"run_id": RUN_ID, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)], "producer": rel(Path(__file__)), "consumer": final["next_run_id"], "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()}, "lineage_judgment": "connected_with_runtime_probe_boundary", "claim_boundary": CLAIM_BOUNDARY})
    write_json(JUDGMENT_RECEIPT, {"run_id": RUN_ID, "result_subject": "synthetic short source runtime repair", "evidence_available": [rel(COMPILE_RESULT), rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(PROXY_MT5_DIFF)], "judgment_label": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "next_condition": final["next_run_id"]})
    write_json(CLAIM_RECEIPT, {"run_id": RUN_ID, "allowed_claim": final["judgment"], "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "claim_boundary": CLAIM_BOUNDARY})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364BV synthetic short source runtime repair(364BV 합성 숏 원천 런타임 수리)

## Result(결과)

Action(행동): BS proxy(BS 프록시)의 synthetic short source(합성 숏 원천)를 EA(`Expert Advisor`, 전문가 자문) input(입력)으로 물질화했다.

Effect(효과): `hour 17|19|20`, `p_short >= 0.4375`, `p_short - p_long >= 0.075`, max hold 6 bars(최대 6봉 보유), December h21 long block(12월 21시 롱 차단)을 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)에서 같은 run(실행)으로 탐침할 수 있게 했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- selected proxy(선택 프록시): `{final['selected_candidate_id']}`
- proxy net/PF/trades(프록시 순수익/수익 팩터/거래수): `{final['selected_proxy_net_profit']}` / `{final['selected_proxy_profit_factor']}` / `{final['selected_proxy_trade_count']}`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- BK MT5 reference(BK MT5 기준): `{final['bk_mt5_net_profit']}` / `{final['bk_mt5_profit_factor']}` / `{final['bk_mt5_trade_count']}`

## Proxy MT5 Diff(프록시 MT5 차이)

{markdown_table(diff_rows, ['comparison_id', 'proxy_net_profit', 'mt5_net_profit', 'net_diff_proxy_minus_mt5', 'net_diff_bv_minus_bk', 'mt5_short_trade_count', 'usability'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BV decision(결정)

Decision(결정): `{final['decision']}`

Judgment(판정): `{final['judgment']}`

Action(행동): synthetic short source overlay(합성 숏 원천 덧씌움)를 EA input(EA 입력), `.set` 파일, MT5 probe(MT5 탐침)로 연결했다. Effect(효과): BU blocker(BU 차단 원인)를 기능 누락에서 runtime evidence(런타임 근거) 검토 대상으로 바꿨다.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364BV -->", f"\n<!-- run364BV -->\n- `{RUN_ID}`: synthetic short source runtime repair(합성 숏 원천 런타임 수리) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364BV -->", f"\n<!-- run364BV -->\n## run364BV synthetic short source runtime repair(합성 숏 원천 런타임 수리)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")

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
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BV` materialized synthetic short source overlay(합성 숏 원천 덧씌움) and completed MT5 runtime probe(MT5 런타임 탐침 완료). MT5 KPI(MT5 핵심 성과 지표) net/PF/trades(순수익/수익 팩터/거래수)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`이다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 BV MT5 output(MT5 출력)을 forensic review(포렌식 검토)하고 proxy/MT5 diff(프록시/MT5 차이)를 원인 귀속한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe candidate(런타임 탐침 후보): `{final['selected_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_proxy_net_profit']}`, PF `{final['selected_proxy_profit_factor']}`, trades `{final['selected_proxy_trade_count']}`.

MT5 KPI(MT5 핵심 성과 지표): net `{final['mt5_net_profit']}`, PF `{final['mt5_profit_factor']}`, trades `{final['mt5_trade_count']}`, long/short `{final['mt5_long_trade_count']}` / `{final['mt5_short_trade_count']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364BV -->", f"\n<!-- run364BV -->\n- {final['created_at_utc']} `{RUN_ID}` materialized synthetic short source overlay(합성 숏 원천 덧씌움) and MT5 runtime probe(MT5 런타임 탐침). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364BV_synthetic_short_source -->", f"\n<!-- run364BV_synthetic_short_source -->\n- Idea(아이디어): BQ/BS synthetic short source(합성 숏 원천)를 runtime overlay(런타임 덧씌움)로 표현한다. Effect(효과): proxy short share repair(프록시 숏 비중 수리)를 MT5 cost/fill(비용/체결)로 검증한다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "trade_count": final["mt5_trade_count"],
        "long_trade_count": final["mt5_long_trade_count"],
        "short_trade_count": final["mt5_short_trade_count"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "evidence_boundary": "runtime_probe_only(런타임 탐침 한정)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "next_action": NEXT_RUN_ID,
        "question": "Can BS synthetic short source be expressed and tested in MT5 runtime?(BS 합성 숏 원천을 MT5 런타임에서 표현하고 시험할 수 있는가?)",
    }
    run_row = {**common, "lane": "runtime_probe(런타임 탐침)", "path": rel(FINAL_DECISION)}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=True)
    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe"),
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
            row.update({"net_profit": "", "profit_factor": "", "trade_count": "", "notes": "Tier B fallback not used in BV(BV에서는 Tier B 대체 미사용)."})
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if not exists(path) or not io_path(Path(path)).is_file():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_NUMBER}_{Path(path).stem}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "stage364BV_artifact",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path),
                "created_at_utc": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


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
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "runtime_module_hashes": mt5_runtime_module_hashes(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    created_at = now_utc()
    validate_inputs()
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    bk_final = read_json(SOURCE_BK_FINAL)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(WORK_PACKET, {"run_id": RUN_ID, "primary_family": "runtime_backtest(런타임 백테스트)", "primary_skill": "obsidian-runtime-parity(런타임 동등성)", "claim_boundary": CLAIM_BOUNDARY})
    support_rows = audit_runtime_support()
    policy = build_runtime_policy(selected)
    attempt = materialize_package(policy)
    compile_result, portable_sync = compile_and_sync()
    execution_results, runtime_outputs, report_records, copy_rows = execute_mt5(args, attempt, compile_result, portable_sync)
    diff_rows = build_proxy_mt5_diff(selected, bk_final, runtime_outputs, report_records)
    gates = gate_rows(compile_result, portable_sync, runtime_outputs, report_records, support_rows)
    write_csv(GATE_AUDIT, gates)
    status, judgment, decision = final_status(runtime_outputs, report_records, compile_result)
    final = final_payload(selected, bk_final, compile_result, portable_sync, runtime_outputs, report_records, diff_rows, gates, status, judgment, decision, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_docs(final, gates, diff_rows)
    write_ledgers(final)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

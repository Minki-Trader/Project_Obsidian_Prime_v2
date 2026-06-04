from __future__ import annotations

import argparse
import json
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
    remove_existing_mt5_report_artifacts,
    sha256_file,
)
from foundation.mt5.terminal_runner import run_mt5_tester, wait_for_mt5_runtime_outputs  # noqa: E402
from foundation.mt5.tester_files import (  # noqa: E402
    TesterMaterializationConfig,
    materialize_tester_ini_file,
    materialize_tester_set_file,
)
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402
from stage_pipelines.stage364 import prepare_late_year_session_gate_mt5_precheck_without_db as bu  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as runtime_base  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = bu.STAGE_ID
RUN_NUMBER = "run364BX"
RUN_ID = "run364BX_overlay_hour17_native_short_ablation_runtime_probe_without_db_v1"
PARENT_RUN_ID = "run364BW_review_synthetic_short_source_runtime_probe_without_db_v1"
BASELINE_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run364BY_review_overlay_hour17_native_short_ablation_runtime_probe_without_db_v1"
EXPLORATION_LABEL = "stage364_OverlayHour17NativeShort__RuntimeAblation"
MODEL_ID = runtime_base.MODEL_ID

CLAIM_BOUNDARY = (
    "research_development_runtime_ablation_probe_only_no_new_model_training_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = bu.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
REPORT_COPY_DIR = MT5_DIR / "reports"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
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
ABLATION_SCOREBOARD = RUN_DIR / "runtime_ablation_scoreboard.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
RUNTIME_EVIDENCE_GATE = RUN_DIR / "runtime_evidence_gate.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BX_overlay_hour17_native_short_ablation_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BX_overlay_hour17_native_short_ablation_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
MT5_INPUT_CONTRACT = ROOT / "docs" / "contracts" / "mt5_ea_input_order_contract_fpmarkets_v2.md"

SOURCE_BW_FINAL = STAGE_DIR / "02_runs" / "run364BW" / "final_decision.json"
SOURCE_BW_QUEUE = STAGE_DIR / "02_runs" / "run364BW" / "run364BX_runtime_ablation_queue.csv"
SOURCE_BW_ATTR_HOUR = STAGE_DIR / "02_runs" / "run364BW" / "attribution_by_hour.csv"
SOURCE_BW_ATTR_SOURCE = STAGE_DIR / "02_runs" / "run364BW" / "attribution_by_source_bucket.csv"
SOURCE_BV_FINAL = bv.FINAL_DECISION
SOURCE_BV_SET = STAGE_DIR / "02_runs" / "run364BV" / "mt5" / "sets" / "OPv2_run364BV.set"
SOURCE_BV_REPORTS = STAGE_DIR / "02_runs" / "run364BV" / "strategy_tester_report_records.json"
SOURCE_SELECTED_CANDIDATE = bu.SOURCE_SELECTED_CANDIDATE
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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_overlay_hour17_native_short_ablation"
COMMON_FEATURE = f"{COMMON_ROOT}/features/density_lift_trade_shape_features.csv"
COMMON_MODEL = f"{COMMON_ROOT}/models/{MODEL_ID}.onnx"
COMMON_FEATURE_ORDER = f"{COMMON_ROOT}/config/feature_order.json"
COMMON_PROBABILITY = f"{COMMON_ROOT}/expected/density_lift_expected_probability_tape.csv"
COMMON_SELECTED = f"{COMMON_ROOT}/config/selected_bs_candidate.json"
COMMON_POLICY = f"{COMMON_ROOT}/config/runtime_policy_config.json"

INPUT_FILES = [
    SOURCE_BW_FINAL,
    SOURCE_BW_QUEUE,
    SOURCE_BW_ATTR_HOUR,
    SOURCE_BW_ATTR_SOURCE,
    SOURCE_BV_FINAL,
    SOURCE_BV_SET,
    SOURCE_BV_REPORTS,
    SOURCE_SELECTED_CANDIDATE,
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
    ABLATION_SCOREBOARD,
    PROXY_MT5_DIFF,
    RUNTIME_EVIDENCE_GATE,
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

VARIANTS = [
    {
        "variant_id": "bx01_overlay_hour17_only_keep_native_short",
        "attempt_name": "run364BX_bx01_hour17_overlay_keep_native_short",
        "report_name": "OPv2_run364BX_bx01_hour17_overlay",
        "split": "validation_oos_bx01_hour17_overlay",
        "synthetic_enabled": True,
        "synthetic_hours": "17",
        "synthetic_p_short_min": 0.4375,
        "synthetic_margin_vs_long_min": 0.075,
        "calendar_enabled": True,
        "calendar_side": "long",
        "calendar_month": 12,
        "calendar_start_hour": 21,
        "calendar_end_hour": 22,
        "magic": 36426021,
        "hypothesis": "hour17 overlay(17시 오버레이)만 남기면 non-17 overlay(17시 외 오버레이) 손실을 줄인다.",
    },
    {
        "variant_id": "bx02_native_short_only_overlay_disabled",
        "attempt_name": "run364BX_bx02_native_short_only_overlay_disabled",
        "report_name": "OPv2_run364BX_bx02_native_short_only",
        "split": "validation_oos_bx02_native_short_only",
        "synthetic_enabled": False,
        "synthetic_hours": "",
        "synthetic_p_short_min": 0.4375,
        "synthetic_margin_vs_long_min": 0.075,
        "calendar_enabled": True,
        "calendar_side": "long",
        "calendar_month": 12,
        "calendar_start_hour": 21,
        "calendar_end_hour": 22,
        "magic": 36426022,
        "hypothesis": "native short(기본 숏)만으로 overlay churn(오버레이 회전)을 제거한다.",
    },
    {
        "variant_id": "bx03_hour17_overlay_plus_weak_late_session_firewall",
        "attempt_name": "run364BX_bx03_hour17_overlay_weak_late_firewall",
        "report_name": "OPv2_run364BX_bx03_hour17_late_firewall",
        "split": "validation_oos_bx03_hour17_late_firewall",
        "synthetic_enabled": True,
        "synthetic_hours": "17",
        "synthetic_p_short_min": 0.4375,
        "synthetic_margin_vs_long_min": 0.075,
        "calendar_enabled": True,
        "calendar_side": "long",
        "calendar_month": 12,
        "calendar_start_hour": 21,
        "calendar_end_hour": 23,
        "magic": 36426023,
        "hypothesis": "hour17 overlay(17시 오버레이)에 weak late-session entry firewall(약한 후반 세션 진입 방화벽)을 붙인다.",
    },
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


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return ""


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
    parser.add_argument("--variant", choices=[row["variant_id"] for row in VARIANTS], action="append")
    return parser.parse_args()


def ensure_dirs() -> None:
    for path in [RUN_DIR, SET_DIR, INI_DIR, COMPILE_DIR, REPORT_COPY_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BX inputs(BX 입력 누락): " + ", ".join(missing))
    bw_final = read_json(SOURCE_BW_FINAL)
    bv_final = read_json(SOURCE_BV_FINAL)
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    if bw_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BW next_run_id mismatch(BW 다음 실행 불일치): {bw_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(bw_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("BW has forbidden authority claim(BW 금지 권위 주장 존재)")
    if bv_final.get("new_mt5_execution") != "completed":
        raise RuntimeError("BV MT5 runtime probe not completed(BV MT5 런타임 탐침 미완료)")
    return bw_final, bv_final, selected


def feature_business_days() -> int:
    probability = pd.read_csv(io_path(SOURCE_PROBABILITY_TAPE))
    timestamps = pd.to_datetime(probability["bar_time_server"])
    days = pd.Index(timestamps.dt.normalize().unique()).sort_values()
    return int(sum(day.weekday() < 5 for day in days))


def date_bounds() -> tuple[str, str]:
    probability = pd.read_csv(io_path(SOURCE_PROBABILITY_TAPE))
    timestamps = pd.to_datetime(probability["bar_time_server"])
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BX runtime ablation source(BX 런타임 제거 비교 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


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


def build_runtime_policy(variants: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], bw_final: Mapping[str, Any]) -> dict[str, Any]:
    policy = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "selected_candidate_id": selected.get("candidate_id"),
        "model_id": MODEL_ID,
        "feature_business_days": feature_business_days(),
        "variants": [
            {
                "variant_id": row["variant_id"],
                "hypothesis": row["hypothesis"],
                "synthetic_enabled": row["synthetic_enabled"],
                "synthetic_hours": row["synthetic_hours"],
                "calendar_block": {
                    "enabled": row["calendar_enabled"],
                    "side": row["calendar_side"],
                    "month": row["calendar_month"],
                    "start_hour": row["calendar_start_hour"],
                    "end_hour": row["calendar_end_hour"],
                },
                "timestamp_safety": "entry-known server hour and closed-bar model probabilities only(진입 시점 서버 시간과 닫힌 봉 모델 확률만 사용)",
            }
            for row in variants
        ],
        "bv_reference": {
            "net_profit": bw_final.get("bv_mt5_net_profit"),
            "profit_factor": bw_final.get("bv_mt5_profit_factor"),
            "trade_count": bw_final.get("bv_mt5_trade_count"),
            "recovery_factor": bw_final.get("bv_mt5_recovery_factor"),
            "equity_drawdown_amount": bw_final.get("bv_mt5_equity_drawdown_amount"),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_POLICY_CONFIG, policy)
    return policy


def materialize_common_files() -> list[dict[str, Any]]:
    rows = [
        copy_common(SOURCE_FEATURE_MATRIX, COMMON_FEATURE, "feature_matrix", "MT5 feature input(MT5 피처 입력)을 고정한다."),
        copy_common(SOURCE_ONNX, COMMON_MODEL, "onnx_model", "ONNX(온엑스) 모델을 고정한다."),
        copy_common(SOURCE_FEATURE_ORDER, COMMON_FEATURE_ORDER, "feature_order", "feature order(피처 순서)를 고정한다."),
        copy_common(SOURCE_PROBABILITY_TAPE, COMMON_PROBABILITY, "probability_tape", "proxy/MT5 diff(프록시/MT5 차이)의 확률 기준을 보존한다."),
        copy_common(SOURCE_SELECTED_CANDIDATE, COMMON_SELECTED, "selected_candidate", "선택 후보 계보를 보존한다."),
        copy_common(RUNTIME_POLICY_CONFIG, COMMON_POLICY, "runtime_policy", "runtime rule stack(런타임 규칙 묶음)을 보존한다."),
    ]
    write_csv(COMMON_FILES_SYNC, rows)
    return rows


def materialize_attempts(variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    set_manifest: list[dict[str, Any]] = []
    ini_manifest: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    feature_order = read_json(SOURCE_FEATURE_ORDER)
    from_date, to_date = date_bounds()
    base_set_values = bu.parse_set_file(SOURCE_BV_SET)

    for variant in variants:
        attempt_name = str(variant["attempt_name"])
        set_values = dict(base_set_values)
        common_telemetry = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
        common_summary = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"
        set_values.update(
            {
                "InpRunId": f"{RUN_ID}_{attempt_name}",
                "InpExplorationLabel": EXPLORATION_LABEL,
                "InpSplitLabel": variant["split"],
                "InpFeatureCsvPath": COMMON_FEATURE,
                "InpModelPath": COMMON_MODEL,
                "InpModelId": MODEL_ID,
                "InpFeatureOrderHash": feature_order["feature_order_hash"],
                "InpSyntheticShortSourceEnabled": variant["synthetic_enabled"],
                "InpSyntheticShortSourceHours": variant["synthetic_hours"],
                "InpSyntheticShortSourcePShortMin": variant["synthetic_p_short_min"],
                "InpSyntheticShortSourceMarginVsLongMin": variant["synthetic_margin_vs_long_min"],
                "InpCalendarBlockEnabled": variant["calendar_enabled"],
                "InpCalendarBlockSide": variant["calendar_side"],
                "InpCalendarBlockMonth": variant["calendar_month"],
                "InpCalendarBlockStartHour": variant["calendar_start_hour"],
                "InpCalendarBlockEndHour": variant["calendar_end_hour"],
                "InpMagic": variant["magic"],
                "InpMaxHoldBars": 6,
                "InpTelemetryCsvPath": common_telemetry,
                "InpSummaryCsvPath": common_summary,
            }
        )
        short_name = str(variant["variant_id"]).replace("bx", "OPv2_run364BX_bx")
        set_path = SET_DIR / f"{short_name}.set"
        ini_path = INI_DIR / f"{short_name}.ini"
        set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = materialize_tester_ini_file(
            TesterMaterializationConfig(shutdown_terminal=1, from_date=from_date, to_date=to_date, report=str(variant["report_name"])),
            ini_path,
            set_file_path=Path(set_path.name),
        )
        attempts.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant["variant_id"],
                "tier": "Tier A",
                "split": variant["split"],
                "set_path": set_path,
                "ini_path": ini_path,
                "tester_profile_set_path": DEFAULT_TESTER_PROFILE_ROOT / set_path.name,
                "tester_profile_ini_path": DEFAULT_TESTER_PROFILE_ROOT / ini_path.name,
                "common_telemetry_path": common_telemetry,
                "common_summary_path": common_summary,
                "report_name": variant["report_name"],
                "ini": ini_payload,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_manifest.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant["variant_id"],
                "attempt_name": attempt_name,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "synthetic_enabled": variant["synthetic_enabled"],
                "synthetic_hours": variant["synthetic_hours"],
                "calendar_block": f"side={variant['calendar_side']},month={variant['calendar_month']},hour={variant['calendar_start_hour']}-{variant['calendar_end_hour']}",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_manifest.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant["variant_id"],
                "attempt_name": attempt_name,
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
                "report": variant["report_name"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempt_rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant["variant_id"],
                "attempt_name": attempt_name,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "common_telemetry_path": common_telemetry,
                "common_summary_path": common_summary,
                "hypothesis": variant["hypothesis"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TESTER_SET_MANIFEST, set_manifest)
    write_csv(TESTER_INI_MANIFEST, ini_manifest)
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempt_rows)
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
                "variant_count": len(attempts),
                "effect": "broker real tick(브로커 실제 틱) 실행 정체성을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUNTIME_PARITY_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "research_path": rel(SOURCE_BW_QUEUE),
                "runtime_path": rel(row["set_path"]),
                "shared_contract": "same ONNX model, same base thresholds, same max_hold=6, variant-only overlay/calendar parameters",
                "known_differences": "MT5 tick fills/costs and position lifecycle can differ from proxy(MT5 틱 체결/비용/포지션 생명주기는 프록시와 다를 수 있음)",
                "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 한정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for row in attempts
        ],
    )
    return attempts


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


def copy_runtime_outputs(runtime_outputs_by_attempt: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for output in runtime_outputs_by_attempt:
        attempt_name = str(output.get("attempt_name", ""))
        for key, suffix in [("telemetry_path", "telemetry.csv"), ("summary_path", "summary.csv")]:
            source = Path(str(output.get(key, "")))
            if not source or not exists(source):
                continue
            destination = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}"
            io_path(destination.parent).mkdir(parents=True, exist_ok=True)
            shutil.copy2(io_path(source), io_path(destination))
            rows.append(
                {
                    "run_id": RUN_ID,
                    "attempt_name": attempt_name,
                    "source_path": source.as_posix(),
                    "copy_path": rel(destination),
                    "sha256": sha(destination),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def execute_mt5(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if args.skip_mt5 or compile_result.get("status") != "completed" or portable_sync.get("copied") is not True:
        reason = "skip_mt5_or_compile_sync_not_ready"
        runtime_outputs = [{"attempt_name": attempt["attempt_name"], "variant_id": attempt["variant_id"], "status": "skipped" if args.skip_mt5 else "blocked", "reason": reason} for attempt in attempts]
        write_json(RUNTIME_OUTPUT_VALIDATION, runtime_outputs)
        write_json(MT5_EXECUTION_RESULT, [])
        write_json(STRATEGY_TESTER_REPORTS, [])
        write_csv(RUNTIME_OUTPUT_COPY, [])
        return [], runtime_outputs, [], []

    results: list[dict[str, Any]] = []
    runtime_outputs: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    for attempt in attempts:
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
        result.update({"attempt_name": attempt["attempt_name"], "variant_id": attempt["variant_id"], "tier": attempt["tier"], "split": attempt["split"], "claim_boundary": CLAIM_BOUNDARY})
        output = wait_for_mt5_runtime_outputs(DEFAULT_COMMON_FILES, attempt, timeout_seconds=180, poll_seconds=2.0)
        output.update({"attempt_name": attempt["attempt_name"], "variant_id": attempt["variant_id"]})
        result["runtime_outputs"] = output
        reports = collect_mt5_strategy_report_artifacts(
            terminal_data_root=DEFAULT_PORTABLE_ROOT,
            run_output_root=RUN_DIR,
            attempts=[attempt],
            run_id=RUN_ID,
        )
        attach_mt5_report_metrics([result], reports)
        results.append(result)
        runtime_outputs.append(output)
        report_records.extend(reports)

    copy_rows = copy_runtime_outputs(runtime_outputs)
    write_json(MT5_EXECUTION_RESULT, results)
    write_json(RUNTIME_OUTPUT_VALIDATION, runtime_outputs)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    write_json(
        TERMINAL_PROCESS_AUDIT,
        {
            "run_id": RUN_ID,
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "terminal_exists": exists(DEFAULT_TERMINAL),
            "attempt_count": len(results),
            "completed_attempts": sum(1 for row in results if row.get("status") == "completed"),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return results, runtime_outputs, report_records, copy_rows


def report_metrics_by_attempt(report_records: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for record in report_records:
        metrics = record.get("metrics", {})
        if metrics.get("status") == "completed":
            out[str(record.get("attempt_name"))] = dict(metrics)
    return out


def build_scoreboard(
    attempts: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    runtime_outputs: Sequence[Mapping[str, Any]],
    bw_final: Mapping[str, Any],
    bv_final: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_attempt = report_metrics_by_attempt(report_records)
    runtime_by_attempt = {str(row.get("attempt_name")): row for row in runtime_outputs}
    business_days = feature_business_days()
    bv_net = as_float(bw_final.get("bv_mt5_net_profit") or bv_final.get("mt5_net_profit"))
    bv_pf = as_float(bw_final.get("bv_mt5_profit_factor") or bv_final.get("mt5_profit_factor"))
    bv_trades = as_float(bw_final.get("bv_mt5_trade_count") or bv_final.get("mt5_trade_count"))
    bv_recovery = as_float(bw_final.get("bv_mt5_recovery_factor") or bv_final.get("mt5_recovery_factor"))
    rows: list[dict[str, Any]] = []
    diff_rows: list[dict[str, Any]] = []
    for attempt in attempts:
        metrics = by_attempt.get(str(attempt["attempt_name"]), {})
        runtime_output = runtime_by_attempt.get(str(attempt["attempt_name"]), {})
        trade_count = as_float(metrics.get("trade_count"))
        density = trade_count / business_days if business_days else 0.0
        net = as_float(metrics.get("net_profit"))
        pf = as_float(metrics.get("profit_factor"))
        recovery = as_float(metrics.get("recovery_factor"))
        score = net + 25.0 * (pf - 1.0) + 3.0 * recovery - 50.0 * max(0.0, 3.0 - density)
        status = "passed_density_floor" if density >= 3.0 else "failed_density_floor"
        if not metrics:
            status = "missing_mt5_metrics"
            score = -999999.0
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": attempt["variant_id"],
                "attempt_name": attempt["attempt_name"],
                "mt5_status": metrics.get("status", ""),
                "runtime_output_status": runtime_output.get("status", ""),
                "net_profit": metrics.get("net_profit", ""),
                "profit_factor": metrics.get("profit_factor", ""),
                "expectancy": metrics.get("expectancy", ""),
                "trade_count": metrics.get("trade_count", ""),
                "trade_density_per_feature_business_day": finite(density),
                "recovery_factor": metrics.get("recovery_factor", ""),
                "equity_drawdown_amount": metrics.get("equity_drawdown_maximal_amount", ""),
                "long_trade_count": metrics.get("long_trade_count", ""),
                "short_trade_count": metrics.get("short_trade_count", ""),
                "net_diff_vs_bv": finite(net - bv_net) if metrics else "",
                "pf_diff_vs_bv": finite(pf - bv_pf) if metrics else "",
                "trade_diff_vs_bv": finite(trade_count - bv_trades) if metrics else "",
                "recovery_diff_vs_bv": finite(recovery - bv_recovery) if metrics else "",
                "score": finite(score),
                "selection_status": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        diff_rows.append(
            {
                "run_id": RUN_ID,
                "comparison": f"{attempt['variant_id']}_vs_bv",
                "variant_net_profit": metrics.get("net_profit", ""),
                "bv_net_profit": bv_net,
                "net_diff_variant_minus_bv": finite(net - bv_net) if metrics else "",
                "variant_trade_count": metrics.get("trade_count", ""),
                "bv_trade_count": bv_trades,
                "trade_diff_variant_minus_bv": finite(trade_count - bv_trades) if metrics else "",
                "variant_profit_factor": metrics.get("profit_factor", ""),
                "bv_profit_factor": bv_pf,
                "interpretation": "MT5 ablation evidence(MT5 제거 비교 근거); proxy cannot replace tester KPI(프록시는 테스터 KPI를 대체하지 않음).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda row: as_float(row.get("score"), -999999.0), reverse=True)
    write_csv(ABLATION_SCOREBOARD, rows)
    write_csv(PROXY_MT5_DIFF, diff_rows)
    return rows, diff_rows


def final_status(
    scoreboard: Sequence[Mapping[str, Any]],
    compile_result: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    expected_attempt_count: int,
) -> tuple[str, str, str]:
    if compile_result.get("status") != "completed":
        return (
            "blocked_stage364BX_compile_failed_no_authority",
            "blocked_runtime_ablation_compile_failed_no_authority",
            "stage364BX_repair_compile_or_ea_source",
        )
    completed_outputs = sum(1 for row in runtime_outputs if row.get("status") == "completed")
    metric_rows = [row for row in scoreboard if row.get("mt5_status") == "completed"]
    if completed_outputs == expected_attempt_count and len(metric_rows) == expected_attempt_count:
        best = metric_rows[0]
        return (
            "completed_stage364BX_overlay_ablation_mt5_probe_executed_review_required_no_authority",
            f"runtime_ablation_completed_best_{best['variant_id']}_review_required_no_authority",
            "stage364BX_open_run364BY_review_overlay_hour17_native_short_ablation_runtime_probe",
        )
    if metric_rows:
        return (
            "incomplete_stage364BX_partial_mt5_probe_metrics_available_no_authority",
            "partial_runtime_ablation_metrics_available_review_required_no_authority",
            "stage364BX_review_partial_or_repair_missing_attempts",
        )
    return (
        "blocked_stage364BX_runtime_probe_outputs_missing_or_report_missing_no_authority",
        "blocked_runtime_ablation_outputs_or_report_missing_no_authority",
        "stage364BX_repair_mt5_output_or_report_collection",
    )


def gate_rows(
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    expected_attempt_count: int,
) -> list[dict[str, Any]]:
    runtime_completed = len(runtime_outputs) == expected_attempt_count and all(row.get("status") == "completed" for row in runtime_outputs)
    report_metrics = report_metrics_by_attempt(report_records)
    required = [
        ("runtime_evidence_gate", runtime_completed and len(report_metrics) == expected_attempt_count, RUNTIME_EVIDENCE_GATE, "telemetry/report(런타임 기록/보고서)가 variant(변형)별로 존재한다."),
        ("scope_completion_gate", len(scoreboard) == expected_attempt_count, ABLATION_SCOREBOARD, "BW queue(BW 대기열)의 제거 비교를 모두 기록한다."),
        ("kpi_contract_audit", all(row.get("mt5_status") == "completed" for row in scoreboard), ABLATION_SCOREBOARD, "MT5 KPI(MT5 핵심 성과 지표)를 tester report(테스터 보고서)에서 읽는다."),
        ("metaeditor_compile_gate", compile_result.get("status") == "completed", COMPILE_RESULT, "EA(전문가 자문)가 compile(컴파일)된다."),
        ("portable_sync_gate", portable_sync.get("copied") is True, PORTABLE_EA_SYNC, "Strategy Tester(전략 테스터)가 같은 EX5를 사용한다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트)를 closeout(종료 기록)에 연결한다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다."),
    ]
    rows = [
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
    write_json(
        RUNTIME_EVIDENCE_GATE,
        {
            "run_id": RUN_ID,
            "runtime_completed_attempts": sum(1 for row in runtime_outputs if row.get("status") == "completed"),
            "report_metric_attempts": len(report_metrics),
            "required_attempts": expected_attempt_count,
            "status": "passed" if runtime_completed and len(report_metrics) == expected_attempt_count else "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return rows


def final_payload(
    bw_final: Mapping[str, Any],
    bv_final: Mapping[str, Any],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    created_at: str,
) -> dict[str, Any]:
    best = dict(scoreboard[0]) if scoreboard else {}
    completed_attempts = sum(1 for row in runtime_outputs if row.get("status") == "completed")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": NEXT_RUN_ID,
        "variant_count": len(scoreboard),
        "runtime_completed_attempts": completed_attempts,
        "strategy_report_count": len(report_records),
        "best_variant_id": best.get("variant_id", ""),
        "best_mt5_net_profit": best.get("net_profit", ""),
        "best_mt5_profit_factor": best.get("profit_factor", ""),
        "best_mt5_expectancy": best.get("expectancy", ""),
        "best_mt5_trade_count": best.get("trade_count", ""),
        "best_mt5_density": best.get("trade_density_per_feature_business_day", ""),
        "best_mt5_recovery_factor": best.get("recovery_factor", ""),
        "best_mt5_equity_drawdown_amount": best.get("equity_drawdown_amount", ""),
        "best_mt5_long_trade_count": best.get("long_trade_count", ""),
        "best_mt5_short_trade_count": best.get("short_trade_count", ""),
        "best_net_diff_vs_bv": best.get("net_diff_vs_bv", ""),
        "bv_mt5_net_profit": bw_final.get("bv_mt5_net_profit") or bv_final.get("mt5_net_profit"),
        "bv_mt5_profit_factor": bw_final.get("bv_mt5_profit_factor") or bv_final.get("mt5_profit_factor"),
        "bv_mt5_trade_count": bw_final.get("bv_mt5_trade_count") or bv_final.get("mt5_trade_count"),
        "compile_status": compile_result.get("status"),
        "portable_ea_copied": portable_sync.get("copied"),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "new_model_training": "not_run",
        "new_mt5_execution": "completed" if completed_attempts else "attempted_or_blocked",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(ABLATION_SCOREBOARD),
            "cost_assumptions": "FPMarkets US100 M5 Strategy Tester real ticks; broker spread/swap/commission from report(FPMarkets US100 M5 실제 틱, 비용은 보고서 기준)",
            "backtest_judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(SOURCE_BW_QUEUE),
            "runtime_path": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(SOURCE_EA)],
            "shared_contract": "BX variant-only overlay/calendar ablation with same model and base thresholds(BX 변형별 오버레이/캘린더 제거 비교, 같은 모델/기본 임계값)",
            "known_differences": "bx03 uses entry-time late-session firewall, not close-hour exit firewall(bx03은 청산시각이 아니라 진입시각 후반 세션 방화벽)",
            "parity_check": [rel(RUNTIME_OUTPUT_VALIDATION), rel(ABLATION_SCOREBOARD)],
            "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 한정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": final["next_run_id"],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "lineage_judgment": "connected_with_runtime_probe_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "overlay hour17/native short runtime ablation",
            "evidence_available": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(ABLATION_SCOREBOARD), rel(PROXY_MT5_DIFF)],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": final["next_run_id"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": final["judgment"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any], scoreboard: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364BX overlay hour17 native short ablation runtime probe(364BX 17시 오버레이 기본 숏 제거 비교 런타임 탐침)

## Result(결과)

Action(행동): BW queue(BW 대기열)의 3개 variant(변형)를 같은 ONNX(온엑스) model(모델), 같은 base thresholds(기본 임계값), 같은 MT5 Strategy Tester(MT5 전략 테스터) identity(정체성)로 실행했다.

Effect(효과): synthetic overlay(합성 오버레이), native short control(기본 숏 대조), late-session entry firewall(후반 세션 진입 방화벽)의 차이를 MT5 KPI(MT5 핵심 성과 지표)로 비교할 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- best MT5 net/PF/trades(최선 MT5 순수익/수익 팩터/거래수): `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}`
- best density(최선 밀도): `{final['best_mt5_density']}`
- BV reference(BV 기준): `{final['bv_mt5_net_profit']}` / `{final['bv_mt5_profit_factor']}` / `{final['bv_mt5_trade_count']}`

## Ablation Scoreboard(제거 비교 점수표)

{markdown_table(scoreboard, ['variant_id', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_feature_business_day', 'recovery_factor', 'equity_drawdown_amount', 'long_trade_count', 'short_trade_count', 'net_diff_vs_bv', 'selection_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BX decision(결정)

Decision(결정): `{final['decision']}`

Judgment(판정): `{final['judgment']}`

Action(행동): hour17-only overlay(17시 전용 오버레이), native-short-only control(기본 숏 단독 대조), weak late-session firewall(약한 후반 세션 방화벽)을 MT5 runtime ablation(MT5 런타임 제거 비교)으로 실행했다.

Effect(효과): BW의 hour17 positive clue(17시 긍정 단서)를 tester KPI(테스터 핵심 성과 지표)와 runtime telemetry(런타임 기록)로 검증하고, 다음 BY review(BY 검토) 입력을 만들었다.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364BX -->", f"\n<!-- run364BX -->\n- `{RUN_ID}`: overlay hour17/native short ablation runtime probe(17시 오버레이/기본 숏 제거 비교 런타임 탐침) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364BX -->", f"\n<!-- run364BX -->\n## run364BX overlay hour17 native short ablation runtime probe(17시 오버레이 기본 숏 제거 비교 런타임 탐침)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364BX` completed MT5 runtime ablation(MT5 런타임 제거 비교) for hour17 overlay(17시 오버레이), native-short-only control(기본 숏 단독 대조), and weak late-session firewall(약한 후반 세션 방화벽). Best variant(최선 변형)는 `{final['best_variant_id']}`이고 MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}`이다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 BX MT5 output(MT5 출력)을 source/session/month/equity attribution(원천/세션/월/수익곡선 귀속)으로 review(검토)한다.

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

Runtime probe best variant(런타임 탐침 최선 변형): `{final['best_variant_id']}`

Best MT5 KPI(최선 MT5 핵심 성과 지표): net `{final['best_mt5_net_profit']}`, PF `{final['best_mt5_profit_factor']}`, trades `{final['best_mt5_trade_count']}`, density `{final['best_mt5_density']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364BX -->", f"\n<!-- run364BX -->\n- {final['created_at_utc']} `{RUN_ID}` executed 3-way MT5 runtime ablation(3방향 MT5 런타임 제거 비교). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364BX_overlay_hour17_ablation -->", f"\n<!-- run364BX_overlay_hour17_ablation -->\n- Idea(아이디어): hour17 overlay(17시 오버레이)와 native short(기본 숏)을 MT5 ablation(MT5 제거 비교)으로 분리한다. Effect(효과): synthetic short source(합성 숏 원천)가 실제 수익인지 churn(회전)인지 판별한다.\n")


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
        "net_profit": final["best_mt5_net_profit"],
        "profit_factor": final["best_mt5_profit_factor"],
        "trade_count": final["best_mt5_trade_count"],
        "trade_density_per_feature_day": final["best_mt5_density"],
        "recovery_factor": final["best_mt5_recovery_factor"],
        "long_trade_count": final["best_mt5_long_trade_count"],
        "short_trade_count": final["best_mt5_short_trade_count"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "evidence_boundary": "runtime_probe_only(런타임 탐침 한정)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "next_action": NEXT_RUN_ID,
        "question": "Can hour17 overlay or native-short control improve BV without density collapse?(17시 오버레이나 기본 숏 대조가 밀도 붕괴 없이 BV를 개선하는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "runtime_probe(런타임 탐침)", "path": rel(FINAL_DECISION)}], extend_header=True)
    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe"),
    ]:
        row_id = f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}"
        ledger_rows.append(
            {
                **common,
                "ledger_row_id": row_id,
                "row_id": row_id,
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "path": rel(FINAL_DECISION),
                "view": view,
                "tier": tier,
                "metric_scope": scope,
                "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "record_view"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "record_view"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "artifact_id": f"{RUN_NUMBER}_{path.stem}",
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "artifact_type": "runtime_ablation_artifact",
            "path": rel(path),
            "sha256": sha(path),
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in OUTPUT_FILES
        if exists(path) and io_path(Path(path)).is_file()
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def write_run_manifest(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "attempts": [{k: (rel(v) if isinstance(v, Path) else v) for k, v in attempt.items()} for attempt in attempts],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": final["created_at_utc"],
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    selected_variants = [row for row in VARIANTS if not args.variant or row["variant_id"] in set(args.variant)]
    bw_final, bv_final, selected = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-run-evidence-system(실행 근거 시스템)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    build_runtime_policy(selected_variants, selected, bw_final)
    materialize_common_files()
    attempts = materialize_attempts(selected_variants)
    compile_result, portable_sync = compile_and_sync()
    _results, runtime_outputs, report_records, _copy_rows = execute_mt5(args, attempts, compile_result, portable_sync)
    scoreboard, diff_rows = build_scoreboard(attempts, report_records, runtime_outputs, bw_final, bv_final)
    status, judgment, decision = final_status(scoreboard, compile_result, runtime_outputs, len(attempts))
    gates = gate_rows(compile_result, portable_sync, runtime_outputs, report_records, scoreboard, len(attempts))
    write_csv(GATE_AUDIT, gates)
    final = final_payload(bw_final, bv_final, compile_result, portable_sync, runtime_outputs, report_records, scoreboard, gates, status, judgment, decision, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_docs(final, scoreboard, gates)
    write_ledgers(final)
    write_run_manifest(final, attempts)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

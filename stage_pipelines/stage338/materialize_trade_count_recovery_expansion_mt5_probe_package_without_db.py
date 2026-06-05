from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage338 import materialize_runtime_collapsed_onnx_mt5_probe_package_without_db as g  # noqa: E402
from stage_pipelines.stage338 import review_runtime_collapsed_onnx_mt5_probe_or_repair_without_db as ri  # noqa: E402


aw = ri.aw

TODAY = "2026-06-01"
STAGE_ID = ri.STAGE_ID
STAGE_DIR = ri.STAGE_DIR
RUN_NUMBER = "run338J"
RUN_ID = "run338J_materialize_trade_count_recovery_expansion_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = ri.RUN_ID
NEXT_RUN_ID = "run338K_execute_trade_count_recovery_expansion_mt5_probe_without_db_v1"
STATUS = "completed_stage338J_trade_count_recovery_expansion_mt5_probe_package_materialized_no_selection"
JUDGMENT = "threshold_corridor_mt5_probe_package_ready_runtime_execution_required_no_selection"
DECISION = "stage338J_open_run338K_execute_trade_count_recovery_expansion_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_threshold_corridor_runtime_probe_package_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "feature_matrices"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338J_threshold_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338J_trade_count_recovery_expansion_mt5_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage338/{RUN_NUMBER}_trade_count_recovery_expansion_mt5_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "runtime_collapsed_holdout_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "runtime_feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "trade_count_recovery_expected_probability_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
THRESHOLD_CORRIDOR_PREVIEW = RUN_DIR / "threshold_corridor_proxy_preview.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN338K_EXECUTION_QUEUE = RUN_DIR / "run338K_execution_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

DEFAULT_PORTABLE_ROOT = g.DEFAULT_PORTABLE_ROOT
DEFAULT_TERMINAL = g.DEFAULT_TERMINAL
DEFAULT_COMMON_FILES = g.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = g.DEFAULT_TESTER_PROFILE_ROOT
PORTABLE_EA_EX5 = g.PORTABLE_EA_EX5
EA_SOURCE = g.EA_SOURCE
EA_BINARY = g.EA_BINARY

INPUT_FILES = (
    ri.FINAL_DECISION,
    ri.REPAIR_QUEUE,
    g.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    g.FEATURE_MATRIX,
    g.EXPECTED_PROBABILITY_TAPE,
    g.MODEL_HANDOFF_MANIFEST,
    g.TESTER_IDENTITY_CONTRACT,
    g.RUNTIME_PARITY_CONTRACT,
)

OUTPUT_FILES = (
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    EXPECTED_PROBABILITY_TAPE,
    EXPECTED_PROBABILITY_INDEX,
    THRESHOLD_CORRIDOR_PREVIEW,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUN338K_EXECUTION_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
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
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


@dataclass(frozen=True)
class ThresholdVariant:
    attempt_name: str
    model_id: str
    short_threshold: float
    long_threshold: float
    min_margin: float
    role: str
    magic: int


VARIANTS = (
    ThresholdVariant("j01_p60_m00_ctrl", "logreg_balanced_c025_j01_p60_m00_ctrl", 0.60, 0.60, 0.00, "control_from_run338H", 3387201),
    ThresholdVariant("j02_p55_m00", "logreg_balanced_c025_j02_p55_m00", 0.55, 0.55, 0.00, "trade_count_expansion", 3387202),
    ThresholdVariant("j03_p50_m00", "logreg_balanced_c025_j03_p50_m00", 0.50, 0.50, 0.00, "aggressive_trade_count_expansion", 3387203),
    ThresholdVariant("j04_p55_m05", "logreg_balanced_c025_j04_p55_m05", 0.55, 0.55, 0.05, "margin_control_expansion", 3387204),
)


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return ri.read_csv(path)


def read_json(path: Path) -> Any:
    return ri.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return ri.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return ri.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return ri.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ri.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    ri.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def display_path(path: Path | str) -> str:
    path = Path(path)
    return rel(path) if str(path).lower().startswith(str(ROOT).lower()) else path.as_posix()


def passed_status(series: pd.Series) -> pd.Series:
    return ri.passed_status(series)


def repo_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(io(source), io(target))
    return {
        "sync_id": sync_id,
        "source_path": display_path(source),
        "target_path": display_path(target),
        "exists": exists(target),
        "sha256": sha(target) if exists(target) else "",
        "status": "synced(동기화됨)" if exists(target) else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def decide_label(p_short: float, p_flat: float, p_long: float, variant: ThresholdVariant) -> str:
    short_margin = p_short - max(p_flat, p_long)
    long_margin = p_long - max(p_flat, p_short)
    short_ok = p_short >= variant.short_threshold and short_margin >= variant.min_margin
    long_ok = p_long >= variant.long_threshold and long_margin >= variant.min_margin
    if long_ok and (not short_ok or p_long >= p_short):
        return "long"
    if short_ok:
        return "short"
    return "flat"


def read_parent_context() -> dict[str, Any]:
    parent_final = read_json(ri.FINAL_DECISION)
    parent_gates = read_csv(ri.GATE_AUDIT)
    if parent_final.get("next_action") != RUN_ID:
        raise RuntimeError(f"parent next_action mismatch: {parent_final.get('next_action')} != {RUN_ID}")
    if parent_final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent made a forbidden goal claim")
    g_attempt = read_csv(g.RUNTIME_PROBE_ATTEMPT_PACKAGE).iloc[0].to_dict()
    g_model = read_csv(g.MODEL_HANDOFF_MANIFEST).iloc[0].to_dict()
    return {
        "parent_final": parent_final,
        "parent_gates": parent_gates,
        "source_attempt": g_attempt,
        "source_model": g_model,
    }


def materialize_feature_matrix(source_attempt: Mapping[str, Any]) -> tuple[str, int, int]:
    copy_file(
        g.FEATURE_MATRIX,
        FEATURE_MATRIX,
        "local_feature_matrix",
        "feature matrix(피처 행렬)를 새 package(패키지)에 복사해 산출물 계보를 분리한다.",
    )
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_collapsed_holdout_features.csv"
    copy_file(
        FEATURE_MATRIX,
        DEFAULT_COMMON_FILES / Path(feature_common),
        "common_feature_matrix",
        "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사해 MT5(메타트레이더5)가 읽게 한다.",
    )
    feature_count = int(numeric(source_attempt.get("feature_count")))
    rows = max(0, sum(1 for _ in io(FEATURE_MATRIX).open("r", encoding="utf-8")) - 1)
    manifest = pd.DataFrame(
        [
            {
                "matrix_id": "runtime_collapsed_holdout_features_reused_from_run338G",
                "path": rel(FEATURE_MATRIX),
                "common_path": feature_common,
                "rows": rows,
                "feature_count": feature_count,
                "feature_order_hash": source_attempt.get("feature_order_hash", ""),
                "sha256": sha(FEATURE_MATRIX),
                "source_path": rel(g.FEATURE_MATRIX),
                "timestamp_semantics": "bar close timestamp, InpCsvTimestampIsBarClose=true(봉 마감 시각)",
                "effect": "모델 입력(feature input, 피처 입력)을 바꾸지 않아 threshold(임계값) 효과만 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(FEATURE_MATRIX_MANIFEST, manifest)
    return feature_common, rows, feature_count


def build_expected_tape() -> tuple[pd.DataFrame, pd.DataFrame]:
    source = pd.read_csv(io(g.EXPECTED_PROBABILITY_TAPE)).fillna("")
    expected_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        labels: list[str] = []
        for _, row in source.iterrows():
            p_short = numeric(row.get("p_short"))
            p_flat = numeric(row.get("p_flat"))
            p_long = numeric(row.get("p_long"))
            decision_label = decide_label(p_short, p_flat, p_long, variant)
            labels.append(decision_label)
            expected_rows.append(
                {
                    "attempt_name": variant.attempt_name,
                    "model_id": variant.model_id,
                    "base_model_id": row.get("model_id", "logreg_balanced_c025"),
                    "bar_time": row.get("bar_time", ""),
                    "source_time": row.get("source_time", row.get("bar_time", "")),
                    "source_row_id": row.get("source_row_id", ""),
                    "feature_input_hash": row.get("feature_input_hash", ""),
                    "p_short": p_short,
                    "p_flat": p_flat,
                    "p_long": p_long,
                    "decision_class": {"short": 0, "flat": 1, "long": 2}[decision_label],
                    "decision_label": decision_label,
                    "decision_mode": "threshold_margin(임계값 마진)",
                    "short_threshold": variant.short_threshold,
                    "long_threshold": variant.long_threshold,
                    "min_margin": variant.min_margin,
                    "variant_role": variant.role,
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선택)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        label_counts = pd.Series(labels).value_counts()
        long_count = int(label_counts.get("long", 0))
        short_count = int(label_counts.get("short", 0))
        trade_count = long_count + short_count
        side_balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) else 0.0
        preview_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "variant_role": variant.role,
                "rows": int(len(labels)),
                "signal_trade_count": trade_count,
                "signal_long_count": long_count,
                "signal_short_count": short_count,
                "signal_flat_count": int(label_counts.get("flat", 0)),
                "signal_density": round(trade_count / len(labels), 8) if labels else 0.0,
                "signal_side_balance": round(side_balance, 8),
                "short_threshold": variant.short_threshold,
                "long_threshold": variant.long_threshold,
                "min_margin": variant.min_margin,
                "effect": "MT5(메타트레이더5) 실행 전 신호 밀도와 방향 쏠림을 미리 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    expected = pd.DataFrame(expected_rows)
    preview = pd.DataFrame(preview_rows)
    write_csv(EXPECTED_PROBABILITY_TAPE, expected)
    write_csv(THRESHOLD_CORRIDOR_PREVIEW, preview)
    index_rows = []
    for variant in VARIANTS:
        subset = expected.loc[expected["attempt_name"].eq(variant.attempt_name)]
        index_rows.append(
            {
                "expected_tape_id": f"expected::{variant.attempt_name}",
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "row_count": int(len(subset)),
                "path": rel(EXPECTED_PROBABILITY_TAPE),
                "sha256": sha(EXPECTED_PROBABILITY_TAPE),
                "decision_mode": "threshold_margin(임계값 마진)",
                "short_threshold": variant.short_threshold,
                "long_threshold": variant.long_threshold,
                "min_margin": variant.min_margin,
                "allowed_use": "proxy-vs-MT5 diff(프록시-MT5 차이)",
                "forbidden_use": "operating selection(운영 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_PROBABILITY_INDEX, pd.DataFrame(index_rows))
    return expected, preview


def materialize_attempts(context: Mapping[str, Any], feature_common: str, rows: int, feature_count: int) -> dict[str, pd.DataFrame]:
    source_attempt = context["source_attempt"]
    source_model_path = repo_path(str(source_attempt["model_local_path"]))
    feature_hash = str(source_attempt["feature_order_hash"])
    from_date = str(source_attempt["from_date"])
    to_date = str(source_attempt["to_date"])
    sync_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    tester_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []

    for variant in VARIANTS:
        local_onnx = MODEL_DIR / f"{variant.attempt_name}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{variant.attempt_name}.onnx"
        sync_rows.append(
            copy_file(
                source_model_path,
                local_onnx,
                f"local_onnx::{variant.attempt_name}",
                "ONNX(온엑스) 모델을 threshold variant(임계값 변형)별로 복사해 hash(해시)를 고정한다.",
            )
        )
        sync_rows.append(
            copy_file(
                local_onnx,
                DEFAULT_COMMON_FILES / Path(common_onnx),
                f"common_onnx::{variant.attempt_name}",
                "ONNX(온엑스) 모델을 Common Files(공용 파일)에 복사해 MT5(메타트레이더5)가 읽게 한다.",
            )
        )

        set_name = f"ObsidianPrimeV2_RuntimeProbeEA_{variant.attempt_name}.set"
        ini_name = f"ObsidianPrimeV2_RuntimeProbeEA_{variant.attempt_name}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        report_name = f"POPv2_338J_{variant.attempt_name}"
        set_values = {
            "InpRunId": f"{RUN_ID}_{variant.attempt_name}",
            "InpExplorationLabel": "stage338_TradeCountRecoveryExpansion__ONNX",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "inner_holdout_runtime_collapsed_probe",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": feature_common,
            "InpFeatureCount": feature_count,
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_onnx,
            "InpModelId": variant.model_id,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": feature_hash,
            "InpFallbackEnabled": False,
            "InpShortThreshold": variant.short_threshold,
            "InpLongThreshold": variant.long_threshold,
            "InpMinMargin": variant.min_margin,
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": variant.magic,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": 18,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{variant.attempt_name}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{variant.attempt_name}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=from_date,
                to_date=to_date,
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "base_model_id": "logreg_balanced_c025",
                "source_onnx_path": rel(source_model_path),
                "source_onnx_sha256": sha(source_model_path),
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps([0, 1, 2]),
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "같은 ONNX(온엑스)를 다른 threshold(임계값)로 실행해 모델과 의사결정 표면을 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "variant_role": variant.role,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "decision_mode": "threshold_margin(임계값 마진)",
                "short_threshold": variant.short_threshold,
                "long_threshold": variant.long_threshold,
                "min_margin": variant.min_margin,
                "fixed_lot": 0.10,
                "max_hold_bars": 18,
                "magic": variant.magic,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "expert": tester.get("Expert", ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "model": tester.get("Model", ""),
                "deposit": tester.get("Deposit", ""),
                "leverage": tester.get("Leverage", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempt_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": len(attempt_rows) + 1,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": variant.model_id,
                "base_model_id": "logreg_balanced_c025",
                "feature_set_id": "run338D_training_feature_schema",
                "feature_count": feature_count,
                "feature_order_hash": feature_hash,
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": rel(local_onnx),
                "model_common_path": common_onnx,
                "expected_tape_path": rel(EXPECTED_PROBABILITY_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{variant.attempt_name}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{variant.attempt_name}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": from_date,
                "to_date": to_date,
                "decision_mode": "threshold_margin",
                "short_threshold": variant.short_threshold,
                "long_threshold": variant.long_threshold,
                "min_margin": variant.min_margin,
                "fixed_lot": 0.10,
                "max_hold_bars": 18,
                "variant_role": variant.role,
                "known_proxy_runtime_difference": "proxy signal count(프록시 신호 수) differs from MT5 position lifecycle(MT5 포지션 생명주기)",
                "forbidden_action": "treat package priority as selection or promotion(패키지 우선순위를 선택/승격으로 취급)",
                "effect": "threshold corridor(임계값 구간)를 MT5 runtime probe(MT5 런타임 탐침)로 실행할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_rows.append(
            {
                "contract_id": f"tester_identity::{variant.attempt_name}",
                "attempt_name": variant.attempt_name,
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "expert": tester.get("Expert", ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "deposit": tester.get("Deposit", ""),
                "leverage": tester.get("Leverage", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "effect": "tester identity(테스터 정체성)를 threshold variant(임계값 변형)마다 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        proxy_rows.append(
            {
                "contract_id": f"proxy_mt5_comparison::{variant.attempt_name}",
                "attempt_name": variant.attempt_name,
                "expected_tape": rel(EXPECTED_PROBABILITY_TAPE),
                "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{variant.attempt_name}_telemetry.csv",
                "must_compare": "feature_input_hash, probabilities, decision, trade KPI(피처 입력 해시/확률/판단/거래 KPI)",
                "proxy_scope": "signal sanity and routing only(신호 점검과 라우팅 전용)",
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        runtime_rows.append(
            {
                "contract_id": f"runtime_parity::{variant.attempt_name}",
                "attempt_name": variant.attempt_name,
                "research_path": rel(ri.FINAL_DECISION),
                "runtime_path": rel(set_path),
                "shared_contract": f"features={feature_count};feature_hash={feature_hash};short={variant.short_threshold};long={variant.long_threshold};margin={variant.min_margin}",
                "known_differences": "same ONNX(온엑스), different decision threshold(의사결정 임계값 다름)",
                "parity_check": "run338K must compare telemetry against expected tape(338K에서 런타임 기록과 예상 테이프 비교 필요)",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "effect": "Python(파이썬) 예상 판단과 MT5(메타트레이더5) 판단의 의미를 묶는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    sync_rows.insert(
        0,
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": (DEFAULT_COMMON_FILES / Path(feature_common)).as_posix(),
            "exists": exists(DEFAULT_COMMON_FILES / Path(feature_common)),
            "sha256": sha(DEFAULT_COMMON_FILES / Path(feature_common)) if exists(DEFAULT_COMMON_FILES / Path(feature_common)) else "",
            "status": "synced(동기화됨)" if exists(DEFAULT_COMMON_FILES / Path(feature_common)) else "missing(누락)",
            "effect": "feature matrix(피처 행렬)를 Common Files(공용 파일)에 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    execution_queue = pd.DataFrame(
        [
            {
                "queue_id": "run338K_execute_trade_count_recovery_expansion_mt5_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "attempt_count": len(VARIANTS),
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "terminal_data_root": DEFAULT_PORTABLE_ROOT.as_posix(),
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "required_outputs": "runtime telemetry, tester reports, proxy-vs-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "blocked_if_missing": "terminal, EA, common files handoff, tester output(터미널, EA, 공용 파일 인계, 테스터 출력)",
                "effect": "패키지를 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    tables = {
        "model": pd.DataFrame(model_rows),
        "sync": pd.DataFrame(sync_rows),
        "set": pd.DataFrame(set_rows),
        "ini": pd.DataFrame(ini_rows),
        "attempts": pd.DataFrame(attempt_rows),
        "tester": pd.DataFrame(tester_rows),
        "proxy": pd.DataFrame(proxy_rows),
        "runtime": pd.DataFrame(runtime_rows),
        "queue": execution_queue,
    }
    for path, frame in [
        (MODEL_HANDOFF_MANIFEST, tables["model"]),
        (COMMON_FILES_SYNC, tables["sync"]),
        (TESTER_SET_MANIFEST, tables["set"]),
        (TESTER_INI_MANIFEST, tables["ini"]),
        (RUNTIME_PROBE_ATTEMPT_PACKAGE, tables["attempts"]),
        (TESTER_IDENTITY_CONTRACT, tables["tester"]),
        (PROXY_MT5_COMPARISON_CONTRACT, tables["proxy"]),
        (RUNTIME_PARITY_CONTRACT, tables["runtime"]),
        (RUN338K_EXECUTION_QUEUE, tables["queue"]),
    ]:
        write_csv(path, frame)
    return tables


def build_package() -> dict[str, Any]:
    context = read_parent_context()
    feature_common, rows, feature_count = materialize_feature_matrix(context["source_attempt"])
    expected, preview = build_expected_tape()
    tables = materialize_attempts(context, feature_common, rows, feature_count)
    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": int(len(VARIANTS)),
        "package_rows": int(rows),
        "expected_rows": int(len(expected)),
        "feature_count": int(feature_count),
        "feature_order_hash": context["source_attempt"].get("feature_order_hash", ""),
        "threshold_roles": ";".join(f"{variant.attempt_name}:{variant.role}" for variant in VARIANTS),
        "preview_max_signal_trade_count": int(preview["signal_trade_count"].max()),
        "preview_min_signal_trade_count": int(preview["signal_trade_count"].min()),
        "preview_best_signal_side_balance": float(preview["signal_side_balance"].max()),
        "from_date": context["source_attempt"].get("from_date", ""),
        "to_date": context["source_attempt"].get("to_date", ""),
        "common_sync_missing": int((~tables["sync"]["exists"].astype(bool)).sum()),
        "set_rows": int(len(tables["set"])),
        "ini_rows": int(len(tables["ini"])),
        "terminal_exists": exists(DEFAULT_TERMINAL),
        "common_files_exists": exists(DEFAULT_COMMON_FILES),
        "ea_binary_exists": exists(EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "parent_gate_passed": bool(passed_status(context["parent_gates"]["status"]).all()),
        "parent_goal_achieve": context["parent_final"].get("goal_achieve", "not_claimed"),
        "feature_matrix_sha256": sha(FEATURE_MATRIX),
        "expected_tape_sha256": sha(EXPECTED_PROBABILITY_TAPE),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "effect": "threshold corridor(임계값 구간)를 MT5(메타트레이더5) 실행 가능한 package(패키지)로 만든다.",
    }
    return summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_338I_gates_passed", "passed" if summary["parent_gate_passed"] else "failed", rel(ri.GATE_AUDIT), "run338I(338I 실행) 검토 근거를 이어받는다."),
            gate_row("feature_matrix_reused_without_model_change", "passed" if summary["package_rows"] > 0 and exists(FEATURE_MATRIX) else "failed", rel(FEATURE_MATRIX_MANIFEST), "feature matrix(피처 행렬)를 재사용해 threshold(임계값) 효과만 분리한다."),
            gate_row("threshold_corridor_materialized", "passed" if summary["attempt_count"] >= 3 else "failed", rel(THRESHOLD_CORRIDOR_PREVIEW), "threshold corridor(임계값 구간)를 여러 개 만든다."),
            gate_row("expected_tape_written_for_all_attempts", "passed" if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"] else "failed", rel(EXPECTED_PROBABILITY_INDEX), "각 attempt(시도)의 예상 판단 테이프를 만든다."),
            gate_row("model_and_feature_common_files_synced", "passed" if summary["common_sync_missing"] == 0 else "failed", rel(COMMON_FILES_SYNC), "ONNX/feature(온엑스/피처)를 Common Files(공용 파일)에 동기화한다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["set_rows"] == summary["attempt_count"] and summary["ini_rows"] == summary["attempt_count"] else "failed", rel(TESTER_INI_MANIFEST), "각 attempt(시도)의 Strategy Tester(전략 테스터) 설정을 만든다."),
            gate_row("runtime_parity_contract_written", "passed" if exists(RUNTIME_PARITY_CONTRACT) else "failed", rel(RUNTIME_PARITY_CONTRACT), "Python/MT5 shared contract(공유 계약)를 기록한다."),
            gate_row("tester_identity_visible", "passed" if summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"] else "failed", rel(TESTER_IDENTITY_CONTRACT), "terminal/EA/Common Files(터미널/EA/공용 파일) 가시성을 확인한다."),
            gate_row("run338K_execution_queue_opened", "passed" if exists(RUN338K_EXECUTION_QUEUE) else "failed", rel(RUN338K_EXECUTION_QUEUE), "다음 MT5 execution(MT5 실행) queue(대기열)를 연다."),
            gate_row("no_forbidden_selection_or_goal_claim", "passed", rel(FINAL_DECISION), "package(패키지)를 selection(선정)이나 Goal Achieve(목표 달성)로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 남긴다."),
        ]
    )


def output_paths_that_exist() -> list[Path]:
    return [path for path in OUTPUT_FILES if exists(path)]


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "source_feature_matrix": rel(g.FEATURE_MATRIX),
            "feature_matrix": rel(FEATURE_MATRIX),
            "rows": summary["package_rows"],
            "feature_count": summary["feature_count"],
            "timestamp_semantics": "runtime-collapsed timestamp unique holdout(런타임 축약 시각 고유 홀드아웃)",
            "effect": "데이터를 바꾸지 않고 의사결정 임계값만 바꾸게 한다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_training": "not_run",
            "model_handoff_manifest": rel(MODEL_HANDOFF_MANIFEST),
            "feature_order_hash": summary["feature_order_hash"],
            "threshold_roles": summary["threshold_roles"],
            "effect": "같은 ONNX(온엑스)를 threshold(임계값) 변형으로만 비교한다.",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(EXPECTED_PROBABILITY_TAPE),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "same model artifact(같은 모델 산출물), different thresholds(다른 임계값)",
            "parity_check": "deferred_to_run338K_runtime_telemetry(338K 런타임 기록으로 확인)",
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(
        FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "report_identity": "not_available_until_run338K(338K 전까지 없음)",
            "trade_evidence": "not_available_no_mt5_execution(MT5 실행 없음)",
            "effect": "KPI(핵심 성과 지표)는 다음 MT5(메타트레이더5) 실행에서만 판정한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "package ready(패키지 준비)를 운영 가능 주장으로 바꾸지 않는다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in output_paths_that_exist()],
            "artifact_hashes": {display_path(path): sha(path) for path in output_paths_that_exist()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_package_boundary(패키지 경계로 연결됨)",
            "effect": "run338K(338K 실행)가 어떤 산출물을 실행하는지 추적한다.",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        **dict(summary),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in output_paths_that_exist()],
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338J Trade Count Recovery Expansion MT5 Probe Package(거래수 회복 확장 MT5 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_count']}`
- rows(행): `{final['package_rows']}`
- expected_rows(예상 행): `{final['expected_rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- tester_range(테스터 구간): `{final['from_date']}` to `{final['to_date']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338I(338I 실행)의 positive clue(긍정 단서)를 버리지 않고, 같은 ONNX(온엑스)와 같은 feature matrix(피처 행렬)에 threshold corridor(임계값 구간) 네 개를 물질화했다.

Effect(효과): 모델 학습(model training, 모델 학습) 없이 MT5(메타트레이더5)에서 trade count/recovery(거래수/회복 계수) 개선 여부를 직접 볼 수 있다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `{rel(EXPECTED_PROBABILITY_TAPE)}`
- runtime_path(런타임 경로): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- shared_contract(공유 계약): `{rel(RUNTIME_PARITY_CONTRACT)}`
- parity_check(동등성 검증): run338K(338K 실행) telemetry-vs-expected tape(런타임 기록 대 예상 테이프) 비교가 필요하다.
- runtime_claim_boundary(런타임 주장 경계): runtime_probe_package_only(런타임 탐침 패키지 전용)

## Boundary(경계)

run338J(338J 실행)는 package only(패키지 전용)이다. MT5 execution(MT5 실행), selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338J Decision(338J 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(THRESHOLD_CORRIDOR_PREVIEW)}`, `{rel(TESTER_SET_MANIFEST)}`

Action(행동): threshold corridor(임계값 구간)를 MT5(메타트레이더5) 실행 패키지로 만들었다.

Effect(효과): run338K(338K 실행)가 즉시 Strategy Tester(전략 테스터)와 runtime parity(런타임 동등성)를 검증할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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

run338J(338J 실행)는 threshold corridor(임계값 구간) MT5 package(MT5 패키지)를 만들었다. run338K(338K 실행)는 실제 MT5 runtime probe(MT5 런타임 탐침)를 실행해 trade count/recovery(거래수/회복 계수)를 판정해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{final['attempt_count']}`
- package_rows(패키지 행): `{final['package_rows']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): threshold package(임계값 패키지)를 운영 모델로 오해하지 않게 한다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run338J {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run338J Trade Count Recovery Expansion Package(거래수 회복 확장 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_count']}`
- rows(행): `{final['package_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): threshold corridor(임계값 구간)를 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run338J Trade Count Recovery Expansion Package(거래수 회복 확장 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempt_package(시도 패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- preview(미리보기): `{rel(THRESHOLD_CORRIDOR_PREVIEW)}`
- effect(효과): Stage338(338단계)을 실제 MT5(메타트레이더5) 다중 threshold(임계값) 실행으로 이동시킨다.
""",
    )
    changelog = f"""## {TODAY} run338J Trade Count Recovery Expansion Package(거래수 회복 확장 패키지)

- action(행동): 같은 ONNX(온엑스)와 feature matrix(피처 행렬)에 threshold corridor(임계값 구간) `{final['attempt_count']}`개를 물질화했다.
- effect(효과): trade count/recovery(거래수/회복 계수) 약점을 MT5 runtime probe(MT5 런타임 탐침)로 직접 확인할 수 있게 했다.
- boundary(경계): package only(패키지 전용)이며 selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "mt5_package", "attempt_count": final["attempt_count"], "sample_rows": final["package_rows"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "attempt_count": final["attempt_count"], "sample_rows": final["package_rows"], "result_status": "same_as_tier_a_until_tier_b_available"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[
            ~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))
        ].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    for path in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_DIR, FEATURE_DIR, EXPECTED_DIR, REVIEW_DIR]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338J inputs: {missing}")

    summary = build_package()
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    write_receipts(final)
    final = write_final(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338J gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "attempt_count": final["attempt_count"],
                "package_rows": final["package_rows"],
                "expected_rows": final["expected_rows"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

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
from stage_pipelines.stage338 import materialize_trade_count_recovery_expansion_mt5_probe_package_without_db as prev_pkg  # noqa: E402
from stage_pipelines.stage338 import review_trade_count_recovery_expansion_mt5_probe_without_db as parent_review  # noqa: E402


aw = parent_review.aw

TODAY = "2026-06-01"
STAGE_ID = parent_review.STAGE_ID
STAGE_DIR = parent_review.STAGE_DIR
RUN_NUMBER = "run338M"
RUN_ID = "run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = parent_review.RUN_ID
NEXT_RUN_ID = "run338N_execute_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_without_db_v1"
STATUS = "completed_stage338M_lifecycle_exit_side_balance_recovery_package_materialized_no_selection"
JUDGMENT = "lifecycle_exit_side_balance_mt5_probe_package_ready_runtime_execution_required_no_selection"
DECISION = "stage338M_open_run338N_execute_lifecycle_exit_side_balance_recovery_probe"
CLAIM_BOUNDARY = (
    "research_development_lifecycle_exit_side_balance_runtime_probe_package_only_no_candidate_selection_"
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
REPORT_PATH = REVIEW_DIR / "run338M_lifecycle_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338M_lifecycle_package.md"
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

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage338/{RUN_NUMBER}_lifecycle_exit_side_balance_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_PROBABILITY_INDEX = RUN_DIR / "expected_tape_index.csv"
VARIANT_PREVIEW = RUN_DIR / "lifecycle_variant_preview.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN338N_EXECUTION_QUEUE = RUN_DIR / "run338N_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

DEFAULT_PORTABLE_ROOT = prev_pkg.DEFAULT_PORTABLE_ROOT
DEFAULT_TERMINAL = prev_pkg.DEFAULT_TERMINAL
DEFAULT_COMMON_FILES = prev_pkg.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = prev_pkg.DEFAULT_TESTER_PROFILE_ROOT
PORTABLE_EA_EX5 = prev_pkg.PORTABLE_EA_EX5
EA_BINARY = prev_pkg.EA_BINARY

INPUT_FILES = (
    parent_review.FINAL_DECISION,
    parent_review.NEXT_QUEUE,
    prev_pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    prev_pkg.MODEL_HANDOFF_MANIFEST,
    prev_pkg.FEATURE_MATRIX,
    prev_pkg.EXPECTED_PROBABILITY_TAPE,
)

OUTPUT_FILES = (
    FEATURE_MATRIX,
    FEATURE_MATRIX_MANIFEST,
    EXPECTED_PROBABILITY_TAPE,
    EXPECTED_PROBABILITY_INDEX,
    VARIANT_PREVIEW,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TESTER_IDENTITY_CONTRACT,
    PROXY_MT5_COMPARISON_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUN338N_EXECUTION_QUEUE,
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
class LifecycleVariant:
    attempt_name: str
    model_id: str
    short_threshold: float
    long_threshold: float
    min_margin: float
    max_hold_bars: int
    close_on_flat: bool
    role: str
    magic: int


VARIANTS = (
    LifecycleVariant("m01_p55_h18_base", "logreg_balanced_c025_m01_p55_h18_base", 0.55, 0.55, 0.00, 18, False, "run338L_best_control", 3387301),
    LifecycleVariant("m02_p55_h12", "logreg_balanced_c025_m02_p55_h12", 0.55, 0.55, 0.00, 12, False, "shorter_hold_recovery", 3387302),
    LifecycleVariant("m03_p55_h12_cf", "logreg_balanced_c025_m03_p55_h12_cf", 0.55, 0.55, 0.00, 12, True, "shorter_hold_close_flat", 3387303),
    LifecycleVariant("m04_s55_l50_h18", "logreg_balanced_c025_m04_s55_l50_h18", 0.55, 0.50, 0.00, 18, False, "asymmetric_long_relief", 3387304),
    LifecycleVariant("m05_s55_l50_h12_cf", "logreg_balanced_c025_m05_s55_l50_h12_cf", 0.55, 0.50, 0.00, 12, True, "asymmetric_long_relief_close_flat", 3387305),
    LifecycleVariant("m06_s55_l48_h12_cf", "logreg_balanced_c025_m06_s55_l48_h12_cf", 0.55, 0.48, 0.00, 12, True, "strong_long_relief_close_flat", 3387306),
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
    return parent_review.read_csv(path)


def read_json(path: Path) -> Any:
    return parent_review.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return parent_review.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return parent_review.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return parent_review.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent_review.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    parent_review.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def display_path(path: Path | str) -> str:
    path = Path(path)
    return rel(path) if str(path).lower().startswith(str(ROOT).lower()) else path.as_posix()


def passed_status(series: pd.Series) -> pd.Series:
    return parent_review.passed_status(series)


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


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


def decide_label(p_short: float, p_flat: float, p_long: float, variant: LifecycleVariant) -> str:
    short_margin = p_short - max(p_flat, p_long)
    long_margin = p_long - max(p_flat, p_short)
    short_ok = p_short >= variant.short_threshold and short_margin >= variant.min_margin
    long_ok = p_long >= variant.long_threshold and long_margin >= variant.min_margin
    if long_ok and (not short_ok or p_long >= p_short):
        return "long"
    if short_ok:
        return "short"
    return "flat"


def load_parent() -> dict[str, Any]:
    parent_final = read_json(parent_review.FINAL_DECISION)
    parent_gates = read_csv(parent_review.GATE_AUDIT)
    if parent_final.get("next_action") != RUN_ID:
        raise RuntimeError(f"parent next_action mismatch: {parent_final.get('next_action')} != {RUN_ID}")
    if parent_final.get("goal_achieve") != "not_claimed":
        raise RuntimeError("parent made a forbidden goal claim")
    attempts = read_csv(prev_pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE).fillna("")
    base_attempt = attempts.loc[attempts["attempt_name"].astype(str).eq("j02_p55_m00")]
    if base_attempt.empty:
        raise RuntimeError("base attempt j02_p55_m00 is missing")
    model_manifest = read_csv(prev_pkg.MODEL_HANDOFF_MANIFEST).fillna("")
    base_model = model_manifest.loc[model_manifest["attempt_name"].astype(str).eq("j02_p55_m00")]
    if base_model.empty:
        raise RuntimeError("base model handoff j02_p55_m00 is missing")
    return {
        "parent_final": parent_final,
        "parent_gates": parent_gates,
        "base_attempt": base_attempt.iloc[0].to_dict(),
        "base_model": base_model.iloc[0].to_dict(),
    }


def materialize_feature_matrix(base_attempt: Mapping[str, Any]) -> tuple[str, int, int]:
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    copy_file(prev_pkg.FEATURE_MATRIX, FEATURE_MATRIX, "local_feature_matrix", "feature matrix(피처 행렬)를 새 run(실행)에 복사한다.")
    copy_file(FEATURE_MATRIX, DEFAULT_COMMON_FILES / Path(feature_common), "common_feature_matrix", "feature matrix(피처 행렬)를 Common Files(공용 파일)에 복사한다.")
    rows = max(0, sum(1 for _ in io(FEATURE_MATRIX).open("r", encoding="utf-8")) - 1)
    feature_count = int(numeric(base_attempt.get("feature_count")))
    write_csv(
        FEATURE_MATRIX_MANIFEST,
        pd.DataFrame(
            [
                {
                    "matrix_id": "run338M_runtime_features_reused",
                    "path": rel(FEATURE_MATRIX),
                    "common_path": feature_common,
                    "rows": rows,
                    "feature_count": feature_count,
                    "feature_order_hash": base_attempt.get("feature_order_hash", ""),
                    "sha256": sha(FEATURE_MATRIX),
                    "source_path": rel(prev_pkg.FEATURE_MATRIX),
                    "effect": "data(데이터)를 바꾸지 않고 lifecycle/exit(생명주기/청산) 효과만 분리한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )
    return feature_common, rows, feature_count


def build_expected_tape() -> tuple[pd.DataFrame, pd.DataFrame]:
    source = pd.read_csv(io(prev_pkg.EXPECTED_PROBABILITY_TAPE)).fillna("")
    source = source.loc[source["attempt_name"].astype(str).eq("j02_p55_m00")].copy()
    if source.empty:
        raise RuntimeError("j02 expected tape is empty")
    expected_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        labels: list[str] = []
        for _, row in source.iterrows():
            p_short = numeric(row.get("p_short"))
            p_flat = numeric(row.get("p_flat"))
            p_long = numeric(row.get("p_long"))
            decision = decide_label(p_short, p_flat, p_long, variant)
            labels.append(decision)
            expected_rows.append(
                {
                    "attempt_name": variant.attempt_name,
                    "model_id": variant.model_id,
                    "base_model_id": "logreg_balanced_c025",
                    "bar_time": row.get("bar_time", ""),
                    "source_time": row.get("source_time", row.get("bar_time", "")),
                    "source_row_id": row.get("source_row_id", ""),
                    "feature_input_hash": row.get("feature_input_hash", ""),
                    "p_short": p_short,
                    "p_flat": p_flat,
                    "p_long": p_long,
                    "decision_class": {"short": 0, "flat": 1, "long": 2}[decision],
                    "decision_label": decision,
                    "short_threshold": variant.short_threshold,
                    "long_threshold": variant.long_threshold,
                    "min_margin": variant.min_margin,
                    "max_hold_bars": variant.max_hold_bars,
                    "close_on_flat": variant.close_on_flat,
                    "variant_role": variant.role,
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선택)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        counts = pd.Series(labels).value_counts()
        long_count = int(counts.get("long", 0))
        short_count = int(counts.get("short", 0))
        trade_count = long_count + short_count
        side_balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) else 0.0
        preview_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "variant_role": variant.role,
                "signal_trade_count": trade_count,
                "signal_long_count": long_count,
                "signal_short_count": short_count,
                "signal_flat_count": int(counts.get("flat", 0)),
                "signal_side_balance": round(side_balance, 8),
                "short_threshold": variant.short_threshold,
                "long_threshold": variant.long_threshold,
                "min_margin": variant.min_margin,
                "max_hold_bars": variant.max_hold_bars,
                "close_on_flat": variant.close_on_flat,
                "effect": "MT5(메타트레이더5) 실행 전 side balance(방향 균형)와 lifecycle(생명주기) 변형을 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    expected = pd.DataFrame(expected_rows)
    preview = pd.DataFrame(preview_rows)
    write_csv(EXPECTED_PROBABILITY_TAPE, expected)
    write_csv(VARIANT_PREVIEW, preview)
    write_csv(
        EXPECTED_PROBABILITY_INDEX,
        pd.DataFrame(
            [
                {
                    "attempt_name": variant.attempt_name,
                    "model_id": variant.model_id,
                    "row_count": int(len(expected.loc[expected["attempt_name"].eq(variant.attempt_name)])),
                    "path": rel(EXPECTED_PROBABILITY_TAPE),
                    "sha256": sha(EXPECTED_PROBABILITY_TAPE),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
                for variant in VARIANTS
            ]
        ),
    )
    return expected, preview


def materialize_attempts(context: Mapping[str, Any], feature_common: str, feature_count: int) -> dict[str, pd.DataFrame]:
    base_attempt = context["base_attempt"]
    base_model = context["base_model"]
    source_onnx = Path(str(base_model["local_onnx_path"]))
    source_onnx = source_onnx if source_onnx.is_absolute() else ROOT / source_onnx
    feature_hash = str(base_attempt["feature_order_hash"])
    from_date = str(base_attempt["from_date"])
    to_date = str(base_attempt["to_date"])
    sync_rows: list[dict[str, Any]] = [
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": (DEFAULT_COMMON_FILES / Path(feature_common)).as_posix(),
            "exists": exists(DEFAULT_COMMON_FILES / Path(feature_common)),
            "sha256": sha(DEFAULT_COMMON_FILES / Path(feature_common)) if exists(DEFAULT_COMMON_FILES / Path(feature_common)) else "",
            "status": "synced(동기화됨)" if exists(DEFAULT_COMMON_FILES / Path(feature_common)) else "missing(누락)",
            "effect": "feature matrix(피처 행렬)를 MT5 Common Files(MT5 공용 파일)에 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    model_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    tester_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    for index, variant in enumerate(VARIANTS, start=1):
        local_onnx = MODEL_DIR / f"{variant.attempt_name}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{variant.attempt_name}.onnx"
        sync_rows.append(copy_file(source_onnx, local_onnx, f"local_onnx::{variant.attempt_name}", "ONNX(온엑스)를 lifecycle variant(생명주기 변형)별로 복사한다."))
        sync_rows.append(copy_file(local_onnx, DEFAULT_COMMON_FILES / Path(common_onnx), f"common_onnx::{variant.attempt_name}", "ONNX(온엑스)를 Common Files(공용 파일)에 복사한다."))
        set_name = f"OPV2_Run338M_{variant.attempt_name}.set"
        ini_name = f"OPV2_Run338M_{variant.attempt_name}.ini"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        report_name = f"POPv2_338M_{variant.attempt_name}"
        set_values = {
            "InpRunId": f"{RUN_ID}_{variant.attempt_name}",
            "InpExplorationLabel": "stage338_LifecycleExitSideBalance__ONNX",
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
            "InpCloseOnFlatSignal": variant.close_on_flat,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": variant.max_hold_bars,
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
            mt5.TesterMaterializationConfig(shutdown_terminal=1, from_date=from_date, to_date=to_date, report=report_name),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": variant.attempt_name,
                "model_id": variant.model_id,
                "base_model_id": "logreg_balanced_c025",
                "source_onnx_path": rel(source_onnx),
                "source_onnx_sha256": sha(source_onnx),
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps([0, 1, 2]),
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "같은 ONNX(온엑스)를 lifecycle/exit(생명주기/청산) 변형으로 비교한다.",
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
                "short_threshold": variant.short_threshold,
                "long_threshold": variant.long_threshold,
                "min_margin": variant.min_margin,
                "max_hold_bars": variant.max_hold_bars,
                "close_on_flat": variant.close_on_flat,
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
                "probe_priority": index,
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
                "max_hold_bars": variant.max_hold_bars,
                "close_on_flat": variant.close_on_flat,
                "variant_role": variant.role,
                "effect": "lifecycle/exit(생명주기/청산) 변형을 MT5 runtime probe(MT5 런타임 탐침)로 실행할 수 있게 한다.",
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
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
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
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        runtime_rows.append(
            {
                "contract_id": f"runtime_parity::{variant.attempt_name}",
                "attempt_name": variant.attempt_name,
                "runtime_path": rel(set_path),
                "shared_contract": f"features={feature_count};feature_hash={feature_hash};short={variant.short_threshold};long={variant.long_threshold};hold={variant.max_hold_bars};close_flat={variant.close_on_flat}",
                "parity_check": "run338N telemetry-vs-expected tape(338N 런타임 기록 대 예상 테이프)",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "run338N_execute_lifecycle_exit_side_balance_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "attempt_count": len(VARIANTS),
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "required_outputs": "runtime telemetry, tester reports, proxy-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "effect": "package(패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tables = {
        "sync": pd.DataFrame(sync_rows),
        "model": pd.DataFrame(model_rows),
        "set": pd.DataFrame(set_rows),
        "ini": pd.DataFrame(ini_rows),
        "attempts": pd.DataFrame(attempt_rows),
        "tester": pd.DataFrame(tester_rows),
        "proxy": pd.DataFrame(proxy_rows),
        "runtime": pd.DataFrame(runtime_rows),
        "queue": queue,
    }
    for path, frame in [
        (COMMON_FILES_SYNC, tables["sync"]),
        (MODEL_HANDOFF_MANIFEST, tables["model"]),
        (TESTER_SET_MANIFEST, tables["set"]),
        (TESTER_INI_MANIFEST, tables["ini"]),
        (RUNTIME_PROBE_ATTEMPT_PACKAGE, tables["attempts"]),
        (TESTER_IDENTITY_CONTRACT, tables["tester"]),
        (PROXY_MT5_COMPARISON_CONTRACT, tables["proxy"]),
        (RUNTIME_PARITY_CONTRACT, tables["runtime"]),
        (RUN338N_EXECUTION_QUEUE, tables["queue"]),
    ]:
        write_csv(path, frame)
    return tables


def build_package() -> dict[str, Any]:
    context = load_parent()
    feature_common, rows, feature_count = materialize_feature_matrix(context["base_attempt"])
    expected, preview = build_expected_tape()
    tables = materialize_attempts(context, feature_common, feature_count)
    return {
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
        "preview_max_signal_trade_count": int(preview["signal_trade_count"].max()),
        "preview_best_signal_side_balance": float(preview["signal_side_balance"].max()),
        "common_sync_missing": int((~tables["sync"]["exists"].astype(bool)).sum()),
        "set_rows": int(len(tables["set"])),
        "ini_rows": int(len(tables["ini"])),
        "terminal_exists": exists(DEFAULT_TERMINAL),
        "common_files_exists": exists(DEFAULT_COMMON_FILES),
        "ea_binary_exists": exists(EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "parent_gate_passed": bool(passed_status(context["parent_gates"]["status"]).all()),
        "parent_goal_achieve": context["parent_final"].get("goal_achieve", "not_claimed"),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_338L_gates_passed", "passed" if summary["parent_gate_passed"] else "failed", rel(parent_review.GATE_AUDIT), "run338L(338L 실행) 판정을 이어받는다."),
            gate_row("feature_matrix_reused", "passed" if exists(FEATURE_MATRIX) and summary["package_rows"] > 0 else "failed", rel(FEATURE_MATRIX_MANIFEST), "feature matrix(피처 행렬)를 재사용한다."),
            gate_row("lifecycle_variants_materialized", "passed" if summary["attempt_count"] >= 5 else "failed", rel(VARIANT_PREVIEW), "lifecycle/exit(생명주기/청산) 변형을 만든다."),
            gate_row("expected_tape_written", "passed" if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"] else "failed", rel(EXPECTED_PROBABILITY_INDEX), "예상 판단 테이프(expected tape, 예상 테이프)를 만든다."),
            gate_row("common_files_synced", "passed" if summary["common_sync_missing"] == 0 else "failed", rel(COMMON_FILES_SYNC), "Common Files(공용 파일) 인계를 확인한다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["set_rows"] == summary["attempt_count"] and summary["ini_rows"] == summary["attempt_count"] else "failed", rel(TESTER_INI_MANIFEST), "테스터 설정 파일을 만든다."),
            gate_row("runtime_parity_contract_written", "passed" if exists(RUNTIME_PARITY_CONTRACT) else "failed", rel(RUNTIME_PARITY_CONTRACT), "runtime parity(런타임 동등성) 계약을 남긴다."),
            gate_row("tester_identity_visible", "passed" if summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"] else "failed", rel(TESTER_IDENTITY_CONTRACT), "MT5(메타트레이더5) 실행 가시성을 확인한다."),
            gate_row("run338N_queue_opened", "passed" if exists(RUN338N_EXECUTION_QUEUE) else "failed", rel(RUN338N_EXECUTION_QUEUE), "다음 MT5 실행(run338N, 338N 실행)을 연다."),
            gate_row("no_forbidden_selection_or_goal_claim", "passed", rel(FINAL_DECISION), "패키지를 선정이나 목표 달성으로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 기록한다."),
        ]
    )


def output_paths_that_exist() -> list[Path]:
    return [path for path in OUTPUT_FILES if exists(path)]


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "created_at_utc": now_utc(), "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY}
    write_json(DATA_RECEIPT, {**base, "feature_matrix": rel(FEATURE_MATRIX), "rows": summary["package_rows"], "effect": "데이터를 바꾸지 않고 실행 생명주기만 바꾼다."})
    write_json(MODEL_RECEIPT, {**base, "model_training": "not_run", "model_handoff": rel(MODEL_HANDOFF_MANIFEST), "effect": "같은 ONNX(온엑스)를 재사용한다."})
    write_json(RUNTIME_RECEIPT, {**base, "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "shared_contract": rel(RUNTIME_PARITY_CONTRACT), "parity_check": "deferred_to_run338N(338N으로 연기)"})
    write_json(FORENSICS_RECEIPT, {**base, "tester_identity": rel(TESTER_IDENTITY_CONTRACT), "trade_evidence": "not_available_no_mt5_execution(MT5 실행 없음)"})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"})
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
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {**dict(summary), "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates))}
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
    report = f"""# run338M Lifecycle Exit Side Balance Package(생명주기 청산 방향 균형 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_count']}`
- rows(행): `{final['package_rows']}`
- expected_rows(예상 행): `{final['expected_rows']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

j02_p55_m00 positive seed(긍정 씨앗)를 기반으로 max hold(최대 보유), close on flat(플랫 청산), asymmetric long threshold(비대칭 롱 임계값)를 바꾼 MT5 package(MT5 패키지)를 만들었다.

Effect(효과): threshold(임계값) 자체보다 execution lifecycle(실행 생명주기)이 recovery factor(회복 계수), drawdown(낙폭), side balance(방향 균형)에 주는 영향을 직접 검증할 수 있다.
"""
    decision = f"""# {TODAY} Stage338M Decision(338M 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(VARIANT_PREVIEW)}`, `{rel(TESTER_SET_MANIFEST)}`

Action(행동): lifecycle/exit(생명주기/청산) 변형을 MT5(메타트레이더5) 실행 패키지로 만들었다.

Effect(효과): run338N(338N 실행)이 runtime parity(런타임 동등성)와 MT5 KPI(MT5 핵심 성과 지표)를 바로 확인할 수 있다.

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

run338M(338M 실행)은 lifecycle/exit(생명주기/청산) MT5 package(MT5 패키지)를 만들었다. run338N(338N 실행)은 실제 MT5 runtime probe(MT5 런타임 탐침)를 실행해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{final['attempt_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 패키지 생성을 운영 모델로 오해하지 않게 한다.
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
    marker = f"run338M {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run338M Lifecycle Exit Package(생명주기 청산 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): lifecycle/exit(생명주기/청산) 변형을 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.
""")
    append_text_once(STAGE_README, marker, f"""## run338M Lifecycle Exit Package(생명주기 청산 패키지)

- run_id(실행 ID): `{RUN_ID}`
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- effect(효과): Stage338(338단계)이 threshold(임계값)에서 execution lifecycle(실행 생명주기) 탐색으로 이동한다.
""")
    append_text_once(ROOT_CHANGELOG, marker, f"""## {TODAY} run338M Lifecycle Exit Package(생명주기 청산 패키지)

- action(행동): lifecycle/exit(생명주기/청산) MT5 package(MT5 패키지) `{final['attempt_count']}`개를 만들었다.
- effect(효과): recovery factor(회복 계수), drawdown(낙폭), side balance(방향 균형) 개선을 MT5 runtime probe(MT5 런타임 탐침)로 확인할 수 있게 했다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
""")
    append_text_once(WORKSPACE_CHANGELOG, marker, f"""## {TODAY} run338M Lifecycle Exit Package(생명주기 청산 패키지)

- action(행동): lifecycle/exit(생명주기/청산) MT5 package(MT5 패키지) `{final['attempt_count']}`개를 만들었다.
- effect(효과): recovery factor(회복 계수), drawdown(낙폭), side balance(방향 균형) 개선을 MT5 runtime probe(MT5 런타임 탐침)로 확인할 수 있게 했다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
""")


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
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path):
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": path.suffix.lstrip(".") or "artifact", "path": display_path(path), "sha256": sha(path), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY})
    if rows:
        registry = registry.loc[registry["run_id"].astype(str) != RUN_ID].copy()
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
        raise FileNotFoundError(f"missing run338M inputs: {missing}")
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
        raise RuntimeError(f"run338M gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "attempt_count": final["attempt_count"], "package_rows": final["package_rows"], "expected_rows": final["expected_rows"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "next_run_id": NEXT_RUN_ID, "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

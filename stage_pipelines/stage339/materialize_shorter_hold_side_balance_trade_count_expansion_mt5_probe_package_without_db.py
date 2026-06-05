from __future__ import annotations

import csv
import hashlib
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

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage338 import materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db as source_pkg  # noqa: E402

TODAY = "2026-06-01"

STAGE_ID = "339_runtime_lifecycle_exit__side_balance_probe_review"
SOURCE_STAGE_ID = "338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair"
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID

RUN_NUMBER = "run339C"
RUN_ID = "run339C_materialize_shorter_hold_side_balance_trade_count_expansion_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = "run339B_review_recovered_lifecycle_exit_side_balance_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run339D_execute_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1"

STATUS = "completed_stage339C_shorter_hold_side_balance_trade_count_probe_package_materialized_no_selection"
JUDGMENT = "shorter_hold_side_balance_trade_count_mt5_probe_package_ready_runtime_execution_required_no_selection"
DECISION = "stage339C_open_run339D_execute_shorter_hold_side_balance_trade_count_probe"
CLAIM_BOUNDARY = (
    "research_development_shorter_hold_side_balance_trade_count_runtime_probe_package_only_no_candidate_selection_"
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
REPORT_PATH = REVIEW_DIR / "run339C_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage339C_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run339B"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_QUEUE = PARENT_RUN_DIR / "run339C_queue.csv"
PARENT_SCORECARD = PARENT_RUN_DIR / "lifecycle_exit_probe_scorecard.csv"

SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run338M"
SOURCE_FEATURE_MATRIX = SOURCE_PACKAGE_DIR / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = SOURCE_PACKAGE_DIR / "expected" / "expected_tape.csv"
SOURCE_MODEL_MANIFEST = SOURCE_PACKAGE_DIR / "model_handoff_manifest.csv"
SOURCE_MODEL_PATH = SOURCE_PACKAGE_DIR / "models" / "m02_p55_h12.onnx"
SOURCE_ATTEMPT_PACKAGE = SOURCE_PACKAGE_DIR / "runtime_probe_attempt_package.csv"

DEFAULT_COMMON_FILES = source_pkg.DEFAULT_COMMON_FILES
DEFAULT_TERMINAL = source_pkg.DEFAULT_TERMINAL
DEFAULT_TESTER_PROFILE_ROOT = source_pkg.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = source_pkg.DEFAULT_PORTABLE_ROOT
EA_BINARY = source_pkg.EA_BINARY
PORTABLE_EA_EX5 = source_pkg.PORTABLE_EA_EX5
aw = source_pkg.aw

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage339/{RUN_NUMBER}_shorter_hold_side_balance_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage339_ShorterHoldSideBalance__ONNX"
MAGIC_BASE = 3397400

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_TAPE
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
VARIANT_PREVIEW = RUN_DIR / "variant_preview.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN339D_EXECUTION_QUEUE = RUN_DIR / "run339D_queue.csv"
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

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "report_path",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "view",
    "tier",
    "metric_scope",
    "candidate_model_id",
    "net_profit",
    "profit_factor",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "result_status",
    "sample_rows",
    "feature_count",
    "matched_rows",
    "expectancy",
    "attempt_count",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    frame = read_csv(path) if path.exists() else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=sorted({column for row in rows for column in row}))
    for row in rows:
        for column in row:
            if column not in frame.columns:
                frame[column] = ""
        mask = pd.Series(True, index=frame.index)
        for key in key_columns:
            if key in frame.columns:
                mask &= frame[key].astype(str).eq(str(row.get(key, "")))
            else:
                mask &= False
        frame = frame.loc[~mask].copy()
        frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + [column for row in rows for column in row]))
    write_csv(path, frame[ordered])


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(source, target)
    return {
        "sync_id": sync_id,
        "source_path": rel(source),
        "target_path": rel(target) if str(target).lower().startswith(str(ROOT).lower()) else target.as_posix(),
        "exists": target.exists(),
        "sha256": sha256_file(target) if target.exists() else "",
        "status": "synced(동기화됨)" if target.exists() else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def decide_label(
    p_short: float,
    p_flat: float,
    p_long: float,
    short_threshold: float,
    long_threshold: float,
    min_margin: float = 0.0,
) -> str:
    short_margin = p_short - max(p_flat, p_long)
    long_margin = p_long - max(p_flat, p_short)
    short_ok = p_short >= short_threshold and short_margin >= min_margin
    long_ok = p_long >= long_threshold and long_margin >= min_margin
    if long_ok and (not short_ok or p_long >= p_short):
        return "long"
    if short_ok:
        return "short"
    return "flat"


def load_context() -> tuple[pd.DataFrame, dict[str, Any]]:
    parent = read_json(PARENT_FINAL_DECISION)
    parent_next = parent.get("next_run_id", parent.get("next_action"))
    if parent_next != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent_next} != {RUN_ID}")
    parent_gates = read_csv(PARENT_GATE_AUDIT)
    if not parent_gates["status"].astype(str).str.lower().eq("passed").all():
        raise RuntimeError("parent gate audit has failed rows")
    queue = read_csv(PARENT_QUEUE).fillna("")
    if queue.empty:
        raise RuntimeError("run339C queue is empty")
    return queue, parent


def materialize_feature_matrix() -> tuple[str, int, int, str]:
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    copy_file(SOURCE_FEATURE_MATRIX, FEATURE_MATRIX, "local_feature_matrix", "feature matrix(피처 행렬)를 run339C(339C 실행)로 복사한다.")
    common_target = DEFAULT_COMMON_FILES / Path(feature_common)
    copy_file(FEATURE_MATRIX, common_target, "common_feature_matrix", "feature matrix(피처 행렬)를 MT5 Common Files(MT5 공용 파일)로 복사한다.")
    rows = max(0, sum(1 for _ in FEATURE_MATRIX.open("r", encoding="utf-8-sig")) - 1)
    attempts = read_csv(SOURCE_ATTEMPT_PACKAGE).fillna("")
    feature_count = int(numeric(attempts.iloc[0].get("feature_count"), 0))
    feature_hash = str(attempts.iloc[0].get("feature_order_hash", ""))
    write_csv(
        FEATURE_MATRIX_MANIFEST,
        pd.DataFrame(
            [
                {
                    "matrix_id": "run339C_runtime_features_reused_from_run338M",
                    "path": rel(FEATURE_MATRIX),
                    "common_path": feature_common,
                    "rows": rows,
                    "feature_count": feature_count,
                    "feature_order_hash": feature_hash,
                    "sha256": sha256_file(FEATURE_MATRIX),
                    "source_path": rel(SOURCE_FEATURE_MATRIX),
                    "effect": "data(데이터)를 바꾸지 않고 decision surface(의사결정 표면) 효과만 분리한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )
    return feature_common, rows, feature_count, feature_hash


def build_expected_tape(queue: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    source = read_csv(SOURCE_EXPECTED_TAPE).fillna("")
    source = source.loc[source["attempt_name"].astype(str).eq("m02_p55_h12")].copy()
    if source.empty:
        raise RuntimeError("source expected tape m02_p55_h12 is empty")
    expected_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    for index, variant in queue.reset_index(drop=True).iterrows():
        attempt = str(variant["variant_id"])
        model_id = f"logreg_balanced_c025_{attempt}"
        short_threshold = numeric(variant["short_threshold"])
        long_threshold = numeric(variant["long_threshold"])
        min_margin = numeric(variant.get("min_margin", 0.0), 0.0)
        max_hold = int(numeric(variant["max_hold_bars"]))
        close_on_flat = str(variant["close_on_flat"]).lower() == "true"
        labels: list[str] = []
        for _, row in source.iterrows():
            p_short = numeric(row.get("p_short"))
            p_flat = numeric(row.get("p_flat"))
            p_long = numeric(row.get("p_long"))
            label = decide_label(p_short, p_flat, p_long, short_threshold, long_threshold, min_margin)
            labels.append(label)
            expected_rows.append(
                {
                    "attempt_name": attempt,
                    "model_id": model_id,
                    "base_model_id": "logreg_balanced_c025",
                    "bar_time": row.get("bar_time", ""),
                    "source_time": row.get("source_time", row.get("bar_time", "")),
                    "source_row_id": row.get("source_row_id", ""),
                    "feature_input_hash": row.get("feature_input_hash", ""),
                    "p_short": p_short,
                    "p_flat": p_flat,
                    "p_long": p_long,
                    "decision_class": {"short": 0, "flat": 1, "long": 2}[label],
                    "decision_label": label,
                    "short_threshold": short_threshold,
                    "long_threshold": long_threshold,
                    "min_margin": min_margin,
                    "max_hold_bars": max_hold,
                    "close_on_flat": close_on_flat,
                    "variant_role": variant["variant_role"],
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시 대 MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선정)",
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
                "attempt_name": attempt,
                "model_id": model_id,
                "variant_role": variant["variant_role"],
                "signal_trade_count": trade_count,
                "signal_long_count": long_count,
                "signal_short_count": short_count,
                "signal_flat_count": int(counts.get("flat", 0)),
                "signal_side_balance": round(side_balance, 8),
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "min_margin": min_margin,
                "max_hold_bars": max_hold,
                "close_on_flat": close_on_flat,
                "effect": "MT5(메타트레이더5) 실행 전 trade_count(거래수)와 side_balance(방향 균형) 공급을 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    expected = pd.DataFrame(expected_rows)
    preview = pd.DataFrame(preview_rows)
    write_csv(EXPECTED_TAPE, expected)
    write_csv(VARIANT_PREVIEW, preview)
    write_csv(
        EXPECTED_TAPE_INDEX,
        pd.DataFrame(
            [
                {
                    "attempt_name": row["attempt_name"],
                    "model_id": row["model_id"],
                    "row_count": int(len(expected.loc[expected["attempt_name"].eq(row["attempt_name"])])),
                    "path": rel(EXPECTED_TAPE),
                    "sha256": sha256_file(EXPECTED_TAPE),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
                for _, row in preview.iterrows()
            ]
        ),
    )
    return expected, preview


def materialize_attempts(queue: pd.DataFrame, feature_common: str, feature_count: int, feature_hash: str) -> dict[str, pd.DataFrame]:
    source_model = SOURCE_MODEL_PATH
    source_sha = sha256_file(source_model)
    sync_rows: list[dict[str, Any]] = [
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": (DEFAULT_COMMON_FILES / Path(feature_common)).as_posix(),
            "exists": (DEFAULT_COMMON_FILES / Path(feature_common)).exists(),
            "sha256": sha256_file(DEFAULT_COMMON_FILES / Path(feature_common)) if (DEFAULT_COMMON_FILES / Path(feature_common)).exists() else "",
            "status": "synced(동기화됨)",
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

    for index, variant in queue.reset_index(drop=True).iterrows():
        attempt = str(variant["variant_id"])
        model_id = f"logreg_balanced_c025_{attempt}"
        short_threshold = numeric(variant["short_threshold"])
        long_threshold = numeric(variant["long_threshold"])
        min_margin = numeric(variant.get("min_margin", 0.0), 0.0)
        max_hold = int(numeric(variant["max_hold_bars"]))
        close_on_flat = str(variant["close_on_flat"]).lower() == "true"
        magic = MAGIC_BASE + index + 1
        local_onnx = MODEL_DIR / f"{attempt}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{attempt}.onnx"
        sync_rows.append(copy_file(source_model, local_onnx, f"local_onnx::{attempt}", "ONNX(온엑스)를 변형 이름으로 복사한다."))
        sync_rows.append(copy_file(local_onnx, DEFAULT_COMMON_FILES / Path(common_onnx), f"common_onnx::{attempt}", "ONNX(온엑스)를 MT5 Common Files(MT5 공용 파일)로 복사한다."))
        run_label = RUN_NUMBER.replace("run", "Run", 1)
        report_run_label = RUN_NUMBER.removeprefix("run")
        set_name = f"OPV2_{run_label}_{attempt}.set"
        ini_name = f"OPV2_{run_label}_{attempt}.ini"
        report_name = f"POPv2_{report_run_label}_{attempt}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt}",
            "InpExplorationLabel": EXPLORATION_LABEL,
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
            "InpModelId": model_id,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": feature_hash,
            "InpFallbackEnabled": False,
            "InpShortThreshold": short_threshold,
            "InpLongThreshold": long_threshold,
            "InpMinMargin": min_margin,
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": magic,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": close_on_flat,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": max_hold,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(shutdown_terminal=1, from_date="2024.07.30", to_date="2025.01.01", report=report_name),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": attempt,
                "model_id": model_id,
                "base_model_id": "logreg_balanced_c025",
                "source_onnx_path": rel(source_model),
                "source_onnx_sha256": source_sha,
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha256_file(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha256_file(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps([0, 1, 2]),
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "같은 ONNX(온엑스)를 threshold/exit(임계값/청산) 변형으로 비교한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt,
                "model_id": model_id,
                "variant_role": variant["variant_role"],
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "min_margin": min_margin,
                "max_hold_bars": max_hold,
                "close_on_flat": close_on_flat,
                "magic": magic,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt,
                "model_id": model_id,
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
                "attempt_name": attempt,
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": index + 1,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": model_id,
                "base_model_id": "logreg_balanced_c025",
                "feature_set_id": "run338D_training_feature_schema",
                "feature_count": feature_count,
                "feature_order_hash": feature_hash,
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": rel(local_onnx),
                "model_common_path": common_onnx,
                "expected_tape_path": rel(EXPECTED_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": "2024.07.30",
                "to_date": "2025.01.01",
                "decision_mode": "threshold_margin",
                "short_threshold": short_threshold,
                "long_threshold": long_threshold,
                "min_margin": min_margin,
                "fixed_lot": 0.10,
                "max_hold_bars": max_hold,
                "close_on_flat": close_on_flat,
                "variant_role": variant["variant_role"],
                "effect": "shorter hold(짧은 보유) 수익 단서에 side threshold(방향 임계값) 탐색을 붙인다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_rows.append(
            {
                "contract_id": f"tester_identity::{attempt}",
                "attempt_name": attempt,
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
                "contract_id": f"proxy_mt5_comparison::{attempt}",
                "attempt_name": attempt,
                "expected_tape": rel(EXPECTED_TAPE),
                "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
                "must_compare": "feature_input_hash, probabilities, decision, trade KPI(피처 입력 해시, 확률, 결정, 거래 KPI)",
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        runtime_rows.append(
            {
                "contract_id": f"runtime_parity::{attempt}",
                "attempt_name": attempt,
                "runtime_path": rel(set_path),
                "shared_contract": f"features={feature_count};feature_hash={feature_hash};short={short_threshold};long={long_threshold};min_margin={min_margin};hold={max_hold};close_flat={close_on_flat}",
                "parity_check": "run339D telemetry-vs-expected tape(339D 런타임 기록 대 기대 테이프)",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    queue_out = pd.DataFrame(
        [
            {
                "queue_id": f"{NEXT_RUN_ID}_queue",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "attempt_count": len(queue),
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "required_outputs": "runtime telemetry, tester reports, proxy-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "effect": "run339C(339C 실행) 패키지를 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
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
        "queue": queue_out,
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
        (RUN339D_EXECUTION_QUEUE, tables["queue"]),
    ]:
        write_csv(path, frame)
    return tables


def build_package() -> dict[str, Any]:
    queue, parent = load_context()
    feature_common, rows, feature_count, feature_hash = materialize_feature_matrix()
    expected, preview = build_expected_tape(queue)
    tables = materialize_attempts(queue, feature_common, feature_count, feature_hash)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": int(len(queue)),
        "package_rows": int(rows),
        "expected_rows": int(len(expected)),
        "feature_count": int(feature_count),
        "preview_max_signal_trade_count": int(preview["signal_trade_count"].max()),
        "preview_best_signal_side_balance": float(preview["signal_side_balance"].max()),
        "common_sync_missing": int((~tables["sync"]["exists"].astype(bool)).sum()),
        "set_rows": int(len(tables["set"])),
        "ini_rows": int(len(tables["ini"])),
        "terminal_exists": DEFAULT_TERMINAL.exists(),
        "common_files_exists": DEFAULT_COMMON_FILES.exists(),
        "ea_binary_exists": EA_BINARY.exists(),
        "portable_ea_exists": PORTABLE_EA_EX5.exists(),
        "parent_goal_achieve": parent.get("goal_achieve", "not_claimed"),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def build_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_339B_gates_passed", "passed", rel(PARENT_GATE_AUDIT), "run339B(339B 실행) 검토를 이어받는다."),
            gate_row("feature_matrix_reused", "passed" if FEATURE_MATRIX.exists() and summary["package_rows"] > 0 else "failed", rel(FEATURE_MATRIX_MANIFEST), "feature matrix(피처 행렬)를 재사용한다."),
            gate_row("threshold_variants_materialized", "passed" if summary["attempt_count"] >= 8 else "failed", rel(VARIANT_PREVIEW), "broad/extreme threshold/exit(넓은/극단 임계값/청산) 변형을 만든다."),
            gate_row("expected_tape_written", "passed" if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"] else "failed", rel(EXPECTED_TAPE_INDEX), "expected tape(기대 테이프)를 변형별로 만든다."),
            gate_row("common_files_synced", "passed" if summary["common_sync_missing"] == 0 else "failed", rel(COMMON_FILES_SYNC), "Common Files(공용 파일) 인계를 확인한다."),
            gate_row("tester_set_ini_materialized", "passed" if summary["set_rows"] == summary["attempt_count"] and summary["ini_rows"] == summary["attempt_count"] else "failed", rel(TESTER_INI_MANIFEST), "tester set/ini(테스터 설정 파일)를 만든다."),
            gate_row("runtime_parity_contract_written", "passed" if RUNTIME_PARITY_CONTRACT.exists() else "failed", rel(RUNTIME_PARITY_CONTRACT), "runtime parity(런타임 동등성) 계약을 남긴다."),
            gate_row("tester_identity_visible", "passed" if summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"] else "failed", rel(TESTER_IDENTITY_CONTRACT), "MT5(메타트레이더5) 실행 가시성을 확인한다."),
            gate_row("run339D_queue_opened", "passed" if RUN339D_EXECUTION_QUEUE.exists() else "failed", rel(RUN339D_EXECUTION_QUEUE), "다음 MT5(메타트레이더5) 실행 대기열을 연다."),
            gate_row("no_forbidden_selection_or_goal_claim", "passed", rel(FINAL_DECISION), "패키지를 선정이나 목표 달성으로 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 기록한다."),
        ]
    )


def output_paths() -> list[Path]:
    return [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        VARIANT_PREVIEW,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        TESTER_IDENTITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUNTIME_PARITY_CONTRACT,
        RUN339D_EXECUTION_QUEUE,
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
        Path(__file__),
    ]


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "created_at_utc": now_utc(), "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY}
    write_json(DATA_RECEIPT, {**base, "feature_matrix": rel(FEATURE_MATRIX), "rows": summary["package_rows"], "effect": "data(데이터)를 바꾸지 않고 threshold/exit(임계값/청산)만 바꾼다."})
    write_json(MODEL_RECEIPT, {**base, "model_training": "not_run(실행 안 함)", "model_handoff": rel(MODEL_HANDOFF_MANIFEST), "effect": "같은 ONNX(온엑스)를 재사용한다."})
    write_json(RUNTIME_RECEIPT, {**base, "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "shared_contract": rel(RUNTIME_PARITY_CONTRACT), "parity_check": "deferred_to_run339D(339D 실행으로 연기)"})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run(실행 안 함)", "runtime_authority": "not_claimed(주장 없음)", "operating_promotion": "not_claimed(주장 없음)", "goal_achieve": "not_claimed(주장 없음)"})
    inputs = [PARENT_FINAL_DECISION, PARENT_QUEUE, PARENT_SCORECARD, SOURCE_FEATURE_MATRIX, SOURCE_EXPECTED_TAPE, SOURCE_MODEL_MANIFEST, SOURCE_ATTEMPT_PACKAGE]
    existing_outputs = [path for path in output_paths() if path.exists()]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in inputs],
            "artifact_paths": [rel(path) for path in existing_outputs],
            "artifact_hashes": {rel(path): sha256_file(path) for path in existing_outputs if path.is_file()},
            "consumer": NEXT_RUN_ID,
            "lineage_judgment": "connected_with_boundary(경계가 있는 연결)",
        },
    )
    write_json(RUN_MANIFEST, {**base, "command": "python stage_pipelines/stage339/materialize_shorter_hold_side_balance_trade_count_expansion_mt5_probe_package_without_db.py", "outputs": [rel(path) for path in existing_outputs]})


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run339C Probe Package(탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- feature_rows(피처 행): `{summary['package_rows']}`
- expected_rows(기대 행): `{summary['expected_rows']}`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `{summary['preview_max_signal_trade_count']}`
- preview_best_signal_side_balance(미리보기 최고 신호 방향 균형): `{summary['preview_best_signal_side_balance']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

m02(엠02)의 hold=12(보유 12) positive clue(긍정 단서)를 유지하고 close_on_flat(평탄 청산)을 끈 채 short/long threshold(숏/롱 임계값) `{summary['attempt_count']}`개를 MT5 runtime probe(MT5 런타임 탐침) 패키지로 만들었다.
Effect(효과): profit/recovery(수익/회복)를 잃지 않으면서 trade_count(거래수)와 side_balance(방향 균형)를 넓힐 수 있는지 바로 실행해 볼 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage339C Probe Package Decision(339C 탐침 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): shorter hold side-balance expansion(짧은 보유 방향 균형 확장) MT5(메타트레이더5) 패키지를 만들었다.
Effect(효과): run339D(339D 실행)가 외부 런타임 탐침을 바로 수행할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage339 Selection Status(339단계 선택 상태)

- active_stage(활성 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5(메타트레이더5) 실행 전 패키지를 운영 모델로 오해하지 않게 한다.
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

run339C(339C 실행)는 shorter hold side-balance expansion(짧은 보유 방향 균형 확장) MT5 package(MT5 패키지)를 만들었다. run339D(339D 실행)는 실제 MT5 runtime probe(MT5 런타임 탐침)를 실행해야 한다.

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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = RUN_ID
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run339C Probe Package(339C 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): m02(엠02)의 수익 단서를 side-balance/trade-count(방향 균형/거래수) 확장 패키지로 바꿨다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run339C Probe Package(339C 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): MT5 runtime probe(MT5 런타임 탐침) 실행 준비물을 만들었다.
""",
    )
    changelog = f"""## {TODAY} run339C Probe Package(탐침 패키지)

- action(행동): shorter hold side-balance expansion(짧은 보유 방향 균형 확장) `{summary['attempt_count']}`개 변형을 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run339D(339D 실행)가 trade_count(거래수)와 side_balance(방향 균형) 개선 여부를 외부 런타임에서 검증할 수 있다.
- boundary(경계): package only(패키지 전용), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    final = {**dict(summary), "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()), "gate_total": int(len(gates)), "created_at_utc": now_utc()}
    write_json(FINAL_DECISION, final)


def stage_rows(gates: pd.DataFrame, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
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
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": "logreg_balanced_c025",
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "recovery_factor": "",
        "trade_count": "",
        "result_status": "mt5_probe_package_ready_runtime_execution_required(런타임 실행 필요)",
        "sample_rows": summary["package_rows"],
        "feature_count": summary["feature_count"],
        "matched_rows": "",
        "expectancy": "",
        "attempt_count": summary["attempt_count"],
    }
    rows = []
    for view, tier, scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "mt5_package"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": scope})
        if scope == "missing_required":
            row.update({"candidate_model_id": "", "sample_rows": "", "feature_count": "", "attempt_count": "", "result_status": "missing_required(필수 누락)"})
        rows.append(row)
    return rows


def write_registries(gates: pd.DataFrame, summary: Mapping[str, Any]) -> None:
    rows = stage_rows(gates, summary)
    existing = read_csv(STAGE_LEDGER) if STAGE_LEDGER.exists() else pd.DataFrame(columns=STAGE_LEDGER_COLUMNS)
    existing = existing.loc[~existing["run_id"].astype(str).eq(RUN_ID)].copy() if "run_id" in existing.columns else existing
    stage_frame = pd.concat([existing, pd.DataFrame(rows)], ignore_index=True)
    for column in STAGE_LEDGER_COLUMNS:
        if column not in stage_frame.columns:
            stage_frame[column] = ""
    write_csv(STAGE_LEDGER, stage_frame[STAGE_LEDGER_COLUMNS])
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [rows[0]])
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["record_view"] = row["view"]
        project_row["kpi_scope"] = "runtime_probe_package(런타임 탐침 패키지)"
        project_row["scoreboard_lane"] = "runtime_probe(런타임 탐침)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_row["primary_artifact"] = rel(FINAL_DECISION)
        project_rows.append(project_row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    artifact_rows = []
    for path in output_paths() + [SELECTION_STATUS, WORKSPACE_STATE, CURRENT_WORKING_STATE, STAGE_BRIEF, STAGE_README]:
        if path.exists() and path.is_file():
            artifact_rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": path.suffix.lstrip(".") or "file", "path": rel(path), "sha256": sha256_file(path), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def main() -> None:
    for directory in [RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, MODEL_DIR, FEATURE_DIR, EXPECTED_DIR, REVIEW_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    summary = build_package()
    write_receipts(summary)
    write_docs(summary)
    gates = build_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_final(summary, gates)
    write_registries(gates, summary)
    print(json.dumps({**summary, "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()), "gate_total": int(len(gates))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402


TODAY = "2026-06-01"
STAGE_ID = "348_cash_open_proxy_review__long_oos_gap_short_carry_triage"
SOURCE_STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"

RUN_NUMBER = "run348C"
RUN_ID = "run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1"
PARENT_RUN_ID = "run348B_review_cash_open_asymmetric_proxy_training_without_db_v1"
SOURCE_TRAINING_RUN_ID = "run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run348D_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1"

STATUS = "completed_stage348C_onnx_deployable_short_carry_probe_package_materialized_no_mt5_execution"
JUDGMENT = (
    "runtime_probe_package_ready_feature_order_53_boundary_cash_open_rule_partial_mapping_"
    "mt5_execution_required_no_selection"
)
DECISION = "stage348C_open_run348D_execute_onnx_deployable_short_carry_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_onnx_deployable_short_carry_"
    "feature_order_53_boundary_no_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
PORTABLE_EA_EX5 = (
    DEFAULT_PORTABLE_ROOT
    / "MQL5"
    / "Experts"
    / "Project_Obsidian_Prime_v2"
    / "foundation"
    / "mt5"
    / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
)
EA_SOURCE = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"

REPORT_PATH = REVIEW_DIR / "run348C_onnx_deployable_short_carry_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage348C_onnx_deployable_short_carry_probe_package.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run348B"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
SEED_QUEUE = PARENT_RUN_DIR / "run348C_onnx_deployable_short_probe_seed_queue.csv"
PARENT_SHORT_TRIAGE = PARENT_RUN_DIR / "short_carry_triage.csv"
PARENT_ONNX_REVIEW = PARENT_RUN_DIR / "onnx_deployability_review.csv"
PARENT_USABILITY = PARENT_RUN_DIR / "proxy_mt5_usability_matrix.csv"

SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run347C"
SOURCE_RUN347B_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run347B"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_FEATURE_ORDER = SOURCE_RUN_DIR / "feature_order.csv"
SOURCE_PREDICTIONS = SOURCE_RUN_DIR / "proxy_model_predictions.csv"
SOURCE_MODEL_MANIFEST = SOURCE_RUN_DIR / "model_artifact_manifest.csv"
SOURCE_ONNX_SMOKE = SOURCE_RUN_DIR / "onnx_parity_smoke.csv"
SOURCE_SPLIT_AUDIT = SOURCE_RUN_DIR / "split_audit.csv"
SOURCE_FEATURE_LABEL = SOURCE_RUN347B_DIR / "feature_label_source_table.csv"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage348/{RUN_NUMBER}_onnx_short_carry_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage348_ONNXShortCarry__RuntimeProbePackage"
MAGIC_BASE = 3486000

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
FEATURE_ORDER_CONTRACT = RUN_DIR / "feature_order_contract.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
RUNTIME_MAPPING_AUDIT = RUN_DIR / "runtime_mapping_audit.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUN348D_QUEUE = RUN_DIR / "run348D_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_system_receipt.json"
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
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

CONTRACT_58_FEATURES = [
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
    "return_zscore_20",
    "hl_zscore_50",
    "overnight_return",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]

LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
    "net_profit",
    "profit_factor",
    "expectancy",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "matched_rows",
    "sample_rows",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not exists(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(items: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value) if exists(value) else value.as_posix()
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if hasattr(value, "item"):
        return json_ready(value.item())
    return value


def csv_ready(value: Any) -> Any:
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    return value


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(10_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: csv_ready(row.get(key, "")) for key in fieldnames})


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n")


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), encoding="utf-8-sig", low_memory=False).fillna("")


def source_gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(output):
        return default
    return output


def to_int(value: Any, default: int = 0) -> int:
    return int(round(to_float(value, float(default))))


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(fs_path(source), fs_path(target))
    copied = exists(target)
    return {
        "sync_id": sync_id,
        "source_path": rel(source) if str(source.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else source.as_posix(),
        "target_path": rel(target) if str(target.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else target.as_posix(),
        "exists": copied,
        "sha256": sha256_file(target) if copied else "",
        "status": "synced(동기화됨)" if copied else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def load_feature_order() -> tuple[list[str], str]:
    _fields, rows = read_csv_rows(required(SOURCE_FEATURE_ORDER))
    features = [row["feature_name"] for row in rows if row.get("feature_name")]
    if not features:
        raise RuntimeError("feature order is empty(피처 순서가 비어 있음)")
    return features, ordered_hash(features)


def write_feature_order_contract(feature_order: Sequence[str], feature_hash: str) -> dict[str, Any]:
    missing = [name for name in CONTRACT_58_FEATURES if name not in feature_order]
    extra = [name for name in feature_order if name not in CONTRACT_58_FEATURES]
    row = {
        "contract_id": "stage348C_feature_order_53_runtime_probe_boundary",
        "source_feature_count": len(feature_order),
        "source_feature_order_hash": feature_hash,
        "mt5_contract_feature_count": len(CONTRACT_58_FEATURES),
        "mt5_contract_feature_order_hash": ordered_hash(CONTRACT_58_FEATURES),
        "missing_mt5_contract_features": ";".join(missing),
        "extra_source_features": ";".join(extra),
        "status": "usable_for_probe_package_only(탐침 패키지 전용 사용 가능)",
        "runtime_claim_boundary": "runtime_probe_package_only_not_runtime_authority(런타임 탐침 패키지 전용, 런타임 권위 아님)",
        "effect": "InpFeatureCount(입력 피처 수)를 53으로 고정해 MT5 probe(탐침)는 가능하게 하고, 58-feature authority(58개 피처 권위)는 주장하지 않는다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(FEATURE_ORDER_CONTRACT, [row])
    return row


def split_dates() -> tuple[str, str]:
    frame = read_frame(required(SOURCE_SPLIT_AUDIT))
    all_row = frame.loc[frame["split"].astype(str).eq("all")]
    if all_row.empty:
        raise RuntimeError("split audit all row missing(split 감사 all 행 누락)")
    first_text = str(all_row.iloc[0]["first_bar_time"])
    last_text = str(all_row.iloc[0]["last_bar_time"])
    first_date = datetime.strptime(first_text.split(" ")[0], "%Y.%m.%d")
    last_date = datetime.strptime(last_text.split(" ")[0], "%Y.%m.%d") + timedelta(days=1)
    return first_date.strftime("%Y.%m.%d"), last_date.strftime("%Y.%m.%d")


def materialize_feature_matrix(feature_order: Sequence[str], feature_hash: str) -> tuple[pd.DataFrame, dict[str, Any], str]:
    source = read_frame(required(SOURCE_FEATURE_LABEL))
    predictions = read_frame(required(SOURCE_PREDICTIONS))[["bar_time", "split"]]
    frame = source.merge(predictions, on="bar_time", how="left")
    if frame["split"].astype(str).str.strip().eq("").any():
        raise RuntimeError("split join failed for feature rows(피처 행 split 결합 실패)")
    missing = [name for name in feature_order if name not in frame.columns]
    if missing:
        raise RuntimeError("source feature table missing columns(원천 피처 테이블 컬럼 누락): " + ", ".join(missing))
    duplicate_timestamps = int(frame["bar_time"].duplicated().sum())
    for name in feature_order:
        numeric = pd.to_numeric(frame[name], errors="coerce")
        if numeric.isna().any():
            raise RuntimeError(f"non numeric feature value(숫자 아닌 피처 값): {name}")
        if (~numeric.map(math.isfinite)).any():
            raise RuntimeError(f"non finite feature value(비정상 피처 값): {name}")
        frame[name] = numeric.astype("float32")

    timestamps = pd.to_datetime(frame["bar_time"], format="%Y.%m.%d %H:%M:%S", utc=True)
    output = pd.DataFrame(
        {
            "bar_time_server": frame["bar_time"].astype(str),
            "timestamp_utc": timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "split": frame["split"].astype(str),
            "row_index": range(len(frame)),
        }
    )
    for name in feature_order:
        output[name] = frame[name]
    write_frame(FEATURE_MATRIX, output)
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    common_target = DEFAULT_COMMON_FILES / Path(feature_common)
    copy_file(FEATURE_MATRIX, common_target, "common_feature_matrix", "feature matrix(피처 행렬)를 MT5 Common Files(MT5 공용 파일)에 복사한다.")
    split_counts = frame["split"].value_counts().to_dict()
    manifest = {
        "path": rel(FEATURE_MATRIX),
        "common_path": feature_common,
        "sha256": sha256_file(FEATURE_MATRIX),
        "rows": int(len(frame)),
        "duplicate_timestamps": duplicate_timestamps,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_hash,
        "first_bar_time": str(frame["bar_time"].iloc[0]),
        "last_bar_time": str(frame["bar_time"].iloc[-1]),
        "split_counts": split_counts,
        "timestamp_boundary": "bar_close_time_from_stage347_source(347단계 원천의 봉 마감 시각)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(FEATURE_MATRIX_MANIFEST, [manifest])
    return frame, manifest, feature_common


def seed_short_name(seed: Mapping[str, Any], index: int) -> str:
    family = "logbal" if seed["model_family"] == "logistic_balanced" else "xtrees"
    rule = "cashopen" if seed["allocator_rule"] == "cash_open_regime_allocator" else "balmargin"
    return f"c{index:02d}_{family}_{rule}_q95q90"


def teacher_label(text: Any) -> str:
    raw = str(text).lower()
    if "short" in raw or "숏" in raw:
        return "short"
    if "long" in raw or "롱" in raw:
        return "long"
    return "flat"


def label_class(label: str) -> int:
    return {"short": 0, "flat": 1, "long": 2}[label]


def proxy_allocator_label(
    p_short: float,
    p_flat: float,
    p_long: float,
    long_threshold: float,
    short_threshold: float,
    allocator_rule: str,
    cash_bucket: str,
) -> str:
    del p_flat
    long_pass = p_long >= long_threshold
    short_pass = p_short >= short_threshold
    if allocator_rule == "short_priority":
        if short_pass:
            return "short"
        if long_pass:
            return "long"
        return "flat"
    if allocator_rule == "cash_open_regime_allocator":
        early = "0-30" in cash_bucket or "30-60" in cash_bucket
        if early and short_pass:
            return "short"
        if long_pass and p_long >= p_short:
            return "long"
        if short_pass and p_short > p_long:
            return "short"
        return "flat"
    if long_pass and p_long >= p_short:
        return "long"
    if short_pass and p_short > p_long:
        return "short"
    return "flat"


def ea_threshold_label(
    p_short: float,
    p_flat: float,
    p_long: float,
    short_threshold: float,
    long_threshold: float,
    min_margin: float,
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


def ea_mapped_label(
    p_short: float,
    p_flat: float,
    p_long: float,
    seed: Mapping[str, Any],
    minutes_from_cash_open: float,
) -> str:
    label = ea_threshold_label(
        p_short,
        p_flat,
        p_long,
        to_float(seed["short_probability_threshold"]),
        to_float(seed["long_probability_threshold"]),
        -1.0,
    )
    if seed["allocator_rule"] == "cash_open_regime_allocator" and label == "long":
        if 0.0 <= minutes_from_cash_open <= 60.0:
            return "flat"
    return label


def build_expected_tape(
    source_frame: pd.DataFrame,
    seeds: Sequence[Mapping[str, Any]],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    predictions = read_frame(required(SOURCE_PREDICTIONS))
    merged = source_frame.merge(predictions, on=["bar_time", "split"], how="left", suffixes=("", "_pred"))
    timestamps = pd.to_datetime(merged["bar_time"], format="%Y.%m.%d %H:%M:%S", utc=True)
    rows: list[dict[str, Any]] = []
    mapping_rows: list[dict[str, Any]] = []
    for index, seed in enumerate(seeds, start=1):
        attempt = seed_short_name(seed, index)
        family = str(seed["model_family"])
        p_short_col = f"{family}_allocator_p_short"
        p_flat_col = f"{family}_allocator_p_flat"
        p_long_col = f"{family}_allocator_p_long"
        for column in [p_short_col, p_flat_col, p_long_col]:
            if column not in merged.columns:
                raise RuntimeError(f"missing prediction column(예측 컬럼 누락): {column}")
        proxy_labels: list[str] = []
        ea_labels: list[str] = []
        for row_index, row in merged.iterrows():
            p_short = to_float(row[p_short_col])
            p_flat = to_float(row[p_flat_col])
            p_long = to_float(row[p_long_col])
            proxy_label = proxy_allocator_label(
                p_short,
                p_flat,
                p_long,
                to_float(seed["long_probability_threshold"]),
                to_float(seed["short_probability_threshold"]),
                str(seed["allocator_rule"]),
                str(row.get("cash_open_bucket", "")),
            )
            mapped_label = ea_mapped_label(
                p_short,
                p_flat,
                p_long,
                seed,
                to_float(row.get("minutes_from_cash_open", 0.0)),
            )
            teacher = teacher_label(row.get("allocator_teacher_label", ""))
            proxy_labels.append(proxy_label)
            ea_labels.append(mapped_label)
            rows.append(
                {
                    "attempt_name": attempt,
                    "seed_id": seed["seed_id"],
                    "model_family": family,
                    "allocator_rule": seed["allocator_rule"],
                    "bar_time_server": row["bar_time"],
                    "timestamp_utc": timestamps.iloc[row_index].strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "split": row["split"],
                    "row_index": int(row_index),
                    "p_short": p_short,
                    "p_flat": p_flat,
                    "p_long": p_long,
                    "proxy_intended_label": proxy_label,
                    "ea_mapped_expected_label": mapped_label,
                    "expected_class_id": label_class(mapped_label),
                    "teacher_allocator_label": teacher,
                    "teacher_hit": mapped_label == teacher and mapped_label != "flat",
                    "short_carry_teacher_label": row.get("short_carry_teacher_label", ""),
                    "long_probability_threshold": seed["long_probability_threshold"],
                    "short_probability_threshold": seed["short_probability_threshold"],
                    "runtime_mapping_status": (
                        "partial_cash_open_priority_not_exact(현금장 우선순위 부분 매핑, 완전 재현 아님)"
                        if seed["allocator_rule"] == "cash_open_regime_allocator"
                        else "threshold_rule_mapped_with_expected_tape_audit(임계값 규칙 매핑, 예상 테이프 감사 포함)"
                    ),
                    "allowed_use": "proxy_vs_mt5_runtime_probe_comparison(프록시와 MT5 런타임 탐침 비교)",
                    "forbidden_use": "MT5_KPI_substitute_or_selection(MT5 핵심 성과 지표 대체 또는 선정)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        mismatch_rows = sum(1 for left, right in zip(proxy_labels, ea_labels) if left != right)
        if seed["allocator_rule"] == "cash_open_regime_allocator":
            mapping_judgment = (
                "partial_mapping_current_ea_lacks_cash_open_short_priority_switch"
                "(부분 매핑, 현재 EA에 현금장 숏 우선 전환 없음)"
            )
        elif mismatch_rows == 0:
            mapping_judgment = "mapped_exact_for_threshold_rule(임계값 규칙 기준 재현)"
        else:
            mapping_judgment = (
                "threshold_rule_mapped_with_observed_expected_mismatch"
                "(임계값 규칙 매핑, 관측된 예상 불일치 포함)"
            )
        mapping_rows.append(
            {
                "attempt_name": attempt,
                "seed_id": seed["seed_id"],
                "allocator_rule": seed["allocator_rule"],
                "runtime_decision_mode": "threshold_margin",
                "runtime_min_margin": -1.0,
                "side_filter_enabled": seed["allocator_rule"] == "cash_open_regime_allocator",
                "side_filter_feature_name": "minutes_from_cash_open" if seed["allocator_rule"] == "cash_open_regime_allocator" else "",
                "block_long_range": "0,60" if seed["allocator_rule"] == "cash_open_regime_allocator" else "",
                "proxy_vs_ea_expected_mismatch_rows": mismatch_rows,
                "mapping_judgment": mapping_judgment,
                "effect": "MT5 runtime probe(MT5 런타임 탐침) 뒤 proxy-MT5 diff(프록시-MT5 차이)를 원인별로 나눌 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    expected = pd.DataFrame(rows)
    index_rows: list[dict[str, Any]] = []
    for attempt in expected["attempt_name"].drop_duplicates():
        attempt_frame = expected.loc[expected["attempt_name"].eq(attempt)]
        for split in ["all", "train", "validation", "test"]:
            split_frame = attempt_frame if split == "all" else attempt_frame.loc[attempt_frame["split"].eq(split)]
            if split_frame.empty:
                continue
            counts = split_frame["ea_mapped_expected_label"].value_counts().to_dict()
            proxy_counts = split_frame["proxy_intended_label"].value_counts().to_dict()
            index_rows.append(
                {
                    "attempt_name": attempt,
                    "split": split,
                    "row_count": int(len(split_frame)),
                    "expected_short_count": int(counts.get("short", 0)),
                    "expected_long_count": int(counts.get("long", 0)),
                    "expected_flat_count": int(counts.get("flat", 0)),
                    "proxy_short_count": int(proxy_counts.get("short", 0)),
                    "proxy_long_count": int(proxy_counts.get("long", 0)),
                    "proxy_flat_count": int(proxy_counts.get("flat", 0)),
                    "teacher_hit_rows": int(split_frame["teacher_hit"].astype(bool).sum()),
                    "proxy_vs_ea_mismatch_rows": int(
                        (split_frame["proxy_intended_label"] != split_frame["ea_mapped_expected_label"]).sum()
                    ),
                    "path": rel(EXPECTED_TAPE),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_frame(EXPECTED_TAPE, expected)
    index_frame = pd.DataFrame(index_rows)
    index_frame["expected_tape_sha256"] = sha256_file(EXPECTED_TAPE)
    write_frame(EXPECTED_TAPE_INDEX, index_frame)
    mapping = pd.DataFrame(mapping_rows)
    write_frame(RUNTIME_MAPPING_AUDIT, mapping)
    return expected, index_frame, mapping


def materialize_attempts(
    seeds: Sequence[Mapping[str, Any]],
    feature_common: str,
    feature_order_hash: str,
    feature_count: int,
    from_date: str,
    to_date: str,
) -> dict[str, pd.DataFrame]:
    sync_rows: list[dict[str, Any]] = [
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": (DEFAULT_COMMON_FILES / Path(feature_common)).as_posix(),
            "exists": exists(DEFAULT_COMMON_FILES / Path(feature_common)),
            "sha256": sha256_file(DEFAULT_COMMON_FILES / Path(feature_common))
            if exists(DEFAULT_COMMON_FILES / Path(feature_common))
            else "",
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
    parity_rows: list[dict[str, Any]] = []
    comparison_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []

    for index, seed in enumerate(seeds, start=1):
        attempt = seed_short_name(seed, index)
        source_model = ROOT / str(seed["onnx_path"])
        required(source_model)
        source_sha = sha256_file(source_model)
        if source_sha != str(seed["onnx_sha256"]):
            raise RuntimeError(f"ONNX hash mismatch(온엑스 해시 불일치): {seed['seed_id']}")
        local_model = MODEL_DIR / f"{attempt}.onnx"
        common_model = f"{COMMON_MODEL_DIR}/{attempt}.onnx"
        common_model_path = DEFAULT_COMMON_FILES / Path(common_model)
        sync_rows.append(copy_file(source_model, local_model, f"local_onnx::{attempt}", "ONNX(온엑스)를 run348C 로컬 모델로 복사한다."))
        sync_rows.append(copy_file(local_model, common_model_path, f"common_onnx::{attempt}", "ONNX(온엑스)를 MT5 Common Files(MT5 공용 파일)에 복사한다."))
        model_id = f"stage348C_{attempt}"
        side_filter = seed["allocator_rule"] == "cash_open_regime_allocator"
        set_name = f"OPV2_{RUN_NUMBER}_{attempt}.set"
        ini_name = f"OPV2_{RUN_NUMBER}_{attempt}.ini"
        report_name = f"POPv2_{RUN_NUMBER}_{attempt}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        telemetry_common = f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv"
        summary_common = f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv"
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt}",
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "all_rows_with_test_seed_thresholds",
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
            "InpModelPath": common_model,
            "InpModelId": model_id,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": feature_order_hash,
            "InpFallbackEnabled": False,
            "InpShortThreshold": to_float(seed["short_probability_threshold"]),
            "InpLongThreshold": to_float(seed["long_probability_threshold"]),
            "InpMinMargin": -1.0,
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": side_filter,
            "InpSideFilterFeatureIndex": 37 if side_filter else -1,
            "InpFallbackSideFilterFeatureIndex": 37 if side_filter else -1,
            "InpBlockShortFeatureRange": False,
            "InpBlockShortFeatureMin": 0.0,
            "InpBlockShortFeatureMax": 0.0,
            "InpBlockLongFeatureRange": side_filter,
            "InpBlockLongFeatureMin": 0.0,
            "InpBlockLongFeatureMax": 60.0 if side_filter else 0.0,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": MAGIC_BASE + index,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpExitRiskOverlayEnabled": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": telemetry_common,
            "InpSummaryCsvPath": summary_common,
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
        model_rows.append(
            {
                "attempt_name": attempt,
                "seed_id": seed["seed_id"],
                "model_family": seed["model_family"],
                "model_id": model_id,
                "output_order": "[p_short,p_flat,p_long]",
                "source_onnx_path": rel(source_model),
                "source_onnx_sha256": source_sha,
                "local_onnx_path": rel(local_model),
                "local_onnx_sha256": sha256_file(local_model),
                "common_onnx_path": common_model,
                "common_onnx_sha256": sha256_file(common_model_path),
                "feature_count": feature_count,
                "feature_order_hash": feature_order_hash,
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt,
                "seed_id": seed["seed_id"],
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "short_threshold": seed["short_probability_threshold"],
                "long_threshold": seed["long_probability_threshold"],
                "min_margin": -1.0,
                "side_filter_enabled": side_filter,
                "side_filter_feature_index": 37 if side_filter else -1,
                "side_filter_feature_name": "minutes_from_cash_open" if side_filter else "",
                "block_long_range": "0,60" if side_filter else "",
                "magic": MAGIC_BASE + index,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt,
                "seed_id": seed["seed_id"],
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "set_file": set_name,
                "report_name": report_name,
                "from_date": from_date,
                "to_date": to_date,
                "tester": ini_payload["tester"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempt_rows.append(
            {
                "attempt_name": attempt,
                "seed_id": seed["seed_id"],
                "tier": "Tier A",
                "split": "all_rows_with_test_seed_thresholds",
                "model_family": seed["model_family"],
                "allocator_rule": seed["allocator_rule"],
                "model_id": model_id,
                "model_backend": "onnx",
                "feature_csv_path": feature_common,
                "common_feature_path": feature_common,
                "feature_count": feature_count,
                "feature_order_hash": feature_order_hash,
                "model_common_path": common_model,
                "common_telemetry_path": telemetry_common,
                "common_summary_path": summary_common,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "report_name": report_name,
                "short_threshold": seed["short_probability_threshold"],
                "long_threshold": seed["long_probability_threshold"],
                "min_margin": -1.0,
                "decision_mode": "threshold_margin",
                "side_filter_enabled": side_filter,
                "side_filter_feature_index": 37 if side_filter else -1,
                "side_filter_feature_name": "minutes_from_cash_open" if side_filter else "",
                "block_long_range": "0,60" if side_filter else "",
                "max_hold_bars": 12,
                "fixed_lot": 0.10,
                "magic": MAGIC_BASE + index,
                "from_date": from_date,
                "to_date": to_date,
                "allowed_use": "MT5 runtime probe(MT5 런타임 탐침)",
                "forbidden_use": "candidate_selection_or_operating_claim(후보 선정 또는 운영 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        module_hashes = mt5.mt5_runtime_module_hashes()
        tester_rows.append(
            {
                "attempt_name": attempt,
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "terminal_exists": exists(DEFAULT_TERMINAL),
                "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
                "common_files_exists": exists(DEFAULT_COMMON_FILES),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "tester_profile_root_exists": exists(DEFAULT_TESTER_PROFILE_ROOT),
                "ea_expert_path": mt5.EA_EXPERT_PATH,
                "ea_source_path": rel(EA_SOURCE),
                "ea_source_sha256": sha256_file(EA_SOURCE) if exists(EA_SOURCE) else "",
                "ea_binary_path": rel(EA_BINARY),
                "ea_binary_exists": exists(EA_BINARY),
                "ea_binary_sha256": sha256_file(EA_BINARY) if exists(EA_BINARY) else "",
                "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
                "portable_ea_exists": exists(PORTABLE_EA_EX5),
                "portable_ea_sha256": sha256_file(PORTABLE_EA_EX5) if exists(PORTABLE_EA_EX5) else "",
                "module_hashes": module_hashes,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        parity_rows.append(
            {
                "attempt_name": attempt,
                "research_path": rel(SOURCE_PREDICTIONS),
                "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "shared_contract": "ONNX output order [p_short,p_flat,p_long](온엑스 출력 순서 [숏, 관망, 롱]); closed-bar feature matrix(닫힌 봉 피처 행렬); feature order hash(피처 순서 해시)",
                "known_differences": (
                    "cash_open_regime_allocator partial mapping(현금장 국면 배분기 부분 매핑); "
                    if side_filter
                    else ""
                )
                + "source feature count 53 vs MT5 v2 contract 58(원천 피처 53개, MT5 v2 계약 58개)",
                "parity_check": "expected tape generated; MT5 tester pending run348D(예상 테이프 생성, MT5 테스터는 run348D 대기)",
                "parity_identity": {
                    "model_sha256": source_sha,
                    "feature_order_hash": feature_order_hash,
                    "set_sha256": set_payload["sha256"],
                    "ini_sha256": ini_payload["sha256"],
                    "ea_binary_sha256": sha256_file(EA_BINARY) if exists(EA_BINARY) else "",
                },
                "runtime_claim_boundary": "runtime_probe_package(런타임 탐침 패키지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        comparison_rows.append(
            {
                "attempt_name": attempt,
                "proxy_source": rel(EXPECTED_TAPE),
                "mt5_runtime_source": telemetry_common,
                "comparison_key": "bar_time_server/source_time + model output + decision label(봉 시각/원천 시각 + 모델 출력 + 결정 라벨)",
                "diff_attribution_plan": "feature_time_match, onnx_output_diff, decision_surface_diff, execution_cost_diff(피처 시점 일치, 온엑스 출력 차이, 결정 표면 차이, 실행 비용 차이)",
                "proxy_is_kpi_substitute": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        queue_rows.append(
            {
                "queue_id": f"{RUN_NUMBER}_{attempt}",
                "next_run_id": NEXT_RUN_ID,
                "attempt_name": attempt,
                "seed_id": seed["seed_id"],
                "ini_path": rel(ini_path),
                "set_path": rel(set_path),
                "common_telemetry_path": telemetry_common,
                "common_summary_path": summary_common,
                "action": "execute MT5 Strategy Tester(MT5 전략 테스터 실행)",
                "effect": "collect runtime KPI and proxy-MT5 diff(런타임 핵심 성과 지표와 프록시-MT5 차이 수집)",
                "must_not_claim": "runtime_authority_or_goal_achieve(런타임 권위 또는 목표 달성)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    tables = {
        "sync": pd.DataFrame(sync_rows),
        "models": pd.DataFrame(model_rows),
        "sets": pd.DataFrame(set_rows),
        "inis": pd.DataFrame(ini_rows),
        "attempts": pd.DataFrame(attempt_rows),
        "tester": pd.DataFrame(tester_rows),
        "parity": pd.DataFrame(parity_rows),
        "comparison": pd.DataFrame(comparison_rows),
        "queue": pd.DataFrame(queue_rows),
    }
    write_frame(COMMON_FILES_SYNC, tables["sync"])
    write_frame(MODEL_HANDOFF_MANIFEST, tables["models"])
    write_frame(TESTER_SET_MANIFEST, tables["sets"])
    write_frame(TESTER_INI_MANIFEST, tables["inis"])
    write_frame(RUNTIME_PROBE_ATTEMPT_PACKAGE, tables["attempts"])
    write_frame(TESTER_IDENTITY_CONTRACT, tables["tester"])
    write_frame(RUNTIME_PARITY_CONTRACT, tables["parity"])
    write_frame(PROXY_MT5_COMPARISON_CONTRACT, tables["comparison"])
    write_frame(RUN348D_QUEUE, tables["queue"])
    return tables


def build_summary(
    feature_manifest: Mapping[str, Any],
    feature_contract: Mapping[str, Any],
    seeds: Sequence[Mapping[str, Any]],
    expected: pd.DataFrame,
    mapping: pd.DataFrame,
    tables: Mapping[str, pd.DataFrame],
) -> dict[str, Any]:
    common_sync_missing = int((~tables["sync"]["exists"].astype(bool)).sum())
    model_hash_ok = int((tables["models"]["source_onnx_sha256"] == tables["models"]["local_onnx_sha256"]).sum())
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_training_run_id": SOURCE_TRAINING_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "feature_rows": int(feature_manifest["rows"]),
        "feature_count": int(feature_manifest["feature_count"]),
        "feature_order_hash": feature_manifest["feature_order_hash"],
        "mt5_contract_feature_count": int(feature_contract["mt5_contract_feature_count"]),
        "missing_mt5_contract_feature_count": len(str(feature_contract["missing_mt5_contract_features"]).split(";")),
        "attempt_count": int(len(seeds)),
        "expected_rows": int(len(expected)),
        "expected_tape_index_rows": int(len(expected["attempt_name"].drop_duplicates()) * 4),
        "mapping_rows": int(len(mapping)),
        "cash_open_partial_mapping_attempts": int(mapping["mapping_judgment"].astype(str).str.contains("partial_mapping").sum()),
        "proxy_ea_expected_mismatch_rows": int(mapping["proxy_vs_ea_expected_mismatch_rows"].astype(int).sum()),
        "model_rows": int(len(tables["models"])),
        "model_hash_matched_rows": model_hash_ok,
        "set_rows": int(len(tables["sets"])),
        "ini_rows": int(len(tables["inis"])),
        "common_sync_rows": int(len(tables["sync"])),
        "common_sync_missing": common_sync_missing,
        "runtime_parity_rows": int(len(tables["parity"])),
        "queue_rows": int(len(tables["queue"])),
        "terminal_exists": exists(DEFAULT_TERMINAL),
        "common_files_exists": exists(DEFAULT_COMMON_FILES),
        "ea_binary_exists": exists(EA_BINARY),
        "portable_ea_exists": exists(PORTABLE_EA_EX5),
        "training": "not_run",
        "mt5_execution": "not_run",
        "candidate_selection": "not_claimed",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "pending_run348D_mt5_runtime_probe(run348D MT5 런타임 탐침 대기)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(summary: Mapping[str, Any]) -> None:
    receipt_time = now_utc()
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
            "measurement": {
                "attempt_count": summary["attempt_count"],
                "feature_rows": summary["feature_rows"],
                "expected_rows": summary["expected_rows"],
                "mt5_execution": "not_run",
            },
            "identity": {
                "feature_order_hash": summary["feature_order_hash"],
                "model_handoff_manifest": rel(MODEL_HANDOFF_MANIFEST),
                "tester_set_manifest": rel(TESTER_SET_MANIFEST),
                "tester_ini_manifest": rel(TESTER_INI_MANIFEST),
            },
            "judgment": JUDGMENT,
            "effect": "run348D(348D 실행)가 MT5 runtime probe(MT5 런타임 탐침)를 바로 시도할 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_feature_table": rel(SOURCE_FEATURE_LABEL),
            "feature_rows": summary["feature_rows"],
            "feature_count": summary["feature_count"],
            "timestamp_boundary": "closed-bar source table(닫힌 봉 원천 테이블)",
            "lookahead_bias_check": "no new label or future join created(새 라벨 또는 미래 결합 없음)",
            "known_boundary": "53-feature source differs from MT5 58-feature contract(53개 원천 피처와 MT5 58개 계약 차이)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_onnx_smoke": rel(SOURCE_ONNX_SMOKE),
            "model_rows": summary["model_rows"],
            "model_hash_matched_rows": summary["model_hash_matched_rows"],
            "model_validation_boundary": "source ONNX smoke only, no MT5 runtime authority(원천 ONNX 점검 전용, MT5 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(SOURCE_PREDICTIONS),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": "closed-bar 53 feature matrix and ONNX output [p_short,p_flat,p_long](닫힌 봉 53개 피처 행렬과 온엑스 출력 [숏, 관망, 롱])",
            "known_differences": "feature_count 53 vs contract 58; cash_open rule partial mapping(피처 수 53 대 계약 58, 현금장 규칙 부분 매핑)",
            "parity_check": "expected tape generated; MT5 run pending(예상 테이프 생성, MT5 실행 대기)",
            "parity_identity": rel(RUNTIME_PARITY_CONTRACT),
            "runtime_claim_boundary": "runtime_probe_package(런타임 탐침 패키지)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": [
                "runtime probe package materialized(런타임 탐침 패키지 물질화)",
                "run348D MT5 probe queued(run348D MT5 탐침 대기열 생성)",
            ],
            "forbidden_claims": [
                "candidate selection(후보 선정)",
                "forward pass(전진 통과)",
                "live readiness(실거래 준비)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
            "training": "not_run",
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )


def output_paths() -> list[Path]:
    return [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        FEATURE_ORDER_CONTRACT,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        RUNTIME_MAPPING_AUDIT,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        TESTER_IDENTITY_CONTRACT,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        RUNTIME_PARITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUN348D_QUEUE,
        RUN_EVIDENCE_RECEIPT,
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
        CURRENT_WORKING_STATE,
        WORKSPACE_STATE,
        SELECTION_STATUS,
        ROOT_SELECTION_STATUS,
        Path(__file__),
    ]


def write_lineage_receipt() -> None:
    existing_outputs = [path for path in output_paths() if exists(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in existing_outputs],
            "artifact_hashes": {rel(path): sha256_file(path) for path in existing_outputs if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적됨 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_runtime_package_boundary(런타임 패키지 경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def build_gates(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        (
            "parent_run348B_gates_passed",
            source_gate_passed(PARENT_GATE_AUDIT),
            PARENT_GATE_AUDIT,
            "run348B(348B 실행)의 review gate(검토 게이트)를 이어받았다.",
        ),
        (
            "source_run347C_gates_passed",
            source_gate_passed(SOURCE_GATE_AUDIT),
            SOURCE_GATE_AUDIT,
            "run347C(347C 실행)의 training gate(학습 게이트)를 확인했다.",
        ),
        (
            "seed_queue_loaded",
            int(summary["attempt_count"]) == 4,
            SEED_QUEUE,
            "ONNX deployable short-carry seed(온엑스 배포 가능 숏 기여 씨앗) 4개를 로드했다.",
        ),
        (
            "feature_order_contract_written",
            exists(FEATURE_ORDER_CONTRACT) and int(summary["feature_count"]) == 53,
            FEATURE_ORDER_CONTRACT,
            "53-feature boundary(53개 피처 경계)를 런타임 계약에 기록했다.",
        ),
        (
            "feature_matrix_materialized",
            exists(FEATURE_MATRIX) and int(summary["feature_rows"]) == 5827,
            FEATURE_MATRIX,
            "timestamp-safe feature matrix(시점 안전 피처 행렬)를 만들었다.",
        ),
        (
            "onnx_files_copied_and_hash_matched",
            int(summary["model_rows"]) == 4 and int(summary["model_hash_matched_rows"]) == 4,
            MODEL_HANDOFF_MANIFEST,
            "ONNX(온엑스) 파일을 로컬과 Common Files(공용 파일)에 해시 일치 상태로 복사했다.",
        ),
        (
            "expected_tape_written",
            exists(EXPECTED_TAPE) and int(summary["expected_rows"]) == int(summary["feature_rows"]) * int(summary["attempt_count"]),
            EXPECTED_TAPE,
            "expected tape(예상 테이프)를 모든 attempt(시도)와 row(행)에 대해 만들었다.",
        ),
        (
            "cash_open_partial_mapping_boundary_recorded",
            exists(RUNTIME_MAPPING_AUDIT) and int(summary["cash_open_partial_mapping_attempts"]) == 2,
            RUNTIME_MAPPING_AUDIT,
            "cash-open rule(현금장 규칙)의 부분 매핑 차이를 숨기지 않고 기록했다.",
        ),
        (
            "tester_set_ini_materialized",
            int(summary["set_rows"]) == 4 and int(summary["ini_rows"]) == 4,
            TESTER_SET_MANIFEST,
            "MT5 tester set/ini(테스터 설정 파일)를 만들었다.",
        ),
        (
            "common_files_synced",
            int(summary["common_sync_missing"]) == 0,
            COMMON_FILES_SYNC,
            "MT5 Common Files(MT5 공용 파일) 인계가 누락 없이 끝났다.",
        ),
        (
            "runtime_parity_contract_written",
            exists(RUNTIME_PARITY_CONTRACT) and int(summary["runtime_parity_rows"]) == 4,
            RUNTIME_PARITY_CONTRACT,
            "runtime parity contract(런타임 동등성 계약)를 작성했다.",
        ),
        (
            "run348D_queue_opened",
            exists(RUN348D_QUEUE) and int(summary["queue_rows"]) == 4,
            RUN348D_QUEUE,
            "다음 MT5 runtime probe(MT5 런타임 탐침) queue(대기열)를 열었다.",
        ),
        (
            "skill_receipts_written",
            all(exists(path) for path in [RUN_EVIDENCE_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, RUNTIME_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]),
            RUN_EVIDENCE_RECEIPT,
            "run evidence/data/model/runtime/lineage/claim receipt(실행 근거/데이터/모델/런타임/계보/주장 영수증)를 기록했다.",
        ),
        (
            "no_forbidden_operating_claim",
            summary["mt5_execution"] == "not_run"
            and summary["candidate_selection"] == "not_claimed"
            and summary["runtime_authority"] == "not_claimed"
            and summary["goal_achieve"] == "not_claimed",
            CLAIM_RECEIPT,
            "운영 승격, 런타임 권위, 목표 달성을 주장하지 않았다.",
        ),
        (
            "required_gate_coverage_audit_written",
            True,
            GATE_AUDIT,
            "required gate coverage audit(필수 게이트 커버리지 감사)를 기록했다.",
        ),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return rows


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run348C ONNX Short-Carry Probe Package(348C 온엑스 숏 기여 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- attempts(시도): `{summary['attempt_count']}`
- feature_rows(피처 행): `{summary['feature_rows']}`
- feature_count(피처 수): `{summary['feature_count']}` vs MT5 contract(MT5 계약) `58`
- expected_rows(예상 행): `{summary['expected_rows']}`
- cash_open_partial_mapping_attempts(현금장 부분 매핑 시도): `{summary['cash_open_partial_mapping_attempts']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run348B(348B 실행)의 ONNX deployable seed(온엑스 배포 가능 씨앗) 4개를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 물질화했다.

## Effect(효과)

run348D(348D 실행)에서 Strategy Tester(전략 테스터)를 바로 실행해 proxy-MT5 diff(프록시-MT5 차이), runtime KPI(런타임 핵심 성과 지표), execution behavior(실행 행동)를 볼 수 있다.

## Boundary(경계)

이 run(실행)은 package only(패키지 전용)다. MT5 execution(MT5 실행), candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage348C Package Decision(348C 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- expected_tape(예상 테이프): `{rel(EXPECTED_TAPE)}`
- parity_contract(동등성 계약): `{rel(RUNTIME_PARITY_CONTRACT)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): 4개 ONNX short-carry seed(온엑스 숏 기여 씨앗)를 MT5 probe(탐침) 실행 단위로 묶었다.
Effect(효과): 다음 작업은 MT5 Strategy Tester(MT5 전략 테스터) 실행과 proxy-MT5 comparison(프록시-MT5 비교)으로 좁아졌다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage348 Selection Status(348단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- latest_package(최근 패키지): `{RUN_ID}`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- feature_order_boundary(피처 순서 경계): `53_feature_probe_only(53개 피처 탐침 전용)`
- short_probe_seed_status(숏 탐침 씨앗 상태): `packaged_for_mt5_probe_only(MT5 탐침 패키지 전용)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage348(348단계)은 selection(선정)이 아니라 MT5 probe(탐침) 실행 대기 상태로 이동했다.
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

run348C(348C 실행)는 ONNX short-carry seeds(온엑스 숏 기여 씨앗)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다. run348D(348D 실행)는 이 패키지를 실제 Strategy Tester(전략 테스터)로 실행해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
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
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run348C {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run348C ONNX Short-Carry Probe Package(348C 온엑스 숏 기여 탐침 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- expected_rows(예상 행): `{summary['expected_rows']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): MT5 runtime probe(MT5 런타임 탐침) 실행 대기열을 열었다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run348C ONNX Short-Carry Probe Package(348C 온엑스 숏 기여 탐침 패키지)

- report(보고서): `{rel(REPORT_PATH)}`
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- queue(대기열): `{rel(RUN348D_QUEUE)}`
- effect(효과): Stage348(348단계)이 가벼운 MT5 execution(실행) 작업으로 넘어갈 수 있다.
""",
    )
    append_text_once(REVIEW_INDEX, marker, f"- run348C package(348C 패키지): `{rel(REPORT_PATH)}`")


def ledger_rows(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gate_passes = sum(1 for gate in gates if gate.get("status") == "passed")
    gate_total = len(gates)
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "lane": "runtime_probe_package(런타임 탐침 패키지)",
        "family": "runtime_backtest(MT5/런타임 백테스트)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": summary["feature_rows"],
        "attempt_count": summary["attempt_count"],
        "feature_count": summary["feature_count"],
        "matched_rows": summary["expected_rows"],
        "candidate_model_id": "none(없음)",
        "sample_rows": summary["feature_rows"],
    }
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier A",
        "subrun_id": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "tier_scope": "Tier A",
        "metric_scope": "runtime_package_no_mt5_kpi",
        "kpi_scope": "runtime_package_no_mt5_kpi",
        "primary_kpi": f"attempts={summary['attempt_count']};expected_rows={summary['expected_rows']};feature_count={summary['feature_count']}",
        "guardrail_kpi": f"feature_contract=53_vs_58;cash_open_partial_mapping_attempts={summary['cash_open_partial_mapping_attempts']};no_mt5_execution",
        "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
        "result_status": "package_ready_runtime_execution_required_no_selection(패키지 준비, 런타임 실행 필요, 선정 없음)",
        "notes": "ONNX short-carry seeds(온엑스 숏 기여 씨앗)를 MT5 probe package(MT5 탐침 패키지)로 만들었다.",
    }
    tier_b = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier B",
        "subrun_id": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "tier_scope": "Tier B",
        "metric_scope": "missing_required",
        "kpi_scope": "missing_required",
        "primary_kpi": "missing_required(필수 누락)",
        "guardrail_kpi": "missing_required(필수 누락)",
        "external_verification_status": "missing_required(필수 누락)",
        "result_status": "missing_required(필수 누락)",
        "attempt_count": "",
        "matched_rows": "",
        "notes": "Tier B(티어 B)는 이번 package(패키지) 범위에 없다.",
    }
    combined = {
        **tier_a,
        "ledger_row_id": f"{RUN_ID}__Tier A+B",
        "subrun_id": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_until_tier_b_available",
        "kpi_scope": "same_as_tier_a_until_tier_b_available",
        "result_status": "same_as_tier_a_until_tier_b_available",
        "guardrail_kpi": f"Tier B missing_required(Tier B 필수 누락);feature_contract=53_vs_58;cash_open_partial_mapping_attempts={summary['cash_open_partial_mapping_attempts']}",
    }
    return [tier_a, tier_b, combined]


def write_registries(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    rows = ledger_rows(summary, gates)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe_package(런타임 탐침 패키지)",
                "family": "runtime_backtest(MT5/런타임 백테스트)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "ONNX short-carry MT5 probe package only(온엑스 숏 기여 MT5 탐침 패키지 전용).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for gate in gates if gate.get("status") == "passed"),
                "gate_total": len(gates),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "package_ready_runtime_execution_required_no_selection(패키지 준비, 런타임 실행 필요, 선정 없음)",
                "matched_rows": summary["expected_rows"],
                "sample_rows": summary["feature_rows"],
                "feature_count": summary["feature_count"],
                "attempt_count": summary["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "runtime_package_no_mt5_kpi",
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            }
        ],
    )
    artifact_rows = []
    for path in output_paths():
        if exists(path):
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{rel(path)}",
                    "artifact_type": path.suffix.lower().lstrip(".") or "artifact",
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at": TODAY,
                    "created_at_utc": now_utc(),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "notes": "run348C runtime probe package artifact(348C 런타임 탐침 패키지 산출물).",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_final_and_manifest(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    final = {
        **dict(summary),
        "gate_passes": sum(1 for gate in gates if gate.get("status") == "passed"),
        "gate_total": len(gates),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_training_run_id": SOURCE_TRAINING_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path(__file__)),
            "execution_command": f"python -B {rel(Path(__file__))}",
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in output_paths() if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_register_notes(summary: Mapping[str, Any]) -> None:
    marker = f"run348C {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} run348C ONNX Short-Carry MT5 Probe Package(온엑스 숏 기여 MT5 탐침 패키지)

- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- idea(아이디어): ONNX deployable allocator(온엑스 배포 가능 배분기)를 실제 MT5 probe(탐침)로 관찰한다.
- attempts(시도): `{summary['attempt_count']}`
- effect(효과): weak proxy short signal(약한 프록시 숏 신호)을 selection(선정)이 아니라 runtime evidence(런타임 근거)로 확인하게 한다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} run348C Runtime Boundary Memory(런타임 경계 기억)

- source_run(원천 실행): `{SOURCE_TRAINING_RUN_ID}`
- constraint(제약): feature count(피처 수) `53` vs MT5 v2 contract(MT5 v2 계약) `58`.
- constraint(제약): cash_open_regime_allocator(현금장 국면 배분기)는 현재 EA(`Expert Advisor`, 전문가 자문)에서 partial mapping(부분 매핑)이다.
- effect(효과): run348D(348D 실행)의 MT5 result(MT5 결과)는 반드시 이 경계를 감안해 proxy-MT5 diff(프록시-MT5 차이)로 읽어야 한다.
- evidence(근거): `{rel(FEATURE_ORDER_CONTRACT)}`, `{rel(RUNTIME_MAPPING_AUDIT)}`
""",
    )


def write_changelog(summary: Mapping[str, Any]) -> None:
    marker = f"run348C {RUN_ID}"
    text = f"""## {TODAY} run348C ONNX Short-Carry Probe Package(온엑스 숏 기여 탐침 패키지)

- action(행동): 4개 ONNX seed(온엑스 씨앗)를 MT5 `.set/.ini`, feature matrix(피처 행렬), expected tape(예상 테이프), parity contract(동등성 계약)로 묶었다.
- effect(효과): run348D(348D 실행)에서 Strategy Tester(전략 테스터)를 실행해 실제 runtime KPI(런타임 핵심 성과 지표)를 확인할 수 있다.
- boundary(경계): package only(패키지 전용), no MT5 execution(MT5 실행 없음), no selection(선정 없음), no runtime authority(런타임 권위 없음).
"""
    append_text_once(WORKSPACE_CHANGELOG, marker, text)
    append_text_once(ROOT_CHANGELOG, marker, text)


def validate(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    required_outputs = [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        FEATURE_ORDER_CONTRACT,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        RUNTIME_MAPPING_AUDIT,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        TESTER_IDENTITY_CONTRACT,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        RUNTIME_PARITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUN348D_QUEUE,
        RUN_EVIDENCE_RECEIPT,
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
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        SELECTION_STATUS,
        ROOT_SELECTION_STATUS,
    ]
    missing = [rel(path) for path in required_outputs if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if any(gate.get("status") != "passed" for gate in gates):
        raise RuntimeError("run348C gate audit failed(348C 게이트 감사 실패)")
    if int(summary["common_sync_missing"]) != 0:
        raise RuntimeError("Common Files sync has missing rows(Common Files 동기화 누락 행 있음)")
    if int(summary["feature_count"]) != 53:
        raise RuntimeError("feature count boundary mismatch(피처 수 경계 불일치)")
    final = read_json(FINAL_DECISION)
    for key in ["operating_promotion", "runtime_authority", "goal_achieve", "candidate_selection"]:
        expected = "not_claimed"
        if key == "candidate_selection":
            expected = "not_claimed"
        if final.get(key) != expected:
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")
    for label, path in [
        ("workspace", WORKSPACE_STATE),
        ("current", CURRENT_WORKING_STATE),
        ("selection", SELECTION_STATUS),
        ("root_selection", ROOT_SELECTION_STATUS),
    ]:
        text = read_text(path)
        if STAGE_ID not in text or NEXT_RUN_ID not in text:
            raise RuntimeError(f"{label} state sync failed({label} 상태 동기화 실패)")


INPUT_FILES = [
    PARENT_FINAL_DECISION,
    PARENT_GATE_AUDIT,
    SEED_QUEUE,
    PARENT_SHORT_TRIAGE,
    PARENT_ONNX_REVIEW,
    PARENT_USABILITY,
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_FEATURE_ORDER,
    SOURCE_FEATURE_LABEL,
    SOURCE_PREDICTIONS,
    SOURCE_MODEL_MANIFEST,
    SOURCE_ONNX_SMOKE,
    SOURCE_SPLIT_AUDIT,
]


def build_package() -> dict[str, Any]:
    for path in [RUN_DIR, FEATURE_DIR, EXPECTED_DIR, MODEL_DIR, SET_DIR, INI_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(path), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    parent = read_json(PARENT_FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 next_run_id 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    feature_order, feature_hash = load_feature_order()
    feature_contract = write_feature_order_contract(feature_order, feature_hash)
    source_frame, feature_manifest, feature_common = materialize_feature_matrix(feature_order, feature_hash)
    _seed_fields, seed_rows = read_csv_rows(SEED_QUEUE)
    if len(seed_rows) != 4:
        raise RuntimeError(f"unexpected seed row count(예상 밖 씨앗 행 수): {len(seed_rows)}")
    expected, _expected_index, mapping = build_expected_tape(source_frame, seed_rows)
    from_date, to_date = split_dates()
    tables = materialize_attempts(seed_rows, feature_common, feature_hash, len(feature_order), from_date, to_date)
    summary = build_summary(feature_manifest, feature_contract, seed_rows, expected, mapping, tables)
    write_docs(summary)
    write_register_notes(summary)
    write_changelog(summary)
    write_receipts(summary)
    write_lineage_receipt()
    gates = build_gates(summary)
    write_final_and_manifest(summary, gates)
    write_receipts(summary)
    write_lineage_receipt()
    gates = build_gates(summary)
    write_final_and_manifest(summary, gates)
    write_registries(summary, gates)
    write_lineage_receipt()
    write_registries(summary, gates)
    validate(summary, gates)
    final = read_json(FINAL_DECISION)
    return final


def main() -> None:
    final = build_package()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "attempt_count": final.get("attempt_count"),
                "feature_rows": final.get("feature_rows"),
                "expected_rows": final.get("expected_rows"),
                "gate_passes": final.get("gate_passes"),
                "gate_total": final.get("gate_total"),
                "mt5_execution": "not_run",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import hashlib
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

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage339 import (  # noqa: E402
    materialize_shorter_hold_side_balance_trade_count_expansion_mt5_probe_package_without_db as mt5_base,
)


TODAY = "2026-06-01"

STAGE_ID = "342_session_long_firewall__early_long_filter_mt5_probe"
SOURCE_STAGE_ID = "340_runtime_lifecycle_exit__quality_balance_pressure_review"
PARENT_STAGE_ID = "342_session_long_firewall__early_long_filter_mt5_probe"
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID

RUN_NUMBER = "run342B"
RUN_ID = "run342B_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1"
PARENT_RUN_ID = "run342A_branch_stage341_to_session_long_firewall_probe_without_db_v1"
NEXT_RUN_ID = "run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1"

STATUS = "completed_stage342B_f01_session_long_firewall_mt5_probe_package_materialized_no_selection"
JUDGMENT = "f01_session_long_firewall_mt5_probe_package_ready_runtime_execution_required_no_selection"
DECISION = "stage342B_open_run342C_execute_f01_session_long_firewall_probe"
CLAIM_BOUNDARY = (
    "research_development_f01_session_long_firewall_runtime_probe_package_only_no_mt5_execution_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run342B_f01_session_long_firewall_probe_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage342B_f01_session_long_firewall_probe_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run342A"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_QUEUE = PARENT_RUN_DIR / "run342B_session_long_firewall_probe_queue.csv"
PARENT_HANDOFF = PARENT_RUN_DIR / "stage341_to_stage342_handoff_manifest.csv"

SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run340F"
SOURCE_FEATURE_MATRIX = SOURCE_PACKAGE_DIR / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = SOURCE_PACKAGE_DIR / "expected" / "expected_tape.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_PACKAGE_DIR / "runtime_probe_attempt_package.csv"
SOURCE_MODEL_MANIFEST = SOURCE_PACKAGE_DIR / "model_handoff_manifest.csv"
SOURCE_PARENT_FINAL = SOURCE_PACKAGE_DIR / "final_decision.json"

DEFAULT_COMMON_FILES = mt5_base.DEFAULT_COMMON_FILES
DEFAULT_TERMINAL = mt5_base.DEFAULT_TERMINAL
DEFAULT_TESTER_PROFILE_ROOT = mt5_base.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = mt5_base.DEFAULT_PORTABLE_ROOT
EA_BINARY = mt5_base.EA_BINARY
PORTABLE_EA_EX5 = mt5_base.PORTABLE_EA_EX5
aw = mt5_base.aw

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage342/{RUN_NUMBER}_f01_session_long_firewall_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage342_F01SessionLongFirewall__ONNX"
MAGIC_BASE = 3428500

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_TAPE
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
SIDE_FILTER_EXPECTED_AUDIT = RUN_DIR / "side_filter_expected_decision_audit.csv"
VARIANT_PREVIEW = RUN_DIR / "variant_preview.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN342C_EXECUTION_QUEUE = RUN_DIR / "run342C_queue.csv"
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
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

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

ATTEMPT_NAME_MAP = {
    "e01_q01_control_no_filter": "e01_q01_ctl",
    "e02_q09_control_no_filter": "e02_q09_ctl",
    "e03_q01_block_early_longs": "e03_q01_blk_early_long",
    "e04_q09_block_early_longs": "e04_q09_blk_early_long",
    "e05_q09_block_early_all_sides_negative_control": "e05_q09_blk_early_all",
}


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def path_exists(path: Path) -> bool:
    return os.path.exists(fs_path(path))


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def ensure_parent(path: Path) -> None:
    Path(fs_path(path.parent)).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), low_memory=False, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.loads(handle.read())


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    if path_exists(path):
        with open(fs_path(path), encoding="utf-8-sig") as handle:
            current = handle.read()
    else:
        current = ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    frame = read_csv(path) if path_exists(path) else pd.DataFrame()
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


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(rel(path))
    return path


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(fs_path(source), fs_path(target))
    exists = path_is_file(target)
    return {
        "sync_id": sync_id,
        "source_path": rel(source) if source.is_absolute() and str(source.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else source.as_posix(),
        "target_path": rel(target) if str(target.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else target.as_posix(),
        "exists": bool(exists),
        "sha256": sha256_file(target) if exists else "",
        "status": "synced(동기화됨)" if exists else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def parse_range(text: Any) -> tuple[bool, float, float]:
    cleaned = str(text or "").strip()
    if not cleaned:
        return False, 0.0, 0.0
    parts = [part.strip() for part in cleaned.split(",")]
    if len(parts) != 2:
        raise ValueError(f"invalid range: {text}")
    low = float(parts[0])
    high = float(parts[1])
    if low > high:
        raise ValueError(f"invalid reversed range: {text}")
    return True, low, high


def decide_label(
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


def label_class(label: str) -> int:
    return {"short": 0, "flat": 1, "long": 2}[label]


def source_model_path(source_attempt: str, source_attempt_package: pd.DataFrame) -> Path:
    matched = source_attempt_package.loc[source_attempt_package["attempt_name"].astype(str).eq(source_attempt)]
    if matched.empty:
        raise RuntimeError(f"missing source attempt package row: {source_attempt}")
    local = str(matched.iloc[0].get("model_local_path", "")).strip()
    if not local:
        raise RuntimeError(f"missing source model path: {source_attempt}")
    return required(ROOT / local)


def source_attempt_config(source_attempt: str, source_attempt_package: pd.DataFrame) -> dict[str, Any]:
    matched = source_attempt_package.loc[source_attempt_package["attempt_name"].astype(str).eq(source_attempt)]
    if matched.empty:
        raise RuntimeError(f"missing source attempt config: {source_attempt}")
    row = matched.iloc[0]
    return {
        "source_attempt": source_attempt,
        "source_model_id": row.get("model_id", ""),
        "base_model_id": row.get("base_model_id", "logreg_balanced_c025"),
        "feature_set_id": row.get("feature_set_id", "run338D_training_feature_schema"),
        "feature_count": int(numeric(row.get("feature_count"), 0)),
        "feature_order_hash": str(row.get("feature_order_hash", "")),
        "short_threshold": numeric(row.get("short_threshold"), 0.0),
        "long_threshold": numeric(row.get("long_threshold"), 0.0),
        "min_margin": numeric(row.get("min_margin"), 0.0),
        "max_hold_bars": int(numeric(row.get("max_hold_bars"), 0)),
        "close_on_flat": boolish(row.get("close_on_flat")),
        "from_date": str(row.get("from_date", "2024.07.30")),
        "to_date": str(row.get("to_date", "2025.01.01")),
    }


def load_context() -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame]:
    parent = read_json(required(PARENT_FINAL_DECISION))
    parent_next = parent.get("next_run_id", parent.get("next_action"))
    if parent_next != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent_next} != {RUN_ID}")
    parent_gates = read_csv(required(PARENT_GATE_AUDIT))
    if not parent_gates["status"].astype(str).str.lower().eq("passed").all():
        raise RuntimeError("parent gate audit has failed rows")
    queue = read_csv(required(PARENT_QUEUE)).fillna("")
    if queue.empty:
        raise RuntimeError(f"{RUN_NUMBER} queue is empty")
    source_attempt_package = read_csv(required(SOURCE_ATTEMPT_PACKAGE)).fillna("")
    return queue, parent, source_attempt_package


def materialize_feature_matrix(source_attempt_package: pd.DataFrame) -> tuple[str, int, int, str, list[str]]:
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    copy_file(
        required(SOURCE_FEATURE_MATRIX),
        FEATURE_MATRIX,
        "local_feature_matrix",
        f"feature matrix(피처 행렬)를 {RUN_NUMBER} 실행으로 복사한다.",
    )
    common_target = DEFAULT_COMMON_FILES / Path(feature_common)
    copy_file(
        FEATURE_MATRIX,
        common_target,
        "common_feature_matrix",
        "feature matrix(피처 행렬)를 MT5 Common Files(MT5 공용 파일)로 복사한다.",
    )
    features = read_csv(FEATURE_MATRIX)
    feature_columns = [column for column in features.columns if column != "timestamp"]
    rows = int(len(features))
    first = source_attempt_package.iloc[0]
    feature_count = int(numeric(first.get("feature_count"), len(feature_columns)))
    feature_hash = str(first.get("feature_order_hash", ""))
    duplicate_timestamps = int(features["timestamp"].duplicated().sum()) if "timestamp" in features.columns else -1
    write_csv(
        FEATURE_MATRIX_MANIFEST,
        pd.DataFrame(
            [
                {
                    "matrix_id": f"{RUN_NUMBER}_runtime_features_reused_from_run340F",
                    "path": rel(FEATURE_MATRIX),
                    "common_path": feature_common,
                    "rows": rows,
                    "feature_count": feature_count,
                    "actual_feature_columns": len(feature_columns),
                    "feature_order_hash": feature_hash,
                    "duplicate_timestamps": duplicate_timestamps,
                    "sha256": sha256_file(FEATURE_MATRIX),
                    "source_path": rel(SOURCE_FEATURE_MATRIX),
                    "time_axis": "bar_time is M5 bar close timestamp(5분봉 종가 시각)",
                    "feature_label_boundary": "feature-only replay; no labels joined(피처 전용 재생, 라벨 결합 없음)",
                    "effect": "데이터(data, 데이터)를 바꾸지 않고 side filter(사이드 필터) 실행 의미만 분리한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )
    return feature_common, rows, feature_count, feature_hash, feature_columns


def build_expected_tape(
    queue: pd.DataFrame,
    source_attempt_package: pd.DataFrame,
    feature_columns: Sequence[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source_expected = read_csv(required(SOURCE_EXPECTED_TAPE)).fillna("")
    features = read_csv(required(FEATURE_MATRIX)).fillna("")
    expected_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []

    feature_lookup = features.set_index("timestamp", drop=False)
    source_expected_count = 0
    for _, variant in queue.reset_index(drop=True).iterrows():
        queue_id = str(variant["queue_id"])
        attempt = ATTEMPT_NAME_MAP.get(queue_id, queue_id)
        source_attempt = str(variant["source_attempt"])
        config = source_attempt_config(source_attempt, source_attempt_package)
        model_id = f"logreg_balanced_c025_{attempt}"
        side_enabled = boolish(variant.get("side_filter_enabled"))
        feature_index = int(numeric(variant.get("feature_index"), -1)) if side_enabled else -1
        feature_name = feature_columns[feature_index] if 0 <= feature_index < len(feature_columns) else ""
        block_long_enabled, block_long_min, block_long_max = parse_range(variant.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(variant.get("block_short_range", ""))

        source = source_expected.loc[source_expected["attempt_name"].astype(str).eq(source_attempt)].copy()
        if source.empty:
            raise RuntimeError(f"source expected tape empty: {source_attempt}")
        source_expected_count = max(source_expected_count, int(len(source)))
        labels: list[str] = []
        pre_labels: list[str] = []
        blocked_long = 0
        blocked_short = 0
        missing_feature_rows = 0
        for _, row in source.iterrows():
            p_short = numeric(row.get("p_short"))
            p_flat = numeric(row.get("p_flat"))
            p_long = numeric(row.get("p_long"))
            pre_label = decide_label(
                p_short,
                p_flat,
                p_long,
                config["short_threshold"],
                config["long_threshold"],
                config["min_margin"],
            )
            label = pre_label
            side_applied = False
            side_reason = ""
            feature_value = ""
            bar_time = str(row.get("bar_time", ""))
            if side_enabled and pre_label != "flat" and feature_name:
                if bar_time in feature_lookup.index:
                    feature_value = numeric(feature_lookup.loc[bar_time, feature_name])
                    if (
                        pre_label == "long"
                        and block_long_enabled
                        and block_long_min <= float(feature_value) <= block_long_max
                    ):
                        label = "flat"
                        side_applied = True
                        blocked_long += 1
                        side_reason = "side_filter_block_long_feature_range(사이드 필터 롱 범위 차단)"
                    elif (
                        pre_label == "short"
                        and block_short_enabled
                        and block_short_min <= float(feature_value) <= block_short_max
                    ):
                        label = "flat"
                        side_applied = True
                        blocked_short += 1
                        side_reason = "side_filter_block_short_feature_range(사이드 필터 숏 범위 차단)"
                else:
                    missing_feature_rows += 1
            labels.append(label)
            pre_labels.append(pre_label)
            expected_rows.append(
                {
                    "attempt_name": attempt,
                    "model_id": model_id,
                    "base_model_id": config["base_model_id"],
                    "source_attempt_name": source_attempt,
                    "source_queue_id": queue_id,
                    "bar_time": bar_time,
                    "source_time": row.get("source_time", row.get("bar_time", "")),
                    "source_row_id": row.get("source_row_id", ""),
                    "feature_input_hash": row.get("feature_input_hash", ""),
                    "p_short": p_short,
                    "p_flat": p_flat,
                    "p_long": p_long,
                    "pre_filter_decision_label": pre_label,
                    "decision_class": label_class(label),
                    "decision_label": label,
                    "short_threshold": config["short_threshold"],
                    "long_threshold": config["long_threshold"],
                    "min_margin": config["min_margin"],
                    "max_hold_bars": config["max_hold_bars"],
                    "close_on_flat": config["close_on_flat"],
                    "side_filter_enabled": side_enabled,
                    "side_filter_feature_index": feature_index,
                    "side_filter_feature_name": feature_name,
                    "side_filter_feature_value": feature_value,
                    "side_filter_applied": side_applied,
                    "side_filter_reason": side_reason,
                    "block_long_range_enabled": block_long_enabled,
                    "block_long_min": block_long_min,
                    "block_long_max": block_long_max,
                    "block_short_range_enabled": block_short_enabled,
                    "block_short_min": block_short_min,
                    "block_short_max": block_short_max,
                    "variant_role": variant["role"],
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선정)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        counts = pd.Series(labels).value_counts()
        pre_counts = pd.Series(pre_labels).value_counts()
        long_count = int(counts.get("long", 0))
        short_count = int(counts.get("short", 0))
        trade_count = long_count + short_count
        side_balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) else 0.0
        preview_rows.append(
            {
                "attempt_name": attempt,
                "queue_id": queue_id,
                "source_attempt": source_attempt,
                "model_id": model_id,
                "variant_role": variant["role"],
                "signal_trade_count": trade_count,
                "signal_long_count": long_count,
                "signal_short_count": short_count,
                "signal_flat_count": int(counts.get("flat", 0)),
                "pre_filter_long_count": int(pre_counts.get("long", 0)),
                "pre_filter_short_count": int(pre_counts.get("short", 0)),
                "side_filter_blocked_long_count": blocked_long,
                "side_filter_blocked_short_count": blocked_short,
                "missing_feature_rows": missing_feature_rows,
                "signal_side_balance": round(side_balance, 8),
                "short_threshold": config["short_threshold"],
                "long_threshold": config["long_threshold"],
                "min_margin": config["min_margin"],
                "max_hold_bars": config["max_hold_bars"],
                "close_on_flat": config["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "side_filter_feature_name": feature_name,
                "block_long_range": str(variant.get("block_long_range", "")),
                "block_short_range": str(variant.get("block_short_range", "")),
                "expected_effect": variant["expected_effect"],
                "effect": "side filter(사이드 필터) 후 MT5 decision supply(MT5 결정 공급)를 예상한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        audit_rows.append(
            {
                "attempt_name": attempt,
                "source_attempt": source_attempt,
                "side_filter_enabled": side_enabled,
                "feature_index": feature_index,
                "feature_name": feature_name,
                "source_expected_rows": int(len(source)),
                "post_filter_rows": int(len(labels)),
                "blocked_long_count": blocked_long,
                "blocked_short_count": blocked_short,
                "missing_feature_rows": missing_feature_rows,
                "timestamp_safe": missing_feature_rows == 0,
                "effect": "feature row(피처 행) 시각의 현재 값만 사용해 side filter(사이드 필터)를 적용한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    expected = pd.DataFrame(expected_rows)
    preview = pd.DataFrame(preview_rows)
    audit = pd.DataFrame(audit_rows)
    write_csv(EXPECTED_TAPE, expected)
    write_csv(VARIANT_PREVIEW, preview)
    write_csv(SIDE_FILTER_EXPECTED_AUDIT, audit)
    write_csv(
        EXPECTED_TAPE_INDEX,
        pd.DataFrame(
            [
                {
                    "attempt_name": row["attempt_name"],
                    "model_id": row["model_id"],
                    "row_count": int(len(expected.loc[expected["attempt_name"].eq(row["attempt_name"])])),
                    "source_expected_count": source_expected_count,
                    "path": rel(EXPECTED_TAPE),
                    "sha256": sha256_file(EXPECTED_TAPE),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
                for _, row in preview.iterrows()
            ]
        ),
    )
    return expected, preview, audit


def materialize_attempts(
    queue: pd.DataFrame,
    source_attempt_package: pd.DataFrame,
    feature_common: str,
    feature_count: int,
    feature_hash: str,
) -> dict[str, pd.DataFrame]:
    sync_rows: list[dict[str, Any]] = [
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": (DEFAULT_COMMON_FILES / Path(feature_common)).as_posix(),
            "exists": path_is_file(DEFAULT_COMMON_FILES / Path(feature_common)),
            "sha256": sha256_file(DEFAULT_COMMON_FILES / Path(feature_common))
            if path_is_file(DEFAULT_COMMON_FILES / Path(feature_common))
            else "",
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
        queue_id = str(variant["queue_id"])
        attempt = ATTEMPT_NAME_MAP.get(queue_id, queue_id)
        source_attempt = str(variant["source_attempt"])
        config = source_attempt_config(source_attempt, source_attempt_package)
        source_model = source_model_path(source_attempt, source_attempt_package)
        source_sha = sha256_file(source_model)
        model_id = f"logreg_balanced_c025_{attempt}"
        side_enabled = boolish(variant.get("side_filter_enabled"))
        feature_index = int(numeric(variant.get("feature_index"), -1)) if side_enabled else -1
        block_long_enabled, block_long_min, block_long_max = parse_range(variant.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(variant.get("block_short_range", ""))

        magic = MAGIC_BASE + index + 1
        local_onnx = MODEL_DIR / f"{attempt}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{attempt}.onnx"
        sync_rows.append(
            copy_file(
                source_model,
                local_onnx,
                f"local_onnx::{attempt}",
                "ONNX(온엑스)를 side filter(사이드 필터) variant(변형) 이름으로 복사한다.",
            )
        )
        sync_rows.append(
            copy_file(
                local_onnx,
                DEFAULT_COMMON_FILES / Path(common_onnx),
                f"common_onnx::{attempt}",
                "ONNX(온엑스)를 MT5 Common Files(MT5 공용 파일)로 복사한다.",
            )
        )

        set_name = f"OPV2_{RUN_NUMBER}_{attempt}.set"
        ini_name = f"OPV2_{RUN_NUMBER}_{attempt}.ini"
        report_name = f"POPv2_{RUN_NUMBER}_{attempt}"
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
            "InpShortThreshold": config["short_threshold"],
            "InpLongThreshold": config["long_threshold"],
            "InpMinMargin": config["min_margin"],
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": side_enabled,
            "InpSideFilterFeatureIndex": feature_index,
            "InpFallbackSideFilterFeatureIndex": feature_index,
            "InpBlockShortFeatureRange": side_enabled and block_short_enabled,
            "InpBlockShortFeatureMin": block_short_min,
            "InpBlockShortFeatureMax": block_short_max,
            "InpBlockLongFeatureRange": side_enabled and block_long_enabled,
            "InpBlockLongFeatureMin": block_long_min,
            "InpBlockLongFeatureMax": block_long_max,
            "InpAllowTrading": True,
            "InpFixedLot": 0.10,
            "InpMagic": magic,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": config["close_on_flat"],
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": config["max_hold_bars"],
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
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=config["from_date"],
                to_date=config["to_date"],
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": attempt,
                "queue_id": queue_id,
                "model_id": model_id,
                "base_model_id": config["base_model_id"],
                "source_attempt": source_attempt,
                "source_onnx_path": rel(source_model),
                "source_onnx_sha256": source_sha,
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha256_file(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha256_file(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps([0, 1, 2]),
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "effect": "같은 ONNX(온엑스)에 side filter(사이드 필터) 설정 효과만 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt,
                "queue_id": queue_id,
                "model_id": model_id,
                "variant_role": variant["role"],
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "short_threshold": config["short_threshold"],
                "long_threshold": config["long_threshold"],
                "min_margin": config["min_margin"],
                "max_hold_bars": config["max_hold_bars"],
                "close_on_flat": config["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "block_long_range_enabled": side_enabled and block_long_enabled,
                "block_long_min": block_long_min,
                "block_long_max": block_long_max,
                "block_short_range_enabled": side_enabled and block_short_enabled,
                "block_short_min": block_short_min,
                "block_short_max": block_short_max,
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
                "queue_id": queue_id,
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": index + 1,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": model_id,
                "base_model_id": config["base_model_id"],
                "source_attempt": source_attempt,
                "feature_set_id": config["feature_set_id"],
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
                "from_date": config["from_date"],
                "to_date": config["to_date"],
                "decision_mode": "threshold_margin",
                "short_threshold": config["short_threshold"],
                "long_threshold": config["long_threshold"],
                "min_margin": config["min_margin"],
                "fixed_lot": 0.10,
                "max_hold_bars": config["max_hold_bars"],
                "close_on_flat": config["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "block_long_range": str(variant.get("block_long_range", "")),
                "block_short_range": str(variant.get("block_short_range", "")),
                "variant_role": variant["role"],
                "effect": variant["expected_effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_rows.append(
            {
                "contract_id": f"tester_identity::{attempt}",
                "attempt_name": attempt,
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "portable_root": DEFAULT_PORTABLE_ROOT.as_posix(),
                "expert": tester.get("Expert", ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "ea_binary": EA_BINARY.as_posix(),
                "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        proxy_rows.append(
            {
                "contract_id": f"proxy_mt5_comparison::{attempt}",
                "attempt_name": attempt,
                "expected_tape": rel(EXPECTED_TAPE),
                "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
                "must_compare": "feature_input_hash, probabilities, post-side-filter decision, trade KPI(피처 해시, 확률, 필터 후 결정, 거래 KPI)",
                "known_difference": "side filter(사이드 필터)는 probabilities(확률)를 바꾸지 않고 decision(결정)만 flat(관망)으로 바꿀 수 있다.",
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        runtime_rows.append(
            {
                "contract_id": f"runtime_parity::{attempt}",
                "attempt_name": attempt,
                "runtime_path": rel(set_path),
                "shared_contract": (
                    f"features={feature_count};feature_hash={feature_hash};short={config['short_threshold']};"
                    f"long={config['long_threshold']};min_margin={config['min_margin']};hold={config['max_hold_bars']};"
                    f"close_flat={config['close_on_flat']};side_filter={side_enabled};feature_index={feature_index};"
                    f"block_long={side_enabled and block_long_enabled}:{block_long_min}:{block_long_max};"
                    f"block_short={side_enabled and block_short_enabled}:{block_short_min}:{block_short_max}"
                ),
                "parity_check": f"{NEXT_RUN_ID} telemetry-vs-expected tape(다음 실행 기록 대 예상 테이프)",
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
                "effect": f"{RUN_NUMBER} 패키지를 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
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
        (RUN342C_EXECUTION_QUEUE, tables["queue"]),
    ]:
        write_csv(path, frame)
    return tables


def output_paths() -> list[Path]:
    return [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        SIDE_FILTER_EXPECTED_AUDIT,
        VARIANT_PREVIEW,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        TESTER_IDENTITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUNTIME_PARITY_CONTRACT,
        RUN342C_EXECUTION_QUEUE,
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
        SELECTION_STATUS,
        STAGE_LEDGER,
        Path(__file__),
    ]


def build_summary(
    queue: pd.DataFrame,
    parent: Mapping[str, Any],
    package_rows: int,
    feature_count: int,
    feature_hash: str,
    expected: pd.DataFrame,
    preview: pd.DataFrame,
    audit: pd.DataFrame,
    tables: Mapping[str, pd.DataFrame],
) -> dict[str, Any]:
    source_expected_rows = int(expected.groupby("attempt_name").size().max()) if not expected.empty else 0
    side_attempts = int(preview["side_filter_enabled"].astype(bool).sum()) if "side_filter_enabled" in preview.columns else 0
    blocked_long = int(audit["blocked_long_count"].sum()) if "blocked_long_count" in audit.columns else 0
    blocked_short = int(audit["blocked_short_count"].sum()) if "blocked_short_count" in audit.columns else 0
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": int(len(queue)),
        "side_filter_attempt_count": side_attempts,
        "package_rows": int(package_rows),
        "source_expected_rows_per_attempt": source_expected_rows,
        "expected_rows": int(len(expected)),
        "feature_count": int(feature_count),
        "feature_order_hash": feature_hash,
        "side_filter_blocked_long_rows": blocked_long,
        "side_filter_blocked_short_rows": blocked_short,
        "side_filter_blocked_rows": blocked_long + blocked_short,
        "preview_max_signal_trade_count": int(preview["signal_trade_count"].max()) if not preview.empty else 0,
        "preview_min_signal_trade_count": int(preview["signal_trade_count"].min()) if not preview.empty else 0,
        "preview_best_signal_side_balance": float(preview["signal_side_balance"].max()) if not preview.empty else 0.0,
        "preview_worst_signal_side_balance": float(preview["signal_side_balance"].min()) if not preview.empty else 0.0,
        "common_sync_missing": int((~tables["sync"]["exists"].astype(bool)).sum()),
        "set_rows": int(len(tables["set"])),
        "ini_rows": int(len(tables["ini"])),
        "side_filter_set_rows": int(tables["set"]["side_filter_enabled"].astype(bool).sum()),
        "terminal_exists": path_is_file(DEFAULT_TERMINAL),
        "common_files_exists": path_exists(DEFAULT_COMMON_FILES),
        "ea_binary_exists": path_is_file(EA_BINARY),
        "portable_ea_exists": path_is_file(PORTABLE_EA_EX5),
        "parent_status": parent.get("status", ""),
        "parent_goal_achieve": parent.get("goal_achieve", "not_claimed"),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gate_passed = False
    if path_is_file(PARENT_GATE_AUDIT):
        parent_gates = read_csv(PARENT_GATE_AUDIT)
        parent_gate_passed = bool(parent_gates["status"].astype(str).str.lower().eq("passed").all())
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["mt5_execution"] == "not_run"
    )
    return pd.DataFrame(
        [
            gate_row(
                "parent_342A_gates_passed",
                "passed" if parent_gate_passed else "failed",
                rel(PARENT_GATE_AUDIT),
                "run342A(342A 실행) 분기 gate(게이트)를 이어받는다.",
            ),
            gate_row(
                "feature_matrix_reused_timestamp_safe",
                "passed"
                if path_is_file(FEATURE_MATRIX) and summary["package_rows"] > 0 and summary["feature_count"] == 53
                else "failed",
                rel(FEATURE_MATRIX_MANIFEST),
                "feature matrix(피처 행렬)를 새로 만들지 않고 timestamp-safe(시점 안전)하게 재사용한다.",
            ),
            gate_row(
                "expected_tape_side_filter_materialized",
                "passed"
                if summary["expected_rows"] == summary["package_rows"] * summary["attempt_count"]
                and summary["side_filter_blocked_rows"] > 0
                else "failed",
                rel(SIDE_FILTER_EXPECTED_AUDIT),
                "expected tape(예상 테이프)에 side filter(사이드 필터) 후 decision(결정)을 반영한다.",
            ),
            gate_row(
                "common_files_synced",
                "passed" if summary["common_sync_missing"] == 0 else "failed",
                rel(COMMON_FILES_SYNC),
                "MT5 Common Files(MT5 공용 파일) 인계를 확인한다.",
            ),
            gate_row(
                "tester_set_ini_materialized",
                "passed"
                if summary["set_rows"] == summary["attempt_count"]
                and summary["ini_rows"] == summary["attempt_count"]
                and summary["side_filter_set_rows"] == summary["side_filter_attempt_count"]
                else "failed",
                rel(TESTER_SET_MANIFEST),
                "tester set/ini(테스터 설정 파일)와 side filter(사이드 필터) 파라미터를 만든다.",
            ),
            gate_row(
                "runtime_parity_contract_written",
                "passed" if path_is_file(RUNTIME_PARITY_CONTRACT) and path_is_file(PROXY_MT5_COMPARISON_CONTRACT) else "failed",
                rel(RUNTIME_PARITY_CONTRACT),
                "runtime parity(런타임 동등성) 비교 계약을 남긴다.",
            ),
            gate_row(
                "tester_identity_visible",
                "passed"
                if summary["terminal_exists"]
                and summary["common_files_exists"]
                and summary["ea_binary_exists"]
                and summary["portable_ea_exists"]
                else "failed",
                rel(TESTER_IDENTITY_CONTRACT),
                "MT5(메타트레이더5) 실행 가시성을 확인한다.",
            ),
            gate_row(
                "run342C_queue_opened",
                "passed" if path_is_file(RUN342C_EXECUTION_QUEUE) else "failed",
                rel(RUN342C_EXECUTION_QUEUE),
                "다음 MT5 runtime probe(MT5 런타임 탐침) queue(대기열)를 연다.",
            ),
            gate_row(
                "no_forbidden_selection_or_goal_claim",
                "passed" if no_forbidden else "failed",
                rel(CLAIM_RECEIPT),
                "package(패키지)를 selection(선정)이나 Goal Achieve(목표 달성)로 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
            ),
        ]
    )


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run342B F01 Session-Long Firewall Probe Package(342B F01 세션 롱 방화벽 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- side_filter_attempts(사이드 필터 시도): `{summary['side_filter_attempt_count']}`
- feature_rows(피처 행): `{summary['package_rows']}`
- feature_count(피처 수): `{summary['feature_count']}`
- expected_rows(예상 행): `{summary['expected_rows']}`
- side_filter_blocked_rows(사이드 필터 차단 행): `{summary['side_filter_blocked_rows']}`
- blocked_long_rows(차단 롱 행): `{summary['side_filter_blocked_long_rows']}`
- blocked_short_rows(차단 숏 행): `{summary['side_filter_blocked_short_rows']}`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `{summary['preview_max_signal_trade_count']}`
- preview_min_signal_trade_count(미리보기 최소 신호 거래수): `{summary['preview_min_signal_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run340F(340F 실행)의 q01/q09(큐01/큐09) ONNX(온엑스), feature matrix(피처 행렬), expected probabilities(예상 확률)를 재사용하고, Stage342(342단계)의 early-long block(초반 롱 차단) side filter(사이드 필터)를 `.set` 파일과 expected tape(예상 테이프)에 반영했다.

## Effect(효과)

run342C(342C 실행)는 MT5 Strategy Tester(MT5 전략 테스터)에서 control(대조), early-long firewall(초반 롱 방화벽), overfilter negative control(과필터 부정 대조)을 같은 runtime contract(런타임 계약)로 비교할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage342B Probe Package Decision(342B 탐침 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- queue(대기열): `{rel(RUN342C_EXECUTION_QUEUE)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): session-long firewall(세션 롱 방화벽) MT5(메타트레이더5) probe package(탐침 패키지)를 만들었다.
Effect(효과): Stage342(342단계)의 실제 runtime probe(런타임 탐침)를 바로 실행할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- side_filter_attempts(사이드 필터 시도): `{summary['side_filter_attempt_count']}`
- quality_anchor(품질 기준점): `q01_ctl_s55_l51_m01_h12`
- net_high_clue(순수익 높은 단서): `q09_s545_l51_m01_h12`
- next_probe(다음 탐침): `session_long_firewall(세션 롱 방화벽)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage 342(342단계)는 패키지 완료 상태이며, 다음에는 MT5 runtime probe(MT5 런타임 탐침)를 실행해야 한다.
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

run342B(342B 실행)는 session-long firewall(세션 롱 방화벽) MT5 package(MT5 패키지)를 만들었다. run342C(342C 실행)는 이 package(패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침)로 실행해야 한다.

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
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)

    append_text_once(
        STAGE_BRIEF,
        RUN_ID,
        f"""## run342B F01 Session-Long Firewall Package(342B F01 세션 롱 방화벽 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- side_filter_blocked_rows(사이드 필터 차단 행): `{summary['side_filter_blocked_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): side filter(사이드 필터) 아이디어를 MT5 runtime probe(MT5 런타임 탐침) 실행 준비물로 바꾼다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run342B F01 Session-Long Firewall Package(342B F01 세션 롱 방화벽 패키지)

- run_id(실행 ID): `{RUN_ID}`
- queue(대기열): `{rel(RUN342C_EXECUTION_QUEUE)}`
- effect(효과): Stage342(342단계)가 MT5(메타트레이더5) 실행 단계로 넘어갈 수 있다.
""",
    )
    changelog = f"""## {TODAY} run342B F01 Session-Long Firewall Package(F01 세션 롱 방화벽 패키지)

- action(행동): q01/q09(큐01/큐09) control(대조)과 side filter(사이드 필터) `{summary['attempt_count']}`개를 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run342C(342C 실행)가 early-long firewall(초반 롱 방화벽)의 runtime KPI(런타임 핵심 성과 지표)를 검증할 수 있다.
- boundary(경계): package only(패키지 전용), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, changelog)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, changelog)


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    final = {
        **dict(summary),
        "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
        "gate_total": int(len(gates)),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": f"python {rel(Path(__file__))}",
            "inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_QUEUE),
                rel(SOURCE_FEATURE_MATRIX),
                rel(SOURCE_EXPECTED_TAPE),
                rel(SOURCE_ATTEMPT_PACKAGE),
                rel(SOURCE_MODEL_MANIFEST),
            ],
            "outputs": [rel(path) for path in output_paths() if path_exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


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
        "candidate_model_id": "logreg_balanced_c025_q01_q09_session_long_firewall_pack",
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "recovery_factor": "",
        "trade_count": "",
        "result_status": "mt5_probe_package_ready_runtime_execution_required(MT5 탐침 패키지 준비, 런타임 실행 필요)",
        "sample_rows": summary["package_rows"],
        "feature_count": summary["feature_count"],
        "matched_rows": "",
        "expectancy": "",
        "attempt_count": summary["attempt_count"],
    }
    return [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "runtime_probe_package_only_no_new_kpi",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "candidate_model_id": "",
            "sample_rows": "",
            "feature_count": "",
            "attempt_count": "",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
        },
    ]


def write_registries(gates: pd.DataFrame, summary: Mapping[str, Any]) -> None:
    rows = stage_rows(gates, summary)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "tier", "view"], rows)
    project_rows = []
    for row in rows:
        project_rows.append(
            {
                **row,
                "ledger_row_id": f"{RUN_ID}__{row['tier']}",
                "subrun_id": row["tier"],
                "record_view": row["view"],
                "tier_scope": row["tier"],
                "kpi_scope": row["metric_scope"],
                "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
                "path": rel(REPORT_PATH),
                "primary_kpi": f"side_filter_blocked_rows={summary['side_filter_blocked_rows']};attempt_count={summary['attempt_count']}",
                "guardrail_kpi": "MT5 KPI not run(MT5 핵심 성과 지표 미실행)",
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "notes": "Package only(패키지 전용); run342C must execute MT5 runtime probe(342C에서 MT5 런타임 탐침 실행 필요).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe_package(런타임 탐침 패키지)",
                "family": "runtime_backtest",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Session-long firewall(세션 롱 방화벽) package only(패키지 전용).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": summary["package_rows"],
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "logreg_balanced_c025_q01_q09_session_long_firewall_pack",
                "result_status": "mt5_probe_package_ready_runtime_execution_required(MT5 탐침 패키지 준비, 런타임 실행 필요)",
                "sample_rows": summary["package_rows"],
                "feature_count": summary["feature_count"],
                "attempt_count": summary["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "runtime_probe_package_only_no_new_kpi",
            }
        ],
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    receipt_base = {
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
            **receipt_base,
            "data_source": rel(FEATURE_MATRIX),
            "time_axis": "M5 bar close timestamp(5분봉 종가 시각)",
            "sample_scope": "FPMarkets US100 M5 inner-holdout runtime collapsed probe(내부 보류 런타임 축약 탐침)",
            "missing_or_duplicate_check": rel(FEATURE_MATRIX_MANIFEST),
            "feature_label_boundary": "no labels joined; side filter uses current feature row only(라벨 결합 없음, 사이드 필터는 현재 피처 행만 사용)",
            "split_boundary": "inner_holdout_runtime_collapsed_probe(내부 보류 런타임 축약 탐침)",
            "leakage_risk": "feature_index misuse(피처 인덱스 오사용); guarded by side_filter_expected_decision_audit(감사 파일)",
            "data_hash_or_identity": sha256_file(FEATURE_MATRIX),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **receipt_base,
            "model_training": "not_run(실행 없음)",
            "source_model_manifest": rel(SOURCE_MODEL_MANIFEST),
            "model_handoff": rel(MODEL_HANDOFF_MANIFEST),
            "effect": "기존 ONNX(온엑스)를 재사용하고 side filter(사이드 필터) 파라미터 효과만 분리한다.",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **receipt_base,
            "research_path": rel(EXPECTED_TAPE),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": rel(RUNTIME_PARITY_CONTRACT),
            "known_differences": "probabilities(확률)는 원본 ONNX(온엑스)와 같고 decision(결정)은 side filter(사이드 필터) 후 flat(관망)으로 바뀔 수 있다.",
            "parity_check": "deferred_to_run342C telemetry-vs-expected tape(342C 기록 대 예상 테이프)",
            "parity_identity": rel(TESTER_IDENTITY_CONTRACT),
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **receipt_base,
            "candidate_selection": "not_run(실행 없음)",
            "mt5_execution": "not_run(실행 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    )
    existing_outputs = [path for path in output_paths() if path_exists(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            **receipt_base,
            "source_inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_QUEUE),
                rel(PARENT_HANDOFF),
                rel(SOURCE_FEATURE_MATRIX),
                rel(SOURCE_EXPECTED_TAPE),
                rel(SOURCE_ATTEMPT_PACKAGE),
                rel(SOURCE_MODEL_MANIFEST),
                rel(SOURCE_PARENT_FINAL),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in existing_outputs],
            "artifact_hashes": {rel(path): sha256_file(path) for path in existing_outputs if path_is_file(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, notes in [
        ("feature_matrix_manifest", FEATURE_MATRIX_MANIFEST, "Runtime feature matrix reuse manifest."),
        ("expected_tape", EXPECTED_TAPE, "Expected probability and post-side-filter decision tape."),
        ("side_filter_expected_audit", SIDE_FILTER_EXPECTED_AUDIT, "Side filter expected decision audit."),
        ("variant_preview", VARIANT_PREVIEW, "Package signal preview."),
        ("model_handoff_manifest", MODEL_HANDOFF_MANIFEST, "ONNX handoff manifest."),
        ("common_files_sync", COMMON_FILES_SYNC, "Common Files sync manifest."),
        ("tester_set_manifest", TESTER_SET_MANIFEST, "MT5 tester set manifest."),
        ("tester_ini_manifest", TESTER_INI_MANIFEST, "MT5 tester ini manifest."),
        ("runtime_probe_attempt_package", RUNTIME_PROBE_ATTEMPT_PACKAGE, "Runtime probe attempt package."),
        ("runtime_parity_contract", RUNTIME_PARITY_CONTRACT, "Runtime parity contract."),
        ("run342C_queue", RUN342C_EXECUTION_QUEUE, "Next MT5 runtime probe queue."),
        ("final_decision", FINAL_DECISION, "Run342B final decision."),
        ("run_manifest", RUN_MANIFEST, "Run342B run manifest."),
        ("report", REPORT_PATH, "Run342B report."),
        ("decision_doc", DECISION_DOC, "Run342B decision document."),
        ("pipeline_script", Path(__file__), "Run342B materializer script."),
    ]:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path) if path_is_file(path) else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "notes": notes,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows)


def main() -> None:
    for path in [
        PARENT_FINAL_DECISION,
        PARENT_GATE_AUDIT,
        PARENT_QUEUE,
        SOURCE_FEATURE_MATRIX,
        SOURCE_EXPECTED_TAPE,
        SOURCE_ATTEMPT_PACKAGE,
        SOURCE_MODEL_MANIFEST,
    ]:
        required(path)
    queue, parent, source_attempt_package = load_context()
    feature_common, package_rows, feature_count, feature_hash, feature_columns = materialize_feature_matrix(source_attempt_package)
    expected, preview, audit = build_expected_tape(queue, source_attempt_package, feature_columns)
    tables = materialize_attempts(queue, source_attempt_package, feature_common, feature_count, feature_hash)
    summary = build_summary(queue, parent, package_rows, feature_count, feature_hash, expected, preview, audit, tables)
    write_docs(summary)
    gates = build_gates(summary)
    write_csv(GATE_AUDIT, gates)
    if not gates["status"].astype(str).str.lower().eq("passed").all():
        failed = gates.loc[gates["status"].astype(str).str.lower() != "passed", "gate_id"].tolist()
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise SystemExit(f"failed gates: {failed}")
    write_final(summary, gates)
    write_registries(gates, summary)
    write_receipts(summary)
    write_artifact_registry()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "attempt_count": summary["attempt_count"],
                "side_filter_blocked_rows": summary["side_filter_blocked_rows"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

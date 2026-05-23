from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE279_ID = "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild"
RUN_ID = "run279B_materialize_directional_runtime_mapping_inputs_v1"
SOURCE_RUN_ID = "run279A_design_directional_runtime_mapping_rebuild_packet_v1"
STATUS = "completed_directional_runtime_mapping_inputs_materialized_no_candidate_selection"
JUDGMENT = "directional_runtime_mapping_inputs_materialized_no_runtime_or_candidate_claim"
NEXT_ACTION = "run279C_execute_or_prepare_directional_runtime_mapping_mt5_probe"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE279_ID
RUN279A = STAGE / "02_runs" / "run279A"
RUN_DIR = STAGE / "02_runs" / "run279B"
PAYLOAD_DIR = RUN_DIR / "payloads"
HANDOFF_DIR = RUN_DIR / "handoff"
MT5_DIR = RUN_DIR / "mt5_handoff"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEWS / "review_index.md"

SOURCE_BRANCH_PLAN = RUN279A / "direction_mapping_branch_plan.csv"
SOURCE_QUEUE = RUN279A / "direction_mapping_materialization_queue.csv"
SOURCE_CONTRACT = RUN279A / "runtime_mapping_contract_plan.csv"
SOURCE_AUDIT = RUN279A / "direction_source_audit.csv"
SOURCE_RUN279A_MANIFEST = RUN279A / "run_manifest.json"
SOURCE_RUN279A_LINEAGE = RUN279A / "artifact_lineage_receipt.json"
SOURCE_PAYLOAD_MANIFEST = STAGE / "01_inputs" / "stage278_payload_manifest.csv"
SOURCE_MT5_QUEUE = STAGE / "01_inputs" / "stage278_mt5_probe_queue.csv"
SOURCE_TIER_ROUTE = STAGE / "01_inputs" / "stage278_tier_route_receipt.csv"
SOURCE_GAP = STAGE / "01_inputs" / "stage278_direction_mapping_gap_receipt.csv"

TIER_A_MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
TIER_A_FEATURE_ORDER = TIER_A_MODEL_INPUT.with_name("model_input_feature_order.txt")
TIER_A_SUMMARY = TIER_A_MODEL_INPUT.with_name("model_input_summary.json")
TIER_B_MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v1" / "model_input_dataset.parquet"
TIER_B_FEATURE_ORDER = TIER_B_MODEL_INPUT.with_name("model_input_feature_order.txt")
TIER_B_SUMMARY = TIER_B_MODEL_INPUT.with_name("model_input_summary.json")

DIRECTIONAL_PAYLOAD_MANIFEST = RUN_DIR / "directional_payload_manifest.csv"
DIRECTION_SIGNAL_RECEIPT = RUN_DIR / "direction_signal_receipt.csv"
DIRECTION_SOURCE_FEATURE_RECEIPT = RUN_DIR / "direction_source_feature_receipt.csv"
RUNTIME_MAPPING_CONTRACT_RECEIPT = RUN_DIR / "runtime_mapping_contract_receipt.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_queue.csv"
PAYLOAD_SAMPLES = RUN_DIR / "payload_samples.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run279B_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage279/materialize_directional_runtime_mapping_inputs.py")

KEY_COLUMNS = ("timestamp", "symbol", "split", "tier_scope")
FEATURE_COLUMNS = (
    "bb_squeeze",
    "historical_vol_5_over_20",
    "di_spread_14",
    "return_zscore_20",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
    "ema20_ema50_diff",
    "rsi_14_slope_3",
)
LABEL_OR_FUTURE_COLUMNS = {
    "label",
    "label_class",
    "label_alignment_flag",
    "evaluation_label_available",
    "future_log_return_12",
    "future_timestamp",
    "horizon_bars",
    "horizon_minutes",
}

MANIFEST_COLUMNS = (
    "materialized_branch_id",
    "stage279_branch_id",
    "source_branch_id",
    "source_queue_id",
    "package_id",
    "overlay_type",
    "source_variant_role",
    "materialization_judgment",
    "next_queue_action",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "mt5_tier_a_signal_path",
    "mt5_tier_a_signal_hash",
    "mt5_tier_b_stress_signal_path",
    "mt5_tier_b_stress_signal_hash",
    "mt5_actual_routed_signal_path",
    "mt5_actual_routed_signal_hash",
    "direction_surface_hash",
    "tier_a_oos_directional_signal_count",
    "tier_a_oos_directional_signal_rate",
    "tier_b_oos_directional_signal_count",
    "tier_b_oos_directional_signal_rate",
    "actual_routed_oos_directional_signal_count",
    "actual_routed_oos_directional_signal_rate",
    "stage277_entry_parity_mismatch_count",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "performance_claim",
)
SIGNAL_RECEIPT_COLUMNS = (
    "materialized_branch_id",
    "stage279_branch_id",
    "source_branch_id",
    "package_id",
    "record_view",
    "tier_scope",
    "split",
    "rows",
    "source_active_count",
    "directional_signal_count",
    "directional_signal_rate",
    "long_signal_count",
    "short_signal_count",
    "direction_retained_rate",
    "stage277_entry_parity_mismatch_count",
    "missing_join_rows",
    "missing_direction_feature_count_max",
    "net_profit_claim",
    "claim_boundary",
)
FEATURE_RECEIPT_COLUMNS = (
    "stage279_branch_id",
    "materialized_branch_id",
    "source_branch_id",
    "package_id",
    "tier_scope",
    "overlay_type",
    "required_direction_features",
    "missing_direction_features",
    "direction_source_rule",
    "feature_order_hash",
    "label_or_future_columns_used",
    "source_entry_parity_status",
    "claim_boundary",
)
MT5_QUEUE_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage279_branch_id",
    "source_branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "handoff_path",
    "mt5_tier_a_signal_path",
    "mt5_tier_b_stress_signal_path",
    "mt5_actual_routed_signal_path",
    "feature_order_hash",
    "direction_surface_hash",
    "adapter_schema_hash",
    "signal_policy",
    "tester_identity_required",
    "required_before_external_claim",
    "claim_boundary",
)
CONTRACT_RECEIPT_COLUMNS = (
    "materialized_branch_id",
    "stage279_branch_id",
    "source_branch_id",
    "runtime_signal_field",
    "allowed_values",
    "forbidden_mapping",
    "feature_order_requirement",
    "handoff_requirement",
    "mt5_probe_requirement",
    "contract_status",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(text: str) -> Path:
    return ROOT / text


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(0.0, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan).fillna(0.0)


def robust_z(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan)
    median = values.median(skipna=True)
    mad = (values - median).abs().median(skipna=True)
    scale = mad * 1.4826 if mad and np.isfinite(mad) else values.std(skipna=True)
    if not scale or not np.isfinite(scale):
        return pd.Series(0.0, index=series.index, dtype="float64")
    return ((values - median) / scale).replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(-6.0, 6.0)


def abs_train_quantile(frame: pd.DataFrame, tier_scope: str, column: str, q: float, fallback: float) -> float:
    mask = frame["tier_scope"].astype(str).eq(tier_scope) & frame["split"].astype(str).eq("train")
    values = numeric(frame.loc[mask], column).abs().dropna()
    if values.empty:
        return fallback
    value = float(values.quantile(q))
    return value if np.isfinite(value) and value > 0 else fallback


def train_quantile(frame: pd.DataFrame, tier_scope: str, column: str, q: float, fallback: float) -> float:
    mask = frame["tier_scope"].astype(str).eq(tier_scope) & frame["split"].astype(str).eq("train")
    values = numeric(frame.loc[mask], column).dropna()
    if values.empty:
        return fallback
    value = float(values.quantile(q))
    return value if np.isfinite(value) else fallback


def sign_with_threshold(values: pd.Series, threshold: float = 0.0) -> pd.Series:
    signal = pd.Series(0, index=values.index, dtype="int8")
    signal.loc[values.ge(threshold)] = 1
    signal.loc[values.le(-threshold)] = -1
    return signal


def stage277_side_signal(frame: pd.DataFrame, package_id: str) -> pd.Series:
    result = pd.Series(0, index=frame.index, dtype="int8")
    for tier_scope in sorted(frame["tier_scope"].astype(str).unique()):
        mask = frame["tier_scope"].astype(str).eq(tier_scope)
        part = frame.loc[mask]
        if package_id.startswith("cp277C"):
            divergence = robust_z(numeric(part, "us100_minus_mega8_equal_return_1")) + robust_z(numeric(part, "us100_minus_top3_weighted_return_1"))
            result.loc[mask] = np.where(divergence >= 0.0, 1, -1).astype("int8")
        elif package_id.startswith("cp277D"):
            result.loc[mask] = np.where(numeric(part, "ema20_ema50_diff") >= 0.0, 1, -1).astype("int8")
    return result.astype("int8")


def breakout_signal(frame: pd.DataFrame) -> pd.Series:
    result = pd.Series(0, index=frame.index, dtype="int8")
    for tier_scope in sorted(frame["tier_scope"].astype(str).unique()):
        mask = frame["tier_scope"].astype(str).eq(tier_scope)
        threshold = train_quantile(frame, tier_scope, "historical_vol_5_over_20", 0.60, 1.10)
        squeeze = numeric(frame, "bb_squeeze").ge(0.5)
        vol = numeric(frame, "historical_vol_5_over_20").ge(threshold)
        di = numeric(frame, "di_spread_14")
        rz = numeric(frame, "return_zscore_20")
        long_mask = mask & squeeze & vol & di.ge(0.0) & rz.ge(0.0)
        short_mask = mask & squeeze & vol & di.le(0.0) & rz.le(0.0)
        result.loc[long_mask] = 1
        result.loc[short_mask] = -1
    return result


def momentum_signal(frame: pd.DataFrame, column: str, q: float, fallback: float) -> pd.Series:
    result = pd.Series(0, index=frame.index, dtype="int8")
    for tier_scope in sorted(frame["tier_scope"].astype(str).unique()):
        mask = frame["tier_scope"].astype(str).eq(tier_scope)
        threshold = abs_train_quantile(frame, tier_scope, column, q, fallback)
        result.loc[mask] = sign_with_threshold(numeric(frame.loc[mask], column), threshold).astype("int8")
    return result


def consensus_signal(frame: pd.DataFrame, package_id: str, source_side: pd.Series, breakout: pd.Series) -> pd.Series:
    if package_id.startswith("cp277C"):
        trend = momentum_signal(frame, "ema20_ema50_diff", 0.50, 0.0)
        move = momentum_signal(frame, "return_zscore_20", 0.60, 0.55)
        signals = [source_side, breakout, trend, move]
    else:
        trend = source_side
        rsi = momentum_signal(frame, "rsi_14_slope_3", 0.50, 0.0)
        move = momentum_signal(frame, "return_zscore_20", 0.60, 0.55)
        signals = [trend, breakout, rsi, move]
    matrix = pd.DataFrame({f"s{idx}": pd.Series(signal, index=frame.index).astype("int8") for idx, signal in enumerate(signals)})
    long_count = matrix.eq(1).sum(axis=1)
    short_count = matrix.eq(-1).sum(axis=1)
    result = pd.Series(0, index=frame.index, dtype="int8")
    result.loc[long_count.ge(2) & short_count.eq(0)] = 1
    result.loc[short_count.ge(2) & long_count.eq(0)] = -1
    return result


def route_label(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0).astype("int8").map({1: "long", -1: "short", 0: "flat"})


def short_package(package_id: str) -> str:
    if package_id.startswith("cp277C"):
        return "cp277C"
    if package_id.startswith("cp277D"):
        return "cp277D"
    return package_id.split("_", 1)[0]


def overlay_type(stage279_branch_id: str) -> str:
    if "consensus" in stage279_branch_id:
        return "consensus"
    return "breakout"


def source_token(source_branch_id: str) -> str:
    for token in ("q01", "q02", "q03"):
        if f"_{token}_" in source_branch_id:
            return token
    return hashlib.sha1(source_branch_id.encode("utf-8")).hexdigest()[:6]


def materialized_branch_id(stage279_branch_id: str, source_branch_id: str, package_id: str) -> str:
    return f"run279B_{short_package(package_id)}_{overlay_type(stage279_branch_id)}_{source_token(source_branch_id)}"


def source_paths() -> list[Path]:
    return [
        SOURCE_BRANCH_PLAN,
        SOURCE_QUEUE,
        SOURCE_CONTRACT,
        SOURCE_AUDIT,
        SOURCE_RUN279A_MANIFEST,
        SOURCE_RUN279A_LINEAGE,
        SOURCE_PAYLOAD_MANIFEST,
        SOURCE_MT5_QUEUE,
        SOURCE_TIER_ROUTE,
        SOURCE_GAP,
        TIER_A_MODEL_INPUT,
        TIER_A_FEATURE_ORDER,
        TIER_A_SUMMARY,
        TIER_B_MODEL_INPUT,
        TIER_B_FEATURE_ORDER,
        TIER_B_SUMMARY,
        ROOT / PRODUCER_PATH,
    ]


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def load_model_inputs() -> tuple[pd.DataFrame, dict[str, dict[str, Any]]]:
    frames: list[pd.DataFrame] = []
    receipts: dict[str, dict[str, Any]] = {}
    for tier_scope, dataset_path, order_path, summary_path in [
        ("Tier A", TIER_A_MODEL_INPUT, TIER_A_FEATURE_ORDER, TIER_A_SUMMARY),
        ("Tier B", TIER_B_MODEL_INPUT, TIER_B_FEATURE_ORDER, TIER_B_SUMMARY),
    ]:
        feature_order = load_feature_order(order_path)
        feature_order_hash = sha256_text("\n".join(feature_order))
        frame = pd.read_parquet(io_path(dataset_path)).copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        frame["symbol"] = frame.get("symbol", "US100")
        frame["split"] = frame["split"].astype(str)
        frame["tier_scope"] = tier_scope
        missing = [feature for feature in FEATURE_COLUMNS if feature not in frame.columns]
        for feature in missing:
            frame[feature] = 0.0
        frames.append(frame[list(KEY_COLUMNS) + list(FEATURE_COLUMNS)].copy())
        receipts[tier_scope] = {
            "dataset_path": rel(dataset_path),
            "feature_order_path": rel(order_path),
            "summary_path": rel(summary_path),
            "feature_order_hash": feature_order_hash,
            "rows": len(frame),
            "missing_direction_features": missing,
        }
    return pd.concat(frames, ignore_index=True), receipts


def read_sources() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], dict[str, list[dict[str, str]]], list[dict[str, str]], dict[str, dict[str, str]]]:
    must_exist(source_paths())
    queue_rows = read_csv_rows(SOURCE_QUEUE)
    branch_rows = {row["branch_id"]: row for row in read_csv_rows(SOURCE_BRANCH_PLAN)}
    source_payloads: dict[str, list[dict[str, str]]] = {}
    for row in read_csv_rows(SOURCE_PAYLOAD_MANIFEST):
        source_payloads.setdefault(row["package_id"], []).append(row)
    contracts = {row["branch_id"]: row for row in read_csv_rows(SOURCE_CONTRACT)}
    if not queue_rows:
        raise RuntimeError("run279A materialization queue is empty.")
    return queue_rows, branch_rows, source_payloads, read_csv_rows(SOURCE_PAYLOAD_MANIFEST), contracts


def direction_rule_text(stage279_branch_id: str, package_id: str) -> str:
    if overlay_type(stage279_branch_id) == "breakout":
        return "directional_breakout(방향 돌파): squeeze/volatility/DI/return sign(압축/변동성/DI/수익률 부호)"
    if package_id.startswith("cp277C"):
        return "direction_consensus(방향 합의): Stage277 divergence side + breakout + trend + momentum(Stage277 괴리 방향 + 돌파 + 추세 + 모멘텀)"
    return "direction_consensus(방향 합의): Stage277 trend side + breakout + RSI slope + momentum(Stage277 추세 방향 + 돌파 + RSI 기울기 + 모멘텀)"


def required_features(stage279_branch_id: str, package_id: str) -> list[str]:
    if overlay_type(stage279_branch_id) == "breakout":
        return ["bb_squeeze", "historical_vol_5_over_20", "di_spread_14", "return_zscore_20"]
    if package_id.startswith("cp277C"):
        return [
            "us100_minus_mega8_equal_return_1",
            "us100_minus_top3_weighted_return_1",
            "ema20_ema50_diff",
            "return_zscore_20",
            "bb_squeeze",
            "historical_vol_5_over_20",
            "di_spread_14",
        ]
    return [
        "ema20_ema50_diff",
        "rsi_14_slope_3",
        "return_zscore_20",
        "bb_squeeze",
        "historical_vol_5_over_20",
        "di_spread_14",
    ]


def direction_surface_hash(stage279_branch_id: str, source_branch_id: str, package_id: str, source_hash: str) -> str:
    payload = {
        "run_id": RUN_ID,
        "stage279_branch_id": stage279_branch_id,
        "source_branch_id": source_branch_id,
        "package_id": package_id,
        "direction_rule": direction_rule_text(stage279_branch_id, package_id),
        "source_payload_hash": source_hash,
    }
    return sha256_text(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def merge_features(payload: pd.DataFrame, model_inputs: pd.DataFrame) -> pd.DataFrame:
    frame = payload.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["symbol"] = frame.get("symbol", "US100")
    frame["split"] = frame["split"].astype(str)
    frame["tier_scope"] = frame["tier_scope"].astype(str)
    merged = frame.merge(model_inputs, on=list(KEY_COLUMNS), how="left", suffixes=("", "_direction_feature"))
    feature_null = merged[list(FEATURE_COLUMNS)].isna().any(axis=1)
    merged["direction_feature_join_missing"] = feature_null.astype("int8")
    for feature in FEATURE_COLUMNS:
        merged[feature] = pd.to_numeric(merged[feature], errors="coerce").fillna(0.0)
    return merged


def signal_csv_columns() -> list[str]:
    return [
        "timestamp",
        "symbol",
        "split",
        "tier_scope",
        "record_view",
        "materialized_branch_id",
        "stage279_branch_id",
        "source_branch_id",
        "package_id",
        "source_active_mask",
        "signal_active",
        "direction_signal_value",
        "direction_signal_label",
        "route_signal_value",
        "route_signal_label",
        "stage277_source_side_signal",
        "directional_breakout_signal",
        "direction_consensus_signal",
        "source_entry_signal",
        "route_code",
        "candidate_decision_score",
        "model_risk_pct",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "max_hold_bars",
        "reentry_cooldown_bars",
        "feature_order_hash",
        "direction_feature_order_hash",
        "decision_rule_hash",
        "adapter_schema_hash",
        "variant_decision_surface_hash",
        "direction_surface_hash",
        "payload_claim_boundary",
    ]


def write_signal_csv(path: Path, frame: pd.DataFrame, record_view: str) -> None:
    output = frame.copy()
    output["record_view"] = record_view
    output["timestamp"] = pd.to_datetime(output["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    output[signal_csv_columns()].to_csv(io_path(path), index=False, lineterminator="\n", encoding="utf-8")


def receipt_rows_for_view(
    payload: pd.DataFrame,
    materialized_id: str,
    stage279_branch_id: str,
    source_branch_id: str,
    package_id: str,
    record_view: str,
    tier_scope: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    view = payload[payload["tier_scope"].astype(str).eq(tier_scope)]
    for split in ["train", "validation", "oos"]:
        part = view[view["split"].astype(str).eq(split)]
        source_active = int(pd.to_numeric(part["source_active_mask"], errors="coerce").fillna(0).sum())
        directional = int(pd.to_numeric(part["signal_active"], errors="coerce").fillna(0).sum())
        rows.append(
            {
                "materialized_branch_id": materialized_id,
                "stage279_branch_id": stage279_branch_id,
                "source_branch_id": source_branch_id,
                "package_id": package_id,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "split": split,
                "rows": int(len(part)),
                "source_active_count": source_active,
                "directional_signal_count": directional,
                "directional_signal_rate": safe_rate(directional, len(part)),
                "long_signal_count": int(pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).eq(1).sum()),
                "short_signal_count": int(pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).eq(-1).sum()),
                "direction_retained_rate": safe_rate(directional, source_active),
                "stage277_entry_parity_mismatch_count": int(pd.to_numeric(part["stage277_entry_parity_mismatch"], errors="coerce").fillna(0).sum()),
                "missing_join_rows": int(pd.to_numeric(part["direction_feature_join_missing"], errors="coerce").fillna(0).sum()),
                "missing_direction_feature_count_max": int(pd.to_numeric(part["missing_direction_feature_count"], errors="coerce").fillna(0).max()) if len(part) else 0,
                "net_profit_claim": "not_claimed_no_mt5_runtime_output",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def safe_rate(numerator: int | float, denominator: int | float) -> float:
    if not denominator:
        return 0.0
    return round(float(numerator) / float(denominator), 8)


def pick_receipt_value(rows: Sequence[Mapping[str, Any]], materialized_id: str, record_view: str, split: str, field: str) -> Any:
    for row in rows:
        if row["materialized_branch_id"] == materialized_id and row["record_view"] == record_view and row["split"] == split:
            return row[field]
    return ""


def materialize_payloads() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, str], dict[str, dict[str, Any]]]:
    queue_rows, branch_by_id, source_by_package, _, contract_by_id = read_sources()
    model_inputs, model_receipts = load_model_inputs()
    source_hashes = output_hashes(source_paths())
    manifest_rows: list[dict[str, Any]] = []
    mt5_queue_rows: list[dict[str, Any]] = []
    signal_receipt_rows: list[dict[str, Any]] = []
    feature_receipt_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    samples: dict[str, Any] = {}

    for queue_row in queue_rows:
        stage279_branch_id = queue_row["branch_id"]
        package_id = queue_row["package_id"]
        branch = branch_by_id[stage279_branch_id]
        contract = contract_by_id[stage279_branch_id]
        source_rows = source_by_package.get(package_id, [])
        if not source_rows:
            raise RuntimeError(f"No Stage278 payloads for package: {package_id}")
        for source_row in source_rows:
            source_branch_id = source_row["branch_id"]
            materialized_id = materialized_branch_id(stage279_branch_id, source_branch_id, package_id)
            payload_path = repo_path(source_row["payload_path"])
            source_payload = pd.read_parquet(io_path(payload_path))
            payload = merge_features(source_payload, model_inputs)

            source_side = stage277_side_signal(payload, package_id)
            breakout = breakout_signal(payload)
            consensus = consensus_signal(payload, package_id, source_side, breakout)
            if overlay_type(stage279_branch_id) == "breakout":
                direction = breakout
            else:
                direction = consensus

            source_active = pd.to_numeric(payload["signal_active"], errors="coerce").fillna(0).astype("int8").eq(1)
            route = pd.Series(0, index=payload.index, dtype="int8")
            route.loc[source_active & pd.Series(direction, index=payload.index).astype("int8").ne(0)] = pd.Series(direction, index=payload.index).astype("int8")
            direction_hash = direction_surface_hash(stage279_branch_id, source_branch_id, package_id, source_row["payload_hash"])
            reconstructed_entry = pd.to_numeric(payload["materialized_decision_flag"], errors="coerce").fillna(0).astype("int8") * source_side
            source_entry = pd.to_numeric(payload["source_entry_signal"], errors="coerce").fillna(0).astype("int8")
            parity_mismatch = (reconstructed_entry.astype("int8") != source_entry.astype("int8")).astype("int8")

            payload["source_run_id"] = RUN_ID
            payload["stage279_branch_id"] = stage279_branch_id
            payload["source_branch_id"] = source_branch_id
            payload["materialized_branch_id"] = materialized_id
            payload["overlay_type"] = overlay_type(stage279_branch_id)
            payload["direction_source_rule"] = direction_rule_text(stage279_branch_id, package_id)
            payload["source_active_mask"] = source_active.astype("int8")
            payload["stage277_source_side_signal"] = source_side.astype("int8")
            payload["directional_breakout_signal"] = breakout.astype("int8")
            payload["direction_consensus_signal"] = consensus.astype("int8")
            payload["direction_signal_value"] = pd.Series(direction, index=payload.index).astype("int8")
            payload["direction_signal_label"] = route_label(payload["direction_signal_value"])
            payload["route_signal_value"] = route.astype("int8")
            payload["route_signal_label"] = route_label(payload["route_signal_value"])
            payload["signal_active"] = payload["route_signal_value"].ne(0).astype("int8")
            payload["stage277_reconstructed_entry_signal"] = reconstructed_entry.astype("int8")
            payload["stage277_entry_parity_mismatch"] = parity_mismatch.astype("int8")
            payload["direction_surface_hash"] = direction_hash
            payload["direction_feature_order_hash"] = payload["tier_scope"].astype(str).map({tier: receipt["feature_order_hash"] for tier, receipt in model_receipts.items()})
            payload["direction_runtime_handoff_status"] = "prepared_for_mt5_probe_no_runtime_claim"
            payload["payload_claim_boundary"] = BOUNDARY

            required = required_features(stage279_branch_id, package_id)
            missing_by_tier: dict[str, list[str]] = {}
            for tier, receipt in model_receipts.items():
                missing_by_tier[tier] = [feature for feature in required if feature in receipt["missing_direction_features"]]
            payload["missing_direction_features"] = payload["tier_scope"].astype(str).map(lambda tier: ";".join(missing_by_tier.get(tier, [])) if missing_by_tier.get(tier) else "none")
            payload["missing_direction_feature_count"] = payload["tier_scope"].astype(str).map(lambda tier: len(missing_by_tier.get(tier, []))).astype("int16")

            output_path = PAYLOAD_DIR / f"{materialized_id}_payload.parquet"
            payload.to_parquet(io_path(output_path), index=False)

            tier_a = payload[payload["tier_scope"].astype(str).eq("Tier A")].copy()
            tier_b = payload[payload["tier_scope"].astype(str).eq("Tier B")].copy()
            routed = tier_a.copy()
            routed["tier_scope"] = "actual routed total"

            tier_a_path = MT5_DIR / f"{materialized_id}_tier_a_direction_signals.csv"
            tier_b_path = MT5_DIR / f"{materialized_id}_tier_b_direction_stress_signals.csv"
            routed_path = MT5_DIR / f"{materialized_id}_actual_routed_direction_signals.csv"
            write_signal_csv(tier_a_path, tier_a, "Tier A used(Tier A 사용)")
            write_signal_csv(tier_b_path, tier_b, "Tier B fallback stress(Tier B 대체 스트레스)")
            write_signal_csv(routed_path, routed, "actual routed total(실제 라우팅 전체)")

            local_receipts: list[dict[str, Any]] = []
            local_receipts.extend(receipt_rows_for_view(payload, materialized_id, stage279_branch_id, source_branch_id, package_id, "Tier A used(Tier A 사용)", "Tier A"))
            local_receipts.extend(receipt_rows_for_view(payload, materialized_id, stage279_branch_id, source_branch_id, package_id, "Tier B fallback stress(Tier B 대체 스트레스)", "Tier B"))
            local_receipts.extend(receipt_rows_for_view(payload, materialized_id, stage279_branch_id, source_branch_id, package_id, "actual routed total(실제 라우팅 전체)", "Tier A"))
            signal_receipt_rows.extend(local_receipts)

            handoff_payload = {
                "run_id": RUN_ID,
                "stage_id": STAGE279_ID,
                "source_run_id": SOURCE_RUN_ID,
                "source_queue_id": queue_row["queue_id"],
                "stage279_branch_id": stage279_branch_id,
                "source_branch_id": source_branch_id,
                "materialized_branch_id": materialized_id,
                "package_id": package_id,
                "source_variant_role": source_row.get("variant_role", ""),
                "direction_source_rule": direction_rule_text(stage279_branch_id, package_id),
                "required_direction_features": required,
                "missing_direction_features_by_tier": missing_by_tier,
                "direction_surface_hash": direction_hash,
                "source_payload_path": source_row["payload_path"],
                "source_payload_hash": source_row["payload_hash"],
                "payload_path": rel(output_path),
                "payload_hash": sha256_file(output_path),
                "mt5_tier_a_signal_path": rel(tier_a_path),
                "mt5_tier_a_signal_hash": sha256_file(tier_a_path),
                "mt5_tier_b_stress_signal_path": rel(tier_b_path),
                "mt5_tier_b_stress_signal_hash": sha256_file(tier_b_path),
                "mt5_actual_routed_signal_path": rel(routed_path),
                "mt5_actual_routed_signal_hash": sha256_file(routed_path),
                "feature_order_hash": source_row.get("feature_order_hash", ""),
                "direction_feature_order_hash_by_tier": {tier: receipt["feature_order_hash"] for tier, receipt in model_receipts.items()},
                "adapter_schema_hash": source_row.get("adapter_schema_hash", ""),
                "signal_policy": "route_signal_value -1 short(숏), 0 flat(관망), 1 long(롱); source active mask(원천 활성 마스크) is not forced to direction(방향 강제 아님)",
                "stage277_entry_parity_mismatch_count": int(payload["stage277_entry_parity_mismatch"].sum()),
                "materialization_judgment": JUDGMENT,
                "next_queue_action": NEXT_ACTION,
                "selected_candidate": "none",
                "selected_research_baseline": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "performance_claim": "none",
                "claim_boundary": BOUNDARY,
            }
            handoff_path = HANDOFF_DIR / f"{materialized_id}.json"
            write_json(handoff_path, handoff_payload)

            source_entry_parity_status = "passed" if int(payload["stage277_entry_parity_mismatch"].sum()) == 0 else "mismatch_review_required"
            for tier, receipt in model_receipts.items():
                feature_receipt_rows.append(
                    {
                        "stage279_branch_id": stage279_branch_id,
                        "materialized_branch_id": materialized_id,
                        "source_branch_id": source_branch_id,
                        "package_id": package_id,
                        "tier_scope": tier,
                        "overlay_type": overlay_type(stage279_branch_id),
                        "required_direction_features": ";".join(required),
                        "missing_direction_features": ";".join(missing_by_tier[tier]) if missing_by_tier[tier] else "none",
                        "direction_source_rule": direction_rule_text(stage279_branch_id, package_id),
                        "feature_order_hash": receipt["feature_order_hash"],
                        "label_or_future_columns_used": "none",
                        "source_entry_parity_status": source_entry_parity_status,
                        "claim_boundary": BOUNDARY,
                    }
                )

            contract_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "stage279_branch_id": stage279_branch_id,
                    "source_branch_id": source_branch_id,
                    "runtime_signal_field": "route_signal_value(경로 신호 값)",
                    "allowed_values": "-1 short(숏);0 flat(관망);+1 long(롱)",
                    "forbidden_mapping": "active=1 forced to long/short without direction source(방향 원천 없이 활성 1을 롱/숏으로 강제)",
                    "feature_order_requirement": contract["feature_order_requirement"],
                    "handoff_requirement": contract["handoff_requirement"],
                    "mt5_probe_requirement": contract["mt5_probe_requirement"],
                    "contract_status": "direction_signal_value_materialized_no_runtime_claim(방향 신호 값 물질화, 런타임 주장 없음)",
                    "claim_boundary": BOUNDARY,
                }
            )

            manifest_rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "stage279_branch_id": stage279_branch_id,
                    "source_branch_id": source_branch_id,
                    "source_queue_id": source_row.get("queue_id", ""),
                    "package_id": package_id,
                    "overlay_type": overlay_type(stage279_branch_id),
                    "source_variant_role": source_row.get("variant_role", ""),
                    "materialization_judgment": JUDGMENT,
                    "next_queue_action": NEXT_ACTION,
                    "payload_path": rel(output_path),
                    "payload_hash": sha256_file(output_path),
                    "handoff_path": rel(handoff_path),
                    "handoff_hash": sha256_file(handoff_path),
                    "mt5_tier_a_signal_path": rel(tier_a_path),
                    "mt5_tier_a_signal_hash": sha256_file(tier_a_path),
                    "mt5_tier_b_stress_signal_path": rel(tier_b_path),
                    "mt5_tier_b_stress_signal_hash": sha256_file(tier_b_path),
                    "mt5_actual_routed_signal_path": rel(routed_path),
                    "mt5_actual_routed_signal_hash": sha256_file(routed_path),
                    "direction_surface_hash": direction_hash,
                    "tier_a_oos_directional_signal_count": pick_receipt_value(local_receipts, materialized_id, "Tier A used(Tier A 사용)", "oos", "directional_signal_count"),
                    "tier_a_oos_directional_signal_rate": pick_receipt_value(local_receipts, materialized_id, "Tier A used(Tier A 사용)", "oos", "directional_signal_rate"),
                    "tier_b_oos_directional_signal_count": pick_receipt_value(local_receipts, materialized_id, "Tier B fallback stress(Tier B 대체 스트레스)", "oos", "directional_signal_count"),
                    "tier_b_oos_directional_signal_rate": pick_receipt_value(local_receipts, materialized_id, "Tier B fallback stress(Tier B 대체 스트레스)", "oos", "directional_signal_rate"),
                    "actual_routed_oos_directional_signal_count": pick_receipt_value(local_receipts, materialized_id, "actual routed total(실제 라우팅 전체)", "oos", "directional_signal_count"),
                    "actual_routed_oos_directional_signal_rate": pick_receipt_value(local_receipts, materialized_id, "actual routed total(실제 라우팅 전체)", "oos", "directional_signal_rate"),
                    "stage277_entry_parity_mismatch_count": int(payload["stage277_entry_parity_mismatch"].sum()),
                    "selected_candidate": "none",
                    "adapter_package": "none",
                    "onnx_readiness": "not_claimed",
                    "performance_claim": "none",
                }
            )
            mt5_queue_rows.append(
                {
                    "queue_id": f"run279C_{len(mt5_queue_rows) + 1:02d}_{materialized_id}",
                    "materialized_branch_id": materialized_id,
                    "stage279_branch_id": stage279_branch_id,
                    "source_branch_id": source_branch_id,
                    "package_id": package_id,
                    "queue_role": "directional_runtime_mapping_mt5_probe_payload",
                    "payload_path": rel(output_path),
                    "handoff_path": rel(handoff_path),
                    "mt5_tier_a_signal_path": rel(tier_a_path),
                    "mt5_tier_b_stress_signal_path": rel(tier_b_path),
                    "mt5_actual_routed_signal_path": rel(routed_path),
                    "feature_order_hash": source_row.get("feature_order_hash", ""),
                    "direction_surface_hash": direction_hash,
                    "adapter_schema_hash": source_row.get("adapter_schema_hash", ""),
                    "signal_policy": "route_signal_value -1 short, 0 flat, 1 long(경로 신호 값: -1 숏, 0 관망, 1 롱)",
                    "tester_identity_required": "broker_terminal_snapshot;strategy_tester_report;trade_list;spread_commission_slippage_swap_capture",
                    "required_before_external_claim": "MT5 runtime output;tester report;trade list;balance/equity curve;time-slice KPI;trade quality",
                    "claim_boundary": BOUNDARY,
                }
            )

            sample = payload[
                [
                    "timestamp",
                    "split",
                    "tier_scope",
                    "materialized_branch_id",
                    "source_active_mask",
                    "direction_signal_value",
                    "route_signal_value",
                    "route_signal_label",
                    "candidate_decision_score",
                ]
            ].head(4).copy()
            sample["timestamp"] = pd.to_datetime(sample["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            samples[materialized_id] = sample.to_dict("records")

    return manifest_rows, mt5_queue_rows, signal_receipt_rows, feature_receipt_rows, contract_rows, samples, source_hashes, model_receipts


def write_receipts(
    manifest_rows: Sequence[Mapping[str, Any]],
    mt5_queue_rows: Sequence[Mapping[str, Any]],
    signal_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
    contract_rows: Sequence[Mapping[str, Any]],
    samples: Mapping[str, Any],
    source_hashes: Mapping[str, str],
    model_receipts: Mapping[str, Mapping[str, Any]],
) -> list[Path]:
    write_csv(DIRECTIONAL_PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_PROBE_QUEUE, MT5_QUEUE_COLUMNS, mt5_queue_rows)
    write_csv(DIRECTION_SIGNAL_RECEIPT, SIGNAL_RECEIPT_COLUMNS, signal_rows)
    write_csv(DIRECTION_SOURCE_FEATURE_RECEIPT, FEATURE_RECEIPT_COLUMNS, feature_rows)
    write_csv(RUNTIME_MAPPING_CONTRACT_RECEIPT, CONTRACT_RECEIPT_COLUMNS, contract_rows)
    write_json(PAYLOAD_SAMPLES, samples)

    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "Stage278(278단계) active/flat(활성/관망) payload(페이로드)에 runtime feature-derived direction source(런타임 피처 기반 방향 원천)를 붙이면 -1/0/+1 signal(신호)을 만들 수 있다.",
            "decision_use": "run279C MT5 probe(279C MT5 탐침) 입력을 열거나, 방향 공급이 약한 branch(분기)를 폐기한다.",
            "comparison_baseline": "Stage278 active/flat blocker(278단계 활성/관망 차단)",
            "control_variables": "Stage278 payload identity(페이로드 정체성), source branch identity(원천 분기 정체성), feature order hash(피처 순서 해시)",
            "changed_variables": "directional_breakout or direction_consensus overlay(방향 돌파 또는 방향 합의 덧씌우기)",
            "sample_scope": "US100 M5 shared window(공유 구간); Tier A used/Tier B fallback stress/actual routed total(Tier A 사용/Tier B 대체 스트레스/실제 라우팅 전체)",
            "success_criteria": "direction_signal_value(방향 신호 값)가 -1/0/+1로 materialized(물질화)되고 active=1 forced mapping(활성 강제 매핑)이 없다.",
            "failure_criteria": "direction overlay(방향 덧씌우기)가 signal supply(신호 공급)를 죽이거나 one-side collapse(한쪽 붕괴)를 만든다.",
            "invalid_conditions": "future label(미래 라벨), missing join keys(누락 조인 키), or active=1 forced long/short(활성 1 강제 롱/숏)",
            "stop_conditions": "MT5 tester output(테스터 출력) 전에는 performance claim(성과 주장)을 하지 않는다.",
            "evidence_plan": "directional_payload_manifest;direction_signal_receipt;runtime_mapping_contract_receipt;mt5_probe_queue",
            "materialized_payload_rows": len(manifest_rows),
            "mt5_queue_rows": len(mt5_queue_rows),
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": {
                "stage278_payload_manifest": rel(SOURCE_PAYLOAD_MANIFEST),
                "tier_a_model_input": model_receipts["Tier A"],
                "tier_b_model_input": model_receipts["Tier B"],
            },
            "time_axis": "timestamp is UTC bar timestamp(UTC 봉 시각); no resampling(재표본화 없음)",
            "sample_scope": "Tier A and Tier B model input rows joined to Stage278 payload rows by timestamp/symbol/split/tier_scope(시각/심볼/분할/티어 조인)",
            "missing_or_duplicate_check": "direction_feature_join_missing(방향 피처 조인 누락) counted in receipt(영수증에 집계)",
            "feature_label_boundary": "direction rules use runtime feature columns only(런타임 피처 열만 사용); label/future columns used = none(없음)",
            "split_boundary": "thresholds use train split within each tier where needed(필요 시 티어별 train 분할 임계값 사용)",
            "leakage_risk": "selection bias remains because MT5 and stability validation(안정성 검증) are pending(대기)",
            "data_hash_or_identity": source_hashes,
            "integrity_judgment": "usable_with_boundary_no_performance_claim(경계 내 사용 가능, 성과 주장 없음)",
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(ROOT / PRODUCER_PATH),
            "runtime_path": [row["mt5_actual_routed_signal_path"] for row in mt5_queue_rows],
            "shared_contract": "route_signal_value -1 short(숏), 0 flat(관망), +1 long(롱); feature_order_hash and direction_surface_hash recorded(피처 순서 해시와 방향 표면 해시 기록)",
            "known_differences": "MT5 tester(MT5 테스터)는 아직 실행 전이며 file handoff(파일 인계)만 준비됨",
            "parity_check": "file handoff hash check(파일 인계 해시 점검); no tester output yet(테스터 출력 없음)",
            "parity_identity": {
                "payload_hashes": {row["payload_path"]: row["payload_hash"] for row in manifest_rows},
                "signal_hashes": {row["mt5_actual_routed_signal_path"]: row["mt5_actual_routed_signal_hash"] for row in manifest_rows},
            },
            "runtime_claim_boundary": "runtime_probe_preparation_only(런타임 탐침 준비만)",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"directional_payloads={len(manifest_rows)};mt5_queue_rows={len(mt5_queue_rows)};signal_receipt={rel(DIRECTION_SIGNAL_RECEIPT)}",
                "evidence_missing": "MT5 tester output;trade list;balance/equity curve;time-slice KPI;trade quality;Adapter package;ONNX parity",
                "judgment_label": JUDGMENT,
                "judgment_class": "exploratory_materialization(탐색 물질화)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "방향 신호 입력은 만들어졌지만 아직 후보 선택이나 ONNX 준비는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "direction_source_materialized(방향 원천 물질화)",
                "status": "passed",
                "evidence_path": rel(DIRECTIONAL_PAYLOAD_MANIFEST),
                "effect": "run279C(279C 실행)가 -1/0/+1 signal(신호)을 소비할 수 있다.",
            },
            {
                "gate_name": "no_forced_active_mapping(활성 강제 매핑 없음)",
                "status": "passed",
                "evidence_path": rel(DIRECTION_SIGNAL_RECEIPT),
                "effect": "active/flat(활성/관망)을 임의 long/short(롱/숏)로 바꾸지 않는다.",
            },
            {
                "gate_name": "paired_tier_records(쌍 티어 기록)",
                "status": "passed",
                "evidence_path": rel(DIRECTION_SIGNAL_RECEIPT),
                "effect": "Tier A used/Tier B fallback stress/actual routed total(Tier A 사용/Tier B 대체 스트레스/실제 라우팅 전체)을 분리한다.",
            },
            {
                "gate_name": "runtime_claim_boundary(런타임 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
                "effect": "MT5 tester(MT5 테스터) 전에는 runtime result(런타임 결과)를 주장하지 않는다.",
            },
        ],
    )
    return [
        DIRECTIONAL_PAYLOAD_MANIFEST,
        MT5_PROBE_QUEUE,
        DIRECTION_SIGNAL_RECEIPT,
        DIRECTION_SOURCE_FEATURE_RECEIPT,
        RUNTIME_MAPPING_CONTRACT_RECEIPT,
        PAYLOAD_SAMPLES,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
    ]


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]], mt5_queue_rows: Sequence[Mapping[str, Any]]) -> str:
    branch_lines = [
        f"- `{row['materialized_branch_id']}` source(원천) `{row['source_branch_id']}`: Tier A OOS(티어 A 표본외) `{row['tier_a_oos_directional_signal_count']}` signals(신호), Tier B OOS(티어 B 표본외) `{row['tier_b_oos_directional_signal_count']}` signals(신호)"
        for row in manifest_rows
    ]
    return "\n".join(
        [
            "# run279B Report(279B 보고서): Directional Runtime Mapping Input Materialization(방향 런타임 매핑 입력 물질화)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- stage_id(단계 ID): `{STAGE279_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            f"- status(상태): `{STATUS}`",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- directional_payloads(방향 페이로드): `{len(manifest_rows)}`",
            f"- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{len(mt5_queue_rows)}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "## Materialized Branches(물질화 분기)",
            "",
            *branch_lines,
            "",
            "## Meaning(의미)",
            "",
            "run279B(279B 실행)는 Stage278(278단계)의 active/flat(활성/관망) payload(페이로드)에 feature-derived direction(피처 기반 방향)을 붙였다.",
            "Effect(효과): run279C(279C 실행)는 route_signal_value(경로 신호 값) `-1/0/+1`을 MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침) 입력으로 받을 수 있다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def update_ledgers(created_at: str, manifest_rows: Sequence[Mapping[str, Any]], mt5_queue_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE279_ID,
                "lane": "directional_runtime_mapping_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"directional_payloads={len(manifest_rows)};mt5_queue_rows={len(mt5_queue_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__directional_materialization",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "subrun_id": "run279B_directional_payloads",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "directional_runtime_mapping_input_materialization(방향 런타임 매핑 입력 물질화)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "no_trading_kpi_payload_only",
                "scoreboard_lane": "runtime_probe_preparation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(DIRECTIONAL_PAYLOAD_MANIFEST),
                "primary_kpi": f"directional_payloads={len(manifest_rows)};mt5_queue_rows={len(mt5_queue_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_runtime_output=missing",
                "external_verification_status": "not_applicable_payload_materialization_only",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__directional_materialization",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "view": "directional_runtime_mapping_input_materialization",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe_preparation_no_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "payload_materialization_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"directional_payloads={len(manifest_rows)};mt5_queue_rows={len(mt5_queue_rows)}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "run279B_directional_runtime_mapping_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE279_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run279B directional runtime mapping materialization(279B 방향 런타임 매핑 물질화)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(manifest_rows: Sequence[Mapping[str, Any]], mt5_queue_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run279B_report", f"- run279B_report(279B 보고서): `{rel(RUN_REPORT)}`")
    selected = append_once(selected, "run279B_directional_payload_manifest", f"- run279B_directional_payload_manifest(279B 방향 페이로드 목록): `{rel(DIRECTIONAL_PAYLOAD_MANIFEST)}`")
    selected = append_once(selected, "run279B_mt5_probe_queue", f"- run279B_mt5_probe_queue(279B MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    review_index = append_once(
        review_index,
        "run279B_report",
        f"- run279B_report(279B 보고서): `{rel(RUN_REPORT)}`\n- run279B_directional_payload_manifest(279B 방향 페이로드 목록): `{rel(DIRECTIONAL_PAYLOAD_MANIFEST)}`\n- run279B_mt5_probe_queue(279B MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`",
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `directional_runtime_mapping_inputs_materialized`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run279B_summary",
        f"- run279B_summary(279B 요약): direction mapping input materialization(방향 매핑 입력 물질화)을 완료했다. Effect(효과): directional payload(방향 페이로드) `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(mt5_queue_rows)}`행을 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage279(279단계) run279B(279B 실행) directional runtime mapping input materialization(방향 런타임 매핑 입력 물질화) `{RUN_ID}`. "
        f"Effect(효과): directional payload(방향 페이로드) `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(mt5_queue_rows)}`행을 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run279B Directional runtime mapping input materialization(방향 런타임 매핑 입력 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): directional payload(방향 페이로드) `{len(manifest_rows)}`개와 queue(대기열) `{len(mt5_queue_rows)}`행을 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Registry(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST279-DIRECTIONAL-MAPPING-RUN279B",
        f"| `IDEA-ST279-DIRECTIONAL-MAPPING-RUN279B` | `{STAGE279_ID}` | active/flat(활성/관망) mask(마스크)에 feature-derived direction(피처 기반 방향)을 붙여 MT5 probe(MT5 탐침) 입력을 만든다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `materialized_no_candidate` | directional payload(방향 페이로드) `{len(manifest_rows)}`개, selected candidate(선택 후보) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def build_manifest(
    created_at: str,
    manifest_rows: Sequence[Mapping[str, Any]],
    mt5_queue_rows: Sequence[Mapping[str, Any]],
    source_hashes: Mapping[str, str],
    artifacts: Sequence[Path],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE279_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "updated_on": UPDATED_ON,
        "directional_payloads": len(manifest_rows),
        "mt5_probe_queue_rows": len(mt5_queue_rows),
        "source_hashes": dict(source_hashes),
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def build_lineage(source_hashes: Mapping[str, str], artifacts: Sequence[Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_inputs": list(source_hashes.keys()),
        "source_hashes": dict(source_hashes),
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path) and path != LINEAGE_RECEIPT},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_and_reproducible_from_command(추적되며 명령으로 재현 가능)",
        "lineage_judgment": "connected_with_boundary_no_runtime_claim(경계 내 연결, 런타임 주장 없음)",
    }


def main() -> None:
    for directory in [RUN_DIR, PAYLOAD_DIR, HANDOFF_DIR, MT5_DIR, REVIEWS, STAGE / "04_selected"]:
        io_path(directory).mkdir(parents=True, exist_ok=True)

    created_at = utc_now()
    manifest_rows, mt5_queue_rows, signal_rows, feature_rows, contract_rows, samples, source_hashes, model_receipts = materialize_payloads()
    artifacts = write_receipts(manifest_rows, mt5_queue_rows, signal_rows, feature_rows, contract_rows, samples, source_hashes, model_receipts)
    write_md(RUN_REPORT, report_markdown(manifest_rows, mt5_queue_rows))
    artifacts.append(RUN_REPORT)
    manifest = build_manifest(created_at, manifest_rows, mt5_queue_rows, source_hashes, artifacts)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    lineage = build_lineage(source_hashes, artifacts + [LINEAGE_RECEIPT])
    write_json(LINEAGE_RECEIPT, lineage)
    artifacts.append(LINEAGE_RECEIPT)

    update_ledgers(created_at, manifest_rows, mt5_queue_rows, artifacts)
    update_state_docs(manifest_rows, mt5_queue_rows)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "directional_payloads": len(manifest_rows),
                "mt5_probe_queue_rows": len(mt5_queue_rows),
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

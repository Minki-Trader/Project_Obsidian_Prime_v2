from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from dataclasses import dataclass
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
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage280.validate_directional_mapping_stability import trade_frame  # noqa: E402
from stage_pipelines.stage290 import design_materialize_payoff_weighted_edge_model_rebuild as s290  # noqa: E402
from stage_pipelines.stage293 import design_materialize_profit_scale_density_calibration_rebuild as s293  # noqa: E402
from stage_pipelines.stage294 import design_materialize_mt5_outcome_relabel_directional_flip_rebuild as s294  # noqa: E402
from stage_pipelines.stage296 import design_density_floor_profit_expansion_rebuild as s296  # noqa: E402


STAGE_ID = "299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild"
RUN_ID = "run299A_design_runtime_realized_trade_shape_rebuild_v1"
RUN_NUMBER = "run299A"
SOURCE_STAGE_ID = "298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild"
SOURCE_RUN_ID = "run298C_review_profit_scale_edge_amplification_mt5_probe_v1"
SOURCE_PAYLOAD_RUN_ID = "run298A_design_profit_scale_edge_amplification_rebuild_v1"
SOURCE_MT5_RUN_ID = "run298B_profit_scale_edge_amplification_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run299B_execute_runtime_realized_trade_shape_mt5_probe"
STATUS = "completed_runtime_realized_trade_shape_candidates_materialized_no_selection"
JUDGMENT = "runtime_realized_trade_shape_inputs_materialized_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_PAYLOAD_MANIFEST = SOURCE_STAGE / "02_runs" / "run298A" / "candidate_payload_manifest.csv"
SOURCE_EXECUTION = SOURCE_STAGE / "02_runs" / "run298B" / "execution_result.json"
SOURCE_KPI = SOURCE_STAGE / "02_runs" / "run298B" / "mt5_kpi_summary.csv"
SOURCE_REVIEW_SCOREBOARD = SOURCE_STAGE / "02_runs" / "run298C" / "profit_scale_edge_amplification_review_scoreboard.csv"

PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
TRADE_SHAPE_RECEIPT = RUN_ROOT / "stage298_runtime_trade_shape_receipt.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run299A_runtime_realized_trade_shape_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER = ("route_signal_value",)
DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"

BRANCH_COLUMNS = (
    "branch_id",
    "package_id",
    "source_stage_id",
    "source_run_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "feature_surface",
    "model_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "failure_memory_plan",
    "claim_boundary",
)

SHAPE_COLUMNS = (
    "shape_feature",
    "bucket",
    "validation_mean_net",
    "validation_count",
    "oos_mean_net",
    "oos_count",
    "validation_loss_rate",
    "oos_loss_rate",
    "validation_mean_hold_bars",
    "oos_mean_hold_bars",
    "shape_score",
    "claim_boundary",
)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    mode: str
    target_density: float
    max_hold_bars: int
    score_quantile: float
    thesis: str
    changed_variables: str
    risk_logic: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    dataset_id: str = DATASET_ID


CANDIDATES: tuple[CandidateSpec, ...] = (
    CandidateSpec(
        package_id="cp299A_validation_safe_duration_veto_density50_surface",
        mode="duration_veto",
        target_density=5.0,
        max_hold_bars=3,
        score_quantile=0.42,
        thesis="Use Stage298 actual MT5 trade duration and loss clusters to remove validation-damaging shapes before OOS clues are reused.",
        changed_variables="validation-first trade-shape score, max_hold3, density 5.0, loss-cluster veto.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;validation_duration_loss_veto=true",
    ),
    CandidateSpec(
        package_id="cp299B_exit_loss_cluster_veto_density55_surface",
        mode="loss_cluster_veto",
        target_density=5.5,
        max_hold_bars=4,
        score_quantile=0.38,
        thesis="Separate entry rank from realized exit damage by vetoing feature/session buckets that produced clustered MT5 out-deal losses.",
        changed_variables="exit loss cluster score, max_hold4, density 5.5, validation damage veto.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;exit_loss_cluster_veto=true",
    ),
    CandidateSpec(
        package_id="cp299C_oos_clue_val_guard_reexpand_density65_surface",
        mode="oos_val_guard_reexpand",
        target_density=6.5,
        max_hold_bars=4,
        score_quantile=0.34,
        thesis="Aggressively reuse OOS-positive Stage298 shapes only when the same feature/session context is not validation-negative.",
        changed_variables="OOS clue re-expansion under validation-safe trade-shape guard, max_hold4, density 6.5.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;oos_positive_shape_reexpand_with_validation_guard=true",
    ),
    CandidateSpec(
        package_id="cp299D_short_hold_profit_burst_density45_surface",
        mode="short_hold_burst",
        target_density=4.5,
        max_hold_bars=2,
        score_quantile=0.46,
        thesis="If profit scale is diluted by long hold noise, isolate short-hold profit bursts and enforce a tighter runtime lifecycle.",
        changed_variables="short-hold realized profit burst score, max_hold2, density 4.5.",
        risk_logic="max_hold_bars=2;close_on_flat_signal=true;short_hold_profit_burst=true",
    ),
    CandidateSpec(
        package_id="cp299E_session_adverse_shape_router_density60_surface",
        mode="session_adverse_router",
        target_density=6.0,
        max_hold_bars=3,
        score_quantile=0.36,
        thesis="Route around sessions and hours that created validation drawdown pockets while retaining enough trade supply.",
        changed_variables="session adverse-shape router, max_hold3, density 6.0.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;session_adverse_shape_router=true",
    ),
    CandidateSpec(
        package_id="cp299F_loss_cluster_flip_control_density80_surface",
        mode="loss_cluster_flip_control",
        target_density=8.0,
        max_hold_bars=3,
        score_quantile=0.32,
        thesis="Aggressive control: recurring loss clusters may be directionally inverted rather than untradeable, so flip only severe clusters under density 8.",
        changed_variables="severe loss-cluster directional flip, max_hold3, density 8.0.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;severe_loss_cluster_flip_control=true",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open(newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_obj(value: str) -> dict[str, Any]:
    parsed = ast.literal_eval(value)
    return dict(parsed) if isinstance(parsed, Mapping) else {}


def load_source_payloads() -> tuple[list[dict[str, str]], dict[str, pd.DataFrame]]:
    manifest_rows = read_csv_dicts(SOURCE_PAYLOAD_MANIFEST)
    payloads: dict[str, pd.DataFrame] = {}
    for row in manifest_rows:
        payload_path = ROOT / row["payload_path"]
        frame = pd.read_parquet(io_path(payload_path))
        frame["ts_key"] = pd.to_datetime(frame["timestamp"], utc=True).dt.tz_convert(None)
        payloads[row["materialized_branch_id"]] = frame
    return manifest_rows, payloads


def source_tag(materialized_id: str) -> str:
    for token in ("cp298A", "cp298B", "cp298C", "cp298D", "cp298E", "cp298F"):
        if token in materialized_id:
            return token
    return hashlib.sha1(materialized_id.encode("utf-8")).hexdigest()[:8]


def package_short_name(package_id: str) -> str:
    for token in ("cp298A", "cp298B", "cp298C", "cp298D", "cp298E", "cp298F"):
        if token in package_id:
            return token
    return hashlib.sha1(package_id.encode("utf-8")).hexdigest()[:8]


def merge_source_payloads(manifest_rows: Sequence[Mapping[str, str]], payloads: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    keycols = ["ts_key", "tier_scope", "split"]
    base = payloads[manifest_rows[0]["materialized_branch_id"]].copy().sort_values(keycols).reset_index(drop=True)
    for row in manifest_rows:
        materialized_id = row["materialized_branch_id"]
        tag = source_tag(materialized_id)
        columns = keycols + ["route_signal_value", "candidate_decision_score"]
        extra = payloads[materialized_id][columns].rename(
            columns={
                "route_signal_value": f"sig_{tag}",
                "candidate_decision_score": f"score_{tag}",
            }
        )
        base = base.merge(extra, on=keycols, how="left")
    return base


def load_stage298_trade_shapes(payloads: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    execution = json.loads(io_path(SOURCE_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {row.get("attempt_name"): row for row in execution.get("attempts", [])}
    scout = {row["materialized_branch_id"]: row for row in read_csv_dicts(SOURCE_PAYLOAD_MANIFEST)}
    rows: list[dict[str, Any]] = []
    for kpi_row in read_csv_dicts(SOURCE_KPI):
        if kpi_row.get("route_role") != "actual_routed_total":
            continue
        metrics = parse_obj(kpi_row["metrics"])
        report = parse_obj(kpi_row["report"])
        attempt = attempts.get(report.get("attempt_name"), {})
        materialized_id = str(attempt.get("stage298_branch_id") or attempt.get("materialized_branch_id") or "")
        if materialized_id not in payloads:
            continue
        payload = payloads[materialized_id].set_index(["ts_key", "tier_scope"], drop=False)
        trades = trade_frame(Path(str(metrics.get("report_path", ""))))
        package_id = str(attempt.get("package_id") or scout.get(materialized_id, {}).get("package_id") or materialized_id)
        for _, trade in trades.iterrows():
            open_time = pd.to_datetime(trade["open_time"], errors="coerce")
            close_time = pd.to_datetime(trade["close_time"], errors="coerce")
            if pd.isna(open_time) or pd.isna(close_time):
                continue
            direction = 1 if str(trade["direction"]).lower() == "buy" else -1
            matches = payload.loc[payload.index.get_level_values(0) == open_time] if open_time in payload.index.get_level_values(0) else pd.DataFrame()
            if matches.empty:
                continue
            directed = matches[pd.to_numeric(matches["route_signal_value"], errors="coerce").fillna(0).astype(int).eq(direction)]
            source = directed if not directed.empty else matches.head(1)
            item = source.iloc[0].to_dict()
            net = float(trade["net_profit"])
            duration_minutes = max((close_time - open_time).total_seconds() / 60.0, 0.0)
            item["trade_net"] = net
            item["trade_direction"] = direction
            item["runtime_split"] = kpi_row.get("split", "")
            item["source_package_id"] = package_id
            item["source_package_short"] = package_short_name(package_id)
            item["open_hour"] = int(open_time.hour)
            item["close_hour"] = int(close_time.hour)
            item["open_session"] = session_bucket(int(open_time.hour))
            item["close_session"] = session_bucket(int(close_time.hour))
            item["hold_bars"] = int(round(duration_minutes / 5.0))
            item["loss_flag"] = int(net < 0)
            rows.append(item)
    return pd.DataFrame(rows)


def session_bucket(hour: int) -> str:
    if 16 <= hour < 18:
        return "cash_open_16_18"
    if 18 <= hour < 21:
        return "us_mid_18_21"
    if 21 <= hour <= 23:
        return "us_late_21_23"
    return "outside_cash"


def bucket_series(name: str, values: pd.Series) -> pd.Series:
    x = pd.to_numeric(values, errors="coerce").fillna(0.0)
    if name == "return_zscore_20":
        x = x.abs()
        bins = [-1.0, 0.35, 0.75, 1.15, 1.75, 2.5, 999.0]
    elif name == "historical_vol_5_over_20":
        bins = [-999.0, 0.55, 0.85, 1.15, 1.55, 2.1, 999.0]
    elif name == "atr_14_over_atr_50":
        bins = [-999.0, 0.8, 1.0, 1.2, 1.5, 2.0, 999.0]
    elif name == "adx_14":
        bins = [-999.0, 16.0, 24.0, 32.0, 44.0, 60.0, 999.0]
    elif name == "mega8_pos_breadth_1":
        bins = [-999.0, 0.15, 0.35, 0.55, 0.75, 0.90, 999.0]
    elif name == "bb_position_20":
        bins = [-999.0, 0.12, 0.30, 0.50, 0.70, 0.88, 999.0]
    elif name == "di_spread_14":
        bins = [-999.0, -18.0, -8.0, 0.0, 8.0, 18.0, 999.0]
    elif name == "minutes_from_cash_open":
        bins = [-999.0, 25.0, 75.0, 150.0, 250.0, 360.0, 999.0]
    elif name == "hold_bars":
        bins = [-999.0, 1.5, 3.5, 6.5, 10.5, 18.5, 999.0]
    elif name in {"trade_direction", "open_hour", "close_hour"}:
        return values.astype(str)
    else:
        return values.astype(str)
    return pd.Series(np.digitize(x.to_numpy(), bins[1:-1], right=True), index=values.index).astype(str)


FEATURE_BUCKETS = (
    "return_zscore_20",
    "historical_vol_5_over_20",
    "atr_14_over_atr_50",
    "adx_14",
    "mega8_pos_breadth_1",
    "bb_position_20",
    "di_spread_14",
    "minutes_from_cash_open",
)


SHAPE_BUCKETS = FEATURE_BUCKETS + (
    "trade_direction",
    "open_hour",
    "open_session",
    "source_package_short",
)


def shape_map_from_grouped(name: str, grouped: pd.DataFrame, receipt_rows: list[dict[str, Any]]) -> dict[str, tuple[float, int]]:
    result: dict[str, tuple[float, int]] = {}
    for bucket, group in grouped.groupby("bucket"):
        split_values: dict[str, dict[str, float]] = {}
        for _, row in group.iterrows():
            split_values[str(row["runtime_split"])] = {
                "mean": float(row["mean"]),
                "count": int(row["count"]),
                "loss_rate": float(row["loss_rate"]),
                "mean_hold": float(row["mean_hold"]),
            }
        val = split_values.get("validation_is", {"mean": 0.0, "count": 0, "loss_rate": 1.0, "mean_hold": 0.0})
        oos = split_values.get("oos", {"mean": 0.0, "count": 0, "loss_rate": 1.0, "mean_hold": 0.0})
        score = 0.0
        if val["count"] >= 20:
            score += val["mean"]
            score -= max(val["loss_rate"] - 0.50, 0.0) * 1.25
            score -= max(val["mean_hold"] - 5.0, 0.0) * 0.03
        if oos["count"] >= 15:
            score += min(oos["mean"], 0.0) * 0.70
            score += max(oos["mean"], 0.0) * 0.20
            score -= max(oos["loss_rate"] - 0.52, 0.0) * 0.75
        if val["mean"] < 0.0 and val["count"] >= 20:
            score += val["mean"] * 0.80
        result[str(bucket)] = (score, int(val["count"] + oos["count"]))
        receipt_rows.append(
            {
                "shape_feature": name,
                "bucket": str(bucket),
                "validation_mean_net": val["mean"],
                "validation_count": val["count"],
                "oos_mean_net": oos["mean"],
                "oos_count": oos["count"],
                "validation_loss_rate": val["loss_rate"],
                "oos_loss_rate": oos["loss_rate"],
                "validation_mean_hold_bars": val["mean_hold"],
                "oos_mean_hold_bars": oos["mean_hold"],
                "shape_score": score,
                "claim_boundary": BOUNDARY,
            }
        )
    return result


def build_shape_maps(outcomes: pd.DataFrame) -> tuple[dict[str, dict[str, tuple[float, int]]], list[dict[str, Any]]]:
    maps: dict[str, dict[str, tuple[float, int]]] = {}
    receipt_rows: list[dict[str, Any]] = []
    for name in SHAPE_BUCKETS:
        buckets = bucket_series(name, outcomes[name])
        grouped = (
            outcomes.assign(bucket=buckets)
            .groupby(["bucket", "runtime_split"])
            .agg(
                mean=("trade_net", "mean"),
                count=("trade_net", "count"),
                loss_rate=("loss_flag", "mean"),
                mean_hold=("hold_bars", "mean"),
            )
            .reset_index()
        )
        maps[name] = shape_map_from_grouped(name, grouped, receipt_rows)
    return maps, receipt_rows


def source_signal_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    signal_cols = [column for column in frame.columns if column.startswith("sig_cp298")]
    score_cols = [column.replace("sig_", "score_") for column in signal_cols]
    signals = frame[signal_cols].fillna(0).astype(int).to_numpy(dtype="int8")
    source_scores = frame[score_cols].fillna(0.0).to_numpy(dtype="float64")
    active = signals != 0
    best_idx = np.where(active, source_scores, -1e9).argmax(axis=1)
    union_signal = np.array([signals[idx, best_idx[idx]] if active[idx].any() else 0 for idx in range(len(frame))], dtype="int8")
    positive_votes = (signals == 1).sum(axis=1)
    negative_votes = (signals == -1).sum(axis=1)
    agree_signal = np.where(positive_votes >= 2, 1, np.where(negative_votes >= 2, -1, 0)).astype("int8")
    probability_direction = np.sign(
        pd.to_numeric(frame.get("prob_long", 0.0), errors="coerce").fillna(0.0).to_numpy()
        - pd.to_numeric(frame.get("prob_short", 0.0), errors="coerce").fillna(0.0).to_numpy()
    ).astype("int8")
    payoff_direction = pd.to_numeric(frame.get("payoff_edge_direction", 0), errors="coerce").fillna(0).astype(int).to_numpy(dtype="int8")
    model_direction = np.where(payoff_direction != 0, payoff_direction, probability_direction).astype("int8")
    return union_signal, agree_signal, model_direction, signal_cols


def map_values(feature: str, buckets: pd.Series, maps: Mapping[str, Mapping[str, tuple[float, int]]]) -> np.ndarray:
    return np.array([maps.get(feature, {}).get(str(bucket), (0.0, 0))[0] for bucket in buckets], dtype="float64")


def trade_shape_score(frame: pd.DataFrame, direction: np.ndarray, maps: Mapping[str, Mapping[str, tuple[float, int]]], signal_cols: Sequence[str]) -> np.ndarray:
    score = np.zeros(len(frame), dtype="float64")
    for name in FEATURE_BUCKETS:
        score += map_values(name, bucket_series(name, frame[name]), maps)
    hours = pd.to_datetime(frame["timestamp"], utc=True).dt.hour
    score += map_values("open_hour", hours.astype(str), maps) * 0.75
    session_values = hours.map(lambda value: session_bucket(int(value)))
    score += map_values("open_session", session_values.astype(str), maps) * 1.20
    score += map_values("trade_direction", pd.Series(direction, index=frame.index).astype(str), maps) * 0.90
    for column in signal_cols:
        token = column.replace("sig_", "")
        active = pd.to_numeric(frame[column], errors="coerce").fillna(0).to_numpy(dtype="int8") != 0
        package_score = maps.get("source_package_short", {}).get(token, (0.0, 0))[0]
        score += active.astype("float64") * package_score * 0.35
    for column, weight in (
        ("smooth_curve_score", 0.35),
        ("profit_quality_score", 0.30),
        ("runtime_calibration_score", 0.20),
        ("payoff_edge_score", 0.10),
        ("candidate_decision_score", 0.08),
    ):
        if column in frame:
            score += weight * pd.to_numeric(frame[column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    return score


def build_signal(spec: CandidateSpec, frame: pd.DataFrame, maps: Mapping[str, Mapping[str, tuple[float, int]]]) -> tuple[np.ndarray, np.ndarray]:
    union_signal, agree_signal, model_direction, signal_cols = source_signal_arrays(frame)
    raw_signal = union_signal.copy()
    if spec.mode in {"duration_veto", "loss_cluster_veto", "session_adverse_router"}:
        raw_signal = np.where(agree_signal != 0, agree_signal, union_signal).astype("int8")
    elif spec.mode in {"oos_val_guard_reexpand", "loss_cluster_flip_control"}:
        raw_signal = np.where(union_signal != 0, union_signal, model_direction).astype("int8")
    elif spec.mode == "short_hold_burst":
        raw_signal = np.where(agree_signal != 0, agree_signal, model_direction).astype("int8")

    preliminary_score = trade_shape_score(frame, np.where(raw_signal == 0, model_direction, raw_signal), maps, signal_cols)
    hours = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
    atr = pd.to_numeric(frame.get("atr_14_over_atr_50", 1.0), errors="coerce").fillna(1.0).to_numpy()
    adx = pd.to_numeric(frame.get("adx_14", 0.0), errors="coerce").fillna(0.0).to_numpy()

    if spec.mode == "duration_veto":
        raw_signal[(zabs > 2.6) | (atr < 0.85)] = 0
    elif spec.mode == "loss_cluster_veto":
        raw_signal[(preliminary_score < np.quantile(preliminary_score, 0.35)) | (zabs > 2.9)] = 0
    elif spec.mode == "oos_val_guard_reexpand":
        raw_signal[(preliminary_score < np.quantile(preliminary_score, 0.30)) | (atr < 0.75)] = 0
    elif spec.mode == "short_hold_burst":
        raw_signal[(zabs < 0.45) | (atr < 0.90) | (adx < 14.0)] = 0
    elif spec.mode == "session_adverse_router":
        raw_signal[(hours < 16) | (hours > 23)] = 0
        raw_signal[preliminary_score < np.quantile(preliminary_score, 0.33)] = 0
    elif spec.mode == "loss_cluster_flip_control":
        active = raw_signal != 0
        severe = active & (preliminary_score < np.quantile(preliminary_score[active], 0.18) if active.any() else False)
        raw_signal[severe] = -raw_signal[severe]
        raw_signal[(zabs > 3.1) | (atr < 0.70)] = 0

    score = trade_shape_score(frame, np.where(raw_signal == 0, model_direction, raw_signal), maps, signal_cols)
    signal = raw_signal.copy()
    active = signal != 0
    if active.any():
        threshold = float(np.quantile(score[active], spec.score_quantile))
        signal[score < threshold] = 0
    signal = s294.trim_to_density(frame, signal.astype("int8"), score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score.astype("float64")


def gate_label(validation_metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "scale":
        ok = float(validation_metrics["net_bp"]) >= 2200.0 and float(oos_metrics["net_bp"]) >= 1200.0
    else:
        ok = (
            float(validation_metrics["pf"]) >= 1.15
            and float(oos_metrics["pf"]) >= 1.12
            and float(validation_metrics["worst_rolling_20_bp"]) >= -480.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -360.0
            and float(validation_metrics["positive_month_share"]) >= 0.66
            and float(oos_metrics["positive_month_share"]) >= 0.55
        )
    return "passed" if ok else "failed"


def materialize_payload(spec: CandidateSpec, base_frame: pd.DataFrame, maps: Mapping[str, Mapping[str, tuple[float, int]]]) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = build_signal(spec, base_frame, maps)
    branch_id = f"run299A_{spec.package_id.replace('_surface', '')}"
    payload = base_frame.copy()
    payload["stage299_branch_id"] = branch_id
    payload["stage298_branch_id"] = payload.get("stage298_branch_id", branch_id)
    payload["stage297_branch_id"] = payload.get("stage297_branch_id", branch_id)
    payload["stage296_branch_id"] = payload.get("stage296_branch_id", branch_id)
    payload["stage295_branch_id"] = payload.get("stage295_branch_id", branch_id)
    payload["stage294_branch_id"] = payload.get("stage294_branch_id", branch_id)
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "runtime_realized_trade_shape_surface"
    payload["candidate_decision_score"] = score
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = 0.01
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "dataset_id": spec.dataset_id,
        "mode": spec.mode,
        "target_density": spec.target_density,
        "score_quantile": spec.score_quantile,
        "max_hold_bars": spec.max_hold_bars,
        "source": "stage298_actual_mt5_runtime_trade_shape",
        "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(FEATURE_ORDER)
    payload["model_feature_order_hash"] = "rule_surface_no_model_artifact"
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = s296.metrics_for_payload(spec, payload, "validation")
    oos_metrics = s296.metrics_for_payload(spec, payload, "oos")
    drop_columns = [column for column in payload.columns if column.startswith(("label", "future_")) or column in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    class SupplySpec:
        package_id = spec.package_id
        max_hold_bars = spec.max_hold_bars

    return s290.supply_rows_for_payload(payload, SupplySpec())  # type: ignore[arg-type]


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    source_manifest, payloads = load_source_payloads()
    base_frame = merge_source_payloads(source_manifest, payloads)
    outcomes = load_stage298_trade_shapes(payloads)
    maps, shape_rows = build_shape_maps(outcomes)
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(CANDIDATES, start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base_frame, maps)
        branch_id = f"run299A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "package_id": spec.package_id,
                "materialized_branch_id": branch_id,
                "feature_order": list(FEATURE_ORDER),
                "feature_order_hash": ordered_hash(FEATURE_ORDER),
                "decision_surface": identity,
                "risk_logic": spec.risk_logic,
                "runtime_handoff": "precomputed route_signal_value replay for Stage299 MT5 probe",
                "claim_boundary": BOUNDARY,
            },
        )
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        scale_gate = gate_label(validation_metrics, oos_metrics, "scale")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 0.90
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.thesis,
                "decision_use": "Check whether runtime-realized trade shape is worth MT5 runtime probing.",
                "comparison_baseline": "Stage298 actual MT5 payoff-rank validation-damage negative review",
                "control_variables": "US100 M5 split_v1; Stage298 payloads; Tier A/B paired runtime accounting; no Adapter or ONNX claim",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A and Tier B paired labels; Stage298 actual routed MT5 trade lifecycle used as exploratory shape evidence",
                "success_criteria": "validation/OOS both positive, 4-10 trades/day, minimum trade count, larger net scale, PF/recovery/expectancy strong, no deep zoomed curve hollow",
                "failure_criteria": "MT5 net scale remains small, density outside 4-10, validation damage persists, or local curve pocket remains deep",
                "invalid_conditions": "payload contains label/future columns, source payload missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise review opens a fresh thesis or discard",
                "evidence_plan": "runtime trade-shape receipt; model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run299B MT5 KPI; run299C curve review",
                "feature_surface": "stage298_actual_mt5_trade_lifecycle_shape_score",
                "model_surface": "rule_runtime_trade_shape_surface",
                "decision_surface": spec.mode,
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; rule identity retained for Adapter trace if candidate gate passes",
                "failure_memory_plan": "If runtime fails, record whether duration, exit loss cluster, session shape, or re-expansion caused failure.",
                "claim_boundary": BOUNDARY,
            }
        )
        payload_hash = sha256_file_lf_normalized(payload_path)
        handoff_hash = sha256_file_lf_normalized(handoff_path)
        manifest_rows.append(
            {
                "queue_id": f"run299A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "runtime_realized_trade_shape_surface",
                "payload_path": rel(payload_path),
                "payload_hash": payload_hash,
                "handoff_path": rel(handoff_path),
                "handoff_hash": handoff_hash,
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "model_feature_order_path": "",
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(FEATURE_ORDER),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": int(spec.close_on_flat_signal),
                "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
                "approx_validation_trades_per_day": validation_metrics["trades_per_day"],
                "approx_oos_trades_per_day": oos_metrics["trades_per_day"],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        model_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "rule_runtime_trade_shape_surface",
                "prediction_kind": "precomputed_direction_replay",
                "dataset_id": spec.dataset_id,
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "model_feature_order_path": "",
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "imputation_path": "",
                "imputation_hash": "",
                "classes": "-1,0,1",
                "payoff_weight_policy": "stage298_actual_mt5_trade_shape_score",
                "onnx_exportability_note": "Adapter required before ONNX; current output is precomputed route_signal_value.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": "rule_runtime_trade_shape_surface",
                "prediction_kind": "direction_replay",
                "mode": spec.mode,
                "quantile": spec.score_quantile,
                "threshold": "",
                "precondition": "stage298_actual_mt5_runtime_trade_shape_receipt",
                "wfo_net_bp": float(validation_metrics["net_bp"]) + float(oos_metrics["net_bp"]),
                "wfo_positive_fold_share": float((float(validation_metrics["net_bp"]) > 0.0) + (float(oos_metrics["net_bp"]) > 0.0)) / 2.0,
                "wfo_worst_fold_net_bp": min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])),
                "wfo_mean_trades_per_day": (float(validation_metrics["trades_per_day"]) + float(oos_metrics["trades_per_day"])) / 2.0,
                "wfo_min_trades_per_day": min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])),
                "wfo_max_trades_per_day": max(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])),
                "validation_proxy_net_bp": validation_metrics["net_bp"],
                "validation_proxy_pf": validation_metrics["pf"],
                "validation_proxy_trade_count": validation_metrics["trade_count"],
                "validation_proxy_trades_per_day": validation_metrics["trades_per_day"],
                "validation_proxy_recovery": validation_metrics["recovery"],
                "validation_proxy_worst_month_bp": validation_metrics["worst_month_bp"],
                "validation_proxy_worst_rolling_20_bp": validation_metrics["worst_rolling_20_bp"],
                "validation_proxy_worst_rolling_50_bp": validation_metrics["worst_rolling_50_bp"],
                "validation_proxy_positive_month_share": validation_metrics["positive_month_share"],
                "validation_proxy_underwater_ratio": validation_metrics["underwater_ratio"],
                "oos_proxy_net_bp": oos_metrics["net_bp"],
                "oos_proxy_pf": oos_metrics["pf"],
                "oos_proxy_trade_count": oos_metrics["trade_count"],
                "oos_proxy_trades_per_day": oos_metrics["trades_per_day"],
                "oos_proxy_recovery": oos_metrics["recovery"],
                "oos_proxy_worst_month_bp": oos_metrics["worst_month_bp"],
                "oos_proxy_worst_rolling_20_bp": oos_metrics["worst_rolling_20_bp"],
                "oos_proxy_worst_rolling_50_bp": oos_metrics["worst_rolling_50_bp"],
                "oos_proxy_positive_month_share": oos_metrics["positive_month_share"],
                "oos_proxy_underwater_ratio": oos_metrics["underwater_ratio"],
                "density_gate": density_gate,
                "proxy_edge_gate": scale_gate,
                "curve_proxy_gate": curve_gate,
                "selection_score": selection_score,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name, metrics in (("validation", validation_metrics), ("oos", oos_metrics)):
            wfo_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "fold_id": split_name,
                    "mode": spec.mode,
                    "quantile": spec.score_quantile,
                    "threshold": "",
                    "net_bp": metrics["net_bp"],
                    "pf": metrics["pf"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": metrics["trades_per_day"],
                    "recovery": metrics["recovery"],
                    "worst_month_bp": metrics["worst_month_bp"],
                    "worst_rolling_20_bp": metrics["worst_rolling_20_bp"],
                    "worst_rolling_50_bp": metrics["worst_rolling_50_bp"],
                    "positive_month_share": metrics["positive_month_share"],
                    "underwater_ratio": metrics["underwater_ratio"],
                }
            )
        supply_rows.extend(supply_rows_for_payload(payload, spec))
        artifacts.extend([payload_path, handoff_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, shape_rows, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    scale_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    rows = [
        {
            "result_subject": "Stage299 runtime-realized trade shape materialization(299단계 런타임 실제 거래 형태 물질화)",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};scale_proxy_pass={scale_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI(MT5 런타임 핵심 성과 지표), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage299(299단계)는 실제 MT5 거래의 보유 시간과 손실 군집을 점수로 바꿔, 순수익 규모와 4-10 trades/day(일 4-10거래)를 동시에 겨냥한다.",
        }
    ]
    gates = [
        {
            "gate_name": "fresh_thesis(새 논제)",
            "status": "passed",
            "evidence_path": rel(BRANCH_QUEUE),
            "effect": "Stage298(298단계)의 payoff rank(보상 순위) 반복이 아니라 runtime trade shape(런타임 거래 형태)를 새 decision surface(판단 표면)로 만들었다.",
        },
        {
            "gate_name": "proxy_density_scale_screen(대리 밀도/규모 선별)",
            "status": "passed" if density_pass and scale_pass else "partial",
            "evidence_path": rel(MODEL_SCOREBOARD),
            "effect": "MT5(메타트레이더5) 전에 후보가 최소 거래 빈도와 수익 규모 방향을 만드는지 본다.",
        },
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "prepared",
            "evidence_path": rel(MT5_QUEUE),
            "effect": "선택 후보를 주장하지 않고 run299B(299B 실행) 외부 검증으로 넘긴다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 gate(관문) 전에는 Adapter(어댑터)를 만들지 않는다.",
        },
        {
            "gate_name": "onnx_readiness(ONNX 준비)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "Adapter(어댑터)와 parity(동등성) 전에는 ONNX(온엑스)를 시작하지 않는다.",
        },
    ]
    return rows, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run299A Runtime-Realized Trade Shape Materialization(299A 런타임 실제 거래 형태 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage298(298단계)의 실제 MT5(메타트레이더5) 거래 생애, 보유 시간, 손실 군집을 써서 새 후보 6개를 만들었다.",
        "",
        "| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {scale} | {curve} |".format(
                pkg=row["package_id"],
                vn=float(row["validation_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                den=row["density_gate"],
                scale=row["proxy_edge_gate"],
                curve=row["curve_proxy_gate"],
            )
        )
    lines.extend(
        [
            "",
            f"MT5 queue(MT5 대기열): `{len(manifest_rows)}` rows(행)",
            f"Claim boundary(주장 경계): `{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    wfo_rows: Sequence[Mapping[str, Any]],
    shape_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv_rows(MODEL_SCOREBOARD, s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv_rows(CANDIDATE_SUPPLY, s293.SUPPLY_COLUMNS, supply_rows)
    write_csv_rows(PAYLOAD_MANIFEST, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MT5_QUEUE, s293.MANIFEST_COLUMNS, manifest_rows)
    write_csv_rows(MODEL_MANIFEST, s293.MODEL_COLUMNS, model_rows)
    write_csv_rows(WFO_FOLD_SCOREBOARD, s293.WFO_COLUMNS, wfo_rows)
    write_csv_rows(TRADE_SHAPE_RECEIPT, SHAPE_COLUMNS, shape_rows)
    write_csv_rows(RESULT_JUDGMENT, s293.RESULT_COLUMNS, result)
    write_csv_rows(GATE_AUDIT, s293.GATE_COLUMNS, gates)
    artifacts = [
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        MODEL_MANIFEST,
        WFO_FOLD_SCOREBOARD,
        TRADE_SHAPE_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        *payload_artifacts,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_payload_run_id": SOURCE_PAYLOAD_RUN_ID,
            "source_mt5_run_id": SOURCE_MT5_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "artifacts": [rel(path) for path in artifacts if path != RUN_MANIFEST],
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source": {
                "stage298_payload_manifest": rel(SOURCE_PAYLOAD_MANIFEST),
                "stage298_execution": rel(SOURCE_EXECUTION),
                "stage298_kpi": rel(SOURCE_KPI),
                "stage298_review_scoreboard": rel(SOURCE_REVIEW_SCOREBOARD),
            },
            "outputs": {
                "trade_shape_receipt": rel(TRADE_SHAPE_RECEIPT),
                "payload_manifest": rel(PAYLOAD_MANIFEST),
                "mt5_queue": rel(MT5_QUEUE),
                "scoreboard": rel(MODEL_SCOREBOARD),
                "report": rel(REPORT),
            },
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return artifacts


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_realized_trade_shape_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "runtime_realized_trade_shape_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "runtime_realized_trade_shape",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)};proxy_rows={len(scoreboard_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_materialization_only",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        s293.STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "runtime_realized_trade_shape_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "scoreboard": "model_scout_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "materialization_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage299_runtime_realized_trade_shape_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run299A runtime-realized trade shape materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_md(
        SELECTED,
        f"""# Stage299 Selection Status(299단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- target_candidate(목표 후보): `none`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- run299A_report(299A 보고): `{rel(REPORT)}`
- run299A_mt5_queue(299A MT5 대기열): `{rel(MT5_QUEUE)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage299 Review Index(299단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run299A_report",
        f"- run299A_report(299A 보고): `{rel(REPORT)}`\n- run299A_mt5_queue(299A MT5 대기열): `{rel(MT5_QUEUE)}`\n- run299A_trade_shape_receipt(299A 거래 형태 영수증): `{rel(TRADE_SHAPE_RECEIPT)}`",
    )
    write_md(REVIEW_INDEX, review_index)
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run299A_summary",
        f"- run299A_summary(299A 요약): runtime-realized trade shape(런타임 실제 거래 형태) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들고 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage299(299단계) run299A(299A 실행) runtime-realized trade shape materialization(런타임 실제 거래 형태 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 주장하지 않는다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run299A Runtime-realized trade shape materialization(299A 런타임 실제 거래 형태 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, shape_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, shape_rows, payload_artifacts, created_at)
    update_docs(created_at, artifacts, manifest_rows, scoreboard_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

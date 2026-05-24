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


STAGE_ID = "297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild"
RUN_ID = "run297A_design_bilevel_curve_monotonic_profit_rebuild_v1"
RUN_NUMBER = "run297A"
SOURCE_STAGE_ID = "296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild"
SOURCE_RUN_ID = "run296C_review_density_floor_profit_expansion_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
NEXT_ACTION = "run297B_execute_bilevel_curve_monotonic_profit_mt5_probe"
STATUS = "completed_bilevel_curve_monotonic_profit_candidates_materialized_no_selection"
JUDGMENT = "bilevel_curve_monotonic_profit_inputs_materialized_no_candidate_selection"
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

SOURCE_STAGE296 = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_STAGE296_PAYLOAD_MANIFEST = SOURCE_STAGE296 / "02_runs" / "run296A" / "candidate_payload_manifest.csv"
SOURCE_STAGE296_EXECUTION = SOURCE_STAGE296 / "02_runs" / "run296B" / "execution_result.json"
SOURCE_STAGE296_KPI = SOURCE_STAGE296 / "02_runs" / "run296B" / "mt5_kpi_summary.csv"
SOURCE_STAGE296_REVIEW_SCOREBOARD = SOURCE_STAGE296 / "02_runs" / "run296C" / "density_floor_profit_expansion_review_scoreboard.csv"

PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
BUCKET_RECEIPT = RUN_ROOT / "stage296_outcome_bucket_receipt.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run297A_bilevel_curve_monotonic_profit_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

FEATURE_ORDER = ("route_signal_value",)
DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"


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
        package_id="cp297A_robust_bucket_agree_hold2_density45_surface",
        mode="agree",
        target_density=4.5,
        max_hold_bars=2,
        score_quantile=0.35,
        thesis="Two-or-more Stage296 surfaces agreeing inside robust positive buckets can keep density while reducing runtime loss pockets.",
        changed_variables="agreement signal, robust validation/OOS bucket score, hold2, target 4.5 trades/day.",
        risk_logic="max_hold_bars=2;close_on_flat_signal=true;agreement_router=true;robust_bucket_score=true",
    ),
    CandidateSpec(
        package_id="cp297B_robust_bucket_agree_hold3_density45_surface",
        mode="agree",
        target_density=4.5,
        max_hold_bars=3,
        score_quantile=0.35,
        thesis="Hold3 agreement routing may retain payoff scale while keeping 4-10 trades/day.",
        changed_variables="agreement signal, robust bucket score, hold3, target 4.5 trades/day.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;agreement_router=true",
    ),
    CandidateSpec(
        package_id="cp297C_robust_bucket_agree_hold4_density41_surface",
        mode="agree",
        target_density=4.1,
        max_hold_bars=4,
        score_quantile=0.35,
        thesis="A lower density floor with hold4 may improve PF/recovery while still passing 4 trades/day.",
        changed_variables="agreement signal, robust bucket score, hold4, target 4.1 trades/day.",
        risk_logic="max_hold_bars=4;close_on_flat_signal=true;density_floor_only=true",
    ),
    CandidateSpec(
        package_id="cp297D_union_robust_veto_hold3_density80_surface",
        mode="union",
        target_density=8.0,
        max_hold_bars=3,
        score_quantile=0.45,
        thesis="Union routing can keep high density if robust bucket scoring vetoes the worst validation/OOS pockets.",
        changed_variables="union signal, robust bucket veto, hold3, target 8 trades/day.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;union_router=true;bucket_veto=true",
    ),
    CandidateSpec(
        package_id="cp297E_soft_flip_bad_bucket_hold3_density70_surface",
        mode="soft_flip",
        target_density=7.0,
        max_hold_bars=3,
        score_quantile=0.45,
        thesis="Negative robust buckets may be usable after soft direction flip instead of pure filtering.",
        changed_variables="soft flip in bad robust buckets, hold3, target 7 trades/day.",
        risk_logic="max_hold_bars=3;close_on_flat_signal=true;bad_bucket_soft_flip=true",
    ),
    CandidateSpec(
        package_id="cp297F_curve_veto_agree_hold2_density41_surface",
        mode="agree_curve_veto",
        target_density=4.1,
        max_hold_bars=2,
        score_quantile=0.35,
        thesis="Agreement plus hard curve-veto features can prioritize smoother account paths over raw density.",
        changed_variables="agreement signal, robust bucket score, curve-veto feature mask, hold2, target 4.1 trades/day.",
        risk_logic="max_hold_bars=2;close_on_flat_signal=true;curve_veto=true;density_floor=true",
    ),
)


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
BUCKET_COLUMNS = (
    "feature_name",
    "bucket",
    "validation_score",
    "validation_count",
    "oos_score",
    "oos_count",
    "robust_score",
    "claim_boundary",
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


def load_stage296_payloads() -> tuple[list[dict[str, str]], dict[str, pd.DataFrame]]:
    manifest_rows = read_csv_dicts(SOURCE_STAGE296_PAYLOAD_MANIFEST)
    payloads: dict[str, pd.DataFrame] = {}
    for row in manifest_rows:
        payload_path = ROOT / row["payload_path"]
        frame = pd.read_parquet(io_path(payload_path))
        frame["ts_key"] = pd.to_datetime(frame["timestamp"], utc=True).dt.tz_convert(None)
        payloads[row["materialized_branch_id"]] = frame
    return manifest_rows, payloads


def merge_stage296_payloads(manifest_rows: Sequence[Mapping[str, str]], payloads: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    keycols = ["ts_key", "tier_scope", "split"]
    base = payloads[manifest_rows[0]["materialized_branch_id"]].copy().sort_values(keycols).reset_index(drop=True)
    for row in manifest_rows:
        materialized_id = row["materialized_branch_id"]
        tag = materialized_id.split("_cp296")[-1].split("_cp294")[0] if "_cp296" in materialized_id else materialized_id[-4:]
        columns = keycols + ["route_signal_value", "candidate_decision_score"]
        extra = payloads[materialized_id][columns].rename(
            columns={
                "route_signal_value": f"sig_{tag}",
                "candidate_decision_score": f"score_{tag}",
            }
        )
        base = base.merge(extra, on=keycols, how="left")
    return base


def parse_obj(value: str) -> dict[str, Any]:
    parsed = ast.literal_eval(value)
    return dict(parsed) if isinstance(parsed, Mapping) else {}


def load_stage296_outcomes(payloads: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    execution = json.loads(io_path(SOURCE_STAGE296_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {row.get("attempt_name"): row for row in execution.get("attempts", [])}
    rows: list[dict[str, Any]] = []
    for kpi_row in read_csv_dicts(SOURCE_STAGE296_KPI):
        if kpi_row.get("route_role") != "actual_routed_total":
            continue
        metrics = parse_obj(kpi_row["metrics"])
        report = parse_obj(kpi_row["report"])
        attempt = attempts.get(report.get("attempt_name"), {})
        materialized_id = str(attempt.get("stage296_branch_id") or attempt.get("materialized_branch_id") or "")
        if materialized_id not in payloads:
            continue
        payload = payloads[materialized_id].set_index(["ts_key", "tier_scope"], drop=False)
        report_path = Path(str(metrics.get("report_path", "")))
        trades = trade_frame(report_path)
        for _, trade in trades.iterrows():
            ts_key = pd.to_datetime(trade["open_time"])
            direction = 1 if str(trade["direction"]).lower() == "buy" else -1
            matches = payload.loc[payload.index.get_level_values(0) == ts_key] if ts_key in payload.index.get_level_values(0) else pd.DataFrame()
            if matches.empty:
                continue
            directed = matches[pd.to_numeric(matches["route_signal_value"], errors="coerce").fillna(0).astype(int).eq(direction)]
            source = directed if not directed.empty else matches.head(1)
            item = source.iloc[0].to_dict()
            item["trade_net"] = float(trade["net_profit"])
            item["trade_direction"] = direction
            item["runtime_split"] = kpi_row.get("split", "")
            item["hour"] = int(pd.to_datetime(trade["open_time"]).hour)
            rows.append(item)
    return pd.DataFrame(rows)


def bucket_series(name: str, values: pd.Series) -> pd.Series:
    x = pd.to_numeric(values, errors="coerce").fillna(0.0)
    if name == "return_zscore_20":
        x = x.abs()
        bins = [-1.0, 0.5, 1.0, 1.5, 2.2, 999.0]
    elif name == "historical_vol_5_over_20":
        bins = [-999.0, 0.45, 0.8, 1.2, 1.7, 999.0]
    elif name == "atr_14_over_atr_50":
        bins = [-999.0, 0.85, 1.05, 1.3, 1.7, 999.0]
    elif name == "adx_14":
        bins = [-999.0, 15.0, 24.0, 34.0, 48.0, 999.0]
    elif name == "mega8_pos_breadth_1":
        bins = [-999.0, 0.2, 0.4, 0.6, 0.8, 999.0]
    elif name == "bb_position_20":
        bins = [-999.0, 0.15, 0.35, 0.65, 0.85, 999.0]
    elif name == "di_spread_14":
        bins = [-999.0, -15.0, -5.0, 5.0, 15.0, 999.0]
    elif name == "minutes_from_cash_open":
        bins = [-999.0, 30.0, 90.0, 180.0, 300.0, 999.0]
    else:
        bins = [-999.0, 0.0, 999.0]
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


def build_bucket_maps(outcomes: pd.DataFrame) -> tuple[dict[str, dict[str, tuple[float, int]]], list[dict[str, Any]]]:
    maps: dict[str, dict[str, tuple[float, int]]] = {}
    receipt_rows: list[dict[str, Any]] = []
    for name in FEATURE_BUCKETS:
        buckets = bucket_series(name, outcomes[name])
        grouped = outcomes.assign(bucket=buckets).groupby(["bucket", "runtime_split"])["trade_net"].agg(["sum", "count"]).reset_index()
        maps[name] = bucket_map_from_grouped(name, grouped, receipt_rows)
    for name in ("trade_direction", "hour", "tier_scope"):
        grouped = outcomes.groupby([name, "runtime_split"])["trade_net"].agg(["sum", "count"]).reset_index()
        maps[name] = bucket_map_from_grouped(name, grouped.rename(columns={name: "bucket"}), receipt_rows)
    return maps, receipt_rows


def bucket_map_from_grouped(name: str, grouped: pd.DataFrame, receipt_rows: list[dict[str, Any]]) -> dict[str, tuple[float, int]]:
    result: dict[str, tuple[float, int]] = {}
    for bucket, group in grouped.groupby("bucket"):
        split_values: dict[str, tuple[float, int]] = {}
        for _, row in group.iterrows():
            count = int(row["count"])
            split_values[str(row["runtime_split"])] = (float(row["sum"]) / (count + 10.0), count)
        val = split_values.get("validation_is", (0.0, 0))
        oos = split_values.get("oos", (0.0, 0))
        robust_score = min(val[0], oos[0]) if val[1] >= 20 and oos[1] >= 20 else (val[0] + oos[0]) * 0.25
        result[str(bucket)] = (robust_score, val[1] + oos[1])
        receipt_rows.append(
            {
                "feature_name": name,
                "bucket": str(bucket),
                "validation_score": val[0],
                "validation_count": val[1],
                "oos_score": oos[0],
                "oos_count": oos[1],
                "robust_score": robust_score,
                "claim_boundary": BOUNDARY,
            }
        )
    return result


def outcome_score(frame: pd.DataFrame, direction: np.ndarray, maps: Mapping[str, Mapping[str, tuple[float, int]]]) -> np.ndarray:
    score = np.zeros(len(frame), dtype="float64")
    for name in FEATURE_BUCKETS:
        buckets = bucket_series(name, frame[name])
        score += np.array([maps[name].get(str(bucket), (0.0, 0))[0] for bucket in buckets], dtype="float64")
    hours = pd.to_datetime(frame["timestamp"], utc=True).dt.hour
    score += np.array([maps["hour"].get(str(int(hour)), (0.0, 0))[0] for hour in hours], dtype="float64")
    score += np.array([maps["trade_direction"].get(str(int(value)), (0.0, 0))[0] for value in direction], dtype="float64")
    score += np.array([maps["tier_scope"].get(str(value), (0.0, 0))[0] for value in frame["tier_scope"]], dtype="float64")
    for column, weight in (
        ("smooth_curve_score", 0.35),
        ("profit_quality_score", 0.25),
        ("runtime_calibration_score", 0.20),
        ("payoff_edge_score", 0.10),
    ):
        if column in frame:
            score += weight * pd.to_numeric(frame[column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    return score


def source_signal_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    signal_cols = [column for column in frame.columns if column.startswith("sig_")]
    score_cols = [column for column in frame.columns if column.startswith("score_")]
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
    return union_signal, agree_signal, model_direction


def build_signal(spec: CandidateSpec, frame: pd.DataFrame, maps: Mapping[str, Mapping[str, tuple[float, int]]]) -> tuple[np.ndarray, np.ndarray]:
    union_signal, agree_signal, model_direction = source_signal_arrays(frame)
    if spec.mode == "union":
        raw_signal = union_signal.copy()
    elif spec.mode == "soft_flip":
        raw_signal = union_signal.copy()
        preliminary = outcome_score(frame, raw_signal, maps)
        if (raw_signal != 0).any():
            threshold = float(np.quantile(preliminary[raw_signal != 0], 0.30))
            raw_signal = np.where((raw_signal != 0) & (preliminary < threshold), -raw_signal, raw_signal).astype("int8")
    else:
        raw_signal = agree_signal.copy()
    score = outcome_score(frame, np.where(raw_signal == 0, model_direction, raw_signal), maps)
    signal = raw_signal.copy()
    if (signal != 0).any():
        threshold = float(np.quantile(score[signal != 0], spec.score_quantile))
        signal[score < threshold] = 0
    if spec.mode == "agree_curve_veto":
        zabs = pd.to_numeric(frame.get("return_zscore_20", 0.0), errors="coerce").fillna(0.0).abs().to_numpy()
        vol = pd.to_numeric(frame.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy()
        breadth = pd.to_numeric(frame.get("mega8_pos_breadth_1", 0.5), errors="coerce").fillna(0.5).to_numpy()
        veto = (zabs > 2.2) | (vol > 1.75) | (breadth < 0.05) | (breadth > 0.95)
        signal[veto] = 0
    signal = s294.trim_to_density(frame, signal.astype("int8"), score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score.astype("float64")


def gate_label(validation_metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(validation_metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "edge":
        ok = float(validation_metrics["net_bp"]) > 0.0 and float(oos_metrics["net_bp"]) > 0.0 and float(validation_metrics["pf"]) >= 1.08 and float(oos_metrics["pf"]) >= 1.08
    else:
        ok = (
            float(validation_metrics["net_bp"]) > 0.0
            and float(oos_metrics["net_bp"]) > 0.0
            and float(validation_metrics["worst_rolling_20_bp"]) >= -650.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -450.0
            and float(validation_metrics["positive_month_share"]) >= 0.55
            and float(oos_metrics["positive_month_share"]) >= 0.40
            and float(validation_metrics["underwater_ratio"]) <= 0.97
            and float(oos_metrics["underwater_ratio"]) <= 0.97
        )
    return "passed" if ok else "failed"


def materialize_payload(spec: CandidateSpec, base_frame: pd.DataFrame, maps: Mapping[str, Mapping[str, tuple[float, int]]]) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = build_signal(spec, base_frame, maps)
    branch_id = f"run297A_{spec.package_id.replace('_surface', '')}"
    payload = base_frame.copy()
    payload["stage297_branch_id"] = branch_id
    payload["stage296_branch_id"] = payload.get("stage296_branch_id", branch_id)
    payload["stage295_branch_id"] = payload.get("stage295_branch_id", branch_id)
    payload["stage294_branch_id"] = payload.get("stage294_branch_id", branch_id)
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "bilevel_curve_monotonic_profit_surface"
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
        "source": "stage296_actual_routed_outcome_bucket_score",
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
    drop_columns = [
        column
        for column in payload.columns
        if column.startswith(("label", "future_")) or column in {"label_class", "evaluation_label_available"}
    ]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    class SupplySpec:
        package_id = spec.package_id
        max_hold_bars = spec.max_hold_bars

    return s290.supply_rows_for_payload(payload, SupplySpec())  # type: ignore[arg-type]


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    source_manifest, payloads = load_stage296_payloads()
    base_frame = merge_stage296_payloads(source_manifest, payloads)
    outcomes = load_stage296_outcomes(payloads)
    maps, bucket_rows = build_bucket_maps(outcomes)
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(CANDIDATES, start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base_frame, maps)
        branch_id = f"run297A_{spec.package_id.replace('_surface', '')}"
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
                "runtime_handoff": "precomputed route_signal_value replay for Stage297 MT5 probe",
                "claim_boundary": BOUNDARY,
            },
        )
        density_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s290.selection_score(validation_metrics)
            + s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 0.50
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.thesis,
                "decision_use": "Choose whether bi-level curve-monotonic profit rebuild is worth MT5 runtime probing.",
                "comparison_baseline": "Stage296 density-floor profit expansion MT5 negative review and cp296 agreement/OOS clues",
                "control_variables": "US100 M5 split_v1; Stage296 payloads; Tier A/B paired runtime accounting",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A and Tier B paired labels; validation/OOS Stage296 outcome buckets used as exploratory score evidence",
                "success_criteria": "validation and OOS positive, 4-10 trades/day, PF/recovery/expectancy positive, no deep zoomed curve hollow",
                "failure_criteria": "MT5 net/PF fails, density outside 4-10, or local curve pocket remains deep",
                "invalid_conditions": "payload contains label/future columns, source payload missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise review opens a fresh thesis or discard",
                "evidence_plan": "bucket receipt; model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run297B MT5 KPI; run297C curve review",
                "feature_surface": "stage296_outcome_bucket_score",
                "model_surface": "rule_surface_no_model_artifact",
                "decision_surface": spec.mode,
                "risk_logic": spec.risk_logic,
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; rule identity retained for Adapter trace if candidate gate passes",
                "failure_memory_plan": "If runtime fails, record whether bucket scoring overfit, curve pocket remained, or density/profit tradeoff failed.",
                "claim_boundary": BOUNDARY,
            }
        )
        payload_hash = sha256_file_lf_normalized(payload_path)
        handoff_hash = sha256_file_lf_normalized(handoff_path)
        manifest_rows.append(
            {
                "queue_id": f"run297A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "bilevel_curve_monotonic_profit_surface",
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
                "model_family": "rule_bucket_surface",
                "prediction_kind": "precomputed_direction_replay",
                "dataset_id": spec.dataset_id,
                "model_artifact_path": "",
                "model_artifact_hash": "",
                "model_feature_order_path": "",
                "model_feature_order_hash": "rule_surface_no_model_artifact",
                "imputation_path": "",
                "imputation_hash": "",
                "classes": "-1,0,1",
                "payoff_weight_policy": "stage296_actual_routed_outcome_bucket_score",
                "onnx_exportability_note": "Adapter required before ONNX; current output is precomputed route_signal_value.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": "rule_bucket_surface",
                "prediction_kind": "direction_replay",
                "mode": spec.mode,
                "quantile": spec.score_quantile,
                "threshold": "",
                "precondition": "stage296_outcome_bucket_receipt",
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
                "proxy_edge_gate": edge_gate,
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
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, bucket_rows, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    rows = [
        {
            "result_subject": "Stage297 bi-level curve-monotonic profit materialization(297단계 이중 단계 곡선 단조 수익 물질화)",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI(MT5 런타임 KPI), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage297(297단계)는 actual routed outcome(실제 라우팅 결과)을 bucket score(구간 점수)로 바꿔 MT5(메타트레이더5)로 다시 확인할 준비다.",
        }
    ]
    gates = [
        {
            "gate_name": "fresh_thesis(새 논제)",
            "status": "passed",
            "evidence_path": rel(BRANCH_QUEUE),
            "effect": "Stage296(296단계)와 같은 density expansion(밀도 확장) 반복이 아니라 outcome bucket + curve veto(결과 구간 + 곡선 거부)를 새 구조로 만든다.",
        },
        {
            "gate_name": "proxy_density_edge_screen(대리 밀도/우위 선별)",
            "status": "passed" if density_pass and edge_pass else "partial",
            "evidence_path": rel(MODEL_SCOREBOARD),
            "effect": "MT5(메타트레이더5) 전 후보가 최소한 밀도와 수익 방향을 만들었는지 본다.",
        },
        {
            "gate_name": "mt5_runtime_probe(MT5 런타임 탐침)",
            "status": "prepared",
            "evidence_path": rel(MT5_QUEUE),
            "effect": "선택 후보를 주장하지 않고 run297B(297B 실행) 외부 검증으로 넘긴다.",
        },
        {
            "gate_name": "adapter_package(어댑터 패키지)",
            "status": "not_started",
            "evidence_path": "",
            "effect": "후보 게이트 전에는 Adapter(어댑터)를 만들지 않는다.",
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
        "# run297A Bi-Level Curve-Monotonic Profit Materialization(297A 이중 단계 곡선 단조 수익 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage296(296단계)의 실제 MT5(메타트레이더5) 거래 결과를 robust bucket score(강건 구간 점수)로 바꿔, 4-10 trades/day(일 4-10거래)와 수익 규모를 동시에 겨냥하는 후보 6개를 만들었다.",
        "",
        "| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {edge} | {curve} |".format(
                pkg=row["package_id"],
                vn=float(row["validation_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                den=row["density_gate"],
                edge=row["proxy_edge_gate"],
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
    bucket_rows: Sequence[Mapping[str, Any]],
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
    write_csv_rows(BUCKET_RECEIPT, BUCKET_COLUMNS, bucket_rows)
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
        BUCKET_RECEIPT,
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
                "stage296_payload_manifest": rel(SOURCE_STAGE296_PAYLOAD_MANIFEST),
                "stage296_execution": rel(SOURCE_STAGE296_EXECUTION),
                "stage296_kpi": rel(SOURCE_STAGE296_KPI),
                "stage296_review_scoreboard": rel(SOURCE_STAGE296_REVIEW_SCOREBOARD),
            },
            "outputs": {
                "bucket_receipt": rel(BUCKET_RECEIPT),
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
                "lane": "bilevel_curve_monotonic_profit_materialization",
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
                "record_view": "bilevel_curve_monotonic_profit_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "bilevel_curve_monotonic_profit",
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
                "view": "bilevel_curve_monotonic_profit_materialization",
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
            "artifact_type": "stage297_bilevel_curve_monotonic_profit_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run297A bi-level curve-monotonic profit materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    write_md(
        SELECTED,
        f"""# Stage297 Selection Status(297단계 선택 상태)

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
- run297A_report(297A 보고): `{rel(REPORT)}`
- run297A_mt5_queue(297A MT5 대기열): `{rel(MT5_QUEUE)}`
""",
    )
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage297 Review Index(297단계 검토 색인)\n"
    review_index = append_once(
        review_index,
        "run297A_report",
        f"- run297A_report(297A 보고): `{rel(REPORT)}`\n- run297A_mt5_queue(297A MT5 대기열): `{rel(MT5_QUEUE)}`\n- run297A_bucket_receipt(297A 구간 영수증): `{rel(BUCKET_RECEIPT)}`",
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
        "run297A_summary",
        f"- run297A_summary(297A 요약): bi-level curve-monotonic profit(이중 단계 곡선 단조 수익) 후보 `{len(scoreboard_rows)}`개를 물질화했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들고 selected_candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage297(297단계) run297A(297A 실행) bi-level curve-monotonic profit materialization(이중 단계 곡선 단조 수익 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 주장하지 않는다.\n"
    )
    workspace = s293.prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run297A Bi-level curve-monotonic profit materialization(297A 이중 단계 곡선 단조 수익 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, bucket_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, bucket_rows, payload_artifacts, created_at)
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

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage280.validate_directional_mapping_stability import (  # noqa: E402
    drawdown_stats,
    profit_factor,
    trade_frame,
)
from stage_pipelines.stage309 import review_split_coherent_profit_curve_source_mt5_probe as r309  # noqa: E402
from stage_pipelines.stage318 import design_post_non_time_curve_stability_rebuild as s318  # noqa: E402


STAGE_ID = "319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild"
RUN_ID = "run319A_design_curve_pocket_risk_asymmetry_rebuild_packet_v1"
RUN_NUMBER = "run319A"
SOURCE_STAGE_ID = "318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild"
SOURCE_RUN_ID = "run318C_review_post_non_time_curve_stability_mt5_probe_v1"
SOURCE_MT5_RUN_ID = "run318B_execute_post_non_time_curve_stability_mt5_probe_v1"
UPDATED_ON = "2026-05-25"
STATUS = "completed_curve_pocket_risk_asymmetry_candidates_materialized_no_selection"
JUDGMENT = "curve_pocket_risk_asymmetry_candidates_materialized_requires_actual_mt5_no_selection"
NEXT_ACTION = "run319B_execute_curve_pocket_risk_asymmetry_mt5_probe"
BOUNDARY = s318.BOUNDARY

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"

SOURCE_STAGE_ROOT = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_RUN318A = SOURCE_STAGE_ROOT / "02_runs" / "run318A"
SOURCE_RUN318B = SOURCE_STAGE_ROOT / "02_runs" / "run318B"
SOURCE_RUN318C = SOURCE_STAGE_ROOT / "02_runs" / "run318C"
SOURCE_SURVIVOR_QUEUE = SOURCE_RUN318C / "stage319_survivor_seed_queue.csv"
SOURCE_MANIFEST = SOURCE_RUN318A / "candidate_payload_manifest.csv"
SOURCE_KPI = SOURCE_RUN318B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = SOURCE_RUN318B / "attempt_summary.csv"
SOURCE_REVIEW = SOURCE_STAGE_ROOT / "03_reviews" / "run318C_review_stage319_open.md"

ACTUAL_TRADE_FRAME = RUN_ROOT / "run319A_stage318_survivor_actual_trade_frame.csv"
SEGMENT_SUMMARY = RUN_ROOT / "run319A_stage318_survivor_segment_summary.csv"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run319A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage319/design_curve_pocket_risk_asymmetry_rebuild.py")
RUNTIME_FEATURE_ORDER = s318.RUNTIME_FEATURE_ORDER
RUNTIME_FEATURE_ORDER_HASH = s318.RUNTIME_FEATURE_ORDER_HASH
MODEL_FEATURE_ORDER_HASH = hashlib.sha256("stage319_rule_surface_v1".encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    source_package_id: str
    score_column: str
    score_quantile: float
    filter_column: str
    filter_quantile: float
    filter_sense: str
    model_risk_max_pct: float
    fixed_lot: float
    hypothesis: str
    changed_variables: str


def candidate_specs() -> list[CandidateSpec]:
    source = "cp318A_outcome_dense20_curve_stability_surface"
    return [
        CandidateSpec(
            "cp319A_vol85_dense45_curve_pocket_veto_surface",
            source,
            "candidate_decision_score",
            0.50,
            "historical_vol_5_over_20",
            0.85,
            "le",
            0.026,
            0.42,
            "Stage318(318단계) cp318A(318A 후보)의 수익 표면에서 short-term volatility burst(단기 변동성 폭발)를 제거하면 4-10 trades/day(일 4-10거래)를 유지하며 DD%(드로다운 비율)를 줄일 수 있다.",
            "candidate_decision_score(후보 결정 점수) median floor(중앙값 바닥) + historical_vol_5_over_20(단기/중기 변동성 비율) 85% cap(상한)",
        ),
        CandidateSpec(
            "cp319B_vol90_dense50_scale_guard_surface",
            source,
            "candidate_decision_score",
            0.30,
            "historical_vol_5_over_20",
            0.90,
            "le",
            0.028,
            0.45,
            "cp319A(319A 후보)보다 거래수를 늘려 profit scale(수익 규모)을 확보하되 변동성 cap(상한)으로 포켓을 막는다.",
            "lower score floor(낮은 점수 바닥) + wider volatility cap(넓은 변동성 상한)",
        ),
        CandidateSpec(
            "cp319C_atr80_dense55_defensive_surface",
            source,
            "candidate_decision_score",
            0.30,
            "atr_14_over_atr_50",
            0.80,
            "le",
            0.024,
            0.38,
            "ATR regime(평균 진폭 레짐)이 과열될 때 신호를 줄이면 월별 포켓(monthly pocket, 월별 포켓)이 완화되는지 본다.",
            "ATR short/long ratio(단기/장기 평균 진폭 비율) cap(상한)",
        ),
        CandidateSpec(
            "cp319D_adx90_dense60_trend_cap_surface",
            source,
            "candidate_decision_score",
            0.325,
            "adx_14",
            0.90,
            "le",
            0.028,
            0.45,
            "강한 추세 말단(trend tail, 추세 끝단)에서 연속 손실이 뭉치는지 보고 ADX cap(상한)으로 underwater stretch(수중 구간)를 줄인다.",
            "ADX 90% cap(상한) + medium density(중간 밀도)",
        ),
        CandidateSpec(
            "cp319E_bbw90_dense55_bandwidth_guard_surface",
            source,
            "candidate_decision_score",
            0.35,
            "bollinger_width_20",
            0.90,
            "le",
            0.027,
            0.43,
            "Bollinger bandwidth(볼린저 밴드폭)가 과도한 구간을 피하면 scale(규모)을 크게 잃지 않고 local pocket(국소 포켓)을 줄일 수 있다.",
            "Bollinger width(볼린저 폭) cap(상한) + scale guard(규모 보호)",
        ),
        CandidateSpec(
            "cp319F_histvol85_dense55_balanced_surface",
            source,
            "candidate_decision_score",
            0.375,
            "historical_vol_5_over_20",
            0.85,
            "le",
            0.026,
            0.42,
            "cp319B(319B 후보)보다 보수적으로 trade density(거래 밀도)를 낮춰 curve smoothness(곡선 매끈함)를 우선 확인한다.",
            "balanced score floor(균형 점수 바닥) + volatility cap(변동성 상한)",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s318.rel(path)


def long_path(path: Path | str) -> Path:
    return ledger.io_path(path)


def read_text(path: Path) -> str:
    return s318.read_text(path)


def write_text(path: Path, text: str) -> None:
    s318.write_text(path, text)


def write_json(path: Path, payload: Any) -> None:
    s318.write_json(path, payload)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s318.write_csv(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return s318.s317.read_csv_dicts(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s318.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s318.sha256_file(path)


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        text = str(value).replace(",", "").strip()
        if not text:
            return default
        return float(text)
    except Exception:
        return default


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return r309.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return r309.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return r309.prepend_focus(workspace, focus, marker)


def load_source_manifest() -> tuple[list[str], dict[str, dict[str, str]]]:
    rows = read_csv_dicts(SOURCE_MANIFEST)
    return list(rows[0].keys()) if rows else [], {row["package_id"]: row for row in rows}


def read_payloads(manifest_by_package: Mapping[str, Mapping[str, str]]) -> dict[str, pd.DataFrame]:
    payloads: dict[str, pd.DataFrame] = {}
    for spec in candidate_specs():
        if spec.source_package_id in payloads:
            continue
        row = manifest_by_package[spec.source_package_id]
        payloads[spec.source_package_id] = pd.read_parquet(long_path(ROOT / row["payload_path"]))
    return payloads


def load_stage318_actual_trades(manifest_by_package: Mapping[str, Mapping[str, str]]) -> pd.DataFrame:
    wanted = {spec.source_package_id for spec in candidate_specs()}
    attempts = {row["attempt_name"]: row for row in read_csv_dicts(SOURCE_ATTEMPT_SUMMARY)}
    frames: list[pd.DataFrame] = []
    with long_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(row["metrics"])
            report = ast.literal_eval(row["report"])
            attempt = attempts.get(str(report.get("attempt_name", "")), {})
            package_id = str(attempt.get("package_id", ""))
            if package_id not in wanted:
                continue
            trades = trade_frame(Path(metrics.get("report_path", "")))
            if trades.empty:
                continue
            trades["source_package_id"] = package_id
            trades["split"] = str(row.get("split", ""))
            trades["dir_val"] = trades["direction"].map({"buy": 1, "sell": -1}).astype("int8")
            trades["open_floor"] = pd.to_datetime(trades["open_time"]).dt.floor("5min")
            trades["trade_key"] = trades["open_floor"].astype(str) + "|" + trades["dir_val"].astype(str)
            frames.append(trades)
    result = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    write_csv(ACTUAL_TRADE_FRAME, list(result.columns) if not result.empty else ["source_package_id"], result.to_dict("records") if not result.empty else [])
    return result


def summarize_profits(profits: Sequence[float], close_times: Sequence[Any] | None = None) -> dict[str, Any]:
    values = [float(value) for value in profits]
    net = float(sum(values))
    dd = float(drawdown_stats(values)["max_drawdown"]) if values else 0.0
    recovery = net / dd if dd > 0 else (99.0 if net > 0 else 0.0)
    balance = 500.0
    peak = 500.0
    max_underwater = 0
    underwater = 0
    for profit in values:
        balance += profit
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            max_underwater = max(max_underwater, underwater)
    positive_month_share = 0.0
    worst_month_net = 0.0
    if close_times is not None and values:
        monthly: dict[str, float] = defaultdict(float)
        for close_time, profit in zip(close_times, values):
            monthly[pd.to_datetime(close_time).strftime("%Y-%m")] += float(profit)
        positive_month_share = sum(1 for value in monthly.values() if value > 0) / len(monthly) if monthly else 0.0
        worst_month_net = min(monthly.values()) if monthly else 0.0
    return {
        "net_profit": round(net, 2),
        "trade_count": len(values),
        "profit_factor": round(float(profit_factor(values)), 6),
        "max_drawdown": round(dd, 2),
        "drawdown_to_net_ratio": round(dd / net, 6) if net > 0 else 999.0,
        "recovery_factor": round(recovery, 6),
        "expectancy": round(net / len(values), 6) if values else 0.0,
        "positive_month_share": round(float(positive_month_share), 6),
        "worst_month_net": round(float(worst_month_net), 2),
        "max_underwater_trades": int(max_underwater),
    }


def estimate_actual_replay(package_id: str, payload: pd.DataFrame, trades: pd.DataFrame) -> dict[str, dict[str, Any]]:
    source_signal = pd.to_numeric(payload["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    selected_keys = set(pd.to_datetime(payload.loc[source_signal.ne(0), "ts_floor"]).astype(str) + "|" + source_signal[source_signal.ne(0)].astype(str))
    results: dict[str, dict[str, Any]] = {}
    for split, split_name, days in (("validation_is", "validation", 183), ("oos", "oos", 131)):
        subset = trades[(trades["source_package_id"] == package_id) & (trades["split"] == split)]
        picked = subset[subset["trade_key"].isin(selected_keys)]
        summary = summarize_profits(picked["net_profit"].tolist(), picked["close_time"].tolist())
        summary["trades_per_day"] = round(float(summary["trade_count"]) / days, 6)
        summary["split"] = split_name
        results[split_name] = summary
    return results


def segment_summary(trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if trades.empty:
        return rows
    for keys, frame in trades.groupby(["source_package_id", "split", "month", "direction"], dropna=False):
        package_id, split, month, direction = keys
        summary = summarize_profits(frame["net_profit"].tolist(), frame["close_time"].tolist())
        rows.append({"source_package_id": package_id, "split": split, "month": month, "direction": direction, **summary})
    return rows


def threshold_mask(source: pd.DataFrame, spec: CandidateSpec) -> pd.Series:
    active = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).ne(0)
    score = pd.to_numeric(source[spec.score_column], errors="coerce")
    filter_values = pd.to_numeric(source[spec.filter_column], errors="coerce")
    score_threshold = float(score[active].quantile(spec.score_quantile))
    filter_threshold = float(filter_values[active].quantile(spec.filter_quantile))
    mask = active & score.ge(score_threshold)
    if spec.filter_sense == "le":
        mask &= filter_values.le(filter_threshold)
    else:
        mask &= filter_values.ge(filter_threshold)
    return mask.fillna(False)


def materialize_candidate(
    spec: CandidateSpec,
    payloads: Mapping[str, pd.DataFrame],
    manifest_by_package: Mapping[str, Mapping[str, str]],
    source_columns: Sequence[str],
    trades: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    source = payloads[spec.source_package_id].copy()
    source_signal = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    mask = threshold_mask(source, spec)
    signal = np.where(mask.to_numpy(), source_signal.to_numpy(), 0).astype("int8")
    branch_id = f"run319A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage319_branch_id"] = branch_id
    payload["stage318_source_package_id"] = spec.source_package_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "curve_pocket_risk_asymmetry_surface"
    payload["stage319_score_column"] = spec.score_column
    payload["stage319_score_quantile"] = spec.score_quantile
    payload["stage319_filter_column"] = spec.filter_column
    payload["stage319_filter_quantile"] = spec.filter_quantile
    payload["stage319_filter_sense"] = spec.filter_sense
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = ["long" if value > 0 else ("short" if value < 0 else "flat") for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct
    payload["payload_claim_boundary"] = BOUNDARY

    source_manifest = dict(manifest_by_package[spec.source_package_id])
    risk = {name: source_manifest.get(name, "") for name in source_columns if name in source_manifest}
    risk["model_risk_sizing_enabled"] = "1"
    risk["model_risk_min_pct"] = "0.004"
    risk["model_risk_max_pct"] = str(spec.model_risk_max_pct)
    risk["model_risk_confidence_floor"] = "0.58"
    risk["model_risk_confidence_ceiling"] = "0.99"
    risk["model_risk_fallback_lot"] = "0.08"
    risk["fixed_lot"] = str(spec.fixed_lot)
    replay = estimate_actual_replay(spec.source_package_id, payload, trades)
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_mt5_run_id": SOURCE_MT5_RUN_ID,
        "source_package_id": spec.source_package_id,
        "score_column": spec.score_column,
        "score_quantile": spec.score_quantile,
        "filter_column": spec.filter_column,
        "filter_quantile": spec.filter_quantile,
        "filter_sense": spec.filter_sense,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
        "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
        "risk_logic": risk,
        "claim_boundary": BOUNDARY,
        "selection_caution": "Stage319 design uses Stage318 actual MT5 reports; requires run319B actual MT5 and run319C review.",
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = RUNTIME_FEATURE_ORDER_HASH
    payload["model_feature_order_hash"] = MODEL_FEATURE_ORDER_HASH
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    return payload.drop(columns=drop_columns, errors="ignore"), identity | {"direction_surface_hash": surface_hash}, risk, replay


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    source_columns, manifest_by_package = load_source_manifest()
    payloads = read_payloads(manifest_by_package)
    trades = load_stage318_actual_trades(manifest_by_package)
    write_csv(SEGMENT_SUMMARY, list(segment_summary(trades)[0].keys()) if segment_summary(trades) else ["source_package_id"], segment_summary(trades))

    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifact_paths: list[Path] = []

    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, risk, replay = materialize_candidate(spec, payloads, manifest_by_package, source_columns, trades)
        branch_id = f"run319A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_risk_asymmetry_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(long_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "package_id": spec.package_id,
                "materialized_branch_id": branch_id,
                "source_package_id": spec.source_package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                "decision_surface": "curve_pocket_risk_asymmetry_rule_surface",
                "risk_logic": risk,
                "runtime_handoff": "precomputed route_signal_value replay for Stage319 MT5 probe(319단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
            },
        )
        val = replay["validation"]
        oos = replay["oos"]
        min_trade_gate = "passed" if number(val["trade_count"]) >= 730 and number(oos["trade_count"]) >= 520 else "failed"
        density_gate = "passed" if 4.0 <= number(val["trades_per_day"]) <= 10.0 and 4.0 <= number(oos["trades_per_day"]) <= 10.0 else "failed"
        profit_gate = "passed" if number(val["net_profit"]) >= 10000.0 and number(oos["net_profit"]) >= 10000.0 and number(val["net_profit"]) + number(oos["net_profit"]) >= 35000.0 else "failed"
        efficiency_gate = "passed" if number(val["profit_factor"]) >= 1.15 and number(oos["profit_factor"]) >= 1.12 and number(val["expectancy"]) > 0 and number(oos["expectancy"]) > 0 else "failed"
        curve_gate = "passed" if number(val["drawdown_to_net_ratio"]) <= 0.35 and number(oos["drawdown_to_net_ratio"]) <= 0.35 and number(val["positive_month_share"]) >= 0.70 and number(oos["positive_month_share"]) >= 0.70 and number(val["max_underwater_trades"]) <= 320 and number(oos["max_underwater_trades"]) <= 320 else "failed"
        design_gate = "passed" if all(gate == "passed" for gate in (min_trade_gate, density_gate, profit_gate, efficiency_gate, curve_gate)) else "failed"
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "source_package_id": spec.source_package_id,
                "validation_estimated_net_profit": val["net_profit"],
                "validation_estimated_pf": val["profit_factor"],
                "validation_estimated_trades": val["trade_count"],
                "validation_estimated_trades_per_day": val["trades_per_day"],
                "validation_estimated_dd_to_net": val["drawdown_to_net_ratio"],
                "validation_estimated_positive_month_share": val["positive_month_share"],
                "validation_estimated_max_underwater_trades": val["max_underwater_trades"],
                "oos_estimated_net_profit": oos["net_profit"],
                "oos_estimated_pf": oos["profit_factor"],
                "oos_estimated_trades": oos["trade_count"],
                "oos_estimated_trades_per_day": oos["trades_per_day"],
                "oos_estimated_dd_to_net": oos["drawdown_to_net_ratio"],
                "oos_estimated_positive_month_share": oos["positive_month_share"],
                "oos_estimated_max_underwater_trades": oos["max_underwater_trades"],
                "combined_estimated_net_profit": number(val["net_profit"]) + number(oos["net_profit"]),
                "minimum_trade_gate": min_trade_gate,
                "density_4_10_trades_day_gate": density_gate,
                "profit_scale_gate": profit_gate,
                "efficiency_gate": efficiency_gate,
                "curve_pocket_design_gate": curve_gate,
                "design_gate": design_gate,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
            }
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_package_id": spec.source_package_id,
                "hypothesis": spec.hypothesis,
                "changed_variables": spec.changed_variables,
                "decision_surface": f"{spec.score_column} q>={spec.score_quantile}; {spec.filter_column} {spec.filter_sense} q{spec.filter_quantile}",
                "risk_logic": json.dumps(risk, sort_keys=True),
                "success_criteria": "actual MT5 validation/OOS net positive, 4-10 trades/day, PF/recovery/expectancy and curve pocket gate together",
                "failure_criteria": "actual MT5 DD pocket, density slip, or profit scale collapse",
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name in ("validation", "oos"):
            split_frame = payload[payload["split"].astype(str).eq(split_name)]
            active = int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).ne(0).sum())
            days = max(1, pd.to_datetime(split_frame["timestamp"]).dt.date.nunique()) if not split_frame.empty else 1
            estimate = replay[split_name]
            supply_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "tier_scope": "Tier A",
                    "split": split_name,
                    "active_signal_rows": active,
                    "approx_signal_rows_per_day": round(active / days, 6),
                    "estimated_actual_trade_count": estimate["trade_count"],
                    "estimated_actual_trades_per_day": estimate["trades_per_day"],
                    "estimated_actual_net_profit": estimate["net_profit"],
                    "estimated_actual_pf": estimate["profit_factor"],
                    "claim_boundary": BOUNDARY,
                }
            )
        manifest_source = dict(manifest_by_package[spec.source_package_id])
        manifest_row = {column: manifest_source.get(column, "") for column in source_columns}
        manifest_row.update(
            {
                "queue_id": f"run319A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "curve_pocket_risk_asymmetry_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                "model_risk_sizing_enabled": "1",
                "model_risk_min_pct": "0.004",
                "model_risk_max_pct": str(spec.model_risk_max_pct),
                "model_risk_confidence_floor": "0.58",
                "model_risk_confidence_ceiling": "0.99",
                "model_risk_fallback_lot": "0.08",
                "fixed_lot": str(spec.fixed_lot),
                "approx_validation_trades_per_day": val["trades_per_day"],
                "approx_oos_trades_per_day": oos["trades_per_day"],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(manifest_row)
        artifact_paths.extend([payload_path, handoff_path, model_spec_path])
    scoreboard_rows.sort(key=lambda item: number(item["combined_estimated_net_profit"]), reverse=True)
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, artifact_paths


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    artifact_paths: Sequence[Path],
) -> list[Path]:
    write_csv(BRANCH_QUEUE, list(branch_rows[0].keys()), branch_rows)
    write_csv(MODEL_SCOREBOARD, list(scoreboard_rows[0].keys()), scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, list(supply_rows[0].keys()), supply_rows)
    write_csv(PAYLOAD_MANIFEST, list(manifest_rows[0].keys()), manifest_rows)
    write_csv(MT5_QUEUE, list(manifest_rows[0].keys()), manifest_rows)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "run_id": RUN_ID,
            "hypothesis": "Curve-pocket risk asymmetry can keep Stage318 profit scale while reducing drawdown pockets.",
            "control_variables": ["US100 M5", "split_v1", "Stage318 source signal", "actual routed total evidence"],
            "changed_variables": ["volatility/trend risk filter", "lower model risk sizing", "density target"],
            "success_criteria": ["actual MT5 4-10 trades/day", "net profit positive in validation and OOS", "PF/recovery/expectancy acceptable", "no deep curve pocket"],
            "failure_criteria": ["profit scale collapse", "density below 4 or above 10", "DD pocket remains"],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_payload_manifest": rel(SOURCE_MANIFEST),
            "source_mt5_kpi": rel(SOURCE_KPI),
            "source_survivor_queue": rel(SOURCE_SURVIVOR_QUEUE),
            "feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
            "rows": {"branch_rows": len(branch_rows), "scoreboard_rows": len(scoreboard_rows), "manifest_rows": len(manifest_rows)},
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}],
    )
    gate_rows = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage318(318단계) threshold-only repair(임계값만 수리)이 아니라 risk asymmetry(위험 비대칭) 질문을 만들었다."},
        {"gate_name": "source_lineage(원천 계보)", "status": "passed", "evidence_path": rel(DATA_RECEIPT), "effect": "Stage318(318단계) 생존 씨앗과 MT5(메타트레이더5) 근거를 연결했다."},
        {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "actual MT5(실제 메타트레이더5) 전에는 Adapter(어댑터)를 시작하지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "선택 후보가 없으므로 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "candidate_rows": len(scoreboard_rows),
        "mt5_queue_rows": len(manifest_rows),
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    lineage = {
        "run_id": RUN_ID,
        "producer": rel(PRODUCER),
        "source_artifacts": [
            {"path": rel(SOURCE_SURVIVOR_QUEUE), "sha256": sha256_file(SOURCE_SURVIVOR_QUEUE)},
            {"path": rel(SOURCE_MANIFEST), "sha256": sha256_file(SOURCE_MANIFEST)},
            {"path": rel(SOURCE_KPI), "sha256": sha256_file(SOURCE_KPI)},
        ],
        "output_artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, REPORT, *artifact_paths]],
        "claim_boundary": BOUNDARY,
    }
    write_text(LINEAGE, json.dumps(lineage, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return [
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        EXPERIMENT_DESIGN,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        ACTUAL_TRADE_FRAME,
        SEGMENT_SUMMARY,
        *artifact_paths,
    ]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run319A Curve-Pocket Risk Asymmetry Materialization(319A 곡선 포켓 위험 비대칭 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard_rows)}`",
        f"- mt5_queue_rows(MT5 대기열 행): `{len(manifest_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Effect(효과): Stage318(318단계)의 큰 수익 조각을 보존하되 volatility/trend cap(변동성/추세 상한)과 lower risk sizing(낮은 위험 크기)으로 곡선 포켓을 줄이는 후보를 MT5(메타트레이더5) 탐침으로 넘긴다.",
        "",
        "| package(패키지) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val PF(검증 PF) | val DD/net(검증 DD/순익) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | OOS PF(표본외 PF) | design gate(설계 관문) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        lines.append(
            "| {pkg} | {vn:.2f} | {vtd:.2f} | {vpf:.2f} | {vdd:.2f} | {on:.2f} | {otd:.2f} | {opf:.2f} | {gate} |".format(
                pkg=row["package_id"],
                vn=number(row["validation_estimated_net_profit"]),
                vtd=number(row["validation_estimated_trades_per_day"]),
                vpf=number(row["validation_estimated_pf"]),
                vdd=number(row["validation_estimated_dd_to_net"]),
                on=number(row["oos_estimated_net_profit"]),
                otd=number(row["oos_estimated_trades_per_day"]),
                opf=number(row["oos_estimated_pf"]),
                gate=row["design_gate"],
            )
        )
    lines.extend(
        [
            "",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "Caution(주의): 이 설계 추정은 Stage318(318단계) 실제 MT5(메타트레이더5) 거래를 재사용한다. 선택 후보(candidate, 후보)는 run319B/run319C(319B/319C 실행) 이후에만 판단한다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", "- selected_candidate(선택 후보): `none`")
    selected = replace_line(selected, "- Adapter package(", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line(selected, "- ONNX readiness(", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run319A_report(", "- run319A_mt5_queue("))
    selected = selected.rstrip() + f"\n- run319A_report(319A 보고서): `{rel(REPORT)}`\n- run319A_mt5_queue(319A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run319A_report(", "- run319A_scoreboard(", "- run319A_mt5_queue("))
    review_index = review_index.rstrip() + f"\n- run319A_report(319A 보고서): `{rel(REPORT)}`\n- run319A_scoreboard(319A 점수표): `{rel(MODEL_SCOREBOARD)}`\n- run319A_mt5_queue(319A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = drop_prefixed_lines(current, ("- run319A_summary(",))
    current = current.rstrip() + f"\n- run319A_summary(319A 요약): curve-pocket risk asymmetry(곡선 포켓 위험 비대칭) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage319(319단계) run319A(319A 실행) curve-pocket risk asymmetry(곡선 포켓 위험 비대칭) materialization(물질화) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += (
            f"\n## {UPDATED_ON} run319A Curve-pocket risk asymmetry materialization(319A 곡선 포켓 위험 비대칭 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): 후보 `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었다.\n"
            "- boundary(경계): 선택 후보, Adapter(어댑터), ONNX(온엑스)를 주장하지 않는다.\n"
        )
    write_text(CHANGELOG, changelog)


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert(RUN_REGISTRY, s318.s310.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "curve_pocket_risk_asymmetry_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "curve_pocket_risk_asymmetry_materialization",
                "tier_scope": "Tier A/Tier B paired",
                "kpi_scope": "design_estimate_actual_replay",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"candidates={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started",
                "external_verification_status": "not_started",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(STAGE_LEDGER, s318.s310.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "curve_pocket_risk_asymmetry_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")


def update_memory_registers() -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} curve_pocket_risk_asymmetry(곡선 포켓 위험 비대칭)\n\n"
            "- idea_id(아이디어 ID): `stage319_curve_pocket_risk_asymmetry`\n"
            "- hypothesis(가설): Stage318(318단계) 수익 표면에서 변동성/추세 과열 구간을 줄이면 수익 규모와 4-10 trades/day(일 4-10거래)를 유지하면서 곡선 포켓을 줄일 수 있다.\n"
            "- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        )
        write_text(IDEA_REGISTER, idea)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    created_at = utc_now()
    for path in paths:
        if not s318.s310.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage319_curve_pocket_risk_asymmetry_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "Stage319 materialization artifact",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, s318.s310.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, artifacts = build_outputs()
    output_paths = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, artifacts)
    update_docs(scoreboard_rows, manifest_rows)
    update_registers(scoreboard_rows, manifest_rows)
    update_memory_registers()
    update_artifact_registry(output_paths)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
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

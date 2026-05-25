from __future__ import annotations

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

from stage_pipelines.stage280.validate_directional_mapping_stability import (  # noqa: E402
    drawdown_stats,
    profit_factor,
)
from stage_pipelines.stage320 import design_validation_pocket_drawdown_controller as s320  # noqa: E402


STAGE_ID = "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild"
RUN_ID = "run321A_design_post_controller_profit_curve_rebuild_packet_v1"
RUN_NUMBER = "run321A"
SOURCE_STAGE_ID = "320_onnx_candidate_campaign__validation_pocket_drawdown_controller"
SOURCE_RUN_ID = "run320C_review_validation_pocket_drawdown_controller_mt5_probe_v1"
SOURCE_MT5_RUN_ID = "run319B_execute_curve_pocket_risk_asymmetry_mt5_probe_v1"
UPDATED_ON = "2026-05-26"
STATUS = "completed_post_controller_profit_curve_candidates_materialized_no_selection"
JUDGMENT = "post_controller_profit_curve_candidates_materialized_requires_actual_mt5_no_selection"
NEXT_ACTION = "run321B_execute_post_controller_profit_curve_mt5_probe"
BOUNDARY = s320.BOUNDARY

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"

SOURCE_STAGE319_ID = "319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild"
SOURCE_STAGE319_ROOT = ROOT / "stages" / SOURCE_STAGE319_ID
SOURCE_RUN319A = SOURCE_STAGE319_ROOT / "02_runs" / "run319A"
SOURCE_RUN319B = SOURCE_STAGE319_ROOT / "02_runs" / "run319B"
SOURCE_MANIFEST = SOURCE_RUN319A / "candidate_payload_manifest.csv"
SOURCE_KPI = SOURCE_RUN319B / "mt5_kpi_summary.csv"
SOURCE_STAGE320_REVIEW = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews" / "run320C_review_stage321_open.md"
SOURCE_STAGE320_FAILURE = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run320C" / "failure_memory.csv"
SOURCE_TRADE_FRAME = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run320A" / "run320A_stage319_survivor_actual_trade_frame.csv"

CONSENSUS_SUMMARY = RUN_ROOT / "run321A_stage319_consensus_signal_summary.csv"
ACTUAL_TRADE_FRAME = RUN_ROOT / "run321A_stage319_actual_trade_frame_reference.csv"
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
REPORT = REVIEWS / "run321A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage321/design_post_controller_profit_curve_rebuild.py")
RUNTIME_FEATURE_ORDER = s320.RUNTIME_FEATURE_ORDER
RUNTIME_FEATURE_ORDER_HASH = s320.RUNTIME_FEATURE_ORDER_HASH
MODEL_FEATURE_ORDER_HASH = hashlib.sha256("stage321_consensus_profit_curve_source_v1".encode("utf-8")).hexdigest()

D = "cp319D_adx90_dense60_trend_cap_surface"
B = "cp319B_vol90_dense50_scale_guard_surface"
F = "cp319F_histvol85_dense55_balanced_surface"
A = "cp319A_vol85_dense45_curve_pocket_veto_surface"
C = "cp319C_atr80_dense55_defensive_surface"
E = "cp319E_bbw90_dense55_bandwidth_guard_surface"
SOURCE_PACKAGES = (D, B, F, A, C, E)
SHORT = {D: "d", B: "b", F: "f", A: "a", C: "c", E: "e"}


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    rule_name: str
    model_risk_max_pct: float
    fixed_lot: float
    hypothesis: str
    changed_variables: str
    branch_lane: str


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            "cp321A_d_a_confirm_efficiency_surface",
            "d_a_confirm_score50",
            0.022,
            0.34,
            "cp319D와 cp319A가 같은 방향일 때만 진입하면 거래 수 4-10/day를 유지하면서 validation pocket을 줄일 수 있는지 본다.",
            "Stage319 D 신호를 A 합의와 평균 점수 상위 50%로 재구성한다.",
            "defensive_efficiency",
        ),
        CandidateSpec(
            "cp321B_d_or_b_score60_scale_curve_surface",
            "d_or_b_score60",
            0.026,
            0.42,
            "D/B 중 하나가 살아 있고 평균 점수 상위 60%이면 profit scale과 curve smoothness를 같이 만들 수 있는지 본다.",
            "Stage319 D/B union priority decision surface를 만든다.",
            "balanced_scale",
        ),
        CandidateSpec(
            "cp321C_d_or_b_score50_aggressive_scale_surface",
            "d_or_b_score50",
            0.028,
            0.45,
            "더 넓은 D/B union으로 수익 규모 상방을 확보하되 곡선 포켓이 실제 MT5에서 견디는지 본다.",
            "공격형 D/B union, 평균 점수 상위 50%, 높은 risk cap.",
            "aggressive_scale",
        ),
        CandidateSpec(
            "cp321D_d_f_confirm_balance_surface",
            "d_f_confirm",
            0.024,
            0.38,
            "D/F 합의가 D 단독보다 수익-곡선 균형을 개선하는지 본다.",
            "D 신호를 F 합의로 제한한다.",
            "balanced_consensus",
        ),
        CandidateSpec(
            "cp321E_three_of_six_consensus_surface",
            "three_of_six_consensus",
            0.024,
            0.38,
            "여섯 개 Stage319 표면 중 세 개 이상 같은 방향이면 독립 합의가 curve pocket을 줄이는지 본다.",
            "multi-surface vote decision surface를 만든다.",
            "consensus_vote",
        ),
        CandidateSpec(
            "cp321F_d_or_b_score50_hv80_curve_surface",
            "d_or_b_score50_hv80",
            0.024,
            0.38,
            "D/B union의 수익 규모를 보존하면서 평균 변동성 상위 20%를 줄이면 포켓이 완화되는지 본다.",
            "D/B score50 union에 historical volatility rank 80% cap을 결합한다.",
            "curve_guard_not_stage320_controller",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s320.rel(path)


def long_path(path: Path | str) -> Path:
    return s320.long_path(path)


def read_text(path: Path) -> str:
    return s320.read_text(path)


def write_text(path: Path, text: str) -> None:
    s320.write_text(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    s320.write_csv(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s320.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return s320.sha256_file(path)


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        text = str(value).replace(",", "").strip()
        return float(text) if text else default
    except Exception:
        return default


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return s320.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return s320.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return s320.prepend_focus(workspace, focus, marker)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return s320.read_csv_rows(path)


def load_manifest() -> tuple[list[str], dict[str, dict[str, str]]]:
    rows = read_csv_rows(SOURCE_MANIFEST)
    return list(rows[0].keys()) if rows else [], {row["package_id"]: row for row in rows}


def load_source_payloads(manifest: Mapping[str, Mapping[str, str]]) -> dict[str, pd.DataFrame]:
    payloads: dict[str, pd.DataFrame] = {}
    for package_id in SOURCE_PACKAGES:
        source = pd.read_parquet(long_path(ROOT / manifest[package_id]["payload_path"]))
        source = source.copy()
        source["ts_key"] = pd.to_datetime(source["ts_floor"]).astype(str)
        payloads[package_id] = source
    return payloads


def build_signal_matrix(payloads: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    base = payloads[D][["timestamp", "ts_floor", "ts_key", "split"]].reset_index(drop=True).copy()
    for package_id in SOURCE_PACKAGES:
        short = SHORT[package_id]
        source = payloads[package_id].reset_index(drop=True)
        if len(source) != len(base):
            raise ValueError(f"payload length mismatch for {package_id}: {len(source)} != {len(base)}")
        base[f"sig_{short}"] = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8")
        base[f"score_{short}"] = pd.to_numeric(source["candidate_decision_score"], errors="coerce")
        base[f"hv_{short}"] = pd.to_numeric(source["historical_vol_5_over_20"], errors="coerce")
        base[f"adx_{short}"] = pd.to_numeric(source["adx_14"], errors="coerce")
    score_cols = [name for name in base.columns if name.startswith("score_")]
    hv_cols = [name for name in base.columns if name.startswith("hv_")]
    adx_cols = [name for name in base.columns if name.startswith("adx_")]
    base["score_mean"] = base[score_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    base["score_rank"] = base.groupby("split")["score_mean"].rank(pct=True)
    base["hv_mean"] = base[hv_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    base["hv_rank"] = base.groupby("split")["hv_mean"].rank(pct=True)
    base["adx_mean"] = base[adx_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1)
    base["adx_rank"] = base.groupby("split")["adx_mean"].rank(pct=True)
    base["active_surface_count"] = sum(base[f"sig_{SHORT[pkg]}"].ne(0).astype("int8") for pkg in SOURCE_PACKAGES)
    base["positive_vote_count"] = sum(base[f"sig_{SHORT[pkg]}"].gt(0).astype("int8") for pkg in SOURCE_PACKAGES)
    base["negative_vote_count"] = sum(base[f"sig_{SHORT[pkg]}"].lt(0).astype("int8") for pkg in SOURCE_PACKAGES)
    return base


def signal_matrix_summary(matrix: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split_name, frame in [("all", matrix), *[(str(name), group) for name, group in matrix.groupby("split", dropna=False)]]:
        summary: dict[str, Any] = {
            "split": split_name,
            "row_count": int(len(frame)),
            "score_mean_p50": round(float(frame["score_mean"].median()), 8) if not frame.empty else 0.0,
            "hv_mean_p80": round(float(frame["hv_mean"].quantile(0.80)), 8) if not frame.empty else 0.0,
            "three_vote_rows": int(((frame["positive_vote_count"] >= 3) | (frame["negative_vote_count"] >= 3)).sum()),
        }
        for package_id in SOURCE_PACKAGES:
            short = SHORT[package_id]
            summary[f"sig_{short}_active_rows"] = int(frame[f"sig_{short}"].ne(0).sum())
        rows.append(summary)
    return rows


def load_reference_trades() -> pd.DataFrame:
    trades = pd.read_csv(long_path(SOURCE_TRADE_FRAME), encoding="utf-8-sig")
    trades["trade_key"] = pd.to_datetime(trades["open_floor"]).astype(str) + "|" + trades["dir_val"].astype(str)
    write_csv(ACTUAL_TRADE_FRAME, list(trades.columns), trades.to_dict("records"))
    return trades


def summarize_profits(profits: Sequence[float], close_times: Sequence[Any] | None = None) -> dict[str, Any]:
    values = [float(value) for value in profits]
    net = float(sum(values))
    dd = float(drawdown_stats(values)["max_drawdown"]) if values else 0.0
    monthly: dict[str, float] = defaultdict(float)
    if close_times is not None:
        for close_time, profit in zip(close_times, values):
            monthly[pd.to_datetime(close_time).strftime("%Y-%m")] += profit
    balance = 500.0
    peak = 500.0
    underwater = 0
    max_underwater = 0
    for profit in values:
        balance += profit
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            max_underwater = max(max_underwater, underwater)
    return {
        "net_profit": round(net, 2),
        "trade_count": len(values),
        "profit_factor": round(float(profit_factor(values)), 6),
        "max_drawdown": round(dd, 2),
        "drawdown_to_net_ratio": round(dd / net, 6) if net > 0 else 999.0,
        "recovery_factor": round(net / dd, 6) if dd > 0 else (99.0 if net > 0 else 0.0),
        "expectancy": round(net / len(values), 6) if values else 0.0,
        "positive_month_share": round(sum(1 for value in monthly.values() if value > 0) / len(monthly), 6) if monthly else 0.0,
        "worst_month_net": round(min(monthly.values()), 2) if monthly else 0.0,
        "max_underwater_trades": int(max_underwater),
    }


def rule_signal(matrix: pd.DataFrame, rule_name: str) -> pd.Series:
    d = matrix["sig_d"]
    b = matrix["sig_b"]
    f = matrix["sig_f"]
    a = matrix["sig_a"]
    if rule_name == "d_a_confirm_score50":
        return pd.Series(np.where((d != 0) & (d == a) & (matrix["score_rank"] >= 0.50), d, 0), index=matrix.index).astype("int8")
    if rule_name == "d_or_b_score60":
        return pd.Series(np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.60), np.where(d != 0, d, b), 0), index=matrix.index).astype("int8")
    if rule_name == "d_or_b_score50":
        return pd.Series(np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.50), np.where(d != 0, d, b), 0), index=matrix.index).astype("int8")
    if rule_name == "d_f_confirm":
        return pd.Series(np.where((d != 0) & (d == f), d, 0), index=matrix.index).astype("int8")
    if rule_name == "three_of_six_consensus":
        return pd.Series(np.where(matrix["positive_vote_count"] >= 3, 1, np.where(matrix["negative_vote_count"] >= 3, -1, 0)), index=matrix.index).astype("int8")
    if rule_name == "d_or_b_score50_hv80":
        return pd.Series(
            np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.50) & (matrix["hv_rank"] <= 0.80), np.where(d != 0, d, b), 0),
            index=matrix.index,
        ).astype("int8")
    raise ValueError(f"unknown rule_name: {rule_name}")


def estimate(payload: pd.DataFrame, trades: pd.DataFrame) -> dict[str, dict[str, Any]]:
    signal = pd.to_numeric(payload["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    selected = set(pd.to_datetime(payload.loc[signal.ne(0), "ts_floor"]).astype(str) + "|" + signal[signal.ne(0)].astype(str))
    out: dict[str, dict[str, Any]] = {}
    for split, name, days in (("validation_is", "validation", 183), ("oos", "oos", 131)):
        source = trades[trades["split"].astype(str).eq(split)]
        picked = source[source["trade_key"].isin(selected)]
        summary = summarize_profits(picked["net_profit"].tolist(), picked["close_time"].tolist())
        summary["trades_per_day"] = round(summary["trade_count"] / days, 6)
        out[name] = summary
    return out


def materialize(
    spec: CandidateSpec,
    matrix: pd.DataFrame,
    source_payload: pd.DataFrame,
    source_columns: Sequence[str],
    source_manifest: Mapping[str, str],
    trades: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, str], dict[str, dict[str, Any]]]:
    signal = rule_signal(matrix, spec.rule_name).to_numpy(dtype="int8")
    branch_id = f"run321A_{spec.package_id.replace('_surface', '')}"
    payload = source_payload.copy()
    payload["stage321_branch_id"] = branch_id
    payload["stage319_primary_source_package_id"] = D
    payload["stage319_consensus_source_packages"] = "|".join(SOURCE_PACKAGES)
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "post_controller_profit_curve_consensus_surface"
    payload["stage321_rule_name"] = spec.rule_name
    payload["stage321_branch_lane"] = spec.branch_lane
    payload["stage321_score_rank"] = matrix["score_rank"].to_numpy()
    payload["stage321_hv_rank"] = matrix["hv_rank"].to_numpy()
    payload["stage321_active_surface_count"] = matrix["active_surface_count"].to_numpy()
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = ["long" if value > 0 else ("short" if value < 0 else "flat") for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct
    payload["payload_claim_boundary"] = BOUNDARY
    risk = {column: source_manifest.get(column, "") for column in source_columns}
    risk.update(
        {
            "model_risk_sizing_enabled": "1",
            "model_risk_min_pct": "0.004",
            "model_risk_max_pct": str(spec.model_risk_max_pct),
            "model_risk_confidence_floor": "0.58",
            "model_risk_confidence_ceiling": "0.99",
            "model_risk_fallback_lot": "0.08",
            "fixed_lot": str(spec.fixed_lot),
            "risk_logic_note": "Stage321 consensus signal source; not Stage320 VIX/quality controller.",
        }
    )
    replay = estimate(payload, trades)
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_mt5_run_id": SOURCE_MT5_RUN_ID,
        "primary_source_package_id": D,
        "consensus_source_packages": list(SOURCE_PACKAGES),
        "rule_name": spec.rule_name,
        "branch_lane": spec.branch_lane,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
        "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
        "risk_logic": risk,
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = RUNTIME_FEATURE_ORDER_HASH
    payload["model_feature_order_hash"] = MODEL_FEATURE_ORDER_HASH
    drop_cols = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    return payload.drop(columns=drop_cols, errors="ignore"), identity | {"direction_surface_hash": surface_hash}, risk, replay


def gates_for(val: Mapping[str, Any], oos: Mapping[str, Any]) -> dict[str, str]:
    return {
        "minimum_trade_gate": "passed" if number(val["trade_count"]) >= 730 and number(oos["trade_count"]) >= 520 else "failed",
        "density_4_10_trades_day_gate": "passed" if 4.0 <= number(val["trades_per_day"]) <= 10.0 and 4.0 <= number(oos["trades_per_day"]) <= 10.0 else "failed",
        "profit_scale_gate": "passed" if number(val["net_profit"]) >= 15000.0 and number(oos["net_profit"]) >= 15000.0 and number(val["net_profit"]) + number(oos["net_profit"]) >= 35000.0 else "failed",
        "efficiency_gate": "passed" if number(val["profit_factor"]) >= 1.45 and number(oos["profit_factor"]) >= 1.50 and number(val["expectancy"]) > 0 and number(oos["expectancy"]) > 0 else "failed",
        "curve_pocket_design_gate": "passed"
        if number(val["drawdown_to_net_ratio"]) <= 0.40
        and number(oos["drawdown_to_net_ratio"]) <= 0.25
        and number(val["positive_month_share"]) >= 0.65
        and number(oos["positive_month_share"]) >= 0.80
        and number(val["max_underwater_trades"]) <= 650
        and number(oos["max_underwater_trades"]) <= 150
        else "failed",
    }


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    source_columns, manifest = load_manifest()
    payloads = load_source_payloads(manifest)
    matrix = build_signal_matrix(payloads)
    trades = load_reference_trades()
    summary_rows = signal_matrix_summary(matrix)
    write_csv(CONSENSUS_SUMMARY, list(summary_rows[0].keys()), summary_rows)

    source_payload = payloads[D]
    source_manifest = manifest[D]
    branch_rows: list[dict[str, Any]] = []
    scoreboard: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []

    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, risk, replay = materialize(spec, matrix, source_payload, source_columns, source_manifest, trades)
        branch_id = f"run321A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_path = MODEL_DIR / f"{branch_id}_consensus_profit_curve_surface.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(long_path(payload_path), index=False)
        write_text(model_path, json.dumps(identity, ensure_ascii=False, indent=2, sort_keys=True))
        write_text(
            handoff_path,
            json.dumps(
                {
                    "package_id": spec.package_id,
                    "materialized_branch_id": branch_id,
                    "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                    "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                    "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH,
                    "decision_surface": spec.rule_name,
                    "risk_logic": risk,
                    "runtime_handoff": "precomputed route_signal_value replay for Stage321 MT5 probe(321단계 MT5 탐침)",
                    "claim_boundary": BOUNDARY,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
        )
        val, oos = replay["validation"], replay["oos"]
        gates = gates_for(val, oos)
        design_gate = "passed" if all(value == "passed" for value in gates.values()) else "failed"
        scoreboard.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "rule_name": spec.rule_name,
                "branch_lane": spec.branch_lane,
                "validation_estimated_net_profit": val["net_profit"],
                "validation_estimated_pf": val["profit_factor"],
                "validation_estimated_trades": val["trade_count"],
                "validation_estimated_trades_per_day": val["trades_per_day"],
                "validation_estimated_dd_to_net": val["drawdown_to_net_ratio"],
                "validation_estimated_recovery": val["recovery_factor"],
                "validation_estimated_positive_month_share": val["positive_month_share"],
                "validation_estimated_worst_month_net": val["worst_month_net"],
                "validation_estimated_max_underwater_trades": val["max_underwater_trades"],
                "oos_estimated_net_profit": oos["net_profit"],
                "oos_estimated_pf": oos["profit_factor"],
                "oos_estimated_trades": oos["trade_count"],
                "oos_estimated_trades_per_day": oos["trades_per_day"],
                "oos_estimated_dd_to_net": oos["drawdown_to_net_ratio"],
                "oos_estimated_recovery": oos["recovery_factor"],
                "oos_estimated_positive_month_share": oos["positive_month_share"],
                "oos_estimated_worst_month_net": oos["worst_month_net"],
                "oos_estimated_max_underwater_trades": oos["max_underwater_trades"],
                "combined_estimated_net_profit": number(val["net_profit"]) + number(oos["net_profit"]),
                **gates,
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
                "rule_name": spec.rule_name,
                "branch_lane": spec.branch_lane,
                "hypothesis": spec.hypothesis,
                "changed_variables": spec.changed_variables,
                "decision_surface": "Stage319 multi-surface consensus/union; Stage320 VIX/quality controller discarded",
                "success_criteria": "actual MT5 validation/OOS net, 4-10 trades/day, PF, recovery, expectancy, and curve pocket gates together",
                "failure_criteria": "actual MT5 profit collapse, DD pocket, density slip, or weak segment concentration",
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name in ("validation", "oos"):
            split_frame = payload[payload["split"].astype(str).eq(split_name)]
            active_count = int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).ne(0).sum())
            days = max(1, pd.to_datetime(split_frame["timestamp"]).dt.date.nunique()) if not split_frame.empty else 1
            est = replay[split_name]
            supply_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "split": split_name,
                    "active_signal_rows": active_count,
                    "approx_signal_rows_per_day": round(active_count / days, 6),
                    "estimated_actual_trade_count": est["trade_count"],
                    "estimated_actual_trades_per_day": est["trades_per_day"],
                    "estimated_actual_net_profit": est["net_profit"],
                    "estimated_actual_pf": est["profit_factor"],
                    "claim_boundary": BOUNDARY,
                }
            )
        manifest_row = {column: source_manifest.get(column, "") for column in source_columns}
        manifest_row.update(
            {
                "queue_id": f"run321A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "post_controller_profit_curve_consensus_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "model_artifact_path": rel(model_path),
                "model_artifact_hash": sha256_file(model_path),
                "model_feature_order_path": rel(model_path),
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
        artifacts.extend([payload_path, handoff_path, model_path])
    scoreboard.sort(
        key=lambda row: (
            row["design_gate"] == "passed",
            number(row["validation_estimated_recovery"]) + number(row["oos_estimated_recovery"]),
            number(row["combined_estimated_net_profit"]),
        ),
        reverse=True,
    )
    return branch_rows, scoreboard, supply_rows, manifest_rows, artifacts


def report_markdown(scoreboard: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run321A Post Controller Profit Curve Materialization(321A 제어기 이후 수익 곡선 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "",
        "Effect(효과): Stage320(320단계)의 VIX/quality controller(VIX/품질 제어기)를 버리고 Stage319(319단계) 여러 수익 표면의 consensus/union(합의/합집합)을 새 decision surface(판단 표면)로 만들었다.",
        "",
        "| package(패키지) | lane(갈래) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val PF(검증 PF) | val rec(검증 회복) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | OOS PF(표본외 PF) | design gate(설계 관문) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        lines.append(
            "| {pkg} | {lane} | {vn:.2f} | {vtd:.2f} | {vpf:.2f} | {vrec:.2f} | {on:.2f} | {otd:.2f} | {opf:.2f} | {gate} |".format(
                pkg=row["package_id"],
                lane=row["branch_lane"],
                vn=number(row["validation_estimated_net_profit"]),
                vtd=number(row["validation_estimated_trades_per_day"]),
                vpf=number(row["validation_estimated_pf"]),
                vrec=number(row["validation_estimated_recovery"]),
                on=number(row["oos_estimated_net_profit"]),
                otd=number(row["oos_estimated_trades_per_day"]),
                opf=number(row["oos_estimated_pf"]),
                gate=row["design_gate"],
            )
        )
    lines.extend(["", f"- next_action(다음 행동): `{NEXT_ACTION}`", "", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Path],
) -> list[Path]:
    write_csv(BRANCH_QUEUE, list(branch_rows[0].keys()), branch_rows)
    write_csv(MODEL_SCOREBOARD, list(scoreboard[0].keys()), scoreboard)
    write_csv(CANDIDATE_SUPPLY, list(supply_rows[0].keys()), supply_rows)
    write_csv(PAYLOAD_MANIFEST, list(manifest_rows[0].keys()), manifest_rows)
    write_csv(MT5_QUEUE, list(manifest_rows[0].keys()), manifest_rows)
    write_text(
        EXPERIMENT_DESIGN,
        json.dumps(
            {
                "run_id": RUN_ID,
                "hypothesis": "A post-controller consensus/union surface can preserve Stage319 scale while reducing curve pockets without repeating Stage320 controller logic.",
                "decision_use": "Choose whether any Stage321 package deserves actual MT5 pressure before Adapter/ONNX.",
                "comparison_baseline": "Stage319 cp319D scale seed and Stage320 VIX/quality controller failure memory.",
                "control_variables": ["US100 M5", "Stage319 payload/runtime handoff", "Tier A primary plus Tier B fallback routed MT5 path", "no ONNX before candidate gate"],
                "changed_variables": ["multi-surface consensus", "D/B union priority", "D/A or D/F confirmation", "risk cap by branch lane"],
                "sample_scope": "validation_is and OOS routed MT5 scope inherited from Stage319/Stage320.",
                "success_criteria": ["actual MT5 4-10 trades/day", "minimum trade count", "net profit/PF/recovery/expectancy jointly acceptable", "no zoomed curve pocket collapse"],
                "failure_criteria": ["profit scale collapse", "density below 4 or above 10 trades/day", "DD pocket remains", "weak month/session concentration"],
                "invalid_conditions": ["missing payload lineage", "feature order mismatch", "MT5 KPI missing"],
                "stop_conditions": ["If actual MT5 rejects all branches, close Stage321 and pivot to a new source rather than repairing this one repeatedly."],
                "evidence_plan": [rel(MODEL_SCOREBOARD), rel(MT5_QUEUE), rel(CANDIDATE_SUPPLY), rel(CONSENSUS_SUMMARY), "run321B actual MT5 KPI", "run321C review"],
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(
        DATA_RECEIPT,
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_manifest": rel(SOURCE_MANIFEST),
                "source_stage319_kpi": rel(SOURCE_KPI),
                "source_stage320_review": rel(SOURCE_STAGE320_REVIEW),
                "source_stage320_failure_memory": rel(SOURCE_STAGE320_FAILURE),
                "source_trade_frame": rel(SOURCE_TRADE_FRAME),
                "feature_order_hash": RUNTIME_FEATURE_ORDER_HASH,
                "rows": {"branch_rows": len(branch_rows), "scoreboard_rows": len(scoreboard), "manifest_rows": len(manifest_rows)},
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}],
    )
    write_csv(
        GATE_AUDIT,
        ("gate_name", "status", "evidence_path", "effect"),
        [
            {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage320 제어기 반복을 버리고 합의/합집합 표면을 만들었다."},
            {"gate_name": "source_lineage(원천 계보)", "status": "passed", "evidence_path": rel(DATA_RECEIPT), "effect": "Stage319 수익 표면과 Stage320 실패 기억을 연결했다."},
            {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
            {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "actual MT5(실제 메타트레이더5) 전에는 Adapter(어댑터)를 시작하지 않는다."},
            {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "선택 후보가 없으므로 ONNX(온엑스)를 시작하지 않는다."},
        ],
    )
    write_text(
        RUN_MANIFEST,
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": len(scoreboard),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(
        LINEAGE,
        json.dumps(
            {
                "run_id": RUN_ID,
                "producer": rel(PRODUCER),
                "source_artifacts": [rel(SOURCE_MANIFEST), rel(SOURCE_KPI), rel(SOURCE_STAGE320_REVIEW), rel(SOURCE_STAGE320_FAILURE), rel(SOURCE_TRADE_FRAME)],
                "output_artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, CONSENSUS_SUMMARY, ACTUAL_TRADE_FRAME, *artifacts]],
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(REPORT, report_markdown(scoreboard))
    return [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, CONSENSUS_SUMMARY, ACTUAL_TRADE_FRAME, *artifacts]


def update_docs(scoreboard: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run321A_report(", "- run321A_mt5_queue("))
    selected = selected.rstrip() + f"\n- run321A_report(321A 보고서): `{rel(REPORT)}`\n- run321A_mt5_queue(321A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run321A_report(", "- run321A_scoreboard(", "- run321A_mt5_queue("))
    review_index = review_index.rstrip() + f"\n- run321A_report(321A 보고서): `{rel(REPORT)}`\n- run321A_scoreboard(321A 점수표): `{rel(MODEL_SCOREBOARD)}`\n- run321A_mt5_queue(321A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = drop_prefixed_lines(current, ("- run321A_summary(",))
    current = current.rstrip() + f"\n- run321A_summary(321A 요약): post-controller profit curve source(제어기 이후 수익 곡선 원천) 후보 `{len(scoreboard)}`개를 materialized(물질화)했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = prepend_focus(
        workspace,
        f"- >-\n  Stage321(321단계) run321A(321A 실행) post-controller profit curve source(제어기 이후 수익 곡선 원천) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n",
        RUN_ID,
    )
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run321A Post-controller profit curve source(321A 제어기 이후 수익 곡선 원천)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(scoreboard)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었다.\n"
    write_text(CHANGELOG, changelog)


def update_registers(scoreboard: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert(RUN_REGISTRY, s320.r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_controller_profit_curve_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, s320.ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "post_controller_profit_curve_materialization", "tier_scope": "Tier A/Tier B paired", "kpi_scope": "design_estimate_actual_replay", "scoreboard_lane": "onnx_candidate_campaign", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"candidates={len(scoreboard)};mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started", "external_verification_status": "not_started", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, s320.r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_controller_profit_curve_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += f"\n## {RUN_ID} post_controller_profit_curve_source(제어기 이후 수익 곡선 원천)\n\n- idea_id(아이디어 ID): `stage321_consensus_profit_curve_source`\n- hypothesis(가설): Stage319(319단계)의 D/B/F/A/C/E 표면 합의와 합집합이 Stage320(320단계) 제어기보다 수익 규모와 곡선 균형을 더 잘 보존할 수 있다.\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        write_text(IDEA_REGISTER, idea)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    created_at = utc_now()
    for path in paths:
        if not s320.r309.path_exists(path):
            continue
        rows.append({"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage321_post_controller_profit_curve_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "Stage321 materialization artifact"})
    safe_upsert(ARTIFACT_REGISTRY, s320.r309.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    branch_rows, scoreboard, supply_rows, manifest_rows, artifacts = build_outputs()
    outputs = write_outputs(branch_rows, scoreboard, supply_rows, manifest_rows, artifacts)
    update_docs(scoreboard, manifest_rows)
    update_registers(scoreboard, manifest_rows)
    update_artifact_registry(outputs)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_rows": len(scoreboard),
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

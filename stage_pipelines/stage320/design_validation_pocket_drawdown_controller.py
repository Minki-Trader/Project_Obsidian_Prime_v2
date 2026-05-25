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
from stage_pipelines.stage280.validate_directional_mapping_stability import drawdown_stats, profit_factor, trade_frame  # noqa: E402
from stage_pipelines.stage309 import review_split_coherent_profit_curve_source_mt5_probe as r309  # noqa: E402
from stage_pipelines.stage318 import design_post_non_time_curve_stability_rebuild as s318  # noqa: E402


STAGE_ID = "320_onnx_candidate_campaign__validation_pocket_drawdown_controller"
RUN_ID = "run320A_design_validation_pocket_drawdown_controller_packet_v1"
RUN_NUMBER = "run320A"
SOURCE_STAGE_ID = "319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild"
SOURCE_RUN_ID = "run319C_review_curve_pocket_risk_asymmetry_mt5_probe_v1"
SOURCE_MT5_RUN_ID = "run319B_execute_curve_pocket_risk_asymmetry_mt5_probe_v1"
UPDATED_ON = "2026-05-25"
STATUS = "completed_validation_pocket_drawdown_controller_candidates_materialized_no_selection"
JUDGMENT = "validation_pocket_drawdown_controller_candidates_materialized_requires_actual_mt5_no_selection"
NEXT_ACTION = "run320B_execute_validation_pocket_drawdown_controller_mt5_probe"
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
SOURCE_RUN319A = SOURCE_STAGE_ROOT / "02_runs" / "run319A"
SOURCE_RUN319B = SOURCE_STAGE_ROOT / "02_runs" / "run319B"
SOURCE_RUN319C = SOURCE_STAGE_ROOT / "02_runs" / "run319C"
SOURCE_SURVIVOR_QUEUE = SOURCE_RUN319C / "stage320_survivor_seed_queue.csv"
SOURCE_MANIFEST = SOURCE_RUN319A / "candidate_payload_manifest.csv"
SOURCE_KPI = SOURCE_RUN319B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = SOURCE_RUN319B / "attempt_summary.csv"

ACTUAL_TRADE_FRAME = RUN_ROOT / "run320A_stage319_survivor_actual_trade_frame.csv"
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
REPORT = REVIEWS / "run320A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

PRODUCER = Path("stage_pipelines/stage320/design_validation_pocket_drawdown_controller.py")
RUNTIME_FEATURE_ORDER = s318.RUNTIME_FEATURE_ORDER
RUNTIME_FEATURE_ORDER_HASH = s318.RUNTIME_FEATURE_ORDER_HASH
MODEL_FEATURE_ORDER_HASH = hashlib.sha256("stage320_validation_pocket_controller_v1".encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    source_package_id: str
    score_quantile: float
    filter_column: str
    filter_quantile: float
    filter_sense: str
    model_risk_max_pct: float
    fixed_lot: float
    hypothesis: str


def candidate_specs() -> list[CandidateSpec]:
    source = "cp319D_adx90_dense60_trend_cap_surface"
    return [
        CandidateSpec("cp320A_cp319D_vix30_pocket_controller_surface", source, 0.00, "vix_zscore_20", 0.30, "ge", 0.020, 0.32, "VIX z-score(VIX 표준점수)가 너무 낮은 검증 포켓을 제거해 DD%(드로다운 비율)를 낮춘다."),
        CandidateSpec("cp320B_cp319D_score10_vix25_scale_surface", source, 0.10, "vix_zscore_20", 0.25, "ge", 0.022, 0.34, "score floor(점수 바닥)을 약하게 두고 VIX filter(VIX 필터)로 규모와 곡선을 함께 본다."),
        CandidateSpec("cp320C_cp319D_score20_quality80_guard_surface", source, 0.20, "stage317_quality_scale_score", 0.80, "le", 0.020, 0.32, "quality scale(품질 규모) 과열 조각을 잘라 validation pocket(검증 포켓)을 줄인다."),
        CandidateSpec("cp320D_cp319D_vix30_lowrisk_surface", source, 0.00, "vix_zscore_20", 0.30, "ge", 0.016, 0.26, "같은 VIX controller(VIX 제어기)에 더 낮은 risk sizing(위험 크기)을 적용한다."),
        CandidateSpec("cp320E_cp319D_score10_vix25_lowrisk_surface", source, 0.10, "vix_zscore_20", 0.25, "ge", 0.018, 0.28, "규모형 VIX filter(VIX 필터)를 낮은 위험 크기로 압박한다."),
        CandidateSpec("cp320F_cp319D_score20_quality80_lowrisk_surface", source, 0.20, "stage317_quality_scale_score", 0.80, "le", 0.016, 0.26, "quality guard(품질 가드)를 낮은 위험 크기로 압박한다."),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return r309.rel(path)


def long_path(path: Path | str) -> Path:
    return ledger.io_path(path)


def read_text(path: Path) -> str:
    return r309.read_text(path)


def write_text(path: Path, text: str) -> None:
    r309.write_text(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    r309.write_csv(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    r309.safe_upsert(path, columns, rows, key)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return r309.read_csv_rows(path)


def sha256_file(path: Path) -> str:
    return r309.sha256_file(path)


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
    return r309.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return r309.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return r309.prepend_focus(workspace, focus, marker)


def load_manifest() -> tuple[list[str], dict[str, dict[str, str]]]:
    rows = read_csv_rows(SOURCE_MANIFEST)
    return list(rows[0].keys()) if rows else [], {row["package_id"]: row for row in rows}


def load_stage319_trades() -> pd.DataFrame:
    wanted = {spec.source_package_id for spec in candidate_specs()}
    attempts = {row["attempt_name"]: row for row in read_csv_rows(SOURCE_ATTEMPT_SUMMARY)}
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
            frame = trade_frame(Path(metrics.get("report_path", "")))
            if frame.empty:
                continue
            frame["source_package_id"] = package_id
            frame["split"] = str(row.get("split", ""))
            frame["dir_val"] = frame["direction"].map({"buy": 1, "sell": -1}).astype("int8")
            frame["open_floor"] = pd.to_datetime(frame["open_time"]).dt.floor("5min")
            frame["trade_key"] = frame["open_floor"].astype(str) + "|" + frame["dir_val"].astype(str)
            frames.append(frame)
    result = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    write_csv(ACTUAL_TRADE_FRAME, list(result.columns) if not result.empty else ["source_package_id"], result.to_dict("records") if not result.empty else [])
    return result


def summarize(values: Sequence[float], close_times: Sequence[Any] | None = None) -> dict[str, Any]:
    profits = [float(value) for value in values]
    net = float(sum(profits))
    dd = float(drawdown_stats(profits)["max_drawdown"]) if profits else 0.0
    monthly: dict[str, float] = defaultdict(float)
    if close_times is not None:
        for close_time, profit in zip(close_times, profits):
            monthly[pd.to_datetime(close_time).strftime("%Y-%m")] += profit
    balance = 500.0
    peak = 500.0
    underwater = 0
    max_underwater = 0
    for profit in profits:
        balance += profit
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            max_underwater = max(max_underwater, underwater)
    return {
        "net_profit": round(net, 2),
        "trade_count": len(profits),
        "profit_factor": round(float(profit_factor(profits)), 6),
        "max_drawdown": round(dd, 2),
        "drawdown_to_net_ratio": round(dd / net, 6) if net > 0 else 999.0,
        "recovery_factor": round(net / dd, 6) if dd > 0 else (99.0 if net > 0 else 0.0),
        "expectancy": round(net / len(profits), 6) if profits else 0.0,
        "positive_month_share": round(sum(1 for value in monthly.values() if value > 0) / len(monthly), 6) if monthly else 0.0,
        "max_underwater_trades": int(max_underwater),
    }


def estimate(package_id: str, payload: pd.DataFrame, trades: pd.DataFrame) -> dict[str, dict[str, Any]]:
    signal = pd.to_numeric(payload["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    selected = set(pd.to_datetime(payload.loc[signal.ne(0), "ts_floor"]).astype(str) + "|" + signal[signal.ne(0)].astype(str))
    out: dict[str, dict[str, Any]] = {}
    for split, name, days in (("validation_is", "validation", 183), ("oos", "oos", 131)):
        source = trades[(trades["source_package_id"] == package_id) & (trades["split"] == split)]
        picked = source[source["trade_key"].isin(selected)]
        summary = summarize(picked["net_profit"].tolist(), picked["close_time"].tolist())
        summary["trades_per_day"] = round(summary["trade_count"] / days, 6)
        out[name] = summary
    return out


def materialize(spec: CandidateSpec, source: pd.DataFrame, manifest_row: Mapping[str, str], columns: Sequence[str], trades: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any], dict[str, str], dict[str, dict[str, Any]]]:
    active = pd.to_numeric(source["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    score = pd.to_numeric(source["candidate_decision_score"], errors="coerce")
    filt = pd.to_numeric(source[spec.filter_column], errors="coerce")
    mask = active.ne(0) & score.ge(score[active.ne(0)].quantile(spec.score_quantile))
    threshold = filt[active.ne(0)].quantile(spec.filter_quantile)
    mask &= filt.ge(threshold) if spec.filter_sense == "ge" else filt.le(threshold)
    signal = np.where(mask.to_numpy(), active.to_numpy(), 0).astype("int8")
    branch_id = f"run320A_{spec.package_id.replace('_surface', '')}"
    payload = source.copy()
    payload["stage320_branch_id"] = branch_id
    payload["stage319_source_package_id"] = spec.source_package_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "validation_pocket_drawdown_controller_surface"
    payload["stage320_score_quantile"] = spec.score_quantile
    payload["stage320_filter_column"] = spec.filter_column
    payload["stage320_filter_quantile"] = spec.filter_quantile
    payload["stage320_filter_sense"] = spec.filter_sense
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = ["long" if value > 0 else ("short" if value < 0 else "flat") for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct
    payload["payload_claim_boundary"] = BOUNDARY
    risk = {column: manifest_row.get(column, "") for column in columns}
    risk.update({"model_risk_sizing_enabled": "1", "model_risk_min_pct": "0.003", "model_risk_max_pct": str(spec.model_risk_max_pct), "model_risk_confidence_floor": "0.60", "model_risk_confidence_ceiling": "0.99", "model_risk_fallback_lot": "0.06", "fixed_lot": str(spec.fixed_lot)})
    replay = estimate(spec.source_package_id, payload, trades)
    identity = {"package_id": spec.package_id, "source_stage_id": SOURCE_STAGE_ID, "source_run_id": SOURCE_RUN_ID, "source_mt5_run_id": SOURCE_MT5_RUN_ID, "source_package_id": spec.source_package_id, "score_quantile": spec.score_quantile, "filter_column": spec.filter_column, "filter_quantile": spec.filter_quantile, "filter_sense": spec.filter_sense, "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH, "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH, "risk_logic": risk, "claim_boundary": BOUNDARY}
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = RUNTIME_FEATURE_ORDER_HASH
    payload["model_feature_order_hash"] = MODEL_FEATURE_ORDER_HASH
    drop_cols = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    return payload.drop(columns=drop_cols, errors="ignore"), identity | {"direction_surface_hash": surface_hash}, risk, replay


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    columns, manifest = load_manifest()
    trades = load_stage319_trades()
    payload_cache: dict[str, pd.DataFrame] = {}
    branch_rows: list[dict[str, Any]] = []
    scoreboard: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        if spec.source_package_id not in payload_cache:
            payload_cache[spec.source_package_id] = pd.read_parquet(long_path(ROOT / manifest[spec.source_package_id]["payload_path"]))
        payload, identity, risk, replay = materialize(spec, payload_cache[spec.source_package_id], manifest[spec.source_package_id], columns, trades)
        branch_id = f"run320A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_path = MODEL_DIR / f"{branch_id}_validation_pocket_controller.json"
        payload_path.parent.mkdir(parents=True, exist_ok=True)
        payload.to_parquet(long_path(payload_path), index=False)
        write_text(model_path, json.dumps(identity, ensure_ascii=False, indent=2, sort_keys=True))
        write_text(handoff_path, json.dumps({"package_id": spec.package_id, "materialized_branch_id": branch_id, "runtime_feature_order": list(RUNTIME_FEATURE_ORDER), "runtime_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH, "risk_logic": risk, "runtime_handoff": "precomputed route_signal_value replay for Stage320 MT5 probe(320단계 MT5 탐침)", "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
        val, oos = replay["validation"], replay["oos"]
        gates = {
            "minimum_trade_gate": "passed" if number(val["trade_count"]) >= 730 and number(oos["trade_count"]) >= 520 else "failed",
            "density_4_10_trades_day_gate": "passed" if 4.0 <= number(val["trades_per_day"]) <= 10.0 and 4.0 <= number(oos["trades_per_day"]) <= 10.0 else "failed",
            "profit_scale_gate": "passed" if number(val["net_profit"]) >= 8000 and number(oos["net_profit"]) >= 8000 else "failed",
            "efficiency_gate": "passed" if number(val["profit_factor"]) >= 1.15 and number(oos["profit_factor"]) >= 1.12 else "failed",
            "curve_pocket_design_gate": "passed" if number(val["drawdown_to_net_ratio"]) <= 0.35 and number(oos["drawdown_to_net_ratio"]) <= 0.35 and number(val["positive_month_share"]) >= 0.70 and number(oos["positive_month_share"]) >= 0.70 and number(val["max_underwater_trades"]) <= 320 and number(oos["max_underwater_trades"]) <= 320 else "failed",
        }
        design_gate = "passed" if all(value == "passed" for value in gates.values()) else "failed"
        scoreboard.append({"materialized_branch_id": branch_id, "package_id": spec.package_id, "source_package_id": spec.source_package_id, "validation_estimated_net_profit": val["net_profit"], "validation_estimated_pf": val["profit_factor"], "validation_estimated_trades": val["trade_count"], "validation_estimated_trades_per_day": val["trades_per_day"], "validation_estimated_dd_to_net": val["drawdown_to_net_ratio"], "validation_estimated_positive_month_share": val["positive_month_share"], "validation_estimated_max_underwater_trades": val["max_underwater_trades"], "oos_estimated_net_profit": oos["net_profit"], "oos_estimated_pf": oos["profit_factor"], "oos_estimated_trades": oos["trade_count"], "oos_estimated_trades_per_day": oos["trades_per_day"], "oos_estimated_dd_to_net": oos["drawdown_to_net_ratio"], "oos_estimated_positive_month_share": oos["positive_month_share"], "oos_estimated_max_underwater_trades": oos["max_underwater_trades"], "combined_estimated_net_profit": number(val["net_profit"]) + number(oos["net_profit"]), **gates, "design_gate": design_gate, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started"})
        branch_rows.append({"branch_id": branch_id, "package_id": spec.package_id, "source_package_id": spec.source_package_id, "hypothesis": spec.hypothesis, "decision_surface": f"candidate_decision_score >= q{spec.score_quantile}; {spec.filter_column} {spec.filter_sense} q{spec.filter_quantile}", "risk_logic": json.dumps(risk, sort_keys=True), "claim_boundary": BOUNDARY})
        for split_name in ("validation", "oos"):
            split_frame = payload[payload["split"].astype(str).eq(split_name)]
            active_count = int(pd.to_numeric(split_frame["route_signal_value"], errors="coerce").fillna(0).ne(0).sum())
            days = max(1, pd.to_datetime(split_frame["timestamp"]).dt.date.nunique()) if not split_frame.empty else 1
            est = replay[split_name]
            supply_rows.append({"materialized_branch_id": branch_id, "package_id": spec.package_id, "split": split_name, "active_signal_rows": active_count, "approx_signal_rows_per_day": round(active_count / days, 6), "estimated_actual_trade_count": est["trade_count"], "estimated_actual_trades_per_day": est["trades_per_day"], "estimated_actual_net_profit": est["net_profit"], "estimated_actual_pf": est["profit_factor"], "claim_boundary": BOUNDARY})
        manifest_row = {column: manifest[spec.source_package_id].get(column, "") for column in columns}
        manifest_row.update({"queue_id": f"run320A_queue_{index:02d}", "materialized_branch_id": branch_id, "package_id": spec.package_id, "queue_role": "validation_pocket_drawdown_controller_surface", "payload_path": rel(payload_path), "payload_hash": sha256_file(payload_path), "handoff_path": rel(handoff_path), "handoff_hash": sha256_file(handoff_path), "model_artifact_path": rel(model_path), "model_artifact_hash": sha256_file(model_path), "model_feature_order_path": rel(model_path), "model_feature_order_hash": MODEL_FEATURE_ORDER_HASH, "direction_surface_hash": identity["direction_surface_hash"], "direction_feature_order_hash": RUNTIME_FEATURE_ORDER_HASH, "model_risk_sizing_enabled": "1", "model_risk_min_pct": "0.003", "model_risk_max_pct": str(spec.model_risk_max_pct), "model_risk_confidence_floor": "0.60", "model_risk_confidence_ceiling": "0.99", "model_risk_fallback_lot": "0.06", "fixed_lot": str(spec.fixed_lot), "approx_validation_trades_per_day": val["trades_per_day"], "approx_oos_trades_per_day": oos["trades_per_day"], "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "claim_boundary": BOUNDARY})
        manifest_rows.append(manifest_row)
        artifacts.extend([payload_path, handoff_path, model_path])
    scoreboard.sort(key=lambda row: number(row["combined_estimated_net_profit"]), reverse=True)
    return branch_rows, scoreboard, supply_rows, manifest_rows, artifacts


def report_markdown(scoreboard: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# run320A Validation Pocket Drawdown Controller Materialization(320A 검증 포켓 드로다운 제어기 물질화)", "", f"- run_id(실행 ID): `{RUN_ID}`", f"- candidates(후보): `{len(scoreboard)}`", "- selected_candidate(선택 후보): `none`", "- Adapter package(어댑터 패키지): `none`", "- ONNX readiness(온엑스 준비): `not_started`", "", "Effect(효과): cp319D(319D 후보)의 수익 규모를 유지하면서 VIX/quality state(VIX/품질 상태)로 validation pocket(검증 포켓)을 줄이는 후보를 만들었다.", "", "| package(패키지) | val net est(검증 추정 순익) | val t/day(검증 일거래) | val DD/net(검증 DD/순익) | OOS net est(표본외 추정 순익) | OOS t/day(표본외 일거래) | design gate(설계 관문) |", "|---|---:|---:|---:|---:|---:|---|"]
    for row in scoreboard:
        lines.append("| {pkg} | {vn:.2f} | {vtd:.2f} | {vdd:.2f} | {on:.2f} | {otd:.2f} | {gate} |".format(pkg=row["package_id"], vn=number(row["validation_estimated_net_profit"]), vtd=number(row["validation_estimated_trades_per_day"]), vdd=number(row["validation_estimated_dd_to_net"]), on=number(row["oos_estimated_net_profit"]), otd=number(row["oos_estimated_trades_per_day"]), gate=row["design_gate"]))
    lines.extend(["", f"- next_action(다음 행동): `{NEXT_ACTION}`", "", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(branch_rows: Sequence[Mapping[str, Any]], scoreboard: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> list[Path]:
    write_csv(BRANCH_QUEUE, list(branch_rows[0].keys()), branch_rows)
    write_csv(MODEL_SCOREBOARD, list(scoreboard[0].keys()), scoreboard)
    write_csv(CANDIDATE_SUPPLY, list(supply_rows[0].keys()), supply_rows)
    write_csv(PAYLOAD_MANIFEST, list(manifest_rows[0].keys()), manifest_rows)
    write_csv(MT5_QUEUE, list(manifest_rows[0].keys()), manifest_rows)
    write_text(EXPERIMENT_DESIGN, json.dumps({"run_id": RUN_ID, "hypothesis": "Validation pocket drawdown controller can reduce DD while preserving 4-10 trades/day.", "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2))
    write_text(DATA_RECEIPT, json.dumps({"run_id": RUN_ID, "source_survivor_queue": rel(SOURCE_SURVIVOR_QUEUE), "source_manifest": rel(SOURCE_MANIFEST), "source_kpi": rel(SOURCE_KPI), "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2))
    write_csv(RESULT_JUDGMENT, ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"), [{"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}])
    write_csv(GATE_AUDIT, ("gate_name", "status", "evidence_path", "effect"), [{"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "payload(페이로드)와 MT5 queue(MT5 대기열)를 만들었다."}, {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "actual MT5(실제 메타트레이더5) 전에는 시작하지 않는다."}])
    write_text(RUN_MANIFEST, json.dumps({"run_id": RUN_ID, "stage_id": STAGE_ID, "status": STATUS, "judgment": JUDGMENT, "candidate_rows": len(scoreboard), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(LINEAGE, json.dumps({"run_id": RUN_ID, "producer": rel(PRODUCER), "source_artifacts": [rel(SOURCE_SURVIVOR_QUEUE), rel(SOURCE_MANIFEST), rel(SOURCE_KPI)], "output_artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, REPORT, *artifacts]], "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard))
    return [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, ACTUAL_TRADE_FRAME, *artifacts]


def update_docs(scoreboard: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run320A_report(", "- run320A_mt5_queue("))
    selected = selected.rstrip() + f"\n- run320A_report(320A 보고서): `{rel(REPORT)}`\n- run320A_mt5_queue(320A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(SELECTED, selected)
    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run320A_report(", "- run320A_scoreboard(", "- run320A_mt5_queue("))
    review_index = review_index.rstrip() + f"\n- run320A_report(320A 보고서): `{rel(REPORT)}`\n- run320A_scoreboard(320A 점수표): `{rel(MODEL_SCOREBOARD)}`\n- run320A_mt5_queue(320A MT5 대기열): `{rel(MT5_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)
    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = drop_prefixed_lines(current, ("- run320A_summary(",))
    current = current.rstrip() + f"\n- run320A_summary(320A 요약): validation pocket drawdown controller(검증 포켓 드로다운 제어기) 후보 `{len(scoreboard)}`개를 materialized(물질화)했다. Effect(효과): MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.\n"
    write_text(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = prepend_focus(workspace, f"- >-\n  Stage320(320단계) run320A(320A 실행) validation pocket drawdown controller(검증 포켓 드로다운 제어기) `{RUN_ID}`. Effect(효과): candidates(후보) `{len(scoreboard)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n", RUN_ID)
    write_text(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run320A Validation pocket drawdown controller(320A 검증 포켓 드로다운 제어기)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(scoreboard)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었다.\n"
    write_text(CHANGELOG, changelog)


def update_registers(scoreboard: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert(RUN_REGISTRY, r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "validation_pocket_drawdown_controller_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"candidates={len(scoreboard)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "validation_pocket_drawdown_controller_materialization", "tier_scope": "Tier A/Tier B paired", "kpi_scope": "design_estimate_actual_replay", "scoreboard_lane": "onnx_candidate_campaign", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"candidates={len(scoreboard)};mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_started", "external_verification_status": "not_started", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "validation_pocket_drawdown_controller_materialization", "tier_scope": "Tier A/Tier B paired", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}], "row_id")
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += f"\n## {RUN_ID} validation_pocket_drawdown_controller(검증 포켓 드로다운 제어기)\n\n- idea_id(아이디어 ID): `stage320_validation_pocket_drawdown_controller`\n- hypothesis(가설): cp319D(319D 후보)의 validation pocket(검증 포켓)은 VIX/quality state(VIX/품질 상태)로 줄일 수 있다.\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        write_text(IDEA_REGISTER, idea)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    created_at = utc_now()
    for path in paths:
        if not r309.path_exists(path):
            continue
        rows.append({"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage320_validation_pocket_drawdown_controller_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "Stage320 materialization artifact"})
    safe_upsert(ARTIFACT_REGISTRY, r309.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    branch_rows, scoreboard, supply_rows, manifest_rows, artifacts = build_outputs()
    outputs = write_outputs(branch_rows, scoreboard, supply_rows, manifest_rows, artifacts)
    update_docs(scoreboard, manifest_rows)
    update_registers(scoreboard, manifest_rows)
    update_artifact_registry(outputs)
    print(json.dumps({"status": STATUS, "judgment": JUDGMENT, "candidate_rows": len(scoreboard), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

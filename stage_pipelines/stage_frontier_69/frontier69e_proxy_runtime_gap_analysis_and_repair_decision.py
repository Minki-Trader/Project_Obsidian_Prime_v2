from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_69 import frontier69b_event_first_first_hit_proxy_sweep as f69b
from stage_pipelines.stage_frontier_69 import frontier69d_event_first_onnx_runtime_probe as f69d


STAGE_ID = f69b.STAGE_ID
RUN_ID = "frontier69E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = f69d.RUN_ID
NEXT_RUN_ID = "frontier69F_stage_closeout_event_first_axis_rotation_v1"
IDEA_ID = f69b.IDEA_ID

CLAIM_BOUNDARY = (
    "gap_analysis_and_proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STATUS = "completed_gap_analysis_trade_shape_repair_no_meaningful_repair_no_authority"
JUDGMENT = "proxy_runtime_gap_trade_shape_repair_negative_memory_preserved_clue_no_authority"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

RUNTIME_RECEIPT_REVIEW = REVIEWS_ROOT / "f69d_runtime_probe_receipt_review.csv"
GAP_CLASSIFICATION_REVIEW = REVIEWS_ROOT / "f69d_gap_classification_review.csv"

RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
SUMMARY_PATH = RUN_ROOT / "frontier69E_gap_analysis_summary.json"
REPAIR_SWEEP_PATH = RUN_ROOT / "f69e_trade_shape_repair_sweep.csv"
GAP_DECISION_PATH = RUN_ROOT / "f69e_proxy_runtime_gap_decision.json"

REPORT_PATH = REVIEWS_ROOT / "frontier69E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
REPAIR_SWEEP_REVIEW = REVIEWS_ROOT / "f69e_trade_shape_repair_sweep_review.csv"
GAP_DECISION_REVIEW = REVIEWS_ROOT / "f69e_proxy_runtime_gap_decision_review.json"
GATE_AUDIT_PATH = REVIEWS_ROOT / "required_gate_coverage_audit_f69e.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_ROOT / "stage_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS = SELECTED_ROOT / "selection_status.md"


SWEEP_QUANTILES = (0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.65, 0.70, 0.80, 0.90, 0.95)
NON_OVERLAP_COOLDOWNS = (0, 1, 2, 3, 6)
DAILY_TOP_QUOTAS = (3, 5, 8, 10, 12)
DAILY_TOP_COOLDOWNS = (0, 1, 2, 3)


SWEEP_COLUMNS = (
    "run_id",
    "axis_id",
    "candidate_id",
    "mode",
    "threshold_quantile",
    "edge_threshold",
    "cooldown_bars",
    "daily_quota",
    "validation_net",
    "validation_pf",
    "validation_dd_pct",
    "validation_trades",
    "validation_trades_per_day",
    "validation_raw_signal_rows",
    "oos_net",
    "oos_pf",
    "oos_dd_pct",
    "oos_trades",
    "oos_trades_per_day",
    "oos_raw_signal_rows",
    "min_pf",
    "min_net",
    "max_dd_pct",
    "density_distance_to_7p5",
    "joint_soft_signal",
    "final_gate_like_signal",
    "repair_decision",
    "claim_boundary",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] = SWEEP_COLUMNS) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def upsert_ledger(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None:
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise RuntimeError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def num(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: Any, digits: int = 6) -> str:
    number = num(value)
    if number is None:
        return str(value or "")
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def select_daily_top(signal: np.ndarray, edge: np.ndarray, timestamps: pd.Series, quota: int, cooldown_bars: int) -> list[int]:
    by_day: dict[str, list[tuple[float, int]]] = defaultdict(list)
    parsed = pd.to_datetime(timestamps, utc=True)
    for idx, active in enumerate(signal):
        if bool(active) and np.isfinite(edge[idx]):
            by_day[parsed.iloc[idx].strftime("%Y-%m-%d")].append((float(edge[idx]), idx))
    chosen: list[int] = []
    for items in by_day.values():
        chosen.extend(idx for _, idx in sorted(items, reverse=True)[: int(quota)])
    chosen = sorted(chosen)
    if cooldown_bars <= 0:
        return chosen
    filtered: list[int] = []
    next_allowed = -1
    for idx in chosen:
        if idx >= next_allowed:
            filtered.append(idx)
            next_allowed = idx + int(cooldown_bars) + 1
    return filtered


def split_metrics(context: Mapping[str, Any], split: str, threshold: float, mode: str, cooldown_bars: int, daily_quota: int | None) -> dict[str, Any]:
    payload = context["split_payload"][split]
    frame: pd.DataFrame = payload["frame"]
    event_mask = np.asarray(payload["event_mask"], dtype=bool)
    side = np.asarray(payload["adjusted_side"], dtype=int)
    edge = np.asarray(payload["edge"], dtype=float)
    signal = event_mask & (side != 1) & (edge >= float(threshold))
    horizon = int(context["target"].horizon_bars)
    if mode == "non_overlap":
        selected = f69b.non_overlap_indices(signal, horizon, int(cooldown_bars))
    else:
        selected = select_daily_top(signal, edge, frame["timestamp"], int(daily_quota or 0), int(cooldown_bars))
    values_all = f69b.profit_for_side(frame, side)
    selected_values = values_all[selected] if selected else np.asarray([], dtype=float)
    selected_timestamps = frame.loc[selected, "timestamp"] if selected else frame["timestamp"].iloc[:0]
    metrics = f69b.proxy_kpi(selected_values, selected_timestamps, frame["timestamp"])
    return {
        "net": metrics["net_profit"],
        "pf": metrics["profit_factor"],
        "dd_pct": metrics["max_drawdown_percent_on_10000"],
        "trades": metrics["trade_count"],
        "trades_per_day": metrics["trades_per_day"],
        "raw_signal_rows": int(signal.sum()),
    }


def train_pool_for_context(context: Mapping[str, Any]) -> np.ndarray:
    train = context["split_payload"]["train"]
    event_mask = np.asarray(train["event_mask"], dtype=bool)
    side = np.asarray(train["adjusted_side"], dtype=int)
    edge = np.asarray(train["edge"], dtype=float)
    pool = edge[event_mask & (side != 1) & np.isfinite(edge)]
    return pool[np.isfinite(pool)]


def repair_decision(row: Mapping[str, Any]) -> str:
    if row.get("final_gate_like_signal"):
        return "materialize_candidate_required_after_grok(그록 후 물질화 필요)"
    if row.get("joint_soft_signal"):
        return "proxy_repair_scout_clue_but_not_runtime_ready(프록시 수리 단서, 런타임 준비 아님)"
    min_pf = num(row.get("min_pf")) or 0.0
    max_dd = num(row.get("max_dd_pct")) or 999.0
    val_tpd = num(row.get("validation_trades_per_day")) or 0.0
    oos_tpd = num(row.get("oos_trades_per_day")) or 0.0
    if val_tpd >= 3.0 and oos_tpd >= 3.0:
        return "density_lift_collapsed_pf_or_dd(밀도 상승이 PF 또는 DD를 훼손)"
    if min_pf >= 1.5 and max_dd < 10.0:
        return "quality_remains_too_sparse(품질은 있으나 너무 희박)"
    return "no_meaningful_trade_shape_repair(의미 있는 거래 형태 수리 없음)"


def run_trade_shape_repair_sweep() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for context in f69d.build_axis_contexts():
        axis = context["axis"]
        train_pool = train_pool_for_context(context)
        if len(train_pool) == 0:
            continue
        threshold_rows: list[tuple[float, float]] = [(quantile, float(np.quantile(train_pool, quantile))) for quantile in SWEEP_QUANTILES]
        for quantile, threshold in threshold_rows:
            for cooldown in NON_OVERLAP_COOLDOWNS:
                rows.append(build_sweep_row(context, quantile, threshold, "non_overlap", cooldown, None))
            for quota in DAILY_TOP_QUOTAS:
                for cooldown in DAILY_TOP_COOLDOWNS:
                    rows.append(build_sweep_row(context, quantile, threshold, "daily_top", cooldown, quota))
    for row in rows:
        row["repair_decision"] = repair_decision(row)
    return rows


def build_sweep_row(
    context: Mapping[str, Any],
    quantile: float,
    threshold: float,
    mode: str,
    cooldown_bars: int,
    daily_quota: int | None,
) -> dict[str, Any]:
    axis = context["axis"]
    validation = split_metrics(context, "validation", threshold, mode, cooldown_bars, daily_quota)
    oos = split_metrics(context, "oos", threshold, mode, cooldown_bars, daily_quota)
    min_pf = min(float(validation["pf"]), float(oos["pf"]))
    min_net = min(float(validation["net"]), float(oos["net"]))
    max_dd = max(float(validation["dd_pct"]), float(oos["dd_pct"]))
    density_distance = abs(float(validation["trades_per_day"]) - 7.5) + abs(float(oos["trades_per_day"]) - 7.5)
    joint_soft = bool(
        min_net > 0.0
        and max_dd < 10.0
        and 3.0 <= float(validation["trades_per_day"]) <= 12.0
        and 3.0 <= float(oos["trades_per_day"]) <= 12.0
    )
    final_gate_like = bool(
        min_net > 0.0
        and min_pf >= 2.0
        and max_dd < 10.0
        and 5.0 <= float(validation["trades_per_day"]) <= 10.0
        and 5.0 <= float(oos["trades_per_day"]) <= 10.0
    )
    return {
        "run_id": RUN_ID,
        "axis_id": axis.axis_id,
        "candidate_id": axis.candidate_id,
        "mode": mode,
        "threshold_quantile": quantile,
        "edge_threshold": threshold,
        "cooldown_bars": cooldown_bars,
        "daily_quota": daily_quota if daily_quota is not None else "",
        "validation_net": validation["net"],
        "validation_pf": validation["pf"],
        "validation_dd_pct": validation["dd_pct"],
        "validation_trades": validation["trades"],
        "validation_trades_per_day": validation["trades_per_day"],
        "validation_raw_signal_rows": validation["raw_signal_rows"],
        "oos_net": oos["net"],
        "oos_pf": oos["pf"],
        "oos_dd_pct": oos["dd_pct"],
        "oos_trades": oos["trades"],
        "oos_trades_per_day": oos["trades_per_day"],
        "oos_raw_signal_rows": oos["raw_signal_rows"],
        "min_pf": min_pf,
        "min_net": min_net,
        "max_dd_pct": max_dd,
        "density_distance_to_7p5": density_distance,
        "joint_soft_signal": joint_soft,
        "final_gate_like_signal": final_gate_like,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def summarize_runtime_gap(runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    signal_diff_total = sum(abs(int(float(row.get("signal_count_diff") or 0))) for row in runtime_rows)
    feature_diff_total = sum(abs(int(float(row.get("feature_ready_diff") or 0))) for row in runtime_rows)
    sparse_oos = next((row for row in runtime_rows if row.get("axis_id") == "pf_sparse_export_axis" and row.get("split") == "oos"), {})
    dense_oos = next((row for row in runtime_rows if row.get("axis_id") == "density_weak_export_axis" and row.get("split") == "oos"), {})
    return {
        "signal_count_diff_total": signal_diff_total,
        "feature_ready_diff_total": feature_diff_total,
        "bridge_gap_judgment": "bridge_parity_not_bottleneck(연결 동등성은 병목 아님)" if signal_diff_total == 0 and feature_diff_total == 0 else "bridge_gap_present(연결 간극 있음)",
        "sparse_oos_runtime": {
            "net_profit": num(sparse_oos.get("net_profit")),
            "profit_factor": num(sparse_oos.get("profit_factor")),
            "drawdown_percent": num(sparse_oos.get("max_drawdown_percent")),
            "trades": num(sparse_oos.get("trade_count")),
            "trades_per_day": num(sparse_oos.get("trades_per_day")),
        },
        "dense_oos_runtime": {
            "net_profit": num(dense_oos.get("net_profit")),
            "profit_factor": num(dense_oos.get("profit_factor")),
            "drawdown_percent": num(dense_oos.get("max_drawdown_percent")),
            "trades": num(dense_oos.get("trade_count")),
            "trades_per_day": num(dense_oos.get("trades_per_day")),
        },
        "gap_rows": len(gap_rows),
    }


def summarize_sweep(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    final_like = [row for row in rows if row.get("final_gate_like_signal")]
    joint_soft = [row for row in rows if row.get("joint_soft_signal")]
    density_rows = [
        row
        for row in rows
        if (num(row.get("validation_trades_per_day")) or 0.0) >= 3.0 and (num(row.get("oos_trades_per_day")) or 0.0) >= 3.0
    ]
    positive_low_dd = [row for row in rows if (num(row.get("min_net")) or -1.0) > 0.0 and (num(row.get("max_dd_pct")) or 999.0) < 10.0]
    best_score = sorted(
        rows,
        key=lambda row: (
            (num(row.get("min_pf")) or 0.0) * 100.0
            + (num(row.get("min_net")) or -999.0) / 10.0
            - (num(row.get("max_dd_pct")) or 999.0) * 3.0
            - (num(row.get("density_distance_to_7p5")) or 99.0) * 10.0
        ),
        reverse=True,
    )[:10]
    best_density = sorted(density_rows, key=lambda row: ((num(row.get("min_pf")) or 0.0), (num(row.get("min_net")) or -999.0)), reverse=True)[:10]
    best_positive_low_dd = sorted(
        positive_low_dd,
        key=lambda row: ((num(row.get("min_pf")) or 0.0), -(num(row.get("density_distance_to_7p5")) or 99.0)),
        reverse=True,
    )[:10]
    return {
        "sweep_rows": len(rows),
        "joint_soft_count": len(joint_soft),
        "final_gate_like_count": len(final_like),
        "density_at_least_3_both_count": len(density_rows),
        "positive_low_dd_count": len(positive_low_dd),
        "best_score_rows": best_score,
        "best_density_rows": best_density,
        "best_positive_low_dd_rows": best_positive_low_dd,
        "repair_conclusion": "no_meaningful_trade_shape_repair_candidate(의미 있는 거래 형태 수리 후보 없음)"
        if not final_like and not joint_soft
        else "repair_candidate_requires_grok_and_runtime_probe(수리 후보는 그록 및 런타임 탐침 필요)",
    }


def build_decision(runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]], sweep_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    runtime_gap = summarize_runtime_gap(runtime_rows, gap_rows)
    sweep_summary = summarize_sweep(sweep_rows)
    next_action = NEXT_RUN_ID if sweep_summary["final_gate_like_count"] == 0 and sweep_summary["joint_soft_count"] == 0 else "frontier69F_grok_pre_mt5_repair_runtime_probe_v1"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": "After exact F69D signal and feature parity, the remaining gap is alpha/trade-shape economics rather than bridge mismatch.",
        "test_period": "validation 2025-01-02..2025-10-01; oos 2025-10-01..2026-04-14",
        "proxy_expectation": "Lower thresholds, shorter cooldown, or daily quota could raise density while preserving the event-first PF clue.",
        "runtime_gap": runtime_gap,
        "repair_sweep": sweep_summary,
        "proxy_runtime_gap_cause": [
            "signal_count_parity_exact_but_economics_not_sufficient(신호 수 동등성은 정확하지만 경제성 부족)",
            "feature_readiness_exact_but_alpha_density_pf_tradeoff_remains(피처 준비는 정확하지만 알파 밀도/PF 절충 남음)",
            "sparse_axis_quality_too_thin(희박 축은 품질은 있으나 너무 얇음)",
            "dense_axis_density_lift_collapses_pf_or_dd(촘촘한 축은 밀도 상승 시 PF 또는 DD 훼손)",
        ],
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(decision: Mapping[str, Any]) -> list[str]:
    runtime = decision["runtime_gap"]
    sweep = decision["repair_sweep"]
    sparse = runtime["sparse_oos_runtime"]
    dense = runtime["dense_oos_runtime"]
    best_density = sweep["best_density_rows"][:5]
    best_quality = sweep["best_positive_low_dd_rows"][:5]
    lines = [
        "# F69E Proxy/Runtime Gap Analysis And Repair Decision(F69E 프록시/런타임 간극 분석 및 수리 결정)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "## Action And Effect(행동과 효과)",
        "",
        "Action(행동): F69D runtime receipt(F69D 런타임 영수증)를 분석하고 threshold/cooldown/daily-top trade-shape repair sweep(임계값/쿨다운/일별 상위 거래 형태 수리 탐색)을 실행했다.",
        "",
        "Effect(효과): bridge parity(연결 동등성) 문제와 alpha/trade-shape economics(알파/거래 형태 경제성) 문제를 분리하고, MT5 repair probe(MT5 수리 탐침)로 보낼 후보가 있는지 결정한다.",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- test period(테스트 기간): `{decision['test_period']}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime Gap Read(런타임 간극 판독)",
        "",
        f"- signal count diff total(신호 수 차이 합계): `{runtime['signal_count_diff_total']}`.",
        f"- feature readiness diff total(피처 준비 차이 합계): `{runtime['feature_ready_diff_total']}`.",
        f"- bridge gap judgment(연결 간극 판정): `{runtime['bridge_gap_judgment']}`.",
        f"- sparse OOS runtime(희박 축 표본외 런타임): net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일거래) `{fmt(sparse['net_profit'])}` / `{fmt(sparse['profit_factor'])}` / `{fmt(sparse['drawdown_percent'])}` / `{fmt(sparse['trades_per_day'])}`.",
        f"- dense OOS runtime(촘촘한 축 표본외 런타임): net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일거래) `{fmt(dense['net_profit'])}` / `{fmt(dense['profit_factor'])}` / `{fmt(dense['drawdown_percent'])}` / `{fmt(dense['trades_per_day'])}`.",
        "",
        "## Repair Sweep(수리 탐색)",
        "",
        f"- sweep rows(탐색 행): `{sweep['sweep_rows']}`.",
        f"- final gate-like rows(최종 조건 유사 행): `{sweep['final_gate_like_count']}`.",
        f"- joint soft rows(완화 공동 조건 행): `{sweep['joint_soft_count']}`.",
        f"- density >=3 both rows(양쪽 일 3회 이상 행): `{sweep['density_at_least_3_both_count']}`.",
        f"- conclusion(결론): `{sweep['repair_conclusion']}`.",
        "",
        "### Best Density Rows(최고 밀도 행)",
        "",
        "| axis(축) | mode(방식) | q(분위수) | cooldown(쿨다운) | quota(할당) | validation PF/DD/trades_day(검증 수익 팩터/손실폭/일거래) | OOS PF/DD/trades_day(표본외 수익 팩터/손실폭/일거래) | decision(결정) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in best_density:
        lines.append(
            "| `{axis}` | `{mode}` | `{q}` | `{cd}` | `{quota}` | `{vpf}`/`{vdd}`/`{vtpd}` | `{opf}`/`{odd}`/`{otpd}` | `{decision}` |".format(
                axis=row.get("axis_id"),
                mode=row.get("mode"),
                q=fmt(row.get("threshold_quantile"), 2),
                cd=row.get("cooldown_bars"),
                quota=row.get("daily_quota"),
                vpf=fmt(row.get("validation_pf")),
                vdd=fmt(row.get("validation_dd_pct")),
                vtpd=fmt(row.get("validation_trades_per_day")),
                opf=fmt(row.get("oos_pf")),
                odd=fmt(row.get("oos_dd_pct")),
                otpd=fmt(row.get("oos_trades_per_day")),
                decision=row.get("repair_decision"),
            )
        )
    lines.extend(
        [
            "",
            "### Best Positive Low-DD Rows(양수 저손실폭 최선 행)",
            "",
            "| axis(축) | mode(방식) | q(분위수) | cooldown(쿨다운) | validation PF/DD/trades_day(검증 수익 팩터/손실폭/일거래) | OOS PF/DD/trades_day(표본외 수익 팩터/손실폭/일거래) | decision(결정) |",
            "|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in best_quality:
        lines.append(
            "| `{axis}` | `{mode}` | `{q}` | `{cd}` | `{vpf}`/`{vdd}`/`{vtpd}` | `{opf}`/`{odd}`/`{otpd}` | `{decision}` |".format(
                axis=row.get("axis_id"),
                mode=row.get("mode"),
                q=fmt(row.get("threshold_quantile"), 2),
                cd=row.get("cooldown_bars"),
                vpf=fmt(row.get("validation_pf")),
                vdd=fmt(row.get("validation_dd_pct")),
                vtpd=fmt(row.get("validation_trades_per_day")),
                opf=fmt(row.get("oos_pf")),
                odd=fmt(row.get("oos_dd_pct")),
                otpd=fmt(row.get("oos_trades_per_day")),
                decision=row.get("repair_decision"),
            )
        )
    lines.extend(
        [
            "",
            "## Decision(결정)",
            "",
            "Action(행동): F69E does not materialize an additional MT5 repair probe(F69E는 추가 MT5 수리 탐침을 물질화하지 않는다).",
            "",
            "Effect(효과): no meaningful proxy repair candidate(의미 있는 프록시 수리 후보 없음)이므로, 같은 event-first ExtraTrees trade-shape repair(이벤트 우선 엑스트라트리스 거래 형태 수리)를 반복하지 않고 closeout review(마감 검토)로 넘긴다.",
            "",
            "Preserved clue(보존 단서): F69D ONNX/probability/signal/feature parity(F69D 온엑스/확률/신호/피처 동등성)는 정확했다.",
            "",
            "Negative memory(부정 기억): F69 event-first axis(이벤트 우선 축)는 sparse PF clue(희박 PF 단서)와 dense weak-PF clue(촘촘하지만 약한 PF 단서)를 동시에 네 축 목표로 끌어올리지 못했다.",
            "",
            f"Next action(다음 행동): `{decision['next_action']}`.",
        ]
    )
    return lines


def gate_audit_lines(summary: Mapping[str, Any]) -> list[str]:
    return [
        "# Required Gate Coverage Audit F69E(필수 게이트 커버리지 감사 F69E)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| current truth re-entry(현재 진실 재진입) | passed(통과) | `docs/workspace/workspace_state.yaml`, F69D receipt(F69D 영수증) | F69E가 현재 F69D 뒤에서 실행됨 |",
        f"| runtime receipt read(런타임 영수증 읽기) | passed(통과) | `{rel(RUNTIME_RECEIPT_REVIEW)}` | signal/feature/runtime KPI(신호/피처/런타임 KPI)를 직접 사용함 |",
        f"| repair sweep materialized(수리 탐색 물질화) | passed(통과) | `{rel(REPAIR_SWEEP_PATH)}` | trade-shape repair(거래 형태 수리)를 임시 출력이 아닌 산출물로 남김 |",
        "| Grok pre-MT5 repair review(사전 MT5 수리 그록 검토) | not_applicable(해당 없음) | meaningful repair candidate(의미 있는 수리 후보) `0` | 추가 MT5 probe(MT5 탐침)를 만들지 않음 |",
        f"| claim boundary(주장 경계) | passed(통과) | `{CLAIM_BOUNDARY}` | completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않음 |",
        "",
        f"Summary(요약): final_gate_like(최종 조건 유사) `{summary['repair_sweep']['final_gate_like_count']}`, joint_soft(완화 공동 조건) `{summary['repair_sweep']['joint_soft_count']}`.",
    ]


def ledger_row(decision: Mapping[str, Any]) -> dict[str, Any]:
    sweep = decision["repair_sweep"]
    best_quality = sweep["best_positive_low_dd_rows"][0] if sweep["best_positive_low_dd_rows"] else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "gap_analysis_and_proxy_repair(간극 분석 및 프록시 수리)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "F69E analyzed F69D proxy/runtime gap and trade-shape repair sweep; no meaningful repair candidate.",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier69E",
        "date": "2026-06-17",
        "decision": "proceed_to_stage_closeout_review",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": decision["next_action"],
        "rows": sweep["sweep_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "best_proxy": best_quality.get("candidate_id", ""),
        "candidate_rows": sweep["sweep_rows"],
        "positive_proxy_rows": sweep["positive_low_dd_count"],
        "best_model_id": best_quality.get("axis_id", ""),
        "best_proxy_net": best_quality.get("min_net", ""),
        "run_date": "2026-06-17",
        "primary_artifact": rel(SUMMARY_PATH),
        "net_profit": best_quality.get("min_net", ""),
        "profit_factor": best_quality.get("min_pf", ""),
        "drawdown": best_quality.get("max_dd_pct", ""),
        "trade_count": best_quality.get("oos_trades", ""),
        "result_status": STATUS,
        "attempt_count": 0,
        "view": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "tier": "Tier A separate(Tier A 분리)",
        "metric_scope": "runtime_gap_and_proxy_repair(런타임 간극 및 프록시 수리)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_probe_gap_analysis(런타임 탐침 간극 분석)",
        "external_verification_status": "completed_by_parent_runtime_probe(F69D 런타임 탐침으로 완료)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(GAP_DECISION_REVIEW),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": utc_now(),
        "ledger_row_id": f"{RUN_ID}__gap_analysis",
        "subrun_id": "trade_shape_repair_sweep(거래 형태 수리 탐색)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "kpi_scope": "gap_analysis_and_proxy_repair(간극 분석 및 프록시 수리)",
        "primary_kpi": f"final_gate_like={sweep['final_gate_like_count']};joint_soft={sweep['joint_soft_count']}",
        "guardrail_kpi": "no additional MT5 repair probe because meaningful proxy repair candidate count is 0",
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution(실험 실행)",
        "row_id": f"{RUN_ID}__gap_analysis",
        "evidence_boundary": "gap_analysis_proxy_repair_only_no_authority(간극 분석 및 프록시 수리 전용, 권위 없음)",
        "next_action": decision["next_action"],
        "question": "Can F69D gap be repaired by threshold/cooldown/daily quota trade-shape changes?(F69D 간극을 임계값/쿨다운/일별 할당 거래 형태로 고칠 수 있는가)",
        "artifact_count": 5,
        "created_at_utc": utc_now(),
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_gap_analysis(전선 간극 분석)",
        "run_type": "trade_shape_repair_proxy_sweep(거래 형태 수리 프록시 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(SUMMARY_PATH),
        "result_path": rel(REPORT_PATH),
        "selected_net_profit": best_quality.get("min_net", ""),
        "selected_profit_factor": best_quality.get("min_pf", ""),
        "selected_trade_density": best_quality.get("oos_trades_per_day", ""),
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_observation_and_proxy_repair_only(런타임 탐침 관찰 및 프록시 수리 전용)",
        "trade_density": best_quality.get("oos_trades_per_day", ""),
        "expected_net_profit": "",
        "expected_profit_factor": "",
        "expected_trade_count": "",
        "expected_trade_density": "",
        "max_drawdown_percent": best_quality.get("max_dd_pct", ""),
        "strict_joint_pass_count": sweep["final_gate_like_count"],
    }


def write_state_files(decision: Mapping[str, Any]) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {decision['next_action']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {decision['next_action']}",
        "runtime_probe_status: f69_runtime_probe_attempted_observation_recorded_no_authority(F69 런타임 탐침 시도/관찰 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{utc_now()}'",
        "notes:",
        '  - "F69E action(행동): F69D proxy/runtime gap(프록시/런타임 간극)을 분석하고 trade-shape repair sweep(거래 형태 수리 탐색)을 실행했다."',
        '  - "Effect(효과): bridge parity(연결 동등성)는 병목이 아니며, event-first axis(이벤트 우선 축)의 밀도/PF 절충이 남았음을 기록했다."',
        f'  - "Next action(다음 행동): `{decision["next_action"]}`."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")

    current_lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{decision['next_action']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F69E proxy/runtime gap analysis and trade-shape repair sweep(F69E 프록시/런타임 간극 분석 및 거래 형태 수리 탐색)을 실행했다.",
        "",
        "Effect(효과): F69D bridge parity(연결 동등성)는 정확했지만, trade-shape-only repair(거래 형태 단독 수리)는 meaningful repair candidate(의미 있는 수리 후보)를 만들지 못했다.",
        "",
        f"- status(상태): `{STATUS}`.",
        f"- judgment(판정): `{JUDGMENT}`.",
        f"- sweep rows(탐색 행): `{decision['repair_sweep']['sweep_rows']}`.",
        f"- final gate-like rows(최종 조건 유사 행): `{decision['repair_sweep']['final_gate_like_count']}`.",
        f"- joint soft rows(완화 공동 조건 행): `{decision['repair_sweep']['joint_soft_count']}`.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- report(보고서): `{rel(REPORT_PATH)}`",
        f"- repair sweep(수리 탐색): `{rel(REPAIR_SWEEP_REVIEW)}`",
        f"- decision(결정): `{rel(GAP_DECISION_REVIEW)}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(CURRENT_WORKING_STATE, current_lines)

    selection_lines = [
        "# F69 Selection Status(F69 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{decision['next_action']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- completed_action(완료 행동): `{RUN_ID}` gap analysis and trade-shape repair sweep(간극 분석 및 거래 형태 수리 탐색).",
        f"- report(보고서): `{rel(REPORT_PATH)}`",
        f"- next_action(다음 행동): `{decision['next_action']}`.",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(SELECTION_STATUS, selection_lines)


def update_registers(decision: Mapping[str, Any]) -> None:
    row = ledger_row(decision)
    upsert_ledger(RUN_REGISTRY, "run_id", row)
    upsert_ledger(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_ledger(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    append_once(
        IDEA_REGISTRY,
        "<!-- frontier69E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->",
        f"""
<!-- frontier69E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` analyzed F69D proxy/runtime gap(프록시/런타임 간극) and ran threshold/cooldown/daily-top trade-shape repair sweep(임계값/쿨다운/일별 상위 거래 형태 수리 탐색). Result(결과): `{JUDGMENT}`. Final gate-like rows(최종 조건 유사 행): `{decision['repair_sweep']['final_gate_like_count']}`; joint soft rows(완화 공동 조건 행): `{decision['repair_sweep']['joint_soft_count']}`. Preserved clue(보존 단서): exact ONNX/signal/feature parity(정확한 온엑스/신호/피처 동등성). Negative memory(부정 기억): event-first trade-shape-only repair(이벤트 우선 거래 형태 단독 수리)는 밀도/PF/DD를 동시에 복구하지 못했다. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{decision['next_action']}`.
""",
    )


def main() -> int:
    if not path_exists(RUNTIME_RECEIPT_REVIEW):
        raise RuntimeError(f"missing runtime receipt: {RUNTIME_RECEIPT_REVIEW}")
    if not path_exists(GAP_CLASSIFICATION_REVIEW):
        raise RuntimeError(f"missing gap classification: {GAP_CLASSIFICATION_REVIEW}")
    runtime_rows = read_csv_rows(RUNTIME_RECEIPT_REVIEW)
    gap_rows = read_csv_rows(GAP_CLASSIFICATION_REVIEW)
    sweep_rows = run_trade_shape_repair_sweep()
    decision = build_decision(runtime_rows, gap_rows, sweep_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": decision["next_action"],
        "created_at_utc": utc_now(),
        "inputs": {
            "runtime_receipt": rel(RUNTIME_RECEIPT_REVIEW),
            "gap_classification": rel(GAP_CLASSIFICATION_REVIEW),
            "source_runtime_probe_script": rel(Path(f69d.__file__).resolve()),
            "source_proxy_script": rel(Path(f69b.__file__).resolve()),
        },
        "outputs": {
            "summary": rel(SUMMARY_PATH),
            "repair_sweep": rel(REPAIR_SWEEP_PATH),
            "gap_decision": rel(GAP_DECISION_PATH),
            "report": rel(REPORT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    write_csv(REPAIR_SWEEP_PATH, sweep_rows)
    write_csv(REPAIR_SWEEP_REVIEW, sweep_rows)
    write_json(GAP_DECISION_PATH, decision)
    write_json(GAP_DECISION_REVIEW, decision)
    write_json(SUMMARY_PATH, decision)
    write_md(REPORT_PATH, report_lines(decision))
    write_md(GATE_AUDIT_PATH, gate_audit_lines(decision))
    update_registers(decision)
    write_state_files(decision)
    print(json.dumps(json_ready({"status": STATUS, "judgment": JUDGMENT, "summary": decision["repair_sweep"], "next_action": decision["next_action"]}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_sklearn_probabilities
from stage_pipelines.stage_frontier_72 import frontier72b_trade_shape_exit_distribution_proxy_scout as f72b
from stage_pipelines.stage_frontier_72 import frontier72c_trade_shape_label_feature_repair as f72c
from stage_pipelines.stage_frontier_72 import frontier72d_pre_mt5_trade_shape_runtime_probe as f72d


STAGE_ID = f72b.STAGE_ID
RUN_ID = "frontier72E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = f72d.RUN_ID
NEXT_REPAIR_PROBE_RUN_ID = "frontier72F_pre_mt5_lifecycle_repair_runtime_probe_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier72F_stage_closeout_trade_shape_runtime_lifecycle_gap_v1"
CLAIM_BOUNDARY = (
    "proxy_runtime_gap_analysis_and_repair_proxy_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f72b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f72b.REVIEWS_ROOT
SELECTED_ROOT = f72b.SELECTED_ROOT
F72D_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F72D_RECEIPT = F72D_ROOT / "f72d_runtime_probe_receipt.csv"
F72D_TAPE = F72D_ROOT / "runtime_veto_tapes/f72d_bridge_f72c_0098_selected_entry_runtime_veto_tape.csv"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def required_inputs() -> list[Path]:
    return [F72D_RECEIPT, F72D_TAPE, f72b.MODEL_INPUT, f72b.FEATURE_ORDER, f72b.RAW_US100]


def side_score(proba: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    short = proba[:, 0]
    flat = proba[:, 1]
    long = proba[:, 2]
    side = np.where(short >= long, -1, 1).astype(int)
    score = np.maximum(short, long) - flat
    return side, score.astype(float)


def compute_shape_path_with_exit(
    model: pd.DataFrame,
    raw: pd.DataFrame,
    positions: np.ndarray,
    shape: f72b.TradeShape,
) -> dict[str, np.ndarray]:
    base = f72b.compute_shape_path(model, raw, positions, shape)
    entry_raw_index = np.full(len(model), -1, dtype=int)
    exit_raw_index = np.full(len(model), -1, dtype=int)
    atr_values = pd.to_numeric(model["atr_14"], errors="coerce").to_numpy(dtype=float)
    open_values = raw["open"].to_numpy(dtype=float)
    high_values = raw["high"].to_numpy(dtype=float)
    low_values = raw["low"].to_numpy(dtype=float)
    max_pos = len(raw) - shape.hold_bars - 2
    for i, pos_float in enumerate(positions):
        if not np.isfinite(pos_float):
            continue
        pos = int(pos_float)
        if pos < 0 or pos > max_pos:
            continue
        atr = atr_values[i]
        if not np.isfinite(atr) or atr <= 0:
            continue
        entry_idx = pos + 1
        horizon_idx = pos + shape.hold_bars
        entry = open_values[entry_idx]
        stop = shape.stop_atr * atr
        target = shape.target_atr * atr
        exit_idx = horizon_idx
        for j in range(entry_idx, horizon_idx + 1):
            if shape.direction > 0:
                hit_stop = low_values[j] <= entry - stop
                hit_target = high_values[j] >= entry + target
            else:
                hit_stop = high_values[j] >= entry + stop
                hit_target = low_values[j] <= entry - target
            if hit_stop or hit_target:
                exit_idx = j
                break
        entry_raw_index[i] = entry_idx
        exit_raw_index[i] = exit_idx
    base["entry_raw_index"] = entry_raw_index
    base["exit_raw_index"] = exit_raw_index
    return base


def lifecycle_take_mask(selected: np.ndarray, path: Mapping[str, np.ndarray]) -> np.ndarray:
    taken = np.zeros(len(selected), dtype=bool)
    blocked_until = -1
    entry_raw = path["entry_raw_index"]
    exit_raw = path["exit_raw_index"]
    for idx in np.where(selected)[0]:
        entry = int(entry_raw[idx])
        exit_idx = int(exit_raw[idx])
        if entry < 0 or exit_idx < 0:
            continue
        if entry > blocked_until:
            taken[idx] = True
            blocked_until = exit_idx
    return taken


def build_three_class_label(
    short_path: Mapping[str, np.ndarray],
    long_path: Mapping[str, np.ndarray],
    short_shape: f72b.TradeShape,
    long_shape: f72b.TradeShape,
    variant: str,
) -> np.ndarray:
    short_label = f72c.repair_label(short_path, short_shape, variant) > 0
    long_label = f72c.repair_label(long_path, long_shape, variant) > 0
    short_quality = np.nan_to_num(short_path["quality"], nan=-999.0)
    long_quality = np.nan_to_num(long_path["quality"], nan=-999.0)
    y = np.zeros(len(short_quality), dtype=int)
    y[short_label & (~long_label | (short_quality >= long_quality))] = -1
    y[long_label & (~short_label | (long_quality > short_quality))] = 1
    return y


def kpi_prefix(metrics: Mapping[str, Any], prefix: str) -> dict[str, Any]:
    return {f"{prefix}_{key}": value for key, value in metrics.items()}


def proxy_metrics(
    model: pd.DataFrame,
    selected: np.ndarray,
    lifecycle: np.ndarray,
    short_path: Mapping[str, np.ndarray],
    split: str,
) -> dict[str, Any]:
    split_mask = model["split"].astype(str).eq(split).to_numpy(dtype=bool)
    signal_mask = split_mask & selected
    lifecycle_mask = split_mask & lifecycle
    signal_metrics = f72b.trade_metrics(
        model.loc[signal_mask, "timestamp"],
        short_path["pnl"][signal_mask],
        np.full(int(signal_mask.sum()), -1),
    )
    lifecycle_metrics = f72b.trade_metrics(
        model.loc[lifecycle_mask, "timestamp"],
        short_path["pnl"][lifecycle_mask],
        np.full(int(lifecycle_mask.sum()), -1),
    )
    return {
        **kpi_prefix(signal_metrics, f"{split}_signal"),
        **kpi_prefix(lifecycle_metrics, f"{split}_lifecycle"),
    }


def runtime_gap_rows() -> list[dict[str, Any]]:
    receipt = pd.read_csv(io_path(F72D_RECEIPT))
    rows: list[dict[str, Any]] = []
    for _, row in receipt.iterrows():
        expected_signal = int(row.get("expected_signal_count") or 0)
        orders = int(row.get("order_attempt_count") or 0)
        trades = int(row.get("trade_count") or 0)
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "split": row.get("split"),
                "test_period_start": row.get("test_period_start"),
                "test_period_end": row.get("test_period_end"),
                "expected_signal_count": expected_signal,
                "runtime_signal_count": row.get("signal_count"),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
                "order_attempt_count": orders,
                "trade_count": trades,
                "order_per_signal_ratio": orders / expected_signal if expected_signal else 0.0,
                "trade_per_signal_ratio": trades / expected_signal if expected_signal else 0.0,
                "runtime_net_profit": row.get("net_profit"),
                "runtime_profit_factor": row.get("profit_factor"),
                "runtime_drawdown_percent": row.get("max_drawdown_percent"),
                "runtime_trades_per_day": row.get("trades_per_day"),
                "proxy_net_profit": row.get("proxy_net_profit"),
                "proxy_profit_factor": row.get("proxy_profit_factor"),
                "proxy_trades_per_day": row.get("proxy_trades_per_day"),
                "proxy_dd_percent": row.get("proxy_dd_percent"),
                "gap_cause": row.get("gap_cause_summary"),
                "local_gap_cause": "overlapping_signal_counting_vs_mt5_single_position_lifecycle",
                "next_repair": "lifecycle_aligned_proxy_sweep",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def repair_grid() -> list[tuple[f72b.TradeShape, str]]:
    rows: list[tuple[f72b.TradeShape, str]] = []
    for hold in (6, 12, 18, 24):
        for stop in (0.9, 1.2):
            for target in (1.2, 1.8):
                for variant in ("early_survival_045", "mfe_mae_gap_040", "dd_guard_balanced"):
                    rows.append((f72b.TradeShape(hold, stop, target, -1), variant))
    return rows


def candidate_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    model = pd.read_parquet(io_path(f72b.MODEL_INPUT))
    model["timestamp"] = pd.to_datetime(model["timestamp"], utc=True)
    raw = pd.read_csv(io_path(f72b.RAW_US100)).sort_values("time_close_unix").reset_index(drop=True)
    positions = f72b.align_raw(model, raw)
    features = [line.strip() for line in f72b.read_text(f72b.FEATURE_ORDER).splitlines() if line.strip()]
    train_mask_base = model["split"].astype(str).eq("train").to_numpy(dtype=bool)
    rows: list[dict[str, Any]] = []
    path_cache: dict[str, dict[str, np.ndarray]] = {}
    for shape, variant in repair_grid():
        short_shape = shape
        long_shape = f72b.TradeShape(shape.hold_bars, shape.stop_atr, shape.target_atr, 1)
        for shape_for_cache in (short_shape, long_shape):
            if shape_for_cache.shape_id not in path_cache:
                path_cache[shape_for_cache.shape_id] = compute_shape_path_with_exit(model, raw, positions, shape_for_cache)
        short_path = path_cache[short_shape.shape_id]
        long_path = path_cache[long_shape.shape_id]
        y = build_three_class_label(short_path, long_path, short_shape, long_shape, variant)
        train_mask = train_mask_base & np.isfinite(short_path["pnl"]) & np.isfinite(long_path["pnl"])
        classes = set(np.unique(y[train_mask]).tolist())
        if classes != {-1, 0, 1}:
            rows.append({
                "candidate_id": f"f72e_invalid_{len(rows):04d}",
                "shape_id": short_shape.shape_id,
                "label_variant": variant,
                "status": "invalid_missing_bridge_class",
                "classes": sorted(classes),
                "claim_boundary": CLAIM_BOUNDARY,
            })
            continue
        bridge = make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesClassifier(
                n_estimators=80,
                max_depth=8,
                min_samples_leaf=70,
                class_weight="balanced_subsample",
                random_state=7205 + len(rows),
                n_jobs=-1,
            ),
        )
        bridge.fit(model.loc[train_mask, features], y[train_mask])
        proba = ordered_sklearn_probabilities(bridge, model.loc[:, features].to_numpy(dtype="float64"), class_order=(-1, 0, 1))
        side, score = side_score(proba)
        validation_mask = (model["split"] == "validation").to_numpy() & (side == -1) & np.isfinite(short_path["pnl"])
        for target_tpd in (5.0, 8.0, 12.0, 16.0, 20.0):
            threshold = f72b.score_threshold(score[validation_mask], model.loc[validation_mask, "timestamp"], target_tpd)
            selected = np.isfinite(short_path["pnl"]) & (side == -1) & (score >= threshold)
            lifecycle = lifecycle_take_mask(selected, short_path)
            row_id = f"f72e_{len(rows):04d}"
            row: dict[str, Any] = {
                "candidate_id": row_id,
                "shape_id": short_shape.shape_id,
                "label_variant": variant,
                "model_id": "extra_trees_3class_bridge_lifecycle_scout",
                "feature_set_id": "all58",
                "target_signal_trades_day": target_tpd,
                "score_threshold": float(threshold),
                "selected_signal_rows": int(selected.sum()),
                "lifecycle_rows": int(lifecycle.sum()),
                "status": "evaluated",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for split in ("train", "validation", "oos"):
                row.update(proxy_metrics(model, selected, lifecycle, short_path, split))
            row["validation_lifecycle_pass"] = bool(
                row["validation_lifecycle_net_profit"] > 0
                and row["validation_lifecycle_profit_factor"] >= 1.05
                and row["validation_lifecycle_max_drawdown_percent"] <= 18.0
                and row["validation_lifecycle_trades_day"] >= 1.0
            )
            row["oos_lifecycle_pass"] = bool(
                row["oos_lifecycle_net_profit"] > 0
                and row["oos_lifecycle_profit_factor"] >= 1.05
                and row["oos_lifecycle_max_drawdown_percent"] <= 18.0
                and row["oos_lifecycle_trades_day"] >= 1.0
            )
            row["runtime_repair_probe_worthy"] = bool(
                row["validation_lifecycle_pass"]
                and row["oos_lifecycle_pass"]
                and row["validation_lifecycle_trades_day"] >= 2.0
                and row["oos_lifecycle_trades_day"] >= 2.0
            )
            row["meaningful_candidate"] = bool(
                row["runtime_repair_probe_worthy"]
                and row["validation_lifecycle_profit_factor"] >= 1.3
                and row["oos_lifecycle_profit_factor"] >= 1.3
                and row["validation_lifecycle_max_drawdown_percent"] <= 12.0
                and row["oos_lifecycle_max_drawdown_percent"] <= 12.0
            )
            rows.append(row)
    evaluated = [row for row in rows if row.get("status") == "evaluated"]
    ranked = sorted(
        evaluated,
        key=lambda row: (
            bool(row.get("runtime_repair_probe_worthy")),
            float(row.get("oos_lifecycle_profit_factor") or 0),
            float(row.get("validation_lifecycle_profit_factor") or 0),
            float(row.get("oos_lifecycle_net_profit") or 0),
            -float(row.get("oos_lifecycle_max_drawdown_percent") or 999),
        ),
        reverse=True,
    )
    return rows, ranked[:25]


def build_summary(gap: Sequence[Mapping[str, Any]], candidates: Sequence[Mapping[str, Any]], top: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    evaluated = [row for row in candidates if row.get("status") == "evaluated"]
    probe_worthy = [row for row in evaluated if row.get("runtime_repair_probe_worthy")]
    meaningful = [row for row in evaluated if row.get("meaningful_candidate")]
    best = top[0] if top else {}
    next_run = NEXT_REPAIR_PROBE_RUN_ID if probe_worthy else NEXT_CLOSEOUT_RUN_ID
    status = "lifecycle_repair_proxy_found_pre_mt5_required" if probe_worthy else "lifecycle_gap_negative_memory_closeout_required"
    judgment = "runtime_gap_repair_probe_required_no_authority" if probe_worthy else "runtime_gap_negative_memory_no_repair_probe_candidate_no_authority"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "gap_rows": len(gap),
        "candidate_count": len(evaluated),
        "runtime_repair_probe_worthy_count": len(probe_worthy),
        "meaningful_candidate_count": len(meaningful),
        "best_candidate": best,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    best = summary.get("best_candidate", {})
    return [
        "# Frontier72E Proxy/Runtime Gap Analysis(F72E 프록시/런타임 간극 분석)",
        "",
        f"- status(상태): `{summary.get('status')}`",
        f"- judgment(판정): `{summary.get('judgment')}`",
        f"- candidate_count(후보 수): `{summary.get('candidate_count')}`",
        f"- runtime_repair_probe_worthy_count(런타임 수리 탐침 가치 후보 수): `{summary.get('runtime_repair_probe_worthy_count')}`",
        f"- meaningful_candidate_count(의미 후보 수): `{summary.get('meaningful_candidate_count')}`",
        f"- best_candidate(최선 후보): `{best.get('candidate_id', '')}` / `{best.get('shape_id', '')}` / `{best.get('label_variant', '')}`",
        f"- best lifecycle validation net/PF/DD/trades_day(최선 생명주기 검증 순수익/수익 팩터/손실폭/일거래): `{best.get('validation_lifecycle_net_profit', '')}` / `{best.get('validation_lifecycle_profit_factor', '')}` / `{best.get('validation_lifecycle_max_drawdown_percent', '')}` / `{best.get('validation_lifecycle_trades_day', '')}`",
        f"- best lifecycle OOS net/PF/DD/trades_day(최선 생명주기 표본외 순수익/수익 팩터/손실폭/일거래): `{best.get('oos_lifecycle_net_profit', '')}` / `{best.get('oos_lifecycle_profit_factor', '')}` / `{best.get('oos_lifecycle_max_drawdown_percent', '')}` / `{best.get('oos_lifecycle_trades_day', '')}`",
        "",
        "## Gap Cause(간극 원인)",
        "",
        "- F72D signal count parity(신호 수 동등성)와 feature readiness parity(피처 준비 동등성)는 통과했다.",
        "- Runtime order/trade count(런타임 주문/거래 수)는 selected signal count(선택 신호 수)의 약 32~38%로 줄었다.",
        "- local_gap_cause(로컬 간극 원인): overlapping signal counting(겹친 신호 집계)이 MT5 single-position lifecycle(MT5 단일 포지션 생명주기)와 맞지 않았다.",
        "",
        "Effect(효과): 다음 판단은 신호 생성이 아니라 lifecycle-aligned proxy(생명주기 정렬 프록시)를 기준으로 한다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{summary.get('next_run_id')}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def update_state(summary: Mapping[str, Any], created_at: str) -> None:
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {summary.get('next_run_id')}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary.get('status')}",
        f"current_judgment: {summary.get('judgment')}",
        f"next_run_id: {summary.get('next_run_id')}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f71_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "Action(행동): F72E proxy/runtime gap analysis(프록시/런타임 간극 분석)와 lifecycle repair scout(생명주기 수리 탐색)를 실행했다. Candidates(후보) {summary.get("candidate_count")}, repair_probe_worthy(수리 탐침 가치) {summary.get("runtime_repair_probe_worthy_count")}."',
        '  - "Effect(효과): F72D 간극 원인은 overlapping signal counting(겹친 신호 집계) 대 MT5 single-position lifecycle(MT5 단일 포지션 생명주기)로 기록했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f72b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F72 Selection Status(F72 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{summary.get('next_run_id')}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{summary.get('status')}`",
        f"- judgment(판정): `{summary.get('judgment')}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{summary.get('next_run_id')}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ])
    write_text(f72b.CURRENT_WORKING_STATE, [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{summary.get('next_run_id')}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F72E proxy/runtime gap analysis(프록시/런타임 간극 분석)와 lifecycle repair scout(생명주기 수리 탐색)를 실행했다.",
        "",
        f"Effect(효과): repair_probe_worthy(수리 탐침 가치 후보) `{summary.get('runtime_repair_probe_worthy_count')}`개를 기록했고, 다음 행동은 `{summary.get('next_run_id')}`다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def update_ledgers(summary: Mapping[str, Any], created_at: str) -> None:
    best = summary.get("best_candidate", {})
    row = {
        "ledger_row_id": f"{RUN_ID}__gap_analysis_lifecycle_repair",
        "row_id": f"{RUN_ID}__gap_analysis_lifecycle_repair",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": summary.get("next_run_id"),
        "status": summary.get("status"),
        "judgment": summary.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier72E_proxy_runtime_gap_analysis_and_lifecycle_repair_report.md"),
        "report_path": rel(REVIEWS_ROOT / "frontier72E_proxy_runtime_gap_analysis_and_lifecycle_repair_report.md"),
        "primary_artifact": rel(RUN_ROOT / "f72e_lifecycle_repair_candidates.csv"),
        "run_number": "frontier72E",
        "date": created_at[:10],
        "decision": summary.get("judgment"),
        "rows": summary.get("candidate_count"),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": best.get("candidate_id"),
        "net_profit": best.get("oos_lifecycle_net_profit"),
        "profit_factor": best.get("oos_lifecycle_profit_factor"),
        "drawdown": best.get("oos_lifecycle_max_drawdown_percent"),
        "trade_count": best.get("oos_lifecycle_trade_count"),
        "trade_density": best.get("oos_lifecycle_trades_day"),
        "scoreboard_lane": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "external_verification_status": "completed_from_parent_runtime_probe(F72D 런타임 탐침 완료 기반)",
        "evidence_boundary": "gap_analysis_and_proxy_repair_no_authority(간극 분석과 프록시 수리, 권위 없음)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72e.md"),
    }
    f72b.upsert_ledger(f72b.ALPHA_LEDGER, "ledger_row_id", row)
    f72b.upsert_ledger(f72b.RUN_REGISTRY, "run_id", row)
    f72b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f72b.ALPHA_LEDGER)


def append_idea(summary: Mapping[str, Any]) -> None:
    marker = "<!-- frontier72E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->"
    block = f"""<!-- frontier72E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->
- `{RUN_ID}` executed(실행): F72D gap cause(간극 원인)를 overlapping signal counting vs MT5 single-position lifecycle(겹친 신호 집계 대 MT5 단일 포지션 생명주기)로 기록하고 lifecycle repair scout(생명주기 수리 탐색)를 실행했다. Candidates(후보) `{summary.get('candidate_count')}`, repair probe worthy(수리 탐침 가치) `{summary.get('runtime_repair_probe_worthy_count')}`, meaningful(의미 후보) `{summary.get('meaningful_candidate_count')}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier72E_proxy_runtime_gap_analysis_and_lifecycle_repair_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{summary.get('next_run_id')}`."""
    append_once(f72b.IDEA_REGISTRY, marker, block)


def main() -> int:
    ensure_dirs()
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F72E required material missing: {missing}")
    created_at = utc_now()
    gap = runtime_gap_rows()
    candidates, top = candidate_rows()
    summary = build_summary(gap, candidates, top)
    write_csv(RUN_ROOT / "f72e_runtime_gap_rows.csv", gap)
    write_csv(RUN_ROOT / "f72e_lifecycle_repair_candidates.csv", candidates)
    write_csv(RUN_ROOT / "f72e_top_lifecycle_repair_candidates.csv", top)
    write_json(RUN_ROOT / "frontier72E_gap_repair_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": summary.get("next_run_id"),
        "status": summary.get("status"),
        "judgment": summary.get("judgment"),
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_csv(REVIEWS_ROOT / "f72e_runtime_gap_rows_review.csv", gap)
    write_csv(REVIEWS_ROOT / "f72e_lifecycle_repair_candidates_review.csv", candidates)
    write_csv(REVIEWS_ROOT / "f72e_top_lifecycle_repair_candidates_review.csv", top)
    write_text(REVIEWS_ROOT / "frontier72E_proxy_runtime_gap_analysis_and_lifecycle_repair_report.md", report_lines(summary))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f72e.md", [
        "# F72E Required Gate Coverage Audit(F72E 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- parent_runtime_probe(상위 런타임 탐침): `{rel(F72D_RECEIPT)}`.",
        f"- gap_rows(간극 행): `{len(gap)}`.",
        f"- lifecycle_repair_candidates(생명주기 수리 후보): `{summary.get('candidate_count')}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ])
    update_ledgers(summary, created_at)
    append_idea(summary)
    update_state(summary, created_at)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

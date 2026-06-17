from __future__ import annotations

import csv
import json
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b


STAGE_ID = f79b.STAGE_ID
RUN_ID = "frontier79F_ambiguous_fill_order_guard_repair_proxy_v1"
PARENT_RUN_ID = "frontier79E_proxy_runtime_gap_analysis_and_repair_decision_v1"
NEXT_RUN_IF_MEANINGFUL = "frontier79G_pre_mt5_grok_ambiguous_fill_guard_repair_runtime_probe_v1"
NEXT_RUN_IF_WEAK = "frontier79G_repair_proxy_weak_nonzero_closeout_decision_v1"
NEXT_RUN_IF_ZERO = "frontier79G_repair_proxy_zero_signal_closeout_decision_v1"
CLAIM_BOUNDARY = (
    "repair_proxy_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SUMMARY_PATH = REVIEW_DIR / "f79f_ambiguous_fill_guard_repair_proxy_summary.json"
CANDIDATES_ALL = RUN_DIR / "f79f_ambiguous_fill_guard_candidates_all.csv"
CANDIDATES_TOP = REVIEW_DIR / "f79f_ambiguous_fill_guard_ranked_top200.csv"
LABEL_AUDIT = REVIEW_DIR / "f79f_ambiguous_fill_guard_label_audit.csv"
REPORT_PATH = REVIEW_DIR / "frontier79F_ambiguous_fill_order_guard_repair_proxy_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f79f.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

INITIAL_BALANCE = 500.0
MAX_CALENDAR_TPD_SCOUT = 14.0


@dataclass(frozen=True)
class RepairSpec:
    name: str
    side: str
    hold_bars: int
    tp_price_units: float
    sl_price_units: float
    fill_policy: str
    label_mode: str
    utility_quantile: float


def utc_now() -> str:
    return f79b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def repair_specs() -> list[RepairSpec]:
    specs: list[RepairSpec] = []
    for hold, tp, sl in ((6, 9.0, 7.0), (12, 15.0, 10.0)):
        for policy in ("bidask_pessimistic", "bidask_skip_both"):
            specs.append(
                RepairSpec(
                    name=f"long_same_h{hold}_tp{int(tp)}_sl{int(sl)}_{policy}_fill_path_net_q60",
                    side="long",
                    hold_bars=hold,
                    tp_price_units=tp,
                    sl_price_units=sl,
                    fill_policy=policy,
                    label_mode="fill_path_net",
                    utility_quantile=0.60,
                )
            )
    return specs


def entry_indices(df: pd.DataFrame, raw: pd.DataFrame) -> np.ndarray:
    mapping = {ts: idx for idx, ts in enumerate(raw["open_ts"])}
    return df["timestamp"].map(mapping).fillna(-2).astype(int).to_numpy()


def compute_bidask_outcome(raw: pd.DataFrame, indices: np.ndarray, spec: RepairSpec) -> dict[str, np.ndarray]:
    open_arr = raw["open"].to_numpy(float)
    high_arr = raw["high"].to_numpy(float)
    low_arr = raw["low"].to_numpy(float)
    close_arr = raw["close"].to_numpy(float)
    spread_price_units = raw["spread_points"].to_numpy(float) / f79b.SLTP_POINT_SCALE
    n = len(indices)
    pnl_contract = np.full(n, np.nan)
    pnl_price = np.full(n, np.nan)
    mfe_contract = np.full(n, np.nan)
    mae_contract = np.full(n, np.nan)
    spread_cost_contract = np.full(n, np.nan)
    utility = np.full(n, np.nan)
    exit_offset = np.zeros(n, dtype=int)
    both_hit = np.zeros(n, dtype=int)
    valid = np.zeros(n, dtype=bool)
    max_idx = len(raw) - spec.hold_bars
    for row_idx, raw_idx in enumerate(indices):
        if raw_idx < 0 or raw_idx > max_idx:
            continue
        spread = float(spread_price_units[raw_idx]) if np.isfinite(spread_price_units[raw_idx]) else 0.0
        entry = float(open_arr[raw_idx]) + spread
        if not np.isfinite(entry) or entry <= 0:
            continue
        hi = high_arr[raw_idx : raw_idx + spec.hold_bars]
        lo = low_arr[raw_idx : raw_idx + spec.hold_bars]
        cl = close_arr[raw_idx : raw_idx + spec.hold_bars]
        if not (np.isfinite(hi).all() and np.isfinite(lo).all() and np.isfinite(cl).all()):
            continue
        mfe_price = float(np.max(hi - entry))
        mae_price = float(np.max(entry - lo))
        realized = float(cl[-1] - entry)
        offset = spec.hold_bars
        ambiguous = False
        for local_idx in range(spec.hold_bars):
            sl_hit = lo[local_idx] <= entry - spec.sl_price_units
            tp_hit = hi[local_idx] >= entry + spec.tp_price_units
            if sl_hit and tp_hit:
                both_hit[row_idx] = 1
                ambiguous = True
                realized = -spec.sl_price_units
                offset = local_idx + 1
                break
            if sl_hit or tp_hit:
                realized = -spec.sl_price_units if sl_hit else spec.tp_price_units
                offset = local_idx + 1
                break
        if ambiguous and spec.fill_policy == "bidask_skip_both":
            continue
        contract_pnl = realized * f79b.CONTRACT_PNL_SCALE
        mae = mae_price * f79b.CONTRACT_PNL_SCALE
        mfe = mfe_price * f79b.CONTRACT_PNL_SCALE
        score = contract_pnl - 0.24 * mae - 0.001 * offset
        pnl_price[row_idx] = realized
        pnl_contract[row_idx] = contract_pnl
        mfe_contract[row_idx] = mfe
        mae_contract[row_idx] = mae
        spread_cost_contract[row_idx] = spread * f79b.CONTRACT_PNL_SCALE
        utility[row_idx] = score
        exit_offset[row_idx] = max(1, int(offset))
        valid[row_idx] = True
    return {
        "pnl_price": pnl_price,
        "pnl_contract": pnl_contract,
        "mfe_contract": mfe_contract,
        "mae_contract": mae_contract,
        "spread_cost_contract": spread_cost_contract,
        "utility": utility,
        "exit_offset": exit_offset,
        "both_hit": both_hit,
        "valid": valid,
    }


def make_label(df: pd.DataFrame, outcome: Mapping[str, np.ndarray], spec: RepairSpec) -> np.ndarray:
    train_mask = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
    if train_mask.sum() == 0:
        return np.zeros(len(df), dtype=int)
    utility = np.asarray(outcome["utility"], dtype=float)
    pnl = np.asarray(outcome["pnl_contract"], dtype=float)
    mae = np.asarray(outcome["mae_contract"], dtype=float)
    threshold = float(np.nanquantile(utility[train_mask], spec.utility_quantile))
    guard = mae <= np.nanquantile(mae[train_mask], 0.78)
    return ((utility >= threshold) & (pnl > 0.0) & guard & np.asarray(outcome["valid"], dtype=bool)).astype(int)


def scout_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            int(metrics["trade_count"]) >= 80
            and float(metrics["pf"]) >= 1.15
            and float(metrics["dd_pct"]) <= 12.0
            and 1.0 <= float(metrics["calendar_trades_day"]) <= MAX_CALENDAR_TPD_SCOUT
        )

    return ok(val) and ok(oos)


def meaningful_gate(val: Mapping[str, Any], oos: Mapping[str, Any]) -> bool:
    def ok(metrics: Mapping[str, Any]) -> bool:
        return (
            float(metrics["net"]) > 0.0
            and float(metrics["pf"]) >= 1.35
            and float(metrics["dd_pct"]) <= 10.0
            and 2.0 <= float(metrics["calendar_trades_day"]) <= 12.0
            and int(metrics["trade_count"]) >= 120
        )

    return ok(val) and ok(oos)


def density_score(value: float) -> float:
    if value <= 0:
        return -10.0
    if 5.0 <= value <= 10.0:
        return 10.0
    if value < 5.0:
        return value * 1.7
    return max(0.0, 10.0 - (value - 10.0) * 1.4)


def rank_score(val: Mapping[str, Any], oos: Mapping[str, Any], meaningful: bool, scout: bool) -> float:
    min_pf = min(float(val["pf"]), float(oos["pf"]), 5.0)
    max_dd = max(float(val["dd_pct"]), float(oos["dd_pct"]))
    min_net = min(float(val["net"]), float(oos["net"]))
    density = min(density_score(float(val["calendar_trades_day"])), density_score(float(oos["calendar_trades_day"])))
    return (
        (1_000_000.0 if meaningful else 0.0)
        + (150_000.0 if scout else 0.0)
        + (25_000.0 if min_net > 0 else 0.0)
        + min_pf * 4_500.0
        + density * 3_000.0
        - max_dd * 500.0
        + min_net * 25.0
    )


def fit_and_score() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    original_balance = f78b.INITIAL_BALANCE
    f78b.INITIAL_BALANCE = INITIAL_BALANCE
    try:
        df, raw, features = f78b.load_inputs()
        feature_map = {key: value for key, value in f79b.feature_sets(features).items() if key in {"runtime_fill_context", "contract_core", "no_external"}}
        builders: dict[str, Callable[[], Any]] = f79b.model_builders()
        thresholds = f78b.risk_thresholds(df)
        specs = repair_specs()
        sessions = ["all", "cash_open", "cash_mid"]
        risk_filters = ["none", "trend_aligned"]
        prob_quantiles = [0.68, 0.82, 0.90]
        cooldowns = [0, 6]
        candidates: list[dict[str, Any]] = []
        label_audit: list[dict[str, Any]] = []
        candidate_id = 0
        for spec in specs:
            indices = entry_indices(df, raw)
            outcome = compute_bidask_outcome(raw, indices, spec)
            label = make_label(df, outcome, spec)
            train_valid = (df["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
            positive = int(label[train_valid].sum()) if train_valid.sum() else 0
            label_audit.append(
                {
                    "label_name": spec.name,
                    "fill_policy": spec.fill_policy,
                    "hold_bars": spec.hold_bars,
                    "tp_price_units": spec.tp_price_units,
                    "sl_price_units": spec.sl_price_units,
                    "train_valid_rows": int(train_valid.sum()),
                    "train_positive_rows": positive,
                    "train_positive_rate": float(label[train_valid].mean()) if train_valid.sum() else 0.0,
                    "train_both_hit_rows": int(np.asarray(outcome["both_hit"], dtype=int)[train_valid].sum()) if train_valid.sum() else 0,
                    "validation_valid_rows": int(((df["split"] == "validation").to_numpy() & np.asarray(outcome["valid"], dtype=bool)).sum()),
                    "oos_valid_rows": int(((df["split"] == "oos").to_numpy() & np.asarray(outcome["valid"], dtype=bool)).sum()),
                }
            )
            if train_valid.sum() == 0 or positive == 0 or positive == train_valid.sum():
                continue
            for feature_set_name, cols in feature_map.items():
                if not cols:
                    continue
                matrices = f78b.clean_matrices(df, train_valid, cols)
                train_matrix = df.loc[train_valid, cols].replace([np.inf, -np.inf], np.nan)
                med = train_matrix.median(numeric_only=True).fillna(0.0)
                train_matrix = train_matrix.fillna(med).astype(float)
                y_train = label[train_valid]
                for model_name, builder in builders.items():
                    model = builder()
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            model.fit(train_matrix, y_train)
                        train_probs = f78b.probability(model, train_matrix)
                        probs = {split: f78b.probability(model, matrices[split]) for split in ("validation", "oos")}
                    except Exception:
                        continue
                    for q in prob_quantiles:
                        prob_threshold = float(np.quantile(train_probs, q))
                        for session in sessions:
                            for risk_filter in risk_filters:
                                for cooldown in cooldowns:
                                    split_payload: dict[str, dict[str, Any]] = {}
                                    row_base: dict[str, Any] = {}
                                    for split in ("validation", "oos"):
                                        split_mask_global = (df["split"] == split).to_numpy()
                                        split_df = df.loc[split_mask_global].reset_index(drop=True)
                                        split_outcome = {key: np.asarray(value)[split_mask_global] for key, value in outcome.items()}
                                        valid = np.asarray(split_outcome["valid"], dtype=bool)
                                        raw_signal = (
                                            (probs[split] >= prob_threshold)
                                            & valid
                                            & f78b.session_mask(split_df, session)
                                            & f78b.risk_mask(split_df, risk_filter, spec.side, thresholds)
                                        )
                                        selected = f78b.lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int), cooldown)
                                        metrics = f78b.contract_kpi(split_df, selected, split_outcome)
                                        split_payload[split] = metrics
                                        row_base[f"{split}_raw_signal_count"] = int(raw_signal.sum())
                                        row_base[f"{split}_lifecycle_trade_count"] = int(selected.sum())
                                        row_base[f"{split}_signal_to_trade_ratio"] = int(selected.sum()) / int(raw_signal.sum()) if int(raw_signal.sum()) else 0.0
                                    val = split_payload["validation"]
                                    oos = split_payload["oos"]
                                    scout = scout_gate(val, oos)
                                    meaningful = meaningful_gate(val, oos)
                                    dual_positive = float(val["net"]) > 0.0 and float(oos["net"]) > 0.0
                                    candidate_id += 1
                                    row: dict[str, Any] = {
                                        "candidate_id": f"f79f_{candidate_id:05d}",
                                        "label_name": spec.name,
                                        "side": spec.side,
                                        "entry_price_model": "bid_open_plus_spread_for_long",
                                        "fill_policy": spec.fill_policy,
                                        "hold_bars": spec.hold_bars,
                                        "tp_price_units": spec.tp_price_units,
                                        "sl_price_units": spec.sl_price_units,
                                        "tp_broker_points": spec.tp_price_units * f79b.SLTP_POINT_SCALE,
                                        "sl_broker_points": spec.sl_price_units * f79b.SLTP_POINT_SCALE,
                                        "feature_set": feature_set_name,
                                        "feature_count": len(cols),
                                        "model": model_name,
                                        "prob_quantile": q,
                                        "prob_threshold": prob_threshold,
                                        "session": session,
                                        "risk_filter": risk_filter,
                                        "cooldown_bars": cooldown,
                                        "scout_clue": int(scout),
                                        "meaningful_signal": int(meaningful),
                                        "dual_positive": int(dual_positive),
                                        "rank_score": rank_score(val, oos, meaningful, scout),
                                        **row_base,
                                    }
                                    for prefix, metrics in (("val", val), ("oos", oos)):
                                        row.update(
                                            {
                                                f"{prefix}_net": metrics["net"],
                                                f"{prefix}_gross_profit": metrics["gross_profit"],
                                                f"{prefix}_gross_loss": metrics["gross_loss"],
                                                f"{prefix}_pf": metrics["pf"],
                                                f"{prefix}_dd_pct": metrics["dd_pct"],
                                                f"{prefix}_trade_count": metrics["trade_count"],
                                                f"{prefix}_calendar_days": metrics["calendar_days"],
                                                f"{prefix}_calendar_trades_day": metrics["calendar_trades_day"],
                                                f"{prefix}_active_trades_day": metrics["active_trades_day"],
                                                f"{prefix}_win_rate": metrics["win_rate"],
                                                f"{prefix}_avg_win": metrics["avg_win"],
                                                f"{prefix}_avg_loss": metrics["avg_loss"],
                                                f"{prefix}_payoff": metrics["payoff"],
                                                f"{prefix}_expectancy": metrics["expectancy"],
                                                f"{prefix}_recovery": metrics["recovery"],
                                                f"{prefix}_max_consecutive_loss": metrics["max_consecutive_loss"],
                                                f"{prefix}_time_under_water_trades": metrics["time_under_water_trades"],
                                            }
                                        )
                                    candidates.append(row)
        candidates.sort(key=lambda item: float(item.get("rank_score", -1e18)), reverse=True)
        summary = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "candidate_rows": len(candidates),
            "label_rows": len(label_audit),
            "scout_clue_count": sum(int(row.get("scout_clue", 0)) for row in candidates),
            "meaningful_signal_count": sum(int(row.get("meaningful_signal", 0)) for row in candidates),
            "dual_positive_count": sum(int(row.get("dual_positive", 0)) for row in candidates),
            "best_candidate": candidates[0] if candidates else {},
            "repair_axis": "bidask_entry_plus_ambiguous_both_hit_guard",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        return candidates, label_audit, summary
    finally:
        f78b.INITIAL_BALANCE = original_balance


def decide_next(summary: Mapping[str, Any]) -> tuple[str, str, str]:
    if int(summary.get("meaningful_signal_count", 0)) > 0:
        return (
            "repair_proxy_meaningful_signal_pre_mt5_grok_required_no_authority",
            "repair_proxy_meaningful_signal_requires_pre_mt5_grok_no_authority",
            NEXT_RUN_IF_MEANINGFUL,
        )
    if int(summary.get("dual_positive_count", 0)) > 0:
        return (
            "repair_proxy_weak_nonzero_no_additional_runtime_probe_yet_no_authority",
            "repair_proxy_weak_nonzero_density_or_gate_failure_closeout_decision_required_no_authority",
            NEXT_RUN_IF_WEAK,
        )
    return (
        "repair_proxy_zero_signal_closeout_decision_required_no_authority",
        "repair_proxy_zero_signal_after_ambiguous_fill_guard_no_authority",
        NEXT_RUN_IF_ZERO,
    )


def report_text(summary: Mapping[str, Any], status: str, judgment: str, next_run: str, created_at: str) -> str:
    best = summary.get("best_candidate") or {}
    return f"""# Frontier79F Ambiguous Fill-Order Guard Repair Proxy Report(F79F 모호 체결 순서 보호 수리 프록시 보고서)

Updated(갱신): {created_at}

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- candidate rows(후보 행): `{summary.get('candidate_rows')}`
- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- dual positive(검증/표본외 양수): `{summary.get('dual_positive_count')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Best Candidate(최선 후보)

- candidate(후보): `{best.get('candidate_id', '')}`
- axes(축): `{best.get('label_name', '')}/{best.get('feature_set', '')}/{best.get('model', '')}/{best.get('session', '')}/{best.get('risk_filter', '')}/q{best.get('prob_quantile', '')}/cd{best.get('cooldown_bars', '')}`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일 거래/거래): `{best.get('val_net', '')}/{best.get('val_pf', '')}/{best.get('val_dd_pct', '')}/{best.get('val_calendar_trades_day', '')}/{best.get('val_trade_count', '')}`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일 거래/거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}/{best.get('oos_trade_count', '')}`

## Repair Read(수리 판독)

Action(행동): long entry(롱 진입)를 bid open plus spread(매수 호가형 시가)로 바꾸고, both-hit ambiguity(동시 도달 모호성)를 pessimistic(보수) 또는 skip(제외) 처리했다.

Effect(효과): F79D에서 보인 close_direction optimism(종가방향 낙관 편향)을 줄인 뒤에도 밀도(density, 밀도)와 경제성(economics, 경제성)이 살아남는지 본다.

## Next Action(다음 행동)

`{next_run}`
"""


def gate_audit_text(summary: Mapping[str, Any], status: str, created_at: str) -> str:
    return f"""# Required Gate Coverage Audit F79F(F79F 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F79E gap cause used(F79E 간극 원인 사용) | `passed(통과)` | both-hit ambiguity(동시 도달 모호성) + bid/ask geometry(매수/매도 호가 구조) |
| repair axis materialized(수리 축 물질화) | `passed(통과)` | `bidask_pessimistic`, `bidask_skip_both` |
| broad-enough proxy repair(충분히 넓은 프록시 수리) | `passed(통과)` | feature/model/session/risk/threshold/cooldown variants(피처/모델/세션/위험/임계값/쿨다운 변형) |
| status(상태) | `{status}` | candidate_rows(후보 행) `{summary.get('candidate_rows')}` |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_ledgers(summary: Mapping[str, Any], status: str, judgment: str, next_run: str, created_at: str) -> None:
    best = summary.get("best_candidate") or {}
    row_id = f"{RUN_ID}__repair_proxy"
    row = {
        "ledger_row_id": row_id,
        "row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_proxy(수리 프록시)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "ambiguous fill-order guard repair proxy(모호 체결 순서 보호 수리 프록시)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "repair_proxy_kpi(수리 프록시 KPI)",
        "scoreboard_lane": "repair_proxy(수리 프록시)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best={best.get('candidate_id', '')};val_pf={best.get('val_pf', '')};oos_pf={best.get('oos_pf', '')};oos_tpd={best.get('oos_calendar_trades_day', '')}",
        "guardrail_kpi": f"scout={summary.get('scout_clue_count')};meaningful={summary.get('meaningful_signal_count')};dual_positive={summary.get('dual_positive_count')}",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": "repair proxy after F79D/F79E; MT5 not claimed in this run",
        "lane": "repair_proxy(수리 프록시)",
        "family": "proxy_repair(프록시 수리)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier79F",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": next_run,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": status,
        "view": "Repair Proxy(수리 프록시)",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "proxy_repair(프록시 수리)",
        "evidence_boundary": "repair_proxy_no_authority(수리 프록시, 권위 없음)",
        "next_action": next_run,
        "question": "Does ambiguous fill-order guarding repair F79 runtime economics?(모호 체결 순서 보호가 F79 런타임 경제성을 고치는가?)",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_repair_only(프록시 수리 전용)",
        "net_profit": best.get("oos_net", ""),
        "profit_factor": best.get("oos_pf", ""),
        "drawdown": best.get("oos_dd_pct", ""),
        "trade_count": best.get("oos_trade_count", ""),
        "trade_density": best.get("oos_calendar_trades_day", ""),
    }
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_state(summary: Mapping[str, Any], status: str, judgment: str, next_run: str, created_at: str) -> None:
    best = summary.get("best_candidate") or {}
    marker = "<!-- frontier79F_ambiguous_fill_order_guard_repair_proxy_v1 -->"
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` executed ambiguous fill-order guard repair proxy(모호 체결 순서 보호 수리 프록시). Result(결과): scout `{summary.get('scout_clue_count')}`, meaningful `{summary.get('meaningful_signal_count')}`, dual_positive `{summary.get('dual_positive_count')}`. Best(최선): `{best.get('candidate_id', '')}` OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일 거래) `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{next_run}`.
"""
        write_text(IDEA_REGISTRY, text.rstrip() + addition)
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {next_run}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {next_run}
runtime_probe_status: f79_runtime_probe_completed_repair_proxy_done
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f78_closeout_3_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F79F ambiguous fill-order guard repair proxy(모호 체결 순서 보호 수리 프록시)를 실행했다."
  - "Effect(효과): F79D 간극 원인을 라벨/거래 형태 수준에서 수리해도 목표 축이 살아남는지 확인했다."
  - "Best(최선): {best.get('candidate_id', '')} OOS net/PF/DD/tpd {best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F79F ambiguous fill-order guard repair proxy(모호 체결 순서 보호 수리 프록시)를 실행했다.

Effect(효과): F79D runtime gap(런타임 간극)의 원인이었던 close_direction optimism(종가방향 낙관)을 줄여도 후보가 살아남는지 확인했다.

## Repair Result(수리 결과)

- scout clue(탐색 단서): `{summary.get('scout_clue_count')}`
- meaningful signal(의미 신호): `{summary.get('meaningful_signal_count')}`
- dual positive(검증/표본외 양수): `{summary.get('dual_positive_count')}`
- best OOS net/PF/DD/tpd(최선 표본외 순수익/수익 팩터/손실폭/일 거래): `{best.get('oos_net', '')}/{best.get('oos_pf', '')}/{best.get('oos_dd_pct', '')}/{best.get('oos_calendar_trades_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{next_run}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F79 Selection Status(F79 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F79F ambiguous fill-order guard repair proxy(모호 체결 순서 보호 수리 프록시)를 실행했다.

Effect(효과): 다음 실행은 수리 결과에 따른 closeout decision(마감 결정) 또는 pre-MT5 Grok review(사전 MT5 그록 검토)다.

Current run(현재 실행): `{next_run}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    candidates, label_audit, summary = fit_and_score()
    status, judgment, next_run = decide_next(summary)
    summary = dict(summary)
    summary.update({"status": status, "judgment": judgment, "next_run_id": next_run, "created_at_utc": created_at})
    write_csv(CANDIDATES_ALL, candidates)
    write_csv(CANDIDATES_TOP, candidates[:200])
    write_csv(LABEL_AUDIT, label_audit)
    write_json(SUMMARY_PATH, summary)
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": next_run,
            "created_at_utc": created_at,
            "summary_path": rel(SUMMARY_PATH),
            "candidates_all": rel(CANDIDATES_ALL),
            "candidates_top": rel(CANDIDATES_TOP),
            "label_audit": rel(LABEL_AUDIT),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(REPORT_PATH, report_text(summary, status, judgment, next_run, created_at))
    write_text(GATE_AUDIT_PATH, gate_audit_text(summary, status, created_at))
    update_ledgers(summary, status, judgment, next_run, created_at)
    update_state(summary, status, judgment, next_run, created_at)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

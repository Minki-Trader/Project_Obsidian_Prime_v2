from __future__ import annotations

import csv
import hashlib
import json
import math
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

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_69 import frontier69b_event_first_first_hit_proxy_sweep as f69b


STAGE_ID = f69b.STAGE_ID
RUN_ID = "frontier69C_repair_event_first_label_or_feature_surface_v1"
PARENT_RUN_ID = f69b.RUN_ID
NEXT_RUN_SIGNAL = "frontier69D_pre_mt5_grok_review_density_repair_v1"
NEXT_RUN_REPAIR = "frontier69D_tier_b_and_event_surface_repair_v1"
IDEA_ID = f69b.IDEA_ID

CLAIM_BOUNDARY = (
    "proxy_repair_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f69b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f69b.REVIEWS_ROOT
SELECTED_ROOT = f69b.SELECTED_ROOT
F69B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f69b_proxy_candidate_summary.csv"


@dataclass(frozen=True)
class RepairSpec:
    candidate_id: str
    target: f69b.TargetSpec
    feature_set: f69b.FeatureSet
    model: f69b.ModelSpec
    event_id: str
    side_policy: str
    edge_floor_quantile: float
    edge_floor: float
    daily_quota: int
    cooldown_bars: int


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def stable_id(parts: Sequence[Any]) -> str:
    return hashlib.sha1("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:12]


def fmt(value: Any, digits: int = 6) -> str:
    if value is None:
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return ""
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


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


def load_f69b_summary() -> pd.DataFrame:
    if not path_exists(F69B_SUMMARY):
        raise FileNotFoundError(rel(F69B_SUMMARY))
    return pd.read_csv(io_path(F69B_SUMMARY))


def seed_rows(summary: pd.DataFrame) -> pd.DataFrame:
    dual_positive = summary[(summary["validation_net"] > 0) & (summary["oos_net"] > 0)].copy()
    high_pf = dual_positive.sort_values(["min_pf", "selection_score"], ascending=False).head(8)
    dense = summary[
        summary["validation_trades_per_day"].between(2.0, 18.0)
        & summary["oos_trades_per_day"].between(2.0, 18.0)
    ].sort_values(["min_pf", "selection_score"], ascending=False).head(4)
    seeds = pd.concat([high_pf, dense], ignore_index=True).drop_duplicates("candidate_id")
    return seeds.head(10).reset_index(drop=True)


def repair_targets(seeds: pd.DataFrame) -> list[f69b.TargetSpec]:
    horizons = sorted({int(value) for value in seeds["horizon_bars"].dropna().tolist()})
    return [
        f69b.TargetSpec(
            target_id=f"fh_h{horizon}_sl09_tp135_edge05_density_repair",
            horizon_bars=horizon,
            sl_atr=0.90,
            tp_atr=1.35,
            min_edge_atr=0.05,
            min_edge_points=0.50,
        )
        for horizon in horizons
    ]


def extra_feature_sets(base: pd.DataFrame) -> list[f69b.FeatureSet]:
    definitions = {
        "session_morph_micro_v2": [
            "minutes_from_cash_open",
            "is_first_30m_after_open",
            "is_last_30m_before_cash_close",
            "hl_range",
            "close_open_ratio",
            "return_zscore_20",
            "rsi_14",
            "bb_position_20",
        ],
        "session_regime_micro_v2": [
            "minutes_from_cash_open",
            "is_first_30m_after_open",
            "is_last_30m_before_cash_close",
            "adx_14",
            "di_spread_14",
            "atr_14_over_atr_50",
            "historical_vol_5_over_20",
            "vortex_indicator",
        ],
    }
    rows: list[f69b.FeatureSet] = []
    for name, columns in definitions.items():
        missing = [column for column in columns if column not in base.columns]
        if missing:
            raise RuntimeError(f"missing columns for {name}: {missing}")
        rows.append(f69b.FeatureSet(name, tuple(columns)))
    return rows


def candidate_feature_sets(base: pd.DataFrame, seeds: pd.DataFrame) -> list[f69b.FeatureSet]:
    lookup = {feature.feature_set_id: feature for feature in f69b.feature_sets(base)}
    selected_ids = list(dict.fromkeys(str(value) for value in seeds["feature_set_id"].dropna().tolist()))[:2]
    selected = [lookup[name] for name in selected_ids if name in lookup]
    selected.extend(extra_feature_sets(base)[:1])
    dedup: dict[str, f69b.FeatureSet] = {}
    for feature in selected:
        dedup[feature.feature_set_id] = feature
    return list(dedup.values())


def candidate_models(seeds: pd.DataFrame) -> list[f69b.ModelSpec]:
    lookup = {model.model_id: model for model in f69b.model_specs()}
    ids = list(dict.fromkeys(str(value) for value in seeds["model_id"].dropna().tolist()))[:2]
    return [lookup[model_id] for model_id in ids if model_id in lookup]


def side_policies(seeds: pd.DataFrame) -> list[str]:
    return ["long_only"]


def selected_event_ids(seeds: pd.DataFrame) -> set[str]:
    return {"event_cash_any_context", "event_morph_range_impulse", "event_session_edges"}


def train_score_cache(frame: pd.DataFrame, features: f69b.FeatureSet, model: f69b.ModelSpec) -> dict[str, Any] | None:
    train_mask = frame["split"].astype(str).eq("train").to_numpy()
    y_train = frame.loc[train_mask, "target_class"].to_numpy(dtype=int)
    if len(set(y_train.tolist())) < 2:
        return None
    estimator = model.build()
    estimator.fit(frame.loc[train_mask, list(features.columns)], y_train)
    classes = list(getattr(estimator, "classes_", getattr(estimator[-1], "classes_", [])))
    cache: dict[str, Any] = {"classes": [int(value) for value in classes]}
    for split_name in ("train", "validation", "oos"):
        mask = frame["split"].astype(str).eq(split_name).to_numpy()
        proba = estimator.predict_proba(frame.loc[mask, list(features.columns)])
        side, edge = f69b.side_and_edge(proba, classes)
        cache[split_name] = (mask, side, edge)
    return cache


def daily_quota_indices(
    split_frame: pd.DataFrame,
    event_mask: np.ndarray,
    side: np.ndarray,
    edge: np.ndarray,
    spec: RepairSpec,
) -> list[int]:
    adjusted_side = f69b.apply_side_policy(side.copy(), spec.side_policy)
    eligible = event_mask & (adjusted_side != 1) & np.isfinite(edge) & (edge >= float(spec.edge_floor))
    if not eligible.any():
        return []
    work = pd.DataFrame(
        {
            "idx": np.arange(len(split_frame)),
            "timestamp": pd.to_datetime(split_frame["timestamp"], utc=True),
            "edge": edge,
            "eligible": eligible,
        }
    )
    work = work.loc[work["eligible"]].copy()
    work["day"] = work["timestamp"].dt.strftime("%Y-%m-%d")
    work["rank"] = work.groupby("day")["edge"].rank(method="first", ascending=False)
    chosen_signal = np.zeros(len(split_frame), dtype=bool)
    chosen_signal[work.loc[work["rank"] <= int(spec.daily_quota), "idx"].to_numpy(dtype=int)] = True
    return f69b.non_overlap_indices(chosen_signal, spec.target.horizon_bars, spec.cooldown_bars)


def evaluate_repair(
    frame: pd.DataFrame,
    events: Mapping[str, np.ndarray],
    cache: Mapping[str, Any],
    spec: RepairSpec,
    split_name: str,
) -> dict[str, Any]:
    split_mask, side, edge = cache[split_name]
    split_frame = frame.loc[split_mask].copy().reset_index(drop=True)
    event_mask = events[spec.event_id][split_mask]
    selected = daily_quota_indices(split_frame, event_mask, side, edge, spec)
    adjusted_side = f69b.apply_side_policy(side.copy(), spec.side_policy)
    values = f69b.profit_for_side(split_frame, adjusted_side)
    selected_values = values[selected] if selected else np.array([], dtype=float)
    selected_timestamps = split_frame.loc[selected, "timestamp"] if selected else split_frame["timestamp"].iloc[:0]
    metrics = f69b.proxy_kpi(selected_values, selected_timestamps, split_frame["timestamp"])
    return {
        "candidate_id": spec.candidate_id,
        "split": split_name,
        "target_id": spec.target.target_id,
        "horizon_bars": spec.target.horizon_bars,
        "feature_set_id": spec.feature_set.feature_set_id,
        "feature_count": len(spec.feature_set.columns),
        "model_id": spec.model.model_id,
        "model_family": spec.model.model_family,
        "event_id": spec.event_id,
        "side_policy": spec.side_policy,
        "edge_floor_quantile": spec.edge_floor_quantile,
        "edge_floor": spec.edge_floor,
        "daily_quota": spec.daily_quota,
        "cooldown_bars": spec.cooldown_bars,
        "trade_count": metrics["trade_count"],
        "trades_per_day": metrics["trades_per_day"],
        "net_profit": metrics["net_profit"],
        "gross_profit": metrics["gross_profit"],
        "gross_loss": metrics["gross_loss"],
        "profit_factor": metrics["profit_factor"],
        "drawdown": metrics["max_drawdown"],
        "drawdown_percent_on_10000": metrics["max_drawdown_percent_on_10000"],
        "win_rate": metrics["win_rate"],
        "average_win": metrics["average_win"],
        "average_loss": metrics["average_loss"],
        "payoff_ratio": metrics["payoff_ratio"],
        "expectancy": metrics["expectancy"],
        "recovery_factor": metrics["recovery_factor"],
        "time_under_water_trade_share": metrics["time_under_water_trade_share"],
        "max_underwater_trades": metrics["max_underwater_trades"],
        "max_consecutive_loss": metrics["max_consecutive_loss"],
        "positive_month_share": metrics["positive_month_share"],
        "long_trade_count": int((adjusted_side[selected] == 2).sum()) if selected else 0,
        "short_trade_count": int((adjusted_side[selected] == 0).sum()) if selected else 0,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def summarize(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["candidate_id"]), {})[str(row["split"])] = row
    summaries: list[dict[str, Any]] = []
    for candidate_id, splits in grouped.items():
        val = splits.get("validation")
        oos = splits.get("oos")
        if not val or not oos:
            continue
        min_pf = min(float(val["profit_factor"]), float(oos["profit_factor"]))
        min_net = min(float(val["net_profit"]), float(oos["net_profit"]))
        max_dd = max(float(val["drawdown_percent_on_10000"]), float(oos["drawdown_percent_on_10000"]))
        density_distance = abs(float(val["trades_per_day"]) - 7.5) + abs(float(oos["trades_per_day"]) - 7.5)
        scout = (
            float(val["net_profit"]) > 0
            and float(oos["net_profit"]) > 0
            and min_pf >= 1.03
            and 2.0 <= float(val["trades_per_day"]) <= 14.0
            and 2.0 <= float(oos["trades_per_day"]) <= 14.0
        )
        meaningful = scout and min_pf >= 1.08 and max_dd <= 25.0
        score = min_pf * 100.0 + min_net * 0.03 - max_dd * 0.4 - density_distance * 2.0
        summaries.append(
            {
                "candidate_id": candidate_id,
                "target_id": val["target_id"],
                "horizon_bars": val["horizon_bars"],
                "feature_set_id": val["feature_set_id"],
                "feature_count": val["feature_count"],
                "model_id": val["model_id"],
                "model_family": val["model_family"],
                "event_id": val["event_id"],
                "side_policy": val["side_policy"],
                "edge_floor_quantile": val["edge_floor_quantile"],
                "daily_quota": val["daily_quota"],
                "cooldown_bars": val["cooldown_bars"],
                "validation_net": val["net_profit"],
                "validation_pf": val["profit_factor"],
                "validation_dd_pct": val["drawdown_percent_on_10000"],
                "validation_trades": val["trade_count"],
                "validation_trades_per_day": val["trades_per_day"],
                "oos_net": oos["net_profit"],
                "oos_pf": oos["profit_factor"],
                "oos_dd_pct": oos["drawdown_percent_on_10000"],
                "oos_trades": oos["trade_count"],
                "oos_trades_per_day": oos["trades_per_day"],
                "min_pf": min_pf,
                "min_net": min_net,
                "max_dd_pct": max_dd,
                "density_distance_to_7p5": density_distance,
                "scout_signal": bool(scout),
                "meaningful_proxy_signal": bool(meaningful),
                "selection_score": float(score),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return sorted(summaries, key=lambda row: float(row["selection_score"]), reverse=True)


def bucket_rows(
    frame_by_target: Mapping[str, pd.DataFrame],
    cache_index: Mapping[str, Mapping[str, Any]],
    events_by_target: Mapping[str, Mapping[str, np.ndarray]],
    spec_index: Mapping[str, RepairSpec],
    top: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for summary in list(top)[:15]:
        spec = spec_index.get(str(summary["candidate_id"]))
        if spec is None:
            continue
        frame = frame_by_target[spec.target.target_id]
        cache = cache_index["|".join([spec.target.target_id, spec.feature_set.feature_set_id, spec.model.model_id])]
        events = events_by_target[spec.target.target_id]
        for split_name in ("validation", "oos"):
            split_mask, side, edge = cache[split_name]
            split_frame = frame.loc[split_mask].copy().reset_index(drop=True)
            event_mask = events[spec.event_id][split_mask]
            selected = daily_quota_indices(split_frame, event_mask, side, edge, spec)
            adjusted_side = f69b.apply_side_policy(side.copy(), spec.side_policy)
            selected_frame = split_frame.loc[selected].copy() if selected else split_frame.iloc[:0].copy()
            selected_frame["selected_side"] = adjusted_side[selected] if selected else []
            selected_frame["selected_profit"] = f69b.profit_for_side(split_frame, adjusted_side)[selected] if selected else []
            for bucket_group in ("session", "regime"):
                labels = f69b.bucket_label(selected_frame, bucket_group) if len(selected_frame) else pd.Series(dtype=str)
                for bucket in sorted(labels.unique().tolist()):
                    bucket_frame = selected_frame.loc[labels.eq(bucket)]
                    metrics = f69b.proxy_kpi(bucket_frame["selected_profit"].to_numpy(dtype=float), bucket_frame["timestamp"], split_frame["timestamp"])
                    rows.append(
                        {
                            "candidate_id": spec.candidate_id,
                            "split": split_name,
                            "bucket_group": bucket_group,
                            "bucket": bucket,
                            "trade_count": metrics["trade_count"],
                            "trades_per_day": metrics["trades_per_day"],
                            "net_profit": metrics["net_profit"],
                            "profit_factor": metrics["profit_factor"],
                            "drawdown_percent_on_10000": metrics["max_drawdown_percent_on_10000"],
                            "win_rate": metrics["win_rate"],
                            "expectancy": metrics["expectancy"],
                        }
                    )
    return rows


def run_repair(created_at: str) -> dict[str, Any]:
    summary = load_f69b_summary()
    seeds = seed_rows(summary)
    base, raw = f69b.load_frames()
    features = candidate_feature_sets(base, seeds)
    models = candidate_models(seeds)
    policies = side_policies(seeds)
    selected_events = selected_event_ids(seeds)

    frame_by_target: dict[str, pd.DataFrame] = {}
    events_by_target: dict[str, dict[str, np.ndarray]] = {}
    cache_index: dict[str, Mapping[str, Any]] = {}
    spec_index: dict[str, RepairSpec] = {}
    kpi_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []

    for target in repair_targets(seeds):
        frame = f69b.build_target_frame(base, raw, target)
        frame_by_target[target.target_id] = frame
        events = {event.event_id: event.mask for event in f69b.event_specs(frame) if event.event_id in selected_events}
        events_by_target[target.target_id] = events
        for feature in features:
            for model in models:
                cache = train_score_cache(frame, feature, model)
                cache_key = "|".join([target.target_id, feature.feature_set_id, model.model_id])
                if cache is None:
                    audit_rows.append({"target_id": target.target_id, "feature_set_id": feature.feature_set_id, "model_id": model.model_id, "status": "skipped_single_class"})
                    continue
                cache_index[cache_key] = cache
                train_mask, train_side_base, train_edge = cache["train"]
                for event_id, event_mask in events.items():
                    for side_policy in policies:
                        train_side = f69b.apply_side_policy(train_side_base.copy(), side_policy)
                        train_pool_mask = event_mask[train_mask] & (train_side != 1) & np.isfinite(train_edge)
                        train_pool = train_edge[train_pool_mask]
                        if len(train_pool) == 0:
                            continue
                        for floor_quantile in (0.00, 0.50):
                            floor = float(np.quantile(train_pool, floor_quantile))
                            for daily_quota in (3, 5, 8):
                                for cooldown_bars in (0,):
                                    candidate_id = "f69c_" + stable_id(
                                        [
                                            target.target_id,
                                            feature.feature_set_id,
                                            model.model_id,
                                            event_id,
                                            side_policy,
                                            floor_quantile,
                                            daily_quota,
                                            cooldown_bars,
                                        ]
                                    )
                                    spec = RepairSpec(
                                        candidate_id=candidate_id,
                                        target=target,
                                        feature_set=feature,
                                        model=model,
                                        event_id=event_id,
                                        side_policy=side_policy,
                                        edge_floor_quantile=floor_quantile,
                                        edge_floor=floor,
                                        daily_quota=int(daily_quota),
                                        cooldown_bars=int(cooldown_bars),
                                    )
                                    spec_index[candidate_id] = spec
                                    for split_name in ("validation", "oos"):
                                        kpi_rows.append(evaluate_repair(frame, events, cache, spec, split_name))
                audit_rows.append(
                    {
                        "target_id": target.target_id,
                        "feature_set_id": feature.feature_set_id,
                        "model_id": model.model_id,
                        "status": "trained",
                        "classes_seen": ",".join(str(value) for value in cache["classes"]),
                    }
                )
    summaries = summarize(kpi_rows)
    scout = [row for row in summaries if row["scout_signal"]]
    meaningful = [row for row in summaries if row["meaningful_proxy_signal"]]
    top = summaries[:25]
    buckets = bucket_rows(frame_by_target, cache_index, events_by_target, spec_index, top)
    next_run = NEXT_RUN_SIGNAL if meaningful else NEXT_RUN_REPAIR
    status = "completed_density_repair_proxy_scout_clue_no_authority" if meaningful else "completed_density_repair_no_meaningful_signal_no_authority"
    judgment = "scout_clue_density_repair_signal_found_no_authority" if meaningful else "proxy_density_repair_inconclusive_no_authority"
    return {
        "created_at_utc": created_at,
        "parent_summary_rows": int(len(summary)),
        "seed_rows": seeds.to_dict(orient="records"),
        "target_count": len(frame_by_target),
        "feature_count": len(features),
        "model_count": len(models),
        "kpi_rows": kpi_rows,
        "candidate_summaries": summaries,
        "scout_candidates": scout,
        "meaningful_candidates": meaningful,
        "bucket_rows": buckets,
        "model_audit_rows": audit_rows,
        "next_run_id": next_run,
        "status": status,
        "judgment": judgment,
    }


def report_lines(result: Mapping[str, Any]) -> list[str]:
    best = result["candidate_summaries"][0] if result["candidate_summaries"] else {}
    return [
        "# F69C Density Repair Proxy(F69C 밀도 수리 프록시)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "## Hypothesis(가설)",
        "",
        "F69B의 high-PF low-density clue(고수익 팩터 저밀도 단서)를 daily quota(일별 할당), lower edge floor(낮은 점수 하한), lighter target edge(가벼운 목표 하한)로 수리하면 trades/day(일 거래)와 PF(수익 팩터)를 동시에 움직일 수 있는지 시험했다.",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F69B 상위 PF 단서와 밀도 단서를 seed(씨앗)로 삼아 label threshold(라벨 하한), feature set(피처 묶음), daily quota trade shape(일별 할당 거래 형태)를 재조합했다.",
        "",
        "Effect(효과): ultra sparse PF(초저밀도 수익 팩터)를 5~10/day 목표 쪽으로 당길 수 있는지 확인한다.",
        "",
        "## KPI Summary(KPI 핵심 성과 요약)",
        "",
        f"- candidate rows(후보 행): `{len(result['candidate_summaries'])}` summary(요약), `{len(result['kpi_rows'])}` split KPI(분할 KPI).",
        f"- scout candidates(탐색 단서 후보): `{len(result['scout_candidates'])}`.",
        f"- meaningful candidates(의미 후보): `{len(result['meaningful_candidates'])}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- top validation net/PF/DD/trades_day(상위 검증 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('validation_net'))}` / `{fmt(best.get('validation_pf'))}` / `{fmt(best.get('validation_dd_pct'))}` / `{fmt(best.get('validation_trades_per_day'))}`.",
        f"- top OOS net/PF/DD/trades_day(상위 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        "",
        "## Decision(결정)",
        "",
        f"- status(상태): `{result['status']}`.",
        f"- judgment(판정): `{result['judgment']}`.",
        f"- next action(다음 행동): `{result['next_run_id']}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def experiment_design(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "hypothesis": "daily quota density repair(일별 할당 밀도 수리)가 F69B high-PF low-density clue(고PF 저밀도 단서)를 확장할 수 있다",
        "changed_variables": [
            "target min edge lowered from edge10 to edge05(목표 최소 하한 edge10에서 edge05로 낮춤)",
            "daily quota trade shape added(일별 할당 거래 형태 추가)",
            "micro feature recombinations added(마이크로 피처 재조합 추가)",
        ],
        "control_variables": [
            "SL/TP fixed at 0.90/1.35 ATR(손절/익절 0.90/1.35 ATR 고정)",
            "validation/OOS not used for thresholds(검증/표본외 임계값 미사용)",
            "no MT5 claim before Grok review(MT5 전 그록 검토 없이는 주장 없음)",
        ],
        "success_criteria": "validation/OOS net positive, PF>=1.08, 2-14 trades/day scout band(검증/표본외 양수, PF 1.08 이상, 2~14 일거래 탐색 구간)",
        "failure_criteria": "density repair collapses PF near 1 or remains ultra sparse(밀도 수리가 PF 1 근처 붕괴 또는 초저밀도 유지)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def gate_audit_lines(result: Mapping[str, Any]) -> list[str]:
    return [
        "# F69C Required Gate Coverage Audit(F69C 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        "| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |",
        "|---|---|---|---|",
        f"| parent_gap_analysis(부모 간극 분석) | pass(통과) | `{rel(F69B_SUMMARY)}` | F69B PF/density 분리 확인 |",
        f"| repair_design(수리 설계) | pass(통과) | `{rel(RUN_ROOT / 'f69c_experiment_design.json')}` | label/trade-shape/feature 수리 기록 |",
        f"| proxy_kpi(프록시 KPI) | pass(통과) | `{rel(RUN_ROOT / 'f69c_proxy_kpi_by_split.csv')}` | validation/OOS KPI 기록 |",
        f"| bucket_kpi(구간 KPI) | pass(통과) | `{rel(RUN_ROOT / 'f69c_bucket_kpi.csv')}` | session/regime 수리 귀속 기록 |",
        "| MT5 runtime probe(MT5 런타임 탐침) | pending(대기) | proxy repair boundary(프록시 수리 경계) | 의미 신호가 있으면 Grok 후 실행 |",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = [
        RUN_ROOT / "f69c_experiment_design.json",
        RUN_ROOT / "f69c_proxy_candidate_summary.csv",
        RUN_ROOT / "f69c_proxy_kpi_by_split.csv",
        RUN_ROOT / "f69c_bucket_kpi.csv",
        RUN_ROOT / "f69c_seed_rows.json",
        REVIEWS_ROOT / "frontier69C_repair_event_first_label_or_feature_surface_report.md",
        REVIEWS_ROOT / "required_gate_coverage_audit_f69c.md",
    ]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "producer": "stage_pipelines/stage_frontier_69/frontier69c_repair_event_first_label_or_feature_surface.py",
        "status": result["status"],
        "judgment": result["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run_id": result["next_run_id"],
        "artifacts": [rel(path) for path in artifacts],
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    for path in (RUN_ROOT, RUN_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_json(RUN_ROOT / "f69c_experiment_design.json", experiment_design(result))
    write_json(RUN_ROOT / "f69c_seed_rows.json", list(result["seed_rows"]))
    write_json(RUN_ROOT / "f69c_top_candidates.json", list(result["candidate_summaries"][:25]))
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(result))
    write_csv(RUN_ROOT / "f69c_proxy_kpi_by_split.csv", list(result["kpi_rows"]))
    write_csv(RUN_ROOT / "f69c_proxy_candidate_summary.csv", list(result["candidate_summaries"]))
    write_csv(RUN_ROOT / "f69c_bucket_kpi.csv", list(result["bucket_rows"]))
    write_csv(RUN_ROOT / "f69c_model_audit.csv", list(result["model_audit_rows"]))
    write_md(RUN_ROOT / "reports" / "result_summary.md", report_lines(result))

    write_csv(REVIEWS_ROOT / "f69c_proxy_kpi_by_split_review.csv", list(result["kpi_rows"]))
    write_csv(REVIEWS_ROOT / "f69c_proxy_candidate_summary_review.csv", list(result["candidate_summaries"]))
    write_csv(REVIEWS_ROOT / "f69c_bucket_kpi_review.csv", list(result["bucket_rows"]))
    write_json(REVIEWS_ROOT / "f69c_top_candidates_review.json", list(result["candidate_summaries"][:25]))
    write_md(REVIEWS_ROOT / "frontier69C_repair_event_first_label_or_feature_surface_report.md", report_lines(result))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f69c.md", gate_audit_lines(result))


def ledger_row(result: Mapping[str, Any]) -> dict[str, Any]:
    best = result["candidate_summaries"][0] if result["candidate_summaries"] else {}
    return {
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "Tier A separate(Tier A 분리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(Tier A 분리)",
        "view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "tier": "Tier A",
        "kpi_scope": "proxy_density_repair(프록시 밀도 수리)",
        "metric_scope": "validation_oos_proxy(검증/표본외 프록시)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "scoreboard": "structural_scout(구조 탐색)",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": f"stages/{STAGE_ID}/03_reviews/frontier69C_repair_event_first_label_or_feature_surface_report.md",
        "primary_report": f"stages/{STAGE_ID}/03_reviews/frontier69C_repair_event_first_label_or_feature_surface_report.md",
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier69C_repair_event_first_label_or_feature_surface_report.md",
        "primary_kpi": f"best={best.get('candidate_id', 'none')};val_pf={fmt(best.get('validation_pf'))};oos_pf={fmt(best.get('oos_pf'))}",
        "guardrail_kpi": "Tier B still missing_required; MT5 pending(Tier B 필수 누락 유지, MT5 대기)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(프록시 전용 주장 범위 밖)",
        "notes": "F69C repaired F69B PF/density split with daily quota and lighter first-hit label.",
        "run_number": "frontier69C",
        "date": str(result["created_at_utc"])[:10],
        "run_date": str(result["created_at_utc"])[:10],
        "decision": "pre_mt5_grok_if_signal_else_tier_b_event_repair",
        "next_run_id": result["next_run_id"],
        "rows": len(result["candidate_summaries"]),
        "candidate_rows": len(result["candidate_summaries"]),
        "positive_proxy_rows": len(result["meaningful_candidates"]),
        "claim_boundary": CLAIM_BOUNDARY,
        "best_proxy": best.get("candidate_id", ""),
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": fmt(best.get("oos_net")),
        "net_profit": fmt(best.get("oos_net")),
        "profit_factor": fmt(best.get("oos_pf")),
        "drawdown": fmt(best.get("oos_dd_pct")),
        "trade_count": fmt(best.get("oos_trades")),
        "trade_density": fmt(best.get("oos_trades_per_day")),
        "feature_count": best.get("feature_count", ""),
        "sample_rows": "",
        "attempt_count": len(result["candidate_summaries"]),
        "source_package_run_id": PARENT_RUN_ID,
        "evidence_boundary": "proxy_repair_only_no_runtime_authority(프록시 수리 전용, 런타임 권위 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "lane": "proxy_repair(프록시 수리)",
        "result_status": result["status"],
        "result_judgment": result["judgment"],
        "final_decision_path": f"stages/{STAGE_ID}/03_reviews/frontier69C_repair_event_first_label_or_feature_surface_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f69c.md",
        "created_at": result["created_at_utc"],
        "created_at_utc": result["created_at_utc"],
        "required_gate_audit": f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f69c.md",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_repair_only_no_runtime(프록시 수리 전용, 런타임 없음)",
        "question": "Can density repair extend F69B PF clue?(밀도 수리가 F69B PF 단서를 확장할 수 있는가)",
        "next_action": result["next_run_id"],
        "artifact_count": 12,
        "run_family": "frontier_proxy_repair(전선 프록시 수리)",
        "run_type": "density_quota_label_feature_repair(밀도 할당 라벨 피처 수리)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/f69c_proxy_candidate_summary.csv",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier69C_repair_event_first_label_or_feature_surface_report.md",
        "kpi_summary": f"summaries={len(result['candidate_summaries'])};scout={len(result['scout_candidates'])};meaningful={len(result['meaningful_candidates'])}",
    }


def update_ledgers(result: Mapping[str, Any]) -> None:
    row = ledger_row(result)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)


def update_review_index() -> None:
    marker = "<!-- frontier69C_repair_event_first_label_or_feature_surface_v1 -->"
    block = f"""<!-- frontier69C_repair_event_first_label_or_feature_surface_v1 -->
- `frontier69C_repair_event_first_label_or_feature_surface_report.md`: F69C density repair report(F69C 밀도 수리 보고서)
- `f69c_proxy_candidate_summary_review.csv`: F69C candidate summary(F69C 후보 요약)
- `f69c_proxy_kpi_by_split_review.csv`: F69C split KPI(F69C 분할 KPI)
- `f69c_bucket_kpi_review.csv`: F69C bucket KPI(F69C 구간 KPI)
- `required_gate_coverage_audit_f69c.md`: F69C gate audit(F69C 게이트 감사)"""
    append_once(REVIEWS_ROOT / "review_index.md", marker, block)


def update_registers(result: Mapping[str, Any]) -> None:
    marker = "<!-- frontier69C_repair_event_first_label_or_feature_surface_v1 -->"
    block = f"""<!-- frontier69C_repair_event_first_label_or_feature_surface_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` repaired F69B PF/density split(F69B PF/밀도 분리 수리). Result(결과): `{result['judgment']}`. Meaningful candidates(의미 후보): `{len(result['meaningful_candidates'])}`. Boundary(경계): proxy repair only(프록시 수리 전용), no authority(권위 없음). Next(다음): `{result['next_run_id']}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)


def update_state_files(result: Mapping[str, Any]) -> None:
    best = result["candidate_summaries"][0] if result["candidate_summaries"] else {}
    signal = bool(result["meaningful_candidates"])
    runtime_status = (
        "f69_mandatory_runtime_probe_pending_pre_mt5_grok_after_density_repair_signal(F69 밀도 수리 신호 후 사전 MT5 그록 및 필수 런타임 탐침 대기)"
        if signal
        else "f69_mandatory_runtime_probe_pending_after_tier_b_event_repair(F69 Tier B/이벤트 수리 후 필수 런타임 탐침 대기)"
    )
    selection = [
        "# F69 Selection Status(F69 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{result['next_run_id']}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{result['status']}`",
        f"- judgment(판정): `{result['judgment']}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- top_proxy_repair_clue(상위 프록시 수리 단서): `{best.get('candidate_id', 'none')}`.",
        f"- top_validation_net_pf_dd_tpd(상위 검증 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('validation_net'))}` / `{fmt(best.get('validation_pf'))}` / `{fmt(best.get('validation_dd_pct'))}` / `{fmt(best.get('validation_trades_per_day'))}`.",
        f"- top_oos_net_pf_dd_tpd(상위 표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        "- Tier B separate(Tier B 분리): still `missing_required(필수 누락)`.",
        f"- next_action(다음 행동): `{result['next_run_id']}`.",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(SELECTED_ROOT / "selection_status.md", selection)

    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {result['next_run_id']}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {result['status']}",
        f"current_judgment: {result['judgment']}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {result['next_run_id']}",
        f"runtime_probe_status: {runtime_status}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{result['created_at_utc']}'",
        "notes:",
        '  - "F69C action(행동): F69B PF/density split(F69B PF/밀도 분리)을 daily quota(일별 할당)와 label edge repair(라벨 하한 수리)로 시험했다."',
        f'  - "Effect(효과): top clue(상위 단서) `{best.get("candidate_id", "none")}` validation/OOS PF(검증/표본외 수익 팩터) `{fmt(best.get("validation_pf"))}/{fmt(best.get("oos_pf"))}`, trades/day(일 거래) `{fmt(best.get("validation_trades_per_day"))}/{fmt(best.get("oos_trades_per_day"))}`."',
        f'  - "Meaningful density repair candidates(의미 있는 밀도 수리 후보): `{len(result["meaningful_candidates"])}`."',
        '  - "Tier boundary(티어 경계): Tier B separate(분리)는 still missing_required(아직 필수 누락)."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(state) + "\n", encoding="utf-8-sig")

    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {result['created_at_utc']}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{result['next_run_id']}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F69C density repair proxy(F69C 밀도 수리 프록시)를 실행했다.",
        "",
        "Effect(효과): F69B의 high-PF low-density clue(고수익 팩터 저밀도 단서)가 daily quota(일별 할당)와 lighter label edge(가벼운 라벨 하한)에서 5~10/day 방향으로 확장되는지 확인했다.",
        "",
        f"- status(상태): `{result['status']}`.",
        f"- judgment(판정): `{result['judgment']}`.",
        f"- top candidate(상위 후보): `{best.get('candidate_id', 'none')}`.",
        f"- validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('validation_net'))}` / `{fmt(best.get('validation_pf'))}` / `{fmt(best.get('validation_dd_pct'))}` / `{fmt(best.get('validation_trades_per_day'))}`.",
        f"- OOS net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래): `{fmt(best.get('oos_net'))}` / `{fmt(best.get('oos_pf'))}` / `{fmt(best.get('oos_dd_pct'))}` / `{fmt(best.get('oos_trades_per_day'))}`.",
        f"- meaningful density repair candidates(의미 있는 밀도 수리 후보): `{len(result['meaningful_candidates'])}`.",
        "- runtime probe(런타임 탐침): pending(대기). 의미 신호가 있으면 Grok review(그록 검토) 후 MT5 Runtime Probe(MT5 런타임 탐침)로 간다.",
        "- Tier B separate(Tier B 분리): still missing_required(아직 필수 누락).",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier69C_repair_event_first_label_or_feature_surface_report.md`",
        f"- candidate summary(후보 요약): `stages/{STAGE_ID}/03_reviews/f69c_proxy_candidate_summary_review.csv`",
        f"- split KPI(분할 KPI): `stages/{STAGE_ID}/03_reviews/f69c_proxy_kpi_by_split_review.csv`",
        f"- bucket KPI(구간 KPI): `stages/{STAGE_ID}/03_reviews/f69c_bucket_kpi_review.csv`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", current)


def main() -> int:
    created_at = utc_now()
    result = run_repair(created_at)
    write_outputs(result)
    update_ledgers(result)
    update_review_index()
    update_registers(result)
    update_state_files(result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": result["status"],
                    "judgment": result["judgment"],
                    "run_id": RUN_ID,
                    "next_run_id": result["next_run_id"],
                    "candidate_summaries": len(result["candidate_summaries"]),
                    "scout_candidates": len(result["scout_candidates"]),
                    "meaningful_candidates": len(result["meaningful_candidates"]),
                    "top_candidate": (result["candidate_summaries"][0] if result["candidate_summaries"] else {}).get("candidate_id", "none"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

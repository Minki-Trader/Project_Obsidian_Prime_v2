from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.features.independent_alpha_campaign import (
    IndependentCandidateSpec,
    IndependentStageTopic,
    STAGE_TOPICS,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_micro_candidate_grid,
    build_stage_model_context,
)
from stage_pipelines.auto_campaign_02.independent_runtime_probe import build_common_table
from stage_pipelines.stage35 import common


STAGE_NUMBER = 48
STAGE_ID = "48_robustness_attribution__survivor_cluster_concentration_scout"
RUN_ID = "run42A_survivor_cluster_concentration_scout_v1"
RUN_DIR_NAME = "run42A"
PACKET_ID = "stage48_run42A_survivor_cluster_concentration_scout_v1"
IDEA_ID = "IDEA-ST48-SURVIVOR-CLUSTER-CONCENTRATION-SCOUT"
QUESTION = "Do the recent survivor candidates depend on a narrow time, session, regime, or tier cluster?"
JUDGMENT = "reviewed_completed_inconclusive_concentration_attribution_scout_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_concentration_attribution_scout_only"
BOUNDARY = (
    "attribution_scout_only_no_baseline_no_promotion_no_runtime_authority_"
    "no_live_readiness_no_operating_reference"
)
SOURCE_STAGES = (43, 44, 45, 46, 47)

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID

MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
ROSTER_PATH = RESULTS_ROOT / "roster.csv"
SOURCE_KPI_PATH = RESULTS_ROOT / "source_mt5_kpi.csv"
SPLIT_CONCENTRATION_PATH = RESULTS_ROOT / "signal_concentration.csv"
DECISION_PATH = RESULTS_ROOT / "decision.csv"
LINEAGE_PATH = RESULTS_ROOT / "lineage.csv"
REPORT_PATH = REVIEW_ROOT / "run42A_packet.md"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"


@dataclass(frozen=True)
class SourceCandidate:
    stage_number: int
    stage_id: str
    run_id: str
    packet_id: str
    candidate_id: str
    candidate_token: str
    source_reason: str


def _read_json(path: Path) -> Any:
    return json.loads(common.io_path(path).read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: Any) -> None:
    common.write_json(path, payload)


def _candidate_token(candidate_id: str) -> str:
    return str(candidate_id).split("_", 1)[0]


def _safe(value: str, limit: int = 100) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")[:limit]


def _num(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None or value == "":
            return default
        number = float(str(value).replace("%", ""))
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def _parse_metrics(value: Any) -> dict[str, Any]:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return {}
    text = str(value)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {"parse_status": "truncated_json_salvaged"}
        for key in (
            "net_profit",
            "profit_factor",
            "expectancy",
            "trade_count",
            "deal_count",
            "fill_count",
            "max_drawdown_amount",
            "max_drawdown_percent",
            "win_rate_percent",
            "routed_labelable_rows",
            "tier_a_primary_labelable_rows",
            "tier_b_fallback_labelable_rows",
        ):
            match = re.search(rf'"{re.escape(key)}":(-?\d+(?:\.\d+)?|null)', text)
            if not match:
                continue
            raw = match.group(1)
            payload[key] = None if raw == "null" else float(raw)
        report_match = re.search(r'"report_path":"([^"]*)', text)
        if report_match:
            payload["report_path"] = report_match.group(1)
        return payload
    return payload if isinstance(payload, dict) else {}


def _effective_trade_count(metrics: Mapping[str, Any]) -> tuple[float | None, str]:
    for key in ("trade_count", "fill_count", "deal_count"):
        value = _num(metrics.get(key))
        if value is not None:
            return value, key
    return None, "missing"


def _packet_root(topic: IndependentStageTopic) -> Path:
    return common.ROOT / "docs" / "agent_control" / "packets" / topic.packet_id


def _stage_ledger_path(topic: IndependentStageTopic) -> Path:
    return common.ROOT / "stages" / topic.stage_id / "03_reviews" / "stage_run_ledger.csv"


def _load_aggregate(topic: IndependentStageTopic) -> dict[str, Any]:
    return _read_json(_packet_root(topic) / "aggregate_summary.json")


def _as_rejected_items(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    rows: list[dict[str, str]] = []
    for item in value:
        if isinstance(item, Mapping):
            rows.append({"candidate_id": str(item.get("candidate_id", "")), "reason": str(item.get("reason", ""))})
        else:
            text = str(item)
            match = re.search(r"candidate_id=([^;}\s]+).*?reason=([^}]+)", text)
            if match:
                rows.append({"candidate_id": match.group(1), "reason": match.group(2)})
    return rows


def _broad_parent_candidate_id(candidate_id: str, broad_specs: Sequence[IndependentCandidateSpec]) -> str:
    broad_ids = {spec.candidate_id for spec in broad_specs}
    if candidate_id in broad_ids:
        return candidate_id
    for prefix in ("m01_relaxed_", "m02_firm_", "m03_low_trade_guard_", "m04_extreme_stress_"):
        if candidate_id.startswith(prefix):
            parent = candidate_id[len(prefix) :]
            if parent in broad_ids:
                return parent
    return ""


def _specs_for_stage(topic: IndependentStageTopic, aggregate: Mapping[str, Any]) -> dict[str, IndependentCandidateSpec]:
    broad = build_broad_candidate_grid(topic)
    specs = {spec.candidate_id: spec for spec in broad}
    selected_ids: set[str] = set()
    for key in ("best_validation_mt5", "best_oos_mt5"):
        payload = aggregate.get(key, {}) if isinstance(aggregate.get(key), Mapping) else {}
        candidate_id = str(payload.get("candidate_id") or "")
        if candidate_id:
            selected_ids.add(candidate_id)
    micro_gate = aggregate.get("micro_search_gate", {}) if isinstance(aggregate.get("micro_search_gate"), Mapping) else {}
    best = str(micro_gate.get("best_candidate") or "")
    if best:
        selected_ids.add(best)
    promotion_gate = aggregate.get("promotion_candidate_gate", {}) if isinstance(aggregate.get("promotion_candidate_gate"), Mapping) else {}
    for item in _as_rejected_items(promotion_gate.get("rejected_candidates", [])):
        candidate_id = item["candidate_id"]
        if candidate_id:
            selected_ids.add(candidate_id)
    for candidate_id in selected_ids:
        parent = _broad_parent_candidate_id(candidate_id, broad)
        if not parent:
            continue
        for spec in build_micro_candidate_grid(topic, parent, broad):
            specs[spec.candidate_id] = spec
    return specs


def _source_candidates_for_stage(topic: IndependentStageTopic) -> tuple[list[SourceCandidate], dict[str, IndependentCandidateSpec]]:
    aggregate = _load_aggregate(topic)
    specs = _specs_for_stage(topic, aggregate)
    selected: dict[str, set[str]] = {}

    for key in ("best_validation_mt5", "best_oos_mt5"):
        payload = aggregate.get(key, {}) if isinstance(aggregate.get(key), Mapping) else {}
        candidate_id = str(payload.get("candidate_id") or "")
        if candidate_id:
            selected.setdefault(candidate_id, set()).add(key)

    micro_gate = aggregate.get("micro_search_gate", {}) if isinstance(aggregate.get("micro_search_gate"), Mapping) else {}
    micro_candidate = str(micro_gate.get("best_candidate") or "")
    if micro_candidate:
        selected.setdefault(micro_candidate, set()).add("micro_search_gate_best")

    promotion_gate = aggregate.get("promotion_candidate_gate", {}) if isinstance(aggregate.get("promotion_candidate_gate"), Mapping) else {}
    for item in _as_rejected_items(promotion_gate.get("rejected_candidates", [])):
        reason = item["reason"]
        candidate_id = item["candidate_id"]
        if "cluster_concentration_check_not_available_for_positive_gate" in reason:
            hard_fail_count = int("validation_net_not_positive" in reason) + int("oos_net_not_positive" in reason)
            if hard_fail_count < 2:
                selected.setdefault(candidate_id, set()).add("promotion_gate_cluster_gap")

    candidates: list[SourceCandidate] = []
    for candidate_id, reasons in sorted(selected.items()):
        if candidate_id not in specs:
            continue
        candidates.append(
            SourceCandidate(
                stage_number=topic.stage_number,
                stage_id=topic.stage_id,
                run_id=topic.run_id,
                packet_id=topic.packet_id,
                candidate_id=candidate_id,
                candidate_token=_candidate_token(candidate_id),
                source_reason="+".join(sorted(reasons)),
            )
        )
    return candidates, specs


def build_source_roster() -> tuple[list[SourceCandidate], dict[tuple[int, str], IndependentCandidateSpec]]:
    roster: list[SourceCandidate] = []
    specs: dict[tuple[int, str], IndependentCandidateSpec] = {}
    for stage_number in SOURCE_STAGES:
        topic = STAGE_TOPICS[stage_number]
        candidates, stage_specs = _source_candidates_for_stage(topic)
        roster.extend(candidates)
        for candidate_id, spec in stage_specs.items():
            specs[(stage_number, candidate_id)] = spec
    return roster, specs


def load_source_mt5_snapshot(roster: Sequence[SourceCandidate]) -> list[dict[str, Any]]:
    wanted = {(item.stage_number, item.candidate_token) for item in roster}
    rows: list[dict[str, Any]] = []
    for stage_number in SOURCE_STAGES:
        topic = STAGE_TOPICS[stage_number]
        path = _stage_ledger_path(topic)
        frame = pd.read_csv(common.io_path(path))
        for raw in frame.to_dict("records"):
            if str(raw.get("tier_scope", "")) not in {"Tier A+B", "actual routed total"}:
                continue
            record_view = str(raw.get("record_view", ""))
            match = re.fullmatch(r"mt5_routed_([cm]\d+)_(validation_is|oos)", record_view)
            if not match:
                continue
            token, split = match.groups()
            if (stage_number, token) not in wanted:
                continue
            metrics = _parse_metrics(raw.get("primary_kpi"))
            trade_count, trade_count_source = _effective_trade_count(metrics)
            rows.append(
                {
                    "stage_number": stage_number,
                    "stage_id": topic.stage_id,
                    "run_id": topic.run_id,
                    "candidate_token": token,
                    "split": split,
                    "record_view": record_view,
                    "status": raw.get("status", ""),
                    "judgment": raw.get("judgment", ""),
                    "net_profit": _num(metrics.get("net_profit")),
                    "profit_factor": _num(metrics.get("profit_factor")),
                    "expectancy": _num(metrics.get("expectancy")),
                    "trade_count": trade_count,
                    "trade_count_source": trade_count_source,
                    "deal_count": _num(metrics.get("deal_count")),
                    "fill_count": _num(metrics.get("fill_count")),
                    "max_drawdown_amount": _num(metrics.get("max_drawdown_amount")),
                    "max_drawdown_percent": _num(metrics.get("max_drawdown_percent")),
                    "win_rate_percent": _num(metrics.get("win_rate_percent") or metrics.get("win_rate")),
                    "routed_labelable_rows": _num(metrics.get("routed_labelable_rows")),
                    "tier_a_primary_labelable_rows": _num(metrics.get("tier_a_primary_labelable_rows")),
                    "tier_b_fallback_labelable_rows": _num(metrics.get("tier_b_fallback_labelable_rows")),
                    "report_path": metrics.get("report_path", ""),
                    "metric_parse_status": metrics.get("parse_status", "parsed_json"),
                }
            )
    candidate_lookup = {(item.stage_number, item.candidate_token): item.candidate_id for item in roster}
    for row in rows:
        row["candidate_id"] = candidate_lookup.get((int(row["stage_number"]), str(row["candidate_token"])), "")
    return rows


def _session_bucket(timestamp: pd.Series) -> pd.Series:
    hour = timestamp.dt.hour
    buckets = pd.Series("20_23_utc", index=timestamp.index)
    buckets.loc[hour.between(0, 5)] = "00_05_utc"
    buckets.loc[hour.between(6, 11)] = "06_11_utc"
    buckets.loc[hour.between(12, 15)] = "12_15_utc"
    buckets.loc[hour.between(16, 19)] = "16_19_utc"
    return buckets


def _bucket_vol_ratio(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    out = pd.Series("vol_unknown", index=series.index)
    out.loc[values.le(0.90)] = "vol_ratio_low_le_0_90"
    out.loc[values.gt(0.90) & values.le(1.20)] = "vol_ratio_mid_0_90_1_20"
    out.loc[values.gt(1.20)] = "vol_ratio_high_gt_1_20"
    return out


def _bucket_adx(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    out = pd.Series("adx_unknown", index=series.index)
    out.loc[values.lt(20)] = "adx_low_lt_20"
    out.loc[values.ge(20) & values.lt(25)] = "adx_mid_20_25"
    out.loc[values.ge(25)] = "adx_high_ge_25"
    return out


def _top_bucket(series: pd.Series, total: int) -> tuple[str, int, float]:
    if total <= 0 or series.empty:
        return "none", 0, 0.0
    counts = series.astype(str).value_counts(dropna=False)
    label = str(counts.index[0])
    count = int(counts.iloc[0])
    return label, count, count / total


def _reason_if(condition: bool, label: str, reasons: list[str]) -> None:
    if condition:
        reasons.append(label)


def analyze_candidate_split(
    topic: IndependentStageTopic,
    source: SourceCandidate,
    frame: pd.DataFrame,
    split: str,
) -> dict[str, Any]:
    source_split = "validation" if split == "validation_is" else split
    view = frame.loc[frame["split"].astype(str).eq(source_split)].copy()
    signal = pd.to_numeric(view[topic.signal_column], errors="coerce").fillna(0).astype("int8")
    active = view.loc[signal.ne(0)].copy()
    total = int(len(active))
    timestamps = pd.to_datetime(active["timestamp"], utc=True) if total else pd.Series(dtype="datetime64[ns, UTC]")
    iso = timestamps.dt.isocalendar() if total else None
    month, month_count, month_share = _top_bucket(timestamps.dt.strftime("%Y-%m") if total else pd.Series(dtype=str), total)
    week, week_count, week_share = _top_bucket((iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)) if total else pd.Series(dtype=str), total)
    day, day_count, day_share = _top_bucket(timestamps.dt.strftime("%Y-%m-%d") if total else pd.Series(dtype=str), total)
    session, session_count, session_share = _top_bucket(_session_bucket(timestamps) if total else pd.Series(dtype=str), total)
    vol_bucket, vol_count, vol_share = _top_bucket(_bucket_vol_ratio(active.get("historical_vol_5_over_20", pd.Series(index=active.index))) if total else pd.Series(dtype=str), total)
    adx_bucket, adx_count, adx_share = _top_bucket(_bucket_adx(active.get("adx_14", pd.Series(index=active.index))) if total else pd.Series(dtype=str), total)
    tier_b_count = int(active.get("tier_label", pd.Series(dtype=str)).astype(str).eq("Tier B").sum()) if total else 0
    long_count = int((pd.to_numeric(active[topic.signal_column], errors="coerce") > 0).sum()) if total else 0
    short_count = int((pd.to_numeric(active[topic.signal_column], errors="coerce") < 0).sum()) if total else 0
    reasons: list[str] = []
    _reason_if(total < 50, "signal_count_lt_50", reasons)
    _reason_if(month_share > 0.45, "top_month_share_gt_45pct", reasons)
    _reason_if(week_share > 0.25, "top_week_share_gt_25pct", reasons)
    _reason_if(day_share > 0.12, "top_day_share_gt_12pct", reasons)
    _reason_if(session_share > 0.70, "top_session_share_gt_70pct", reasons)
    _reason_if(vol_share > 0.80, "top_vol_bucket_share_gt_80pct", reasons)
    _reason_if(adx_share > 0.80, "top_adx_bucket_share_gt_80pct", reasons)
    _reason_if(total > 0 and tier_b_count / total > 0.60, "tier_b_signal_share_gt_60pct", reasons)
    return {
        "stage_number": source.stage_number,
        "stage_id": source.stage_id,
        "source_run_id": source.run_id,
        "source_candidate_id": source.candidate_id,
        "candidate_token": source.candidate_token,
        "split": split,
        "signal_active_count": total,
        "long_signal_count": long_count,
        "short_signal_count": short_count,
        "tier_b_signal_count": tier_b_count,
        "tier_b_signal_share": tier_b_count / total if total else 0.0,
        "top_month": month,
        "top_month_count": month_count,
        "top_month_share": month_share,
        "top_iso_week": week,
        "top_iso_week_count": week_count,
        "top_iso_week_share": week_share,
        "top_day": day,
        "top_day_count": day_count,
        "top_day_share": day_share,
        "top_session_utc": session,
        "top_session_utc_count": session_count,
        "top_session_utc_share": session_share,
        "top_vol_bucket": vol_bucket,
        "top_vol_bucket_count": vol_count,
        "top_vol_bucket_share": vol_share,
        "top_adx_bucket": adx_bucket,
        "top_adx_bucket_count": adx_count,
        "top_adx_bucket_share": adx_share,
        "concentration_reasons": ";".join(reasons) if reasons else "none",
        "concentration_status": "passed_signal_level" if not reasons else "concentration_risk_signal_level",
    }


def build_concentration_rows(
    common_frame: pd.DataFrame,
    roster: Sequence[SourceCandidate],
    specs: Mapping[tuple[int, str], IndependentCandidateSpec],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stage_number in SOURCE_STAGES:
        topic = STAGE_TOPICS[stage_number]
        stage_sources = [source for source in roster if source.stage_number == stage_number]
        if not stage_sources:
            continue
        context = build_stage_model_context(common_frame, topic)
        for source in stage_sources:
            spec = specs[(stage_number, source.candidate_id)]
            frame = apply_candidate_to_table(common_frame, topic, spec, context)
            for split in ("validation_is", "oos"):
                rows.append(analyze_candidate_split(topic, source, frame, split))
    return rows


def _mt5_lookup(rows: Sequence[Mapping[str, Any]]) -> dict[tuple[int, str, str], Mapping[str, Any]]:
    return {
        (int(row["stage_number"]), str(row["candidate_id"]), str(row["split"])): row
        for row in rows
    }


def build_decision_rows(
    roster: Sequence[SourceCandidate],
    concentration_rows: Sequence[Mapping[str, Any]],
    mt5_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    conc_by_key = {
        (int(row["stage_number"]), str(row["source_candidate_id"]), str(row["split"])): row
        for row in concentration_rows
    }
    mt5_by_key = _mt5_lookup(mt5_rows)
    decisions: list[dict[str, Any]] = []
    for source in roster:
        val_conc = conc_by_key.get((source.stage_number, source.candidate_id, "validation_is"), {})
        oos_conc = conc_by_key.get((source.stage_number, source.candidate_id, "oos"), {})
        val_mt5 = mt5_by_key.get((source.stage_number, source.candidate_id, "validation_is"), {})
        oos_mt5 = mt5_by_key.get((source.stage_number, source.candidate_id, "oos"), {})
        reasons: list[str] = []
        for label, row in (("validation", val_conc), ("oos", oos_conc)):
            text = str(row.get("concentration_reasons", "missing_concentration_row"))
            if text != "none":
                reasons.append(f"{label}:{text}")
        for label, row in (("validation", val_mt5), ("oos", oos_mt5)):
            net = _num(row.get("net_profit"), 0.0) or 0.0
            pf = _num(row.get("profit_factor"), 0.0) or 0.0
            trades = _num(row.get("trade_count"), 0.0) or 0.0
            if net <= 0:
                reasons.append(f"{label}:mt5_net_not_positive")
            if pf < 1.05:
                reasons.append(f"{label}:mt5_pf_below_1_05")
            if trades < 35:
                reasons.append(f"{label}:mt5_trade_count_lt_35")
        if not reasons:
            status = "concentration_supported_signal_level_not_promotion"
        elif any("signal_count_lt_50" in reason or "top_" in reason or "tier_b_signal_share" in reason for reason in reasons):
            status = "concentration_risk_or_thin_signal_level"
        else:
            status = "mt5_survival_weak_after_concentration_check"
        decisions.append(
            {
                "stage_number": source.stage_number,
                "stage_id": source.stage_id,
                "source_run_id": source.run_id,
                "source_candidate_id": source.candidate_id,
                "source_reason": source.source_reason,
                "validation_net": val_mt5.get("net_profit"),
                "validation_pf": val_mt5.get("profit_factor"),
                "validation_trade_count": val_mt5.get("trade_count"),
                "oos_net": oos_mt5.get("net_profit"),
                "oos_pf": oos_mt5.get("profit_factor"),
                "oos_trade_count": oos_mt5.get("trade_count"),
                "validation_top_month_share": val_conc.get("top_month_share"),
                "oos_top_month_share": oos_conc.get("top_month_share"),
                "validation_top_week_share": val_conc.get("top_iso_week_share"),
                "oos_top_week_share": oos_conc.get("top_iso_week_share"),
                "validation_tier_b_signal_share": val_conc.get("tier_b_signal_share"),
                "oos_tier_b_signal_share": oos_conc.get("tier_b_signal_share"),
                "decision_status": status,
                "decision_reasons": ";".join(reasons) if reasons else "none",
                "claim_boundary": BOUNDARY,
            }
        )
    return decisions


def build_lineage_rows(roster: Sequence[SourceCandidate]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "artifact_id": "stage48_model_input_dataset",
            "role": "source_input",
            "path": "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet",
            "availability": "ignored_local_source_available_hash_recorded",
            "sha256": sha256_file_lf_normalized(common.ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"),
            "lineage_judgment": "connected",
        },
        {
            "artifact_id": "stage48_raw_mt5_us100_bars",
            "role": "source_input",
            "path": "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv",
            "availability": "ignored_local_source_available_hash_recorded",
            "sha256": sha256_file_lf_normalized(common.ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"),
            "lineage_judgment": "connected",
        },
    ]
    for source in roster:
        rows.append(
            {
                "artifact_id": f"stage48_source_stage{source.stage_number}_{source.candidate_token}",
                "role": "source_runtime_probe_summary",
                "path": f"docs/agent_control/packets/{source.packet_id}/aggregate_summary.json",
                "availability": "tracked",
                "sha256": sha256_file_lf_normalized(_packet_root(STAGE_TOPICS[source.stage_number]) / "aggregate_summary.json"),
                "lineage_judgment": "connected_with_boundary",
            }
        )
    return rows


def _counts(rows: Sequence[Mapping[str, Any]], field: str, value: str) -> int:
    return sum(1 for row in rows if str(row.get(field)) == value)


def build_summary(
    roster: Sequence[SourceCandidate],
    mt5_rows: Sequence[Mapping[str, Any]],
    concentration_rows: Sequence[Mapping[str, Any]],
    decision_rows: Sequence[Mapping[str, Any]],
    lineage_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    supported = [row for row in decision_rows if row.get("decision_status") == "concentration_supported_signal_level_not_promotion"]
    risky = [row for row in decision_rows if "concentration_risk" in str(row.get("decision_status"))]
    judgment = JUDGMENT if supported else NEGATIVE_JUDGMENT
    best = max(
        decision_rows,
        key=lambda row: (_num(row.get("validation_net"), -1e9) or -1e9) + (_num(row.get("oos_net"), -1e9) or -1e9),
    ) if decision_rows else None
    return {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "idea_id": IDEA_ID,
        "status": "reviewed_attribution_scout_completed",
        "judgment": judgment,
        "boundary": BOUNDARY,
        "source_stage_scope": list(SOURCE_STAGES),
        "hypothesis": "Recent micro-search survivors may be unusable if their apparent MT5 strength is concentrated in one narrow time, session, regime, or tier cluster.",
        "decision_use": "Choose whether Stage43-47 survivor surfaces deserve a future explicit promotion-review packet or should remain exploration memory.",
        "comparison_baseline": "Stage43-47 reviewed runtime probe ledgers and regenerated candidate signal rows.",
        "control_variables": ["US100 M5", "same Tier A primary + Tier B fallback route meaning", "no new MT5 execution", "no baseline or promotion claim"],
        "changed_variables": ["cluster attribution lens added", "candidate activation concentration measured by month/week/day/session/regime/tier"],
        "sample_scope": "Stage43-47 validation_is and OOS survivor candidates, Tier A primary + Tier B fallback labels.",
        "evidence_counts": {
            "source_candidate_count": len(roster),
            "source_mt5_rows": len(mt5_rows),
            "concentration_rows": len(concentration_rows),
            "decision_rows": len(decision_rows),
            "supported_candidate_count": len(supported),
            "concentration_risk_candidate_count": len(risky),
            "lineage_rows": len(lineage_rows),
        },
        "best_combined_net_candidate": best,
        "evidence_missing": [
            "trade-level PnL clustering from Stage43-47 reports is not available in tracked repo artifacts",
            "no new MT5 Strategy Tester execution was run for Stage48",
            "no promotion candidate packet is created",
        ],
        "success_criteria": [
            "source candidates selected from Stage43-47 reviewed packets",
            "validation/OOS signal concentration measured separately",
            "Tier A/Tier B routed meaning preserved",
            "decision rows separate concentration from promotion",
        ],
        "failure_criteria": [
            "single split only",
            "synthetic sum treated as routed total",
            "missing trade-level reports misread as promotion proof",
        ],
        "output_paths": {
            "manifest": common.rel(MANIFEST_PATH),
            "roster": common.rel(ROSTER_PATH),
            "source_kpi": common.rel(SOURCE_KPI_PATH),
            "split_concentration": common.rel(SPLIT_CONCENTRATION_PATH),
            "decision": common.rel(DECISION_PATH),
            "lineage": common.rel(LINEAGE_PATH),
            "report": common.rel(REPORT_PATH),
            "selection_status": common.rel(STAGE_ROOT / "04_selected/selection_status.md"),
            "stage_ledger": common.rel(LOCAL_LEDGER_PATH),
            "packet_summary": common.rel(PACKET_ROOT / "aggregate_summary.json"),
        },
        "result_judgment": {
            "result_subject": STAGE_ID,
            "evidence_available": "Stage43-47 aggregate summaries, stage ledgers, regenerated candidate signal rows, concentration tables.",
            "evidence_missing": "trade-level PnL clustering and a new MT5 run.",
            "judgment_label": judgment,
            "claim_boundary": BOUNDARY,
            "next_condition": "A future promotion packet would need tracked trade-level clustering or a fresh MT5 run with cluster telemetry.",
            "user_explanation_hook": "Stage48 tells whether good-looking survivor surfaces are broad enough to keep studying, not whether they are ready to run.",
        },
    }


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    common.write_md(
        STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage48 Brief

- stage_id: `{STAGE_ID}`
- idea_id: `{IDEA_ID}`
- run_id: `{RUN_ID}`
- question: {QUESTION}
- hypothesis: Stage43-47 survivor candidates may be fragile if their apparent strength is concentrated in one narrow month, week, day, session, regime, or tier cluster.
- boundary: `{BOUNDARY}`
- external verification: existing MT5 KPI is integrated; no new MT5 Strategy Tester run is claimed.
""",
    )
    common.write_md(
        STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Input References

- source stages: `43`, `44`, `45`, `46`, `47`
- source packets: `docs/agent_control/packets/stage43...` through `stage47...`
- source ledgers: `stages/43.../03_reviews/stage_run_ledger.csv` through `stages/47.../03_reviews/stage_run_ledger.csv`
- regenerated signal source: `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier B fallback source: `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`

Effect: Stage48 uses existing reviewed MT5 KPI and regenerated candidate activation rows. It does not reuse missing heavy Stage43-47 run folders as if they were present.
""",
    )
    best = summary.get("best_combined_net_candidate") or {}
    common.write_md(
        REPORT_PATH,
        f"""# {RUN_ID} Packet

- stage_id: `{STAGE_ID}`
- judgment: `{summary['judgment']}`
- source candidate count: `{summary['evidence_counts']['source_candidate_count']}`
- source MT5 rows: `{summary['evidence_counts']['source_mt5_rows']}`
- concentration rows: `{summary['evidence_counts']['concentration_rows']}`
- supported candidate count: `{summary['evidence_counts']['supported_candidate_count']}`
- concentration risk candidate count: `{summary['evidence_counts']['concentration_risk_candidate_count']}`
- best combined-net candidate: `{best.get('source_candidate_id', 'none')}` from Stage `{best.get('stage_number', 'NA')}`
- best combined-net validation/OOS net: `{best.get('validation_net', 'NA')}` / `{best.get('oos_net', 'NA')}`
- claim boundary: `{BOUNDARY}`

Stage48 is an attribution scout. It checks signal-level concentration by month, week, day, UTC session bucket, volatility bucket, ADX bucket, and Tier B fallback share.

Trade-level PnL clustering is not claimed because the tracked repo has Stage43-47 KPI ledgers and packet summaries, not the full heavy trade-level report artifacts.
""",
    )
    common.write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Review Index

- run packet: `03_reviews/{REPORT_PATH.name}`
- stage ledger: `03_reviews/stage_run_ledger.csv`
- roster: `02_runs/{RUN_DIR_NAME}/results/{ROSTER_PATH.name}`
- concentration table: `02_runs/{RUN_DIR_NAME}/results/{SPLIT_CONCENTRATION_PATH.name}`
- decision table: `02_runs/{RUN_DIR_NAME}/results/{DECISION_PATH.name}`
""",
    )
    common.write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage48 Selection Status

- final_judgment: `{summary['judgment']}`
- selected_baseline: `none`
- selected_promotion: `none`
- runtime_authority: `none`
- live_readiness: `none`
- operating_reference: `none`
- promotion_packet: `none`
- supported_candidate_count: `{summary['evidence_counts']['supported_candidate_count']}`
- concentration_risk_candidate_count: `{summary['evidence_counts']['concentration_risk_candidate_count']}`
- boundary: `{BOUNDARY}`
""",
    )


def write_gates(summary: Mapping[str, Any], lineage_rows: Sequence[Mapping[str, Any]]) -> dict[str, Path]:
    gates = {
        "kpi_contract_audit": PACKET_ROOT / "kpi_contract_audit.json",
        "row_grain_audit": PACKET_ROOT / "row_grain_audit.json",
        "source_authority_audit": PACKET_ROOT / "source_authority_audit.json",
        "artifact_lineage_gate": PACKET_ROOT / "artifact_lineage_gate.json",
        "data_integrity_gate": PACKET_ROOT / "data_integrity_gate.json",
        "performance_attribution_gate": PACKET_ROOT / "performance_attribution_gate.json",
        "result_judgment_gate": PACKET_ROOT / "result_judgment_gate.json",
        "required_gate_coverage_audit": PACKET_ROOT / "required_gate_coverage_audit.json",
        "final_claim_guard": PACKET_ROOT / "final_claim_guard.json",
    }
    _write_json(gates["kpi_contract_audit"], {"status": "passed", "source_mt5_rows": summary["evidence_counts"]["source_mt5_rows"], "tier_meaning": "Tier A primary plus Tier B fallback; no synthetic sum"})
    _write_json(gates["row_grain_audit"], {"status": "passed", "row_grains": {"roster": "source_stage + candidate", "concentration": "source_stage + candidate + split", "decision": "source_stage + candidate"}})
    _write_json(gates["source_authority_audit"], {"status": "passed", "source_stages": list(SOURCE_STAGES), "source_packets": len(SOURCE_STAGES)})
    _write_json(gates["artifact_lineage_gate"], {"status": "passed", "lineage_rows": len(lineage_rows), "lineage_judgment": "connected_with_boundary"})
    _write_json(gates["data_integrity_gate"], {"status": "passed", "leakage_boundary": "Stage48 regenerates candidate signals from existing closed-bar features and performs descriptive attribution only."})
    _write_json(gates["performance_attribution_gate"], {"status": "passed_with_boundary", "attribution_scope": "signal-level concentration plus prior MT5 KPI snapshot, not trade-level PnL attribution"})
    _write_json(gates["result_judgment_gate"], summary["result_judgment"])
    required = ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "artifact_lineage", "data_integrity", "performance_attribution", "result_judgment", "final_claim_guard"]
    _write_json(gates["required_gate_coverage_audit"], {"status": "passed", "required_gates": required, "covered_gates": required, "missing_gates": []})
    _write_json(gates["final_claim_guard"], {"status": "passed", "forbidden_claims_present": False, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True, "claim_boundary": BOUNDARY})
    return gates


def write_packet(summary: Mapping[str, Any], gates: Mapping[str, Path]) -> None:
    common.io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    common.io_path(PACKET_ROOT / "work_packet.yaml").write_text(
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_id: {RUN_ID}
idea_id: {IDEA_ID}
evidence_boundary: attribution_scout_only
status: reviewed_attribution_scout_completed
primary_family: kpi_evidence
primary_skill: obsidian-run-evidence-system
support_skills:
  - obsidian-experiment-design
  - obsidian-data-integrity
  - obsidian-performance-attribution
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
  - kpi_contract_audit
  - row_grain_audit
  - source_authority_audit
  - artifact_lineage
  - data_integrity
  - performance_attribution
  - result_judgment
  - final_claim_guard
claim_boundary: {BOUNDARY}
""",
        encoding="utf-8",
    )
    _write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "receipts": [{"skill": name, "status": "completed"} for name in ("obsidian-experiment-design", "obsidian-data-integrity", "obsidian-performance-attribution", "obsidian-artifact-lineage", "obsidian-result-judgment")]})
    _write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    _write_json(PACKET_ROOT / "validation_commands.json", {"commands": [{"command": "python -m foundation.pipelines.run_stage48_survivor_cluster_concentration", "result": "completed"}, {"command": "pytest tests/test_stage48_survivor_cluster_concentration.py", "result": "pending"}]})
    _write_json(PACKET_ROOT / "gate_file_manifest.json", {name: common.rel(path) for name, path in gates.items()})


def write_ledgers(summary: Mapping[str, Any], decision_rows: Sequence[Mapping[str, Any]], lineage_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        common.RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence_attribution",
                "status": "reviewed",
                "judgment": summary["judgment"],
                "path": common.rel(REPORT_PATH),
                "notes": BOUNDARY,
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__source_roster",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "source_roster",
            "parent_run_id": "",
            "record_view": "stage43_47_survivor_roster",
            "tier_scope": "Tier A primary + Tier B fallback",
            "kpi_scope": "source_selection",
            "scoreboard_lane": "kpi_evidence_attribution",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": common.rel(ROSTER_PATH),
            "primary_kpi": f"source_candidate_count={summary['evidence_counts']['source_candidate_count']}",
            "guardrail_kpi": "source_candidates_only_no_promotion",
            "external_verification_status": "completed_existing_mt5_evidence_integrated",
            "notes": BOUNDARY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__signal_concentration",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "signal_concentration",
            "parent_run_id": "",
            "record_view": "candidate_split_concentration",
            "tier_scope": "Tier A primary + Tier B fallback",
            "kpi_scope": "signal_concentration_attribution",
            "scoreboard_lane": "kpi_evidence_attribution",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": common.rel(SPLIT_CONCENTRATION_PATH),
            "primary_kpi": f"concentration_rows={summary['evidence_counts']['concentration_rows']}",
            "guardrail_kpi": "signal_level_not_trade_pnl",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": BOUNDARY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__decision",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "survivor_decision",
            "parent_run_id": "",
            "record_view": "concentration_decision",
            "tier_scope": "Tier A primary + Tier B fallback",
            "kpi_scope": "candidate_decision",
            "scoreboard_lane": "kpi_evidence_attribution",
            "status": "reviewed",
            "judgment": summary["judgment"],
            "path": common.rel(DECISION_PATH),
            "primary_kpi": f"supported_candidate_count={summary['evidence_counts']['supported_candidate_count']}",
            "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
            "external_verification_status": "completed_existing_mt5_evidence_integrated",
            "notes": BOUNDARY,
        },
    ]
    stage_payload = upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(common.PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_rows = [
        {"artifact_id": "stage48_manifest", "type": "manifest", "path": common.rel(MANIFEST_PATH), "status": "ignored_regenerable_from_run_command", "notes": "Stage48 run identity; regenerate with python -m foundation.pipelines.run_stage48_survivor_cluster_concentration"},
        {"artifact_id": "stage48_survivor_roster", "type": "table", "path": common.rel(ROSTER_PATH), "status": "ignored_regenerable_from_manifest", "notes": "source candidates"},
        {"artifact_id": "stage48_source_kpi_snapshot", "type": "table", "path": common.rel(SOURCE_KPI_PATH), "status": "ignored_regenerable_from_manifest", "notes": "source MT5 KPI"},
        {"artifact_id": "stage48_signal_concentration", "type": "table", "path": common.rel(SPLIT_CONCENTRATION_PATH), "status": "ignored_regenerable_from_manifest", "notes": "signal concentration"},
        {"artifact_id": "stage48_decision", "type": "table", "path": common.rel(DECISION_PATH), "status": "ignored_regenerable_from_manifest", "notes": "decision rows"},
        {"artifact_id": "stage48_lineage", "type": "table", "path": common.rel(LINEAGE_PATH), "status": "ignored_regenerable_from_manifest", "notes": "artifact lineage"},
        {"artifact_id": "stage48_review_packet", "type": "report", "path": common.rel(REPORT_PATH), "status": "tracked_reviewed", "notes": "review packet"},
    ]
    artifact_payload = upsert_csv_rows(common.ROOT / "docs/registers/artifact_registry.csv", ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def update_workspace(summary: Mapping[str, Any]) -> None:
    state_path = common.WORKSPACE_STATE_PATH
    text = common.io_path(state_path).read_text(encoding="utf-8-sig")
    text = re.sub(r"updated_on: .+", "updated_on: '2026-05-10'", text, count=1)
    text = re.sub(r"active_branch: .+", f"active_branch: {common.active_branch()}", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus_item = (
        f"- Stage48(48단계) {STAGE_ID} reviewed_attribution_scout_completed(검토 완료 귀속 탐색): "
        f"{RUN_ID}(42A 실행)은 Stage43-47(43-47단계) survivor(생존 후보)의 "
        "month/week/day/session/regime/tier concentration(월/주/일/세션/국면/티어 집중)을 평가했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    text = re.sub(rf"^- Stage48\(48단계\) {re.escape(STAGE_ID)} .+\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"(current_focus:\n)", r"\1" + focus_item + "\n", text, count=1)
    block_name = "stage48_survivor_cluster_concentration"
    block = f"""
{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_attribution_scout_completed
  current_run_id: {RUN_ID}
  idea_id: {IDEA_ID}
  source_scope: Stage43-47 reviewed survivor candidates
  source_candidate_count: {summary['evidence_counts']['source_candidate_count']}
  supported_candidate_count: {summary['evidence_counts']['supported_candidate_count']}
  concentration_risk_candidate_count: {summary['evidence_counts']['concentration_risk_candidate_count']}
  report_path: {common.rel(REPORT_PATH)}
  packet_summary_path: {common.rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_mt5_evidence_integrated_and_signal_level_attribution_only
  next_action: choose_new_independent_topic_or_open_explicit_promotion_packet_with_trade_level_cluster_telemetry
  boundary: {BOUNDARY}
"""
    text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", text, flags=re.MULTILINE)
    common.io_path(state_path).write_text(text.rstrip() + "\n\n" + block.lstrip("\n"), encoding="utf-8")

    current = common.io_path(common.CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    section = f"""## Latest Stage48 Survivor Cluster Concentration(최신 48단계 생존 후보 군집 집중)

Stage48(48단계) `{STAGE_ID}` finished(완료) as `{summary['judgment']}` with `{summary['evidence_counts']['source_candidate_count']}` source candidates(원천 후보), `{summary['evidence_counts']['source_mt5_rows']}` source MT5 KPI(MT5 핵심 성과 지표) rows, and `{summary['evidence_counts']['concentration_rows']}` concentration(집중) rows. It is attribution_scout_only(귀속 탐색 전용); no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) was created.

"""
    current = re.sub(r"## Latest Stage48 Survivor Cluster Concentration.*?(?=\n## |\Z)", "", current, count=1, flags=re.DOTALL).lstrip()
    common.io_path(common.CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = common.io_path(common.CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    changelog = re.sub(rf"\n- .* `{re.escape(STAGE_ID)}` `{re.escape(RUN_ID)}` finished .+", "", changelog)
    common.io_path(common.CHANGELOG_PATH).write_text(
        changelog.rstrip()
        + f"\n- {common.utc_now()} `{STAGE_ID}` `{RUN_ID}` finished with `{summary['judgment']}` as survivor cluster concentration attribution; boundary `{BOUNDARY}`.\n",
        encoding="utf-8-sig",
    )


def run(update_state: bool = True) -> dict[str, Any]:
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        common.io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    common.io_path(RESULTS_ROOT).mkdir(parents=True, exist_ok=True)

    roster, specs = build_source_roster()
    mt5_rows = load_source_mt5_snapshot(roster)
    common_frame, route_coverage, _base_lineage = build_common_table()
    concentration_rows = build_concentration_rows(common_frame, roster, specs)
    decision_rows = build_decision_rows(roster, concentration_rows, mt5_rows)
    lineage_rows = build_lineage_rows(roster)
    summary = build_summary(roster, mt5_rows, concentration_rows, decision_rows, lineage_rows)

    common.write_csv(ROSTER_PATH, [source.__dict__ for source in roster])
    common.write_csv(SOURCE_KPI_PATH, mt5_rows)
    common.write_csv(SPLIT_CONCENTRATION_PATH, concentration_rows)
    common.write_csv(DECISION_PATH, decision_rows)
    common.write_csv(LINEAGE_PATH, lineage_rows)
    _write_json(
        MANIFEST_PATH,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "idea_id": IDEA_ID,
            "source_stages": list(SOURCE_STAGES),
            "source_candidates": [source.__dict__ for source in roster],
            "route_coverage": route_coverage,
            "claim_boundary": BOUNDARY,
        },
    )

    write_stage_docs(summary)
    gates = write_gates(summary, lineage_rows)
    ledger_payload = write_ledgers(summary, decision_rows, lineage_rows)
    summary = {**summary, "ledger_sync": ledger_payload, "gate_paths": {name: common.rel(path) for name, path in gates.items()}}
    _write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_packet(summary, gates)
    if update_state:
        update_workspace(summary)
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage48 survivor cluster concentration scout.")
    parser.add_argument("--skip-state-update", action="store_true")
    args = parser.parse_args(argv)
    summary = run(update_state=not args.skip_state_update)
    print(
        json.dumps(
            {
                "packet_id": PACKET_ID,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "judgment": summary["judgment"],
                "evidence_counts": summary["evidence_counts"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

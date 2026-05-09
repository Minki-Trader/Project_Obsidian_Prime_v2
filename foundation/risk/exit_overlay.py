from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


STAGE39_FEATURE_ORDER = (
    "stage39_base_entry_signal",
    "stage39_close_long_overlay",
    "stage39_close_short_overlay",
    "stage39_overlay_max_hold_bars",
)


@dataclass(frozen=True)
class ExitOverlayCandidateSpec:
    candidate_id: str
    label: str
    enabled_surfaces: tuple[str, ...]
    exit_overlay_rule: str
    hold_override_rule: str = "none"
    direction_specific_rule: str = "both_directions"
    fallback_rule: str = "Tier A primary + Tier B fallback"
    threshold_family: str = "loose_v1"
    min_hold_bars: int = 0
    dynamic_max_hold_bars: int = 0
    long_enabled: bool = True
    short_enabled: bool = True
    adverse_excursion_proxy_required: bool = False
    threshold_overrides: Mapping[str, float] = field(default_factory=dict)


def finite_quantile(values: pd.Series, q: float, fallback: float) -> float:
    series = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if series.empty:
        return float(fallback)
    return float(series.quantile(float(q)))


def build_loose_thresholds(common: pd.DataFrame) -> dict[str, float]:
    train = common.loc[common["split"].astype(str).eq("train") & ~common["stage39_surface_missing"]]
    return {
        "survival_risk_min": finite_quantile(train["stage24_survival_risk_z"], 0.70, 0.50),
        "hazard_risk_min": finite_quantile(train["stage25_hazard_risk_z"], 0.70, 0.50),
        "tail_pressure_min": finite_quantile(train["stage27_tail_pressure"], 0.70, 0.005),
        "adverse_excursion_proxy_min": finite_quantile(train["stage27_tail_pressure"], 0.82, 0.008),
        "survival_long_min": finite_quantile(train["stage24_survival_risk_z"], 0.68, 0.45),
        "survival_short_min": finite_quantile(train["stage24_survival_risk_z"], 0.76, 0.65),
        "hazard_long_min": finite_quantile(train["stage25_hazard_risk_z"], 0.68, 0.45),
        "hazard_short_min": finite_quantile(train["stage25_hazard_risk_z"], 0.76, 0.65),
        "tail_long_min": finite_quantile(train["stage27_tail_pressure"], 0.68, 0.005),
        "tail_short_min": finite_quantile(train["stage27_tail_pressure"], 0.76, 0.007),
    }


def build_broad_candidate_grid() -> list[ExitOverlayCandidateSpec]:
    return [
        ExitOverlayCandidateSpec("c01_no_overlay_reference", "base/carry reference without Stage39 overlay", (), "none"),
        ExitOverlayCandidateSpec("c02_survival_clock_exit", "survival clock exit", ("survival",), "close when survival risk is high"),
        ExitOverlayCandidateSpec("c03_hazard_lifecycle_exit", "hazard lifecycle exit", ("hazard",), "close when hazard risk is high"),
        ExitOverlayCandidateSpec("c04_tail_pressure_exit", "tail pressure exit", ("tail",), "close when tail pressure is high"),
        ExitOverlayCandidateSpec("c05_survival_hazard_exit", "survival + hazard exit", ("survival", "hazard"), "close on survival and hazard overlap"),
        ExitOverlayCandidateSpec("c06_survival_tail_exit", "survival + tail exit", ("survival", "tail"), "close on survival and tail overlap"),
        ExitOverlayCandidateSpec("c07_hazard_tail_exit", "hazard + tail exit", ("hazard", "tail"), "close on hazard and tail overlap"),
        ExitOverlayCandidateSpec("c08_survival_hazard_tail_exit", "survival + hazard + tail exit", ("survival", "hazard", "tail"), "close on all risk surfaces"),
        ExitOverlayCandidateSpec("c09_hazard_tail_after_min_hold", "hazard + tail after min hold", ("hazard", "tail"), "close on hazard and tail after min hold", min_hold_bars=6),
        ExitOverlayCandidateSpec("c10_survival_after_min_hold", "survival after min hold", ("survival",), "close on survival after min hold", min_hold_bars=6),
        ExitOverlayCandidateSpec("c11_tail_only_after_adverse_excursion_proxy", "tail after adverse excursion proxy", ("tail",), "close on tail only after adverse excursion proxy", adverse_excursion_proxy_required=True),
        ExitOverlayCandidateSpec("c12_hazard_only_after_adverse_excursion_proxy", "hazard after adverse excursion proxy", ("hazard",), "close on hazard only after adverse excursion proxy", adverse_excursion_proxy_required=True),
        ExitOverlayCandidateSpec("c13_reduce_max_hold_on_hazard", "reduce max hold on hazard", ("hazard",), "none", hold_override_rule="max_hold_6_when_hazard", dynamic_max_hold_bars=6),
        ExitOverlayCandidateSpec("c14_reduce_max_hold_on_tail", "reduce max hold on tail", ("tail",), "none", hold_override_rule="max_hold_6_when_tail", dynamic_max_hold_bars=6),
        ExitOverlayCandidateSpec("c15_long_only_lifecycle_exit", "long-only lifecycle/tail exit", ("hazard", "tail"), "close long positions only on hazard or tail", direction_specific_rule="long_only", short_enabled=False),
        ExitOverlayCandidateSpec("c16_short_only_lifecycle_exit", "short-only lifecycle/tail exit", ("hazard", "tail"), "close short positions only on hazard or tail", direction_specific_rule="short_only", long_enabled=False),
        ExitOverlayCandidateSpec("c17_direction_specific_lifecycle_tail_exit", "direction-specific lifecycle/tail exit", ("hazard", "tail"), "long and short use separate loose thresholds", direction_specific_rule="direction_specific"),
    ]


def candidate_thresholds(base: Mapping[str, float], spec: ExitOverlayCandidateSpec) -> dict[str, float]:
    thresholds = {key: float(value) for key, value in base.items()}
    thresholds.update({key: float(value) for key, value in spec.threshold_overrides.items()})
    return thresholds


def risk_masks(frame: pd.DataFrame, thresholds: Mapping[str, float]) -> dict[str, pd.Series]:
    return {
        "survival": pd.to_numeric(frame["stage24_survival_risk_z"], errors="coerce").ge(float(thresholds["survival_risk_min"])),
        "hazard": pd.to_numeric(frame["stage25_hazard_risk_z"], errors="coerce").ge(float(thresholds["hazard_risk_min"])),
        "tail": pd.to_numeric(frame["stage27_tail_pressure"], errors="coerce").ge(float(thresholds["tail_pressure_min"])),
        "adverse": pd.to_numeric(frame["stage27_tail_pressure"], errors="coerce").ge(float(thresholds["adverse_excursion_proxy_min"])),
        "long_hazard_tail": (
            pd.to_numeric(frame["stage25_hazard_risk_z"], errors="coerce").ge(float(thresholds["hazard_long_min"]))
            | pd.to_numeric(frame["stage27_tail_pressure"], errors="coerce").ge(float(thresholds["tail_long_min"]))
        ),
        "short_hazard_tail": (
            pd.to_numeric(frame["stage25_hazard_risk_z"], errors="coerce").ge(float(thresholds["hazard_short_min"]))
            | pd.to_numeric(frame["stage27_tail_pressure"], errors="coerce").ge(float(thresholds["tail_short_min"]))
        ),
    }


def apply_exit_overlay_candidate(
    common: pd.DataFrame,
    spec: ExitOverlayCandidateSpec,
    base_thresholds: Mapping[str, float],
) -> pd.DataFrame:
    thresholds = candidate_thresholds(base_thresholds, spec)
    masks = risk_masks(common, thresholds)
    risk_active = pd.Series(False, index=common.index)
    if spec.candidate_id == "c01_no_overlay_reference":
        risk_active = pd.Series(False, index=common.index)
    elif spec.direction_specific_rule == "direction_specific":
        risk_active = masks["long_hazard_tail"] | masks["short_hazard_tail"]
    elif spec.candidate_id in {"c15_long_only_lifecycle_exit", "c16_short_only_lifecycle_exit"}:
        risk_active = masks["hazard"] | masks["tail"]
    elif spec.enabled_surfaces:
        risk_active = pd.Series(True, index=common.index)
        for name in spec.enabled_surfaces:
            risk_active &= masks[name]

    if spec.adverse_excursion_proxy_required:
        risk_active &= masks["adverse"]
    risk_active &= ~common["stage39_surface_missing"].astype(bool)

    base_signal = pd.to_numeric(common["stage39_base_entry_signal"], errors="coerce").fillna(0).astype(int)
    out = common.copy()
    out["candidate_id"] = spec.candidate_id
    out["candidate_label"] = spec.label
    out["enabled_surfaces"] = "+".join(spec.enabled_surfaces) if spec.enabled_surfaces else "none"
    out["exit_overlay_rule"] = spec.exit_overlay_rule
    out["hold_override_rule"] = spec.hold_override_rule
    out["direction_specific_rule"] = spec.direction_specific_rule
    out["fallback_rule"] = spec.fallback_rule
    out["threshold_family"] = spec.threshold_family
    out["min_hold_bars"] = int(spec.min_hold_bars)
    for key, value in thresholds.items():
        out[key] = float(value)
    out["surface_survival_pass"] = masks["survival"].to_numpy()
    out["surface_hazard_pass"] = masks["hazard"].to_numpy()
    out["surface_tail_pass"] = masks["tail"].to_numpy()
    out["adverse_excursion_proxy_active"] = masks["adverse"].to_numpy()
    out["overlay_risk_active"] = risk_active.to_numpy()
    out[STAGE39_FEATURE_ORDER[0]] = base_signal.to_numpy(dtype="int32")
    close_long = risk_active & bool(spec.long_enabled)
    close_short = risk_active & bool(spec.short_enabled)
    if spec.direction_specific_rule == "direction_specific":
        close_long = masks["long_hazard_tail"] & ~common["stage39_surface_missing"].astype(bool)
        close_short = masks["short_hazard_tail"] & ~common["stage39_surface_missing"].astype(bool)
    if spec.dynamic_max_hold_bars > 0:
        out[STAGE39_FEATURE_ORDER[1]] = 0
        out[STAGE39_FEATURE_ORDER[2]] = 0
        out[STAGE39_FEATURE_ORDER[3]] = np.where(risk_active, int(spec.dynamic_max_hold_bars), 0).astype("int32")
    else:
        out[STAGE39_FEATURE_ORDER[1]] = close_long.astype("int32")
        out[STAGE39_FEATURE_ORDER[2]] = close_short.astype("int32")
        out[STAGE39_FEATURE_ORDER[3]] = 0
    out["entry_decision"] = np.where(base_signal.gt(0), "long", np.where(base_signal.lt(0), "short", "flat"))
    return out


def entry_count_stability(reference: pd.DataFrame, candidate: pd.DataFrame, *, signal_column: str = STAGE39_FEATURE_ORDER[0]) -> dict[str, Any]:
    ref_count = int(pd.to_numeric(reference[signal_column], errors="coerce").fillna(0).ne(0).sum())
    candidate_count = int(pd.to_numeric(candidate[signal_column], errors="coerce").fillna(0).ne(0).sum())
    return {
        "reference_entry_signal_count": ref_count,
        "candidate_entry_signal_count": candidate_count,
        "entry_count_delta": candidate_count - ref_count,
        "stable": candidate_count == ref_count,
    }


def summarize_candidate_frames(candidate_frames: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    reference = candidate_frames["c01_no_overlay_reference"]
    rows: list[dict[str, Any]] = []
    for candidate_id, frame in candidate_frames.items():
        for split in ("validation", "oos"):
            view = frame.loc[frame["split"].astype(str).eq(split)].copy()
            ref_view = reference.loc[reference["split"].astype(str).eq(split)]
            stability = entry_count_stability(ref_view, view)
            tier_a = view.loc[view["tier_label"].astype(str).eq("Tier A")]
            tier_b = view.loc[view["tier_label"].astype(str).eq("Tier B")]
            risk_active = view["overlay_risk_active"].astype(bool) if "overlay_risk_active" in view.columns else pd.Series(False, index=view.index)
            signal = pd.to_numeric(view[STAGE39_FEATURE_ORDER[0]], errors="coerce").fillna(0).astype(int)
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": str(view["candidate_label"].iloc[0]) if not view.empty else "",
                    "split": "validation_is" if split == "validation" else split,
                    "enabled_surfaces": str(view["enabled_surfaces"].iloc[0]) if not view.empty else "",
                    "exit_overlay_rule": str(view["exit_overlay_rule"].iloc[0]) if not view.empty else "",
                    "hold_override_rule": str(view["hold_override_rule"].iloc[0]) if not view.empty else "",
                    "direction_specific_rule": str(view["direction_specific_rule"].iloc[0]) if not view.empty else "",
                    "fallback_rule": str(view["fallback_rule"].iloc[0]) if not view.empty else "",
                    "tier_a_used_count": int(tier_a[STAGE39_FEATURE_ORDER[0]].ne(0).sum()),
                    "tier_b_fallback_used_count": int(tier_b[STAGE39_FEATURE_ORDER[0]].ne(0).sum()),
                    "actual_routed_total_count": int(signal.ne(0).sum()),
                    "validation_trade_count": int(signal.ne(0).sum()) if split == "validation" else "",
                    "oos_trade_count": int(signal.ne(0).sum()) if split == "oos" else "",
                    "entry_count_delta_vs_reference": int(stability["entry_count_delta"]),
                    "base_entry_count_stable": bool(stability["stable"]),
                    "exit_count": int((view[STAGE39_FEATURE_ORDER[1]].astype(int).ne(0) | view[STAGE39_FEATURE_ORDER[2]].astype(int).ne(0)).sum()),
                    "early_exit_count": int((view[STAGE39_FEATURE_ORDER[1]].astype(int).ne(0) | view[STAGE39_FEATURE_ORDER[2]].astype(int).ne(0)).sum()),
                    "overlay_activation_rate_py": float(risk_active.mean()) if len(view) else 0.0,
                    "no_trade_rate": float(1.0 - signal.ne(0).mean()) if len(view) else 1.0,
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "candidate_rejection_reason": "mt5_pending",
                }
            )
    return rows


def hold_metrics_from_actions(actions: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    hold_lengths: list[int] = []
    open_index: int | None = None
    entry_count = 0
    close_count = 0
    overlay_close_count = 0
    for index, row in enumerate(actions):
        action = str(row.get("exec_action", "") or row.get("action", ""))
        before = str(row.get("position_before", ""))
        if action in {"open_long", "open_short"}:
            open_index = index
            entry_count += 1
        elif action in {"reverse_open_long", "reverse_open_short"}:
            if open_index is not None and before != "none":
                hold_lengths.append(max(index - open_index, 0))
                close_count += 1
            open_index = index
            entry_count += 1
        elif action.startswith("close_"):
            if open_index is not None:
                hold_lengths.append(max(index - open_index, 0))
                open_index = None
            close_count += 1
            if "exit_overlay" in action:
                overlay_close_count += 1
    arr = np.asarray(hold_lengths, dtype="float64")
    return {
        "entry_count_runtime": int(entry_count),
        "exit_count_runtime": int(close_count),
        "early_exit_count_runtime": int(overlay_close_count),
        "average_hold_bars": float(arr.mean()) if arr.size else None,
        "median_hold_bars": float(np.median(arr)) if arr.size else None,
        "p90_hold_bars": float(np.quantile(arr, 0.90)) if arr.size else None,
        "max_hold_bars": int(arr.max()) if arr.size else None,
    }


def rejection_reason(row: Mapping[str, Any], reference: Mapping[str, Any] | None = None) -> str:
    if row.get("tester_status") not in {None, "", "completed"}:
        return "mt5_execution_not_completed"
    if int(float(row.get("entry_count_delta_runtime_vs_reference") or 0)) != 0:
        return "entry_count_changed_by_exit_reentry_mechanics_documented_exception"
    trade_count = int(float(row.get("trade_count") or 0))
    if trade_count < 20:
        return "trade_count_too_thin"
    activation = float(row.get("overlay_activation_rate_mt5") or row.get("overlay_activation_rate_py") or 0.0)
    if str(row.get("candidate_id")) != "c01_no_overlay_reference" and activation <= 0.0:
        return "overlay_activation_trivially_zero"
    pf = row.get("profit_factor")
    try:
        if pf is not None and float(pf) < 0.80:
            return "profit_factor_collapse"
    except (TypeError, ValueError):
        pass
    if reference:
        try:
            ref_trades = max(int(float(reference.get("trade_count") or 0)), 1)
            if trade_count / ref_trades < 0.50:
                return "trade_stream_destroyed_vs_reference"
        except (TypeError, ValueError):
            pass
    return "candidate_survived_basic_rejection_checks"

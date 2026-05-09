from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np
import pandas as pd

from stage_pipelines.stage35 import atlas_model, common


MaskBuilder = Callable[[pd.DataFrame], pd.Series]


@dataclass(frozen=True)
class SweepVariant:
    variant_id: str
    family: str
    description: str
    mask_builder: MaskBuilder
    splits: tuple[str, ...] = ("validation", "oos")


def _between(column: str, left: float, right: float) -> MaskBuilder:
    def mask(frame: pd.DataFrame) -> pd.Series:
        value = pd.to_numeric(frame[column], errors="coerce")
        return value.ge(left) & value.lt(right)

    return mask


def _state_mask(topic_id: str, state_id: int, *, no_oct2025: bool = False) -> MaskBuilder:
    column = f"state_{topic_id}"

    def mask(frame: pd.DataFrame) -> pd.Series:
        out = frame[column].astype(int).eq(int(state_id))
        if no_oct2025:
            month = pd.to_datetime(frame["timestamp"], utc=True).dt.strftime("%Y-%m")
            out &= ~month.eq("2025-10")
        return out

    return mask


def session_variants() -> list[SweepVariant]:
    return [
        SweepVariant("session_cash_open_0_30", "session_timing", "cash open 0-30m", _between("minutes_from_cash_open", 0, 30)),
        SweepVariant("session_cash_open_30_90", "session_timing", "cash open 30-90m", _between("minutes_from_cash_open", 30, 90)),
        SweepVariant("session_cash_open_90_180", "session_timing", "cash open 90-180m", _between("minutes_from_cash_open", 90, 180)),
        SweepVariant("session_cash_mid_180_330", "session_timing", "cash mid 180-330m", _between("minutes_from_cash_open", 180, 330)),
        SweepVariant("session_cash_late_30", "session_timing", "cash late 30m", lambda frame: frame["is_last_30m_before_cash_close"].astype(float).gt(0.5)),
        SweepVariant("session_cash_only", "session_timing", "cash session only", lambda frame: frame["is_us_cash_open"].astype(float).gt(0.5)),
        SweepVariant("session_non_cash_only", "session_timing", "non-cash only", lambda frame: frame["is_us_cash_open"].astype(float).lt(0.5)),
    ]


def atlas_state_variants(assignments: pd.DataFrame) -> list[SweepVariant]:
    variants: list[SweepVariant] = []
    for topic_id, family in (("return_volatility_shape", "return_volatility"), ("trend_momentum_pressure", "trend_momentum")):
        states = sorted(int(value) for value in assignments[f"state_{topic_id}"].dropna().unique())
        for state_id in states:
            variants.append(
                SweepVariant(
                    f"{topic_id}_state{state_id}",
                    family,
                    f"{topic_id} state {state_id}",
                    _state_mask(topic_id, state_id),
                )
            )
    variants.extend(
        [
            SweepVariant(
                "return_volatility_shape_state0_no_oct2025",
                "return_volatility_drift",
                "return volatility selected state without 2025-10",
                _state_mask("return_volatility_shape", 0, no_oct2025=True),
                ("oos",),
            ),
            SweepVariant(
                "trend_momentum_pressure_state4_no_oct2025",
                "trend_momentum_drift",
                "trend momentum selected state without 2025-10",
                _state_mask("trend_momentum_pressure", 4, no_oct2025=True),
                ("oos",),
            ),
        ]
    )
    return variants


def choose_direction(frame: pd.DataFrame, mask: pd.Series) -> str:
    validation = frame.loc[frame["split"].astype(str).eq("validation") & mask].copy()
    if validation.empty:
        return "long"
    returns = validation["future_log_return_12"].astype(float).to_numpy()
    long_pf = common.profit_factor(returns)
    short_pf = common.profit_factor(-returns)
    long_net = float(np.nansum(returns))
    short_net = float(np.nansum(-returns))
    long_score = (common.numeric(long_pf, -999.0), long_net)
    short_score = (common.numeric(short_pf, -999.0), short_net)
    return "short" if short_score > long_score else "long"


def metrics_for(frame: pd.DataFrame, mask: pd.Series, direction: str, split_name: str) -> dict[str, object]:
    split = frame.loc[frame["split"].astype(str).eq(split_name) & mask].copy()
    sign = 1.0 if direction == "long" else -1.0
    returns = (split["future_log_return_12"].astype(float) * sign).to_numpy()
    return {
        "row_count": int(len(split)),
        "net_return_proxy": round(float(np.nansum(returns)), 10) if len(returns) else 0.0,
        "profit_factor_proxy": common.profit_factor(returns),
    }


def build_variants() -> tuple[pd.DataFrame, list[dict[str, object]]]:
    atlas = atlas_model.build_atlas()
    frame = atlas["frame"]
    definitions = session_variants() + atlas_state_variants(frame)
    rows: list[dict[str, object]] = []
    for variant in definitions:
        mask = variant.mask_builder(frame)
        direction = choose_direction(frame, mask)
        row: dict[str, object] = {
            "variant_id": variant.variant_id,
            "family": variant.family,
            "description": variant.description,
            "direction": direction,
            "splits": list(variant.splits),
        }
        for split_name in ("validation", "oos"):
            metrics = metrics_for(frame, mask, direction, split_name)
            for key, value in metrics.items():
                row[f"{split_name}_{key}"] = value
        row["worth_gate"] = "included_all_worthwhile_stage35_axes"
        rows.append(row)
    return frame, rows


def variant_mask(frame: pd.DataFrame, variant_id: str) -> pd.Series:
    definitions = {variant.variant_id: variant for variant in session_variants() + atlas_state_variants(frame)}
    return definitions[variant_id].mask_builder(frame)


__all__ = [
    "SweepVariant",
    "atlas_state_variants",
    "build_variants",
    "choose_direction",
    "metrics_for",
    "session_variants",
    "variant_mask",
]

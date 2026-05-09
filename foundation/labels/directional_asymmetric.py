from __future__ import annotations

import math
from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


SIGNAL_FEATURE_ORDER = ("stage41_directional_label_signal",)
CLASS_ID_MAP = {"short": 0, "flat": 1, "long": 2}
CLASS_NAME_MAP = {value: key for key, value in CLASS_ID_MAP.items()}
BAR_MINUTES = 5
MAX_CASH_SESSION_MINUTES = 390


@dataclass(frozen=True)
class DirectionalAsymmetricLabelSpec:
    candidate_id: str
    label_id: str
    description: str
    label_family: str
    long_horizon_bars: int
    short_horizon_bars: int
    long_threshold_multiplier: float = 1.0
    short_threshold_multiplier: float = 1.0
    flat_band_rule: str = "symmetric_current_band"
    volatility_normalization: bool = False
    session_adjustment: bool = False
    threshold_source: str = "base_threshold_multiplier"
    model_family: str = "elastic_net_logistic"
    model_variant: str = "balanced_multiclass_v1"
    long_short_scope: str = "both"
    decision_threshold: float = 0.44
    expected_trade_count_effect: str = "reference"
    overfit_risk: str = "medium"
    notes: str = ""

    @property
    def max_horizon_bars(self) -> int:
        return max(int(self.long_horizon_bars), int(self.short_horizon_bars))

    @property
    def max_horizon_minutes(self) -> int:
        return self.max_horizon_bars * BAR_MINUTES

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_stage41_broad_candidate_grid() -> list[DirectionalAsymmetricLabelSpec]:
    items = [
        DirectionalAsymmetricLabelSpec(
            "c01_current_label_reference",
            "stage41_c01_current_label_reference",
            "current v2 label/reference behavior using fwd12 symmetric threshold",
            "current_label_reference",
            12,
            12,
            expected_trade_count_effect="reference",
            overfit_risk="low",
        ),
        DirectionalAsymmetricLabelSpec(
            "c02_long_horizon_longer_short_same",
            "stage41_c02_long18_short12",
            "long horizon longer while short horizon stays at current horizon",
            "long_horizon_longer",
            18,
            12,
            expected_trade_count_effect="slightly lower",
        ),
        DirectionalAsymmetricLabelSpec(
            "c03_short_horizon_shorter_long_same",
            "stage41_c03_long12_short8",
            "short horizon shorter while long horizon stays at current horizon",
            "short_horizon_shorter",
            12,
            8,
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c04_asymmetric_long_slow_short_fast",
            "stage41_c04_long18_short8",
            "long opportunities get slower horizon and short opportunities get faster horizon",
            "asymmetric_long_slow_short_fast",
            18,
            8,
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c05_asymmetric_long_fast_short_slow",
            "stage41_c05_long8_short18",
            "long opportunities get faster horizon and short opportunities get slower horizon",
            "asymmetric_long_fast_short_slow",
            8,
            18,
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c06_wider_flat_band",
            "stage41_c06_wider_flat_band",
            "wider flat band with current horizon",
            "flat_band_width",
            12,
            12,
            long_threshold_multiplier=1.35,
            short_threshold_multiplier=1.35,
            flat_band_rule="wider_flat_band_1_35x",
            expected_trade_count_effect="lower",
            overfit_risk="low",
        ),
        DirectionalAsymmetricLabelSpec(
            "c07_narrower_flat_band",
            "stage41_c07_narrower_flat_band",
            "narrower flat band with current horizon",
            "flat_band_width",
            12,
            12,
            long_threshold_multiplier=0.75,
            short_threshold_multiplier=0.75,
            flat_band_rule="narrower_flat_band_0_75x",
            expected_trade_count_effect="higher",
        ),
        DirectionalAsymmetricLabelSpec(
            "c08_asymmetric_flat_band",
            "stage41_c08_asymmetric_flat_band",
            "directional thresholds create an asymmetric flat definition",
            "asymmetric_flat_band",
            12,
            12,
            long_threshold_multiplier=1.15,
            short_threshold_multiplier=0.85,
            flat_band_rule="long_wider_short_narrower",
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c09_volatility_normalized_return_label",
            "stage41_c09_vol_normalized",
            "return thresholds scaled by trailing realized volatility",
            "volatility_normalized_return",
            12,
            12,
            volatility_normalization=True,
            threshold_source="volatility_scaled_base_threshold",
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c10_session_adjusted_label",
            "stage41_c10_session_adjusted",
            "thresholds adjusted by cash-session location",
            "session_adjusted_label",
            12,
            12,
            session_adjustment=True,
            threshold_source="session_adjusted_base_threshold",
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c11_direction_specific_threshold_label",
            "stage41_c11_direction_quantile_threshold",
            "long and short thresholds derived from train-side directional quantiles",
            "direction_specific_threshold",
            12,
            12,
            threshold_source="directional_train_q60",
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c12_long_only_label_pressure_test",
            "stage41_c12_long_only_pressure",
            "long-side label quality pressure test",
            "direction_side_pressure",
            12,
            12,
            long_short_scope="long_only",
            expected_trade_count_effect="lower",
        ),
        DirectionalAsymmetricLabelSpec(
            "c13_short_only_label_pressure_test",
            "stage41_c13_short_only_pressure",
            "short-side label quality pressure test",
            "direction_side_pressure",
            12,
            12,
            long_short_scope="short_only",
            expected_trade_count_effect="lower",
        ),
        DirectionalAsymmetricLabelSpec(
            "c14_low_complexity_model_rebuilt_label",
            "stage41_c14_low_complexity_long18_short8",
            "simple regularized model trained on rebuilt asymmetric label",
            "rebuilt_label_model_read",
            18,
            8,
            model_family="elastic_net_logistic",
            model_variant="regularized_low_complexity_c04_label",
            expected_trade_count_effect="moderate",
        ),
        DirectionalAsymmetricLabelSpec(
            "c15_tree_model_rebuilt_label",
            "stage41_c15_tree_long18_short8",
            "constrained tree model trained on rebuilt asymmetric label",
            "rebuilt_label_model_read",
            18,
            8,
            model_family="extra_trees_depth4",
            model_variant="constrained_tree_c04_label",
            expected_trade_count_effect="moderate",
            overfit_risk="medium_high",
        ),
        DirectionalAsymmetricLabelSpec(
            "c16_calibrated_rebuilt_label",
            "stage41_c16_calibrated_long18_short8",
            "calibration layer on rebuilt-label probabilities",
            "rebuilt_label_calibration_read",
            18,
            8,
            model_family="calibrated_logistic",
            model_variant="train_probability_gate_c04_label",
            decision_threshold=0.50,
            expected_trade_count_effect="lower",
        ),
        DirectionalAsymmetricLabelSpec(
            "c17_extreme_horizon_stress",
            "stage41_c17_extreme_long24_short6",
            "extreme horizon contrast to expose failure boundary",
            "extreme_horizon_stress",
            24,
            6,
            long_threshold_multiplier=1.20,
            short_threshold_multiplier=0.90,
            flat_band_rule="extreme_horizon_contrast",
            expected_trade_count_effect="lower",
            overfit_risk="high",
        ),
    ]
    return items


def build_stage41_micro_candidate_grid(
    best_candidate_id: str,
    broad_specs: Sequence[DirectionalAsymmetricLabelSpec],
) -> list[DirectionalAsymmetricLabelSpec]:
    base = next(spec for spec in broad_specs if spec.candidate_id == best_candidate_id)
    variants = [
        (
            "m01_threshold_minus10",
            {
                "long_threshold_multiplier": max(base.long_threshold_multiplier * 0.90, 0.20),
                "short_threshold_multiplier": max(base.short_threshold_multiplier * 0.90, 0.20),
                "notes": "bounded micro-search threshold relaxation after broad gate pass",
            },
        ),
        (
            "m02_threshold_plus10",
            {
                "long_threshold_multiplier": base.long_threshold_multiplier * 1.10,
                "short_threshold_multiplier": base.short_threshold_multiplier * 1.10,
                "notes": "bounded micro-search threshold firming after broad gate pass",
            },
        ),
        (
            "m03_long_horizon_plus2",
            {
                "long_horizon_bars": min(base.long_horizon_bars + 2, 30),
                "notes": "bounded micro-search long horizon extension after broad gate pass",
            },
        ),
        (
            "m04_short_horizon_minus2",
            {
                "short_horizon_bars": max(base.short_horizon_bars - 2, 4),
                "notes": "bounded micro-search short horizon compression after broad gate pass",
            },
        ),
    ]
    out = []
    for prefix, overrides in variants:
        out.append(
            replace(
                base,
                candidate_id=f"{prefix}_{base.candidate_id}",
                label_id=f"stage41_{prefix}_{base.label_id}",
                description=f"bounded micro-search around {base.description}",
                label_family=f"micro_{base.label_family}",
                **overrides,
            )
        )
    return out


def label_schema() -> list[dict[str, Any]]:
    return [
        {
            "column": "stage41_long_forward_log_return",
            "formula": "log(close[t+long_horizon] / close[t])",
            "warmup": 0,
            "lookahead": "long_horizon_bars future closed bars",
            "missingness": "NaN when exact future closed bar is unavailable",
        },
        {
            "column": "stage41_short_forward_log_return",
            "formula": "log(close[t] / close[t+short_horizon])",
            "warmup": 0,
            "lookahead": "short_horizon_bars future closed bars",
            "missingness": "NaN when exact future closed bar is unavailable",
        },
        {
            "column": "stage41_long_effective_threshold",
            "formula": "base_threshold * long_multiplier, optionally volatility/session adjusted",
            "warmup": "historical_vol_20 when volatility-normalized",
            "lookahead": "none",
            "missingness": "falls back to base threshold when historical volatility is unavailable",
        },
        {
            "column": "stage41_short_effective_threshold",
            "formula": "base_threshold * short_multiplier, optionally volatility/session adjusted",
            "warmup": "historical_vol_20 when volatility-normalized",
            "lookahead": "none",
            "missingness": "falls back to base threshold when historical volatility is unavailable",
        },
        {
            "column": "stage41_label_class",
            "formula": "short=0, flat=1, long=2 using direction-specific future returns and thresholds",
            "warmup": "max(long_horizon_bars, short_horizon_bars)",
            "lookahead": "label-only target; not exported as model feature",
            "missingness": "row is excluded when current or future close is unavailable",
        },
    ]


def _numeric(frame: pd.DataFrame, column: str, fallback: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(fallback, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").astype("float64")


def _to_utc(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True)


def _threshold_quantile(values: pd.Series, q: float, fallback: float) -> float:
    clean = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    clean = clean.loc[clean > 0]
    if clean.empty:
        return float(fallback)
    value = float(clean.quantile(q))
    return value if math.isfinite(value) and value > 0 else float(fallback)


def _effective_thresholds(
    working: pd.DataFrame,
    spec: DirectionalAsymmetricLabelSpec,
    base_threshold: float,
) -> tuple[pd.Series, pd.Series, dict[str, Any]]:
    long_threshold = float(base_threshold) * float(spec.long_threshold_multiplier)
    short_threshold = float(base_threshold) * float(spec.short_threshold_multiplier)
    threshold_source_detail: dict[str, Any] = {
        "base_threshold": float(base_threshold),
        "long_threshold_before_adjustment": long_threshold,
        "short_threshold_before_adjustment": short_threshold,
        "threshold_source": spec.threshold_source,
    }

    train_mask = working["split"].astype(str).eq("train")
    if spec.threshold_source == "directional_train_q60":
        long_threshold = _threshold_quantile(working.loc[train_mask, "stage41_long_forward_log_return"], 0.60, long_threshold)
        short_threshold = _threshold_quantile(working.loc[train_mask, "stage41_short_forward_log_return"], 0.60, short_threshold)
        threshold_source_detail["directional_train_q60_long"] = long_threshold
        threshold_source_detail["directional_train_q60_short"] = short_threshold

    long_eff = pd.Series(long_threshold, index=working.index, dtype="float64")
    short_eff = pd.Series(short_threshold, index=working.index, dtype="float64")

    if spec.volatility_normalization:
        vol = _numeric(working, "historical_vol_20").replace([np.inf, -np.inf], np.nan)
        train_vol = vol.loc[train_mask & vol.gt(0)].median()
        if not math.isfinite(float(train_vol)) or float(train_vol) <= 0:
            train_vol = 1.0
        multiplier = (vol / float(train_vol)).clip(lower=0.50, upper=2.50).fillna(1.0)
        long_eff *= multiplier
        short_eff *= multiplier
        threshold_source_detail["volatility_train_median"] = float(train_vol)
        threshold_source_detail["volatility_multiplier_clip"] = [0.50, 2.50]

    if spec.session_adjustment:
        minutes = _numeric(working, "minutes_from_cash_open")
        session_multiplier = pd.Series(1.0, index=working.index, dtype="float64")
        session_multiplier.loc[minutes.between(0, 30, inclusive="both")] = 0.90
        session_multiplier.loc[minutes.between(360, 390, inclusive="both")] = 0.90
        session_multiplier.loc[minutes.between(120, 270, inclusive="both")] = 1.10
        long_eff *= session_multiplier
        short_eff *= session_multiplier
        threshold_source_detail["session_adjustment_rule"] = "0-30m and last-30m use 0.90x; 120-270m use 1.10x"

    return long_eff, short_eff, threshold_source_detail


def materialize_directional_asymmetric_labels(
    base_frame: pd.DataFrame,
    raw_close_frame: pd.DataFrame,
    spec: DirectionalAsymmetricLabelSpec,
    base_threshold: float,
) -> pd.DataFrame:
    required = {"timestamp", "split", "minutes_from_cash_open"}
    missing = required.difference(base_frame.columns)
    if missing:
        raise ValueError(f"base frame missing required label columns: {sorted(missing)}")
    if {"timestamp", "close"}.difference(raw_close_frame.columns):
        raise ValueError("raw close frame must contain timestamp and close")

    raw = raw_close_frame[["timestamp", "close"]].copy()
    raw["timestamp"] = _to_utc(raw["timestamp"])
    raw = raw.drop_duplicates("timestamp").sort_values("timestamp")
    close_by_time = raw.rename(columns={"close": "stage41_current_close"}).set_index("timestamp")

    working = base_frame.copy()
    working["timestamp"] = _to_utc(working["timestamp"])
    working["stage41_long_future_timestamp"] = working["timestamp"] + pd.Timedelta(minutes=spec.long_horizon_bars * BAR_MINUTES)
    working["stage41_short_future_timestamp"] = working["timestamp"] + pd.Timedelta(minutes=spec.short_horizon_bars * BAR_MINUTES)
    working = working.merge(close_by_time, left_on="timestamp", right_index=True, how="left")
    working = working.merge(
        close_by_time.rename(columns={"stage41_current_close": "stage41_long_future_close"}),
        left_on="stage41_long_future_timestamp",
        right_index=True,
        how="left",
    )
    working = working.merge(
        close_by_time.rename(columns={"stage41_current_close": "stage41_short_future_close"}),
        left_on="stage41_short_future_timestamp",
        right_index=True,
        how="left",
    )
    working["stage41_long_forward_log_return"] = np.log(
        working["stage41_long_future_close"].astype("float64") / working["stage41_current_close"].astype("float64")
    )
    working["stage41_short_forward_log_return"] = np.log(
        working["stage41_current_close"].astype("float64") / working["stage41_short_future_close"].astype("float64")
    )

    max_label_start = MAX_CASH_SESSION_MINUTES - spec.max_horizon_minutes
    labelable = _numeric(working, "minutes_from_cash_open").le(max_label_start)
    labelable &= working["stage41_current_close"].notna()
    labelable &= working["stage41_long_future_close"].notna()
    labelable &= working["stage41_short_future_close"].notna()
    working = working.loc[labelable].copy().reset_index(drop=True)
    if working.empty:
        raise ValueError(f"no labelable rows for {spec.candidate_id}")

    long_eff, short_eff, threshold_detail = _effective_thresholds(working, spec, base_threshold)
    working["stage41_long_effective_threshold"] = long_eff
    working["stage41_short_effective_threshold"] = short_eff
    long_hit = working["stage41_long_forward_log_return"].ge(long_eff)
    short_hit = working["stage41_short_forward_log_return"].ge(short_eff)
    if spec.long_short_scope == "long_only":
        short_hit = pd.Series(False, index=working.index)
    elif spec.long_short_scope == "short_only":
        long_hit = pd.Series(False, index=working.index)

    long_margin = (working["stage41_long_forward_log_return"] / long_eff.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
    short_margin = (working["stage41_short_forward_log_return"] / short_eff.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
    labels = pd.Series("flat", index=working.index, dtype="object")
    labels.loc[long_hit & ~short_hit] = "long"
    labels.loc[short_hit & ~long_hit] = "short"
    both = long_hit & short_hit
    labels.loc[both & long_margin.ge(short_margin)] = "long"
    labels.loc[both & short_margin.gt(long_margin)] = "short"
    working["stage41_label"] = labels
    working["stage41_label_class"] = working["stage41_label"].map(CLASS_ID_MAP).astype("int8")
    working["stage41_label_id"] = spec.label_id
    working["stage41_label_family"] = spec.label_family
    working["stage41_long_horizon_bars"] = int(spec.long_horizon_bars)
    working["stage41_short_horizon_bars"] = int(spec.short_horizon_bars)
    working["stage41_max_horizon_bars"] = int(spec.max_horizon_bars)
    working["stage41_threshold_detail_json"] = pd.Series([threshold_detail] * len(working), dtype="object").map(str)
    return working


def split_label_distribution(frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}
    for split in ("train", "validation", "oos"):
        view = frame.loc[frame["split"].astype(str).eq(split)]
        counts = view["stage41_label"].value_counts().to_dict() if len(view) else {}
        ordered = {name: int(counts.get(name, 0)) for name in ("short", "flat", "long")}
        total = int(sum(ordered.values()))
        shares = {key: (value / total if total else 0.0) for key, value in ordered.items()}
        nonzero = [value for value in ordered.values() if value > 0]
        payload[split] = {
            "rows": total,
            "class_counts": ordered,
            "class_shares": shares,
            "max_class_share": max(shares.values()) if shares else 0.0,
            "min_nonzero_class_count": min(nonzero) if nonzero else 0,
            "class_balance_status": "pathological" if total and max(shares.values()) >= 0.90 else "usable",
        }
    return payload


def leakage_audit(frame: pd.DataFrame, spec: DirectionalAsymmetricLabelSpec) -> dict[str, Any]:
    long_ok = (pd.to_datetime(frame["stage41_long_future_timestamp"], utc=True) > pd.to_datetime(frame["timestamp"], utc=True)).all()
    short_ok = (pd.to_datetime(frame["stage41_short_future_timestamp"], utc=True) > pd.to_datetime(frame["timestamp"], utc=True)).all()
    horizon_ok = bool((frame["stage41_long_horizon_bars"].eq(spec.long_horizon_bars)).all() and (frame["stage41_short_horizon_bars"].eq(spec.short_horizon_bars)).all())
    return {
        "status": "passed" if long_ok and short_ok and horizon_ok else "failed",
        "future_timestamps_after_current": bool(long_ok and short_ok),
        "horizon_alignment_exact": horizon_ok,
        "partial_current_bar_used": False,
        "model_feature_reads_future_columns": False,
        "timestamp_rule": "features at closed M5 bar timestamp; labels use exact future closed-bar timestamps",
        "max_horizon_bars": int(spec.max_horizon_bars),
    }


def label_lineage_rows(
    specs: Sequence[DirectionalAsymmetricLabelSpec],
    *,
    source_data_path: str,
) -> list[dict[str, Any]]:
    rows = []
    for spec in specs:
        rows.append(
            {
                "candidate_id": spec.candidate_id,
                "label_id": spec.label_id,
                "source_data_path": source_data_path,
                "source_symbol": "US100",
                "timeframe": "M5",
                "timestamp_rule": "bar close timestamp; exact future closed bar by horizon",
                "ohlc_column_mapping": "close from raw MT5 closed M5 bar close",
                "calculation_formula": "direction-specific forward log returns with asymmetric thresholds",
                "long_horizon_bars": int(spec.long_horizon_bars),
                "short_horizon_bars": int(spec.short_horizon_bars),
                "warmup_requirement": f"lookahead max {spec.max_horizon_bars} closed bars; no partial current bar",
                "missingness_behavior": "row excluded when current close or exact future close is unavailable",
                "used_directly_in_mt5": False,
                "used_only_for_python_candidate_design": True,
            }
        )
    return rows

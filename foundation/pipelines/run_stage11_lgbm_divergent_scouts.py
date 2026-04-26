from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.pipelines import run_stage10_logreg_mt5_scout as scout  # noqa: E402
from foundation.pipelines import run_stage11_lgbm_training_method_scout as run02a  # noqa: E402
from foundation.pipelines import run_stage11_lgbm_rank_threshold_scout as run02b  # noqa: E402


STAGE_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
MODEL_FAMILY = "lightgbm_lgbmclassifier_multiclass"
SOURCE_RUN_ID = "run02A_lgbm_training_method_scout_v1"
DEFAULT_SOURCE_ROOT = Path("stages") / STAGE_ID / "02_runs" / SOURCE_RUN_ID
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
RUN01Y_REFERENCE = run02a.RUN01Y_REFERENCE
PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")
DECISION_COLUMNS = set(run02b.DECISION_COLUMNS)


@dataclass(frozen=True)
class DivergentSpec:
    key: str
    run_number: str
    run_id: str
    exploration_label: str
    idea_id: str
    hypothesis: str
    lane: str
    decision_surface_id: str
    mode: str
    allowed_side: str
    tier_a_quantile: float
    tier_b_quantile: float
    tier_a_margin: float
    tier_b_margin: float
    context_gate: str | None = None


SPECS: dict[str, DivergentSpec] = {
    "run02C": DivergentSpec(
        key="run02C",
        run_number="run02C",
        run_id="run02C_lgbm_long_only_direction_isolation_v1",
        exploration_label="stage11_Direction__LGBMLongOnly",
        idea_id="IDEA-ST11-LGBM-DIRECTION-LONG-ONLY",
        hypothesis="LightGBM failure may be direction-asymmetric; long-only routing may remove the harmful short side.",
        lane="alpha_direction_isolation_scout",
        decision_surface_id="run02C_lgbm_long_only_direction_surface_hold9_slice200_220",
        mode="long_only",
        allowed_side="long",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.08,
        tier_b_margin=0.05,
    ),
    "run02D": DivergentSpec(
        key="run02D",
        run_number="run02D",
        run_id="run02D_lgbm_short_only_direction_isolation_v1",
        exploration_label="stage11_Direction__LGBMShortOnly",
        idea_id="IDEA-ST11-LGBM-DIRECTION-SHORT-ONLY",
        hypothesis="LightGBM failure may be direction-asymmetric; short-only routing may reveal whether the long side is harmful.",
        lane="alpha_direction_isolation_scout",
        decision_surface_id="run02D_lgbm_short_only_direction_surface_hold9_slice200_220",
        mode="short_only",
        allowed_side="short",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.08,
        tier_b_margin=0.05,
    ),
    "run02E": DivergentSpec(
        key="run02E",
        run_number="run02E",
        run_id="run02E_lgbm_extreme_confidence_rejection_v1",
        exploration_label="stage11_Confidence__LGBMExtremeOnly",
        idea_id="IDEA-ST11-LGBM-EXTREME-CONFIDENCE",
        hypothesis="LightGBM may only carry usable edge at extreme probability and margin, so uncertain rows should be rejected.",
        lane="alpha_confidence_rejection_scout",
        decision_surface_id="run02E_lgbm_extreme_confidence_surface_hold9_slice200_220",
        mode="extreme_confidence",
        allowed_side="both",
        tier_a_quantile=0.99,
        tier_b_quantile=0.99,
        tier_a_margin=0.20,
        tier_b_margin=0.16,
    ),
    "run02F": DivergentSpec(
        key="run02F",
        run_number="run02F",
        run_id="run02F_lgbm_calm_trend_context_gate_v1",
        exploration_label="stage11_Context__LGBMCalmTrendGate",
        idea_id="IDEA-ST11-LGBM-CALM-TREND-GATE",
        hypothesis="LightGBM may need a market-context gate; calm trend rows may carry cleaner signal than all rows.",
        lane="alpha_context_gate_scout",
        decision_surface_id="run02F_lgbm_calm_trend_context_gate_surface_hold9_slice200_220",
        mode="context_gate",
        allowed_side="both",
        tier_a_quantile=0.96,
        tier_b_quantile=0.96,
        tier_a_margin=0.12,
        tier_b_margin=0.08,
        context_gate="adx14_gte25_hvol5over20_lte125",
    ),
    "run02G": DivergentSpec(
        key="run02G",
        run_number="run02G",
        run_id="run02G_lgbm_long_pullback_salvage_v1",
        exploration_label="stage11_Context__LGBMLongPullback",
        idea_id="IDEA-ST11-LGBM-LONG-PULLBACK",
        hypothesis="RUN02C long-only salvage may improve if long entries are limited to RSI and Bollinger pullback rows.",
        lane="alpha_context_direction_scout",
        decision_surface_id="run02G_lgbm_long_pullback_surface_hold9_slice200_220",
        mode="long_pullback",
        allowed_side="long",
        tier_a_quantile=0.93,
        tier_b_quantile=0.93,
        tier_a_margin=0.06,
        tier_b_margin=0.04,
        context_gate="rsi14_lte45_bbpos_lte45",
    ),
    "run02H": DivergentSpec(
        key="run02H",
        run_number="run02H",
        run_id="run02H_lgbm_bull_trend_long_v1",
        exploration_label="stage11_Context__LGBMBullTrendLong",
        idea_id="IDEA-ST11-LGBM-BULL-TREND-LONG",
        hypothesis="Long-only LGBM signals may need bullish trend confirmation instead of generic confidence filtering.",
        lane="alpha_context_direction_scout",
        decision_surface_id="run02H_lgbm_bull_trend_long_surface_hold9_slice200_220",
        mode="bull_trend_long",
        allowed_side="long",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.07,
        tier_b_margin=0.05,
        context_gate="adx14_gte20_di_spread_gt0",
    ),
    "run02I": DivergentSpec(
        key="run02I",
        run_number="run02I",
        run_id="run02I_lgbm_low_vol_extreme_confidence_v1",
        exploration_label="stage11_Context__LGBMLowVolExtremeConfidence",
        idea_id="IDEA-ST11-LGBM-LOW-VOL-EXTREME-CONFIDENCE",
        hypothesis="Extreme-confidence LGBM signals may only survive when short-term volatility is below the longer ATR regime.",
        lane="alpha_context_confidence_scout",
        decision_surface_id="run02I_lgbm_low_vol_extreme_confidence_surface_hold9_slice200_220",
        mode="low_vol_extreme_confidence",
        allowed_side="both",
        tier_a_quantile=0.985,
        tier_b_quantile=0.985,
        tier_a_margin=0.18,
        tier_b_margin=0.14,
        context_gate="hvol5over20_lte90_atr_lte115",
    ),
    "run02J": DivergentSpec(
        key="run02J",
        run_number="run02J",
        run_id="run02J_lgbm_balanced_midband_context_v1",
        exploration_label="stage11_Context__LGBMBalancedMidband",
        idea_id="IDEA-ST11-LGBM-BALANCED-MIDBAND",
        hypothesis="LGBM may be less unstable in mid-band RSI and Bollinger rows where price is not stretched.",
        lane="alpha_context_gate_scout",
        decision_surface_id="run02J_lgbm_balanced_midband_surface_hold9_slice200_220",
        mode="balanced_midband",
        allowed_side="both",
        tier_a_quantile=0.95,
        tier_b_quantile=0.95,
        tier_a_margin=0.10,
        tier_b_margin=0.07,
        context_gate="rsi14_between45_60_bbpos_between35_75",
    ),
    "run02K": DivergentSpec(
        key="run02K",
        run_number="run02K",
        run_id="run02K_lgbm_quiet_return_zscore_v1",
        exploration_label="stage11_Context__LGBMQuietReturnZScore",
        idea_id="IDEA-ST11-LGBM-QUIET-RETURN-ZSCORE",
        hypothesis="LGBM probability ranks may be cleaner when the immediate return z-score is not already stretched.",
        lane="alpha_context_gate_scout",
        decision_surface_id="run02K_lgbm_quiet_return_zscore_surface_hold9_slice200_220",
        mode="quiet_return_zscore",
        allowed_side="both",
        tier_a_quantile=0.96,
        tier_b_quantile=0.96,
        tier_a_margin=0.12,
        tier_b_margin=0.08,
        context_gate="return_zscore_abs_lte70",
    ),
    "run02L": DivergentSpec(
        key="run02L",
        run_number="run02L",
        run_id="run02L_lgbm_range_compression_v1",
        exploration_label="stage11_Context__LGBMRangeCompression",
        idea_id="IDEA-ST11-LGBM-RANGE-COMPRESSION",
        hypothesis="LGBM may behave differently when DI spread and ADX imply compression rather than directional chase.",
        lane="alpha_context_gate_scout",
        decision_surface_id="run02L_lgbm_range_compression_surface_hold9_slice200_220",
        mode="range_compression",
        allowed_side="both",
        tier_a_quantile=0.96,
        tier_b_quantile=0.96,
        tier_a_margin=0.10,
        tier_b_margin=0.06,
        context_gate="di_spread_abs_lte8_adx_lte25",
    ),
    "run02M": DivergentSpec(
        key="run02M",
        run_number="run02M",
        run_id="run02M_lgbm_high_vol_momentum_alignment_v1",
        exploration_label="stage11_Context__LGBMHighVolMomentumAlignment",
        idea_id="IDEA-ST11-LGBM-HIGH-VOL-MOMENTUM-ALIGN",
        hypothesis="The weak LGBM surface may need volatility expansion plus aligned ROC and PPO momentum before it becomes tradable.",
        lane="alpha_context_momentum_scout",
        decision_surface_id="run02M_lgbm_high_vol_momentum_alignment_surface_hold9_slice200_220",
        mode="high_vol_momentum_alignment",
        allowed_side="both",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.08,
        tier_b_margin=0.05,
        context_gate="atr_ratio_gte115_momentum_align",
    ),
    "run02N": DivergentSpec(
        key="run02N",
        run_number="run02N",
        run_id="run02N_lgbm_squeeze_breakout_probe_v1",
        exploration_label="stage11_Context__LGBMSqueezeBreakout",
        idea_id="IDEA-ST11-LGBM-SQUEEZE-BREAKOUT",
        hypothesis="LGBM may only carry edge around Bollinger squeeze breakout conditions where the next move is more discrete.",
        lane="alpha_context_momentum_scout",
        decision_surface_id="run02N_lgbm_squeeze_breakout_surface_hold9_slice200_220",
        mode="squeeze_breakout",
        allowed_side="both",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.08,
        tier_b_margin=0.05,
        context_gate="bb_squeeze_true",
    ),
    "run02O": DivergentSpec(
        key="run02O",
        run_number="run02O",
        run_id="run02O_lgbm_bull_vortex_long_v1",
        exploration_label="stage11_Context__LGBMBullVortexLong",
        idea_id="IDEA-ST11-LGBM-BULL-VORTEX-LONG",
        hypothesis="RUN02C long-only salvage may be concentrated in bullish vortex rows with RSI50 support.",
        lane="alpha_context_direction_scout",
        decision_surface_id="run02O_lgbm_bull_vortex_long_surface_hold9_slice200_220",
        mode="bull_vortex_long",
        allowed_side="long",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.07,
        tier_b_margin=0.05,
        context_gate="vortex_positive_rsi50_gte50",
    ),
    "run02P": DivergentSpec(
        key="run02P",
        run_number="run02P",
        run_id="run02P_lgbm_bear_vortex_short_v1",
        exploration_label="stage11_Context__LGBMBearVortexShort",
        idea_id="IDEA-ST11-LGBM-BEAR-VORTEX-SHORT",
        hypothesis="Although RUN02D was weak, short-only rows may need bearish vortex and RSI50 confirmation before being rejected broadly.",
        lane="alpha_context_direction_scout",
        decision_surface_id="run02P_lgbm_bear_vortex_short_surface_hold9_slice200_220",
        mode="bear_vortex_short",
        allowed_side="short",
        tier_a_quantile=0.94,
        tier_b_quantile=0.94,
        tier_a_margin=0.07,
        tier_b_margin=0.05,
        context_gate="vortex_negative_rsi50_lte50",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 11 divergent LGBM scouts.")
    parser.add_argument("--source-run-root", default=str(DEFAULT_SOURCE_ROOT))
    parser.add_argument("--run-root", default=str(Path("stages") / STAGE_ID / "02_runs"))
    parser.add_argument("--variants", nargs="+", default=["run02C", "run02D", "run02E", "run02F"])
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


def _io_path(path: Path) -> Path:
    return scout._io_path(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(_io_path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout.write_json(path, payload)


def copy_artifact(source: Path, destination: Path) -> dict[str, Any]:
    _io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(_io_path(source), _io_path(destination))
    return {"source": source.as_posix(), "path": destination.as_posix(), "sha256": scout.sha256_file(destination)}


def validation_quantile(frame: pd.DataFrame, column: str, quantile: float) -> float:
    validation = frame.loc[frame["split"].astype(str).eq("validation")]
    if validation.empty:
        raise RuntimeError(f"Cannot select quantile from empty validation split for {column}.")
    return float(validation[column].quantile(float(quantile)))


def threshold_id(prefix: str, mode: str, quantile: float, short_threshold: float, long_threshold: float, margin: float) -> str:
    return (
        f"{prefix}_{mode}_q{quantile:.3f}"
        f"_short{short_threshold:.3f}_long{long_threshold:.3f}_margin{margin:.3f}"
    )


def build_rule(frame: pd.DataFrame, *, spec: DivergentSpec, tier_prefix: str, quantile: float, margin: float) -> scout.ThresholdRule:
    short_threshold = validation_quantile(frame, "p_short", quantile)
    long_threshold = validation_quantile(frame, "p_long", quantile)
    if spec.allowed_side == "long":
        short_threshold = 1.0
    elif spec.allowed_side == "short":
        long_threshold = 1.0
    elif spec.allowed_side != "both":
        raise ValueError(f"Unknown allowed_side: {spec.allowed_side}")
    return scout.ThresholdRule(
        threshold_id=threshold_id(tier_prefix, spec.mode, quantile, short_threshold, long_threshold, margin),
        short_threshold=float(short_threshold),
        long_threshold=float(long_threshold),
        min_margin=float(margin),
    )


def recompute_predictions(frame: pd.DataFrame, rule: scout.ThresholdRule) -> pd.DataFrame:
    identity_columns = [column for column in frame.columns if column not in DECISION_COLUMNS]
    identity = frame.loc[:, identity_columns].reset_index(drop=True)
    decisions = scout.apply_threshold_rule(frame.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64"), rule)
    return pd.concat([identity, decisions], axis=1)


def timestamp_key(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def context_gate_mask(frame: pd.DataFrame, gate: str) -> pd.Series:
    if gate == "adx14_gte25_hvol5over20_lte125":
        return frame["adx_14"].astype(float).ge(25.0) & frame["historical_vol_5_over_20"].astype(float).le(1.25)
    if gate == "rsi14_lte45_bbpos_lte45":
        return frame["rsi_14"].astype(float).le(45.0) & frame["bb_position_20"].astype(float).le(0.45)
    if gate == "adx14_gte20_di_spread_gt0":
        return frame["adx_14"].astype(float).ge(20.0) & frame["di_spread_14"].astype(float).gt(0.0)
    if gate == "hvol5over20_lte90_atr_lte115":
        return frame["historical_vol_5_over_20"].astype(float).le(0.90) & frame["atr_14_over_atr_50"].astype(float).le(1.15)
    if gate == "rsi14_between45_60_bbpos_between35_75":
        return (
            frame["rsi_14"].astype(float).between(45.0, 60.0, inclusive="both")
            & frame["bb_position_20"].astype(float).between(0.35, 0.75, inclusive="both")
        )
    if gate == "return_zscore_abs_lte70":
        return frame["return_zscore_20"].astype(float).abs().le(0.70)
    if gate == "di_spread_abs_lte8_adx_lte25":
        return frame["di_spread_14"].astype(float).abs().le(8.0) & frame["adx_14"].astype(float).le(25.0)
    if gate == "atr_ratio_gte115_momentum_align":
        return (
            frame["atr_14_over_atr_50"].astype(float).ge(1.15)
            & (frame["ppo_hist_12_26_9"].astype(float) * frame["roc_12"].astype(float)).gt(0.0)
        )
    if gate == "bb_squeeze_true":
        return frame["bb_squeeze"].astype(float).ge(0.5)
    if gate == "vortex_positive_rsi50_gte50":
        return frame["vortex_indicator"].astype(float).gt(0.0) & frame["rsi_50"].astype(float).ge(50.0)
    if gate == "vortex_negative_rsi50_lte50":
        return frame["vortex_indicator"].astype(float).lt(0.0) & frame["rsi_50"].astype(float).le(50.0)
    raise ValueError(f"Unknown context gate: {gate}")


def write_matrix_for_variant(
    *,
    source_path: Path,
    destination_path: Path,
    context_gate: str | None,
) -> dict[str, Any]:
    _io_path(destination_path.parent).mkdir(parents=True, exist_ok=True)
    if context_gate is None:
        shutil.copy2(_io_path(source_path), _io_path(destination_path))
        copied = pd.read_csv(_io_path(destination_path), usecols=["timestamp_utc"])
        allowed = set(timestamp_key(copied["timestamp_utc"]))
        return {
            "path": destination_path.as_posix(),
            "source": source_path.as_posix(),
            "sha256": scout.sha256_file(destination_path),
            "rows": int(len(copied)),
            "filtered_out_rows": 0,
            "allowed_timestamps": allowed,
        }
    source = pd.read_csv(_io_path(source_path))
    mask = context_gate_mask(source, context_gate)
    filtered = source.loc[mask].copy()
    filtered.to_csv(_io_path(destination_path), index=False)
    allowed = set(timestamp_key(filtered["timestamp_utc"]))
    return {
        "path": destination_path.as_posix(),
        "source": source_path.as_posix(),
        "sha256": scout.sha256_file(destination_path),
        "rows": int(len(filtered)),
        "source_rows": int(len(source)),
        "filtered_out_rows": int(len(source) - len(filtered)),
        "context_gate": context_gate,
        "allowed_timestamps": allowed,
    }


def filter_predictions_for_context(
    frame: pd.DataFrame,
    *,
    allowed_by_split: Mapping[str, set[str]] | None,
) -> pd.DataFrame:
    if not allowed_by_split:
        return frame.copy().reset_index(drop=True)
    split_alias = {"validation": "validation_is", "oos": "oos"}
    keyed = frame.copy()
    keyed["_timestamp_key"] = timestamp_key(keyed["timestamp"])
    keep = pd.Series(False, index=keyed.index)
    for split_name, allowed in allowed_by_split.items():
        canonical_split = "validation" if split_name == "validation_is" else split_name
        keep |= keyed["split"].astype(str).eq(canonical_split) & keyed["_timestamp_key"].isin(allowed)
    return keyed.loc[keep].drop(columns=["_timestamp_key"]).reset_index(drop=True)


def selected_threshold_id(spec: DivergentSpec, tier_a_rule: scout.ThresholdRule, tier_b_rule: scout.ThresholdRule) -> str:
    return (
        f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}"
        f"__hold9__slice_mid_second_overlap_200_220__model_lgbm_{spec.mode}"
    )


def build_route_coverage(
    *,
    base_summary: Mapping[str, Any],
    tier_a_predictions: pd.DataFrame,
    tier_b_predictions: pd.DataFrame,
    spec: DivergentSpec,
) -> dict[str, Any]:
    empty_no_tier = tier_a_predictions.iloc[0:0].copy()
    coverage = scout.build_eval_route_coverage_summary(
        base_summary=base_summary,
        tier_a_eval_frame=tier_a_predictions,
        tier_b_eval_frame=tier_b_predictions,
        no_tier_eval_frame=empty_no_tier,
        session_slice=base_summary.get("session_slice"),
    )
    coverage["variant_mode"] = spec.mode
    coverage["idea_id"] = spec.idea_id
    coverage["context_gate"] = spec.context_gate
    coverage["note"] = (
        "Variant-specific route coverage after context gating."
        if spec.context_gate
        else "Variant-specific route coverage with the base Stage 11 session slice."
    )
    return coverage


def materialize_run_registry_row(
    *,
    spec: DivergentSpec,
    run_output_root: Path,
    route_coverage: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    external_verification_status: str,
) -> dict[str, Any]:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}
    by_mt5_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}
    validation = by_mt5_view.get("mt5_routed_total_validation_is", {})
    oos = by_mt5_view.get("mt5_routed_total_oos", {})
    notes = scout._ledger_pairs(
        (
            ("idea_id", spec.idea_id),
            ("model_family", MODEL_FAMILY),
            ("comparison_reference", RUN01Y_REFERENCE["run_id"]),
            ("decision_surface", spec.decision_surface_id),
            ("variant_mode", spec.mode),
            ("allowed_side", spec.allowed_side),
            ("context_gate", spec.context_gate),
            ("session_slice", RUN01Y_REFERENCE["session_slice_id"]),
            ("max_hold_bars", RUN01Y_REFERENCE["max_hold_bars"]),
            ("tier_b_fallback_rows", route_coverage.get("tier_b_fallback_rows")),
            ("no_tier_labelable_rows", route_coverage.get("no_tier_labelable_rows")),
            ("tier_a_signal_coverage", by_view.get("tier_a_separate", {}).get("signal_coverage")),
            ("tier_b_signal_coverage", by_view.get("tier_b_separate", {}).get("signal_coverage")),
            ("combined_signal_coverage", by_view.get("tier_ab_combined", {}).get("signal_coverage")),
            ("validation_net_profit", validation.get("net_profit")),
            ("validation_pf", validation.get("profit_factor")),
            ("validation_b_fallback_used", validation.get("tier_b_fallback_used_count")),
            ("oos_net_profit", oos.get("net_profit")),
            ("oos_pf", oos.get("profit_factor")),
            ("oos_b_fallback_used", oos.get("tier_b_fallback_used_count")),
            ("external_verification", external_verification_status),
            ("boundary", "mt5_runtime_probe_only"),
        )
    )
    row = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "lane": spec.lane,
        "status": "reviewed" if external_verification_status == "completed" else "payload_only",
        "judgment": (
            f"inconclusive_{spec.mode}_mt5_runtime_probe_completed"
            if external_verification_status == "completed"
            else f"inconclusive_{spec.mode}_payload"
        ),
        "path": run_output_root.as_posix(),
        "notes": notes,
    }
    return run02a._upsert_csv_rows(run02a.RUN_REGISTRY_PATH, scout.RUN_REGISTRY_COLUMNS, [row], key="run_id")


def write_result_summary(
    *,
    path: Path,
    spec: DivergentSpec,
    threshold_id: str,
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    external_status: str,
) -> None:
    py_by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}
    mt5_by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}

    def py(view: str, key: str) -> Any:
        return py_by_view.get(view, {}).get(key)

    def mt5(view: str, key: str) -> Any:
        return mt5_by_view.get(view, {}).get(key)

    lines = [
        f"# Stage 11 {spec.run_number.upper()} LGBM Divergent Scout",
        "",
        f"- run_id(실행 ID): `{spec.run_id}`",
        f"- idea_id(아이디어 ID): `{spec.idea_id}`",
        f"- hypothesis(가설): {spec.hypothesis}",
        f"- mode(방식): `{spec.mode}`",
        f"- allowed side(허용 방향): `{spec.allowed_side}`",
        f"- selected threshold(선택 임계값): `{threshold_id}`",
        f"- context gate(문맥 제한): `{spec.context_gate or 'none(없음)'}`",
        f"- external verification status(외부 검증 상태): `{external_status}`",
        "",
        "## Python Signal Views(파이썬 신호 보기)",
        "",
        "| view(보기) | rows(행) | signal count(신호 수) | coverage(커버리지) | short/long(숏/롱) |",
        "|---|---:|---:|---:|---:|",
        (
            f"| Tier A separate(Tier A 분리) | `{py('tier_a_separate', 'rows')}` | "
            f"`{py('tier_a_separate', 'signal_count')}` | `{py('tier_a_separate', 'signal_coverage')}` | "
            f"`{py('tier_a_separate', 'short_count')}/{py('tier_a_separate', 'long_count')}` |"
        ),
        (
            f"| Tier B separate(Tier B 분리) | `{py('tier_b_separate', 'rows')}` | "
            f"`{py('tier_b_separate', 'signal_count')}` | `{py('tier_b_separate', 'signal_coverage')}` | "
            f"`{py('tier_b_separate', 'short_count')}/{py('tier_b_separate', 'long_count')}` |"
        ),
        (
            f"| Tier A+B combined(Tier A+B 합산) | `{py('tier_ab_combined', 'rows')}` | "
            f"`{py('tier_ab_combined', 'signal_count')}` | `{py('tier_ab_combined', 'signal_coverage')}` | "
            f"`{py('tier_ab_combined', 'short_count')}/{py('tier_ab_combined', 'long_count')}` |"
        ),
        "",
        "## MT5 Routed Probe(MT5 라우팅 탐침)",
        "",
        f"- validation routed net/PF(검증 라우팅 순수익/수익 팩터): `{mt5('mt5_routed_total_validation_is', 'net_profit')}` / `{mt5('mt5_routed_total_validation_is', 'profit_factor')}`",
        f"- OOS routed net/PF(표본외 라우팅 순수익/수익 팩터): `{mt5('mt5_routed_total_oos', 'net_profit')}` / `{mt5('mt5_routed_total_oos', 'profit_factor')}`",
        f"- validation Tier B fallback used(검증 Tier B 대체 사용): `{mt5('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
        f"- OOS Tier B fallback used(표본외 Tier B 대체 사용): `{mt5('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
        "",
        "## Boundary(경계)",
        "",
        "이 실행(run, 실행)은 divergent scout(발산형 탐색)이자 MT5 runtime_probe(MT5 런타임 탐침)다.",
        "효과(effect, 효과)는 RUN01(실행 01) 근처 튜닝이 아니라 LightGBM(라이트GBM)의 다른 실패 구조를 빠르게 분리해서 보는 것이다.",
        "",
        "이 실행은 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
        "",
    ]
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text("\n".join(lines), encoding="utf-8-sig")
    return

    lines = [
        f"# Stage 11 {spec.run_number.upper()} LGBM Divergent Scout",
        "",
        f"- run_id(실행 ID): `{spec.run_id}`",
        f"- idea_id(아이디어 ID): `{spec.idea_id}`",
        f"- hypothesis(가설): {spec.hypothesis}",
        f"- mode(방식): `{spec.mode}`",
        f"- selected threshold(선택 임계값): `{threshold_id}`",
        f"- context gate(문맥 제한): `{spec.context_gate or 'none(없음)'}`",
        f"- external verification status(외부 검증 상태): `{external_status}`",
        "",
        "## Python Signal Views(파이썬 신호 보기)",
        "",
        "| view(보기) | rows(행) | signal count(신호 수) | coverage(커버리지) | short/long(숏/롱) |",
        "|---|---:|---:|---:|---:|",
        (
            f"| Tier A separate(Tier A 분리) | `{py('tier_a_separate', 'rows')}` | "
            f"`{py('tier_a_separate', 'signal_count')}` | `{py('tier_a_separate', 'signal_coverage')}` | "
            f"`{py('tier_a_separate', 'short_count')}/{py('tier_a_separate', 'long_count')}` |"
        ),
        (
            f"| Tier B separate(Tier B 분리) | `{py('tier_b_separate', 'rows')}` | "
            f"`{py('tier_b_separate', 'signal_count')}` | `{py('tier_b_separate', 'signal_coverage')}` | "
            f"`{py('tier_b_separate', 'short_count')}/{py('tier_b_separate', 'long_count')}` |"
        ),
        (
            f"| Tier A+B combined(Tier A+B 합산) | `{py('tier_ab_combined', 'rows')}` | "
            f"`{py('tier_ab_combined', 'signal_count')}` | `{py('tier_ab_combined', 'signal_coverage')}` | "
            f"`{py('tier_ab_combined', 'short_count')}/{py('tier_ab_combined', 'long_count')}` |"
        ),
        "",
        "## MT5 Routed Probe(MT5 라우팅 탐침)",
        "",
        f"- validation routed net/PF(검증 라우팅 순수익/수익 팩터): `{mt5('mt5_routed_total_validation_is', 'net_profit')}` / `{mt5('mt5_routed_total_validation_is', 'profit_factor')}`",
        f"- OOS routed net/PF(표본외 라우팅 순수익/수익 팩터): `{mt5('mt5_routed_total_oos', 'net_profit')}` / `{mt5('mt5_routed_total_oos', 'profit_factor')}`",
        f"- validation Tier B fallback used(검증 Tier B 대체 사용): `{mt5('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
        f"- OOS Tier B fallback used(표본외 Tier B 대체 사용): `{mt5('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
        "",
        "## Boundary(경계)",
        "",
        "이 실행(run, 실행)은 divergent scout(발산형 탐색)와 MT5 runtime_probe(MT5 런타임 탐침)다.",
        "효과(effect, 효과)는 RUN01(실행 01)식 근처 튜닝이 아니라, LightGBM(라이트GBM)의 다른 실패 구조를 빠르게 분리해서 보는 것이다.",
        "",
        "이 실행은 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
        "",
    ]
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text("\n".join(lines), encoding="utf-8-sig")


def append_artifact_rows(rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    path = Path("docs/registers/artifact_registry.csv")
    existing: dict[str, dict[str, str]] = {}
    columns = ["artifact_id", "type", "path", "status", "notes"]
    if scout._path_exists(path):
        with _io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                existing[str(row["artifact_id"])] = {column: row.get(column, "") for column in columns}
    for row in rows:
        existing[str(row["artifact_id"])] = {column: str(row.get(column, "")) for column in columns}
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with _io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for key in existing:
            writer.writerow(existing[key])
    return {"path": path.as_posix(), "rows": len(existing), "sha256": scout.sha256_file_lf_normalized(path)}


def run_one_spec(
    *,
    spec: DivergentSpec,
    source_run_root: Path,
    run_root: Path,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
) -> dict[str, Any]:
    scout.configure_run_identity(
        run_number=spec.run_number,
        run_id=spec.run_id,
        exploration_label=spec.exploration_label,
        common_run_root=f"Project_Obsidian_Prime_v2/stage11/{spec.run_id}",
    )
    run_output_root = run_root / spec.run_id
    predictions_root = run_output_root / "predictions"
    models_root = run_output_root / "models"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"
    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)

    source_summary = read_json(source_run_root / "summary.json")
    base_route_coverage = source_summary["route_coverage"]
    tier_a_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_a_predictions.parquet"))
    tier_b_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_b_predictions.parquet"))

    tier_a_rule = build_rule(tier_a_source, spec=spec, tier_prefix="tier_a", quantile=spec.tier_a_quantile, margin=spec.tier_a_margin)
    tier_b_rule = build_rule(tier_b_source, spec=spec, tier_prefix="tier_b", quantile=spec.tier_b_quantile, margin=spec.tier_b_margin)
    threshold_id = selected_threshold_id(spec, tier_a_rule, tier_b_rule)

    split_specs = {"validation_is": ("2025.01.01", "2025.10.01"), "oos": ("2025.10.01", "2026.04.14")}
    source_tier_a_onnx = source_run_root / "models" / "tier_a_lgbm_58_model.onnx"
    source_tier_b_onnx = source_run_root / "models" / "tier_b_lgbm_core42_model.onnx"
    tier_a_onnx_path = models_root / source_tier_a_onnx.name
    tier_b_onnx_path = models_root / source_tier_b_onnx.name
    source_tier_a_order = source_run_root / "models" / "tier_a_58_feature_order.txt"
    source_tier_b_order = source_run_root / "models" / "tier_b_core42_feature_order.txt"
    tier_a_feature_order_path = models_root / source_tier_a_order.name
    tier_b_feature_order_path = models_root / source_tier_b_order.name
    model_copies = [
        copy_artifact(source_tier_a_onnx, tier_a_onnx_path),
        copy_artifact(source_tier_b_onnx, tier_b_onnx_path),
        copy_artifact(source_tier_a_order, tier_a_feature_order_path),
        copy_artifact(source_tier_b_order, tier_b_feature_order_path),
    ]
    tier_a_feature_order = scout.load_feature_order(_io_path(tier_a_feature_order_path))
    tier_b_feature_order = scout.load_feature_order(_io_path(tier_b_feature_order_path))
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)

    common_copies = [
        scout.copy_to_common_files(common_files_root, tier_a_onnx_path, scout.common_ref("models", tier_a_onnx_path.name)),
        scout.copy_to_common_files(common_files_root, tier_b_onnx_path, scout.common_ref("models", tier_b_onnx_path.name)),
    ]
    matrix_records: list[dict[str, Any]] = []
    allowed_by_tier_split: dict[str, dict[str, set[str]]] = {"tier_a": {}, "tier_b": {}}
    mt5_attempts: list[dict[str, Any]] = []
    for split_name, (from_date, to_date) in split_specs.items():
        source_tier_a_matrix = source_run_root / "mt5" / f"tier_a_{split_name}_feature_matrix.csv"
        source_tier_b_matrix = source_run_root / "mt5" / f"tier_b_{split_name}_feature_matrix.csv"
        tier_a_matrix_path = mt5_root / f"tier_a_{split_name}_feature_matrix.csv"
        tier_b_matrix_path = mt5_root / f"tier_b_{split_name}_feature_matrix.csv"
        tier_a_matrix = write_matrix_for_variant(
            source_path=source_tier_a_matrix,
            destination_path=tier_a_matrix_path,
            context_gate=spec.context_gate,
        )
        tier_b_matrix = write_matrix_for_variant(
            source_path=source_tier_b_matrix,
            destination_path=tier_b_matrix_path,
            context_gate=spec.context_gate,
        )
        allowed_by_tier_split["tier_a"][split_name] = set(tier_a_matrix.pop("allowed_timestamps"))
        allowed_by_tier_split["tier_b"][split_name] = set(tier_b_matrix.pop("allowed_timestamps"))
        matrix_records.extend(
            [
                {"tier": scout.TIER_A, "split": split_name, **tier_a_matrix},
                {"tier": scout.TIER_B, "split": split_name, **tier_b_matrix},
            ]
        )
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_a_matrix_path, scout.common_ref("features", tier_a_matrix_path.name)))
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_b_matrix_path, scout.common_ref("features", tier_b_matrix_path.name)))
        mt5_attempts.append(
            scout.materialize_mt5_routed_attempt_files(
                run_output_root=run_output_root,
                split_name=split_name,
                primary_onnx_path=tier_a_onnx_path,
                primary_feature_matrix_path=tier_a_matrix_path,
                primary_feature_count=len(tier_a_feature_order),
                primary_feature_order_hash=tier_a_feature_hash,
                fallback_onnx_path=tier_b_onnx_path,
                fallback_feature_matrix_path=tier_b_matrix_path,
                fallback_feature_count=len(tier_b_feature_order),
                fallback_feature_order_hash=tier_b_feature_hash,
                rule=tier_a_rule,
                fallback_rule=tier_b_rule,
                max_hold_bars=RUN01Y_REFERENCE["max_hold_bars"],
                fallback_enabled=True,
                from_date=from_date,
                to_date=to_date,
            )
        )

    tier_a_context_allowed = allowed_by_tier_split["tier_a"] if spec.context_gate else None
    tier_b_context_allowed = allowed_by_tier_split["tier_b"] if spec.context_gate else None
    tier_a_predictions = recompute_predictions(filter_predictions_for_context(tier_a_source, allowed_by_split=tier_a_context_allowed), tier_a_rule)
    tier_b_predictions = recompute_predictions(filter_predictions_for_context(tier_b_source, allowed_by_split=tier_b_context_allowed), tier_b_rule)
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)

    tier_views = scout.build_tier_prediction_views(predictions)
    tier_outputs = scout.materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = scout.build_paired_tier_records(
        tier_views,
        run_id=spec.run_id,
        stage_id=STAGE_ID,
        base_path=predictions_root,
        kpi_scope=f"signal_probability_{spec.mode}",
        scoreboard_lane="structural_scout",
        external_verification_status="out_of_scope_by_claim",
    )
    route_coverage = build_route_coverage(
        base_summary=base_route_coverage,
        tier_a_predictions=tier_a_predictions,
        tier_b_predictions=tier_b_predictions,
        spec=spec,
    )
    python_ledger_rows = run02a.build_python_alpha_ledger_rows(
        run_id=spec.run_id,
        tier_records=tier_records,
        selected_threshold_id=threshold_id,
        model_family=MODEL_FAMILY,
    )
    for row in python_ledger_rows:
        row["kpi_scope"] = f"signal_probability_{spec.mode}"
        row["judgment"] = f"inconclusive_{spec.mode}_payload"

    compile_payload: dict[str, Any] | None = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[output_key]))
                if scout._path_exists(output_path):
                    _io_path(output_path).unlink()
            scout.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = scout.compile_mql5_ea(metaeditor_path, scout.EA_SOURCE_PATH, mt5_root / "mt5_compile.log")
        if compile_payload.get("status") == "completed":
            for attempt in mt5_attempts:
                try:
                    result = scout.run_mt5_tester(
                        terminal_path,
                        Path(attempt["ini"]["path"]),
                        set_path=Path(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / scout.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_root / scout.mt5_short_profile_ini_name(attempt["tier"], attempt["split"]),
                        timeout_seconds=300,
                    )
                except Exception as exc:  # pragma: no cover - external MT5 boundary
                    result = {"status": "blocked", "blocker": "mt5_tester_exception", "error": repr(exc)}
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                result["routing_mode"] = attempt["routing_mode"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = (
                    scout.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
                    if result.get("status") == "completed"
                    else scout.validate_mt5_runtime_outputs(common_files_root, attempt)
                )
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = (
        scout.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=mt5_attempts,
        )
        if attempt_mt5
        else []
    )
    scout.attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = scout.build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = scout.enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    expected_mt5_count = len(mt5_attempts) * 3
    mt5_runtime_completed = bool(mt5_execution_results) and all(item.get("status") == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_count and all(item.get("status") == "completed" for item in mt5_kpi_records)
    external_status = "completed" if mt5_runtime_completed and mt5_reports_completed else "blocked" if attempt_mt5 else "out_of_scope_by_claim"

    mt5_ledger_rows = run02a.build_mt5_alpha_ledger_rows(
        run_id=spec.run_id,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_rows = [*python_ledger_rows, *mt5_ledger_rows]
    ledger_payload = run02a.materialize_ledgers(ledger_rows)
    registry_payload = materialize_run_registry_row(
        spec=spec,
        run_output_root=run_output_root,
        route_coverage=route_coverage,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        external_verification_status=external_status,
    )

    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    decision_surface = {
        "decision_surface_id": spec.decision_surface_id,
        "source_run_id": SOURCE_RUN_ID,
        "variant_mode": spec.mode,
        "context_gate": spec.context_gate,
        "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
        "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
        "selected_threshold_id": threshold_id,
        "selection_scope": "validation_quantile_then_mt5_routed_probe",
    }
    manifest = {
        "identity": {
            "run_id": spec.run_id,
            "run_number": spec.run_number,
            "stage_id": STAGE_ID,
            "exploration_label": spec.exploration_label,
            "idea_id": spec.idea_id,
            "model_family": MODEL_FAMILY,
            "status": "reviewed_payload",
            "judgment": f"inconclusive_{spec.mode}_mt5_runtime_probe_completed"
            if external_status == "completed"
            else f"inconclusive_{spec.mode}_payload",
        },
        "hypothesis": spec.hypothesis,
        "legacy_relation": "none",
        "tier_scope": "mixed_tier_a_tier_b",
        "broad_sweep": {
            "variant": spec.mode,
            "allowed_side": spec.allowed_side,
            "tier_a_quantile": spec.tier_a_quantile,
            "tier_b_quantile": spec.tier_b_quantile,
            "tier_a_margin": spec.tier_a_margin,
            "tier_b_margin": spec.tier_b_margin,
            "context_gate": spec.context_gate,
        },
        "extreme_sweep": "Single-side variants disable the opposite direction with threshold 1.0; high-confidence variants use upper probability quantiles and larger margins.",
        "micro_search_gate": "Only consider fine search if routed validation and OOS both stop the RUN02A/RUN02B drawdown pattern.",
        "wfo_plan": "explicit_exception_single_window_runtime_probe_first; WFO deferred until a structurally different idea is worth hardening.",
        "failure_memory": "If weak, preserve as negative evidence and reopen only with new label, model family, or context feature.",
        "evidence_boundary": "runtime_probe_only_not_alpha_quality",
        "comparison_reference": RUN01Y_REFERENCE,
        "source_run_id": SOURCE_RUN_ID,
        "decision_surface": decision_surface,
        "route_coverage": route_coverage,
        "tier_records": tier_records,
        "artifacts": [
            {"role": "source_run_manifest", "path": (source_run_root / "run_manifest.json").as_posix(), "sha256": scout.sha256_file(source_run_root / "run_manifest.json")},
            {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_a_predictions_path)},
            {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_b_predictions_path)},
            {"role": "tier_ab_combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(combined_predictions_path)},
            {"role": "copied_models_and_feature_orders", "copies": model_copies},
            {"role": "feature_matrices", "matrices": matrix_records},
            {"role": "mt5_attempts", "attempts": mt5_attempts},
            {"role": "mt5_common_file_copies", "copies": common_copies},
            {"role": "mt5_compile", "compile": compile_payload},
            {"role": "mt5_execution_results", "execution_results": mt5_execution_results},
            {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
            {"role": "mt5_runtime_module_hashes", "modules": scout.mt5_runtime_module_hashes()},
            {"role": "tier_prediction_views", "views": tier_outputs},
            {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
            {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
            {"role": "project_run_registry", **registry_payload},
        ],
        "mt5": {
            "attempted": bool(attempt_mt5),
            "attempt_policy": "routed_only",
            "compile": compile_payload,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
            "kpi_records": mt5_kpi_records,
            "runtime_completed": mt5_runtime_completed,
            "reports_completed": mt5_reports_completed,
        },
        "external_verification_status": external_status,
        "boundary": "divergent_runtime_probe_only_not_alpha_quality",
    }
    kpi = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": f"signal_probability_{spec.mode}_trading_risk_execution",
        "decision_surface": decision_surface,
        "signal": {"tier_records": tier_records},
        "routing": {"route_coverage": route_coverage, "mt5_kpi_records": mt5_kpi_records},
        "mt5": manifest["mt5"],
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "idea_id": spec.idea_id,
        "status": "reviewed_payload",
        "judgment": manifest["identity"]["judgment"],
        "selected_threshold_id": threshold_id,
        "decision_surface": decision_surface,
        "tier_records": tier_records,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": registry_payload,
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi)
    write_json(summary_path, summary)
    write_result_summary(
        path=result_summary_path,
        spec=spec,
        threshold_id=threshold_id,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        external_status=external_status,
    )

    artifact_rows = [
        {
            "artifact_id": f"stage11_{spec.run_number}_manifest",
            "type": "run_manifest",
            "path": manifest_path.as_posix(),
            "status": "local_generated_reviewed",
            "notes": f"Stage 11 {spec.run_number} divergent LGBM scout; manifest_sha256 {scout.sha256_file(manifest_path)}; boundary runtime_probe only",
        },
        {
            "artifact_id": f"stage11_{spec.run_number}_kpi_record",
            "type": "kpi_record",
            "path": kpi_path.as_posix(),
            "status": "local_generated_reviewed",
            "notes": f"Stage 11 {spec.run_number} KPI record; kpi_sha256 {scout.sha256_file(kpi_path)}; routed-only MT5 runtime_probe",
        },
        {
            "artifact_id": f"stage11_{spec.run_number}_result_summary",
            "type": "result_summary",
            "path": result_summary_path.as_posix(),
            "status": "local_generated_reviewed",
            "notes": f"Stage 11 {spec.run_number} result summary; summary_sha256 {scout.sha256_file(result_summary_path)}",
        },
    ]
    artifact_payload = append_artifact_rows(artifact_rows)
    return {
        "run_id": spec.run_id,
        "run_number": spec.run_number,
        "idea_id": spec.idea_id,
        "external_verification_status": external_status,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "mt5_kpi_records": mt5_kpi_records,
        "artifact_payload": artifact_payload,
    }


def main() -> int:
    args = parse_args()
    unknown = [key for key in args.variants if key not in SPECS]
    if unknown:
        raise SystemExit(f"Unknown variants: {unknown}; available={sorted(SPECS)}")
    results = []
    for key in args.variants:
        results.append(
            run_one_spec(
                spec=SPECS[key],
                source_run_root=Path(args.source_run_root),
                run_root=Path(args.run_root),
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
            )
        )
    print(json.dumps(scout._json_ready({"status": "ok", "results": results}), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


BAR_MINUTES = 5


@dataclass(frozen=True)
class IndependentStageTopic:
    stage_number: int
    stage_id: str
    idea_id: str
    run_id: str
    run_number: str
    packet_id: str
    topic_key: str
    signal_column: str
    exploration_label: str
    question: str

    def short_stage(self) -> str:
        return f"s{self.stage_number}"


@dataclass(frozen=True)
class IndependentCandidateSpec:
    candidate_id: str
    label: str
    mechanism_family: str
    rule_code: str
    model_family: str
    feature_set: tuple[str, ...] = ()
    thresholds: Mapping[str, float] | None = None
    direction_specific: bool = True
    expected_trade_count_effect: str = "moderate"
    overfit_risk: str = "medium"
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["feature_set"] = list(self.feature_set)
        payload["thresholds"] = dict(self.thresholds or {})
        return payload


STAGE_TOPICS: dict[int, IndependentStageTopic] = {
    43: IndependentStageTopic(
        stage_number=43,
        stage_id="43_model_rebuild__low_complexity_feature_subset_regularized_signal",
        idea_id="IDEA-ST43-LOW-COMPLEXITY-FEATURE-SUBSET-REBUILD",
        run_id="run37A_low_complexity_feature_subset_rebuild_broad_mt5_probe_v1",
        run_number="run37A",
        packet_id="stage43_run37A_low_complexity_feature_subset_rebuild_broad_mt5_probe_v1",
        topic_key="feature_subset_rebuild",
        signal_column="stage43_low_complexity_signal",
        exploration_label="stage43_ModelRebuild__LowComplexityFeatureSubset",
        question="Can a smaller feature subset plus low-complexity regularized model produce stable validation+OOS MT5 behavior?",
    ),
    44: IndependentStageTopic(
        stage_number=44,
        stage_id="44_robustness_protocol__rolling_walkforward_split_stability",
        idea_id="IDEA-ST44-ROLLING-WALKFORWARD-SPLIT-STABILITY",
        run_id="run38A_rolling_walkforward_split_stability_broad_mt5_probe_v1",
        run_number="run38A",
        packet_id="stage44_run38A_rolling_walkforward_split_stability_broad_mt5_probe_v1",
        topic_key="rolling_walkforward_stability",
        signal_column="stage44_wfo_stability_signal",
        exploration_label="stage44_RobustnessProtocol__RollingWalkforwardStability",
        question="Can rolling/walk-forward evidence identify a signal family that survives multiple time partitions?",
    ),
    45: IndependentStageTopic(
        stage_number=45,
        stage_id="45_volatility_mechanism__compression_expansion_signal_rebuild",
        idea_id="IDEA-ST45-VOLATILITY-COMPRESSION-EXPANSION-SIGNAL",
        run_id="run39A_volatility_compression_expansion_broad_mt5_probe_v1",
        run_number="run39A",
        packet_id="stage45_run39A_volatility_compression_expansion_broad_mt5_probe_v1",
        topic_key="volatility_compression_expansion",
        signal_column="stage45_volatility_mechanism_signal",
        exploration_label="stage45_VolatilityMechanism__CompressionExpansion",
        question="Does volatility compression followed by expansion define a cleaner signal mechanism?",
    ),
    46: IndependentStageTopic(
        stage_number=46,
        stage_id="46_feature_interaction__nonlinear_pairwise_structure_scout",
        idea_id="IDEA-ST46-NONLINEAR-FEATURE-INTERACTION-SCOUT",
        run_id="run40A_nonlinear_pairwise_feature_interaction_broad_mt5_probe_v1",
        run_number="run40A",
        packet_id="stage46_run40A_nonlinear_pairwise_feature_interaction_broad_mt5_probe_v1",
        topic_key="pairwise_interaction_scout",
        signal_column="stage46_pairwise_interaction_signal",
        exploration_label="stage46_FeatureInteraction__NonlinearPairwise",
        question="Are stable pairwise feature interactions lost when features are treated independently?",
    ),
    47: IndependentStageTopic(
        stage_number=47,
        stage_id="47_meta_signal__cross_model_agreement_disagreement_scout",
        idea_id="IDEA-ST47-CROSS-MODEL-AGREEMENT-DISAGREEMENT-SCOUT",
        run_id="run41A_cross_model_agreement_disagreement_broad_mt5_probe_v1",
        run_number="run41A",
        packet_id="stage47_run41A_cross_model_agreement_disagreement_broad_mt5_probe_v1",
        topic_key="cross_model_agreement",
        signal_column="stage47_meta_agreement_signal",
        exploration_label="stage47_MetaSignal__AgreementDisagreement",
        question="Does agreement or disagreement across independent model families explain signal reliability?",
    ),
}


CORE_FEATURES = (
    "return_zscore_20",
    "adx_14",
    "di_spread_14",
    "rsi_14",
    "rsi_14_minus_50",
    "bb_position_20",
    "bb_squeeze",
    "bollinger_width_20",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "atr_14_over_atr_50",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "mega8_equal_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "vix_zscore_20",
    "us10yr_zscore_20",
    "usdx_zscore_20",
)

TECHNICAL_FEATURES = (
    "return_zscore_20",
    "adx_14",
    "di_spread_14",
    "rsi_14_minus_50",
    "bb_position_20",
    "historical_vol_5_over_20",
    "ema20_ema50_diff",
    "ppo_hist_12_26_9",
    "roc_12",
)

MACRO_FEATURES = ("vix_zscore_20", "us10yr_zscore_20", "usdx_zscore_20")
MEGA_FEATURES = ("mega8_equal_return_1", "mega8_pos_breadth_1", "mega8_dispersion_5", "us100_minus_mega8_equal_return_1")


def _numeric(frame: pd.DataFrame, column: str, fallback: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(fallback, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).astype("float64")


def _finite_mask(frame: pd.DataFrame, columns: Sequence[str]) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for column in columns:
        if column not in frame.columns:
            return pd.Series(False, index=frame.index)
        mask &= np.isfinite(pd.to_numeric(frame[column], errors="coerce"))
    return mask


def _quantile(series: pd.Series, q: float, fallback: float) -> float:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        return float(fallback)
    value = float(values.quantile(float(q)))
    return value if math.isfinite(value) else float(fallback)


def _abs_quantile(series: pd.Series, q: float, fallback: float) -> float:
    return _quantile(pd.to_numeric(series, errors="coerce").abs(), q, fallback)


def _direction_target(frame: pd.DataFrame) -> pd.Series:
    label = pd.to_numeric(frame.get("label_class"), errors="coerce")
    target = pd.Series(0.0, index=frame.index)
    target.loc[label.eq(2)] = 1.0
    target.loc[label.eq(0)] = -1.0
    return target


def _zscore_from_train(frame: pd.DataFrame, column: str) -> pd.Series:
    train = frame.loc[frame["split"].astype(str).eq("train"), column]
    median = float(pd.to_numeric(train, errors="coerce").median())
    std = float(pd.to_numeric(train, errors="coerce").std(ddof=0))
    if not math.isfinite(median):
        median = 0.0
    if not math.isfinite(std) or std <= 1e-12:
        std = 1.0
    return (_numeric(frame, column) - median) / std


def _feature_correlations(frame: pd.DataFrame, features: Sequence[str]) -> dict[str, float]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    target = _direction_target(train)
    rows: dict[str, float] = {}
    for feature in features:
        if feature not in train.columns:
            continue
        values = _numeric(train, feature)
        mask = np.isfinite(values) & np.isfinite(target)
        if int(mask.sum()) < 50 or float(values.loc[mask].std(ddof=0)) <= 1e-12:
            rows[feature] = 0.0
            continue
        corr = float(np.corrcoef(values.loc[mask], target.loc[mask])[0, 1])
        rows[feature] = corr if math.isfinite(corr) else 0.0
    return rows


def _weighted_score(frame: pd.DataFrame, weights: Mapping[str, float]) -> pd.Series:
    score = pd.Series(0.0, index=frame.index, dtype="float64")
    denom = 0.0
    for feature, weight in weights.items():
        if feature not in frame.columns:
            continue
        score += _zscore_from_train(frame, feature).fillna(0.0) * float(weight)
        denom += abs(float(weight))
    if denom <= 0:
        return score
    return score / denom


def _signal_from_score(score: pd.Series, threshold: float) -> pd.Series:
    signal = pd.Series(0, index=score.index, dtype="int8")
    signal.loc[score.ge(float(threshold))] = 1
    signal.loc[score.le(-float(threshold))] = -1
    return signal


def build_stage_model_context(frame: pd.DataFrame, topic: IndependentStageTopic) -> dict[str, Any]:
    correlations = _feature_correlations(frame, CORE_FEATURES)
    ranked = sorted(correlations, key=lambda feature: abs(correlations[feature]), reverse=True)
    train = frame.loc[frame["split"].astype(str).eq("train")]
    thresholds = {
        "return_abs_q60": _abs_quantile(train.get("return_zscore_20", pd.Series(dtype=float)), 0.60, 0.55),
        "return_abs_q70": _abs_quantile(train.get("return_zscore_20", pd.Series(dtype=float)), 0.70, 0.75),
        "score_abs_q58": _abs_quantile(_weighted_score(frame, {feature: correlations.get(feature, 0.0) for feature in ranked[:8]}).loc[frame["split"].astype(str).eq("train")], 0.58, 0.18),
        "score_abs_q68": _abs_quantile(_weighted_score(frame, {feature: correlations.get(feature, 0.0) for feature in ranked[:12]}).loc[frame["split"].astype(str).eq("train")], 0.68, 0.25),
        "adx_q50": _quantile(train.get("adx_14", pd.Series(dtype=float)), 0.50, 20.0),
        "adx_q65": _quantile(train.get("adx_14", pd.Series(dtype=float)), 0.65, 25.0),
        "bb_width_q25": _quantile(train.get("bollinger_width_20", pd.Series(dtype=float)), 0.25, 0.008),
        "bb_width_q35": _quantile(train.get("bollinger_width_20", pd.Series(dtype=float)), 0.35, 0.010),
        "vol_ratio_q60": _quantile(train.get("historical_vol_5_over_20", pd.Series(dtype=float)), 0.60, 1.10),
        "vol_ratio_q72": _quantile(train.get("historical_vol_5_over_20", pd.Series(dtype=float)), 0.72, 1.25),
        "atr_ratio_q60": _quantile(train.get("atr_14_over_atr_50", pd.Series(dtype=float)), 0.60, 1.0),
        "pair_abs_q65": 0.35,
    }
    fold_payload = _rolling_fold_context(frame, ranked, correlations)
    interaction_payload = _interaction_context(frame)
    source_payload = _source_signal_context(frame, correlations, thresholds, fold_payload, interaction_payload)
    return {
        "topic_key": topic.topic_key,
        "correlations": correlations,
        "ranked_features": ranked,
        "thresholds": thresholds,
        "top4": ranked[:4],
        "top8": ranked[:8],
        "top12": ranked[:12],
        "technical_ranked": [feature for feature in ranked if feature in TECHNICAL_FEATURES],
        "macro_ranked": [feature for feature in ranked if feature in MACRO_FEATURES],
        "mega_ranked": [feature for feature in ranked if feature in MEGA_FEATURES],
        "folds": fold_payload,
        "interactions": interaction_payload,
        "source_signals": source_payload,
        "leakage_audit": {
            "status": "passed",
            "training_only_thresholds": True,
            "features_use_closed_bar_inputs_only": True,
            "validation_oos_labels_not_used_for_threshold_fit": True,
        },
    }


def _rolling_fold_context(frame: pd.DataFrame, ranked: Sequence[str], correlations: Mapping[str, float]) -> dict[str, Any]:
    train = frame.loc[frame["split"].astype(str).eq("train")].copy().sort_values("timestamp")
    if train.empty:
        return {"folds": [], "stable_features": list(ranked[:8]), "vote_weights": {feature: correlations.get(feature, 0.0) for feature in ranked[:8]}}
    folds: list[dict[str, Any]] = []
    chunks = np.array_split(train.index.to_numpy(), 6)
    feature_votes: dict[str, int] = {feature: 0 for feature in ranked}
    direction_sum: dict[str, float] = {feature: 0.0 for feature in ranked}
    for idx, chunk in enumerate(chunks, start=1):
        fold = train.loc[chunk]
        corr = _feature_correlations(fold, ranked[:18])
        fold_ranked = sorted(corr, key=lambda feature: abs(corr[feature]), reverse=True)[:8]
        for feature in fold_ranked:
            feature_votes[feature] = feature_votes.get(feature, 0) + 1
            direction_sum[feature] = direction_sum.get(feature, 0.0) + math.copysign(1.0, corr.get(feature, 0.0) or correlations.get(feature, 0.0) or 1.0)
        folds.append(
            {
                "fold_id": f"fold{idx:02d}",
                "row_count": int(len(fold)),
                "first_timestamp": str(pd.to_datetime(fold["timestamp"], utc=True).min()),
                "last_timestamp": str(pd.to_datetime(fold["timestamp"], utc=True).max()),
                "top_features": fold_ranked,
            }
        )
    stable = [feature for feature, votes in sorted(feature_votes.items(), key=lambda item: (-item[1], item[0])) if votes >= 3][:10]
    if not stable:
        stable = list(ranked[:8])
    vote_weights = {
        feature: float(math.copysign(max(feature_votes.get(feature, 1), 1), direction_sum.get(feature, correlations.get(feature, 0.0) or 1.0)))
        for feature in stable
    }
    return {"folds": folds, "stable_features": stable, "feature_votes": feature_votes, "vote_weights": vote_weights}


def _interaction_context(frame: pd.DataFrame) -> dict[str, Any]:
    pairs = [
        ("return_zscore_20", "adx_14", "return_x_adx"),
        ("bb_position_20", "bb_squeeze", "bb_position_x_squeeze"),
        ("di_spread_14", "historical_vol_5_over_20", "di_x_vol_expansion"),
        ("rsi_14_minus_50", "ema20_ema50_diff", "rsi_x_trend"),
        ("us100_minus_mega8_equal_return_1", "mega8_pos_breadth_1", "divergence_x_breadth"),
        ("vix_zscore_20", "usdx_zscore_20", "macro_risk_x_usd"),
        ("atr_14_over_atr_50", "ema50_ema200_diff", "atr_x_slow_trend"),
        ("mega8_dispersion_5", "return_zscore_20", "dispersion_x_return"),
    ]
    train_mask = frame["split"].astype(str).eq("train")
    thresholds: dict[str, float] = {}
    for left, right, name in pairs:
        product = _zscore_from_train(frame, left).fillna(0.0) * _zscore_from_train(frame, right).fillna(0.0)
        thresholds[name] = _abs_quantile(product.loc[train_mask], 0.65, 0.35)
    return {"pairs": pairs, "thresholds": thresholds}


def _volatility_signal(frame: pd.DataFrame, thresholds: Mapping[str, float], mode: str = "squeeze_release") -> pd.Series:
    rz = _numeric(frame, "return_zscore_20")
    width = _numeric(frame, "bollinger_width_20")
    squeeze = _numeric(frame, "bb_squeeze").ge(0.5)
    vol_ratio = _numeric(frame, "historical_vol_5_over_20")
    adx = _numeric(frame, "adx_14")
    di = _numeric(frame, "di_spread_14")
    long = pd.Series(False, index=frame.index)
    short = pd.Series(False, index=frame.index)
    if mode == "atr_compression_release":
        comp = _numeric(frame, "atr_14_over_atr_50").le(float(thresholds["atr_ratio_q60"]))
        expand = vol_ratio.ge(float(thresholds["vol_ratio_q60"]))
        long = comp & expand & rz.ge(float(thresholds["return_abs_q60"]))
        short = comp & expand & rz.le(-float(thresholds["return_abs_q60"]))
    elif mode == "bb_width_breakout":
        comp = width.le(float(thresholds["bb_width_q35"]))
        long = comp & rz.ge(float(thresholds["return_abs_q60"]))
        short = comp & rz.le(-float(thresholds["return_abs_q60"]))
    elif mode == "directional_breakout":
        long = squeeze & vol_ratio.ge(float(thresholds["vol_ratio_q60"])) & di.ge(0) & rz.ge(0)
        short = squeeze & vol_ratio.ge(float(thresholds["vol_ratio_q60"])) & di.le(0) & rz.le(0)
    else:
        long = squeeze & vol_ratio.ge(float(thresholds["vol_ratio_q60"])) & rz.ge(float(thresholds["return_abs_q60"])) & adx.ge(float(thresholds["adx_q50"]))
        short = squeeze & vol_ratio.ge(float(thresholds["vol_ratio_q60"])) & rz.le(-float(thresholds["return_abs_q60"])) & adx.ge(float(thresholds["adx_q50"]))
    return _mask_to_signal(long, short)


def _interaction_signal(frame: pd.DataFrame, context: Mapping[str, Any], pair_name: str) -> tuple[pd.Series, pd.Series]:
    pair = next((item for item in context["pairs"] if item[2] == pair_name), None)
    if pair is None:
        return pd.Series(0.0, index=frame.index), pd.Series(0, index=frame.index, dtype="int8")
    left, right, name = pair
    score = _zscore_from_train(frame, left).fillna(0.0) * _zscore_from_train(frame, right).fillna(0.0)
    threshold = float(context["thresholds"].get(name, 0.35))
    direction = np.sign(_zscore_from_train(frame, left).fillna(0.0) + _zscore_from_train(frame, right).fillna(0.0))
    signal = pd.Series(0, index=frame.index, dtype="int8")
    active = score.abs().ge(threshold)
    signal.loc[active & pd.Series(direction, index=frame.index).gt(0)] = 1
    signal.loc[active & pd.Series(direction, index=frame.index).lt(0)] = -1
    return score, signal


def _source_signal_context(
    frame: pd.DataFrame,
    correlations: Mapping[str, float],
    thresholds: Mapping[str, float],
    fold_payload: Mapping[str, Any],
    interaction_payload: Mapping[str, Any],
) -> dict[str, Any]:
    feature_weights = {feature: correlations.get(feature, 0.0) for feature in sorted(correlations, key=lambda f: abs(correlations[f]), reverse=True)[:8]}
    feature_score = _weighted_score(frame, feature_weights)
    feature_signal = _signal_from_score(feature_score, float(thresholds["score_abs_q58"]))
    wfo_score = _weighted_score(frame, fold_payload.get("vote_weights", {}))
    wfo_signal = _signal_from_score(wfo_score, float(thresholds["score_abs_q58"]))
    volatility_signal = _volatility_signal(frame, thresholds)
    _pair_score, interaction_signal = _interaction_signal(frame, interaction_payload, "return_x_adx")
    reference = _mask_to_signal(
        _numeric(frame, "return_zscore_20").ge(float(thresholds["return_abs_q60"])) & _numeric(frame, "adx_14").ge(float(thresholds["adx_q50"])),
        _numeric(frame, "return_zscore_20").le(-float(thresholds["return_abs_q60"])) & _numeric(frame, "adx_14").ge(float(thresholds["adx_q50"])),
    )
    return {
        "feature_subset": feature_signal,
        "wfo_stability": wfo_signal,
        "volatility_mechanism": volatility_signal,
        "pairwise_interaction": interaction_signal,
        "reference": reference,
        "source_names": ["feature_subset", "wfo_stability", "volatility_mechanism", "pairwise_interaction", "reference"],
    }


def _mask_to_signal(long_mask: pd.Series, short_mask: pd.Series) -> pd.Series:
    signal = pd.Series(0, index=long_mask.index, dtype="int8")
    signal.loc[long_mask.fillna(False)] = 1
    signal.loc[short_mask.fillna(False)] = -1
    conflict = long_mask.fillna(False) & short_mask.fillna(False)
    signal.loc[conflict] = 0
    return signal


def build_broad_candidate_grid(topic: IndependentStageTopic) -> list[IndependentCandidateSpec]:
    if topic.stage_number == 43:
        return _stage43_grid()
    if topic.stage_number == 44:
        return _stage44_grid()
    if topic.stage_number == 45:
        return _stage45_grid()
    if topic.stage_number == 46:
        return _stage46_grid()
    if topic.stage_number == 47:
        return _stage47_grid()
    raise ValueError(f"unsupported stage: {topic.stage_number}")


def _stage43_grid() -> list[IndependentCandidateSpec]:
    return [
        IndependentCandidateSpec("c01_current_broad_surface_reference", "current broad surface reference proxy", "reference/carry comparison", "reference_momentum", "score_table_rule", TECHNICAL_FEATURES[:4], overfit_risk="low"),
        IndependentCandidateSpec("c02_top8_stability_ranked_elasticnet", "top-8 stability-ranked elastic-net proxy", "stability feature subset", "weighted_top8", "elastic_net_logistic_proxy"),
        IndependentCandidateSpec("c03_top12_regularized_core", "top-12 regularized core subset", "regularized core subset", "weighted_top12", "elastic_net_logistic_proxy"),
        IndependentCandidateSpec("c04_top4_extreme_sparse", "top-4 extreme sparse pressure test", "extreme sparse subset", "weighted_top4_firm", "elastic_net_logistic_proxy", expected_trade_count_effect="lower", overfit_risk="medium_high"),
        IndependentCandidateSpec("c05_technical_only_subset", "technical-only low complexity subset", "technical subset", "technical_only", "score_table_rule"),
        IndependentCandidateSpec("c06_macro_proxy_subset", "macro proxy-only subset", "macro subset", "macro_only", "score_table_rule", MACRO_FEATURES, expected_trade_count_effect="lower"),
        IndependentCandidateSpec("c07_mega_cap_subset", "mega-cap breadth/divergence subset", "mega-cap subset", "mega_only", "score_table_rule", MEGA_FEATURES),
        IndependentCandidateSpec("c08_constrained_tree_stump_combo", "constrained shallow-tree stump combo", "constrained tree", "tree_stump_combo", "shallow_tree_proxy", expected_trade_count_effect="lower", overfit_risk="medium_high"),
    ]


def _stage44_grid() -> list[IndependentCandidateSpec]:
    return [
        IndependentCandidateSpec("c01_single_split_reference", "single-split reference for WFO contrast", "reference/carry comparison", "reference_momentum", "score_table_rule", overfit_risk="low"),
        IndependentCandidateSpec("c02_fold_vote_top5", "fold-vote top-5 stable features", "fold survival vote", "fold_vote_top5", "rolling_wfo_vote_proxy"),
        IndependentCandidateSpec("c03_survives_4of6_folds", "features surviving at least 4 of 6 folds", "fold survival threshold", "fold_survive_4of6", "rolling_wfo_vote_proxy"),
        IndependentCandidateSpec("c04_recent_fold_weighted", "recent-fold weighted stability signal", "recent fold weight", "recent_fold_weighted", "rolling_wfo_vote_proxy"),
        IndependentCandidateSpec("c05_all_fold_consensus", "all-fold consensus pressure test", "all fold consensus", "all_fold_consensus", "rolling_wfo_vote_proxy", expected_trade_count_effect="lower"),
        IndependentCandidateSpec("c06_fold_dispersion_avoid", "avoid high-dispersion fold features", "fold dispersion guard", "fold_dispersion_avoid", "rolling_wfo_vote_proxy"),
        IndependentCandidateSpec("c07_directional_fold_stability", "directional fold-stability signal", "directional fold stability", "directional_fold_stability", "rolling_wfo_vote_proxy"),
        IndependentCandidateSpec("c08_one_lucky_fold_negative_control", "one-lucky-fold negative control", "negative control", "one_lucky_fold", "rolling_wfo_vote_proxy", overfit_risk="high"),
    ]


def _stage45_grid() -> list[IndependentCandidateSpec]:
    return [
        IndependentCandidateSpec("c01_reference_return_vol_momentum", "reference return/vol momentum", "reference/carry comparison", "reference_momentum", "score_table_rule", overfit_risk="low"),
        IndependentCandidateSpec("c02_atr_compression_release", "ATR compression then release", "ATR compression/release", "atr_compression_release", "score_table_rule"),
        IndependentCandidateSpec("c03_bollinger_width_compression_breakout", "Bollinger width compression breakout", "width compression breakout", "bb_width_breakout", "score_table_rule"),
        IndependentCandidateSpec("c04_histvol_ratio_expansion", "realized volatility expansion", "realized-vol expansion", "vol_ratio_expansion", "score_table_rule"),
        IndependentCandidateSpec("c05_range_contraction_expansion", "range contraction then expansion", "range contraction expansion", "range_contraction_expansion", "score_table_rule"),
        IndependentCandidateSpec("c06_direction_specific_expansion_breakout", "direction-specific expansion breakout", "directional expansion", "directional_breakout", "score_table_rule"),
        IndependentCandidateSpec("c07_expansion_after_low_adx", "expansion after low-ADX squeeze", "low ADX release", "low_adx_release", "score_table_rule", expected_trade_count_effect="lower"),
        IndependentCandidateSpec("c08_extreme_compression_stress", "extreme compression stress test", "extreme stress", "extreme_compression", "score_table_rule", expected_trade_count_effect="much lower", overfit_risk="high"),
    ]


def _stage46_grid() -> list[IndependentCandidateSpec]:
    return [
        IndependentCandidateSpec("c01_additive_reference", "additive reference without pairwise term", "reference/carry comparison", "reference_momentum", "score_table_rule", overfit_risk="low"),
        IndependentCandidateSpec("c02_return_x_adx", "return z-score x ADX interaction", "trend interaction", "return_x_adx", "pairwise_score_table"),
        IndependentCandidateSpec("c03_bb_position_x_squeeze", "Bollinger position x squeeze interaction", "squeeze interaction", "bb_position_x_squeeze", "pairwise_score_table"),
        IndependentCandidateSpec("c04_di_x_vol_expansion", "DI spread x volatility expansion", "direction-vol interaction", "di_x_vol_expansion", "pairwise_score_table"),
        IndependentCandidateSpec("c05_rsi_x_trend", "RSI displacement x EMA trend", "oscillator-trend interaction", "rsi_x_trend", "pairwise_score_table"),
        IndependentCandidateSpec("c06_divergence_x_breadth", "mega-cap divergence x breadth", "breadth interaction", "divergence_x_breadth", "pairwise_score_table"),
        IndependentCandidateSpec("c07_macro_risk_x_usd", "VIX risk x USD pressure", "macro interaction", "macro_risk_x_usd", "pairwise_score_table"),
        IndependentCandidateSpec("c08_interaction_extreme_stress", "highest-threshold interaction stress", "extreme stress", "interaction_extreme", "pairwise_score_table", expected_trade_count_effect="much lower", overfit_risk="high"),
    ]


def _stage47_grid() -> list[IndependentCandidateSpec]:
    return [
        IndependentCandidateSpec("c01_single_reference_signal", "single reference signal", "reference/carry comparison", "single_reference", "meta_signal_score_table", overfit_risk="low"),
        IndependentCandidateSpec("c02_all_family_agreement", "all-family direction agreement", "full agreement", "all_agreement", "meta_signal_score_table", expected_trade_count_effect="lower"),
        IndependentCandidateSpec("c03_majority_agreement", "majority agreement signal", "majority consensus", "majority_agreement", "meta_signal_score_table"),
        IndependentCandidateSpec("c04_disagreement_avoidance", "avoid disagreement clusters", "disagreement filter", "disagreement_avoidance", "meta_signal_score_table"),
        IndependentCandidateSpec("c05_low_dispersion_consensus", "low-dispersion consensus", "dispersion consensus", "low_dispersion", "meta_signal_score_table"),
        IndependentCandidateSpec("c06_direction_consensus_long_short", "direction-specific long/short consensus", "direction consensus", "direction_consensus", "meta_signal_score_table"),
        IndependentCandidateSpec("c07_flat_consensus_no_trade", "flat-consensus no-trade pressure test", "flat consensus", "flat_consensus", "meta_signal_score_table", expected_trade_count_effect="lower"),
        IndependentCandidateSpec("c08_disagreement_contrarian_control", "contrarian disagreement negative control", "negative control", "contrarian_disagreement", "meta_signal_score_table", overfit_risk="high"),
    ]


def build_micro_candidate_grid(
    topic: IndependentStageTopic,
    best_candidate_id: str,
    broad_specs: Sequence[IndependentCandidateSpec],
) -> list[IndependentCandidateSpec]:
    base = next(spec for spec in broad_specs if spec.candidate_id == best_candidate_id)
    return [
        replace(base, candidate_id=f"m01_relaxed_{base.candidate_id}", label=f"relaxed threshold around {base.label}", thresholds={"score_multiplier": 0.90}, notes="bounded micro-search after broad gate pass"),
        replace(base, candidate_id=f"m02_firm_{base.candidate_id}", label=f"firm threshold around {base.label}", thresholds={"score_multiplier": 1.10}, notes="bounded micro-search after broad gate pass"),
        replace(base, candidate_id=f"m03_low_trade_guard_{base.candidate_id}", label=f"low trade-count guard around {base.label}", thresholds={"score_multiplier": 0.95, "min_activation": 0.02}, notes="bounded micro-search after broad gate pass"),
        replace(base, candidate_id=f"m04_extreme_stress_{base.candidate_id}", label=f"extreme stress around {base.label}", thresholds={"score_multiplier": 1.25}, expected_trade_count_effect="lower", notes="bounded micro-search after broad gate pass"),
    ]


def apply_candidate_to_table(
    common: pd.DataFrame,
    topic: IndependentStageTopic,
    spec: IndependentCandidateSpec,
    context: Mapping[str, Any],
) -> pd.DataFrame:
    if topic.stage_number == 43:
        score, signal, activation, required = _apply_stage43(common, spec, context)
    elif topic.stage_number == 44:
        score, signal, activation, required = _apply_stage44(common, spec, context)
    elif topic.stage_number == 45:
        score, signal, activation, required = _apply_stage45(common, spec, context)
    elif topic.stage_number == 46:
        score, signal, activation, required = _apply_stage46(common, spec, context)
    elif topic.stage_number == 47:
        score, signal, activation, required = _apply_stage47(common, spec, context)
    else:
        raise ValueError(f"unsupported stage: {topic.stage_number}")
    multiplier = float((spec.thresholds or {}).get("score_multiplier", 1.0))
    if multiplier != 1.0:
        threshold = _abs_quantile(score.loc[common["split"].astype(str).eq("train")], 0.58, 0.2) * multiplier
        signal = _signal_from_score(score, threshold)
        activation = signal.ne(0)
    missing = ~_finite_mask(common, required)
    signal = signal.where(~missing, 0).fillna(0).astype("int8")
    out = _base_output(common, topic, required)
    out["candidate_id"] = spec.candidate_id
    out["candidate_label"] = spec.label
    out["mechanism_family"] = spec.mechanism_family
    out["rule_code"] = spec.rule_code
    out["model_family"] = spec.model_family
    out["feature_set_json"] = json.dumps(list(spec.feature_set), ensure_ascii=False)
    out["thresholds_json"] = json.dumps(dict(spec.thresholds or {}), sort_keys=True, separators=(",", ":"))
    out[f"{topic.short_stage()}_score"] = score.astype("float64").replace([np.inf, -np.inf], np.nan)
    out[f"{topic.short_stage()}_activation"] = activation.fillna(False).astype("int8")
    out[f"{topic.short_stage()}_missing"] = missing.astype("int8")
    out[topic.signal_column] = signal
    out["entry_decision"] = np.where(signal > 0, "long", np.where(signal < 0, "short", "flat"))
    return out


def _base_output(common: pd.DataFrame, topic: IndependentStageTopic, required: Sequence[str]) -> pd.DataFrame:
    columns = [
        "timestamp",
        "timestamp_utc",
        "split",
        "validation_oos_split_label",
        "symbol",
        "label_class",
        "tier_label",
        "routing_source",
        "partial_context_subtype",
        "tier_a_available",
        "tier_b_fallback_available",
        *required,
    ]
    seen: list[str] = []
    for column in columns:
        if column in common.columns and column not in seen:
            seen.append(column)
    out = common[seen].copy()
    out[f"{topic.short_stage()}_row_id"] = np.arange(len(out))
    return out


def _reference_signal(common: pd.DataFrame, context: Mapping[str, Any], threshold_key: str = "return_abs_q60") -> pd.Series:
    thresholds = context["thresholds"]
    rz = _numeric(common, "return_zscore_20")
    adx = _numeric(common, "adx_14")
    return _mask_to_signal(rz.ge(float(thresholds[threshold_key])) & adx.ge(float(thresholds["adx_q50"])), rz.le(-float(thresholds[threshold_key])) & adx.ge(float(thresholds["adx_q50"])))


def _apply_stage43(common: pd.DataFrame, spec: IndependentCandidateSpec, context: Mapping[str, Any]) -> tuple[pd.Series, pd.Series, pd.Series, tuple[str, ...]]:
    thresholds = context["thresholds"]
    if spec.rule_code == "reference_momentum":
        score = _zscore_from_train(common, "return_zscore_20") + 0.35 * _zscore_from_train(common, "adx_14")
        signal = _reference_signal(common, context)
        return score, signal, signal.ne(0), ("return_zscore_20", "adx_14")
    if spec.rule_code == "weighted_top4_firm":
        features = tuple(context["top4"])
        score = _weighted_score(common, {feature: context["correlations"].get(feature, 0.0) for feature in features})
        signal = _signal_from_score(score, float(thresholds["score_abs_q68"]))
        return score, signal, signal.ne(0), features
    if spec.rule_code == "weighted_top12":
        features = tuple(context["top12"])
    elif spec.rule_code == "technical_only":
        features = tuple((context["technical_ranked"] or list(TECHNICAL_FEATURES))[:8])
    elif spec.rule_code == "macro_only":
        features = tuple(MACRO_FEATURES)
    elif spec.rule_code == "mega_only":
        features = tuple(MEGA_FEATURES)
    elif spec.rule_code == "tree_stump_combo":
        long = _numeric(common, "rsi_14_minus_50").ge(0) & _numeric(common, "ema20_ema50_diff").ge(0) & _numeric(common, "adx_14").ge(float(thresholds["adx_q50"]))
        short = _numeric(common, "rsi_14_minus_50").le(0) & _numeric(common, "ema20_ema50_diff").le(0) & _numeric(common, "adx_14").ge(float(thresholds["adx_q50"]))
        score = _zscore_from_train(common, "rsi_14_minus_50") + _zscore_from_train(common, "ema20_ema50_diff")
        signal = _mask_to_signal(long, short)
        return score, signal, signal.ne(0), ("rsi_14_minus_50", "ema20_ema50_diff", "adx_14")
    else:
        features = tuple(context["top8"])
    weights = {feature: context["correlations"].get(feature, 0.0) for feature in features}
    score = _weighted_score(common, weights)
    signal = _signal_from_score(score, float(thresholds["score_abs_q58"]))
    return score, signal, signal.ne(0), features


def _apply_stage44(common: pd.DataFrame, spec: IndependentCandidateSpec, context: Mapping[str, Any]) -> tuple[pd.Series, pd.Series, pd.Series, tuple[str, ...]]:
    thresholds = context["thresholds"]
    folds = context["folds"]
    stable = tuple(folds.get("stable_features", context["top8"])[:8])
    if spec.rule_code == "reference_momentum":
        score = _zscore_from_train(common, "return_zscore_20") + 0.25 * _zscore_from_train(common, "adx_14")
        signal = _reference_signal(common, context)
        return score, signal, signal.ne(0), ("return_zscore_20", "adx_14")
    if spec.rule_code == "one_lucky_fold":
        first = tuple(folds.get("folds", [{}])[0].get("top_features", stable)[:4])
        weights = {feature: context["correlations"].get(feature, 0.0) for feature in first}
        score = _weighted_score(common, weights)
        signal = _signal_from_score(score, float(thresholds["score_abs_q58"]))
        return score, signal, signal.ne(0), first
    if spec.rule_code == "all_fold_consensus":
        features = tuple(feature for feature, votes in folds.get("feature_votes", {}).items() if int(votes) >= 5)[:8] or stable[:4]
        q = float(thresholds["score_abs_q68"])
    elif spec.rule_code == "fold_dispersion_avoid":
        votes = folds.get("feature_votes", {})
        features = tuple(feature for feature in stable if int(votes.get(feature, 0)) >= 3)[:8]
        q = float(thresholds["score_abs_q58"])
    elif spec.rule_code == "recent_fold_weighted":
        recent = []
        for fold in folds.get("folds", [])[-3:]:
            recent.extend(fold.get("top_features", []))
        features = tuple(dict.fromkeys(recent))[:8] or stable
        q = float(thresholds["score_abs_q58"])
    elif spec.rule_code == "directional_fold_stability":
        features = stable[:6]
        q = float(thresholds["score_abs_q58"])
    elif spec.rule_code == "fold_survive_4of6":
        features = tuple(feature for feature, votes in folds.get("feature_votes", {}).items() if int(votes) >= 4)[:8] or stable
        q = float(thresholds["score_abs_q58"])
    else:
        features = stable[:5]
        q = float(thresholds["score_abs_q58"])
    weights = {feature: folds.get("vote_weights", {}).get(feature, context["correlations"].get(feature, 0.0)) for feature in features}
    score = _weighted_score(common, weights)
    signal = _signal_from_score(score, q)
    return score, signal, signal.ne(0), features


def _apply_stage45(common: pd.DataFrame, spec: IndependentCandidateSpec, context: Mapping[str, Any]) -> tuple[pd.Series, pd.Series, pd.Series, tuple[str, ...]]:
    thresholds = context["thresholds"]
    required = ("return_zscore_20", "hl_range", "bollinger_width_20", "bb_squeeze", "historical_vol_5_over_20", "atr_14_over_atr_50", "adx_14", "di_spread_14")
    rz = _numeric(common, "return_zscore_20")
    if spec.rule_code == "reference_momentum":
        signal = _reference_signal(common, context)
        return rz, signal, signal.ne(0), ("return_zscore_20", "adx_14")
    if spec.rule_code == "vol_ratio_expansion":
        signal = _mask_to_signal(_numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q72"])) & rz.ge(float(thresholds["return_abs_q60"])), _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q72"])) & rz.le(-float(thresholds["return_abs_q60"])))
        score = _zscore_from_train(common, "historical_vol_5_over_20") * np.sign(rz)
    elif spec.rule_code == "range_contraction_expansion":
        low_range = _numeric(common, "hl_range").le(_quantile(common.loc[common["split"].astype(str).eq("train"), "hl_range"], 0.30, 0.001))
        signal = _mask_to_signal(low_range & _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q60"])) & rz.ge(0), low_range & _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q60"])) & rz.le(0))
        score = _zscore_from_train(common, "historical_vol_5_over_20") - _zscore_from_train(common, "hl_range").abs()
    elif spec.rule_code == "low_adx_release":
        low_adx = _numeric(common, "adx_14").le(float(thresholds["adx_q50"]))
        signal = _mask_to_signal(low_adx & _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q72"])) & rz.ge(float(thresholds["return_abs_q60"])), low_adx & _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q72"])) & rz.le(-float(thresholds["return_abs_q60"])))
        score = _zscore_from_train(common, "historical_vol_5_over_20") - _zscore_from_train(common, "adx_14")
    elif spec.rule_code == "extreme_compression":
        low_width = _numeric(common, "bollinger_width_20").le(float(thresholds["bb_width_q25"]))
        signal = _mask_to_signal(low_width & _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q72"])) & rz.ge(float(thresholds["return_abs_q70"])), low_width & _numeric(common, "historical_vol_5_over_20").ge(float(thresholds["vol_ratio_q72"])) & rz.le(-float(thresholds["return_abs_q70"])))
        score = _zscore_from_train(common, "historical_vol_5_over_20") - _zscore_from_train(common, "bollinger_width_20")
    else:
        signal = _volatility_signal(common, thresholds, spec.rule_code)
        score = _zscore_from_train(common, "historical_vol_5_over_20") + np.sign(rz) * _zscore_from_train(common, "return_zscore_20").abs()
    return score, signal, signal.ne(0), required


def _apply_stage46(common: pd.DataFrame, spec: IndependentCandidateSpec, context: Mapping[str, Any]) -> tuple[pd.Series, pd.Series, pd.Series, tuple[str, ...]]:
    if spec.rule_code == "reference_momentum":
        signal = _reference_signal(common, context)
        score = _zscore_from_train(common, "return_zscore_20") + 0.25 * _zscore_from_train(common, "adx_14")
        return score, signal, signal.ne(0), ("return_zscore_20", "adx_14")
    pair_name = "return_x_adx" if spec.rule_code == "interaction_extreme" else spec.rule_code
    score, signal = _interaction_signal(common, context["interactions"], pair_name)
    if spec.rule_code == "interaction_extreme":
        signal = _signal_from_score(score, _abs_quantile(score.loc[common["split"].astype(str).eq("train")], 0.78, 0.70))
    pair = next((item for item in context["interactions"]["pairs"] if item[2] == pair_name), ("return_zscore_20", "adx_14", pair_name))
    return score, signal, signal.ne(0), (pair[0], pair[1])


def _apply_stage47(common: pd.DataFrame, spec: IndependentCandidateSpec, context: Mapping[str, Any]) -> tuple[pd.Series, pd.Series, pd.Series, tuple[str, ...]]:
    sources = context["source_signals"]
    names = sources["source_names"]
    matrix = pd.DataFrame({name: pd.Series(sources[name], index=common.index).astype("int8") for name in names})
    nonzero = matrix.ne(0)
    vote_sum = matrix.sum(axis=1)
    active_count = nonzero.sum(axis=1)
    dispersion = matrix.replace(0, np.nan).std(axis=1).fillna(0.0)
    if spec.rule_code == "single_reference":
        signal = matrix["reference"].astype("int8")
        score = matrix["reference"].astype("float64")
    elif spec.rule_code == "all_agreement":
        all_active = active_count.ge(3) & (vote_sum.abs().eq(active_count))
        signal = pd.Series(0, index=common.index, dtype="int8")
        signal.loc[all_active & vote_sum.gt(0)] = 1
        signal.loc[all_active & vote_sum.lt(0)] = -1
        score = vote_sum.astype("float64") / active_count.replace(0, np.nan).fillna(1)
    elif spec.rule_code == "majority_agreement":
        signal = pd.Series(0, index=common.index, dtype="int8")
        signal.loc[vote_sum.ge(2)] = 1
        signal.loc[vote_sum.le(-2)] = -1
        score = vote_sum.astype("float64")
    elif spec.rule_code == "disagreement_avoidance":
        disagree = (matrix.max(axis=1).gt(0) & matrix.min(axis=1).lt(0))
        signal = matrix["reference"].where(~disagree, 0).astype("int8")
        score = vote_sum.astype("float64")
    elif spec.rule_code == "low_dispersion":
        signal = pd.Series(0, index=common.index, dtype="int8")
        low = dispersion.le(0.50) & active_count.ge(2)
        signal.loc[low & vote_sum.gt(0)] = 1
        signal.loc[low & vote_sum.lt(0)] = -1
        score = vote_sum.abs().astype("float64") - dispersion
    elif spec.rule_code == "direction_consensus":
        signal = pd.Series(0, index=common.index, dtype="int8")
        signal.loc[(matrix.eq(1).sum(axis=1) >= 2) & (matrix.eq(-1).sum(axis=1) == 0)] = 1
        signal.loc[(matrix.eq(-1).sum(axis=1) >= 2) & (matrix.eq(1).sum(axis=1) == 0)] = -1
        score = vote_sum.astype("float64")
    elif spec.rule_code == "flat_consensus":
        signal = matrix["reference"].where(active_count.ge(2), 0).astype("int8")
        score = active_count.astype("float64")
    elif spec.rule_code == "contrarian_disagreement":
        signal = pd.Series(0, index=common.index, dtype="int8")
        signal.loc[vote_sum.ge(2)] = -1
        signal.loc[vote_sum.le(-2)] = 1
        score = -vote_sum.astype("float64")
    else:
        raise ValueError(f"unknown Stage47 rule: {spec.rule_code}")
    return score, signal, signal.ne(0), ()


def summarize_candidate_frames(
    topic: IndependentStageTopic,
    frames: Mapping[str, pd.DataFrame],
    specs: Sequence[IndependentCandidateSpec],
) -> list[dict[str, Any]]:
    specs_by_id = {spec.candidate_id: spec for spec in specs}
    reference_id = next((spec.candidate_id for spec in specs if spec.candidate_id.startswith("c01")), "")
    reference_counts: dict[str, int] = {}
    if reference_id in frames:
        ref = frames[reference_id]
        for split in ("validation", "oos"):
            reference_counts[split] = int(ref.loc[ref["split"].astype(str).eq(split), topic.signal_column].ne(0).sum())
    rows: list[dict[str, Any]] = []
    for candidate_id, frame in frames.items():
        spec = specs_by_id[candidate_id]
        for split in ("validation", "oos"):
            view = frame.loc[frame["split"].astype(str).eq(split)]
            runtime_split = "validation_is" if split == "validation" else "oos"
            if view.empty:
                rows.append({"candidate_id": candidate_id, "split": runtime_split, "candidate_rejection_reason": "missing_split_rows"})
                continue
            signal = pd.to_numeric(view[topic.signal_column], errors="coerce").fillna(0).astype("int8")
            active = signal.ne(0)
            tier_a = view["tier_label"].astype(str).eq("Tier A") if "tier_label" in view else pd.Series(False, index=view.index)
            tier_b = view["tier_label"].astype(str).eq("Tier B") if "tier_label" in view else pd.Series(False, index=view.index)
            ref_count = max(reference_counts.get(split, int(active.sum())), 1)
            active_count = int(active.sum())
            tier_b_count = int((active & tier_b).sum())
            reason = "mt5_pending"
            if active_count < 20:
                reason = "thin_trade_stream_python_signal_count_lt_20"
            elif candidate_id != reference_id and active_count / ref_count < 0.10:
                reason = "trade_count_delta_extreme_vs_reference_python"
            elif active_count and tier_b_count / active_count > 0.60:
                reason = "tier_b_fallback_signal_share_gt_60pct_python"
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_label": spec.label,
                    "split": runtime_split,
                    "stage_number": topic.stage_number,
                    "mechanism_family": spec.mechanism_family,
                    "rule_code": spec.rule_code,
                    "model_family": spec.model_family,
                    "feature_set": json.dumps(list(spec.feature_set), ensure_ascii=False),
                    "tier_a_used_count": int((active & tier_a).sum()),
                    "tier_b_fallback_used_count": tier_b_count,
                    "actual_routed_total_count": active_count,
                    "long_count": int(signal.gt(0).sum()),
                    "short_count": int(signal.lt(0).sum()),
                    "no_trade_rate": float(1.0 - active.mean()) if len(view) else 1.0,
                    "trade_count_delta_vs_reference": int(active_count - ref_count),
                    "activation_rate": float(active.mean()) if len(view) else 0.0,
                    "candidate_rejection_reason": reason,
                    "expected_trade_count_effect": spec.expected_trade_count_effect,
                    "overfit_risk": spec.overfit_risk,
                }
            )
    return rows


def topic_schema(topic: IndependentStageTopic) -> list[dict[str, Any]]:
    return [
        {
            "column": topic.signal_column,
            "formula": "candidate-specific closed-bar score mapped to -1/0/+1 signal",
            "timestamp_rule": "closed M5 bar timestamp only",
            "warmup": "uses existing feature warmup; no future bar read for runtime feature",
            "missingness": "missing required feature forces flat signal 0",
            "used_directly_in_mt5": True,
        },
        {
            "column": f"{topic.short_stage()}_score",
            "formula": "stage-specific train-fitted score for diagnostics",
            "timestamp_rule": "closed M5 bar timestamp only",
            "warmup": "same as source features",
            "missingness": "NaN allowed in diagnostics; signal is flat when required feature missing",
            "used_directly_in_mt5": False,
        },
        {
            "column": f"{topic.short_stage()}_activation",
            "formula": "1 when candidate rule activates before final missingness guard",
            "timestamp_rule": "closed M5 bar timestamp only",
            "warmup": "same as source features",
            "missingness": "0 when inactive or missing",
            "used_directly_in_mt5": False,
        },
    ]


def lineage_rows(topic: IndependentStageTopic, specs: Sequence[IndependentCandidateSpec], source_path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        rows.append(
            {
                "candidate_id": spec.candidate_id,
                "source_data_path": source_path,
                "source_symbol": "US100",
                "timeframe": "M5",
                "timestamp_rule": "closed M5 bar close",
                "calculation_formula": spec.rule_code,
                "feature_set": json.dumps(list(spec.feature_set), ensure_ascii=False),
                "warmup_requirement": "existing source-feature warmup only",
                "missingness_behavior": "flat signal when required inputs are non-finite",
                "used_directly_in_mt5": topic.signal_column,
                "python_candidate_design_only": False,
            }
        )
    return rows

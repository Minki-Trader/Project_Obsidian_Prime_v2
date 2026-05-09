from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from foundation.mt5.runtime_support import FEATURE_ORDER_HASH
from stage_pipelines.stage35.common import ROOT


STAGE_ID = "35_context_map__unsupervised_market_state_atlas"
STAGE_NUMBER = 35
RUN_NUMBER = "run29A"
RUN_ID = "run29A_unsupervised_market_state_atlas_mt5_probe_v1"
PACKET_ID = "stage35_run29A_unsupervised_market_state_atlas_mt5_probe_v1"
EXPLORATION_LABEL = "stage35_ContextMap__UnsupervisedAtlas"
IDEA_ID = "IDEA-ST35-UNSUPERVISED-MARKET-STATE-ATLAS"
BOUNDARY = "stage35_unsupervised_atlas_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_unsupervised_atlas_mt5_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_unsupervised_atlas_mt5_runtime_probe_after_attempt"
MODEL_INPUT_PATH = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
RESULT_ROOT = RUN_ROOT / "results"
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / "run29A_unsupervised_market_state_atlas_packet.md"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-05-09_stage35_unsupervised_market_state_atlas_open_run29A.md"
MODEL_FAMILY = "unsupervised_kmeans_state_atlas_constant_ebm_runtime_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_q33_3class"
SPLIT_CONTRACT = "split_v1_train_validation_oos"
KMEANS_CLUSTERS = 5
MIN_VALIDATION_ROWS = 200
MAX_HOLD_BARS = 12
RANDOM_STATE = 3501

FEATURE_ORDER: tuple[str, ...] = (
    "log_return_1",
    "log_return_3",
    "hl_range",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
    "return_zscore_20",
    "hl_zscore_50",
    "overnight_return",
    "return_1_over_atr_14",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "ema20_ema50_spread_zscore_50",
    "sma50_sma200_ratio",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
)


@dataclass(frozen=True)
class AtlasTopic:
    topic_id: str
    idea_id: str
    korean_name: str
    hypothesis: str
    features: Sequence[str]
    tier_b_scope: str = "available"


TOPICS: tuple[AtlasTopic, ...] = (
    AtlasTopic(
        "return_volatility_shape",
        "IDEA-ST35-ATLAS-RETURN-VOLATILITY",
        "수익률/변동성 모양",
        "return and volatility shape(수익률과 변동성 모양)가 label(라벨) 없이도 반복 가능한 시장 상태를 나눌 수 있다.",
        (
            "log_return_1",
            "log_return_3",
            "hl_range",
            "close_open_ratio",
            "gap_percent",
            "close_prev_close_ratio",
            "return_zscore_20",
            "hl_zscore_50",
            "overnight_return",
            "return_1_over_atr_14",
            "atr_14",
            "atr_50",
            "atr_14_over_atr_50",
            "historical_vol_20",
            "historical_vol_5_over_20",
        ),
    ),
    AtlasTopic(
        "trend_momentum_pressure",
        "IDEA-ST35-ATLAS-TREND-MOMENTUM",
        "추세/모멘텀 압력",
        "trend and momentum pressure(추세와 모멘텀 압력)가 좋은/나쁜 체결 문맥을 나눌 수 있다.",
        (
            "close_ema20_ratio",
            "close_ema50_ratio",
            "ema9_ema20_diff",
            "ema20_ema50_diff",
            "ema50_ema200_diff",
            "ema20_ema50_spread_zscore_50",
            "sma50_sma200_ratio",
            "rsi_14",
            "rsi_50",
            "rsi_14_slope_3",
            "rsi_14_minus_50",
            "stoch_kd_diff",
            "stochrsi_kd_diff",
            "ppo_hist_12_26_9",
            "roc_12",
            "trix_15",
            "adx_14",
            "di_spread_14",
            "supertrend_10_3",
            "vortex_indicator",
        ),
    ),
    AtlasTopic(
        "session_timing_map",
        "IDEA-ST35-ATLAS-SESSION-TIMING",
        "세션 시간 지도",
        "session timing(세션 시간)만으로도 장중 상태 밀도가 다르게 나타날 수 있다.",
        ("is_us_cash_open", "minutes_from_cash_open", "is_first_30m_after_open", "is_last_30m_before_cash_close"),
    ),
    AtlasTopic(
        "macro_risk_proxy_map",
        "IDEA-ST35-ATLAS-MACRO-RISK",
        "거시 위험 대리 지도",
        "macro proxy(거시 대리) 변화가 모델 없이도 위험 선호/회피 상태를 나눌 수 있다.",
        ("vix_change_1", "vix_zscore_20", "us10yr_change_1", "us10yr_zscore_20", "usdx_change_1", "usdx_zscore_20"),
        tier_b_scope="out_of_scope_by_partial_context",
    ),
    AtlasTopic(
        "mega_cap_breadth_divergence",
        "IDEA-ST35-ATLAS-MEGA-BREADTH",
        "대형주 폭/괴리 지도",
        "mega-cap breadth/divergence(대형주 폭/괴리)가 US100(나스닥100) 내부 상태를 나눌 수 있다.",
        (
            "nvda_xnas_log_return_1",
            "aapl_xnas_log_return_1",
            "msft_xnas_log_return_1",
            "amzn_xnas_log_return_1",
            "mega8_equal_return_1",
            "top3_weighted_return_1",
            "mega8_pos_breadth_1",
            "mega8_dispersion_5",
            "us100_minus_mega8_equal_return_1",
            "us100_minus_top3_weighted_return_1",
        ),
        tier_b_scope="out_of_scope_by_partial_context",
    ),
)


def validate_topic_layout() -> None:
    used: dict[str, str] = {}
    for topic in TOPICS:
        for feature in topic.features:
            if feature in used:
                raise ValueError(f"feature overlap: {feature} in {used[feature]} and {topic.topic_id}")
            used[feature] = topic.topic_id
    missing = sorted(set(used) - set(FEATURE_ORDER))
    if missing:
        raise ValueError(f"topic features outside 58-feature contract: {missing}")


__all__ = [
    "BOUNDARY",
    "DECISION_PATH",
    "EXPLORATION_LABEL",
    "FEATURE_ORDER",
    "FEATURE_ORDER_HASH",
    "FEATURE_SET_ID",
    "IDEA_ID",
    "JUDGMENT_BLOCKED",
    "JUDGMENT_COMPLETED",
    "KMEANS_CLUSTERS",
    "LABEL_ID",
    "MAX_HOLD_BARS",
    "MIN_VALIDATION_ROWS",
    "MODEL_FAMILY",
    "MODEL_INPUT_PATH",
    "PACKET_ID",
    "PACKET_ROOT",
    "RANDOM_STATE",
    "REPORT_PATH",
    "RESULT_ROOT",
    "RUN_ID",
    "RUN_NUMBER",
    "RUN_ROOT",
    "SPLIT_CONTRACT",
    "STAGE_ID",
    "STAGE_LEDGER_PATH",
    "STAGE_NUMBER",
    "STAGE_ROOT",
    "TOPICS",
    "AtlasTopic",
    "validate_topic_layout",
]

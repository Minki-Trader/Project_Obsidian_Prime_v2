from __future__ import annotations

from typing import Any, Mapping, Sequence

import pandas as pd


def _row_lookup(rows: Sequence[Mapping[str, Any]], tier_scope: str, split: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("tier_scope") == tier_scope and row.get("split") == split), {})


def _segment_lookup(rows: Sequence[Mapping[str, Any]], split: str, dimension: str, segment: str) -> Mapping[str, Any]:
    return next(
        (row for row in rows if row.get("split") == split and row.get("dimension") == dimension and row.get("segment") == segment),
        {},
    )


def build_read(
    tier_rows: Sequence[Mapping[str, Any]],
    segments: Sequence[Mapping[str, Any]],
    matched: pd.DataFrame,
) -> dict[str, Any]:
    a_val = _row_lookup(tier_rows, "Tier A", "validation")
    a_oos = _row_lookup(tier_rows, "Tier A", "oos")
    b_val = _row_lookup(tier_rows, "Tier B", "validation")
    b_oos = _row_lookup(tier_rows, "Tier B", "oos")
    tier_a = matched.loc[matched["matched_tier_scope"].eq("Tier A")].copy()
    return {
        "observed_change": {
            "validation": {
                "tier_a_profit_factor": a_val.get("profit_factor"),
                "tier_b_profit_factor": b_val.get("profit_factor"),
                "tier_a_net_profit": a_val.get("net_profit"),
                "tier_b_net_profit": b_val.get("net_profit"),
                "tier_a_trades": a_val.get("trade_count"),
                "tier_b_trades": b_val.get("trade_count"),
            },
            "oos": {
                "tier_a_profit_factor": a_oos.get("profit_factor"),
                "tier_b_profit_factor": b_oos.get("profit_factor"),
                "tier_a_net_profit": a_oos.get("net_profit"),
                "tier_b_net_profit": b_oos.get("net_profit"),
                "tier_a_trades": a_oos.get("trade_count"),
                "tier_b_trades": b_oos.get("trade_count"),
            },
        },
        "likely_drivers": [
            "Tier A(티어 A) executed trades(체결 거래)는 validation/OOS(검증/표본외) 모두 high-positive Markov state(고양수 마르코프 상태), confidence >= 0.97(신뢰 0.97 이상), entropy_inv >= 0.80(엔트로피 역수 0.80 이상)에 있었다.",
            "state/confidence/entropy(상태/신뢰/엔트로피)는 내부 차별자라기보다 entry gate(진입 게이트)처럼 작동했다.",
            "profit(수익)은 time segment(시간 구간)와 hold shape(보유 형태)에서 갈렸다.",
            "Tier B fallback(티어 B 대체)은 short exposure(숏 노출)와 partial context(부분 문맥)가 섞이며 Tier A(티어 A)보다 약했다.",
        ],
        "segment_checks": {
            "state_score_segments": sorted(tier_a["state_score_band"].dropna().unique().tolist()),
            "confidence_segments": sorted(tier_a["confidence_band"].dropna().unique().tolist()),
            "entropy_segments": sorted(tier_a["entropy_inv_band"].dropna().unique().tolist()),
            "validation_mid_net_profit": _segment_lookup(segments, "validation", "session_slice", "mid").get("net_profit"),
            "validation_late_net_profit": _segment_lookup(segments, "validation", "session_slice", "late").get("net_profit"),
            "oos_mid_net_profit": _segment_lookup(segments, "oos", "session_slice", "mid").get("net_profit"),
            "oos_late_net_profit": _segment_lookup(segments, "oos", "session_slice", "late").get("net_profit"),
            "validation_long_hold_net_profit": _segment_lookup(segments, "validation", "hold_bucket", "hold_gt_96").get("net_profit"),
            "oos_long_hold_net_profit": _segment_lookup(segments, "oos", "hold_bucket", "hold_gt_96").get("net_profit"),
        },
        "trade_shape": {
            "tier_a_total_trades": int(len(tier_a)),
            "tier_a_direction": "long_only(롱 전용)",
            "validation_avg_hold_bars": a_val.get("avg_hold_bars"),
            "oos_avg_hold_bars": a_oos.get("avg_hold_bars"),
            "validation_avg_mae": a_val.get("avg_mae"),
            "oos_avg_mae": a_oos.get("avg_mae"),
        },
        "alternative_explanations": [
            "trade count(거래 수)가 validation 77개, OOS 51개라 segment concentration(구간 집중)을 과장할 수 있다.",
            "trade open time(거래 개시 시각)에 feature row(피처 행)를 맞춘 구조 귀속이라 intra-trade path(거래 중 경로) 전체를 설명하지 않는다.",
            "run22B(22B 실행)는 sampled score-table handoff(표본 점수표 인계)이며 native statsmodels runtime authority(원본 스탯스모델 런타임 권위)가 아니다.",
        ],
        "attribution_confidence": "medium_for_gate_read_low_to_medium_for_segment_driver",
        "next_probe": "run28B_tier_a_markov_long_permission_segment_stress_probe_v1",
    }

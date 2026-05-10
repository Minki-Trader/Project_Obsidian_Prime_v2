from __future__ import annotations

from stage_pipelines.stage48.trade_level_cluster_telemetry import (
    SOURCE_CANDIDATE_ID,
    _top_cluster,
    build_cluster_summary_rows,
)


def test_cluster_summary_marks_top_abs_net_bucket() -> None:
    rows = [
        _row("validation_is", "2025-01", "2025-W01", "early", 10.0),
        _row("validation_is", "2025-01", "2025-W01", "early", -4.0),
        _row("validation_is", "2025-02", "2025-W05", "mid", 2.0),
    ]

    summary = build_cluster_summary_rows(rows)
    top_month = _top_cluster(summary, "validation_is", "month")

    assert top_month["source_candidate_id"] == SOURCE_CANDIDATE_ID
    assert top_month["bucket"] == "2025-01"
    assert top_month["is_top_abs_net_bucket"] is True
    assert top_month["trade_count"] == 2


def test_cluster_summary_keeps_split_boundaries() -> None:
    rows = [
        _row("validation_is", "2025-01", "2025-W01", "early", 5.0),
        _row("oos", "2025-10", "2025-W40", "late", -8.0),
    ]

    summary = build_cluster_summary_rows(rows)

    assert _top_cluster(summary, "validation_is", "month")["bucket"] == "2025-01"
    assert _top_cluster(summary, "oos", "month")["bucket"] == "2025-10"


def _row(split: str, month: str, iso_week: str, session: str, net: float) -> dict[str, object]:
    return {
        "attempt_name": f"routed_c08_{split}",
        "split": split,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "day": f"{month}-01",
        "iso_week": iso_week,
        "month": month,
        "quarter": "2025-Q1",
        "session_slice": session,
        "volatility_regime": "vol_mid",
        "trend_regime": "range_or_weak_trend",
        "adx_bucket": "adx_lt20",
        "spread_regime": "spread_mid",
        "direction": "buy",
        "net_profit": net,
        "hold_bars": 3.0,
    }

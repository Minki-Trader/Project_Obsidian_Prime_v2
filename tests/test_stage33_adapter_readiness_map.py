from __future__ import annotations

from stage_pipelines.stage33 import adapter_readiness_map as stage33


def test_repeatability_blocks_oos_only_positive() -> None:
    label, val_ok, oos_ok, inversion = stage33.repeatability_label(
        {"net_profit": -1.0, "profit_factor": 0.9, "trades": 100},
        {"net_profit": 10.0, "profit_factor": 1.2, "trades": 100},
    )

    assert label == "oos_only_positive_deferred"
    assert not val_ok
    assert oos_ok
    assert inversion


def test_mechanism_classification_combines_runtime_packaging_roles() -> None:
    classes = stage33.classify_mechanisms(
        "markov state score_table runtime_probe mt5 handoff",
        {"model_backend": "ebm_table", "score_table_parity": {"tier_a": {"passed": True}}},
    )
    roles = stage33.classify_roles("markov state score_table runtime_probe mt5 handoff")

    assert "score_table_adapter" in classes
    assert "regime_context_adapter" in classes
    assert "Runtime / Packaging" in roles
    assert "Regime / Context" in roles


def test_evidence_row_selects_adapter_candidate_when_gates_survive() -> None:
    summary = stage33.SummaryRef(
        path=stage33.ROOT / "docs/agent_control/packets/example/aggregate_summary.json",
        quality=30,
        payload={
            "stage_id": "28_regime_model__markov_switching_regression_state_link",
            "run_id": "run22B_markov_regression_state_runtime_probe_v1",
            "boundary": "runtime_probe_only",
            "external_verification_status": "completed",
            "mt5_kpi_record_count": 10,
            "model_family": "markov_regression_state_score_table_runtime_probe",
            "model_artifacts": {
                "model_backend": "ebm_table",
                "runtime_feature_order": ["state_score"],
                "score_table_parity": {"tier_a": {"passed": True}, "tier_b": {"passed": True}},
            },
            "prediction_artifacts": {
                "tier_a_predictions": {"path": "a.parquet"},
                "tier_b_predictions": {"path": "b.parquet"},
                "tier_ab_predictions": {"path": "ab.parquet"},
            },
            "validation_routed": {"net_profit": 100.0, "profit_factor": 1.5, "trade_count": 50},
            "oos_routed": {"net_profit": 50.0, "profit_factor": 1.2, "trade_count": 40},
        },
    )

    row = stage33.evidence_row(
        "run22B_markov_regression_state_runtime_probe_v1",
        "28_regime_model__markov_switching_regression_state_link",
        {"lane": "alpha_runtime_probe", "status": "reviewed", "judgment": "inconclusive"},
        summary,
        [
            {"tier_scope": "Tier A", "external_verification_status": "completed", "record_view": "mt5_a"},
            {"tier_scope": "Tier B", "external_verification_status": "completed", "record_view": "mt5_b"},
            {"tier_scope": "Tier A+B", "external_verification_status": "completed", "record_view": "mt5_total"},
        ],
    )

    assert row["evidence_decision"] == "adapter_candidate"
    assert row["repeatability_label"] == "validation_and_oos_positive_non_tiny"
    assert row["score_table_parity_status"] == "pass"

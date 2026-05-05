from __future__ import annotations

import unittest

import numpy as np

from foundation.adapters.contracts import AdapterInputContract, SignalCard
from foundation.adapters.onnx_signal_adapter import OnnxSignalAdapter, summarize_signal_cards
from foundation.adapters.score_table_signal_adapter import ScoreTableSignalAdapter
from foundation.control_plane.adapter_feasibility_matrix import build_adapter_feasibility_matrix
from foundation.control_plane.adapter_probe_shortlist import build_adapter_probe_shortlist
from foundation.control_plane.mechanism_role_map import build_mechanism_role_map, infer_mechanism_class, infer_roles
from foundation.control_plane.mt5_handoff_identity_audit import build_mt5_handoff_identity_audit
from foundation.control_plane.quantile_score_table_mt5_handoff_identity_audit import (
    build_quantile_score_table_mt5_handoff_identity_audit,
)
from foundation.control_plane.quantile_score_table_signalcard_probe import build_quantile_score_table_signalcard_probe
from foundation.control_plane.score_table_mt5_handoff_identity_audit import build_score_table_mt5_handoff_identity_audit
from foundation.control_plane.score_table_signalcard_probe import build_score_table_signalcard_probe
from foundation.control_plane.segmented_catboost_mt5_handoff_identity_audit import build_segmented_catboost_mt5_handoff_identity_audit
from foundation.control_plane.segmented_catboost_onnx_signalcard_probe import build_segmented_catboost_onnx_signalcard_probe
from foundation.control_plane.segmented_catboost_regime_mt5_handoff_identity_audit import (
    build_segmented_catboost_regime_mt5_handoff_identity_audit,
)
from foundation.control_plane.segmented_catboost_regime_onnx_signalcard_probe import (
    build_segmented_catboost_regime_onnx_signalcard_probe,
)


class AdapterContractTests(unittest.TestCase):
    def test_signal_card_requires_known_role_and_no_trade_fallback(self) -> None:
        card = SignalCard(
            adapter_id="candidate",
            roles=("Permission / Filter / Abstention",),
            direction="flat",
            score=0.7,
            confidence=0.6,
        )

        self.assertEqual(card.safe_fallback, "no_trade")
        self.assertEqual(card.to_dict()["roles"], ["Permission / Filter / Abstention"])

    def test_input_contract_hash_is_stable(self) -> None:
        contract = AdapterInputContract(feature_names=("a", "b"), state_names=("session",))

        self.assertEqual(contract.to_dict()["feature_order_hash"], "7e18f737311b2dc3b2f269dd78396b0351f14fb66efa879f768cb23181883c78")

    def test_onnx_signal_adapter_maps_probabilities_to_signal_cards(self) -> None:
        adapter = OnnxSignalAdapter(
            adapter_id="candidate",
            source_stage_id="stage",
            source_run_id="run",
            mechanism_class="model_probability_surface",
            roles=("Entry", "Runtime / Packaging"),
            feature_names=("a",),
            source_model_path=__file__,
            onnx_model_path=__file__,
            nonflat_threshold=0.6,
            tier_scope="Tier A",
        )

        cards = adapter.signal_cards(np.asarray([[0.7, 0.1, 0.2], [0.2, 0.5, 0.3], [0.45, 0.2, 0.35]]))

        self.assertEqual([card.direction for card in cards], ["short", "flat", "no_trade"])
        self.assertEqual(summarize_signal_cards(cards)["direction_counts"]["no_trade"], 1)

    def test_score_table_signal_adapter_maps_probabilities_to_signal_cards(self) -> None:
        adapter = ScoreTableSignalAdapter(
            adapter_id="candidate",
            source_stage_id="stage",
            source_run_id="run",
            mechanism_class="sequence_context_surface",
            roles=("Entry", "Runtime / Packaging"),
            feature_names=("a",),
            score_table_path=__file__,
            nonflat_threshold=0.6,
            tier_scope="Tier A",
        )

        cards = adapter.signal_cards(np.asarray([[0.7, 0.1, 0.2], [0.2, 0.5, 0.3], [0.45, 0.2, 0.35]]))

        self.assertEqual([card.direction for card in cards], ["short", "flat", "no_trade"])


class MechanismRoleMapTests(unittest.TestCase):
    def test_infer_roles_from_runtime_context_text(self) -> None:
        roles = infer_roles("supervised regime classifier filter onnx runtime handoff p_flat abstention")

        self.assertIn("Permission / Filter / Abstention", roles)
        self.assertIn("Regime / Context", roles)
        self.assertIn("Runtime / Packaging", roles)

    def test_infer_mechanism_class_prefers_onnx_runtime(self) -> None:
        self.assertEqual(infer_mechanism_class("elasticnet logistic onnx runtime parity"), "onnx_model_runtime")

    def test_infer_mechanism_class_keeps_sequence_context_ahead_of_generic_risk(self) -> None:
        self.assertEqual(infer_mechanism_class("stage32 tcn temporal sequence regular_risk_execution"), "sequence_context_surface")

    def test_current_repo_scan_finds_stage10_to_32_candidates(self) -> None:
        result = build_mechanism_role_map()

        self.assertGreater(result.summary["counts"]["candidate_count"], 20)
        self.assertIn("Runtime / Packaging", result.summary["counts"]["roles"])
        self.assertIn("model_probability_surface", result.summary["counts"]["mechanism_classes"])
        self.assertEqual(result.summary["claim_boundary"].split("_not_alpha_quality")[0], "evidence_scan_and_adapter_contract_only")


class AdapterProbeShortlistTests(unittest.TestCase):
    def test_current_repo_shortlist_applies_repeatability_gate(self) -> None:
        result = build_adapter_probe_shortlist()

        self.assertGreaterEqual(result.summary["counts"]["source_candidate_count"], result.summary["counts"]["shortlist_count"])
        self.assertEqual(result.summary["counts"]["onnx_export_ready"], 0)
        self.assertEqual(
            result.summary["onnx_decision"]["decision"],
            "defer_new_onnx_export_until_shortlisted_adapter_survives_signalcard_probe",
        )


class AdapterFeasibilityMatrixTests(unittest.TestCase):
    def test_current_repo_selects_score_table_candidate_after_first_onnx_probe(self) -> None:
        result = build_adapter_feasibility_matrix()

        self.assertEqual(result.summary["counts"]["shortlist_count"], 7)
        self.assertEqual(result.summary["counts"]["new_onnx_export_ready"], 0)
        self.assertEqual(
            result.summary["selected_next_probe"]["candidate_id"],
            "stage32_run26D_torch_tcn_native_temporal_runtime_probe_v1",
        )
        self.assertEqual(result.summary["selected_next_probe"]["adapter_probe_route"], "score_table_signalcard_adapter")


class ScoreTableSignalCardProbeTests(unittest.TestCase):
    def test_current_repo_score_table_probe_preserves_signal_direction(self) -> None:
        result = build_score_table_signalcard_probe()

        self.assertTrue(result.summary["parity_passed"])
        self.assertEqual(result.summary["parity_rows"], 20856)
        self.assertEqual(result.summary["signal_direction_mismatches"], 0)
        self.assertEqual(
            result.summary["onnx_readiness_decision"],
            "defer_onnx_export_score_table_runtime_advantage_not_established",
        )


class ScoreTableMt5HandoffIdentityAuditTests(unittest.TestCase):
    def test_current_repo_links_score_table_adapter_pack_to_stage32_mt5_probe(self) -> None:
        result = build_score_table_mt5_handoff_identity_audit()

        self.assertTrue(result.summary["passed"], result.summary["blocking_findings"])
        self.assertEqual(result.summary["counts"]["attempt_count"], 6)
        self.assertEqual(result.summary["counts"]["attempts_passed"], 6)
        self.assertEqual(
            result.summary["runtime_handoff_decision"],
            "existing_stage32_mt5_probe_identity_linked_to_run27f_score_table_adapter_pack",
        )


class QuantileScoreTableSignalCardProbeTests(unittest.TestCase):
    def test_quantile_tail_score_table_probe_records_exact_signalcard_gap(self) -> None:
        result = build_quantile_score_table_signalcard_probe()

        self.assertTrue(result.summary["parity_passed"])
        self.assertEqual(result.summary["parity_rows"], 20856)
        self.assertEqual(result.summary["signal_direction_mismatches"], 1)
        self.assertEqual(result.summary["trading_action_mismatches"], 0)
        self.assertEqual(result.summary["adapter_readiness_decision"], "defer_exact_signalcard_direction_gap")
        self.assertEqual(
            result.summary["selected_candidate"]["candidate_id"],
            "stage27_run21B_quantile_boosting_tail_risk_runtime_probe_v1",
        )


class QuantileScoreTableMt5HandoffIdentityAuditTests(unittest.TestCase):
    def test_quantile_tail_score_table_pack_links_to_existing_stage27_mt5_probe(self) -> None:
        result = build_quantile_score_table_mt5_handoff_identity_audit()

        self.assertTrue(result.summary["passed"], result.summary["blocking_findings"])
        self.assertEqual(result.summary["counts"]["attempt_count"], 6)
        self.assertEqual(result.summary["counts"]["attempts_passed"], 6)
        self.assertEqual(result.summary["source_mt5_external_verification_status"], "completed")


class SegmentedCatBoostOnnxSignalCardProbeTests(unittest.TestCase):
    def test_current_repo_segmented_catboost_onnx_probe_preserves_signal_direction(self) -> None:
        result = build_segmented_catboost_onnx_signalcard_probe()

        self.assertTrue(result.summary["parity_passed"])
        self.assertEqual(result.summary["segment_count"], 4)
        self.assertEqual(result.summary["tier_view_count"], 8)
        self.assertEqual(result.summary["signal_direction_mismatches"], 0)
        self.assertEqual(
            result.summary["onnx_readiness_decision"],
            "existing_segmented_catboost_onnx_packaged_manifest_only_no_new_export",
        )


class SegmentedCatBoostMt5HandoffIdentityAuditTests(unittest.TestCase):
    def test_current_repo_links_segmented_catboost_pack_to_stage18_mt5_probe(self) -> None:
        result = build_segmented_catboost_mt5_handoff_identity_audit()

        self.assertTrue(result.summary["passed"], result.summary["blocking_findings"])
        self.assertEqual(result.summary["counts"]["attempt_count"], 4)
        self.assertEqual(result.summary["counts"]["attempts_passed"], 4)
        self.assertEqual(
            result.summary["runtime_handoff_decision"],
            "existing_stage18_mt5_probe_identity_linked_to_run27h_segmented_catboost_onnx_signalcard_probe_v1_segmented_catboost_model_pack",
        )


class SegmentedCatBoostRegimeOnnxSignalCardProbeTests(unittest.TestCase):
    def test_current_repo_regime_segmented_catboost_onnx_probe_preserves_signal_direction(self) -> None:
        result = build_segmented_catboost_regime_onnx_signalcard_probe()

        self.assertTrue(result.summary["parity_passed"])
        self.assertEqual(result.summary["segment_count"], 4)
        self.assertEqual(result.summary["tier_view_count"], 8)
        self.assertEqual(result.summary["signal_direction_mismatches"], 0)
        self.assertEqual(
            result.summary["selected_candidate"]["candidate_id"],
            "stage18_run12D_catboost_regime_split_probe_v1",
        )


class SegmentedCatBoostRegimeMt5HandoffIdentityAuditTests(unittest.TestCase):
    def test_current_repo_links_regime_segmented_catboost_pack_to_stage18_mt5_probe(self) -> None:
        result = build_segmented_catboost_regime_mt5_handoff_identity_audit()

        self.assertTrue(result.summary["passed"], result.summary["blocking_findings"])
        self.assertEqual(result.summary["counts"]["attempt_count"], 4)
        self.assertEqual(result.summary["counts"]["attempts_passed"], 4)
        self.assertEqual(
            result.summary["runtime_handoff_decision"],
            "existing_stage18_mt5_probe_identity_linked_to_run27j_segmented_catboost_regime_onnx_signalcard_probe_v1_segmented_catboost_model_pack",
        )


class Mt5HandoffIdentityAuditTests(unittest.TestCase):
    def test_current_repo_links_run27c_pack_to_stage12_mt5_probe_identity(self) -> None:
        result = build_mt5_handoff_identity_audit()

        self.assertTrue(result.summary["passed"], result.summary["blocking_findings"])
        self.assertEqual(result.summary["counts"]["attempt_count"], 6)
        self.assertEqual(result.summary["counts"]["attempts_passed"], 6)
        self.assertEqual(
            result.summary["runtime_handoff_decision"],
            "existing_stage12_mt5_probe_identity_linked_to_run27c_model_pack",
        )


if __name__ == "__main__":
    unittest.main()

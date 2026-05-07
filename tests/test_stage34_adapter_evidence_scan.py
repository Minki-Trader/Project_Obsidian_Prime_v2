from __future__ import annotations

import unittest

from stage_pipelines.stage34 import adapter_evidence_scan as scan


class Stage34AdapterEvidenceScanTests(unittest.TestCase):
    def test_stage_scope_is_limited_to_stage10_32(self) -> None:
        self.assertTrue(scan.in_scope_stage("23_regime_model__supervised_regime_classifier_filter"))
        self.assertTrue(scan.in_scope_stage("32_sequence_model__tcn_temporal_convolution_context"))
        self.assertFalse(scan.in_scope_stage("09_pre_alpha_handoff__registry_publish_packet"))
        self.assertFalse(scan.in_scope_stage("34_mechanism_discovery__stage10_32_adapter_evidence_scan"))

    def test_roles_are_derived_from_evidence_text(self) -> None:
        roles = scan.derive_roles("supervised regime classifier filter onnx runtime handoff")
        self.assertIn("Permission / Filter / Abstention", roles)
        self.assertIn("Regime / Context", roles)
        self.assertIn("Runtime / Packaging", roles)

    def test_candidate_classification_blocks_validation_oos_inversion(self) -> None:
        row = {
            "stage_number": 23,
            "external_verification_status": "completed",
            "validation_net_profit": -1.0,
            "validation_profit_factor": 0.9,
            "validation_trades": 100,
            "oos_net_profit": 10.0,
            "oos_profit_factor": 1.1,
            "oos_trades": 100,
            "quarter_positive_rate": 0.8,
        }
        status, reason = scan.classify_candidate(row, "")
        self.assertEqual(status, "negative_memory")
        self.assertIn("inversion", reason)

    def test_signal_contract_has_safe_fallback(self) -> None:
        contract = scan.signal_contract(
            {
                "run_id": "run17B_supervised_regime_classifier_runtime_probe_v1",
                "stage_id": "23_regime_model__supervised_regime_classifier_filter",
                "roles": "Permission / Filter / Abstention|Runtime / Packaging",
                "mechanism_class": "onnx_runtime_adapter",
            }
        )
        self.assertEqual(contract["output_contract"]["safe_fallback"]["permission"], "abstain")
        self.assertEqual(contract["output_contract"]["type"], "SignalCard")


if __name__ == "__main__":
    unittest.main()

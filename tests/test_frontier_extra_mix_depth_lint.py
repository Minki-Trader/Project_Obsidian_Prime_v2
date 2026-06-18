from __future__ import annotations

import unittest
from pathlib import Path

from foundation.control_plane.frontier_extra_mix_depth_lint import audit_frontier_extra_mix_depth_receipt


ROOT = Path(__file__).resolve().parents[1]


class FrontierExtraMixDepthLintTests(unittest.TestCase):
    def test_progressive_mix_depth_receipt_passes(self) -> None:
        result = audit_frontier_extra_mix_depth_receipt(_receipt(), root=ROOT)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_full_mix_materialization_and_pf_share_block(self) -> None:
        receipt = _receipt()
        receipt["depth_receipts"][0]["full_mix_materialized"] = True
        receipt["depth_receipts"][0]["top_forward_pf_share"] = 0.5

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        check_ids = {finding.check_id for finding in result.findings}
        self.assertIn("frontier_extra_mix_depth::depth::full_mix_materialized_forbidden", check_ids)
        self.assertIn("frontier_extra_mix_depth::depth::top_forward_pf_share_exceeded", check_ids)

    def test_missing_single_substrate_warning_blocks(self) -> None:
        receipt = _receipt()
        receipt["depth_receipts"][0]["runtime_substrate_count"] = 1
        receipt["depth_receipts"][0]["single_substrate_warning"] = ""

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "frontier_extra_mix_depth::depth::missing_single_substrate_warning",
            {finding.check_id for finding in result.findings},
        )

    def test_compile_only_attempt_blocks(self) -> None:
        receipt = _receipt()
        receipt["attempt_receipts"][0]["tester_status"] = ""
        receipt["attempt_receipts"][0]["runtime_status"] = ""
        receipt["attempt_receipts"][0]["report_status"] = ""

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "frontier_extra_mix_depth::attempt::compile_only_not_runtime_evidence",
            {finding.check_id for finding in result.findings},
        )

    def test_missing_ingredient_card_receipts_blocks(self) -> None:
        receipt = _receipt()
        receipt["ingredient_card_receipts"] = []

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "frontier_extra_mix_depth::ingredient_card::missing_rows",
            {finding.check_id for finding in result.findings},
        )

    def test_mix_queue_must_link_known_card_count_for_depth(self) -> None:
        receipt = _receipt()
        receipt["mix_queue_receipts"][0]["source_card_ids"] = ["card01", "missing_card", "card01"]

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        check_ids = {finding.check_id for finding in result.findings}
        self.assertIn("frontier_extra_mix_depth::mix_queue::source_card_count_mismatch", check_ids)
        self.assertIn("frontier_extra_mix_depth::mix_queue::duplicate_source_cards", check_ids)
        self.assertIn("frontier_extra_mix_depth::mix_queue::unknown_source_cards", check_ids)

    def test_pf_only_mix_selection_blocks(self) -> None:
        receipt = _receipt()
        receipt["mix_queue_receipts"][0]["selection_lanes"] = ["PF(수익 팩터)"]
        receipt["depth_receipts"][0]["selection_lane_counts"] = {
            "PF(수익 팩터)": 1,
            "DD resilience(손실폭 회복력)": 0,
            "density/materiality(밀도/물질성)": 0,
            "runtime materialization(런타임 물질화)": 0,
            "negative-memory repair(부정 기억 수리)": 0,
        }

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        check_ids = {finding.check_id for finding in result.findings}
        self.assertIn("frontier_extra_mix_depth::mix_queue::pf_only_selection_forbidden", check_ids)
        self.assertIn("frontier_extra_mix_depth::depth::pf_only_selection_forbidden", check_ids)

    def test_proxy_only_attempt_cannot_support_runtime_claim(self) -> None:
        receipt = _receipt()
        receipt["attempt_receipts"][0]["tester_status"] = "proxy_only"
        receipt["attempt_receipts"][0]["runtime_status"] = "proxy_only"
        receipt["attempt_receipts"][0]["report_status"] = "proxy_only"

        result = audit_frontier_extra_mix_depth_receipt(receipt, root=ROOT)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "frontier_extra_mix_depth::attempt::proxy_only_not_runtime_evidence",
            {finding.check_id for finding in result.findings},
        )


def _receipt() -> dict[str, object]:
    return {
        "ingredient_card_receipts": [
            {
                "ingredient_card_id": "card01",
                "source_frontier_id": "stage_frontier_001",
                "source_run_id": "frontier001_closeout",
                "hypothesis": "first source hypothesis",
                "axis_tags": ["feature_set", "label"],
                "artifact_path_hash": "hash01",
                "salvage_value": "density clue",
                "negative_memory": "runtime gap",
                "do_not_repeat": "threshold-only repair",
                "tier_scope": "Tier A separate",
                "claim_boundary": "reference only",
                "selection_eligibility": "eligible_for_mix",
                "selection_lane_candidates": ["density/materiality(밀도/물질성)", "negative-memory repair(부정 기억 수리)"],
            },
            {
                "ingredient_card_id": "card02",
                "source_frontier_id": "stage_frontier_002",
                "source_run_id": "frontier002_closeout",
                "hypothesis": "second source hypothesis",
                "axis_tags": ["trade_shape", "risk_logic"],
                "artifact_path_hash": "hash02",
                "salvage_value": "risk clue",
                "negative_memory": "drawdown collapse",
                "do_not_repeat": "same surface repair",
                "tier_scope": "Tier A+B combined",
                "claim_boundary": "reference only",
                "selection_eligibility": "eligible_for_mix",
                "selection_lane_candidates": ["DD resilience(손실폭 회복력)", "runtime materialization(런타임 물질화)"],
            },
        ],
        "mix_queue_receipts": [
            {
                "mix_id": "mix01",
                "depth_id": "2mix(2개 혼합)",
                "source_card_ids": ["card01", "card02"],
                "axis_tags": ["feature_set", "label", "trade_shape", "risk_logic"],
                "selection_lanes": [
                    "DD resilience(손실폭 회복력)",
                    "density/materiality(밀도/물질성)",
                    "runtime materialization(런타임 물질화)",
                ],
                "novelty_delta": "label plus risk logic",
                "near_duplicate_cluster_id": "cluster01",
                "sample_method": "lane_stratified",
                "selected_for_runtime": True,
                "selection_reason": "cross-axis complementarity",
                "risk_notes": "runtime gap risk retained",
                "claim_boundary": "runtime learning only",
            }
        ],
        "depth_receipts": [
            {
                "depth_id": "2mix(2개 혼합)",
                "candidate_possible_count": 1225,
                "candidate_queued_count": 60,
                "candidate_cap": 60,
                "sample_method": "lane_stratified",
                "selected_for_runtime_count": 1,
                "materialized_count": 1,
                "runtime_completed_count": 1,
                "selection_lane_counts": {
                    "PF(수익 팩터)": 1,
                    "DD resilience(손실폭 회복력)": 1,
                    "density/materiality(밀도/물질성)": 1,
                    "runtime materialization(런타임 물질화)": 1,
                    "negative-memory repair(부정 기억 수리)": 1,
                },
                "top_forward_pf_share": 0.2,
                "runtime_substrate_count": 1,
                "single_substrate_warning": "broad materialization claim forbidden",
                "full_mix_materialized": False,
                "depth_decision": "continue_if_gates_pass",
                "claim_effect": "runtime learning only",
                "claim_boundary": "no runtime authority",
            }
        ],
        "attempt_receipts": [
            {
                "attempt_id": "attempt01",
                "depth_id": "2mix(2개 혼합)",
                "mix_id": "mix01",
                "parent_mix_id": "NA",
                "candidate_id": "candidate01",
                "dataset_id": "dataset01",
                "feature_set_id": "features01",
                "label_id": "label01",
                "split": "validation",
                "split_id": "split01",
                "split_contract": "train_validation_oos_locked",
                "source_identities": ["source01"],
                "parser_contract_version": "parser_v1",
                "runtime_contract_version": "runtime_v1",
                "runtime_substrate_id": "substrate01",
                "compile_status": "pass",
                "tester_status": "completed",
                "runtime_status": "completed",
                "report_status": "completed",
                "onnx_path_hash": "hash",
                "onnx_hash": "hash",
                "ea_source_binary_hash": "hash",
                "ea_source_hash": "hash",
                "ea_binary_hash": "hash",
                "set_ini_hash": "hash",
                "feature_order_hash": "hash",
                "tester_identity": "tester01",
                "telemetry_path": "telemetry.json",
                "telemetry_hash": "hash",
                "summary_path": "summary.json",
                "report_path_hash": "hash",
                "report_hash": "hash",
                "snapshot_path": "snapshot.png",
                "execution_log_path": "terminal.log",
                "trade_list_hash": "hash",
                "trade_count": 42,
                "profit_factor": 1.2,
                "drawdown": 8.0,
                "gap_cause": "none",
                "claim_effect": "runtime learning only",
                "claim_boundary": "no runtime authority",
            }
        ],
    }


if __name__ == "__main__":
    unittest.main()

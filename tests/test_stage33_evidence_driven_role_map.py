from __future__ import annotations

from pathlib import Path

from foundation.alpha.adapter_contract import SignalCard, default_safe_signal, validate_signal_card
from stage_pipelines.stage33.evidence_driven_role_map import run
from stage_pipelines.stage33.evidence_sources import EvidenceRow
from stage_pipelines.stage33.role_classifier import build_role_map


def test_signal_card_contract_validates_role_and_score() -> None:
    card = SignalCard(role="Entry", action="emit_signal", direction="long", score=0.5, confidence=0.7)
    assert validate_signal_card(card) == []
    invalid = SignalCard(role="Mystery", action="emit_signal", score=1.5)
    assert "unknown_role:Mystery" in validate_signal_card(invalid)
    assert "score_outside_0_1" in validate_signal_card(invalid)


def test_default_safe_signal_abstains_for_unknown_role() -> None:
    card = default_safe_signal("unknown", reason="test_reason")
    assert card.role == "Deferred"
    assert card.action == "abstain"
    assert card.reason_codes == ("test_reason",)


def test_role_map_derives_candidates_without_fixed_mechanism() -> None:
    rows = [
        EvidenceRow("unit", "a", 21, "run15B", "1", "reviewed", "runtime_probe", "ONNX runtime parity logistic probability handoff"),
        EvidenceRow("unit", "b", 23, "run17B", "2", "reviewed", "runtime_probe", "regime classifier permission filter abstention MT5"),
        EvidenceRow("unit", "c", 27, "run21B", "3", "reviewed", "runtime_probe", "quantile tail risk drawdown runtime"),
    ]
    role_map = build_role_map(rows)
    roles = {item["role"] for item in role_map["adapter_candidates"]}
    assert "Runtime / Packaging" in roles
    assert "Permission / Filter / Abstention" in roles
    assert "Risk / Tail-risk" in roles


def test_stage33_no_write_scans_current_repo() -> None:
    summary = run(Path("."), write=False)
    assert summary["stage_id"].startswith("33_")
    assert summary["inventory"]["row_count"] > 0
    assert summary["candidate_count"] > 0
    assert summary["onnx_artifacts_generated"] is False

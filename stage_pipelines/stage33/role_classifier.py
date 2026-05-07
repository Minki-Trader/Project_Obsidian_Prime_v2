from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Iterable, Mapping

from foundation.alpha.adapter_contract import ADAPTER_ROLES, make_contract, role_slug
from stage_pipelines.stage33.evidence_sources import EvidenceRow


ROLE_TOKENS: dict[str, tuple[str, ...]] = {
    "Entry": ("entry", "signal", "threshold", "long", "short", "direction", "probability"),
    "Permission / Filter / Abstention": ("permission", "filter", "abstain", "block", "allow", "gate", "fallback"),
    "Risk / Tail-risk": ("risk", "tail", "drawdown", "hazard", "quantile", "loss", "recovery"),
    "Sizing": ("sizing", "size", "lot", "exposure", "risk_budget"),
    "Position Management": ("position", "routing", "route", "fill", "skip", "reject", "hold_bars"),
    "Exit / Hold": ("exit", "hold", "survival", "time_to_event", "close", "lifecycle"),
    "Regime / Context": ("regime", "context", "state", "hmm", "markov", "session", "volatility"),
    "Runtime / Packaging": ("runtime", "mt5", "onnx", "score-table", "score_table", "handoff", "package", "parity"),
    "Negative Memory": ("negative", "failed", "why_failed", "do-not-repeat", "reopen_condition"),
    "Deferred": ("blocked", "invalid", "inconclusive", "out_of_scope", "deferred"),
}

MECHANISM_TOKENS: dict[str, tuple[str, ...]] = {
    "model_score_surface": ("model", "classifier", "probability", "score", "logistic", "boost", "tcn", "tabnet"),
    "rule_or_threshold_surface": ("threshold", "gate", "rule", "cutoff", "q0.", "adx", "rank"),
    "runtime_score_table_handoff": ("score-table", "score_table", "mt5", "handoff", "tester"),
    "onnx_packaging": ("onnx", "parity", "export"),
    "regime_context_state": ("regime", "context", "hmm", "markov", "state", "session"),
    "exit_hold_lifecycle": ("survival", "hazard", "hold", "exit", "lifecycle"),
    "tail_risk_surface": ("tail", "risk", "quantile", "drawdown", "loss"),
    "calibration_abstention": ("calibration", "isotonic", "abstention", "abstain"),
    "adaptive_online_learning": ("river", "online", "drift", "adaptive"),
    "negative_memory": ("negative", "why_failed", "failed", "reopen_condition"),
}

SPLIT_TOKENS = ("validation", "oos", "wfo", "rolling")


def build_role_map(rows: Iterable[EvidenceRow]) -> dict[str, Any]:
    evidence = list(rows)
    role_rows: dict[str, list[EvidenceRow]] = {role: [] for role in ADAPTER_ROLES}
    class_rows: dict[str, list[EvidenceRow]] = defaultdict(list)
    for row in evidence:
        roles = classify_roles(row.text)
        classes = classify_mechanism_classes(row.text)
        for role in roles:
            role_rows[role].append(row)
        for mechanism_class in classes:
            class_rows[mechanism_class].append(row)

    roles_payload = {
        role: _role_payload(role, rows_for_role, class_rows)
        for role, rows_for_role in role_rows.items()
        if rows_for_role
    }
    mechanism_payload = {
        mechanism_class: {
            "evidence_count": len(rows_for_class),
            "stage_count": _unique_stage_count(rows_for_class),
            "example_paths": _example_paths(rows_for_class),
        }
        for mechanism_class, rows_for_class in sorted(class_rows.items())
    }
    candidates = [_candidate_from_role(role, payload) for role, payload in roles_payload.items()]
    candidates = sorted(candidates, key=lambda item: (-item["evidence_count"], item["candidate_id"]))
    return {
        "roles": roles_payload,
        "mechanism_classes": mechanism_payload,
        "adapter_candidates": candidates,
        "candidate_count": len(candidates),
    }


def classify_roles(text: str) -> list[str]:
    lowered = text.lower()
    roles = [role for role, tokens in ROLE_TOKENS.items() if _contains_any(lowered, tokens)]
    if not roles:
        roles = ["Deferred"]
    return roles


def classify_mechanism_classes(text: str) -> list[str]:
    lowered = text.lower()
    classes = [name for name, tokens in MECHANISM_TOKENS.items() if _contains_any(lowered, tokens)]
    return classes or ["unclassified_evidence"]


def build_gate_payloads(role_map: Mapping[str, Any], inventory: Mapping[str, Any]) -> dict[str, Any]:
    candidates = list(role_map.get("adapter_candidates", []))
    evidence_gate = {
        "status": "pass" if inventory.get("row_count", 0) > 0 and candidates else "blocked",
        "why_needed": "Derive mechanism classes from Stage10-32 evidence before choosing implementation.",
        "evidence_gap": "No fixed adapter taxonomy or ONNX target is assumed.",
        "input_data": {
            "stage_range": [inventory.get("stage_min"), inventory.get("stage_max")],
            "row_count": inventory.get("row_count"),
            "source_counts": inventory.get("source_counts"),
            "unique_runs": inventory.get("unique_runs"),
        },
        "output": "mechanism_role_map.json and adapter_candidates.json",
        "claim_boundary": "evidence map only; no alpha quality, promotion, baseline, runtime authority, or live readiness.",
    }
    repeatability = {
        "status": "pass" if inventory.get("source_files") else "blocked",
        "command": "python -m foundation.pipelines.run_stage33_evidence_driven_role_map --no-write",
        "repeatability_check": "Deterministic source scan from tracked ledgers, stage docs, and packet docs.",
        "source_files": inventory.get("source_files", []),
    }
    runtime_parity = {
        "status": "not_applicable_by_claim",
        "research_path": "stage_pipelines/stage33/evidence_driven_role_map.py",
        "runtime_path": "not_created",
        "shared_contract": "SignalCard output contract drafted; no runtime adapter behavior fixed.",
        "parity_check": "not_applicable_no_runtime_artifact",
        "runtime_claim_boundary": "research_only",
    }
    return {
        "evidence_gate": evidence_gate,
        "repeatability_check": repeatability,
        "runtime_parity_check": runtime_parity,
        "adapter_readiness": _adapter_readiness(candidates),
        "onnx_readiness": _onnx_readiness(candidates),
        "claim_boundary": _claim_boundary(),
    }


def _role_payload(role: str, rows_for_role: list[EvidenceRow], class_rows: Mapping[str, list[EvidenceRow]]) -> dict[str, Any]:
    class_counts = Counter()
    for row in rows_for_role:
        for mechanism_class in classify_mechanism_classes(row.text):
            class_counts[mechanism_class] += 1
    return {
        "role": role,
        "evidence_count": len(rows_for_role),
        "stage_count": _unique_stage_count(rows_for_role),
        "unique_runs": len({row.run_id for row in rows_for_role if row.run_id}),
        "runtime_evidence_count": sum(1 for row in rows_for_role if _contains_any(row.text.lower(), ("runtime", "mt5", "onnx"))),
        "split_evidence_count": sum(1 for row in rows_for_role if _contains_any(row.text.lower(), SPLIT_TOKENS)),
        "mechanism_class_counts": dict(class_counts.most_common()),
        "example_paths": _example_paths(rows_for_role),
        "example_judgments": sorted({row.judgment for row in rows_for_role if row.judgment})[:8],
    }


def _candidate_from_role(role: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    classes = list(payload.get("mechanism_class_counts", {}).keys())
    top_class = classes[0] if classes else "unclassified_evidence"
    readiness = {
        "role_clear": True,
        "input_state_defined": False,
        "output_contract_defined": True,
        "comparison_kpi_available": payload.get("evidence_count", 0) > 0,
        "not_single_split_only": payload.get("stage_count", 0) >= 3,
        "safe_fallback_defined": True,
        "reusable_next_experiment": True,
        "status": "contract_candidate_not_runtime_ready",
    }
    contract = make_contract(
        adapter_id=f"stage33_{role_slug(role)}_adapter_contract_candidate",
        role=role,
        mechanism_class=top_class,
        input_contract={
            "status": "not_fixed_for_runtime",
            "source": "Stage10-32 evidence-derived role map",
            "required_next_step": "Choose one role and freeze feature/state inputs before runtime implementation.",
        },
        comparison_kpi=("evidence_count", "stage_count", "runtime_evidence_count", "split_evidence_count"),
        readiness_status=readiness["status"],
        claim_boundary="adapter contract candidate only; not a deployed adapter.",
    )
    return {
        "candidate_id": contract.adapter_id,
        "role": role,
        "mechanism_class": top_class,
        "supporting_mechanism_classes": classes,
        "evidence_count": payload.get("evidence_count", 0),
        "stage_count": payload.get("stage_count", 0),
        "runtime_evidence_count": payload.get("runtime_evidence_count", 0),
        "split_evidence_count": payload.get("split_evidence_count", 0),
        "readiness": readiness,
        "contract": contract.__dict__,
        "next_action": "run bounded adapter probe only after fixed input contract and comparison KPI are selected",
    }


def _adapter_readiness(candidates: list[Mapping[str, Any]]) -> dict[str, Any]:
    ready = [item for item in candidates if item.get("readiness", {}).get("status") == "ready"]
    return {
        "status": "no_runtime_ready_adapter",
        "candidate_count": len(candidates),
        "runtime_ready_count": len(ready),
        "gate": "partial_contract_candidates_only",
        "stop_rule": "Do not implement runtime adapter until one candidate has fixed input state and comparison KPI.",
    }


def _onnx_readiness(candidates: list[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "status": "not_ready_for_new_onnx_artifact",
        "candidate_count": len(candidates),
        "reasons": [
            "No candidate has a fixed runtime input feature contract.",
            "No new source model or adapter behavior is stable enough for packaging.",
            "No Python-vs-ONNX parity target exists for this packet.",
            "No runtime advantage over MQL rule, score-table, or Python bridge has been established.",
        ],
        "next_required_evidence": "bounded adapter probe with fixed inputs, source outputs, parity plan, and MT5 handoff plan",
    }


def _claim_boundary() -> dict[str, Any]:
    return {
        "status": "bounded_claims_only",
        "allowed_claims": ["Stage10-32 evidence was scanned", "adapter contract candidates were identified"],
        "forbidden_claims": [
            "alpha_quality",
            "operating_baseline",
            "promotion_candidate",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
        ],
    }


def _contains_any(text: str, tokens: Iterable[str]) -> bool:
    return any(token in text for token in tokens)


def _unique_stage_count(rows: Iterable[EvidenceRow]) -> int:
    return len({row.stage_number for row in rows if row.stage_number})


def _example_paths(rows: Iterable[EvidenceRow]) -> list[str]:
    seen: list[str] = []
    for row in rows:
        if row.source_path not in seen:
            seen.append(row.source_path)
        if len(seen) >= 8:
            break
    return seen


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")

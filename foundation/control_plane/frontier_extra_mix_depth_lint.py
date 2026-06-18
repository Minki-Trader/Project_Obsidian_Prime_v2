from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


DEFAULT_REGISTRY = Path("docs/agent_control/work_family_registry.yaml")


def audit_frontier_extra_mix_depth_receipt(
    receipt: Mapping[str, Any],
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    root: Path = Path("."),
) -> AuditResult:
    contract = _progressive_contract(root / registry_path)
    findings: list[AuditFinding] = []
    ingredient_rows = _mapping_list(receipt.get("ingredient_card_receipts") or receipt.get("ingredient_cards"))
    mix_rows = _mapping_list(receipt.get("mix_queue_receipts") or receipt.get("mix_receipts") or receipt.get("mixes"))
    depth_rows = _mapping_list(receipt.get("depth_receipts") or receipt.get("depths"))
    attempt_rows = _mapping_list(receipt.get("attempt_receipts") or receipt.get("attempts"))

    ingredient_required = tuple(str(field) for field in contract.get("required_ingredient_card_fields", ()) if field)
    mix_required = tuple(str(field) for field in contract.get("required_mix_queue_receipt_fields", ()) if field)
    depth_required = tuple(str(field) for field in contract.get("required_depth_receipt_fields", ()) if field)
    attempt_required = tuple(str(field) for field in contract.get("required_attempt_receipt_fields", ()) if field)
    depth_caps = _depth_caps(contract)
    selection_lanes = tuple(str(lane) for lane in contract.get("selection_lanes", ()) if lane)

    _check_required_rows(ingredient_rows, ingredient_required, "ingredient_card", findings)
    _check_required_rows(mix_rows, mix_required, "mix_queue", findings)
    _check_required_rows(depth_rows, depth_required, "depth", findings)
    _check_required_rows(attempt_rows, attempt_required, "attempt", findings)
    _check_ingredient_mix_links(ingredient_rows, mix_rows, depth_caps, findings)
    _check_depth_caps(depth_rows, depth_caps, selection_lanes, findings)
    _check_mix_caps(mix_rows, depth_caps, findings)
    _check_attempt_caps(attempt_rows, depth_caps, findings)
    _check_total_attempt_cap(attempt_rows, contract, findings)
    _check_attempt_mix_links(attempt_rows, mix_rows, findings)
    _check_attempt_runtime_evidence(attempt_rows, findings)
    _check_forbidden_claims(ingredient_rows, "ingredient_card", findings)
    _check_forbidden_claims(mix_rows, "mix_queue", findings)
    _check_forbidden_claims(depth_rows, "depth", findings)
    _check_forbidden_claims(attempt_rows, "attempt", findings)

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="frontier_extra_mix_depth_lint",
        status=status,
        findings=tuple(findings),
        counts={
            "ingredient_card_count": len(ingredient_rows),
            "mix_queue_count": len(mix_rows),
            "depth_receipt_count": len(depth_rows),
            "attempt_receipt_count": len(attempt_rows),
            "depth_ids": sorted(depth_caps),
        },
        allowed_claims=("frontier_extra_mix_depth_receipt_valid",) if status == "pass" else ("blocked",),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def audit_frontier_extra_mix_depth_receipt_path(
    path: Path,
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    root: Path = Path("."),
) -> AuditResult:
    return audit_frontier_extra_mix_depth_receipt(
        _load_mapping(path),
        registry_path=registry_path,
        root=root,
    )


def _check_required_rows(
    rows: Sequence[Mapping[str, Any]],
    required_fields: Sequence[str],
    row_type: str,
    findings: list[AuditFinding],
) -> None:
    if not rows:
        findings.append(
            AuditFinding(
                check_id=f"frontier_extra_mix_depth::{row_type}::missing_rows",
                message=f"Frontier Extra {row_type} receipts are required.",
            )
        )
        return
    for index, row in enumerate(rows):
        missing = [field for field in required_fields if _is_missing(row.get(field))]
        if missing:
            findings.append(
                AuditFinding(
                    check_id=f"frontier_extra_mix_depth::{row_type}::missing_fields",
                    message=f"Frontier Extra {row_type} receipt is missing required fields.",
                    details={"index": index, "missing": missing},
                )
            )


def _check_ingredient_mix_links(
    ingredient_rows: Sequence[Mapping[str, Any]],
    mix_rows: Sequence[Mapping[str, Any]],
    depth_caps: Mapping[str, Mapping[str, int]],
    findings: list[AuditFinding],
) -> None:
    card_ids = {str(row.get("ingredient_card_id", "")).strip() for row in ingredient_rows if row.get("ingredient_card_id")}
    for index, row in enumerate(mix_rows):
        depth_id = str(row.get("depth_id", "")).strip()
        expected_arity = _depth_arity(depth_id)
        source_card_ids = _string_list(row.get("source_card_ids"))
        if expected_arity and len(source_card_ids) != expected_arity:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::mix_queue::source_card_count_mismatch",
                    message="Mix queue row must cite exactly the number of ingredient cards implied by its depth.",
                    details={"index": index, "mix_id": row.get("mix_id"), "depth_id": depth_id, "source_card_ids": source_card_ids},
                )
            )
        if len(set(source_card_ids)) != len(source_card_ids):
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::mix_queue::duplicate_source_cards",
                    message="Mix queue row repeats the same ingredient card inside one mix.",
                    details={"index": index, "mix_id": row.get("mix_id"), "source_card_ids": source_card_ids},
                )
            )
        unknown = [card_id for card_id in source_card_ids if card_id not in card_ids]
        if unknown:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::mix_queue::unknown_source_cards",
                    message="Mix queue row references ingredient cards that are not present in the receipt.",
                    details={"index": index, "mix_id": row.get("mix_id"), "unknown_source_card_ids": unknown},
                )
            )
        if depth_id and depth_id not in depth_caps:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::mix_queue::unknown_depth_id",
                    message="Mix queue row uses a depth_id outside the registered progressive sequence.",
                    details={"index": index, "mix_id": row.get("mix_id"), "depth_id": depth_id, "allowed": sorted(depth_caps)},
                )
            )


def _check_depth_caps(
    depth_rows: Sequence[Mapping[str, Any]],
    depth_caps: Mapping[str, Mapping[str, int]],
    selection_lanes: Sequence[str],
    findings: list[AuditFinding],
) -> None:
    for index, row in enumerate(depth_rows):
        depth_id = str(row.get("depth_id", "")).strip()
        caps = depth_caps.get(depth_id, {})
        if not caps:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::depth::unknown_depth_id",
                    message="Depth receipt uses a depth_id outside the registered progressive sequence.",
                    details={"index": index, "depth_id": depth_id, "allowed": sorted(depth_caps)},
                )
            )
            continue
        _check_int_cap(row, "candidate_queued_count", caps["queue_cap"], index, "queue_cap", findings)
        _check_int_cap(row, "materialized_count", caps["materialized_mix_cap"], index, "materialized_mix_cap", findings)
        _check_int_cap(row, "selected_for_runtime_count", caps["mt5_attempt_cap"], index, "mt5_attempt_cap", findings)
        if _truthy(row.get("full_mix_materialized")):
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::depth::full_mix_materialized_forbidden",
                    message="Progressive Extra Stage receipts must not claim full mix materialization.",
                    details={"index": index, "depth_id": depth_id},
                )
            )
        top_pf_share = _float_or_none(row.get("top_forward_pf_share"))
        if top_pf_share is not None and top_pf_share > 0.25:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::depth::top_forward_pf_share_exceeded",
                    message="top_forward_pf selection share exceeds the registered 25% cap.",
                    details={"index": index, "depth_id": depth_id, "top_forward_pf_share": top_pf_share},
                )
            )
        _check_selection_lane_counts(row, selection_lanes, index, findings)
        substrate_count = _int_or_none(row.get("runtime_substrate_count"))
        if substrate_count is not None and substrate_count <= 1 and _is_missing(row.get("single_substrate_warning")):
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::depth::missing_single_substrate_warning",
                    message="Single-substrate Extra Stage learning needs a warning and a reduced claim boundary.",
                    details={"index": index, "depth_id": depth_id, "runtime_substrate_count": substrate_count},
                )
            )


def _check_selection_lane_counts(
    row: Mapping[str, Any],
    selection_lanes: Sequence[str],
    index: int,
    findings: list[AuditFinding],
) -> None:
    counts = _mapping(row.get("selection_lane_counts"))
    if not counts:
        return
    missing_lanes = [lane for lane in selection_lanes if lane not in counts]
    if missing_lanes:
        findings.append(
            AuditFinding(
                check_id="frontier_extra_mix_depth::depth::missing_selection_lanes",
                message="Depth receipt must record every registered selection lane.",
                details={"index": index, "depth_id": row.get("depth_id"), "missing_lanes": missing_lanes},
            )
        )
    positive_lanes = [lane for lane, value in counts.items() if (_int_or_none(value) or 0) > 0]
    pf_lane_names = {lane for lane in counts if "PF" in lane or "수익 팩터" in lane or "top_forward_pf" in lane}
    if positive_lanes and set(positive_lanes).issubset(pf_lane_names):
        findings.append(
            AuditFinding(
                check_id="frontier_extra_mix_depth::depth::pf_only_selection_forbidden",
                message="Extra Stage depth selection cannot be PF-only.",
                details={"index": index, "depth_id": row.get("depth_id"), "positive_lanes": positive_lanes},
            )
        )


def _check_mix_caps(
    mix_rows: Sequence[Mapping[str, Any]],
    depth_caps: Mapping[str, Mapping[str, int]],
    findings: list[AuditFinding],
) -> None:
    counts: dict[str, int] = {}
    for row in mix_rows:
        depth_id = str(row.get("depth_id", "")).strip()
        counts[depth_id] = counts.get(depth_id, 0) + 1
        lanes = _string_list(row.get("selection_lanes"))
        if lanes and all("PF" in lane or "수익 팩터" in lane or "top_forward_pf" in lane for lane in lanes):
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::mix_queue::pf_only_selection_forbidden",
                    message="Mix queue selection lanes cannot be PF-only.",
                    details={"mix_id": row.get("mix_id"), "selection_lanes": lanes},
                )
            )
    for depth_id, count in counts.items():
        caps = depth_caps.get(depth_id)
        if not caps:
            continue
        if count > caps["queue_cap"]:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::mix_queue::queue_cap_exceeded",
                    message="Mix queue count exceeds the registered cap for this mix depth.",
                    details={"depth_id": depth_id, "mix_queue_count": count, "cap": caps["queue_cap"]},
                )
            )


def _check_attempt_caps(
    attempt_rows: Sequence[Mapping[str, Any]],
    depth_caps: Mapping[str, Mapping[str, int]],
    findings: list[AuditFinding],
) -> None:
    counts: dict[str, int] = {}
    for row in attempt_rows:
        depth_id = str(row.get("depth_id", "")).strip()
        counts[depth_id] = counts.get(depth_id, 0) + 1
    for depth_id, count in counts.items():
        caps = depth_caps.get(depth_id)
        if not caps:
            continue
        if count > caps["mt5_attempt_cap"]:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::attempt::depth_attempt_cap_exceeded",
                    message="MT5 attempt count exceeds the registered cap for this mix depth.",
                    details={"depth_id": depth_id, "attempt_count": count, "cap": caps["mt5_attempt_cap"]},
                )
            )


def _check_total_attempt_cap(
    attempt_rows: Sequence[Mapping[str, Any]],
    contract: Mapping[str, Any],
    findings: list[AuditFinding],
) -> None:
    cap = _int_or_none(contract.get("total_mt5_attempt_cap_with_invalid_or_block_recovery")) or 30
    if len(attempt_rows) > cap:
        findings.append(
            AuditFinding(
                check_id="frontier_extra_mix_depth::attempt::total_attempt_cap_exceeded",
                message="Total MT5 attempts exceed the Extra Stage hard cap including invalid/block recovery.",
                details={"attempt_count": len(attempt_rows), "cap": cap},
            )
        )


def _check_attempt_mix_links(
    attempt_rows: Sequence[Mapping[str, Any]],
    mix_rows: Sequence[Mapping[str, Any]],
    findings: list[AuditFinding],
) -> None:
    mix_ids = {str(row.get("mix_id", "")).strip() for row in mix_rows if row.get("mix_id")}
    for index, row in enumerate(attempt_rows):
        mix_id = str(row.get("mix_id", "")).strip()
        if mix_id and mix_ids and mix_id not in mix_ids:
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::attempt::unknown_mix_id",
                    message="Materialized attempt references a mix that is not present in the mix queue receipt.",
                    details={"index": index, "attempt_id": row.get("attempt_id"), "mix_id": mix_id},
                )
            )


def _check_attempt_runtime_evidence(attempt_rows: Sequence[Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    for index, row in enumerate(attempt_rows):
        compile_status = str(row.get("compile_status", "")).strip().lower()
        tester_status = str(row.get("tester_status", "")).strip().lower()
        runtime_status = str(row.get("runtime_status", "")).strip().lower()
        report_status = str(row.get("report_status", "")).strip().lower()
        evidence_statuses = {_normalize_status(status) for status in (tester_status, runtime_status, report_status)}
        if compile_status in {"pass", "passed", "completed"} and not any(evidence_statuses & _RUNTIME_EVIDENCE_STATUSES):
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::attempt::compile_only_not_runtime_evidence",
                    message="Compile success without tester/runtime/report evidence cannot close a runtime attempt.",
                    details={"index": index, "attempt_id": row.get("attempt_id")},
                )
            )
        claim_text = f"{row.get('claim_effect', '')} {row.get('claim_boundary', '')}".lower()
        if "runtime" in claim_text and any(status in {"proxy_only", "proxy-only"} for status in evidence_statuses):
            findings.append(
                AuditFinding(
                    check_id="frontier_extra_mix_depth::attempt::proxy_only_not_runtime_evidence",
                    message="Proxy-only evidence cannot support a runtime learning claim.",
                    details={"index": index, "attempt_id": row.get("attempt_id"), "runtime_status": runtime_status},
                )
            )


def _check_forbidden_claims(
    rows: Sequence[Mapping[str, Any]],
    row_type: str,
    findings: list[AuditFinding],
) -> None:
    forbidden_terms = {
        "completion",
        "completed_claim",
        "selected_baseline",
        "operating_promotion",
        "runtime_authority",
        "live_readiness",
        "goal_achieve",
        "full_mix_materialized=true",
    }
    for index, row in enumerate(rows):
        text = f"{row.get('claim_effect', '')} {row.get('claim_boundary', '')}".lower()
        matches = [term for term in forbidden_terms if term in text and f"no_{term}" not in text]
        if matches:
            findings.append(
                AuditFinding(
                    check_id=f"frontier_extra_mix_depth::{row_type}::forbidden_claim_boundary",
                    message="Frontier Extra mix receipts cannot claim completion, baseline, promotion, runtime authority, live readiness, Goal Achieve, or full mix materialization.",
                    details={"index": index, "matches": matches},
                )
            )


def _check_int_cap(
    row: Mapping[str, Any],
    field: str,
    cap: int,
    index: int,
    cap_name: str,
    findings: list[AuditFinding],
) -> None:
    value = _int_or_none(row.get(field))
    if value is not None and value > cap:
        findings.append(
            AuditFinding(
                check_id=f"frontier_extra_mix_depth::depth::{cap_name}_exceeded",
                message="Depth receipt exceeds the registered progressive mix cap.",
                details={"index": index, "field": field, "actual": value, "cap": cap},
            )
        )


def _progressive_contract(path: Path) -> Mapping[str, Any]:
    registry = _load_mapping(path)
    overlay = _mapping(_mapping(registry.get("trigger_overlays")).get("frontier_extra_stage_due_check"))
    return _mapping(overlay.get("progressive_mix_depth_contract"))


def _depth_caps(contract: Mapping[str, Any]) -> dict[str, dict[str, int]]:
    caps: dict[str, dict[str, int]] = {}
    for item in _mapping_list(contract.get("depth_sequence")):
        depth_id = str(item.get("depth_id", "")).strip()
        if not depth_id:
            continue
        caps[depth_id] = {
            "queue_cap": _int_or_none(item.get("queue_cap")) or 0,
            "materialized_mix_cap": _int_or_none(item.get("materialized_mix_cap")) or 0,
            "mt5_attempt_cap": _int_or_none(item.get("mt5_attempt_cap")) or 0,
        }
    return caps


def _load_mapping(path: Path) -> Mapping[str, Any]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    text = io_path(path).read_text(encoding="utf-8-sig")
    payload = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(payload, Mapping):
        raise ValueError(f"{path} must contain a mapping")
    return payload


def _mapping_list(value: Any) -> list[Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, Sequence):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _depth_arity(depth_id: str) -> int | None:
    token = depth_id.strip().lower()
    if token.startswith("2mix") or token.startswith("2-mix"):
        return 2
    if token.startswith("3mix") or token.startswith("3-mix"):
        return 3
    if token.startswith("4mix") or token.startswith("4-mix"):
        return 4
    return None


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _int_or_none(value: Any) -> int | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _float_or_none(value: Any) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_status(value: Any) -> str:
    return str(value).strip().lower().replace(" ", "_")


_RUNTIME_EVIDENCE_STATUSES = {
    "completed",
    "complete",
    "pass",
    "passed",
    "failed",
    "fail",
    "blocked",
    "crashed",
    "crash",
    "mismatch",
    "zero_trade",
    "zero-trade",
    "invalid",
    "error",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Frontier Extra progressive mix depth receipts.")
    parser.add_argument("receipt_path")
    parser.add_argument("--registry-path", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_frontier_extra_mix_depth_receipt_path(
        Path(args.receipt_path),
        registry_path=Path(args.registry_path),
        root=Path(args.root),
    )
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output_json:
        output = Path(args.output_json)
        io_path(output.parent).mkdir(parents=True, exist_ok=True)
        io_path(output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if args.allow_blocked_exit_zero or result.status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

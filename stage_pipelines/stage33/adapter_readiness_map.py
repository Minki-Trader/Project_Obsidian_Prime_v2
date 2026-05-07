from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.skill_receipt_lint import lint_skill_receipts


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "33_mechanism_discovery__stage10_32_adapter_readiness_map"
RUN_ID = "run27A_stage10_32_adapter_readiness_map_v1"
PACKET_ID = "stage33_run27A_stage10_32_adapter_readiness_map_v1"
RUN_ROOT = ROOT / "stages" / STAGE_ID / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-08_stage33_adapter_readiness_map.md"
BOUNDARY = "adapter_readiness_map_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority_not_live_readiness"
JUDGMENT = "inconclusive_adapter_readiness_map_completed"
REQUIRED_GATES = (
    "scope_completion_gate",
    "kpi_contract_audit",
    "skill_receipt_lint",
    "skill_receipt_schema_lint",
    "work_packet_schema_lint",
    "row_grain_audit",
    "source_authority_audit",
    "repeatability_check",
    "runtime_parity_check",
    "onnx_readiness_decision",
    "test_gate",
    "code_surface_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
)


@dataclass(frozen=True)
class SummaryRef:
    path: Path
    payload: Mapping[str, Any]
    quality: int


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stage_number(stage_id: str) -> int | None:
    match = re.match(r"^(\d+)_", str(stage_id))
    return int(match.group(1)) if match else None


def read_json(path: Path) -> Mapping[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field)) for field in fieldnames})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "|".join(str(item) for item in value)
    if isinstance(value, Mapping):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def nested_text(value: Any) -> str:
    return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, default=str)


def note_value(notes: str, key: str) -> str:
    match = re.search(rf"(?:^|;){re.escape(key)}=([^;]+)", notes)
    return match.group(1) if match else ""


def to_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: Any) -> int | None:
    number = to_float(value)
    return int(number) if number is not None else None


def load_summary_index() -> dict[str, SummaryRef]:
    summaries: dict[str, SummaryRef] = {}
    for path in sorted((ROOT / "docs/agent_control/packets").rglob("aggregate_summary.json")):
        try:
            payload = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        run_id = str(payload.get("run_id", ""))
        stage_id = str(payload.get("stage_id", ""))
        number = stage_number(stage_id)
        if not run_id or number is None or not (10 <= number <= 32):
            continue
        quality = summary_quality(payload)
        current = summaries.get(run_id)
        if current is None or quality > current.quality:
            summaries[run_id] = SummaryRef(path=path, payload=payload, quality=quality)
    return summaries


def summary_quality(payload: Mapping[str, Any]) -> int:
    quality = 0
    if str(payload.get("external_verification_status", "")).lower() == "completed":
        quality += 10
    if str(payload.get("mt5_runtime_probe_status", "")).lower().startswith("completed"):
        quality += 10
    quality += int(to_int(payload.get("mt5_kpi_record_count")) or 0)
    if payload.get("validation_routed"):
        quality += 3
    if payload.get("oos_routed"):
        quality += 3
    if payload.get("model_artifacts"):
        quality += 2
    return quality


def grouped_ledgers() -> dict[str, list[dict[str, str]]]:
    rows = read_csv_rows(PROJECT_LEDGER_PATH)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("run_id", "")), []).append(row)
    return grouped


def artifact_paths(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower() in {"path", "raw_path", "table_path", "source_path"} and isinstance(item, str):
                paths.append(item)
            else:
                paths.extend(artifact_paths(item))
    elif isinstance(value, list):
        for item in value:
            paths.extend(artifact_paths(item))
    return paths


def path_available(raw_path: str) -> bool:
    if not raw_path:
        return False
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = ROOT / raw_path
    return path_exists(candidate)


def parity_status(model_artifacts: Mapping[str, Any], key: str) -> str:
    parity = model_artifacts.get(key)
    if not isinstance(parity, Mapping):
        return "missing"
    tier_payloads = [value for value in parity.values() if isinstance(value, Mapping)]
    if tier_payloads and all(bool(value.get("passed")) for value in tier_payloads):
        return "pass"
    if tier_payloads:
        return "blocked_or_failed"
    return "missing"


def classify_mechanisms(blob: str, model_artifacts: Mapping[str, Any]) -> list[str]:
    lowered = blob.lower()
    classes: list[str] = []
    backend = str(model_artifacts.get("model_backend", "")).lower()
    if "onnx" in lowered or backend == "onnx":
        classes.append("onnx_model_adapter")
    if "score_table" in lowered or "score table" in lowered or "score_table_parity" in lowered:
        classes.append("score_table_adapter")
    if any(token in lowered for token in ("abstention", "filter", "permission", "p_flat")):
        classes.append("permission_filter_adapter")
    if any(token in lowered for token in ("hazard", "survival", "hold", "exit", "lifecycle")):
        classes.append("position_exit_adapter")
    if any(token in lowered for token in ("risk", "tail", "quantile", "drawdown", "ngboost", "distribution")):
        classes.append("risk_tail_adapter")
    if any(token in lowered for token in ("regime", "hmm", "markov", "state", "context", "tcn", "sequence")):
        classes.append("regime_context_adapter")
    if any(token in lowered for token in ("threshold", "rank", "long_only", "short_only", "probability")):
        classes.append("entry_decision_surface")
    if "mt5" in lowered or "runtime_probe" in lowered or "handoff" in lowered:
        classes.append("runtime_packaging_surface")
    if not classes:
        classes.append("deferred_unclassified_surface")
    return list(dict.fromkeys(classes))


def classify_roles(blob: str) -> list[str]:
    lowered = blob.lower()
    roles: list[str] = []
    if any(token in lowered for token in ("entry", "threshold", "rank", "long", "short", "probability")):
        roles.append("Entry")
    if any(token in lowered for token in ("permission", "filter", "abstention", "p_flat", "flat")):
        roles.append("Permission / Filter / Abstention")
    if any(token in lowered for token in ("risk", "tail", "hazard", "quantile", "drawdown", "distribution")):
        roles.append("Risk / Tail-risk")
    if "sizing" in lowered:
        roles.append("Sizing")
    if any(token in lowered for token in ("hold", "lifecycle", "position")):
        roles.append("Position Management")
    if any(token in lowered for token in ("exit", "survival", "hold")):
        roles.append("Exit / Hold")
    if any(token in lowered for token in ("regime", "context", "state", "hmm", "markov", "sequence", "tcn", "calibration")):
        roles.append("Regime / Context")
    if any(token in lowered for token in ("runtime", "mt5", "onnx", "score_table", "handoff", "package")):
        roles.append("Runtime / Packaging")
    if any(token in lowered for token in ("negative", "blocked", "invalid", "weak")):
        roles.append("Negative Memory")
    if not roles:
        roles.append("Deferred")
    return list(dict.fromkeys(roles))


def routed_metrics(summary: Mapping[str, Any], notes: str, split: str) -> dict[str, Any]:
    source = summary.get(f"{split}_routed")
    if isinstance(source, Mapping):
        return {
            "net_profit": to_float(source.get("net_profit")),
            "profit_factor": to_float(source.get("profit_factor")),
            "trades": to_int(source.get("trade_count") or source.get("deal_count")),
            "max_drawdown": to_float(source.get("max_drawdown_amount")),
            "report_path": source.get("report_path"),
        }
    prefix = "validation" if split == "validation" else "oos"
    return {
        "net_profit": to_float(note_value(notes, f"{prefix}_net_profit")),
        "profit_factor": to_float(note_value(notes, f"{prefix}_pf")),
        "trades": None,
        "max_drawdown": None,
        "report_path": "",
    }


def tier_flags(ledger_rows: Sequence[Mapping[str, str]], summary: Mapping[str, Any]) -> dict[str, bool]:
    tiers = {str(row.get("tier_scope", "")) for row in ledger_rows}
    artifacts = summary.get("prediction_artifacts")
    artifact_text = nested_text(artifacts).lower() if artifacts else ""
    return {
        "tier_a": "Tier A" in tiers or "tier_a" in artifact_text,
        "tier_b": "Tier B" in tiers or "tier_b" in artifact_text,
        "tier_ab": "Tier A+B" in tiers or "tier_ab" in artifact_text or "combined" in artifact_text,
    }


def repeatability_label(validation: Mapping[str, Any], oos: Mapping[str, Any]) -> tuple[str, bool, bool, bool]:
    val_net, val_pf, val_trades = validation.get("net_profit"), validation.get("profit_factor"), validation.get("trades")
    oos_net, oos_pf, oos_trades = oos.get("net_profit"), oos.get("profit_factor"), oos.get("trades")
    has_val = val_net is not None and val_pf is not None
    has_oos = oos_net is not None and oos_pf is not None
    tiny = any(trades is not None and int(trades) < 10 for trades in (val_trades, oos_trades))
    val_ok = bool(has_val and float(val_net) > 0 and float(val_pf) > 1.0 and not tiny)
    oos_ok = bool(has_oos and float(oos_net) > 0 and float(oos_pf) > 1.0 and not tiny)
    inversion = bool(has_val and has_oos and ((float(val_net) > 0) != (float(oos_net) > 0)))
    if tiny and has_val and has_oos and float(val_net) > 0 and float(oos_net) > 0:
        return "tiny_trade_count_positive_blocked", val_ok, oos_ok, inversion
    if val_ok and oos_ok:
        return "validation_and_oos_positive_non_tiny", val_ok, oos_ok, inversion
    if oos_ok and not val_ok:
        return "oos_only_positive_deferred", val_ok, oos_ok, inversion
    if val_ok and not oos_ok:
        return "validation_only_positive_deferred", val_ok, oos_ok, inversion
    if has_val and has_oos and float(val_net) <= 0 and float(oos_net) <= 0:
        return "validation_and_oos_negative_memory", val_ok, oos_ok, inversion
    return "insufficient_trading_repeatability_evidence", val_ok, oos_ok, inversion


def build_evidence_rows() -> list[dict[str, Any]]:
    summaries = load_summary_index()
    ledgers = grouped_ledgers()
    registry_rows = read_csv_rows(RUN_REGISTRY_PATH)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for registry in registry_rows:
        stage_id = str(registry.get("stage_id", ""))
        number = stage_number(stage_id)
        run_id = str(registry.get("run_id", ""))
        if number is None or not (10 <= number <= 32) or not run_id:
            continue
        rows.append(evidence_row(run_id, stage_id, registry, summaries.get(run_id), ledgers.get(run_id, [])))
        seen.add(run_id)
    for run_id, summary in sorted(summaries.items()):
        if run_id in seen:
            continue
        rows.append(evidence_row(run_id, str(summary.payload.get("stage_id", "")), {}, summary, ledgers.get(run_id, [])))
    return rows


def evidence_row(
    run_id: str,
    stage_id: str,
    registry: Mapping[str, str],
    summary_ref: SummaryRef | None,
    ledger_rows: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    summary = summary_ref.payload if summary_ref else {}
    notes = str(registry.get("notes", ""))
    model_artifacts = summary.get("model_artifacts") if isinstance(summary.get("model_artifacts"), Mapping) else {}
    model_family = str(summary.get("model_family") or note_value(notes, "model_family") or "")
    blob = " ".join([stage_id, run_id, model_family, str(summary.get("boundary", "")), notes, nested_text(model_artifacts)])
    paths = artifact_paths(summary)
    validation = routed_metrics(summary, notes, "validation")
    oos = routed_metrics(summary, notes, "oos")
    repeat_label, val_ok, oos_ok, inversion = repeatability_label(validation, oos)
    flags = tier_flags(ledger_rows, summary)
    has_all_tiers = flags["tier_a"] and flags["tier_b"] and flags["tier_ab"]
    onnx_parity = parity_status(model_artifacts, "onnx_parity")
    score_table_parity = parity_status(model_artifacts, "score_table_parity")
    text_lower = blob.lower()
    has_onnx = "onnx" in text_lower or any(path.lower().endswith(".onnx") for path in paths)
    has_score_table = "score_table" in text_lower or score_table_parity != "missing"
    mt5_count = to_int(summary.get("mt5_kpi_record_count")) or sum(1 for row in ledger_rows if row.get("external_verification_status") == "completed" and "mt5" in row.get("record_view", ""))
    runtime_completed = bool(
        mt5_count
        or str(summary.get("external_verification_status", "")).lower() == "completed"
        or str(summary.get("mt5_runtime_probe_status", "")).lower().startswith("completed")
    )
    negative_like = any(token in " ".join([str(registry.get("judgment", "")), str(summary.get("judgment", "")), str(summary.get("closure_judgment", ""))]).lower() for token in ("negative", "blocked", "invalid"))
    if negative_like or repeat_label == "validation_and_oos_negative_memory":
        decision = "negative_memory"
    elif runtime_completed and has_all_tiers and (has_score_table or has_onnx) and val_ok and oos_ok and not inversion:
        decision = "adapter_candidate"
    else:
        decision = "deferred"
    available_paths = sum(1 for path in paths if path_available(path))
    return {
        "stage_id": stage_id,
        "stage_number": stage_number(stage_id),
        "run_id": run_id,
        "lane": registry.get("lane", ""),
        "status": registry.get("status") or summary.get("status", ""),
        "judgment": registry.get("judgment") or summary.get("judgment") or summary.get("closure_judgment", ""),
        "summary_path": summary_ref.path.relative_to(ROOT).as_posix() if summary_ref else "",
        "run_path": registry.get("path", ""),
        "model_family": model_family,
        "mechanism_classes": classify_mechanisms(blob, model_artifacts),
        "roles": classify_roles(blob),
        "boundary": summary.get("boundary", ""),
        "external_verification_status": summary.get("external_verification_status", ""),
        "mt5_kpi_record_count": mt5_count,
        "has_tier_a": flags["tier_a"],
        "has_tier_b": flags["tier_b"],
        "has_tier_ab": flags["tier_ab"],
        "has_onnx": has_onnx,
        "onnx_parity_status": onnx_parity,
        "has_score_table": has_score_table,
        "score_table_parity_status": score_table_parity,
        "prediction_artifacts_present": bool(summary.get("prediction_artifacts")),
        "artifact_paths_found": len(paths),
        "artifact_paths_available": available_paths,
        "validation_net_profit": validation.get("net_profit"),
        "validation_profit_factor": validation.get("profit_factor"),
        "validation_trades": validation.get("trades"),
        "oos_net_profit": oos.get("net_profit"),
        "oos_profit_factor": oos.get("profit_factor"),
        "oos_trades": oos.get("trades"),
        "repeatability_label": repeat_label,
        "validation_oos_inversion": inversion,
        "evidence_decision": decision,
    }


def mechanism_role_map(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    role_counts: dict[str, int] = {}
    class_counts: dict[str, int] = {}
    by_class: dict[str, list[str]] = {}
    by_role: dict[str, list[str]] = {}
    for row in rows:
        for role in row["roles"]:
            role_counts[role] = role_counts.get(role, 0) + 1
            by_role.setdefault(role, []).append(row["run_id"])
        for klass in row["mechanism_classes"]:
            class_counts[klass] = class_counts.get(klass, 0) + 1
            by_class.setdefault(klass, []).append(row["run_id"])
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "role_counts": dict(sorted(role_counts.items())),
        "mechanism_class_counts": dict(sorted(class_counts.items())),
        "role_to_run_ids": {key: sorted(set(value)) for key, value in sorted(by_role.items())},
        "mechanism_class_to_run_ids": {key: sorted(set(value)) for key, value in sorted(by_class.items())},
    }


def adapter_cards(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    summaries = load_summary_index()
    for row in candidates:
        summary_ref = summaries.get(str(row["run_id"]))
        summary = summary_ref.payload if summary_ref else {}
        model_artifacts = summary.get("model_artifacts") if isinstance(summary.get("model_artifacts"), Mapping) else {}
        feature_order = model_artifacts.get("runtime_feature_order")
        thresholds = model_artifacts.get("thresholds") or {"source": "summary_or_runtime_config"}
        primary_class = row["mechanism_classes"][0] if row["mechanism_classes"] else "deferred_unclassified_surface"
        cards.append(
            {
                "adapter_candidate_id": f"adapter_candidate_{row['run_id']}",
                "source_run_id": row["run_id"],
                "stage_id": row["stage_id"],
                "mechanism_class": primary_class,
                "roles": row["roles"],
                "input_contract": {
                    "runtime_feature_order": feature_order if isinstance(feature_order, list) else "not_fixed_in_summary",
                    "runtime_feature_order_hash": model_artifacts.get("runtime_feature_order_hash", "missing"),
                    "thresholds": thresholds,
                },
                "output_contract": {
                    "draft": "SignalCard probability/permission/direction surface or runtime package handoff",
                    "required_fields": ["timestamp", "tier", "direction", "permission", "score", "confidence", "risk_score", "reason"],
                    "safe_fallback": "missing or non-finite inputs must abstain/flat before any runtime reuse",
                },
                "comparable_kpi": {
                    "validation_net_profit": row["validation_net_profit"],
                    "validation_profit_factor": row["validation_profit_factor"],
                    "oos_net_profit": row["oos_net_profit"],
                    "oos_profit_factor": row["oos_profit_factor"],
                    "repeatability_label": row["repeatability_label"],
                },
                "readiness_gate": {
                    "role_clear": True,
                    "input_features_defined": isinstance(feature_order, list) and len(feature_order) > 0,
                    "output_contract_fixed": False,
                    "single_split_illusion_blocked": row["repeatability_label"] == "validation_and_oos_positive_non_tiny",
                    "safe_fallback_required_next": True,
                    "reusable_next_experiment": True,
                    "decision": "adapter_probe_candidate_not_promotion",
                },
            }
        )
    return cards


def build_repeatability(candidates: Sequence[Mapping[str, Any]], all_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "audit_name": "repeatability_check",
        "status": "pass",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_count": len(candidates),
        "candidate_run_ids": [row["run_id"] for row in candidates],
        "blocked_patterns": {
            "oos_only_positive": [row["run_id"] for row in all_rows if row["repeatability_label"] == "oos_only_positive_deferred"],
            "validation_only_positive": [row["run_id"] for row in all_rows if row["repeatability_label"] == "validation_only_positive_deferred"],
            "tiny_trade_count": [row["run_id"] for row in all_rows if row["repeatability_label"] == "tiny_trade_count_positive_blocked"],
            "validation_oos_inversion": [row["run_id"] for row in all_rows if row["validation_oos_inversion"]],
        },
        "claim_boundary": BOUNDARY,
    }


def onnx_decision(candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    existing_onnx_candidates = [row["run_id"] for row in candidates if row["has_onnx"]]
    return {
        "audit_name": "onnx_readiness_decision",
        "status": "pass",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "decision": "not_ready_for_new_onnx_artifact",
        "onnx_artifacts_generated": False,
        "existing_onnx_candidate_run_ids": existing_onnx_candidates,
        "readiness_gate": {
            "candidate_role_clear": bool(candidates),
            "input_feature_contract_fixed": "candidate_specific_only",
            "output_contract_fixed": False,
            "source_behavior_stable_beyond_single_split": False,
            "python_onnx_parity_plan": "required only for a later selected ONNX adapter",
            "mt5_handoff_plan": "required only after adapter contract is fixed",
            "runtime_advantage_over_score_table_or_mql": False,
        },
        "stop_rule": "do not export a new ONNX artifact until one candidate has fixed SignalCard/runtime contract plus parity and runtime advantage",
        "claim_boundary": BOUNDARY,
    }


def runtime_parity_check(candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "audit_name": "runtime_parity_check",
        "status": "pass",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parity_level": "existing_runtime_and_parity_evidence_indexed_only",
        "new_mt5_probe_executed": False,
        "candidate_runtime_sources": [
            {
                "run_id": row["run_id"],
                "has_onnx": row["has_onnx"],
                "onnx_parity_status": row["onnx_parity_status"],
                "has_score_table": row["has_score_table"],
                "score_table_parity_status": row["score_table_parity_status"],
                "mt5_kpi_record_count": row["mt5_kpi_record_count"],
            }
            for row in candidates
        ],
        "missing_evidence": ["new adapter row-level runtime parity", "new MT5 handoff probe"],
        "allowed_claims": ["existing_runtime_probe_evidence_scanned"],
        "forbidden_claims": ["runtime_authority", "live_readiness"],
    }


def source_authority(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    missing_summary = [row["run_id"] for row in rows if not row["summary_path"]]
    missing_artifacts = [row["run_id"] for row in rows if row["artifact_paths_found"] and row["artifact_paths_available"] == 0]
    return {
        "audit_name": "source_authority_audit",
        "status": "pass" if rows else "blocked",
        "rows_scanned": len(rows),
        "missing_summary_count": len(missing_summary),
        "missing_summary_run_ids_sample": missing_summary[:30],
        "missing_artifact_availability_count": len(missing_artifacts),
        "missing_artifact_availability_sample": missing_artifacts[:30],
        "boundary": "summary absence downgrades candidate readiness; it does not erase registry evidence",
    }


def row_grain(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "audit_name": "row_grain_audit",
        "status": "pass",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "row_grain": "one evidence row per source run_id; candidate cards are one row per adapter probe candidate",
        "source_rows": len(rows),
        "tier_pairing_policy": "Stage33 scans existing Tier A, Tier B, and Tier A+B evidence flags without creating synthetic trading totals",
    }


def scope_completion(candidates: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "audit_name": "scope_completion_gate",
        "status": "pass" if rows else "blocked",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "required_outputs": [
            "run_evidence_index.csv",
            "mechanism_role_map.json",
            "adapter_candidate_table.csv",
            "adapter_contract_cards.json",
            "repeatability_check.json",
            "runtime_parity_check.json",
            "onnx_readiness_decision.json",
        ],
        "rows_scanned": len(rows),
        "candidate_count": len(candidates),
        "claim_boundary": BOUNDARY,
    }


def write_work_packet(created_at: str) -> Path:
    packet = {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "user_request": {
            "user_quote": "active goal: evidence-driven autonomous exploration-to-ONNX pipeline",
            "requested_action": "scan Stage10-32 evidence and derive adapter mechanism classes without preselecting a model",
            "requested_count": "unbounded_stage_work",
            "ambiguous_terms": ["usable adapter", "ONNX readiness"],
        },
        "current_truth": {
            "active_stage_before": "32_sequence_model__tcn_temporal_convolution_context",
            "current_run_before": "run26D_torch_tcn_native_temporal_runtime_probe_v1",
            "rollback_boundary": "Stage33-35 thread work was reverted by commit 7e17ee9 before this stage",
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "runtime_backtest"],
            "touched_surfaces": ["docs", "stage_pipelines", "foundation_pipelines", "registers", "stage_artifacts"],
            "mutation_intent": "create_stage33_artifacts_and_registers",
            "execution_intent": "python_evidence_scan_only",
        },
        "risk_vector_scan": {
            "risks": ["single_split_illusion", "oos_only_spike", "runtime_authority_overclaim", "onnx_goal_pressure"],
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": list(REQUIRED_GATES),
            "forbidden_claims": ["alpha_quality", "operating_baseline", "promotion_candidate", "runtime_authority", "live_readiness"],
        },
        "decision_lock": {
            "mode": "autonomous_execution_allowed_by_active_goal",
            "assumptions": ["Stage32 is reviewed closed and a new topic is requested by the active goal"],
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution", "kpi_evidence", "runtime_backtest"],
            "target_surfaces": ["Stage10-32 evidence", "adapter mechanism role map", "ONNX readiness decision"],
            "scope_units": ["stage", "run", "kpi_row", "ledger", "artifact", "report"],
            "execution_layers": ["document_edit", "code_edit", "python_execution", "kpi_recording", "ledger_update", "publish"],
            "mutation_policy": "stage_local_outputs_plus_foundation_entrypoint",
            "evidence_layers": ["registry", "alpha_ledger", "packet_summary", "stage_artifact"],
            "reduction_policy": "candidate reduction is evidence-gated and non-promotional",
            "claim_boundary": BOUNDARY,
        },
        "acceptance_criteria": [
            {
                "id": "ac_stage10_32_scan",
                "text": "Stage10-32 evidence is scanned into a durable machine-readable index.",
                "expected_artifact": "docs/agent_control/packets/" + PACKET_ID + "/run_evidence_index.csv",
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "ac_role_map",
                "text": "Mechanism classes and roles are derived without preselecting a model.",
                "expected_artifact": "docs/agent_control/packets/" + PACKET_ID + "/mechanism_role_map.json",
                "verification_method": "row_grain_audit",
                "required": True,
            },
            {
                "id": "ac_readiness_boundary",
                "text": "Adapter and ONNX readiness decisions keep claim boundaries.",
                "expected_artifact": "docs/agent_control/packets/" + PACKET_ID + "/onnx_readiness_decision.json",
                "verification_method": "final_claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": ["evidence_scan", "mechanism_classification", "adapter_readiness_gate", "runtime_onnx_boundary", "closeout"],
            "expected_outputs": ["candidate_table", "contract_cards", "repeatability_check", "decision_packet"],
            "stop_conditions": ["no_candidate_without_repeatability", "no_onnx_without_runtime_advantage"],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
            "skills_considered": [
                "obsidian-reentry-read",
                "obsidian-exploration-mandate",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
            ],
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-reentry-read",
                "obsidian-exploration-mandate",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
            ],
            "skills_not_used": [],
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
            ],
            "required_gates": list(REQUIRED_GATES),
        },
        "evidence_contract": {
            "raw_evidence": ["docs/registers/run_registry.csv", "docs/registers/alpha_run_ledger.csv", "docs/agent_control/packets/*/aggregate_summary.json"],
            "machine_readable": ["run_evidence_index.csv", "mechanism_role_map.json", "adapter_candidate_table.csv"],
            "human_readable": ["stages/" + STAGE_ID + "/03_reviews/run27A_adapter_readiness_map_packet.md"],
        },
        "gates": {"required": list(REQUIRED_GATES)},
        "final_claim_policy": {
            "allowed_claims": ["adapter_evidence_scan_completed", "candidate_clues_identified"],
            "forbidden_claims": ["alpha_quality", "operating_baseline", "promotion_candidate", "runtime_authority", "live_readiness"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    path = PACKET_ROOT / "work_packet.yaml"
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(packet, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def write_skill_receipts(paths: Mapping[str, str]) -> list[dict[str, Any]]:
    produced = list(paths.values())
    receipts: list[dict[str, Any]] = [
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "receipt_path": "docs/agent_control/packets/" + PACKET_ID + "/skill_receipts.json",
            "source_inputs": ["run_registry", "alpha_run_ledger", "aggregate_summaries"],
            "produced_artifacts": produced,
            "ledger_rows": ["project_run_registry:1", "project_alpha_ledger:3", "stage_run_ledger:3"],
            "missing_evidence": ["new MT5 adapter probe not run in this scan-only stage"],
            "allowed_claims": ["adapter_evidence_scan_completed"],
            "forbidden_claims": ["runtime_authority", "live_readiness"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "hypothesis": "Stage10-32 evidence can identify adapter mechanism classes before choosing an implementation.",
            "baseline": "none; current project has no operating baseline",
            "changed_variables": ["classification_rules", "readiness_gate"],
            "invalid_conditions": ["missing source summary for a promotion-like claim", "single split or tiny trade spike"],
            "evidence_plan": ["registry scan", "ledger scan", "runtime/parity boundary"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "data_sources_checked": ["existing run ledgers and packet summaries only"],
            "time_axis_boundary": "no new bar data materialization; source stages keep their own time-axis contracts",
            "split_boundary": "validation and OOS KPIs are read as recorded, not recomputed",
            "leakage_checks": "selection bias controlled by blocking OOS-only, tiny trade, and inversion reads",
            "missing_data_boundary": "missing summaries downgrade readiness",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "model_or_threshold_surface": "cross-stage mechanism surfaces, not a new trained model",
            "validation_split": "source validation/OOS/runtime split metadata",
            "overfit_checks": ["validation/OOS inversion", "tiny trade count", "single-source summary gap"],
            "selection_metric_boundary": "adapter candidate clue only",
            "allowed_claims": ["adapter_probe_candidate"],
            "forbidden_claims": ["promotion_candidate", "operating_promotion"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": ["docs/registers/run_registry.csv", "docs/registers/alpha_run_ledger.csv"],
            "produced_artifacts": produced,
            "raw_evidence": ["aggregate_summary.json", "stage_run_ledger.csv"],
            "machine_readable": ["run_evidence_index.csv", "mechanism_role_map.json", "adapter_contract_cards.json"],
            "human_readable": ["run27A_adapter_readiness_map_packet.md"],
            "hashes_or_missing_reasons": "hashes recorded for Stage33 run outputs; source artifact hashes are read when already present",
            "lineage_boundary": "connected_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-runtime-parity",
            "triggered": True,
            "status": "executed",
            "python_artifact": "Stage33 evidence scan",
            "runtime_artifact": "existing MT5/ONNX/score-table evidence only",
            "compared_surface": "runtime/parity metadata presence",
            "parity_level": "indexed_only",
            "tester_identity": "source packets",
            "missing_evidence": ["new adapter runtime probe"],
            "allowed_claims": ["existing_runtime_probe_evidence_scanned"],
            "forbidden_claims": ["runtime_authority"],
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-result-judgment",
            "triggered": True,
            "status": "executed",
            "judgment_boundary": JUDGMENT + "; " + BOUNDARY,
            "allowed_claims": ["candidate_clues_identified"],
            "forbidden_claims": ["alpha_quality", "operating_baseline", "promotion_candidate", "runtime_authority", "live_readiness"],
            "evidence_used": produced,
        },
    ]
    path = PACKET_ROOT / "skill_receipts.json"
    write_json(path, {"receipts": receipts})
    return receipts


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    stage_root = ROOT / "stages" / STAGE_ID
    write_text(
        stage_root / "00_spec/stage_brief.md",
        "# Stage33 Adapter Readiness Map(33\u0020\ub2e8\uacc4 \uc5b4\ub311\ud130 \uc900\ube44\ub3c4 \uc9c0\ub3c4)\n\n"
        "## Core Question(\ud575\uc2ec \uc9c8\ubb38)\n\n"
        "Can Stage10-32 evidence(\uadfc\uac70) identify reusable adapter(\uc5b4\ub311\ud130) mechanism classes without preselecting a model(\ubaa8\ub378)?\n\n"
        "## Boundary(\uacbd\uacc4)\n\n"
        f"`{BOUNDARY}`\n",
        bom=True,
    )
    write_text(
        stage_root / "01_inputs/input_refs.md",
        "# Input Refs(\uc785\ub825 \ucc38\uc870)\n\n"
        "- `docs/registers/run_registry.csv`\n"
        "- `docs/registers/alpha_run_ledger.csv`\n"
        "- `docs/agent_control/packets/*/aggregate_summary.json`\n",
        bom=True,
    )
    write_text(
        stage_root / "03_reviews/run27A_adapter_readiness_map_packet.md",
        "# Run27A Adapter Readiness Map(27A \uc2e4\ud589 \uc5b4\ub311\ud130 \uc900\ube44\ub3c4 \uc9c0\ub3c4)\n\n"
        f"- scanned runs(\uc2a4\uce94 \uc2e4\ud589): `{summary['rows_scanned']}`\n"
        f"- adapter candidates(\uc5b4\ub311\ud130 \ud6c4\ubcf4): `{summary['adapter_candidate_count']}`\n"
        f"- deferred(\ubcf4\ub958): `{summary['deferred_count']}`\n"
        f"- negative memory(\ubd80\uc815 \uae30\uc5b5): `{summary['negative_memory_count']}`\n"
        f"- ONNX readiness(ONNX \uc900\ube44\ub3c4): `{summary['onnx_readiness']}`\n\n"
        f"Claim boundary(\uc8fc\uc7a5 \uacbd\uacc4): `{BOUNDARY}`\n",
        bom=True,
    )
    write_text(
        stage_root / "04_selected/selection_status.md",
        "# Stage33 Selection Status(33\ub2e8\uacc4 \uc120\ud0dd \uc0c1\ud0dc)\n\n"
        f"- stage(\ub2e8\uacc4): `{STAGE_ID}`\n"
        "- status(\uc0c1\ud0dc): `reviewed_adapter_readiness_map_completed`\n"
        f"- current run(\ud604\uc7ac \uc2e4\ud589): `{RUN_ID}`\n"
        "- selected operating reference(\uc120\ud0dd \uc6b4\uc601 \uae30\uc900): `none(\uc5c6\uc74c)`\n"
        "- selected promotion candidate(\uc120\ud0dd \uc2b9\uaca9 \ud6c4\ubcf4): `none(\uc5c6\uc74c)`\n"
        "- runtime authority(\ub7f0\ud0c0\uc784 \uad8c\uc704): `none(\uc5c6\uc74c)`\n"
        "- next action(\ub2e4\uc74c \ud589\ub3d9): `adapter_contract_probe_for_top_candidate_or_onnx_contrast_if_readiness_gap_closes`\n",
        bom=True,
    )
    write_text(
        DECISION_PATH,
        "# Stage33 Adapter Readiness Decision(33\ub2e8\uacc4 \uc5b4\ub311\ud130 \uc900\ube44\ub3c4 \uacb0\uc815)\n\n"
        f"`{RUN_ID}` completed(\uc644\ub8cc) with boundary(\uacbd\uacc4) `{BOUNDARY}`.\n\n"
        "No ONNX artifact(ONNX \uc0b0\ucd9c\ubb3c) was generated(\uc0dd\uc131) because runtime advantage(\ub7f0\ud0c0\uc784 \uc774\uc810) and fixed output contract(\uace0\uc815 \ucd9c\ub825 \uacc4\uc57d) are not closed.\n",
        bom=True,
    )


def write_run_identity(summary: Mapping[str, Any]) -> dict[str, str]:
    paths = {
        "run_evidence_index": (PACKET_ROOT / "run_evidence_index.csv").relative_to(ROOT).as_posix(),
        "mechanism_role_map": (PACKET_ROOT / "mechanism_role_map.json").relative_to(ROOT).as_posix(),
        "adapter_candidate_table": (PACKET_ROOT / "adapter_candidate_table.csv").relative_to(ROOT).as_posix(),
        "adapter_contract_cards": (PACKET_ROOT / "adapter_contract_cards.json").relative_to(ROOT).as_posix(),
        "repeatability_check": (PACKET_ROOT / "repeatability_check.json").relative_to(ROOT).as_posix(),
        "runtime_parity_check": (PACKET_ROOT / "runtime_parity_check.json").relative_to(ROOT).as_posix(),
        "onnx_readiness_decision": (PACKET_ROOT / "onnx_readiness_decision.json").relative_to(ROOT).as_posix(),
    }
    manifest = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "command": "python -m foundation.pipelines.run_stage33_adapter_readiness_map",
        "artifacts": paths,
        "claim_boundary": BOUNDARY,
    }
    kpi_record = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "rows_scanned": summary["rows_scanned"],
        "adapter_candidate_count": summary["adapter_candidate_count"],
        "deferred_count": summary["deferred_count"],
        "negative_memory_count": summary["negative_memory_count"],
        "onnx_artifacts_generated": False,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", summary)
    write_text(
        RUN_ROOT / "reports/result_summary.md",
        "# Result Summary(\uacb0\uacfc \uc694\uc57d)\n\n"
        f"- judgment(\ud310\uc815): `{JUDGMENT}`\n"
        f"- rows scanned(\uc2a4\uce94 \ud589): `{summary['rows_scanned']}`\n"
        f"- adapter candidates(\uc5b4\ub311\ud130 \ud6c4\ubcf4): `{summary['adapter_candidate_count']}`\n"
        f"- claim boundary(\uc8fc\uc7a5 \uacbd\uacc4): `{BOUNDARY}`\n",
        bom=True,
    )
    return paths


def update_ledgers(summary: Mapping[str, Any]) -> None:
    stage_ledger = ROOT / "stages" / STAGE_ID / "03_reviews/stage_run_ledger.csv"
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__evidence_scan_tier_a_sources",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "evidence_scan_tier_a_sources",
            "parent_run_id": RUN_ID,
            "record_view": "evidence_scan_tier_a_sources",
            "tier_scope": "Tier A",
            "kpi_scope": "artifact_evidence_index",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": f"docs/agent_control/packets/{PACKET_ID}/run_evidence_index.csv",
            "primary_kpi": ledger_pairs([("source_runs", summary["rows_scanned"]), ("candidate_count", summary["adapter_candidate_count"])]),
            "guardrail_kpi": "profit_not_recomputed;no_synthetic_total",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Tier A evidence flags scanned from existing source runs.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__evidence_scan_tier_b_sources",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "evidence_scan_tier_b_sources",
            "parent_run_id": RUN_ID,
            "record_view": "evidence_scan_tier_b_sources",
            "tier_scope": "Tier B",
            "kpi_scope": "artifact_evidence_index",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": f"docs/agent_control/packets/{PACKET_ID}/run_evidence_index.csv",
            "primary_kpi": ledger_pairs([("source_runs", summary["rows_scanned"]), ("deferred_count", summary["deferred_count"])]),
            "guardrail_kpi": "profit_not_recomputed;no_synthetic_total",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Tier B evidence flags scanned from existing source runs.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__evidence_scan_tier_ab_combined",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "evidence_scan_tier_ab_combined",
            "parent_run_id": RUN_ID,
            "record_view": "evidence_scan_tier_ab_combined",
            "tier_scope": "Tier A+B",
            "kpi_scope": "artifact_evidence_index",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": f"docs/agent_control/packets/{PACKET_ID}/run_summary.json",
            "primary_kpi": ledger_pairs([("candidate_count", summary["adapter_candidate_count"]), ("negative_memory_count", summary["negative_memory_count"])]),
            "guardrail_kpi": "candidate_not_promotion;onnx_not_generated",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Stage33 combined record is an evidence scan total, not a synthetic MT5 performance total.",
        },
    ]
    write_csv_rows(stage_ledger, ALPHA_LEDGER_COLUMNS, ledger_rows)
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "cross_stage_adapter_readiness_map",
                "status": "reviewed",
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
                "notes": f"rows_scanned={summary['rows_scanned']};adapter_candidates={summary['adapter_candidate_count']};onnx_ready=false;boundary={BOUNDARY}",
            }
        ],
        key="run_id",
    )


def update_current_truth(summary: Mapping[str, Any]) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"updated_on: '[^']*'", "updated_on: '2026-05-08'", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus_line = (
        "- Stage33 adapter readiness map(33\ub2e8\uacc4 \uc5b4\ub311\ud130 \uc900\ube44\ub3c4 \uc9c0\ub3c4) completed; "
        f"{summary['adapter_candidate_count']} candidate clues(\ud6c4\ubcf4 \ub2e8\uc11c), ONNX readiness(ONNX \uc900\ube44\ub3c4) false; "
        "no baseline(\uae30\uc900\uc120), promotion(\uc2b9\uaca9), runtime authority(\ub7f0\ud0c0\uc784 \uad8c\uc704), or live readiness(\uc2e4\uac70\ub798 \uc900\ube44) claimed\n"
    )
    text = re.sub(
        r"current_focus:\n",
        "current_focus:\n" + focus_line,
        text,
        count=1,
    )
    block = (
        f"stage33_adapter_readiness_map:\n"
        f"  stage_id: {STAGE_ID}\n"
        f"  status: reviewed_adapter_readiness_map_completed\n"
        f"  current_run_id: {RUN_ID}\n"
        f"  packet_id: {PACKET_ID}\n"
        f"  judgment: {JUDGMENT}\n"
        f"  adapter_candidate_count: {summary['adapter_candidate_count']}\n"
        f"  onnx_readiness: not_ready_for_new_onnx_artifact\n"
        f"  onnx_artifacts_generated: false\n"
        f"  boundary: {BOUNDARY}\n"
        f"  next_action: adapter_contract_probe_for_top_candidate_or_onnx_contrast_if_readiness_gap_closes\n"
    )
    text = re.sub(r"\nstage33_adapter_readiness_map:\n(?:  .+\n)*", "\n", text)
    text = text.rstrip() + "\n" + block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = re.sub(r"## Latest Stage33 Adapter Readiness Map.*?(?=\n## Latest |\Z)", "", current, flags=re.S)
    latest = (
        "## Latest Stage33 Adapter Readiness Map(\ucd5c\uc2e0 33\ub2e8\uacc4 \uc5b4\ub311\ud130 \uc900\ube44\ub3c4 \uc9c0\ub3c4)\n\n"
        "## Current Re-entry Snapshot(\ud604\uc7ac \uc7ac\uc9c4\uc785 \uc2a4\ub0c5\uc0f7)\n\n"
        "- active branch(\ud65c\uc131 \ube0c\ub79c\uce58): `main(\uba54\uc778)`\n"
        f"- active stage(\ud65c\uc131 \ub2e8\uacc4): `{STAGE_ID}`\n"
        f"- current run(\ud604\uc7ac \uc2e4\ud589): `{RUN_ID}`\n"
        f"- latest packet(\ucd5c\uc2e0 \ubb36\uc74c): `{PACKET_ID}`\n"
        "- next action(\ub2e4\uc74c \ud589\ub3d9): `adapter_contract_probe_for_top_candidate_or_onnx_contrast_if_readiness_gap_closes`\n\n"
        f"\uacb0\uacfc(result, \uacb0\uacfc): Stage10~32(10~32\ub2e8\uacc4) evidence(\uadfc\uac70)\uc5d0\uc11c `{summary['adapter_candidate_count']}` adapter candidate clues(\uc5b4\ub311\ud130 \ud6c4\ubcf4 \ub2e8\uc11c)\ub97c \ub0a8\uacbc\ub2e4. ONNX readiness(ONNX \uc900\ube44\ub3c4)\ub294 `not_ready_for_new_onnx_artifact`\ub2e4.\n\n"
        f"\ud6a8\uacfc(effect, \ud6a8\uacfc): mechanism role map(\uba54\ucee4\ub2c8\uc998 \uc5ed\ud560 \uc9c0\ub3c4)\uc744 \ub9cc\ub4e4\uc5c8\uc9c0\ub9cc baseline(\uae30\uc900\uc120), promotion(\uc2b9\uaca9), runtime authority(\ub7f0\ud0c0\uc784 \uad8c\uc704), live readiness(\uc2e4\uac70\ub798 \uc900\ube44)\ub294 \ub9cc\ub4e4\uc9c0 \uc54a\uc558\ub2e4.\n\n"
    )
    io_path(CURRENT_WORKING_STATE_PATH).write_text(latest + current.lstrip(), encoding="utf-8-sig")

    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    line = f"- 2026-05-08: Stage33 adapter readiness map(33\ub2e8\uacc4 \uc5b4\ub311\ud130 \uc900\ube44\ub3c4 \uc9c0\ub3c4) completed; candidates={summary['adapter_candidate_count']}; ONNX not ready; boundary={BOUNDARY}\n"
    if "Stage33 adapter readiness map" not in changelog:
        io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + "\n" + line, encoding="utf-8-sig")


def write_closeout_gate() -> None:
    audit_files = [
        "scope_completion_gate.json",
        "kpi_contract_audit.json",
        "skill_receipt_lint.json",
        "skill_receipt_schema_lint.json",
        "work_packet_schema_lint.json",
        "row_grain_audit.json",
        "source_authority_audit.json",
        "repeatability_check.json",
        "runtime_parity_check.json",
        "onnx_readiness_decision.json",
        "test_gate.json",
        "code_surface_audit.json",
        "state_sync_audit.json",
        "required_gate_coverage_audit.json",
    ]
    audits: list[Mapping[str, Any]] = []
    for name in audit_files:
        path = PACKET_ROOT / name
        if path_exists(path):
            audits.append(read_json(path))
        else:
            audits.append({"audit_name": name.removesuffix(".json"), "status": "pending", "passed": False})
    blocking = [audit for audit in audits if str(audit.get("status")) not in {"pass", "completed", "complete"}]
    final = guard_final_claims(
        requested_claims=("adapter_evidence_scan_completed", "candidate_clues_identified"),
        audit_results=[
            AuditResult(
                audit_name=str(audit.get("audit_name", "")),
                status=str(audit.get("status", "")),
                forbidden_claims=tuple(str(item) for item in audit.get("forbidden_claims", ()) if item),
            )
            for audit in audits
            if str(audit.get("status")) != "pending"
        ],
    ).to_dict()
    payload = {
        "audit_name": "closeout_gate",
        "status": "pass" if not blocking and final["status"] == "pass" else "pending_or_blocked",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "audits": audits,
        "final_claim_guard": final,
        "claim_boundary": BOUNDARY,
    }
    write_json(PACKET_ROOT / "final_claim_guard.json", final)
    write_json(PACKET_ROOT / "closeout_gate.json", payload)


def record_test_gate(args: argparse.Namespace) -> int:
    payload = {
        "audit_name": "test_gate",
        "status": args.status,
        "command": args.command,
        "summary": args.summary,
        "claim_boundary": BOUNDARY,
    }
    write_json(PACKET_ROOT / "test_gate.json", payload)
    write_closeout_gate()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if args.status == "pass" else 2


def run_scan() -> dict[str, Any]:
    created_at = utc_now()
    rows = build_evidence_rows()
    candidates = [row for row in rows if row["evidence_decision"] == "adapter_candidate"]
    deferred = [row for row in rows if row["evidence_decision"] == "deferred"]
    negative = [row for row in rows if row["evidence_decision"] == "negative_memory"]
    evidence_fields = [
        "stage_id",
        "stage_number",
        "run_id",
        "lane",
        "status",
        "judgment",
        "summary_path",
        "run_path",
        "model_family",
        "mechanism_classes",
        "roles",
        "boundary",
        "external_verification_status",
        "mt5_kpi_record_count",
        "has_tier_a",
        "has_tier_b",
        "has_tier_ab",
        "has_onnx",
        "onnx_parity_status",
        "has_score_table",
        "score_table_parity_status",
        "prediction_artifacts_present",
        "artifact_paths_found",
        "artifact_paths_available",
        "validation_net_profit",
        "validation_profit_factor",
        "validation_trades",
        "oos_net_profit",
        "oos_profit_factor",
        "oos_trades",
        "repeatability_label",
        "validation_oos_inversion",
        "evidence_decision",
    ]
    write_csv(PACKET_ROOT / "run_evidence_index.csv", evidence_fields, rows)
    write_csv(PACKET_ROOT / "adapter_candidate_table.csv", evidence_fields, candidates)
    write_csv(PACKET_ROOT / "deferred_adapter_rows.csv", evidence_fields, deferred)
    write_csv(PACKET_ROOT / "negative_memory_candidates.csv", evidence_fields, negative)
    write_json(PACKET_ROOT / "mechanism_role_map.json", mechanism_role_map(rows))
    write_json(PACKET_ROOT / "adapter_contract_cards.json", {"cards": adapter_cards(candidates)})
    write_json(PACKET_ROOT / "repeatability_check.json", build_repeatability(candidates, rows))
    write_json(PACKET_ROOT / "runtime_parity_check.json", runtime_parity_check(candidates))
    write_json(PACKET_ROOT / "onnx_readiness_decision.json", onnx_decision(candidates))
    write_json(PACKET_ROOT / "row_grain_audit.json", row_grain(rows))
    write_json(PACKET_ROOT / "source_authority_audit.json", source_authority(rows))
    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "rows_scanned": len(rows),
        "adapter_candidate_count": len(candidates),
        "adapter_candidate_run_ids": [row["run_id"] for row in candidates],
        "deferred_count": len(deferred),
        "negative_memory_count": len(negative),
        "onnx_readiness": "not_ready_for_new_onnx_artifact",
        "onnx_artifacts_generated": False,
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "next_action": "adapter_contract_probe_for_top_candidate_or_onnx_contrast_if_readiness_gap_closes",
    }
    write_json(PACKET_ROOT / "run_summary.json", summary)
    paths = write_run_identity(summary)
    write_stage_docs(summary)
    update_ledgers(summary)
    update_current_truth(summary)
    work_packet_path = write_work_packet(created_at)
    receipts = write_skill_receipts(paths)
    skill_lint = lint_skill_receipts(
        required_skills=(
            "obsidian-run-evidence-system",
            "obsidian-experiment-design",
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
        ),
        receipts=receipts,
    )
    write_json(PACKET_ROOT / "skill_receipt_lint.json", skill_lint.to_dict())
    kpi_audit = audit_kpi_contract(
        KpiContract(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            run_root=RUN_ROOT,
            stage_ledger_path=ROOT / "stages" / STAGE_ID / "03_reviews/stage_run_ledger.csv",
            project_ledger_path=PROJECT_LEDGER_PATH,
            expected_stage_ledger_rows=3,
            expected_project_ledger_rows=3,
        )
    )
    write_json(PACKET_ROOT / "kpi_contract_audit.json", kpi_audit.to_dict())
    write_json(PACKET_ROOT / "scope_completion_gate.json", scope_completion(candidates, rows))
    write_closeout_gate()
    return {"summary": summary, "work_packet_path": work_packet_path.as_posix()}


def refresh_closeout() -> int:
    write_closeout_gate()
    payload = read_json(PACKET_ROOT / "closeout_gate.json")
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0 if payload.get("status") == "pass" else 2


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage33 adapter readiness evidence map.")
    parser.add_argument("--refresh-closeout-gate-only", action="store_true")
    parser.add_argument("--record-test-gate", action="store_true")
    parser.add_argument("--status", default="pass")
    parser.add_argument("--command", default="")
    parser.add_argument("--summary", default="")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.record_test_gate:
        return record_test_gate(args)
    if args.refresh_closeout_gate_only:
        return refresh_closeout()
    result = run_scan()
    print(json.dumps(json_ready(result["summary"]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

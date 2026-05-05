from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.adapters.contracts import ADAPTER_ROLE_NAMES, AdapterOutputContract
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "33_adapter_runtime__mechanism_role_map_signal_contract"
RUN_ID = "run27A_mechanism_role_map_evidence_scan_v1"
PACKET_ID = "stage33_run27A_mechanism_role_map_evidence_scan_v1"
BOUNDARY = "evidence_scan_and_adapter_contract_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

ROLE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Entry": (
        "entry",
        "signal",
        "threshold",
        "direction",
        "logreg",
        "lightgbm",
        "lgbm",
        "extratrees",
        "mlp",
        "svm",
        "lda",
        "qda",
        "xgboost",
        "catboost",
        "ebm",
        "gam",
        "elasticnet",
        "tabnet",
        "tcn",
    ),
    "Permission / Filter / Abstention": (
        "permission",
        "filter",
        "abstention",
        "abstain",
        "p_flat",
        "block",
        "flat",
        "regime classifier",
    ),
    "Risk / Tail-risk": ("tail-risk", "tail risk", "tail", "quantile", "distribution", "ngboost", "drawdown", "hazard"),
    "Sizing": ("sizing", "position size", "size overlay"),
    "Position Management": ("position management", "lifecycle", "reversal", "carry", "followthrough"),
    "Exit / Hold": ("exit", "hold", "survival", "time-to-event", "hazard", "close-on-flat"),
    "Regime / Context": (
        "regime",
        "hmm",
        "markov",
        "state",
        "session",
        "volatility",
        "trend",
        "chop",
        "macro",
        "gap",
        "overnight",
        "mega",
        "sequence",
        "temporal",
    ),
    "Runtime / Packaging": (
        "onnx",
        "runtime",
        "handoff",
        "score-table",
        "score table",
        "mt5",
        "parity",
        "packaging",
    ),
    "Negative Memory": ("negative", "blocked", "invalid", "failed", "failure", "no stable", "inversion", "weak"),
    "Deferred": ("inconclusive", "deferred", "out_of_scope", "not_attempted", "next_action", "supplement"),
}

MECHANISM_CLASS_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("onnx_model_runtime", ("onnx", "parity")),
    ("sequence_context_surface", ("tcn", "temporal", "sequence")),
    ("calibration_decision_layer", ("calibration", "abstention", "abstain")),
    ("regime_context_gate", ("regime", "hmm", "markov", "state")),
    ("risk_lifecycle_surface", ("hazard", "survival", "tail", "quantile", "risk")),
    ("model_probability_surface", ("model", "probability", "classifier", "boost", "logistic", "tabnet", "river")),
    ("score_table_runtime", ("score-table", "score table")),
    ("rule_context_gate", ("threshold", "filter", "permission", "session", "volatility", "trend", "gap")),
)

NET_RE = re.compile(r"(?:net_profit|validation_net_profit|oos_net_profit)=(-?\d+(?:\.\d+)?)")
PF_RE = re.compile(r"(?:pf|validation_pf|oos_pf|profit_factor)=(-?\d+(?:\.\d+)?)")
TRADES_RE = re.compile(r"(?:trades|trade_count)=(-?\d+(?:\.\d+)?)")


@dataclass(frozen=True)
class RoleMapResult:
    summary: dict[str, Any]
    candidates: list[dict[str, Any]]
    signal_contracts: dict[str, Any]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def stage_number(stage_id: str) -> int | None:
    prefix = str(stage_id or "").split("_", 1)[0]
    return int(prefix) if prefix.isdigit() else None


def infer_roles(text: str) -> list[str]:
    lowered = text.lower()
    roles: list[str] = []
    for role in ADAPTER_ROLE_NAMES:
        if any(_keyword_hit(lowered, keyword) for keyword in ROLE_KEYWORDS[role]):
            roles.append(role)
    if not roles:
        roles.append("Deferred")
    if "Negative Memory" in roles and "Deferred" not in roles:
        roles.append("Deferred")
    return roles


def infer_mechanism_class(text: str) -> str:
    lowered = text.lower()
    for mechanism_class, keywords in MECHANISM_CLASS_KEYWORDS:
        if any(_keyword_hit(lowered, keyword) for keyword in keywords):
            return mechanism_class
    return "unclassified_mechanism_surface"


def _keyword_hit(lowered_text: str, keyword: str) -> bool:
    lowered_keyword = str(keyword).lower()
    if re.search(r"[^a-z0-9_]", lowered_keyword):
        return lowered_keyword in lowered_text
    return re.search(rf"(?<![a-z0-9]){re.escape(lowered_keyword)}(?![a-z0-9])", lowered_text) is not None


def build_mechanism_role_map(root: Path | str = Path("."), *, min_stage: int = 10, max_stage: int = 32) -> RoleMapResult:
    root_path = Path(root)
    run_registry_path = root_path / "docs/registers/run_registry.csv"
    alpha_ledger_path = root_path / "docs/registers/alpha_run_ledger.csv"
    run_rows = read_csv_rows(run_registry_path)
    alpha_rows = read_csv_rows(alpha_ledger_path)
    alpha_by_run: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in alpha_rows:
        alpha_by_run[str(row.get("run_id", ""))].append(row)

    candidates: list[dict[str, Any]] = []
    for row in run_rows:
        stage_id = str(row.get("stage_id", ""))
        number = stage_number(stage_id)
        if number is None or number < min_stage or number > max_stage:
            continue
        run_id = str(row.get("run_id", ""))
        ledgers = alpha_by_run.get(run_id, [])
        text = _evidence_text(row, ledgers)
        mechanism_text = _mechanism_text(row, ledgers)
        roles = infer_roles(mechanism_text)
        mechanism_class = infer_mechanism_class(mechanism_text)
        evidence = _evidence_flags(row, ledgers)
        adapter_gate = _adapter_readiness(roles, mechanism_class, evidence, mechanism_text)
        onnx_gate = _onnx_readiness(roles, mechanism_class, evidence, mechanism_text, adapter_gate)
        candidates.append(
            {
                "candidate_id": f"stage{number}_{run_id}",
                "stage_id": stage_id,
                "stage_number": number,
                "run_id": run_id,
                "lane": row.get("lane", ""),
                "status": row.get("status", ""),
                "judgment": row.get("judgment", ""),
                "mechanism_class": mechanism_class,
                "roles": roles,
                "evidence": evidence,
                "adapter_readiness": adapter_gate,
                "onnx_readiness": onnx_gate,
                "claim_boundary": BOUNDARY,
                "source_path": row.get("path", ""),
            }
        )

    candidates.sort(key=_candidate_sort_key)
    summary = _summary(root_path, candidates, run_registry_path, alpha_ledger_path, min_stage, max_stage)
    signal_contracts = _signal_contracts(candidates)
    stage_rows = _stage_ledger_rows(summary)
    run_registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_adapter_evidence_scan",
        "status": "reviewed",
        "judgment": "inconclusive_mechanism_role_map_evidence_scan_completed",
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("candidate_count", summary["counts"]["candidate_count"]),
                ("adapter_partial_or_ready", summary["counts"]["adapter_partial_or_ready"]),
                ("onnx_export_ready", summary["counts"]["onnx_export_ready"]),
                ("boundary", BOUNDARY),
            )
        ),
    }
    artifact_rows = _artifact_rows()
    return RoleMapResult(
        summary=summary,
        candidates=candidates,
        signal_contracts=signal_contracts,
        stage_rows=stage_rows,
        run_registry_row=run_registry_row,
        artifact_rows=artifact_rows,
    )


def write_role_map_packet(root: Path | str = Path("."), *, generated_at_utc: str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_mechanism_role_map(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    role_map_path = run_root / "role_map.json"
    candidate_csv_path = run_root / "adapter_candidate_matrix.csv"
    signal_contract_path = run_root / "signal_contracts.json"
    manifest_path = run_root / "run_manifest.json"
    result_summary_path = reports_root / "result_summary.md"
    aggregate_summary_path = packet_root / "aggregate_summary.json"

    _write_json(role_map_path, {"generated_at_utc": generated_at, **result.summary, "candidates": result.candidates})
    _write_candidate_csv(candidate_csv_path, result.candidates)
    _write_json(signal_contract_path, {"generated_at_utc": generated_at, **result.signal_contracts})
    manifest = _manifest(root_path, generated_at, role_map_path, candidate_csv_path, signal_contract_path, result)
    _write_json(manifest_path, manifest)
    _write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "reviewed_scan_completed",
        "judgment": "inconclusive_mechanism_role_map_evidence_scan_completed",
        "boundary": BOUNDARY,
        "generated_at_utc": generated_at,
        "role_map_path": _rel(root_path, role_map_path),
        "candidate_matrix_path": _rel(root_path, candidate_csv_path),
        "signal_contracts_path": _rel(root_path, signal_contract_path),
        "run_manifest_path": _rel(root_path, manifest_path),
        "result_summary_path": _rel(root_path, result_summary_path),
        "counts": result.summary["counts"],
        "top_adapter_candidates": result.summary["top_adapter_candidates"],
        "onnx_decision": result.summary["onnx_decision"],
        "required_gates": {
            "evidence_gate": "completed_stage10_32_register_scan",
            "repeatability_check": result.summary["repeatability_check"],
            "runtime_parity_check": result.summary["runtime_parity_check"],
            "claim_boundary": BOUNDARY,
        },
    }
    _write_json(aggregate_summary_path, aggregate)

    _upsert_registers(root_path, result)
    upsert_csv_rows(
        root_path / "stages" / STAGE_ID / "03_reviews/stage_run_ledger.csv",
        ALPHA_LEDGER_COLUMNS,
        result.stage_rows,
        key="ledger_row_id",
    )
    return aggregate


def _evidence_text(run_row: Mapping[str, str], ledger_rows: Sequence[Mapping[str, str]]) -> str:
    fields = [run_row.get(key, "") for key in ("run_id", "stage_id", "lane", "status", "judgment", "notes", "path")]
    for row in ledger_rows:
        fields.extend(
            row.get(key, "")
            for key in (
                "subrun_id",
                "record_view",
                "tier_scope",
                "kpi_scope",
                "scoreboard_lane",
                "status",
                "judgment",
                "primary_kpi",
                "guardrail_kpi",
                "external_verification_status",
                "notes",
            )
        )
    return " ".join(str(item) for item in fields if item)


def _mechanism_text(run_row: Mapping[str, str], ledger_rows: Sequence[Mapping[str, str]]) -> str:
    fields = [run_row.get(key, "") for key in ("run_id", "stage_id", "lane", "judgment", "notes", "path")]
    for row in ledger_rows:
        fields.extend(row.get(key, "") for key in ("subrun_id", "record_view", "tier_scope", "kpi_scope", "judgment", "notes"))
    text = " ".join(str(item) for item in fields if item)
    return text.replace("regular_risk_execution", "").replace("trading_risk_execution", "")


def _evidence_flags(run_row: Mapping[str, str], ledger_rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    text = _evidence_text(run_row, ledger_rows).lower()
    row_texts = [" ".join(str(value).lower() for value in row.values()) for row in ledger_rows]
    validation_rows = [row for row, row_text in zip(ledger_rows, row_texts) if "validation" in row_text]
    oos_rows = [row for row, row_text in zip(ledger_rows, row_texts) if "oos" in row_text]
    mt5_rows = [row for row, row_text in zip(ledger_rows, row_texts) if "mt5" in row_text or "runtime_probe" in row_text]
    wfo_rows = [row for row, row_text in zip(ledger_rows, row_texts) if "wfo" in row_text or "rolling" in row_text]
    python_rows = [row for row, row_text in zip(ledger_rows, row_texts) if "python" in row_text or "structural" in row_text]
    external_statuses = sorted({row.get("external_verification_status", "") for row in ledger_rows if row.get("external_verification_status")})
    validation_net = _best_metric(validation_rows, NET_RE)
    oos_net = _best_metric(oos_rows, NET_RE)
    validation_pf = _best_metric(validation_rows, PF_RE)
    oos_pf = _best_metric(oos_rows, PF_RE)
    min_trades = _min_metric(validation_rows + oos_rows, TRADES_RE)
    validation_oos_inversion = validation_net is not None and oos_net is not None and validation_net <= 0 < oos_net
    oos_only_positive = validation_oos_inversion or (validation_net is None and oos_net is not None and oos_net > 0)
    tiny_trade_count = min_trades is not None and min_trades < 50
    return {
        "project_ledger_rows": len(ledger_rows),
        "validation_rows": len(validation_rows),
        "oos_rows": len(oos_rows),
        "mt5_rows": len(mt5_rows),
        "python_rows": len(python_rows),
        "wfo_rows": len(wfo_rows),
        "has_validation": bool(validation_rows),
        "has_oos": bool(oos_rows),
        "has_mt5": bool(mt5_rows),
        "has_wfo_or_rolling": bool(wfo_rows),
        "has_onnx": "onnx" in text,
        "has_score_table": "score-table" in text or "score table" in text,
        "external_verification_statuses": external_statuses,
        "external_verification_completed": "completed" in external_statuses,
        "validation_net_profit_best": validation_net,
        "oos_net_profit_best": oos_net,
        "validation_pf_best": validation_pf,
        "oos_pf_best": oos_pf,
        "min_trade_count_seen": min_trades,
        "validation_oos_inversion": validation_oos_inversion,
        "oos_only_positive": oos_only_positive,
        "tiny_trade_count_spike": tiny_trade_count,
    }


def _adapter_readiness(
    roles: Sequence[str],
    mechanism_class: str,
    evidence: Mapping[str, Any],
    text: str,
) -> dict[str, Any]:
    role_clear = any(role not in {"Negative Memory", "Deferred"} for role in roles)
    input_defined = any(token in text.lower() for token in ("feature", "core24", "full58", "score-table", "score table", "model"))
    output_defined = role_clear and mechanism_class != "unclassified_mechanism_surface"
    comparable_kpi = bool(evidence.get("has_validation") and evidence.get("has_oos"))
    not_single_split = bool(comparable_kpi or evidence.get("has_wfo_or_rolling"))
    safe_fallback = True
    reusable = role_clear and output_defined and safe_fallback
    blockers = []
    if evidence.get("validation_oos_inversion"):
        blockers.append("validation_oos_inversion")
    if evidence.get("oos_only_positive"):
        blockers.append("oos_only_positive")
    if evidence.get("tiny_trade_count_spike"):
        blockers.append("tiny_trade_count_spike")
    checks = {
        "role_clear": role_clear,
        "input_defined": input_defined,
        "output_signalcard_contract": output_defined,
        "comparable_kpi": comparable_kpi,
        "not_single_split": not_single_split,
        "safe_fallback_no_trade": safe_fallback,
        "reusable_next_experiment": reusable,
    }
    score = sum(1 for passed in checks.values() if passed)
    deferred_role = "Deferred" in roles or "Negative Memory" in roles
    if blockers:
        state = "deferred"
    elif deferred_role and score >= 5:
        state = "partial_adapter_candidate"
    elif deferred_role:
        state = "deferred"
    elif score == len(checks):
        state = "ready_for_adapter_probe"
    elif score >= 5:
        state = "partial_adapter_candidate"
    else:
        state = "deferred"
    return {
        "state": state,
        "score": score,
        "max_score": len(checks),
        "checks": checks,
        "blockers": blockers,
        "safe_fallback": "no_trade",
    }


def _onnx_readiness(
    roles: Sequence[str],
    mechanism_class: str,
    evidence: Mapping[str, Any],
    text: str,
    adapter_gate: Mapping[str, Any],
) -> dict[str, Any]:
    role_clear = any(role not in {"Negative Memory", "Deferred"} for role in roles)
    input_contract_fixed = bool(adapter_gate["checks"]["input_defined"])
    output_contract_fixed = bool(adapter_gate["checks"]["output_signalcard_contract"])
    source_stable = adapter_gate["state"] == "ready_for_adapter_probe" and not adapter_gate["blockers"]
    not_single_split = bool(adapter_gate["checks"]["not_single_split"])
    parity_plan = bool(evidence.get("has_onnx"))
    mt5_plan = bool(evidence.get("has_mt5") or "runtime" in text.lower())
    runtime_advantage = mechanism_class in {"onnx_model_runtime", "model_probability_surface", "sequence_context_surface"} and not evidence.get("has_score_table")
    dedicated_export_packet_open = False
    checks = {
        "candidate_role_clear": role_clear,
        "input_feature_contract_fixed": input_contract_fixed,
        "output_contract_fixed": output_contract_fixed,
        "source_behavior_stable": source_stable,
        "not_single_split_illusion": not_single_split,
        "python_vs_onnx_parity_plan": parity_plan,
        "mt5_runtime_handoff_plan": mt5_plan,
        "onnx_runtime_advantage": runtime_advantage,
        "dedicated_export_packet_open": dedicated_export_packet_open,
    }
    score = sum(1 for passed in checks.values() if passed)
    if all(checks.values()):
        decision = "ready_to_export_or_refresh_onnx"
    elif evidence.get("has_onnx"):
        decision = "existing_onnx_evidence_only_defer_new_export"
    else:
        decision = "defer_no_onnx_export"
    return {"decision": decision, "score": score, "max_score": len(checks), "checks": checks}


def _summary(
    root: Path,
    candidates: Sequence[Mapping[str, Any]],
    run_registry_path: Path,
    alpha_ledger_path: Path,
    min_stage: int,
    max_stage: int,
) -> dict[str, Any]:
    role_counts: Counter[str] = Counter()
    class_counts = Counter(str(candidate["mechanism_class"]) for candidate in candidates)
    for candidate in candidates:
        role_counts.update(candidate["roles"])
    adapter_candidates = [
        candidate
        for candidate in candidates
        if candidate["adapter_readiness"]["state"] in {"ready_for_adapter_probe", "partial_adapter_candidate"}
    ]
    onnx_ready = [
        candidate
        for candidate in candidates
        if candidate["onnx_readiness"]["decision"] == "ready_to_export_or_refresh_onnx"
    ]
    return {
        "scan_scope": {
            "min_stage": min_stage,
            "max_stage": max_stage,
            "source_registers": [
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
                "stages/<stage_id>/03_reviews/stage_run_ledger.csv",
            ],
        },
        "source_hashes": {
            "run_registry": sha256_file_lf_normalized(run_registry_path),
            "alpha_run_ledger": sha256_file_lf_normalized(alpha_ledger_path),
        },
        "counts": {
            "candidate_count": len(candidates),
            "adapter_partial_or_ready": len(adapter_candidates),
            "onnx_export_ready": len(onnx_ready),
            "roles": dict(sorted(role_counts.items())),
            "mechanism_classes": dict(sorted(class_counts.items())),
        },
        "top_adapter_candidates": [
            {
                "candidate_id": candidate["candidate_id"],
                "stage_id": candidate["stage_id"],
                "run_id": candidate["run_id"],
                "mechanism_class": candidate["mechanism_class"],
                "roles": candidate["roles"],
                "adapter_state": candidate["adapter_readiness"]["state"],
                "onnx_decision": candidate["onnx_readiness"]["decision"],
            }
            for candidate in _dedupe_top_candidates(adapter_candidates, limit=10)
        ],
        "onnx_decision": {
            "ready_count": len(onnx_ready),
            "decision": "defer_new_onnx_export_until_adapter_probe_survives_repeatability"
            if not onnx_ready
            else "ready_candidates_exist_requires_dedicated_export_packet",
            "existing_onnx_rows": sum(1 for candidate in candidates if candidate["evidence"]["has_onnx"]),
        },
        "repeatability_check": {
            "status": "scan_only",
            "rule": "validation/OOS or WFO/rolling evidence is required before adapter probe readiness.",
            "single_split_blocker": "candidate is partial/deferred when comparable validation/OOS or WFO evidence is absent.",
        },
        "runtime_parity_check": {
            "status": "scan_only",
            "rule": "ONNX export remains deferred unless parity and MT5 handoff plan are explicit.",
        },
        "claim_boundary": BOUNDARY,
    }


def _signal_contracts(candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    output_contract = AdapterOutputContract().to_dict()
    role_contracts: dict[str, Any] = {}
    for role in ADAPTER_ROLE_NAMES:
        role_contracts[role] = {
            "output_contract": output_contract,
            "safe_fallback": "no_trade",
            "required_next_probe_fields": [
                "candidate_id",
                "source_run_id",
                "input_contract",
                "output_contract",
                "validation_oos_or_wfo_reference",
                "claim_boundary",
            ],
        }
    return {
        "contract_family": "SignalCard/AdapterContract",
        "version": "stage33_run27A_v1",
        "role_contracts": role_contracts,
        "candidate_contract_count": len(candidates),
    }


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__mechanism_role_map",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mechanism_role_map",
            "parent_run_id": RUN_ID,
            "record_view": "stage10_32_evidence_scan",
            "tier_scope": "Tier A+B",
            "kpi_scope": "mechanism_role_map",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "inconclusive_mechanism_role_map_scan_completed",
            "path": f"{run_root}/role_map.json",
            "primary_kpi": ledger_pairs(
                (
                    ("candidate_count", summary["counts"]["candidate_count"]),
                    ("adapter_partial_or_ready", summary["counts"]["adapter_partial_or_ready"]),
                )
            ),
            "guardrail_kpi": ledger_pairs((("onnx_export_ready", summary["counts"]["onnx_export_ready"]),)),
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Stage10-32 evidence scan; no model training, MT5 run, or ONNX export in this subrun.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__adapter_readiness_matrix",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_readiness_matrix",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_candidate_matrix",
            "tier_scope": "Tier A+B",
            "kpi_scope": "adapter_readiness_gate",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "inconclusive_adapter_readiness_matrix_completed",
            "path": f"{run_root}/adapter_candidate_matrix.csv",
            "primary_kpi": ledger_pairs((("partial_or_ready", summary["counts"]["adapter_partial_or_ready"]),)),
            "guardrail_kpi": "safe_fallback=no_trade;single_split_blocker=enforced",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Adapter readiness is a next-probe filter, not promotion or baseline evidence.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__onnx_readiness_decision",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "onnx_readiness_decision",
            "parent_run_id": RUN_ID,
            "record_view": "onnx_readiness_gate",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_packaging_gate",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "defer_new_onnx_export_until_adapter_probe_survives_repeatability",
            "path": f"{run_root}/signal_contracts.json",
            "primary_kpi": ledger_pairs((("onnx_export_ready", summary["counts"]["onnx_export_ready"]),)),
            "guardrail_kpi": "python_vs_onnx_parity_plan_required;mt5_handoff_plan_required",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "ONNX remains optional packaging; no new ONNX artifact generated by run27A.",
        },
    ]


def _artifact_rows() -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "artifact_id": f"{RUN_ID}__role_map",
            "type": "evidence_scan",
            "path": f"{run_root}/role_map.json",
            "status": "tracked_reviewed",
            "notes": "Stage10-32 mechanism role map; scan-only boundary.",
        },
        {
            "artifact_id": f"{RUN_ID}__adapter_candidate_matrix",
            "type": "adapter_readiness_matrix",
            "path": f"{run_root}/adapter_candidate_matrix.csv",
            "status": "tracked_reviewed",
            "notes": "Adapter readiness gate matrix; no promotion or ONNX export.",
        },
        {
            "artifact_id": f"{RUN_ID}__signal_contracts",
            "type": "runtime_contract",
            "path": f"{run_root}/signal_contracts.json",
            "status": "tracked_reviewed",
            "notes": "SignalCard/AdapterContract output contract for future adapter probes.",
        },
        {
            "artifact_id": f"{RUN_ID}__result_summary",
            "type": "result_summary",
            "path": f"{run_root}/reports/result_summary.md",
            "status": "tracked_reviewed",
            "notes": "Human readout for Stage33 run27A scan.",
        },
    ]


def _candidate_sort_key(candidate: Mapping[str, Any]) -> tuple[int, int, int, int]:
    gate = candidate["adapter_readiness"]
    evidence = candidate["evidence"]
    state_rank = {"ready_for_adapter_probe": 0, "partial_adapter_candidate": 1, "deferred": 2}.get(gate["state"], 3)
    return (
        state_rank,
        -int(gate["score"]),
        -int(bool(evidence.get("has_mt5"))),
        -int(candidate.get("stage_number") or 0),
    )


def _dedupe_top_candidates(candidates: Sequence[Mapping[str, Any]], *, limit: int) -> list[Mapping[str, Any]]:
    selected: list[Mapping[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for candidate in candidates:
        primary_role = next(
            (role for role in candidate["roles"] if role not in {"Deferred", "Negative Memory", "Runtime / Packaging"}),
            next((role for role in candidate["roles"] if role not in {"Deferred", "Negative Memory"}), "Deferred"),
        )
        key = (str(candidate["mechanism_class"]), str(primary_role))
        if key in seen:
            continue
        seen.add(key)
        selected.append(candidate)
        if len(selected) >= limit:
            break
    return selected


def _best_metric(rows: Sequence[Mapping[str, str]], pattern: re.Pattern[str]) -> float | None:
    values = _metric_values(rows, pattern)
    return max(values) if values else None


def _min_metric(rows: Sequence[Mapping[str, str]], pattern: re.Pattern[str]) -> float | None:
    values = _metric_values(rows, pattern)
    return min(values) if values else None


def _metric_values(rows: Sequence[Mapping[str, str]], pattern: re.Pattern[str]) -> list[float]:
    values: list[float] = []
    for row in rows:
        text = " ".join(str(row.get(name, "")) for name in ("primary_kpi", "guardrail_kpi", "notes"))
        for match in pattern.finditer(text):
            values.append(float(match.group(1)))
    return values


def _manifest(
    root: Path,
    generated_at: str,
    role_map_path: Path,
    candidate_csv_path: Path,
    signal_contract_path: Path,
    result: RoleMapResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.mechanism_role_map",
        "inputs": {
            "run_registry": {
                "path": "docs/registers/run_registry.csv",
                "sha256_lf_normalized": result.summary["source_hashes"]["run_registry"],
            },
            "alpha_run_ledger": {
                "path": "docs/registers/alpha_run_ledger.csv",
                "sha256_lf_normalized": result.summary["source_hashes"]["alpha_run_ledger"],
            },
        },
        "outputs": {
            "role_map": {"path": _rel(root, role_map_path), "sha256": sha256_file_lf_normalized(role_map_path)},
            "adapter_candidate_matrix": {
                "path": _rel(root, candidate_csv_path),
                "sha256": sha256_file_lf_normalized(candidate_csv_path),
            },
            "signal_contracts": {
                "path": _rel(root, signal_contract_path),
                "sha256": sha256_file_lf_normalized(signal_contract_path),
            },
        },
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: RoleMapResult) -> str:
    top = result.summary["top_adapter_candidates"][:8]
    lines = [
        "# Stage33 RUN27A Mechanism Role Map Evidence Scan(33단계 실행27A 메커니즘 역할 지도 근거 스캔)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- candidates scanned(스캔 후보): `{result.summary['counts']['candidate_count']}`",
        f"- adapter partial/ready(어댑터 부분/준비 후보): `{result.summary['counts']['adapter_partial_or_ready']}`",
        f"- ONNX export ready(ONNX 내보내기 준비): `{result.summary['counts']['onnx_export_ready']}`",
        "",
        "## Evidence Gate(근거 게이트)",
        "",
        "Stage10~32(10~32단계) run_registry(실행 등록부)와 alpha_run_ledger(알파 실행 장부)를 읽었다. 효과(effect, 효과)는 새 model(모델)을 미리 정하지 않고 기존 evidence(근거)에서 mechanism class(메커니즘 분류)를 도출하는 것이다.",
        "",
        "## Top Adapter Candidates(상위 어댑터 후보)",
        "",
    ]
    if not top:
        lines.append("- none(없음): adapter readiness gate(어댑터 준비 게이트)를 통과한 후보가 없다.")
    for item in top:
        lines.append(
            f"- `{item['candidate_id']}`: `{item['mechanism_class']}`, roles(역할)={', '.join(item['roles'])}, adapter_state(어댑터 상태)=`{item['adapter_state']}`, onnx_decision(ONNX 결정)=`{item['onnx_decision']}`"
        )
    lines.extend(
        [
            "",
            "## ONNX Decision(ONNX 결정)",
            "",
            f"`{result.summary['onnx_decision']['decision']}`. 효과(effect, 효과)는 ONNX(온닉스)를 목표로 강제하지 않고, adapter probe(어댑터 탐침)가 repeatability(반복성)와 parity plan(동등성 계획)을 만족할 때만 export(내보내기)로 넘기는 것이다.",
            "",
            "## Explicit Non-Claims(명시적 비주장)",
            "",
            "- alpha quality(알파 품질) 주장 없음",
            "- operating baseline(운영 기준선) 주장 없음",
            "- promotion candidate(승격 후보) 주장 없음",
            "- runtime authority(런타임 권위) 주장 없음",
            "- live readiness(실거래 준비) 주장 없음",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_markdown(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def _write_candidate_csv(path: Path, candidates: Sequence[Mapping[str, Any]]) -> None:
    columns = (
        "candidate_id",
        "stage_id",
        "run_id",
        "mechanism_class",
        "roles",
        "adapter_state",
        "adapter_score",
        "onnx_decision",
        "has_validation",
        "has_oos",
        "has_mt5",
        "has_wfo_or_rolling",
        "has_onnx",
        "validation_net_profit_best",
        "oos_net_profit_best",
        "validation_oos_inversion",
        "tiny_trade_count_spike",
        "claim_boundary",
    )
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        evidence = candidate["evidence"]
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "stage_id": candidate["stage_id"],
                "run_id": candidate["run_id"],
                "mechanism_class": candidate["mechanism_class"],
                "roles": "|".join(candidate["roles"]),
                "adapter_state": candidate["adapter_readiness"]["state"],
                "adapter_score": candidate["adapter_readiness"]["score"],
                "onnx_decision": candidate["onnx_readiness"]["decision"],
                "has_validation": evidence["has_validation"],
                "has_oos": evidence["has_oos"],
                "has_mt5": evidence["has_mt5"],
                "has_wfo_or_rolling": evidence["has_wfo_or_rolling"],
                "has_onnx": evidence["has_onnx"],
                "validation_net_profit_best": evidence["validation_net_profit_best"],
                "oos_net_profit_best": evidence["oos_net_profit_best"],
                "validation_oos_inversion": evidence["validation_oos_inversion"],
                "tiny_trade_count_spike": evidence["tiny_trade_count_spike"],
                "claim_boundary": candidate["claim_boundary"],
            }
        )
    _write_csv_rows(path, columns, rows)


def _write_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def _upsert_registers(root: Path, result: RoleMapResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Stage33 mechanism role map and adapter readiness scan.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_mechanism_role_map(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_role_map_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

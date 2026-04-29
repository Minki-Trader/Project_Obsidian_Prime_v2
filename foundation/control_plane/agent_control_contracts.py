from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

import yaml

from foundation.control_plane.audit_result import AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


REQUIRED_AGENT_CONTROL_FILES = (
    "docs/agent_control/codex_operating_format.yaml",
    "docs/agent_control/work_packet.schema.yaml",
    "docs/agent_control/code_surface_baseline.yaml",
    "docs/agent_control/n_a_reason_registry.yaml",
    "docs/agent_control/claim_vocabulary.yaml",
    "docs/agent_control/kpi_source_authority.yaml",
    "docs/agent_control/row_grain_contract.yaml",
    "docs/agent_control/work_family_registry.yaml",
    "docs/agent_control/surface_registry.yaml",
    "docs/agent_control/risk_flag_registry.yaml",
    "docs/agent_control/skill_receipt_schema.yaml",
)

REQUIRED_TEMPLATE_FILES = (
    "docs/templates/work_packet.template.yaml",
    "docs/templates/run_plan.template.yaml",
    "docs/templates/work_plan.template.yaml",
    "docs/templates/closeout_report.template.yaml",
    "docs/templates/closeout_report.template.md",
    "docs/templates/kpi_record_normalized.template.json",
)

EXPECTED_KPI_LAYERS = (
    "run_identity",
    "signal_model",
    "mt5_trading_headline",
    "risk",
    "trade_diagnostics",
    "regime_slice_attribution",
    "execution",
)

EXPECTED_ROW_GRAIN_KEYS = ("run_id", "variant_id", "split", "tier_scope", "record_view", "route_role")
EXPECTED_WORK_FAMILIES = (
    "information_only",
    "state_sync",
    "policy_skill_governance",
    "code_edit",
    "code_refactor",
    "experiment_design",
    "experiment_execution",
    "runtime_backtest",
    "kpi_evidence",
    "artifact_lineage",
    "cleanup_archive",
    "publish_handoff",
)
EXPECTED_SURFACES = (
    "docs_current_truth",
    "policies_and_skills",
    "foundation_code",
    "pipelines",
    "mt5_runtime",
    "kpi_ledgers",
    "run_artifacts",
)
EXPECTED_RISK_FLAGS = (
    "scope_ambiguous",
    "mutation_ambiguous",
    "state_sync_risk",
    "claim_boundary_risk",
    "skill_abandonment_risk",
    "evidence_gap_risk",
    "runtime_parity_risk",
    "kpi_source_risk",
    "code_surface_risk",
    "destructive_change_risk",
    "unattended_autonomy_risk",
    "answer_clarity_risk",
)


def audit_agent_control_contracts(root: Path | str = Path(".")) -> AuditResult:
    root_path = Path(root)
    findings: list[AuditFinding] = []
    counts: dict[str, Any] = {}

    payloads: dict[str, Mapping[str, Any]] = {}
    for relative in (*REQUIRED_AGENT_CONTROL_FILES, *REQUIRED_TEMPLATE_FILES):
        path = root_path / relative
        exists = path_exists(path)
        counts[f"file::{relative}"] = {"exists": exists, "path": relative}
        if not exists:
            findings.append(
                AuditFinding(
                    check_id=f"agent_control_file::{relative}",
                    message="Required agent-control contract or template is missing.",
                    details={"path": relative},
                )
            )
            continue
        try:
            payloads[relative] = _load_structured(path)
        except Exception as exc:  # pragma: no cover - defensive error path
            findings.append(
                AuditFinding(
                    check_id=f"agent_control_parse::{relative}",
                    message="Required agent-control contract or template could not be parsed.",
                    details={"path": relative, "error": str(exc)},
                )
            )

    _check_row_grain(payloads, findings)
    _check_kpi_authority(payloads, findings)
    _check_n_a_reasons(payloads, findings)
    _check_claim_vocabulary(payloads, findings)
    _check_normalized_kpi_template(payloads, findings)
    _check_work_packet_schema(payloads, findings)
    _check_control_plane_v2_registries(payloads, findings)

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="agent_control_contracts",
        status=status,
        findings=tuple(findings),
        counts=counts,
        allowed_claims=("contracts_ready",) if status == "pass" else ("blocked",),
        forbidden_claims=() if status == "pass" else ("contracts_ready",),
    )


def _load_structured(path: Path) -> Mapping[str, Any]:
    text = io_path(path).read_text(encoding="utf-8-sig")
    if path.suffix == ".md":
        return {"text": text}
    if path.suffix == ".json":
        payload = json.loads(text)
    else:
        payload = yaml.safe_load(text)
    if not isinstance(payload, Mapping):
        raise ValueError("payload must be a mapping")
    return payload


def _check_row_grain(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    payload = payloads.get("docs/agent_control/row_grain_contract.yaml", {})
    keys = tuple(payload.get("normalized_row_key", ()))
    missing = [key for key in EXPECTED_ROW_GRAIN_KEYS if key not in keys]
    if missing:
        findings.append(
            AuditFinding(
                check_id="row_grain_contract::missing_keys",
                message="Row grain contract is missing required normalized row keys.",
                details={"missing": missing, "expected": EXPECTED_ROW_GRAIN_KEYS},
            )
        )


def _check_kpi_authority(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    payload = payloads.get("docs/agent_control/kpi_source_authority.yaml", {})
    layers = payload.get("layers", {})
    if not isinstance(layers, Mapping):
        layers = {}
    missing_layers = [layer for layer in EXPECTED_KPI_LAYERS if layer not in layers]
    if missing_layers:
        findings.append(
            AuditFinding(
                check_id="kpi_source_authority::missing_layers",
                message="KPI source authority is missing required 7-layer entries.",
                details={"missing": missing_layers},
            )
        )
    mt5_layer = layers.get("mt5_trading_headline", {})
    if isinstance(mt5_layer, Mapping) and mt5_layer.get("authority") != "mt5_strategy_tester_report":
        findings.append(
            AuditFinding(
                check_id="kpi_source_authority::mt5_headline_authority",
                message="MT5 trading headline authority must be the MT5 Strategy Tester report.",
                details={"actual": mt5_layer.get("authority")},
            )
        )


def _check_n_a_reasons(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    payload = payloads.get("docs/agent_control/n_a_reason_registry.yaml", {})
    reasons = payload.get("allowed_reasons", {})
    if not isinstance(reasons, Mapping):
        reasons = {}
    required = (
        "run_has_no_variant_layer",
        "python_structural_only_no_mt5_report",
        "gross_loss_is_zero",
        "trade_telemetry_missing",
        "runtime_telemetry_missing",
        "invalid_scope_mismatch",
    )
    missing = [reason for reason in required if reason not in reasons]
    if missing:
        findings.append(
            AuditFinding(
                check_id="n_a_reason_registry::missing_required",
                message="N/A reason registry is missing required reasons.",
                details={"missing": missing},
            )
        )


def _check_claim_vocabulary(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    payload = payloads.get("docs/agent_control/claim_vocabulary.yaml", {})
    claims = payload.get("claim_classes", {})
    if not isinstance(claims, Mapping):
        claims = {}
    required = ("completed", "completed_reduced_scope", "partial", "blocked", "invalid", "verified")
    missing = [claim for claim in required if claim not in claims]
    if missing:
        findings.append(
            AuditFinding(
                check_id="claim_vocabulary::missing_claims",
                message="Claim vocabulary is missing required claim classes.",
                details={"missing": missing},
            )
        )


def _check_normalized_kpi_template(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    payload = payloads.get("docs/templates/kpi_record_normalized.template.json", {})
    missing_layers = [layer for layer in EXPECTED_KPI_LAYERS if layer not in payload]
    if missing_layers:
        findings.append(
            AuditFinding(
                check_id="normalized_kpi_template::missing_layers",
                message="Normalized KPI template is missing required 7-layer entries.",
                details={"missing": missing_layers},
            )
        )
    row_grain = payload.get("row_grain", {})
    if not isinstance(row_grain, Mapping):
        row_grain = {}
    missing_keys = [key for key in EXPECTED_ROW_GRAIN_KEYS if key not in row_grain]
    if missing_keys:
        findings.append(
            AuditFinding(
                check_id="normalized_kpi_template::missing_row_grain",
                message="Normalized KPI template is missing required row-grain fields.",
                details={"missing": missing_keys},
            )
        )


def _check_work_packet_schema(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    payload = payloads.get("docs/agent_control/work_packet.schema.yaml", {})
    required = payload.get("required_top_level", ())
    for key in ("preflight", "acceptance_criteria", "kpi_contract", "final_claim_policy"):
        if key not in required:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::missing_required_top_level",
                    message="Work packet schema is missing a required top-level section.",
                    details={"missing": key},
                )
            )


def _check_control_plane_v2_registries(payloads: Mapping[str, Mapping[str, Any]], findings: list[AuditFinding]) -> None:
    family_payload = payloads.get("docs/agent_control/work_family_registry.yaml", {})
    families = family_payload.get("families", {})
    if not isinstance(families, Mapping):
        families = {}
    missing_families = [family for family in EXPECTED_WORK_FAMILIES if family not in families]
    if missing_families:
        findings.append(
            AuditFinding(
                check_id="work_family_registry::missing_families",
                message="Work family registry is missing required families.",
                details={"missing": missing_families},
            )
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Project Obsidian agent-control contracts and templates.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_agent_control_contracts(Path(args.root))
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

    surface_payload = payloads.get("docs/agent_control/surface_registry.yaml", {})
    surfaces = surface_payload.get("surfaces", {})
    if not isinstance(surfaces, Mapping):
        surfaces = {}
    missing_surfaces = [surface for surface in EXPECTED_SURFACES if surface not in surfaces]
    if missing_surfaces:
        findings.append(
            AuditFinding(
                check_id="surface_registry::missing_surfaces",
                message="Surface registry is missing required surfaces.",
                details={"missing": missing_surfaces},
            )
        )

    risk_payload = payloads.get("docs/agent_control/risk_flag_registry.yaml", {})
    risks = risk_payload.get("risks", {})
    if not isinstance(risks, Mapping):
        risks = {}
    missing_risks = [risk for risk in EXPECTED_RISK_FLAGS if risk not in risks]
    if missing_risks:
        findings.append(
            AuditFinding(
                check_id="risk_flag_registry::missing_risks",
                message="Risk flag registry is missing required risk axes.",
                details={"missing": missing_risks},
            )
        )

    receipt_payload = payloads.get("docs/agent_control/skill_receipt_schema.yaml", {})
    schemas = receipt_payload.get("schemas", {})
    if not isinstance(schemas, Mapping) or "default" not in schemas:
        findings.append(
            AuditFinding(
                check_id="skill_receipt_schema::missing_default",
                message="Skill receipt schema must define a default receipt schema.",
                details={},
            )
        )

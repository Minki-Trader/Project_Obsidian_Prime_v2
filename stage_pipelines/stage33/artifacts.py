from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

import yaml

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "33_adapter_mechanism__evidence_driven_role_map"
RUN_ID = "run27A_evidence_driven_adapter_role_map_v1"
RUN_NUMBER = "run27A"
PACKET_ID = "stage33_run27A_evidence_driven_adapter_role_map_v1"
EXPLORATION_LABEL = "stage33_AdapterMechanism__EvidenceDrivenRoleMap"
STATUS = "blocked"
JUDGMENT = "exploratory_adapter_contract_candidates_identified_runtime_inputs_not_fixed"
BOUNDARY = "evidence_map_and_contract_candidates_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"


def materialize(root: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    paths = stage_paths(root)
    for directory in {path.parent for path in paths.values()}:
        directory.mkdir(parents=True, exist_ok=True)

    inventory = payload["inventory"]
    role_map = payload["role_map"]
    gates = payload["gates"]
    evidence_rows = payload["evidence_rows"]

    write_json(paths["source_inventory"], inventory)
    write_json(paths["evidence_rows"], evidence_rows)
    write_json(paths["mechanism_role_map"], {k: v for k, v in role_map.items() if k != "adapter_candidates"})
    write_json(paths["adapter_candidates"], role_map["adapter_candidates"])
    for name, gate_payload in gates.items():
        write_json(paths[name], gate_payload)

    write_yaml(paths["work_packet"], build_work_packet(inventory, role_map))
    write_json(paths["skill_receipts"], build_skill_receipts(inventory, role_map))
    write_md(paths["stage_brief"], stage_brief_md(inventory, role_map))
    write_md(paths["stage_open_draft"], stage_open_md(inventory, role_map))
    write_md(paths["review_packet"], review_packet_md(inventory, role_map, gates))
    write_md(paths["review_index"], review_index_md())
    write_md(paths["selection_status"], selection_status_md(role_map))
    write_md(paths["decision"], decision_md(inventory, role_map, gates))
    write_md(paths["packet_readme"], packet_readme_md(inventory, role_map, gates))

    ledger_payloads = write_ledgers(root, paths, inventory, role_map)
    update_workspace_state(root)
    update_current_working_state(root, inventory, role_map)
    update_changelog(root, role_map)

    closeout = build_closeout(root, inventory, role_map, gates, ledger_payloads)
    write_json(paths["closeout_gate"], closeout)
    run_summary = build_run_summary(paths, inventory, role_map, gates, ledger_payloads, closeout)
    write_json(paths["run_summary"], run_summary)
    return run_summary


def stage_paths(root: Path) -> dict[str, Path]:
    stage_root = root / "stages" / STAGE_ID
    packet_root = root / "docs/agent_control/packets" / PACKET_ID
    return {
        "stage_root": stage_root,
        "packet_root": packet_root,
        "source_inventory": packet_root / "source_inventory.json",
        "evidence_rows": packet_root / "evidence_rows.json",
        "mechanism_role_map": packet_root / "mechanism_role_map.json",
        "adapter_candidates": packet_root / "adapter_candidates.json",
        "evidence_gate": packet_root / "evidence_gate.json",
        "repeatability_check": packet_root / "repeatability_check.json",
        "runtime_parity_check": packet_root / "runtime_parity_check.json",
        "adapter_readiness": packet_root / "adapter_readiness.json",
        "onnx_readiness": packet_root / "onnx_readiness.json",
        "claim_boundary": packet_root / "claim_boundary.json",
        "work_packet": packet_root / "work_packet.yaml",
        "skill_receipts": packet_root / "skill_receipts.json",
        "closeout_gate": packet_root / "closeout_gate.json",
        "run_summary": packet_root / "run_summary.json",
        "packet_readme": packet_root / "README.md",
        "stage_brief": stage_root / "00_spec/stage_brief.md",
        "stage_open_draft": stage_root / "01_inputs/stage_open_draft.md",
        "review_packet": stage_root / "03_reviews/run27A_evidence_driven_adapter_role_map_packet.md",
        "review_index": stage_root / "03_reviews/review_index.md",
        "stage_ledger": stage_root / "03_reviews/stage_run_ledger.csv",
        "selection_status": stage_root / "04_selected/selection_status.md",
        "decision": root / "docs/decisions/2026-05-08_stage33_evidence_driven_adapter_role_map.md",
    }


def build_work_packet(inventory: Mapping[str, Any], role_map: Mapping[str, Any]) -> dict[str, Any]:
    required_gates = [
        "evidence_gate",
        "repeatability_check",
        "runtime_parity_check",
        "adapter_readiness_gate",
        "onnx_readiness_gate",
        "artifact_lineage_audit",
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "state_sync_audit",
        "code_surface_audit",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "version": "work_packet_schema_v2",
        "packet_id": PACKET_ID,
        "created_at_utc": "2026-05-08T00:00:00Z",
        "user_request": {
            "requested_action": "evidence-driven autonomous exploration-to-ONNX pipeline kickoff",
            "source": "active_goal",
        },
        "current_truth": {"active_stage_before": "32_sequence_model__tcn_temporal_convolution_context", "new_stage": STAGE_ID, "branch": git_branch()},
        "work_classification": {"primary_family": "experiment_execution", "lifecycle": "code_to_experiment_to_evidence_to_report"},
        "risk_vector_scan": {"required_gates": required_gates, "runtime_or_operating_claim": False},
        "decision_lock": {"status": "not_operating_decision", "baseline_or_promotion_change": False},
        "interpreted_scope": {
            "work_families": ["experiment_execution", "code_edit", "kpi_evidence", "artifact_lineage"],
            "target_surfaces": ["Stage10-32 evidence", "adapter contract candidates", "ONNX readiness decision"],
            "scope_units": ["evidence rows", "role map", "candidate contracts", "stage ledgers", "control packet"],
            "execution_layers": ["python_scan", "report_materialization", "control_plane_audits"],
            "mutation_policy": "repo_docs_and_small_python_helpers",
            "evidence_layers": ["registry", "alpha_ledger", "stage_docs", "agent_control_packets", "negative_memory"],
            "reduction_policy": "no model training, MT5 probe, or ONNX export until readiness gates pass",
            "claim_boundary": BOUNDARY,
        },
        "acceptance_criteria": [
            "Stage10-32 evidence scan is repeatable.",
            "Mechanism roles are derived without preselecting a model or feature.",
            "Adapter and ONNX readiness gates are explicit.",
            "No operating baseline, promotion, runtime authority, or live readiness is claimed.",
        ],
        "work_plan": ["scan evidence", "derive roles", "materialize candidates", "record gates", "run audits", "push main"],
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
            "skills_considered": [
                "obsidian-reentry-read",
                "obsidian-work-packet-router",
                "obsidian-code-surface-guard",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
                "obsidian-environment-reproducibility",
            ],
            "skills_selected": ["obsidian-run-evidence-system", "obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
            "skills_not_used": {
                "obsidian-backtest-forensics": "no MT5 tester result is produced in this packet",
                "obsidian-performance-attribution": "no trading KPI delta is claimed",
            },
            "required_skill_receipts": ["obsidian-run-evidence-system", "obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
            "required_gates": required_gates,
        },
        "evidence_contract": {"row_count": inventory.get("row_count"), "candidate_count": role_map.get("candidate_count"), "stage_range": [10, 32]},
        "gates": {"required": required_gates, "not_applicable_with_reason": {"kpi_contract_audit": "no trading KPI or promotion KPI claimed"}},
        "final_claim_policy": {"allowed": ["evidence_map_materialized"], "forbidden": list(gates_forbidden_claims())},
    }


def build_skill_receipts(inventory: Mapping[str, Any], role_map: Mapping[str, Any]) -> dict[str, Any]:
    common = {"packet_id": PACKET_ID, "status": "executed"}
    forbidden = list(gates_forbidden_claims())
    receipts = [
        {**common, "skill": "obsidian-run-evidence-system", "source_inputs": ["run_registry", "alpha_run_ledger", "stage_docs"], "produced_artifacts": ["mechanism_role_map.json", "adapter_candidates.json"], "ledger_rows": 4, "missing_evidence": ["no fixed runtime adapter"], "allowed_claims": ["evidence_scan"], "forbidden_claims": forbidden},
        {**common, "skill": "obsidian-experiment-design", "hypothesis": "Stage10-32 evidence can identify adapter roles before implementation.", "baseline": "no operating baseline", "changed_variables": ["classification surface only"], "invalid_conditions": ["source ledgers missing"], "evidence_plan": ["evidence_gate", "repeatability_check", "adapter_readiness"]},
        {**common, "skill": "obsidian-data-integrity", "data_sources_checked": inventory.get("source_counts", {}), "time_axis_boundary": "registry/doc evidence only; raw bar time axis not reinterpreted", "split_boundary": "split tokens read from prior evidence, no new split made", "leakage_checks": ["no new feature-label join"], "missing_data_boundary": "source docs can be incomplete; candidate claims stay bounded"},
        {**common, "skill": "obsidian-model-validation", "model_or_threshold_surface": "no new model or threshold selected", "validation_split": "not_applicable", "overfit_checks": ["no single split promotion"], "selection_metric_boundary": "evidence counts only", "allowed_claims": ["contract_candidate"], "forbidden_claims": forbidden},
        {**common, "skill": "obsidian-artifact-lineage", "source_inputs": [item["path"] for item in inventory.get("source_files", [])], "produced_artifacts": ["packet json", "stage docs", "ledger rows"], "raw_evidence": ["registry rows", "stage markdown"], "machine_readable": ["json", "csv", "yaml"], "human_readable": ["md"], "hashes_or_missing_reasons": inventory.get("source_files", []), "lineage_boundary": "connected_with_boundary"},
        {**common, "skill": "obsidian-runtime-parity", "python_artifact": "stage_pipelines/stage33/evidence_driven_role_map.py", "runtime_artifact": "not_created", "compared_surface": "not_applicable_no_runtime_artifact", "parity_level": "P0_unverified", "tester_identity": "not_applicable", "missing_evidence": ["MT5 handoff", "Python-vs-ONNX parity"], "allowed_claims": ["research_only"], "forbidden_claims": forbidden},
        {**common, "skill": "obsidian-result-judgment", "judgment_boundary": JUDGMENT, "allowed_claims": ["evidence_map_materialized"], "forbidden_claims": forbidden, "evidence_used": ["gates", "candidate_count"]},
    ]
    return {"packet_id": PACKET_ID, "candidate_count": role_map.get("candidate_count"), "receipts": receipts}


def write_ledgers(root: Path, paths: Mapping[str, Path], inventory: Mapping[str, Any], role_map: Mapping[str, Any]) -> dict[str, Any]:
    candidate_count = role_map.get("candidate_count", 0)
    rows = [
        _ledger_row("tier_a_separate", "Tier A", inventory, candidate_count, "Stage10-32 evidence scan; Tier A view is inherited prior evidence only."),
        _ledger_row("tier_b_separate", "Tier B", inventory, candidate_count, "Stage10-32 evidence scan; Tier B view is inherited prior evidence only."),
        _ledger_row("tier_ab_combined", "Tier A+B", inventory, candidate_count, "Combined evidence inventory, not synthetic trading performance."),
    ]
    stage_ledger = upsert_csv_rows(paths["stage_ledger"], ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    alpha_ledger = upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry = upsert_csv_rows(
        root / "docs/registers/run_registry.csv",
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "adapter_mechanism_evidence_scan",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": paths["review_packet"].as_posix(),
                "notes": f"candidates={candidate_count}; boundary={BOUNDARY}; onnx_ready=no",
            }
        ],
        key="run_id",
    )
    return {"stage_ledger": stage_ledger, "alpha_ledger": alpha_ledger, "run_registry": registry}


def _ledger_row(view: str, tier: str, inventory: Mapping[str, Any], candidate_count: int, notes: str) -> dict[str, str]:
    return {
        "ledger_row_id": f"{RUN_ID}__{view}",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": view,
        "parent_run_id": RUN_ID,
        "record_view": view,
        "tier_scope": tier,
        "kpi_scope": "evidence_inventory_adapter_contract",
        "scoreboard_lane": "structural_scout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": f"docs/agent_control/packets/{PACKET_ID}/run_summary.json",
        "primary_kpi": ledger_pairs((("candidate_count", candidate_count), ("evidence_rows", inventory.get("row_count")))),
        "guardrail_kpi": "no_trading_kpi_claimed;onnx_ready=no;runtime_probe=no",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": notes,
    }


def update_workspace_state(root: Path) -> None:
    path = root / "docs/workspace/workspace_state.yaml"
    focus_marker = "Stage33(33단계) evidence-driven adapter role map(근거 기반 어댑터 역할 지도)"
    focus_entry = (
        "- Stage33(33단계) evidence-driven adapter role map(근거 기반 어댑터 역할 지도)\n"
        "  opened(개방) as blocked/materialized evidence scan(차단/물질화 근거 스캔);\n"
        "  no baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비).\n"
    )
    text = path.read_text(encoding="utf-8-sig")
    replacements = {
        "updated_on: '2026-05-05'": "updated_on: '2026-05-08'",
        "active_stage: 32_sequence_model__tcn_temporal_convolution_context": f"active_stage: {STAGE_ID}",
        "current_run_id: run26D_torch_tcn_native_temporal_runtime_probe_v1": f"current_run_id: {RUN_ID}",
    }
    for before, after in replacements.items():
        text = text.replace(before, after, 1)
    if focus_marker not in text and "Stage33 evidence-driven adapter role map opened" not in text:
        text = text.replace("current_focus:\n", f"current_focus:\n{focus_entry}", 1)
    path.write_text(text, encoding="utf-8-sig")


def update_current_working_state(root: Path, inventory: Mapping[str, Any], role_map: Mapping[str, Any]) -> None:
    path = root / "docs/context/current_working_state.md"
    old = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    section = f"""## Latest Stage33 Evidence-Driven Adapter Role Map(최신 33단계 근거 기반 어댑터 역할 지도)

- active branch(활성 브랜치): `main(메인)`
- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- status(상태): `{STATUS}(차단)`
- adapter candidates(어댑터 후보): `{role_map.get("candidate_count")}`
- evidence rows(근거 행): `{inventory.get("row_count")}`

효과(effect, 효과): Stage10-32(10-32단계) 근거에서 역할(role, 역할)과 mechanism class(메커니즘 분류)를 도출했지만, fixed runtime input contract(고정 런타임 입력 계약)이 없어 ONNX(온닉스)나 MT5(`MetaTrader 5`, 메타트레이더5) 권위 주장은 하지 않는다.

"""
    if RUN_ID in old:
        return
    path.write_text(section + old, encoding="utf-8-sig")


def update_changelog(root: Path, role_map: Mapping[str, Any]) -> None:
    path = root / "docs/workspace/changelog.md"
    old = path.read_text(encoding="utf-8-sig") if path.exists() else "# Changelog\n"
    if RUN_ID in old:
        return
    entry = f"\n## 2026-05-08 Stage33 Evidence Adapter Map(33단계 근거 어댑터 지도)\n\n- Materialized(물질화) `{RUN_ID}` with `{role_map.get('candidate_count')}` adapter contract candidates(어댑터 계약 후보). No ONNX(온닉스), baseline(기준선), promotion(승격), or runtime authority(런타임 권위) claimed.\n"
    path.write_text(old.rstrip() + entry + "\n", encoding="utf-8-sig")


def build_closeout(root: Path, inventory: Mapping[str, Any], role_map: Mapping[str, Any], gates: Mapping[str, Any], ledgers: Mapping[str, Any]) -> dict[str, Any]:
    packet_root = stage_paths(root)["packet_root"]
    audits = _load_existing_audits(packet_root)
    blocking = any(audit.get("status") in {"blocked", "partial"} for audit in audits)
    return {
        "packet_id": PACKET_ID,
        "status": "blocked_by_audit_or_runtime_readiness" if blocking else "materialized_with_bounded_claims",
        "audits": audits,
        "gate_summaries": {name: payload.get("status") for name, payload in gates.items()},
        "ledger_updates": ledgers,
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "blocked" if blocking else "pass",
            "requested_claims": ["evidence_map_materialized", "reviewed", "completed"],
            "allowed_claims": ["evidence_map_materialized"] if not blocking else ["partial", "blocked"],
            "forbidden_claims": ["reviewed", "completed", *gates_forbidden_claims()],
        },
        "claim_boundary": gates["claim_boundary"],
        "next_action": "Pick one role candidate and run a bounded adapter probe after code-surface blocker is repaired or scoped.",
    }


def build_run_summary(paths: Mapping[str, Path], inventory: Mapping[str, Any], role_map: Mapping[str, Any], gates: Mapping[str, Any], ledgers: Mapping[str, Any], closeout: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "inventory": inventory,
        "candidate_count": role_map.get("candidate_count"),
        "candidate_ids": [item["candidate_id"] for item in role_map.get("adapter_candidates", [])],
        "gate_status": {name: payload.get("status") for name, payload in gates.items()},
        "onnx_artifacts_generated": False,
        "mt5_probe_executed": False,
        "model_training_executed": False,
        "ledgers": ledgers,
        "closeout_status": closeout.get("status"),
        "paths": {key: value.as_posix() for key, value in paths.items() if key not in {"stage_root", "packet_root"}},
        "claim_boundary": BOUNDARY,
    }


def stage_brief_md(inventory: Mapping[str, Any], role_map: Mapping[str, Any]) -> str:
    return f"""# Stage33 Adapter Mechanism Evidence-Driven Role Map(33단계 어댑터 메커니즘 근거 기반 역할 지도)

## Question(질문)

Stage10-32(10-32단계)의 evidence(근거)와 현재 repo(저장소) 상태만으로 어떤 adapter role(어댑터 역할)과 mechanism class(메커니즘 분류)를 먼저 물질화해야 하는가?

## Boundary(경계)

- evidence rows(근거 행): `{inventory.get("row_count")}`
- adapter candidates(어댑터 후보): `{role_map.get("candidate_count")}`
- claim boundary(주장 경계): `{BOUNDARY}`

효과(effect, 효과): 특정 model(모델), feature(피처), mechanism(메커니즘)을 미리 정하지 않고 다음 adapter probe(어댑터 탐침)의 후보 표면만 만든다.
"""


def stage_open_md(inventory: Mapping[str, Any], role_map: Mapping[str, Any]) -> str:
    return stage_brief_md(inventory, role_map)


def review_packet_md(inventory: Mapping[str, Any], role_map: Mapping[str, Any], gates: Mapping[str, Any]) -> str:
    candidates = "\n".join(f"- `{item['candidate_id']}`: {item['role']} / {item['mechanism_class']}" for item in role_map.get("adapter_candidates", []))
    return f"""# run27A Evidence-Driven Adapter Role Map(근거 기반 어댑터 역할 지도)

## Result(결과)

Materialized(물질화) `{role_map.get("candidate_count")}` adapter contract candidates(어댑터 계약 후보) from `{inventory.get("row_count")}` Stage10-32 evidence rows(근거 행).

{candidates}

## Gates(게이트)

- evidence gate(근거 게이트): `{gates['evidence_gate']['status']}`
- repeatability check(반복성 확인): `{gates['repeatability_check']['status']}`
- runtime parity check(런타임 동등성 확인): `{gates['runtime_parity_check']['status']}`
- adapter readiness(어댑터 준비도): `{gates['adapter_readiness']['status']}`
- ONNX readiness(온닉스 준비도): `{gates['onnx_readiness']['status']}`

## Claim Boundary(주장 경계)

No alpha quality(알파 품질), operating baseline(운영 기준선), promotion candidate(승격 후보), runtime authority(런타임 권위), or live readiness(실거래 준비)를 주장하지 않는다.
"""


def selection_status_md(role_map: Mapping[str, Any]) -> str:
    return f"""# Stage33 Selection Status(33단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- status(상태): `{STATUS}(차단)`
- current run(현재 실행): `{RUN_ID}`
- adapter candidates(어댑터 후보): `{role_map.get("candidate_count")}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- ONNX readiness(온닉스 준비도): `not_ready(준비 안 됨)`
- next action(다음 행동): `bounded_adapter_probe_after_input_contract_selection`
"""


def review_index_md() -> str:
    return f"""# Stage33 Review Index(33단계 검토 색인)

- `{RUN_ID}`: `03_reviews/run27A_evidence_driven_adapter_role_map_packet.md`
- packet(작업 묶음): `docs/agent_control/packets/{PACKET_ID}/`
"""


def decision_md(inventory: Mapping[str, Any], role_map: Mapping[str, Any], gates: Mapping[str, Any]) -> str:
    return review_packet_md(inventory, role_map, gates)


def packet_readme_md(inventory: Mapping[str, Any], role_map: Mapping[str, Any], gates: Mapping[str, Any]) -> str:
    return review_packet_md(inventory, role_map, gates)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8-sig")


def _load_existing_audits(packet_root: Path) -> list[dict[str, Any]]:
    names = [
        "work_packet_schema_lint.json",
        "skill_receipt_schema_lint.json",
        "state_sync_audit.json",
        "code_surface_audit.json",
        "code_surface_self_correction_plan.json",
        "required_gate_coverage_audit.json",
    ]
    audits: list[dict[str, Any]] = []
    for name in names:
        path = packet_root / name
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            audits.append({"audit_name": payload.get("audit_name", name.removesuffix(".json")), "status": payload.get("status"), "path": path.as_posix()})
    return audits


def gates_forbidden_claims() -> tuple[str, ...]:
    return ("alpha_quality", "operating_baseline", "promotion_candidate", "operating_promotion", "runtime_authority", "live_readiness")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_branch() -> str:
    try:
        return subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
    except Exception:
        return ""

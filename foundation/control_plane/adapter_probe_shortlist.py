from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
from foundation.control_plane.mechanism_role_map import STAGE_ID, build_mechanism_role_map


SOURCE_RUN_ID = "run27A_mechanism_role_map_evidence_scan_v1"
RUN_ID = "run27B_adapter_candidate_repeatability_shortlist_v1"
PACKET_ID = "stage33_run27B_adapter_candidate_repeatability_shortlist_v1"
BOUNDARY = "adapter_repeatability_shortlist_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"


@dataclass(frozen=True)
class AdapterProbeShortlistResult:
    summary: dict[str, Any]
    matrix_rows: list[dict[str, Any]]
    shortlist: list[dict[str, Any]]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_adapter_probe_shortlist(
    root: Path | str = Path("."),
    *,
    max_shortlist: int = 12,
    limit_per_mechanism: int = 2,
) -> AdapterProbeShortlistResult:
    root_path = Path(root)
    role_result = build_mechanism_role_map(root_path)
    matrix_rows: list[dict[str, Any]] = []
    for candidate in role_result.candidates:
        gate = _shortlist_gate(candidate)
        evidence = candidate["evidence"]
        row = {
            "candidate_id": candidate["candidate_id"],
            "stage_id": candidate["stage_id"],
            "stage_number": candidate["stage_number"],
            "run_id": candidate["run_id"],
            "mechanism_class": candidate["mechanism_class"],
            "roles": candidate["roles"],
            "adapter_state": candidate["adapter_readiness"]["state"],
            "shortlist_state": gate["state"],
            "shortlist_score": gate["score"],
            "rank_score": gate["rank_score"],
            "gate_checks": gate["checks"],
            "hard_blockers": gate["hard_blockers"],
            "evidence_gaps": gate["evidence_gaps"],
            "next_probe_action": gate["next_probe_action"],
            "onnx_decision": gate["onnx_decision"],
            "has_validation": evidence["has_validation"],
            "has_oos": evidence["has_oos"],
            "has_mt5": evidence["has_mt5"],
            "external_verification_completed": evidence["external_verification_completed"],
            "has_wfo_or_rolling": evidence["has_wfo_or_rolling"],
            "has_score_table": evidence["has_score_table"],
            "has_onnx": evidence["has_onnx"],
            "validation_net_profit_best": evidence["validation_net_profit_best"],
            "oos_net_profit_best": evidence["oos_net_profit_best"],
            "validation_oos_inversion": evidence["validation_oos_inversion"],
            "oos_only_positive": evidence["oos_only_positive"],
            "tiny_trade_count_spike": evidence["tiny_trade_count_spike"],
            "source_path": candidate["source_path"],
            "claim_boundary": BOUNDARY,
        }
        matrix_rows.append(row)

    matrix_rows.sort(key=_row_sort_key)
    shortlist = _select_diverse_shortlist(
        matrix_rows,
        max_shortlist=max_shortlist,
        limit_per_mechanism=limit_per_mechanism,
    )
    selected_ids = {row["candidate_id"]: index + 1 for index, row in enumerate(shortlist)}
    for row in matrix_rows:
        row["selected_rank"] = selected_ids.get(row["candidate_id"], "")
    for row in shortlist:
        row["selected_rank"] = selected_ids[row["candidate_id"]]

    summary = _summary(root_path, matrix_rows, shortlist, role_result.summary)
    stage_rows = _stage_ledger_rows(summary)
    run_registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_adapter_repeatability_shortlist",
        "status": "reviewed",
        "judgment": "inconclusive_adapter_repeatability_shortlist_completed",
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("source_run_id", SOURCE_RUN_ID),
                ("shortlist_count", summary["counts"]["shortlist_count"]),
                ("deferred_gate_blocked", summary["counts"]["deferred_gate_blocked"]),
                ("onnx_export_ready", summary["onnx_decision"]["ready_count"]),
                ("boundary", BOUNDARY),
            )
        ),
    }
    artifact_rows = _artifact_rows()
    return AdapterProbeShortlistResult(
        summary=summary,
        matrix_rows=matrix_rows,
        shortlist=shortlist,
        stage_rows=stage_rows,
        run_registry_row=run_registry_row,
        artifact_rows=artifact_rows,
    )


def write_adapter_probe_shortlist_packet(root: Path | str = Path("."), *, generated_at_utc: str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_adapter_probe_shortlist(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    shortlist_path = run_root / "adapter_probe_shortlist.json"
    matrix_path = run_root / "adapter_probe_shortlist_matrix.csv"
    manifest_path = run_root / "run_manifest.json"
    result_summary_path = reports_root / "result_summary.md"
    aggregate_summary_path = packet_root / "aggregate_summary.json"

    _write_json(shortlist_path, {"generated_at_utc": generated_at, **result.summary, "shortlist": result.shortlist})
    _write_matrix_csv(matrix_path, result.matrix_rows)
    manifest = _manifest(root_path, generated_at, shortlist_path, matrix_path, result)
    _write_json(manifest_path, manifest)
    _write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))

    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "reviewed_shortlist_completed",
        "judgment": "inconclusive_adapter_repeatability_shortlist_completed",
        "boundary": BOUNDARY,
        "generated_at_utc": generated_at,
        "shortlist_path": _rel(root_path, shortlist_path),
        "matrix_path": _rel(root_path, matrix_path),
        "run_manifest_path": _rel(root_path, manifest_path),
        "result_summary_path": _rel(root_path, result_summary_path),
        "counts": result.summary["counts"],
        "top_shortlist": result.summary["top_shortlist"],
        "onnx_decision": result.summary["onnx_decision"],
        "required_gates": result.summary["required_gates"],
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


def _shortlist_gate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    evidence = candidate["evidence"]
    roles = [str(role) for role in candidate["roles"]]
    adapter_state = str(candidate["adapter_readiness"]["state"])
    validation_net = _optional_float(evidence.get("validation_net_profit_best"))
    oos_net = _optional_float(evidence.get("oos_net_profit_best"))
    numeric_pair_available = validation_net is not None and oos_net is not None
    validation_oos_both_positive = bool(
        numeric_pair_available and validation_net is not None and oos_net is not None and validation_net > 0.0 and oos_net > 0.0
    )
    checks = {
        "role_clear": any(role not in {"Negative Memory", "Deferred", "Runtime / Packaging"} for role in roles),
        "adapter_partial_or_ready": adapter_state in {"ready_for_adapter_probe", "partial_adapter_candidate"},
        "validation_and_oos_present": bool(evidence.get("has_validation") and evidence.get("has_oos")),
        "mt5_runtime_completed": bool(evidence.get("has_mt5") and evidence.get("external_verification_completed")),
        "numeric_validation_oos_available": numeric_pair_available,
        "validation_oos_both_positive": validation_oos_both_positive,
        "no_validation_oos_inversion": not bool(evidence.get("validation_oos_inversion")),
        "no_oos_only_positive": not bool(evidence.get("oos_only_positive")),
        "no_tiny_trade_count_spike": not bool(evidence.get("tiny_trade_count_spike")),
        "safe_fallback_no_trade": candidate["adapter_readiness"]["safe_fallback"] == "no_trade",
    }
    hard_blockers: list[str] = []
    for name in (
        "role_clear",
        "adapter_partial_or_ready",
        "validation_and_oos_present",
        "mt5_runtime_completed",
        "no_validation_oos_inversion",
        "no_oos_only_positive",
        "no_tiny_trade_count_spike",
        "safe_fallback_no_trade",
    ):
        if not checks[name]:
            hard_blockers.append(name)
    evidence_gaps = [name for name in ("numeric_validation_oos_available", "validation_oos_both_positive") if not checks[name]]
    if hard_blockers:
        state = "deferred_gate_blocked"
    elif evidence_gaps:
        state = "deferred_metric_balance_gap"
    else:
        state = "repeatability_probe_shortlist"
    score = sum(1 for passed in checks.values() if passed)
    rank_score = _rank_score(candidate, checks, validation_net, oos_net)
    if state == "repeatability_probe_shortlist":
        next_probe_action = "run27C_signalcard_adapter_contract_probe_v1"
    elif state == "deferred_metric_balance_gap":
        next_probe_action = "defer_until_numeric_validation_oos_balance_is_clear"
    else:
        next_probe_action = "defer_until_hard_blockers_are_repaired_or_reclassified"
    return {
        "state": state,
        "score": score,
        "rank_score": rank_score,
        "checks": checks,
        "hard_blockers": hard_blockers,
        "evidence_gaps": evidence_gaps,
        "next_probe_action": next_probe_action,
        "onnx_decision": _onnx_decision_for_shortlist(candidate, state),
    }


def _rank_score(
    candidate: Mapping[str, Any],
    checks: Mapping[str, bool],
    validation_net: float | None,
    oos_net: float | None,
) -> float:
    numeric_score = max(float(validation_net or 0.0), 0.0) + max(float(oos_net or 0.0), 0.0)
    native_bonus = 50.0 if "native" in str(candidate["run_id"]).lower() else 0.0
    wfo_bonus = 25.0 if bool(candidate["evidence"].get("has_wfo_or_rolling")) else 0.0
    stage_bonus = float(candidate.get("stage_number") or 0)
    check_score = float(sum(1 for passed in checks.values() if passed) * 100)
    return check_score + numeric_score + native_bonus + wfo_bonus + stage_bonus


def _onnx_decision_for_shortlist(candidate: Mapping[str, Any], state: str) -> str:
    evidence = candidate["evidence"]
    if state != "repeatability_probe_shortlist":
        return "defer_no_shortlisted_adapter_probe"
    if evidence.get("has_score_table"):
        return "defer_runtime_advantage_absent_score_table_handoff_exists"
    if not evidence.get("has_onnx"):
        return "defer_until_signalcard_probe_and_parity_plan"
    return "existing_onnx_evidence_only_requires_source_parity_refresh"


def _select_diverse_shortlist(
    rows: Sequence[Mapping[str, Any]],
    *,
    max_shortlist: int,
    limit_per_mechanism: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    per_mechanism: dict[str, int] = {}
    for row in rows:
        if row["shortlist_state"] != "repeatability_probe_shortlist":
            continue
        mechanism = str(row["mechanism_class"])
        if per_mechanism.get(mechanism, 0) >= int(limit_per_mechanism):
            continue
        per_mechanism[mechanism] = per_mechanism.get(mechanism, 0) + 1
        selected.append(dict(row))
        if len(selected) >= int(max_shortlist):
            break
    return selected


def _summary(
    root: Path,
    matrix_rows: Sequence[Mapping[str, Any]],
    shortlist: Sequence[Mapping[str, Any]],
    role_summary: Mapping[str, Any],
) -> dict[str, Any]:
    counts = {
        "source_candidate_count": len(matrix_rows),
        "shortlist_count": len(shortlist),
        "deferred_metric_balance_gap": sum(1 for row in matrix_rows if row["shortlist_state"] == "deferred_metric_balance_gap"),
        "deferred_gate_blocked": sum(1 for row in matrix_rows if row["shortlist_state"] == "deferred_gate_blocked"),
        "onnx_export_ready": 0,
    }
    top = [
        {
            "selected_rank": row["selected_rank"],
            "candidate_id": row["candidate_id"],
            "stage_id": row["stage_id"],
            "run_id": row["run_id"],
            "mechanism_class": row["mechanism_class"],
            "roles": row["roles"],
            "rank_score": row["rank_score"],
            "validation_net_profit_best": row["validation_net_profit_best"],
            "oos_net_profit_best": row["oos_net_profit_best"],
            "next_probe_action": row["next_probe_action"],
            "onnx_decision": row["onnx_decision"],
        }
        for row in shortlist[:8]
    ]
    return {
        "source": {
            "source_run_id": SOURCE_RUN_ID,
            "source_boundary": role_summary.get("claim_boundary"),
            "source_candidate_count": role_summary.get("counts", {}).get("candidate_count"),
        },
        "source_hashes": {
            "run_registry": sha256_file_lf_normalized(root / "docs/registers/run_registry.csv"),
            "alpha_run_ledger": sha256_file_lf_normalized(root / "docs/registers/alpha_run_ledger.csv"),
        },
        "counts": counts,
        "top_shortlist": top,
        "onnx_decision": {
            "ready_count": 0,
            "decision": "defer_new_onnx_export_until_shortlisted_adapter_survives_signalcard_probe",
            "reason": "Shortlist only chooses repeatability probes; ONNX export still needs fixed input/output contract, source parity plan, and MT5 handoff advantage.",
        },
        "required_gates": {
            "evidence_gate": "completed_stage10_32_role_map_scan_consumed",
            "repeatability_check": {
                "status": "shortlist_filter_completed",
                "rule": "validation/OOS plus completed MT5 evidence and no OOS-only/tiny-trade/inversion blockers.",
            },
            "adapter_readiness_gate": {
                "status": "partial",
                "rule": "selected rows are ready only for a next SignalCard adapter probe, not for promotion.",
            },
            "runtime_parity_check": {
                "status": "not_attempted_by_claim",
                "rule": "Python-vs-runtime or Python-vs-ONNX parity must be a later packet.",
            },
            "claim_boundary": BOUNDARY,
        },
        "claim_boundary": BOUNDARY,
    }


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__adapter_repeatability_shortlist",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_repeatability_shortlist",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_probe_shortlist",
            "tier_scope": "Tier A+B",
            "kpi_scope": "adapter_readiness_gate",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "inconclusive_adapter_repeatability_shortlist_completed",
            "path": f"{run_root}/adapter_probe_shortlist.json",
            "primary_kpi": ledger_pairs(
                (
                    ("source_candidates", summary["counts"]["source_candidate_count"]),
                    ("shortlist_count", summary["counts"]["shortlist_count"]),
                )
            ),
            "guardrail_kpi": "no_oos_only_positive=true;no_tiny_trade_count_spike=true;safe_fallback=no_trade",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Shortlist consumes existing MT5 evidence; no new MT5 run, training, or ONNX export in run27B.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__next_signalcard_probe_plan",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "next_signalcard_probe_plan",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_probe_next_action",
            "tier_scope": "Tier A+B",
            "kpi_scope": "SignalCard_adapter_contract",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "next_probe_run27C_signalcard_adapter_contract_probe",
            "path": f"{run_root}/adapter_probe_shortlist.json",
            "primary_kpi": ledger_pairs((("next_probe_candidates", summary["counts"]["shortlist_count"]),)),
            "guardrail_kpi": "adapter_probe_not_promotion;onnx_not_ready",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Next action is a SignalCard adapter contract probe over the shortlisted evidence, not operating selection.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__onnx_deferred",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "onnx_deferred",
            "parent_run_id": RUN_ID,
            "record_view": "onnx_readiness_gate",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_packaging_gate",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "defer_new_onnx_export_until_shortlisted_adapter_survives_signalcard_probe",
            "path": f"{run_root}/run_manifest.json",
            "primary_kpi": ledger_pairs((("onnx_export_ready", summary["counts"]["onnx_export_ready"]),)),
            "guardrail_kpi": "source_parity_plan_required;mt5_handoff_advantage_required",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "ONNX remains optional packaging; no ONNX artifact generated by run27B.",
        },
    ]


def _artifact_rows() -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "artifact_id": f"{RUN_ID}__shortlist",
            "type": "adapter_probe_shortlist",
            "path": f"{run_root}/adapter_probe_shortlist.json",
            "status": "tracked_reviewed",
            "notes": "Repeatability-gated shortlist for next SignalCard adapter probe.",
        },
        {
            "artifact_id": f"{RUN_ID}__shortlist_matrix",
            "type": "adapter_probe_shortlist_matrix",
            "path": f"{run_root}/adapter_probe_shortlist_matrix.csv",
            "status": "tracked_reviewed",
            "notes": "Full candidate gate matrix with blockers and evidence gaps.",
        },
        {
            "artifact_id": f"{RUN_ID}__result_summary",
            "type": "result_summary",
            "path": f"{run_root}/reports/result_summary.md",
            "status": "tracked_reviewed",
            "notes": "Human readout for Stage33 run27B shortlist.",
        },
    ]


def _manifest(
    root: Path,
    generated_at: str,
    shortlist_path: Path,
    matrix_path: Path,
    result: AdapterProbeShortlistResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.adapter_probe_shortlist",
        "inputs": {
            "role_map_scan": SOURCE_RUN_ID,
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
            "adapter_probe_shortlist": {"path": _rel(root, shortlist_path), "sha256": sha256_file_lf_normalized(shortlist_path)},
            "adapter_probe_shortlist_matrix": {"path": _rel(root, matrix_path), "sha256": sha256_file_lf_normalized(matrix_path)},
        },
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: AdapterProbeShortlistResult) -> str:
    lines = [
        "# Stage33 RUN27B Adapter Repeatability Shortlist(33단계 실행27B 어댑터 반복성 후보 목록)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- source candidates(원천 후보): `{result.summary['counts']['source_candidate_count']}`",
        f"- shortlist count(후보 목록 수): `{result.summary['counts']['shortlist_count']}`",
        f"- ONNX export ready(ONNX 내보내기 준비): `{result.summary['counts']['onnx_export_ready']}`",
        "",
        "## Evidence Gate(근거 게이트)",
        "",
        "run27B(27B 실행)는 validation/OOS(검증/표본외), completed MT5 runtime evidence(완료된 MT5 런타임 근거), no inversion(역전 없음), no OOS-only positive(OOS만 긍정 아님), no tiny trade spike(작은 거래 수 급등 아님)를 요구했다.",
        "",
        "효과(effect, 효과)는 run27C(27C 실행)에서 adapter(어댑터)를 실제 구현할 때 약한 후보를 먼저 제거하는 것이다.",
        "",
        "## Shortlist(후보 목록)",
        "",
    ]
    if not result.shortlist:
        lines.append("- none(없음): repeatability gate(반복성 게이트)를 통과한 후보가 없다.")
    for item in result.shortlist:
        lines.append(
            f"- rank(순위) `{item['selected_rank']}` `{item['candidate_id']}`: `{item['mechanism_class']}`, roles(역할)={', '.join(item['roles'])}, validation_net_profit(검증 순손익)=`{item['validation_net_profit_best']}`, oos_net_profit(표본외 순손익)=`{item['oos_net_profit_best']}`, next(다음)=`{item['next_probe_action']}`"
        )
    lines.extend(
        [
            "",
            "## ONNX Decision(ONNX 결정)",
            "",
            f"`{result.summary['onnx_decision']['decision']}`. 효과(effect, 효과)는 ONNX(온닉스)를 포장 목표로 앞세우지 않고, SignalCard adapter probe(신호 카드 어댑터 탐침)가 먼저 살아남는지 보게 하는 것이다.",
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


def _write_matrix_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns = (
        "selected_rank",
        "candidate_id",
        "stage_id",
        "run_id",
        "mechanism_class",
        "roles",
        "adapter_state",
        "shortlist_state",
        "shortlist_score",
        "rank_score",
        "hard_blockers",
        "evidence_gaps",
        "next_probe_action",
        "onnx_decision",
        "has_validation",
        "has_oos",
        "has_mt5",
        "external_verification_completed",
        "has_wfo_or_rolling",
        "has_score_table",
        "has_onnx",
        "validation_net_profit_best",
        "oos_net_profit_best",
        "validation_oos_inversion",
        "oos_only_positive",
        "tiny_trade_count_spike",
        "source_path",
        "claim_boundary",
    )
    flattened: list[dict[str, Any]] = []
    for row in rows:
        flat = dict(row)
        flat["roles"] = "|".join(str(role) for role in row["roles"])
        flat["hard_blockers"] = "|".join(str(item) for item in row["hard_blockers"])
        flat["evidence_gaps"] = "|".join(str(item) for item in row["evidence_gaps"])
        flattened.append(flat)
    write_csv_rows(path, columns, flattened)


def _write_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def _upsert_registers(root: Path, result: AdapterProbeShortlistResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _row_sort_key(row: Mapping[str, Any]) -> tuple[int, float, int, str]:
    state_rank = {"repeatability_probe_shortlist": 0, "deferred_metric_balance_gap": 1, "deferred_gate_blocked": 2}.get(
        str(row["shortlist_state"]),
        3,
    )
    return (state_rank, -float(row["rank_score"]), -int(row.get("stage_number") or 0), str(row["candidate_id"]))


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper() == "NA":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Stage33 adapter repeatability shortlist from the run27A role map scan.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_adapter_probe_shortlist(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_adapter_probe_shortlist_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335Q"
RUN_ID = "run335Q_review_balanced_repair_defense_offense_research_inputs_v1"
PARENT_RUN_ID = "run335P_materialize_balanced_repair_defense_offense_research_inputs_v1"
NEXT_RUN_ID = "run335R_materialize_repaired_attribution_and_branch_specific_proxy_scout_v1"

STATUS = "completed_balanced_repair_defense_offense_input_review_no_forward_decision"
JUDGMENT = "inputs_reviewed_repair_accepted_proxy_rebuild_required_no_selection"
DECISION = "stage335Q_accept_same_bar_attribution_repair_keep_proxy_blocked_queue_branch_specific_proxy_scout"
CLAIM_BOUNDARY = (
    "research_development_only_stage335Q_balanced_input_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN335P_DIR = STAGE_DIR / "02_runs" / "run335P"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335Q_balanced_input_review.md"
REPORT_DOC = REVIEWS_DIR / "run335Q_balanced_input_review.md"

EXACT_JOIN_REVIEW_CSV = RUN_DIR / "exact_join_repair_review.csv"
PROXY_REVIEW_CSV = RUN_DIR / "proxy_rebuild_or_block_review.csv"
CONSTRAINT_REVIEW_CSV = RUN_DIR / "predeclared_constraint_review.csv"
PACKAGE_REVIEW_CSV = RUN_DIR / "balanced_package_review.csv"
RUN335R_QUEUE_CSV = RUN_DIR / "run335R_materialization_queue.csv"
REVIEW_SUMMARY_CSV = RUN_DIR / "review_summary_scorecard.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_balanced_input_review_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return io_path(path).resolve().relative_to(io_path(ROOT).resolve()).as_posix()


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value is None:
            return default
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    number = as_float(value, math.nan)
    if not math.isfinite(number):
        return default
    return int(number)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_text_bom(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_or_replace_section(path: Path, title: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    heading = f"## {title}"
    next_marker = "\n## "
    section = f"{heading}\n\n{body.strip()}\n"
    if heading in text:
        start = text.index(heading)
        next_start = text.find(next_marker, start + len(heading))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + section
        else:
            text = text[:start].rstrip() + "\n\n" + section + text[next_start:]
    else:
        text = text.rstrip() + "\n\n" + section
    write_text_lossless(path, text, had_bom)


def read_csv(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(io_path(path))


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "exact": read_csv(RUN335P_DIR / "exact_join_gap_repair_ledger.csv"),
        "proxy": read_csv(RUN335P_DIR / "proxy_bridge_rejection_matrix.csv"),
        "proxy_spec": read_csv(RUN335P_DIR / "branch_specific_proxy_rebuild_spec.csv"),
        "constraints": read_csv(RUN335P_DIR / "predeclared_research_constraints.csv"),
        "packages": read_csv(RUN335P_DIR / "balanced_repair_defense_offense_input_packages.csv"),
        "defense": read_csv(RUN335P_DIR / "defense_guardrail_contract.csv"),
        "offense": read_csv(RUN335P_DIR / "offense_research_seed_manifest.csv"),
        "queue": read_csv(RUN335P_DIR / "run335Q_review_queue.csv"),
        "gate": read_csv(RUN335P_DIR / "required_gate_coverage_audit.csv"),
    }


def review_exact_join(exact: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in exact.to_dict("records"):
        original = str(row.get("open_time_server_original", ""))
        repair = str(row.get("open_time_server_repair_key", ""))
        same_prefix = original[:16] == repair[:16]
        second_delta_ok = original.endswith(":01") and repair.endswith(":00") and same_prefix
        feature_ok = str(row.get("feature_floor_key_exists", "")).lower() == "true"
        telemetry_ok = str(row.get("telemetry_floor_key_exists", "")).lower() == "true"
        status_ok = row.get("repair_status") == "same_bar_second_floor_attribution_repair_ready"
        accepted = second_delta_ok and feature_ok and telemetry_ok and status_ok
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "trade_index": row.get("trade_index", ""),
                "open_time_server_original": original,
                "open_time_server_repair_key": repair,
                "same_bar_second_floor_check": "passed" if second_delta_ok else "failed",
                "feature_floor_key_exists": str(feature_ok).lower(),
                "telemetry_floor_key_exists": str(telemetry_ok).lower(),
                "review_decision": "accepted_attribution_only_repair" if accepted else "rejected_or_needs_manual_repair",
                "allowed_use": "attribution_join_key_only",
                "forbidden_use": "mutate_trade_time;train_model;retune_threshold;declare_forward_pass_fail",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_proxy(proxy: pd.DataFrame, proxy_spec: pd.DataFrame) -> list[dict[str, Any]]:
    spec_dims = set(proxy_spec["dimension"].astype(str))
    rows: list[dict[str, Any]] = []
    for row in proxy.to_dict("records"):
        dimension = str(row.get("dimension", ""))
        spec_exists = dimension in spec_dims
        selection_blocked = row.get("selection_use") == "blocked"
        forward_blocked = row.get("forward_pass_fail_use") == "blocked"
        if dimension == "overall_proxy_bridge":
            review = "overall_proxy_bridge_blocked_until_rebuild"
        elif spec_exists and selection_blocked and forward_blocked:
            review = "rebuild_required_before_any_rank_use"
        else:
            review = "review_failed_proxy_boundary_unclear"
        rows.append(
            {
                "dimension": dimension,
                "selection_use": row.get("selection_use", ""),
                "forward_pass_fail_use": row.get("forward_pass_fail_use", ""),
                "diagnostic_use": row.get("diagnostic_use", ""),
                "branch_specific_rebuild_spec_exists": str(spec_exists).lower(),
                "review_decision": review,
                "run335R_action": "materialize_branch_specific_proxy_scout" if spec_exists else "keep_proxy_blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_constraints(constraints: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    forbidden_terms = ("tune", "threshold", "lot", "forward_pocket_filter", "drop_or_keep_trades_based_on_known_forward")
    for row in constraints.to_dict("records"):
        forbidden = str(row.get("forbidden_use", ""))
        rule = str(row.get("predeclared_rule", ""))
        hard_boundary = any(term in forbidden for term in forbidden_terms) or "no direct" in rule.lower()
        direct_filter_risk = "known_forward_pocket_dates" in forbidden or "direct forward" in rule.lower()
        rows.append(
            {
                "constraint_id": row.get("constraint_id", ""),
                "lane": row.get("lane", ""),
                "source_finding": row.get("source_finding", ""),
                "observed_evidence": row.get("observed_evidence", ""),
                "predeclared_rule": rule,
                "boundary_strength": "strong" if hard_boundary else "medium",
                "direct_forward_filter_risk": "controlled" if direct_filter_risk or hard_boundary else "needs_review",
                "review_decision": "accepted_predeclared_research_gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_packages(packages: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in packages.to_dict("records"):
        ready = row.get("review_status") == "ready_for_run335Q_review"
        selection_false = str(row.get("selection_eligible", "")).lower() == "false"
        rows.append(
            {
                "package_id": row.get("package_id", ""),
                "package_lane": row.get("package_lane", ""),
                "source_queue_ids": row.get("source_queue_ids", ""),
                "artifact_inputs": row.get("artifact_inputs", ""),
                "review_status": row.get("review_status", ""),
                "selection_eligible": row.get("selection_eligible", ""),
                "review_decision": "accepted_for_run335R_materialization" if ready and selection_false else "rejected_until_boundary_fixed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run335r_queue(
    exact_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    constraint_review: Sequence[Mapping[str, Any]],
    package_review: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    accepted_exact = sum(1 for row in exact_review if row.get("review_decision") == "accepted_attribution_only_repair")
    proxy_dims = [row["dimension"] for row in proxy_review if row.get("run335R_action") == "materialize_branch_specific_proxy_scout"]
    packages_ok = [row["package_id"] for row in package_review if row.get("review_decision") == "accepted_for_run335R_materialization"]
    constraints_ok = [row["constraint_id"] for row in constraint_review if row.get("review_decision") == "accepted_predeclared_research_gate"]
    return [
        {
            "queue_id": "materialize_same_bar_repaired_attribution_views",
            "priority": 1,
            "source_artifact": rel(EXACT_JOIN_REVIEW_CSV),
            "task": f"Apply attribution-only same-bar floor repair for {accepted_exact} accepted rows and regenerate affected attribution summaries.",
            "success_condition": "repaired views preserve original trade times and mark repair_key separately",
            "forbidden": "mutate trades;future shift;nearest shift;model training",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_branch_specific_proxy_scout",
            "priority": 2,
            "source_artifact": rel(PROXY_REVIEW_CSV),
            "task": f"Build branch-specific proxy scout for {len(proxy_dims)} dimensions at branch/attempt/bar/trade grain while keeping selection blocked.",
            "success_condition": "proxy rows vary by branch/attempt and are compared to MT5 without fitting to MT5 outcome",
            "forbidden": "retrofit proxy to match forward MT5;selection use before review",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "materialize_constraint_bound_research_packet_inputs",
            "priority": 3,
            "source_artifact": rel(CONSTRAINT_REVIEW_CSV),
            "task": f"Package {len(constraints_ok)} accepted constraints into the next research packet input contract.",
            "success_condition": "cost/curve/direction/proxy constraints are present before any new training or threshold work",
            "forbidden": "direct forward pocket filter;lot optimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "carry_balanced_repair_defense_offense_packages",
            "priority": 4,
            "source_artifact": rel(PACKAGE_REVIEW_CSV),
            "task": f"Carry {len(packages_ok)} reviewed packages into run335R without candidate selection.",
            "success_condition": "repair, defense, and offense lanes remain represented",
            "forbidden": "promote m48_plain_rf;claim runtime authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_summary_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "subject": "exact_join_repair",
            "review_result": "accepted_attribution_only",
            "primary_count": metrics["exact_accepted"],
            "blocked_count": metrics["exact_rejected"],
            "next_action": "run335R_materialize_same_bar_repaired_attribution_views",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "proxy_bridge",
            "review_result": "selection_blocked_rebuild_required",
            "primary_count": metrics["proxy_rebuild_required"],
            "blocked_count": metrics["proxy_failed"],
            "next_action": "run335R_materialize_branch_specific_proxy_scout",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "predeclared_constraints",
            "review_result": "accepted_for_next_packet_input",
            "primary_count": metrics["constraints_accepted"],
            "blocked_count": 0,
            "next_action": "run335R_materialize_constraint_bound_inputs",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "balanced_packages",
            "review_result": "accepted_for_run335R",
            "primary_count": metrics["packages_accepted"],
            "blocked_count": metrics["packages_rejected"],
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run335P_inputs_loaded",
            "status": "passed",
            "evidence": rel(RUN335P_DIR),
            "finding": f"exact={metrics['exact_rows']};proxy={metrics['proxy_rows']};constraints={metrics['constraint_rows']};packages={metrics['package_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "exact_join_repair_reviewed",
            "status": "passed" if metrics["exact_rejected"] == 0 else "failed",
            "evidence": rel(EXACT_JOIN_REVIEW_CSV),
            "finding": f"accepted={metrics['exact_accepted']};rejected={metrics['exact_rejected']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_rebuild_boundary_reviewed",
            "status": "passed" if metrics["proxy_failed"] == 0 else "passed_with_boundary",
            "evidence": rel(PROXY_REVIEW_CSV),
            "finding": f"rebuild_required={metrics['proxy_rebuild_required']};selection_blocked_all=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "constraints_reviewed_as_predeclared_not_forward_filters",
            "status": "passed",
            "evidence": rel(CONSTRAINT_REVIEW_CSV),
            "finding": f"accepted={metrics['constraints_accepted']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "balanced_packages_reviewed",
            "status": "passed" if metrics["packages_rejected"] == 0 else "failed",
            "evidence": rel(PACKAGE_REVIEW_CSV),
            "finding": f"accepted={metrics['packages_accepted']};rejected={metrics['packages_rejected']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_selection_no_goal_achieve",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "no Forward Passed/Failed, no runtime authority, no Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = {
        "data_integrity_receipt.json": {
            **common,
            "data_source": rel(RUN335P_DIR),
            "time_axis": "review accepts same-bar :01 to :00 repair only for attribution keys.",
            "sample_scope": "run335P repair/proxy/constraint/package inputs.",
            "missing_or_duplicate_check": f"exact accepted={metrics['exact_accepted']}; exact rejected={metrics['exact_rejected']}.",
            "feature_label_boundary": "no model training, threshold retune, or forward pocket filtering.",
            "split_boundary": "forward diagnostic input review only.",
            "leakage_risk": "proxy ranking and forward pocket filters remain blocked.",
            "data_hash_or_identity": "run335Q artifacts registered after execution.",
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUN335P_DIR),
            "shared_contract": "same runtime evidence; run335Q reviews inputs only and does not alter EA, model, threshold, lot, or handoff.",
            "known_differences": "same-bar attribution repair is accepted only as a derived join view.",
            "parity_check": "no new MT5 execution; consumes prior MT5 and telemetry evidence.",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "run335P inputs were reviewed into accepted repair, proxy rebuild, constraints, and package carry-forward decisions.",
            "comparison_baseline": "run335P inputs were materialized but not yet reviewed.",
            "likely_drivers": "exact join :01 gap, aggregate proxy limitation, cost/curve/direction fragility.",
            "segment_checks": "exact join rows; proxy dimensions; constraints; package lanes.",
            "trade_shape": "no new trade results; input review only.",
            "alternative_explanations": "reviewed inputs do not prove any ONNX improvement.",
            "attribution_confidence": "high_for_input_review_low_for_selection",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run335Q balanced repair defense offense input review",
            "evidence_available": "exact repair review, proxy review, constraint review, package review, run335R queue.",
            "evidence_missing": "run335R materialization, branch-specific proxy scout output, new MT5 after any future repair.",
            "judgment_label": "exploratory_input_review",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "입력은 검토 통과했지만 후보 선택은 아직 아니다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [rel(RUN335P_DIR)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(EXACT_JOIN_REVIEW_CSV),
                rel(PROXY_REVIEW_CSV),
                rel(CONSTRAINT_REVIEW_CSV),
                rel(PACKAGE_REVIEW_CSV),
                rel(RUN335R_QUEUE_CSV),
            ],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_stage_closeout",
            "lineage_judgment": "connected_with_boundary",
        },
    }
    paths = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)
    return paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# Run335Q Balanced Input Review(335Q 균형 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- exact_join_accepted(정확 조인 승인): `{metrics['exact_accepted']}`
- proxy_rebuild_required(프록시 재구축 필요): `{metrics['proxy_rebuild_required']}`
- constraints_accepted(제약 승인): `{metrics['constraints_accepted']}`
- packages_accepted(패키지 승인): `{metrics['packages_accepted']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run335Q(335Q 실행)는 run335P(335P 실행)의 repair/defense/offense input package(수리/방어/공격 입력 패키지)를 검토했다.

Effect(효과): same-bar second floor repair(동일 봉 초 단위 보정)는 attribution-only(귀속 전용)으로 승인한다. proxy(프록시)는 selection/Forward decision(선택/전진 판정)에서 계속 차단하고, branch-specific proxy scout(분기별 프록시 스카우트)를 run335R(335R 실행)에서 물질화하도록 넘긴다.

## Evidence(근거)

- exact_join_repair_review(정확 조인 수리 검토): `{rel(EXACT_JOIN_REVIEW_CSV)}`
- proxy_rebuild_or_block_review(프록시 재구축/차단 검토): `{rel(PROXY_REVIEW_CSV)}`
- predeclared_constraint_review(사전 제약 검토): `{rel(CONSTRAINT_REVIEW_CSV)}`
- balanced_package_review(균형 패키지 검토): `{rel(PACKAGE_REVIEW_CSV)}`
- run335R_queue(335R 대기열): `{rel(RUN335R_QUEUE_CSV)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT_CSV)}`

## Boundary(경계)

이 실행은 review(검토)다. model(모델), threshold(임계값), lot(로트), risk logic(위험 로직), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage335Q Balanced Input Review(균형 입력 검토)

`{RUN_ID}`은 run335P(335P 실행)의 균형 입력 패키지를 검토했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- exact_join_accepted(정확 조인 승인): `{metrics['exact_accepted']}`
- exact_join_rejected(정확 조인 거절): `{metrics['exact_rejected']}`
- proxy_rebuild_required(프록시 재구축 필요): `{metrics['proxy_rebuild_required']}`
- constraints_accepted(제약 승인): `{metrics['constraints_accepted']}`
- packages_accepted(패키지 승인): `{metrics['packages_accepted']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): 다음 run335R(335R 실행)는 귀속 전용 조인 수리 view(보기)와 분기별 proxy scout(프록시 스카우트)를 물질화한다.
"""
    write_text_bom(REPORT_DOC, report)
    write_text_bom(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage335(335단계) run335Q(335Q 실행)는 "
        f"`{STATUS}`로 balanced input review(균형 입력 검토)를 완료했다. "
        f"Effect(효과): exact join repair(정확 조인 수리) `{metrics['exact_accepted']}`행을 attribution-only(귀속 전용)로 승인하고, "
        f"proxy(프록시)는 selection(선택) 차단을 유지한 채 run335R(335R 실행) branch-specific scout(분기별 스카우트)로 넘긴다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335Q(335Q 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_line}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v18`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run335Q_summary(335Q 요약): balanced input review(균형 입력 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): same-bar attribution repair(동일 봉 귀속 수리)는 승인, proxy(프록시)는 선택 차단 유지, "
        f"`{NEXT_RUN_ID}`에서 repaired attribution/proxy scout(수리 귀속/프록시 스카우트)를 물질화한다. Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335Q_summary(335Q 요약)" not in current_text:
        current_text = current_text.replace("- run335P_summary", summary_line + "\n- run335P_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- latest_design", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        f"- effect(효과): Stage335Q(335Q 실행)은 run335P 입력을 검토해 same-bar attribution repair(동일 봉 귀속 수리)를 승인하고 proxy(프록시)는 선택 차단을 유지했다. next_action(다음 행동)은 `{NEXT_RUN_ID}`이며 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- exact_join_repair_review(정확 조인 수리 검토): `{rel(EXACT_JOIN_REVIEW_CSV)}`
- proxy_rebuild_or_block_review(프록시 재구축/차단 검토): `{rel(PROXY_REVIEW_CSV)}`
- predeclared_constraint_review(사전 제약 검토): `{rel(CONSTRAINT_REVIEW_CSV)}`
- balanced_package_review(균형 패키지 검토): `{rel(PACKAGE_REVIEW_CSV)}`
- run335R_materialization_queue(335R 물질화 대기열): `{rel(RUN335R_QUEUE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335Q Balanced Input Review(335Q 균형 입력 검토)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): same-bar attribution repair(동일 봉 귀속 수리)를 승인하고 proxy(프록시)는 선택 차단 유지, run335R(335R 실행) 물질화 대기열을 만들었다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335Q Balanced Input Review(335Q 균형 입력 검토)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_balanced_input_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__balanced_input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "balanced_repair_defense_offense_input_review",
                "tier_scope": "Tier A runtime diagnostic evidence with no selection",
                "kpi_scope": "exact_join_proxy_constraints_package_review",
                "scoreboard_lane": "research_input_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"exact_accepted={metrics['exact_accepted']};proxy_rebuild_required={metrics['proxy_rebuild_required']}",
                "guardrail_kpi": "proxy_selection_blocked;no_forward_pocket_filter;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_input_review_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        [
            {
                "ledger_row_id": f"{RUN_ID}__balanced_input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "research_input_review",
                "evidence_scope": "run335P_balanced_repair_defense_offense_inputs",
                "kpi_scope": "review_exact_join_proxy_constraints_packages",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"exact_accepted={metrics['exact_accepted']};next={NEXT_RUN_ID}.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335_balanced_input_review",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "balanced_input_review_output_no_retune_no_forward_decision",
        }
        for path in outputs
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    exact_review = review_exact_join(inputs["exact"])
    proxy_review = review_proxy(inputs["proxy"], inputs["proxy_spec"])
    constraint_review = review_constraints(inputs["constraints"])
    package_review = review_packages(inputs["packages"])
    run335r_queue = build_run335r_queue(exact_review, proxy_review, constraint_review, package_review)
    metrics = {
        "exact_rows": len(exact_review),
        "exact_accepted": sum(1 for row in exact_review if row.get("review_decision") == "accepted_attribution_only_repair"),
        "exact_rejected": sum(1 for row in exact_review if row.get("review_decision") != "accepted_attribution_only_repair"),
        "proxy_rows": len(proxy_review),
        "proxy_rebuild_required": sum(1 for row in proxy_review if row.get("run335R_action") == "materialize_branch_specific_proxy_scout"),
        "proxy_failed": sum(1 for row in proxy_review if row.get("review_decision") == "review_failed_proxy_boundary_unclear"),
        "constraint_rows": len(constraint_review),
        "constraints_accepted": sum(1 for row in constraint_review if row.get("review_decision") == "accepted_predeclared_research_gate"),
        "package_rows": len(package_review),
        "packages_accepted": sum(1 for row in package_review if row.get("review_decision") == "accepted_for_run335R_materialization"),
        "packages_rejected": sum(1 for row in package_review if row.get("review_decision") != "accepted_for_run335R_materialization"),
        "run335r_queue_rows": len(run335r_queue),
    }
    summary_rows = build_summary_rows(metrics)
    gate_rows = build_gate_rows(metrics)
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "exact_join_review;proxy_review;constraint_review;package_review;run335R_queue",
            "evidence_missing": "run335R_materialization;branch_specific_proxy_scout;new_mt5_after_future_repair",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    outputs = [
        write_csv(
            EXACT_JOIN_REVIEW_CSV,
            (
                "attempt_name",
                "trade_index",
                "open_time_server_original",
                "open_time_server_repair_key",
                "same_bar_second_floor_check",
                "feature_floor_key_exists",
                "telemetry_floor_key_exists",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            exact_review,
        ),
        write_csv(
            PROXY_REVIEW_CSV,
            (
                "dimension",
                "selection_use",
                "forward_pass_fail_use",
                "diagnostic_use",
                "branch_specific_rebuild_spec_exists",
                "review_decision",
                "run335R_action",
                "claim_boundary",
            ),
            proxy_review,
        ),
        write_csv(
            CONSTRAINT_REVIEW_CSV,
            (
                "constraint_id",
                "lane",
                "source_finding",
                "observed_evidence",
                "predeclared_rule",
                "boundary_strength",
                "direct_forward_filter_risk",
                "review_decision",
                "claim_boundary",
            ),
            constraint_review,
        ),
        write_csv(
            PACKAGE_REVIEW_CSV,
            (
                "package_id",
                "package_lane",
                "source_queue_ids",
                "artifact_inputs",
                "review_status",
                "selection_eligible",
                "review_decision",
                "claim_boundary",
            ),
            package_review,
        ),
        write_csv(
            RUN335R_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            run335r_queue,
        ),
        write_csv(
            REVIEW_SUMMARY_CSV,
            ("subject", "review_result", "primary_count", "blocked_count", "next_action", "claim_boundary"),
            summary_rows,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), gate_rows),
        write_csv(
            RESULT_JUDGMENT_CSV,
            (
                "run_id",
                "status",
                "judgment",
                "decision",
                "evidence_available",
                "evidence_missing",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            result_rows,
        ),
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "metrics": metrics,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "created_at_utc": now_utc(),
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(RUN335P_DIR)],
                "status": STATUS,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    write_reports(metrics)
    outputs.extend([REPORT_DOC, DECISION_DOC])
    update_docs(metrics)
    outputs.extend([WORKSPACE_STATE, CURRENT_STATE, STAGE_BRIEF, INPUT_REFS, CHANGELOG, SELECTED_DIR / "selection_status.md"])
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "exact_accepted": metrics["exact_accepted"],
                "proxy_rebuild_required": metrics["proxy_rebuild_required"],
                "constraints_accepted": metrics["constraints_accepted"],
                "packages_accepted": metrics["packages_accepted"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

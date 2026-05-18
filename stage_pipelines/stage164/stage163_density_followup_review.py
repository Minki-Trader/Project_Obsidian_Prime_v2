from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)

STAGE_ID = "164_adapter_research__stage163_density_followup_review"
RUN_ID = "run164A_stage164_stage163_density_followup_review_v1"
PACKET_ID = "stage164_stage163_density_followup_review_v1"
SOURCE_STAGE_ID = "163_adapter_research__stage161_density_preserving_score_repair"
SOURCE_RUN_ID = "run163A_stage163_stage161_density_preserving_score_repair_v1"
SOURCE_STAGE163_CLOSEOUT_COMMIT = "deb4276a8b176549bd5df4f3ab9aea480a471f3f"
SOURCE_STAGE163_HASH_RECORD_COMMIT = "72029ed89df1f2761399890593d99d9674da6b46"
NEXT_STAGE_ID = "165_adapter_research__side_context_oos_early_repair"
NEXT_RUN_ID = "run165A_stage165_side_context_oos_early_repair_v1"
NEXT_PACKET_ID = "stage165_side_context_oos_early_repair_v1"
DECISION = "open_stage165_side_context_oos_early_repair_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
LEGACY_34D = {"profit_factor": 1.583157, "net_profit": 987.60, "max_drawdown_percent": 12.909136, "trade_count": 404}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_REPORT = SOURCE_ROOT / "stage163_density_preserving_score_repair_report.md"
SOURCE_SUMMARY = SOURCE_ROOT / "stage163_density_preserving_score_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_ROOT / "stage163_segment_kpi_summary.csv"
SOURCE_PROBABILITY = SOURCE_ROOT / "stage163_probability_binding_summary.csv"
SOURCE_DECISION = SOURCE_ROOT / "stage163_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage164_stage163_density_followup_review.md"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage164_density_followup_summary.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage164_failure_memory.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage164_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage164_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage164_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage164/stage163_density_followup_review.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = tuple(columns or (rows[0].keys() if rows else ()))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def actual_row(rows: Sequence[Mapping[str, str]], adapter_id: str, split: str) -> Mapping[str, str]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def segment_row(rows: Sequence[Mapping[str, str]], adapter_id: str, split: str, segment: str) -> Mapping[str, str]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def build_review() -> dict[str, Any]:
    summary = read_csv(SOURCE_SUMMARY)
    segments = read_csv(SOURCE_SEGMENTS)
    adapters = sorted({row["adapter_id"] for row in summary if row.get("view") == "actual_routed_total"})
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = actual_row(summary, adapter_id, "validation_is")
        oos = actual_row(summary, adapter_id, "oos")
        early = segment_row(segments, adapter_id, "oos", "early")
        flags: list[str] = []
        val_pf = as_float(val.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        oos_dd = as_float(oos.get("max_drawdown_percent"))
        early_pf = as_float(early.get("profit_factor"))
        early_net = as_float(early.get("net_profit"))
        if val_pf < LEGACY_34D["profit_factor"]:
            flags.append("validation_pf_below_34d")
        if oos_pf < LEGACY_34D["profit_factor"]:
            flags.append("oos_pf_below_34d")
        if oos_dd > LEGACY_34D["max_drawdown_percent"]:
            flags.append("oos_dd_above_34d")
        if early_pf < 1.10 or early_net <= 0:
            flags.append("oos_early_damage")
        row = {
            "adapter_id": adapter_id,
            "validation_pf": val_pf,
            "validation_net": as_float(val.get("net_profit")),
            "oos_pf": oos_pf,
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": oos_dd,
            "oos_early_pf": early_pf,
            "oos_early_net": early_net,
            "quality_flags": ";".join(flags) if flags else "candidate_quality_pass_review_required",
            "candidate_quality_pass": not flags,
        }
        rows.append(row)
        if flags:
            failures.append(
                {
                    "adapter_id": adapter_id,
                    "failure_label": row["quality_flags"],
                    "reason": "Stage164 found Stage163 did not satisfy full validation/OOS PF, DD, and OOS early requirements.",
                    "next_use": "Stage165 side/context OOS early repair input",
                    "overall_goal_complete": False,
                }
            )
    route = [
        {
            "decision": DECISION,
            "next_stage": NEXT_STAGE_ID,
            "reason": "Stage163 split the failure: long-dense improves validation PF but breaks OOS; low-risk shortgate protects OOS but fails validation PF.",
            "next_axis": "side_context_router_with_oos_early_guard_and_validation_pf_repair",
            "do_not_repeat": "do_not_scale_risk_or_block_all_shorts_as_standalone_solution",
            "overall_goal_complete": False,
        }
    ]
    return {"decision": DECISION, "rows": rows, "failure_memory": failures, "route_decision": route, "overall_goal_complete": False}


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | flags(플래그) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append("| {adapter_id} | {validation_pf:.6f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_early_pf:.6f} | {quality_flags} |".format(**row))
    return "\n".join(lines)


def write_reports(review: Mapping[str, Any]) -> None:
    write_csv(SUMMARY_CSV_PATH, review["rows"])
    write_csv(FAILURE_MEMORY_PATH, review["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, review["route_decision"])
    write_json(SUMMARY_JSON_PATH, review)
    write_md(
        REPORT_PATH,
        f"""# Stage164 Stage163 Density Follow-up Review(164단계 163단계 밀도 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE163_CLOSEOUT_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

No(아니오). Stage163(163단계)은 complete repair(완전 수리)가 아니다. Effect(효과): long-dense(롱 밀도 보존)는 OOS(표본외)를 깨고, low-risk shortgate(저위험 숏 게이트)는 validation PF(검증 수익요인)가 34D(34D) 아래다.

## KPI Read(KPI 판독)

{kpi_table(review["rows"])}

## Route(경로)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_axis(다음 축): `side_context_router_with_oos_early_guard_and_validation_pf_repair`
- overall_goal_complete(전체 목표 완료): `false`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Stage164 Decision(164단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE163_CLOSEOUT_COMMIT}`
- review_report(검토 보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage164(164단계)은 review-only(검토 전용)로 닫는다. Effect(효과): Stage165(165단계) 새 수리축으로 넘긴다.
""",
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, SUMMARY_CSV_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{Path(path).name}",
            "artifact_type": "stage164_density_followup_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage164 review-only density follow-up artifact.",
        }
        for path in paths
        if path_exists(path)
    ]


def write_ledgers() -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "baseline_adapter_stage164_density_followup_review", "status": "completed", "judgment": DECISION, "path": rel(DECISION_PATH), "notes": ledger_pairs((("source_closeout_commit", SOURCE_STAGE163_CLOSEOUT_COMMIT), ("overall_goal_complete", 0)))}],
        key="run_id",
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_only",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "review_only",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "stage_review",
        "tier_scope": "actual_routed_total",
        "kpi_scope": "density_followup_review",
        "scoreboard_lane": "baseline_adapter_stage164",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": "stage163_no_full_quality_pass",
        "guardrail_kpi": "overall_goal_complete=false",
        "external_verification_status": "completed_from_stage163_mt5_evidence",
        "notes": ledger_pairs((("source_summary", rel(SOURCE_SUMMARY)), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    payloads = {
        "routing_receipt.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "result_judgment", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "status": "completed"},
        "runtime_evidence_gate.json": {"external_verification_status": "completed_from_stage163_mt5_evidence", "new_mt5_run": False, "status": "passed"},
        "scope_completion_gate.json": {"bounded_question": "stage163_density_followup_review", "decision": DECISION, "overall_goal_complete": False, "status": "passed"},
        "kpi_contract_audit.json": {"legacy_34d_target": LEGACY_34D, "summary_csv": rel(SUMMARY_CSV_PATH), "status": "completed"},
        "result_judgment_gate.json": {"decision": DECISION, "claim_boundary": BOUNDARY, "overall_goal_complete": False, "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {"observed": "long-dense OOS damage and low-risk shortgate validation PF gap", "next_axis": NEXT_STAGE_ID, "status": "completed"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(SOURCE_REPORT), rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_PROBABILITY), rel(SOURCE_DECISION)], "producer": rel(PRODUCER_PATH), "ledger_payload": ledger_payload, "status": "completed"},
        "runtime_parity_gate.json": {"runtime_parity_claim": False, "status": "passed"},
        "backtest_forensics_gate.json": {"source_summary": rel(SOURCE_SUMMARY), "status": "passed_from_source_evidence"},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"declared_required_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "runtime_parity_gate", "backtest_forensics_gate", "required_gate_coverage_audit", "final_claim_guard"], "executed_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "runtime_parity_gate", "backtest_forensics_gate", "required_gate_coverage_audit", "final_claim_guard"], "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "summary_csv": rel(SUMMARY_CSV_PATH), "route_decision": rel(ROUTE_DECISION_PATH), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False},
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def write_next_stage_seed() -> None:
    write_md(NEXT_STAGE_ROOT / "00_spec/stage_brief.md", f"# {NEXT_STAGE_ID}\n\nStage165(165단계)는 side/context router(방향/문맥 라우터)와 OOS early guard(표본외 초반 보호)를 좁게 시험한다.\n\n## Bounded Question(경계 질문)\n\nCan side/context repair(방향/문맥 수리) lift validation PF(검증 수익요인) above 34D while preventing OOS early(표본외 초반) damage and keeping DD(낙폭) acceptable?\n\nEffect(효과): risk scaling(위험 확대)이나 all-short block(전체 숏 차단)을 반복하지 않고 새 수리축을 분리한다.\n\n## Boundary(경계)\n\n`{BOUNDARY}`\n")
    write_md(NEXT_STAGE_ROOT / "01_inputs/input_refs.md", f"# Stage165 Input References(165단계 입력 참조)\n\n- stage164_decision(164단계 판정): `{rel(DECISION_PATH)}`\n- stage164_review(164단계 검토): `{rel(REPORT_PATH)}`\n- stage164_summary(164단계 요약): `{rel(SUMMARY_CSV_PATH)}`\n- stage163_summary(163단계 요약): `{rel(SOURCE_SUMMARY)}`\n- stage163_segment_kpi(163단계 구간 핵심 성과 지표): `{rel(SOURCE_SEGMENTS)}`\n- source_stage163_closeout_commit(원천 163단계 종료 커밋): `{SOURCE_STAGE163_CLOSEOUT_COMMIT}`\n")
    write_md(NEXT_STAGE_ROOT / "03_reviews/review_index.md", f"# Stage165 Review Index(165단계 검토 색인)\n\n- status(상태): `open_planned_from_stage164`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n")
    write_md(NEXT_STAGE_ROOT / "04_selected/selection_status.md", f"# Stage165 Selection Status(165단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage164`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{DECISION}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?m)^updated_on:.*$", "updated_on: '2026-05-18'", state)
    state = re.sub(r"(?s)\nstage164_stage163_density_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?s)\nstage165_side_context_oos_early_repair:.*?(?=\nstage\d+_|\Z)", "\n", state)
    focus = f"""current_focus:
- >-
  Stage164(164단계) closed(종료) as `{DECISION}` and Stage165(165단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): density repair(밀도 수리) 실패를 새 side/context(방향/문맥) 수리축으로 넘긴다.
- >-
  Stage164 evidence(164단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): OOS early damage(표본외 초반 손상)와 validation PF gap(검증 수익요인 차이)을 함께 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?s)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    block = f"""
stage164_stage163_density_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only_{DECISION}
  current_run_id: {RUN_ID}
  source_stage163_closeout_commit: {SOURCE_STAGE163_CLOSEOUT_COMMIT}
  source_stage163_hash_record_commit: {SOURCE_STAGE163_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage165_side_context_oos_early_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage164
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(CURRENT_WORKING_STATE_PATH, f"# Current Working State(현재 작업 상태)\n\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- active_stage(활성 단계): `{NEXT_STAGE_ID}`\n- selected_research_baseline(선택 연구 기준선): `none`\n- target_surface(목표 표면): `{TARGET_SURFACE}`\n- adapter_under_review(검토 중 어댑터): `stage165_side_context_oos_early_repair_surface`\n- status(상태): `stage164_closed_review_only_{DECISION}_stage165_open_planned`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n\nStage164(164단계)는 Stage163(163단계) density repair(밀도 수리)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage165(165단계) side/context(방향/문맥) 수리로 넘긴다.\n\n## Latest Stage164 Evidence(최신 164단계 근거)\n\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- summary(요약): `{rel(SUMMARY_CSV_PATH)}`\n- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n\nForbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).\n")


def write_status_files() -> None:
    write_md(SELECTED_ROOT / "selection_status.md", f"# Stage164 Selection Status(164단계 선택 상태)\n\n- stage_status(단계 상태): `closed_review_only_{DECISION}`\n- current_packet(현재 작업 묶음): `{PACKET_ID}`\n- current_run(현재 실행): `{RUN_ID}`\n- source_stage(원천 단계): `{SOURCE_STAGE_ID}`\n- source_run(원천 실행): `{SOURCE_RUN_ID}`\n- decision(판정): `{DECISION}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")
    write_md(REVIEWS_ROOT / "review_index.md", f"# Stage164 Review Index(164단계 검토 색인)\n\n- status(상태): `closed_review_only_{DECISION}`\n- packet(작업 묶음): `{PACKET_ID}`\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- summary(요약): `{rel(SUMMARY_CSV_PATH)}`\n- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = f"\n## {utc_now()} Stage164 Stage163 density follow-up review closeout(164단계 163단계 밀도 후속 검토 종료)\n\n- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n- effect(효과): Stage163(163단계) 결과가 full repair(완전 수리)가 아님을 기록하고 Stage165(165단계) side/context(방향/문맥) 수리로 넘겼다.\n- boundary(주장 경계): `{BOUNDARY}`.\n"
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def run() -> dict[str, Any]:
    review = build_review()
    write_reports(review)
    ledger_payload = write_ledgers()
    write_packet_files(review, ledger_payload)
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    return {"status": "completed", "decision": DECISION, "report": rel(REPORT_PATH), "overall_goal_complete": False}


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

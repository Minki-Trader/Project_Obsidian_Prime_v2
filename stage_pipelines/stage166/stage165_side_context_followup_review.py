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

STAGE_ID = "166_adapter_research__stage165_side_context_followup_review"
RUN_NUMBER = "run166A"
RUN_ID = "run166A_stage166_stage165_side_context_followup_review_v1"
PACKET_ID = "stage166_stage165_side_context_followup_review_v1"
SOURCE_STAGE_ID = "165_adapter_research__side_context_oos_early_repair"
SOURCE_RUN_ID = "run165A_stage165_side_context_oos_early_repair_v1"
SOURCE_STAGE165_CLOSEOUT_COMMIT = "8419d954cbdc2d8652da395a7bc7d9b11a02eb12"
SOURCE_STAGE165_HASH_RECORD_COMMIT = "7dbbcb7c54619c5813523b1b5503414f17eb24b7"
NEXT_STAGE_ID = "167_adapter_research__validation_pf_lift_density_preservation"
NEXT_RUN_ID = "run167A_stage167_validation_pf_lift_density_preservation_v1"
NEXT_PACKET_ID = "stage167_validation_pf_lift_density_preservation_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "open_stage167_validation_pf_lift_density_preservation_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage165_completed"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY_JSON = Path("stages/165_adapter_research__side_context_oos_early_repair/03_reviews/stage165_side_context_oos_early_repair_summary.json")
SOURCE_SUMMARY_CSV = Path("stages/165_adapter_research__side_context_oos_early_repair/03_reviews/stage165_side_context_oos_early_repair_summary.csv")
SOURCE_SEGMENT_CSV = Path("stages/165_adapter_research__side_context_oos_early_repair/03_reviews/stage165_segment_kpi_summary.csv")
SOURCE_REPORT = Path("stages/165_adapter_research__side_context_oos_early_repair/03_reviews/stage165_side_context_oos_early_repair_report.md")

REPORT_PATH = REVIEWS_ROOT / "stage166_stage165_side_context_followup_review.md"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage166_stage165_quality_matrix.csv"
ROUTE_CSV_PATH = REVIEWS_ROOT / "stage166_repair_route_summary.csv"
ROUTE_JSON_PATH = REVIEWS_ROOT / "stage166_repair_route_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage166_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage166/stage165_side_context_followup_review.py")
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def load_stage165() -> Mapping[str, Any]:
    return json.loads(io_path(SOURCE_SUMMARY_JSON).read_text(encoding="utf-8-sig"))


def review_rows(stage165: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in stage165.get("quality_rows", []):
        adapter_id = str(row.get("adapter_id", ""))
        flags = str(row.get("quality_flags", ""))
        if adapter_id.startswith("s165_long_cashopen_guard"):
            judgment = "pf_shape_clue_but_overfiltered"
            route_role = "secondary_density_restoration_clue"
            route_reason = "PF(수익요인), DD(낙폭), OOS early(표본외 초반)는 좋지만 net/trade density(순손익/거래 밀도)가 너무 얇다."
        elif adapter_id.startswith("s165_shortgate_long_lowedge"):
            judgment = "best_repair_anchor_but_validation_pf_failed"
            route_role = "primary_stage167_repair_anchor"
            route_reason = "OOS(표본외), DD(낙폭), density(밀도)는 가장 좋고 validation PF(검증 수익요인)만 34D 아래라 수리 여지가 가장 크다."
        else:
            judgment = "oos_good_validation_failed_not_primary"
            route_role = "negative_mixed_router_memory"
            route_reason = "OOS early(표본외 초반)는 좋지만 validation PF(검증 수익요인)와 OOS mid(표본외 중반)가 약해 주축으로 두지 않는다."
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_dd_percent": row.get("oos_dd_percent", ""),
                "oos_early_pf": row.get("oos_early_pf", ""),
                "oos_early_net": row.get("oos_early_net", ""),
                "oos_trade_count": row.get("oos_trade_count", ""),
                "quality_flags": flags,
                "review_judgment": judgment,
                "route_role": route_role,
                "route_reason": route_reason,
            }
        )
    return rows


def route_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in rows if row["route_role"] == "primary_stage167_repair_anchor")
    secondary = next(row for row in rows if row["route_role"] == "secondary_density_restoration_clue")
    rejected = next(row for row in rows if row["route_role"] == "negative_mixed_router_memory")
    return [
        {
            "run_id": RUN_ID,
            "route_rank": 1,
            "route": "stage167_primary_shortgate_validation_pf_lift",
            "adapter_id": primary["adapter_id"],
            "bounded_question": "Can validation PF(검증 수익요인) be lifted above 34D while preserving OOS PF/net/DD/OOS early(표본외 수익요인/순손익/낙폭/초반)?",
            "why": primary["route_reason"],
            "do_not_do": "Do not increase risk(위험) as the main repair and do not claim final package(최종 패키지).",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 2,
            "route": "secondary_overfilter_density_restore_clue",
            "adapter_id": secondary["adapter_id"],
            "bounded_question": "Can the long cash-open guard(롱 현금장 초반 보호) keep PF(수익요인) while restoring density(밀도)?",
            "why": secondary["route_reason"],
            "do_not_do": "Do not accept high PF(수익요인) if net/trade density(순손익/거래 밀도) stays too thin.",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 3,
            "route": "preserve_negative_memory_mixed_router",
            "adapter_id": rejected["adapter_id"],
            "bounded_question": "Keep mixed router(혼합 라우터) as failure memory(실패 기억), not a primary anchor(주 앵커).",
            "why": rejected["route_reason"],
            "do_not_do": "Do not cherry-pick(유리한 구간만 선택) OOS early(표본외 초반).",
        },
    ]


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | role(역할) | val PF(검증 수익요인) | val net(검증 순손익) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | judgment(판정) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {route_role} | {validation_pf} | {validation_net} | {oos_pf} | {oos_net} | {oos_dd_percent} | {oos_early_pf} | {review_judgment} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], routes: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage166 Stage165 Side/Context Follow-up Review(166단계 165단계 방향/문맥 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE165_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE165_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage165(165단계) find a v2-native side/context path(v2 고유 방향/문맥 경로) that genuinely improves validation/OOS KPI(검증/표본외 핵심 성과 지표), or should the work route to another bounded repair(경계 수리)?

## KPI Read(KPI 판독)

{kpi_table(rows)}

## Route Decision(경로 판정)

1. primary(주): `{routes[0]["route"]}` from `{routes[0]["adapter_id"]}`.
2. secondary(보조): `{routes[1]["route"]}` from `{routes[1]["adapter_id"]}`.
3. failure_memory(실패 기억): `{routes[2]["route"]}` from `{routes[2]["adapter_id"]}`.

Effect(효과): Stage167(167단계)은 shortgate low-edge(숏게이트 낮은 엣지) 축의 validation PF(검증 수익요인)를 올리되, OOS PF/net/DD/OOS early(표본외 수익요인/순손익/낙폭/초반)를 훼손하지 않는 좁은 수리로 열린다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage166 Decision(166단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage165_closeout_commit(원천 165단계 종료 커밋): `{SOURCE_STAGE165_CLOSEOUT_COMMIT}`
- source_stage165_hash_record_commit(원천 165단계 해시 기록 커밋): `{SOURCE_STAGE165_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage166(166단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        QUALITY_MATRIX_PATH,
        ROUTE_CSV_PATH,
        ROUTE_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        SOURCE_REPORT,
        SOURCE_SUMMARY_JSON,
        SOURCE_SUMMARY_CSV,
        SOURCE_SEGMENT_CSV,
    ]
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage166_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage166 review-only evidence; no deployment or live-readiness claim.",
                }
            )
    return rows


def write_ledgers(artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage166_stage165_side_context_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage165_closeout_commit", SOURCE_STAGE165_CLOSEOUT_COMMIT),
                        ("source_stage165_hash_record_commit", SOURCE_STAGE165_HASH_RECORD_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only_no_inheritance"),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__review_only",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "review_only",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "stage166_review_only",
            "tier_scope": "Stage165 MT5 evidence",
            "kpi_scope": "stage165_side_context_followup_review",
            "scoreboard_lane": "research_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": "source_stage165_quality_matrix_reviewed",
            "guardrail_kpi": "no_final_adapter_no_deployment_no_live_readiness",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage166 reviewed Stage165 MT5 evidence and opened Stage167 bounded repair.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(ledger_payload: Mapping[str, Any], rows: Sequence[Mapping[str, Any]], routes: Sequence[Mapping[str, Any]]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "report_path": rel(REPORT_PATH),
        "quality_matrix": rel(QUALITY_MATRIX_PATH),
        "route_summary": rel(ROUTE_CSV_PATH),
        "ledger_payload": ledger_payload,
        "quality_rows": list(rows),
        "route_rows": list(routes),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage166 Closeout Packet(166단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage166(166단계) review-only(검토 전용) 결과를 장부와 packet(작업 묶음)에 연결해 Stage167(167단계) 수리 질문을 좁힌다.
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage167(167단계)는 validation PF lift with density preservation(검증 수익요인 상승과 밀도 보존)만 좁게 시험한다.

## Bounded Question(경계 질문)

Can the Stage165(165단계) shortgate low-edge route(숏게이트 낮은 엣지 경로) lift validation PF(검증 수익요인) above legacy 34D(레거시 34D) while preserving OOS PF/net/DD/OOS early(표본외 수익요인/순손익/낙폭/초반) and avoiding thin density(얇은 밀도)?

Effect(효과): OOS(표본외)가 좋은 축을 버리지 않고, 부족한 validation PF(검증 수익요인)만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage167 Inputs(167단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_stage165_closeout_commit(원천 165단계 종료 커밋): `{SOURCE_STAGE165_CLOSEOUT_COMMIT}`
- source_stage165_hash_record_commit(원천 165단계 해시 기록 커밋): `{SOURCE_STAGE165_HASH_RECORD_COMMIT}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- source_stage165_summary(원천 165단계 요약): `{rel(SOURCE_SUMMARY_CSV)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage167 Review Index(167단계 검토 색인)

- status(상태): `open_planned_from_stage166`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage167 Selection Status(167단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage166`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage166(166단계) closed(종료) as `{DECISION}` and Stage167(167단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage165(165단계) 결과에서 가장 수리 가치가 큰 shortgate low-edge(숏게이트 낮은 엣지) 축으로 좁힌다.
- >-
  Stage166 evidence(166단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(ROUTE_CSV_PATH)}`에 있다. Effect(효과): high PF but thin density(높은 수익요인이나 얇은 밀도)와 dense OOS but weak validation PF(밀도 있는 표본외이나 약한 검증 수익요인)를 분리해서 판독한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage166_stage165_side_context_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage166_stage165_side_context_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage165_closeout_commit: {SOURCE_STAGE165_CLOSEOUT_COMMIT}
  source_stage165_hash_record_commit: {SOURCE_STAGE165_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  route_summary_path: {rel(ROUTE_CSV_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage167_validation_pf_lift_density_preservation_surface`
- status(상태): `stage166_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage166(166단계)는 Stage165(165단계) side/context repair(방향/문맥 수리)를 review-only(검토 전용)로 판독했다. Effect(효과): Stage167(167단계)은 validation PF lift(검증 수익요인 상승)와 density preservation(밀도 보존)만 좁게 시험한다.

## Latest Stage166 Evidence(최신 166단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage166 Selection Status(166단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage166(166단계)는 review-only(검토 전용) 질문만 닫고, 전체 목표 완료를 주장하지 않는다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage166 Review Index(166단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage166 Stage165 side/context follow-up review closeout(166단계 165단계 방향/문맥 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage167(167단계)을 validation PF lift with density preservation(검증 수익요인 상승과 밀도 보존) 수리로 열었다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    stage165 = load_stage165()
    rows = review_rows(stage165)
    routes = route_rows(rows)
    write_csv(QUALITY_MATRIX_PATH, rows)
    write_csv(ROUTE_CSV_PATH, routes)
    write_json(
        ROUTE_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "quality_rows": rows,
            "route_rows": routes,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_md(REPORT_PATH, report_markdown(rows, routes))
    write_md(DECISION_PATH, decision_markdown())
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(artifacts)
    write_packet_files(ledger_payload, rows, routes)
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "report_path": rel(REPORT_PATH),
                    "next_stage": NEXT_STAGE_ID,
                    "overall_goal_complete": False,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

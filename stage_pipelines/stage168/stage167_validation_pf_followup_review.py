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

STAGE_ID = "168_adapter_research__stage167_validation_pf_followup_review"
RUN_NUMBER = "run168A"
RUN_ID = "run168A_stage168_stage167_validation_pf_followup_review_v1"
PACKET_ID = "stage168_stage167_validation_pf_followup_review_v1"
SOURCE_STAGE_ID = "167_adapter_research__validation_pf_lift_density_preservation"
SOURCE_RUN_ID = "run167A_stage167_validation_pf_lift_density_preservation_v1"
SOURCE_STAGE167_CLOSEOUT_COMMIT = "e5df224ca4405b0cfc7aa0ada5474f31368afd54"
SOURCE_STAGE167_HASH_RECORD_COMMIT = "2fdf365d4aa74cfed16f71bdd0d353882d16e9c6"
NEXT_STAGE_ID = "169_adapter_research__net_density_lift_pf_preservation"
NEXT_RUN_ID = "run169A_stage169_net_density_lift_pf_preservation_v1"
NEXT_PACKET_ID = "stage169_net_density_lift_pf_preservation_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "open_stage169_net_density_lift_pf_preservation_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage167_completed"

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

SOURCE_SUMMARY_JSON = Path("stages/167_adapter_research__validation_pf_lift_density_preservation/03_reviews/stage167_validation_pf_lift_density_preservation_summary.json")
SOURCE_SUMMARY_CSV = Path("stages/167_adapter_research__validation_pf_lift_density_preservation/03_reviews/stage167_validation_pf_lift_density_preservation_summary.csv")
SOURCE_SEGMENT_CSV = Path("stages/167_adapter_research__validation_pf_lift_density_preservation/03_reviews/stage167_segment_kpi_summary.csv")
SOURCE_REPORT = Path("stages/167_adapter_research__validation_pf_lift_density_preservation/03_reviews/stage167_validation_pf_lift_density_preservation_report.md")

REPORT_PATH = REVIEWS_ROOT / "stage168_stage167_validation_pf_followup_review.md"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage168_stage167_quality_matrix.csv"
ROUTE_CSV_PATH = REVIEWS_ROOT / "stage168_repair_route_summary.csv"
ROUTE_JSON_PATH = REVIEWS_ROOT / "stage168_repair_route_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage168_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage168/stage167_validation_pf_followup_review.py")
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


def load_stage167() -> Mapping[str, Any]:
    return json.loads(io_path(SOURCE_SUMMARY_JSON).read_text(encoding="utf-8-sig"))


def review_rows(stage167: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in stage167.get("quality_rows", []):
        adapter_id = str(row.get("adapter_id", ""))
        if adapter_id.startswith("s167_short_pre_guard"):
            judgment = "primary_pf_pass_density_preserved_net_still_below_34d"
            route_role = "primary_stage169_net_density_lift_anchor"
            route_reason = "PF(수익요인), OOS(표본외), DD(낙폭), density(밀도)가 균형 있게 개선됐지만 net(순손익)은 34D보다 낮다."
        elif adapter_id.startswith("s167_short_wide_lowedge"):
            judgment = "secondary_pf_pass_lower_net_density"
            route_role = "secondary_guard_strength_clue"
            route_reason = "PF(수익요인)는 통과했지만 short_pre_guard(숏 사전구간 보호)보다 net/density(순손익/밀도)가 낮다."
        else:
            judgment = "failure_memory_pf_failed_overfiltered"
            route_role = "negative_overfilter_memory"
            route_reason = "OOS(표본외)는 좋지만 validation PF(검증 수익요인)와 validation net(검증 순손익)이 무너져 주축으로 두지 않는다."
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_trade_count": row.get("validation_trade_count", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_dd_percent": row.get("oos_dd_percent", ""),
                "oos_trade_count": row.get("oos_trade_count", ""),
                "oos_early_pf": row.get("oos_early_pf", ""),
                "quality_flags": row.get("quality_flags", ""),
                "review_judgment": judgment,
                "route_role": route_role,
                "route_reason": route_reason,
            }
        )
    return rows


def route_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in rows if row["route_role"] == "primary_stage169_net_density_lift_anchor")
    secondary = next(row for row in rows if row["route_role"] == "secondary_guard_strength_clue")
    negative = next(row for row in rows if row["route_role"] == "negative_overfilter_memory")
    return [
        {
            "run_id": RUN_ID,
            "route_rank": 1,
            "route": "stage169_primary_short_pre_guard_net_density_lift",
            "adapter_id": primary["adapter_id"],
            "bounded_question": "Can net/density(순손익/밀도) move closer to 34D while preserving PF/DD/OOS early(수익요인/낙폭/표본외 초반)?",
            "why": primary["route_reason"],
            "do_not_do": "Do not call this final(최종) and do not make risk scaling(위험 확대) the only explanation.",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 2,
            "route": "secondary_wide_guard_conservative_backup",
            "adapter_id": secondary["adapter_id"],
            "bounded_question": "Use as backup(대체) if Stage169 density repair damages PF(수익요인).",
            "why": secondary["route_reason"],
            "do_not_do": "Do not prefer it over primary while net/density(순손익/밀도) is lower.",
        },
        {
            "run_id": RUN_ID,
            "route_rank": 3,
            "route": "preserve_cash45_overfilter_failure_memory",
            "adapter_id": negative["adapter_id"],
            "bounded_question": "Keep as failure memory(실패 기억), not a repair anchor(수리 앵커).",
            "why": negative["route_reason"],
            "do_not_do": "Do not cherry-pick(유리한 구간만 선택) high OOS PF(높은 표본외 수익요인).",
        },
    ]


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | role(역할) | val PF(검증 수익요인) | val net(검증 순손익) | val trades(검증 거래) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | judgment(판정) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {route_role} | {validation_pf} | {validation_net} | {validation_trade_count} | {oos_pf} | {oos_net} | {oos_dd_percent} | {review_judgment} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], routes: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage168 Stage167 Validation PF Follow-up Review(168단계 167단계 검증 수익요인 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE167_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE167_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage167(167단계) produce a v2-native repair(v2 고유 수리) that lifts validation PF(검증 수익요인) above 34D while preserving OOS and density(표본외와 밀도)?

## KPI Read(KPI 판독)

{kpi_table(rows)}

## Route Decision(경로 판정)

1. primary(주): `{routes[0]["route"]}` from `{routes[0]["adapter_id"]}`.
2. secondary(보조): `{routes[1]["route"]}` from `{routes[1]["adapter_id"]}`.
3. failure_memory(실패 기억): `{routes[2]["route"]}` from `{routes[2]["adapter_id"]}`.

Effect(효과): Stage169(169단계)은 `short_pre_guard(숏 사전구간 보호)`를 중심으로 net/density lift(순손익/밀도 상승)를 시험하되, PF/DD/OOS early(수익요인/낙폭/표본외 초반)를 훼손하지 않는 경계로 열린다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage168 Decision(168단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage167_closeout_commit(원천 167단계 종료 커밋): `{SOURCE_STAGE167_CLOSEOUT_COMMIT}`
- source_stage167_hash_record_commit(원천 167단계 해시 기록 커밋): `{SOURCE_STAGE167_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage168(168단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
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
                    "artifact_type": "stage168_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage168 review-only evidence; no deployment or live-readiness claim.",
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
                "lane": "baseline_adapter_stage168_stage167_validation_pf_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage167_closeout_commit", SOURCE_STAGE167_CLOSEOUT_COMMIT),
                        ("source_stage167_hash_record_commit", SOURCE_STAGE167_HASH_RECORD_COMMIT),
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
            "record_view": "stage168_review_only",
            "tier_scope": "Stage167 MT5 evidence",
            "kpi_scope": "stage167_validation_pf_followup_review",
            "scoreboard_lane": "research_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": "source_stage167_quality_matrix_reviewed",
            "guardrail_kpi": "no_final_adapter_no_deployment_no_live_readiness",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage168 reviewed Stage167 MT5 evidence and opened Stage169 bounded repair.",
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
        f"""# Stage168 Closeout Packet(168단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage168(168단계) review-only(검토 전용) 결과를 장부와 packet(작업 묶음)에 연결해 Stage169(169단계) 수리 질문을 좁힌다.
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage169(169단계)는 net/density lift with PF preservation(순손익/밀도 상승과 수익요인 보존)만 좁게 시험한다.

## Bounded Question(경계 질문)

Can the Stage167(167단계) `short_pre_guard(숏 사전구간 보호)` route move net/density(순손익/밀도) closer to legacy 34D(레거시 34D) while preserving validation/OOS PF(검증/표본외 수익요인), DD(낙폭), and OOS early behavior(표본외 초반 행동)?

Effect(효과): PF(수익요인)를 얻은 축을 최종으로 부르지 않고, 아직 낮은 net/density(순손익/밀도)를 다음 경계에서 확인한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage169 Inputs(169단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_stage167_closeout_commit(원천 167단계 종료 커밋): `{SOURCE_STAGE167_CLOSEOUT_COMMIT}`
- source_stage167_hash_record_commit(원천 167단계 해시 기록 커밋): `{SOURCE_STAGE167_HASH_RECORD_COMMIT}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- route_summary(경로 요약): `{rel(ROUTE_CSV_PATH)}`
- source_stage167_summary(원천 167단계 요약): `{rel(SOURCE_SUMMARY_CSV)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage169 Review Index(169단계 검토 색인)

- status(상태): `open_planned_from_stage168`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage169 Selection Status(169단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage168`
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
  Stage168(168단계) closed(종료) as `{DECISION}` and Stage169(169단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage167(167단계)의 PF(수익요인) 통과 축을 net/density lift(순손익/밀도 상승) 수리로 좁힌다.
- >-
  Stage168 evidence(168단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(ROUTE_CSV_PATH)}`에 있다. Effect(효과): PF pass(수익요인 통과)를 최종으로 착각하지 않고, net/density(순손익/밀도) 부족을 다음 질문으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage168_stage167_validation_pf_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage168_stage167_validation_pf_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage167_closeout_commit: {SOURCE_STAGE167_CLOSEOUT_COMMIT}
  source_stage167_hash_record_commit: {SOURCE_STAGE167_HASH_RECORD_COMMIT}
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
- adapter_under_review(검토 중 어댑터): `stage169_net_density_lift_pf_preservation_surface`
- status(상태): `stage168_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage168(168단계)는 Stage167(167단계) validation PF lift(검증 수익요인 상승)를 review-only(검토 전용)로 판독했다. Effect(효과): Stage169(169단계)은 net/density lift(순손익/밀도 상승)와 PF preservation(수익요인 보존)만 좁게 시험한다.

## Latest Stage168 Evidence(최신 168단계 근거)

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
        f"""# Stage168 Selection Status(168단계 선택 상태)

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

Effect(효과): Stage168(168단계)는 review-only(검토 전용) 질문만 닫고, 전체 목표 완료를 주장하지 않는다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage168 Review Index(168단계 검토 색인)

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
        f"\n## {utc_now()} Stage168 Stage167 validation PF follow-up review closeout(168단계 167단계 검증 수익요인 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage169(169단계)을 net/density lift with PF preservation(순손익/밀도 상승과 수익요인 보존) 수리로 열었다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    stage167 = load_stage167()
    rows = review_rows(stage167)
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

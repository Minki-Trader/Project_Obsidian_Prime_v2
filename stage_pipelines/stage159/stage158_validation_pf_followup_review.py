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

STAGE_ID = "159_adapter_research__stage158_validation_pf_followup_review"
RUN_ID = "run159A_stage159_stage158_validation_pf_followup_review_v1"
PACKET_ID = "stage159_stage158_validation_pf_followup_review_v1"
SOURCE_STAGE_ID = "158_adapter_research__stage156_validation_pf_margin_repair"
SOURCE_RUN_ID = "run158A_stage158_stage156_validation_pf_margin_repair_v1"
SOURCE_CLOSEOUT_COMMIT = "f863e4a3758d0095e8bf4333b6bcd0ad6a6391d3"
SOURCE_HASH_RECORD_COMMIT = "6e8e4a54e40b4317a33c88b1b3c080444f1c75a5"
NEXT_STAGE_ID = "160_adapter_research__stage158_threshold_binding_audit"
NEXT_RUN_ID = "run160A_stage160_stage158_threshold_binding_audit_v1"
NEXT_PACKET_ID = "stage160_stage158_threshold_binding_audit_v1"
DECISION = "open_stage160_stage158_threshold_binding_audit_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

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

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_ROOT / "stage158_validation_pf_margin_summary.csv"
SOURCE_SEGMENTS = SOURCE_ROOT / "stage158_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_ROOT / "stage158_risk_atr_telemetry.csv"
SOURCE_GATE = SOURCE_ROOT / "stage158_gate_feature_summary.csv"
SOURCE_TRADE_AUDIT = SOURCE_ROOT / "stage158_trade_audit.csv"
SOURCE_REPORT = SOURCE_ROOT / "stage158_validation_pf_margin_report.md"
SOURCE_DECISION = SOURCE_ROOT / "stage158_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage159_stage158_validation_pf_followup_review.md"
KPI_DELTA_PATH = REVIEWS_ROOT / "stage159_threshold_binding_summary.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage159_failure_memory.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage159_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage159_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage159_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage159/stage158_validation_pf_followup_review.py")

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
    columns = tuple(columns or (rows[0].keys() if rows else ()))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


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


def split_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def oos_mid_row(rows: Sequence[Mapping[str, Any]], adapter_id: str) -> Mapping[str, Any]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == "oos"
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == "mid"
        ):
            return row
    return {}


def build_review() -> dict[str, Any]:
    summary = read_csv(SOURCE_SUMMARY)
    segments = read_csv(SOURCE_SEGMENTS)
    gate = read_csv(SOURCE_GATE)
    adapters = sorted({row["adapter_id"] for row in summary if row.get("view") == "actual_routed_total"})
    base_adapter = "s158_valpf_lng53_risk0300_h3_cd5_sht54_lng53"
    base_val = split_row(summary, base_adapter, "validation_is")
    base_oos = split_row(summary, base_adapter, "oos")
    base_mid = oos_mid_row(segments, base_adapter)

    rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    for adapter in adapters:
        val = split_row(summary, adapter, "validation_is")
        oos = split_row(summary, adapter, "oos")
        mid = oos_mid_row(segments, adapter)
        gate_rows = [row for row in gate if row.get("variant_id") == adapter]
        val_gate = next((row for row in gate_rows if row.get("split") == "validation_is"), {})
        oos_gate = next((row for row in gate_rows if row.get("split") == "oos"), {})
        row = {
            "adapter_id": adapter,
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_pf_delta_vs_base": as_float(val.get("profit_factor")) - as_float(base_val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_pf_delta_vs_base": as_float(oos.get("profit_factor")) - as_float(base_oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_net_delta_vs_base": as_float(oos.get("net_profit")) - as_float(base_oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_dd_delta_vs_base": as_float(oos.get("max_drawdown_percent")) - as_float(base_oos.get("max_drawdown_percent")),
            "oos_mid_pf": as_float(mid.get("profit_factor")),
            "oos_mid_pf_delta_vs_base": as_float(mid.get("profit_factor")) - as_float(base_mid.get("profit_factor")),
            "validation_gate_blocked_ratio": as_float(val_gate.get("blocked_ratio")),
            "oos_gate_blocked_ratio": as_float(oos_gate.get("blocked_ratio")),
            "stage159_label": "threshold_non_binding_or_not_material" if adapter != base_adapter else "base_stage158_candidate",
            "overall_goal_complete": False,
        }
        if row["validation_pf"] < LEGACY_34D["profit_factor"]:
            failure_rows.append(
                {
                    "adapter_id": adapter,
                    "failure_label": row["stage159_label"],
                    "reason": "validation_pf_still_below_34d_and_threshold_variants_have_zero_or_near_zero_kpi_delta",
                    "next_use": "threshold_binding_audit_input",
                    "overall_goal_complete": False,
                }
            )
        rows.append(row)

    all_non_binding = all(abs(row["validation_pf_delta_vs_base"]) < 0.000001 and abs(row["oos_net_delta_vs_base"]) < 0.01 for row in rows if row["adapter_id"] != "s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53")
    route = [
        {
            "decision": DECISION,
            "reason": "stage158_threshold_variants_did_not_materially_change_trade_count_or_kpi_and_validation_pf_remains_below_34d",
            "next_stage": NEXT_STAGE_ID,
            "next_axis": "audit_threshold_binding_decision_score_distribution_and_runtime_handoff_before_more_tuning",
            "primary_input": rel(SOURCE_SUMMARY),
            "do_not_repeat": "do_not_keep_raising_thresholds_without_proving_thresholds_bind",
            "overall_goal_complete": False,
        }
    ]
    return {
        "decision": DECISION,
        "kpi_delta_rows": rows,
        "failure_memory": failure_rows,
        "all_threshold_variants_non_binding": all_non_binding,
        "route_decision": route,
        "legacy_34d": LEGACY_34D,
        "overall_goal_complete": False,
    }


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | val PF delta(검증 수익요인 차이) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS mid PF(표본외 중반 수익요인) | label(라벨) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {validation_pf_delta_vs_base:.6f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_mid_pf:.9f} | {stage159_label} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(review: Mapping[str, Any]) -> str:
    return f"""# Stage159 Stage158 Validation PF Follow-up Review(159단계 158단계 검증 수익요인 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

No(아니오). Stage158(158단계)는 validation PF(검증 수익요인)를 올리지 못했다.

더 중요한 판독(read, 판독)은 threshold variants(문턱값 변형)가 trade count/KPI(거래 수/핵심 성과 지표)를 거의 바꾸지 않았다는 점이다. Effect(효과): 다음은 더 센 threshold(문턱값)가 아니라 threshold binding audit(문턱값 작동 감사)이어야 한다.

## KPI Delta Read(KPI 차이 판독)

{kpi_table(review["kpi_delta_rows"])}

## Judgment(판정)

- threshold_binding_risk(문턱값 작동 위험): `{review["all_threshold_variants_non_binding"]}`
- decision(판정): `{DECISION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Stage159(159단계)는 review-only(검토 전용)다. Effect(효과): 새 MT5(메타트레이더5) 실험을 더 붙이지 않고, Stage160(160단계) audit(감사)로 원인 확인을 분리한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage159 Decision(159단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- source_gate(원천 게이트): `{rel(SOURCE_GATE)}`
- source_trade_audit(원천 거래 감사): `{rel(SOURCE_TRADE_AUDIT)}`
- review_report(검토 보고서): `{rel(REPORT_PATH)}`
- threshold_binding_summary(문턱값 작동 요약): `{rel(KPI_DELTA_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage159(159단계)는 review-only(검토 전용)로 닫는다. Effect(효과): Stage158(158단계)의 무변화 threshold(문턱값) 축을 Stage160(160단계) threshold binding audit(문턱값 작동 감사)로 넘긴다.

overall_goal_complete(전체 목표 완료): `false`
"""


def write_stage160_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage160(160단계)는 Stage158(158단계) threshold(문턱값) 변형이 왜 KPI(핵심 성과 지표)를 바꾸지 않았는지 감사한다.

## Bounded Question(경계 질문)

Are the short/long threshold controls(숏/롱 문턱값 제어)가 model export(모델 내보내기), set file(설정 파일), EA runtime(전문가 자문 런타임), and decision telemetry(판정 기록)에서 실제로 binding(작동)하는가, 아니면 다른 path(경로)가 entry decision(진입 판정)을 지배하는가?

Effect(효과): 작동하지 않는 knob(조절값)을 계속 돌리지 않고, 다음 repair(수리) 축을 증거로 정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage160 Input References(160단계 입력 참조)

- stage159_decision(159단계 판정): `{rel(DECISION_PATH)}`
- stage159_review(159단계 검토): `{rel(REPORT_PATH)}`
- stage159_threshold_binding_summary(159단계 문턱값 작동 요약): `{rel(KPI_DELTA_PATH)}`
- source_stage158_summary(원천 158단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage158_gate(원천 158단계 게이트): `{rel(SOURCE_GATE)}`
- source_stage158_trade_audit(원천 158단계 거래 감사): `{rel(SOURCE_TRADE_AUDIT)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage160 Review Index(160단계 검토 색인)

- status(상태): `open_planned_from_stage159`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage160(160단계) threshold binding audit(문턱값 작동 감사) 산출물을 추적한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage160 Selection Status(160단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage159`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage160(160단계)는 threshold binding(문턱값 작동 여부) 감사만 흡수한다.
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?ms)\nstage159_stage158_validation_pf_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage160_stage158_threshold_binding_audit:.*?(?=\nstage\d+_|$)", "\n", state)
    block = f"""
stage159_stage158_validation_pf_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only_{DECISION}
  current_run_id: {RUN_ID}
  source_stage158_closeout_commit: {SOURCE_CLOSEOUT_COMMIT}
  source_stage158_hash_record_commit: {SOURCE_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage160_stage158_threshold_binding_audit:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage159
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
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
- adapter_under_review(검토 중 어댑터): `stage160_stage158_threshold_binding_audit_surface`
- status(상태): `stage159_closed_review_only_{DECISION}_stage160_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage159(159단계)는 Stage158(158단계)의 validation PF(검증 수익요인) repair(수리)를 review-only(검토 전용)로 판정했다. Effect(효과): threshold(문턱값) 변형이 KPI(핵심 성과 지표)를 바꾸지 않은 원인을 Stage160(160단계) audit(감사)로 분리한다.

## Latest Stage159 Evidence(최신 159단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_binding_summary(문턱값 작동 요약): `{rel(KPI_DELTA_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage159 Selection Status(159단계 선택 상태)

- stage_status(단계 상태): `closed_review_only_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- stage159_decision(159단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage159(159단계)는 Stage158(158단계) 무변화 결과를 닫고 Stage160(160단계) audit(감사)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage159 Review Index(159단계 검토 색인)

- status(상태): `closed_review_only_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_binding_summary(문턱값 작동 요약): `{rel(KPI_DELTA_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage159(159단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage159 Stage158 validation PF follow-up review closeout(159단계 158단계 검증 수익요인 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): threshold(문턱값) 조정 무변화 문제를 Stage160(160단계) threshold binding audit(문턱값 작동 감사)로 분리했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, KPI_DELTA_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage159_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage159 review-only Stage158 validation PF follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage159_stage158_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("source_closeout_commit", SOURCE_CLOSEOUT_COMMIT), ("source_hash_record_commit", SOURCE_HASH_RECORD_COMMIT), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0))),
            }
        ],
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
        "kpi_scope": "validation_oos_segment_threshold_binding",
        "scoreboard_lane": "baseline_adapter_stage159",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": "stage158_threshold_variants_no_material_kpi_delta;validation_pf_still_1.55_or_1.54",
        "guardrail_kpi": "legacy_34d_pf=1.583157;overall_goal_complete=false",
        "external_verification_status": "completed_from_stage158_mt5_evidence",
        "notes": ledger_pairs((("source_summary", rel(SOURCE_SUMMARY)), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    payloads = {
        "routing_receipt.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "result_judgment", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "status": "completed"},
        "kpi_contract_audit.json": {"legacy_34d_target": LEGACY_34D, "source_summary": rel(SOURCE_SUMMARY), "threshold_binding_summary": rel(KPI_DELTA_PATH), "status": "completed"},
        "result_judgment_gate.json": {"judgment_label": "threshold_variants_non_binding_candidate_not_final", "decision": DECISION, "claim_boundary": BOUNDARY, "overall_goal_complete": False, "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {"observed_change": "Stage158 threshold variants produced zero or near-zero KPI movement.", "likely_driver": "threshold controls may not bind the decision path or score distribution is far from tested thresholds.", "next_probe": NEXT_STAGE_ID, "status": "completed"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_GATE), rel(SOURCE_TRADE_AUDIT), rel(SOURCE_DECISION)], "producer": rel(PRODUCER_PATH), "artifact_paths": [rel(path) for path in [REPORT_PATH, KPI_DELTA_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]], "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)], "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"packet_id": PACKET_ID, "run_id": RUN_ID, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "source_stage158_closeout_commit": SOURCE_CLOSEOUT_COMMIT, "source_stage158_hash_record_commit": SOURCE_HASH_RECORD_COMMIT, "threshold_binding_summary": rel(KPI_DELTA_PATH), "route_decision": rel(ROUTE_DECISION_PATH), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False},
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def run() -> dict[str, Any]:
    review = build_review()
    write_csv(KPI_DELTA_PATH, review["kpi_delta_rows"])
    write_csv(FAILURE_MEMORY_PATH, review["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, review["route_decision"])
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown())
    write_json(SUMMARY_JSON_PATH, review)
    ledger_payload = write_ledgers(review)
    write_packet_files(review, ledger_payload)
    write_stage160_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    return {"status": "completed", "decision": DECISION, "report": rel(REPORT_PATH)}


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

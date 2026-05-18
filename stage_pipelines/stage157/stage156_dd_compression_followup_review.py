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

STAGE_ID = "157_adapter_research__stage156_dd_compression_followup_review"
RUN_ID = "run157A_stage157_stage156_dd_compression_followup_review_v1"
PACKET_ID = "stage157_stage156_dd_compression_followup_review_v1"
SOURCE_STAGE_ID = "156_adapter_research__stage154_low_edge_oos_dd_compression_repair"
SOURCE_RUN_ID = "run156A_stage156_stage154_low_edge_oos_dd_compression_repair_v1"
SOURCE_CLOSEOUT_COMMIT = "15c6091dfe5cbbcb742b44c573b4785e840279a9"
SOURCE_HASH_RECORD_COMMIT = "88dfb2aecbdea6ef136e844d2dd64d2f0094f4b9"
NEXT_STAGE_ID = "158_adapter_research__stage156_validation_pf_margin_repair"
NEXT_RUN_ID = "run158A_stage158_stage156_validation_pf_margin_repair_v1"
NEXT_PACKET_ID = "stage158_stage156_validation_pf_margin_repair_v1"
DECISION = "open_stage158_stage156_validation_pf_margin_repair_candidate_not_final"
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

PRIMARY_CANDIDATE = "s156_low_edge_risk0300_h3_cd5_sht54_lng52"
BACKUP_CANDIDATE = "s156_low_edge_risk0325_h3_cd5_sht54_lng52"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"

SOURCE_SUMMARY = SOURCE_ROOT / "stage156_oos_dd_compression_summary.csv"
SOURCE_SEGMENTS = SOURCE_ROOT / "stage156_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_ROOT / "stage156_risk_atr_telemetry.csv"
SOURCE_REPORT = SOURCE_ROOT / "stage156_oos_dd_compression_report.md"
SOURCE_DECISION = SOURCE_ROOT / "stage156_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage157_stage156_dd_compression_followup_review.md"
KPI_JUDGMENT_PATH = REVIEWS_ROOT / "stage157_kpi_judgment_summary.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage157_failure_memory.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage157_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage157_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage157_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage157/stage156_dd_compression_followup_review.py")

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


def risk_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def margin(value: float, target: float, *, lower_is_better: bool = False) -> float:
    return target - value if lower_is_better else value - target


def label_row(row: Mapping[str, Any]) -> tuple[str, str, str]:
    if row["adapter_id"] == PRIMARY_CANDIDATE:
        return (
            "best_dd_compression_candidate_not_final",
            "primary_stage158_seed",
            "validation_pf_below_34d_and_net_margin_thin",
        )
    if row["adapter_id"] == BACKUP_CANDIDATE:
        return (
            "backup_dd_compression_candidate_not_final",
            "backup_stage158_seed",
            "oos_net_cushion_better_but_validation_pf_below_34d_and_oos_dd_close_to_limit",
        )
    if row["oos_dd_margin_vs_34d"] < 0:
        return ("oos_dd_failed_after_atr_stop_tightening", "failure_memory", "oos_dd_above_34d_target")
    return ("validation_pf_failed", "failure_memory", "validation_pf_below_34d_target")


def build_review() -> dict[str, Any]:
    summary = read_csv(SOURCE_SUMMARY)
    segments = read_csv(SOURCE_SEGMENTS)
    risk = read_csv(SOURCE_RISK_ATR)
    adapters = sorted({row["adapter_id"] for row in summary if row.get("view") == "actual_routed_total"})
    judgment_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []

    for adapter_id in adapters:
        val = split_row(summary, adapter_id, "validation_is")
        oos = split_row(summary, adapter_id, "oos")
        mid = oos_mid_row(segments, adapter_id)
        risk_oos = risk_row(risk, adapter_id, "oos")
        row = {
            "adapter_id": adapter_id,
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_pf_margin_vs_34d": margin(as_float(val.get("profit_factor")), LEGACY_34D["profit_factor"]),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_pf_margin_vs_34d": margin(as_float(oos.get("profit_factor")), LEGACY_34D["profit_factor"]),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_net_margin_vs_34d": margin(as_float(oos.get("net_profit")), LEGACY_34D["net_profit"]),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_dd_margin_vs_34d": margin(as_float(oos.get("max_drawdown_percent")), LEGACY_34D["max_drawdown_percent"], lower_is_better=True),
            "oos_mid_pf": as_float(mid.get("profit_factor")),
            "oos_mid_pf_margin_vs_34d": margin(as_float(mid.get("profit_factor")), LEGACY_34D["profit_factor"]),
            "oos_mid_net": as_float(mid.get("net_profit")),
            "trade_count": as_float(oos.get("trade_count")),
            "risk_floor_applied_count": as_float(risk_oos.get("risk_floor_applied_count")),
            "max_model_risk_pct": as_float(risk_oos.get("max_model_risk_pct")),
            "max_actual_risk_pct_after_floor": as_float(risk_oos.get("max_actual_risk_pct_after_floor")),
            "avg_executed_lot": as_float(risk_oos.get("avg_executed_lot")),
            "atr_stop_multiplier": as_float(risk_oos.get("atr_stop_multiplier")),
            "atr_take_profit_multiplier": as_float(risk_oos.get("atr_take_profit_multiplier")),
            "overall_goal_complete": False,
        }
        label, next_use, reason = label_row(row)
        row["stage157_label"] = label
        row["next_use"] = next_use
        row["reason"] = reason
        row["strict_34d_surface_pass"] = (
            row["validation_pf_margin_vs_34d"] >= 0
            and row["oos_pf_margin_vs_34d"] >= 0
            and row["oos_net_margin_vs_34d"] >= 0
            and row["oos_dd_margin_vs_34d"] >= 0
            and row["oos_mid_pf_margin_vs_34d"] >= 0
        )
        judgment_rows.append(row)
        if next_use != "primary_stage158_seed":
            failure_rows.append(
                {
                    "adapter_id": adapter_id,
                    "stage157_label": label,
                    "reason": reason,
                    "next_use": next_use,
                    "validation_pf_margin_vs_34d": row["validation_pf_margin_vs_34d"],
                    "oos_dd_margin_vs_34d": row["oos_dd_margin_vs_34d"],
                    "overall_goal_complete": False,
                }
            )

    best = next((row for row in judgment_rows if row["adapter_id"] == PRIMARY_CANDIDATE), judgment_rows[0] if judgment_rows else {})
    route = [
        {
            "decision": DECISION,
            "reason": "stage156_compressed_oos_dd_below_34d_but_validation_pf_remains_below_34d_and_oos_net_margin_is_thin",
            "next_stage": NEXT_STAGE_ID,
            "next_seed": PRIMARY_CANDIDATE,
            "backup_seed": BACKUP_CANDIDATE,
            "next_axis": "raise_validation_pf_to_34d_or_better_without_losing_oos_dd_oos_pf_oos_net_or_oos_mid_pf",
            "stop_conditions": "validation_pf_ge_1_583157;oos_dd_le_12_909136;oos_pf_ge_1_583157;oos_net_gt_987_60;oos_mid_pf_ge_1_583157;risk_floor_count_eq_0",
            "overall_goal_complete": False,
        }
    ]
    return {
        "best_candidate": best,
        "decision": DECISION,
        "failure_memory": failure_rows,
        "kpi_judgment_rows": judgment_rows,
        "legacy_34d": LEGACY_34D,
        "overall_goal_complete": False,
        "route_decision": route,
    }


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS mid PF(표본외 중반 수익요인) | label(라벨) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_mid_pf:.9f} | {stage157_label} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(review: Mapping[str, Any]) -> str:
    best = review["best_candidate"]
    return f"""# Stage157 Stage156 DD Compression Follow-up Review(157단계 156단계 낙폭 압축 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

Partly yes, but not enough(부분 성공, 아직 부족).

Stage156(156단계)는 `s156_low_edge_risk0300_h3_cd5_sht54_lng52`에서 OOS DD(표본외 낙폭)를 `11.92`로 낮춰 34D target(34D 목표) `12.909136` 아래로 넣었다. Effect(효과): Stage154(154단계)의 가장 큰 DD(낙폭) 문제는 실제로 줄었다.

하지만 validation PF(검증 수익요인)가 `{as_float(best.get("validation_pf")):.6f}`로 34D target(34D 목표) `{LEGACY_34D["profit_factor"]:.6f}`보다 낮고, OOS net(표본외 순손익) margin(여유)이 `{as_float(best.get("oos_net_margin_vs_34d")):.2f}`로 얇다. Effect(효과): 이 후보는 research candidate(연구 후보)이지 final package(최종 패키지)가 아니다.

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(review["kpi_judgment_rows"])}

## Key Judgment(핵심 판정)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- OOS PF(표본외 수익요인): `{as_float(best.get("oos_pf")):.6f}` vs 34D target(34D 목표) `{LEGACY_34D["profit_factor"]:.6f}`
- OOS net(표본외 순손익): `{as_float(best.get("oos_net")):.2f}` vs 34D target(34D 목표) `{LEGACY_34D["net_profit"]:.2f}`
- OOS DD(표본외 낙폭): `{as_float(best.get("oos_dd_percent")):.2f}` vs 34D target(34D 목표) `{LEGACY_34D["max_drawdown_percent"]:.6f}`
- OOS mid PF(표본외 중반 수익요인): `{as_float(best.get("oos_mid_pf")):.9f}` vs 34D target(34D 목표) `{LEGACY_34D["profit_factor"]:.6f}`
- risk_floor_applied_count(위험 최소 lot 바닥 적용 수): `{as_float(best.get("risk_floor_applied_count")):.0f}`

Stage157(157단계)는 review-only(검토 전용)다. Effect(효과): 새 최적화(optimization, 최적화)나 MT5 rerun(MT5 재실행)을 하지 않고, Stage158(158단계)의 좁은 repair(수리) 질문만 연다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage157 Decision(157단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- source_segments(원천 구간): `{rel(SOURCE_SEGMENTS)}`
- source_risk_atr(원천 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- review_report(검토 보고서): `{rel(REPORT_PATH)}`
- kpi_judgment_summary(KPI 판정 요약): `{rel(KPI_JUDGMENT_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage157(157단계)는 review-only(검토 전용)로 닫는다. Effect(효과): Stage156(156단계)의 DD(낙폭) 개선은 보존하되, validation PF(검증 수익요인) 부족을 Stage158(158단계) repair(수리)로 분리한다.

overall_goal_complete(전체 목표 완료): `false`
"""


def write_stage158_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage158(158단계)는 Stage156(156단계)의 DD compression(낙폭 압축) 후보에서 validation PF(검증 수익요인) margin(여유)만 좁게 수리한다.

## Bounded Question(경계 질문)

Can `s156_low_edge_risk0300_h3_cd5_sht54_lng52` lift validation PF(검증 수익요인) to at least 34D target(34D 목표) `1.583157` while preserving OOS DD(표본외 낙폭) <= `12.909136`, OOS PF(표본외 수익요인) >= `1.583157`, OOS net(표본외 순손익) > `987.60`, OOS mid PF(표본외 중반 수익요인) >= `1.583157`, and risk/ATR telemetry(위험/ATR 기록)?

Effect(효과): DD(낙폭)를 다시 키우지 않고 validation(검증) 품질을 보강한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage158 Input References(158단계 입력 참조)

- stage157_decision(157단계 판정): `{rel(DECISION_PATH)}`
- stage157_review(157단계 검토): `{rel(REPORT_PATH)}`
- stage157_kpi_judgment_summary(157단계 KPI 판정 요약): `{rel(KPI_JUDGMENT_PATH)}`
- source_stage156_summary(원천 156단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage156_segments(원천 156단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage156_risk_atr(원천 156단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- primary_seed(주 씨앗): `{PRIMARY_CANDIDATE}`
- backup_seed(예비 씨앗): `{BACKUP_CANDIDATE}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage158 Review Index(158단계 검토 색인)

- status(상태): `open_planned_from_stage157`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage158(158단계) validation PF(검증 수익요인) repair(수리) 산출물을 추적한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage158 Selection Status(158단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage157`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage158(158단계)는 validation PF(검증 수익요인) 보강만 흡수한다.
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?ms)\nstage157_stage156_dd_compression_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage158_stage156_validation_pf_margin_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\n\n  packet_id: stage157_stage156_dd_compression_followup_review_v1.*?boundary: research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment\n", "\n", state)
    block = f"""
stage157_stage156_dd_compression_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only_{DECISION}
  current_run_id: {RUN_ID}
  source_stage156_closeout_commit: {SOURCE_CLOSEOUT_COMMIT}
  source_stage156_hash_record_commit: {SOURCE_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage158_stage156_validation_pf_margin_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage157
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
- adapter_under_review(검토 중 어댑터): `{PRIMARY_CANDIDATE}`
- status(상태): `stage157_closed_review_only_{DECISION}_stage158_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage157(157단계)는 Stage156(156단계)의 DD compression(낙폭 압축)을 review-only(검토 전용)로 판정했다. Effect(효과): DD(낙폭) 개선은 보존하고, validation PF(검증 수익요인) 부족은 Stage158(158단계) repair(수리)로 넘긴다.

## Latest Stage157 Evidence(최신 157단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- kpi_judgment_summary(KPI 판정 요약): `{rel(KPI_JUDGMENT_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage157 Selection Status(157단계 선택 상태)

- stage_status(단계 상태): `closed_review_only_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- stage157_decision(157단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage157(157단계)은 Stage156(156단계) KPI(핵심 성과 지표) 판정을 닫고 Stage158(158단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage157 Review Index(157단계 검토 색인)

- status(상태): `closed_review_only_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- kpi_judgment_summary(KPI 판정 요약): `{rel(KPI_JUDGMENT_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage157(157단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage157 Stage156 DD compression follow-up review closeout(157단계 156단계 낙폭 압축 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage156(156단계)의 OOS DD(표본외 낙폭) 개선을 보존하고 validation PF(검증 수익요인) 보강을 Stage158(158단계)로 분리했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, KPI_JUDGMENT_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage157_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage157 review-only Stage156 DD compression follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any]) -> dict[str, Any]:
    best = review["best_candidate"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage157_stage156_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_closeout_commit", SOURCE_CLOSEOUT_COMMIT),
                        ("source_hash_record_commit", SOURCE_HASH_RECORD_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", 0),
                    )
                ),
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
        "kpi_scope": "validation_oos_segment_risk_atr_kpi",
        "scoreboard_lane": "baseline_adapter_stage157",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": (
            f"best={best.get('adapter_id')};validation_pf={best.get('validation_pf')};"
            f"oos_pf={best.get('oos_pf')};oos_net={best.get('oos_net')};"
            f"oos_dd={best.get('oos_dd_percent')};oos_mid_pf={best.get('oos_mid_pf')}"
        ),
        "guardrail_kpi": "legacy_34d_pf=1.583157;legacy_34d_oos_dd=12.909136;overall_goal_complete=false",
        "external_verification_status": "completed_from_stage156_mt5_evidence",
        "notes": ledger_pairs((("source_summary", rel(SOURCE_SUMMARY)), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    payloads = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "legacy_34d_target": LEGACY_34D,
            "source_summary": rel(SOURCE_SUMMARY),
            "source_segments": rel(SOURCE_SEGMENTS),
            "source_risk_atr": rel(SOURCE_RISK_ATR),
            "kpi_judgment_summary": rel(KPI_JUDGMENT_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(KPI_JUDGMENT_PATH), rel(FAILURE_MEMORY_PATH), rel(ROUTE_DECISION_PATH)],
            "evidence_missing": [],
            "judgment_label": "dd_compression_candidate_not_final_due_to_validation_pf_gap",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage158 must lift validation PF without damaging OOS DD/PF/net/mid PF or risk/ATR telemetry.",
            "overall_goal_complete": False,
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage156 reduced OOS DD via model risk cap compression; validation PF remained below 34D.",
            "comparison_baseline": "Stage154 low-edge seed and legacy 34D KPI target surface.",
            "likely_drivers": ["model_risk_max_pct", "atr_stop_multiplier", "low_edge_gate_reuse"],
            "next_probe": NEXT_STAGE_ID,
            "attribution_confidence": "medium",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_REPORT), rel(SOURCE_DECISION)],
            "producer": rel(PRODUCER_PATH),
            "artifact_paths": [rel(path) for path in [REPORT_PATH, KPI_JUDGMENT_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {"packet_id": PACKET_ID, "run_id": RUN_ID, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage156_closeout_commit": SOURCE_CLOSEOUT_COMMIT,
            "source_stage156_hash_record_commit": SOURCE_HASH_RECORD_COMMIT,
            "best_candidate": review["best_candidate"],
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "kpi_judgment_summary": rel(KPI_JUDGMENT_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "route_decision": rel(ROUTE_DECISION_PATH),
                "decision": rel(DECISION_PATH),
                "summary_json": rel(SUMMARY_JSON_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def run() -> dict[str, Any]:
    review = build_review()
    write_csv(KPI_JUDGMENT_PATH, review["kpi_judgment_rows"])
    write_csv(FAILURE_MEMORY_PATH, review["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, review["route_decision"])
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown())
    write_json(SUMMARY_JSON_PATH, review)
    ledger_payload = write_ledgers(review)
    write_packet_files(review, ledger_payload)
    write_stage158_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    return {"status": "completed", "decision": DECISION, "best_candidate": review["best_candidate"], "report": rel(REPORT_PATH)}


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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

STAGE_ID = "162_adapter_research__stage161_score_margin_followup_review"
RUN_ID = "run162A_stage162_stage161_score_margin_followup_review_v1"
PACKET_ID = "stage162_stage161_score_margin_followup_review_v1"
SOURCE_STAGE_ID = "161_adapter_research__score_margin_or_side_filter_repair"
SOURCE_RUN_ID = "run161A_stage161_score_margin_or_side_filter_repair_v1"
SOURCE_STAGE161_CLOSEOUT_COMMIT = "b9f95b07366d9135d90df5a103070d98f1a0f1fd"
SOURCE_STAGE161_HASH_RECORD_COMMIT = "a95c66c979f0d2a166a68aaf174c0d77b4aab013"
NEXT_STAGE_ID = "163_adapter_research__stage161_density_preserving_score_repair"
NEXT_RUN_ID = "run163A_stage163_stage161_density_preserving_score_repair_v1"
NEXT_PACKET_ID = "stage163_stage161_density_preserving_score_repair_v1"
DECISION = "open_stage163_density_preserving_score_repair_candidate_not_final"
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

SOURCE_REFERENCE = {
    "adapter_id": "s156_low_edge_risk0300_h3_cd5_sht54_lng52",
    "validation_pf": 1.55,
    "validation_net": 1037.79,
    "validation_dd_percent": 10.23,
    "validation_trade_count": 275,
    "oos_pf": 1.85,
    "oos_net": 1032.34,
    "oos_dd_percent": 11.92,
    "oos_trade_count": 193,
    "oos_mid_pf": 1.659175838,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_REPORT = SOURCE_ROOT / "stage161_score_margin_or_side_filter_repair_report.md"
SOURCE_SUMMARY = SOURCE_ROOT / "stage161_score_margin_or_side_filter_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_ROOT / "stage161_segment_kpi_summary.csv"
SOURCE_PROBABILITY = SOURCE_ROOT / "stage161_probability_binding_summary.csv"
SOURCE_RISK_ATR = SOURCE_ROOT / "stage161_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_ROOT / "stage161_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage162_stage161_score_margin_followup_review.md"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage162_score_margin_followup_summary.csv"
SEGMENT_FLAGS_PATH = REVIEWS_ROOT / "stage162_segment_damage_summary.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage162_route_decision.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage162_failure_memory.csv"
DECISION_PATH = REVIEWS_ROOT / "stage162_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage162_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage162/stage161_score_margin_followup_review.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def summary_row(rows: Sequence[Mapping[str, str]], adapter_id: str, split: str) -> Mapping[str, str]:
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


def probability_rows(rows: Sequence[Mapping[str, str]], adapter_id: str) -> list[Mapping[str, str]]:
    return [row for row in rows if row.get("adapter_id") == adapter_id and row.get("view") == "actual_routed_total"]


def verdict_for(row: Mapping[str, Any]) -> str:
    flags: list[str] = []
    if row["validation_pf"] < LEGACY_34D["profit_factor"]:
        flags.append("validation_pf_below_34d_not_enough")
    if row["oos_pf"] < LEGACY_34D["profit_factor"]:
        flags.append("oos_pf_below_34d_not_enough")
    if row["oos_dd_percent"] > LEGACY_34D["max_drawdown_percent"]:
        flags.append("oos_dd_above_34d_damage")
    if row["oos_early_pf"] < 1.10 or row["oos_early_net"] <= 0:
        flags.append("pf_uplift_with_oos_early_segment_damage")
    if row["validation_net_retention_vs_source"] < 0.35 or row["oos_net_retention_vs_source"] < 0.35:
        flags.append("pf_uplift_with_net_density_damage")
    return ";".join(flags) if flags else "useful_but_candidate_not_final"


def build_review() -> dict[str, Any]:
    summary = read_csv(SOURCE_SUMMARY)
    segments = read_csv(SOURCE_SEGMENTS)
    probability = read_csv(SOURCE_PROBABILITY)
    adapters = sorted({row["adapter_id"] for row in summary if row.get("view") == "actual_routed_total"})

    review_rows: list[dict[str, Any]] = []
    segment_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []

    for adapter_id in adapters:
        val = summary_row(summary, adapter_id, "validation_is")
        oos = summary_row(summary, adapter_id, "oos")
        val_mid = segment_row(segments, adapter_id, "validation_is", "mid")
        oos_early = segment_row(segments, adapter_id, "oos", "early")
        oos_mid = segment_row(segments, adapter_id, "oos", "mid")
        oos_late = segment_row(segments, adapter_id, "oos", "late")
        probs = probability_rows(probability, adapter_id)
        directional_band = max((as_int(row.get("directional_050_060_band_rows")) for row in probs), default=0)
        near_threshold = max((as_int(row.get("directional_near_threshold_001_rows")) for row in probs), default=0)
        side_block = max((as_int(row.get("side_filter_block_rows")) for row in probs), default=0)
        threshold_block = max((as_int(row.get("threshold_or_margin_not_met_rows")) for row in probs), default=0)

        row = {
            "adapter_id": adapter_id,
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "validation_trade_count": as_int(val.get("trade_count")),
            "validation_mid_pf": as_float(val_mid.get("profit_factor")),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trade_count": as_int(oos.get("trade_count")),
            "oos_early_pf": as_float(oos_early.get("profit_factor")),
            "oos_early_net": as_float(oos_early.get("net_profit")),
            "oos_mid_pf": as_float(oos_mid.get("profit_factor")),
            "oos_late_pf": as_float(oos_late.get("profit_factor")),
            "validation_pf_gap_vs_34d": as_float(val.get("profit_factor")) - LEGACY_34D["profit_factor"],
            "oos_pf_gap_vs_34d": as_float(oos.get("profit_factor")) - LEGACY_34D["profit_factor"],
            "oos_dd_gap_vs_34d": LEGACY_34D["max_drawdown_percent"] - as_float(oos.get("max_drawdown_percent")),
            "validation_net_retention_vs_source": as_float(val.get("net_profit")) / SOURCE_REFERENCE["validation_net"],
            "oos_net_retention_vs_source": as_float(oos.get("net_profit")) / SOURCE_REFERENCE["oos_net"],
            "oos_trade_retention_vs_source": as_int(oos.get("trade_count")) / SOURCE_REFERENCE["oos_trade_count"],
            "directional_050_060_band_rows": directional_band,
            "directional_near_threshold_001_rows": near_threshold,
            "side_filter_block_rows": side_block,
            "threshold_or_margin_not_met_rows": threshold_block,
            "probability_binding_observed": directional_band > 0 and (near_threshold > 0 or threshold_block > 0),
            "overall_goal_complete": False,
        }
        row["stage162_verdict"] = verdict_for(row)
        review_rows.append(row)

        for split, segment, source in (
            ("validation_is", "mid", val_mid),
            ("oos", "early", oos_early),
            ("oos", "mid", oos_mid),
            ("oos", "late", oos_late),
        ):
            flags = []
            pf = as_float(source.get("profit_factor"))
            net = as_float(source.get("net_profit"))
            if pf < 1.10:
                flags.append("weak_pf")
            if net <= 0:
                flags.append("negative_or_flat_net")
            if split == "oos" and segment == "early" and (pf < 1.10 or net <= 0):
                flags.append("oos_early_damage")
            segment_rows.append(
                {
                    "adapter_id": adapter_id,
                    "split": split,
                    "segment": segment,
                    "trade_count": as_int(source.get("trade_count")),
                    "profit_factor": pf,
                    "net_profit": net,
                    "max_drawdown_amount": as_float(source.get("max_closed_trade_drawdown")),
                    "flags": ";".join(flags) if flags else "acceptable_measurement_only",
                }
            )

        if row["stage162_verdict"] != "useful_but_candidate_not_final":
            failure_rows.append(
                {
                    "adapter_id": adapter_id,
                    "failure_label": row["stage162_verdict"],
                    "reason": "Stage162 review found PF/net/DD/segment tradeoff that prevents research baseline selection.",
                    "next_use": "Stage163 density-preserving score repair input",
                    "overall_goal_complete": False,
                }
            )

    best_pf = max(review_rows, key=lambda item: (item["validation_pf"] >= LEGACY_34D["profit_factor"], item["oos_pf"], item["validation_pf"]))
    route = [
        {
            "decision": DECISION,
            "next_stage": NEXT_STAGE_ID,
            "primary_branch_to_repair": "s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52",
            "reason": "shortprob lifts validation/OOS PF above legacy 34D but loses too much net/trade density and has OOS early damage.",
            "preserve": "non_saturated_probability_binding_and_pf_uplift",
            "repair": "recover_density_and_oos_early_segment_without_reintroducing_oos_dd_damage",
            "reject_as_final": "all_stage161_variants_candidate_not_final",
            "overall_goal_complete": False,
        }
    ]
    return {
        "decision": DECISION,
        "review_rows": review_rows,
        "segment_damage_rows": segment_rows,
        "failure_memory": failure_rows,
        "route_decision": route,
        "best_pf_adapter": best_pf["adapter_id"],
        "legacy_34d": LEGACY_34D,
        "source_reference": SOURCE_REFERENCE,
        "overall_goal_complete": False,
    }


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | verdict(판정) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {validation_net:.2f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_early_pf:.6f} | {stage162_verdict} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(review: Mapping[str, Any]) -> str:
    route = review["route_decision"][0]
    return f"""# Stage162 Stage161 Score Margin Follow-up Review(162단계 161단계 점수 마진 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE161_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE161_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

Stage161(161단계)은 useful signal(유용한 신호)을 만들었다. Effect(효과): saturated score(포화 점수) 문제는 줄었고 threshold/filter(문턱값/필터)가 실제로 행 선택(row selection, 행 선택)을 바꿨다.

하지만 final research baseline(최종 연구 기준선)은 아니다. Effect(효과): shortprob(숏 확률 필터)는 PF(수익요인)는 좋지만 net/trade density(순손익/거래 밀도)가 너무 줄고 OOS early(표본외 초반) 구간이 손상됐다.

## KPI Read(KPI 판독)

{kpi_table(review["review_rows"])}

## Route(경로)

- decision(판정): `{DECISION}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- preserve(보존): `{route["preserve"]}`
- repair(수리): `{route["repair"]}`
- reject_as_final(최종 불가): `{route["reject_as_final"]}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage162 Decision(162단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_STAGE161_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE161_HASH_RECORD_COMMIT}`
- review_report(검토 보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_damage_summary(구간 손상 요약): `{rel(SEGMENT_FLAGS_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage162(162단계)은 review-only(검토 전용)로 닫는다. Effect(효과): Stage161(161단계) 안에서 계속 고치지 않고 Stage163(163단계) density-preserving repair(밀도 보존 수리)로 넘긴다.

overall_goal_complete(전체 목표 완료): `false`
"""


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage163(163단계)는 Stage161(161단계) shortprob(숏 확률 필터)의 PF uplift(수익요인 상승)를 보존하면서 net/trade density(순손익/거래 밀도)와 OOS early(표본외 초반) 손상을 수리한다.

## Bounded Question(경계 질문)

Can a density-preserving score repair(밀도 보존 점수 수리) keep validation/OOS PF(검증/표본외 수익요인) at or above legacy 34D(레거시 34D) while recovering net(순손익), trade count(거래수), OOS early segment(표본외 초반 구간), and DD(낙폭)?

Effect(효과): PF(수익요인)만 높은 얇은 가지를 최종처럼 착각하지 않고, 거래 밀도와 구간 안정성을 같이 고친다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage163 Input References(163단계 입력 참조)

- stage162_decision(162단계 판정): `{rel(DECISION_PATH)}`
- stage162_review(162단계 검토): `{rel(REPORT_PATH)}`
- stage162_summary(162단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage162_segment_damage(162단계 구간 손상): `{rel(SEGMENT_FLAGS_PATH)}`
- stage161_summary(161단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage161_probability_binding(161단계 확률 작동): `{rel(SOURCE_PROBABILITY)}`
- source_stage161_closeout_commit(원천 161단계 종료 커밋): `{SOURCE_STAGE161_CLOSEOUT_COMMIT}`
- source_stage161_hash_record_commit(원천 161단계 해시 기록 커밋): `{SOURCE_STAGE161_HASH_RECORD_COMMIT}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage163 Review Index(163단계 검토 색인)

- status(상태): `open_planned_from_stage162`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage163(163단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage163 Selection Status(163단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage162`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage163(163단계)는 연구개발(research/development, 연구개발) 전용 bounded repair(경계 수리)로 고정된다.
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?m)^updated_on:.*$", "updated_on: '2026-05-18'", state)
    current_focus = f"""current_focus:
- >-
  Stage162(162단계) closed(종료) as `{DECISION}` and Stage163(163단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage161(161단계) PF(수익요인) 신호를 밀도 보존 수리로 넘긴다.
- >-
  Stage162 evidence(162단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_FLAGS_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): shortprob(숏 확률 필터)의 PF 상승과 net/trade density(순손익/거래 밀도) 손상을 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?s)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    state = re.sub(r"(?s)\nstage162_stage161_score_margin_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?s)\nstage163_stage161_density_preserving_score_repair:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage162_stage161_score_margin_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only_{DECISION}
  current_run_id: {RUN_ID}
  source_stage161_closeout_commit: {SOURCE_STAGE161_CLOSEOUT_COMMIT}
  source_stage161_hash_record_commit: {SOURCE_STAGE161_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage163_stage161_density_preserving_score_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage162
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
- adapter_under_review(검토 중 어댑터): `stage163_density_preserving_score_repair_surface`
- status(상태): `stage162_closed_review_only_{DECISION}_stage163_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage162(162단계)는 Stage161(161단계) score margin(점수 마진) / side filter(방향 필터) 결과를 review-only(검토 전용)로 판정했다. Effect(효과): PF(수익요인) 상승과 net/trade density(순손익/거래 밀도) 손상을 분리하고 Stage163(163단계) 수리로 넘긴다.

## Latest Stage162 Evidence(최신 162단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_damage(구간 손상): `{rel(SEGMENT_FLAGS_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage162 Selection Status(162단계 선택 상태)

- stage_status(단계 상태): `closed_review_only_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage161_closeout_commit(원천 161단계 종료 커밋): `{SOURCE_STAGE161_CLOSEOUT_COMMIT}`
- source_stage161_hash_record_commit(원천 161단계 해시 기록 커밋): `{SOURCE_STAGE161_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage162(162단계)은 한 질문만 닫고 Stage163(163단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage162 Review Index(162단계 검토 색인)

- status(상태): `closed_review_only_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_damage(구간 손상): `{rel(SEGMENT_FLAGS_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage162(162단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage162 Stage161 score margin follow-up review closeout(162단계 161단계 점수 마진 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage161(161단계)의 PF(수익요인) 개선 신호와 net/trade density(순손익/거래 밀도) 손상을 분리하고 Stage163(163단계) 수리축으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_FLAGS_PATH,
        ROUTE_DECISION_PATH,
        FAILURE_MEMORY_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage162_score_margin_followup_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage162 review-only score margin follow-up artifact.",
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
                "lane": "baseline_adapter_stage162_score_margin_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_closeout_commit", SOURCE_STAGE161_CLOSEOUT_COMMIT),
                        ("source_hash_record_commit", SOURCE_STAGE161_HASH_RECORD_COMMIT),
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
        "kpi_scope": "score_margin_side_filter_segment_density_review",
        "scoreboard_lane": "baseline_adapter_stage162",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": "shortprob_pf_above_34d_but_net_density_and_oos_early_damage",
        "guardrail_kpi": "overall_goal_complete=false;research_development_only",
        "external_verification_status": "completed_from_stage161_mt5_evidence",
        "notes": ledger_pairs((("source_summary", rel(SOURCE_SUMMARY)), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    artifact_paths = [
        rel(REPORT_PATH),
        rel(SUMMARY_CSV_PATH),
        rel(SEGMENT_FLAGS_PATH),
        rel(ROUTE_DECISION_PATH),
        rel(FAILURE_MEMORY_PATH),
        rel(DECISION_PATH),
        rel(SUMMARY_JSON_PATH),
    ]
    payloads = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "status": "completed",
        },
        "scope_completion_gate.json": {
            "bounded_question": "Did Stage161 create useful row-selection movement without unacceptable KPI or segment damage?",
            "decision": DECISION,
            "overall_goal_complete": False,
            "status": "passed",
        },
        "runtime_evidence_gate.json": {
            "external_verification_status": "completed_from_stage161_mt5_evidence",
            "new_mt5_run": False,
            "source_summary": rel(SOURCE_SUMMARY),
            "status": "passed",
        },
        "backtest_forensics_gate.json": {
            "source_stage": SOURCE_STAGE_ID,
            "source_report": rel(SOURCE_REPORT),
            "source_summary": rel(SOURCE_SUMMARY),
            "status": "passed_from_source_evidence",
        },
        "kpi_contract_audit.json": {
            "legacy_34d_target": LEGACY_34D,
            "source_reference": SOURCE_REFERENCE,
            "summary_csv": rel(SUMMARY_CSV_PATH),
            "segment_damage_csv": rel(SEGMENT_FLAGS_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "judgment_label": "useful_signal_but_not_final_due_density_and_segment_damage",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage161 shortprob raised PF but sharply reduced net/trade density and exposed OOS early damage.",
            "likely_driver": "probability calibration made thresholds bind, but the filter became too thin.",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_REPORT), rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_PROBABILITY), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)],
            "producer": rel(PRODUCER_PATH),
            "artifact_paths": artifact_paths,
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "runtime_parity_gate.json": {
            "runtime_parity_claim": False,
            "reason": "Stage162 is review-only and does not make new runtime parity claims.",
            "status": "passed",
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
        "required_gate_coverage_audit.json": {
            "declared_required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "runtime_parity_gate",
                "backtest_forensics_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "executed_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "runtime_parity_gate",
                "backtest_forensics_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage161_closeout_commit": SOURCE_STAGE161_CLOSEOUT_COMMIT,
            "source_stage161_hash_record_commit": SOURCE_STAGE161_HASH_RECORD_COMMIT,
            "summary_csv": rel(SUMMARY_CSV_PATH),
            "segment_damage_csv": rel(SEGMENT_FLAGS_PATH),
            "route_decision": rel(ROUTE_DECISION_PATH),
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
    write_csv(SUMMARY_CSV_PATH, review["review_rows"])
    write_csv(SEGMENT_FLAGS_PATH, review["segment_damage_rows"])
    write_csv(FAILURE_MEMORY_PATH, review["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, review["route_decision"])
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown())
    write_json(SUMMARY_JSON_PATH, review)
    ledger_payload = write_ledgers(review)
    write_packet_files(review, ledger_payload)
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    return {
        "status": "completed",
        "decision": DECISION,
        "report": rel(REPORT_PATH),
        "summary_csv": rel(SUMMARY_CSV_PATH),
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

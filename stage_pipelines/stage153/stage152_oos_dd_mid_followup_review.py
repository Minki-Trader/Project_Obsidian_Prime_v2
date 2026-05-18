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


STAGE_ID = "153_adapter_research__stage152_oos_dd_mid_followup_review"
RUN_ID = "run153A_stage153_stage152_oos_dd_mid_followup_review_v1"
PACKET_ID = "stage153_stage152_oos_dd_mid_followup_review_v1"
SOURCE_STAGE152_ID = "152_adapter_research__oos_dd_mid_compression_after_stage150_tradeoff"
SOURCE_STAGE152_CLOSEOUT_COMMIT = "94fc6e2bc70d0e64382c58b6b16d72916f401855"
SOURCE_STAGE152_HASH_RECORD_COMMIT = "ec5e4cf57daf52f95d8b92c8e2e85a93c244db35"
SOURCE_STAGE151_HASH_RECORD_COMMIT = "7cb669c9f17328c42658e903a03ec52f0cab85c0"
NEXT_STAGE_ID = "154_adapter_research__oos_mid_edge_restore_validation_repair"
NEXT_RUN_ID = "run154A_stage154_oos_mid_edge_restore_validation_repair_v1"
NEXT_PACKET_ID = "stage154_oos_mid_edge_restore_validation_repair_v1"
DECISION = "open_stage154_oos_mid_edge_restore_validation_repair_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE152_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage152_oos_dd_mid_compression_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage152_segment_kpi_summary.csv"
SOURCE_AUDIT = SOURCE_REVIEWS / "stage152_trade_audit.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage152_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage152_decision.md"
SOURCE_REPORT = SOURCE_REVIEWS / "stage152_oos_dd_mid_compression_report.md"

REPORT_PATH = REVIEWS_ROOT / "stage153_stage152_oos_dd_mid_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage153_stage152_tradeoff_summary.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage153_failure_memory.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage153_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage153_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage153_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage153/stage152_oos_dd_mid_followup_review.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE150_MARGIN_RESTORE = {
    "adapter_id": "s150_session_mid_margin_restore_h3_cd5_sht54_lng52_risk035",
    "validation_profit_factor": 1.59,
    "validation_net_profit": 1416.97,
    "validation_max_drawdown_percent": 11.82,
    "profit_factor": 1.73,
    "net_profit": 1045.62,
    "max_drawdown_percent": 18.94,
    "oos_mid_profit_factor": 1.578473376,
}


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
    if columns is None:
        columns = tuple(rows[0].keys()) if rows else ()
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


def segment_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
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


def strict_pass(val: Mapping[str, Any], oos: Mapping[str, Any], mid: Mapping[str, Any]) -> bool:
    return (
        as_float(val.get("profit_factor")) >= 1.55
        and as_float(val.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(val.get("max_drawdown_percent"), 99.0) <= 15.0
        and as_float(oos.get("profit_factor")) >= LEGACY_34D["profit_factor"]
        and as_float(oos.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(oos.get("max_drawdown_percent"), 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(mid.get("profit_factor")) >= LEGACY_34D["profit_factor"]
    )


def failure_label(val: Mapping[str, Any], oos: Mapping[str, Any], mid: Mapping[str, Any]) -> str:
    val_ok = (
        as_float(val.get("profit_factor")) >= 1.55
        and as_float(val.get("net_profit")) >= LEGACY_34D["net_profit"]
        and as_float(val.get("max_drawdown_percent"), 99.0) <= 15.0
    )
    oos_mid_ok = as_float(mid.get("profit_factor")) >= LEGACY_34D["profit_factor"]
    oos_dd_ok = as_float(oos.get("max_drawdown_percent"), 99.0) <= LEGACY_34D["max_drawdown_percent"]
    oos_net_ok = as_float(oos.get("net_profit")) >= LEGACY_34D["net_profit"]
    oos_pf_ok = as_float(oos.get("profit_factor")) >= LEGACY_34D["profit_factor"]
    if val_ok and oos_pf_ok and oos_net_ok and oos_dd_ok and oos_mid_ok:
        return "full_kpi_pass_candidate_not_final"
    if oos_mid_ok and oos_pf_ok and oos_net_ok and not val_ok:
        return "oos_mid_lifted_validation_failed"
    if val_ok and not oos_dd_ok:
        return "validation_preserved_oos_dd_failed"
    if oos_dd_ok and not oos_net_ok:
        return "dd_compressed_profit_collapsed"
    if val_ok and not oos_mid_ok:
        return "validation_preserved_oos_mid_failed"
    return "mixed_damage_no_full_repair"


def build_review() -> dict[str, Any]:
    summary = read_csv(SOURCE_SUMMARY)
    segments = read_csv(SOURCE_SEGMENTS)
    audit = read_csv(SOURCE_AUDIT)
    adapters = sorted({row.get("adapter_id", "") for row in summary if row.get("view") == "actual_routed_total"})
    tradeoff: list[dict[str, Any]] = []
    failure_memory: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = split_row(summary, adapter_id, "validation_is")
        oos = split_row(summary, adapter_id, "oos")
        val_mid = segment_row(segments, adapter_id, "validation_is", "mid")
        oos_mid = segment_row(segments, adapter_id, "oos", "mid")
        label = failure_label(val, oos, oos_mid)
        row = {
            "adapter_id": adapter_id,
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "validation_mid_pf": as_float(val_mid.get("profit_factor")),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trades": as_float(oos.get("trade_count")),
            "oos_mid_pf": as_float(oos_mid.get("profit_factor")),
            "oos_mid_net": as_float(oos_mid.get("net_profit")),
            "strict_pass": strict_pass(val, oos, oos_mid),
            "failure_label": label,
        }
        tradeoff.append(row)
        if label == "oos_mid_lifted_validation_failed":
            next_use = "use_as_stage154_oos_mid_seed_repair_validation"
        elif label == "validation_preserved_oos_dd_failed":
            next_use = "preserve_as_validation_recovery_failure_memory"
        elif label == "dd_compressed_profit_collapsed":
            next_use = "preserve_as_dd_compression_overfit_warning"
        else:
            next_use = "preserve_as_failure_memory"
        failure_memory.append(
            {
                "adapter_id": adapter_id,
                "failure_label": label,
                "next_use": next_use,
                "validation_gap": max(0.0, 1.55 - row["validation_pf"]),
                "oos_dd_excess_vs_34d": max(0.0, row["oos_dd_percent"] - LEGACY_34D["max_drawdown_percent"]),
                "oos_mid_gap_vs_34d": max(0.0, LEGACY_34D["profit_factor"] - row["oos_mid_pf"]),
                "profit_gap_vs_34d": max(0.0, LEGACY_34D["net_profit"] - row["oos_net"]),
            }
        )
    best_oos_mid = max(tradeoff, key=lambda row: (row["oos_mid_pf"], row["oos_pf"], -row["oos_dd_percent"])) if tradeoff else {}
    best_validation = max(tradeoff, key=lambda row: (row["validation_pf"], row["validation_net"], -row["oos_dd_percent"])) if tradeoff else {}
    route = [
        {
            "decision": DECISION,
            "reason": "stage152_split_the_problem_but_no_variant_passed_full_validation_oos_dd_mid_gate",
            "next_stage": NEXT_STAGE_ID,
            "next_seed": best_oos_mid.get("adapter_id", ""),
            "validation_memory": best_validation.get("adapter_id", ""),
            "next_axis": "restore_validation_on_margin_trim_oos_mid_seed_without_reintroducing_oos_dd",
            "do_not_repeat": "do_not_accept_margin_trim_oos_mid_without_validation_and_do_not_accept_margin_restore_validation_with_oos_dd_18_94",
            "overall_goal_complete": False,
        }
    ]
    return {
        "tradeoff": tradeoff,
        "failure_memory": failure_memory,
        "route": route,
        "audit_row_count": len(audit),
        "best_oos_mid_seed": best_oos_mid,
        "best_validation_memory": best_validation,
        "decision": DECISION,
        "overall_goal_complete": False,
    }


def table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 낙폭) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS mid PF(표본외 중반 수익 팩터) | label(라벨) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {validation_net:.2f} | {validation_dd_percent:.2f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_mid_pf:.9f} | {failure_label} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(review: Mapping[str, Any]) -> str:
    best_mid = review["best_oos_mid_seed"]
    best_val = review["best_validation_memory"]
    return f"""# Stage153 Stage152 Follow-up Review(153단계 152단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage152(원천 152단계): `{SOURCE_STAGE152_ID}`
- source_stage152_closeout_commit(원천 152단계 종료 커밋): `{SOURCE_STAGE152_CLOSEOUT_COMMIT}`
- source_stage152_hash_record_commit(원천 152단계 해시 기록 커밋): `{SOURCE_STAGE152_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

No(아니오). Stage152(152단계)는 문제를 분리하는 데는 성공했지만, validation(검증), OOS DD(표본외 낙폭), OOS mid PF(표본외 중반 수익 팩터)를 동시에 통과한 변형은 없었다.

Effect(효과): 좋은 한쪽만 잡고 candidate(후보)를 과장하지 않고, 다음 Stage154(154단계)를 작은 repair(수리) 질문으로 연다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table(review["tradeoff"])}

## Key Reads(핵심 판독)

- best_oos_mid_seed(최고 표본외 중반 씨앗): `{best_mid.get("adapter_id", "none")}` with OOS mid PF(표본외 중반 수익 팩터) `{as_float(best_mid.get("oos_mid_pf")):.9f}`, OOS DD(표본외 낙폭) `{as_float(best_mid.get("oos_dd_percent")):.2f}`, validation PF(검증 수익 팩터) `{as_float(best_mid.get("validation_pf")):.6f}`.
- best_validation_memory(최고 검증 기억): `{best_val.get("adapter_id", "none")}` with validation PF(검증 수익 팩터) `{as_float(best_val.get("validation_pf")):.6f}`, OOS DD(표본외 낙폭) `{as_float(best_val.get("oos_dd_percent")):.2f}`, OOS mid PF(표본외 중반 수익 팩터) `{as_float(best_val.get("oos_mid_pf")):.9f}`.
- lesson(교훈): margin_trim(마진 축소)은 OOS mid(표본외 중반)를 살렸지만 validation(검증)을 손상했고, margin_restore(마진 복원)는 validation(검증)을 살렸지만 OOS DD(표본외 낙폭)를 18.94로 남겼다.

## Next(다음)

Stage154(154단계)는 margin_trim(마진 축소)의 OOS mid(표본외 중반) 장점을 씨앗으로 쓰되, validation recovery(검증 회복)를 되살리는 작은 repair(수리)만 한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), production_baseline(생산 기준선), operating_promotion(운영 승격), operating_reference(운영 기준), runtime_authority(런타임 권위), overall_goal_complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage153 Decision(153단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- source_segments(원천 구간): `{rel(SOURCE_SEGMENTS)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage153(153단계)는 review-only(검토 전용)로 닫는다. Effect(효과): Stage152(152단계) 실패를 보존하고 Stage154(154단계) repair(수리)로 넘긴다.

overall_goal_complete(전체 목표 완료): `false`
"""


def write_stage154_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage154(154단계)는 Stage153(153단계) 판정에 따라 OOS mid seed(표본외 중반 씨앗)의 validation repair(검증 수리)를 연다.

## Bounded Question(경계 질문)

Can the Stage152 margin_trim(152단계 마진 축소) OOS mid lift(표본외 중반 상승)를 preserve(보존) while restoring validation PF/net(검증 수익 팩터/순손익) without bringing OOS DD(표본외 낙폭) back to the Stage150 margin_restore(150단계 마진 복원) damage level?

Effect(효과): OOS mid(표본외 중반)만 좋거나 validation(검증)만 좋은 후보를 최종처럼 보지 않고, 둘의 결합만 좁게 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage154 Input References(154단계 입력 참조)

- stage153_decision(153단계 판정): `{rel(DECISION_PATH)}`
- stage153_report(153단계 보고서): `{rel(REPORT_PATH)}`
- stage153_tradeoff_summary(153단계 상충 요약): `{rel(TRADEOFF_PATH)}`
- stage153_failure_memory(153단계 실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- source_stage152_summary(원천 152단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage152_segments(원천 152단계 구간): `{rel(SOURCE_SEGMENTS)}`
- primary_seed(주 씨앗): `s152_margin_restore_margin_trim_h3_cd5_sht54_lng52_risk035`
- validation_memory(검증 기억): `s152_margin_restore_threshold_guard_h3_cd5_sht55_lng53_risk035`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage154 Review Index(154단계 검토 색인)

- status(상태): `open_planned_from_stage153`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage154(154단계) 수리 산출물을 한 곳에서 추적한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage154 Selection Status(154단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage153`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `run154A_stage154_oos_mid_edge_restore_validation_repair_v1`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage154(154단계)는 validation(검증) 회복과 OOS mid/DD(표본외 중반/낙폭) 결합만 좁게 시험한다.
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    block = f"""
stage153_stage152_oos_dd_mid_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage152_closeout_commit: {SOURCE_STAGE152_CLOSEOUT_COMMIT}
  source_stage152_hash_record_commit: {SOURCE_STAGE152_HASH_RECORD_COMMIT}
  source_stage151_hash_record_commit: {SOURCE_STAGE151_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage154_oos_mid_edge_restore_validation_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage153
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run154A_stage154_oos_mid_edge_restore_validation_repair_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage153_stage152_oos_dd_mid_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage154_oos_mid_edge_restore_validation_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage153 Selection Status(153단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage152(원천 152단계): `{SOURCE_STAGE152_ID}`
- stage153_decision(153단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage153(153단계)는 실패를 숨기지 않고 Stage154(154단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage153 Review Index(153단계 검토 색인)

- status(상태): `closed_review_only`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage153(153단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage154_oos_mid_edge_restore_validation_repair_surface`
- status(상태): `stage153_closed_review_only_stage154_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage153(153단계)는 Stage152(152단계) failure shape(실패 모양)를 review-only(검토 전용)로 고정했다. Effect(효과): Stage154(154단계)는 margin_trim(마진 축소)의 OOS mid(표본외 중반) 장점을 보존하면서 validation(검증)을 되살리는 좁은 repair(수리)로 이어진다.

## Latest Stage153 Evidence(최신 153단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    write_stage154_seed()


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage153 Stage152 follow-up review closeout(153단계 152단계 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage152(152단계)가 OOS mid(표본외 중반), validation(검증), DD(낙폭)를 동시에 통과하지 못한 실패 모양을 보존하고 Stage154(154단계) 수리로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    rows = []
    for path in [REPORT_PATH, TRADEOFF_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH, PRODUCER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage153_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage153 review-only Stage152 OOS DD/mid follow-up artifact.",
                }
            )
    return rows


def write_ledgers() -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage153_stage152_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("source_stage152_closeout_commit", SOURCE_STAGE152_CLOSEOUT_COMMIT), ("source_stage152_hash_record_commit", SOURCE_STAGE152_HASH_RECORD_COMMIT), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0))),
            }
        ],
        key="run_id",
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_only",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "view": "review_only",
        "split": "stage152_existing_evidence",
        "tier": "actual_routed_total",
        "route_role": "followup_review",
        "status": "completed",
        "profit_factor": "",
        "net_profit": "",
        "max_drawdown_percent": "",
        "trade_count": "",
        "notes": ledger_pairs((("decision", DECISION), ("source_summary", rel(SOURCE_SUMMARY)), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "result_judgment", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"], "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"], "status": "completed"},
        "kpi_contract_audit.json": {"source_summary": rel(SOURCE_SUMMARY), "source_segments": rel(SOURCE_SEGMENTS), "tradeoff_path": rel(TRADEOFF_PATH), "failure_memory_path": rel(FAILURE_MEMORY_PATH), "status": "completed"},
        "result_judgment_gate.json": {"result_subject": RUN_ID, "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(FAILURE_MEMORY_PATH), rel(DECISION_PATH)], "evidence_missing": ["new_repair_not_attempted_in_stage153_by_design"], "judgment_label": "stage152_no_full_repair_candidate_not_final", "decision": DECISION, "claim_boundary": BOUNDARY, "next_condition": "Stage154 must try a bounded validation repair on the OOS-mid seed.", "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {"observed_change": "Stage152 margin_trim lifted OOS mid but lost validation, while margin_restore preserved validation but kept OOS DD damage.", "comparison_baseline": "Stage150 margin_restore and Stage152 margin_trim", "likely_drivers": ["margin_block_width", "session_window", "lifecycle_hold", "threshold_guard"], "attribution_confidence": "medium", "next_probe": NEXT_STAGE_ID, "status": "completed"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_AUDIT), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)], "producer": rel(PRODUCER_PATH), "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID], "artifact_paths": [rel(path) for path in [REPORT_PATH, TRADEOFF_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]], "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)], "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"packet_id": PACKET_ID, "run_id": RUN_ID, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "source_stage152_closeout_commit": SOURCE_STAGE152_CLOSEOUT_COMMIT, "source_stage152_hash_record_commit": SOURCE_STAGE152_HASH_RECORD_COMMIT, "required_outputs": {"report": rel(REPORT_PATH), "tradeoff": rel(TRADEOFF_PATH), "failure_memory": rel(FAILURE_MEMORY_PATH), "route_decision": rel(ROUTE_DECISION_PATH), "decision": rel(DECISION_PATH)}, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False},
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def run() -> Mapping[str, Any]:
    review = build_review()
    write_csv(TRADEOFF_PATH, review["tradeoff"])
    write_csv(FAILURE_MEMORY_PATH, review["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, review["route"])
    write_json(SUMMARY_JSON_PATH, review)
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown())
    update_current_truth()
    append_changelog()
    ledger_payload = write_ledgers()
    write_packet_files(ledger_payload)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files({**ledger_payload, "artifact_registry": artifact_payload})
    return review


def main() -> int:
    review = run()
    print(
        json.dumps(
            json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID, "best_oos_mid_seed": review["best_oos_mid_seed"].get("adapter_id")}),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

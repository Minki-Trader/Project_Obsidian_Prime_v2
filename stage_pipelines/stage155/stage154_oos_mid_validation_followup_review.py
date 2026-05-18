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

STAGE_ID = "155_adapter_research__stage154_oos_mid_validation_followup_review"
RUN_ID = "run155A_stage155_stage154_oos_mid_validation_followup_review_v1"
PACKET_ID = "stage155_stage154_oos_mid_validation_followup_review_v1"
SOURCE_STAGE_ID = "154_adapter_research__oos_mid_edge_restore_validation_repair"
SOURCE_RUN_ID = "run154A_stage154_oos_mid_edge_restore_validation_repair_v1"
SOURCE_CLOSEOUT_COMMIT = "200c8ab3510b19d89711d0de5b5ca825b10180c4"
SOURCE_HASH_RECORD_COMMIT = "e6b2f1e2860c1497a287ea4ecd74b536a02dc3f3"
NEXT_STAGE_ID = "156_adapter_research__stage154_low_edge_oos_dd_compression_repair"
NEXT_RUN_ID = "run156A_stage156_stage154_low_edge_oos_dd_compression_repair_v1"
NEXT_PACKET_ID = "stage156_stage154_low_edge_oos_dd_compression_repair_v1"
DECISION = "open_stage156_stage154_low_edge_oos_dd_compression_repair_candidate_not_final"
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
SOURCE_SUMMARY = SOURCE_ROOT / "stage154_oos_mid_validation_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_ROOT / "stage154_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_ROOT / "stage154_risk_atr_telemetry.csv"
SOURCE_REPORT = SOURCE_ROOT / "stage154_oos_mid_validation_repair_report.md"
SOURCE_DECISION = SOURCE_ROOT / "stage154_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage155_stage154_oos_mid_validation_followup_review.md"
KPI_GAP_PATH = REVIEWS_ROOT / "stage155_kpi_gap_summary.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage155_failure_memory.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage155_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage155_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage155_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage155/stage154_oos_mid_validation_followup_review.py")

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


def gap(value: float, target: float, *, lower_is_better: bool = False) -> float:
    if lower_is_better:
        return max(0.0, value - target)
    return max(0.0, target - value)


def build_review() -> dict[str, Any]:
    summary = read_csv(SOURCE_SUMMARY)
    segments = read_csv(SOURCE_SEGMENTS)
    adapters = sorted({row["adapter_id"] for row in summary if row.get("view") == "actual_routed_total"})
    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = split_row(summary, adapter_id, "validation_is")
        oos = split_row(summary, adapter_id, "oos")
        oos_mid = segment_row(segments, adapter_id, "oos", "mid")
        row = {
            "adapter_id": adapter_id,
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trades": as_float(oos.get("trade_count")),
            "oos_mid_pf": as_float(oos_mid.get("profit_factor")),
            "oos_mid_net": as_float(oos_mid.get("net_profit")),
            "gap_vs_34d_pf_oos": gap(as_float(oos.get("profit_factor")), LEGACY_34D["profit_factor"]),
            "gap_vs_34d_net_oos": gap(as_float(oos.get("net_profit")), LEGACY_34D["net_profit"]),
            "excess_vs_34d_dd_oos": gap(as_float(oos.get("max_drawdown_percent")), LEGACY_34D["max_drawdown_percent"], lower_is_better=True),
            "gap_vs_34d_oos_mid_pf": gap(as_float(oos_mid.get("profit_factor")), LEGACY_34D["profit_factor"]),
            "gap_vs_34d_validation_pf": gap(as_float(val.get("profit_factor")), LEGACY_34D["profit_factor"]),
            "strict_34d_kpi_pass": False,
        }
        row["strict_34d_kpi_pass"] = (
            row["gap_vs_34d_pf_oos"] == 0
            and row["gap_vs_34d_net_oos"] == 0
            and row["excess_vs_34d_dd_oos"] == 0
            and row["gap_vs_34d_oos_mid_pf"] == 0
            and row["gap_vs_34d_validation_pf"] == 0
        )
        if row["adapter_id"] == "s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035":
            label = "best_stage154_seed_oos_dd_above_34d"
            next_use = "use_as_stage156_dd_compression_seed"
        elif row["excess_vs_34d_dd_oos"] > 0:
            label = "oos_dd_or_balance_failed"
            next_use = "preserve_as_failure_memory"
        else:
            label = "profit_or_validation_tradeoff_failed"
            next_use = "preserve_as_control_memory"
        row["stage155_label"] = label
        rows.append(row)
        failures.append(
            {
                "adapter_id": adapter_id,
                "stage155_label": label,
                "next_use": next_use,
                "oos_dd_excess_vs_34d": row["excess_vs_34d_dd_oos"],
                "validation_pf_gap_vs_34d": row["gap_vs_34d_validation_pf"],
                "oos_mid_pf_gap_vs_34d": row["gap_vs_34d_oos_mid_pf"],
                "overall_goal_complete": False,
            }
        )
    best = max(rows, key=lambda r: (r["oos_pf"], r["oos_net"], r["oos_mid_pf"], -r["oos_dd_percent"])) if rows else {}
    route = [
        {
            "decision": DECISION,
            "reason": "stage154_low_edge_is_best_but_oos_dd_13_77_exceeds_34d_12_909136_and_validation_pf_is_slightly_below_34d",
            "next_stage": NEXT_STAGE_ID,
            "next_seed": best.get("adapter_id", "s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035"),
            "next_axis": "compress_oos_drawdown_without_losing_validation_net_oos_pf_oos_net_or_oos_mid_pf",
            "do_not_repeat": "do_not_accept_high_oos_pf_if_oos_dd_stays_above_legacy_34d_target",
            "overall_goal_complete": False,
        }
    ]
    return {
        "best_adapter": best,
        "decision": DECISION,
        "failure_memory": failures,
        "kpi_gap_rows": rows,
        "legacy_34d": LEGACY_34D,
        "overall_goal_complete": False,
        "route_decision": route,
    }


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS mid PF(표본외 중반 수익 팩터) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_mid_pf:.9f} | {stage155_label} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(review: Mapping[str, Any]) -> str:
    best = review["best_adapter"]
    return f"""# Stage155 Stage154 Follow-up Review(155단계 154단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_closeout_commit(원천 종료 커밋): `{SOURCE_CLOSEOUT_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

No(아니오). Stage154(154단계)는 best seed(최선 씨앗)를 찾았지만 full 34D KPI gate(전체 34D 핵심 성과 지표 문턱)를 통과하지 못했다.

Effect(효과): 좋은 OOS PF(표본외 수익 팩터)와 net(순손익)을 final(최종)로 착각하지 않고, DD(낙폭) 압축만 다음 Stage156(156단계)로 분리한다.

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(review["kpi_gap_rows"])}

## Key Judgment(핵심 판정)

- best_adapter(최선 어댑터): `{best.get("adapter_id", "none")}`
- OOS PF(표본외 수익 팩터): `{as_float(best.get("oos_pf")):.6f}` vs 34D target(34D 목표) `{LEGACY_34D["profit_factor"]:.6f}`
- OOS net(표본외 순손익): `{as_float(best.get("oos_net")):.2f}` vs 34D target(34D 목표) `{LEGACY_34D["net_profit"]:.2f}`
- OOS DD(표본외 낙폭): `{as_float(best.get("oos_dd_percent")):.2f}` vs 34D target(34D 목표) `{LEGACY_34D["max_drawdown_percent"]:.6f}`
- OOS mid PF(표본외 중반 수익 팩터): `{as_float(best.get("oos_mid_pf")):.9f}` vs 34D target(34D 목표) `{LEGACY_34D["profit_factor"]:.6f}`

Stage155(155단계)는 review-only(검토 전용)이다. Effect(효과): 새 최적화나 새 MT5(메타트레이더5) 실행을 흡수하지 않고 Stage156(156단계) repair(수리) 질문을 좁힌다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage155 Decision(155단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- source_segments(원천 구간): `{rel(SOURCE_SEGMENTS)}`
- review_report(검토 보고서): `{rel(REPORT_PATH)}`
- kpi_gap_summary(KPI 차이 요약): `{rel(KPI_GAP_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage155(155단계)는 review-only(검토 전용)로 닫는다. Effect(효과): Stage154(154단계)의 강점은 보존하고, OOS DD(표본외 낙폭) 초과를 Stage156(156단계)로 넘긴다.

overall_goal_complete(전체 목표 완료): `false`
"""


def write_stage156_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage156(156단계)는 Stage154 low-edge seed(154단계 낮은 가장자리 씨앗)의 OOS DD(표본외 낙폭)만 좁게 압축한다.

## Bounded Question(경계 질문)

Can `s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035` reduce OOS DD(표본외 낙폭) from `13.77` to at or below 34D target(34D 목표) `12.909136` without losing OOS PF(표본외 수익 팩터), OOS net(표본외 순손익), OOS mid PF(표본외 중반 수익 팩터), validation PF/net(검증 수익 팩터/순손익), or ATR/risk telemetry(ATR/위험 기록)?

Effect(효과): DD(낙폭) 하나를 고치려다 좋은 수익 구조를 망가뜨리는지 분리해서 본다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage156 Input References(156단계 입력 참조)

- stage155_decision(155단계 판정): `{rel(DECISION_PATH)}`
- stage155_review(155단계 검토): `{rel(REPORT_PATH)}`
- stage155_kpi_gap_summary(155단계 KPI 차이 요약): `{rel(KPI_GAP_PATH)}`
- source_stage154_summary(원천 154단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage154_segments(원천 154단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage154_risk_atr(원천 154단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- primary_seed(주 씨앗): `s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035`
- target_axis(목표 축): `oos_dd_compression_without_profit_or_mid_pf_damage`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage156 Review Index(156단계 검토 색인)

- status(상태): `open_planned_from_stage155`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage156(156단계) repair(수리) 산출물을 한 곳에서 추적한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage156 Selection Status(156단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage155`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage156(156단계)는 OOS DD(표본외 낙폭) 압축 실험만 흡수한다.
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?ms)\nstage155_stage154_oos_mid_validation_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage156_stage154_low_edge_oos_dd_compression_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\n\n  packet_id: stage155_stage154_oos_mid_validation_followup_review_v1.*?boundary: research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment\n", "\n", state)
    state = re.sub(r"(?ms)\n\n  packet_id: stage156_stage154_low_edge_oos_dd_compression_repair_v1.*?boundary: research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment\n", "\n", state)
    block = f"""
stage155_stage154_oos_mid_validation_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage154_closeout_commit: {SOURCE_CLOSEOUT_COMMIT}
  source_stage154_hash_record_commit: {SOURCE_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage156_stage154_low_edge_oos_dd_compression_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage155
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
- adapter_under_review(검토 중 어댑터): `s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035`
- status(상태): `stage155_closed_review_only_stage156_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage155(155단계)는 Stage154(154단계)의 KPI(핵심 성과 지표)를 review-only(검토 전용)로 판정했다. Effect(효과): Stage154(154단계)의 best seed(최선 씨앗)는 보존하되, OOS DD(표본외 낙폭) 초과 때문에 전체 목표 완료를 주장하지 않는다.

## Latest Stage155 Evidence(최신 155단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- kpi_gap_summary(KPI 차이 요약): `{rel(KPI_GAP_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage155 Selection Status(155단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- stage155_decision(155단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage155(155단계)는 Stage154(154단계)의 미달 KPI(핵심 성과 지표)를 숨기지 않고 Stage156(156단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage155 Review Index(155단계 검토 색인)

- status(상태): `closed_review_only`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- kpi_gap_summary(KPI 차이 요약): `{rel(KPI_GAP_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage155(155단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage155 Stage154 follow-up review closeout(155단계 154단계 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage154(154단계)의 best seed(최선 씨앗)를 Stage156(156단계) OOS DD(표본외 낙폭) 압축으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, KPI_GAP_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage155_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage155 review-only Stage154 KPI follow-up artifact.",
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
                "lane": "baseline_adapter_stage155_stage154_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("source_closeout_commit", SOURCE_CLOSEOUT_COMMIT), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0))),
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
        "kpi_scope": "validation_oos_segment_kpi",
        "scoreboard_lane": "baseline_adapter_stage155",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": "best_stage154_low_edge_oos_pf=1.84;oos_net=1321.77;oos_dd=13.77;oos_mid_pf=1.662173615",
        "guardrail_kpi": "legacy_34d_oos_dd_target=12.909136;overall_goal_complete=false",
        "external_verification_status": "completed_from_stage154_evidence",
        "notes": ledger_pairs((("source_summary", rel(SOURCE_SUMMARY)), ("overall_goal_complete", 0))),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(ledger_payload: Mapping[str, Any]) -> None:
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
            "kpi_gap_summary": rel(KPI_GAP_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "judgment_label": "stage154_best_seed_candidate_not_final_due_to_oos_dd_excess",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage154 low-edge restore improved OOS PF/net and OOS mid PF, but OOS DD remained above the 34D target.",
            "likely_driver": "low-edge margin restoration increased opportunity quality but did not sufficiently cap adverse OOS excursions.",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_REPORT), rel(SOURCE_DECISION)],
            "producer": rel(PRODUCER_PATH),
            "artifact_paths": [rel(path) for path in [REPORT_PATH, KPI_GAP_PATH, FAILURE_MEMORY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]],
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
            "source_stage154_closeout_commit": SOURCE_CLOSEOUT_COMMIT,
            "source_stage154_hash_record_commit": SOURCE_HASH_RECORD_COMMIT,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "kpi_gap_summary": rel(KPI_GAP_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "route_decision": rel(ROUTE_DECISION_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def run() -> Mapping[str, Any]:
    review = build_review()
    write_csv(KPI_GAP_PATH, review["kpi_gap_rows"])
    write_csv(FAILURE_MEMORY_PATH, review["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, review["route_decision"])
    write_json(SUMMARY_JSON_PATH, review)
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown())
    write_status_files()
    write_stage156_seed()
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
            json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID, "best_adapter": review["best_adapter"].get("adapter_id")}),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

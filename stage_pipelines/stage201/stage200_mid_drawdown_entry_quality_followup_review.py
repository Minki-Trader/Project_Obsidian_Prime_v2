from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage200 import mid_drawdown_entry_quality_repair as s200  # noqa: E402

s172 = s200.s172

STAGE_ID = "201_adapter_research__stage200_mid_drawdown_entry_quality_followup_review"
RUN_ID = "run201A_stage201_stage200_mid_drawdown_entry_quality_followup_review_v1"
PACKET_ID = "stage201_stage200_mid_drawdown_entry_quality_followup_review_v1"
PARENT_RUN_ID = "run200A_stage200_stage198_mid_drawdown_entry_quality_repair_v1"
SOURCE_STAGE_ID = "200_adapter_research__stage198_mid_drawdown_entry_quality_repair"
SOURCE_RUN_ID = "run200A_stage200_stage198_mid_drawdown_entry_quality_repair_v1"
SOURCE_STAGE200_EVIDENCE_COMMIT = "d1bee8df4f8900295da896f6dbb8284797545a16"
SOURCE_STAGE200_HASH_RECORD_COMMIT = "37309e423eeb897530bb562c253f0d091a5a2aea"
NEXT_STAGE_ID = "202_adapter_research__stage200_probability_binding_repair"
NEXT_RUN_ID = "run202A_stage202_stage200_probability_binding_repair_v1"
NEXT_PACKET_ID = "stage202_stage200_probability_binding_repair_v1"
DECISION = "open_stage202_bounded_probability_binding_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage200_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_probability_binding_repair"
BOUNDARY = s200.BOUNDARY
LEGACY_34D = s200.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_quality_matrix.csv")
SOURCE_SEGMENT_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_risk_atr_telemetry.csv")
SOURCE_PROBABILITY_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_probability_binding_summary.csv")
SOURCE_REPORT_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_mid_drawdown_entry_quality_report.md")
SOURCE_DECISION_PATH = Path("stages/200_adapter_research__stage198_mid_drawdown_entry_quality_repair/03_reviews/stage200_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage201_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage201_mid_drawdown_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage201_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage201_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage201_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage201/stage200_mid_drawdown_entry_quality_followup_review.py")


def rel(path: Path | str) -> str:
    return s172.rel(path)


def fnum(value: Any, default: float = 0.0) -> float:
    return s172.parse_float(value, default)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    inferred: list[str] = []
    for row in rows:
        for key in row:
            if key not in inferred:
                inferred.append(key)
    fieldnames = list(columns or inferred)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in fieldnames})


def by_adapter(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("adapter_id")): row for row in rows}


def segment_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
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


def probability_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def stage201_read(adapter_id: str, row: Mapping[str, Any]) -> str:
    if adapter_id == "s200_cd8_ref_r0325":
        return "best_reference_still_dd_midpf_gap(최선 기준이나 낙폭/중반 수익요인 격차 유지)"
    if adapter_id == "s200_cd8_thr55_r0325":
        return "threshold_lift_nonbinding_no_change(문턱값 상향 비구속 변화 없음)"
    if adapter_id in {"s200_cd8_qwide_r0325", "s200_cd8_qwide_thr55_r0325"}:
        return "qwide_gate_overfilters_net_oos_damage(넓은 제한문 과필터로 순손익/표본외 손상)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ref = by_adapter(quality_rows).get("s200_cd8_ref_r0325", {})
    ref_net = fnum(ref.get("validation_net"))
    ref_dd = fnum(ref.get("validation_balance_dd_percent"))
    ref_mid = fnum(ref.get("validation_mid_pf"))
    ref_oos_net = fnum(ref.get("oos_net"))
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        mid = segment_lookup(segment_rows, adapter_id, "validation_is", "mid")
        late = segment_lookup(segment_rows, adapter_id, "validation_is", "late")
        prob = probability_lookup(probability_rows, adapter_id, "validation_is")
        val_net = fnum(row.get("validation_net"))
        val_dd = fnum(row.get("validation_balance_dd_percent"))
        val_mid = fnum(row.get("validation_mid_pf"))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": round(val_net - LEGACY_34D["net_profit"], 6),
                "validation_net_delta_vs_ref": round(val_net - ref_net, 6),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_gap_above_34d": round(val_dd - LEGACY_34D["max_drawdown_percent"], 6),
                "validation_dd_delta_vs_ref": round(val_dd - ref_dd, 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d_pf": round(val_mid - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf_delta_vs_ref": round(val_mid - ref_mid, 6),
                "validation_mid_net": mid.get("net_profit", ""),
                "validation_mid_mfe_capture": mid.get("mfe_capture_ratio", ""),
                "validation_mid_max_closed_trade_drawdown": mid.get("max_closed_trade_drawdown", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_late_net": late.get("net_profit", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_ref": round(fnum(row.get("oos_net")) - ref_oos_net, 6),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "short_threshold": prob.get("short_threshold", ""),
                "long_threshold": prob.get("long_threshold", ""),
                "directional_threshold_pass_rows": prob.get("directional_threshold_pass_rows", ""),
                "threshold_or_margin_not_met_rows": prob.get("threshold_or_margin_not_met_rows", ""),
                "order_attempted_rows": prob.get("order_attempted_rows", ""),
                "order_filled_rows": prob.get("order_filled_rows", ""),
                "decision_counts": prob.get("decision_counts", ""),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage201_read": stage201_read(adapter_id, row),
            }
        )
    return rows


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = by_adapter(tradeoff_rows)
    ref = rows.get("s200_cd8_ref_r0325", {})
    thr = rows.get("s200_cd8_thr55_r0325", {})
    qwide = rows.get("s200_cd8_qwide_r0325", {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "Threshold lift(문턱값 상향) from 0.54/0.52 to 0.55/0.53 produced identical KPI(동일 핵심 성과 지표).",
            "comparison_baseline": "s200_cd8_ref_r0325 reference(기준)",
            "trade_shape": f"ref net={ref.get('validation_net')}, DD={ref.get('validation_dd_percent')}, midPF={ref.get('validation_mid_pf')}; thr net={thr.get('validation_net')}, DD={thr.get('validation_dd_percent')}, midPF={thr.get('validation_mid_pf')}",
            "likely_drivers": "Probability outputs(확률 출력)이 two-value/plateau shape(두 값/평탄 형태)라 threshold(문턱값)이 실제 decision boundary(결정 경계)를 바꾸지 못했다.",
            "next_probe": "Stage202(202단계)는 threshold-only(문턱값만 조정)를 금지하고 binding-aware score/margin gate(구속 인식 점수/마진 제한문)를 시험한다.",
            "attribution_confidence": "high(높음)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "qwide gate(넓은 품질 제한문)는 trade count(거래 수)를 줄였지만 validation net/OOS(검증 순손익/표본외)를 훼손했다.",
            "comparison_baseline": "s200_cd8_ref_r0325 reference(기준)",
            "trade_shape": f"qwide net={qwide.get('validation_net')}, DD={qwide.get('validation_dd_percent')}, midPF={qwide.get('validation_mid_pf')}, OOS net={qwide.get('oos_net')}",
            "likely_drivers": "Broad context blocking(넓은 문맥 차단)이 weak trades(약한 거래)만이 아니라 profitable recovery trades(회복 수익 거래)도 제거했다.",
            "next_probe": "Do not widen the context gate(문맥 제한문 확대 금지) unless a bounded repair can preserve recovery trades(회복 거래).",
            "attribution_confidence": "medium_high(중상)",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage202_primary(202단계 주 경로)",
            "decision": DECISION,
            "source_clue": "threshold_nonbinding_and_qwide_damage(문턱값 비구속 및 넓은 제한문 손상)",
            "bounded_question": "Can a binding-aware score/margin or transition gate(구속 인식 점수/마진 또는 전환 제한문) change trades without broad qwide damage(넓은 제한문 손상)?",
            "why": "Stage200(200단계) showed numeric thresholds do not bind and broad context filtering damages edge.",
            "guardrail": "no_threshold_only(문턱값만 금지); no_qwide_only(넓은 제한문만 금지); preserve_ref_net_oos(기준 순손익/표본외 보존)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "s200_cd8_qwide_r0325 overfilter(과필터)",
            "bounded_question": "Do not accept trade-count reduction(거래 수 감소) as quality improvement(품질 개선) by itself.",
            "why": "qwide reduced trades but worsened validation net, mid PF, and OOS drawdown.",
            "guardrail": "trade_reduction_not_sufficient(거래 감소는 충분조건 아님)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage201 Follow-up Review(201단계 후속 검토)",
        "",
        f"- decision(판정): `{DECISION}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Stage201(201단계)는 Stage200(200단계) 결과를 review-only(검토 전용)로 판독했다. Effect(효과): threshold lift(문턱값 상향)가 실제로 안 먹힌 원인과 qwide gate(넓은 제한문)의 손상을 다음 bounded repair(경계 수리) 질문으로 분리한다.",
        "",
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row['adapter_id']} | {row['validation_pf']} | {row['validation_net']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_pf']} | {row['stage201_read']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- `s200_cd8_ref_r0325` remains best reference(최선 기준) but DD/midPF(낙폭/중반 수익요인) still fail.",
            "- `s200_cd8_thr55_r0325` is a no-op(무효 변화) because the probability/decision telemetry(확률/결정 기록) is identical to reference(기준).",
            "- `s200_cd8_qwide_r0325` and `s200_cd8_qwide_thr55_r0325` are failure memory(실패 기억): they reduce trade supply(거래 공급) but damage net/OOS(순손익/표본외).",
            f"- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`.",
            "- Stage201(201단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.",
        ]
    )
    return "\n".join(lines)


def decision_md() -> str:
    return f"""# Stage201 Decision(201단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage200_evidence_commit(원천 200단계 근거 커밋): `{SOURCE_STAGE200_EVIDENCE_COMMIT}`
- source_stage200_hash_record_commit(원천 200단계 해시 기록 커밋): `{SOURCE_STAGE200_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage201(201단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage202(202단계)에서 probability binding(확률 구속)을 실제로 바꾸는 수리만 좁게 진행한다.
"""


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    ref = by_adapter(tradeoff_rows).get("s200_cd8_ref_r0325", {})
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage200_mid_drawdown_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage200_mid_drawdown_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage200_mid_drawdown_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_reference=s200_cd8_ref_r0325;validation_net={ref.get('validation_net')};validation_dd={ref.get('validation_dd_percent')};mid_pf={ref.get('validation_mid_pf')};oos_pf={ref.get('oos_pf')}",
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage201 reviewed Stage200 threshold non-binding and qwide damage, then opened Stage202 binding-aware repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage201_stage200_mid_drawdown_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage200_evidence_commit", SOURCE_STAGE200_EVIDENCE_COMMIT),
                ("source_stage200_hash_record_commit", SOURCE_STAGE200_HASH_RECORD_COMMIT),
                ("target_surface", TARGET_SURFACE),
                ("overall_goal_complete", 0),
            )
        ),
    }
    write_csv(STAGE_LEDGER_PATH, [ledger_row], columns=s172.ALPHA_LEDGER_COLUMNS)
    upsert_csv_rows(RUN_REGISTRY_PATH, s172.RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, s172.ALPHA_LEDGER_COLUMNS, [ledger_row], key="ledger_row_id")


def artifact_rows() -> list[dict[str, Any]]:
    paths = [
        (PRODUCER_PATH, "Stage201 follow-up review producer script(생산 스크립트)."),
        (REPORT_PATH, "Stage201 bounded follow-up review report(경계 후속 검토 보고서)."),
        (TRADEOFF_MATRIX_PATH, "Stage201 mid drawdown tradeoff matrix(중반 낙폭 상충 행렬)."),
        (ATTRIBUTION_PATH, "Stage201 performance attribution(성과 원인 분해)."),
        (ROUTE_MATRIX_PATH, "Stage201 route matrix(경로 행렬)."),
        (DECISION_PATH, "Stage201 decision(판정)."),
        (STAGE_LEDGER_PATH, "Stage201 local ledger(단계 장부)."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage201_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": note,
        }
        for path, note in paths
    ]


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "external_verification_status": EXTERNAL_STATUS,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
        "attribution": rel(ATTRIBUTION_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "tradeoff_rows": list(tradeoff_rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    s172.write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    s172.write_json(PACKET_ROOT / "packet_receipt.json", payload)
    s172.write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage201 Closeout Packet(201단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage202(202단계)은 Stage201(201단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a binding-aware probability or margin gate(구속 인식 확률 또는 마진 제한문) actually change trades(거래를 실제로 바꿈) and improve validation mid PF/DD(검증 중반 수익요인/낙폭) without broad qwide damage(넓은 제한문 손상) to validation net/OOS(검증 순손익/표본외)?

Effect(효과): threshold-only(문턱값만 조정) no-op(무효 변화)와 qwide overfilter(넓은 제한문 과필터)를 피하고, 실제 decision boundary(결정 경계)를 바꾸는 좁은 수리를 한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage202 Input References(202단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_attribution(원천 성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- source_route_matrix(원천 경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage200_quality_matrix(원천 200단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage200_probability_binding(원천 200단계 확률 구속): `{rel(SOURCE_PROBABILITY_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage202 Review Index(202단계 검토 색인)

- status(상태): `open_planned_from_stage201`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage202 Selection Status(202단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage201`
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
  Stage201(201단계) closed(종료) as `{DECISION}` and Stage202(202단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): threshold-only(문턱값만 조정) no-op(무효 변화)와 qwide overfilter(넓은 제한문 과필터)를 피하고 probability binding(확률 구속) 수리로 넘어간다.
- >-
  Stage201 evidence(201단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): trade reduction(거래 감소) 자체를 품질 개선으로 오해하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage201_stage200_mid_drawdown_entry_quality_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage201_stage200_mid_drawdown_entry_quality_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_MATRIX_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    s172.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage201_stage200_mid_drawdown_entry_quality_followup_review`
- status(상태): `stage201_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage201(201단계)는 Stage200(200단계) mid drawdown entry quality repair(중반 낙폭 진입 품질 수리)를 follow-up review(후속 검토)했다. Effect(효과): Stage202(202단계)은 probability binding(확률 구속)을 실제로 바꾸는 수리를 좁게 진행한다.

## Latest Stage201 Evidence(최신 201단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage201 Selection Status(201단계 선택 상태)

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
""",
    )
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage201 Review Index(201단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage201 Stage200 mid drawdown follow-up review closeout(201단계 200단계 중반 낙폭 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): threshold non-binding(문턱값 비구속)과 qwide overfilter(넓은 제한문 과필터)를 분리하고 Stage202(202단계) probability binding repair(확률 구속 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    probability_rows = read_csv(SOURCE_PROBABILITY_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, probability_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows()
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows))
    s172.write_md(DECISION_PATH, decision_md())
    write_ledgers(tradeoff_rows)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, s172.ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows)
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
                    "external_verification_status": EXTERNAL_STATUS,
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "tradeoff_matrix": rel(TRADEOFF_MATRIX_PATH),
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

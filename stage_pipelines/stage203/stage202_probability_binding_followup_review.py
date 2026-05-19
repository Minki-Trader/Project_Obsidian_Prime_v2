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
from stage_pipelines.stage202 import probability_binding_repair as s202  # noqa: E402

s172 = s202.s172

STAGE_ID = "203_adapter_research__stage202_probability_binding_followup_review"
RUN_ID = "run203A_stage203_stage202_probability_binding_followup_review_v1"
PACKET_ID = "stage203_stage202_probability_binding_followup_review_v1"
PARENT_RUN_ID = "run202A_stage202_stage200_probability_binding_repair_v1"
SOURCE_STAGE_ID = "202_adapter_research__stage200_probability_binding_repair"
SOURCE_RUN_ID = "run202A_stage202_stage200_probability_binding_repair_v1"
SOURCE_STAGE202_EVIDENCE_COMMIT = "9d8c3e04d626d5cb2b9408c429886ede799ead63"
SOURCE_STAGE202_HASH_RECORD_COMMIT = "61e750e9e259244cc78618b93b314fbcd1d742b2"
NEXT_STAGE_ID = "204_adapter_research__selective_probability_margin_recovery_repair"
NEXT_RUN_ID = "run204A_stage204_selective_probability_margin_recovery_repair_v1"
NEXT_PACKET_ID = "stage204_selective_probability_margin_recovery_repair_v1"
DECISION = "open_stage204_selective_probability_margin_recovery_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage202_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_selective_probability_margin_repair"
BOUNDARY = s202.BOUNDARY
LEGACY_34D = s202.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_quality_matrix.csv")
SOURCE_KPI_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_probability_binding_kpi_summary.csv")
SOURCE_SEGMENT_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_risk_atr_telemetry.csv")
SOURCE_PROBABILITY_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_probability_binding_telemetry_summary.csv")
SOURCE_REPORT_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_probability_binding_report.md")
SOURCE_DECISION_PATH = Path("stages/202_adapter_research__stage200_probability_binding_repair/03_reviews/stage202_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage203_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage203_probability_binding_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage203_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage203_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage203_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage203_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage203/stage202_probability_binding_followup_review.py")


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


def kpi_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


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


def stage203_read(adapter_id: str) -> str:
    if adapter_id == "s202_cd8_ref_r0325":
        return "reference_retained_but_dd_midpf_gap(기준 유지, 낙폭/중반 수익요인 격차)"
    if adapter_id == "s202_cd8_shortcut_r0325":
        return "short_side_cut_rejected_net_oos_damage(숏 방향 차단 기각, 순손익/표본외 손상)"
    if adapter_id == "s202_cd8_longcut_r0325":
        return "long_side_cut_is_repair_clue_not_solution(롱 방향 차단은 수리 단서, 해답 아님)"
    if adapter_id == "s202_cd8_bothcut_r0325":
        return "binding_proof_no_trade_control(구속 증명용 무거래 대조군)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ref = by_adapter(quality_rows).get("s202_cd8_ref_r0325", {})
    ref_net = fnum(ref.get("validation_net"))
    ref_dd = fnum(ref.get("validation_balance_dd_percent"))
    ref_mid = fnum(ref.get("validation_mid_pf"))
    ref_oos_net = fnum(ref.get("oos_net"))
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_kpi = kpi_lookup(kpi_rows, adapter_id, "validation_is")
        oos_kpi = kpi_lookup(kpi_rows, adapter_id, "oos")
        mid = segment_lookup(segment_rows, adapter_id, "validation_is", "mid")
        prob = probability_lookup(probability_rows, adapter_id, "validation_is")
        val_net = fnum(row.get("validation_net"))
        val_dd = fnum(row.get("validation_balance_dd_percent"))
        val_mid = fnum(row.get("validation_mid_pf"))
        oos_net = fnum(row.get("oos_net"))
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
                "validation_dd_gap_vs_34d": round(val_dd - LEGACY_34D["max_drawdown_percent"], 6),
                "validation_dd_delta_vs_ref": round(val_dd - ref_dd, 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d_pf": round(val_mid - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf_delta_vs_ref": round(val_mid - ref_mid, 6),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_ref": round(oos_net - ref_oos_net, 6),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "validation_trade_count": val_kpi.get("trade_count", ""),
                "oos_trade_count": oos_kpi.get("trade_count", ""),
                "validation_mid_net": mid.get("net_profit", ""),
                "validation_mid_mfe_capture": mid.get("mfe_capture_ratio", ""),
                "short_threshold": prob.get("short_threshold", ""),
                "long_threshold": prob.get("long_threshold", ""),
                "directional_threshold_pass_rows": prob.get("directional_threshold_pass_rows", ""),
                "order_filled_rows": prob.get("order_filled_rows", ""),
                "decision_counts": prob.get("decision_counts", ""),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage203_read": stage203_read(adapter_id),
            }
        )
    return rows


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = by_adapter(tradeoff_rows)
    ref = rows.get("s202_cd8_ref_r0325", {})
    shortcut = rows.get("s202_cd8_shortcut_r0325", {})
    longcut = rows.get("s202_cd8_longcut_r0325", {})
    bothcut = rows.get("s202_cd8_bothcut_r0325", {})
    return [
        {
            "run_id": RUN_ID,
            "finding": "reference_still_best_total_package(기준이 아직 전체 패키지 최선)",
            "evidence": f"ref val_net={ref.get('validation_net')}, val_dd={ref.get('validation_dd_percent')}, mid_pf={ref.get('validation_mid_pf')}, oos_net={ref.get('oos_net')}",
            "meaning": "High net/OOS(높은 순손익/표본외)은 유지되지만 DD/midPF(낙폭/중반 수익요인)는 34D(34D)보다 약하다.",
            "next_use": "Stage204(204단계)는 ref(기준)를 버리지 않고 작은 selective repair(선별 수리)를 붙인다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "short_cut_is_too_blunt(숏 차단은 너무 둔함)",
            "evidence": f"shortcut val_dd={shortcut.get('validation_dd_percent')} but val_net={shortcut.get('validation_net')} and oos_net={shortcut.get('oos_net')}",
            "meaning": "DD(낙폭)는 좋아지지만 profit engine(수익 엔진)을 크게 자른다.",
            "next_use": "Stage204(204단계)에서 side-wide short cut(방향 전체 숏 차단)은 금지한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "long_cut_has_repair_clue(롱 차단은 수리 단서가 있음)",
            "evidence": f"longcut val_dd={longcut.get('validation_dd_percent')}, val_net={longcut.get('validation_net')}, mid_pf={longcut.get('validation_mid_pf')}, oos_net={longcut.get('oos_net')}",
            "meaning": "DD(낙폭)는 34D(34D)보다 좋아지지만 net/OOS(순손익/표본외) 손상이 아직 크다.",
            "next_use": "Stage204(204단계)는 long-side harmful context(롱 방향 해로운 문맥)만 좁게 찾는다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "both_cut_confirms_binding(양방향 차단은 구속 확인)",
            "evidence": f"bothcut val_net={bothcut.get('validation_net')}, trade_count={bothcut.get('validation_trade_count')}",
            "meaning": "0.58/0.58 threshold(문턱값)는 실제로 no-trade(무거래)를 만들 만큼 binding(구속)된다.",
            "next_use": "Stage204(204단계)는 threshold-only(문턱값 단독)가 아니라 context/score(문맥/점수)를 같이 써야 한다.",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage204_selective_probability_margin_recovery_repair(204단계 선별 확률/마진 회복 수리)",
            "decision": DECISION,
            "source_clue": "longcut_dd_improves_but_net_oos_damage(롱 차단은 낙폭 개선, 순손익/표본외 손상)",
            "bounded_question": "Can a selective probability/margin repair(선별 확률/마진 수리) reduce DD(낙폭) and lift mid PF(중반 수익요인) without side-wide net/OOS damage(방향 전체 순손익/표본외 손상)?",
            "guardrail": "no_side_wide_cut(방향 전체 차단 금지); no_no_trade_solution(무거래 해답 금지); preserve_ref_net_oos(기준 순손익/표본외 보존)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "shortcut_and_bothcut_overreduce_trade_supply(숏 차단/양방향 차단은 거래 공급 과감소)",
            "bounded_question": "Do not accept lower DD(낮은 낙폭) when net/OOS(순손익/표본외) is destroyed.",
            "guardrail": "DD improvement is necessary but not sufficient(낙폭 개선은 필요하지만 충분하지 않음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage203 Follow-up Review(203단계 후속 검토)",
        "",
        f"- decision(판정): `{DECISION}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage202_evidence_commit(원천 202단계 근거 커밋): `{SOURCE_STAGE202_EVIDENCE_COMMIT}`",
        f"- source_stage202_hash_record_commit(원천 202단계 해시 기록 커밋): `{SOURCE_STAGE202_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Stage203(203단계)는 review-only(검토 전용)다. Effect(효과): Stage202(202단계)의 probability binding(확률 구속) 결과를 추가 튜닝 없이 판정하고 Stage204(204단계) 수리 질문을 좁힌다.",
        "",
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row['adapter_id']} | {row['validation_pf']} | {row['validation_net']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['stage203_read']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- `s202_cd8_ref_r0325` keeps the best total package(전체 패키지 최선 유지)이지만 DD/midPF(낙폭/중반 수익요인)는 아직 34D(34D)에 못 미친다.",
            "- `s202_cd8_shortcut_r0325`는 DD(낙폭)를 줄였지만 net/OOS(순손익/표본외)를 크게 손상해 기각한다.",
            "- `s202_cd8_longcut_r0325`는 DD(낙폭) 개선 단서가 있지만 net/OOS(순손익/표본외) 손상이 커서 그대로 채택하지 않는다.",
            "- `s202_cd8_bothcut_r0325`는 binding proof(구속 증명)일 뿐이며 전략 후보가 아니다.",
            f"- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`.",
            "- Stage203(203단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.",
        ]
    )
    return "\n".join(lines)


def decision_md() -> str:
    return f"""# Stage203 Decision(203단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage202_evidence_commit(원천 202단계 근거 커밋): `{SOURCE_STAGE202_EVIDENCE_COMMIT}`
- source_stage202_hash_record_commit(원천 202단계 해시 기록 커밋): `{SOURCE_STAGE202_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage203(203단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage204(204단계)에서 side-wide cut(방향 전체 차단)이 아니라 selective probability/margin repair(선별 확률/마진 수리)를 좁게 진행한다.
"""


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    ref = by_adapter(tradeoff_rows).get("s202_cd8_ref_r0325", {})
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage202_probability_binding_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage202_probability_binding_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage202_probability_binding_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_reference=s202_cd8_ref_r0325;validation_net={ref.get('validation_net')};validation_dd={ref.get('validation_dd_percent')};mid_pf={ref.get('validation_mid_pf')};oos_net={ref.get('oos_net')}",
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage203 reviewed Stage202 probability binding tradeoff and opened Stage204 selective repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage203_stage202_probability_binding_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage202_evidence_commit", SOURCE_STAGE202_EVIDENCE_COMMIT),
                ("source_stage202_hash_record_commit", SOURCE_STAGE202_HASH_RECORD_COMMIT),
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
        (PRODUCER_PATH, "Stage203 follow-up review producer script(생산 스크립트)."),
        (REPORT_PATH, "Stage203 bounded follow-up review report(경계 후속 검토 보고서)."),
        (TRADEOFF_MATRIX_PATH, "Stage203 probability binding tradeoff matrix(확률 구속 상충 행렬)."),
        (ATTRIBUTION_PATH, "Stage203 performance attribution(성과 원인 분해)."),
        (ROUTE_MATRIX_PATH, "Stage203 route matrix(경로 행렬)."),
        (SUMMARY_JSON_PATH, "Stage203 summary JSON(요약 JSON)."),
        (DECISION_PATH, "Stage203 decision(판정)."),
        (STAGE_LEDGER_PATH, "Stage203 local ledger(단계 장부)."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage203_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": note,
        }
        for path, note in paths
    ]


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> None:
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
        f"""# Stage203 Closeout Packet(203단계 종료 작업 묶음)

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

Stage204(204단계)는 Stage203(203단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can selective probability/margin repair(선별 확률/마진 수리) reduce validation DD(검증 낙폭), lift validation mid PF(검증 중반 수익요인), and preserve validation/OOS net(검증/표본외 순손익) better than side-wide cuts(방향 전체 차단)?

Effect(효과): Stage202(202단계)의 longcut clue(롱 차단 단서)는 쓰되, long side(롱 방향) 전체를 자르는 방식은 피한다.

## Constraints(제약)

- no side-wide cut(방향 전체 차단 금지)
- no no-trade solution(무거래 해답 금지)
- no qwide-only broad filter(qwide 단독 넓은 제한문 금지)
- preserve reference net/OOS(기준 순손익/표본외 보존)
- target 34D-level DD and mid PF(34D급 낙폭과 중반 수익요인 목표)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage204 Input References(204단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_attribution(원천 성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- source_route_matrix(원천 경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage202_quality_matrix(원천 202단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage202_probability_telemetry(원천 202단계 확률 기록): `{rel(SOURCE_PROBABILITY_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage204 Review Index(204단계 검토 색인)

- status(상태): `open_planned_from_stage203`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage204 Selection Status(204단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage203`
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
  Stage203(203단계) closed(종료) as `{DECISION}` and Stage204(204단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): side-wide cut(방향 전체 차단) 대신 selective probability/margin repair(선별 확률/마진 수리)로 넘어간다.
- >-
  Stage203 evidence(203단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): DD improvement(낙폭 개선)과 net/OOS damage(순손익/표본외 손상)를 분리해서 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage203_stage202_probability_binding_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage203_stage202_probability_binding_followup_review:
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
- adapter_under_review(검토 중 어댑터): `stage203_stage202_probability_binding_followup_review`
- status(상태): `stage203_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage203(203단계)는 Stage202(202단계) probability binding repair(확률 구속 수리)를 follow-up review(후속 검토)했다. Effect(효과): Stage204(204단계)는 side-wide cut(방향 전체 차단)이 아니라 selective probability/margin repair(선별 확률/마진 수리)를 좁게 진행한다.

## Latest Stage203 Evidence(최신 203단계 근거)

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
        f"""# Stage203 Selection Status(203단계 선택 상태)

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
        f"""# Stage203 Review Index(203단계 검토 색인)

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
        f"\n## {s172.utc_now()} Stage203 Stage202 probability binding follow-up review closeout(203단계 202단계 확률 구속 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): side-wide cut(방향 전체 차단)의 net/OOS damage(순손익/표본외 손상)를 기록하고 Stage204(204단계) selective repair(선별 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    kpi_rows = read_csv(SOURCE_KPI_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    probability_rows = read_csv(SOURCE_PROBABILITY_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, kpi_rows, segment_rows, probability_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows()
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows))
    s172.write_md(DECISION_PATH, decision_md())
    write_ledgers(tradeoff_rows)
    summary_payload = {
        "run_id": RUN_ID,
        "decision": DECISION,
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "route_rows": route_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(SUMMARY_JSON_PATH, summary_payload)
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

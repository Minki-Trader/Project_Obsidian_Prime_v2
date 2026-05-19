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
from stage_pipelines.stage206 import long_session_dd_micro_repair as s206  # noqa: E402

s172 = s206.s172

STAGE_ID = "207_adapter_research__stage206_long_session_dd_micro_repair_followup_review"
RUN_ID = "run207A_stage207_stage206_long_session_dd_micro_repair_followup_review_v1"
PACKET_ID = "stage207_stage206_long_session_dd_micro_repair_followup_review_v1"
PARENT_RUN_ID = "run206A_stage206_stage204_long_session_dd_micro_repair_v1"
SOURCE_STAGE_ID = "206_adapter_research__stage204_long_session_dd_micro_repair"
SOURCE_RUN_ID = "run206A_stage206_stage204_long_session_dd_micro_repair_v1"
SOURCE_STAGE206_EVIDENCE_COMMIT = "3f9fcb1dd2eef452b4708d8ae98ad202a3000fb0"
SOURCE_STAGE206_HASH_RECORD_COMMIT = "7e70cd2142615a45c7231058f800083f47c308f2"
NEXT_STAGE_ID = "208_adapter_research__stage206_risk_cap_interpolation_repair"
NEXT_RUN_ID = "run208A_stage208_stage206_risk_cap_interpolation_repair_v1"
NEXT_PACKET_ID = "stage208_stage206_risk_cap_interpolation_repair_v1"
DECISION = "open_stage208_bounded_risk_cap_interpolation_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage206_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_long_session_dd_micro_repair"
BOUNDARY = s206.BOUNDARY
LEGACY_34D = s206.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_quality_matrix.csv")
SOURCE_KPI_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_dd_micro_repair_kpi_summary.csv")
SOURCE_SEGMENT_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_risk_atr_telemetry.csv")
SOURCE_PROBABILITY_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_probability_telemetry_summary.csv")
SOURCE_REPORT_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_dd_micro_repair_report.md")
SOURCE_DECISION_PATH = Path("stages/206_adapter_research__stage204_long_session_dd_micro_repair/03_reviews/stage206_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage207_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage207_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage207_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage207_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage207_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage207_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage207/stage206_long_session_dd_micro_repair_followup_review.py")


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


def stage207_read(adapter_id: str) -> str:
    if adapter_id == "s206_ls_ref_r0325":
        return "reference_strong_but_dd_gap_remains(기준 강함, 낙폭 격차 잔존)"
    if adapter_id == "s206_ls_session_p5_r0325":
        return "session_p5_damages_midpf_oos_without_dd_help(5분 세션 확장은 낙폭 개선 없이 중반 수익요인/표본외 손상)"
    if adapter_id == "s206_ls_session_p10_r0325":
        return "session_p10_no_effect_same_as_ref(10분 세션 확장은 기준과 동일)"
    if adapter_id == "s206_ls_risk0250":
        return "risk0250_fixes_dd_but_net_below_34d(2.5% 위험은 낙폭 해결, 순손익 34D 미달)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ref = by_adapter(quality_rows).get("s206_ls_ref_r0325", {})
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
                "stage207_read": stage207_read(adapter_id),
            }
        )
    return rows


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = by_adapter(tradeoff_rows)
    ref = rows.get("s206_ls_ref_r0325", {})
    session_p5 = rows.get("s206_ls_session_p5_r0325", {})
    session_p10 = rows.get("s206_ls_session_p10_r0325", {})
    risk0250 = rows.get("s206_ls_risk0250", {})
    return [
        {
            "run_id": RUN_ID,
            "finding": "reference_still_best_total_package(기준이 여전히 전체 패키지 최선)",
            "evidence": f"ref val_net={ref.get('validation_net')}, val_dd={ref.get('validation_dd_percent')}, mid_pf={ref.get('validation_mid_pf')}, oos_net={ref.get('oos_net')}",
            "meaning": "Reference(기준)는 validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인)를 지키지만 DD(낙폭)가 아직 34D(34D)보다 높다.",
            "next_use": "Stage208(208단계)는 기준의 수익 구조를 보존한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "session_window_nudge_not_the_fix(세션 창 조정은 해법 아님)",
            "evidence": f"p5 val_net={session_p5.get('validation_net')}, val_dd={session_p5.get('validation_dd_percent')}, mid_pf={session_p5.get('validation_mid_pf')}, oos_net={session_p5.get('oos_net')}; p10 val_net={session_p10.get('validation_net')}, val_dd={session_p10.get('validation_dd_percent')}",
            "meaning": "Session p5(세션 5분 확장)는 DD(낙폭)를 낮추지 못하고, p10(10분 확장)은 기준과 동일하게 나왔다.",
            "next_use": "Stage208(208단계)에서는 세션 창 확장을 failure memory(실패 기억)로 둔다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk_cap_has_signal_but_overshoots(위험 상한은 단서가 있으나 과하게 낮춤)",
            "evidence": f"risk0250 val_net={risk0250.get('validation_net')}, val_dd={risk0250.get('validation_dd_percent')}, mid_pf={risk0250.get('validation_mid_pf')}, oos_net={risk0250.get('oos_net')}",
            "meaning": "Risk cap 2.5%(위험 상한 2.5%)는 DD/PF/midPF(낙폭/수익요인/중반 수익요인)는 통과하지만 net/OOS(순손익/표본외)를 과하게 줄인다.",
            "next_use": "Stage208(208단계)는 2.5%와 3.25% 사이의 risk cap interpolation(위험 상한 보간)을 좁게 측정한다.",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage208_risk_cap_interpolation_repair(208단계 위험 상한 보간 수리)",
            "decision": DECISION,
            "source_clue": "risk0250_passes_dd_pf_midpf_but_net_low(2.5% 위험은 낙폭/수익요인/중반 통과, 순손익 낮음)",
            "bounded_question": "Can intermediate risk caps(중간 위험 상한) reduce DD(낙폭) below 34D(34D) while keeping validation net(검증 순손익) above 34D(34D)?",
            "guardrail": "risk_cap_only(위험 상한만); preserve_long_session_gate(롱 세션 제한 보존); preserve_validation_net_above_34d(검증 순손익 34D 이상 보존)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "session_window_nudge_failed(세션 창 조정 실패)",
            "bounded_question": "Do not continue session window widening(세션 창 확장 지속 금지) unless a new hypothesis is written.",
            "guardrail": "no_more_session_widening_inside_stage207(207단계 안 세션 확장 금지)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage207 Follow-up Review(207단계 후속 검토)",
        "",
        f"- decision(판정): `{DECISION}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage206_evidence_commit(원천 206단계 근거 커밋): `{SOURCE_STAGE206_EVIDENCE_COMMIT}`",
        f"- source_stage206_hash_record_commit(원천 206단계 해시 기록 커밋): `{SOURCE_STAGE206_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Stage207(207단계)는 review-only(검토 전용)다. Effect(효과): Stage206(206단계)의 DD micro repair(낙폭 미세 수리) 결과를 추가 튜닝 없이 판정하고 Stage208(208단계) risk cap interpolation(위험 상한 보간) 질문을 좁힌다.",
        "",
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row['adapter_id']} | {row['validation_pf']} | {row['validation_net']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['stage207_read']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- `s206_ls_ref_r0325`는 validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인)는 34D(34D) 이상이지만 DD(낙폭)가 아직 높다.",
            "- `s206_ls_session_p5_r0325`는 DD(낙폭)를 낮추지 못하고 midPF/OOS(중반 수익요인/표본외)를 손상했다.",
            "- `s206_ls_session_p10_r0325`는 reference(기준)와 동일하게 나와 세션 창 확장 단서가 약하다.",
            "- `s206_ls_risk0250`는 DD(낙폭)를 `10.2997%`까지 낮췄지만 validation net(검증 순손익)이 `851.54`로 34D(34D) 미달이다.",
            f"- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`.",
            "- Stage207(207단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.",
        ]
    )
    return "\n".join(lines)


def decision_md() -> str:
    return f"""# Stage207 Decision(207단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage206_evidence_commit(원천 206단계 근거 커밋): `{SOURCE_STAGE206_EVIDENCE_COMMIT}`
- source_stage206_hash_record_commit(원천 206단계 해시 기록 커밋): `{SOURCE_STAGE206_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage207(207단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage206(206단계)의 risk cap clue(위험 상한 단서)를 Stage208(208단계) risk cap interpolation(위험 상한 보간)으로 좁게 넘긴다.
"""


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    best = by_adapter(tradeoff_rows).get("s206_ls_ref_r0325", {})
    risk = by_adapter(tradeoff_rows).get("s206_ls_risk0250", {})
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage206_dd_micro_repair_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage206_dd_micro_repair_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage206_dd_micro_repair_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_total=s206_ls_ref_r0325;validation_net={best.get('validation_net')};validation_dd={best.get('validation_dd_percent')};risk0250_dd={risk.get('validation_dd_percent')};risk0250_net={risk.get('validation_net')}",
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage207 reviewed Stage206 long-session DD micro repair tradeoff and opened Stage208 risk-cap interpolation.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage207_stage206_dd_micro_repair_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage206_evidence_commit", SOURCE_STAGE206_EVIDENCE_COMMIT),
                ("source_stage206_hash_record_commit", SOURCE_STAGE206_HASH_RECORD_COMMIT),
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
        (PRODUCER_PATH, "Stage207 follow-up review producer script(생산 스크립트)."),
        (REPORT_PATH, "Stage207 bounded follow-up review report(경계 후속 검토 보고서)."),
        (TRADEOFF_MATRIX_PATH, "Stage207 DD tradeoff matrix(낙폭 상충 행렬)."),
        (ATTRIBUTION_PATH, "Stage207 performance attribution(성과 원인 분해)."),
        (ROUTE_MATRIX_PATH, "Stage207 route matrix(경로 행렬)."),
        (SUMMARY_JSON_PATH, "Stage207 summary JSON(요약 JSON)."),
        (DECISION_PATH, "Stage207 decision(판정)."),
        (STAGE_LEDGER_PATH, "Stage207 local ledger(단계 장부)."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage207_followup_review_evidence",
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
        f"""# Stage207 Closeout Packet(207단계 종료 작업 묶음)

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

Stage208(208단계)은 Stage207(207단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can intermediate model risk caps(중간 모델 위험 상한) between 2.5% and 3.25%(2.5%와 3.25% 사이) reduce validation DD(검증 낙폭) below 34D(34D) while preserving validation net(검증 순손익) above 34D(34D)?

Effect(효과): Stage206(206단계)의 risk0250 clue(2.5% 위험 단서)는 쓰되, 세션 창이나 진입 로직을 새로 만지지 않는다.

## Constraints(제약)

- start from `s206_ls_ref_r0325` long-session structure(롱 세션 구조에서 시작)
- change model_risk_max_pct only(모델 위험 상한만 변경)
- no session window widening(세션 창 확장 금지)
- no entry logic change(진입 로직 변경 금지)
- preserve validation net above 34D(검증 순손익 34D 이상 보존)
- preserve validation PF and mid PF above 34D(검증 수익요인과 중반 수익요인 34D 이상 보존)
- record OOS PF/net/DD(표본외 수익요인/순손익/낙폭 기록)
- record risk/ATR telemetry(위험/ATR 기록)
- if no interpolation works, close Stage208(208단계) with evidence and route next bounded repair(다음 경계 수리)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage208 Input References(208단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_attribution(원천 성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- source_route_matrix(원천 경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage206_quality_matrix(원천 206단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage206_probability_telemetry(원천 206단계 확률 기록): `{rel(SOURCE_PROBABILITY_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage208 Review Index(208단계 검토 색인)

- status(상태): `open_planned_from_stage207`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage208 Selection Status(208단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage207`
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
  Stage207(207단계) closed(종료) as `{DECISION}` and Stage208(208단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): risk cap interpolation(위험 상한 보간)으로 DD/net(낙폭/순손익) 균형점을 좁게 찾는다.
- >-
  Stage207 evidence(207단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): session window failure(세션 창 실패)와 risk cap clue(위험 상한 단서)를 분리해서 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage207_stage206_dd_micro_repair_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage207_stage206_dd_micro_repair_followup_review:
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
- adapter_under_review(검토 중 어댑터): `stage207_stage206_dd_micro_repair_followup_review`
- status(상태): `stage207_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage207(207단계)는 Stage206(206단계) long-session DD micro repair(롱 세션 낙폭 미세 수리)를 follow-up review(후속 검토)했다. Effect(효과): Stage208(208단계)는 model risk cap interpolation(모델 위험 상한 보간)만 좁게 진행한다.

## Latest Stage207 Evidence(최신 207단계 근거)

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
        f"""# Stage207 Selection Status(207단계 선택 상태)

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
        f"""# Stage207 Review Index(207단계 검토 색인)

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
        f"\n## {s172.utc_now()} Stage207 Stage206 DD micro repair follow-up review closeout(207단계 206단계 낙폭 미세 수리 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): risk0250(위험 2.5%) 단서를 Stage208(208단계) risk cap interpolation(위험 상한 보간)으로 넘겼다.\n"
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


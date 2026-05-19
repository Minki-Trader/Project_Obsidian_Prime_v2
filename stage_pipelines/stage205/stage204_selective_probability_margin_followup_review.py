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
from stage_pipelines.stage204 import selective_probability_margin_recovery_repair as s204  # noqa: E402

s172 = s204.s172

STAGE_ID = "205_adapter_research__stage204_selective_probability_margin_followup_review"
RUN_ID = "run205A_stage205_stage204_selective_probability_margin_followup_review_v1"
PACKET_ID = "stage205_stage204_selective_probability_margin_followup_review_v1"
PARENT_RUN_ID = "run204A_stage204_selective_probability_margin_recovery_repair_v1"
SOURCE_STAGE_ID = "204_adapter_research__selective_probability_margin_recovery_repair"
SOURCE_RUN_ID = "run204A_stage204_selective_probability_margin_recovery_repair_v1"
SOURCE_STAGE204_EVIDENCE_COMMIT = "4826c3609e3dfaaed50b942c98f9ca5c495625fe"
SOURCE_STAGE204_HASH_RECORD_COMMIT = "5c99b056ec968159c084adc5994eb261135e2e59"
NEXT_STAGE_ID = "206_adapter_research__stage204_long_session_dd_micro_repair"
NEXT_RUN_ID = "run206A_stage206_stage204_long_session_dd_micro_repair_v1"
NEXT_PACKET_ID = "stage206_stage204_long_session_dd_micro_repair_v1"
DECISION = "open_stage206_long_session_dd_micro_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage204_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_long_session_dd_micro_repair"
BOUNDARY = s204.BOUNDARY
LEGACY_34D = s204.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_quality_matrix.csv")
SOURCE_KPI_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_selective_probability_margin_kpi_summary.csv")
SOURCE_SEGMENT_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_risk_atr_telemetry.csv")
SOURCE_PROBABILITY_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_selective_probability_margin_telemetry_summary.csv")
SOURCE_REPORT_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_selective_probability_margin_report.md")
SOURCE_DECISION_PATH = Path("stages/204_adapter_research__selective_probability_margin_recovery_repair/03_reviews/stage204_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage205_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage205_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage205_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage205_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage205_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage205_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage205/stage204_selective_probability_margin_followup_review.py")


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


def stage205_read(adapter_id: str) -> str:
    if adapter_id == "s204_cd8_ref_r0325":
        return "reference_retained_but_dd_midpf_gap(기준 유지, 낙폭/중반 수익요인 격차)"
    if adapter_id == "s204_cd8_long_wide_r0325":
        return "wide_long_gate_rejected_net_midpf_late_concentration_damage(넓은 롱 제한 기각, 순손익/중반 수익요인/후반 집중 손상)"
    if adapter_id == "s204_cd8_long_tight_r0325":
        return "tight_long_gate_preserves_net_but_not_midpf_dd(좁은 롱 제한은 순손익 보존, 중반 수익요인/낙폭 부족)"
    if adapter_id == "s204_cd8_long_session_r0325":
        return "long_session_best_candidate_dd_gap_small(롱 세션 제한 최선 후보, 낙폭 격차 작음)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ref = by_adapter(quality_rows).get("s204_cd8_ref_r0325", {})
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
                "stage205_read": stage205_read(adapter_id),
            }
        )
    return rows


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = by_adapter(tradeoff_rows)
    ref = rows.get("s204_cd8_ref_r0325", {})
    long_wide = rows.get("s204_cd8_long_wide_r0325", {})
    long_tight = rows.get("s204_cd8_long_tight_r0325", {})
    long_session = rows.get("s204_cd8_long_session_r0325", {})
    return [
        {
            "run_id": RUN_ID,
            "finding": "reference_strong_but_overtaken_by_long_session(기준은 강하지만 롱 세션 제한이 앞섬)",
            "evidence": f"ref val_net={ref.get('validation_net')}, val_dd={ref.get('validation_dd_percent')}, mid_pf={ref.get('validation_mid_pf')}, oos_net={ref.get('oos_net')}",
            "meaning": "Reference(기준)는 OOS(표본외)가 좋지만 DD/midPF(낙폭/중반 수익요인) 약점이 남는다.",
            "next_use": "Stage206(206단계)는 long_session(롱 세션 제한)을 중심 후보로 삼는다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "long_wide_overfilters_midpf(넓은 롱 제한은 중반 수익요인을 과하게 훼손)",
            "evidence": f"long_wide val_net={long_wide.get('validation_net')}, val_dd={long_wide.get('validation_dd_percent')}, mid_pf={long_wide.get('validation_mid_pf')}, late_share={long_wide.get('validation_late_net_share')}",
            "meaning": "DD(낙폭)는 34D(34D)를 넘지만 net/midPF/late concentration(순손익/중반 수익요인/후반 집중)이 약하다.",
            "next_use": "Stage206(206단계)에서 wide gate(넓은 제한문)는 failure memory(실패 기억)로 둔다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "long_tight_preserves_net_but_not_quality(좁은 롱 제한은 순손익은 보존하지만 품질 부족)",
            "evidence": f"long_tight val_net={long_tight.get('validation_net')}, val_dd={long_tight.get('validation_dd_percent')}, mid_pf={long_tight.get('validation_mid_pf')}, oos_net={long_tight.get('oos_net')}",
            "meaning": "Net(순손익)은 좋지만 DD/midPF(낙폭/중반 수익요인)가 여전히 약하다.",
            "next_use": "Stage206(206단계)에서 tight gate(좁은 제한문)는 보존 대조군으로 참고한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "long_session_nearly_hits_full_34d_target(롱 세션 제한은 34D 목표에 거의 도달)",
            "evidence": f"long_session val_net={long_session.get('validation_net')}, val_dd={long_session.get('validation_dd_percent')}, mid_pf={long_session.get('validation_mid_pf')}, oos_net={long_session.get('oos_net')}",
            "meaning": "Validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인)는 34D(34D) 이상이고 DD(낙폭)만 약 0.183%p 남았다.",
            "next_use": "Stage206(206단계)는 long_session(롱 세션 제한)의 DD micro repair(낙폭 미세 수리)만 좁게 시도한다.",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage206_long_session_dd_micro_repair(206단계 롱 세션 낙폭 미세 수리)",
            "decision": DECISION,
            "source_clue": "long_session_strong_net_midpf_small_dd_gap(롱 세션 제한은 순손익/중반 수익요인 강함, 낙폭 격차 작음)",
            "bounded_question": "Can a tiny session window or risk/bracket nudge(아주 작은 세션 창 또는 위험/브래킷 조정) reduce DD(낙폭) below 34D(34D) while preserving long_session net/OOS(롱 세션 순손익/표본외)?",
            "guardrail": "no_large_gate_widening(큰 제한문 확장 금지); preserve_validation_net_above_34d(검증 순손익 34D 이상 보존); preserve_midpf_above_34d(중반 수익요인 34D 이상 보존)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "long_wide_overfilters_and_ref_dd_gap_remains(넓은 롱 제한은 과필터, 기준은 낙폭 격차 잔존)",
            "bounded_question": "Do not accept DD(낙폭) improvement if midPF/net/OOS(중반 수익요인/순손익/표본외)가 무너진다.",
            "guardrail": "DD improvement is necessary but not sufficient(낙폭 개선은 필요하지만 충분하지 않음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage205 Follow-up Review(205단계 후속 검토)",
        "",
        f"- decision(판정): `{DECISION}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage204_evidence_commit(원천 204단계 근거 커밋): `{SOURCE_STAGE204_EVIDENCE_COMMIT}`",
        f"- source_stage204_hash_record_commit(원천 204단계 해시 기록 커밋): `{SOURCE_STAGE204_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Stage205(205단계)는 review-only(검토 전용)다. Effect(효과): Stage204(204단계)의 selective probability/margin(선별 확률/마진) 결과를 추가 튜닝 없이 판정하고 Stage206(206단계) DD micro repair(낙폭 미세 수리) 질문을 좁힌다.",
        "",
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row['adapter_id']} | {row['validation_pf']} | {row['validation_net']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['stage205_read']} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- `s204_cd8_ref_r0325` keeps a strong reference(강한 기준을 유지)하지만 DD/midPF(낙폭/중반 수익요인)는 아직 34D(34D)에 못 미친다.",
            "- `s204_cd8_long_wide_r0325`는 DD(낙폭)를 34D(34D) 아래로 낮췄지만 net/midPF/late concentration(순손익/중반 수익요인/후반 집중)을 손상해 기각한다.",
            "- `s204_cd8_long_tight_r0325`는 net(순손익)을 보존하지만 DD/midPF(낙폭/중반 수익요인) 격차가 남아 중심 후보가 아니다.",
            "- `s204_cd8_long_session_r0325`는 validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인)가 34D(34D) 이상이고 DD(낙폭)만 약 0.183%p 남아 Stage206(206단계) 중심 후보다.",
            f"- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`.",
            "- Stage205(205단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.",
        ]
    )
    return "\n".join(lines)


def decision_md() -> str:
    return f"""# Stage205 Decision(205단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage204_evidence_commit(원천 204단계 근거 커밋): `{SOURCE_STAGE204_EVIDENCE_COMMIT}`
- source_stage204_hash_record_commit(원천 204단계 해시 기록 커밋): `{SOURCE_STAGE204_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage205(205단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage204(204단계)의 long_session(롱 세션 제한) 단서를 Stage206(206단계) DD micro repair(낙폭 미세 수리)로 좁게 넘긴다.
"""


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    best = by_adapter(tradeoff_rows).get("s204_cd8_long_session_r0325", {})
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage204_selective_probability_margin_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage204_selective_probability_margin_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage204_selective_probability_margin_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_candidate=s204_cd8_long_session_r0325;validation_net={best.get('validation_net')};validation_dd={best.get('validation_dd_percent')};mid_pf={best.get('validation_mid_pf')};oos_net={best.get('oos_net')}",
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage205 reviewed Stage204 selective probability/margin tradeoff and opened Stage206 long-session DD micro repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage205_stage204_selective_probability_margin_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage204_evidence_commit", SOURCE_STAGE204_EVIDENCE_COMMIT),
                ("source_stage204_hash_record_commit", SOURCE_STAGE204_HASH_RECORD_COMMIT),
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
        (PRODUCER_PATH, "Stage205 follow-up review producer script(생산 스크립트)."),
        (REPORT_PATH, "Stage205 bounded follow-up review report(경계 후속 검토 보고서)."),
        (TRADEOFF_MATRIX_PATH, "Stage205 selective probability/margin tradeoff matrix(선별 확률/마진 상충 행렬)."),
        (ATTRIBUTION_PATH, "Stage205 performance attribution(성과 원인 분해)."),
        (ROUTE_MATRIX_PATH, "Stage205 route matrix(경로 행렬)."),
        (SUMMARY_JSON_PATH, "Stage205 summary JSON(요약 JSON)."),
        (DECISION_PATH, "Stage205 decision(판정)."),
        (STAGE_LEDGER_PATH, "Stage205 local ledger(단계 장부)."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage205_followup_review_evidence",
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
        f"""# Stage205 Closeout Packet(205단계 종료 작업 묶음)

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

Stage206(206단계)는 Stage205(205단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a tiny DD micro repair(아주 작은 낙폭 미세 수리) on `s204_cd8_long_session_r0325` reduce validation DD(검증 낙폭) below legacy 34D(레거시 34D) while preserving validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인) above 34D(34D) and keeping OOS(표본외) credible?

Effect(효과): Stage204(204단계)의 long_session clue(롱 세션 제한 단서)는 쓰되, broad hunting(넓은 사냥)이나 side-wide cut(방향 전체 차단)으로 Stage206(206단계)를 부풀리지 않는다.

## Constraints(제약)

- start from `s204_cd8_long_session_r0325`(롱 세션 제한 후보에서 시작)
- no side-wide cut(방향 전체 차단 금지)
- no no-trade solution(무거래 해답 금지)
- no large gate widening(큰 제한문 확장 금지)
- preserve validation net above 34D(검증 순손익 34D 이상 보존)
- preserve validation PF and mid PF above 34D(검증 수익요인과 중반 수익요인 34D 이상 보존)
- record OOS PF/net/DD(표본외 수익요인/순손익/낙폭 기록)
- record risk/ATR telemetry(위험/ATR 기록)
- if DD remains weak, close Stage206(206단계) with evidence and route next bounded repair(다음 경계 수리)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage206 Input References(206단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_attribution(원천 성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- source_route_matrix(원천 경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage204_quality_matrix(원천 204단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage204_selective_probability_telemetry(원천 204단계 선별 확률 기록): `{rel(SOURCE_PROBABILITY_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage206 Review Index(206단계 검토 색인)

- status(상태): `open_planned_from_stage205`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage206 Selection Status(206단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage205`
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
  Stage205(205단계) closed(종료) as `{DECISION}` and Stage206(206단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): long_session(롱 세션 제한)의 남은 DD gap(낙폭 격차)을 좁게 수리한다.
- >-
  Stage205 evidence(205단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): long_wide damage(넓은 롱 제한 손상)와 long_session clue(롱 세션 제한 단서)를 분리해서 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage205_stage204_selective_probability_margin_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage205_stage204_selective_probability_margin_followup_review:
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
- adapter_under_review(검토 중 어댑터): `stage205_stage204_selective_probability_margin_followup_review`
- status(상태): `stage205_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage205(205단계)는 Stage204(204단계) selective probability/margin repair(선별 확률/마진 수리)를 follow-up review(후속 검토)했다. Effect(효과): Stage206(206단계)는 `s204_cd8_long_session_r0325`의 DD micro repair(낙폭 미세 수리)만 좁게 진행한다.

## Latest Stage205 Evidence(최신 205단계 근거)

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
        f"""# Stage205 Selection Status(205단계 선택 상태)

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
        f"""# Stage205 Review Index(205단계 검토 색인)

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
        f"\n## {s172.utc_now()} Stage205 Stage204 selective probability/margin follow-up review closeout(205단계 204단계 선별 확률/마진 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): long_session(롱 세션 제한)을 Stage206(206단계) DD micro repair(낙폭 미세 수리) 중심 후보로 넘겼다.\n"
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


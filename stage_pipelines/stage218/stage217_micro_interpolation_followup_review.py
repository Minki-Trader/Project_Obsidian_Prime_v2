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
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage213 import s210_r0315_oos_monthly_concentration_repair as s213  # noqa: E402

s172 = s213.s172

STAGE_ID = "218_adapter_research__stage217_micro_interpolation_followup_review"
RUN_ID = "run218A_stage218_stage217_micro_interpolation_followup_review_v1"
PACKET_ID = "stage218_stage217_micro_interpolation_followup_review_v1"
PARENT_RUN_ID = "run217A_stage217_oos_preserving_mid_pf_micro_interpolation_v1"
SOURCE_STAGE_ID = "217_adapter_research__oos_preserving_mid_pf_micro_interpolation"
SOURCE_RUN_ID = "run217A_stage217_oos_preserving_mid_pf_micro_interpolation_v1"
SOURCE_STAGE217_EVIDENCE_COMMIT = "053616518aa105c2830bd5d70a29b2ed65f2f61c"
SOURCE_STAGE217_HASH_RECORD_COMMIT = "957f95127576c36b90d791754a2f069023f8b30b"
NEXT_STAGE_ID = "219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure"
NEXT_RUN_ID = "run219A_stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1"
NEXT_PACKET_ID = "stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1"
DECISION = "open_stage219_bounded_entry_lifecycle_repair_due_to_bracket_axis_failure_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage217_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_entry_lifecycle_repair_after_bracket_axis_failure"
BOUNDARY = s213.BOUNDARY
LEGACY_34D = s213.LEGACY_34D
STAGE210_ANCHOR = {
    "adapter_id": "s210_ls_r0315",
    "validation_net": 1200.27,
    "validation_mid_pf": 1.695877099,
    "validation_dd": 12.6726,
    "oos_net": 714.86,
}
STAGE215_MID_RECOVERY = {
    "adapter_id": "s215_r031375_s2050_t465",
    "validation_net": 1059.28,
    "validation_mid_pf": 1.690898468,
    "validation_dd": 12.6140,
    "oos_net": 706.62,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_summary.json")
SOURCE_QUALITY_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_quality_matrix.csv")
SOURCE_MONTHLY_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_monthly_kpi_summary.csv")
SOURCE_CONCENTRATION_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_concentration_risk_summary.csv")
SOURCE_RISK_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_micro_interpolation_report.md")
SOURCE_DECISION_PATH = Path("stages/217_adapter_research__oos_preserving_mid_pf_micro_interpolation/03_reviews/stage217_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage218_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage218_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage218_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage218_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage218_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage218_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage218/stage217_micro_interpolation_followup_review.py")
ARTIFACT_COLUMNS = s172.ARTIFACT_COLUMNS


def rel(path: Path | str) -> str:
    return s172.rel(path)


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip().replace(",", "")
        return float(text) if text else default
    except (TypeError, ValueError):
        return default


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


def monthly_stats(monthly_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> dict[str, Any]:
    rows = [row for row in monthly_rows if row.get("adapter_id") == adapter_id and row.get("split") == split]
    negative = [row for row in rows if fnum(row.get("net_profit")) <= 0]
    pf_below = [row for row in rows if fnum(row.get("profit_factor")) < float(LEGACY_34D["profit_factor"])]
    return {
        "month_count": len(rows),
        "negative_month_count": len(negative),
        "negative_months": ",".join(str(row.get("month", "")) for row in negative),
        "negative_month_net": round(sum(fnum(row.get("net_profit")) for row in negative), 2),
        "pf_below_34d_count": len(pf_below),
    }


def lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, view: str | None = None) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") != adapter_id or row.get("split") != split:
            continue
        if view is None or row.get("view") == view:
            return row
    return {}


def profile_label(row: Mapping[str, Any]) -> str:
    mid_ok = fnum(row.get("validation_mid_pf")) >= float(LEGACY_34D["profit_factor"])
    net_ok = fnum(row.get("validation_net")) >= float(LEGACY_34D["net_profit"])
    oos_ok = fnum(row.get("oos_net")) >= STAGE210_ANCHOR["oos_net"]
    if oos_ok and not (mid_ok and net_ok):
        return "oos_preserved_validation_failed(표본외 보존, 검증 실패)"
    if not oos_ok and not (mid_ok and net_ok):
        return "both_oos_and_validation_failed(표본외와 검증 모두 실패)"
    if mid_ok and net_ok and not oos_ok:
        return "validation_recovered_oos_failed(검증 회복, 표본외 실패)"
    return "unexpected_full_pass_review_needed(예상 밖 전체 통과, 검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    concentration_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_months = monthly_stats(monthly_rows, adapter_id, "validation_is")
        oos_months = monthly_stats(monthly_rows, adapter_id, "oos")
        oos_conc = lookup(concentration_rows, adapter_id, "oos")
        val_risk = lookup(risk_rows, adapter_id, "validation_is", "actual_routed_total")
        oos_risk = lookup(risk_rows, adapter_id, "oos", "actual_routed_total")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "profile_label": profile_label(row),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_stage215_mid_recovery": round(fnum(row.get("validation_net")) - STAGE215_MID_RECOVERY["validation_net"], 2),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(fnum(row.get("validation_mid_pf")) - float(LEGACY_34D["profit_factor"]), 6),
                "validation_mid_pf_delta_vs_stage215_mid_recovery": round(fnum(row.get("validation_mid_pf")) - STAGE215_MID_RECOVERY["validation_mid_pf"], 6),
                "validation_negative_month_count": val_months["negative_month_count"],
                "validation_pf_below_34d_month_count": val_months["pf_below_34d_count"],
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_stage210_anchor": round(fnum(row.get("oos_net")) - STAGE210_ANCHOR["oos_net"], 2),
                "oos_net_delta_vs_stage215_mid_recovery": round(fnum(row.get("oos_net")) - STAGE215_MID_RECOVERY["oos_net"], 2),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_negative_month_count": oos_months["negative_month_count"],
                "oos_negative_months": oos_months["negative_months"],
                "oos_negative_month_net": oos_months["negative_month_net"],
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (fnum(row.get("oos_net")), fnum(row.get("validation_mid_pf"))), default={})


def build_attribution_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "micro_interpolation_failed_to_restore_validation(미세 보간은 검증 회복 실패)",
            "comparison_baseline": "Stage215 mid recovery and Stage210 anchor(215단계 중반 회복과 210단계 기준 후보)",
            "likely_drivers": "bracket_axis_now_exhausted(브래킷 축 소진)",
            "segment_checks": f"best={best.get('adapter_id')};mid_pf={best.get('validation_mid_pf')};val_net={best.get('validation_net')};oos={best.get('oos_net')}",
            "trade_shape": f"best_oos_delta_vs_stage210={best.get('oos_net_delta_vs_stage210_anchor')};mid_delta_vs_34d={best.get('validation_mid_pf_gap_vs_34d')}",
            "alternative_explanations": "entry_timing_or_lifecycle_density_drives_tradeoff(진입 타이밍 또는 생애주기 밀도가 상충을 만들 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "entry_lifecycle_repair_not_more_bracket_interpolation(추가 브래킷 보간이 아닌 진입/생애주기 수리)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "risk_floor_not_driver(위험 바닥은 원인이 아님)",
            "comparison_baseline": "Stage217 risk/ATR telemetry(217단계 위험/ATR 기록)",
            "likely_drivers": "risk_floor_count_zero(위험 바닥 적용 수 0)",
            "segment_checks": f"risk_floor_oos={best.get('oos_risk_floor_applied_count')}",
            "trade_shape": "same bracket family damaged validation payoff(같은 브래킷 계열이 검증 보상을 손상)",
            "alternative_explanations": "model_risk_cap_not_primary_axis(모델 위험 상한은 주축이 아닐 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "entry_lifecycle_repair_with_bracket_held_constant(브래킷 고정 후 진입/생애주기 수리)",
        },
    ]


def build_route_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stop_bracket_micro_interpolation_axis(브래킷 미세 보간 축 중단)",
            "adapter_id": best.get("adapter_id", ""),
            "action": "do_not_extend_stage217_axis(217단계 축을 연장하지 않음)",
            "effect": "prevents_open_ended_SLTP_tuning(끝없는 손절/익절 튜닝 방지)",
            "risk": "may_abandon_small_oos_gain(작은 표본외 이득을 버릴 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "stage219_entry_lifecycle_repair(219단계 진입/생애주기 수리)",
            "adapter_id": STAGE210_ANCHOR["adapter_id"],
            "action": "hold_bracket_family_constant_and_repair_entry_or_lifecycle(브래킷 계열은 고정하고 진입 또는 생애주기 수리)",
            "effect": "targets_validation_payoff_without_replaying_bracket_axis(브래킷 축 반복 없이 검증 보상을 겨냥)",
            "risk": "oos_monthly_concentration_may_remain(표본외 월별 집중이 남을 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "preserve_failure_memory(실패 기억 보존)",
            "adapter_id": "stage217_axis",
            "action": "record_as_failed_axis_not_invalid(무효가 아닌 실패 축으로 기록)",
            "effect": "future_stages_do_not_repeat_same_microgrid(미래 단계가 같은 미세 격자를 반복하지 않음)",
            "risk": "none_review_boundary(검토 경계상 없음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> str:
    lines = [
        "# Stage218 Follow-up Review(218단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage217_evidence_commit(원천 217단계 근거 커밋): `{SOURCE_STAGE217_EVIDENCE_COMMIT}`",
        f"- source_stage217_hash_record_commit(원천 217단계 해시 기록 커밋): `{SOURCE_STAGE217_HASH_RECORD_COMMIT}`",
        f"- decision(판정): `{DECISION}`",
        f"- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | profile(유형) | val net gap(검증 순손익 차이) | mid PF gap(중반 수익요인 차이) | OOS vs 210(210 대비 표본외) | early PF(초반 수익요인) | risk floor(위험 바닥) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('profile_label', '')} | {row.get('validation_net_gap_vs_34d', '')} | {row.get('validation_mid_pf_gap_vs_34d', '')} | {row.get('oos_net_delta_vs_stage210_anchor', '')} | {row.get('validation_early_pf', '')} | {row.get('oos_risk_floor_applied_count', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- `{best.get('adapter_id', '')}`가 OOS net(표본외 순손익) `{best.get('oos_net', '')}`로 가장 낫지만 validation net(검증 순손익) `{best.get('validation_net', '')}`와 validation mid PF(검증 중반 수익요인) `{best.get('validation_mid_pf', '')}`가 모두 부족하다.",
            "- Stage217(217단계)의 SL/TP micro interpolation(손절/익절 미세 보간)은 bounded negative evidence(경계 부정 근거)다.",
            "- 다음은 같은 브래킷 축이 아니라 entry/lifecycle(진입/생애주기) 수리다.",
            "- Stage218(218단계)는 final(최종), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.",
        ]
    )
    return "\n".join(lines)


def decision_md(best: Mapping[str, Any]) -> str:
    return f"""# Stage218 Decision(218단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage217_evidence_commit(원천 217단계 근거 커밋): `{SOURCE_STAGE217_EVIDENCE_COMMIT}`
- source_stage217_hash_record_commit(원천 217단계 해시 기록 커밋): `{SOURCE_STAGE217_HASH_RECORD_COMMIT}`
- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage218(218단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage219(219단계)에서 bracket axis(브래킷 축)를 더 늘리지 않고 entry/lifecycle repair(진입/생애주기 수리)를 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage218_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage218 Stage217 micro interpolation follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(best: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("best_stage217_row", best.get("adapter_id", "")),
            ("best_oos_net", best.get("oos_net", "")),
            ("best_mid_pf", best.get("validation_mid_pf", "")),
            ("best_val_net", best.get("validation_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("bracket_axis_status", "failed_bounded_negative_evidence"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage218_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage218_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage217_micro_interpolation_followup_review(217단계 미세 보간 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage218 review-only closeout; not final and not deployment.",
        }
    ]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "notes": f"source_run={SOURCE_RUN_ID}; best_stage217_row={best.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "best_stage217_row": best.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
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
        f"""# Stage218 Closeout Packet(218단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(best: Mapping[str, Any]) -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage219(219단계)은 Stage218(218단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can entry/lifecycle repair(진입/생애주기 수리), with the bracket axis(브래킷 축) held constant, recover validation net(검증 순손익), validation mid PF(검증 중반 수익요인), early PF(초반 수익요인), and OOS net(표본외 순손익) after Stage217(217단계) proved SL/TP micro interpolation(손절/익절 미세 보간) weak?

Effect(효과): 같은 bracket microgrid(브래킷 미세 격자)를 반복하지 않고, 진입 타이밍/재진입/보유 생애주기만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage219 Input References(219단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage217_quality_matrix(원천 217단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage217_risk_atr_telemetry(원천 217단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    s172.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"# Stage219 Review Index(219단계 검토 색인)\n\n- status(상태): `open_planned_from_stage218`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n")
    s172.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"# Stage219 Selection Status(219단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage218`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{DECISION}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def update_current_truth(best: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage218(218단계) closed(종료) as `{DECISION}` and Stage219(219단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage217(217단계)의 SL/TP micro interpolation(손절/익절 미세 보간) 축을 중단하고 entry/lifecycle repair(진입/생애주기 수리)로 전환한다.
- >-
  Stage218 evidence(218단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): bracket axis failure(브래킷 축 실패)를 failure memory(실패 기억)로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage218_stage217_micro_interpolation_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage218_stage217_micro_interpolation_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  best_stage217_row: {best.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `entry_lifecycle_repair_after_bracket_axis_failure`
- status(상태): `stage218_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage218(218단계)는 Stage217(217단계) micro interpolation(미세 보간) 결과를 follow-up review(후속 검토)했다. Effect(효과): Stage219(219단계)는 bracket axis(브래킷 축)를 멈추고 entry/lifecycle(진입/생애주기)을 좁게 수리한다.

## Latest Stage218 Evidence(최신 218단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(best: Mapping[str, Any]) -> None:
    s172.write_md(SELECTED_ROOT / "selection_status.md", f"# Stage218 Selection Status(218단계 선택 상태)\n\n- stage_status(단계 상태): `closed_{DECISION}`\n- current_packet(현재 작업 묶음): `{PACKET_ID}`\n- current_run(현재 실행): `{RUN_ID}`\n- source_stage(원천 단계): `{SOURCE_STAGE_ID}`\n- source_run(원천 실행): `{SOURCE_RUN_ID}`\n- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`\n- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`\n- decision(판정): `{DECISION}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")
    s172.write_md(REVIEWS_ROOT / "review_index.md", f"# Stage218 Review Index(218단계 검토 색인)\n\n- status(상태): `closed_{DECISION}`\n- packet(작업 묶음): `{PACKET_ID}`\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- best_stage217_row(최선 217단계 행): `{best.get('adapter_id', '')}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`\n- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`\n- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n")


def append_changelog(best: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage218 Stage217 micro interpolation follow-up review closeout(218단계 217단계 미세 보간 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): recorded(기록) `{best.get('adapter_id', '')}` as best failed row(최선 실패 행) and opened(개방) Stage219(219단계) entry/lifecycle repair(진입/생애주기 수리).\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    json.loads(io_path(SOURCE_SUMMARY_PATH).read_text(encoding="utf-8-sig"))
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    monthly_rows = read_csv(SOURCE_MONTHLY_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    risk_rows = read_csv(SOURCE_RISK_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, monthly_rows, concentration_rows, risk_rows)
    best = best_row(tradeoff_rows)
    attribution_rows = build_attribution_rows(best)
    route_rows = build_route_rows(best)
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows, best))
    s172.write_md(DECISION_PATH, decision_md(best))
    write_ledgers(best)
    payload = {
        "run_id": RUN_ID,
        "decision": DECISION,
        "best_stage217_row": best.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "route_rows": route_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(SUMMARY_JSON_PATH, payload)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, best)
    write_next_stage_seed(best)
    update_current_truth(best)
    write_status_files(best)
    append_changelog(best)
    print(json.dumps(json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "best_stage217_row": best.get("adapter_id", ""), "overall_goal_complete": False, "report": rel(REPORT_PATH)}), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

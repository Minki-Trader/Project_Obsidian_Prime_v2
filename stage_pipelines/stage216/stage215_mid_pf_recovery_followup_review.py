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

STAGE_ID = "216_adapter_research__stage215_mid_pf_recovery_followup_review"
RUN_ID = "run216A_stage216_stage215_mid_pf_recovery_followup_review_v1"
PACKET_ID = "stage216_stage215_mid_pf_recovery_followup_review_v1"
PARENT_RUN_ID = "run215A_stage215_validation_mid_pf_recovery_preserve_oos_gain_v1"
SOURCE_STAGE_ID = "215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain"
SOURCE_RUN_ID = "run215A_stage215_validation_mid_pf_recovery_preserve_oos_gain_v1"
SOURCE_STAGE215_EVIDENCE_COMMIT = "1d6a2a4b1cda23981bb09e3fb4dfefa1cdd85825"
SOURCE_STAGE215_HASH_RECORD_COMMIT = "ada5f5d5d1b061aad906028e9e22ae9f94e4da14"
NEXT_STAGE_ID = "217_adapter_research__oos_preserving_mid_pf_micro_interpolation"
NEXT_RUN_ID = "run217A_stage217_oos_preserving_mid_pf_micro_interpolation_v1"
NEXT_PACKET_ID = "stage217_oos_preserving_mid_pf_micro_interpolation_v1"
DECISION = "open_stage217_bounded_oos_preserving_mid_pf_micro_interpolation_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage215_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_oos_preserving_mid_pf_recovery"
BOUNDARY = s213.BOUNDARY
LEGACY_34D = s213.LEGACY_34D
STAGE210_ANCHOR = {
    "adapter_id": "s210_ls_r0315",
    "validation_net": 1200.27,
    "validation_mid_pf": 1.695877099,
    "validation_dd": 12.6726,
    "oos_net": 714.86,
}
STAGE213_PROBE = {
    "adapter_id": "s213_r03125_s200_t455",
    "validation_net": 993.92,
    "validation_mid_pf": 1.541362846,
    "validation_dd": 12.6649,
    "oos_net": 749.91,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_summary.json")
SOURCE_QUALITY_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_quality_matrix.csv")
SOURCE_MONTHLY_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_monthly_kpi_summary.csv")
SOURCE_CONCENTRATION_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_concentration_risk_summary.csv")
SOURCE_RISK_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_mid_pf_recovery_report.md")
SOURCE_DECISION_PATH = Path("stages/215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain/03_reviews/stage215_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage216_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage216_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage216_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage216_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage216_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage216_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage216/stage215_mid_pf_recovery_followup_review.py")
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


def pass_mid_recovery(row: Mapping[str, Any]) -> bool:
    return (
        fnum(row.get("validation_mid_pf")) >= float(LEGACY_34D["profit_factor"])
        and fnum(row.get("validation_net")) >= float(LEGACY_34D["net_profit"])
        and fnum(row.get("validation_balance_dd_percent")) <= float(LEGACY_34D["max_drawdown_percent"])
    )


def pass_oos_preserve(row: Mapping[str, Any]) -> bool:
    return fnum(row.get("oos_net")) >= STAGE210_ANCHOR["oos_net"]


def profile_label(row: Mapping[str, Any]) -> str:
    mid_ok = pass_mid_recovery(row)
    oos_ok = pass_oos_preserve(row)
    if mid_ok and oos_ok:
        return "full_stage215_pass_not_observed(215단계 완전 통과, 관측 안 됨)"
    if mid_ok and not oos_ok:
        return "mid_pf_recovered_oos_failed(중반 수익요인 회복, 표본외 실패)"
    if oos_ok and not mid_ok:
        return "oos_preserved_mid_pf_failed(표본외 보존, 중반 수익요인 실패)"
    return "both_required_surfaces_failed(두 필수 표면 모두 실패)"


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
                "validation_net_delta_vs_stage213_probe": round(fnum(row.get("validation_net")) - STAGE213_PROBE["validation_net"], 2),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(fnum(row.get("validation_mid_pf")) - float(LEGACY_34D["profit_factor"]), 6),
                "validation_mid_pf_delta_vs_stage213_probe": round(fnum(row.get("validation_mid_pf")) - STAGE213_PROBE["validation_mid_pf"], 6),
                "validation_negative_month_count": val_months["negative_month_count"],
                "validation_pf_below_34d_month_count": val_months["pf_below_34d_count"],
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_stage210_anchor": round(fnum(row.get("oos_net")) - STAGE210_ANCHOR["oos_net"], 2),
                "oos_net_delta_vs_stage213_probe": round(fnum(row.get("oos_net")) - STAGE213_PROBE["oos_net"], 2),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_negative_month_count": oos_months["negative_month_count"],
                "oos_negative_months": oos_months["negative_months"],
                "oos_negative_month_net": oos_months["negative_month_net"],
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "validation_avg_actual_risk_pct_after_floor": val_risk.get("avg_actual_risk_pct_after_floor", ""),
                "oos_avg_actual_risk_pct_after_floor": oos_risk.get("avg_actual_risk_pct_after_floor", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def best_oos_preserver(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if fnum(row.get("oos_net")) >= STAGE210_ANCHOR["oos_net"]]
    return max(candidates or rows, key=lambda row: fnum(row.get("oos_net")), default={})


def best_mid_recovery(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if pass_mid_recovery(row)]
    return max(candidates or rows, key=lambda row: (fnum(row.get("validation_mid_pf")), fnum(row.get("validation_net"))), default={})


def build_attribution_rows(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "stage215_split_the_surface(215단계가 표면을 둘로 갈랐음)",
            "comparison_baseline": "Stage210 anchor(210단계 기준 후보) and Stage213 probe(213단계 탐침)",
            "likely_drivers": "SL/TP_bracket_width_controls_mid_pf_vs_oos_tradeoff(손절/익절 브래킷 폭이 중반 수익요인과 표본외 상충을 지배)",
            "segment_checks": f"best_oos={oos_row.get('adapter_id')}:{oos_row.get('oos_net')};best_mid={mid_row.get('adapter_id')}:{mid_row.get('validation_mid_pf')}",
            "trade_shape": f"best_mid_oos_gap_vs_stage210={mid_row.get('oos_net_delta_vs_stage210_anchor')};best_oos_mid_gap_vs_34d={oos_row.get('validation_mid_pf_gap_vs_34d')}",
            "alternative_explanations": "early_validation_pf_remains_weak(검증 초반 수익요인이 계속 약함)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "micro_interpolate_between_brackets(브래킷 사이 미세 보간)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "risk_floor_not_driver(최소 로트 위험 바닥은 원인이 아님)",
            "comparison_baseline": "Stage215 risk/ATR telemetry(215단계 위험/ATR 기록)",
            "likely_drivers": "risk_floor_count_zero(위험 바닥 적용 수 0)",
            "segment_checks": f"oos_row_floor={oos_row.get('oos_risk_floor_applied_count')};mid_row_floor={mid_row.get('oos_risk_floor_applied_count')}",
            "trade_shape": "ATR bracket choice changed payoff, not lot floor(ATR 브래킷 선택이 보상을 바꿨고 로트 바닥은 아님)",
            "alternative_explanations": "model risk cap may still shift lot scaling(모델 위험 상한은 여전히 로트 배율을 바꿀 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "hold risk cap near 0.03125 while testing bracket midpoint(위험 상한을 0.03125 근처에 두고 브래킷 중간값 시험)",
        },
    ]


def build_route_rows(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "do_not_promote_stage215(215단계 승격 금지)",
            "adapter_id": "none",
            "action": "keep_research_development_only(연구개발 전용 유지)",
            "effect": "prevents_partial_kpi_recovery_from_becoming_final_claim(부분 KPI 회복이 최종 주장으로 바뀌지 않게 함)",
            "risk": "overall_goal_not_complete(전체 목표 미완료)",
        },
        {
            "run_id": RUN_ID,
            "route": "stage217_micro_interpolation(217단계 미세 보간)",
            "adapter_id": f"{oos_row.get('adapter_id')} -> {mid_row.get('adapter_id')}",
            "action": "test_narrow_SLTP_midpoints_and_small_risk_cap_blend(좁은 손절/익절 중간값과 작은 위험 상한 혼합 시험)",
            "effect": "targets_oos_gap_less_than_10_without_reopening_broad_search(10 미만 표본외 차이를 노리고 넓은 탐색을 다시 열지 않음)",
            "risk": "early_validation_pf_may_remain_weak(검증 초반 수익요인이 계속 약할 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "preserve_stage210_anchor(210단계 후보 보존)",
            "adapter_id": STAGE210_ANCHOR["adapter_id"],
            "action": "keep_as_reference_not_final(참조 후보로 보존, 최종 아님)",
            "effect": "maintains_validation_stability_reference_while_repair_continues(수리 중에도 검증 안정성 참조를 유지)",
            "risk": "oos_monthly_weakness_unrepaired(표본외 월별 약점은 수리되지 않음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> str:
    lines = [
        "# Stage216 Follow-up Review(216단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage215_evidence_commit(원천 215단계 근거 커밋): `{SOURCE_STAGE215_EVIDENCE_COMMIT}`",
        f"- source_stage215_hash_record_commit(원천 215단계 해시 기록 커밋): `{SOURCE_STAGE215_HASH_RECORD_COMMIT}`",
        f"- decision(판정): `{DECISION}`",
        f"- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`",
        f"- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | profile(유형) | val net gap(검증 순손익 차이) | mid PF gap(중반 수익요인 차이) | OOS vs 210(210 대비 표본외) | OOS vs 213(213 대비 표본외) | early PF(초반 수익요인) | risk floor(위험 바닥) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('profile_label', '')} | {row.get('validation_net_gap_vs_34d', '')} | {row.get('validation_mid_pf_gap_vs_34d', '')} | {row.get('oos_net_delta_vs_stage210_anchor', '')} | {row.get('oos_net_delta_vs_stage213_probe', '')} | {row.get('validation_early_pf', '')} | {row.get('oos_risk_floor_applied_count', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- `{oos_row.get('adapter_id', '')}`는 OOS net(표본외 순손익) `{oos_row.get('oos_net', '')}`로 Stage210(210단계) 기준을 넘겼지만 validation mid PF(검증 중반 수익요인)는 `{oos_row.get('validation_mid_pf', '')}`로 약했다.",
            f"- `{mid_row.get('adapter_id', '')}`는 validation mid PF(검증 중반 수익요인) `{mid_row.get('validation_mid_pf', '')}`와 validation net(검증 순손익) `{mid_row.get('validation_net', '')}`를 회복했지만 OOS net(표본외 순손익)은 `{mid_row.get('oos_net', '')}`로 Stage210(210단계) 기준보다 `{mid_row.get('oos_net_delta_vs_stage210_anchor', '')}` 낮았다.",
            "- risk floor(위험 바닥)는 0건이라 이번 상충의 주원인으로 보지 않는다.",
            "- Stage216(216단계)는 final(최종), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.",
            "- Effect(효과): Stage217(217단계)는 넓은 탐색이 아니라 SL/TP(손절/익절)와 risk cap(위험 상한)의 좁은 미세 보간만 시험한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> str:
    return f"""# Stage216 Decision(216단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage215_evidence_commit(원천 215단계 근거 커밋): `{SOURCE_STAGE215_EVIDENCE_COMMIT}`
- source_stage215_hash_record_commit(원천 215단계 해시 기록 커밋): `{SOURCE_STAGE215_HASH_RECORD_COMMIT}`
- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`
- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage216(216단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage217(217단계)에서 OOS preservation(표본외 보존)과 mid PF recovery(중반 수익요인 회복)를 좁은 micro interpolation(미세 보간)으로 다시 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage216_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage216 Stage215 mid PF recovery follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("best_oos_preserver", oos_row.get("adapter_id", "")),
            ("best_oos_net", oos_row.get("oos_net", "")),
            ("best_mid_recovery", mid_row.get("adapter_id", "")),
            ("best_mid_pf", mid_row.get("validation_mid_pf", "")),
            ("best_mid_oos_gap_vs_stage210", mid_row.get("oos_net_delta_vs_stage210_anchor", "")),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("decision", DECISION),
            ("next_stage", NEXT_STAGE_ID),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage216_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage216_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage215_mid_pf_recovery_followup_review(215단계 중반 수익요인 회복 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage216 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; best_oos_preserver={oos_row.get('adapter_id', '')}; best_mid_recovery={mid_row.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    oos_row: Mapping[str, Any],
    mid_row: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "best_oos_preserver": oos_row.get("adapter_id", ""),
        "best_mid_recovery": mid_row.get("adapter_id", ""),
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
        f"""# Stage216 Closeout Packet(216단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`
- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage217(217단계)은 Stage216(216단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a narrow micro interpolation(미세 보간) between `{oos_row.get('adapter_id', '')}` and `{mid_row.get('adapter_id', '')}` preserve OOS net(표본외 순손익) above Stage210(210단계) while keeping validation mid PF(검증 중반 수익요인), validation net(검증 순손익), validation DD(검증 낙폭), early PF(초반 수익요인), and risk/ATR telemetry(위험/ATR 기록) acceptable?

Effect(효과): Stage215(215단계)의 넓은 tradeoff(상충)를 다시 넓히지 않고, OOS gap(표본외 차이) 약 6-9 단위만 좁게 복구한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage217 Input References(217단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`
- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage215_quality_matrix(원천 215단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage215_risk_atr_telemetry(원천 215단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"# Stage217 Review Index(217단계 검토 색인)\n\n- status(상태): `open_planned_from_stage216`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"# Stage217 Selection Status(217단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage216`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`\n- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n",
    )


def update_current_truth(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage216(216단계) closed(종료) as `{DECISION}` and Stage217(217단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage215(215단계)의 OOS preservation(표본외 보존)과 mid PF recovery(중반 수익요인 회복) 상충을 좁은 micro interpolation(미세 보간)으로 시험한다.
- >-
  Stage216 evidence(216단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): `{oos_row.get('adapter_id', '')}`와 `{mid_row.get('adapter_id', '')}` 사이의 다음 수리 범위를 제한한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage216_stage215_mid_pf_recovery_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage216_stage215_mid_pf_recovery_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  best_oos_preserver: {oos_row.get('adapter_id', '')}
  best_mid_recovery: {mid_row.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `{oos_row.get('adapter_id', '')} to {mid_row.get('adapter_id', '')}`
- status(상태): `stage216_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage216(216단계)는 Stage215(215단계) mid PF recovery(중반 수익요인 회복) 결과를 follow-up review(후속 검토)했다. Effect(효과): Stage217(217단계)는 OOS preservation(표본외 보존)과 validation mid PF recovery(검증 중반 수익요인 회복)를 좁게 동시에 시험한다.

## Latest Stage216 Evidence(최신 216단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`
- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> None:
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"# Stage216 Selection Status(216단계 선택 상태)\n\n- stage_status(단계 상태): `closed_{DECISION}`\n- current_packet(현재 작업 묶음): `{PACKET_ID}`\n- current_run(현재 실행): `{RUN_ID}`\n- source_stage(원천 단계): `{SOURCE_STAGE_ID}`\n- source_run(원천 실행): `{SOURCE_RUN_ID}`\n- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`\n- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`\n- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`\n- decision(판정): `{DECISION}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n",
    )
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"# Stage216 Review Index(216단계 검토 색인)\n\n- status(상태): `closed_{DECISION}`\n- packet(작업 묶음): `{PACKET_ID}`\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- best_oos_preserver(최선 표본외 보존): `{oos_row.get('adapter_id', '')}`\n- best_mid_recovery(최선 중반 회복): `{mid_row.get('adapter_id', '')}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`\n- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`\n- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n",
    )


def append_changelog(oos_row: Mapping[str, Any], mid_row: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage216 Stage215 mid PF recovery follow-up review closeout(216단계 215단계 중반 수익요인 회복 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): routed(라우팅) Stage217(217단계) to micro interpolation(미세 보간) between `{oos_row.get('adapter_id', '')}` and `{mid_row.get('adapter_id', '')}`.\n"
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
    oos_row = best_oos_preserver(tradeoff_rows)
    mid_row = best_mid_recovery(tradeoff_rows)
    attribution_rows = build_attribution_rows(oos_row, mid_row)
    route_rows = build_route_rows(oos_row, mid_row)
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows, oos_row, mid_row))
    s172.write_md(DECISION_PATH, decision_md(oos_row, mid_row))
    write_ledgers(oos_row, mid_row)
    payload = {
        "run_id": RUN_ID,
        "decision": DECISION,
        "best_oos_preserver": oos_row.get("adapter_id", ""),
        "best_mid_recovery": mid_row.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "route_rows": route_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(SUMMARY_JSON_PATH, payload)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, oos_row, mid_row)
    write_next_stage_seed(oos_row, mid_row)
    update_current_truth(oos_row, mid_row)
    write_status_files(oos_row, mid_row)
    append_changelog(oos_row, mid_row)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "best_oos_preserver": oos_row.get("adapter_id", ""),
                    "best_mid_recovery": mid_row.get("adapter_id", ""),
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

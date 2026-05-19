from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)

STAGE_ID = "224_adapter_research__stage223_oos_recovery_followup_review"
RUN_ID = "run224A_stage224_stage223_oos_recovery_followup_review_v1"
PACKET_ID = "stage224_stage223_oos_recovery_followup_review_v1"
PARENT_RUN_ID = "run223A_stage223_oos_recovery_after_no_long_block_validation_gain_v1"
SOURCE_STAGE_ID = "223_adapter_research__oos_recovery_after_no_long_block_validation_gain"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE223_EVIDENCE_COMMIT = "ef25cfecc56dde0bf1ba6f60e9568f4d0f9002e1"
SOURCE_STAGE223_HASH_RECORD_COMMIT = "e71560872f89334de213ad77d5d617ff3bf83bc5"
NEXT_STAGE_ID = "225_adapter_research__validation_recovery_after_lowedge_oos_gain"
NEXT_RUN_ID = "run225A_stage225_validation_recovery_after_lowedge_oos_gain_v1"
NEXT_PACKET_ID = "stage225_validation_recovery_after_lowedge_oos_gain_v1"
DECISION = "open_stage225_bounded_validation_recovery_after_lowedge_oos_gain_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage223_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_validation_recovery_after_lowedge_oos_gain"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}
STAGE219_CONTROL = {
    "validation_net": 952.16,
    "validation_mid_pf": 1.541193855,
    "validation_early_pf": 1.563704148,
    "validation_dd": 12.6953,
    "oos_net": 719.48,
}
STAGE223_OOS_GAIN = {
    "adapter_id": "s223_oos_lowedge_long_guard",
    "validation_net": 833.22,
    "validation_mid_pf": 1.498515715,
    "validation_early_pf": 1.446826244,
    "validation_dd": 13.0158,
    "oos_net": 765.40,
    "oos_pf": 1.93,
    "oos_dd": 7.7935,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_SUMMARY_PATH = SOURCE_ROOT / "stage223_summary.json"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage223_quality_matrix.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage223_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage223_concentration_risk_summary.csv"
SOURCE_RISK_PATH = SOURCE_ROOT / "stage223_risk_atr_telemetry.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage223_segment_kpi_summary.csv"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage223_oos_recovery_report.md"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage223_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage224_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage224_oos_validation_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage224_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage224_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage224_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage224_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage224/stage223_oos_recovery_followup_review.py")
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
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


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


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def lookup(rows: Sequence[Mapping[str, Any]], **filters: str) -> Mapping[str, Any]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in filters.items()):
            return row
    return {}


def monthly_stats(monthly_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> dict[str, Any]:
    rows = [row for row in monthly_rows if row.get("adapter_id") == adapter_id and row.get("split") == split]
    negative = [row for row in rows if fnum(row.get("net_profit")) <= 0.0]
    pf_below = [row for row in rows if fnum(row.get("profit_factor")) < LEGACY_34D["profit_factor"]]
    return {
        "month_count": len(rows),
        "negative_month_count": len(negative),
        "negative_months": ",".join(str(row.get("month", "")) for row in negative),
        "pf_below_34d_count": len(pf_below),
        "net_profit": round(sum(fnum(row.get("net_profit")) for row in rows), 2),
    }


def profile_label(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    if adapter_id == "s223_oos_control_no_long":
        return "validation_gain_oos_failed(검증 개선, 표본외 실패)"
    if adapter_id == "s223_oos_tight_long_guard":
        return "control_reversion_oos_restored_validation_failed(대조군 회귀, 표본외 회복, 검증 실패)"
    if adapter_id == "s223_oos_wide_long_guard":
        return "wide_guard_damaged_validation_without_oos_recovery(넓은 보호, 검증 손상, 표본외 미회복)"
    if adapter_id == "s223_oos_lowedge_long_guard":
        return "oos_gain_validation_damage(표본외 개선, 검증 손상)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    concentration_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_months = monthly_stats(monthly_rows, adapter_id, "validation_is")
        oos_months = monthly_stats(monthly_rows, adapter_id, "oos")
        val_conc = lookup(concentration_rows, adapter_id=adapter_id, split="validation_is")
        oos_conc = lookup(concentration_rows, adapter_id=adapter_id, split="oos")
        val_risk = lookup(risk_rows, adapter_id=adapter_id, split="validation_is", view="actual_routed_total")
        oos_risk = lookup(risk_rows, adapter_id=adapter_id, split="oos", view="actual_routed_total")
        val_mid = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="validation_is",
            view="actual_routed_total",
            segment_type="chronological_third",
            segment="mid",
        )
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "profile_label": profile_label(row),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_no_long": round(fnum(row.get("validation_net")) - 1050.87, 2),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(fnum(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_late_share": row.get("validation_late_net_share", ""),
                "validation_mid_mfe_capture_ratio": val_mid.get("mfe_capture_ratio", ""),
                "validation_pf_below_34d_month_count": val_months["pf_below_34d_count"],
                "validation_negative_month_count": val_months["negative_month_count"],
                "validation_top5_winner_share": val_conc.get("top5_winner_share_of_net", ""),
                "validation_last_quarter_share": val_conc.get("last_quarter_net_share", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_no_long": round(fnum(row.get("oos_net")) - 626.79, 2),
                "oos_net_delta_vs_stage219_control": round(fnum(row.get("oos_net")) - STAGE219_CONTROL["oos_net"], 2),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_pf_below_34d_month_count": oos_months["pf_below_34d_count"],
                "oos_negative_month_count": oos_months["negative_month_count"],
                "oos_negative_months": oos_months["negative_months"],
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def oos_gain_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == "s223_oos_lowedge_long_guard":
            return row
    return max(rows, key=lambda row: fnum(row.get("oos_net")), default={})


def build_attribution_rows(clue: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "finding": "lowedge_long_guard_recovers_oos_but_damages_validation(저엣지 롱 보호는 표본외를 회복하지만 검증을 손상)",
            "evidence": "OOS net 765.40, OOS PF 1.93, OOS DD 7.7935(표본외 순손익/수익요인/낙폭 개선)",
            "damage": "validation net 833.22, early PF 1.446826, mid PF 1.498516, DD 13.0158(검증 순손익/초반/중반/낙폭 손상)",
            "interpretation": "long_guard_axis_can_recover_oos_but_overfilters_validation(롱 보호 축은 표본외를 살리지만 검증을 과필터링)",
            "next_use": "preserve_lowedge_oos_gain_as_repair_clue(저엣지 표본외 개선을 수리 단서로 보존)",
        },
        {
            "run_id": RUN_ID,
            "finding": "no_long_block_keeps_validation_gain_but_oos_fails(롱 차단 없음은 검증 개선을 지키지만 표본외 실패)",
            "evidence": "validation net 1050.87, early PF 1.604594, DD 11.6030(검증 개선)",
            "damage": "OOS net 626.79 and validation mid PF 1.484282(표본외 순손익과 검증 중반 PF 실패)",
            "interpretation": "validation_and_oos_need_combined_repair_not_single_guard_toggle(검증과 표본외는 단순 보호 토글이 아니라 결합 수리가 필요)",
            "next_use": "do_not_mark_no_long_block_final(no_long_block을 최종으로 표시하지 않음)",
        },
        {
            "run_id": RUN_ID,
            "finding": "tight_long_guard_reverts_to_stage219_control(좁은 롱 보호는 Stage219 대조군으로 회귀)",
            "evidence": "validation net 952.16 and OOS net 719.48 exactly match the prior control shape(이전 대조군 형태 재현)",
            "damage": "still below 34D validation net, early PF, and mid PF(34D 검증 순손익/초반/중반 PF 미달)",
            "interpretation": "tight_guard_is_safety_reversion_not_improvement(좁은 보호는 안전 회귀이지 개선이 아님)",
            "next_use": "keep_as_reference_only(참조로만 보존)",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk_floor_not_driver(위험 바닥은 주원인 아님)",
            "evidence": f"risk_floor_counts val={clue.get('validation_risk_floor_applied_count')} oos={clue.get('oos_risk_floor_applied_count')}",
            "damage": "remaining problem is selection balance(남은 문제는 선택 균형)",
            "interpretation": "next_stage_should_not_be_standalone_risk_campaign(다음 단계는 위험 단독 캠페인이 아니어야 함)",
            "next_use": "keep_risk_atr_telemetry_mandatory(위험/ATR 기록은 필수 유지)",
        },
    ]


def build_route_rows(clue: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "open_stage225_validation_recovery_after_lowedge_oos_gain(225단계 저엣지 표본외 개선 뒤 검증 회복 개방)",
            "adapter_id": clue.get("adapter_id", ""),
            "action": "repair_validation_after_preserving_lowedge_oos_gain(저엣지 표본외 개선을 보존한 뒤 검증 회복 수리)",
            "effect": "targets_the_new_tradeoff_directly(새 상충을 직접 겨냥)",
            "risk": "may_lose_oos_gain_when_validation_is_recovered(검증 회복 시 표본외 개선을 잃을 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "preserve_no_long_and_lowedge_as_pair(롱 차단 없음과 저엣지 롱 보호를 쌍으로 보존)",
            "adapter_id": "s223_oos_control_no_long;s223_oos_lowedge_long_guard",
            "action": "use_pair_as_bounds_for_next_repair(다음 수리의 양끝 경계로 사용)",
            "effect": "prevents_repeating_single_toggle_search(단일 토글 반복 탐색 방지)",
            "risk": "requires_careful_bounded_axis_selection(조심스러운 경계 축 선택 필요)",
        },
        {
            "run_id": RUN_ID,
            "route": "stop_wide_long_guard_axis(넓은 롱 보호 축 중단)",
            "adapter_id": "s223_oos_wide_long_guard",
            "action": "record_as_negative_evidence(부정 근거로 기록)",
            "effect": "keeps_stage225_from_repeating_damaged_variant(Stage225에서 손상 변형 반복 방지)",
            "risk": "one_untried_wide_window_may_be_missed(미시도 넓은 창 하나를 놓칠 수 있음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], clue: Mapping[str, Any]) -> str:
    lines = [
        "# Stage224 Follow-up Review(224단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- decision(판정): `{DECISION}`",
        f"- oos_gain_clue(표본외 개선 단서): `{clue.get('adapter_id', '')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "- Stage223(223단계)는 OOS(표본외)를 살리는 방법을 하나 찾았다.",
        "- `s223_oos_lowedge_long_guard`는 OOS net(표본외 순손익)을 765.40까지 올렸지만 validation(검증)을 크게 깎았다.",
        "- `s223_oos_control_no_long`은 validation(검증)은 좋지만 OOS(표본외)가 약하다.",
        "- 따라서 다음은 lowedge OOS gain(저엣지 표본외 개선)을 보존하면서 validation(검증)을 회복하는 Stage225(225단계)다.",
        "",
        "## KPI Tradeoff(KPI 상충)",
        "",
        "| adapter(어댑터) | profile(유형) | val net(검증 순손익) | mid PF(중반 PF) | OOS net(표본외 순손익) | OOS vs no-long(표본외 no-long 대비) | OOS vs control(표본외 대조군 대비) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('profile_label', '')} | "
            f"{row.get('validation_net', '')} | {row.get('validation_mid_pf', '')} | "
            f"{row.get('oos_net', '')} | {row.get('oos_net_delta_vs_no_long', '')} | "
            f"{row.get('oos_net_delta_vs_stage219_control', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage223 OOS recovery long guard axis(223단계 표본외 회복 롱 보호 축).",
            "- evidence_available(사용 근거): Stage223 MT5 Strategy Tester(MetaTrader 5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).",
            "- evidence_missing(부족 근거): 표본외 개선을 보존한 상태의 validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인) 회복.",
            "- judgment_label(판정 라벨): oos_gain_with_validation_damage_not_final(표본외 개선과 검증 손상, 최종 아님).",
            "- next_condition(다음 조건): Stage225(225단계)에서 lowedge OOS gain(저엣지 표본외 개선)을 보존하면서 validation(검증)을 회복해야 한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(clue: Mapping[str, Any]) -> str:
    return f"""# Stage224 Decision(224단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage223_evidence_commit(원천 223단계 근거 커밋): `{SOURCE_STAGE223_EVIDENCE_COMMIT}`
- source_stage223_hash_record_commit(원천 223단계 해시 기록 커밋): `{SOURCE_STAGE223_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- oos_gain_clue(표본외 개선 단서): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage224(224단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage225(225단계)는 `s223_oos_lowedge_long_guard`의 OOS gain(표본외 개선)을 보존하면서 validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인)를 회복하는지만 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage224_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage224 Stage223 OOS recovery follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(clue: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("oos_gain_clue", clue.get("adapter_id", "")),
            ("validation_net", clue.get("validation_net", "")),
            ("validation_mid_pf", clue.get("validation_mid_pf", "")),
            ("oos_net", clue.get("oos_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage224_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage224_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage224_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage223_oos_recovery_followup_review(223단계 표본외 회복 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage224 review-only closeout; not final and not deployment.",
        }
    ]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "notes": f"source_run={SOURCE_RUN_ID}; oos_gain_clue={clue.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], clue: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "oos_gain_clue": clue.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": list(tradeoff_rows),
        "attribution_rows": list(attribution_rows),
        "route_rows": list(route_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage224 Closeout Packet(224단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- oos_gain_clue(표본외 개선 단서): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(clue: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage225(225단계)는 Stage224(224단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can validation net(검증 순손익), early PF(초반 수익요인), and mid PF(중반 수익요인) be recovered after the `s223_oos_lowedge_long_guard` OOS gain(표본외 개선), while preserving OOS net(표본외 순손익), drawdown(낙폭), model-controlled risk%(모델 제어 위험 비율), and ATR/bracket behavior(ATR/브래킷 동작)?

Effect(효과): Stage223(223단계)의 OOS gain(표본외 개선)을 버리지 않되, 34D(34D 기준)에 못 미친 validation(검증)만 좁게 겨냥한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage225 Input References(225단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- oos_gain_clue(표본외 개선 단서): `{clue.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage223_quality_matrix(원천 223단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage223_risk_atr_telemetry(원천 223단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage225 Review Index(225단계 검토 색인)

- status(상태): `open_planned_from_stage224`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage225 Selection Status(225단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage224`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(clue: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage224(224단계) closed(종료) as `{DECISION}` and Stage225(225단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): lowedge long guard(저엣지 롱 보호)의 OOS gain(표본외 개선)을 보존하면서 validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인) 회복만 좁게 시험한다.
- >-
  Stage224 evidence(224단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): Stage223(223단계) 상충은 oos_gain_validation_damage(표본외 개선, 검증 손상)로 기록된다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage224_stage223_oos_recovery_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage224_stage223_oos_recovery_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  oos_gain_clue: {clue.get('adapter_id', '')}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_MATRIX_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
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
- adapter_under_review(검토 중 어댑터): `s223_oos_lowedge_long_guard_as_oos_gain_clue_not_final`
- status(상태): `stage224_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage224(224단계)는 Stage223(223단계) OOS recovery(표본외 회복)를 review-only(검토 전용)로 판정했다. Effect(효과): Stage225(225단계)는 lowedge OOS gain(저엣지 표본외 개선)을 보존하면서 validation(검증) 회복을 좁게 시험한다.

## Latest Stage224 Evidence(최신 224단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- oos_gain_clue(표본외 개선 단서): `{clue.get('adapter_id', '')}`
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
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage224 Selection Status(224단계 선택 상태)

- stage_status(단계 상태): `reviewed_closed_{DECISION}`
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
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage224 Review Index(224단계 검토 색인)

- status(상태): `reviewed_closed_{DECISION}`
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
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if io_path(CHANGELOG_PATH).exists() else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage224 OOS recovery follow-up review closeout(224단계 표본외 회복 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): lowedge long guard(저엣지 롱 보호)의 OOS gain(표본외 개선)을 보존하고 validation recovery(검증 회복)를 Stage225(225단계)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    monthly_rows = read_csv(SOURCE_MONTHLY_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    risk_rows = read_csv(SOURCE_RISK_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, monthly_rows, concentration_rows, risk_rows, segment_rows)
    clue = oos_gain_row(tradeoff_rows)
    attribution_rows = build_attribution_rows(clue)
    route_rows = build_route_rows(clue)

    write_md(REPORT_PATH, report_md(tradeoff_rows, clue))
    write_md(DECISION_PATH, decision_md(clue))
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "source_summary": rel(SOURCE_SUMMARY_PATH),
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "oos_gain_clue": clue,
            "legacy_34d": LEGACY_34D,
            "stage219_control": STAGE219_CONTROL,
            "stage223_oos_gain": STAGE223_OOS_GAIN,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_ledgers(clue)
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, clue)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_next_stage_seed(clue)
    update_current_truth(clue)
    write_status_files()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "reviewed_closed",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "oos_gain_clue": clue.get("adapter_id", ""),
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "next_stage": NEXT_STAGE_ID,
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

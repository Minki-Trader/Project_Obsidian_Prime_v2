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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage213 import s210_r0315_oos_monthly_concentration_repair as s213  # noqa: E402

s172 = s213.s172

STAGE_ID = "220_adapter_research__stage219_entry_lifecycle_followup_review"
RUN_ID = "run220A_stage220_stage219_entry_lifecycle_followup_review_v1"
PACKET_ID = "stage220_stage219_entry_lifecycle_followup_review_v1"
PARENT_RUN_ID = "run219A_stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1"
SOURCE_STAGE_ID = "219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure"
SOURCE_RUN_ID = "run219A_stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1"
SOURCE_STAGE219_EVIDENCE_COMMIT = "9f7668ccf2c2f443127c6c8001a444822ab0d5ef"
SOURCE_STAGE219_HASH_RECORD_COMMIT = "dcfa058fd05b0fe14e50cc0a13e0ff7b17218f8b"
NEXT_STAGE_ID = "221_adapter_research__entry_signal_gate_repair_after_lifecycle_axis_failure"
NEXT_RUN_ID = "run221A_stage221_entry_signal_gate_repair_after_lifecycle_axis_failure_v1"
NEXT_PACKET_ID = "stage221_entry_signal_gate_repair_after_lifecycle_axis_failure_v1"
DECISION = "open_stage221_bounded_entry_signal_gate_repair_due_to_lifecycle_axis_failure_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage219_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_entry_signal_gate_repair_after_lifecycle_axis_failure"
BOUNDARY = s213.BOUNDARY
LEGACY_34D = s213.LEGACY_34D
STAGE210_ANCHOR = {
    "adapter_id": "s210_ls_r0315",
    "validation_net": 1200.27,
    "validation_mid_pf": 1.695877099,
    "validation_dd": 12.6726,
    "oos_net": 714.86,
}
STAGE217_BEST = {
    "adapter_id": "s217_r031375_s20325_t4615",
    "validation_net": 952.16,
    "validation_mid_pf": 1.541193855,
    "validation_early_pf": 1.563704148,
    "validation_dd": 12.6953,
    "oos_net": 719.48,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_summary.json")
SOURCE_QUALITY_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_quality_matrix.csv")
SOURCE_MONTHLY_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_monthly_kpi_summary.csv")
SOURCE_CONCENTRATION_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_concentration_risk_summary.csv")
SOURCE_RISK_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_entry_lifecycle_repair_report.md")
SOURCE_DECISION_PATH = Path("stages/219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure/03_reviews/stage219_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage220_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage220_lifecycle_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage220_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage220_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage220_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage220_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage220/stage219_entry_lifecycle_followup_review.py")
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


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, view: str | None = None) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") != adapter_id or row.get("split") != split:
            continue
        if view is None or row.get("view") == view:
            return row
    return {}


def monthly_stats(monthly_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> dict[str, Any]:
    rows = [row for row in monthly_rows if row.get("adapter_id") == adapter_id and row.get("split") == split]
    negative = [row for row in rows if fnum(row.get("net_profit")) <= 0.0]
    pf_below = [row for row in rows if fnum(row.get("profit_factor")) < float(LEGACY_34D["profit_factor"])]
    return {
        "month_count": len(rows),
        "negative_month_count": len(negative),
        "negative_months": ",".join(str(row.get("month", "")) for row in negative),
        "negative_month_net": round(sum(fnum(row.get("net_profit")) for row in negative), 2),
        "pf_below_34d_count": len(pf_below),
    }


def lifecycle_label(adapter_id: str) -> str:
    labels = {
        "s219_life_control_h3_sd8": "control_h3_sd8(대조군 보유3 재진입8)",
        "s219_life_h4_sd8": "hold4_sd8(보유4 재진입8)",
        "s219_life_h4_sd10": "hold4_sd10(보유4 재진입10)",
        "s219_life_closeonly_h4_sd8": "closeonly_h4_sd8(청산만 보유4 재진입8)",
    }
    return labels.get(adapter_id, "unknown(미확인)")


def profile_label(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    val_net = fnum(row.get("validation_net"))
    mid_pf = fnum(row.get("validation_mid_pf"))
    early_pf = fnum(row.get("validation_early_pf"))
    oos_net = fnum(row.get("oos_net"))
    if adapter_id == "s219_life_control_h3_sd8":
        return "control_reproduced_stage217_best_but_validation_failed(대조군 재현, 검증 실패)"
    if val_net < STAGE217_BEST["validation_net"] and oos_net < STAGE217_BEST["oos_net"]:
        return "lifecycle_change_damaged_validation_and_oos(생애주기 변경이 검증과 표본외 손상)"
    if mid_pf < LEGACY_34D["profit_factor"] or early_pf < LEGACY_34D["profit_factor"]:
        return "segment_pf_still_failed(구간 수익요인 여전히 실패)"
    return "review_required(검토 필요)"


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
                "lifecycle_profile": lifecycle_label(adapter_id),
                "profile_label": profile_label(row),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_stage217_best": round(fnum(row.get("validation_net")) - STAGE217_BEST["validation_net"], 2),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(fnum(row.get("validation_early_pf")) - float(LEGACY_34D["profit_factor"]), 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(fnum(row.get("validation_mid_pf")) - float(LEGACY_34D["profit_factor"]), 6),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_pf_below_34d_month_count": val_months["pf_below_34d_count"],
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_stage217_best": round(fnum(row.get("oos_net")) - STAGE217_BEST["oos_net"], 2),
                "oos_net_delta_vs_stage210_anchor": round(fnum(row.get("oos_net")) - STAGE210_ANCHOR["oos_net"], 2),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
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


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: (fnum(row.get("oos_net")), fnum(row.get("validation_net")), fnum(row.get("validation_mid_pf"))), default={})


def build_attribution_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "control_remained_best(대조군이 최선 유지)",
            "comparison_baseline": "Stage217 best and Stage219 lifecycle variants(217단계 최선과 219단계 생애주기 변형)",
            "likely_drivers": "lifecycle_axis_did_not_repair_entry_quality(생애주기 축이 진입 품질을 고치지 못함)",
            "segment_checks": f"best={best.get('adapter_id')};early_pf={best.get('validation_early_pf')};mid_pf={best.get('validation_mid_pf')}",
            "trade_shape": f"best_oos={best.get('oos_net')};best_val_net={best.get('validation_net')}",
            "alternative_explanations": "entry_signal_or_gate_quality_is_primary_remaining_axis(진입 신호 또는 게이트 품질이 남은 주축일 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "entry_signal_gate_repair_with_bracket_and_lifecycle_held_constant(브래킷과 생애주기 고정 후 진입 신호/게이트 수리)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "hold_extension_damaged_mid_pf_and_oos(보유 연장이 중반 수익요인과 표본외 손상)",
            "comparison_baseline": "s219_life_control_h3_sd8(219단계 대조군)",
            "likely_drivers": "longer_hold_kept_weak_trades_alive(긴 보유가 약한 거래를 오래 살림)",
            "segment_checks": "hold4 variants have validation mid PF near 1.25 to 1.30(보유4 변형 중반 수익요인 1.25~1.30대)",
            "trade_shape": "late_net_share_above_50pct_for_hold4_variants(보유4 변형 후반 순손익 비중 50% 초과)",
            "alternative_explanations": "entry timing could still be wrong before lifecycle sees it(생애주기 전에 진입 타이밍 자체가 틀렸을 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "do_not_extend_lifecycle_axis_without_new_entry_filter(새 진입 필터 없이 생애주기 축 연장 금지)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "risk_floor_count_zero(위험 바닥 적용 0)",
            "comparison_baseline": "Stage219 risk/ATR telemetry(219단계 위험/ATR 기록)",
            "likely_drivers": "min_lot_floor_not_primary_driver(최소 lot 바닥은 주 원인이 아님)",
            "segment_checks": f"best_risk_floor_val={best.get('validation_risk_floor_applied_count')};best_risk_floor_oos={best.get('oos_risk_floor_applied_count')}",
            "trade_shape": "risk_and_bracket_present_but_entry_segments_weak(위험/브래킷은 있으나 진입 구간 약함)",
            "alternative_explanations": "risk_cap_interacts_with_entry_quality_later(위험 상한은 이후 진입 품질과 상호작용할 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "keep_risk_and_bracket_constant_in_stage221(221단계에서 위험과 브래킷 고정)",
        },
    ]


def build_route_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stop_lifecycle_extension_axis(생애주기 연장 축 중단)",
            "adapter_id": best.get("adapter_id", ""),
            "action": "do_not_continue_hold4_or_closeonly_variants(보유4 또는 청산만 변형을 계속하지 않음)",
            "effect": "prevents_open_ended_lifecycle_tuning(끝없는 생애주기 미세조정 방지)",
            "risk": "may_skip_one_untried_lifecycle_combination(안 해본 생애주기 조합 하나를 건너뛸 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "preserve_control_as_measurement_reference(대조군을 측정 참조로 보존)",
            "adapter_id": "s219_life_control_h3_sd8",
            "action": "carry_control_bracket_risk_lifecycle_forward_as_fixed_context(대조군 브래킷/위험/생애주기를 고정 문맥으로 넘김)",
            "effect": "lets_next_stage_test_entry_signal_or_gate_only(다음 단계가 진입 신호/게이트만 시험하게 함)",
            "risk": "validation_net_still_below_34d(검증 순손익은 여전히 34D 아래)",
        },
        {
            "run_id": RUN_ID,
            "route": "open_stage221_entry_signal_gate_repair(221단계 진입 신호/게이트 수리 개방)",
            "adapter_id": "stage221_planned",
            "action": "change_entry_signal_or_gate_selectivity_with_bracket_risk_lifecycle_held_constant(브래킷/위험/생애주기 고정 후 진입 신호 또는 게이트 선별성 변경)",
            "effect": "targets_early_mid_pf_and_validation_net_without_replaying_failed_axes(실패한 축 반복 없이 초반/중반 수익요인과 검증 순손익 겨냥)",
            "risk": "overfiltering_may_damage_oos_trade_count(과필터링이 표본외 거래 수를 손상할 수 있음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> str:
    lines = [
        "# Stage220 Follow-up Review(220단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage219_evidence_commit(원천 219단계 근거 커밋): `{SOURCE_STAGE219_EVIDENCE_COMMIT}`",
        f"- source_stage219_hash_record_commit(원천 219단계 해시 기록 커밋): `{SOURCE_STAGE219_HASH_RECORD_COMMIT}`",
        f"- decision(판정): `{DECISION}`",
        f"- best_stage219_row(최선 219단계 행): `{best.get('adapter_id', '')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | profile(유형) | val net gap(검증 순손익 차이) | early PF gap(초반 수익요인 차이) | mid PF gap(중반 수익요인 차이) | OOS vs 217(217 대비 표본외) | OOS vs 210(210 대비 표본외) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('profile_label', '')} | {row.get('validation_net_gap_vs_34d', '')} | {row.get('validation_early_pf_gap_vs_34d', '')} | {row.get('validation_mid_pf_gap_vs_34d', '')} | {row.get('oos_net_delta_vs_stage217_best', '')} | {row.get('oos_net_delta_vs_stage210_anchor', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- `{best.get('adapter_id', '')}`가 best(최선)이고, 사실상 Stage217 best(217단계 최선)를 재현했다.",
            "- hold4(보유4), same-direction cooldown 10(동일 방향 대기10), close-only(청산만)는 validation net(검증 순손익), mid PF(중반 수익요인), OOS net(표본외 순손익)을 더 손상했다.",
            "- risk floor(위험 바닥) 적용은 0이라 이번 약점의 주 원인으로 보지 않는다.",
            "- 다음은 lifecycle(생애주기)이 아니라 entry signal/gate(진입 신호/게이트) 수리다.",
            "- Stage220(220단계)는 final(최종), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.",
        ]
    )
    return "\n".join(lines)


def decision_md(best: Mapping[str, Any]) -> str:
    return f"""# Stage220 Decision(220단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage219_evidence_commit(원천 219단계 근거 커밋): `{SOURCE_STAGE219_EVIDENCE_COMMIT}`
- source_stage219_hash_record_commit(원천 219단계 해시 기록 커밋): `{SOURCE_STAGE219_HASH_RECORD_COMMIT}`
- best_stage219_row(최선 219단계 행): `{best.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage220(220단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage221(221단계)에서 failed lifecycle axis(실패한 생애주기 축)를 반복하지 않고 entry signal/gate repair(진입 신호/게이트 수리)를 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage220_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage220 Stage219 entry/lifecycle follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(best: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("best_stage219_row", best.get("adapter_id", "")),
            ("best_oos_net", best.get("oos_net", "")),
            ("best_val_net", best.get("validation_net", "")),
            ("best_early_pf", best.get("validation_early_pf", "")),
            ("best_mid_pf", best.get("validation_mid_pf", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("lifecycle_axis_status", "failed_bounded_negative_evidence"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage220_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage220_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage219_entry_lifecycle_followup_review(219단계 진입/생애주기 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage220 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; best_stage219_row={best.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    best: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "best_stage219_row": best.get("adapter_id", ""),
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
    s172.write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage220 Closeout Packet(220단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- best_stage219_row(최선 219단계 행): `{best.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(best: Mapping[str, Any]) -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage221(221단계)은 Stage220(220단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can entry signal/gate repair(진입 신호/게이트 수리), with bracket/risk/lifecycle(브래킷/위험/생애주기) held constant at `{best.get('adapter_id', 's219_life_control_h3_sd8')}`, improve validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), OOS net(표본외 순손익), and drawdown(낙폭) after lifecycle axis(생애주기 축) failed?

Effect(효과): failed bracket/lifecycle axes(실패한 브래킷/생애주기 축)를 반복하지 않고 entry selectivity(진입 선별성)만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage221 Input References(221단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- best_stage219_row(최선 219단계 행): `{best.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage219_quality_matrix(원천 219단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage219_risk_atr_telemetry(원천 219단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"# Stage221 Review Index(221단계 검토 색인)\n\n- status(상태): `open_planned_from_stage220`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"# Stage221 Selection Status(221단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage220`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{DECISION}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n",
    )


def update_current_truth(best: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage220(220단계) closed(종료) as `{DECISION}` and Stage221(221단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): lifecycle axis(생애주기 축)을 중단하고 entry signal/gate repair(진입 신호/게이트 수리)로 전환한다.
- >-
  Stage220 evidence(220단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): Stage219(219단계)의 control(대조군)만 살아남았고 hold/re-entry/close-only(보유/재진입/청산만) 변화는 KPI(핵심 성과 지표)를 손상했다는 failure memory(실패 기억)를 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage220_stage219_entry_lifecycle_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage220_stage219_entry_lifecycle_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  best_stage219_row: {best.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `entry_signal_gate_repair_after_lifecycle_axis_failure`
- status(상태): `stage220_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage220(220단계)는 Stage219(219단계) entry/lifecycle repair(진입/생애주기 수리)를 follow-up review(후속 검토)했다. Effect(효과): Stage221(221단계)은 bracket/risk/lifecycle(브래킷/위험/생애주기)을 고정하고 entry signal/gate(진입 신호/게이트)만 수리한다.

## Latest Stage220 Evidence(최신 220단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- best_stage219_row(최선 219단계 행): `{best.get('adapter_id', '')}`
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
        f"""# Stage220 Selection Status(220단계 선택 상태)

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
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage220 Review Index(220단계 검토 색인)

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
        f"\n## {s172.utc_now()} Stage220 lifecycle follow-up review closeout(220단계 생애주기 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): lifecycle axis(생애주기 축)을 failure memory(실패 기억)로 보존하고 Stage221(221단계) entry signal/gate repair(진입 신호/게이트 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    monthly_rows = read_csv(SOURCE_MONTHLY_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    risk_rows = read_csv(SOURCE_RISK_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, monthly_rows, concentration_rows, risk_rows)
    best = best_row(tradeoff_rows)
    attribution_rows = build_attribution_rows(best)
    route_rows = build_route_rows(best)

    s172.write_md(REPORT_PATH, report_md(tradeoff_rows, best))
    s172.write_md(DECISION_PATH, decision_md(best))
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
            "best_stage219_row": best,
            "legacy_34d": LEGACY_34D,
            "stage210_anchor": STAGE210_ANCHOR,
            "stage217_best": STAGE217_BEST,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_ledgers(best)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, best)
    write_next_stage_seed(best)
    update_current_truth(best)
    write_status_files()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "reviewed_closed",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "best_stage219_row": best.get("adapter_id", ""),
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

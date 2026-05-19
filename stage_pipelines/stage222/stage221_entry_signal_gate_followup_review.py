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

STAGE_ID = "222_adapter_research__stage221_entry_signal_gate_followup_review"
RUN_ID = "run222A_stage222_stage221_entry_signal_gate_followup_review_v1"
PACKET_ID = "stage222_stage221_entry_signal_gate_followup_review_v1"
PARENT_RUN_ID = "run221A_stage221_entry_signal_gate_repair_after_lifecycle_axis_failure_v1"
SOURCE_STAGE_ID = "221_adapter_research__entry_signal_gate_repair_after_lifecycle_axis_failure"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE221_EVIDENCE_COMMIT = "49bc0adf2759507805640330c01dfe2dc9870df6"
SOURCE_STAGE221_HASH_RECORD_COMMIT = "68f800fd60278ce951999b59994c951ee4aabaea"
NEXT_STAGE_ID = "223_adapter_research__oos_recovery_after_no_long_block_validation_gain"
NEXT_RUN_ID = "run223A_stage223_oos_recovery_after_no_long_block_validation_gain_v1"
NEXT_PACKET_ID = "stage223_oos_recovery_after_no_long_block_validation_gain_v1"
DECISION = "open_stage223_bounded_oos_recovery_after_no_long_block_validation_gain_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage221_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_oos_recovery_after_no_long_block_validation_gain"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}
STAGE210_ANCHOR = {
    "adapter_id": "s210_ls_r0315",
    "validation_net": 1200.27,
    "validation_mid_pf": 1.695877099,
    "validation_dd": 12.6726,
    "oos_net": 714.86,
}
STAGE219_CONTROL = {
    "adapter_id": "s219_life_control_h3_sd8",
    "validation_net": 952.16,
    "validation_mid_pf": 1.541193855,
    "validation_early_pf": 1.563704148,
    "validation_dd": 12.6953,
    "oos_net": 719.48,
}
STAGE221_NO_LONG_BLOCK = {
    "adapter_id": "s221_gate_no_long_block",
    "validation_net": 1050.87,
    "validation_mid_pf": 1.484282384,
    "validation_early_pf": 1.604593810,
    "validation_dd": 11.6030,
    "oos_net": 626.79,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_SUMMARY_PATH = SOURCE_ROOT / "stage221_summary.json"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage221_quality_matrix.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage221_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage221_concentration_risk_summary.csv"
SOURCE_RISK_PATH = SOURCE_ROOT / "stage221_risk_atr_telemetry.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage221_segment_kpi_summary.csv"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage221_entry_signal_gate_repair_report.md"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage221_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage222_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage222_gate_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage222_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage222_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage222_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage222_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage222/stage221_entry_signal_gate_followup_review.py")
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
        "negative_month_net": round(sum(fnum(row.get("net_profit")) for row in negative), 2),
        "pf_below_34d_count": len(pf_below),
        "net_profit": round(sum(fnum(row.get("net_profit")) for row in rows), 2),
    }


def useful_profile(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    if adapter_id == "s221_gate_no_long_block":
        return "validation_gain_oos_damage_mid_pf_failed(검증 개선, 표본외 손상, 중반 PF 실패)"
    if adapter_id == "s221_gate_short_broad":
        return "early_pf_gain_net_oos_damage(초반 PF 개선, 순손익/표본외 손상)"
    if adapter_id == "s221_gate_control":
        return "oos_preserved_validation_failed(표본외 보존, 검증 실패)"
    if adapter_id == "s221_gate_short_narrow":
        return "damaged_gate_variant(손상된 게이트 변형)"
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
        val_mid_segment = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="validation_is",
            view="actual_routed_total",
            segment_type="chronological_third",
            segment="mid",
        )
        oos_mid_segment = lookup(
            segment_rows,
            adapter_id=adapter_id,
            split="oos",
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
                "profile_label": useful_profile(row),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_net_delta_vs_stage219_control": round(fnum(row.get("validation_net")) - STAGE219_CONTROL["validation_net"], 2),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(fnum(row.get("validation_early_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(fnum(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_late_pf": row.get("validation_late_pf", ""),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_mid_mfe_capture_ratio": val_mid_segment.get("mfe_capture_ratio", ""),
                "validation_pf_below_34d_month_count": val_months["pf_below_34d_count"],
                "validation_negative_month_count": val_months["negative_month_count"],
                "validation_top5_winner_share": val_conc.get("top5_winner_share_of_net", ""),
                "validation_last_quarter_share": val_conc.get("last_quarter_net_share", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_stage219_control": round(fnum(row.get("oos_net")) - STAGE219_CONTROL["oos_net"], 2),
                "oos_net_delta_vs_stage210_anchor": round(fnum(row.get("oos_net")) - STAGE210_ANCHOR["oos_net"], 2),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_mid_mfe_capture_ratio": oos_mid_segment.get("mfe_capture_ratio", ""),
                "oos_pf_below_34d_month_count": oos_months["pf_below_34d_count"],
                "oos_negative_month_count": oos_months["negative_month_count"],
                "oos_negative_months": oos_months["negative_months"],
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "avg_validation_executed_lot": val_risk.get("avg_executed_lot", ""),
                "avg_oos_executed_lot": oos_risk.get("avg_executed_lot", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def clue_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == "s221_gate_no_long_block":
            return row
    return max(rows, key=lambda row: fnum(row.get("validation_net")), default={})


def build_attribution_rows(clue: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "finding": "no_long_block_is_useful_but_not_final(롱 차단 제거는 단서지만 최종 아님)",
            "evidence": (
                "validation_net +98.71 vs Stage219 control(219단계 대조군 대비 검증 순손익 +98.71); "
                "early_pf +0.04089; validation_dd improved by 1.09pp(검증 낙폭 1.09%p 개선)"
            ),
            "damage": "oos_net -92.69 vs Stage219 control(219단계 대조군 대비 표본외 순손익 -92.69); mid_pf still below 34D(중반 PF 34D 미달)",
            "interpretation": "remove_long_block_recovered_validation_supply_but_weakened_oos_balance(롱 차단 제거가 검증 공급은 회복했지만 표본외 균형을 약화)",
            "next_use": "preserve_as_clue_for_oos_mid_recovery_stage(표본외/중반 회복 단계의 단서로 보존)",
        },
        {
            "run_id": RUN_ID,
            "finding": "short_broad_lifts_early_pf_only(숏 확장 차단은 초반 PF만 올림)",
            "evidence": "early_pf 1.873798 above 34D(초반 PF 34D 초과)",
            "damage": "validation_net 686.74 and oos_net 647.38 damaged(검증/표본외 순손익 손상); mid_pf 1.312105 failed(중반 PF 실패)",
            "interpretation": "short_filter_strength_can_help_one_window_but_overfilters_total_curve(숏 필터 강도는 한 구간만 돕고 전체 곡선을 과필터링)",
            "next_use": "do_not_continue_broad_short_gate_axis(넓은 숏 게이트 축은 계속하지 않음)",
        },
        {
            "run_id": RUN_ID,
            "finding": "short_narrow_is_negative_evidence(좁은 숏 차단은 부정 근거)",
            "evidence": "validation_dd 14.5931 above 34D and oos_pf 1.42 below 34D(검증 DD 34D 초과, 표본외 PF 34D 미달)",
            "damage": "validation and oos both degraded(검증과 표본외 모두 저하)",
            "interpretation": "narrow_short_block_added_fragility(좁은 숏 차단이 취약성을 추가)",
            "next_use": "preserve_as_failure_memory(실패 기억으로 보존)",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk_atr_not_the_observed_driver(위험/ATR은 이번 관측 손상의 주원인 아님)",
            "evidence": f"risk_floor_counts val={clue.get('validation_risk_floor_applied_count')} oos={clue.get('oos_risk_floor_applied_count')}; bracket settings held fixed(브래킷 설정 고정)",
            "damage": "remaining weakness is entry-gate distribution and OOS balance(남은 약점은 진입 게이트 분포와 표본외 균형)",
            "interpretation": "keep_risk_atr_constant_before_next_axis_change(다음 축 변경 전 위험/ATR 고정)",
            "next_use": "Stage223 should not become standalone risk campaign(Stage223은 위험 단독 캠페인이 아니어야 함)",
        },
    ]


def build_route_rows(clue: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "open_stage223_oos_mid_recovery(223단계 표본외/중반 회복 개방)",
            "adapter_id": clue.get("adapter_id", ""),
            "action": "test_bounded_oos_recovery_after_no_long_block_validation_gain(no_long_block 검증 개선 뒤 표본외 회복을 좁게 시험)",
            "effect": "targets_the_actual_remaining_gap_without_restarting_broad_gate_search(넓은 게이트 탐색을 재시작하지 않고 남은 간극만 겨냥)",
            "risk": "may_fail_if_validation_gain_is_intrinsically_oos_fragile(검증 개선 자체가 표본외 취약이면 실패 가능)",
        },
        {
            "run_id": RUN_ID,
            "route": "preserve_no_long_block_as_clue_not_anchor(no_long_block을 기준선이 아닌 단서로 보존)",
            "adapter_id": "s221_gate_no_long_block",
            "action": "carry_validation_gain_pattern_forward_but_do_not_mark_candidate_final(검증 개선 패턴은 넘기되 최종 후보로 표시하지 않음)",
            "effect": "keeps_useful_signal_without_hiding_oos_damage(쓸모 있는 신호를 보존하면서 표본외 손상을 숨기지 않음)",
            "risk": "next_stage_must_protect_oos_net_and_mid_pf(다음 단계가 표본외 순손익과 중반 PF를 보호해야 함)",
        },
        {
            "run_id": RUN_ID,
            "route": "stop_short_broad_and_short_narrow_axes(숏 확장/축소 차단 중단)",
            "adapter_id": "s221_gate_short_broad;s221_gate_short_narrow",
            "action": "record_as_failure_memory_and_do_not_expand_inside_stage222(실패 기억으로 기록하고 Stage222 안에서 확장하지 않음)",
            "effect": "prevents_stage222_bloat(222단계 비대화 방지)",
            "risk": "one_untried_short_gate_combo_may_be_missed(미시도 숏 게이트 조합 하나를 놓칠 수 있음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], clue: Mapping[str, Any]) -> str:
    lines = [
        "# Stage222 Follow-up Review(222단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- decision(판정): `{DECISION}`",
        f"- clue_row(단서 행): `{clue.get('adapter_id', '')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "- Stage221(221단계)는 34D(34D 기준)에 가까워진 부분이 있다.",
        "- `s221_gate_no_long_block`은 validation net(검증 순손익)과 early PF(초반 수익요인), drawdown(낙폭)을 개선했다.",
        "- 그러나 OOS net(표본외 순손익)이 크게 낮아졌고 mid PF(중반 수익요인)가 34D(34D 기준)에 못 미친다.",
        "- 그래서 이것은 final(최종)이 아니라 Stage223(223단계)로 넘길 clue(단서)다.",
        "",
        "## KPI Tradeoff(KPI 상충)",
        "",
        "| adapter(어댑터) | profile(유형) | val net gap(검증 순손익 차이) | early PF gap(초반 PF 차이) | mid PF gap(중반 PF 차이) | OOS vs control(표본외 대조군 대비) | OOS vs 210(표본외 210 대비) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('profile_label', '')} | "
            f"{row.get('validation_net_gap_vs_34d', '')} | {row.get('validation_early_pf_gap_vs_34d', '')} | "
            f"{row.get('validation_mid_pf_gap_vs_34d', '')} | {row.get('oos_net_delta_vs_stage219_control', '')} | "
            f"{row.get('oos_net_delta_vs_stage210_anchor', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage221 entry signal/gate repair(221단계 진입 신호/게이트 수리).",
            "- evidence_available(사용 근거): Stage221 MT5 Strategy Tester(MetaTrader 5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).",
            "- evidence_missing(부족 근거): OOS net(표본외 순손익) 회복, mid PF(중반 수익요인) 회복, 더 매끄러운 equity/balance curve(자본/잔고 곡선) 확인.",
            "- judgment_label(판정 라벨): exploratory_positive_clue_not_final(탐색상 긍정 단서, 최종 아님).",
            "- claim_boundary(주장 경계): research/development only(연구개발 전용).",
            "- next_condition(다음 조건): Stage223(223단계)에서 OOS net(표본외 순손익)과 mid PF(중반 수익요인)를 회복하면서 no_long_block(롱 차단 제거)의 검증 개선을 보존해야 한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(clue: Mapping[str, Any]) -> str:
    return f"""# Stage222 Decision(222단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage221_evidence_commit(원천 221단계 근거 커밋): `{SOURCE_STAGE221_EVIDENCE_COMMIT}`
- source_stage221_hash_record_commit(원천 221단계 해시 기록 커밋): `{SOURCE_STAGE221_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- clue_row(단서 행): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage222(222단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage223(223단계)는 `s221_gate_no_long_block`의 validation gain(검증 개선)을 보존하면서 OOS net(표본외 순손익)과 mid PF(중반 수익요인) 회복만 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        TRADEOFF_MATRIX_PATH,
        ATTRIBUTION_PATH,
        ROUTE_MATRIX_PATH,
        SUMMARY_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
    ]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage222_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage222 Stage221 entry signal/gate follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(clue: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("clue_row", clue.get("adapter_id", "")),
            ("validation_net", clue.get("validation_net", "")),
            ("validation_mid_pf", clue.get("validation_mid_pf", "")),
            ("oos_net", clue.get("oos_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage222_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage222_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage222_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage221_entry_signal_gate_followup_review(221단계 진입 신호/게이트 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage222 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; clue_row={clue.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    clue: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "clue_row": clue.get("adapter_id", ""),
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
        f"""# Stage222 Closeout Packet(222단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- clue_row(단서 행): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(clue: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage223(223단계)는 Stage222(222단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can OOS net(표본외 순손익) and validation mid PF(검증 중반 수익요인) be recovered after the `s221_gate_no_long_block` validation gain(검증 개선), while preserving validation net(검증 순손익), early PF(초반 수익요인), drawdown(낙폭), model-controlled risk%(모델 제어 위험 비율), and ATR/bracket behavior(ATR/브래킷 동작)?

Effect(효과): Stage221(221단계)의 유용한 validation gain(검증 개선)을 버리지 않되, 34D(34D 기준)에 못 미친 OOS(표본외)와 mid PF(중반 수익요인)만 좁게 겨냥한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage223 Input References(223단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- clue_row(단서 행): `{clue.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage221_quality_matrix(원천 221단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage221_risk_atr_telemetry(원천 221단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage223 Review Index(223단계 검토 색인)

- status(상태): `open_planned_from_stage222`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage223 Selection Status(223단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage222`
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
  Stage222(222단계) closed(종료) as `{DECISION}` and Stage223(223단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage221(221단계)의 no_long_block(롱 차단 제거) validation gain(검증 개선)을 단서로 보존하면서 OOS net(표본외 순손익)과 mid PF(중반 수익요인) 회복만 좁게 시험한다.
- >-
  Stage222 evidence(222단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): `s221_gate_no_long_block`은 final(최종)이 아니라 validation_gain_oos_damage_mid_pf_failed(검증 개선, 표본외 손상, 중반 PF 실패) 단서로 기록된다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage222_stage221_entry_signal_gate_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage222_stage221_entry_signal_gate_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  clue_row: {clue.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `s221_gate_no_long_block_as_clue_not_final`
- status(상태): `stage222_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage222(222단계)는 Stage221(221단계) entry signal/gate repair(진입 신호/게이트 수리)를 review-only(검토 전용)로 판정했다. Effect(효과): Stage223(223단계)는 no_long_block(롱 차단 제거)의 validation gain(검증 개선)을 보존하면서 OOS net(표본외 순손익)과 mid PF(중반 수익요인) 회복을 좁게 시험한다.

## Latest Stage222 Evidence(최신 222단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- clue_row(단서 행): `{clue.get('adapter_id', '')}`
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
        f"""# Stage222 Selection Status(222단계 선택 상태)

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
        f"""# Stage222 Review Index(222단계 검토 색인)

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
        f"\n## {utc_now()} Stage222 entry signal/gate follow-up review closeout(222단계 진입 신호/게이트 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): no_long_block(롱 차단 제거)을 validation gain clue(검증 개선 단서)로 보존하고, OOS net(표본외 순손익)과 mid PF(중반 수익요인) 회복을 Stage223(223단계)로 넘겼다.\n"
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
    clue = clue_row(tradeoff_rows)
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
            "clue_row": clue,
            "legacy_34d": LEGACY_34D,
            "stage210_anchor": STAGE210_ANCHOR,
            "stage219_control": STAGE219_CONTROL,
            "stage221_no_long_block": STAGE221_NO_LONG_BLOCK,
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
                    "clue_row": clue.get("adapter_id", ""),
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

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

STAGE_ID = "226_adapter_research__stage225_validation_recovery_followup_review"
RUN_ID = "run226A_stage226_stage225_validation_recovery_followup_review_v1"
PACKET_ID = "stage226_stage225_validation_recovery_followup_review_v1"
PARENT_RUN_ID = "run225A_stage225_validation_recovery_after_lowedge_oos_gain_v1"
SOURCE_STAGE_ID = "225_adapter_research__validation_recovery_after_lowedge_oos_gain"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE225_EVIDENCE_COMMIT = "21f86245b96f10ee1dc1569a6f92933b2635dbf8"
SOURCE_STAGE225_HASH_RECORD_COMMIT = "ce57329b361d13073f330f993e54595b5f655ba2"
NEXT_STAGE_ID = "227_adapter_research__selection_structure_repair_after_threshold_axis_no_effect"
NEXT_RUN_ID = "run227A_stage227_selection_structure_repair_after_threshold_axis_no_effect_v1"
NEXT_PACKET_ID = "stage227_selection_structure_repair_after_threshold_axis_no_effect_v1"
DECISION = "open_stage227_bounded_selection_structure_repair_after_threshold_axis_no_effect_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage225_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_selection_structure_repair_after_threshold_axis_no_effect"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}
STAGE224_OOS_GAIN_CLUE = {
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
SOURCE_SUMMARY_PATH = SOURCE_ROOT / "stage225_summary.json"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage225_quality_matrix.csv"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage225_validation_recovery_kpi_summary.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage225_segment_kpi_summary.csv"
SOURCE_BALANCE_PATH = SOURCE_ROOT / "stage225_balance_curve_audit.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage225_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage225_concentration_risk_summary.csv"
SOURCE_RISK_PATH = SOURCE_ROOT / "stage225_risk_atr_telemetry.csv"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage225_validation_recovery_report.md"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage225_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage226_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage226_threshold_axis_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage226_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage226_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage226_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage226_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage226/stage225_validation_recovery_followup_review.py")
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


def metric_signature(row: Mapping[str, Any]) -> tuple[float, ...]:
    return (
        round(fnum(row.get("validation_net")), 2),
        round(fnum(row.get("validation_early_pf")), 9),
        round(fnum(row.get("validation_mid_pf")), 9),
        round(fnum(row.get("validation_balance_dd_percent")), 4),
        round(fnum(row.get("oos_net")), 2),
        round(fnum(row.get("oos_pf")), 6),
        round(fnum(row.get("oos_balance_dd_percent")), 4),
    )


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


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    concentration_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    signatures = {metric_signature(row) for row in quality_rows}
    first_signature = metric_signature(quality_rows[0]) if quality_rows else ()
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
        validation_recovered = (
            fnum(row.get("validation_net")) >= LEGACY_34D["net_profit"]
            and fnum(row.get("validation_early_pf")) >= LEGACY_34D["profit_factor"]
            and fnum(row.get("validation_mid_pf")) >= LEGACY_34D["profit_factor"]
            and fnum(row.get("validation_balance_dd_percent")) <= LEGACY_34D["max_drawdown_percent"]
        )
        oos_preserved = (
            fnum(row.get("oos_net")) >= STAGE224_OOS_GAIN_CLUE["oos_net"]
            and fnum(row.get("oos_pf")) >= STAGE224_OOS_GAIN_CLUE["oos_pf"]
            and fnum(row.get("oos_balance_dd_percent")) <= STAGE224_OOS_GAIN_CLUE["oos_dd"]
        )
        axis_effect = "no_measurable_change" if len(signatures) == 1 and metric_signature(row) == first_signature else "changed"
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "axis_effect": axis_effect,
                "distinct_metric_signature_count": len(signatures),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_recovered": validation_recovered,
                "oos_preserved": oos_preserved,
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(
                    fnum(row.get("validation_early_pf")) - LEGACY_34D["profit_factor"], 6
                ),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d": round(
                    fnum(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 6
                ),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_late_share": row.get("validation_late_net_share", ""),
                "validation_mid_mfe_capture_ratio": val_mid.get("mfe_capture_ratio", ""),
                "validation_pf_below_34d_month_count": val_months["pf_below_34d_count"],
                "validation_negative_month_count": val_months["negative_month_count"],
                "validation_top5_winner_share": val_conc.get("top5_winner_share_of_net", ""),
                "validation_last_quarter_share": val_conc.get("last_quarter_net_share", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_pf_below_34d_month_count": oos_months["pf_below_34d_count"],
                "oos_negative_month_count": oos_months["negative_month_count"],
                "oos_negative_months": oos_months["negative_months"],
                "oos_top5_winner_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "validation_risk_floor_applied_count": val_risk.get("risk_floor_applied_count", ""),
                "oos_risk_floor_applied_count": oos_risk.get("risk_floor_applied_count", ""),
                "validation_model_risk_max_pct": row.get("model_risk_max_pct", ""),
                "validation_atr_stop_multiplier": row.get("atr_stop_multiplier", ""),
                "validation_atr_take_profit_multiplier": row.get("atr_take_profit_multiplier", ""),
                "quality_flags": row.get("quality_flags", ""),
            }
        )
    return rows


def representative_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == "s225_val_lowedge_lng520":
            return row
    return rows[0] if rows else {}


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    clue = representative_row(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "finding": "long_threshold_axis_no_effect(롱 임계값 축 효과 없음)",
            "evidence": "0.520, 0.515, 0.510, 0.505 variants produced one identical KPI signature(네 변형 모두 동일한 KPI 서명).",
            "damage": "validation net 833.22, early PF 1.446826, mid PF 1.498516, DD 13.0158 stayed failed(검증 순손익/초반/중반/낙폭 실패 유지).",
            "interpretation": "validation damage is not caused by simple long-threshold supply shortage(단순 롱 임계값 공급 부족이 주원인 아님).",
            "next_use": "move to selection-structure repair instead of more threshold tuning(임계값 조정 반복 대신 선택 구조 수리로 이동).",
        },
        {
            "run_id": RUN_ID,
            "finding": "oos_gain_preserved_but_not_sufficient(표본외 개선 보존, 충분조건 아님)",
            "evidence": "OOS net 765.40, OOS PF 1.93, OOS DD 7.7935 stayed intact(표본외 순손익/수익요인/낙폭 유지).",
            "damage": "validation remained below 34D and late concentration stayed 0.5301(검증은 34D 미달, 후반 집중 53.01%).",
            "interpretation": "OOS preservation alone cannot mark the adapter final(표본외 보존만으로 최종 어댑터가 될 수 없음).",
            "next_use": "preserve lowedge OOS gain as a bound while repairing validation(저엣지 표본외 개선을 경계로 보존하며 검증 수리).",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk_atr_capability_present_not_driver(위험/ATR 기능은 존재하지만 주원인 아님)",
            "evidence": f"model_risk_max_pct={clue.get('validation_model_risk_max_pct')}, ATR SL/TP multipliers {clue.get('validation_atr_stop_multiplier')}/{clue.get('validation_atr_take_profit_multiplier')}.",
            "damage": "mandatory risk/ATR presence did not repair segment KPI(필수 위험/ATR 존재만으로 구간 KPI 수리 안 됨).",
            "interpretation": "next stage remains adapter repair, not standalone risk campaign(다음 단계는 위험 단독 캠페인이 아니라 어댑터 수리).",
            "next_use": "keep risk/ATR telemetry mandatory in Stage227(227단계에서도 위험/ATR 기록 필수 유지).",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "open_stage227_selection_structure_repair(227단계 선택 구조 수리 개방)",
            "action": "test bounded structure changes around lowedge guard versus no-long bounds(저엣지 보호와 롱 차단 없음 경계 사이의 구조 변화를 좁게 시험)",
            "effect": "targets the actual observed failure after threshold axis produced no change(임계값 축 무효 뒤 실제 실패 원인을 직접 겨냥)",
            "risk": "validation may improve while OOS gain disappears(검증이 좋아져도 표본외 개선이 사라질 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "stop_more_long_threshold_tuning(추가 롱 임계값 조정 중단)",
            "action": "record 0.520 to 0.505 as exhausted for this guard shape(0.520부터 0.505까지 이 보호 구조에서는 소진으로 기록)",
            "effect": "prevents Stage227 from repeating Stage225(227단계가 225단계를 반복하지 않게 함)",
            "risk": "a different model source could still respond to threshold changes(다른 모델 원천은 임계값에 반응할 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "no_final_claim_no_onnx_hardening(최종 주장 없음, ONNX 경화 없음)",
            "action": "keep adapter in research repair path(어댑터를 연구 수리 경로에 둠)",
            "effect": "avoids treating OOS reproduction or ATR/risk presence as completion(표본외 재현이나 ATR/위험 존재를 완료로 오해하지 않게 함)",
            "risk": "more bounded stages are required(추가 경계 단계가 필요함)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage226 Follow-up Review(226단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "- Stage225(225단계)는 long threshold(롱 임계값)을 0.520에서 0.505까지 낮췄다.",
        "- 결과는 네 변형이 모두 완전히 같았다.",
        "- OOS(표본외)는 유지됐지만 validation(검증)은 34D(34D 기준)보다 약했다.",
        "- 그래서 다음은 threshold tuning(임계값 조정)이 아니라 selection structure repair(선택 구조 수리)다.",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | axis(축) | effect(효과) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | flags(표식) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('axis', '')} | {row.get('axis_effect', '')} | "
            f"{row.get('validation_net', '')} | {row.get('validation_early_pf', '')} | "
            f"{row.get('validation_mid_pf', '')} | {row.get('validation_dd_percent', '')} | "
            f"{row.get('oos_net', '')} | {row.get('oos_pf', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage225 validation recovery after lowedge OOS gain(225단계 저엣지 표본외 개선 후 검증 회복).",
            "- evidence_available(사용 근거): MT5 Strategy Tester(메타트레이더5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).",
            "- judgment_label(판정 라벨): threshold_axis_no_effect_validation_failed_not_final(임계값 축 효과 없음, 검증 실패, 최종 아님).",
            "- next_condition(다음 조건): Stage227(227단계)는 lowedge guard(저엣지 보호) 구조 자체를 좁게 바꿔 검증을 회복하되 OOS(표본외), risk(위험), ATR/bracket(ATR/브래킷)을 보존해야 한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(clue: Mapping[str, Any]) -> str:
    return f"""# Stage226 Decision(226단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage225_evidence_commit(원천 225단계 근거 커밋): `{SOURCE_STAGE225_EVIDENCE_COMMIT}`
- source_stage225_hash_record_commit(원천 225단계 해시 기록 커밋): `{SOURCE_STAGE225_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- representative_adapter(대표 어댑터): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage226(226단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage227(227단계)은 더 낮은 long threshold(롱 임계값)를 반복하지 않고, lowedge guard(저엣지 보호) 선택 구조 자체를 bounded repair(경계 수리)로 시험한다.
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
            "artifact_type": "stage226_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage226 Stage225 validation recovery follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(clue: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("representative_adapter", clue.get("adapter_id", "")),
            ("axis_effect", clue.get("axis_effect", "")),
            ("validation_net", clue.get("validation_net", "")),
            ("validation_mid_pf", clue.get("validation_mid_pf", "")),
            ("oos_net", clue.get("oos_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage226_role", "review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage226_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage226_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage225_validation_recovery_followup_review(225단계 검증 회복 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage226 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; representative_adapter={clue.get('adapter_id', '')}; boundary={BOUNDARY}",
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
        "representative_adapter": clue.get("adapter_id", ""),
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
        f"""# Stage226 Closeout Packet(226단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- representative_adapter(대표 어댑터): `{clue.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage227(227단계)은 Stage226(226단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can the adapter recover validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), drawdown(낙폭), and late concentration(후반 집중) after Stage225(225단계) proved the long-threshold axis(롱 임계값 축) had no measurable effect, while preserving OOS net(표본외 순손익), OOS PF(표본외 수익요인), model-controlled risk%(모델 제어 위험 비율), and ATR/bracket behavior(ATR/브래킷 동작)?

Effect(효과): 더 낮은 threshold(임계값)를 반복하지 않고, selection structure(선택 구조)를 좁게 바꿔 34D(34D 기준) 이상 KPI(핵심 성과 지표)에 가까워지는지 확인한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage227 Input References(227단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage225_quality_matrix(원천 225단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage225_risk_atr_telemetry(원천 225단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage227 Review Index(227단계 검토 색인)

- status(상태): `open_planned_from_stage226`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage227 Selection Status(227단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage226`
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
  Stage226(226단계) closed(종료) as `{DECISION}` and Stage227(227단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage225(225단계)의 long-threshold axis(롱 임계값 축)이 no measurable change(측정 가능한 변화 없음)였으므로, 다음은 selection structure repair(선택 구조 수리)로 좁힌다.
- >-
  Stage226 evidence(226단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): OOS gain(표본외 개선)은 보존됐지만 validation(검증)은 34D(34D 기준) 미달이라는 판단을 분리 기록한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage226_stage225_validation_recovery_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage226_stage225_validation_recovery_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  representative_adapter: {clue.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `lowedge_guard_selection_structure_repair_candidate_not_final`
- status(상태): `stage226_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage226(226단계)는 Stage225(225단계) validation recovery(검증 회복)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage227(227단계)는 long threshold(롱 임계값) 반복이 아니라 selection structure(선택 구조) 수리를 시험한다.

## Latest Stage226 Evidence(최신 226단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- representative_adapter(대표 어댑터): `{clue.get('adapter_id', '')}`
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
        f"""# Stage226 Selection Status(226단계 선택 상태)

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
        f"""# Stage226 Review Index(226단계 검토 색인)

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
        f"\n## {utc_now()} Stage226 validation recovery follow-up review closeout(226단계 검증 회복 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage225(225단계)의 long threshold(롱 임계값) 조정 축이 KPI(핵심 성과 지표)를 바꾸지 못했으므로 Stage227(227단계) 선택 구조 수리로 넘겼다.\n"
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
    clue = representative_row(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows()

    write_md(REPORT_PATH, report_md(tradeoff_rows))
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
            "source_quality": rel(SOURCE_QUALITY_PATH),
            "source_kpi": rel(SOURCE_KPI_PATH),
            "source_balance_curve_audit": rel(SOURCE_BALANCE_PATH),
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "representative_adapter": clue,
            "legacy_34d": LEGACY_34D,
            "stage224_oos_gain_clue": STAGE224_OOS_GAIN_CLUE,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_ledgers(clue)
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, clue)
    write_next_stage_seed()
    update_current_truth(clue)
    write_status_files()
    append_changelog()
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    print(
        json.dumps(
            json_ready(
                {
                    "status": "reviewed_closed",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "representative_adapter": clue.get("adapter_id", ""),
                    "axis_effect": clue.get("axis_effect", ""),
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

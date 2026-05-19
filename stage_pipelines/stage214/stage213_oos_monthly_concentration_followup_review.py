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

STAGE_ID = "214_adapter_research__stage213_oos_monthly_concentration_followup_review"
RUN_ID = "run214A_stage214_stage213_oos_monthly_concentration_followup_review_v1"
PACKET_ID = "stage214_stage213_oos_monthly_concentration_followup_review_v1"
PARENT_RUN_ID = "run213A_stage213_s210_r0315_oos_monthly_concentration_repair_v1"
SOURCE_STAGE_ID = "213_adapter_research__s210_r0315_oos_monthly_concentration_repair"
SOURCE_RUN_ID = "run213A_stage213_s210_r0315_oos_monthly_concentration_repair_v1"
SOURCE_STAGE213_EVIDENCE_COMMIT = "3937f368904f0871f0d78be46daee32b72a956c8"
SOURCE_STAGE213_HASH_RECORD_COMMIT = "1f5de86d429b2361a121fd195ad669075ba2c8a5"
NEXT_STAGE_ID = "215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain"
NEXT_RUN_ID = "run215A_stage215_validation_mid_pf_recovery_preserve_oos_gain_v1"
NEXT_PACKET_ID = "stage215_validation_mid_pf_recovery_preserve_oos_gain_v1"
DECISION = "open_stage215_bounded_validation_mid_pf_recovery_preserve_oos_gain_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage213_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_validation_mid_pf_recovery"
BOUNDARY = s213.BOUNDARY
LEGACY_34D = s213.LEGACY_34D
SOURCE_ANCHOR_ID = "s210_ls_r0315"
REPAIR_PROBE_ID = "s213_r03125_s200_t455"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE212_SUMMARY_PATH = Path("stages/212_adapter_research__stage210_candidate_segment_equity_audit/03_reviews/stage212_summary.json")
SOURCE_QUALITY_PATH = Path("stages/213_adapter_research__s210_r0315_oos_monthly_concentration_repair/03_reviews/stage213_quality_matrix.csv")
SOURCE_MONTHLY_PATH = Path("stages/213_adapter_research__s210_r0315_oos_monthly_concentration_repair/03_reviews/stage213_monthly_kpi_summary.csv")
SOURCE_CONCENTRATION_PATH = Path("stages/213_adapter_research__s210_r0315_oos_monthly_concentration_repair/03_reviews/stage213_concentration_risk_summary.csv")
SOURCE_RISK_PATH = Path("stages/213_adapter_research__s210_r0315_oos_monthly_concentration_repair/03_reviews/stage213_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/213_adapter_research__s210_r0315_oos_monthly_concentration_repair/03_reviews/stage213_oos_monthly_concentration_repair_report.md")
SOURCE_DECISION_PATH = Path("stages/213_adapter_research__s210_r0315_oos_monthly_concentration_repair/03_reviews/stage213_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage214_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage214_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage214_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage214_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage214_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage214_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage214/stage213_oos_monthly_concentration_followup_review.py")
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


def concentration_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def risk_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def stage214_read(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    flags = str(row.get("quality_flags", ""))
    if adapter_id == REPAIR_PROBE_ID:
        return "oos_gain_but_validation_mid_pf_failed(표본외 이득은 있으나 검증 중반 수익요인 실패)"
    if "validation_balance_dd_above_34d" in flags:
        return "repair_damaged_validation_dd(수리가 검증 낙폭을 손상)"
    if "validation_net_below_34d" in flags:
        return "repair_lost_validation_net(수리가 검증 순손익을 잃음)"
    if "validation_mid_pf_below_34d" in flags:
        return "repair_mid_pf_tradeoff(수리 중반 수익요인 상충)"
    return "measurement_only_candidate_not_final(측정 전용 후보, 최종 아님)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    monthly_rows: Sequence[Mapping[str, Any]],
    concentration_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    baseline: Mapping[str, Any],
) -> list[dict[str, Any]]:
    baseline_oos = fnum(baseline.get("oos_net"))
    baseline_val_net = fnum(baseline.get("validation_net"))
    baseline_mid_pf = fnum(baseline.get("validation_mid_pf"))
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        oos_months = monthly_stats(monthly_rows, adapter_id, "oos")
        val_months = monthly_stats(monthly_rows, adapter_id, "validation_is")
        oos_conc = concentration_lookup(concentration_rows, adapter_id, "oos")
        val_risk = risk_lookup(risk_rows, adapter_id, "validation_is")
        oos_risk = risk_lookup(risk_rows, adapter_id, "oos")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_delta_vs_s210": round(fnum(row.get("validation_net")) - baseline_val_net, 2),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_delta_vs_s210": round(fnum(row.get("validation_mid_pf")) - baseline_mid_pf, 6),
                "validation_negative_month_count": val_months["negative_month_count"],
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_s210": round(fnum(row.get("oos_net")) - baseline_oos, 2),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_negative_month_count": oos_months["negative_month_count"],
                "oos_negative_months": oos_months["negative_months"],
                "oos_negative_month_net": oos_months["negative_month_net"],
                "oos_top5_share": oos_conc.get("top5_winner_share_of_net", ""),
                "oos_last_quarter_share": oos_conc.get("last_quarter_net_share", ""),
                "risk_floor_applied_validation": val_risk.get("risk_floor_applied_count", ""),
                "risk_floor_applied_oos": oos_risk.get("risk_floor_applied_count", ""),
                "quality_flags": row.get("quality_flags", ""),
                "stage214_read": stage214_read(row),
            }
        )
    return rows


def selected_probe(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == REPAIR_PROBE_ID:
            return row
    return max(rows, key=lambda row: fnum(row.get("oos_net")), default={})


def build_attribution_rows(probe: Mapping[str, Any], baseline: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "oos_net_improved_but_validation_mid_pf_failed(표본외 순손익은 개선됐으나 검증 중반 수익요인 실패)",
            "comparison_baseline": SOURCE_ANCHOR_ID,
            "likely_drivers": "tighter_bracket_reduced_loss_windows_but_cut_mid_segment_payoff(타이트한 브래킷이 손실 창을 줄였지만 중반 구간 보상을 깎음)",
            "segment_checks": f"validation_mid_pf={probe.get('validation_mid_pf')};baseline_mid_pf={baseline.get('validation_mid_pf')}",
            "trade_shape": f"oos_net_delta={probe.get('oos_net_delta_vs_s210')};validation_net_delta={probe.get('validation_net_delta_vs_s210')}",
            "alternative_explanations": "oos_gain_may_be_risk_shape_not_signal_quality(표본외 이득은 신호 품질이 아니라 위험 형태일 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "recover_validation_mid_pf_without_losing_oos_gain(표본외 이득을 잃지 않고 검증 중반 수익요인 회복)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "monthly_negative_loss_size_improved_but_count_remained(월별 음수 손실 크기는 줄었지만 개수는 유지)",
            "comparison_baseline": "Stage212 audit baseline(212단계 감사 기준)",
            "likely_drivers": "bracket_tightening(브래킷 축소)",
            "segment_checks": f"oos_negative_months={probe.get('oos_negative_months')};negative_net={probe.get('oos_negative_month_net')}",
            "trade_shape": f"oos_top5={probe.get('oos_top5_share')};oos_last_quarter={probe.get('oos_last_quarter_share')}",
            "alternative_explanations": "late_profit_cluster_remains(후반 수익 군집은 남아 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "mid_pf_recovery_plus_late_concentration_review(중반 수익요인 회복과 후반 집중 검토)",
        },
    ]


def build_route_rows(probe: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "preserve_incumbent_candidate(기존 후보 보존)",
            "adapter_id": SOURCE_ANCHOR_ID,
            "action": "keep_as_active_reference_not_final(활성 참조 후보로 보존, 최종 아님)",
            "effect": "prevents_oos_gain_from_replacing_validation_stability(표본외 이득이 검증 안정성을 대체하지 못하게 함)",
            "risk": "oos_weakness_remains(표본외 약점은 남음)",
        },
        {
            "run_id": RUN_ID,
            "route": "stage215_repair_probe(215단계 수리 탐침)",
            "adapter_id": probe.get("adapter_id", ""),
            "action": "repair_validation_mid_pf_preserve_oos_gain(검증 중반 수익요인 회복과 표본외 이득 보존)",
            "effect": "turns_stage213_tradeoff_into_bounded_next_question(213단계 상충을 다음 경계 질문으로 전환)",
            "risk": "validation_net_margin_thin_and_mid_pf_failed(검증 순손익 여유가 얇고 중반 수익요인 실패)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], probe: Mapping[str, Any]) -> str:
    lines = [
        "# Stage214 Follow-up Review(214단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage213_evidence_commit(원천 213단계 근거 커밋): `{SOURCE_STAGE213_EVIDENCE_COMMIT}`",
        f"- source_stage213_hash_record_commit(원천 213단계 해시 기록 커밋): `{SOURCE_STAGE213_HASH_RECORD_COMMIT}`",
        f"- decision(판정): `{DECISION}`",
        f"- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | hard pass(엄격 통과) | val net delta(검증 순손익 차이) | mid PF delta(중반 수익요인 차이) | OOS net delta(표본외 순손익 차이) | OOS neg months(표본외 음수 월) | OOS top5(표본외 상위5) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('hard_quality_pass', '')} | {row.get('validation_net_delta_vs_s210', '')} | {row.get('validation_mid_pf_delta_vs_s210', '')} | {row.get('oos_net_delta_vs_s210', '')} | {row.get('oos_negative_month_count', '')} | {row.get('oos_top5_share', '')} | {row.get('stage214_read', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- `{probe.get('adapter_id', '')}`는 OOS net(표본외 순손익)을 개선했지만 validation mid PF(검증 중반 수익요인)를 34D(34D) 아래로 떨어뜨렸다.",
            "- Stage214(214단계)는 final(최종), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.",
            "- Effect(효과): Stage215(215단계)는 validation mid PF(검증 중반 수익요인)를 회복하면서 OOS gain(표본외 이득)을 보존하는지 좁게 시험한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(probe: Mapping[str, Any]) -> str:
    return f"""# Stage214 Decision(214단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage213_evidence_commit(원천 213단계 근거 커밋): `{SOURCE_STAGE213_EVIDENCE_COMMIT}`
- source_stage213_hash_record_commit(원천 213단계 해시 기록 커밋): `{SOURCE_STAGE213_HASH_RECORD_COMMIT}`
- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage214(214단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage215(215단계)에서 validation mid PF recovery(검증 중반 수익요인 회복)와 OOS gain preservation(표본외 이득 보존)을 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage214_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage214 Stage213 OOS monthly concentration follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(probe: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("repair_probe", probe.get("adapter_id", "")),
            ("oos_net_delta_vs_s210", probe.get("oos_net_delta_vs_s210", "")),
            ("validation_mid_pf", probe.get("validation_mid_pf", "")),
            ("validation_net_delta_vs_s210", probe.get("validation_net_delta_vs_s210", "")),
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
            "ledger_row_id": f"{RUN_ID}__stage214_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage214_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage213_oos_monthly_concentration_followup_review(213단계 표본외 월별/집중 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage214 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; repair_probe={probe.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], probe: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "repair_probe": probe.get("adapter_id", ""),
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
        f"""# Stage214 Closeout Packet(214단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(probe: Mapping[str, Any]) -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage215(215단계)은 Stage214(214단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can `{probe.get('adapter_id', REPAIR_PROBE_ID)}` recover validation mid PF(검증 중반 수익요인) to 34D(34D) level while preserving OOS net gain(표본외 순손익 이득), validation net/DD(검증 순손익/낙폭), monthly loss reduction(월별 손실 축소), and risk/ATR telemetry(위험/ATR 기록)?

Effect(효과): Stage213(213단계)의 OOS gain(표본외 이득)을 바로 채택하지 않고, 깨진 validation mid PF(검증 중반 수익요인)를 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage215 Input References(215단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage213_quality_matrix(원천 213단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage213_monthly_kpi(원천 213단계 월별 KPI 핵심 성과 지표): `{rel(SOURCE_MONTHLY_PATH)}`
- source_stage213_concentration(원천 213단계 집중): `{rel(SOURCE_CONCENTRATION_PATH)}`
""",
    )
    s172.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"# Stage215 Review Index(215단계 검토 색인)\n\n- status(상태): `open_planned_from_stage214`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n")
    s172.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"# Stage215 Selection Status(215단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage214`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def update_current_truth(probe: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage214(214단계) closed(종료) as `{DECISION}` and Stage215(215단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): `{probe.get('adapter_id', '')}`의 validation mid PF(검증 중반 수익요인)를 회복하면서 OOS gain(표본외 이득)을 보존하는지 좁게 시험한다.
- >-
  Stage214 evidence(214단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): OOS improvement(표본외 개선)와 validation damage(검증 손상)를 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage214_stage213_oos_monthly_concentration_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage214_stage213_oos_monthly_concentration_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  repair_probe: {probe.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `{probe.get('adapter_id', '')}`
- status(상태): `stage214_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage214(214단계)는 Stage213(213단계) OOS monthly/concentration repair(표본외 월별/집중 수리)를 follow-up review(후속 검토)했다. Effect(효과): Stage215(215단계)는 validation mid PF(검증 중반 수익요인) 회복만 좁게 진행한다.

## Latest Stage214 Evidence(최신 214단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(probe: Mapping[str, Any]) -> None:
    s172.write_md(SELECTED_ROOT / "selection_status.md", f"# Stage214 Selection Status(214단계 선택 상태)\n\n- stage_status(단계 상태): `closed_{DECISION}`\n- current_packet(현재 작업 묶음): `{PACKET_ID}`\n- current_run(현재 실행): `{RUN_ID}`\n- source_stage(원천 단계): `{SOURCE_STAGE_ID}`\n- source_run(원천 실행): `{SOURCE_RUN_ID}`\n- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`\n- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`\n- decision(판정): `{DECISION}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")
    s172.write_md(REVIEWS_ROOT / "review_index.md", f"# Stage214 Review Index(214단계 검토 색인)\n\n- status(상태): `closed_{DECISION}`\n- packet(작업 묶음): `{PACKET_ID}`\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- repair_probe(수리 탐침): `{probe.get('adapter_id', '')}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`\n- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`\n- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n")


def append_changelog(probe: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage214 Stage213 OOS monthly concentration follow-up review closeout(214단계 213단계 표본외 월별/집중 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): selected(선택) `{probe.get('adapter_id', '')}` as Stage215(215단계) repair probe(수리 탐침), not replacement(교체 아님).\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    baseline = json.loads(io_path(SOURCE_STAGE212_SUMMARY_PATH).read_text(encoding="utf-8-sig"))
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    monthly_rows = read_csv(SOURCE_MONTHLY_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    risk_rows = read_csv(SOURCE_RISK_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, monthly_rows, concentration_rows, risk_rows, baseline)
    probe = selected_probe(tradeoff_rows)
    attribution_rows = build_attribution_rows(probe, baseline)
    route_rows = build_route_rows(probe)
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows, probe))
    s172.write_md(DECISION_PATH, decision_md(probe))
    write_ledgers(probe)
    payload = {
        "run_id": RUN_ID,
        "decision": DECISION,
        "repair_probe": probe.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "route_rows": route_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(SUMMARY_JSON_PATH, payload)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, probe)
    write_next_stage_seed(probe)
    update_current_truth(probe)
    write_status_files(probe)
    append_changelog(probe)
    print(json.dumps(json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "repair_probe": probe.get("adapter_id", ""), "overall_goal_complete": False, "report": rel(REPORT_PATH)}), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

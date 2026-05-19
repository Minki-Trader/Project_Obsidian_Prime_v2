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
from stage_pipelines.stage198 import bctl_adverse_excursion_dd_guard_repair as s198  # noqa: E402

s172 = s198.s172

STAGE_ID = "199_adapter_research__stage198_adverse_excursion_followup_review"
RUN_ID = "run199A_stage199_stage198_adverse_excursion_followup_review_v1"
PACKET_ID = "stage199_stage198_adverse_excursion_followup_review_v1"
PARENT_RUN_ID = "run198A_stage198_bctl_adverse_excursion_dd_guard_repair_v1"
SOURCE_STAGE_ID = "198_adapter_research__bctl_adverse_excursion_dd_guard_repair"
SOURCE_RUN_ID = "run198A_stage198_bctl_adverse_excursion_dd_guard_repair_v1"
SOURCE_STAGE198_EVIDENCE_COMMIT = "227466ca040fa074eec46a42afe3bc439afb2fda"
SOURCE_STAGE198_HASH_RECORD_COMMIT = "77a7dadc37cdea355f2112efdb0e3d928325ab8d"
NEXT_STAGE_ID = "200_adapter_research__stage198_mid_drawdown_entry_quality_repair"
NEXT_RUN_ID = "run200A_stage200_stage198_mid_drawdown_entry_quality_repair_v1"
NEXT_PACKET_ID = "stage200_stage198_mid_drawdown_entry_quality_repair_v1"
DECISION = "open_stage200_bounded_mid_drawdown_entry_quality_repair_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage198_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_mid_drawdown_entry_quality_repair"
BOUNDARY = s198.BOUNDARY
LEGACY_34D = s198.LEGACY_34D

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/198_adapter_research__bctl_adverse_excursion_dd_guard_repair/03_reviews/stage198_quality_matrix.csv")
SOURCE_SEGMENT_PATH = Path("stages/198_adapter_research__bctl_adverse_excursion_dd_guard_repair/03_reviews/stage198_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/198_adapter_research__bctl_adverse_excursion_dd_guard_repair/03_reviews/stage198_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/198_adapter_research__bctl_adverse_excursion_dd_guard_repair/03_reviews/stage198_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/198_adapter_research__bctl_adverse_excursion_dd_guard_repair/03_reviews/stage198_adverse_excursion_report.md")
SOURCE_DECISION_PATH = Path("stages/198_adapter_research__bctl_adverse_excursion_dd_guard_repair/03_reviews/stage198_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage199_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage199_adverse_excursion_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage199_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage199_route_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage199_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage199/stage198_adverse_excursion_followup_review.py")


def rel(path: Path | str) -> str:
    return s172.rel(path)


def fnum(value: Any, default: float = 0.0) -> float:
    return s172.parse_float(value, default)


def pct(value: float) -> str:
    return f"{value:.4f}"


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


def full_segment_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "full_split"
        ):
            return row
    return {}


def risk_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def stage199_read(adapter_id: str, row: Mapping[str, Any]) -> str:
    val_net = fnum(row.get("validation_net"))
    val_dd = fnum(row.get("validation_balance_dd_percent"))
    val_mid = fnum(row.get("validation_mid_pf"))
    late_share = fnum(row.get("validation_late_net_share"))
    if adapter_id == "s198_cd8_r0325_ref":
        return "best_reference_not_pass(최선 기준이지만 통과 아님)"
    if adapter_id in {"s198_cd8_sl200_r0325", "s198_cd8_sl195_r0325"}:
        return "atr_stop_tightening_damages_validation_shape(ATR 손절 축소가 검증 형태를 훼손)"
    if adapter_id == "s198_cd8_sl200_flat_r0325":
        return "dd_passes_but_edge_collapses_failure_memory(낙폭은 통과하지만 엣지 붕괴 실패 기억)"
    if val_net < LEGACY_34D["net_profit"] or val_mid < LEGACY_34D["profit_factor"] or val_dd > LEGACY_34D["max_drawdown_percent"] or late_share > 0.50:
        return "candidate_not_final_due_to_segment_or_curve_gap(구간 또는 곡선 결함으로 최종 아님)"
    return "review_required(검토 필요)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    adapter_rows = by_adapter(quality_rows)
    ref = adapter_rows.get("s198_cd8_r0325_ref", {})
    ref_net = fnum(ref.get("validation_net"))
    ref_dd = fnum(ref.get("validation_balance_dd_percent"))
    ref_mid = fnum(ref.get("validation_mid_pf"))
    ref_oos_net = fnum(ref.get("oos_net"))

    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        early = segment_lookup(segment_rows, adapter_id, "validation_is", "early")
        mid = segment_lookup(segment_rows, adapter_id, "validation_is", "mid")
        late = segment_lookup(segment_rows, adapter_id, "validation_is", "late")
        oos_full = full_segment_lookup(segment_rows, adapter_id, "oos")
        val_risk = risk_lookup(risk_rows, adapter_id, "validation_is")
        val_net = fnum(row.get("validation_net"))
        val_dd = fnum(row.get("validation_balance_dd_percent"))
        val_mid = fnum(row.get("validation_mid_pf"))
        late_share = fnum(row.get("validation_late_net_share"))
        oos_net = fnum(row.get("oos_net"))
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "validation_pf": row.get("validation_pf", ""),
                "validation_pf_gap_vs_34d": round(fnum(row.get("validation_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": round(val_net - LEGACY_34D["net_profit"], 6),
                "validation_net_delta_vs_ref": round(val_net - ref_net, 6),
                "validation_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_gap_above_34d": round(val_dd - LEGACY_34D["max_drawdown_percent"], 6),
                "validation_dd_delta_vs_ref": round(val_dd - ref_dd, 6),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d_pf": round(val_mid - LEGACY_34D["profit_factor"], 6),
                "validation_mid_pf_delta_vs_ref": round(val_mid - ref_mid, 6),
                "validation_mid_net": mid.get("net_profit", ""),
                "validation_mid_mfe_capture": mid.get("mfe_capture_ratio", ""),
                "validation_mid_max_closed_trade_drawdown": mid.get("max_closed_trade_drawdown", ""),
                "validation_late_pf": row.get("validation_late_pf", ""),
                "validation_late_net": late.get("net_profit", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_late_share_margin_to_50pct": round(0.50 - late_share, 6),
                "early_net": early.get("net_profit", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_ref": round(oos_net - ref_oos_net, 6),
                "oos_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_mfe_capture": oos_full.get("mfe_capture_ratio", ""),
                "avg_model_risk_pct_validation": val_risk.get("avg_model_risk_pct", ""),
                "avg_executed_lot_validation": val_risk.get("avg_executed_lot", ""),
                "avg_open_sl_points_validation": val_risk.get("avg_open_sl_points", ""),
                "avg_open_tp_points_validation": val_risk.get("avg_open_tp_points", ""),
                "quality_flags": row.get("quality_flags", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "stage199_read": stage199_read(adapter_id, row),
            }
        )
    return rows


def best_reference(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == "s198_cd8_r0325_ref":
            return row
    return max(rows, key=lambda row: fnum(row.get("validation_net")))


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = by_adapter(tradeoff_rows)
    ref = rows.get("s198_cd8_r0325_ref", {})
    sl200 = rows.get("s198_cd8_sl200_r0325", {})
    sl195 = rows.get("s198_cd8_sl195_r0325", {})
    flat = rows.get("s198_cd8_sl200_flat_r0325", {})
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "ATR stop tightening(ATR 손절 축소) from 2.075 to 2.00/1.95 did not reduce validation DD(검증 낙폭).",
            "comparison_baseline": "s198_cd8_r0325_ref reference(기준)",
            "trade_shape": (
                f"ref DD(기준 낙폭)={ref.get('validation_dd_percent')}, "
                f"sl200 DD(2.00 손절 낙폭)={sl200.get('validation_dd_percent')}, "
                f"sl195 DD(1.95 손절 낙폭)={sl195.get('validation_dd_percent')}; "
                f"ref mid PF(기준 중반 수익요인)={ref.get('validation_mid_pf')}, "
                f"sl195 mid PF(1.95 중반 수익요인)={sl195.get('validation_mid_pf')}"
            ),
            "likely_drivers": "Stop-only guard(손절만 쓰는 방어)가 losing-path timing(손실 경로 시점)을 고치지 못하고 validation early/mid edge(검증 초중반 엣지)를 깎았다.",
            "next_probe": "Stage200(200단계)은 exit-only repair(청산만 수리)가 아니라 mid drawdown entry/context quality(중반 낙폭 진입/문맥 품질)를 좁게 본다.",
            "attribution_confidence": "medium_high(중상)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "close_on_flat_signal(평탄 신호 청산)은 DD(낙폭)를 34D(34D) 아래로 낮췄지만 PF/net(수익요인/순손익)을 크게 붕괴시켰다.",
            "comparison_baseline": "s198_cd8_r0325_ref reference(기준)",
            "trade_shape": (
                f"flat PF(평탄 청산 수익요인)={flat.get('validation_pf')}, "
                f"flat net(평탄 청산 순손익)={flat.get('validation_net')}, "
                f"flat DD(평탄 청산 낙폭)={flat.get('validation_dd_percent')}, "
                f"flat OOS net(평탄 청산 표본외 순손익)={flat.get('oos_net')}"
            ),
            "likely_drivers": "Flat-exit lifecycle guard(평탄 청산 생애주기 방어)가 MFE capture(최대 유리 이동 포착)을 죽여서 drawdown optics(낙폭 겉모습)만 좋아졌다.",
            "next_probe": "Treat flat-exit as failure_memory(실패 기억) unless a future variant restores edge(엣지) and segment KPI(구간 핵심 성과 지표).",
            "attribution_confidence": "high(높음)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "OOS(표본외)는 ATR stop tightening(ATR 손절 축소)에서 좋아졌지만 validation(검증) 형태가 나빠졌다.",
            "comparison_baseline": "s198_cd8_r0325_ref reference(기준)",
            "trade_shape": (
                f"ref OOS net(기준 표본외 순손익)={ref.get('oos_net')}, "
                f"sl200 OOS net(2.00 표본외 순손익)={sl200.get('oos_net')}, "
                f"sl195 OOS net(1.95 표본외 순손익)={sl195.get('oos_net')}"
            ),
            "likely_drivers": "OOS(표본외) improvement(개선)은 useful clue(유용한 단서)이지만 validation/OOS consistency(검증/표본외 일관성)는 아직 약하다.",
            "next_probe": "Do not promote(승격하지 않음). Use the clue(단서) only inside bounded repair(경계 수리).",
            "attribution_confidence": "medium(중간)",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage200_primary(200단계 주 경로)",
            "decision": DECISION,
            "source_clue": "s198_cd8_r0325_ref best_reference_not_pass(최선 기준이지만 통과 아님)",
            "bounded_question": "Can entry/context filtering(진입/문맥 필터링) reduce validation mid DD(검증 중반 낙폭) and lift mid PF(중반 수익요인) without killing net/OOS(순손익/표본외)?",
            "why": "Stage198(198단계) showed stop-only and flat-exit fixes are not enough.",
            "guardrail": "no_risk_increase(위험 증가 금지); no_flat_exit_only_acceptance(평탄 청산만으로 수용 금지); preserve_oos_pf_near_1_9(표본외 수익요인 1.9 근처 보존)",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory(실패 기억)",
            "decision": DECISION,
            "source_clue": "s198_cd8_sl200_flat_r0325 dd_pass_edge_collapse(낙폭 통과 엣지 붕괴)",
            "bounded_question": "Do not accept DD(낙폭) improvement when PF/net/MFE(수익요인/순손익/최대 유리 이동) collapse.",
            "why": "Flat-exit result passed DD but failed core KPI(핵심 성과 지표) and OOS net(표본외 순손익).",
            "guardrail": "DD pass is necessary-not-sufficient(낙폭 통과는 필요조건일 뿐 충분조건 아님)",
        },
        {
            "run_id": RUN_ID,
            "route": "bounded_no_go(경계 금지)",
            "decision": DECISION,
            "source_clue": "s198_cd8_sl200_r0325 and s198_cd8_sl195_r0325 stop_tightening_tradeoff(손절 축소 상충)",
            "bounded_question": "Do not keep tightening ATR stop(ATR 손절) inside Stage199(199단계).",
            "why": "Tighter stop worsened validation DD and late concentration while only improving OOS.",
            "guardrail": "Stage199 is review-only(199단계는 검토 전용)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    ref = best_reference(tradeoff_rows)
    lines = [
        "# Stage199 Follow-up Review(199단계 후속 검토)",
        "",
        f"- decision(판정): `{DECISION}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Stage199(199단계)는 Stage198(198단계) 결과를 새로 튜닝하지 않고 review-only(검토 전용)로 판독했다. Effect(효과): ATR stop(ATR 손절)과 flat-exit(평탄 청산) 수리가 KPI(핵심 성과 지표)를 어디서 망가뜨렸는지 분리하고 Stage200(200단계) 질문을 좁힌다.",
        "",
        "## KPI Read(핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            "| {adapter} | {pf} | {net} | {dd} | {mid} | {late} | {oos} | {read} |".format(
                adapter=row["adapter_id"],
                pf=row["validation_pf"],
                net=row["validation_net"],
                dd=row["validation_dd_percent"],
                mid=row["validation_mid_pf"],
                late=row["validation_late_net_share"],
                oos=row["oos_pf"],
                read=row["stage199_read"],
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- best_reference(최선 기준): `{ref.get('adapter_id')}`.",
            f"- 34D gap(34D 격차): validation DD(검증 낙폭) is `{ref.get('validation_dd_gap_above_34d')}` above 34D(34D), and mid PF(중반 수익요인) is `{ref.get('validation_mid_pf_gap_vs_34d_pf')}` vs 34D PF(34D 수익요인).",
            "- ATR stop tightening(ATR 손절 축소)은 validation DD(검증 낙폭)를 줄이지 못했고, late share(후반 비중)를 50% 위로 밀어 올렸다.",
            "- close_on_flat_signal(평탄 신호 청산)은 DD(낙폭)만 통과시켰고 PF/net/MFE(수익요인/순손익/최대 유리 이동)를 무너뜨렸으므로 failure memory(실패 기억)로 남긴다.",
            "- Stage199(199단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.",
            "",
            "## Next Stage(다음 단계)",
            "",
            f"Open `{NEXT_STAGE_ID}` with `{NEXT_RUN_ID}`. Effect(효과): Stage200(200단계)은 risk-only(위험만 조정)나 exit-only(청산만 조정)가 아니라 validation mid drawdown(검증 중반 낙폭)을 만든 entry/context quality(진입/문맥 품질)를 좁게 수리한다.",
        ]
    )
    return "\n".join(lines)


def decision_md() -> str:
    return f"""# Stage199 Decision(199단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage198_evidence_commit(원천 198단계 근거 커밋): `{SOURCE_STAGE198_EVIDENCE_COMMIT}`
- source_stage198_hash_record_commit(원천 198단계 해시 기록 커밋): `{SOURCE_STAGE198_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage199(199단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage200(200단계)에서 entry/context quality(진입/문맥 품질) 수리를 좁게 진행한다.
"""


def write_ledgers(tradeoff_rows: Sequence[Mapping[str, Any]]) -> None:
    ref = best_reference(tradeoff_rows)
    primary_kpi = (
        f"best_reference={ref.get('adapter_id')};"
        f"validation_pf={ref.get('validation_pf')};"
        f"validation_net={ref.get('validation_net')};"
        f"validation_dd={ref.get('validation_dd_percent')};"
        f"validation_mid_pf={ref.get('validation_mid_pf')};"
        f"oos_pf={ref.get('oos_pf')}"
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__stage198_adverse_excursion_followup_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage198_adverse_excursion_followup_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_review",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage198_adverse_excursion_tradeoff",
        "scoreboard_lane": "regular_risk_execution",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": primary_kpi,
        "guardrail_kpi": f"claim_boundary={BOUNDARY};overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage199 reviewed Stage198 adverse-excursion tradeoff and opened Stage200 mid drawdown entry/context quality repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage199_stage198_adverse_excursion_followup_review",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": ledger_pairs(
            (
                ("source_stage198_evidence_commit", SOURCE_STAGE198_EVIDENCE_COMMIT),
                ("source_stage198_hash_record_commit", SOURCE_STAGE198_HASH_RECORD_COMMIT),
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
        (PRODUCER_PATH, "Stage199 follow-up review producer script(생산 스크립트)."),
        (REPORT_PATH, "Stage199 bounded follow-up review report(경계 후속 검토 보고서)."),
        (TRADEOFF_MATRIX_PATH, "Stage199 adverse-excursion tradeoff matrix(불리한 움직임 상충 행렬)."),
        (ATTRIBUTION_PATH, "Stage199 performance attribution(성과 원인 분해)."),
        (ROUTE_MATRIX_PATH, "Stage199 route matrix(경로 행렬)."),
        (DECISION_PATH, "Stage199 decision(판정)."),
        (STAGE_LEDGER_PATH, "Stage199 local ledger(단계 장부)."),
    ]
    created = s172.utc_now()
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage199_followup_review_evidence",
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
        f"""# Stage199 Closeout Packet(199단계 종료 작업 묶음)

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

Stage200(200단계)은 Stage199(199단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can v2-native entry/context filtering(v2 고유 진입/문맥 필터링) repair validation mid drawdown(검증 중반 낙폭) and mid PF(중반 수익요인) without the Stage198(198단계) stop-tightening or flat-exit tradeoff(손절 축소 또는 평탄 청산 상충)?

Effect(효과): Stage198(198단계)의 failure memory(실패 기억)를 보존하면서, risk-only(위험만 조정) 또는 exit-only(청산만 조정) 방식이 아닌 진입 품질 수리로 넘어간다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage200 Input References(200단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_attribution(원천 성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- source_route_matrix(원천 경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage198_quality_matrix(원천 198단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage198_segment_kpi(원천 198단계 구간 핵심 성과 지표): `{rel(SOURCE_SEGMENT_PATH)}`
- source_stage198_risk_atr(원천 198단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage200 Review Index(200단계 검토 색인)

- status(상태): `open_planned_from_stage199`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage200 Selection Status(200단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage199`
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
  Stage199(199단계) closed(종료) as `{DECISION}` and Stage200(200단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage198(198단계)의 ATR stop tightening(ATR 손절 축소)과 flat-exit(평탄 청산) 상충을 실패 기억으로 보존하고, mid drawdown entry/context quality(중반 낙폭 진입/문맥 품질) 수리로 넘어간다.
- >-
  Stage199 evidence(199단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): `s198_cd8_r0325_ref`를 best_reference_not_pass(최선 기준이지만 통과 아님)로 남기고, flat-exit DD pass(평탄 청산 낙폭 통과)를 최종 성공으로 오해하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage199_stage198_adverse_excursion_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage199_stage198_adverse_excursion_followup_review:
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
- adapter_under_review(검토 중 어댑터): `s198_cd8_r0325_ref_best_reference_not_pass`
- status(상태): `stage199_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage199(199단계)는 Stage198(198단계) adverse excursion DD guard(불리한 움직임 낙폭 방어) 결과를 follow-up review(후속 검토)했다. Effect(효과): Stage200(200단계)은 mid drawdown entry/context quality(중반 낙폭 진입/문맥 품질)를 좁게 수리한다.

## Latest Stage199 Evidence(최신 199단계 근거)

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
        f"""# Stage199 Selection Status(199단계 선택 상태)

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
        f"""# Stage199 Review Index(199단계 검토 색인)

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
        f"\n## {s172.utc_now()} Stage199 Stage198 adverse excursion follow-up review closeout(199단계 198단계 불리한 움직임 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage198(198단계)의 stop-tightening/flat-exit(손절 축소/평탄 청산) 상충을 분리하고 Stage200(200단계) entry/context quality repair(진입/문맥 품질 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, segment_rows, risk_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows()
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows))
    s172.write_md(DECISION_PATH, decision_md())
    write_ledgers(tradeoff_rows)
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

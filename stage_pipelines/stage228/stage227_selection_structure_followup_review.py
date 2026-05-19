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

STAGE_ID = "228_adapter_research__stage227_selection_structure_followup_review"
RUN_ID = "run228A_stage228_stage227_selection_structure_followup_review_v1"
PACKET_ID = "stage228_stage227_selection_structure_followup_review_v1"
PARENT_RUN_ID = "run227A_stage227_selection_structure_repair_after_threshold_axis_no_effect_v1"
SOURCE_STAGE_ID = "227_adapter_research__selection_structure_repair_after_threshold_axis_no_effect"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE227_EVIDENCE_COMMIT = "e213ffa63a2bf4c52740fee3a8b669e6f3308ec0"
SOURCE_STAGE227_HASH_RECORD_COMMIT = "5c52c520b8d2270c07895a1ffdaa3a673fb8d2a7"
NEXT_STAGE_ID = "229_adapter_research__dual_objective_guard_blend_after_selection_tradeoff"
NEXT_RUN_ID = "run229A_stage229_dual_objective_guard_blend_after_selection_tradeoff_v1"
NEXT_PACKET_ID = "stage229_dual_objective_guard_blend_after_selection_tradeoff_v1"
DECISION = "open_stage229_bounded_dual_objective_guard_blend_after_selection_tradeoff_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage227_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_dual_objective_guard_blend_after_selection_tradeoff"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}
LOWEDGE_OOS_GAIN = {"oos_net": 765.40, "oos_pf": 1.93, "oos_dd": 7.7935}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_SUMMARY_PATH = SOURCE_ROOT / "stage227_summary.json"
SOURCE_QUALITY_PATH = SOURCE_ROOT / "stage227_quality_matrix.csv"
SOURCE_KPI_PATH = SOURCE_ROOT / "stage227_selection_structure_kpi_summary.csv"
SOURCE_MONTHLY_PATH = SOURCE_ROOT / "stage227_monthly_kpi_summary.csv"
SOURCE_CONCENTRATION_PATH = SOURCE_ROOT / "stage227_concentration_risk_summary.csv"
SOURCE_RISK_PATH = SOURCE_ROOT / "stage227_risk_atr_telemetry.csv"
SOURCE_SEGMENT_PATH = SOURCE_ROOT / "stage227_segment_kpi_summary.csv"
SOURCE_REPORT_PATH = SOURCE_ROOT / "stage227_selection_structure_repair_report.md"
SOURCE_DECISION_PATH = SOURCE_ROOT / "stage227_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage228_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage228_selection_structure_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage228_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage228_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage228_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage228_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage228/stage227_selection_structure_followup_review.py")
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


def profile_label(adapter_id: str) -> str:
    labels = {
        "s227_sel_lowedge_or_control": "oos_preserved_validation_failed(표본외 보존, 검증 실패)",
        "s227_sel_session_only": "balanced_reference_still_below_34d(균형 참조, 34D 미달)",
        "s227_sel_margin_only": "dominated_margin_only(마진 전용 열세)",
        "s227_sel_session_and_margin": "validation_net_recovered_oos_collapsed_midpf_failed(검증 순손익 회복, 표본외 붕괴, 중반 PF 실패)",
    }
    return labels.get(adapter_id, "review_required(검토 필요)")


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
                "profile_label": profile_label(adapter_id),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_early_pf": row.get("validation_early_pf", ""),
                "validation_early_pf_gap_vs_34d": round(fnum(row.get("validation_early_pf")) - LEGACY_34D["profit_factor"], 6),
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
                "oos_net_gap_vs_lowedge_gain": round(fnum(row.get("oos_net")) - LOWEDGE_OOS_GAIN["oos_net"], 2),
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


def best_validation_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(rows, key=lambda row: fnum(row.get("validation_net")), default={})


def best_balance_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        rows,
        key=lambda row: (
            fnum(row.get("oos_net")) >= 700.0,
            fnum(row.get("validation_net")),
            fnum(row.get("oos_net")),
        ),
        default={},
    )


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    validation = best_validation_row(tradeoff_rows)
    balance = best_balance_row(tradeoff_rows)
    return [
        {
            "run_id": RUN_ID,
            "finding": "session_and_margin_recovers_validation_net_but_breaks_oos(세션+마진은 검증 순손익을 회복하지만 표본외를 깬다)",
            "evidence": f"validation_net={validation.get('validation_net')}, early_pf={validation.get('validation_early_pf')}, dd={validation.get('validation_dd_percent')}",
            "damage": f"mid_pf={validation.get('validation_mid_pf')}, oos_net={validation.get('oos_net')}",
            "interpretation": "too much long supply returns validation but loses OOS balance(롱 공급을 너무 돌려주면 검증은 오르지만 표본외 균형이 무너짐)",
            "next_use": "blend with OOS-protective guard instead of adopting as anchor(그대로 채택하지 말고 표본외 보호 구조와 혼합)",
        },
        {
            "run_id": RUN_ID,
            "finding": "session_only_is_best_balance_reference_but_not_enough(세션 전용은 균형 참조지만 충분하지 않다)",
            "evidence": f"validation_net={balance.get('validation_net')}, oos_net={balance.get('oos_net')}, oos_pf={balance.get('oos_pf')}",
            "damage": f"early_pf_gap={balance.get('validation_early_pf_gap_vs_34d')}, mid_pf_gap={balance.get('validation_mid_pf_gap_vs_34d')}",
            "interpretation": "session-only can be the lower-risk bound for next blend(세션 전용은 다음 혼합의 낮은 위험 경계가 될 수 있음)",
            "next_use": "use as control bound in Stage229(229단계 대조 경계로 사용)",
        },
        {
            "run_id": RUN_ID,
            "finding": "margin_only_is_dominated(마진 전용은 열세)",
            "evidence": "validation and OOS both remain below stronger references(검증과 표본외 모두 더 나은 참조보다 낮음)",
            "damage": "late concentration remains high and OOS net falls(후반 집중이 높고 표본외 순손익 하락)",
            "interpretation": "do not continue margin-only as its own campaign(마진 전용을 독립 캠페인으로 계속하지 않음)",
            "next_use": "preserve only as failure memory(실패 기억으로만 보존)",
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "open_stage229_dual_objective_guard_blend(229단계 이중목표 보호 혼합 개방)",
            "action": "combine session-only OOS preservation with session-and-margin validation recovery(세션 전용 표본외 보존과 세션+마진 검증 회복을 혼합)",
            "effect": "targets the exact Stage227 tradeoff without repeating the same structures(같은 구조 반복 없이 227단계 상충을 직접 겨냥)",
            "risk": "blend may still fail both validation and OOS(혼합이 검증과 표본외 모두 실패할 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "stop_margin_only_axis(마진 전용 축 중단)",
            "action": "record margin-only as dominated evidence(마진 전용을 열세 근거로 기록)",
            "effect": "prevents a standalone margin campaign(마진 단독 캠페인 방지)",
            "risk": "one unexplored margin sub-window may be missed(미시험 마진 세부 구간 하나를 놓칠 수 있음)",
        },
        {
            "run_id": RUN_ID,
            "route": "no_final_claim_no_onnx_hardening(최종 주장 없음, ONNX 경화 없음)",
            "action": "keep adapter in research repair path(어댑터를 연구 수리 경로에 둠)",
            "effect": "prevents KPI partial improvement from becoming completion(부분 KPI 개선을 완료로 오해하지 않게 함)",
            "risk": "additional bounded stages are required(추가 경계 단계 필요)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage228 Follow-up Review(228단계 후속 검토)",
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
        "- Stage227(227단계)은 선택 구조를 바꾸면 무엇이 움직이는지 보여줬다.",
        "- `session_and_margin(세션+마진)`은 validation net(검증 순손익)을 1046.57까지 올렸지만 OOS net(표본외 순손익)을 625.27로 깎았다.",
        "- `session_only(세션 전용)`은 균형이 낫지만 validation net(검증 순손익) 952.16으로 34D(34D 기준)에 모자랐다.",
        "- 다음은 둘을 섞는 dual-objective guard blend(이중목표 보호 혼합)이다.",
        "",
        "## KPI Tradeoff(KPI 핵심 성과 지표 상충)",
        "",
        "| adapter(어댑터) | profile(유형) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | OOS gap(표본외 차이) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {row.get('profile_label', '')} | "
            f"{row.get('validation_net', '')} | {row.get('validation_early_pf', '')} | "
            f"{row.get('validation_mid_pf', '')} | {row.get('oos_net', '')} | "
            f"{row.get('oos_net_gap_vs_lowedge_gain', '')} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage227 selection structure repair(227단계 선택 구조 수리).",
            "- judgment_label(판정 라벨): selection_structure_tradeoff_not_final(선택 구조 상충, 최종 아님).",
            "- next_condition(다음 조건): Stage229(229단계)는 session-only(세션 전용)의 OOS 보존과 session-and-margin(세션+마진)의 검증 회복을 하나의 좁은 혼합 축으로 시험한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(best: Mapping[str, Any]) -> str:
    return f"""# Stage228 Decision(228단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage227_evidence_commit(원천 227단계 근거 커밋): `{SOURCE_STAGE227_EVIDENCE_COMMIT}`
- source_stage227_hash_record_commit(원천 227단계 해시 기록 커밋): `{SOURCE_STAGE227_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- best_validation_clue(최대 검증 단서): `{best.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage228(228단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage229(229단계)은 selection structure(선택 구조)를 다시 반복하지 않고, validation recovery(검증 회복)와 OOS preservation(표본외 보존)을 동시에 보는 좁은 blend(혼합) 축으로 간다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage228_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage228 Stage227 selection structure follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(best: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("best_validation_clue", best.get("adapter_id", "")),
            ("validation_net", best.get("validation_net", "")),
            ("validation_mid_pf", best.get("validation_mid_pf", "")),
            ("oos_net", best.get("oos_net", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs((("next_stage", NEXT_STAGE_ID), ("stage228_role", "review_only_no_tuning"), ("boundary", BOUNDARY)))
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage228_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage228_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage227_selection_structure_followup_review(227단계 선택 구조 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage228 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; best_validation_clue={best.get('adapter_id', '')}; boundary={BOUNDARY}",
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
        "best_validation_clue": best.get("adapter_id", ""),
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
        f"""# Stage228 Closeout Packet(228단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- best_validation_clue(최대 검증 단서): `{best.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(best: Mapping[str, Any]) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage229(229단계)는 Stage228(228단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a dual-objective guard blend(이중목표 보호 혼합) recover validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), and drawdown(낙폭) without losing the OOS preservation(표본외 보존) seen in the safer Stage227 session-only(세션 전용) structure?

Effect(효과): `session_and_margin(세션+마진)`의 validation gain(검증 개선)을 그대로 채택하지 않고, `session_only(세션 전용)`의 OOS balance(표본외 균형)를 경계로 둔 혼합만 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage229 Input References(229단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- best_validation_clue(최대 검증 단서): `{best.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage227_quality_matrix(원천 227단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage227_risk_atr_telemetry(원천 227단계 위험/ATR 기록): `{rel(SOURCE_RISK_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage229 Review Index(229단계 검토 색인)

- status(상태): `open_planned_from_stage228`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage229 Selection Status(229단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage228`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(best: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage228(228단계) closed(종료) as `{DECISION}` and Stage229(229단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage227(227단계)의 선택 구조 상충을 dual-objective guard blend(이중목표 보호 혼합)로 좁힌다.
- >-
  Stage228 evidence(228단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): session-only(세션 전용)와 session-and-margin(세션+마진)을 다음 수리의 양쪽 경계로 기록한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage228_stage227_selection_structure_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage228_stage227_selection_structure_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  best_validation_clue: {best.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `stage229_dual_objective_guard_blend_after_selection_tradeoff`
- status(상태): `stage228_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage228(228단계)는 Stage227(227단계) selection structure repair(선택 구조 수리)를 review-only(검토 전용)로 닫았다. Effect(효과): Stage229(229단계)는 validation(검증)과 OOS(표본외)를 동시에 보는 blend(혼합) 축만 시험한다.

## Latest Stage228 Evidence(최신 228단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- best_validation_clue(최대 검증 단서): `{best.get('adapter_id', '')}`
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
        f"""# Stage228 Selection Status(228단계 선택 상태)

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
        f"""# Stage228 Review Index(228단계 검토 색인)

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
        f"\n## {utc_now()} Stage228 selection structure follow-up review closeout(228단계 선택 구조 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage227(227단계) 상충을 session-only(세션 전용)와 session-and-margin(세션+마진) 경계로 나눠 Stage229(229단계) 혼합 축으로 넘겼다.\n"
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
    best = best_validation_row(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows)
    route_rows = build_route_rows()

    write_md(REPORT_PATH, report_md(tradeoff_rows))
    write_md(DECISION_PATH, decision_md(best))
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
            "tradeoff_rows": tradeoff_rows,
            "attribution_rows": attribution_rows,
            "route_rows": route_rows,
            "best_validation_clue": best,
            "legacy_34d": LEGACY_34D,
            "lowedge_oos_gain": LOWEDGE_OOS_GAIN,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_ledgers(best)
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, best)
    write_next_stage_seed(best)
    update_current_truth(best)
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
                    "best_validation_clue": best.get("adapter_id", ""),
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

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
from stage_pipelines.stage210 import oos_net_recovery_preserve_validation_gate as s210  # noqa: E402

s172 = s210.s172

STAGE_ID = "211_adapter_research__stage210_oos_net_recovery_followup_review"
RUN_ID = "run211A_stage211_stage210_oos_net_recovery_followup_review_v1"
PACKET_ID = "stage211_stage210_oos_net_recovery_followup_review_v1"
PARENT_RUN_ID = "run210A_stage210_oos_net_recovery_preserve_stage208_validation_gate_v1"
SOURCE_STAGE_ID = "210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate"
SOURCE_RUN_ID = "run210A_stage210_oos_net_recovery_preserve_stage208_validation_gate_v1"
SOURCE_STAGE210_EVIDENCE_COMMIT = "80026754f6a61e5adfcf22c4144f523246afb5b1"
SOURCE_STAGE210_HASH_RECORD_COMMIT = "8489bf7b1ed039658b361ae9617777268882bb03"
NEXT_STAGE_ID = "212_adapter_research__stage210_candidate_segment_equity_audit"
NEXT_RUN_ID = "run212A_stage212_stage210_candidate_segment_equity_audit_v1"
NEXT_PACKET_ID = "stage212_stage210_candidate_segment_equity_audit_v1"
DECISION = "open_stage212_bounded_segment_equity_audit_for_s210_r0315_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage210_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_stage210_candidate_audit"
BOUNDARY = s210.BOUNDARY
LEGACY_34D = s210.LEGACY_34D
STAGE171_PRIMARY = s210.STAGE171_PRIMARY
SELECTED_ANCHOR_ID = "s210_ls_r0315"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_quality_matrix.csv")
SOURCE_KPI_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_oos_net_recovery_kpi_summary.csv")
SOURCE_SEGMENT_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_oos_net_recovery_report.md")
SOURCE_DECISION_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage211_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage211_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage211_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage211_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage211_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage211_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage211/stage210_oos_net_recovery_followup_review.py")
ARTIFACT_COLUMNS = s210.ARTIFACT_COLUMNS


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


def risk_lookup(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def validation_gate_pass(row: Mapping[str, Any]) -> bool:
    return (
        fnum(row.get("validation_net")) >= LEGACY_34D["net_profit"]
        and fnum(row.get("validation_balance_dd_percent")) <= LEGACY_34D["max_drawdown_percent"]
        and fnum(row.get("validation_pf")) >= LEGACY_34D["profit_factor"]
        and fnum(row.get("validation_mid_pf")) >= LEGACY_34D["profit_factor"]
    )


def stage211_read(adapter_id: str, gate_pass: bool, hard_pass: bool) -> str:
    if adapter_id == "s210_ls_r03175":
        return "net_highest_but_dd_above_34d(순손익 최고이나 낙폭 34D 초과)"
    if adapter_id == SELECTED_ANCHOR_ID and hard_pass:
        return "selected_candidate_validation_gate_and_oos_recovery_best(선택 후보, 검증 관문 통과 및 표본외 회복 최선)"
    if gate_pass:
        return "validation_gate_pass_but_lower_oos_than_selected(검증 관문 통과, 선택 후보보다 표본외 낮음)"
    return "not_selected(미선택)"


def build_tradeoff_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    kpi_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        val_kpi = kpi_lookup(kpi_rows, adapter_id, "validation_is")
        oos_kpi = kpi_lookup(kpi_rows, adapter_id, "oos")
        val_mid = segment_lookup(segment_rows, adapter_id, "validation_is", "mid")
        oos_mid = segment_lookup(segment_rows, adapter_id, "oos", "mid")
        val_risk = risk_lookup(risk_rows, adapter_id, "validation_is")
        oos_risk = risk_lookup(risk_rows, adapter_id, "oos")
        gate_pass = validation_gate_pass(row)
        hard_pass = str(row.get("hard_quality_pass", "")).lower() == "true"
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "model_risk_max_pct": row.get("model_risk_max_pct", ""),
                "validation_gate_pass": gate_pass,
                "hard_quality_pass": hard_pass,
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_balance_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_trade_count": val_kpi.get("trade_count", ""),
                "validation_mid_net": val_mid.get("net_profit", ""),
                "validation_mid_mfe_capture": val_mid.get("mfe_capture_ratio", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_delta_vs_stage171_primary": row.get("stage171_oos_net_delta", ""),
                "oos_balance_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_late_net_share": row.get("oos_late_net_share", ""),
                "oos_trade_count": oos_kpi.get("trade_count", ""),
                "oos_mid_net": oos_mid.get("net_profit", ""),
                "oos_mid_mfe_capture": oos_mid.get("mfe_capture_ratio", ""),
                "risk_floor_applied_count_validation": val_risk.get("risk_floor_applied_count", ""),
                "risk_floor_applied_count_oos": oos_risk.get("risk_floor_applied_count", ""),
                "avg_executed_lot_validation": val_risk.get("avg_executed_lot", ""),
                "avg_executed_lot_oos": oos_risk.get("avg_executed_lot", ""),
                "risk_bucket_validation": val_risk.get("risk_bucket", ""),
                "risk_bucket_oos": oos_risk.get("risk_bucket", ""),
                "quality_flags": row.get("quality_flags", ""),
                "stage211_read": stage211_read(adapter_id, gate_pass, hard_pass),
            }
        )
    return rows


def selected_anchor(tradeoff_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in tradeoff_rows:
        if row.get("adapter_id") == SELECTED_ANCHOR_ID:
            return row
    return {}


def build_attribution_rows(anchor: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "finding": "s210_r0315_is_best_stage210_candidate(s210 r0315가 210단계 최선 후보)",
            "evidence": f"val_net={anchor.get('validation_net')}, val_dd={anchor.get('validation_balance_dd_percent')}, mid_pf={anchor.get('validation_mid_pf')}, oos_net={anchor.get('oos_net')}",
            "meaning": "validation KPI(검증 핵심 성과 지표)는 34D(34D)를 넘고 OOS net(표본외 순손익)은 Stage208 r0305보다 개선됐다.",
            "next_use": "Stage212(212단계)는 curve/segment(곡선/구간) 안정성을 감사한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "upper_bound_found_before_dd_break(낙폭 파손 전 상한 발견)",
            "evidence": "s210_ls_r03175 has validation DD above 34D(검증 낙폭 34D 초과)",
            "meaning": "risk cap(위험 상한)만 더 올리는 방식은 이미 DD(낙폭) 한계에 닿았다.",
            "next_use": "추가 수리가 필요하면 risk cap(위험 상한) 단독이 아니라 bracket/lifecycle/equity review(브래킷/생애주기/잔고곡선 검토)로 분리한다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "not_final_even_with_hard_pass_review_required(엄격 통과 검토 표식이 있어도 최종 아님)",
            "evidence": "decision remains candidate_not_final(후보, 최종 아님)",
            "meaning": "segment/equity concentration(구간/잔고 집중), monthly behavior(월별 행동), telemetry(기록)를 확인해야 한다.",
            "next_use": "Stage212(212단계) audit gate(감사 관문)를 연다.",
        },
    ]


def build_route_rows(anchor: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage212_primary_audit_anchor(212단계 주 감사 기준 후보)",
            "adapter_id": anchor.get("adapter_id", SELECTED_ANCHOR_ID),
            "action": "carry_forward_to_segment_equity_audit(구간/잔고곡선 감사로 이월)",
            "effect": "prevents final claim from KPI alone(KPI만으로 최종 주장하지 않음)",
            "risk": "hidden concentration may remain(숨은 집중 위험 가능)",
        },
        {
            "run_id": RUN_ID,
            "route": "do_not_continue_risk_cap_only(위험 상한 단독 계속 금지)",
            "adapter_id": "s210_ls_r03175",
            "action": "preserve_as_failure_memory(실패 기억으로 보존)",
            "effect": "records DD boundary(낙폭 경계 기록)",
            "risk": "none_if_not_selected(미선택이면 없음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], anchor: Mapping[str, Any]) -> str:
    lines = [
        "# Stage211 Follow-up Review(211단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage210_evidence_commit(원천 210단계 근거 커밋): `{SOURCE_STAGE210_EVIDENCE_COMMIT}`",
        f"- source_stage210_hash_record_commit(원천 210단계 해시 기록 커밋): `{SOURCE_STAGE210_HASH_RECORD_COMMIT}`",
        f"- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## KPI Read(KPI 핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | risk cap(위험 상한) | val gate(검증 관문) | hard pass(엄격 통과) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | read(판독) |",
        "|---|---:|---|---|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            "| {adapter} | {risk} | {gate} | {hard} | {vnet} | {vdd} | {midpf} | {onet} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                risk=row.get("model_risk_max_pct", ""),
                gate=row.get("validation_gate_pass", ""),
                hard=row.get("hard_quality_pass", ""),
                vnet=row.get("validation_net", ""),
                vdd=row.get("validation_balance_dd_percent", ""),
                midpf=row.get("validation_mid_pf", ""),
                onet=row.get("oos_net", ""),
                read=row.get("stage211_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- `s210_ls_r0315`는 Stage210(210단계) 최선 후보다.",
            "- `s210_ls_r03175`는 validation DD(검증 낙폭)가 34D(34D)를 넘어 risk cap(위험 상한) 단독 확장은 여기서 멈춘다.",
            "- Stage211(211단계)은 final(최종)이나 deployment(배포)를 주장하지 않는다.",
            "- Effect(효과): Stage212(212단계)에서 segment/equity curve audit(구간/잔고곡선 감사)로 품질을 확인한다.",
        ]
    )
    return "\n".join(lines)


def decision_md(anchor: Mapping[str, Any]) -> str:
    return f"""# Stage211 Decision(211단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage210_evidence_commit(원천 210단계 근거 커밋): `{SOURCE_STAGE210_EVIDENCE_COMMIT}`
- source_stage210_hash_record_commit(원천 210단계 해시 기록 커밋): `{SOURCE_STAGE210_HASH_RECORD_COMMIT}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage211(211단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage212(212단계)에서 `s210_ls_r0315`의 segment/equity(구간/잔고곡선) 품질을 따로 감사한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
    paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_MATRIX_PATH, ATTRIBUTION_PATH, ROUTE_MATRIX_PATH, SUMMARY_JSON_PATH, DECISION_PATH, STAGE_LEDGER_PATH]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage211_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage211 Stage210 OOS net recovery follow-up review evidence.",
        }
        for path in paths
    ]


def write_ledgers(anchor: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("selected_anchor", anchor.get("adapter_id", "")),
            ("validation_net", anchor.get("validation_net", "")),
            ("validation_dd", anchor.get("validation_balance_dd_percent", "")),
            ("oos_net", anchor.get("oos_net", "")),
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
            "ledger_row_id": f"{RUN_ID}__stage211_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage211_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage210_oos_recovery_followup_review(210단계 표본외 회복 후속 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage211 review-only closeout; not final and not deployment.",
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
            "notes": f"source_run={SOURCE_RUN_ID}; selected_anchor={anchor.get('adapter_id', '')}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(tradeoff_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], anchor: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "selected_next_anchor": anchor.get("adapter_id", ""),
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
        f"""# Stage211 Closeout Packet(211단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(anchor: Mapping[str, Any]) -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage212(212단계)은 Stage211(211단계) 판정에서 열린 bounded audit(경계 감사) 단계다.

## Bounded Question(경계 질문)

Does `{anchor.get('adapter_id', SELECTED_ANCHOR_ID)}` have acceptable segment KPI(구간 핵심 성과 지표), monthly behavior(월별 행동), equity/balance curve(자산/잔고 곡선), concentration risk(집중 위험), and risk/ATR telemetry(위험/ATR 기록) to remain the active research candidate?

Effect(효과): Stage210(210단계)의 좋은 final net(최종 순손익)을 바로 완료로 보지 않고, 곡선과 구간 안정성으로 확인한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage212 Input References(212단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_stage210_quality_matrix(원천 210단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage210_segment_kpi(원천 210단계 구간 KPI): `{rel(SOURCE_SEGMENT_PATH)}`
- source_stage210_balance_audit(원천 210단계 잔고 감사): `{rel(SOURCE_BALANCE_PATH)}`
- source_stage210_risk_atr_telemetry(원천 210단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR_PATH)}`
""",
    )
    s172.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"# Stage212 Review Index(212단계 검토 색인)\n\n- status(상태): `open_planned_from_stage211`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n")
    s172.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"# Stage212 Selection Status(212단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage211`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def update_current_truth(anchor: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage211(211단계) closed(종료) as `{DECISION}` and Stage212(212단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): `{anchor.get('adapter_id', '')}`를 segment/equity audit(구간/잔고곡선 감사)로 넘긴다.
- >-
  Stage211 evidence(211단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): KPI(핵심 성과 지표) 개선과 남은 감사 필요성을 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage211_stage210_oos_net_recovery_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage211_stage210_oos_net_recovery_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  selected_next_anchor: {anchor.get('adapter_id', '')}
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
- adapter_under_review(검토 중 어댑터): `{anchor.get('adapter_id', '')}`
- status(상태): `stage211_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage211(211단계)는 Stage210(210단계) OOS net recovery(표본외 순손익 회복)를 follow-up review(후속 검토)했다. Effect(효과): Stage212(212단계)는 segment/equity audit(구간/잔고곡선 감사)만 좁게 진행한다.

## Latest Stage211 Evidence(최신 211단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(anchor: Mapping[str, Any]) -> None:
    s172.write_md(SELECTED_ROOT / "selection_status.md", f"# Stage211 Selection Status(211단계 선택 상태)\n\n- stage_status(단계 상태): `closed_{DECISION}`\n- current_packet(현재 작업 묶음): `{PACKET_ID}`\n- current_run(현재 실행): `{RUN_ID}`\n- source_stage(원천 단계): `{SOURCE_STAGE_ID}`\n- source_run(원천 실행): `{SOURCE_RUN_ID}`\n- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`\n- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`\n- decision(판정): `{DECISION}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")
    s172.write_md(REVIEWS_ROOT / "review_index.md", f"# Stage211 Review Index(211단계 검토 색인)\n\n- status(상태): `closed_{DECISION}`\n- packet(작업 묶음): `{PACKET_ID}`\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`\n- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`\n- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n")


def append_changelog(anchor: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage211 Stage210 OOS net recovery follow-up review closeout(211단계 210단계 표본외 순손익 회복 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): selected(선택) `{anchor.get('adapter_id', '')}` for Stage212(212단계) segment/equity audit(구간/잔고곡선 감사).\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    kpi_rows = read_csv(SOURCE_KPI_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, kpi_rows, segment_rows, risk_rows)
    anchor = selected_anchor(tradeoff_rows)
    attribution_rows = build_attribution_rows(anchor)
    route_rows = build_route_rows(anchor)
    write_csv(TRADEOFF_MATRIX_PATH, tradeoff_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    s172.write_md(REPORT_PATH, report_md(tradeoff_rows, anchor))
    s172.write_md(DECISION_PATH, decision_md(anchor))
    write_ledgers(anchor)
    summary_payload = {
        "run_id": RUN_ID,
        "decision": DECISION,
        "selected_next_anchor": anchor.get("adapter_id", ""),
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "route_rows": route_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(SUMMARY_JSON_PATH, summary_payload)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(tradeoff_rows, attribution_rows, route_rows, anchor)
    write_next_stage_seed(anchor)
    update_current_truth(anchor)
    write_status_files(anchor)
    append_changelog(anchor)
    print(json.dumps(json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "selected_next_anchor": anchor.get("adapter_id", ""), "overall_goal_complete": False, "report": rel(REPORT_PATH)}), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
from stage_pipelines.stage208 import risk_cap_interpolation_repair as s208  # noqa: E402

s172 = s208.s172

STAGE_ID = "209_adapter_research__stage208_risk_cap_interpolation_followup_review"
RUN_ID = "run209A_stage209_stage208_risk_cap_interpolation_followup_review_v1"
PACKET_ID = "stage209_stage208_risk_cap_interpolation_followup_review_v1"
PARENT_RUN_ID = "run208A_stage208_stage206_risk_cap_interpolation_repair_v1"
SOURCE_STAGE_ID = "208_adapter_research__stage206_risk_cap_interpolation_repair"
SOURCE_RUN_ID = "run208A_stage208_stage206_risk_cap_interpolation_repair_v1"
SOURCE_STAGE208_EVIDENCE_COMMIT = "af3b2acbb32a1576c395270e937ea2465bb7aff0"
SOURCE_STAGE208_HASH_RECORD_COMMIT = "e5e921b20d59fc11ea61bb8379303eba6ef27979"
NEXT_STAGE_ID = "210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate"
NEXT_RUN_ID = "run210A_stage210_oos_net_recovery_preserve_stage208_validation_gate_v1"
NEXT_PACKET_ID = "stage210_oos_net_recovery_preserve_stage208_validation_gate_v1"
DECISION = "open_stage210_bounded_oos_net_recovery_preserve_stage208_validation_gate_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage208_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_oos_net_recovery_preserve_validation_gate"
BOUNDARY = s208.BOUNDARY
LEGACY_34D = s208.LEGACY_34D
STAGE171_PRIMARY = s208.STAGE171_PRIMARY

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_QUALITY_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_quality_matrix.csv")
SOURCE_KPI_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_risk_cap_kpi_summary.csv")
SOURCE_SEGMENT_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_balance_curve_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_risk_atr_telemetry.csv")
SOURCE_REPORT_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_risk_cap_report.md")
SOURCE_DECISION_PATH = Path("stages/208_adapter_research__stage206_risk_cap_interpolation_repair/03_reviews/stage208_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage209_followup_review.md"
TRADEOFF_MATRIX_PATH = REVIEWS_ROOT / "stage209_tradeoff_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage209_performance_attribution.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage209_route_matrix.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage209_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage209_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage209/stage208_risk_cap_interpolation_followup_review.py")
ARTIFACT_COLUMNS = s208.ARTIFACT_COLUMNS


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


def stage209_read(adapter_id: str, gate_pass: bool, oos_gap: float) -> str:
    if adapter_id == "s208_ls_r0275":
        return "risk0275_dd_good_but_validation_net_below_34d(2.75% 위험은 낙폭은 좋지만 검증 순손익 34D 미달)"
    if adapter_id == "s208_ls_r0305" and gate_pass:
        return "best_next_anchor_highest_net_oos_but_dd_margin_tight(다음 기준 후보, 순손익/표본외 최고이나 낙폭 여유 좁음)"
    if gate_pass and oos_gap < 0:
        return "validation_gate_pass_but_oos_net_gap_remains(검증 관문 통과, 표본외 순손익 격차 잔존)"
    if gate_pass:
        return "validation_gate_pass_review_only(검증 관문 통과, 검토 전용)"
    return "validation_gate_not_met(검증 관문 미충족)"


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
        oos_gap = fnum(row.get("oos_net")) - STAGE171_PRIMARY["oos_net"]
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "axis": row.get("axis", ""),
                "model_risk_max_pct": row.get("model_risk_max_pct", ""),
                "validation_gate_pass": gate_pass,
                "validation_pf": row.get("validation_pf", ""),
                "validation_net": row.get("validation_net", ""),
                "validation_net_gap_vs_34d": row.get("validation_net_gap_vs_34d", ""),
                "validation_balance_dd_percent": row.get("validation_balance_dd_percent", ""),
                "validation_dd_margin_vs_34d": row.get("validation_dd_margin_vs_34d", ""),
                "validation_mid_pf": row.get("validation_mid_pf", ""),
                "validation_mid_pf_gap_vs_34d_pf": round(fnum(row.get("validation_mid_pf")) - LEGACY_34D["profit_factor"], 6),
                "validation_late_net_share": row.get("validation_late_net_share", ""),
                "validation_trade_count": val_kpi.get("trade_count", ""),
                "validation_mid_net": val_mid.get("net_profit", ""),
                "validation_mid_mfe_capture": val_mid.get("mfe_capture_ratio", ""),
                "oos_pf": row.get("oos_pf", ""),
                "oos_net": row.get("oos_net", ""),
                "oos_net_gap_vs_stage171_primary": round(oos_gap, 6),
                "oos_balance_dd_percent": row.get("oos_balance_dd_percent", ""),
                "oos_late_net_share": row.get("oos_late_net_share", ""),
                "oos_trade_count": oos_kpi.get("trade_count", ""),
                "oos_mid_net": oos_mid.get("net_profit", ""),
                "oos_mid_mfe_capture": oos_mid.get("mfe_capture_ratio", ""),
                "risk_floor_applied_count_validation": val_risk.get("risk_floor_applied_count", ""),
                "risk_floor_applied_count_oos": oos_risk.get("risk_floor_applied_count", ""),
                "max_model_risk_pct_validation": val_risk.get("max_model_risk_pct", ""),
                "max_actual_risk_pct_after_floor_validation": val_risk.get("max_actual_risk_pct_after_floor", ""),
                "avg_executed_lot_validation": val_risk.get("avg_executed_lot", ""),
                "avg_executed_lot_oos": oos_risk.get("avg_executed_lot", ""),
                "risk_bucket_validation": val_risk.get("risk_bucket", ""),
                "risk_bucket_oos": oos_risk.get("risk_bucket", ""),
                "hard_quality_pass": row.get("hard_quality_pass", ""),
                "quality_flags": row.get("quality_flags", ""),
                "stage209_read": stage209_read(adapter_id, gate_pass, oos_gap),
            }
        )
    return rows


def select_anchor(tradeoff_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in tradeoff_rows if str(row.get("validation_gate_pass")) == "True" or row.get("validation_gate_pass") is True]
    if not candidates:
        return {}
    return max(candidates, key=lambda row: (fnum(row.get("oos_net")), fnum(row.get("validation_net"))))


def build_attribution_rows(tradeoff_rows: Sequence[Mapping[str, Any]], anchor: Mapping[str, Any]) -> list[dict[str, Any]]:
    by_id = {str(row.get("adapter_id")): row for row in tradeoff_rows}
    r0275 = by_id.get("s208_ls_r0275", {})
    r0285 = by_id.get("s208_ls_r0285", {})
    r0295 = by_id.get("s208_ls_r0295", {})
    r0305 = by_id.get("s208_ls_r0305", {})
    return [
        {
            "run_id": RUN_ID,
            "finding": "risk_cap_interpolation_found_validation_pass_zone(위험 상한 보간이 검증 통과 구간을 찾음)",
            "evidence": f"r0285/r0295/r0305 val_net={r0285.get('validation_net')}/{r0295.get('validation_net')}/{r0305.get('validation_net')} and val_dd={r0285.get('validation_balance_dd_percent')}/{r0295.get('validation_balance_dd_percent')}/{r0305.get('validation_balance_dd_percent')}",
            "meaning": "2.85%-3.05%(2.85%-3.05%) risk cap(위험 상한)은 validation net/PF/midPF/DD(검증 순손익/수익요인/중반 수익요인/낙폭)를 34D(34D) 문턱 안에 넣었다.",
            "next_use": "Stage210(210단계)는 이 검증 관문을 보존 조건으로 둔다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "risk0275_too_much_net_compression(2.75% 위험은 순손익 압축 과도)",
            "evidence": f"r0275 val_net={r0275.get('validation_net')} gap_vs_34d={r0275.get('validation_net_gap_vs_34d')}",
            "meaning": "DD(낙폭)는 좋아졌지만 net(순손익)이 34D(34D)를 넘지 못해 anchor(기준 후보)로 쓰기 어렵다.",
            "next_use": "r0275는 downside bound(하한 참고)로만 남긴다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "r0305_best_next_anchor_but_not_final(r0305가 다음 기준 후보이나 최종 아님)",
            "evidence": f"selected={anchor.get('adapter_id')}, val_net={anchor.get('validation_net')}, val_dd={anchor.get('validation_balance_dd_percent')}, oos_net={anchor.get('oos_net')}, oos_gap={anchor.get('oos_net_gap_vs_stage171_primary')}",
            "meaning": "r0305는 Stage208(208단계) 중 validation/OOS net(검증/표본외 순손익)이 가장 높고 DD(낙폭)도 34D(34D) 아래지만, OOS net(표본외 순손익)은 Stage171(171단계) 주 후보보다 낮다.",
            "next_use": "Stage210(210단계)는 r0305에서 OOS net(표본외 순손익)을 회복하되 validation gate(검증 관문)를 깨지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "finding": "hard_quality_pass_still_false_due_to_oos_gap(표본외 격차 때문에 엄격 품질 통과는 아직 거짓)",
            "evidence": "all Stage208 candidates keep oos_net_materially_below_stage171_primary flag(모든 208단계 후보가 표본외 순손익 약점 표식을 유지)",
            "meaning": "34D(34D) 검증 KPI(핵심 성과 지표) 일부를 넘겨도 research package(연구 패키지) 완료가 아니다.",
            "next_use": "ONNX(온닉스)나 deployment(배포) 쪽으로 가지 않고 bounded repair(경계 수리)를 계속한다.",
        },
    ]


def build_route_rows(anchor: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "route": "stage210_primary_anchor(210단계 주 기준 후보)",
            "adapter_id": anchor.get("adapter_id", "s208_ls_r0305"),
            "action": "carry_forward_with_oos_recovery_guard(표본외 회복 조건으로 이월)",
            "effect": "highest validation/OOS net among Stage208 while still below 34D DD(208단계 중 검증/표본외 순손익 최고이면서 34D 낙폭 아래)",
            "risk": "validation DD margin is tight(검증 낙폭 여유가 좁음)",
        },
        {
            "run_id": RUN_ID,
            "route": "stage210_backup_dd_conservative(210단계 보조 낙폭 보수 후보)",
            "adapter_id": "s208_ls_r0285",
            "action": "preserve_as_backup_not_selected(보조 후보로 보존, 선택 아님)",
            "effect": "better DD/midPF margin(낙폭/중반 수익요인 여유가 더 큼)",
            "risk": "lower validation/OOS net(검증/표본외 순손익이 낮음)",
        },
        {
            "run_id": RUN_ID,
            "route": "do_not_start_onnx_or_finalization(ONNX 또는 최종화 시작 금지)",
            "adapter_id": "all_stage208_candidates",
            "action": "continue_bounded_repair(경계 수리 계속)",
            "effect": "prevents overclaim from validation KPI improvement(검증 KPI 개선을 과장하지 않음)",
            "risk": "none_if_boundary_is_kept(경계 유지 시 없음)",
        },
    ]


def report_md(tradeoff_rows: Sequence[Mapping[str, Any]], anchor: Mapping[str, Any]) -> str:
    lines = [
        "# Stage209 Follow-up Review(209단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage208_evidence_commit(원천 208단계 근거 커밋): `{SOURCE_STAGE208_EVIDENCE_COMMIT}`",
        f"- source_stage208_hash_record_commit(원천 208단계 해시 기록 커밋): `{SOURCE_STAGE208_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`",
        f"- decision(판정): `{DECISION}`",
        f"- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', 'none')}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Bounded Question(경계 질문)",
        "",
        "Did Stage208(208단계) find a risk cap(위험 상한) that lowers validation DD(검증 낙폭) below 34D(34D) while preserving validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인), trade supply(거래 공급), OOS(표본외), and risk/ATR telemetry(위험/ATR 기록)?",
        "",
        "## KPI Read(KPI 핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | risk cap(위험 상한) | val gate(검증 관문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | OOS gap(표본외 격차) | read(판독) |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        lines.append(
            "| {adapter} | {risk} | {gate} | {vpf} | {vnet} | {vdd} | {midpf} | {onet} | {ogap} | {read} |".format(
                adapter=row.get("adapter_id", ""),
                risk=row.get("model_risk_max_pct", ""),
                gate=row.get("validation_gate_pass", ""),
                vpf=row.get("validation_pf", ""),
                vnet=row.get("validation_net", ""),
                vdd=row.get("validation_balance_dd_percent", ""),
                midpf=row.get("validation_mid_pf", ""),
                onet=row.get("oos_net", ""),
                ogap=row.get("oos_net_gap_vs_stage171_primary", ""),
                read=row.get("stage209_read", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- Stage208(208단계)는 validation(검증) 34D(34D) 문턱을 넘는 risk cap zone(위험 상한 구간)을 찾았다.",
            "- `s208_ls_r0305`는 net/OOS(순손익/표본외)가 가장 좋고 validation DD(검증 낙폭)가 34D(34D) 아래라 Stage210(210단계) 주 기준 후보로 쓴다.",
            "- 하지만 모든 후보가 OOS net(표본외 순손익) 약점 표식을 유지하므로 final(최종), ONNX(온닉스), deployment(배포)로 가지 않는다.",
            "- Effect(효과): 다음 작업은 OOS net recovery(표본외 순손익 회복) 하나로 좁혀지고, validation gate(검증 관문)는 보존 조건이 된다.",
        ]
    )
    return "\n".join(lines)


def decision_md(anchor: Mapping[str, Any]) -> str:
    return f"""# Stage209 Decision(209단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage208_evidence_commit(원천 208단계 근거 커밋): `{SOURCE_STAGE208_EVIDENCE_COMMIT}`
- source_stage208_hash_record_commit(원천 208단계 해시 기록 커밋): `{SOURCE_STAGE208_HASH_RECORD_COMMIT}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', 'none')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage209(209단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage210(210단계)에서 OOS net recovery(표본외 순손익 회복)를 validation gate preservation(검증 관문 보존) 조건으로 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
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
    rows = []
    for path in paths:
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.name}",
                "artifact_type": "stage209_followup_review_evidence",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "Stage209 Stage208 risk-cap interpolation follow-up review evidence.",
            }
        )
    return rows


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
            ("oos_gap_vs_stage171_primary", anchor.get("oos_net_gap_vs_stage171_primary", "")),
            ("hard_quality_pass", anchor.get("hard_quality_pass", "")),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage209_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage209_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "validation_oos_tradeoff_review(검증/표본외 상충 검토)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage209 review-only closeout; not final and not deployment.",
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


def write_packet_files(
    tradeoff_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    anchor: Mapping[str, Any],
) -> None:
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
        f"""# Stage209 Closeout Packet(209단계 종료 작업 묶음)

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

Stage210(210단계)은 Stage209(209단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can `s208_ls_r0305` recover OOS net(표본외 순손익) while preserving Stage208 validation gate(208단계 검증 관문): validation net/PF/midPF above 34D(검증 순손익/수익요인/중반 수익요인 34D 이상) and validation DD below 34D(검증 낙폭 34D 아래)?

Effect(효과): Stage208(208단계)의 검증 통과를 버리지 않고, 아직 약한 OOS net(표본외 순손익)만 좁게 고친다.

## Constraints(제약)

- source_adapter(원천 어댑터): `{anchor.get('adapter_id', 's208_ls_r0305')}`
- preserve validation DD below 34D(검증 낙폭 34D 아래 보존)
- preserve validation net/PF/midPF above 34D(검증 순손익/수익요인/중반 수익요인 34D 이상 보존)
- improve or explain OOS net gap(표본외 순손익 격차 개선 또는 설명)
- keep ATR/bracket and model-risk telemetry(ATR/브래킷 및 모델위험 기록 유지)
- do not start ONNX(ONNX 시작 금지)
- do not claim final package(최종 패키지 주장 금지)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage210 Input References(210단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- source_attribution(원천 성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- source_route_matrix(원천 경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- source_stage208_quality_matrix(원천 208단계 품질 행렬): `{rel(SOURCE_QUALITY_PATH)}`
- source_stage208_risk_atr_telemetry(원천 208단계 위험/ATR 기록): `{rel(SOURCE_RISK_ATR_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage210 Review Index(210단계 검토 색인)

- status(상태): `open_planned_from_stage209`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage210 Selection Status(210단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage209`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(anchor: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage209(209단계) closed(종료) as `{DECISION}` and Stage210(210단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage208(208단계) 검증 통과 후보의 OOS net(표본외 순손익) 약점을 별도 경계 수리로 넘긴다.
- >-
  Stage209 evidence(209단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`에 있다. Effect(효과): risk cap(위험 상한) 성공과 OOS(표본외) 약점을 분리해서 본다.
- >-
  Selected next anchor(선택된 다음 기준 후보)는 `{anchor.get('adapter_id', '')}`이고 target surface(목표 표면)는 `{TARGET_SURFACE}`이다. Effect(효과): legacy 34D(레거시 34D)는 KPI lesson-only target(교훈 전용 핵심 성과 지표 목표)로만 사용한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage209_stage208_risk_cap_interpolation_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage209_stage208_risk_cap_interpolation_followup_review:
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
- status(상태): `stage209_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage209(209단계)는 Stage208(208단계) risk cap interpolation(위험 상한 보간)을 follow-up review(후속 검토)했다. Effect(효과): Stage210(210단계)는 OOS net recovery(표본외 순손익 회복)를 validation gate preservation(검증 관문 보존) 조건으로 좁게 진행한다.

## Latest Stage209 Evidence(최신 209단계 근거)

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
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage209 Selection Status(209단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage209 Review Index(209단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- selected_next_anchor(선택된 다음 기준 후보): `{anchor.get('adapter_id', '')}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog(anchor: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage209 Stage208 risk cap interpolation follow-up review closeout(209단계 208단계 위험 상한 보간 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): selected(선택) `{anchor.get('adapter_id', '')}` as Stage210(210단계) OOS net recovery(표본외 순손익 회복) anchor(기준 후보).\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    kpi_rows = read_csv(SOURCE_KPI_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows, kpi_rows, segment_rows, risk_rows)
    anchor = select_anchor(tradeoff_rows)
    attribution_rows = build_attribution_rows(tradeoff_rows, anchor)
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
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "selected_next_anchor": anchor.get("adapter_id", ""),
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

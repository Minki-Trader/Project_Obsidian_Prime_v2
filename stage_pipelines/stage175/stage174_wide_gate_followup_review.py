from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
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

STAGE_ID = "175_adapter_research__stage174_wide_gate_followup_review"
RUN_ID = "run175A_stage175_stage174_wide_gate_followup_review_v1"
PACKET_ID = "stage175_stage174_wide_gate_followup_review_v1"
PARENT_RUN_ID = "run174A_stage174_wide_gate_mid_segment_recovery_repair_v1"
SOURCE_STAGE_ID = "174_adapter_research__wide_gate_mid_segment_recovery_repair"
SOURCE_RUN_ID = "run174A_stage174_wide_gate_mid_segment_recovery_repair_v1"
SOURCE_STAGE174_CLOSEOUT_COMMIT = "7918c76576c0a1246ca3561f1bcf347baed89f90"
SOURCE_STAGE174_HASH_RECORD_COMMIT = "51bdd138407a1bfe99105259d7ba8dc3346c41e0"
NEXT_STAGE_ID = "176_adapter_research__tp45_dd_midpf_repair"
NEXT_RUN_ID = "run176A_stage176_tp45_dd_midpf_repair_v1"
NEXT_PACKET_ID = "stage176_tp45_dd_midpf_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage174_mt5_reports_completed"
DECISION = "open_stage176_tp45_dd_midpf_repair_candidate_not_final"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE174_REPORT = Path("stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_wide_gate_mid_segment_recovery_report.md")
SOURCE_STAGE174_QUALITY = Path("stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_quality_matrix.csv")
SOURCE_STAGE174_BALANCE = Path("stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_balance_curve_audit.csv")
SOURCE_STAGE174_SEGMENT = Path("stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_segment_kpi_summary.csv")
SOURCE_STAGE174_RISK_ATR = Path("stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_risk_atr_telemetry.csv")
SOURCE_STAGE174_DECISION = Path("stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage175_stage174_wide_gate_followup_review.md"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage175_route_matrix.csv"
LESSON_MATRIX_PATH = REVIEWS_ROOT / "stage175_stage174_lesson_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage175_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage175/stage174_wide_gate_followup_review.py")
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
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def load_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = row.get(key, default)
        if value in (None, ""):
            return default
        return float(str(value).replace(",", "").replace("%", ""))
    except (TypeError, ValueError):
        return default


def quality_flag(row: Mapping[str, Any]) -> str:
    return str(row.get("quality_flags", ""))


def clue_type(adapter_id: str) -> str:
    if "tp45" in adapter_id:
        return "primary_tp45_net_pf_clue"
    if "midwide" in adapter_id:
        return "secondary_midwide_trade_supply_clue"
    if "risk0380" in adapter_id:
        return "risk_recapture_negative_memory"
    return "wide_original_stop_negative_memory"


def lesson_text(row: Mapping[str, Any]) -> str:
    adapter_id = str(row.get("adapter_id", ""))
    if "tp45" in adapter_id:
        return "TP 4.5(익절 4.5)는 validation PF/net(검증 수익요인/순손익)을 회복하고 late share(후반 비중)를 낮췄지만, DD(낙폭), mid PF(중반 수익요인), OOS DD(표본외 낙폭)는 아직 실패다."
    if "midwide" in adapter_id:
        return "Midwide gate(중간 폭 제한문)는 validation PF/net(검증 수익요인/순손익)과 OOS DD(표본외 낙폭)를 좋게 했지만, validation DD(검증 낙폭)와 late concentration(후반 집중도)를 악화했다."
    if "risk0380" in adapter_id:
        return "Risk 3.8 percent(위험 3.8퍼센트)는 validation PF/net(검증 수익요인/순손익)을 충분히 고치지 못했고 DD(낙폭)를 키웠다."
    return "Original SL 2.075(기존 손절 2.075)와 wide gate(넓은 제한문)는 Stage172 SL 1.95(172단계 손절 1.95)보다 나아졌지만 34D net/PF/DD(34D 순손익/수익요인/낙폭)에는 아직 못 미친다."


def build_lesson_rows(quality_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        val_net = as_float(row, "validation_net")
        val_dd = as_float(row, "validation_balance_dd_percent")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "clue_type": clue_type(str(row.get("adapter_id", ""))),
                "validation_pf": as_float(row, "validation_pf"),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_balance_dd_percent": val_dd,
                "validation_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - val_dd,
                "validation_mid_pf": as_float(row, "validation_mid_pf"),
                "validation_late_share": as_float(row, "validation_late_net_share"),
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_balance_dd_percent": as_float(row, "oos_balance_dd_percent"),
                "hard_quality_pass": str(row.get("hard_quality_pass", "")).lower() == "true",
                "quality_flags": quality_flag(row),
                "lesson": lesson_text(row),
            }
        )
    return rows


def build_route_rows(lesson_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    tp45 = next((row for row in lesson_rows if row.get("clue_type") == "primary_tp45_net_pf_clue"), {})
    midwide = next((row for row in lesson_rows if row.get("clue_type") == "secondary_midwide_trade_supply_clue"), {})
    return [
        {
            "run_id": RUN_ID,
            "route": "stage176_primary",
            "decision": DECISION,
            "source_clue": tp45.get("adapter_id", ""),
            "repair_question": "Can TP 4.5(익절 4.5) keep validation PF/net(검증 수익요인/순손익) above 34D(34D) while reducing validation DD(검증 낙폭), OOS DD(표본외 낙폭), and mid PF weakness(중반 수익요인 약점)?",
            "why": "TP 4.5(익절 4.5)는 Stage174(174단계)에서 validation PF/net(검증 수익요인/순손익)이 34D(34D)를 넘고 late share(후반 비중)가 50 percent(50퍼센트) 아래인 첫 단서다.",
            "guardrails": "no legacy method inheritance(레거시 방식 상속 없음); no date-specific filter(날짜 전용 필터 없음); keep v2 source model(v2 원천 모델 유지) unless Stage176(176단계) fails(실패).",
        },
        {
            "run_id": RUN_ID,
            "route": "stage176_supporting_comparison",
            "decision": DECISION,
            "source_clue": midwide.get("adapter_id", ""),
            "repair_question": "Use midwide(중간 폭) only as a contrast(대조군) for trade supply(거래 공급) and OOS DD behavior(표본외 낙폭 행동).",
            "why": "Midwide(중간 폭)는 OOS DD(표본외 낙폭)를 개선했지만 validation DD(검증 낙폭)와 late concentration(후반 집중도)를 악화했다.",
            "guardrails": "do not treat validation net(검증 순손익) alone as sufficient(충분 조건).",
        },
    ]


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | lesson(교훈) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {validation_pf:.6f} | {validation_net:.2f} | {validation_balance_dd_percent:.4f} | {validation_mid_pf:.6f} | {validation_late_share:.4f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_balance_dd_percent:.4f} | {lesson} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> str:
    primary = next((row for row in lesson_rows if row.get("clue_type") == "primary_tp45_net_pf_clue"), {})
    return f"""# Stage175 Stage174 Wide Gate Follow-up Review(175단계 174단계 넓은 제한문 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Result Subject(결과 대상)

Stage174(174단계)의 wide gate(넓은 제한문), TP(익절), SL(손절), risk cap(위험 상한) 변형을 판독했다. Effect(효과): Stage176(176단계)는 가장 좋은 단서만 좁게 이어받는다.

## Evidence Available(사용 가능한 근거)

- source_report(원천 보고서): `{rel(SOURCE_STAGE174_REPORT)}`
- quality_matrix(품질 행렬): `{rel(SOURCE_STAGE174_QUALITY)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(SOURCE_STAGE174_BALANCE)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SOURCE_STAGE174_SEGMENT)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(SOURCE_STAGE174_RISK_ATR)}`

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(lesson_rows)}

## Judgment(판정)

- judgment_label(판정 라벨): `exploratory(탐색)`
- primary_clue(주 단서): `{primary.get("adapter_id", "none")}`
- why(이유): TP 4.5(익절 4.5)는 validation PF/net(검증 수익요인/순손익)을 34D(34D) 위로 올리고 late share(후반 비중)를 낮췄지만, validation DD(검증 낙폭), validation mid PF(검증 중반 수익요인), OOS DD(표본외 낙폭)가 아직 실패다.
- claim_boundary(주장 경계): research/development only(연구개발 전용). Deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 아니다.
- next_condition(다음 조건): Stage176(176단계)에서 TP 4.5(익절 4.5)의 net/PF(순손익/수익요인)를 보존하면서 DD(낙폭), mid PF(중반 수익요인), OOS DD(표본외 낙폭)를 좁게 수리해야 한다.

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
"""


def decision_markdown() -> str:
    return f"""# Stage175 Decision(175단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage174_closeout_commit(원천 174단계 종료 커밋): `{SOURCE_STAGE174_CLOSEOUT_COMMIT}`
- source_stage174_hash_record_commit(원천 174단계 해시 기록 커밋): `{SOURCE_STAGE174_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage175(175단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage176(176단계)에서 TP45(익절 4.5) 단서의 DD/mid PF/OOS DD(낙폭/중반 수익요인/표본외 낙폭)를 수리한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    for path in (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, ROUTE_MATRIX_PATH, LESSON_MATRIX_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage175_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage175 follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    primary = next((row for row in lesson_rows if row.get("clue_type") == "primary_tp45_net_pf_clue"), {})
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage175_stage174_wide_gate_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage174_closeout_commit", SOURCE_STAGE174_CLOSEOUT_COMMIT),
                        ("source_stage174_hash_record_commit", SOURCE_STAGE174_HASH_RECORD_COMMIT),
                        ("primary_clue", primary.get("adapter_id", "none")),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage174_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage174_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage174_wide_gate_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("primary_clue", primary.get("adapter_id", "none")),
                    ("validation_pf", primary.get("validation_pf", "")),
                    ("validation_net", primary.get("validation_net", "")),
                    ("validation_dd", primary.get("validation_balance_dd_percent", "")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("claim_boundary", BOUNDARY),
                    ("route_count", len(route_rows)),
                    ("overall_goal_complete", 0),
                )
            ),
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage175 reviewed Stage174 evidence and opened Stage176 bounded repair.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "completed",
        "decision": DECISION,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "lesson_matrix": rel(LESSON_MATRIX_PATH),
        "lesson_rows": list(lesson_rows),
        "route_rows": list(route_rows),
        "ledger_payload": ledger_payload,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage175 Closeout Packet(175단계 종료 작업 묶음)

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
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage176(176단계)는 Stage175(175단계)가 고른 TP45(익절 4.5) 단서를 bounded repair(경계 수정)로 시험한다.

## Bounded Question(경계 질문)

Can TP 4.5(익절 4.5) preserve validation PF/net(검증 수익요인/순손익) above the legacy 34D(레거시 34D) lesson target while repairing validation DD(검증 낙폭), validation mid PF(검증 중반 수익요인), and OOS DD(표본외 낙폭)?

Effect(효과): Stage176(176단계)는 net/PF(순손익/수익요인)를 더 키우는 넓은 사냥이 아니라 DD/mid/OOS 손상만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage176 Inputs(176단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- source_stage174_quality(원천 174단계 품질): `{rel(SOURCE_STAGE174_QUALITY)}`
- source_stage174_balance(원천 174단계 잔고): `{rel(SOURCE_STAGE174_BALANCE)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage176 Review Index(176단계 검토 색인)

- status(상태): `open_planned_from_stage175`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage176 Selection Status(176단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage175`
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
  Stage175(175단계) closed(종료) as `{DECISION}` and Stage176(176단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage174(174단계)의 TP45(익절 4.5) net/PF(순손익/수익요인) 단서를 DD/mid PF/OOS DD(낙폭/중반 수익요인/표본외 낙폭) 수리로 넘긴다.
- >-
  Stage175 evidence(175단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`, `{rel(LESSON_MATRIX_PATH)}`에 있다. Effect(효과): Stage176(176단계)는 손상 축을 좁혀 시작한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage175_stage174_wide_gate_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage175_stage174_wide_gate_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  route_matrix_path: {rel(ROUTE_MATRIX_PATH)}
  lesson_matrix_path: {rel(LESSON_MATRIX_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage176_tp45_dd_midpf_repair_surface`
- status(상태): `stage175_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage175(175단계)는 Stage174(174단계)의 KPI(핵심 성과 지표)를 follow-up review(후속 검토)로 판독했다. Effect(효과): TP45(익절 4.5) 단서는 살리고 DD/mid PF/OOS DD(낙폭/중반 수익요인/표본외 낙폭) 손상은 Stage176(176단계)에서 좁게 수리한다.

## Latest Stage175 Evidence(최신 175단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage175 Selection Status(175단계 선택 상태)

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
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage175 Review Index(175단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage175 Stage174 wide gate follow-up review closeout(175단계 174단계 넓은 제한문 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): TP45(익절 4.5) 단서를 Stage176(176단계) DD/mid PF/OOS DD(낙폭/중반 수익요인/표본외 낙폭) 수리로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = load_csv(SOURCE_STAGE174_QUALITY)
    lesson_rows = build_lesson_rows(quality_rows)
    route_rows = build_route_rows(lesson_rows)
    write_csv(LESSON_MATRIX_PATH, lesson_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_md(REPORT_PATH, report_markdown(lesson_rows, route_rows))
    write_md(DECISION_PATH, decision_markdown())
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(lesson_rows, route_rows, artifacts)
    write_packet_files(lesson_rows, route_rows, ledger_payload)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "external_verification_status": EXTERNAL_STATUS,
                    "report": rel(REPORT_PATH),
                    "route_matrix": rel(ROUTE_MATRIX_PATH),
                    "lesson_matrix": rel(LESSON_MATRIX_PATH),
                    "overall_goal_complete": False,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

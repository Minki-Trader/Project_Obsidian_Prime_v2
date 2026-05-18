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

STAGE_ID = "179_adapter_research__stage178_risk_compression_followup_review"
RUN_ID = "run179A_stage179_stage178_risk_compression_followup_review_v1"
PACKET_ID = "stage179_stage178_risk_compression_followup_review_v1"
PARENT_RUN_ID = "run178A_stage178_tp45_model_risk_compression_repair_v1"
SOURCE_STAGE_ID = "178_adapter_research__tp45_model_risk_compression_repair"
SOURCE_RUN_ID = "run178A_stage178_tp45_model_risk_compression_repair_v1"
SOURCE_STAGE178_CLOSEOUT_COMMIT = "86794ec917bee816eb58c34e23bb00ef9ff373a7"
SOURCE_STAGE178_HASH_RECORD_COMMIT = "7c7431886dd1938e94e772d3b2ca5a16ca1a5f94"
NEXT_STAGE_ID = "180_adapter_research__tp45_context_lifecycle_dd_repair"
NEXT_RUN_ID = "run180A_stage180_tp45_context_lifecycle_dd_repair_v1"
NEXT_PACKET_ID = "stage180_tp45_context_lifecycle_dd_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage178_mt5_reports_completed"
DECISION = "open_stage180_tp45_context_lifecycle_dd_repair_candidate_not_final"

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

SOURCE_REPORT = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_tp45_model_risk_compression_report.md")
SOURCE_QUALITY = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_quality_matrix.csv")
SOURCE_BALANCE = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_balance_curve_audit.csv")
SOURCE_SEGMENT = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_segment_kpi_summary.csv")
SOURCE_MONTHLY = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_monthly_kpi_summary.csv")
SOURCE_RISK_ATR = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_risk_atr_telemetry.csv")
SOURCE_DECISION = Path("stages/178_adapter_research__tp45_model_risk_compression_repair/03_reviews/stage178_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage179_stage178_risk_compression_followup_review.md"
LESSON_MATRIX_PATH = REVIEWS_ROOT / "stage179_risk_compression_lesson_matrix.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage179_route_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage179_performance_attribution.csv"
DECISION_PATH = REVIEWS_ROOT / "stage179_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage179/stage178_risk_compression_followup_review.py")
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


def source_role(adapter_id: str) -> str:
    if "control_risk0365_c060" in adapter_id:
        return "tp45_control_net_pf_preserved_dd_failed"
    if "cap0285_c060" in adapter_id:
        return "risk_cap_compression_dd_repaired_net_broken"
    if "cap0275_c060" in adapter_id:
        return "stronger_risk_cap_compression_dd_repaired_net_broken"
    if "cap0365_c055" in adapter_id:
        return "confidence_ceiling_net_boost_dd_damage"
    return "unclassified_stage178_variant"


def lesson_text(row: Mapping[str, Any]) -> str:
    role = source_role(str(row.get("adapter_id", "")))
    if role == "tp45_control_net_pf_preserved_dd_failed":
        return "TP45 control(익절 4.5 대조군)은 validation PF/net(검증 수익요인/순손익)을 보존하지만 DD/mid PF/OOS DD(낙폭/중반 수익요인/표본외 낙폭)가 남는다."
    if role == "risk_cap_compression_dd_repaired_net_broken":
        return "Risk cap 0.0285(위험 상한 0.0285)는 DD(낙폭)를 34D(레거시 34D) 아래로 낮추지만 validation net(검증 순손익)을 34D(레거시 34D) 아래로 떨어뜨린다."
    if role == "stronger_risk_cap_compression_dd_repaired_net_broken":
        return "Risk cap 0.0275(위험 상한 0.0275)는 DD(낙폭)를 더 낮추지만 net(순손익) 손상이 더 커진다."
    if role == "confidence_ceiling_net_boost_dd_damage":
        return "Confidence ceiling 0.55(신뢰도 상단 0.55)는 net(순손익)을 키우지만 DD(낙폭)를 크게 악화한다."
    return "Stage178(178단계) 변형은 별도 검토가 필요하다."


def build_lesson_rows(quality_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        val_pf = as_float(row, "validation_pf")
        val_net = as_float(row, "validation_net")
        val_dd = as_float(row, "validation_balance_dd_percent")
        mid_pf = as_float(row, "validation_mid_pf")
        oos_pf = as_float(row, "oos_pf")
        oos_net = as_float(row, "oos_net")
        oos_dd = as_float(row, "oos_balance_dd_percent")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "source_role": source_role(str(row.get("adapter_id", ""))),
                "model_risk_max_pct": as_float(row, "model_risk_max_pct"),
                "validation_pf": val_pf,
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_balance_dd_percent": val_dd,
                "validation_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - val_dd,
                "validation_mid_pf": mid_pf,
                "validation_mid_pf_gap_vs_34d_pf": mid_pf - LEGACY_34D["profit_factor"],
                "validation_late_net_share": as_float(row, "validation_late_net_share"),
                "oos_pf": oos_pf,
                "oos_net": oos_net,
                "oos_balance_dd_percent": oos_dd,
                "oos_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - oos_dd,
                "oos_late_net_share": as_float(row, "oos_late_net_share"),
                "pf_pass": val_pf >= LEGACY_34D["profit_factor"] and oos_pf >= LEGACY_34D["profit_factor"],
                "net_pass": val_net >= LEGACY_34D["net_profit"],
                "dd_pass": val_dd <= LEGACY_34D["max_drawdown_percent"] and oos_dd <= LEGACY_34D["max_drawdown_percent"],
                "mid_pf_pass": mid_pf >= LEGACY_34D["profit_factor"],
                "hard_quality_pass": str(row.get("hard_quality_pass", "")).lower() == "true",
                "quality_flags": str(row.get("quality_flags", "")),
                "lesson": lesson_text(row),
            }
        )
    return rows


def control_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("source_role") == "tp45_control_net_pf_preserved_dd_failed"), {})


def cap_row(rows: Sequence[Mapping[str, Any]], role: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("source_role") == role), {})


def build_attribution_rows(lesson_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    control = control_row(lesson_rows)
    cap0285 = cap_row(lesson_rows, "risk_cap_compression_dd_repaired_net_broken")
    cap0275 = cap_row(lesson_rows, "stronger_risk_cap_compression_dd_repaired_net_broken")
    c055 = cap_row(lesson_rows, "confidence_ceiling_net_boost_dd_damage")
    return [
        {
            "run_id": RUN_ID,
            "finding": "risk_cap_compression_tradeoff(위험 상한 압축 상충)",
            "observed_change": "Risk cap(위험 상한)을 0.0365에서 0.0285/0.0275로 낮추면 validation/OOS DD(검증/표본외 낙폭)는 통과권으로 내려가지만 validation net(검증 순손익)이 34D(레거시 34D) 아래로 내려간다.",
            "comparison": f"control_net={control.get('validation_net','')}; cap0285_net={cap0285.get('validation_net','')}; cap0275_net={cap0275.get('validation_net','')}; control_val_dd={control.get('validation_balance_dd_percent','')}; cap0285_val_dd={cap0285.get('validation_balance_dd_percent','')}; cap0275_val_dd={cap0275.get('validation_balance_dd_percent','')}",
            "likely_driver": "Risk cap(위험 상한) 축소는 trade quality(거래 품질)를 고친 것이 아니라 exposure scale(노출 규모)을 줄인 효과가 크다.",
            "confidence": "high(높음)",
        },
        {
            "run_id": RUN_ID,
            "finding": "confidence_ceiling_tail_damage(신뢰도 상단 꼬리 손상)",
            "observed_change": "Confidence ceiling(신뢰도 상단) 0.55는 validation/OOS net(검증/표본외 순손익)을 키우지만 validation/OOS DD(검증/표본외 낙폭)를 크게 악화한다.",
            "comparison": f"c055_net={c055.get('validation_net','')}; c055_oos_net={c055.get('oos_net','')}; c055_val_dd={c055.get('validation_balance_dd_percent','')}; c055_oos_dd={c055.get('oos_balance_dd_percent','')}",
            "likely_driver": "Higher effective exposure(실효 노출) 또는 risk mapping(위험 매핑)이 profitable windows(수익 구간)와 losing tails(손실 꼬리)를 같이 키운다.",
            "confidence": "medium(중간)",
        },
        {
            "run_id": RUN_ID,
            "finding": "mid_pf_not_risk_scale_problem(중반 수익요인은 위험 규모 문제가 아님)",
            "observed_change": "모든 Stage178(178단계) 변형의 validation mid PF(검증 중반 수익요인)가 34D(레거시 34D) PF(수익요인) 아래에 남는다.",
            "comparison": "; ".join(f"{row.get('adapter_id')} mid_pf={row.get('validation_mid_pf')}" for row in lesson_rows),
            "likely_driver": "Entry context(진입 문맥), lifecycle(생활주기), same-move re-entry(같은 움직임 재진입) 또는 side/regime exposure(방향/국면 노출)를 봐야 한다.",
            "confidence": "medium(중간)",
        },
    ]


def build_route_rows(lesson_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    control = control_row(lesson_rows)
    cap0285 = cap_row(lesson_rows, "risk_cap_compression_dd_repaired_net_broken")
    c055 = cap_row(lesson_rows, "confidence_ceiling_net_boost_dd_damage")
    return [
        {
            "run_id": RUN_ID,
            "route": "stage180_primary",
            "decision": DECISION,
            "source_clue": control.get("adapter_id", ""),
            "repair_question": "Can context/lifecycle repair(문맥/생활주기 수정) reduce DD/mid PF weakness(낙폭/중반 수익요인 약점) while preserving TP45 net/PF(익절 4.5 순손익/수익요인)?",
            "why": "Risk cap compression(위험 상한 압축)은 DD(낙폭)는 고치지만 net(순손익)을 깨므로 단독 해법이 아니다.",
            "guardrails": "keep source model(원천 모델), TP45(익절 4.5), SL2.075(손절 2.075), ATR bracket(ATR 브래킷), model-risk telemetry(모델 위험 기록); adjust only bounded context/lifecycle controls(경계 문맥/생활주기 제어).",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": cap0285.get("adapter_id", ""),
            "repair_question": "Do not continue blunt risk cap cutting(무딘 위험 상한 축소) as the main path.",
            "why": "DD(낙폭) repair is bought by net(순손익) collapse below 34D(레거시 34D).",
            "guardrails": "preserve as risk_atr_damage_observed(위험/ATR 손상 관찰) style evidence, not invalid(무효).",
        },
        {
            "run_id": RUN_ID,
            "route": "non_candidate_high_net",
            "decision": DECISION,
            "source_clue": c055.get("adapter_id", ""),
            "repair_question": "Do not choose high final net(높은 최종 순손익) when DD(낙폭) explodes.",
            "why": "c055(신뢰도 상단 0.55)는 net(순손익)은 강하지만 validation/OOS DD(검증/표본외 낙폭)가 더 나빠진다.",
            "guardrails": "high net(높은 순손익) is not sufficient(충분 조건 아님); segment/DD(구간/낙폭) gates remain active(활성).",
        },
    ]


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | role(역할) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | lesson(교훈) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {source_role} | {validation_pf:.6f} | {validation_net:.2f} | {validation_balance_dd_percent:.4f} | {validation_mid_pf:.6f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_balance_dd_percent:.4f} | {lesson} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(
    lesson_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
) -> str:
    control = control_row(lesson_rows)
    return f"""# Stage179 Stage178 Risk Compression Follow-up Review(179단계 178단계 위험 압축 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Result Subject(결과 대상)

Stage178(178단계)의 model-risk compression(모델 위험 압축) 변형을 판독했다. Effect(효과): Stage180(180단계)는 blunt risk cap cut(무딘 위험 상한 축소)을 반복하지 않고 context/lifecycle(문맥/생활주기) 수정으로 좁혀 간다.

## Evidence Available(사용 가능한 근거)

- source_report(원천 보고서): `{rel(SOURCE_REPORT)}`
- quality_matrix(품질 행렬): `{rel(SOURCE_QUALITY)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(SOURCE_BALANCE)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SOURCE_SEGMENT)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(SOURCE_MONTHLY)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(SOURCE_RISK_ATR)}`

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(lesson_rows)}

## Attribution(귀속)

- risk_cap_tradeoff(위험 상한 상충): `{attribution_rows[0].get("observed_change", "")}`
- confidence_tail_damage(신뢰도 꼬리 손상): `{attribution_rows[1].get("observed_change", "")}`
- mid_pf_problem(중반 수익요인 문제): `{attribution_rows[2].get("observed_change", "")}`

## Judgment(판정)

- judgment_label(판정 라벨): `risk_compression_tradeoff_memory(위험 압축 상충 기억)`
- primary_clue(주 단서): `{control.get("adapter_id", "none")}`
- why(이유): Risk cap compression(위험 상한 압축)은 DD(낙폭)를 줄이지만 net(순손익)을 34D(레거시 34D) 아래로 낮춘다. Confidence ceiling(신뢰도 상단) 조정은 net(순손익)을 키워도 DD(낙폭)를 악화한다.
- claim_boundary(주장 경계): research/development only(연구개발 전용). Deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 아니다.
- next_condition(다음 조건): Stage180(180단계)는 source model(원천 모델), TP45(익절 4.5), SL2.075(손절 2.075), ATR/risk telemetry(ATR/위험 기록)를 보존하고 context/lifecycle DD repair(문맥/생활주기 낙폭 수정)를 좁게 시험해야 한다.

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
"""


def decision_markdown() -> str:
    return f"""# Stage179 Decision(179단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage178_closeout_commit(원천 178단계 종료 커밋): `{SOURCE_STAGE178_CLOSEOUT_COMMIT}`
- source_stage178_hash_record_commit(원천 178단계 해시 기록 커밋): `{SOURCE_STAGE178_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- attribution(귀속): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage179(179단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage180(180단계)에서 TP45(익절 4.5) context/lifecycle DD repair(문맥/생활주기 낙폭 수정)를 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    paths = (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, ROUTE_MATRIX_PATH, LESSON_MATRIX_PATH, ATTRIBUTION_PATH, STAGE_LEDGER_PATH)
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage179_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage179 risk-compression follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(
    lesson_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    control = control_row(lesson_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage179_stage178_risk_compression_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage178_closeout_commit", SOURCE_STAGE178_CLOSEOUT_COMMIT),
                        ("source_stage178_hash_record_commit", SOURCE_STAGE178_HASH_RECORD_COMMIT),
                        ("primary_clue", control.get("adapter_id", "none")),
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
            "ledger_row_id": f"{RUN_ID}__stage178_risk_compression_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage178_risk_compression_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage178_risk_compression_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("primary_clue", control.get("adapter_id", "none")),
                    ("validation_pf", control.get("validation_pf", "")),
                    ("validation_net", control.get("validation_net", "")),
                    ("validation_dd", control.get("validation_balance_dd_percent", "")),
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
            "notes": "Stage179 reviewed Stage178 risk-compression evidence and opened Stage180 context/lifecycle DD repair.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(
    lesson_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
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
        "attribution": rel(ATTRIBUTION_PATH),
        "lesson_rows": list(lesson_rows),
        "route_rows": list(route_rows),
        "attribution_rows": list(attribution_rows),
        "ledger_payload": ledger_payload,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage179 Closeout Packet(179단계 종료 작업 묶음)

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

Stage180(180단계)는 TP45(익절 4.5) control(대조군)의 PF/net(수익요인/순손익) 장점을 보존하면서 context/lifecycle(문맥/생활주기) 수정으로 DD/mid PF/OOS DD(낙폭/중반 수익요인/표본외 낙폭)를 수리할 수 있는지 시험한다.

## Bounded Question(경계 질문)

Can bounded context/lifecycle repair(경계 문맥/생활주기 수정), without changing source model(원천 모델), TP45(익절 4.5), SL2.075(손절 2.075), ATR bracket(ATR 브래킷), and model-risk telemetry(모델 위험 기록), reduce validation DD(검증 낙폭), validation mid PF weakness(검증 중반 수익요인 약점), and OOS DD(표본외 낙폭) while preserving validation PF/net(검증 수익요인/순손익) above legacy 34D KPI(레거시 34D 핵심 성과 지표)?

Effect(효과): Stage180(180단계)는 risk cap cut(위험 상한 축소) 반복을 멈추고, trade selection/lifecycle quality(거래 선택/생활주기 품질) 쪽으로 수리 가설을 좁힌다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage180 Inputs(180단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- attribution(귀속): `{rel(ATTRIBUTION_PATH)}`
- source_stage178_quality(원천 178단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage178_risk_atr(원천 178단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage180 Review Index(180단계 검토 색인)

- status(상태): `open_planned_from_stage179`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage180 Selection Status(180단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage179`
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
  Stage179(179단계) closed(종료) as `{DECISION}` and Stage180(180단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage178(178단계)의 risk cap compression tradeoff(위험 상한 압축 상충)를 보존하고 context/lifecycle DD repair(문맥/생활주기 낙폭 수정)로 넘긴다.
- >-
  Stage179 evidence(179단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`, `{rel(LESSON_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`에 있다. Effect(효과): Stage180(180단계)는 무딘 위험 축소 대신 거래 선택/보유 구조를 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage179_stage178_risk_compression_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage179_stage178_risk_compression_followup_review:
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
  attribution_path: {rel(ATTRIBUTION_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage180_tp45_context_lifecycle_dd_repair_surface`
- status(상태): `stage179_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage179(179단계)는 Stage178(178단계)의 KPI(핵심 성과 지표)를 follow-up review(후속 검토)로 판독했다. Effect(효과): risk cap compression(위험 상한 압축)은 tradeoff memory(상충 기억)로 보존하고, Stage180(180단계)은 context/lifecycle DD repair(문맥/생활주기 낙폭 수정)을 좁게 시험한다.

## Latest Stage179 Evidence(최신 179단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- attribution(귀속): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage179 Selection Status(179단계 선택 상태)

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
        f"""# Stage179 Review Index(179단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- attribution(귀속): `{rel(ATTRIBUTION_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage179 Stage178 risk compression follow-up review closeout(179단계 178단계 위험 압축 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): risk cap compression tradeoff(위험 상한 압축 상충)를 보존하고 Stage180(180단계) context/lifecycle DD repair(문맥/생활주기 낙폭 수정)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = load_csv(SOURCE_QUALITY)
    lesson_rows = build_lesson_rows(quality_rows)
    attribution_rows = build_attribution_rows(lesson_rows)
    route_rows = build_route_rows(lesson_rows)
    write_csv(LESSON_MATRIX_PATH, lesson_rows)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_md(REPORT_PATH, report_markdown(lesson_rows, route_rows, attribution_rows))
    write_md(DECISION_PATH, decision_markdown())
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(lesson_rows, route_rows, artifacts)
    write_packet_files(lesson_rows, route_rows, attribution_rows, ledger_payload)
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
                    "attribution": rel(ATTRIBUTION_PATH),
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

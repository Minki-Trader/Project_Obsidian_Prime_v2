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

STAGE_ID = "181_adapter_research__stage180_context_lifecycle_followup_review"
RUN_ID = "run181A_stage181_stage180_context_lifecycle_followup_review_v1"
PACKET_ID = "stage181_stage180_context_lifecycle_followup_review_v1"
PARENT_RUN_ID = "run180A_stage180_tp45_context_lifecycle_dd_repair_v1"
SOURCE_STAGE_ID = "180_adapter_research__tp45_context_lifecycle_dd_repair"
SOURCE_RUN_ID = "run180A_stage180_tp45_context_lifecycle_dd_repair_v1"
SOURCE_STAGE180_CLOSEOUT_COMMIT = "0fb102c050efad24cc96435a08684516447808a9"
SOURCE_STAGE180_HASH_RECORD_COMMIT = "736f05cb4858ce351e30503fecb0f0f965306835"
NEXT_STAGE_ID = "182_adapter_research__tp45_midwide_risk_balance_repair"
NEXT_RUN_ID = "run182A_stage182_tp45_midwide_risk_balance_repair_v1"
NEXT_PACKET_ID = "stage182_tp45_midwide_risk_balance_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage180_mt5_reports_completed"
DECISION = "open_stage182_tp45_midwide_risk_balance_repair_candidate_not_final"

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

SOURCE_REPORT = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_tp45_context_lifecycle_report.md")
SOURCE_QUALITY = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_quality_matrix.csv")
SOURCE_BALANCE = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_balance_curve_audit.csv")
SOURCE_SEGMENT = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_segment_kpi_summary.csv")
SOURCE_MONTHLY = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_monthly_kpi_summary.csv")
SOURCE_RISK_ATR = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_risk_atr_telemetry.csv")
SOURCE_DECISION = Path("stages/180_adapter_research__tp45_context_lifecycle_dd_repair/03_reviews/stage180_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage181_stage180_context_lifecycle_followup_review.md"
LESSON_MATRIX_PATH = REVIEWS_ROOT / "stage181_context_lifecycle_lesson_matrix.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage181_route_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage181_performance_attribution.csv"
DECISION_PATH = REVIEWS_ROOT / "stage181_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage181/stage180_context_lifecycle_followup_review.py")
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
    if "control" in adapter_id:
        return "control_net_pf_preserved_dd_failed"
    if "cd8" in adapter_id:
        return "cooldown8_net_lift_dd_still_failed"
    if "hold2" in adapter_id:
        return "hold2_dd_fixed_net_destroyed"
    if "midwide" in adapter_id:
        return "midwide_oos_dd_fixed_net_lift_val_dd_failed"
    return "unclassified_stage180_variant"


def lesson_text(row: Mapping[str, Any]) -> str:
    role = source_role(str(row.get("adapter_id", "")))
    if role == "control_net_pf_preserved_dd_failed":
        return "Control(대조군)은 PF/net(수익요인/순손익)을 보존하지만 validation/OOS DD(검증/표본외 낙폭)와 mid PF(중반 수익요인)가 실패한다."
    if role == "cooldown8_net_lift_dd_still_failed":
        return "Cooldown 8(8봉 대기)은 validation net/PF(검증 순손익/수익요인)를 올리지만 DD(낙폭)와 mid PF(중반 수익요인)를 고치지 못한다."
    if role == "hold2_dd_fixed_net_destroyed":
        return "Hold 2(2봉 보유)는 DD(낙폭)를 고치지만 net(순손익)을 크게 깨고 late concentration(후반 집중)을 만든다."
    if role == "midwide_oos_dd_fixed_net_lift_val_dd_failed":
        return "Midwide context(중간넓은 문맥)는 validation net/PF(검증 순손익/수익요인)와 OOS DD(표본외 낙폭)를 개선하지만 validation DD(검증 낙폭)와 mid PF(중반 수익요인)가 남는다."
    return "Stage180(180단계) 변형은 별도 검토가 필요하다."


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
                "validation_pf": val_pf,
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_balance_dd_percent": val_dd,
                "validation_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - val_dd,
                "validation_mid_pf": mid_pf,
                "validation_mid_pf_gap_vs_34d_pf": mid_pf - LEGACY_34D["profit_factor"],
                "oos_pf": oos_pf,
                "oos_net": oos_net,
                "oos_balance_dd_percent": oos_dd,
                "oos_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - oos_dd,
                "quality_flags": str(row.get("quality_flags", "")),
                "hard_quality_pass": str(row.get("hard_quality_pass", "")).lower() == "true",
                "lesson": lesson_text(row),
            }
        )
    return rows


def row_by_role(rows: Sequence[Mapping[str, Any]], role: str) -> Mapping[str, Any]:
    return next((row for row in rows if row.get("source_role") == role), {})


def build_attribution_rows(lesson_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    midwide = row_by_role(lesson_rows, "midwide_oos_dd_fixed_net_lift_val_dd_failed")
    hold2 = row_by_role(lesson_rows, "hold2_dd_fixed_net_destroyed")
    cooldown = row_by_role(lesson_rows, "cooldown8_net_lift_dd_still_failed")
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "Midwide context(중간넓은 문맥)는 OOS DD(표본외 낙폭)를 8.8227로 고치고 validation net(검증 순손익)을 1223.67로 올렸지만 validation DD(검증 낙폭)는 14.8516으로 실패했다.",
            "comparison_baseline": "Stage180 control(180단계 대조군)",
            "likely_drivers": "Context filtering(문맥 필터링)이 OOS tail(표본외 꼬리)을 줄였지만 validation losing cluster(검증 손실 군집)는 아직 남았다.",
            "segment_checks": "validation mid PF(검증 중반 수익요인)는 midwide에서도 1.487087로 34D PF(34D 수익요인) 아래다.",
            "trade_shape": f"midwide_val_net={midwide.get('validation_net','')}; midwide_val_dd={midwide.get('validation_balance_dd_percent','')}; midwide_oos_dd={midwide.get('oos_balance_dd_percent','')}; hold2_val_net={hold2.get('validation_net','')}; cooldown_val_net={cooldown.get('validation_net','')}",
            "alternative_explanations": "Midwide(중간넓은 문맥)의 OOS DD(표본외 낙폭) 개선이 표본별 trade mix(거래 구성) 차이일 수 있어 Stage182(182단계)에서 calibrated risk balance(보정 위험 균형)로 확인한다.",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage182(182단계)는 midwide context(중간넓은 문맥)를 유지하고 risk cap(위험 상한)을 0.0365보다 약간 낮춰 validation DD(검증 낙폭)를 34D 아래로 낮추되 validation net(검증 순손익)을 34D 위에 남길 수 있는지 본다.",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "Hold2(2봉 보유)는 validation/OOS DD(검증/표본외 낙폭)를 통과권으로 낮췄지만 validation net(검증 순손익)을 446.88로 깨뜨렸다.",
            "comparison_baseline": "Stage180 control(180단계 대조군)",
            "likely_drivers": "Max hold(최대 보유) 축소가 손실 체류와 이익 체류를 함께 잘라 MFE capture(최대 유리 이동 포착)를 훼손했다.",
            "segment_checks": "validation mid PF(검증 중반 수익요인) 1.133111은 모든 변형 중 최악이다.",
            "trade_shape": "short hold(짧은 보유)는 DD(낙폭) repair clue(수리 단서)이지만 standalone path(단독 경로)는 아니다.",
            "alternative_explanations": "Net(순손익) 훼손은 exit timing(청산 타이밍) 문제일 수 있다.",
            "attribution_confidence": "high(높음)",
            "next_probe": "Do not repeat blunt hold2(무딘 2봉 보유 반복 금지); keep as failure memory(실패 기억).",
        },
    ]


def build_route_rows(lesson_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    midwide = row_by_role(lesson_rows, "midwide_oos_dd_fixed_net_lift_val_dd_failed")
    hold2 = row_by_role(lesson_rows, "hold2_dd_fixed_net_destroyed")
    return [
        {
            "run_id": RUN_ID,
            "route": "stage182_primary",
            "decision": DECISION,
            "source_clue": midwide.get("adapter_id", ""),
            "repair_question": "Can midwide context(중간넓은 문맥) plus calibrated risk balance(보정 위험 균형) fix validation DD(검증 낙폭) without dropping validation net/PF(검증 순손익/수익요인) below 34D(레거시 34D)?",
            "why": "Midwide(중간넓은 문맥)는 OOS DD(표본외 낙폭)를 고치고 net(순손익) buffer(완충)를 만들었으므로, slight risk balancing(가벼운 위험 균형)이 검증 낙폭만 낮출 가능성이 있다.",
            "guardrails": "do not use blunt risk cap collapse(무딘 위험 상한 붕괴); test small caps only and preserve ATR bracket/model-risk telemetry(ATR 브래킷/모델 위험 기록).",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": hold2.get("adapter_id", ""),
            "repair_question": "Do not continue hold2(2봉 보유) as standalone repair(단독 수정).",
            "why": "DD(낙폭)는 고치지만 net(순손익)과 mid PF(중반 수익요인)를 크게 훼손한다.",
            "guardrails": "preserve as failure_memory(실패 기억), not invalid(무효).",
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
    midwide = row_by_role(lesson_rows, "midwide_oos_dd_fixed_net_lift_val_dd_failed")
    return f"""# Stage181 Stage180 Context Lifecycle Follow-up Review(181단계 180단계 문맥/생활주기 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Result Subject(결과 대상)

Stage180(180단계)의 context/lifecycle DD repair(문맥/생활주기 낙폭 수정) 변형을 판독했다. Effect(효과): Stage182(182단계)는 midwide context(중간넓은 문맥) 단서를 유지하고 calibrated risk balance(보정 위험 균형)만 좁게 본다.

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

- observed_change(관찰 변화): `{attribution_rows[0].get("observed_change", "")}`
- likely_drivers(가능 원인): `{attribution_rows[0].get("likely_drivers", "")}`
- attribution_confidence(귀속 신뢰도): `{attribution_rows[0].get("attribution_confidence", "")}`

## Judgment(판정)

- judgment_label(판정 라벨): `context_lifecycle_tradeoff_memory(문맥/생활주기 상충 기억)`
- primary_clue(주 단서): `{midwide.get("adapter_id", "none")}`
- why(이유): midwide context(중간넓은 문맥)는 validation net/PF(검증 순손익/수익요인)와 OOS DD(표본외 낙폭)를 개선했지만 validation DD(검증 낙폭)와 mid PF(중반 수익요인)는 아직 실패했다.
- claim_boundary(주장 경계): research/development only(연구개발 전용). Deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 아니다.
- next_condition(다음 조건): Stage182(182단계)는 midwide context(중간넓은 문맥)의 net buffer(순손익 완충)를 활용해 small calibrated risk balance(작은 보정 위험 균형)를 시험한다.

## Route Decision(경로 판정)

- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
"""


def decision_markdown() -> str:
    return f"""# Stage181 Decision(181단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage180_closeout_commit(원천 180단계 종료 커밋): `{SOURCE_STAGE180_CLOSEOUT_COMMIT}`
- source_stage180_hash_record_commit(원천 180단계 해시 기록 커밋): `{SOURCE_STAGE180_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- attribution(귀속): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage181(181단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage182(182단계)에서 TP45(익절 4.5) midwide risk balance repair(중간넓은 문맥 위험 균형 수정)를 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    for path in (PRODUCER_PATH, REPORT_PATH, DECISION_PATH, ROUTE_MATRIX_PATH, LESSON_MATRIX_PATH, ATTRIBUTION_PATH, STAGE_LEDGER_PATH):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage181_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage181 context/lifecycle follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    midwide = row_by_role(lesson_rows, "midwide_oos_dd_fixed_net_lift_val_dd_failed")
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage181_stage180_context_lifecycle_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage180_closeout_commit", SOURCE_STAGE180_CLOSEOUT_COMMIT),
                        ("source_stage180_hash_record_commit", SOURCE_STAGE180_HASH_RECORD_COMMIT),
                        ("primary_clue", midwide.get("adapter_id", "none")),
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
            "ledger_row_id": f"{RUN_ID}__stage180_context_lifecycle_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage180_context_lifecycle_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage180_context_lifecycle_followup_review",
            "scoreboard_lane": "regular_risk_execution",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("primary_clue", midwide.get("adapter_id", "none")),
                    ("validation_pf", midwide.get("validation_pf", "")),
                    ("validation_net", midwide.get("validation_net", "")),
                    ("validation_dd", midwide.get("validation_balance_dd_percent", "")),
                    ("oos_dd", midwide.get("oos_balance_dd_percent", "")),
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
            "notes": "Stage181 reviewed Stage180 context/lifecycle evidence and opened Stage182 midwide risk-balance repair.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], attribution_rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
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
        f"""# Stage181 Closeout Packet(181단계 종료 작업 묶음)

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

Stage182(182단계)는 Stage180(180단계)의 midwide context(중간넓은 문맥) 단서를 이어받아, validation DD(검증 낙폭)를 줄이면서 validation PF/net(검증 수익요인/순손익)과 OOS DD(표본외 낙폭)를 보존할 수 있는지 시험한다.

## Bounded Question(경계 질문)

Can calibrated risk balance(보정 위험 균형) on the midwide context(중간넓은 문맥) TP45(익절 4.5) surface reduce validation DD(검증 낙폭) below legacy 34D KPI(레거시 34D 핵심 성과 지표) while keeping validation PF/net(검증 수익요인/순손익) above legacy 34D(레거시 34D), OOS DD(표본외 낙폭) acceptable, and ATR/risk telemetry(ATR/위험 기록) intact?

Effect(효과): Stage182(182단계)는 무딘 risk cap collapse(위험 상한 붕괴)가 아니라, midwide context(중간넓은 문맥)의 net buffer(순손익 완충)를 이용한 작은 위험 균형만 본다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage182 Inputs(182단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- attribution(귀속): `{rel(ATTRIBUTION_PATH)}`
- source_stage180_quality(원천 180단계 품질): `{rel(SOURCE_QUALITY)}`
- source_stage180_risk_atr(원천 180단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage182 Review Index(182단계 검토 색인)

- status(상태): `open_planned_from_stage181`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage182 Selection Status(182단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage181`
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
  Stage181(181단계) closed(종료) as `{DECISION}` and Stage182(182단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage180(180단계)의 midwide context(중간넓은 문맥) 단서를 calibrated risk balance(보정 위험 균형) 수리로 넘긴다.
- >-
  Stage181 evidence(181단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`, `{rel(LESSON_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`에 있다. Effect(효과): Stage182(182단계)는 net buffer(순손익 완충)를 보존하면서 validation DD(검증 낙폭)만 낮출 수 있는지 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage181_stage180_context_lifecycle_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage181_stage180_context_lifecycle_followup_review:
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
- adapter_under_review(검토 중 어댑터): `stage182_tp45_midwide_risk_balance_surface`
- status(상태): `stage181_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage181(181단계)는 Stage180(180단계)의 KPI(핵심 성과 지표)를 follow-up review(후속 검토)로 판독했다. Effect(효과): midwide context(중간넓은 문맥)는 preserved clue(보존 단서)로 남기고, Stage182(182단계)은 calibrated risk balance(보정 위험 균형)를 좁게 시험한다.

## Latest Stage181 Evidence(최신 181단계 근거)

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
        f"""# Stage181 Selection Status(181단계 선택 상태)

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
        f"""# Stage181 Review Index(181단계 검토 색인)

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
        f"\n## {utc_now()} Stage181 Stage180 context lifecycle follow-up review closeout(181단계 180단계 문맥 생활주기 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): midwide context clue(중간넓은 문맥 단서)를 보존하고 Stage182(182단계) calibrated risk balance(보정 위험 균형) 수리로 넘겼다.\n"
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

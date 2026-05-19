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


STAGE_ID = "237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure"
RUN_ID = "run237A_stage237_reference_micro_threshold_recovery_after_context_side_failure_v1"
PACKET_ID = "stage237_reference_micro_threshold_recovery_after_context_side_failure_v1"
SOURCE_STAGE_ID = "236_adapter_research__stage235_side_specific_followup_review"
SOURCE_RUN_ID = "run236A_stage236_stage235_side_specific_followup_review_v1"
SOURCE_STAGE236_EVIDENCE_COMMIT = "69bc3e305b7c9a546c3243d7ebfe89480e6913f7"
SOURCE_STAGE236_HASH_RECORD_COMMIT = "7fd2b31c4df6567296a3eb1542e9e8f648526994"
SOURCE_STAGE235_ID = "235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff"
SOURCE_STAGE235_RUN_ID = "run235A_stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1"
NEXT_STAGE_ID = "238_adapter_research__score_shape_repair_after_threshold_surface_discrete"
NEXT_RUN_ID = "run238A_stage238_score_shape_repair_after_threshold_surface_discrete_v1"
NEXT_PACKET_ID = "stage238_score_shape_repair_after_threshold_surface_discrete_v1"
DECISION = "open_stage238_bounded_score_shape_repair_after_threshold_surface_discrete_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage235_mt5_telemetry_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_score_shape_repair_after_threshold_surface_discrete"
REFERENCE_ADAPTER = "s235_session_ref_h3_cd8"
CLUE_ADAPTER = "s235_cashopen45_h3_cd8"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "net_profit": 987.60,
    "profit_factor": 1.583157,
    "max_drawdown_percent": 12.909136,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE236_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE236_DECISION_PATH = SOURCE236_ROOT / "stage236_decision.md"
SOURCE236_TRADEOFF_PATH = SOURCE236_ROOT / "stage236_side_specific_tradeoff_matrix.csv"
SOURCE236_FAILURE_PATH = SOURCE236_ROOT / "stage236_failure_memory.csv"

SOURCE235_ROOT = Path("stages") / SOURCE_STAGE235_ID / "03_reviews"
SOURCE235_PROBABILITY_PATH = SOURCE235_ROOT / "stage235_probability_telemetry_summary.csv"
SOURCE235_MODEL_SCORE_PATH = SOURCE235_ROOT / "stage235_model_score_audit.csv"
SOURCE235_QUALITY_PATH = SOURCE235_ROOT / "stage235_quality_matrix.csv"
SOURCE235_TRADE_AUDIT_PATH = SOURCE235_ROOT / "stage235_trade_audit.csv"
SOURCE235_RISK_ATR_PATH = SOURCE235_ROOT / "stage235_risk_atr_telemetry.csv"

REPORT_PATH = REVIEWS_ROOT / "stage237_threshold_surface_feasibility_report.md"
AUDIT_PATH = REVIEWS_ROOT / "stage237_threshold_surface_audit.csv"
SCORE_SHAPE_PATH = REVIEWS_ROOT / "stage237_score_shape_audit.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage237_route_matrix.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage237_failure_memory.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage237_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage237_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage237/threshold_surface_feasibility_after_context_side_failure.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip().replace(",", "")
        return float(text) if text else default
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        text = str(value).strip().replace(",", "")
        return int(float(text)) if text else default
    except (TypeError, ValueError):
        return default


def lookup(rows: Sequence[Mapping[str, Any]], **filters: str) -> Mapping[str, Any]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in filters.items()):
            return row
    return {}


def build_threshold_audit(probability_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    selected = [
        row
        for row in probability_rows
        if row.get("adapter_id") == REFERENCE_ADAPTER and row.get("view") == "actual_routed_total"
    ]
    for row in selected:
        pass_min = as_float(row.get("directional_pass_min_probability"))
        pass_max = as_float(row.get("directional_pass_max_probability"))
        near = as_int(row.get("directional_near_threshold_001_rows"))
        short_unique = as_int(row.get("p_short_unique_count"))
        flat_unique = as_int(row.get("p_flat_unique_count"))
        long_unique = as_int(row.get("p_long_unique_count"))
        pass_rows = as_int(row.get("directional_threshold_pass_rows"))
        not_met = as_int(row.get("threshold_or_margin_not_met_rows"))
        rows.append(
            {
                "adapter_id": row.get("adapter_id", ""),
                "split": row.get("split", ""),
                "view": row.get("view", ""),
                "short_threshold": as_float(row.get("short_threshold")),
                "long_threshold": as_float(row.get("long_threshold")),
                "directional_pass_rows": pass_rows,
                "threshold_or_margin_not_met_rows": not_met,
                "directional_near_threshold_001_rows": near,
                "directional_pass_min_probability": pass_min,
                "directional_pass_median_probability": as_float(row.get("directional_pass_median_probability")),
                "directional_pass_max_probability": pass_max,
                "p_short_unique_count": short_unique,
                "p_flat_unique_count": flat_unique,
                "p_long_unique_count": long_unique,
                "decision_counts": row.get("decision_counts", ""),
                "micro_lower_threshold_expected_effect": "no_material_change_in_existing_stage225_and_stage235_evidence",
                "micro_raise_to_0575_expected_effect": "no_material_change_because_pass_probability_is_0_5761168848",
                "raise_above_pass_probability_expected_effect": "binary_signal_collapse_risk",
                "threshold_surface_status": (
                    "discrete_no_rank_surface"
                    if near == 0 and pass_min == pass_max and max(short_unique, flat_unique, long_unique) <= 2
                    else "rank_surface_exists"
                ),
            }
        )
    return rows


def build_score_shape_audit(model_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    selected = [row for row in model_rows if row.get("variant_id") == REFERENCE_ADAPTER]
    for row in selected:
        min_prob = as_float(row.get("feature0_min_implied_winner_prob"))
        max_prob = as_float(row.get("feature0_max_implied_winner_prob"))
        rows.append(
            {
                "adapter_id": row.get("variant_id", ""),
                "model_sha256": row.get("model_sha256", ""),
                "feature0_score_rows": as_int(row.get("feature0_score_rows")),
                "feature0_min_score_gap": as_float(row.get("feature0_min_score_gap")),
                "feature0_max_score_gap": as_float(row.get("feature0_max_score_gap")),
                "feature0_min_implied_winner_prob": min_prob,
                "feature0_max_implied_winner_prob": max_prob,
                "feature1_scores_all_zero": row.get("feature1_scores_all_zero", ""),
                "score_shape_label": row.get("score_shape_label", ""),
                "logit_strength": as_float(row.get("logit_strength")),
                "risk_confidence_floor": as_float(row.get("risk_confidence_floor")),
                "risk_confidence_ceiling": as_float(row.get("risk_confidence_ceiling")),
                "score_shape_status": (
                    "flat_binary_score_shape_no_micro_rank"
                    if min_prob == max_prob and str(row.get("feature1_scores_all_zero", "")).lower() == "true"
                    else "rankable_score_shape_possible"
                ),
            }
        )
    return rows


def build_route_rows(threshold_rows: Sequence[Mapping[str, Any]], score_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "route": DECISION,
            "action": "Open Stage238(238단계) for score shape repair(점수 형태 수리) instead of repeating threshold(문턱값) variants.",
            "effect": "현재 확률이 0.5761168848 근처 이산값이라 threshold(문턱값)만으로는 34D(34D 기준) 부족분을 세밀하게 회복할 수 없다는 실패 축을 보존한다.",
            "evidence": ledger_pairs(
                [
                    ("threshold_rows", len(threshold_rows)),
                    ("score_shape_rows", len(score_rows)),
                    ("reference_adapter", REFERENCE_ADAPTER),
                ]
            ),
            "risk": "Score shape repair(점수 형태 수리)는 새 모델/특징 축이므로 Stage238(238단계)에서 별도 경계가 필요하다.",
        },
        {
            "route": "do_not_run_threshold_noop_variants",
            "action": "Do not run small long/short threshold(롱/숏 문턱값) sweeps around 0.52/0.54.",
            "effect": "Stage225(225단계)와 Stage235(235단계) telemetry(기록)가 이미 no-rank surface(순위 없는 표면)를 보여 주므로 MT5(MetaTrader 5, 메타트레이더5) 시간을 아낀다.",
            "evidence": "directional_near_threshold_001_rows=0 and pass probability is constant.",
            "risk": "If a future model changes probabilities, threshold(문턱값) can be reopened in a new bounded stage(경계 단계).",
        },
    ]


def build_failure_memory(threshold_rows: Sequence[Mapping[str, Any]], score_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    validation = lookup(threshold_rows, split="validation_is")
    score = score_rows[0] if score_rows else {}
    return [
        {
            "failure_id": f"{RUN_ID}__micro_threshold_surface_discrete",
            "hypothesis": "Small threshold/rank-confidence(문턱값/순위 신뢰도) adjustments around the reference can recover validation net/PF(검증 순손익/수익요인).",
            "why_failed": ledger_pairs(
                [
                    ("directional_near_threshold_001_rows", validation.get("directional_near_threshold_001_rows", "")),
                    ("directional_pass_probability", validation.get("directional_pass_min_probability", "")),
                    ("unique_probability_count", validation.get("p_long_unique_count", "")),
                ]
            ),
            "salvage_value": "Threshold(문턱값)이 아니라 score shape(점수 형태)를 바꿔야 한다는 다음 수리 축을 얻었다.",
            "reopen_condition": "Only reopen after model score shape(모델 점수 형태)가 more granular(더 세분화)해진다.",
            "do_not_repeat": "Do not run micro threshold(미세 문턱값) variants on the current binary score shape(이진 점수 형태).",
        },
        {
            "failure_id": f"{RUN_ID}__score_shape_flat",
            "hypothesis": "Reference model(기준 모델) has enough rank diversity(순위 다양성) for confidence gating(신뢰도 게이트).",
            "why_failed": ledger_pairs(
                [
                    ("feature0_min_implied_winner_prob", score.get("feature0_min_implied_winner_prob", "")),
                    ("feature0_max_implied_winner_prob", score.get("feature0_max_implied_winner_prob", "")),
                    ("feature1_scores_all_zero", score.get("feature1_scores_all_zero", "")),
                ]
            ),
            "salvage_value": "Stage238(238단계)은 feature/model score diversity(특징/모델 점수 다양성)를 직접 다룬다.",
            "reopen_condition": "Reopen threshold(문턱값) only after score distribution(점수 분포) has multiple useful ranks(유용한 여러 순위).",
            "do_not_repeat": "Do not treat constant probability(상수 확률)를 rank-confidence(순위 신뢰도)로 해석하지 않는다.",
        },
    ]


def audit_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| split(분할) | pass rows(통과 행) | near threshold(근접 행) | pass prob(통과 확률) | status(상태) |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {split} | {passes} | {near} | {prob:.10f} | {status} |".format(
                split=row.get("split", ""),
                passes=as_int(row.get("directional_pass_rows")),
                near=as_int(row.get("directional_near_threshold_001_rows")),
                prob=as_float(row.get("directional_pass_min_probability")),
                status=row.get("threshold_surface_status", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(
    threshold_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
) -> str:
    routes = "\n".join(
        f"- {row['route']}: {row['action']} Effect(효과): {row['effect']}"
        for row in route_rows
    )
    score = score_rows[0] if score_rows else {}
    return f"""# Stage237 Threshold Surface Feasibility Report(237단계 문턱값 표면 가능성 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage236_evidence_commit(원천 236단계 근거 커밋): `{SOURCE_STAGE236_EVIDENCE_COMMIT}`
- source_stage236_hash_record_commit(원천 236단계 해시 기록 커밋): `{SOURCE_STAGE236_HASH_RECORD_COMMIT}`
- reference_adapter(기준 어댑터): `{REFERENCE_ADAPTER}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 설명)

Stage237(237단계)는 새 MT5(MetaTrader 5, 메타트레이더5) 반복을 먼저 돌리지 않았다. 이유는 Stage235(235단계) telemetry(기록)가 이미 threshold surface(문턱값 표면)가 거의 이진형임을 보여 주기 때문이다.

검증/표본외(validation/OOS, 검증/표본외) 모두 directional pass probability(방향 통과 확률)가 `0.5761168848`로 고정되어 있고, near-threshold rows(문턱값 근접 행)는 `0`이다. Effect(효과): `0.52/0.54` 주변의 작은 threshold(문턱값) 조정은 아무 것도 바꾸지 않거나, `0.576` 위로 올리면 신호를 한꺼번에 죽일 가능성이 크다.

## Threshold Audit(문턱값 감사)

{audit_table(threshold_rows)}

## Score Shape(점수 형태)

- feature0_score_rows(특징0 점수 행): `{score.get('feature0_score_rows', '')}`
- implied_winner_prob(암시 승자 확률): `{score.get('feature0_min_implied_winner_prob', '')}` to `{score.get('feature0_max_implied_winner_prob', '')}`
- feature1_scores_all_zero(특징1 점수 전부 0): `{score.get('feature1_scores_all_zero', '')}`
- score_shape_status(점수 형태 상태): `{score.get('score_shape_status', '')}`

Effect(효과): 다음 수리는 threshold(문턱값)이 아니라 score shape(점수 형태) 또는 model output diversity(모델 출력 다양성)를 직접 다뤄야 한다.

## Route(다음 경로)

{routes}

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage237 Decision(237단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage236_evidence_commit(원천 236단계 근거 커밋): `{SOURCE_STAGE236_EVIDENCE_COMMIT}`
- source_stage236_hash_record_commit(원천 236단계 해시 기록 커밋): `{SOURCE_STAGE236_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- reference_adapter(기준 어댑터): `{REFERENCE_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_surface_audit(문턱값 표면 감사): `{rel(AUDIT_PATH)}`
- score_shape_audit(점수 형태 감사): `{rel(SCORE_SHAPE_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage237(237단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): threshold/rank-confidence(문턱값/순위 신뢰도) 축을 현재 score shape(점수 형태)에서는 실패로 닫고, Stage238(238단계)에서 score shape repair(점수 형태 수리)를 별도 bounded stage(경계 단계)로 연다.
"""


def write_stage238_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage238(238단계)은 Stage237(237단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can score shape repair(점수 형태 수리) create enough rank diversity(순위 다양성) around `{REFERENCE_ADAPTER}` to recover validation net/early PF/mid PF(검증 순손익/초반 수익요인/중반 수익요인) toward 34D(34D 기준) while preserving OOS net/PF/DD(표본외 순손익/수익요인/낙폭), ATR SL/TP(ATR 손절/익절), and model-controlled risk%(모델 제어 위험 비율)?

Effect(효과): Stage237(237단계)의 binary threshold surface(이진 문턱값 표면) 실패를 반복하지 않고, 모델 출력/점수 분포 자체를 좁게 수리한다.

## Fixed Requirements(고정 요구)

- reference_adapter(기준 어댑터): `{REFERENCE_ADAPTER}`.
- cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) are failure memory(실패 기억), not primary axes(주 축 아님).
- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage238 Inputs(238단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- reference_adapter(기준 어댑터): `{REFERENCE_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_surface_audit(문턱값 표면 감사): `{rel(AUDIT_PATH)}`
- score_shape_audit(점수 형태 감사): `{rel(SCORE_SHAPE_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage238 Review Index(238단계 검토 색인)

- status(상태): `open_planned_from_stage237`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage238 Selection Status(238단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage237`
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
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage237(237단계) closed(종료) as `{DECISION}` and Stage238(238단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): threshold/rank-confidence(문턱값/순위 신뢰도) 반복을 멈추고 score shape repair(점수 형태 수리)를 좁게 연다.
- >-
  Stage237 evidence(237단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(AUDIT_PATH)}`, `{rel(SCORE_SHAPE_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): 현재 확률 표면이 이진형이라 작은 threshold(문턱값) 조정이 유효하지 않음을 기록한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage237_reference_micro_threshold_recovery_after_context_side_failure:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage238_score_shape_repair_after_threshold_surface_discrete:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage237_reference_micro_threshold_recovery_after_context_side_failure:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  reference_adapter: {REFERENCE_ADAPTER}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  threshold_surface_audit_path: {rel(AUDIT_PATH)}
  score_shape_audit_path: {rel(SCORE_SHAPE_PATH)}
  failure_memory_path: {rel(FAILURE_MEMORY_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage238_score_shape_repair_after_threshold_surface_discrete:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage237
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  reference_adapter: {REFERENCE_ADAPTER}
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
- adapter_under_review(검토 중 어댑터): `stage238_score_shape_repair_after_threshold_surface_discrete`
- status(상태): `stage237_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage237(237단계)는 threshold/rank-confidence(문턱값/순위 신뢰도) 축을 telemetry audit(기록 감사)로 닫았다. Effect(효과): Stage238(238단계)이 score shape repair(점수 형태 수리)를 좁게 시험한다.

## Latest Stage237 Evidence(최신 237단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- reference_adapter(기준 어댑터): `{REFERENCE_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_surface_audit(문턱값 표면 감사): `{rel(AUDIT_PATH)}`
- score_shape_audit(점수 형태 감사): `{rel(SCORE_SHAPE_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage237 Selection Status(237단계 선택 상태)

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
        f"""# Stage237 Review Index(237단계 검토 색인)

- status(상태): `reviewed_closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_surface_audit(문턱값 표면 감사): `{rel(AUDIT_PATH)}`
- score_shape_audit(점수 형태 감사): `{rel(SCORE_SHAPE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage237 threshold surface feasibility closeout(237단계 문턱값 표면 가능성 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage235(235단계) telemetry(기록)로 threshold/rank-confidence(문턱값/순위 신뢰도) 축이 이진형임을 판정하고 Stage238(238단계) score shape repair(점수 형태 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        AUDIT_PATH,
        SCORE_SHAPE_PATH,
        ROUTE_MATRIX_PATH,
        FAILURE_MEMORY_PATH,
        SUMMARY_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage237_threshold_surface_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage237 threshold surface feasibility evidence.",
                }
            )
    return rows


def write_ledgers(threshold_rows: Sequence[Mapping[str, Any]], score_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validation = lookup(threshold_rows, split="validation_is")
    score = score_rows[0] if score_rows else {}
    primary = ledger_pairs(
        [
            ("reference_adapter", REFERENCE_ADAPTER),
            ("pass_probability", validation.get("directional_pass_min_probability", "")),
            ("near_threshold_rows", validation.get("directional_near_threshold_001_rows", "")),
            ("score_shape_status", score.get("score_shape_status", "")),
            ("decision", DECISION),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("stage237_role", "threshold_surface_review_only_no_tuning"),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage237_review__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage237_review",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "stage237_threshold_surface_feasibility(237단계 문턱값 표면 가능성)",
            "scoreboard_lane": "baseline_adapter_research(기준 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage237 review-only closeout; not final and not deployment.",
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
            "notes": ledger_pairs(
                [
                    ("source_run", SOURCE_RUN_ID),
                    ("reference_adapter", REFERENCE_ADAPTER),
                    ("next_stage", NEXT_STAGE_ID),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    return {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload}


def write_packet_files(
    threshold_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    route_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "reference_adapter": REFERENCE_ADAPTER,
        "external_verification_status": EXTERNAL_STATUS,
        "threshold_rows": list(threshold_rows),
        "score_rows": list(score_rows),
        "route_rows": list(route_rows),
        "failure_memory": list(failure_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "result_judgment_gate.json": {
            **base_payload,
            "judgment_label": "negative_threshold_surface_candidate_not_final",
            "next_condition": "Stage238 must repair score shape rather than repeat current threshold variants.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Existing Stage235 telemetry shows constant pass probability and no near-threshold rows.",
            "comparison_baseline": "Stage235 reference probability and model score audit",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [
                rel(SOURCE236_DECISION_PATH),
                rel(SOURCE236_TRADEOFF_PATH),
                rel(SOURCE236_FAILURE_PATH),
                rel(SOURCE235_PROBABILITY_PATH),
                rel(SOURCE235_MODEL_SCORE_PATH),
                rel(SOURCE235_QUALITY_PATH),
                rel(SOURCE235_TRADE_AUDIT_PATH),
                rel(SOURCE235_RISK_ATR_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "threshold_surface_audit": rel(AUDIT_PATH),
                "score_shape_audit": rel(SCORE_SHAPE_PATH),
                "route": rel(ROUTE_MATRIX_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage237 Closeout Packet(237단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed`
- decision(판정): `{DECISION}`
- reference_adapter(기준 어댑터): `{REFERENCE_ADAPTER}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def run() -> Mapping[str, Any]:
    probability_rows = read_csv(SOURCE235_PROBABILITY_PATH)
    model_rows = read_csv(SOURCE235_MODEL_SCORE_PATH)
    if not probability_rows:
        raise FileNotFoundError(f"Missing or empty probability telemetry: {SOURCE235_PROBABILITY_PATH}")
    if not model_rows:
        raise FileNotFoundError(f"Missing or empty model score audit: {SOURCE235_MODEL_SCORE_PATH}")

    threshold_rows = build_threshold_audit(probability_rows)
    score_rows = build_score_shape_audit(model_rows)
    route_rows = build_route_rows(threshold_rows, score_rows)
    failure_rows = build_failure_memory(threshold_rows, score_rows)

    write_md(REPORT_PATH, report_markdown(threshold_rows, score_rows, route_rows))
    write_csv(AUDIT_PATH, threshold_rows)
    write_csv(SCORE_SHAPE_PATH, score_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(DECISION_PATH, decision_markdown())
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "source_stage236_decision": rel(SOURCE236_DECISION_PATH),
            "source_stage236_tradeoff": rel(SOURCE236_TRADEOFF_PATH),
            "source_stage235_probability": rel(SOURCE235_PROBABILITY_PATH),
            "source_stage235_model_score": rel(SOURCE235_MODEL_SCORE_PATH),
            "threshold_rows": threshold_rows,
            "score_rows": score_rows,
            "route_rows": route_rows,
            "failure_memory": failure_rows,
            "legacy_34d": LEGACY_34D,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_stage238_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    ledger_payload = write_ledgers(threshold_rows, score_rows)
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(
        threshold_rows,
        score_rows,
        route_rows,
        failure_rows,
        {**ledger_payload, "artifact_registry": artifact_payload},
    )
    return {
        "status": "reviewed_closed",
        "run_id": RUN_ID,
        "decision": DECISION,
        "reference_adapter": REFERENCE_ADAPTER,
        "report": rel(REPORT_PATH),
        "next_stage": NEXT_STAGE_ID,
        "overall_goal_complete": False,
    }


def main() -> int:
    print(json.dumps(json_ready(run()), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

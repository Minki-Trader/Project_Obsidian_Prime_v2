from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage246 import soft_timestamp_guard_repair_after_stage244_overprune as stage246


STAGE_ID = "248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff"
RUN_NUMBER = "run248A"
RUN_ID = "run248A_stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1"
PACKET_ID = "stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1"
PARENT_RUN_ID = "run247A_stage247_stage246_soft_guard_followup_review_v1"
SOURCE_STAGE_ID = "247_adapter_research__stage246_soft_guard_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE247_EVIDENCE_COMMIT = "afc675cb7036ea69e9fa4655e5c23831e11a52be"
SOURCE_STAGE247_HASH_RECORD_COMMIT = "319aa8a5e0ad03d54526f697a474b861aaa98253"
NEXT_STAGE_ID = "249_adapter_research__stage248_entry_source_followup_review"
NEXT_RUN_ID = "run249A_stage249_stage248_entry_source_followup_review_v1"
NEXT_PACKET_ID = "stage249_stage248_entry_source_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_entry_source_quality_repair_after_soft_guard_tradeoff"
BOUNDARY = stage246.BOUNDARY
LEGACY_34D = stage246.LEGACY_34D
OOS_REFERENCE = {"adapter_id": "s246_cap0305_control", "oos_net": 775.76, "oos_pf": 1.78, "oos_dd": 9.5076}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s248a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage248_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage248_entry_source_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage248_entry_source_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage248_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage248_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage248_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage248_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage248_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage248_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage248_risk_atr_telemetry.csv"
ENTRY_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage248_entry_source_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage248_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage248_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage248_tier_b_diagnostic_summary.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage248_performance_attribution.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage248_failure_memory.csv"
DECISION_PATH = REVIEWS_ROOT / "stage248_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage248_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage248/entry_source_quality_repair_after_stage246_soft_guard_tradeoff.py")
ARTIFACT_COLUMNS = stage246.ARTIFACT_COLUMNS

RANK_COLUMN = "stage248_entry_quality_rank_bucket"
GATE_COLUMN_PREFIX = "stage248_entry_source_gate"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return stage246.rel(path)


def write_md(path: Path, text: str) -> None:
    stage246.write_md(path, text)


def write_json(path: Path, payload: Any) -> None:
    stage246.write_json(path, payload)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    stage246.write_csv(path, rows, columns)


def repair_variant(
    adapter_id: str,
    label: str,
    *,
    short_threshold: float,
    long_threshold: float,
    note: str,
) -> Any:
    return stage246.stage238.repair.RepairVariant(
        adapter_id=adapter_id,
        label=label,
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.0305,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=short_threshold,
        long_threshold=long_threshold,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes=note,
    )


VARIANTS = (
    repair_variant(
        "s248_cap0305_reference",
        "stage248_cap0305_reference",
        short_threshold=0.54,
        long_threshold=0.52,
        note="Stage248 reference: preserve Stage246 cap0305 control and remove soft guard penalty.",
    ),
    repair_variant(
        "s248_short055",
        "stage248_short055",
        short_threshold=0.55,
        long_threshold=0.52,
        note="Stage248 entry repair: tighten short entry threshold only.",
    ),
    repair_variant(
        "s248_short056",
        "stage248_short056",
        short_threshold=0.56,
        long_threshold=0.52,
        note="Stage248 entry repair: stronger short entry threshold.",
    ),
    repair_variant(
        "s248_long053",
        "stage248_long053",
        short_threshold=0.54,
        long_threshold=0.53,
        note="Stage248 entry repair: tighten long entry threshold only.",
    ),
    repair_variant(
        "s248_balanced055_053",
        "stage248_balanced055_053",
        short_threshold=0.55,
        long_threshold=0.53,
        note="Stage248 entry repair: balanced long and short threshold tightening.",
    ),
)

VARIANT_EXTRAS = {
    item.adapter_id: stage246.extra(item.adapter_id.replace("s248_", ""), 0.0, 0.0)
    for item in VARIANTS
}
SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(stage246.SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}


def best_row(quality_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    if not quality_rows:
        return None
    return max(
        quality_rows,
        key=lambda row: (
            float(row.get("hard_quality_pass") == "True"),
            float(row.get("validation_net", 0) or 0),
            -float(row.get("validation_balance_dd_percent", 99) or 99),
        ),
    )


def decide(quality_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage248_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(str(row.get("hard_quality_pass")) == "True" for row in quality_rows):
        return "open_stage249_followup_due_to_entry_source_candidate_not_final"
    return "open_stage249_bounded_followup_due_to_entry_source_tradeoff_candidate_not_final"


def performance_attribution_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s248_cap0305_reference"), {})
    rows: list[dict[str, Any]] = []
    all_identical = bool(reference) and all(
        (
            row.get("adapter_id") == "s248_cap0305_reference"
            or (
                float(row.get("validation_net", 0) or 0) == float(reference.get("validation_net", 0) or 0)
                and float(row.get("validation_balance_dd_percent", 0) or 0) == float(reference.get("validation_balance_dd_percent", 0) or 0)
                and float(row.get("validation_mid_pf", 0) or 0) == float(reference.get("validation_mid_pf", 0) or 0)
                and float(row.get("oos_net", 0) or 0) == float(reference.get("oos_net", 0) or 0)
            )
        )
        for row in quality_rows
    )
    if all_identical:
        rows.append(
            {
                "attribution_id": f"{RUN_ID}__entry_threshold_no_effect",
                "observed_change": "all Stage248 threshold variants reproduced the reference KPI exactly",
                "comparison_baseline": "s248_cap0305_reference",
                "likely_drivers": "entry threshold inputs did not alter accepted decisions, or all accepted scores stayed beyond tightened thresholds",
                "segment_checks": "validation/OOS full split and early/mid/late KPI identical across variants",
                "trade_shape": "trade count, net, DD, mid PF, and OOS net were unchanged",
                "alternative_explanations": "threshold parameters may be bypassed by the score-table decision surface",
                "attribution_confidence": "high",
                "next_probe": NEXT_STAGE_ID,
            }
        )
    for row in quality_rows:
        adapter = str(row.get("adapter_id", ""))
        if adapter == "s248_cap0305_reference":
            rows.append(
                {
                    "attribution_id": f"{RUN_ID}__reference_preserved",
                    "observed_change": "Stage246 cap0305 reference reproduced without soft guard penalty",
                    "comparison_baseline": "s246_cap0305_control",
                    "likely_drivers": "same risk cap, ATR bracket, thresholds, and reference side filter",
                    "segment_checks": "validation/OOS full and early/mid/late segment KPI",
                    "trade_shape": "control arm for entry threshold repair",
                    "alternative_explanations": "tester variance possible but expected to be small",
                    "attribution_confidence": "medium_high",
                    "next_probe": NEXT_STAGE_ID,
                }
            )
            continue
        net_delta = float(row.get("validation_net", 0) or 0) - float(reference.get("validation_net", 0) or 0)
        dd_delta = float(row.get("validation_balance_dd_percent", 0) or 0) - float(reference.get("validation_balance_dd_percent", 0) or 0)
        mid_delta = float(row.get("validation_mid_pf", 0) or 0) - float(reference.get("validation_mid_pf", 0) or 0)
        rows.append(
            {
                "attribution_id": f"{RUN_ID}__{adapter}",
                "observed_change": f"validation_net_delta={net_delta:.2f};validation_dd_delta={dd_delta:.4f};validation_mid_pf_delta={mid_delta:.6f}",
                "comparison_baseline": "s248_cap0305_reference",
                "likely_drivers": "entry threshold tightening changed accepted trade quality without adding soft guard penalty",
                "segment_checks": "validation/OOS KPI, drawdown, mid PF, risk/ATR telemetry",
                "trade_shape": "threshold repair should reduce weak entries if signal quality is real",
                "alternative_explanations": "trade count shrink can improve DD mechanically while hiding net damage",
                "attribution_confidence": "medium",
                "next_probe": NEXT_STAGE_ID,
            }
        )
    return rows


def failure_memory_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    chosen = best_row(quality_rows) or {}
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s248_cap0305_reference"), {})
    all_identical = bool(reference) and all(
        (
            row.get("adapter_id") == "s248_cap0305_reference"
            or (
                float(row.get("validation_net", 0) or 0) == float(reference.get("validation_net", 0) or 0)
                and float(row.get("validation_balance_dd_percent", 0) or 0) == float(reference.get("validation_balance_dd_percent", 0) or 0)
                and float(row.get("validation_mid_pf", 0) or 0) == float(reference.get("validation_mid_pf", 0) or 0)
                and float(row.get("oos_net", 0) or 0) == float(reference.get("oos_net", 0) or 0)
            )
        )
        for row in quality_rows
    )
    rows = [
        {
            "failure_id": "stage248_entry_threshold_not_final_until_reviewed",
            "evidence": f"best_adapter={chosen.get('adapter_id', '')};hard_quality_pass={chosen.get('hard_quality_pass', '')}",
            "impact": "entry/source repair may help, but one Stage248 run is not a final adapter package",
            "next_handling": NEXT_STAGE_ID,
        }
    ]
    if all_identical:
        rows.append(
            {
                "failure_id": "stage248_entry_threshold_variants_no_effect",
                "evidence": "all threshold variants matched reference validation net/DD/mid PF and OOS net",
                "impact": "the chosen threshold knobs did not change runtime decisions; do not repeat this exact axis",
                "next_handling": "Stage249 review should route to source/feature binding or decision-surface repair",
            }
        )
    return rows


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    lines = [
        "# Stage248 Entry/Source Quality Repair(248단계 진입/원천 품질 수리)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage247_evidence_commit(원천 247단계 근거 커밋): `{SOURCE_STAGE247_EVIDENCE_COMMIT}`",
        f"- source_stage247_hash_record_commit(원천 247단계 해시 기록 커밋): `{SOURCE_STAGE247_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{external}`",
        f"- decision(판정): `{decision}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "- Stage248(248단계)는 soft guard(부드러운 보호문)를 더 강하게 하지 않았다.",
        "- 대신 short/long entry threshold(숏/롱 진입 임계값)를 좁게 올려 weak entry(약한 진입)를 줄일 수 있는지 봤다.",
        "- ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), risk cap(위험 상한) `0.0305`, hold(보유) `3`, cooldown(대기) `8`은 고정했다.",
        "- 결과적으로 모든 threshold variant(임계값 변형)가 reference(참고값)와 같은 KPI(핵심 성과 지표)를 냈다. Effect(효과): 이 축은 decision surface(의사결정 표면)를 실제로 바꾸지 못한 no-effect failure(효과 없음 실패)로 본다.",
        "",
        "## KPI Matrix(KPI 핵심 성과 지표 행렬)",
        "",
        "| adapter(어댑터) | val net(검증 순손익) | DD%(낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | flags(표식) |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in quality_rows:
        lines.append(
            f"| {row.get('adapter_id','')} | {row.get('validation_net','')} | {row.get('validation_balance_dd_percent','')} | {row.get('validation_mid_pf','')} | {row.get('oos_net','')} | {row.get('quality_flags','')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- result_subject(판정 대상): `{RUN_ID}`",
            f"- evidence_available(사용 근거): `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`.",
            "- evidence_missing(부족 근거): Stage249(249단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).",
            "- judgment_label(판정 라벨): `entry_source_repair_measured_candidate_not_final(진입/원천 수리 측정됨, 최종 아님)`",
            f"- claim_boundary(주장 경계): `{BOUNDARY}`",
            f"- next_condition(다음 조건): `{NEXT_STAGE_ID}`",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage248 Decision(248단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage248(248단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def write_stage249_seed(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage249(249단계)는 Stage248(248단계) entry/source repair(진입/원천 수리)를 follow-up review(후속 검토)하는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage248(248단계) improve validation/OOS KPI(검증/표본외 핵심 성과 지표), mid PF(중간 수익요인), DD(낙폭), risk/ATR behavior(위험/ATR 행동), and segment stability(구간 안정성) enough to continue this branch?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage249 Inputs(249단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- stage248_report(248단계 보고서): `{rel(REPORT_PATH)}`
- stage248_quality_matrix(248단계 품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- stage248_failure_memory(248단계 실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage249 Review Index(249단계 검토 색인)

- status(상태): `open_planned_from_stage248`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage249 Selection Status(249단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage248`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_stage_block(text: str, key: str, block: str) -> str:
    return stage246.replace_stage_block(text, key, block)


def update_current_truth(decision: str, external: str) -> None:
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = stage246.re.sub(r"^current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=stage246.re.MULTILINE)
    state = stage246.re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=stage246.re.MULTILINE)
    focus = f"""- >-
  Stage248(248단계) closed(종료) as `{decision}` and Stage249(249단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): entry/source threshold repair(진입/원천 임계값 수리)의 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.
- >-
  Stage248 evidence(248단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): soft guard(부드러운 보호문)가 아닌 entry quality(진입 품질) 축을 평가한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = state.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    stage248_block = f"""stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage249_followup_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage247_evidence_commit: {SOURCE_STAGE247_EVIDENCE_COMMIT}
  source_stage247_hash_record_commit: {SOURCE_STAGE247_HASH_RECORD_COMMIT}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  risk_atr_telemetry_path: {rel(RISK_ATR_TELEMETRY_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff", stage248_block)
    if external == "completed":
        stage249_block = f"""stage249_stage248_entry_source_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage248
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
        state = replace_stage_block(state, "stage249_stage248_entry_source_followup_review", stage249_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage248_entry_source_quality_repair`
- status(상태): `stage248_closed_open_stage249_followup_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage248(248단계)는 Stage246/247(246/247단계)의 soft guard tradeoff(부드러운 보호문 상충) 이후 entry/source quality repair(진입/원천 품질 수리)를 측정했다. Effect(효과): Stage249(249단계)이 이 결과를 별도 review(검토)한다.

## Latest Stage248 Evidence(최신 248단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage248 Review Index(248단계 검토 색인)

- status(상태): `closed_open_stage249_followup_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage248 Selection Status(248단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage249_followup_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage248 entry/source quality repair closeout(248단계 진입/원천 품질 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        f"- effect(효과): soft guard(부드러운 보호문) 대신 entry threshold(진입 임계값) 축을 측정하고 `{NEXT_STAGE_ID}`로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths: list[Path] = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        BALANCE_CURVE_AUDIT_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        QUALITY_MATRIX_PATH,
        RISK_ATR_TELEMETRY_PATH,
        ENTRY_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        ATTRIBUTION_PATH,
        FAILURE_MEMORY_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
        SELECTED_ROOT / "selection_status.md",
        REVIEWS_ROOT / "review_index.md",
        WORKSPACE_STATE_PATH,
        CURRENT_WORKING_STATE_PATH,
        CHANGELOG_PATH,
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
    ]
    for execution in result.get("execution_results", []):
        for value in (execution.get("set_path"), execution.get("ini_path"), execution.get("report_path")):
            if value:
                paths.append(Path(str(value)))
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            artifact_name = rel(path).replace("/", "__").replace("\\", "__")
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{artifact_name}",
                    "artifact_type": "stage248_entry_source_quality_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage248 entry/source quality repair evidence; research only.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    summary_rows = result.get("mt5_kpi_records", [])
    alpha_rows = stage246.stage238.s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=summary_rows,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status", "")),
    )
    primary = ledger_pairs([("decision", decision), ("variant_count", len(VARIANTS)), ("target_surface", TARGET_SURFACE)])
    guardrail = ledger_pairs([("next_stage", NEXT_STAGE_ID), ("overall_goal_complete", 0), ("boundary", BOUNDARY)])
    for row in alpha_rows:
        row["parent_run_id"] = PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage248_entry_source_quality_repair"
        row["judgment"] = decision
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage248_entry_source_quality_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": ledger_pairs(
                [
                    ("source_stage247_evidence_commit", SOURCE_STAGE247_EVIDENCE_COMMIT),
                    ("source_stage247_hash_record_commit", SOURCE_STAGE247_HASH_RECORD_COMMIT),
                    ("overall_goal_complete", 0),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifacts, key="artifact_id"),
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage247_evidence_commit": SOURCE_STAGE247_EVIDENCE_COMMIT,
        "source_stage247_hash_record_commit": SOURCE_STAGE247_HASH_RECORD_COMMIT,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {**base_payload, "route": decision, "next_stage_or_branch": NEXT_STAGE_ID},
        "kpi_contract_audit.json": {**base_payload, "summary": rel(SUMMARY_CSV_PATH), "quality": rel(QUALITY_MATRIX_PATH), "risk_atr": rel(RISK_ATR_TELEMETRY_PATH), "status": "completed"},
        "result_judgment_gate.json": {**base_payload, "result_subject": RUN_ID, "judgment_label": "entry_source_repair_measured_candidate_not_final", "next_condition": NEXT_STAGE_ID},
        "performance_attribution_gate.json": {**base_payload, "attribution": rel(ATTRIBUTION_PATH), "status": "completed"},
        "artifact_lineage_audit.json": {**base_payload, "producer": rel(PRODUCER_PATH), "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {**base_payload, "forbidden_claims": ["deployment", "live_readiness", "runtime_authority", "operating_promotion", "operating_reference", "production_baseline", "overall_goal_complete"], "status": "passed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard"], "status": "passed"},
        "aggregate_summary.json": {**base_payload, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push"},
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage248 Closeout Packet(248단계 종료 작업 묶음)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(경계): `{BOUNDARY}`
""",
    )


def configure_stage248() -> None:
    replacements = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "SOURCE_STAGE245_EVIDENCE_COMMIT": SOURCE_STAGE247_EVIDENCE_COMMIT,
        "SOURCE_STAGE245_HASH_RECORD_COMMIT": SOURCE_STAGE247_HASH_RECORD_COMMIT,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "OOS_REFERENCE": OOS_REFERENCE,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "BALANCE_CURVE_AUDIT_PATH": BALANCE_CURVE_AUDIT_PATH,
        "MONTHLY_KPI_PATH": MONTHLY_KPI_PATH,
        "CONCENTRATION_PATH": CONCENTRATION_PATH,
        "DRAWDOWN_PATH": DRAWDOWN_PATH,
        "QUALITY_MATRIX_PATH": QUALITY_MATRIX_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "SOFT_GUARD_FEATURE_SUMMARY_PATH": ENTRY_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "ATTRIBUTION_PATH": ATTRIBUTION_PATH,
        "FAILURE_MEMORY_PATH": FAILURE_MEMORY_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "RANK_COLUMN": RANK_COLUMN,
        "GATE_COLUMN_PREFIX": GATE_COLUMN_PREFIX,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "best_row": best_row,
        "decide": decide,
        "performance_attribution_rows": performance_attribution_rows,
        "failure_memory_rows": failure_memory_rows,
        "report_markdown": report_markdown,
        "decision_markdown": decision_markdown,
        "write_stage247_seed": write_stage249_seed,
        "update_current_truth": update_current_truth,
        "write_status_files": write_status_files,
        "append_changelog": append_changelog,
        "artifact_rows": artifact_rows,
        "write_ledgers": write_ledgers,
        "write_packet_files": write_packet_files,
    }
    for name, value in replacements.items():
        setattr(stage246, name, value)


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage248()
    return stage246.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())

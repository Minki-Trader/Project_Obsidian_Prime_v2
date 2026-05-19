from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage258 import short_tight_margin_pf_repair_after_stage256_tradeoff as prev


s250 = prev.s250

STAGE_ID = "260_adapter_research__tight_plus_highedge_pf_oos_recovery_repair"
RUN_NUMBER = "run260A"
RUN_ID = "run260A_stage260_tight_plus_highedge_pf_oos_recovery_repair_v1"
PACKET_ID = "stage260_tight_plus_highedge_pf_oos_recovery_repair_v1"
PARENT_RUN_ID = "run259A_stage259_stage258_short_tight_margin_pf_followup_review_v1"
SOURCE_STAGE_ID = "259_adapter_research__stage258_short_tight_margin_pf_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE258_EVIDENCE_COMMIT = "5dbd67b79c824e3d7049b6f482b8c83b0eda92db"
SOURCE_STAGE258_HASH_RECORD_COMMIT = "7f916e6bae523c45f269eb48c91f6c17e61a55e3"
SOURCE_STAGE259_EVIDENCE_COMMIT = "8d3f6644fa08bb344e7763d9d8e211f045c61f78"
SOURCE_STAGE259_HASH_RECORD_COMMIT = "28cfb566f3ae6633ec04237a307754666f6cde38"
NEXT_STAGE_ID = "261_adapter_research__stage260_tight_plus_highedge_pf_oos_followup_review"
NEXT_RUN_ID = "run261A_stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1"
NEXT_PACKET_ID = "stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_tight_plus_highedge_pf_oos_recovery_repair"
BOUNDARY = s250.BOUNDARY
LEGACY_34D = s250.LEGACY_34D
OOS_REFERENCE = dict(s250.OOS_REFERENCE)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
COMMON_ROOT = f"OPV2/s260a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage260_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage260_source_feature_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage260_tight_plus_highedge_pf_oos_recovery_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage260_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage260_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage260_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage260_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage260_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage260_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage260_risk_atr_telemetry.csv"
FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage260_source_feature_summary.csv"
PROBABILITY_PATH = REVIEWS_ROOT / "stage260_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage260_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage260_tier_b_diagnostic_summary.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage260_performance_attribution.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage260_failure_memory.csv"
DECISION_PATH = REVIEWS_ROOT / "stage260_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage260_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage260/tight_plus_highedge_pf_oos_recovery_repair.py")

SIGNAL_COLUMN = s250.SIGNAL_COLUMN
RANK_COLUMN = "stage260_source_feature_rank_bucket"
GATE_COLUMN_PREFIX = "stage260_source_feature_gate"
SOURCE_SPEC = dict(s250.SOURCE_SPEC)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s250.rel(path)


def repair_variant(adapter_id: str, label: str, note: str) -> Any:
    return s250.stage238.repair.RepairVariant(
        adapter_id=adapter_id,
        label=label,
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.0305,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes=note,
    )


VARIANTS = (
    repair_variant(
        "s260_highedge_control",
        "stage260_highedge_control",
        "Stage260 control: exact Stage258 tight_plus_highedge gate with fixed score surface, thresholds, lifecycle, ATR bracket, and model risk.",
    ),
    repair_variant(
        "s260_lowrank_lowedge_filter",
        "stage260_lowrank_lowedge_filter",
        "Stage260 PF repair: keep tight-plus-high guard and additionally block low-edge short signals only when rank bucket is low.",
    ),
    repair_variant(
        "s260_midlow_lowedge_filter",
        "stage260_midlow_lowedge_filter",
        "Stage260 PF repair: keep tight-plus-high guard and additionally block low-edge short signals when rank bucket is low or mid.",
    ),
    repair_variant(
        "s260_vhigh_highedge_relax",
        "stage260_vhigh_highedge_relax",
        "Stage260 OOS recovery: keep tight guard but allow high-edge short signals only when rank bucket is vhigh.",
    ),
    repair_variant(
        "s260_lowrank_filter_vhigh_relax",
        "stage260_lowrank_filter_vhigh_relax",
        "Stage260 balanced repair: block low-rank low-edge shorts while allowing only vhigh high-edge shorts.",
    ),
)


def _score(short: float, flat: float, long: float) -> tuple[float, float, float]:
    return (float(short), float(flat), float(long))


def source_branch_extra(axis: str, branch_mode: str, description: str) -> dict[str, Any]:
    return {
        "axis": axis,
        "asymmetric_gate": "none",
        "low_penalty": 0.0,
        "mid_penalty": 0.0,
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": branch_mode,
        "source_branch_mode": branch_mode,
        "gate_description": description,
        "side_filter_enabled": True,
        "short_block_rule": "stage260_highedge_pf_oos_recovery_variant",
        "long_block_rule": "stage260_highedge_pf_oos_recovery_variant",
        "rank_scores": {
            "low": _score(0.0, 0.0, 0.0),
            "mid": _score(0.0, 0.0, 0.0),
            "high": _score(0.10, -0.10, 0.10),
            "vhigh": _score(0.15, -0.15, 0.15),
        },
    }


VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s260_highedge_control": source_branch_extra("highedge_control", "highedge_control", "Exact Stage258 tight_plus_highedge: block wide session plus tight and high edge margin band."),
    "s260_lowrank_lowedge_filter": source_branch_extra("lowrank_lowedge_filter", "lowrank_lowedge_filter", "Tight-plus-high guard plus low-rank low-edge block."),
    "s260_midlow_lowedge_filter": source_branch_extra("midlow_lowedge_filter", "midlow_lowedge_filter", "Tight-plus-high guard plus low/mid-rank low-edge block."),
    "s260_vhigh_highedge_relax": source_branch_extra("vhigh_highedge_relax", "vhigh_highedge_relax", "Tight guard plus high-edge relax only for vhigh rank."),
    "s260_lowrank_filter_vhigh_relax": source_branch_extra("lowrank_filter_vhigh_relax", "lowrank_filter_vhigh_relax", "Low-rank low-edge block plus vhigh high-edge relax."),
}
SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}


def hit_range(value: float | None, lower: Any, upper: Any) -> bool:
    return value is not None and float(lower) <= float(value) <= float(upper)


def source_branch_gate_value(row: Mapping[str, str], branch_mode: str) -> float:
    signal = int(round(s250.stage238.parse_float(row.get(SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return 0.0
    minutes = s250.stage238.s174.s167_minutes_for(row)
    margin = s250.stage238.s174.s167_margin_for(row)
    _, bucket_label = s250.stage238.rank_bucket_for(row)
    ref = s250.REFERENCE_EXTRA
    if signal > 0 and hit_range(minutes, ref["session_min"], ref["session_max"]):
        return 2.0
    if signal < 0:
        wide_session = hit_range(minutes, ref["wide_session_min"], ref["wide_session_max"])
        if margin is None:
            low_edge = tight_margin = high_edge = False
        else:
            low_edge = float(ref["wide_margin_min"]) <= margin < float(ref["tight_margin_min"])
            tight_margin = float(ref["tight_margin_min"]) <= margin <= float(ref["tight_margin_max"])
            high_edge = float(ref["tight_margin_max"]) < margin <= float(ref["wide_margin_max"])
        if branch_mode == "lowrank_lowedge_filter":
            short_blocked = wide_session or tight_margin or high_edge or (low_edge and bucket_label == "low")
        elif branch_mode == "midlow_lowedge_filter":
            short_blocked = wide_session or tight_margin or high_edge or (low_edge and bucket_label in {"low", "mid"})
        elif branch_mode == "vhigh_highedge_relax":
            short_blocked = wide_session or tight_margin or (high_edge and bucket_label != "vhigh")
        elif branch_mode == "lowrank_filter_vhigh_relax":
            short_blocked = wide_session or tight_margin or (high_edge and bucket_label != "vhigh") or (low_edge and bucket_label == "low")
        else:
            short_blocked = wide_session or tight_margin or high_edge
        if short_blocked:
            return 1.0
    return 0.0


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, item in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / item.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s250.stage238.s161.base.parse_ini(s250.stage238.s161.base.engine.source_attempt_ini(split, item))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s250.stage238.s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{item.adapter_id}", "ta"),
                    (s250.stage238.s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{item.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 26010000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s250.stage238.s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=260,
                        exploration_label="stage260_BaselineAdapter__TightPlusHighEdgePfOosRecovery",
                        attempt_name=f"{item.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][item.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{item.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][item.adapter_id][split]["common_path"]),
                        feature_count=3,
                        feature_order_hash=inputs["model_exports"][item.adapter_id]["feature_order_hash"],
                        short_threshold=item.short_threshold,
                        long_threshold=item.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=item.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{item.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=item.close_on_flat_signal,
                        reverse_on_opposite_signal=item.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=item.close_only_on_opposite_signal,
                        extra_set_values=s250.extra_set_values(item, magic),
                    )
                )
    return attempts


def decide(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage260_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(prev.hard_quality_pass(row) for row in quality_rows):
        return "open_stage261_bounded_followup_due_to_stage260_34d_candidate_not_final"
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s260_highedge_control"), {})
    best = prev.best_row(quality_rows)
    if best and reference and best.get("adapter_id") != reference.get("adapter_id"):
        if (
            prev.as_float(best, "validation_pf") > prev.as_float(reference, "validation_pf")
            or prev.as_float(best, "validation_mid_pf") > prev.as_float(reference, "validation_mid_pf")
            or prev.as_float(best, "oos_net") > prev.as_float(reference, "oos_net")
            or prev.as_float(best, "oos_pf") > prev.as_float(reference, "oos_pf")
        ):
            return "open_stage261_bounded_followup_due_to_stage260_pf_oos_tradeoff_candidate_not_final"
    return "open_stage261_bounded_followup_due_to_stage260_no_repair_gain_candidate_not_final"


def performance_attribution_rows(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s260_highedge_control"), {})
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = str(row.get("adapter_id", ""))
        rows.append(
            {
                "attribution_id": f"{RUN_ID}__{adapter}",
                "observed_change": (
                    "control_exact_stage258_highedge"
                    if adapter == "s260_highedge_control"
                    else (
                        f"validation_pf_delta={prev.as_float(row, 'validation_pf') - prev.as_float(reference, 'validation_pf'):.4f};"
                        f"validation_mid_pf_delta={prev.as_float(row, 'validation_mid_pf') - prev.as_float(reference, 'validation_mid_pf'):.6f};"
                        f"oos_net_delta={prev.as_float(row, 'oos_net') - prev.as_float(reference, 'oos_net'):.2f};"
                        f"oos_pf_delta={prev.as_float(row, 'oos_pf') - prev.as_float(reference, 'oos_pf'):.4f}"
                    )
                ),
                "comparison_baseline": "s260_highedge_control",
                "likely_drivers": "rank-conditioned low-edge or high-edge short supply changed while score table, thresholds, lifecycle, ATR bracket, and model risk stayed fixed",
                "segment_checks": "validation/OOS, early/mid/late PF, DD, source gate counts, probability telemetry, risk/ATR telemetry",
                "trade_shape": "Stage260 tests whether the Stage258 highedge validation gain can keep low DD while recovering PF and OOS net/PF",
                "alternative_explanations": "small changes can reflect supply shrink or calendar cluster effects rather than durable edge",
                "attribution_confidence": "medium",
                "next_probe": NEXT_STAGE_ID,
            }
        )
    return rows


def failure_memory_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = prev.best_row(quality_rows)
    return [
        {
            "failure_id": f"{RUN_ID}__stage260_not_final_until_followup_review",
            "evidence": f"best_adapter={best.get('adapter_id', '')};hard_quality_pass={prev.hard_quality_pass(best)}",
            "impact": "one bounded PF/OOS source-gate repair does not complete the research package",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__single_axis_boundary",
            "evidence": "Stage260 changes only rank-conditioned source gate behavior around the Stage258 highedge candidate",
            "impact": "prevents Stage260 from becoming broad threshold, lifecycle, model, or ATR/risk over-tuning",
            "next_handling": NEXT_STAGE_ID,
        },
    ]


def quality_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순수익) | DD%(손실폭) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순수익) | pass(통과) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('adapter_id','')} | {row.get('validation_pf','')} | {row.get('validation_net','')} | {row.get('validation_balance_dd_percent','')} | {row.get('validation_mid_pf','')} | {row.get('oos_pf','')} | {row.get('oos_net','')} | {row.get('hard_quality_pass','')} |"
        )
    return "\n".join(lines)


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = prev.best_row(quality_rows)
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s260_highedge_control"), {})
    return f"""# Stage260 Tight Plus High Edge PF/OOS Recovery Repair(260단계 타이트+하이엣지 PF/표본외 회복 수리)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage258_evidence_commit(원천 258단계 근거 커밋): `{SOURCE_STAGE258_EVIDENCE_COMMIT}`
- source_stage258_hash_record_commit(원천 258단계 해시 기록 커밋): `{SOURCE_STAGE258_HASH_RECORD_COMMIT}`
- source_stage259_evidence_commit(원천 259단계 근거 커밋): `{SOURCE_STAGE259_EVIDENCE_COMMIT}`
- source_stage259_hash_record_commit(원천 259단계 해시 기록 커밋): `{SOURCE_STAGE259_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can rank-conditioned source gate repair(순위 조건 소스 차단문 수리) preserve `s258_tight_plus_highedge` validation net/DD(검증 순수익/손실폭) while improving PF/mid PF(수익 팩터/중간 수익 팩터) and OOS net/PF(표본외 순수익/수익 팩터)?

## Design(설계)

- fixed(고정): score table(점수 표면), thresholds(임계값) `0.54/0.52`, lifecycle(생명주기) hold 3/cooldown 8(3봉 보유/8봉 대기), ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험비율) cap(상한) `0.0305`.
- changed(변경): only rank-conditioned low-edge/high-edge short supply(순위 조건 낮은/높은 마진 가장자리 숏 공급).
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

{quality_table(quality_rows)}

## Easy Read(쉬운 해석)

- control(대조군): `{reference.get('adapter_id', '')}` validation PF(검증 수익 팩터) `{reference.get('validation_pf', '')}`, validation net(검증 순수익) `{reference.get('validation_net', '')}`, OOS net(표본외 순수익) `{reference.get('oos_net', '')}`.
- best_read(최선 해석): `{best.get('adapter_id', '')}` validation PF(검증 수익 팩터) `{best.get('validation_pf', '')}`, validation net(검증 순수익) `{best.get('validation_net', '')}`, OOS net(표본외 순수익) `{best.get('oos_net', '')}`.
- final claim(최종 주장)은 금지다. Stage261(261단계)에서 이 결과를 review-only(검토 전용)로 판정해야 한다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage260 Decision(260단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage258_evidence_commit(원천 258단계 근거 커밋): `{SOURCE_STAGE258_EVIDENCE_COMMIT}`
- source_stage258_hash_record_commit(원천 258단계 해시 기록 커밋): `{SOURCE_STAGE258_HASH_RECORD_COMMIT}`
- source_stage259_evidence_commit(원천 259단계 근거 커밋): `{SOURCE_STAGE259_EVIDENCE_COMMIT}`
- source_stage259_hash_record_commit(원천 259단계 해시 기록 커밋): `{SOURCE_STAGE259_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- probability_telemetry(확률 원격측정): `{rel(PROBABILITY_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage260(260단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def write_next_stage_seed(decision: str, external: str) -> None:
    prev.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage261(261단계)는 Stage260(260단계) PF/OOS recovery repair(PF/표본외 회복 수리)를 review-only(검토 전용)로 닫는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage260(260단계) produce a useful v2-native improvement(v2 고유 개선) over `s260_highedge_control`, or should the current highedge branch be repaired differently, demoted, or branched?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    prev.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage261 Input References(261단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_quality_matrix(원천 품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
""",
    )
    prev.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage261 Review Index(261단계 검토 색인)

- status(상태): `open_planned_from_stage260`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
""",
    )
    prev.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage261 Selection Status(261단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage260`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_stage_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.rstrip() + "\n\n" + block


def update_current_truth(decision: str, external: str) -> None:
    state = s250.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-20'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage260(260단계) closed(종료) as `{decision}` and Stage261(261단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): highedge PF/OOS repair(하이엣지 PF/표본외 수리) 결과를 독립 검토로 넘긴다.
- >-
  Stage260 evidence(260단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): 다음 단계가 결과를 final(최종)로 오해하지 않고 KPI(핵심 성과 지표) 약점과 개선을 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 KPI 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    state = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, state, count=1, flags=re.DOTALL)
    stage260_block = f"""stage260_tight_plus_highedge_pf_oos_recovery_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage261_followup_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage258_evidence_commit: {SOURCE_STAGE258_EVIDENCE_COMMIT}
  source_stage258_hash_record_commit: {SOURCE_STAGE258_HASH_RECORD_COMMIT}
  source_stage259_evidence_commit: {SOURCE_STAGE259_EVIDENCE_COMMIT}
  source_stage259_hash_record_commit: {SOURCE_STAGE259_HASH_RECORD_COMMIT}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  probability_telemetry_path: {rel(PROBABILITY_PATH)}
  risk_atr_telemetry_path: {rel(RISK_ATR_TELEMETRY_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    stage261_block = f"""stage261_stage260_tight_plus_highedge_pf_oos_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage260
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage260_tight_plus_highedge_pf_oos_recovery_repair", stage260_block)
    state = replace_stage_block(state, "stage261_stage260_tight_plus_highedge_pf_oos_followup_review", stage261_block)
    s250.io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    prev.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `s260_tight_plus_highedge_pf_oos_recovery`
- status(상태): `stage260_closed_open_stage261_followup_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage260(260단계)는 `s258_tight_plus_highedge` 주변의 PF/OOS recovery(PF/표본외 회복)를 MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외)로 측정했다.
Effect(효과): Stage261(261단계)은 이 결과를 review-only(검토 전용)로 판정한다.

## Latest Stage260 Evidence(최신 260단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    prev.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage260 Review Index(260단계 검토 색인)

- status(상태): `closed_open_stage261_followup_candidate_not_final`
- current_run(현재 실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
""",
    )
    prev.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage260 Selection Status(260단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage261_followup_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = s250.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s250.io_path(CHANGELOG_PATH).exists() else ""
    marker = "Stage260 tight_plus_highedge PF/OOS recovery repair closeout"
    existing = re.sub(rf"\n## [^\n]*{re.escape(marker)}[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    entry = (
        f"\n## {utc_now()} Stage260 tight_plus_highedge PF/OOS recovery repair closeout(260단계 타이트+하이엣지 PF/표본외 회복 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage259가 고른 highedge tradeoff(하이엣지 절충안)를 rank-conditioned source gate(순위 조건 소스 차단문) 축으로 좁게 측정했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    s250.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = prev.base.ORIGINAL_ARTIFACT_ROWS(result)
    for row in rows:
        row["artifact_type"] = "stage260_tight_plus_highedge_pf_oos_recovery_evidence"
        row["notes"] = "Stage260 tight_plus_highedge PF/OOS recovery repair evidence; research only."
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    summary_rows = result.get("mt5_kpi_records", [])
    primary = s250.ledger_pairs([("decision", decision), ("external_status", result.get("external_verification_status", "")), ("variant_count", len(VARIANTS)), ("target_surface", TARGET_SURFACE)])
    guardrail = s250.ledger_pairs([("next_stage", NEXT_STAGE_ID), ("boundary", BOUNDARY), ("overall_goal_complete", 0)])
    alpha_rows = s250.stage238.s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=summary_rows,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status", "")),
    )
    for row in alpha_rows:
        row["parent_run_id"] = PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage260_tight_plus_highedge_pf_oos_recovery"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage260_tight_plus_highedge_pf_oos_recovery",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": s250.ledger_pairs(
                [
                    ("source_stage258_evidence_commit", SOURCE_STAGE258_EVIDENCE_COMMIT),
                    ("source_stage258_hash_record_commit", SOURCE_STAGE258_HASH_RECORD_COMMIT),
                    ("source_stage259_evidence_commit", SOURCE_STAGE259_EVIDENCE_COMMIT),
                    ("source_stage259_hash_record_commit", SOURCE_STAGE259_HASH_RECORD_COMMIT),
                    ("target_surface", TARGET_SURFACE),
                    ("overall_goal_complete", 0),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    return {
        "run_registry": s250.upsert_csv_rows(RUN_REGISTRY_PATH, s250.RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": s250.upsert_csv_rows(PROJECT_LEDGER_PATH, s250.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": s250.upsert_csv_rows(STAGE_LEDGER_PATH, s250.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": s250.upsert_csv_rows(ARTIFACT_REGISTRY_PATH, s250.stage238.ARTIFACT_COLUMNS, artifacts, key="artifact_id"),
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage258_evidence_commit": SOURCE_STAGE258_EVIDENCE_COMMIT,
        "source_stage258_hash_record_commit": SOURCE_STAGE258_HASH_RECORD_COMMIT,
        "source_stage259_evidence_commit": SOURCE_STAGE259_EVIDENCE_COMMIT,
        "source_stage259_hash_record_commit": SOURCE_STAGE259_HASH_RECORD_COMMIT,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    required_gates = ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"]
    files = {
        "routing_receipt.json": {**base_payload, "route": decision, "next_stage_or_branch": NEXT_STAGE_ID, "required_gates": required_gates, "status": "completed"},
        "kpi_contract_audit.json": {**base_payload, "summary": rel(SUMMARY_CSV_PATH), "segments": rel(SEGMENT_KPI_PATH), "risk_atr": rel(RISK_ATR_TELEMETRY_PATH), "probability_telemetry": rel(PROBABILITY_PATH), "status": "completed"},
        "result_judgment_gate.json": {**base_payload, "judgment_label": "pf_oos_repair_measured_candidate_not_final", "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {**base_payload, "attribution": rel(ATTRIBUTION_PATH), "status": "completed"},
        "artifact_lineage_audit.json": {**base_payload, "producer": rel(PRODUCER_PATH), "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {**base_payload, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": required_gates, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {**base_payload, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push"},
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        prev.write_json(PACKET_ROOT / name, payload)
    prev.write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage260 Closeout Packet(260단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{result.get('external_verification_status', '')}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(경계): `{BOUNDARY}`
""",
    )


def patch_prev_module() -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "SOURCE_STAGE256_EVIDENCE_COMMIT": SOURCE_STAGE258_EVIDENCE_COMMIT,
        "SOURCE_STAGE256_HASH_RECORD_COMMIT": SOURCE_STAGE258_HASH_RECORD_COMMIT,
        "SOURCE_STAGE257_EVIDENCE_COMMIT": SOURCE_STAGE259_EVIDENCE_COMMIT,
        "SOURCE_STAGE257_HASH_RECORD_COMMIT": SOURCE_STAGE259_HASH_RECORD_COMMIT,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "COMMON_ROOT": COMMON_ROOT,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
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
        "FEATURE_SUMMARY_PATH": FEATURE_SUMMARY_PATH,
        "PROBABILITY_PATH": PROBABILITY_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "ATTRIBUTION_PATH": ATTRIBUTION_PATH,
        "FAILURE_MEMORY_PATH": FAILURE_MEMORY_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "RUN_REGISTRY_PATH": RUN_REGISTRY_PATH,
        "PROJECT_LEDGER_PATH": PROJECT_LEDGER_PATH,
        "ARTIFACT_REGISTRY_PATH": ARTIFACT_REGISTRY_PATH,
        "WORKSPACE_STATE_PATH": WORKSPACE_STATE_PATH,
        "CURRENT_WORKING_STATE_PATH": CURRENT_WORKING_STATE_PATH,
        "CHANGELOG_PATH": CHANGELOG_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "SIGNAL_COLUMN": SIGNAL_COLUMN,
        "RANK_COLUMN": RANK_COLUMN,
        "GATE_COLUMN_PREFIX": GATE_COLUMN_PREFIX,
        "SOURCE_SPEC": SOURCE_SPEC,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
    }
    for name, value in values.items():
        setattr(prev, name, value)
    prev.source_branch_gate_value = source_branch_gate_value
    prev.build_attempts = build_attempts
    prev.decide = decide
    prev.performance_attribution_rows = performance_attribution_rows
    prev.failure_memory_rows = failure_memory_rows
    prev.quality_table = quality_table
    prev.report_markdown = report_markdown
    prev.decision_markdown = decision_markdown
    prev.write_next_stage_seed = write_next_stage_seed
    prev.update_current_truth = update_current_truth
    prev.write_status_files = write_status_files
    prev.append_changelog = append_changelog
    prev.artifact_rows = artifact_rows
    prev.write_ledgers = write_ledgers
    prev.write_packet_files = write_packet_files


def main(argv: Sequence[str] | None = None) -> int:
    patch_prev_module()
    return prev.main(argv or sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())

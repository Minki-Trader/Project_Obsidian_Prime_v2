from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage217 import oos_preserving_mid_pf_micro_interpolation as s217  # noqa: E402

s213 = s217.s213
s210 = s217.s210
base = s217.base
s192 = s217.s192
s190 = s217.s190
s188 = s217.s188
s184 = s217.s184
s180 = s217.s180
s178 = s217.s178
s176 = s217.s176
s174 = s217.s174
s172 = s217.s172
s161 = s217.s161
repair = s217.repair

STAGE_ID = "219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure"
RUN_NUMBER = "run219A"
RUN_ID = "run219A_stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1"
PACKET_ID = "stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1"
PARENT_RUN_ID = "run218A_stage218_stage217_micro_interpolation_followup_review_v1"
SOURCE_STAGE_ID = "218_adapter_research__stage217_micro_interpolation_followup_review"
SOURCE_RUN_ID = "run218A_stage218_stage217_micro_interpolation_followup_review_v1"
SOURCE_STAGE218_EVIDENCE_COMMIT = "fcc21f1c1d214790490bd6d98305ce8ccf13c413"
SOURCE_STAGE218_HASH_RECORD_COMMIT = "0884c3b3800b2e62a7485559c34a01a6fd7efbed"
SOURCE_STAGE217_BEST_ID = "s217_r031375_s20325_t4615"
NEXT_STAGE_ID = "220_adapter_research__stage219_entry_lifecycle_followup_review"
NEXT_RUN_ID = "run220A_stage220_stage219_entry_lifecycle_followup_review_v1"
NEXT_PACKET_ID = "stage220_stage219_entry_lifecycle_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_entry_lifecycle_repair_after_bracket_axis_failure"
BOUNDARY = s213.BOUNDARY
LEGACY_34D = s213.LEGACY_34D
STAGE171_PRIMARY = s213.STAGE171_PRIMARY
STAGE210_ANCHOR = {
    "adapter_id": "s210_ls_r0315",
    "validation_net": 1200.27,
    "validation_mid_pf": 1.695877099,
    "validation_dd": 12.6726,
    "oos_net": 714.86,
}
STAGE217_BEST = {
    "adapter_id": SOURCE_STAGE217_BEST_ID,
    "validation_net": 952.16,
    "validation_mid_pf": 1.541193855,
    "validation_early_pf": 1.563704148,
    "validation_dd": 12.6953,
    "oos_net": 719.48,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s219a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage219_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage219_entry_lifecycle_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage219_entry_lifecycle_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage219_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage219_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage219_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage219_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage219_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage219_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage219_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage219_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage219_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage219_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage219_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage219_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage219_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage219/entry_lifecycle_repair_after_bracket_axis_failure.py")
ARTIFACT_COLUMNS = s172.ARTIFACT_COLUMNS

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s219_life_control_h3_sd8",
        label="stage219_lifecycle_control_h3_sd8",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage219 control: bracket and lifecycle match the best Stage217 row.",
    ),
    repair.RepairVariant(
        adapter_id="s219_life_h4_sd8",
        label="stage219_lifecycle_hold4_same8",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=4,
        notes="Stage219 lifecycle repair: allow one extra bar of hold with the bracket held constant.",
    ),
    repair.RepairVariant(
        adapter_id="s219_life_h4_sd10",
        label="stage219_lifecycle_hold4_same10",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=10,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=4,
        notes="Stage219 lifecycle repair: hold four bars and reduce same-direction re-entry density.",
    ),
    repair.RepairVariant(
        adapter_id="s219_life_closeonly_h4_sd8",
        label="stage219_lifecycle_closeonly_hold4_same8",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=4,
        notes="Stage219 lifecycle repair: close on opposite signal instead of immediate reversal.",
    ),
)

BASE_EXTRA = {**s213.BASE_EXTRA, "block_mode": "encoded_side_context"}
VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    variant.adapter_id: {
        **BASE_EXTRA,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "axis": variant.adapter_id,
    }
    for variant in VARIANTS
}
MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}


def rel(path: Path | str) -> str:
    return s172.rel(path)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s172.as_float(row, key, default)


def stage_values(context_specs: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_ADAPTER_ID": SOURCE_STAGE217_BEST_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "LEGACY_34D": LEGACY_34D,
        "STAGE171_PRIMARY": STAGE171_PRIMARY,
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
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
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
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "VARIANT_BY_ID": {variant.adapter_id: variant for variant in VARIANTS},
        "SOURCE_SPECS_BY_VARIANT": {variant.adapter_id: dict(s161.s158.LOW_EDGE_SOURCE_SPEC) for variant in VARIANTS},
        "CONTEXT_GATE_SPECS": context_specs,
    }


def apply_stage_values(context_specs: Mapping[str, Any]) -> None:
    values = stage_values(context_specs)
    for module in (s217, s213, s210, s192, s190, base, s188, s184, s180, s178, s176, s174, s172, s161):
        for name, value in values.items():
            setattr(module, name, value)
    s161._CONTEXT_LOOKUP = None


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s161.base.parse_ini(s161.base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 21910000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=219,
                        exploration_label="stage219_BaselineAdapter__EntryLifecycleRepairAfterBracketAxisFailure",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=2,
                        feature_order_hash=inputs["model_exports"][variant.adapter_id]["feature_order_hash"],
                        short_threshold=variant.short_threshold,
                        long_threshold=variant.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=variant.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{variant.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=variant.close_on_flat_signal,
                        reverse_on_opposite_signal=variant.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=variant.close_only_on_opposite_signal,
                        extra_set_values=s172.extra_set_values(variant, magic),
                    )
                )
    return attempts


def configure_runner() -> None:
    context_specs = {}
    for variant in VARIANTS:
        extra = VARIANT_EXTRAS[variant.adapter_id]
        context_specs[variant.adapter_id] = {
            "gate_column": f"stage219_gate_{extra['axis']}",
            "gate_type": "encoded_stage219_entry_lifecycle_repair_gate",
            "block_mode": extra["block_mode"],
            "session_min": float(extra["session_min"]),
            "session_max": float(extra["session_max"]),
            "margin_min": float(extra["margin_min"]),
            "margin_max": float(extra["margin_max"]),
            "pre_min": 90.0,
            "pre_max": 170.0,
            "wide_session_min": float(extra["wide_session_min"]),
            "wide_session_max": float(extra["wide_session_max"]),
            "wide_margin_min": float(extra["wide_margin_min"]),
            "wide_margin_max": float(extra["wide_margin_max"]),
            "tight_session_min": float(extra["tight_session_min"]),
            "tight_session_max": float(extra["tight_session_max"]),
            "tight_margin_min": float(extra["tight_margin_min"]),
            "tight_margin_max": float(extra["tight_margin_max"]),
            "description": "Stage219 encoded gate: bracket held constant while entry/lifecycle settings change.",
        }
    apply_stage_values(context_specs)
    s172.configure_runner = configure_runner
    s172.build_attempts = build_attempts
    s172.gate_value = s210.gate_value
    s161.gate_value = s210.gate_value
    s161.build_attempts = build_attempts
    s161.extra_set_values = s172.extra_set_values
    s161._CONTEXT_LOOKUP = None


def pass_entry_lifecycle(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_mid_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_early_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_net") >= LEGACY_34D["net_profit"]
        and as_float(row, "validation_balance_dd_percent") <= LEGACY_34D["max_drawdown_percent"]
        and as_float(row, "oos_net") >= STAGE210_ANCHOR["oos_net"]
    )


def decide(rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage219_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(pass_entry_lifecycle(row) for row in rows):
        return "open_stage220_stage219_entry_lifecycle_followup_review_candidate_not_final"
    return "open_stage220_bounded_followup_due_to_entry_lifecycle_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            pass_entry_lifecycle(row),
            min(
                as_float(row, "validation_mid_pf") - LEGACY_34D["profit_factor"],
                as_float(row, "validation_early_pf") - LEGACY_34D["profit_factor"],
                as_float(row, "oos_net") - STAGE210_ANCHOR["oos_net"],
            ),
            as_float(row, "validation_net"),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
        ),
    )


def variant_lifecycle(adapter_id: str) -> str:
    variant = {variant.adapter_id: variant for variant in VARIANTS}.get(adapter_id)
    if variant is None:
        return "unknown(미확인)"
    mode = "reverse(반전)" if variant.reverse_on_opposite_signal else "close_only(청산만)"
    return f"hold={variant.max_hold_bars};same_dir_cd={variant.same_direction_reentry_cooldown_bars};{mode}"


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | lifecycle(생애주기) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {life} | {val:.2f} | {early:.6f} | {mid:.6f} | {dd:.4f} | {oos:.2f} | {flags} |".format(
                adapter=row.get("adapter_id", ""),
                life=variant_lifecycle(str(row.get("adapter_id", ""))),
                val=as_float(row, "validation_net"),
                early=as_float(row, "validation_early_pf"),
                mid=as_float(row, "validation_mid_pf"),
                dd=as_float(row, "validation_balance_dd_percent"),
                oos=as_float(row, "oos_net"),
                flags=row.get("quality_flags", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(rows)
    return f"""# Stage219 Entry/Lifecycle Repair Report(219단계 진입/생애주기 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage218_evidence_commit(원천 218단계 근거 커밋): `{SOURCE_STAGE218_EVIDENCE_COMMIT}`
- source_stage218_hash_record_commit(원천 218단계 해시 기록 커밋): `{SOURCE_STAGE218_HASH_RECORD_COMMIT}`
- source_stage217_best(원천 217단계 최선): `{SOURCE_STAGE217_BEST_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Design(경계 설계)

- hypothesis(가설): bracket(브래킷), model risk(모델 위험), threshold(문턱값)를 고정하고 entry/lifecycle(진입/생애주기)만 바꾸면 validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), OOS net(표본외 순손익)의 상충을 줄일 수 있다.
- decision_use(판정 사용처): Stage220(220단계) follow-up review(후속 검토)에서 이 축을 더 밀지, 새 수리 축으로 갈지 정한다.
- comparison_baseline(비교 기준): Stage217 best row(217단계 최선 행) `{SOURCE_STAGE217_BEST_ID}`와 Stage210 anchor(210단계 기준 후보) `{STAGE210_ANCHOR["adapter_id"]}`다.
- control_variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, risk cap(위험 상한) `0.031375`, thresholds(문턱값) `short=0.54,long=0.52`, model/data(모델/데이터), encoded gate(인코딩 게이트)를 고정했다.
- changed_variables(변경 변수): max_hold_bars(최대 보유 봉), same_direction_reentry_cooldown_bars(동일 방향 재진입 대기), reverse/close-only lifecycle(반전/청산 생애주기)만 바꿨다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage219(219단계)을 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(rows)}

## Attribution(성과 원인 분해)

- observed_change(관찰 변화): best adapter(최선 어댑터) `{best.get("adapter_id", "none")}`는 validation net(검증 순손익) `{as_float(best, "validation_net"):.2f}`, early PF(초반 수익요인) `{as_float(best, "validation_early_pf"):.6f}`, mid PF(중반 수익요인) `{as_float(best, "validation_mid_pf"):.6f}`, OOS net(표본외 순손익) `{as_float(best, "oos_net"):.2f}`를 기록했다.
- baseline_gap(기준 차이): Stage217 best(217단계 최선)는 validation net(검증 순손익) `{STAGE217_BEST["validation_net"]}`, early PF(초반 수익요인) `{STAGE217_BEST["validation_early_pf"]}`, mid PF(중반 수익요인) `{STAGE217_BEST["validation_mid_pf"]}`, OOS net(표본외 순손익) `{STAGE217_BEST["oos_net"]}`였다.
- likely_drivers(가능 원인): hold/re-entry/reverse(보유/재진입/반전) 변화가 payoff timing(보상 타이밍)과 same-direction density(동일 방향 밀도)에 영향을 줬다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage220_review(220단계 검토 전 중간)`이다.

## Judgment(판정)

Stage219(219단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage219 Decision(219단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage218_evidence_commit(원천 218단계 근거 커밋): `{SOURCE_STAGE218_EVIDENCE_COMMIT}`
- source_stage218_hash_record_commit(원천 218단계 해시 기록 커밋): `{SOURCE_STAGE218_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 KPI 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage219(219단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage220(220단계) follow-up review(후속 검토)에서 entry/lifecycle repair(진입/생애주기 수리)의 KPI(핵심 성과 지표) 상충을 별도로 판정한다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = s188.artifact_rows(result)
    for row in rows:
        if row.get("artifact_type") != "mt5_strategy_tester_report":
            row["artifact_type"] = "stage219_evidence"
            row["notes"] = "Stage219 entry/lifecycle repair after bracket-axis failure evidence."
        else:
            row["notes"] = "Stage219 MT5 Strategy Tester report."
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = s172.upsert_csv_rows(
        RUN_REGISTRY_PATH,
        s172.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage219_entry_lifecycle_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": s172.ledger_pairs(
                    (
                        ("source_stage218_evidence_commit", SOURCE_STAGE218_EVIDENCE_COMMIT),
                        ("source_stage218_hash_record_commit", SOURCE_STAGE218_HASH_RECORD_COMMIT),
                        ("source_stage217_best", SOURCE_STAGE217_BEST_ID),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only_no_inheritance"),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    if not alpha_rows:
        alpha_rows = [
            {
                "ledger_row_id": f"{RUN_ID}__materialized_or_blocked",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "materialized_or_blocked",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "materialized_or_blocked",
                "tier_scope": "Tier A+B",
                "kpi_scope": "stage219_entry_lifecycle_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage219 materialized or blocked before KPI records were available.",
            }
        ]
    for row in alpha_rows:
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
    return {
        "run_registry": run_payload,
        "alpha_ledger": s172.upsert_csv_rows(PROJECT_LEDGER_PATH, s172.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": s172.upsert_csv_rows(STAGE_LEDGER_PATH, s172.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": s172.upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": status,
        "decision": decision,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "summary_csv": rel(SUMMARY_CSV_PATH),
        "quality_matrix": rel(QUALITY_MATRIX_PATH),
        "segment_kpi": rel(SEGMENT_KPI_PATH),
        "balance_curve_audit": rel(BALANCE_CURVE_AUDIT_PATH),
        "monthly_kpi": rel(MONTHLY_KPI_PATH),
        "concentration_risk": rel(CONCENTRATION_PATH),
        "risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
        "ledger_payload": ledger_payload,
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    s172.write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    s172.write_json(PACKET_ROOT / "packet_receipt.json", payload)
    s172.write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage219 Closeout Packet(219단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{status}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage220(220단계)은 Stage219(219단계) entry/lifecycle repair(진입/생애주기 수리) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage219(219단계) improve validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), OOS net(표본외 순손익), drawdown(낙폭), segment KPI(구간 핵심 성과 지표), concentration risk(집중 위험), and risk/ATR telemetry(위험/ATR 기록) enough to continue this repair axis?

Effect(효과): Stage219(219단계) 안에서 추가 수리를 하지 않고, KPI(핵심 성과 지표) 판정을 별도 review(검토)로 닫는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage220 Inputs(220단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"# Stage220 Review Index(220단계 검토 색인)\n\n- status(상태): `open_planned_from_stage219`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_decision(원천 판정): `{decision}`\n- next_action(다음 행동): `{NEXT_RUN_ID}`\n",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"# Stage220 Selection Status(220단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage219`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{decision}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = s172.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage219(219단계) closed(종료) as `{decision}` and Stage220(220단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): bracket axis(브래킷 축)는 고정하고 entry/lifecycle repair(진입/생애주기 수리)의 KPI(핵심 성과 지표) 상충을 별도 follow-up review(후속 검토)로 판정한다.
- >-
  Stage219 evidence(219단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(MONTHLY_KPI_PATH)}`, `{rel(CONCENTRATION_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): hold/re-entry/reverse(보유/재진입/반전) 변화가 34D(34D 기준) KPI(핵심 성과 지표) 간극을 줄였는지 확인한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage219_entry_lifecycle_repair_after_bracket_axis_failure:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage219_entry_lifecycle_repair_after_bracket_axis_failure:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage217_best: {SOURCE_STAGE217_BEST_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  monthly_kpi_path: {rel(MONTHLY_KPI_PATH)}
  concentration_path: {rel(CONCENTRATION_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}
"""
    s172.io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    s172.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage219_entry_lifecycle_repair`
- status(상태): `stage219_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage219(219단계)는 Stage218(218단계) 판정에 따라 bracket axis(브래킷 축)를 고정하고 entry/lifecycle(진입/생애주기)만 MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정했다. Effect(효과): Stage220(220단계)가 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.

## Latest Stage219 Evidence(최신 219단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    status = f"closed_{decision}" if external == "completed" else "blocked_runtime_incomplete"
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage219 Selection Status(219단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage219 Review Index(219단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 KPI 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = s172.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s172.path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage219 entry/lifecycle repair closeout(219단계 진입/생애주기 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): bracket axis(브래킷 축)를 고정하고 hold/re-entry/reverse(보유/재진입/반전) lifecycle(생애주기)을 MT5(MetaTrader 5, 메타트레이더5)로 측정한 뒤 Stage220(220단계) follow-up review(후속 검토)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    s172.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    configure_runner()
    s161.configure_base()
    args = s161.parse_args(argv or sys.argv[1:])
    inputs = s161.prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 219,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage219_v2_native_entry_lifecycle_repair",
        "feature_set_id": "stage219_signal_plus_encoded_lifecycle_repair_gate",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = s161.base.execute_or_materialize(prepared, args)
    audit_rows = s172.s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s172.s58.risk_rows_from_result(result)
    summary_rows = s172.s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s172.s58.segment_kpi_rows(summary_rows)
    probability_rows = s161.probability_binding_rows(result)
    model_rows = s161.model_score_rows(inputs)
    balance_rows, monthly_rows_, concentration_rows, drawdown_rows = s172.build_curve_audit(summary_rows, segment_rows)
    quality = s172.quality_rows(summary_rows, segment_rows, balance_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality, external)

    s161.write_run_identity(result, probability_rows, model_rows)
    s161.write_csv(AUDIT_CSV_PATH, audit_rows)
    s161.write_csv(SUMMARY_CSV_PATH, summary_rows)
    s161.write_csv(SEGMENT_KPI_PATH, segment_rows)
    s161.write_csv(BALANCE_CURVE_AUDIT_PATH, balance_rows)
    s161.write_csv(MONTHLY_KPI_PATH, monthly_rows_)
    s161.write_csv(CONCENTRATION_PATH, concentration_rows)
    s161.write_csv(DRAWDOWN_PATH, drawdown_rows)
    s161.write_csv(QUALITY_MATRIX_PATH, quality)
    s161.write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    s161.write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    s161.write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    s161.write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    s161.write_csv(TIER_B_DIAGNOSTIC_PATH, s161.tier_b_rows())
    s172.write_md(REPORT_PATH, report_markdown(quality, decision, external))
    s172.write_md(DECISION_PATH, decision_markdown(decision, external))
    s172.write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "balance_rows": balance_rows,
            "monthly_rows": monthly_rows_,
            "concentration_rows": concentration_rows,
            "drawdown_rows": drawdown_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "quality_rows": quality,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "stage210_anchor": STAGE210_ANCHOR,
            "stage217_best": STAGE217_BEST,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "source_stage218_evidence_commit": SOURCE_STAGE218_EVIDENCE_COMMIT,
            "source_stage218_hash_record_commit": SOURCE_STAGE218_HASH_RECORD_COMMIT,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality)
    write_next_stage_seed(decision, external)
    update_current_truth(decision, external)
    write_status_files(decision, external)
    append_changelog(decision)
    print(
        json.dumps(
            s172.json_ready(
                {
                    "status": external,
                    "run_id": RUN_ID,
                    "decision": decision,
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "quality_rows": quality,
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

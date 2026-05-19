from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage198 import bctl_adverse_excursion_dd_guard_repair as s198  # noqa: E402

base = s198.base
s192 = s198.s192
s190 = s198.s190
s188 = s198.s188
s184 = s198.s184
s180 = s198.s180
s178 = s198.s178
s176 = s198.s176
s174 = s198.s174
s172 = s198.s172
s161 = s198.s161
repair = s198.repair

STAGE_ID = "204_adapter_research__selective_probability_margin_recovery_repair"
RUN_NUMBER = "run204A"
RUN_ID = "run204A_stage204_selective_probability_margin_recovery_repair_v1"
PACKET_ID = "stage204_selective_probability_margin_recovery_repair_v1"
PARENT_RUN_ID = "run203A_stage203_stage202_probability_binding_followup_review_v1"
SOURCE_STAGE_ID = "203_adapter_research__stage202_probability_binding_followup_review"
SOURCE_RUN_ID = "run203A_stage203_stage202_probability_binding_followup_review_v1"
SOURCE_STAGE203_EVIDENCE_COMMIT = "e1110b277df623aae687191de84efb58e92c165f"
SOURCE_STAGE203_HASH_RECORD_COMMIT = "ffa719d43d189d784a5e48f6b73637c7b94b07a2"
SOURCE_ADAPTER_ID = "s202_cd8_ref_r0325"
NEXT_STAGE_ID = "205_adapter_research__stage204_selective_probability_margin_followup_review"
NEXT_RUN_ID = "run205A_stage205_stage204_selective_probability_margin_followup_review_v1"
NEXT_PACKET_ID = "stage205_stage204_selective_probability_margin_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_selective_probability_margin_repair"
BOUNDARY = s198.BOUNDARY
LEGACY_34D = s198.LEGACY_34D
STAGE171_PRIMARY = s198.STAGE171_PRIMARY

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s204a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage204_selective_probability_margin_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage204_selective_probability_margin_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage204_selective_probability_margin_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage204_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage204_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage204_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage204_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage204_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage204_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage204_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage204_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage204_selective_probability_margin_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage204_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage204_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage204_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage204_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage204/selective_probability_margin_recovery_repair.py")
ARTIFACT_COLUMNS = s172.ARTIFACT_COLUMNS

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s204_cd8_ref_r0325",
        label="stage204_cd8_ref_r0325",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.75,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage204 reference: Stage202 reference shape with cd8/r0325 and fixed risk/ATR settings.",
    ),
    repair.RepairVariant(
        adapter_id="s204_cd8_long_wide_r0325",
        label="stage204_cd8_long_wide_r0325",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.75,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage204 selective repair: widen only the long-side low-edge gate while preserving short side and thresholds.",
    ),
    repair.RepairVariant(
        adapter_id="s204_cd8_long_tight_r0325",
        label="stage204_cd8_long_tight_r0325",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.75,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage204 selective repair: tighten the long-side low-edge gate as a preservation control.",
    ),
    repair.RepairVariant(
        adapter_id="s204_cd8_long_session_r0325",
        label="stage204_cd8_long_session_r0325",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.75,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage204 selective repair: block only long-side session risk while preserving margin-only longs.",
    ),
)

BASE_EXTRA = {
    "logit_strength": 0.50,
    "risk_confidence_floor": 0.50,
    "risk_confidence_ceiling": 0.60,
    "block_mode": "encoded_side_context",
    "side_filter_enabled": True,
    "session_min": 170.0,
    "session_max": 265.0,
    "margin_min": 0.04,
    "margin_max": 0.0775,
    "wide_session_min": 160.0,
    "wide_session_max": 285.0,
    "wide_margin_min": 0.0375,
    "wide_margin_max": 0.0825,
    "tight_session_min": 190.0,
    "tight_session_max": 245.0,
    "tight_margin_min": 0.0475,
    "tight_margin_max": 0.0700,
}

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s204_cd8_ref_r0325": {
        **BASE_EXTRA,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "lowedge_gate",
        "axis": "ref",
    },
    "s204_cd8_long_wide_r0325": {
        **BASE_EXTRA,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "wide_lowedge",
        "axis": "long_wide",
    },
    "s204_cd8_long_tight_r0325": {
        **BASE_EXTRA,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "tight_lowedge",
        "axis": "long_tight",
    },
    "s204_cd8_long_session_r0325": {
        **BASE_EXTRA,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "axis": "long_session",
    },
}

MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}


def rel(path: Path | str) -> str:
    return s172.rel(path)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s172.as_float(row, key, default)


def install_stage_values(context_specs: Mapping[str, Any]) -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
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
    for module in (s192, s190, base, s188, s184, s180, s178, s176, s174, s172, s161):
        for name, value in values.items():
            setattr(module, name, value)


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
                magic = 20410000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=204,
                        exploration_label="stage204_BaselineAdapter__SelectiveProbabilityMarginRecoveryRepair",
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


def bounded_lowedge_hit(row: Mapping[str, str], spec: Mapping[str, Any], prefix: str, *, use_session: bool = True, use_margin: bool = True) -> bool:
    minutes = s174.s167_minutes_for(row)
    margin = s174.s167_margin_for(row)
    session_hit = False
    margin_hit = False
    key_prefix = f"{prefix}_" if prefix else ""
    if use_session:
        session_hit = minutes is not None and float(spec[f"{key_prefix}session_min"]) <= minutes <= float(spec[f"{key_prefix}session_max"])
    if use_margin:
        margin_hit = float(spec[f"{key_prefix}margin_min"]) <= margin <= float(spec[f"{key_prefix}margin_max"])
    return session_hit or margin_hit


def gate_value(row: Mapping[str, str], variant: repair.RepairVariant) -> float:
    signal = int(round(s172.parse_float(row.get(s161.SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return 0.0
    spec = s161.CONTEXT_GATE_SPECS[variant.adapter_id]
    extra = VARIANT_EXTRAS[variant.adapter_id]
    if signal > 0:
        rule = str(extra["long_block_rule"])
        if rule == "lowedge_gate" and s172.lowedge_hit(row, spec):
            return 2.0
        if rule == "wide_lowedge" and bounded_lowedge_hit(row, spec, "wide"):
            return 2.0
        if rule == "tight_lowedge" and bounded_lowedge_hit(row, spec, "tight"):
            return 2.0
        if rule == "session_only" and bounded_lowedge_hit(row, spec, "", use_margin=False):
            return 2.0
    if signal < 0:
        rule = str(extra["short_block_rule"])
        if rule in {"wide_lowedge", "midwide_lowedge"} and bounded_lowedge_hit(row, spec, "wide"):
            return 1.0
    return 0.0


def configure_runner() -> None:
    context_specs = {}
    for variant in VARIANTS:
        extra = VARIANT_EXTRAS[variant.adapter_id]
        context_specs[variant.adapter_id] = {
            "gate_column": f"stage204_gate_{extra['axis']}",
            "gate_type": "encoded_stage204_selective_probability_margin_repair",
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
            "description": "Stage204 encoded gate: selective long-side probability/margin repair.",
        }
    install_stage_values(context_specs)
    s172.configure_runner = configure_runner
    s172.build_attempts = build_attempts
    s172.gate_value = gate_value
    s161.gate_value = gate_value
    s161.build_attempts = build_attempts
    s161.extra_set_values = s172.extra_set_values
    s161._CONTEXT_LOOKUP = None


def decide(rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage204_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(row.get("hard_quality_pass") for row in rows):
        return "open_stage205_stage204_selective_probability_margin_followup_review_candidate_not_final"
    return "open_stage205_bounded_followup_due_to_selective_probability_margin_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            bool(row.get("hard_quality_pass")),
            as_float(row, "validation_net") >= LEGACY_34D["net_profit"],
            as_float(row, "validation_pf") >= LEGACY_34D["profit_factor"],
            as_float(row, "validation_balance_dd_percent") <= LEGACY_34D["max_drawdown_percent"],
            as_float(row, "validation_mid_pf"),
            -as_float(row, "validation_late_net_share"),
            as_float(row, "oos_pf"),
            as_float(row, "oos_net"),
        ),
    )


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    variants = {variant.adapter_id: variant for variant in VARIANTS}
    for row in rows:
        adapter_id = str(row.get("adapter_id", ""))
        variant = variants.get(adapter_id)
        threshold = "unknown(미확인)"
        if variant is not None:
            threshold = f"{variant.short_threshold:.2f}/{variant.long_threshold:.2f}"
        extra = VARIANT_EXTRAS.get(adapter_id, {})
        gate = f"{extra.get('short_block_rule', '')}/{extra.get('long_block_rule', '')}"
        lines.append(
            "| {adapter_id} | {axis} | {threshold} | {gate} | {pf:.6f} | {net:.2f} | {dd:.4f} | {mid:.6f} | {late:.4f} | {oos_pf:.6f} | {flags} |".format(
                adapter_id=adapter_id,
                axis=extra.get("axis", ""),
                threshold=threshold,
                gate=gate,
                pf=as_float(row, "validation_pf"),
                net=as_float(row, "validation_net"),
                dd=as_float(row, "validation_balance_dd_percent"),
                mid=as_float(row, "validation_mid_pf"),
                late=as_float(row, "validation_late_net_share"),
                oos_pf=as_float(row, "oos_pf"),
                flags=row.get("quality_flags", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(rows)
    ref = next((row for row in rows if row.get("adapter_id") == "s204_cd8_ref_r0325"), {})
    return f"""# Stage204 Selective Probability/Margin Repair Report(204단계 선별 확률/마진 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_stage203_evidence_commit(원천 203단계 근거 커밋): `{SOURCE_STAGE203_EVIDENCE_COMMIT}`
- source_stage203_hash_record_commit(원천 203단계 해시 기록 커밋): `{SOURCE_STAGE203_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage202(202단계) reference(기준)의 net/PF/OOS(순손익/수익요인/표본외)를 보존하면서, long-side context gate(롱 방향 문맥 제한문)를 선별 조정하면 validation DD/mid PF(검증 낙폭/중반 수익요인)가 개선되는가?
- action(행동): risk cap(위험 상한) `0.0325`, SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유), thresholds(문턱값)는 고정하고 long-side gate(롱 방향 제한문)만 wide/tight/session(넓게/좁게/세션만)으로 바꿨다.
- effect(효과): Stage202(202단계)의 side-wide longcut(롱 전체 차단)보다 덜 거칠게 DD(낙폭)를 낮출 수 있는지 본다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage204(204단계)를 닫고 Stage205(205단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(rows)}

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `{best.get("adapter_id", "none")}`는 validation net(검증 순손익) `{as_float(best, "validation_net"):.2f}`, validation DD(검증 낙폭) `{as_float(best, "validation_balance_dd_percent"):.4f}`, mid PF(중반 수익요인) `{as_float(best, "validation_mid_pf"):.6f}`, late share(후반 비중) `{as_float(best, "validation_late_net_share"):.4f}`를 기록했다.
- comparison_baseline(비교 기준): Stage204 reference(204단계 기준) `{ref.get("adapter_id", "none")}`는 validation net(검증 순손익) `{as_float(ref, "validation_net"):.2f}`, validation DD(검증 낙폭) `{as_float(ref, "validation_balance_dd_percent"):.4f}`, mid PF(중반 수익요인) `{as_float(ref, "validation_mid_pf"):.6f}`, late share(후반 비중) `{as_float(ref, "validation_late_net_share"):.4f}`다.
- likely_drivers(가능 원인): long-side gate(롱 방향 제한문)가 일부 위험 구간만 줄이면 DD(낙폭)는 개선되고 net/OOS(순손익/표본외)는 보존될 수 있다.
- alternative_explanations(대체 설명): gate(제한문)가 너무 넓으면 Stage202 longcut(202단계 롱 차단)처럼 수익 엔진도 같이 잘릴 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage205_review`다. Effect(효과): Stage204(204단계)는 실행 측정이고, Stage205(205단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage204(204단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage204 Decision(204단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_stage203_evidence_commit(원천 203단계 근거 커밋): `{SOURCE_STAGE203_EVIDENCE_COMMIT}`
- source_stage203_hash_record_commit(원천 203단계 해시 기록 커밋): `{SOURCE_STAGE203_HASH_RECORD_COMMIT}`
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

Stage204(204단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage205(205단계) follow-up review(후속 검토)에서 selective probability/margin(선별 확률/마진) 상충을 따로 판정한다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = s188.artifact_rows(result)
    for row in rows:
        if row.get("artifact_type") != "mt5_strategy_tester_report":
            row["artifact_type"] = "stage204_evidence"
            row["notes"] = "Stage204 selective probability/margin repair evidence."
        else:
            row["notes"] = "Stage204 MT5 Strategy Tester report."
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
                "lane": "baseline_adapter_stage204_selective_probability_margin_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": s172.ledger_pairs(
                    (
                        ("source_stage203_evidence_commit", SOURCE_STAGE203_EVIDENCE_COMMIT),
                        ("source_stage203_hash_record_commit", SOURCE_STAGE203_HASH_RECORD_COMMIT),
                        ("source_adapter", SOURCE_ADAPTER_ID),
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
                "kpi_scope": "stage204_selective_probability_margin_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage204 materialized or blocked before KPI records were available.",
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
        f"""# Stage204 Closeout Packet(204단계 종료 작업 묶음)

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

Stage205(205단계)는 Stage204(204단계) selective probability/margin repair(선별 확률/마진 수리) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage204(204단계) selective long-side gates(선별 롱 방향 제한문) improve validation DD/mid PF(검증 낙폭/중반 수익요인) without damaging validation net/PF(검증 순손익/수익요인), trade supply(거래 공급), OOS(표본외), and risk/ATR telemetry(위험/ATR 기록)?

Effect(효과): Stage204(204단계) 안에서 추가 수리를 하지 않고, selective repair(선별 수리) 측정 결과를 별도 판독 단계에서 과장 없이 판단한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage205 Inputs(205단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 KPI 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage205 Review Index(205단계 검토 색인)

- status(상태): `open_planned_from_stage204`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage205 Selection Status(205단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage204`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = s172.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage204(204단계) closed(종료) as `{decision}` and Stage205(205단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): selective probability/margin(선별 확률/마진) 결과를 별도 follow-up review(후속 검토)로 넘긴다.
- >-
  Stage204 evidence(204단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(BALANCE_CURVE_AUDIT_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): 실제 구속된 threshold(문턱값)가 DD/PF/OOS(낙폭/수익요인/표본외)에 준 영향을 같이 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage204_selective_probability_margin_repair:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage204_selective_probability_margin_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  balance_curve_audit_path: {rel(BALANCE_CURVE_AUDIT_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage204_selective_probability_margin_repair`
- status(상태): `stage204_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage204(204단계)는 Stage203(203단계) 판정에 따라 selective probability/margin(선별 확률/마진) 수리를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정했다. Effect(효과): Stage205(205단계)가 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.

## Latest Stage204 Evidence(최신 204단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    status = f"closed_{decision}" if external == "completed" else "blocked_runtime_incomplete"
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage204 Selection Status(204단계 선택 상태)

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
        f"""# Stage204 Review Index(204단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 KPI 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = s172.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s172.path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage204 selective probability/margin repair closeout(204단계 선별 확률/마진 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): risk cap/ATR bracket/cooldown(위험 상한/ATR 브래킷/대기)을 고정하고 selective long-side gate(선별 롱 방향 제한문)를 MT5(MetaTrader 5, 메타트레이더5)로 측정해 Stage205(205단계) follow-up review(후속 검토)로 넘겼다.\n"
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
        "stage_number": 204,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage204_v2_native_selective_probability_margin_repair",
        "feature_set_id": "stage204_signal_plus_encoded_selective_probability_margin_gate",
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
            "stage171_primary": STAGE171_PRIMARY,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality)
    if not args.materialize_only:
        write_next_stage_seed(decision, external)
        update_current_truth(decision, external)
        write_status_files(decision, external)
        append_changelog(decision)
    print(
        json.dumps(
            s172.json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "external_verification_status": external,
                    "summary_csv": rel(SUMMARY_CSV_PATH),
                    "quality_matrix": rel(QUALITY_MATRIX_PATH),
                    "decision_path": rel(DECISION_PATH),
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
    raise SystemExit(main(sys.argv[1:]))


from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage184 import tp45_midwide_midsegment_quality_repair as s184  # noqa: E402

s180 = s184.s180
s178 = s184.s178
s176 = s184.s176
s174 = s184.s174
s172 = s184.s172
s161 = s184.s161
repair = s184.repair

STAGE_ID = "186_adapter_research__tp45_midwide_bracket_shape_repair"
RUN_NUMBER = "run186A"
RUN_ID = "run186A_stage186_tp45_midwide_bracket_shape_repair_v1"
PACKET_ID = "stage186_tp45_midwide_bracket_shape_repair_v1"
PARENT_RUN_ID = "run185A_stage185_stage184_midsegment_quality_followup_review_v1"
SOURCE_STAGE_ID = "185_adapter_research__stage184_midsegment_quality_followup_review"
SOURCE_RUN_ID = "run185A_stage185_stage184_midsegment_quality_followup_review_v1"
SOURCE_STAGE185_CLOSEOUT_COMMIT = "589ae57e5da2963c263c238b1fee03a858dcf614"
SOURCE_STAGE185_HASH_RECORD_COMMIT = "d46e0fdf4e5426f71ba21829daf0eb65a8cf486e"
SOURCE_ADAPTER_ID = "s184_mid_r0325_control"
NEXT_STAGE_ID = "187_adapter_research__stage186_bracket_shape_followup_review"
NEXT_RUN_ID = "run187A_stage187_stage186_bracket_shape_followup_review_v1"
NEXT_PACKET_ID = "stage187_stage186_bracket_shape_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = s180.LEGACY_34D
STAGE171_PRIMARY = s180.STAGE171_PRIMARY

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s186a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage186_bracket_shape_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage186_bracket_shape_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage186_bracket_shape_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage186_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage186_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage186_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage186_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage186_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage186_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage186_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage186_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage186_probability_binding_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage186_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage186_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage186_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage186_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage186/tp45_midwide_bracket_shape_repair.py")
ARTIFACT_COLUMNS = s172.ARTIFACT_COLUMNS

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s186_bctl",
        label="stage186_bctl",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.5,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage186 control: Stage184 control surface with TP45 and SL2.075.",
    ),
    repair.RepairVariant(
        adapter_id="s186_tp425",
        label="stage186_tp425",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.25,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage186: slightly shorter TP intended to capture mid-window MFE sooner.",
    ),
    repair.RepairVariant(
        adapter_id="s186_sl195",
        label="stage186_sl195",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.95,
        atr_take_profit_multiplier=4.5,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage186: slightly tighter SL intended to reduce validation DD without entry filtering.",
    ),
    repair.RepairVariant(
        adapter_id="s186_tp425_sl195",
        label="stage186_tp425_sl195",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.95,
        atr_take_profit_multiplier=4.25,
        model_risk_max_pct=0.0325,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage186: combined shorter TP and tighter SL bracket-shape test.",
    ),
)

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    variant.adapter_id: {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "lowedge_gate",
        "axis": variant.label.replace("stage186_", ""),
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04,
        "margin_max": 0.0775,
        "wide_session_min": 160.0,
        "wide_session_max": 285.0,
        "wide_margin_min": 0.0375,
        "wide_margin_max": 0.0825,
    }
    for variant in VARIANTS
}

MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}


def rel(path: Path | str) -> str:
    return s172.rel(path)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s172.as_float(row, key, default)


def sync_globals(context_specs: Mapping[str, Any] | None = None) -> None:
    values = stage_values(context_specs or {})
    values["VARIANT_BY_ID"] = {variant.adapter_id: variant for variant in VARIANTS}
    for name, value in values.items():
        setattr(s184, name, value)
    s184.VARIANTS = VARIANTS
    s184.VARIANT_EXTRAS = VARIANT_EXTRAS
    s184.MODEL_RISK_MIN_PCT = MODEL_RISK_MIN_PCT


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
        "SOURCE_SPECS_BY_VARIANT": {variant.adapter_id: dict(s161.s158.LOW_EDGE_SOURCE_SPEC) for variant in VARIANTS},
        "CONTEXT_GATE_SPECS": context_specs,
    }


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
                magic = 18610000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=186,
                        exploration_label="stage186_BaselineAdapter__TP45MidwideBracketShapeRepair",
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
            "gate_column": f"stage186_gate_{extra['axis']}",
            "gate_type": "encoded_tp45_midwide_bracket_shape_context",
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
            "description": "Stage186 encoded gate: value 1 blocks short, value 2 blocks long when enabled.",
        }
    sync_globals(context_specs)
    for name, value in stage_values(context_specs).items():
        for module in (s180, s178, s176, s174, s172, s161):
            setattr(module, name, value)
    s172.configure_runner = configure_runner
    s172.build_attempts = build_attempts
    s172.gate_value = s184.gate_value
    s161.gate_value = s184.gate_value
    s161.build_attempts = build_attempts
    s161.extra_set_values = s172.extra_set_values
    s161._CONTEXT_LOOKUP = None


def decide(rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage186_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(row.get("hard_quality_pass") for row in rows):
        return "open_stage187_bracket_shape_followup_review_candidate_not_final"
    return "open_stage187_bounded_followup_due_to_bracket_shape_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            bool(row.get("hard_quality_pass")),
            as_float(row, "validation_net") >= LEGACY_34D["net_profit"],
            as_float(row, "validation_pf") >= LEGACY_34D["profit_factor"],
            -max(0.0, as_float(row, "validation_balance_dd_percent") - LEGACY_34D["max_drawdown_percent"]),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_pf"),
        ),
    )


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | SL/TP(손절/익절) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {sl:.3f}/{tp:.2f} | {validation_pf:.6f} | {validation_net:.2f} | {validation_balance_dd_percent:.4f} | {validation_mid_pf:.6f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_balance_dd_percent:.4f} | {quality_flags} |".format(
                adapter_id=row.get("adapter_id", ""),
                sl=as_float(row, "atr_stop_multiplier"),
                tp=as_float(row, "atr_take_profit_multiplier"),
                validation_pf=as_float(row, "validation_pf"),
                validation_net=as_float(row, "validation_net"),
                validation_balance_dd_percent=as_float(row, "validation_balance_dd_percent"),
                validation_mid_pf=as_float(row, "validation_mid_pf"),
                oos_pf=as_float(row, "oos_pf"),
                oos_net=as_float(row, "oos_net"),
                oos_balance_dd_percent=as_float(row, "oos_balance_dd_percent"),
                quality_flags=row.get("quality_flags", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(rows)
    return f"""# Stage186 TP45 Midwide Bracket Shape Repair Report(186단계 익절 4.5 중간넓은 문맥 브래킷 모양 수정 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage184(184단계)의 entry gate(진입 제한문)는 실패했지만, TP/SL bracket shape(익절/손절 브래킷 모양)를 작게 바꾸면 mid PF(중반 수익요인), MFE capture(최대유리이동 포착), validation DD(검증 낙폭)를 개선할 수 있다.
- action(행동): model(모델), TP45 midwide context(익절 4.5 중간넓은 문맥), threshold(문턱값), hold/cooldown(보유/대기), model-controlled risk(모델 제어 위험), risk0325(위험 0.0325)는 고정하고 ATR SL/TP multiplier(ATR 손절/익절 배수)만 `2.075/4.5`, `2.075/4.25`, `1.95/4.5`, `1.95/4.25`로 바꿨다.
- effect(효과): entry filtering(진입 필터링)을 반복하지 않고, 같은 거래 표면의 exit shape(청산 모양)만 좁게 평가한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage186(186단계)을 닫고 Stage187(187단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(rows)}

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_balance_dd(검증 잔고 낙폭): `{as_float(best, "validation_balance_dd_percent"):.4f}`
- validation_mid_pf(검증 중반 수익요인): `{as_float(best, "validation_mid_pf"):.6f}`
- oos_balance_dd(표본외 잔고 낙폭): `{as_float(best, "oos_balance_dd_percent"):.4f}`
- quality_flags(품질 표식): `{best.get("quality_flags", "")}`

## Judgment(판정)

Stage186(186단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage186 Decision(186단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_stage185_closeout_commit(원천 185단계 종료 커밋): `{SOURCE_STAGE185_CLOSEOUT_COMMIT}`
- source_stage185_hash_record_commit(원천 185단계 해시 기록 커밋): `{SOURCE_STAGE185_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage186(186단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage187(187단계)에서 bracket/exit shape repair(브래킷/청산 모양 수정) 결과를 follow-up review(후속 검토)로 다시 판독한다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    now = s172.utc_now()
    rows: list[dict[str, Any]] = []
    paths = (
        PRODUCER_PATH,
        REPORT_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        BALANCE_CURVE_AUDIT_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        QUALITY_MATRIX_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
    )
    for path in paths:
        if s172.path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage186_evidence",
                    "path": rel(path),
                    "sha256": s172.sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage186 TP45 midwide bracket-shape repair evidence.",
                }
            )
    for report in result.get("reports", []):
        if not isinstance(report, Mapping):
            continue
        path = Path(str(report.get("report_path") or ""))
        if s172.path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": s172.sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage186 MT5 Strategy Tester report.",
                }
            )
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
                "lane": "baseline_adapter_stage186_tp45_midwide_bracket_shape_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": s172.ledger_pairs(
                    (
                        ("source_stage185_closeout_commit", SOURCE_STAGE185_CLOSEOUT_COMMIT),
                        ("source_stage185_hash_record_commit", SOURCE_STAGE185_HASH_RECORD_COMMIT),
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
                "kpi_scope": "stage186_tp45_midwide_bracket_shape_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage186 materialized or blocked before KPI records were available.",
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
        "segment_kpi": rel(SEGMENT_KPI_PATH),
        "balance_curve_audit": rel(BALANCE_CURVE_AUDIT_PATH),
        "monthly_kpi": rel(MONTHLY_KPI_PATH),
        "concentration_risk": rel(CONCENTRATION_PATH),
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
        f"""# Stage186 Closeout Packet(186단계 종료 작업 묶음)

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

Stage187(187단계)는 Stage186(186단계) TP45(익절 4.5) midwide bracket/exit shape repair(중간넓은 문맥 브래킷/청산 모양 수정) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage186(186단계) improve validation mid PF(검증 중반 수익요인), validation DD(검증 낙폭), and MFE capture(최대유리이동 포착) while preserving validation net/PF(검증 순손익/수익요인), OOS DD(표본외 낙폭), ATR bracket(ATR 브래킷), and model-controlled risk(모델 제어 위험), or should the path move to another bounded repair(경계 수정), demotion(강등), or branch(분기)?

Effect(효과): Stage186(186단계) 안에서 끝없이 고치지 않고, bracket/exit shape repair(브래킷/청산 모양 수정)의 실제 KPI(핵심 성과 지표) 효용만 따로 판독한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage187 Inputs(187단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage187 Review Index(187단계 검토 색인)

- status(상태): `open_planned_from_stage186`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage187 Selection Status(187단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage186`
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
    if external == "completed":
        state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
        state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
        focus = f"""current_focus:
- >-
  Stage186(186단계) closed(종료) as `{decision}` and Stage187(187단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): TP45(익절 4.5) midwide bracket/exit shape repair(중간넓은 문맥 브래킷/청산 모양 수정) 결과를 별도 follow-up review(후속 검토)로 넘긴다.
- >-
  Stage186 evidence(186단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(BALANCE_CURVE_AUDIT_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): net(순손익), PF(수익요인), DD(낙폭), segment(구간), concentration(집중도), ATR/risk telemetry(ATR/위험 기록)를 함께 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    else:
        focus = f"""current_focus:
- >-
  Stage186(186단계) runtime evidence(런타임 근거)가 incomplete(불완전)하여 `{decision}`로 기록했다. Effect(효과): 완료 주장을 낮추고 Stage186 runtime completion(런타임 완료) 조건을 보존한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage186_tp45_midwide_bracket_shape_repair:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage186_tp45_midwide_bracket_shape_repair:
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
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    s172.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage186_tp45_midwide_bracket_shape_surface`
- status(상태): `stage186_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage186(186단계)는 TP45(익절 4.5) midwide context(중간넓은 문맥) surface(표면)에서 ATR bracket(ATR 브래킷)과 model-controlled risk(모델 제어 위험)를 보존하고 bracket/exit shape repair(브래킷/청산 모양 수정)를 측정했다. Effect(효과): Stage187(187단계)는 결과를 final(최종)로 보지 않고 KPI(핵심 성과 지표) 상충을 follow-up review(후속 검토)로 판독한다.

## Latest Stage186 Evidence(최신 186단계 근거)

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
        f"""# Stage186 Selection Status(186단계 선택 상태)

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
        f"""# Stage186 Review Index(186단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
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
        f"\n## {s172.utc_now()} Stage186 TP45 midwide bracket shape repair closeout(186단계 익절 4.5 중간넓은 문맥 브래킷 모양 수정 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): risk0325(위험 0.0325)를 중심으로 ATR SL/TP bracket(ATR 손절/익절 브래킷)을 MT5(MetaTrader 5, 메타트레이더5)로 측정한 뒤 Stage187(187단계) follow-up review(후속 검토)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    s172.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def patch_driver() -> None:
    configure_runner()
    s172.configure_runner = configure_runner
    s172.build_attempts = build_attempts
    s172.decide = decide
    s172.report_markdown = report_markdown
    s172.decision_markdown = decision_markdown
    s172.artifact_rows = artifact_rows
    s172.write_ledgers = write_ledgers
    s172.write_packet_files = write_packet_files
    s172.write_next_stage_seed = write_next_stage_seed
    s172.update_current_truth = update_current_truth
    s172.write_status_files = write_status_files
    s172.append_changelog = append_changelog


def main(argv: Sequence[str] | None = None) -> int:
    patch_driver()
    return s172.main(argv or sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

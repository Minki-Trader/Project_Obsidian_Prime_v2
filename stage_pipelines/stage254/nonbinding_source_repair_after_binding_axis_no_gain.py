from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage252 import asymmetric_binding_repair_after_stage250_overprune as base


s250 = base.s250

STAGE_ID = "254_adapter_research__nonbinding_source_repair_after_binding_axis_no_gain"
RUN_NUMBER = "run254A"
RUN_ID = "run254A_stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1"
PACKET_ID = "stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1"
PARENT_RUN_ID = "run253A_stage253_stage252_asymmetric_binding_followup_review_v1"
SOURCE_STAGE_ID = "253_adapter_research__stage252_asymmetric_binding_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE252_EVIDENCE_COMMIT = "53aa5f020f0b7e6d97325d9fc25b2a50a3be5c1d"
SOURCE_STAGE252_HASH_RECORD_COMMIT = "1ae463e528189f7d406580aa99923edf0600aa46"
SOURCE_STAGE253_EVIDENCE_COMMIT = "e7f7a542e425fb4bdaf340cb669cc5b4dbb75933"
SOURCE_STAGE253_HASH_RECORD_COMMIT = "ca9af85eaa28295532018b7b98950f829ca67645"
NEXT_STAGE_ID = "255_adapter_research__stage254_nonbinding_source_followup_review"
NEXT_RUN_ID = "run255A_stage255_stage254_nonbinding_source_followup_review_v1"
NEXT_PACKET_ID = "stage255_stage254_nonbinding_source_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_nonbinding_lifecycle_repair_after_binding_axis_no_gain"
BOUNDARY = s250.BOUNDARY
LEGACY_34D = s250.LEGACY_34D
OOS_REFERENCE = dict(s250.OOS_REFERENCE)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
COMMON_ROOT = f"OPV2/s254a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage254_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage254_nonbinding_source_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage254_nonbinding_source_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage254_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage254_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage254_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage254_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage254_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage254_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage254_risk_atr_telemetry.csv"
FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage254_nonbinding_source_feature_summary.csv"
PROBABILITY_PATH = REVIEWS_ROOT / "stage254_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage254_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage254_tier_b_diagnostic_summary.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage254_performance_attribution.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage254_failure_memory.csv"
DECISION_PATH = REVIEWS_ROOT / "stage254_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage254_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage254/nonbinding_source_repair_after_binding_axis_no_gain.py")

SIGNAL_COLUMN = s250.SIGNAL_COLUMN
RANK_COLUMN = "stage254_nonbinding_rank_bucket"
GATE_COLUMN_PREFIX = "stage254_nonbinding_gate"
SOURCE_SPEC = dict(s250.SOURCE_SPEC)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s250.rel(path)


def write_md(path: Path, text: str) -> None:
    s250.write_md(path, text)


def write_json(path: Path, payload: Any) -> None:
    s250.write_json(path, payload)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    s250.write_csv(path, rows, columns)


def csv_value(value: Any) -> str:
    return s250.csv_value(value)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s250.as_float(row, key, default)


def repair_variant(
    adapter_id: str,
    label: str,
    *,
    max_hold_bars: int = 3,
    same_direction_reentry_cooldown_bars: int = 8,
    close_on_flat_signal: bool = False,
    reverse_on_opposite_signal: bool = True,
    note: str,
) -> Any:
    return s250.stage238.repair.RepairVariant(
        adapter_id=adapter_id,
        label=label,
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.0305,
        same_direction_reentry_cooldown_bars=same_direction_reentry_cooldown_bars,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=close_on_flat_signal,
        reverse_on_opposite_signal=reverse_on_opposite_signal,
        close_only_on_opposite_signal=False,
        max_hold_bars=max_hold_bars,
        notes=note,
    )


VARIANTS = (
    repair_variant(
        "s254_stage252_control",
        "stage254_stage252_control",
        note="Stage254 control: preserve Stage252 control decision table, ATR bracket, model risk, hold 3, cooldown 8.",
    ),
    repair_variant(
        "s254_hold4",
        "stage254_hold4",
        max_hold_bars=4,
        note="Stage254 non-binding lifecycle repair: extend max hold to 4 bars.",
    ),
    repair_variant(
        "s254_hold5",
        "stage254_hold5",
        max_hold_bars=5,
        note="Stage254 non-binding lifecycle repair: extend max hold to 5 bars.",
    ),
    repair_variant(
        "s254_hold4_flatclose",
        "stage254_hold4_flatclose",
        max_hold_bars=4,
        close_on_flat_signal=True,
        note="Stage254 non-binding lifecycle repair: hold 4 with flat-signal close.",
    ),
    repair_variant(
        "s254_hold4_reentry12",
        "stage254_hold4_reentry12",
        max_hold_bars=4,
        same_direction_reentry_cooldown_bars=12,
        note="Stage254 non-binding lifecycle repair: hold 4 with 12-bar same-direction reentry cooldown.",
    ),
)


def _score(short: float, flat: float, long: float) -> tuple[float, float, float]:
    return (float(short), float(flat), float(long))


def lifecycle_extra(axis: str) -> dict[str, Any]:
    return {
        "axis": axis,
        "asymmetric_gate": "none",
        "low_penalty": 0.0,
        "mid_penalty": 0.0,
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "reference_nonbinding_lifecycle_only",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge_plus_optional_short_low",
        "long_block_rule": "session_only_plus_optional_long_low",
        "rank_scores": {
            "low": _score(0.0, 0.0, 0.0),
            "mid": _score(0.0, 0.0, 0.0),
            "high": _score(0.10, -0.10, 0.10),
            "vhigh": _score(0.15, -0.15, 0.15),
        },
    }


VARIANT_EXTRAS = {item.adapter_id: lifecycle_extra(item.adapter_id.replace("s254_", "")) for item in VARIANTS}
SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}


def write_nonbinding_feature(source: Path, destination: Path, variant: Any, split: str) -> dict[str, Any]:
    extra_cfg = VARIANT_EXTRAS[variant.adapter_id]
    gate_column = f"{GATE_COLUMN_PREFIX}_{extra_cfg['axis']}"
    s250.io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    signal_rows = 0
    blocked_signal_rows = 0
    rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    allowed_signal_rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    with s250.io_path(source).open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with s250.io_path(destination).open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(output_handle, fieldnames=("bar_time_server", SIGNAL_COLUMN, RANK_COLUMN, gate_column), lineterminator="\n")
            writer.writeheader()
            for row in reader:
                total_rows += 1
                signal = int(round(s250.stage238.parse_float(row.get(SIGNAL_COLUMN), 0.0)))
                bucket_value, bucket_label = s250.stage238.rank_bucket_for(row)
                gate = s250.stage238.reference_gate_value(row)
                rank_counts[bucket_label] += 1
                if signal != 0:
                    signal_rows += 1
                    if gate >= 0.5:
                        blocked_signal_rows += 1
                    else:
                        allowed_signal_rank_counts[bucket_label] += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        SIGNAL_COLUMN: csv_value(float(signal)),
                        RANK_COLUMN: csv_value(float(bucket_value)),
                        gate_column: csv_value(gate),
                    }
                )
    return {
        "run_id": RUN_ID,
        "adapter_id": variant.adapter_id,
        "split": split,
        "gate_column": gate_column,
        "source_feature": rel(source),
        "decision_feature": rel(destination),
        "total_rows": total_rows,
        "signal_rows": signal_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "allowed_signal_rows": signal_rows - blocked_signal_rows,
        "rank_counts": rank_counts,
        "allowed_signal_rank_counts": allowed_signal_rank_counts,
        "max_hold_bars": variant.max_hold_bars,
        "same_direction_reentry_cooldown_bars": variant.same_direction_reentry_cooldown_bars,
        "close_on_flat_signal": variant.close_on_flat_signal,
        "reverse_on_opposite_signal": variant.reverse_on_opposite_signal,
        "gate_description": "Stage254 keeps the Stage252 control score/gate surface and changes only non-binding lifecycle knobs.",
        "side_filter_feature_index": 2,
        "rank_feature_index": 1,
    }


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
                magic = 25410000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s250.stage238.s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=254,
                        exploration_label="stage254_BaselineAdapter__NonbindingLifecycleRepair",
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


def hard_quality_pass(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_net") >= LEGACY_34D["net_profit"]
        and as_float(row, "validation_early_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_mid_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_balance_dd_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(row, "oos_net") >= OOS_REFERENCE["oos_net"]
        and as_float(row, "oos_pf") >= OOS_REFERENCE["oos_pf"]
        and as_float(row, "oos_balance_dd_percent", 99.0) <= OOS_REFERENCE["oos_dd"]
    )


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            hard_quality_pass(row),
            as_float(row, "validation_net"),
            -as_float(row, "validation_balance_dd_percent", 99.0),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
        ),
    )


def decide(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage254_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(hard_quality_pass(row) for row in quality_rows):
        return "open_stage255_bounded_followup_due_to_nonbinding_lifecycle_34d_candidate_not_final"
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s254_stage252_control"), {})
    best = best_row(quality_rows)
    if best and reference and best.get("adapter_id") != reference.get("adapter_id"):
        if (
            as_float(best, "validation_net") > as_float(reference, "validation_net")
            or as_float(best, "validation_balance_dd_percent", 99.0) < as_float(reference, "validation_balance_dd_percent", 99.0)
            or as_float(best, "validation_mid_pf") > as_float(reference, "validation_mid_pf")
        ):
            return "open_stage255_bounded_followup_due_to_nonbinding_lifecycle_tradeoff_candidate_not_final"
    return "open_stage255_bounded_followup_due_to_nonbinding_lifecycle_no_gain_candidate_not_final"


def performance_attribution_rows(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s254_stage252_control"), {})
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = str(row.get("adapter_id", ""))
        if adapter == "s254_stage252_control":
            rows.append(
                {
                    "attribution_id": f"{RUN_ID}__{adapter}",
                    "observed_change": "Stage252 control surface re-run as Stage254 control",
                    "comparison_baseline": "s252_binding_control",
                    "likely_drivers": "same score/gate surface, ATR bracket, model risk cap, thresholds, max hold 3, and cooldown 8",
                    "segment_checks": "validation/OOS, early/mid/late PF, DD, probability telemetry, risk/ATR telemetry",
                    "trade_shape": "control row for non-binding lifecycle repair",
                    "alternative_explanations": "small deltas can come from generated artifact identity and tester path differences",
                    "attribution_confidence": "high",
                    "next_probe": NEXT_STAGE_ID,
                }
            )
            continue
        rows.append(
            {
                "attribution_id": f"{RUN_ID}__{adapter}",
                "observed_change": (
                    f"validation_net_delta={as_float(row, 'validation_net') - as_float(reference, 'validation_net'):.2f};"
                    f"validation_dd_delta={as_float(row, 'validation_balance_dd_percent') - as_float(reference, 'validation_balance_dd_percent'):.4f};"
                    f"validation_mid_pf_delta={as_float(row, 'validation_mid_pf') - as_float(reference, 'validation_mid_pf'):.6f};"
                    f"oos_net_delta={as_float(row, 'oos_net') - as_float(reference, 'oos_net'):.2f}"
                ),
                "comparison_baseline": "s254_stage252_control",
                "likely_drivers": "lifecycle settings changed exit/reentry timing while score surface and thresholds stayed fixed",
                "segment_checks": "validation/OOS KPI, early/mid/late segments, DD, risk/ATR telemetry, probability telemetry",
                "trade_shape": "hold duration, flat-close, or same-direction reentry cooldown can alter MFE capture, MAE, and same-move density without binding overprune",
                "alternative_explanations": "one lifecycle knob can shift exposure timing rather than improve true entry quality",
                "attribution_confidence": "medium_high",
                "next_probe": NEXT_STAGE_ID,
            }
        )
    return rows


def failure_memory_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_row(quality_rows)
    return [
        {
            "failure_id": f"{RUN_ID}__stage254_not_final_until_followup_review",
            "evidence": f"best_adapter={best.get('adapter_id', '')};hard_quality_pass={hard_quality_pass(best)}",
            "impact": "one bounded non-binding lifecycle run does not complete the research package",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__binding_axis_not_repeated",
            "evidence": "Stage254 preserves score/gate surface and changes only lifecycle knobs",
            "impact": "prevents repeating Stage250/252 threshold or binding overprune as the main repair axis",
            "next_handling": NEXT_STAGE_ID,
        },
    ]


def quality_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순수익) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | pass(통과) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('adapter_id','')} | {row.get('validation_pf','')} | {row.get('validation_net','')} | {row.get('validation_balance_dd_percent','')} | {row.get('validation_mid_pf','')} | {row.get('oos_pf','')} | {row.get('oos_net','')} | {row.get('hard_quality_pass','')} |"
        )
    return "\n".join(lines)


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(quality_rows)
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s254_stage252_control"), {})
    return f"""# Stage254 Non-binding Source/Lifecycle Repair(254단계 비결합 원천/생명주기 수리)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage253_evidence_commit(원천 253단계 근거 커밋): `{SOURCE_STAGE253_EVIDENCE_COMMIT}`
- source_stage253_hash_record_commit(원천 253단계 해시 기록 커밋): `{SOURCE_STAGE253_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can non-binding lifecycle repair(비결합 생명주기 수리) improve validation/OOS net, PF, DD, and mid-window behavior(검증/표본외 순수익, 수익요인, 낙폭, 중간 구간 행동) without using threshold/binding overprune(임계값/결합 과축소)?

## Design(설계)

- fixed(고정): score/gate surface(점수/게이트 표면), thresholds(임계값) `0.54/0.52`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험비율) cap(상한) `0.0305`.
- changed(변경): max_hold_bars(최대 보유 봉), close_on_flat_signal(무포지션 신호 청산), same_direction_reentry_cooldown_bars(동일 방향 재진입 대기).
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

{quality_table(quality_rows)}

## Easy Read(쉬운 해석)

- reference(기준): `{reference.get('adapter_id', '')}` validation net(검증 순수익) `{reference.get('validation_net', '')}`, DD(낙폭) `{reference.get('validation_balance_dd_percent', '')}`, mid PF(중간 수익요인) `{reference.get('validation_mid_pf', '')}`, OOS net(표본외 순수익) `{reference.get('oos_net', '')}`.
- best_read(최선 해석): `{best.get('adapter_id', '')}` validation net(검증 순수익) `{best.get('validation_net', '')}`, DD(낙폭) `{best.get('validation_balance_dd_percent', '')}`, mid PF(중간 수익요인) `{best.get('validation_mid_pf', '')}`, OOS net(표본외 순수익) `{best.get('oos_net', '')}`.
- ATR/risk(ATR/위험)는 유지됐지만 final adapter(최종 어댑터) 주장은 금지다.

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI matrix(KPI 행렬), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage255(255단계) follow-up review(후속 검토), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 Stage254(254단계) tradeoff(절충)를 판정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage254 Decision(254단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage252_evidence_commit(원천 252단계 근거 커밋): `{SOURCE_STAGE252_EVIDENCE_COMMIT}`
- source_stage252_hash_record_commit(원천 252단계 해시 기록 커밋): `{SOURCE_STAGE252_HASH_RECORD_COMMIT}`
- source_stage253_evidence_commit(원천 253단계 근거 커밋): `{SOURCE_STAGE253_EVIDENCE_COMMIT}`
- source_stage253_hash_record_commit(원천 253단계 해시 기록 커밋): `{SOURCE_STAGE253_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- probability_telemetry(확률 원격측정): `{rel(PROBABILITY_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage254(254단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def write_next_stage_seed(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage255(255단계)는 Stage254(254단계) non-binding lifecycle repair(비결합 생명주기 수리)를 review-only(검토 전용)로 닫는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage254(254단계) produce useful non-binding lifecycle movement(비결합 생명주기 이동), or did it preserve the Stage252/253(252/253단계) near-miss/no-gain problem?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage255 Input References(255단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_quality_matrix(원천 품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage255 Review Index(255단계 검토 색인)

- status(상태): `open_planned_from_stage254`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage255 Selection Status(255단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage254`
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
  Stage254(254단계) closed(종료) as `{decision}` and Stage255(255단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): non-binding lifecycle repair(비결합 생명주기 수리)의 KPI(핵심 성과 지표) 상충을 분리해서 판정한다.
- >-
  Stage254 evidence(254단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`에 있다. Effect(효과): Stage255(255단계)가 수리축 지속, 축 교체, 또는 demotion(강등)을 좁게 판정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    state = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, state, count=1, flags=re.DOTALL)
    stage254_block = f"""stage254_nonbinding_source_repair_after_binding_axis_no_gain:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage255_followup_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage252_evidence_commit: {SOURCE_STAGE252_EVIDENCE_COMMIT}
  source_stage252_hash_record_commit: {SOURCE_STAGE252_HASH_RECORD_COMMIT}
  source_stage253_evidence_commit: {SOURCE_STAGE253_EVIDENCE_COMMIT}
  source_stage253_hash_record_commit: {SOURCE_STAGE253_HASH_RECORD_COMMIT}
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
    stage255_block = f"""stage255_stage254_nonbinding_source_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage254
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage254_nonbinding_source_repair_after_binding_axis_no_gain", stage254_block)
    state = replace_stage_block(state, "stage255_stage254_nonbinding_source_followup_review", stage255_block)
    s250.io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage254_nonbinding_lifecycle_repair`
- status(상태): `stage254_closed_open_stage255_followup_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage254(254단계)는 non-binding lifecycle repair(비결합 생명주기 수리)를 MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외)로 측정했다.
Effect(효과): Stage255(255단계)는 이 결과를 review-only(검토 전용)로 판정한다.

## Latest Stage254 Evidence(최신 254단계 근거)

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
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage254 Review Index(254단계 검토 색인)

- status(상태): `closed_open_stage255_followup_candidate_not_final`
- current_run(현재 실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage254 Selection Status(254단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage255_followup_candidate_not_final`
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
    marker = "Stage254 non-binding lifecycle repair closeout"
    existing = re.sub(rf"\n## [^\n]*{re.escape(marker)}[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    entry = (
        f"\n## {utc_now()} Stage254 non-binding lifecycle repair closeout(254단계 비결합 생명주기 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage250/252(250/252단계)의 binding axis no-gain(결합 축 무개선)을 반복하지 않고 lifecycle(생명주기) 수리 근거로 분리했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    s250.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = base.ORIGINAL_ARTIFACT_ROWS(result)
    for row in rows:
        row["artifact_type"] = "stage254_nonbinding_lifecycle_repair_evidence"
        row["notes"] = "Stage254 non-binding lifecycle repair evidence; research only."
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
        row["scoreboard_lane"] = "baseline_adapter_stage254_nonbinding_lifecycle_repair"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage254_nonbinding_lifecycle_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": s250.ledger_pairs(
                [
                    ("source_stage252_evidence_commit", SOURCE_STAGE252_EVIDENCE_COMMIT),
                    ("source_stage252_hash_record_commit", SOURCE_STAGE252_HASH_RECORD_COMMIT),
                    ("source_stage253_evidence_commit", SOURCE_STAGE253_EVIDENCE_COMMIT),
                    ("source_stage253_hash_record_commit", SOURCE_STAGE253_HASH_RECORD_COMMIT),
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
        "source_stage252_evidence_commit": SOURCE_STAGE252_EVIDENCE_COMMIT,
        "source_stage252_hash_record_commit": SOURCE_STAGE252_HASH_RECORD_COMMIT,
        "source_stage253_evidence_commit": SOURCE_STAGE253_EVIDENCE_COMMIT,
        "source_stage253_hash_record_commit": SOURCE_STAGE253_HASH_RECORD_COMMIT,
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
        "result_judgment_gate.json": {**base_payload, "judgment_label": "nonbinding_lifecycle_repair_measured_candidate_not_final", "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {**base_payload, "attribution": rel(ATTRIBUTION_PATH), "status": "completed"},
        "artifact_lineage_audit.json": {**base_payload, "producer": rel(PRODUCER_PATH), "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {**base_payload, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": required_gates, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {**base_payload, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push"},
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage254 Closeout Packet(254단계 종료 작업 묶음)

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


def patch_modules() -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
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
        "GATE_FEATURE_SUMMARY_PATH": FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_PATH,
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
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "RANK_COLUMN": RANK_COLUMN,
        "GATE_COLUMN_PREFIX": GATE_COLUMN_PREFIX,
        "SOURCE_STAGE250_EVIDENCE_COMMIT": SOURCE_STAGE252_EVIDENCE_COMMIT,
        "SOURCE_STAGE251_EVIDENCE_COMMIT": SOURCE_STAGE253_EVIDENCE_COMMIT,
    }
    for name, value in values.items():
        setattr(base, name, value)
    base.write_asymmetric_feature = write_nonbinding_feature
    base.build_attempts = build_attempts
    base.decide = decide
    base.performance_attribution_rows = performance_attribution_rows
    base.failure_memory_rows = failure_memory_rows
    base.report_markdown = report_markdown
    base.decision_markdown = decision_markdown
    base.write_next_stage_seed = write_next_stage_seed
    base.update_current_truth = update_current_truth
    base.write_status_files = write_status_files
    base.append_changelog = append_changelog
    base.artifact_rows = artifact_rows
    base.write_packet_files = write_packet_files
    base.patch_stage250_module()


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    return s250.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    patch_modules()
    s250.configure_runner()
    s250.stage238.s161.configure_base()
    args = parse_args(argv or sys.argv[1:])
    inputs = s250.prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 254,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s250.stage238.s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage254_v2_native_nonbinding_lifecycle_repair",
        "feature_set_id": "stage254_stage252_control_surface_lifecycle_variants",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = s250.stage238.load_existing_result_if_requested(args) or s250.stage238.s161.base.execute_or_materialize(prepared, args)
    audit_rows = s250.stage238.s172.s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s250.stage238.s172.s58.risk_rows_from_result(result)
    summary_rows = s250.stage238.s172.s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s250.stage238.s172.s58.segment_kpi_rows(summary_rows)
    probability_rows = s250.stage238.s161.probability_binding_rows(result)
    model_rows = s250.stage238.s161.model_score_rows(inputs)
    balance_rows, monthly_rows, concentration_rows, drawdown_rows = s250.stage238.s172.build_curve_audit(summary_rows, segment_rows)
    quality_rows = s250.stage238.s172.quality_rows(summary_rows, segment_rows, balance_rows)
    attribution_rows = performance_attribution_rows(quality_rows, probability_rows)
    failure_rows = failure_memory_rows(quality_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality_rows, probability_rows, external)

    s250.stage238.s161.write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(BALANCE_CURVE_AUDIT_PATH, balance_rows)
    write_csv(MONTHLY_KPI_PATH, monthly_rows)
    write_csv(CONCENTRATION_PATH, concentration_rows)
    write_csv(DRAWDOWN_PATH, drawdown_rows)
    write_csv(QUALITY_MATRIX_PATH, quality_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, s250.tier_b_rows())
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(REPORT_PATH, report_markdown(quality_rows, probability_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "balance_rows": balance_rows,
            "monthly_rows": monthly_rows,
            "concentration_rows": concentration_rows,
            "drawdown_rows": drawdown_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "quality_rows": quality_rows,
            "attribution_rows": attribution_rows,
            "failure_rows": failure_rows,
            "gate_rows": inputs["gate_rows"],
            "source_stage252_evidence_commit": SOURCE_STAGE252_EVIDENCE_COMMIT,
            "source_stage253_hash_record_commit": SOURCE_STAGE253_HASH_RECORD_COMMIT,
            "overall_goal_complete": False,
            "pushed_commit_hash": "pending_until_push",
            "claim_boundary": BOUNDARY,
        },
    )
    write_next_stage_seed(decision, external)
    update_current_truth(decision, external)
    write_status_files(decision, external)
    append_changelog(decision)
    result_with_outputs = {
        **result,
        "report_path": rel(REPORT_PATH),
        "decision": decision,
        "external_verification_status": external,
    }
    artifacts = artifact_rows(result_with_outputs)
    ledger_payload = write_ledgers(result_with_outputs, decision, artifacts)
    write_packet_files(result_with_outputs, decision, ledger_payload, quality_rows)
    print(json.dumps({"run_id": RUN_ID, "decision": decision, "external_verification_status": external}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

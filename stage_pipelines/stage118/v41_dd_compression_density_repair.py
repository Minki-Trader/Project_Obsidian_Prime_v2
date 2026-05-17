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

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage116 import v41_density_quality_balance_repair as s116  # noqa: E402


s100 = s116.s100
s114 = s116.s114
s108 = s116.s108

STAGE_ID = "118_adapter_research__v41_dd_compression_density_repair"
RUN_NUMBER = "run118A"
RUN_ID = "run118A_stage118_v41_dd_compression_density_repair_v1"
PACKET_ID = "stage118_v41_dd_compression_density_repair_v1"
PARENT_RUN_ID = "run117A_stage117_v41_density_quality_followup_review_v1"
SOURCE_STAGE117_ID = "117_adapter_research__v41_density_quality_followup_review"
SOURCE_STAGE117_CLOSEOUT_COMMIT = "df51abd7602801dc78cf3e23172bf03b13688557"
SOURCE_STAGE117_LATEST_COMMIT = "f3263eaf79a5d5eb55c25ff7c3b35ec42544fa6c"
SOURCE_STAGE116_ID = "116_adapter_research__v41_density_quality_balance_repair"
SOURCE_STAGE116_CLOSEOUT_COMMIT = "e2ef0707cdaaefc77df92e5dac641db4199c3cb7"
SOURCE_STAGE116_LATEST_COMMIT = "c115268a398da4c8334b2c21530016f110b8e927"
SOURCE_ADAPTER_ID = "stage116_quality_density_surface"
NEXT_STAGE_ID = "119_adapter_research__v41_dd_compression_followup_review"
NEXT_RUN_ID = "run119A_stage119_v41_dd_compression_followup_review_v1"
NEXT_PACKET_ID = "stage119_v41_dd_compression_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
COMMON_ROOT = f"OPV2/s118a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage118_dd_compression_density_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage118_dd_compression_density_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage118_dd_compression_density_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage118_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage118_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage118_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage118_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage118_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage118_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
    "oos_early_net": 38.84,
    "oos_early_pf": 1.157011764,
}
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE116_BASELINES = {
    "s116_v41_h3_cd9_session_margin_lng52": {
        "profit_factor": 1.810756505,
        "net_profit": 2041.72,
        "max_drawdown_percent": 19.10,
        "trade_count": 174,
        "read": "stage116_quality_anchor",
    },
    "s116_v41_h3_cd8_session_margin_lng53": {
        "profit_factor": 1.707481833,
        "net_profit": 1783.59,
        "max_drawdown_percent": 19.59,
        "trade_count": 176,
        "read": "stage116_density_anchor",
    },
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s118_v41_h3_cd9_session_margin_risk040_lng52",
        label="stage118_quality_anchor_risk_cap_040_long52",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0400,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage118 risk-cap DD compression from Stage116 session+margin quality anchor.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s118_v41_h3_cd9_session_margin_risk035_lng52",
        label="stage118_quality_anchor_risk_cap_035_long52",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage118 risk-cap DD compression from Stage116 session+margin quality anchor.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s118_v41_h3_cd9_session_margin_risk030_lng52",
        label="stage118_quality_anchor_risk_cap_030_long52",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage118 risk-cap DD compression from Stage116 session+margin quality anchor.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s118_v41_h3_cd8_session_margin_risk035_lng53",
        label="stage118_density_anchor_risk_cap_035_long53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage118 risk-cap DD compression from Stage116 session+margin density anchor.",
    ),
)

SOURCE_BASELINE_BY_VARIANT = {
    "s118_v41_h3_cd9_session_margin_risk040_lng52": "s116_v41_h3_cd9_session_margin_lng52",
    "s118_v41_h3_cd9_session_margin_risk035_lng52": "s116_v41_h3_cd9_session_margin_lng52",
    "s118_v41_h3_cd9_session_margin_risk030_lng52": "s116_v41_h3_cd9_session_margin_lng52",
    "s118_v41_h3_cd8_session_margin_risk035_lng53": "s116_v41_h3_cd8_session_margin_lng53",
}

SOURCE_SPECS_BY_VARIANT = {
    variant.adapter_id: {
        "label": "v41_v22_midcov_et40_agree_h2c0_no_b",
        "feature_anchor": "s59ar_v41_sd8_h3_stage59d_adapter",
        "variant_root": s100.SOURCE_VARIANT_ROOT,
        "model": s100.SOURCE_MODEL,
        "validation_ini": s100.SOURCE_VAL_INI,
        "oos_ini": s100.SOURCE_OOS_INI,
    }
    for variant in VARIANTS
}

CONTEXT_GATE_SPECS = {
    "s118_v41_h3_cd9_session_margin_risk040_lng52": {
        "gate_column": "stage118_gate_session_margin_risk040_l52",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage116 session+margin quality gate with model-risk cap 4.0%.",
    },
    "s118_v41_h3_cd9_session_margin_risk035_lng52": {
        "gate_column": "stage118_gate_session_margin_risk035_l52",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage116 session+margin quality gate with model-risk cap 3.5%.",
    },
    "s118_v41_h3_cd9_session_margin_risk030_lng52": {
        "gate_column": "stage118_gate_session_margin_risk030_l52",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage116 session+margin quality gate with model-risk cap 3.0%.",
    },
    "s118_v41_h3_cd8_session_margin_risk035_lng53": {
        "gate_column": "stage118_gate_session_margin_cd8_risk035_l53",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage116 session+margin density gate with cooldown 8 and model-risk cap 3.5%.",
    },
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s116.as_float(row, key, default)


def routed_oos(summary_rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return s116.routed_oos(summary_rows)


def early_segment(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> Mapping[str, Any]:
    return s116.early_segment(segment_rows, adapter_id)


def stage118_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s100.base.engine.extra_set_values(variant, magic)
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 1
    values["InpFallbackSideFilterFeatureIndex"] = 1
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 0.5
    values["InpBlockLongFeatureMax"] = 1.5
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s100.parse_ini(s100.base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s100.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (s100.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 11810000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=118,
                        exploration_label="stage118_BaselineAdapter__DdCompressionDensityRepair",
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
                        extra_set_values=stage118_extra_set_values(variant, magic),
                    )
                )
    return attempts


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    adapter_id = str(row.get("adapter_id", ""))
    source_id = SOURCE_BASELINE_BY_VARIANT.get(adapter_id, "")
    return STAGE116_BASELINES.get(source_id, {})


def best_stage118(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in routed_oos(summary_rows):
        early = early_segment(segment_rows, str(row.get("adapter_id", "")))
        trades = as_float(row, "trade_count")
        pf = as_float(row, "profit_factor")
        net = as_float(row, "net_profit")
        dd = as_float(row, "max_drawdown_percent", 99.0)
        early_pf = as_float(early, "profit_factor")
        keeps_34d_pf_net = pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"]
        keeps_stage116_density = trades >= STAGE116_BASELINES["s116_v41_h3_cd9_session_margin_lng52"]["trade_count"]
        candidates.append(
            (
                dd <= LEGACY_34D["max_drawdown_percent"] and keeps_34d_pf_net and keeps_stage116_density,
                dd <= STAGE110_REFERENCE["oos_dd_pct"] and keeps_34d_pf_net and keeps_stage116_density,
                keeps_34d_pf_net,
                keeps_stage116_density,
                early_pf >= STAGE110_REFERENCE["oos_early_pf"],
                dd <= LEGACY_34D["max_drawdown_percent"],
                -dd,
                pf,
                net,
                trades,
                row,
            )
        )
    return max(candidates, key=lambda item: item[:10])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_dd_compression_runtime_repair_in_stage119_due_to_incomplete_runtime"
    best = best_stage118(summary_rows, segment_rows)
    early = early_segment(segment_rows, str(best.get("adapter_id", "")))
    trades = as_float(best, "trade_count")
    pf = as_float(best, "profit_factor")
    net = as_float(best, "net_profit")
    dd = as_float(best, "max_drawdown_percent", 99.0)
    if (
        dd <= LEGACY_34D["max_drawdown_percent"]
        and pf >= LEGACY_34D["profit_factor"]
        and net >= LEGACY_34D["net_profit"]
        and trades >= STAGE116_BASELINES["s116_v41_h3_cd9_session_margin_lng52"]["trade_count"]
        and as_float(early, "profit_factor") >= STAGE110_REFERENCE["oos_early_pf"]
    ):
        return "continue_dd_compression_followup_review_in_stage119_with_34d_dd_candidate"
    if dd <= STAGE110_REFERENCE["oos_dd_pct"] and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"]:
        return "continue_dd_compression_followup_review_in_stage119"
    return "continue_dd_compression_repair_review_in_stage119"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | source(원천) | risk cap(위험 상한) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | DD delta(손실률 차이) | trades(거래 수) | early PF(초반 수익 팩터) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        baseline_id = SOURCE_BASELINE_BY_VARIANT.get(adapter_id, "")
        baseline = source_baseline(row)
        early = early_segment(segment_rows, adapter_id)
        dd = as_float(row, "max_drawdown_percent")
        baseline_dd = float(baseline.get("max_drawdown_percent", 0.0) or 0.0)
        lines.append(
            "| {adapter} | {source} | {risk:.4f} | {pf:.6f} | {net:.2f} | {dd:.2f} | {delta:.2f} | {trades:.0f} | {early_pf:.6f} |".format(
                adapter=adapter_id,
                source=baseline_id,
                risk=as_float(row, "model_risk_max_pct"),
                pf=as_float(row, "profit_factor"),
                net=as_float(row, "net_profit"),
                dd=dd,
                delta=dd - baseline_dd,
                trades=as_float(row, "trade_count"),
                early_pf=as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    best = best_stage118(summary_rows, segment_rows)
    baseline = source_baseline(best)
    best_dd = as_float(best, "max_drawdown_percent")
    baseline_dd = float(baseline.get("max_drawdown_percent", 0.0) or 0.0)
    return f"""# Stage118 DD Compression Density Repair Report(118단계 손실률 압축 밀도 수리 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE117_ID}`
- source_stage117_closeout_commit(원천 117단계 종료 커밋): `{SOURCE_STAGE117_CLOSEOUT_COMMIT}`
- source_stage117_latest_commit(원천 117단계 최신 커밋): `{SOURCE_STAGE117_LATEST_COMMIT}`
- source_stage116_latest_commit(원천 116단계 최신 커밋): `{SOURCE_STAGE116_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage116(116단계)의 strong PF/net(강한 수익 팩터/순손익)을 크게 훼손하지 않으면서, model-risk cap(모델 위험 상한)만 낮춰 DD%(손실률)를 Stage110 reference(110단계 참조점) 또는 34D target(34D 목표)에 더 가깝게 압축할 수 있는가?

Effect(효과): Stage118(118단계)은 threshold-only density recovery(임계값만 낮추는 밀도 회복)를 반복하지 않고, ATR/bracket(ATR/괄호 주문)과 model-controlled risk%(모델 제어 위험 퍼센트)를 유지한 채 위험 상한만 좁게 시험한다.

## Result Table(결과 표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- oos_pf(표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(표본외 손실률): `{best_dd:.2f}`
- dd_delta_vs_stage116(116단계 대비 손실률 차이): `{best_dd - baseline_dd:.2f}`
- trades(거래 수): `{as_float(best, "trade_count"):.0f}`

## Judgment(판정)

- result_subject(판정 대상): Stage118 risk-cap DD compression(118단계 위험 상한 손실률 압축).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): 34D trade count(34D 거래 수) `404`에 가까운 density(밀도) 회복과 더 넓은 equity-shape audit(자본 곡선 형태 감사).
- judgment_label(판정 라벨): `dd_compression_measured_not_final`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

## Evidence Files(근거 파일)

- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- trade_audit(거래 감사): `{rel(AUDIT_CSV_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage118 Decision(118단계 판정)

decision(판정): `{decision}`

Stage118(118단계)은 Stage117(117단계)의 판정대로 DD compression density repair(손실률 압축 밀도 수리)를 실제 MT5 runtime(실행환경)에서 측정했다.

Effect(효과): 결과를 Stage119(119단계) follow-up review(후속 검토)로 넘겨, DD%(손실률) 개선이 단순 risk scaling(위험 축소)인지, 다음 density repair(밀도 수리)에 쓸 수 있는 안정 신호인지 판정한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage117_closeout_commit(원천 117단계 종료 커밋): `{SOURCE_STAGE117_CLOSEOUT_COMMIT}`
- source_stage117_latest_commit(원천 117단계 최신 커밋): `{SOURCE_STAGE117_LATEST_COMMIT}`
- source_stage116_latest_commit(원천 116단계 최신 커밋): `{SOURCE_STAGE116_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage118(118단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research(브이투 고유 연구)는 Stage119(119단계)에서 계속된다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage118_dd_compression_density_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage118 v2-native DD compression density repair artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if raw_path and path_exists(Path(str(raw_path))):
            path = Path(str(raw_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage118 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_dd_compression_density_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage117_closeout_commit", SOURCE_STAGE117_CLOSEOUT_COMMIT),
                        ("source_stage117_latest_commit", SOURCE_STAGE117_LATEST_COMMIT),
                        ("source_stage116_latest_commit", SOURCE_STAGE116_LATEST_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = s100.build_mt5_alpha_ledger_rows(
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
                "kpi_scope": "stage118_v41_dd_compression_density_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage118 run materialized or blocked before KPI records were available.",
            }
        ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def tier_b_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    coverage = s100.base.engine.route_coverage()
    for variant in VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_dd_compression_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage118 isolates Stage116 Tier A routed DD compression before any Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s108.write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [
                "obsidian-performance-attribution",
                "obsidian-result-judgment",
                "obsidian-runtime-parity",
                "obsidian-artifact-lineage",
            ],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": status,
        },
    )
    s108.write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": result.get("external_verification_status"),
            "completed_attempt_count": result.get("completed_attempt_count"),
            "expected_attempt_count": result.get("expected_attempt_count"),
            "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH),
            "claim_boundary": BOUNDARY,
        },
    )
    s108.write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "judgment_label": "dd_compression_measured_not_final",
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
            "overall_goal_complete": False,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    s108.write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage117_closeout_commit": SOURCE_STAGE117_CLOSEOUT_COMMIT,
            "source_stage117_latest_commit": SOURCE_STAGE117_LATEST_COMMIT,
            "source_stage116_closeout_commit": SOURCE_STAGE116_CLOSEOUT_COMMIT,
            "source_stage116_latest_commit": SOURCE_STAGE116_LATEST_COMMIT,
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def create_next_stage(decision: str, external: str) -> None:
    s108.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage119(119단계)은 Stage118(118단계)의 DD compression density repair(손실률 압축 밀도 수리) 결과를 후속 검토한다.

## Bounded Question(경계 질문)

Stage118(118단계)의 DD%(손실률) 개선이 34D KPI(34D 핵심 성과 지표) 목표를 향한 유효한 full-adapter repair(전체 어댑터 수리) 단서인가, 아니면 단순 risk scaling(위험 축소) 효과라서 density repair(밀도 수리)를 별도로 이어가야 하는가?

Effect(효과): Stage119(119단계)은 새 모델 hunting(모델 탐색)이 아니라 Stage118 evidence(근거)를 판독해서 다음 bounded repair(경계 수리)를 하나로 정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage119 Input References(119단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage118_report(118단계 보고서): `{rel(REPORT_PATH)}`
- stage118_summary(118단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage119(119단계)은 Stage118(118단계)의 실제 MT5 runtime evidence(실행환경 근거)만 받아 다음 수리 축을 정한다.
""",
    )
    s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage119 Review Index(119단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage119(119단계)은 Stage118(118단계) closeout(종료 기록)을 이어받아 후속 판정만 수행한다.
""",
    )
    s108.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage119 Selection Status(119단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage119(119단계)은 34D KPI(34D 핵심 성과 지표) 격차를 계속 줄이지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage118(118단계) closed(종료) as `{decision}` and Stage119(119단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): DD compression(손실률 압축) 결과를 후속 검토로 넘겨 density(밀도)와 34D KPI(34D 핵심 성과 지표) 격차를 계속 줄인다.
- >-
  Stage118 result(118단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록했다. Effect(효과): risk cap(위험 상한) 축소가 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수)에 준 영향을 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage118_v41_dd_compression_density_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage117_closeout_commit: {SOURCE_STAGE117_CLOSEOUT_COMMIT}
  source_stage117_latest_commit: {SOURCE_STAGE117_LATEST_COMMIT}
  source_stage116_closeout_commit: {SOURCE_STAGE116_CLOSEOUT_COMMIT}
  source_stage116_latest_commit: {SOURCE_STAGE116_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage118_v41_dd_compression_density_repair:"
    if marker in text:
        text = re.sub(r"\nstage118_v41_dd_compression_density_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage118 Selection Status(118단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE117_ID}`
- source_decision(원천 판정): `continue_dd_compression_density_repair_in_stage118`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage118_decision(118단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage118(118단계)은 실제 실행 결과를 기록하고, 운영 의미 없이 Stage119(119단계)로 넘긴다.
""",
    )
    s108.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage119_dd_compression_followup_review_surface`
- status(상태): `stage118_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage118(118단계) closed(종료) as v2-native v41 DD compression density repair(브이투 고유 브이41 손실률 압축 밀도 수리). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage119(119단계) DD compression follow-up review(손실률 압축 후속 검토)로 이어진다.

## Latest Stage118 Evidence(최신 118단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage118 Review Index(118단계 검토 색인)

- status(상태): `closed_{decision}`
- source_decision(원천 판정): `continue_dd_compression_density_repair_in_stage118`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage118(118단계)은 실제 MT5 runtime evidence(실행환경 근거)를 기록하고 Stage119(119단계) 후속 검토로 넘긴다.
""",
    )
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage118 v41 DD compression density repair closeout(118단계 v41 손실률 압축 밀도 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage116(116단계)의 quality/density anchors(품질/밀도 기준점)에 model-risk cap(모델 위험 상한) 축소를 적용해 DD%(손실률) 압축 가능성을 실제 MT5 runtime(실행환경)으로 측정하고 Stage119(119단계) 후속 검토로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def configure_stage118() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE115_ID": SOURCE_STAGE117_ID,
        "SOURCE_STAGE115_CLOSEOUT_COMMIT": SOURCE_STAGE117_CLOSEOUT_COMMIT,
        "SOURCE_STAGE115_LATEST_COMMIT": SOURCE_STAGE117_LATEST_COMMIT,
        "SOURCE_STAGE114_CLOSEOUT_COMMIT": SOURCE_STAGE116_CLOSEOUT_COMMIT,
        "SOURCE_STAGE114_LATEST_COMMIT": SOURCE_STAGE116_LATEST_COMMIT,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
        "VARIANTS": VARIANTS,
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }.items():
        setattr(s116, name, value)
    s116.build_attempts = build_attempts
    s116.decide = decide
    s116.report_markdown = report_markdown
    s116.decision_markdown = decision_markdown
    s116.artifact_rows = artifact_rows
    s116.write_ledgers = write_ledgers
    s116.write_packet_files = write_packet_files
    s116.update_current_truth = update_current_truth
    s116.append_changelog = append_changelog
    s116.configure_stage116()
    s100.tier_b_rows = tier_b_rows


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage118()
    return s100.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

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

from stage_pipelines.stage124 import v41_route_supply_density_repair_after_small_gain as s124  # noqa: E402


s100 = s124.s100
s108 = s124.s108

STAGE_ID = "128_adapter_research__v41_quality_reframe_after_shortgate_failure"
RUN_NUMBER = "run128A"
RUN_ID = "run128A_stage128_v41_quality_reframe_after_shortgate_failure_v1"
PACKET_ID = "stage128_v41_quality_reframe_after_shortgate_failure_v1"
PARENT_RUN_ID = "run127A_stage127_v41_shortgate_quality_followup_review_v1"
SOURCE_STAGE127_ID = "127_adapter_research__v41_shortgate_quality_followup_review"
SOURCE_STAGE127_CLOSEOUT_COMMIT = "b08c8ede9ba36e0aee6670abb818e63076b8c7a5"
SOURCE_STAGE127_LATEST_COMMIT = "30a94995ff3feccedf9815f683bdd71a72c9cc2c"
SOURCE_STAGE126_LATEST_COMMIT = "e8144bed82184543c079a846193bb4e1c7aae9e0"
SOURCE_ADAPTER_ID = "s126_v41_h3_cd6_shortgate_risk035_sht54_lng52"
NEXT_STAGE_ID = "129_adapter_research__v41_quality_density_followup_review"
NEXT_RUN_ID = "run129A_stage129_v41_quality_density_followup_review_v1"
NEXT_PACKET_ID = "stage129_v41_quality_density_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s128a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage128_quality_reframe_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage128_quality_reframe_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage128_quality_reframe_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage128_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage128_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage128_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage128_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage128_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage128_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE122_QUALITY = {
    "adapter_id": "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52",
    "profit_factor": 1.75,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
}
STAGE124_SHORTGATE = {
    "adapter_id": "s124_v41_h3_cd5_shortgate_risk035_sht54_lng52",
    "profit_factor": 1.51,
    "net_profit": 889.34,
    "max_drawdown_percent": 20.23,
    "trade_count": 230,
}
STAGE126_BEST = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.510119726,
    "net_profit": 882.40,
    "max_drawdown_percent": 20.12,
    "trade_count": 229,
}
STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s128_v41_h2_bothgate_sl2075_tp40_risk035_sht54_lng52",
        label="stage128_h2_bothgate_sl2075_tp40",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage128 quality-density reframe: both side gate, shorter hold, original bracket.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s128_v41_h2_bothgate_sl180_tp320_risk035_sht54_lng52",
        label="stage128_h2_bothgate_sl180_tp320",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.8,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage128 quality-density reframe: both side gate, shorter hold, tighter bracket.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s128_v41_h2_shortgate_sl2075_tp40_risk035_sht54_lng52",
        label="stage128_h2_shortgate_sl2075_tp40",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage128 quality-density reframe: shortgate supply, shorter hold, original bracket.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s128_v41_h2_shortgate_sl180_tp320_risk035_sht54_lng52",
        label="stage128_h2_shortgate_sl180_tp320",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.8,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage128 quality-density reframe: shortgate supply, shorter hold, tighter bracket.",
    ),
)

SOURCE_BASELINE_BY_VARIANT = {variant.adapter_id: SOURCE_ADAPTER_ID for variant in VARIANTS}
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
    "s128_v41_h2_bothgate_sl2075_tp40_risk035_sht54_lng52": {
        "gate_column": "stage128_gate_both_h2_sl2075_tp40",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage128 quality-density reframe: both side gate with shorter lifecycle.",
    },
    "s128_v41_h2_bothgate_sl180_tp320_risk035_sht54_lng52": {
        "gate_column": "stage128_gate_both_h2_sl180_tp320",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage128 quality-density reframe: both side gate with shorter lifecycle and tighter ATR bracket.",
    },
    "s128_v41_h2_shortgate_sl2075_tp40_risk035_sht54_lng52": {
        "gate_column": "stage128_gate_short_h2_sl2075_tp40",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage128 quality-density reframe: short side gate with shorter lifecycle.",
    },
    "s128_v41_h2_shortgate_sl180_tp320_risk035_sht54_lng52": {
        "gate_column": "stage128_gate_short_h2_sl180_tp320",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage128 quality-density reframe: short side gate with shorter lifecycle and tighter ATR bracket.",
    },
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s124.as_float(row, key, default)


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE126_BEST if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


def stage128_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s100.base.engine.extra_set_values(variant, magic)
    block_mode = str(CONTEXT_GATE_SPECS.get(variant.adapter_id, {}).get("block_mode", "both"))
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 1
    values["InpFallbackSideFilterFeatureIndex"] = 1
    values["InpBlockShortFeatureRange"] = block_mode in {"both", "short"}
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = block_mode in {"both", "long"}
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
                magic = 12810000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=128,
                        exploration_label="stage128_BaselineAdapter__QualityReframeAfterShortgateFailure",
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
                        extra_set_values=stage128_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage128(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in s124.s122.s120.routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        early = s124.s122.s120.early_segment(segment_rows, adapter_id)
        trades = as_float(row, "trade_count")
        pf = as_float(row, "profit_factor")
        net = as_float(row, "net_profit")
        dd = as_float(row, "max_drawdown_percent", 99.0)
        candidates.append(
            (
                trades >= 220 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= 18.0,
                trades >= 200 and pf > STAGE126_BEST["profit_factor"] and net >= STAGE126_BEST["net_profit"] and dd < STAGE126_BEST["max_drawdown_percent"],
                pf >= LEGACY_34D["profit_factor"],
                net >= LEGACY_34D["net_profit"],
                -dd,
                trades,
                as_float(early, "profit_factor"),
                row,
            )
        )
    return max(candidates, key=lambda item: item[:7])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_quality_density_runtime_repair_in_stage129_due_to_incomplete_runtime"
    best = best_stage128(summary_rows, segment_rows)
    trades = as_float(best, "trade_count")
    pf = as_float(best, "profit_factor")
    net = as_float(best, "net_profit")
    dd = as_float(best, "max_drawdown_percent", 99.0)
    if trades >= 220 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= 18.0:
        return "continue_quality_density_followup_review_in_stage129_with_material_repair"
    if trades >= 200 and pf > STAGE126_BEST["profit_factor"] and net >= STAGE126_BEST["net_profit"] and dd < STAGE126_BEST["max_drawdown_percent"]:
        return "continue_quality_density_followup_review_in_stage129_with_small_repair"
    return "continue_quality_density_followup_review_in_stage129_due_to_damage_or_no_repair"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | gate(게이트) | bracket(괄호) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | vs126 net(126 대비 순손익) | early PF(초반 수익 팩터) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in s124.s122.s120.routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        early = s124.s122.s120.early_segment(segment_rows, adapter_id)
        spec = CONTEXT_GATE_SPECS.get(adapter_id, {})
        variant = next((item for item in VARIANTS if item.adapter_id == adapter_id), None)
        bracket = "" if variant is None else f"SL{variant.atr_stop_multiplier}/TP{variant.atr_take_profit_multiplier}"
        lines.append(
            "| {adapter} | {gate} | {bracket} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {net_delta:.2f} | {early_pf:.6f} |".format(
                adapter=adapter_id,
                gate=spec.get("block_mode", ""),
                bracket=bracket,
                pf=as_float(row, "profit_factor"),
                net=as_float(row, "net_profit"),
                dd=as_float(row, "max_drawdown_percent"),
                trades=as_float(row, "trade_count"),
                net_delta=as_float(row, "net_profit") - STAGE126_BEST["net_profit"],
                early_pf=as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage128(summary_rows, segment_rows)
    return f"""# Stage128 Quality Reframe Report(128단계 품질 재구성 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE127_ID}`
- source_stage127_closeout_commit(원천 127단계 종료 커밋): `{SOURCE_STAGE127_CLOSEOUT_COMMIT}`
- source_stage127_latest_commit(원천 127단계 최신 커밋): `{SOURCE_STAGE127_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage126/127(126/127단계)에서 실패한 shortgate threshold/cooldown(숏 게이트 임계값/대기시간) 반복 대신, max_hold(최대 보유)와 ATR bracket(ATR 괄호) 재구성으로 34D KPI(34D 핵심 성과 지표)에 가까운 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 균형을 만들 수 있는가?

Effect(효과): Stage128(128단계)는 legacy method(레거시 방식)를 답습하지 않고 v2-native failure memory(브이투 고유 실패 기억)를 이용해 품질과 밀도의 균형만 좁게 본다.

## Result Table(결과표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_variant(최선 변형): `{best.get('adapter_id', '')}`
- oos_pf(표본외 수익 팩터): `{as_float(best, 'profit_factor'):.6f}`
- oos_net(표본외 순손익): `{as_float(best, 'net_profit'):.2f}`
- oos_dd_pct(표본외 손실률): `{as_float(best, 'max_drawdown_percent'):.2f}`
- trades(거래 수): `{as_float(best, 'trade_count'):.0f}`
- gap_to_34D(34D 대비 차이): PF `{as_float(best, 'profit_factor') - LEGACY_34D['profit_factor']:.6f}`, net `{as_float(best, 'net_profit') - LEGACY_34D['net_profit']:.2f}`, DD `{as_float(best, 'max_drawdown_percent') - LEGACY_34D['max_drawdown_percent']:.2f}`, trades `{as_float(best, 'trade_count') - LEGACY_34D['trade_count']:.0f}`.
- vs_stage126_best(126단계 최선 대비): net `{as_float(best, 'net_profit') - STAGE126_BEST['net_profit']:.2f}`, DD `{as_float(best, 'max_drawdown_percent') - STAGE126_BEST['max_drawdown_percent']:.2f}`, trades `{as_float(best, 'trade_count') - STAGE126_BEST['trade_count']:.0f}`.

## Judgment(판정)

- result_subject(판정 대상): Stage128 quality-density reframe(128단계 품질-밀도 재구성).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- judgment_label(판정 라벨): `quality_density_reframe_measured_not_final`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage128 Decision(128단계 판정)

decision(판정): `{decision}`

Stage128(128단계)는 Stage127(127단계) 판정대로 threshold/cooldown(임계값/대기시간) 반복을 멈추고 quality-density reframe(품질-밀도 재구성)을 좁게 실행했다.

Effect(효과): 결과를 Stage129(129단계) follow-up review(후속 검토)로 넘겨 34D KPI(34D 핵심 성과 지표) 격차와 다음 수리 경로를 다시 판독한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage127_closeout_commit(원천 127단계 종료 커밋): `{SOURCE_STAGE127_CLOSEOUT_COMMIT}`
- source_stage127_latest_commit(원천 127단계 최신 커밋): `{SOURCE_STAGE127_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage128(128단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research/development(브이투 고유 연구개발)는 Stage129(129단계)로 이어진다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        REPORT_PATH,
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
        if s124.s122.path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage128_quality_reframe_evidence",
                    "path": rel(path),
                    "sha256": s124.s122.sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage128 v2-native quality-density reframe artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if raw_path and s124.s122.path_exists(Path(str(raw_path))):
            path = Path(str(raw_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": s124.s122.sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage128 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = s124.s122.upsert_csv_rows(
        RUN_REGISTRY_PATH,
        s124.s122.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_quality_reframe_after_shortgate_failure",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": s124.s122.ledger_pairs(
                    (
                        ("source_stage127_closeout_commit", SOURCE_STAGE127_CLOSEOUT_COMMIT),
                        ("source_stage127_latest_commit", SOURCE_STAGE127_LATEST_COMMIT),
                        ("source_stage126_latest_commit", SOURCE_STAGE126_LATEST_COMMIT),
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
    alpha_payload = s124.s122.upsert_csv_rows(PROJECT_LEDGER_PATH, s124.s122.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = s124.s122.upsert_csv_rows(STAGE_LEDGER_PATH, s124.s122.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = s124.s122.upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def tier_b_rows() -> list[dict[str, Any]]:
    rows = []
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_quality_reframe",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage128 isolates Tier A quality-density reframe before Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s108.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment_design", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-artifact-lineage"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"], "status": status})
    s108.write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "claim_boundary": BOUNDARY})
    s108.write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "judgment_label": "quality_density_reframe_measured_not_final", "legacy_relation": "lesson_only_target_surface_no_code_copy", "overall_goal_complete": False})
    s108.write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage127_closeout_commit": SOURCE_STAGE127_CLOSEOUT_COMMIT, "source_stage127_latest_commit": SOURCE_STAGE127_LATEST_COMMIT, "source_stage126_latest_commit": SOURCE_STAGE126_LATEST_COMMIT, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage(decision: str, external: str) -> None:
    s108.write_md(NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage129(129단계)는 Stage128(128단계)의 quality-density reframe(품질-밀도 재구성) 결과를 후속 검토한다.

## Bounded Question(경계 질문)

Stage128(128단계)의 max_hold/ATR bracket(최대 보유/ATR 괄호) 재구성이 34D KPI(34D 핵심 성과 지표) 격차를 실제로 줄였는가, 아니면 다음 bounded repair(경계 수리), demotion(강등), 또는 new branch(새 분기)가 필요한가?

Effect(효과): Stage129(129단계)는 새 실험을 벌이지 않고 Stage128 evidence(근거)를 읽어 다음 경계를 정한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage129 Input References(129단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage128_report(128단계 보고서): `{rel(REPORT_PATH)}`
- stage128_summary(128단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage129 Review Index(129단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage129 Selection Status(129단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")


def update_current_truth(decision: str, external: str) -> None:
    text = s124.s122.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage128(128단계) closed(종료) as `{decision}` and Stage129(129단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): quality-density reframe(품질-밀도 재구성) 결과를 후속 검토로 넘겨 34D KPI(34D 핵심 성과 지표) 격차를 다시 판독한다.
- >-
  Stage128 result(128단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록했다. Effect(효과): max_hold/ATR bracket(최대 보유/ATR 괄호)이 손실률과 순손익을 실제로 바꿨는지 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage128_v41_quality_reframe_after_shortgate_failure:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage127_closeout_commit: {SOURCE_STAGE127_CLOSEOUT_COMMIT}
  source_stage127_latest_commit: {SOURCE_STAGE127_LATEST_COMMIT}
  source_stage126_latest_commit: {SOURCE_STAGE126_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage128_v41_quality_reframe_after_shortgate_failure:"
    if marker in text:
        text = re.sub(r"\nstage128_v41_quality_reframe_after_shortgate_failure:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    s124.s122.io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    s108.write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage128 Selection Status(128단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE127_ID}`
- source_decision(원천 판정): `continue_quality_reframe_in_stage128_after_shortgate_repair_failure`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage128_decision(128단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    s108.write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage128 Review Index(128단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
""")
    s108.write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage129_quality_density_followup_review_surface`
- status(상태): `stage128_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage128(128단계) closed(종료) as v2-native v41 quality-density reframe(브이투 고유 브이41 품질-밀도 재구성). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage129(129단계) quality-density follow-up review(품질-밀도 후속 검토)로 이어진다.

## Latest Stage128 Evidence(최신 128단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage128 v41 quality-density reframe closeout(128단계 v41 품질-밀도 재구성 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): shortgate threshold/cooldown(숏 게이트 임계값/대기시간) 반복을 멈추고 max_hold/ATR bracket(최대 보유/ATR 괄호) 재구성을 측정해 Stage129(129단계) 후속 검토로 넘겼다.\n"
    )
    existing = s124.s122.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s124.s122.path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        s124.s122.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def configure_stage128() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE123_CLOSEOUT_COMMIT": SOURCE_STAGE127_CLOSEOUT_COMMIT,
        "SOURCE_STAGE123_LATEST_COMMIT": SOURCE_STAGE127_LATEST_COMMIT,
        "SOURCE_STAGE122_LATEST_COMMIT": SOURCE_STAGE126_LATEST_COMMIT,
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
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "STAGE122_SOURCE": STAGE126_BEST,
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }.items():
        setattr(s124, name, value)
    s124.build_attempts = build_attempts
    s124.source_baseline = source_baseline
    s124.best_stage124 = best_stage128
    s124.decide = decide
    s124.row_table = row_table
    s124.report_markdown = report_markdown
    s124.decision_markdown = decision_markdown
    s124.artifact_rows = artifact_rows
    s124.write_ledgers = write_ledgers
    s124.tier_b_rows = tier_b_rows
    s124.write_packet_files = write_packet_files
    s124.update_current_truth = update_current_truth
    s124.append_changelog = append_changelog
    s124.configure_stage124()


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage128()
    return s124.s122.s120.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

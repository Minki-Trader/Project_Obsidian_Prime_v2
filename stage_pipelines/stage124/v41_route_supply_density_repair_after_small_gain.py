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

from stage_pipelines.stage122 import v41_density_scale_repair_after_dd_guardrail as s122  # noqa: E402


s100 = s122.s100
s108 = s122.s108

STAGE_ID = "124_adapter_research__v41_route_supply_density_repair_after_small_gain"
RUN_NUMBER = "run124A"
RUN_ID = "run124A_stage124_v41_route_supply_density_repair_after_small_gain_v1"
PACKET_ID = "stage124_v41_route_supply_density_repair_after_small_gain_v1"
PARENT_RUN_ID = "run123A_stage123_v41_density_scale_followup_review_v1"
SOURCE_STAGE123_ID = "123_adapter_research__v41_density_scale_followup_review"
SOURCE_STAGE123_CLOSEOUT_COMMIT = "36c6cbf4a89000b213d535b152ec2eb49fe26296"
SOURCE_STAGE123_LATEST_COMMIT = "410d29cb988af0d3a522201f5491fc8168405f7a"
SOURCE_STAGE122_LATEST_COMMIT = "fed35f028fac5621453df67889c4a95cbd8bd77a"
SOURCE_ADAPTER_ID = "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52"
NEXT_STAGE_ID = "125_adapter_research__v41_route_supply_followup_review_after_stage124"
NEXT_RUN_ID = "run125A_stage125_v41_route_supply_followup_review_after_stage124_v1"
NEXT_PACKET_ID = "stage125_v41_route_supply_followup_review_after_stage124_v1"
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
COMMON_ROOT = f"OPV2/s124a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage124_route_supply_density_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage124_route_supply_density_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage124_route_supply_density_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage124_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage124_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage124_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage124_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage124_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage124_trade_audit.csv"
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
STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
}
STAGE122_SOURCE = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.75,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s124_v41_h3_cd5_shortgate_risk035_sht54_lng52",
        label="stage124_cd5_shortgate_short54_long52",
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
        max_hold_bars=3,
        notes="Stage124 route supply repair: block weak short route only under risk035.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s124_v41_h3_cd5_longgate_risk035_sht54_lng52",
        label="stage124_cd5_longgate_short54_long52",
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
        max_hold_bars=3,
        notes="Stage124 route supply repair: block weak long route only under risk035.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s124_v41_h3_cd5_nogate_risk035_sht55_lng53",
        label="stage124_cd5_nogate_short55_long53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage124 route supply repair: no side block with tighter thresholds under risk035.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s124_v41_h3_cd5_nogate_risk035_sht54_lng52",
        label="stage124_cd5_nogate_short54_long52",
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
        max_hold_bars=3,
        notes="Stage124 route supply repair: raw no side block under Stage122 thresholds.",
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
    "s124_v41_h3_cd5_shortgate_risk035_sht54_lng52": {
        "gate_column": "stage124_gate_short_only_cd5_sht54_lng52",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Release long route supply while blocking weak short only.",
    },
    "s124_v41_h3_cd5_longgate_risk035_sht54_lng52": {
        "gate_column": "stage124_gate_long_only_cd5_sht54_lng52",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "long",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Release short route supply while blocking weak long only.",
    },
    "s124_v41_h3_cd5_nogate_risk035_sht55_lng53": {
        "gate_column": "stage124_gate_no_block_cd5_sht55_lng53",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "none",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "No side block; tighter thresholds damp supply damage.",
    },
    "s124_v41_h3_cd5_nogate_risk035_sht54_lng52": {
        "gate_column": "stage124_gate_no_block_cd5_sht54_lng52",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "none",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "No side block at the Stage122 threshold surface.",
    },
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s122.as_float(row, key, default)


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE122_SOURCE if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


def stage124_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
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
                magic = 12410000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=124,
                        exploration_label="stage124_BaselineAdapter__RouteSupplyDensityRepairAfterSmallGain",
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
                        extra_set_values=stage124_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage124(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in s122.s120.routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        early = s122.s120.early_segment(segment_rows, adapter_id)
        trades = as_float(row, "trade_count")
        pf = as_float(row, "profit_factor")
        net = as_float(row, "net_profit")
        dd = as_float(row, "max_drawdown_percent", 99.0)
        gain = trades - STAGE122_SOURCE["trade_count"]
        candidates.append(
            (
                gain >= 20 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= 16.0,
                gain > 0 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= STAGE110_REFERENCE["oos_dd_pct"],
                gain,
                pf,
                net,
                -dd,
                as_float(early, "profit_factor"),
                row,
            )
        )
    return max(candidates, key=lambda item: item[:7])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_route_supply_runtime_repair_in_stage125_due_to_incomplete_runtime"
    best = best_stage124(summary_rows, segment_rows)
    trades = as_float(best, "trade_count")
    gain = trades - STAGE122_SOURCE["trade_count"]
    pf_ok = as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
    net_ok = as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
    dd = as_float(best, "max_drawdown_percent", 99.0)
    if gain >= 20 and pf_ok and net_ok and dd <= 16.0:
        return "continue_route_supply_followup_review_in_stage125_with_material_density_gain"
    if gain > 0 and pf_ok and net_ok and dd <= STAGE110_REFERENCE["oos_dd_pct"]:
        return "continue_route_supply_followup_review_in_stage125_with_small_or_fragile_gain"
    return "continue_route_supply_followup_review_in_stage125_due_to_damage_or_no_gain"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | gate(게이트) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | gain vs Stage122(증가) | early PF(초반 수익 팩터) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in s122.s120.routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        early = s122.s120.early_segment(segment_rows, adapter_id)
        gate = CONTEXT_GATE_SPECS.get(adapter_id, {}).get("block_mode", "")
        trades = as_float(row, "trade_count")
        lines.append(
            "| {adapter} | {gate} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} | {early_pf:.6f} |".format(
                adapter=adapter_id,
                gate=gate,
                pf=as_float(row, "profit_factor"),
                net=as_float(row, "net_profit"),
                dd=as_float(row, "max_drawdown_percent"),
                trades=trades,
                gain=trades - STAGE122_SOURCE["trade_count"],
                early_pf=as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage124(summary_rows, segment_rows)
    trade_gain = as_float(best, "trade_count") - STAGE122_SOURCE["trade_count"]
    return f"""# Stage124 Route Supply Density Repair Report(124단계 경로 공급 밀도 수리 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE123_ID}`
- source_stage123_closeout_commit(원천 123단계 종료 커밋): `{SOURCE_STAGE123_CLOSEOUT_COMMIT}`
- source_stage123_latest_commit(원천 123단계 최신 커밋): `{SOURCE_STAGE123_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage122(122단계)의 risk035 ATR bracket(위험 3.5% ATR 괄호)과 모델 위험 제어(model risk control, 모델 위험 제어)를 유지하면서 side gate(방향 게이트)를 풀거나 좁혀 trade count(거래 수)를 의미 있게 늘릴 수 있는가?

Effect(효과): threshold/cooldown-only easing(임계값/대기시간만 푸는 방식)이 작게 끝났기 때문에, 이번 단계는 route supply/lifecycle source(경로 공급/생애주기 원천)만 좁게 본다.

## Result Table(결과표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- oos_pf(표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(표본외 손실률): `{as_float(best, "max_drawdown_percent"):.2f}`
- trades(거래 수): `{as_float(best, "trade_count"):.0f}`
- trade_gain_vs_stage122_source(Stage122 원천 대비 거래 증가): `{trade_gain:.0f}`
- trade_count_gap_to_34d(34D 거래 수 차이): `{as_float(best, "trade_count") - LEGACY_34D["trade_count"]:.0f}`
- dd_gap_to_34d(34D 손실률 차이): `{as_float(best, "max_drawdown_percent") - LEGACY_34D["max_drawdown_percent"]:.2f}`

## Judgment(판정)

- result_subject(판정 대상): Stage124 route supply density repair(124단계 경로 공급 밀도 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage125(125단계) 후속 검토 전까지 route supply gain(경로 공급 증가)의 안정성, 월별 분포, equity shape(자본 곡선 모양)는 최종 판정하지 않는다.
- judgment_label(판정 라벨): `route_supply_repair_measured_not_final`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage124 Decision(124단계 판정)

decision(판정): `{decision}`

Stage124(124단계)는 Stage123(123단계) 판정대로 threshold/cooldown(임계값/대기시간)보다 route supply(경로 공급)를 좁게 시험했다.

Effect(효과): 결과를 Stage125(125단계) follow-up review(후속 검토)로 넘겨 거래 수 증가가 PF/net/DD(수익 팩터/순손익/손실률)를 망가뜨렸는지 다시 판독한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 핵심 성과 지표 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage123_closeout_commit(원천 123단계 종료 커밋): `{SOURCE_STAGE123_CLOSEOUT_COMMIT}`
- source_stage123_latest_commit(원천 123단계 최신 커밋): `{SOURCE_STAGE123_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage124(124단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research/development(브이투 고유 연구개발)는 Stage125(125단계)로 이어진다.
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
        if s122.path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage124_route_supply_density_repair_evidence",
                    "path": rel(path),
                    "sha256": s122.sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage124 v2-native route supply density repair artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if raw_path and s122.path_exists(Path(str(raw_path))):
            path = Path(str(raw_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": s122.sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage124 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = s122.upsert_csv_rows(
        RUN_REGISTRY_PATH,
        s122.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_route_supply_density_repair_after_small_gain",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": s122.ledger_pairs(
                    (
                        ("source_stage123_closeout_commit", SOURCE_STAGE123_CLOSEOUT_COMMIT),
                        ("source_stage123_latest_commit", SOURCE_STAGE123_LATEST_COMMIT),
                        ("source_stage122_latest_commit", SOURCE_STAGE122_LATEST_COMMIT),
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
    alpha_payload = s122.upsert_csv_rows(PROJECT_LEDGER_PATH, s122.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = s122.upsert_csv_rows(STAGE_LEDGER_PATH, s122.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = s122.upsert_csv_rows(
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_route_supply_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage124 isolates Tier A route supply repair before Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s108.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment_design", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-artifact-lineage"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"], "status": status})
    s108.write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "claim_boundary": BOUNDARY})
    s108.write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "judgment_label": "route_supply_repair_measured_not_final", "legacy_relation": "lesson_only_target_surface_no_code_copy", "overall_goal_complete": False})
    s108.write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage123_closeout_commit": SOURCE_STAGE123_CLOSEOUT_COMMIT, "source_stage123_latest_commit": SOURCE_STAGE123_LATEST_COMMIT, "source_stage122_latest_commit": SOURCE_STAGE122_LATEST_COMMIT, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage(decision: str, external: str) -> None:
    s108.write_md(NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage125(125단계)는 Stage124(124단계)의 route supply density repair(경로 공급 밀도 수리) 결과를 후속 검토한다.

## Bounded Question(경계 질문)

Stage124(124단계)의 거래 수 증가가 PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), equity shape(자본 곡선 모양)를 보존했는가?

Effect(효과): Stage125(125단계)는 새 실험을 벌리지 않고 Stage124 evidence(근거)를 읽어 다음 bounded repair(경계 수리)를 정한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage125 Input References(125단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage124_report(124단계 보고서): `{rel(REPORT_PATH)}`
- stage124_summary(124단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage125 Review Index(125단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
""")
    s108.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage125 Selection Status(125단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")


def update_current_truth(decision: str, external: str) -> None:
    text = s122.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage124(124단계) closed(종료) as `{decision}` and Stage125(125단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): route supply(경로 공급) 결과를 후속 검토로 넘겨 34D trade count(34D 거래 수) 격차를 계속 줄인다.
- >-
  Stage124 result(124단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록했다. Effect(효과): 거래 수 증가가 PF/net/DD(수익 팩터/순손익/손실률)를 보존했는지 Stage125(125단계)에서 다시 판독한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage124_v41_route_supply_density_repair_after_small_gain:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage123_closeout_commit: {SOURCE_STAGE123_CLOSEOUT_COMMIT}
  source_stage123_latest_commit: {SOURCE_STAGE123_LATEST_COMMIT}
  source_stage122_latest_commit: {SOURCE_STAGE122_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage124_v41_route_supply_density_repair_after_small_gain:"
    if marker in text:
        text = re.sub(r"\nstage124_v41_route_supply_density_repair_after_small_gain:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    s122.io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    s108.write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage124 Selection Status(124단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE123_ID}`
- source_decision(원천 판정): `continue_route_supply_density_repair_in_stage124_due_to_small_gain`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage124_decision(124단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    s108.write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage124 Review Index(124단계 검토 색인)

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
- adapter_under_review(검토 중 어댑터): `stage125_route_supply_followup_review_surface`
- status(상태): `stage124_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage124(124단계) closed(종료) as v2-native v41 route supply density repair(브이투 고유 브이41 경로 공급 밀도 수리). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage125(125단계) route supply follow-up review(경로 공급 후속 검토)로 이어진다.

## Latest Stage124 Evidence(최신 124단계 근거)

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
        "\n## 2026-05-18 - Stage124 v41 route supply density repair closeout(124단계 v41 경로 공급 밀도 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage122 risk035 ATR bracket(위험 3.5% ATR 괄호)을 유지한 채 side gate(방향 게이트) 경로 공급을 측정하고 Stage125(125단계) 후속 검토로 넘겼다.\n"
    )
    existing = s122.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s122.path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        s122.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def configure_stage124() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE121_ID": SOURCE_STAGE123_ID,
        "SOURCE_STAGE121_CLOSEOUT_COMMIT": SOURCE_STAGE123_CLOSEOUT_COMMIT,
        "SOURCE_STAGE121_LATEST_COMMIT": SOURCE_STAGE123_LATEST_COMMIT,
        "SOURCE_STAGE120_CLOSEOUT_COMMIT": SOURCE_STAGE123_CLOSEOUT_COMMIT,
        "SOURCE_STAGE120_LATEST_COMMIT": SOURCE_STAGE122_LATEST_COMMIT,
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
        "STAGE118_GUARDRAILS": {SOURCE_ADAPTER_ID: STAGE122_SOURCE},
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }.items():
        setattr(s122, name, value)
    s122.build_attempts = build_attempts
    s122.source_baseline = source_baseline
    s122.best_stage122 = best_stage124
    s122.decide = decide
    s122.row_table = row_table
    s122.report_markdown = report_markdown
    s122.decision_markdown = decision_markdown
    s122.artifact_rows = artifact_rows
    s122.write_ledgers = write_ledgers
    s122.tier_b_rows = tier_b_rows
    s122.write_packet_files = write_packet_files
    s122.update_current_truth = update_current_truth
    s122.append_changelog = append_changelog
    s122.configure_stage122()


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage124()
    return s122.s120.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

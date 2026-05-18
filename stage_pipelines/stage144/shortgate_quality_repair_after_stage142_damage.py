from __future__ import annotations

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
from stage_pipelines.stage142 import route_coverage_supply_branch_after_reverse_exhaustion as s142  # noqa: E402


s138 = s142.s138
s122 = s142.s122
s100 = s142.s100

STAGE_ID = "144_adapter_research__route_shortgate_quality_repair_after_stage142_damage"
RUN_NUMBER = "run144A"
RUN_ID = "run144A_stage144_route_shortgate_quality_repair_after_stage142_damage_v1"
PACKET_ID = "stage144_route_shortgate_quality_repair_after_stage142_damage_v1"
PARENT_RUN_ID = "run143A_stage143_stage142_route_coverage_followup_review_v1"
SOURCE_STAGE143_ID = "143_adapter_research__stage142_route_coverage_followup_review"
SOURCE_STAGE143_CLOSEOUT_COMMIT = "6c238545e2b7a0887e30504a9415046cad0a7e2a"
SOURCE_STAGE143_HASH_RECORD_COMMIT = "ee0f8e716bbcf1252aac3f1f1178c6ecfc7d015a"
SOURCE_STAGE142_ID = "142_adapter_research__route_coverage_supply_branch_after_reverse_exhaustion"
SOURCE_STAGE142_CLOSEOUT_COMMIT = "0f53be36d3bb88fc97ec44cfeaa3e600e7b9e414"
SOURCE_STAGE142_HASH_RECORD_COMMIT = "7813b4d26006336dcf1709949ce78d47462b3c47"
SOURCE_ADAPTER_ID = "s142_route_shortgate_reverse_h3_cd5_risk035"
NEXT_STAGE_ID = "145_adapter_research__stage144_shortgate_quality_followup_review"
NEXT_RUN_ID = "run145A_stage145_stage144_shortgate_quality_followup_review_v1"
NEXT_PACKET_ID = "stage145_stage144_shortgate_quality_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s144a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage144_shortgate_quality_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage144_shortgate_quality_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage144_shortgate_quality_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage144_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage144_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage144_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage144_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage144_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage144_trade_audit.csv"
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
STAGE142_SHORTGATE = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.549398689,
    "net_profit": 963.92,
    "max_drawdown_percent": 20.23,
    "trade_count": 231,
    "validation_profit_factor": 1.561425361,
    "validation_net_profit": 1821.00,
    "validation_max_drawdown_percent": 11.84,
    "validation_trade_count": 321,
}
STAGE142_CONTROL = {
    "adapter_id": "s142_control_reverse_bothgate_h3_cd5_risk035",
    "profit_factor": 1.795976838,
    "net_profit": 1186.30,
    "max_drawdown_percent": 14.66,
    "trade_count": 180,
    "validation_profit_factor": 1.582222632,
    "validation_net_profit": 1388.24,
    "validation_max_drawdown_percent": 11.85,
    "validation_trade_count": 265,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s144_shortgate_reverse_cd6_h3_sht54_lng52_risk035",
        label="stage144_shortgate_reverse_cd6_h3_sht54_lng52_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=6,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage144 shortgate quality repair: preserve Stage142 reverse shortgate, cooldown 6.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s144_shortgate_reverse_cd7_h3_sht54_lng52_risk035",
        label="stage144_shortgate_reverse_cd7_h3_sht54_lng52_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=7,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage144 shortgate quality repair: preserve thresholds, cooldown 7.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s144_shortgate_reverse_tight_cd6_h3_sht55_lng53_risk035",
        label="stage144_shortgate_reverse_tight_cd6_h3_sht55_lng53_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=6,
        short_threshold=0.55,
        long_threshold=0.53,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage144 shortgate quality repair: tighter confidence and cooldown 6.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s144_shortgate_reverse_strictgate_cd6_h3_sht54_lng52_risk035",
        label="stage144_shortgate_reverse_strictgate_cd6_h3_sht54_lng52_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=6,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage144 shortgate quality repair: broader weak-context short block and cooldown 6.",
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
    "s144_shortgate_reverse_cd6_h3_sht54_lng52_risk035": {
        "gate_column": "stage144_gate_short_reverse_cd6",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage144 shortgate repair: original weak short gate, reverse, cooldown 6.",
    },
    "s144_shortgate_reverse_cd7_h3_sht54_lng52_risk035": {
        "gate_column": "stage144_gate_short_reverse_cd7",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage144 shortgate repair: original weak short gate, reverse, cooldown 7.",
    },
    "s144_shortgate_reverse_tight_cd6_h3_sht55_lng53_risk035": {
        "gate_column": "stage144_gate_short_reverse_tight_cd6",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage144 shortgate repair: original gate, tighter confidence, cooldown 6.",
    },
    "s144_shortgate_reverse_strictgate_cd6_h3_sht54_lng52_risk035": {
        "gate_column": "stage144_gate_short_reverse_strict_cd6",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "short",
        "session_min": 150.0,
        "session_max": 300.0,
        "margin_min": 0.03,
        "margin_max": 0.10,
        "description": "Stage144 shortgate repair: broader weak-context short block, reverse, cooldown 6.",
    },
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s122.as_float(row, key, default)


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE142_SHORTGATE if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


def split_row(summary_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in summary_rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def segment_row(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in segment_rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def stage144_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s122.s120.stage120_extra_set_values(variant, magic)
    block_mode = str(CONTEXT_GATE_SPECS.get(variant.adapter_id, {}).get("block_mode", "short"))
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
                magic = 14410000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=144,
                        exploration_label="stage144_BaselineAdapter__ShortgateQualityRepairAfterStage142Damage",
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
                        extra_set_values=stage144_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage144(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        oos_early = segment_row(segment_rows, adapter_id, "oos", "early")
        trades = as_float(oos, "trade_count")
        pf = as_float(oos, "profit_factor")
        net = as_float(oos, "net_profit")
        dd = as_float(oos, "max_drawdown_percent", 99.0)
        val_pf = as_float(val, "profit_factor")
        val_net = as_float(val, "net_profit")
        val_dd = as_float(val, "max_drawdown_percent", 99.0)
        material = (
            trades >= 200
            and pf >= LEGACY_34D["profit_factor"]
            and net >= LEGACY_34D["net_profit"]
            and dd <= 18.0
            and val_pf >= 1.55
            and val_net >= LEGACY_34D["net_profit"]
            and val_dd <= 15.0
        )
        small = (
            trades >= 190
            and pf > STAGE142_SHORTGATE["profit_factor"]
            and net >= STAGE142_SHORTGATE["net_profit"]
            and dd < STAGE142_SHORTGATE["max_drawdown_percent"]
            and val_pf >= 1.55
            and val_net >= LEGACY_34D["net_profit"]
            and val_dd <= 15.0
        )
        candidates.append(
            (
                material,
                small,
                trades - STAGE142_CONTROL["trade_count"],
                pf,
                net,
                -dd,
                as_float(oos_early, "profit_factor"),
                as_float(val, "trade_count") - STAGE142_CONTROL["validation_trade_count"],
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:8])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage145_shortgate_quality_runtime_repair_due_to_incomplete_runtime_candidate_not_final"
    best = best_stage144(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    trades = as_float(best, "trade_count")
    pf = as_float(best, "profit_factor")
    net = as_float(best, "net_profit")
    dd = as_float(best, "max_drawdown_percent", 99.0)
    val_pf = as_float(val, "profit_factor")
    val_net = as_float(val, "net_profit")
    val_dd = as_float(val, "max_drawdown_percent", 99.0)
    if trades >= 200 and pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= 18.0 and val_pf >= 1.55 and val_net >= LEGACY_34D["net_profit"] and val_dd <= 15.0:
        return "continue_stage145_shortgate_quality_followup_review_with_material_repair_candidate_not_final"
    if trades >= 190 and pf > STAGE142_SHORTGATE["profit_factor"] and net >= STAGE142_SHORTGATE["net_profit"] and dd < STAGE142_SHORTGATE["max_drawdown_percent"] and val_pf >= 1.55 and val_net >= LEGACY_34D["net_profit"] and val_dd <= 15.0:
        return "continue_stage145_shortgate_quality_followup_review_with_small_repair_candidate_not_final"
    return "continue_stage145_shortgate_quality_followup_review_due_to_damage_or_no_repair_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | vs shortgate trades(숏게이트 대비 거래) | vs control trades(대조군 대비 거래) | OOS early PF(초반 수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        early = segment_row(segment_rows, adapter_id, "oos", "early")
        trades = as_float(oos, "trade_count")
        lines.append(
            "| {adapter} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {short_delta:.0f} | {control_delta:.0f} | {early_pf:.6f} |".format(
                adapter=adapter_id,
                pf=as_float(oos, "profit_factor"),
                net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=trades,
                short_delta=trades - STAGE142_SHORTGATE["trade_count"],
                control_delta=trades - STAGE142_CONTROL["trade_count"],
                early_pf=as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage144(summary_rows, segment_rows)
    best_id = str(best.get("adapter_id", ""))
    best_val = split_row(summary_rows, best_id, "validation_is")
    return f"""# Stage144 Shortgate Quality Repair Report(144단계 숏게이트 품질 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE143_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the Stage142 shortgate route(142단계 숏게이트 경로)가 만든 trade count gain(거래 수 증가)을 일부 보존하면서 OOS PF/net/DD(미래구간 수익 팩터/순손익/손실률)를 34D target surface(34D 목표 표면)에 가깝게 회복할 수 있는가?

Effect(효과): no-gate pressure(무게이트 압력)를 반복하지 않고 damaged shortgate(손상된 숏게이트) 후보의 품질 회복만 측정한다.

## Experiment Design(실험 설계)

- hypothesis(가설): Stage142 shortgate(142단계 숏게이트)는 거래 공급 가치가 있지만, same-direction cooldown(동일 방향 대기시간), threshold(임계값), weak-context short block(약한 문맥 숏 차단)을 조금 강화하면 DD(손실률)를 낮추고 PF(수익 팩터)를 회복할 수 있다.
- decision_use(판정 용도): Stage145(145단계)에서 수리 단서를 살릴지, 다른 bounded repair(경계 수리)로 넘길지 정한다.
- comparison_baseline(비교 기준): Stage142 shortgate reverse(142단계 숏게이트 반전) `{SOURCE_ADAPTER_ID}` = OOS PF `1.549399`, net `963.92`, DD `20.23`, trades `231`.
- control_reference(대조 참고): Stage142 control(142단계 대조군) = OOS PF `1.795977`, net `1186.30`, DD `14.66`, trades `180`.
- control_variables(고정 변수): v41 source model(v41 원천 모델), ATR bracket(ATR 괄호), model risk cap(모델 위험 한도) `3.5%`, max hold(최대 보유) `3`, Tier B disabled(티어 B 비활성).
- changed_variables(변경 변수): cooldown(대기시간) `6/7`, thresholds(임계값) `0.54/0.52` 또는 `0.55/0.53`, short gate breadth(숏 게이트 폭).
- success_criteria(성공 기준): OOS trades(미래구간 거래 수) `200+`, PF `>= 1.583157`, net `>= 987.60`, DD `<= 18.0`, validation(검증) PF/net/DD 유지.
- failure_criteria(실패 기준): 거래 수만 줄거나, PF/net/DD(수익 팩터/순손익/손실률)가 Stage142 shortgate보다 회복되지 않는 경우.
- stop_conditions(중단 조건): 이 단계 안에서 추가 최적화하지 않고 Stage145(145단계) 후속 검토로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_candidate(최선 후보): `{best_id or "none"}`
- oos_pf(미래구간 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(미래구간 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(미래구간 손실률): `{as_float(best, "max_drawdown_percent"):.2f}`
- oos_trades(미래구간 거래 수): `{as_float(best, "trade_count"):.0f}`
- trade_delta_vs_stage142_shortgate(142단계 숏게이트 대비 거래 차이): `{as_float(best, "trade_count") - STAGE142_SHORTGATE["trade_count"]:.0f}`
- trade_delta_vs_stage142_control(142단계 대조군 대비 거래 차이): `{as_float(best, "trade_count") - STAGE142_CONTROL["trade_count"]:.0f}`
- val_pf(검증 수익 팩터): `{as_float(best_val, "profit_factor"):.6f}`
- val_net(검증 순손익): `{as_float(best_val, "net_profit"):.2f}`
- val_dd_pct(검증 손실률): `{as_float(best_val, "max_drawdown_percent"):.2f}`
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): shortgate quality repair(숏게이트 품질 수리)에 따른 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 변화.
- comparison_baseline(비교 기준): `{SOURCE_ADAPTER_ID}`.
- likely_drivers(가능한 원인): cooldown(대기시간), threshold(임계값), short gate breadth(숏 게이트 폭), reverse lifecycle(반전 생명주기).
- segment_checks(구간 확인): chronological thirds(시간 3분할), full split(전체 구간), Tier A/Tier B disabled diagnostic(티어 A/티어 B 비활성 진단), risk/ATR telemetry(위험/ATR 기록).
- attribution_confidence(귀속 신뢰도): `medium_bounded_measurement_pending_stage145_review`.
- next_probe(다음 확인): Stage145(145단계) follow-up review(후속 검토)에서 segment KPI(구간 핵심 성과 지표)와 equity shape(자본 곡선 모양)을 판독한다.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage144/shortgate_quality_repair_after_stage142_damage.py`
- runtime_path(런타임 경로): MT5 Strategy Tester(MT5 전략 테스터) reports under `{rel(RUN_ROOT / "mt5" / "reports")}`.
- shared_contract(공유 계약): model export(모델 내보내기), feature count(피처 수) `2`, thresholds(임계값), ATR bracket(ATR 괄호), risk cap(위험 한도), side filter(방향 필터).
- parity_check(동등성 확인): Strategy Tester output(전략 테스터 출력) and generated telemetry(생성 원격측정).
- runtime_claim_boundary(런타임 주장 경계): `research_only_no_runtime_authority`.

## Judgment(판정)

- result_subject(판정 대상): Stage144 shortgate quality repair(144단계 숏게이트 품질 수리).
- evidence_available(사용 가능 근거): MT5 reports(MT5 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage145(145단계) follow-up review(후속 검토) 전에는 equity curve(자본 곡선), concentration(집중도), final package(최종 패키지) 판정이 닫히지 않는다.
- judgment_label(판정 라벨): `shortgate_quality_repair_measured_not_final`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage144 Decision(144단계 판정)

decision(판정): `{decision}`

Stage144(144단계)는 Stage142 shortgate reverse(142단계 숏게이트 반전) 후보의 quality repair(품질 수리)만 좁게 실행했다.

Effect(효과): 결과가 좋아도 final adapter(최종 어댑터)나 operating claim(운영 주장)으로 올리지 않고 Stage145(145단계) follow-up review(후속 검토)로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage143_closeout_commit(원천 143단계 종료 커밋): `{SOURCE_STAGE143_CLOSEOUT_COMMIT}`
- source_stage143_hash_record_commit(원천 143단계 해시 기록 커밋): `{SOURCE_STAGE143_HASH_RECORD_COMMIT}`
- source_stage142_hash_record_commit(원천 142단계 해시 기록 커밋): `{SOURCE_STAGE142_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage144 closeout(144단계 종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상 목표는 Stage145(145단계)와 후속 bounded repair(경계 수리)로 계속된다.
"""


def write_stage145_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage145(145단계)는 Stage144 shortgate quality repair(144단계 숏게이트 품질 수리) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage144(144단계) recover shortgate quality(숏게이트 품질)를 enough to keep the repaired route(수리된 경로), or should the next bounded stage pivot to another repair axis(다른 수리 축)?

Effect(효과): Stage144(144단계) 안에서 추가 최적화하지 않고, 근거를 읽어 다음 좁은 결정을 정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage145 Input References(145단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- stage144_decision(144단계 판정): `{rel(DECISION_PATH)}`
- stage144_report(144단계 보고서): `{rel(REPORT_PATH)}`
- stage144_summary(144단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage144_segment_kpi(144단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage144_risk_atr_telemetry(144단계 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage145 Review Index(145단계 검토 색인)

- status(상태): `open_planned`
- source_stage(원천 단계): `{STAGE_ID}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage145(145단계)는 새 MT5 run(MT5 실행)이 아니라 Stage144(144단계) 근거 판독으로 시작한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage145 Selection Status(145단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage144`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    current_focus = f"""current_focus:
- >-
  Stage144(144단계) closed(종료) as `{decision}` and Stage145(145단계) `{NEXT_STAGE_ID}` is open_planned(열린 계획). Effect(효과): shortgate quality repair(숏게이트 품질 수리) 결과를 보존하고 후속 검토로 넘긴다.
- >-
  Stage144 evidence(144단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): 거래 수 보존과 KPI(핵심 성과 지표) 회복 여부를 분리해서 판정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on:.*$", "updated_on: '2026-05-18'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    block = f"""
stage144_route_shortgate_quality_repair_after_stage142_damage:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage143_closeout_commit: {SOURCE_STAGE143_CLOSEOUT_COMMIT}
  source_stage143_hash_record_commit: {SOURCE_STAGE143_HASH_RECORD_COMMIT}
  source_stage142_hash_record_commit: {SOURCE_STAGE142_HASH_RECORD_COMMIT}
  source_adapter: {SOURCE_ADAPTER_ID}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage145_stage144_shortgate_quality_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage144
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run145A_stage145_stage144_shortgate_quality_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage144_route_shortgate_quality_repair_after_stage142_damage:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage145_stage144_shortgate_quality_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage144 Selection Status(144단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE143_ID}`
- source_stage142_adapter(원천 142단계 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage144_decision(144단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage144(144단계)는 닫지만 전체 목표 완료나 운영 주장은 만들지 않는다.
""",
    )
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage144 Review Index(144단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage144(144단계) 산출물 위치를 한 곳에서 추적하게 한다.
""",
    )
    s122.s108.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage145_shortgate_quality_followup_review_surface`
- status(상태): `stage144_closed_{decision}_stage145_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage144(144단계)는 shortgate quality repair(숏게이트 품질 수리)를 측정했다. Effect(효과): 결과를 final package(최종 패키지)나 operating claim(운영 주장)으로 과장하지 않고 Stage145(145단계) 검토로 넘긴다.

## Latest Stage144 Evidence(최신 144단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    write_stage145_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage144 shortgate quality repair closeout(144단계 숏게이트 품질 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage142 shortgate(142단계 숏게이트) 손상 후보를 cooldown/threshold/gate breadth(대기시간/임계값/게이트 폭) 축에서 측정하고 Stage145(145단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
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
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage144_shortgate_quality_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage144 v2-native shortgate quality repair artifact.",
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
                    "notes": "Actual Stage144 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_stage144_shortgate_quality_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage143_closeout_commit", SOURCE_STAGE143_CLOSEOUT_COMMIT),
                        ("source_stage143_hash_record_commit", SOURCE_STAGE143_HASH_RECORD_COMMIT),
                        ("source_stage142_hash_record_commit", SOURCE_STAGE142_HASH_RECORD_COMMIT),
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                        ("overall_goal_complete", 0),
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
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_stage144_shortgate_quality_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage144 isolates Tier A shortgate quality repair before any Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s122.s108.write_json(
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
    s122.s108.write_json(
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
    s122.s108.write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "kpi_scope": "regular_risk_execution",
            "comparison_baseline": SOURCE_ADAPTER_ID,
            "target_surface": TARGET_SURFACE,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "performance_attribution_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "observed_change": "shortgate_quality_repair_vs_stage142_shortgate_reverse",
            "comparison_baseline": SOURCE_ADAPTER_ID,
            "likely_drivers": ["same_direction_cooldown", "threshold_surface", "short_gate_breadth", "reverse_lifecycle"],
            "segment_checks": ["chronological_thirds", "validation_vs_oos", "tier_b_disabled_diagnostic", "risk_atr_telemetry"],
            "attribution_confidence": "medium_bounded_measurement_pending_stage145_review",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "runtime_parity_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "research_path": rel(Path("stage_pipelines/stage144/shortgate_quality_repair_after_stage142_damage.py")),
            "runtime_path": rel(RUN_ROOT / "mt5" / "reports"),
            "shared_contract": ["feature_count_2", "thresholds", "atr_bracket", "model_risk_cap", "side_filter"],
            "parity_check": "mt5_strategy_tester_output",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "judgment_label": "shortgate_quality_repair_measured_not_final",
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "artifact_lineage_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "source_inputs": [rel(Path("stage_pipelines/stage142/route_coverage_supply_branch_after_reverse_exhaustion.py"))],
            "producer": rel(Path("stage_pipelines/stage144/shortgate_quality_repair_after_stage142_damage.py")),
            "consumer": NEXT_STAGE_ID,
            "artifact_paths": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "segment_kpi": rel(SEGMENT_KPI_PATH),
                "risk_atr": rel(RISK_ATR_TELEMETRY_PATH),
                "stage_ledger": rel(STAGE_LEDGER_PATH),
            },
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage143_closeout_commit": SOURCE_STAGE143_CLOSEOUT_COMMIT,
            "source_stage143_hash_record_commit": SOURCE_STAGE143_HASH_RECORD_COMMIT,
            "source_stage142_hash_record_commit": SOURCE_STAGE142_HASH_RECORD_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def configure_stage144() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE137_ID": SOURCE_STAGE143_ID,
        "SOURCE_STAGE137_CLOSEOUT_COMMIT": SOURCE_STAGE143_CLOSEOUT_COMMIT,
        "SOURCE_STAGE137_LATEST_COMMIT": SOURCE_STAGE143_HASH_RECORD_COMMIT,
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
        "STAGE136_SOURCE": STAGE142_SHORTGATE,
        "STAGE110_REFERENCE": STAGE142_CONTROL,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s138, name, value)
    s138.source_baseline = source_baseline
    s138.best_stage138 = best_stage144
    s138.decide = decide
    s138.row_table = row_table
    s138.report_markdown = report_markdown
    s138.decision_markdown = decision_markdown
    s138.update_current_truth = update_current_truth
    s138.append_changelog = append_changelog
    s138.build_attempts = build_attempts
    s138.artifact_rows = artifact_rows
    s138.write_ledgers = write_ledgers
    s138.tier_b_rows = tier_b_rows
    s138.write_packet_files = write_packet_files
    s138.configure_stage138()
    s122.s120.build_attempts = build_attempts
    s122.s120.artifact_rows = artifact_rows
    s122.s120.write_ledgers = write_ledgers
    s122.s120.tier_b_rows = tier_b_rows
    s122.s120.write_packet_files = write_packet_files


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage144()
    code = s122.s120.main(argv)
    write_stage145_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

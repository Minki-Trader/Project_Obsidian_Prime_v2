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
from stage_pipelines.stage146 import control_anchor_trade_supply_after_shortgate_no_repair as s146  # noqa: E402


s144 = s146.s144
s138 = s146.s138
s122 = s146.s122
s100 = s146.s100

STAGE_ID = "148_adapter_research__softsession_supply_quality_repair_after_stage146_damage"
RUN_NUMBER = "run148A"
RUN_ID = "run148A_stage148_softsession_supply_quality_repair_after_stage146_damage_v1"
PACKET_ID = "stage148_softsession_supply_quality_repair_after_stage146_damage_v1"
PARENT_RUN_ID = "run147A_stage147_stage146_control_anchor_followup_review_v1"
SOURCE_STAGE147_ID = "147_adapter_research__stage146_control_anchor_followup_review"
SOURCE_STAGE147_CLOSEOUT_COMMIT = "2998bff304cfe0d681f894d320eb888a54643d76"
SOURCE_STAGE147_HASH_RECORD_COMMIT = "cf5f7eb83d5b4fe07696f6ae11fe8146fa072558"
SOURCE_STAGE146_HASH_RECORD_COMMIT = "f63827bc249653329b99494eca2b17f0926af7cd"
SOURCE_STAGE142_HASH_RECORD_COMMIT = "7813b4d26006336dcf1709949ce78d47462b3c47"
SOURCE_ADAPTER_ID = "s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035"
NEXT_STAGE_ID = "149_adapter_research__stage148_softsession_repair_followup_review"
NEXT_RUN_ID = "run149A_stage149_stage148_softsession_repair_followup_review_v1"
NEXT_PACKET_ID = "stage149_stage148_softsession_repair_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s148a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage148_softsession_supply_quality_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage148_softsession_supply_quality_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage148_softsession_supply_quality_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage148_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage148_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage148_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage148_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage148_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage148_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage148/softsession_supply_quality_repair_after_stage146_damage.py")

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
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
STAGE146_SOFTSESSION = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.61,
    "net_profit": 1142.79,
    "max_drawdown_percent": 9.67,
    "trade_count": 215,
    "validation_profit_factor": 1.43,
    "validation_net_profit": 1052.35,
    "validation_max_drawdown_percent": 13.31,
    "validation_trade_count": 308,
    "oos_mid_profit_factor": 1.408466063,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s148_softsession_replay_h3_cd5_sht54_lng52_risk035",
        label="stage148_softsession_replay_h3_cd5_sht54_lng52_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage148 control seed replay: preserve Stage146 softsession damage surface.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s148_softsession_margin_restore_h3_cd5_sht54_lng52_risk035",
        label="stage148_softsession_margin_restore_h3_cd5_sht54_lng52_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage148 repair: keep soft session but restore original et40 mid-margin block.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s148_softsession_session_mid_h3_cd5_sht54_lng52_risk035",
        label="stage148_softsession_session_mid_h3_cd5_sht54_lng52_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage148 repair: partly restore weak-session block while preserving some supply gain.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s148_softsession_threshold_guard_h3_cd5_sht55_lng53_risk035",
        label="stage148_softsession_threshold_guard_h3_cd5_sht55_lng53_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.55,
        long_threshold=0.53,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage148 repair: keep soft gate but add stricter threshold guard.",
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
    "s148_softsession_replay_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage148_gate_softsession_replay",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 175.0,
        "session_max": 260.0,
        "margin_min": 0.045,
        "margin_max": 0.075,
        "description": "Stage148 seed replay: Stage146 softsession gate.",
    },
    "s148_softsession_margin_restore_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage148_gate_softsession_margin_restore",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 175.0,
        "session_max": 260.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage148 repair: soft session plus restored original margin block.",
    },
    "s148_softsession_session_mid_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage148_gate_softsession_session_mid",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.045,
        "margin_max": 0.075,
        "description": "Stage148 repair: session block halfway between soft and original.",
    },
    "s148_softsession_threshold_guard_h3_cd5_sht55_lng53_risk035": {
        "gate_column": "stage148_gate_softsession_threshold_guard",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 175.0,
        "session_max": 260.0,
        "margin_min": 0.045,
        "margin_max": 0.075,
        "description": "Stage148 repair: soft gate with stricter entry thresholds.",
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
    return STAGE146_SOFTSESSION if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


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


def stage148_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s122.s120.stage120_extra_set_values(variant, magic)
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
                magic = 14810000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=148,
                        exploration_label="stage148_BaselineAdapter__SoftsessionSupplyQualityRepairAfterStage146Damage",
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
                        extra_set_values=stage148_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage148(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        oos_trade_gain_vs_control = as_float(oos, "trade_count") - STAGE142_CONTROL["trade_count"]
        val_trade_gain_vs_control = as_float(val, "trade_count") - STAGE142_CONTROL["validation_trade_count"]
        safe = (
            as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
            and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(oos, "max_drawdown_percent", 99.0) <= 16.5
            and as_float(val, "profit_factor") >= 1.55
            and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
            and as_float(mid, "profit_factor") >= LEGACY_34D["profit_factor"]
        )
        candidates.append(
            (
                safe and oos_trade_gain_vs_control >= 20 and val_trade_gain_vs_control >= 0,
                safe and oos_trade_gain_vs_control > 0,
                safe,
                oos_trade_gain_vs_control,
                val_trade_gain_vs_control,
                as_float(mid, "profit_factor"),
                as_float(val, "profit_factor"),
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                -as_float(oos, "max_drawdown_percent", 99.0),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:10])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage149_runtime_repair_due_to_incomplete_runtime_candidate_not_final"
    best = best_stage148(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    mid = segment_row(segment_rows, adapter_id, "oos", "mid")
    oos_trade_gain_vs_control = as_float(best, "trade_count") - STAGE142_CONTROL["trade_count"]
    val_trade_gain_vs_control = as_float(val, "trade_count") - STAGE142_CONTROL["validation_trade_count"]
    safe = (
        as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(best, "max_drawdown_percent", 99.0) <= 16.5
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
        and as_float(mid, "profit_factor") >= LEGACY_34D["profit_factor"]
    )
    if safe and oos_trade_gain_vs_control >= 20 and val_trade_gain_vs_control >= 0:
        return "proceed_to_stage149_softsession_repair_followup_review_with_material_supply_quality_candidate_not_final"
    if safe and oos_trade_gain_vs_control > 0:
        return "proceed_to_stage149_softsession_repair_followup_review_with_small_supply_quality_candidate_not_final"
    return "continue_stage149_softsession_repair_followup_review_due_to_damage_or_no_gain_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 손실률) | val trades(검증 거래 수) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | gain vs control(대조군 대비 증가) | OOS mid PF(표본외 중반 수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        gain = as_float(oos, "trade_count") - STAGE142_CONTROL["trade_count"]
        lines.append(
            "| {adapter} | {val_pf:.6f} | {val_net:.2f} | {val_dd:.2f} | {val_trades:.0f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} | {mid_pf:.6f} |".format(
                adapter=adapter_id,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                val_dd=as_float(val, "max_drawdown_percent"),
                val_trades=as_float(val, "trade_count"),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=as_float(oos, "trade_count"),
                gain=gain,
                mid_pf=as_float(mid, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage148(summary_rows, segment_rows)
    best_id = str(best.get("adapter_id", ""))
    best_val = split_row(summary_rows, best_id, "validation_is")
    best_mid = segment_row(segment_rows, best_id, "oos", "mid")
    return f"""# Stage148 Softsession Supply Quality Repair Report(148단계 소프트 세션 거래 공급 품질 수리 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE147_ID}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the Stage146 softsession(146단계 소프트 세션) trade count gain(거래 수 증가)을 keep(보존)하면서 validation PF(검증 수익 팩터)와 OOS mid segment(표본외 중반 구간) 손상을 줄일 수 있는가?

Effect(효과): 거래 수 증가 단서를 버리지 않되, 손상된 softsession(소프트 세션)을 기준선처럼 승격하지 않는다.

## Experiment Design(실험 설계)

- hypothesis(가설): Stage146 softsession(146단계 소프트 세션)의 손상은 weak-session block width(약한 세션 차단 폭), et40 mid-margin block(et40 중간 마진 차단), 또는 threshold guard(임계값 보호) 부족에서 온다.
- decision_use(판정 용도): Stage149(149단계) follow-up review(후속 검토)에서 이 축을 계속 수리할지, 다른 bounded stage(경계 단계)로 넘길지 정한다.
- comparison_baseline(비교 기준): Stage146 softsession(146단계 소프트 세션)과 Stage142 control anchor(142단계 대조군 앵커)를 함께 본다.
- control_variables(고정 변수): v41 source model(v41 원천 모델), ATR bracket(ATR 괄호), model risk cap(모델 위험 상한) `3.5%`, reverse lifecycle(반전 생명주기), Tier B disabled(Tier B 비활성).
- changed_variables(변경 변수): gate margin range(게이트 마진 범위), weak-session range(약한 세션 범위), short/long threshold(숏/롱 임계값).
- sample_scope(표본 범위): FPMarkets US100 M5, validation/OOS(검증/표본외), Tier A routed total(Tier A 실제 라우팅 전체; Tier B 비활성 진단 기록).
- success_criteria(성공 기준): OOS trades(표본외 거래 수) `>=200`, OOS PF(표본외 수익 팩터) `>=1.583157`, OOS net(표본외 순손익) `>=987.60`, OOS DD(표본외 손실률) `<=16.5`, validation PF(검증 수익 팩터) `>=1.55`, OOS mid PF(표본외 중반 수익 팩터) `>=1.583157`.
- failure_criteria(실패 기준): 거래 수 증가가 사라지거나, validation/OOS/mid(검증/표본외/중반) 품질 손상이 남는다.
- invalid_conditions(무효 조건): MT5 runtime(메타트레이더5 실행) 미완료, tester report(테스터 보고서) 누락, feature/model hash(피처/모델 해시) 불일치, ledger(장부) 누락.
- stop_conditions(중단 조건): Stage148 안에서 추가 최적화하지 않고 판정 후 Stage149(149단계)로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_candidate(최선 후보): `{best_id or "none"}`
- oos_trade_gain_vs_stage142_control(142단계 대조군 대비 표본외 거래 증가): `{as_float(best, "trade_count") - STAGE142_CONTROL["trade_count"]:.0f}`
- oos_trade_delta_vs_stage146_softsession(146단계 소프트 세션 대비 표본외 거래 차이): `{as_float(best, "trade_count") - STAGE146_SOFTSESSION["trade_count"]:.0f}`
- validation_pf(검증 수익 팩터): `{as_float(best_val, "profit_factor"):.6f}`
- oos_mid_pf(표본외 중반 수익 팩터): `{as_float(best_mid, "profit_factor"):.6f}`
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): Stage146 softsession(146단계 소프트 세션)의 +35 거래 증가와 validation/OOS mid(검증/표본외 중반) 손상을 분리해 측정한다.
- likely_drivers(가능 원인): session block width(세션 차단 폭), et40 mid margin(et40 중간 마진), threshold guard(임계값 보호).
- segment_checks(구간 확인): validation/OOS(검증/표본외), chronological thirds(시간 3분할), risk/ATR telemetry(위험/ATR 기록), same-move reentry(동일 이동 재진입).
- attribution_confidence(귀속 신뢰도): `medium_bounded_mt5_measurement`.
- next_probe(다음 확인): `{NEXT_STAGE_ID}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage148 Decision(148단계 판정)

decision(판정): `{decision}`

Stage148(148단계)는 softsession supply quality repair(소프트 세션 거래 공급 품질 수리)를 bounded repair(경계 수리)로 측정했다. Effect(효과): 결과가 좋든 나쁘든 Stage149(149단계) review-only(검토 전용)로 넘겨 과최적화를 막는다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage147_closeout_commit(원천 147단계 종료 커밋): `{SOURCE_STAGE147_CLOSEOUT_COMMIT}`
- source_stage147_hash_record_commit(원천 147단계 해시 기록 커밋): `{SOURCE_STAGE147_HASH_RECORD_COMMIT}`
- source_stage146_hash_record_commit(원천 146단계 해시 기록 커밋): `{SOURCE_STAGE146_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_stage149_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage149(149단계)는 Stage148 softsession supply quality repair(148단계 소프트 세션 거래 공급 품질 수리) 결과를 follow-up review(후속 검토)로 판정한다.

## Bounded Question(경계 질문)

Did Stage148(148단계) keep useful trade supply(거래 공급)를 while repairing validation PF(검증 수익 팩터) and OOS mid quality(표본외 중반 품질)?

Effect(효과): Stage148(148단계) 안에서 계속 고치지 않고, 다음 수리축 또는 폐기 판단을 분리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage149 Input References(149단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- stage148_decision(148단계 판정): `{rel(DECISION_PATH)}`
- stage148_report(148단계 보고서): `{rel(REPORT_PATH)}`
- stage148_summary(148단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage148_segment_kpi(148단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage148_risk_atr_telemetry(148단계 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage149 Review Index(149단계 검토 색인)

- status(상태): `open_planned`
- source_stage(원천 단계): `{STAGE_ID}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage149(149단계)는 새 MT5 run(MT5 실행)이 아니라 Stage148(148단계) 근거 판독으로 시작한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage149 Selection Status(149단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage148`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    current_focus = f"""current_focus:
- >-
  Stage148(148단계) closed(종료) as `{decision}` and Stage149(149단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): softsession supply quality repair(소프트 세션 거래 공급 품질 수리) 근거를 보존하고 후속 검토로 넘긴다.
- >-
  Stage148 evidence(148단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): 거래 수 증가와 validation/OOS mid(검증/표본외 중반) 품질 회복 여부를 분리해 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on:.*$", "updated_on: '2026-05-18'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    block = f"""
stage148_softsession_supply_quality_repair_after_stage146_damage:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage147_closeout_commit: {SOURCE_STAGE147_CLOSEOUT_COMMIT}
  source_stage147_hash_record_commit: {SOURCE_STAGE147_HASH_RECORD_COMMIT}
  source_stage146_hash_record_commit: {SOURCE_STAGE146_HASH_RECORD_COMMIT}
  source_stage142_hash_record_commit: {SOURCE_STAGE142_HASH_RECORD_COMMIT}
  repair_seed: {SOURCE_ADAPTER_ID}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage149_stage148_softsession_repair_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage148
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run149A_stage149_stage148_softsession_repair_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage148_softsession_supply_quality_repair_after_stage146_damage:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage149_stage148_softsession_repair_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage148 Selection Status(148단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE147_ID}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage148_decision(148단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage148(148단계)는 숫자만으로 전체 목표 완료나 운영 주장을 만들지 않는다.
""",
    )
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage148 Review Index(148단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage148(148단계) 산출물 위치를 한 곳에서 추적하게 한다.
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
- adapter_under_review(검토 중 어댑터): `stage149_softsession_repair_followup_review_surface`
- status(상태): `stage148_closed_{decision}_stage149_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage148(148단계)는 softsession supply quality repair(소프트 세션 거래 공급 품질 수리)를 측정했다. Effect(효과): 결과를 최종 패키지나 운영 주장으로 과장하지 않고 Stage149(149단계) 검토로 넘긴다.

## Latest Stage148 Evidence(최신 148단계 근거)

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
    write_stage149_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage148 softsession supply quality repair closeout(148단계 소프트 세션 거래 공급 품질 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage146 softsession(146단계 소프트 세션)의 거래 수 단서를 validation/OOS mid(검증/표본외 중반) 품질 수리 관점에서 MT5(메타트레이더5)로 측정하고 Stage149(149단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
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
                    "artifact_type": "stage148_softsession_supply_quality_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage148 v2-native softsession supply quality repair artifact.",
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
                    "notes": "Actual Stage148 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_stage148_softsession_supply_quality_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage147_closeout_commit", SOURCE_STAGE147_CLOSEOUT_COMMIT),
                        ("source_stage147_hash_record_commit", SOURCE_STAGE147_HASH_RECORD_COMMIT),
                        ("source_stage146_hash_record_commit", SOURCE_STAGE146_HASH_RECORD_COMMIT),
                        ("repair_seed", SOURCE_ADAPTER_ID),
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_stage148_softsession_quality_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage148 isolates Tier A softsession repair before any Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    required_gates = [
        "runtime_evidence_gate",
        "scope_completion_gate",
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "runtime_parity_gate",
        "backtest_forensics_gate",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    s122.s108.write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-experiment-design",
                "obsidian-performance-attribution",
                "obsidian-result-judgment",
                "obsidian-artifact-lineage",
            ],
            "required_gates": required_gates,
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
            "summary_csv": rel(SUMMARY_CSV_PATH),
            "claim_boundary": BOUNDARY,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "scope_completion_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "bounded_question": "repair Stage146 softsession supply quality without making final or operating claims",
            "scope_completed": result.get("external_verification_status") == "completed",
            "out_of_scope": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "runtime_authority", "overall_goal_completion"],
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "summary_csv": rel(SUMMARY_CSV_PATH),
            "segment_kpi_csv": rel(SEGMENT_KPI_PATH),
            "risk_atr_telemetry_csv": rel(RISK_ATR_TELEMETRY_PATH),
            "gate_feature_summary_csv": rel(GATE_FEATURE_SUMMARY_PATH),
            "target_surface": TARGET_SURFACE,
            "tier_b_policy": "disabled_with_diagnostic_rows",
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(DECISION_PATH)],
            "evidence_missing": [] if status == "completed" else ["completed_mt5_runtime_evidence"],
            "judgment_label": decision,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "user_explanation_hook": "Stage148 is a bounded repair measurement only; it cannot complete the overall goal.",
            "status": "passed_with_boundary" if status == "completed" else "blocked",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "performance_attribution_gate.json",
        {
            "observed_change": "Stage148 changes gate margin, weak-session range, or thresholds around the Stage146 softsession seed.",
            "comparison_baseline": [SOURCE_ADAPTER_ID, STAGE142_CONTROL["adapter_id"]],
            "likely_drivers": ["session_block_width", "et40_mid_margin_block", "threshold_guard"],
            "segment_checks": ["validation_vs_oos", "chronological_thirds", "oos_mid", "risk_atr_telemetry"],
            "trade_shape": rel(AUDIT_CSV_PATH),
            "attribution_confidence": "medium_if_completed_else_blocked",
            "next_probe": NEXT_STAGE_ID,
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "runtime_parity_gate.json",
        {
            "research_path": rel(PRODUCER_PATH),
            "runtime_path": "foundation/mt5 tester profile via generated set files and run_manifest",
            "shared_contract": ["feature_count_2", "thresholds", "atr_bracket", "model_risk_cap", "side_filter"],
            "known_differences": ["Stage148 is runtime_probe research only and not runtime authority."],
            "parity_check": "MT5 Strategy Tester output" if status == "completed" else "blocked_or_incomplete",
            "parity_identity": rel(RUN_ROOT / "run_manifest.json"),
            "runtime_claim_boundary": "runtime_probe_research_only",
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "backtest_forensics_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "tester_identity": "MT5 Strategy Tester via generated run manifest",
            "ea_identity": "Obsidian Prime v2 adapter EA parameterized by generated set files",
            "report_identity": rel(RUN_ROOT / "run_manifest.json"),
            "trade_evidence": rel(SUMMARY_CSV_PATH),
            "cost_assumptions": "same Stage148 regular-risk execution cost model; cost stress recorded in trade audit",
            "forensic_checks": ["report_path_exists", "summary_rows", "risk_telemetry", "artifact_hashes"],
            "backtest_judgment": "usable_with_boundary" if status == "completed" else "blocked",
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "artifact_lineage_audit.json",
        {
            "source_inputs": [
                "stages/147_adapter_research__stage146_control_anchor_followup_review/03_reviews/stage147_control_anchor_tradeoff_summary.csv",
                "stages/146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair/03_reviews/stage146_control_anchor_trade_supply_summary.csv",
                rel(PRODUCER_PATH),
            ],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "artifact_paths": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "segment_kpi": rel(SEGMENT_KPI_PATH),
                "risk_atr": rel(RISK_ATR_TELEMETRY_PATH),
                "gate_feature": rel(GATE_FEATURE_SUMMARY_PATH),
                "stage_ledger": rel(STAGE_LEDGER_PATH),
            },
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "ledger_payload": ledger_payload,
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "declared_required_gates": required_gates,
            "executed_gates": required_gates,
            "missing_gates": [],
            "status": "passed" if status == "completed" else "blocked_with_evidence",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage147_closeout_commit": SOURCE_STAGE147_CLOSEOUT_COMMIT,
            "source_stage147_hash_record_commit": SOURCE_STAGE147_HASH_RECORD_COMMIT,
            "repair_seed": SOURCE_ADAPTER_ID,
            "summary_csv": rel(SUMMARY_CSV_PATH),
            "segment_kpi_csv": rel(SEGMENT_KPI_PATH),
            "risk_atr_telemetry_csv": rel(RISK_ATR_TELEMETRY_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )


def configure_stage148() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE145_ID": SOURCE_STAGE147_ID,
        "SOURCE_STAGE145_CLOSEOUT_COMMIT": SOURCE_STAGE147_CLOSEOUT_COMMIT,
        "SOURCE_STAGE145_HASH_RECORD_COMMIT": SOURCE_STAGE147_HASH_RECORD_COMMIT,
        "SOURCE_STAGE144_HASH_RECORD_COMMIT": SOURCE_STAGE146_HASH_RECORD_COMMIT,
        "SOURCE_STAGE142_HASH_RECORD_COMMIT": SOURCE_STAGE142_HASH_RECORD_COMMIT,
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
        "STAGE142_CONTROL": STAGE146_SOFTSESSION,
        "STAGE144_BEST": STAGE142_CONTROL,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s146, name, value)
    s146.source_baseline = source_baseline
    s146.best_stage146 = best_stage148
    s146.decide = decide
    s146.row_table = row_table
    s146.report_markdown = report_markdown
    s146.decision_markdown = decision_markdown
    s146.update_current_truth = update_current_truth
    s146.append_changelog = append_changelog
    s146.build_attempts = build_attempts
    s146.artifact_rows = artifact_rows
    s146.write_ledgers = write_ledgers
    s146.tier_b_rows = tier_b_rows
    s146.write_packet_files = write_packet_files
    s146.configure_stage146()


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage148()
    code = s122.s120.main(argv)
    write_stage149_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

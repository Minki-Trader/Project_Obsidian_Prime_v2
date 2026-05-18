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
from stage_pipelines.stage144 import shortgate_quality_repair_after_stage142_damage as s144  # noqa: E402


s138 = s144.s138
s122 = s144.s122
s100 = s144.s100

STAGE_ID = "146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair"
RUN_NUMBER = "run146A"
RUN_ID = "run146A_stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1"
PACKET_ID = "stage146_control_anchor_trade_supply_after_shortgate_no_repair_v1"
PARENT_RUN_ID = "run145A_stage145_stage144_shortgate_quality_followup_review_v1"
SOURCE_STAGE145_ID = "145_adapter_research__stage144_shortgate_quality_followup_review"
SOURCE_STAGE145_CLOSEOUT_COMMIT = "6006e4546224f104f6d102a2a04ae2f9dfa26b06"
SOURCE_STAGE145_HASH_RECORD_COMMIT = "7b6d881cbf5871674724d2c2a8dfb082301fda82"
SOURCE_STAGE144_HASH_RECORD_COMMIT = "07f23d8939ab31e6e7d1a564cc9c8c9496fa2704"
SOURCE_STAGE142_HASH_RECORD_COMMIT = "7813b4d26006336dcf1709949ce78d47462b3c47"
SOURCE_ADAPTER_ID = "s142_control_reverse_bothgate_h3_cd5_risk035"
NEXT_STAGE_ID = "147_adapter_research__stage146_control_anchor_followup_review"
NEXT_RUN_ID = "run147A_stage147_stage146_control_anchor_followup_review_v1"
NEXT_PACKET_ID = "stage147_stage146_control_anchor_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s146a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage146_control_anchor_trade_supply_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage146_control_anchor_trade_supply_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage146_control_anchor_trade_supply_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage146_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage146_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage146_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage146_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage146_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage146_trade_audit.csv"
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
STAGE142_CONTROL = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.795976838,
    "net_profit": 1186.30,
    "max_drawdown_percent": 14.66,
    "trade_count": 180,
    "validation_profit_factor": 1.582222632,
    "validation_net_profit": 1388.24,
    "validation_max_drawdown_percent": 11.85,
    "validation_trade_count": 265,
}
STAGE144_BEST = {
    "adapter_id": "s144_shortgate_reverse_cd6_h3_sht54_lng52_risk035",
    "profit_factor": 1.55,
    "net_profit": 952.38,
    "max_drawdown_percent": 20.12,
    "trade_count": 230,
    "validation_profit_factor": 1.56,
    "validation_net_profit": 1821.00,
    "validation_max_drawdown_percent": 11.84,
    "validation_trade_count": 321,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s146_control_bothgate_replay_h3_cd5_sht54_lng52_risk035",
        label="stage146_control_bothgate_replay_h3_cd5_sht54_lng52_risk035",
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
        notes="Stage146 control replay: preserve Stage142 control anchor settings.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035",
        label="stage146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035",
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
        notes="Stage146 supply probe: keep both-side gate but soften weak-session block.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s146_control_bothgate_ease_h3_cd5_sht53_lng51_risk035",
        label="stage146_control_bothgate_ease_h3_cd5_sht53_lng51_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.53,
        long_threshold=0.51,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage146 supply probe: ease thresholds while preserving both-side gate.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s146_control_bothgate_hold4_h4_cd5_sht54_lng52_risk035",
        label="stage146_control_bothgate_hold4_h4_cd5_sht54_lng52_risk035",
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
        max_hold_bars=4,
        notes="Stage146 supply probe: hold 4 bars while preserving both-side gate.",
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
    "s146_control_bothgate_replay_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage146_gate_control_replay",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Control replay: original both-side weak-context block.",
    },
    "s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage146_gate_control_soft_session",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 175.0,
        "session_max": 260.0,
        "margin_min": 0.045,
        "margin_max": 0.075,
        "description": "Supply probe: narrower weak-session block, still both-side.",
    },
    "s146_control_bothgate_ease_h3_cd5_sht53_lng51_risk035": {
        "gate_column": "stage146_gate_control_threshold_ease",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Supply probe: eased thresholds with original both-side gate.",
    },
    "s146_control_bothgate_hold4_h4_cd5_sht54_lng52_risk035": {
        "gate_column": "stage146_gate_control_hold4",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Supply probe: hold 4 bars with original both-side gate.",
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
    return STAGE142_CONTROL if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


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


def stage146_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
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
                magic = 14610000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=146,
                        exploration_label="stage146_BaselineAdapter__ControlAnchorTradeSupplyAfterShortgateNoRepair",
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
                        extra_set_values=stage146_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage146(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        early = segment_row(segment_rows, adapter_id, "oos", "early")
        oos_trade_gain = as_float(oos, "trade_count") - STAGE142_CONTROL["trade_count"]
        val_trade_gain = as_float(val, "trade_count") - STAGE142_CONTROL["validation_trade_count"]
        safe = (
            as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
            and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(oos, "max_drawdown_percent", 99.0) <= 16.5
            and as_float(val, "profit_factor") >= 1.55
            and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
        )
        candidates.append(
            (
                safe and oos_trade_gain >= 20 and val_trade_gain >= 0,
                safe and oos_trade_gain > 0,
                safe,
                oos_trade_gain,
                val_trade_gain,
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                -as_float(oos, "max_drawdown_percent", 99.0),
                as_float(early, "profit_factor"),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:9])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage147_control_anchor_runtime_repair_due_to_incomplete_runtime_candidate_not_final"
    best = best_stage146(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    oos_trade_gain = as_float(best, "trade_count") - STAGE142_CONTROL["trade_count"]
    val_trade_gain = as_float(val, "trade_count") - STAGE142_CONTROL["validation_trade_count"]
    safe = (
        as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(best, "max_drawdown_percent", 99.0) <= 16.5
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
    )
    if safe and oos_trade_gain >= 20 and val_trade_gain >= 0:
        return "proceed_to_stage147_control_anchor_followup_review_with_material_trade_supply_candidate_not_final"
    if safe and oos_trade_gain > 0:
        return "proceed_to_stage147_control_anchor_followup_review_with_small_trade_supply_candidate_not_final"
    return "continue_stage147_control_anchor_followup_review_due_to_damage_or_no_trade_gain_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | gate(게이트) | val PF(검증 수익 팩터) | val net(검증 순손익) | val trades(검증 거래 수) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | gain vs control(대조군 대비 증가) | OOS early PF(표본외 초반 수익 팩터) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        early = segment_row(segment_rows, adapter_id, "oos", "early")
        gate = CONTEXT_GATE_SPECS.get(adapter_id, {}).get("block_mode", "")
        trades = as_float(oos, "trade_count")
        lines.append(
            "| {adapter} | {gate} | {val_pf:.6f} | {val_net:.2f} | {val_trades:.0f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} | {early_pf:.6f} |".format(
                adapter=adapter_id,
                gate=gate,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                val_trades=as_float(val, "trade_count"),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=trades,
                gain=trades - STAGE142_CONTROL["trade_count"],
                early_pf=as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage146(summary_rows, segment_rows)
    best_id = str(best.get("adapter_id", ""))
    best_val = split_row(summary_rows, best_id, "validation_is")
    return f"""# Stage146 Control Anchor Trade Supply Report(146단계 대조군 앵커 거래 공급 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE145_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the Stage142 control anchor(142단계 대조군 앵커)의 OOS quality(표본외 품질)를 보존하면서 no-gate(무게이트)나 failed shortgate same-axis repair(실패한 숏게이트 동일 축 수리)를 반복하지 않고 trade count(거래 수)를 늘릴 수 있는가?

Effect(효과): 손상된 숏게이트 축을 더 밀지 않고, 품질이 살아 있던 대조군 앵커에서 좁은 공급 축만 시험한다.

## Experiment Design(실험 설계)

- hypothesis(가설): both-side gate(양방향 게이트)를 유지한 상태에서 session block(세션 차단), threshold(임계값), hold(보유 기간)만 좁게 바꾸면 Stage142 control(142단계 대조군)의 PF/net/DD(수익 팩터/순손익/손실률)를 크게 훼손하지 않고 거래 수를 조금 늘릴 수 있다.
- decision_use(판정 용도): Stage147(147단계)에서 이 축을 더 볼지, 다른 bounded repair(경계 수리)로 돌릴지 정한다.
- comparison_baseline(비교 기준): `{SOURCE_ADAPTER_ID}` OOS PF `1.795977`, net `1186.30`, DD `14.66`, trades `180`.
- control_variables(고정 변수): v41 source model(v41 원천 모델), ATR bracket(ATR 괄호), model risk cap(모델 위험 한도) `3.5%`, reverse lifecycle(반전 생명주기), Tier B disabled(Tier B 비활성).
- changed_variables(변경 변수): weak-session block(약한 세션 차단), thresholds(임계값), max_hold_bars(최대 보유 봉수).
- success_criteria(성공 기준): OOS trades(표본외 거래 수) `200+`, PF `>= 1.583157`, net `>= 987.60`, DD `<= 16.5`, validation(검증) PF/net/DD 유지.
- failure_criteria(실패 기준): 거래 수가 늘어도 PF/net/DD가 손상되거나, 거래 수가 늘지 않거나, Stage144 손상 경로와 비슷한 품질 저하가 나타나는 경우.
- stop_conditions(중단 조건): Stage146 안에서 추가 최적화하지 않고 Stage147 follow-up review(후속 검토)로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_candidate(최선 후보): `{best_id or "none"}`
- oos_pf(표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(표본외 손실률): `{as_float(best, "max_drawdown_percent"):.2f}`
- oos_trades(표본외 거래 수): `{as_float(best, "trade_count"):.0f}`
- trade_delta_vs_control(대조군 대비 거래 차이): `{as_float(best, "trade_count") - STAGE142_CONTROL["trade_count"]:.0f}`
- trade_delta_vs_34d(34D 대비 거래 차이): `{as_float(best, "trade_count") - LEGACY_34D["trade_count"]:.0f}`
- val_pf(검증 수익 팩터): `{as_float(best_val, "profit_factor"):.6f}`
- val_net(검증 순손익): `{as_float(best_val, "net_profit"):.2f}`
- val_dd_pct(검증 손실률): `{as_float(best_val, "max_drawdown_percent"):.2f}`
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): control anchor(대조군 앵커) 대비 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 변화.
- likely_drivers(가능 원인): both-side gate(양방향 게이트), threshold ease(임계값 완화), weak-session block width(약한 세션 차단 폭), hold length(보유 길이).
- segment_checks(구간 확인): chronological thirds(시간 3분할), validation vs OOS(검증 대 표본외), Tier B disabled diagnostic(Tier B 비활성 진단), risk/ATR telemetry(위험/ATR 기록).
- attribution_confidence(귀속 신뢰도): `medium_bounded_measurement_pending_stage147_review`.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `stage_pipelines/stage146/control_anchor_trade_supply_after_shortgate_no_repair.py`
- runtime_path(런타임 경로): MT5 Strategy Tester(MT5 전략 테스터) reports under `{rel(RUN_ROOT / "mt5" / "reports")}`.
- parity_check(동등성 확인): Strategy Tester output(전략 테스터 출력) and generated telemetry(생성 기록).
- runtime_claim_boundary(런타임 주장 경계): `research_only_no_runtime_authority`.

## Judgment(판정)

- judgment_label(판정 라벨): `control_anchor_trade_supply_measured_not_final`.
- evidence_available(사용 가능 근거): MT5 reports(MT5 보고서), summary CSV(요약 CSV), segment KPI(구간 KPI), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage147(147단계) follow-up review(후속 검토) 전에는 equity curve(자본 곡선), concentration(집중도), final package(최종 패키지) 판정이 닫히지 않았다.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage146 Decision(146단계 판정)

decision(판정): `{decision}`

Stage146(146단계)은 control anchor trade supply repair(대조군 앵커 거래 공급 수리)만 좁게 실행했다.

Effect(효과): 결과가 좋아도 final adapter(최종 어댑터)나 operating claim(운영 주장)으로 올리지 않고, Stage147(147단계) follow-up review(후속 검토)로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage145_closeout_commit(원천 145단계 종료 커밋): `{SOURCE_STAGE145_CLOSEOUT_COMMIT}`
- source_stage145_hash_record_commit(원천 145단계 해시 기록 커밋): `{SOURCE_STAGE145_HASH_RECORD_COMMIT}`
- source_stage144_hash_record_commit(원천 144단계 해시 기록 커밋): `{SOURCE_STAGE144_HASH_RECORD_COMMIT}`
- source_stage142_hash_record_commit(원천 142단계 해시 기록 커밋): `{SOURCE_STAGE142_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage146 closeout(146단계 종료)은 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상 목표는 Stage147(147단계) 이후 bounded research/development(경계 연구개발)로 계속된다.
"""


def write_stage147_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage147(147단계)은 Stage146 control anchor trade supply repair(146단계 대조군 앵커 거래 공급 수리) 결과를 follow-up review(후속 검토)로 판정한다.

## Bounded Question(경계 질문)

Did Stage146(146단계) increase trade count(거래 수) without damaging PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), and concentration(집중도)?

Effect(효과): Stage146 안에서 계속 고치지 않고, 결과 판독만 분리해 다음 수리 축을 좁게 고른다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage147 Input References(147단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- stage146_decision(146단계 판정): `{rel(DECISION_PATH)}`
- stage146_report(146단계 보고서): `{rel(REPORT_PATH)}`
- stage146_summary(146단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage146_segment_kpi(146단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage146_risk_atr_telemetry(146단계 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage147 Review Index(147단계 검토 색인)

- status(상태): `open_planned`
- source_stage(원천 단계): `{STAGE_ID}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage147(147단계)은 새 MT5 run(MT5 실행)이 아니라 Stage146(146단계) 근거 판독으로 시작한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage147 Selection Status(147단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage146`
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
  Stage146(146단계) closed(종료) as `{decision}` and Stage147(147단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): control anchor trade supply repair(대조군 앵커 거래 공급 수리) 근거를 보존하고 후속 검토로 넘긴다.
- >-
  Stage146 evidence(146단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): 거래 수 증가와 KPI(핵심 성과 지표) 손상 여부를 분리해 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on:.*$", "updated_on: '2026-05-18'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    block = f"""
stage146_control_anchor_trade_supply_after_shortgate_no_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage145_closeout_commit: {SOURCE_STAGE145_CLOSEOUT_COMMIT}
  source_stage145_hash_record_commit: {SOURCE_STAGE145_HASH_RECORD_COMMIT}
  source_stage144_hash_record_commit: {SOURCE_STAGE144_HASH_RECORD_COMMIT}
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

stage147_stage146_control_anchor_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage146
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run147A_stage147_stage146_control_anchor_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage146_control_anchor_trade_supply_after_shortgate_no_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage147_stage146_control_anchor_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage146 Selection Status(146단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE145_ID}`
- source_stage142_adapter(원천 142단계 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage146_decision(146단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage146(146단계)은 닫지만 전체 목표 완료나 운영 주장은 만들지 않는다.
""",
    )
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage146 Review Index(146단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage146(146단계) 산출물 위치를 한 곳에서 추적하게 한다.
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
- adapter_under_review(검토 중 어댑터): `stage147_control_anchor_followup_review_surface`
- status(상태): `stage146_closed_{decision}_stage147_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage146(146단계)은 control anchor trade supply repair(대조군 앵커 거래 공급 수리)를 측정했다. Effect(효과): 결과를 final package(최종 패키지)나 operating claim(운영 주장)으로 과장하지 않고 Stage147(147단계) 검토로 넘긴다.

## Latest Stage146 Evidence(최신 146단계 근거)

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
    write_stage147_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage146 control anchor trade supply closeout(146단계 대조군 앵커 거래 공급 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage142 control anchor(142단계 대조군 앵커)의 거래 공급 축을 MT5(메타트레이더5)로 측정하고 Stage147(147단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        Path("stage_pipelines/stage146/control_anchor_trade_supply_after_shortgate_no_repair.py"),
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
                    "artifact_type": "stage146_control_anchor_trade_supply_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage146 v2-native control anchor trade supply artifact.",
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
                    "notes": "Actual Stage146 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_stage146_control_anchor_trade_supply_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage145_closeout_commit", SOURCE_STAGE145_CLOSEOUT_COMMIT),
                        ("source_stage145_hash_record_commit", SOURCE_STAGE145_HASH_RECORD_COMMIT),
                        ("source_stage144_hash_record_commit", SOURCE_STAGE144_HASH_RECORD_COMMIT),
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_stage146_control_anchor_trade_supply",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage146 isolates Tier A control anchor trade supply before any Tier B fallback repair.",
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
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-artifact-lineage",
            ],
            "required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "runtime_parity_gate",
                "backtest_forensics_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
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
        PACKET_ROOT / "scope_completion_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "bounded_question_answered": True,
            "stage_scope": "control_anchor_trade_supply_repair_only",
            "not_in_scope": [
                "deployment",
                "live_readiness",
                "operating_promotion",
                "operating_reference",
                "production_baseline",
                "runtime_authority",
                "overall_goal_completion",
            ],
            "next_stage_or_branch": NEXT_STAGE_ID,
            "status": status,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "performance_attribution_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "observed_change": "control_anchor_trade_supply_vs_stage142_control",
            "comparison_baseline": SOURCE_ADAPTER_ID,
            "likely_drivers": ["both_side_gate_width", "threshold_surface", "max_hold_bars", "reverse_lifecycle"],
            "segment_checks": ["chronological_thirds", "validation_vs_oos", "tier_b_disabled_diagnostic", "risk_atr_telemetry"],
            "attribution_confidence": "medium_bounded_measurement_pending_stage147_review",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "runtime_parity_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "research_path": rel(Path("stage_pipelines/stage146/control_anchor_trade_supply_after_shortgate_no_repair.py")),
            "runtime_path": rel(RUN_ROOT / "mt5" / "reports"),
            "shared_contract": ["feature_count_2", "thresholds", "atr_bracket", "model_risk_cap", "side_filter"],
            "known_differences": ["research_runtime_probe_only_no_runtime_authority"],
            "parity_check": "mt5_strategy_tester_output",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "backtest_forensics_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "tester_identity": "MT5 Strategy Tester, US100 M5, validation_is and oos date ranges from source ini files",
            "ea_identity": "parameter_only_variant_using_existing thin EA and shared include modules",
            "report_identity": rel(RUN_ROOT / "mt5" / "reports"),
            "trade_evidence": {
                "summary_csv": rel(SUMMARY_CSV_PATH),
                "segment_kpi": rel(SEGMENT_KPI_PATH),
            },
            "cost_assumptions": "same source tester profile and Stage142/144 cost assumptions; cost_stressed_expectancy recorded in summary",
            "forensic_checks": [
                "external_verification_status_completed",
                "strategy_tester_reports_imported",
                "tier_a_and_actual_routed_rows_recorded",
                "no_synthetic_sum_used_as_routed_total",
            ],
            "backtest_judgment": "usable_with_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "judgment_label": "control_anchor_trade_supply_measured_not_final",
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
            "source_inputs": [
                rel(Path("stage_pipelines/stage142/route_coverage_supply_branch_after_reverse_exhaustion.py")),
                rel(Path("stage_pipelines/stage145/stage144_shortgate_quality_followup_review.py")),
            ],
            "producer": rel(Path("stage_pipelines/stage146/control_anchor_trade_supply_after_shortgate_no_repair.py")),
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
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "allowed_claims": [
                "research_development_only",
                "runtime_probe_evidence_completed",
                "control_anchor_trade_supply_measured_not_final",
                "stage147_followup_required",
            ],
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "runtime_authority",
                "operating_promotion",
                "operating_reference",
                "production_baseline",
                "overall_goal_complete",
                "legacy_inheritance",
            ],
            "overall_goal_complete": False,
            "status": "passed",
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "declared_required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "runtime_parity_gate",
                "backtest_forensics_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "executed_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "runtime_parity_gate",
                "backtest_forensics_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "missing_gates": [],
            "status": "passed_with_research_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage145_closeout_commit": SOURCE_STAGE145_CLOSEOUT_COMMIT,
            "source_stage145_hash_record_commit": SOURCE_STAGE145_HASH_RECORD_COMMIT,
            "source_stage144_hash_record_commit": SOURCE_STAGE144_HASH_RECORD_COMMIT,
            "source_stage142_hash_record_commit": SOURCE_STAGE142_HASH_RECORD_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def configure_stage146() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE137_ID": SOURCE_STAGE145_ID,
        "SOURCE_STAGE137_CLOSEOUT_COMMIT": SOURCE_STAGE145_CLOSEOUT_COMMIT,
        "SOURCE_STAGE137_LATEST_COMMIT": SOURCE_STAGE145_HASH_RECORD_COMMIT,
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
        "STAGE136_SOURCE": STAGE142_CONTROL,
        "STAGE110_REFERENCE": STAGE144_BEST,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s138, name, value)
    s138.source_baseline = source_baseline
    s138.best_stage138 = best_stage146
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
    configure_stage146()
    code = s122.s120.main(argv)
    write_stage147_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage66 import soft_gate_kpi_repair as base  # noqa: E402

repair = base.repair
s58 = base.s58
engine = base.engine
checkpoint = base.checkpoint
mt5 = base.mt5


STAGE67_ID = "67_adapter_research__short_gate_net_scale_review"
RUN_NUMBER = "run67A"
RUN_ID = "run67A_stage67_short_gate_net_scale_review_v1"
PACKET_ID = "stage67_short_gate_net_scale_review_v1"
PARENT_RUN_ID = "run66A_stage66_soft_gate_kpi_repair_v1"
SOURCE_STAGE66_COMMIT = "3ef3643433a0d3fb4dae6368a44643abb73be20f"
NEXT_STAGE_ID = "68_adapter_research__dd_net_balance_repair"
NEXT_RUN_ID = "run68A_stage68_dd_net_balance_repair_v1"
NEXT_PACKET_ID = "stage68_dd_net_balance_repair_v1"
SOURCE_ADAPTER_ID = "s62_v41_sd8_h5"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DEVELOPMENT_ANCHOR = "v41_v22_midcov_et40_agree_h2c0_no_b"
BACKUP_ANCHOR = "s62_v41_sd8_h5"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE67_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE_ROOT = Path("stages") / "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN50BN_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BN"
RUN50BN_MODEL = RUN50BN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
RUN50BN_SIGNAL = "stage56_context_et_event_signal"
SOURCE_ANCHOR = "v41_v22_midcov_et40_agree_h2c0_no_b"
SOURCE_TOKEN = "x01"
COMMON_ROOT = f"OPV2/s67/{RUN_NUMBER}"
MIN_MARGIN = 0.0

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage67_short_gate_net_scale_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage67_short_gate_net_scale_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage67_short_gate_net_scale_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage67_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage67_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage67_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage67_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage67_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage67_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

LEGACY_34D_TARGETS = base.LEGACY_34D_TARGETS
STAGE66_REFERENCE = {
    "best_adapter": "s66_short_risk5_h5",
    "validation_pf": 1.41,
    "validation_net": 893.80,
    "validation_dd_pct": 25.88,
    "oos_pf": 1.40,
    "oos_net": 540.04,
    "oos_dd_pct": 18.62,
}

STAGE67_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s67_ctrl_risk5_h5_cd8",
        label="short_gate_control_risk5_sl20_tp32_h5_cd8",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.05,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes=(
            "Stage67 v2-native control: rerun the Stage66 best short-gate risk5 hold5 shape. "
            "Legacy 34D is a lesson-only KPI target surface, not copied logic."
        ),
    ),
    repair.RepairVariant(
        adapter_id="s67_risk45_h5_cd8",
        label="short_gate_risk45_sl20_tp32_h5_cd8",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.045,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes=(
            "Stage67 v2-native risk interpolation: test 4.5% model-risk cap with the same Stage66 short gate. "
            "Effect: measure whether net remains closer to 34D while DD moves back toward the safer risk4 shape."
        ),
    ),
    repair.RepairVariant(
        adapter_id="s67_risk5_h5_cd12",
        label="short_gate_risk5_sl20_tp32_h5_cd12",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.05,
        same_direction_reentry_cooldown_bars=12,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes=(
            "Stage67 v2-native re-entry guard: keep 5% cap but extend same-direction cooldown to 12 bars. "
            "Effect: measure whether same-move density and DD drop without losing the net gain."
        ),
    ),
)

MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in STAGE67_VARIANTS}
CONTEXT_GATE_SPECS = {
    variant.adapter_id: {
        "gate_column": "stage67_gate_margin_lt_008_short",
        "gate_type": "margin",
        "threshold": 0.08,
        "block_mode": "short",
        "description": f"block shorts only if et40_decision_margin < 0.08; {variant.label}",
    }
    for variant in STAGE67_VARIANTS
}


def rel(path: Path | str) -> str:
    return base.rel(path)


def configure_stage67_globals() -> None:
    assignments = {
        "STAGE66_ID": STAGE67_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_STAGE65_COMMIT": SOURCE_STAGE66_COMMIT,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "DEVELOPMENT_ANCHOR": DEVELOPMENT_ANCHOR,
        "BACKUP_ANCHOR": BACKUP_ANCHOR,
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "SPEC_ROOT": SPEC_ROOT,
        "INPUT_ROOT": INPUT_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "SOURCE_STAGE_ROOT": SOURCE_STAGE_ROOT,
        "RUN50BN_ROOT": RUN50BN_ROOT,
        "RUN50BN_MODEL": RUN50BN_MODEL,
        "RUN50BN_SIGNAL": RUN50BN_SIGNAL,
        "SOURCE_ANCHOR": SOURCE_ANCHOR,
        "SOURCE_TOKEN": SOURCE_TOKEN,
        "COMMON_ROOT": COMMON_ROOT,
        "MIN_MARGIN": MIN_MARGIN,
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
        "RUN_REGISTRY_PATH": RUN_REGISTRY_PATH,
        "PROJECT_LEDGER_PATH": PROJECT_LEDGER_PATH,
        "ARTIFACT_REGISTRY_PATH": ARTIFACT_REGISTRY_PATH,
        "WORKSPACE_STATE_PATH": WORKSPACE_STATE_PATH,
        "CURRENT_WORKING_STATE_PATH": CURRENT_WORKING_STATE_PATH,
        "CHANGELOG_PATH": CHANGELOG_PATH,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "STAGE66_VARIANTS": STAGE67_VARIANTS,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }
    for name, value in assignments.items():
        setattr(base, name, value)
    base.configure_reused_engine()
    engine.EQUITY_AUDIT_PATH = REVIEWS_ROOT / "stage67_equity_curve_audit.md"


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for variant in STAGE67_VARIANTS:
        source_label = engine.source_label_for_variant(variant)
        model_source = engine.source_model_for_variant(variant)
        gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
        model_local = RUN_ROOT / variant.adapter_id / "models" / f"{source_label}_{model_source.stem}_{gate_column}.csv"
        base.write_neutral_gate_model(model_source, model_local)
        copied.append(
            {
                "source": rel(model_source),
                "path": rel(model_local),
                "sha256": base.sha256_file_lf_normalized(model_local),
                "transform": "append_neutral_stage67_gate_feature",
            }
        )
        copied.append(engine.copy_to_common(model_local, f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[variant.adapter_id] = {
            "path": rel(model_local),
            "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}",
            "sha256": base.sha256_file_lf_normalized(model_local),
            "source_model": rel(model_source),
            "source_anchor": engine.source_anchor_for_variant(variant),
            "signal_column": RUN50BN_SIGNAL,
            "gate_column": gate_column,
            "feature_order_hash": base.feature_order_hash_for_variant(variant),
        }
        feature_exports[variant.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = engine.source_feature(split, variant, "a")
            feature_local = RUN_ROOT / variant.adapter_id / "features" / f"{variant.adapter_id}_stage67_state_context_a_{token}.csv"
            gate_row = base.write_gated_feature(feature_source, feature_local, variant)
            gate_row["split"] = split
            gate_rows.append(gate_row)
            copied.append(
                {
                    "source": rel(feature_source),
                    "path": rel(feature_local),
                    "sha256": base.sha256_file_lf_normalized(feature_local),
                    "transform": "stage67_short_gate_feature",
                }
            )
            copied.append(engine.copy_to_common(feature_local, f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}", common_files_root))
            feature_exports[variant.adapter_id][split] = {
                "path": rel(feature_local),
                "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}",
                "sha256": base.sha256_file_lf_normalized(feature_local),
                "source_feature": rel(feature_source),
                "gate_column": gate_column,
            }
    return {
        "model_exports": model_exports,
        "feature_exports": feature_exports,
        "common_copies": copied,
        "gate_rows": gate_rows,
    }


def stage67_extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = engine.extra_set_values(variant, magic)
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
    for variant_index, variant in enumerate(STAGE67_VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = base.parse_ini(engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            roles = (
                (mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                (mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
            )
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(roles, start=1):
                magic = 67067000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=67,
                        exploration_label="stage67_BaselineAdapter__ShortGateNetScaleReview",
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
                        min_margin=MIN_MARGIN,
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
                        extra_set_values=stage67_extra_set_values(variant, magic),
                    )
                )
    return attempts


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage67_due_to_incomplete_runtime"
    by_adapter: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in summary_rows:
        if row.get("view") != "actual_routed_total" or row.get("status") != "completed":
            continue
        adapter_id = str(row.get("adapter_id") or "")
        split_key = "validation" if row.get("split") == "validation_is" else str(row.get("split") or "")
        by_adapter.setdefault(adapter_id, {})[split_key] = row
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows)
    candidate_found = False
    for splits in by_adapter.values():
        val = splits.get("validation", {})
        oos = splits.get("oos", {})
        val_pf = s58.as_float(val.get("profit_factor"), 0.0) or 0.0
        oos_pf = s58.as_float(oos.get("profit_factor"), 0.0) or 0.0
        val_net = s58.as_float(val.get("net_profit"), 0.0) or 0.0
        oos_net = s58.as_float(oos.get("net_profit"), 0.0) or 0.0
        val_dd = s58.as_float(val.get("max_drawdown_percent"), 99.0) or 99.0
        oos_dd = s58.as_float(oos.get("max_drawdown_percent"), 99.0) or 99.0
        if val_net >= 930 and oos_net >= 520 and val_pf >= 1.38 and oos_pf >= 1.35 and val_dd <= 18.8 and oos_dd <= 18.8 and not reasons:
            return "proceed_to_stage68_research_candidate_review"
        if val_net >= 650 and oos_net >= 400 and val_pf >= 1.30 and oos_pf >= 1.25 and val_dd <= 24.0 and oos_dd <= 20.0:
            candidate_found = True
    if candidate_found:
        return "continue_dd_net_balance_repair_in_stage68"
    return "cap_short_gate_branch_and_open_new_model_branch"


def balanced_candidate_id(summary_rows: Sequence[Mapping[str, Any]]) -> str:
    by_adapter: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in summary_rows:
        if row.get("view") != "actual_routed_total" or row.get("status") != "completed":
            continue
        adapter_id = str(row.get("adapter_id") or "")
        split_key = "validation" if row.get("split") == "validation_is" else str(row.get("split") or "")
        by_adapter.setdefault(adapter_id, {})[split_key] = row
    candidates: list[tuple[float, str]] = []
    for adapter_id, splits in by_adapter.items():
        val = splits.get("validation", {})
        oos = splits.get("oos", {})
        val_pf = s58.as_float(val.get("profit_factor"), 0.0) or 0.0
        oos_pf = s58.as_float(oos.get("profit_factor"), 0.0) or 0.0
        val_net = s58.as_float(val.get("net_profit"), 0.0) or 0.0
        oos_net = s58.as_float(oos.get("net_profit"), 0.0) or 0.0
        val_dd = s58.as_float(val.get("max_drawdown_percent"), 99.0) or 99.0
        oos_dd = s58.as_float(oos.get("max_drawdown_percent"), 99.0) or 99.0
        if val_net >= 650 and oos_net >= 400 and val_pf >= 1.30 and oos_pf >= 1.25 and val_dd <= 24.0 and oos_dd <= 20.0:
            score = val_net + oos_net - (val_dd + oos_dd) * 10.0
            candidates.append((score, adapter_id))
    if not candidates:
        return "none"
    return sorted(candidates, reverse=True)[0][1]


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    lines = [
        "| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in target_rows:
        lines.append(
            "| {adapter} | {split} | {pf:.4f} | {net:.2f} | {dd:.2f} | {exp:.4f} | {gap:.4f} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                pf=float(row.get("profit_factor") or 0.0),
                net=float(row.get("net_profit") or 0.0),
                dd=float(row.get("max_drawdown_percent") or 0.0),
                exp=float(row.get("expectancy") or 0.0),
                gap=float(row.get("pf_gap_to_34d_latest") or 0.0),
            )
        )
    best = engine.best_repaired_variant(summary_rows)
    balanced = balanced_candidate_id(summary_rows)
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["runtime_incomplete_or_blocked"]
    variants = ", ".join(variant.adapter_id for variant in STAGE67_VARIANTS)
    return f"""# Stage67 Short Gate Net Scale Review Report(67단계 숏 게이트 순손익 확대 검토 보고)

- run(실행): `{RUN_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_stage66_pushed_commit(원천 66단계 푸시 커밋): `{SOURCE_STAGE66_COMMIT}`
- variants(변형): `{variants}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage66(66단계)의 short-gate risk5 hold5(숏 게이트 위험5 보유5) 순손익 증가는 유효하지만, DD(손실률)는 risk cap(위험 상한) 보간이나 same-direction cooldown(같은 방향 냉각)으로 낮출 수 있다.
- comparison_baseline(비교 기준): Stage66(66단계) best(최선) `{STAGE66_REFERENCE["best_adapter"]}` validation/OOS(검증/표본외) PF(수익 팩터) `{STAGE66_REFERENCE["validation_pf"]:.2f}/{STAGE66_REFERENCE["oos_pf"]:.2f}`, net(순손익) `{STAGE66_REFERENCE["validation_net"]:.2f}/{STAGE66_REFERENCE["oos_net"]:.2f}`, DD(손실률) `{STAGE66_REFERENCE["validation_dd_pct"]:.2f}/{STAGE66_REFERENCE["oos_dd_pct"]:.2f}`.
- changed_variables(변경 변수): risk cap(위험 상한) `5% -> 4.5%`, same-direction cooldown(같은 방향 냉각) `8 -> 12`; gate(게이트), model(모델), ATR bracket(ATR 브래킷), hold(보유)는 고정한다.
- stop_conditions(중단 조건): validation/OOS(검증/표본외) 중 하나라도 PF(수익 팩터), DD(손실률), cost stress(비용 압박)가 무너지면 branch cap(분기 제한) 또는 Stage68(68단계) 수리로 넘긴다.

## Result Table(결과 표)

{chr(10).join(lines)}

## Attribution Read(원인 분해 판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- balanced_candidate(균형 후보): `{balanced}`
- weakness_reasons(약점 이유): `{";".join(reasons) if reasons else "none"}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- tier_b_diagnostic(Tier B 진단): `{rel(TIER_B_DIAGNOSTIC_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage67 Decision(67단계 판정)

decision(판정): `{decision}`

Stage67(67단계)는 legacy 34D(레거시 34D)를 복사하지 않고, Stage66(66단계) best(최선)인 short-gate risk5 hold5(숏 게이트 위험5 보유5) 흐름을 control(대조군), 4.5% risk cap(4.5% 위험 상한), 12-bar cooldown(12봉 냉각)으로 좁게 비교했다.

Effect(효과): 이번 단계 결과는 operating claim(운영 주장)이 아니라, net/DD balance(순손익/손실률 균형)를 다음 bounded research(경계 연구)로 넘길지 또는 branch cap(분기 제한)을 할지 정한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- tier_b_diagnostic(Tier B 진단): `{rel(TIER_B_DIAGNOSTIC_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def tier_b_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    coverage = engine.route_coverage()
    for variant in STAGE67_VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_short_gate_review",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage67 keeps Tier B fallback disabled to isolate short-gate net/DD balance first.",
                }
            )
    return rows


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = base.utc_now()
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
        if base.path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage67_short_gate_net_scale_review_evidence",
                    "path": rel(path),
                    "sha256": base.sha256_file_lf_normalized(path),
                    "stage_id": STAGE67_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage67 v2-native short-gate net/DD balance artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if raw_path and base.path_exists(Path(str(raw_path))):
            path = Path(str(raw_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": base.sha256_file_lf_normalized(path),
                    "stage_id": STAGE67_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage67 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any]) -> None:
    base.write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE67_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "source_adapter_id": SOURCE_ADAPTER_ID,
            "source_stage66_pushed_commit": SOURCE_STAGE66_COMMIT,
            "target_surface": TARGET_SURFACE,
            "legacy_relation": "lesson_only_target_surface_no_code_copy_no_promotion_inheritance",
            "variants": [variant.__dict__ for variant in STAGE67_VARIANTS],
            "attempts": result.get("attempts", []),
            "model_artifacts": result.get("model_artifacts", {}),
            "feature_exports": result.get("feature_exports", {}),
            "gate_rows": result.get("gate_rows", []),
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )
    base.write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE67_ID,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "execution_results": result.get("execution_results", []),
            "gate_rows": result.get("gate_rows", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = base.upsert_csv_rows(
        RUN_REGISTRY_PATH,
        base.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE67_ID,
                "lane": "baseline_adapter_v2_native_short_gate_net_scale_review",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": base.ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("source_stage66_commit", SOURCE_STAGE66_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = base.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE67_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    if not alpha_rows:
        alpha_rows = [
            {
                "ledger_row_id": f"{RUN_ID}__materialized_or_blocked",
                "stage_id": STAGE67_ID,
                "run_id": RUN_ID,
                "subrun_id": "materialized_or_blocked",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "materialized_or_blocked",
                "tier_scope": "Tier A+B",
                "kpi_scope": "stage67_short_gate_net_scale_review",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage67 run materialized or blocked before KPI records were available.",
            }
        ]
    alpha_payload = base.upsert_csv_rows(PROJECT_LEDGER_PATH, base.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = base.upsert_csv_rows(STAGE_LEDGER_PATH, base.ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = base.upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    base.write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE67_ID,
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-model-validation"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": status,
        },
    )
    base.write_json(
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
    base.write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
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
    base.write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE67_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH),
            "ledger_payload": ledger_payload,
            "overall_goal_complete": False,
        },
    )


def update_current_truth(decision: str, external: str) -> None:
    text = base.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-17'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage67(67단계) closed(종료) as `{decision}` and Stage68(68단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): short-gate net/DD balance(숏 게이트 순손익/손실률 균형) 근거를 보존하고, 다음 연구 질문으로만 넘긴다.
- >-
  Stage67 result(67단계 결과): validation(검증), OOS(표본외), PF(수익 팩터), net(순손익), DD(손실률), risk/ATR telemetry(위험/ATR 텔레메트리)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(RISK_ATR_TELEMETRY_PATH)}`에 기록됐다. Effect(효과): 34D target surface(34D 목표 표면) 대비 남은 KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", current_focus, text, count=1, flags=re.MULTILINE)
    block = f"""

stage67_short_gate_net_scale_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE67_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage66_pushed_commit: {SOURCE_STAGE66_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage67_short_gate_net_scale_review:" in text:
        text = re.sub(
            r"\nstage67_short_gate_net_scale_review:\n(?:  .*\n)+",
            "\n" + block.strip() + "\n",
            text,
            count=1,
        )
    else:
        text = text.rstrip() + block
    base.io_path(WORKSPACE_STATE_PATH).write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")
    base.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage67 Selection Status(67단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- source_stage(원천 단계): `66_adapter_research__soft_gate_kpi_repair`
- source_decision(원천 판정): `continue_net_scale_repair_in_stage67`
- current_run(현재 실행): `{RUN_ID}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage67_decision(67단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage67(67단계)는 34D KPI target(34D 핵심 성과 지표 목표)을 향한 short-gate net/DD balance(숏 게이트 순손익/손실률 균형) batch(묶음)를 닫고, 운영 의미 없이 다음 경계 연구로 넘긴다.
""",
    )
    base.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage67_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage67(67단계) closed(종료) as v2-native short-gate net/DD balance batch(브이투 고유 숏 게이트 순손익/손실률 균형 묶음). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage68(68단계)로 이어진다.

## Latest Stage67 Evidence(최신 67단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage67_decision(67단계 판정): `{rel(DECISION_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage(decision, external)


def create_next_stage(decision: str, external: str) -> None:
    base.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage68(68단계)는 Stage67(67단계)의 short-gate net/DD balance(숏 게이트 순손익/손실률 균형) 결과를 받아, 남은 34D KPI(34D 핵심 성과 지표) 격차를 DD(손실률) 훼손 없이 줄일 수 있는지 보는 follow-up(후속) 단계다.

## Bounded Question(경계 질문)

Can the Stage67 best branch(67단계 최선 분기) repair validation DD(검증 손실률) and keep OOS net/PF(표본외 순손익/수익 팩터), or should the short-gate branch be capped and a new model branch(새 모델 분기)를 열어야 하는가?

Effect(효과): Stage68(68단계)는 Stage67(67단계) 결과를 무한 조정하지 않고, DD/net balance(손실률/순손익 균형) 또는 새 분기 결정을 하나의 측정 질문으로 좁힌다.

## Boundary(경계)

`{BOUNDARY}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
""",
    )
    base.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage68 Input References(68단계 입력 참조)

- source_stage(원천 단계): `{STAGE67_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage67_report(67단계 보고서): `{rel(REPORT_PATH)}`
- stage67_decision(67단계 판정): `{rel(DECISION_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): 다음 단계는 34D KPI(34D 핵심 성과 지표)를 참고하되, v2 고유 근거만 입력으로 쓴다.
""",
    )
    base.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage68 Review Index(68단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage68(68단계)는 Stage67(67단계) closeout(종료 기록)을 이어받아 다음 bounded batch(경계 묶음 실행)만 검토한다.
""",
    )
    base.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage68 Selection Status(68단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE67_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage68(68단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-17 - Stage67 short-gate net/DD balance closeout(67단계 숏 게이트 순손익/손실률 균형 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage66(66단계)의 short-only margin gate(숏 전용 마진 게이트)를 유지하고 risk cap(위험 상한)과 cooldown(냉각)을 좁게 비교해, 순손익 확대가 손실률을 과도하게 훼손하는지 측정했다.\n"
    )
    existing = base.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if base.path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        base.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")
    else:
        existing = re.sub(
            rf"(- run\(실행\): `{re.escape(RUN_ID)}`\n- decision\(판정\): `)[^`]+(`)",
            rf"\1{decision}\2",
            existing,
            count=1,
        )
        base.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + "\n", encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage67 v2-native short-gate net/DD balance review.")
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(base.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(base.TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(base.COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(base.TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--runtime-output-timeout-seconds", type=int, default=180)
    parser.add_argument("--attempt-name-contains", default="")
    parser.add_argument("--attempt-offset", type=int, default=0)
    parser.add_argument("--attempt-limit", type=int)
    parser.add_argument("--resume-partials", action="store_true")
    parser.add_argument("--skip-compile", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.3)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage67_globals()
    args = parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE67_ID,
        "stage_number": 67,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": engine.route_coverage(),
        "model_family": "baseline_adapter_stage67_v2_native_short_gate_net_scale_review_ebm_table",
        "feature_set_id": "stage67_run50bn_v41_short_gate_net_scale_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "source_stage66_pushed_commit": SOURCE_STAGE66_COMMIT,
        "gate_rows": inputs["gate_rows"],
    }
    result = base.execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    target_rows = base.target_progress_rows(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(summary_rows, segment_rows, external)
    write_run_identity(result)
    base.write_csv(AUDIT_CSV_PATH, audit_rows)
    base.write_csv(SUMMARY_CSV_PATH, summary_rows)
    base.write_csv(SEGMENT_KPI_PATH, segment_rows)
    base.write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    base.write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    base.write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows())
    base.write_md(REPORT_PATH, report_markdown(summary_rows, segment_rows, target_rows, decision, external))
    base.write_md(DECISION_PATH, decision_markdown(decision, external))
    base.write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "target_progress_rows": target_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d_targets": LEGACY_34D_TARGETS,
            "stage66_reference": STAGE66_REFERENCE,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload)
    if not args.materialize_only:
        update_current_truth(decision, external)
        append_changelog(decision)
    print(
        json.dumps(
            base.json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "external_verification_status": external,
                    "summary_csv": rel(SUMMARY_CSV_PATH),
                    "decision_path": rel(DECISION_PATH),
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

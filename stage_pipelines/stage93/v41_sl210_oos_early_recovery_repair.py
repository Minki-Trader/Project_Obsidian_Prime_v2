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

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage70 import new_model_branch_from_short_gate_limit as base  # noqa: E402


STAGE_ID = "93_adapter_research__v41_sl210_oos_early_recovery_repair"
RUN_NUMBER = "run93A"
RUN_ID = "run93A_stage93_v41_sl210_oos_early_recovery_repair_v1"
PACKET_ID = "stage93_v41_sl210_oos_early_recovery_repair_v1"
PARENT_RUN_ID = "run92A_stage92_v41_sl205_net_recovery_followup_review_v1"
SOURCE_STAGE92_ID = "92_adapter_research__v41_sl205_net_recovery_followup_review"
SOURCE_STAGE92_CLOSEOUT_COMMIT = "82efcbd8ec102d31401f186b400de6c956e4aeda"
SOURCE_STAGE92_LATEST_COMMIT = "030c5305c4bf60bc4a091f4e467542e9e7f621f6"
SOURCE_STAGE91_CLOSEOUT_COMMIT = "8eacc51919b7cd1bfb675eaefcdfc6efadf65f38"
SOURCE_STAGE91_LATEST_COMMIT = "fe792bfadabc91b41c23a7e54a95f4026053cc2d"
NEXT_STAGE_ID = "94_adapter_research__v41_sl210_oos_early_followup_review"
NEXT_RUN_ID = "run94A_stage94_v41_sl210_oos_early_followup_review_v1"
NEXT_PACKET_ID = "stage94_v41_sl210_oos_early_followup_review_v1"
SOURCE_ADAPTER_ID = "s91_v41_h3_risk475_gate08_sl210_tp38_cd10"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
COMMON_ROOT = f"OPV2/s93a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage93_v41_sl210_oos_early_recovery_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage93_v41_sl210_oos_early_recovery_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage93_v41_sl210_oos_early_recovery_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage93_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage93_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage93_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage93_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage93_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage93_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

SOURCE_RUN_ROOT = Path("stages") / "59AR_adapter_repair__new_model_branch_from_stage59aq" / "02_runs/run59AM"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / "s59ar_v41_sd8_h3"
SOURCE_MODEL = SOURCE_VARIANT_ROOT / "models/v41_v22_midcov_et40_agree_h2c0_no_b_stage56_context_timed_event_signal_discrete_score_table.csv"
SOURCE_VAL_INI = SOURCE_VARIANT_ROOT / "mt5/s59ar_v41_sd8_h3_ta_val.ini"
SOURCE_OOS_INI = SOURCE_VARIANT_ROOT / "mt5/s59ar_v41_sd8_h3_ta_oos.ini"

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s93_v41_h3_risk475_gate08_sl210_tp40_cd10",
        label="run50BN_v41_h3_risk475_gate08_sl210_tp40_cd10",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.10,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=10,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage93 SL2.10 OOS early recovery repair: combine SL2.10 validation recovery with TP4.0 clue.",
    ),
    repair.RepairVariant(
        adapter_id="s93_v41_h3_risk475_gate08_sl210_tp39_cd10",
        label="run50BN_v41_h3_risk475_gate08_sl210_tp39_cd10",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.10,
        atr_take_profit_multiplier=3.9,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=10,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage93 SL2.10 OOS early recovery repair: midpoint TP3.9 between TP3.8 and TP4.0.",
    ),
    repair.RepairVariant(
        adapter_id="s93_v41_h3_risk475_gate08_sl2075_tp40_cd10",
        label="run50BN_v41_h3_risk475_gate08_sl2075_tp40_cd10",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=10,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage93 SL2.10 OOS early recovery repair: midpoint SL2.075 with TP4.0 OOS early clue.",
    ),
)
SOURCE_SPECS_BY_VARIANT = {
    variant.adapter_id: {
        "label": "v41_v22_midcov_et40_agree_h2c0_no_b",
        "feature_anchor": "s59ar_v41_sd8_h3_stage59d_adapter",
        "variant_root": SOURCE_VARIANT_ROOT,
        "model": SOURCE_MODEL,
        "validation_ini": SOURCE_VAL_INI,
        "oos_ini": SOURCE_OOS_INI,
    }
    for variant in VARIANTS
}

CONTEXT_GATE_SPECS = {
    variant.adapter_id: {
        "gate_column": "stage93_gate_margin_lt_008_short",
        "gate_type": "margin",
        "threshold": 0.08,
        "block_mode": "short",
        "description": f"v41 source; block shorts if et40_decision_margin < 0.08; {variant.label}",
    }
    for variant in VARIANTS
}


def rel(path: Path) -> str:
    return base.rel(path)


def write_md(path: Path, text: str) -> None:
    base.write_md(path, text)


def write_json(path: Path, payload: Any) -> None:
    base.write_json(path, payload)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    base.write_csv(path, rows, columns)


def configure_base() -> None:
    base.STAGE70_ID = STAGE_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.RUN_ID = RUN_ID
    base.PACKET_ID = PACKET_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.NEXT_STAGE_ID = NEXT_STAGE_ID
    base.NEXT_RUN_ID = NEXT_RUN_ID
    base.NEXT_PACKET_ID = NEXT_PACKET_ID
    base.SOURCE_ADAPTER_ID = SOURCE_ADAPTER_ID
    base.TARGET_SURFACE = TARGET_SURFACE
    base.BOUNDARY = BOUNDARY
    base.DEVELOPMENT_ANCHOR = "v41_v22_midcov_et40_agree_h2c0_no_b"
    base.BACKUP_ANCHOR = "s73_v41_h3_risk5_gate08_tp35"
    base.STAGE_ROOT = STAGE_ROOT
    base.RUN_ROOT = RUN_ROOT
    base.REVIEWS_ROOT = REVIEWS_ROOT
    base.SELECTED_ROOT = SELECTED_ROOT
    base.SPEC_ROOT = SPEC_ROOT
    base.INPUT_ROOT = INPUT_ROOT
    base.PACKET_ROOT = PACKET_ROOT
    base.RUN50BN_ROOT = SOURCE_RUN_ROOT
    base.SOURCE_SPECS_BY_VARIANT = SOURCE_SPECS_BY_VARIANT
    base.STAGE70_VARIANTS = VARIANTS
    base.MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}
    base.CONTEXT_GATE_SPECS = CONTEXT_GATE_SPECS
    base.COMMON_ROOT = COMMON_ROOT
    base.SUMMARY_JSON_PATH = SUMMARY_JSON_PATH
    base.SUMMARY_CSV_PATH = SUMMARY_CSV_PATH
    base.REPORT_PATH = REPORT_PATH
    base.SEGMENT_KPI_PATH = SEGMENT_KPI_PATH
    base.RISK_ATR_TELEMETRY_PATH = RISK_ATR_TELEMETRY_PATH
    base.GATE_FEATURE_SUMMARY_PATH = GATE_FEATURE_SUMMARY_PATH
    base.TIER_B_DIAGNOSTIC_PATH = TIER_B_DIAGNOSTIC_PATH
    base.DECISION_PATH = DECISION_PATH
    base.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    base.STAGE_LEDGER_PATH = STAGE_LEDGER_PATH
    base.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH
    base.PROJECT_LEDGER_PATH = PROJECT_LEDGER_PATH
    base.ARTIFACT_REGISTRY_PATH = ARTIFACT_REGISTRY_PATH
    base.WORKSPACE_STATE_PATH = WORKSPACE_STATE_PATH
    base.CURRENT_WORKING_STATE_PATH = CURRENT_WORKING_STATE_PATH
    base.CHANGELOG_PATH = CHANGELOG_PATH
    base.NEXT_STAGE_ROOT = NEXT_STAGE_ROOT
    base.configure_reused_engine()


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage93_due_to_incomplete_runtime"
    best = base.best_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    val_pf = s58.as_float(val.get("profit_factor"), 0.0) or 0.0
    oos_pf = s58.as_float(oos.get("profit_factor"), 0.0) or 0.0
    val_net = s58.as_float(val.get("net_profit"), 0.0) or 0.0
    oos_net = s58.as_float(oos.get("net_profit"), 0.0) or 0.0
    val_dd = s58.as_float(val.get("max_drawdown_percent"), 99.0) or 99.0
    oos_dd = s58.as_float(oos.get("max_drawdown_percent"), 99.0) or 99.0
    reasons = base.engine.repair_failure_reasons(summary_rows, segment_rows)
    if val_net >= 930 and oos_net >= 580 and val_dd <= 22.8 and oos_dd <= 20.8 and val_pf >= 1.50 and oos_pf >= 1.54 and not reasons:
        return "proceed_to_stage94_sl210_oos_early_followup_review"
    if val_net >= 850 and oos_net >= 540 and val_dd <= 23.5 and oos_dd <= 21.0 and val_pf >= 1.45 and oos_pf >= 1.48:
        return "continue_sl210_oos_early_followup_review_in_stage94"
    if val_pf < 1.0 or val_net <= 0:
        return "open_new_model_source_branch_in_stage94"
    return "continue_sl210_oos_early_followup_review_in_stage94"


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    best = base.best_variant(summary_rows)
    table = []
    for row in summary_rows:
        if row.get("view") != "actual_routed_total":
            continue
        table.append(
            "| {adapter} | {split} | {pf:.4f} | {net:.2f} | {dd:.2f} | {exp:.4f} | {gap:.4f} |".format(
                adapter=row.get("adapter_id"),
                split=row.get("split"),
                pf=s58.as_float(row.get("profit_factor"), 0.0) or 0.0,
                net=s58.as_float(row.get("net_profit"), 0.0) or 0.0,
                dd=s58.as_float(row.get("max_drawdown_percent"), 0.0) or 0.0,
                exp=s58.as_float(row.get("expectancy"), 0.0) or 0.0,
                gap=next(
                    (
                        s58.as_float(t.get("pf_gap_to_34d_latest"), 0.0) or 0.0
                        for t in target_rows
                        if t.get("adapter_id") == row.get("adapter_id") and t.get("split") == row.get("split")
                    ),
                    0.0,
                ),
            )
        )
    reasons = base.engine.repair_failure_reasons(summary_rows, segment_rows)
    variants = ", ".join(variant.adapter_id for variant in VARIANTS)
    return f"""# Stage93 V41 SL2.10 OOS Early Recovery Repair Report(93단계 V41 손절 2.10 표본외 초반 회복 수리 보고서)

- run(실행): `{RUN_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- source_stage(원천 단계): `{SOURCE_STAGE92_ID}`
- source_stage92_closeout_commit(원천 92단계 종료 커밋): `{SOURCE_STAGE92_CLOSEOUT_COMMIT}`
- source_stage92_latest_commit(원천 92단계 최신 커밋): `{SOURCE_STAGE92_LATEST_COMMIT}`
- source_stage91_closeout_commit(원천 91단계 종료 커밋): `{SOURCE_STAGE91_CLOSEOUT_COMMIT}`
- source_stage91_latest_commit(원천 91단계 최신 커밋): `{SOURCE_STAGE91_LATEST_COMMIT}`
- variants(변형): `{variants}`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Target Read(목표 판독)

Stage92(92단계)는 SL2.10(손절 2.10)이 validation recovery(검증 회복) 단서이고 TP4.0(익절 4.0)이 OOS early(표본외 초반) 단서라고 판정했다. Effect(효과): Stage93(93단계)는 두 단서를 조합해 OOS early flatline risk(표본외 초반 평탄화 위험)를 좁게 수리한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
{chr(10).join(table)}

## Read(판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- weakness_reasons(약점 이유): `{';'.join(reasons) if reasons else 'none'}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- tier_b_diagnostic(Tier B 진단): `{rel(TIER_B_DIAGNOSTIC_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage93 Decision(93단계 판정)

decision(판정): `{decision}`

Stage93(93단계)는 Stage92(92단계) 판정에 따라 SL2.10 validation recovery(손절 2.10 검증 회복)와 TP4.0 OOS early clue(익절 4.0 표본외 초반 단서)를 좁게 결합했다.

Effect(효과): 이번 단계 결과는 operating claim(운영 주장)이 아니라, 다음 bounded research(경계 연구) 근거만 만든다.

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
    coverage = base.engine.route_coverage()
    for variant in VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_v41_sl210_oos_early_recovery_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage93 isolates v41 SL2.10 OOS early recovery first; Tier B fallback remains diagnostic and disabled.",
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
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage93_v41_sl210_oos_early_recovery_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage93 v2-native v41 SL2.10 OOS early recovery repair artifact.",
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
                    "notes": "Actual Stage93 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any]) -> None:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "source_stage92_closeout_commit": SOURCE_STAGE92_CLOSEOUT_COMMIT,
            "source_stage92_latest_commit": SOURCE_STAGE92_LATEST_COMMIT,
            "source_stage91_closeout_commit": SOURCE_STAGE91_CLOSEOUT_COMMIT,
            "source_stage91_latest_commit": SOURCE_STAGE91_LATEST_COMMIT,
            "source_adapter_id": SOURCE_ADAPTER_ID,
            "target_surface": TARGET_SURFACE,
            "legacy_relation": "lesson_only_target_surface_no_code_copy_no_promotion_inheritance",
            "variants": [variant.__dict__ for variant in VARIANTS],
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
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
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
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_sl210_oos_early_recovery_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("source_stage92_closeout_commit", SOURCE_STAGE92_CLOSEOUT_COMMIT),
                        ("source_stage92_latest_commit", SOURCE_STAGE92_LATEST_COMMIT),
                        ("source_stage91_closeout_commit", SOURCE_STAGE91_CLOSEOUT_COMMIT),
                        ("source_stage91_latest_commit", SOURCE_STAGE91_LATEST_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = build_mt5_alpha_ledger_rows(
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
                "kpi_scope": "stage93_v41_sl210_oos_early_recovery_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage93 run materialized or blocked before KPI records were available.",
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
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment_design", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-exploration-mandate", "obsidian-performance-attribution", "obsidian-model-validation"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"], "status": status})
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "claim_boundary": BOUNDARY})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "legacy_relation": "lesson_only_target_surface_no_code_copy", "forbidden_claims": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "operating_reference", "runtime_authority", "legacy_inheritance"]})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage92_closeout_commit": SOURCE_STAGE92_CLOSEOUT_COMMIT, "source_stage92_latest_commit": SOURCE_STAGE92_LATEST_COMMIT, "source_stage91_closeout_commit": SOURCE_STAGE91_CLOSEOUT_COMMIT, "source_stage91_latest_commit": SOURCE_STAGE91_LATEST_COMMIT, "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "ledger_payload": ledger_payload, "overall_goal_complete": False})


def create_next_stage(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage94(94단계)는 Stage93(93단계)의 SL2.10 OOS early recovery repair(손절 2.10 표본외 초반 회복 수리) 결과를 review gate(검토 게이트)로만 판독하는 follow-up(후속) 단계다.

## Bounded Question(경계 질문)

Stage93(93단계)의 SL2.10/TP4.0 조합(손절 2.10/익절 4.0 조합)이 validation recovery(검증 회복), OOS early(표본외 초반), DD compression(손실률 압축)을 동시에 개선했는가?

Effect(효과): Stage94(94단계)는 Stage93(93단계)의 결과를 과장하지 않고 다음 판단으로만 좁힌다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage94 Input References(94단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage93_report(93단계 보고서): `{rel(REPORT_PATH)}`
- stage93_decision(93단계 판정): `{rel(DECISION_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage94(94단계)는 v2 고유 근거만 이어받아 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속한다.
""",
    )
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage94 Review Index(94단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage94(94단계)는 Stage93(93단계) closeout(종료 기록)을 이어받아 다음 bounded review(경계 검토)만 수행한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage94 Selection Status(94단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage94(94단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""")


def update_current_truth(decision: str, external: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-17'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage93(93단계) closed(종료) as `{decision}` and Stage94(94단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): v41 SL2.10 OOS early recovery repair(V41 손절 2.10 표본외 초반 회복 수리) 근거를 보존하고 다음 경계 연구 질문으로만 넘긴다.
- >-
  Stage93 result(93단계 결과): validation/OOS(검증/표본외), PF/net/DD(수익 팩터/순손익/손실률), risk/ATR telemetry(위험/ATR 텔레메트리)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(RISK_ATR_TELEMETRY_PATH)}`에 기록된다. Effect(효과): 34D target surface(34D 목표 표면) 대비 KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", current_focus, text, count=1, flags=re.MULTILINE)
    block = f"""

stage93_v41_sl210_oos_early_recovery_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage92_closeout_commit: {SOURCE_STAGE92_CLOSEOUT_COMMIT}
  source_stage92_latest_commit: {SOURCE_STAGE92_LATEST_COMMIT}
  source_stage91_closeout_commit: {SOURCE_STAGE91_CLOSEOUT_COMMIT}
  source_stage91_latest_commit: {SOURCE_STAGE91_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage93_v41_sl210_oos_early_recovery_repair:" in text:
        text = re.sub(r"\nstage93_v41_sl210_oos_early_recovery_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block
    io_path(WORKSPACE_STATE_PATH).write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8-sig")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage93 Selection Status(93단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE92_ID}`
- source_decision(원천 판정): `continue_sl210_tp40_oos_early_recovery_repair_in_stage93`
- source_stage92_closeout_commit(원천 92단계 종료 커밋): `{SOURCE_STAGE92_CLOSEOUT_COMMIT}`
- source_stage92_latest_commit(원천 92단계 최신 커밋): `{SOURCE_STAGE92_LATEST_COMMIT}`
- source_stage91_closeout_commit(원천 91단계 종료 커밋): `{SOURCE_STAGE91_CLOSEOUT_COMMIT}`
- source_stage91_latest_commit(원천 91단계 최신 커밋): `{SOURCE_STAGE91_LATEST_COMMIT}`
- current_run(현재 실행): `{RUN_ID}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage93_decision(93단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage93(93단계)는 v41 SL2.10 OOS early recovery repair(V41 손절 2.10 표본외 초반 회복 수리)를 측정하고, 운영 의미 없이 Stage94(94단계)로 넘긴다.
""")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage93_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage93(93단계) closed(종료) as v2-native v41 SL2.10 OOS early recovery repair batch(브이투 고유 브이41 손절 2.10 표본외 초반 회복 수리 묶음). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage94(94단계)로 이어진다.

## Latest Stage93 Evidence(최신 93단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage93_decision(93단계 판정): `{rel(DECISION_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage93 v41 SL2.10 OOS early recovery repair closeout(93단계 v41 손절 2.10 표본외 초반 회복 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage92(92단계)의 판정대로 SL2.10 validation recovery(손절 2.10 검증 회복)와 TP4.0 OOS early clue(익절 4.0 표본외 초반 단서)를 좁게 결합해 측정했다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    return base.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    configure_base()
    args = parse_args(argv or sys.argv[1:])
    inputs = base.prepare_inputs(Path(args.common_files_root))
    attempts = base.build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 93,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage93_v2_native_v41_sl210_oos_early_recovery_repair_ebm_table",
        "feature_set_id": "stage93_v41_sl210_oos_early_recovery_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
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
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows())
    write_md(REPORT_PATH, report_markdown(summary_rows, segment_rows, target_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(SUMMARY_JSON_PATH, {"run_id": RUN_ID, "decision": decision, "external_verification_status": external, "summary_rows": summary_rows, "segment_rows": segment_rows, "target_progress_rows": target_rows, "gate_rows": inputs["gate_rows"], "legacy_34d_targets": base.LEGACY_34D_TARGETS, "claim_boundary": BOUNDARY})
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload)
    if not args.materialize_only:
        update_current_truth(decision, external)
        append_changelog(decision)
    print(json.dumps(json_ready({"status": "ok" if external == "completed" else "blocked", "run_id": RUN_ID, "decision": decision, "external_verification_status": external, "summary_csv": rel(SUMMARY_CSV_PATH), "decision_path": rel(DECISION_PATH)}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

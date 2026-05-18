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
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage136 import stage122_survivor_trade_count_concentration_repair as s136  # noqa: E402


s122 = s136.s122
s100 = s136.s100

STAGE_ID = "138_adapter_research__trade_supply_repair_after_stage136_no_gain"
RUN_NUMBER = "run138A"
RUN_ID = "run138A_stage138_trade_supply_repair_after_stage136_no_gain_v1"
PACKET_ID = "stage138_trade_supply_repair_after_stage136_no_gain_v1"
PARENT_RUN_ID = "run137A_stage137_stage136_trade_count_concentration_followup_review_v1"
SOURCE_STAGE137_ID = "137_adapter_research__stage136_trade_count_concentration_followup_review"
SOURCE_STAGE137_CLOSEOUT_COMMIT = "7cd9f72aebf247970ac57d93d249569ff3d3859e"
SOURCE_STAGE137_LATEST_COMMIT = "685ae86bd49fb58eb70668efc7d8b69706753396"
SOURCE_STAGE136_ID = "136_adapter_research__stage122_survivor_trade_count_concentration_repair"
SOURCE_STAGE136_CLOSEOUT_COMMIT = "fd3728e2aa224b1dede8ee6c36d3aabfab710124"
SOURCE_STAGE136_LATEST_COMMIT = "bd39fb842cc24ba70a25771541c4255ac71f4a85"
SOURCE_ADAPTER_ID = "s136_control_sht54_lng52_cd5_h3_risk035"
NEXT_STAGE_ID = "139_adapter_research__stage138_trade_supply_followup_review"
NEXT_RUN_ID = "run139A_stage139_stage138_trade_supply_followup_review_v1"
NEXT_PACKET_ID = "stage139_stage138_trade_supply_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s138a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage138_trade_supply_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage138_trade_supply_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage138_trade_supply_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage138_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage138_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage138_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage138_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage138_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage138_trade_audit.csv"
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
STAGE136_SOURCE = {
    "profit_factor": 1.747830217,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
    "validation_profit_factor": 1.58255668,
    "validation_net_profit": 1392.66,
    "validation_trade_count": 263,
    "validation_late_net_share": 897.14 / 1392.66,
}
STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s138_control_sht54_lng52_cd5_h3_risk035",
        label="stage138_control_stage136_lifecycle",
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
        notes="Stage138 control: preserve Stage136 lifecycle so trade supply deltas are isolated.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s138_flat_exit_h3_cd5_risk035",
        label="stage138_flat_exit_h3_cd5_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=True,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage138 bounded repair: close flat signals to free capital and test lifecycle bottleneck.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s138_reverse_opposite_h3_cd5_risk035",
        label="stage138_reverse_opposite_h3_cd5_risk035",
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
        notes="Stage138 bounded repair: allow opposite-signal reversal to test blocked trade supply.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s138_flat_reverse_h2_cd3_risk035",
        label="stage138_flat_reverse_h2_cd3_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=3,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=True,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=2,
        notes="Stage138 bounded repair: strongest lifecycle supply probe with flat exits, reversals, and shorter hold.",
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
    variant.adapter_id: {
        "gate_column": f"stage138_gate_session_margin_{variant.adapter_id}",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": f"Stage138 trade supply lifecycle repair: {variant.label}.",
    }
    for variant in VARIANTS
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
    return STAGE136_SOURCE if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


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


def validation_late_share(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> float:
    full = next(
        (
            row
            for row in segment_rows
            if row.get("adapter_id") == adapter_id
            and row.get("split") == "validation_is"
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "full_split"
        ),
        {},
    )
    late = segment_row(segment_rows, adapter_id, "validation_is", "late")
    return as_float(late, "net_profit") / as_float(full, "net_profit", 1.0)


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
                magic = 13810000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=138,
                        exploration_label="stage138_BaselineAdapter__TradeSupplyRepairAfterStage136NoGain",
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
                        extra_set_values=s122.s120.stage120_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage138(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        late_share = validation_late_share(segment_rows, adapter_id)
        oos_trade_gain = as_float(oos, "trade_count") - STAGE136_SOURCE["trade_count"]
        val_trade_gain = as_float(val, "trade_count") - STAGE136_SOURCE["validation_trade_count"]
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
                safe and oos_trade_gain >= 20 and val_trade_gain >= 0 and late_share <= 0.62,
                safe and oos_trade_gain > 0,
                oos_trade_gain,
                val_trade_gain,
                -late_share,
                -as_float(oos, "max_drawdown_percent", 99.0),
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:8])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage139_runtime_repair_due_to_incomplete_runtime"
    best = best_stage138(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    late_share = validation_late_share(segment_rows, adapter_id)
    oos_trade_gain = as_float(best, "trade_count") - STAGE136_SOURCE["trade_count"]
    val_trade_gain = as_float(val, "trade_count") - STAGE136_SOURCE["validation_trade_count"]
    safe = (
        as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(best, "max_drawdown_percent", 99.0) <= 16.5
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
    )
    if safe and oos_trade_gain >= 20 and val_trade_gain >= 0 and late_share <= 0.62:
        return "proceed_to_stage139_trade_supply_followup_review_with_material_gain_candidate_not_final"
    if safe and oos_trade_gain > 0:
        return "proceed_to_stage139_trade_supply_followup_review_with_small_gain_candidate_not_final"
    return "continue_stage139_trade_supply_repair_after_damage_or_no_gain_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val trades(검증 거래 수) | val late share(검증 후반 비중) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | trade gain(거래 증가) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        gain = as_float(oos, "trade_count") - STAGE136_SOURCE["trade_count"]
        lines.append(
            "| {adapter} | {val_pf:.6f} | {val_net:.2f} | {val_trades:.0f} | {late:.3f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} |".format(
                adapter=adapter_id,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                val_trades=as_float(val, "trade_count"),
                late=validation_late_share(segment_rows, adapter_id),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=as_float(oos, "trade_count"),
                gain=gain,
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage138(summary_rows, segment_rows)
    return f"""# Stage138 Trade Supply Repair Report(138단계 거래 공급 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage137(원천 137단계): `{SOURCE_STAGE137_ID}`
- source_stage136_adapter(원천 136단계 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can lifecycle repair(생명주기 수리) increase trade supply(거래 공급) after Stage136(136단계) threshold/cooldown(임계값/대기시간) repair failed to add trades?

Effect(효과): threshold/cooldown(임계값/대기시간)을 또 반복하지 않고, close-on-flat(평탄 신호 청산), reverse-on-opposite(반대 신호 반전), shorter hold(짧은 보유)가 거래 수 병목인지 좁게 확인한다.

## KPI Table(KPI 핵심 성과 지표 표)

{row_table(summary_rows, segment_rows)}

## Read(판독)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- oos_trade_gain_vs_stage136(136단계 대비 미래구간 거래 증가): `{as_float(best, "trade_count") - STAGE136_SOURCE["trade_count"]:.0f}`
- oos_gap_to_34d_trades(34D 거래 수 차이): `{as_float(best, "trade_count") - LEGACY_34D["trade_count"]:.0f}`
- overall_goal_complete(전체 목표 완료): `false`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`

Stage138(138단계)는 research/development(연구개발) 측정 단계다. Effect(효과): 좋은 결과가 나와도 최종 패키지나 운영 주장은 만들지 않고 Stage139(139단계) 검토로 넘긴다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage138 Decision(138단계 판정)

decision(판정): `{decision}`

Stage138(138단계)는 trade supply repair(거래 공급 수리)를 lifecycle(생명주기) 관점에서만 측정했다. Effect(효과): 결과가 좋든 나쁘든 Stage139(139단계)에서 거래 증가가 품질을 망가뜨렸는지 따로 검토한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage137_closeout_commit(원천 137단계 종료 커밋): `{SOURCE_STAGE137_CLOSEOUT_COMMIT}`
- source_stage137_latest_commit(원천 137단계 최신 커밋): `{SOURCE_STAGE137_LATEST_COMMIT}`
- source_stage136_latest_commit(원천 136단계 최신 커밋): `{SOURCE_STAGE136_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


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
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage138_trade_supply_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage138 v2-native trade supply lifecycle repair artifact.",
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
                    "notes": "Actual Stage138 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_stage138_trade_supply_lifecycle_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage137_closeout_commit", SOURCE_STAGE137_CLOSEOUT_COMMIT),
                        ("source_stage137_latest_commit", SOURCE_STAGE137_LATEST_COMMIT),
                        ("source_stage136_latest_commit", SOURCE_STAGE136_LATEST_COMMIT),
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_stage138_trade_supply_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage138 isolates Tier A routed lifecycle supply before Tier B fallback repair.",
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
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "judgment_label": "trade_supply_lifecycle_repair_measured_not_final",
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
            "overall_goal_complete": False,
        },
    )
    s122.s108.write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage137_closeout_commit": SOURCE_STAGE137_CLOSEOUT_COMMIT,
            "source_stage137_latest_commit": SOURCE_STAGE137_LATEST_COMMIT,
            "source_stage136_latest_commit": SOURCE_STAGE136_LATEST_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def write_stage139_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage139(139단계)는 Stage138(138단계) trade supply repair(거래 공급 수리) 결과를 follow-up review(후속 검토)로 판정한다.

## Bounded Question(경계 질문)

Did Stage138(138단계) increase trade count(거래 수) without damaging PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 원격측정), and concentration(집중도)?

Effect(효과): Stage138(138단계) 안에서 계속 고치지 않고, 결과를 보존한 뒤 다음 수리 축을 하나만 고른다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage139 Input References(139단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- stage138_decision(138단계 판정): `{rel(DECISION_PATH)}`
- stage138_report(138단계 보고서): `{rel(REPORT_PATH)}`
- stage138_summary(138단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage138_segment_kpi(138단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage138_risk_atr_telemetry(138단계 위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage139 Review Index(139단계 검토 색인)

- status(상태): `open_planned`
- source_stage(원천 단계): `{STAGE_ID}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage139(139단계)는 새 실험이 아니라 Stage138(138단계) 증거 판독으로 시작한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage139 Selection Status(139단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage138`
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
  Stage138(138단계) closed(종료) as `{decision}` and Stage139(139단계) `{NEXT_STAGE_ID}` is open_planned(열린 계획). Effect(효과): trade supply repair(거래 공급 수리) 결과를 보존하고 새 판독 단계로 넘긴다.
- >-
  Stage138 evidence(138단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 대비 거래 수 격차가 줄었는지 분리해서 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on:.*$", "updated_on: '2026-05-18'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    block = f"""
stage138_trade_supply_repair_after_stage136_no_gain:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage137_closeout_commit: {SOURCE_STAGE137_CLOSEOUT_COMMIT}
  source_stage137_latest_commit: {SOURCE_STAGE137_LATEST_COMMIT}
  source_stage136_latest_commit: {SOURCE_STAGE136_LATEST_COMMIT}
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

stage139_stage138_trade_supply_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage138
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run139A_stage139_stage138_trade_supply_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage138_trade_supply_repair_after_stage136_no_gain:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage139_stage138_trade_supply_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage138 Selection Status(138단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE137_ID}`
- source_stage136_adapter(원천 136단계 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage138_decision(138단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage138(138단계)는 닫고, 전체 목표 완료나 운영 주장은 만들지 않는다.
""",
    )
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage138 Review Index(138단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage138(138단계) 산출물 위치를 한 곳에서 재진입할 수 있게 한다.
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
- adapter_under_review(검토 중 어댑터): `stage138_trade_supply_repair_candidate`
- status(상태): `stage138_closed_{decision}_stage139_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage138(138단계)는 trade supply repair(거래 공급 수리)를 lifecycle(생명주기) 축으로 측정했다. Effect(효과): 결과가 좋아도 final package(최종 패키지)나 operating claim(운영 주장)이 아니라 Stage139(139단계) 검토로 넘긴다.

## Latest Stage138 Evidence(최신 138단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    write_stage139_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage138 trade supply repair closeout(138단계 거래 공급 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage136/137(136/137단계)에서 남은 거래 수 부족을 lifecycle(생명주기) 축으로 측정하고 Stage139(139단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def configure_stage138() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE135_ID": SOURCE_STAGE137_ID,
        "SOURCE_STAGE135_CLOSEOUT_COMMIT": SOURCE_STAGE137_CLOSEOUT_COMMIT,
        "SOURCE_STAGE135_LATEST_COMMIT": SOURCE_STAGE137_LATEST_COMMIT,
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
        "STAGE135_SOURCE": STAGE136_SOURCE,
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s136, name, value)

    s136.source_baseline = source_baseline
    s136.best_stage136 = best_stage138
    s136.decide = decide
    s136.row_table = row_table
    s136.report_markdown = report_markdown
    s136.decision_markdown = decision_markdown
    s136.update_current_truth = update_current_truth
    s136.append_changelog = append_changelog

    s122.build_attempts = build_attempts
    s122.artifact_rows = artifact_rows
    s122.write_ledgers = write_ledgers
    s122.tier_b_rows = tier_b_rows
    s122.write_packet_files = write_packet_files
    s136.configure_stage136()
    s122.s120.build_attempts = build_attempts
    s122.s120.artifact_rows = artifact_rows
    s122.s120.write_ledgers = write_ledgers
    s122.s120.tier_b_rows = tier_b_rows
    s122.s120.write_packet_files = write_packet_files


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage138()
    code = s122.s120.main(argv)
    write_stage139_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

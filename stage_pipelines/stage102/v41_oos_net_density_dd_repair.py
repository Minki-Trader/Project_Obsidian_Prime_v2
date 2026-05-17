from __future__ import annotations

import json
import re
import sys
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
from stage_pipelines.stage100 import v41_oos_early_context_gate_runtime_repair as s100  # noqa: E402


STAGE_ID = "102_adapter_research__v41_oos_net_density_dd_repair"
RUN_NUMBER = "run102A"
RUN_ID = "run102A_stage102_v41_oos_net_density_dd_repair_v1"
PACKET_ID = "stage102_v41_oos_net_density_dd_repair_v1"
PARENT_RUN_ID = "run101A_stage101_v41_context_gate_followup_review_v1"
SOURCE_STAGE101_ID = "101_adapter_research__v41_context_gate_followup_review"
SOURCE_STAGE101_CLOSEOUT_COMMIT = "30470ff25b02787f2aabfe8d78d1bf729c36bc72"
SOURCE_STAGE101_LATEST_COMMIT = "172104e12a1f8dda9352d5f84c668d2467a7adb3"
SOURCE_STAGE100_CLOSEOUT_COMMIT = "85d881d1b0df85768f8fb38dfe0afe6a7877a7fd"
SOURCE_STAGE100_LATEST_COMMIT = "ef4b4ab1fbcb63a985512af5a6c49d199533e1fd"
SOURCE_ADAPTER_ID = "s100_v41_h3_cd8_lng_early_adx20"
NEXT_STAGE_ID = "103_adapter_research__v41_oos_net_density_followup_review"
NEXT_RUN_ID = "run103A_stage103_v41_oos_net_density_followup_review_v1"
NEXT_PACKET_ID = "stage103_v41_oos_net_density_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s102a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage102_oos_net_density_dd_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage102_oos_net_density_dd_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage102_oos_net_density_dd_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage102_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage102_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage102_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage102_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage102_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage102_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s102_v41_h3_cd7_lng_early_adx20",
        label="stage102_cd7_long_early_adx_lt20_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=7,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage102 repair: keep early ADX<20 long gate, relax same-direction cooldown from 8 to 7.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s102_v41_h3_cd6_lng_early_adx20",
        label="stage102_cd6_long_early_adx_lt20_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=6,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage102 repair: keep early ADX<20 long gate, relax same-direction cooldown from 8 to 6.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s102_v41_h3_cd8_lng_early_adx18",
        label="stage102_cd8_long_early_adx_lt18_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage102 repair: keep cooldown 8 but lighten the early long ADX block from <20 to <18.",
    ),
)

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
    "s102_v41_h3_cd7_lng_early_adx20": {
        "gate_column": "stage102_gate_long_early_adx_lt20_cd7",
        "gate_type": "long_session_adx",
        "session_min": 0.0,
        "session_max": 110.0,
        "adx_max": 20.0,
        "short_margin_threshold": 0.08,
        "block_mode": "both",
        "description": "Preserve Stage97 short margin gate and block long if source signal is long, minutes_from_cash_open in (0,110], and adx_14 < 20; cooldown 7.",
    },
    "s102_v41_h3_cd6_lng_early_adx20": {
        "gate_column": "stage102_gate_long_early_adx_lt20_cd6",
        "gate_type": "long_session_adx",
        "session_min": 0.0,
        "session_max": 110.0,
        "adx_max": 20.0,
        "short_margin_threshold": 0.08,
        "block_mode": "both",
        "description": "Preserve Stage97 short margin gate and block long if source signal is long, minutes_from_cash_open in (0,110], and adx_14 < 20; cooldown 6.",
    },
    "s102_v41_h3_cd8_lng_early_adx18": {
        "gate_column": "stage102_gate_long_early_adx_lt18_cd8",
        "gate_type": "long_session_adx",
        "session_min": 0.0,
        "session_max": 110.0,
        "adx_max": 18.0,
        "short_margin_threshold": 0.08,
        "block_mode": "both",
        "description": "Preserve Stage97 short margin gate and block long if source signal is long, minutes_from_cash_open in (0,110], and adx_14 < 18; cooldown 8.",
    },
}

STAGE100_BEST = {
    "adapter_id": "s100_v41_h3_cd8_lng_early_adx20",
    "validation_net": 1289.00,
    "validation_pf": 1.723000,
    "validation_dd_pct": 16.46,
    "oos_net": 605.06,
    "oos_pf": 1.584029,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 149,
}

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def configure_stage102() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
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
    }.items():
        setattr(s100, name, value)
    s100.SOURCE_STAGE99_ID = SOURCE_STAGE101_ID
    s100.SOURCE_STAGE99_CLOSEOUT_COMMIT = SOURCE_STAGE101_CLOSEOUT_COMMIT
    s100.SOURCE_STAGE99_LATEST_COMMIT = SOURCE_STAGE101_LATEST_COMMIT
    s100.COMMON_ROOT = COMMON_ROOT
    s100.build_attempts = build_attempts
    s100.decide = decide
    s100.report_markdown = report_markdown
    s100.decision_markdown = decision_markdown
    s100.artifact_rows = artifact_rows
    s100.write_ledgers = write_ledgers
    s100.write_packet_files = write_packet_files
    s100.update_current_truth = update_current_truth
    s100.append_changelog = append_changelog


def stage102_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
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
                magic = 10210000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=102,
                        exploration_label="stage102_BaselineAdapter__OosNetDensityDdRepair",
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
                        extra_set_values=stage102_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_oos(summary_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row
        for row in summary_rows
        if row.get("view") == "actual_routed_total"
        and row.get("split") == "oos"
        and row.get("status") == "completed"
    ]
    if not candidates:
        return {}
    return max(
        candidates,
        key=lambda row: (
            s100.s58.as_float(row.get("profit_factor"), 0.0) or 0.0,
            s100.s58.as_float(row.get("net_profit"), 0.0) or 0.0,
            -(s100.s58.as_float(row.get("max_drawdown_percent"), 999.0) or 999.0),
        ),
    )


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_oos_net_density_runtime_repair_in_stage103_due_to_incomplete_runtime"
    best = best_oos(summary_rows)
    oos_pf = s100.s58.as_float(best.get("profit_factor"), 0.0) or 0.0
    oos_net = s100.s58.as_float(best.get("net_profit"), 0.0) or 0.0
    oos_dd = s100.s58.as_float(best.get("max_drawdown_percent"), 99.0) or 99.0
    oos_trades = s100.s58.as_float(best.get("trade_count"), 0.0) or 0.0
    if (
        oos_pf >= LEGACY_34D["profit_factor"]
        and oos_net >= LEGACY_34D["net_profit"]
        and oos_dd <= LEGACY_34D["max_drawdown_percent"]
    ):
        return "continue_research_package_review_in_stage103"
    if oos_net > STAGE100_BEST["oos_net"] and oos_pf >= 1.55 and oos_dd <= 22.0 and oos_trades >= STAGE100_BEST["oos_trade_count"]:
        return "continue_oos_net_density_followup_review_in_stage103"
    return "continue_oos_net_density_repair_review_in_stage103"


def row_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | expectancy(기대값) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        if row.get("view") != "actual_routed_total":
            continue
        lines.append(
            "| {adapter} | {split} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades} | {exp:.4f} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                pf=s100.s58.as_float(row.get("profit_factor"), 0.0) or 0.0,
                net=s100.s58.as_float(row.get("net_profit"), 0.0) or 0.0,
                dd=s100.s58.as_float(row.get("max_drawdown_percent"), 0.0) or 0.0,
                trades=row.get("trade_count", ""),
                exp=s100.s58.as_float(row.get("expectancy"), 0.0) or 0.0,
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_oos(summary_rows)
    best_id = str(best.get("adapter_id", "none"))
    oos_net = s100.s58.as_float(best.get("net_profit"), 0.0) or 0.0
    oos_pf = s100.s58.as_float(best.get("profit_factor"), 0.0) or 0.0
    oos_dd = s100.s58.as_float(best.get("max_drawdown_percent"), 0.0) or 0.0
    oos_trades = s100.s58.as_float(best.get("trade_count"), 0.0) or 0.0
    return f"""# Stage102 OOS Net Density/DD Repair Report(102단계 표본외 순손익 밀도/손실률 수리 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE101_ID}`
- source_stage101_closeout_commit(원천 101단계 종료 커밋): `{SOURCE_STAGE101_CLOSEOUT_COMMIT}`
- source_stage101_latest_commit(원천 101단계 최신 커밋): `{SOURCE_STAGE101_LATEST_COMMIT}`
- source_stage100_latest_commit(원천 100단계 최신 커밋): `{SOURCE_STAGE100_LATEST_COMMIT}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage100 best(100단계 최선)의 OOS PF(표본외 수익 팩터)를 보존하면서 OOS net(표본외 순손익), trade density(거래 밀도), DD%(손실률)를 34D target surface(34D 목표 표면)에 더 가깝게 만들 수 있는가?

Effect(효과): Stage102(102단계)는 세 가지 변형만 실제 MT5 runtime(실행환경)으로 재측정한다.

## Result Table(결과 표)

{row_table(summary_rows)}

## Best Read(최선 판독)

- best_variant(최선 변형): `{best_id}`
- oos_pf(표본외 수익 팩터): `{oos_pf:.6f}` versus stage100_best(100단계 최선) `{STAGE100_BEST['oos_pf']:.6f}` and 34D latest(34D 최신) `{LEGACY_34D['profit_factor']}`
- oos_net(표본외 순손익): `{oos_net:.2f}` versus stage100_best(100단계 최선) `{STAGE100_BEST['oos_net']:.2f}` and 34D latest(34D 최신) `{LEGACY_34D['net_profit']}`
- oos_dd_pct(표본외 손실률): `{oos_dd:.2f}` versus stage100_best(100단계 최선) `{STAGE100_BEST['oos_dd_pct']:.2f}` and 34D latest(34D 최신) `{LEGACY_34D['max_drawdown_percent']}`
- oos_trade_count(표본외 거래 수): `{oos_trades:.0f}` versus stage100_best(100단계 최선) `{STAGE100_BEST['oos_trade_count']}`

## Decision(판정)

decision(판정): `{decision}`

Stage102(102단계)는 전체 목표 완료가 아니다. Effect(효과): 성공이면 Stage103(103단계)에서 후속 검토로 고정하고, 부족하면 다음 좁은 수리로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage102 Decision(102단계 판정)

decision(판정): `{decision}`

Stage102(102단계)는 Stage101(101단계)의 판정대로 OOS net density(표본외 순손익 밀도)와 DD(손실률)를 좁게 수리했다.

Effect(효과): Stage100(100단계) 개선을 전체 완료로 오해하지 않고, 실제 MT5 runtime(실행환경) 근거를 다음 Stage103(103단계) 검토로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(제한문 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = s100.base.utc_now()
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
                    "artifact_type": "stage102_v41_oos_net_density_dd_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage102 v2-native OOS net density/DD repair artifact.",
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
                    "notes": "Actual Stage102 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_v2_native_v41_oos_net_density_dd_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("source_stage101_closeout_commit", SOURCE_STAGE101_CLOSEOUT_COMMIT),
                        ("source_stage101_latest_commit", SOURCE_STAGE101_LATEST_COMMIT),
                        ("source_stage100_latest_commit", SOURCE_STAGE100_LATEST_COMMIT),
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
                "kpi_scope": "stage102_v41_oos_net_density_dd_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage102 run materialized or blocked before KPI records were available.",
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
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation", "obsidian-runtime-parity"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": status,
        },
    )
    write_json(
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
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
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
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage101_closeout_commit": SOURCE_STAGE101_CLOSEOUT_COMMIT,
            "source_stage101_latest_commit": SOURCE_STAGE101_LATEST_COMMIT,
            "source_stage100_closeout_commit": SOURCE_STAGE100_CLOSEOUT_COMMIT,
            "source_stage100_latest_commit": SOURCE_STAGE100_LATEST_COMMIT,
            "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def create_next_stage(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage103(103단계)는 Stage102(102단계)의 actual MT5 runtime result(실제 MT5 실행환경 결과)를 follow-up review(후속 검토)로 판독한다.

## Bounded Question(경계 질문)

Stage102(102단계)의 OOS net density/DD repair(표본외 순손익 밀도/손실률 수리)가 Stage100 best(100단계 최선)보다 개선됐는가, 아니면 다른 좁은 수리 또는 분기가 필요한가?

Effect(효과): Stage103(103단계)은 새 최적화가 아니라 실제 실행 결과의 판정과 다음 좁은 경로 선택만 맡는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage103 Input References(103단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage102_report(102단계 보고서): `{rel(REPORT_PATH)}`
- stage102_summary(102단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage103(103단계)은 실제 runtime(실행환경) 결과만 받아 34D KPI(34D 핵심 성과 지표) 격차 축소 여부를 판정한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage103 Review Index(103단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage103(103단계)은 Stage102(102단계) closeout(종료 기록)을 이어받아 후속 판정만 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage103 Selection Status(103단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage103(103단계)은 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage102(102단계) closed(종료) as `{decision}` and Stage103(103단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): OOS net density/DD repair(표본외 순손익 밀도/손실률 수리) 결과를 후속 검토로 넘긴다.
- >-
  Stage102 result(102단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록된다. Effect(효과): Stage100 best(100단계 최선) 및 34D target surface(34D 목표 표면) 대비 KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage102_v41_oos_net_density_dd_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage101_closeout_commit: {SOURCE_STAGE101_CLOSEOUT_COMMIT}
  source_stage101_latest_commit: {SOURCE_STAGE101_LATEST_COMMIT}
  source_stage100_closeout_commit: {SOURCE_STAGE100_CLOSEOUT_COMMIT}
  source_stage100_latest_commit: {SOURCE_STAGE100_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage102_v41_oos_net_density_dd_repair:"
    if marker in text:
        text = re.sub(r"\nstage102_v41_oos_net_density_dd_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage102 Selection Status(102단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE101_ID}`
- source_decision(원천 판정): `continue_oos_net_density_dd_repair_in_stage102`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage102_decision(102단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage102(102단계)은 실제 실행 결과를 기록하고, 운영 의미 없이 Stage103(103단계)로 넘긴다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage102_oos_net_density_dd_surface`
- status(상태): `stage102_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage102(102단계) closed(종료) as v2-native v41 OOS net density/DD repair(브이투 고유 브이41 표본외 순손익 밀도/손실률 수리). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage103(103단계)로 이어진다.

## Latest Stage102 Evidence(최신 102단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage102 v41 OOS net density/DD repair closeout(102단계 v41 표본외 순손익 밀도/손실률 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage100(100단계)의 PF(수익 팩터) 개선을 보존하며 OOS net/DD/trade density(표본외 순손익/손실률/거래 밀도) 수리를 실제 MT5 runtime(실행환경)으로 측정하고 Stage103(103단계) 후속 검토로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage102()
    s100.configure_base()
    return s100.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

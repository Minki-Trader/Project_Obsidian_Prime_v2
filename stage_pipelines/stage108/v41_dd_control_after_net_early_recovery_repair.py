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
from stage_pipelines.stage104 import v41_oos_early_segment_repair as s104  # noqa: E402
from stage_pipelines.stage106 import v41_oos_net_density_dd_after_early_recovery_repair as s106  # noqa: E402


s100 = s104.s100

STAGE_ID = "108_adapter_research__v41_dd_control_after_net_early_recovery_repair"
RUN_NUMBER = "run108A"
RUN_ID = "run108A_stage108_v41_dd_control_after_net_early_recovery_repair_v1"
PACKET_ID = "stage108_v41_dd_control_after_net_early_recovery_repair_v1"
PARENT_RUN_ID = "run107A_stage107_v41_oos_net_density_dd_followup_review_v1"
SOURCE_STAGE107_ID = "107_adapter_research__v41_oos_net_density_dd_followup_review"
SOURCE_STAGE107_CLOSEOUT_COMMIT = "6af2f17a497baacff8f1ad4089c97a36bad95398"
SOURCE_STAGE107_LATEST_COMMIT = "728d4cba5b3361ba5eaf49561ea8b2d2282b6343"
SOURCE_STAGE106_CLOSEOUT_COMMIT = "5123f0df630b214a225194202717c3b6bcf7df00"
SOURCE_STAGE106_LATEST_COMMIT = "0e34739b13eaf7d8c7d9bfb48bf168396122d17a"
SOURCE_STAGE104_LATEST_COMMIT = "61778183dc73e327b612f58b70491a2f14408de2"
SOURCE_STAGE102_LATEST_COMMIT = "5ca329c468db459a8f68b9c28dd0897dfbf79623"
SOURCE_ADAPTER_ID = "s106_v41_h3_cd9_lng_early_adx19"
NEXT_STAGE_ID = "109_adapter_research__v41_dd_control_followup_review"
NEXT_RUN_ID = "run109A_stage109_v41_dd_control_followup_review_v1"
NEXT_PACKET_ID = "stage109_v41_dd_control_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s108a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage108_dd_control_after_net_early_recovery_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage108_dd_control_after_net_early_recovery_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage108_dd_control_after_net_early_recovery_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage108_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage108_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage108_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage108_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage108_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage108_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

STAGE104_BALANCED = {
    "oos_net": 614.67,
    "oos_pf": 1.593270725,
    "oos_dd_pct": 18.69,
    "oos_early_net": 32.51,
    "oos_early_pf": 1.128143477,
}
STAGE106_NET_PF_BEST = {
    "adapter_id": "s106_v41_h3_cd9_lng_early_adx19",
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
    "oos_early_net": 38.84,
    "oos_early_pf": 1.157011764,
}
STAGE106_DD_BEST = {
    "adapter_id": "s106_v41_h4_cd8_lng_early_adx19",
    "oos_net": 615.72,
    "oos_pf": 1.551824268,
    "oos_dd_pct": 16.06,
    "oos_trade_count": 147,
    "oos_early_net": 57.13,
    "oos_early_pf": 1.198058589,
}
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s108_v41_h4_cd9_lng_early_adx19",
        label="stage108_h4_cd9_long_early_adx_lt19_direct_blend",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=4,
        notes="Stage108 direct blend: preserve Stage106 cooldown 9 net clue and add hold 4 drawdown clue.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s108_v41_h4_cd10_lng_early_adx19",
        label="stage108_h4_cd10_long_early_adx_lt19_dd_pressure",
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
        max_hold_bars=4,
        notes="Stage108 pressure: hold 4 plus cooldown 10 tests whether fewer same-direction reentries reduce DD.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s108_v41_h3_cd10_lng_early_adx19",
        label="stage108_h3_cd10_long_early_adx_lt19_cooldown_only",
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
        notes="Stage108 control: keep hold 3 and press cooldown only from 9 to 10.",
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
    "s108_v41_h4_cd9_lng_early_adx19": {
        "gate_column": "stage108_gate_long_early_adx_lt19_h4_cd9",
        "gate_type": "long_session_adx",
        "session_min": 0.0,
        "session_max": 110.0,
        "adx_max": 19.0,
        "short_margin_threshold": 0.08,
        "block_mode": "both",
        "description": "Preserve Stage97 short margin gate and block long if source signal is long, minutes_from_cash_open in (0,110], and adx_14 < 19; max hold 4; cooldown 9.",
    },
    "s108_v41_h4_cd10_lng_early_adx19": {
        "gate_column": "stage108_gate_long_early_adx_lt19_h4_cd10",
        "gate_type": "long_session_adx",
        "session_min": 0.0,
        "session_max": 110.0,
        "adx_max": 19.0,
        "short_margin_threshold": 0.08,
        "block_mode": "both",
        "description": "Preserve Stage97 short margin gate and block long if source signal is long, minutes_from_cash_open in (0,110], and adx_14 < 19; max hold 4; cooldown 10.",
    },
    "s108_v41_h3_cd10_lng_early_adx19": {
        "gate_column": "stage108_gate_long_early_adx_lt19_h3_cd10",
        "gate_type": "long_session_adx",
        "session_min": 0.0,
        "session_max": 110.0,
        "adx_max": 19.0,
        "short_margin_threshold": 0.08,
        "block_mode": "both",
        "description": "Preserve Stage97 short margin gate and block long if source signal is long, minutes_from_cash_open in (0,110], and adx_14 < 19; max hold 3; cooldown 10.",
    },
}


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def configure_stage108() -> None:
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
        "STAGE100_EARLY": {
            "oos_early_net": STAGE104_BALANCED["oos_early_net"],
            "oos_early_pf": STAGE104_BALANCED["oos_early_pf"],
            "oos_early_mfe_capture": 0.06074909558,
        },
        "STAGE104_BALANCED": STAGE104_BALANCED,
        "STAGE102_BEST": {
            "oos_net": 639.85,
            "oos_pf": 1.612695342,
            "oos_dd_pct": 18.56,
        },
        "LEGACY_34D": LEGACY_34D,
    }.items():
        setattr(s106, name, value)
    s106.SOURCE_STAGE105_ID = SOURCE_STAGE107_ID
    s106.SOURCE_STAGE105_CLOSEOUT_COMMIT = SOURCE_STAGE107_CLOSEOUT_COMMIT
    s106.SOURCE_STAGE105_LATEST_COMMIT = SOURCE_STAGE107_LATEST_COMMIT
    s106.SOURCE_STAGE104_CLOSEOUT_COMMIT = SOURCE_STAGE106_CLOSEOUT_COMMIT
    s106.SOURCE_STAGE104_LATEST_COMMIT = SOURCE_STAGE106_LATEST_COMMIT
    s106.SOURCE_STAGE102_LATEST_COMMIT = SOURCE_STAGE102_LATEST_COMMIT
    s106.build_attempts = build_attempts
    s106.decide = decide
    s106.report_markdown = report_markdown
    s106.decision_markdown = decision_markdown
    s106.artifact_rows = artifact_rows
    s106.write_ledgers = write_ledgers
    s106.write_packet_files = write_packet_files
    s106.update_current_truth = update_current_truth
    s106.append_changelog = append_changelog
    s106.configure_stage106()


def stage108_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
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
                magic = 10810000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=108,
                        exploration_label="stage108_BaselineAdapter__DdControlAfterNetEarlyRecoveryRepair",
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
                        extra_set_values=stage108_extra_set_values(variant, magic),
                    )
                )
    return attempts


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = s100.s58.as_float(row.get(key), default)
    return default if value is None else float(value)


def routed_oos(summary_rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [
        row
        for row in summary_rows
        if row.get("view") == "actual_routed_total" and row.get("split") == "oos" and row.get("status") == "completed"
    ]


def early_segment(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> Mapping[str, Any]:
    for row in segment_rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == "oos"
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == "early"
        ):
            return row
    return {}


def early_ok(early: Mapping[str, Any]) -> bool:
    tolerance = 1e-9
    return (
        as_float(early, "profit_factor") + tolerance >= STAGE104_BALANCED["oos_early_pf"]
        and as_float(early, "net_profit") + tolerance >= STAGE104_BALANCED["oos_early_net"]
    )


def best_balanced(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in routed_oos(summary_rows):
        early = early_segment(segment_rows, str(row.get("adapter_id", "")))
        oos_net = as_float(row, "net_profit")
        oos_pf = as_float(row, "profit_factor")
        oos_dd = as_float(row, "max_drawdown_percent", 99.0)
        candidates.append(
            (
                early_ok(early),
                oos_pf >= LEGACY_34D["profit_factor"],
                oos_net >= STAGE104_BALANCED["oos_net"],
                STAGE106_NET_PF_BEST["oos_dd_pct"] - oos_dd,
                oos_pf,
                oos_net,
                as_float(early, "net_profit"),
                row,
            )
        )
    return max(candidates, key=lambda item: item[:7])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_dd_control_runtime_repair_in_stage109_due_to_incomplete_runtime"
    best = best_balanced(summary_rows, segment_rows)
    early = early_segment(segment_rows, str(best.get("adapter_id", "")))
    oos_net = as_float(best, "net_profit")
    oos_pf = as_float(best, "profit_factor")
    oos_dd = as_float(best, "max_drawdown_percent", 99.0)
    if (
        early_ok(early)
        and oos_net >= STAGE106_NET_PF_BEST["oos_net"]
        and oos_pf >= STAGE106_NET_PF_BEST["oos_pf"]
        and oos_dd <= STAGE106_DD_BEST["oos_dd_pct"]
    ):
        return "continue_dd_control_followup_review_in_stage109"
    if (
        early_ok(early)
        and oos_net >= STAGE104_BALANCED["oos_net"]
        and oos_pf >= LEGACY_34D["profit_factor"]
        and oos_dd < STAGE106_NET_PF_BEST["oos_dd_pct"]
    ):
        return "continue_dd_control_followup_review_in_stage109"
    return "continue_dd_control_repair_review_in_stage109"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | early PF(초반 수익 팩터) | early net(초반 순손익) | early ok(초반 통과) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in routed_oos(summary_rows):
        early = early_segment(segment_rows, str(row.get("adapter_id", "")))
        lines.append(
            "| {adapter} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd:.2f} | {trades:.0f} | {early_pf:.6f} | {early_net:.2f} | {early_ok} |".format(
                adapter=row.get("adapter_id", ""),
                oos_pf=as_float(row, "profit_factor"),
                oos_net=as_float(row, "net_profit"),
                oos_dd=as_float(row, "max_drawdown_percent"),
                trades=as_float(row, "trade_count"),
                early_pf=as_float(early, "profit_factor"),
                early_net=as_float(early, "net_profit"),
                early_ok="yes" if early_ok(early) else "no",
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_balanced(summary_rows, segment_rows)
    early = early_segment(segment_rows, str(best.get("adapter_id", "")))
    return f"""# Stage108 DD Control After Net/Early Recovery Repair Report(108단계 손실률 제어 후속 수리 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE107_ID}`
- source_stage107_closeout_commit(원천 107단계 종료 커밋): `{SOURCE_STAGE107_CLOSEOUT_COMMIT}`
- source_stage107_latest_commit(원천 107단계 최신 커밋): `{SOURCE_STAGE107_LATEST_COMMIT}`
- source_stage106_latest_commit(원천 106단계 최신 커밋): `{SOURCE_STAGE106_LATEST_COMMIT}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Hypothesis(가설)

Stage106(106단계)의 `h3_cd9`는 OOS net/PF/early(표본외 순손익/수익 팩터/초반)를 보존했지만 DD(손실률)는 `18.69`로 남았다. `h4_cd8`는 DD(손실률)를 `16.06`까지 낮췄지만 PF/net(수익 팩터/순손익)을 훼손했다.

Effect(효과): Stage108(108단계)은 새 모델 탐색(model hunting, 모델 탐색)이 아니라 `hold 4(보유 4봉)`와 `cooldown 9/10(쿨다운 9/10봉)`만 좁게 조합한다.

## Result Table(결과 표)

{row_table(summary_rows, segment_rows)}

## Best Balanced Read(균형 최선 판독)

- best_balanced_variant(균형 최선 변형): `{best.get("adapter_id", "none")}`
- oos_pf(표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(표본외 손실률): `{as_float(best, "max_drawdown_percent"):.2f}`
- early_pf(초반 수익 팩터): `{as_float(early, "profit_factor"):.6f}`
- early_net(초반 순손익): `{as_float(early, "net_profit"):.2f}`
- stage106_net_gap(106단계 순손익 최선 대비): `{as_float(best, "net_profit") - STAGE106_NET_PF_BEST["oos_net"]:.2f}`
- stage106_dd_gap(106단계 손실률 최선 대비): `{as_float(best, "max_drawdown_percent") - STAGE106_DD_BEST["oos_dd_pct"]:.2f}`
- early_floor_preserved(초반 바닥 보존): `{"yes" if early_ok(early) else "no"}`

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage108 DD control after net/early recovery repair(108단계 손실률 제어 후속 수리).
- evidence_available(있는 근거): MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(빠진 근거): 34D KPI(34D 핵심 성과 지표) 수준의 net/DD/trade density(순손익/손실률/거래 밀도) 동시 충족.
- judgment_label(판정 라벨): `exploratory_repair_continues`.
- claim_boundary(주장 경계): `{BOUNDARY}`.
- next_condition(다음 조건): `{decision}`.

## Decision(판정)

decision(판정): `{decision}`

Stage108(108단계)는 전체 목표 완료가 아니다. Effect(효과): 결과는 Stage109(109단계)에서 후속 검토하고, 부족하면 다음 bounded repair(경계 수리)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage108 Decision(108단계 판정)

decision(판정): `{decision}`

Stage108(108단계)는 Stage107(107단계)의 판정대로 Stage106 net/PF/early(106단계 순손익/수익 팩터/초반) 장점을 보존하면서 DD(손실률)를 좁게 낮추는 조합을 실제 MT5 runtime(실행환경)에서 측정했다.

Effect(효과): 34D KPI(34D 핵심 성과 지표)는 lesson-only target surface(교훈 전용 목표 표면)로만 쓰고, v2-native research(브이투 고유 연구) 경계 안에서 다음 판정을 이어간다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(제한문 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage107_closeout_commit(원천 107단계 종료 커밋): `{SOURCE_STAGE107_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

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
                    "artifact_type": "stage108_v41_dd_control_after_net_early_recovery_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage108 v2-native DD control after net/early recovery repair artifact.",
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
                    "notes": "Actual Stage108 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_v2_native_v41_dd_control_after_net_early_recovery_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("source_stage107_closeout_commit", SOURCE_STAGE107_CLOSEOUT_COMMIT),
                        ("source_stage107_latest_commit", SOURCE_STAGE107_LATEST_COMMIT),
                        ("source_stage106_latest_commit", SOURCE_STAGE106_LATEST_COMMIT),
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
                "kpi_scope": "stage108_v41_dd_control_after_net_early_recovery_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage108 run materialized or blocked before KPI records were available.",
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
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment_design", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation", "obsidian-runtime-parity"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"], "status": status})
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "claim_boundary": BOUNDARY})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "legacy_relation": "lesson_only_target_surface_no_code_copy", "overall_goal_complete": False, "forbidden_claims": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "operating_reference", "runtime_authority", "legacy_inheritance"]})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage107_closeout_commit": SOURCE_STAGE107_CLOSEOUT_COMMIT, "source_stage107_latest_commit": SOURCE_STAGE107_LATEST_COMMIT, "source_stage106_closeout_commit": SOURCE_STAGE106_CLOSEOUT_COMMIT, "source_stage106_latest_commit": SOURCE_STAGE106_LATEST_COMMIT, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage109(109단계)는 Stage108(108단계)의 actual MT5 runtime result(실제 MT5 실행환경 결과)를 후속 검토한다.

## Bounded Question(경계 질문)

Stage108(108단계)의 DD control after net/early recovery repair(손실률 제어 후속 수리)가 Stage106 net/PF best(106단계 순손익/수익 팩터 최선), Stage106 DD best(106단계 손실률 최선), 34D target surface(34D 목표 표면) 대비 어떤 균형을 만들었는가?

Effect(효과): Stage109(109단계)는 새 최적화가 아니라 실제 실행 결과를 판독하고, 다음 bounded repair(경계 수리) 또는 다른 분기를 정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage109 Input References(109단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage108_report(108단계 보고서): `{rel(REPORT_PATH)}`
- stage108_summary(108단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage109(109단계)는 Stage108(108단계) runtime(실행환경) 근거만 받아 34D KPI(34D 핵심 성과 지표) 격차 축소 여부를 판정한다.
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage109 Review Index(109단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage109(109단계)는 Stage108(108단계) closeout(종료 기록)을 이어받아 후속 판정만 수행한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage109 Selection Status(109단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage109(109단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""")


def update_current_truth(decision: str, external: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage108(108단계) closed(종료) as `{decision}` and Stage109(109단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage106(106단계)의 cd9 net/PF/early(쿨다운9 순손익/수익 팩터/초반)와 hold4 DD(보유4 손실률) 단서 조합을 후속 검토로 넘긴다.
- >-
  Stage108 result(108단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록된다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 대비 손실률/순손익/거래 밀도 격차를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage108_v41_dd_control_after_net_early_recovery_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage107_closeout_commit: {SOURCE_STAGE107_CLOSEOUT_COMMIT}
  source_stage107_latest_commit: {SOURCE_STAGE107_LATEST_COMMIT}
  source_stage106_closeout_commit: {SOURCE_STAGE106_CLOSEOUT_COMMIT}
  source_stage106_latest_commit: {SOURCE_STAGE106_LATEST_COMMIT}
  source_stage104_latest_commit: {SOURCE_STAGE104_LATEST_COMMIT}
  source_stage102_latest_commit: {SOURCE_STAGE102_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage108_v41_dd_control_after_net_early_recovery_repair:"
    if marker in text:
        text = re.sub(r"\nstage108_v41_dd_control_after_net_early_recovery_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage108 Selection Status(108단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE107_ID}`
- source_decision(원천 판정): `continue_dd_control_after_net_early_recovery_repair_in_stage108`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage108_decision(108단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage108(108단계)은 실제 실행 결과를 기록하고, 운영 의미 없이 Stage109(109단계)로 넘긴다.
""")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage108_dd_control_after_net_early_recovery_surface`
- status(상태): `stage108_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage108(108단계) closed(종료) as v2-native v41 DD control after net/early recovery repair(브이투 고유 브이41 손실률 제어 후속 수리). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage109(109단계)로 이어진다.

## Latest Stage108 Evidence(최신 108단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage108 v41 DD control after net/early recovery repair closeout(108단계 v41 손실률 제어 후속 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage106(106단계)의 cd9 순손익 단서와 hold4 손실률 단서를 실제 MT5 runtime(실행환경)에서 좁게 조합하고 Stage109(109단계) 후속 검토로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage108()
    s100.configure_base()
    return s100.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

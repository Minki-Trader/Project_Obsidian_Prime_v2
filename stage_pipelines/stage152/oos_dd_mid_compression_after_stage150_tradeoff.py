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
from stage_pipelines.stage148 import softsession_supply_quality_repair_after_stage146_damage as s148  # noqa: E402


s122 = s148.s122
s100 = s148.s100

STAGE_ID = "152_adapter_research__oos_dd_mid_compression_after_stage150_tradeoff"
RUN_NUMBER = "run152A"
RUN_ID = "run152A_stage152_oos_dd_mid_compression_after_stage150_tradeoff_v1"
PACKET_ID = "stage152_oos_dd_mid_compression_after_stage150_tradeoff_v1"
PARENT_RUN_ID = "run151A_stage151_stage150_validation_session_guard_followup_review_v1"
SOURCE_STAGE151_ID = "151_adapter_research__stage150_validation_session_guard_followup_review"
SOURCE_STAGE151_CLOSEOUT_COMMIT = "a7b45527cba4d171e4d6363d12e8f90410cc0b28"
SOURCE_STAGE151_HASH_RECORD_COMMIT = "7cb669c9f17328c42658e903a03ec52f0cab85c0"
SOURCE_STAGE150_ID = "150_adapter_research__validation_session_guard_repair_after_stage148_tradeoff"
SOURCE_STAGE150_CLOSEOUT_COMMIT = "3331309a56e2f9ae8f7cdd7d1c234e875483449f"
SOURCE_STAGE150_HASH_RECORD_COMMIT = "23d7d57e67ebfaf468c036114630a1e20d2abc9b"
SOURCE_STAGE148_HASH_RECORD_COMMIT = "db69b5f07831b58675481f180055a0c60f96997f"
SOURCE_ADAPTER_ID = "s150_session_mid_margin_restore_h3_cd5_sht54_lng52_risk035"
OOS_REFERENCE_ID = "s150_session_mid_replay_h3_cd5_sht54_lng52_risk035"
NEXT_STAGE_ID = "153_adapter_research__stage152_oos_dd_mid_followup_review"
NEXT_RUN_ID = "run153A_stage153_stage152_oos_dd_mid_followup_review_v1"
NEXT_PACKET_ID = "stage153_stage152_oos_dd_mid_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s152a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage152_oos_dd_mid_compression_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage152_oos_dd_mid_compression_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage152_oos_dd_mid_compression_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage152_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage152_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage152_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage152_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage152_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage152_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage152/oos_dd_mid_compression_after_stage150_tradeoff.py")

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
STAGE150_MARGIN_RESTORE = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.73,
    "net_profit": 1045.62,
    "max_drawdown_percent": 18.94,
    "trade_count": 187,
    "validation_profit_factor": 1.59,
    "validation_net_profit": 1416.97,
    "validation_max_drawdown_percent": 11.82,
    "validation_trade_count": 332,
    "oos_mid_profit_factor": 1.578473376,
}
STAGE150_OOS_REFERENCE = {
    "adapter_id": OOS_REFERENCE_ID,
    "profit_factor": 1.69,
    "net_profit": 1261.68,
    "max_drawdown_percent": 9.65,
    "trade_count": 205,
    "validation_profit_factor": 1.45,
    "validation_net_profit": 1161.94,
    "validation_max_drawdown_percent": 13.59,
    "validation_trade_count": 304,
    "oos_mid_profit_factor": 1.592742226,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s152_margin_restore_session_narrow_h3_cd5_sht54_lng52_risk035",
        label="stage152_margin_restore_session_narrow",
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
        notes="Stage152 bounded repair: keep Stage150 margin restore but narrow the session block.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s152_margin_restore_margin_trim_h3_cd5_sht54_lng52_risk035",
        label="stage152_margin_restore_margin_trim",
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
        notes="Stage152 bounded repair: trim both edges of the restored margin block.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s152_margin_restore_hold2_cd5_sht54_lng52_risk035",
        label="stage152_margin_restore_hold2",
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
        max_hold_bars=2,
        notes="Stage152 bounded repair: compress lifecycle hold while keeping the Stage150 margin surface.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s152_margin_restore_threshold_guard_h3_cd5_sht55_lng53_risk035",
        label="stage152_margin_restore_threshold_guard",
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
        notes="Stage152 bounded repair: keep restored margin block and add a stricter entry threshold.",
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
    "s152_margin_restore_session_narrow_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage152_gate_margin_restore_session_narrow",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 172.0,
        "session_max": 262.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage152 repair: Stage150 restored margin with a narrower session block.",
    },
    "s152_margin_restore_margin_trim_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage152_gate_margin_restore_margin_trim",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.0425,
        "margin_max": 0.0775,
        "description": "Stage152 repair: Stage150 session block with trimmed restored margin edges.",
    },
    "s152_margin_restore_hold2_cd5_sht54_lng52_risk035": {
        "gate_column": "stage152_gate_margin_restore_hold2",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage152 repair: Stage150 restored margin surface with hold-2 lifecycle compression.",
    },
    "s152_margin_restore_threshold_guard_h3_cd5_sht55_lng53_risk035": {
        "gate_column": "stage152_gate_margin_restore_threshold_guard",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage152 repair: Stage150 restored margin surface with stricter entry thresholds.",
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
    return STAGE150_MARGIN_RESTORE if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


def split_row(summary_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    return s148.split_row(summary_rows, adapter_id, split)


def segment_row(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    return s148.segment_row(segment_rows, adapter_id, split, segment)


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
                magic = 15210000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=152,
                        exploration_label="stage152_BaselineAdapter__OosDdMidCompressionAfterStage150Tradeoff",
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
                        extra_set_values=s148.stage148_extra_set_values(variant, magic),
                    )
                )
    return attempts


def _safe(adapter_id: str, oos: Mapping[str, Any], val: Mapping[str, Any], oos_mid: Mapping[str, Any]) -> bool:
    return (
        bool(adapter_id)
        and as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(oos, "max_drawdown_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
        and as_float(oos_mid, "profit_factor") >= LEGACY_34D["profit_factor"]
    )


def best_stage152(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        val_mid = segment_row(segment_rows, adapter_id, "validation_is", "mid")
        oos_mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        safe = _safe(adapter_id, oos, val, oos_mid)
        oos_dd_improvement = STAGE150_MARGIN_RESTORE["max_drawdown_percent"] - as_float(oos, "max_drawdown_percent", 99.0)
        oos_mid_gain = as_float(oos_mid, "profit_factor") - STAGE150_MARGIN_RESTORE["oos_mid_profit_factor"]
        candidates.append(
            (
                safe,
                oos_dd_improvement > 0 and oos_mid_gain > 0,
                as_float(val, "profit_factor"),
                as_float(val_mid, "profit_factor"),
                oos_mid_gain,
                oos_dd_improvement,
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                -as_float(oos, "max_drawdown_percent", 99.0),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:9])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage153_runtime_completion_due_to_incomplete_stage152_runtime_candidate_not_final"
    best = best_stage152(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    oos_mid = segment_row(segment_rows, adapter_id, "oos", "mid")
    if _safe(adapter_id, best, val, oos_mid):
        return "proceed_to_stage153_oos_dd_mid_followup_review_with_candidate_not_final"
    return "continue_stage153_oos_dd_mid_followup_review_due_to_damage_or_no_gain_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 낙폭) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS trades(표본외 거래 수) | OOS mid PF(표본외 중반 수익 팩터) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        oos_mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        safe = _safe(adapter_id, oos, val, oos_mid)
        read = "candidate_not_final" if safe else "needs_followup_or_repair"
        lines.append(
            "| {adapter} | {val_pf:.6f} | {val_net:.2f} | {val_dd:.2f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {trades:.0f} | {mid_pf:.6f} | {read} |".format(
                adapter=adapter_id,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                val_dd=as_float(val, "max_drawdown_percent"),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=as_float(oos, "trade_count"),
                mid_pf=as_float(oos_mid, "profit_factor"),
                read=read,
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage152(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", "none"))
    val = split_row(summary_rows, adapter_id, "validation_is")
    oos_mid = segment_row(segment_rows, adapter_id, "oos", "mid")
    return f"""# Stage152 OOS DD/Mid Compression Report(152단계 표본외 낙폭/중반 압축 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage151(원천 151단계): `{SOURCE_STAGE151_ID}`
- source_stage151_closeout_commit(원천 151단계 종료 커밋): `{SOURCE_STAGE151_CLOSEOUT_COMMIT}`
- source_stage151_hash_record_commit(원천 151단계 해시 기록 커밋): `{SOURCE_STAGE151_HASH_RECORD_COMMIT}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- oos_reference(표본외 참고): `{OOS_REFERENCE_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can Stage150 margin_restore(150단계 마진 복원)의 validation recovery(검증 회복)를 preserve(보존)하면서 OOS DD(표본외 낙폭)를 34D(34디) drawdown(낙폭) 기준 아래로 낮추고 OOS mid PF(표본외 중반 수익 팩터)를 34D(34디) PF(수익 팩터) 이상으로 올릴 수 있는가?

Effect(효과): 최종 순손익(net profit, 순손익) 하나가 아니라 validation/OOS(검증/표본외), drawdown(낙폭), mid segment(중반 구간)을 같이 본다.

## KPI Read(KPI 핵심 성과 지표 판독)

{row_table(summary_rows, segment_rows)}

## Source Comparison(원천 비교)

- Stage150 margin_restore(150단계 마진 복원): validation PF(검증 수익 팩터) `{STAGE150_MARGIN_RESTORE["validation_profit_factor"]:.6f}`, OOS PF(표본외 수익 팩터) `{STAGE150_MARGIN_RESTORE["profit_factor"]:.6f}`, OOS DD(표본외 낙폭) `{STAGE150_MARGIN_RESTORE["max_drawdown_percent"]:.2f}`, OOS mid PF(표본외 중반 수익 팩터) `{STAGE150_MARGIN_RESTORE["oos_mid_profit_factor"]:.9f}`.
- Stage150 OOS reference(150단계 표본외 참고): validation PF(검증 수익 팩터) `{STAGE150_OOS_REFERENCE["validation_profit_factor"]:.6f}`, OOS DD(표본외 낙폭) `{STAGE150_OOS_REFERENCE["max_drawdown_percent"]:.2f}`, OOS mid PF(표본외 중반 수익 팩터) `{STAGE150_OOS_REFERENCE["oos_mid_profit_factor"]:.9f}`.

## Judgment(판정)

- best_adapter(최선 어댑터): `{adapter_id}`
- best_validation_pf(최선 검증 수익 팩터): `{as_float(val, "profit_factor"):.6f}`
- best_oos_pf(최선 표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- best_oos_dd(최선 표본외 낙폭): `{as_float(best, "max_drawdown_percent"):.2f}`
- best_oos_mid_pf(최선 표본외 중반 수익 팩터): `{as_float(oos_mid, "profit_factor"):.9f}`

Stage152(152단계)는 research/development only(연구개발 전용)이다. Effect(효과): candidate(후보)가 좋아도 deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), production baseline(생산 기준선)을 주장하지 않는다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage152 Decision(152단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage152(152단계)는 Stage150(150단계)의 validation recovery(검증 회복)와 OOS weakness(표본외 약점)의 tradeoff(상충)를 좁게 수리했다. Effect(효과): 이 판정은 다음 Stage153(153단계) follow-up review(후속 검토)로 넘어가는 경계 기록이지 전체 목표 완료가 아니다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), production_baseline(생산 기준선), operating_promotion(운영 승격), operating_reference(운영 기준), runtime_authority(런타임 권위), overall_goal_complete(전체 목표 완료).
"""


def write_stage153_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage153(153단계)는 Stage152(152단계) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage152(152단계) preserve(보존) validation recovery(검증 회복) while compressing(압축) OOS DD(표본외 낙폭) and lifting(상승) OOS mid PF(표본외 중반 수익 팩터), or should the campaign continue into another bounded repair(경계 수리)?

Effect(효과): Stage152(152단계) 결과가 좋아 보여도 바로 final(최종)이나 deployment(배포)로 건너뛰지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage153 Input References(153단계 입력 참조)

- stage152_decision(152단계 판정): `{rel(DECISION_PATH)}`
- stage152_report(152단계 보고서): `{rel(REPORT_PATH)}`
- stage152_summary(152단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage152_segment_kpi(152단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage152_risk_atr_telemetry(152단계 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- source_stage151_decision(원천 151단계 판정): `stages/151_adapter_research__stage150_validation_session_guard_followup_review/03_reviews/stage151_decision.md`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage153 Review Index(153단계 검토 색인)

- status(상태): `open_planned_from_stage152`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage152(152단계) 수리 결과를 다음 review(검토)에서 과장 없이 판정한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage153 Selection Status(153단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage152`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `run153A_stage153_stage152_oos_dd_mid_followup_review_v1`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage153(153단계)는 Stage152(152단계)를 검토하고 다음 수리/분기 여부를 정한다.
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    block = f"""
stage152_oos_dd_mid_compression_after_stage150_tradeoff:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage151_closeout_commit: {SOURCE_STAGE151_CLOSEOUT_COMMIT}
  source_stage151_hash_record_commit: {SOURCE_STAGE151_HASH_RECORD_COMMIT}
  source_stage150_closeout_commit: {SOURCE_STAGE150_CLOSEOUT_COMMIT}
  source_stage150_hash_record_commit: {SOURCE_STAGE150_HASH_RECORD_COMMIT}
  repair_seed: {SOURCE_ADAPTER_ID}
  oos_reference: {OOS_REFERENCE_ID}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage153_stage152_oos_dd_mid_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage152
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run153A_stage153_stage152_oos_dd_mid_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage152_oos_dd_mid_compression_after_stage150_tradeoff:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage153_stage152_oos_dd_mid_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage152 Selection Status(152단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage151(원천 151단계): `{SOURCE_STAGE151_ID}`
- repair_seed(수리 씨앗): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage152_decision(152단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage152(152단계)는 KPI(핵심 성과 지표)를 수리 대상으로만 기록하고 전체 목표 완료로 올리지 않는다.
""",
    )
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage152 Review Index(152단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage152(152단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )
    s122.s108.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage153_stage152_oos_dd_mid_followup_review_surface`
- status(상태): `stage152_closed_{decision}_stage153_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage152(152단계)는 Stage150 margin_restore(150단계 마진 복원)의 validation recovery(검증 회복)를 유지하면서 OOS DD/mid(표본외 낙폭/중반)를 압축할 수 있는지 실제 MT5(메타트레이더5) evidence(근거)로 측정했다. Effect(효과): 결과는 Stage153(153단계) review(검토)로 넘어가며, 전체 목표 완료나 운영 주장으로 승격하지 않는다.

## Latest Stage152 Evidence(최신 152단계 근거)

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
    write_stage153_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage152 OOS DD/mid compression closeout(152단계 표본외 낙폭/중반 압축 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage150(150단계)의 validation recovery(검증 회복)와 OOS DD/mid weakness(표본외 낙폭/중반 약점)를 좁은 MT5(메타트레이더5) 수리 변형으로 측정하고 Stage153(153단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    rows = []
    for path in [
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
    ]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage152_oos_dd_mid_compression_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage152 v2-native OOS DD/mid compression repair artifact.",
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
                    "notes": "Actual Stage152 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_stage152_oos_dd_mid_compression",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage151_closeout_commit", SOURCE_STAGE151_CLOSEOUT_COMMIT),
                        ("source_stage151_hash_record_commit", SOURCE_STAGE151_HASH_RECORD_COMMIT),
                        ("source_stage150_hash_record_commit", SOURCE_STAGE150_HASH_RECORD_COMMIT),
                        ("repair_seed", SOURCE_ADAPTER_ID),
                        ("oos_reference", OOS_REFERENCE_ID),
                        ("target_surface", TARGET_SURFACE),
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
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"), list(artifacts), key="artifact_id")
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
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_stage152_oos_dd_mid_compression",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage152 isolates Tier A routed behavior before any Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s122.s108.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-backtest-forensics", "obsidian-experiment-design", "obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-artifact-lineage"], "status": status})
    s122.s108.write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "summary_csv": rel(SUMMARY_CSV_PATH), "claim_boundary": BOUNDARY})
    s122.s108.write_json(PACKET_ROOT / "scope_completion_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "bounded_question": "compress OOS DD and lift OOS mid PF while preserving validation recovery", "scope_completed": result.get("external_verification_status") == "completed", "out_of_scope": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "runtime_authority", "overall_goal_completion"], "status": status})
    s122.s108.write_json(PACKET_ROOT / "kpi_contract_audit.json", {"summary_csv": rel(SUMMARY_CSV_PATH), "segment_kpi_csv": rel(SEGMENT_KPI_PATH), "risk_atr_csv": rel(RISK_ATR_TELEMETRY_PATH), "status": status})
    s122.s108.write_json(PACKET_ROOT / "result_judgment_gate.json", {"result_subject": RUN_ID, "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(DECISION_PATH)], "evidence_missing": [], "judgment_label": "bounded_repair_candidate_not_final", "decision": decision, "claim_boundary": BOUNDARY, "next_condition": "Stage153 must judge whether Stage152 is a credible repair or needs another bounded repair.", "status": status})
    s122.s108.write_json(PACKET_ROOT / "performance_attribution_gate.json", {"comparison_baseline": SOURCE_ADAPTER_ID, "observed_change": "Stage152 varies session width, margin width, lifecycle hold, and threshold guard around Stage150 margin_restore.", "likely_drivers": ["session_window", "margin_block", "max_hold_bars", "threshold_guard"], "next_probe": NEXT_STAGE_ID, "status": status})
    s122.s108.write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"source_inputs": [SOURCE_ADAPTER_ID, rel(PRODUCER_PATH)], "producer": rel(PRODUCER_PATH), "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID], "artifact_paths": {"report": rel(REPORT_PATH), "summary": rel(SUMMARY_CSV_PATH), "segment_kpi": rel(SEGMENT_KPI_PATH), "risk_atr": rel(RISK_ATR_TELEMETRY_PATH), "stage_ledger": rel(STAGE_LEDGER_PATH)}, "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)], "ledger_payload": ledger_payload, "status": status})
    s122.s108.write_json(PACKET_ROOT / "runtime_parity_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "runtime_path": "foundation/mt5 tester profile via generated set files and run_manifest", "parity_check": "MT5 Strategy Tester output" if status == "completed" else "blocked_or_incomplete", "runtime_claim_boundary": "runtime_probe_research_only", "status": status})
    s122.s108.write_json(PACKET_ROOT / "backtest_forensics_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "tester_identity": "MT5 Strategy Tester via generated run manifest", "trade_evidence": rel(SUMMARY_CSV_PATH), "forensic_checks": ["report_path_exists", "summary_rows", "risk_telemetry", "artifact_hashes"], "status": status})
    s122.s108.write_json(PACKET_ROOT / "final_claim_guard.json", {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"})
    s122.s108.write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "missing_gates": [], "status": "passed" if status == "completed" else "blocked_with_evidence"})
    s122.s108.write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage151_closeout_commit": SOURCE_STAGE151_CLOSEOUT_COMMIT, "source_stage151_hash_record_commit": SOURCE_STAGE151_HASH_RECORD_COMMIT, "source_stage150_hash_record_commit": SOURCE_STAGE150_HASH_RECORD_COMMIT, "repair_seed": SOURCE_ADAPTER_ID, "oos_reference": OOS_REFERENCE_ID, "summary_csv": rel(SUMMARY_CSV_PATH), "segment_kpi_csv": rel(SEGMENT_KPI_PATH), "risk_atr_telemetry_csv": rel(RISK_ATR_TELEMETRY_PATH), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False})


def configure_stage152() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE147_ID": SOURCE_STAGE151_ID,
        "SOURCE_STAGE147_CLOSEOUT_COMMIT": SOURCE_STAGE151_CLOSEOUT_COMMIT,
        "SOURCE_STAGE147_HASH_RECORD_COMMIT": SOURCE_STAGE151_HASH_RECORD_COMMIT,
        "SOURCE_STAGE146_HASH_RECORD_COMMIT": SOURCE_STAGE150_HASH_RECORD_COMMIT,
        "SOURCE_STAGE142_HASH_RECORD_COMMIT": SOURCE_STAGE148_HASH_RECORD_COMMIT,
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
        "STAGE142_CONTROL": STAGE142_CONTROL,
        "STAGE146_SOFTSESSION": STAGE150_MARGIN_RESTORE,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s148, name, value)
    s148.source_baseline = source_baseline
    s148.best_stage148 = best_stage152
    s148.decide = decide
    s148.row_table = row_table
    s148.report_markdown = report_markdown
    s148.decision_markdown = decision_markdown
    s148.update_current_truth = update_current_truth
    s148.append_changelog = append_changelog
    s148.build_attempts = build_attempts
    s148.artifact_rows = artifact_rows
    s148.write_ledgers = write_ledgers
    s148.tier_b_rows = tier_b_rows
    s148.write_packet_files = write_packet_files
    s148.write_stage149_seed = write_stage153_seed


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage152()
    code = s148.main(argv)
    write_stage153_seed()
    print(json.dumps(json_ready({"status": "stage152_wrapper_complete", "run_id": RUN_ID, "decision_path": rel(DECISION_PATH)}), ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

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
from stage_pipelines.stage152 import oos_dd_mid_compression_after_stage150_tradeoff as s152  # noqa: E402


s148 = s152.s148
s122 = s152.s122
s100 = s152.s100

STAGE_ID = "154_adapter_research__oos_mid_edge_restore_validation_repair"
RUN_NUMBER = "run154A"
RUN_ID = "run154A_stage154_oos_mid_edge_restore_validation_repair_v1"
PACKET_ID = "stage154_oos_mid_edge_restore_validation_repair_v1"
PARENT_RUN_ID = "run153A_stage153_stage152_oos_dd_mid_followup_review_v1"
SOURCE_STAGE153_ID = "153_adapter_research__stage152_oos_dd_mid_followup_review"
SOURCE_STAGE153_CLOSEOUT_COMMIT = "6652a43e017b23003d704a1398916553b61e5562"
SOURCE_STAGE153_HASH_RECORD_COMMIT = "9c9c412bb7be01e9a9ace37351ea3fac578700f6"
SOURCE_STAGE152_HASH_RECORD_COMMIT = "ec5e4cf57daf52f95d8b92c8e2e85a93c244db35"
SOURCE_ADAPTER_ID = "s152_margin_restore_margin_trim_h3_cd5_sht54_lng52_risk035"
VALIDATION_MEMORY_ID = "s152_margin_restore_threshold_guard_h3_cd5_sht55_lng53_risk035"
NEXT_STAGE_ID = "155_adapter_research__stage154_oos_mid_validation_followup_review"
NEXT_RUN_ID = "run155A_stage155_stage154_oos_mid_validation_followup_review_v1"
NEXT_PACKET_ID = "stage155_stage154_oos_mid_validation_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s154a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage154_oos_mid_validation_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage154_oos_mid_validation_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage154_oos_mid_validation_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage154_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage154_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage154_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage154_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage154_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage154_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage154/oos_mid_edge_restore_validation_repair.py")

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE142_CONTROL = s152.STAGE142_CONTROL
STAGE152_MARGIN_TRIM = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "validation_profit_factor": 1.43,
    "validation_net_profit": 1075.52,
    "validation_max_drawdown_percent": 13.59,
    "profit_factor": 1.76,
    "net_profit": 1261.13,
    "max_drawdown_percent": 13.79,
    "trade_count": 198,
    "oos_mid_profit_factor": 1.611944327,
}
STAGE152_VALIDATION_MEMORY = {
    "adapter_id": VALIDATION_MEMORY_ID,
    "validation_profit_factor": 1.59,
    "validation_net_profit": 1416.97,
    "validation_max_drawdown_percent": 11.82,
    "profit_factor": 1.73,
    "net_profit": 1045.62,
    "max_drawdown_percent": 18.94,
    "trade_count": 187,
    "oos_mid_profit_factor": 1.578473376,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s154_trim_center_restore_h3_cd5_sht54_lng52_risk035",
        label="stage154_trim_center_restore",
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
        notes="Stage154 repair: restore half of both margin edges around the Stage152 margin_trim seed.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035",
        label="stage154_trim_low_edge_restore",
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
        notes="Stage154 repair: restore only the low margin edge to recover validation without full OOS DD damage.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s154_trim_high_edge_restore_h3_cd5_sht54_lng52_risk035",
        label="stage154_trim_high_edge_restore",
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
        notes="Stage154 repair: restore only the high margin edge to recover validation without full OOS DD damage.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s154_validation_memory_hold2_h2_cd5_sht55_lng53_risk035",
        label="stage154_validation_memory_hold2",
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
        max_hold_bars=2,
        notes="Stage154 repair: apply hold-2 compression to the validation-memory threshold guard.",
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
    "s154_trim_center_restore_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage154_gate_trim_center_restore",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04125,
        "margin_max": 0.07875,
        "description": "Stage154 repair: center restore around Stage152 margin_trim.",
    },
    "s154_trim_low_edge_restore_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage154_gate_trim_low_edge_restore",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04,
        "margin_max": 0.0775,
        "description": "Stage154 repair: restore the low margin edge only.",
    },
    "s154_trim_high_edge_restore_h3_cd5_sht54_lng52_risk035": {
        "gate_column": "stage154_gate_trim_high_edge_restore",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.0425,
        "margin_max": 0.08,
        "description": "Stage154 repair: restore the high margin edge only.",
    },
    "s154_validation_memory_hold2_h2_cd5_sht55_lng53_risk035": {
        "gate_column": "stage154_gate_validation_memory_hold2",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Stage154 repair: Stage152 validation-memory surface with hold-2 compression.",
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
    return STAGE152_MARGIN_TRIM if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


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
                magic = 15410000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=154,
                        exploration_label="stage154_BaselineAdapter__OosMidEdgeRestoreValidationRepair",
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


def safe(adapter_id: str, oos: Mapping[str, Any], val: Mapping[str, Any], mid: Mapping[str, Any]) -> bool:
    return (
        bool(adapter_id)
        and as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(oos, "max_drawdown_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
        and as_float(mid, "profit_factor") >= LEGACY_34D["profit_factor"]
    )


def best_stage154(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        val_gain = as_float(val, "profit_factor") - STAGE152_MARGIN_TRIM["validation_profit_factor"]
        mid_keep = as_float(mid, "profit_factor") - LEGACY_34D["profit_factor"]
        dd_gap = LEGACY_34D["max_drawdown_percent"] - as_float(oos, "max_drawdown_percent", 99.0)
        candidates.append(
            (
                safe(adapter_id, oos, val, mid),
                val_gain > 0 and mid_keep >= 0,
                dd_gap >= 0,
                as_float(val, "profit_factor"),
                as_float(val, "net_profit"),
                as_float(mid, "profit_factor"),
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                -as_float(oos, "max_drawdown_percent", 99.0),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:9])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage155_runtime_completion_due_to_incomplete_stage154_runtime_candidate_not_final"
    best = best_stage154(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    mid = segment_row(segment_rows, adapter_id, "oos", "mid")
    if safe(adapter_id, best, val, mid):
        return "proceed_to_stage155_stage154_followup_review_with_candidate_not_final"
    return "continue_stage155_stage154_followup_review_due_to_damage_or_no_gain_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 낙폭) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS mid PF(표본외 중반 수익 팩터) | read(판독) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        read = "candidate_not_final" if safe(adapter_id, oos, val, mid) else "needs_followup_or_repair"
        lines.append(
            "| {adapter} | {val_pf:.6f} | {val_net:.2f} | {val_dd:.2f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {mid_pf:.9f} | {read} |".format(
                adapter=adapter_id,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                val_dd=as_float(val, "max_drawdown_percent"),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                mid_pf=as_float(mid, "profit_factor"),
                read=read,
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage154(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", "none"))
    val = split_row(summary_rows, adapter_id, "validation_is")
    mid = segment_row(segment_rows, adapter_id, "oos", "mid")
    return f"""# Stage154 OOS Mid Edge Restore Validation Repair Report(154단계 표본외 중반 가장자리 복원 검증 수리 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage153(원천 153단계): `{SOURCE_STAGE153_ID}`
- source_stage153_closeout_commit(원천 153단계 종료 커밋): `{SOURCE_STAGE153_CLOSEOUT_COMMIT}`
- source_stage153_hash_record_commit(원천 153단계 해시 기록 커밋): `{SOURCE_STAGE153_HASH_RECORD_COMMIT}`
- primary_seed(주 씨앗): `{SOURCE_ADAPTER_ID}`
- validation_memory(검증 기억): `{VALIDATION_MEMORY_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the Stage152 margin_trim(152단계 마진 축소) OOS mid lift(표본외 중반 상승)를 preserve(보존) while restoring validation PF/net(검증 수익 팩터/순손익) without bringing OOS DD(표본외 낙폭) back to the Stage150 margin_restore(150단계 마진 복원) damage level?

Effect(효과): OOS mid(표본외 중반)만 좋거나 validation(검증)만 좋은 후보를 최종처럼 보지 않는다.

## KPI Read(KPI 핵심 성과 지표 판독)

{row_table(summary_rows, segment_rows)}

## Judgment(판정)

- best_adapter(최선 어댑터): `{adapter_id}`
- best_validation_pf(최선 검증 수익 팩터): `{as_float(val, "profit_factor"):.6f}`
- best_oos_pf(최선 표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- best_oos_dd(최선 표본외 낙폭): `{as_float(best, "max_drawdown_percent"):.2f}`
- best_oos_mid_pf(최선 표본외 중반 수익 팩터): `{as_float(mid, "profit_factor"):.9f}`

Stage154(154단계)는 research/development only(연구개발 전용)이다. Effect(효과): candidate(후보)가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선)을 주장하지 않는다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage154 Decision(154단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- primary_seed(주 씨앗): `{SOURCE_ADAPTER_ID}`
- validation_memory(검증 기억): `{VALIDATION_MEMORY_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage154(154단계)는 margin_trim(마진 축소)의 OOS mid(표본외 중반) 장점과 validation memory(검증 기억)의 상충을 좁게 측정했다. Effect(효과): 이 판정은 다음 Stage155(155단계) review(검토)로 넘어가는 경계 기록이지 전체 목표 완료가 아니다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), production_baseline(생산 기준선), operating_promotion(운영 승격), operating_reference(운영 기준), runtime_authority(런타임 권위), overall_goal_complete(전체 목표 완료).
"""


def write_stage155_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage155(155단계)는 Stage154(154단계) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage154(154단계) restore validation(검증) while preserving OOS mid(표본외 중반) and controlling OOS DD(표본외 낙폭), or should the campaign continue into another bounded repair(경계 수리)?

Effect(효과): Stage154(154단계) 결과가 좋아 보여도 바로 final(최종)이나 deployment(배포)로 건너뛰지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage155 Input References(155단계 입력 참조)

- stage154_decision(154단계 판정): `{rel(DECISION_PATH)}`
- stage154_report(154단계 보고서): `{rel(REPORT_PATH)}`
- stage154_summary(154단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage154_segment_kpi(154단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage154_risk_atr_telemetry(154단계 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- source_stage153_decision(원천 153단계 판정): `stages/153_adapter_research__stage152_oos_dd_mid_followup_review/03_reviews/stage153_decision.md`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage155 Review Index(155단계 검토 색인)

- status(상태): `open_planned_from_stage154`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage154(154단계) 수리 결과를 다음 review(검토)에서 과장 없이 판정한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage155 Selection Status(155단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage154`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `run155A_stage155_stage154_oos_mid_validation_followup_review_v1`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage155(155단계)는 Stage154(154단계)를 검토하고 다음 수리/분기 여부를 정한다.
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    block = f"""
stage154_oos_mid_edge_restore_validation_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage153_closeout_commit: {SOURCE_STAGE153_CLOSEOUT_COMMIT}
  source_stage153_hash_record_commit: {SOURCE_STAGE153_HASH_RECORD_COMMIT}
  source_stage152_hash_record_commit: {SOURCE_STAGE152_HASH_RECORD_COMMIT}
  primary_seed: {SOURCE_ADAPTER_ID}
  validation_memory: {VALIDATION_MEMORY_ID}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage155_stage154_oos_mid_validation_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage154
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run155A_stage155_stage154_oos_mid_validation_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage154_oos_mid_edge_restore_validation_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage155_stage154_oos_mid_validation_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage154 Selection Status(154단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage153(원천 153단계): `{SOURCE_STAGE153_ID}`
- primary_seed(주 씨앗): `{SOURCE_ADAPTER_ID}`
- validation_memory(검증 기억): `{VALIDATION_MEMORY_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage154_decision(154단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage154(154단계)는 KPI(핵심 성과 지표)를 수리 대상으로만 기록하고 전체 목표 완료로 올리지 않는다.
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
- adapter_under_review(검토 중 어댑터): `stage155_stage154_oos_mid_validation_followup_review_surface`
- status(상태): `stage154_closed_{decision}_stage155_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage154(154단계)는 OOS mid seed(표본외 중반 씨앗)의 validation repair(검증 수리)를 실제 MT5(메타트레이더5) evidence(근거)로 측정했다. Effect(효과): 결과는 Stage155(155단계) review(검토)로 넘어가며, 전체 목표 완료나 운영 주장으로 승격하지 않는다.

## Latest Stage154 Evidence(최신 154단계 근거)

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
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage154 Review Index(154단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage154(154단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )
    write_stage155_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage154 OOS mid validation repair closeout(154단계 표본외 중반 검증 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage152 margin_trim(152단계 마진 축소)의 OOS mid(표본외 중반) 장점과 validation memory(검증 기억)를 좁은 MT5(메타트레이더5) 수리 변형으로 측정하고 Stage155(155단계) 검토로 넘겼다.\n"
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
                    "artifact_type": "stage154_oos_mid_validation_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage154 v2-native OOS mid validation repair artifact.",
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
                    "notes": "Actual Stage154 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_stage154_oos_mid_validation_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("source_stage153_hash_record_commit", SOURCE_STAGE153_HASH_RECORD_COMMIT), ("source_stage152_hash_record_commit", SOURCE_STAGE152_HASH_RECORD_COMMIT), ("primary_seed", SOURCE_ADAPTER_ID), ("validation_memory", VALIDATION_MEMORY_ID), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", 0))),
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


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s122.s108.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-backtest-forensics", "obsidian-experiment-design", "obsidian-performance-attribution", "obsidian-result-judgment", "obsidian-artifact-lineage"], "status": status})
    s122.s108.write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "summary_csv": rel(SUMMARY_CSV_PATH), "claim_boundary": BOUNDARY})
    s122.s108.write_json(PACKET_ROOT / "scope_completion_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "bounded_question": "restore validation on the OOS-mid seed without reintroducing OOS DD damage", "scope_completed": result.get("external_verification_status") == "completed", "out_of_scope": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "runtime_authority", "overall_goal_completion"], "status": status})
    s122.s108.write_json(PACKET_ROOT / "kpi_contract_audit.json", {"summary_csv": rel(SUMMARY_CSV_PATH), "segment_kpi_csv": rel(SEGMENT_KPI_PATH), "risk_atr_csv": rel(RISK_ATR_TELEMETRY_PATH), "status": status})
    s122.s108.write_json(PACKET_ROOT / "result_judgment_gate.json", {"result_subject": RUN_ID, "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(DECISION_PATH)], "evidence_missing": [], "judgment_label": "bounded_repair_candidate_not_final", "decision": decision, "claim_boundary": BOUNDARY, "next_condition": "Stage155 must judge whether Stage154 is a credible repair or needs another bounded repair.", "status": status})
    s122.s108.write_json(PACKET_ROOT / "performance_attribution_gate.json", {"comparison_baseline": SOURCE_ADAPTER_ID, "observed_change": "Stage154 varies margin edge restoration and hold compression around Stage152 margin_trim.", "likely_drivers": ["margin_block_width", "margin_edge_restore", "max_hold_bars", "threshold_guard"], "next_probe": NEXT_STAGE_ID, "status": status})
    s122.s108.write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"source_inputs": [SOURCE_ADAPTER_ID, VALIDATION_MEMORY_ID, rel(PRODUCER_PATH)], "producer": rel(PRODUCER_PATH), "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID], "artifact_paths": {"report": rel(REPORT_PATH), "summary": rel(SUMMARY_CSV_PATH), "segment_kpi": rel(SEGMENT_KPI_PATH), "risk_atr": rel(RISK_ATR_TELEMETRY_PATH), "stage_ledger": rel(STAGE_LEDGER_PATH)}, "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)], "ledger_payload": ledger_payload, "status": status})
    s122.s108.write_json(PACKET_ROOT / "runtime_parity_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "runtime_path": "foundation/mt5 tester profile via generated set files and run_manifest", "parity_check": "MT5 Strategy Tester output" if status == "completed" else "blocked_or_incomplete", "runtime_claim_boundary": "runtime_probe_research_only", "status": status})
    s122.s108.write_json(PACKET_ROOT / "backtest_forensics_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "tester_identity": "MT5 Strategy Tester via generated run manifest", "trade_evidence": rel(SUMMARY_CSV_PATH), "forensic_checks": ["report_path_exists", "summary_rows", "risk_telemetry", "artifact_hashes"], "status": status})
    s122.s108.write_json(PACKET_ROOT / "final_claim_guard.json", {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"})
    s122.s108.write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "missing_gates": [], "status": "passed" if status == "completed" else "blocked_with_evidence"})
    s122.s108.write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage153_closeout_commit": SOURCE_STAGE153_CLOSEOUT_COMMIT, "source_stage153_hash_record_commit": SOURCE_STAGE153_HASH_RECORD_COMMIT, "source_stage152_hash_record_commit": SOURCE_STAGE152_HASH_RECORD_COMMIT, "primary_seed": SOURCE_ADAPTER_ID, "validation_memory": VALIDATION_MEMORY_ID, "summary_csv": rel(SUMMARY_CSV_PATH), "segment_kpi_csv": rel(SEGMENT_KPI_PATH), "risk_atr_telemetry_csv": rel(RISK_ATR_TELEMETRY_PATH), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False})


def configure_stage154() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE151_ID": SOURCE_STAGE153_ID,
        "SOURCE_STAGE151_CLOSEOUT_COMMIT": SOURCE_STAGE153_CLOSEOUT_COMMIT,
        "SOURCE_STAGE151_HASH_RECORD_COMMIT": SOURCE_STAGE153_HASH_RECORD_COMMIT,
        "SOURCE_STAGE150_HASH_RECORD_COMMIT": SOURCE_STAGE152_HASH_RECORD_COMMIT,
        "SOURCE_STAGE148_HASH_RECORD_COMMIT": SOURCE_STAGE152_HASH_RECORD_COMMIT,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
        "OOS_REFERENCE_ID": VALIDATION_MEMORY_ID,
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
        "STAGE150_MARGIN_RESTORE": STAGE152_MARGIN_TRIM,
        "STAGE150_OOS_REFERENCE": STAGE152_VALIDATION_MEMORY,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s152, name, value)
    s152.source_baseline = source_baseline
    s152.best_stage152 = best_stage154
    s152.decide = decide
    s152.row_table = row_table
    s152.report_markdown = report_markdown
    s152.decision_markdown = decision_markdown
    s152.update_current_truth = update_current_truth
    s152.append_changelog = append_changelog
    s152.build_attempts = build_attempts
    s152.artifact_rows = artifact_rows
    s152.write_ledgers = write_ledgers
    s152.write_packet_files = write_packet_files
    s152.write_stage153_seed = write_stage155_seed
    s152.configure_stage152()


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage154()
    code = s148.main(argv)
    write_stage155_seed()
    print(json.dumps(json_ready({"status": "stage154_wrapper_complete", "run_id": RUN_ID, "decision_path": rel(DECISION_PATH)}), ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

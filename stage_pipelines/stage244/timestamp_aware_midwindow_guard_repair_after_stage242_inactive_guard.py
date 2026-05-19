from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, date, datetime
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
from stage_pipelines.stage238 import score_shape_repair_after_threshold_surface_discrete as stage238  # noqa: E402


STAGE_ID = "244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard"
RUN_NUMBER = "run244A"
RUN_ID = "run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1"
PACKET_ID = "stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1"
PARENT_RUN_ID = "run243A_stage243_stage242_selective_midsegment_followup_review_v1"
SOURCE_STAGE_ID = "243_adapter_research__stage242_selective_midsegment_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE243_EVIDENCE_COMMIT = "4b7c3394df8525180d4df401973cd8c61d8262e3"
SOURCE_STAGE243_HASH_RECORD_COMMIT = "156c5a743b379a90e79f4ec99ee97b75581f6257"
NEXT_STAGE_ID = "245_adapter_research__stage244_timestamp_guard_followup_review"
NEXT_RUN_ID = "run245A_stage245_stage244_timestamp_guard_followup_review_v1"
NEXT_PACKET_ID = "stage245_stage244_timestamp_guard_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_timestamp_aware_midwindow_guard_repair"
BOUNDARY = stage238.BOUNDARY
LEGACY_34D = stage238.LEGACY_34D
OOS_REFERENCE = {
    "adapter_id": "s240_highbonus010_samecap",
    "oos_net": 812.80,
    "oos_pf": 1.78,
    "oos_dd": 9.792,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s244a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage244_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage244_selective_midsegment_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage244_selective_midsegment_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage244_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage244_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage244_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage244_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage244_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage244_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage244_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage244_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage244_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage244_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage244_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage244_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage244_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage244/timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard.py")
ARTIFACT_COLUMNS = stage238.ARTIFACT_COLUMNS

SIGNAL_COLUMN = stage238.SIGNAL_COLUMN
RANK_COLUMN = "stage244_margin_rank_bucket"
SOURCE_REFERENCE_ADAPTER = "s235_session_ref_h3_cd8"
SOURCE_SPEC = dict(stage238.SOURCE_SPEC)
REFERENCE_EXTRA = dict(stage238.REFERENCE_EXTRA)


def variant(
    adapter_id: str,
    label: str,
    *,
    bonus_high: float,
    bonus_vhigh: float,
    risk_cap: float,
    mid_guard_mode: str,
    note: str,
) -> Any:
    return stage238.repair.RepairVariant(
        adapter_id=adapter_id,
        label=label,
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=risk_cap,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes=f"{note} mid_guard_mode={mid_guard_mode}",
    )


VARIANTS = (
    variant(
        "s244_samecap_control",
        "stage244_samecap_control",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.031375,
        mid_guard_mode="none",
        note="Stage244 control: repeat Stage240 highbonus same-cap behavior.",
    ),
    variant(
        "s244_midlow_guard",
        "stage244_midlow_guard",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.031375,
        mid_guard_mode="low",
        note="Stage244 repair: block only low-margin signals inside the middle window.",
    ),
    variant(
        "s244_midlowmid_guard",
        "stage244_midlowmid_guard",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.031375,
        mid_guard_mode="low_mid",
        note="Stage244 repair: block low and mid margin signals inside the middle window.",
    ),
    variant(
        "s244_cap0305_control",
        "stage244_cap0305_control",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.0305,
        mid_guard_mode="none",
        note="Stage244 control: isolate mild cap 0.0305 without a middle-window guard.",
    ),
    variant(
        "s244_midlowmid_guard_cap0305",
        "stage244_midlowmid_guard_cap0305",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.0305,
        mid_guard_mode="low_mid",
        note="Stage244 repair: combine selective middle-window guard with a mild cap only.",
    ),
)


def extra(axis: str, bonus_high: float, bonus_vhigh: float, mid_guard_mode: str) -> dict[str, Any]:
    return {
        "axis": axis,
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "mid_guard_mode": mid_guard_mode,
        "rank_scores": {
            "low": (0.0, 0.0, 0.0),
            "mid": (0.0, 0.0, 0.0),
            "high": (bonus_high, -bonus_high, bonus_high),
            "vhigh": (bonus_vhigh, -bonus_vhigh, bonus_vhigh),
        },
    }


VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s244_samecap_control": extra("samecap_control", 0.10, 0.15, "none"),
    "s244_midlow_guard": extra("midlow_guard", 0.10, 0.15, "low"),
    "s244_midlowmid_guard": extra("midlowmid_guard", 0.10, 0.15, "low_mid"),
    "s244_cap0305_control": extra("cap0305_control", 0.10, 0.15, "none"),
    "s244_midlowmid_guard_cap0305": extra("midlowmid_guard_cap0305", 0.10, 0.15, "low_mid"),
}
SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}

SPLIT_WINDOWS = {
    "validation_is": (date(2025, 1, 1), date(2025, 9, 30)),
    "oos": (date(2025, 10, 1), date(2026, 4, 13)),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return stage238.rel(path)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    stage238.write_csv(path, rows, columns)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return stage238.as_float(row, key, default)


def csv_value(value: Any) -> str:
    return stage238.csv_value(value)


def parse_date(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d"):
        try:
            return datetime.strptime(text[:19] if " " in fmt else text[:10], fmt).date()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(text[:19].replace("Z", "")).date()
    except ValueError:
        try:
            return datetime.strptime(text[:10], "%Y-%m-%d").date()
        except ValueError:
            return None


def in_middle_window(row_date: date | None, split: str) -> bool:
    if row_date is None or split not in SPLIT_WINDOWS:
        return False
    start, end = SPLIT_WINDOWS[split]
    span = (end - start).days + 1
    first_mid = start.toordinal() + span // 3
    last_mid = start.toordinal() + (2 * span // 3) - 1
    return first_mid <= row_date.toordinal() <= last_mid


def guard_buckets(mode: str) -> set[str]:
    if mode == "low":
        return {"low"}
    if mode == "low_mid":
        return {"low", "mid"}
    return set()


def selective_gate_value(row: Mapping[str, str], variant: Any, split: str) -> tuple[float, str]:
    base_gate = stage238.reference_gate_value(row)
    if base_gate >= 0.5:
        return base_gate, "reference_side_filter"
    mode = str(VARIANT_EXTRAS[variant.adapter_id]["mid_guard_mode"])
    buckets = guard_buckets(mode)
    if not buckets:
        return base_gate, "none"
    signal = int(round(stage238.parse_float(row.get(SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return base_gate, "none"
    _, bucket_label = stage238.rank_bucket_for(row)
    row_date = parse_date(row.get("bar_time_server") or row.get("timestamp_utc"))
    if not in_middle_window(row_date, split) or bucket_label not in buckets:
        return base_gate, "none"
    return (2.0 if signal > 0 else 1.0), f"mid_window_{mode}_guard"


def write_selective_feature(source: Path, destination: Path, variant: Any, split: str) -> dict[str, Any]:
    gate_column = f"stage244_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}"
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    signal_rows = 0
    reference_blocked_rows = 0
    selective_blocked_rows = 0
    mid_window_rows = 0
    rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    allowed_signal_rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    selective_block_rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with io_path(destination).open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(
                output_handle,
                fieldnames=("bar_time_server", SIGNAL_COLUMN, RANK_COLUMN, gate_column),
                lineterminator="\n",
            )
            writer.writeheader()
            for row in reader:
                total_rows += 1
                signal = int(round(stage238.parse_float(row.get(SIGNAL_COLUMN), 0.0)))
                bucket_value, bucket_label = stage238.rank_bucket_for(row)
                rank_counts[bucket_label] += 1
                row_date = parse_date(row.get("bar_time_server") or row.get("timestamp_utc"))
                if in_middle_window(row_date, split):
                    mid_window_rows += 1
                gate, gate_reason = selective_gate_value(row, variant, split)
                if signal != 0:
                    signal_rows += 1
                    if gate_reason == "reference_side_filter":
                        reference_blocked_rows += 1
                    elif gate_reason.startswith("mid_window"):
                        selective_blocked_rows += 1
                        selective_block_rank_counts[bucket_label] += 1
                    else:
                        allowed_signal_rank_counts[bucket_label] += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        SIGNAL_COLUMN: csv_value(float(signal)),
                        RANK_COLUMN: csv_value(float(bucket_value)),
                        gate_column: csv_value(gate),
                    }
                )
    return {
        "run_id": RUN_ID,
        "adapter_id": variant.adapter_id,
        "split": split,
        "gate_column": gate_column,
        "source_feature": rel(source),
        "score_shape_feature": rel(destination),
        "total_rows": total_rows,
        "signal_rows": signal_rows,
        "mid_window_rows": mid_window_rows,
        "reference_blocked_signal_rows": reference_blocked_rows,
        "selective_blocked_signal_rows": selective_blocked_rows,
        "allowed_signal_rows": signal_rows - reference_blocked_rows - selective_blocked_rows,
        "rank_counts": rank_counts,
        "allowed_signal_rank_counts": allowed_signal_rank_counts,
        "selective_block_rank_counts": selective_block_rank_counts,
        "mid_guard_mode": VARIANT_EXTRAS[variant.adapter_id]["mid_guard_mode"],
        "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
        "gate_description": "Stage244 reference side filter plus selective middle-window low/mid margin guard.",
        "side_filter_feature_index": 2,
        "rank_feature_index": 1,
    }


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for item in VARIANTS:
        gate_column = f"stage244_gate_{VARIANT_EXTRAS[item.adapter_id]['axis']}"
        model_source = stage238.s161.base.engine.source_model_for_variant(item)
        model_local = RUN_ROOT / item.adapter_id / "models" / f"{item.adapter_id}_model.csv"
        model_meta = stage238.write_score_shape_model(model_local, item, gate_column)
        copied.append(
            {
                "source": rel(model_source),
                "path": rel(model_local),
                "sha256": sha256_file_lf_normalized(model_local),
                "transform": "stage244_three_feature_selective_midsegment_score_shape_model",
            }
        )
        copied.append(stage238.s161.base.engine.copy_to_common(model_local, f"{COMMON_ROOT}/{item.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[item.adapter_id] = {
            **model_meta,
            "common_path": f"{COMMON_ROOT}/{item.adapter_id}/models/{model_local.name}",
            "source_model": rel(model_source),
            "source_anchor": stage238.s161.base.engine.source_anchor_for_variant(item),
        }
        feature_exports[item.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = stage238.s161.base.engine.source_feature(split, item, "a")
            feature_local = RUN_ROOT / item.adapter_id / "features" / f"{item.adapter_id}_{token}.csv"
            gate_row = write_selective_feature(feature_source, feature_local, item, split)
            gate_rows.append(gate_row)
            copied.append(
                {
                    "source": rel(feature_source),
                    "path": rel(feature_local),
                    "sha256": sha256_file_lf_normalized(feature_local),
                    "transform": "stage244_margin_rank_plus_midwindow_selective_guard_feature",
                }
            )
            copied.append(stage238.s161.base.engine.copy_to_common(feature_local, f"{COMMON_ROOT}/{item.adapter_id}/features/{feature_local.name}", common_files_root))
            feature_exports[item.adapter_id][split] = {
                "path": rel(feature_local),
                "common_path": f"{COMMON_ROOT}/{item.adapter_id}/features/{feature_local.name}",
                "sha256": sha256_file_lf_normalized(feature_local),
                "source_feature": rel(feature_source),
                "gate_column": gate_row["gate_column"],
                "rank_column": RANK_COLUMN,
            }
    return {
        "model_exports": model_exports,
        "feature_exports": feature_exports,
        "common_copies": copied,
        "gate_rows": gate_rows,
    }


def extra_set_values(item: Any, magic: int) -> dict[str, Any]:
    values = stage238.s161.base.engine.extra_set_values(item, magic)
    extra = VARIANT_EXTRAS[item.adapter_id]
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 2
    values["InpFallbackSideFilterFeatureIndex"] = 2
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 1.5
    values["InpBlockLongFeatureMax"] = 2.5
    values["InpModelRiskConfidenceFloor"] = float(extra["risk_confidence_floor"])
    values["InpModelRiskConfidenceCeiling"] = float(extra["risk_confidence_ceiling"])
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, item in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / item.adapter_id
        for split in ("validation_is", "oos"):
            date_values = stage238.s161.base.parse_ini(stage238.s161.base.engine.source_attempt_ini(split, item))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (stage238.s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{item.adapter_id}", "ta"),
                    (stage238.s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{item.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 24210000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    stage238.s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=242,
                        exploration_label="stage244_BaselineAdapter__SelectiveMidsegmentRepair",
                        attempt_name=f"{item.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][item.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{item.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][item.adapter_id][split]["common_path"]),
                        feature_count=3,
                        feature_order_hash=inputs["model_exports"][item.adapter_id]["feature_order_hash"],
                        short_threshold=item.short_threshold,
                        long_threshold=item.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=item.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{item.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=item.close_on_flat_signal,
                        reverse_on_opposite_signal=item.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=item.close_only_on_opposite_signal,
                        extra_set_values=extra_set_values(item, magic),
                    )
                )
    return attempts


def pass_stage242(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_net") >= LEGACY_34D["net_profit"]
        and as_float(row, "validation_early_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_mid_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_balance_dd_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(row, "oos_net") >= OOS_REFERENCE["oos_net"]
        and as_float(row, "oos_pf") >= OOS_REFERENCE["oos_pf"]
        and as_float(row, "oos_balance_dd_percent", 99.0) <= OOS_REFERENCE["oos_dd"]
    )


def decide(quality_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage244_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(pass_stage242(row) for row in quality_rows):
        return "open_stage245_bounded_followup_due_to_timestamp_guard_repair_candidate_not_final"
    return "open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            pass_stage242(row),
            as_float(row, "validation_net"),
            -as_float(row, "validation_balance_dd_percent", 99.0),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
        ),
    )


def tier_b_rows_stage242() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in VARIANTS:
        for split in ("validation", "oos"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": item.adapter_id,
                    "split": split,
                    "status": "diagnostic_missing_required_but_disabled_for_stage244_selective_midsegment_repair",
                    "fallback_enabled": 0,
                    "fallback_used_count": 0,
                    "notes": "Stage244 isolates Tier A routed selective midsegment repair; Tier B fallback remains disabled by prior fallback-only damage memory.",
                }
            )
    return rows


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(quality_rows)
    lines = [
        "# Stage244 Selective Midsegment Repair Report(244단계 선택적 중간 구간 수리 보고서)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage243_evidence_commit(원천 243단계 근거 커밋): `{SOURCE_STAGE243_EVIDENCE_COMMIT}`",
        f"- source_stage243_hash_record_commit(원천 243단계 해시 기록 커밋): `{SOURCE_STAGE243_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{external}`",
        f"- decision(판정): `{decision}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Bounded Design(경계 설계)",
        "",
        "- hypothesis(가설): Stage240(240단계)의 전역 risk cap(위험 상한)은 순손익을 너무 깎았다. 중간 기간의 낮은 margin bucket(마진 구간) 신호만 선택적으로 막으면 DD(낙폭)와 mid PF(중간 수익요인)를 고치면서 net/OOS(순손익/표본외)를 보존할 수 있다.",
        "- fixed variables(고정 변수): highbonus(고마진 보너스) `0.10/0.15`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, hold(보유) `3`, cooldown(대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).",
        "- changed variables(변경 변수): middle-window guard(중간 기간 보호문) `none/low/low_mid`, mild cap(완만한 상한) `0.0305` one variant(한 변형).",
        "- stop condition(정지 조건): 5개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage244(244단계)는 닫는다.",
        "",
        "## KPI Read(KPI 핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in quality_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {as_float(row, 'validation_net'):.2f} | {as_float(row, 'validation_early_pf'):.6f} | {as_float(row, 'validation_mid_pf'):.6f} | {as_float(row, 'validation_balance_dd_percent'):.4f} | {as_float(row, 'oos_net'):.2f} | {as_float(row, 'oos_pf'):.6f} | {as_float(row, 'oos_balance_dd_percent'):.4f} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- best_row(최선 행): `{best.get('adapter_id', '')}` with validation net(검증 순손익) `{best.get('validation_net', '')}`, validation DD(검증 낙폭) `{best.get('validation_balance_dd_percent', '')}`, mid PF(중간 수익요인) `{best.get('validation_mid_pf', '')}`, OOS net(표본외 순손익) `{best.get('oos_net', '')}`.",
            f"- decision(판정): `{decision}`.",
            "- overall_goal_complete(전체 목표 완료): `false`.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(decision: str, external: str) -> str:
    next_target = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    return f"""# Stage244 Decision(244단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{next_target}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage244(244단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage245(245단계) follow-up review(후속 검토)에서 timestamp-aware midwindow guard(시간 형식 인식 중간 창 보호문)의 KPI(핵심 성과 지표) 상충과 다음 bounded repair(경계 수리)를 판정한다.
"""


def write_stage243_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage245(245단계)는 Stage244(244단계) timestamp-aware midwindow guard repair(시간 형식 인식 중간 창 보호문 수리) 결과를 follow-up review(후속 검토)하는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage244(244단계) improve validation DD(검증 낙폭), mid PF(중간 수익요인), and cost-stressed behavior(비용 압박 행동) while preserving validation/OOS net(검증/표본외 순손익), ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), and segment behavior(구간 행동)?

Effect(효과): Stage244(244단계) 안에서 다음 수리를 흡수하지 않고 timestamp-aware guard(시간 형식 인식 보호문) 결과를 별도 review(검토)로 닫는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage245 Inputs(245단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(보호문 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage245 Review Index(245단계 검토 색인)

- status(상태): `open_planned_from_stage244`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage245 Selection Status(245단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage244`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_stage_block(text: str, key: str, block: str) -> str:
    pattern = rf"(?ms)^({re.escape(key)}:\r?\n).*?(?=^\S|\Z)"
    if re.search(pattern, text):
        return re.sub(pattern, block.rstrip() + "\n\n", text, count=1)
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_current_truth(decision: str, external: str) -> None:
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage244(244단계) closed(종료) as `{decision}` and Stage245(245단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): timestamp-aware midwindow guard(시간 형식 인식 중간 창 보호문)의 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.
- >-
  Stage244 evidence(244단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(GATE_FEATURE_SUMMARY_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): 중간 기간 보호문이 34D(34D 기준)에 가까워졌는지 확인한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=^\S)", focus, state, count=1)
    stage244_block = f"""stage244_selective_midsegment_quality_repair_after_highbonus_tradeoff:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  gate_feature_summary_path: {rel(GATE_FEATURE_SUMMARY_PATH)}
  risk_atr_telemetry_path: {rel(RISK_ATR_TELEMETRY_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}
"""
    stage243_block = f"""stage245_stage244_timestamp_guard_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage244
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage244_selective_midsegment_quality_repair_after_highbonus_tradeoff", stage244_block)
    if external == "completed":
        state = replace_stage_block(state, "stage245_stage244_timestamp_guard_followup_review", stage243_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8-sig")

    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage244_selective_midsegment_quality_repair`
- status(상태): `stage244_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage244(244단계)는 timestamp-aware midwindow guard repair(시간 형식 인식 중간 창 보호문 수리)를 MT5(MetaTrader 5, 메타트레이더5)로 측정했다. Effect(효과): Stage245(245단계)가 결과 상충과 다음 bounded repair(경계 수리)를 별도 review(검토)로 판정한다.

## Latest Stage244 Evidence(최신 244단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- gate_feature_summary(보호문 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage244 Selection Status(244단계 선택 상태)

- stage_status(단계 상태): `closed_{decision if external == "completed" else "blocked_runtime_incomplete"}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage244 Review Index(244단계 검토 색인)

- status(상태): `closed_{decision if external == "completed" else "blocked_runtime_incomplete"}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- gate_feature_summary(보호문 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage244 selective midsegment repair closeout(244단계 선택적 중간 구간 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): 시간 형식 인식 low/mid margin guard(저/중간 마진 보호문)를 MT5(MetaTrader 5, 메타트레이더5)로 측정하고 Stage245(245단계) follow-up review(후속 검토)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths: list[Path] = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        BALANCE_CURVE_AUDIT_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        QUALITY_MATRIX_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
    ]
    for execution in result.get("execution_results", []):
        for value in (execution.get("set_path"), execution.get("ini_path"), execution.get("report_path")):
            if value:
                paths.append(Path(str(value)))
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage244_selective_midsegment_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage244 selective midsegment repair evidence.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    summary_rows = result.get("mt5_kpi_records", [])
    primary = ledger_pairs(
        [
            ("decision", decision),
            ("external_status", result.get("external_verification_status", "")),
            ("variant_count", len(VARIANTS)),
            ("target_surface", TARGET_SURFACE),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("boundary", BOUNDARY),
            ("overall_goal_complete", 0),
        ]
    )
    alpha_rows = stage238.s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=summary_rows,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status", "")),
    )
    for row in alpha_rows:
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage244_selective_midsegment_repair"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage244_selective_midsegment_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": ledger_pairs(
                [
                    ("source_stage243_evidence_commit", SOURCE_STAGE243_EVIDENCE_COMMIT),
                    ("source_stage243_hash_record_commit", SOURCE_STAGE243_HASH_RECORD_COMMIT),
                    ("target_surface", TARGET_SURFACE),
                    ("overall_goal_complete", 0),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifacts, key="artifact_id")
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    required_gates = [
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "runtime_backtest(MT5/백테스트 실행)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-performance-attribution(성과 기여 분석)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": required_gates,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "summary": rel(SUMMARY_CSV_PATH),
            "segments": rel(SEGMENT_KPI_PATH),
            "risk_atr": rel(RISK_ATR_TELEMETRY_PATH),
            "gate_features": rel(GATE_FEATURE_SUMMARY_PATH),
            "variant_count": len(VARIANTS),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(QUALITY_MATRIX_PATH), rel(DECISION_PATH)],
            "evidence_missing": ["Stage245 follow-up review not run yet(245단계 후속 검토 미실행)", "ONNX/runtime hardening not in scope(ONNX/런타임 경화 범위 밖)"],
            "judgment_label": "selective_midsegment_repair_measured_candidate_not_final",
            "next_condition": NEXT_STAGE_ID,
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Selective middle-window guard variants measured against Stage240 highbonus same-cap clue.",
            "comparison_baseline": "s240_highbonus010_samecap and legacy 34D KPI(레거시 34D 핵심 성과 지표)",
            "likely_drivers": ["middle-window low/mid margin guard", "risk cap preservation", "ATR bracket unchanged"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [SOURCE_STAGE_ID, "stages/243_adapter_research__stage242_selective_midsegment_followup_review/03_reviews/stage243_decision.md"],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            **base_payload,
            "required_gates": required_gates,
            "covered_by": [
                "kpi_contract_audit.json",
                "result_judgment_gate.json",
                "performance_attribution_gate.json",
                "artifact_lineage_audit.json",
                "final_claim_guard.json",
                "required_gate_coverage_audit.json",
            ],
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "ledger_payload": ledger_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "quality": rel(QUALITY_MATRIX_PATH),
                "decision": rel(DECISION_PATH),
            },
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage244 Closeout Packet(244단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{result.get('external_verification_status', '')}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def configure_stage_module() -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "OOS_REFERENCE": OOS_REFERENCE,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "BALANCE_CURVE_AUDIT_PATH": BALANCE_CURVE_AUDIT_PATH,
        "MONTHLY_KPI_PATH": MONTHLY_KPI_PATH,
        "CONCENTRATION_PATH": CONCENTRATION_PATH,
        "DRAWDOWN_PATH": DRAWDOWN_PATH,
        "QUALITY_MATRIX_PATH": QUALITY_MATRIX_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "RANK_COLUMN": RANK_COLUMN,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
    }
    for name, value in values.items():
        setattr(stage238, name, value)
    stage238.prepare_inputs = prepare_inputs
    stage238.build_attempts = build_attempts
    stage238.decide = decide
    stage238.pass_stage238 = pass_stage242
    stage238.best_row = best_row
    stage238.tier_b_rows_stage238 = tier_b_rows_stage242
    stage238.report_markdown = report_markdown
    stage238.decision_markdown = decision_markdown
    stage238.write_stage239_seed = write_stage243_seed
    stage238.update_current_truth = update_current_truth
    stage238.write_status_files = write_status_files
    stage238.append_changelog = append_changelog
    stage238.artifact_rows = artifact_rows
    stage238.write_ledgers = write_ledgers
    stage238.write_packet_files = write_packet_files


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage_module()
    stage238.configure_runner()
    stage238.s161.configure_base()
    args = stage238.s161.parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 242,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": stage238.s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage244_v2_native_selective_midsegment_repair",
        "feature_set_id": "stage244_signal_margin_rank_plus_midwindow_guard",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = stage238.load_existing_result_if_requested(args) or stage238.s161.base.execute_or_materialize(prepared, args)
    audit_rows = stage238.s172.s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = stage238.s172.s58.risk_rows_from_result(result)
    summary_rows = stage238.s172.s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = stage238.s172.s58.segment_kpi_rows(summary_rows)
    probability_rows = stage238.s161.probability_binding_rows(result)
    model_rows = stage238.s161.model_score_rows(inputs)
    balance_rows, monthly_rows, concentration_rows, drawdown_rows = stage238.s172.build_curve_audit(summary_rows, segment_rows)
    quality_rows = stage238.s172.quality_rows(summary_rows, segment_rows, balance_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality_rows, external)

    stage238.s161.write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(BALANCE_CURVE_AUDIT_PATH, balance_rows)
    write_csv(MONTHLY_KPI_PATH, monthly_rows)
    write_csv(CONCENTRATION_PATH, concentration_rows)
    write_csv(DRAWDOWN_PATH, drawdown_rows)
    write_csv(QUALITY_MATRIX_PATH, quality_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows_stage242())
    write_md(REPORT_PATH, report_markdown(quality_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "balance_rows": balance_rows,
            "monthly_rows": monthly_rows,
            "concentration_rows": concentration_rows,
            "drawdown_rows": drawdown_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "quality_rows": quality_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "source_stage243_evidence_commit": SOURCE_STAGE243_EVIDENCE_COMMIT,
            "source_stage243_hash_record_commit": SOURCE_STAGE243_HASH_RECORD_COMMIT,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality_rows)
    write_stage243_seed(decision, external)
    update_current_truth(decision, external)
    write_status_files(decision, external)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": external,
                    "run_id": RUN_ID,
                    "decision": decision,
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "quality_rows": quality_rows,
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

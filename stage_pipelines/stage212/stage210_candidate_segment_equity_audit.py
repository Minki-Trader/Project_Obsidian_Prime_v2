from __future__ import annotations

import csv
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
from stage_pipelines.stage210 import oos_net_recovery_preserve_validation_gate as s210  # noqa: E402

s172 = s210.s172

STAGE_ID = "212_adapter_research__stage210_candidate_segment_equity_audit"
RUN_ID = "run212A_stage212_stage210_candidate_segment_equity_audit_v1"
PACKET_ID = "stage212_stage210_candidate_segment_equity_audit_v1"
PARENT_RUN_ID = "run211A_stage211_stage210_oos_net_recovery_followup_review_v1"
SOURCE_STAGE_ID = "211_adapter_research__stage210_oos_net_recovery_followup_review"
SOURCE_RUN_ID = "run211A_stage211_stage210_oos_net_recovery_followup_review_v1"
SOURCE_STAGE210_ID = "210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate"
SOURCE_STAGE210_RUN_ID = "run210A_stage210_oos_net_recovery_preserve_stage208_validation_gate_v1"
SOURCE_STAGE211_EVIDENCE_COMMIT = "6beda2e88076605ba2cb81e805ceb24f0c675b49"
SOURCE_STAGE211_HASH_RECORD_COMMIT = "749fc3a09534b99d1f1afa185f798571a586704c"
NEXT_STAGE_ID = "213_adapter_research__s210_r0315_oos_monthly_concentration_repair"
NEXT_RUN_ID = "run213A_stage213_s210_r0315_oos_monthly_concentration_repair_v1"
NEXT_PACKET_ID = "stage213_s210_r0315_oos_monthly_concentration_repair_v1"
SELECTED_ANCHOR_ID = "s210_ls_r0315"
DECISION = "open_stage213_bounded_oos_monthly_concentration_repair_for_s210_r0315_candidate_not_final"
EXTERNAL_STATUS = "review_only_source_stage210_mt5_reports_completed"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_segment_equity_audit"
BOUNDARY = s210.BOUNDARY
LEGACY_34D = s210.LEGACY_34D
STAGE171_PRIMARY = s210.STAGE171_PRIMARY

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE211_TRADEOFF_PATH = Path("stages/211_adapter_research__stage210_oos_net_recovery_followup_review/03_reviews/stage211_tradeoff_matrix.csv")
SOURCE_QUALITY_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_quality_matrix.csv")
SOURCE_KPI_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_oos_net_recovery_kpi_summary.csv")
SOURCE_SEGMENT_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_segment_kpi_summary.csv")
SOURCE_BALANCE_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_balance_curve_audit.csv")
SOURCE_MONTHLY_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_monthly_kpi_summary.csv")
SOURCE_CONCENTRATION_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_concentration_risk_summary.csv")
SOURCE_DRAWDOWN_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_drawdown_recovery_summary.csv")
SOURCE_TRADE_AUDIT_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_trade_audit.csv")
SOURCE_RISK_ATR_PATH = Path("stages/210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate/03_reviews/stage210_risk_atr_telemetry.csv")

REPORT_PATH = REVIEWS_ROOT / "stage212_segment_equity_audit.md"
SEGMENT_MATRIX_PATH = REVIEWS_ROOT / "stage212_segment_equity_matrix.csv"
MONTHLY_MATRIX_PATH = REVIEWS_ROOT / "stage212_monthly_stability_matrix.csv"
CONCENTRATION_MATRIX_PATH = REVIEWS_ROOT / "stage212_concentration_matrix.csv"
RISK_ATR_MATRIX_PATH = REVIEWS_ROOT / "stage212_risk_atr_telemetry_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage212_performance_attribution.csv"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage212_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage212_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage212/stage210_candidate_segment_equity_audit.py")
ARTIFACT_COLUMNS = s210.ARTIFACT_COLUMNS


def rel(path: Path | str) -> str:
    return s172.rel(path)


def fnum(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        text = str(value).strip().replace(",", "")
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def pct(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    inferred: list[str] = []
    for row in rows:
        for key in row:
            if key not in inferred:
                inferred.append(key)
    fieldnames = list(columns or inferred)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in fieldnames})


def selected_rows(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [row for row in rows if row.get("adapter_id") == SELECTED_ANCHOR_ID]


def selected_row(rows: Sequence[Mapping[str, Any]], split: str | None = None, **matches: str) -> Mapping[str, Any]:
    for row in selected_rows(rows):
        if split is not None and row.get("split") != split:
            continue
        if all(row.get(key) == value for key, value in matches.items()):
            return row
    return {}


def quality_anchor(quality_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return selected_row(quality_rows) or {}


def split_net_lookup(segment_rows: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    nets: dict[str, float] = {}
    for row in selected_rows(segment_rows):
        if row.get("view") == "actual_routed_total" and row.get("segment_type") == "full_split":
            nets[str(row.get("split", ""))] = fnum(row.get("net_profit"))
    return nets


def flags_or_ok(flags: list[str]) -> str:
    return ";".join(flags) if flags else "acceptable_measurement_only"


def build_segment_matrix(segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    split_nets = split_net_lookup(segment_rows)
    rows: list[dict[str, Any]] = []
    legacy_pf = float(LEGACY_34D["profit_factor"])
    for row in selected_rows(segment_rows):
        if row.get("view") != "actual_routed_total":
            continue
        split = str(row.get("split", ""))
        segment_type = str(row.get("segment_type", ""))
        segment = str(row.get("segment", ""))
        net = fnum(row.get("net_profit"))
        pf_value = fnum(row.get("profit_factor"))
        capture = fnum(row.get("mfe_capture_ratio"))
        share = net / split_nets.get(split, 1.0) if split_nets.get(split) else 0.0
        flags: list[str] = []
        if net <= 0:
            flags.append("negative_segment")
        if pf_value < legacy_pf:
            flags.append("pf_below_34d")
        if segment_type == "chronological_third" and abs(share) > 0.45:
            flags.append("segment_net_concentration_watch")
        if capture < 0.24:
            flags.append("mfe_capture_watch")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_STAGE210_RUN_ID,
                "adapter_id": SELECTED_ANCHOR_ID,
                "split": split,
                "segment_type": segment_type,
                "segment": segment,
                "trade_count": row.get("trade_count", ""),
                "trades_per_day": row.get("trades_per_day", ""),
                "net_profit": row.get("net_profit", ""),
                "net_share_of_split": pct(share),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "max_closed_trade_drawdown": row.get("max_closed_trade_drawdown", ""),
                "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                "mfe_mean": row.get("mfe_mean", ""),
                "mae_mean": row.get("mae_mean", ""),
                "avg_model_risk_pct": row.get("avg_model_risk_pct", ""),
                "avg_executed_lot": row.get("avg_executed_lot", ""),
                "avg_open_sl_points": row.get("avg_open_sl_points", ""),
                "avg_open_tp_points": row.get("avg_open_tp_points", ""),
                "audit_flag": flags_or_ok(flags),
            }
        )
    return rows


def build_monthly_matrix(monthly_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    split_nets = split_net_lookup(segment_rows)
    legacy_pf = float(LEGACY_34D["profit_factor"])
    rows: list[dict[str, Any]] = []
    for row in selected_rows(monthly_rows):
        split = str(row.get("split", ""))
        net = fnum(row.get("net_profit"))
        pf_value = fnum(row.get("profit_factor"))
        share = net / split_nets.get(split, 1.0) if split_nets.get(split) else 0.0
        flags: list[str] = []
        if net <= 0:
            flags.append("negative_month")
        if pf_value < legacy_pf:
            flags.append("pf_below_34d")
        if abs(share) > 0.30:
            flags.append("month_concentration_watch")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_STAGE210_RUN_ID,
                "adapter_id": SELECTED_ANCHOR_ID,
                "split": split,
                "month": row.get("month", ""),
                "trade_count": row.get("trade_count", ""),
                "net_profit": row.get("net_profit", ""),
                "net_share_of_split": pct(share),
                "profit_factor": row.get("profit_factor", ""),
                "winner_count": row.get("winner_count", ""),
                "loser_count": row.get("loser_count", ""),
                "source_quality_flag": row.get("quality_flag", ""),
                "audit_flag": flags_or_ok(flags),
            }
        )
    return rows


def monthly_stats(monthly_matrix: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for split in ("validation_is", "oos"):
        rows = [row for row in monthly_matrix if row.get("split") == split]
        negative = [row for row in rows if "negative_month" in str(row.get("audit_flag", ""))]
        pf_below = [row for row in rows if "pf_below_34d" in str(row.get("audit_flag", ""))]
        concentrated = [row for row in rows if "month_concentration_watch" in str(row.get("audit_flag", ""))]
        stats[split] = {
            "month_count": len(rows),
            "negative_month_count": len(negative),
            "negative_months": ",".join(str(row.get("month", "")) for row in negative),
            "pf_below_34d_count": len(pf_below),
            "concentrated_month_count": len(concentrated),
            "net_sum": round(sum(fnum(row.get("net_profit")) for row in rows), 2),
        }
    return stats


def build_concentration_matrix(
    concentration_rows: Sequence[Mapping[str, Any]],
    balance_rows: Sequence[Mapping[str, Any]],
    drawdown_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    legacy_dd = float(LEGACY_34D["max_drawdown_percent"])
    for conc in selected_rows(concentration_rows):
        split = str(conc.get("split", ""))
        balance = selected_row(balance_rows, split=split)
        dd = selected_row(drawdown_rows, split=split)
        max_dd = fnum(balance.get("max_drawdown_percent"))
        dd_margin = legacy_dd - max_dd
        flags: list[str] = []
        if fnum(conc.get("top1_winner_share_of_net")) > 0.15:
            flags.append("top1_spike_watch")
        if fnum(conc.get("top5_winner_share_of_net")) > 0.40:
            flags.append("top5_concentration_watch")
        if fnum(conc.get("last_quarter_net_share")) > 0.40:
            flags.append("late_quarter_concentration_watch")
        if split == "validation_is" and 0 <= dd_margin < 0.50:
            flags.append("thin_validation_dd_margin")
        if bool_text(dd.get("recovered")) is False:
            flags.append("drawdown_not_recovered")
        if bool_text(dd.get("final_balance_is_new_high")) is False:
            flags.append("final_balance_not_new_high")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_STAGE210_RUN_ID,
                "adapter_id": SELECTED_ANCHOR_ID,
                "split": split,
                "net_profit": balance.get("net_profit", ""),
                "profit_factor": balance.get("profit_factor", ""),
                "max_drawdown_percent": balance.get("max_drawdown_percent", ""),
                "legacy_34d_dd_percent": LEGACY_34D["max_drawdown_percent"],
                "dd_margin_vs_34d": pct(dd_margin),
                "late_net_share": balance.get("late_net_share", ""),
                "top1_winner": conc.get("top1_winner", ""),
                "top1_winner_share_of_net": conc.get("top1_winner_share_of_net", ""),
                "top3_winner_share_of_net": conc.get("top3_winner_share_of_net", ""),
                "top5_winner_share_of_net": conc.get("top5_winner_share_of_net", ""),
                "last_quarter_net": conc.get("last_quarter_net", ""),
                "last_quarter_net_share": conc.get("last_quarter_net_share", ""),
                "worst_loss": conc.get("worst_loss", ""),
                "recovered": dd.get("recovered", ""),
                "recovery_trades": dd.get("recovery_trades", ""),
                "max_underwater_trades": dd.get("max_underwater_trades", ""),
                "final_balance_is_new_high": dd.get("final_balance_is_new_high", ""),
                "audit_flag": flags_or_ok(flags),
            }
        )
    return rows


def build_risk_atr_matrix(
    risk_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    trade_by_split = {
        row.get("split"): row
        for row in trade_rows
        if row.get("variant_id") == SELECTED_ANCHOR_ID and str(row.get("record_view", "")).startswith("mt5_routed")
    }
    rows: list[dict[str, Any]] = []
    for row in selected_rows(risk_rows):
        if row.get("view") != "actual_routed_total":
            continue
        split = str(row.get("split", ""))
        trade = trade_by_split.get(split, {})
        flags: list[str] = []
        if not bool_text(row.get("atr_enabled")):
            flags.append("atr_missing")
        if not bool_text(row.get("model_risk_enabled")):
            flags.append("model_risk_missing")
        if fnum(row.get("max_clipped_risk_pct")) > 0.05:
            flags.append("risk_cap_above_5pct")
        if fnum(row.get("risk_floor_applied_count")) > 0:
            flags.append("min_lot_floor_applied_watch")
        if fnum(trade.get("cost_stressed_expectancy")) <= 0:
            flags.append("cost_stress_expectancy_nonpositive")
        if fnum(trade.get("same_move_reentry_ratio")) > 0.10:
            flags.append("same_move_density_watch")
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_STAGE210_RUN_ID,
                "adapter_id": SELECTED_ANCHOR_ID,
                "split": split,
                "atr_enabled": row.get("atr_enabled", ""),
                "model_risk_enabled": row.get("model_risk_enabled", ""),
                "atr_stop_multiplier": row.get("atr_stop_multiplier", ""),
                "atr_take_profit_multiplier": row.get("atr_take_profit_multiplier", ""),
                "risk_floor_applied_count": row.get("risk_floor_applied_count", ""),
                "avg_model_risk_pct": row.get("avg_model_risk_pct", ""),
                "max_model_risk_pct": row.get("max_model_risk_pct", ""),
                "avg_clipped_risk_pct": row.get("avg_clipped_risk_pct", ""),
                "max_clipped_risk_pct": row.get("max_clipped_risk_pct", ""),
                "avg_computed_lot": row.get("avg_computed_lot", ""),
                "avg_executed_lot": row.get("avg_executed_lot", ""),
                "max_actual_risk_pct_after_floor": row.get("max_actual_risk_pct_after_floor", ""),
                "avg_actual_risk_pct_after_floor": row.get("avg_actual_risk_pct_after_floor", ""),
                "avg_atr_points": row.get("avg_atr_points", ""),
                "avg_open_sl_points": row.get("avg_open_sl_points", ""),
                "avg_open_tp_points": row.get("avg_open_tp_points", ""),
                "risk_bucket": row.get("risk_bucket", ""),
                "cost_stressed_expectancy": trade.get("cost_stressed_expectancy", ""),
                "same_move_reentry_ratio": trade.get("same_move_reentry_ratio", ""),
                "mfe_capture_delta_vs_d390h10": trade.get("mfe_capture_delta_vs_d390h10", ""),
                "profit_factor_after_cooldown": trade.get("profit_factor_after_cooldown", ""),
                "net_after_cooldown": trade.get("net_after_cooldown", ""),
                "audit_flag": flags_or_ok(flags),
                "telemetry_sha256": row.get("telemetry_sha256", ""),
            }
        )
    return rows


def build_attribution_rows(
    quality: Mapping[str, Any],
    monthly_summary: Mapping[str, Mapping[str, Any]],
    concentration_matrix: Sequence[Mapping[str, Any]],
    risk_matrix: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    oos_conc = next((row for row in concentration_matrix if row.get("split") == "oos"), {})
    val_conc = next((row for row in concentration_matrix if row.get("split") == "validation_is"), {})
    risk_flags = ",".join(str(row.get("audit_flag", "")) for row in risk_matrix)
    return [
        {
            "run_id": RUN_ID,
            "observed_change": "s210_ls_r0315_keeps_stage210_headline_kpi(s210_ls_r0315가 Stage210 헤드라인 KPI를 유지)",
            "comparison_baseline": "legacy_34d_lesson_only_and_stage208_r0305(레거시 34D 교훈 전용 및 Stage208 r0305)",
            "likely_drivers": "risk_cap_0315_with_long_session_gate(위험 상한 0.0315와 롱 세션 관문)",
            "segment_checks": "validation_and_oos_chronological_thirds_months_concentration_drawdown_risk_atr(검증/표본외 시간 3분할, 월별, 집중, 낙폭, 위험/ATR)",
            "trade_shape": f"validation_net={quality.get('validation_net')};validation_dd={quality.get('validation_balance_dd_percent')};oos_net={quality.get('oos_net')}",
            "alternative_explanations": "risk_scaling_may_lift_net_without_curve_quality(위험 배율이 곡선 품질 없이 순손익만 올렸을 수 있음)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "Stage213 bounded repair must reduce OOS monthly/concentration risk while preserving validation gate(Stage213 경계 수리는 표본외 월별/집중 위험을 줄이면서 검증 관문을 보존해야 함)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "oos_has_two_negative_months_and_concentration_watch(표본외에 음수 월 2개와 집중 주의가 있음)",
            "comparison_baseline": "desired_gradual_curve(원하는 완만한 곡선)",
            "likely_drivers": "late_quarter_profit_cluster_and_monthly_regime_variance(후반 분기 수익 군집과 월별 국면 변동)",
            "segment_checks": f"oos_negative_months={monthly_summary.get('oos', {}).get('negative_months')};oos_top5={oos_conc.get('top5_winner_share_of_net')};oos_last_quarter={oos_conc.get('last_quarter_net_share')}",
            "trade_shape": "all_chronological_thirds_positive_but_oos_december_and_april_negative(시간 3분할은 모두 양수이나 표본외 12월과 4월이 음수)",
            "alternative_explanations": "small_oos_month_sample_and_session_concentration(작은 표본외 월 표본과 세션 집중)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "repair_monthly_loss_windows_without_open_ended_tuning(월별 손실 창을 무기한 튜닝 없이 수리)",
        },
        {
            "run_id": RUN_ID,
            "observed_change": "mandatory_risk_atr_present_and_floor_clean(필수 위험/ATR이 존재하고 최소 lot 바닥 영향이 없음)",
            "comparison_baseline": "mandatory_risk_atr_requirements(필수 위험/ATR 요구사항)",
            "likely_drivers": "model_risk_and_atr_bracket_active(모델 위험과 ATR 브래킷 활성)",
            "segment_checks": f"risk_flags={risk_flags}",
            "trade_shape": f"validation_final_new_high={val_conc.get('final_balance_is_new_high')};oos_final_new_high={oos_conc.get('final_balance_is_new_high')}",
            "alternative_explanations": "telemetry_is_summary_level_not_full_package_parity(기록은 요약 수준이고 전체 패키지 동등성은 아님)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "keep telemetry while repairing monthly/concentration behavior(월별/집중 행동을 수리하면서 기록을 유지)",
        },
    ]


def audit_summary(
    quality: Mapping[str, Any],
    monthly_summary: Mapping[str, Mapping[str, Any]],
    concentration_matrix: Sequence[Mapping[str, Any]],
    risk_matrix: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    validation_conc = next((row for row in concentration_matrix if row.get("split") == "validation_is"), {})
    oos_conc = next((row for row in concentration_matrix if row.get("split") == "oos"), {})
    risk_failures = [
        row for row in risk_matrix if str(row.get("audit_flag")) not in {"acceptable_measurement_only", ""}
    ]
    audit_flags: list[str] = []
    if monthly_summary.get("oos", {}).get("negative_month_count", 0):
        audit_flags.append("oos_negative_months")
    if "top5_concentration_watch" in str(oos_conc.get("audit_flag", "")):
        audit_flags.append("oos_top5_concentration_watch")
    if "late_quarter_concentration_watch" in str(oos_conc.get("audit_flag", "")):
        audit_flags.append("oos_late_quarter_concentration_watch")
    if "thin_validation_dd_margin" in str(validation_conc.get("audit_flag", "")):
        audit_flags.append("thin_validation_dd_margin")
    if "final_balance_not_new_high" in str(validation_conc.get("audit_flag", "")) or "final_balance_not_new_high" in str(oos_conc.get("audit_flag", "")):
        audit_flags.append("final_balance_not_new_high")
    if risk_failures:
        audit_flags.append("risk_atr_telemetry_watch")
    return {
        "run_id": RUN_ID,
        "decision": DECISION,
        "selected_anchor": SELECTED_ANCHOR_ID,
        "validation_net": quality.get("validation_net", ""),
        "validation_pf": quality.get("validation_pf", ""),
        "validation_dd": quality.get("validation_balance_dd_percent", ""),
        "validation_dd_margin_vs_34d": quality.get("validation_dd_margin_vs_34d", ""),
        "validation_mid_pf": quality.get("validation_mid_pf", ""),
        "oos_net": quality.get("oos_net", ""),
        "oos_pf": quality.get("oos_pf", ""),
        "oos_dd": quality.get("oos_balance_dd_percent", ""),
        "oos_delta_vs_stage171_primary": quality.get("stage171_oos_net_delta", ""),
        "monthly_summary": monthly_summary,
        "validation_concentration_flags": validation_conc.get("audit_flag", ""),
        "oos_concentration_flags": oos_conc.get("audit_flag", ""),
        "risk_atr_flags": [row.get("audit_flag", "") for row in risk_matrix],
        "audit_flags": audit_flags,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }


def report_md(summary: Mapping[str, Any], monthly_summary: Mapping[str, Mapping[str, Any]]) -> str:
    return f"""# Stage212 Segment Equity Audit(212단계 구간/잔고곡선 감사)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage211_evidence_commit(원천 211단계 근거 커밋): `{SOURCE_STAGE211_EVIDENCE_COMMIT}`
- source_stage211_hash_record_commit(원천 211단계 해시 기록 커밋): `{SOURCE_STAGE211_HASH_RECORD_COMMIT}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Read(KPI 핵심 성과 지표 판독)

- validation net(검증 순손익): `{summary.get('validation_net')}`
- validation PF(검증 수익요인): `{summary.get('validation_pf')}`
- validation DD(검증 낙폭): `{summary.get('validation_dd')}` with margin vs 34D(34D 대비 여유) `{summary.get('validation_dd_margin_vs_34d')}`
- validation mid PF(검증 중반 수익요인): `{summary.get('validation_mid_pf')}`
- OOS net(표본외 순손익): `{summary.get('oos_net')}`
- OOS PF(표본외 수익요인): `{summary.get('oos_pf')}`
- OOS DD(표본외 낙폭): `{summary.get('oos_dd')}`
- OOS delta vs Stage171 primary(Stage171 주 후보 대비 표본외 차이): `{summary.get('oos_delta_vs_stage171_primary')}`

## Audit Read(감사 판독)

- Segment thirds(3분할 구간): validation/OOS(검증/표본외) 모두 net positive(순손익 양수)다.
- Monthly behavior(월별 행동): validation(검증)은 negative month(음수 월)가 없고, OOS(표본외)는 `{monthly_summary.get('oos', {}).get('negative_month_count')}`개 negative month(음수 월)가 있다: `{monthly_summary.get('oos', {}).get('negative_months')}`.
- Concentration risk(집중 위험): validation flags(검증 표식) `{summary.get('validation_concentration_flags')}`, OOS flags(표본외 표식) `{summary.get('oos_concentration_flags')}`.
- Risk/ATR telemetry(위험/ATR 기록): mandatory telemetry(필수 기록)는 존재하고 min lot floor(최소 lot 바닥) 영향은 0이다.

## Judgment(판정)

`s210_ls_r0315` remains active research candidate(활성 연구 후보 유지) but is not final(최종 아님).

Effect(효과): Stage213(213단계)은 OOS monthly loss(표본외 월별 손실), concentration watch(집중 주의), thin validation DD margin(얇은 검증 낙폭 여유)을 좁게 수리한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_md(summary: Mapping[str, Any]) -> str:
    return f"""# Stage212 Decision(212단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage211_evidence_commit(원천 211단계 근거 커밋): `{SOURCE_STAGE211_EVIDENCE_COMMIT}`
- source_stage211_hash_record_commit(원천 211단계 해시 기록 커밋): `{SOURCE_STAGE211_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- segment_matrix(구간 행렬): `{rel(SEGMENT_MATRIX_PATH)}`
- monthly_matrix(월별 행렬): `{rel(MONTHLY_MATRIX_PATH)}`
- concentration_matrix(집중 행렬): `{rel(CONCENTRATION_MATRIX_PATH)}`
- risk_atr_matrix(위험/ATR 행렬): `{rel(RISK_ATR_MATRIX_PATH)}`
- attribution(성과 원인 분해): `{rel(ATTRIBUTION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage212(212단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): `s210_ls_r0315`는 active research candidate(활성 연구 후보)로 남기되, Stage213(213단계)에서 OOS monthly/concentration repair(표본외 월별/집중 수리)를 진행한다.

audit_flags(감사 표식): `{','.join(summary.get('audit_flags', []))}`
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = s172.utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        SEGMENT_MATRIX_PATH,
        MONTHLY_MATRIX_PATH,
        CONCENTRATION_MATRIX_PATH,
        RISK_ATR_MATRIX_PATH,
        ATTRIBUTION_PATH,
        SUMMARY_JSON_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
    ]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage212_segment_equity_audit_evidence",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage212 segment/equity audit evidence.",
        }
        for path in paths
    ]


def write_ledgers(summary: Mapping[str, Any]) -> None:
    primary = ledger_pairs(
        [
            ("selected_anchor", SELECTED_ANCHOR_ID),
            ("validation_net", summary.get("validation_net", "")),
            ("validation_dd", summary.get("validation_dd", "")),
            ("validation_mid_pf", summary.get("validation_mid_pf", "")),
            ("oos_net", summary.get("oos_net", "")),
            ("oos_dd", summary.get("oos_dd", "")),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("audit_flags", ",".join(summary.get("audit_flags", []))),
            ("decision", DECISION),
            ("next_stage", NEXT_STAGE_ID),
            ("boundary", BOUNDARY),
        ]
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage212_audit__actual_routed_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage212_audit",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "actual_routed_total",
            "tier_scope": "Tier A+B actual routed total(Tier A+B 실제 라우팅 전체)",
            "kpi_scope": "segment_equity_audit(구간/잔고곡선 감사)",
            "scoreboard_lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage212 review-only audit; not final and not deployment.",
        }
    ]
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_research(기준선 어댑터 연구)",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "notes": f"source_run={SOURCE_RUN_ID}; selected_anchor={SELECTED_ANCHOR_ID}; boundary={BOUNDARY}",
        }
    ]
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def write_packet_files(summary: Mapping[str, Any]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": DECISION,
        "selected_anchor": SELECTED_ANCHOR_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "report_path": rel(REPORT_PATH),
        "segment_matrix": rel(SEGMENT_MATRIX_PATH),
        "monthly_matrix": rel(MONTHLY_MATRIX_PATH),
        "concentration_matrix": rel(CONCENTRATION_MATRIX_PATH),
        "risk_atr_matrix": rel(RISK_ATR_MATRIX_PATH),
        "summary": summary,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    s172.write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    s172.write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    s172.write_json(PACKET_ROOT / "packet_receipt.json", payload)
    s172.write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage212 Closeout Packet(212단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `completed`
- decision(판정): `{DECISION}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    s172.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage213(213단계)은 Stage212(212단계) 감사에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a narrow v2-native repair(v2 고유 좁은 수리) reduce OOS monthly loss(표본외 월별 손실), OOS concentration watch(표본외 집중 주의), and thin validation DD margin(얇은 검증 낙폭 여유) for `{SELECTED_ANCHOR_ID}` while preserving validation net/PF/DD/midPF(검증 순손익/수익요인/낙폭/중반 수익요인), OOS net/PF/DD(표본외 순손익/수익요인/낙폭), and risk/ATR telemetry(위험/ATR 기록)?

Effect(효과): Stage212(212단계)의 감사 약점을 Stage213(213단계) 하나의 수리 질문으로 제한한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage213 Input References(213단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_segment_matrix(원천 구간 행렬): `{rel(SEGMENT_MATRIX_PATH)}`
- source_monthly_matrix(원천 월별 행렬): `{rel(MONTHLY_MATRIX_PATH)}`
- source_concentration_matrix(원천 집중 행렬): `{rel(CONCENTRATION_MATRIX_PATH)}`
- source_risk_atr_matrix(원천 위험/ATR 행렬): `{rel(RISK_ATR_MATRIX_PATH)}`
- source_stage210_summary(원천 210단계 요약): `{rel(SOURCE_KPI_PATH)}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage213 Review Index(213단계 검토 색인)

- status(상태): `open_planned_from_stage212`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    s172.write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage213 Selection Status(213단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage212`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage212(212단계) closed(종료) as `{DECISION}` and Stage213(213단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): `{SELECTED_ANCHOR_ID}`의 OOS monthly/concentration(표본외 월별/집중) 약점과 thin validation DD margin(얇은 검증 낙폭 여유)을 좁게 수리한다.
- >-
  Stage212 evidence(212단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SEGMENT_MATRIX_PATH)}`, `{rel(MONTHLY_MATRIX_PATH)}`, `{rel(CONCENTRATION_MATRIX_PATH)}`, `{rel(RISK_ATR_MATRIX_PATH)}`에 있다. Effect(효과): headline KPI(헤드라인 핵심 성과 지표)와 곡선/구간 약점을 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)^stage212_stage210_candidate_segment_equity_audit:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage212_stage210_candidate_segment_equity_audit:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  selected_anchor: {SELECTED_ANCHOR_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  segment_matrix_path: {rel(SEGMENT_MATRIX_PATH)}
  monthly_matrix_path: {rel(MONTHLY_MATRIX_PATH)}
  concentration_matrix_path: {rel(CONCENTRATION_MATRIX_PATH)}
  risk_atr_matrix_path: {rel(RISK_ATR_MATRIX_PATH)}
  audit_flags: {','.join(summary.get('audit_flags', []))}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    s172.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{SELECTED_ANCHOR_ID}`
- status(상태): `stage212_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage212(212단계)는 Stage210(210단계) 후보 `{SELECTED_ANCHOR_ID}`의 segment/equity(구간/잔고곡선) 품질을 review-only audit(검토 전용 감사)로 판정했다. Effect(효과): Stage213(213단계)은 월별/집중/낙폭 여유 수리만 좁게 진행한다.

## Latest Stage212 Evidence(최신 212단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- validation_net(검증 순손익): `{summary.get('validation_net')}`
- validation_dd(검증 낙폭): `{summary.get('validation_dd')}`
- oos_net(표본외 순손익): `{summary.get('oos_net')}`
- audit_flags(감사 표식): `{','.join(summary.get('audit_flags', []))}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- segment_matrix(구간 행렬): `{rel(SEGMENT_MATRIX_PATH)}`
- monthly_matrix(월별 행렬): `{rel(MONTHLY_MATRIX_PATH)}`
- concentration_matrix(집중 행렬): `{rel(CONCENTRATION_MATRIX_PATH)}`
- risk_atr_matrix(위험/ATR 행렬): `{rel(RISK_ATR_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(summary: Mapping[str, Any]) -> None:
    s172.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage212 Selection Status(212단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- audit_flags(감사 표식): `{','.join(summary.get('audit_flags', []))}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    s172.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage212 Review Index(212단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- selected_anchor(선택 후보): `{SELECTED_ANCHOR_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- segment_matrix(구간 행렬): `{rel(SEGMENT_MATRIX_PATH)}`
- monthly_matrix(월별 행렬): `{rel(MONTHLY_MATRIX_PATH)}`
- concentration_matrix(집중 행렬): `{rel(CONCENTRATION_MATRIX_PATH)}`
- risk_atr_matrix(위험/ATR 행렬): `{rel(RISK_ATR_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog(summary: Mapping[str, Any]) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {s172.utc_now()} Stage212 segment/equity audit closeout(212단계 구간/잔고곡선 감사 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): kept(유지) `{SELECTED_ANCHOR_ID}` as active research candidate(활성 연구 후보) and opened(개방) Stage213(213단계) bounded repair(경계 수리).\n"
        f"- audit_flags(감사 표식): `{','.join(summary.get('audit_flags', []))}`.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality_rows = read_csv(SOURCE_QUALITY_PATH)
    segment_rows = read_csv(SOURCE_SEGMENT_PATH)
    monthly_rows = read_csv(SOURCE_MONTHLY_PATH)
    concentration_rows = read_csv(SOURCE_CONCENTRATION_PATH)
    balance_rows = read_csv(SOURCE_BALANCE_PATH)
    drawdown_rows = read_csv(SOURCE_DRAWDOWN_PATH)
    risk_rows = read_csv(SOURCE_RISK_ATR_PATH)
    trade_rows = read_csv(SOURCE_TRADE_AUDIT_PATH)

    quality = quality_anchor(quality_rows)
    segment_matrix = build_segment_matrix(segment_rows)
    monthly_matrix = build_monthly_matrix(monthly_rows, segment_rows)
    monthly_summary = monthly_stats(monthly_matrix)
    concentration_matrix = build_concentration_matrix(concentration_rows, balance_rows, drawdown_rows)
    risk_matrix = build_risk_atr_matrix(risk_rows, trade_rows)
    summary = audit_summary(quality, monthly_summary, concentration_matrix, risk_matrix)
    attribution_rows = build_attribution_rows(quality, monthly_summary, concentration_matrix, risk_matrix)

    write_csv(SEGMENT_MATRIX_PATH, segment_matrix)
    write_csv(MONTHLY_MATRIX_PATH, monthly_matrix)
    write_csv(CONCENTRATION_MATRIX_PATH, concentration_matrix)
    write_csv(RISK_ATR_MATRIX_PATH, risk_matrix)
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    s172.write_json(SUMMARY_JSON_PATH, summary)
    s172.write_md(REPORT_PATH, report_md(summary, monthly_summary))
    s172.write_md(DECISION_PATH, decision_md(summary))
    write_ledgers(summary)
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    write_packet_files(summary)
    write_next_stage_seed()
    update_current_truth(summary)
    write_status_files(summary)
    append_changelog(summary)

    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "selected_anchor": SELECTED_ANCHOR_ID,
                    "audit_flags": summary.get("audit_flags", []),
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

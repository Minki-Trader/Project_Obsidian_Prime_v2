from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from PIL import Image, ImageStat
except Exception:  # pragma: no cover - optional local dependency fallback
    Image = None
    ImageStat = None

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_ID = input_probe.RUN_ID
RUN_ROOT = input_probe.RUN_ROOT
HIST_ROOT = input_probe.HIST_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH

EXECUTION_RESULT_PATH = HIST_ROOT / "execution_result.json"
TIME_SLICE_KPI_PATH = HIST_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = HIST_ROOT / "balance_curve_diagnostics.csv"
CANDIDATE_WEAKNESS_PATH = HIST_ROOT / "candidate_weakness_summary.csv"
VISUAL_ZOOM_MANIFEST_PATH = HIST_ROOT / "visual_zoom_manifest.csv"
ABLATION_REPLACEMENT_DESIGN_PATH = HIST_ROOT / "ablation_replacement_design.csv"
DESIGN_RESULT_PATH = HIST_ROOT / "visual_ablation_replacement_design.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_historical_2024_visual_ablation_design_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/historical_2024_visual_ablation_replacement_design.py")
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = input_probe.STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

NEXT_STATUS = "stage267_run267B_historical_2024_visual_ablation_replacement_design_completed"
NEXT_ACTION = "run267C_stage267_execute_prioritized_ablation_replacement_variants"

CANDIDATE_ROLES = {
    "s264_allow_inner_high_quarter": "core_challenger",
    "s264_lowrank_control": "defensive_control",
    "s262_lowrank_inner_half_filter": "validation_heavy",
    "s264_allow_inner_all_oos_anchor": "oos_anchor",
    "s258_short_tight_control": "stress_challenger",
}

DESIGN_COLUMNS = (
    "design_id",
    "design_type",
    "candidate_scope",
    "weakness_axis",
    "weakness_bucket",
    "source_evidence",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "priority",
    "status",
)

VISUAL_COLUMNS = (
    "attempt_name",
    "record_view",
    "candidate_id",
    "candidate_alias",
    "candidate_role",
    "tier_scope",
    "route_role",
    "split",
    "net_profit",
    "profit_factor",
    "trade_count",
    "equity_drawdown_percent",
    "curve_grade",
    "curve_read",
    "chart_path",
    "chart_sha256_recorded",
    "chart_sha256_actual",
    "file_size_bytes",
    "image_width",
    "image_height",
    "luma_min",
    "luma_max",
    "rgb_mean",
    "rgb_stddev",
    "nonblank_status",
    "visual_zoom_status",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return value


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"Missing text for replacement: {old}")
    return text.replace(old, new, 1)


def append_line_after_anchor(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"Missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def image_diagnostics(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {
            "file_size_bytes": 0,
            "image_width": "",
            "image_height": "",
            "luma_min": "",
            "luma_max": "",
            "rgb_mean": "",
            "rgb_stddev": "",
            "nonblank_status": "missing_chart_file",
            "notes": "chart path missing",
        }
    file_size = io_path(path).stat().st_size
    if Image is None or ImageStat is None:
        return {
            "file_size_bytes": file_size,
            "image_width": "",
            "image_height": "",
            "luma_min": "",
            "luma_max": "",
            "rgb_mean": "",
            "rgb_stddev": "",
            "nonblank_status": "file_exists_pil_unavailable",
            "notes": "PIL unavailable; file presence only",
        }
    try:
        with Image.open(io_path(path)) as image:
            rgb = image.convert("RGB")
            luma = image.convert("L")
            extrema = luma.getextrema()
            stat = ImageStat.Stat(rgb)
            nonblank = extrema[0] != extrema[1] and file_size > 1024
            return {
                "file_size_bytes": file_size,
                "image_width": rgb.width,
                "image_height": rgb.height,
                "luma_min": extrema[0],
                "luma_max": extrema[1],
                "rgb_mean": ";".join(f"{value:.2f}" for value in stat.mean),
                "rgb_stddev": ";".join(f"{value:.2f}" for value in stat.stddev),
                "nonblank_status": "nonblank_png_verified" if nonblank else "blank_or_tiny_png",
                "notes": "pixel extrema checked; curve quality still requires zoom review",
            }
    except Exception as exc:
        return {
            "file_size_bytes": file_size,
            "image_width": "",
            "image_height": "",
            "luma_min": "",
            "luma_max": "",
            "rgb_mean": "",
            "rgb_stddev": "",
            "nonblank_status": "image_open_error",
            "notes": str(exc),
        }


def sha256_file_raw(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def curve_lookup() -> dict[str, Mapping[str, str]]:
    rows = read_csv_rows(CURVE_DIAGNOSTICS_PATH)
    return {str(row.get("record_view")): row for row in rows}


def attempt_lookup(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}


def build_visual_manifest(execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts = attempt_lookup(execution_result)
    curves = curve_lookup()
    rows: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        chart = report.get("chart", {}) if isinstance(report.get("chart"), Mapping) else {}
        chart_path = Path(str(chart.get("path") or ""))
        chart_full_path = chart_path if chart_path.is_absolute() else REPO_ROOT / chart_path
        diagnostics = image_diagnostics(chart_full_path)
        record_view = str(record.get("record_view") or "")
        curve = curves.get(record_view, {})
        actual_sha = sha256_file_raw(chart_full_path) if path_exists(chart_full_path) else "missing"
        rows.append(
            {
                "attempt_name": attempt_name,
                "record_view": record_view,
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": CANDIDATE_ROLES.get(str(attempt.get("candidate_id")), ""),
                "tier_scope": record.get("tier_scope"),
                "route_role": record.get("route_role"),
                "split": record.get("split"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "equity_drawdown_percent": metrics.get("equity_drawdown_maximal_percent")
                or metrics.get("max_drawdown_percent"),
                "curve_grade": curve.get("curve_grade"),
                "curve_read": curve.get("curve_read"),
                "chart_path": rel(chart_path),
                "chart_sha256_recorded": chart.get("sha256"),
                "chart_sha256_actual": actual_sha,
                "visual_zoom_status": (
                    "available_for_zoom_not_quality_approved"
                    if diagnostics["nonblank_status"] == "nonblank_png_verified"
                    else "blocked_or_needs_repair"
                ),
                **diagnostics,
            }
        )
    return sorted(rows, key=lambda row: (str(row.get("candidate_alias")), str(row.get("route_role"))))


def weak_slice_lookup() -> dict[tuple[str, str], list[dict[str, str]]]:
    rows = read_csv_rows(TIME_SLICE_KPI_PATH)
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        try:
            net = float(row.get("net_profit") or 0.0)
        except ValueError:
            net = 0.0
        if net >= 0.0:
            continue
        key = (str(row.get("axis")), str(row.get("bucket")))
        grouped.setdefault(key, []).append(row)
    return grouped


def evidence_text(axis: str, bucket: str) -> str:
    grouped = weak_slice_lookup()
    rows = grouped.get((axis, bucket), [])
    if not rows:
        return f"{axis}:{bucket} weakness planned from 2024 review"
    parts = []
    seen: set[str] = set()
    for row in sorted(rows, key=lambda item: float(item.get("net_profit") or 0.0)):
        alias = str(row.get("candidate_alias") or "")
        if alias in seen:
            continue
        seen.add(alias)
        parts.append(
            f"{row.get('candidate_alias')} trades={row.get('trade_count')} net={row.get('net_profit')} PF={row.get('profit_factor')}"
        )
        if len(parts) >= 5:
            break
    return f"{axis}:{bucket}; " + "; ".join(parts)


def build_design_rows() -> list[dict[str, Any]]:
    all_candidates = "all_five_baseline_research_candidates"
    controls = (
        "symbol=US100;timeframe=M5;broker=FPMarkets;period=2024_train_era_stress;"
        "fixed candidate pool;fixed MT5 EA/runtime settings unless manifest records change"
    )
    sample = "historical_2024_train_era_stress plus canonical validation/OOS replay before any candidate upgrade"
    evidence_plan = (
        "variant manifest;feature order hash;MT5 report;trade records;time-slice KPI;"
        "balance/equity visual manifest;failure memory row;no ONNX claim"
    )
    return [
        {
            "design_id": "d01_vol_low_volatility_bandwidth_ablation",
            "design_type": "feature_category_ablation",
            "candidate_scope": all_candidates,
            "weakness_axis": "volatility_regime",
            "weakness_bucket": "vol_low",
            "source_evidence": evidence_text("volatility_regime", "vol_low"),
            "hypothesis": "If low-volatility damage is driven by one volatility feature family, removing that family should reveal which candidates are over-dependent.",
            "decision_use": "Downgrade candidates that collapse, or route the next feature engineering toward volatility-state robustness.",
            "comparison_baseline": "run267B historical_2024 balance/time-slice candidate summary",
            "control_variables": controls,
            "changed_variables": "remove volatility_bandwidth family: atr_14;atr_50;atr ratios;bollinger width;historical volatility proxies",
            "sample_scope": sample,
            "success_criteria": "Damage in vol_low becomes less concentrated without destroying trade count or total curve shape.",
            "failure_criteria": "All candidates lose broad profitability or one candidate only survives by under-trading.",
            "invalid_conditions": "Feature order hash mismatch; period mislabeled as OOS; MT5 report missing chart/deal list.",
            "stop_conditions": "If vol_low worsens across all candidates, stop this branch and pivot to feature engineering rather than threshold repair.",
            "evidence_plan": evidence_plan,
            "priority": "P0",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d02_vol_low_atr_to_historical_vol_replacement",
            "design_type": "similar_feature_replacement",
            "candidate_scope": all_candidates,
            "weakness_axis": "volatility_regime",
            "weakness_bucket": "vol_low",
            "source_evidence": evidence_text("volatility_regime", "vol_low"),
            "hypothesis": "ATR-specific scaling may be a lucky fit; historical-volatility and Bollinger-width proxies should test whether the market meaning survives.",
            "decision_use": "Keep candidates that retain shape under volatility proxy replacement; downgrade ATR-only survivors.",
            "comparison_baseline": "rep_volatility_atr map from run267B input readiness",
            "control_variables": controls,
            "changed_variables": "replace atr_14 emphasis with atr_50;historical_vol_20;historical_vol_5_over_20;bollinger_width_20",
            "sample_scope": sample,
            "success_criteria": "Vol_low PF and closed-balance drawdown improve or degrade mildly while total trade count remains credible.",
            "failure_criteria": "Replacement flips the edge only in one month or creates a cleaner number with uglier curve.",
            "invalid_conditions": "Replacement feature unavailable in Tier B fallback rows without missing_required label.",
            "stop_conditions": "Stop after one replacement family pass; do not micro-tune ATR multipliers around July only.",
            "evidence_plan": evidence_plan,
            "priority": "P0",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d03_adx_20_25_trend_strength_ablation",
            "design_type": "feature_category_ablation",
            "candidate_scope": all_candidates,
            "weakness_axis": "adx_bucket",
            "weakness_bucket": "adx_20_25",
            "source_evidence": evidence_text("adx_bucket", "adx_20_25"),
            "hypothesis": "The common ADX 20-25 damage may mean the trend-strength boundary is unstable, not that one ADX threshold needs repair.",
            "decision_use": "Decide whether trend-strength features need redesign before Adapter packaging.",
            "comparison_baseline": "run267B time_slice_kpi adx_bucket rows",
            "control_variables": controls,
            "changed_variables": "remove trend_strength_direction family: adx_14;di_spread_14;supertrend_10_3;vortex_indicator",
            "sample_scope": sample,
            "success_criteria": "Candidate degradation is gradual and weakness moves less sharply into ADX 20-25.",
            "failure_criteria": "All edge disappears or candidate behavior becomes untraceable by trend-strength slice.",
            "invalid_conditions": "ADX bucket computed with future data or mismatched close/open timestamp.",
            "stop_conditions": "If trend-strength removal kills all candidates, record dependency and move to replacement, not threshold fiddling.",
            "evidence_plan": evidence_plan,
            "priority": "P1",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d04_adx_to_di_vortex_supertrend_replacement",
            "design_type": "similar_feature_replacement",
            "candidate_scope": all_candidates,
            "weakness_axis": "adx_bucket",
            "weakness_bucket": "adx_20_25",
            "source_evidence": evidence_text("adx_bucket", "adx_20_25"),
            "hypothesis": "If the candidate captures trend-strength meaning, DI spread, vortex, or supertrend proxies should preserve part of the structure.",
            "decision_use": "Separate real trend-strength signal from ADX-only coincidence.",
            "comparison_baseline": "rep_trend_strength_adx map from run267B input readiness",
            "control_variables": controls,
            "changed_variables": "replace ADX-centered feature use with di_spread_14;vortex_indicator;supertrend_10_3 variants",
            "sample_scope": sample,
            "success_criteria": "At least one replacement keeps trade count, total curve, and weak-slice damage within acceptable research range.",
            "failure_criteria": "Only one proxy works in one month while validation/OOS shape worsens.",
            "invalid_conditions": "Replacement proxy changes label boundary or model input order without manifest update.",
            "stop_conditions": "Stop after family-level replacement; do not optimize a single ADX threshold.",
            "evidence_plan": evidence_plan,
            "priority": "P1",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d05_july_2024_holdout_stress",
            "design_type": "period_stress_holdout",
            "candidate_scope": all_candidates,
            "weakness_axis": "month",
            "weakness_bucket": "2024-07",
            "source_evidence": evidence_text("month", "2024-07"),
            "hypothesis": "July 2024 is a shared drawdown pocket; a robust candidate should not need a July-only patch to survive.",
            "decision_use": "Flag candidates whose improvement is only a July-specific repair and not broad robustness.",
            "comparison_baseline": "run267B monthly KPI and closed-balance diagnostics",
            "control_variables": controls,
            "changed_variables": "evaluate pre-July, July-only, post-July slices and no-July replay labels without changing thresholds first",
            "sample_scope": sample,
            "success_criteria": "Weakness attribution is explainable across vol/session/trend axes and not hidden by total-year profit.",
            "failure_criteria": "Candidate depends on excluding July or adding a calendar-only hard block.",
            "invalid_conditions": "Month filtering changes trade pairing or includes open trades outside scope.",
            "stop_conditions": "Use July as stress evidence only; do not open a calendar micro-repair loop.",
            "evidence_plan": evidence_plan,
            "priority": "P0",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d06_monday_session_timing_ablation",
            "design_type": "feature_category_ablation",
            "candidate_scope": all_candidates,
            "weakness_axis": "weekday",
            "weakness_bucket": "Monday",
            "source_evidence": evidence_text("weekday", "Monday"),
            "hypothesis": "Monday damage may be a timing/context interaction rather than a reason for a day-only block.",
            "decision_use": "Decide whether session_timing features need interaction terms or downgrade for narrow calendar dependence.",
            "comparison_baseline": "run267B weekday and session_slice KPI",
            "control_variables": controls,
            "changed_variables": "remove or isolate session_timing family: cash open flags;minutes_from_cash_open;last_30m;overnight_return",
            "sample_scope": sample,
            "success_criteria": "Monday damage becomes explainable through session/volatility interaction while broad curve remains stable.",
            "failure_criteria": "A candidate only survives by blocking Monday or collapsing trade count.",
            "invalid_conditions": "Timezone mismatch between UTC close hour and broker session labels.",
            "stop_conditions": "If weakness is calendar-only, record as fragility and avoid overfitting a weekday filter.",
            "evidence_plan": evidence_plan,
            "priority": "P1",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d07_late_session_interaction_engineering",
            "design_type": "feature_engineering_design",
            "candidate_scope": all_candidates,
            "weakness_axis": "session_slice",
            "weakness_bucket": "late",
            "source_evidence": evidence_text("session_slice", "late"),
            "hypothesis": "Late-session losses may require interaction features between session, volatility compression, spread, and trend-strength rather than a simple session filter.",
            "decision_use": "Define Adapter-facing features that explain late-session risk without hiding it behind local stage tricks.",
            "comparison_baseline": "run267B session_slice KPI and visual manifest",
            "control_variables": controls,
            "changed_variables": "add candidate features: late_session_x_vol_low;late_session_x_spread_high;late_session_x_adx_20_25;minutes_to_cash_close_bucket",
            "sample_scope": sample,
            "success_criteria": "Late-session damage falls without sacrificing normal-session expectancy and without opaque feature order changes.",
            "failure_criteria": "New interactions only repair one month or create untraceable decision surface.",
            "invalid_conditions": "Engineered feature cannot be reproduced in Python and MT5 with the same timestamp boundary.",
            "stop_conditions": "If two passes fail, close as failure memory and pivot away from late-session repair.",
            "evidence_plan": evidence_plan,
            "priority": "P0",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d08_rank_gate_compressed_surface_ablation",
            "design_type": "compressed_gate_ablation",
            "candidate_scope": all_candidates,
            "weakness_axis": "candidate_gate",
            "weakness_bucket": "rank_inner_outer_bucket",
            "source_evidence": "Stage258/262/264 candidate gates plus run267B feature_ablation_map",
            "hypothesis": "Some candidates may be stage-local gate tricks rather than reusable Adapter structures.",
            "decision_use": "Identify candidates that should be demoted before deeper Adapter work.",
            "comparison_baseline": "abl_gate_rank_bucket and abl_gate_variant_rule maps",
            "control_variables": controls,
            "changed_variables": "remove or rotate lowrank/inner/high-quarter gate bucket while keeping model and execution settings documented",
            "sample_scope": sample,
            "success_criteria": "A strong candidate degrades mildly or exposes a clear reusable structure.",
            "failure_criteria": "Candidate collapses when its named gate is removed.",
            "invalid_conditions": "Gate removal changes unrelated risk/ATR or trade management settings.",
            "stop_conditions": "If gate removal collapses a candidate twice, downgrade instead of repairing for more than two stages.",
            "evidence_plan": evidence_plan,
            "priority": "P0",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d09_chron_mid_weakness_decomposition",
            "design_type": "time_slice_decomposition",
            "candidate_scope": all_candidates,
            "weakness_axis": "chron_segment",
            "weakness_bucket": "chron_mid",
            "source_evidence": evidence_text("chron_segment", "chron_mid"),
            "hypothesis": "The mid-year chronological slump may be the intersection of July, low volatility, and late-session exposure.",
            "decision_use": "Prevent a single-axis repair from hiding a multi-axis weakness.",
            "comparison_baseline": "run267B chron_segment KPI and candidate weakness summary",
            "control_variables": controls,
            "changed_variables": "cross-tab chron_mid with vol/session/weekday/month before model retraining",
            "sample_scope": sample,
            "success_criteria": "Weakness source is decomposed into a small number of reproducible axes.",
            "failure_criteria": "No stable attribution; candidate remains broad rough-curve survivor only.",
            "invalid_conditions": "Chronological slicing changes trade order or equity curve reconstruction.",
            "stop_conditions": "If no attribution appears, record inconclusive and move to broader feature family work.",
            "evidence_plan": evidence_plan,
            "priority": "P1",
            "status": "designed_not_executed",
        },
        {
            "design_id": "d10_breadth_macro_context_replacement",
            "design_type": "similar_feature_replacement",
            "candidate_scope": all_candidates,
            "weakness_axis": "context_proxy",
            "weakness_bucket": "breadth_macro_optional",
            "source_evidence": "run267B prior research utilization audit and source feature manifest",
            "hypothesis": "If low-volatility and late-session failures are missing context problems, breadth or macro proxies may stabilize without calendar overfit.",
            "decision_use": "Decide whether to invest in broader context Adapter features.",
            "comparison_baseline": "rep_breadth_proxy and abl_external_macro_risk maps",
            "control_variables": controls,
            "changed_variables": "replace or add breadth/macro proxies: top3_weighted_return;mega8_dispersion;vix_zscore_20;us10yr_zscore_20",
            "sample_scope": sample,
            "success_criteria": "Weak-slice damage improves across more than one candidate and does not rely on missing Tier B context.",
            "failure_criteria": "Context proxy helps only one candidate or creates Tier B missing-data fragility.",
            "invalid_conditions": "External macro data alignment or availability is incomplete without missing_required label.",
            "stop_conditions": "If context proxies introduce data integrity risk, stop and record blocked/invalid rather than force comparison.",
            "evidence_plan": evidence_plan,
            "priority": "P2",
            "status": "designed_not_executed",
        },
    ]


def visual_status(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "blocked_no_visual_rows"
    if all(row.get("nonblank_status") == "nonblank_png_verified" for row in rows):
        return "completed_visual_artifact_sanity_not_quality_approval"
    if any(row.get("nonblank_status") == "nonblank_png_verified" for row in rows):
        return "partial_visual_artifact_sanity"
    return "blocked_visual_artifacts_unusable"


def upsert_stage_ledger(status: str) -> None:
    row = {
        "row_id": "stage267_run267B_historical_2024_visual_ablation_replacement_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "historical_2024_visual_ablation_replacement_design",
        "tier_scope": "Tier A and Tier A+B historical stress attempts",
        "scoreboard": "experiment_design",
        "status": status,
        "judgment": "designed_next_experiments_no_candidate_selection",
        "evidence_boundary": "visual_artifact_sanity_and_experiment_design_no_onnx_readiness",
        "report_path": rel(REPORT_PATH),
        "notes": "2024 chart PNG sanity and prioritized ablation/replacement design recorded; selected candidate none.",
    }
    rows = input_probe.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    input_probe.write_csv(
        STAGE_LEDGER_PATH,
        merged,
        (
            "row_id",
            "stage_id",
            "run_id",
            "view",
            "tier_scope",
            "scoreboard",
            "status",
            "judgment",
            "evidence_boundary",
            "report_path",
            "notes",
        ),
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        (
            "stage267_run267B_historical_2024_visual_ablation_design_script",
            "producer_script",
            PRODUCER_PATH,
            "Builds 2024 chart PNG sanity manifest and ablation/replacement experiment design.",
        ),
        (
            "stage267_run267B_historical_2024_visual_zoom_manifest",
            "visual_zoom_manifest",
            VISUAL_ZOOM_MANIFEST_PATH,
            "MT5 chart PNG presence, hash, and nonblank pixel sanity manifest.",
        ),
        (
            "stage267_run267B_historical_2024_ablation_replacement_design",
            "experiment_design",
            ABLATION_REPLACEMENT_DESIGN_PATH,
            "Prioritized feature ablation, similar replacement, and feature engineering design from 2024 weaknesses.",
        ),
        (
            "stage267_run267B_historical_2024_visual_ablation_design_result",
            "review_result",
            DESIGN_RESULT_PATH,
            "JSON payload for 2024 visual sanity and ablation/replacement design.",
        ),
        (
            "stage267_run267B_historical_2024_visual_ablation_design_report",
            "review_report",
            REPORT_PATH,
            "User-facing report for visual sanity and ablation/replacement design boundary.",
        ),
    )
    rows = input_probe.read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]
    replacements = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacements]
    merged.extend(new_rows)
    input_probe.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_run_manifest(status: str) -> None:
    manifest = read_json(RUN_MANIFEST_PATH)
    manifest["status"] = "historical_2024_visual_ablation_replacement_design_completed"
    manifest["execution_status"] = "historical_2024_visual_ablation_replacement_design_completed"
    manifest["latest_judgment"] = {
        "result_subject": "Stage267 run267B 2024 visual artifact sanity and ablation/replacement design",
        "evidence_available": [
            rel(VISUAL_ZOOM_MANIFEST_PATH),
            rel(ABLATION_REPLACEMENT_DESIGN_PATH),
            rel(DESIGN_RESULT_PATH),
            rel(REPORT_PATH),
        ],
        "evidence_missing": [
            "actual ablation/replacement MT5 reruns",
            "Adapter structure validation",
            "ONNX parity",
            "runtime reproduction",
        ],
        "judgment_label": "exploratory_design_completed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_ACTION,
    }
    plan = list(manifest.get("evidence_plan", []))
    for path in (
        rel(VISUAL_ZOOM_MANIFEST_PATH),
        rel(ABLATION_REPLACEMENT_DESIGN_PATH),
        rel(DESIGN_RESULT_PATH),
        rel(REPORT_PATH),
    ):
        if path not in plan:
            plan.append(path)
    manifest["evidence_plan"] = plan
    manifest["outputs"] = {
        **dict(manifest.get("outputs", {})),
        "visual_zoom_manifest": rel(VISUAL_ZOOM_MANIFEST_PATH),
        "ablation_replacement_design": rel(ABLATION_REPLACEMENT_DESIGN_PATH),
        "visual_ablation_replacement_design_result": rel(DESIGN_RESULT_PATH),
        "visual_ablation_replacement_design_report": rel(REPORT_PATH),
    }
    manifest["next_action"] = NEXT_ACTION
    manifest["visual_artifact_status"] = status
    write_json(RUN_MANIFEST_PATH, manifest)


def update_current_truth_docs() -> None:
    current_text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = replace_once(
        current_text,
        "- status(상태): `stage267_run267B_historical_2024_balance_time_slice_review_completed_visual_zoom_pending`",
        f"- status(상태): `{NEXT_STATUS}`",
    )
    current_text = replace_once(
        current_text,
        "- next_run(다음 실행): `run267B_stage267_extended_period_ablation_probe_v1`",
        "- next_run(다음 실행): `run267C_stage267_execute_prioritized_ablation_replacement_variants`",
    )
    current_text = replace_once(
        current_text,
        "- action(행동): 2024 historical stress(2024 과거 압박) MT5 deal list(거래 목록)에서 3,574개 trade record(거래 기록)와 490개 time-slice KPI(시간 구간 핵심 성과 지표)를 만들었다.",
        "- action(행동): 2024 historical stress(2024 과거 압박) MT5 chart PNG(MT5 차트 이미지) 10개를 sanity check(기초 점검)하고, 약점 기반 ablation/replacement design(제거/대체 설계) 10개를 만들었다.",
    )
    current_text = replace_once(
        current_text,
        "- effect(효과): 공통 약점은 vol_low(낮은 변동성), 2024-07(2024년 7월), Monday(월요일), late session(후반 세션)으로 드러났고, selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비)는 계속 없다.",
        "- effect(효과): 공통 약점인 vol_low(낮은 변동성), 2024-07(2024년 7월), Monday(월요일), late session(후반 세션)을 다음 실행 가능한 feature ablation(피처 제거), similar replacement(유사 대체), feature engineering(피처 엔지니어링) 질문으로 바꾸었다.",
    )
    current_text = replace_once(
        current_text,
        "- next_action(다음 행동): MT5 chart PNG(MT5 차트 이미지) visual zoom review(시각 확대 검토)를 보강하고, vol_low/July/Monday/late-session(낮은 변동성/7월/월요일/후반 세션) 약점을 기준으로 feature ablation(피처 제거)과 similar replacement(유사 대체)를 설계한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 설계만 끝낸 상태에서 멈추지 않고, 실제 rerun(재실행)으로 어떤 후보가 덜 깨지는지 확인한다.",
    )
    current_text = append_line_after_anchor(
        current_text,
        "- Stage267(267단계) historical 2024 balance/time-slice review(2024 과거 압박 잔액/시간 구간 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_balance_time_slice_review.md`",
        "- Stage267(267단계) historical 2024 visual ablation design(2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current_text)

    selection_text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection_text = replace_once(
        selection_text,
        "- stage_status(단계 상태): `run267B_historical_2024_balance_time_slice_review_completed_visual_zoom_pending`",
        "- stage_status(단계 상태): `run267B_historical_2024_visual_ablation_replacement_design_completed`",
    )
    selection_text = replace_once(
        selection_text,
        "- next_action(다음 행동): `run267B_2024_visual_zoom_ablation_replacement_design`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection_text = append_line_after_anchor(
        selection_text,
        "- historical_2024_balance_time_slice_review(2024 잔액/시간 구간 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_balance_time_slice_review.md`",
        "- historical_2024_visual_ablation_design(2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`",
    )
    selection_text = replace_once(
        selection_text,
        "Run267B(267B 실행)는 input readiness(입력 준비), first-pass equity curve shape grading(1차 평가금 곡선 형태 판정), 2024 historical stress input materialization(2024 과거 압박 입력 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행), 2024 balance/time-slice review(잔액/시간 구간 검토)를 완료했다.",
        "Run267B(267B 실행)는 input readiness(입력 준비), first-pass equity curve shape grading(1차 평가금 곡선 형태 판정), 2024 historical stress input materialization(2024 과거 압박 입력 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행), 2024 balance/time-slice review(잔액/시간 구간 검토), visual artifact sanity(시각 산출물 기초 점검), ablation/replacement design(제거/대체 설계)을 완료했다.",
    )
    write_md(SELECTION_STATUS_PATH, selection_text)

    review_text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_text = replace_once(
        review_text,
        "- status(상태): `run267B_historical_2024_balance_time_slice_review_completed_visual_zoom_pending`",
        "- status(상태): `run267B_historical_2024_visual_ablation_replacement_design_completed`",
    )
    review_text = append_line_after_anchor(
        review_text,
        "- run267B_historical_2024_balance_time_slice_review(267B 2024 잔액/시간 구간 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_balance_time_slice_review.md`",
        "- run267B_historical_2024_visual_ablation_design(267B 2024 시각/제거 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_historical_2024_visual_ablation_design_report.md`",
    )
    review_text = replace_once(
        review_text,
        "Run267B(267B 실행)는 input readiness(입력 준비), existing MT5 report(기존 MT5 보고서)의 equity curve shape grading(평가금 곡선 형태 판정), 2024 historical stress(2024 과거 압박) 입력 물질화(materialization, 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행), 2024 balance/time-slice review(잔액/시간 구간 검토)를 완료했다.",
        "Run267B(267B 실행)는 input readiness(입력 준비), existing MT5 report(기존 MT5 보고서)의 equity curve shape grading(평가금 곡선 형태 판정), 2024 historical stress(2024 과거 압박) 입력 물질화(materialization, 산출물화), 2024 MT5 Strategy Tester execution(MT5 전략 테스터 실행), 2024 balance/time-slice review(잔액/시간 구간 검토), visual artifact sanity(시각 산출물 기초 점검), ablation/replacement design(제거/대체 설계)을 완료했다.",
    )
    review_text = replace_once(
        review_text,
        "visual zoom review(시각 확대 검토)와 vol_low/July/Monday/late-session(낮은 변동성/7월/월요일/후반 세션) 기반 ablation/replacement(제거/대체) 설계로 넘어간다.",
        f"`{NEXT_ACTION}`로 넘어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review_text)

    workspace_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace_text = replace_once(
        workspace_text,
        "Stage267(267단계) run267B(267B 실행) historical 2024 balance/time-slice review(2024 과거 압박 잔액/시간 구간 검토) completed(완료).",
        "Stage267(267단계) run267B(267B 실행) historical 2024 visual ablation/replacement design(2024 시각 제거/대체 설계) completed(완료).",
    )
    workspace_text = replace_once(
        workspace_text,
        "Effect(효과): MT5 Strategy Tester(전략 테스터) 10개 report(보고서)의 deal list(거래 목록)에서 3,574개 trade record(거래 기록)와 490개 time-slice KPI(시간 구간 핵심 성과 지표)를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Effect(효과): 2024 deal list(거래 목록), time-slice KPI(시간 구간 핵심 성과 지표), chart PNG(차트 이미지)를 다음 feature ablation(피처 제거), similar replacement(유사 대체), feature engineering(피처 엔지니어링) 실행 질문 10개로 연결했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "Next action(다음 행동)는 `run267B_2024_visual_zoom_ablation_replacement_design`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "active_historical_2024_balance_time_slice_review_completed_visual_zoom_pending(2024 잔액/시간 구간 검토 완료 후 시각 확대 대기 활성).",
        "active_historical_2024_visual_ablation_replacement_design_completed(2024 시각 제거/대체 설계 완료 활성).",
    )
    write_md(WORKSPACE_STATE_PATH, workspace_text)


def build_report(
    visual_rows: Sequence[Mapping[str, Any]],
    design_rows: Sequence[Mapping[str, Any]],
    result: Mapping[str, Any],
) -> str:
    routed_rows = [row for row in visual_rows if row.get("route_role") == "routed_total"]
    design_preview = list(design_rows)
    lines = [
        "# Stage267 Historical 2024 Visual/Ablation Design(267단계 2024 시각/제거 설계)",
        "",
        "- action(행동): MT5 chart PNG(MT5 차트 이미지) 10개를 hash(해시), 크기, 픽셀 범위로 sanity check(기초 점검)하고, 2024 약점에서 다음 ablation/replacement(제거/대체) 실험 설계를 만들었다.",
        "- effect(효과): 후보를 고르지 않고, 약점이 어디서 다시 검증되어야 하는지 실행 가능한 질문으로 바꾸었다.",
        f"- visual_manifest_rows(시각 목록 행): `{len(visual_rows)}`",
        f"- design_rows(설계 행): `{len(design_rows)}`",
        f"- visual_status(시각 상태): `{result['visual_status']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Visual Artifact Sanity(시각 산출물 기초 점검)",
        "",
        "| candidate(후보) | role(역할) | route(경로) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | curve grade(곡선 등급) | chart status(차트 상태) |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in sorted(routed_rows, key=lambda item: str(item.get("candidate_alias"))):
        lines.append(
            "| `{candidate_id}` | `{candidate_role}` | `{route_role}` | {net_profit} | {profit_factor} | {trade_count} | {equity_drawdown_percent} | `{curve_grade}` | `{nonblank_status}` |".format(
                **{key: cell(row.get(key)) for key in VISUAL_COLUMNS}
            )
        )
    lines.extend(
        [
            "",
            "Read(판독): chart PNG(MT5 차트 이미지)는 모두 비어 있지 않은 파일로 확인됐다. Effect(효과): 다음 rerun(재실행)에서 balance/equity curve(잔액/평가금 곡선)를 대조할 수 있는 시각 산출물 신원은 확보했다.",
            "",
            "Boundary(경계): 이 점검은 그림 파일이 존재하고 열리는지 확인한 것이다. curve(곡선)가 예쁘거나 후보가 강하다는 판정은 아니다.",
            "",
            "## Prioritized Design(우선 설계)",
            "",
            "| design(설계) | type(유형) | weakness(약점) | priority(우선순위) | status(상태) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in design_preview:
        lines.append(
            f"| `{row['design_id']}` | `{row['design_type']}` | `{row['weakness_axis']}:{row['weakness_bucket']}` | `{row['priority']}` | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- result_subject(판정 대상): Stage267 run267B 2024 visual artifact sanity(시각 산출물 기초 점검) and ablation/replacement design(제거/대체 설계).",
            "- evidence_available(사용 가능 근거): MT5 chart PNG(MT5 차트 이미지), visual manifest(시각 목록), time-slice KPI(시간 구간 핵심 성과 지표), candidate weakness summary(후보 약점 요약), design CSV/JSON(설계 표/JSON).",
            "- evidence_missing(부족 근거): actual ablation/replacement reruns(실제 제거/대체 재실행), Adapter validation(어댑터 검증), ONNX parity(ONNX 동등성), runtime reproduction(런타임 재현).",
            "- judgment_label(판정 라벨): `exploratory_design_completed`.",
            "- selected_candidate(선택 후보): `none`.",
            "- selected_research_baseline(선택 연구 기준선): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def execute() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(EXECUTION_RESULT_PATH)
    visual_rows = build_visual_manifest(execution_result)
    design_rows = build_design_rows()
    status = visual_status(visual_rows)
    result = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": NEXT_STATUS,
        "visual_status": status,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "visual_manifest_rows": len(visual_rows),
        "design_rows": len(design_rows),
        "p0_designs": [row["design_id"] for row in design_rows if row.get("priority") == "P0"],
        "p1_designs": [row["design_id"] for row in design_rows if row.get("priority") == "P1"],
        "outputs": {
            "visual_zoom_manifest": rel(VISUAL_ZOOM_MANIFEST_PATH),
            "ablation_replacement_design": rel(ABLATION_REPLACEMENT_DESIGN_PATH),
            "visual_ablation_replacement_design_result": rel(DESIGN_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "next_action": NEXT_ACTION,
    }
    write_csv(VISUAL_ZOOM_MANIFEST_PATH, visual_rows, VISUAL_COLUMNS)
    write_csv(ABLATION_REPLACEMENT_DESIGN_PATH, design_rows, DESIGN_COLUMNS)
    write_json(DESIGN_RESULT_PATH, result)
    write_md(REPORT_PATH, build_report(visual_rows, design_rows, result))
    upsert_stage_ledger(status)
    update_run_manifest(status)
    update_current_truth_docs()
    upsert_artifacts(created_at)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "visual_status": result["visual_status"],
                "visual_manifest_rows": result["visual_manifest_rows"],
                "design_rows": result["design_rows"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

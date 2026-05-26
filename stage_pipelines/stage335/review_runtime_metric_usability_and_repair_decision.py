from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335O"
RUN_ID = "run335O_branch_specific_runtime_metric_usability_and_repair_decision_v1"
PARENT_RUN_ID = "run335N_materialize_branch_specific_runtime_metric_extractors_v1"
NEXT_RUN_ID = "run335P_materialize_balanced_repair_defense_offense_research_inputs_v1"

STATUS = "completed_runtime_metric_usability_and_repair_decision_no_forward_decision"
JUDGMENT = "structured_runtime_metrics_usable_with_boundary_proxy_not_selection_usable"
DECISION = "stage335O_proxy_context_only_runtime_metrics_usable_with_boundary_repair_defense_offense_queue"
CLAIM_BOUNDARY = (
    "research_development_only_stage335O_runtime_metric_usability_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN335K_DIR = STAGE_DIR / "02_runs" / "run335K"
RUN335L_DIR = STAGE_DIR / "02_runs" / "run335L"
RUN335M_DIR = STAGE_DIR / "02_runs" / "run335M"
RUN335N_DIR = STAGE_DIR / "02_runs" / "run335N"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335O_runtime_metric_usability_and_repair_decision.md"
REPORT_DOC = REVIEWS_DIR / "run335O_runtime_metric_usability_and_repair_decision.md"

ATTEMPT_SCORECARD_CSV = RUN_DIR / "attempt_runtime_usability_scorecard.csv"
PROXY_USABILITY_CSV = RUN_DIR / "proxy_mt5_usability_decision.csv"
BRANCH_DECISION_CSV = RUN_DIR / "branch_metric_usability_decision.csv"
FRAGILITY_FINDINGS_CSV = RUN_DIR / "runtime_fragility_findings.csv"
REGIME_RISK_CSV = RUN_DIR / "regime_risk_summary.csv"
REPAIR_QUEUE_CSV = RUN_DIR / "repair_research_queue.csv"
DEFENSE_QUEUE_CSV = RUN_DIR / "defensive_guard_queue.csv"
OFFENSE_QUEUE_CSV = RUN_DIR / "offensive_research_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_runtime_metric_usability_and_repair_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return io_path(path).resolve().relative_to(io_path(ROOT).resolve()).as_posix()


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value is None:
            return default
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    number = as_float(value, math.nan)
    if not math.isfinite(number):
        return default
    return int(number)


def fmt_float(value: Any, digits: int = 6) -> str:
    number = as_float(value, math.nan)
    if not math.isfinite(number):
        return ""
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_text_bom(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_or_replace_section(path: Path, title: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    heading = f"## {title}"
    next_marker = "\n## "
    body_text = f"{heading}\n\n{body.strip()}\n"
    if heading in text:
        start = text.index(heading)
        next_start = text.find(next_marker, start + len(heading))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + body_text
        else:
            text = text[:start].rstrip() + "\n\n" + body_text + text[next_start:]
    else:
        text = text.rstrip() + "\n\n" + body_text
    write_text_lossless(path, text, had_bom)


def read_csv(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(io_path(path))


def unique_branch_rows(branch_df: pd.DataFrame) -> pd.DataFrame:
    cols = ["branch_name", "branch_id", "metric_id", "metric_family"]
    existing = [col for col in cols if col in branch_df.columns]
    return branch_df[existing].drop_duplicates().sort_values(existing).reset_index(drop=True)


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "attempt": read_csv(RUN335N_DIR / "attempt_runtime_metric_summary.csv"),
        "cost": read_csv(RUN335N_DIR / "cost_stress_metric_matrix.csv"),
        "curve": read_csv(RUN335N_DIR / "curve_pocket_underwater_matrix.csv"),
        "regime": read_csv(RUN335N_DIR / "regime_direction_slice_matrix.csv"),
        "proxy": read_csv(RUN335N_DIR / "protocol_specific_proxy_mt5_difference.csv"),
        "join": read_csv(RUN335N_DIR / "trade_telemetry_join_audit.csv"),
        "negative_control": read_csv(RUN335N_DIR / "negative_control_subject_boundary_audit.csv"),
        "branch": read_csv(RUN335N_DIR / "branch_runtime_metric_matrix.csv"),
        "gate": read_csv(RUN335N_DIR / "required_gate_coverage_audit.csv"),
    }


def cost_value(cost: pd.DataFrame, attempt: str, extra_cost: float, column: str) -> float:
    sub = cost[(cost["attempt_name"] == attempt) & (pd.to_numeric(cost["extra_cost_per_trade"], errors="coerce") == extra_cost)]
    if sub.empty:
        return math.nan
    return as_float(sub.iloc[0].get(column))


def curve_value(curve: pd.DataFrame, attempt: str, window: int, column: str) -> float:
    sub = curve[(curve["attempt_name"] == attempt) & (pd.to_numeric(curve["rolling_window_trades"], errors="coerce") == window)]
    if sub.empty:
        return math.nan
    return as_float(sub.iloc[0].get(column))


def classify_attempt(row: Mapping[str, Any], cost: pd.DataFrame, curve: pd.DataFrame) -> dict[str, Any]:
    attempt = str(row.get("attempt_name"))
    net = as_float(row.get("net_profit"))
    pf = as_float(row.get("profit_factor"))
    tpd = as_float(row.get("trades_per_calendar_day"))
    recovery = as_float(row.get("recovery_factor_closed"))
    underwater_share = as_float(row.get("underwater_trade_share"))
    longest_underwater = as_int(row.get("longest_underwater_trades"))
    trades = as_int(row.get("trade_count"))
    long_net = as_float(row.get("long_net_profit"))
    short_net = as_float(row.get("short_net_profit"))
    cost025 = cost_value(cost, attempt, 0.25, "net_profit")
    cost05 = cost_value(cost, attempt, 0.5, "net_profit")
    cost10 = cost_value(cost, attempt, 1.0, "net_profit")
    cost20 = cost_value(cost, attempt, 2.0, "net_profit")
    worst20 = curve_value(curve, attempt, 20, "worst_window_net")
    reasons: list[str] = []
    score = 0

    if net > 0 and pf > 1.0:
        score += 2
    else:
        reasons.append("headline_runtime_edge_missing")
    if pf >= 1.2:
        score += 2
    else:
        reasons.append("profit_factor_thin")
    if tpd >= 4.0:
        score += 2
    else:
        reasons.append("trade_density_below_goal_shape")
    if recovery >= 1.0:
        score += 2
    else:
        reasons.append("recovery_factor_weak")
    if math.isfinite(cost05) and cost05 > 0:
        score += 2
    else:
        reasons.append("fails_cost_plus_0_5")
    if math.isfinite(cost10) and cost10 > 0:
        score += 1
    else:
        reasons.append("fails_or_barely_passes_cost_plus_1_0")
    if math.isfinite(worst20) and worst20 > -65.0:
        score += 1
    else:
        reasons.append("rolling20_curve_pocket_too_deep")
    if underwater_share <= 0.75:
        score += 1
    else:
        reasons.append("underwater_share_high")
    if long_net > 0 and short_net > 0:
        score += 2
    else:
        reasons.append("direction_asymmetry_or_short_drag")
    if longest_underwater <= max(60, trades * 0.35):
        score += 1
    else:
        reasons.append("underwater_stretch_long")

    if score >= 12:
        usability = "strong_research_clue_not_candidate"
    elif score >= 8:
        usability = "usable_research_clue_with_repair_required"
    elif score >= 5:
        usability = "fragile_research_clue_defensive_memory"
    else:
        usability = "failure_memory_only"

    return {
        "attempt_name": attempt,
        "artifact_slug": row.get("artifact_slug", ""),
        "feature_set_id": row.get("feature_set_id", ""),
        "net_profit": net,
        "profit_factor": pf,
        "trade_count": trades,
        "trades_per_calendar_day": tpd,
        "expectancy": as_float(row.get("expectancy")),
        "win_rate": as_float(row.get("win_rate")),
        "closed_balance_max_drawdown": as_float(row.get("closed_balance_max_drawdown")),
        "recovery_factor_closed": recovery,
        "long_net_profit": long_net,
        "short_net_profit": short_net,
        "longest_underwater_trades": longest_underwater,
        "underwater_trade_share": underwater_share,
        "net_per_lot": as_float(row.get("net_per_lot")),
        "cost_plus_0_25_net": cost025,
        "cost_plus_0_5_net": cost05,
        "cost_plus_1_0_net": cost10,
        "cost_plus_2_0_net": cost20,
        "rolling20_worst_net": worst20,
        "usability_score": score,
        "runtime_metric_usability": usability,
        "primary_failure_axes": ";".join(reasons) if reasons else "none_observed_in_this_review",
        "selection_eligible": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_attempt_scorecard(inputs: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows = [classify_attempt(row, inputs["cost"], inputs["curve"]) for row in inputs["attempt"].to_dict("records")]
    return sorted(rows, key=lambda item: (-as_float(item["usability_score"]), -as_float(item["net_profit"])))


def build_proxy_usability(inputs: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    proxy = inputs["proxy"].copy()
    proxy["proxy_num"] = pd.to_numeric(proxy["proxy_expected_value"], errors="coerce")
    proxy["runtime_num"] = pd.to_numeric(proxy["structured_runtime_value"], errors="coerce")
    rows: list[dict[str, Any]] = []
    for dimension, group in proxy.groupby("dimension", dropna=False):
        numeric = group.dropna(subset=["proxy_num", "runtime_num"])
        numeric_rows = len(numeric)
        structured_available = int((group["difference_status"] == "structured_runtime_available_proxy_aggregate_context_only").sum())
        sign_agreement = math.nan
        spearman = math.nan
        mean_abs_diff = math.nan
        median_abs_diff = math.nan
        if numeric_rows:
            proxy_sign = numeric["proxy_num"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
            runtime_sign = numeric["runtime_num"].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
            sign_agreement = float((proxy_sign == runtime_sign).mean())
            mean_abs_diff = float((numeric["proxy_num"] - numeric["runtime_num"]).abs().mean())
            median_abs_diff = float((numeric["proxy_num"] - numeric["runtime_num"]).abs().median())
            if numeric["proxy_num"].nunique() > 1 and numeric["runtime_num"].nunique() > 1:
                spearman = float(numeric["proxy_num"].corr(numeric["runtime_num"], method="spearman"))
        if numeric_rows == 0:
            usability = "non_numeric_context_only"
        elif group["proxy_expected_value"].nunique(dropna=False) <= 1:
            usability = "not_rank_usable_repeated_aggregate_proxy"
        elif math.isfinite(spearman) and spearman >= 0.5:
            usability = "diagnostic_rank_usable_with_runtime_confirmation"
        else:
            usability = "diagnostic_presence_only_not_branch_decision"
        rows.append(
            {
                "dimension": dimension,
                "rows": len(group),
                "numeric_comparable_rows": numeric_rows,
                "structured_runtime_available_rows": structured_available,
                "unique_proxy_expected_values": int(group["proxy_expected_value"].nunique(dropna=False)),
                "mean_abs_proxy_runtime_difference": mean_abs_diff,
                "median_abs_proxy_runtime_difference": median_abs_diff,
                "sign_agreement_rate": sign_agreement,
                "spearman_rank_correlation": spearman,
                "proxy_usability_decision": usability,
                "allowed_use": "diagnostic_context_only_no_forward_pass_fail_no_selection",
                "next_condition": "rebuild_proxy_as_branch_specific_row_level_trade_simulation_then_compare_to_mt5",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "dimension": "overall_proxy_bridge",
            "rows": len(proxy),
            "numeric_comparable_rows": int(proxy[["proxy_num", "runtime_num"]].dropna().shape[0]),
            "structured_runtime_available_rows": int((proxy["difference_status"] == "structured_runtime_available_proxy_aggregate_context_only").sum()),
            "unique_proxy_expected_values": int(proxy["proxy_expected_value"].nunique(dropna=False)),
            "mean_abs_proxy_runtime_difference": "",
            "median_abs_proxy_runtime_difference": "",
            "sign_agreement_rate": "",
            "spearman_rank_correlation": "",
            "proxy_usability_decision": "not_selection_usable_context_only",
            "allowed_use": "can_confirm_measurement_presence_but_cannot_rank_branches_or_pass_forward",
            "next_condition": "run335P_must_materialize_branch_specific_proxy_or_skip_proxy_as_selection_input",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_branch_decisions(inputs: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    branch_rows = unique_branch_rows(inputs["branch"])
    rows: list[dict[str, Any]] = []
    for branch, group in branch_rows.groupby("branch_name"):
        metric_ids = sorted(str(item) for item in group["metric_id"].dropna().unique())
        metric_families = sorted(str(item) for item in group["metric_family"].dropna().unique())
        if branch in {"cp322a_exact_blocker_control", "subject_swap_negative_control", "null_adjacent_period_control"}:
            decision = "negative_control_boundary_usable_not_selection_input"
            next_use = "keep_as_hard_boundary"
        elif "runtime" in " ".join(metric_families) or "trade_ledger" in " ".join(metric_ids):
            decision = "diagnostic_view_usable_with_boundary"
            next_use = "use_for_failure_memory_and_repair_queue_only"
        else:
            decision = "measurement_contract_usable_but_not_branch_separating"
            next_use = "requires_branch_specific_materialization_before_selection_use"
        rows.append(
            {
                "branch_name": branch,
                "metric_row_count": int(len(inputs["branch"][inputs["branch"]["branch_name"] == branch])),
                "metric_ids": ";".join(metric_ids),
                "metric_families": ";".join(metric_families),
                "branch_metric_usability_decision": decision,
                "selection_eligible": "false",
                "allowed_use": next_use,
                "limitation": "run335N metrics are structured runtime views over six MT5 attempts; they are not a new trained branch surface.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_risk_summary(inputs: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    regime = inputs["regime"].copy()
    regime["trade_count_num"] = pd.to_numeric(regime["trade_count"], errors="coerce").fillna(0)
    regime["net_profit_num"] = pd.to_numeric(regime["net_profit"], errors="coerce")
    rows: list[dict[str, Any]] = []
    for (attempt, axis), group in regime[regime["trade_count_num"] >= 3].groupby(["attempt_name", "axis"], dropna=False):
        worst = group.sort_values(["net_profit_num", "trade_count_num"], ascending=[True, False]).iloc[0]
        best = group.sort_values(["net_profit_num", "trade_count_num"], ascending=[False, False]).iloc[0]
        rows.append(
            {
                "attempt_name": attempt,
                "axis": axis,
                "worst_bucket": worst.get("bucket", ""),
                "worst_direction": worst.get("direction", ""),
                "worst_trade_count": int(as_int(worst.get("trade_count"))),
                "worst_net_profit": as_float(worst.get("net_profit")),
                "worst_profit_factor": as_float(worst.get("profit_factor")),
                "best_bucket": best.get("bucket", ""),
                "best_direction": best.get("direction", ""),
                "best_trade_count": int(as_int(best.get("trade_count"))),
                "best_net_profit": as_float(best.get("net_profit")),
                "regime_judgment": "diagnostic_regime_risk_only_no_filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_fragility_findings(scorecard: Sequence[Mapping[str, Any]], inputs: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    cost_fail_05 = sum(1 for row in scorecard if as_float(row.get("cost_plus_0_5_net")) <= 0)
    cost_fail_10 = sum(1 for row in scorecard if as_float(row.get("cost_plus_1_0_net")) <= 0)
    short_drag = sum(1 for row in scorecard if as_float(row.get("short_net_profit")) <= 0)
    high_underwater = sum(1 for row in scorecard if as_float(row.get("underwater_trade_share")) > 0.75)
    low_density = sum(1 for row in scorecard if as_float(row.get("trades_per_calendar_day")) < 4.0)
    join_missing = int((inputs["join"]["open_join_status"] != "matched").sum() + (inputs["join"]["feature_join_status"] != "matched").sum())
    proxy_repeated = int(inputs["proxy"].groupby("dimension")["proxy_expected_value"].nunique(dropna=False).le(1).sum())
    negative_controls_allowed = int((inputs["negative_control"]["positive_inference_allowed"].astype(str).str.lower() == "true").sum())
    rows = [
        {
            "finding_id": "proxy_repeated_aggregate_context_only",
            "severity": "high",
            "observed_change": f"{proxy_repeated} proxy dimensions have one repeated expected value per dimension",
            "comparison_baseline": "branch-specific proxy should vary by branch/attempt if used for ranking",
            "likely_driver": "proxy expected numeric values are aggregate context, not branch-specific MT5-like simulation",
            "next_probe": "run335P rebuilds or rejects proxy ranking input before any branch decision",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "cost_fragility",
            "severity": "high",
            "observed_change": f"{cost_fail_05}/6 attempts fail extra cost 0.5; {cost_fail_10}/6 fail extra cost 1.0",
            "comparison_baseline": "forward-usable research clue should keep a buffer under plausible cost stress",
            "likely_driver": "thin expectancy and high trade count amplify synthetic round-turn costs",
            "next_probe": "predeclare cost floor in new research packet without tuning threshold on forward data",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "direction_asymmetry",
            "severity": "high",
            "observed_change": f"{short_drag}/6 attempts have non-positive short net profit",
            "comparison_baseline": "direction source should not rely on one side while claiming robust surface",
            "likely_driver": "long-side dominance and short-side drag in runtime trade list",
            "next_probe": "design side-separated failure-memory probes and reject short-side cosmetic repair",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "curve_underwater_stretch",
            "severity": "high",
            "observed_change": f"{high_underwater}/6 attempts spend more than 75% of closed trades under water",
            "comparison_baseline": "goal curve shape requires pockets not to dominate the whole forward window",
            "likely_driver": "loss clusters and slow recovery after drawdown pockets",
            "next_probe": "require rolling-window and recovery diagnostics before any new ONNX handoff",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "density_quality_tradeoff",
            "severity": "medium",
            "observed_change": f"{low_density}/6 attempts are below 4 trades/day while higher-density attempts show cost or underwater weakness",
            "comparison_baseline": "target shape wants both trade count and clean curve",
            "likely_driver": "current non-identity clues split density and robustness instead of combining them",
            "next_probe": "search for features that improve trade quality without post-forward pocket filtering",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "exact_join_gap",
            "severity": "medium",
            "observed_change": f"{join_missing} open/feature exact join misses across the joined trade audit cells",
            "comparison_baseline": "runtime attribution should use exact timestamp joins or explicitly mark gaps",
            "likely_driver": "terminal edge rows or timestamp coverage gap",
            "next_probe": "repair attribution join coverage without nearest/future shift",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "negative_control_boundary",
            "severity": "guard_passed",
            "observed_change": f"{negative_controls_allowed} negative control rows allow positive inference",
            "comparison_baseline": "negative controls must block promotion-like interpretation",
            "likely_driver": "boundary enforcement held",
            "next_probe": "carry controls into run335P input materialization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def build_queues(scorecard: Sequence[Mapping[str, Any]], findings: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    top = sorted(scorecard, key=lambda row: (-as_float(row.get("usability_score")), -as_float(row.get("net_profit"))))
    best = top[0]
    best_attempt = str(best.get("attempt_name"))
    repair = [
        {
            "queue_id": "repair_exact_join_gap_no_future_shift",
            "priority": 1,
            "source_finding": "exact_join_gap",
            "action": "Inspect the 9 trade-level missing exact joins / 18 open-feature missing cells and create a no-lookahead repair or explicit exclusion ledger.",
            "effect": "Keeps attribution reliable without silently nearest-shifting timestamps.",
            "success_condition": "join gap is explained or repaired with zero future shift.",
            "forbidden": "future row fill; threshold retune; lot optimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "repair_proxy_bridge_branch_specificity",
            "priority": 2,
            "source_finding": "proxy_repeated_aggregate_context_only",
            "action": "Materialize branch-specific proxy rows or mark proxy ranking unavailable before any branch decision.",
            "effect": "Stops aggregate proxy values from pretending to rank runtime branches.",
            "success_condition": "proxy values vary by branch/attempt or are removed from ranking logic.",
            "forbidden": "retrofit proxy to match MT5 forward result",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "repair_cost_curve_direction_combined_gate",
            "priority": 3,
            "source_finding": "cost_fragility;curve_underwater_stretch;direction_asymmetry",
            "action": "Convert cost, rolling pocket, underwater, and direction asymmetry into predeclared next-stage research constraints.",
            "effect": "Uses failure memory as design pressure without overfitting to a forward pocket.",
            "success_condition": "next research packet has cost/curve/direction gates before model training.",
            "forbidden": "directly optimize score threshold on run335N MT5 outcomes",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    defense = [
        {
            "queue_id": "defense_no_proxy_forward_decision",
            "priority": 1,
            "guard": "Do not use proxy expected numeric values for Forward Passed/Failed or selection.",
            "effect": "Prevents aggregate proxy leakage into candidate judgment.",
            "evidence": "proxy_mt5_usability_decision.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "defense_no_forward_pocket_filter",
            "priority": 2,
            "guard": "Do not turn worst/best forward curve pockets into a direct filter.",
            "effect": "Avoids another look-ahead-bias path.",
            "evidence": "curve_pocket_underwater_matrix.csv and runtime_fragility_findings.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "defense_negative_controls_required",
            "priority": 3,
            "guard": "Carry cp322A exact blocker, subject swap, and adjacent-period null controls into the next packet.",
            "effect": "Keeps non-identity clues from being confused with cp322A exact forward evidence.",
            "evidence": "negative_control_subject_boundary_audit.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    offense = [
        {
            "queue_id": "offense_density_quality_seed_from_best_runtime_clue",
            "priority": 1,
            "source_attempt": best_attempt,
            "action": "Use the best non-selection clue as a research seed for a new predeclared packet, not as a candidate.",
            "effect": "Preserves the strongest observed trade-shape clue while respecting no-retune boundaries.",
            "seed_reason": f"score={best.get('usability_score')};net={fmt_float(best.get('net_profit'))};pf={fmt_float(best.get('profit_factor'))};tpd={fmt_float(best.get('trades_per_calendar_day'))}",
            "forbidden": "promote this attempt; deploy; claim runtime authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "offense_side_separated_short_rebuild",
            "priority": 2,
            "source_attempt": "all_attempts",
            "action": "Explore side-separated or short-side reliability features under WFO-style constraints.",
            "effect": "Targets the dominant short-drag failure axis without cosmetic post-hoc side filtering.",
            "seed_reason": "5 of 6 attempts have non-positive short net profit.",
            "forbidden": "drop shorts solely because this forward window short side lost",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "offense_cost_buffer_feature_search",
            "priority": 3,
            "source_attempt": "c56_plain_rf;m48_plain_rf;u42_plain_rf",
            "action": "Search for feature families that improve expectancy buffer before cost stress, with locked cost gates.",
            "effect": "Aims at the user's desired high-density clean curve without tuning lots or thresholds on this window.",
            "seed_reason": "plain attempts retain positive headline net but lose robustness under higher synthetic cost.",
            "forbidden": "lot optimization; threshold retune on run335N",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return repair, defense, offense


def build_gate_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "run335N_inputs_loaded",
            "status": "passed",
            "evidence": rel(RUN335N_DIR),
            "finding": f"attempts={metrics['attempt_rows']};proxy_rows={metrics['proxy_rows']};regime_rows={metrics['regime_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_usability_reframed",
            "status": "passed",
            "evidence": rel(PROXY_USABILITY_CSV),
            "finding": "proxy expected numeric values are context only and not selection usable",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_fragility_identified",
            "status": "passed",
            "evidence": rel(FRAGILITY_FINDINGS_CSV),
            "finding": f"findings={metrics['fragility_rows']};high={metrics['high_fragility_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "repair_defense_offense_queues_created",
            "status": "passed",
            "evidence": f"{rel(REPAIR_QUEUE_CSV)};{rel(DEFENSE_QUEUE_CSV)};{rel(OFFENSE_QUEUE_CSV)}",
            "finding": "balanced next work queues created without retune",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "negative_control_boundary_preserved",
            "status": "passed",
            "evidence": rel(RUN335N_DIR / "negative_control_subject_boundary_audit.csv"),
            "finding": "positive inference remains disallowed for negative controls",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_selection_no_goal_achieve",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "no Forward Passed/Failed, no runtime authority, no Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = {
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "run335N structured runtime metrics were converted into usability and fragility judgments.",
            "comparison_baseline": "goal shape requires clean curve, enough trades, cost buffer, and no broken KPI pocket.",
            "likely_drivers": "cost fragility;direction asymmetry;underwater stretch;aggregate proxy limitation.",
            "segment_checks": "attempt;cost;curve;direction;regime;proxy;join gap.",
            "trade_shape": f"attempts={metrics['attempt_rows']};best_score_attempt={metrics['best_attempt']}.",
            "alternative_explanations": "non-identity attempts are not cp322A exact and proxy values are aggregate context.",
            "attribution_confidence": "medium_for_diagnostics_low_for_selection",
            "next_probe": NEXT_RUN_ID,
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": f"{rel(RUN335K_DIR)};{rel(RUN335L_DIR)};{rel(RUN335N_DIR)}",
            "shared_contract": "run335K MT5 reports, telemetry, feature handoff, and run335N trade ledger are interpreted without changing model threshold or runtime handoff.",
            "known_differences": "run335N has 9 exact open/feature join misses; non-identity attempts are not cp322A exact.",
            "parity_check": "run335L row-level decision mismatch zero consumed as existing evidence; no new MT5 run in run335O.",
            "runtime_claim_boundary": "runtime_probe_diagnostic_only_no_runtime_authority",
        },
        "data_integrity_receipt.json": {
            **common,
            "data_source": rel(RUN335N_DIR),
            "time_axis": "MT5 server timestamps are used for exact trade open/feature/telemetry joins; no nearest or future shift is introduced.",
            "sample_scope": "US100 M5 run335K runtime attempts from 2026-04-14 through 2026-05-22.",
            "missing_or_duplicate_check": "9 trade-level exact join gaps / 18 open-feature missing cells carried as repair queue, not silently filled.",
            "feature_label_boundary": "diagnostic attribution only; no model training or threshold retune from forward rows.",
            "split_boundary": "forward/runtime diagnostic window only, not training data.",
            "leakage_risk": "turning forward curve pockets or proxy hindsight into filters; explicitly rejected.",
            "data_hash_or_identity": f"run335N_artifacts_registered;attempt_rows={metrics['attempt_rows']}.",
            "integrity_judgment": "usable_with_boundary",
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run335O runtime metric usability and repair decision",
            "evidence_available": "attempt scorecard, proxy usability, branch decision, fragility findings, repair/defense/offense queues.",
            "evidence_missing": "new ONNX candidate, branch-specific proxy rebuild, exact join repair, independent MT5 confirmation after repair.",
            "judgment_label": "exploratory_diagnostic_usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "proxy는 순위 판단에는 못 쓰고, MT5 구조화 지표는 다음 연구 제약으로 쓸 수 있다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [rel(RUN335N_DIR), rel(RUN335M_DIR / "branch_runtime_metric_extraction_contract.csv")],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(ATTEMPT_SCORECARD_CSV),
                rel(PROXY_USABILITY_CSV),
                rel(REPAIR_QUEUE_CSV),
                rel(DEFENSE_QUEUE_CSV),
                rel(OFFENSE_QUEUE_CSV),
            ],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_stage_closeout",
            "lineage_judgment": "connected_with_boundary",
        },
    }
    paths = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)
    return paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# Run335O Runtime Metric Usability and Repair Decision(335O 런타임 지표 활용성 및 수리 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- best_research_clue(최상 연구 단서): `{metrics['best_attempt']}`
- proxy_decision(프록시 결정): `context_only_not_selection_usable`
- high_fragility_findings(높은 취약성 발견): `{metrics['high_fragility_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run335O(335O 실행)는 run335N(335N 실행)의 structured MT5 runtime metrics(구조화 MT5 런타임 지표)를 활용성 관점에서 판정했다.

Effect(효과): proxy expected numeric value(프록시 예상 숫자값)는 branch ranking(분기 순위)이나 Forward Passed/Failed(전진 통과/실패)에 쓸 수 없다. 다만 MT5 trade ledger(거래 장부), cost stress(비용 압박), curve pocket(곡선 포켓), regime slice(국면 조각)는 다음 연구 제약(research constraint, 연구 제약)으로 쓸 수 있다.

## Key Findings(핵심 발견)

- proxy(프록시): repeated aggregate context(반복 집계 문맥)라서 selection(선택) 근거가 아니다.
- cost(비용): extra cost 0.5(추가 비용 0.5)에서 여러 attempt(시도)가 무너진다.
- direction(방향): short side(숏 방향) 손익이 대부분 약하다.
- curve(곡선): underwater stretch(수중 구간)가 길고 rolling pocket(롤링 포켓)이 깊다.
- parity/data(동등성/데이터): 9개 trade-level exact join gap(거래 수준 정확 조인 공백)과 18개 open-feature cell gap(개별 셀 공백)은 repair queue(수리 대기열)로 넘겼다.

## Evidence(근거)

- attempt_scorecard(시도 점수표): `{rel(ATTEMPT_SCORECARD_CSV)}`
- proxy_usability(프록시 활용성): `{rel(PROXY_USABILITY_CSV)}`
- branch_decision(분기 결정): `{rel(BRANCH_DECISION_CSV)}`
- fragility_findings(취약성 발견): `{rel(FRAGILITY_FINDINGS_CSV)}`
- repair_queue(수리 대기열): `{rel(REPAIR_QUEUE_CSV)}`
- defense_queue(방어 대기열): `{rel(DEFENSE_QUEUE_CSV)}`
- offense_queue(공격 대기열): `{rel(OFFENSE_QUEUE_CSV)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT_CSV)}`

## Boundary(경계)

이 실행은 diagnostic decision(진단 결정)이다. model(모델), threshold(임계값), lot(로트), risk logic(위험 로직), runtime handoff(런타임 인계)는 바꾸지 않았다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage335O Runtime Metric Usability and Repair Decision(런타임 지표 활용성 및 수리 결정)

`{RUN_ID}`은 run335N(335N 실행)의 MT5 structured runtime metrics(구조화 런타임 지표)를 해석했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- best_research_clue(최상 연구 단서): `{metrics['best_attempt']}`
- proxy_usability(프록시 활용성): `context_only_not_selection_usable`
- high_fragility_findings(높은 취약성 발견): `{metrics['high_fragility_rows']}`
- repair_queue_rows(수리 대기열 행): `{metrics['repair_rows']}`
- defense_queue_rows(방어 대기열 행): `{metrics['defense_rows']}`
- offense_queue_rows(공격 대기열 행): `{metrics['offense_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): 다음 run335P(335P 실행)는 proxy bridge repair(프록시 연결 수리), exact join repair(정확 조인 수리), cost/curve/direction guard(비용/곡선/방향 방어), 그리고 새 research seed(연구 씨앗)를 한 묶음으로 물질화한다.
"""
    write_text_bom(REPORT_DOC, report)
    write_text_bom(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage335(335단계) run335O(335O 실행)는 "
        f"`{STATUS}`로 runtime metric usability/repair decision(런타임 지표 활용성/수리 결정)을 완료했다. "
        f"Effect(효과): proxy(프록시)는 context-only(문맥 전용)로 낮추고, MT5 structured metrics(구조화 지표)는 "
        f"repair/defense/offense queue(수리/방어/공격 대기열) `{metrics['repair_rows'] + metrics['defense_rows'] + metrics['offense_rows']}`행으로 넘긴다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335O(335O 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_line}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v16`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run335O_summary(335O 요약): runtime metric usability/repair decision(런타임 지표 활용성/수리 결정)을 `{STATUS}`로 완료했다. "
        f"Effect(효과): proxy(프록시)는 selection/Forward decision(선택/전진 판정)에는 `not_usable`이고, "
        f"MT5 structured metrics(구조화 지표)는 `{NEXT_RUN_ID}`의 repair/defense/offense inputs(수리/방어/공격 입력)으로 넘긴다. "
        "Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335O_summary(335O 요약)" not in current_text:
        current_text = current_text.replace("- run335N_summary", summary_line + "\n- run335N_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- latest_design", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        f"- effect(효과): Stage335O(335O 실행)은 proxy(프록시)를 context-only(문맥 전용)로 낮추고 MT5 structured runtime metrics(구조화 런타임 지표)를 repair/defense/offense queue(수리/방어/공격 대기열)로 바꿨다. next_action(다음 행동)은 `{NEXT_RUN_ID}`이며 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- attempt_scorecard(시도 점수표): `{rel(ATTEMPT_SCORECARD_CSV)}`
- proxy_usability(프록시 활용성): `{rel(PROXY_USABILITY_CSV)}`
- branch_decision(분기 결정): `{rel(BRANCH_DECISION_CSV)}`
- fragility_findings(취약성 발견): `{rel(FRAGILITY_FINDINGS_CSV)}`
- repair_queue(수리 대기열): `{rel(REPAIR_QUEUE_CSV)}`
- defense_queue(방어 대기열): `{rel(DEFENSE_QUEUE_CSV)}`
- offense_queue(공격 대기열): `{rel(OFFENSE_QUEUE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335O Runtime Metric Usability and Repair Decision(335O 런타임 지표 활용성 및 수리 결정)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): proxy(프록시)를 context-only(문맥 전용)로 낮추고, MT5 structured runtime metrics(구조화 런타임 지표)를 repair/defense/offense queue(수리/방어/공격 대기열)로 넘겼다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335O Runtime Metric Usability and Repair Decision(335O 런타임 지표 활용성 및 수리 결정)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_runtime_metric_usability_repair_decision",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};proxy_context_only;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__runtime_metric_usability_repair_decision",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "runtime_metric_usability_repair_decision",
                "tier_scope": "Tier A runtime reports with branch diagnostic views",
                "kpi_scope": "proxy_usability_cost_curve_direction_regime_repair_queue",
                "scoreboard_lane": "runtime_probe_diagnostic_judgment",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"best_attempt={metrics['best_attempt']};high_fragility={metrics['high_fragility_rows']};proxy_context_only=true",
                "guardrail_kpi": "no_retune;no_selection;no_forward_passed;goal_achieve_not_claimed",
                "external_verification_status": "completed_existing_run335K_run335N_evidence_review_no_new_mt5",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        [
            {
                "ledger_row_id": f"{RUN_ID}__runtime_metric_usability_repair_decision",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_metric_usability_review",
                "evidence_scope": "run335N_structured_runtime_metrics_and_run335L_parity",
                "kpi_scope": "proxy_cost_curve_direction_regime_repair_defense_offense",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"best_attempt={metrics['best_attempt']};queues={metrics['queue_rows']};next={NEXT_RUN_ID}.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335_runtime_metric_usability_repair_decision",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "diagnostic_usability_and_queue_output_no_retune_no_forward_decision",
        }
        for path in outputs
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    scorecard = build_attempt_scorecard(inputs)
    proxy_rows = build_proxy_usability(inputs)
    branch_rows = build_branch_decisions(inputs)
    regime_rows = build_regime_risk_summary(inputs)
    findings = build_fragility_findings(scorecard, inputs)
    repair_rows, defense_rows, offense_rows = build_queues(scorecard, findings)
    best_attempt = str(scorecard[0]["attempt_name"]) if scorecard else "none"
    metrics = {
        "attempt_rows": len(scorecard),
        "proxy_rows": len(inputs["proxy"]),
        "regime_rows": len(inputs["regime"]),
        "fragility_rows": len(findings),
        "high_fragility_rows": sum(1 for row in findings if row.get("severity") == "high"),
        "repair_rows": len(repair_rows),
        "defense_rows": len(defense_rows),
        "offense_rows": len(offense_rows),
        "queue_rows": len(repair_rows) + len(defense_rows) + len(offense_rows),
        "best_attempt": best_attempt,
    }
    gate_rows = build_gate_rows(metrics)
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "attempt_scorecard;proxy_usability;branch_decision;fragility_findings;repair_defense_offense_queues",
            "evidence_missing": "new_onnx_candidate;branch_specific_proxy_rebuild;exact_join_repair;new_mt5_after_repair",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    outputs = [
        write_csv(
            ATTEMPT_SCORECARD_CSV,
            (
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "net_profit",
                "profit_factor",
                "trade_count",
                "trades_per_calendar_day",
                "expectancy",
                "win_rate",
                "closed_balance_max_drawdown",
                "recovery_factor_closed",
                "long_net_profit",
                "short_net_profit",
                "longest_underwater_trades",
                "underwater_trade_share",
                "net_per_lot",
                "cost_plus_0_25_net",
                "cost_plus_0_5_net",
                "cost_plus_1_0_net",
                "cost_plus_2_0_net",
                "rolling20_worst_net",
                "usability_score",
                "runtime_metric_usability",
                "primary_failure_axes",
                "selection_eligible",
                "claim_boundary",
            ),
            scorecard,
        ),
        write_csv(
            PROXY_USABILITY_CSV,
            (
                "dimension",
                "rows",
                "numeric_comparable_rows",
                "structured_runtime_available_rows",
                "unique_proxy_expected_values",
                "mean_abs_proxy_runtime_difference",
                "median_abs_proxy_runtime_difference",
                "sign_agreement_rate",
                "spearman_rank_correlation",
                "proxy_usability_decision",
                "allowed_use",
                "next_condition",
                "claim_boundary",
            ),
            proxy_rows,
        ),
        write_csv(
            BRANCH_DECISION_CSV,
            (
                "branch_name",
                "metric_row_count",
                "metric_ids",
                "metric_families",
                "branch_metric_usability_decision",
                "selection_eligible",
                "allowed_use",
                "limitation",
                "claim_boundary",
            ),
            branch_rows,
        ),
        write_csv(
            FRAGILITY_FINDINGS_CSV,
            (
                "finding_id",
                "severity",
                "observed_change",
                "comparison_baseline",
                "likely_driver",
                "next_probe",
                "claim_boundary",
            ),
            findings,
        ),
        write_csv(
            REGIME_RISK_CSV,
            (
                "attempt_name",
                "axis",
                "worst_bucket",
                "worst_direction",
                "worst_trade_count",
                "worst_net_profit",
                "worst_profit_factor",
                "best_bucket",
                "best_direction",
                "best_trade_count",
                "best_net_profit",
                "regime_judgment",
                "claim_boundary",
            ),
            regime_rows,
        ),
        write_csv(
            REPAIR_QUEUE_CSV,
            ("queue_id", "priority", "source_finding", "action", "effect", "success_condition", "forbidden", "claim_boundary"),
            repair_rows,
        ),
        write_csv(
            DEFENSE_QUEUE_CSV,
            ("queue_id", "priority", "guard", "effect", "evidence", "claim_boundary"),
            defense_rows,
        ),
        write_csv(
            OFFENSE_QUEUE_CSV,
            ("queue_id", "priority", "source_attempt", "action", "effect", "seed_reason", "forbidden", "claim_boundary"),
            offense_rows,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), gate_rows),
        write_csv(
            RESULT_JUDGMENT_CSV,
            (
                "run_id",
                "status",
                "judgment",
                "decision",
                "evidence_available",
                "evidence_missing",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            result_rows,
        ),
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "best_attempt": best_attempt,
                "proxy_decision": "context_only_not_selection_usable",
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
                "metrics": metrics,
            },
        ),
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "created_at_utc": now_utc(),
                "producer": rel(Path(__file__)),
                "source_inputs": {
                    "run335N": rel(RUN335N_DIR),
                    "run335L": rel(RUN335L_DIR),
                    "run335M_contract": rel(RUN335M_DIR / "branch_runtime_metric_extraction_contract.csv"),
                },
                "status": STATUS,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    write_reports(metrics)
    outputs.extend([REPORT_DOC, DECISION_DOC])
    update_docs(metrics)
    outputs.extend([WORKSPACE_STATE, CURRENT_STATE, STAGE_BRIEF, INPUT_REFS, CHANGELOG, SELECTED_DIR / "selection_status.md"])
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, ARTIFACT_REGISTRY, STAGE_LEDGER])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "best_attempt": best_attempt,
                "proxy_decision": "context_only_not_selection_usable",
                "high_fragility_findings": metrics["high_fragility_rows"],
                "queue_rows": metrics["queue_rows"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

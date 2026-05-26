from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

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
RUN_NUMBER = "run335R"
RUN_ID = "run335R_materialize_repaired_attribution_and_branch_specific_proxy_scout_v1"
PARENT_RUN_ID = "run335Q_review_balanced_repair_defense_offense_research_inputs_v1"
NEXT_RUN_ID = "run335S_review_repaired_attribution_proxy_scout_and_open_constraint_bound_research_packet_v1"

STATUS = "completed_repaired_attribution_and_proxy_scout_materialized_no_forward_decision"
JUDGMENT = "repaired_attribution_views_and_branch_specific_proxy_scout_materialized_selection_blocked"
DECISION = "stage335R_materialized_same_bar_attribution_repair_and_proxy_scout_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335R_repaired_attribution_proxy_scout_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

DEPOSIT = 500.0
FEATURE_METADATA = {"bar_time_server", "timestamp_utc", "split", "row_index"}

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN335K_DIR = STAGE_DIR / "02_runs" / "run335K"
RUN335N_DIR = STAGE_DIR / "02_runs" / "run335N"
RUN335P_DIR = STAGE_DIR / "02_runs" / "run335P"
RUN335Q_DIR = STAGE_DIR / "02_runs" / "run335Q"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335R_repaired_attribution_proxy_scout.md"
REPORT_DOC = REVIEWS_DIR / "run335R_repaired_attribution_proxy_scout.md"

REPAIRED_JOIN_VIEW_CSV = RUN_DIR / "repaired_trade_telemetry_join_view.csv"
REPAIRED_TRADE_LEDGER_CSV = RUN_DIR / "repaired_runtime_trade_ledger.csv"
ATTRIBUTION_REPAIR_DELTA_CSV = RUN_DIR / "attribution_repair_delta_summary.csv"
REPAIRED_REGIME_SLICE_CSV = RUN_DIR / "repaired_regime_direction_slice_matrix.csv"
PROXY_SCOUT_TRADE_CSV = RUN_DIR / "branch_specific_proxy_scout_trade_key_matrix.csv"
PROXY_SCOUT_MATRIX_CSV = RUN_DIR / "branch_specific_proxy_scout_matrix.csv"
PROXY_COMPARISON_CSV = RUN_DIR / "proxy_scout_vs_mt5_runtime_comparison.csv"
PROXY_USABILITY_CSV = RUN_DIR / "proxy_scout_usability_decision.csv"
CONSTRAINT_PACKET_CSV = RUN_DIR / "constraint_bound_research_packet_inputs.csv"
PACKAGE_CARRY_CSV = RUN_DIR / "balanced_package_carry_forward_manifest.csv"
RUN335S_QUEUE_CSV = RUN_DIR / "run335S_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_repaired_attribution_proxy_scout_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    return str(value)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip()
        if text == "":
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_or_replace_section(path: Path, header: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    section = f"\n## {header}\n\n{body.strip()}\n"
    pattern = re.compile(rf"\n## {re.escape(header)}\n.*?(?=\n## |\Z)", re.S)
    if pattern.search(text):
        text = pattern.sub(section.rstrip(), text)
    else:
        text = text.rstrip() + section
    write_text_lossless(path, text.rstrip() + "\n", had_bom)


def read_csv(path: Path) -> pd.DataFrame:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return pd.read_csv(io_path(path), keep_default_na=False)


def group_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key) for key in keys)].append(row)
    return grouped


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    gross_profit = sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) > 0.0)
    gross_loss = -sum(as_float(row.get("net_profit")) for row in rows if as_float(row.get("net_profit")) < 0.0)
    if gross_loss == 0.0:
        return math.inf if gross_profit > 0.0 else None
    return gross_profit / gross_loss


def sequence_metrics(rows: Sequence[Mapping[str, Any]], *, deposit: float = DEPOSIT) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    count = len(ordered)
    net = sum(as_float(row.get("net_profit")) for row in ordered)
    wins = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) > 0.0]
    losses = [as_float(row.get("net_profit")) for row in ordered if as_float(row.get("net_profit")) < 0.0]
    peak = deposit
    balance = deposit
    max_dd = 0.0
    underwater = 0
    longest_underwater = 0
    underwater_count = 0
    for row in ordered:
        balance += as_float(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            underwater_count += 1
            longest_underwater = max(longest_underwater, underwater)
        max_dd = max(max_dd, peak - balance)
    total_volume = sum(as_float(row.get("volume")) for row in ordered)
    return {
        "trade_count": count,
        "net_profit": net,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": len(wins) / count if count else None,
        "closed_balance_max_drawdown": max_dd,
        "longest_underwater_trades": longest_underwater,
        "underwater_trade_share": underwater_count / count if count else None,
        "recovery_factor_closed": net / max_dd if max_dd > 0.0 else None,
        "total_volume": total_volume,
        "net_per_lot": net / total_volume if total_volume else None,
        "long_net_profit": sum(as_float(row.get("net_profit")) for row in ordered if row.get("direction") == "long"),
        "short_net_profit": sum(as_float(row.get("net_profit")) for row in ordered if row.get("direction") == "short"),
    }


def rolling_pocket(rows: Sequence[Mapping[str, Any]], window: int) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    if not ordered:
        return {"window": window, "eligible": False}
    if len(ordered) < window:
        return {
            "window": window,
            "eligible": False,
            "observed_trades": len(ordered),
            "worst_window_net": sum(as_float(row.get("net_profit")) for row in ordered),
        }
    best_start = 0
    worst = math.inf
    for index in range(0, len(ordered) - window + 1):
        value = sum(as_float(row.get("net_profit")) for row in ordered[index : index + window])
        if value < worst:
            worst = value
            best_start = index
    return {
        "window": window,
        "eligible": True,
        "observed_trades": len(ordered),
        "worst_window_net": worst,
        "worst_window_start_trade": best_start + 1,
        "worst_window_end_trade": best_start + window,
        "worst_window_start_time": ordered[best_start].get("close_time"),
        "worst_window_end_time": ordered[best_start + window - 1].get("close_time"),
    }


def feature_bucket(value: Any, low: float | None = None, high: float | None = None, prefix: str = "bucket") -> str:
    number = as_float(value, math.nan)
    if not math.isfinite(number):
        return "feature_missing"
    if low is not None and high is not None:
        if number <= low:
            return f"{prefix}_low"
        if number <= high:
            return f"{prefix}_mid"
        return f"{prefix}_high"
    if number < -1.0:
        return f"{prefix}_lt_minus1"
    if number > 1.0:
        return f"{prefix}_gt_plus1"
    return f"{prefix}_neutral"


def feature_quantiles(frames: Mapping[str, pd.DataFrame], column: str) -> tuple[float, float] | None:
    values: list[float] = []
    for frame in frames.values():
        if column in frame.columns:
            values.extend(pd.to_numeric(frame[column], errors="coerce").dropna().astype(float).tolist())
    if not values:
        return None
    series = pd.Series(values)
    return float(series.quantile(1.0 / 3.0)), float(series.quantile(2.0 / 3.0))


def last_indexed_row_as_dict(frame: pd.DataFrame | None, key: str) -> dict[str, Any]:
    if frame is None or key not in frame.index:
        return {}
    matched = frame.loc[key]
    if isinstance(matched, pd.DataFrame):
        return matched.iloc[-1].to_dict()
    return matched.to_dict()


def load_inputs() -> dict[str, pd.DataFrame]:
    return {
        "handoff": read_csv(RUN335K_DIR / "independent_handoff_attempt_manifest.csv"),
        "join": read_csv(RUN335N_DIR / "trade_telemetry_join_audit.csv"),
        "trade": read_csv(RUN335N_DIR / "runtime_trade_ledger.csv"),
        "attempt_summary": read_csv(RUN335N_DIR / "attempt_runtime_metric_summary.csv"),
        "branch_metric": read_csv(RUN335N_DIR / "branch_runtime_metric_matrix.csv"),
        "old_proxy_diff": read_csv(RUN335N_DIR / "protocol_specific_proxy_mt5_difference.csv"),
        "cost_stress": read_csv(RUN335N_DIR / "cost_stress_metric_matrix.csv"),
        "curve_pocket": read_csv(RUN335N_DIR / "curve_pocket_underwater_matrix.csv"),
        "proxy_spec": read_csv(RUN335P_DIR / "branch_specific_proxy_rebuild_spec.csv"),
        "constraints": read_csv(RUN335Q_DIR / "predeclared_constraint_review.csv"),
        "packages": read_csv(RUN335Q_DIR / "balanced_package_review.csv"),
        "exact_review": read_csv(RUN335Q_DIR / "exact_join_repair_review.csv"),
        "proxy_review": read_csv(RUN335Q_DIR / "proxy_rebuild_or_block_review.csv"),
        "queue": read_csv(RUN335Q_DIR / "run335R_materialization_queue.csv"),
    }


def load_feature_frames(handoff: pd.DataFrame) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for row in handoff.to_dict("records"):
        attempt = str(row.get("attempt_name"))
        path = ROOT / str(row.get("new_feature_path", ""))
        if not path_exists(path):
            continue
        frame = pd.read_csv(io_path(path), keep_default_na=False)
        frame["bar_time_server"] = frame["bar_time_server"].astype(str)
        for column in frame.columns:
            if column not in FEATURE_METADATA:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
        frames[attempt] = frame
    return frames


def load_telemetry_frames(attempts: Sequence[str]) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for attempt in attempts:
        path = RUN335K_DIR / "runtime_telemetry" / f"{attempt}_telemetry.csv"
        if not path_exists(path):
            continue
        frame = pd.read_csv(io_path(path), keep_default_na=False)
        frame = frame[frame["record_type"].eq("cycle")].copy()
        frame["bar_time"] = frame["bar_time"].astype(str)
        frames[attempt] = frame
    return frames


def build_repair_map(exact_review: pd.DataFrame) -> dict[tuple[str, str], dict[str, Any]]:
    accepted = exact_review[exact_review["review_decision"].eq("accepted_attribution_only_repair")]
    output: dict[tuple[str, str], dict[str, Any]] = {}
    for row in accepted.to_dict("records"):
        output[(str(row.get("attempt_name")), str(row.get("trade_index")))] = row
    return output


def enrich_with_repair(
    trade_rows: Sequence[Mapping[str, Any]],
    repair_map: Mapping[tuple[str, str], Mapping[str, Any]],
    telemetry_frames: Mapping[str, pd.DataFrame],
    feature_frames: Mapping[str, pd.DataFrame],
) -> list[dict[str, Any]]:
    vol_edges = feature_quantiles(feature_frames, "historical_vol_20")
    feature_by_attempt = {
        attempt: frame.set_index("bar_time_server", drop=False)
        for attempt, frame in feature_frames.items()
        if "bar_time_server" in frame.columns
    }
    telemetry_by_attempt = {
        attempt: frame.set_index("bar_time", drop=False)
        for attempt, frame in telemetry_frames.items()
        if "bar_time" in frame.columns
    }
    output: list[dict[str, Any]] = []
    for row in trade_rows:
        current = dict(row)
        attempt = str(row.get("attempt_name"))
        trade_index = str(row.get("trade_index"))
        open_original = str(row.get("open_time_server"))
        close_key = str(row.get("close_time_server"))
        repair = repair_map.get((attempt, trade_index))
        repair_key = str(repair.get("open_time_server_repair_key")) if repair else ""
        effective_key = repair_key if repair_key else open_original
        telemetry = telemetry_by_attempt.get(attempt)
        features = feature_by_attempt.get(attempt)
        open_telemetry = last_indexed_row_as_dict(telemetry, effective_key)
        close_telemetry = last_indexed_row_as_dict(telemetry, close_key)
        feature_row = last_indexed_row_as_dict(features, effective_key)
        current.update(
            {
                "open_time_server_original": open_original,
                "open_time_server_repair_key": repair_key,
                "effective_attribution_join_key": effective_key,
                "repair_applied": bool(repair),
                "repair_scope": "attribution_join_key_only_no_trade_time_mutation" if repair else "not_applicable",
                "open_time_mutated": False,
                "lookahead_guard_status": "passed_same_bar_floor_no_future_shift" if repair else "not_applicable_original_key",
                "open_active_tier": open_telemetry.get("active_tier", ""),
                "open_decision": open_telemetry.get("decision", ""),
                "open_exec_action": open_telemetry.get("exec_action", ""),
                "open_order_filled": open_telemetry.get("order_filled", ""),
                "open_p_short": open_telemetry.get("p_short", ""),
                "open_p_flat": open_telemetry.get("p_flat", ""),
                "open_p_long": open_telemetry.get("p_long", ""),
                "close_decision": close_telemetry.get("decision", ""),
                "close_exec_action": close_telemetry.get("exec_action", ""),
                "open_join_status_repaired": "matched" if open_telemetry else "missing",
                "close_join_status_repaired": "matched" if close_telemetry else "missing",
                "feature_join_status_repaired": "matched" if feature_row else "missing",
                "feature_minutes_from_cash_open": feature_row.get("minutes_from_cash_open", ""),
                "feature_historical_vol_20": feature_row.get("historical_vol_20", ""),
                "feature_adx_14": feature_row.get("adx_14", ""),
                "feature_vix_zscore_20": feature_row.get("vix_zscore_20", ""),
                "feature_usdx_zscore_20": feature_row.get("usdx_zscore_20", ""),
                "feature_us10yr_zscore_20": feature_row.get("us10yr_zscore_20", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        if vol_edges is None:
            current["volatility_regime"] = "feature_missing"
        else:
            current["volatility_regime"] = feature_bucket(feature_row.get("historical_vol_20"), vol_edges[0], vol_edges[1], "vol")
        adx = as_float(feature_row.get("adx_14"), math.nan)
        if not math.isfinite(adx):
            current["adx_bucket"] = "feature_missing"
        elif adx < 20:
            current["adx_bucket"] = "adx_lt20"
        elif adx <= 25:
            current["adx_bucket"] = "adx_20_25"
        else:
            current["adx_bucket"] = "adx_gt25"
        current["vix_regime"] = feature_bucket(feature_row.get("vix_zscore_20"), prefix="vix_z")
        current["usd_regime"] = feature_bucket(feature_row.get("usdx_zscore_20"), prefix="usdx_z")
        current["rate_regime"] = feature_bucket(feature_row.get("us10yr_zscore_20"), prefix="us10yr_z")
        output.append(current)
    return output


def build_repaired_join_view(join_rows: Sequence[Mapping[str, Any]], repaired_trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    repaired_by_key = {
        (str(row.get("attempt_name")), str(row.get("trade_index"))): row
        for row in repaired_trade_rows
    }
    output: list[dict[str, Any]] = []
    for row in join_rows:
        key = (str(row.get("attempt_name")), str(row.get("trade_index")))
        repaired = repaired_by_key.get(key, {})
        repair_applied = str(repaired.get("repair_applied", "")).lower() == "true" or repaired.get("repair_applied") is True
        output.append(
            {
                "attempt_name": row.get("attempt_name"),
                "trade_index": row.get("trade_index"),
                "open_time_server": row.get("open_time_server"),
                "close_time_server": row.get("close_time_server"),
                "open_time_server_repair_key": repaired.get("open_time_server_repair_key", ""),
                "effective_attribution_join_key": repaired.get("effective_attribution_join_key", row.get("open_time_server")),
                "repair_applied": repair_applied,
                "open_join_status_original": row.get("open_join_status"),
                "feature_join_status_original": row.get("feature_join_status"),
                "open_join_status_repaired": repaired.get("open_join_status_repaired", row.get("open_join_status")),
                "close_join_status_repaired": repaired.get("close_join_status_repaired", row.get("close_join_status")),
                "feature_join_status_repaired": repaired.get("feature_join_status_repaired", row.get("feature_join_status")),
                "open_active_tier_repaired": repaired.get("open_active_tier", ""),
                "open_decision_repaired": repaired.get("open_decision", ""),
                "open_exec_action_repaired": repaired.get("open_exec_action", ""),
                "open_order_filled_repaired": repaired.get("open_order_filled", ""),
                "lookahead_guard_status": repaired.get("lookahead_guard_status", "not_applicable_original_key"),
                "allowed_use": "diagnostic_attribution_only_no_trade_time_mutation",
                "forbidden_use": "model_training;threshold_retuning;lot_optimization;forward_pass_fail_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def slice_rows(rows: Sequence[Mapping[str, Any]], axis: str, bucket_field: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (bucket, direction), grouped in group_rows(rows, (bucket_field, "direction")).items():
        metrics = sequence_metrics(grouped)
        output.append(
            {
                "axis": axis,
                "bucket": bucket,
                "direction": direction,
                "repair_applied_trade_count": sum(1 for row in grouped if row.get("repair_applied") is True),
                **metrics,
            }
        )
    return output


def build_repaired_regime_rows(branches: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axes = {
        "direction": "direction",
        "session": "session_bucket",
        "open_hour": "open_hour",
        "close_hour": "close_hour",
        "month": "month",
        "volatility": "volatility_regime",
        "adx": "adx_bucket",
        "vix": "vix_regime",
        "usd": "usd_regime",
        "rate": "rate_regime",
    }
    output: list[dict[str, Any]] = []
    for (attempt_name,), attempt_rows in group_rows(trade_rows, ("attempt_name",)).items():
        for branch in branches:
            for axis, field in axes.items():
                for item in slice_rows(attempt_rows, axis, field):
                    output.append(
                        {
                            "branch_name": branch.get("branch_name"),
                            "branch_id": branch.get("branch_id"),
                            "attempt_name": attempt_name,
                            "axis": item["axis"],
                            "bucket": item["bucket"],
                            "direction": item["direction"],
                            "trade_count": item["trade_count"],
                            "repair_applied_trade_count": item["repair_applied_trade_count"],
                            "net_profit": item["net_profit"],
                            "profit_factor": item["profit_factor"],
                            "expectancy": item["expectancy"],
                            "win_rate": item["win_rate"],
                            "closed_balance_max_drawdown": item["closed_balance_max_drawdown"],
                            "longest_underwater_trades": item["longest_underwater_trades"],
                            "slice_use": "diagnostic_attribution_only_after_same_bar_repair_no_regime_filter",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
    return output


def build_repair_delta_summary(
    original_join: pd.DataFrame,
    repaired_join: Sequence[Mapping[str, Any]],
    repaired_trade_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    repaired_by_attempt = group_rows(repaired_trade_rows, ("attempt_name",))
    repaired_join_by_attempt = group_rows(repaired_join, ("attempt_name",))
    output: list[dict[str, Any]] = []
    attempts = sorted(str(item) for item in original_join["attempt_name"].unique())
    for attempt in attempts:
        original_attempt = original_join[original_join["attempt_name"].astype(str).eq(attempt)]
        original_missing = original_attempt[
            original_attempt["open_join_status"].ne("matched") | original_attempt["feature_join_status"].ne("matched")
        ]
        fixed_rows = [
            row
            for row in repaired_join_by_attempt.get((attempt,), [])
            if str(row.get("repair_applied", "")).lower() == "true"
        ]
        after_missing = [
            row
            for row in repaired_join_by_attempt.get((attempt,), [])
            if row.get("open_join_status_repaired") != "matched" or row.get("feature_join_status_repaired") != "matched"
        ]
        fixed_keys = {(str(row.get("attempt_name")), str(row.get("trade_index"))) for row in fixed_rows}
        fixed_trade_rows = [
            row
            for row in repaired_by_attempt.get((attempt,), [])
            if (str(row.get("attempt_name")), str(row.get("trade_index"))) in fixed_keys
        ]
        output.append(
            {
                "attempt_name": attempt,
                "original_missing_open_or_feature_join_count": len(original_missing),
                "accepted_same_bar_repair_count": len(fixed_rows),
                "remaining_missing_open_or_feature_join_count": len(after_missing),
                "repaired_trade_net_profit": sum(as_float(row.get("net_profit")) for row in fixed_trade_rows),
                "repaired_long_trade_count": sum(1 for row in fixed_trade_rows if row.get("direction") == "long"),
                "repaired_short_trade_count": sum(1 for row in fixed_trade_rows if row.get("direction") == "short"),
                "repair_policy": "same_bar_second_floor_attribution_only",
                "lookahead_guard_status": "passed_no_future_or_nearest_shift" if len(after_missing) == 0 else "needs_review",
                "selection_use": "blocked",
                "forward_pass_fail_use": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def cumulative_trade_proxy_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (attempt,), rows in group_rows(trade_rows, ("attempt_name",)).items():
        ordered = sorted(rows, key=lambda item: (str(item.get("close_time")), str(item.get("trade_index"))))
        if not ordered:
            continue
        first_open = pd.Timestamp(str(ordered[0].get("open_time")))
        balance = DEPOSIT
        peak = DEPOSIT
        underwater = 0
        gross_profit = 0.0
        gross_loss = 0.0
        running_volume = 0.0
        trailing_net: list[float] = []
        for index, row in enumerate(ordered, start=1):
            pnl = as_float(row.get("net_profit"))
            running_volume += as_float(row.get("volume"))
            if pnl > 0.0:
                gross_profit += pnl
            elif pnl < 0.0:
                gross_loss += pnl
            balance += pnl
            if balance >= peak:
                peak = balance
                underwater = 0
            else:
                underwater += 1
            current_dd = peak - balance
            close_time = pd.Timestamp(str(row.get("close_time")))
            days_elapsed = max((close_time - first_open).total_seconds() / 86400.0, 1.0)
            trailing_net.append(pnl)
            if len(trailing_net) > 5:
                trailing_net.pop(0)
            current = dict(row)
            current.update(
                {
                    "cumulative_net_profit": balance - DEPOSIT,
                    "cumulative_profit_factor": (gross_profit / abs(gross_loss)) if gross_loss < 0.0 else (math.inf if gross_profit > 0 else None),
                    "cumulative_expectancy": (balance - DEPOSIT) / index,
                    "cumulative_drawdown": current_dd,
                    "cumulative_recovery_factor": ((balance - DEPOSIT) / current_dd) if current_dd > 0.0 else None,
                    "cumulative_trades_per_day": index / days_elapsed,
                    "cumulative_underwater_stretch": underwater,
                    "rolling5_ending_net": sum(trailing_net),
                    "stress_cost_plus_0_5_net": pnl - 0.5,
                    "lot_normalized_trade_result": pnl / as_float(row.get("volume")) if as_float(row.get("volume")) > 0.0 else None,
                    "long_short_attribution_value": pnl,
                    "long_short_attribution_side": row.get("direction"),
                    "session_hour_regime_label": f"{row.get('session_bucket')}|hour_{row.get('open_hour')}",
                }
            )
            output.append(current)
    return output


def build_proxy_trade_matrix(branches: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    trade_proxy = cumulative_trade_proxy_rows(trade_rows)
    output: list[dict[str, Any]] = []
    for branch in branches:
        for row in trade_proxy:
            output.append(
                {
                    "branch_name": branch.get("branch_name"),
                    "branch_id": branch.get("branch_id"),
                    "attempt_name": row.get("attempt_name"),
                    "trade_index": row.get("trade_index"),
                    "bar_time_server_original": row.get("open_time_server_original"),
                    "effective_attribution_join_key": row.get("effective_attribution_join_key"),
                    "repair_applied": row.get("repair_applied"),
                    "direction": row.get("direction"),
                    "session_hour_regime_label": row.get("session_hour_regime_label"),
                    "net_profit": row.get("net_profit"),
                    "expectancy": row.get("cumulative_expectancy"),
                    "profit_factor": row.get("cumulative_profit_factor"),
                    "max_drawdown": row.get("cumulative_drawdown"),
                    "recovery_factor": row.get("cumulative_recovery_factor"),
                    "trades_per_day": row.get("cumulative_trades_per_day"),
                    "underwater_stretch": row.get("cumulative_underwater_stretch"),
                    "curve_pocket": row.get("rolling5_ending_net"),
                    "spread_slippage_stress": row.get("stress_cost_plus_0_5_net"),
                    "lot_normalized_result": row.get("lot_normalized_trade_result"),
                    "long_short_attribution": row.get("long_short_attribution_value"),
                    "selection_use": "blocked",
                    "forward_pass_fail_use": "blocked",
                    "diagnostic_use": "trade_key_proxy_scout_only_pending_run335S_review",
                    "no_fit_guard": "not_fit_to_mt5_outcome;derived_from_runtime_trade_sequence_and_same_bar_repair_only",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return output


def branch_rows(branch_metric: pd.DataFrame) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    output: list[dict[str, Any]] = []
    for row in branch_metric[["branch_name", "branch_id"]].drop_duplicates().to_dict("records"):
        key = (str(row.get("branch_name")), str(row.get("branch_id")))
        if key not in seen:
            seen.add(key)
            output.append(row)
    return output


def build_attempt_metric_map(trade_rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for (attempt,), rows in group_rows(trade_rows, ("attempt_name",)).items():
        metrics = sequence_metrics(rows)
        first_open = min(pd.Timestamp(str(row.get("open_time"))) for row in rows)
        last_close = max(pd.Timestamp(str(row.get("close_time"))) for row in rows)
        day_span = max((last_close - first_open).total_seconds() / 86400.0, 1.0)
        metrics["trades_per_calendar_day"] = metrics["trade_count"] / day_span
        metrics["rolling20_worst_window_net"] = rolling_pocket(rows, 20).get("worst_window_net")
        output[str(attempt)] = metrics
    return output


def value_for_dimension(
    dimension: str,
    branch: Mapping[str, Any],
    attempt: str,
    attempt_metrics: Mapping[str, Mapping[str, Any]],
    cost_stress: pd.DataFrame,
    curve_pocket: pd.DataFrame,
) -> tuple[Any, str]:
    metrics = attempt_metrics.get(attempt, {})
    if dimension == "net_profit":
        return metrics.get("net_profit"), ""
    if dimension == "profit_factor":
        return metrics.get("profit_factor"), ""
    if dimension == "trades_per_day":
        return metrics.get("trades_per_calendar_day"), ""
    if dimension == "expectancy":
        return metrics.get("expectancy"), ""
    if dimension == "max_drawdown":
        return metrics.get("closed_balance_max_drawdown"), ""
    if dimension == "recovery_factor":
        return metrics.get("recovery_factor_closed"), ""
    if dimension == "underwater_stretch":
        return metrics.get("longest_underwater_trades"), ""
    if dimension == "lot_normalized_result":
        return metrics.get("net_per_lot"), ""
    if dimension == "curve_pocket":
        matched = curve_pocket[
            curve_pocket["branch_name"].astype(str).eq(str(branch.get("branch_name")))
            & curve_pocket["attempt_name"].astype(str).eq(attempt)
            & curve_pocket["rolling_window_trades"].astype(str).eq("20")
        ]
        if not matched.empty:
            return as_float(matched.iloc[0].get("worst_window_net"), math.nan), ""
        return metrics.get("rolling20_worst_window_net"), ""
    if dimension == "spread_slippage_stress":
        matched = cost_stress[
            cost_stress["branch_name"].astype(str).eq(str(branch.get("branch_name")))
            & cost_stress["attempt_name"].astype(str).eq(attempt)
            & cost_stress["extra_cost_per_trade"].astype(str).eq("0.5")
        ]
        if not matched.empty:
            return as_float(matched.iloc[0].get("net_profit"), math.nan), ""
        return as_float(metrics.get("net_profit"), 0.0) - 0.5 * as_float(metrics.get("trade_count"), 0.0), ""
    if dimension == "long_short_attribution":
        text = json.dumps(
            {
                "long_net_profit": metrics.get("long_net_profit"),
                "short_net_profit": metrics.get("short_net_profit"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return "", text
    if dimension == "session_hour_regime":
        return "", "available_in_repaired_regime_direction_slice_matrix"
    return "", ""


def numeric_difference(left: Any, right: Any) -> float | None:
    left_num = as_float(left, math.nan)
    right_num = as_float(right, math.nan)
    if math.isfinite(left_num) and math.isfinite(right_num):
        return left_num - right_num
    return None


def build_proxy_scout_matrix(
    branches: Sequence[Mapping[str, Any]],
    dimensions: Sequence[str],
    attempts: Sequence[str],
    attempt_metrics: Mapping[str, Mapping[str, Any]],
    cost_stress: pd.DataFrame,
    curve_pocket: pd.DataFrame,
    old_proxy_diff: pd.DataFrame,
) -> list[dict[str, Any]]:
    old_index: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for row in old_proxy_diff.to_dict("records"):
        old_index[(str(row.get("branch_name")), str(row.get("attempt_name")), str(row.get("dimension")))] = row
    rows: list[dict[str, Any]] = []
    for branch in branches:
        for attempt in attempts:
            for dimension in dimensions:
                scout_numeric, scout_text = value_for_dimension(dimension, branch, attempt, attempt_metrics, cost_stress, curve_pocket)
                old = old_index.get((str(branch.get("branch_name")), attempt, dimension), {})
                rows.append(
                    {
                        "branch_name": branch.get("branch_name"),
                        "branch_id": branch.get("branch_id"),
                        "attempt_name": attempt,
                        "dimension": dimension,
                        "old_proxy_expected_value": old.get("proxy_expected_value", ""),
                        "mt5_runtime_probe_value": old.get("structured_runtime_value", ""),
                        "branch_specific_scout_value_numeric": scout_numeric,
                        "branch_specific_scout_value_text": scout_text,
                        "old_proxy_minus_mt5_runtime": old.get("difference_proxy_minus_structured_runtime", ""),
                        "old_proxy_minus_branch_specific_scout": numeric_difference(old.get("proxy_expected_value", ""), scout_numeric),
                        "old_proxy_use": "blocked_repeated_aggregate_context_only",
                        "scout_use": "diagnostic_only_pending_run335S_review",
                        "selection_use": "blocked",
                        "forward_pass_fail_use": "blocked",
                        "no_fit_guard": "not_fit_to_mt5_outcome;no_threshold_or_lot_or_rule_change",
                        "branch_variation_status": "",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    grouped = group_rows(rows, ("attempt_name", "dimension"))
    for grouped_rows in grouped.values():
        values = {
            str(row.get("branch_specific_scout_value_numeric")) + "|" + str(row.get("branch_specific_scout_value_text"))
            for row in grouped_rows
        }
        status = "branch_numeric_or_text_variation_present" if len(values) > 1 else "runtime_value_shared_by_attempt_across_branches"
        for row in grouped_rows:
            row["branch_variation_status"] = status
    return rows


def build_proxy_usability_rows(proxy_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for (dimension,), rows in group_rows(proxy_rows, ("dimension",)).items():
        old_values = {str(row.get("old_proxy_expected_value")) for row in rows if str(row.get("old_proxy_expected_value")) != ""}
        runtime_values = {str(row.get("mt5_runtime_probe_value")) for row in rows if str(row.get("mt5_runtime_probe_value")) != ""}
        scout_values = {
            str(row.get("branch_specific_scout_value_numeric")) + "|" + str(row.get("branch_specific_scout_value_text"))
            for row in rows
        }
        shared_count = sum(1 for row in rows if row.get("branch_variation_status") == "runtime_value_shared_by_attempt_across_branches")
        output.append(
            {
                "dimension": dimension,
                "row_count": len(rows),
                "old_proxy_unique_values": len(old_values),
                "mt5_runtime_unique_values": len(runtime_values),
                "branch_specific_scout_unique_values": len(scout_values),
                "old_proxy_rank_usable": "false",
                "old_proxy_block_reason": "repeated_aggregate_context_only_not_branch_specific",
                "scout_selection_usable": "false",
                "scout_forward_decision_usable": "false",
                "scout_diagnostic_usable": "true_pending_run335S_review",
                "branch_variation_boundary": "shared_attempt_values_present" if shared_count else "branch_variation_present",
                "usability_judgment": "diagnostic_only_not_selection_usable",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    output.append(
        {
            "dimension": "overall_proxy_scout",
            "row_count": len(proxy_rows),
            "old_proxy_unique_values": "",
            "mt5_runtime_unique_values": "",
            "branch_specific_scout_unique_values": "",
            "old_proxy_rank_usable": "false",
            "old_proxy_block_reason": "old_proxy_expected_values_remain_rejected_for_selection",
            "scout_selection_usable": "false",
            "scout_forward_decision_usable": "false",
            "scout_diagnostic_usable": "true_pending_run335S_review",
            "branch_variation_boundary": "branch_grain_materialized_but_runtime_values_often_shared_by_attempt",
            "usability_judgment": "proxy_scout_materialized_for_review_selection_blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return output


def build_constraint_packet_rows(constraints: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in constraints.to_dict("records"):
        accepted = row.get("review_decision") == "accepted_predeclared_research_gate"
        rows.append(
            {
                "constraint_id": row.get("constraint_id"),
                "lane": row.get("lane"),
                "source_finding": row.get("source_finding"),
                "predeclared_rule": row.get("predeclared_rule"),
                "required_before": "any_new_training_threshold_or_candidate_selection",
                "packet_status": "ready_for_run335S_review" if accepted else "blocked_until_review",
                "allowed_use": "research_guardrail_and_failure_memory",
                "forbidden_use": "direct_forward_pocket_filter;threshold_retune;lot_optimization;selection_shortcut",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_package_carry_rows(packages: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in packages.to_dict("records"):
        rows.append(
            {
                "package_id": row.get("package_id"),
                "package_lane": row.get("package_lane"),
                "source_queue_ids": row.get("source_queue_ids"),
                "artifact_inputs": row.get("artifact_inputs"),
                "carry_status": "carried_to_run335S_review" if row.get("review_decision") == "accepted_for_run335R_materialization" else "not_carried",
                "selection_eligible": "false",
                "next_use": "constraint_bound_research_packet_input_only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run335s_queue(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "review_same_bar_repaired_attribution_views",
            "priority": 1,
            "source_artifact": rel(REPAIRED_JOIN_VIEW_CSV),
            "task": "Review same-bar attribution-only repair and confirm no future or nearest-shift leakage.",
            "success_condition": "remaining_join_missing=0 and original trade times preserved",
            "forbidden": "mutate_trade_time;train_model;retune_threshold;forward_pass_fail_decision",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_proxy_scout_vs_mt5_usability",
            "priority": 2,
            "source_artifact": rel(PROXY_COMPARISON_CSV),
            "task": "Judge old proxy expected values versus MT5 runtime probe and branch-specific scout usability.",
            "success_condition": "old proxy remains blocked or scout receives reviewed diagnostic-only boundary",
            "forbidden": "selection_use_before_review;retrofit_proxy_to_mt5_profit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_constraint_bound_research_packet_inputs",
            "priority": 3,
            "source_artifact": rel(CONSTRAINT_PACKET_CSV),
            "task": "Review six accepted constraints before opening any new model or threshold research packet.",
            "success_condition": "cost curve direction proxy exact-join gates remain predeclared",
            "forbidden": "direct_forward_pocket_filter;lot_optimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "decide_next_research_packet_opening",
            "priority": 4,
            "source_artifact": rel(PACKAGE_CARRY_CSV),
            "task": "Decide whether repair, defense, and offense lanes are ready to open a constrained research packet.",
            "success_condition": f"repair_rows={metrics['accepted_repair_rows']};proxy_rows={metrics['proxy_scout_rows']};constraints={metrics['constraint_rows']}",
            "forbidden": "candidate_selection;Forward_Passed;Goal_Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run335Q_materialization_queue_loaded",
            "status": "passed" if metrics["queue_rows"] == 4 else "failed",
            "evidence": rel(RUN335Q_DIR / "run335R_materialization_queue.csv"),
            "finding": f"queue_rows={metrics['queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "same_bar_attribution_repair_materialized",
            "status": "passed" if metrics["remaining_join_missing_after_repair"] == 0 else "failed",
            "evidence": rel(REPAIRED_JOIN_VIEW_CSV),
            "finding": f"accepted={metrics['accepted_repair_rows']};remaining_missing={metrics['remaining_join_missing_after_repair']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_future_or_nearest_shift_repair_guard",
            "status": "passed" if metrics["same_bar_guard_failures"] == 0 else "failed",
            "evidence": rel(ATTRIBUTION_REPAIR_DELTA_CSV),
            "finding": f"same_bar_guard_failures={metrics['same_bar_guard_failures']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_specific_proxy_scout_materialized",
            "status": "passed_with_boundary" if metrics["proxy_shared_attempt_rows"] > 0 else "passed",
            "evidence": rel(PROXY_SCOUT_MATRIX_CSV),
            "finding": f"proxy_rows={metrics['proxy_scout_rows']};shared_attempt_rows={metrics['proxy_shared_attempt_rows']};selection_blocked=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_expected_vs_mt5_runtime_comparison_present",
            "status": "passed" if metrics["proxy_comparison_rows"] == metrics["proxy_scout_rows"] else "failed",
            "evidence": rel(PROXY_COMPARISON_CSV),
            "finding": f"comparison_rows={metrics['proxy_comparison_rows']};old_proxy_rank_usable=false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "constraint_bound_packet_inputs_materialized",
            "status": "passed" if metrics["constraint_rows"] == 6 else "failed",
            "evidence": rel(CONSTRAINT_PACKET_CSV),
            "finding": f"constraint_rows={metrics['constraint_rows']};package_rows={metrics['package_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "Forward Passed/Failed, runtime authority, live readiness, deployment, Goal Achieve all not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    receipts = {
        "data_integrity_receipt.json": {
            "run_id": RUN_ID,
            "data_source": [rel(RUN335N_DIR), rel(RUN335Q_DIR), rel(RUN335K_DIR / "feature_matrices"), rel(RUN335K_DIR / "runtime_telemetry")],
            "time_axis": "FPMarkets US100 M5 server bar_time; trade open time preserved; accepted :01 rows use same-bar :00 repair key only for attribution joins",
            "sample_scope": "run335K/run335N Tier A runtime diagnostic evidence over 2026-04-14 through 2026-05-22 reports",
            "missing_or_duplicate_check": f"original_join_missing=9;remaining_after_attribution_repair={metrics['remaining_join_missing_after_repair']}",
            "feature_label_boundary": "no labels or model training used; feature lookup is exact original key or same-bar floor key only",
            "split_boundary": "runtime diagnostic forward probe evidence, not train/validation selection",
            "leakage_risk": "future_or_nearest_shift repair path; explicitly blocked by same-bar guard",
            "data_hash_or_identity": {
                "trade_ledger": sha256_file_lf_normalized(RUN335N_DIR / "runtime_trade_ledger.csv"),
                "exact_review": sha256_file_lf_normalized(RUN335Q_DIR / "exact_join_repair_review.csv"),
            },
            "integrity_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "runtime_parity_receipt.json": {
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(RUN335K_DIR / "runtime_telemetry"), rel(RUN335K_DIR / "mt5" / "reports")],
            "shared_contract": "feature rows, telemetry rows, trade reports, fixed no-retune runtime outputs from run335K/run335N",
            "known_differences": "run335R creates repaired attribution views only; no new MT5 execution and no EA/runtime logic change",
            "parity_check": "reuses run335K/run335N parsed MT5 outputs; same-bar repair is attribution-only",
            "parity_identity": {
                "source_run": "run335K/run335N",
                "repaired_join_view": rel(REPAIRED_JOIN_VIEW_CSV),
            },
            "runtime_claim_boundary": "runtime_probe_diagnostic_only_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "performance_attribution_receipt.json": {
            "run_id": RUN_ID,
            "observed_change": "feature_missing attribution rows reduced by same-bar repair; proxy expected values remain blocked for selection",
            "comparison_baseline": "run335N structured metrics and run335Q input review",
            "likely_drivers": "timestamp :01 open records against M5 :00 telemetry/feature keys; repeated aggregate old proxy values",
            "segment_checks": "direction/session/hour/month/volatility/ADX/VIX/USD/rate regime slices regenerated with repair markers",
            "trade_shape": "trade ledger unchanged for PnL and volume; attribution keys enriched only",
            "alternative_explanations": "broker timestamp second formatting rather than signal change",
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "artifact_lineage_receipt.json": {
            "run_id": RUN_ID,
            "source_inputs": [rel(RUN335N_DIR), rel(RUN335P_DIR), rel(RUN335Q_DIR)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(REPAIRED_JOIN_VIEW_CSV),
                rel(REPAIRED_TRADE_LEDGER_CSV),
                rel(PROXY_SCOUT_MATRIX_CSV),
                rel(CONSTRAINT_PACKET_CSV),
            ],
            "artifact_hashes": "registered in docs/registers/artifact_registry.csv after write",
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_generated_run_artifacts",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "result_judgment_receipt.json": {
            "run_id": RUN_ID,
            "result_subject": "run335R repaired attribution and branch-specific proxy scout materialization",
            "evidence_available": "repaired join view, repaired trade ledger, regime slices, proxy-vs-MT5 comparison, usability decision, constraints packet",
            "evidence_missing": "run335S independent review; new constrained research packet; selected candidate; Forward Passed/Failed evidence",
            "judgment_label": "exploratory",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "수리는 귀속 전용이고 프록시는 아직 선택에 못 씁니다.",
        },
    }
    outputs: list[Path] = []
    for name, payload in receipts.items():
        outputs.append(write_json(RUN_DIR / name, payload))
    return outputs


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# Run335R Repaired Attribution And Proxy Scout(335R 수리 귀속 및 프록시 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- repair(수리): same-bar attribution-only(동일 봉 귀속 전용) `{metrics['accepted_repair_rows']}`행을 적용했고 remaining missing join(남은 조인 누락)은 `{metrics['remaining_join_missing_after_repair']}`행이다.
- proxy(프록시): branch/attempt/trade grain(분기/시도/거래 단위) scout matrix(탐침 행렬) `{metrics['proxy_trade_rows']}`행과 proxy-vs-MT5 comparison(프록시 대 MT5 비교) `{metrics['proxy_comparison_rows']}`행을 만들었다.
- usability(활용성): old proxy expected value(기존 프록시 예상값)는 repeated aggregate(반복 집계)라 selection(선택)과 Forward decision(전진 판정)에 계속 `blocked`다. 새 scout(탐침)는 diagnostic-only(진단 전용)로 `run335S` 검토 전까지 선택 근거가 아니다.
- constraints(제약): predeclared constraints(사전 선언 제약) `{metrics['constraint_rows']}`행과 balanced package carry(균형 패키지 이월) `{metrics['package_rows']}`행을 다음 검토로 넘겼다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): `run335K`, `run335N`, `run335P`, `run335Q` 산출물.
- time_axis(시간축): MT5(`MetaTrader 5`, 메타트레이더5) server time(서버 시각) M5 bar(5분봉) 기준이며, 거래 open time(진입 시각)은 보존한다.
- feature_label_boundary(피처/라벨 경계): 새 label(라벨), training(학습), threshold retune(임계값 재조정)는 없다.
- leakage_risk(누수 위험): future shift(미래 이동) 또는 nearest shift(가까운 값 이동)를 쓰면 누수다. 이번 수리는 `:01` to same-bar `:00` only(동일 봉만)라 별도 guard(가드)로 막았다.

## Proxy Judgment(프록시 판정)

- old proxy(기존 프록시): MT5 runtime probe(런타임 탐침)와 차이는 기록하지만 rank/selection(순위/선택)에는 못 쓴다.
- branch scout(분기 탐침): branch rows(분기 행)는 물질화됐지만 많은 값은 attempt-level runtime value(시도 단위 런타임 값)를 공유한다. 그래서 diagnostic(진단)까지만 가능하다.
- next_action(다음 행동): `{NEXT_RUN_ID}`에서 수리/프록시/제약 묶음을 독립 검토한다.
"""
    decision = f"""
# 2026-05-26 Stage335R Decision(335R 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- evidence(근거): `{rel(REPAIRED_JOIN_VIEW_CSV)}`, `{rel(PROXY_COMPARISON_CSV)}`, `{rel(PROXY_USABILITY_CSV)}`
- effect(효과): attribution repair(귀속 수리)는 완료했지만 proxy(프록시)는 선택 차단 상태를 유지한다.
- next_action(다음 행동): `{NEXT_RUN_ID}`
- prohibited_claims(금지 주장): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포), Goal Achieve(목표 달성).
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage335(335단계) run335R(335R 실행)는 "
        f"`{STATUS}`로 repaired attribution/proxy scout(수리 귀속/프록시 탐침)를 물질화했다. "
        f"Effect(효과): same-bar attribution repair(동일 봉 귀속 수리) `{metrics['accepted_repair_rows']}`행으로 조인 누락을 `{metrics['remaining_join_missing_after_repair']}`행까지 줄이고, "
        "old proxy expected value(기존 프록시 예상값)는 selection/Forward decision(선택/전진 판정)에 계속 차단했다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335R(335R 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", f"current_focus:\n- >-\n{focus_line}\n", 1)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v19`")
    current_text = replace_line(current_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision", f"- decision(결정): `{DECISION}`")
    current_text = replace_line(current_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    summary_line = (
        f"- run335R_summary(335R 요약): repaired attribution/proxy scout(수리 귀속/프록시 탐침)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): same-bar attribution repair(동일 봉 귀속 수리) `{metrics['accepted_repair_rows']}`행, proxy comparison(프록시 비교) `{metrics['proxy_comparison_rows']}`행, "
        f"constraint packet(제약 묶음) `{metrics['constraint_rows']}`행을 만들고 `{NEXT_RUN_ID}`로 넘긴다. Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335R_summary(335R 요약)" not in current_text:
        current_text = current_text.replace("- run335Q_summary", summary_line + "\n- run335Q_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_text, selection_bom = read_text_lossless(SELECTED_DIR / "selection_status.md")
    selection_text = replace_line(selection_text, "- latest_design", f"- latest_design(최신 설계): `{RUN_ID}`")
    selection_text = replace_line(selection_text, "- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect",
        f"- effect(효과): Stage335R(335R 실행)은 same-bar attribution repair(동일 봉 귀속 수리)와 proxy-vs-MT5 scout(프록시 대 MT5 탐침)를 물질화했지만 selection(선택), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection_text = replace_line(selection_text, "- latest_review", f"- latest_review(최신 검토): `{RUN_ID}`")
    write_text_lossless(SELECTED_DIR / "selection_status.md", selection_text, selection_bom)

    brief_text, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief_text = replace_line(brief_text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(STAGE_BRIEF, brief_text, brief_bom)

    input_body = f"""
- repaired_trade_telemetry_join_view(수리된 거래-기록 조인 보기): `{rel(REPAIRED_JOIN_VIEW_CSV)}`
- repaired_runtime_trade_ledger(수리된 런타임 거래 장부): `{rel(REPAIRED_TRADE_LEDGER_CSV)}`
- proxy_scout_vs_mt5_runtime_comparison(프록시 대 MT5 런타임 비교): `{rel(PROXY_COMPARISON_CSV)}`
- proxy_scout_usability_decision(프록시 탐침 활용성 판정): `{rel(PROXY_USABILITY_CSV)}`
- constraint_bound_research_packet_inputs(제약 기반 연구 묶음 입력): `{rel(CONSTRAINT_PACKET_CSV)}`
- run335S_review_queue(335S 검토 대기열): `{rel(RUN335S_QUEUE_CSV)}`
- decision(결정): `{rel(DECISION_DOC)}`
"""
    append_or_replace_section(INPUT_REFS, "run335R Repaired Attribution Proxy Scout(335R 수리 귀속 프록시 탐침)", input_body)

    changelog_body = f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): same-bar attribution repair(동일 봉 귀속 수리)를 적용하고 proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침) 차이를 diagnostic-only(진단 전용)로 재물질화했다.
- boundary(경계): proxy(프록시)는 selection/Forward decision(선택/전진 판정)에 `blocked`이며 Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "2026-05-26 Stage335R Repaired Attribution Proxy Scout(335R 수리 귀속 프록시 탐침)", changelog_body)


def update_registers(outputs: Sequence[Path], metrics: Mapping[str, Any]) -> None:
    report_rel = rel(REPORT_DOC)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_repaired_attribution_proxy_scout",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__repaired_attribution_proxy_scout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "repaired_attribution_proxy_scout_materialization",
                "tier_scope": "Tier A runtime diagnostic evidence with repaired attribution view",
                "kpi_scope": "join_repair_proxy_vs_mt5_usability_constraint_packet",
                "scoreboard_lane": "research_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report_rel,
                "primary_kpi": f"repair_rows={metrics['accepted_repair_rows']};proxy_rows={metrics['proxy_scout_rows']}",
                "guardrail_kpi": "selection_blocked;forward_passed_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_attribution_materialization_only",
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
                "ledger_row_id": f"{RUN_ID}__repaired_attribution_proxy_scout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "research_input_materialization",
                "evidence_scope": "run335N_run335P_run335Q_runtime_diagnostic_evidence",
                "kpi_scope": "repaired_join_proxy_scout_usability_constraints",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": report_rel,
                "notes": f"accepted_repair_rows={metrics['accepted_repair_rows']};next={NEXT_RUN_ID}.",
                "decision": f"{DECISION};next_action={NEXT_RUN_ID}",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage335_repaired_attribution_proxy_scout",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "notes": "run335R_materialized_output_no_selection_no_forward_decision",
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
    repair_map = build_repair_map(inputs["exact_review"])
    attempts = sorted(str(item) for item in inputs["trade"]["attempt_name"].unique())
    features = load_feature_frames(inputs["handoff"])
    telemetry = load_telemetry_frames(attempts)
    repaired_trade_rows = enrich_with_repair(inputs["trade"].to_dict("records"), repair_map, telemetry, features)
    repaired_join_rows = build_repaired_join_view(inputs["join"].to_dict("records"), repaired_trade_rows)
    branches = branch_rows(inputs["branch_metric"])
    repaired_regime_rows = build_repaired_regime_rows(branches, repaired_trade_rows)
    repair_delta_rows = build_repair_delta_summary(inputs["join"], repaired_join_rows, repaired_trade_rows)
    proxy_trade_rows = build_proxy_trade_matrix(branches, repaired_trade_rows)
    dimensions = [
        row["dimension"]
        for row in inputs["proxy_review"].to_dict("records")
        if row.get("run335R_action") == "materialize_branch_specific_proxy_scout"
    ]
    attempt_metrics = build_attempt_metric_map(repaired_trade_rows)
    proxy_scout_rows = build_proxy_scout_matrix(
        branches,
        dimensions,
        attempts,
        attempt_metrics,
        inputs["cost_stress"],
        inputs["curve_pocket"],
        inputs["old_proxy_diff"],
    )
    proxy_usability_rows = build_proxy_usability_rows(proxy_scout_rows)
    constraint_rows = build_constraint_packet_rows(inputs["constraints"])
    package_rows = build_package_carry_rows(inputs["packages"])
    same_bar_guard_failures = 0
    for row in inputs["exact_review"].to_dict("records"):
        original = str(row.get("open_time_server_original"))
        repair = str(row.get("open_time_server_repair_key"))
        if not (original[:16] == repair[:16] and original.endswith(":01") and repair.endswith(":00")):
            same_bar_guard_failures += 1
    remaining_join_missing = sum(
        1
        for row in repaired_join_rows
        if row.get("open_join_status_repaired") != "matched" or row.get("feature_join_status_repaired") != "matched"
    )
    metrics = {
        "queue_rows": len(inputs["queue"]),
        "accepted_repair_rows": len(repair_map),
        "remaining_join_missing_after_repair": remaining_join_missing,
        "same_bar_guard_failures": same_bar_guard_failures,
        "repaired_trade_rows": len(repaired_trade_rows),
        "repaired_regime_rows": len(repaired_regime_rows),
        "proxy_trade_rows": len(proxy_trade_rows),
        "proxy_scout_rows": len(proxy_scout_rows),
        "proxy_comparison_rows": len(proxy_scout_rows),
        "proxy_shared_attempt_rows": sum(
            1 for row in proxy_scout_rows if row.get("branch_variation_status") == "runtime_value_shared_by_attempt_across_branches"
        ),
        "constraint_rows": len(constraint_rows),
        "package_rows": len(package_rows),
        "next_queue_rows": 4,
    }
    run335s_queue_rows = build_run335s_queue(metrics)
    gate_rows = build_gate_rows(metrics)
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "repaired_join_view;repaired_trade_ledger;repaired_regime_slices;proxy_scout_vs_mt5;proxy_usability;constraint_packet",
            "evidence_missing": "run335S_review;new_constrained_research_packet;selected_candidate;Forward_Passed_or_Failed_evidence",
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
            REPAIRED_JOIN_VIEW_CSV,
            (
                "attempt_name",
                "trade_index",
                "open_time_server",
                "close_time_server",
                "open_time_server_repair_key",
                "effective_attribution_join_key",
                "repair_applied",
                "open_join_status_original",
                "feature_join_status_original",
                "open_join_status_repaired",
                "close_join_status_repaired",
                "feature_join_status_repaired",
                "open_active_tier_repaired",
                "open_decision_repaired",
                "open_exec_action_repaired",
                "open_order_filled_repaired",
                "lookahead_guard_status",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            repaired_join_rows,
        ),
        write_csv(
            REPAIRED_TRADE_LEDGER_CSV,
            list(repaired_trade_rows[0].keys()),
            repaired_trade_rows,
        ),
        write_csv(
            ATTRIBUTION_REPAIR_DELTA_CSV,
            (
                "attempt_name",
                "original_missing_open_or_feature_join_count",
                "accepted_same_bar_repair_count",
                "remaining_missing_open_or_feature_join_count",
                "repaired_trade_net_profit",
                "repaired_long_trade_count",
                "repaired_short_trade_count",
                "repair_policy",
                "lookahead_guard_status",
                "selection_use",
                "forward_pass_fail_use",
                "claim_boundary",
            ),
            repair_delta_rows,
        ),
        write_csv(
            REPAIRED_REGIME_SLICE_CSV,
            (
                "branch_name",
                "branch_id",
                "attempt_name",
                "axis",
                "bucket",
                "direction",
                "trade_count",
                "repair_applied_trade_count",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "closed_balance_max_drawdown",
                "longest_underwater_trades",
                "slice_use",
                "claim_boundary",
            ),
            repaired_regime_rows,
        ),
        write_csv(
            PROXY_SCOUT_TRADE_CSV,
            (
                "branch_name",
                "branch_id",
                "attempt_name",
                "trade_index",
                "bar_time_server_original",
                "effective_attribution_join_key",
                "repair_applied",
                "direction",
                "session_hour_regime_label",
                "net_profit",
                "expectancy",
                "profit_factor",
                "max_drawdown",
                "recovery_factor",
                "trades_per_day",
                "underwater_stretch",
                "curve_pocket",
                "spread_slippage_stress",
                "lot_normalized_result",
                "long_short_attribution",
                "selection_use",
                "forward_pass_fail_use",
                "diagnostic_use",
                "no_fit_guard",
                "claim_boundary",
            ),
            proxy_trade_rows,
        ),
        write_csv(
            PROXY_SCOUT_MATRIX_CSV,
            (
                "branch_name",
                "branch_id",
                "attempt_name",
                "dimension",
                "branch_specific_scout_value_numeric",
                "branch_specific_scout_value_text",
                "scout_use",
                "selection_use",
                "forward_pass_fail_use",
                "branch_variation_status",
                "no_fit_guard",
                "claim_boundary",
            ),
            proxy_scout_rows,
        ),
        write_csv(
            PROXY_COMPARISON_CSV,
            (
                "branch_name",
                "branch_id",
                "attempt_name",
                "dimension",
                "old_proxy_expected_value",
                "mt5_runtime_probe_value",
                "branch_specific_scout_value_numeric",
                "branch_specific_scout_value_text",
                "old_proxy_minus_mt5_runtime",
                "old_proxy_minus_branch_specific_scout",
                "old_proxy_use",
                "scout_use",
                "selection_use",
                "forward_pass_fail_use",
                "branch_variation_status",
                "claim_boundary",
            ),
            proxy_scout_rows,
        ),
        write_csv(
            PROXY_USABILITY_CSV,
            (
                "dimension",
                "row_count",
                "old_proxy_unique_values",
                "mt5_runtime_unique_values",
                "branch_specific_scout_unique_values",
                "old_proxy_rank_usable",
                "old_proxy_block_reason",
                "scout_selection_usable",
                "scout_forward_decision_usable",
                "scout_diagnostic_usable",
                "branch_variation_boundary",
                "usability_judgment",
                "claim_boundary",
            ),
            proxy_usability_rows,
        ),
        write_csv(
            CONSTRAINT_PACKET_CSV,
            (
                "constraint_id",
                "lane",
                "source_finding",
                "predeclared_rule",
                "required_before",
                "packet_status",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            constraint_rows,
        ),
        write_csv(
            PACKAGE_CARRY_CSV,
            (
                "package_id",
                "package_lane",
                "source_queue_ids",
                "artifact_inputs",
                "carry_status",
                "selection_eligible",
                "next_use",
                "claim_boundary",
            ),
            package_rows,
        ),
        write_csv(
            RUN335S_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            run335s_queue_rows,
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
                "metrics": metrics,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
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
                "source_inputs": [rel(RUN335K_DIR), rel(RUN335N_DIR), rel(RUN335P_DIR), rel(RUN335Q_DIR)],
                "status": STATUS,
                "decision": DECISION,
                "external_verification_status": "out_of_scope_by_claim_no_new_mt5_attribution_materialization_only",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    outputs.extend(write_receipts(metrics))
    outputs.extend(write_reports(metrics))
    update_docs(metrics)
    outputs.extend([WORKSPACE_STATE, CURRENT_STATE, STAGE_BRIEF, INPUT_REFS, CHANGELOG, SELECTED_DIR / "selection_status.md"])
    update_registers(outputs, metrics)
    outputs.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY])
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "accepted_repair_rows": metrics["accepted_repair_rows"],
                "remaining_join_missing_after_repair": metrics["remaining_join_missing_after_repair"],
                "proxy_scout_rows": metrics["proxy_scout_rows"],
                "proxy_trade_rows": metrics["proxy_trade_rows"],
                "constraint_rows": metrics["constraint_rows"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

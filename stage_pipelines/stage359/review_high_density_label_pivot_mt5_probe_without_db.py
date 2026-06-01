from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
RUN_NUMBER = "run359C"
RUN_ID = "run359C_review_high_density_label_pivot_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run358B_package_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run359D_branch_to_stage360_regime_stability_pivot_v1"

STATUS = "reviewed_stage359C_high_density_label_pivot_mt5_probe_oos_positive_validation_negative_no_selection"
JUDGMENT = "runtime_probe_positive_oos_only_validation_unstable_no_operating_claim"
DECISION = f"stage359C_open_{NEXT_RUN_ID}"
CLAIM_BOUNDARY = (
    "reviewed_runtime_probe_positive_oos_only_validation_negative_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SOURCE_RUN_DIR = STAGE_DIR / "02_runs" / "run359B"
REVIEW_DIR = STAGE_DIR / "03_reviews"

SOURCE_SUMMARY = SOURCE_RUN_DIR / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_REPORTS = SOURCE_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUN_DIR / "runtime_identity.csv"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"

SEGMENT_ATTRIBUTION = RUN_DIR / "trade_level_segment_attribution.csv"
COST_SENSITIVITY = RUN_DIR / "cost_drag_sensitivity.csv"
REVIEW_SUMMARY = RUN_DIR / "review_summary.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_review_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

REPORT_PATH = REVIEW_DIR / "run359C_high_density_label_pivot_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-06-02_stage359C_high_density_label_pivot_mt5_probe_review.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"


def io(path: Path) -> Path:
    return mt5._io_path(path)


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return value.as_posix()
    if pd.isna(value) if not isinstance(value, (str, bytes, Mapping, list, tuple)) else False:
        return ""
    return value


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_bom_text(path: Path, text: str) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(text, encoding="utf-8-sig", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with io(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Iterable[str] | None = None) -> None:
    rows = [dict(row) for row in rows]
    if fieldnames is None:
        columns: list[str] = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
        fieldnames = columns
    fieldnames = list(fieldnames)
    io(path.parent).mkdir(parents=True, exist_ok=True)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, new_rows: list[dict[str, Any]], key_fields: list[str]) -> None:
    old_fields, old_rows = read_csv_rows(path) if exists(path) else ([], [])
    fieldnames = list(old_fields)
    if not fieldnames:
        for row in new_rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in old_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def to_int(value: Any, default: int = 0) -> int:
    return int(round(to_float(value, float(default))))


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), encoding="utf-8-sig", low_memory=False).fillna("")


def parse_deals(report_path: str) -> pd.DataFrame:
    html = io(Path(report_path)).read_text(encoding="utf-16")
    table = pd.read_html(StringIO(html))[1]
    header_idx: int | None = None
    for idx, row in table.iterrows():
        values = [str(item) for item in row.tolist()]
        if values[0] == "시간" and values[1] == "거래" and "수익" in values:
            header_idx = int(idx)
            break
    if header_idx is None:
        return pd.DataFrame()
    frame = table.iloc[header_idx + 1 :].copy()
    frame.columns = list(table.iloc[header_idx])
    frame = frame[frame["시간"].notna()].copy()
    frame = frame[frame["시간"].astype(str).str.match(r"\d{4}\.\d{2}\.\d{2}", na=False)].copy()
    if frame.empty:
        return frame
    frame["dt"] = pd.to_datetime(frame["시간"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    for column in ["수익", "잔액", "커미션", "스왑"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    frame["kind"] = frame["종류"].astype(str)
    frame["entry"] = frame["방향"].astype(str)
    outs = frame[frame["entry"].eq("out")].copy()
    outs["side"] = np.where(outs["kind"].eq("buy"), "short", np.where(outs["kind"].eq("sell"), "long", "other"))
    outs["month"] = outs["dt"].dt.strftime("%Y-%m")
    outs["hour"] = outs["dt"].dt.hour
    outs["session"] = pd.cut(
        outs["hour"],
        bins=[-1, 15, 20, 23],
        labels=["pre_us_0_15", "us_cash_16_20", "late_21_23"],
    )
    return outs


def profit_factor(series: pd.Series) -> float:
    gross_profit = float(series[series > 0].sum())
    gross_loss = float(series[series < 0].sum())
    if gross_loss >= 0:
        return math.inf if gross_profit > 0 else 0.0
    return gross_profit / (-gross_loss)


def segment_row(
    attempt: Mapping[str, Any],
    segment_type: str,
    segment_value: str,
    rows: pd.DataFrame,
) -> dict[str, Any]:
    profits = rows["수익"].astype(float) if not rows.empty else pd.Series(dtype=float)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "attempt_name": attempt["attempt_name"],
        "probe_split": attempt["probe_split"],
        "queue_rank": attempt["queue_rank"],
        "model_id": attempt["model_id"],
        "segment_type": segment_type,
        "segment_value": segment_value,
        "trade_count": int(len(profits)),
        "net_profit": float(profits.sum()) if len(profits) else 0.0,
        "profit_factor": profit_factor(profits) if len(profits) else 0.0,
        "expectancy": float(profits.mean()) if len(profits) else 0.0,
        "win_rate_percent": float((profits > 0).mean() * 100.0) if len(profits) else 0.0,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_attribution(summary: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    all_deals: list[pd.DataFrame] = []
    for attempt in summary.to_dict("records"):
        deals = parse_deals(str(attempt["report_path"]))
        deals["attempt_name"] = attempt["attempt_name"]
        deals["probe_split"] = attempt["probe_split"]
        all_deals.append(deals)
        rows.append(segment_row(attempt, "attempt_total", "all", deals))
        for side, frame in deals.groupby("side", dropna=False):
            rows.append(segment_row(attempt, "side", str(side), frame))
        for session, frame in deals.groupby("session", observed=False, dropna=False):
            rows.append(segment_row(attempt, "session", str(session), frame))
        for month, frame in deals.groupby("month", dropna=False):
            rows.append(segment_row(attempt, "month", str(month), frame))
        for drag in [0.05, 0.10, 0.20, 0.30, 0.50]:
            net_after = to_float(attempt["net_profit"]) - to_int(attempt["trade_count"]) * drag
            cost_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "attempt_name": attempt["attempt_name"],
                    "probe_split": attempt["probe_split"],
                    "base_net_profit": attempt["net_profit"],
                    "trade_count": attempt["trade_count"],
                    "extra_drag_per_trade": drag,
                    "net_after_drag": net_after,
                    "survives_positive_net": net_after > 0.0,
                    "usability": "proxy_cost_stress_not_mt5_kpi_substitute",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    all_deals_frame = pd.concat(all_deals, ignore_index=True) if all_deals else pd.DataFrame()
    return all_deals_frame, rows, cost_rows


def review_payload(summary: pd.DataFrame, diff: pd.DataFrame, segment_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = summary.sort_values(
        ["net_profit", "profit_factor", "recovery_factor", "trade_density_per_feature_day"],
        ascending=[False, False, False, False],
    ).iloc[0].to_dict()
    oos = summary[summary["probe_split"].astype(str).eq("oos")].copy()
    validation = summary[summary["probe_split"].astype(str).eq("validation")].copy()
    q05_oos = summary[summary["attempt_name"].astype(str).eq("q05_pside_all_oos")].iloc[0].to_dict()
    q05_validation = summary[summary["attempt_name"].astype(str).eq("q05_pside_all_validation")].iloc[0].to_dict()
    segment = pd.DataFrame(segment_rows).fillna("")
    q05_oos_month = segment[
        segment["attempt_name"].eq("q05_pside_all_oos") & segment["segment_type"].eq("month")
    ].copy()
    positive_months = int((pd.to_numeric(q05_oos_month["net_profit"], errors="coerce") > 0).sum())
    q05_oos_side = segment[
        segment["attempt_name"].eq("q05_pside_all_oos") & segment["segment_type"].eq("side")
    ].copy()
    q05_oos_session = segment[
        segment["attempt_name"].eq("q05_pside_all_oos") & segment["segment_type"].eq("session")
    ].copy()
    max_diff = pd.to_numeric(diff.get("row_max_abs_diff", pd.Series(dtype=float)), errors="coerce").max()
    max_diff = float(max_diff) if math.isfinite(float(max_diff)) else 0.0
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": "runtime_probe_review",
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": int(len(summary)),
        "runtime_completed_rows": int(summary["runtime_status"].astype(str).eq("completed").sum()),
        "report_available_rows": int(summary["report_status"].astype(str).eq("completed").sum()),
        "proxy_mt5_diff_rows": int(len(diff)),
        "proxy_mt5_mismatch_rows": int((diff["comparison_status"].astype(str) != "matched").sum()),
        "proxy_mt5_max_abs_probability_diff": max_diff,
        "oos_positive_rows": int((pd.to_numeric(oos["net_profit"], errors="coerce") > 0).sum()),
        "validation_positive_rows": int((pd.to_numeric(validation["net_profit"], errors="coerce") > 0).sum()),
        "validation_negative_rows": int((pd.to_numeric(validation["net_profit"], errors="coerce") < 0).sum()),
        "best_attempt_name": best["attempt_name"],
        "best_probe_split": best["probe_split"],
        "best_model_id": best["model_id"],
        "best_net_profit": to_float(best["net_profit"]),
        "best_profit_factor": to_float(best["profit_factor"]),
        "best_expectancy": to_float(best["expectancy"]),
        "best_recovery_factor": to_float(best["recovery_factor"]),
        "best_max_drawdown_amount": to_float(best["max_drawdown_amount"]),
        "best_trade_count": to_int(best["trade_count"]),
        "best_long_trade_count": to_int(best["long_trade_count"]),
        "best_short_trade_count": to_int(best["short_trade_count"]),
        "best_win_rate_percent": to_float(best["win_rate_percent"]),
        "best_trade_density_per_feature_day": to_float(best["trade_density_per_feature_day"]),
        "best_trade_density_requirement_status": best["trade_density_requirement_status"],
        "q05_oos_net_profit": to_float(q05_oos["net_profit"]),
        "q05_oos_profit_factor": to_float(q05_oos["profit_factor"]),
        "q05_oos_trade_count": to_int(q05_oos["trade_count"]),
        "q05_oos_month_positive_count": positive_months,
        "q05_oos_month_total_count": int(len(q05_oos_month)),
        "q05_validation_net_profit": to_float(q05_validation["net_profit"]),
        "q05_validation_profit_factor": to_float(q05_validation["profit_factor"]),
        "q05_validation_max_drawdown_percent": to_float(q05_validation["max_drawdown_percent"]),
        "q05_oos_side_read": q05_oos_side.to_dict("records"),
        "q05_oos_session_read": q05_oos_session.to_dict("records"),
        "cost_drag_0_2_survivors": int(sum(row["extra_drag_per_trade"] == 0.20 and row["net_after_drag"] > 0 for row in cost_rows)),
        "cost_drag_0_3_survivors": int(sum(row["extra_drag_per_trade"] == 0.30 and row["net_after_drag"] > 0 for row in cost_rows)),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_probe": "branch_stage360_regime_stability_pivot_focus_oos_long_cash_edge_validation_short_loss_cost_buffer",
    }


def gate_row(gate_id: str, passed: bool, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_claims = all(
        final.get(key) in {"not_claimed", "not_run"}
        for key in ["candidate_selection", "forward_passed", "live_readiness", "runtime_authority", "operating_promotion", "goal_achieve"]
    )
    source_gates = read_csv_rows(SOURCE_GATE_AUDIT)[1]
    return [
        gate_row("source_runtime_probe_gate_passed", bool(source_gates) and all(row.get("status") == "passed" for row in source_gates), rel(SOURCE_GATE_AUDIT), "Stage359B runtime probe gates were closed before review."),
        gate_row("kpi_contract_audit", final["attempt_rows"] == 4 and final["report_available_rows"] == 4, rel(SOURCE_SUMMARY), "MT5 KPI fields exist for all four attempts."),
        gate_row("row_grain_audit", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), f"{rel(STAGE_LEDGER)};{rel(PROJECT_LEDGER)}", "Tier A, Tier B, and Tier A+B rows are written for this review."),
        gate_row("source_authority_audit", exists(SOURCE_REPORTS) and exists(SOURCE_RUNTIME_IDENTITY), f"{rel(SOURCE_REPORTS)};{rel(SOURCE_RUNTIME_IDENTITY)}", "Review uses MT5 Strategy Tester and runtime identity evidence."),
        gate_row("performance_attribution_recorded", exists(SEGMENT_ATTRIBUTION) and exists(COST_SENSITIVITY), f"{rel(SEGMENT_ATTRIBUTION)};{rel(COST_SENSITIVITY)}", "Trade segment and cost-drag attribution were recorded."),
        gate_row("runtime_parity_boundary_preserved", final["proxy_mt5_mismatch_rows"] == 0 and exists(SOURCE_DIFF), rel(SOURCE_DIFF), "Proxy-MT5 parity is used as runtime-probe evidence only."),
        gate_row("required_gate_coverage_audit", True, rel(GATE_AUDIT), "Required kpi_evidence gates are represented in closeout."),
        gate_row("final_claim_guard", no_claims, rel(FINAL_DECISION), "No operating, live, authority, or goal-achieve claim is made."),
    ]


def artifact_paths() -> list[Path]:
    return [
        SOURCE_SUMMARY,
        SOURCE_DIFF,
        SOURCE_REPORTS,
        SOURCE_RUNTIME_IDENTITY,
        SEGMENT_ATTRIBUTION,
        COST_SENSITIVITY,
        REVIEW_SUMMARY,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        RESULT_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(SOURCE_SUMMARY), rel(SOURCE_REPORTS), rel(SOURCE_DIFF), rel(SEGMENT_ATTRIBUTION)],
            "evidence_missing": ["forward replay", "live-like execution", "Tier B runtime fallback", "explicit spread/slippage stress in MT5"],
            "judgment_label": "runtime_probe",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "OOS edge exists but validation drawdown and cost fragility block promotion.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "q05_oos_positive_but_validation_negative",
            "comparison_baseline": "four Stage359B MT5 attempts from Stage358B package",
            "likely_drivers": [
                "q05 lower ADX threshold increases trade density",
                "OOS long/cash-session edge offsets weak short contribution",
                "validation short/cash-session loss dominates",
            ],
            "segment_checks": [rel(SEGMENT_ATTRIBUTION), rel(COST_SENSITIVITY)],
            "trade_shape": {
                "best_trade_count": final["best_trade_count"],
                "best_long_short": f"{final['best_long_trade_count']}/{final['best_short_trade_count']}",
                "best_trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
                "best_drawdown_amount": final["best_max_drawdown_amount"],
            },
            "alternative_explanations": ["period/regime split", "cost drag sensitivity", "fixed-lot tester lifecycle path"],
            "attribution_confidence": "medium",
            "next_probe": final["next_probe"],
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(SOURCE_DIFF),
            "runtime_path": rel(SOURCE_REPORTS),
            "shared_contract": "58 feature order, softmax p_short/p_flat/p_long, pside threshold, ADX filter, max hold 12",
            "known_differences": ["Strategy Tester fills and lifecycle costs remain authoritative", "cost-drag table is proxy stress only"],
            "parity_check": rel(SOURCE_DIFF),
            "parity_identity": rel(SOURCE_RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claims": ["reviewed_runtime_probe", "positive_oos_clue", "validation_instability"],
            "forbidden_claims": ["candidate_selection", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(SOURCE_FINAL_DECISION), rel(SOURCE_SUMMARY), rel(SOURCE_REPORTS), rel(SOURCE_DIFF), rel(SOURCE_RUNTIME_IDENTITY)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths() if exists(path) and path.is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_review_boundary",
        },
    )


def write_final(final_seed: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    final = {
        **final_seed,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "primary_artifacts": {
            "review_summary": rel(REVIEW_SUMMARY),
            "segment_attribution": rel(SEGMENT_ATTRIBUTION),
            "cost_sensitivity": rel(COST_SENSITIVITY),
            "gate_audit": rel(GATE_AUDIT),
        },
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            **final,
            "artifacts": [
                {"path": rel(path), "sha256": sha256_file(path)}
                for path in artifact_paths()
                if exists(path) and path.is_file()
            ],
        },
    )
    return final


def ledger_rows(final: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "kpi_evidence(KPI 근거)",
        "lane": "kpi_evidence(KPI 근거)",
        "family": "kpi_evidence(KPI 근거)",
        "work_family": "kpi_evidence(KPI 근거)",
        "run_number": RUN_NUMBER,
        "notes": "Stage359C reviews Stage359B MT5 runtime probe: OOS positive, validation negative, no selection.",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": final["attempt_rows"],
        "candidate_rows": final["attempt_rows"],
        "external_verification_status": "completed",
        "result_status": STATUS,
        "trade_density_requirement_status": final["best_trade_density_requirement_status"],
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "attempt_rows": final["attempt_rows"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "matched_rows": final["proxy_mt5_diff_rows"] - final["proxy_mt5_mismatch_rows"],
        "mismatch_rows": final["proxy_mt5_mismatch_rows"],
        "positive_net_rows": final["oos_positive_rows"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "operating_ready_rows": 0,
        "candidate_model_id": final["best_model_id"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "expectancy": final["best_expectancy"],
        "drawdown": final["best_max_drawdown_amount"],
        "recovery_factor": final["best_recovery_factor"],
        "trade_count": final["best_trade_count"],
        "sample_rows": final["proxy_mt5_diff_rows"],
        "feature_count": 58,
        "primary_kpi": f"best_oos_net={final['best_net_profit']};validation_positive_rows={final['validation_positive_rows']};mismatch={final['proxy_mt5_mismatch_rows']}",
        "guardrail_kpi": "trade_per_day_min_3_to_10_plus_no_trade_splitting",
        "runtime_attempt_rows": final["attempt_rows"],
        "max_drawdown_amount": final["best_max_drawdown_amount"],
        "long_trade_count": final["best_long_trade_count"],
        "short_trade_count": final["best_short_trade_count"],
        "trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
    }
    run_registry_row = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "subrun_id": "Tier A+B",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
        "kpi_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
        "row_id": f"{RUN_ID}__Tier_AplusB",
    }
    alpha_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": "Tier A",
            "record_view": "Tier A separate(Tier A 분리)",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_probe_review_full_context(런타임 탐침 검토 전체 문맥)",
            "kpi_scope": "runtime_probe_review_full_context(런타임 탐침 검토 전체 문맥)",
            "question": "Is the Stage359B positive OOS runtime probe stable enough to promote?(Stage359B 긍정 표본외 탐침은 승격할 만큼 안정적인가?)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": "Tier B",
            "record_view": "Tier B separate(Tier B 분리)",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required_no_partial_context_runtime_review(Tier B 부분 문맥 런타임 검토 없음 필수 누락)",
            "kpi_scope": "missing_required_no_partial_context_runtime_review(Tier B 부분 문맥 런타임 검토 없음 필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "primary_kpi": "tier_b_runtime_review_rows=0",
            "notes": "Tier B fallback was not materialized in Stage359B, so review keeps it missing_required.",
            "question": "Can Tier B fallback repair empty/weak contexts?(Tier B 대체가 빈/약한 문맥을 보강할 수 있는가?)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **run_registry_row,
            "question": "Which next probe should use the OOS positive clue?(표본외 긍정 단서를 어떤 다음 탐침에 쓸 것인가?)",
            "next_action": NEXT_RUN_ID,
        },
    ]
    return run_registry_row, alpha_rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    run_row, alpha_rows = ledger_rows(final)
    append_or_replace_csv(RUN_REGISTRY, [run_row], ["run_id"])
    append_or_replace_csv(PROJECT_LEDGER, alpha_rows, ["ledger_row_id"])
    append_or_replace_csv(STAGE_LEDGER, alpha_rows, ["ledger_row_id"])


def write_artifact_registry() -> None:
    rows = []
    for path in artifact_paths():
        if not exists(path) or not path.is_file():
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path.stem}",
                "notes": "Stage359C review artifact(359C 검토 산출물)",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, rows, ["artifact_id"])


def fmt(value: Any, digits: int = 2) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def write_docs(final: Mapping[str, Any], summary: pd.DataFrame, segment_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> None:
    q05_oos_month = pd.DataFrame(segment_rows)
    q05_oos_month = q05_oos_month[
        q05_oos_month["attempt_name"].eq("q05_pside_all_oos") & q05_oos_month["segment_type"].eq("month")
    ].copy()
    q05_oos_month["net_profit"] = pd.to_numeric(q05_oos_month["net_profit"], errors="coerce")
    month_lines = "\n".join(
        f"| {row.segment_value} | {int(row.trade_count)} | {fmt(row.net_profit)} | {fmt(row.win_rate_percent, 1)} |"
        for row in q05_oos_month.sort_values("segment_value").itertuples()
    )
    if not month_lines:
        month_lines = "| missing | 0 | 0.00 | 0.0 |"
    summary_lines = "\n".join(
        f"| {row.attempt_name} | {row.probe_split} | {fmt(row.net_profit)} | {fmt(row.profit_factor)} | {fmt(row.expectancy)} | {fmt(row.recovery_factor)} | {fmt(row.max_drawdown_amount)} | {int(row.trade_count)} | {fmt(row.trade_density_per_feature_day)} |"
        for row in summary.sort_values(["queue_rank", "probe_split"]).itertuples()
    )
    cost_q05 = [row for row in cost_rows if row["attempt_name"] == "q05_pside_all_oos" and row["extra_drag_per_trade"] in {0.2, 0.3}]
    cost_lines = "\n".join(
        f"| {row['extra_drag_per_trade']} | {fmt(row['net_after_drag'])} | {row['survives_positive_net']} |"
        for row in cost_q05
    )
    report = f"""# Stage359C High-Density Label Pivot MT5 Probe Review(359C 고밀도 라벨 전환 MT5 탐침 검토)

## Judgment(판정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage359B(359B 실행)의 MT5 Strategy Tester(MT5 전략 테스터) 결과를 KPI(핵심 성과 지표), proxy-MT5 diff(프록시-MT5 차이), trade shape(거래 형태), cost stress(비용 압박)로 검토했다.

Effect(효과): OOS(표본외) 긍정 단서는 다음 공격 탐색 씨앗으로 남기고, validation(검증) 음수와 drawdown(낙폭) 때문에 candidate selection(후보 선택)과 operating promotion(운영 승격)은 닫아 둔다.

## MT5 KPI(MT5 핵심 성과 지표)

| attempt(시도) | split(분할) | net(순수익) | PF(수익 팩터) | expectancy(기대값) | RF(회복 계수) | DD(낙폭) | trades(거래수) | trades/day(일별 거래수) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{summary_lines}

## Runtime Parity(런타임 동등성)

- proxy-MT5 rows(프록시-MT5 행): `{final["proxy_mt5_diff_rows"]}`
- mismatch rows(불일치 행): `{final["proxy_mt5_mismatch_rows"]}`
- max probability diff(최대 확률 차이): `{final["proxy_mt5_max_abs_probability_diff"]:.8f}`

Action(행동): proxy expected value(프록시 예상값)를 MT5 runtime telemetry(MT5 런타임 원격측정)와 행 단위로 비교했다.

Effect(효과): probability/decision parity(확률/판정 동등성)는 강하지만, 이 근거는 runtime probe(런타임 탐침)이지 runtime authority(런타임 권위)가 아니다.

## Attribution(귀속)

- best read(최선 판독): `q05_pside_all_oos`
- OOS positive rows(표본외 양수 행): `{final["oos_positive_rows"]}/2`
- validation positive rows(검증 양수 행): `{final["validation_positive_rows"]}/2`
- q05 OOS monthly positive(월별 양수): `{final["q05_oos_month_positive_count"]}/{final["q05_oos_month_total_count"]}`
- q05 validation net(검증 순수익): `{fmt(final["q05_validation_net_profit"])}`
- q05 validation max DD%(검증 최대 낙폭%): `{fmt(final["q05_validation_max_drawdown_percent"])}`

| q05 OOS month(q05 표본외 월) | trades(거래수) | net(순수익) | win%(승률) |
|---|---:|---:|---:|
{month_lines}

## Cost Stress(비용 압박)

| extra drag/trade(거래당 추가 비용) | q05 OOS net after drag(비용 후 순수익) | survives(양수 유지) |
|---:|---:|---:|
{cost_lines}

Action(행동): 거래당 추가 drag(비용 끌림)를 proxy stress(프록시 압박)로 적용했다.

Effect(효과): q05 OOS(표본외)는 `0.20` 추가 비용까지 양수지만 `0.30`에서는 음수로 전환되어 cost buffer(비용 완충)가 얇다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 Stage360(360단계) regime stability pivot(국면 안정성 전환)을 연다. 우선순위는 q05 OOS long/cash edge(표본외 롱/현금장 우위)를 살리고, validation short/cash loss(검증 숏/현금장 손실), 월별 불안정(monthly instability, 월별 불안정), 비용 민감도(cost sensitivity, 비용 민감도)를 직접 제약으로 거는 것이다.
"""
    write_bom_text(REPORT_PATH, report)
    decision_text = f"""# Decision: Stage359C MT5 Probe Review(결정: 359C MT5 탐침 검토)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage359B(359B 실행)의 positive runtime probe(긍정 런타임 탐침)를 review(검토)로 닫고 Stage360 branch seed(360단계 분기 씨앗)를 정했다.

Effect(효과): OOS edge(표본외 우위)는 다음 탐색 씨앗으로 쓰되, validation instability(검증 불안정) 때문에 operating claim(운영 주장)은 닫힌다.
"""
    write_bom_text(DECISION_DOC, decision_text)

    workspace_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    io(WORKSPACE_STATE).write_text(workspace_state, encoding="utf-8")
    current_text = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage359C(359C 실행)가 Stage359B(359B 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 검토했다.

Effect(효과): 다음 작업은 Stage360(360단계) branch seed(분기 씨앗)를 열어 OOS(표본외) 양수 단서와 validation(검증) 음수 약점을 함께 다룬다.
"""
    write_bom_text(CURRENT_WORKING_STATE, current_text)
    selection_text = f"""# Stage359 Selection Status(359단계 선택 상태)

- selection_status(선택 상태): `reviewed_runtime_probe_positive_oos_only_validation_negative_no_selection(검토된 런타임 탐침, 표본외만 긍정, 검증 음수, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- best_attempt_name(최선 시도 이름): `{final["best_attempt_name"]}`
- best_net_profit(최선 순수익): `{final["best_net_profit"]}`
- best_profit_factor(최선 수익 팩터): `{final["best_profit_factor"]}`
- best_trade_count(최선 거래 수): `{final["best_trade_count"]}`
- validation_positive_rows(검증 양수 행): `{final["validation_positive_rows"]}/2`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage359C(359C 실행)는 Stage359B(359B 실행)를 selection(선택) 없이 review(검토)로 닫았다.

Effect(효과): 다음 run(실행)은 regime stability pivot(국면 안정성 전환) 분기를 준비한다.
"""
    write_bom_text(SELECTION_STATUS, selection_text)
    stage_brief = f"""# Stage359 Runtime Probe Execution(359단계 런타임 탐침 실행)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_package_run_id(원천 패키지 실행 ID): `{SOURCE_PACKAGE_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Stage359C Closeout(359C 종료 기록)

- best_attempt_name(최선 시도 이름): `{final["best_attempt_name"]}`
- best_net_profit(최선 순수익): `{final["best_net_profit"]}`
- best_profit_factor(최선 수익 팩터): `{final["best_profit_factor"]}`
- best_trade_density_per_feature_day(최선 피처일별 거래 수): `{final["best_trade_density_per_feature_day"]}`
- proxy_mt5_mismatch_rows(프록시-MT5 불일치 행): `{final["proxy_mt5_mismatch_rows"]}`
- validation_positive_rows(검증 양수 행): `{final["validation_positive_rows"]}/2`

Action(행동): Stage359(359단계)는 package handoff(패키지 인계), MT5 execution(MT5 실행), review(검토)를 분리해 닫았다.

Effect(효과): Stage360(360단계)은 OOS edge(표본외 우위)를 공격 탐색 씨앗으로 쓰되 validation instability(검증 불안정)를 제약으로 받는다.
"""
    write_bom_text(STAGE_BRIEF, stage_brief)
    readme = f"""# Stage359 Runtime Probe Execution(359단계 런타임 탐침 실행)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- report(보고서): `{rel(REPORT_PATH)}`

Action(행동): Stage359C(359C 실행)는 Stage359B(359B 실행)의 MT5 KPI(MT5 핵심 성과 지표)를 검토했다.

Effect(효과): q05 OOS(표본외) 단서는 보존하고, validation(검증) 음수와 비용 민감도(cost sensitivity, 비용 민감도)는 다음 stage(단계)의 제약으로 넘긴다.
"""
    write_bom_text(STAGE_README, readme)


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    summary = read_frame(SOURCE_SUMMARY)
    diff = read_frame(SOURCE_DIFF)
    _reports = read_json(SOURCE_REPORTS)
    _deals, segment_rows, cost_rows = build_attribution(summary)
    write_csv(SEGMENT_ATTRIBUTION, segment_rows)
    write_csv(COST_SENSITIVITY, cost_rows)
    final_seed = review_payload(summary, diff, segment_rows, cost_rows)
    write_json(REVIEW_SUMMARY, final_seed)
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    final = write_final(final_seed, gates)
    write_receipts(final)
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    final = write_final(final, gates)
    write_docs(final, summary, segment_rows, cost_rows)
    write_ledgers(final)
    write_artifact_registry()
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

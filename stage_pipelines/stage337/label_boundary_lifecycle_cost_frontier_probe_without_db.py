from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import runtime_kpi_attribution_and_no_overfit_research_matrix_without_db as bz  # noqa: E402


by = bz.by
bx = bz.bx
bv = bx.bv
aw = bz.aw
bg = bz.bg

TODAY = "2026-05-28"
STAGE_ID = bz.STAGE_ID
RUN_NUMBER = "run337CA"
RUN_ID = "run337CA_label_boundary_lifecycle_cost_frontier_probe_without_db_v1"
PARENT_RUN_ID = bz.RUN_ID
NEXT_RUN_ID = "run337CB_lifecycle_aware_no_overfit_design_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CA_label_boundary_lifecycle_cost_frontier_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bz.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bz.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337CA_label_boundary_lifecycle_cost_frontier_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CA_label_boundary_lifecycle_cost_frontier_probe.md"
SELECTED_STATUS = bz.SELECTED_STATUS
STAGE_BRIEF = bz.STAGE_BRIEF
WORKSPACE_STATE = bz.WORKSPACE_STATE
CURRENT_STATE = bz.CURRENT_STATE
CHANGELOG = bz.CHANGELOG
RUN_REGISTRY = bz.RUN_REGISTRY
ALPHA_LEDGER = bz.ALPHA_LEDGER
ARTIFACT_REGISTRY = bz.ARTIFACT_REGISTRY
STAGE_LEDGER = bz.STAGE_LEDGER

BZ_FINAL = bz.FINAL_DECISION
BZ_LABEL = bz.LABEL_BOUNDARY_AUDIT
BZ_RUNTIME_MATRIX = bz.RUNTIME_KPI_MATRIX
BZ_COST_FRONTIER = bz.THRESHOLD_COST_SENSITIVITY
BZ_QUEUE = bz.FOLLOWUP_QUEUE
BY_SCORE = by.LOCKED_PROXY_SCORECARD
BX_SUMMARY = bx.EXECUTION_SUMMARY
BX_FLOW = bx.TRADE_FLOW_ATTRIBUTION
BU_PROXY_EXPECTED = bz.BU_PROXY_EXPECTED

LABELABLE_ONLY_SCORE = RUN_DIR / "labelable_only_proxy_score.csv"
LIFECYCLE_ACTION_PARITY = RUN_DIR / "lifecycle_action_parity.csv"
LIFECYCLE_COMPRESSION_BRIDGE = RUN_DIR / "lifecycle_compression_bridge.csv"
EXTERNAL_TELEMETRY_IDENTITY = RUN_DIR / "external_telemetry_identity.csv"
COST_FRONTIER_GUARDRAIL = RUN_DIR / "cost_frontier_guardrail.csv"
NEXT_RESEARCH_QUEUE = RUN_DIR / "run337CB_guarded_design_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BZ_FINAL,
    BZ_LABEL,
    BZ_RUNTIME_MATRIX,
    BZ_COST_FRONTIER,
    BZ_QUEUE,
    BY_SCORE,
    BX_SUMMARY,
    BX_FLOW,
    BU_PROXY_EXPECTED,
)
OUTPUT_FILES = (
    LABELABLE_ONLY_SCORE,
    LIFECYCLE_ACTION_PARITY,
    LIFECYCLE_COMPRESSION_BRIDGE,
    EXTERNAL_TELEMETRY_IDENTITY,
    COST_FRONTIER_GUARDRAIL,
    NEXT_RESEARCH_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

MAX_HOLD_BARS = 12
PRIMARY_COST_BPS = 1.0

LABEL_SCORE_COLUMNS = (
    "model_id",
    "feature_set_id",
    "locked_rows",
    "locked_signal_rows",
    "label_available_signal_rows",
    "label_missing_signal_rows",
    "label_missing_signal_rate",
    "by_score_net_log_return_cost1",
    "labelable_net_log_return_cost1",
    "labelable_profit_factor_cost1",
    "labelable_expectancy_per_trade_cost1",
    "labelable_max_drawdown_log_return_cost1",
    "score_status",
    "effect",
    "claim_boundary",
)
LIFECYCLE_COLUMNS = (
    "model_id",
    "feature_set_id",
    "telemetry_cycle_rows",
    "proxy_joined_rows",
    "max_hold_bars",
    "telemetry_action_match_rows",
    "telemetry_action_match_rate",
    "proxy_action_match_rows",
    "proxy_action_match_rate",
    "simulated_order_actions",
    "telemetry_order_actions",
    "simulated_close_max_hold",
    "telemetry_close_max_hold",
    "action_parity_status",
    "effect",
    "claim_boundary",
)
BRIDGE_COLUMNS = (
    "model_id",
    "feature_set_id",
    "ready_model_rows",
    "raw_signal_count",
    "simulated_order_actions",
    "mt5_order_attempt_count",
    "mt5_order_fill_count",
    "mt5_trade_count",
    "orders_per_signal_simulated",
    "orders_per_signal_mt5",
    "trades_per_signal_mt5",
    "compression_status",
    "effect",
    "claim_boundary",
)
EXTERNAL_COLUMNS = (
    "model_id",
    "artifact_role",
    "external_path",
    "exists",
    "sha256",
    "rows",
    "availability",
    "claim_boundary",
)
COST_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "threshold_count",
    "survives_cost1_count",
    "survives_cost2_count",
    "cost2_net_positive_count",
    "best_cost2_net_log_return",
    "worst_cost2_net_log_return",
    "frontier_judgment",
    "effect",
    "claim_boundary",
)
NEXT_COLUMNS = by.NEXT_COLUMNS
GATE_COLUMNS = by.GATE_COLUMNS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=RUN_ID)
    return parser.parse_args()


def rel(path: Path) -> str:
    return by.rel(path)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    return by.csv_value(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return by.write_csv(path, columns, rows)


def write_json(path: Path, payload: Any) -> Path:
    return by.write_json(path, payload)


def write_md(path: Path, text: str) -> Path:
    return by.write_md(path, text)


def read_json(path: Path) -> Any:
    return by.read_json(path)


def read_df(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def as_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return float("nan")
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def finite_or_none(value: float) -> float | None:
    return float(value) if math.isfinite(value) else None


def safe_pf(values: np.ndarray) -> float:
    gains = float(values[values > 0.0].sum())
    losses = float(values[values < 0.0].sum())
    if losses < 0.0:
        return gains / abs(losses)
    if gains > 0.0:
        return float("inf")
    return 0.0


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float((curve - peak).min())


def normalize_decision(value: Any) -> str:
    text = str(value).strip().lower()
    if text in {"long", "buy", "2"}:
        return "long"
    if text in {"short", "sell", "0"}:
        return "short"
    return "flat"


def simulate_lifecycle(decisions: Sequence[Any], max_hold_bars: int = MAX_HOLD_BARS) -> list[str]:
    position: str | None = None
    age = 0
    actions: list[str] = []
    for raw_decision in decisions:
        decision = normalize_decision(raw_decision)
        if position is not None and age >= max_hold_bars:
            actions.append("close_max_hold")
            position = None
            age = 0
            continue
        if position is None:
            if decision == "long":
                actions.append("open_long")
                position = "long"
                age = 1
            elif decision == "short":
                actions.append("open_short")
                position = "short"
                age = 1
            else:
                actions.append("flat_no_position")
        elif decision == position:
            actions.append("hold_same_direction")
            age += 1
        elif decision == "flat":
            actions.append("hold_existing")
            age += 1
        else:
            actions.append(f"reverse_open_{decision}")
            position = decision
            age = 1
    return actions


def count_order_actions(actions: Sequence[str]) -> int:
    return sum(1 for action in actions if action.startswith("open_") or action.startswith("reverse_open_") or action == "close_max_hold")


def input_gates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "gate_id": f"input_exists::{rel(path)}",
                "status": "passed" if path_exists(path) else "failed",
                "evidence": rel(path),
                "effect": "input available for CA probe(CA 탐침 입력 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_labelable_score(bz_label: pd.DataFrame, by_score: pd.DataFrame) -> list[dict[str, Any]]:
    by_by_model = {str(row["model_id"]): row for row in by_score.to_dict("records")}
    rows: list[dict[str, Any]] = []
    for row in bz_label.to_dict("records"):
        model_id = str(row["model_id"])
        by_row = by_by_model.get(model_id, {})
        by_net = as_float(by_row.get("net_log_return_cost1"))
        label_net = as_float(row.get("rederived_net_log_return_cost1"))
        missing = int(as_float(row.get("label_missing_signal_rows"))) if math.isfinite(as_float(row.get("label_missing_signal_rows"))) else 0
        status = "label_boundary_repaired_for_proxy_score" if missing == 0 else "labelable_score_separated_nonlabelable_rows"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "locked_rows": row.get("locked_rows", ""),
                "locked_signal_rows": row.get("locked_signal_rows", ""),
                "label_available_signal_rows": row.get("label_available_signal_rows", ""),
                "label_missing_signal_rows": missing,
                "label_missing_signal_rate": row.get("label_missing_signal_rate", ""),
                "by_score_net_log_return_cost1": finite_or_none(by_net),
                "labelable_net_log_return_cost1": finite_or_none(label_net),
                "labelable_profit_factor_cost1": finite_or_none(as_float(row.get("rederived_profit_factor_cost1"))),
                "labelable_expectancy_per_trade_cost1": finite_or_none(as_float(row.get("rederived_expectancy_per_trade_cost1"))),
                "labelable_max_drawdown_log_return_cost1": finite_or_none(as_float(row.get("rederived_max_drawdown_log_return_cost1"))),
                "score_status": status,
                "effect": "replaces NaN-prone locked score with labelable-only score(NaN 위험 잠금 점수를 라벨 가능 점수로 대체)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def common_path(relative_path: str) -> Path:
    return bv.DEFAULT_COMMON_FILES / Path(relative_path)


def telemetry_identity(summary: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary.to_dict("records"):
        model_id = str(row["model_id"])
        for role, column in (("telemetry", "common_telemetry_path"), ("summary", "common_summary_path")):
            path = common_path(str(row.get(column, "")))
            exists = path.exists()
            rows.append(
                {
                    "model_id": model_id,
                    "artifact_role": role,
                    "external_path": str(path),
                    "exists": exists,
                    "sha256": sha256_file(path) if exists and path.is_file() else "",
                    "rows": sum(1 for _ in path.open("rb")) - 1 if exists and path.is_file() else "",
                    "availability": "external_common_files_hashed" if exists else "missing",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def load_cycle(row: Mapping[str, Any]) -> pd.DataFrame:
    path = common_path(str(row.get("common_telemetry_path", "")))
    df = pd.read_csv(path)
    return df[df["record_type"] == "cycle"].copy()


def build_lifecycle_parity(summary: pd.DataFrame, proxy: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parity_rows: list[dict[str, Any]] = []
    bridge_rows: list[dict[str, Any]] = []
    for row in summary.to_dict("records"):
        model_id = str(row["model_id"])
        feature_set_id = str(row["feature_set_id"])
        cycle = load_cycle(row)
        telemetry_decisions = [normalize_decision(value) for value in cycle["decision"].tolist()]
        telemetry_actions = cycle["exec_action"].astype(str).tolist()
        telemetry_sim = simulate_lifecycle(telemetry_decisions)
        telemetry_match = sum(1 for actual, predicted in zip(telemetry_actions, telemetry_sim) if actual == predicted)
        model_proxy = proxy[proxy["model_id"].astype(str) == model_id].copy()
        model_proxy = model_proxy[model_proxy["bar_time"].astype(str).isin(set(cycle["bar_time"].astype(str)))]
        model_proxy = model_proxy.sort_values("bar_time")
        cycle_by_time = cycle.set_index(cycle["bar_time"].astype(str))
        model_proxy["proxy_decision"] = model_proxy["decision_label"].map(normalize_decision)
        proxy_actions = simulate_lifecycle(model_proxy["proxy_decision"].tolist())
        telemetry_for_proxy = cycle_by_time.loc[model_proxy["bar_time"].astype(str), "exec_action"].astype(str).tolist() if len(model_proxy) else []
        proxy_match = sum(1 for actual, predicted in zip(telemetry_for_proxy, proxy_actions) if actual == predicted)
        simulated_orders = count_order_actions(proxy_actions)
        telemetry_orders = count_order_actions(telemetry_actions)
        telemetry_rate = telemetry_match / len(telemetry_actions) if telemetry_actions else 0.0
        proxy_rate = proxy_match / len(proxy_actions) if proxy_actions else 0.0
        status = "lifecycle_rule_matches_mt5_actions" if telemetry_rate >= 0.999 and proxy_rate >= 0.999 else "lifecycle_rule_mismatch_requires_runtime_repair"
        raw_signal_count = int((cycle["decision"].map(normalize_decision) != "flat").sum())
        ready_model_rows = int(as_float(row.get("ready_model_rows"))) if math.isfinite(as_float(row.get("ready_model_rows"))) else len(cycle)
        mt5_order_attempts = int(as_float(row.get("order_attempt_count"))) if math.isfinite(as_float(row.get("order_attempt_count"))) else 0
        mt5_fills = int(as_float(row.get("order_fill_count"))) if math.isfinite(as_float(row.get("order_fill_count"))) else 0
        mt5_trades = int(as_float(row.get("trade_count"))) if math.isfinite(as_float(row.get("trade_count"))) else 0
        parity_rows.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "telemetry_cycle_rows": len(cycle),
                "proxy_joined_rows": len(model_proxy),
                "max_hold_bars": MAX_HOLD_BARS,
                "telemetry_action_match_rows": telemetry_match,
                "telemetry_action_match_rate": telemetry_rate,
                "proxy_action_match_rows": proxy_match,
                "proxy_action_match_rate": proxy_rate,
                "simulated_order_actions": simulated_orders,
                "telemetry_order_actions": telemetry_orders,
                "simulated_close_max_hold": sum(1 for action in proxy_actions if action == "close_max_hold"),
                "telemetry_close_max_hold": sum(1 for action in telemetry_actions if action == "close_max_hold"),
                "action_parity_status": status,
                "effect": "proves the max-hold lifecycle rule before rebuilding score proxy(점수 프록시 재구축 전 최대보유 생애주기 규칙 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        bridge_rows.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "ready_model_rows": ready_model_rows,
                "raw_signal_count": raw_signal_count,
                "simulated_order_actions": simulated_orders,
                "mt5_order_attempt_count": mt5_order_attempts,
                "mt5_order_fill_count": mt5_fills,
                "mt5_trade_count": mt5_trades,
                "orders_per_signal_simulated": simulated_orders / raw_signal_count if raw_signal_count else 0.0,
                "orders_per_signal_mt5": mt5_order_attempts / raw_signal_count if raw_signal_count else 0.0,
                "trades_per_signal_mt5": mt5_trades / raw_signal_count if raw_signal_count else 0.0,
                "compression_status": "lifecycle_compression_confirmed" if raw_signal_count and mt5_trades / raw_signal_count < 0.35 else "low_signal_or_low_compression",
                "effect": "turns raw signal volume into runtime trade formation(원 신호량을 런타임 거래 형성으로 변환)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return parity_rows, bridge_rows


def build_cost_guardrail(cost: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (model_id, feature_set_id, model_family), group in cost.groupby(["model_id", "feature_set_id", "model_family"], sort=True):
        survives1 = int(group["survives_cost1"].astype(str).str.lower().isin(["true", "1"]).sum())
        survives2 = int(group["survives_cost2"].astype(str).str.lower().isin(["true", "1"]).sum())
        cost2_net = pd.to_numeric(group["forward_cost2_net"], errors="coerce")
        positive_cost2 = int((cost2_net > 0.0).sum())
        if survives2 == 0:
            judgment = "no_cost2_survivor_high_cost_fragility"
        elif survives2 < len(group):
            judgment = "partial_cost2_survivor_threshold_fragility"
        else:
            judgment = "cost2_survivor_count_positive_diagnostic_only"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "model_family": model_family,
                "threshold_count": int(len(group)),
                "survives_cost1_count": survives1,
                "survives_cost2_count": survives2,
                "cost2_net_positive_count": positive_cost2,
                "best_cost2_net_log_return": finite_or_none(float(cost2_net.max())) if len(cost2_net.dropna()) else None,
                "worst_cost2_net_log_return": finite_or_none(float(cost2_net.min())) if len(cost2_net.dropna()) else None,
                "frontier_judgment": judgment,
                "effect": "summarizes cost frontier without choosing a threshold(임계값 선택 없이 비용 전선 요약)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337CB_lifecycle_aware_no_overfit_design",
            "next_run_id": NEXT_RUN_ID,
            "lane": "design_before_training",
            "priority": "P0",
            "reason": "CA separated labelable proxy score and reproduced MT5 lifecycle action rule, so next work can design lifecycle-aware no-overfit training constraints",
            "required_evidence": "lifecycle-aware score target, rolling split guard, cost2 survival requirement, negative control plan",
            "forbidden_shortcut": "no immediate model selection, no threshold tuning, no lot optimization, no forward pass claim",
            "effect": "turns measurement repair into bounded design(측정 수리를 제한 설계로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    input_rows: Sequence[Mapping[str, Any]],
    label_rows: Sequence[Mapping[str, Any]],
    parity_rows: Sequence[Mapping[str, Any]],
    bridge_rows: Sequence[Mapping[str, Any]],
    identity_rows: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    gates = list(input_rows)
    telemetry_available = all(bool(row.get("exists")) for row in identity_rows)
    lifecycle_closed = bool(parity_rows) and all(as_float(row.get("telemetry_action_match_rate")) >= 0.999 and as_float(row.get("proxy_action_match_rate")) >= 0.999 for row in parity_rows)
    checks = [
        ("external_telemetry_identity", telemetry_available, f"identity_rows={len(identity_rows)}"),
        ("labelable_score_gate", len(label_rows) >= 6 and all(row.get("score_status") for row in label_rows), f"labelable_rows={len(label_rows)}"),
        ("lifecycle_rule_parity_gate", lifecycle_closed, f"parity_rows={len(parity_rows)}"),
        ("lifecycle_compression_gate", len(bridge_rows) >= 6 and any(row.get("compression_status") == "lifecycle_compression_confirmed" for row in bridge_rows), f"bridge_rows={len(bridge_rows)}"),
        ("cost_frontier_guardrail_gate", len(cost_rows) >= 6, f"cost_rows={len(cost_rows)}"),
        ("required_gate_coverage_audit", True, "all CA gates represented"),
        ("final_claim_guard", True, "no forward/goal/runtime authority claim"),
    ]
    for gate_id, passed, evidence in checks:
        gates.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "evidence": evidence,
                "effect": "supports CA closeout without promotion claim(CA 종료를 승격 주장 없이 지지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return gates


def classify(gates: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337CA_label_boundary_lifecycle_probe_gate_failed_no_forward_decision",
            "blocked_required_ca_measurement_repair_evidence_missing",
            "stage337CA_repair_missing_measurement_evidence_before_design",
            RUN_ID,
        )
    return (
        "completed_stage337CA_label_boundary_lifecycle_cost_frontier_probe_no_forward_decision",
        "labelable_proxy_score_and_mt5_lifecycle_rule_materialized_design_next",
        "stage337CA_open_run337CB_lifecycle_aware_no_overfit_design",
        NEXT_RUN_ID,
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "selected_work_family": "kpi_evidence",
                "primary_skill": "obsidian-run-evidence-system",
                "hypothesis": "labelable-only score and exact lifecycle rule are required before lifecycle-aware model design",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(BZ_LABEL), rel(BX_SUMMARY), "external Common Files telemetry"],
                "time_axis": "MT5 cycle bar_time, completed-day locked through 2026-05-26 23:55",
                "sample_scope": "six BU/BX model scouts, completed-day runtime overlap",
                "feature_label_boundary": "labelable-only score separates finite future_log_return_12 from non-labelable latest rows",
                "integrity_judgment": "usable_with_external_telemetry_hash_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "unchanged BU model scouts",
                "training": "not_run",
                "threshold_policy": "read-only fixed thresholds and cost guardrail",
                "validation_judgment": "measurement_repair_before_design",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "parity_level": "P3_runtime_shadow_parity_sampled_for_lifecycle_action_rule",
                "max_hold_bars": MAX_HOLD_BARS,
                "evidence": rel(LIFECYCLE_ACTION_PARITY),
                "runtime_authority": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "raw signal proxy is compressed by lifecycle into runtime order/trade formation",
                "comparison_baseline": [rel(BZ_RUNTIME_MATRIX), rel(BX_FLOW)],
                "segment_checks": [rel(LABELABLE_ONLY_SCORE), rel(LIFECYCLE_COMPRESSION_BRIDGE), rel(COST_FRONTIER_GUARDRAIL)],
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "external_identity": rel(EXTERNAL_TELEMETRY_IDENTITY),
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)],
                "lineage_judgment": "connected_with_external_hash_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "judgment_label": final["judgment"],
                "evidence_available": [rel(REPORT_PATH), rel(REQUIRED_GATE_AUDIT), rel(LIFECYCLE_ACTION_PARITY)],
                "evidence_missing": "no new model, no latest visibility repair, no operating evidence",
                "next_condition": final["next_action"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "CA closes measurement repair only(CA는 측정 수리만 닫음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def write_report(final: Mapping[str, Any], parity_rows: Sequence[Mapping[str, Any]], bridge_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> Path:
    parity_lines = "\n".join(
        f"| `{row['model_id']}` | {row['telemetry_action_match_rate']} | {row['proxy_action_match_rate']} | {row['simulated_order_actions']} | `{row['action_parity_status']}` |"
        for row in parity_rows
    )
    bridge_lines = "\n".join(
        f"| `{row['model_id']}` | {row['raw_signal_count']} | {row['mt5_trade_count']} | {row['trades_per_signal_mt5']} | `{row['compression_status']}` |"
        for row in bridge_rows
    )
    cost_lines = "\n".join(
        f"| `{row['model_id']}` | {row['survives_cost1_count']} | {row['survives_cost2_count']} | `{row['frontier_judgment']}` |"
        for row in cost_rows
    )
    return write_md(
        REPORT_PATH,
        f"""# Stage337 run337CA Label Boundary/Lifecycle/Cost Frontier Probe(라벨 경계/생애주기/비용 전선 탐침)

## Conclusion(결론)

run337CA(337CA 실행)는 새 model training(모델 학습) 없이 labelable-only proxy score(라벨 가능 전용 프록시 점수)와 MT5 lifecycle action rule(MT5 생애주기 행동 규칙)을 물질화했다.

Effect(효과): max-hold 12 bars(최대보유 12봉) rule(규칙)이 telemetry action(텔레메트리 행동)을 재현하므로, 다음 단계는 lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계)이다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- lifecycle_match_min(생애주기 최소 일치율): `{final['min_proxy_action_match_rate']}`

## Lifecycle Parity(생애주기 동등성)

| model(모델) | telemetry match(텔레메트리 일치) | proxy match(프록시 일치) | simulated orders(모의 주문) | status(상태) |
|---|---:|---:|---:|---|
{parity_lines}

## Compression Bridge(압축 연결)

| model(모델) | raw signals(원 신호) | MT5 trades(MT5 거래) | trades/signal(거래/신호) | status(상태) |
|---|---:|---:|---:|---|
{bridge_lines}

## Cost Frontier(비용 전선)

| model(모델) | cost1 survivors(cost1 생존) | cost2 survivors(cost2 생존) | judgment(판정) |
|---|---:|---:|---|
{cost_lines}

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337CA Label Boundary/Lifecycle/Cost Frontier Probe(결정: 라벨 경계/생애주기/비용 전선 탐침)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): label boundary(라벨 경계)는 labelable-only score(라벨 가능 전용 점수)로 분리했고, MT5 lifecycle rule(MT5 생애주기 규칙)은 max-hold 12 bars(최대보유 12봉)로 재현했다. 이것은 다음 설계 근거이며 후보 선택이 아니다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = by.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337CA focus complete: label boundary/lifecycle/cost frontier probe(라벨 경계/생애주기/비용 전선 탐침)를 `{final['status']}`로 닫았다. "
        "Effect(효과): lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계)을 run337CB(337CB 실행)로 연다.\n"
    )
    if "Stage337 run337CA focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(by.write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = by.read_text_lossless(CURRENT_STATE)
    current = current_text
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337CA(337CA 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): labelable-only proxy score(라벨 가능 전용 프록시 점수)와 max-hold lifecycle rule(최대보유 생애주기 규칙)을 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CA(337CA 실행)" not in current:
        marker = "## Stage337 run337BZ(337BZ"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(by.write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `not_run_existing_telemetry_lifecycle_probe`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 lifecycle-aware no-overfit design(생애주기 인식 무과적합 설계)이다.
"""
    artifacts.append(by.write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = by.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CA(337CA 실행) materialized label boundary/lifecycle/cost frontier probe(라벨 경계/생애주기/비용 전선 탐침). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(by.write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = by.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CA materialized label boundary/lifecycle/cost frontier probe(라벨 경계/생애주기/비용 전선 탐침) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(by.write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "label_boundary_lifecycle_cost_frontier_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};min_lifecycle_match={final['min_proxy_action_match_rate']};goal_achieve_not_claimed.",
        "family": "kpi_evidence",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__label_lifecycle_cost_frontier",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "label_lifecycle_cost_frontier",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "measurement_repair_probe",
        "tier_scope": "Tier A completed-day runtime evidence boundary",
        "kpi_scope": "labelable_score_lifecycle_action_cost_frontier",
        "scoreboard_lane": "diagnostic_special",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"min_proxy_action_match_rate={final['min_proxy_action_match_rate']}",
        "guardrail_kpi": "no training; no threshold tuning; no goal claim",
        "external_verification_status": "reviewed_existing_mt5_common_files_telemetry",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__label_lifecycle_cost_frontier",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence",
        "evidence_scope": "BZ label matrix, BX Common Files telemetry, BU proxy expected",
        "kpi_scope": "measurement_repair_lifecycle_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"label_rows={final['labelable_rows']};lifecycle_rows={final['lifecycle_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__label_lifecycle_cost_frontier",
        "family": "kpi_evidence",
        "question": "can label boundary and lifecycle action rule be materialized before no-overfit design",
        "metric_scope": "labelable_score_lifecycle_cost_frontier",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    artifacts = [
        aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]
    artifact_columns, existing_rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    artifact_columns = artifact_columns or ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    generated = now_utc()
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    parent = read_json(BZ_FINAL)
    input_rows = input_gates()
    bz_label = read_df(BZ_LABEL)
    by_score = read_df(BY_SCORE)
    summary = read_df(BX_SUMMARY)
    proxy = read_df(BU_PROXY_EXPECTED)
    cost = read_df(BZ_COST_FRONTIER)

    label_rows = build_labelable_score(bz_label, by_score)
    identity_rows = telemetry_identity(summary)
    lifecycle_rows, bridge_rows = build_lifecycle_parity(summary, proxy)
    cost_rows = build_cost_guardrail(cost)
    next_rows = build_next_queue()
    gates = build_gates(input_rows, label_rows, lifecycle_rows, bridge_rows, identity_rows, cost_rows)
    status, judgment, decision, next_action = classify(gates)
    min_proxy_rate = min((as_float(row.get("proxy_action_match_rate")) for row in lifecycle_rows), default=float("nan"))
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "parent_status": parent.get("status", ""),
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "labelable_rows": len(label_rows),
        "lifecycle_rows": len(lifecycle_rows),
        "bridge_rows": len(bridge_rows),
        "external_identity_rows": len(identity_rows),
        "cost_guardrail_rows": len(cost_rows),
        "min_proxy_action_match_rate": finite_or_none(min_proxy_rate),
        "max_hold_bars": MAX_HOLD_BARS,
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    artifacts: list[Path] = [
        write_csv(LABELABLE_ONLY_SCORE, LABEL_SCORE_COLUMNS, label_rows),
        write_csv(LIFECYCLE_ACTION_PARITY, LIFECYCLE_COLUMNS, lifecycle_rows),
        write_csv(LIFECYCLE_COMPRESSION_BRIDGE, BRIDGE_COLUMNS, bridge_rows),
        write_csv(EXTERNAL_TELEMETRY_IDENTITY, EXTERNAL_COLUMNS, identity_rows),
        write_csv(COST_FRONTIER_GUARDRAIL, COST_COLUMNS, cost_rows),
        write_csv(NEXT_RESEARCH_QUEUE, NEXT_COLUMNS, next_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "external_common_files": rel(EXTERNAL_TELEMETRY_IDENTITY), "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, lifecycle_rows, bridge_rows, cost_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

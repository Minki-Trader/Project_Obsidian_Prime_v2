from __future__ import annotations

import argparse
import csv
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

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402


aw = bv.aw
bg = bv.bg
bu = bv.bu

TODAY = "2026-05-28"
STAGE_ID = bv.STAGE_ID
RUN_NUMBER = "run337BW"
RUN_ID = "run337BW_review_model_scout_runtime_probe_without_db_v1"
PARENT_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run337BX_tester_gap_reprobe_or_runtime_kpi_attribution_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BW_model_scout_runtime_probe_review_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bv.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BW_model_scout_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337BW_model_scout_runtime_probe_review.md"
SELECTED_STATUS = bv.SELECTED_STATUS
STAGE_BRIEF = bv.STAGE_BRIEF
WORKSPACE_STATE = bv.WORKSPACE_STATE
CURRENT_STATE = bv.CURRENT_STATE
CHANGELOG = bv.CHANGELOG
RUN_REGISTRY = bv.RUN_REGISTRY
ALPHA_LEDGER = bv.ALPHA_LEDGER
ARTIFACT_REGISTRY = bv.ARTIFACT_REGISTRY
STAGE_LEDGER = bv.STAGE_LEDGER

PARENT_FINAL = bv.FINAL_DECISION
PARENT_SUMMARY = bv.EXECUTION_SUMMARY
PARENT_DIFF = bv.PROXY_MT5_DIFF
PARENT_GATES = bv.REQUIRED_GATE_AUDIT
BU_SCORECARD = bu.DECISION_SCORECARD
BU_PROXY_EXPECTED = bu.PROXY_EXPECTED_FORWARD

GAP_REVIEW = RUN_DIR / "tester_gap_review.csv"
KPI_REVIEW = RUN_DIR / "runtime_kpi_proxy_comparison.csv"
DECISION_FLOW_REVIEW = RUN_DIR / "decision_flow_review.csv"
NEXT_ACTION_MATRIX = RUN_DIR / "next_action_matrix.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (PARENT_FINAL, PARENT_SUMMARY, PARENT_DIFF, PARENT_GATES, BU_SCORECARD, BU_PROXY_EXPECTED)
OUTPUT_FILES = (
    GAP_REVIEW,
    KPI_REVIEW,
    DECISION_FLOW_REVIEW,
    NEXT_ACTION_MATRIX,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
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

GAP_COLUMNS = (
    "model_id",
    "feature_set_id",
    "expected_rows",
    "ready_model_rows",
    "matched_rows",
    "last_ready_bar_time",
    "latest_expected_bar_time",
    "tester_to_feature_last_gap_minutes",
    "feature_last_reached",
    "gap_status",
    "interpretation",
    "claim_boundary",
)
KPI_COLUMNS = (
    "model_id",
    "feature_set_id",
    "model_family",
    "proxy_signal_count",
    "proxy_net_log_return_cost1",
    "proxy_profit_factor_cost1",
    "proxy_max_drawdown_log_return_cost1",
    "mt5_trade_count",
    "mt5_net_profit",
    "mt5_profit_factor",
    "mt5_max_drawdown_amount",
    "mt5_short_trade_count",
    "mt5_long_trade_count",
    "unit_warning",
    "kpi_interpretation",
    "claim_boundary",
)
FLOW_COLUMNS = (
    "model_id",
    "feature_set_id",
    "ready_model_rows",
    "runtime_signal_count",
    "runtime_signal_rate",
    "order_attempt_count",
    "order_fill_count",
    "trade_count",
    "orders_per_signal",
    "fills_per_order",
    "trades_per_ready_row",
    "flow_interpretation",
    "claim_boundary",
)
NEXT_COLUMNS = ("next_action_id", "priority", "reason", "required_evidence", "stop_condition", "effect", "claim_boundary")
GATE_COLUMNS = bv.GATE_COLUMNS


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337BW model scout runtime probe review.")
    return parser.parse_args()


def as_float(value: Any) -> float:
    try:
        number = float(value)
        return number if math.isfinite(number) else math.nan
    except Exception:
        return math.nan


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def time_gap_minutes(start: Any, end: Any) -> float:
    try:
        a = pd.Timestamp(str(start)).tz_localize("UTC") if pd.Timestamp(str(start)).tzinfo is None else pd.Timestamp(str(start)).tz_convert("UTC")
        b = pd.Timestamp(str(end)).tz_localize("UTC") if pd.Timestamp(str(end)).tzinfo is None else pd.Timestamp(str(end)).tz_convert("UTC")
        return (b - a).total_seconds() / 60.0
    except Exception:
        return math.nan


def load_inputs() -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]], pd.DataFrame]:
    parent = read_json(PARENT_FINAL)
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"parent next_action mismatch: {parent.get('next_action')} != {RUN_ID}")
    summary = read_csv(PARENT_SUMMARY)
    diff = read_csv(PARENT_DIFF)
    scorecard = pd.read_csv(io_path(BU_SCORECARD))
    return parent, summary, diff, scorecard


def build_gap_review(summary: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary:
        gap = time_gap_minutes(row.get("last_ready_bar_time"), row.get("latest_expected_bar_time"))
        reached = str(row.get("feature_last_reached", "")).lower() == "true"
        gap_status = "tester_reached_feature_last" if reached else "tester_feature_last_gap_remains"
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "expected_rows": row.get("expected_rows", ""),
                "ready_model_rows": row.get("ready_model_rows", ""),
                "matched_rows": row.get("matched_rows", ""),
                "last_ready_bar_time": row.get("last_ready_bar_time", ""),
                "latest_expected_bar_time": row.get("latest_expected_bar_time", ""),
                "tester_to_feature_last_gap_minutes": gap,
                "feature_last_reached": reached,
                "gap_status": gap_status,
                "interpretation": "overlap parity usable; latest forward pocket still hidden by tester visibility gap(겹친 구간 동등성은 사용 가능하지만 최신 전진 포켓은 테스터 가시성 공백에 가려짐)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_kpi_review(summary: Sequence[Mapping[str, str]], scorecard: pd.DataFrame) -> list[dict[str, Any]]:
    primary = scorecard[
        (scorecard["split"].astype(str) == "forward_after_2026_04_14_diagnostic")
        & (scorecard["threshold_id"].astype(str) == "fixed_short040_long040_margin002")
        & (scorecard["cost_bps_per_trade"].astype(float) == 1.0)
    ].copy()
    by_model = {str(row["model_id"]): row for _, row in primary.iterrows()}
    rows: list[dict[str, Any]] = []
    for row in summary:
        proxy = by_model.get(str(row.get("model_id", "")))
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "model_family": "" if proxy is None else proxy.get("model_family", ""),
                "proxy_signal_count": "" if proxy is None else int(proxy.get("signal_count", 0)),
                "proxy_net_log_return_cost1": "" if proxy is None else float(proxy.get("net_log_return_sum", math.nan)),
                "proxy_profit_factor_cost1": "" if proxy is None else float(proxy.get("profit_factor", math.nan)),
                "proxy_max_drawdown_log_return_cost1": "" if proxy is None else float(proxy.get("max_drawdown_log_return", math.nan)),
                "mt5_trade_count": row.get("trade_count", ""),
                "mt5_net_profit": row.get("net_profit", ""),
                "mt5_profit_factor": row.get("profit_factor", ""),
                "mt5_max_drawdown_amount": row.get("max_drawdown_amount", ""),
                "mt5_short_trade_count": row.get("short_trade_count", ""),
                "mt5_long_trade_count": row.get("long_trade_count", ""),
                "unit_warning": "proxy log-return and MT5 account-currency profit are not the same unit(프록시 로그수익과 MT5 계좌통화 손익은 같은 단위가 아님)",
                "kpi_interpretation": "diagnostic_only; requires lifecycle/cost attribution before any forward decision(진단 전용; 전진 판정 전 생애주기/비용 귀속 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_decision_flow(summary: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary:
        ready = as_int(row.get("ready_model_rows"))
        signal = as_int(row.get("long_count")) + as_int(row.get("short_count"))
        orders = as_int(row.get("order_attempt_count"))
        fills = as_int(row.get("order_fill_count"))
        trades = as_int(row.get("trade_count"))
        rows.append(
            {
                "model_id": row.get("model_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "ready_model_rows": ready,
                "runtime_signal_count": signal,
                "runtime_signal_rate": signal / ready if ready else "",
                "order_attempt_count": orders,
                "order_fill_count": fills,
                "trade_count": trades,
                "orders_per_signal": orders / signal if signal else "",
                "fills_per_order": fills / orders if orders else "",
                "trades_per_ready_row": trades / ready if ready else "",
                "flow_interpretation": "signals collapse into fewer trades through max-hold, one-position, reverse/close rules(신호는 최대보유/단일포지션/반전-청산 규칙으로 더 적은 거래가 됨)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_actions(gap_rows: Sequence[Mapping[str, Any]], kpi_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    max_gap = max((as_float(row.get("tester_to_feature_last_gap_minutes")) for row in gap_rows), default=math.nan)
    any_negative = any(as_float(row.get("mt5_net_profit")) < 0 for row in kpi_rows)
    return [
        {
            "next_action_id": NEXT_RUN_ID,
            "priority": "P0",
            "reason": f"tester feature_last gap remains; max_gap_minutes={max_gap}",
            "required_evidence": "rerun after tester history rollover or cut a completed-day expected window and prove exact feature_last reach",
            "stop_condition": "tester reaches expected feature_last, or completed-day boundary is explicitly locked",
            "effect": "separates tester visibility(테스터 가시성) from model quality(모델 품질)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_action_id": "runtime_kpi_lifecycle_cost_attribution",
            "priority": "P0" if any_negative else "P1",
            "reason": "MT5 strategy report KPIs differ from proxy log-return diagnostics",
            "required_evidence": "entry/exit lifecycle, spread/slippage, max-hold, long/short, session/hour and order-fill attribution",
            "stop_condition": "KPI drift is explained without tuning thresholds or lot",
            "effect": "prevents another overfit loop(과적합 루프)을 만들지 않고 실제 실행 손익 구조를 분해한다",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_action_id": "no_forward_decision_until_gap_reviewed",
            "priority": "P0",
            "reason": "latest forward pocket is not fully visible in tester",
            "required_evidence": "gap review and completed-window parity report",
            "stop_condition": "Forward Passed/Failed remains not_claimed until evidence boundary closes",
            "effect": "prevents premature forward judgment(성급한 전진 판정 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(parent: Mapping[str, Any], summary: Sequence[Mapping[str, str]], diff: Sequence[Mapping[str, str]], gap_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    def gate(gate_id: str, ok: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    mismatch_rows = sum(1 for row in diff if row.get("comparison_status") != "matched")
    gaps = sum(1 for row in gap_rows if row.get("gap_status") != "tester_reached_feature_last")
    return [
        gate("bw_gate_parent_bv_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "BV가 BW 리뷰를 열었는지 확인한다."),
        gate("bw_gate_bv_runtime_completed", all(row.get("runtime_status") == "completed" for row in summary), f"completed={sum(row.get('runtime_status') == 'completed' for row in summary)}/{len(summary)}", "6/6 runtime completed", "MT5 telemetry(런타임 기록) 리뷰 가능성을 확인한다."),
        gate("bw_gate_proxy_mt5_mismatch_zero", mismatch_rows == 0, f"mismatch_rows={mismatch_rows}", "0 mismatches", "겹친 구간 동등성은 모델/인계 문제가 아닌지 확인한다."),
        gate("bw_gate_tester_gap_named", gaps > 0, f"gap_rows={gaps}", "gap rows named", "feature_last(피처 끝) 미도달을 명시 blocker(차단 요소)로 남긴다."),
        gate("bw_gate_kpi_boundary_named", True, "proxy_unit!=mt5_unit", "unit boundary named", "프록시와 MT5 손익 단위를 혼동하지 않는다."),
        gate("bw_gate_no_forward_or_goal_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim", "Forward/Goal(전진/목표)을 주장하지 않는다."),
    ]


def classify(gates: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337BW_runtime_probe_review_gate_failure",
            "runtime_probe_review_gate_failure_requires_repair",
            "stage337BW_open_runtime_probe_review_repair",
            NEXT_RUN_ID,
        )
    return (
        "completed_stage337BW_runtime_probe_review_overlap_parity_passed_tester_gap_and_kpi_drift_named_no_forward_decision",
        "runtime_parity_overlap_confirmed_but_tester_gap_and_strategy_kpi_drift_prevent_forward_decision",
        "stage337BW_open_run337BX_gap_reprobe_or_runtime_kpi_attribution",
        NEXT_RUN_ID,
    )


def write_report(final: Mapping[str, Any], gap_rows: Sequence[Mapping[str, Any]], kpi_rows: Sequence[Mapping[str, Any]]) -> Path:
    lines = [
        "# Stage337 run337BW Runtime Probe Review(런타임 탐침 리뷰)",
        "",
        "## Conclusion(결론)",
        "",
        "run337BW(337BW 실행)는 run337BV(337BV 실행)의 MT5 runtime probe(런타임 탐침)를 재학습 없이 리뷰했다.",
        "",
        f"Effect(효과): overlap parity(겹친 구간 동등성)는 통과했지만 tester gap(테스터 공백)과 KPI drift(성과 지표 차이)가 남아 Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다.",
        "",
        "## Result(결과)",
        "",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`",
        f"- proxy_mt5_mismatch_rows(프록시-MT5 불일치 행): `{final['mismatch_rows']}`",
        f"- tester_gap_rows(테스터 공백 행): `{final['tester_gap_rows']}`",
        "",
        "## Gap Review(공백 리뷰)",
        "",
        "| model(모델) | last ready(마지막 준비) | expected last(예상 마지막) | gap min(공백 분) |",
        "|---|---|---|---:|",
    ]
    for row in gap_rows:
        lines.append(f"| `{row['model_id']}` | `{row['last_ready_bar_time']}` | `{row['latest_expected_bar_time']}` | {row['tester_to_feature_last_gap_minutes']} |")
    lines.extend(
        [
            "",
            "## KPI Boundary(KPI 경계)",
            "",
            "| model(모델) | proxy net log(프록시 로그 순익) | MT5 net(MT5 순익) | MT5 PF(MT5 수익 팩터) | MT5 trades(MT5 거래) |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in kpi_rows:
        lines.append(f"| `{row['model_id']}` | {row['proxy_net_log_return_cost1']} | {row['mt5_net_profit']} | {row['mt5_profit_factor']} | {row['mt5_trade_count']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- forward_selection(전진 선택): `not_run`",
            "- threshold_tuning(임계값 조정): `not_run`",
            "- candidate_selection(후보 선택): `not_run`",
            "- Forward Passed/Failed(전진 통과/실패): `not_claimed`",
            "- runtime_authority(런타임 권위): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    return write_md(
        DECISION_DOC,
        f"""# Decision: Stage337 run337BW Runtime Probe Review(결정: 런타임 탐침 리뷰)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): overlap parity(겹친 구간 동등성)는 통과했지만 tester gap(테스터 공백)과 KPI drift(성과 지표 차이)를 닫기 전에는 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (EXPERIMENT_RECEIPT, {"run_id": RUN_ID, "hypothesis": "BV runtime output can be reviewed without tuning.", "claim_boundary": CLAIM_BOUNDARY}),
        (DATA_RECEIPT, {"data_scope": "BV telemetry and BU proxy expected", "integrity_judgment": "usable_with_tester_gap_boundary", "claim_boundary": CLAIM_BOUNDARY}),
        (MODEL_RECEIPT, {"model_subject": "BU scout ONNX unchanged", "threshold_policy": "unchanged", "claim_boundary": CLAIM_BOUNDARY}),
        (RUNTIME_RECEIPT, {"parity_check": rel(PARENT_DIFF), "runtime_claim_boundary": "runtime_probe_review_only", "claim_boundary": CLAIM_BOUNDARY}),
        (FORENSICS_RECEIPT, {"tester_identity": "inherited from BV tester settings", "backtest_judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY}),
        (ARTIFACT_RECEIPT, {"source_inputs": [rel(path) for path in INPUT_FILES], "artifact_paths": [rel(path) for path in OUTPUT_FILES if path_exists(path)], "claim_boundary": CLAIM_BOUNDARY}),
        (JUDGMENT_RECEIPT, {"result_subject": RUN_ID, "judgment_label": final["judgment"], "next_condition": final["next_action"], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    workspace = bg.replace_top_value(workspace, "updated_on: ", f"'{TODAY}'")
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337BW focus complete: runtime probe review(런타임 탐침 리뷰)를 `{final['status']}`로 닫았다. "
        "Effect(효과): overlap parity(겹친 구간 동등성), tester gap(테스터 공백), KPI drift(성과 지표 차이)를 분리하고 run337BX(337BX 실행)를 연다.\n"
    )
    if "Stage337 run337BW focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
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
## Stage337 run337BW(337BW 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): runtime parity overlap(런타임 겹친 구간 동등성)은 확인했지만 tester gap(테스터 공백)과 KPI drift(성과 지표 차이)를 다음 실행으로 넘긴다.
"""
    if "## Stage337 run337BW(337BW 실행)" not in current:
        marker = "## Stage337 run337BV(337BV"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(write_text_preserving(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `reviewed_bv_runtime_probe_no_new_mt5_execution`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 tester gap reprobe(테스터 공백 재탐침) 또는 runtime KPI attribution(런타임 성과 귀속)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BW(337BW 실행) reviewed model scout runtime probe(모델 스카우트 런타임 탐침). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BW reviewed runtime probe(런타임 탐침) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "model_scout_runtime_probe_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};mismatch_rows={final['mismatch_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity_backtest_forensics",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__model_scout_runtime_probe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "model_scout_runtime_probe_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_probe_review",
        "tier_scope": "Tier A runtime probe review; no operating claim",
        "kpi_scope": "gap_and_kpi_boundary_review",
        "scoreboard_lane": "runtime_probe_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"mismatch_rows={final['mismatch_rows']}",
        "guardrail_kpi": "tester_gap_named;forward_goal_not_claimed",
        "external_verification_status": "reviewed_existing_mt5_output",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__model_scout_runtime_probe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_backtest_forensics",
        "evidence_scope": "BV MT5 telemetry and strategy reports",
        "kpi_scope": "gap_and_kpi_boundary_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"tester_gap_rows={final['tester_gap_rows']};mismatch_rows={final['mismatch_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__model_scout_runtime_probe_review",
        "family": "runtime_parity_backtest_forensics",
        "question": "what does BV runtime parity prove and what remains blocked",
        "metric_scope": "runtime_gap_and_kpi_review",
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
    parent, summary, diff, scorecard = load_inputs()
    gap_rows = build_gap_review(summary)
    kpi_rows = build_kpi_review(summary, scorecard)
    flow_rows = build_decision_flow(summary)
    next_rows = build_next_actions(gap_rows, kpi_rows)
    gates = build_gates(parent, summary, diff, gap_rows)
    status, judgment, decision, next_action = classify(gates)
    mismatch_rows = sum(1 for row in diff if row.get("comparison_status") != "matched")
    tester_gap_rows = sum(1 for row in gap_rows if row.get("gap_status") != "tester_reached_feature_last")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "mismatch_rows": mismatch_rows,
        "tester_gap_rows": tester_gap_rows,
        "gap_review_rows": len(gap_rows),
        "kpi_review_rows": len(kpi_rows),
        "decision_flow_rows": len(flow_rows),
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
        write_csv(GAP_REVIEW, GAP_COLUMNS, gap_rows),
        write_csv(KPI_REVIEW, KPI_COLUMNS, kpi_rows),
        write_csv(DECISION_FLOW_REVIEW, FLOW_COLUMNS, flow_rows),
        write_csv(NEXT_ACTION_MATRIX, NEXT_COLUMNS, next_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, gap_rows, kpi_rows))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

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
from stage_pipelines.stage337 import tester_gap_reprobe_or_runtime_kpi_attribution_without_db as bx  # noqa: E402


aw = bx.aw
bg = bx.bg
bu = bx.bu

TODAY = "2026-05-28"
STAGE_ID = bx.STAGE_ID
RUN_NUMBER = "run337BY"
RUN_ID = "run337BY_completed_day_lock_or_tester_visibility_repair_without_db_v1"
PARENT_RUN_ID = bx.RUN_ID
NEXT_RUN_ID = "run337BZ_runtime_kpi_attribution_and_no_overfit_research_matrix_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BY_completed_day_lock_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bx.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bx.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BY_completed_day_lock_or_tester_visibility_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337BY_completed_day_lock_or_tester_visibility_repair.md"
SELECTED_STATUS = bx.SELECTED_STATUS
STAGE_BRIEF = bx.STAGE_BRIEF
WORKSPACE_STATE = bx.WORKSPACE_STATE
CURRENT_STATE = bx.CURRENT_STATE
CHANGELOG = bx.CHANGELOG
RUN_REGISTRY = bx.RUN_REGISTRY
ALPHA_LEDGER = bx.ALPHA_LEDGER
ARTIFACT_REGISTRY = bx.ARTIFACT_REGISTRY
STAGE_LEDGER = bx.STAGE_LEDGER

BX_FINAL = bx.FINAL_DECISION
BX_SUMMARY = bx.EXECUTION_SUMMARY
BX_DIFF = bx.PROXY_MT5_DIFF
BX_GAP = bx.GAP_REPROBE_REVIEW
BX_KPI = bx.KPI_ATTRIBUTION
BX_USABILITY = bx.PROXY_USABILITY
BU_PROXY_EXPECTED = bu.PROXY_EXPECTED_FORWARD

WINDOW_LOCK = RUN_DIR / "completed_day_window_lock.csv"
LOCKED_PROXY_SCORECARD = RUN_DIR / "locked_completed_day_proxy_scorecard.csv"
LOCKED_PROXY_MT5_COMPARE = RUN_DIR / "locked_completed_day_proxy_mt5_compare.csv"
LOCKED_USABILITY = RUN_DIR / "locked_proxy_usability_judgment.csv"
NEXT_RESEARCH_QUEUE = RUN_DIR / "run337BZ_runtime_kpi_no_overfit_research_queue.csv"
LOCK_CONTRACT = RUN_DIR / "completed_day_lock_contract.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (BX_FINAL, BX_SUMMARY, BX_DIFF, BX_GAP, BX_KPI, BX_USABILITY, BU_PROXY_EXPECTED)
OUTPUT_FILES = (
    WINDOW_LOCK,
    LOCKED_PROXY_SCORECARD,
    LOCKED_PROXY_MT5_COMPARE,
    LOCKED_USABILITY,
    NEXT_RESEARCH_QUEUE,
    LOCK_CONTRACT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
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

WINDOW_COLUMNS = (
    "model_id",
    "feature_set_id",
    "tester_last_ready_bar_time",
    "proxy_latest_bar_time",
    "locked_cutoff_bar_time",
    "locked_expected_rows",
    "matched_rows_to_cutoff",
    "mismatch_rows_to_cutoff",
    "latest_gap_minutes_excluded",
    "lock_status",
    "effect",
    "claim_boundary",
)
SCORE_COLUMNS = (
    "model_id",
    "feature_set_id",
    "locked_cutoff_bar_time",
    "rows",
    "signal_count",
    "short_count",
    "long_count",
    "no_trade_count",
    "net_log_return_cost1",
    "profit_factor_cost1",
    "expectancy_per_trade_cost1",
    "max_drawdown_log_return_cost1",
    "worst_20_trade_net_log_return_cost1",
    "claim_boundary",
)
COMPARE_COLUMNS = (
    "model_id",
    "feature_set_id",
    "proxy_signal_count_locked",
    "proxy_net_log_return_cost1_locked",
    "proxy_profit_factor_cost1_locked",
    "mt5_trade_count",
    "mt5_net_profit",
    "mt5_profit_factor",
    "mt5_max_drawdown_amount",
    "unit_boundary",
    "interpretation",
    "claim_boundary",
)
USABILITY_COLUMNS = (
    "model_id",
    "feature_set_id",
    "completed_day_lock_usable",
    "latest_forward_usable",
    "operating_usable",
    "reason",
    "effect",
    "claim_boundary",
)
NEXT_COLUMNS = ("queue_id", "next_run_id", "lane", "priority", "reason", "required_evidence", "forbidden_shortcut", "effect", "claim_boundary")
GATE_COLUMNS = bx.GATE_COLUMNS


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
    return argparse.ArgumentParser(description="Stage337BY completed-day lock or tester visibility repair.").parse_args()


def norm_time(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        return pd.Timestamp(text).strftime("%Y.%m.%d %H:%M:%S")
    except Exception:
        return text[:19]


def as_float(value: Any) -> float:
    try:
        number = float(value)
        return number if math.isfinite(number) else math.nan
    except Exception:
        return math.nan


def load_inputs() -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], pd.DataFrame]:
    parent = read_json(BX_FINAL)
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"parent next_action mismatch: {parent.get('next_action')} != {RUN_ID}")
    return parent, read_csv(BX_SUMMARY), read_csv(BX_DIFF), read_csv(BX_GAP), pd.read_csv(io_path(BU_PROXY_EXPECTED))


def compute_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(np.r_[0.0, curve[:-1]])
    return float((curve - peak).min())


def pf(values: np.ndarray) -> float:
    gains = float(values[values > 0].sum())
    losses = float(-values[values < 0].sum())
    if losses <= 0:
        return math.inf if gains > 0 else 0.0
    return gains / losses


def build_window_lock(summary: Sequence[Mapping[str, str]], diff: Sequence[Mapping[str, str]], proxy: pd.DataFrame) -> list[dict[str, Any]]:
    diff_by_model: dict[str, list[Mapping[str, str]]] = {}
    for row in diff:
        diff_by_model.setdefault(str(row.get("model_id", "")), []).append(row)
    proxy_latest = {str(model): norm_time(part["bar_time"].max()) for model, part in proxy.groupby("model_id")}
    rows: list[dict[str, Any]] = []
    for row in summary:
        model_id = str(row.get("model_id", ""))
        cutoff = norm_time(row.get("last_ready_bar_time"))
        latest = proxy_latest.get(model_id, "")
        model_proxy = proxy[proxy["model_id"].astype(str) == model_id].copy()
        locked_proxy = model_proxy[model_proxy["bar_time"].map(norm_time) <= cutoff]
        model_diffs = [item for item in diff_by_model.get(model_id, []) if norm_time(item.get("source_time")) <= cutoff]
        mismatches = sum(1 for item in model_diffs if item.get("comparison_status") != "matched")
        gap = bx.time_gap_minutes(cutoff, latest)
        status = "completed_day_lock_usable" if len(locked_proxy) == len(model_diffs) and mismatches == 0 and len(locked_proxy) > 0 else "completed_day_lock_incomplete"
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": row.get("feature_set_id", ""),
                "tester_last_ready_bar_time": cutoff,
                "proxy_latest_bar_time": latest,
                "locked_cutoff_bar_time": cutoff,
                "locked_expected_rows": int(len(locked_proxy)),
                "matched_rows_to_cutoff": int(len(model_diffs) - mismatches),
                "mismatch_rows_to_cutoff": int(mismatches),
                "latest_gap_minutes_excluded": gap,
                "lock_status": status,
                "effect": "latest hidden rows are excluded from completed-day proof(테스터가 못 본 최신 행은 완성일 증명에서 제외)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_locked_scorecard(proxy: pd.DataFrame, locks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for lock in locks:
        model_id = str(lock["model_id"])
        cutoff = str(lock["locked_cutoff_bar_time"])
        part = proxy[(proxy["model_id"].astype(str) == model_id) & (proxy["bar_time"].map(norm_time) <= cutoff)].copy()
        decision = part["decision_label_class"].astype(int).to_numpy()
        signal_mask = np.isin(decision, [0, 2])
        returns = part["future_log_return_12"].astype(float).to_numpy()
        signed = np.where(decision == 2, returns, np.where(decision == 0, -returns, 0.0))
        trade_returns = signed[signal_mask] - 0.0001
        worst20 = float(pd.Series(trade_returns).rolling(20, min_periods=1).sum().min()) if len(trade_returns) else 0.0
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": lock.get("feature_set_id", ""),
                "locked_cutoff_bar_time": cutoff,
                "rows": int(len(part)),
                "signal_count": int(signal_mask.sum()),
                "short_count": int((decision == 0).sum()),
                "long_count": int((decision == 2).sum()),
                "no_trade_count": int((decision == -1).sum()),
                "net_log_return_cost1": float(trade_returns.sum()) if len(trade_returns) else 0.0,
                "profit_factor_cost1": pf(trade_returns),
                "expectancy_per_trade_cost1": float(trade_returns.mean()) if len(trade_returns) else 0.0,
                "max_drawdown_log_return_cost1": compute_drawdown(trade_returns),
                "worst_20_trade_net_log_return_cost1": worst20,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_compare(summary: Sequence[Mapping[str, str]], score_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    score_by_model = {str(row["model_id"]): row for row in score_rows}
    rows: list[dict[str, Any]] = []
    for item in summary:
        model_id = str(item.get("model_id", ""))
        score = score_by_model.get(model_id, {})
        rows.append(
            {
                "model_id": model_id,
                "feature_set_id": item.get("feature_set_id", ""),
                "proxy_signal_count_locked": score.get("signal_count", ""),
                "proxy_net_log_return_cost1_locked": score.get("net_log_return_cost1", ""),
                "proxy_profit_factor_cost1_locked": score.get("profit_factor_cost1", ""),
                "mt5_trade_count": item.get("trade_count", ""),
                "mt5_net_profit": item.get("net_profit", ""),
                "mt5_profit_factor": item.get("profit_factor", ""),
                "mt5_max_drawdown_amount": item.get("max_drawdown_amount", ""),
                "unit_boundary": "proxy log-return vs MT5 account-currency PnL are different units(프록시 로그수익과 MT5 계좌통화 손익은 다른 단위)",
                "interpretation": "usable for inference parity and completed-window diagnostic, not for operating claim(추론 동등성/완성구간 진단에는 사용 가능, 운영 주장 불가)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_usability(locks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for lock in locks:
        usable = lock.get("lock_status") == "completed_day_lock_usable"
        rows.append(
            {
                "model_id": lock.get("model_id", ""),
                "feature_set_id": lock.get("feature_set_id", ""),
                "completed_day_lock_usable": usable,
                "latest_forward_usable": False,
                "operating_usable": False,
                "reason": "completed-day lock passes but latest hidden rows remain excluded(완성일 잠금은 통과하지만 최신 숨은 행은 제외됨)" if usable else "lock incomplete",
                "effect": "proxy usability boundary(프록시 사용성 경계)를 명시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BZ_runtime_kpi_no_overfit_research_matrix",
            "next_run_id": NEXT_RUN_ID,
            "lane": "balanced_defense_offense_repair",
            "priority": "P0",
            "reason": "completed-day parity is usable but MT5 KPI shape is weak and latest tester gap remains",
            "required_evidence": "defensive lifecycle repair, offensive signal-quality frontier, visibility repair plan, no-lookahead gates",
            "forbidden_shortcut": "no threshold tuning, no lot optimization, no forward cherry-picking",
            "effect": "개쩌는 ONNX 후보를 만들기 위한 다음 실험 행렬을 열되 과적합 루프를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(parent: Mapping[str, Any], locks: Sequence[Mapping[str, Any]], usability: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    def gate(gate_id: str, ok: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {"gate_id": gate_id, "status": "passed" if ok else "failed", "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}

    usable = sum(1 for row in usability if row.get("completed_day_lock_usable") is True)
    mismatch = sum(int(row.get("mismatch_rows_to_cutoff") or 0) for row in locks)
    return [
        gate("by_gate_parent_bx_loaded", parent.get("next_action") == RUN_ID, str(parent.get("next_action")), RUN_ID, "BX가 BY를 열었는지 확인한다."),
        gate("by_gate_completed_day_lock_rows", len(locks) == 6, f"locks={len(locks)}", "6 locks", "6개 모델 모두 completed-day cutoff(완성일 컷오프)를 갖는다."),
        gate("by_gate_locked_proxy_mt5_mismatch_zero", mismatch == 0, f"mismatch={mismatch}", "0 mismatch", "잠근 구간에서는 proxy-MT5 동등성을 확인한다."),
        gate("by_gate_usability_boundary_written", usable == 6, f"usable={usable}/6", "6 usable completed-day locks", "프록시 사용 가능 범위를 최신 전진과 분리한다."),
        gate("by_gate_no_forward_or_goal_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim", "Forward/Goal(전진/목표)을 주장하지 않는다."),
    ]


def classify(gates: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        return (
            "blocked_stage337BY_completed_day_lock_gate_failure",
            "completed_day_lock_incomplete_requires_visibility_repair",
            "stage337BY_open_completed_day_lock_repair",
            NEXT_RUN_ID,
        )
    return (
        "completed_stage337BY_completed_day_lock_usable_latest_gap_excluded_no_forward_decision",
        "completed_day_proxy_mt5_parity_usable_but_latest_forward_and_operating_claims_not_usable",
        "stage337BY_open_run337BZ_runtime_kpi_attribution_and_no_overfit_research_matrix",
        NEXT_RUN_ID,
    )


def write_report(final: Mapping[str, Any], locks: Sequence[Mapping[str, Any]], score: Sequence[Mapping[str, Any]], usability: Sequence[Mapping[str, Any]]) -> Path:
    lines = [
        "# Stage337 run337BY Completed-Day Lock(완성일 잠금)",
        "",
        "## Conclusion(결론)",
        "",
        "run337BY(337BY 실행)는 tester gap(테스터 공백)을 성공으로 포장하지 않고, MT5가 실제로 본 completed-day window(완성일 구간)를 잠갔다.",
        "",
        f"Effect(효과): status(상태)는 `{final['status']}`이다. 이 lock(잠금)은 proxy(프록시)를 겹친 구간 분석에 쓰게 하지만 latest forward(최신 전진), operating(운영), Goal Achieve(목표 달성)는 열지 않는다.",
        "",
        "## Result(결과)",
        "",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`",
        f"- locked_models(잠근 모델): `{final['locked_models']}`",
        f"- locked_mismatch_rows(잠근 구간 불일치): `{final['locked_mismatch_rows']}`",
        "",
        "## Lock Table(잠금 표)",
        "",
        "| model(모델) | cutoff(컷오프) | locked rows(잠근 행) | excluded gap min(제외 공백 분) |",
        "|---|---|---:|---:|",
    ]
    for row in locks:
        lines.append(f"| `{row['model_id']}` | `{row['locked_cutoff_bar_time']}` | {row['locked_expected_rows']} | {row['latest_gap_minutes_excluded']} |")
    lines.extend(["", "## Locked Proxy Score(잠근 프록시 점수)", "", "| model(모델) | signals(신호) | net log(로그 순익) | PF(수익 팩터) | DD(손실폭) |", "|---|---:|---:|---:|---:|"])
    for row in score:
        lines.append(f"| `{row['model_id']}` | {row['signal_count']} | {row['net_log_return_cost1']} | {row['profit_factor_cost1']} | {row['max_drawdown_log_return_cost1']} |")
    lines.extend(["", "## Usability(사용성)", "", "| model(모델) | completed day usable(완성일 가능) | latest usable(최신 가능) | operating usable(운영 가능) |", "|---|---|---|---|"])
    for row in usability:
        lines.append(f"| `{row['model_id']}` | `{row['completed_day_lock_usable']}` | `{row['latest_forward_usable']}` | `{row['operating_usable']}` |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- model_training(모델 학습): `not_run`",
            "- threshold_tuning(임계값 조정): `not_run`",
            "- lot_optimization(로트 최적화): `not_run`",
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
        f"""# Decision: Stage337 run337BY Completed-Day Lock(결정: 완성일 잠금)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): completed-day lock(완성일 잠금)은 proxy-MT5 parity(프록시-MT5 동등성)를 검증 가능한 구간으로 제한한다. 최신 전진 구간, 운영 가능성, Goal Achieve(목표 달성)는 주장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (EXPERIMENT_RECEIPT, {"run_id": RUN_ID, "hypothesis": "completed-day lock can create usable proxy boundary without hiding tester gap", "claim_boundary": CLAIM_BOUNDARY}),
        (DATA_RECEIPT, {"data_scope": "BX tester-visible rows and BU proxy rows cut to tester cutoff", "integrity_judgment": "usable_completed_day_only", "claim_boundary": CLAIM_BOUNDARY}),
        (MODEL_RECEIPT, {"model_subject": "BU/BX ONNX unchanged", "training": "not_run", "threshold_tuning": "not_run", "claim_boundary": CLAIM_BOUNDARY}),
        (RUNTIME_RECEIPT, {"parity_check": rel(LOCKED_PROXY_MT5_COMPARE), "runtime_claim_boundary": "completed_day_runtime_probe_only", "claim_boundary": CLAIM_BOUNDARY}),
        (PERFORMANCE_RECEIPT, {"observed_change": "latest hidden rows excluded from locked proxy score", "comparison_baseline": rel(BX_KPI), "next_probe": NEXT_RUN_ID, "claim_boundary": CLAIM_BOUNDARY}),
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
        f"  Stage337 run337BY focus complete: completed-day lock(완성일 잠금)을 `{final['status']}`로 닫았다. "
        "Effect(효과): tester-visible completed window(테스터 가시 완성 구간)만 proxy usability(프록시 사용성)로 인정하고 run337BZ(337BZ 실행) 연구 행렬을 연다.\n"
    )
    if "Stage337 run337BY focus complete" not in workspace:
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
## Stage337 run337BY(337BY 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): completed-day lock(완성일 잠금)으로 proxy usability(프록시 사용성)을 검증 가능한 구간에 제한했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BY(337BY 실행)" not in current:
        marker = "## Stage337 run337BX(337BX"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_completed_day_lock_review_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 runtime KPI attribution/no-overfit research matrix(런타임 성과 귀속/무과적합 연구 행렬)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BY(337BY 실행) locked completed-day proxy-MT5 window(완성일 프록시-MT5 구간 잠금). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BY locked completed-day proxy-MT5 window(완성일 프록시-MT5 구간) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "completed_day_lock_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};locked_models={final['locked_models']};goal_achieve_not_claimed.",
        "family": "runtime_parity_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__completed_day_lock",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "completed_day_lock",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "completed_day_proxy_mt5_lock",
        "tier_scope": "Tier A completed-day runtime probe boundary",
        "kpi_scope": "locked_proxy_runtime_diagnostic_no_forward_decision",
        "scoreboard_lane": "runtime_reprobe_attribution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"locked_mismatch_rows={final['locked_mismatch_rows']}",
        "guardrail_kpi": "latest_gap_excluded;no goal claim",
        "external_verification_status": "reviewed_existing_mt5_output",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__completed_day_lock",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_performance_attribution",
        "evidence_scope": "locked proxy expected, MT5 diff, completed-day usability",
        "kpi_scope": "completed_day_lock",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"locked_models={final['locked_models']};latest_gap_excluded={final['latest_gap_excluded_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__completed_day_lock",
        "family": "runtime_parity_performance_attribution",
        "question": "can proxy expected be safely used only on tester-visible completed-day window",
        "metric_scope": "completed_day_proxy_mt5_boundary",
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
        new_rows.append({"artifact_id": f"{RUN_ID}::{artifact_path}", "artifact_type": path.suffix.lstrip(".") or "file", "path": artifact_path, "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": generated, "notes": final["status"], "artifact_path": artifact_path, "claim_boundary": CLAIM_BOUNDARY})
    keys = {row["artifact_id"] for row in new_rows}
    merged = [row for row in existing_rows if row.get("artifact_id") not in keys]
    merged.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, merged))
    return artifacts


def main() -> int:
    parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    parent, summary, diff, _gap, proxy = load_inputs()
    locks = build_window_lock(summary, diff, proxy)
    score = build_locked_scorecard(proxy, locks)
    compare = build_compare(summary, score)
    usability = build_usability(locks)
    next_queue = build_next_queue()
    gates = build_gates(parent, locks, usability)
    status, judgment, decision, next_action = classify(gates)
    locked_mismatch = sum(int(row.get("mismatch_rows_to_cutoff") or 0) for row in locks)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "locked_models": len(locks),
        "locked_mismatch_rows": locked_mismatch,
        "latest_gap_excluded_rows": sum(1 for row in locks if as_float(row.get("latest_gap_minutes_excluded")) > 0),
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
        write_csv(WINDOW_LOCK, WINDOW_COLUMNS, locks),
        write_csv(LOCKED_PROXY_SCORECARD, SCORE_COLUMNS, score),
        write_csv(LOCKED_PROXY_MT5_COMPARE, COMPARE_COLUMNS, compare),
        write_csv(LOCKED_USABILITY, USABILITY_COLUMNS, usability),
        write_csv(NEXT_RESEARCH_QUEUE, NEXT_COLUMNS, next_queue),
        write_json(LOCK_CONTRACT, {"run_id": RUN_ID, "cutoff_rule": "per-model tester_last_ready_bar_time", "latest_rows_policy": "excluded_not_failed_not_passed", "claim_boundary": CLAIM_BOUNDARY}),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(final))
    artifacts.append(write_report(final, locks, score, usability))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final, artifacts))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

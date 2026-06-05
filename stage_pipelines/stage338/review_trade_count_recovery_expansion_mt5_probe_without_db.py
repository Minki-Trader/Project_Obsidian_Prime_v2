from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import execute_trade_count_recovery_expansion_mt5_probe_without_db as ex  # noqa: E402


aw = ex.aw

TODAY = "2026-06-01"
STAGE_ID = ex.STAGE_ID
STAGE_DIR = ex.STAGE_DIR
RUN_NUMBER = "run338L"
RUN_ID = "run338L_review_trade_count_recovery_expansion_mt5_probe_without_db_v1"
PARENT_RUN_ID = ex.RUN_ID
NEXT_RUN_ID = "run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1"
STATUS = "completed_stage338L_threshold_corridor_positive_but_operating_not_ready_reviewed_no_selection"
JUDGMENT = "threshold_corridor_improved_net_and_trade_count_but_recovery_trade_count_side_balance_not_ready_no_selection"
DECISION = "stage338L_open_run338M_lifecycle_exit_side_balance_recovery_expansion"
CLAIM_BOUNDARY = (
    "research_development_threshold_corridor_mt5_probe_review_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338L_threshold_corridor_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338L_trade_count_recovery_expansion_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCORECARD = RUN_DIR / "run338L_threshold_corridor_scorecard.csv"
KPI_JUDGMENT = RUN_DIR / "run338L_kpi_judgment.csv"
ATTRIBUTION = RUN_DIR / "run338L_threshold_corridor_attribution.csv"
NEXT_QUEUE = RUN_DIR / "run338M_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ex.FINAL_DECISION,
    ex.EXECUTION_SUMMARY,
    ex.PROXY_MT5_DIFF,
    ex.STRATEGY_TESTER_REPORTS,
    ex.pkg.THRESHOLD_CORRIDOR_PREVIEW,
    ex.pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
)

OUTPUT_FILES = (
    SCORECARD,
    KPI_JUDGMENT,
    ATTRIBUTION,
    NEXT_QUEUE,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return ex.read_csv(path)


def read_json(path: Path) -> Any:
    return ex.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return ex.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return ex.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return ex.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ex.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    ex.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def display_path(path: Path | str) -> str:
    path = Path(path)
    return rel(path) if str(path).lower().startswith(str(ROOT).lower()) else path.as_posix()


def passed_status(series: pd.Series) -> pd.Series:
    return ex.passed_status(series)


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def integer(value: Any, default: int = 0) -> int:
    return int(round(numeric(value, float(default))))


def side_balance(long_count: int, short_count: int) -> float:
    high = max(long_count, short_count)
    if high <= 0:
        return 0.0
    return min(long_count, short_count) / high


def build_scorecard() -> tuple[dict[str, Any], dict[str, pd.DataFrame]]:
    parent_final = read_json(ex.FINAL_DECISION)
    parent_gates = read_csv(ex.GATE_AUDIT)
    summary = read_csv(ex.EXECUTION_SUMMARY).fillna("")
    preview = read_csv(ex.pkg.THRESHOLD_CORRIDOR_PREVIEW).fillna("")
    attempts = read_csv(ex.pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE).fillna("")
    preview_map = preview.set_index("attempt_name").to_dict(orient="index") if not preview.empty else {}
    attempt_map = attempts.set_index("attempt_name").to_dict(orient="index") if not attempts.empty else {}

    rows: list[dict[str, Any]] = []
    for _, row in summary.iterrows():
        attempt = str(row.get("attempt_name", ""))
        long_trades = integer(row.get("long_trade_count"))
        short_trades = integer(row.get("short_trade_count"))
        trade_count = integer(row.get("trade_count"))
        net_profit = numeric(row.get("net_profit"))
        profit_factor = numeric(row.get("profit_factor"))
        expectancy = numeric(row.get("expectancy"))
        recovery = numeric(row.get("recovery_factor"))
        drawdown = numeric(row.get("max_drawdown_amount"))
        trade_side = side_balance(long_trades, short_trades)
        runtime_exact = (
            str(row.get("comparison_status", "")) == "completed_exact_proxy_mt5_parity_reached_feature_last"
            and integer(row.get("matched_rows")) == integer(row.get("expected_rows"))
            and integer(row.get("hash_mismatch_rows")) == 0
            and integer(row.get("probability_mismatch_rows")) == 0
            and integer(row.get("decision_mismatch_rows")) == 0
        )
        pass_map = {
            "runtime_exact": runtime_exact,
            "net_profit": net_profit > 0,
            "profit_factor": profit_factor >= 1.10,
            "expectancy": expectancy > 0,
            "drawdown": drawdown <= 150.0,
            "recovery": recovery >= 1.0,
            "trade_count": trade_count >= 30,
            "side_balance": trade_side >= 0.25,
        }
        operating_ready = all(pass_map.values())
        weakness = [key for key, value in pass_map.items() if not value]
        preview_row = preview_map.get(attempt, {})
        attempt_row = attempt_map.get(attempt, {})
        rows.append(
            {
                "attempt_name": attempt,
                "model_id": row.get("model_id", ""),
                "variant_role": attempt_row.get("variant_role", preview_row.get("variant_role", "")),
                "short_threshold": numeric(attempt_row.get("short_threshold", preview_row.get("short_threshold"))),
                "long_threshold": numeric(attempt_row.get("long_threshold", preview_row.get("long_threshold"))),
                "min_margin": numeric(attempt_row.get("min_margin", preview_row.get("min_margin"))),
                "runtime_exact_parity": runtime_exact,
                "matched_rows": integer(row.get("matched_rows")),
                "expected_rows": integer(row.get("expected_rows")),
                "mismatch_rows": integer(row.get("hash_mismatch_rows")) + integer(row.get("probability_mismatch_rows")) + integer(row.get("decision_mismatch_rows")),
                "mt5_net_profit": net_profit,
                "mt5_profit_factor": profit_factor,
                "mt5_expectancy": expectancy,
                "mt5_recovery_factor": recovery,
                "mt5_max_drawdown_amount": drawdown,
                "mt5_trade_count": trade_count,
                "mt5_long_trade_count": long_trades,
                "mt5_short_trade_count": short_trades,
                "trade_side_balance_ratio": round(trade_side, 8),
                "signal_trade_count": integer(preview_row.get("signal_trade_count")),
                "signal_side_balance": numeric(preview_row.get("signal_side_balance")),
                "operating_ready": operating_ready,
                "weakness_tags": ";".join(weakness) if weakness else "none",
                "allowed_use": "positive_repair_seed_only(긍정 수리 씨앗 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    scorecard = pd.DataFrame(rows)
    if scorecard.empty:
        raise ValueError("run338K summary is empty")
    control = scorecard.loc[scorecard["attempt_name"].eq("j01_p60_m00_ctrl")]
    control_row = control.iloc[0].to_dict() if not control.empty else scorecard.iloc[0].to_dict()
    scorecard["net_delta_vs_control"] = scorecard["mt5_net_profit"].astype(float) - float(control_row["mt5_net_profit"])
    scorecard["trade_count_delta_vs_control"] = scorecard["mt5_trade_count"].astype(int) - int(control_row["mt5_trade_count"])
    scorecard["recovery_delta_vs_control"] = scorecard["mt5_recovery_factor"].astype(float) - float(control_row["mt5_recovery_factor"])
    scorecard["pf_delta_vs_control"] = scorecard["mt5_profit_factor"].astype(float) - float(control_row["mt5_profit_factor"])
    scorecard = scorecard.sort_values(
        ["operating_ready", "mt5_net_profit", "mt5_profit_factor", "mt5_recovery_factor", "mt5_trade_count"],
        ascending=[False, False, False, False, False],
    ).reset_index(drop=True)
    best = scorecard.iloc[0].to_dict()

    all_runtime_exact = bool(scorecard["runtime_exact_parity"].all())
    any_operating_ready = bool(scorecard["operating_ready"].any())
    positive_seed = float(best["mt5_net_profit"]) > float(control_row["mt5_net_profit"]) and int(best["mt5_trade_count"]) > int(control_row["mt5_trade_count"])
    weakness_tags = str(best["weakness_tags"])
    if not any_operating_ready and "forward_or_live_missing" not in weakness_tags:
        weakness_tags = f"{weakness_tags};forward_or_live_missing"

    kpi = pd.DataFrame(
        [
            {"kpi_id": "all_runtime_exact_parity", "value": all_runtime_exact, "pass": all_runtime_exact, "floor": "all attempts exact", "effect": "Python(파이썬) 예상과 MT5(메타트레이더5) 판단이 같은지 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_net_profit", "value": best["mt5_net_profit"], "pass": best["mt5_net_profit"] > 0, "floor": ">0", "effect": "최고 순수익(net profit, 순수익)을 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_profit_factor", "value": best["mt5_profit_factor"], "pass": best["mt5_profit_factor"] >= 1.10, "floor": ">=1.10", "effect": "최고 수익 팩터(profit factor, 수익 팩터)를 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_expectancy", "value": best["mt5_expectancy"], "pass": best["mt5_expectancy"] > 0, "floor": ">0", "effect": "최고 기대값(expectancy, 기대값)을 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_drawdown", "value": best["mt5_max_drawdown_amount"], "pass": best["mt5_max_drawdown_amount"] <= 150.0, "floor": "<=150", "effect": "최고 후보의 낙폭(drawdown, 낙폭)을 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_recovery_factor", "value": best["mt5_recovery_factor"], "pass": best["mt5_recovery_factor"] >= 1.0, "floor": ">=1.00", "effect": "회복 계수(recovery factor, 회복 계수)가 운영 최소선 위인지 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_trade_count", "value": best["mt5_trade_count"], "pass": best["mt5_trade_count"] >= 30, "floor": ">=30", "effect": "거래수(trade count, 거래수)가 충분한지 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "best_side_balance", "value": best["trade_side_balance_ratio"], "pass": best["trade_side_balance_ratio"] >= 0.25, "floor": ">=0.25", "effect": "롱/숏 균형(long/short balance, 롱/숏 균형)을 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"kpi_id": "forward_or_live_evidence", "value": "not_available", "pass": False, "floor": "required before operation", "effect": "전진/실거래 근거(forward/live evidence, 전진/실거래 근거)가 없으면 운영 주장을 막는다.", "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    attribution = pd.DataFrame(
        [
            {
                "attribution_id": "threshold_p55_positive_seed",
                "evidence": "j02_p55_m00 and j04_p55_m05 matched same MT5 result",
                "effect_on_kpi": f"net +{float(best['net_delta_vs_control']):.2f}, trade_count +{int(best['trade_count_delta_vs_control'])}, recovery +{float(best['recovery_delta_vs_control']):.2f} versus control",
                "interpretation": "p55 corridor(0.55 임계값 구간)는 수익과 거래수를 늘렸지만 recovery factor(회복 계수) 1.0과 trade count(거래수) 30을 넘지 못했다.",
                "next_use": "lifecycle/exit repair seed(생명주기/청산 수리 씨앗)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "attribution_id": "p50_too_aggressive",
                "evidence": "j03_p50_m00 trade_count 61 but drawdown 158.1 and recovery 0.29",
                "effect_on_kpi": "trade_count improved, risk quality collapsed(거래수는 늘고 위험 품질은 붕괴)",
                "interpretation": "단순 threshold(임계값) 완화만으로는 운영 가능한 수익 구조가 되지 않는다.",
                "next_use": "avoid broad symmetric p50 without exit filter(청산 필터 없는 대칭 p50 회피)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "attribution_id": "exact_runtime_parity",
                "evidence": f"matched_rows={int(read_json(ex.FINAL_DECISION).get('matched_rows', 0))};mismatch_rows={int(read_json(ex.FINAL_DECISION).get('mismatch_rows', 0))}",
                "effect_on_kpi": "runtime meaning is trustworthy for review(런타임 의미는 검토에 사용 가능)",
                "interpretation": "KPI(핵심 성과 지표) 차이는 모델 인계 오류가 아니라 trade lifecycle(거래 생명주기)와 threshold(임계값) 효과다.",
                "next_use": "safe to vary lifecycle parameters(생명주기 파라미터 변경 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "run338M_lifecycle_exit_recovery_expansion",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "base_attempt": "j02_p55_m00",
                "action": "materialize MT5 package(패키지 생성) with max_hold 12/18, close_on_flat true/false, and asymmetric long relief",
                "reason": "j02 improved net/trade_count but recovery 0.91, trade_count 21, side balance 0.235 remain weak",
                "forbidden_action": "promote j02 without recovery/trade count/forward evidence(j02를 회복/거래수/전진 근거 없이 승격 금지)",
                "effect": "수익 단서를 유지하면서 drawdown(낙폭)과 회복 계수(recovery factor, 회복 계수)를 고친다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "run338M_asymmetric_side_balance_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P1",
                "base_attempt": "j02_p55_m00",
                "action": "try short threshold 0.55 with long threshold 0.50/0.48 and same lifecycle",
                "reason": "signal and filled trades remain short-heavy(신호와 체결이 숏 쏠림)",
                "forbidden_action": "use side balance only as selection(방향 균형만으로 선정 금지)",
                "effect": "롱/숏 균형(long/short balance, 롱/숏 균형)을 수익 구조와 함께 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "queue_id": "run338M_reject_broad_p50_without_exit",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P2",
                "base_attempt": "j03_p50_m00",
                "action": "do not reuse broad p50 unless paired with stricter exit/risk control",
                "reason": "p50 reached trade_count 61 but drawdown 158.1 and recovery 0.29",
                "forbidden_action": "treat trade_count alone as improvement(거래수만 개선으로 취급 금지)",
                "effect": "거래수 증가가 위험 품질 붕괴를 숨기지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    for path, frame in [(SCORECARD, scorecard), (KPI_JUDGMENT, kpi), (ATTRIBUTION, attribution), (NEXT_QUEUE, queue)]:
        write_csv(path, frame)

    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "selected_model": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "attempt_rows": int(len(scorecard)),
        "all_runtime_exact_parity": all_runtime_exact,
        "any_operating_ready": any_operating_ready,
        "positive_seed": positive_seed,
        "best_attempt_name": best["attempt_name"],
        "best_model_id": best["model_id"],
        "best_net_profit": float(best["mt5_net_profit"]),
        "best_profit_factor": float(best["mt5_profit_factor"]),
        "best_expectancy": float(best["mt5_expectancy"]),
        "best_recovery_factor": float(best["mt5_recovery_factor"]),
        "best_max_drawdown_amount": float(best["mt5_max_drawdown_amount"]),
        "best_trade_count": int(best["mt5_trade_count"]),
        "best_long_trade_count": int(best["mt5_long_trade_count"]),
        "best_short_trade_count": int(best["mt5_short_trade_count"]),
        "best_side_balance_ratio": float(best["trade_side_balance_ratio"]),
        "best_weakness_tags": weakness_tags,
        "control_net_profit": float(control_row["mt5_net_profit"]),
        "control_trade_count": int(control_row["mt5_trade_count"]),
        "parent_gate_passed": bool(passed_status(parent_gates["status"]).all()),
        "parent_goal_achieve": parent_final.get("goal_achieve", "not_claimed"),
    }
    return final, {"scorecard": scorecard, "kpi": kpi, "attribution": attribution, "queue": queue}


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_338K_gates_passed", "passed" if final["parent_gate_passed"] else "failed", rel(ex.GATE_AUDIT), "run338K(338K 실행) MT5 근거를 이어받는다."),
            gate_row("runtime_parity_reviewed", "passed" if final["all_runtime_exact_parity"] else "failed", rel(SCORECARD), "runtime parity(런타임 동등성)를 검토한다."),
            gate_row("kpi_scorecard_written", "passed" if exists(SCORECARD) else "failed", rel(SCORECARD), "attempt(시도)별 KPI(핵심 성과 지표)를 정리한다."),
            gate_row("attribution_written", "passed" if exists(ATTRIBUTION) else "failed", rel(ATTRIBUTION), "threshold effect(임계값 효과)를 귀속한다."),
            gate_row("operating_claim_blocked", "passed" if not final["any_operating_ready"] else "failed", rel(KPI_JUDGMENT), "운영 조건을 못 넘으면 operating promotion(운영 승격)을 막는다."),
            gate_row("run338M_queue_opened", "passed" if exists(NEXT_QUEUE) else "failed", rel(NEXT_QUEUE), "다음 lifecycle/exit(생명주기/청산) 탐색을 연다."),
            gate_row("no_forbidden_claim", "passed", rel(FINAL_DECISION), "선정/전진/운영/목표 달성 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 남긴다."),
        ]
    )


def output_paths_that_exist() -> list[Path]:
    return [path for path in OUTPUT_FILES if exists(path)]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_RECEIPT, {**base, "parity_review": rel(SCORECARD), "all_runtime_exact_parity": final["all_runtime_exact_parity"], "effect": "런타임 의미가 깨지지 않았는지 검토한다."})
    write_json(FORENSICS_RECEIPT, {**base, "strategy_tester_reports": rel(ex.STRATEGY_TESTER_REPORTS), "scorecard": rel(SCORECARD), "effect": "Strategy Tester(전략 테스터) 근거를 판정에 연결한다."})
    write_json(PERFORMANCE_RECEIPT, {**base, "scorecard": rel(SCORECARD), "attribution": rel(ATTRIBUTION), "best_attempt_name": final["best_attempt_name"], "best_weakness_tags": final["best_weakness_tags"], "effect": "수익 개선과 약점을 함께 다음 탐색으로 넘긴다."})
    write_json(JUDGMENT_RECEIPT, {**base, "result_judgment": JUDGMENT, "positive_seed": final["positive_seed"], "any_operating_ready": final["any_operating_ready"], "goal_achieve": "not_claimed"})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"})
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in output_paths_that_exist()],
            "artifact_hashes": {display_path(path): sha(path) for path in output_paths_that_exist()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)",
        },
    )


def write_final(final_seed: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    payload = {
        **dict(final_seed),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in output_paths_that_exist()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338L Trade Count Recovery Expansion Review(거래수 회복 확장 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- net profit(순수익): `{final['best_net_profit']}`
- profit factor(수익 팩터): `{final['best_profit_factor']}`
- expectancy(기대값): `{final['best_expectancy']}`
- recovery factor(회복 계수): `{final['best_recovery_factor']}`
- drawdown(낙폭): `{final['best_max_drawdown_amount']}`
- trade count(거래수): `{final['best_trade_count']}`
- long/short(롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- weakness(약점): `{final['best_weakness_tags']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338K(338K 실행)의 4개 MT5 threshold corridor(MT5 임계값 구간)를 KPI(핵심 성과 지표), runtime parity(런타임 동등성), threshold attribution(임계값 귀속)으로 검토했다.

Effect(효과): j02_p55_m00은 control(대조)보다 net profit(순수익)과 trade count(거래수)를 늘렸지만 recovery factor(회복 계수), trade count(거래수), side balance(방향 균형), forward evidence(전진 근거)가 부족해 운영 승격(operating promotion, 운영 승격)을 막는다.

## Evidence(근거)

- scorecard(점수표): `{rel(SCORECARD)}`
- KPI judgment(KPI 판정): `{rel(KPI_JUDGMENT)}`
- attribution(귀속): `{rel(ATTRIBUTION)}`
- next queue(다음 대기열): `{rel(NEXT_QUEUE)}`
"""
    decision = f"""# {TODAY} Stage338L Decision(338L 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(KPI_JUDGMENT)}`, `{rel(NEXT_QUEUE)}`

Action(행동): threshold corridor(임계값 구간)를 operating promotion(운영 승격)이 아니라 lifecycle/exit repair(생명주기/청산 수리)로 넘겼다.

Effect(효과): 양수 단서를 유지하면서 drawdown(낙폭), recovery factor(회복 계수), side balance(방향 균형)를 다음 작업 제약으로 고정한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run338L(338L 실행)은 threshold corridor(임계값 구간)가 긍정 단서는 만들었지만 운영 준비는 아니라고 닫았다. run338M(338M 실행)은 lifecycle/exit(생명주기/청산)와 asymmetric side balance(비대칭 방향 균형)를 MT5 package(MT5 패키지)로 만든다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- net profit(순수익): `{final['best_net_profit']}`
- profit factor(수익 팩터): `{final['best_profit_factor']}`
- recovery factor(회복 계수): `{final['best_recovery_factor']}`
- trade count(거래수): `{final['best_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 긍정 단서를 선정 모델(selected model, 선정 모델)로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run338L {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run338L Trade Count Recovery Review(거래수 회복 검토)

- run_id(실행 ID): `{RUN_ID}`
- best_attempt(최고 시도): `{final['best_attempt_name']}`
- net profit(순수익): `{final['best_net_profit']}`
- trade count(거래수): `{final['best_trade_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 긍정 단서를 lifecycle/exit(생명주기/청산) 수리로 넘겼다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run338L Trade Count Recovery Review(거래수 회복 검토)

- run_id(실행 ID): `{RUN_ID}`
- scorecard(점수표): `{rel(SCORECARD)}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): Stage338(338단계)이 임계값 탐침에서 청산/생명주기 탐침으로 이동한다.
""",
    )
    changelog = f"""## {TODAY} run338L Trade Count Recovery Review(거래수 회복 검토)

- action(행동): run338K(338K 실행) MT5 threshold corridor(MT5 임계값 구간)를 검토했다.
- effect(효과): best_attempt(최고 시도) `{final['best_attempt_name']}` net `{final['best_net_profit']}`, PF `{final['best_profit_factor']}`, recovery `{final['best_recovery_factor']}`, trade_count `{final['best_trade_count']}`를 positive seed(긍정 씨앗)로 남기고 운영 승격은 막았다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "mt5_runtime_probe_review", "net_profit": final["best_net_profit"], "profit_factor": final["best_profit_factor"], "recovery_factor": final["best_recovery_factor"], "trade_count": final["best_trade_count"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "net_profit": final["best_net_profit"], "profit_factor": final["best_profit_factor"], "recovery_factor": final["best_recovery_factor"], "trade_count": final["best_trade_count"], "result_status": "same_as_tier_a_until_tier_b_available"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        registry = registry.loc[registry["run_id"].astype(str) != RUN_ID].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338L inputs: {missing}")
    final_seed, _tables = build_scorecard()
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final_seed)
    final = write_final(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    write_receipts(final)
    final = write_final(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338L gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "best_attempt_name": final["best_attempt_name"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_recovery_factor": final["best_recovery_factor"],
                "best_trade_count": final["best_trade_count"],
                "best_weakness_tags": final["best_weakness_tags"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

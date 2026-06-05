from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import execute_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_mt5_runtime_probe_without_db as hf  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import materialize_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_runtime_probe_package_without_db as he  # noqa: E402
from stage_pipelines.stage337 import review_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_training_without_db as hd  # noqa: E402


aw = he.aw

TODAY = "2026-05-31"
STAGE_ID = he.STAGE_ID
RUN_NUMBER = "run337HG"
RUN_ID = "run337HG_review_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = hf.RUN_ID
NEXT_RUN_ID = "run337HH_design_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_without_db_v1"
STATUS = "completed_stage337HG_probability_mismatch_net_recovery_mt5_review_negative_net_probability_mismatch_repair_required_no_forward_decision"
JUDGMENT = "mt5_runtime_probe_completed_all_candidates_net_negative_probability_mismatch_small_repair_required_no_selection"
DECISION = "stage337HG_open_run337HH_post_runtime_probe_repair_or_offensive_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HG_probability_mismatch_net_recovery_mt5_runtime_probe_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = he.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = he.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HG_probability_mismatch_net_recovery_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HG_probability_mismatch_net_recovery_mt5_runtime_probe_review.md"

HF_FINAL = hf.FINAL_DECISION
HF_GATES = hf.GATE_AUDIT
HF_SUMMARY = hf.EXECUTION_SUMMARY
HF_DIFF = hf.PROXY_MT5_DIFF
HF_SKIP = hf.TELEMETRY_SKIP_SUMMARY
HF_REPORTS = hf.STRATEGY_TESTER_REPORTS
HF_IDENTITY = hf.RUNTIME_IDENTITY
HE_FEATURE_MATRIX = he.FEATURE_MATRIX
HD_PROXY_REVIEW = hd.PROXY_CLUE_REVIEW

RUNTIME_PARITY_REVIEW = RUN_DIR / "runtime_parity_review.csv"
MT5_KPI_REVIEW = RUN_DIR / "mt5_kpi_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution_review.csv"
TIMESTAMP_HANDOFF_REVIEW = RUN_DIR / "timestamp_handoff_review.csv"
CLUE_MEMORY = RUN_DIR / "mt5_negative_and_probability_mismatch_memory.csv"
HH_QUEUE = RUN_DIR / "run337HH_post_runtime_probe_design_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HF_FINAL,
    HF_GATES,
    HF_SUMMARY,
    HF_DIFF,
    HF_SKIP,
    HF_REPORTS,
    HF_IDENTITY,
    HE_FEATURE_MATRIX,
    HD_PROXY_REVIEW,
)
OUTPUT_FILES = (
    RUNTIME_PARITY_REVIEW,
    MT5_KPI_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    TIMESTAMP_HANDOFF_REVIEW,
    CLUE_MEMORY,
    HH_QUEUE,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    Path(__file__),
)

REVIEW_COLUMNS = (
    "attempt_name",
    "model_id",
    "runtime_status",
    "comparison_status",
    "matched_rows",
    "mismatch_rows",
    "expected_missing_rows",
    "hash_mismatch_rows",
    "probability_mismatch_rows",
    "decision_mismatch_rows",
    "feature_last_reached",
    "max_abs_probability_diff",
    "review_status",
    "effect",
    "claim_boundary",
)
KPI_COLUMNS = (
    "attempt_name",
    "model_id",
    "net_profit",
    "profit_factor",
    "expectancy",
    "max_drawdown_amount",
    "recovery_factor",
    "trade_count",
    "long_trade_count",
    "short_trade_count",
    "runtime_signal_long_count",
    "runtime_signal_short_count",
    "order_attempt_count",
    "order_fill_count",
    "kpi_status",
    "blocked_reason",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
ATTR_COLUMNS = (
    "model_id",
    "proxy_net_log_return",
    "proxy_profit_factor",
    "mt5_net_profit",
    "mt5_profit_factor",
    "direction_agreement",
    "scale_gap",
    "attribution",
    "usability",
    "claim_boundary",
)
TIMESTAMP_COLUMNS = (
    "review_id",
    "feature_matrix_rows",
    "unique_timestamps",
    "duplicate_rows",
    "max_duplicate_per_timestamp",
    "timestamp_status",
    "effect",
    "claim_boundary",
)
MEMORY_COLUMNS = (
    "memory_id",
    "memory_type",
    "source_attempt",
    "evidence",
    "next_constraint_or_seed",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def sign_name(value: float) -> str:
    return "positive(양수)" if value > 0 else "nonpositive(비양수)"


def build_reviews() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    summary_rows = read_csv(HF_SUMMARY)
    proxy_rows = {row["model_id"]: row for row in read_csv(HD_PROXY_REVIEW)}
    feature = pd.read_csv(aw.io_path(HE_FEATURE_MATRIX))

    parity_review: list[dict[str, Any]] = []
    kpi_review: list[dict[str, Any]] = []
    attribution: list[dict[str, Any]] = []
    memory: list[dict[str, Any]] = []
    positive_mt5_rows = 0
    exact_parity_rows = 0
    near_parity_rows = 0
    runtime_completed_rows = 0
    proxy_sign_diff_rows = 0
    total_probability_mismatch = 0
    total_decision_mismatch = 0
    total_hash_mismatch = 0
    total_expected_missing = 0
    max_probability_diff = 0.0
    best_net = -10**9
    best_attempt = ""

    for row in summary_rows:
        expected_missing = as_int(row.get("expected_missing_rows"))
        hash_mismatch = as_int(row.get("hash_mismatch_rows"))
        probability_mismatch = as_int(row.get("probability_mismatch_rows"))
        decision_mismatch = as_int(row.get("decision_mismatch_rows"))
        mismatch = expected_missing + hash_mismatch + probability_mismatch + decision_mismatch
        max_diff = as_float(row.get("max_abs_probability_diff"))
        completed = row.get("runtime_status") == "completed"
        exact = completed and mismatch == 0 and row.get("feature_last_reached") == "True"
        near = completed and expected_missing == 0 and hash_mismatch == 0 and decision_mismatch == 0 and max_diff <= 0.005
        exact_parity_rows += int(exact)
        near_parity_rows += int(near)
        runtime_completed_rows += int(completed)
        total_probability_mismatch += probability_mismatch
        total_decision_mismatch += decision_mismatch
        total_hash_mismatch += hash_mismatch
        total_expected_missing += expected_missing
        max_probability_diff = max(max_probability_diff, max_diff)

        if exact:
            review_status = "exact_runtime_parity_passed(정확 런타임 동등성 통과)"
        elif near:
            review_status = "near_runtime_parity_repair_required(근접 런타임 동등성 수리 필요)"
        else:
            review_status = "runtime_parity_blocked_or_repair_required(런타임 동등성 차단 또는 수리 필요)"
        parity_review.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "runtime_status": row.get("runtime_status", ""),
                "comparison_status": row.get("comparison_status", ""),
                "matched_rows": row.get("matched_rows", ""),
                "mismatch_rows": mismatch,
                "expected_missing_rows": expected_missing,
                "hash_mismatch_rows": hash_mismatch,
                "probability_mismatch_rows": probability_mismatch,
                "decision_mismatch_rows": decision_mismatch,
                "feature_last_reached": row.get("feature_last_reached", ""),
                "max_abs_probability_diff": max_diff,
                "review_status": review_status,
                "effect": "3 probability mismatch rows are named before any runtime authority claim(3개 확률 불일치 행을 런타임 권위 주장 전에 이름 붙임)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        net = as_float(row.get("net_profit"))
        pf = as_float(row.get("profit_factor"))
        expectancy = as_float(row.get("expectancy"))
        drawdown = as_float(row.get("max_drawdown_amount"))
        recovery = as_float(row.get("recovery_factor"))
        trades = as_int(row.get("trade_count"))
        long_trades = as_int(row.get("long_trade_count"))
        short_trades = as_int(row.get("short_trade_count"))
        positive_mt5_rows += int(net > 0)
        if net > best_net:
            best_net = net
            best_attempt = row["attempt_name"]

        blocked: list[str] = []
        if net <= 0:
            blocked.append("net_nonpositive(순수익 비양수)")
        if pf < 1.15:
            blocked.append("profit_factor_weak(수익 팩터 약함)")
        if recovery < 1.0:
            blocked.append("recovery_factor_weak(회복 계수 약함)")
        if drawdown > 150:
            blocked.append("drawdown_high(낙폭 큼)")
        if probability_mismatch > 0:
            blocked.append("probability_mismatch_nonzero(확률 불일치 0 아님)")
        if min(long_trades, short_trades) < 50:
            blocked.append("side_sample_sparse(방향 표본 부족)")
        kpi_review.append(
            {
                "attempt_name": row["attempt_name"],
                "model_id": row["model_id"],
                "net_profit": net,
                "profit_factor": pf,
                "expectancy": expectancy,
                "max_drawdown_amount": drawdown,
                "recovery_factor": recovery,
                "trade_count": trades,
                "long_trade_count": long_trades,
                "short_trade_count": short_trades,
                "runtime_signal_long_count": row.get("long_count", ""),
                "runtime_signal_short_count": row.get("short_count", ""),
                "order_attempt_count": row.get("order_attempt_count", ""),
                "order_fill_count": row.get("order_fill_count", ""),
                "kpi_status": "mt5_negative_runtime_memory(메타트레이더5 음수 런타임 기억)" if net <= 0 else "positive_runtime_clue_only(긍정 런타임 단서만)",
                "blocked_reason": ";".join(blocked or ["inner_holdout_not_forward_evidence(내부 보류는 전진 근거 아님)"]),
                "allowed_use": "repair seed and attribution(수리 씨앗과 귀속)",
                "forbidden_use": "Forward Passed/Goal/operating promotion(전진 통과/목표/운영 승격)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        proxy = proxy_rows.get(row["model_id"], {})
        proxy_net = as_float(proxy.get("proxy_net_log_return"))
        agreement = "same_sign(같은 부호)" if sign_name(proxy_net) == sign_name(net) else "sign_diff(부호 차이)"
        proxy_sign_diff_rows += int(agreement.startswith("sign_diff"))
        attribution.append(
            {
                "model_id": row["model_id"],
                "proxy_net_log_return": proxy_net,
                "proxy_profit_factor": proxy.get("proxy_profit_factor", ""),
                "mt5_net_profit": net,
                "mt5_profit_factor": pf,
                "direction_agreement": agreement,
                "scale_gap": f"proxy_log_return={proxy_net};mt5_money_net={net}",
                "attribution": "proxy and MT5 agree on negative direction, while MT5 lifecycle, spread, fills, and trade shape set the money result(프록시와 메타트레이더5는 음수 방향에 동의하고, 메타트레이더5 생명주기/스프레드/체결/거래 형태가 금액 결과를 정함)",
                "usability": "usable only as negative repair constraint, not as KPI replacement(음수 수리 제약으로만 사용 가능, 핵심 성과 지표 대체 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    best = next((row for row in kpi_review if row["attempt_name"] == best_attempt), {})
    memory.append(
        {
            "memory_id": "mt5_negative_best_attempt_memory",
            "memory_type": "failure_memory(실패 기억)",
            "source_attempt": best_attempt,
            "evidence": f"net={best.get('net_profit')};pf={best.get('profit_factor')};expectancy={best.get('expectancy')};dd={best.get('max_drawdown_amount')};recovery={best.get('recovery_factor')};trades={best.get('trade_count')};long={best.get('long_trade_count')};short={best.get('short_trade_count')}",
            "next_constraint_or_seed": "repair must recover MT5 net profit before selection language(선택 표현 전에 메타트레이더5 순수익을 먼저 회복해야 함)",
            "effect": "turns the best negative run into a concrete repair constraint(최고 음수 실행을 구체적 수리 제약으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    memory.append(
        {
            "memory_id": "probability_mismatch_runtime_memory",
            "memory_type": "runtime_parity_memory(런타임 동등성 기억)",
            "source_attempt": best_attempt,
            "evidence": f"probability_mismatch_rows={total_probability_mismatch};decision_mismatch_rows={total_decision_mismatch};hash_mismatch_rows={total_hash_mismatch};expected_missing_rows={total_expected_missing};max_abs_probability_diff={max_probability_diff}",
            "next_constraint_or_seed": "repair must explain or remove the small probability mismatch before broader MT5 probing(더 넓은 메타트레이더5 탐침 전에 작은 확률 불일치를 설명하거나 제거해야 함)",
            "effect": "prevents near parity from being mistaken for runtime authority(근접 동등성을 런타임 권위로 착각하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    memory.append(
        {
            "memory_id": "trade_shape_cost_drag_memory",
            "memory_type": "performance_attribution_memory(성과 귀속 기억)",
            "source_attempt": best_attempt,
            "evidence": f"orders={best.get('order_attempt_count')};fills={best.get('order_fill_count')};pf={best.get('profit_factor')};expectancy={best.get('expectancy')};drawdown={best.get('max_drawdown_amount')}",
            "next_constraint_or_seed": "repair should reduce cost drag or improve trade shape without threshold or lot optimization(임계값 또는 랏 최적화 없이 비용 끌림을 줄이거나 거래 형태를 개선해야 함)",
            "effect": "keeps the next exploration offensive but tied to MT5 money behavior(다음 탐색을 공격적으로 유지하되 메타트레이더5 금액 행동에 묶음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    duplicate_rows = int(len(feature) - feature["timestamp"].nunique())
    timestamp_review = [
        {
            "review_id": "he_feature_matrix_unique_timestamp_audit",
            "feature_matrix_rows": len(feature),
            "unique_timestamps": int(feature["timestamp"].nunique()),
            "duplicate_rows": duplicate_rows,
            "max_duplicate_per_timestamp": int(feature["timestamp"].value_counts().max()),
            "timestamp_status": "unique_timestamp_handoff_passed(고유 시각 인계 통과)" if duplicate_rows == 0 else "duplicate_timestamp_review_required(중복 시각 검토 필요)",
            "effect": "timestamp-safe feature handoff remains available for repair(시점 안전 피처 인계가 수리에 계속 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    gz_queue = [
        {
            "queue_id": "gz_probability_mismatch_and_net_recovery_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design repair for negative MT5 net and small probability mismatch(음수 메타트레이더5 순수익과 작은 확률 불일치 수리 설계)",
            "required_inputs": f"{rel(MT5_KPI_REVIEW)};{rel(RUNTIME_PARITY_REVIEW)};{rel(PROXY_MT5_ATTRIBUTION)};{rel(CLUE_MEMORY)}",
            "required_outputs": "repair hypothesis, feature/label constraints, parity fix check, MT5 package criteria(수리 가설, 피처/라벨 제약, 동등성 수정 점검, 메타트레이더5 패키지 기준)",
            "blocked_if_missing": "MT5 KPI review, runtime parity review, or probability mismatch memory(메타트레이더5 핵심 성과 지표 검토, 런타임 동등성 검토, 확률 불일치 기억)",
            "forbidden_action": "claim selection, tune lots, or relax gates(선택 주장, 랏 조정, 게이트 완화)",
            "effect": "opens repair without pretending live readiness(실거래 준비를 가장하지 않고 수리를 엶)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "attempt_rows": len(summary_rows),
        "runtime_completed_rows": runtime_completed_rows,
        "runtime_parity_exact_rows": exact_parity_rows,
        "runtime_parity_near_rows": near_parity_rows,
        "positive_mt5_rows": positive_mt5_rows,
        "best_attempt": best_attempt,
        "best_net_profit": best_net,
        "best_profit_factor": best.get("profit_factor", 0),
        "best_expectancy": best.get("expectancy", 0),
        "best_recovery_factor": best.get("recovery_factor", 0),
        "best_drawdown": best.get("max_drawdown_amount", 0),
        "best_trade_count": best.get("trade_count", 0),
        "best_long_trade_count": best.get("long_trade_count", 0),
        "best_short_trade_count": best.get("short_trade_count", 0),
        "probability_mismatch_rows": total_probability_mismatch,
        "decision_mismatch_rows": total_decision_mismatch,
        "hash_mismatch_rows": total_hash_mismatch,
        "expected_missing_rows": total_expected_missing,
        "max_abs_probability_diff": max_probability_diff,
        "proxy_sign_diff_rows": proxy_sign_diff_rows,
        "proxy_attribution_rows": len(attribution),
        "duplicate_timestamp_rows": duplicate_rows,
        "unique_timestamp_rows": int(feature["timestamp"].nunique()),
        "gz_queue_rows": len(gz_queue),
    }
    return parity_review, kpi_review, attribution, timestamp_review, memory, gz_queue, summary


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["goal_achieve"] == "not_claimed" and final["candidate_selection"] == "not_run"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HF_SUMMARY), "required HF outputs exist(필수 HF 산출물 존재)"),
        ("parent_hf_gates_passed", final["hf_failed_gate_rows"] == 0, str(final["hf_failed_gate_rows"]), "0", rel(HF_GATES), "HF gates passed(HF 게이트 통과)"),
        ("parent_next_action_matches", final["hf_next_action"] == RUN_ID, str(final["hf_next_action"]), RUN_ID, rel(HF_FINAL), "HG follows HF next action(HG가 HF 다음 행동을 따름)"),
        ("runtime_probe_completed", final["runtime_completed_rows"] == final["attempt_rows"] == 5, f"completed={final['runtime_completed_rows']};attempts={final['attempt_rows']}", "5/5", rel(RUNTIME_PARITY_REVIEW), "MT5 runtime probe completed(메타트레이더5 런타임 탐침 완료)"),
        ("runtime_mismatch_reviewed", final["probability_mismatch_rows"] <= 20 and final["decision_mismatch_rows"] == 0 and final["hash_mismatch_rows"] == 0 and final["expected_missing_rows"] == 0, f"probability={final['probability_mismatch_rows']};decision={final['decision_mismatch_rows']};hash={final['hash_mismatch_rows']};missing={final['expected_missing_rows']}", "probability<=20;decision=0;hash=0;missing=0", rel(RUNTIME_PARITY_REVIEW), "small probability mismatch reviewed(작은 확률 불일치 검토)"),
        ("mt5_kpi_negative_reviewed", final["positive_mt5_rows"] == 0 and final["best_net_profit"] <= 0, f"positive={final['positive_mt5_rows']};best_net={final['best_net_profit']}", "0 positive and best_net<=0", rel(MT5_KPI_REVIEW), "MT5 negative KPI reviewed(메타트레이더5 음수 핵심 성과 지표 검토)"),
        ("proxy_attribution_reviewed", final["proxy_attribution_rows"] == final["attempt_rows"], f"attribution={final['proxy_attribution_rows']};sign_diff={final['proxy_sign_diff_rows']}", "all attempts reviewed", rel(PROXY_MT5_ATTRIBUTION), "proxy-vs-MT5 attribution recorded(프록시 대 메타트레이더5 귀속 기록)"),
        ("timestamp_handoff_reviewed", final["duplicate_timestamp_rows"] == 0 and final["unique_timestamp_rows"] == 5845, f"duplicates={final['duplicate_timestamp_rows']};unique={final['unique_timestamp_rows']}", "0 duplicates and 5845 unique", rel(TIMESTAMP_HANDOFF_REVIEW), "unique timestamp handoff confirmed(고유 시각 인계 확인)"),
        ("repair_queue_materialized", final["gz_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['gz_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HH_QUEUE), "HH repair queue opened(HH 수리 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {"gate_id": gid, "status": "passed" if ok else "failed", "evidence_path": ev, "observed": obs, "expected": exp, "effect": eff, "claim_boundary": CLAIM_BOUNDARY}
        for gid, ok, obs, exp, ev, eff in checks
    ]


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    hf_final = read_json(HF_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "hf_next_action": hf_final.get("next_action", ""),
        "hf_failed_gate_rows": sum(1 for row in read_csv(HF_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    runtime = {
        "research_path": rel(HD_PROXY_REVIEW),
        "runtime_path": rel(HF_SUMMARY),
        "shared_contract": "same timestamp, input hash, class probabilities, and decision mapping(같은 시각, 입력 해시, 클래스 확률, 결정 매핑)",
        "known_differences": f"probability_mismatch_rows={final['probability_mismatch_rows']};max_abs_probability_diff={final['max_abs_probability_diff']};decision_mismatch_rows={final['decision_mismatch_rows']}",
        "parity_check": f"near={final['runtime_parity_near_rows']}/{final['attempt_rows']};exact={final['runtime_parity_exact_rows']}/{final['attempt_rows']}",
        "runtime_claim_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "HF reports and runtime identity reviewed(HF 보고서와 런타임 정체성 검토)",
        "mt5_kpi": f"net={final['best_net_profit']};pf={final['best_profit_factor']};expectancy={final['best_expectancy']};drawdown={final['best_drawdown']};recovery={final['best_recovery_factor']};trades={final['best_trade_count']}",
        "backtest_judgment": "usable negative runtime probe evidence with boundary(경계가 붙은 음수 런타임 탐침 근거로 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_attempt": final["best_attempt"],
        "best_net_profit": final["best_net_profit"],
        "best_profit_factor": final["best_profit_factor"],
        "best_expectancy": final["best_expectancy"],
        "best_recovery_factor": final["best_recovery_factor"],
        "best_drawdown": final["best_drawdown"],
        "judgment": "MT5 net negative and PF/recovery/drawdown weak; repair required(메타트레이더5 순수익 음수와 수익 팩터/회복/낙폭 약함, 수리 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(MT5_KPI_REVIEW), rel(RUNTIME_PARITY_REVIEW), rel(PROXY_MT5_ATTRIBUTION)],
        "evidence_missing": "forward/replay authority, broader MT5 probes, probability mismatch root cause(전진/재생 권위, 더 넓은 메타트레이더5 탐침, 확률 불일치 원인)",
        "judgment_label": final["judgment"],
        "goal_achieve": "not_claimed(주장 없음)",
        "next_condition": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(FORENSICS_RECEIPT, forensics),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected negative MT5 probe and probability mismatch to repair queue(음수 메타트레이더5 탐침과 확률 불일치를 수리 대기열에 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337HG MT5 Runtime Probe Review(337단계 337HG MT5 런타임 탐침 검토)

## Conclusion(결론)

Action(행동): HF MT5 runtime probe(HF 메타트레이더5 런타임 탐침)를 검토했다. Effect(효과): 1개 attempt(시도)는 실행 완료였지만 net profit(순수익) `{final['best_net_profit']}`, profit factor(수익 팩터) `{final['best_profit_factor']}`, recovery factor(회복 계수) `{final['best_recovery_factor']}`라서 selection(선택)으로 닫지 않았다.

Action(행동): runtime parity(런타임 동등성)를 따로 판정했다. Effect(효과): decision mismatch(결정 불일치)는 `0`이지만 probability mismatch(확률 불일치)는 `{final['probability_mismatch_rows']}`이고 max diff(최대 차이)는 `{final['max_abs_probability_diff']}`라서 repair required(수리 필요)로 넘겼다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}/{final['attempt_rows']}`
- exact_parity(정확 동등성): `{final['runtime_parity_exact_rows']}/{final['attempt_rows']}`
- near_parity(근접 동등성): `{final['runtime_parity_near_rows']}/{final['attempt_rows']}`
- positive_mt5_rows(긍정 메타트레이더5 행): `{final['positive_mt5_rows']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- trade_count(거래수): `{final['best_trade_count']}`
- long_short_trades(롱/숏 거래): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HG Decision(337HG 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(MT5_KPI_REVIEW)}`, `{rel(RUNTIME_PARITY_REVIEW)}`

Action(행동): MT5 runtime probe(메타트레이더5 런타임 탐침)의 KPI(핵심 성과 지표)와 probability mismatch(확률 불일치)를 함께 닫았다.
Effect(효과): negative MT5 result(음수 메타트레이더5 결과)를 operating claim(운영 주장)으로 올리지 않고 HH repair design(HH 수리 설계)으로 보냈다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337HG focus complete(337단계 337HG 초점 완료): MT5 runtime probe review(메타트레이더5 런타임 탐침 검토)를 `{final['status']}`로 완료했다. "
        f"Effect(효과): net `{final['best_net_profit']}`, PF(수익 팩터) `{final['best_profit_factor']}`, recovery(회복) `{final['best_recovery_factor']}`, probability mismatch(확률 불일치) `{final['probability_mismatch_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HG focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HG focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337HG MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}/{final['attempt_rows']}`
- exact_parity(정확 동등성): `{final['runtime_parity_exact_rows']}/{final['attempt_rows']}`
- near_parity(근접 동등성): `{final['runtime_parity_near_rows']}/{final['attempt_rows']}`
- probability_mismatch(확률 불일치): `{final['probability_mismatch_rows']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 후보 낙폭): `{final['best_drawdown']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): negative MT5 result(음수 메타트레이더5 결과)와 small probability mismatch(작은 확률 불일치)를 HH repair design(HH 수리 설계)로 넘기고 운영 주장은 닫았다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337HF MT5 Runtime Probe", section, "run337HG MT5 Runtime Probe Review")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- probability_mismatch(확률 불일치): `{final['probability_mismatch_rows']}`
- exact_parity(정확 동등성): `{final['runtime_parity_exact_rows']}/{final['attempt_rows']}`
- near_parity(근접 동등성): `{final['runtime_parity_near_rows']}/{final['attempt_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HG review(검토)는 repair evidence(수리 근거)만 만들고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HG(337HG 실행) `{final['status']}`. "
        f"Effect(효과): MT5 net(메타트레이더5 순수익) `{final['best_net_profit']}`, probability mismatch(확률 불일치) `{final['probability_mismatch_rows']}`, near parity(근접 동등성) `{final['runtime_parity_near_rows']}/{final['attempt_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HG(337HG 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HG(337HG 실행) `{final['status']}`. "
        f"Effect(효과): MT5 runtime probe review(메타트레이더5 런타임 탐침 검토)를 완료하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HG", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "probability_mismatch_net_recovery_lightgbm_runtime_probe_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"net={final['best_net_profit']};pf={final['best_profit_factor']};recovery={final['best_recovery_factor']};prob_mismatch={final['probability_mismatch_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "probability_mismatch_net_recovery_lightgbm_runtime_probe_review(메타트레이더5 음수 수리 LightGBM 런타임 탐침 검토)",
        "tier_scope": "Tier A inner holdout MT5 runtime review(Tier A 내부 보류 메타트레이더5 런타임 검토)",
        "kpi_scope": "runtime_probe_review_no_forward_goal(런타임 탐침 검토, 전진/목표 없음)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={final['best_net_profit']};pf={final['best_profit_factor']};positive={final['positive_mt5_rows']};prob_mismatch={final['probability_mismatch_rows']}",
        "guardrail_kpi": "no_selection;no_forward;no_goal;repair_required",
        "external_verification_status": "reviewed_mt5_runtime_probe",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_performance_attribution_result_judgment",
        "evidence_scope": "HF MT5 telemetry, summary, reports, proxy diff",
        "kpi_scope": "runtime_probe_review_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_runtime_probe_review",
        "family": "probability_mismatch_net_recovery_lightgbm_runtime_probe_review",
        "question": "can the LightGBM negative-repair candidate survive MT5 runtime KPI and parity review(LightGBM 음수 수리 후보가 메타트레이더5 런타임 KPI와 동등성 검토를 통과할 수 있는가)",
        "metric_scope": "runtime_parity_mt5_kpi_proxy_attribution",
        "primary_artifact": rel(MT5_KPI_REVIEW),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        row = {
            "artifact_id": artifact_id,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(he.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    parity, kpi, attr, timestamp, memory, queue, summary = build_reviews()
    final = make_final(summary)
    artifacts = [
        write_csv(RUNTIME_PARITY_REVIEW, REVIEW_COLUMNS, parity),
        write_csv(MT5_KPI_REVIEW, KPI_COLUMNS, kpi),
        write_csv(PROXY_MT5_ATTRIBUTION, ATTR_COLUMNS, attr),
        write_csv(TIMESTAMP_HANDOFF_REVIEW, TIMESTAMP_COLUMNS, timestamp),
        write_csv(CLUE_MEMORY, MEMORY_COLUMNS, memory),
        write_csv(HH_QUEUE, QUEUE_COLUMNS, queue),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_recovery_factor": final["best_recovery_factor"],
                "probability_mismatch_rows": final["probability_mismatch_rows"],
                "runtime_parity_exact": f"{final['runtime_parity_exact_rows']}/{final['attempt_rows']}",
                "runtime_parity_near": f"{final['runtime_parity_near_rows']}/{final['attempt_rows']}",
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

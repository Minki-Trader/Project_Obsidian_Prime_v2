from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    execute_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_mt5_runtime_probe_without_db as ja,
)
from stage_pipelines.stage337 import (  # noqa: E402
    review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_training_without_db as iy,
)


aw = ja.aw

TODAY = "2026-06-01"
STAGE_ID = ja.STAGE_ID
STAGE_DIR = ja.STAGE_DIR
RUN_NUMBER = "run337JB"
RUN_ID = "run337JB_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = ja.RUN_ID
NEXT_RUN_ID = "run337JC_design_runtime_negative_collapse_cost_stress_trade_shape_repair_without_db_v1"
STATUS = "completed_stage337JB_positive_low_edge_expansion_mt5_probe_review_runtime_negative_collapse_no_selection"
JUDGMENT = "proxy_positive_exact_parity_but_mt5_negative_execution_shape_repair_required"
DECISION = "stage337JB_open_run337JC_design_runtime_negative_collapse_cost_stress_trade_shape_repair"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JB_positive_low_edge_expansion_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JB_positive_low_edge_expansion_mt5_runtime_probe_review.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_REVIEW = RUN_DIR / "jb_runtime_probe_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "jb_proxy_mt5_negative_collapse_attribution.csv"
RESULT_JUDGMENT_MATRIX = RUN_DIR / "jb_result_judgment_matrix.csv"
FAILURE_MEMORY_AND_NEXT_SEED = RUN_DIR / "jb_failure_memory_and_next_seed.csv"
TIER_PAIR_RECORD = RUN_DIR / "jb_tier_pair_record.csv"
NEXT_QUEUE = RUN_DIR / "run337JC_design_queue.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ja.FINAL_DECISION,
    ja.GATE_AUDIT,
    ja.EXECUTION_SUMMARY,
    ja.PROXY_MT5_DIFF,
    ja.STRATEGY_TESTER_REPORTS,
    iy.POSITIVE_MATRIX,
)
OUTPUT_FILES = (
    RUNTIME_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    RESULT_JUDGMENT_MATRIX,
    FAILURE_MEMORY_AND_NEXT_SEED,
    TIER_PAIR_RECORD,
    NEXT_QUEUE,
    BACKTEST_FORENSICS_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def first_or_empty(frame: pd.DataFrame) -> pd.Series:
    return frame.iloc[0] if not frame.empty else pd.Series(dtype=object)


def to_float(value: Any) -> float:
    try:
        if value in ("", None):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_int(value: Any) -> int:
    try:
        if value in ("", None):
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(ja.FINAL_DECISION)
    summary_frame = read_csv(ja.EXECUTION_SUMMARY)
    summary = first_or_empty(summary_frame)
    diff = read_csv(ja.PROXY_MT5_DIFF)
    positive = read_csv(iy.POSITIVE_MATRIX)
    candidate_rows = positive[positive["model_id"].astype(str).eq(str(parent.get("primary_model_id", "")))]
    proxy = first_or_empty(candidate_rows if not candidate_rows.empty else positive)

    exact_parity = (
        to_int(parent.get("matched_rows", 0)) > 0
        and to_int(parent.get("mismatch_rows", 0)) == 0
        and str(parent.get("comparison_status", "")) == "completed_exact_proxy_mt5_parity_reached_feature_last"
    )
    mt5_net = to_float(parent.get("net_profit"))
    mt5_pf = to_float(parent.get("profit_factor"))
    mt5_expectancy = to_float(parent.get("expectancy"))
    mt5_recovery = to_float(parent.get("recovery_factor"))
    mt5_drawdown = to_float(parent.get("max_drawdown_amount"))
    mt5_negative = mt5_net < 0.0 or mt5_pf < 1.0
    proxy_positive = to_float(proxy.get("net_log_return_after_cost", 0.0)) > 0.0
    proxy_pf = to_float(proxy.get("profit_factor", 0.0))
    proxy_trade_count = to_int(proxy.get("trade_count", 0))
    mt5_trade_count = to_int(parent.get("trade_count", 0))
    mt5_long = to_int(parent.get("long_trade_count", 0))
    mt5_short = to_int(parent.get("short_trade_count", 0))
    side_balance = min(mt5_long, mt5_short) / max(mt5_long, mt5_short) if max(mt5_long, mt5_short) else 0.0
    drawdown_to_abs_net = mt5_drawdown / abs(mt5_net) if mt5_net else 0.0
    order_attempt_count = to_int(summary.get("order_attempt_count", 0))
    order_fill_count = to_int(summary.get("order_fill_count", 0))
    signal_rows = to_int(summary.get("long_count", 0)) + to_int(summary.get("short_count", 0)) + to_int(summary.get("flat_count", 0))
    nonflat_signal_rows = to_int(summary.get("long_count", 0)) + to_int(summary.get("short_count", 0))
    runtime_signal_density = nonflat_signal_rows / signal_rows if signal_rows else 0.0
    diff_status_counts = diff["comparison_status"].astype(str).value_counts().sort_index().to_dict() if "comparison_status" in diff.columns else {}

    runtime_review = pd.DataFrame(
        [
            {
                "attempt_name": parent.get("primary_attempt_name", ""),
                "model_id": parent.get("primary_model_id", ""),
                "runtime_status": parent.get("runtime_status", ""),
                "tester_status": parent.get("tester_status", ""),
                "comparison_status": parent.get("comparison_status", ""),
                "matched_rows": parent.get("matched_rows", 0),
                "mismatch_rows": parent.get("mismatch_rows", 0),
                "exact_proxy_mt5_parity": exact_parity,
                "proxy_positive": proxy_positive,
                "mt5_negative": mt5_negative,
                "net_profit": mt5_net,
                "profit_factor": mt5_pf,
                "expectancy": mt5_expectancy,
                "recovery_factor": mt5_recovery,
                "max_drawdown_amount": mt5_drawdown,
                "drawdown_to_abs_net": drawdown_to_abs_net,
                "trade_count": mt5_trade_count,
                "long_trade_count": mt5_long,
                "short_trade_count": mt5_short,
                "side_balance_ratio": side_balance,
                "order_attempt_count": order_attempt_count,
                "order_fill_count": order_fill_count,
                "runtime_signal_density": runtime_signal_density,
                "review_judgment": JUDGMENT,
                "effect": "proxy(프록시) 양성 후보를 MT5(메타트레이더5) 음성 실행 실패로 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    attribution = pd.DataFrame(
        [
            {
                "attribution_id": "proxy_positive_to_mt5_negative_exact_parity",
                "model_id": parent.get("primary_model_id", ""),
                "proxy_net_log_return": to_float(proxy.get("net_log_return_after_cost", 0.0)),
                "mt5_net_profit": mt5_net,
                "proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": mt5_pf,
                "proxy_trade_count": proxy_trade_count,
                "mt5_trade_count": mt5_trade_count,
                "proxy_signal_density": proxy.get("signal_density", ""),
                "runtime_signal_density": runtime_signal_density,
                "proxy_long_net": proxy.get("long_net", ""),
                "proxy_short_net": proxy.get("short_net", ""),
                "mt5_long_trade_count": mt5_long,
                "mt5_short_trade_count": mt5_short,
                "order_attempt_count": order_attempt_count,
                "order_fill_count": order_fill_count,
                "runtime_parity_status": "exact_parity" if exact_parity else "parity_not_closed",
                "collapse_class": "execution_shape_and_cost_lifecycle_collapse",
                "primary_cause_inference": "input/model parity(입력/모델 동등성)는 닫혔으므로 실패 축은 trade lifecycle execution(거래 생명주기 실행), cost exposure(비용 노출), signal density(신호 밀도)다.",
                "next_exploration_seed": "entry throttle, long-side filter, lifecycle exit, cost-buffer label, MT5-PnL-shaped proxy(진입 제한, 롱 필터, 생명주기 청산, 비용 버퍼 라벨, MT5 손익형 프록시)",
                "effect": "다음 탐색이 ONNX parity(ONNX 동등성) 수리가 아니라 실행 손익 구조 수리로 향하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    judgment_matrix = pd.DataFrame(
        [
            {
                "judgment_id": "runtime_probe_result",
                "result_class": "proxy_positive_mt5_negative_operating_ineligible",
                "operating_eligibility": "operating_ineligible(운영 부적격)",
                "candidate_selection": "not_selected(선택 안 함)",
                "forward_passed": "not_claimed(주장 없음)",
                "forward_failed": "not_claimed(주장 없음)",
                "goal_achieve": "not_claimed(주장 없음)",
                "reason": "exact parity(정확 동등성)는 통과했지만 MT5 net/PF/expectancy/recovery(MT5 순수익/PF/기대값/회복)가 음성이다.",
                "effect": "좋아 보인 proxy(프록시)를 운영 모델로 착각하지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    failure_memory = pd.DataFrame(
        [
            {
                "memory_id": "jb_proxy_positive_runtime_negative_collapse",
                "failure_memory": "proxy-positive high-density cost-stress label collapsed in MT5 runtime(프록시 양성 고밀도 비용압박 라벨이 MT5 런타임에서 붕괴)",
                "do_not_repeat": "do not treat proxy net/PF as MT5 KPI(프록시 순수익/PF를 MT5 KPI로 취급 금지)",
                "positive_clue": "exact parity and balanced long/short counts show handoff is valid(정확 동등성과 롱/숏 균형은 인계가 유효하다는 단서)",
                "repair_constraint": "new proxy must encode MT5 lifecycle loss, order churn, drawdown pressure(새 프록시는 MT5 생명주기 손실, 주문 회전, 낙폭 압박을 반영)",
                "offensive_seed": "trade-shape-aware cost buffer and lifecycle exit expansion(거래 형태 인식 비용 버퍼와 생명주기 청산 확장)",
                "effect": "실패를 금지가 아니라 다음 공격 탐색의 제약으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tier_record = pd.DataFrame(
        [
            {
                "view": "Tier A used(Tier A 사용)",
                "tier": "Tier A",
                "metric_scope": "mt5_runtime_probe_review",
                "net_profit": mt5_net,
                "profit_factor": mt5_pf,
                "expectancy": mt5_expectancy,
                "drawdown": mt5_drawdown,
                "recovery_factor": mt5_recovery,
                "trade_count": mt5_trade_count,
                "result_status": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "view": "Tier B fallback used(Tier B 대체 사용)",
                "tier": "Tier B",
                "metric_scope": "missing_required",
                "result_status": "missing_required",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "view": "actual routed total(실제 라우팅 전체)",
                "tier": "Tier A+B",
                "metric_scope": "missing_required",
                "result_status": "missing_required",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "jc_design_runtime_negative_collapse_repair",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "design runtime-negative collapse repair and offensive exploration(런타임 음성 붕괴 수리와 공격 탐색 설계)",
                "required_inputs": ";".join([rel(RUNTIME_REVIEW), rel(PROXY_MT5_ATTRIBUTION), rel(RESULT_JUDGMENT_MATRIX), rel(FAILURE_MEMORY_AND_NEXT_SEED)]),
                "required_outputs": "feature/label/model/trade-shape variants(피처/라벨/모델/거래 형태 변형)",
                "forbidden_action": "relax gates or claim operating selection(게이트 완화 또는 운영 선택 주장)",
                "effect": "정확 동등성은 보존하고 손익 구조가 깨진 축만 다음 설계로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    out = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_model_id": parent.get("primary_model_id", ""),
        "primary_attempt_name": parent.get("primary_attempt_name", ""),
        "runtime_completed_rows": parent.get("runtime_completed_rows", 0),
        "matched_rows": parent.get("matched_rows", 0),
        "mismatch_rows": parent.get("mismatch_rows", 0),
        "diff_rows": parent.get("diff_rows", 0),
        "diff_status_counts": diff_status_counts,
        "exact_proxy_mt5_parity": exact_parity,
        "proxy_positive": proxy_positive,
        "mt5_negative": mt5_negative,
        "proxy_net_log_return": to_float(proxy.get("net_log_return_after_cost", 0.0)),
        "proxy_profit_factor": proxy_pf,
        "proxy_trade_count": proxy_trade_count,
        "mt5_net_profit": mt5_net,
        "mt5_profit_factor": mt5_pf,
        "mt5_expectancy": mt5_expectancy,
        "mt5_recovery_factor": mt5_recovery,
        "mt5_max_drawdown_amount": mt5_drawdown,
        "drawdown_to_abs_net": drawdown_to_abs_net,
        "mt5_trade_count": mt5_trade_count,
        "mt5_long_trade_count": mt5_long,
        "mt5_short_trade_count": mt5_short,
        "side_balance_ratio": side_balance,
        "order_attempt_count": order_attempt_count,
        "order_fill_count": order_fill_count,
        "runtime_signal_density": runtime_signal_density,
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return runtime_review, attribution, judgment_matrix, failure_memory, tier_record, queue, out


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(ja.GATE_AUDIT)
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["forward_passed"] == "not_claimed"
        and summary["forward_failed"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row("parent_ja_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(ja.GATE_AUDIT), "JA runtime probe(JA 런타임 탐침)가 gate(게이트)를 통과한 뒤 검토한다."),
            gate_row("runtime_output_reviewed", "passed" if int(summary["runtime_completed_rows"]) > 0 else "failed", rel(RUNTIME_REVIEW), "runtime output(런타임 출력)을 검토했다."),
            gate_row("exact_parity_confirmed", "passed" if summary["exact_proxy_mt5_parity"] else "failed", rel(PROXY_MT5_ATTRIBUTION), "proxy-MT5 exact parity(프록시-MT5 정확 동등성)를 확인했다."),
            gate_row("mt5_negative_collapse_recorded", "passed" if summary["mt5_negative"] else "failed", rel(RESULT_JUDGMENT_MATRIX), "MT5 negative collapse(MT5 음성 붕괴)를 기록했다."),
            gate_row("execution_shape_attribution_recorded", "passed" if exists(PROXY_MT5_ATTRIBUTION) else "failed", rel(PROXY_MT5_ATTRIBUTION), "실패 원인을 parity(동등성)가 아니라 execution shape(실행 형태)로 좁혔다."),
            gate_row("failure_memory_written", "passed" if exists(FAILURE_MEMORY_AND_NEXT_SEED) else "failed", rel(FAILURE_MEMORY_AND_NEXT_SEED), "failure memory(실패 기억)를 다음 공격 탐색 제약으로 바꿨다."),
            gate_row("tier_pair_record_written", "passed" if exists(TIER_PAIR_RECORD) and len(read_csv(TIER_PAIR_RECORD)) == 3 else "failed", rel(TIER_PAIR_RECORD), "Tier A/B paired record(티어 A/B 쌍 기록)를 남겼다."),
            gate_row("next_exploration_queue_written", "passed" if exists(NEXT_QUEUE) else "failed", rel(NEXT_QUEUE), "다음 design queue(설계 대기열)를 열었다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(FINAL_DECISION), "selection/forward/runtime authority/Goal(선택/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": display_path(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_RECEIPT, {**base, "exact_proxy_mt5_parity": summary["exact_proxy_mt5_parity"], "matched_rows": summary["matched_rows"], "mismatch_rows": summary["mismatch_rows"], "runtime_claim_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)"})
    write_json(BACKTEST_FORENSICS_RECEIPT, {**base, "tester_identity": rel(ja.RUNTIME_IDENTITY), "report_identity": rel(ja.STRATEGY_TESTER_REPORTS), "trade_evidence": {"net_profit": summary["mt5_net_profit"], "profit_factor": summary["mt5_profit_factor"], "trade_count": summary["mt5_trade_count"], "drawdown": summary["mt5_max_drawdown_amount"]}, "backtest_judgment": "negative_runtime_probe(음성 런타임 탐침)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "proxy_mt5_attribution": rel(PROXY_MT5_ATTRIBUTION), "result_judgment_matrix": rel(RESULT_JUDGMENT_MATRIX), "positive_clue": "exact_parity_handoff_valid(정확 동등성 인계 유효)", "failure": "mt5_negative_execution_shape_collapse(MT5 음성 실행 형태 붕괴)", "mt5_net_profit": summary["mt5_net_profit"], "mt5_profit_factor": summary["mt5_profit_factor"], "mt5_expectancy": summary["mt5_expectancy"], "mt5_recovery_factor": summary["mt5_recovery_factor"]})
    write_json(JUDGMENT_RECEIPT, {**base, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates)), "result_class": "proxy_positive_mt5_negative_operating_ineligible"})
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 해시 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "forward_passed": "not_claimed", "forward_failed": "not_claimed", "goal_achieve": "not_claimed", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed"})


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        **dict(summary),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JB Positive Low-Edge Expansion MT5 Runtime Probe Review(run337JB 양성 저마진 확장 MT5 런타임 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- exact_proxy_mt5_parity(정확 프록시-MT5 동등성): `{final['exact_proxy_mt5_parity']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- proxy_net_log_return(프록시 순수익 로그수익): `{final['proxy_net_log_return']}`
- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- mt5_expectancy(MT5 기대값): `{final['mt5_expectancy']}`
- mt5_recovery_factor(MT5 회복 계수): `{final['mt5_recovery_factor']}`
- mt5_trade_count(MT5 거래수): `{final['mt5_trade_count']}`

## Action(행동)

JA MT5 runtime probe(JA MT5 런타임 탐침)를 review(검토)했다.
Effect(효과): proxy-positive(프록시 양성)가 MT5(메타트레이더5)에서는 negative collapse(음성 붕괴)였음을 운영 부적격으로 분리했다.

## Attribution(귀속)

ONNX parity(ONNX 동등성)와 feature handoff(피처 인계)는 닫혔다. 실패 축은 execution shape(실행 형태), cost exposure(비용 노출), lifecycle exit(생명주기 청산), signal density(신호 밀도)다.

## Boundary(경계)

Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

## Next(다음)

`{NEXT_RUN_ID}`에서 entry throttle(진입 제한), long-side filter(롱 필터), lifecycle exit(생명주기 청산), cost-buffer label(비용 버퍼 라벨), MT5-PnL-shaped proxy(MT5 손익형 프록시)를 설계한다.
"""
    decision = f"""# {TODAY} Stage337JB Decision(337JB 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_REVIEW)}`, `{rel(PROXY_MT5_ATTRIBUTION)}`, `{rel(RESULT_JUDGMENT_MATRIX)}`

Action(행동): proxy-positive exact-parity(프록시 양성 정확 동등성) 결과를 MT5 negative collapse(MT5 음성 붕괴)로 판정했다.
Effect(효과): 실패를 폐기하지 않고 다음 offensive exploration(공격 탐색)의 제약과 씨앗으로 넘긴다.

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

JB review(JB 검토)는 parity(동등성)는 보존하고 runtime negative collapse(런타임 음성 붕괴)를 다음 설계 제약으로 넘겼다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선택 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['primary_model_id']}`
- runtime_probe_judgment(런타임 탐침 판정): `proxy_positive_mt5_negative_operating_ineligible(프록시 양성 MT5 음성 운영 부적격)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 음성 MT5 결과를 선택 또는 운영 승격으로 오해하지 않게 한다.
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

    marker = f"run337JB {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JB MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- mt5_recovery_factor(MT5 회복 계수): `{final['mt5_recovery_factor']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): exact parity(정확 동등성)는 보존하고 MT5 negative collapse(MT5 음성 붕괴)를 다음 설계 제약으로 남겼다.
""",
    )
    changelog_entry = f"""## {TODAY} run337JB MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- action(행동): JA MT5 runtime probe(JA MT5 런타임 탐침)를 review(검토)했다.
- effect(효과): matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`, MT5 net profit(순수익) `{final['mt5_net_profit']}`, PF(수익 팩터) `{final['mt5_profit_factor']}`를 proxy-positive MT5-negative(프록시 양성 MT5 음성)으로 기록했다.
- boundary(경계): selected model(선택 모델), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base_row = {
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
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    rows = [
        {
            **base_row,
            "view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_review",
            "candidate_model_id": final["primary_model_id"],
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "expectancy": final["mt5_expectancy"],
            "drawdown": final["mt5_max_drawdown_amount"],
            "recovery_factor": final["mt5_recovery_factor"],
            "trade_count": final["mt5_trade_count"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "result_status": JUDGMENT,
        },
        {
            **base_row,
            "view": "Tier B fallback used(Tier B 대체 사용)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base_row,
            "view": "actual routed total(실제 라우팅 전체)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    runtime_review, attribution, judgment_matrix, failure_memory, tier_record, queue, summary = build_review()
    write_csv(RUNTIME_REVIEW, runtime_review)
    write_csv(PROXY_MT5_ATTRIBUTION, attribution)
    write_csv(RESULT_JUDGMENT_MATRIX, judgment_matrix)
    write_csv(FAILURE_MEMORY_AND_NEXT_SEED, failure_memory)
    write_csv(TIER_PAIR_RECORD, tier_record)
    write_csv(NEXT_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JB gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "judgment": JUDGMENT,
                "exact_proxy_mt5_parity": final["exact_proxy_mt5_parity"],
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
                "mt5_recovery_factor": final["mt5_recovery_factor"],
                "mt5_trade_count": final["mt5_trade_count"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

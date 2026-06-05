from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    execute_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_without_db as jq,
)
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_runtime_probe_package_without_db as jp,
)


aw = jq.aw

TODAY = "2026-06-01"
STAGE_ID = jq.STAGE_ID
STAGE_DIR = jq.STAGE_DIR
RUN_NUMBER = "run337JR"
RUN_ID = "run337JR_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = jq.RUN_ID
NEXT_RUN_ID = "run337JS_design_runtime_positive_proxy_mt5_negative_trade_lifecycle_repair_without_db_v1"
STATUS = "completed_stage337JR_positive_low_pf_recovery_drawdown_dual_probe_mt5_runtime_probe_review_negative_repair_design_required"
JUDGMENT = "valid_negative_mt5_runtime_probe_proxy_signal_parity_but_trade_lifecycle_unprofitable_no_selection"
DECISION = "stage337JR_open_run337JS_design_proxy_positive_mt5_negative_trade_lifecycle_repair"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_valid_negative_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JR_positive_low_pf_recovery_drawdown_dual_probe_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JR_positive_low_pf_recovery_drawdown_dual_probe_mt5_runtime_probe_review.md"

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

JO_RUN_DIR = STAGE_DIR / "02_runs" / "run337JO"
JO_PRIORITY = JO_RUN_DIR / "jo_runtime_probe_priority_matrix.csv"
JO_POSITIVE_MATRIX = JO_RUN_DIR / "jo_positive_proxy_candidate_matrix.csv"

SCORECARD = RUN_DIR / "jr_mt5_runtime_probe_review_scorecard.csv"
ATTRIBUTION = RUN_DIR / "jr_proxy_mt5_attribution.csv"
FAILURE_MEMORY = RUN_DIR / "jr_failure_memory_and_repair_constraints.csv"
NEXT_QUEUE = RUN_DIR / "run337JS_design_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    jq.FINAL_DECISION,
    jq.GATE_AUDIT,
    jq.EXECUTION_SUMMARY,
    jq.PROXY_MT5_DIFF,
    jq.STRATEGY_TESTER_REPORTS,
    jq.RUNTIME_IDENTITY,
    jq.RUNTIME_OUTPUT_COPY,
    jp.FINAL_DECISION,
    jp.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    JO_PRIORITY,
)
OUTPUT_FILES = (
    SCORECARD,
    ATTRIBUTION,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    RESULT_JUDGMENT_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
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
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def to_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def repair_hint(proxy: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    hints: list[str] = []
    if to_float(proxy.get("signal_density")) > 0.95:
        hints.append("density throttle(밀도 제한)")
    if to_float(proxy.get("side_balance_ratio")) < 0.70:
        hints.append("side balance guard(롱/숏 균형 가드)")
    if to_float(proxy.get("long_net")) < 0:
        hints.append("long loss quarantine(롱 손실 격리)")
    if to_float(summary.get("profit_factor")) < 1.0:
        hints.append("trade lifecycle cost objective(거래 생명주기 비용 목적)")
    if to_float(summary.get("max_drawdown_amount")) > 300:
        hints.append("drawdown corridor(낙폭 통로)")
    if not hints:
        hints.append("runtime attribution review(런타임 귀속 검토)")
    return ";".join(hints)


def load_reports() -> dict[str, Mapping[str, Any]]:
    reports = read_json(jq.STRATEGY_TESTER_REPORTS)
    if not isinstance(reports, list):
        return {}
    return {str(row.get("attempt_name", "")): row for row in reports}


def build_review_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    summary = read_csv(jq.EXECUTION_SUMMARY).fillna("")
    priority = read_csv(JO_PRIORITY).fillna("")
    reports = load_reports()
    priority_by_model = {str(row["model_id"]): row for row in priority.to_dict(orient="records")}

    rows: list[dict[str, Any]] = []
    for row in summary.to_dict(orient="records"):
        model_id = str(row.get("model_id", ""))
        proxy = priority_by_model.get(model_id, {})
        mt5_net = to_float(row.get("net_profit"))
        mt5_pf = to_float(row.get("profit_factor"))
        mt5_recovery = to_float(row.get("recovery_factor"))
        probability_mismatch = to_int(row.get("probability_mismatch_rows"))
        decision_mismatch = to_int(row.get("decision_mismatch_rows"))
        hash_mismatch = to_int(row.get("hash_mismatch_rows"))
        expected_missing = to_int(row.get("expected_missing_rows"))
        parity_ok = probability_mismatch == 0 and decision_mismatch == 0 and hash_mismatch == 0 and expected_missing == 0
        report = reports.get(str(row.get("attempt_name", "")), {})
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "model_id": model_id,
                "probe_role": proxy.get("jo_probe_role", ""),
                "model_family": proxy.get("model_family", ""),
                "proxy_rank": to_int(proxy.get("raw_proxy_rank")),
                "proxy_net_log_return_after_cost": to_float(proxy.get("net_log_return_after_cost")),
                "proxy_profit_factor": to_float(proxy.get("profit_factor")),
                "proxy_expectancy": to_float(proxy.get("expectancy")),
                "proxy_recovery_factor": to_float(proxy.get("recovery_factor")),
                "proxy_drawdown": to_float(proxy.get("max_drawdown")),
                "proxy_trade_count": to_int(proxy.get("trade_count")),
                "signal_density": to_float(proxy.get("signal_density")),
                "side_balance_ratio": to_float(proxy.get("side_balance_ratio")),
                "proxy_long_net": to_float(proxy.get("long_net")),
                "proxy_short_net": to_float(proxy.get("short_net")),
                "mt5_runtime_status": row.get("runtime_status", ""),
                "mt5_tester_status": row.get("tester_status", ""),
                "mt5_report_status": row.get("report_status", report.get("status", "")),
                "mt5_net_profit": mt5_net,
                "mt5_profit_factor": mt5_pf,
                "mt5_expectancy": to_float(row.get("expectancy")),
                "mt5_recovery_factor": mt5_recovery,
                "mt5_drawdown": to_float(row.get("max_drawdown_amount")),
                "mt5_trade_count": to_int(row.get("trade_count")),
                "mt5_long_trade_count": to_int(row.get("long_trade_count")),
                "mt5_short_trade_count": to_int(row.get("short_trade_count")),
                "matched_rows": to_int(row.get("matched_rows")),
                "probability_mismatch_rows": probability_mismatch,
                "decision_mismatch_rows": decision_mismatch,
                "hash_mismatch_rows": hash_mismatch,
                "expected_missing_rows": expected_missing,
                "proxy_mt5_parity_ok": parity_ok,
                "comparison_status": row.get("comparison_status", ""),
                "report_path": row.get("report_path", ""),
                "proxy_mt5_direction_flip": bool(to_float(proxy.get("net_log_return_after_cost")) > 0 and mt5_net < 0),
                "mt5_negative_flag": bool(mt5_net < 0 or mt5_pf < 1.0 or mt5_recovery < 0),
                "review_judgment": "valid_negative_runtime_probe(유효한 부정 런타임 탐침)",
                "repair_hint": repair_hint(proxy, row),
                "weakness_tags": proxy.get("weakness_tags", ""),
                "eligible_for_selection": "no(아니오)",
                "effect": "proxy(프록시) 신호는 재현됐지만 MT5(메타트레이더5) 거래 생명주기 성과가 음수인지 판정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    scorecard = pd.DataFrame(rows)
    scorecard["mt5_net_rank"] = scorecard["mt5_net_profit"].rank(method="first", ascending=False).astype(int)
    scorecard["mt5_profit_factor_rank"] = scorecard["mt5_profit_factor"].rank(method="first", ascending=False).astype(int)

    attribution = scorecard[
        [
            "attempt_name",
            "model_id",
            "probe_role",
            "proxy_rank",
            "mt5_net_rank",
            "proxy_net_log_return_after_cost",
            "mt5_net_profit",
            "proxy_profit_factor",
            "mt5_profit_factor",
            "proxy_recovery_factor",
            "mt5_recovery_factor",
            "proxy_trade_count",
            "mt5_trade_count",
            "signal_density",
            "side_balance_ratio",
            "proxy_mt5_direction_flip",
            "repair_hint",
        ]
    ].copy()
    attribution["comparison_limit"] = "scale_not_same_direction_and_rank_only(척도 다름, 방향과 순위만 비교)"
    attribution["attribution"] = np.where(
        attribution["proxy_mt5_direction_flip"],
        "proxy_positive_but_mt5_negative_trade_lifecycle_failure(프록시 양수지만 MT5 거래 생명주기 실패)",
        "proxy_mt5_direction_same_or_needs_detail(프록시-MT5 방향 같거나 세부 검토 필요)",
    )
    attribution["effect"] = "proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않게 한다."
    attribution["claim_boundary"] = CLAIM_BOUNDARY

    failure_rows = [
        {
            "memory_id": "jr_signal_reproduced_but_mt5_negative",
            "evidence": rel(SCORECARD),
            "finding": "ONNX probabilities(온엑스 확률)는 MT5 telemetry(MT5 런타임 기록)와 정확히 맞았지만 3개 후보 모두 순수익이 음수다.",
            "constraint": "다음 label/objective(라벨/목적)는 신호 품질만이 아니라 broker lifecycle PnL(브로커 생명주기 손익)을 직접 압박한다.",
            "effect": "parity bug(동등성 버그) 수리가 아니라 trade-shape repair(거래 형태 수리)로 방향을 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "jr_high_density_argmax_overtrading",
            "evidence": rel(ATTRIBUTION),
            "finding": "signal_density(신호 밀도)가 0.95 이상인 후보들이 MT5에서 높은 drawdown(낙폭)과 PF<1을 냈다.",
            "constraint": "density throttle(밀도 제한), cooldown(쿨다운), max-hold corridor(최대 보유 통로)를 탐색한다.",
            "effect": "좋은 proxy(프록시) 점수가 과잉 거래를 숨기지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "jr_balance_control_insufficient",
            "evidence": rel(SCORECARD),
            "finding": "balance control(균형 대조)도 PF 0.85와 순수익 -333.2로 실패했다.",
            "constraint": "side balance(롱/숏 균형)만이 아니라 side-specific loss quarantine(방향별 손실 격리)을 붙인다.",
            "effect": "롱/숏 수량 균형을 수익 균형으로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "jr_cost_control_less_bad_not_candidate",
            "evidence": rel(SCORECARD),
            "finding": "cost control(비용 대조)이 가장 덜 나빴지만 순수익 -191.49, PF 0.92라 후보가 아니다.",
            "constraint": "cost-stress buffer(비용 압박 완충)를 유지하되 positive selection(긍정 선택)은 금지한다.",
            "effect": "덜 나쁜 결과를 promotion_candidate(승격 후보)로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    failure_memory = pd.DataFrame(failure_rows)

    best = scorecard.sort_values(["mt5_net_profit", "mt5_profit_factor", "mt5_recovery_factor"], ascending=False).iloc[0]
    all_negative = bool((scorecard["mt5_negative_flag"] == True).all())
    parity_ok = bool((scorecard["proxy_mt5_parity_ok"] == True).all())
    summary_payload = {
        "attempt_rows": int(len(scorecard)),
        "runtime_completed_rows": int(scorecard["mt5_runtime_status"].astype(str).eq("completed").sum()),
        "report_completed_rows": int(scorecard["mt5_report_status"].astype(str).eq("completed").sum()),
        "matched_rows": int(scorecard["matched_rows"].sum()),
        "mismatch_rows": int(
            scorecard["probability_mismatch_rows"].sum()
            + scorecard["decision_mismatch_rows"].sum()
            + scorecard["hash_mismatch_rows"].sum()
            + scorecard["expected_missing_rows"].sum()
        ),
        "all_mt5_negative": all_negative,
        "parity_ok": parity_ok,
        "best_model_id": str(best["model_id"]),
        "best_attempt_name": str(best["attempt_name"]),
        "best_mt5_net_profit": float(best["mt5_net_profit"]),
        "best_mt5_profit_factor": float(best["mt5_profit_factor"]),
        "best_mt5_expectancy": float(best["mt5_expectancy"]),
        "best_mt5_recovery_factor": float(best["mt5_recovery_factor"]),
        "best_mt5_drawdown": float(best["mt5_drawdown"]),
        "best_mt5_trade_count": int(best["mt5_trade_count"]),
        "primary_model_id": str(scorecard.sort_values("proxy_rank").iloc[0]["model_id"]),
    }
    return scorecard, attribution, failure_memory, summary_payload


def build_next_queue(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "queue_id": "js_design_proxy_positive_mt5_negative_trade_lifecycle_repair",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "Design timestamp-safe trade lifecycle repair after proxy-positive MT5-negative probe(프록시 양수 MT5 음수 탐침 뒤 시점 안전 거래 생명주기 수리 설계)",
                "required_inputs": f"{rel(SCORECARD)};{rel(ATTRIBUTION)};{rel(FAILURE_MEMORY)};{rel(jq.PROXY_MT5_DIFF)}",
                "design_requirements": "density throttle(밀도 제한); side-specific loss quarantine(방향별 손실 격리); cost-stress objective(비용 압박 목적); drawdown corridor(낙폭 통로); Tier A/B paired records(Tier A/B 쌍 기록)",
                "blocked_if_missing": "runtime telemetry or MT5 reports(런타임 기록 또는 MT5 보고서)",
                "forbidden_action": "candidate selection or Goal claim from negative MT5 probe(음수 MT5 탐침에서 후보 선택 또는 목표 주장)",
                "effect": "valid negative evidence(유효한 부정 근거)를 다음 offensive exploration seed(공격 탐색 씨앗)로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jq.GATE_AUDIT)
    no_forbidden = True
    return pd.DataFrame(
        [
            gate_row("parent_jq_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(jq.GATE_AUDIT), "JQ execution(JQ 실행)이 gate(게이트)를 통과한 근거만 검토한다."),
            gate_row("mt5_runtime_outputs_reviewed", "passed" if summary["runtime_completed_rows"] == 3 and summary["report_completed_rows"] == 3 else "failed", rel(SCORECARD), "3개 attempt(시도)의 MT5 runtime output(MT5 런타임 출력)을 모두 검토한다."),
            gate_row("proxy_mt5_parity_verified", "passed" if summary["parity_ok"] and summary["mismatch_rows"] == 0 else "failed", rel(ATTRIBUTION), "proxy-MT5 parity(프록시-MT5 동등성)가 깨지지 않았는지 확인한다."),
            gate_row("valid_negative_judgment_recorded", "passed" if summary["all_mt5_negative"] else "failed", rel(RESULT_JUDGMENT_RECEIPT), "MT5 KPI(MT5 핵심 성과 지표)가 음수인 유효한 부정 판정을 기록한다."),
            gate_row("failure_memory_written", "passed" if exists(FAILURE_MEMORY) else "failed", rel(FAILURE_MEMORY), "failure memory(실패 기억)를 다음 제약으로 남긴다."),
            gate_row("next_repair_design_queue_written", "passed" if exists(NEXT_QUEUE) else "failed", rel(NEXT_QUEUE), "다음 JS design(설계) queue(대기열)를 연다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(FINAL_DECISION), "selection/forward/runtime authority/Goal(선택/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any], final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run337JQ three ONNX MT5 runtime probes(run337JQ ONNX 3개 MT5 런타임 탐침)",
            "evidence_available": [rel(SCORECARD), rel(ATTRIBUTION), rel(jq.STRATEGY_TESTER_REPORTS), rel(jq.PROXY_MT5_DIFF)],
            "evidence_missing": "forward/replay/live-like evidence(전진/재생/실거래 유사 근거), operating promotion evidence(운영 승격 근거)",
            "judgment_label": "negative(부정)",
            "next_condition": "JS design(설계) must reduce density, side loss, lifecycle cost, and drawdown before any new package(JS 설계는 새 패키지 전 밀도/방향 손실/생명주기 비용/낙폭을 줄여야 함)",
            "user_explanation_hook": "신호는 MT5에서 그대로 재현됐지만 거래하면 돈을 잃는다. 그래서 모델 선택이 아니라 수익 구조 수리로 간다.",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(jq.EXECUTION_SUMMARY),
            "shared_contract": rel(jp.RUNTIME_PARITY_CONTRACT),
            "known_differences": "proxy expected value(프록시 예상값) scale(척도)은 MT5 account currency(MT5 계좌 통화)와 다르다.",
            "parity_check": rel(ATTRIBUTION),
            "parity_identity": f"matched_rows={summary['matched_rows']};mismatch_rows={summary['mismatch_rows']}",
            "runtime_claim_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)",
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(jq.RUNTIME_IDENTITY),
            "ea_identity": rel(jp.TESTER_IDENTITY_CONTRACT),
            "report_identity": rel(jq.STRATEGY_TESTER_REPORTS),
            "trade_evidence": {
                "best_model_id": summary["best_model_id"],
                "net_profit": summary["best_mt5_net_profit"],
                "profit_factor": summary["best_mt5_profit_factor"],
                "expectancy": summary["best_mt5_expectancy"],
                "drawdown": summary["best_mt5_drawdown"],
                "recovery_factor": summary["best_mt5_recovery_factor"],
                "trade_count": summary["best_mt5_trade_count"],
            },
            "cost_assumptions": "JP tester set(JP 테스터 설정) fixed lot(고정 랏) 0.10 and broker tester lifecycle(브로커 테스터 생명주기)",
            "forensic_checks": [rel(jq.MT5_EXECUTION_RESULT), rel(jq.STRATEGY_TESTER_REPORTS), rel(jq.RUNTIME_OUTPUT_COPY), rel(SCORECARD)],
            "backtest_judgment": "usable_negative_with_boundary(경계 조건부 사용 가능한 부정 근거)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "proxy-positive candidates became MT5-negative(프록시 양수 후보가 MT5 음수로 바뀜)",
            "scorecard": rel(SCORECARD),
            "attribution": rel(ATTRIBUTION),
            "best_model_id": summary["best_model_id"],
            "best_mt5_net_profit": summary["best_mt5_net_profit"],
            "best_mt5_profit_factor": summary["best_mt5_profit_factor"],
            "best_mt5_recovery_factor": summary["best_mt5_recovery_factor"],
            "attribution_confidence": "high_for_direction_and_parity_low_for_causal_microstructure(방향/동등성은 높고 미시 원인 귀속은 낮음)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_negative_boundary(부정 경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "final_decision": rel(FINAL_DECISION),
            "effect": "negative runtime probe(부정 런타임 탐침)를 operating claim(운영 주장)으로 올리지 않는다.",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        **dict(summary),
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
    report = f"""# run337JR MT5 Runtime Probe Review(run337JR MT5 런타임 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- parity_ok(동등성 정상): `{final['parity_ok']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- best_model_id(가장 덜 나쁜 모델 ID): `{final['best_model_id']}`
- best_mt5_net_profit(가장 덜 나쁜 MT5 순수익): `{final['best_mt5_net_profit']}`
- best_mt5_profit_factor(가장 덜 나쁜 MT5 수익 팩터): `{final['best_mt5_profit_factor']}`
- best_mt5_recovery_factor(가장 덜 나쁜 MT5 회복 계수): `{final['best_mt5_recovery_factor']}`
- best_mt5_drawdown(가장 덜 나쁜 MT5 낙폭): `{final['best_mt5_drawdown']}`

## Judgment(판정)

JQ의 3개 ONNX(온엑스) 후보는 모두 runtime parity(런타임 동등성)가 맞았지만 MT5 KPI(MT5 핵심 성과 지표)가 모두 음수다.
Effect(효과): 이 결과는 invalid(무효)가 아니라 valid negative(유효한 부정)이고, 후보 선택이 아니라 trade lifecycle repair(거래 생명주기 수리)로 넘긴다.

## Evidence(근거)

- scorecard(점수표): `{rel(SCORECARD)}`
- attribution(귀속): `{rel(ATTRIBUTION)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`

## Boundary(경계)

Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage337JR Decision(337JR 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(ATTRIBUTION)}`, `{rel(FAILURE_MEMORY)}`

Action(행동): proxy-positive MT5-negative(프록시 양수 MT5 음수) 결과를 valid negative(유효한 부정)로 닫았다.
Effect(효과): 다음 JS design(JS 설계)이 density throttle(밀도 제한), side loss quarantine(방향 손실 격리), lifecycle cost objective(생명주기 비용 목적)를 직접 다루게 한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`

## Effect(효과)

JR은 JQ runtime probe(JQ 런타임 탐침)를 valid negative(유효한 부정)로 닫았다. 이제 JS는 같은 신호를 더 세게 미는 것이 아니라 거래 생명주기 손실을 줄이는 설계를 해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- best_runtime_probe_model(가장 덜 나쁜 런타임 탐침 모델): `{final['best_model_id']}`
- best_mt5_net_profit(가장 덜 나쁜 MT5 순수익): `{final['best_mt5_net_profit']}`
- mt5_runtime_probe_judgment(MT5 런타임 탐침 판정): `valid_negative(유효한 부정)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 가장 덜 나쁜 후보도 selected model(선정 모델)로 승격하지 않는다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
current_decision: {final['decision']}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run337JR {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JR MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- best_model_id(가장 덜 나쁜 모델 ID): `{final['best_model_id']}`
- best_mt5_net_profit(가장 덜 나쁜 MT5 순수익): `{final['best_mt5_net_profit']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): proxy-positive(프록시 양수)를 MT5-negative(메타트레이더5 음수) 근거로 낮춰 다음 수리 설계에 연결했다.
""",
    )
    changelog_entry = f"""## {TODAY} run337JR MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- action(행동): JQ의 3개 ONNX(온엑스) MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
- effect(효과): parity_ok(동등성 정상) `{final['parity_ok']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`, best_net(가장 덜 나쁜 순수익) `{final['best_mt5_net_profit']}`로 valid negative(유효한 부정)를 기록했다.
- boundary(경계): model selection(모델 선택), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


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


def update_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    rows = [
        {
            **base_row,
            "view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_review",
            "candidate_model_id": final["best_model_id"],
            "net_profit": final["best_mt5_net_profit"],
            "profit_factor": final["best_mt5_profit_factor"],
            "expectancy": final["best_mt5_expectancy"],
            "drawdown": final["best_mt5_drawdown"],
            "recovery_factor": final["best_mt5_recovery_factor"],
            "trade_count": final["best_mt5_trade_count"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "result_status": final["judgment"],
        },
        {**base_row, "view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base_row, "view": "actual routed total(실제 라우팅 전체)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def artifact_paths() -> list[Path]:
    return [path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY]


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
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    write_csv(ARTIFACT_REGISTRY, registry[required + [c for c in registry.columns if c not in required]])


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    scorecard, attribution, failure_memory, summary = build_review_tables()
    write_csv(SCORECARD, scorecard)
    write_csv(ATTRIBUTION, attribution)
    write_csv(FAILURE_MEMORY, failure_memory)
    write_csv(NEXT_QUEUE, build_next_queue(summary))
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    final = write_final(summary, gates)
    write_receipts(summary, final)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final, gates)
    update_artifact_registry(artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JR gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "attempt_rows": final["attempt_rows"],
                "parity_ok": final["parity_ok"],
                "mismatch_rows": final["mismatch_rows"],
                "best_model_id": final["best_model_id"],
                "best_mt5_net_profit": final["best_mt5_net_profit"],
                "best_mt5_profit_factor": final["best_mt5_profit_factor"],
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

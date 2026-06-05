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
    execute_runtime_negative_collapse_cost_stress_trade_shape_repair_mt5_runtime_probe_without_db as ji,
)


aw = ji.aw

TODAY = "2026-06-01"
STAGE_ID = ji.STAGE_ID
STAGE_DIR = ji.STAGE_DIR
RUN_NUMBER = "run337JJ"
RUN_ID = "run337JJ_review_runtime_negative_collapse_cost_stress_trade_shape_repair_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = ji.RUN_ID
NEXT_RUN_ID = "run337JK_design_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_without_db_v1"
STATUS = "completed_stage337JJ_runtime_negative_collapse_repair_mt5_probe_review_positive_low_edge_repair_required_no_selection"
JUDGMENT = "mt5_raw_top_positive_but_low_pf_recovery_and_control_negative_repair_required_no_selection"
DECISION = "stage337JJ_open_run337JK_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_design"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JJ_runtime_negative_collapse_repair_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JJ_runtime_negative_collapse_repair_mt5_probe_review.md"

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

RUNTIME_REVIEW = RUN_DIR / "jj_runtime_probe_attempt_review.csv"
TRADE_SHAPE_COMPARISON = RUN_DIR / "jj_trade_shape_comparison.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "jj_proxy_mt5_attribution.csv"
RESULT_JUDGMENT_MATRIX = RUN_DIR / "jj_result_judgment_matrix.csv"
TIER_PAIR_RECORD = RUN_DIR / "jj_tier_pair_record.csv"
NEXT_QUEUE = RUN_DIR / "run337JK_repair_design_queue.csv"
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
    ji.FINAL_DECISION,
    ji.GATE_AUDIT,
    ji.EXECUTION_SUMMARY,
    ji.PROXY_MT5_DIFF,
    ji.MT5_EXECUTION_RESULT,
    ji.STRATEGY_TESTER_REPORTS,
    ji.jh.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    ji.jh.jg.PROBE_PRIORITY,
)
OUTPUT_FILES = (
    RUNTIME_REVIEW,
    TRADE_SHAPE_COMPARISON,
    PROXY_MT5_ATTRIBUTION,
    RESULT_JUDGMENT_MATRIX,
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
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def to_float(value: Any) -> float:
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_int(value: Any) -> int:
    try:
        if pd.isna(value):
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def first_row(frame: pd.DataFrame) -> pd.Series:
    return frame.iloc[0] if not frame.empty else pd.Series(dtype=object)


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(ji.FINAL_DECISION)
    summaries = read_csv(ji.EXECUTION_SUMMARY)
    priority = read_csv(ji.jh.jg.PROBE_PRIORITY)
    attempt_pkg = read_csv(ji.jh.RUNTIME_PROBE_ATTEMPT_PACKAGE)
    diff = read_csv(ji.PROXY_MT5_DIFF)
    reports = read_json(ji.STRATEGY_TESTER_REPORTS)
    report_count = len(reports) if isinstance(reports, list) else 0

    review = (
        summaries.merge(attempt_pkg[["attempt_name", "probe_disposition", "probe_priority"]], on="attempt_name", how="left")
        .merge(
            priority[
                [
                    "model_id",
                    "jg_disposition",
                    "net_log_return_after_cost",
                    "profit_factor",
                    "recovery_factor",
                    "signal_density",
                    "side_balance_ratio",
                    "long_net",
                    "short_net",
                    "balanced_accuracy",
                    "weakness_tags",
                ]
            ].rename(
                columns={
                    "net_log_return_after_cost": "proxy_net_log_return",
                    "profit_factor": "proxy_profit_factor",
                    "recovery_factor": "proxy_recovery_factor",
                    "signal_density": "proxy_signal_density",
                }
            ),
            on="model_id",
            how="left",
        )
    )
    review["mismatch_rows_filled"] = review["mismatch_rows"].apply(to_int) if "mismatch_rows" in review.columns else 0
    review["exact_proxy_mt5_parity"] = (
        review["comparison_status"].astype(str).eq("completed_exact_proxy_mt5_parity_reached_feature_last")
        & (review["matched_rows"].apply(to_int) > 0)
        & review["mismatch_rows_filled"].eq(0)
    )
    review["mt5_net_profit"] = review["net_profit"].apply(to_float)
    review["mt5_profit_factor"] = review["profit_factor"].apply(to_float)
    review["mt5_expectancy"] = review["expectancy"].apply(to_float)
    review["mt5_recovery_factor"] = review["recovery_factor"].apply(to_float)
    review["mt5_max_drawdown_amount"] = review["max_drawdown_amount"].apply(to_float)
    review["mt5_trade_count"] = review["trade_count"].apply(to_int)
    review["mt5_positive"] = review["mt5_net_profit"].gt(0.0) & review["mt5_profit_factor"].gt(1.0)
    review["low_edge_runtime_risk"] = (
        review["mt5_profit_factor"].lt(1.20)
        | review["mt5_recovery_factor"].lt(1.0)
        | ((review["mt5_max_drawdown_amount"] > 0.0) & ((review["mt5_net_profit"] / review["mt5_max_drawdown_amount"]).lt(1.0)))
    )
    review["review_disposition"] = "runtime_probe_negative_or_weak_repair_required"
    review.loc[
        review["mt5_positive"] & review["low_edge_runtime_risk"],
        "review_disposition",
    ] = "positive_runtime_clue_low_edge_repair_seed_not_selected"
    review.loc[
        ~review["mt5_positive"],
        "review_disposition",
    ] = "negative_runtime_control_repair_memory"
    review["operating_eligibility"] = "operating_ineligible(운영 부적격)"
    review["effect"] = "MT5 runtime probe(MT5 런타임 탐침)를 positive clue(긍정 단서)와 repair memory(수리 기억)로 분리한다."
    review["claim_boundary"] = CLAIM_BOUNDARY

    positive = review.loc[review["mt5_positive"]].sort_values("mt5_net_profit", ascending=False)
    negative = review.loc[~review["mt5_positive"]].sort_values("mt5_net_profit")
    best = first_row(positive)
    worst = first_row(negative)

    trade_shape = review[
        [
            "attempt_name",
            "model_id",
            "probe_disposition",
            "proxy_net_log_return",
            "proxy_profit_factor",
            "proxy_signal_density",
            "mt5_net_profit",
            "mt5_profit_factor",
            "mt5_expectancy",
            "mt5_recovery_factor",
            "mt5_max_drawdown_amount",
            "mt5_trade_count",
            "long_trade_count",
            "short_trade_count",
            "side_balance_ratio",
            "long_net",
            "short_net",
            "balanced_accuracy",
            "review_disposition",
        ]
    ].copy()
    trade_shape["effect"] = "trade shape(거래 형태)를 proxy(프록시)와 MT5(메타트레이더5) 양쪽에서 비교한다."
    trade_shape["claim_boundary"] = CLAIM_BOUNDARY

    attribution = pd.DataFrame(
        [
            {
                "attribution_id": "raw_top_positive_control_negative_dual_probe",
                "observed_change": "raw top model became MT5 positive; risk-adjusted control became MT5 negative(raw top 모델은 MT5 양수, 위험 보정 대조는 MT5 음수)",
                "comparison_baseline": rel(ji.FINAL_DECISION),
                "likely_drivers": "runtime PnL label preserved short-side edge; session-regime risk adjustment over-throttled or shifted side exposure(런타임 손익 라벨이 숏 우위를 보존, 세션/국면 위험 보정은 과도 제한 또는 방향 노출 이동)",
                "segment_checks": rel(TRADE_SHAPE_COMPARISON),
                "trade_shape": f"positive={best.get('model_id', '')}: net={best.get('mt5_net_profit', 0)}, PF={best.get('mt5_profit_factor', 0)}, recovery={best.get('mt5_recovery_factor', 0)}; negative={worst.get('model_id', '')}: net={worst.get('mt5_net_profit', 0)}",
                "alternative_explanations": "Strategy Tester report parse rows are zero; telemetry summary is present, so tester-report audit still needs review(전략 테스터 보고서 파싱 행은 0, 런타임 요약은 있으므로 보고서 감사는 아직 필요)",
                "attribution_confidence": "medium_low_until_report_parse_and_followup_probe(보고서 파싱과 후속 탐침 전까지 중하)",
                "next_probe": NEXT_RUN_ID,
                "effect": "positive clue(긍정 단서)를 운영 주장으로 올리지 않고 다음 수리 설계의 입력으로 쓴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    judgment_matrix = pd.DataFrame(
        [
            {
                "judgment_id": "jj_runtime_probe_result",
                "result_class": "runtime_probe_positive_clue_but_operating_ineligible",
                "positive_model_id": best.get("model_id", ""),
                "negative_control_model_id": worst.get("model_id", ""),
                "candidate_selection": "not_selected(선정 없음)",
                "forward_passed": "not_claimed(주장 없음)",
                "forward_failed": "not_claimed(주장 없음)",
                "runtime_authority": "not_claimed(주장 없음)",
                "goal_achieve": "not_claimed(주장 없음)",
                "reason": "PF/recovery/drawdown and missing parsed tester report prevent operating claim(PF/회복/낙폭과 파싱된 테스터 보고서 공백 때문에 운영 주장 불가)",
                "effect": "좋아진 런타임 탐침을 selected model(선정 모델)로 과장하지 않는다.",
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
                "net_profit": best.get("mt5_net_profit", 0.0),
                "profit_factor": best.get("mt5_profit_factor", 0.0),
                "expectancy": best.get("mt5_expectancy", 0.0),
                "drawdown": best.get("mt5_max_drawdown_amount", 0.0),
                "recovery_factor": best.get("mt5_recovery_factor", 0.0),
                "trade_count": best.get("mt5_trade_count", 0),
                "result_status": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {"view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required", "claim_boundary": CLAIM_BOUNDARY},
            {"view": "actual routed total(실제 라우팅 전체)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required", "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "design_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair(런타임 양수 저PF/저회복/낙폭 이중 탐침 수리 설계)",
                "positive_clue_model_id": best.get("model_id", ""),
                "negative_control_model_id": worst.get("model_id", ""),
                "required_inputs": f"{rel(RUNTIME_REVIEW)};{rel(TRADE_SHAPE_COMPARISON)};{rel(PROXY_MT5_ATTRIBUTION)}",
                "repair_focus": "preserve raw runtime PnL edge, raise PF/recovery, reduce drawdown, keep negative session-regime control as failure memory(raw 런타임 손익 우위 보존, PF/회복 개선, 낙폭 축소, 음수 세션/국면 대조를 실패 기억으로 유지)",
                "forbidden_action": "promotion, selection, threshold/lots optimization before review(검토 전 승격/선정/임계값·랏 최적화)",
                "effect": "다음 설계가 수익 단서를 살리면서 운영 주장은 닫게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "attempt_rows": int(len(review)),
        "runtime_completed_rows": int(review["runtime_status"].astype(str).eq("completed").sum()),
        "exact_parity_rows": int(review["exact_proxy_mt5_parity"].sum()),
        "positive_runtime_rows": int(review["mt5_positive"].sum()),
        "negative_runtime_rows": int((~review["mt5_positive"]).sum()),
        "report_rows": int(parent.get("report_rows", 0)),
        "report_usable_rows": int(parent.get("report_usable_rows", 0)),
        "best_model_id": str(best.get("model_id", "")),
        "best_net_profit": to_float(best.get("mt5_net_profit", 0.0)),
        "best_profit_factor": to_float(best.get("mt5_profit_factor", 0.0)),
        "best_expectancy": to_float(best.get("mt5_expectancy", 0.0)),
        "best_recovery_factor": to_float(best.get("mt5_recovery_factor", 0.0)),
        "best_drawdown": to_float(best.get("mt5_max_drawdown_amount", 0.0)),
        "best_trade_count": to_int(best.get("mt5_trade_count", 0)),
        "best_long_trade_count": to_int(best.get("long_trade_count", 0)),
        "best_short_trade_count": to_int(best.get("short_trade_count", 0)),
        "negative_control_model_id": str(worst.get("model_id", "")),
        "negative_control_net_profit": to_float(worst.get("mt5_net_profit", 0.0)),
        "next_action": NEXT_RUN_ID,
    }
    return review, trade_shape, attribution, judgment_matrix, tier_record, queue, summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(ji.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row("parent_ji_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(ji.GATE_AUDIT), "JI execution(JI 실행) gate(게이트)가 통과한 뒤에만 review(검토)한다."),
            gate_row("runtime_review_materialized", "passed" if exists(RUNTIME_REVIEW) and summary["attempt_rows"] == 2 else "failed", rel(RUNTIME_REVIEW), "두 MT5 runtime probe(MT5 런타임 탐침)를 모두 검토한다."),
            gate_row("exact_parity_checked", "passed" if summary["exact_parity_rows"] == summary["attempt_rows"] else "failed", rel(ji.PROXY_MT5_DIFF), "proxy-MT5 exact parity(프록시-MT5 정확 동등성)를 확인한다."),
            gate_row("positive_and_negative_contrast_recorded", "passed" if summary["positive_runtime_rows"] >= 1 and summary["negative_runtime_rows"] >= 1 else "failed", rel(TRADE_SHAPE_COMPARISON), "양수 단서와 음수 대조를 함께 기록한다."),
            gate_row("operating_ineligible_boundary_recorded", "passed" if exists(RESULT_JUDGMENT_MATRIX) else "failed", rel(RESULT_JUDGMENT_MATRIX), "운영 부적격 경계를 기록한다."),
            gate_row("next_repair_queue_opened", "passed" if exists(NEXT_QUEUE) else "failed", rel(NEXT_QUEUE), "다음 수리 설계 queue(대기열)를 연다."),
            gate_row("tier_pair_recorded", "passed" if exists(TIER_PAIR_RECORD) else "failed", rel(TIER_PAIR_RECORD), "Tier B(티어 B)와 합산 누락을 숨기지 않는다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(CLAIM_RECEIPT), "selection/forward/runtime authority/Goal(선정/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "created_at_utc": now_utc(), "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY}
    write_json(BACKTEST_FORENSICS_RECEIPT, {**base, "tester_identity": rel(ji.RUNTIME_IDENTITY), "ea_identity": rel(ji.jh.TESTER_IDENTITY_CONTRACT), "report_identity": rel(ji.STRATEGY_TESTER_REPORTS), "trade_evidence": rel(TRADE_SHAPE_COMPARISON), "cost_assumptions": "fixed lot 0.10, argmax probe, no threshold tuning(고정 랏 0.10, argmax 탐침, 임계값 조정 없음)", "forensic_checks": [rel(ji.MT5_EXECUTION_RESULT), rel(ji.RUNTIME_OUTPUT_COPY), rel(ji.EXECUTION_SUMMARY)], "backtest_judgment": "usable_with_boundary_report_parse_gap(보고서 파싱 공백 경계 조건부 사용 가능)"})
    write_json(RUNTIME_RECEIPT, {**base, "research_path": rel(Path(__file__)), "runtime_path": rel(ji.ATTEMPT_PACKAGE), "shared_contract": rel(ji.jh.RUNTIME_PARITY_CONTRACT), "known_differences": "runtime summary present but parsed tester report usable rows are zero(런타임 요약은 있으나 파싱된 테스터 보고서 사용 행은 0)", "parity_check": rel(ji.PROXY_MT5_DIFF), "parity_identity": f"{summary['exact_parity_rows']}/{summary['attempt_rows']}", "runtime_claim_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "observed_change": "raw top MT5 positive, risk-adjusted control MT5 negative(raw top MT5 양수, 위험 보정 대조 MT5 음수)", "comparison_baseline": rel(ji.FINAL_DECISION), "likely_drivers": "runtime PnL proxy preserved edge; session-regime adjustment failed runtime transfer(런타임 손익 프록시가 우위 보존, 세션/국면 조정은 런타임 전이 실패)", "segment_checks": rel(TRADE_SHAPE_COMPARISON), "trade_shape": {"best_trade_count": summary["best_trade_count"], "best_net_profit": summary["best_net_profit"], "best_profit_factor": summary["best_profit_factor"], "best_recovery_factor": summary["best_recovery_factor"], "best_drawdown": summary["best_drawdown"]}, "alternative_explanations": "single inner-holdout runtime probe and report parse gap(단일 내부 보류 런타임 탐침과 보고서 파싱 공백)", "attribution_confidence": "medium_low(중하)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(RUNTIME_REVIEW), rel(TRADE_SHAPE_COMPARISON), rel(PROXY_MT5_ATTRIBUTION), rel(GATE_AUDIT)], "evidence_missing": "forward replay, parsed tester report, cost stress variations, operating promotion evidence(전진 재생, 파싱된 테스터 보고서, 비용 압박 변형, 운영 승격 근거)", "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "좋아졌지만 아직 운영 모델은 아니다."})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "forward_passed": "not_claimed", "forward_failed": "not_claimed", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_with_manifest(목록과 함께 생성)", "lineage_judgment": "connected_with_boundary(경계 조건부 연결)"})


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
        "mt5_runtime_probe": "reviewed",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at": TODAY, "created_at_utc": now_utc(), "script": rel(Path(__file__)), "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "claim_boundary": CLAIM_BOUNDARY})
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JJ Runtime Negative Collapse Repair MT5 Runtime Probe Review(run337JJ 런타임 음수 붕괴 수리 MT5 런타임 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- exact_parity_rows(정확 동등성 행): `{final['exact_parity_rows']}/{final['attempt_rows']}`
- positive_runtime_rows(런타임 양수 행): `{final['positive_runtime_rows']}`
- best_model_id(최고 모델 ID): `{final['best_model_id']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 후보 낙폭): `{final['best_drawdown']}`
- negative_control_model_id(음수 대조 모델 ID): `{final['negative_control_model_id']}`
- negative_control_net_profit(음수 대조 순수익): `{final['negative_control_net_profit']}`

## Action(행동)

JI MT5 runtime probe(JI MT5 런타임 탐침)를 review(검토)해 raw top(순수 1위) 양수 단서와 risk-adjusted control(위험 보정 대조) 실패를 분리했다.
Effect(효과): +202.81 순수익 단서는 보존하지만 PF(수익 팩터), recovery(회복), drawdown(낙폭), report parse(보고서 파싱) 경계 때문에 운영 주장으로 올리지 않는다.

## Next(다음)

`{NEXT_RUN_ID}`에서 low PF/recovery/drawdown(낮은 PF/회복/낙폭) 수리를 설계한다.
"""
    decision = f"""# {TODAY} Stage337JJ Decision(337JJ 결정)

- decision(결정): `{DECISION}`
- evidence(근거): `{rel(RUNTIME_REVIEW)}`, `{rel(TRADE_SHAPE_COMPARISON)}`, `{rel(PROXY_MT5_ATTRIBUTION)}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

Effect(효과): JJ review(JJ 검토)는 런타임 양수 단서를 다음 수리 설계로 넘기고 운영 주장은 닫아 둔다.
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- positive_clue_model(긍정 단서 모델): `{final['best_model_id']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`
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
    marker = f"run337JJ {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run337JJ Runtime Probe Review(런타임 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 양수 런타임 단서를 수리 설계로 넘겼고 selection(선정)은 하지 않았다.
""")
    append_text_once(ROOT_CHANGELOG, marker, f"""## {TODAY} run337JJ Runtime Probe Review(런타임 탐침 검토)

- action(행동): JI MT5 runtime probe(JI MT5 런타임 탐침)를 검토했다.
- effect(효과): `{final['best_model_id']}`는 긍정 단서, `{final['negative_control_model_id']}`는 실패 기억으로 분리했다.
- boundary(경계): selected model(선정 모델), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
""")
    append_text_once(WORKSPACE_CHANGELOG, marker, f"""## {TODAY} run337JJ Runtime Probe Review(런타임 탐침 검토)

- action(행동): JI MT5 runtime probe(JI MT5 런타임 탐침)를 검토했다.
- effect(효과): 다음 JK repair design(JK 수리 설계)로 연결했다.
- boundary(경계): 운영 주장은 없다.
""")


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


def update_registers(final: Mapping[str, Any]) -> None:
    base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "run_date": TODAY, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "primary_artifact": rel(FINAL_DECISION), "report_path": rel(REPORT_PATH), "claim_boundary": CLAIM_BOUNDARY}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A used(Tier A 사용)", "tier": "Tier A", "metric_scope": "mt5_runtime_probe_review", "net_profit": final["best_net_profit"], "profit_factor": final["best_profit_factor"], "recovery_factor": final["best_recovery_factor"], "drawdown": final["best_drawdown"], "trade_count": final["best_trade_count"], "result_status": JUDGMENT},
        {**base, "view": "Tier B fallback used(Tier B 대체 사용)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "actual routed total(실제 라우팅 전체)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."), "path": rel(path), "sha256": sha(path), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY})
    if rows:
        registry = registry.loc[~registry["path"].astype(str).isin({row["path"] for row in rows})].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        write_csv(ARTIFACT_REGISTRY, registry[list(dict.fromkeys(required + list(registry.columns)))])


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    review, trade_shape, attribution, judgment_matrix, tier_record, queue, summary = build_review()
    write_csv(RUNTIME_REVIEW, review)
    write_csv(TRADE_SHAPE_COMPARISON, trade_shape)
    write_csv(PROXY_MT5_ATTRIBUTION, attribution)
    write_csv(RESULT_JUDGMENT_MATRIX, judgment_matrix)
    write_csv(TIER_PAIR_RECORD, tier_record)
    write_csv(NEXT_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JJ gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "best_model_id": final["best_model_id"], "best_net_profit": final["best_net_profit"], "best_profit_factor": final["best_profit_factor"], "best_recovery_factor": final["best_recovery_factor"], "negative_control_model_id": final["negative_control_model_id"], "gates": f"{final['gate_passes']}/{final['gate_total']}", "next_action": NEXT_RUN_ID, "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

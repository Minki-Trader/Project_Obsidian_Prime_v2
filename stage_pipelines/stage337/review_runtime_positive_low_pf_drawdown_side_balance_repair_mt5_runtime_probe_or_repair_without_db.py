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
    execute_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_without_db as ik,
)


aw = ik.aw

TODAY = "2026-06-01"
STAGE_ID = ik.STAGE_ID
STAGE_DIR = ik.STAGE_DIR
RUN_NUMBER = "run337IL"
RUN_ID = "run337IL_review_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_or_repair_without_db_v1"
PARENT_RUN_ID = ik.RUN_ID
NEXT_RUN_ID = "run337IM_design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_without_db_v1"
STATUS = "completed_stage337IL_runtime_positive_repair_mt5_probe_review_negative_exact_parity_repair_required_no_selection"
JUDGMENT = "proxy_positive_candidate_mt5_negative_exact_parity_operating_ineligible_repair_required"
DECISION = "stage337IL_open_run337IM_design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IL_repair_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IL_runtime_positive_repair_mt5_runtime_probe_review.md"

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

RUNTIME_REVIEW = RUN_DIR / "il_runtime_probe_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "il_proxy_mt5_attribution.csv"
RESULT_JUDGMENT_MATRIX = RUN_DIR / "il_result_judgment_matrix.csv"
TIER_PAIR_RECORD = RUN_DIR / "il_tier_pair_record.csv"
REPAIR_QUEUE = RUN_DIR / "run337IM_repair_design_queue.csv"
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
    ik.FINAL_DECISION,
    ik.GATE_AUDIT,
    ik.EXECUTION_SUMMARY,
    ik.PROXY_MT5_DIFF,
    ik.STRATEGY_TESTER_REPORTS,
    ik.ij.ii.POSITIVE_MATRIX,
)
OUTPUT_FILES = (
    RUNTIME_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    RESULT_JUDGMENT_MATRIX,
    TIER_PAIR_RECORD,
    REPAIR_QUEUE,
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
    return pd.read_csv(io(path))


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
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


def build_review() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(ik.FINAL_DECISION)
    summary_frame = read_csv(ik.EXECUTION_SUMMARY)
    diff = read_csv(ik.PROXY_MT5_DIFF)
    positive = read_csv(ik.ij.ii.POSITIVE_MATRIX)
    reports = read_json(ik.STRATEGY_TESTER_REPORTS)
    report = reports[0] if reports else {}
    metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
    summary = first_or_empty(summary_frame)
    proxy = first_or_empty(positive)

    exact_parity = (
        int(parent.get("matched_rows", 0)) > 0
        and int(parent.get("mismatch_rows", 0)) == 0
        and str(parent.get("comparison_status", "")) == "completed_exact_proxy_mt5_parity_reached_feature_last"
    )
    mt5_negative = float(parent.get("net_profit", 0.0) or 0.0) < 0.0 or float(parent.get("profit_factor", 0.0) or 0.0) < 1.0
    report_has_metrics = bool(metrics) and str(metrics.get("status", "")).lower() == "completed"
    proxy_net = float(proxy.get("net_log_return_after_cost", 0.0) or 0.0)
    mt5_net = float(parent.get("net_profit", 0.0) or 0.0)
    proxy_pf = float(proxy.get("profit_factor", 0.0) or 0.0)
    mt5_pf = float(parent.get("profit_factor", 0.0) or 0.0)
    proxy_trades = int(float(proxy.get("trade_count", 0) or 0))
    mt5_trades = int(float(parent.get("trade_count", 0) or 0))

    runtime_review = pd.DataFrame(
        [
            {
                "attempt_name": parent.get("primary_attempt_name", ""),
                "model_id": parent.get("primary_model_id", ""),
                "runtime_status": parent.get("runtime_status", ""),
                "comparison_status": parent.get("comparison_status", ""),
                "matched_rows": parent.get("matched_rows", 0),
                "mismatch_rows": parent.get("mismatch_rows", 0),
                "exact_proxy_mt5_parity": "true" if exact_parity else "false",
                "net_profit": parent.get("net_profit"),
                "profit_factor": parent.get("profit_factor"),
                "expectancy": parent.get("expectancy"),
                "recovery_factor": parent.get("recovery_factor"),
                "max_drawdown_amount": parent.get("max_drawdown_amount"),
                "trade_count": parent.get("trade_count"),
                "long_trade_count": parent.get("long_trade_count"),
                "short_trade_count": parent.get("short_trade_count"),
                "report_has_metrics": "true" if report_has_metrics else "false",
                "review_judgment": JUDGMENT,
                "effect": "Runtime probe(런타임 탐침)를 operating claim(운영 주장)이 아니라 repair evidence(수리 근거)로 판정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    attribution = pd.DataFrame(
        [
            {
                "attribution_id": "proxy_positive_to_mt5_negative_exact_parity",
                "model_id": parent.get("primary_model_id", ""),
                "proxy_net_log_return": proxy_net,
                "mt5_net_profit": mt5_net,
                "proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": mt5_pf,
                "proxy_trade_count": proxy_trades,
                "mt5_trade_count": mt5_trades,
                "proxy_signal_density": proxy.get("signal_density", ""),
                "proxy_long_net": proxy.get("long_net", ""),
                "proxy_short_net": proxy.get("short_net", ""),
                "mt5_long_trade_count": parent.get("long_trade_count"),
                "mt5_short_trade_count": parent.get("short_trade_count"),
                "runtime_parity_status": "exact_parity" if exact_parity else "parity_not_closed",
                "primary_failure_axis": (
                    "trade_lifecycle_cost_drawdown_shape(거래 생명주기/비용/낙폭 구조)"
                    if exact_parity and mt5_negative
                    else "runtime_handoff_or_missing_output(런타임 인계 또는 출력 누락)"
                ),
                "repair_seed": (
                    "density throttle, lifecycle exit, cost survival, side net filter"
                    "(밀도 제한, 생명주기 청산, 비용 생존, 방향 순수익 필터)"
                ),
                "effect": "Parity(동등성)가 맞았으므로 모델/피처 인계보다 실행 구조 수리로 원인을 좁힌다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    judgment_matrix = pd.DataFrame(
        [
            {
                "judgment_id": "runtime_probe_result",
                "result_class": "negative_runtime_probe_repair_required" if mt5_negative else "runtime_probe_review_required",
                "operating_eligibility": "operating_ineligible(운영 부적격)",
                "candidate_selection": "not_selected(선택 안 함)",
                "forward_passed": "not_claimed(주장 안 함)",
                "forward_failed": "not_claimed(주장 안 함)",
                "goal_achieve": "not_claimed(주장 안 함)",
                "reason": (
                    "MT5 net profit(순수익) and PF(수익 팩터) are negative/weak despite exact proxy parity"
                    "(정확한 프록시 동등성에도 MT5 순수익과 수익 팩터가 약함)"
                ),
                "effect": "proxy-positive(프록시 양성)를 운영 가능 모델로 올리지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tier_record = pd.DataFrame(
        [
            {
                "tier_view": "Tier A used(Tier A 사용)",
                "status": "reviewed_negative_runtime_probe",
                "evidence_path": rel(RUNTIME_REVIEW),
                "effect": "Tier A(티어 A) MT5 결과를 수리 근거로 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier B fallback used(Tier B 대체 사용)",
                "status": "missing_required",
                "evidence_path": rel(TIER_PAIR_RECORD),
                "effect": "Tier B(티어 B)가 없음을 생략하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "actual routed total(실제 라우팅 전체)",
                "status": "missing_required",
                "evidence_path": rel(TIER_PAIR_RECORD),
                "effect": "합산 라우팅이 없음을 명시해 synthetic sum(합성 합산)을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair",
                "required_inputs": f"{rel(PROXY_MT5_ATTRIBUTION)};{rel(RUNTIME_REVIEW)};{rel(ik.PROXY_MT5_DIFF)}",
                "repair_focus": "lifecycle_exit_density_cost_side_filter(생명주기 청산/밀도/비용/방향 필터)",
                "forbidden_action": "claim selection or relax gates(선택 주장 또는 게이트 완화)",
                "effect": "negative MT5 result(MT5 음수 결과)를 다음 공격 탐색 제약으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    diff_status = diff["comparison_status"].astype(str).value_counts().to_dict() if "comparison_status" in diff.columns else {}
    out = {
        "runtime_completed_rows": int(parent.get("runtime_completed_rows", 0)),
        "matched_rows": int(parent.get("matched_rows", 0)),
        "mismatch_rows": int(parent.get("mismatch_rows", 0)),
        "diff_rows": int(parent.get("diff_rows", len(diff))),
        "exact_proxy_mt5_parity": exact_parity,
        "report_has_metrics": report_has_metrics,
        "mt5_negative": mt5_negative,
        "proxy_net_log_return": proxy_net,
        "mt5_net_profit": mt5_net,
        "proxy_profit_factor": proxy_pf,
        "mt5_profit_factor": mt5_pf,
        "proxy_trade_count": proxy_trades,
        "mt5_trade_count": mt5_trades,
        "mt5_expectancy": float(parent.get("expectancy", 0.0) or 0.0),
        "mt5_recovery_factor": float(parent.get("recovery_factor", 0.0) or 0.0),
        "mt5_max_drawdown_amount": float(parent.get("max_drawdown_amount", 0.0) or 0.0),
        "mt5_long_trade_count": int(parent.get("long_trade_count", 0) or 0),
        "mt5_short_trade_count": int(parent.get("short_trade_count", 0) or 0),
        "primary_model_id": str(parent.get("primary_model_id", "")),
        "primary_attempt_name": str(parent.get("primary_attempt_name", "")),
        "diff_status_counts": diff_status,
        "next_action": NEXT_RUN_ID,
    }
    return runtime_review, attribution, judgment_matrix, tier_record, queue, out


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(ik.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row(
                "parent_ik_gates_passed",
                "passed" if passed_status(parent_gates["status"]).all() else "failed",
                rel(ik.GATE_AUDIT),
                "IK runtime probe(런타임 탐침)가 gate(게이트)를 통과한 뒤 검토한다.",
            ),
            gate_row(
                "runtime_output_reviewed",
                "passed" if summary["runtime_completed_rows"] >= 1 else "failed",
                rel(RUNTIME_REVIEW),
                "MT5 runtime output(MT5 런타임 출력)을 검토한다.",
            ),
            gate_row(
                "exact_parity_recorded",
                "passed" if summary["exact_proxy_mt5_parity"] else "failed",
                rel(PROXY_MT5_ATTRIBUTION),
                "proxy-MT5 exact parity(정확 동등성)를 기록한다.",
            ),
            gate_row(
                "mt5_negative_kpi_recorded",
                "passed" if summary["mt5_negative"] else "failed",
                rel(RESULT_JUDGMENT_MATRIX),
                "MT5 negative KPI(MT5 음수 핵심 성과 지표)를 숨기지 않는다.",
            ),
            gate_row(
                "repair_queue_opened",
                "passed" if exists(REPAIR_QUEUE) else "failed",
                rel(REPAIR_QUEUE),
                "음수 MT5 결과를 다음 repair design(수리 설계)로 넘긴다.",
            ),
            gate_row(
                "tier_pair_missing_required_recorded",
                "passed" if exists(TIER_PAIR_RECORD) else "failed",
                rel(TIER_PAIR_RECORD),
                "Tier B(티어 B)와 actual routed total(실제 라우팅 전체) 누락을 기록한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "selected model(선정 모델), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    if exists(path):
        frame = read_csv(path)
    else:
        frame = pd.DataFrame()
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
    return [
        RUNTIME_REVIEW,
        PROXY_MT5_ATTRIBUTION,
        RESULT_JUDGMENT_MATRIX,
        TIER_PAIR_RECORD,
        REPAIR_QUEUE,
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
        Path(__file__),
    ]


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
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": rel(path),
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
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "runtime_review": rel(RUNTIME_REVIEW),
            "report_has_metrics": summary["report_has_metrics"],
            "mt5_net_profit": summary["mt5_net_profit"],
            "mt5_profit_factor": summary["mt5_profit_factor"],
            "effect": "Tester report(테스터 보고서)를 음수 MT5 판정 근거로 고정한다.",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "exact_proxy_mt5_parity": summary["exact_proxy_mt5_parity"],
            "matched_rows": summary["matched_rows"],
            "mismatch_rows": summary["mismatch_rows"],
            "effect": "runtime parity(런타임 동등성)가 닫혀 실패 원인을 인계가 아닌 실행 구조로 좁힌다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "proxy_net_log_return": summary["proxy_net_log_return"],
            "mt5_net_profit": summary["mt5_net_profit"],
            "proxy_profit_factor": summary["proxy_profit_factor"],
            "mt5_profit_factor": summary["mt5_profit_factor"],
            "mt5_expectancy": summary["mt5_expectancy"],
            "mt5_recovery_factor": summary["mt5_recovery_factor"],
            "allowed_use": "repair design seed(수리 설계 씨앗)",
            "forbidden_use": "candidate selection or operating promotion(후보 선택 또는 운영 승격)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
            "gate_total": int(len(gates)),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "runtime_review": rel(RUNTIME_REVIEW),
            "proxy_mt5_attribution": rel(PROXY_MT5_ATTRIBUTION),
            "consumer": NEXT_RUN_ID,
            "effect": "negative runtime result(음수 런타임 결과)를 다음 repair packet(수리 묶음)에 연결한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
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
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
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
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IL MT5 Runtime Probe Review(run337IL MT5 런타임 탐침 검토)

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
- mt5_trade_count(MT5 거래수): `{final['mt5_trade_count']}`
- mt5_max_drawdown_amount(MT5 최대 낙폭 금액): `{final['mt5_max_drawdown_amount']}`

## Action(행동)

IK MT5 runtime probe(런타임 탐침)를 review(검토)했다.
Effect(효과): proxy-positive(프록시 양성)가 MT5에서는 negative(음수)였고, parity(동등성)는 정확히 맞았음을 분리했다.

## Judgment(판정)

이 후보는 operating-ineligible(운영 부적격)이다. 이유는 MT5 net profit(순수익) `{final['mt5_net_profit']}`, PF(수익 팩터) `{final['mt5_profit_factor']}`, recovery factor(회복 계수) `{final['mt5_recovery_factor']}` 때문이다.
Effect(효과): 실패를 model handoff(모델 인계) 문제가 아니라 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 수리 조건으로 바꾼다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 lifecycle exit(생명주기 청산), density throttle(밀도 제한), cost survival(비용 생존), side net filter(방향 순수익 필터)를 설계한다.
"""
    decision = f"""# {TODAY} Stage337IL Decision(337IL 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_REVIEW)}`, `{rel(PROXY_MT5_ATTRIBUTION)}`, `{rel(RESULT_JUDGMENT_MATRIX)}`

Action(행동): proxy-positive(프록시 양성) 후보를 MT5 negative(음수) exact-parity(정확 동등성) 결과로 판정했다.
Effect(효과): 다음 작업은 selection(선택)이 아니라 repair design(수리 설계)로 열린다.

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

IL review(검토)는 proxy-positive(프록시 양성)를 MT5 negative(음수) exact-parity(정확 동등성) 결과로 닫았다.
효과는 다음 IM design(설계)이 handoff(인계) 수리가 아니라 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 수리로 시작하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- runtime_probe_judgment(런타임 탐침 판정): `negative_exact_parity_repair_required(음수 정확 동등성 수리 필요)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): negative MT5 probe(음수 MT5 탐침)를 운영 승격으로 오해하지 않게 한다.
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

    marker = f"run337IL {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IL MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): exact parity(정확 동등성)였지만 MT5 negative(음수)이므로 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 수리로 넘겼다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IL MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- action(행동): IK MT5 runtime probe(런타임 탐침)를 review(검토)했다.
- effect(효과): matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`인데 MT5 net profit(순수익) `{final['mt5_net_profit']}`, PF(수익 팩터) `{final['mt5_profit_factor']}`라서 repair design(수리 설계)로 넘겼다.
- boundary(경계): selected model(선정 모델), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없음.
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
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    ledger_rows = [
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
    for row in ledger_rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    runtime_review, attribution, judgment_matrix, tier_record, queue, summary = build_review()
    write_csv(RUNTIME_REVIEW, runtime_review)
    write_csv(PROXY_MT5_ATTRIBUTION, attribution)
    write_csv(RESULT_JUDGMENT_MATRIX, judgment_matrix)
    write_csv(TIER_PAIR_RECORD, tier_record)
    write_csv(REPAIR_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IL gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "exact_proxy_mt5_parity": final["exact_proxy_mt5_parity"],
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
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

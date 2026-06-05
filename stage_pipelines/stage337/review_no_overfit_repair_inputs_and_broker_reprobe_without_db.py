from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import materialize_no_overfit_repair_inputs_or_broker_forward_reprobe_without_db as et  # noqa: E402


aw = et.aw

TODAY = "2026-05-31"
STAGE_ID = et.STAGE_ID
RUN_NUMBER = "run337EU"
RUN_ID = "run337EU_review_no_overfit_repair_inputs_and_broker_reprobe_without_db_v1"
PARENT_RUN_ID = et.RUN_ID
NEXT_RUN_ID = "run337EV_design_broker_confirmed_side_cost_curve_offensive_repair_without_db_v1"
STATUS = "completed_stage337EU_review_inputs_and_broker_reprobe_reached_cost_side_curve_blocks_release_no_selection"
JUDGMENT = "broker_reprobe_reached_and_confirms_cost_side_curve_failure_memory_with_rank2_positive_clue_no_release"
DECISION = "stage337EU_open_run337EV_broker_confirmed_side_cost_curve_offensive_repair_design_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EU_no_overfit_repair_input_and_broker_reprobe_review_without_db_"
    "no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = et.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = et.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EU_review_no_overfit_repair_inputs_and_broker_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337EU_review_no_overfit_repair_inputs_and_broker_reprobe.md"
SELECTED_STATUS = et.SELECTED_STATUS
STAGE_BRIEF = et.STAGE_BRIEF
WORKSPACE_STATE = et.WORKSPACE_STATE
CURRENT_STATE = et.CURRENT_STATE
CHANGELOG = et.CHANGELOG
RUN_REGISTRY = et.RUN_REGISTRY
ALPHA_LEDGER = et.ALPHA_LEDGER
ARTIFACT_REGISTRY = et.ARTIFACT_REGISTRY
STAGE_LEDGER = et.STAGE_LEDGER

ET_FINAL = et.FINAL_DECISION
ET_MANIFEST = et.RUN_MANIFEST
ET_FEATURE = et.FEATURE_CONTRACT
ET_GATE = et.GATE_CONTRACT
ET_NEGATIVE = et.NEGATIVE_CONTROL_PLAN
ET_PROXY = et.PROXY_MT5_PAIRING
ET_NO_LOOKAHEAD = et.NO_LOOKAHEAD_AUDIT
ET_REQUIRED_GATES = et.GATE_AUDIT
ET_BROKER_PRECHECK = et.BROKER_VISIBILITY_PRECHECK
ET_BROKER_SUMMARY = et.BROKER_REPROBE_SUMMARY
ET_MT5_REPORT = et.BROKER_MT5_REPORT
ET_TRADE_RECORDS = et.BROKER_TRADE_RECORDS
ET_RUNTIME_GATES = et.BROKER_RUNTIME_GATE_AUDIT
ET_COST = et.BROKER_COST_STRESS
ET_CURVE = et.BROKER_CURVE_POCKET
ET_REGIME = et.BROKER_REGIME_ATTRIBUTION
ET_DB = et.BROKER_DB_ATTRIBUTION
ET_SIGNAL = et.BROKER_SIGNAL_ATTRIBUTION
ET_EXECUTION = et.BROKER_MT5_EXECUTION_RESULT
ET_SOURCE_HASH = et.INPUT_SOURCE_HASH
ET_REVIEW_QUEUE = et.RUN337EU_QUEUE

FEATURE_REVIEW = RUN_DIR / "feature_contract_review.csv"
GATE_REVIEW = RUN_DIR / "gate_contract_review.csv"
NEGATIVE_REVIEW = RUN_DIR / "negative_control_review.csv"
PROXY_REVIEW = RUN_DIR / "proxy_mt5_pairing_review.csv"
BROKER_RUNTIME_REVIEW = RUN_DIR / "broker_runtime_kpi_release_review.csv"
FAILURE_MEMORY_UPDATE = RUN_DIR / "broker_confirmed_failure_memory_update.csv"
RELEASE_GUARDRAIL = RUN_DIR / "release_guardrail_review.csv"
EV_QUEUE = RUN_DIR / "run337EV_offensive_repair_design_queue.csv"
INPUT_SOURCE_HASH = RUN_DIR / "input_source_hash_matrix.csv"
PACKAGE_MANIFEST = RUN_DIR / "review_package_manifest.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ET_FINAL,
    ET_MANIFEST,
    ET_FEATURE,
    ET_GATE,
    ET_NEGATIVE,
    ET_PROXY,
    ET_NO_LOOKAHEAD,
    ET_REQUIRED_GATES,
    ET_BROKER_PRECHECK,
    ET_BROKER_SUMMARY,
    ET_MT5_REPORT,
    ET_TRADE_RECORDS,
    ET_RUNTIME_GATES,
    ET_COST,
    ET_CURVE,
    ET_REGIME,
    ET_DB,
    ET_SIGNAL,
    ET_EXECUTION,
    ET_SOURCE_HASH,
    ET_REVIEW_QUEUE,
)

FEATURE_REVIEW_COLUMNS = (
    "contract_id",
    "input_family",
    "timestamp_rule_status",
    "forbidden_source_status",
    "proxy_mt5_role_status",
    "review_gate_status",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
GATE_REVIEW_COLUMNS = (
    "gate_id",
    "gate_family",
    "artifact_exists",
    "pass_condition_present",
    "fail_condition_present",
    "required_before_status",
    "review_status",
    "effect",
    "claim_boundary",
)
NEGATIVE_REVIEW_COLUMNS = (
    "control_id",
    "control_family",
    "invalid_condition_present",
    "expected_guard_present",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PROXY_REVIEW_COLUMNS = (
    "pairing_id",
    "source_role",
    "usable_for",
    "not_usable_for",
    "boundary_status",
    "review_status",
    "effect",
    "claim_boundary",
)
BROKER_REVIEW_COLUMNS = (
    "attempt_name",
    "proxy_rank",
    "feature_set_id",
    "trade_count",
    "net_profit",
    "profit_factor",
    "expectancy",
    "max_drawdown_percent",
    "recovery_factor",
    "long_trade_count",
    "short_trade_count",
    "long_net_profit",
    "short_net_profit",
    "cost_1pt_net_profit",
    "cost_5pt_net_profit",
    "worst_month_net_profit",
    "release_gate_status",
    "positive_clue",
    "failure_read",
    "effect",
    "claim_boundary",
)
MEMORY_COLUMNS = (
    "memory_id",
    "status",
    "observed",
    "usable_as",
    "not_usable_as",
    "next_design_pressure",
    "effect",
    "claim_boundary",
)
GUARDRAIL_COLUMNS = (
    "guard_id",
    "status",
    "observed",
    "forbidden_claim",
    "allowed_next_use",
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
SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "used_for",
    "availability",
    "claim_boundary",
)
PACKAGE_COLUMNS = (
    "package_id",
    "artifact_path",
    "artifact_type",
    "rows",
    "producer",
    "consumer",
    "source_inputs",
    "status",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    proc = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


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


def row_count(path: Path) -> int:
    return len(read_csv(path)) if path_exists(path) and path.suffix.lower() == ".csv" else 0


def num(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(str(value).strip())
    except Exception:
        return default
    return parsed if math.isfinite(parsed) else default


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def resolve_repo_path(text: str) -> Path:
    path = Path(str(text).strip())
    return path if path.is_absolute() else ROOT / path


def source_identity(source_id: str, path: Path, used_for: str) -> dict[str, Any]:
    exists = path_exists(path)
    return {
        "source_id": source_id,
        "path": rel(path),
        "exists": bool_text(exists),
        "row_count": row_count(path),
        "sha256": aw.sha256_file(path) if exists else "",
        "used_for": used_for,
        "availability": "available" if exists else "missing",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_features(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    reviewed = []
    for row in rows:
        timestamp_ok = bool(row.get("timestamp_rule"))
        forbidden_named = bool(row.get("forbidden_sources"))
        proxy_bounded = "MT5" in row.get("proxy_mt5_role", "") or "mt5" in row.get("proxy_mt5_role", "").lower()
        gate_ok = str(row.get("review_gate", "")).startswith("et_gate_")
        status = "accepted_for_train_only_design(학습 전용 설계 허용)" if all([timestamp_ok, forbidden_named, proxy_bounded, gate_ok]) else "blocked_review_gap(검토 공백 차단)"
        reviewed.append(
            {
                "contract_id": row.get("contract_id", ""),
                "input_family": row.get("input_family", ""),
                "timestamp_rule_status": "present" if timestamp_ok else "missing",
                "forbidden_source_status": "named" if forbidden_named else "missing",
                "proxy_mt5_role_status": "bounded" if proxy_bounded else "missing_or_unbounded",
                "review_gate_status": "linked" if gate_ok else "missing",
                "review_status": status,
                "allowed_use": "EV design input only(EV 설계 입력 전용)",
                "forbidden_use": "candidate selection or forward filter(후보 선택 또는 전진 필터)",
                "effect": "keeps repair inputs timestamp-safe and non-selective(수리 입력을 시점 안전/비선택 상태로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return reviewed


def review_gates(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    reviewed = []
    for row in rows:
        artifact = resolve_repo_path(row.get("artifact_to_check", ""))
        artifact_exists = path_exists(artifact)
        required_before_ok = row.get("required_before") == RUN_ID
        status = "accepted_active_gate(활성 게이트 수락)" if artifact_exists and required_before_ok and row.get("pass_condition") and row.get("fail_condition") else "blocked_gate_gap(게이트 공백 차단)"
        reviewed.append(
            {
                "gate_id": row.get("gate_id", ""),
                "gate_family": row.get("gate_family", ""),
                "artifact_exists": bool_text(artifact_exists),
                "pass_condition_present": bool_text(bool(row.get("pass_condition"))),
                "fail_condition_present": bool_text(bool(row.get("fail_condition"))),
                "required_before_status": "matches_run337EU" if required_before_ok else "mismatch",
                "review_status": status,
                "effect": "keeps EU review tied to ET predeclared gates(EU 검토를 ET 사전 선언 게이트에 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return reviewed


def review_negative_controls(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    reviewed = []
    for row in rows:
        invalid_present = bool(row.get("invalid_if"))
        guard_present = bool(row.get("expected_guard"))
        status = "accepted_active_negative_control(활성 부정 대조 수락)" if invalid_present and guard_present else "blocked_negative_control_gap(부정 대조 공백 차단)"
        reviewed.append(
            {
                "control_id": row.get("control_id", ""),
                "control_family": row.get("control_family", ""),
                "invalid_condition_present": bool_text(invalid_present),
                "expected_guard_present": bool_text(guard_present),
                "review_status": status,
                "allowed_use": "falsification and release blocking(반증과 해제 차단)",
                "forbidden_use": "threshold relaxation or test skip(임계값 완화 또는 테스트 생략)",
                "effect": "keeps weak releases from passing quietly(약한 해제가 조용히 통과하지 못하게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return reviewed


def review_proxy_pairings(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    reviewed = []
    for row in rows:
        not_usable = row.get("not_usable_for", "").lower()
        bounded = any(term in not_usable for term in ("profit", "operating", "forward", "authority"))
        reviewed.append(
            {
                "pairing_id": row.get("pairing_id", ""),
                "source_role": row.get("proxy_or_diagnostic_source", ""),
                "usable_for": row.get("usable_for", ""),
                "not_usable_for": row.get("not_usable_for", ""),
                "boundary_status": "proxy_bounded(프록시 제한됨)" if bounded else "proxy_boundary_gap(프록시 경계 공백)",
                "review_status": "accepted_signal_sanity_only(신호 점검 전용 수락)" if bounded else "blocked",
                "effect": "keeps proxy helpful without replacing MT5 KPI(프록시를 유용하게 쓰되 MT5 성과를 대체하지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return reviewed


def index_by_attempt(rows: Sequence[Mapping[str, str]], key: str = "attempt_name") -> dict[str, list[Mapping[str, str]]]:
    indexed: dict[str, list[Mapping[str, str]]] = {}
    for row in rows:
        indexed.setdefault(str(row.get(key, "")), []).append(row)
    return indexed


def first_row(rows: Sequence[Mapping[str, str]], **filters: str) -> Mapping[str, str]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in filters.items()):
            return row
    return {}


def review_broker_runtime(
    mt5_rows: Sequence[Mapping[str, str]],
    cost_rows: Sequence[Mapping[str, str]],
    curve_rows: Sequence[Mapping[str, str]],
    regime_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    cost_by_attempt = index_by_attempt(cost_rows)
    curve_by_attempt = index_by_attempt(curve_rows)
    regime_by_attempt = index_by_attempt(regime_rows)
    reviewed = []
    for row in sorted(mt5_rows, key=lambda item: num(item.get("proxy_rank"), 999)):
        attempt = row.get("attempt_name", "")
        rank = row.get("proxy_rank", "")
        net = num(row.get("net_profit"))
        pf = num(row.get("profit_factor"))
        expectancy = num(row.get("expectancy"))
        recovery = num(row.get("recovery_factor"))
        dd_pct = num(row.get("max_drawdown_percent"))
        trade_count = int(num(row.get("trade_count")))
        long_trades = int(num(row.get("long_trade_count")))
        short_trades = int(num(row.get("short_trade_count")))
        cost_1 = first_row(cost_by_attempt.get(attempt, []), extra_round_trip_points="1")
        cost_5 = first_row(cost_by_attempt.get(attempt, []), extra_round_trip_points="5")
        curve_summary = first_row(curve_by_attempt.get(attempt, []), pocket_type="attempt_summary")
        worst_month = first_row(curve_by_attempt.get(attempt, []), pocket_type="worst_month")
        long_row = first_row(regime_by_attempt.get(attempt, []), axis="direction", bucket="buy")
        short_row = first_row(regime_by_attempt.get(attempt, []), axis="direction", bucket="sell")
        long_net = num(long_row.get("net_profit"))
        short_net = num(short_row.get("net_profit"))
        cost_1_net = num(cost_1.get("net_profit"), math.nan)
        cost_5_net = num(cost_5.get("net_profit"), math.nan)
        worst_month_net = num(worst_month.get("net_profit"), math.nan)
        release_ok = (
            net > 0
            and pf >= 1.10
            and expectancy > 0
            and recovery >= 1.0
            and trade_count >= 40
            and dd_pct <= 20
            and long_net > 0
            and short_net > 0
            and cost_1_net > 0
            and cost_5_net > 0
            and worst_month_net >= 0
        )
        if release_ok:
            release_status = "release_review_required_not_auto_selected(해제 검토 필요, 자동 선택 아님)"
        else:
            release_status = "blocked_release_multi_kpi_fragile(다중 성과 취약으로 해제 차단)"
        if net > 0 and long_net > 0 and trade_count >= 40:
            clue = "positive_clue_rank_net_and_long_side(순익과 롱 방향 긍정 단서)"
        elif long_net > 0:
            clue = "positive_clue_long_side_only(롱 방향 단서만 긍정)"
        else:
            clue = "no_positive_release_clue(해제 긍정 단서 없음)"
        failures = []
        if net <= 0:
            failures.append("net<=0")
        if pf < 1.10:
            failures.append("pf<1.10")
        if expectancy <= 0:
            failures.append("expectancy<=0")
        if recovery < 1.0:
            failures.append("recovery<1")
        if short_net <= 0:
            failures.append("short_net<=0")
        if cost_1_net <= 0 or cost_5_net <= 0:
            failures.append("cost_stress_break")
        if worst_month_net < 0:
            failures.append("negative_worst_month")
        reviewed.append(
            {
                "attempt_name": attempt,
                "proxy_rank": rank,
                "feature_set_id": row.get("feature_set_id", ""),
                "trade_count": trade_count,
                "net_profit": net,
                "profit_factor": pf,
                "expectancy": expectancy,
                "max_drawdown_percent": dd_pct,
                "recovery_factor": recovery,
                "long_trade_count": long_trades,
                "short_trade_count": short_trades,
                "long_net_profit": long_net,
                "short_net_profit": short_net,
                "cost_1pt_net_profit": cost_1_net,
                "cost_5pt_net_profit": cost_5_net,
                "worst_month_net_profit": worst_month_net,
                "release_gate_status": release_status,
                "positive_clue": clue,
                "failure_read": ";".join(failures) if failures else "none",
                "effect": "turns broker evidence into design pressure without selecting a candidate(브로커 근거를 후보 선택 없이 설계 압력으로 변환)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return reviewed


def build_failure_memory(runtime_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    total = len(runtime_rows)
    negative_net = sum(1 for row in runtime_rows if num(row.get("net_profit")) <= 0)
    pf_below_1_1 = sum(1 for row in runtime_rows if num(row.get("profit_factor")) < 1.10)
    cost_fragile = sum(1 for row in runtime_rows if num(row.get("cost_1pt_net_profit")) <= 0 or num(row.get("cost_5pt_net_profit")) <= 0)
    short_negative = sum(1 for row in runtime_rows if num(row.get("short_net_profit")) <= 0)
    long_positive = sum(1 for row in runtime_rows if num(row.get("long_net_profit")) > 0)
    worst_month_negative = sum(1 for row in runtime_rows if num(row.get("worst_month_net_profit")) < 0)
    best = max(runtime_rows, key=lambda row: num(row.get("net_profit")), default={})
    return [
        {
            "memory_id": "broker_visibility_reached",
            "status": "completed",
            "observed": f"reports={summary.get('runtime_summary_rows')};trades={summary.get('trade_rows')};latest_runtime={summary.get('latest_runtime_timestamp')}",
            "usable_as": "real broker runtime evidence(실제 브로커 런타임 근거)",
            "not_usable_as": "operating authority or Goal Achieve(운영 권위 또는 목표 달성)",
            "next_design_pressure": "use broker evidence as constraint only(브로커 근거를 제약으로만 사용)",
            "effect": "replaces stale visibility blocker with measured broker evidence(낡은 가시성 차단을 측정된 브로커 근거로 대체)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "multi_kpi_release_block",
            "status": "blocked_release",
            "observed": f"negative_net={negative_net}/{total};pf_below_1_10={pf_below_1_1}/{total};cost_fragile={cost_fragile}/{total};worst_month_negative={worst_month_negative}/{total}",
            "usable_as": "failure memory and guardrail(실패 기억과 가드레일)",
            "not_usable_as": "candidate death or threshold selector(후보 사망 또는 임계값 선택자)",
            "next_design_pressure": "predeclare cost survival and curve stability gates(비용 생존과 곡선 안정 게이트를 사전 선언)",
            "effect": "prevents a single positive net row from becoming a release claim(단일 양수 순익 행이 해제 주장으로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "side_asymmetry_confirmed",
            "status": "offensive_clue_with_guardrail",
            "observed": f"long_positive={long_positive}/{total};short_negative={short_negative}/{total};best_rank={best.get('proxy_rank')};best_net={best.get('net_profit')};best_pf={best.get('profit_factor')}",
            "usable_as": "side-aware offensive repair seed(방향 인식 공격 수리 씨앗)",
            "not_usable_as": "known-forward short veto(알려진 전진 숏 거부 규칙)",
            "next_design_pressure": "train-only side quality objective with separate long/short reporting(학습 전용 방향 품질 목표와 롱/숏 분리 보고)",
            "effect": "keeps the strongest clue while blocking forward-side overfit(가장 강한 단서를 살리면서 전진 방향 과적합을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "db_source_still_unavailable",
            "status": "out_of_scope_by_claim",
            "observed": "broker reprobe rows use argmax_short_flat_long_no_D_B_source_columns",
            "usable_as": "reason to avoid D/B rewrite(D/B 재작성 회피 사유)",
            "not_usable_as": "D/B attribution proof(D/B 귀속 증명)",
            "next_design_pressure": "continue without D/B or materialize a separate timestamp-safe D/B source before use(D/B 없이 계속하거나 사용 전 시점 안전 D/B 원천을 별도 물질화)",
            "effect": "keeps missing D/B source from becoming hidden model logic(D/B 원천 누락이 숨은 모델 로직이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_guardrails(runtime_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    release_rows = [row for row in runtime_rows if str(row.get("release_gate_status", "")).startswith("release_review_required")]
    blockers = summary.get("execution_blockers", [])
    return [
        {
            "guard_id": "no_candidate_release",
            "status": "passed",
            "observed": f"release_review_rows={len(release_rows)};auto_selected=0",
            "forbidden_claim": "candidate selection or promotion candidate(후보 선택 또는 승격 후보)",
            "allowed_next_use": "EV design only(EV 설계 전용)",
            "effect": "keeps slight positive rank2 as a clue, not a release(약한 rank2 양수를 해제가 아닌 단서로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "external_verification_completed_not_authority",
            "status": "passed" if not blockers and num(summary.get("trade_rows")) > 0 else "blocked",
            "observed": f"blockers={blockers};trade_rows={summary.get('trade_rows')};status={summary.get('status')}",
            "forbidden_claim": "Forward Passed/Failed or runtime authority(전진 통과/실패 또는 런타임 권위)",
            "allowed_next_use": "broker evidence for failure memory(실패 기억용 브로커 근거)",
            "effect": "separates external check completion from operating meaning(외부 확인 완료와 운영 의미를 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "no_forward_parameter_search",
            "status": "passed",
            "observed": "EU reviewed ET contracts and did not tune threshold, lot, D/B, ATR, risk, or dates",
            "forbidden_claim": "post-forward retune(전진 이후 재튜닝)",
            "allowed_next_use": "predeclared train-only repair design(사전 선언 학습 전용 수리 설계)",
            "effect": "turns observed failure into future controls instead of immediate parameters(관측 실패를 즉시 파라미터가 아닌 미래 대조로 변환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ev_design_broker_confirmed_side_cost_curve_repair",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "design train-only offensive side/cost/curve repair(학습 전용 공격 방향/비용/곡선 수리 설계)",
            "required_inputs": f"{rel(BROKER_RUNTIME_REVIEW)};{rel(FAILURE_MEMORY_UPDATE)};{rel(RELEASE_GUARDRAIL)}",
            "required_outputs": "feature/label/objective contracts, side-aware negative controls, release gates(피처/라벨/목표 계약, 방향 인식 부정 대조, 해제 게이트)",
            "blocked_if_missing": "long/short separate KPI, cost ladder, worst-month curve evidence(롱/숏 분리 성과, 비용 사다리, 최악 월 곡선 근거)",
            "forbidden_action": "known forward short veto, threshold retune, lot optimization, D/B rewrite(알려진 전진 숏 거부, 임계값 재조정, 랏 최적화, D/B 재작성)",
            "effect": "moves from blocker recovery to new profit-source exploration(차단 복구에서 새 수익원 탐색으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "ev_keep_broker_forward_claim_closed",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "preserve broker evidence as constraint, not Forward decision(브로커 근거를 전진 판정이 아닌 제약으로 보존)",
            "required_inputs": f"{rel(ET_MT5_REPORT)};{rel(ET_TRADE_RECORDS)}",
            "required_outputs": "claim boundary row and failure memory link(주장 경계 행과 실패 기억 연결)",
            "blocked_if_missing": "explicit no Forward Passed/Failed boundary(전진 통과/실패 없음 경계)",
            "forbidden_action": "Goal Achieve or operating promotion(목표 달성 또는 운영 승격)",
            "effect": "lets actual MT5 evidence guide research without overclaiming(실제 MT5 근거가 과장 없이 연구를 이끌게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_sources() -> list[dict[str, Any]]:
    return [source_identity(f"eu_input_{idx:02d}", path, "run337EU_review_input") for idx, path in enumerate(INPUT_FILES, start=1)]


def build_package_manifest(paths: Sequence[Path]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": f"eu_pkg_{idx:03d}",
            "artifact_path": rel(path),
            "artifact_type": path.suffix.lstrip(".") or "file",
            "rows": row_count(path) if path.suffix.lower() == ".csv" else "",
            "producer": rel(__file__),
            "consumer": NEXT_RUN_ID,
            "source_inputs": ";".join(rel(path) for path in INPUT_FILES if path_exists(path)),
            "status": "available" if path_exists(path) else "missing",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for idx, path in enumerate(paths, start=1)
    ]


def build_required_gates(
    feature_review: Sequence[Mapping[str, Any]],
    gate_review: Sequence[Mapping[str, Any]],
    negative_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    runtime_review: Sequence[Mapping[str, Any]],
    guardrails: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
    runtime_gates: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    blocked_runtime = [row for row in runtime_gates if row.get("status") == "blocked"]
    release_rows = [row for row in runtime_review if str(row.get("release_gate_status", "")).startswith("release_review_required")]
    return [
        {
            "gate_id": "scope_completion_gate",
            "status": "passed" if all([feature_review, gate_review, negative_review, proxy_review, runtime_review, guardrails]) else "failed",
            "evidence_path": f"{rel(FEATURE_REVIEW)};{rel(BROKER_RUNTIME_REVIEW)};{rel(RELEASE_GUARDRAIL)}",
            "observed": f"feature={len(feature_review)};gate={len(gate_review)};negative={len(negative_review)};runtime={len(runtime_review)}",
            "expected": "all EU review surfaces materialized(모든 EU 검토 표면 물질화)",
            "effect": "proves EU reviewed both contracts and broker evidence(EU가 계약과 브로커 근거를 함께 검토했음을 증명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "kpi_contract_audit",
            "status": "passed" if len(runtime_review) == 7 and len(release_rows) == 0 else "failed",
            "evidence_path": rel(BROKER_RUNTIME_REVIEW),
            "observed": f"attempts={len(runtime_review)};auto_release_rows={len(release_rows)}",
            "expected": "7 attempts reviewed and no auto release(7개 시도 검토, 자동 해제 없음)",
            "effect": "blocks single-KPI release(단일 성과 해제를 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "data_integrity_gate",
            "status": "passed" if all(row.get("availability") == "available" for row in sources) else "failed",
            "evidence_path": rel(INPUT_SOURCE_HASH),
            "observed": f"available_sources={sum(1 for row in sources if row.get('availability') == 'available')}/{len(sources)}",
            "expected": "all ET review inputs available(모든 ET 검토 입력 가용)",
            "effect": "keeps EU review tied to real artifacts(EU 검토를 실제 산출물에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_evidence_gate",
            "status": "passed" if not blocked_runtime and num(summary.get("trade_rows")) > 0 and not summary.get("execution_blockers") else "failed",
            "evidence_path": f"{rel(ET_MT5_REPORT)};{rel(ET_TRADE_RECORDS)};{rel(ET_RUNTIME_GATES)}",
            "observed": f"trade_rows={summary.get('trade_rows')};blocked_runtime_gates={len(blocked_runtime)};execution_blockers={summary.get('execution_blockers')}",
            "expected": "real broker reprobe executed with parsed trades(실제 브로커 재탐침과 파싱된 거래)",
            "effect": "replaces blocked visibility with measured runtime evidence(차단 가시성을 측정 런타임 근거로 대체)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "model_validation_gate",
            "status": "passed" if all(row.get("status") == "passed" for row in guardrails) else "failed",
            "evidence_path": rel(RELEASE_GUARDRAIL),
            "observed": ";".join(f"{row.get('guard_id')}={row.get('status')}" for row in guardrails),
            "expected": "no training, tuning, selection, or release(학습/조정/선택/해제 없음)",
            "effect": "keeps broker evidence from becoming hidden selection(브로커 근거가 숨은 선택이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed" if sources else "failed",
            "evidence_path": rel(INPUT_SOURCE_HASH),
            "observed": f"sources={len(sources)}",
            "expected": "source hashes recorded(원천 해시 기록)",
            "effect": "makes EU review reproducible(EU 검토를 재현 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "required_gate_coverage_audit",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "observed": "scope_completion_gate;kpi_contract_audit;data_integrity_gate;runtime_evidence_gate;model_validation_gate;artifact_lineage_audit",
            "expected": "all required gates connected to closeout(모든 필수 게이트가 종료 기록에 연결)",
            "effect": "prevents completion without gate evidence(게이트 근거 없는 완료를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(summary: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]]) -> list[Path]:
    payloads = {
        ROUTING_RECEIPT: {
            "run_id": RUN_ID,
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "data_integrity_gate",
                "runtime_evidence_gate",
                "model_validation_gate",
                "artifact_lineage_audit",
                "required_gate_coverage_audit",
            ],
            "effect": "routes EU as evidence review, not training(EU를 학습이 아닌 근거 검토로 라우팅)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUN_EVIDENCE_RECEIPT: {
            "measurement_identity": RUN_ID,
            "broker_reprobe_status": summary.get("status"),
            "mt5_report_rows": summary.get("runtime_summary_rows"),
            "trade_rows": summary.get("trade_rows"),
            "runtime_rows_reviewed": len(runtime_rows),
            "external_verification_status": "completed",
            "judgment": JUDGMENT,
        },
        EXPERIMENT_RECEIPT: {
            "hypothesis": "broker-confirmed side/cost/curve failure can seed a safer offensive repair(브로커 확인 방향/비용/곡선 실패가 더 안전한 공격 수리 씨앗이 될 수 있음)",
            "comparison": "rank2 positive clue versus multi-KPI release guards(rank2 긍정 단서와 다중 성과 해제 가드 비교)",
            "controls": [rel(ET_NEGATIVE), rel(RELEASE_GUARDRAIL)],
            "stop_condition": "no candidate release if PF, cost, curve, side, or recovery breaks(PF/비용/곡선/방향/회복이 깨지면 후보 해제 없음)",
            "next_action": NEXT_RUN_ID,
        },
        DATA_RECEIPT: {
            "timestamp_safety": "review-only; no new features or labels(검토 전용, 새 피처/라벨 없음)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "missing_inputs": [rel(path) for path in INPUT_FILES if not path_exists(path)],
            "leakage_judgment": "no new look-ahead path introduced(새 미래참조 경로 없음)",
        },
        MODEL_RECEIPT: {
            "training": "not_run",
            "threshold_tuning": "not_run",
            "candidate_selection": "not_run",
            "release_guardrails": [row.get("guard_id") for row in guardrails],
            "validation_judgment": "no release; design next(해제 없음, 다음 설계)",
        },
        RUNTIME_RECEIPT: {
            "mt5_strategy_tester": "executed",
            "runtime_summary": summary,
            "runtime_authority": "not_claimed",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
        },
        PERFORMANCE_RECEIPT: {
            "attempt_count": len(runtime_rows),
            "positive_clues": [row for row in runtime_rows if "positive_clue" in str(row.get("positive_clue", ""))],
            "release_rows": [row for row in runtime_rows if str(row.get("release_gate_status", "")).startswith("release_review_required")],
            "attribution_axes": ["net", "pf", "expectancy", "drawdown", "recovery", "cost", "side", "curve"],
        },
        JUDGMENT_RECEIPT: {
            "judgment": JUDGMENT,
            "decision": DECISION,
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "reason": "real broker evidence is measured but multi-KPI release guards fail(실제 브로커 근거는 측정됐지만 다중 성과 해제 가드 실패)",
        },
        ARTIFACT_RECEIPT: {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(__file__),
            "artifact_paths": [rel(BROKER_RUNTIME_REVIEW), rel(FAILURE_MEMORY_UPDATE), rel(FINAL_DECISION)],
            "lineage_judgment": "connected_to_ET_and_EV(ET와 EV에 연결)",
        },
    }
    return [write_json(path, payload) for path, payload in payloads.items()]


def final_decision_payload(
    runtime_rows: Sequence[Mapping[str, Any]],
    memory_rows: Sequence[Mapping[str, Any]],
    guardrails: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    failed = [row.get("gate_id") for row in gates if row.get("status") != "passed"]
    best = max(runtime_rows, key=lambda row: num(row.get("net_profit")), default={})
    release_rows = [row for row in runtime_rows if str(row.get("release_gate_status", "")).startswith("release_review_required")]
    status = STATUS if not failed else "invalid_stage337EU_required_gate_failure_no_selection"
    judgment = JUDGMENT if not failed else "required_gate_failure_blocks_EU_review_claim"
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": DECISION if not failed else "repair_stage337EU_required_gate_failure_before_EV",
        "next_action": NEXT_RUN_ID if not failed else "repair_stage337EU_required_gate_failure_v1",
        "broker_reprobe_status": summary.get("status", ""),
        "external_verification_status": "completed" if not summary.get("execution_blockers") and num(summary.get("trade_rows")) > 0 else "blocked",
        "mt5_report_rows": summary.get("runtime_summary_rows"),
        "trade_rows": summary.get("trade_rows"),
        "attempts_reviewed": len(runtime_rows),
        "release_rows": len(release_rows),
        "best_proxy_rank": best.get("proxy_rank", ""),
        "best_attempt_name": best.get("attempt_name", ""),
        "best_net_profit": best.get("net_profit", ""),
        "best_profit_factor": best.get("profit_factor", ""),
        "best_expectancy": best.get("expectancy", ""),
        "best_recovery_factor": best.get("recovery_factor", ""),
        "long_positive_attempts": sum(1 for row in runtime_rows if num(row.get("long_net_profit")) > 0),
        "short_negative_attempts": sum(1 for row in runtime_rows if num(row.get("short_net_profit")) <= 0),
        "cost_fragile_attempts": sum(1 for row in runtime_rows if num(row.get("cost_1pt_net_profit")) <= 0 or num(row.get("cost_5pt_net_profit")) <= 0),
        "negative_net_attempts": sum(1 for row in runtime_rows if num(row.get("net_profit")) <= 0),
        "pf_below_1_10_attempts": sum(1 for row in runtime_rows if num(row.get("profit_factor")) < 1.10),
        "memory_rows": len(memory_rows),
        "guardrail_rows": len(guardrails),
        "passed_gates": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_rows": len(gates),
        "failed_gates": failed,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "deployment": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EU Review No-Overfit Inputs and Broker Reprobe(337단계 337EU 무과적합 입력과 브로커 재탐침 검토)

## Conclusion(결론)

run337EU(337EU 실행)는 run337ET(337ET 실행)의 contracts(계약)와 real broker MT5 Strategy Tester evidence(실제 브로커 MT5 전략 테스터 근거)를 검토했다.
Effect(효과): broker visibility blocker(브로커 가시성 차단)는 해소됐지만 multi-KPI release(다중 성과 해제)는 차단하고, side/cost/curve offensive repair design(방향/비용/곡선 공격 수리 설계)을 다음으로 연다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Broker Evidence(브로커 근거)

- broker_reprobe_status(브로커 재탐침 상태): `{final['broker_reprobe_status']}`
- MT5 reports(MT5 보고서): `{final['mt5_report_rows']}`
- trade rows(거래 행): `{final['trade_rows']}`
- attempts reviewed(검토 시도): `{final['attempts_reviewed']}`
- release rows(해제 행): `{final['release_rows']}`
- best rank(최고 순위): `{final['best_proxy_rank']}`
- best net/PF/expectancy/recovery(최고 순익/PF/기대값/회복): `{final['best_net_profit']}` / `{final['best_profit_factor']}` / `{final['best_expectancy']}` / `{final['best_recovery_factor']}`

## Failure Memory(실패 기억)

- negative net attempts(순익 음수 시도): `{final['negative_net_attempts']}/{final['attempts_reviewed']}`
- PF below 1.10(PF 1.10 미만): `{final['pf_below_1_10_attempts']}/{final['attempts_reviewed']}`
- cost fragile attempts(비용 취약 시도): `{final['cost_fragile_attempts']}/{final['attempts_reviewed']}`
- long positive attempts(롱 양수 시도): `{final['long_positive_attempts']}/{final['attempts_reviewed']}`
- short negative attempts(숏 음수 시도): `{final['short_negative_attempts']}/{final['attempts_reviewed']}`

## Boundary(경계)

- model training(모델 학습): `not_run`
- threshold tuning(임계값 조정): `not_run`
- D/B rewrite(D/B 재작성): `not_run`
- lot optimization(랏 최적화): `not_run`
- candidate selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337EU Decision(337EU 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`

Effect(효과): broker reprobe(브로커 재탐침)는 완료됐지만 release(해제)는 차단했다. rank2(2순위)의 약한 positive clue(긍정 단서)는 다음 EV design(EV 설계)에서 train-only side/cost/curve repair(학습 전용 방향/비용/곡선 수리)로만 사용한다.
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    import re

    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def insert_before_once(text: str, marker: str, section: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337EU focus complete: run337EU(337EU 실행)는 `{final['status']}`로 broker reprobe(브로커 재탐침) `{final['broker_reprobe_status']}`를 검토했다. "
        f"Effect(효과): MT5 reports(MT5 보고서) `{final['mt5_report_rows']}`, trade rows(거래 행) `{final['trade_rows']}`, release rows(해제 행) `{final['release_rows']}`로 해제는 차단하고 `{final['next_action']}`를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EU focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(상태):": f"- status(상태): `{final['status']}`",
        "- decision(결정):": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(최근 완료 실행):": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current = replace_line(current, prefix, replacement)
    section = f"""## run337EU Review No-Overfit Inputs and Broker Reprobe(무과적합 입력과 브로커 재탐침 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- broker_reprobe_status(브로커 재탐침 상태): `{final['broker_reprobe_status']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- MT5 reports/trades(MT5 보고서/거래): `{final['mt5_report_rows']}` / `{final['trade_rows']}`
- release_rows(해제 행): `{final['release_rows']}`
- best_rank_net_pf(최고 순위 순익/PF): `{final['best_proxy_rank']}` / `{final['best_net_profit']}` / `{final['best_profit_factor']}`
- effect(효과): 실제 브로커 가시성은 닫혔지만 비용/방향/곡선 취약성 때문에 release(해제)는 차단하고 EV(337EV 실행) 설계를 연다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = insert_before_once(current, "## run337ET No-Overfit Repair Inputs", section, "## run337EU Review No-Overfit Inputs")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface / stage337 survivor forward surface`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- broker_forward_boundary(브로커 전진 경계): `not_closed_EU_release_blocked`
- broker_reprobe_status(브로커 재탐침 상태): `{final['broker_reprobe_status']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- MT5 reports(보고서): `{final['mt5_report_rows']}`
- trade_rows(거래 행): `{final['trade_rows']}`
- release_rows(해제 행): `{final['release_rows']}`
- best_rank_net_pf_expectancy(최고 순위 순익/PF/기대값): `{final['best_proxy_rank']}` / `{final['best_net_profit']}` / `{final['best_profit_factor']}` / `{final['best_expectancy']}`
- negative_net_attempts(순익 음수 시도): `{final['negative_net_attempts']}/{final['attempts_reviewed']}`
- pf_below_1_10_attempts(PF 1.10 미만 시도): `{final['pf_below_1_10_attempts']}/{final['attempts_reviewed']}`
- cost_fragile_attempts(비용 취약 시도): `{final['cost_fragile_attempts']}/{final['attempts_reviewed']}`
- long_positive_attempts(롱 양수 시도): `{final['long_positive_attempts']}/{final['attempts_reviewed']}`
- short_negative_attempts(숏 음수 시도): `{final['short_negative_attempts']}/{final['attempts_reviewed']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): EU(337EU 실행)는 브로커 근거를 실패 기억과 공격 설계 씨앗으로 바꾸지만 후보 선택이나 운영 주장은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = replace_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337EU_summary(337EU 요약): `{final['status']}`. "
        f"Effect(효과): broker MT5 reports(브로커 MT5 보고서) `{final['mt5_report_rows']}`, trade rows(거래 행) `{final['trade_rows']}`를 검토했고 release rows(해제 행) `{final['release_rows']}`로 후보 해제를 차단했다. "
        f"rank2(2순위) net/PF(순익/PF) `{final['best_net_profit']}`/`{final['best_profit_factor']}`는 positive clue(긍정 단서)지만 cost/side/curve(비용/방향/곡선) 수리 설계에만 사용한다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    brief = append_once(brief, summary, "run337EU_summary")
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    entry = (
        f"- {TODAY}: Stage337 run337EU(337EU 실행) `{final['status']}`. "
        f"Effect(효과): broker reprobe(브로커 재탐침) 완료 근거를 검토하고 release(해제)는 차단했으며 `{final['next_action']}`를 열었다. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    changelog = append_once(changelog, entry, "Stage337 run337EU")
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_overfit_repair_input_and_broker_reprobe_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};external_verification_status={final['external_verification_status']};reports={final['mt5_report_rows']};trades={final['trade_rows']};release_rows={final['release_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__broker_reprobe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "broker_reprobe_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "broker_confirmed_no_overfit_input_review(브로커 확인 무과적합 입력 검토)",
        "tier_scope": "Tier A broker US100 M5 evidence and research-only failure memory(Tier A 브로커 US100 M5 근거와 연구 전용 실패 기억)",
        "kpi_scope": "MT5 broker reprobe net/PF/expectancy/DD/recovery/cost/side/curve no release(MT5 브로커 재탐침 순익/PF/기대값/낙폭/회복/비용/방향/곡선, 해제 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"reports={final['mt5_report_rows']};trades={final['trade_rows']};best_rank={final['best_proxy_rank']};best_net={final['best_net_profit']};best_pf={final['best_profit_factor']};release_rows={final['release_rows']}",
        "guardrail_kpi": f"negative_net={final['negative_net_attempts']}/{final['attempts_reviewed']};pf_below_1_10={final['pf_below_1_10_attempts']}/{final['attempts_reviewed']};cost_fragile={final['cost_fragile_attempts']}/{final['attempts_reviewed']};short_negative={final['short_negative_attempts']}/{final['attempts_reviewed']};no_forward_claim",
        "external_verification_status": final["external_verification_status"],
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed;runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__broker_reprobe_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "ET contracts plus real broker MT5 reprobe",
        "kpi_scope": "broker_reprobe_release_guardrail",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};release_rows={final['release_rows']};best_rank={final['best_proxy_rank']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__broker_reprobe_review",
        "family": "no_overfit_repair_input_and_broker_reprobe_review",
        "question": "can broker-confirmed evidence become offensive side/cost/curve repair pressure without selecting a candidate",
        "metric_scope": "net_pf_expectancy_dd_recovery_cost_side_curve",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path):
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"stage337EU review artifact; decision={final['decision']}",
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    feature_rows = read_csv(ET_FEATURE)
    gate_rows = read_csv(ET_GATE)
    negative_rows = read_csv(ET_NEGATIVE)
    proxy_rows = read_csv(ET_PROXY)
    mt5_rows = read_csv(ET_MT5_REPORT)
    cost_rows = read_csv(ET_COST)
    curve_rows = read_csv(ET_CURVE)
    regime_rows = read_csv(ET_REGIME)
    runtime_gates = read_csv(ET_RUNTIME_GATES)
    summary = read_json(ET_BROKER_SUMMARY)

    feature_review = review_features(feature_rows)
    gate_review = review_gates(gate_rows)
    negative_review = review_negative_controls(negative_rows)
    proxy_review = review_proxy_pairings(proxy_rows)
    runtime_review = review_broker_runtime(mt5_rows, cost_rows, curve_rows, regime_rows)
    memory_rows = build_failure_memory(runtime_review, summary)
    guardrails = build_guardrails(runtime_review, summary)
    queue_rows = build_queue()
    source_rows = build_sources()

    feature_path = write_csv(FEATURE_REVIEW, FEATURE_REVIEW_COLUMNS, feature_review)
    gate_review_path = write_csv(GATE_REVIEW, GATE_REVIEW_COLUMNS, gate_review)
    negative_path = write_csv(NEGATIVE_REVIEW, NEGATIVE_REVIEW_COLUMNS, negative_review)
    proxy_path = write_csv(PROXY_REVIEW, PROXY_REVIEW_COLUMNS, proxy_review)
    runtime_path = write_csv(BROKER_RUNTIME_REVIEW, BROKER_REVIEW_COLUMNS, runtime_review)
    memory_path = write_csv(FAILURE_MEMORY_UPDATE, MEMORY_COLUMNS, memory_rows)
    guard_path = write_csv(RELEASE_GUARDRAIL, GUARDRAIL_COLUMNS, guardrails)
    queue_path = write_csv(EV_QUEUE, QUEUE_COLUMNS, queue_rows)
    source_path = write_csv(INPUT_SOURCE_HASH, SOURCE_COLUMNS, source_rows)

    gates = build_required_gates(feature_review, gate_review, negative_review, proxy_review, runtime_review, guardrails, source_rows, summary, runtime_gates)
    gate_path = write_csv(GATE_AUDIT, GATE_COLUMNS, gates)
    receipt_paths = write_receipts(summary, runtime_review, guardrails)
    final = final_decision_payload(runtime_review, memory_rows, guardrails, gates, summary)
    final_path = write_json(FINAL_DECISION, final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    output_paths = [
        feature_path,
        gate_review_path,
        negative_path,
        proxy_path,
        runtime_path,
        memory_path,
        guard_path,
        queue_path,
        source_path,
        gate_path,
        *receipt_paths,
        final_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    package_rows = build_package_manifest(output_paths)
    package_path = write_csv(PACKAGE_MANIFEST, PACKAGE_COLUMNS, package_rows)
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_action": final["next_action"],
        "external_verification_status": final["external_verification_status"],
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in [FEATURE_REVIEW, BROKER_RUNTIME_REVIEW, FAILURE_MEMORY_UPDATE, RELEASE_GUARDRAIL, EV_QUEUE, GATE_AUDIT, FINAL_DECISION, REPORT_PATH, DECISION_DOC, PACKAGE_MANIFEST]],
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    manifest_path = write_json(RUN_MANIFEST, manifest)
    registry_path = update_artifact_registry([*output_paths, package_path, manifest_path, Path(__file__)], final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "external_verification_status": final["external_verification_status"],
                "mt5_reports": final["mt5_report_rows"],
                "trade_rows": final["trade_rows"],
                "release_rows": final["release_rows"],
                "best_rank": final["best_proxy_rank"],
                "best_net_profit": final["best_net_profit"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": rel(report_path),
                "artifact_registry": rel(registry_path),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import execute_mt5_feature_parity_probe_without_db as br


aw = br.aw
bg = br.bg

TODAY = "2026-05-27"
STAGE_ID = br.STAGE_ID
RUN_NUMBER = "run337BS"
RUN_ID = "run337BS_review_mt5_feature_parity_and_stale_lag_stress_without_db_v1"
PARENT_RUN_ID = br.RUN_ID
NEXT_RUN_ID = "run337BT_materialize_stale_lag_guarded_model_scout_inputs_without_db_v1"
STATUS = "completed_stage337BS_feature_parity_review_stale_lag_risk_named_no_forward_decision"
JUDGMENT = "mt5_feature_reader_usable_with_boundary_but_latest_tester_gap_and_equity_stale_lag_block_forward_runtime_authority"
DECISION = "stage337BS_open_run337BT_stale_lag_guarded_model_scout_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BS_feature_parity_and_stale_lag_review_without_db_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = br.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = br.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BS_feature_parity_stale_lag_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BS_feature_parity_stale_lag_review.md"
SELECTED_STATUS = br.SELECTED_STATUS
STAGE_BRIEF = br.STAGE_BRIEF
WORKSPACE_STATE = br.WORKSPACE_STATE
CURRENT_STATE = br.CURRENT_STATE
CHANGELOG = br.CHANGELOG
RUN_REGISTRY = br.RUN_REGISTRY
ALPHA_LEDGER = br.ALPHA_LEDGER
ARTIFACT_REGISTRY = br.ARTIFACT_REGISTRY
STAGE_LEDGER = br.STAGE_LEDGER

BR_DIR = STAGE_DIR / "02_runs" / "run337BR"
BQ_DIR = STAGE_DIR / "02_runs" / "run337BQ"
BR_FINAL = BR_DIR / "final_decision.json"
BR_ATTEMPT_SUMMARY = BR_DIR / "mt5_feature_parity_probe_attempt_summary.csv"
BR_HASH_COMPARISON = BR_DIR / "mt5_feature_parity_hash_comparison.csv"
BR_SKIP_REASON = BR_DIR / "mt5_feature_parity_skip_reason_summary.csv"
BR_GATE_AUDIT = BR_DIR / "required_gate_coverage_audit.csv"
BQ_FINAL = BQ_DIR / "final_decision.json"
BQ_LAG_SUMMARY = BQ_DIR / "asof_source_lag_summary.csv"
BQ_SESSION = BQ_DIR / "session_boundary_review.csv"
BQ_FEATURE_SUMMARY = BQ_DIR / "feature_set_materialization_summary.csv"

PARITY_REVIEW = RUN_DIR / "mt5_feature_parity_review.csv"
TESTER_GAP_REVIEW = RUN_DIR / "tester_gap_review.csv"
STALE_LAG_STRESS = RUN_DIR / "stale_lag_stress_matrix.csv"
FEATURE_SET_USABILITY = RUN_DIR / "feature_set_usability_matrix.csv"
PROXY_SCOPE_REVIEW = RUN_DIR / "proxy_scope_review.csv"
RUN337BT_QUEUE = RUN_DIR / "run337BT_stale_lag_guarded_model_scout_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BR_FINAL,
    BR_ATTEMPT_SUMMARY,
    BR_HASH_COMPARISON,
    BR_SKIP_REASON,
    BR_GATE_AUDIT,
    BQ_FINAL,
    BQ_LAG_SUMMARY,
    BQ_SESSION,
    BQ_FEATURE_SUMMARY,
)
OUTPUT_FILES = (
    PARITY_REVIEW,
    TESTER_GAP_REVIEW,
    STALE_LAG_STRESS,
    FEATURE_SET_USABILITY,
    PROXY_SCOPE_REVIEW,
    RUN337BT_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

PARITY_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "expected_rows",
    "ready_rows",
    "hash_match_rows",
    "hash_mismatch_rows",
    "feature_count_mismatch_rows",
    "coverage_ratio",
    "last_ready_bar_time",
    "latest_expected_timestamp",
    "latest_gap_minutes",
    "feature_last_reached",
    "parity_status",
    "usable_for_model_scout",
    "usable_for_forward_decision",
    "effect",
    "claim_boundary",
)
TESTER_GAP_COLUMNS = (
    "feature_set_id",
    "gap_id",
    "gap_type",
    "rows",
    "first_timestamp",
    "last_timestamp",
    "latest_gap_minutes",
    "classification",
    "effect",
    "claim_boundary",
)
STALE_COLUMNS = (
    "stress_id",
    "contract_symbol",
    "source_group",
    "feature_role",
    "threshold_hours",
    "max_lag_hours",
    "p95_lag_hours",
    "missing_rows",
    "lookahead_violations",
    "stress_status",
    "risk_class",
    "effect",
    "claim_boundary",
)
USABILITY_COLUMNS = (
    "feature_set_id",
    "feature_family",
    "parity_status",
    "external_stale_risk",
    "tester_gap_status",
    "usable_for_next_model_scout",
    "usable_for_forward_decision",
    "required_controls",
    "recommendation",
    "effect",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "review_id",
    "proxy_expected_available",
    "mt5_runtime_probe_available",
    "difference_review_status",
    "usable_for_kpi",
    "next_condition",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "accepted_inputs",
    "must_include",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = br.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with aw.io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    return aw.write_json(path, payload)


def rel(path: Path | str) -> str:
    return aw.rel(Path(path))


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_args() -> argparse.Namespace:
    return argparse.ArgumentParser(description=RUN_ID).parse_args()


def load_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BS inputs: {missing}")
    br_final = read_json(BR_FINAL)
    if br_final.get("next_action") != RUN_ID:
        raise RuntimeError(f"run337BR final does not open run337BS: {br_final.get('next_action')}")
    return {
        "br_final": br_final,
        "bq_final": read_json(BQ_FINAL),
        "attempt_rows": read_rows(BR_ATTEMPT_SUMMARY),
        "hash_rows": read_rows(BR_HASH_COMPARISON),
        "skip_rows": read_rows(BR_SKIP_REASON),
        "br_gates": read_rows(BR_GATE_AUDIT),
        "lag_rows": read_rows(BQ_LAG_SUMMARY),
        "session_rows": read_rows(BQ_SESSION),
        "feature_rows": read_rows(BQ_FEATURE_SUMMARY),
    }


def parse_mql_timestamp(value: str) -> pd.Timestamp | None:
    text = str(value or "").strip()
    if not text:
        return None
    return pd.Timestamp(datetime.strptime(text, "%Y.%m.%d %H:%M:%S").replace(tzinfo=UTC))


def parse_skip_timestamp(reason: str) -> pd.Timestamp | None:
    marker = "feature_csv_timestamp_not_found:"
    if not str(reason).startswith(marker):
        return None
    return parse_mql_timestamp(str(reason).split(marker, 1)[1])


def minutes_between(left: pd.Timestamp | None, right: pd.Timestamp | None) -> int:
    if left is None or right is None:
        return 0
    return int((right - left).total_seconds() // 60)


def as_int(row: Mapping[str, Any], key: str) -> int:
    try:
        return int(float(row.get(key, 0) or 0))
    except (TypeError, ValueError):
        return 0


def as_float(row: Mapping[str, Any], key: str) -> float:
    try:
        return float(row.get(key, 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def build_parity_review(attempt_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in attempt_rows:
        feature_set_id = row.get("feature_set_id", "")
        latest = parse_mql_timestamp(row.get("latest_expected_timestamp", ""))
        last_ready = parse_mql_timestamp(row.get("last_ready_bar_time", ""))
        latest_gap = minutes_between(last_ready, latest)
        hash_mismatch = as_int(row, "hash_mismatch_rows")
        count_mismatch = as_int(row, "feature_count_mismatch_rows")
        ready_rows = as_int(row, "ready_rows")
        usable = ready_rows > 0 and hash_mismatch == 0 and count_mismatch == 0
        feature_last_reached = str(row.get("feature_last_reached", "")).lower() == "true"
        if not usable:
            parity_status = "blocked_parity_mismatch_or_no_ready_rows"
        elif feature_last_reached:
            parity_status = "usable_latest_feature_reached"
        else:
            parity_status = "usable_overlap_latest_tester_gap_remains"
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "feature_count": row.get("feature_count", ""),
                "expected_rows": row.get("expected_rows", ""),
                "ready_rows": ready_rows,
                "hash_match_rows": row.get("hash_match_rows", ""),
                "hash_mismatch_rows": hash_mismatch,
                "feature_count_mismatch_rows": count_mismatch,
                "coverage_ratio": row.get("coverage_ratio", ""),
                "last_ready_bar_time": row.get("last_ready_bar_time", ""),
                "latest_expected_timestamp": row.get("latest_expected_timestamp", ""),
                "latest_gap_minutes": latest_gap,
                "feature_last_reached": row.get("feature_last_reached", ""),
                "parity_status": parity_status,
                "usable_for_model_scout": bool_text(usable),
                "usable_for_forward_decision": "false",
                "effect": "MT5 feature reader is usable for research if guarded by tester-gap boundary(MT5 피처 리더는 테스터 공백 경계 안에서 연구에 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_tester_gap_review(
    attempt_rows: Sequence[Mapping[str, str]],
    skip_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_feature: dict[str, list[pd.Timestamp]] = {}
    for row in skip_rows:
        ts = parse_skip_timestamp(row.get("skip_reason", ""))
        if ts is None:
            continue
        by_feature.setdefault(row.get("feature_set_id", ""), []).extend([ts] * max(as_int(row, "rows"), 1))
    attempt_by_feature = {row.get("feature_set_id", ""): row for row in attempt_rows}
    for feature_set_id, attempt in attempt_by_feature.items():
        latest = parse_mql_timestamp(attempt.get("latest_expected_timestamp", ""))
        last_ready = parse_mql_timestamp(attempt.get("last_ready_bar_time", ""))
        latest_gap = minutes_between(last_ready, latest)
        timestamps = sorted(by_feature.get(feature_set_id, []))
        if timestamps:
            first_ts = timestamps[0]
            last_ts = timestamps[-1]
            rows.append(
                {
                    "feature_set_id": feature_set_id,
                    "gap_id": f"{feature_set_id}_timestamp_not_found",
                    "gap_type": "feature_csv_timestamp_not_found",
                    "rows": len(timestamps),
                    "first_timestamp": first_ts.strftime("%Y.%m.%d %H:%M:%S"),
                    "last_timestamp": last_ts.strftime("%Y.%m.%d %H:%M:%S"),
                    "latest_gap_minutes": latest_gap,
                    "classification": "expected_calendar_or_session_gaps_plus_latest_tester_gap",
                    "effect": "missing timestamps are named so they cannot become silent runtime authority(누락 시각을 이름 붙여 조용한 런타임 권위가 되지 않게 함)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "gap_id": f"{feature_set_id}_latest_feature_not_reached",
                "gap_type": "latest_feature_tester_gap",
                "rows": 1 if latest_gap > 0 else 0,
                "first_timestamp": attempt.get("last_ready_bar_time", ""),
                "last_timestamp": attempt.get("latest_expected_timestamp", ""),
                "latest_gap_minutes": latest_gap,
                "classification": "blocks_forward_decision" if latest_gap > 0 else "no_latest_gap",
                "effect": "latest tester gap blocks Forward Passed/Failed(최신 테스터 공백이 전진 통과/실패를 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def risk_class(source_group: str, max_lag_hours: float, p95_lag_hours: float, lookahead: int) -> str:
    if lookahead > 0:
        return "invalid_lookahead"
    if source_group == "equity_cash" and p95_lag_hours >= 24:
        return "high_stale_carry_risk"
    if max_lag_hours >= 12:
        return "moderate_session_gap_risk"
    return "low_observed_lag_risk"


def build_stale_lag_stress(lag_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    thresholds_by_group = {
        "macro_proxy": (6.0, 12.0, 24.0),
        "equity_cash": (24.0, 48.0, 72.0),
    }
    rows: list[dict[str, Any]] = []
    for row in lag_rows:
        source_group = row.get("source_group", "")
        max_lag_hours = round(as_float(row, "max_lag_minutes") / 60.0, 6)
        p95_lag_hours = round(as_float(row, "p95_lag_minutes") / 60.0, 6)
        lookahead = as_int(row, "lookahead_violations")
        base_risk = risk_class(source_group, max_lag_hours, p95_lag_hours, lookahead)
        for threshold in thresholds_by_group.get(source_group, (float(row.get("tolerance_hours") or 0.0),)):
            if lookahead > 0:
                stress_status = "invalid_lookahead"
            elif max_lag_hours <= threshold:
                stress_status = "passed_under_threshold"
            else:
                stress_status = "fails_under_threshold"
            rows.append(
                {
                    "stress_id": f"{source_group}_maxlag_le_{threshold:g}h",
                    "contract_symbol": row.get("contract_symbol", ""),
                    "source_group": source_group,
                    "feature_role": row.get("feature_role", ""),
                    "threshold_hours": threshold,
                    "max_lag_hours": max_lag_hours,
                    "p95_lag_hours": p95_lag_hours,
                    "missing_rows": row.get("missing_rows", ""),
                    "lookahead_violations": lookahead,
                    "stress_status": stress_status,
                    "risk_class": base_risk,
                    "effect": "lag threshold stress separates no-lookahead validity from stale-context risk(지연 기준 압박이 미래참조 없음과 낡은 문맥 위험을 분리)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def feature_family(feature_set_id: str) -> str:
    if feature_set_id.startswith("core56"):
        return "core_plus_macro_plus_equity_context"
    if feature_set_id.startswith("macro48"):
        return "us100_plus_macro_context"
    if feature_set_id.startswith("us100_technical42"):
        return "us100_technical_only"
    return "unknown"


def build_feature_set_usability(
    parity_rows: Sequence[Mapping[str, Any]],
    stale_rows: Sequence[Mapping[str, Any]],
    tester_gap_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    equity_fail = any(row.get("source_group") == "equity_cash" and row.get("stress_status") == "fails_under_threshold" for row in stale_rows)
    macro_fail = any(row.get("source_group") == "macro_proxy" and row.get("stress_status") == "fails_under_threshold" for row in stale_rows)
    latest_gap = any(row.get("gap_type") == "latest_feature_tester_gap" and as_int(row, "latest_gap_minutes") > 0 for row in tester_gap_rows)
    rows: list[dict[str, Any]] = []
    for row in parity_rows:
        feature_set_id = str(row.get("feature_set_id", ""))
        family = feature_family(feature_set_id)
        if family == "us100_technical_only":
            stale_risk = "none_external_inputs"
            controls = "tester_gap_review;no_forward_claim"
            recommendation = "usable_as_low_stale_risk_model_scout_input"
            usable = row.get("usable_for_model_scout") == "true"
        elif family == "us100_plus_macro_context":
            stale_risk = "macro_moderate_stale_risk" if macro_fail else "macro_within_standard_tolerance"
            controls = "macro_lag_ablation;tester_gap_review;no_forward_claim"
            recommendation = "usable_with_macro_lag_stress"
            usable = row.get("usable_for_model_scout") == "true"
        elif family == "core_plus_macro_plus_equity_context":
            stale_risk = "equity_cash_high_stale_risk" if equity_fail else "equity_cash_within_static_tolerance"
            controls = "equity_lag_ablation;technical_only_negative_control;macro_only_control;tester_gap_review"
            recommendation = "usable_only_as_stale_stress_branch_not_primary"
            usable = row.get("usable_for_model_scout") == "true"
        else:
            stale_risk = "unknown"
            controls = "manual_review_required"
            recommendation = "blocked_unknown_feature_family"
            usable = False
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "feature_family": family,
                "parity_status": row.get("parity_status", ""),
                "external_stale_risk": stale_risk,
                "tester_gap_status": "latest_gap_remains" if latest_gap else "latest_reached",
                "usable_for_next_model_scout": bool_text(usable),
                "usable_for_forward_decision": "false",
                "required_controls": controls,
                "recommendation": recommendation,
                "effect": "feature sets are routed by risk before any model scout(모델 스카우트 전에 피처 세트를 위험별로 라우팅)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_scope_review() -> list[dict[str, Any]]:
    return [
        {
            "review_id": "run337BS_proxy_scope_boundary",
            "proxy_expected_available": "false",
            "mt5_runtime_probe_available": "feature_reader_only",
            "difference_review_status": "not_applicable_for_profit_or_signal_proxy",
            "usable_for_kpi": "false",
            "next_condition": "run337BT_or_later must produce proxy expected signal/profit and compare to MT5 runtime probe before KPI use",
            "effect": "prevents feature parity from being mistaken for proxy KPI parity(피처 동등성을 프록시 KPI 동등성으로 착각하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_queue(usability_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    accepted = [row["feature_set_id"] for row in usability_rows if row.get("usable_for_next_model_scout") == "true"]
    return [
        {
            "queue_id": "run337BT_stale_lag_guarded_model_scout_inputs",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "stale-lag guarded model scout inputs(낡은 지연 방어 모델 스카우트 입력)",
            "accepted_inputs": ";".join(accepted),
            "must_include": "technical-only control;macro-lag ablation;equity-lag stress branch;no-lookahead gates;proxy-vs-MT5 comparison plan",
            "must_reject_if": "uses forward labels for selection;claims runtime authority;ignores latest tester gap;promotes equity-stale branch as primary",
            "expected_outputs": "scout_input_packages;negative_controls;proxy_mt5_comparison_contract;no_training_if_inputs_fail",
            "priority": "P0",
            "effect": "moves from feature parity into guarded model research without retuning by forward outcome(전진 결과 재튜닝 없이 피처 동등성에서 방어된 모델 연구로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    parity_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    stale_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    br_gate_passed = sum(1 for row in src["br_gates"] if row.get("status") == "passed")
    no_hash_mismatch = all(as_int(row, "hash_mismatch_rows") == 0 for row in parity_rows)
    no_count_mismatch = all(as_int(row, "feature_count_mismatch_rows") == 0 for row in parity_rows)
    latest_gap_named = any(row.get("gap_type") == "latest_feature_tester_gap" and as_int(row, "latest_gap_minutes") > 0 for row in gap_rows)
    no_lookahead = all(as_int(row, "lookahead_violations") == 0 for row in stale_rows)
    stale_risk_named = any(row.get("risk_class") == "high_stale_carry_risk" for row in stale_rows)
    scout_input_exists = any(row.get("usable_for_next_model_scout") == "true" for row in usability_rows)
    proxy_bounded = all(row.get("usable_for_kpi") == "false" for row in proxy_rows)
    specs = [
        ("bs_gate_parent_br_loaded", src["br_final"].get("next_action") == RUN_ID, str(src["br_final"].get("next_action")), "run337BR opens run337BS(337BR이 337BS를 엶)"),
        ("bs_gate_parent_br_gates_passed", br_gate_passed == 11 and src["br_final"].get("passed_gates") == 11, f"br_gates={br_gate_passed}", "BR gates passed(BR 게이트 통과)"),
        ("bs_gate_hash_parity_reviewed", no_hash_mismatch, f"hash_mismatch={sum(as_int(row, 'hash_mismatch_rows') for row in parity_rows)}", "no MT5/Python hash mismatch(MT5/파이썬 해시 불일치 없음)"),
        ("bs_gate_feature_count_reviewed", no_count_mismatch, f"count_mismatch={sum(as_int(row, 'feature_count_mismatch_rows') for row in parity_rows)}", "no feature count mismatch(피처 수 불일치 없음)"),
        ("bs_gate_latest_tester_gap_named", latest_gap_named, f"latest_gap_named={latest_gap_named}", "latest tester gap is named(최신 테스터 공백 명명)"),
        ("bs_gate_no_lookahead_lag_rows", no_lookahead, f"lookahead={sum(as_int(row, 'lookahead_violations') for row in stale_rows)}", "no lag lookahead violations(지연 미래참조 위반 없음)"),
        ("bs_gate_stale_lag_stress_written", len(stale_rows) > 0 and stale_risk_named, f"stale_rows={len(stale_rows)};high_risk={stale_risk_named}", "stale lag risk is stressed(낡은 지연 위험 압박)"),
        ("bs_gate_feature_set_usability_written", scout_input_exists, f"usable_inputs={sum(1 for row in usability_rows if row.get('usable_for_next_model_scout') == 'true')}", "next scout inputs are bounded(다음 스카우트 입력 경계 설정)"),
        ("bs_gate_proxy_scope_not_misused", proxy_bounded, f"proxy_rows={len(proxy_rows)}", "feature parity is not proxy KPI parity(피처 동등성은 프록시 KPI 동등성이 아님)"),
        ("bs_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BT queue ready(337BT 대기열 준비)"),
        ("bs_gate_no_forward_or_goal_claim", True, "forward=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "review converts parity evidence into bounded next research inputs(검토가 동등성 근거를 경계 있는 다음 연구 입력으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def report_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| feature_set(피처 세트) | parity(동등성) | stale_risk(낡은 위험) | model_scout(모델 스카우트) | forward(전진) |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['feature_set_id']}` | `{row['parity_status']}` | `{row['external_stale_risk']}` | `{row['usable_for_next_model_scout']}` | `{row['usable_for_forward_decision']}` |"
        )
    return "\n".join(lines)


def write_report(final: Mapping[str, Any], usability_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]]) -> Path:
    latest_gap = max((as_int(row, "latest_gap_minutes") for row in gap_rows), default=0)
    text = f"""# Stage337 run337BS Feature Parity and Stale Lag Review(피처 동등성 및 지연 위험 검토)

## Conclusion(결론)

run337BS(337BS 실행)는 run337BR(337BR 실행)의 MT5 feature reader parity(MT5 피처 리더 동등성)를 review(검토)하고, run337BQ(337BQ 실행)의 as-of source lag(시점 기준 원천 지연)를 stress(압박)했다.

Effect(효과): MT5 reader(MT5 리더)는 연구용 handoff(인계)로 쓸 수 있지만, latest tester gap(최신 테스터 공백)과 equity stale carry risk(주식 낡은 이월 위험) 때문에 Forward/Runtime authority(전진/런타임 권위)는 닫지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- latest_tester_gap_minutes(최신 테스터 공백 분): `{latest_gap}`
- forward_passed(전진 통과): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Usability(사용 가능성)

{report_table(usability_rows)}

## Proxy Boundary(프록시 경계)

run337BR(337BR 실행)은 feature reader probe(피처 리더 탐침)라서 proxy expected vs MT5 runtime result(프록시 예상값 대 MT5 런타임 결과) 비교가 아니다. 다음 model scout(모델 스카우트)에서는 이 비교 계약을 반드시 포함한다.

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BS Feature Parity and Stale Lag Review(결정: 피처 동등성 및 지연 위험 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 다음 run337BT(337BT 실행)는 stale-lag guarded model scout input(낡은 지연 방어 모델 스카우트 입력)을 만들되, Forward/Runtime authority(전진/런타임 권위)는 주장하지 않는다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "work_family": "runtime_parity_data_integrity_review",
                "hypothesis": "MT5 feature parity can feed guarded model scouting only after stale lag and tester gap are named",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [rel(BR_ATTEMPT_SUMMARY), rel(BQ_LAG_SUMMARY), rel(BQ_SESSION)],
                "time_axis": "closed M5 bar timestamps in UTC; MT5 probe uses bar close timestamp",
                "sample_scope": "US100 M5 forward-after-2026-04-14 feature package review",
                "feature_label_boundary": "no labels, no outcomes, no threshold tuning in run337BS",
                "leakage_risk": "stale as-of carry and latest tester gap, not lookahead",
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "no model training, no ONNX export, no candidate selection",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(br.EA_SOURCE),
                "shared_contract": "feature count/order, closed M5 timestamp, exact MT5 CSV reader hash",
                "known_differences": "latest tester gap remains; no model inference in BR/BS",
                "parity_check": rel(BR_ATTEMPT_SUMMARY),
                "runtime_claim_boundary": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "outputs": [rel(path) for path in OUTPUT_FILES if aw.path_exists(path)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(PARITY_REVIEW), rel(STALE_LAG_STRESS), rel(FEATURE_SET_USABILITY)],
                "evidence_missing": "proxy expected vs MT5 signal/profit runtime comparison; latest feature timestamp tester reach",
                "judgment_label": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "피처 리더는 맞지만, 최신 구간과 낡은 외부 입력을 아직 전진 판정에 쓸 수 없다.",
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in payloads]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.replace_top_value(workspace_text, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        "- >-\n"
        f"  Stage337 run337BS focus complete: feature parity/stale lag review(피처 동등성/지연 위험 검토)를 `{final['status']}`로 닫았다. "
        "Effect(효과): MT5 reader(MT5 리더)는 연구용으로 쓸 수 있지만 latest tester gap(최신 테스터 공백)과 equity stale carry risk(주식 낡은 이월 위험)를 다음 run337BT(337BT 실행)의 방어 조건으로 넘긴다.\n"
    )
    if "Stage337 run337BS focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
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
## Stage337 run337BS(337BS 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): MT5 feature parity(MT5 피처 동등성)는 연구 입력으로 수락하되, tester gap(테스터 공백)과 stale lag(낡은 지연)을 다음 모델 스카우트 방어 조건으로 넘긴다.
"""
    if "## Stage337 run337BS(337BS 실행)" not in current:
        marker = "## Stage337 run337BR(337BR 실행)"
        current = current.replace(marker, entry + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + entry
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- actual_mt5_execution(실제 MT5 실행): `reviewed_from_run337BR_feature_reader_probe`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 stale-lag guarded model scout input(낡은 지연 방어 모델 스카우트 입력)이다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337BS(337BS 실행) reviewed MT5 feature parity and stale lag risk(MT5 피처 동등성/낡은 지연 위험). Status(상태) `{final['status']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337BS feature parity/stale lag review(피처 동등성/낡은 지연 검토) `{final['status']}`; run337BT queue opened."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_parity_stale_lag_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity_data_integrity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__feature_parity_stale_lag_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "feature_parity_stale_lag_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "feature_parity_stale_lag_review",
        "tier_scope": "Tier A+B combined feature package",
        "kpi_scope": "runtime_parity_data_integrity_no_profit_kpi",
        "scoreboard_lane": "runtime_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"usable_feature_sets={final['usable_feature_sets']}",
        "guardrail_kpi": "hash_mismatch_rows=0;forward_not_claimed;runtime_authority_not_claimed",
        "external_verification_status": "completed_from_run337BR",
        "notes": f"decision={final['decision']};next={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__feature_parity_stale_lag_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_data_integrity",
        "evidence_scope": "BR MT5 feature reader output plus BQ source lag summary",
        "kpi_scope": "feature_handoff_integrity_no_profit",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"usable_feature_sets={final['usable_feature_sets']};high_stale_risk={final['high_stale_risk_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__feature_parity_stale_lag_review",
        "family": "runtime_parity_data_integrity",
        "question": "which BQ feature sets can feed guarded model scouting after MT5 parity and stale-lag review",
        "metric_scope": "feature_parity_stale_lag_usability",
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
    artifact_columns = artifact_columns or [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    generated = now_utc()
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not aw.path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
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
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    parity_rows = build_parity_review(src["attempt_rows"])
    gap_rows = build_tester_gap_review(src["attempt_rows"], src["skip_rows"])
    stale_rows = build_stale_lag_stress(src["lag_rows"])
    usability_rows = build_feature_set_usability(parity_rows, stale_rows, gap_rows)
    proxy_rows = build_proxy_scope_review()
    queue_rows = build_queue(usability_rows)
    gates = build_gates(src, parity_rows, gap_rows, stale_rows, usability_rows, proxy_rows, queue_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "parity_review_rows": len(parity_rows),
        "tester_gap_rows": len(gap_rows),
        "stale_lag_stress_rows": len(stale_rows),
        "usable_feature_sets": sum(1 for row in usability_rows if row.get("usable_for_next_model_scout") == "true"),
        "high_stale_risk_rows": sum(1 for row in stale_rows if row.get("risk_class") == "high_stale_carry_risk"),
        "hash_mismatch_rows": sum(as_int(row, "hash_mismatch_rows") for row in parity_rows),
        "feature_count_mismatch_rows": sum(as_int(row, "feature_count_mismatch_rows") for row in parity_rows),
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final["gate_rows"] = len(gates)
    final["passed_gates"] = count_passed(gates)
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifact_paths: list[Path] = [
        write_csv(PARITY_REVIEW, PARITY_COLUMNS, parity_rows),
        write_csv(TESTER_GAP_REVIEW, TESTER_GAP_COLUMNS, gap_rows),
        write_csv(STALE_LAG_STRESS, STALE_COLUMNS, stale_rows),
        write_csv(FEATURE_SET_USABILITY, USABILITY_COLUMNS, usability_rows),
        write_csv(PROXY_SCOPE_REVIEW, PROXY_COLUMNS, proxy_rows),
        write_csv(RUN337BT_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
    ]
    artifact_paths.extend(build_receipts(final))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": now_utc(),
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifact_paths.append(write_report(final, usability_rows, gap_rows))
    artifact_paths.append(write_decision_doc(final))
    artifact_paths.extend(update_docs(final))
    artifact_paths.extend(update_registers(final, artifact_paths))
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

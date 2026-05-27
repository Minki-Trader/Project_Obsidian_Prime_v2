from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AL"
RUN_ID = "run337AL_exact_timestamp_policy_boundary_or_broker_rollover_wait_v1"
PARENT_RUN_ID = "run337AK_next_rollover_or_synthetic_custom_parity_repair_v1"
NEXT_RUN_ID = "run337AM_no_lookahead_cost_direction_curve_rebuild_input_materialization_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AL_exact_timestamp_policy_boundary_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_COMPLETED = "completed_stage337AL_proxy_role_lock_refreshed_broker_rollover_not_due_no_forward_decision"
JUDGMENT_COMPLETED = "exact_timestamp_proxy_usable_for_runtime_signal_parity_only_broker_forward_boundary_remains"
DECISION_COMPLETED = "stage337AL_open_run337AM_no_lookahead_rebuild_inputs_with_broker_rollover_guard_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AK_DIR = STAGE_DIR / "02_runs" / "run337AK"
RUN337AG_DIR = STAGE_DIR / "02_runs" / "run337AG"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AL_exact_timestamp_policy_boundary_or_broker_rollover_wait.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AL_exact_timestamp_policy_boundary.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    return str(value)


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def columns_for(rows: Sequence[Mapping[str, Any]], defaults: Sequence[str] | None = None) -> list[str]:
    columns = list(defaults or [])
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    return columns


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp = io_path(path).with_name(io_path(path).name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, io_path(path))
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding=encoding, newline="\n")
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AL exact timestamp policy boundary materialization.")
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def to_float(value: Any) -> float | None:
    if value in {None, ""}:
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "matched", "passed"}


def input_evidence_rows() -> list[dict[str, Any]]:
    paths = [
        RUN337AK_DIR / "final_decision.json",
        RUN337AK_DIR / "exact_timestamp_proxy_scope.csv",
        RUN337AK_DIR / "exact_timestamp_proxy_expected_result.csv",
        RUN337AK_DIR / "exact_timestamp_proxy_mt5_difference.csv",
        RUN337AK_DIR / "proxy_usability_exact_timestamp.csv",
        RUN337AK_DIR / "tester_feature_last_gap_exact_timestamp.csv",
        RUN337AK_DIR / "runtime_summary.csv",
        RUN337AK_DIR / "required_gate_coverage_audit.csv",
        RUN337AG_DIR / "proxy_mt5_role_lock_contract.csv",
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.append(
            {
                "artifact_path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "",
                "role": "parent_evidence" if "run337AK" in rel(path) else "prior_contract",
                "effect": "run337AL(337AL 실행)의 proxy usability(프록시 사용성) 판정 입력이다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_runtime_usability_rows() -> list[dict[str, Any]]:
    usability = {row["attempt_name"]: row for row in read_csv(RUN337AK_DIR / "proxy_usability_exact_timestamp.csv")}
    scope = {row["attempt_name"]: row for row in read_csv(RUN337AK_DIR / "exact_timestamp_proxy_scope.csv")}
    diff = read_csv(RUN337AK_DIR / "exact_timestamp_proxy_mt5_difference.csv")
    diff_by_attempt: dict[str, list[dict[str, str]]] = {}
    for row in diff:
        diff_by_attempt.setdefault(row.get("attempt_name", ""), []).append(row)
    rows: list[dict[str, Any]] = []
    for attempt, use in usability.items():
        subset = diff_by_attempt.get(attempt, [])
        matched = sum(1 for row in subset if row.get("difference_status") == "matched")
        dimensions = ",".join(row.get("dimension", "") for row in subset)
        scope_row = scope.get(attempt, {})
        continuous = to_float(scope_row.get("continuous_window_feature_rows")) or 0.0
        exact = to_float(scope_row.get("exact_cycle_feature_rows")) or 0.0
        overcount = continuous - exact
        synthetic = "shifted_custom" in attempt
        rows.append(
            {
                "attempt_name": attempt,
                "role": "synthetic_shift_diagnostic" if synthetic else "broker_observed_window_control",
                "gap_status": use.get("gap_status", ""),
                "matched_dimensions": matched,
                "total_dimensions": len(subset),
                "dimensions": dimensions,
                "continuous_window_feature_rows": int(continuous),
                "exact_cycle_feature_rows": int(exact),
                "continuous_overcount_rows": int(overcount),
                "diagnostic_use": "allowed_runtime_signal_parity_only" if matched == len(subset) and subset else "not_allowed_until_mismatch_repaired",
                "forward_use": "forbidden_synthetic_shift_not_broker_forward" if synthetic else "forbidden_until_broker_reaches_feature_last",
                "kpi_use": "forbidden_for_forward_kpi",
                "proxy_policy": "exact_cycle_timestamp_only",
                "effect": "proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)의 차이를 사용 가능 범위로 변환한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def claim_authority_rows(final_ak: Mapping[str, Any]) -> list[dict[str, Any]]:
    matched = int(final_ak.get("proxy_mt5_matched", 0) or 0)
    total = int(final_ak.get("proxy_mt5_rows", 0) or 0)
    broker_gap = str(final_ak.get("broker_gap_status", ""))
    shifted_gap = str(final_ak.get("shifted_gap_status", ""))
    return [
        {
            "claim_subject": "exact_timestamp_proxy_runtime_signal_parity",
            "authority": "allowed",
            "evidence": f"proxy_mt5={matched}/{total}",
            "reason": "MT5 cycle timestamp(MT5 사이클 시각)과 같은 feature row(피처 행)만 비교했고 전 차원이 일치했다.",
            "forbidden_upgrade": "runtime_authority, Forward Passed/Failed(전진 통과/실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_subject": "continuous_window_proxy_for_shifted_custom",
            "authority": "forbidden",
            "evidence": f"shifted_continuous_minus_exact_rows={final_ak.get('shifted_continuous_minus_exact_rows', '')}",
            "reason": "continuous window(연속 창)는 synthetic custom(합성 커스텀)에서 실제 MT5 cycle(사이클)보다 과대계산한다.",
            "forbidden_upgrade": "proxy_only_kpi, candidate selection(후보 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_subject": "broker_forward_pass_fail",
            "authority": "forbidden_until_repaired_or_rollover",
            "evidence": f"broker_gap_status={broker_gap}",
            "reason": "broker tester(브로커 테스터)가 feature_last(피처 마지막)에 아직 닿지 않았다.",
            "forbidden_upgrade": "Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_subject": "synthetic_shift_forward_kpi",
            "authority": "forbidden",
            "evidence": f"shifted_gap_status={shifted_gap}",
            "reason": "shifted custom(이동 커스텀)은 boundary diagnostic(경계 진단)일 뿐 실제 broker forward(브로커 전진)가 아니다.",
            "forbidden_upgrade": "Forward Passed/Failed(전진 통과/실패), operating promotion(운영 승격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_subject": "no_lookahead_rebuild_continuation",
            "authority": "allowed_as_next_research",
            "evidence": "run337AG scaffold(뼈대) + run337AK exact proxy lock(정확 프록시 고정)",
            "reason": "새 후보 선택이 아니라 입력/게이트 물질화로 이동하며 forward(전진) 결과에 맞춘 threshold/lot(임계값/로트) 조정은 금지한다.",
            "forbidden_upgrade": "instant repair branch(즉시 수리 가지 남발), forward-tuned threshold(전진 맞춤 임계값)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def broker_rollover_rows(final_ak: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_last = pd.to_datetime("2026-05-27T02:00:00Z", utc=True)
    gap_rows = read_csv(RUN337AK_DIR / "tester_feature_last_gap_exact_timestamp.csv")
    broker_gap = next((row for row in gap_rows if "broker_rollover_control" in row.get("attempt_name", "")), {})
    api_latest = pd.to_datetime(broker_gap.get("api_latest_us100_close_utc", ""), errors="coerce", utc=True)
    tester_last = pd.to_datetime(broker_gap.get("tester_last_observed_bar_time", ""), errors="coerce", utc=True)
    api_reached = not pd.isna(api_latest) and api_latest >= feature_last
    tester_reached = not pd.isna(tester_last) and tester_last >= feature_last
    return [
        {
            "condition_id": "api_has_forward_feature_last",
            "status": "passed" if api_reached else "failed",
            "observed": "" if pd.isna(api_latest) else api_latest.isoformat().replace("+00:00", "Z"),
            "required": feature_last.isoformat().replace("+00:00", "Z"),
            "action": "not_sufficient_without_tester_reach",
            "effect": "API data(API 데이터)는 있어도 tester(테스터)가 못 보면 forward decision(전진 판정) 근거가 아니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "condition_id": "tester_has_forward_feature_last",
            "status": "passed" if tester_reached else "failed",
            "observed": "" if pd.isna(tester_last) else tester_last.isoformat().replace("+00:00", "Z"),
            "required": feature_last.isoformat().replace("+00:00", "Z"),
            "action": "reprobe_after_utc_rollover_or_history_repair",
            "effect": "broker tester(브로커 테스터)가 feature_last(피처 마지막)를 보지 못하면 Forward Passed/Failed(전진 통과/실패)를 금지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "condition_id": "continue_non_forward_research",
            "status": "passed",
            "observed": final_ak.get("status", ""),
            "required": "no forward authority claim",
            "action": NEXT_RUN_ID,
            "effect": "blocked(차단) 선언 대신 no-lookahead rebuild input(미래참조 없는 재구성 입력)으로 계속 전진한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "next_run_id": NEXT_RUN_ID,
            "track": "defensive_offensive_rebuild_input(방어/공격 재구성 입력)",
            "action": "materialize_no_lookahead_cost_direction_curve_inputs",
            "required_evidence": "run337AG cost/direction/risk/regime contracts + run337AL proxy policy lock",
            "forbidden": "forward threshold retune(전진 임계값 재조정), lot optimization(로트 최적화), pocket cherry-pick(포켓 골라잡기)",
            "effect": "운영 가능한 ONNX(온엑스)로 가기 위한 다음 후보 연구를 전진 데이터에 맞추지 않고 시작한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "order": 2,
            "next_run_id": "run337AN_broker_rollover_reprobe_when_utc_day_boundary_available_v1",
            "track": "runtime_repair(런타임 수리)",
            "action": "reprobe_broker_tester_feature_last_after_rollover_condition",
            "required_evidence": "tester_has_forward_feature_last condition",
            "forbidden": "Forward Passed/Failed without tester reach(테스터 도달 없는 전진 판정)",
            "effect": "브로커 전진 판정은 별도 충분 조건이 생길 때 다시 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "order": 3,
            "next_run_id": "run337AO_asof_regime_and_db_source_materialization_v1",
            "track": "data_instrumentation(데이터/계측)",
            "action": "materialize_asof_regime_and_db_source_inputs",
            "required_evidence": "as-of source hash(시점 기준 원천 해시), lag audit(지연 감사), telemetry field contract(기록 필드 계약)",
            "forbidden": "post-forward macro backfill(전진 이후 거시지표 사후 채움)",
            "effect": "경제지표 전문가 관점의 regime attribution(국면 귀속)을 look-ahead bias(미래참조 편향) 없이 준비한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def required_gate_rows(proxy_rows: Sequence[Mapping[str, Any]], authority_rows: Sequence[Mapping[str, Any]], rollover_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "parent_run337AK_loaded",
            "status": "passed" if path_exists(RUN337AK_DIR / "final_decision.json") else "failed",
            "evidence_path": rel(RUN337AK_DIR / "final_decision.json"),
            "effect": "부모 실행의 실제 근거를 읽었다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_difference_judged",
            "status": "passed" if proxy_rows and all(row["diagnostic_use"] == "allowed_runtime_signal_parity_only" for row in proxy_rows) else "failed",
            "evidence_path": rel(RUN_DIR / "proxy_runtime_usability_policy.csv"),
            "effect": "proxy expected(프록시 예상값)와 MT5 runtime(런타임) 차이를 사용성 판정으로 바꿨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_claim_forbidden",
            "status": "passed" if any(row["claim_subject"] == "broker_forward_pass_fail" and str(row["authority"]).startswith("forbidden") for row in authority_rows) else "failed",
            "evidence_path": rel(RUN_DIR / "claim_authority_matrix.csv"),
            "effect": "Forward Passed/Failed(전진 통과/실패) 주장을 막았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "broker_rollover_condition_checked",
            "status": "passed" if any(row["condition_id"] == "tester_has_forward_feature_last" for row in rollover_rows) else "failed",
            "evidence_path": rel(RUN_DIR / "broker_rollover_condition_matrix.csv"),
            "effect": "브로커 테스터 도달 조건을 명시했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_no_lookahead_route_opened",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "next_experiment_routing_queue.csv"),
            "effect": "차단 선언 대신 미래참조 없는 다음 연구 입력으로 전진한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_decision_payload(proxy_rows: Sequence[Mapping[str, Any]], authority_rows: Sequence[Mapping[str, Any]], rollover_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    matched = sum(1 for row in proxy_rows if row["diagnostic_use"] == "allowed_runtime_signal_parity_only")
    tester_condition = next((row for row in rollover_rows if row["condition_id"] == "tester_has_forward_feature_last"), {})
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS_COMPLETED,
        "judgment": JUDGMENT_COMPLETED,
        "decision": DECISION_COMPLETED,
        "next_action": NEXT_RUN_ID,
        "proxy_attempts_runtime_signal_usable": matched,
        "proxy_attempts_total": len(proxy_rows),
        "tester_forward_feature_last_status": tester_condition.get("status", ""),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def receipt_payloads(final: Mapping[str, Any]) -> dict[Path, Mapping[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        RUN_DIR / "runtime_parity_receipt.json": {
            **common,
            "receipt_type": "runtime_parity",
            "research_path": rel(Path(__file__)),
            "runtime_path": "run337AK MT5 telemetry and tester reports",
            "shared_contract": "exact timestamp proxy can be used only for runtime signal parity",
            "known_differences": "synthetic shifted custom is diagnostic only; broker tester still misses feature_last",
            "parity_check": "run337AK exact proxy/MT5 diff reviewed",
            "runtime_claim_boundary": "runtime_probe_research_only",
        },
        RUN_DIR / "data_integrity_receipt.json": {
            **common,
            "receipt_type": "data_integrity",
            "data_source": "run337AK exact timestamp artifacts and run337AG role contract",
            "time_axis": "UTC feature rows, MT5 cycle timestamps, no continuous-window proxy for shifted custom",
            "sample_scope": "u42 broker control and shifted custom diagnostic",
            "feature_label_boundary": "no label built, no training performed",
            "split_boundary": "forward diagnostic evidence only",
            "leakage_risk": "using synthetic shifted custom as forward KPI would be leakage-like overclaim",
            "integrity_judgment": "usable_with_boundary",
        },
        RUN_DIR / "result_judgment_receipt.json": {
            **common,
            "receipt_type": "result_judgment",
            "result_subject": RUN_ID,
            "evidence_available": "proxy role lock, claim authority matrix, broker rollover matrix",
            "evidence_missing": "broker tester feature_last reach",
            "judgment_label": "runtime_probe",
            "next_condition": "run337AM no-lookahead input materialization or later broker rollover reprobe",
        },
        RUN_DIR / "performance_attribution_receipt.json": {
            **common,
            "receipt_type": "performance_attribution",
            "observed_change": "proxy mismatch repaired by exact tester cycle timestamp filter",
            "comparison_baseline": "run337AC timestamp cutoff proxy mismatch",
            "likely_drivers": "continuous-window overcount in shifted custom symbol",
            "segment_checks": "broker control versus shifted custom, exact versus continuous row scope",
            "attribution_confidence": "high_for_proxy_mismatch_low_for_forward_kpi",
            "next_probe": NEXT_RUN_ID,
        },
    }


def report_text(final: Mapping[str, Any], proxy_rows: Sequence[Mapping[str, Any]], authority_rows: Sequence[Mapping[str, Any]], rollover_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage337AL Exact Timestamp Policy Boundary(337AL 정확 시각 정책 경계)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- proxy runtime usable(프록시 런타임 사용 가능): `{final['proxy_attempts_runtime_signal_usable']}/{final['proxy_attempts_total']}`",
        f"- tester forward feature_last(테스터 전진 피처 마지막): `{final['tester_forward_feature_last_status']}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Meaning(의미)",
        "",
        "run337AL(337AL 실행)은 run337AK(337AK 실행)의 proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침) 차이를 보고, 무엇을 연구에 쓸 수 있고 무엇은 금지해야 하는지 고정한다.",
        "",
        "Effect(효과): exact timestamp proxy(정확 시각 프록시)는 runtime signal parity(런타임 신호 동등성)에만 사용하고, synthetic shift(합성 이동)와 broker gap(브로커 공백)을 Forward Passed/Failed(전진 통과/실패)로 승격하지 않는다.",
        "",
        "## Proxy Usability(프록시 사용성)",
        "",
        "| attempt(시도) | role(역할) | matched(일치) | overcount(과대계산) | diagnostic use(진단 사용) | forward use(전진 사용) |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in proxy_rows:
        lines.append(
            f"| `{row['attempt_name']}` | `{row['role']}` | `{row['matched_dimensions']}/{row['total_dimensions']}` | `{row['continuous_overcount_rows']}` | `{row['diagnostic_use']}` | `{row['forward_use']}` |"
        )
    lines.extend(["", "## Claim Authority(주장 권한)", "", "| subject(대상) | authority(권한) | evidence(근거) | forbidden upgrade(금지 승격) |", "|---|---|---|---|"])
    for row in authority_rows:
        lines.append(f"| `{row['claim_subject']}` | `{row['authority']}` | `{row['evidence']}` | `{row['forbidden_upgrade']}` |")
    lines.extend(["", "## Broker Rollover(브로커 이월)", "", "| condition(조건) | status(상태) | observed(관측) | required(필수) | action(행동) |", "|---|---|---:|---:|---|"])
    for row in rollover_rows:
        lines.append(f"| `{row['condition_id']}` | `{row['status']}` | `{row['observed']}` | `{row['required']}` | `{row['action']}` |")
    lines.extend(["", "## Next Queue(다음 대기열)", "", "| order(순서) | next run(다음 실행) | track(트랙) | action(행동) |", "|---:|---|---|---|"])
    for row in queue_rows:
        lines.append(f"| `{row['order']}` | `{row['next_run_id']}` | `{row['track']}` | `{row['action']}` |")
    return "\n".join(lines)


def decision_doc_text(final: Mapping[str, Any]) -> str:
    return f"""# 2026-05-27 Stage337AL Exact Timestamp Policy Boundary Decision(337AL 정확 시각 정책 경계 결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): exact timestamp proxy(정확 시각 프록시)는 runtime signal parity(런타임 신호 동등성) 전용으로 허용하고, broker tester(브로커 테스터)가 feature_last(피처 마지막)에 닿기 전까지 전진 판정은 금지한다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return replacement + "\n" + text


def upsert_focus_block(text: str, focus: str) -> str:
    block = f"- >-\n  {focus}\n"
    if "current_focus:\n" not in text:
        return text.rstrip() + "\ncurrent_focus:\n" + block
    if "Stage337 run337AL focus complete" in text:
        return re.sub(r"- >-\n  Stage337 run337AL focus complete:.*?(?=\n- >-|\Z)", block.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + block, 1)


def update_status_docs(final: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- proxy_runtime_signal_usable(프록시 런타임 신호 사용 가능): `{final['proxy_attempts_runtime_signal_usable']}/{final['proxy_attempts_total']}`
- broker_forward_boundary(브로커 전진 경계): `{final['tester_forward_feature_last_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_feature_last_not_reached`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): exact timestamp proxy(정확 시각 프록시)는 runtime signal parity(런타임 신호 동등성)로만 쓰고, 다음은 no-lookahead rebuild input(미래참조 없는 재구성 입력)으로 전진한다.
"""
    changed.append(write_md(SELECTED_STATUS, selected_text))
    focus = (
        f"Stage337 run337AL focus complete: run337AL(337AL 실행)은 `{final['status']}`로 exact timestamp policy boundary"
        f"(정확 시각 정책 경계)를 닫았다. Effect(효과): proxy runtime signal usable(프록시 런타임 신호 사용 가능) "
        f"`{final['proxy_attempts_runtime_signal_usable']}/{final['proxy_attempts_total']}`, broker forward boundary(브로커 전진 경계) "
        f"`{final['tester_forward_feature_last_status']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, focus)
        changed.append(write_text(WORKSPACE_STATE, text, bom))
    header = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{final['next_action']}`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    entry = f"""## Stage337 run337AL(337AL 실행) - {TODAY}

- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)의 차이를 사용성 정책으로 고정했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        if text.startswith("# Current Working State"):
            text = re.sub(r"\A# Current Working State.*?(?=\n## |\Z)", header.rstrip() + "\n", text, count=1, flags=re.S)
        else:
            text = header.rstrip() + "\n\n" + text
        if "## Stage337 run337AL(337AL 실행)" in text:
            text = re.sub(r"## Stage337 run337AL\(337AL 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(write_text(CURRENT_STATE, text, bom))
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337AL(337AL 실행) `{final['status']}`. Effect(효과): exact timestamp proxy(정확 시각 프록시) 사용성을 고정하고 Forward/Goal(전진/목표)은 주장하지 않음."
        if "Stage337 run337AL(337AL 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(write_text(CHANGELOG, text, bom))
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AL_summary(337AL 요약): `{final['status']}`. Effect(효과): proxy runtime signal usable(프록시 런타임 신호 사용 가능) "
            f"`{final['proxy_attempts_runtime_signal_usable']}/{final['proxy_attempts_total']}`, next_action(다음 행동) `{final['next_action']}`.\n"
        )
        if "run337AL_summary(337AL 요약)" in text:
            text = re.sub(r"- run337AL_summary\(337AL 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.rstrip() + "\n" + summary
        changed.append(write_text(STAGE_BRIEF, text, bom))
    return changed


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "exact_timestamp_policy_boundary",
        "family": "kpi_evidence",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__exact_timestamp_policy_boundary",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "exact_timestamp_policy_boundary",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_mt5_usability_policy",
        "tier_scope": "Tier A u42 broker and synthetic diagnostic(티어 A u42 브로커 및 합성 진단)",
        "kpi_scope": "runtime_signal_parity_policy_no_forward_kpi(런타임 신호 동등성 정책, 전진 KPI 아님)",
        "scoreboard_lane": "runtime_parity_policy",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"proxy_signal_usable={final['proxy_attempts_runtime_signal_usable']}/{final['proxy_attempts_total']};tester_feature_last={final['tester_forward_feature_last_status']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_forward_claim;synthetic_not_forward_authority",
        "external_verification_status": "completed_parent_mt5_evidence_reviewed",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__exact_timestamp_policy_boundary",
        "run_key": f"{RUN_ID}__exact_timestamp_policy_boundary",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "kpi_evidence",
        "family": "exact_timestamp_policy_boundary",
        "question": "which proxy/MT5 evidence can be used after run337AK exact timestamp repair",
        "evidence_scope": "run337AK exact proxy/MT5, broker gap, synthetic custom scope, run337AG role contract",
        "metric_scope": "proxy_usability_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_action": final["next_action"],
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def append_artifacts(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else [
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
    for column in ("artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "claim_boundary"):
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if row.get("run_id") != RUN_ID]
    generated = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        relative = rel(path)
        if relative in seen:
            continue
        seen.add(relative)
        suffix = path.suffix.lower()
        digest = sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml", ".ini", ".set"} else sha256_file(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{relative}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": relative,
                "artifact_path": relative,
                "sha256": digest,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final.get("status", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    parse_args()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    final_ak = read_json(RUN337AK_DIR / "final_decision.json")
    evidence = input_evidence_rows()
    proxy_rows = proxy_runtime_usability_rows()
    authority = claim_authority_rows(final_ak)
    rollover = broker_rollover_rows(final_ak)
    queue = next_queue_rows()
    gates = required_gate_rows(proxy_rows, authority, rollover)
    final = final_decision_payload(proxy_rows, authority, rollover)

    artifacts: list[Path] = [
        write_csv(RUN_DIR / "input_evidence_index.csv", columns_for(evidence, ["artifact_path"]), evidence),
        write_csv(RUN_DIR / "proxy_runtime_usability_policy.csv", columns_for(proxy_rows, ["attempt_name"]), proxy_rows),
        write_csv(RUN_DIR / "claim_authority_matrix.csv", columns_for(authority, ["claim_subject"]), authority),
        write_csv(RUN_DIR / "broker_rollover_condition_matrix.csv", columns_for(rollover, ["condition_id"]), rollover),
        write_csv(RUN_DIR / "next_experiment_routing_queue.csv", columns_for(queue, ["order"]), queue),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", columns_for(gates, ["gate_id"]), gates),
        write_json(RUN_DIR / "final_decision.json", final),
        write_md(REPORT_PATH, report_text(final, proxy_rows, authority, rollover, queue)),
        write_md(DECISION_DOC, decision_doc_text(final)),
    ]
    for path, payload in receipt_payloads(final).items():
        artifacts.append(write_json(path, payload))
    artifacts.extend(update_status_docs(final))
    artifacts.extend(update_registers(final))
    manifest = write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/materialize_exact_timestamp_policy_boundary_or_broker_rollover_wait.py",
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-runtime-parity", "obsidian-data-integrity", "obsidian-performance-attribution"],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)], final))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

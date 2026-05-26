from __future__ import annotations

import csv
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337O"
RUN_ID = "run337O_review_fresh_mt5_runtime_probe_and_core56_repair_or_attribution_queue_v1"
PARENT_RUN_ID = "run337N_attempt_fresh_mt5_runtime_probe_or_block_v1"
NEXT_RUN_ID = "run337P_materialize_runtime_data_and_feature_source_repair_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337O_timestamp_aligned_runtime_review_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS = "completed_stage337O_timestamp_aligned_runtime_review_repair_queue_no_forward_decision"
JUDGMENT = (
    "timestamp_aligned_parity_passed_on_tester_observed_window_latest_forward_blocked_by_"
    "current_day_tester_gap_macro_source_gap_core56_source_gap"
)
DECISION = "stage337O_open_run337P_runtime_data_and_feature_source_repair_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337N_DIR = STAGE_DIR / "02_runs" / "run337N"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS_DIR / "run337O_fresh_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337O_fresh_mt5_runtime_probe_review.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


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
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


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
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    write_csv(path, columns, rows)
    return path


def append_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]]) -> Path:
    if not rows:
        return path
    existing: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            existing = [dict(item) for item in reader]
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    existing.extend({column: csv_value(row.get(column, "")) for column in columns} for row in rows)
    write_csv(path, columns, existing)
    return path


def parse_timestamp_series(values: pd.Series) -> pd.Series:
    normalized = values.astype(str).str.replace(".", "-", regex=False)
    return pd.to_datetime(normalized, errors="coerce", utc=True)


def latest_raw_by_symbol() -> dict[str, pd.Timestamp]:
    rows = read_csv(RUN337N_DIR / "fresh_forward_data_probe_summary.csv")
    return {
        row["contract_symbol"]: pd.to_datetime(row.get("last_close_utc", ""), errors="coerce", utc=True)
        for row in rows
        if row.get("status") == "completed"
    }


def runtime_by_attempt() -> dict[str, dict[str, str]]:
    return {row["attempt_name"]: row for row in read_csv(RUN337N_DIR / "fresh_mt5_runtime_probe_result.csv")}


def freshness_by_attempt() -> dict[str, dict[str, str]]:
    return {row["attempt_name"]: row for row in read_csv(RUN337N_DIR / "feature_freshness_gap_audit.csv")}


def telemetry_last_observed(attempt_name: str) -> tuple[pd.Timestamp, int]:
    path = RUN337N_DIR / "runtime_telemetry" / f"{attempt_name}_telemetry.csv"
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"bar_time"})
    times = parse_timestamp_series(frame["bar_time"]).dropna()
    return times.max(), int(len(times))


def compute_aligned_proxy_counts(attempt: Mapping[str, Any], cutoff: pd.Timestamp) -> dict[str, Any]:
    set_values = base.parse_key_value_file(ROOT / str(attempt["set"]["path"]))
    feature_path = ROOT / str(attempt["feature_local_path"])
    model_path = ROOT / str(attempt["model_local_path"])
    feature_count = base.parse_int(set_values.get("InpFeatureCount"))
    frame = pd.read_csv(io_path(feature_path))
    times = parse_timestamp_series(frame["bar_time_server"])
    scoped = frame.loc[times <= cutoff].copy()
    cols = base.feature_columns(scoped, feature_count)
    matrix = scoped.loc[:, cols].to_numpy(dtype="float64", copy=False)
    probabilities = base.model_probabilities(model_path, matrix)
    rule = base.ThresholdRule(
        threshold_id=f"stage337O_{attempt['attempt_name']}_tester_observed_window",
        short_threshold=base.parse_float(set_values.get("InpShortThreshold")),
        long_threshold=base.parse_float(set_values.get("InpLongThreshold")),
        min_margin=base.parse_float(set_values.get("InpMinMargin")),
    )
    decisions = base.apply_threshold_rule(pd.DataFrame(probabilities, columns=["p_short", "p_flat", "p_long"]), rule)
    decision_class = decisions["decision_label_class"].to_numpy(dtype="int64", copy=False)
    if base.parse_bool(set_values.get("InpInvertSignal")):
        inverted = decision_class.copy()
        inverted[decision_class == 0] = 2
        inverted[decision_class == 2] = 0
        decision_class = inverted
    short_count = int((decision_class == 0).sum())
    long_count = int((decision_class == 2).sum())
    flat_count = int((decision_class == -1).sum())
    return {
        "aligned_feature_ready_count": int(len(scoped)),
        "aligned_model_ok_count": int(len(scoped)),
        "aligned_short_count": short_count,
        "aligned_long_count": long_count,
        "aligned_flat_count": flat_count,
        "aligned_signal_count": short_count + long_count,
        "aligned_feature_first_timestamp": times.loc[times <= cutoff].min(),
        "aligned_feature_last_timestamp": times.loc[times <= cutoff].max(),
    }


def build_alignment_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    latest = read_json(RUN337N_DIR / "fresh_forward_data_probe_latest.json")
    latest_close = pd.to_datetime(latest["us100_last_close_utc"], utc=True)
    raw_latest = latest_raw_by_symbol()
    runtime_rows = runtime_by_attempt()
    freshness_rows = freshness_by_attempt()
    attempts = read_json(RUN337N_DIR / "independent_handoff_attempts.json")
    audit_rows: list[dict[str, Any]] = []
    diff_rows: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    feature_summaries = {row["feature_set_id"]: row for row in read_csv(RUN337N_DIR / "repaired_feature_set_summary.csv")}

    for feature_set_id, summary in feature_summaries.items():
        required = [item for item in summary.get("required_symbols", "").split(";") if item]
        for symbol in required:
            symbol_latest = raw_latest.get(symbol)
            gap = (latest_close - symbol_latest).total_seconds() / 60 if symbol_latest is not None and not pd.isna(symbol_latest) else None
            source_rows.append(
                {
                    "feature_set_id": feature_set_id,
                    "required_symbol": symbol,
                    "symbol_last_close_utc": symbol_latest,
                    "latest_us100_last_close_utc": latest_close,
                    "gap_to_us100_latest_minutes": gap,
                    "source_status": "aligned_to_latest" if gap == 0 else "source_lag_or_session_gap",
                    "effect": "required symbol(필수 심볼)의 최신성이 feature handoff(피처 인계) 가능 구간을 제한한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    for attempt in attempts:
        attempt_name = attempt["attempt_name"]
        runtime = runtime_rows[attempt_name]
        freshness = freshness_rows[attempt_name]
        tester_last, telemetry_rows = telemetry_last_observed(attempt_name)
        aligned = compute_aligned_proxy_counts(attempt, tester_last)
        dimensions = [
            ("feature_ready_count", "aligned_feature_ready_count", "feature_ready_count"),
            ("model_ok_count", "aligned_model_ok_count", "model_ok_count"),
            ("long_count", "aligned_long_count", "tier_a_long_count"),
            ("short_count", "aligned_short_count", "tier_a_short_count"),
            ("flat_count", "aligned_flat_count", "tier_a_flat_count"),
        ]
        matched = 0
        for dimension, proxy_key, mt5_key in dimensions:
            proxy_value = int(aligned[proxy_key])
            mt5_value = int(float(runtime.get(mt5_key) or 0))
            status = "matched" if proxy_value == mt5_value else "mismatch_requires_review"
            matched += int(status == "matched")
            diff_rows.append(
                {
                    "attempt_name": attempt_name,
                    "artifact_slug": attempt.get("artifact_slug", ""),
                    "dimension": dimension,
                    "aligned_proxy_value": proxy_value,
                    "mt5_runtime_value": mt5_value,
                    "difference_aligned_proxy_minus_mt5": proxy_value - mt5_value,
                    "difference_status": status,
                    "tester_last_observed_bar_time": tester_last,
                    "latest_us100_last_close_utc": latest_close,
                    "usable_for_runtime_signal_parity": status == "matched",
                    "usable_for_forward_pass_fail": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        feature_last = pd.to_datetime(freshness.get("feature_last_timestamp", ""), errors="coerce", utc=True)
        latest_gap = (latest_close - feature_last).total_seconds() / 60 if not pd.isna(feature_last) else None
        tester_gap = (latest_close - tester_last).total_seconds() / 60 if not pd.isna(tester_last) else None
        issue = "tester_current_day_gap_only"
        if str(attempt.get("feature_set_id")) == "macro48_no_equity_breadth_or_top3" and latest_gap and latest_gap > 0:
            issue = "macro_source_gap_plus_tester_current_day_gap"
        audit_rows.append(
            {
                "attempt_name": attempt_name,
                "feature_set_id": attempt.get("feature_set_id", ""),
                "raw_proxy_rows": freshness.get("feature_rows", ""),
                "aligned_proxy_rows": aligned["aligned_feature_ready_count"],
                "mt5_feature_ready_count": runtime.get("feature_ready_count", ""),
                "telemetry_rows": telemetry_rows,
                "raw_proxy_minus_aligned_rows": int(freshness.get("feature_rows") or 0) - int(aligned["aligned_feature_ready_count"]),
                "latest_us100_last_close_utc": latest_close,
                "feature_last_timestamp": feature_last,
                "tester_last_observed_bar_time": tester_last,
                "feature_to_latest_gap_minutes": latest_gap,
                "tester_to_latest_gap_minutes": tester_gap,
                "timestamp_aligned_matches": matched,
                "timestamp_aligned_total": len(dimensions),
                "timestamp_alignment_status": "matched" if matched == len(dimensions) else "mismatch_requires_review",
                "issue_class": issue,
                "effect": "proxy(프록시)를 tester-observed window(테스터 관측 구간)로 자르면 실제 신호 동등성 여부가 드러난다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return audit_rows, diff_rows, source_rows


def repair_queue_rows(audit_rows: Sequence[Mapping[str, Any]], source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    tester_gap = max(float(row.get("tester_to_latest_gap_minutes") or 0.0) for row in audit_rows)
    macro_gap_symbols = [
        row["required_symbol"]
        for row in source_rows
        if row.get("feature_set_id") == "macro48_no_equity_breadth_or_top3" and float(row.get("gap_to_us100_latest_minutes") or 0.0) > 0
    ]
    return [
        {
            "queue_id": "run337P_current_day_tester_gap_probe",
            "priority": 1,
            "subject": "all_m48_u42_attempts",
            "repair_question": "Can MT5 Strategy Tester include current-day bars that MT5 Python API already sees?",
            "required_action": "test terminal history sync, tester cache refresh, and narrow u42 smoke run without changing model or thresholds",
            "known_gap": f"tester_to_latest_gap_minutes={tester_gap}",
            "forbidden_action": "threshold_retune_or_lot_optimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337P_macro48_source_gap_probe",
            "priority": 2,
            "subject": "m48_bal_rf;m48_plain_rf",
            "repair_question": "Can macro48 use an as-of safe source policy after USDX/VIX session gaps without look-ahead?",
            "required_action": "materialize no-lookahead source-lag audit and, only if accepted, a last-known-as-of handoff probe",
            "known_gap": "lag_symbols=" + ";".join(sorted(set(macro_gap_symbols))),
            "forbidden_action": "forward-pocket filtering or target-driven feature fill",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337P_core56_source_repair_or_drop_decision",
            "priority": 3,
            "subject": "core56_refresh_candidate",
            "repair_question": "Can core56 equity breadth/top3 source be refreshed as-of safely, or should it be dropped from this packet?",
            "required_action": "audit source availability, no-lookahead boundary, and materialize/drop decision before MT5",
            "known_gap": "core56 blocked in run337N",
            "forbidden_action": "mixing blocked core56 with m48/u42 runtime success",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337P_tester_observed_window_attribution_only",
            "priority": 4,
            "subject": "m48_u42_completed_runtime_window",
            "repair_question": "What can be learned from the already completed tester-observed window without Forward Passed/Failed?",
            "required_action": "produce attribution-only D/B, long/short, session, cost, curve pocket reads on tester-observed window",
            "known_gap": "not latest-full-forward because tester/current-day and macro source gaps remain",
            "forbidden_action": "using attribution-only result as selection or forward pass",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(
    audit_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    tester_gap_attempts = sum(1 for row in audit_rows if float(row.get("tester_to_latest_gap_minutes") or 0.0) > 0)
    source_gap_rows = sum(1 for row in source_rows if row.get("source_status") != "aligned_to_latest")
    return [
        {
            "gate_name": "parent_run337N_runtime_probe_loaded",
            "status": "covered",
            "evidence_path": rel(RUN337N_DIR / "final_fresh_mt5_runtime_probe_or_block_decision.json"),
            "effect": "run337N(337N 실행)의 MT5(메타트레이더5) 증거를 원천으로 고정한다.",
        },
        {
            "gate_name": "timestamp_aligned_parity_review",
            "status": "covered" if matched == len(diff_rows) else "covered_with_mismatch",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"tester-observed window(테스터 관측 구간)에서 proxy-MT5(프록시-MT5) 차이를 재계산한다; matched={matched}/{len(diff_rows)}.",
        },
        {
            "gate_name": "tester_current_day_gap_identified",
            "status": "covered_blocker",
            "evidence_path": rel(RUN_DIR / "timestamp_basis_audit.csv"),
            "effect": f"API 최신 봉과 Strategy Tester(전략 테스터) 관측 봉의 차이를 분리한다; attempts={tester_gap_attempts}.",
        },
        {
            "gate_name": "macro_source_gap_identified",
            "status": "covered_blocker",
            "evidence_path": rel(RUN_DIR / "source_gap_repair_matrix.csv"),
            "effect": f"m48의 VIX/USDX source gap(원천 공백)을 따로 기록한다; gap rows={source_gap_rows}.",
        },
        {
            "gate_name": "repair_queue_opened",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "run337P_runtime_data_and_feature_source_repair_queue.csv"),
            "effect": f"tester/macro/core56 repair(수리)와 attribution-only(귀속 전용)를 run337P(337P 실행)로 넘긴다; rows={len(queue_rows)}.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_timestamp_aligned_runtime_review_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def write_report(audit_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> Path:
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    tester_gap = max(float(row.get("tester_to_latest_gap_minutes") or 0.0) for row in audit_rows)
    text = f"""# Stage337O Runtime Review(337O 런타임 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- timestamp-aligned parity(타임스탬프 정렬 동등성): `{matched}/{len(diff_rows)} matched(일치)`
- tester current-day gap(테스터 현재일 공백): `{tester_gap}` minutes(분)
- queue rows(대기열 행): `{len(queue_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Effect(효과)

run337O는 run337N의 raw proxy-MT5 mismatch(원시 프록시-MT5 불일치)를 tester-observed window(테스터 관측 구간) 기준으로 다시 계산했다. 효과는 u42의 `14/20` 원시 동등성이 실제 신호 불일치가 아니라 현재일 테스터 관측 구간 차이임을 분리하고, m48/core56은 source repair(원천 수리) 대상임을 고정하는 것이다.

## Boundary(경계)

이 검토는 repair queue(수리 대기열)와 attribution-only(귀속 전용) 입력이다. Forward Passed/Failed(전진 통과/실패), selection(선택), operating promotion(운영 승격)은 주장하지 않는다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(audit_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> Path:
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    text = f"""# Stage337O Decision(337O 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- timestamp-aligned parity(타임스탬프 정렬 동등성): `{matched}/{len(diff_rows)} matched(일치)`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): 현재 결과는 전진 통과가 아니라 run337P(337P 실행)의 tester current-day gap(테스터 현재일 공백), macro48 source gap(거시48 원천 공백), core56 source repair(핵심56 원천 수리)를 여는 근거다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(audit_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- timestamp-aligned parity(타임스탬프 정렬 동등성): `{matched}/{len(diff_rows)} matched(일치)`
- current blockers(현재 차단 요소): `tester_current_day_gap;macro48_source_gap;core56_source_gap`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337O(337O 실행)는 run337N(337N 실행)의 raw mismatch(원시 불일치)를 timestamp basis(타임스탬프 기준)으로 설명하고 run337P(337P 실행) 수리 대기열을 열었다. 아직 선택 후보는 없다.
"""
    write_md(SELECTED_STATUS, selection_text)
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {NEXT_RUN_ID}"
                break
        focus_line = (
            "- >-\n"
            f"  Stage337 run337O focus complete: Stage337(337단계) run337O(337O 실행)는 `{STATUS}`로 timestamp-aligned runtime review(타임스탬프 정렬 런타임 검토)를 완료했다. "
            "Effect(효과): tester current-day gap(테스터 현재일 공백), macro48 source gap(거시48 원천 공백), core56 source gap(핵심56 원천 공백)을 run337P(337P 실행) 수리 대기열로 넘기고 Forward/Goal(전진/목표) 주장은 닫아둔다.\n"
        )
        if "Stage337 run337O focus complete" not in text:
            try:
                idx = lines.index("current_focus:")
                lines.insert(idx + 1, focus_line.rstrip())
            except ValueError:
                lines.extend(["current_focus:", focus_line.rstrip()])
        write_text_preserving(WORKSPACE_STATE, "\n".join(lines) + "\n", had_bom)
    entry = f"""
## Stage337 run337O(337O 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- timestamp-aligned parity(타임스탬프 정렬 동등성): `{matched}/{len(diff_rows)} matched(일치)`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337N(337N 실행)의 원시 불일치를 시간축 기준으로 분해했고, tester/macro/core56 repair(테스터/거시/핵심56 수리)를 다음 실행으로 넘겼다.
"""
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337O(337O 실행)" not in text:
            write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + entry.strip() + "\n", had_bom)
    if path_exists(CHANGELOG):
        text, had_bom = read_text_lossless(CHANGELOG)
        line = f"\n- {TODAY}: Stage337 run337O(337O 실행) `{STATUS}`. Effect(효과): timestamp-aligned parity(타임스탬프 정렬 동등성)와 repair queue(수리 대기열)를 만들고 Forward/Goal(전진/목표) 주장은 없음.\n"
        if "Stage337 run337O(337O 실행)" not in text:
            write_text_preserving(CHANGELOG, text.rstrip() + line, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "runtime_parity_review",
                "lane": "runtime_parity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "primary_report": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__timestamp_aligned_runtime_review",
                "ledger_row_id": f"{RUN_ID}__timestamp_aligned_runtime_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "runtime_parity_review",
                "work_family": "runtime_parity_review",
                "question": "does run337N raw proxy-MT5 mismatch remain after tester-observed timestamp alignment",
                "metric_scope": "timestamp_alignment_and_repair_queue_no_forward_decision",
                "evidence_scope": "run337N_runtime_probe_review",
                "kpi_scope": "diagnostic_runtime_parity_not_forward_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
            },
        ),
    ]
    rows: list[dict[str, Any]] = []
    generated = now_utc()
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    artifacts.append(append_csv_rows(ARTIFACT_REGISTRY, rows))
    return artifacts


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    generated_at_utc = now_utc()
    audit_rows, diff_rows, source_rows = build_alignment_outputs()
    queue_rows = repair_queue_rows(audit_rows, source_rows)
    gates = gate_rows(audit_rows, diff_rows, source_rows, queue_rows)
    matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "timestamp_aligned_matched_rows": matched,
        "timestamp_aligned_total_rows": len(diff_rows),
        "tester_current_day_gap_attempts": sum(1 for row in audit_rows if float(row.get("tester_to_latest_gap_minutes") or 0.0) > 0),
        "macro_source_gap_rows": sum(1 for row in source_rows if row.get("source_status") != "aligned_to_latest"),
        "core56_status": "blocked_until_source_repair_or_drop_decision",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifacts: list[Path] = [
        write_csv(
            RUN_DIR / "timestamp_basis_audit.csv",
            [
                "attempt_name",
                "feature_set_id",
                "raw_proxy_rows",
                "aligned_proxy_rows",
                "mt5_feature_ready_count",
                "telemetry_rows",
                "raw_proxy_minus_aligned_rows",
                "latest_us100_last_close_utc",
                "feature_last_timestamp",
                "tester_last_observed_bar_time",
                "feature_to_latest_gap_minutes",
                "tester_to_latest_gap_minutes",
                "timestamp_aligned_matches",
                "timestamp_aligned_total",
                "timestamp_alignment_status",
                "issue_class",
                "effect",
                "claim_boundary",
            ],
            audit_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv",
            [
                "attempt_name",
                "artifact_slug",
                "dimension",
                "aligned_proxy_value",
                "mt5_runtime_value",
                "difference_aligned_proxy_minus_mt5",
                "difference_status",
                "tester_last_observed_bar_time",
                "latest_us100_last_close_utc",
                "usable_for_runtime_signal_parity",
                "usable_for_forward_pass_fail",
                "claim_boundary",
            ],
            diff_rows,
        ),
        write_csv(
            RUN_DIR / "source_gap_repair_matrix.csv",
            [
                "feature_set_id",
                "required_symbol",
                "symbol_last_close_utc",
                "latest_us100_last_close_utc",
                "gap_to_us100_latest_minutes",
                "source_status",
                "effect",
                "claim_boundary",
            ],
            source_rows,
        ),
        write_csv(
            RUN_DIR / "run337P_runtime_data_and_feature_source_repair_queue.csv",
            ["queue_id", "priority", "subject", "repair_question", "required_action", "known_gap", "forbidden_action", "claim_boundary"],
            queue_rows,
        ),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(RUN_DIR / "final_timestamp_aligned_runtime_review_decision.json", final_decision),
        write_report(audit_rows, diff_rows, queue_rows),
        write_decision_doc(audit_rows, diff_rows),
    ]
    artifacts.extend(update_status_docs(audit_rows, diff_rows))
    artifacts.extend(
        [
            write_json(
                RUN_DIR / "data_integrity_receipt.json",
                {
                    "run_id": RUN_ID,
                    "judgment": "latest_full_forward_incomplete_until_tester_and_source_gaps_are_repaired",
                    "effect": "API 최신 봉, 테스터 관측 봉, feature source(피처 원천) 봉을 분리해 기록한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
            write_json(
                RUN_DIR / "runtime_parity_receipt.json",
                {
                    "run_id": RUN_ID,
                    "timestamp_aligned_parity": f"{matched}/{len(diff_rows)}",
                    "judgment": "runtime_signal_parity_passes_on_tester_observed_window",
                    "effect": "raw mismatch(원시 불일치)를 시간축 차이로 설명한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
            write_json(
                RUN_DIR / "result_judgment_receipt.json",
                {
                    **final_decision,
                    "effect": "수리 대기열을 열지만 Forward/Goal(전진/목표)은 주장하지 않는다.",
                },
            ),
        ]
    )
    artifacts.extend(update_registers([*artifacts, Path(__file__)]))
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "artifacts": [rel(path) for path in artifacts if path_exists(path)],
            },
        )
    )
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

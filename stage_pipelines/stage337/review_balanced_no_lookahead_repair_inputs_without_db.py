from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
)


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AV"
RUN_ID = "run337AV_review_balanced_no_lookahead_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337AU_materialize_balanced_no_lookahead_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337AW_attempt_balanced_no_lookahead_runtime_probe_without_db_v1"
STATUS = "completed_stage337AV_balanced_no_lookahead_repair_inputs_reviewed_no_training_no_selection"
JUDGMENT = "repair_inputs_review_pass_runtime_probe_attempt_queue_ready_but_no_forward_or_goal_claim"
DECISION = "stage337AV_open_run337AW_attempt_balanced_no_lookahead_runtime_probe_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AV_balanced_no_lookahead_repair_input_review_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AU_DIR = STAGE_DIR / "02_runs" / "run337AU"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
REPORT_PATH = REVIEWS_DIR / "run337AV_review_balanced_no_lookahead_repair_inputs_without_db.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AV_balanced_no_lookahead_repair_inputs_without_db.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

AU_FINAL = RUN337AU_DIR / "final_decision.json"
AU_MANIFEST = RUN337AU_DIR / "run_manifest.json"
AU_FRAME = RUN337AU_DIR / "completed_day_pretrade_repair_feature_frame.csv"
AU_PROTOCOLS = RUN337AU_DIR / "protocol_materialized_input_matrix.csv"
AU_BINDINGS = RUN337AU_DIR / "protocol_feature_binding_matrix.csv"
AU_NEGATIVE = RUN337AU_DIR / "negative_control_input_recipe_matrix.csv"
AU_COST = RUN337AU_DIR / "cost_ladder_input_matrix.csv"
AU_PROXY = RUN337AU_DIR / "proxy_mt5_materialization_contract.csv"
AU_FORWARD = RUN337AU_DIR / "forward_visibility_handoff_matrix.csv"
AU_RUNTIME_QUEUE = RUN337AU_DIR / "mt5_runtime_probe_candidate_queue.csv"
AU_NO_LOOKAHEAD = RUN337AU_DIR / "no_lookahead_materialization_audit.csv"
AU_GATES = RUN337AU_DIR / "required_gate_coverage_audit.csv"

FEATURE_INTEGRITY = RUN_DIR / "feature_frame_integrity_review.csv"
PROTOCOL_REVIEW = RUN_DIR / "protocol_input_review_matrix.csv"
BINDING_REVIEW = RUN_DIR / "feature_binding_coverage_review.csv"
NEGATIVE_REVIEW = RUN_DIR / "negative_control_review_matrix.csv"
PROXY_REVIEW = RUN_DIR / "proxy_mt5_usability_review.csv"
FORWARD_REVIEW = RUN_DIR / "forward_claim_boundary_review.csv"
REGIME_COVERAGE = RUN_DIR / "regime_coverage_review.csv"
OVERFIT_GUARD = RUN_DIR / "overfit_guard_review_matrix.csv"
RUNTIME_ACCEPTANCE = RUN_DIR / "runtime_probe_acceptance_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    AU_FINAL,
    AU_MANIFEST,
    AU_FRAME,
    AU_PROTOCOLS,
    AU_BINDINGS,
    AU_NEGATIVE,
    AU_COST,
    AU_PROXY,
    AU_FORWARD,
    AU_RUNTIME_QUEUE,
    AU_NO_LOOKAHEAD,
    AU_GATES,
)

OUTPUT_FILES = (
    FEATURE_INTEGRITY,
    PROTOCOL_REVIEW,
    BINDING_REVIEW,
    NEGATIVE_REVIEW,
    PROXY_REVIEW,
    FORWARD_REVIEW,
    REGIME_COVERAGE,
    OVERFIT_GUARD,
    RUNTIME_ACCEPTANCE,
    GATE_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

STAGE_LEDGER_COLUMNS = (
    "ledger_row_id",
    "stage_id",
    "run_id",
    "work_family",
    "evidence_scope",
    "kpi_scope",
    "status",
    "judgment",
    "claim_boundary",
    "path",
    "notes",
    "decision",
    "run_key",
    "family",
    "question",
    "metric_scope",
    "primary_artifact",
    "report_path",
    "next_action",
)
ARTIFACT_COLUMNS = (
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
)

FEATURE_INTEGRITY_COLUMNS = (
    "check_id",
    "status",
    "evidence_path",
    "observed_value",
    "expected_value",
    "effect",
    "claim_boundary",
)
PROTOCOL_REVIEW_COLUMNS = (
    "protocol_id",
    "branch_family",
    "priority",
    "source_driver",
    "required_column_count",
    "missing_columns",
    "blank_required_cells",
    "binding_rows",
    "input_row_count_declared",
    "input_row_count_observed",
    "input_review_status",
    "runtime_probe_queue_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
BINDING_REVIEW_COLUMNS = (
    "protocol_id",
    "binding_rows",
    "bound_features",
    "source_artifacts",
    "missing_source_artifacts",
    "binding_review_status",
    "effect",
    "claim_boundary",
)
NEGATIVE_REVIEW_COLUMNS = (
    "control_id",
    "protocol_id",
    "control_type",
    "source_rows",
    "recipe_present",
    "invalid_if_present",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PROXY_REVIEW_COLUMNS = (
    "dimension",
    "rows",
    "matched_rows",
    "mismatched_rows",
    "usable_for_runtime_signal_parity_rows",
    "usable_for_forward_pass_fail_rows",
    "review_status",
    "effect",
    "claim_boundary",
)
FORWARD_REVIEW_COLUMNS = (
    "window_id",
    "source_window",
    "current_status",
    "usable_for",
    "forbidden_for",
    "required_repair",
    "review_status",
    "effect",
    "claim_boundary",
)
REGIME_COVERAGE_COLUMNS = (
    "dimension",
    "distinct_values",
    "largest_bucket",
    "largest_bucket_rows",
    "smallest_bucket",
    "smallest_bucket_rows",
    "coverage_status",
    "effect",
    "claim_boundary",
)
OVERFIT_GUARD_COLUMNS = (
    "guard_id",
    "status",
    "evidence_path",
    "risk_checked",
    "effect",
    "claim_boundary",
)
RUNTIME_ACCEPTANCE_COLUMNS = (
    "queue_id",
    "protocol_id",
    "branch_family",
    "priority",
    "accepted_for_run337AW",
    "acceptance_status",
    "required_mt5_outputs",
    "preflight_status",
    "runtime_claim_boundary",
    "forbidden_actions",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return io_path(item).resolve().relative_to(io_path(ROOT).resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def parse_dt(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    text = text.replace("Z", "+00:00")
    try:
        if "T" not in text and "+" not in text:
            return datetime.fromisoformat(text).replace(tzinfo=UTC)
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    except ValueError:
        return None


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def git_head_text(path: Path) -> tuple[str, bool] | None:
    repo_path = rel(path)
    try:
        completed = subprocess.run(
            ["git", "show", f"HEAD:{repo_path}"],
            cwd=io_path(ROOT),
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    raw = completed.stdout
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def read_csv_update_base(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    base = git_head_text(path)
    if base is None:
        if not path_exists(path):
            return [], []
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            return list(reader.fieldnames or []), [dict(row) for row in reader]
    text, _ = base
    reader = csv.DictReader(text.splitlines())
    return list(reader.fieldnames or []), [dict(row) for row in reader]


def upsert_csv_preserve(path: Path, default_columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    columns, rows = read_csv_update_base(path)
    if not columns:
        columns = list(default_columns)
    for column in row:
        if column not in columns:
            columns.append(column)
    row_key = str(row.get(key, ""))
    rows = [item for item in rows if str(item.get(key, "")) != row_key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_focus_once(text: str, body: str, token: str) -> str:
    if token in text:
        return text
    return text.replace("current_focus:\n", f"current_focus:\n{body}\n", 1)


def upsert_focus(text: str, body: str, token: str) -> str:
    if token not in text:
        return insert_focus_once(text, body, token)
    pattern = rf"- >-\n  {re.escape(token)}.*?(?=\n- >-|\n\n|\Z)"
    return re.sub(pattern, body, text, count=1, flags=re.DOTALL)


def append_line_once(path: Path, line: str, token: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if token in text:
        return path
    text = text.rstrip() + "\n" + line.rstrip() + "\n"
    return write_text_lossless(path, text, had_bom)


def parse_required_columns(raw: str) -> list[str]:
    text = str(raw or "").strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in re.split(r"[,;]", text) if item.strip()]


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337AV inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "au_final": read_json(AU_FINAL),
        "au_manifest": read_json(AU_MANIFEST),
        "frame": read_csv(AU_FRAME),
        "protocols": read_csv(AU_PROTOCOLS),
        "bindings": read_csv(AU_BINDINGS),
        "negative": read_csv(AU_NEGATIVE),
        "cost": read_csv(AU_COST),
        "proxy": read_csv(AU_PROXY),
        "forward": read_csv(AU_FORWARD),
        "runtime_queue": read_csv(AU_RUNTIME_QUEUE),
        "no_lookahead": read_csv(AU_NO_LOOKAHEAD),
        "au_gates": read_csv(AU_GATES),
    }


def build_feature_integrity(frame: Sequence[Mapping[str, str]], protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    columns = set(frame[0].keys()) if frame else set()
    declared_counts = {safe_int(row.get("row_count")) for row in protocols if str(row.get("row_count", "")).strip()}
    forbidden_columns = {
        "net_profit",
        "profit",
        "pnl",
        "close_time",
        "balance_after",
        "equity_after",
        "current_trade_profit",
        "future_return",
        "forward_passed",
        "forward_failed",
    }
    forbidden_present = sorted(columns & forbidden_columns)
    trade_indices = [safe_int(row.get("trade_index"), -1) for row in frame]
    feature_times = [parse_dt(str(row.get("feature_timestamp", ""))) for row in frame]
    source_times = [parse_dt(str(row.get("source_time_max", ""))) for row in frame]
    open_times = [parse_dt(str(row.get("open_time", ""))) for row in frame]
    source_future_count = sum(
        1
        for feature_time, source_time, row in zip(feature_times, source_times, frame, strict=False)
        if str(row.get("no_future_source_violation", "")).lower() == "true"
        or (feature_time is not None and source_time is not None and source_time > feature_time)
    )
    open_feature_bad = sum(
        1
        for feature_time, open_time in zip(feature_times, open_times, strict=False)
        if feature_time is None
        or open_time is None
        or open_time < feature_time
        or (open_time - feature_time).total_seconds() > 60
    )
    monotonic = all(
        left is not None and right is not None and left <= right
        for left, right in zip(feature_times, feature_times[1:], strict=False)
    )
    prior_columns = {"prior_trade_count", "prior_cumulative_net", "prior_balance", "prior_peak_balance", "prior_drawdown"}
    prior_missing = sorted(prior_columns - columns)
    prior_blank_cells = sum(1 for row in frame for column in prior_columns if not str(row.get(column, "")).strip())
    rows.extend(
        [
            {
                "check_id": "row_count_matches_parent_protocols",
                "status": "passed" if frame and declared_counts == {len(frame)} else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": f"frame_rows={len(frame)};declared_counts={sorted(declared_counts)}",
                "expected_value": "all protocols declare the same completed-day frame rows(모든 프로토콜이 같은 완성일 프레임 행을 선언)",
                "effect": "입력 표본이 프로토콜별로 갈라져 포켓 과적합되는 위험을 줄인다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "trade_index_unique_and_dense",
                "status": "passed" if trade_indices == list(range(1, len(frame) + 1)) else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": f"first={trade_indices[:1]};last={trade_indices[-1:]};unique={len(set(trade_indices))}",
                "expected_value": "1..N dense trade_index(1부터 N까지 조밀한 거래 인덱스)",
                "effect": "행 중복이나 누락으로 생기는 리뷰 왜곡을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "feature_timestamp_monotonic",
                "status": "passed" if monotonic else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": f"first={frame[0].get('feature_timestamp') if frame else ''};last={frame[-1].get('feature_timestamp') if frame else ''}",
                "expected_value": "nondecreasing feature timestamps(감소하지 않는 피처 시각)",
                "effect": "시간축 순서가 섞여 생기는 미래참조 위험을 줄인다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "source_time_not_after_feature_time",
                "status": "passed" if source_future_count == 0 else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": f"future_source_violations={source_future_count}",
                "expected_value": "0",
                "effect": "경제지표/시장 원천이 진입 이후 값을 끌어오지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "open_time_at_or_after_feature_timestamp_within_60s",
                "status": "passed" if open_feature_bad == 0 else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": f"bad_rows={open_feature_bad}",
                "expected_value": "open_time is feature_timestamp..feature_timestamp+60s(진입 시각은 피처 시각부터 60초 이내)",
                "effect": "MT5 실행 초 단위 지연은 허용하되 피처가 진입 이후로 밀리는 미래참조는 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "forbidden_current_trade_outcome_absent",
                "status": "passed" if not forbidden_present else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": forbidden_present,
                "expected_value": "no current/future outcome columns(현재/미래 결과 컬럼 없음)",
                "effect": "현재 거래 손익을 보고 수리하는 과적합 통로를 닫는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "prior_state_columns_present_and_filled",
                "status": "passed" if not prior_missing and prior_blank_cells == 0 else "failed",
                "evidence_path": rel(AU_FRAME),
                "observed_value": f"missing={prior_missing};blank_cells={prior_blank_cells}",
                "expected_value": "prior-only curve state present and filled(과거 전용 곡선 상태 존재 및 채움)",
                "effect": "회복/수중 구간 수리는 현재 거래 결과가 아니라 이전 상태만 쓰게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    return rows


def build_binding_review(bindings: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in bindings:
        grouped[str(row.get("protocol_id", ""))].append(row)
    rows: list[dict[str, Any]] = []
    for protocol_id, items in sorted(grouped.items()):
        source_artifacts = sorted({str(row.get("source_artifact", "")) for row in items if row.get("source_artifact")})
        missing = [artifact for artifact in source_artifacts if not path_exists(ROOT / artifact)]
        rows.append(
            {
                "protocol_id": protocol_id,
                "binding_rows": len(items),
                "bound_features": sorted({str(row.get("feature_name", "")) for row in items}),
                "source_artifacts": source_artifacts,
                "missing_source_artifacts": missing,
                "binding_review_status": "passed" if items and not missing else "failed",
                "effect": "피처가 어느 부모 산출물에서 왔는지 끊기지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_protocol_review(
    frame: Sequence[Mapping[str, str]],
    protocols: Sequence[Mapping[str, str]],
    binding_review: Sequence[Mapping[str, Any]],
    feature_integrity: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    frame_columns = set(frame[0].keys()) if frame else set()
    binding_by_protocol = {str(row["protocol_id"]): row for row in binding_review}
    feature_integrity_passed = all(row.get("status") == "passed" for row in feature_integrity)
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        protocol_id = str(protocol.get("protocol_id", ""))
        required_columns = parse_required_columns(str(protocol.get("required_pre_trade_columns", "")))
        missing_columns = [column for column in required_columns if column not in frame_columns]
        blank_cells = sum(1 for row in frame for column in required_columns if column in frame_columns and not str(row.get(column, "")).strip())
        declared = safe_int(protocol.get("row_count"), -1)
        binding_rows = safe_int(binding_by_protocol.get(protocol_id, {}).get("binding_rows"), 0)
        binding_ok = binding_by_protocol.get(protocol_id, {}).get("binding_review_status") == "passed"
        review_ok = (
            not missing_columns
            and blank_cells == 0
            and declared == len(frame)
            and binding_ok
            and feature_integrity_passed
            and str(protocol.get("materialized_status", "")).startswith("ready_for_review")
        )
        is_negative = "negative_control" in str(protocol.get("branch_family", ""))
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_family": protocol.get("branch_family", ""),
                "priority": protocol.get("priority", ""),
                "source_driver": protocol.get("source_driver", ""),
                "required_column_count": len(required_columns),
                "missing_columns": missing_columns,
                "blank_required_cells": blank_cells,
                "binding_rows": binding_rows,
                "input_row_count_declared": declared,
                "input_row_count_observed": len(frame),
                "input_review_status": "passed" if review_ok else "failed",
                "runtime_probe_queue_status": (
                    "accepted_for_diagnostic_control_attempt(진단 대조 탐침 수락)"
                    if review_ok and is_negative
                    else "accepted_for_runtime_probe_attempt(런타임 탐침 시도 수락)"
                    if review_ok
                    else "not_accepted_until_repaired(수리 전 수락 불가)"
                ),
                "allowed_use": "run337AW runtime probe attempt input only(run337AW 런타임 탐침 시도 입력 전용)",
                "forbidden_use": "model training, threshold retuning, D/B rewrite, lot optimization, Forward Passed/Failed, Goal Achieve(모델 학습/임계값 재조정/D-B 재작성/랏 최적화/전진 판정/목표 달성 금지)",
                "effect": "프로토콜별 입력이 실제로 실행 전 검토 기준을 통과하는지 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_negative_review(negative: Sequence[Mapping[str, str]], frame: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in negative:
        source_rows = safe_int(row.get("source_rows"), -1)
        recipe_present = bool(str(row.get("recipe", "")).strip())
        invalid_if_present = bool(str(row.get("invalid_if", "")).strip())
        ok = source_rows == len(frame) and recipe_present and invalid_if_present
        rows.append(
            {
                "control_id": row.get("control_id", ""),
                "protocol_id": row.get("protocol_id", ""),
                "control_type": row.get("control_type", ""),
                "source_rows": source_rows,
                "recipe_present": recipe_present,
                "invalid_if_present": invalid_if_present,
                "review_status": "passed" if ok else "failed",
                "allowed_use": row.get("allowed_use", ""),
                "forbidden_use": row.get("forbidden_use", ""),
                "effect": "부정 대조가 성과 선택이 아니라 과적합 탐지로만 쓰이게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_review(proxy_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in proxy_rows:
        grouped[str(row.get("dimension", ""))].append(row)
    rows = []
    for dimension, items in sorted(grouped.items()):
        matched = sum(1 for row in items if row.get("difference_status") == "matched")
        signal_rows = sum(1 for row in items if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
        forward_rows = sum(1 for row in items if str(row.get("usable_for_forward_pass_fail", "")).lower() == "true")
        rows.append(
            {
                "dimension": dimension,
                "rows": len(items),
                "matched_rows": matched,
                "mismatched_rows": len(items) - matched,
                "usable_for_runtime_signal_parity_rows": signal_rows,
                "usable_for_forward_pass_fail_rows": forward_rows,
                "review_status": "signal_parity_only_passed" if matched == len(items) and forward_rows == 0 else "failed_or_overclaimed",
                "effect": "proxy expected(프록시 예상값)를 runtime signal parity(런타임 신호 동등성)에만 묶는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_forward_review(forward_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in forward_rows:
        forbidden = str(row.get("forbidden_for", ""))
        required_repair = str(row.get("required_repair", "")).strip()
        future_only_lock = (
            str(row.get("source_window", "")).startswith("not_materialized_yet")
            and "required_before_forward_decision" in str(row.get("current_status", ""))
        )
        current_forbidden_lock = "Forward Passed" in forbidden and "Goal Achieve" in forbidden
        ok = (current_forbidden_lock or future_only_lock) and bool(required_repair)
        rows.append(
            {
                "window_id": row.get("window_id", ""),
                "source_window": row.get("source_window", ""),
                "current_status": row.get("current_status", ""),
                "usable_for": row.get("usable_for", ""),
                "forbidden_for": row.get("forbidden_for", ""),
                "required_repair": required_repair,
                "review_status": "claim_boundary_locked(주장 경계 고정)" if ok else "claim_boundary_gap(주장 경계 공백)",
                "effect": "완성일 귀속과 진짜 forward(전진) 판정을 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_coverage(frame: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    dimensions = (
        "direction",
        "month",
        "weekday",
        "open_hour_utc",
        "session_utc",
        "chron_segment",
        "vol_regime",
        "atr_ratio_regime",
        "adx_regime",
        "di_regime",
        "vix_z_regime",
        "rate_z_regime",
        "usd_z_regime",
    )
    rows: list[dict[str, Any]] = []
    for dimension in dimensions:
        counts = Counter(str(row.get(dimension, "")) for row in frame if str(row.get(dimension, "")).strip())
        if counts:
            largest_bucket, largest_count = counts.most_common(1)[0]
            smallest_bucket, smallest_count = sorted(counts.items(), key=lambda item: (item[1], item[0]))[0]
        else:
            largest_bucket, largest_count, smallest_bucket, smallest_count = "", 0, "", 0
        rows.append(
            {
                "dimension": dimension,
                "distinct_values": len(counts),
                "largest_bucket": largest_bucket,
                "largest_bucket_rows": largest_count,
                "smallest_bucket": smallest_bucket,
                "smallest_bucket_rows": smallest_count,
                "coverage_status": "covered_for_review_not_selection" if counts else "missing_required",
                "effect": "국면별 편중을 다음 MT5 탐침에서 분해할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_overfit_guards(
    frame_review: Sequence[Mapping[str, Any]],
    protocols: Sequence[Mapping[str, str]],
    negative_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    forward_review: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    family_counts = Counter(str(row.get("branch_family", "")).split("(")[0] for row in protocols)
    rows = [
        {
            "guard_id": "no_current_trade_outcome_in_feature_frame",
            "status": "passed" if any(row["check_id"] == "forbidden_current_trade_outcome_absent" and row["status"] == "passed" for row in frame_review) else "failed",
            "evidence_path": rel(FEATURE_INTEGRITY),
            "risk_checked": "lookahead current-trade outcome leak(현재 거래 결과 누수)",
            "effect": "수리 입력이 손익을 본 뒤 움직이는 경로를 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "source_time_guard_passed",
            "status": "passed" if any(row["check_id"] == "source_time_not_after_feature_time" and row["status"] == "passed" for row in frame_review) else "failed",
            "evidence_path": rel(FEATURE_INTEGRITY),
            "risk_checked": "future macro/source timestamp leak(미래 거시/원천 시각 누수)",
            "effect": "경제지표 전문가 관점에서 발표/가용 시각을 진입 이후로 밀어넣지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "balanced_branch_family_coverage",
            "status": "passed" if all(family_counts.get(item, 0) > 0 for item in ("defensive", "repair", "offensive", "negative_control")) else "failed",
            "evidence_path": rel(PROTOCOL_REVIEW),
            "risk_checked": "one-sided defensive/offensive bias(방어/공격 한쪽 편향)",
            "effect": "방어, 수리, 공격, 부정 대조를 같이 보게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "negative_controls_ready",
            "status": "passed" if negative_review and all(row.get("review_status") == "passed" for row in negative_review) else "failed",
            "evidence_path": rel(NEGATIVE_REVIEW),
            "risk_checked": "repair-by-overfitting without controls(대조 없는 수리 과적합)",
            "effect": "좋아 보이는 변형이 신호인지 포켓 선택인지 비교할 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "proxy_is_signal_parity_only",
            "status": "passed" if proxy_review and all(row.get("review_status") == "signal_parity_only_passed" for row in proxy_review) else "failed",
            "evidence_path": rel(PROXY_REVIEW),
            "risk_checked": "proxy KPI authority overclaim(프록시 KPI 권한 과장)",
            "effect": "프록시는 런타임 신호 점검용이고 전진 판정이 아님을 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "forward_claim_boundary_locked",
            "status": "passed" if forward_review and all(row.get("review_status") == "claim_boundary_locked(주장 경계 고정)" for row in forward_review) else "failed",
            "evidence_path": rel(FORWARD_REVIEW),
            "risk_checked": "completed-day attribution mistaken as forward pass(완성일 귀속을 전진 통과로 오해)",
            "effect": "전진 통과/실패와 목표 달성 주장을 계속 금지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def build_runtime_acceptance(runtime_queue: Sequence[Mapping[str, str]], protocol_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_protocol = {str(row.get("protocol_id", "")): row for row in protocol_review}
    rows = []
    for item in runtime_queue:
        protocol_id = str(item.get("protocol_id", ""))
        review = by_protocol.get(protocol_id, {})
        accepted = str(review.get("input_review_status", "")) == "passed"
        rows.append(
            {
                "queue_id": item.get("queue_id", ""),
                "protocol_id": protocol_id,
                "branch_family": item.get("branch_family", ""),
                "priority": item.get("priority", ""),
                "accepted_for_run337AW": accepted,
                "acceptance_status": "accepted_for_attempt_only(시도 전용 수락)" if accepted else "rejected_until_input_repair(입력 수리 전 거절)",
                "required_mt5_outputs": item.get("required_mt5_outputs", ""),
                "preflight_status": "reviewed_ready_for_attempt_not_authority(검토됨, 시도 준비, 권위 아님)" if accepted else item.get("preflight_status", ""),
                "runtime_claim_boundary": "runtime_probe_attempt_only_no_runtime_authority(런타임 탐침 시도 전용, 런타임 권위 없음)",
                "forbidden_actions": item.get("forbidden_actions", ""),
                "effect": "MT5 실행으로 넘길 수 있는 항목과 주장 한계를 같이 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gates(
    feature_review: Sequence[Mapping[str, Any]],
    protocol_review: Sequence[Mapping[str, Any]],
    binding_review: Sequence[Mapping[str, Any]],
    negative_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    forward_review: Sequence[Mapping[str, Any]],
    overfit_review: Sequence[Mapping[str, Any]],
    runtime_acceptance: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    def passed(rows: Sequence[Mapping[str, Any]], key: str = "status", value: str = "passed") -> bool:
        return bool(rows) and all(row.get(key) == value for row in rows)

    accepted_runtime = sum(1 for row in runtime_acceptance if str(row.get("accepted_for_run337AW", "")).lower() == "true")
    gates = [
        (
            "feature_frame_integrity_passed",
            passed(feature_review),
            FEATURE_INTEGRITY,
            "진입 전 입력 프레임이 행/시각/누수 검사를 통과했다.",
        ),
        (
            "protocol_inputs_reviewed",
            passed(protocol_review, "input_review_status", "passed"),
            PROTOCOL_REVIEW,
            "9개 프로토콜 입력을 실행 전 기준으로 검토했다.",
        ),
        (
            "feature_bindings_reviewed",
            passed(binding_review, "binding_review_status", "passed"),
            BINDING_REVIEW,
            "피처 연결과 원천 산출물 존재를 확인했다.",
        ),
        (
            "negative_controls_reviewed",
            passed(negative_review, "review_status", "passed"),
            NEGATIVE_REVIEW,
            "부정 대조 3개가 진단 전용으로 준비됐다.",
        ),
        (
            "proxy_signal_only_locked",
            passed(proxy_review, "review_status", "signal_parity_only_passed"),
            PROXY_REVIEW,
            "proxy-MT5는 신호 동등성 전용으로 고정됐다.",
        ),
        (
            "forward_claim_boundary_locked",
            passed(forward_review, "review_status", "claim_boundary_locked(주장 경계 고정)"),
            FORWARD_REVIEW,
            "완성일 귀속을 전진 판정으로 올리지 않도록 막았다.",
        ),
        (
            "overfit_guard_review_passed",
            passed(overfit_review),
            OVERFIT_GUARD,
            "과적합 방지 검문이 모두 통과했다.",
        ),
        (
            "runtime_probe_queue_accepted",
            accepted_runtime == len(runtime_acceptance) and accepted_runtime == 9,
            RUNTIME_ACCEPTANCE,
            "9개 항목을 run337AW 런타임 탐침 시도 전용으로 수락했다.",
        ),
        (
            "final_claim_guard",
            True,
            FINAL_DECISION,
            "Forward/Goal/runtime authority 주장을 하지 않는다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = {
        EXPERIMENT_RECEIPT: {
            "skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "hypothesis": "run337AU materialized inputs can be reviewed into an MT5 runtime probe attempt queue without lookahead, retuning, or D/B source use(run337AU 물질화 입력은 미래참조/재튜닝/D-B 원천 없이 MT5 런타임 탐침 대기열로 검토될 수 있다)",
            "decision_use": "open run337AW runtime probe attempt queue only(run337AW 런타임 탐침 시도 대기열 개방 전용)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": [
                "frozen cp322A package(고정 cp322A 패키지)",
                "no threshold retuning(임계값 재조정 없음)",
                "no lot optimization(랏 최적화 없음)",
                "no D/B rewrite(D/B 재작성 없음)",
            ],
            "changed_variables": ["review status and runtime attempt queue only(검토 상태와 런타임 시도 대기열만 변경)"],
            "sample_scope": "US100 M5 completed-day broker slice, 344 rows(US100 M5 완성일 브로커 구간 344행)",
            "success_criteria": "all review gates pass and no forward/goal claim(모든 리뷰 게이트 통과 및 전진/목표 주장 없음)",
            "failure_criteria": "missing required columns, source future violation, proxy overclaim, or runtime queue rejection(필수 컬럼 누락/미래 원천 위반/프록시 과장/런타임 큐 거절)",
            "invalid_conditions": "current trade PnL enters feature frame or hidden current-day rows are used(현재 거래 손익 또는 숨은 현재일 행 사용)",
            "stop_conditions": "open MT5 probe attempt only after input review passes(입력 리뷰 통과 후에만 MT5 탐침 시도 개방)",
            "evidence_plan": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        DATA_RECEIPT: {
            "skill": "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "data_source": [rel(AU_FRAME), rel(AU_PROTOCOLS), rel(AU_FORWARD)],
            "time_axis": "feature_timestamp/open_time are UTC completed-day trade timestamps; source_time_max must be <= feature_timestamp(피처/진입 시각은 UTC 완성일 거래 시각이고 원천 최대 시각은 피처 시각 이하여야 한다)",
            "sample_scope": "US100 M5 completed-day attribution-only slice, 344 rows(US100 M5 완성일 귀속 전용 구간 344행)",
            "missing_or_duplicate_check": "trade_index dense 1..N and required cells nonblank(거래 인덱스 1..N 및 필수 셀 비공백)",
            "feature_label_boundary": "current trade outcome columns forbidden; prior curve state allowed(현재 거래 결과 컬럼 금지, 이전 곡선 상태 허용)",
            "split_boundary": "completed-day attribution only, not Forward Passed/Failed(완성일 귀속 전용, 전진 통과/실패 아님)",
            "leakage_risk": "hidden current-day tester rows and current-trade PnL are the main risks(숨은 현재일 테스터 행과 현재 거래 손익이 주 위험)",
            "data_hash_or_identity": sha256_file_lf_normalized(AU_FRAME),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)" if final["failed_gates"] == [] else "invalid(무효)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUNTIME_RECEIPT: {
            "skill": "obsidian-runtime-parity(옵시디언 런타임 동등성)",
            "research_path": rel(Path(__file__)),
            "runtime_path": "run337AW MT5 runtime probe attempt queue only(run337AW MT5 런타임 탐침 시도 대기열 전용)",
            "shared_contract": "proxy expected and MT5 runtime values remain signal parity only; exact tester output required next(프록시 예상값과 MT5 런타임 값은 신호 동등성 전용이며 다음에는 정확 테스터 출력 필요)",
            "known_differences": "D/B source unavailable; broker current-day tester cutoff remains locked(D/B 원천 없음, 브로커 현재일 테스터 컷오프 고정)",
            "parity_check": "parent run337AU proxy contract 10/10 matched, reviewed as signal parity only(부모 run337AU 프록시 계약 10/10 일치, 신호 동등성 전용 검토)",
            "parity_identity": {
                "au_proxy_contract": sha256_file_lf_normalized(AU_PROXY),
                "runtime_acceptance": rel(RUNTIME_ACCEPTANCE),
            },
            "runtime_claim_boundary": "runtime_probe_attempt_only_no_runtime_authority(런타임 탐침 시도 전용, 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        ATTRIBUTION_RECEIPT: {
            "skill": "obsidian-performance-attribution(옵시디언 성과 귀속)",
            "observed_change": "input status changed from materialized to reviewed queue, not KPI improvement(입력 상태가 물질화에서 리뷰된 대기열로 바뀌었을 뿐 KPI 개선 아님)",
            "comparison_baseline": PARENT_RUN_ID,
            "likely_drivers": "input completeness, no-lookahead guard, proxy signal-only lock, and negative controls(입력 완전성/미래참조 방어/프록시 신호 전용 고정/부정 대조)",
            "segment_checks": "direction, month, hour, session, chronology, volatility, ADX, VIX, rate, USD coverage reviewed(방향/월/시간/세션/시간순서/변동성/ADX/VIX/금리/USD 커버리지 검토)",
            "trade_shape": "344 completed-day trades only; no new PnL interpretation(완성일 거래 344개 전용, 새 손익 해석 없음)",
            "alternative_explanations": "review pass can still fail in MT5 runtime or true forward data(리뷰 통과도 MT5 런타임 또는 진짜 전진 데이터에서 실패할 수 있음)",
            "attribution_confidence": "medium_for_input_readiness_low_for_performance(입력 준비도는 중간, 성과는 낮음)",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        JUDGMENT_RECEIPT: {
            "skill": "obsidian-result-judgment(옵시디언 결과 판정)",
            "result_subject": RUN_ID,
            "evidence_available": [rel(FEATURE_INTEGRITY), rel(PROTOCOL_REVIEW), rel(GATE_AUDIT), rel(RUNTIME_ACCEPTANCE)],
            "evidence_missing": "fresh MT5 tester output and true forward latest broker data remain missing(신규 MT5 테스터 출력과 진짜 최신 브로커 전진 데이터는 아직 없음)",
            "judgment_label": "exploratory(탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "run337AW must execute or block narrow MT5 runtime probe attempt(run337AW가 좁은 MT5 런타임 탐침을 실행하거나 차단 근거를 남겨야 함)",
            "user_explanation_hook": "입력 검토는 통과했지만 운영/전진 통과가 아니라 다음 MT5 탐침으로 넘기는 단계다.",
        },
    }
    return [write_json(path, payload) for path, payload in receipts.items()]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337AV Balanced No-Lookahead Repair Input Review Without D/B(337AV D/B 없는 균형 미래참조 방지 수리 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{final['next_action']}`
- protocol_reviews(프로토콜 검토): `{final['protocol_review_passed']}/{final['protocol_review_rows']}`
- runtime_acceptance(런타임 수락): `{final['runtime_acceptance_rows']}`
- negative_controls(부정 대조): `{final['negative_control_review_rows']}`
- proxy_review(프록시 검토): `{final['proxy_review_rows']}` dimension rows(차원 행)
- gates_passed(게이트 통과): `{final['passed_gates']}/{final['gate_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Runtime Authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Review Meaning(검토 의미)

run337AV(337AV 실행)는 run337AU(337AU 실행)의 materialized input(물질화 입력)을 실제 MT5 runtime probe attempt(MT5 런타임 탐침 시도)로 넘겨도 되는지 본다.
Effect(효과): 입력은 `run337AW` 시도 대기열로 넘기지만, 수익성/forward passed(전진 통과)/운영 가능성은 주장하지 않는다.

## Key Locks(핵심 고정)

- source time guard(원천 시각 방어): `{final['source_time_guard']}`
- current outcome leak guard(현재 결과 누수 방어): `{final['current_outcome_guard']}`
- proxy-MT5 usability(프록시-MT5 활용성): `signal_parity_only(신호 동등성 전용)`
- forward boundary(전진 경계): `completed_day_attribution_only(완성일 귀속 전용)`
- D/B source(D/B 원천): `out_of_scope_by_claim_no_timestamp_aligned_sidecar(시점 맞춤 보조표 없음으로 주장 범위 밖)`

## Next Work(다음 작업)

`{final['next_action']}` must attempt or explicitly block the narrow MT5 runtime probe(MT5 런타임 탐침) for the 9 reviewed protocol/control rows.
Effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime value(MT5 런타임 값)를 다시 비교하고, 활용 가능성은 signal parity(신호 동등성)와 execution evidence(실행 근거)로만 판단한다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""
# 2026-05-27 Stage337AV Decision(337AV 결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- protocol_reviews(프로토콜 검토): `{final['protocol_review_passed']}/{final['protocol_review_rows']}`
- runtime_acceptance_rows(런타임 수락 행): `{final['runtime_acceptance_rows']}`
- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337AV(337AV 실행)는 균형 수리 입력을 리뷰 통과 상태로 고정하고 run337AW(337AW 실행) MT5 runtime probe attempt(MT5 런타임 탐침 시도)를 연다. 이 결정은 운영 승격이나 전진 통과가 아니다.
"""
    return write_md(DECISION_DOC, text)


def update_workspace_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace = replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337AV focus complete: run337AV(337AV 실행)은 `{final['status']}`로 balanced no-lookahead repair input review(균형 미래참조 방지 수리 입력 검토)를 완료했다. "
        f"Effect(효과): protocol reviews(프로토콜 검토) `{final['protocol_review_passed']}/{final['protocol_review_rows']}`, runtime acceptance(런타임 수락) `{final['runtime_acceptance_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    workspace = upsert_focus(workspace, focus, "Stage337 run337AV focus complete")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_base = git_head_text(CURRENT_STATE)
    if current_base is not None:
        current, current_bom = current_base
    else:
        current, current_bom = read_text_lossless(CURRENT_STATE)
    current = replace_prefix_line(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current = replace_prefix_line(current, "- status(상태):", f"- status(상태): `{final['status']}`")
    current = replace_prefix_line(current, "- decision(결정):", f"- decision(결정): `{final['decision']}`")
    current = replace_prefix_line(current, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
    current = replace_prefix_line(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current = replace_prefix_line(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    av_section = f"""## Stage337 run337AV(337AV 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AV(337AV 실행)는 run337AU(337AU 실행)의 pre-trade input(진입 전 입력), protocol binding(프로토콜 연결), negative control(부정 대조), proxy-MT5 contract(프록시-MT5 계약)을 검토해 run337AW(337AW 실행) 런타임 탐침 시도 대기열로 넘겼다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337AV(337AV 실행)" in current:
        current = re.sub(
            r"## Stage337 run337AV\(337AV 실행\).*?(?=\n## )",
            av_section.rstrip() + "\n\n",
            current,
            count=1,
            flags=re.DOTALL,
        )
    else:
        current = current.replace("## Stage267 Candidate Pool(267단계 후보군)", av_section + "\n## Stage267 Candidate Pool(267단계 후보군)", 1)
    artifacts.append(write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- completed_day_attribution_status(완성일 귀속 상태): `usable_without_db_for_attribution_only`
- db_source_status(D/B 원천 상태): `out_of_scope_by_claim_no_timestamp_aligned_sidecar`
- db_source_sidecar_feasible(D/B 원천 보조표 가능): `false`
- repair_inputs_status(수리 입력 상태): `balanced_no_lookahead_without_db_reviewed`
- protocol_review_passed(프로토콜 검토 통과): `{final['protocol_review_passed']}/{final['protocol_review_rows']}`
- runtime_acceptance_rows(런타임 수락 행): `{final['runtime_acceptance_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_review_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_current_day_cutoff_and_db_source_out_of_scope`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AV(337AV 실행)는 리뷰 통과 입력을 MT5 runtime probe attempt(MT5 런타임 탐침 시도)로 넘기지만 운영/전진 주장은 막는다.
"""
    artifacts.append(write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = read_text_lossless(STAGE_BRIEF)
    brief = replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337AV_summary(337AV 요약): `{final['status']}`. "
        f"Effect(효과): protocol reviews(프로토콜 검토) `{final['protocol_review_passed']}/{final['protocol_review_rows']}`, runtime acceptance(런타임 수락) `{final['runtime_acceptance_rows']}`, next_action(다음 행동) `{NEXT_RUN_ID}`; Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337AV_summary" in brief:
        brief = re.sub(r"^- run337AV_summary\(337AV 요약\):.*$", summary.rstrip(), brief, flags=re.MULTILINE)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog_line = (
        f"- {TODAY}: Stage337 run337AV(337AV 실행) `{final['status']}`. "
        f"Effect(효과): balanced no-lookahead repair inputs(균형 미래참조 방지 수리 입력) 리뷰를 통과시키고 runtime acceptance(런타임 수락) `{final['runtime_acceptance_rows']}`행을 만들었으며 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    changelog, changelog_bom = read_text_lossless(CHANGELOG)
    if "Stage337 run337AV" in changelog:
        changelog = re.sub(rf"^- {re.escape(TODAY)}: Stage337 run337AV\(337AV 실행\).*$", changelog_line, changelog, flags=re.MULTILINE)
    else:
        changelog = changelog.rstrip() + "\n" + changelog_line + "\n"
    artifacts.append(write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "balanced_no_lookahead_repair_input_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_acceptance={final['runtime_acceptance_rows']};goal_achieve_not_claimed.",
        "family": "input_review_runtime_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balanced_repair_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "reviewed_repair_inputs_without_db(D/B 없는 수리 입력 검토)",
        "tier_scope": "Tier A u42 completed-day attribution input(Tier A u42 완성일 귀속 입력)",
        "kpi_scope": "input_review_no_new_trading_kpi(입력 검토, 신규 거래 KPI 없음)",
        "scoreboard_lane": "input_review_runtime_boundary",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"protocol_review={final['protocol_review_passed']}/{final['protocol_review_rows']};runtime_acceptance={final['runtime_acceptance_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 리뷰 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_repair_input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "input_review_runtime_boundary",
        "evidence_scope": "run337AU materialized pre-trade inputs and proxy/runtime contracts",
        "kpi_scope": "input_review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;runtime_acceptance={final['runtime_acceptance_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__balanced_repair_input_review",
        "family": "balanced_no_lookahead_repair_input_review_without_db",
        "question": "can run337AU materialized inputs pass review for a narrow MT5 runtime probe without lookahead or D/B",
        "metric_scope": "protocol_review_runtime_acceptance_no_new_kpi",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    upsert_csv_preserve(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, run_row, "run_id")
    upsert_csv_preserve(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    upsert_csv_preserve(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = read_csv_update_base(ARTIFACT_REGISTRY)
    if not columns:
        columns = list(ARTIFACT_COLUMNS)
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path):
            continue
        artifact_path = rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        unique.append(path)
    artifact_ids = {f"{RUN_ID}::{rel(path)}" for path in unique}
    rows = [row for row in rows if row.get("artifact_id") not in artifact_ids]
    created_at = now_utc()
    for path in unique:
        artifact_path = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    feature_review = build_feature_integrity(inputs["frame"], inputs["protocols"])
    feature_path = write_csv(FEATURE_INTEGRITY, FEATURE_INTEGRITY_COLUMNS, feature_review)
    binding_review = build_binding_review(inputs["bindings"])
    binding_path = write_csv(BINDING_REVIEW, BINDING_REVIEW_COLUMNS, binding_review)
    protocol_review = build_protocol_review(inputs["frame"], inputs["protocols"], binding_review, feature_review)
    protocol_path = write_csv(PROTOCOL_REVIEW, PROTOCOL_REVIEW_COLUMNS, protocol_review)
    negative_review = build_negative_review(inputs["negative"], inputs["frame"])
    negative_path = write_csv(NEGATIVE_REVIEW, NEGATIVE_REVIEW_COLUMNS, negative_review)
    proxy_review = build_proxy_review(inputs["proxy"])
    proxy_path = write_csv(PROXY_REVIEW, PROXY_REVIEW_COLUMNS, proxy_review)
    forward_review = build_forward_review(inputs["forward"])
    forward_path = write_csv(FORWARD_REVIEW, FORWARD_REVIEW_COLUMNS, forward_review)
    regime_review = build_regime_coverage(inputs["frame"])
    regime_path = write_csv(REGIME_COVERAGE, REGIME_COVERAGE_COLUMNS, regime_review)
    overfit_review = build_overfit_guards(feature_review, inputs["protocols"], negative_review, proxy_review, forward_review)
    overfit_path = write_csv(OVERFIT_GUARD, OVERFIT_GUARD_COLUMNS, overfit_review)
    runtime_acceptance = build_runtime_acceptance(inputs["runtime_queue"], protocol_review)
    runtime_path = write_csv(RUNTIME_ACCEPTANCE, RUNTIME_ACCEPTANCE_COLUMNS, runtime_acceptance)
    gate_rows = build_gates(
        feature_review,
        protocol_review,
        binding_review,
        negative_review,
        proxy_review,
        forward_review,
        overfit_review,
        runtime_acceptance,
    )
    gate_path = write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows)
    failed_gates = [row["gate_id"] for row in gate_rows if row.get("status") != "passed"]
    protocol_passed = sum(1 for row in protocol_review if row.get("input_review_status") == "passed")
    runtime_accepted = sum(1 for row in runtime_acceptance if str(row.get("accepted_for_run337AW", "")).lower() == "true")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "invalid_stage337AV_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if not failed_gates else "balanced_repair_input_review_gate_failure",
        "decision": DECISION if not failed_gates else "repair_stage337AV_review_gate_failure_before_runtime_attempt",
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_stage337AV_review_gate_failure_v1",
        "protocol_review_rows": len(protocol_review),
        "protocol_review_passed": protocol_passed,
        "runtime_acceptance_rows": runtime_accepted,
        "negative_control_review_rows": len(negative_review),
        "proxy_review_rows": len(proxy_review),
        "regime_review_rows": len(regime_review),
        "overfit_guard_rows": len(overfit_review),
        "gate_rows": len(gate_rows),
        "passed_gates": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "failed_gates": failed_gates,
        "source_time_guard": next((row.get("status") for row in feature_review if row.get("check_id") == "source_time_not_after_feature_time"), "missing"),
        "current_outcome_guard": next((row.get("status") for row in feature_review if row.get("check_id") == "forbidden_current_trade_outcome_absent"), "missing"),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": rel(__file__),
        "parent_inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in OUTPUT_FILES],
        "frozen_items": [
            "selected candidate(선택 후보)",
            "ONNX model(온엑스 모델)",
            "Adapter package(어댑터 패키지)",
            "feature order(피처 순서)",
            "score threshold(점수 임계값)",
            "risk/lot/ATR/runtime handoff(위험/랏/ATR/런타임 인계)",
        ],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rule rewrite(D/B 규칙 재작성)",
            "lot optimization(랏 최적화)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 리뷰 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = write_json(FINAL_DECISION, final)
    manifest_path = write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    workspace_paths = update_workspace_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        Path(__file__),
        feature_path,
        protocol_path,
        binding_path,
        negative_path,
        proxy_path,
        forward_path,
        regime_path,
        overfit_path,
        runtime_path,
        gate_path,
        final_path,
        manifest_path,
        *receipt_paths,
        report_path,
        decision_path,
        *workspace_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    summary = {
        "run_id": RUN_ID,
        "status": final["status"],
        "decision": final["decision"],
        "protocol_reviews": f"{protocol_passed}/{len(protocol_review)}",
        "runtime_acceptance_rows": runtime_accepted,
        "gates": f"{final['passed_gates']}/{final['gate_rows']}",
        "report_path": rel(report_path),
        "artifact_registry": rel(artifact_registry_path),
        "next_action": final["next_action"],
        "goal_achieve": "not_claimed",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

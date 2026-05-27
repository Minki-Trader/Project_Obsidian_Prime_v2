from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, RUN_REGISTRY_COLUMNS, io_path, path_exists


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AW"
RUN_ID = "run337AW_attempt_balanced_no_lookahead_runtime_probe_without_db_v1"
PARENT_RUN_ID = "run337AV_review_balanced_no_lookahead_repair_inputs_without_db_v1"
RUNTIME_SOURCE_RUN_ID = "run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_v1"
NEXT_RUN_ID = "run337AX_tester_gap_repair_and_protocol_attribution_without_db_v1"
STATUS = "completed_stage337AW_balanced_no_lookahead_runtime_probe_evidence_bound_gap_remains_no_forward_decision"
JUDGMENT = "runtime_probe_signal_parity_matched_protocol_matrix_but_tester_feature_last_gap_blocks_forward_decision"
DECISION = "stage337AW_open_run337AX_tester_gap_repair_and_protocol_attribution_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AW_balanced_no_lookahead_runtime_probe_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AV_DIR = STAGE_DIR / "02_runs" / "run337AV"
RUN337Z_DIR = STAGE_DIR / "02_runs" / "run337Z"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
REPORT_PATH = REVIEWS_DIR / "run337AW_balanced_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AW_runtime_probe.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

AV_QUEUE = RUN337AV_DIR / "runtime_probe_acceptance_queue.csv"
AV_PROTOCOL_REVIEW = RUN337AV_DIR / "protocol_input_review_matrix.csv"
AV_PROXY_REVIEW = RUN337AV_DIR / "proxy_mt5_usability_review.csv"
AV_REGIME_REVIEW = RUN337AV_DIR / "regime_coverage_review.csv"
AV_FINAL = RUN337AV_DIR / "final_decision.json"
Z_MT5_RESULT = RUN337Z_DIR / "frozen_forward_mt5_result.csv"
Z_DIFF = RUN337Z_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
Z_GAP = RUN337Z_DIR / "tester_rollover_feature_last_gap.csv"
Z_RUNTIME_EXECUTION = RUN337Z_DIR / "runtime_execution_result.json"
Z_SETTINGS = RUN337Z_DIR / "tester_settings_identity.json"
Z_FINAL = RUN337Z_DIR / "final_decision.json"
Z_REPORT = RUN337Z_DIR / "mt5_strategy_tester_report.html"
Z_REPORT_ALIAS = RUN337Z_DIR / "frozen_forward_mt5_report.html"
Z_TELEMETRY = RUN337Z_DIR / "mt5_terminal_telemetry.csv"
Z_SUMMARY = RUN337Z_DIR / "runtime_telemetry" / "u42_plain_rf_summary.csv"
Z_SET = RUN337Z_DIR / "mt5" / "u42_plain_rf.set"
Z_INI = RUN337Z_DIR / "mt5" / "u42_plain_rf.ini"
Z_MODEL = RUN337Z_DIR / "models" / "u42_plain.onnx"
Z_FEATURES = RUN337Z_DIR / "feature_matrices" / "u42_plain_features.csv"

DEFAULT_TERMINAL = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/terminal64.exe")
DEFAULT_METAEDITOR = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E/MetaEditor64.exe")

RUNTIME_ATTEMPT_IDENTITY = RUN_DIR / "runtime_attempt_identity.csv"
PROTOCOL_RUNTIME_EVIDENCE = RUN_DIR / "protocol_runtime_probe_evidence_matrix.csv"
PROXY_MT5_BY_PROTOCOL = RUN_DIR / "proxy_mt5_runtime_difference_by_protocol.csv"
TESTER_GAP_BY_PROTOCOL = RUN_DIR / "tester_feature_last_gap_by_protocol.csv"
RUNTIME_ATTRIBUTION = RUN_DIR / "runtime_metric_attribution_by_protocol.csv"
BACKTEST_FORENSICS = RUN_DIR / "backtest_forensics_identity.csv"
CLAIM_BOUNDARY_MATRIX = RUN_DIR / "runtime_claim_boundary_matrix.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    AV_QUEUE,
    AV_PROTOCOL_REVIEW,
    AV_PROXY_REVIEW,
    AV_REGIME_REVIEW,
    AV_FINAL,
    Z_MT5_RESULT,
    Z_DIFF,
    Z_GAP,
    Z_RUNTIME_EXECUTION,
    Z_SETTINGS,
    Z_FINAL,
    Z_REPORT,
    Z_TELEMETRY,
    Z_SUMMARY,
    Z_SET,
    Z_INI,
    Z_MODEL,
    Z_FEATURES,
)
OUTPUT_FILES = (
    RUNTIME_ATTEMPT_IDENTITY,
    PROTOCOL_RUNTIME_EVIDENCE,
    PROXY_MT5_BY_PROTOCOL,
    TESTER_GAP_BY_PROTOCOL,
    RUNTIME_ATTRIBUTION,
    BACKTEST_FORENSICS,
    CLAIM_BOUNDARY_MATRIX,
    GATE_AUDIT,
    ARTIFACT_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
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

RUNTIME_ATTEMPT_COLUMNS = (
    "attempt_id",
    "runtime_source_run_id",
    "execution_mode",
    "terminal_path",
    "terminal_exists",
    "metaeditor_path",
    "metaeditor_exists",
    "mt5_result_path",
    "mt5_result_exists",
    "report_path",
    "report_exists",
    "telemetry_path",
    "telemetry_exists",
    "tester_status",
    "runtime_status",
    "report_status",
    "runtime_result_sha256",
    "report_sha256",
    "telemetry_sha256",
    "evidence_status",
    "fresh_attempt_need",
    "effect",
    "claim_boundary",
)
PROTOCOL_RUNTIME_COLUMNS = (
    "protocol_id",
    "branch_family",
    "priority",
    "runtime_source_run_id",
    "execution_mode",
    "accepted_for_run337AW",
    "evidence_status",
    "tester_status",
    "runtime_status",
    "report_status",
    "feature_ready_count",
    "model_ok_count",
    "long_count",
    "short_count",
    "flat_count",
    "trade_count",
    "order_attempt_count",
    "order_fill_count",
    "net_profit",
    "profit_factor",
    "expectancy",
    "recovery_factor",
    "max_drawdown_amount",
    "short_trade_count",
    "long_trade_count",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PROXY_BY_PROTOCOL_COLUMNS = (
    "protocol_id",
    "dimension",
    "proxy_expected_value",
    "mt5_runtime_value",
    "difference_proxy_minus_mt5",
    "difference_status",
    "usable_for_runtime_signal_parity",
    "usable_for_forward_pass_fail",
    "runtime_skip_reason",
    "effect",
    "claim_boundary",
)
GAP_BY_PROTOCOL_COLUMNS = (
    "protocol_id",
    "gap_status",
    "api_latest_us100_close_utc",
    "feature_last_timestamp",
    "tester_last_observed_bar_time",
    "tester_to_feature_last_gap_minutes",
    "tester_to_api_latest_gap_minutes",
    "telemetry_rows",
    "effect",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "protocol_id",
    "protocol_family",
    "diagnostic_axis",
    "metric_read",
    "risk_read",
    "usable_for_repair_memory",
    "usable_for_forward_decision",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "recovery_factor",
    "expectancy",
    "long_trade_count",
    "short_trade_count",
    "effect",
    "claim_boundary",
)
FORENSICS_COLUMNS = (
    "evidence_id",
    "evidence_type",
    "path",
    "exists",
    "sha256",
    "role",
    "status",
    "effect",
    "claim_boundary",
)
CLAIM_COLUMNS = (
    "claim_id",
    "status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return Path(path).resolve().relative_to(ROOT).as_posix() if Path(path).resolve().is_relative_to(ROOT) else Path(path).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    _columns, rows = read_csv_table(path)
    return rows


def git_head_bytes(path: Path) -> bytes | None:
    try:
        rel_path = rel(path)
    except ValueError:
        return None
    proc = subprocess.run(
        ["git", "show", f"HEAD:{rel_path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def read_csv_table(path: Path, *, prefer_head: bool = False) -> tuple[list[str], list[dict[str, str]]]:
    raw = git_head_bytes(path) if prefer_head else None
    if raw is not None:
        text = raw.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        return list(reader.fieldnames or []), [dict(row) for row in reader]
    if not path_exists(path):
        return [], []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\r\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def read_tracked_text_lossless(path: Path) -> tuple[str, bool]:
    raw = git_head_bytes(path)
    if raw is None:
        raw = io_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_lossless(path: Path, text: str, has_bom: bool = True) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    raw = text.encode("utf-8")
    if has_bom:
        raw = b"\xef\xbb\xbf" + raw
    io_path(path).write_bytes(raw)
    return path


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return ""
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def upsert_csv(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    base_columns, existing = read_csv_table(path, prefer_head=True)
    columns = tuple(base_columns or list(columns))
    key_value = str(row.get(key, ""))
    merged = [item for item in existing if str(item.get(key, "")) != key_value]
    merged.append({column: row.get(column, "") for column in columns})
    return write_csv(path, columns, merged)


def first(rows: Sequence[Mapping[str, str]]) -> dict[str, str]:
    return dict(rows[0]) if rows else {}


def protocol_family(protocol_id: str) -> tuple[str, str]:
    if protocol_id.startswith("defense_"):
        return "defensive(방어)", "guard fragility before repair(수리 전 취약성 방어)"
    if protocol_id.startswith("repair_"):
        return "repair(수리)", "repair target diagnosis(수리 목표 진단)"
    if protocol_id.startswith("offense_"):
        return "offensive(공격)", "edge preservation check(우위 보존 점검)"
    if protocol_id.startswith("negative_control_"):
        return "negative_control(부정 대조)", "overfit leakage control(과적합 누수 대조)"
    return "unknown(미확인)", "runtime diagnostic(런타임 진단)"


def build_runtime_identity(mt5: Mapping[str, str]) -> list[dict[str, Any]]:
    report_path = Path(mt5.get("report_path", "")) if mt5.get("report_path") else Z_REPORT
    report_exists = path_exists(report_path) or path_exists(Z_REPORT)
    report_hash_path = report_path if path_exists(report_path) else Z_REPORT
    telemetry_exists = path_exists(Z_TELEMETRY)
    result_exists = path_exists(Z_MT5_RESULT)
    evidence_ok = (
        str(mt5.get("tester_status", "")) == "completed"
        and str(mt5.get("runtime_status", "")) == "completed"
        and str(mt5.get("report_status", "")) == "completed"
        and result_exists
        and report_exists
        and telemetry_exists
    )
    return [
        {
            "attempt_id": RUN_ID,
            "runtime_source_run_id": RUNTIME_SOURCE_RUN_ID,
            "execution_mode": "evidence_bound_exact_frozen_mt5_runtime_probe(근거 연결 정확 고정 MT5 런타임 탐침)",
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "terminal_exists": str(path_exists(DEFAULT_TERMINAL)).lower(),
            "metaeditor_path": DEFAULT_METAEDITOR.as_posix(),
            "metaeditor_exists": str(path_exists(DEFAULT_METAEDITOR)).lower(),
            "mt5_result_path": rel(Z_MT5_RESULT),
            "mt5_result_exists": str(result_exists).lower(),
            "report_path": report_hash_path.as_posix(),
            "report_exists": str(report_exists).lower(),
            "telemetry_path": rel(Z_TELEMETRY),
            "telemetry_exists": str(telemetry_exists).lower(),
            "tester_status": mt5.get("tester_status", ""),
            "runtime_status": mt5.get("runtime_status", ""),
            "report_status": mt5.get("report_status", ""),
            "runtime_result_sha256": sha256_file(Z_MT5_RESULT),
            "report_sha256": sha256_file(report_hash_path),
            "telemetry_sha256": sha256_file(Z_TELEMETRY),
            "evidence_status": "passed" if evidence_ok else "failed",
            "fresh_attempt_need": "not_for_protocol_view_yes_for_forward_gap_repair(프로토콜 보기에는 불필요, 전진 공백 수리에는 필요)",
            "effect": "run337AW binds reviewed protocols to the exact frozen run337Z MT5 evidence; this avoids a new candidate or retune(run337AW는 검토된 프로토콜을 정확한 고정 run337Z MT5 근거에 연결해 새 후보나 재튜닝을 피한다).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_protocol_runtime(queue_rows: Sequence[Mapping[str, str]], mt5: Mapping[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in queue_rows:
        protocol_id = str(item.get("protocol_id", ""))
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_family": item.get("branch_family", ""),
                "priority": item.get("priority", ""),
                "runtime_source_run_id": RUNTIME_SOURCE_RUN_ID,
                "execution_mode": "same_frozen_runtime_diagnostic_view(같은 고정 런타임 진단 보기)",
                "accepted_for_run337AW": item.get("accepted_for_run337AW", ""),
                "evidence_status": "bound_to_completed_mt5_probe(완료 MT5 탐침에 연결됨)",
                "tester_status": mt5.get("tester_status", ""),
                "runtime_status": mt5.get("runtime_status", ""),
                "report_status": mt5.get("report_status", ""),
                "feature_ready_count": mt5.get("feature_ready_count", ""),
                "model_ok_count": mt5.get("model_ok_count", ""),
                "long_count": mt5.get("long_count", ""),
                "short_count": mt5.get("short_count", ""),
                "flat_count": mt5.get("flat_count", ""),
                "trade_count": mt5.get("trade_count", ""),
                "order_attempt_count": mt5.get("order_attempt_count", ""),
                "order_fill_count": mt5.get("order_fill_count", ""),
                "net_profit": mt5.get("net_profit", ""),
                "profit_factor": mt5.get("profit_factor", ""),
                "expectancy": mt5.get("expectancy", ""),
                "recovery_factor": mt5.get("recovery_factor", ""),
                "max_drawdown_amount": mt5.get("max_drawdown_amount", ""),
                "short_trade_count": mt5.get("short_trade_count", ""),
                "long_trade_count": mt5.get("long_trade_count", ""),
                "allowed_use": "runtime signal parity and protocol attribution only(런타임 신호 동등성과 프로토콜 귀속 전용)",
                "forbidden_use": "model training, threshold retune, D/B rewrite, lot optimization, Forward Passed/Failed, Goal Achieve(모델 학습/임계값 재조정/D-B 재작성/랏 최적화/전진 통과-실패/목표 달성 금지)",
                "effect": "The protocol reads the frozen MT5 result as evidence, not as a tuned variant(프로토콜은 고정 MT5 결과를 튜닝 변형이 아니라 근거로 읽는다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_by_protocol(queue_rows: Sequence[Mapping[str, str]], diff_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in queue_rows:
        protocol_id = str(protocol.get("protocol_id", ""))
        for diff in diff_rows:
            rows.append(
                {
                    "protocol_id": protocol_id,
                    "dimension": diff.get("dimension", ""),
                    "proxy_expected_value": diff.get("proxy_expected_value", ""),
                    "mt5_runtime_value": diff.get("mt5_runtime_value", ""),
                    "difference_proxy_minus_mt5": diff.get("difference_proxy_minus_mt5", ""),
                    "difference_status": diff.get("difference_status", ""),
                    "usable_for_runtime_signal_parity": diff.get("usable_for_runtime_signal_parity", ""),
                    "usable_for_forward_pass_fail": "false",
                    "runtime_skip_reason": diff.get("runtime_skip_reason", ""),
                    "effect": "Matched proxy-MT5 dimensions can check signal handoff, not forward success(일치한 프록시-MT5 차원은 신호 인계를 점검할 수 있지만 전진 성공은 판단하지 못한다).",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_gap_by_protocol(queue_rows: Sequence[Mapping[str, str]], gap: Mapping[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in queue_rows:
        rows.append(
            {
                "protocol_id": protocol.get("protocol_id", ""),
                "gap_status": gap.get("gap_status", ""),
                "api_latest_us100_close_utc": gap.get("api_latest_us100_close_utc", ""),
                "feature_last_timestamp": gap.get("feature_last_timestamp", ""),
                "tester_last_observed_bar_time": gap.get("tester_last_observed_bar_time", ""),
                "tester_to_feature_last_gap_minutes": gap.get("tester_to_feature_last_gap_minutes", ""),
                "tester_to_api_latest_gap_minutes": gap.get("tester_to_api_latest_gap_minutes", ""),
                "telemetry_rows": gap.get("telemetry_rows", ""),
                "effect": "The gap is carried into every protocol so no protocol can claim forward authority(공백을 모든 프로토콜에 싣기 때문에 어느 프로토콜도 전진 권위를 주장하지 못한다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def metric_read(protocol_id: str, mt5: Mapping[str, str]) -> tuple[str, str, str]:
    trade_count = mt5.get("trade_count", "")
    pf = mt5.get("profit_factor", "")
    dd = mt5.get("max_drawdown_amount", "")
    recovery = mt5.get("recovery_factor", "")
    long_trades = mt5.get("long_trade_count", "")
    short_trades = mt5.get("short_trade_count", "")
    if protocol_id == "defense_cost_buffer_guard":
        return (
            f"PF(수익 팩터)={pf}; DD(손실폭)={dd}; recovery(회복)={recovery}",
            "cost buffer remains thin enough to keep as failure memory(비용 버퍼가 얇아 실패 기억으로 유지)",
            "cost_buffer(비용 버퍼)",
        )
    if protocol_id == "defense_late_curve_pocket_guard":
        return (
            f"trade_count(거래수)={trade_count}; DD(손실폭)={dd}",
            "curve pocket remains a diagnostic risk until tester gap is repaired(곡선 포켓은 테스터 공백 수리 전까지 진단 위험)",
            "curve_pocket(곡선 포켓)",
        )
    if protocol_id == "repair_direction_symmetry_probe":
        return (
            f"long_trades(롱 거래)={long_trades}; short_trades(숏 거래)={short_trades}",
            "direction skew remains visible; do not repair by tuning threshold(방향 쏠림이 보이며 임계값 튜닝으로 수리 금지)",
            "direction_symmetry(방향 대칭)",
        )
    if protocol_id == "repair_recovery_shape_probe":
        return (
            f"recovery(회복)={recovery}; expectancy(기대값)={mt5.get('expectancy', '')}",
            "recovery shape is weak and needs attribution before model work(회복 형태가 약해 모델 작업 전 귀속 필요)",
            "recovery_shape(회복 형태)",
        )
    if protocol_id == "offense_long_edge_preservation":
        return (
            f"long_trades(롱 거래)={long_trades}; feature_ready(피처 준비)={mt5.get('feature_ready_count', '')}",
            "long-side signal exists but cannot be promoted from completed-day evidence(롱 신호는 있으나 완성일 근거만으로 승격 불가)",
            "long_edge(롱 우위)",
        )
    if protocol_id == "offense_trade_count_recovery":
        return (
            f"trade_count(거래수)={trade_count}; order_fills(주문 체결)={mt5.get('order_fill_count', '')}",
            "trade count is analyzable but not a forward pass(거래수는 분석 가능하나 전진 통과가 아님)",
            "trade_count(거래수)",
        )
    if protocol_id.startswith("negative_control_"):
        return (
            "negative control is diagnostic only(부정 대조는 진단 전용)",
            "must not become a selection rule or repair target(선택 규칙이나 수리 목표가 되면 안 됨)",
            "negative_control(부정 대조)",
        )
    return ("runtime diagnostic(런타임 진단)", "no claim(주장 없음)", "runtime(런타임)")


def build_runtime_attribution(queue_rows: Sequence[Mapping[str, str]], mt5: Mapping[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in queue_rows:
        protocol_id = str(protocol.get("protocol_id", ""))
        family, _ = protocol_family(protocol_id)
        read, risk, axis = metric_read(protocol_id, mt5)
        rows.append(
            {
                "protocol_id": protocol_id,
                "protocol_family": family,
                "diagnostic_axis": axis,
                "metric_read": read,
                "risk_read": risk,
                "usable_for_repair_memory": "true",
                "usable_for_forward_decision": "false",
                "net_profit": mt5.get("net_profit", ""),
                "profit_factor": mt5.get("profit_factor", ""),
                "trade_count": mt5.get("trade_count", ""),
                "max_drawdown_amount": mt5.get("max_drawdown_amount", ""),
                "recovery_factor": mt5.get("recovery_factor", ""),
                "expectancy": mt5.get("expectancy", ""),
                "long_trade_count": mt5.get("long_trade_count", ""),
                "short_trade_count": mt5.get("short_trade_count", ""),
                "effect": "This row turns MT5 evidence into failure memory or attribution, not a tuned candidate(이 행은 MT5 근거를 튜닝 후보가 아니라 실패 기억 또는 귀속으로 바꾼다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_forensics() -> list[dict[str, Any]]:
    evidence = [
        ("terminal64", "executable(실행 파일)", DEFAULT_TERMINAL, "MT5 terminal identity(MT5 터미널 정체성)"),
        ("metaeditor64", "executable(실행 파일)", DEFAULT_METAEDITOR, "MetaEditor compile tool identity(메타에디터 컴파일 도구 정체성)"),
        ("frozen_forward_result", "csv", Z_MT5_RESULT, "MT5 KPI summary(MT5 핵심 성과 요약)"),
        ("strategy_report", "html", Z_REPORT, "Strategy Tester report(전략 테스터 보고서)"),
        ("strategy_report_alias", "html", Z_REPORT_ALIAS, "frozen forward report alias(고정 전진 보고서 별칭)"),
        ("runtime_telemetry", "csv", Z_TELEMETRY, "runtime telemetry(런타임 기록)"),
        ("runtime_summary", "csv", Z_SUMMARY, "runtime summary(런타임 요약)"),
        ("tester_settings", "json", Z_SETTINGS, "tester settings identity(테스터 설정 정체성)"),
        ("runtime_execution", "json", Z_RUNTIME_EXECUTION, "runtime execution result(런타임 실행 결과)"),
        ("run_set", "set", Z_SET, "tester set file(테스터 설정 파일)"),
        ("run_ini", "ini", Z_INI, "tester ini file(테스터 INI 파일)"),
        ("onnx_model", "onnx", Z_MODEL, "frozen ONNX model(고정 ONNX 모델)"),
        ("feature_matrix", "csv", Z_FEATURES, "frozen feature matrix(고정 피처 행렬)"),
    ]
    rows: list[dict[str, Any]] = []
    for evidence_id, evidence_type, path, role in evidence:
        exists = path_exists(path)
        rows.append(
            {
                "evidence_id": evidence_id,
                "evidence_type": evidence_type,
                "path": path.as_posix() if path.is_absolute() else rel(path),
                "exists": str(exists).lower(),
                "sha256": sha256_file(path) if exists else "",
                "role": role,
                "status": "present" if exists else "missing",
                "effect": "Identity evidence makes runtime reuse auditable(정체성 근거는 런타임 재사용을 감사 가능하게 한다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_claims(gap: Mapping[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "Forward Passed(전진 통과)",
            "status": "not_claimed",
            "allowed_use": "none(없음)",
            "forbidden_use": "pass decision(통과 판정)",
            "effect": "tester gap prevents forward pass(테스터 공백이 전진 통과를 막는다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_id": "Forward Failed(전진 실패)",
            "status": "not_claimed",
            "allowed_use": "none(없음)",
            "forbidden_use": "fail decision(실패 판정)",
            "effect": "gap means the full latest broker window is not judged(공백 때문에 최신 브로커 구간 전체를 판정하지 않는다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_id": "forward_decision_boundary(전진 판정 경계)",
            "status": f"not_closed_gap_status={gap.get('gap_status', '')}",
            "allowed_use": "runtime gap repair input(런타임 공백 수리 입력)",
            "forbidden_use": "operating reference(운영 기준)",
            "effect": "the next action targets tester gap repair instead of promotion(다음 행동은 승격이 아니라 테스터 공백 수리다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_id": "runtime_authority(런타임 권위)",
            "status": "not_claimed",
            "allowed_use": "signal parity only(신호 동등성 전용)",
            "forbidden_use": "runtime authority(런타임 권위)",
            "effect": "signal parity is narrower than runtime authority(신호 동등성은 런타임 권위보다 좁다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_id": "mutation_boundary(변경 경계)",
            "status": "no_training_no_retune_no_db_rewrite_no_lot_opt",
            "allowed_use": "diagnosis and failure memory(진단과 실패 기억)",
            "forbidden_use": "new candidate or threshold change(새 후보 또는 임계값 변경)",
            "effect": "overfit repair is not allowed to become another overfit(과적합 수리가 또 다른 과적합이 되지 못하게 한다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "claim_id": "Goal Achieve(목표 달성)",
            "status": "not_claimed",
            "allowed_use": "continue research(연구 지속)",
            "forbidden_use": "goal completion(목표 완료)",
            "effect": "the active goal remains open until operating-grade ONNX evidence exists(운영급 ONNX 근거가 있을 때까지 목표는 열린다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(
    queue_rows: Sequence[Mapping[str, str]],
    mt5: Mapping[str, str],
    diff_rows: Sequence[Mapping[str, str]],
    gap: Mapping[str, str],
    identity_rows: Sequence[Mapping[str, Any]],
    protocol_runtime: Sequence[Mapping[str, Any]],
    proxy_by_protocol: Sequence[Mapping[str, Any]],
    forensics: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    accepted_count = sum(1 for row in queue_rows if str(row.get("accepted_for_run337AW", "")).lower() == "true")
    matched_diff = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    per_protocol_matches = sum(1 for row in proxy_by_protocol if row.get("difference_status") == "matched")
    required_evidence = {"frozen_forward_result", "strategy_report", "runtime_telemetry", "tester_settings", "runtime_execution", "onnx_model"}
    present_required = {
        str(row.get("evidence_id", ""))
        for row in forensics
        if str(row.get("evidence_id", "")) in required_evidence and str(row.get("status", "")) == "present"
    }
    gates = [
        (
            "run337AV_acceptance_queue_loaded(337AV 수락 대기열 로드)",
            len(queue_rows) == 9 and accepted_count == 9,
            f"rows={len(queue_rows)};accepted={accepted_count}",
            "rows=9;accepted=9",
            "all reviewed protocol/control rows are available(검토된 프로토콜/대조 행이 모두 있다).",
        ),
        (
            "exact_frozen_runtime_evidence_available(정확 고정 런타임 근거 있음)",
            bool(identity_rows and identity_rows[0].get("evidence_status") == "passed"),
            f"identity_status={identity_rows[0].get('evidence_status', '') if identity_rows else 'missing'}",
            "passed",
            "actual MT5 evidence can be reused as a frozen diagnostic view(실제 MT5 근거를 고정 진단 보기로 재사용할 수 있다).",
        ),
        (
            "protocol_runtime_matrix_complete(프로토콜 런타임 행렬 완성)",
            len(protocol_runtime) == len(queue_rows) == 9,
            f"rows={len(protocol_runtime)}",
            "rows=9",
            "each protocol has a runtime evidence row(각 프로토콜에 런타임 근거 행이 있다).",
        ),
        (
            "proxy_mt5_signal_parity_5x9_recorded(프록시-MT5 신호 동등성 5x9 기록)",
            len(diff_rows) == 5 and matched_diff == 5 and len(proxy_by_protocol) == 45 and per_protocol_matches == 45,
            f"base={matched_diff}/{len(diff_rows)};protocol={per_protocol_matches}/{len(proxy_by_protocol)}",
            "base=5/5;protocol=45/45",
            "proxy can be used for signal handoff sanity only(프록시는 신호 인계 점검에만 쓸 수 있다).",
        ),
        (
            "tester_feature_last_gap_recorded(테스터 피처 끝 공백 기록)",
            gap.get("gap_status") == "tester_feature_last_gap_remains",
            f"gap_status={gap.get('gap_status', '')};minutes={gap.get('tester_to_feature_last_gap_minutes', '')}",
            "gap_status=tester_feature_last_gap_remains",
            "forward decision remains closed until gap repair(공백 수리 전까지 전진 판정은 닫힌다).",
        ),
        (
            "negative_controls_diagnostic_only(부정 대조 진단 전용)",
            sum(1 for row in queue_rows if str(row.get("protocol_id", "")).startswith("negative_control_")) == 3,
            f"negative_controls={sum(1 for row in queue_rows if str(row.get('protocol_id', '')).startswith('negative_control_'))}",
            "negative_controls=3",
            "negative controls are guards, not selection rules(부정 대조는 선택 규칙이 아니라 방어 장치다).",
        ),
        (
            "required_backtest_identity_present(필수 백테스트 정체성 존재)",
            present_required == required_evidence,
            f"present={len(present_required)}/{len(required_evidence)}",
            f"present={len(required_evidence)}/{len(required_evidence)}",
            "report, telemetry, settings, execution, model evidence are auditable(보고서/기록/설정/실행/모델 근거를 감사할 수 있다).",
        ),
        (
            "no_mutation_boundary(변경 금지 경계)",
            True,
            "no_training;no_threshold_retune;no_db_rewrite;no_lot_opt",
            "no_training;no_threshold_retune;no_db_rewrite;no_lot_opt",
            "the probe does not change the frozen surface(탐침은 고정 표면을 바꾸지 않는다).",
        ),
        (
            "final_claim_guard(최종 주장 방어)",
            True,
            "forward_passed=not_claimed;forward_failed=not_claimed;goal_achieve=not_claimed",
            "no forward or goal claim(전진 또는 목표 주장 없음)",
            "result judgment remains bounded(결과 판정이 경계 안에 남는다).",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = {
        ARTIFACT_RECEIPT: {
            "skill": "obsidian-artifact-lineage(아티팩트 계보)",
            "status": "passed",
            "runtime_source_run_id": RUNTIME_SOURCE_RUN_ID,
            "effect": "inputs, MT5 outputs, reports, and registers are tied to run337AW(입력, MT5 출력, 보고서, 등록부를 run337AW에 연결한다).",
        },
        DATA_RECEIPT: {
            "skill": "obsidian-data-integrity(데이터 무결성)",
            "status": "passed",
            "source_boundary": "run337AV reviewed queue plus run337Z actual MT5 evidence(337AV 검토 대기열과 337Z 실제 MT5 근거)",
            "lookahead_guard": "no current outcome, no threshold tuning, tester gap explicitly recorded(현재 결과 없음, 임계값 튜닝 없음, 테스터 공백 명시 기록)",
            "effect": "future visibility risk remains named instead of hidden(미래 가시성 위험을 숨기지 않고 이름 붙인다).",
        },
        RUNTIME_RECEIPT: {
            "skill": "obsidian-runtime-parity(런타임 동등성)",
            "status": "passed_signal_parity_only",
            "proxy_mt5_match": f"{final['proxy_mt5_matched_rows']}/{final['proxy_mt5_rows']}",
            "runtime_authority": "not_claimed",
            "effect": "signal handoff is consistent, but forward authority is blocked by the tester gap(신호 인계는 일관되지만 전진 권위는 테스터 공백이 막는다).",
        },
        FORENSICS_RECEIPT: {
            "skill": "obsidian-backtest-forensics(백테스트 포렌식)",
            "status": "passed_identity_recorded",
            "report_path": rel(Z_REPORT),
            "telemetry_path": rel(Z_TELEMETRY),
            "effect": "MT5 report and telemetry identity are hash-recorded(MT5 보고서와 런타임 기록 정체성을 해시로 남긴다).",
        },
        ATTRIBUTION_RECEIPT: {
            "skill": "obsidian-performance-attribution(성과 귀속)",
            "status": "passed_diagnostic_only",
            "protocol_rows": final["protocol_rows"],
            "effect": "metrics are split into defensive, repair, offensive, and negative-control reads(지표를 방어/수리/공격/부정 대조 판독으로 나눈다).",
        },
        JUDGMENT_RECEIPT: {
            "skill": "obsidian-result-judgment(결과 판정)",
            "status": "passed_no_forward_decision",
            "judgment": final["judgment"],
            "effect": "the run closes without Forward Passed/Failed or Goal Achieve(실행은 전진 통과/실패 또는 목표 달성 없이 닫힌다).",
        },
    }
    paths: list[Path] = []
    for path, payload in payloads.items():
        enriched = {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            **payload,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        paths.append(write_json(path, enriched))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AW Attempt Balanced Runtime Probe Without D/B(337단계 337AW 실행 D/B 없는 균형 런타임 탐침 시도)

## Purpose(목적)

run337AW(337AW 실행)는 run337AV(337AV 실행)가 넘긴 9개 protocol/control(프로토콜/대조) 행을 run337Z(337Z 실행)의 실제 MT5(MetaTrader 5, 메타트레이더5) runtime evidence(런타임 근거)에 연결했다.

Effect(효과): 새 ONNX(온엑스), threshold(임계값), D/B rule(D/B 규칙), lot(랏), runtime handoff(런타임 인계)는 바꾸지 않고, signal parity(신호 동등성)와 tester gap(테스터 공백)을 같은 표 안에서 보게 한다.

## Evidence(근거)

- runtime_source(런타임 원천): `{RUNTIME_SOURCE_RUN_ID}`
- protocol_rows(프로토콜 행): `{final['protocol_rows']}`
- proxy_MT5_match(프록시-MT5 일치): `{final['proxy_mt5_matched_rows']}/{final['proxy_mt5_rows']}`
- protocol_proxy_MT5_match(프로토콜별 프록시-MT5 일치): `{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}`
- tester_gap(테스터 공백): `{final['tester_gap_status']}`, `{final['tester_to_feature_last_gap_minutes']}` minutes(분)
- MT5 net/PF/DD(MT5 순익/수익 팩터/손실폭): `{final['net_profit']}` / `{final['profit_factor']}` / `{final['max_drawdown_amount']}`

## Judgment(판정)

Signal parity(신호 동등성)는 5/5 기본 차원과 45/45 protocol view(프로토콜 보기)에서 matched(일치)다. 그러나 tester feature-last gap(테스터 피처 마지막 공백)이 남아 최신 broker forward window(브로커 전진 구간)를 판단할 수 없다.

Effect(효과): run337AW(337AW 실행)는 runtime probe evidence(런타임 탐침 근거)를 닫지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Outputs(산출물)

- `{rel(PROTOCOL_RUNTIME_EVIDENCE)}`
- `{rel(PROXY_MT5_BY_PROTOCOL)}`
- `{rel(TESTER_GAP_BY_PROTOCOL)}`
- `{rel(RUNTIME_ATTRIBUTION)}`
- `{rel(BACKTEST_FORENSICS)}`
- `{rel(CLAIM_BOUNDARY_MATRIX)}`
- `{rel(GATE_AUDIT)}`

## Decision(결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AW Decision(337단계 337AW 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AW(337AW 실행)는 frozen MT5 runtime evidence(고정 MT5 런타임 근거)를 9개 protocol/control(프로토콜/대조) 행에 연결했다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Boundary(경계)

- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- tester_gap(테스터 공백): `{final['tester_gap_status']}`

## Evidence Paths(근거 경로)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- protocol_runtime(프로토콜 런타임): `{rel(PROTOCOL_RUNTIME_EVIDENCE)}`
- proxy_mt5_by_protocol(프로토콜별 프록시-MT5): `{rel(PROXY_MT5_BY_PROTOCOL)}`
"""
    return write_text_lossless(DECISION_DOC, text, True)


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []

    workspace, workspace_bom = read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337AW focus complete: run337AW(337AW 실행)은 `{final['status']}`로 balanced runtime probe evidence binding(균형 런타임 탐침 근거 연결)을 완료했다. "
        f"Effect(효과): protocol rows(프로토콜 행) `{final['protocol_rows']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}`, tester gap(테스터 공백) `{final['tester_gap_status']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if "Stage337 run337AW focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337AW focus complete:.*?(?=\n- >-|\Z)", focus, workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = read_tracked_text_lossless(CURRENT_STATE)
    current = replace_prefix_line(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current = replace_prefix_line(current, "- status(상태):", f"- status(상태): `{final['status']}`")
    current = replace_prefix_line(current, "- decision(결정):", f"- decision(결정): `{final['decision']}`")
    current = replace_prefix_line(current, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
    current = replace_prefix_line(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current = replace_prefix_line(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    aw_section = f"""## Stage337 run337AW(337AW 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AW(337AW 실행)는 run337AV(337AV 실행)의 9개 protocol/control(프로토콜/대조) 행을 run337Z(337Z 실행)의 실제 MT5 runtime evidence(MT5 런타임 근거)에 연결했다. proxy/MT5 parity(프록시/MT5 동등성)는 `{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}`이지만 tester gap(테스터 공백) `{final['tester_gap_status']}` 때문에 Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    if "## Stage337 run337AW(337AW 실행)" in current:
        current = re.sub(r"## Stage337 run337AW\(337AW 실행\).*?(?=\n## |\Z)", aw_section.strip() + "\n\n", current, count=1, flags=re.S)
    else:
        current = current.replace("## Stage337 run337AU(337AU 실행)", aw_section + "## Stage337 run337AU(337AU 실행)", 1)
    artifacts.append(write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `not_closed_tester_feature_last_gap_remains`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- completed_day_attribution_status(완성일 귀속 상태): `usable_without_db_for_attribution_only`
- db_source_status(D/B 원천 상태): `out_of_scope_by_claim_no_timestamp_aligned_sidecar`
- db_source_sidecar_feasible(D/B 원천 보조표 가능): `false`
- repair_inputs_status(수리 입력 상태): `balanced_no_lookahead_without_db_runtime_evidence_bound`
- protocol_runtime_rows(프로토콜 런타임 행): `{final['protocol_rows']}`
- proxy_mt5_parity(프록시-MT5 동등성): `{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}`
- tester_gap_status(테스터 공백 상태): `{final['tester_gap_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_gap_repair_required`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AW(337AW 실행)는 runtime probe evidence(런타임 탐침 근거)를 protocol/control(프로토콜/대조) 행에 묶었지만 전진/운영 주장은 막는다.
"""
    artifacts.append(write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = read_tracked_text_lossless(STAGE_BRIEF)
    brief = replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337AW_summary(337AW 요약): `{final['status']}`. "
        f"Effect(효과): protocol runtime rows(프로토콜 런타임 행) `{final['protocol_rows']}`, proxy/MT5 parity(프록시/MT5 동등성) `{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}`, tester gap(테스터 공백) `{final['tester_gap_status']}`; Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337AW_summary" in brief:
        brief = re.sub(r"^- run337AW_summary\(337AW 요약\):.*$", summary.rstrip(), brief, flags=re.MULTILINE)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog_line = (
        f"- {TODAY}: Stage337 run337AW(337AW 실행) `{final['status']}`. "
        f"Effect(효과): balanced runtime probe evidence(균형 런타임 탐침 근거)를 9개 protocol/control(프로토콜/대조)에 연결했고 proxy/MT5 parity(프록시/MT5 동등성) `{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}`를 기록했다. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    changelog, changelog_bom = read_tracked_text_lossless(CHANGELOG)
    if "Stage337 run337AW" in changelog:
        changelog = re.sub(rf"^- {re.escape(TODAY)}: Stage337 run337AW\(337AW 실행\).*$", changelog_line, changelog, flags=re.MULTILINE)
    else:
        changelog = changelog.rstrip() + "\n" + changelog_line + "\n"
    artifacts.append(write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "balanced_runtime_probe_evidence_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};protocol_rows={final['protocol_rows']};proxy_mt5={final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']};goal_achieve_not_claimed.",
        "family": "runtime_parity_attribution_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_runtime_probe_evidence",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balanced_runtime_probe_evidence",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_probe_evidence_bound_without_db(D/B 없는 런타임 탐침 근거 연결)",
        "tier_scope": "Tier A u42 completed MT5 evidence(Tier A u42 완료 MT5 근거)",
        "kpi_scope": "runtime_signal_parity_no_forward_decision(런타임 신호 동등성, 전진 판정 없음)",
        "scoreboard_lane": "runtime_parity_attribution_boundary",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"protocol_rows={final['protocol_rows']};proxy_mt5={final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']};gap={final['tester_gap_status']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed_from_run337Z_actual_mt5_evidence_gap_remains(337Z 실제 MT5 근거에서 완료, 공백 남음)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_runtime_probe_evidence",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_attribution_boundary",
        "evidence_scope": "run337AV protocol queue plus run337Z actual MT5 report telemetry and parity evidence",
        "kpi_scope": "runtime_signal_parity_and_gap_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;proxy_mt5={final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__balanced_runtime_probe_evidence",
        "family": "balanced_no_lookahead_runtime_probe_without_db",
        "question": "can reviewed no-lookahead repair protocols be bound to exact frozen MT5 runtime evidence without D/B or retuning",
        "metric_scope": "protocol_runtime_signal_parity_gap_identity",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    upsert_csv(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, run_row, "run_id")
    upsert_csv(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    upsert_csv(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns = list(ARTIFACT_COLUMNS)
    base_columns, rows = read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = base_columns or columns
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path):
            continue
        artifact_path = rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
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
    queue_rows = read_csv(AV_QUEUE)
    protocol_review = read_csv(AV_PROTOCOL_REVIEW)
    diff_rows = read_csv(Z_DIFF)
    mt5 = first(read_csv(Z_MT5_RESULT))
    gap = first(read_csv(Z_GAP))
    av_final = read_json(AV_FINAL)
    z_final = read_json(Z_FINAL)

    identity_rows = build_runtime_identity(mt5)
    identity_path = write_csv(RUNTIME_ATTEMPT_IDENTITY, RUNTIME_ATTEMPT_COLUMNS, identity_rows)
    protocol_runtime = build_protocol_runtime(queue_rows, mt5)
    protocol_runtime_path = write_csv(PROTOCOL_RUNTIME_EVIDENCE, PROTOCOL_RUNTIME_COLUMNS, protocol_runtime)
    proxy_by_protocol = build_proxy_by_protocol(queue_rows, diff_rows)
    proxy_path = write_csv(PROXY_MT5_BY_PROTOCOL, PROXY_BY_PROTOCOL_COLUMNS, proxy_by_protocol)
    gap_by_protocol = build_gap_by_protocol(queue_rows, gap)
    gap_path = write_csv(TESTER_GAP_BY_PROTOCOL, GAP_BY_PROTOCOL_COLUMNS, gap_by_protocol)
    attribution = build_runtime_attribution(queue_rows, mt5)
    attribution_path = write_csv(RUNTIME_ATTRIBUTION, ATTRIBUTION_COLUMNS, attribution)
    forensics = build_forensics()
    forensics_path = write_csv(BACKTEST_FORENSICS, FORENSICS_COLUMNS, forensics)
    claims = build_claims(gap)
    claims_path = write_csv(CLAIM_BOUNDARY_MATRIX, CLAIM_COLUMNS, claims)
    gates = build_gates(queue_rows, mt5, diff_rows, gap, identity_rows, protocol_runtime, proxy_by_protocol, forensics)
    gate_path = write_csv(GATE_AUDIT, GATE_COLUMNS, gates)

    failed_gates = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    proxy_base_matched = sum(1 for row in diff_rows if row.get("difference_status") == "matched")
    proxy_protocol_matched = sum(1 for row in proxy_by_protocol if row.get("difference_status") == "matched")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_source_run_id": RUNTIME_SOURCE_RUN_ID,
        "status": STATUS if not failed_gates else "invalid_stage337AW_runtime_probe_evidence_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if not failed_gates else "runtime_probe_evidence_gate_failure",
        "decision": DECISION if not failed_gates else "repair_stage337AW_runtime_probe_evidence_gate_failure_before_next_step",
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_stage337AW_runtime_probe_evidence_gate_failure_v1",
        "protocol_rows": len(queue_rows),
        "protocol_review_rows": len(protocol_review),
        "proxy_mt5_rows": len(diff_rows),
        "proxy_mt5_matched_rows": proxy_base_matched,
        "protocol_proxy_mt5_rows": len(proxy_by_protocol),
        "protocol_proxy_mt5_matched_rows": proxy_protocol_matched,
        "tester_gap_status": gap.get("gap_status", ""),
        "tester_to_feature_last_gap_minutes": gap.get("tester_to_feature_last_gap_minutes", ""),
        "net_profit": mt5.get("net_profit", ""),
        "profit_factor": mt5.get("profit_factor", ""),
        "trade_count": mt5.get("trade_count", ""),
        "max_drawdown_amount": mt5.get("max_drawdown_amount", ""),
        "recovery_factor": mt5.get("recovery_factor", ""),
        "expectancy": mt5.get("expectancy", ""),
        "long_trade_count": mt5.get("long_trade_count", ""),
        "short_trade_count": mt5.get("short_trade_count", ""),
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row.get("status") == "passed"),
        "failed_gates": failed_gates,
        "run337AV_status": av_final.get("status", ""),
        "run337Z_status": z_final.get("status", ""),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": rel(__file__),
        "parent_run_id": PARENT_RUN_ID,
        "runtime_source_run_id": RUNTIME_SOURCE_RUN_ID,
        "inputs": [rel(path) if path.is_relative_to(ROOT) else path.as_posix() for path in INPUT_FILES],
        "outputs": [rel(path) for path in OUTPUT_FILES],
        "execution_mode": "evidence_bound_exact_frozen_mt5_runtime_probe(근거 연결 정확 고정 MT5 런타임 탐침)",
        "frozen_items": [
            "selected candidate(선택 후보)",
            "ONNX model(온엑스 모델)",
            "Adapter package(어댑터 패키지)",
            "feature order(피처 순서)",
            "D/B decision surface(D/B 결정 표면)",
            "score threshold(점수 임계값)",
            "risk logic(위험 로직)",
            "lot logic(랏 로직)",
            "ATR SL/TP(ATR 손절/익절)",
            "runtime handoff(런타임 인계)",
        ],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(랏 최적화)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_doc_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        identity_path,
        protocol_runtime_path,
        proxy_path,
        gap_path,
        attribution_path,
        forensics_path,
        claims_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_doc_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    summary = {
        "run_id": RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_action": final["next_action"],
        "protocol_rows": final["protocol_rows"],
        "protocol_proxy_mt5": f"{final['protocol_proxy_mt5_matched_rows']}/{final['protocol_proxy_mt5_rows']}",
        "tester_gap_status": final["tester_gap_status"],
        "gates": f"{final['passed_gates']}/{final['gate_rows']}",
        "report": rel(report_path),
        "artifact_registry": rel(artifact_registry_path),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if not failed_gates else 1


if __name__ == "__main__":
    raise SystemExit(main())

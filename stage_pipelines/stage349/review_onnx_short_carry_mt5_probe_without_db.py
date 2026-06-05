from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-06-01"
STAGE_ID = "349_onnx_short_carry_runtime__execute_mt5_probe"
SOURCE_STAGE_ID = "348_cash_open_proxy_review__long_oos_gap_short_carry_triage"
RUN_NUMBER = "run349C"
RUN_ID = "run349C_review_onnx_short_carry_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1"
NEXT_RUN_ID = "run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1"

STATUS = "reviewed_stage349C_onnx_short_carry_mt5_probe_negative_runtime_parity_repair_required_no_selection"
JUDGMENT = "negative_runtime_probe_trade_density_partial_but_loss_and_mt5_onnx_probability_mismatch_repair_required"
DECISION = "stage349C_open_run349D_test_onnx_no_conversion_runtime_parity_diagnostic"
CLAIM_BOUNDARY = (
    "research_development_onnx_short_carry_mt5_probe_review_negative_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run349C_onnx_short_carry_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage349C_onnx_short_carry_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

RUN349B_DIR = STAGE_DIR / "02_runs" / "run349B"
RUN349B_FINAL_DECISION = RUN349B_DIR / "final_decision.json"
RUN349B_GATE_AUDIT = RUN349B_DIR / "required_gate_coverage_audit.csv"
RUN349B_SUMMARY = RUN349B_DIR / "onnx_short_carry_mt5_probe_summary.csv"
RUN349B_DIFF = RUN349B_DIR / "proxy_mt5_runtime_difference.csv"
RUN349B_REPORTS = RUN349B_DIR / "strategy_tester_report_records.json"
RUN349B_IDENTITY = RUN349B_DIR / "runtime_identity.csv"
RUN349B_MANIFEST = RUN349B_DIR / "run_manifest.json"

SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run348C"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected" / "expected_tape.csv"
SOURCE_FEATURE_MATRIX = SOURCE_RUN_DIR / "features" / "runtime_features.csv"
SOURCE_MODEL_DIR = SOURCE_RUN_DIR / "models"
SOURCE_MODEL_MANIFEST = SOURCE_RUN_DIR / "model_handoff_manifest.csv"
SOURCE_FEATURE_ORDER = SOURCE_RUN_DIR / "feature_order_contract.csv"
SOURCE_RUNTIME_PARITY = SOURCE_RUN_DIR / "runtime_parity_contract.csv"

ONNX_DIAGNOSTIC = RUN_DIR / "python_onnx_vs_expected_vs_mt5_diagnostic.csv"
ATTEMPT_REVIEW_MATRIX = RUN_DIR / "attempt_review_matrix.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_ACTION_QUEUE = RUN_DIR / "next_action_queue.csv"
RUNTIME_REPAIR_RECEIPT = RUN_DIR / "runtime_parity_repair_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

INPUT_FILES = (
    RUN349B_FINAL_DECISION,
    RUN349B_GATE_AUDIT,
    RUN349B_SUMMARY,
    RUN349B_DIFF,
    RUN349B_REPORTS,
    RUN349B_IDENTITY,
    RUN349B_MANIFEST,
    SOURCE_EXPECTED_TAPE,
    SOURCE_FEATURE_MATRIX,
    SOURCE_MODEL_MANIFEST,
    SOURCE_FEATURE_ORDER,
    SOURCE_RUNTIME_PARITY,
)

OUTPUT_FILES = (
    ONNX_DIAGNOSTIC,
    ATTEMPT_REVIEW_MATRIX,
    FAILURE_MEMORY,
    NEXT_ACTION_QUEUE,
    RUNTIME_REPAIR_RECEIPT,
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
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not exists(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value) if exists(value) else value.as_posix()
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        return json_ready(value.item())
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(10_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def csv_ready(value: Any) -> Any:
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}" if math.isfinite(value) else ""
    return value


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with open(fs_path(tmp_path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: csv_ready(row.get(key, "")) for key in fieldnames})
    for attempt in range(5):
        try:
            os.replace(fs_path(tmp_path), fs_path(path))
            break
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.5 * (attempt + 1))


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def read_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), encoding="utf-8-sig", low_memory=False).fillna("")


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return default
    return output if math.isfinite(output) else default


def to_int(value: Any, default: int = 0) -> int:
    return int(round(to_float(value, float(default))))


def gate_passed(path: Path) -> bool:
    _fields, rows = read_csv_rows(required(path))
    return bool(rows) and all(str(row.get("status", "")).lower() == "passed" for row in rows)


def feature_columns(frame: pd.DataFrame) -> list[str]:
    metadata = {"bar_time_server", "timestamp_utc", "split", "row_index"}
    return [column for column in frame.columns if column not in metadata]


def ready_mt5_telemetry(attempt_name: str) -> pd.DataFrame:
    path = RUN349B_DIR / "runtime_telemetry" / f"{attempt_name}_telemetry.csv"
    frame = pd.read_csv(fs_path(required(path)), low_memory=False).fillna("")
    cycles = frame[frame["record_type"].astype(str).str.lower().eq("cycle")].copy()
    return cycles[
        cycles["feature_ready"].astype(str).str.lower().eq("true")
        & cycles["model_ok"].astype(str).str.lower().eq("true")
    ].copy()


def run_python_onnx_diagnostic(summary: pd.DataFrame) -> list[dict[str, Any]]:
    try:
        import onnxruntime as ort
    except Exception as exc:  # pragma: no cover - local environment evidence
        rows = [
            {
                "attempt_name": str(row["attempt_name"]),
                "status": "blocked_onnxruntime_unavailable(onnxruntime 없음)",
                "error": str(exc),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for _, row in summary.iterrows()
        ]
        write_csv(ONNX_DIAGNOSTIC, rows)
        return rows

    features = read_frame(required(SOURCE_FEATURE_MATRIX))
    expected = read_frame(required(SOURCE_EXPECTED_TAPE))
    cols = feature_columns(features)
    matrix = features.loc[:, cols].to_numpy(dtype=np.float32)
    rows: list[dict[str, Any]] = []
    for _, summary_row in summary.iterrows():
        attempt = str(summary_row["attempt_name"])
        model_path = SOURCE_MODEL_DIR / f"{attempt}.onnx"
        sess = ort.InferenceSession(str(required(model_path)), providers=["CPUExecutionProvider"])
        input_meta = sess.get_inputs()[0]
        outputs = sess.run(None, {input_meta.name: matrix})
        output_names = [output.name for output in sess.get_outputs()]
        probability = None
        chosen_output = ""
        for name, value in zip(output_names, outputs):
            array = np.asarray(value)
            if array.ndim == 2 and array.shape[1] == 3:
                probability = array.astype(float)
                chosen_output = name
                break
        if probability is None:
            rows.append(
                {
                    "attempt_name": attempt,
                    "status": "blocked_no_probability_output(확률 출력 없음)",
                    "output_names": ";".join(output_names),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        exp = expected[expected["attempt_name"].astype(str).eq(attempt)].copy()
        mt5 = ready_mt5_telemetry(attempt)
        exp_probs = exp.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype=float)
        mt5_probs = mt5.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype=float)
        n = min(len(probability), len(exp_probs), len(mt5_probs))
        py_vs_expected = np.max(np.abs(probability[:n] - exp_probs[:n]), axis=1)
        py_vs_mt5 = np.max(np.abs(probability[:n] - mt5_probs[:n]), axis=1)
        mt5_vs_expected = np.max(np.abs(mt5_probs[:n] - exp_probs[:n]), axis=1)
        tolerance = 1e-4
        rows.append(
            {
                "attempt_name": attempt,
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_input_name": input_meta.name,
                "onnx_input_shape": list(input_meta.shape),
                "chosen_output": chosen_output,
                "output_names": ";".join(output_names),
                "feature_count": len(cols),
                "rows_compared": n,
                "python_onnx_expected_max_abs_diff": float(np.max(py_vs_expected)) if n else "",
                "python_onnx_mt5_max_abs_diff": float(np.max(py_vs_mt5)) if n else "",
                "mt5_expected_max_abs_diff": float(np.max(mt5_vs_expected)) if n else "",
                "python_onnx_expected_match_rows": int((py_vs_expected <= tolerance).sum()) if n else 0,
                "python_onnx_mt5_match_rows": int((py_vs_mt5 <= tolerance).sum()) if n else 0,
                "mt5_expected_match_rows": int((mt5_vs_expected <= tolerance).sum()) if n else 0,
                "first_python_onnx": probability[0].tolist() if n else [],
                "first_expected": exp_probs[0].tolist() if n else [],
                "first_mt5": mt5_probs[0].tolist() if n else [],
                "diagnostic_judgment": (
                    "python_expected_match_mt5_mismatch_runtime_parity_fault(파이썬과 예상은 일치, MT5 런타임 불일치)"
                    if n and float(np.max(py_vs_expected)) <= tolerance and float(np.max(py_vs_mt5)) > tolerance
                    else "needs_manual_review(수동 검토 필요)"
                ),
                "effect": "expected tape(예상 테이프) 문제가 아니라 MT5 ONNX runtime(런타임) 문제인지 분리한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ONNX_DIAGNOSTIC, rows)
    return rows


def build_attempt_review(summary: pd.DataFrame, diagnostics: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    diag_by_attempt = {str(row.get("attempt_name")): row for row in diagnostics}
    rows: list[dict[str, Any]] = []
    for _, row in summary.iterrows():
        attempt = str(row["attempt_name"])
        trade_count = to_int(row.get("trade_count"))
        net_profit = to_float(row.get("net_profit"))
        profit_factor = to_float(row.get("profit_factor"))
        density_status = str(row.get("trade_density_requirement_status", ""))
        diag = diag_by_attempt.get(attempt, {})
        parity_fault = "runtime_parity_fault" in str(diag.get("diagnostic_judgment", ""))
        if trade_count <= 0:
            result = "negative_zero_trade_density_fail(부정, 거래 없음)"
            salvage = "threshold/decision surface too restrictive or MT5 output rounded to flat(임계값/결정 표면 과도 제한 또는 MT5 출력 관망화)"
        elif net_profit < 0 or profit_factor < 1.0:
            result = "negative_trade_density_ok_but_loss(부정, 거래 밀도는 되나 손실)"
            salvage = "short-carry direction has trade-count seed value but needs parity repair and loss-control rule(숏 기여 방향은 거래수 씨앗 가치가 있으나 동등성 수리와 손실 제어 필요)"
        else:
            result = "inconclusive_positive_kpi_not_expected_here(불충분, 긍정 KPI 별도 검토 필요)"
            salvage = "review manually(수동 검토)"
        rows.append(
            {
                "attempt_name": attempt,
                "model_id": row.get("model_id", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "expectancy": row.get("expectancy", ""),
                "drawdown": row.get("max_drawdown_amount", ""),
                "recovery_factor": row.get("recovery_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "long_trade_count": row.get("long_trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "trade_density_per_feature_day": row.get("trade_density_per_feature_day", ""),
                "trade_density_requirement_status": density_status,
                "matched_rows": row.get("matched_rows", ""),
                "probability_mismatch_rows": row.get("probability_mismatch_rows", ""),
                "decision_mismatch_rows": row.get("decision_mismatch_rows", ""),
                "python_expected_match_rows": diag.get("python_onnx_expected_match_rows", ""),
                "python_mt5_match_rows": diag.get("python_onnx_mt5_match_rows", ""),
                "runtime_parity_fault": "true" if parity_fault else "false",
                "result_judgment": result,
                "salvage_value": salvage,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_REVIEW_MATRIX, rows)
    return rows


def write_failure_and_next(review_rows: Sequence[Mapping[str, Any]]) -> None:
    rows = [
        {
            "memory_id": f"{RUN_ID}__onnx_runtime_probability_mismatch",
            "hypothesis": "Stage348 ONNX short-carry package can execute in MT5 with matching Python ONNX probabilities(348단계 온엑스 숏 기여 패키지가 파이썬 온엑스 확률과 같은 의미로 MT5 실행 가능)",
            "variants_tried": "logistic_balanced cashopen/balanced_margin; ExtraTrees cashopen/balanced_margin(로지스틱/엑스트라트리 4개)",
            "failed_boundary": "MT5 runtime parity and operating profitability(MT5 런타임 동등성과 운영 수익성)",
            "why_failed": "Python ONNX matches expected tape, but MT5 ONNX probabilities diverge; trade-producing attempts lose money(파이썬 온엑스는 예상 테이프와 맞지만 MT5 확률이 어긋나고 거래 발생 후보는 손실)",
            "salvage_value": "ExtraTrees produced 451~496 trades and 4.25~4.68 feature-day density, so trade-shape seed survives after parity repair(엑스트라트리가 거래수와 거래 밀도 씨앗을 남김)",
            "reopen_condition": "Run no-conversion or tensor-shape MT5 diagnostic reaches Python ONNX parity, then rebuild trade-shape/loss-control surface(no-conversion 또는 tensor-shape 진단이 파이썬 온엑스 동등성에 도달한 뒤 거래 형태/손실 제어 표면 재구축)",
            "do_not_repeat_note": "Do not promote or retune from MT5 KPIs while ONNX probability parity is broken(온엑스 확률 동등성이 깨진 상태에서 MT5 KPI로 승격/미세조정 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(FAILURE_MEMORY, rows)
    queue = [
        {
            "next_run_id": NEXT_RUN_ID,
            "action": "test InpModelNoConversion=true and tensor output handling(MT5 no conversion 및 텐서 출력 처리 진단)",
            "effect": "separate MT5 ONNX conversion issue from model alpha quality(MT5 온엑스 변환 문제와 모델 알파 품질을 분리)",
            "input_attempt": "c03_xtrees_cashopen_q95q90",
            "success_condition": "python_onnx_mt5_max_abs_diff <= 1e-4 on diagnostic rows(진단 행에서 파이썬 온엑스-MT5 차이 1e-4 이하)",
            "failure_condition": "MT5 probability mismatch remains after no-conversion/tensor-shape check(no-conversion/텐서 형태 확인 뒤에도 MT5 확률 불일치 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "next_run_id": "stage350_seed_runtime_parity_repaired_trade_shape_offensive_exploration",
            "action": "after parity repair, explore trade-shape loss-control seeds(동등성 수리 후 거래 형태 손실 제어 씨앗 탐색)",
            "effect": "keep offensive exploration moving without using invalid runtime probabilities(무효 런타임 확률을 쓰지 않고 공격 탐색 유지)",
            "input_attempt": "c03/c04 ExtraTrees trade-density clue(엑스트라트리 거래 밀도 단서)",
            "success_condition": "MT5 net profit/PF/expectancy/recovery improve while trade density >=3/day(MT5 순수익/PF/기대값/회복 계수 개선, 거래 밀도 3/day 이상)",
            "failure_condition": "loss persists after parity repair and cost stress(동등성 수리 및 비용 압박 뒤 손실 지속)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_ACTION_QUEUE, queue)


def gate_row(gate_id: str, passed: bool, evidence: str, effect: str, observed: str = "") -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "observed": observed,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any], diagnostics: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    py_expected_ok = all(to_float(row.get("python_onnx_expected_max_abs_diff"), 1.0) <= 1e-4 for row in diagnostics)
    mt5_fault = any(to_float(row.get("python_onnx_mt5_max_abs_diff"), 0.0) > 1e-4 for row in diagnostics)
    no_forbidden = all(
        final.get(key) == "not_claimed"
        for key in ["forward_passed", "forward_failed", "live_readiness", "runtime_authority", "operating_promotion", "goal_achieve"]
    ) and final.get("candidate_selection") == "not_run"
    return [
        gate_row("parent_run349B_gates_passed", gate_passed(RUN349B_GATE_AUDIT), rel(RUN349B_GATE_AUDIT), "run349B runtime probe(런타임 탐침) gate(게이트)를 확인한다."),
        gate_row("python_onnx_expected_parity_confirmed", py_expected_ok, rel(ONNX_DIAGNOSTIC), "Python ONNX(파이썬 온엑스)가 expected tape(예상 테이프)와 맞는지 확인한다."),
        gate_row("mt5_runtime_mismatch_attributed", mt5_fault, rel(ONNX_DIAGNOSTIC), "MT5 확률 불일치를 runtime parity fault(런타임 동등성 결함)로 귀속한다."),
        gate_row("negative_kpi_judgment_recorded", exists(ATTEMPT_REVIEW_MATRIX), rel(ATTEMPT_REVIEW_MATRIX), "손실, 거래수, 거래 밀도, 동등성 결함을 후보별 판정으로 기록한다."),
        gate_row("failure_memory_recorded", exists(FAILURE_MEMORY), rel(FAILURE_MEMORY), "반복 금지와 재개 조건을 failure memory(실패 기억)로 남긴다."),
        gate_row("next_action_queue_written", exists(NEXT_ACTION_QUEUE), rel(NEXT_ACTION_QUEUE), "다음 수리/공격 탐색 조건을 queue(대기열)로 남긴다."),
        gate_row("tier_pair_rows_written", exists(STAGE_LEDGER), rel(STAGE_LEDGER), "Tier A/B/A+B(티어 A/B/A+B) 기록을 유지한다."),
        gate_row("final_claim_guard", no_forbidden, rel(CLAIM_RECEIPT), "review(검토)를 운영 주장으로 올리지 않는다."),
        gate_row("required_gate_coverage_audit", True, rel(GATE_AUDIT), "필수 gate coverage(게이트 커버리지)를 종료 기록에 연결한다."),
    ]


def best_trade_row(summary: pd.DataFrame) -> dict[str, Any]:
    frame = summary.copy()
    for column in ["trade_count", "net_profit", "profit_factor", "recovery_factor", "trade_density_per_feature_day"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    trade_rows = frame[frame["trade_count"] > 0].copy()
    source = trade_rows if not trade_rows.empty else frame
    source = source.sort_values(["net_profit", "profit_factor", "recovery_factor", "trade_density_per_feature_day"], ascending=[False, False, False, False])
    return source.iloc[0].to_dict()


def build_final(summary: pd.DataFrame, diagnostics: Sequence[Mapping[str, Any]], review_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    parent = read_json(required(RUN349B_FINAL_DECISION))
    best = best_trade_row(summary)
    py_expected_max = max(to_float(row.get("python_onnx_expected_max_abs_diff"), 0.0) for row in diagnostics)
    py_mt5_max = max(to_float(row.get("python_onnx_mt5_max_abs_diff"), 0.0) for row in diagnostics)
    negative_rows = sum(1 for row in review_rows if str(row.get("result_judgment", "")).startswith("negative"))
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": int(len(summary)),
        "negative_attempt_rows": negative_rows,
        "runtime_completed_rows": parent.get("runtime_completed_rows", ""),
        "report_completed_rows": parent.get("report_completed_rows", ""),
        "matched_rows": parent.get("matched_rows", ""),
        "expected_rows": parent.get("expected_rows", ""),
        "diff_mismatch_rows": parent.get("diff_mismatch_rows", ""),
        "best_trade_attempt": best.get("attempt_name", ""),
        "best_trade_net_profit": to_float(best.get("net_profit")),
        "best_trade_profit_factor": to_float(best.get("profit_factor")),
        "best_trade_expectancy": to_float(best.get("expectancy")),
        "best_trade_recovery_factor": to_float(best.get("recovery_factor")),
        "best_trade_drawdown": to_float(best.get("max_drawdown_amount")),
        "best_trade_count": to_int(best.get("trade_count")),
        "best_trade_density_per_feature_day": to_float(best.get("trade_density_per_feature_day")),
        "best_trade_density_requirement_status": best.get("trade_density_requirement_status", ""),
        "python_onnx_expected_max_abs_diff": py_expected_max,
        "python_onnx_mt5_max_abs_diff": py_mt5_max,
        "runtime_parity_judgment": "mt5_onnx_probability_mismatch_repair_required(MT5 온엑스 확률 불일치 수리 필요)",
        "result_judgment": "negative(부정)",
        "external_verification_status": "completed(완료)",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": now_utc(),
    }


def artifact_paths() -> list[Path]:
    return [path for path in OUTPUT_FILES if exists(path)]


def write_receipts(final: Mapping[str, Any]) -> None:
    created_at = now_utc()
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_REPAIR_RECEIPT,
        {
            **base,
            "research_path": rel(SOURCE_EXPECTED_TAPE),
            "runtime_path": rel(RUN349B_DIFF),
            "shared_contract": rel(SOURCE_RUNTIME_PARITY),
            "known_differences": "feature_count 53 vs 58 contract(53개 피처와 58개 계약 차이); MT5 ONNX probability mismatch(MT5 온엑스 확률 불일치)",
            "parity_check": rel(ONNX_DIAGNOSTIC),
            "parity_identity": rel(RUN349B_IDENTITY),
            "runtime_claim_boundary": "runtime_probe_review(런타임 탐침 검토)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "summary": rel(RUN349B_SUMMARY),
            "attempt_review_matrix": rel(ATTEMPT_REVIEW_MATRIX),
            "best_trade_attempt": final["best_trade_attempt"],
            "best_trade_net_profit": final["best_trade_net_profit"],
            "best_trade_count": final["best_trade_count"],
            "best_trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
            "performance_judgment": "negative(부정)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_judgment": "negative(부정)",
            "external_verification_status": final["external_verification_status"],
            "candidate_selection": "not_run",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "reviewed negative runtime probe and repair condition(부정 런타임 탐침 검토 및 수리 조건)",
            "forbidden_claims": ["candidate_selection(후보 선정)", "runtime_authority(런타임 권위)", "operating_promotion(운영 승격)", "Goal_Achieve(목표 달성)"],
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "live_readiness": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths()],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_negative_review_boundary(부정 검토 경계로 연결됨)",
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run349C ONNX Short-Carry MT5 Probe Review(349C 온엑스 숏 기여 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- result_judgment(결과 판정): `{final['result_judgment']}`
- best_trade_attempt(거래 발생 최고 시도): `{final['best_trade_attempt']}`
- best_trade_net_profit(거래 발생 최고 순수익): `{final['best_trade_net_profit']}`
- best_trade_profit_factor(거래 발생 최고 수익 팩터): `{final['best_trade_profit_factor']}`
- best_trade_expectancy(거래 발생 최고 기대값): `{final['best_trade_expectancy']}`
- best_trade_recovery_factor(거래 발생 최고 회복 계수): `{final['best_trade_recovery_factor']}`
- best_trade_count(거래 수): `{final['best_trade_count']}`
- best_trade_density(거래 밀도): `{final['best_trade_density_per_feature_day']}`
- python_onnx_expected_max_abs_diff(파이썬 온엑스-예상 최대 차이): `{final['python_onnx_expected_max_abs_diff']}`
- python_onnx_mt5_max_abs_diff(파이썬 온엑스-MT5 최대 차이): `{final['python_onnx_mt5_max_abs_diff']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run349B(349B 실행)의 MT5 KPI(MT5 핵심 성과 지표), proxy-MT5 diff(프록시-MT5 차이), Python ONNX diagnostic(파이썬 온엑스 진단)을 함께 검토했다.

## Effect(효과)

Python ONNX(파이썬 온엑스)는 expected tape(예상 테이프)와 맞지만 MT5 ONNX probabilities(MT5 온엑스 확률)가 어긋난다는 것을 분리했다. 따라서 수익 음수 결과는 운영 실패로 닫되, 다음에는 `InpModelNoConversion=true`와 tensor output handling(텐서 출력 처리)을 좁게 검증한다.

## Boundary(경계)

Negative result(부정 결과)이며 reusable evidence(재사용 근거)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage349C Review Decision(349C 검토 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(ONNX_DIAGNOSTIC)}`, `{rel(ATTEMPT_REVIEW_MATRIX)}`, `{rel(FAILURE_MEMORY)}`

Action(행동): run349B(349B 실행)를 negative runtime probe(부정 런타임 탐침)로 검토했다.
Effect(효과): 다음 작업은 MT5 ONNX conversion/tensor handling(MT5 온엑스 변환/텐서 처리)을 수리 조건으로 좁힌다.

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

run349C(349C 실행)는 run349B(349B 실행)를 negative(부정)로 검토하고, 다음 수리 조건을 `InpModelNoConversion=true`와 tensor output handling(텐서 출력 처리) 진단으로 좁혔다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage349 Selection Status(349단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- reviewed_parent(검토된 상위 실행): `{PARENT_RUN_ID}`
- best_trade_attempt(거래 발생 최고 시도): `{final['best_trade_attempt']}`
- best_trade_net_profit(거래 발생 최고 순수익): `{final['best_trade_net_profit']}`
- best_trade_count(거래 수): `{final['best_trade_count']}`
- best_trade_density_per_feature_day(피처일 거래 밀도): `{final['best_trade_density_per_feature_day']}`
- runtime_parity_judgment(런타임 동등성 판정): `{final['runtime_parity_judgment']}`
- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 거래 밀도 단서는 보존하지만 손실과 런타임 동등성 결함 때문에 선정하지 않는다.
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
    stage_brief = f"""# Stage 349 Brief(349단계 개요)

## Stage ID(단계 ID)

`{STAGE_ID}`

## Question(질문)

Can the ONNX short-carry probe package(온엑스 숏 기여 탐침 패키지) from Stage348(348단계) be executed and reviewed as an MT5 runtime probe(MT5 런타임 탐침) without making Stage348(348단계) heavier?

## Current Truth(현재 진실)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_package_run(원천 패키지 실행): `{SOURCE_PACKAGE_RUN_ID}`
- branch_run(분기 실행): `run349A_branch_stage348_to_onnx_short_carry_runtime_probe_without_db_v1`
- runtime_probe_run(런타임 탐침 실행): `{PARENT_RUN_ID}`
- review_run(검토 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

## run349B Runtime Evidence(run349B 런타임 근거)

- attempts(시도): `{final['attempt_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}/{final['expected_rows']}`
- diff_mismatch_rows(차이 행): `{final['diff_mismatch_rows']}`
- best_trade_attempt(거래 발생 최고 시도): `{final['best_trade_attempt']}`
- best_trade_net_profit(순수익): `{final['best_trade_net_profit']}`
- best_trade_count(거래 수): `{final['best_trade_count']}`
- best_trade_density(거래 밀도): `{final['best_trade_density_per_feature_day']}`

## Review Judgment(검토 판정)

Action(행동): Python ONNX(파이썬 온엑스), expected tape(예상 테이프), MT5 telemetry(MT5 기록)를 함께 비교했다.
Effect(효과): Python ONNX(파이썬 온엑스)는 expected tape(예상 테이프)와 맞고, MT5 ONNX runtime(런타임)에서 확률이 어긋나는 것을 확인했다.

## Runtime Review Constraint(런타임 검토 제약)

- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`
- result(결과): ExtraTrees(엑스트라트리)는 거래 밀도 3/day 이상을 만들었지만 손실과 런타임 확률 불일치 때문에 운영 후보가 아니다.
- next_condition(다음 조건): `{NEXT_RUN_ID}`에서 `InpModelNoConversion=true`와 tensor output handling(텐서 출력 처리)을 검증한다.

## Evidence Boundary(근거 경계)

This stage(이 단계)는 runtime probe and review(런타임 탐침과 검토)만 수행한다. No candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)이다.
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    write_bom_text(STAGE_BRIEF, stage_brief)
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run349C ONNX Short-Carry MT5 Probe Review(349C 온엑스 숏 기여 MT5 탐침 검토)

- run_id(실행 ID): `{RUN_ID}`
- review(검토): `{rel(REPORT_PATH)}`
- diagnostic(진단): `{rel(ONNX_DIAGNOSTIC)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): 런타임 동등성 결함을 수리 조건으로 좁힌다.
""",
    )
    block = f"""## {TODAY} {RUN_ID}

Action(행동): run349B(349B 실행)를 MT5 KPI(MT5 핵심 성과 지표), Python ONNX diagnostic(파이썬 온엑스 진단), proxy-MT5 diff(프록시-MT5 차이)로 검토했다.
Effect(효과): 거래 밀도 단서는 보존하지만, 손실과 MT5 ONNX probability mismatch(MT5 온엑스 확률 불일치) 때문에 운영 후보로 닫지 않는다.

- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, block)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, block)


def write_final_and_manifest(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    payload = {
        **dict(final),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "work_family": "kpi_evidence(KPI/근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": ["obsidian-runtime-parity(런타임 동등성)", "obsidian-backtest-forensics(백테스트 포렌식)", "obsidian-artifact-lineage(산출물 계보)"],
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in artifact_paths()],
            "external_verification_status": payload["external_verification_status"],
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "lane": "runtime_probe_review(런타임 탐침 검토)",
        "family": "kpi_evidence(KPI/근거)",
        "run_number": RUN_NUMBER,
        "notes": "Reviewed run349B as negative runtime probe; opened no-conversion diagnostic(349B를 부정 런타임 탐침으로 검토하고 no-conversion 진단을 열었음).",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "candidate_model_id": "none(없음)",
        "external_verification_status": final["external_verification_status"],
        "result_status": "negative(부정)",
    }
    run_row = {
        **base,
        "net_profit": final["best_trade_net_profit"],
        "profit_factor": final["best_trade_profit_factor"],
        "expectancy": final["best_trade_expectancy"],
        "drawdown": final["best_trade_drawdown"],
        "recovery_factor": final["best_trade_recovery_factor"],
        "trade_count": final["best_trade_count"],
        "matched_rows": final["matched_rows"],
        "trade_density_per_feature_day": final["best_trade_density_per_feature_day"],
        "trade_density_requirement_status": final["best_trade_density_requirement_status"],
        "attempt_count": final["attempt_rows"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_rows = [
        {
            **run_row,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_runtime_probe_review",
            "kpi_scope": "mt5_runtime_probe_review",
            "primary_kpi": f"net_profit={final['best_trade_net_profit']};pf={final['best_trade_profit_factor']};trades={final['best_trade_count']}",
            "guardrail_kpi": f"py_expected_diff={final['python_onnx_expected_max_abs_diff']};py_mt5_diff={final['python_onnx_mt5_max_abs_diff']}",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **run_row,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows)


def update_artifact_registry() -> None:
    rows = []
    for path in artifact_paths():
        relative = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{relative.replace('/', '__').replace('.', '_')}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": relative,
                "artifact_path": relative,
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    missing = [rel(path) for path in [FINAL_DECISION, RUN_MANIFEST, GATE_AUDIT, REPORT_PATH, DECISION_DOC, ONNX_DIAGNOSTIC, ATTEMPT_REVIEW_MATRIX, FAILURE_MEMORY, NEXT_ACTION_QUEUE] if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    failed = [row for row in gates if row.get("status") != "passed"]
    if failed:
        raise RuntimeError("run349C gates failed(349C 게이트 실패): " + ", ".join(str(row.get("gate_id")) for row in failed))
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path in INPUT_FILES:
        required(path)
    summary = read_frame(required(RUN349B_SUMMARY))
    diagnostics = run_python_onnx_diagnostic(summary)
    review_rows = build_attempt_review(summary, diagnostics)
    write_failure_and_next(review_rows)
    final_seed = build_final(summary, diagnostics, review_rows)
    write_receipts(final_seed)
    gates = make_gates(final_seed, diagnostics)
    write_csv(GATE_AUDIT, gates)
    final = write_final_and_manifest(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    write_receipts(final)
    final = write_final_and_manifest(final, gates)
    update_artifact_registry()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "result_judgment": final["result_judgment"],
                "best_trade_attempt": final["best_trade_attempt"],
                "best_trade_net_profit": final["best_trade_net_profit"],
                "best_trade_count": final["best_trade_count"],
                "python_onnx_expected_max_abs_diff": final["python_onnx_expected_max_abs_diff"],
                "python_onnx_mt5_max_abs_diff": final["python_onnx_mt5_max_abs_diff"],
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

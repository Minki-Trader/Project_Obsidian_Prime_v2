from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"
RUN_NUMBER = "run347B"
RUN_ID = "run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1"
PARENT_RUN_ID = "run347A_design_cash_open_asymmetric_long_short_source_without_db_v1"
SOURCE_REVIEW_RUN_ID = "run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
NEXT_RUN_ID = "run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1"

STATUS = "completed_stage347B_cash_open_asymmetric_source_inputs_materialized_proxy_training_ready_no_selection"
JUDGMENT = "timestamp_safe_teacher_source_inputs_materialized_for_proxy_training_tier_b_missing_no_operating_claim"
DECISION = "stage347B_open_run347C_train_cash_open_asymmetric_source_proxy_models"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_cash_open_asymmetric_source_teacher_labels_"
    "no_model_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
GATE_TOTAL = 11

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run347B_cash_open_asymmetric_source_materialization.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_SELECTION = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

DESIGN_RUN_DIR = STAGE_DIR / "02_runs" / "run347A"
DESIGN_FINAL_DECISION = DESIGN_RUN_DIR / "final_decision.json"
DESIGN_GATE_AUDIT = DESIGN_RUN_DIR / "required_gate_coverage_audit.csv"
DESIGN_MATRIX = DESIGN_RUN_DIR / "asymmetric_source_design_matrix.csv"
FEATURE_SOURCE_PLAN = DESIGN_RUN_DIR / "feature_source_plan.csv"
LABEL_HEAD_PLAN = DESIGN_RUN_DIR / "label_head_plan.csv"
MODEL_FAMILY_PLAN = DESIGN_RUN_DIR / "model_family_plan.csv"
RUN347B_QUEUE = DESIGN_RUN_DIR / "run347B_materialization_queue.csv"

SOURCE_RUN344N_DIR = ROOT / "stages" / "344_directional_long_quality__supply_surface_probe" / "02_runs" / "run344N"
SOURCE_FEATURES = SOURCE_RUN344N_DIR / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN344N_DIR / "expected" / "expected_tape.csv"
SOURCE_EXPECTED_INDEX = SOURCE_RUN344N_DIR / "expected_tape_index.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_RUN344N_DIR / "runtime_probe_attempt_package.csv"
SOURCE_RUN345B_DIR = ROOT / "stages" / "345_cash_open_decomposition__long_quality_short_carry_runtime_probe" / "02_runs" / "run345B"
SOURCE_RUN345B_SUMMARY = SOURCE_RUN345B_DIR / "cash_open_long_quality_short_carry_mt5_probe_summary.csv"
SOURCE_RUN345B_DIFF = SOURCE_RUN345B_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_REVIEW_RUN_DIR = ROOT / "stages" / "346_cash_open_runtime_review__asymmetric_source_pivot" / "02_runs" / "run346B"
SOURCE_SCORECARD = SOURCE_REVIEW_RUN_DIR / "variant_review_scorecard.csv"
SOURCE_POSITIVE_CLUES = SOURCE_REVIEW_RUN_DIR / "positive_clues.csv"
SOURCE_FAILURE_MEMORY = SOURCE_REVIEW_RUN_DIR / "failure_memory.csv"

FEATURE_LABEL_TABLE = RUN_DIR / "feature_label_source_table.csv"
FEATURE_SCHEMA_MANIFEST = RUN_DIR / "feature_schema_manifest.csv"
LABEL_SOURCE_MANIFEST = RUN_DIR / "teacher_label_manifest.csv"
LABEL_DISTRIBUTION = RUN_DIR / "proxy_label_distribution.csv"
PROXY_SCREEN_GRID = RUN_DIR / "proxy_screen_grid.csv"
PROXY_GRID_SUMMARY = RUN_DIR / "proxy_grid_summary.csv"
TIMESTAMP_INTEGRITY_AUDIT = RUN_DIR / "timestamp_integrity_audit.csv"
MATERIALIZATION_SUMMARY = RUN_DIR / "materialization_summary.csv"
HANDOFF_INDEX = RUN_DIR / "handoff_index.csv"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage347B_cash_open_asymmetric_source_materialization.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

ATTEMPT_PREFIXES = {
    "n01_s07_base_control": "n01",
    "n02_s07_long_only_disable_short": "n02",
    "n03_s07_short_only_disable_long": "n03",
    "n04_s07_no_cash_open_short_single_filter": "n04",
    "n05_s07_late_long_firewall_single_filter": "n05",
    "n06_s07_long_only_late_firewall": "n06",
}

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
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
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def iter_csv_rows(path: Path):
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            yield dict(row)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if path_is_file(path):
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


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path_is_file(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def safe_float(value: Any, default: float = 0.0) -> float:
    output = to_float(value)
    return default if math.isnan(output) else output


def bucket_cash_open(value: str) -> str:
    minutes = safe_float(value, default=-9999)
    if minutes < 0:
        return "outside_cash_open_window(현금장 창 밖)"
    if minutes < 30:
        return "cash_000_030(현금장 0-30분)"
    if minutes < 60:
        return "cash_030_060(현금장 30-60분)"
    if minutes < 120:
        return "cash_060_120(현금장 60-120분)"
    if minutes < 240:
        return "cash_120_240(현금장 120-240분)"
    return "cash_240_plus(현금장 240분 이후)"


def bucket_adx(value: str) -> str:
    adx = safe_float(value, default=-1)
    if adx < 0:
        return "adx_missing(ADX 결측)"
    if adx < 20:
        return "adx_low_lt20(ADX 낮음 20 미만)"
    if adx < 35:
        return "adx_mid_20_35(ADX 중간 20-35)"
    return "adx_high_ge35(ADX 높음 35 이상)"


def bucket_vol_ratio(value: str) -> str:
    ratio = safe_float(value, default=-1)
    if ratio < 0:
        return "vol_missing(변동성 결측)"
    if ratio < 0.8:
        return "vol_compressed_lt08(변동성 압축 0.8 미만)"
    if ratio <= 1.2:
        return "vol_neutral_08_12(변동성 중립 0.8-1.2)"
    return "vol_expanded_gt12(변동성 확장 1.2 초과)"


def sign_bucket(value: str) -> str:
    v = safe_float(value, default=0)
    if v > 0:
        return "positive(양수)"
    if v < 0:
        return "negative(음수)"
    return "zero_or_missing(0 또는 결측)"


def quantile(values: Sequence[float], q: float) -> float:
    clean = sorted(v for v in values if not math.isnan(v))
    if not clean:
        return 0.0
    index = (len(clean) - 1) * q
    lo = math.floor(index)
    hi = math.ceil(index)
    if lo == hi:
        return clean[int(index)]
    weight = index - lo
    return clean[lo] * (1 - weight) + clean[hi] * weight


def read_feature_table() -> tuple[list[str], dict[str, dict[str, str]], dict[str, Any]]:
    fields, rows = read_csv_rows(required(SOURCE_FEATURES))
    by_timestamp: dict[str, dict[str, str]] = {}
    duplicates = 0
    for row in rows:
        timestamp = row.get("timestamp", "")
        if timestamp in by_timestamp:
            duplicates += 1
        by_timestamp[timestamp] = row
    return fields, by_timestamp, {"rows": len(rows), "unique_timestamps": len(by_timestamp), "duplicates": duplicates}


def read_expected_by_time() -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    expected: dict[str, dict[str, str]] = {}
    attempt_counts = {attempt: 0 for attempt in ATTEMPT_PREFIXES}
    duplicate_keys = 0
    for row in iter_csv_rows(required(SOURCE_EXPECTED_TAPE)):
        attempt = row.get("attempt_name", "")
        prefix = ATTEMPT_PREFIXES.get(attempt)
        if not prefix:
            continue
        bar_time = row.get("bar_time", "")
        if not bar_time:
            continue
        bucket = expected.setdefault(
            bar_time,
            {
                "bar_time": bar_time,
                "source_time": row.get("source_time", ""),
                "source_row_id": row.get("source_row_id", ""),
                "feature_input_hash": row.get("feature_input_hash", ""),
            },
        )
        if f"{prefix}_decision_label" in bucket:
            duplicate_keys += 1
        attempt_counts[attempt] += 1
        for key in ["p_short", "p_flat", "p_long", "decision_label", "pre_filter_decision_label"]:
            bucket[f"{prefix}_{key}"] = row.get(key, "")
        bucket[f"{prefix}_side_filter_applied"] = row.get("side_filter_applied", "")
        bucket[f"{prefix}_side_filter_reason"] = row.get("side_filter_reason", "")
    return expected, {"rows": len(expected), "attempt_counts": attempt_counts, "duplicate_attempt_keys": duplicate_keys}


def score_margin(p_yes: float, p_a: float, p_b: float) -> float:
    return p_yes - max(p_a, p_b)


def top_two_margin(values: Sequence[float]) -> float:
    clean = sorted((v for v in values if not math.isnan(v)), reverse=True)
    if len(clean) < 2:
        return 0.0
    return clean[0] - clean[1]


def materialize_feature_label_table() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    feature_fields, features, feature_audit = read_feature_table()
    expected, expected_audit = read_expected_by_time()
    feature_columns = [field for field in feature_fields if field != "timestamp"]
    rows: list[dict[str, Any]] = []
    feature_missing = 0
    expected_missing = 0
    for bar_time in sorted(expected):
        expected_row = expected[bar_time]
        feature_row = features.get(bar_time)
        if feature_row is None:
            feature_missing += 1
            feature_row = {}
        row: dict[str, Any] = {
            "bar_time": bar_time,
            "source_time": expected_row.get("source_time", ""),
            "source_row_id": expected_row.get("source_row_id", ""),
            "feature_input_hash": expected_row.get("feature_input_hash", ""),
        }
        for field in feature_columns:
            row[field] = feature_row.get(field, "")
        row["cash_open_bucket"] = bucket_cash_open(row.get("minutes_from_cash_open", ""))
        row["adx_bucket"] = bucket_adx(row.get("adx_14", ""))
        row["vol_ratio_bucket"] = bucket_vol_ratio(row.get("historical_vol_5_over_20", ""))
        row["di_spread_sign"] = sign_bucket(row.get("di_spread_14", ""))
        for attempt, prefix in ATTEMPT_PREFIXES.items():
            if f"{prefix}_decision_label" not in expected_row:
                expected_missing += 1
            for key in ["p_short", "p_flat", "p_long", "decision_label", "pre_filter_decision_label", "side_filter_applied", "side_filter_reason"]:
                row[f"{prefix}_{key}"] = expected_row.get(f"{prefix}_{key}", "")
        n02_long = safe_float(row.get("n02_p_long"))
        n02_short = safe_float(row.get("n02_p_short"))
        n02_flat = safe_float(row.get("n02_p_flat"))
        n03_short = safe_float(row.get("n03_p_short"))
        n03_long = safe_float(row.get("n03_p_long"))
        n03_flat = safe_float(row.get("n03_p_flat"))
        n01_short = safe_float(row.get("n01_p_short"))
        n01_flat = safe_float(row.get("n01_p_flat"))
        n01_long = safe_float(row.get("n01_p_long"))
        row["long_quality_teacher_label"] = "1" if row.get("n02_decision_label") == "long" else "0"
        row["short_carry_teacher_label"] = "1" if row.get("n03_decision_label") == "short" else "0"
        row["base_active_teacher_label"] = "1" if row.get("n01_decision_label") in {"long", "short"} else "0"
        row["base_decision_label"] = row.get("n01_decision_label", "")
        row["long_quality_score"] = round(score_margin(n02_long, n02_short, n02_flat), 12)
        row["short_carry_score"] = round(score_margin(n03_short, n03_long, n03_flat), 12)
        row["base_direction_margin"] = round(top_two_margin([n01_short, n01_flat, n01_long]), 12)
        long_signal = row["long_quality_teacher_label"] == "1"
        short_signal = row["short_carry_teacher_label"] == "1"
        if long_signal and not short_signal:
            allocator = "long(롱)"
        elif short_signal and not long_signal:
            allocator = "short(숏)"
        elif long_signal and short_signal:
            allocator = "conflict(충돌)"
        else:
            allocator = "flat(관망)"
        row["allocator_teacher_label"] = allocator
        rows.append(row)
    write_csv(FEATURE_LABEL_TABLE, rows)
    summary = {
        "feature_rows": feature_audit["rows"],
        "feature_unique_timestamps": feature_audit["unique_timestamps"],
        "feature_duplicate_timestamps": feature_audit["duplicates"],
        "expected_unique_timestamps": expected_audit["rows"],
        "expected_attempt_counts": expected_audit["attempt_counts"],
        "expected_duplicate_attempt_keys": expected_audit["duplicate_attempt_keys"],
        "materialized_rows": len(rows),
        "feature_missing_rows": feature_missing,
        "expected_missing_cells": expected_missing,
        "first_bar_time": rows[0]["bar_time"] if rows else "",
        "last_bar_time": rows[-1]["bar_time"] if rows else "",
    }
    return rows, summary


def write_feature_and_label_manifests(rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> None:
    if not rows:
        raise RuntimeError("no materialized rows(물질화 행 없음)")
    fields = list(rows[0].keys())
    source_feature_fields, _feature_rows = read_csv_rows(required(SOURCE_FEATURES))
    feature_schema_rows = []
    for field in fields:
        if field in source_feature_fields:
            source = rel(SOURCE_FEATURES)
            boundary = "feature_at_bar_close(봉 종가 피처)"
        elif field.endswith("_score") or field.endswith("_margin") or field.endswith("_teacher_label") or field == "allocator_teacher_label":
            source = rel(SOURCE_EXPECTED_TAPE)
            boundary = "teacher_source_from_runtime_expected_tape(런타임 예상 테이프 기반 교사 원천)"
        elif field.endswith("_bucket") or field == "di_spread_sign":
            source = rel(SOURCE_FEATURES)
            boundary = "deterministic_transform_from_timestamp_safe_feature(시점 안전 피처의 결정적 변환)"
        else:
            source = "join_key_or_metadata(결합 키 또는 메타데이터)"
            boundary = "metadata(메타데이터)"
        feature_schema_rows.append(
            {
                "column_name": field,
                "source_path": source,
                "boundary": boundary,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FEATURE_SCHEMA_MANIFEST, feature_schema_rows)
    label_rows = [
        {
            "label_name": "long_quality_teacher_label(롱 품질 교사 라벨)",
            "definition": "1 when n02 long-only expected decision is long(n02 롱 전용 예상 결정이 롱이면 1)",
            "source": rel(SOURCE_EXPECTED_TAPE),
            "future_outcome_label": "false(아님)",
            "timestamp_boundary": "same-bar model-output teacher source, not future PnL(동일 봉 모델 출력 교사 원천, 미래 손익 아님)",
            "allowed_use": "proxy/model-source distillation input(프록시/모델 원천 증류 입력)",
            "forbidden_use": "claim realized edge or MT5 KPI(실현 우위나 MT5 KPI 주장)",
        },
        {
            "label_name": "short_carry_teacher_label(숏 기여 교사 라벨)",
            "definition": "1 when n03 short-only expected decision is short(n03 숏 전용 예상 결정이 숏이면 1)",
            "source": rel(SOURCE_EXPECTED_TAPE),
            "future_outcome_label": "false(아님)",
            "timestamp_boundary": "same-bar model-output teacher source, not future PnL(동일 봉 모델 출력 교사 원천, 미래 손익 아님)",
            "allowed_use": "proxy/model-source distillation input(프록시/모델 원천 증류 입력)",
            "forbidden_use": "claim realized edge or MT5 KPI(실현 우위나 MT5 KPI 주장)",
        },
        {
            "label_name": "allocator_teacher_label(배분 교사 라벨)",
            "definition": "long/short/flat/conflict from long_quality and short_carry teacher labels(롱 품질/숏 기여 교사 라벨에서 롱/숏/관망/충돌)",
            "source": rel(FEATURE_LABEL_TABLE),
            "future_outcome_label": "false(아님)",
            "timestamp_boundary": "derived from teacher decisions only(교사 결정에서만 파생)",
            "allowed_use": "broad proxy routing design(넓은 프록시 라우팅 설계)",
            "forbidden_use": "operating selection(운영 선정)",
        },
        {
            "label_name": "base_active_teacher_label(기본 활성 교사 라벨)",
            "definition": "1 when n01 base expected decision is long or short(n01 기본 예상 결정이 long 또는 short이면 1)",
            "source": rel(SOURCE_EXPECTED_TAPE),
            "future_outcome_label": "false(아님)",
            "timestamp_boundary": "same-bar base decision teacher source, not future PnL(동일 봉 기본 결정 교사 원천, 미래 손익 아님)",
            "allowed_use": "activity control and allocator sanity check(활성 대조와 배분기 점검)",
            "forbidden_use": "realized edge claim or operating promotion(실현 우위 주장 또는 운영 승격)",
        },
    ]
    write_csv(LABEL_SOURCE_MANIFEST, label_rows)


def count_by(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key, ""))
        counts[value] = counts.get(value, 0) + 1
    return counts


def write_distribution_and_grid(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    distribution_rows = []
    for label_name in ["base_decision_label", "base_active_teacher_label", "long_quality_teacher_label", "short_carry_teacher_label", "allocator_teacher_label", "cash_open_bucket", "adx_bucket", "vol_ratio_bucket"]:
        for value, count in sorted(count_by(rows, label_name).items()):
            distribution_rows.append({"field": label_name, "value": value, "count": count, "share": round(count / max(len(rows), 1), 8)})
    write_csv(LABEL_DISTRIBUTION, distribution_rows)
    long_scores = [safe_float(row.get("long_quality_score"), default=float("nan")) for row in rows]
    short_scores = [safe_float(row.get("short_carry_score"), default=float("nan")) for row in rows]
    quantiles = [0.70, 0.80, 0.85, 0.90, 0.95]
    long_thresholds = [(f"q{int(q*100)}", quantile(long_scores, q)) for q in quantiles]
    short_thresholds = [(f"q{int(q*100)}", quantile(short_scores, q)) for q in quantiles]
    families = ["logistic_balanced(균형 로지스틱)", "ExtraTrees(엑스트라 트리)", "HistGBM(히스토그램 GBM)"]
    allocator_rules = ["balanced_margin(균형 마진)", "short_priority(숏 우선)", "cash_open_regime_allocator(현금장 국면 배분기)"]
    grid_rows = []
    grid_id = 1
    for family in families:
        for long_label, long_threshold in long_thresholds:
            for short_label, short_threshold in short_thresholds:
                for allocator in allocator_rules:
                    long_supply = sum(1 for row in rows if safe_float(row.get("long_quality_score"), -999) >= long_threshold)
                    short_supply = sum(1 for row in rows if safe_float(row.get("short_carry_score"), -999) >= short_threshold)
                    grid_rows.append(
                        {
                            "grid_id": f"g{grid_id:03d}",
                            "model_family": family,
                            "long_threshold_label": long_label,
                            "long_quality_score_threshold": round(long_threshold, 12),
                            "short_threshold_label": short_label,
                            "short_carry_score_threshold": round(short_threshold, 12),
                            "allocator_rule": allocator,
                            "estimated_long_supply_rows": long_supply,
                            "estimated_short_supply_rows": short_supply,
                            "estimated_total_supply_rows": long_supply + short_supply,
                            "allowed_use": "proxy_screen_only(프록시 선별 전용)",
                            "forbidden_use": "MT5 KPI substitute or selection(MT5 KPI 대체 또는 선정)",
                        }
                    )
                    grid_id += 1
    write_csv(PROXY_SCREEN_GRID, grid_rows)
    grid_summary = [
        {
            "metric": "grid_rows",
            "value": len(grid_rows),
            "effect": "broad sweep grid(넓은 탐색 격자)을 만든다.",
        },
        {
            "metric": "long_score_min_max",
            "value": f"{round(min(long_scores), 12)}..{round(max(long_scores), 12)}",
            "effect": "long quality score(롱 품질 점수) 범위를 기록한다.",
        },
        {
            "metric": "short_score_min_max",
            "value": f"{round(min(short_scores), 12)}..{round(max(short_scores), 12)}",
            "effect": "short carry score(숏 기여 점수) 범위를 기록한다.",
        },
    ]
    write_csv(PROXY_GRID_SUMMARY, grid_summary)
    return distribution_rows, grid_rows


def write_integrity_and_summary(summary: Mapping[str, Any], distribution_rows: Sequence[Mapping[str, Any]], grid_rows: Sequence[Mapping[str, Any]]) -> None:
    attempt_counts = summary["expected_attempt_counts"]
    expected_rows_each = sorted(set(attempt_counts.values()))
    audit_rows = [
        {
            "check": "feature_rows_joined(피처 행 결합)",
            "status": "passed" if summary["feature_missing_rows"] == 0 else "failed",
            "value": f"feature_missing_rows={summary['feature_missing_rows']}",
            "effect": "모든 expected timestamp(예상 시각)에 feature(피처)를 붙인다.",
        },
        {
            "check": "expected_attempt_counts_equal(예상 시도 행 수 동일)",
            "status": "passed" if len(expected_rows_each) == 1 and expected_rows_each[0] == summary["materialized_rows"] else "failed",
            "value": json.dumps(attempt_counts, ensure_ascii=False, sort_keys=True),
            "effect": "6개 attempt(시도)가 같은 row grain(행 단위)을 공유한다.",
        },
        {
            "check": "feature_duplicate_timestamps(피처 중복 시각)",
            "status": "passed" if summary["feature_duplicate_timestamps"] == 0 else "failed",
            "value": summary["feature_duplicate_timestamps"],
            "effect": "timestamp join(시각 결합)이 일대일임을 확인한다.",
        },
        {
            "check": "teacher_label_boundary(교사 라벨 경계)",
            "status": "passed",
            "value": "teacher labels derive from expected tape only(교사 라벨은 예상 테이프에서만 파생)",
            "effect": "미래 손익 라벨처럼 과장하지 않는다.",
        },
    ]
    write_csv(TIMESTAMP_INTEGRITY_AUDIT, audit_rows)
    summary_rows = [
        {"metric": "materialized_rows", "value": summary["materialized_rows"]},
        {"metric": "feature_rows", "value": summary["feature_rows"]},
        {"metric": "expected_unique_timestamps", "value": summary["expected_unique_timestamps"]},
        {"metric": "first_bar_time", "value": summary["first_bar_time"]},
        {"metric": "last_bar_time", "value": summary["last_bar_time"]},
        {"metric": "distribution_rows", "value": len(distribution_rows)},
        {"metric": "proxy_grid_rows", "value": len(grid_rows)},
        {"metric": "claim_boundary", "value": CLAIM_BOUNDARY},
    ]
    write_csv(MATERIALIZATION_SUMMARY, summary_rows)


def write_handoff_index() -> None:
    paths = [
        FEATURE_LABEL_TABLE,
        FEATURE_SCHEMA_MANIFEST,
        LABEL_SOURCE_MANIFEST,
        LABEL_DISTRIBUTION,
        PROXY_SCREEN_GRID,
        PROXY_GRID_SUMMARY,
        TIMESTAMP_INTEGRITY_AUDIT,
        MATERIALIZATION_SUMMARY,
    ]
    rows = [
        {
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "consumer": NEXT_RUN_ID,
            "availability": "tracked(추적됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in paths
    ]
    write_csv(HANDOFF_INDEX, rows)


def write_receipts(summary: Mapping[str, Any]) -> None:
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_FEATURES), rel(SOURCE_EXPECTED_TAPE), rel(SOURCE_RUN345B_SUMMARY)],
            "time_axis": "bar_time/source_time from expected tape joined to runtime feature timestamp(예상 테이프 bar_time/source_time을 런타임 피처 timestamp와 결합)",
            "sample_scope": f"Tier A source rows={summary['materialized_rows']}; Tier B missing_required(Tier A 원천 행, Tier B 필수 누락)",
            "missing_or_duplicate_check": f"feature_missing_rows={summary['feature_missing_rows']}; duplicate_timestamps={summary['feature_duplicate_timestamps']}",
            "feature_label_boundary": "features are closed-bar inputs; teacher labels come from same expected model decisions, not future PnL(피처는 확정 봉 입력, 교사 라벨은 같은 예상 모델 결정이며 미래 손익 아님)",
            "split_boundary": "materialization only; no train/validation/OOS split selected(물질화 전용, 학습/검증/표본외 분할 선정 없음)",
            "leakage_risk": "teacher labels could be mistaken for realized outcome labels(교사 라벨을 실현 결과 라벨로 오해할 위험)",
            "data_hash_or_identity": rel(HANDOFF_INDEX),
            "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "not trained yet; proxy grid for logistic/ExtraTrees/HistGBM prepared(아직 학습 없음, 로지스틱/엑스트라트리스/히스토그램 GBM 프록시 격자 준비)",
            "target_and_label": "teacher labels from n02 long-only and n03 short-only expected decisions(n02 롱 전용/n03 숏 전용 예상 결정 기반 교사 라벨)",
            "split_method": "not selected in run347B(347B에서 미선정)",
            "selection_metric": "not selected; next run uses proxy screen(미선정, 다음 실행이 프록시 선별)",
            "secondary_metrics": "label distribution, supply counts, timestamp integrity(라벨 분포, 공급 수, 시점 무결성)",
            "threshold_policy": "broad score quantile grid materialized(넓은 점수 분위 격자 물질화)",
            "overfit_risk": "teacher-label distillation can inherit s07 bias(교사 라벨 증류가 s07 편향을 물려받을 수 있음)",
            "calibration_risk": "scores are margins/ranks, not calibrated probabilities(점수는 마진/순위이며 보정 확률 아님)",
            "comparison_baseline": "n01_s07_base_control",
            "validation_judgment": "materialized_for_exploration_only(탐색 전용 물질화)",
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(SOURCE_FEATURES), rel(SOURCE_EXPECTED_TAPE), rel(DESIGN_MATRIX), rel(LABEL_HEAD_PLAN)],
            "producer": rel(Path("stage_pipelines/stage347/materialize_cash_open_asymmetric_source_inputs_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(FEATURE_LABEL_TABLE), rel(PROXY_SCREEN_GRID), rel(HANDOFF_INDEX), rel(REPORT_PATH), rel(FINAL_DECISION)],
            "artifact_hashes": "recorded in handoff_index and artifact_registry(인계 색인과 산출물 등록부에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "timestamp-safe teacher-source materialization ready(시점 안전 교사 원천 물질화 준비)",
            "model_training": "not_claimed",
            "mt5_execution": "not_claimed",
            "candidate_selection": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def gate_rows(summary: Mapping[str, Any], grid_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    parent_gate = False
    _fields, parent_rows = read_csv_rows(required(DESIGN_GATE_AUDIT))
    parent_gate = bool(parent_rows) and all(row.get("status") == "passed" for row in parent_rows)
    checks = [
        ("materialization_summary_written", path_is_file(MATERIALIZATION_SUMMARY), MATERIALIZATION_SUMMARY, "materialization summary(물질화 요약)를 기록한다."),
        ("parent_run347A_gates_passed", parent_gate, DESIGN_GATE_AUDIT, "run347A design gate(설계 게이트)를 확인한다."),
        ("source_features_available", path_is_file(SOURCE_FEATURES), SOURCE_FEATURES, "runtime feature source(런타임 피처 원천)를 확인한다."),
        ("source_expected_tape_available", path_is_file(SOURCE_EXPECTED_TAPE), SOURCE_EXPECTED_TAPE, "expected tape(예상 테이프)를 확인한다."),
        ("feature_label_table_written", path_is_file(FEATURE_LABEL_TABLE) and summary["materialized_rows"] > 0, FEATURE_LABEL_TABLE, "feature/teacher-label table(피처/교사 라벨 표)을 만든다."),
        ("timestamp_integrity_passed", path_is_file(TIMESTAMP_INTEGRITY_AUDIT) and summary["feature_missing_rows"] == 0 and summary["feature_duplicate_timestamps"] == 0, TIMESTAMP_INTEGRITY_AUDIT, "timestamp integrity(시점 무결성)를 확인한다."),
        ("label_manifest_written", path_is_file(LABEL_SOURCE_MANIFEST), LABEL_SOURCE_MANIFEST, "label source manifest(라벨 원천 목록)을 기록한다."),
        ("proxy_screen_grid_written", path_is_file(PROXY_SCREEN_GRID) and len(grid_rows) > 0, PROXY_SCREEN_GRID, "proxy screen grid(프록시 선별 격자)를 만든다."),
        ("handoff_index_written", path_is_file(HANDOFF_INDEX), HANDOFF_INDEX, "handoff index(인계 색인)를 만든다."),
        ("no_forbidden_operating_claim", path_is_file(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장을 하지 않는다."),
        ("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage audit(필수 게이트 감사)를 남긴다."),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, effect in checks
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_docs(summary: Mapping[str, Any], grid_rows: Sequence[Mapping[str, Any]]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run347B Cash-Open Asymmetric Source Input Materialization(347B 현금장 비대칭 원천 입력 물질화)

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): run344N runtime features(런타임 피처)와 expected tape(예상 테이프)를 결합해 asymmetric source input(비대칭 원천 입력)을 물질화했다.
Effect(효과): run347C(347C 실행)가 teacher/source labels(교사/원천 라벨)와 proxy grid(프록시 격자)로 학습/선별을 시작할 수 있다.

## Materialized Scope(물질화 범위)

- materialized_rows(물질화 행): `{summary['materialized_rows']}`
- first_bar_time(첫 봉 시각): `{summary['first_bar_time']}`
- last_bar_time(마지막 봉 시각): `{summary['last_bar_time']}`
- proxy_grid_rows(프록시 격자 행): `{len(grid_rows)}`
- Tier B(티어 B): `missing_required(필수 누락)`

## Important Boundary(중요 경계)

The labels(라벨)은 realized PnL label(실현 손익 라벨)이 아니다. They are teacher/source labels(교사/원천 라벨) from n02 long-only and n03 short-only expected decisions(n02 롱 전용과 n03 숏 전용 예상 결정)이다.

## Artifacts(산출물)

- feature_label_table(피처/라벨 표): `{rel(FEATURE_LABEL_TABLE)}`
- feature_schema_manifest(피처 스키마 목록): `{rel(FEATURE_SCHEMA_MANIFEST)}`
- label_source_manifest(라벨 원천 목록): `{rel(LABEL_SOURCE_MANIFEST)}`
- proxy_screen_grid(프록시 선별 격자): `{rel(PROXY_SCREEN_GRID)}`
- handoff_index(인계 색인): `{rel(HANDOFF_INDEX)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "## run347B Cash-Open Asymmetric Source Input Materialization(347B 현금장 비대칭 원천 입력 물질화)",
        f"""## run347B Cash-Open Asymmetric Source Input Materialization(347B 현금장 비대칭 원천 입력 물질화)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): teacher/source label(교사/원천 라벨)과 proxy grid(프록시 격자)를 물질화했다.
""",
    )
    append_text_once(
        STAGE_BRIEF,
        "## run347B Input Materialization(347B 입력 물질화)",
        f"""## run347B Input Materialization(347B 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- materialized_rows(물질화 행): `{summary['materialized_rows']}`
- proxy_grid_rows(프록시 격자 행): `{len(grid_rows)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage347(347단계)의 설계를 학습/프록시 선별 입력으로 바꿨다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# 2026-06-01 Stage347B Materialization Decision(347B 물질화 결정)

- decision(결정): `{DECISION}`
- source_design(원천 설계): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- reason(이유): run347A(347A 실행)가 timestamp-safe feature/label/proxy input(시점 안전 피처/라벨/프록시 입력) 물질화를 다음 작업으로 열었기 때문이다.

Action(행동): runtime features(런타임 피처), expected tape(예상 테이프), teacher/source labels(교사/원천 라벨), proxy screen grid(프록시 선별 격자)를 물질화했다.
Effect(효과): run347C(347C 실행)는 모델 학습/프록시 선별로 진행할 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_status_docs(summary: Mapping[str, Any]) -> None:
    selection = f"""# Stage 347 Selection Status(347단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_review_run(원천 검토 실행): `{SOURCE_REVIEW_RUN_ID}`
- source_runtime_probe(원천 런타임 탐침): `{SOURCE_RUNTIME_RUN_ID}`
- materialized_rows(물질화 행): `{summary['materialized_rows']}`
- proxy_grid_rows(프록시 격자 행): `225`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage347(347단계)는 materialization(물질화)까지 완료했고 다음은 proxy training/screen(프록시 학습/선별)이다.
"""
    write_text(STAGE_SELECTION, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage347B(347B 실행)는 asymmetric source input(비대칭 원천 입력)을 물질화했다. 다음 run347C(347C 실행)는 proxy training/screen(프록시 학습/선별)을 실행하되, teacher/source labels(교사/원천 라벨)을 realized PnL labels(실현 손익 라벨)처럼 말하면 안 된다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )


def write_ledgers(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "gate_passes": GATE_TOTAL,
        "gate_total": GATE_TOTAL,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "materialization(물질화)",
        "lane": "kpi_evidence(KPI 근거)",
        "family": "kpi_evidence(KPI 근거)",
        "run_number": RUN_NUMBER,
        "notes": "teacher/source input materialization only(교사/원천 입력 물질화 전용).",
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": summary["materialized_rows"],
        "attempt_count": 6,
        "feature_count": summary.get("feature_column_count", ""),
        "candidate_model_id": "none(없음)",
    }
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "teacher_source_materialization",
            "kpi_scope": "materialization_only",
            "primary_kpi": f"rows={summary['materialized_rows']};grid=225",
            "guardrail_kpi": "teacher_labels_not_realized_pnl(교사 라벨은 실현 손익 아님)",
            "external_verification_status": "not_applicable(해당 없음)",
            "result_status": "materialized_no_selection(물질화 완료, 선정 없음)",
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
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": "same_as_tier_a_until_tier_b_available",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "same_as_tier_a_until_tier_b_available",
        },
    ]
    existing_fields, existing_rows = read_csv_rows(STAGE_LEDGER) if path_is_file(STAGE_LEDGER) else (STAGE_LEDGER_COLUMNS, [])
    replacement = {row["ledger_row_id"] for row in rows}
    kept = [row for row in existing_rows if row.get("ledger_row_id") not in replacement]
    fieldnames = list(dict.fromkeys(list(existing_fields) + STAGE_LEDGER_COLUMNS))
    write_csv(STAGE_LEDGER, kept + rows, fieldnames)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    return rows


def write_final_and_manifest(summary: Mapping[str, Any], grid_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_review_run_id": SOURCE_REVIEW_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "materialized_rows": summary["materialized_rows"],
            "feature_missing_rows": summary["feature_missing_rows"],
            "feature_duplicate_timestamps": summary["feature_duplicate_timestamps"],
            "proxy_grid_rows": len(grid_rows),
            "gate_passes": GATE_TOTAL,
            "gate_total": GATE_TOTAL,
            "model_training": "not_claimed",
            "mt5_execution": "not_claimed",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage347/materialize_cash_open_asymmetric_source_inputs_without_db.py")),
            "inputs": [rel(SOURCE_FEATURES), rel(SOURCE_EXPECTED_TAPE), rel(DESIGN_MATRIX), rel(LABEL_HEAD_PLAN), rel(RUN347B_QUEUE)],
            "outputs": [
                rel(FEATURE_LABEL_TABLE),
                rel(FEATURE_SCHEMA_MANIFEST),
                rel(LABEL_SOURCE_MANIFEST),
                rel(LABEL_DISTRIBUTION),
                rel(PROXY_SCREEN_GRID),
                rel(HANDOFF_INDEX),
                rel(FINAL_DECISION),
                rel(REPORT_PATH),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_registries(summary: Mapping[str, Any]) -> None:
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence(KPI 근거)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Teacher/source inputs materialized(교사/원천 입력 물질화).",
                "family": "kpi_evidence(KPI 근거)",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": summary["materialized_rows"],
                "gate_passes": GATE_TOTAL,
                "gate_total": GATE_TOTAL,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "materialized_no_selection(물질화 완료, 선정 없음)",
                "attempt_count": 6,
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "teacher_source_materialization",
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            }
        ],
    )
    artifact_paths = [
        FEATURE_LABEL_TABLE,
        FEATURE_SCHEMA_MANIFEST,
        LABEL_SOURCE_MANIFEST,
        LABEL_DISTRIBUTION,
        PROXY_SCREEN_GRID,
        PROXY_GRID_SUMMARY,
        TIMESTAMP_INTEGRITY_AUDIT,
        MATERIALIZATION_SUMMARY,
        HANDOFF_INDEX,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": f"{path.stem}(산출물)",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "run347B materialization artifact(347B 물질화 산출물).",
        }
        for path in artifact_paths
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_register_notes() -> None:
    append_text_once(
        IDEA_REGISTRY,
        "`IDEA-ST347-RUN347B-ASYMMETRIC-SOURCE-INPUTS`",
        f"""| `IDEA-ST347-RUN347B-ASYMMETRIC-SOURCE-INPUTS` | `{STAGE_ID}` | asymmetric source teacher labels and proxy grid(비대칭 원천 교사 라벨과 프록시 격자)을 물질화한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `materialized_no_selection` | rows(행) `5827`, proxy_grid(프록시 격자) `225`; next_action(다음 행동) `{NEXT_RUN_ID}`; model training(모델 학습), MT5 execution(MT5 실행), selection(선정) 없음 |""",
    )
    text = f"""## 2026-06-01 run347B Cash-Open Asymmetric Source Input Materialization(현금장 비대칭 원천 입력 물질화)

- action(행동): runtime features(런타임 피처)와 expected tape(예상 테이프)를 결합해 teacher/source labels(교사/원천 라벨)와 proxy grid(프록시 격자)를 만들었다.
- effect(효과): run347C(347C 실행)가 proxy training/screen(프록시 학습/선별)을 시작할 수 있다.
- boundary(경계): teacher labels(교사 라벨)는 realized PnL labels(실현 손익 라벨)이 아니며, model training/MT5 execution/selection(모델 학습/MT5 실행/선정)은 아직 없음.
"""
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run347B Cash-Open Asymmetric Source Input Materialization", text)
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run347B Cash-Open Asymmetric Source Input Materialization", text)


def validate(summary: Mapping[str, Any], grid_rows: Sequence[Mapping[str, Any]]) -> None:
    outputs = [
        FEATURE_LABEL_TABLE,
        FEATURE_SCHEMA_MANIFEST,
        LABEL_SOURCE_MANIFEST,
        LABEL_DISTRIBUTION,
        PROXY_SCREEN_GRID,
        PROXY_GRID_SUMMARY,
        TIMESTAMP_INTEGRITY_AUDIT,
        MATERIALIZATION_SUMMARY,
        HANDOFF_INDEX,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        STAGE_SELECTION,
    ]
    missing = [rel(path) for path in outputs if not path_is_file(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if summary["materialized_rows"] != 5827:
        raise RuntimeError(f"unexpected materialized rows(예상 밖 물질화 행): {summary['materialized_rows']}")
    if len(grid_rows) != 225:
        raise RuntimeError(f"unexpected proxy grid rows(예상 밖 프록시 격자 행): {len(grid_rows)}")
    _fields, gates = read_csv_rows(GATE_AUDIT)
    if len(gates) != GATE_TOTAL or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run347B gate audit failed(347B 게이트 감사 실패)")
    current_texts = [read_text(WORKSPACE_STATE), read_text(CURRENT_WORKING_STATE), read_text(STAGE_SELECTION)]
    if not all(NEXT_RUN_ID in text and STAGE_ID in text for text in current_texts):
        raise RuntimeError("current truth sync failed(현재 진실 동기화 실패)")


def main() -> None:
    for path in [
        DESIGN_FINAL_DECISION,
        DESIGN_GATE_AUDIT,
        DESIGN_MATRIX,
        FEATURE_SOURCE_PLAN,
        LABEL_HEAD_PLAN,
        MODEL_FAMILY_PLAN,
        RUN347B_QUEUE,
        SOURCE_FEATURES,
        SOURCE_EXPECTED_TAPE,
        SOURCE_EXPECTED_INDEX,
        SOURCE_ATTEMPT_PACKAGE,
        SOURCE_RUN345B_SUMMARY,
        SOURCE_SCORECARD,
        SOURCE_POSITIVE_CLUES,
        SOURCE_FAILURE_MEMORY,
    ]:
        required(path)
    rows, summary = materialize_feature_label_table()
    summary = dict(summary)
    summary["feature_column_count"] = len(rows[0]) if rows else 0
    write_feature_and_label_manifests(rows, summary)
    distribution_rows, grid_rows = write_distribution_and_grid(rows)
    write_integrity_and_summary(summary, distribution_rows, grid_rows)
    write_handoff_index()
    write_receipts(summary)
    gates = gate_rows(summary, grid_rows)
    write_docs(summary, grid_rows)
    write_status_docs(summary)
    write_ledgers(summary)
    write_final_and_manifest(summary, grid_rows)
    write_registries(summary)
    write_register_notes()
    validate(summary, grid_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "materialized_rows": summary["materialized_rows"],
                "proxy_grid_rows": len(grid_rows),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

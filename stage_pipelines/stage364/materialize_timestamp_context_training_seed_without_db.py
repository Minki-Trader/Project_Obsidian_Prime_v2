from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "364_source_regime_label_pivot__dense_cost_recovery"
RUN_NUMBER = "run364D"
RUN_ID = "run364D_materialize_timestamp_context_training_seed_without_db_v1"
PARENT_RUN_ID = "run364C_review_timestamp_context_cost_surface_without_db_v1"
SOURCE_MATERIALIZATION_RUN_ID = "run364B_materialize_timestamp_context_cost_surface_without_db_v1"
NEXT_RUN_ID = "run364E_train_timestamp_context_cost_filter_model_without_db_v1"

STATUS = "completed_stage364D_timestamp_context_training_seed_materialized_model_training_opened_no_selection_no_mt5"
JUDGMENT = "timestamp_context_training_seed_materialized_ready_with_month_pressure_no_operating_claim"
DECISION = "stage364D_open_run364E_train_timestamp_context_cost_filter_model_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_timestamp_context_training_seed_no_new_model_training_"
    "no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_open_close_time_joined_to_runtime_bar_time_no_timezone_conversion"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SOURCE_REVIEW_DIR = STAGE_DIR / "02_runs" / "run364C"
SOURCE_MATERIALIZATION_DIR = STAGE_DIR / "02_runs" / "run364B"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_TRADE_TABLE = (
    ROOT
    / "stages"
    / "362_long_only_margin_grid__cost_buffer_first_branch"
    / "02_runs"
    / "run362B"
    / "q05_long_trade_probability_table.csv"
)
SOURCE_PASS_REVIEW = SOURCE_REVIEW_DIR / "pass_candidate_review.csv"
SOURCE_TRAINING_SEED_QUEUE = SOURCE_REVIEW_DIR / "run364D_training_seed_queue.csv"
SOURCE_REVIEW_FINAL = SOURCE_REVIEW_DIR / "final_decision.json"
SOURCE_REVIEW_GATE_AUDIT = SOURCE_REVIEW_DIR / "required_gate_coverage_audit.csv"
SOURCE_REVIEW_REPORT = REVIEW_DIR / "run364C_timestamp_context_cost_surface_review.md"
SOURCE_CROSS_SPLIT = SOURCE_MATERIALIZATION_DIR / "timestamp_context_cross_split.csv"
SOURCE_FAILURE_ATTRIBUTION = SOURCE_MATERIALIZATION_DIR / "timestamp_context_failure_attribution.csv"
SOURCE_MATERIALIZER = ROOT / "stage_pipelines" / "stage364" / "materialize_timestamp_context_cost_surface_without_db.py"

INPUT_FILES = [
    SOURCE_TRADE_TABLE,
    SOURCE_PASS_REVIEW,
    SOURCE_TRAINING_SEED_QUEUE,
    SOURCE_REVIEW_FINAL,
    SOURCE_REVIEW_GATE_AUDIT,
    SOURCE_REVIEW_REPORT,
    SOURCE_CROSS_SPLIT,
    SOURCE_FAILURE_ATTRIBUTION,
    SOURCE_MATERIALIZER,
]

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
TRAINING_SEED_TABLE = RUN_DIR / "timestamp_context_training_seed_table.csv"
FEATURE_SCHEMA = RUN_DIR / "timestamp_context_feature_schema.json"
SEED_METRICS = RUN_DIR / "seed_metric_summary.csv"
MONTH_PRESSURE = RUN_DIR / "month_pressure_matrix.csv"
MODEL_TASK_QUEUE = RUN_DIR / "run364E_model_task_queue.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

REPORT_PATH = REVIEW_DIR / "run364D_timestamp_context_training_seed_materialization.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364D_timestamp_context_training_seed_materialization.md"

RAW_FEATURE_COLUMNS = [
    "p_short",
    "p_flat",
    "p_long",
    "margin_gap_actual",
    "p_long_minus_p_short",
    "p_long_minus_p_flat",
    "open_hour",
    "open_dow",
    "minute_bucket15",
    "is_hour17",
    "is_minute30_or45",
    "is_primary_toxic_bucket",
    "open_hour_sin",
    "open_hour_cos",
    "open_dow_sin",
    "open_dow_cos",
    "minute_bucket15_sin",
    "minute_bucket15_cos",
    "hour17_p_long_interaction",
    "hour17_margin_gap_interaction",
    "hour17_plong_minus_pshort_interaction",
]
LABEL_COLUMNS = [
    "label_cost_positive_0_30",
    "label_cost_nonnegative_0_30",
    "label_loss_severity_0_30",
    "label_primary_context_keep",
    "label_hour17_score_guard_keep",
]
SEED_IDS = [
    "dense_control_all_long",
    "primary_hour_minute_context_guard",
    "hour17_p_long_q80_guard",
    "support_hour_dow_context_guard",
]


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
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with open(fs_path(temp_path), "w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for row in rows_list:
                writer.writerow({key: row.get(key, "") for key in fieldnames})
        for attempt in range(12):
            try:
                os.replace(fs_path(temp_path), fs_path(path))
                break
            except PermissionError:
                if attempt == 11:
                    raise
                time.sleep(0.25)
    finally:
        if exists(temp_path):
            os.remove(fs_path(temp_path))


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    replacements = {tuple(str(row.get(key, "")) for key in key_fields): dict(row) for row in rows}
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in existing:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        if key in replacements:
            output.append(replacements[key])
            seen.add(key)
        else:
            output.append(row)
    for key, row in replacements.items():
        if key not in seen:
            output.append(row)
    write_csv(path, output, fieldnames)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def load_materializer() -> Any:
    spec = importlib.util.spec_from_file_location("stage364b_materializer", SOURCE_MATERIALIZER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Stage364B materializer module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_gate_passed() -> bool:
    _, rows = read_csv_rows(SOURCE_REVIEW_GATE_AUDIT)
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def load_seed_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    materializer = load_materializer()
    frame = materializer.load_trade_table().copy()
    variants = {variant["variant_id"]: variant for variant in materializer.build_variants(frame)}
    masks = {
        "dense_control_all_long": pd.Series(True, index=frame.index),
        "primary_hour_minute_context_guard": materializer.select_mask(frame, variants["s364_r02_drop_worst_open_hour_minute_bucket15_k2"]),
        "hour17_p_long_q80_guard": materializer.select_mask(frame, variants["s364_r03_h17_p_long_gt_q80"]),
        "support_hour_dow_context_guard": materializer.select_mask(frame, variants["s364_r02_drop_worst_open_hour_open_dow_k3"]),
    }
    frame["cost_0_30_net"] = frame["net_profit"].astype(float) - 0.30
    frame["label_cost_positive_0_30"] = (frame["cost_0_30_net"] > 0).astype(int)
    frame["label_cost_nonnegative_0_30"] = (frame["cost_0_30_net"] >= 0).astype(int)
    frame["label_loss_severity_0_30"] = frame["cost_0_30_net"].where(frame["cost_0_30_net"] < 0, 0.0).abs().round(6)
    frame["is_hour17"] = (frame["open_hour"].astype(int) == 17).astype(int)
    frame["is_minute30_or45"] = frame["minute_bucket15"].astype(int).isin([30, 45]).astype(int)
    frame["is_primary_toxic_bucket"] = ((frame["open_hour"].astype(int) == 17) & frame["minute_bucket15"].astype(int).isin([30, 45])).astype(int)
    frame["open_hour_sin"] = frame["open_hour"].astype(float).map(lambda value: math.sin(2.0 * math.pi * value / 24.0))
    frame["open_hour_cos"] = frame["open_hour"].astype(float).map(lambda value: math.cos(2.0 * math.pi * value / 24.0))
    frame["open_dow_sin"] = frame["open_dow"].astype(float).map(lambda value: math.sin(2.0 * math.pi * value / 7.0))
    frame["open_dow_cos"] = frame["open_dow"].astype(float).map(lambda value: math.cos(2.0 * math.pi * value / 7.0))
    frame["minute_bucket15_sin"] = frame["minute_bucket15"].astype(float).map(lambda value: math.sin(2.0 * math.pi * value / 60.0))
    frame["minute_bucket15_cos"] = frame["minute_bucket15"].astype(float).map(lambda value: math.cos(2.0 * math.pi * value / 60.0))
    frame["hour17_p_long_interaction"] = frame["is_hour17"] * frame["p_long"].astype(float)
    frame["hour17_margin_gap_interaction"] = frame["is_hour17"] * frame["margin_gap_actual"].astype(float)
    frame["hour17_plong_minus_pshort_interaction"] = frame["is_hour17"] * frame["p_long_minus_p_short"].astype(float)
    frame["label_primary_context_keep"] = masks["primary_hour_minute_context_guard"].astype(int)
    frame["label_hour17_score_guard_keep"] = masks["hour17_p_long_q80_guard"].astype(int)
    for seed_id, mask in masks.items():
        frame[f"seed_keep__{seed_id}"] = mask.astype(int)
    frame["seed_membership_count"] = frame[[f"seed_keep__{seed_id}" for seed_id in SEED_IDS]].sum(axis=1).astype(int)
    frame["wfo_fold_id"] = frame["split"].astype(str) + "_" + frame["open_dt"].dt.to_period("Q").astype(str)
    frame["month_id"] = frame["year_month"].astype(str)
    frame["training_seed_claim_boundary"] = CLAIM_BOUNDARY
    return frame, variants


def profit_factor(values: pd.Series) -> float:
    gains = values[values > 0].sum()
    losses = values[values < 0].sum()
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return float(gains / abs(losses))


def seed_metrics(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed_id in SEED_IDS:
        selected = frame[frame[f"seed_keep__{seed_id}"] == 1].copy()
        for split in ("validation", "oos"):
            split_frame = selected[selected["split"].eq(split)]
            days = float(split_frame["feature_day_count"].iloc[0]) if not split_frame.empty else 0.0
            cost_values = split_frame["cost_0_30_net"].astype(float)
            trade_count = int(len(split_frame))
            net = float(cost_values.sum()) if trade_count else 0.0
            rows.append({
                "run_id": RUN_ID,
                "seed_id": seed_id,
                "split": split,
                "trade_count": trade_count,
                "feature_day_count": round(days, 4),
                "trade_density": round(trade_count / days, 10) if days else 0.0,
                "cost_0_30_net": round(net, 2),
                "cost_0_30_profit_factor": round(profit_factor(cost_values), 10) if trade_count else 0.0,
                "expectancy_cost_0_30": round(net / trade_count, 10) if trade_count else 0.0,
                "win_rate_cost_0_30": round(float((cost_values > 0).mean()), 10) if trade_count else 0.0,
                "worst_trade_cost_0_30": round(float(cost_values.min()), 2) if trade_count else 0.0,
                "best_trade_cost_0_30": round(float(cost_values.max()), 2) if trade_count else 0.0,
                "claim_boundary": CLAIM_BOUNDARY,
            })
    dense = {(row["split"]): row for row in rows if row["seed_id"] == "dense_control_all_long"}
    for row in rows:
        base = dense.get(row["split"], {})
        row["net_delta_vs_dense_control"] = round(as_float(row["cost_0_30_net"]) - as_float(base.get("cost_0_30_net")), 2)
        row["density_delta_vs_dense_control"] = round(as_float(row["trade_density"]) - as_float(base.get("trade_density")), 10)
    return rows


def month_pressure_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed_id in SEED_IDS:
        selected = frame[frame[f"seed_keep__{seed_id}"] == 1].copy()
        grouped = (
            selected.groupby(["split", "year_month"], dropna=False)
            .agg(cost_0_30_net=("cost_0_30_net", "sum"), trade_count=("cost_0_30_net", "size"))
            .reset_index()
        )
        for _, month_row in grouped.iterrows():
            month_net = float(month_row["cost_0_30_net"])
            rows.append({
                "run_id": RUN_ID,
                "seed_id": seed_id,
                "split": month_row["split"],
                "year_month": month_row["year_month"],
                "cost_0_30_net": round(month_net, 2),
                "trade_count": int(month_row["trade_count"]),
                "month_pressure_class": "positive_month" if month_net > 0 else "negative_or_flat_month",
                "promotion_risk_flag": "true" if month_net <= 0 else "false",
                "claim_boundary": CLAIM_BOUNDARY,
            })
    return rows


def task_queue_rows(metric_rows: Sequence[Mapping[str, Any]], pressure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    primary_val = next(row for row in metric_rows if row["seed_id"] == "primary_hour_minute_context_guard" and row["split"] == "validation")
    primary_oos = next(row for row in metric_rows if row["seed_id"] == "primary_hour_minute_context_guard" and row["split"] == "oos")
    hour17_oos = next(row for row in metric_rows if row["seed_id"] == "hour17_p_long_q80_guard" and row["split"] == "oos")
    primary_pressure = [row for row in pressure_rows if row["seed_id"] == "primary_hour_minute_context_guard"]
    negative_months = sum(1 for row in primary_pressure if row["month_pressure_class"] != "positive_month")
    return [
        {
            "queue_id": "s364E_r01_cost_filter_lgbm_seed",
            "priority": 1,
            "model_family": "LightGBM_or_tree_exportable_to_ONNX(LightGBM 또는 ONNX 변환 가능 트리)",
            "source_artifact": rel(TRAINING_SEED_TABLE),
            "feature_schema": rel(FEATURE_SCHEMA),
            "target_label": "label_cost_positive_0_30",
            "objective": "learn timestamp context cost filter(시점 문맥 비용 필터 학습)",
            "required_control": "beat dense_control_all_long on validation and OOS(검증/표본외에서 전체 롱 고밀도 대조 초과)",
            "seed_reference": f"primary validation_net={primary_val['cost_0_30_net']};oos_net={primary_oos['cost_0_30_net']};hour17_oos_net={hour17_oos['cost_0_30_net']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364E_r02_month_pressure_wfo_control",
            "priority": 2,
            "model_family": "WFO_pressure_control(WFO 압박 대조)",
            "source_artifact": rel(MONTH_PRESSURE),
            "feature_schema": rel(FEATURE_SCHEMA),
            "target_label": "label_cost_positive_0_30",
            "objective": "reject models that only win a few months(소수 월만 이기는 모델 거부)",
            "required_control": "positive month coverage must improve before promotion(승격 전 양수 월 커버리지 개선 필요)",
            "seed_reference": f"primary_negative_or_flat_months={negative_months}/{len(primary_pressure)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364E_r03_pseudo_label_context_keep_control",
            "priority": 3,
            "model_family": "pseudo_label_control(의사 라벨 대조)",
            "source_artifact": rel(TRAINING_SEED_TABLE),
            "feature_schema": rel(FEATURE_SCHEMA),
            "target_label": "label_primary_context_keep",
            "objective": "separate rule imitation from real profit label(규칙 모방과 실제 수익 라벨 분리)",
            "required_control": "profit-label model must beat pseudo-label imitation(수익 라벨 모델이 의사 라벨 모방을 넘어야 함)",
            "seed_reference": "primary context keep is evidence label only(주 문맥 keep은 근거 라벨 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "s364E_r04_onnx_handoff_precheck",
            "priority": 4,
            "model_family": "ONNX_export_precheck(ONNX 내보내기 사전 점검)",
            "source_artifact": rel(FEATURE_SCHEMA),
            "feature_schema": rel(FEATURE_SCHEMA),
            "target_label": "label_cost_positive_0_30",
            "objective": "prepare stable numeric feature order for ONNX(ONNX용 안정 숫자 피처 순서 준비)",
            "required_control": "feature order and output schema must be frozen before MT5 probe(MT5 탐침 전 피처 순서와 출력 스키마 고정)",
            "seed_reference": f"feature_count={len(RAW_FEATURE_COLUMNS)};label_count={len(LABEL_COLUMNS)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_role": path.stem,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and path.is_file() else "",
            "availability": "tracked_or_ignored_with_manifest",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_feature_schema(frame: pd.DataFrame) -> None:
    payload = {
        "schema_version": "stage364D_timestamp_context_training_seed_v1",
        "run_id": RUN_ID,
        "source_trade_table": rel(SOURCE_TRADE_TABLE),
        "row_count": int(len(frame)),
        "split_counts": {str(key): int(value) for key, value in frame["split"].value_counts().sort_index().items()},
        "feature_columns": RAW_FEATURE_COLUMNS,
        "label_columns": LABEL_COLUMNS,
        "seed_membership_columns": [f"seed_keep__{seed_id}" for seed_id in SEED_IDS],
        "feature_boundary": "all feature columns are known at q05 signal open timestamp(모든 피처 컬럼은 q05 신호 진입 시점에 알려짐)",
        "label_boundary": "label columns use realized future trade result and must never feed features(라벨 컬럼은 미래 실현 거래 결과이며 피처로 쓰면 안 됨)",
        "split_boundary": "source report-derived validation/OOS split retained(원천 보고서 파생 검증/표본외 분할 유지)",
        "output_schema_intent": "future model should output cost-filter probability or keep/drop score(미래 모델은 비용 필터 확률 또는 keep/drop 점수 출력)",
        "ea_output_boundary": "not an EA bundle and not ONNX yet(EA 번들과 ONNX 아님)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FEATURE_SCHEMA, payload)


def write_receipts(frame: pd.DataFrame, metric_rows: Sequence[Mapping[str, Any]], pressure_rows: Sequence[Mapping[str, Any]], task_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(WORK_PACKET, {
        "run_id": RUN_ID,
        "primary_family": "experiment_materialization(실험 구체화)",
        "primary_skill": "obsidian-data-integrity(데이터 무결성)",
        "support_skills": [
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-result-judgment(결과 판정)",
            "obsidian-exploration-mandate(탐색 명령)",
        ],
        "required_gates": [
            "input_presence",
            "source_review_gate_passed",
            "training_seed_table_materialized",
            "feature_schema_materialized",
            "month_pressure_materialized",
            "model_task_queue_materialized",
            "claim_boundary_enforced",
            "ledger_synced",
        ],
        "status": STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(DATA_INTEGRITY_RECEIPT, {
        "data_source": [rel(SOURCE_TRADE_TABLE), rel(SOURCE_PASS_REVIEW), rel(SOURCE_TRAINING_SEED_QUEUE)],
        "time_axis": TIME_AXIS,
        "sample_scope": f"US100 M5 q05 long-only report-derived trades; rows={len(frame)}; splits={dict(frame['split'].value_counts())}",
        "missing_or_duplicate_check": f"input_hash duplicates={int(frame['input_hash'].duplicated().sum())}; duplicate trades are not removed in materialization(중복 거래 제거 없음)",
        "feature_label_boundary": "feature columns are timestamp-known; labels are realized PnL and pseudo labels only(피처는 시점상 알려짐, 라벨은 실현 손익 및 의사 라벨)",
        "split_boundary": "validation/OOS retained from source table; no train split synthesized(원천 검증/표본외 유지, 학습 분할 합성 없음)",
        "leakage_risk": "Stage364C reviewed OOS, so this seed is not a selection claim and must be re-trained with WFO controls(364C가 OOS를 보았으므로 선택 주장이 아니며 WFO 대조 필요)",
        "data_hash_or_identity": {
            "source_trade_table_sha256": sha256_file(SOURCE_TRADE_TABLE),
            "training_seed_rows": int(len(frame)),
            "feature_count": len(RAW_FEATURE_COLUMNS),
            "label_count": len(LABEL_COLUMNS),
        },
        "integrity_judgment": "usable_with_boundary",
    })
    write_json(LINEAGE_RECEIPT, {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": "python stage_pipelines/stage364/materialize_timestamp_context_training_seed_without_db.py",
        "consumer": [rel(REPORT_PATH), rel(MODEL_TASK_QUEUE), rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
        "artifact_paths": [rel(TRAINING_SEED_TABLE), rel(FEATURE_SCHEMA), rel(SEED_METRICS), rel(MONTH_PRESSURE), rel(MODEL_TASK_QUEUE), rel(FINAL_DECISION)],
        "artifact_hashes": "written to artifact_registry after closeout(종료 후 산출물 등록부에 기록)",
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked reports plus ignored run artifacts with manifest(추적 보고서와 manifest가 있는 ignored 실행 산출물)",
        "lineage_judgment": "connected_with_boundary",
    })
    write_json(JUDGMENT_RECEIPT, {
        "result_subject": RUN_ID,
        "evidence_available": [rel(TRAINING_SEED_TABLE), rel(FEATURE_SCHEMA), rel(SEED_METRICS), rel(MONTH_PRESSURE), rel(REPORT_PATH), rel(FINAL_DECISION)],
        "evidence_missing": "no model training, no ONNX export, no proxy execution, no MT5 execution, no candidate selection, Tier B missing_required(모델 학습 없음, ONNX 내보내기 없음, 프록시 실행 없음, MT5 실행 없음, 후보 선택 없음, Tier B 필수 누락)",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "the seed table is ready for model training, not ready for live trading(씨앗 표는 모델 학습 준비이지 실거래 준비가 아님)",
    })
    write_json(CLAIM_RECEIPT, {
        "run_id": RUN_ID,
        "model_training": "not_run",
        "onnx_export": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_json(RUN_MANIFEST, {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "command": "python stage_pipelines/stage364/materialize_timestamp_context_training_seed_without_db.py",
        "input_manifest": rel(INPUT_MANIFEST),
        "outputs": [rel(TRAINING_SEED_TABLE), rel(FEATURE_SCHEMA), rel(SEED_METRICS), rel(MONTH_PRESSURE), rel(MODEL_TASK_QUEUE), rel(FINAL_DECISION)],
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    })
    primary_val = next(row for row in metric_rows if row["seed_id"] == "primary_hour_minute_context_guard" and row["split"] == "validation")
    primary_oos = next(row for row in metric_rows if row["seed_id"] == "primary_hour_minute_context_guard" and row["split"] == "oos")
    write_json(FINAL_DECISION, {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_materialization_run_id": SOURCE_MATERIALIZATION_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "training_seed_rows": int(len(frame)),
        "feature_columns": len(RAW_FEATURE_COLUMNS),
        "label_columns": len(LABEL_COLUMNS),
        "seed_metric_rows": len(metric_rows),
        "month_pressure_rows": len(pressure_rows),
        "model_task_rows": len(task_rows),
        "primary_seed_id": "primary_hour_minute_context_guard",
        "primary_seed_validation_cost_0_30_net": primary_val["cost_0_30_net"],
        "primary_seed_oos_cost_0_30_net": primary_oos["cost_0_30_net"],
        "primary_seed_validation_density": primary_val["trade_density"],
        "primary_seed_oos_density": primary_oos["trade_density"],
        "model_training_ready": "ready_with_boundary",
        "new_model_training": "not_run",
        "onnx_export": "not_run",
        "new_proxy_execution": "not_run",
        "mt5_execution": "not_run",
        "candidate_selection": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": 0,
        "gate_total": 0,
    })


def write_run_artifacts(frame: pd.DataFrame, metric_rows: Sequence[Mapping[str, Any]], pressure_rows: Sequence[Mapping[str, Any]], task_rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    output_columns = [
        "split",
        "attempt_name",
        "trade_index",
        "direction",
        "open_time",
        "close_time",
        "net_profit",
        "cost_0_30_net",
        "source_report_sha256",
        "bar_time",
        "input_hash",
        "month_id",
        "wfo_fold_id",
        *RAW_FEATURE_COLUMNS,
        *LABEL_COLUMNS,
        *[f"seed_keep__{seed_id}" for seed_id in SEED_IDS],
        "seed_membership_count",
        "feature_day_count",
        "probability_join_status",
        "time_axis",
        "training_seed_claim_boundary",
    ]
    write_csv(TRAINING_SEED_TABLE, frame[output_columns].to_dict("records"))
    write_feature_schema(frame)
    write_csv(SEED_METRICS, metric_rows)
    write_csv(MONTH_PRESSURE, pressure_rows)
    write_csv(MODEL_TASK_QUEUE, task_rows)
    write_receipts(frame, metric_rows, pressure_rows, task_rows)


def gate_rows() -> list[dict[str, Any]]:
    final = read_json(FINAL_DECISION) if exists(FINAL_DECISION) else {}
    _, project_rows = read_csv_rows(PROJECT_LEDGER)
    _, stage_rows = read_csv_rows(STAGE_LEDGER)
    gates = [
        ("input_trade_table_present", exists(SOURCE_TRADE_TABLE), SOURCE_TRADE_TABLE, "q05 trade table(q05 거래표) 확인"),
        ("input_pass_review_present", exists(SOURCE_PASS_REVIEW), SOURCE_PASS_REVIEW, "run364C pass review(364C 통과 검토) 확인"),
        ("source_review_gate_passed", source_gate_passed(), SOURCE_REVIEW_GATE_AUDIT, "run364C gate(364C 게이트) 통과 확인"),
        ("source_next_run_matches", read_json(SOURCE_REVIEW_FINAL).get("next_run_id") == RUN_ID, SOURCE_REVIEW_FINAL, "source next run(원천 다음 실행) 일치"),
        ("training_seed_table_present", exists(TRAINING_SEED_TABLE) and as_int(final.get("training_seed_rows")) == 1114, TRAINING_SEED_TABLE, "training seed table(학습 씨앗 표) 1114행"),
        ("feature_schema_present", exists(FEATURE_SCHEMA) and as_int(final.get("feature_columns")) == len(RAW_FEATURE_COLUMNS), FEATURE_SCHEMA, "feature schema(피처 스키마) 생성"),
        ("seed_metrics_present", exists(SEED_METRICS) and as_int(final.get("seed_metric_rows")) == 8, SEED_METRICS, "seed metrics(씨앗 지표) 생성"),
        ("month_pressure_present", exists(MONTH_PRESSURE) and as_int(final.get("month_pressure_rows")) > 0, MONTH_PRESSURE, "month pressure(月 압박) 생성"),
        ("model_task_queue_present", exists(MODEL_TASK_QUEUE) and as_int(final.get("model_task_rows")) == 4, MODEL_TASK_QUEUE, "model task queue(모델 작업 대기열) 생성"),
        ("model_training_not_run", final.get("new_model_training") == "not_run", FINAL_DECISION, "model training(모델 학습) 없음"),
        ("onnx_not_run", final.get("onnx_export") == "not_run", FINAL_DECISION, "ONNX export(ONNX 내보내기) 없음"),
        ("candidate_selection_not_run", final.get("candidate_selection") == "not_run", FINAL_DECISION, "candidate selection(후보 선택) 없음"),
        ("report_present", exists(REPORT_PATH), REPORT_PATH, "report(보고서) 존재"),
        ("selection_status_synced", NEXT_RUN_ID in read_text(SELECTION_STATUS), SELECTION_STATUS, "selection status(선택 상태) 다음 실행 동기화"),
        ("workspace_state_synced", NEXT_RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "workspace state(작업공간 상태) 다음 실행 동기화"),
        ("project_ledger_synced", sum(1 for row in project_rows if row.get("run_id") == RUN_ID) == 3, PROJECT_LEDGER, "project ledger(프로젝트 장부) 3행"),
        ("stage_ledger_synced", sum(1 for row in stage_rows if row.get("run_id") == RUN_ID) == 3, STAGE_LEDGER, "stage ledger(단계 장부) 3행"),
        ("claim_boundary_receipt", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "claim receipt(주장 영수증) 존재"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": rel(path),
            "description": description,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, path, description in gates
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return ""
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def write_reports(metric_rows: Sequence[Mapping[str, Any]], task_rows: Sequence[Mapping[str, Any]]) -> None:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    primary_metrics = [row for row in metric_rows if row["seed_id"] in {"dense_control_all_long", "primary_hour_minute_context_guard", "hour17_p_long_q80_guard"}]
    report = f"""# run364D Timestamp Context Training Seed Materialization(run364D 시점 문맥 학습 씨앗 구체화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): q05 long-only trade table(q05 롱 단독 거래표) `1114`행에 timestamp-safe feature columns(시점 안전 피처 컬럼), realized label columns(실현 라벨 컬럼), seed membership(씨앗 소속), month pressure(月 압박)를 붙였다.

Effect(효과): 다음 실행은 hard-coded context rule(하드코딩 문맥 규칙)이 아니라 model training(모델 학습)과 ONNX precheck(ONNX 사전 점검)으로 넘어갈 수 있다.

## Result(결과)

- training_seed_rows(학습 씨앗 행): `{final["training_seed_rows"]}`
- feature_columns(피처 컬럼): `{final["feature_columns"]}`
- label_columns(라벨 컬럼): `{final["label_columns"]}`
- seed_metric_rows(씨앗 지표 행): `{final["seed_metric_rows"]}`
- month_pressure_rows(月 압박 행): `{final["month_pressure_rows"]}`
- model_task_rows(모델 작업 행): `{final["model_task_rows"]}`
- primary_seed_id(주 씨앗 ID): `{final["primary_seed_id"]}`
- primary_seed_validation_cost_0_30_net(주 씨앗 검증 +0.30 비용 순수익): `{final["primary_seed_validation_cost_0_30_net"]}`
- primary_seed_oos_cost_0_30_net(주 씨앗 표본외 +0.30 비용 순수익): `{final["primary_seed_oos_cost_0_30_net"]}`
- primary_seed_validation_density(주 씨앗 검증 밀도): `{final["primary_seed_validation_density"]}`
- primary_seed_oos_density(주 씨앗 표본외 밀도): `{final["primary_seed_oos_density"]}`

## Seed Metrics(씨앗 지표)

{markdown_table(primary_metrics, ["seed_id", "split", "trade_count", "trade_density", "cost_0_30_net", "cost_0_30_profit_factor", "expectancy_cost_0_30", "net_delta_vs_dense_control"])}

## Model Task Queue(모델 작업 대기열)

{markdown_table(task_rows, ["queue_id", "priority", "model_family", "target_label", "objective", "required_control"])}

## Artifact Boundary(산출물 경계)

- training_seed_table(학습 씨앗 표): `{rel(TRAINING_SEED_TABLE)}`
- feature_schema(피처 스키마): `{rel(FEATURE_SCHEMA)}`
- seed_metrics(씨앗 지표): `{rel(SEED_METRICS)}`
- month_pressure(月 압박): `{rel(MONTH_PRESSURE)}`
- model_task_queue(모델 작업 대기열): `{rel(MODEL_TASK_QUEUE)}`

Action(행동): `{NEXT_RUN_ID}`를 열었다.

Effect(효과): 다음 작업은 cost-filter model(비용 필터 모델)을 학습하되, dense control(고밀도 대조), month pressure(月 압박), ONNX handoff(ONNX 인계)를 같이 검증한다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, f"""# {TODAY} Stage364D Timestamp Context Training Seed Decision(364D 시점 문맥 학습 씨앗 결정)

- decision(결정): `{DECISION}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`

Action(행동): timestamp context(시점 문맥)를 feature/label separated training seed(피처/라벨 분리 학습 씨앗)로 구체화했다.

Effect(효과): 다음 실행은 실제 model training(모델 학습)을 할 수 있지만, 아직 ONNX(온엑스), MT5(메타트레이더5), candidate selection(후보 선택)은 아니다.

Evidence(근거): `{rel(TRAINING_SEED_TABLE)}`, `{rel(FEATURE_SCHEMA)}`, `{rel(MODEL_TASK_QUEUE)}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")
    write_text(SELECTION_STATUS, f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `training_seed_materialized_model_training_opened_no_selection(학습 씨앗 구체화 완료, 모델 학습 열림, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364D Training Seed Closeout(364D 학습 씨앗 종료 기록)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{sum(1 for row in gates if row["status"] == "passed")}/{len(gates)}`
- training_seed_rows(학습 씨앗 행): `{final["training_seed_rows"]}`
- feature_columns(피처 컬럼): `{final["feature_columns"]}`
- label_columns(라벨 컬럼): `{final["label_columns"]}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364C(364C)의 timestamp context seed(시점 문맥 씨앗)를 학습용 표와 스키마로 구체화했다.

Effect(효과): Stage364(364단계)는 후보 선택 없이 model training(모델 학습)으로 진행한다.
""")
    append_text_once(STAGE_BRIEF, "## run364D Training Seed Closeout", f"""## run364D Training Seed Closeout(364D 학습 씨앗 종료)

Action(행동): timestamp-safe feature/label seed table(시점 안전 피처/라벨 씨앗 표) `{final["training_seed_rows"]}`행을 만들었다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 model training(모델 학습)과 ONNX precheck(ONNX 사전 점검)를 시작한다.
""")
    append_text_once(REVIEW_INDEX, "run364D_timestamp_context_training_seed_materialization", f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}` - timestamp context training seed materialization(시점 문맥 학습 씨앗 구체화).""")
    append_text_once(STAGE_README, "run364D Training Seed", f"""## run364D Training Seed(364D 학습 씨앗)

Action(행동): q05 trade table(q05 거래표)를 model training seed(모델 학습 씨앗)로 구체화했다.

Effect(효과): 다음 실행은 `{NEXT_RUN_ID}`이고, 운영 주장은 없다.
""")


def replace_stage_brief_header() -> None:
    text = read_text(STAGE_BRIEF)
    replacements = {
        "- current_run_id(": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(": "- selection_status(선택 상태): `training_seed_materialized_model_training_opened_no_selection(학습 씨앗 구체화 완료, 모델 학습 열림, 선택 없음)`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    next_lines = []
    for line in text.splitlines():
        replaced = False
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                next_lines.append(value)
                replaced = True
                break
        if not replaced:
            next_lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(next_lines))


def registry_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    final = read_json(FINAL_DECISION)
    gates = gate_rows()
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "timestamp_context_training_seed(시점 문맥 학습 씨앗)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage364D timestamp context training seed materialization(Stage364D 시점 문맥 학습 씨앗 구체화).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["training_seed_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(TRAINING_SEED_TABLE),
        "result_status": STATUS,
        "sample_rows": final["training_seed_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_materialization(실험 구체화)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "lane": "timestamp_context_training_seed(시점 문맥 학습 씨앗)",
        "family": "experiment_materialization(실험 구체화)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can timestamp context become model-training input?(시점 문맥을 모델 학습 입력으로 만들 수 있는가?)",
        "metric_scope": "materialization_only_no_runtime(구체화 전용, 런타임 없음)",
        "feature_count": final["feature_columns"],
    }
    tier_a = dict(common)
    tier_a.update({
        "subrun_id": f"{RUN_ID}__Tier_A",
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "row_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "kpi_scope": "training_seed_materialization(학습 씨앗 구체화)",
        "primary_kpi": f"rows={final['training_seed_rows']};features={final['feature_columns']};labels={final['label_columns']}",
        "guardrail_kpi": f"model_training={final['new_model_training']};onnx={final['onnx_export']};candidate_selection={final['candidate_selection']}",
    })
    tier_b = dict(tier_a)
    tier_b.update({
        "subrun_id": f"{RUN_ID}__Tier_B",
        "ledger_row_id": f"{RUN_ID}__Tier_B",
        "row_id": f"{RUN_ID}__Tier_B",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier_scope": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
        "primary_kpi": "missing_required(필수 누락)",
        "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
    })
    combined = dict(tier_a)
    combined.update({
        "subrun_id": f"{RUN_ID}__Tier_AplusB",
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "row_id": f"{RUN_ID}__Tier_AplusB",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "status": "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)",
        "primary_kpi": "combined_not_run(합산 실행 없음)",
        "guardrail_kpi": "do_not_synthesize_combined_result(합산 결과 합성 금지)",
    })
    return [tier_a], [tier_a, tier_b, combined], [tier_a, tier_b, combined]


def write_registries() -> None:
    run_rows, project_rows, stage_rows = registry_rows()
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=True)


def write_workspace_and_notes() -> None:
    final = read_json(FINAL_DECISION)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage364D(364D 실행)가 timestamp context(시점 문맥)를 학습 씨앗 표 `{final["training_seed_rows"]}`행과 feature schema(피처 스키마) `{final["feature_columns"]}`개로 구체화했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 cost-filter model(비용 필터 모델)을 학습하고 ONNX precheck(ONNX 사전 점검)를 붙이는 것이다.
""")
    append_text_once(WORKSPACE_CHANGELOG, "run364D_materialize_timestamp_context_training_seed_without_db_v1", f"""## {TODAY} run364D Timestamp Context Training Seed Materialization(364D 시점 문맥 학습 씨앗 구체화)

Action(행동): q05 report-derived trade table(q05 보고서 파생 거래표)을 feature/label separated training seed(피처/라벨 분리 학습 씨앗)로 만들었다.

Effect(효과): 다음 실행은 `{NEXT_RUN_ID}`이며, 아직 model training(모델 학습), ONNX export(ONNX 내보내기), MT5 execution(MT5 실행), candidate selection(후보 선택)은 없다.
""")
    append_text_once(IDEA_REGISTRY, "IDEA-ST364D-TIMESTAMP-CONTEXT-TRAINING-SEED", f"""## IDEA-ST364D-TIMESTAMP-CONTEXT-TRAINING-SEED

- idea(아이디어): timestamp context(시점 문맥)를 hard-coded rule(하드코딩 규칙)이 아니라 cost-filter model training seed(비용 필터 모델 학습 씨앗)로 사용한다.
- training_seed_table(학습 씨앗 표): `{rel(TRAINING_SEED_TABLE)}`.
- feature_schema(피처 스키마): `{rel(FEATURE_SCHEMA)}`.
- model_task_queue(모델 작업 대기열): `{rel(MODEL_TASK_QUEUE)}`.
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
""")
    replace_stage_brief_header()


def write_artifact_registry() -> None:
    artifacts = [
        ("script", Path("stage_pipelines/stage364/materialize_timestamp_context_training_seed_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "ignored_with_manifest"),
        ("training_seed_table", TRAINING_SEED_TABLE, "ignored_with_manifest"),
        ("feature_schema", FEATURE_SCHEMA, "ignored_with_manifest"),
        ("seed_metrics", SEED_METRICS, "ignored_with_manifest"),
        ("month_pressure", MONTH_PRESSURE, "ignored_with_manifest"),
        ("model_task_queue", MODEL_TASK_QUEUE, "ignored_with_manifest"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        rows.append({
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) and Path(path).is_file() else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}__{artifact_type}",
            "notes": f"Stage364D timestamp context training seed artifact(364D 시점 문맥 학습 씨앗 산출물); availability={availability}",
            "artifact_path": rel(path),
        })
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows, extend_header=False)


def refresh_gates_and_final() -> None:
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    final = read_json(FINAL_DECISION)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    final["required_gate_coverage_audit"] = rel(GATE_AUDIT)
    write_json(FINAL_DECISION, final)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("Missing required Stage364D inputs: " + ", ".join(missing))
    final = read_json(SOURCE_REVIEW_FINAL)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"Stage364C final_decision next_run_id mismatch: {final.get('next_run_id')}")
    if final.get("result_judgment") != "positive_scout_reviewed_training_seed_only_no_selection":
        raise RuntimeError("Stage364D expects Stage364C training-seed-only judgment")
    if not source_gate_passed():
        raise RuntimeError("Stage364C source gate audit is not fully passed")


def main() -> None:
    validate_inputs()
    frame, _ = load_seed_frame()
    metric_rows = seed_metrics(frame)
    pressure_rows = month_pressure_rows(frame)
    task_rows = task_queue_rows(metric_rows, pressure_rows)
    write_run_artifacts(frame, metric_rows, pressure_rows, task_rows)
    write_reports(metric_rows, task_rows)
    write_workspace_and_notes()
    write_registries()
    refresh_gates_and_final()
    write_reports(metric_rows, task_rows)
    write_workspace_and_notes()
    write_registries()
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

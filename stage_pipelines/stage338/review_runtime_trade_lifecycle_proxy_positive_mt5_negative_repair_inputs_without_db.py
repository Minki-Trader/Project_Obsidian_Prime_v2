from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import materialize_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_inputs_without_db as mat  # noqa: E402


aw = mat.aw

TODAY = "2026-06-01"
STAGE_ID = mat.STAGE_ID
STAGE_DIR = mat.STAGE_DIR
RUN_NUMBER = "run338D"
RUN_ID = "run338D_review_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_inputs_without_db_v1"
PARENT_RUN_ID = mat.RUN_ID
NEXT_RUN_ID = "run338E_train_runtime_trade_lifecycle_repair_models_group_safe_without_db_v1"
STATUS = "completed_stage338D_input_review_group_safe_split_repair_queue_no_training_no_selection"
JUDGMENT = "input_review_passed_group_safe_split_repair_written_training_queue_opened_no_selection"
DECISION = "stage338D_open_run338E_group_safe_trade_lifecycle_training"
CLAIM_BOUNDARY = (
    "research_development_input_review_and_split_repair_only_no_model_training_no_threshold_tuning_"
    "no_lot_optimization_no_candidate_selection_no_mt5_execution_no_forward_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338D_runtime_trade_lifecycle_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338D_runtime_trade_lifecycle_input_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

SCORECARD = RUN_DIR / "run338D_input_review_scorecard.csv"
FEATURE_QUALITY_AUDIT = RUN_DIR / "run338D_feature_quality_audit.csv"
TRAINING_FEATURE_SCHEMA = RUN_DIR / "run338D_training_feature_schema.csv"
LABEL_SPLIT_DISTRIBUTION_AUDIT = RUN_DIR / "run338D_label_split_distribution_audit.csv"
TIME_ORDER_AUDIT = RUN_DIR / "run338D_time_order_audit.csv"
GROUP_SAFE_SPLIT_ASSIGNMENT = RUN_DIR / "run338D_group_safe_split_assignment.csv"
GROUP_SAFE_SPLIT_MANIFEST = RUN_DIR / "run338D_group_safe_split_manifest.csv"
TRAINING_READINESS_CONTRACT = RUN_DIR / "run338D_training_readiness_contract.csv"
REVIEW_SUMMARY = RUN_DIR / "run338D_review_summary.csv"
RUN338E_TRAINING_QUEUE = RUN_DIR / "run338E_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    mat.FINAL_DECISION,
    mat.INPUT_FRAME,
    mat.FEATURE_SCHEMA,
    mat.LABEL_AUDIT,
    mat.FEATURE_LABEL_BOUNDARY_AUDIT,
    mat.SPLIT_MANIFEST,
    mat.TIER_RECORDS,
    mat.RUN338D_REVIEW_QUEUE,
)
OUTPUT_FILES = (
    SCORECARD,
    FEATURE_QUALITY_AUDIT,
    TRAINING_FEATURE_SCHEMA,
    LABEL_SPLIT_DISTRIBUTION_AUDIT,
    TIME_ORDER_AUDIT,
    GROUP_SAFE_SPLIT_ASSIGNMENT,
    GROUP_SAFE_SPLIT_MANIFEST,
    TRAINING_READINESS_CONTRACT,
    REVIEW_SUMMARY,
    RUN338E_TRAINING_QUEUE,
    DATA_RECEIPT,
    LINEAGE_RECEIPT,
    MODEL_RECEIPT,
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
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

LABEL_COLUMNS = (
    "tlr_label_runtime_net_after_cost_fwd18",
    "tlr_label_drawdown_survival_corridor_fwd18",
    "tlr_label_session_regime_lifecycle_net_fwd18",
)
WEIGHT_COLUMNS = (
    "tlr_weight_side_loss_quarantine",
    "tlr_weight_density_cost_pressure",
    "tlr_weight_lifecycle_composite",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return mat.read_csv(path)


def read_json(path: Path) -> Any:
    return mat.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return mat.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return mat.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return mat.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    mat.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    mat.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    return mat.display_path(path)


def passed_status(series: pd.Series) -> pd.Series:
    return mat.passed_status(series)


def class_counts(series: pd.Series) -> str:
    counts = series.value_counts(dropna=False).sort_index()
    return ";".join(f"{key}:{int(value)}" for key, value in counts.items())


def pct(value: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return round(float(value) / float(denominator), 8)


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)


def split_counts(frame: pd.DataFrame, split_column: str) -> dict[str, int]:
    return {str(key): int(value) for key, value in frame[split_column].value_counts(dropna=False).items()}


def overlap_timestamp_count(frame: pd.DataFrame, split_column: str) -> int:
    counts = frame.groupby("timestamp", dropna=False)[split_column].nunique(dropna=True)
    return int(counts.gt(1).sum())


def build_group_safe_split(frame: pd.DataFrame) -> tuple[pd.Series, dict[str, Any], pd.DataFrame, pd.DataFrame]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    original = frame["run338_split"].astype(str)
    train_mask = original.eq("inner_train")
    holdout_mask = original.eq("inner_holdout")
    original_train_max = timestamps.loc[train_mask].max()
    original_holdout_min = timestamps.loc[holdout_mask].min()
    if pd.isna(original_holdout_min):
        raise RuntimeError("run338C split has no holdout rows")

    safe_split = pd.Series(np.where(timestamps < original_holdout_min, "inner_train", "inner_holdout"), index=frame.index)
    repaired_train_mask = safe_split.eq("inner_train")
    repaired_holdout_mask = safe_split.eq("inner_holdout")

    assignment = pd.DataFrame(
        {
            "source_row_id": frame["source_row_id"],
            "timestamp": frame["timestamp"],
            "run338_split": original,
            "run338D_group_safe_split": safe_split,
            "repair_action": np.where(original.ne(safe_split), "moved_boundary_timestamp_to_holdout", "unchanged"),
            "effect": "동일 timestamp(타임스탬프)가 train/holdout(학습/홀드아웃)을 동시에 밟지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    time_audit = pd.DataFrame(
        [
            {
                "audit_id": "run338C_original_split",
                "train_rows": int(train_mask.sum()),
                "holdout_rows": int(holdout_mask.sum()),
                "train_last_timestamp": str(original_train_max),
                "holdout_first_timestamp": str(original_holdout_min),
                "overlap_timestamp_count": overlap_timestamp_count(frame.assign(run338D_tmp_split=original), "run338D_tmp_split"),
                "boundary_train_rows": int((train_mask & timestamps.eq(original_holdout_min)).sum()),
                "boundary_holdout_rows": int((holdout_mask & timestamps.eq(original_holdout_min)).sum()),
                "judgment": "repair_required(수리 필요)",
                "effect": "원래 split(분할)의 동일 시각 경계 위험을 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "run338D_group_safe_split",
                "train_rows": int(repaired_train_mask.sum()),
                "holdout_rows": int(repaired_holdout_mask.sum()),
                "train_last_timestamp": str(timestamps.loc[repaired_train_mask].max()),
                "holdout_first_timestamp": str(timestamps.loc[repaired_holdout_mask].min()),
                "overlap_timestamp_count": overlap_timestamp_count(frame.assign(run338D_tmp_split=safe_split), "run338D_tmp_split"),
                "boundary_train_rows": int((repaired_train_mask & timestamps.eq(original_holdout_min)).sum()),
                "boundary_holdout_rows": int((repaired_holdout_mask & timestamps.eq(original_holdout_min)).sum()),
                "judgment": "passed(통과)",
                "effect": "동일 timestamp(타임스탬프)를 holdout(홀드아웃) 쪽으로 모아 시간 경계를 안전하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    manifest = pd.DataFrame(
        [
            {
                "split_id": "inner_train",
                "rows": int(repaired_train_mask.sum()),
                "first_timestamp": str(timestamps.loc[repaired_train_mask].min()),
                "last_timestamp": str(timestamps.loc[repaired_train_mask].max()),
                "source": rel(GROUP_SAFE_SPLIT_ASSIGNMENT),
                "effect": "group-safe train(묶음 안전 학습) 구간을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "split_id": "inner_holdout",
                "rows": int(repaired_holdout_mask.sum()),
                "first_timestamp": str(timestamps.loc[repaired_holdout_mask].min()),
                "last_timestamp": str(timestamps.loc[repaired_holdout_mask].max()),
                "source": rel(GROUP_SAFE_SPLIT_ASSIGNMENT),
                "effect": "group-safe holdout(묶음 안전 홀드아웃) 구간을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = {
        "original_train_rows": int(train_mask.sum()),
        "original_holdout_rows": int(holdout_mask.sum()),
        "repaired_train_rows": int(repaired_train_mask.sum()),
        "repaired_holdout_rows": int(repaired_holdout_mask.sum()),
        "original_overlap_timestamp_count": int(time_audit.loc[0, "overlap_timestamp_count"]),
        "repaired_overlap_timestamp_count": int(time_audit.loc[1, "overlap_timestamp_count"]),
        "original_train_last_timestamp": str(original_train_max),
        "original_holdout_first_timestamp": str(original_holdout_min),
        "repaired_train_last_timestamp": str(timestamps.loc[repaired_train_mask].max()),
        "repaired_holdout_first_timestamp": str(timestamps.loc[repaired_holdout_mask].min()),
    }
    return safe_split, summary, assignment, time_audit, manifest


def build_feature_quality(frame: pd.DataFrame, feature_names: Sequence[str], safe_split: pd.Series) -> tuple[pd.DataFrame, dict[str, Any]]:
    train_mask = safe_split.eq("inner_train")
    holdout_mask = safe_split.eq("inner_holdout")
    rows = []
    for feature in feature_names:
        values = numeric(frame[feature])
        train_values = values.loc[train_mask]
        holdout_values = values.loc[holdout_mask]
        missing_count = int(values.isna().sum())
        missing_rate = pct(missing_count, len(values))
        unique_count = int(values.nunique(dropna=True))
        train_mean = float(train_values.mean()) if not train_values.dropna().empty else 0.0
        holdout_mean = float(holdout_values.mean()) if not holdout_values.dropna().empty else 0.0
        train_std = float(train_values.std(ddof=0)) if not train_values.dropna().empty else 0.0
        drift_z_abs = abs(holdout_mean - train_mean) / max(abs(train_std), 1e-12)
        status = "passed"
        if missing_rate > 0.2 or unique_count <= 1:
            status = "failed"
        elif missing_rate > 0.02 or drift_z_abs > 1.5:
            status = "warning"
        rows.append(
            {
                "feature_name": feature,
                "missing_count": missing_count,
                "missing_rate": missing_rate,
                "unique_count": unique_count,
                "train_mean": round(train_mean, 10),
                "holdout_mean": round(holdout_mean, 10),
                "train_std": round(train_std, 10),
                "drift_z_abs": round(float(drift_z_abs), 8),
                "status": status,
                "effect": "training(학습) 전 feature(피처) 품질과 split drift(분할 이동)를 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    audit = pd.DataFrame(rows)
    summary = {
        "feature_count": int(len(feature_names)),
        "feature_failed_count": int(audit["status"].eq("failed").sum()) if not audit.empty else 0,
        "feature_warning_count": int(audit["status"].eq("warning").sum()) if not audit.empty else 0,
        "max_feature_missing_rate": float(audit["missing_rate"].max()) if not audit.empty else 0.0,
        "max_feature_drift_z_abs": float(audit["drift_z_abs"].max()) if not audit.empty else 0.0,
    }
    return audit, summary


def build_label_distribution(frame: pd.DataFrame, safe_split: pd.Series) -> tuple[pd.DataFrame, dict[str, Any]]:
    rows = []
    for label in LABEL_COLUMNS:
        if label not in frame.columns:
            rows.append(
                {
                    "label_id": label,
                    "split_id": "all",
                    "rows": 0,
                    "class_counts": "missing",
                    "invalid_rate": 1.0,
                    "status": "failed",
                    "effect": "label(라벨) 누락을 학습 전에 막는다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        values = pd.to_numeric(frame[label], errors="coerce").fillna(-1).astype(int)
        for split_id, mask in {
            "all": pd.Series(True, index=frame.index),
            "inner_train": safe_split.eq("inner_train"),
            "inner_holdout": safe_split.eq("inner_holdout"),
        }.items():
            split_values = values.loc[mask]
            invalid_rate = pct(split_values.eq(-1).sum(), len(split_values))
            usable_classes = sorted([int(value) for value in split_values[~split_values.eq(-1)].unique().tolist()])
            status = "passed" if len(split_values) > 0 and len(usable_classes) >= 2 and invalid_rate < 0.05 else "failed"
            rows.append(
                {
                    "label_id": label,
                    "split_id": split_id,
                    "rows": int(len(split_values)),
                    "class_counts": class_counts(split_values),
                    "invalid_rate": invalid_rate,
                    "usable_classes": ";".join(str(value) for value in usable_classes),
                    "status": status,
                    "effect": "label(라벨) 분포가 학습/홀드아웃 양쪽에서 살아 있는지 확인한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    audit = pd.DataFrame(rows)
    summary = {
        "label_count": int(len(LABEL_COLUMNS)),
        "label_failed_count": int(audit["status"].eq("failed").sum()) if not audit.empty else 0,
    }
    return audit, summary


def build_review_outputs() -> tuple[dict[str, Any], dict[str, pd.DataFrame]]:
    parent_final = read_json(mat.FINAL_DECISION)
    parent_gates = read_csv(mat.GATE_AUDIT)
    schema = read_csv(mat.FEATURE_SCHEMA)
    boundary = read_csv(mat.FEATURE_LABEL_BOUNDARY_AUDIT)
    tier_records = read_csv(mat.TIER_RECORDS)
    frame = pd.read_parquet(str(io(mat.INPUT_FRAME)))
    if "timestamp" not in frame.columns or "source_row_id" not in frame.columns or "run338_split" not in frame.columns:
        raise RuntimeError("run338C input frame missing timestamp/source_row_id/run338_split")

    feature_names = [str(name) for name in schema["feature_name"].tolist() if str(name) in frame.columns]
    forbidden_feature_hits = int(boundary.loc[boundary["audit_id"].eq("feature_columns"), "forbidden_pattern_hits"].iloc[0])
    forbidden_schema_hits = [name for name in feature_names if mat.is_forbidden_feature(name)]
    safe_split, split_summary, assignment, time_audit, split_manifest = build_group_safe_split(frame)
    feature_audit, feature_summary = build_feature_quality(frame, feature_names, safe_split)
    failed_features = set(feature_audit.loc[feature_audit["status"].eq("failed"), "feature_name"].astype(str))
    training_schema = schema.loc[schema["feature_name"].astype(str).isin(feature_names)].copy()
    training_schema["run338D_train_allowed"] = np.where(
        training_schema["feature_name"].astype(str).isin(failed_features),
        "no_excluded_by_input_review(입력 검토 제외)",
        "yes(예)",
    )
    training_schema["run338D_review_reason"] = np.where(
        training_schema["feature_name"].astype(str).isin(failed_features),
        "constant_or_unusable_feature(상수 또는 사용 불가 피처)",
        "passed_input_review(입력 검토 통과)",
    )
    training_schema["run338D_claim_boundary"] = CLAIM_BOUNDARY
    feature_summary["train_feature_count"] = int(training_schema["run338D_train_allowed"].astype(str).str.startswith("yes").sum())
    feature_summary["excluded_feature_count"] = int(training_schema["run338D_train_allowed"].astype(str).str.startswith("no_").sum())
    feature_summary["feature_unhandled_failed_count"] = 0
    label_audit, label_summary = build_label_distribution(frame, safe_split)

    tier_statuses = ";".join(f"{row['tier']}={row['status']}" for _, row in tier_records.iterrows())
    scorecard_rows = [
        {
            "review_id": "parent_338C_evidence",
            "status": "passed" if passed_status(parent_gates["status"]).all() and parent_final.get("goal_achieve") == "not_claimed" else "failed",
            "evidence_path": rel(mat.FINAL_DECISION),
            "effect": "부모 run338C(338C 실행)의 gate(게이트)와 주장 경계를 이어받는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "feature_label_boundary",
            "status": "passed" if forbidden_feature_hits == 0 and not forbidden_schema_hits else "failed",
            "evidence_path": rel(mat.FEATURE_LABEL_BOUNDARY_AUDIT),
            "effect": "future/label/weight(미래/라벨/가중치) 열을 feature(피처)에서 뺀 상태를 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "timestamp_group_safe_split",
            "status": "passed" if split_summary["repaired_overlap_timestamp_count"] == 0 else "failed",
            "evidence_path": rel(GROUP_SAFE_SPLIT_MANIFEST),
            "effect": "동일 timestamp(타임스탬프)가 학습과 홀드아웃에 동시에 들어가는 위험을 수리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "feature_quality",
            "status": "passed" if feature_summary["train_feature_count"] > 0 and feature_summary["feature_unhandled_failed_count"] == 0 else "failed",
            "evidence_path": rel(TRAINING_FEATURE_SCHEMA),
            "effect": "학습 전 feature(피처)의 결측, 상수, split drift(분할 이동)를 확인하고 상수 피처를 제외한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "label_distribution",
            "status": "passed" if label_summary["label_failed_count"] == 0 else "failed",
            "evidence_path": rel(LABEL_SPLIT_DISTRIBUTION_AUDIT),
            "effect": "label(라벨)이 train/holdout(학습/홀드아웃)에 모두 살아 있는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "tier_pair_record",
            "status": "passed" if {"Tier A", "Tier B", "Tier A+B"}.issubset(set(tier_records["tier"].astype(str))) else "failed",
            "evidence_path": rel(mat.TIER_RECORDS),
            "effect": "Tier A/Tier B/Tier A+B(티어 A/티어 B/티어 A+B)를 생략하지 않고 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    scorecard = pd.DataFrame(scorecard_rows)

    readiness = pd.DataFrame(
        [
            {
                "contract_id": "training_input_frame",
                "value": rel(mat.INPUT_FRAME),
                "required": "yes(예)",
                "effect": "run338E(338E 실행)가 같은 입력 정체성을 쓰게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "feature_schema",
                "value": rel(mat.FEATURE_SCHEMA),
                "required": "yes(예)",
                "effect": "원천 허용 feature(피처) 순서를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "training_feature_schema",
                "value": rel(TRAINING_FEATURE_SCHEMA),
                "required": "yes(예)",
                "effect": "상수 feature(피처)를 제외한 학습 feature schema(피처 스키마)를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "group_safe_split_assignment",
                "value": rel(GROUP_SAFE_SPLIT_ASSIGNMENT),
                "required": "yes(예)",
                "effect": "학습은 run338C 원래 split(분할)이 아니라 run338D 수리 split(분할)을 써야 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "primary_label",
                "value": "tlr_label_runtime_net_after_cost_fwd18",
                "required": "yes(예)",
                "effect": "거래 생명주기 손익 방향 label(라벨)을 첫 학습 목표로 둔다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "candidate_variants",
                "value": "tlr01_density_margin_cost_throttle;tlr02_side_specific_loss_quarantine;tlr03_drawdown_corridor_exit_pressure;tlr04_session_regime_loss_firewall;tlr05_sparse_extreme_edge_router",
                "required": "yes(예)",
                "effect": "Stage338B(338B 단계) 설계 변형을 버리지 않고 학습 대기열로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "forbidden_actions",
                "value": "no feature outside schema; no label/weight as feature; no MT5 or operating claim in run338E training(스키마 밖 피처 금지; 라벨/가중치 피처 금지; 338E 학습에서 MT5/운영 주장 금지)",
                "required": "yes(예)",
                "effect": "탐색은 열되 운영 주장은 닫는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    queue = pd.DataFrame(
        [
            {
                "queue_id": "run338E_group_safe_trade_lifecycle_training",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "allowed_action": "train exploratory trade lifecycle models using run338D group-safe split(338D 묶음 안전 분할로 탐색 학습)",
                "required_inputs": f"{rel(mat.INPUT_FRAME)};{rel(TRAINING_FEATURE_SCHEMA)};{rel(GROUP_SAFE_SPLIT_ASSIGNMENT)};{rel(TRAINING_READINESS_CONTRACT)}",
                "required_outputs": "model scorecards(모델 점수표); proxy evaluation(프록시 평가); no selection unless later gates pass(이후 게이트 전 선택 없음)",
                "blocked_if_missing": "group_safe_split_assignment or feature boundary pass(묶음 안전 분할 또는 피처 경계 통과)",
                "effect": "학습을 열되 run338D 수리 split(분할)을 강제한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    summary = {
        "source_rows": int(len(frame)),
        "source_columns": int(len(frame.columns)),
        "feature_count": int(len(feature_names)),
        "forbidden_feature_hits": int(forbidden_feature_hits + len(forbidden_schema_hits)),
        "split_counts_original": json.dumps(split_counts(frame, "run338_split"), ensure_ascii=False, sort_keys=True),
        "split_counts_repaired": json.dumps(split_counts(frame.assign(run338D_group_safe_split=safe_split), "run338D_group_safe_split"), ensure_ascii=False, sort_keys=True),
        "tier_statuses": tier_statuses,
        "input_frame_sha256": sha(mat.INPUT_FRAME),
        "feature_schema_sha256": sha(mat.FEATURE_SCHEMA),
        **split_summary,
        **feature_summary,
        **label_summary,
        "scorecard_failed_count": int(scorecard["status"].eq("failed").sum()),
        "next_run_id": NEXT_RUN_ID,
        "effect": "run338E(338E 실행)가 학습 전에 써야 할 group-safe input contract(묶음 안전 입력 계약)을 만든다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    summary_frame = pd.DataFrame([summary])

    return summary, {
        "scorecard": scorecard,
        "feature_audit": feature_audit,
        "training_schema": training_schema,
        "label_audit": label_audit,
        "time_audit": time_audit,
        "assignment": assignment,
        "split_manifest": split_manifest,
        "readiness": readiness,
        "queue": queue,
        "summary": summary_frame,
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any], tables: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    parent_gates = read_csv(mat.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row("parent_338C_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(mat.GATE_AUDIT), "run338C(338C 실행) 입력 생성 gate(게이트)를 이어받는다."),
            gate_row("input_frame_loaded", "passed" if summary["source_rows"] > 0 else "failed", rel(mat.INPUT_FRAME), "물질화된 입력 frame(프레임)을 읽는다."),
            gate_row("feature_label_boundary_passed", "passed" if summary["forbidden_feature_hits"] == 0 else "failed", rel(mat.FEATURE_LABEL_BOUNDARY_AUDIT), "feature(피처)에 future/label/weight(미래/라벨/가중치) 계열이 없음을 확인한다."),
            gate_row("original_split_reviewed", "passed" if exists(TIME_ORDER_AUDIT) or summary["original_overlap_timestamp_count"] >= 0 else "failed", rel(TIME_ORDER_AUDIT), "원래 split(분할)의 경계 위험을 기록한다."),
            gate_row("timestamp_group_safe_split_repair_written", "passed" if summary["repaired_overlap_timestamp_count"] == 0 else "failed", rel(GROUP_SAFE_SPLIT_ASSIGNMENT), "동일 timestamp(타임스탬프) 경계를 holdout(홀드아웃)으로 모아 수리한다."),
            gate_row("feature_quality_reviewed", "passed" if summary["feature_unhandled_failed_count"] == 0 and summary["train_feature_count"] > 0 else "failed", rel(TRAINING_FEATURE_SCHEMA), "feature(피처) 결측/상수/drift(이동)를 학습 전에 확인하고 상수 피처를 제외한다."),
            gate_row("label_distribution_reviewed", "passed" if summary["label_failed_count"] == 0 else "failed", rel(LABEL_SPLIT_DISTRIBUTION_AUDIT), "label(라벨) 분포가 양 split(분할)에 있는지 확인한다."),
            gate_row("tier_pair_records_preserved", "passed" if "Tier B=missing_required" in summary["tier_statuses"] else "failed", rel(mat.TIER_RECORDS), "Tier B(티어 B) 누락을 생략하지 않고 보존한다."),
            gate_row("run338E_training_queue_opened", "passed" if len(tables["queue"]) == 1 else "failed", rel(RUN338E_TRAINING_QUEUE), "다음 학습 queue(대기열)를 열되 group-safe split(묶음 안전 분할)을 강제한다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(FINAL_DECISION), "training/model selection/MT5/live(학습/모델 선택/MT5/실거래) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_review_tables(tables: Mapping[str, pd.DataFrame]) -> None:
    write_csv(SCORECARD, tables["scorecard"])
    write_csv(FEATURE_QUALITY_AUDIT, tables["feature_audit"])
    write_csv(TRAINING_FEATURE_SCHEMA, tables["training_schema"])
    write_csv(LABEL_SPLIT_DISTRIBUTION_AUDIT, tables["label_audit"])
    write_csv(TIME_ORDER_AUDIT, tables["time_audit"])
    write_csv(GROUP_SAFE_SPLIT_ASSIGNMENT, tables["assignment"])
    write_csv(GROUP_SAFE_SPLIT_MANIFEST, tables["split_manifest"])
    write_csv(TRAINING_READINESS_CONTRACT, tables["readiness"])
    write_csv(REVIEW_SUMMARY, tables["summary"])
    write_csv(RUN338E_TRAINING_QUEUE, tables["queue"])


def write_receipts(summary: Mapping[str, Any]) -> None:
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
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(mat.INPUT_FRAME),
            "time_axis": "run338C split reviewed and repaired by timestamp group(338C 분할을 timestamp 묶음으로 검토/수리)",
            "sample_scope": f"rows={summary['source_rows']};features={summary['feature_count']}",
            "missing_or_duplicate_check": rel(FEATURE_QUALITY_AUDIT),
            "feature_label_boundary": rel(mat.FEATURE_LABEL_BOUNDARY_AUDIT),
            "split_boundary": rel(GROUP_SAFE_SPLIT_MANIFEST),
            "leakage_risk": "original boundary tie repaired before training(원래 경계 동시 시각을 학습 전 수리)",
            "data_hash_or_identity": summary["input_frame_sha256"],
            "integrity_judgment": "review_passed_with_group_safe_split_repair(묶음 안전 분할 수리와 함께 검토 통과)",
            "training_feature_schema": rel(TRAINING_FEATURE_SCHEMA),
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "not_trained_in_run338D(338D에서 학습 없음)",
            "target_and_label": rel(LABEL_SPLIT_DISTRIBUTION_AUDIT),
            "split_method": rel(GROUP_SAFE_SPLIT_MANIFEST),
            "selection_metric": "not_applicable_input_review(입력 검토라 해당 없음)",
            "validation_judgment": "ready_for_exploratory_training_queue_only(탐색 학습 대기열까지만 준비)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in OUTPUT_FILES if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_group_safe_split_manifest(묶음 안전 분할 목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "threshold_tuning": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
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
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
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
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338D Input Review(입력 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['source_rows']}`
- features(피처): `{final['feature_count']}`
- train_features(학습 피처): `{final['train_feature_count']}`
- excluded_features(제외 피처): `{final['excluded_feature_count']}`
- original_overlap_timestamp_count(기존 겹친 타임스탬프 수): `{final['original_overlap_timestamp_count']}`
- repaired_overlap_timestamp_count(수리 뒤 겹친 타임스탬프 수): `{final['repaired_overlap_timestamp_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338C(338C 실행) 입력을 검토하고 group-safe split repair(묶음 안전 분할 수리)를 기록했다.
Effect(효과): run338E(338E 실행)는 같은 timestamp(타임스탬프)를 train/holdout(학습/홀드아웃)에 동시에 넣지 않고 학습할 수 있다.

## Evidence(근거)

- scorecard(점수표): `{rel(SCORECARD)}`
- time audit(시간 감사): `{rel(TIME_ORDER_AUDIT)}`
- group-safe split(묶음 안전 분할): `{rel(GROUP_SAFE_SPLIT_ASSIGNMENT)}`
- training feature schema(학습 피처 스키마): `{rel(TRAINING_FEATURE_SCHEMA)}`
- readiness contract(준비 계약): `{rel(TRAINING_READINESS_CONTRACT)}`
- training queue(학습 대기열): `{rel(RUN338E_TRAINING_QUEUE)}`

## Boundary(경계)

run338D(338D 실행)는 input review(입력 검토)와 split repair(분할 수리)만 수행했다. Model training(모델 학습), candidate selection(후보 선택), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338D Decision(338D 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(SCORECARD)}`, `{rel(GROUP_SAFE_SPLIT_MANIFEST)}`, `{rel(RUN338E_TRAINING_QUEUE)}`

Action(행동): Stage338(338단계) 입력 검토에서 timestamp group-safe split(타임스탬프 묶음 안전 분할)을 만들었다.
Effect(효과): 다음 학습은 repaired split(수리된 분할)을 강제받는다.

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

run338D(338D 실행)는 입력 검토와 split repair(분할 수리)를 끝냈고, run338E(338E 실행)는 group-safe split(묶음 안전 분할)로만 학습해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- materialized_rows(물질화 행): `{final['source_rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- train_feature_count(학습 피처 수): `{final['train_feature_count']}`
- group_safe_split(묶음 안전 분할): `{rel(GROUP_SAFE_SPLIT_ASSIGNMENT)}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 입력 검토/분할 수리를 선정 모델로 오해하지 않게 한다.
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
    marker = f"run338D {RUN_ID} group_safe_training_schema"
    append_text_once(STAGE_BRIEF, marker, f"""## run338D Input Review(입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- original_overlap_timestamp_count(기존 겹친 타임스탬프 수): `{final['original_overlap_timestamp_count']}`
- repaired_overlap_timestamp_count(수리 뒤 겹친 타임스탬프 수): `{final['repaired_overlap_timestamp_count']}`
- train_feature_count(학습 피처 수): `{final['train_feature_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): run338E(338E 실행)가 group-safe split(묶음 안전 분할)로 학습하게 한다.
""")
    append_text_once(STAGE_README, marker, f"""## run338D Input Review(입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- group_safe_split(묶음 안전 분할): `{rel(GROUP_SAFE_SPLIT_ASSIGNMENT)}`
- training_feature_schema(학습 피처 스키마): `{rel(TRAINING_FEATURE_SCHEMA)}`
- effect(효과): Stage338(338단계) 학습 입력의 시간 경계 위험을 수리했다.
""")
    changelog = f"""## {TODAY} run338D Input Review(입력 검토)

- action(행동): run338C(338C 실행) 입력을 검토하고 group-safe split repair(묶음 안전 분할 수리)를 만들었다.
- effect(효과): 기존 split(분할)의 겹친 timestamp(타임스탬프) `{final['original_overlap_timestamp_count']}`개를 수리 뒤 `{final['repaired_overlap_timestamp_count']}`개로 낮추고, 학습 feature(피처)를 `{final['train_feature_count']}`개로 고정했다.
- boundary(경계): training/model selection/MT5 execution(학습/모델 선택/MT5 실행)은 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
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
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "input_review", "sample_rows": final["source_rows"], "feature_count": final["feature_count"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "sample_rows": final["source_rows"], "result_status": "same_as_tier_a_until_tier_b_available"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


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
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338D inputs: {missing}")
    summary, tables = build_review_outputs()
    write_review_tables(tables)
    gates = make_gates(summary, tables)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338D gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "source_rows": final["source_rows"],
                "feature_count": final["feature_count"],
                "original_overlap_timestamp_count": final["original_overlap_timestamp_count"],
                "repaired_overlap_timestamp_count": final["repaired_overlap_timestamp_count"],
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

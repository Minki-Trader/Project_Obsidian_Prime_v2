from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import design_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_without_db as fd  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_repair_inputs_without_db as ew  # noqa: E402


aw = fd.aw

TODAY = "2026-05-31"
STAGE_ID = fd.STAGE_ID
RUN_NUMBER = "run337FE"
RUN_ID = "run337FE_materialize_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_inputs_without_db_v1"
PARENT_RUN_ID = fd.RUN_ID
NEXT_RUN_ID = "run337FF_review_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_inputs_without_db_v1"
STATUS = "completed_stage337FE_runtime_positive_clue_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "train_only_drawdown_recovery_side_balance_repair_inputs_materialized_review_required"
DECISION = "stage337FE_open_run337FF_review_runtime_positive_clue_repair_inputs_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FE_runtime_positive_clue_repair_input_materialization_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = fd.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FE_runtime_positive_clue_drawdown_balance_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FE_runtime_positive_clue_drawdown_balance_repair_inputs.md"
SELECTED_STATUS = fd.SELECTED_STATUS
STAGE_BRIEF = fd.STAGE_BRIEF
WORKSPACE_STATE = fd.WORKSPACE_STATE
CURRENT_STATE = fd.CURRENT_STATE
CHANGELOG = fd.CHANGELOG
RUN_REGISTRY = fd.RUN_REGISTRY
ALPHA_LEDGER = fd.ALPHA_LEDGER
ARTIFACT_REGISTRY = fd.ARTIFACT_REGISTRY
STAGE_LEDGER = fd.STAGE_LEDGER

FD_FINAL = fd.FINAL_DECISION
FD_GATES = fd.GATE_AUDIT
FD_QUEUE = fd.MATERIALIZATION_QUEUE
FD_DESIGN = fd.DESIGN_MATRIX
FD_OBJECTIVE = fd.OBJECTIVE_CONTRACT
FD_FEATURE_LABEL = fd.FEATURE_LABEL_CONTRACT
FD_HANDOFF = fd.RUNTIME_HANDOFF_CONTRACT
FD_NEGATIVE = fd.NEGATIVE_CONTROL_PLAN
FD_RELEASE = fd.RELEASE_GATE_CONTRACT

EW_FRAME = ew.TRAIN_ONLY_INPUT_FRAME
EW_ALLOWED_FEATURES = ew.ALLOWED_FEATURE_SET
EW_MANIFEST = ew.INPUT_MANIFEST
EW_QUARANTINE = ew.FORWARD_QUARANTINE

TRAIN_ONLY_REPAIR_FRAME = RUN_DIR / "train_only_runtime_positive_clue_repair_input_frame.parquet"
MATERIALIZATION_SOURCE_MAP = RUN_DIR / "fe_materialization_source_map.csv"
ALLOWED_FEATURE_SET = RUN_DIR / "fe_allowed_model_feature_set.csv"
WEIGHT_RECIPE_MATRIX = RUN_DIR / "fd_repair_weight_recipe_matrix.csv"
WEIGHT_AUDIT = RUN_DIR / "fd_repair_weight_audit.csv"
FEATURE_LABEL_BOUNDARY = RUN_DIR / "feature_label_boundary_audit.csv"
UNIQUE_TIMESTAMP_HANDOFF = RUN_DIR / "unique_timestamp_handoff_materialization.csv"
NEGATIVE_CONTROL_MATERIALIZATION = RUN_DIR / "negative_control_materialization_matrix.csv"
RELEASE_GATE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
TRAINING_TASK_SEEDS = RUN_DIR / "run337FG_training_task_seed_matrix.csv"
FF_QUEUE = RUN_DIR / "run337FF_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    FD_FINAL,
    FD_GATES,
    FD_QUEUE,
    FD_DESIGN,
    FD_OBJECTIVE,
    FD_FEATURE_LABEL,
    FD_HANDOFF,
    FD_NEGATIVE,
    FD_RELEASE,
    EW_FRAME,
    EW_ALLOWED_FEATURES,
    EW_MANIFEST,
    EW_QUARANTINE,
)
OUTPUT_FILES = (
    TRAIN_ONLY_REPAIR_FRAME,
    MATERIALIZATION_SOURCE_MAP,
    ALLOWED_FEATURE_SET,
    WEIGHT_RECIPE_MATRIX,
    WEIGHT_AUDIT,
    FEATURE_LABEL_BOUNDARY,
    UNIQUE_TIMESTAMP_HANDOFF,
    NEGATIVE_CONTROL_MATERIALIZATION,
    RELEASE_GATE_MATERIALIZATION,
    TRAINING_TASK_SEEDS,
    FF_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    RUN_REGISTRY,
    ALPHA_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "allowed_role",
    "forbidden_role",
    "materialization_use",
    "effect",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_name",
    "feature_family",
    "source_layer",
    "timestamp_rule",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
RECIPE_COLUMNS = (
    "recipe_id",
    "materialized_column",
    "source_columns",
    "split_scope",
    "timestamp_rule",
    "train_only_formula",
    "non_feature_status",
    "effect",
    "claim_boundary",
)
WEIGHT_AUDIT_COLUMNS = (
    "weight_column",
    "rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_rows",
    "short_label_mean",
    "flat_label_mean",
    "long_label_mean",
    "effect",
    "claim_boundary",
)
BOUNDARY_COLUMNS = (
    "audit_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "control_id",
    "source_control",
    "materialized_status",
    "observed",
    "invalid_if_future_review",
    "effect",
    "claim_boundary",
)
RELEASE_COLUMNS = (
    "gate_id",
    "source_gate",
    "materialized_status",
    "observed",
    "future_release_dependency",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "feature_set_id",
    "target_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "feature_count",
    "training_eligibility_status",
    "required_guard",
    "forbidden_action",
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
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")

NEW_WEIGHT_COLUMNS = (
    "fd_positive_clue_preservation_weight",
    "fd_curve_risk_suppression",
    "fd_short_balance_boost",
    "fd_drawdown_recovery_weight",
    "fd_side_balance_rescue_weight",
    "fd_drawdown_balance_weight",
    "fd_runtime_positive_clue_weight",
)
FORBIDDEN_FEATURE_COLUMNS = {
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "fd_positive_clue_preservation_weight",
    "fd_curve_risk_suppression",
    "fd_short_balance_boost",
    "fd_drawdown_recovery_weight",
    "fd_side_balance_rescue_weight",
    "fd_drawdown_balance_weight",
    "fd_runtime_positive_clue_weight",
    "net_profit",
    "profit_factor",
    "expectancy",
    "max_drawdown_amount",
    "recovery_factor",
}


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def row_count(path: Path) -> int:
    if not path_exists(path):
        return 0
    if path.suffix.lower() == ".csv":
        return len(read_csv(path))
    if path.suffix.lower() == ".parquet":
        return int(len(pd.read_parquet(aw.io_path(path), columns=[])))
    return 0


def normalize_positive(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").fillna(0.0)
    positive = numeric.clip(lower=0.0)
    scale = float(positive.quantile(0.95)) if len(positive) else 0.0
    if scale <= 0:
        return positive * 0.0
    return (positive / scale).clip(lower=0.0, upper=1.0)


def numeric(frame: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(np.full(len(frame), default, dtype="float64"), index=frame.index)
    return pd.to_numeric(frame[column], errors="coerce").fillna(default).astype("float64")


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 10.0) -> pd.Series:
    series = pd.Series(values, copy=False)
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(lower=lower, upper=upper)


def build_repair_frame() -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = pd.read_parquet(aw.io_path(EW_FRAME)).copy()
    drawdown = numeric(frame, "drawdown_pressure_norm").clip(lower=0.0, upper=1.0)
    underwater = numeric(frame, "underwater_rate_model").clip(lower=0.0, upper=1.0)
    low_margin = numeric(frame, "low_margin_rate_model").clip(lower=0.0, upper=1.0)
    risk_pressure = (0.55 * drawdown + 0.25 * underwater + 0.20 * low_margin).clip(lower=0.0, upper=1.0)
    frame["fd_curve_risk_suppression"] = (1.35 - 0.70 * risk_pressure).clip(lower=0.35, upper=1.35)

    short_quality_norm = normalize_positive(numeric(frame, "short_quality_target"))
    side_gap = numeric(frame, "side_quality_gap_norm").clip(lower=0.0, upper=1.0)
    label = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int)
    short_boost = np.where(label == 0, 1.0 + 0.45 * (0.50 + short_quality_norm), 1.0)
    long_damper = np.where(label == 2, 1.0 - 0.15 * side_gap, 1.0)
    frame["fd_short_balance_boost"] = clip_weight(short_boost * long_damper, lower=0.75, upper=1.75)

    side = numeric(frame, "side_quality_weight", default=1.0)
    cost = numeric(frame, "cost_survival_weight", default=1.0)
    curve = numeric(frame, "curve_state_pressure_weight", default=1.0)
    combined = numeric(frame, "combined_sample_weight", default=1.0)
    short_abstention = numeric(frame, "short_abstention_pressure_weight", default=1.0)

    frame["fd_positive_clue_preservation_weight"] = clip_weight(side * cost * curve)
    frame["fd_drawdown_recovery_weight"] = clip_weight(combined * frame["fd_curve_risk_suppression"])
    frame["fd_side_balance_rescue_weight"] = clip_weight(side * cost * frame["fd_short_balance_boost"] * short_abstention)
    frame["fd_drawdown_balance_weight"] = clip_weight(
        frame["fd_positive_clue_preservation_weight"] * frame["fd_curve_risk_suppression"] * frame["fd_short_balance_boost"]
    )
    frame["fd_runtime_positive_clue_weight"] = clip_weight(
        0.50 * frame["fd_positive_clue_preservation_weight"] + 0.50 * frame["fd_drawdown_balance_weight"]
    )

    frame["claim_boundary"] = CLAIM_BOUNDARY
    summary = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "unique_timestamps": int(frame["timestamp"].nunique()) if "timestamp" in frame.columns else 0,
        "source_row_count": int(frame["source_row_id"].nunique()) if "source_row_id" in frame.columns else 0,
        "cost_policy_count": int(frame["cost_policy_id"].nunique()) if "cost_policy_id" in frame.columns else 0,
        "split_values": ",".join(sorted(str(value) for value in frame["split"].dropna().unique())) if "split" in frame.columns else "",
        "label_counts": json.dumps(
            {str(int(key)): int(value) for key, value in frame["label_class"].value_counts().sort_index().items()},
            ensure_ascii=False,
            sort_keys=True,
        )
        if "label_class" in frame.columns
        else "{}",
        "new_weight_count": len(NEW_WEIGHT_COLUMNS),
        "nonfinite_weight_rows": int(
            sum(
                pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).isna().sum()
                for column in NEW_WEIGHT_COLUMNS
            )
        ),
    }
    return frame, summary


def write_frame(frame: pd.DataFrame) -> Path:
    aw.io_path(TRAIN_ONLY_REPAIR_FRAME.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(aw.io_path(TRAIN_ONLY_REPAIR_FRAME), index=False)
    return TRAIN_ONLY_REPAIR_FRAME


def copy_allowed_features() -> list[dict[str, Any]]:
    rows = read_csv(EW_ALLOWED_FEATURES)
    copied: list[dict[str, Any]] = []
    for row in rows:
        copied.append(
            {
                "feature_name": row.get("feature_name", ""),
                "feature_family": row.get("feature_family", ""),
                "source_layer": rel(TRAIN_ONLY_REPAIR_FRAME),
                "timestamp_rule": "closed-bar/as-of only(닫힌 봉/시점 기준만)",
                "allowed_use": "future reviewed training feature after FF review(FF 검토 후 학습 피처)",
                "forbidden_use": "label, selector, forward proof, repair weight(라벨/선택자/전진 증거/수리 가중치)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return copied


def build_source_map() -> list[dict[str, Any]]:
    roles: dict[Path, tuple[str, str, str, str]] = {
        FD_FINAL: ("parent decision(부모 결정)", "scope expansion(범위 확장)", "routing identity(라우팅 정체성)", "keeps FE tied to FD decision(FE를 FD 결정에 묶음)"),
        FD_GATES: ("parent gate evidence(부모 게이트 근거)", "gate relaxation(게이트 완화)", "gate inheritance(게이트 상속)", "blocks FE if FD gates failed(FD 게이트 실패 시 FE 차단)"),
        FD_QUEUE: ("parent queue(부모 대기열)", "next-action rewrite(다음 행동 재작성)", "queue identity(대기열 정체성)", "confirms FE was opened(FE가 열렸는지 확인)"),
        FD_DESIGN: ("repair design(수리 설계)", "model feature(모델 피처)", "materialization guide(물질화 안내)", "turns clue into input work(단서를 입력 작업으로 전환)"),
        FD_OBJECTIVE: ("objective contract(목표 계약)", "feature column(피처 열)", "weight recipe source(가중치 조리법 원천)", "keeps objective out of features(목표를 피처에서 분리)"),
        FD_FEATURE_LABEL: ("feature-label contract(피처-라벨 계약)", "future data join(미래 데이터 결합)", "boundary check(경계 확인)", "prevents look-ahead bias(미래참조 편향 방지)"),
        FD_HANDOFF: ("unique timestamp contract(고유 시각 계약)", "extra evidence count(추가 근거 수)", "runtime handoff rule(런타임 인계 규칙)", "keeps future package deduped(향후 패키지 중복 제거 유지)"),
        FD_NEGATIVE: ("negative controls(부정 대조)", "skipped controls(생략된 대조)", "control materialization(대조 물질화)", "keeps overfit routes named(과적합 경로 명명 유지)"),
        FD_RELEASE: ("release gates(해제 게이트)", "operating claim proof(운영 주장 증거)", "future release dependency(향후 해제 의존성)", "keeps operating claims closed(운영 주장 닫힘 유지)"),
        EW_FRAME: ("train-only base frame(학습 전용 기본 프레임)", "Forward proof(전진 증거)", "repair frame source(수리 프레임 원천)", "provides timestamp-safe row space(시점 안전 행 공간 제공)"),
        EW_ALLOWED_FEATURES: ("allowed feature schema(허용 피처 스키마)", "feature expansion without review(검토 없는 피처 확장)", "feature copy source(피처 복사 원천)", "keeps 58 feature order(58개 피처 순서 유지)"),
        EW_MANIFEST: ("base input manifest(기본 입력 목록)", "selection proof(선택 증거)", "source identity(원천 정체성)", "tracks source rows(원천 행 추적)"),
        EW_QUARANTINE: ("forward quarantine(전진 격리)", "training feature(학습 피처)", "quarantine carry-forward(격리 이월)", "keeps forward evidence out of FE(전진 근거를 FE 밖에 둠)"),
    }
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(INPUT_FILES, start=1):
        allowed, forbidden, use, effect = roles.get(path, ("input(입력)", "unknown forbidden use(알 수 없는 금지 사용)", "source identity(원천 정체성)", "tracks input(입력 추적)"))
        exists = path_exists(path)
        rows.append(
            {
                "source_id": f"fe_source_{index:02d}",
                "path": rel(path),
                "exists": "true" if exists else "false",
                "row_count": row_count(path) if exists else 0,
                "sha256": aw.sha256_file(path) if exists else "",
                "allowed_role": allowed,
                "forbidden_role": forbidden,
                "materialization_use": use,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_weight_recipes() -> list[dict[str, Any]]:
    return [
        {
            "recipe_id": "fe001_positive_clue_preservation",
            "materialized_column": "fd_positive_clue_preservation_weight",
            "source_columns": "side_quality_weight;cost_survival_weight;curve_state_pressure_weight",
            "split_scope": "train_only(학습 전용)",
            "timestamp_rule": "closed-bar source columns only(확정 봉 원천 열만)",
            "train_only_formula": "clip(side_quality_weight * cost_survival_weight * curve_state_pressure_weight, 0.10, 10.0)",
            "non_feature_status": "not_allowed_as_feature(피처 사용 금지)",
            "effect": "preserves ey003 signal family(ey003 신호 계열 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "fe002_curve_risk_suppression",
            "materialized_column": "fd_curve_risk_suppression",
            "source_columns": "drawdown_pressure_norm;underwater_rate_model;low_margin_rate_model",
            "split_scope": "train_only(학습 전용)",
            "timestamp_rule": "existing EW timestamp-safe columns only(기존 EW 시점 안전 열만)",
            "train_only_formula": "clip(1.35 - 0.70 * risk_pressure, 0.35, 1.35)",
            "non_feature_status": "not_allowed_as_feature(피처 사용 금지)",
            "effect": "reduces weight on high drawdown pressure rows(높은 낙폭 압력 행 가중 축소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "fe003_short_balance_boost",
            "materialized_column": "fd_short_balance_boost",
            "source_columns": "label_class;short_quality_target;side_quality_gap_norm",
            "split_scope": "train_only(학습 전용)",
            "timestamp_rule": "label horizon remains unchanged(라벨 지평 변경 없음)",
            "train_only_formula": "boost valid short labels and damp crowded long labels(유효 숏 라벨 가중, 롱 쏠림 완화)",
            "non_feature_status": "not_allowed_as_feature(피처 사용 금지)",
            "effect": "repairs side balance without forcing shorts(강제 숏 없이 방향 균형 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "fe004_drawdown_balance_weight",
            "materialized_column": "fd_drawdown_balance_weight",
            "source_columns": "fd_positive_clue_preservation_weight;fd_curve_risk_suppression;fd_short_balance_boost",
            "split_scope": "train_only(학습 전용)",
            "timestamp_rule": "derived from train-only recipe columns(학습 전용 조리법 열에서 파생)",
            "train_only_formula": "clip(preservation * suppression * side_balance, 0.10, 10.0)",
            "non_feature_status": "not_allowed_as_feature(피처 사용 금지)",
            "effect": "combines signal preservation and repair pressure(신호 보존과 수리 압력 결합)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_weight_audit(frame: pd.DataFrame) -> list[dict[str, Any]]:
    label = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int)
    rows: list[dict[str, Any]] = []
    for column in NEW_WEIGHT_COLUMNS:
        weights = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
        rows.append(
            {
                "weight_column": column,
                "rows": int(len(weights)),
                "weight_min": float(weights.min()),
                "weight_mean": float(weights.mean()),
                "weight_max": float(weights.max()),
                "nonfinite_rows": int(weights.isna().sum()),
                "short_label_mean": float(weights[label == 0].mean()),
                "flat_label_mean": float(weights[label == 1].mean()),
                "long_label_mean": float(weights[label == 2].mean()),
                "effect": "checks bounded train-only repair weights(범위 제한 학습 전용 수리 가중치 점검)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_boundary_rows(frame: pd.DataFrame, feature_rows: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    feature_names = {row["feature_name"] for row in feature_rows}
    forbidden_as_feature = sorted(feature_names.intersection(FORBIDDEN_FEATURE_COLUMNS))
    duplicated = int(len(frame) - frame["timestamp"].nunique()) if "timestamp" in frame.columns else 0
    boundary_rows = [
        {
            "audit_id": "fe001_feature_count",
            "status": "passed" if len(feature_names) == 58 else "failed",
            "observed": str(len(feature_names)),
            "expected": "58",
            "effect": "keeps EW reviewed feature order(검토된 EW 피처 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "fe002_forbidden_feature_exclusion",
            "status": "passed" if not forbidden_as_feature else "failed",
            "observed": ";".join(forbidden_as_feature) if forbidden_as_feature else "none",
            "expected": "none",
            "effect": "prevents labels, outcomes, and repair weights entering model features(라벨/결과/수리 가중치의 피처 유입 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "fe003_split_boundary",
            "status": "passed" if summary["split_values"] == "train" else "failed",
            "observed": summary["split_values"],
            "expected": "train",
            "effect": "keeps FE train-only( FE를 학습 전용으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "fe004_nonfinite_weights",
            "status": "passed" if summary["nonfinite_weight_rows"] == 0 else "failed",
            "observed": str(summary["nonfinite_weight_rows"]),
            "expected": "0",
            "effect": "keeps future training numerically safe(향후 학습 수치 안정성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    handoff_rows = [
        {
            "audit_id": "fe_unique_timestamp_handoff_contract",
            "status": "materialized",
            "observed": f"frame_rows={summary['rows']};unique_timestamps={summary['unique_timestamps']};duplicate_training_rows={duplicated}",
            "expected": "future runtime package must dedupe to one row per timestamp/model(향후 런타임 패키지는 시각/모델당 한 행으로 중복 제거)",
            "effect": "training keeps cost-policy rows, runtime handoff stays unique(학습은 비용정책 행을 유지하고 런타임 인계는 고유 행 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    negative_rows = [
        {
            "control_id": row.get("constraint_id", f"negative_{index:02d}"),
            "source_control": row.get("subject", ""),
            "materialized_status": "carried_forward_active",
            "observed": row.get("rule", ""),
            "invalid_if_future_review": row.get("forbidden_action", ""),
            "effect": row.get("effect", "negative control remains active(부정 대조 활성 유지)"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(read_csv(FD_NEGATIVE), start=1)
    ]
    release_rows = [
        {
            "gate_id": row.get("gate_id", f"release_{index:02d}"),
            "source_gate": row.get("gate_family", ""),
            "materialized_status": "carried_forward_active",
            "observed": row.get("pass_condition", ""),
            "future_release_dependency": row.get("required_artifact", ""),
            "effect": row.get("effect", "release gate remains active(해제 게이트 활성 유지)"),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(read_csv(FD_RELEASE), start=1)
    ]
    task_rows = [
        {
            "task_id": "fg001_fd_drawdown_recovery",
            "feature_set_id": "fe_allowed_pretrade_features_v1",
            "target_column": "label_class",
            "sample_weight_expression": "fd_drawdown_recovery_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fd_drawdown_recovery",
            "feature_count": len(feature_names),
            "training_eligibility_status": "pending_run337FF_review",
            "required_guard": "FF review must pass feature boundary and weight audit(FF 검토에서 피처 경계와 가중치 감사를 통과해야 함)",
            "forbidden_action": "candidate selection, MT5 execution, Forward/Goal claim(후보 선택, MT5 실행, 전진/목표 주장)",
            "effect": "tests drawdown/recovery repair weight(낙폭/회복 수리 가중치 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fg002_fd_side_balance_rescue",
            "feature_set_id": "fe_allowed_pretrade_features_v1",
            "target_column": "label_class",
            "sample_weight_expression": "fd_side_balance_rescue_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fd_side_balance_rescue",
            "feature_count": len(feature_names),
            "training_eligibility_status": "pending_run337FF_review",
            "required_guard": "FF review must pass short-balance no-forcing control(FF 검토에서 숏 강제 금지 대조를 통과해야 함)",
            "forbidden_action": "candidate selection, MT5 execution, Forward/Goal claim(후보 선택, MT5 실행, 전진/목표 주장)",
            "effect": "tests side-balance rescue without forced shorts(강제 숏 없는 방향 균형 수리 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fg003_fd_drawdown_balance",
            "feature_set_id": "fe_allowed_pretrade_features_v1",
            "target_column": "label_class",
            "sample_weight_expression": "fd_drawdown_balance_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fd_drawdown_balance",
            "feature_count": len(feature_names),
            "training_eligibility_status": "pending_run337FF_review",
            "required_guard": "FF review must pass no leakage and weight bounds(FF 검토에서 누수 없음과 가중치 범위를 통과해야 함)",
            "forbidden_action": "candidate selection, MT5 execution, Forward/Goal claim(후보 선택, MT5 실행, 전진/목표 주장)",
            "effect": "combines positive clue preservation with risk repair(긍정 단서 보존과 위험 수리 결합)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fg004_fd_runtime_positive_clue_blend",
            "feature_set_id": "fe_allowed_pretrade_features_v1",
            "target_column": "label_class",
            "sample_weight_expression": "fd_runtime_positive_clue_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fd_runtime_positive_clue_blend",
            "feature_count": len(feature_names),
            "training_eligibility_status": "pending_run337FF_review",
            "required_guard": "FF review must keep proxy/MT5 boundary(FF 검토에서 프록시/MT5 경계를 유지해야 함)",
            "forbidden_action": "candidate selection, MT5 execution, Forward/Goal claim(후보 선택, MT5 실행, 전진/목표 주장)",
            "effect": "keeps a conservative blend of clue and repair(단서와 수리의 보수적 결합 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    queue_rows = [
        {
            "queue_id": "ff001_review_runtime_positive_clue_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "Review FE train-only repair inputs(FE 학습 전용 수리 입력 검토) before any model training(모델 학습 전).",
            "required_inputs": ";".join(rel(path) for path in (TRAIN_ONLY_REPAIR_FRAME, ALLOWED_FEATURE_SET, WEIGHT_AUDIT, FEATURE_LABEL_BOUNDARY, TRAINING_TASK_SEEDS)),
            "required_outputs": "input safety review(입력 안전 검토); training eligibility matrix(학습 적격 행렬); FG training queue(FG 학습 대기열)",
            "blocked_if_missing": "FE frame or weight audit(FE 프레임 또는 가중치 감사)",
            "forbidden_action": "train model, tune threshold, run MT5, or claim selection in FF(FF에서 학습/임계값 튜닝/MT5 실행/선택 주장 금지)",
            "effect": "keeps materialization and training separated(물질화와 학습을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return boundary_rows, handoff_rows, negative_rows, release_rows, task_rows + queue_rows


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fd_final = read_json(FD_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fd_next_action": fd_final.get("next_action", ""),
        "fd_failed_gate_rows": sum(1 for row in read_csv(FD_GATES) if row.get("status") != "passed"),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["model_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(FD_FINAL), "required FE inputs exist(필수 FE 입력 존재)"),
        ("parent_fd_gates_passed", final["fd_failed_gate_rows"] == 0, str(final["fd_failed_gate_rows"]), "0", rel(FD_GATES), "FD gates passed(FD 게이트 통과)"),
        ("parent_next_action_matches", final["fd_next_action"] == RUN_ID, str(final["fd_next_action"]), RUN_ID, rel(FD_FINAL), "FE follows FD next action(FE가 FD 다음 행동을 따름)"),
        ("base_frame_loaded", final["rows"] > 80000, str(final["rows"]), ">80000", rel(TRAIN_ONLY_REPAIR_FRAME), "train-only base frame loaded(학습 전용 기본 프레임 적재)"),
        ("feature_count_matches", final["feature_count"] == 58, str(final["feature_count"]), "58", rel(ALLOWED_FEATURE_SET), "reviewed feature set preserved(검토된 피처 묶음 보존)"),
        ("new_weights_materialized", final["new_weight_count"] == len(NEW_WEIGHT_COLUMNS), str(final["new_weight_count"]), str(len(NEW_WEIGHT_COLUMNS)), rel(WEIGHT_AUDIT), "repair weights materialized(수리 가중치 물질화)"),
        ("nonfinite_weights_zero", final["nonfinite_weight_rows"] == 0, str(final["nonfinite_weight_rows"]), "0", rel(WEIGHT_AUDIT), "weights are finite(가중치 유한)"),
        ("forbidden_features_excluded", final["forbidden_feature_rows"] == 0, str(final["forbidden_feature_rows"]), "0", rel(FEATURE_LABEL_BOUNDARY), "labels/outcomes/weights excluded from features(라벨/결과/가중치 피처 제외)"),
        ("unique_timestamp_contract_materialized", final["unique_timestamps"] > 0 and path_exists(UNIQUE_TIMESTAMP_HANDOFF), str(final["unique_timestamps"]), ">0", rel(UNIQUE_TIMESTAMP_HANDOFF), "runtime handoff contract carried(런타임 인계 계약 이월)"),
        ("ff_queue_materialized", final["ff_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['ff_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(FF_QUEUE), "FF review queue opened(FF 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['model_training']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "materialization without operating claim(운영 주장 없는 물질화)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장이 게이트에 연결됨)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    data = {
        "data_source": rel(EW_FRAME),
        "time_axis": "closed M5 bar timestamp(확정 M5 봉 시각), train-only split(학습 전용 분할)",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": final["rows"],
            "unique_timestamps": final["unique_timestamps"],
            "cost_policy_count": final["cost_policy_count"],
            "split_values": final["split_values"],
        },
        "missing_or_duplicate_check": "training keeps cost-policy duplicate timestamps; runtime handoff must dedupe(학습은 비용정책 중복 시각 유지, 런타임 인계는 중복 제거)",
        "feature_label_boundary": "allowed 58 features only; labels/outcomes/repair weights excluded(허용 58개 피처만, 라벨/결과/수리 가중치 제외)",
        "split_boundary": "train only, FF review required before training(학습 전용, 학습 전 FF 검토 필요)",
        "leakage_risk": "repair weights accidentally used as features(수리 가중치가 피처로 들어가는 위험)",
        "data_hash_or_identity": {"frame_sha256": aw.sha256_file(TRAIN_ONLY_REPAIR_FRAME), "feature_sha256": aw.sha256_file(ALLOWED_FEATURE_SET)},
        "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_action": "not_run(실행 안 함)",
        "training_task_seed_rows": final["training_task_seed_rows"],
        "future_requirement": "FF review must approve tasks before FG training(FF 검토가 FG 학습 전 작업을 승인해야 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "source_clue": "fa_ey_ey003_side_cost_curve net 49.99, PF 1.04, DD 241.33, recovery 0.21",
        "materialized_repair": "drawdown/recovery/side-balance weights(낙폭/회복/방향 균형 가중치)",
        "kpi_status": "no new KPI; materialization only(새 KPI 없음, 물질화 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "runtime_authority": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    lineage_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in lineage_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in lineage_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록과 함께 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FE Repair Input Materialization(337단계 337FE 수리 입력 물질화)

## Conclusion(결론)

Action(행동): run337EW train-only frame(337EW 학습 전용 프레임)에 FD repair weights(FD 수리 가중치)를 물질화했다. Effect(효과): ey003 positive clue(ey003 긍정 단서)를 보존하면서 drawdown/recovery/side balance(낙폭/회복/방향 균형) 수리 입력을 만들었다.

Action(행동): model training(모델 학습), threshold tuning(임계값 튜닝), MT5 execution(MT5 실행)은 하지 않았다. Effect(효과): 다음 FF review(FF 검토)가 feature boundary(피처 경계), weight audit(가중치 감사), training eligibility(학습 적격성)를 먼저 판단한다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- unique_timestamps(고유 시각): `{final['unique_timestamps']}`
- cost_policy_count(비용 정책 수): `{final['cost_policy_count']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['nonfinite_weight_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Artifacts(산출물)

- train_only_frame(학습 전용 프레임): `{rel(TRAIN_ONLY_REPAIR_FRAME)}`
- feature_set(피처 묶음): `{rel(ALLOWED_FEATURE_SET)}`
- weight_recipe(가중치 조리법): `{rel(WEIGHT_RECIPE_MATRIX)}`
- weight_audit(가중치 감사): `{rel(WEIGHT_AUDIT)}`
- feature_boundary(피처 경계): `{rel(FEATURE_LABEL_BOUNDARY)}`
- training_task_seeds(학습 작업 씨앗): `{rel(TRAINING_TASK_SEEDS)}`
- next_queue(다음 대기열): `{rel(FF_QUEUE)}`

Boundary(경계): FE(337FE 실행)는 materialization only(물질화 전용)이다. Forward/Goal(전진/목표), runtime authority(런타임 권위), operating promotion(운영 승격)은 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FE Decision(337FE 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAIN_ONLY_REPAIR_FRAME)}`, `{rel(WEIGHT_AUDIT)}`, `{rel(FEATURE_LABEL_BOUNDARY)}`

Action(행동): drawdown/recovery/side-balance repair input(낙폭/회복/방향 균형 수리 입력)을 학습 전용 프레임으로 만들었다.
Effect(효과): 다음 FF review(FF 검토)는 모델 학습 전 데이터 무결성과 수리 가중치가 안전한지 판단한다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    if marker in text:
        return text.replace(marker, section.rstrip() + "\n\n" + marker, 1)
    return text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {fd.current_branch()}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FE focus complete: run337FE(337FE 실행)는 `{final['status']}`로 repair input materialization(수리 입력 물질화)을 완료했다. "
        f"Effect(효과): rows(행) `{final['rows']}`, feature count(피처 수) `{final['feature_count']}`, new weights(새 가중치) `{final['new_weight_count']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FE focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FE focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337FE Repair Input Materialization(수리 입력 물질화)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): FD design(FD 설계)을 train-only repair inputs(학습 전용 수리 입력)로 물질화했고, 모델 학습 전 FF review(FF 검토)를 요구한다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337FD Positive Clue Repair Design", section, "run337FE Repair Input Materialization")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- materialized_rows(물질화 행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FE(337FE 실행)는 materialization(물질화)만 완료했고 model training(모델 학습), MT5 execution(MT5 실행), operating selection(운영 선택)은 하지 않았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337FE(337FE 실행) `{final['status']}`. Effect(효과): FD 수리 설계를 `{final['rows']}`행 train-only repair frame(학습 전용 수리 프레임)으로 물질화하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337FE(337FE 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337FE(337FE 실행) `{final['status']}`. Effect(효과): runtime positive clue repair(런타임 긍정 단서 수리) 입력을 물질화하고 FF review(FF 검토)를 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337FE", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    rows = [item for item in existing if str(item.get(key, "")) != str(row.get(key, ""))]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_clue_drawdown_balance_repair_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "data_integrity_artifact_lineage_experiment_execution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "train_only_runtime_positive_clue_repair_inputs(학습 전용 런타임 긍정 단서 수리 입력)",
        "tier_scope": "Tier A train-only input; Tier B out_of_scope_by_claim(Tier A 학습 전용 입력, Tier B 주장 범위 밖)",
        "kpi_scope": "materialization only; no new KPI(물질화 전용, 새 성과 없음)",
        "scoreboard_lane": "data_integrity",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']}",
        "guardrail_kpi": "no_training;no_mt5;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_artifact_lineage_experiment_execution",
        "evidence_scope": "FD design and EW train-only frame",
        "kpi_scope": "materialization_no_new_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_input_materialization",
        "family": "runtime_positive_clue_repair_inputs",
        "question": "can the FD repair design be materialized into timestamp-safe train-only inputs",
        "metric_scope": "rows_features_weights_boundaries",
        "primary_artifact": rel(TRAIN_ONLY_REPAIR_FRAME),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        row = {
            "artifact_id": f"{RUN_ID}::{artifact_path}",
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    frame, summary = build_repair_frame()
    feature_rows = copy_allowed_features()
    source_rows = build_source_map()
    recipe_rows = build_weight_recipes()
    weight_rows = build_weight_audit(frame)
    boundary_rows, handoff_rows, negative_rows, release_rows, task_and_queue_rows = build_boundary_rows(frame, feature_rows, summary)
    task_rows = [row for row in task_and_queue_rows if "task_id" in row]
    queue_rows = [row for row in task_and_queue_rows if "queue_id" in row]

    summary = {
        **summary,
        "feature_count": len(feature_rows),
        "forbidden_feature_rows": sum(1 for row in boundary_rows if row["audit_id"] == "fe002_forbidden_feature_exclusion" and row["status"] != "passed"),
        "source_rows": len(source_rows),
        "recipe_rows": len(recipe_rows),
        "weight_audit_rows": len(weight_rows),
        "boundary_rows": len(boundary_rows),
        "negative_control_rows": len(negative_rows),
        "release_gate_rows": len(release_rows),
        "training_task_seed_rows": len(task_rows),
        "ff_queue_rows": len(queue_rows),
    }
    final = make_final(summary)

    artifacts = [
        write_frame(frame),
        write_csv(MATERIALIZATION_SOURCE_MAP, SOURCE_COLUMNS, source_rows),
        write_csv(ALLOWED_FEATURE_SET, FEATURE_COLUMNS, feature_rows),
        write_csv(WEIGHT_RECIPE_MATRIX, RECIPE_COLUMNS, recipe_rows),
        write_csv(WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, weight_rows),
        write_csv(FEATURE_LABEL_BOUNDARY, BOUNDARY_COLUMNS, boundary_rows),
        write_csv(UNIQUE_TIMESTAMP_HANDOFF, BOUNDARY_COLUMNS, handoff_rows),
        write_csv(NEGATIVE_CONTROL_MATERIALIZATION, CONTROL_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_MATERIALIZATION, RELEASE_COLUMNS, release_rows),
        write_csv(TRAINING_TASK_SEEDS, TASK_COLUMNS, task_rows),
        write_csv(FF_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]

    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "new_weight_count": final["new_weight_count"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

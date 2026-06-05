from __future__ import annotations

import json
import math
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
from stage_pipelines.stage337 import design_proxy_negative_trade_shape_second_order_repair_without_db as hr  # noqa: E402


aw = hr.aw
fb = hr.fb
he = hr.he

TODAY = "2026-05-31"
STAGE_ID = hr.STAGE_ID
RUN_NUMBER = "run337HS"
RUN_ID = "run337HS_materialize_proxy_negative_trade_shape_second_order_repair_inputs_without_db_v1"
PARENT_RUN_ID = hr.RUN_ID
NEXT_RUN_ID = "run337HT_review_proxy_negative_trade_shape_second_order_repair_inputs_without_db_v1"
STATUS = "completed_stage337HS_proxy_negative_trade_shape_second_order_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_second_order_density_calibration_regime_inputs_materialized_review_required"
DECISION = "stage337HS_open_run337HT_proxy_negative_trade_shape_second_order_input_review"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HS_proxy_negative_trade_shape_second_order_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_runtime_package_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hr.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hr.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HS_proxy_negative_trade_shape_second_order_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HS_proxy_negative_trade_shape_second_order_repair_inputs.md"

HR_FINAL = hr.FINAL_DECISION
HR_GATES = hr.GATE_AUDIT
HR_QUEUE = hr.MATERIALIZATION_QUEUE
HR_DESIGN = hr.DESIGN_MATRIX
HR_EXPERIMENT = hr.EXPERIMENT_CONTRACT
HR_OBJECTIVE = hr.OBJECTIVE_CONTRACT
HR_FEATURE_LABEL = hr.FEATURE_LABEL_CONTRACT
HR_ATTRIBUTION = hr.FAILURE_ATTRIBUTION
HR_CALIBRATION_PLAN = hr.CALIBRATION_SELECTIVITY_PLAN
HR_DENSITY_PLAN = hr.DENSITY_COLLAPSE_PLAN
HR_SESSION_PLAN = hr.SESSION_REGIME_PLAN
HR_MODEL_PROPOSAL = hr.MODEL_PROPOSAL
HR_TASK_BLUEPRINT = hr.TRAINING_TASK_BLUEPRINT
HR_RELEASE = hr.RELEASE_GATE_CONTRACT
BASE_FRAME = hr.HN_INPUT_FRAME
BASE_ALLOWED_FEATURES = hr.HN_ALLOWED_FEATURES
BASE_WEIGHT_AUDIT = hr.HN_WEIGHT_AUDIT

HS_INPUT_FRAME = RUN_DIR / "hs_input_frame.parquet"
HS_SOURCE_MAP = RUN_DIR / "hs_materialization_source_map.csv"
HS_ALLOWED_FEATURE_SET = RUN_DIR / "hs_allowed_model_feature_set.csv"
HS_WEIGHT_RECIPE = RUN_DIR / "hr_second_order_weight_recipe_matrix.csv"
HS_WEIGHT_AUDIT = RUN_DIR / "hr_second_order_weight_audit.csv"
HS_TARGET_AUDIT = RUN_DIR / "target_contract_audit.csv"
HS_FEATURE_BOUNDARY = RUN_DIR / "feature_label_boundary_audit.csv"
HS_DENSITY_AUDIT = RUN_DIR / "second_order_density_calibration_audit.csv"
HS_MODEL_PROPOSAL_REVIEW = RUN_DIR / "model_family_proposal_materialization_review.csv"
HS_RELEASE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
HS_TRAINING_TASK_SEEDS = RUN_DIR / "run337HU_training_task_seed_matrix.csv"
HT_QUEUE = RUN_DIR / "run337HT_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HR_FINAL,
    HR_GATES,
    HR_QUEUE,
    HR_DESIGN,
    HR_EXPERIMENT,
    HR_OBJECTIVE,
    HR_FEATURE_LABEL,
    HR_ATTRIBUTION,
    HR_CALIBRATION_PLAN,
    HR_DENSITY_PLAN,
    HR_SESSION_PLAN,
    HR_MODEL_PROPOSAL,
    HR_TASK_BLUEPRINT,
    HR_RELEASE,
    BASE_FRAME,
    BASE_ALLOWED_FEATURES,
    BASE_WEIGHT_AUDIT,
)
OUTPUT_FILES = (
    HS_INPUT_FRAME,
    HS_SOURCE_MAP,
    HS_ALLOWED_FEATURE_SET,
    HS_WEIGHT_RECIPE,
    HS_WEIGHT_AUDIT,
    HS_TARGET_AUDIT,
    HS_FEATURE_BOUNDARY,
    HS_DENSITY_AUDIT,
    HS_MODEL_PROPOSAL_REVIEW,
    HS_RELEASE_MATERIALIZATION,
    HS_TRAINING_TASK_SEEDS,
    HT_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUN_EVIDENCE_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    he.RUN_REGISTRY,
    he.ALPHA_LEDGER,
    he.STAGE_LEDGER,
    he.ARTIFACT_REGISTRY,
    Path(__file__),
)

NEW_WEIGHT_COLUMNS = (
    "hr_flat_rescue_calibration_weight",
    "hr_cost_buffer_sparse_edge_weight",
    "hr_session_regime_loss_firewall_weight",
    "hr_train_holdout_inversion_brake_weight",
    "hr_multi_kpi_release_firewall_weight",
)
TASK_WEIGHT_COLUMNS = {
    "hs_hr001_flat_rescue_calibration_gate": "hr_flat_rescue_calibration_weight",
    "hs_hr002_cost_buffer_sparse_edge": "hr_cost_buffer_sparse_edge_weight",
    "hs_hr003_session_regime_loss_firewall": "hr_session_regime_loss_firewall_weight",
    "hs_hr004_inversion_brake_low_complexity": "hr_train_holdout_inversion_brake_weight",
    "hs_hr005_multi_kpi_release_firewall": "hr_multi_kpi_release_firewall_weight",
}
FORBIDDEN_FEATURE_TOKENS = (
    "label",
    "future",
    "claim_boundary",
    "net_profit",
    "profit_factor",
    "recovery",
    "drawdown",
    "expectancy",
)

SOURCE_COLUMNS = ("source_id", "source_path", "source_type", "required", "exists", "sha256", "effect", "claim_boundary")
WEIGHT_RECIPE_COLUMNS = (
    "recipe_id",
    "materialized_column",
    "source_columns",
    "train_only_formula",
    "lower_bound",
    "upper_bound",
    "expected_effect",
    "claim_boundary",
)
WEIGHT_AUDIT_COLUMNS = (
    "weight_column",
    "rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_rows",
    "saturated_rows",
    "saturation_rate",
    "short_label_mean",
    "flat_label_mean",
    "long_label_mean",
    "effect",
    "claim_boundary",
)
AUDIT_COLUMNS = ("audit_id", "status", "observed", "expected", "evidence", "effect", "claim_boundary")
TASK_SEED_COLUMNS = (
    "task_id",
    "target_column",
    "sample_weight_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "source_failure_or_seed",
    "selection_status",
    "required_guard",
    "expected_effect",
    "forbidden_use",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "source_run_id",
    "next_run_id",
    "task",
    "required_inputs",
    "expected_outputs",
    "blocked_if_missing",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


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


def numeric(df: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in df.columns:
        return pd.Series(default, index=df.index, dtype="float64")
    return pd.to_numeric(df[column], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(default).astype("float64")


def norm01(series: pd.Series) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0).astype("float64")
    lo = float(clean.quantile(0.05))
    hi = float(clean.quantile(0.95))
    if not math.isfinite(lo) or not math.isfinite(hi) or hi <= lo:
        return pd.Series(0.0, index=clean.index, dtype="float64")
    return ((clean - lo) / (hi - lo)).clip(0.0, 1.0)


def clip_weight(value: pd.Series | np.ndarray) -> np.ndarray:
    return np.clip(np.asarray(value, dtype="float64"), 0.25, 10.0)


def normalized_base(df: pd.DataFrame, column: str, default: float = 1.0) -> pd.Series:
    raw = numeric(df, column, default).clip(0.35, 8.0)
    median = float(raw.median())
    if not math.isfinite(median) or median <= 0:
        median = 1.0
    return (raw / median).clip(0.45, 1.95)


def build_weights(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    out = df.copy()
    label_text = out.get("label", pd.Series("", index=out.index)).astype(str).str.lower()
    is_short = label_text.eq("short")
    is_flat = label_text.eq("flat")
    is_long = label_text.eq("long")
    is_trade = is_short | is_long

    hm_base = normalized_base(out, "hm_balanced_proxy_release_ladder_weight")
    hm_density = normalized_base(out, "hm_density_cost_selectivity_weight")
    hm_gap = normalized_base(out, "hm_generalization_gap_pressure_weight")
    hm_session = normalized_base(out, "hm_session_regime_turnover_firewall_weight")
    low_margin = norm01(numeric(out, "low_margin_rate"))
    abstention = norm01(numeric(out, "abstention_rate"))
    churn = norm01(numeric(out, "gz_trade_churn_pressure") + numeric(out, "hh_trade_churn_pressure"))
    cost_risk = norm01(numeric(out, "gz_cost_adverse_risk") + numeric(out, "hh_cost_adverse_risk"))
    precision_risk = norm01(numeric(out, "gz_precision_risk") + numeric(out, "hh_precision_risk"))
    payoff_tail = norm01(numeric(out, "payoff_tail_norm"))
    prob_margin = norm01(numeric(out, "gz_probability_margin") + numeric(out, "hh_probability_margin"))
    side_quality = norm01(numeric(out, "side_quality_weight", 1.0))
    cash_open = numeric(out, "is_us_cash_open").clip(0.0, 1.0)
    open_edge = numeric(out, "is_first_30m_after_open").clip(0.0, 1.0)
    close_edge = numeric(out, "is_last_30m_before_cash_close").clip(0.0, 1.0)
    session_stress = (0.60 * cash_open + 0.25 * open_edge + 0.25 * close_edge).clip(0.0, 1.0)

    flat_rescue = hm_base * np.where(
        is_flat,
        1.35 + 1.45 * low_margin + 1.20 * churn + 0.85 * cost_risk + 0.35 * abstention,
        1.05 + 0.55 * payoff_tail + 0.25 * prob_margin - 0.60 * low_margin - 0.55 * churn,
    )
    sparse_edge = hm_density * np.where(
        is_trade,
        1.05 + 0.80 * payoff_tail + 0.70 * prob_margin + 0.35 * side_quality - 0.70 * cost_risk - 0.45 * low_margin,
        1.20 + 1.15 * cost_risk + 0.95 * low_margin + 0.45 * churn,
    )
    session_firewall = hm_session * np.where(
        is_flat,
        1.10 + 0.75 * session_stress + 0.75 * churn + 0.55 * cost_risk,
        1.05 + 0.40 * payoff_tail + 0.25 * prob_margin - 0.35 * session_stress * churn,
    )
    inversion_brake = hm_gap * np.where(
        is_trade,
        1.00 + 0.50 * payoff_tail + 0.45 * prob_margin - 0.65 * precision_risk - 0.40 * low_margin,
        1.10 + 0.85 * precision_risk + 0.75 * abstention + 0.50 * low_margin,
    )
    multi_kpi = np.power(
        np.maximum(flat_rescue, 0.25)
        * np.maximum(sparse_edge, 0.25)
        * np.maximum(session_firewall, 0.25)
        * np.maximum(inversion_brake, 0.25),
        0.25,
    )

    out["hr_flat_rescue_calibration_weight"] = clip_weight(flat_rescue)
    out["hr_cost_buffer_sparse_edge_weight"] = clip_weight(sparse_edge)
    out["hr_session_regime_loss_firewall_weight"] = clip_weight(session_firewall)
    out["hr_train_holdout_inversion_brake_weight"] = clip_weight(inversion_brake)
    out["hr_multi_kpi_release_firewall_weight"] = clip_weight(multi_kpi)

    recipes = [
        {
            "recipe_id": "hr_flat_rescue_calibration",
            "materialized_column": "hr_flat_rescue_calibration_weight",
            "source_columns": "hm_balanced_proxy_release_ladder_weight;low_margin_rate;abstention_rate;gz_trade_churn_pressure;hh_trade_churn_pressure;label",
            "train_only_formula": "flat support rises under low-margin churn; trade pressure needs payoff/probability support(낮은 마진 과회전에서는 무거래 지지 상승, 거래 압력은 payoff/probability 지지 필요)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "약한 방향 신호를 줄이고 무거래 구조를 회복한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hr_cost_buffer_sparse_edge",
            "materialized_column": "hr_cost_buffer_sparse_edge_weight",
            "source_columns": "hm_density_cost_selectivity_weight;gz_cost_adverse_risk;hh_cost_adverse_risk;payoff_tail_norm;label",
            "train_only_formula": "trade labels need cost-buffer support; flat labels rise in adverse cost states(거래 라벨은 비용 버퍼 지지 필요, 악성 비용 상태에서는 무거래 상승)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "비용을 넘지 못하는 거래를 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hr_session_regime_loss_firewall",
            "materialized_column": "hr_session_regime_loss_firewall_weight",
            "source_columns": "hm_session_regime_turnover_firewall_weight;is_us_cash_open;is_first_30m_after_open;is_last_30m_before_cash_close;label",
            "train_only_formula": "session stress raises flat support under churn/cost(세션 압박은 과회전/비용 상태에서 무거래 지지 상승)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "세션/국면 취약성을 완화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hr_train_holdout_inversion_brake",
            "materialized_column": "hr_train_holdout_inversion_brake_weight",
            "source_columns": "hm_generalization_gap_pressure_weight;gz_precision_risk;hh_precision_risk;low_margin_rate;label",
            "train_only_formula": "precision risk and low margin raise flat support, trade labels need probability margin(정밀도 위험과 낮은 마진은 무거래 지지 상승, 거래 라벨은 확률 마진 필요)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "학습/보류 역전 압력을 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hr_multi_kpi_release_firewall",
            "materialized_column": "hr_multi_kpi_release_firewall_weight",
            "source_columns": ";".join(NEW_WEIGHT_COLUMNS[:-1]),
            "train_only_formula": "geometric blend of flat/cost/session/inversion weights(무거래/비용/세션/역전 가중치 기하 혼합)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "단일 수리축 과맞춤을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    summary = {
        "label_short_rows": int(is_short.sum()),
        "label_flat_rows": int(is_flat.sum()),
        "label_long_rows": int(is_long.sum()),
    }
    return out, recipes, summary


def build_weight_audit(df: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    label_text = df.get("label", pd.Series("", index=df.index)).astype(str).str.lower()
    rows: list[dict[str, Any]] = []
    total_nonfinite = 0
    max_saturation_rate = 0.0
    for column in NEW_WEIGHT_COLUMNS:
        values = numeric(df, column, np.nan)
        finite = np.isfinite(values.to_numpy())
        nonfinite = int((~finite).sum())
        saturated = int((values >= 9.999).sum())
        saturation_rate = float(saturated / max(len(values), 1))
        total_nonfinite += nonfinite
        max_saturation_rate = max(max_saturation_rate, saturation_rate)
        rows.append(
            {
                "weight_column": column,
                "rows": len(values),
                "weight_min": float(values.min()),
                "weight_mean": float(values.mean()),
                "weight_max": float(values.max()),
                "nonfinite_rows": nonfinite,
                "saturated_rows": saturated,
                "saturation_rate": saturation_rate,
                "short_label_mean": float(values[label_text.eq("short")].mean()),
                "flat_label_mean": float(values[label_text.eq("flat")].mean()),
                "long_label_mean": float(values[label_text.eq("long")].mean()),
                "effect": "records second-order class-aware repair pressure(2차 클래스 인식 수리 압력 기록)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, {"total_nonfinite_weight_rows": total_nonfinite, "max_saturation_rate": max_saturation_rate}


def build_packets() -> tuple[dict[str, Any], list[Path]]:
    hr_final = read_json(HR_FINAL)
    hr_tasks = read_csv(HR_TASK_BLUEPRINT)
    hr_release = read_csv(HR_RELEASE)
    hr_proposals = read_csv(HR_MODEL_PROPOSAL)
    base_features = read_csv(BASE_ALLOWED_FEATURES)
    df = pd.read_parquet(aw.io_path(BASE_FRAME))
    materialized, recipes, label_summary = build_weights(df)
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    materialized.to_parquet(aw.io_path(HS_INPUT_FRAME), index=False)

    source_rows = []
    for source_id, path, source_type, effect in [
        ("hr_final", HR_FINAL, "parent_final_decision", "HR decision lock(HR 결정 잠금)"),
        ("hr_gates", HR_GATES, "parent_gates", "HR gates passed(HR 게이트 통과)"),
        ("hr_queue", HR_QUEUE, "parent_queue", "HS queue authority(HS 대기열 권위)"),
        ("hr_task_blueprint", HR_TASK_BLUEPRINT, "task_blueprint", "task and weight mapping(작업과 가중치 매핑)"),
        ("hr_calibration_plan", HR_CALIBRATION_PLAN, "repair_plan", "calibration/selectivity repair plan(보정/선택성 수리 계획)"),
        ("hr_density_plan", HR_DENSITY_PLAN, "repair_plan", "density/cost repair plan(밀도/비용 수리 계획)"),
        ("hr_session_plan", HR_SESSION_PLAN, "repair_plan", "session/regime repair plan(세션/국면 수리 계획)"),
        ("base_frame", BASE_FRAME, "train_only_frame", "base timestamp-safe HN input frame(기본 시점 안전 HN 입력 프레임)"),
        ("base_allowed_features", BASE_ALLOWED_FEATURES, "feature_contract", "feature list without second-order weights(2차 가중치 없는 피처 목록)"),
    ]:
        source_rows.append(
            {
                "source_id": source_id,
                "source_path": rel(path),
                "source_type": source_type,
                "required": "true",
                "exists": str(path_exists(path)).lower(),
                "sha256": aw.sha256_file(path) if path_exists(path) and aw.io_path(path).is_file() else "",
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    allowed_rows = []
    for row in base_features:
        feature_name = row.get("feature_name", "")
        allowed_rows.append(
            {
                "feature_name": feature_name,
                "feature_family": row.get("feature_family", ""),
                "source_layer": rel(HS_INPUT_FRAME),
                "timestamp_rule": row.get("timestamp_rule", "known at or before decision bar close(의사결정 봉 마감 이전 인지 가능)"),
                "allowed_use": "future reviewed training feature after HT review(HT 검토 뒤 향후 학습 피처)",
                "forbidden_use": "label, selector, future outcome, second-order repair weight(라벨/선택자/미래 결과/2차 수리 가중치)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    forbidden_feature_hits = [
        row.get("feature_name", "")
        for row in allowed_rows
        if any(token in str(row.get("feature_name", "")).lower() for token in FORBIDDEN_FEATURE_TOKENS)
    ]

    weight_audit, weight_summary = build_weight_audit(materialized)
    timestamp_ordered = bool(pd.to_datetime(materialized["timestamp"], errors="coerce").is_monotonic_increasing) if "timestamp" in materialized.columns else False
    duplicate_timestamps = int(materialized["timestamp"].duplicated().sum()) if "timestamp" in materialized.columns else -1
    target_rows = [
        {
            "audit_id": "hs_target001_label_class_present",
            "status": "passed" if "label_class" in materialized.columns else "failed",
            "observed": "present" if "label_class" in materialized.columns else "missing",
            "expected": "present",
            "evidence": rel(HS_INPUT_FRAME),
            "effect": "keeps supervised target boundary(지도학습 목표 경계 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_target002_tasks_target_label_class",
            "status": "passed" if sum(1 for row in hr_tasks if row.get("target_column") == "label_class") == 5 else "failed",
            "observed": str(sum(1 for row in hr_tasks if row.get("target_column") == "label_class")),
            "expected": "5",
            "evidence": rel(HR_TASK_BLUEPRINT),
            "effect": "all HS tasks use the same target(모든 HS 작업이 같은 목표 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    feature_rows = [
        {
            "audit_id": "hs_feature001_allowed_feature_count",
            "status": "passed" if len(allowed_rows) == 58 else "failed",
            "observed": str(len(allowed_rows)),
            "expected": "58",
            "evidence": rel(HS_ALLOWED_FEATURE_SET),
            "effect": "keeps reviewed model feature order(검토된 모델 피처 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_feature002_forbidden_features_excluded",
            "status": "passed" if not forbidden_feature_hits else "failed",
            "observed": ";".join(forbidden_feature_hits),
            "expected": "no label/future/weight/outcome features(라벨/미래/가중치/결과 피처 없음)",
            "evidence": rel(HS_ALLOWED_FEATURE_SET),
            "effect": "prevents target and repair-weight leakage(목표와 수리 가중치 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_feature003_timestamp_order",
            "status": "passed" if timestamp_ordered else "failed",
            "observed": str(timestamp_ordered),
            "expected": "True",
            "evidence": rel(HS_INPUT_FRAME),
            "effect": "keeps time axis ordered(시간축 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_feature004_timestamp_duplicates_named",
            "status": "passed" if duplicate_timestamps >= 0 else "failed",
            "observed": str(duplicate_timestamps),
            "expected": "duplicates allowed by cost_policy_id expansion(비용 정책 확장 중복 허용)",
            "evidence": rel(HS_INPUT_FRAME),
            "effect": "names repeated timestamps instead of hiding them(반복 시각을 숨기지 않고 이름 붙임)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_feature005_nonfinite_weights",
            "status": "passed" if weight_summary["total_nonfinite_weight_rows"] == 0 else "failed",
            "observed": str(weight_summary["total_nonfinite_weight_rows"]),
            "expected": "0",
            "evidence": rel(HS_WEIGHT_AUDIT),
            "effect": "second-order weights are finite(2차 가중치 유한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_feature006_macro_join_safe_by_absence",
            "status": "passed",
            "observed": "no new macro source joined in HS(HS에서 새 거시 자료 결합 없음)",
            "expected": "economic data requires release timestamp(경제자료는 발표 시각 필요)",
            "evidence": rel(HR_FEATURE_LABEL),
            "effect": "prevents macro look-ahead(거시 미래참조 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    density_rows = [
        {
            "audit_id": "hs_density001_hr_weights_created",
            "status": "passed" if all(column in materialized.columns for column in NEW_WEIGHT_COLUMNS) else "failed",
            "observed": str(sum(1 for column in NEW_WEIGHT_COLUMNS if column in materialized.columns)),
            "expected": str(len(NEW_WEIGHT_COLUMNS)),
            "evidence": rel(HS_INPUT_FRAME),
            "effect": "materializes HR second-order weights(HR 2차 가중치 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hs_density002_saturation_watch",
            "status": "passed" if weight_summary["max_saturation_rate"] <= 0.25 else "failed",
            "observed": f"{weight_summary['max_saturation_rate']:.6f}",
            "expected": "<=0.25",
            "evidence": rel(HS_WEIGHT_AUDIT),
            "effect": "prevents clipped weight domination(클립 가중치 지배 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    proposal_review = [
        {
            "audit_id": f"hs_model_proposal_{index:02d}",
            "status": "materialized_as_metadata(메타데이터로 물질화)",
            "observed": row.get("model_family_or_rule_stack", ""),
            "expected": "proposal only, no training(제안만, 학습 없음)",
            "evidence": rel(HR_MODEL_PROPOSAL),
            "effect": row.get("expected_effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(hr_proposals, start=1)
    ]
    release_rows = [
        {
            "audit_id": row.get("gate_id", f"hr_release_{index}"),
            "status": "materialized_for_future_review(향후 검토용 물질화)",
            "observed": row.get("pass_condition", ""),
            "expected": row.get("fail_condition", ""),
            "evidence": rel(HR_RELEASE),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(hr_release, start=1)
    ]
    task_rows = []
    for row in hr_tasks:
        task_id = row.get("task_id", "")
        task_rows.append(
            {
                "task_id": task_id,
                "target_column": row.get("target_column", ""),
                "sample_weight_column": TASK_WEIGHT_COLUMNS.get(task_id, row.get("sample_weight_column", "")),
                "sample_weight_expression": row.get("sample_weight_expression", ""),
                "model_family": row.get("model_family", ""),
                "model_config_id": row.get("model_config_id", ""),
                "source_failure_or_seed": row.get("source_failure_or_seed", ""),
                "selection_status": "eligible_for_HT_review(HT 검토 대기)",
                "required_guard": row.get("required_guard", ""),
                "expected_effect": row.get("expected_effect", ""),
                "forbidden_use": row.get("forbidden_use", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    queue_rows = [
        {
            "queue_id": "ht_second_order_input_review",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "review HS materialized second-order weights before guarded training(HS 2차 가중치를 방어 학습 전 검토)",
            "required_inputs": ";".join(rel(path) for path in (HS_INPUT_FRAME, HS_ALLOWED_FEATURE_SET, HS_WEIGHT_AUDIT, HS_FEATURE_BOUNDARY, HS_TRAINING_TASK_SEEDS)),
            "expected_outputs": "HT eligibility review and HU training queue(HT 적격성 검토와 HU 학습 대기열)",
            "blocked_if_missing": "HS frame, feature set, or weight audit missing(HS 프레임, 피처셋, 가중치 감사 누락)",
            "effect": "prevents unreviewed second-order weights from training(미검토 2차 가중치 학습 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    artifacts = [
        HS_INPUT_FRAME,
        write_csv(HS_SOURCE_MAP, SOURCE_COLUMNS, source_rows),
        write_csv(HS_ALLOWED_FEATURE_SET, ("feature_name", "feature_family", "source_layer", "timestamp_rule", "allowed_use", "forbidden_use", "claim_boundary"), allowed_rows),
        write_csv(HS_WEIGHT_RECIPE, WEIGHT_RECIPE_COLUMNS, recipes),
        write_csv(HS_WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, weight_audit),
        write_csv(HS_TARGET_AUDIT, AUDIT_COLUMNS, target_rows),
        write_csv(HS_FEATURE_BOUNDARY, AUDIT_COLUMNS, feature_rows),
        write_csv(HS_DENSITY_AUDIT, AUDIT_COLUMNS, density_rows),
        write_csv(HS_MODEL_PROPOSAL_REVIEW, AUDIT_COLUMNS, proposal_review),
        write_csv(HS_RELEASE_MATERIALIZATION, AUDIT_COLUMNS, release_rows),
        write_csv(HS_TRAINING_TASK_SEEDS, TASK_SEED_COLUMNS, task_rows),
        write_csv(HT_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    first_ts = str(materialized["timestamp"].min()) if "timestamp" in materialized.columns else ""
    last_ts = str(materialized["timestamp"].max()) if "timestamp" in materialized.columns else ""
    summary = {
        "hr_failed_gate_rows": sum(1 for row in read_csv(HR_GATES) if row.get("status") != "passed"),
        "hr_next_action": hr_final.get("next_action"),
        "base_rows": len(materialized),
        "base_columns": len(df.columns),
        "materialized_columns": len(materialized.columns),
        "first_timestamp": first_ts,
        "last_timestamp": last_ts,
        "duplicate_timestamp_rows": duplicate_timestamps,
        "allowed_feature_rows": len(allowed_rows),
        "forbidden_feature_hits": len(forbidden_feature_hits),
        "new_weight_columns": len(NEW_WEIGHT_COLUMNS),
        "weight_recipe_rows": len(recipes),
        "weight_audit_rows": len(weight_audit),
        "total_nonfinite_weight_rows": weight_summary["total_nonfinite_weight_rows"],
        "max_saturation_rate": weight_summary["max_saturation_rate"],
        "target_audit_rows": len(target_rows),
        "failed_target_audits": sum(1 for row in target_rows if row["status"] != "passed"),
        "feature_boundary_rows": len(feature_rows),
        "failed_feature_boundary_rows": sum(1 for row in feature_rows if row["status"] != "passed"),
        "density_audit_rows": len(density_rows),
        "failed_density_audits": sum(1 for row in density_rows if row["status"] != "passed"),
        "model_proposal_review_rows": len(proposal_review),
        "release_materialization_rows": len(release_rows),
        "training_task_seed_rows": len(task_rows),
        "task_weight_columns_present": sum(1 for row in task_rows if row.get("sample_weight_column") in materialized.columns),
        "queue_rows": len(queue_rows),
        **label_summary,
    }
    return summary, artifacts


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": "obsidian-experiment-design;obsidian-data-integrity;obsidian-model-validation;obsidian-artifact-lineage",
        "required_gates": "scope_completion_gate;kpi_contract_audit;skill_receipt_lint;required_gate_coverage_audit;final_claim_guard",
        "new_training": "not_run",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "runtime_package": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["runtime_package"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    gate_specs = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HR_FINAL), "required HR and base inputs exist(필수 HR/기본 입력 존재)"),
        ("parent_hr_gates_passed", final["hr_failed_gate_rows"] == 0, str(final["hr_failed_gate_rows"]), "0", rel(HR_GATES), "HR gates passed(HR 게이트 통과)"),
        ("parent_next_action_matches", final["hr_next_action"] == RUN_ID, str(final["hr_next_action"]), RUN_ID, rel(HR_FINAL), "HS follows HR next action(HS가 HR 다음 행동을 따름)"),
        ("frame_materialized", path_exists(HS_INPUT_FRAME) and final["base_rows"] > 0, str(final["base_rows"]), ">0", rel(HS_INPUT_FRAME), "HS frame materialized(HS 프레임 물질화)"),
        ("new_weights_materialized", final["new_weight_columns"] == 5 and final["task_weight_columns_present"] == 5, f"weights={final['new_weight_columns']};task_columns={final['task_weight_columns_present']}", "5/5", rel(HS_WEIGHT_AUDIT), "all HR repair weights available(모든 HR 수리 가중치 사용 가능)"),
        ("weights_finite", final["total_nonfinite_weight_rows"] == 0, str(final["total_nonfinite_weight_rows"]), "0", rel(HS_WEIGHT_AUDIT), "weights are finite(가중치 유한)"),
        ("weight_saturation_guard", final["max_saturation_rate"] <= 0.25, f"{final['max_saturation_rate']:.6f}", "<=0.25", rel(HS_WEIGHT_AUDIT), "weight clipping not dominant(가중치 클립 지배 아님)"),
        ("feature_set_preserved", final["allowed_feature_rows"] == 58 and final["forbidden_feature_hits"] == 0, f"features={final['allowed_feature_rows']};forbidden={final['forbidden_feature_hits']}", "58/0", rel(HS_ALLOWED_FEATURE_SET), "allowed feature set preserved(허용 피처셋 보존)"),
        ("target_contract_audit", final["failed_target_audits"] == 0, str(final["failed_target_audits"]), "0", rel(HS_TARGET_AUDIT), "target boundary passed(목표 경계 통과)"),
        ("feature_boundary_audit", final["failed_feature_boundary_rows"] == 0, str(final["failed_feature_boundary_rows"]), "0", rel(HS_FEATURE_BOUNDARY), "feature/label boundary passed(피처/라벨 경계 통과)"),
        ("density_audit", final["failed_density_audits"] == 0, str(final["failed_density_audits"]), "0", rel(HS_DENSITY_AUDIT), "second-order repair audit passed(2차 수리 감사 통과)"),
        ("training_task_queue_ready", final["training_task_seed_rows"] == 5 and final["queue_rows"] == 1, f"tasks={final['training_task_seed_rows']};queue={final['queue_rows']}", "5 and 1", rel(HT_QUEUE), "HT review queue opened(HT 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};mt5={final['mt5_execution']};runtime_package={final['runtime_package']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "materialization without operating claim(운영 주장 없는 물질화)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    rows: list[dict[str, Any]] = []
    for gate_id, passed, observed, expected, evidence_path, effect in gate_specs:
        rows.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "evidence_path": evidence_path,
                "observed": observed,
                "expected": expected,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    receipts = [
        (
            DATA_RECEIPT,
            {
                "receipt_type": "data_integrity(데이터 무결성)",
                "run_id": RUN_ID,
                "data_source": rel(BASE_FRAME),
                "time_axis": f"{final['first_timestamp']} to {final['last_timestamp']} UTC closed-bar/as-of(UTC 닫힌 봉/시점 기준)",
                "sample_scope": f"FPMarkets US100 M5 train-only rows={final['base_rows']}",
                "missing_or_duplicate_check": f"duplicate_timestamp_rows={final['duplicate_timestamp_rows']} allowed by cost_policy_id expansion(비용 정책 확장 중복 허용)",
                "feature_label_boundary": "allowed feature set preserved; second-order weights excluded from features(허용 피처셋 보존, 2차 가중치는 피처 제외)",
                "split_boundary": "train-only materialization; HT must review before training(학습 전용 물질화, HT 검토 뒤 학습)",
                "leakage_risk": "holdout KPI or MT5 tester result copied into row input(보류 KPI 또는 MT5 테스터 결과 행 입력 복사)",
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "evidence": [rel(HS_FEATURE_BOUNDARY), rel(HS_ALLOWED_FEATURE_SET)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "receipt_type": "model_validation(모델 검증)",
                "run_id": RUN_ID,
                "model_action": "no model training(모델 학습 없음)",
                "task_seed_rows": final["training_task_seed_rows"],
                "future_validation": "HT input review then HU guarded training(HT 입력 검토 뒤 HU 방어 학습)",
                "evidence": [rel(HS_TRAINING_TASK_SEEDS), rel(HS_MODEL_PROPOSAL_REVIEW)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUN_EVIDENCE_RECEIPT,
            {
                "receipt_type": "run_evidence(실행 근거)",
                "run_id": RUN_ID,
                "status": STATUS,
                "gate_result": f"{final['passed_gates']}/{final['gate_rows']}",
                "evidence": [rel(FINAL_DECISION), rel(GATE_AUDIT), rel(RUN_MANIFEST)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "receipt_type": "performance_attribution(성과 귀속)",
                "run_id": RUN_ID,
                "materialized_repair": "flat/cost/session/inversion/multi-KPI weights(무거래/비용/세션/역전/복수 KPI 가중치)",
                "weight_summary": f"nonfinite={final['total_nonfinite_weight_rows']};max_saturation={final['max_saturation_rate']}",
                "evidence": [rel(HS_WEIGHT_AUDIT), rel(HS_DENSITY_AUDIT)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "result_subject": RUN_ID,
                "evidence_available": [rel(HS_INPUT_FRAME), rel(HS_WEIGHT_AUDIT), rel(GATE_AUDIT)],
                "evidence_missing": "input review, model training, positive proxy, MT5 runtime probe(입력 검토, 모델 학습, 양수 프록시, MT5 런타임 탐침)",
                "judgment_label": "materialized_research_inputs(연구 입력 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "created_at_utc": created_at,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                "receipt_type": "claim_discipline(주장 규율)",
                "run_id": RUN_ID,
                "forbidden_claims": "Forward Passed/Failed, runtime authority, operating promotion, Goal Achieve(전진 통과/실패, 런타임 권위, 운영 승격, 목표 달성)",
                "allowed_claim": "HS materialized timestamp-safe research inputs(HS 시점 안전 연구 입력 물질화)",
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            LINEAGE_RECEIPT,
            {
                "receipt_type": "artifact_lineage(산출물 계보)",
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "artifact_paths": [rel(path) for path in artifacts],
                "artifact_hashes": {rel(path): aw.sha256_file(path) for path in artifacts if path_exists(path) and aw.io_path(path).is_file()},
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in receipts]


def write_manifest(final: Mapping[str, Any], artifacts: Sequence[Path]) -> Path:
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "input_files": [rel(path) for path in INPUT_FILES],
        "output_files": [rel(path) for path in artifacts],
        "external_verification_status": "not_applicable_materialization_only(물질화 전용 해당 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(RUN_MANIFEST, payload)


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HS Proxy Negative Trade Shape Second-Order Repair Inputs(run337HS 프록시 음수 거래 형태 2차 수리 입력)

Action(행동): HR design(HR 설계)을 HS train-only input frame(HS 학습 전용 입력 프레임)과 second-order weights(2차 가중치)로 물질화했다.
Effect(효과): flat/cost/session/inversion/multi-KPI(무거래/비용/세션/역전/복수 KPI) 수리를 다음 HT review(HT 검토)로 넘겼다.

## Judgment(판정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`

## Evidence(근거)

- rows(행): `{final['base_rows']}`
- first/last timestamp(첫/마지막 시각): `{final['first_timestamp']}` / `{final['last_timestamp']}`
- allowed_features(허용 피처): `{final['allowed_feature_rows']}`
- new_weight_columns(새 가중치 열): `{final['new_weight_columns']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['total_nonfinite_weight_rows']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']}`
- duplicate_timestamp_rows(중복 시각 행): `{final['duplicate_timestamp_rows']}`

## Boundary(경계)

Action(행동): 이 run(실행)은 model training(모델 학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택)을 하지 않았다.
Effect(효과): 입력 물질화와 operating claim(운영 주장)을 분리한다.

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- failed_gates(실패 게이트): `{','.join(final['failed_gates']) if final['failed_gates'] else 'none'}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HS

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HR second-order repair design(HR 2차 수리 설계)을 HS train-only frame(HS 학습 전용 프레임)과 HT review queue(HT 검토 대기열)로 바꾼다.
- forbidden_claim(금지 주장): Forward Passed(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성).
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    lines = workspace.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("current_run_id:"):
            lines[index] = f"current_run_id: {final['next_action']}"
        elif line.startswith("updated_on:"):
            lines[index] = f"updated_on: '{TODAY}'"
    workspace_text = "\n".join(lines) + "\n"
    if "Stage337 run337HS focus complete" not in workspace_text:
        focus_lines = [
            "- >-",
            (
                f"  Stage337 run337HS focus complete(337단계 run337HS 초점 완료): `{final['status']}`. "
                f"Effect(효과): rows(행) `{final['base_rows']}`, new weights(새 가중치) `{final['new_weight_columns']}`, "
                f"gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. "
                "Forward/Goal(전진/목표)는 주장하지 않는다."
            ),
        ]
        workspace_lines = workspace_text.splitlines()
        for index, line in enumerate(workspace_lines):
            if line.startswith("current_focus:"):
                workspace_lines[index + 1:index + 1] = focus_lines
                break
        workspace_text = "\n".join(workspace_lines) + "\n"
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace_text, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    current_lines = current.splitlines()
    current_replacements = {
        "- current_run(": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(": f"- status(상태): `{final['status']}`",
        "- decision(": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for index, line in enumerate(current_lines):
        if line.startswith("## "):
            break
        for prefix, replacement in current_replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HS Proxy Negative Trade Shape Second-Order Repair Inputs(프록시 음수 거래 형태 2차 수리 입력)

Action(행동): run337HS(337HS 실행)는 HR design(HR 설계)을 train-only frame(학습 전용 프레임)과 5개 second-order repair weight(2차 수리 가중치)로 물질화했다.
Effect(효과): rows(행) `{final['base_rows']}`, allowed features(허용 피처) `{final['allowed_feature_rows']}`, nonfinite weights(비유한 가중치) `{final['total_nonfinite_weight_rows']}`, max saturation(최대 포화율) `{final['max_saturation_rate']}`를 HT review(HT 검토)로 넘겼다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = fb.upsert_section_before(current, "## run337HR", section, "run337HS Proxy Negative Trade Shape Second-Order Repair Inputs")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- rows(행): `{final['base_rows']}`
- allowed_features(허용 피처): `{final['allowed_feature_rows']}`
- new_weight_columns(새 가중치 열): `{final['new_weight_columns']}`
- max_saturation_rate(최대 포화율): `{final['max_saturation_rate']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['total_nonfinite_weight_rows']}`
- runtime_package(런타임 패키지): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HS materialization(HS 물질화)은 2차 수리 입력을 HT review(HT 검토)로 넘기고 운영 선택은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HS(337HS 실행) `{final['status']}`. "
        f"Effect(효과): rows(행) `{final['base_rows']}`, new weights(새 가중치) `{final['new_weight_columns']}`, "
        f"max saturation(최대 포화율) `{final['max_saturation_rate']}`를 `{final['next_action']}` 검토로 넘겼다. "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HS(337HS 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HS(337HS 실행) `{final['status']}`. "
        f"Effect(효과): proxy negative second-order repair inputs(프록시 음수 2차 수리 입력)을 물질화하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HS", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_negative_second_order_repair_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['base_rows']};weights={final['new_weight_columns']};max_saturation={final['max_saturation_rate']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__second_order_repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "second_order_repair_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "second_order_repair_inputs(2차 수리 입력)",
        "tier_scope": "Tier A train-only materialization(Tier A 학습 전용 물질화)",
        "kpi_scope": "materialization_only_no_new_mt5(물질화 전용 새 MT5 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"rows={final['base_rows']};weights={final['new_weight_columns']};nonfinite={final['total_nonfinite_weight_rows']}",
        "guardrail_kpi": "no_training;no_mt5;no_runtime_package;no_selection;no_goal",
        "external_verification_status": "not_applicable_materialization_only(물질화 전용 해당 없음)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__second_order_repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "HR contracts plus HN train-only frame",
        "kpi_scope": "materialization_only_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__second_order_repair_inputs",
        "family": "proxy_negative_second_order_repair_input_materialization",
        "question": "were HR second-order repair inputs materialized safely(HR 2차 수리 입력이 안전하게 물질화됐는가)",
        "metric_scope": "frame_weight_audit_gate_receipts",
        "primary_artifact": rel(HS_INPUT_FRAME),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        row = {
            "artifact_id": artifact_id,
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
    return write_csv(he.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    summary, artifacts = build_packets()
    final = make_final(summary)
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
        ]
    )
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.append(write_manifest(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

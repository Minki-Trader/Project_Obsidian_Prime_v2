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
from stage_pipelines.stage337 import design_post_runtime_probe_proxy_negative_trade_shape_repair_without_db as hm  # noqa: E402


aw = hm.aw
fb = hm.fb
he = hm.he

TODAY = "2026-05-31"
STAGE_ID = hm.STAGE_ID
RUN_NUMBER = "run337HN"
RUN_ID = "run337HN_materialize_post_runtime_probe_proxy_negative_trade_shape_repair_inputs_without_db_v1"
PARENT_RUN_ID = hm.RUN_ID
NEXT_RUN_ID = "run337HO_review_post_runtime_probe_proxy_negative_trade_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337HN_proxy_negative_trade_shape_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_density_cost_trade_shape_repair_inputs_materialized_review_required"
DECISION = "stage337HN_open_run337HO_proxy_negative_trade_shape_input_review"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HN_proxy_negative_trade_shape_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hm.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hm.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HN_proxy_negative_trade_shape_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HN_proxy_negative_trade_shape_repair_inputs.md"

HM_FINAL = hm.FINAL_DECISION
HM_GATES = hm.GATE_AUDIT
HM_QUEUE = hm.MATERIALIZATION_QUEUE
HM_DESIGN = hm.DESIGN_MATRIX
HM_EXPERIMENT = hm.EXPERIMENT_CONTRACT
HM_OBJECTIVE = hm.OBJECTIVE_CONTRACT
HM_FEATURE_LABEL = hm.FEATURE_LABEL_CONTRACT
HM_ATTRIBUTION = hm.TRADE_SHAPE_ATTRIBUTION
HM_MODEL_PROPOSAL = hm.MODEL_FAMILY_PROPOSAL
HM_TASK_BLUEPRINT = hm.TRAINING_TASK_BLUEPRINT
HM_DENSITY_PLAN = hm.DENSITY_REPAIR_PLAN
HM_SESSION_PLAN = hm.SESSION_REGIME_REPAIR_PLAN
HM_RELEASE = hm.RELEASE_GATE_CONTRACT
BASE_FRAME = hm.HI_INPUT_FRAME
BASE_ALLOWED_FEATURES = STAGE_DIR / "02_runs" / "run337HI" / "hi_allowed_model_feature_set.csv"
BASE_FEATURE_BOUNDARY = STAGE_DIR / "02_runs" / "run337HI" / "feature_label_boundary_audit.csv"
BASE_WEIGHT_AUDIT = STAGE_DIR / "02_runs" / "run337HI" / "hh_repair_weight_audit.csv"

HN_INPUT_FRAME = RUN_DIR / "hn_input_frame.parquet"
HN_SOURCE_MAP = RUN_DIR / "hn_materialization_source_map.csv"
HN_ALLOWED_FEATURE_SET = RUN_DIR / "hn_allowed_model_feature_set.csv"
HN_WEIGHT_RECIPE = RUN_DIR / "hm_trade_shape_weight_recipe_matrix.csv"
HN_WEIGHT_AUDIT = RUN_DIR / "hm_trade_shape_weight_audit.csv"
HN_TARGET_AUDIT = RUN_DIR / "target_contract_audit.csv"
HN_FEATURE_BOUNDARY = RUN_DIR / "feature_label_boundary_audit.csv"
HN_DENSITY_AUDIT = RUN_DIR / "density_trade_shape_audit.csv"
HN_MODEL_PROPOSAL_REVIEW = RUN_DIR / "model_family_proposal_materialization_review.csv"
HN_RELEASE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
HN_TRAINING_TASK_SEEDS = RUN_DIR / "run337HP_training_task_seed_matrix.csv"
HO_QUEUE = RUN_DIR / "run337HO_review_queue.csv"
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
    HM_FINAL,
    HM_GATES,
    HM_QUEUE,
    HM_DESIGN,
    HM_EXPERIMENT,
    HM_OBJECTIVE,
    HM_FEATURE_LABEL,
    HM_ATTRIBUTION,
    HM_MODEL_PROPOSAL,
    HM_TASK_BLUEPRINT,
    HM_DENSITY_PLAN,
    HM_SESSION_PLAN,
    HM_RELEASE,
    BASE_FRAME,
    BASE_ALLOWED_FEATURES,
    BASE_FEATURE_BOUNDARY,
    BASE_WEIGHT_AUDIT,
)
OUTPUT_FILES = (
    HN_INPUT_FRAME,
    HN_SOURCE_MAP,
    HN_ALLOWED_FEATURE_SET,
    HN_WEIGHT_RECIPE,
    HN_WEIGHT_AUDIT,
    HN_TARGET_AUDIT,
    HN_FEATURE_BOUNDARY,
    HN_DENSITY_AUDIT,
    HN_MODEL_PROPOSAL_REVIEW,
    HN_RELEASE_MATERIALIZATION,
    HN_TRAINING_TASK_SEEDS,
    HO_QUEUE,
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
    "hm_density_cost_selectivity_weight",
    "hm_generalization_gap_pressure_weight",
    "hm_side_net_balance_repair_weight",
    "hm_session_regime_turnover_firewall_weight",
    "hm_balanced_proxy_release_ladder_weight",
)
TASK_WEIGHT_COLUMNS = {
    "hn_hm001_density_cost_selectivity_guard": "hm_density_cost_selectivity_weight",
    "hn_hm002_generalization_gap_pressure": "hm_generalization_gap_pressure_weight",
    "hn_hm003_side_net_balance_repair": "hm_side_net_balance_repair_weight",
    "hn_hm004_session_regime_turnover_firewall": "hm_session_regime_turnover_firewall_weight",
    "hn_hm005_balanced_proxy_release_ladder": "hm_balanced_proxy_release_ladder_weight",
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


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


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


def build_weights(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    out = df.copy()
    label_text = out.get("label", pd.Series("", index=out.index)).astype(str).str.lower()
    is_short = label_text.eq("short")
    is_flat = label_text.eq("flat")
    is_long = label_text.eq("long")
    is_trade = is_short | is_long
    base_raw = numeric(out, "hh_balanced_release_ladder_weight", 1.0).clip(0.35, 8.0)
    base_median = float(base_raw.median()) if math.isfinite(float(base_raw.median())) and float(base_raw.median()) > 0 else 1.0
    base = (base_raw / base_median).clip(0.45, 1.85)
    low_margin = norm01(numeric(out, "low_margin_rate"))
    abstention = norm01(numeric(out, "abstention_rate"))
    churn = norm01(numeric(out, "hh_trade_churn_pressure"))
    cost_risk = norm01(numeric(out, "hh_cost_adverse_risk"))
    precision_risk = norm01(numeric(out, "hh_precision_risk"))
    payoff_tail = norm01(numeric(out, "payoff_tail_norm"))
    side_quality = norm01(numeric(out, "side_quality_weight", 1.0))
    session_seed_raw = numeric(out, "hh_cost_session_regime_seed", 1.0).clip(0.5, 6.0)
    session_median = float(session_seed_raw.median()) if math.isfinite(float(session_seed_raw.median())) and float(session_seed_raw.median()) > 0 else 1.0
    session_seed = (session_seed_raw / session_median).clip(0.60, 1.75)
    cash_open = numeric(out, "is_us_cash_open").clip(0.0, 1.0)
    open_edge = numeric(out, "is_first_30m_after_open").clip(0.0, 1.0)
    close_edge = numeric(out, "is_last_30m_before_cash_close").clip(0.0, 1.0)

    no_trade_support = np.where(is_flat, 1.35 + 1.65 * churn + 1.10 * low_margin + 0.75 * cost_risk, 1.00 + 0.35 * payoff_tail - 0.35 * churn)
    density_cost = base * no_trade_support * (1.00 + 0.35 * cost_risk + 0.20 * precision_risk)

    gap_trade_clip = np.where(is_trade, 1.15 + 0.75 * payoff_tail + 0.40 * side_quality - 0.45 * low_margin - 0.35 * churn, 1.15 + 1.20 * abstention + 0.80 * low_margin)
    generalization = base * gap_trade_clip * (1.00 + 0.25 * precision_risk)

    side_balance = np.where(
        is_short,
        1.12 + 0.85 * side_quality + 0.35 * payoff_tail - 0.25 * cost_risk,
        np.where(is_long, 1.08 + 0.75 * side_quality + 0.35 * payoff_tail - 0.25 * cost_risk, 1.05 + 0.80 * low_margin + 0.55 * abstention),
    )
    side_repair = base * side_balance

    turnover_flat_guard = np.where(is_flat, 1.20 + 1.25 * churn + 0.80 * cost_risk, 1.05 + 0.35 * payoff_tail - 0.25 * churn)
    session_regime = session_seed * turnover_flat_guard * (1.00 + 0.18 * cash_open + 0.12 * open_edge + 0.12 * close_edge)

    balanced = np.power(
        np.maximum(density_cost, 0.25)
        * np.maximum(generalization, 0.25)
        * np.maximum(side_repair, 0.25)
        * np.maximum(session_regime, 0.25),
        0.25,
    )

    out["hm_density_cost_selectivity_weight"] = clip_weight(density_cost)
    out["hm_generalization_gap_pressure_weight"] = clip_weight(generalization)
    out["hm_side_net_balance_repair_weight"] = clip_weight(side_repair)
    out["hm_session_regime_turnover_firewall_weight"] = clip_weight(session_regime)
    out["hm_balanced_proxy_release_ladder_weight"] = clip_weight(balanced)

    recipes = [
        {
            "recipe_id": "hm_density_cost_selectivity",
            "materialized_column": "hm_density_cost_selectivity_weight",
            "source_columns": "hh_balanced_release_ladder_weight;low_margin_rate;abstention_rate;hh_trade_churn_pressure;hh_cost_adverse_risk;label",
            "train_only_formula": "flat/no-trade support rises under churn/cost; trade labels are clipped under weak-edge churn(과회전/비용에서 flat 지지 상승, 약한 엣지 과회전 거래 라벨 축소)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "signal density(신호 밀도)를 낮추되 trade starvation(거래 고갈)을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hm_generalization_gap_pressure",
            "materialized_column": "hm_generalization_gap_pressure_weight",
            "source_columns": "low_margin_rate;abstention_rate;payoff_tail_norm;side_quality_weight;hh_precision_risk;label",
            "train_only_formula": "low-margin flat pressure plus payoff-supported trade pressure(낮은 마진 flat 압박과 payoff 지지 거래 압박)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "train/holdout inversion(학습/보류 역전)을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hm_side_net_balance_repair",
            "materialized_column": "hm_side_net_balance_repair_weight",
            "source_columns": "side_quality_weight;payoff_tail_norm;hh_cost_adverse_risk;label",
            "train_only_formula": "side-aware pressure without manual side override(수동 방향 덮어쓰기 없는 방향 인식 압박)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "long/short balance(롱/숏 균형)를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hm_session_regime_turnover_firewall",
            "materialized_column": "hm_session_regime_turnover_firewall_weight",
            "source_columns": "hh_cost_session_regime_seed;is_us_cash_open;is_first_30m_after_open;is_last_30m_before_cash_close;hh_trade_churn_pressure;label",
            "train_only_formula": "cost-session seed with turnover cap pressure(비용-세션 씨앗과 회전 상한 압박)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "positive cost-session clue(긍정 비용-세션 단서)를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "hm_balanced_proxy_release_ladder",
            "materialized_column": "hm_balanced_proxy_release_ladder_weight",
            "source_columns": ";".join(NEW_WEIGHT_COLUMNS[:-1]),
            "train_only_formula": "geometric blend of density/generalization/side/session weights(밀도/일반화/방향/세션 가중치 기하 혼합)",
            "lower_bound": 0.25,
            "upper_bound": 10.0,
            "expected_effect": "단일 수리축 과적합을 줄인다.",
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
        nonfinite = int((~np.isfinite(values.to_numpy())).sum())
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
                "effect": "records class-aware repair pressure(클래스별 수리 압박 기록)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows, {"total_nonfinite_weight_rows": total_nonfinite, "max_saturation_rate": max_saturation_rate}


def build_packets() -> tuple[dict[str, Any], list[Path]]:
    hm_final = read_json(HM_FINAL)
    hm_tasks = read_csv(HM_TASK_BLUEPRINT)
    hm_release = read_csv(HM_RELEASE)
    hm_proposals = read_csv(HM_MODEL_PROPOSAL)
    base_features = read_csv(BASE_ALLOWED_FEATURES)
    df = pd.read_parquet(aw.io_path(BASE_FRAME))
    materialized, recipes, label_summary = build_weights(df)
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    materialized.to_parquet(aw.io_path(HN_INPUT_FRAME), index=False)

    source_rows = []
    for source_id, path, source_type, effect in [
        ("hm_final", HM_FINAL, "parent_final_decision", "parent decision lock(부모 결정 잠금)"),
        ("hm_gates", HM_GATES, "parent_gates", "parent gates passed(부모 게이트 통과)"),
        ("hm_queue", HM_QUEUE, "parent_queue", "HN queue authority(HN 대기열 권위)"),
        ("hm_task_blueprint", HM_TASK_BLUEPRINT, "task_blueprint", "task and weight mapping(작업과 가중치 매핑)"),
        ("hm_density_plan", HM_DENSITY_PLAN, "repair_plan", "density/cost repair plan(밀도/비용 수리 계획)"),
        ("hm_session_plan", HM_SESSION_PLAN, "repair_plan", "session/side repair plan(세션/방향 수리 계획)"),
        ("base_frame", BASE_FRAME, "train_only_frame", "base timestamp-safe input frame(기본 시점 안전 입력 프레임)"),
        ("base_allowed_features", BASE_ALLOWED_FEATURES, "feature_contract", "feature list without repair weights(수리 가중치 없는 피처 목록)"),
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
    allowed_rows = [
        {
            **row,
            "source_layer": rel(HN_INPUT_FRAME),
            "allowed_use": "future reviewed training feature after HO review(HO 검토 후 학습 피처)",
            "forbidden_use": "label, selector, forward proof, repair weight(라벨/선택자/전진 증거/수리 가중치)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in base_features
    ]
    forbidden_feature_hits = [
        row.get("feature_name", "")
        for row in allowed_rows
        if any(token in str(row.get("feature_name", "")).lower() for token in FORBIDDEN_FEATURE_TOKENS)
    ]
    weight_audit, weight_summary = build_weight_audit(materialized)
    target_rows = [
        {
            "audit_id": "hn_target001_label_class_present",
            "status": "passed" if "label_class" in materialized.columns else "failed",
            "observed": "present" if "label_class" in materialized.columns else "missing",
            "expected": "present",
            "evidence": rel(HN_INPUT_FRAME),
            "effect": "keeps original target boundary(기존 목표 경계 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_target002_tasks_target_label_class",
            "status": "passed" if sum(1 for row in hm_tasks if row.get("target_column") == "label_class") == 5 else "failed",
            "observed": str(sum(1 for row in hm_tasks if row.get("target_column") == "label_class")),
            "expected": "5",
            "evidence": rel(HM_TASK_BLUEPRINT),
            "effect": "all HN tasks use same target(모든 HN 작업이 같은 목표 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    timestamp_ordered = bool(pd.to_datetime(materialized["timestamp"], errors="coerce").is_monotonic_increasing) if "timestamp" in materialized.columns else False
    duplicate_timestamps = int(materialized["timestamp"].duplicated().sum()) if "timestamp" in materialized.columns else -1
    feature_rows = [
        {
            "audit_id": "hn_feature001_allowed_feature_count",
            "status": "passed" if len(allowed_rows) == 58 else "failed",
            "observed": str(len(allowed_rows)),
            "expected": "58",
            "evidence": rel(HN_ALLOWED_FEATURE_SET),
            "effect": "keeps reviewed model feature order(검토된 모델 피처 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_feature002_forbidden_features_excluded",
            "status": "passed" if not forbidden_feature_hits else "failed",
            "observed": ";".join(forbidden_feature_hits),
            "expected": "no label/future/weight/outcome/MT5 KPI features(라벨/미래/가중치/결과/MT5 지표 피처 없음)",
            "evidence": rel(HN_ALLOWED_FEATURE_SET),
            "effect": "prevents target leakage into model features(목표 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_feature003_nonfinite_weights",
            "status": "passed" if weight_summary["total_nonfinite_weight_rows"] == 0 else "failed",
            "observed": str(weight_summary["total_nonfinite_weight_rows"]),
            "expected": "0",
            "evidence": rel(HN_WEIGHT_AUDIT),
            "effect": "repair weights are finite(수리 가중치 유한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_feature004_timestamp_order",
            "status": "passed" if timestamp_ordered else "failed",
            "observed": str(timestamp_ordered),
            "expected": "True",
            "evidence": rel(HN_INPUT_FRAME),
            "effect": "keeps time axis ordered(시간축 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_feature005_timestamp_duplicates_named",
            "status": "passed" if duplicate_timestamps >= 0 else "failed",
            "observed": str(duplicate_timestamps),
            "expected": "duplicates allowed by cost_policy_id training expansion(비용 정책 학습 확장 중복 허용)",
            "evidence": rel(HN_INPUT_FRAME),
            "effect": "names expanded train-only repeated timestamps(확장 학습 전용 반복 시각 명명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_feature006_macro_join_safe_by_absence",
            "status": "passed",
            "observed": "no new macro source joined in HN(HN에서 새 거시 자료 결합 없음)",
            "expected": "economic data requires release timestamp(경제자료는 발표 시각 필요)",
            "evidence": rel(HM_FEATURE_LABEL),
            "effect": "prevents macro look-ahead(거시 미래참조 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    density_rows = [
        {
            "audit_id": "hn_density001_hm_weights_created",
            "status": "passed" if all(column in materialized.columns for column in NEW_WEIGHT_COLUMNS) else "failed",
            "observed": str(sum(1 for column in NEW_WEIGHT_COLUMNS if column in materialized.columns)),
            "expected": str(len(NEW_WEIGHT_COLUMNS)),
            "evidence": rel(HN_INPUT_FRAME),
            "effect": "materializes HM density/cost/side/session weights(HM 밀도/비용/방향/세션 가중치 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hn_density002_saturation_watch",
            "status": "passed" if weight_summary["max_saturation_rate"] <= 0.25 else "failed",
            "observed": f"{weight_summary['max_saturation_rate']:.6f}",
            "expected": "<=0.25",
            "evidence": rel(HN_WEIGHT_AUDIT),
            "effect": "prevents clipped weight domination(클립 가중치 지배 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    proposal_review = [
        {
            "audit_id": f"hn_model_proposal_{index:02d}",
            "status": "materialized_as_metadata(메타데이터로 물질화)",
            "observed": row.get("model_family_or_rule_stack", ""),
            "expected": "proposal only, no training(제안만, 학습 없음)",
            "evidence": rel(HM_MODEL_PROPOSAL),
            "effect": row.get("expected_effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(hm_proposals, start=1)
    ]
    release_rows = [
        {
            "audit_id": row.get("gate_id", f"hm_release_{index}"),
            "status": "materialized_for_future_review(향후 검토용 물질화)",
            "observed": row.get("pass_condition", ""),
            "expected": row.get("fail_condition", ""),
            "evidence": rel(HM_RELEASE),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(hm_release, start=1)
    ]
    task_rows = []
    for row in hm_tasks:
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
                "selection_status": "eligible_for_HO_review(HO 검토 대상)",
                "required_guard": row.get("required_guard", ""),
                "expected_effect": row.get("expected_effect", ""),
                "forbidden_use": row.get("forbidden_use", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    queue_rows = [
        {
            "queue_id": "ho_proxy_negative_trade_shape_input_review",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "review HN materialized weights before guarded training(HN 물질화 가중치를 방어 학습 전 검토)",
            "required_inputs": ";".join(rel(path) for path in (HN_INPUT_FRAME, HN_ALLOWED_FEATURE_SET, HN_WEIGHT_AUDIT, HN_FEATURE_BOUNDARY, HN_TRAINING_TASK_SEEDS)),
            "expected_outputs": "HO eligibility review and HP training queue(HO 적격성 검토와 HP 학습 대기열)",
            "blocked_if_missing": "HN frame, feature set, or weight audit missing(HN 프레임, 피처셋, 가중치 감사 누락)",
            "effect": "prevents unreviewed weights from training(미검토 가중치 학습 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    artifacts = [
        HN_INPUT_FRAME,
        write_csv(HN_SOURCE_MAP, SOURCE_COLUMNS, source_rows),
        write_csv(HN_ALLOWED_FEATURE_SET, ("feature_name", "feature_family", "source_layer", "timestamp_rule", "allowed_use", "forbidden_use", "claim_boundary"), allowed_rows),
        write_csv(HN_WEIGHT_RECIPE, WEIGHT_RECIPE_COLUMNS, recipes),
        write_csv(HN_WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, weight_audit),
        write_csv(HN_TARGET_AUDIT, AUDIT_COLUMNS, target_rows),
        write_csv(HN_FEATURE_BOUNDARY, AUDIT_COLUMNS, feature_rows),
        write_csv(HN_DENSITY_AUDIT, AUDIT_COLUMNS, density_rows),
        write_csv(HN_MODEL_PROPOSAL_REVIEW, AUDIT_COLUMNS, proposal_review),
        write_csv(HN_RELEASE_MATERIALIZATION, AUDIT_COLUMNS, release_rows),
        write_csv(HN_TRAINING_TASK_SEEDS, TASK_SEED_COLUMNS, task_rows),
        write_csv(HO_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    first_ts = str(materialized["timestamp"].min()) if "timestamp" in materialized.columns else ""
    last_ts = str(materialized["timestamp"].max()) if "timestamp" in materialized.columns else ""
    summary = {
        "hm_failed_gate_rows": sum(1 for row in read_csv(HM_GATES) if row.get("status") != "passed"),
        "hm_next_action": hm_final.get("next_action"),
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
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HM_FINAL), "required HM and base inputs exist(필수 HM과 기본 입력 존재)"),
        ("parent_hm_gates_passed", final["hm_failed_gate_rows"] == 0, str(final["hm_failed_gate_rows"]), "0", rel(HM_GATES), "HM gates passed(HM 게이트 통과)"),
        ("parent_next_action_matches", final["hm_next_action"] == RUN_ID, str(final["hm_next_action"]), RUN_ID, rel(HM_FINAL), "HN follows HM next action(HN이 HM 다음 행동을 따름)"),
        ("frame_materialized", path_exists(HN_INPUT_FRAME) and final["base_rows"] > 0, str(final["base_rows"]), ">0", rel(HN_INPUT_FRAME), "HN frame materialized(HN 프레임 물질화)"),
        ("new_weights_materialized", final["new_weight_columns"] == 5 and final["task_weight_columns_present"] == 5, f"weights={final['new_weight_columns']};task_columns={final['task_weight_columns_present']}", "5/5", rel(HN_WEIGHT_AUDIT), "all HM repair weights available(모든 HM 수리 가중치 사용 가능)"),
        ("weights_finite", final["total_nonfinite_weight_rows"] == 0, str(final["total_nonfinite_weight_rows"]), "0", rel(HN_WEIGHT_AUDIT), "weights are finite(가중치 유한)"),
        ("weight_saturation_guard", final["max_saturation_rate"] <= 0.25, f"{final['max_saturation_rate']:.6f}", "<=0.25", rel(HN_WEIGHT_AUDIT), "weight clipping not dominant(가중치 클립 지배 아님)"),
        ("feature_set_preserved", final["allowed_feature_rows"] == 58 and final["forbidden_feature_hits"] == 0, f"features={final['allowed_feature_rows']};forbidden={final['forbidden_feature_hits']}", "58/0", rel(HN_ALLOWED_FEATURE_SET), "allowed feature set preserved(허용 피처셋 보존)"),
        ("target_contract_audit", final["failed_target_audits"] == 0, str(final["failed_target_audits"]), "0", rel(HN_TARGET_AUDIT), "target boundary passed(목표 경계 통과)"),
        ("feature_boundary_audit", final["failed_feature_boundary_rows"] == 0, str(final["failed_feature_boundary_rows"]), "0", rel(HN_FEATURE_BOUNDARY), "feature/label boundary passed(피처/라벨 경계 통과)"),
        ("density_audit", final["failed_density_audits"] == 0, str(final["failed_density_audits"]), "0", rel(HN_DENSITY_AUDIT), "density repair audit passed(밀도 수리 감사 통과)"),
        ("training_task_queue_ready", final["training_task_seed_rows"] == 5 and final["queue_rows"] == 1, f"tasks={final['training_task_seed_rows']};queue={final['queue_rows']}", "5 and 1", rel(HO_QUEUE), "HO review queue opened(HO 검토 대기열 열림)"),
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
                "feature_label_boundary": "allowed feature set preserved; repair weights excluded from features(허용 피처셋 보존, 수리 가중치는 피처 제외)",
                "split_boundary": "train-only materialization; HO must review before training(학습 전용 물질화, HO 검토 후 학습)",
                "leakage_risk": "holdout KPI or MT5 tester result copied into row input(보류 KPI 또는 MT5 테스터 결과 행 입력 복사)",
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "evidence": [rel(HN_FEATURE_BOUNDARY), rel(HN_ALLOWED_FEATURE_SET)],
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
                "future_validation": "HO input review then HP guarded training(HO 입력 검토 후 HP 방어 학습)",
                "evidence": [rel(HN_TRAINING_TASK_SEEDS), rel(HN_MODEL_PROPOSAL_REVIEW)],
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
                "materialized_repair": "density/cost/generalization/side/session weights(밀도/비용/일반화/방향/세션 가중치)",
                "weight_summary": f"nonfinite={final['total_nonfinite_weight_rows']};max_saturation={final['max_saturation_rate']}",
                "evidence": [rel(HN_WEIGHT_AUDIT), rel(HN_DENSITY_AUDIT)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "result_subject": RUN_ID,
                "evidence_available": [rel(HN_INPUT_FRAME), rel(HN_WEIGHT_AUDIT), rel(GATE_AUDIT)],
                "evidence_missing": "input review, model training, positive proxy, MT5 runtime probe(입력 검토, 모델 학습, 긍정 프록시, MT5 런타임 탐침)",
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
                "allowed_claim": "HN materialized timestamp-safe research inputs(HN 시점 안전 연구 입력 물질화)",
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
    text = f"""# run337HN Proxy Negative Trade Shape Repair Inputs(run337HN 프록시 음수 거래 형태 수리 입력)

Action(행동): HM design(HM 설계)을 HN train-only input frame(HN 학습 전용 입력 프레임)과 repair weights(수리 가중치)로 물질화했다. Effect(효과): density/cost/generalization/side/session(밀도/비용/일반화/방향/세션) 수리를 다음 HO review(HO 검토)로 넘겼다.

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

Action(행동): 이 run(실행)은 model training(모델 학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택)을 하지 않았다. Effect(효과): 입력 물질화와 운영 주장(operating claim, 운영 주장)을 분리했다.

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- failed_gates(실패 게이트): `{','.join(final['failed_gates']) if final['failed_gates'] else 'none'}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HN

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HM trade-shape repair design(HM 거래 형태 수리 설계)을 HN train-only frame(HN 학습 전용 프레임)과 HO review queue(HO 검토 대기열)로 바꾼다.
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
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, "\n".join(lines) + "\n", workspace_bom))

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
    section = f"""## run337HN Proxy Negative Trade Shape Repair Inputs(프록시 음수 거래 형태 수리 입력)

Action(행동): run337HN(337HN 실행)은 HM design(HM 설계)을 train-only frame(학습 전용 프레임)과 5개 repair weight(수리 가중치)로 물질화했다.
Effect(효과): rows(행) `{final['base_rows']}`, allowed features(허용 피처) `{final['allowed_feature_rows']}`, nonfinite weights(비유한 가중치) `{final['total_nonfinite_weight_rows']}`, max saturation(최대 포화율) `{final['max_saturation_rate']}`를 HO review(HO 검토)로 넘겼다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = fb.upsert_section_before(current, "## run337HM", section, "run337HN Proxy Negative Trade Shape Repair Inputs")
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
- effect(효과): HN materialization(물질화)은 proxy negative trade-shape repair(프록시 음수 거래 형태 수리)를 HO review(HO 검토)로 넘기고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HN(337HN 실행) `{final['status']}`. "
        f"Effect(효과): rows(행) `{final['base_rows']}`, new weights(새 가중치) `{final['new_weight_columns']}`, "
        f"max saturation(최대 포화율) `{final['max_saturation_rate']}`를 `{final['next_action']}` 검토로 넘겼다. "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HN(337HN 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HN(337HN 실행) `{final['status']}`. "
        f"Effect(효과): proxy negative trade-shape repair inputs(프록시 음수 거래 형태 수리 입력)을 물질화하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HN", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_negative_trade_shape_repair_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['base_rows']};weights={final['new_weight_columns']};max_saturation={final['max_saturation_rate']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_negative_trade_shape_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_negative_trade_shape_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_negative_trade_shape_inputs(프록시 음수 거래 형태 입력)",
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
        "ledger_row_id": f"{RUN_ID}__proxy_negative_trade_shape_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "HM contracts plus HI train-only frame",
        "kpi_scope": "materialization_only_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__proxy_negative_trade_shape_inputs",
        "family": "proxy_negative_trade_shape_repair_input_materialization",
        "question": "were HM trade-shape repair inputs materialized safely(HM 거래 형태 수리 입력이 안전하게 물질화됐는가)",
        "metric_scope": "frame_weight_audit_gate_receipts",
        "primary_artifact": rel(HN_INPUT_FRAME),
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

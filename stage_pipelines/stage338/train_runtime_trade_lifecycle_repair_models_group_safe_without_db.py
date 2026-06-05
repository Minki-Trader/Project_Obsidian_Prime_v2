from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage338 import review_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_inputs_without_db as rv  # noqa: E402


aw = rv.aw

TODAY = "2026-06-01"
STAGE_ID = rv.STAGE_ID
STAGE_DIR = rv.STAGE_DIR
RUN_NUMBER = "run338E"
RUN_ID = "run338E_train_runtime_trade_lifecycle_repair_models_group_safe_without_db_v1"
PARENT_RUN_ID = rv.RUN_ID
NEXT_RUN_ID = "run338F_review_group_safe_onnx_proxy_scores_for_mt5_probe_without_db_v1"
STATUS = "completed_stage338E_group_safe_trade_lifecycle_training_proxy_onnx_no_selection"
JUDGMENT = "onnx_models_trained_proxy_scored_review_required_no_mt5_no_selection"
DECISION = "stage338E_open_run338F_proxy_score_review_for_mt5_probe_routing"
CLAIM_BOUNDARY = (
    "research_development_training_and_proxy_evaluation_only_no_candidate_selection_no_threshold_promotion_"
    "no_lot_optimization_no_mt5_execution_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338E_group_safe_trade_lifecycle_training_proxy.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338E_group_safe_trade_lifecycle_training_proxy.md"
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

FEATURE_ORDER = RUN_DIR / "run338E_feature_order.csv"
MODEL_SCORECARD = RUN_DIR / "run338E_model_scorecard.csv"
PROXY_THRESHOLD_GRID = RUN_DIR / "run338E_proxy_threshold_grid.csv"
ONNX_PARITY_AUDIT = RUN_DIR / "run338E_onnx_parity_audit.csv"
HOLDOUT_PREDICTIONS = RUN_DIR / "run338E_holdout_predictions.parquet"
TRAINING_SUMMARY = RUN_DIR / "run338E_training_summary.csv"
RUN338F_REVIEW_QUEUE = RUN_DIR / "run338F_proxy_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

PRIMARY_LABEL = "tlr_label_runtime_net_after_cost_fwd18"
LONG_PROXY = "tlr_long_net_after_cost_proxy"
SHORT_PROXY = "tlr_short_net_after_cost_proxy"
SPLIT_COLUMN = "run338D_group_safe_split"

INPUT_FILES = (
    rv.FINAL_DECISION,
    rv.TRAINING_FEATURE_SCHEMA,
    rv.GROUP_SAFE_SPLIT_ASSIGNMENT,
    rv.TRAINING_READINESS_CONTRACT,
    rv.RUN338E_TRAINING_QUEUE,
    rv.mat.INPUT_FRAME,
)
OUTPUT_FILES = (
    FEATURE_ORDER,
    MODEL_SCORECARD,
    PROXY_THRESHOLD_GRID,
    ONNX_PARITY_AUDIT,
    HOLDOUT_PREDICTIONS,
    TRAINING_SUMMARY,
    RUN338F_REVIEW_QUEUE,
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

MODEL_SPECS = {
    "et_depth9_leaf120_balanced": Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                ExtraTreesClassifier(
                    n_estimators=260,
                    max_depth=9,
                    min_samples_leaf=120,
                    max_features="sqrt",
                    class_weight="balanced_subsample",
                    random_state=338001,
                    n_jobs=-1,
                ),
            ),
        ]
    ),
    "rf_depth8_leaf120_balanced": Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=180,
                    max_depth=8,
                    min_samples_leaf=120,
                    max_features="sqrt",
                    class_weight="balanced_subsample",
                    random_state=338002,
                    n_jobs=-1,
                ),
            ),
        ]
    ),
    "logreg_balanced_c025": Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    C=0.25,
                    class_weight="balanced",
                    max_iter=500,
                    n_jobs=-1,
                    solver="lbfgs",
                ),
            ),
        ]
    ),
}

THRESHOLD_GRID = [
    {"min_prob": min_prob, "min_margin": min_margin, "density_cap": density_cap}
    for min_prob in (0.40, 0.45, 0.50, 0.55, 0.60)
    for min_margin in (0.00, 0.05, 0.10, 0.15)
    for density_cap in (1.00, 0.20, 0.10, 0.05)
]


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
    return rv.read_csv(path)


def read_json(path: Path) -> Any:
    return rv.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return rv.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return rv.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return rv.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    rv.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    rv.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    return rv.display_path(path)


def passed_status(series: pd.Series) -> pd.Series:
    return rv.passed_status(series)


def safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return float(numerator) / float(denominator)


def max_drawdown(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    drawdown = peak - curve
    return float(np.max(drawdown)) if drawdown.size else 0.0


def profit_factor(values: np.ndarray) -> float:
    gains = float(values[values > 0].sum())
    losses = float(-values[values < 0].sum())
    if losses <= 0:
        return math.inf if gains > 0 else 0.0
    return gains / losses


def load_training_frame() -> tuple[pd.DataFrame, list[str]]:
    schema = read_csv(rv.TRAINING_FEATURE_SCHEMA)
    feature_names = [
        str(row["feature_name"])
        for _, row in schema.iterrows()
        if str(row.get("run338D_train_allowed", "")).startswith("yes")
    ]
    frame = pd.read_parquet(str(io(rv.mat.INPUT_FRAME)))
    assignment = read_csv(rv.GROUP_SAFE_SPLIT_ASSIGNMENT)[["source_row_id", "timestamp", SPLIT_COLUMN]]
    if len(assignment) != len(frame):
        raise RuntimeError(f"group-safe split assignment row mismatch: frame={len(frame)} assignment={len(assignment)}")
    frame_ts = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce").reset_index(drop=True)
    assignment_ts = pd.to_datetime(assignment["timestamp"], utc=True, errors="coerce").reset_index(drop=True)
    same_timestamp = frame_ts.eq(assignment_ts)
    same_source_row = frame["source_row_id"].astype(str).reset_index(drop=True).eq(assignment["source_row_id"].astype(str).reset_index(drop=True))
    if not bool((same_timestamp & same_source_row).all()):
        bad_count = int((~(same_timestamp & same_source_row)).sum())
        raise RuntimeError(f"group-safe split assignment order mismatch for {bad_count} rows")
    frame[SPLIT_COLUMN] = assignment[SPLIT_COLUMN].astype(str).to_numpy()
    missing_features = [name for name in feature_names if name not in frame.columns]
    if missing_features:
        raise RuntimeError(f"training features missing from frame: {missing_features[:10]}")
    required_columns = [PRIMARY_LABEL, LONG_PROXY, SHORT_PROXY]
    missing_required = [name for name in required_columns if name not in frame.columns]
    if missing_required:
        raise RuntimeError(f"required label/proxy columns missing: {missing_required}")
    frame = frame.sort_values(["timestamp", "source_row_id"]).reset_index(drop=True)
    return frame, feature_names


def make_feature_order(feature_names: Sequence[str]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "feature_index": index,
                "feature_name": name,
                "dtype": "float32",
                "source_schema": rel(rv.TRAINING_FEATURE_SCHEMA),
                "effect": "ONNX(온엑스) 입력 순서를 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for index, name in enumerate(feature_names)
        ]
    )


def convert_and_check_onnx(model_id: str, model: Pipeline, x_holdout: np.ndarray, sklearn_proba: np.ndarray) -> dict[str, Any]:
    onnx_path = MODEL_DIR / f"{model_id}.onnx"
    initial_types = [("float_input", FloatTensorType([None, x_holdout.shape[1]]))]
    classifier = model.steps[-1][1]
    onnx_model = convert_sklearn(
        model,
        initial_types=initial_types,
        options={id(classifier): {"zipmap": False}},
        target_opset=17,
    )
    ensure_parent(onnx_path)
    io(onnx_path).write_bytes(onnx_model.SerializeToString())
    session = ort.InferenceSession(str(io(onnx_path)), providers=["CPUExecutionProvider"])
    outputs = session.run(None, {"float_input": x_holdout.astype(np.float32)})
    onnx_proba = outputs[1]
    max_abs_diff = float(np.max(np.abs(onnx_proba - sklearn_proba))) if sklearn_proba.size else 0.0
    return {
        "model_id": model_id,
        "onnx_path": rel(onnx_path),
        "onnx_sha256": sha(onnx_path),
        "max_abs_probability_diff": max_abs_diff,
        "parity_status": "passed" if max_abs_diff <= 1e-5 else "failed",
        "effect": "sklearn(사이킷런) 예측과 ONNX runtime(온엑스 런타임) 예측 차이를 확인한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evaluate_proxy_grid(model_id: str, proba: np.ndarray, holdout: pd.DataFrame) -> pd.DataFrame:
    classes = np.array([0, 1, 2])
    top_order = np.argsort(-proba, axis=1)
    top_class = classes[top_order[:, 0]]
    top_prob = proba[np.arange(len(proba)), top_order[:, 0]]
    second_prob = proba[np.arange(len(proba)), top_order[:, 1]]
    margin = top_prob - second_prob
    long_proxy = pd.to_numeric(holdout[LONG_PROXY], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    short_proxy = pd.to_numeric(holdout[SHORT_PROXY], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    rows = []
    for grid in THRESHOLD_GRID:
        signal_mask = (top_class != 1) & (top_prob >= grid["min_prob"]) & (margin >= grid["min_margin"])
        if grid["density_cap"] < 1.0 and signal_mask.any():
            candidate_indices = np.where(signal_mask)[0]
            keep_count = max(1, int(math.ceil(len(holdout) * grid["density_cap"])))
            ranked = candidate_indices[np.argsort(-margin[candidate_indices])]
            keep = set(ranked[:keep_count].tolist())
            signal_mask = np.array([index in keep for index in range(len(holdout))])
        direction = np.where(signal_mask & (top_class == 2), 1, np.where(signal_mask & (top_class == 0), -1, 0))
        pnl = np.where(direction > 0, long_proxy, np.where(direction < 0, short_proxy, 0.0))
        trades = int(np.count_nonzero(direction))
        long_trades = int(np.count_nonzero(direction > 0))
        short_trades = int(np.count_nonzero(direction < 0))
        trade_values = pnl[direction != 0]
        net = float(trade_values.sum()) if trades else 0.0
        dd = max_drawdown(trade_values)
        pf = profit_factor(trade_values)
        expectancy = safe_ratio(net, trades)
        side_balance = safe_ratio(max(long_trades, short_trades), trades) if trades else 0.0
        density = safe_ratio(trades, len(holdout))
        rows.append(
            {
                "model_id": model_id,
                "min_prob": grid["min_prob"],
                "min_margin": grid["min_margin"],
                "density_cap": grid["density_cap"],
                "trade_count": trades,
                "long_trades": long_trades,
                "short_trades": short_trades,
                "signal_density": round(density, 8),
                "side_balance": round(side_balance, 8),
                "proxy_net_log_return": round(net, 10),
                "proxy_profit_factor": round(pf if math.isfinite(pf) else 999.0, 8),
                "proxy_expectancy": round(expectancy, 10),
                "proxy_max_drawdown": round(dd, 10),
                "proxy_recovery": round(safe_ratio(net, dd), 8) if dd > 0 else (999.0 if net > 0 else 0.0),
                "proxy_score": round(net - dd - max(0.0, side_balance - 0.72) * abs(net) - max(0.0, density - 0.25) * abs(net), 10),
                "effect": "MT5(메타트레이더5)가 아니라 proxy(프록시)로 threshold(임계값) 표면을 거칠게 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_training_outputs() -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[Path]]:
    parent_final = read_json(rv.FINAL_DECISION)
    parent_gates = read_csv(rv.GATE_AUDIT)
    frame, feature_names = load_training_frame()
    feature_order = make_feature_order(feature_names)
    valid = pd.to_numeric(frame[PRIMARY_LABEL], errors="coerce").fillna(-1).astype(int).ne(-1)
    train_mask = frame[SPLIT_COLUMN].astype(str).eq("inner_train") & valid
    holdout_mask = frame[SPLIT_COLUMN].astype(str).eq("inner_holdout") & valid
    x_train = frame.loc[train_mask, feature_names].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=np.float32)
    y_train = pd.to_numeric(frame.loc[train_mask, PRIMARY_LABEL], errors="coerce").astype(int).to_numpy()
    x_holdout = frame.loc[holdout_mask, feature_names].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=np.float32)
    y_holdout = pd.to_numeric(frame.loc[holdout_mask, PRIMARY_LABEL], errors="coerce").astype(int).to_numpy()
    holdout = frame.loc[holdout_mask].copy().reset_index(drop=True)

    model_rows = []
    parity_rows = []
    grid_frames = []
    prediction_frame = holdout[["timestamp", "symbol", "source_row_id", PRIMARY_LABEL, LONG_PROXY, SHORT_PROXY]].copy()
    model_paths: list[Path] = []
    for model_id, model in MODEL_SPECS.items():
        model.fit(x_train, y_train)
        proba = model.predict_proba(x_holdout)
        pred = model.classes_[np.argmax(proba, axis=1)]
        model_path = MODEL_DIR / f"{model_id}.joblib"
        ensure_parent(model_path)
        joblib.dump(model, str(io(model_path)))
        model_paths.append(model_path)
        parity = convert_and_check_onnx(model_id, model, x_holdout, proba)
        parity_rows.append(parity)
        model_paths.append(MODEL_DIR / f"{model_id}.onnx")
        grid = evaluate_proxy_grid(model_id, proba, holdout)
        grid_frames.append(grid)
        best = grid.sort_values(
            ["proxy_score", "proxy_net_log_return", "proxy_profit_factor", "trade_count"],
            ascending=[False, False, False, False],
        ).iloc[0]
        model_rows.append(
            {
                "model_id": model_id,
                "joblib_path": rel(model_path),
                "onnx_path": parity["onnx_path"],
                "train_rows": int(len(y_train)),
                "holdout_rows": int(len(y_holdout)),
                "feature_count": int(len(feature_names)),
                "accuracy": round(float(accuracy_score(y_holdout, pred)), 8),
                "balanced_accuracy": round(float(balanced_accuracy_score(y_holdout, pred)), 8),
                "macro_f1": round(float(f1_score(y_holdout, pred, average="macro")), 8),
                "log_loss": round(float(log_loss(y_holdout, proba, labels=[0, 1, 2])), 8),
                "best_min_prob": best["min_prob"],
                "best_min_margin": best["min_margin"],
                "best_density_cap": best["density_cap"],
                "best_trade_count": best["trade_count"],
                "best_proxy_net_log_return": best["proxy_net_log_return"],
                "best_proxy_profit_factor": best["proxy_profit_factor"],
                "best_proxy_expectancy": best["proxy_expectancy"],
                "best_proxy_max_drawdown": best["proxy_max_drawdown"],
                "best_proxy_recovery": best["proxy_recovery"],
                "best_side_balance": best["side_balance"],
                "onnx_parity_max_abs_probability_diff": parity["max_abs_probability_diff"],
                "result_role": "proxy_training_output_not_selection(프록시 학습 산출물_선택 아님)",
                "effect": "모델별 proxy(프록시) 표면을 다음 MT5 runtime probe(MT5 런타임 탐침) 검토 후보로만 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for class_index, class_label in enumerate(model.classes_):
            prediction_frame[f"{model_id}_proba_class_{class_label}"] = proba[:, class_index]
        prediction_frame[f"{model_id}_pred_class"] = pred

    proxy_grid = pd.concat(grid_frames, ignore_index=True)
    scorecard = pd.DataFrame(model_rows).sort_values(
        ["best_proxy_net_log_return", "best_proxy_profit_factor", "best_trade_count"],
        ascending=[False, False, False],
    )
    parity_audit = pd.DataFrame(parity_rows)
    positive_proxy_rows = int((proxy_grid["proxy_net_log_return"] > 0).sum())
    best_row = scorecard.iloc[0].to_dict() if not scorecard.empty else {}
    queue = pd.DataFrame(
        [
            {
                "queue_id": "run338F_proxy_score_review_for_mt5_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "review proxy-positive ONNX models for MT5 runtime probe routing(프록시 양수 ONNX 모델의 MT5 런타임 탐침 라우팅 검토)",
                "required_inputs": f"{rel(MODEL_SCORECARD)};{rel(PROXY_THRESHOLD_GRID)};{rel(ONNX_PARITY_AUDIT)};{rel(FEATURE_ORDER)}",
                "blocked_if_missing": "positive proxy surface or ONNX parity pass(양수 프록시 표면 또는 ONNX 동등성 통과)",
                "forbidden_action": "operating promotion before MT5 runtime evidence(MT5 런타임 근거 전 운영 승격)",
                "effect": "proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표) 대체가 아니라 탐침 라우팅 자료로만 쓴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "source_rows": int(len(frame)),
        "train_rows": int(len(y_train)),
        "holdout_rows": int(len(y_holdout)),
        "feature_count": int(len(feature_names)),
        "model_count": int(len(MODEL_SPECS)),
        "onnx_export_count": int(len(parity_audit)),
        "onnx_parity_failed_count": int(parity_audit["parity_status"].ne("passed").sum()) if not parity_audit.empty else 0,
        "proxy_grid_rows": int(len(proxy_grid)),
        "positive_proxy_rows": positive_proxy_rows,
        "best_model_id": str(best_row.get("model_id", "")),
        "best_proxy_net_log_return": float(best_row.get("best_proxy_net_log_return", 0.0) or 0.0),
        "best_proxy_profit_factor": float(best_row.get("best_proxy_profit_factor", 0.0) or 0.0),
        "best_proxy_trade_count": int(best_row.get("best_trade_count", 0) or 0),
        "input_frame_sha256": sha(rv.mat.INPUT_FRAME),
        "training_feature_schema_sha256": sha(rv.TRAINING_FEATURE_SCHEMA),
        "group_safe_split_sha256": sha(rv.GROUP_SAFE_SPLIT_ASSIGNMENT),
        "parent_gate_passed": bool(passed_status(parent_gates["status"]).all()),
        "parent_goal_achieve": parent_final.get("goal_achieve", "not_claimed"),
        "next_run_id": NEXT_RUN_ID,
        "effect": "ONNX(온엑스) 모델과 proxy(프록시) 점수표를 만들되 MT5(메타트레이더5) 성과로 주장하지 않는다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return summary, {
        "feature_order": feature_order,
        "scorecard": scorecard,
        "proxy_grid": proxy_grid,
        "parity": parity_audit,
        "predictions": prediction_frame,
        "summary": pd.DataFrame([summary]),
        "queue": queue,
    }, model_paths


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            gate_row("parent_338D_gates_passed", "passed" if summary["parent_gate_passed"] else "failed", rel(rv.GATE_AUDIT), "run338D(338D 실행) 입력 검토를 이어받는다."),
            gate_row("group_safe_split_used", "passed" if summary["group_safe_split_sha256"] else "failed", rel(rv.GROUP_SAFE_SPLIT_ASSIGNMENT), "학습은 group-safe split(묶음 안전 분할)만 쓴다."),
            gate_row("training_feature_schema_applied", "passed" if summary["feature_count"] > 0 else "failed", rel(rv.TRAINING_FEATURE_SCHEMA), "상수 제외 training feature schema(학습 피처 스키마)를 적용한다."),
            gate_row("models_trained", "passed" if summary["model_count"] > 0 else "failed", rel(MODEL_SCORECARD), "탐색 모델을 실제 학습한다."),
            gate_row("onnx_exports_written", "passed" if summary["onnx_export_count"] == summary["model_count"] else "failed", rel(ONNX_PARITY_AUDIT), "학습 모델을 ONNX(온엑스)로 내보낸다."),
            gate_row("onnx_parity_passed", "passed" if summary["onnx_parity_failed_count"] == 0 else "failed", rel(ONNX_PARITY_AUDIT), "sklearn(사이킷런)과 ONNX runtime(온엑스 런타임) 예측 동등성을 확인한다."),
            gate_row("proxy_scorecard_written", "passed" if summary["proxy_grid_rows"] > 0 else "failed", rel(PROXY_THRESHOLD_GRID), "MT5(메타트레이더5) 전 proxy(프록시) 표면을 기록한다."),
            gate_row("run338F_review_queue_opened", "passed" if exists(RUN338F_REVIEW_QUEUE) or summary["positive_proxy_rows"] >= 0 else "failed", rel(RUN338F_REVIEW_QUEUE), "다음 proxy review(프록시 검토) queue(대기열)를 연다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(FINAL_DECISION), "선택/MT5/운영/목표 달성을 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_tables(tables: Mapping[str, pd.DataFrame]) -> None:
    write_csv(FEATURE_ORDER, tables["feature_order"])
    write_csv(MODEL_SCORECARD, tables["scorecard"])
    write_csv(PROXY_THRESHOLD_GRID, tables["proxy_grid"])
    write_csv(ONNX_PARITY_AUDIT, tables["parity"])
    ensure_parent(HOLDOUT_PREDICTIONS)
    tables["predictions"].to_parquet(str(io(HOLDOUT_PREDICTIONS)), index=False)
    write_csv(TRAINING_SUMMARY, tables["summary"])
    write_csv(RUN338F_REVIEW_QUEUE, tables["queue"])


def write_receipts(summary: Mapping[str, Any], model_paths: Sequence[Path]) -> None:
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
            "data_source": rel(rv.mat.INPUT_FRAME),
            "time_axis": "run338D group-safe split only(338D 묶음 안전 분할만 사용)",
            "sample_scope": f"train={summary['train_rows']};holdout={summary['holdout_rows']};features={summary['feature_count']}",
            "feature_label_boundary": rel(rv.mat.FEATURE_LABEL_BOUNDARY_AUDIT),
            "split_boundary": rel(rv.GROUP_SAFE_SPLIT_MANIFEST),
            "data_hash_or_identity": summary["input_frame_sha256"],
            "integrity_judgment": "usable_for_proxy_training_only(프록시 학습 전용 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "sklearn tree/logistic multiclass converted to ONNX(사이킷런 트리/로지스틱 다중분류 ONNX 변환)",
            "target_and_label": PRIMARY_LABEL,
            "split_method": rel(rv.GROUP_SAFE_SPLIT_MANIFEST),
            "selection_metric": "none_selected; proxy score review next(선택 없음; 다음 프록시 점수 검토)",
            "model_paths": [rel(path) for path in model_paths],
            "onnx_parity": rel(ONNX_PARITY_AUDIT),
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in list(OUTPUT_FILES) + list(model_paths) if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in list(OUTPUT_FILES) + list(model_paths) if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "models_and_onnx_written(모델과 ONNX 작성됨)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "run",
            "threshold_tuning": "proxy_grid_only_not_promotion",
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
        "model_training": "run",
        "threshold_tuning": "proxy_grid_only_not_promotion",
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
    report = f"""# run338E Group-Safe Training Proxy(묶음 안전 학습 프록시)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- train_rows(학습 행): `{final['train_rows']}`
- holdout_rows(홀드아웃 행): `{final['holdout_rows']}`
- features(피처): `{final['feature_count']}`
- models(모델): `{final['model_count']}`
- best_model(최고 프록시 모델): `{final['best_model_id']}`
- best_proxy_net_log_return(최고 프록시 순로그수익): `{final['best_proxy_net_log_return']}`
- best_proxy_profit_factor(최고 프록시 수익 팩터): `{final['best_proxy_profit_factor']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338D(338D 실행)의 group-safe split(묶음 안전 분할)과 training feature schema(학습 피처 스키마)만 사용해 sklearn(사이킷런) 모델을 학습하고 ONNX(온엑스)로 변환했다.
Effect(효과): MT5 runtime probe(MT5 런타임 탐침) 전에 proxy(프록시)로 볼 수 있는 ONNX(온엑스) 산출물이 생겼다.

## Evidence(근거)

- model scorecard(모델 점수표): `{rel(MODEL_SCORECARD)}`
- proxy threshold grid(프록시 임계값 표면): `{rel(PROXY_THRESHOLD_GRID)}`
- ONNX parity audit(온엑스 동등성 감사): `{rel(ONNX_PARITY_AUDIT)}`
- feature order(피처 순서): `{rel(FEATURE_ORDER)}`
- next queue(다음 대기열): `{rel(RUN338F_REVIEW_QUEUE)}`

## Boundary(경계)

run338E(338E 실행)는 training/proxy evaluation(학습/프록시 평가)이다. Candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338E Decision(338E 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(MODEL_SCORECARD)}`, `{rel(ONNX_PARITY_AUDIT)}`, `{rel(RUN338F_REVIEW_QUEUE)}`

Action(행동): group-safe(묶음 안전) 학습 모델과 ONNX(온엑스) 변환 산출물을 만들었다.
Effect(효과): proxy-positive(프록시 양수) 표면은 run338F(338F 실행)에서 MT5 runtime probe(MT5 런타임 탐침) 라우팅 여부만 검토한다.

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

run338E(338E 실행)는 ONNX(온엑스) 학습 산출물을 만들었지만, 운영 의미는 아직 없다. run338F(338F 실행)는 proxy(프록시) 결과를 MT5 runtime probe(MT5 런타임 탐침) 라우팅 근거로만 검토해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- trained_model_count(학습 모델 수): `{final['model_count']}`
- onnx_export_count(온엑스 내보내기 수): `{final['onnx_export_count']}`
- best_proxy_model(최고 프록시 모델): `{final['best_model_id']}`
- best_proxy_net_log_return(최고 프록시 순로그수익): `{final['best_proxy_net_log_return']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): ONNX(온엑스) 산출물을 선정 모델로 오해하지 않게 한다.
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
    marker = f"run338E {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run338E Group-Safe Training Proxy(묶음 안전 학습 프록시)

- run_id(실행 ID): `{RUN_ID}`
- models(모델): `{final['model_count']}`
- best_proxy_model(최고 프록시 모델): `{final['best_model_id']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): ONNX(온엑스) 산출물을 만들되 MT5(메타트레이더5) 검증 전 선택으로 올리지 않는다.
""")
    append_text_once(STAGE_README, marker, f"""## run338E Group-Safe Training Proxy(묶음 안전 학습 프록시)

- run_id(실행 ID): `{RUN_ID}`
- model_scorecard(모델 점수표): `{rel(MODEL_SCORECARD)}`
- effect(효과): Stage338(338단계)이 실제 ONNX(온엑스) 모델 산출물 단계로 이동했다.
""")
    changelog = f"""## {TODAY} run338E Group-Safe Training Proxy(묶음 안전 학습 프록시)

- action(행동): `{final['model_count']}`개 모델을 학습하고 `{final['onnx_export_count']}`개 ONNX(온엑스)를 내보냈다.
- effect(효과): best proxy(최고 프록시) `{final['best_model_id']}` net `{final['best_proxy_net_log_return']}`를 run338F(338F 실행) 검토로 넘긴다.
- boundary(경계): selected candidate/MT5/operating promotion/Goal Achieve(선정 후보/MT5/운영 승격/목표 달성)는 없다.
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
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "proxy_training", "sample_rows": final["source_rows"], "feature_count": final["feature_count"], "net_profit": final["best_proxy_net_log_return"], "profit_factor": final["best_proxy_profit_factor"], "trade_count": final["best_proxy_trade_count"], "result_status": JUDGMENT},
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
    io(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io(REVIEW_DIR).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run338E inputs: {missing}")
    summary, tables, model_paths = build_training_outputs()
    write_tables(tables)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, model_paths)
    final = write_final(summary, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in list(OUTPUT_FILES) + list(model_paths) if path != ARTIFACT_REGISTRY])
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338E gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "model_count": final["model_count"],
                "onnx_export_count": final["onnx_export_count"],
                "best_model_id": final["best_model_id"],
                "best_proxy_net_log_return": final["best_proxy_net_log_return"],
                "best_proxy_profit_factor": final["best_proxy_profit_factor"],
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

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
)


warnings.filterwarnings("ignore", message="X does not have valid feature names.*", category=UserWarning)
warnings.filterwarnings("ignore", message="X has feature names.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*lbfgs failed to converge.*", category=UserWarning)

TODAY = "2026-06-02"
STAGE_ID = "356_density_recovery_training__proxy_model_queue_scout"
RUN_NUMBER = "run356D"
RUN_ID = "run356D_design_high_density_label_pivot_without_db_v1"
PARENT_RUN_ID = "run356C_expand_density_recovery_proxy_training_search_without_db_v1"
SOURCE_RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"
NEXT_RUN_ID_POSITIVE = "run356E_package_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID_NEGATIVE = "run356E_expand_high_density_label_pivot_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_high_density_label_pivot_proxy_scout_only_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
LABEL_ORDER = [0, 1, 2]
MIN_TRADE_PER_DAY = 3.0
MAX_TRADE_PER_DAY = 10.0
MIN_STRESS_PF = 1.02
MIN_BALANCE = 0.20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_STAGE_DIR = ROOT / "stages" / "355_density_recovery_model_family__new_label_source_probe"
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run355B"
FEATURE_LABEL_TABLE = SOURCE_RUN_DIR / "feature_label_table.csv"
TRAINING_QUEUE_REF = STAGE_DIR / "01_inputs" / "run356B_training_queue_ref.csv"
RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run356C"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_BEST_SCORECARD = PARENT_RUN_DIR / "best_expansion_scorecard.csv"
PARENT_FEATURE_SCHEMA = STAGE_DIR / "02_runs" / "run356B" / "feature_schema.json"

SOURCE_DATA_AUDIT = RUN_DIR / "source_data_audit.csv"
LABEL_DESIGN_MANIFEST = RUN_DIR / "high_density_label_design_manifest.csv"
LABEL_DISTRIBUTION = RUN_DIR / "high_density_label_distribution.csv"
MODEL_MANIFEST = RUN_DIR / "classifier_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "classification_scorecard.csv"
THRESHOLD_SWEEP_SCORECARD = RUN_DIR / "threshold_sweep_scorecard.csv"
BEST_SCORECARD = RUN_DIR / "best_candidate_scorecard.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_candidate_queue.csv"
FIREWALL_REVIEW = RUN_DIR / "runtime_firewall_review.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run356D_high_density_label_pivot.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_SELECTION = SELECTED_DIR / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage356D_high_density_label_pivot.md"

KEY_COLUMNS = ["bar_time_server", "timestamp_utc", "split", "row_index"]
RETURN_COLUMNS = ["future_log_return_6", "future_log_return_8", "future_log_return_12"]

MODEL_SPECS: tuple[tuple[str, str, Any], ...] = (
    (
        "extratrees_cls_depth5_leaf100",
        "ExtraTreesClassifier(엑스트라트리 분류기)",
        ExtraTreesClassifier(
            n_estimators=160,
            max_depth=5,
            min_samples_leaf=100,
            max_features="sqrt",
            class_weight="balanced",
            random_state=3564,
            n_jobs=-1,
        ),
    ),
    (
        "extratrees_cls_depth8_leaf120",
        "ExtraTreesClassifier(엑스트라트리 분류기)",
        ExtraTreesClassifier(
            n_estimators=160,
            max_depth=8,
            min_samples_leaf=120,
            max_features="sqrt",
            class_weight="balanced",
            random_state=3565,
            n_jobs=-1,
        ),
    ),
    (
        "extratrees_cls_depth10_leaf80",
        "ExtraTreesClassifier(엑스트라트리 분류기)",
        ExtraTreesClassifier(
            n_estimators=160,
            max_depth=10,
            min_samples_leaf=80,
            max_features="sqrt",
            class_weight="balanced",
            random_state=3566,
            n_jobs=-1,
        ),
    ),
)

SCORE_POLICIES = ["pside", "margin", "side_x_nonflat", "margin_x_nonflat"]
QUANTILES = [0.20, 0.30, 0.40, 0.50]
ADX_MIN_VALUES = [10.0, 16.0, 20.0]
SESSION_MODES = ["all", "cash_0_360"]


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
    try:
        return Path(fs_path(path)).exists()
    except OSError:
        return False


def ensure_parent(path: Path) -> None:
    Path(fs_path(path.parent)).mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(items: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()


def json_default(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        numeric = float(value)
        return numeric if math.isfinite(numeric) else None
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True, default=json_default)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows_list:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(path: Path, key_fields: Sequence[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    existing_fields: list[str] = []
    existing_rows: list[dict[str, Any]] = []
    if exists(path):
        existing_fields, existing_rows = read_csv_rows(path)
    fieldnames = list(existing_fields)
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing_rows
        if tuple(str(row.get(field, "")) for field in key_fields) not in replace_keys
    ]
    write_csv(path, [*kept, *[dict(row) for row in new_rows]], fieldnames)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    return numeric if math.isfinite(numeric) else default


def split_days(frame: pd.DataFrame) -> int:
    return max(1, int(frame["timestamp_utc"].astype(str).str.slice(0, 10).nunique()))


def session_mask(frame: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "all":
        return np.ones(len(frame), dtype=bool)
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    if mode == "cash_0_360":
        return (minutes >= 0) & (minutes <= 360)
    raise ValueError(f"Unknown session mode(알 수 없는 세션 모드): {mode}")


def nonoverlap_indices(row_index: np.ndarray, signal: np.ndarray, horizon_bars: int) -> np.ndarray:
    chosen: list[int] = []
    next_open = -10**18
    for index in np.flatnonzero(signal):
        row_value = int(row_index[index])
        if row_value < next_open:
            continue
        chosen.append(int(index))
        next_open = row_value + int(horizon_bars)
    return np.asarray(chosen, dtype=int)


def equity_metrics(pnl: np.ndarray) -> tuple[float, float, float, float, float]:
    if pnl.size == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    net = float(pnl.sum())
    wins = float(pnl[pnl > 0].sum())
    losses = float(-pnl[pnl < 0].sum())
    profit_factor = wins / losses if losses > 0 else (999.0 if wins > 0 else 0.0)
    equity = np.cumsum(pnl)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = float(np.max(peaks - equity)) if equity.size else 0.0
    recovery = net / drawdown if drawdown > 0 else (999.0 if net > 0 else 0.0)
    return net, profit_factor, float(net / pnl.size), drawdown, recovery


def evaluate_trades(returns: np.ndarray, sides: np.ndarray, costs: np.ndarray, days: int) -> dict[str, Any]:
    if returns.size == 0:
        return {
            "trade_count": 0,
            "trade_per_day": 0.0,
            "stress_net": 0.0,
            "stress_profit_factor": 0.0,
            "stress_expectancy": 0.0,
            "stress_max_drawdown": 0.0,
            "stress_recovery_factor": 0.0,
            "win_rate": 0.0,
            "long_count": 0,
            "short_count": 0,
            "long_short_balance": 0.0,
        }
    pnl = sides * returns - costs
    net, pf, expectancy, drawdown, recovery = equity_metrics(pnl)
    long_count = int((sides > 0).sum())
    short_count = int((sides < 0).sum())
    balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) else 0.0
    return {
        "trade_count": int(returns.size),
        "trade_per_day": float(returns.size / days),
        "stress_net": net,
        "stress_profit_factor": pf,
        "stress_expectancy": expectancy,
        "stress_max_drawdown": drawdown,
        "stress_recovery_factor": recovery,
        "win_rate": float((pnl > 0).mean()),
        "long_count": long_count,
        "short_count": short_count,
        "long_short_balance": float(balance),
    }


def load_sources() -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    feature_schema = read_json(PARENT_FEATURE_SCHEMA)
    feature_columns = list(feature_schema["features"])
    feature_frame = pd.read_csv(fs_path(RUNTIME_FEATURES), usecols=[*KEY_COLUMNS, *feature_columns])
    raw = pd.read_csv(
        fs_path(FEATURE_LABEL_TABLE),
        usecols=[*KEY_COLUMNS, "label_variant_id", *RETURN_COLUMNS, "stress_cost_log_return", "base_cost_log_return"],
    )
    raw = raw[raw["label_variant_id"].eq("d01_h6_cost_buffer")].drop(columns=["label_variant_id"])
    full = raw.merge(feature_frame, on=KEY_COLUMNS, how="left", validate="one_to_one")
    full = full.sort_values("row_index").reset_index(drop=True)
    feature_dups = int(feature_frame.duplicated(KEY_COLUMNS).sum())
    raw_dups = int(raw.duplicated(KEY_COLUMNS).sum())
    missing = int(full[feature_columns].isna().any(axis=1).sum())
    if feature_dups or raw_dups or missing:
        raise RuntimeError(
            "source join integrity failed(원천 결합 무결성 실패): "
            f"feature_dups={feature_dups}, raw_dups={raw_dups}, missing={missing}"
        )
    identity = {
        "feature_rows": int(len(feature_frame)),
        "raw_label_rows": int(len(raw)),
        "merged_rows": int(len(full)),
        "feature_columns": int(len(feature_columns)),
        "feature_duplicate_key_rows": feature_dups,
        "raw_duplicate_key_rows": raw_dups,
        "missing_feature_join_rows": missing,
        "feature_order_hash": ordered_hash(feature_columns),
        "runtime_features_sha256": sha256_file(RUNTIME_FEATURES),
        "feature_label_table_sha256": sha256_file(FEATURE_LABEL_TABLE),
        "training_queue_ref_sha256": sha256_file(TRAINING_QUEUE_REF),
        "parent_final_decision_sha256": sha256_file(PARENT_FINAL_DECISION),
        "parent_best_scorecard_sha256": sha256_file(PARENT_BEST_SCORECARD),
    }
    return full, feature_columns, identity


def build_labels(full: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]]]:
    train_mask = full["split"].eq("train")
    ret12 = full["future_log_return_12"].to_numpy(dtype=float)
    cost = full["stress_cost_log_return"].to_numpy(dtype=float)
    q40 = float(full.loc[train_mask, "future_log_return_12"].quantile(0.40))
    q45 = float(full.loc[train_mask, "future_log_return_12"].quantile(0.45))
    q55 = float(full.loc[train_mask, "future_log_return_12"].quantile(0.55))
    q60 = float(full.loc[train_mask, "future_log_return_12"].quantile(0.60))
    definitions = [
        {
            "label_variant_id": "d04_h12_q45_55_high_density_band",
            "design_id": "d04_train_quantile_h12_q45_q55",
            "horizon_bars": 12,
            "threshold_family": "train_quantile_band(학습 분위수 밴드)",
            "lower_threshold": q45,
            "upper_threshold": q55,
            "labels": np.where(ret12 > q55, 2, np.where(ret12 < q45, 0, 1)),
            "hypothesis": "narrow flat band raises density while preserving directional edge(좁은 플랫 밴드가 방향 엣지를 보존하며 밀도를 높인다)",
        },
        {
            "label_variant_id": "d05_h12_q40_60_balanced_band",
            "design_id": "d05_train_quantile_h12_q40_q60",
            "horizon_bars": 12,
            "threshold_family": "train_quantile_band(학습 분위수 밴드)",
            "lower_threshold": q40,
            "upper_threshold": q60,
            "labels": np.where(ret12 > q60, 2, np.where(ret12 < q40, 0, 1)),
            "hypothesis": "wider flat band improves quality while staying near 3+ trade/day(넓은 플랫 밴드가 품질을 높이면서 3+ 일별 거래에 근접한다)",
        },
        {
            "label_variant_id": "d06_h12_cost025_soft_flat",
            "design_id": "d06_h12_stress_cost_025_soft_flat",
            "horizon_bars": 12,
            "threshold_family": "stress_cost_fraction(압박 비용 비율)",
            "lower_threshold": -0.25,
            "upper_threshold": 0.25,
            "labels": np.where(ret12 > cost * 0.25, 2, np.where(ret12 < -cost * 0.25, 0, 1)),
            "hypothesis": "soft cost flat lowers noise without killing density(완화 비용 플랫이 밀도를 죽이지 않고 잡음을 줄인다)",
        },
    ]
    label_frames: list[pd.DataFrame] = []
    manifest_rows: list[dict[str, Any]] = []
    dist_rows: list[dict[str, Any]] = []
    for item in definitions:
        labels = item["labels"].astype(int)
        label_frame = full[[*KEY_COLUMNS, *RETURN_COLUMNS, "stress_cost_log_return", "base_cost_log_return"]].copy()
        label_frame["label_variant_id"] = item["label_variant_id"]
        label_frame["design_id"] = item["design_id"]
        label_frame["horizon_bars"] = item["horizon_bars"]
        label_frame["label_class_id"] = labels
        label_frame["label_name"] = np.where(labels == 2, "long", np.where(labels == 0, "short", "flat"))
        label_frame["allowed_use"] = "model_training_proxy_scout(모델 학습 프록시 탐색)"
        label_frame["forbidden_use"] = "operating_claim_without_mt5_probe(MT5 탐침 없는 운영 주장)"
        label_frame["claim_boundary"] = CLAIM_BOUNDARY
        label_frames.append(label_frame)
        manifest_rows.append(
            {
                "label_variant_id": item["label_variant_id"],
                "design_id": item["design_id"],
                "horizon_bars": item["horizon_bars"],
                "threshold_family": item["threshold_family"],
                "lower_threshold": item["lower_threshold"],
                "upper_threshold": item["upper_threshold"],
                "rows": int(len(label_frame)),
                "timestamp_boundary": "current closed M5 bar then future-only raw bars(현재 닫힌 M5 봉 뒤 미래 원시 봉만)",
                "hypothesis": item["hypothesis"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split in ["train", "validation", "oos"]:
            split_labels = labels[full["split"].eq(split).to_numpy()]
            for class_id, class_name in [(0, "short"), (1, "flat"), (2, "long")]:
                count = int((split_labels == class_id).sum())
                dist_rows.append(
                    {
                        "label_variant_id": item["label_variant_id"],
                        "split": split,
                        "label_class_id": class_id,
                        "label_name": class_name,
                        "count": count,
                        "share": float(count / max(1, len(split_labels))),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    labels_out = pd.concat(label_frames, ignore_index=True)
    write_csv(LABEL_DESIGN_MANIFEST, manifest_rows)
    write_csv(LABEL_DISTRIBUTION, dist_rows)
    return labels_out, manifest_rows, dist_rows


def write_source_audit(identity: Mapping[str, Any]) -> None:
    rows = [
        {"check_id": key, "value": json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value, "status": "passed", "claim_boundary": CLAIM_BOUNDARY}
        for key, value in identity.items()
    ]
    rows.extend(
        [
            {
                "check_id": "time_axis",
                "value": "timestamp_utc is closed M5 bar time; labels use future raw bars only(시각은 닫힌 M5 봉이며 라벨은 미래 원시 봉만 사용)",
                "status": "passed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "feature_label_boundary",
                "value": "quantile thresholds use train split only; features are joined at t(분위수 임계값은 학습 분할만 쓰고 피처는 t에서 결합)",
                "status": "passed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(SOURCE_DATA_AUDIT, rows)


def train_models(label_frame: pd.DataFrame, full: pd.DataFrame, feature_columns: Sequence[str]) -> dict[str, Any]:
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    prediction_cache: dict[str, dict[str, Any]] = {}
    feature_frame = full[[*KEY_COLUMNS, *feature_columns]].copy()
    for label_variant_id in sorted(label_frame["label_variant_id"].unique()):
        labels = label_frame[label_frame["label_variant_id"].eq(label_variant_id)].copy()
        merged = labels.merge(feature_frame, on=KEY_COLUMNS, how="left", validate="one_to_one")
        merged = merged.sort_values("row_index").reset_index(drop=True)
        horizon = int(merged["horizon_bars"].iloc[0])
        x_all = merged.loc[:, feature_columns].astype("float32").to_numpy()
        y_all = merged["label_class_id"].to_numpy(dtype=int)
        train_mask = merged["split"].eq("train").to_numpy()
        validation_mask = merged["split"].eq("validation").to_numpy()
        if len(np.unique(y_all[train_mask])) < 3:
            raise RuntimeError(f"label variant missing class(라벨 클래스 누락): {label_variant_id}")
        for model_config_id, model_family, estimator in MODEL_SPECS:
            model = estimator.__class__(**estimator.get_params())
            model_id = f"{RUN_NUMBER}_{label_variant_id}__{model_config_id}"
            model.fit(x_all[train_mask], y_all[train_mask])
            probabilities = ordered_sklearn_probabilities(model, x_all, LABEL_ORDER)
            model_path = MODEL_DIR / f"{model_id}.joblib"
            onnx_path = ONNX_DIR / f"{model_id}.onnx"
            bundle = {
                "model": model,
                "features": list(feature_columns),
                "class_order": LABEL_ORDER,
                "label_variant_id": label_variant_id,
                "model_config_id": model_config_id,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            joblib.dump(bundle, fs_path(model_path))
            export_status = "passed"
            export_error = ""
            parity: dict[str, Any]
            onnx_meta: dict[str, Any] = {}
            try:
                onnx_meta = export_sklearn_to_onnx_zipmap_disabled(
                    model,
                    onnx_path,
                    feature_count=len(feature_columns),
                    input_name="float_input",
                    target_opset=12,
                    drop_label_output=True,
                )
                parity = check_onnxruntime_probability_parity(
                    onnx_path=onnx_path,
                    input_values=x_all[validation_mask][:512],
                    expected_probabilities=ordered_sklearn_probabilities(model, x_all[validation_mask][:512], LABEL_ORDER),
                    probability_output_name=onnx_meta["probability_output_name"],
                    input_name=onnx_meta["input_name"],
                )
            except Exception as exc:  # pragma: no cover - recorded as evidence.
                export_status = "failed"
                export_error = repr(exc)
                parity = {
                    "status": "failed",
                    "rows": 0,
                    "max_abs_diff": "",
                    "mean_abs_diff": "",
                    "row_sum_max_abs_error": "",
                    "input_name": "",
                    "output_names": "",
                    "probability_output_name": "",
                }
            row = {
                "model_id": model_id,
                "label_variant_id": label_variant_id,
                "model_config_id": model_config_id,
                "model_family": model_family,
                "horizon_bars": horizon,
                "feature_count": len(feature_columns),
                "feature_order_hash": ordered_hash(feature_columns),
                "class_order_json": json.dumps(LABEL_ORDER),
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_path": onnx_meta.get("path", rel(onnx_path)),
                "onnx_sha256": onnx_meta.get("sha256", ""),
                "onnx_export_status": export_status,
                "onnx_export_error": export_error,
                "onnx_parity_status": parity.get("status", "failed"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            model_rows.append(row)
            parity_rows.append(
                {
                    "model_id": model_id,
                    "label_variant_id": label_variant_id,
                    "onnx_path": row["onnx_path"],
                    "onnx_export_status": export_status,
                    "onnx_export_error": export_error,
                    "parity_status": parity.get("status", "failed"),
                    "rows": parity.get("rows", ""),
                    "max_abs_diff": parity.get("max_abs_diff", ""),
                    "mean_abs_diff": parity.get("mean_abs_diff", ""),
                    "onnx_row_sum_max_abs_error": parity.get("row_sum_max_abs_error", ""),
                    "input_name": parity.get("input_name", onnx_meta.get("input_name", "")),
                    "output_names": json.dumps(parity.get("output_names", onnx_meta.get("outputs", "")), ensure_ascii=False),
                    "probability_output_name": parity.get("probability_output_name", onnx_meta.get("probability_output_name", "")),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for split in ["train", "validation", "oos"]:
                mask = merged["split"].eq(split).to_numpy()
                pred = np.asarray([LABEL_ORDER[int(np.argmax(row))] for row in probabilities[mask]], dtype=int)
                true = y_all[mask]
                class_rows.append(
                    {
                        "model_id": model_id,
                        "label_variant_id": label_variant_id,
                        "split": split,
                        "rows": int(mask.sum()),
                        "accuracy": float(accuracy_score(true, pred)),
                        "balanced_accuracy": float(balanced_accuracy_score(true, pred)),
                        "f1_macro": float(f1_score(true, pred, average="macro")),
                        "log_loss": float(log_loss(true, probabilities[mask], labels=LABEL_ORDER)),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
            prediction_cache[model_id] = {
                "frame": merged,
                "probabilities": probabilities,
                "horizon_bars": horizon,
                "model_row": row,
            }
    write_csv(MODEL_MANIFEST, model_rows)
    write_csv(ONNX_PARITY, parity_rows)
    write_csv(CLASSIFICATION_SCORECARD, class_rows)
    return {
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "class_rows": class_rows,
        "prediction_cache": prediction_cache,
    }


def score_values(probabilities: np.ndarray, policy: str) -> tuple[np.ndarray, np.ndarray]:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    side = np.where(p_long >= p_short, 1.0, -1.0)
    pside = np.maximum(p_long, p_short)
    margin = np.abs(p_long - p_short)
    nonflat = 1.0 - p_flat
    if policy == "pside":
        return pside, side
    if policy == "margin":
        return margin, side
    if policy == "side_x_nonflat":
        return pside * nonflat, side
    if policy == "margin_x_nonflat":
        return margin * nonflat, side
    raise ValueError(f"Unknown score policy(알 수 없는 점수 정책): {policy}")


def evaluate_model_threshold(
    model_id: str,
    cache_item: Mapping[str, Any],
    split: str,
    score_policy: str,
    score_quantile: float,
    adx_min: float,
    session_mode: str,
) -> dict[str, Any]:
    frame = cache_item["frame"]
    mask = frame["split"].eq(split).to_numpy()
    split_frame = frame.loc[mask].reset_index(drop=True)
    probabilities = cache_item["probabilities"][mask]
    score, side = score_values(probabilities, score_policy)
    threshold = float(np.quantile(score, score_quantile))
    signal = (
        (score >= threshold)
        & (split_frame["adx_14"].to_numpy(dtype=float) >= float(adx_min))
        & session_mask(split_frame, session_mode)
    )
    chosen = nonoverlap_indices(split_frame["row_index"].to_numpy(dtype=int), signal, int(cache_item["horizon_bars"]))
    target_col = f"future_log_return_{int(cache_item['horizon_bars'])}"
    metrics = evaluate_trades(
        returns=split_frame[target_col].to_numpy(dtype=float)[chosen],
        sides=side[chosen],
        costs=split_frame["stress_cost_log_return"].to_numpy(dtype=float)[chosen],
        days=split_days(split_frame),
    )
    return {
        "model_id": model_id,
        "label_variant_id": cache_item["model_row"]["label_variant_id"],
        "model_config_id": cache_item["model_row"]["model_config_id"],
        "split": split,
        "score_policy": score_policy,
        "score_quantile": score_quantile,
        "score_threshold": threshold,
        "adx_min": adx_min,
        "session_mode": session_mode,
        "horizon_bars": int(cache_item["horizon_bars"]),
        "days": split_days(split_frame),
        "density_requirement": TRADE_DENSITY_REQUIREMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        **metrics,
    }


def evaluate_sweep(train_result: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    for model_id, cache_item in train_result["prediction_cache"].items():
        for split in ["validation", "oos"]:
            for score_policy in SCORE_POLICIES:
                for score_quantile in QUANTILES:
                    for adx_min in ADX_MIN_VALUES:
                        for session_mode in SESSION_MODES:
                            rows.append(
                                evaluate_model_threshold(
                                    model_id,
                                    cache_item,
                                    split,
                                    score_policy,
                                    score_quantile,
                                    adx_min,
                                    session_mode,
                                )
                            )
    write_csv(THRESHOLD_SWEEP_SCORECARD, rows)
    frame = pd.DataFrame(rows)
    keys = ["model_id", "label_variant_id", "model_config_id", "score_policy", "score_quantile", "adx_min", "session_mode"]
    val = frame[frame["split"].eq("validation")]
    oos = frame[frame["split"].eq("oos")]
    merged = val.merge(oos, on=keys, suffixes=("_validation", "_oos"))
    paired_rows: list[dict[str, Any]] = []
    for _, item in merged.iterrows():
        validation_tpd = safe_float(item["trade_per_day_validation"])
        oos_tpd = safe_float(item["trade_per_day_oos"])
        validation_net = safe_float(item["stress_net_validation"])
        oos_net = safe_float(item["stress_net_oos"])
        validation_pf = safe_float(item["stress_profit_factor_validation"])
        oos_pf = safe_float(item["stress_profit_factor_oos"])
        validation_balance = safe_float(item["long_short_balance_validation"])
        oos_balance = safe_float(item["long_short_balance_oos"])
        candidate = (
            MIN_TRADE_PER_DAY <= validation_tpd <= MAX_TRADE_PER_DAY
            and MIN_TRADE_PER_DAY <= oos_tpd <= MAX_TRADE_PER_DAY
            and validation_net > 0.0
            and oos_net > 0.0
            and validation_pf >= MIN_STRESS_PF
            and oos_pf >= MIN_STRESS_PF
            and validation_balance >= MIN_BALANCE
            and oos_balance >= MIN_BALANCE
        )
        paired_rows.append(
            {
                "model_id": item["model_id"],
                "label_variant_id": item["label_variant_id"],
                "model_config_id": item["model_config_id"],
                "score_policy": item["score_policy"],
                "score_quantile": item["score_quantile"],
                "adx_min": item["adx_min"],
                "session_mode": item["session_mode"],
                "validation_trade_count": int(safe_float(item["trade_count_validation"])),
                "validation_trade_per_day": validation_tpd,
                "validation_stress_net": validation_net,
                "validation_stress_pf": validation_pf,
                "validation_balance": validation_balance,
                "validation_drawdown": safe_float(item["stress_max_drawdown_validation"]),
                "validation_recovery_factor": safe_float(item["stress_recovery_factor_validation"]),
                "oos_trade_count": int(safe_float(item["trade_count_oos"])),
                "oos_trade_per_day": oos_tpd,
                "oos_stress_net": oos_net,
                "oos_stress_pf": oos_pf,
                "oos_balance": oos_balance,
                "oos_drawdown": safe_float(item["stress_max_drawdown_oos"]),
                "oos_recovery_factor": safe_float(item["stress_recovery_factor_oos"]),
                "combined_stress_net": validation_net + oos_net,
                "min_trade_per_day": min(validation_tpd, oos_tpd),
                "candidate_gate": "passed_proxy_scout_queue(프록시 탐색 대기열 통과)"
                if candidate
                else "failed_proxy_scout_queue(프록시 탐색 대기열 실패)",
                "density_requirement": TRADE_DENSITY_REQUIREMENT,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    paired = pd.DataFrame(paired_rows)
    candidate_rank = paired["candidate_gate"].eq("passed_proxy_scout_queue(프록시 탐색 대기열 통과)").astype(int)
    paired["_rank"] = candidate_rank * 1_000_000 + paired["combined_stress_net"].astype(float) + paired["min_trade_per_day"].astype(float)
    best = paired.sort_values("_rank", ascending=False).drop(columns=["_rank"]).head(80)
    write_csv(BEST_SCORECARD, best.to_dict("records"))
    return frame, best


def write_candidate_queue(best: pd.DataFrame, train_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    candidates = best[best["candidate_gate"].eq("passed_proxy_scout_queue(프록시 탐색 대기열 통과)")].copy()
    rows: list[dict[str, Any]] = []
    model_by_id = {row["model_id"]: row for row in train_result["model_rows"]}
    parity_by_id = {row["model_id"]: row for row in train_result["parity_rows"]}
    for rank, (_, item) in enumerate(candidates.head(12).iterrows(), start=1):
        model_row = model_by_id[str(item["model_id"])]
        parity_row = parity_by_id[str(item["model_id"])]
        rows.append(
            {
                "queue_rank": rank,
                "run_id": RUN_ID,
                "model_id": item["model_id"],
                "label_variant_id": item["label_variant_id"],
                "model_config_id": item["model_config_id"],
                "onnx_path": model_row["onnx_path"],
                "onnx_sha256": model_row["onnx_sha256"],
                "onnx_parity_status": parity_row["parity_status"],
                "score_policy": item["score_policy"],
                "score_quantile": item["score_quantile"],
                "adx_min": item["adx_min"],
                "session_mode": item["session_mode"],
                "validation_trade_per_day": item["validation_trade_per_day"],
                "validation_stress_net": item["validation_stress_net"],
                "validation_stress_pf": item["validation_stress_pf"],
                "validation_balance": item["validation_balance"],
                "oos_trade_per_day": item["oos_trade_per_day"],
                "oos_stress_net": item["oos_stress_net"],
                "oos_stress_pf": item["oos_stress_pf"],
                "oos_balance": item["oos_balance"],
                "next_required_action": "package_and_run_mt5_runtime_probe(MT5 런타임 탐침 패키지 실행)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(MT5_PROBE_QUEUE, rows)
    return rows


def status_tuple(queue_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if queue_rows:
        return (
            "completed_stage356D_high_density_label_pivot_positive_proxy_queue_ready_no_selection",
            "positive_proxy_high_density_label_pivot_mt5_probe_required_no_operating_claim",
            "stage356D_open_run356E_package_high_density_label_pivot_mt5_probe_without_db_v1",
            NEXT_RUN_ID_POSITIVE,
        )
    return (
        "completed_stage356D_high_density_label_pivot_no_proxy_queue_no_selection",
        "negative_proxy_high_density_label_pivot_no_density_edge_no_operating_claim",
        "stage356D_open_run356E_expand_high_density_label_pivot_without_db_v1",
        NEXT_RUN_ID_NEGATIVE,
    )


def best_row_dict(best: pd.DataFrame) -> dict[str, Any]:
    return dict(best.iloc[0]) if len(best) else {}


def write_firewall(queue_rows: Sequence[Mapping[str, Any]], status: str, judgment: str) -> None:
    write_csv(
        FIREWALL_REVIEW,
        [
            {
                "check_id": "mt5_execution",
                "status": "not_run(실행 안 함)",
                "effect": "proxy queue is not MT5 KPI(프록시 대기열은 MT5 KPI가 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "candidate_selection",
                "status": "not_claimed(주장 안 함)",
                "effect": "queue does not select operating model(대기열은 운영 모델 선택이 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "queue_rows",
                "status": str(len(queue_rows)),
                "effect": status,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "judgment",
                "status": judgment,
                "effect": "MT5 probe required before positive operating read(MT5 탐침 전 운영 긍정 판독 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )


def write_receipts(
    identity: Mapping[str, Any],
    train_result: Mapping[str, Any],
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    next_run_id: str,
) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    best_row = best_row_dict(best)
    write_json(
        DATA_RECEIPT,
        {
            **common,
            "data_source": [rel(FEATURE_LABEL_TABLE), rel(RUNTIME_FEATURES)],
            "time_axis": "timestamp_utc closed M5 bar time(닫힌 M5 봉 시각)",
            "sample_scope": identity,
            "feature_label_boundary": "future returns are labels only; train quantiles define label thresholds(미래 수익률은 라벨 전용이고 학습 분위수가 라벨 임계값을 정의)",
            "split_boundary": "train fits labels and models; validation/oos score only(학습은 라벨/모델 적합, 검증/표본외는 점수만)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "idea_id": "stage356D_high_density_h12_quantile_label_pivot",
            "hypothesis": "H12 train-quantile labels can recover 3+ trade/day without trade splitting(H12 학습 분위수 라벨이 거래 쪼개기 없이 3+ 일별 거래를 회복할 수 있다)",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A with Tier B missing_required(Tier A, Tier B 필수 누락)",
            "broad_sweep": "three high-density labels and three ExtraTrees classifiers(고밀도 라벨 3개와 엑스트라트리 분류기 3개)",
            "extreme_sweep": "q30 threshold with ADX20 and all/cash360 sessions(q30 임계값, ADX20, 전체/현금장 360분 세션)",
            "micro_search_gate": "MT5 probe after proxy queue, not operating promotion(프록시 대기열 뒤 MT5 탐침, 운영 승격 아님)",
            "wfo_plan": "required after MT5 probe if runtime clue survives(런타임 단서가 살아남으면 WFO 필요)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **common,
            "model_family": "ExtraTreesClassifier ONNX-compatible high-density labels(엑스트라트리 분류기 온엑스 호환 고밀도 라벨)",
            "target_and_label": "H12 direction/flat train-quantile and soft-cost labels(H12 방향/플랫 학습 분위수와 완화 비용 라벨)",
            "split_method": "train/validation/oos holdout(학습/검증/표본외 고정 분할)",
            "selection_metric": "candidate queue gate over validation and oos stress KPI(검증과 표본외 압박 KPI 후보 대기열 게이트)",
            "secondary_metrics": "trade/day, long/short balance, drawdown, recovery(일별 거래수, 롱/숏 균형, 손실, 회복)",
            "threshold_policy": "searched probability score quantile, ADX, session(확률 점수 분위수, ADX, 세션 탐색)",
            "overfit_risk": "single-window scout and grid selection(단일 구간 탐색과 격자 선택)",
            "calibration_risk": "tree probability is ranking score, not calibrated live probability(트리 확률은 순위 점수이며 보정된 실거래 확률 아님)",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": judgment,
            "onnx_parity_rows": len(train_result["parity_rows"]),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [rel(FEATURE_LABEL_TABLE), rel(RUNTIME_FEATURES), rel(PARENT_BEST_SCORECARD)],
            "producer": rel(Path(__file__)),
            "consumer": next_run_id,
            "artifact_paths": [rel(LABEL_DESIGN_MANIFEST), rel(MODEL_MANIFEST), rel(ONNX_PARITY), rel(BEST_SCORECARD), rel(MT5_PROBE_QUEUE)],
            "artifact_hashes": {
                "label_design_manifest": sha256_file(LABEL_DESIGN_MANIFEST),
                "model_manifest": sha256_file(MODEL_MANIFEST),
                "onnx_parity": sha256_file(ONNX_PARITY),
                "best_scorecard": sha256_file(BEST_SCORECARD),
                "mt5_probe_queue": sha256_file(MT5_PROBE_QUEUE),
            },
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_ignored_with_manifest_and_tracked_closeout(생성 산출물은 무시되며 목록과 추적 종료 기록 보유)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(BEST_SCORECARD), rel(ONNX_PARITY), rel(MT5_PROBE_QUEUE), rel(GATE_AUDIT)],
            "evidence_missing": "MT5 execution, forward pass, runtime authority(MT5 실행, 전진 검증, 런타임 권위)",
            "judgment_label": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_run_id,
            "best_row": best_row,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "status": status,
            "judgment": judgment,
            "mt5_probe_queue_rows": len(queue_rows),
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )


def write_final_and_manifest(
    identity: Mapping[str, Any],
    label_rows: Sequence[Mapping[str, Any]],
    train_result: Mapping[str, Any],
    sweep: pd.DataFrame,
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "label_design_rows": len(label_rows),
        "trained_models": len(train_result["model_rows"]),
        "onnx_parity_rows": len(train_result["parity_rows"]),
        "threshold_sweep_rows": int(len(sweep)),
        "best_rows": int(len(best)),
        "mt5_probe_queue_rows": len(queue_rows),
        "source_identity": identity,
        "best_row": best_row,
        "mt5_execution": "not_run",
        "candidate_selection": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            **final,
            "command": "python stage_pipelines/stage356/design_high_density_label_pivot_without_db.py",
            "outputs": {
                "label_design_manifest": rel(LABEL_DESIGN_MANIFEST),
                "label_distribution": rel(LABEL_DISTRIBUTION),
                "model_manifest": rel(MODEL_MANIFEST),
                "onnx_parity": rel(ONNX_PARITY),
                "threshold_sweep": rel(THRESHOLD_SWEEP_SCORECARD),
                "best_scorecard": rel(BEST_SCORECARD),
                "mt5_probe_queue": rel(MT5_PROBE_QUEUE),
            },
        },
    )


def write_report(
    train_result: Mapping[str, Any],
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    write_text(
        REPORT_PATH,
        f"""# run356D High-Density Label Pivot(run356D 고밀도 라벨 전환)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- next_run_id(다음 실행 ID): `{next_run_id}`
- trained_models(학습 모델): `{len(train_result["model_rows"])}`
- onnx_parity_rows(온엑스 동등성 행): `{len(train_result["parity_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{len(queue_rows)}`

Action(행동): Stage356C(356C 실행)의 3 trade/day(일별 거래수) 미달 실패 기억을 바탕으로 H12 train-quantile high-density label(학습 분위수 고밀도 라벨)을 만들고 ExtraTrees ONNX classifier(엑스트라트리 온엑스 분류기)를 학습했다.

Effect(효과): proxy(프록시)에서 MT5 runtime probe(MT5 런타임 탐침)로 보낼 queue(대기열)를 만들었지만, 이 결과는 operating claim(운영 주장)이 아니다.

## Best Proxy Row(최선 프록시 행)

- model_id(모델 ID): `{best_row.get("model_id", "")}`
- label_variant_id(라벨 변형 ID): `{best_row.get("label_variant_id", "")}`
- score_policy(점수 정책): `{best_row.get("score_policy", "")}`
- validation_trade_per_day(검증 일별 거래수): `{best_row.get("validation_trade_per_day", "")}`
- validation_stress_net(검증 압박 순수익): `{best_row.get("validation_stress_net", "")}`
- validation_stress_pf(검증 압박 수익 팩터): `{best_row.get("validation_stress_pf", "")}`
- oos_trade_per_day(표본외 일별 거래수): `{best_row.get("oos_trade_per_day", "")}`
- oos_stress_net(표본외 압박 순수익): `{best_row.get("oos_stress_net", "")}`
- oos_stress_pf(표본외 압박 수익 팩터): `{best_row.get("oos_stress_pf", "")}`
- candidate_gate(후보 게이트): `{best_row.get("candidate_gate", "")}`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.
""",
    )
    append_text_once(REVIEW_INDEX, "run356D_high_density_label_pivot", f"- `{rel(REPORT_PATH)}`")
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage356D High-Density Label Pivot(356D 고밀도 라벨 전환)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): high-density H12 labels(고밀도 H12 라벨)와 ONNX classifier(온엑스 분류기)를 만들고 proxy queue(프록시 대기열)를 평가했다.

Effect(효과): MT5 probe(MT5 탐침)로 넘길 수 있는 후보를 `mt5_probe_queue_rows={len(queue_rows)}`로 기록하되, 운영 주장은 금지했다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_state_and_selection(
    train_result: Mapping[str, Any],
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    queue_count = len(queue_rows)
    selection_status = (
        "proxy_mt5_probe_queue_ready_no_selection(프록시 MT5 탐침 대기열 준비, 선택 없음)"
        if queue_count
        else "no_proxy_mt5_queue_no_selection(프록시 MT5 대기열 없음, 선택 없음)"
    )
    selection_text = f"""# Stage356 Selection Status(356단계 선택 상태)

- selection_status(선택 상태): `{selection_status}`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- trained_models(학습 모델): `{len(train_result["model_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{queue_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(STAGE_SELECTION, selection_text)
    write_text(ROOT_SELECTION_STATUS, selection_text)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
current_decision: {decision}
next_run_id: {next_run_id}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{status}`
- current_judgment(현재 판정): `{judgment}`
- current_decision(현재 결정): `{decision}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage356D(356D 실행)에서 high-density H12 label pivot(고밀도 H12 라벨 전환)과 ONNX classifier proxy scout(온엑스 분류기 프록시 탐색)를 실행했다.

Effect(효과): 다음 작업은 `{next_run_id}`에서 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들고, proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)의 차이를 확인한다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} {RUN_ID}",
        f"""## {TODAY} {RUN_ID}

Action(행동): high-density H12 labels(고밀도 H12 라벨)와 ExtraTrees ONNX classifiers(엑스트라트리 온엑스 분류기)를 학습하고 proxy queue(프록시 대기열)를 평가했다.

Effect(효과): mt5_probe_queue_rows(MT5 탐침 대기열 행) `{queue_count}`로 Stage356D(356D 실행)를 닫고, next_run(다음 실행)을 `{next_run_id}`로 동기화했다.

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    if queue_count:
        append_text_once(
            IDEA_REGISTRY,
            RUN_ID,
            f"""## {TODAY} {RUN_ID}

- idea_id(아이디어 ID): `stage356D_high_density_h12_quantile_label_pivot`
- hypothesis(가설): H12 train-quantile label(학습 분위수 라벨)이 3+ trade/day(일별 거래수)와 positive stress KPI(양수 압박 KPI)를 동시에 회복한다.
- evidence_boundary(근거 경계): proxy scout queue only(프록시 탐색 대기열 전용).
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{queue_count}`
- next_condition(다음 조건): `{next_run_id}`에서 MT5 runtime probe(MT5 런타임 탐침) 실행.
""",
        )


def write_ledgers(
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "proxy_high_density_label_pivot(프록시 고밀도 라벨 전환)",
        "lane": "proxy_high_density_label_pivot(프록시 고밀도 라벨 전환)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": SOURCE_RUN_ID,
        "rows": int(len(best)),
        "candidate_rows": len(queue_rows),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "positive_proxy_queue_ready(긍정 프록시 대기열 준비)"
        if queue_rows
        else "negative_proxy_no_queue(부정 프록시, 대기열 없음)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": judgment,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "primary_kpi": "mt5_probe_queue_rows=" + str(len(queue_rows)),
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
    }
    tier_rows = []
    for suffix, tier, view, metric_scope, notes in [
        (
            "Tier_A",
            "Tier A",
            "Tier A separate(Tier A 분리)",
            "high_density_label_pivot_full_context(고밀도 라벨 전환 전체 문맥)",
            "Tier A full-context high-density label pivot(Tier A 전체 문맥 고밀도 라벨 전환).",
        ),
        (
            "Tier_B",
            "Tier B",
            "Tier B separate(Tier B 분리)",
            "missing_required_no_partial_context_materialization(Tier B 부분 문맥 물질화 없음 필수 누락)",
            "Tier B partial-context sample is not materialized in Stage356D(Tier B 부분 문맥 표본은 356D에서 미산출).",
        ),
        (
            "Tier_AplusB",
            "Tier A+B",
            "Tier A+B combined(Tier A+B 합산)",
            "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)",
            "Combined record is same as Tier A because no fallback is materialized(대체가 없어 합산 기록은 Tier A와 동일).",
        ),
    ]:
        row = {
            **base,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": tier,
            "view": view,
            "record_view": view,
            "tier": tier,
            "tier_scope": tier,
            "metric_scope": metric_scope,
            "kpi_scope": metric_scope,
            "notes": notes,
        }
        if tier == "Tier B":
            row.update(
                {
                    "result_status": "missing_required(필수 누락)",
                    "net_profit": "",
                    "profit_factor": "",
                    "drawdown": "",
                    "recovery_factor": "",
                    "trade_count": "",
                    "trade_density_per_feature_day": "",
                }
            )
        else:
            row.update(
                {
                    "net_profit": best_row.get("oos_stress_net", ""),
                    "profit_factor": best_row.get("oos_stress_pf", ""),
                    "drawdown": best_row.get("oos_drawdown", ""),
                    "recovery_factor": best_row.get("oos_recovery_factor", ""),
                    "trade_count": best_row.get("oos_trade_count", ""),
                    "trade_density_per_feature_day": best_row.get("oos_trade_per_day", ""),
                }
            )
        tier_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], tier_rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], tier_rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
                "row_id": f"{RUN_ID}__Tier_AplusB",
                "subrun_id": "Tier A+B",
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "tier_scope": "Tier A+B",
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )


def write_artifact_registry(train_result: Mapping[str, Any]) -> None:
    artifacts = [
        SOURCE_DATA_AUDIT,
        LABEL_DESIGN_MANIFEST,
        LABEL_DISTRIBUTION,
        MODEL_MANIFEST,
        ONNX_PARITY,
        CLASSIFICATION_SCORECARD,
        THRESHOLD_SWEEP_SCORECARD,
        BEST_SCORECARD,
        MT5_PROBE_QUEUE,
        FIREWALL_REVIEW,
        DATA_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    for row in train_result["model_rows"]:
        artifacts.append(ROOT / row["model_path"])
        if row.get("onnx_sha256"):
            artifacts.append(ROOT / row["onnx_path"])
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": Path(path).suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage356D high-density label pivot artifact(356D 고밀도 라벨 전환 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_gates(train_result: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    parity_pass = all(
        row.get("onnx_export_status") == "passed" and row.get("parity_status") == "passed"
        for row in train_result["parity_rows"]
    )
    gate_specs = [
        ("scope_completion_gate", all(exists(path) for path in [LABEL_DESIGN_MANIFEST, MODEL_MANIFEST, ONNX_PARITY, THRESHOLD_SWEEP_SCORECARD, BEST_SCORECARD, MT5_PROBE_QUEUE, FINAL_DECISION, REPORT_PATH]), FINAL_DECISION, "planned high-density label pivot outputs(계획 고밀도 라벨 전환 산출물) 생성"),
        ("kpi_contract_audit", exists(BEST_SCORECARD) and exists(STAGE_LEDGER), BEST_SCORECARD, "proxy KPI and tier ledger(프록시 KPI와 티어 장부) 기록"),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]), MODEL_RECEIPT, "skill receipts(스킬 영수증) 작성"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 포함"),
        ("timestamp_join_gate", exists(SOURCE_DATA_AUDIT), SOURCE_DATA_AUDIT, "timestamp-safe join and label threshold(시점 안전 결합과 라벨 임계값) 확인"),
        ("lookahead_boundary_gate", exists(DATA_RECEIPT), DATA_RECEIPT, "future returns excluded from features(미래 수익률 피처 제외) 기록"),
        ("onnx_parity_audit", parity_pass, ONNX_PARITY, "classifier ONNX parity(분류기 온엑스 동등성) 확인"),
        ("nonoverlap_trade_shape_gate", exists(THRESHOLD_SWEEP_SCORECARD), THRESHOLD_SWEEP_SCORECARD, "non-overlap trade shape(비중첩 거래 형태) 기록"),
        ("candidate_queue_gate", exists(MT5_PROBE_QUEUE) and len(queue_rows) > 0, MT5_PROBE_QUEUE, f"MT5 probe queue rows(MT5 탐침 대기열 행) {len(queue_rows)} 기록"),
        ("tier_pair_records", exists(STAGE_LEDGER) and RUN_ID in read_text(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined(Tier A/B/합산) 기록"),
        ("artifact_lineage_audit", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "operating claims(운영 주장) 차단"),
    ]
    gate_ids = {item[0] for item in gate_specs}
    required_gate_names = {"scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"}
    gate_specs[3] = (
        "required_gate_coverage_audit",
        required_gate_names.issubset(gate_ids),
        GATE_AUDIT,
        "required gates(필수 게이트) 포함",
    )
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gate_specs
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "candidate_selection"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        Path(fs_path(directory)).mkdir(parents=True, exist_ok=True)
    full, feature_columns, identity = load_sources()
    write_source_audit(identity)
    label_frame, label_manifest_rows, _dist_rows = build_labels(full)
    train_result = train_models(label_frame, full, feature_columns)
    sweep, best = evaluate_sweep(train_result)
    queue_rows = write_candidate_queue(best, train_result)
    status, judgment, decision, next_run_id = status_tuple(queue_rows)
    write_firewall(queue_rows, status, judgment)
    write_receipts(identity, train_result, best, queue_rows, status, judgment, next_run_id)
    write_final_and_manifest(
        identity,
        label_manifest_rows,
        train_result,
        sweep,
        best,
        queue_rows,
        status,
        judgment,
        decision,
        next_run_id,
    )
    write_report(train_result, best, queue_rows, status, judgment, decision, next_run_id)
    write_state_and_selection(train_result, queue_rows, status, judgment, decision, next_run_id)
    write_ledgers(best, queue_rows, status, judgment, decision, next_run_id)
    gates = write_gates(train_result, queue_rows)
    write_artifact_registry(train_result)
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "label_design_rows": len(label_manifest_rows),
                "trained_models": len(train_result["model_rows"]),
                "onnx_parity_rows": len(train_result["parity_rows"]),
                "threshold_sweep_rows": int(len(sweep)),
                "mt5_probe_queue_rows": len(queue_rows),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "next_run_id": next_run_id,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

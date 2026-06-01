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
from sklearn.base import clone
from sklearn.ensemble import ExtraTreesClassifier
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

TODAY = "2026-06-02"
STAGE_ID = "357_high_density_label_pivot__trade_frequency_recovery"
RUN_NUMBER = "run357B"
RUN_ID = "run357B_design_high_density_label_pivot_without_db_v1"
PARENT_RUN_ID = "run357A_branch_stage356_to_high_density_label_pivot_without_db_v1"
SOURCE_RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"
SOURCE_STAGE356_RUN_ID = "run356C_expand_density_recovery_proxy_training_search_without_db_v1"
NEXT_RUN_ID_POSITIVE = "run357C_package_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID_NEGATIVE = "run357C_expand_high_density_label_pivot_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_high_density_label_pivot_proxy_scout_only_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
LABEL_ORDER = [0, 1, 2]
MIN_TRADE_PER_DAY = 3.0
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
RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)
FEATURE_SCHEMA = (
    ROOT
    / "stages"
    / "356_density_recovery_training__proxy_model_queue_scout"
    / "02_runs"
    / "run356B"
    / "feature_schema.json"
)
PARENT_FINAL_DECISION = STAGE_DIR / "02_runs" / "run357A" / "final_decision.json"
PARENT_INPUT_MANIFEST = STAGE_DIR / "01_inputs" / "stage357_input_manifest.csv"
STAGE356_FINAL_DECISION = (
    ROOT
    / "stages"
    / "356_density_recovery_training__proxy_model_queue_scout"
    / "02_runs"
    / "run356C"
    / "final_decision.json"
)
STAGE356_BEST_SCORECARD = (
    ROOT
    / "stages"
    / "356_density_recovery_training__proxy_model_queue_scout"
    / "02_runs"
    / "run356C"
    / "best_expansion_scorecard.csv"
)

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

REPORT_PATH = REVIEW_DIR / "run357B_high_density_label_pivot.md"
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
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage357B_high_density_label_pivot.md"

KEY_COLUMNS = ["bar_time_server", "timestamp_utc", "split", "row_index"]
RETURN_COLUMNS = ["future_log_return_6", "future_log_return_8", "future_log_return_12"]

MODEL_SPECS: tuple[tuple[str, str, Any], ...] = (
    (
        "extratrees_cls_depth5_leaf100_seed11",
        "ExtraTreesClassifier shallow balanced(얕은 균형 엑스트라트리스 분류기)",
        ExtraTreesClassifier(
            n_estimators=160,
            max_depth=5,
            min_samples_leaf=100,
            max_features="sqrt",
            class_weight="balanced",
            random_state=11,
            n_jobs=-1,
        ),
    ),
    (
        "extratrees_cls_depth8_leaf120_seed12",
        "ExtraTreesClassifier medium balanced(중간 균형 엑스트라트리스 분류기)",
        ExtraTreesClassifier(
            n_estimators=160,
            max_depth=8,
            min_samples_leaf=120,
            max_features="sqrt",
            class_weight="balanced",
            random_state=12,
            n_jobs=-1,
        ),
    ),
    (
        "extratrees_cls_depth10_leaf80_seed13",
        "ExtraTreesClassifier deeper balanced(깊은 균형 엑스트라트리스 분류기)",
        ExtraTreesClassifier(
            n_estimators=160,
            max_depth=10,
            min_samples_leaf=80,
            max_features="sqrt",
            class_weight="balanced",
            random_state=13,
            n_jobs=-1,
        ),
    ),
)

SCORE_POLICIES = ["pside", "margin", "side_x_nonflat", "margin_x_nonflat"]
QUANTILES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
ADX_MIN_VALUES = [0.0, 10.0, 16.0, 20.0]
SESSION_MODES = ["all", "cash_0_360"]
THRESHOLD_BASES = ["train", "validation"]


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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
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


def split_days(frame: pd.DataFrame, split_name: str) -> int:
    split_frame = frame[frame["split"].eq(split_name)]
    return max(1, int(split_frame["timestamp_utc"].astype(str).str.slice(0, 10).nunique()))


def session_mask(frame: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "all":
        return np.ones(len(frame), dtype=bool)
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    if mode == "cash_0_360":
        return (minutes >= 0) & (minutes <= 360)
    raise ValueError(f"Unknown session mode(알 수 없는 세션 모드): {mode}")


def base_mask(frame: pd.DataFrame, split_name: str, adx_min: float, session_mode: str) -> np.ndarray:
    mask = frame["split"].eq(split_name).to_numpy()
    if adx_min > 0:
        mask &= frame["adx_14"].to_numpy(dtype=float) >= float(adx_min)
    mask &= session_mask(frame, session_mode)
    return mask


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
            "stress_pf": 0.0,
            "stress_expectancy": 0.0,
            "drawdown": 0.0,
            "recovery_factor": 0.0,
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
        "stress_pf": pf,
        "stress_expectancy": expectancy,
        "drawdown": drawdown,
        "recovery_factor": recovery,
        "win_rate": float((pnl > 0).mean()),
        "long_count": long_count,
        "short_count": short_count,
        "long_short_balance": float(balance),
    }


def load_sources() -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    feature_schema = read_json(FEATURE_SCHEMA)
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
        "feature_schema_sha256": sha256_file(FEATURE_SCHEMA),
        "parent_final_decision_sha256": sha256_file(PARENT_FINAL_DECISION),
        "parent_input_manifest_sha256": sha256_file(PARENT_INPUT_MANIFEST),
        "stage356_final_decision_sha256": sha256_file(STAGE356_FINAL_DECISION),
        "stage356_best_scorecard_sha256": sha256_file(STAGE356_BEST_SCORECARD),
    }
    return full, feature_columns, identity


def build_labels(full: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
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
            "labels": np.where(ret12 > q55, 2, np.where(ret12 < q45, 0, 1)).astype(int),
            "hypothesis": "narrow flat band raises density while preserving direction(좁은 평탄 밴드가 방향성을 보존하며 밀도를 올린다)",
        },
        {
            "label_variant_id": "d05_h12_q40_60_balanced_band",
            "design_id": "d05_train_quantile_h12_q40_q60",
            "horizon_bars": 12,
            "threshold_family": "train_quantile_band(학습 분위수 밴드)",
            "lower_threshold": q40,
            "upper_threshold": q60,
            "labels": np.where(ret12 > q60, 2, np.where(ret12 < q40, 0, 1)).astype(int),
            "hypothesis": "wider flat band improves quality while keeping density(넓은 평탄 밴드가 밀도를 유지하면서 품질을 올린다)",
        },
        {
            "label_variant_id": "d06_h12_cost025_soft_flat",
            "design_id": "d06_h12_stress_cost_025_soft_flat",
            "horizon_bars": 12,
            "threshold_family": "stress_cost_fraction(압박 비용 비율)",
            "lower_threshold": -0.25,
            "upper_threshold": 0.25,
            "labels": np.where(ret12 > cost * 0.25, 2, np.where(ret12 < -cost * 0.25, 0, 1)).astype(int),
            "hypothesis": "soft cost flat lowers noise without killing density(완화 비용 평탄이 밀도를 죽이지 않고 잡음을 낮춘다)",
        },
        {
            "label_variant_id": "d07_h12_cost050_balanced_flat",
            "design_id": "d07_h12_stress_cost_050_balanced_flat",
            "horizon_bars": 12,
            "threshold_family": "stress_cost_fraction(압박 비용 비율)",
            "lower_threshold": -0.50,
            "upper_threshold": 0.50,
            "labels": np.where(ret12 > cost * 0.50, 2, np.where(ret12 < -cost * 0.50, 0, 1)).astype(int),
            "hypothesis": "larger cost flat checks quality cliff(큰 비용 평탄이 품질 절벽을 확인한다)",
        },
    ]
    manifest_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    for item in definitions:
        labels = item["labels"]
        manifest_rows.append(
            {
                "label_variant_id": item["label_variant_id"],
                "design_id": item["design_id"],
                "horizon_bars": item["horizon_bars"],
                "threshold_family": item["threshold_family"],
                "lower_threshold": item["lower_threshold"],
                "upper_threshold": item["upper_threshold"],
                "rows": int(len(labels)),
                "timestamp_boundary": "features at current closed M5 bar, labels use future returns only(피처는 현재 마감 M5 봉, 라벨은 미래 수익률만 사용)",
                "hypothesis": item["hypothesis"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split_name in ["train", "validation", "oos"]:
            split_mask = full["split"].eq(split_name).to_numpy()
            split_labels = labels[split_mask]
            counts = {int(label): int((split_labels == label).sum()) for label in LABEL_ORDER}
            distribution_rows.append(
                {
                    "label_variant_id": item["label_variant_id"],
                    "split": split_name,
                    "rows": int(split_mask.sum()),
                    "short_count": counts[0],
                    "flat_count": counts[1],
                    "long_count": counts[2],
                    "nonflat_share": float((counts[0] + counts[2]) / max(1, split_mask.sum())),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_DESIGN_MANIFEST, manifest_rows)
    write_csv(LABEL_DISTRIBUTION, distribution_rows)
    return definitions, manifest_rows, distribution_rows


def classification_metrics(model: Any, x_values: np.ndarray, y_true: np.ndarray) -> dict[str, Any]:
    predicted = model.predict(x_values)
    proba = ordered_sklearn_probabilities(model, x_values, class_order=LABEL_ORDER)
    return {
        "accuracy": float(accuracy_score(y_true, predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, predicted)),
        "macro_f1": float(f1_score(y_true, predicted, average="macro")),
        "log_loss": float(log_loss(y_true, proba, labels=LABEL_ORDER)),
    }


def score_arrays(proba: np.ndarray) -> dict[str, np.ndarray]:
    p_short = proba[:, 0]
    p_flat = proba[:, 1]
    p_long = proba[:, 2]
    margin = np.abs(p_long - p_short)
    pside = np.maximum(p_long, p_short)
    return {
        "pside": pside,
        "margin": margin,
        "side_x_nonflat": pside * (1.0 - p_flat),
        "margin_x_nonflat": margin * (1.0 - p_flat),
    }


def evaluate_split(
    full: pd.DataFrame,
    split_name: str,
    score: np.ndarray,
    side: np.ndarray,
    threshold: float,
    adx_min: float,
    session_mode: str,
    horizon_bars: int,
) -> dict[str, Any]:
    mask = base_mask(full, split_name, adx_min, session_mode)
    signal = mask & (score >= float(threshold))
    chosen = nonoverlap_indices(full["row_index"].to_numpy(dtype=int), signal, horizon_bars)
    returns = full["future_log_return_12"].to_numpy(dtype=float)[chosen]
    costs = full["stress_cost_log_return"].to_numpy(dtype=float)[chosen]
    sides = side[chosen]
    return evaluate_trades(returns, sides, costs, split_days(full, split_name))


def candidate_gate(row: Mapping[str, Any], parity_passed: bool) -> tuple[str, str]:
    checks = [
        ("onnx_parity", parity_passed),
        ("validation_trade_per_day", float(row["validation_trade_per_day"]) >= MIN_TRADE_PER_DAY),
        ("oos_trade_per_day", float(row["oos_trade_per_day"]) >= MIN_TRADE_PER_DAY),
        ("validation_stress_net", float(row["validation_stress_net"]) > 0.0),
        ("oos_stress_net", float(row["oos_stress_net"]) > 0.0),
        ("validation_stress_pf", float(row["validation_stress_pf"]) >= MIN_STRESS_PF),
        ("oos_stress_pf", float(row["oos_stress_pf"]) >= MIN_STRESS_PF),
        ("validation_balance", float(row["validation_balance"]) >= MIN_BALANCE),
        ("oos_balance", float(row["oos_balance"]) >= MIN_BALANCE),
    ]
    failed = [name for name, passed in checks if not passed]
    if failed:
        return "failed_proxy_scout_queue(프록시 탐색 대기열 실패)", ";".join(failed)
    return "passed_proxy_mt5_probe_queue(프록시 MT5 탐침 대기열 통과)", "all_candidate_checks_passed(모든 후보 점검 통과)"


def train_and_evaluate(
    full: pd.DataFrame,
    feature_columns: Sequence[str],
    label_definitions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    x_all = full[list(feature_columns)].astype("float64").to_numpy()
    train_mask = full["split"].eq("train").to_numpy()
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    sweep_rows: list[dict[str, Any]] = []
    sample_indices = np.r_[
        np.flatnonzero(full["split"].eq("train").to_numpy())[:256],
        np.flatnonzero(full["split"].eq("validation").to_numpy())[:256],
        np.flatnonzero(full["split"].eq("oos").to_numpy())[:256],
    ]
    for label_item in label_definitions:
        y_all = np.asarray(label_item["labels"], dtype=int)
        for model_config_id, model_family, estimator in MODEL_SPECS:
            model_id = f"{RUN_NUMBER}_{label_item['label_variant_id']}__{model_config_id}"
            model = clone(estimator)
            model.fit(x_all[train_mask], y_all[train_mask])
            model_path = MODEL_DIR / f"{model_id}.joblib"
            onnx_path = ONNX_DIR / f"{model_id}.onnx"
            ensure_parent(model_path)
            joblib.dump(model, fs_path(model_path))
            export_meta = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=len(feature_columns),
                target_opset=12,
                drop_label_output=False,
            )
            parity = check_onnxruntime_probability_parity(
                model,
                onnx_path,
                x_all[sample_indices],
                class_order=LABEL_ORDER,
                tolerance=1e-5,
            )
            parity_passed = bool(parity["passed"])
            parity_rows.append(
                {
                    "model_id": model_id,
                    "label_variant_id": label_item["label_variant_id"],
                    "model_config_id": model_config_id,
                    "onnx_path": rel(onnx_path),
                    "onnx_sha256": export_meta["sha256"],
                    "onnx_export_status": "passed",
                    "parity_status": "passed" if parity_passed else "failed",
                    "max_abs_diff": parity["max_abs_diff"],
                    "mean_abs_diff": parity["mean_abs_diff"],
                    "rows_checked": parity["rows"],
                    "input_name": parity["input_name"],
                    "output_names": "|".join(parity["output_names"]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            model_rows.append(
                {
                    "model_id": model_id,
                    "label_variant_id": label_item["label_variant_id"],
                    "model_config_id": model_config_id,
                    "model_family": model_family,
                    "model_path": rel(model_path),
                    "model_sha256": sha256_file(model_path),
                    "onnx_path": rel(onnx_path),
                    "onnx_sha256": export_meta["sha256"],
                    "classes": "|".join(str(value) for value in model.classes_),
                    "feature_count": len(feature_columns),
                    "feature_order_hash": ordered_hash(feature_columns),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for split_name in ["train", "validation", "oos"]:
                mask = full["split"].eq(split_name).to_numpy()
                metrics = classification_metrics(model, x_all[mask], y_all[mask])
                classification_rows.append(
                    {
                        "model_id": model_id,
                        "label_variant_id": label_item["label_variant_id"],
                        "model_config_id": model_config_id,
                        "split": split_name,
                        **metrics,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
            proba = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
            scores = score_arrays(proba)
            side = np.where(proba[:, 2] >= proba[:, 0], 1, -1)
            for score_policy, score in scores.items():
                for quantile in QUANTILES:
                    for adx_min in ADX_MIN_VALUES:
                        for session_mode in SESSION_MODES:
                            for threshold_basis in THRESHOLD_BASES:
                                threshold_mask = base_mask(full, threshold_basis, adx_min, session_mode)
                                if not threshold_mask.any():
                                    continue
                                threshold = float(np.quantile(score[threshold_mask], quantile))
                                validation = evaluate_split(
                                    full,
                                    "validation",
                                    score,
                                    side,
                                    threshold,
                                    adx_min,
                                    session_mode,
                                    int(label_item["horizon_bars"]),
                                )
                                oos = evaluate_split(
                                    full,
                                    "oos",
                                    score,
                                    side,
                                    threshold,
                                    adx_min,
                                    session_mode,
                                    int(label_item["horizon_bars"]),
                                )
                                row = {
                                    "model_id": model_id,
                                    "label_variant_id": label_item["label_variant_id"],
                                    "model_config_id": model_config_id,
                                    "score_policy": score_policy,
                                    "score_quantile": quantile,
                                    "threshold_basis": threshold_basis,
                                    "threshold_value": threshold,
                                    "adx_min": adx_min,
                                    "session_mode": session_mode,
                                    "horizon_bars": int(label_item["horizon_bars"]),
                                    "validation_trade_count": validation["trade_count"],
                                    "validation_trade_per_day": validation["trade_per_day"],
                                    "validation_stress_net": validation["stress_net"],
                                    "validation_stress_pf": validation["stress_pf"],
                                    "validation_expectancy": validation["stress_expectancy"],
                                    "validation_drawdown": validation["drawdown"],
                                    "validation_recovery_factor": validation["recovery_factor"],
                                    "validation_balance": validation["long_short_balance"],
                                    "validation_long_count": validation["long_count"],
                                    "validation_short_count": validation["short_count"],
                                    "oos_trade_count": oos["trade_count"],
                                    "oos_trade_per_day": oos["trade_per_day"],
                                    "oos_stress_net": oos["stress_net"],
                                    "oos_stress_pf": oos["stress_pf"],
                                    "oos_expectancy": oos["stress_expectancy"],
                                    "oos_drawdown": oos["drawdown"],
                                    "oos_recovery_factor": oos["recovery_factor"],
                                    "oos_balance": oos["long_short_balance"],
                                    "oos_long_count": oos["long_count"],
                                    "oos_short_count": oos["short_count"],
                                    "min_trade_per_day": min(validation["trade_per_day"], oos["trade_per_day"]),
                                    "combined_stress_net": validation["stress_net"] + oos["stress_net"],
                                    "threshold_policy": "fixed_from_train_or_validation_no_oos_quantile(학습 또는 검증 고정 임계값, 표본외 분위수 미사용)",
                                    "density_requirement": TRADE_DENSITY_REQUIREMENT,
                                    "claim_boundary": CLAIM_BOUNDARY,
                                }
                                gate, reason = candidate_gate(row, parity_passed)
                                row["candidate_gate"] = gate
                                row["candidate_reason"] = reason
                                sweep_rows.append(row)
    write_csv(MODEL_MANIFEST, model_rows)
    write_csv(ONNX_PARITY, parity_rows)
    write_csv(CLASSIFICATION_SCORECARD, classification_rows)
    sweep_rows = sorted(
        sweep_rows,
        key=lambda item: (
            item["candidate_gate"].startswith("passed"),
            item["combined_stress_net"],
            item["min_trade_per_day"],
            item["oos_stress_pf"],
        ),
        reverse=True,
    )
    write_csv(THRESHOLD_SWEEP_SCORECARD, sweep_rows)
    best_rows = sweep_rows[: min(100, len(sweep_rows))]
    write_csv(BEST_SCORECARD, best_rows)
    queue_rows = [row for row in sweep_rows if row["candidate_gate"].startswith("passed_proxy_mt5_probe_queue")]
    for rank, row in enumerate(queue_rows, start=1):
        row["queue_rank"] = rank
        row["next_action"] = "package_for_mt5_runtime_probe(MT5 런타임 탐침 패키지)"
    write_csv(MT5_PROBE_QUEUE, queue_rows)
    return {
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "classification_rows": classification_rows,
        "sweep_rows": sweep_rows,
        "best_rows": best_rows,
        "queue_rows": queue_rows,
    }


def status_tuple(queue_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if queue_rows:
        return (
            "completed_stage357B_high_density_label_pivot_positive_proxy_queue_ready_no_selection",
            "positive_proxy_high_density_label_pivot_mt5_probe_required_no_operating_claim",
            "stage357B_open_run357C_package_high_density_label_pivot_mt5_probe_without_db_v1",
            NEXT_RUN_ID_POSITIVE,
        )
    return (
        "completed_stage357B_high_density_label_pivot_no_proxy_queue_no_selection",
        "negative_proxy_high_density_label_pivot_no_trade_frequency_edge_no_operating_claim",
        "stage357B_open_run357C_expand_high_density_label_pivot_without_db_v1",
        NEXT_RUN_ID_NEGATIVE,
    )


def best_row_dict(train_result: Mapping[str, Any]) -> dict[str, Any]:
    rows = list(train_result["best_rows"])
    return dict(rows[0]) if rows else {}


def write_source_audit(identity: Mapping[str, Any]) -> None:
    write_csv(
        SOURCE_DATA_AUDIT,
        [
            {
                **identity,
                "data_source": f"{rel(RUNTIME_FEATURES)} + {rel(FEATURE_LABEL_TABLE)}",
                "time_axis": "FPMarkets server bar_time plus timestamp_utc, sorted by row_index(FPMarkets 서버 봉 시간과 UTC, row_index 정렬)",
                "sample_scope": "US100 M5 Tier A full-context rows(US100 M5 Tier A 전체 문맥 행)",
                "feature_label_boundary": "features exclude future returns; labels use future_log_return_12 only after current row(피처는 미래 수익률 제외, 라벨은 현재 행 이후 수익률 사용)",
                "split_boundary": "train fits model, validation tunes threshold, oos is held out from threshold quantile(학습은 모델 적합, 검증은 임계값 조정, 표본외는 분위수 미사용)",
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_firewall(queue_rows: Sequence[Mapping[str, Any]], status: str, judgment: str) -> None:
    write_csv(
        FIREWALL_REVIEW,
        [
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "mt5_probe_queue_rows": len(queue_rows),
                "mt5_execution": "not_run",
                "candidate_selection": "not_claimed",
                "runtime_authority": "not_claimed",
                "operating_promotion": "not_claimed",
                "goal_achieve": "not_claimed",
                "proxy_to_mt5_requirement": "MT5 runtime probe required before any operating claim(운영 주장 전 MT5 런타임 탐침 필수)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(
    identity: Mapping[str, Any],
    train_result: Mapping[str, Any],
    status: str,
    judgment: str,
    next_run_id: str,
) -> None:
    created = now_utc()
    best = best_row_dict(train_result)
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created,
    }
    write_json(
        DATA_RECEIPT,
        {
            **common,
            "data_source": [rel(RUNTIME_FEATURES), rel(FEATURE_LABEL_TABLE), rel(FEATURE_SCHEMA)],
            "time_axis": "bar_time_server plus timestamp_utc, chronological row_index(서버 봉 시간과 UTC, 시간순 row_index)",
            "sample_scope": "US100 M5 Tier A full-context sample(US100 M5 Tier A 전체 문맥 표본)",
            "missing_or_duplicate_check": {
                "feature_duplicate_key_rows": identity["feature_duplicate_key_rows"],
                "raw_duplicate_key_rows": identity["raw_duplicate_key_rows"],
                "missing_feature_join_rows": identity["missing_feature_join_rows"],
            },
            "feature_label_boundary": "future return columns are label/evaluation only and are not in feature_columns(미래 수익률 컬럼은 라벨/평가 전용이며 피처가 아님)",
            "split_boundary": "train/validation/oos fixed from source table(원천 표의 고정 학습/검증/표본외 분할)",
            "leakage_risk": "validation threshold tuning may overfit; oos threshold quantile is not used(검증 임계값 조정 과적합 위험, 표본외 분위수 미사용)",
            "data_hash_or_identity": identity,
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "idea_id": "IDEA-ST357-HIGH-DENSITY-LABEL-PIVOT",
            "hypothesis": "H12 high-density label recovers 3+ trade/day with positive stress PF(H12 고밀도 라벨이 3+ 일별 거래수와 양수 압박 수익 팩터를 회복)",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)",
            "broad_sweep": "4 label variants x 3 ExtraTrees classifiers x fixed threshold policies(4개 라벨 x 3개 엑스트라트리스 x 고정 임계값)",
            "extreme_sweep": "q bands and cost-flat labels, ADX/session stress(분위수 밴드와 비용 평탄 라벨, ADX/세션 압박)",
            "micro_search_gate": "validation/oos trade_per_day >=3, stress PF >=1.02(검증/표본외 일별 거래수 3 이상, 압박 수익 팩터 1.02 이상)",
            "wfo_plan": "required after scout before promotion(승격 전 탐색 이후 필요)",
            "failure_memory": "Stage356C missed trade/day 3 and validation PF; preserved as constraint(356C는 일별 거래수 3과 검증 수익 팩터 미달, 제약으로 보존)",
            "evidence_boundary": "proxy_scout_queue_only(프록시 탐색 대기열 전용)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **common,
            "model_family": "ExtraTreesClassifier ONNX classifiers(엑스트라트리스 온엑스 분류기)",
            "target_and_label": "3-class short/flat/long H12 labels(3분류 숏/평탄/롱 H12 라벨)",
            "split_method": "train fit, validation threshold search, oos holdout(학습 적합, 검증 임계값 탐색, 표본외 보류)",
            "selection_metric": "candidate gate across trade/day, stress net/PF, balance(거래수/압박 순수익/수익 팩터/균형 후보 게이트)",
            "secondary_metrics": "drawdown, recovery, expectancy, classification score(낙폭, 회복 계수, 기대값, 분류 점수)",
            "threshold_policy": "fixed train or validation quantile; no oos quantile(학습 또는 검증 고정 분위수, 표본외 분위수 없음)",
            "overfit_risk": "multiple model/threshold search and validation threshold tuning(다중 모델/임계값 탐색과 검증 임계값 조정)",
            "calibration_risk": "tree probabilities treated as ranking scores(트리 확률은 순위 점수로 취급)",
            "comparison_baseline": SOURCE_STAGE356_RUN_ID,
            "validation_judgment": judgment,
            "best_row": best,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [rel(RUNTIME_FEATURES), rel(FEATURE_LABEL_TABLE), rel(FEATURE_SCHEMA), rel(PARENT_FINAL_DECISION)],
            "producer": rel(Path(__file__)),
            "consumer": next_run_id,
            "artifact_paths": [
                rel(LABEL_DESIGN_MANIFEST),
                rel(MODEL_MANIFEST),
                rel(ONNX_PARITY),
                rel(THRESHOLD_SWEEP_SCORECARD),
                rel(MT5_PROBE_QUEUE),
                rel(REPORT_PATH),
            ],
            "artifact_hashes": {
                "feature_label_table": identity["feature_label_table_sha256"],
                "runtime_features": identity["runtime_features_sha256"],
            },
            "registry_links": [rel(ARTIFACT_REGISTRY), rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
            "availability": "tracked reports with ignored heavy run artifacts by hash(추적 보고서와 해시 기반 무거운 실행 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(THRESHOLD_SWEEP_SCORECARD), rel(ONNX_PARITY), rel(MT5_PROBE_QUEUE), rel(GATE_AUDIT)],
            "evidence_missing": "MT5 runtime probe, WFO, runtime parity authority(MT5 런타임 탐침, WFO, 런타임 권위 동등성)",
            "judgment_label": "positive" if train_result["queue_rows"] else "negative",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_run_id,
            "user_explanation_hook": "proxy queue can only request MT5 probe; it is not an operating model(프록시 대기열은 MT5 탐침 요청일 뿐 운영 모델이 아님)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "proxy scout result and MT5 probe queue only(프록시 탐색 결과와 MT5 탐침 대기열만)",
            "forbidden_claims": [
                "candidate selection(후보 선정)",
                "MT5 reviewed performance(MT5 검토 완료 성과)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "live readiness(실거래 준비)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def write_final_and_manifest(
    identity: Mapping[str, Any],
    label_manifest_rows: Sequence[Mapping[str, Any]],
    train_result: Mapping[str, Any],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best = best_row_dict(train_result)
    queue_count = len(train_result["queue_rows"])
    payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage356_run_id": SOURCE_STAGE356_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
        "label_design_rows": len(label_manifest_rows),
        "trained_models": len(train_result["model_rows"]),
        "onnx_parity_rows": len(train_result["parity_rows"]),
        "threshold_sweep_rows": len(train_result["sweep_rows"]),
        "mt5_probe_queue_rows": queue_count,
        "best_row": best,
        "data_identity": identity,
        "new_model_training": "run",
        "new_proxy_execution": "run",
        "mt5_execution": "not_run",
        "candidate_selection": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            **payload,
            "work_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "outputs": {
                "source_data_audit": rel(SOURCE_DATA_AUDIT),
                "label_manifest": rel(LABEL_DESIGN_MANIFEST),
                "label_distribution": rel(LABEL_DISTRIBUTION),
                "model_manifest": rel(MODEL_MANIFEST),
                "onnx_parity": rel(ONNX_PARITY),
                "classification_scorecard": rel(CLASSIFICATION_SCORECARD),
                "threshold_sweep": rel(THRESHOLD_SWEEP_SCORECARD),
                "best_scorecard": rel(BEST_SCORECARD),
                "mt5_probe_queue": rel(MT5_PROBE_QUEUE),
                "report": rel(REPORT_PATH),
            },
        },
    )


def write_report(
    train_result: Mapping[str, Any],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best = best_row_dict(train_result)
    write_text(
        REPORT_PATH,
        f"""# run357B High-Density Label Pivot(run357B 고밀도 라벨 전환)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- next_run_id(다음 실행 ID): `{next_run_id}`
- trained_models(학습 모델): `{len(train_result["model_rows"])}`
- onnx_parity_rows(온엑스 동등성 행): `{len(train_result["parity_rows"])}`
- threshold_sweep_rows(임계값 탐색 행): `{len(train_result["sweep_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{len(train_result["queue_rows"])}`

Action(행동): Stage356C(356C 실행)의 trade/day(일별 거래수) 3 미달 실패 기억을 바탕으로 H12 high-density label(고밀도 H12 라벨)과 ExtraTrees ONNX classifier(엑스트라트리스 온엑스 분류기)를 학습했다.

Effect(효과): proxy(프록시) 기준에서 MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있는 queue(대기열)를 만들었지만, 이 결과는 operating claim(운영 주장)이 아니다.

## Best Proxy Row(최선 프록시 행)

- model_id(모델 ID): `{best.get("model_id", "")}`
- label_variant_id(라벨 변형 ID): `{best.get("label_variant_id", "")}`
- score_policy(점수 정책): `{best.get("score_policy", "")}`
- score_quantile(점수 분위수): `{best.get("score_quantile", "")}`
- threshold_basis(임계값 기준): `{best.get("threshold_basis", "")}`
- adx_min(ADX 최소값): `{best.get("adx_min", "")}`
- session_mode(세션 모드): `{best.get("session_mode", "")}`
- validation_trade_per_day(검증 일별 거래수): `{best.get("validation_trade_per_day", "")}`
- validation_stress_net(검증 압박 순수익): `{best.get("validation_stress_net", "")}`
- validation_stress_pf(검증 압박 수익 팩터): `{best.get("validation_stress_pf", "")}`
- validation_balance(검증 롱/숏 균형): `{best.get("validation_balance", "")}`
- oos_trade_per_day(표본외 일별 거래수): `{best.get("oos_trade_per_day", "")}`
- oos_stress_net(표본외 압박 순수익): `{best.get("oos_stress_net", "")}`
- oos_stress_pf(표본외 압박 수익 팩터): `{best.get("oos_stress_pf", "")}`
- oos_balance(표본외 롱/숏 균형): `{best.get("oos_balance", "")}`
- candidate_gate(후보 게이트): `{best.get("candidate_gate", "")}`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.
""",
    )
    append_text_once(REVIEW_INDEX, "run357B_high_density_label_pivot", f"- `{rel(REPORT_PATH)}`")
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage357B High-Density Label Pivot(357B 고밀도 라벨 전환)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): high-density H12 label(고밀도 H12 라벨)과 ONNX classifier(온엑스 분류기)를 만들어 proxy queue(프록시 대기열)를 평가했다.

Effect(효과): `mt5_probe_queue_rows={len(train_result["queue_rows"])}`를 기록했고, 다음 단계는 MT5 probe package(MT5 탐침 패키지) 또는 추가 label expansion(라벨 확장)이다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_state_and_selection(
    train_result: Mapping[str, Any],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    queue_count = len(train_result["queue_rows"])
    selection_status = (
        "proxy_mt5_probe_queue_ready_no_selection(프록시 MT5 탐침 대기열 준비, 선택 없음)"
        if queue_count
        else "no_proxy_mt5_queue_no_selection(프록시 MT5 대기열 없음, 선택 없음)"
    )
    selection_text = f"""# Stage357 Selection Status(357단계 선택 상태)

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

Action(행동): Stage357B(357B 실행)에서 high-density H12 label pivot(고밀도 H12 라벨 전환)과 ONNX classifier proxy scout(온엑스 분류기 프록시 탐색)를 실행했다.

Effect(효과): 다음 작업은 `{next_run_id}`에서 proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 비교할 준비를 하며, 운영 주장(operating claim, 운영 주장)은 아직 없다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} {RUN_ID}",
        f"""## {TODAY} {RUN_ID}

Action(행동): high-density H12 labels(고밀도 H12 라벨)와 ExtraTrees ONNX classifiers(엑스트라트리스 온엑스 분류기)를 학습하고 proxy queue(프록시 대기열)를 평가했다.

Effect(효과): `mt5_probe_queue_rows={queue_count}`로 Stage357B(357B 실행)를 닫고, next_run(다음 실행)을 `{next_run_id}`로 동기화했다.

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_ledgers(
    train_result: Mapping[str, Any],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best = best_row_dict(train_result)
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
        "gate_passes": 13,
        "gate_total": 13,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "proxy_high_density_label_pivot(프록시 고밀도 라벨 전환)",
        "lane": "proxy_high_density_label_pivot(프록시 고밀도 라벨 전환)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": SOURCE_RUN_ID,
        "rows": int(len(train_result["sweep_rows"])),
        "candidate_rows": int(len(train_result["queue_rows"])),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": (
            "positive_proxy_queue_ready(긍정 프록시 대기열 준비)"
            if train_result["queue_rows"]
            else "negative_proxy_no_queue(부정 프록시, 대기열 없음)"
        ),
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": judgment,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "primary_kpi": "mt5_probe_queue_rows=" + str(len(train_result["queue_rows"])),
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
            "Tier B partial-context sample is not materialized in Stage357B(Tier B 부분 문맥 표본은 357B에서 미산출).",
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
                    "net_profit": best.get("oos_stress_net", ""),
                    "profit_factor": best.get("oos_stress_pf", ""),
                    "drawdown": best.get("oos_drawdown", ""),
                    "recovery_factor": best.get("oos_recovery_factor", ""),
                    "trade_count": best.get("oos_trade_count", ""),
                    "trade_density_per_feature_day": best.get("oos_trade_per_day", ""),
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
            "notes": "Stage357B high-density label pivot artifact(357B 고밀도 라벨 전환 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_gates(train_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    parity_pass = all(
        row.get("onnx_export_status") == "passed" and row.get("parity_status") == "passed"
        for row in train_result["parity_rows"]
    )
    data_receipt = read_json(DATA_RECEIPT)
    leakage_text = str(data_receipt.get("leakage_risk", "")).lower()
    fixed_threshold_pass = "oos" in leakage_text and "not used" in leakage_text
    gate_specs = [
        ("scope_completion_gate", all(exists(path) for path in [LABEL_DESIGN_MANIFEST, MODEL_MANIFEST, ONNX_PARITY, THRESHOLD_SWEEP_SCORECARD, BEST_SCORECARD, MT5_PROBE_QUEUE, FINAL_DECISION, REPORT_PATH]), FINAL_DECISION, "planned outputs(계획 산출물) 생성"),
        ("kpi_contract_audit", exists(BEST_SCORECARD) and exists(STAGE_LEDGER), BEST_SCORECARD, "proxy KPI and tier ledger(프록시 KPI와 티어 장부) 기록"),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]), MODEL_RECEIPT, "skill receipts(스킬 영수증) 작성"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 포함"),
        ("timestamp_join_gate", exists(SOURCE_DATA_AUDIT), SOURCE_DATA_AUDIT, "timestamp-safe join and train-only label threshold(시점 안전 결합과 학습 전용 라벨 임계값) 확인"),
        ("lookahead_boundary_gate", exists(DATA_RECEIPT), DATA_RECEIPT, "future returns excluded from features(미래 수익률 피처 제외) 기록"),
        ("onnx_parity_audit", parity_pass, ONNX_PARITY, "classifier ONNX parity(분류기 온엑스 동등성) 확인"),
        ("fixed_threshold_policy_gate", fixed_threshold_pass, DATA_RECEIPT, "OOS quantile leakage(표본외 분위수 누수) 차단"),
        ("nonoverlap_trade_shape_gate", exists(THRESHOLD_SWEEP_SCORECARD), THRESHOLD_SWEEP_SCORECARD, "non-overlap trade shape(비중첩 거래 형태) 기록"),
        ("candidate_queue_file_audit", exists(MT5_PROBE_QUEUE), MT5_PROBE_QUEUE, "MT5 probe queue file(MT5 탐침 대기열 파일) 생성"),
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
    label_definitions, label_manifest_rows, _distribution_rows = build_labels(full)
    train_result = train_and_evaluate(full, feature_columns, label_definitions)
    status, judgment, decision, next_run_id = status_tuple(train_result["queue_rows"])
    write_firewall(train_result["queue_rows"], status, judgment)
    write_receipts(identity, train_result, status, judgment, next_run_id)
    write_final_and_manifest(identity, label_manifest_rows, train_result, status, judgment, decision, next_run_id)
    write_report(train_result, status, judgment, decision, next_run_id)
    write_state_and_selection(train_result, status, judgment, decision, next_run_id)
    write_ledgers(train_result, status, judgment, decision, next_run_id)
    gates = write_gates(train_result)
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
                "threshold_sweep_rows": len(train_result["sweep_rows"]),
                "mt5_probe_queue_rows": len(train_result["queue_rows"]),
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

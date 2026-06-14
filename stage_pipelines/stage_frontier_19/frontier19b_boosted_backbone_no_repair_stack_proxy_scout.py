from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.baseline_training import LABEL_ORDER, validate_model_input_frame
from foundation.models.catboost_ordered import (
    CatBoostVariantSpec,
    feature_importance_frame as cat_feature_importance_frame,
    fit_catboost_variant,
    probability_frame as cat_probability_frame,
)
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_catboost_classifier_to_onnx,
    export_xgboost_classifier_to_onnx,
    ordered_hash,
    sha256_file,
)
from foundation.models.xgboost_boosting import (
    XgbVariantSpec,
    feature_importance_frame as xgb_feature_importance_frame,
    fit_xgb_variant,
    probability_frame as xgb_probability_frame,
)
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_19__boosted_backbone_no_repair_stack_onnx_scout"
RUN_ID = "frontier19B_boosted_backbone_no_repair_stack_proxy_scout_v1"
RUN_NUMBER = "frontier19B"
PARENT_RUN_ID = "frontier19A_stage_open_boosted_backbone_no_repair_stack_onnx_scout_v1"
NEXT_GROK_RUN_ID = "frontier19C_grok_pre_expensive_boosted_backbone_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier19C_boosted_backbone_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
PROB_DIR = RUN_ROOT / "probabilities"
IMPORTANCE_DIR = RUN_ROOT / "feature_importance"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_19/frontier19b_boosted_backbone_no_repair_stack_proxy_scout.py")

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
F19A_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"
F19A_MODEL_LOCK = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "model_variant_lock.json"
F19A_EXECUTION_LOCK = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "execution_surface_lock.json"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")


def variant_specs() -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "f19b_xgb_depth2_l2_backbone_control",
            "family": "xgboost",
            "spec": XgbVariantSpec(
                variant_id="f19b_xgb_depth2_l2_backbone_control",
                idea_id="frontier19_backbone_only_xgb_depth2_l2",
                description="Frontier19 backbone-only XGBoost depth2 L2 control.",
                n_estimators=90,
                max_depth=2,
                learning_rate=0.045,
                reg_lambda=4.0,
                random_state=1901,
            ),
        },
        {
            "variant_id": "f19b_xgb_depth3_balanced_l2_backbone",
            "family": "xgboost",
            "spec": XgbVariantSpec(
                variant_id="f19b_xgb_depth3_balanced_l2_backbone",
                idea_id="frontier19_backbone_only_xgb_depth3_balanced_l2",
                description="Frontier19 backbone-only XGBoost depth3 balanced L2.",
                n_estimators=100,
                max_depth=3,
                learning_rate=0.040,
                min_child_weight=2.0,
                subsample=0.80,
                colsample_bytree=0.80,
                reg_lambda=6.0,
                random_state=1902,
                sample_weight_policy="balanced_classes",
            ),
        },
        {
            "variant_id": "f19b_cat_ordered_depth3_backbone",
            "family": "catboost",
            "spec": CatBoostVariantSpec(
                variant_id="f19b_cat_ordered_depth3_backbone",
                idea_id="frontier19_backbone_only_cat_ordered_depth3",
                description="Frontier19 backbone-only CatBoost ordered depth3.",
                iterations=90,
                depth=3,
                learning_rate=0.040,
                l2_leaf_reg=6.0,
                random_strength=0.50,
                bagging_temperature=1.0,
                random_seed=1812,
            ),
        },
        {
            "variant_id": "f19b_cat_plain_depth3_backbone_control",
            "family": "catboost",
            "spec": CatBoostVariantSpec(
                variant_id="f19b_cat_plain_depth3_backbone_control",
                idea_id="frontier19_backbone_only_cat_plain_depth3",
                description="Frontier19 backbone-only CatBoost plain depth3 control.",
                iterations=95,
                depth=3,
                learning_rate=0.040,
                l2_leaf_reg=7.0,
                random_strength=0.60,
                bootstrap_type="Bayesian",
                bagging_temperature=1.0,
                boosting_type="Plain",
                random_seed=1816,
            ),
        },
    ]


def main() -> int:
    now = utc_now()
    ensure_dirs()
    parent_summary = read_json(F19A_SUMMARY)
    execution_lock = read_json(F19A_EXECUTION_LOCK)
    frame = load_frame()
    feature_order = read_feature_order()
    specs = variant_specs()
    if len(specs) != 4:
        raise RuntimeError("Frontier19B variant cap must stay exactly four(전선19B 변형 상한은 정확히 4개여야 합니다).")

    model_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    stability_rows: list[dict[str, Any]] = []
    importance_outputs: list[dict[str, Any]] = []
    probability_outputs: list[dict[str, Any]] = []

    for item in specs:
        result = fit_export_evaluate_variant(frame, feature_order, item)
        model_rows.append(result["model_row"])
        metric_rows.extend(result["metric_rows"])
        stability_rows.extend(result["stability_rows"])
        importance_outputs.append(result["importance_output"])
        probability_outputs.append(result["probability_output"])

    metrics = pd.DataFrame(metric_rows)
    model_audit = pd.DataFrame(model_rows)
    stability = pd.DataFrame(stability_rows)
    summary = summarize_variants(metrics, model_audit, stability)
    final = build_final(now, parent_summary, execution_lock, feature_order, model_audit, metrics, stability, summary)
    write_outputs(final, model_audit, metrics, stability, summary, importance_outputs, probability_outputs)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "best_candidate_id": final["best_candidate_id"],
        "strict_count": final["strict_count"],
        "seed_count": final["seed_count"],
        "preserved_count": final["preserved_count"],
        "handoff_candidate_count": final["handoff_candidate_count"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_DIR, PROB_DIR, IMPORTANCE_DIR, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", ALPHA_LEDGER)


def load_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    required = {"timestamp", "split", "label_class", "future_log_return_12"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns(필수 열 누락): {missing}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if frame["timestamp"].isna().any():
        raise ValueError("Timestamp contains NaT(타임스탬프 결측).")
    if frame["timestamp"].duplicated().any():
        raise ValueError("Timestamp contains duplicates(타임스탬프 중복).")
    if set(frame["split"].astype(str).unique()) != {"train", "validation", "oos"}:
        raise ValueError("Split must be train/validation/oos(분할은 학습/검증/표본외만 허용).")
    return frame


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    feature_hash = ordered_hash(features)
    if feature_hash != EXPECTED_FEATURE_HASH:
        raise ValueError(f"Feature order hash mismatch(피처 순서 해시 불일치): {feature_hash}")
    return features


def fit_export_evaluate_variant(
    frame: pd.DataFrame,
    feature_order: list[str],
    item: dict[str, Any],
) -> dict[str, Any]:
    variant_id = str(item["variant_id"])
    family = str(item["family"])
    spec = item["spec"]
    validate_model_input_frame(frame, feature_order)
    if family == "xgboost":
        model, fit_info = fit_xgb_variant(frame, feature_order, spec)
        probabilities = xgb_probability_frame(model, frame, feature_order)
        importance = xgb_feature_importance_frame(model, feature_order)
        export_info = try_export_and_parity(
            family,
            model,
            MODEL_DIR / f"{variant_id}.onnx",
            frame,
            feature_order,
            export_xgboost_classifier_to_onnx,
        )
    elif family == "catboost":
        model, fit_info = fit_catboost_variant(frame, feature_order, spec)
        probabilities = cat_probability_frame(model, frame, feature_order)
        importance = cat_feature_importance_frame(model, feature_order)
        export_info = try_export_and_parity(
            family,
            model,
            MODEL_DIR / f"{variant_id}.onnx",
            frame,
            feature_order,
            export_catboost_classifier_to_onnx,
        )
    else:
        raise ValueError(f"Unknown family(알 수 없는 계열): {family}")

    probability_path = PROB_DIR / f"{variant_id}_probabilities.parquet"
    probabilities.to_parquet(io_path(probability_path), index=False)
    importance_path = IMPORTANCE_DIR / f"{variant_id}_feature_importance.csv"
    importance.to_csv(io_path(importance_path), index=False, lineterminator="\n")
    metric_rows = [evaluate_split(frame, probabilities, variant_id, family, split_name) for split_name in ("train", "validation", "oos")]
    stability_rows = stability_audit(frame, probabilities, variant_id, family)
    model_row = {
        "variant_id": variant_id,
        "family": family,
        "spec": asdict(spec),
        "fit_info": fit_info,
        "onnx_export_status": export_info["status"],
        "onnx_path": export_info.get("onnx_path", ""),
        "onnx_sha256": export_info.get("onnx_sha256", ""),
        "onnx_probability_output_name": export_info.get("probability_output_name", ""),
        "onnx_parity_passed": bool(export_info.get("parity", {}).get("passed", False)),
        "onnx_parity_max_abs_diff": export_info.get("parity", {}).get("max_abs_diff", None),
        "onnx_parity_rows": export_info.get("parity", {}).get("rows", 0),
        "export_error": export_info.get("error", ""),
        "probability_path": probability_path.as_posix(),
        "probability_sha256": sha256_file(probability_path),
        "feature_importance_path": importance_path.as_posix(),
        "feature_importance_sha256": sha256_file(importance_path),
    }
    return {
        "model_row": model_row,
        "metric_rows": metric_rows,
        "stability_rows": stability_rows,
        "importance_output": artifact_identity(importance_path),
        "probability_output": artifact_identity(probability_path),
    }


def try_export_and_parity(
    family: str,
    model: Any,
    output_path: Path,
    frame: pd.DataFrame,
    feature_order: list[str],
    export_fn: Any,
) -> dict[str, Any]:
    try:
        if family == "catboost":
            export = export_fn(model, output_path, feature_count=len(feature_order), target_opset=13, drop_label_output=True)
        else:
            export = export_fn(model, output_path, feature_count=len(feature_order), target_opset=13, drop_label_output=True)
        values = parity_values(frame, feature_order)
        parity = check_onnxruntime_probability_parity(model, output_path, values, tolerance=2e-5)
        return {
            "status": "exported_and_parity_checked(내보내기와 동등성 확인)",
            "onnx_path": output_path.as_posix(),
            "onnx_sha256": sha256_file(output_path),
            "probability_output_name": export.get("probability_output_name", ""),
            "export": export,
            "parity": parity,
        }
    except Exception as exc:  # noqa: BLE001 - record artifact failure as evidence.
        return {
            "status": "export_or_parity_failed(내보내기 또는 동등성 실패)",
            "onnx_path": output_path.as_posix(),
            "error": repr(exc),
            "parity": {"passed": False, "rows": 0},
        }


def parity_values(frame: pd.DataFrame, feature_order: list[str]) -> np.ndarray:
    sample = frame.loc[frame["split"].astype(str).isin(["validation", "oos"])].copy()
    if len(sample) > 1024:
        sample = sample.iloc[np.linspace(0, len(sample) - 1, 1024).round().astype(int)].copy()
    return sample.loc[:, feature_order].to_numpy(dtype="float64", copy=False)


def evaluate_split(
    frame: pd.DataFrame,
    probabilities: pd.DataFrame,
    variant_id: str,
    family: str,
    split_name: str,
) -> dict[str, Any]:
    mask = frame["split"].astype(str).eq(split_name).to_numpy(dtype=bool)
    split_frame = frame.loc[mask].copy()
    split_prob = probabilities.loc[mask].copy()
    decision = argmax_signal(split_prob)
    trade_mask = decision != 0
    returns = pd.to_numeric(split_frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    pnl = decision.astype("float64") * returns - trade_mask.astype("float64") * scout.ROUGH_COST_LOG_RETURN
    trade_pnl = pnl[trade_mask]
    trade_times = split_frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    days = scout.count_scope_days(split_frame["timestamp"])
    trade_count = int(len(trade_pnl))
    density = float(trade_count / days) if days else 0.0
    sparse_floor = max(30, int(math.ceil(days)))
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
    density_distance = scout.density_axis_distance(density)
    pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], trade_count, sparse_flag, pf999_sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    split_probs = split_prob.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    return {
        "variant_id": variant_id,
        "family": family,
        "split": split_name,
        "decision_policy": "argmax_nonflat_control(최대확률 비중립 대조)",
        "threshold_policy": "none_no_threshold_search(없음, 임계값 탐색 없음)",
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": density,
        "short_trade_count": int((decision == -1).sum()),
        "long_trade_count": int((decision == 1).sum()),
        "flat_count": int((decision == 0).sum()),
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "joint_axis_distance": density_distance + pf_distance + dd_distance + smoothness_distance,
        "density_pass": bool(scout.DENSITY_TARGET_LOW <= density <= scout.DENSITY_TARGET_HIGH),
        "pf_pass": bool(metrics["profit_factor"] >= scout.PF_TARGET and metrics["net_profit"] > 0 and not sparse_flag),
        "dd_pass": bool(dd_risk < scout.DD_TARGET_PERCENT),
        "smoothness_pass": bool(
            metrics["net_profit"] > 0
            and metrics["underwater_ratio"] <= 0.45
            and metrics["equity_trend_r2"] >= 0.35
            and metrics["max_loss_streak"] <= 6
        ),
        "mean_p_short": float(split_probs[:, 0].mean()) if len(split_probs) else 0.0,
        "mean_p_flat": float(split_probs[:, 1].mean()) if len(split_probs) else 0.0,
        "mean_p_long": float(split_probs[:, 2].mean()) if len(split_probs) else 0.0,
        "mean_probability_margin": float(split_prob["probability_margin"].mean()) if len(split_prob) else 0.0,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def argmax_signal(probabilities: pd.DataFrame) -> np.ndarray:
    values = probabilities.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    labels = np.asarray(LABEL_ORDER, dtype="int64")[values.argmax(axis=1)]
    decision = np.zeros(len(labels), dtype="int8")
    decision[labels == 0] = -1
    decision[labels == 2] = 1
    return decision


def stability_audit(
    frame: pd.DataFrame,
    probabilities: pd.DataFrame,
    variant_id: str,
    family: str,
) -> list[dict[str, Any]]:
    decision = argmax_signal(probabilities)
    returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    trade_mask = decision != 0
    pnl = decision.astype("float64") * returns - trade_mask.astype("float64") * scout.ROUGH_COST_LOG_RETURN
    payload = frame.loc[:, ["timestamp", "split"]].copy()
    payload["period"] = payload["timestamp"].dt.to_period("M").astype(str)
    payload["decision"] = decision
    payload["pnl"] = pnl
    rows: list[dict[str, Any]] = []
    for (split_name, period), group in payload.groupby(["split", "period"], sort=True):
        group_trade = group.loc[group["decision"].ne(0)]
        metrics = scout.trade_metrics(group_trade["pnl"].to_numpy(dtype="float64"), group_trade["timestamp"])
        days = scout.count_scope_days(group["timestamp"])
        rows.append({
            "variant_id": variant_id,
            "family": family,
            "split": str(split_name),
            "period": str(period),
            "trade_count": int(len(group_trade)),
            "days_in_scope": days,
            "trades_per_day": float(len(group_trade) / days) if days else 0.0,
            "net_profit": metrics["net_profit"],
            "profit_factor": metrics["profit_factor"],
            "max_drawdown_percent": metrics["max_drawdown_percent"],
            "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
            "audit_role": "stability_audit_tie_break_only(안정성 감사, 동률 처리 전용)",
        })
    return rows


def summarize_variants(metrics: pd.DataFrame, model_audit: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for variant_id, group in metrics.groupby("variant_id", sort=False):
        model_row = model_audit.loc[model_audit["variant_id"].eq(variant_id)].iloc[0].to_dict()
        payload: dict[str, Any] = {
            "candidate_id": f"{variant_id}__argmax_nonflat_backbone_only",
            "variant_id": variant_id,
            "family": str(group["family"].iloc[0]),
            "onnx_parity_passed": bool(model_row.get("onnx_parity_passed", False)),
            "onnx_path": model_row.get("onnx_path", ""),
            "onnx_sha256": model_row.get("onnx_sha256", ""),
            "export_error": model_row.get("export_error", ""),
        }
        for split_name in ("train", "validation", "oos"):
            split = group.loc[group["split"].eq(split_name)].iloc[0].to_dict()
            for key in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "max_drawdown_percent",
                "max_monthly_drawdown_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "density_axis_distance",
                "pf_axis_distance",
                "dd_axis_distance",
                "smoothness_axis_distance",
                "joint_axis_distance",
                "density_pass",
                "pf_pass",
                "dd_pass",
                "smoothness_pass",
                "short_trade_count",
                "long_trade_count",
                "flat_count",
                "mean_probability_margin",
            ):
                payload[f"{split_name}_{key}"] = split.get(key)
        train_stability = stability.loc[stability["variant_id"].eq(variant_id) & stability["split"].eq("train")]
        positive_fraction = float((train_stability["net_profit"] > 0).mean()) if len(train_stability) else 0.0
        worst_dd = float(train_stability["max_drawdown_percent"].max()) if len(train_stability) else 0.0
        payload["train_stability_positive_period_fraction"] = positive_fraction
        payload["train_stability_worst_period_dd"] = worst_dd
        payload["stability_tie_break_score"] = positive_fraction - min(worst_dd / 100.0, 1.0)
        payload["proxy_joint_distance"] = float(payload["validation_joint_axis_distance"]) + float(payload["oos_joint_axis_distance"])
        payload["strict_scout_clue"] = bool(
            payload["onnx_parity_passed"]
            and payload["validation_net_profit"] > 0
            and payload["oos_net_profit"] > 0
            and payload["validation_profit_factor"] >= 1.50
            and payload["oos_profit_factor"] >= 1.50
            and 5.0 <= payload["validation_trades_per_day"] <= 10.0
            and 5.0 <= payload["oos_trades_per_day"] <= 10.0
            and max(payload["validation_max_drawdown_percent"], payload["oos_max_drawdown_percent"]) <= 15.0
        )
        payload["seed_surface"] = bool(
            payload["onnx_parity_passed"]
            and payload["validation_net_profit"] > 0
            and payload["oos_net_profit"] > 0
            and payload["validation_profit_factor"] >= 1.10
            and payload["oos_profit_factor"] >= 1.10
            and 3.0 <= payload["validation_trades_per_day"] <= 15.0
            and 3.0 <= payload["oos_trades_per_day"] <= 15.0
            and max(payload["validation_max_drawdown_percent"], payload["oos_max_drawdown_percent"]) <= 25.0
        )
        payload["preserved_clue"] = bool(
            payload["onnx_parity_passed"]
            and not payload["seed_surface"]
            and min(payload["validation_max_drawdown_percent"], payload["oos_max_drawdown_percent"]) <= 10.0
            and max(payload["validation_profit_factor"], payload["oos_profit_factor"]) >= 1.0
        )
        payload["handoff_candidate"] = bool(payload["strict_scout_clue"] or payload["seed_surface"])
        rows.append(payload)
    summary = pd.DataFrame(rows)
    return summary.sort_values(
        [
            "strict_scout_clue",
            "seed_surface",
            "preserved_clue",
            "proxy_joint_distance",
            "stability_tie_break_score",
            "oos_profit_factor",
        ],
        ascending=[False, False, False, True, False, False],
    ).reset_index(drop=True)


def build_final(
    now: str,
    parent_summary: dict[str, Any],
    execution_lock: dict[str, Any],
    feature_order: list[str],
    model_audit: pd.DataFrame,
    metrics: pd.DataFrame,
    stability: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    best = summary.iloc[0].to_dict()
    strict_count = int(summary["strict_scout_clue"].sum())
    seed_count = int(summary["seed_surface"].sum())
    preserved_count = int(summary["preserved_clue"].sum())
    handoff_count = int(summary["handoff_candidate"].sum())
    parity_pass_count = int(model_audit["onnx_parity_passed"].sum())
    if strict_count:
        status = "boosted_backbone_strict_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run = NEXT_GROK_RUN_ID
    elif seed_count:
        status = "boosted_backbone_seed_surface_no_authority"
        judgment = "seed_surface(씨앗 표면)"
        next_run = NEXT_GROK_RUN_ID
    elif preserved_count:
        status = "boosted_backbone_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    elif parity_pass_count == 0:
        status = "boosted_backbone_invalid_no_onnx_parity_no_authority"
        judgment = "invalid_setup(무효 설정)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "boosted_backbone_no_forward_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_CLOSEOUT_RUN_ID
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run,
        "status": status,
        "judgment": judgment,
        "best_candidate_id": best["candidate_id"],
        "best_variant_id": best["variant_id"],
        "best_family": best["family"],
        "best_summary": json_ready(best),
        "strict_count": strict_count,
        "seed_count": seed_count,
        "preserved_count": preserved_count,
        "handoff_candidate_count": handoff_count,
        "onnx_parity_pass_count": parity_pass_count,
        "model_count": int(len(model_audit)),
        "metric_rows": int(len(metrics)),
        "stability_rows": int(len(stability)),
        "data_integrity": {
            "dataset": artifact_identity(DATASET_PATH),
            "feature_order": artifact_identity(FEATURE_ORDER_PATH),
            "feature_count": len(feature_order),
            "feature_order_hash": ordered_hash(feature_order),
            "split_counts": {str(k): int(v) for k, v in load_frame()["split"].value_counts().to_dict().items()},
            "tier_b_status": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
            "tier_ab_status": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
        },
        "parent_stage_open": {
            "path": F19A_SUMMARY.as_posix(),
            "status": parent_summary.get("status", ""),
            "judgment": parent_summary.get("judgment", ""),
        },
        "execution_lock": execution_lock,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "runtime_probe_boundary": (
            "handoff_candidate_requires_grok_before_mt5(인계 후보는 MT5 전 Grok 필요)"
            if handoff_count
            else "no_runtime_handoff_candidate_from_frontier19b_proxy(전선19B 프록시에서 런타임 인계 후보 없음)"
        ),
    }


def write_outputs(
    final: dict[str, Any],
    model_audit: pd.DataFrame,
    metrics: pd.DataFrame,
    stability: pd.DataFrame,
    summary: pd.DataFrame,
    importance_outputs: list[dict[str, Any]],
    probability_outputs: list[dict[str, Any]],
) -> None:
    model_audit_path = RUN_ROOT / "model_export_parity_audit.csv"
    metrics_path = RUN_ROOT / "proxy_split_metrics.csv"
    stability_path = RUN_ROOT / "subperiod_stability_audit.csv"
    summary_path = RUN_ROOT / "candidate_summary.csv"
    top_path = RUN_ROOT / "top_candidates.csv"
    final_path = RUN_ROOT / "final_summary.json"
    manifest_path = RUN_ROOT / "run_manifest.json"
    model_audit.to_csv(io_path(model_audit_path), index=False, lineterminator="\n")
    metrics.to_csv(io_path(metrics_path), index=False, lineterminator="\n")
    stability.to_csv(io_path(stability_path), index=False, lineterminator="\n")
    summary.to_csv(io_path(summary_path), index=False, lineterminator="\n")
    summary.head(12).to_csv(io_path(top_path), index=False, lineterminator="\n")
    write_json(final_path, final)
    write_json(manifest_path, run_manifest(final, model_audit_path, metrics_path, stability_path, summary_path, top_path, final_path, importance_outputs, probability_outputs))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(
    final: dict[str, Any],
    model_audit_path: Path,
    metrics_path: Path,
    stability_path: Path,
    summary_path: Path,
    top_path: Path,
    final_path: Path,
    importance_outputs: list[dict[str, Any]],
    probability_outputs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "script": artifact_identity(SCRIPT_PATH),
        "inputs": {
            "stage_open_summary": artifact_identity(F19A_SUMMARY),
            "model_variant_lock": artifact_identity(F19A_MODEL_LOCK),
            "execution_surface_lock": artifact_identity(F19A_EXECUTION_LOCK),
            "dataset": artifact_identity(DATASET_PATH),
            "feature_order": artifact_identity(FEATURE_ORDER_PATH),
        },
        "outputs": {
            "model_export_parity_audit": artifact_identity(model_audit_path),
            "proxy_split_metrics": artifact_identity(metrics_path),
            "subperiod_stability_audit": artifact_identity(stability_path),
            "candidate_summary": artifact_identity(summary_path),
            "top_candidates": artifact_identity(top_path),
            "final_summary": artifact_identity(final_path),
            "report": artifact_identity(REPORT_PATH),
            "probabilities": probability_outputs,
            "feature_importance": importance_outputs,
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
        "runtime_probe_boundary": final["runtime_probe_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    top_rows = summary.head(6).to_dict("records")
    best = final["best_summary"]
    return f"""# Frontier19B Boosted Backbone No Repair Stack Proxy Scout Report(전선19B 부스팅 백본 수리 중첩 없는 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): 4 pre-registered boosted backbone variants(사전 등록 부스팅 백본 변형 4개)를 train-only(학습 전용)으로 학습하고 ONNX export/parity(ONNX 내보내기/동등성)와 argmax_nonflat proxy(최대확률 비중립 프록시)를 평가했습니다.

Effect(효과): threshold/veto/firewall/lifecycle/quota/stability-selector repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리)를 추가하지 않고, 백본(backbone, 백본) 자체가 네 축(PF/빈도/손실폭/매끄러움)에 주는 영향을 분리합니다.

Best candidate(최상 후보): `{final['best_candidate_id']}`

- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best['validation_profit_factor'])}` / `{fmt(best['validation_trades_per_day'])}/day` / `{fmt(best['validation_max_drawdown_percent'])}%`
- OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭): `{fmt(best['oos_profit_factor'])}` / `{fmt(best['oos_trades_per_day'])}/day` / `{fmt(best['oos_max_drawdown_percent'])}%`
- ONNX parity(ONNX 동등성): `{best['onnx_parity_passed']}`
- strict/seed/preserved(엄격/씨앗/보존): `{final['strict_count']}` / `{final['seed_count']}` / `{final['preserved_count']}`
- handoff candidates(인계 후보): `{final['handoff_candidate_count']}`

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_boundary']}`

Top rows(상위 행):

```json
{json.dumps(json_ready(top_rows), ensure_ascii=False, indent=2)}
```

Tier records(티어 기록):

- Tier A separate(티어 A 분리): materialized(물질화)
- Tier B separate(티어 B 분리): `missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)`
- Tier A+B combined(티어 A+B 합산): `out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(final: dict[str, Any]) -> str:
    return f"""# Frontier19 Review Index(전선19 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{PARENT_RUN_ID}`: stage open(단계 개방), Grok adjusted accepted(그록 수정 수용), backbone-only locks(백본 단독 잠금).
- `{RUN_ID}`: proxy scout(프록시 탐색), model training(모델 학습), ONNX export/parity(ONNX 내보내기/동등성), Tier records(티어 기록), status(상태) `{final['status']}`.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier19B Required Gate Coverage Audit(전선19B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): 4/4 pre-registered variants(사전 등록 변형 4개) evaluated(평가).
- kpi_contract_audit(KPI 계약 감사): PF/density/DD/smoothness(PF/빈도/손실폭/매끄러움) by split(분할별) recorded(기록).
- onnx_parity_gate(ONNX 동등성 게이트): `{final['onnx_parity_pass_count']}`/`{final['model_count']}` variants(변형) passed(통과).
- do_not_repeat_lock_gate(반복 금지 잠금 게이트): no threshold/veto/firewall/lifecycle/quota/stability selector repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리 없음).
- tier_record_gate(티어 기록 게이트): Tier A materialized(티어 A 물질화), Tier B missing_required(티어 B 필수 누락), Tier A+B out_of_scope_by_claim(합산 주장 범위 밖).
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): `{final['runtime_probe_boundary']}`.
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier19 Selection Status(전선19 선택 상태)

Updated(갱신): {final['created_at_utc']}

Latest run(최근 실행): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Strict/seed/preserved counts(엄격/씨앗/보존 수): `{final['strict_count']}` / `{final['seed_count']}` / `{final['preserved_count']}`

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_boundary']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    if final["strict_count"] == 0 and final["seed_count"] == 0:
        f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_memory_candidate_entry(final))


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(f03b.WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_summary"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "boosted_backbone_proxy_scout(부스팅 백본 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_count']};seed={final['seed_count']};preserved={final['preserved_count']};handoff={final['handoff_candidate_count']};parity={final['onnx_parity_pass_count']}/{final['model_count']};no_authority",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "trained_models": str(final["model_count"]),
        "onnx_parity": f"{final['onnx_parity_pass_count']}/{final['model_count']}",
        "best_proxy": final["best_candidate_id"],
        "candidate_rows": str(final["model_count"]),
        "positive_proxy_rows": str(final["seed_count"] + final["strict_count"]),
        "best_model_id": final["best_variant_id"],
        "best_profit_factor": fmt(best.get("oos_profit_factor")),
        "trade_density": fmt(best.get("oos_trades_per_day")),
        "max_drawdown_percent": fmt(best.get("oos_max_drawdown_percent")),
        "claim_boundary": "proxy_and_onnx_parity_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_summary"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "boosted_backbone_proxy_scout(부스팅 백본 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_boosted_backbone_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_boosted_backbone_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "proxy_onnx_parity_not_runtime(프록시 ONNX 동등성, 런타임 아님)",
            "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_max_drawdown_percent'))}",
            "guardrail_kpi": "no_threshold_veto_firewall_lifecycle_quota_stability_selector_repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리 없음)",
            "external_verification_status": final["runtime_probe_boundary"],
            "notes": f"strict={final['strict_count']};seed={final['seed_count']};preserved={final['preserved_count']};parity={final['onnx_parity_pass_count']}/{final['model_count']}",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)",
            "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)",
            "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
            "notes": "Tier B model input not available in this dataset(Tier B 모델 입력이 이 데이터셋에 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)",
            "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)",
            "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
            "notes": "Combined record blocked by missing Tier B source(Tier B 원천 누락으로 합산 기록 차단)",
        },
    ]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` completed Frontier19B boosted backbone proxy scout(전선19B 부스팅 백본 프록시 탐색). "
        f"Effect(효과): status(상태) `{final['status']}`, next run(다음 실행) `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: boosted backbone no-repair-stack proxy scout(부스팅 백본 수리 중첩 없는 프록시 탐색) evaluated `{final['model_count']}` models. "
        f"Effect(효과): best candidate(최상 후보) `{final['best_candidate_id']}` and runtime boundary(런타임 경계) `{final['runtime_probe_boundary']}` recorded.\n"
    )


def negative_memory_candidate_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: no strict/seed surface(엄격/씨앗 표면 없음) under boosted backbone-only locks(부스팅 백본 단독 잠금). "
        "Effect(효과): repair/closeout decision(수리/마감 결정)로 넘겨 같은 repair stack(수리 중첩)을 반복하지 않습니다.\n"
    )


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_summary"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier19B(전선19B)가 4개 boosted backbone variants(부스팅 백본 변형 4개)를 proxy/ONNX parity(프록시/ONNX 동등성)로 평가했습니다.

Effect(효과): threshold/veto/firewall/lifecycle/quota/stability-selector repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리) 없이 best candidate(최상 후보) `{final['best_candidate_id']}`를 기록했습니다.

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_max_drawdown_percent'))}%`

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_boundary']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    with io_path(template_path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "0"
    return f"{number:.6g}" if math.isfinite(number) else "0"


if __name__ == "__main__":
    raise SystemExit(main())

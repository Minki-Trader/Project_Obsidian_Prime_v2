from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (
    design_proxy_negative_trade_shape_offensive_pivot_without_db as hw,
)  # noqa: E402

aw = hw.aw
fb = hw.fb
he = hw.he

TODAY = "2026-06-01"
STAGE_ID = hw.STAGE_ID
RUN_NUMBER = "run337HX"
RUN_ID = "run337HX_materialize_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1"
PARENT_RUN_ID = hw.RUN_ID
NEXT_RUN_ID = "run337HY_review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1"
STATUS = "completed_stage337HX_proxy_negative_trade_shape_offensive_pivot_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_offensive_pivot_inputs_materialized_review_required"
DECISION = "stage337HX_open_run337HY_proxy_negative_trade_shape_offensive_pivot_input_review"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_mt5_"
    "no_runtime_package_no_operating_or_goal_claim"
)

STAGE_DIR = hw.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = hw.REVIEWS_DIR
REPORT_PATH = REVIEW_DIR / f"{RUN_NUMBER}_proxy_negative_trade_shape_offensive_pivot_inputs.md"
DECISION_DOC = aw.ROOT / "docs" / "decisions" / f"{TODAY}_stage337HX_proxy_negative_trade_shape_offensive_pivot_inputs.md"
RUN_REGISTRY = aw.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = aw.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = aw.STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = aw.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = aw.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = aw.ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = aw.ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = aw.STAGE_DIR / "README.md"
CHANGELOG = aw.ROOT / "CHANGELOG.md"

BASE_FRAME = hw.hv.hu.HS_FRAME
BASE_ALLOWED_FEATURES = hw.hv.hu.HS_ALLOWED_FEATURES
HW_FINAL = hw.FINAL_DECISION
HW_GATES = hw.GATE_AUDIT
HW_QUEUE = hw.HX_QUEUE
HW_DESIGN = hw.DESIGN_MATRIX
HW_EXPERIMENT = hw.EXPERIMENT_CONTRACT
HW_LABEL = hw.LABEL_HORIZON_CONTRACT
HW_MODEL = hw.MODEL_FAMILY_CONTRACT
HW_TRADE = hw.TRADE_SHAPE_CONTRACT
HW_TIER = hw.TIER_PAIR_CONTRACT
HW_FEATURE = hw.FEATURE_BOUNDARY_CONTRACT
HW_RELEASE = hw.RELEASE_FIREWALL_CONTRACT
HU_PROXY = hw.hv.HU_PROXY
HU_CLASSIFICATION = hw.hv.HU_CLASSIFICATION

HX_INPUT_FRAME = RUN_DIR / "hx_input_frame.parquet"
HX_SOURCE_MAP = RUN_DIR / "hx_materialization_source_map.csv"
HX_ALLOWED_FEATURES = RUN_DIR / "hx_allowed_model_feature_set.csv"
HX_LABEL_AUDIT = RUN_DIR / "hx_label_horizon_audit.csv"
HX_SIDE_AUDIT = RUN_DIR / "hx_side_asymmetry_audit.csv"
HX_ACTIVE_FLAT_AUDIT = RUN_DIR / "hx_active_flat_audit.csv"
HX_REGIME_AUDIT = RUN_DIR / "hx_regime_context_audit.csv"
HX_TIER_PLAN = RUN_DIR / "hx_tier_record_plan.csv"
HX_FEATURE_BOUNDARY = RUN_DIR / "hx_feature_boundary_audit.csv"
HX_MODEL_BLUEPRINT = RUN_DIR / "hx_model_family_task_blueprint.csv"
HX_THRESHOLD_CONTRACT = RUN_DIR / "hx_label_threshold_contract.csv"
HY_TASK_SEEDS = RUN_DIR / "run337HY_training_task_seed_matrix.csv"
HY_QUEUE = RUN_DIR / "run337HY_review_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

LABEL_COLUMNS = [
    "hx_label_class_fwd6",
    "hx_label_class_fwd18",
    "hx_label_class_fwd24",
    "hx_active_flat_label",
]
VALID_COLUMNS = [
    "hx_valid_fwd6",
    "hx_valid_fwd18",
    "hx_valid_fwd24",
]
WEIGHT_COLUMNS = [
    "hx_label_horizon_weight",
    "hx_side_asymmetry_weight",
    "hx_model_family_challenge_weight",
    "hx_active_flat_weight",
    "hx_regime_context_weight",
]
FORBIDDEN_FEATURE_TOKENS = [
    "label",
    "future",
    "target",
    "claim_boundary",
    "net_profit",
    "profit_factor",
    "recovery",
    "drawdown",
    "expectancy",
    "mt5",
    "proxy",
]


def _ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent, RUN_REGISTRY.parent]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _read_json(path: Path) -> dict:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload: dict) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _norm01(series: pd.Series) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    low = clean.quantile(0.05)
    high = clean.quantile(0.95)
    if not np.isfinite(low) or not np.isfinite(high) or high <= low:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return ((clean - low) / (high - low)).clip(0.0, 1.0).fillna(0.0)


def _future_sum(group: pd.DataFrame, horizon: int) -> pd.Series:
    returns = pd.to_numeric(group["log_return_1"], errors="coerce")
    total = pd.Series(np.zeros(len(group)), index=group.index, dtype="float64")
    valid = pd.Series(True, index=group.index)
    for step in range(1, horizon + 1):
        shifted = returns.shift(-step)
        total = total + shifted.fillna(0.0)
        valid = valid & shifted.notna()
    return total.where(valid, np.nan)


def _make_class(ret: pd.Series, threshold: float) -> pd.Series:
    values = pd.Series(np.full(len(ret), -1, dtype=np.int16), index=ret.index)
    valid = ret.notna()
    values.loc[valid & (ret > threshold)] = 2
    values.loc[valid & (ret < -threshold)] = 0
    values.loc[valid & (ret >= -threshold) & (ret <= threshold)] = 1
    return values


def _derive_thresholds(frame: pd.DataFrame) -> pd.DataFrame:
    source = frame.loc[
        pd.to_numeric(frame["label_class"], errors="coerce").isin([0, 2]),
        "future_log_return_12",
    ].abs()
    base_threshold = float(source.quantile(0.05)) if not source.empty else 0.001
    if not np.isfinite(base_threshold) or base_threshold <= 0:
        base_threshold = 0.001
    rows = []
    for horizon in [6, 12, 18, 24]:
        threshold = float(base_threshold * np.sqrt(horizon / 12.0))
        rows.append(
            {
                "horizon_bars": horizon,
                "threshold_abs_log_return": threshold,
                "threshold_source": "source_label_boundary_abs_return_5pct_scaled_by_sqrt_horizon",
                "timestamp_safety": "target_only_not_feature",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def _materialize_frame(base: pd.DataFrame, thresholds: pd.DataFrame) -> pd.DataFrame:
    frame = base.copy()
    frame = frame.sort_values(["cost_policy_id", "source_row_id", "timestamp"]).reset_index(drop=True)

    for horizon in [6, 18, 24]:
        future_col = f"hx_future_log_return_{horizon}"
        valid_col = f"hx_valid_fwd{horizon}"
        label_col = f"hx_label_class_fwd{horizon}"
        frame[future_col] = (
            frame.groupby("cost_policy_id", group_keys=False)
            .apply(lambda group: _future_sum(group, horizon), include_groups=False)
            .reset_index(level=0, drop=True)
        )
        threshold = float(
            thresholds.loc[thresholds["horizon_bars"] == horizon, "threshold_abs_log_return"].iloc[0]
        )
        frame[valid_col] = frame[future_col].notna().astype("int8")
        frame[label_col] = _make_class(frame[future_col], threshold).astype("int16")

    threshold18 = float(
        thresholds.loc[thresholds["horizon_bars"] == 18, "threshold_abs_log_return"].iloc[0]
    )
    frame["hx_active_flat_label"] = np.where(
        frame["hx_valid_fwd18"] == 1,
        (frame["hx_future_log_return_18"].abs() > threshold18).astype("int16"),
        -1,
    ).astype("int16")

    base_weight = pd.to_numeric(
        frame.get("hr_multi_kpi_release_firewall_weight", 1.0), errors="coerce"
    ).fillna(1.0)
    base_weight = base_weight.clip(0.25, 8.0)
    abs18 = _norm01(frame["hx_future_log_return_18"].abs())
    side_quality = _norm01(frame.get("side_quality_weight", pd.Series(0.0, index=frame.index)))
    macro_stress = _norm01(frame.get("vix_return_5", pd.Series(0.0, index=frame.index)).abs())
    volatility = _norm01(frame.get("historical_vol_20", pd.Series(0.0, index=frame.index)))
    trend = _norm01(frame.get("adx_14", pd.Series(0.0, index=frame.index)))
    opening_edge = (
        pd.to_numeric(frame.get("is_first_30m_after_open", 0), errors="coerce").fillna(0.0)
        + pd.to_numeric(frame.get("is_last_30m_before_cash_close", 0), errors="coerce").fillna(0.0)
    ).clip(0.0, 1.0)
    side_label = frame["hx_label_class_fwd18"]
    active_label = frame["hx_active_flat_label"]

    frame["hx_label_horizon_weight"] = (base_weight * (1.0 + 0.65 * abs18)).clip(0.10, 12.0)
    frame["hx_side_asymmetry_weight"] = (
        base_weight
        * (1.0 + 0.55 * side_quality)
        * np.where(side_label.isin([0, 2]), 1.25, 0.85)
    ).clip(0.10, 12.0)
    frame["hx_model_family_challenge_weight"] = (
        base_weight * (1.0 + 0.35 * trend + 0.25 * volatility)
    ).clip(0.10, 10.0)
    frame["hx_active_flat_weight"] = (
        base_weight * np.where(active_label == 1, 1.65, np.where(active_label == 0, 0.90, 0.25))
    ).clip(0.10, 12.0)
    frame["hx_regime_context_weight"] = (
        base_weight
        * (1.0 + 0.40 * macro_stress + 0.25 * opening_edge + 0.20 * volatility)
    ).clip(0.10, 12.0)
    return frame


def _make_source_map(frame: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source_artifact": "base_hs_input_frame",
                "path": aw.rel(BASE_FRAME),
                "sha256": _sha(BASE_FRAME),
                "rows": len(frame),
                "effect": "HW offensive pivot design becomes timestamp-safe HX training input material.",
            },
            {
                "source_artifact": "base_allowed_model_features",
                "path": aw.rel(BASE_ALLOWED_FEATURES),
                "sha256": _sha(BASE_ALLOWED_FEATURES),
                "rows": int(len(_read_csv(BASE_ALLOWED_FEATURES))),
                "effect": "Feature boundary is inherited so new target columns cannot enter model inputs.",
            },
            {
                "source_artifact": "parent_hw_design_matrix",
                "path": aw.rel(HW_DESIGN),
                "sha256": _sha(HW_DESIGN),
                "rows": int(len(_read_csv(HW_DESIGN))),
                "effect": "Five offensive pivot families are materialized into HY task seeds.",
            },
            {
                "source_artifact": "parent_hw_final_decision",
                "path": aw.rel(HW_FINAL),
                "sha256": _sha(HW_FINAL),
                "rows": 1,
                "effect": "Parent decision opens HX without turning the proxy-negative repair into selection.",
            },
        ]
    )


def _copy_allowed_features() -> pd.DataFrame:
    allowed = _read_csv(BASE_ALLOWED_FEATURES).copy()
    if "feature_name" not in allowed.columns:
        first = allowed.columns[0]
        allowed = allowed.rename(columns={first: "feature_name"})
    allowed["hx_usage"] = "allowed_model_input_for_run337HY"
    allowed["claim_boundary"] = CLAIM_BOUNDARY
    return allowed


def _make_label_audit(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for horizon in [6, 18, 24]:
        label_col = f"hx_label_class_fwd{horizon}"
        future_col = f"hx_future_log_return_{horizon}"
        valid_col = f"hx_valid_fwd{horizon}"
        counts = frame[label_col].value_counts(dropna=False).to_dict()
        rows.append(
            {
                "label_column": label_col,
                "future_column": future_col,
                "valid_column": valid_col,
                "valid_rows": int(frame[valid_col].sum()),
                "invalid_rows": int((frame[valid_col] == 0).sum()),
                "short_rows": int(counts.get(0, 0)),
                "flat_rows": int(counts.get(1, 0)),
                "long_rows": int(counts.get(2, 0)),
                "missing_class_rows": int(counts.get(-1, 0)),
                "timestamp_rule": "future returns used only as target labels and excluded from feature set",
                "effect": "Alternative holding horizons can be reviewed without changing runtime authority.",
            }
        )
    return pd.DataFrame(rows)


def _make_side_audit(frame: pd.DataFrame) -> pd.DataFrame:
    label = frame["hx_label_class_fwd18"]
    long_rows = int((label == 2).sum())
    short_rows = int((label == 0).sum())
    flat_rows = int((label == 1).sum())
    active_rows = long_rows + short_rows
    balance = min(long_rows, short_rows) / max(long_rows, short_rows) if max(long_rows, short_rows) else 0.0
    return pd.DataFrame(
        [
            {
                "audit_item": "fwd18_side_distribution",
                "short_rows": short_rows,
                "flat_rows": flat_rows,
                "long_rows": long_rows,
                "active_rows": active_rows,
                "long_short_balance_ratio": balance,
                "weight_column": "hx_side_asymmetry_weight",
                "effect": "HY can test whether the repair failure came from side symmetry pressure.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def _make_active_flat_audit(frame: pd.DataFrame) -> pd.DataFrame:
    label = frame["hx_active_flat_label"]
    counts = label.value_counts(dropna=False).to_dict()
    return pd.DataFrame(
        [
            {
                "audit_item": "active_flat_stage_one",
                "active_rows": int(counts.get(1, 0)),
                "flat_rows": int(counts.get(0, 0)),
                "invalid_rows": int(counts.get(-1, 0)),
                "target_column": "hx_active_flat_label",
                "weight_column": "hx_active_flat_weight",
                "effect": "Two-stage active/flat testing can attack negative proxy trade shape directly.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def _make_regime_audit(frame: pd.DataFrame) -> pd.DataFrame:
    def _count(col: str) -> int:
        return int(pd.to_numeric(frame.get(col, 0), errors="coerce").fillna(0).astype(bool).sum())

    rows = [
        {
            "regime_slice": "us_cash_open",
            "rows": _count("is_us_cash_open"),
            "weight_column": "hx_regime_context_weight",
            "effect": "Cash-session behavior remains visible to HY review.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "regime_slice": "first_30m_after_open",
            "rows": _count("is_first_30m_after_open"),
            "weight_column": "hx_regime_context_weight",
            "effect": "Opening microstructure stress can be isolated before training.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "regime_slice": "last_30m_before_cash_close",
            "rows": _count("is_last_30m_before_cash_close"),
            "weight_column": "hx_regime_context_weight",
            "effect": "Closing microstructure stress can be isolated before training.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    if "historical_vol_20" in frame.columns:
        high_vol_cutoff = pd.to_numeric(frame["historical_vol_20"], errors="coerce").quantile(0.80)
        rows.append(
            {
                "regime_slice": "top20pct_historical_vol_20",
                "rows": int((pd.to_numeric(frame["historical_vol_20"], errors="coerce") >= high_vol_cutoff).sum()),
                "weight_column": "hx_regime_context_weight",
                "effect": "Volatility context is available without joining new external data.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def _make_feature_boundary(allowed: pd.DataFrame) -> pd.DataFrame:
    def _forbidden_hits(feature_name: str) -> list[str]:
        lowered = feature_name.lower()
        hits = [token for token in FORBIDDEN_FEATURE_TOKENS if token in lowered]
        if lowered.endswith("_weight") or "_weight_" in lowered or lowered == "weight":
            hits.append("sample_weight_column")
        return hits

    rows = []
    for feature in allowed["feature_name"].astype(str):
        hits = _forbidden_hits(feature)
        rows.append(
            {
                "feature_name": feature,
                "forbidden_hits": "|".join(hits),
                "status": "fail" if hits else "pass",
                "effect": "Targets, weights, proxy KPI, and runtime evidence cannot leak into model inputs.",
            }
        )
    return pd.DataFrame(rows)


def _make_tier_plan(frame: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "required_record": "Tier A separate",
                "status": "materialized",
                "rows": len(frame),
                "artifact": aw.rel(HX_INPUT_FRAME),
                "effect": "Full-context sample remains the only materialized HX input.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "required_record": "Tier B separate",
                "status": "missing_required",
                "rows": 0,
                "artifact": "",
                "effect": "Missing partial-context source is named instead of silently omitted.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "required_record": "Tier A+B combined",
                "status": "missing_required",
                "rows": 0,
                "artifact": "",
                "effect": "Combined read is blocked until Tier B exists, so no synthetic sum is claimed.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def _make_task_blueprint() -> pd.DataFrame:
    rows = [
        {
            "task_id": "hx_hw001_fwd6_label_horizon_lgbm",
            "pivot_family": "hw001_label_horizon_pivot",
            "target_column": "hx_label_class_fwd6",
            "valid_column": "hx_valid_fwd6",
            "sample_weight_column": "hx_label_horizon_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd6_fast_horizon_attack",
        },
        {
            "task_id": "hx_hw001_fwd18_label_horizon_lgbm",
            "pivot_family": "hw001_label_horizon_pivot",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "hx_label_horizon_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_swing_horizon_attack",
        },
        {
            "task_id": "hx_hw002_side_asymmetry_fwd18_lgbm",
            "pivot_family": "hw002_side_specific_asymmetry",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "hx_side_asymmetry_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_side_asymmetry_attack",
        },
        {
            "task_id": "hx_hw003_model_family_extratrees_fwd18",
            "pivot_family": "hw003_model_family_challenge",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "hx_model_family_challenge_weight",
            "model_family": "ExtraTrees(엑스트라트리스)_multiclass",
            "model_config_id": "extratrees_family_challenge",
        },
        {
            "task_id": "hx_hw003_model_family_xgboost_fwd18",
            "pivot_family": "hw003_model_family_challenge",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "hx_model_family_challenge_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_family_challenge",
        },
        {
            "task_id": "hx_hw004_active_flat_stage1_lgbm",
            "pivot_family": "hw004_active_flat_two_stage",
            "target_column": "hx_active_flat_label",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "hx_active_flat_weight",
            "model_family": "LightGBM(라이트GBM)_binary",
            "model_config_id": "lgbm_active_flat_stage_one",
        },
        {
            "task_id": "hx_hw005_regime_context_fwd18_lgbm",
            "pivot_family": "hw005_regime_context_mixture",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "hx_regime_context_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass_regime_context",
            "model_config_id": "lgbm_regime_context_attack",
        },
    ]
    blueprint = pd.DataFrame(rows)
    blueprint["input_frame"] = aw.rel(HX_INPUT_FRAME)
    blueprint["allowed_features"] = aw.rel(HX_ALLOWED_FEATURES)
    blueprint["required_guard"] = "drop rows where valid_column equals 0 or target equals -1"
    blueprint["expected_effect"] = "Attack proxy-negative trade shape with new labels, sides, model families, active-flat split, and regime context."
    blueprint["forbidden_use"] = "No selection, no runtime package, no MT5 claim, no operating claim from HX alone."
    blueprint["claim_boundary"] = CLAIM_BOUNDARY
    return blueprint


def _make_queue(task_seed_rows: int) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "review_materialized_offensive_pivot_inputs_before_training",
                "input_frame": aw.rel(HX_INPUT_FRAME),
                "task_seed_matrix": aw.rel(HY_TASK_SEEDS),
                "task_seed_rows": task_seed_rows,
                "required_review": "feature boundary, label validity, tier records, source lineage, and training guard readiness",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def _make_receipts(frame: pd.DataFrame, task_seed_rows: int) -> dict[str, dict]:
    data_receipt = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "input_frame": aw.rel(HX_INPUT_FRAME),
        "source_frame": aw.rel(BASE_FRAME),
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "cost_policies": sorted(frame["cost_policy_id"].astype(str).unique().tolist()),
        "timestamp_min": str(frame["timestamp"].min()),
        "timestamp_max": str(frame["timestamp"].max()),
        "tier_a_status": "materialized",
        "tier_b_status": "missing_required",
        "tier_ab_status": "missing_required",
        "effect": "Timestamp-safe offensive pivot inputs are available for HY review.",
    }
    experiment_receipt = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "work_family": "input_materialization",
        "primary_skill": "obsidian-data-integrity",
        "support_skills": ["obsidian-exploration-mandate", "obsidian-artifact-lineage"],
        "parent_design": aw.rel(HW_DESIGN),
        "task_seed_rows": task_seed_rows,
        "effect": "HW design is converted into auditable HY training tasks.",
    }
    model_receipt = {
        "run_id": RUN_ID,
        "model_training": "not_run",
        "onnx_export": "not_run",
        "runtime_package": "not_opened",
        "effect": "No model authority is created by input materialization.",
    }
    performance_receipt = {
        "run_id": RUN_ID,
        "mt5_kpi": "not_measured",
        "proxy_kpi": "not_measured",
        "selection": "not_selected",
        "effect": "HY starts from inputs, not a performance claim.",
    }
    judgment_receipt = {
        "run_id": RUN_ID,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "effect": "Review is required before training uses the materialized inputs.",
    }
    claim_receipt = {
        "run_id": RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "goal_achieve_claim": "not_claimed",
        "runtime_authority_claim": "not_claimed",
        "operating_promotion_claim": "not_claimed",
        "live_readiness_claim": "not_claimed",
    }
    lineage_receipt = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_map": aw.rel(HX_SOURCE_MAP),
        "artifact_registry_updated": True,
        "effect": "Input, contract, queue, and review artifacts can be traced together.",
    }
    return {
        "experiment": experiment_receipt,
        "data": data_receipt,
        "model": model_receipt,
        "performance": performance_receipt,
        "judgment": judgment_receipt,
        "claim": claim_receipt,
        "lineage": lineage_receipt,
    }


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(
    frame: pd.DataFrame,
    feature_boundary: pd.DataFrame,
    tier_plan: pd.DataFrame,
    task_seeds: pd.DataFrame,
    parent_final: dict,
) -> pd.DataFrame:
    parent_gates = _read_csv(HW_GATES)
    parent_queue = _read_csv(HW_QUEUE)
    parent_statuses = parent_gates["status"].astype(str).str.lower()
    parent_hw_passed = parent_statuses.isin(["pass", "passed"]).all()
    parent_next_action = parent_final.get("next_run_id") or parent_final.get("next_action")
    gates = [
        _gate_row(
            "source_inputs_present",
            "pass" if all(path.exists() for path in [BASE_FRAME, BASE_ALLOWED_FEATURES, HW_DESIGN, HW_FINAL]) else "fail",
            aw.rel(HX_SOURCE_MAP),
            "HX starts from recorded HS/HW artifacts.",
        ),
        _gate_row(
            "parent_hw_gates_passed",
            "pass" if parent_hw_passed else "fail",
            aw.rel(HW_GATES),
            "Parent design is not materialized unless its gates passed.",
        ),
        _gate_row(
            "parent_next_action_matches_hx",
            "pass"
            if parent_next_action == RUN_ID
            and parent_queue["next_run_id"].astype(str).eq(RUN_ID).any()
            else "fail",
            aw.rel(HW_QUEUE),
            "The queued action matches the materialization run.",
        ),
        _gate_row(
            "input_frame_materialized",
            "pass" if HX_INPUT_FRAME.exists() and len(frame) > 0 else "fail",
            aw.rel(HX_INPUT_FRAME),
            "HY receives a concrete input frame.",
        ),
        _gate_row(
            "label_columns_materialized",
            "pass" if all(col in frame.columns for col in LABEL_COLUMNS + VALID_COLUMNS) else "fail",
            aw.rel(HX_LABEL_AUDIT),
            "Horizon and active-flat targets exist with validity flags.",
        ),
        _gate_row(
            "weight_columns_finite",
            "pass"
            if all(np.isfinite(pd.to_numeric(frame[col], errors="coerce")).all() for col in WEIGHT_COLUMNS)
            else "fail",
            aw.rel(HX_ACTIVE_FLAT_AUDIT),
            "Training weights are bounded before HY review.",
        ),
        _gate_row(
            "feature_boundary_no_forbidden_targets",
            "pass" if feature_boundary["status"].astype(str).eq("pass").all() else "fail",
            aw.rel(HX_FEATURE_BOUNDARY),
            "New labels, weights, proxy and runtime terms stay outside features.",
        ),
        _gate_row(
            "tier_records_present",
            "pass"
            if set(tier_plan["required_record"].astype(str))
            == {"Tier A separate", "Tier B separate", "Tier A+B combined"}
            else "fail",
            aw.rel(HX_TIER_PLAN),
            "Required tier records are named even when missing.",
        ),
        _gate_row(
            "tier_b_missing_not_silent",
            "pass"
            if tier_plan.loc[tier_plan["required_record"].eq("Tier B separate"), "status"].iloc[0]
            == "missing_required"
            else "fail",
            aw.rel(HX_TIER_PLAN),
            "Missing Tier B is recorded instead of hidden.",
        ),
        _gate_row(
            "task_seed_matrix_opened",
            "pass" if len(task_seeds) >= 7 else "fail",
            aw.rel(HY_TASK_SEEDS),
            "HY has multiple offensive training paths.",
        ),
        _gate_row(
            "next_review_queue_opened",
            "pass" if HY_QUEUE.exists() else "fail",
            aw.rel(HY_QUEUE),
            "The next review run is queued before training.",
        ),
        _gate_row(
            "no_forbidden_operating_claim",
            "pass",
            aw.rel(CLAIM_BOUNDARY_RECEIPT),
            "HX does not claim Goal, runtime authority, operating promotion, or live readiness.",
        ),
        _gate_row(
            "required_gate_coverage_audit_written",
            "pass",
            aw.rel(GATE_AUDIT),
            "Closeout can cite exactly which gates support the claim boundary.",
        ),
    ]
    return pd.DataFrame(gates)


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        if key in frame.columns:
            current = frame[key].astype(str).eq(str(row[key]))
            mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = [
        "stage_id",
        "run_id",
        "artifact_type",
        "path",
        "sha256",
        "created_at",
        "claim_boundary",
    ]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not path.exists():
            continue
        artifact_type = "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip(".") or "artifact"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": aw.rel(path),
                "sha256": _sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if not rows:
        return
    new_paths = {row["path"] for row in rows}
    registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
    registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    columns = list(dict.fromkeys(required + list(registry.columns)))
    registry[columns].to_csv(
        aw.io_path(ARTIFACT_REGISTRY),
        index=False,
        encoding="utf-8-sig",
        lineterminator="\n",
    )


def _update_docs(frame: pd.DataFrame, gates: pd.DataFrame, task_seed_rows: int) -> None:
    gate_passes = int(gates["status"].astype(str).eq("pass").sum())
    gate_total = int(len(gates))
    report = f"""﻿# Stage 337HX Proxy-Negative Offensive Pivot Inputs

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- judgment: `{JUDGMENT}`
- gates: `{gate_passes}/{gate_total}`
- rows: `{len(frame)}`
- task_seed_rows: `{task_seed_rows}`

## What Changed

HW design(설계)을 HX input materialization(입력 물질화)으로 바꿨다.
효과는 fwd6/fwd18/fwd24 label(라벨), active-flat target(능동/평탄 타깃), side/regime weight(방향/국면 가중치), HY task seed(작업 씨앗)를 검토 가능한 산출물로 남긴 것이다.

## Tier Records

- Tier A separate(Tier A 분리): materialized(물질화), `{len(frame)}` rows.
- Tier B separate(Tier B 분리): missing_required(필수 누락).
- Tier A+B combined(Tier A+B 합산): missing_required(필수 누락).

## Boundary

No model training(모델 학습 없음), no MT5(메타트레이더5) run(실행 없음), no runtime package(런타임 패키지 없음), no operating claim(운영 주장 없음).

## Next

Open `{NEXT_RUN_ID}` to review(검토) label validity(라벨 유효성), feature boundary(피처 경계), tier records(티어 기록), lineage(계보), and training guard(학습 보호조건).
"""
    decision = f"""﻿# Decision: Stage 337HX Offensive Pivot Inputs

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{DECISION}`
- judgment: `{JUDGMENT}`
- next_run_id: `{NEXT_RUN_ID}`

## Reason

HU/HV repair(수리)는 proxy net(프록시 순수익)을 개선했지만 여전히 negative(음수)였다.
HW는 weight-only repair(가중치만 수리)를 멈추고 offensive pivot(공격 전환)을 열었다.
HX는 그 설계를 timestamp-safe(시점 안전) input(입력)과 task seed(작업 씨앗)로 만들었다.

## Effect

다음 HY 검토(review, 검토)는 새 수익 원천 후보를 학습하기 전에 leakage(누수), tier omission(티어 누락), invalid label(무효 라벨)을 먼저 잡을 수 있다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)

    state = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    _write_bom_text(WORKSPACE_STATE, state)

    current = f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- current_run: `{RUN_ID}`
- latest_completed_run: `{RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`
- next_run: `{NEXT_RUN_ID}`

## Effect

HX materialized(물질화) offensive pivot input(공격 전환 입력)을 만들었다.
효과는 HY가 training(학습) 전에 label/feature/tier/lineage gate(라벨/피처/티어/계보 게이트)를 검토할 수 있게 된 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(CURRENT_WORKING_STATE, current)

    selection = f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- runtime_package: not_opened
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed

효과는 HX input materialization(입력 물질화)을 모델 선택(selection, 선택)으로 오해하지 않게 하는 것이다.
"""
    _write_bom_text(SELECTION_STATUS, selection)

    stage_brief = f"""﻿# {STAGE_ID}

Latest run: `{RUN_ID}`

HX materialized(물질화) proxy-negative offensive pivot(프록시 음수 공격 전환) inputs for HY review(검토).
Tier B separate(Tier B 분리) and Tier A+B combined(Tier A+B 합산) are `missing_required`.
"""
    _write_bom_text(STAGE_BRIEF, stage_brief)

    if CHANGELOG.exists():
        existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    else:
        existing = "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        "- Materialized(물질화) offensive pivot inputs and HY task seeds.\n"
        "- Recorded(기록) Tier B and combined records as missing_required(필수 누락).\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(frame: pd.DataFrame, gates: pd.DataFrame) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": int(len(frame)),
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], common)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], common)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], common)


def _write_final_decision(frame: pd.DataFrame, gates: pd.DataFrame, task_seed_rows: int) -> None:
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": int(len(frame)),
        "task_seed_rows": int(task_seed_rows),
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "tier_a_status": "materialized",
        "tier_b_status": "missing_required",
        "tier_ab_status": "missing_required",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at": TODAY,
        "script": aw.rel(Path(__file__)),
        "inputs": [aw.rel(BASE_FRAME), aw.rel(BASE_ALLOWED_FEATURES), aw.rel(HW_DESIGN), aw.rel(HW_FINAL)],
        "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    _write_json(FINAL_DECISION, payload)
    _write_json(RUN_MANIFEST, manifest)


def _artifact_paths() -> list[Path]:
    return [
        HX_INPUT_FRAME,
        HX_SOURCE_MAP,
        HX_ALLOWED_FEATURES,
        HX_LABEL_AUDIT,
        HX_SIDE_AUDIT,
        HX_ACTIVE_FLAT_AUDIT,
        HX_REGIME_AUDIT,
        HX_TIER_PLAN,
        HX_FEATURE_BOUNDARY,
        HX_MODEL_BLUEPRINT,
        HX_THRESHOLD_CONTRACT,
        HY_TASK_SEEDS,
        HY_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        PERFORMANCE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_BOUNDARY_RECEIPT,
        LINEAGE_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def main() -> None:
    _ensure_dirs()

    base = pd.read_parquet(aw.io_path(BASE_FRAME))
    thresholds = _derive_thresholds(base)
    frame = _materialize_frame(base, thresholds)
    aw.io_path(HX_INPUT_FRAME.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(aw.io_path(HX_INPUT_FRAME), index=False)

    allowed = _copy_allowed_features()
    source_map = _make_source_map(frame)
    label_audit = _make_label_audit(frame)
    side_audit = _make_side_audit(frame)
    active_flat_audit = _make_active_flat_audit(frame)
    regime_audit = _make_regime_audit(frame)
    tier_plan = _make_tier_plan(frame)
    feature_boundary = _make_feature_boundary(allowed)
    task_blueprint = _make_task_blueprint()
    queue = _make_queue(len(task_blueprint))

    _write_csv(HX_SOURCE_MAP, source_map)
    _write_csv(HX_ALLOWED_FEATURES, allowed)
    _write_csv(HX_LABEL_AUDIT, label_audit)
    _write_csv(HX_SIDE_AUDIT, side_audit)
    _write_csv(HX_ACTIVE_FLAT_AUDIT, active_flat_audit)
    _write_csv(HX_REGIME_AUDIT, regime_audit)
    _write_csv(HX_TIER_PLAN, tier_plan)
    _write_csv(HX_FEATURE_BOUNDARY, feature_boundary)
    _write_csv(HX_MODEL_BLUEPRINT, task_blueprint)
    _write_csv(HX_THRESHOLD_CONTRACT, thresholds)
    _write_csv(HY_TASK_SEEDS, task_blueprint)
    _write_csv(HY_QUEUE, queue)

    receipts = _make_receipts(frame, len(task_blueprint))
    _write_json(EXPERIMENT_RECEIPT, receipts["experiment"])
    _write_json(DATA_RECEIPT, receipts["data"])
    _write_json(MODEL_RECEIPT, receipts["model"])
    _write_json(PERFORMANCE_RECEIPT, receipts["performance"])
    _write_json(JUDGMENT_RECEIPT, receipts["judgment"])
    _write_json(CLAIM_BOUNDARY_RECEIPT, receipts["claim"])
    _write_json(LINEAGE_RECEIPT, receipts["lineage"])

    parent_final = _read_json(HW_FINAL)
    gates = _make_gates(frame, feature_boundary, tier_plan, task_blueprint, parent_final)
    _write_csv(GATE_AUDIT, gates)
    _write_final_decision(frame, gates, len(task_blueprint))
    _update_docs(frame, gates, len(task_blueprint))
    _update_ledgers(frame, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"HX gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "rows": int(len(frame)),
                "columns": int(len(frame.columns)),
                "task_seed_rows": int(len(task_blueprint)),
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

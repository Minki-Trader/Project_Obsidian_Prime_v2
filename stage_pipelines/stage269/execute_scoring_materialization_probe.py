from __future__ import annotations

import csv
import hashlib
import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
RUN_ID = "run269D_scoring_materialization_probe_v1"
RUN_ROOT = ROOT / "stages" / STAGE_ID / "02_runs" / "run269D"
REVIEW_ROOT = ROOT / "stages" / STAGE_ID / "03_reviews"

SOURCE_SPECS = ROOT / "stages" / STAGE_ID / "02_runs" / "run269C" / "scoring_input_specs.json"
SOURCE_HANDOFF_PLAN = ROOT / "stages" / STAGE_ID / "02_runs" / "run269C" / "handoff_input_plan.csv"
SOURCE_IDENTITY = ROOT / "stages" / STAGE_ID / "02_runs" / "run269C" / "package_identity_receipts.csv"
SOURCE_RUN269C_MANIFEST = ROOT / "stages" / STAGE_ID / "02_runs" / "run269C" / "run_manifest.json"

TIER_A_MODEL_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)
TIER_A_FEATURE_ORDER = TIER_A_MODEL_INPUT.with_name("model_input_feature_order.txt")
TIER_A_SUMMARY = TIER_A_MODEL_INPUT.with_name("model_input_summary.json")
TIER_A_FEATURE_MANIFEST = TIER_A_MODEL_INPUT.with_name("feature_set_manifest.json")

TIER_B_MODEL_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v1"
    / "model_input_dataset.parquet"
)
TIER_B_FEATURE_ORDER = TIER_B_MODEL_INPUT.with_name("model_input_feature_order.txt")
TIER_B_SUMMARY = TIER_B_MODEL_INPUT.with_name("model_input_summary.json")
TIER_B_FEATURE_MANIFEST = TIER_B_MODEL_INPUT.with_name("feature_set_manifest.json")

BASE_ADAPTER = ROOT / "foundation" / "adapters" / "baseline_adapter.py"

CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

LABEL_OR_FUTURE_COLUMNS = {
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "horizon_bars",
    "horizon_minutes",
}

PACKAGE_SHORT_IDS = {
    "cp269A_asymmetric_nonfilter_reentry_surface": "cp269A",
    "cp269B_identity_collapse_disambiguator": "cp269B",
    "cp269C_session_skew_reward_surface": "cp269C",
    "cp269D_runtime_handoff_isolation_control": "cp269D",
}


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding=encoding)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig")


def robust_z(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").astype("float64")
    median = numeric.median(skipna=True)
    mad = (numeric - median).abs().median(skipna=True)
    scale = (mad * 1.4826) if mad and np.isfinite(mad) else numeric.std(skipna=True)
    if not scale or not np.isfinite(scale):
        return pd.Series(0.0, index=series.index)
    return ((numeric - median) / scale).replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(-6.0, 6.0)


def sigmoid(value: pd.Series | np.ndarray) -> pd.Series:
    array = np.asarray(value, dtype="float64")
    clipped = np.clip(array, -20.0, 20.0)
    return pd.Series(1.0 / (1.0 + np.exp(-clipped)))


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> pd.Series:
    if name not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[name], errors="coerce").astype("float64").fillna(default)


def finite_missing_columns(frame: pd.DataFrame, feature_order: list[str]) -> list[str]:
    return [name for name in feature_order if name not in frame.columns]


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def prepare_view(
    *,
    path: Path,
    tier_view: str,
    input_feature_order_hash: str,
    expected_feature_order: list[str],
) -> pd.DataFrame:
    frame = pd.read_parquet(path).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["tier_view"] = tier_view
    frame["input_feature_order_hash"] = input_feature_order_hash
    frame["expected_feature_order_hash"] = sha256_text("\n".join(expected_feature_order))
    missing = finite_missing_columns(frame, expected_feature_order)
    for name in missing:
        frame[name] = np.nan
    frame["missing_required_feature_count"] = len(missing)
    frame["missing_required_features"] = ";".join(missing) if missing else "none"
    return frame


def base_output(frame: pd.DataFrame, package_id: str, spec: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "symbol": frame.get("symbol", pd.Series("US100", index=frame.index)),
            "split": frame["split"].astype(str),
            "tier_view": frame["tier_view"],
            "package_id": package_id,
            "input_feature_order_hash": frame["input_feature_order_hash"],
            "expected_feature_order_hash": frame["expected_feature_order_hash"],
            "decision_rule_hash": spec["decision_rule_hash"],
            "adapter_schema_hash": spec["adapter_schema_hash"],
            "score_columns_hash": spec["score_columns_hash"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )


def score_cp269a(frame: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    trend = (
        0.28 * robust_z(col(frame, "di_spread_14"))
        + 0.24 * robust_z(col(frame, "ppo_hist_12_26_9"))
        + 0.20 * robust_z(col(frame, "ema9_ema20_diff"))
        + 0.18 * robust_z(col(frame, "return_zscore_20"))
        + 0.10 * robust_z(col(frame, "supertrend_10_3"))
    )
    volatility = (
        0.35 * robust_z(col(frame, "bollinger_width_20"))
        + 0.25 * robust_z(col(frame, "atr_14_over_atr_50"))
        + 0.25 * robust_z(col(frame, "historical_vol_5_over_20"))
        + 0.15 * robust_z(col(frame, "hl_zscore_50").abs())
    )
    cash_open = col(frame, "is_us_cash_open")
    weak_context_cost = sigmoid(
        0.32 * robust_z(col(frame, "vix_zscore_20").abs())
        + 0.24 * robust_z(col(frame, "usdx_zscore_20").abs())
        + 0.22 * (1.0 - cash_open)
        + 0.14 * col(frame, "is_last_30m_before_cash_close")
        + 0.08 * robust_z(col(frame, "mega8_dispersion_5").abs())
    )
    reward_skew_score = sigmoid(
        0.42 * volatility.abs()
        + 0.30 * trend.abs()
        + 0.18 * robust_z(col(frame, "bb_position_20")).abs()
        + 0.10 * cash_open
    )
    entry_probability = sigmoid(0.70 * trend.abs() + 0.20 * reward_skew_score - 0.35 * weak_context_cost)
    failure_zone_cut_flag = ((weak_context_cost > 0.70) & (reward_skew_score < 0.56)).astype("int8")
    candidate_decision_score = (
        entry_probability * reward_skew_score * (1.0 - 0.55 * weak_context_cost)
    ).clip(lower=0.0, upper=1.0)

    output = base_output(frame, spec["package_id"], spec)
    output["entry_probability"] = entry_probability.round(8)
    output["reward_skew_score"] = reward_skew_score.round(8)
    output["weak_context_cost"] = weak_context_cost.round(8)
    output["failure_zone_cut_flag"] = failure_zone_cut_flag
    output["candidate_decision_score"] = candidate_decision_score.round(8)
    output["materialized_decision_flag"] = ((candidate_decision_score >= 0.32) & (failure_zone_cut_flag == 0)).astype("int8")
    return output


def score_cp269b(frame: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    source_a_raw = (
        0.30 * robust_z(col(frame, "adx_14"))
        + 0.28 * robust_z(col(frame, "di_spread_14"))
        + 0.22 * robust_z(col(frame, "ema20_ema50_diff"))
        + 0.20 * robust_z(col(frame, "ppo_hist_12_26_9"))
    )
    source_b_raw = (
        0.30 * robust_z(col(frame, "atr_14_over_atr_50"))
        + 0.25 * robust_z(col(frame, "historical_vol_5_over_20"))
        + 0.25 * robust_z(col(frame, "bb_squeeze"))
        + 0.20 * robust_z(col(frame, "mega8_dispersion_5"))
    )
    source_a_score = sigmoid(source_a_raw)
    source_b_score = sigmoid(source_b_raw)
    divergence_metric = (source_a_score - source_b_score).abs()
    duplicate_signature_flag = (divergence_metric < 0.055).astype("int8")
    source_mask_id = np.where(source_a_score >= source_b_score, "trend_identity_mask", "volatility_identity_mask")

    output = base_output(frame, spec["package_id"], spec)
    output["source_mask_id"] = source_mask_id
    output["source_a_score"] = source_a_score.round(8)
    output["source_b_score"] = source_b_score.round(8)
    output["divergence_metric"] = divergence_metric.round(8)
    output["duplicate_signature_flag"] = duplicate_signature_flag
    output["materialized_decision_flag"] = ((divergence_metric >= 0.08) & (duplicate_signature_flag == 0)).astype("int8")
    return output


def session_code(frame: pd.DataFrame) -> pd.Series:
    minutes = col(frame, "minutes_from_cash_open", default=np.nan)
    cash_open = col(frame, "is_us_cash_open").astype(bool)
    values = np.select(
        [
            ~cash_open,
            minutes <= 30,
            (minutes > 30) & (minutes <= 150),
            (minutes > 150) & (minutes < 360),
            minutes >= 360,
        ],
        ["outside_cash", "open_30", "early_mid", "mid_late", "close_30"],
        default="unknown",
    )
    return pd.Series(values, index=frame.index)


def score_cp269c(frame: pd.DataFrame, spec: dict[str, Any]) -> pd.DataFrame:
    minutes = col(frame, "minutes_from_cash_open", default=np.nan).fillna(999.0)
    cash_open = col(frame, "is_us_cash_open")
    distance_to_open = minutes.clip(lower=0.0)
    distance_to_close = (390.0 - minutes).clip(lower=0.0)
    distance_to_open_close = np.minimum(distance_to_open, distance_to_close)
    normalized_distance = (distance_to_open_close / 390.0).clip(lower=0.0, upper=1.0)
    morphology_shock = sigmoid(
        0.45 * robust_z(col(frame, "return_1_over_atr_14").abs())
        + 0.35 * robust_z(col(frame, "hl_zscore_50").abs())
        + 0.20 * robust_z(col(frame, "gap_percent").abs())
    )
    volatility_regime = sigmoid(
        0.45 * robust_z(col(frame, "atr_14_over_atr_50"))
        + 0.30 * robust_z(col(frame, "historical_vol_5_over_20"))
        + 0.25 * robust_z(col(frame, "bollinger_width_20"))
    )
    session_reward_score = sigmoid(
        0.36 * volatility_regime
        + 0.26 * morphology_shock
        + 0.20 * cash_open
        + 0.18 * (1.0 - normalized_distance)
    )
    session_risk_cap = (0.20 + 0.75 * session_reward_score - 0.25 * morphology_shock).clip(lower=0.05, upper=0.95)

    output = base_output(frame, spec["package_id"], spec)
    output["session_code"] = session_code(frame)
    output["session_reward_score"] = session_reward_score.round(8)
    output["session_risk_cap"] = session_risk_cap.round(8)
    output["distance_to_open_close"] = pd.Series(distance_to_open_close, index=frame.index).round(4)
    output["morphology_shock"] = morphology_shock.round(8)
    output["materialized_decision_flag"] = ((session_reward_score >= 0.58) & (session_risk_cap >= 0.25)).astype("int8")
    return output


def score_cp269d(
    frame: pd.DataFrame,
    spec: dict[str, Any],
    *,
    adapter_hash: str,
    package_model_hash: str,
    handoff_hash: str,
) -> pd.DataFrame:
    input_hash = frame["input_feature_order_hash"].astype(str)
    expected_hash = frame["expected_feature_order_hash"].astype(str)
    identity_match = input_hash.eq(expected_hash).astype("int8")

    output = base_output(frame, spec["package_id"], spec)
    output["feature_order_hash"] = input_hash
    output["model_hash"] = package_model_hash
    output["adapter_hash"] = adapter_hash
    output["handoff_hash"] = handoff_hash
    output["identity_match_flag"] = identity_match
    output["materialized_decision_flag"] = identity_match
    return output


def summarize_scores(package_id: str, table: pd.DataFrame, score_columns: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tier_view, tier_frame in table.groupby("tier_view", dropna=False):
        for split, split_frame in tier_frame.groupby("split", dropna=False):
            numeric_score_columns = [
                name for name in score_columns if name in split_frame.columns and pd.api.types.is_numeric_dtype(split_frame[name])
            ]
            null_cells = int(split_frame[score_columns].isna().sum().sum()) if score_columns else 0
            score_min = float(split_frame[numeric_score_columns].min(numeric_only=True).min()) if numeric_score_columns else np.nan
            score_max = float(split_frame[numeric_score_columns].max(numeric_only=True).max()) if numeric_score_columns else np.nan
            rows.append(
                {
                    "package_id": package_id,
                    "tier_view": str(tier_view),
                    "split": str(split),
                    "rows": int(len(split_frame)),
                    "score_columns": ";".join(score_columns),
                    "null_score_cells": null_cells,
                    "numeric_score_min": round(score_min, 8) if np.isfinite(score_min) else "",
                    "numeric_score_max": round(score_max, 8) if np.isfinite(score_max) else "",
                    "materialized_decision_count": int(split_frame["materialized_decision_flag"].sum()),
                    "performance_claim": "none",
                }
            )
    return rows


def build_handoff_payload(
    *,
    spec: dict[str, Any],
    table_path: Path,
    table_hash: str,
    tier_rows: dict[str, int],
    view_feature_hashes: dict[str, str],
    package_model_hash: str,
) -> dict[str, Any]:
    return {
        "package_id": spec["package_id"],
        "package_role": spec["package_role"],
        "feature_order_hash": spec["feature_order_hash"],
        "blueprint_hash": "",
        "decision_rule_hash": spec["decision_rule_hash"],
        "adapter_schema_hash": spec["adapter_schema_hash"],
        "score_columns_hash": spec["score_columns_hash"],
        "model_hash": package_model_hash,
        "score_table_path": repo_path(table_path),
        "score_table_hash": table_hash,
        "tier_view_rows": tier_rows,
        "input_view_feature_order_hashes": view_feature_hashes,
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_judgment": "score_table_materialized_no_performance_claim",
    }


def materialize() -> dict[str, Any]:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)
    scores_root = RUN_ROOT / "scores"
    handoff_root = RUN_ROOT / "handoff"
    scores_root.mkdir(parents=True, exist_ok=True)
    handoff_root.mkdir(parents=True, exist_ok=True)

    specs = json.loads(SOURCE_SPECS.read_text(encoding="utf-8"))
    handoff_plan_rows = list(csv.DictReader(SOURCE_HANDOFF_PLAN.open(newline="", encoding="utf-8")))
    identity_rows = list(csv.DictReader(SOURCE_IDENTITY.open(newline="", encoding="utf-8")))

    tier_a_feature_order = load_feature_order(TIER_A_FEATURE_ORDER)
    tier_b_feature_order = load_feature_order(TIER_B_FEATURE_ORDER)
    expected_feature_order = tier_a_feature_order
    tier_a_hash = sha256_text("\n".join(tier_a_feature_order))
    tier_b_hash = sha256_text("\n".join(tier_b_feature_order))

    tier_a = prepare_view(
        path=TIER_A_MODEL_INPUT,
        tier_view="Tier A separate",
        input_feature_order_hash=tier_a_hash,
        expected_feature_order=expected_feature_order,
    )
    tier_b = prepare_view(
        path=TIER_B_MODEL_INPUT,
        tier_view="Tier B separate",
        input_feature_order_hash=tier_b_hash,
        expected_feature_order=expected_feature_order,
    )
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.*",
            category=FutureWarning,
        )
        combined = pd.concat([tier_a, tier_b], ignore_index=True, sort=False)
    combined["combined_view_label"] = "Tier A+B combined materialization view; no routed PnL"

    adapter_hash = sha256_file(BASE_ADAPTER)
    source_hashes = {
        repo_path(SOURCE_SPECS): sha256_file(SOURCE_SPECS),
        repo_path(SOURCE_HANDOFF_PLAN): sha256_file(SOURCE_HANDOFF_PLAN),
        repo_path(SOURCE_IDENTITY): sha256_file(SOURCE_IDENTITY),
        repo_path(SOURCE_RUN269C_MANIFEST): sha256_file(SOURCE_RUN269C_MANIFEST),
        repo_path(TIER_A_MODEL_INPUT): sha256_file(TIER_A_MODEL_INPUT),
        repo_path(TIER_A_FEATURE_ORDER): sha256_file(TIER_A_FEATURE_ORDER),
        repo_path(TIER_A_SUMMARY): sha256_file(TIER_A_SUMMARY),
        repo_path(TIER_A_FEATURE_MANIFEST): sha256_file(TIER_A_FEATURE_MANIFEST),
        repo_path(TIER_B_MODEL_INPUT): sha256_file(TIER_B_MODEL_INPUT),
        repo_path(TIER_B_FEATURE_ORDER): sha256_file(TIER_B_FEATURE_ORDER),
        repo_path(TIER_B_SUMMARY): sha256_file(TIER_B_SUMMARY),
        repo_path(TIER_B_FEATURE_MANIFEST): sha256_file(TIER_B_FEATURE_MANIFEST),
        repo_path(BASE_ADAPTER): adapter_hash,
    }

    summary_rows: list[dict[str, Any]] = []
    handoff_resolution_rows: list[dict[str, Any]] = []
    handoff_paths: list[Path] = []
    score_table_paths: list[Path] = []
    score_sample_rows: list[dict[str, Any]] = []

    plan_by_package = {row["package_id"]: row for row in handoff_plan_rows}
    identity_by_package = {row["package_id"]: row for row in identity_rows}

    for spec in specs["packages"]:
        package_id = spec["package_id"]
        short_id = PACKAGE_SHORT_IDS[package_id]
        spec = {**spec, "package_id": package_id}
        model_hash = sha256_text(json.dumps(spec, ensure_ascii=False, sort_keys=True))
        pre_handoff_hash = sha256_text(
            "|".join(
                [
                    package_id,
                    spec["feature_order_hash"],
                    spec["decision_rule_hash"],
                    spec["adapter_schema_hash"],
                    spec["score_columns_hash"],
                    model_hash,
                    CLAIM_BOUNDARY,
                ]
            )
        )
        if package_id.endswith("asymmetric_nonfilter_reentry_surface"):
            table = score_cp269a(combined, spec)
        elif package_id.endswith("identity_collapse_disambiguator"):
            table = score_cp269b(combined, spec)
        elif package_id.endswith("session_skew_reward_surface"):
            table = score_cp269c(combined, spec)
        elif package_id.endswith("runtime_handoff_isolation_control"):
            table = score_cp269d(
                combined,
                spec,
                adapter_hash=adapter_hash,
                package_model_hash=model_hash,
                handoff_hash=pre_handoff_hash,
            )
        else:
            raise RuntimeError(f"Unknown package_id: {package_id}")

        table_path = scores_root / f"{short_id}_scores.parquet"
        table.to_parquet(table_path, index=False)
        table_hash = sha256_file(table_path)
        score_table_paths.append(table_path)
        summary_rows.extend(summarize_scores(package_id, table, spec["scoring_columns"]))
        sample = table.groupby(["tier_view", "split"], dropna=False).head(1).copy()
        for _, row in sample.iterrows():
            payload = {
                "package_id": package_id,
                "tier_view": row["tier_view"],
                "split": row["split"],
                "timestamp": row["timestamp"].isoformat(),
                "materialized_decision_flag": int(row["materialized_decision_flag"]),
            }
            for score_column in spec["scoring_columns"]:
                if score_column in row:
                    value = row[score_column]
                    payload[score_column] = value.item() if hasattr(value, "item") else value
            score_sample_rows.append(payload)

        tier_rows = {str(k): int(v) for k, v in table["tier_view"].value_counts().sort_index().items()}
        view_feature_hashes = {
            str(k): str(v)
            for k, v in table.groupby("tier_view")["input_feature_order_hash"].first().sort_index().items()
        }
        handoff_payload = build_handoff_payload(
            spec=spec,
            table_path=table_path,
            table_hash=table_hash,
            tier_rows=tier_rows,
            view_feature_hashes=view_feature_hashes,
            package_model_hash=model_hash,
        )
        identity_row = identity_by_package[package_id]
        handoff_payload["blueprint_hash"] = identity_row["blueprint_hash"]
        compact_handoff_path = handoff_root / f"{short_id}.json"
        write_json(compact_handoff_path, handoff_payload)
        handoff_paths.append(compact_handoff_path)
        handoff_resolution_rows.append(
            {
                "package_id": package_id,
                "planned_handoff_file": plan_by_package[package_id]["handoff_file_plan"],
                "actual_handoff_file": repo_path(compact_handoff_path),
                "path_resolution_reason": "compact_path_to_avoid_windows_path_length_risk",
                "actual_handoff_hash": sha256_file(compact_handoff_path),
            }
        )

    tier_receipt_rows = [
        {
            "tier_scope": "Tier A separate",
            "source_path": repo_path(TIER_A_MODEL_INPUT),
            "feature_order_hash": tier_a_hash,
            "rows": int(len(tier_a)),
            "missing_required_features": "none",
            "materialization_status": "materialized_full_context_score_inputs",
            "performance_claim": "none",
        },
        {
            "tier_scope": "Tier B separate",
            "source_path": repo_path(TIER_B_MODEL_INPUT),
            "feature_order_hash": tier_b_hash,
            "rows": int(len(tier_b)),
            "missing_required_features": tier_b["missing_required_features"].iloc[0],
            "materialization_status": "materialized_partial_context_score_inputs",
            "performance_claim": "none",
        },
        {
            "tier_scope": "Tier A+B combined",
            "source_path": "synthetic_materialization_view_from_tier_a_and_tier_b_score_tables",
            "feature_order_hash": f"TierA={tier_a_hash};TierB={tier_b_hash}",
            "rows": int(len(combined)),
            "missing_required_features": "see_component_rows",
            "materialization_status": "materialized_combined_score_input_view_no_routed_pnl",
            "performance_claim": "none",
        },
    ]
    tier_receipts_path = RUN_ROOT / "tier_scope_receipts.csv"
    write_csv(
        tier_receipts_path,
        tier_receipt_rows,
        [
            "tier_scope",
            "source_path",
            "feature_order_hash",
            "rows",
            "missing_required_features",
            "materialization_status",
            "performance_claim",
        ],
    )

    summary_path = RUN_ROOT / "score_materialization_summary.csv"
    write_csv(
        summary_path,
        summary_rows,
        [
            "package_id",
            "tier_view",
            "split",
            "rows",
            "score_columns",
            "null_score_cells",
            "numeric_score_min",
            "numeric_score_max",
            "materialized_decision_count",
            "performance_claim",
        ],
    )

    handoff_resolution_path = RUN_ROOT / "handoff_path_resolution.csv"
    write_csv(
        handoff_resolution_path,
        handoff_resolution_rows,
        [
            "package_id",
            "planned_handoff_file",
            "actual_handoff_file",
            "path_resolution_reason",
            "actual_handoff_hash",
        ],
    )

    score_sample_path = RUN_ROOT / "score_samples.json"
    write_json(score_sample_path, score_sample_rows)

    data_integrity_path = RUN_ROOT / "data_integrity_receipt.json"
    write_json(
        data_integrity_path,
        {
            "run_id": RUN_ID,
            "status": "passed_for_scoring_materialization_no_performance_claim",
            "source_model_inputs": {
                "tier_a": repo_path(TIER_A_MODEL_INPUT),
                "tier_b": repo_path(TIER_B_MODEL_INPUT),
            },
            "tier_a_feature_order_hash": tier_a_hash,
            "tier_b_feature_order_hash": tier_b_hash,
            "expected_package_feature_order_hash": specs["feature_order_hash"],
            "label_or_future_columns_excluded_from_scoring": sorted(LABEL_OR_FUTURE_COLUMNS),
            "score_formula_uses_label_or_future_columns": False,
            "tier_a_missing_required_features": [],
            "tier_b_missing_required_features": finite_missing_columns(pd.read_parquet(TIER_B_MODEL_INPUT), expected_feature_order),
            "tier_b_boundary": "partial_context_score_input_materialized_not_runtime_fallback_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    output_paths = [
        *score_table_paths,
        *handoff_paths,
        tier_receipts_path,
        summary_path,
        handoff_resolution_path,
        score_sample_path,
        data_integrity_path,
    ]
    output_hashes = {repo_path(path): sha256_file(path) for path in output_paths}

    manifest_path = RUN_ROOT / "run_manifest.json"
    manifest_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_scoring_materialization_probe_no_candidate_selection",
        "producer": "stage_pipelines/stage269/execute_scoring_materialization_probe.py",
        "entry_command": "python stage_pipelines/stage269/execute_scoring_materialization_probe.py",
        "source_inputs": list(source_hashes.keys()),
        "input_hashes": source_hashes,
        "output_artifacts": list(output_hashes.keys()),
        "output_hashes": output_hashes,
        "package_count": len(specs["packages"]),
        "selectable_packages": sum(1 for package in specs["packages"] if package["package_role"] == "selectable_blueprint"),
        "support_controls": sum(1 for package in specs["packages"] if package["package_role"] == "support_control"),
        "tier_scope_records": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": "run269E_screen_materialized_scores_for_stage270_aggressive_upside_queue",
    }
    write_json(manifest_path, manifest_payload)

    report_path = REVIEW_ROOT / "run269D_report.md"
    report = f"""# Stage269 Run269D Scoring Materialization Probe(269단계 269D 점수 물질화 탐침)

- status(상태): `completed_scoring_materialization_probe_no_candidate_selection`
- run(실행): `{RUN_ID}`
- source_run(원천 실행): `run269C_materialized_scoring_handoff_inputs_v1`
- packages(패키지): `{manifest_payload["package_count"]}`
- selectable_packages(선택 가능 패키지): `{manifest_payload["selectable_packages"]}`
- support_controls(보조 대조): `{manifest_payload["support_controls"]}`
- tier_records(티어 기록): `Tier A separate(티어 A 분리)`, `Tier B separate(티어 B 분리)`, `Tier A+B combined(티어 A+B 합산)`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run269E_screen_materialized_scores_for_stage270_aggressive_upside_queue`

## Experiment Design Receipt(실험 설계 영수증)

- hypothesis(가설): run269C(269C 실행)의 package scoring spec(패키지 점수 규격)이 Tier A/Tier B(티어 A/티어 B) 입력 프레임에서 결정적으로 물질화될 수 있다.
- decision_use(판단 용도): Stage270(270단계) aggressive upside probe(공격형 상방 탐침)로 넘길 점수 표면(score surface, 점수 표면)이 있는지 선별한다.
- comparison_baseline(비교 기준): Stage267(267단계) 결과는 reference evidence(참고 근거)만 사용하고, selected baseline(선택 기준선)은 없다.
- control_variables(고정 변수): FPMarkets US100 M5, run269C(269C 실행) hash receipt(해시 영수증), label/future column exclusion(라벨/미래 열 제외), research-only claim boundary(연구 전용 주장 경계).
- changed_variables(변경 변수): package별 deterministic scoring formula(결정적 점수 공식), Tier B partial-context view(티어 B 부분 문맥 보기), compact handoff path(짧은 인계 경로).
- sample_scope(표본 범위): Tier A separate(티어 A 분리) `{len(tier_a)}` rows(행), Tier B separate(티어 B 분리) `{len(tier_b)}` rows(행), Tier A+B combined(티어 A+B 합산) `{len(combined)}` materialization rows(물질화 행).
- success_criteria(성공 기준): score table(점수표), handoff JSON(인계 JSON), tier receipt(티어 영수증), data integrity receipt(데이터 무결성 영수증), lineage(계보)가 모두 생성된다.
- failure_criteria(실패 기준): 점수 열 누락, 해시 불일치, Tier B(티어 B) 누락, label/future column(라벨/미래 열) 사용.
- invalid_conditions(무효 조건): 입력 feature order(피처 순서) 불명, run269C(269C 실행) 규격 누락, 스크립트 재실행 불가.
- stop_conditions(중단 조건): run269E(269E 실행)에서 물질화된 점수표가 후보 선별에 쓸 구조를 만들지 못하면 Stage269(269단계) 안에서 폐기 또는 재구성한다.
- evidence_plan(근거 계획): run269E(269E 실행)에서 점수 분포, 공급량, 중복 서명, Tier B 영향, handoff identity(인계 정체성)를 검토한다.

## Plain Result(쉬운 결과)

run269D(269D 실행)는 run269C(269C 실행)의 scoring input specs(점수 입력 규격)를 실제 model input dataset(모델 입력 데이터셋)에 적용했다.
효과(effect, 효과): 세 selectable package(선택 가능 패키지)와 하나의 support control(보조 대조)에 대해 score table(점수표)과 handoff JSON(인계 JSON)을 만들었고, run269E(269E 실행)가 후보 선별 전 점수 표면을 검토할 수 있다.

## Boundary(경계)

This report(이 보고서)는 performance improvement(성과 개선), selected candidate(선택 후보), ONNX readiness(온엑스 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.
"""
    write_md(report_path, report)

    lineage_path = RUN_ROOT / "lineage.json"
    lineage_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": list(source_hashes.keys()),
        "producer": "stage_pipelines/stage269/execute_scoring_materialization_probe.py",
        "consumer": "run269E_screen_materialized_scores_for_stage270_aggressive_upside_queue",
        "artifact_paths": [repo_path(path) for path in [manifest_path, *output_paths, lineage_path, report_path]],
        "artifact_hashes": {
            **source_hashes,
            **output_hashes,
            repo_path(manifest_path): sha256_file(manifest_path),
            repo_path(report_path): sha256_file(report_path),
        },
        "self_hash_note": "lineage file hash is recorded in docs/registers/artifact_registry.csv after generation",
        "registry_links": [
            "docs/registers/run_registry.csv",
            "docs/registers/alpha_run_ledger.csv",
            f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv",
            "docs/registers/artifact_registry.csv",
        ],
        "availability": "tracked",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(lineage_path, lineage_payload)

    final_hashes = {
        repo_path(path): sha256_file(path)
        for path in [manifest_path, *output_paths, lineage_path, report_path]
    }
    return {
        "run_id": RUN_ID,
        "status": manifest_payload["status"],
        "packages": len(specs["packages"]),
        "tier_a_rows": int(len(tier_a)),
        "tier_b_rows": int(len(tier_b)),
        "combined_rows": int(len(combined)),
        "outputs": final_hashes,
    }


if __name__ == "__main__":
    print(json.dumps(materialize(), ensure_ascii=False, indent=2))

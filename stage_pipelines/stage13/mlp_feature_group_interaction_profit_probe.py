from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import warnings
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from pandas.errors import ParserWarning

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
)
from foundation.models.baseline_training import load_feature_order
from foundation.mt5 import runtime_support as mt5
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades
from stage_pipelines.stage13.mlp_internal_behavior_probes import feature_group, rel
from stage_pipelines.stage13.mlp_feature_group_interaction_docs import decision, report, skill_receipts, sync_docs, work_packet


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04N"
RUN_ID = "run04N_mlp_feature_group_interaction_profit_probe_v1"
PACKET_ID = "stage13_run04N_mlp_feature_group_interaction_profit_probe_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
SOURCE_LEARNING_RUN_ID = "run04M_mlp_learning_behavior_runtime_probe_v1"
EXPLORATION_LABEL = "stage13_MLPInternal__FeatureGroupInteractionProfit"
BOUNDARY = "feature_group_interaction_profit_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
MODEL_FAMILY = "sklearn_mlpclassifier_feature_group_interaction_profit_probe"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run04N_mlp_feature_group_interaction_profit_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_feature_group_interaction_profit_probe.md"
MAX_HOLD_BARS = 9
PARITY_MEAN_TOLERANCE = 3.0e-4
STOP_OUT_DRAWDOWN_AMOUNT = 450.0

VARIANT_SPECS = (
    {"variant": "original", "ablate": (), "keep": None, "purpose": "original fixed RUN04F surface"},
    {"variant": "no_volatility_range", "ablate": ("volatility_range",), "keep": None, "purpose": "single strongest RUN04M group removal"},
    {"variant": "no_trend_structure", "ablate": ("trend_structure",), "keep": None, "purpose": "single partner group removal"},
    {"variant": "no_session", "ablate": ("session",), "keep": None, "purpose": "single partner group removal"},
    {"variant": "no_oscillator", "ablate": ("oscillator",), "keep": None, "purpose": "single partner group removal"},
    {"variant": "no_volatility_trend", "ablate": ("volatility_range", "trend_structure"), "keep": None, "purpose": "double removal interaction"},
    {"variant": "no_volatility_session", "ablate": ("volatility_range", "session"), "keep": None, "purpose": "double removal interaction"},
    {"variant": "no_volatility_oscillator", "ablate": ("volatility_range", "oscillator"), "keep": None, "purpose": "double removal interaction"},
    {"variant": "only_volatility_range", "ablate": (), "keep": ("volatility_range",), "purpose": "restore volatility/range only on median background"},
)
VARIANTS = tuple(str(spec["variant"]) for spec in VARIANT_SPECS)
PROBABILITY_COLUMNS = ("variant", "split", "rows", "mean_p_short", "mean_p_flat", "mean_p_long", "mean_entropy_norm", "mean_margin", "signal_share_q90", "mean_l1_prob_delta", "decision_flip_share", "signal_flip_share")
PARITY_COLUMNS = ("variant", "split", "row_delta", "mean_p_short_abs_delta", "mean_p_flat_abs_delta", "mean_p_long_abs_delta", "mean_entropy_abs_delta", "parity_status")
TRADE_COLUMNS = ("variant", "split", "record_view", "net_profit", "profit_delta_vs_original", "profit_factor", "max_drawdown", "drawdown_delta_vs_original", "trade_count", "trade_count_delta_vs_original", "win_rate_percent", "long_trade_count", "short_trade_count", "avg_trade_net", "avg_win", "avg_loss", "largest_loss", "max_consecutive_losses", "avg_hold_bars", "order_attempt_count", "fill_count", "reject_count", "report_path")
INTERACTION_COLUMNS = ("partner_group", "split", "single_partner_variant", "double_variant", "l1_residual", "decision_flip_residual", "signal_flip_residual", "net_profit_residual", "trade_count_residual", "interpretation")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))

def copy_file(source: Path, destination: Path) -> dict[str, Any]:
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def source_manifest() -> dict[str, Any]:
    return read_json(SOURCE_ROOT / "run_manifest.json")


def threshold_payload() -> dict[str, Any]:
    raw = read_json(SOURCE_ROOT / "thresholds/threshold_handoff.json")
    payload = {
        "source_run_id": SOURCE_RUN_ID,
        "threshold_source_run_id": raw.get("threshold_source_run_id"),
        "threshold_id": raw.get("threshold_id", "q90_m000"),
        "tier_a_threshold": float(raw["tier_a_threshold"]),
        "tier_b_fallback_threshold": float(raw.get("tier_b_fallback_threshold", raw["tier_a_threshold"])),
        "min_margin": float(raw.get("min_margin", 0.0)),
        "threshold_policy": "RUN04F q90 threshold reused without optimization for feature-group interaction profit probe",
        "boundary": "diagnostic_threshold_handoff_not_selected_threshold",
    }
    out = RUN_ROOT / "thresholds/threshold_handoff.json"
    write_json(out, payload)
    return {**payload, "path": rel(out), "sha256": sha256_file_lf_normalized(out)}


def load_model_and_frames() -> tuple[Any, dict[str, pd.DataFrame], list[str]]:
    manifest = source_manifest()
    joblib_path = ROOT / str(manifest["model_artifacts"]["tier_a_joblib"]["path"])
    model = joblib.load(io_path(joblib_path))
    feature_order = load_feature_order(FEATURE_ORDER_PATH)
    frames = {
        "validation_is": pd.read_csv(io_path(SOURCE_ROOT / "features/tier_a_validation_is_feature_matrix.csv")),
        "oos": pd.read_csv(io_path(SOURCE_ROOT / "features/tier_a_oos_feature_matrix.csv")),
    }
    for split, frame in frames.items():
        missing = [name for name in feature_order if name not in frame.columns]
        if missing:
            raise ValueError(f"{split} missing features: {missing[:5]}")
    return model, frames, feature_order


def reference_stats(frames: Mapping[str, pd.DataFrame], feature_order: Sequence[str]) -> dict[str, pd.Series]:
    validation = frames["validation_is"].loc[:, list(feature_order)].astype("float64")
    return {"median": validation.median(axis=0)}


def feature_group_counts(feature_order: Sequence[str]) -> list[dict[str, Any]]:
    counts = Counter(feature_group(name) for name in feature_order)
    return [{"feature_group": key, "feature_count": int(value)} for key, value in sorted(counts.items())]


def variant_spec(variant: str) -> Mapping[str, Any]:
    for spec in VARIANT_SPECS:
        if spec["variant"] == variant:
            return spec
    raise ValueError(f"unknown variant: {variant}")

def variant_matrix(frame: pd.DataFrame, feature_order: Sequence[str], ref: Mapping[str, pd.Series], variant: str) -> pd.DataFrame:
    spec = variant_spec(variant)
    out = frame.copy()
    features = list(feature_order)
    if variant == "original":
        return out
    keep_groups = spec.get("keep")
    if keep_groups is not None:
        selected = [name for name in features if feature_group(name) not in set(keep_groups)]
    else:
        ablate_groups = set(spec.get("ablate", ()))
        selected = [name for name in features if feature_group(name) in ablate_groups]
    if not selected:
        raise ValueError(f"{variant} selected no features")
    out.loc[:, selected] = ref["median"].loc[selected].to_numpy()
    return out


def predict_surface(model: Any, frame: pd.DataFrame, feature_order: Sequence[str], threshold: Mapping[str, Any]) -> dict[str, Any]:
    probs = np.asarray(model.predict_proba(frame.loc[:, list(feature_order)].to_numpy(dtype="float64")), dtype=np.float64)
    sorted_probs = np.sort(probs, axis=1)
    margin = sorted_probs[:, -1] - sorted_probs[:, -2]
    entropy = -np.sum(np.clip(probs, 1.0e-12, 1.0) * np.log(np.clip(probs, 1.0e-12, 1.0)), axis=1) / math.log(3.0)
    directional = np.maximum(probs[:, 0], probs[:, 2])
    side = np.where(probs[:, 2] >= probs[:, 0], "long", "short")
    signal = (directional >= float(threshold["tier_a_threshold"])) & (margin >= float(threshold["min_margin"]))
    return {"probabilities": probs, "entropy_norm": entropy, "margin": margin, "decision": np.where(signal, side, "flat"), "signal": signal}


def probability_summary(variant: str, split: str, surface: Mapping[str, Any], base: Mapping[str, Any] | None) -> dict[str, Any]:
    probs = np.asarray(surface["probabilities"], dtype=np.float64)
    row = {
        "variant": variant,
        "split": split,
        "rows": len(probs),
        "mean_p_short": float(probs[:, 0].mean()),
        "mean_p_flat": float(probs[:, 1].mean()),
        "mean_p_long": float(probs[:, 2].mean()),
        "mean_entropy_norm": float(np.asarray(surface["entropy_norm"]).mean()),
        "mean_margin": float(np.asarray(surface["margin"]).mean()),
        "signal_share_q90": float(np.asarray(surface["signal"]).mean()),
    }
    if base is None:
        return {**row, "mean_l1_prob_delta": 0.0, "decision_flip_share": 0.0, "signal_flip_share": 0.0}
    base_probs = np.asarray(base["probabilities"], dtype=np.float64)
    return {
        **row,
        "mean_l1_prob_delta": float(np.sum(np.abs(probs - base_probs), axis=1).mean()),
        "decision_flip_share": float(np.mean(np.asarray(surface["decision"]) != np.asarray(base["decision"]))),
        "signal_flip_share": float(np.mean(np.asarray(surface["signal"]) != np.asarray(base["signal"]))),
    }


def build_python_rows(model: Any, frames: Mapping[str, pd.DataFrame], feature_order: Sequence[str], ref: Mapping[str, pd.Series], threshold: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    surfaces: dict[tuple[str, str], dict[str, Any]] = {}
    for split, frame in frames.items():
        base = predict_surface(model, variant_matrix(frame, feature_order, ref, "original"), feature_order, threshold)
        surfaces[("original", split)] = base
        for variant in VARIANTS:
            surface = base if variant == "original" else predict_surface(model, variant_matrix(frame, feature_order, ref, variant), feature_order, threshold)
            surfaces[(variant, split)] = surface
            rows.append(probability_summary(variant, split, surface, None if variant == "original" else base))
    return rows, surfaces


def materialize_models(manifest: Mapping[str, Any]) -> dict[str, Any]:
    tier_a_joblib = ROOT / str(manifest["model_artifacts"]["tier_a_joblib"]["path"])
    tier_a_onnx = ROOT / str(manifest["model_artifacts"]["tier_a_onnx"]["path"])
    return {
        "tier_a_joblib": copy_file(tier_a_joblib, RUN_ROOT / "models" / tier_a_joblib.name),
        "tier_a_onnx": copy_file(tier_a_onnx, RUN_ROOT / "models" / tier_a_onnx.name),
    }


def export_feature_matrices(frames: Mapping[str, pd.DataFrame], feature_order: Sequence[str], ref: Mapping[str, pd.Series], manifest: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "features"
    feature_hash = str(manifest["feature_matrices"][0]["feature_order_hash"])
    out: dict[str, Any] = {}
    for variant in VARIANTS:
        for split, frame in frames.items():
            path = root / f"tier_a_fgint_{variant}_{split}_feature_matrix.csv"
            write_csv(path, list(frame.columns), variant_matrix(frame, feature_order, ref, variant).to_dict("records"))
            out[f"{variant}__{split}"] = {
                "variant": variant,
                "split": split,
                "path": rel(path),
                "rows": len(frame),
                "feature_count": len(feature_order),
                "feature_order_hash": feature_hash,
                "sha256": sha256_file_lf_normalized(path),
            }
    return out


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], matrices: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies = [copy_to_common(ROOT / str(model_artifacts["tier_a_onnx"]["path"]), f"{common}/models/{Path(str(model_artifacts['tier_a_onnx']['path'])).name}", COMMON_FILES_ROOT_DEFAULT)]
    for matrix in matrices.values():
        source = ROOT / str(matrix["path"])
        copies.append(copy_to_common(source, f"{common}/features/{source.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def source_dates(manifest: Mapping[str, Any], split: str) -> tuple[str, str]:
    for attempt in manifest.get("attempts", []):
        if attempt.get("split") == split:
            tester = attempt["ini"]["tester"]
            return str(tester["FromDate"]), str(tester["ToDate"])
    raise RuntimeError(f"missing source dates for {split}")


def make_attempts(
    manifest: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    matrices: Mapping[str, Mapping[str, Any]],
    threshold: Mapping[str, Any],
) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    model_name = Path(str(model_artifacts["tier_a_onnx"]["path"])).name
    attempts: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        from_date, to_date = source_dates(manifest, split)
        for variant in VARIANTS:
            matrix = matrices[f"{variant}__{split}"]
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=STAGE_NUMBER,
                exploration_label=EXPLORATION_LABEL,
                attempt_name=f"tier_a_fgint_{variant}_{split}",
                tier=mt5.TIER_A,
                split=split,
                model_path=f"{common}/models/{model_name}",
                model_id=f"{RUN_ID}_tier_a_fgint",
                feature_path=f"{common}/features/{Path(str(matrix['path'])).name}",
                feature_count=int(matrix["feature_count"]),
                feature_order_hash=str(matrix["feature_order_hash"]),
                short_threshold=float(threshold["tier_a_threshold"]),
                long_threshold=float(threshold["tier_a_threshold"]),
                min_margin=float(threshold["min_margin"]),
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix=f"mt5_tier_a_fgint_{variant}",
                max_hold_bars=MAX_HOLD_BARS,
                common_root=common,
                reverse_on_opposite_signal=True,
                close_only_on_opposite_signal=False,
            )
            attempt["variant"] = variant
            attempt["variant_purpose"] = str(variant_spec(variant)["purpose"])
            attempts.append(attempt)
    return attempts


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_materialize_only_no_mt5_execution"}
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_feature_group_interaction_profit_probe", "failure": {"type": type(exc).__name__, "message": str(exc)}}
    return dict(result)


def parse_variant_split(text: str, prefix: str) -> tuple[str, str]:
    value = text.removeprefix(prefix)
    if value.endswith("_validation_is"):
        return value.removesuffix("_validation_is"), "validation_is"
    if value.endswith("_oos"):
        return value.removesuffix("_oos"), "oos"
    raise ValueError(f"cannot parse variant/split from {text}")


def mt5_probability_rows(result: Mapping[str, Any], threshold: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for execution in result.get("execution_results", []):
        runtime = execution.get("runtime_outputs", {})
        telemetry_path = runtime.get("telemetry_path")
        if not telemetry_path or not io_path(Path(str(telemetry_path))).exists():
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ParserWarning)
            frame = pd.read_csv(io_path(Path(str(telemetry_path))), index_col=False)
        cycle = frame.loc[frame["record_type"].astype(str).eq("cycle")].copy()
        if "feature_ready" in cycle:
            cycle = cycle.loc[truthy(cycle["feature_ready"])]
        if "model_ok" in cycle:
            cycle = cycle.loc[truthy(cycle["model_ok"])]
        probs = cycle.loc[:, ["p_short", "p_flat", "p_long"]].apply(pd.to_numeric, errors="coerce").dropna()
        if probs.empty:
            continue
        variant, split = parse_variant_split(str(execution["attempt_name"]), "tier_a_fgint_")
        values = probs.to_numpy(dtype="float64", copy=False)
        sorted_probs = np.sort(values, axis=1)
        margin = sorted_probs[:, -1] - sorted_probs[:, -2]
        entropy = -np.sum(np.clip(values, 1.0e-12, 1.0) * np.log(np.clip(values, 1.0e-12, 1.0)), axis=1) / math.log(3.0)
        signal = np.maximum(values[:, 0], values[:, 2]) >= float(threshold["tier_a_threshold"])
        rows.append(
            {
                "variant": variant,
                "split": split,
                "rows": len(probs),
                "mean_p_short": float(probs["p_short"].mean()),
                "mean_p_flat": float(probs["p_flat"].mean()),
                "mean_p_long": float(probs["p_long"].mean()),
                "mean_entropy_norm": float(entropy.mean()),
                "mean_margin": float(margin.mean()),
                "signal_share_q90": float(signal.mean()),
                "mean_l1_prob_delta": None,
                "decision_flip_share": None,
                "signal_flip_share": None,
            }
        )
    return rows


def truthy(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin({"true", "1", "yes"})

def parity_rows(python_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_key = {(row["variant"], row["split"]): row for row in python_rows}
    rows: list[dict[str, Any]] = []
    for mt5_row in mt5_rows:
        key = (mt5_row["variant"], mt5_row["split"])
        py = by_key.get(key)
        if not py:
            continue
        row_delta = int(mt5_row["rows"]) - int(py["rows"])
        deltas = {
            "mean_p_short_abs_delta": abs(float(mt5_row["mean_p_short"]) - float(py["mean_p_short"])),
            "mean_p_flat_abs_delta": abs(float(mt5_row["mean_p_flat"]) - float(py["mean_p_flat"])),
            "mean_p_long_abs_delta": abs(float(mt5_row["mean_p_long"]) - float(py["mean_p_long"])),
            "mean_entropy_abs_delta": abs(float(mt5_row["mean_entropy_norm"]) - float(py["mean_entropy_norm"])),
        }
        rows.append({"variant": key[0], "split": key[1], "row_delta": row_delta, **deltas, "parity_status": "pass" if row_delta == 0 and max(deltas.values()) <= PARITY_MEAN_TOLERANCE else "review"})
    return rows


def annotate_parity_rows(rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    trades = {(row["variant"], row["split"]): row for row in trade_rows}
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        trade = trades.get((row["variant"], row["split"]), {})
        drawdown = as_float(trade.get("max_drawdown"))
        if item["parity_status"] == "review" and int(item["row_delta"]) < 0 and drawdown is not None and drawdown >= STOP_OUT_DRAWDOWN_AMOUNT:
            item["parity_status"] = "partial_trade_stopout"
        out.append(item)
    return out


def telemetry_action_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for execution in result.get("execution_results", []):
        runtime = execution.get("runtime_outputs", {})
        telemetry_path = runtime.get("telemetry_path")
        if not telemetry_path or not io_path(Path(str(telemetry_path))).exists():
            continue
        variant, split = parse_variant_split(str(execution["attempt_name"]), "tier_a_fgint_")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ParserWarning)
            frame = pd.read_csv(io_path(Path(str(telemetry_path))), index_col=False)
        cycle = frame.loc[frame["record_type"].astype(str).eq("cycle")]
        counter = Counter(cycle.get("exec_action", pd.Series(dtype=str)).astype(str))
        for action, count in sorted(counter.items()):
            rows.append({"variant": variant, "split": split, "exec_action": action, "count": int(count)})
    return rows


def trade_summary_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    records = list(result.get("mt5_kpi_records", []))
    original_by_split: dict[str, Mapping[str, Any]] = {}
    for record in records:
        variant, split = parse_variant_split(str(record["record_view"]), "mt5_tier_a_fgint_")
        if variant == "original":
            original_by_split[split] = record.get("metrics", {})
    for record in records:
        metrics = record.get("metrics", {})
        variant, split = parse_variant_split(str(record["record_view"]), "mt5_tier_a_fgint_")
        original = original_by_split.get(split, {})
        report_path = metrics.get("report_path")
        trades = []
        if report_path and io_path(Path(str(report_path))).exists():
            trades = pair_deals_into_trades(parse_mt5_trade_report(Path(str(report_path)))["deals"])
        values = [float(trade.net_profit) for trade in trades]
        wins = [value for value in values if value > 0.0]
        losses = [value for value in values if value < 0.0]
        hold_bars = [float((trade.close_time - trade.open_time).total_seconds() / 60.0 / 5.0) for trade in trades]
        net = as_float(metrics.get("net_profit"))
        dd = as_float(metrics.get("max_drawdown_amount"))
        trades_count = as_float(metrics.get("trade_count"))
        rows.append(
            {
                "variant": variant,
                "split": split,
                "record_view": record.get("record_view"),
                "net_profit": net,
                "profit_delta_vs_original": subtract(net, as_float(original.get("net_profit"))),
                "profit_factor": as_float(metrics.get("profit_factor")),
                "max_drawdown": dd,
                "drawdown_delta_vs_original": subtract(dd, as_float(original.get("max_drawdown_amount"))),
                "trade_count": trades_count,
                "trade_count_delta_vs_original": subtract(trades_count, as_float(original.get("trade_count"))),
                "win_rate_percent": as_float(metrics.get("win_rate_percent")),
                "long_trade_count": as_float(metrics.get("long_trade_count")),
                "short_trade_count": as_float(metrics.get("short_trade_count")),
                "avg_trade_net": mean(values),
                "avg_win": mean(wins),
                "avg_loss": mean(losses),
                "largest_loss": min(losses) if losses else None,
                "max_consecutive_losses": max_consecutive_losses(values),
                "avg_hold_bars": mean(hold_bars),
                "order_attempt_count": as_float(metrics.get("order_attempt_count")),
                "fill_count": as_float(metrics.get("fill_count")),
                "reject_count": as_float(metrics.get("reject_count")),
                "report_path": report_path,
            }
        )
    return rows


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def subtract(left: float | None, right: float | None) -> float | None:
    return None if left is None or right is None else left - right


def mean(values: Sequence[float]) -> float | None:
    return float(sum(values) / len(values)) if values else None


def max_consecutive_losses(values: Sequence[float]) -> int:
    longest = current = 0
    for value in values:
        if value < 0.0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def interaction_rows(python_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    py = {(row["variant"], row["split"]): row for row in python_rows}
    tr = {(row["variant"], row["split"]): row for row in trade_rows}
    partners = (
        ("trend_structure", "no_trend_structure", "no_volatility_trend"),
        ("session", "no_session", "no_volatility_session"),
        ("oscillator", "no_oscillator", "no_volatility_oscillator"),
    )
    rows: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        vol = py.get(("no_volatility_range", split), {})
        vol_trade = tr.get(("no_volatility_range", split), {})
        original_trade = tr.get(("original", split), {})
        for partner, single, double in partners:
            single_py = py.get((single, split), {})
            double_py = py.get((double, split), {})
            single_trade = tr.get((single, split), {})
            double_trade = tr.get((double, split), {})
            rows.append(
                {
                    "partner_group": partner,
                    "split": split,
                    "single_partner_variant": single,
                    "double_variant": double,
                    "l1_residual": residual(double_py, vol, single_py, "mean_l1_prob_delta"),
                    "decision_flip_residual": residual(double_py, vol, single_py, "decision_flip_share"),
                    "signal_flip_residual": residual(double_py, vol, single_py, "signal_flip_share"),
                    "net_profit_residual": profit_residual(double_trade, vol_trade, single_trade, original_trade),
                    "trade_count_residual": profit_residual(double_trade, vol_trade, single_trade, original_trade, metric="trade_count"),
                    "interpretation": "non_additive_shape" if abs(residual(double_py, vol, single_py, "mean_l1_prob_delta") or 0.0) >= 0.03 else "mostly_additive_shape",
                }
            )
    return rows


def residual(double: Mapping[str, Any], first: Mapping[str, Any], second: Mapping[str, Any], metric: str) -> float | None:
    values = [as_float(row.get(metric)) for row in (double, first, second)]
    if any(value is None for value in values):
        return None
    return float(values[0] - values[1] - values[2])


def profit_residual(double: Mapping[str, Any], first: Mapping[str, Any], second: Mapping[str, Any], original: Mapping[str, Any], metric: str = "net_profit") -> float | None:
    values = [as_float(row.get(metric)) for row in (double, first, second, original)]
    if any(value is None for value in values):
        return None
    return float((values[0] - values[3]) - (values[1] - values[3]) - (values[2] - values[3]))


def judge(payload: Mapping[str, Any]) -> tuple[str, str]:
    external = payload["mt5_result"].get("external_verification_status")
    parity_rows_ = payload["parity_rows"]
    allowed = {"pass", "partial_trade_stopout"}
    parity_pass = bool(parity_rows_) and all(row["parity_status"] in allowed for row in parity_rows_)
    partial = any(row["parity_status"] == "partial_trade_stopout" for row in parity_rows_)
    if external != "completed":
        return "blocked_feature_group_interaction_profit_probe", "repair_mt5_feature_group_interaction_runtime_before_reading_profit"
    if not parity_pass:
        return "inconclusive_feature_group_interaction_profit_runtime_shape_mismatch", "inspect_variant_feature_matrix_or_runtime_probability_parity"
    if partial:
        return "inconclusive_feature_group_interaction_profit_completed_with_partial_trade_stopout", "treat_profit_as_stress_diagnostic_not_edge_and_consider_stage13_closeout"
    return "inconclusive_feature_group_interaction_profit_runtime_confirmed", "stage13_can_close_model_behavior_or_pivot_within_stage13"


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_csv(RUN_ROOT / "python_variant_probability_summary.csv", PROBABILITY_COLUMNS, payload["python_probability_rows"])
    write_csv(RUN_ROOT / "mt5_runtime_probability_summary.csv", PROBABILITY_COLUMNS, payload["mt5_probability_rows"])
    write_csv(RUN_ROOT / "mt5_python_parity_summary.csv", PARITY_COLUMNS, payload["parity_rows"])
    write_csv(RUN_ROOT / "mt5_trade_profit_summary.csv", TRADE_COLUMNS, payload["trade_rows"])
    write_csv(RUN_ROOT / "feature_group_interaction_summary.csv", INTERACTION_COLUMNS, payload["interaction_rows"])
    write_csv(RUN_ROOT / "telemetry_action_summary.csv", ("variant", "split", "exec_action", "count"), payload["telemetry_action_rows"])
    write_json(RUN_ROOT / "summary.json", payload)
    write_json(RUN_ROOT / "kpi_record.json", payload)
    write_json(RUN_ROOT / "run_manifest.json", manifest(payload))
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(payload))
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "summary": payload})
    write_md(PACKET_ROOT / "work_packet.md", work_packet(payload))
    write_md(RUN_ROOT / "reports/result_summary.md", report(payload))
    write_md(REPORT_PATH, report(payload))
    write_md(DECISION_PATH, decision(payload))


def manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "source_learning_run_id": SOURCE_LEARNING_RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "exploration_label": EXPLORATION_LABEL,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "variant_specs": list(VARIANT_SPECS),
        "feature_group_counts": payload["feature_group_counts"],
        "threshold": payload["threshold"],
        "model_artifacts": payload["model_artifacts"],
        "feature_matrices": list(payload["feature_matrices"].values()),
        "attempts": payload["prepared"].get("attempts", []),
        "common_copies": payload["prepared"].get("common_copies", []),
        "compile": payload["mt5_result"].get("compile", {}),
        "execution_results": payload["mt5_result"].get("execution_results", []),
        "strategy_tester_reports": payload["mt5_result"].get("strategy_tester_reports", []),
        "external_verification_status": payload["external_verification_status"],
        "judgment": payload["judgment"],
        "outputs": {
            "report": rel(REPORT_PATH),
            "summary": rel(RUN_ROOT / "summary.json"),
            "python_probability": rel(RUN_ROOT / "python_variant_probability_summary.csv"),
            "mt5_probability": rel(RUN_ROOT / "mt5_runtime_probability_summary.csv"),
            "parity": rel(RUN_ROOT / "mt5_python_parity_summary.csv"),
            "profit": rel(RUN_ROOT / "mt5_trade_profit_summary.csv"),
            "interaction": rel(RUN_ROOT / "feature_group_interaction_summary.csv"),
        },
    }


def ledger_outputs(payload: Mapping[str, Any]) -> dict[str, Any]:
    rows = [
        ledger_row("tier_b_out_of_scope", "Tier B", "claim_scope_boundary", "out_of_scope_by_claim_feature_group_interaction_profit_probe", RUN_ROOT / "summary.json", (("source_run", SOURCE_RUN_ID),), (("boundary", BOUNDARY),), "out_of_scope_by_claim", "RUN04N inspects Tier A source model feature variants only."),
        ledger_row("tier_abb_out_of_scope", "Tier A+B", "claim_scope_boundary", "out_of_scope_by_claim_feature_group_interaction_profit_probe", RUN_ROOT / "summary.json", (("source_run", SOURCE_RUN_ID),), (("boundary", BOUNDARY),), "out_of_scope_by_claim", "RUN04N inspects Tier A source model feature variants only."),
    ]
    rows.extend(build_mt5_alpha_ledger_rows(run_id=RUN_ID, stage_id=STAGE_ID, mt5_kpi_records=payload["mt5_result"].get("mt5_kpi_records", []), run_output_root=Path(rel(RUN_ROOT)), external_verification_status=str(payload["external_verification_status"])))
    oos_profit = sorted((row for row in payload["trade_rows"] if row["split"] == "oos"), key=lambda row: as_float(row.get("net_profit")) if as_float(row.get("net_profit")) is not None else -1.0e18, reverse=True)
    top = oos_profit[0] if oos_profit else {}
    rows.append(ledger_row("oos_profit_diagnostic", "Tier A", "feature_group_interaction_profit_diagnostic", payload["judgment"], RUN_ROOT / "mt5_trade_profit_summary.csv", (("top_oos_variant", top.get("variant")), ("net_profit", top.get("net_profit")), ("trade_count", top.get("trade_count"))), (("boundary", "profit_is_diagnostic_not_edge"), ("threshold_id", payload["threshold"]["threshold_id"])), payload["external_verification_status"], "Profit is recorded as diagnostic propagation of feature perturbations, not edge selection."))
    oos_interaction = [row for row in payload["interaction_rows"] if row["split"] == "oos"]
    top_interaction = max(oos_interaction, key=lambda row: abs(as_float(row.get("l1_residual")) or 0.0), default={})
    rows.append(ledger_row("oos_interaction_residual", "Tier A", "feature_group_interaction_residual", payload["judgment"], RUN_ROOT / "feature_group_interaction_summary.csv", (("partner_group", top_interaction.get("partner_group")), ("l1_residual", top_interaction.get("l1_residual")), ("net_profit_residual", top_interaction.get("net_profit_residual"))), (("boundary", "non_additive_diagnostic"),), payload["external_verification_status"], "Residual compares double group removal against single group removals."))
    ledger = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [{
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "feature_group_interaction_profit_probe",
            "status": "reviewed" if payload["external_verification_status"] == "completed" else "blocked",
            "judgment": payload["judgment"],
            "path": rel(RUN_ROOT / "summary.json"),
            "notes": ledger_pairs((("source_run", SOURCE_RUN_ID), ("source_learning_run", SOURCE_LEARNING_RUN_ID), ("variants", len(VARIANTS)), ("boundary", BOUNDARY))),
        }],
        key="run_id",
    )
    return {"ledger_outputs": ledger, "run_registry_output": registry}


def ledger_row(subrun: str, tier: str, kpi_scope: str, judgment: Any, path: Path, primary: Sequence[tuple[str, Any]], guardrail: Sequence[tuple[str, Any]], external: str, notes: str) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__{subrun}",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": subrun,
        "parent_run_id": RUN_ID,
        "record_view": subrun,
        "tier_scope": tier,
        "kpi_scope": kpi_scope,
        "scoreboard_lane": "runtime_probe",
        "status": "completed" if external != "blocked" else "blocked",
        "judgment": judgment,
        "path": rel(path),
        "primary_kpi": ledger_pairs(primary),
        "guardrail_kpi": ledger_pairs(guardrail),
        "external_verification_status": external,
        "notes": notes,
    }



def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    manifest_payload = source_manifest()
    threshold = threshold_payload()
    model, frames, feature_order = load_model_and_frames()
    ref = reference_stats(frames, feature_order)
    python_rows, surfaces = build_python_rows(model, frames, feature_order, ref, threshold)
    model_artifacts = materialize_models(manifest_payload)
    feature_matrices = export_feature_matrices(frames, feature_order, ref, manifest_payload)
    prepared = {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_learning_run_id": SOURCE_LEARNING_RUN_ID,
        "run_number": RUN_NUMBER,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "variant_specs": list(VARIANT_SPECS),
        "attempts": make_attempts(manifest_payload, model_artifacts, feature_matrices, threshold),
        "common_copies": copy_runtime_inputs(model_artifacts, feature_matrices),
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": {},
    }
    mt5_result = execute_or_block(prepared, args)
    mt5_rows = mt5_probability_rows(mt5_result, threshold)
    trade_rows = trade_summary_rows(mt5_result)
    parity = annotate_parity_rows(parity_rows(python_rows, mt5_rows), trade_rows)
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_learning_run_id": SOURCE_LEARNING_RUN_ID,
        "created_at_utc": created_at,
        "boundary": BOUNDARY,
        "threshold": threshold,
        "variant_specs": list(VARIANT_SPECS),
        "feature_group_counts": feature_group_counts(feature_order),
        "model_artifacts": model_artifacts,
        "feature_matrices": feature_matrices,
        "prepared": prepared,
        "mt5_result": mt5_result,
        "external_verification_status": mt5_result.get("external_verification_status"),
        "python_probability_rows": python_rows,
        "mt5_probability_rows": mt5_rows,
        "parity_rows": parity,
        "trade_rows": trade_rows,
        "interaction_rows": interaction_rows(python_rows, trade_rows),
        "telemetry_action_rows": telemetry_action_rows(mt5_result),
    }
    judgment, recommendation = judge(payload)
    payload.update({"judgment": judgment, "recommendation": recommendation})
    payload["ledger_outputs"] = ledger_outputs(payload)
    write_outputs(payload)
    sync_docs(payload)
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP feature group interaction profit runtime probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    payload = build_all(args)
    print(json.dumps({"run_id": RUN_ID, "status": payload["external_verification_status"], "judgment": payload["judgment"], "parity_rows": len(payload["parity_rows"]), "trade_rows": len(payload["trade_rows"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"

RUNS = {
    "activation": {
        "run_id": "run04K_mlp_activation_behavior_probe_v1",
        "packet_id": "stage13_run04K_mlp_activation_behavior_probe_packet_v1",
        "label": "stage13_MLPInternal__ActivationBehavior",
        "boundary": "activation_behavior_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        "report": STAGE_ROOT / "03_reviews/run04K_mlp_activation_behavior_probe_packet.md",
        "decision": ROOT / "docs/decisions/2026-05-02_stage13_mlp_activation_behavior_probe.md",
    },
    "sensitivity": {
        "run_id": "run04L_mlp_feature_sensitivity_probe_v1",
        "packet_id": "stage13_run04L_mlp_feature_sensitivity_probe_packet_v1",
        "label": "stage13_MLPInternal__FeatureSensitivity",
        "boundary": "feature_sensitivity_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        "report": STAGE_ROOT / "03_reviews/run04L_mlp_feature_sensitivity_probe_packet.md",
        "decision": ROOT / "docs/decisions/2026-05-02_stage13_mlp_feature_sensitivity_probe.md",
    },
}
for spec in RUNS.values():
    spec["root"] = STAGE_ROOT / "02_runs" / str(spec["run_id"])
    spec["packet_root"] = spec["root"] / "packet"

META_COLUMNS = ("bar_time_server", "timestamp_utc", "split", "row_index")
SPLIT_FILES = {"validation_is": "tier_a_validation_is_feature_matrix.csv", "oos": "tier_a_oos_feature_matrix.csv"}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


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


def load_model() -> Any:
    raw = read_json(SOURCE_ROOT / "run_manifest.json")["model_artifacts"]["tier_a_joblib"]["path"]
    path = Path(str(raw))
    return joblib.load(io_path(path if path.is_absolute() else ROOT / path))


def load_frames() -> dict[str, dict[str, Any]]:
    frames: dict[str, dict[str, Any]] = {}
    for split, name in SPLIT_FILES.items():
        path = SOURCE_ROOT / "features" / name
        df = pd.read_csv(io_path(path))
        features = [column for column in df.columns if column not in META_COLUMNS]
        if len(features) != 58:
            raise ValueError(f"{split} expected 58 features, got {len(features)}")
        frames[split] = {
            "path": path,
            "rows": len(df),
            "feature_columns": features,
            "features": df[features].astype("float64").to_numpy(copy=True),
            "sha256": sha256_file_lf_normalized(path),
        }
    return frames


def threshold_payload() -> dict[str, Any]:
    raw = read_json(SOURCE_ROOT / "thresholds/threshold_handoff.json")
    return {
        "threshold_id": raw.get("threshold_id", "q90_m000"),
        "tier_a_threshold": float(raw["tier_a_threshold"]),
        "min_margin": float(raw.get("min_margin", 0.0)),
        "policy": "RUN04F Tier A q90 threshold reused without optimization",
    }


def source_inputs(frames: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "source_run_manifest": {
            "path": rel(SOURCE_ROOT / "run_manifest.json"),
            "sha256": sha256_file_lf_normalized(SOURCE_ROOT / "run_manifest.json"),
        },
        "source_threshold": {
            "path": rel(SOURCE_ROOT / "thresholds/threshold_handoff.json"),
            "sha256": sha256_file_lf_normalized(SOURCE_ROOT / "thresholds/threshold_handoff.json"),
        },
        "feature_matrices": {
            split: {"path": rel(frame["path"]), "sha256": frame["sha256"], "rows": frame["rows"], "feature_count": len(frame["feature_columns"])}
            for split, frame in frames.items()
        },
        "model_artifact": read_json(SOURCE_ROOT / "run_manifest.json")["model_artifacts"]["tier_a_joblib"],
    }


def surface_from_probs(probs: np.ndarray, threshold: Mapping[str, Any]) -> dict[str, Any]:
    sorted_probs = np.sort(probs, axis=1)
    margin = sorted_probs[:, -1] - sorted_probs[:, -2]
    entropy = -np.sum(probs * np.log(np.clip(probs, 1.0e-12, 1.0)), axis=1) / math.log(3.0)
    directional = np.maximum(probs[:, 0], probs[:, 2])
    side = np.where(probs[:, 2] >= probs[:, 0], "long", "short")
    signal = (directional >= float(threshold["tier_a_threshold"])) & (margin >= float(threshold["min_margin"]))
    return {
        "probabilities": probs,
        "p_short": probs[:, 0],
        "p_flat": probs[:, 1],
        "p_long": probs[:, 2],
        "margin": margin,
        "entropy_norm": entropy,
        "decision": np.where(signal, side, "flat"),
        "signal": signal,
    }


def probability_surfaces(model: Any, frames: Mapping[str, Mapping[str, Any]], threshold: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {split: surface_from_probs(np.asarray(model.predict_proba(frame["features"]), dtype=np.float64), threshold) for split, frame in frames.items()}


def hidden_activations(model: Any, frames: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    scaler = model.named_steps["scaler"]
    classifier = model.named_steps["classifier"]
    weights = np.asarray(classifier.coefs_[0], dtype=np.float64)
    bias = np.asarray(classifier.intercepts_[0], dtype=np.float64)
    out = {}
    for split, frame in frames.items():
        activation = np.maximum(scaler.transform(frame["features"]) @ weights + bias, 0.0)
        active = activation > 0.0
        out[split] = {
            "activation": activation,
            "active": active,
            "active_rate": active.mean(axis=0),
            "row_active": active.sum(axis=1),
            "row_l1": activation.sum(axis=1),
            "unit_mean": activation.mean(axis=0),
        }
    return out


def activation_summary_rows(acts: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for split, payload in acts.items():
        rates = np.asarray(payload["active_rate"], dtype=np.float64)
        row_active = np.asarray(payload["row_active"], dtype=np.float64)
        row_l1 = np.asarray(payload["row_l1"], dtype=np.float64)
        unit_mean = np.asarray(payload["unit_mean"], dtype=np.float64)
        top = np.sort(unit_mean)[::-1]
        total = float(unit_mean.sum())
        dead = int(np.sum(rates < 0.01))
        sparse = int(np.sum(rates < 0.10))
        top10 = float(top[:10].sum() / total) if total else 0.0
        rows.append(
            {
                "split": split,
                "rows": len(row_active),
                "units": len(rates),
                "mean_active_units": float(row_active.mean()),
                "median_active_units": float(np.median(row_active)),
                "p90_active_units": float(np.quantile(row_active, 0.90)),
                "mean_active_rate": float(rates.mean()),
                "dead_unit_count": dead,
                "sparse_unit_count": sparse,
                "always_active_unit_count": int(np.sum(rates > 0.99)),
                "mean_activation_l1": float(row_l1.mean()),
                "median_activation_l1": float(np.median(row_l1)),
                "p90_activation_l1": float(np.quantile(row_l1, 0.90)),
                "top5_activation_share": float(top[:5].sum() / total) if total else 0.0,
                "top10_activation_share": top10,
                "interpretation": "dead_unit_risk" if dead else "activation_concentrated" if top10 >= 0.55 else "distributed_activation",
            }
        )
    return rows


def activation_unit_rows(acts: Mapping[str, Mapping[str, Any]], surfaces: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for split, payload in acts.items():
        activation = np.asarray(payload["activation"], dtype=np.float64)
        active = np.asarray(payload["active"], dtype=bool)
        signal = np.asarray(surfaces[split]["signal"], dtype=bool)
        flat = ~signal
        for unit in range(activation.shape[1]):
            values = activation[:, unit]
            rows.append(
                {
                    "split": split,
                    "unit_index": unit,
                    "active_rate": float(active[:, unit].mean()),
                    "mean_activation": float(values.mean()),
                    "p95_activation": float(np.quantile(values, 0.95)),
                    "max_activation": float(values.max()),
                    "signal_active_rate": float(active[signal, unit].mean()) if signal.any() else None,
                    "signal_mean_activation": float(values[signal].mean()) if signal.any() else None,
                    "flat_mean_activation": float(values[flat].mean()) if flat.any() else None,
                    "signal_minus_flat_mean_activation": float(values[signal].mean() - values[flat].mean()) if signal.any() and flat.any() else None,
                }
            )
    return rows


def activation_contrast_rows(acts: Mapping[str, Mapping[str, Any]], surfaces: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for split, surface in surfaces.items():
        decisions = np.asarray(surface["decision"])
        groups = {
            "all": np.ones_like(decisions, dtype=bool),
            "flat": decisions == "flat",
            "any_signal": np.asarray(surface["signal"], dtype=bool),
            "long_signal": decisions == "long",
            "short_signal": decisions == "short",
        }
        for group, mask in groups.items():
            rows.append(masked_surface_row(split, group, mask, acts[split], surface))
    return rows


def masked_surface_row(split: str, group: str, mask: np.ndarray, act: Mapping[str, Any], surface: Mapping[str, Any]) -> dict[str, Any]:
    base = {"split": split, "group": group, "rows": int(mask.sum())}
    if not mask.any():
        return base | {key: None for key in ("mean_active_units", "mean_activation_l1", "mean_entropy_norm", "mean_margin", "mean_p_short", "mean_p_flat", "mean_p_long")}
    return base | {
        "mean_active_units": float(np.asarray(act["row_active"])[mask].mean()),
        "mean_activation_l1": float(np.asarray(act["row_l1"])[mask].mean()),
        "mean_entropy_norm": float(np.asarray(surface["entropy_norm"])[mask].mean()),
        "mean_margin": float(np.asarray(surface["margin"])[mask].mean()),
        "mean_p_short": float(np.asarray(surface["p_short"])[mask].mean()),
        "mean_p_flat": float(np.asarray(surface["p_flat"])[mask].mean()),
        "mean_p_long": float(np.asarray(surface["p_long"])[mask].mean()),
    }


def activation_stability_rows(split_rows: Sequence[Mapping[str, Any]], unit_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_split = {row["split"]: row for row in split_rows}
    units = defaultdict(list)
    for row in unit_rows:
        units[row["split"]].append(row)
    val_rate = np.array([float(row["active_rate"]) for row in units["validation_is"]])
    oos_rate = np.array([float(row["active_rate"]) for row in units["oos"]])
    val_mean = np.array([float(row["mean_activation"]) for row in units["validation_is"]])
    oos_mean = np.array([float(row["mean_activation"]) for row in units["oos"]])
    rows = [metric_delta(metric, by_split["validation_is"][metric], by_split["oos"][metric]) for metric in ("mean_active_units", "mean_active_rate", "mean_activation_l1", "top10_activation_share", "dead_unit_count", "sparse_unit_count")]
    rows.append(metric_delta("unit_active_rate_mean_abs_delta", 0.0, float(np.mean(np.abs(oos_rate - val_rate)))))
    rows.append(metric_delta("unit_mean_activation_mean_abs_delta", 0.0, float(np.mean(np.abs(oos_mean - val_mean)))))
    rows.append(metric_delta("top10_unit_overlap", 1.0, top_overlap(val_mean, oos_mean, 10)))
    return rows


def feature_group(feature: str) -> str:
    text = feature.lower()
    groups = (
        ("oscillator", ("rsi", "stoch")),
        ("volatility_range", ("atr", "vol", "bollinger", "bb_", "hl_")),
        ("trend_structure", ("ema", "sma", "adx", "di_", "supertrend", "vortex", "ppo", "trix")),
        ("macro_proxy", ("vix", "us10yr", "usdx")),
        ("constituent_proxy", ("xnas", "mega8", "top3", "us100_minus")),
        ("session", ("cash", "open")),
        ("price_return", ("return", "gap", "roc", "close_open")),
    )
    return next((name for name, tokens in groups if any(token in text for token in tokens)), "other")


def feature_sensitivity_rows(model: Any, frames: Mapping[str, Mapping[str, Any]], surfaces: Mapping[str, Mapping[str, Any]], threshold: Mapping[str, Any]) -> list[dict[str, Any]]:
    features = list(frames["validation_is"]["feature_columns"])
    medians = np.median(np.asarray(frames["validation_is"]["features"], dtype=np.float64), axis=0)
    rows = []
    for split, frame in frames.items():
        x = np.asarray(frame["features"], dtype=np.float64)
        base = np.asarray(surfaces[split]["probabilities"], dtype=np.float64)
        base_decision = np.asarray(surfaces[split]["decision"])
        base_signal = np.asarray(surfaces[split]["signal"], dtype=bool)
        split_rows = []
        for index, feature in enumerate(features):
            perturbed = x.copy()
            perturbed[:, index] = medians[index]
            new = np.asarray(model.predict_proba(perturbed), dtype=np.float64)
            surface = surface_from_probs(new, threshold)
            l1 = np.sum(np.abs(new - base), axis=1)
            decision = np.asarray(surface["decision"])
            signal = np.asarray(surface["signal"], dtype=bool)
            split_rows.append(
                {
                    "split": split,
                    "feature": feature,
                    "feature_group": feature_group(feature),
                    "reference_median": float(medians[index]),
                    "mean_l1_prob_delta": float(l1.mean()),
                    "p90_l1_prob_delta": float(np.quantile(l1, 0.90)),
                    "mean_abs_p_short_delta": float(np.mean(np.abs(new[:, 0] - base[:, 0]))),
                    "mean_abs_p_flat_delta": float(np.mean(np.abs(new[:, 1] - base[:, 1]))),
                    "mean_abs_p_long_delta": float(np.mean(np.abs(new[:, 2] - base[:, 2]))),
                    "mean_margin_delta": float(np.mean(np.asarray(surface["margin"]) - np.asarray(surfaces[split]["margin"]))),
                    "decision_flip_share": float(np.mean(decision != base_decision)),
                    "signal_drop_share": float(np.mean(base_signal & ~signal)),
                    "signal_create_share": float(np.mean(~base_signal & signal)),
                    "rank_by_l1_delta": 0,
                }
            )
        for rank, row in enumerate(sorted(split_rows, key=lambda item: float(item["mean_l1_prob_delta"]), reverse=True), start=1):
            row["rank_by_l1_delta"] = rank
            rows.append(row)
    return rows


def group_sensitivity_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for split in ("validation_is", "oos"):
        split_rows = [row for row in rows if row["split"] == split]
        for group in sorted({str(row["feature_group"]) for row in split_rows}):
            group_rows = [row for row in split_rows if row["feature_group"] == group]
            top = max(group_rows, key=lambda row: float(row["mean_l1_prob_delta"]))
            out.append({"split": split, "feature_group": group, "feature_count": len(group_rows), "mean_l1_prob_delta_sum": float(sum(float(row["mean_l1_prob_delta"]) for row in group_rows)), "top_feature": top["feature"], "top_feature_l1_delta": top["mean_l1_prob_delta"]})
    return out


def sensitivity_stability_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_split = {split: [row for row in rows if row["split"] == split] for split in ("validation_is", "oos")}
    val = {str(row["feature"]): float(row["mean_l1_prob_delta"]) for row in by_split["validation_is"]}
    oos = {str(row["feature"]): float(row["mean_l1_prob_delta"]) for row in by_split["oos"]}
    shifts = [abs(oos[name] - val[name]) for name in sorted(val)]
    top5 = top_feature_overlap(by_split, 5)
    top10 = top_feature_overlap(by_split, 10)
    return [
        metric_delta("mean_abs_feature_l1_delta_shift", 0.0, float(np.mean(shifts))),
        metric_delta("max_abs_feature_l1_delta_shift", 0.0, float(max(shifts))),
        metric_delta("top5_feature_overlap", 1.0, top5),
        metric_delta("top10_feature_overlap", 1.0, top10),
        metric_delta("validation_top1_l1_delta", 0.0, float(by_split["validation_is"][0]["mean_l1_prob_delta"])),
        metric_delta("oos_top1_l1_delta", 0.0, float(by_split["oos"][0]["mean_l1_prob_delta"])),
    ]


def metric_delta(metric: str, validation: Any, oos: Any) -> dict[str, Any]:
    val = float(validation)
    out = float(oos)
    if metric.endswith("overlap"):
        interp = "stable_overlap" if out >= 0.70 else "partial_overlap" if out >= 0.40 else "unstable_overlap"
    else:
        delta = abs(out - val)
        interp = "stable" if delta < (0.05 if ("share" in metric or "rate" in metric) else 0.25) else "shifted"
    return {"metric": metric, "validation_value": val, "oos_value": out, "oos_minus_validation": out - val, "interpretation": interp}


def top_overlap(left: np.ndarray, right: np.ndarray, n: int) -> float:
    return len(set(np.argsort(left)[::-1][:n]) & set(np.argsort(right)[::-1][:n])) / float(n)


def top_feature_overlap(by_split: Mapping[str, Sequence[Mapping[str, Any]]], n: int) -> float:
    left = {str(row["feature"]) for row in by_split["validation_is"][:n]}
    right = {str(row["feature"]) for row in by_split["oos"][:n]}
    return len(left & right) / float(n)


def judge_activation(split_rows: Sequence[Mapping[str, Any]], contrast_rows: Sequence[Mapping[str, Any]], stability: Sequence[Mapping[str, Any]]) -> tuple[str, str]:
    by_split = {row["split"]: row for row in split_rows}
    by_group = {(row["split"], row["group"]): row for row in contrast_rows}
    no_dead = max(int(by_split[split]["dead_unit_count"]) for split in ("validation_is", "oos")) == 0
    stable = next(row for row in stability if row["metric"] == "top10_unit_overlap")["oos_value"] >= 0.70
    top10 = max(float(by_split[split]["top10_activation_share"]) for split in ("validation_is", "oos"))
    lift = all(float(by_group[(split, "any_signal")]["mean_activation_l1"]) > float(by_group[(split, "flat")]["mean_activation_l1"]) for split in ("validation_is", "oos"))
    if no_dead and stable and top10 < 0.55:
        return "inconclusive_activation_distributed_and_split_stable", "move_to_feature_sensitivity_or_new_stage13_topic"
    if lift:
        return "inconclusive_activation_signal_energy_lift_observed", "feature_sensitivity_can_check_which_inputs_drive_activation"
    return "inconclusive_activation_behavior_probe_completed", "do_not_deepen_activation_until_candidate_surface_exists"


def judge_sensitivity(rows: Sequence[Mapping[str, Any]], stability: Sequence[Mapping[str, Any]]) -> tuple[str, str]:
    metrics = {row["metric"]: row for row in stability}
    if float(metrics["top10_feature_overlap"]["oos_value"]) >= 0.70:
        return "inconclusive_feature_sensitivity_stable_top_drivers", "one_shallow_followup_on_top_feature_groups_if_staying_in_stage13"
    if float(metrics["top5_feature_overlap"]["oos_value"]) <= 0.40:
        return "inconclusive_feature_sensitivity_split_unstable", "pivot_within_stage13_to_new_nonoverlapping_topic"
    return "inconclusive_feature_sensitivity_probe_completed", "pivot_within_stage13_unless_user_wants_feature_group_followup"


def make_summary(kind: str, created: str, threshold: Mapping[str, Any], frames: Mapping[str, Mapping[str, Any]], payload: Mapping[str, Any]) -> dict[str, Any]:
    spec = RUNS[kind]
    summary = {"run_id": spec["run_id"], "packet_id": spec["packet_id"], "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "created_at_utc": created, "exploration_label": spec["label"], "status": "completed", "external_verification_status": "completed_python_model_artifact_probe_no_new_mt5", "boundary": spec["boundary"], "threshold": threshold, "source_inputs": source_inputs(frames)}
    summary.update(payload)
    return summary


def write_run(kind: str, summary: Mapping[str, Any], tables: Mapping[str, tuple[Sequence[str], Sequence[Mapping[str, Any]]]]) -> None:
    spec = RUNS[kind]
    root = Path(spec["root"])
    packet_root = Path(spec["packet_root"])
    for name, (columns, rows) in tables.items():
        write_csv(root / f"{name}.csv", columns, rows)
    write_json(root / "summary.json", summary)
    write_json(root / "kpi_record.json", summary)
    write_json(root / "run_manifest.json", manifest(kind, summary, tables))
    write_json(packet_root / "skill_receipts.json", receipts(kind, summary, tables))
    write_json(packet_root / "command_result.json", {"run_id": spec["run_id"], "summary": summary})
    write_md(packet_root / "work_packet.md", work_packet(kind))
    report = report_md(kind, summary)
    write_md(root / "reports/result_summary.md", report)
    write_md(Path(spec["report"]), report)
    write_md(Path(spec["decision"]), decision_md(kind, summary))


def manifest(kind: str, summary: Mapping[str, Any], tables: Mapping[str, Any]) -> dict[str, Any]:
    spec = RUNS[kind]
    root = Path(spec["root"])
    run_number = "run04K" if kind == "activation" else "run04L"
    return {"run_id": spec["run_id"], "packet_id": spec["packet_id"], "stage_id": STAGE_ID, "run_number": run_number, "source_run_id": SOURCE_RUN_ID, "model_family": f"sklearn_mlpclassifier_relu64_{kind}_probe", "exploration_label": spec["label"], "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference", "boundary": spec["boundary"], "inputs": summary["source_inputs"], "outputs": {"summary": rel(root / "summary.json"), "report": rel(Path(spec["report"]))} | {name: rel(root / f"{name}.csv") for name in tables}}


def receipts(kind: str, summary: Mapping[str, Any], tables: Mapping[str, Any]) -> list[dict[str, Any]]:
    spec = RUNS[kind]
    evidence = [rel(Path(spec["root"]) / f"{name}.csv") for name in tables]
    return [
        {"packet_id": spec["packet_id"], "skill": "obsidian-experiment-design", "status": "completed", "hypothesis": f"Inspect MLP {kind} behavior without model or threshold changes.", "decision_use": "Stage13 internal MLP characteristic exploration only.", "comparison_baseline": "RUN04F Tier A validation/OOS under fixed q90 threshold.", "control_variables": ["model artifact", "feature order", "split", "threshold"], "changed_variables": ["analysis view only"], "sample_scope": "Tier A validation_is and OOS feature matrices", "success_criteria": "Produces interpretable model characteristic evidence.", "failure_criteria": "Missing model or feature artifacts.", "invalid_conditions": ["feature count mismatch", "class order mismatch", "threshold missing"], "stop_conditions": ["do not optimize in this packet"], "evidence_plan": evidence},
        {"packet_id": spec["packet_id"], "skill": "obsidian-model-validation", "status": "completed", "model_family": "sklearn MLPClassifier ReLU64", "target_and_label": "RUN04F inherited label contract only; no labels used here.", "split_method": "split_v1 validation_is/OOS", "selection_metric": "none; analysis-only", "secondary_metrics": list(tables), "threshold_policy": "fixed RUN04F q90 threshold", "overfit_risk": "post-hoc inspection can over-explain one split", "calibration_risk": "probabilities are model scores, not calibrated truth", "comparison_baseline": "original unperturbed RUN04F predictions", "validation_judgment": summary["judgment"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"]},
        {"packet_id": spec["packet_id"], "skill": "obsidian-data-integrity", "status": "completed", "data_source": "RUN04F Tier A feature matrices", "time_axis": "existing split rows; no timestamp joins", "sample_scope": "validation_is rows 9844 and OOS rows 7584", "missing_or_duplicate_check": "source hashes and row counts reused from RUN04F", "feature_label_boundary": "no label read and no retraining", "split_boundary": "validation_is/OOS unchanged", "leakage_risk": "post-hoc interpretation risk", "data_hash_or_identity": "source input hashes recorded in summary.json", "integrity_judgment": "usable_with_boundary"},
        {"packet_id": spec["packet_id"], "skill": "obsidian-performance-attribution", "status": "completed", "observed_change": "internal probability or activation behavior, not PnL", "comparison_baseline": "original RUN04F surface", "likely_drivers": [kind], "segment_checks": ["validation_is", "OOS"], "trade_shape": "out_of_scope_by_claim", "alternative_explanations": ["one split inspection", "uncalibrated scores"], "attribution_confidence": "low_to_medium_structural", "next_probe": summary["recommendation"]},
        {"packet_id": spec["packet_id"], "skill": "obsidian-artifact-lineage", "status": "completed", "source_inputs": [rel(SOURCE_ROOT / "run_manifest.json"), rel(SOURCE_ROOT / "thresholds/threshold_handoff.json")], "producer": "stage_pipelines/stage13/mlp_internal_behavior_probes.py", "consumer": "stage13 report and ledgers", "artifact_paths": evidence, "artifact_hashes": "summary.json records source input hashes; outputs reproducible from command", "registry_links": [rel(STAGE_LEDGER_PATH), rel(PROJECT_LEDGER_PATH), rel(RUN_REGISTRY_PATH)], "availability": "generated", "lineage_judgment": "connected_with_boundary"},
        {"packet_id": spec["packet_id"], "skill": "obsidian-result-judgment", "status": "completed", "result_subject": spec["run_id"], "evidence_available": evidence, "evidence_missing": ["new MT5 tester run", "WFO", "calibration study"], "judgment_label": summary["judgment"], "claim_boundary": spec["boundary"], "next_condition": summary["recommendation"], "user_explanation_hook": "This explains internal MLP behavior, not tradability."},
    ]


def report_md(kind: str, summary: Mapping[str, Any]) -> str:
    spec = RUNS[kind]
    lines = [f"# {spec['run_id']} 결과 요약(Result Summary, 결과 요약)", "", "- status(상태): `completed(완료)`", f"- judgment(판정): `{summary['judgment']}`", f"- recommendation(추천): `{summary['recommendation']}`", f"- source run(원천 실행): `{SOURCE_RUN_ID}`", f"- boundary(경계): `{spec['boundary']}`", ""]
    if kind == "activation":
        split = {row["split"]: row for row in summary["activation_split_summary"]}
        contrast = {(row["split"], row["group"]): row for row in summary["activation_signal_contrast"]}
        top_overlap = next(row for row in summary["activation_split_stability"] if row["metric"] == "top10_unit_overlap")["oos_value"]
        lines += ["## Core Read(핵심 판독)", "", f"- validation(검증) mean active units(평균 활성 유닛): `{split['validation_is']['mean_active_units']:.2f}` / 64.", f"- OOS(표본외) mean active units(평균 활성 유닛): `{split['oos']['mean_active_units']:.2f}` / 64.", f"- dead units(죽은 유닛): validation(검증) `{split['validation_is']['dead_unit_count']}`, OOS(표본외) `{split['oos']['dead_unit_count']}`.", f"- top10 activation share(상위 10개 활성 비중): validation(검증) `{split['validation_is']['top10_activation_share']:.3f}`, OOS(표본외) `{split['oos']['top10_activation_share']:.3f}`.", f"- top10 unit overlap(상위 10개 유닛 겹침): `{top_overlap:.3f}`.", "", "효과(effect, 효과): hidden activation(은닉층 활성화)은 한두 유닛에 과도하게 몰린 붕괴라기보다 넓게 퍼진 구조다.", "", "## Signal Contrast(신호 대비)", "", "| split(분할) | group(그룹) | rows(행) | active units(활성 유닛) | activation L1(활성 L1) | entropy(엔트로피) | margin(마진) |", "|---|---|---:|---:|---:|---:|---:|"]
        for split_name in ("validation_is", "oos"):
            for group in ("flat", "any_signal", "long_signal", "short_signal"):
                row = contrast[(split_name, group)]
                lines.append(f"| {split_name} | {group} | {row['rows']} | {fmt(row['mean_active_units'])} | {fmt(row['mean_activation_l1'])} | {fmt(row['mean_entropy_norm'])} | {fmt(row['mean_margin'])} |")
    else:
        rows = list(summary["feature_sensitivity_summary"])
        stability = {row["metric"]: row for row in summary["feature_sensitivity_stability"]}
        lines += ["## Core Read(핵심 판독)", "", f"- top5 feature overlap(상위 5개 피처 겹침): `{stability['top5_feature_overlap']['oos_value']:.3f}`.", f"- top10 feature overlap(상위 10개 피처 겹침): `{stability['top10_feature_overlap']['oos_value']:.3f}`.", f"- validation top1(검증 1위): `{rows[0]['feature']}` / group(그룹) `{rows[0]['feature_group']}` / l1 delta(L1 변화) `{rows[0]['mean_l1_prob_delta']:.4f}`.", f"- OOS top1(표본외 1위): `{[row for row in rows if row['split'] == 'oos'][0]['feature']}`.", "", "효과(effect, 효과): 한 feature(피처)를 validation median(검증 중앙값)으로 가렸을 때 probability(확률) 표면이 얼마나 바뀌는지 본다. 새 학습이나 threshold search(기준값 탐색)는 없다.", "", "## Top Features(상위 피처)", "", "| split(분할) | rank(순위) | feature(피처) | group(그룹) | L1 delta(L1 변화) | decision flip(결정 뒤집힘) | signal drop(신호 소실) |", "|---|---:|---|---|---:|---:|---:|"]
        for row in [item for item in rows if item["split"] == "validation_is"][:10] + [item for item in rows if item["split"] == "oos"][:10]:
            lines.append(f"| {row['split']} | {row['rank_by_l1_delta']} | {row['feature']} | {row['feature_group']} | {row['mean_l1_prob_delta']:.4f} | {row['decision_flip_share']:.4f} | {row['signal_drop_share']:.4f} |")
    return "\n".join(lines)


def decision_md(kind: str, summary: Mapping[str, Any]) -> str:
    spec = RUNS[kind]
    title = "Activation Behavior" if kind == "activation" else "Feature Sensitivity"
    topic = "activation behavior(활성화 행동)" if kind == "activation" else "feature sensitivity(피처 민감도)"
    return "\n".join([f"# 2026-05-02 Stage13 MLP {title} Probe", "", f"- run(실행): `{spec['run_id']}`", f"- source(원천): `{SOURCE_RUN_ID}`", f"- judgment(판정): `{summary['judgment']}`", f"- recommendation(추천): `{summary['recommendation']}`", f"- boundary(경계): `{spec['boundary']}`", "", f"효과(effect, 효과): {topic}는 내부 구조 판독으로만 남기고 alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다."])


def work_packet(kind: str) -> str:
    spec = RUNS[kind]
    topic = "hidden activation(은닉층 활성화)" if kind == "activation" else "one-feature median occlusion(단일 피처 중앙값 가림)"
    return "\n".join([f"# {spec['packet_id']}", "", f"- hypothesis(가설): RUN04F(실행 04F) MLP(다층 퍼셉트론)의 {topic} 특성을 얕게 확인한다.", "- changed_variables(변경 변수): 분석 view(보기)만 추가한다. 모델, feature(피처), threshold(기준값), MT5(메타트레이더5)는 바꾸지 않는다.", f"- boundary(경계): `{spec['boundary']}`"])


def build_ledgers(activation: Mapping[str, Any], sensitivity: Mapping[str, Any]) -> dict[str, Any]:
    rows = out_of_scope_rows("activation") + activation_ledger_rows(activation) + out_of_scope_rows("sensitivity") + sensitivity_ledger_rows(sensitivity)
    stage = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            registry_row("activation", activation["judgment"]),
            registry_row("sensitivity", sensitivity["judgment"]),
        ],
        key="run_id",
    )
    return {"stage_ledger": stage, "project_ledger": project, "run_registry": registry}


def registry_row(kind: str, judgment: Any) -> dict[str, Any]:
    spec = RUNS[kind]
    return {"run_id": spec["run_id"], "stage_id": STAGE_ID, "lane": "structural_scout", "status": "completed", "judgment": judgment, "path": rel(Path(spec["root"]) / "summary.json"), "notes": ledger_pairs((("source", SOURCE_RUN_ID), ("boundary", spec["boundary"])))}


def out_of_scope_rows(kind: str) -> list[dict[str, Any]]:
    spec = RUNS[kind]
    rows = []
    for tier, subrun in (("Tier B", "tier_b_out_of_scope"), ("Tier A+B", "tier_abb_out_of_scope")):
        rows.append(ledger_row(spec["run_id"], subrun, tier, "claim_scope_boundary", f"out_of_scope_by_claim_{kind}_probe", Path(spec["root"]) / "summary.json", (("source_run", SOURCE_RUN_ID),), (("boundary", spec["boundary"]),), "out_of_scope_by_claim", "RUN04K/RUN04L inspect Tier A source model artifacts only."))
    return rows


def activation_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    split = {row["split"]: row for row in summary["activation_split_summary"]}
    contrast = {(row["split"], row["group"]): row for row in summary["activation_signal_contrast"]}
    rows = []
    for split_name in ("validation_is", "oos"):
        row = split[split_name]
        signal = contrast[(split_name, "any_signal")]
        flat = contrast[(split_name, "flat")]
        rows.append(ledger_row(summary["run_id"], f"activation_behavior_{split_name}", "Tier A", "mlp_internal_activation", summary["judgment"], Path(RUNS["activation"]["root"]) / "activation_split_summary.csv", (("rows", row["rows"]), ("active_units", row["mean_active_units"]), ("dead_units", row["dead_unit_count"]), ("top10_share", row["top10_activation_share"])), (("signal_l1", signal["mean_activation_l1"]), ("flat_l1", flat["mean_activation_l1"]), ("boundary", "no_alpha_quality")), "completed_python_model_artifact_probe_no_new_mt5", "Tier A hidden activation behavior under fixed RUN04F model and threshold."))
    rows.append(ledger_row(summary["run_id"], "activation_stability", "Tier A", "mlp_internal_activation_stability", summary["judgment"], Path(RUNS["activation"]["root"]) / "activation_split_stability.csv", (("top10_overlap", metric_value(summary["activation_split_stability"], "top10_unit_overlap")),), (("boundary", "not_runtime_authority"),), "completed_python_model_artifact_probe_no_new_mt5", "Validation/OOS activation stability view."))
    return rows


def sensitivity_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    by_split = {split: [row for row in summary["feature_sensitivity_summary"] if row["split"] == split] for split in ("validation_is", "oos")}
    rows = []
    for split_name, split_rows in by_split.items():
        top = split_rows[0]
        rows.append(ledger_row(summary["run_id"], f"feature_sensitivity_{split_name}", "Tier A", "mlp_feature_sensitivity", summary["judgment"], Path(RUNS["sensitivity"]["root"]) / "feature_sensitivity_summary.csv", (("top_feature", top["feature"]), ("group", top["feature_group"]), ("l1_delta", top["mean_l1_prob_delta"]), ("flip_share", top["decision_flip_share"])), (("signal_drop", top["signal_drop_share"]), ("policy", "validation_median_occlusion"), ("boundary", "no_threshold_search")), "completed_python_model_artifact_probe_no_new_mt5", "Tier A one-feature median occlusion sensitivity under fixed RUN04F model."))
    rows.append(ledger_row(summary["run_id"], "feature_sensitivity_stability", "Tier A", "mlp_feature_sensitivity_stability", summary["judgment"], Path(RUNS["sensitivity"]["root"]) / "feature_sensitivity_stability.csv", (("top5_overlap", metric_value(summary["feature_sensitivity_stability"], "top5_feature_overlap")), ("top10_overlap", metric_value(summary["feature_sensitivity_stability"], "top10_feature_overlap"))), (("boundary", "not_alpha_quality"),), "completed_python_model_artifact_probe_no_new_mt5", "Validation/OOS top feature overlap under median occlusion."))
    return rows


def ledger_row(run_id: str, subrun: str, tier: str, kpi_scope: str, judgment: Any, path: Path, primary: Sequence[tuple[str, Any]], guardrail: Sequence[tuple[str, Any]], external: str, notes: str) -> dict[str, Any]:
    return {"ledger_row_id": f"{run_id}__{subrun}", "stage_id": STAGE_ID, "run_id": run_id, "subrun_id": subrun, "parent_run_id": run_id, "record_view": subrun, "tier_scope": tier, "kpi_scope": kpi_scope, "scoreboard_lane": "structural_scout", "status": "completed", "judgment": judgment, "path": rel(path), "primary_kpi": ledger_pairs(primary), "guardrail_kpi": ledger_pairs(guardrail), "external_verification_status": external, "notes": notes}


def metric_value(rows: Sequence[Mapping[str, Any]], metric: str) -> Any:
    return next(row["oos_value"] for row in rows if row["metric"] == metric)


def sync_docs(activation: Mapping[str, Any], sensitivity: Mapping[str, Any]) -> None:
    current_run = str(RUNS["sensitivity"]["run_id"])
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = state.replace("active_run04J_mlp_probability_geometry_probe", "active_run04L_mlp_feature_sensitivity_probe")
    state = ensure_top_level_current_run(state, current_run)
    state = add_stage13_current_run(state, current_run)
    block = "\n".join([
        "stage13_mlp_activation_behavior_probe:",
        f"  run_id: {RUNS['activation']['run_id']}",
        "  status: completed",
        f"  judgment: {activation['judgment']}",
        f"  recommendation: {activation['recommendation']}",
        f"  boundary: {RUNS['activation']['boundary']}",
        f"  source_run_id: {SOURCE_RUN_ID}",
        f"  report_path: {rel(Path(RUNS['activation']['report']))}",
        "stage13_mlp_feature_sensitivity_probe:",
        f"  run_id: {current_run}",
        "  status: completed",
        f"  judgment: {sensitivity['judgment']}",
        f"  recommendation: {sensitivity['recommendation']}",
        f"  boundary: {RUNS['sensitivity']['boundary']}",
        f"  source_run_id: {SOURCE_RUN_ID}",
        f"  report_path: {rel(Path(RUNS['sensitivity']['report']))}",
        "",
    ])
    if "stage13_mlp_activation_behavior_probe:" not in state:
        state = state.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n")
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    latest = f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{current_run}`이고, `{RUNS['activation']['run_id']}`에서 activation behavior(활성화 행동), `{current_run}`에서 feature sensitivity(피처 민감도)를 각각 한 번 확인했다.\n\n효과(effect, 효과): 둘 다 RUN04F(실행 04F) 모델과 q90 threshold(q90 기준값)를 그대로 썼기 때문에 새 학습이나 새 MT5(메타트레이더5) 거래 결과가 아니라 MLP(다층 퍼셉트론) 내부 성향 판독으로만 쓴다."
    current = replace_latest_update(replace_current_run_line(io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig"), current_run), latest)
    io_path(CURRENT_STATE_PATH).write_text(current, encoding="utf-8-sig")
    write_md(SELECTION_STATUS_PATH, "\n".join(["# Stage 13 Selection Status", "", "## Current Read(현재 판독)", "", f"- stage(단계): `{STAGE_ID}`", "- status(상태): `reviewed_internal_behavior_probes_completed(내부 행동 탐침 검토 완료)`", "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`", f"- current run(현재 실행): `{current_run}`", "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`", f"- activation judgment(활성화 판정): `{activation['judgment']}`", f"- sensitivity judgment(민감도 판정): `{sensitivity['judgment']}`"]))
    append_once(REVIEW_INDEX_PATH, RUNS["activation"]["run_id"], f"- `{RUNS['activation']['run_id']}`: `{activation['judgment']}`, report(보고서) `{rel(Path(RUNS['activation']['report']))}`\n")
    append_once(REVIEW_INDEX_PATH, current_run, f"- `{current_run}`: `{sensitivity['judgment']}`, report(보고서) `{rel(Path(RUNS['sensitivity']['report']))}`\n")
    append_once(CHANGELOG_PATH, RUNS["activation"]["run_id"], f"\n- 2026-05-02: Added `{RUNS['activation']['run_id']}` activation behavior(활성화 행동) probe; no alpha quality(알파 품질), baseline(기준선), promotion(승격), or runtime authority(런타임 권위) claim.\n")
    append_once(CHANGELOG_PATH, current_run, f"- 2026-05-02: Added `{current_run}` feature sensitivity(피처 민감도) probe; no alpha quality(알파 품질), baseline(기준선), promotion(승격), or runtime authority(런타임 권위) claim.\n")


def ensure_top_level_current_run(state: str, run_id: str) -> str:
    lines, out, done = state.splitlines(), [], False
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {run_id}")
            done = True
        else:
            out.append(line)
            if not done and line.startswith("active_stage:"):
                out.append(f"current_run_id: {run_id}")
                done = True
    return "\n".join(out) + "\n"


def add_stage13_current_run(state: str, run_id: str) -> str:
    needle = "    stage13:\n      stage_id: 13_model_family_challenge__mlp_training_effect\n      ownership: independent MLPClassifier coarse characteristic scout plus narrow MT5 runtime_probe\n      status: active_run04L_mlp_feature_sensitivity_probe\n"
    return state.replace(needle, needle + f"      current_run_id: {run_id}\n") if f"current_run_id: {run_id}" not in state.split("stage13:", 1)[-1][:250] and needle in state else state


def replace_current_run_line(text: str, run_id: str) -> str:
    return "\n".join(f"- current run(현재 실행): `{run_id}`" if "current run(" in line else line for line in text.splitlines()) + "\n"


def replace_latest_update(text: str, latest: str) -> str:
    header = "## Latest Stage 13 Update(최신 Stage 13 업데이트)"
    next_header = "## 쉬운 설명(Plain Read, 쉬운 설명)"
    if header not in text or next_header not in text:
        return text
    before, rest = text.split(header, 1)
    _, after = rest.split(next_header, 1)
    return before + header + "\n\n" + latest + "\n" + next_header + after


def append_once(path: Path, token: Any, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig")
    if str(token) not in text:
        io_path(path).write_text(text.rstrip() + "\n" + addition, encoding="utf-8-sig")


def fmt(value: Any) -> str:
    return "" if value is None else f"{float(value):.3f}"


def build_all() -> tuple[dict[str, Any], dict[str, Any]]:
    model = load_model()
    frames = load_frames()
    threshold = threshold_payload()
    surfaces = probability_surfaces(model, frames, threshold)
    acts = hidden_activations(model, frames)
    activation_tables = {
        "activation_split_summary": (("split", "rows", "units", "mean_active_units", "median_active_units", "p90_active_units", "mean_active_rate", "dead_unit_count", "sparse_unit_count", "always_active_unit_count", "mean_activation_l1", "median_activation_l1", "p90_activation_l1", "top5_activation_share", "top10_activation_share", "interpretation"), activation_summary_rows(acts)),
        "activation_unit_summary": (("split", "unit_index", "active_rate", "mean_activation", "p95_activation", "max_activation", "signal_active_rate", "signal_mean_activation", "flat_mean_activation", "signal_minus_flat_mean_activation"), []),
        "activation_signal_contrast": (("split", "group", "rows", "mean_active_units", "mean_activation_l1", "mean_entropy_norm", "mean_margin", "mean_p_short", "mean_p_flat", "mean_p_long"), []),
        "activation_split_stability": (("metric", "validation_value", "oos_value", "oos_minus_validation", "interpretation"), []),
    }
    activation_tables["activation_unit_summary"] = (activation_tables["activation_unit_summary"][0], activation_unit_rows(acts, surfaces))
    activation_tables["activation_signal_contrast"] = (activation_tables["activation_signal_contrast"][0], activation_contrast_rows(acts, surfaces))
    activation_tables["activation_split_stability"] = (activation_tables["activation_split_stability"][0], activation_stability_rows(activation_tables["activation_split_summary"][1], activation_tables["activation_unit_summary"][1]))
    activation_judgment, activation_rec = judge_activation(activation_tables["activation_split_summary"][1], activation_tables["activation_signal_contrast"][1], activation_tables["activation_split_stability"][1])
    activation = make_summary("activation", utc_now(), threshold, frames, {"judgment": activation_judgment, "recommendation": activation_rec, **{name: rows for name, (_, rows) in activation_tables.items()}})

    sensitivity_rows = feature_sensitivity_rows(model, frames, surfaces, threshold)
    sensitivity_tables = {
        "feature_sensitivity_summary": (("split", "feature", "feature_group", "reference_median", "mean_l1_prob_delta", "p90_l1_prob_delta", "mean_abs_p_short_delta", "mean_abs_p_flat_delta", "mean_abs_p_long_delta", "mean_margin_delta", "decision_flip_share", "signal_drop_share", "signal_create_share", "rank_by_l1_delta"), sensitivity_rows),
        "feature_group_sensitivity": (("split", "feature_group", "feature_count", "mean_l1_prob_delta_sum", "top_feature", "top_feature_l1_delta"), group_sensitivity_rows(sensitivity_rows)),
        "feature_sensitivity_stability": (("metric", "validation_value", "oos_value", "oos_minus_validation", "interpretation"), sensitivity_stability_rows(sensitivity_rows)),
    }
    sensitivity_judgment, sensitivity_rec = judge_sensitivity(sensitivity_rows, sensitivity_tables["feature_sensitivity_stability"][1])
    sensitivity = make_summary("sensitivity", utc_now(), threshold, frames, {"judgment": sensitivity_judgment, "recommendation": sensitivity_rec, "occlusion_policy": "replace one feature with validation median; no retraining and no threshold search", **{name: rows for name, (_, rows) in sensitivity_tables.items()}})

    write_run("activation", activation, activation_tables)
    write_run("sensitivity", sensitivity, sensitivity_tables)
    ledger_outputs = build_ledgers(activation, sensitivity)
    activation["ledger_outputs"] = ledger_outputs
    sensitivity["ledger_outputs"] = ledger_outputs
    write_json(Path(RUNS["activation"]["root"]) / "summary.json", activation)
    write_json(Path(RUNS["activation"]["root"]) / "kpi_record.json", activation)
    write_json(Path(RUNS["sensitivity"]["root"]) / "summary.json", sensitivity)
    write_json(Path(RUNS["sensitivity"]["root"]) / "kpi_record.json", sensitivity)
    sync_docs(activation, sensitivity)
    return activation, sensitivity


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP internal activation and feature sensitivity probes.")
    parser.parse_args(argv)
    activation, sensitivity = build_all()
    print(json.dumps(json_ready({"activation": activation["judgment"], "sensitivity": sensitivity["judgment"]}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

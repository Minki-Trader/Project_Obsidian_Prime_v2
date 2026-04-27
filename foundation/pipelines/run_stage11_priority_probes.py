from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.pipelines.materialize_training_label_split_dataset import (  # noqa: E402
    DEFAULT_FEATURES_PATH,
    DEFAULT_RAW_ROOT,
    TrainingLabelSplitSpec,
    assign_label_classes,
    assign_split,
    build_label_candidates,
    compute_train_threshold,
    load_feature_dataset,
    load_us100_close_series,
)


STAGE_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"

PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
STAGE_ALPHA_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
ARTIFACT_COLUMNS = ("artifact_id", "type", "path", "status", "notes")

PREDICTION_FILE = "tier_ab_combined_predictions.parquet"
SOURCE_RUN_DIR_NAMES = {
    "run02P": "run02P_lgbm_bear_vortex_short_v1",
    "run02Q": "run02Q_lgbm_bear_vortex_short_density_v1",
    "run02S": "run02S_lgbm_squeeze_density_v1",
}


@dataclass(frozen=True)
class ProbeSpec:
    key: str
    run_id: str
    idea_id: str
    priority: int
    title: str
    lane: str
    source_runs: tuple[str, ...]
    hypothesis: str
    claim_boundary: str


PROBES = {
    "run02T": ProbeSpec(
        key="run02T",
        run_id="run02T_label_horizon_priority_probe_v1",
        idea_id="IDEA-ST11-LABEL-HORIZON-PRIORITY",
        priority=1,
        title="label/horizon sensitivity structural probe",
        lane="alpha_label_horizon_structural_scout",
        source_runs=("run02S",),
        hypothesis=(
            "RUN02S squeeze-density may be more sensitive to label horizon than to another "
            "context gate tweak."
        ),
        claim_boundary=(
            "structural relabel probe(구조 재라벨 탐침) only(전용); "
            "no retraining(재학습 없음), no MT5 runtime claim(MT5 런타임 주장 없음)"
        ),
    ),
    "run02U": ProbeSpec(
        key="run02U",
        run_id="run02U_wfo_lite_priority_probe_v1",
        idea_id="IDEA-ST11-WFO-LITE-PRIORITY",
        priority=2,
        title="WFO-lite feasibility structural probe",
        lane="alpha_wfo_lite_structural_scout",
        source_runs=("run02S",),
        hypothesis=(
            "RUN02S should be segmented by walk-forward-like windows before spending a full "
            "WFO retrain budget."
        ),
        claim_boundary=(
            "window segmentation probe(구간 분할 탐침) only(전용); "
            "not a retrained WFO(재학습 워크포워드 최적화 아님)"
        ),
    ),
    "run02V": ProbeSpec(
        key="run02V",
        run_id="run02V_short_specific_priority_probe_v1",
        idea_id="IDEA-ST11-SHORT-SPECIFIC-PRIORITY",
        priority=3,
        title="short-specific structural probe",
        lane="alpha_short_specific_structural_scout",
        source_runs=("run02P", "run02Q"),
        hypothesis=(
            "RUN02P/RUN02Q suggest short-side density expansion alone may be the wrong fix; "
            "short labels or short-only modeling need a separate read."
        ),
        claim_boundary=(
            "existing short-surface comparison(기존 숏 표면 비교) only(전용); "
            "no new model(새 모델 없음), no new MT5 run(새 MT5 실행 없음)"
        ),
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 11 priority structural probes.")
    parser.add_argument("--run-root", default=str(RUN_ROOT))
    parser.add_argument("--features-path", default=str(DEFAULT_FEATURES_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--horizons", nargs="+", type=int, default=[6, 12, 18])
    return parser.parse_args()


def read_predictions(source_key: str) -> pd.DataFrame:
    run_dir = source_run_dir(source_key)
    path = run_dir / "predictions" / PREDICTION_FILE
    if not io_path(path).exists():
        raise FileNotFoundError(path)
    frame = pd.read_parquet(io_path(path))
    required = {
        "timestamp",
        "split",
        "label",
        "label_class",
        "tier_label",
        "decision_label",
        "decision_label_class",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise RuntimeError(f"{path} is missing columns: {sorted(missing)}")
    frame = frame.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["source_run"] = source_key
    return frame.sort_values("timestamp").reset_index(drop=True)


def source_run_dir(source_key: str) -> Path:
    return RUN_ROOT / SOURCE_RUN_DIR_NAMES[source_key]


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_markdown(path: Path, content: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(content.rstrip() + "\n", encoding="utf-8-sig")


def round_or_none(value: float | int | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    number = float(value)
    if not np.isfinite(number):
        return None
    return round(number, digits)


def safe_rate(numerator: int | float, denominator: int | float) -> float | None:
    if not denominator:
        return None
    return round_or_none(float(numerator) / float(denominator))


def label_counts(frame: pd.DataFrame, column: str = "label") -> dict[str, int]:
    counts = frame[column].astype(str).value_counts().to_dict()
    return {label: int(counts.get(label, 0)) for label in ("short", "flat", "long")}


def signal_alignment_metrics(
    frame: pd.DataFrame,
    *,
    label_class_column: str = "label_class",
    label_column: str = "label",
) -> dict[str, Any]:
    signals = frame.loc[frame["decision_label"].astype(str).ne("no_trade")].copy()
    short_signals = signals.loc[signals["decision_label"].astype(str).eq("short")]
    long_signals = signals.loc[signals["decision_label"].astype(str).eq("long")]
    if signals.empty:
        hit_count = 0
    else:
        hit_count = int(signals["decision_label_class"].astype("int64").eq(signals[label_class_column].astype("int64")).sum())
    return {
        "rows": int(len(frame)),
        "signal_count": int(len(signals)),
        "signal_rate": safe_rate(len(signals), len(frame)),
        "short_signals": int(len(short_signals)),
        "long_signals": int(len(long_signals)),
        "signal_hit_count": hit_count,
        "signal_hit_rate": safe_rate(hit_count, len(signals)),
        "signal_label_distribution": label_counts(signals, label_column) if len(signals) else {"short": 0, "flat": 0, "long": 0},
        "row_label_distribution": label_counts(frame, label_column) if len(frame) else {"short": 0, "flat": 0, "long": 0},
    }


def build_label_variants(features_path: Path, raw_root: Path, horizons: Sequence[int]) -> dict[int, dict[str, Any]]:
    feature_frame = load_feature_dataset(features_path)
    raw_close_frame = load_us100_close_series(raw_root)
    variants: dict[int, dict[str, Any]] = {}
    for horizon in horizons:
        spec = TrainingLabelSplitSpec(
            label_id=f"label_v1_fwd{horizon}_m5_logret_train_q33_3class",
            horizon_bars=int(horizon),
        )
        labelable = build_label_candidates(feature_frame, raw_close_frame, spec)
        threshold = compute_train_threshold(labelable, spec)
        labeled = assign_label_classes(labelable, threshold)
        labeled["split"] = assign_split(labeled, spec)
        labeled["label_id"] = spec.label_id
        labeled["horizon_bars"] = horizon
        labeled["horizon_minutes"] = spec.horizon_minutes
        variants[int(horizon)] = {
            "spec": {
                "label_id": spec.label_id,
                "horizon_bars": horizon,
                "horizon_minutes": spec.horizon_minutes,
                "threshold_abs_quantile": spec.threshold_abs_quantile,
                "train_threshold": threshold,
            },
            "frame": labeled[
                [
                    "timestamp",
                    "split",
                    "label",
                    "label_class",
                    "future_log_return_12",
                    "label_id",
                    "horizon_bars",
                    "horizon_minutes",
                ]
            ].rename(columns={"future_log_return_12": f"future_log_return_fwd{horizon}"}),
        }
    return variants


def split_views(frame: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    return [
        ("validation", frame.loc[frame["split"].astype(str).eq("validation")]),
        ("oos", frame.loc[frame["split"].astype(str).eq("oos")]),
        ("combined", frame.loc[frame["split"].astype(str).isin(["validation", "oos"])]),
    ]


def run_label_horizon_probe(predictions: pd.DataFrame, variants: Mapping[int, Mapping[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    variant_summaries: dict[str, Any] = {}
    base_columns = [
        "timestamp",
        "split",
        "tier_label",
        "decision_label",
        "decision_label_class",
        "label",
        "label_class",
    ]
    source = predictions[base_columns].copy()
    for horizon, payload in variants.items():
        labels = payload["frame"][["timestamp", "label", "label_class"]].copy()
        merged = source.merge(labels, on="timestamp", how="left", suffixes=("_source", "_variant"))
        merged = merged.rename(
            columns={
                "label_variant": "probe_label",
                "label_class_variant": "probe_label_class",
                "label_source": "source_label",
                "label_class_source": "source_label_class",
            }
        )
        variant_summaries[str(horizon)] = {
            "label_spec": payload["spec"],
            "label_distribution_by_split": {
                split_name: label_counts(split_frame)
                for split_name, split_frame in split_views(payload["frame"])[0:2]
            },
        }
        for split_name, split_frame in split_views(merged):
            valid = split_frame.loc[split_frame["probe_label_class"].notna()].copy()
            metrics = signal_alignment_metrics(
                valid,
                label_class_column="probe_label_class",
                label_column="probe_label",
            )
            metrics.update(
                {
                    "horizon_bars": int(horizon),
                    "split": split_name,
                    "missing_label_rows": int(len(split_frame) - len(valid)),
                }
            )
            rows.append(metrics)
    oos_rows = [row for row in rows if row["split"] == "oos"]
    best_oos = max(
        oos_rows,
        key=lambda item: (
            -1.0 if item["signal_hit_rate"] is None else float(item["signal_hit_rate"]),
            int(item["signal_count"]),
        ),
    )
    benchmark_oos = next(row for row in oos_rows if int(row["horizon_bars"]) == 12)
    if best_oos["horizon_bars"] != 12 and (best_oos["signal_hit_rate"] or 0) > (benchmark_oos["signal_hit_rate"] or 0):
        decision = "horizon_shift_worth_retraining_probe"
    else:
        decision = "no_structural_horizon_edge_over_fwd12"
    return {
        "probe": PROBES["run02T"].__dict__,
        "source_run_id": "run02S_lgbm_squeeze_density_v1",
        "metrics": rows,
        "variant_summaries": variant_summaries,
        "best_oos": best_oos,
        "benchmark_oos_fwd12": benchmark_oos,
        "decision": decision,
    }


def quarter_id(value: pd.Timestamp) -> str:
    stamp = pd.Timestamp(value)
    quarter = int((stamp.month - 1) // 3 + 1)
    return f"{stamp.year}Q{quarter}"


def run_wfo_lite_probe(predictions: pd.DataFrame) -> dict[str, Any]:
    frame = predictions.copy()
    frame["window_id"] = frame["timestamp"].map(quarter_id)
    rows: list[dict[str, Any]] = []
    for split_name in ("validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split_name)]
        for window_id in sorted(split_frame["window_id"].dropna().unique()):
            window_frame = split_frame.loc[split_frame["window_id"].eq(window_id)]
            metrics = signal_alignment_metrics(window_frame)
            metrics.update(
                {
                    "split": split_name,
                    "window_id": str(window_id),
                    "first_timestamp": window_frame["timestamp"].min(),
                    "last_timestamp": window_frame["timestamp"].max(),
                }
            )
            rows.append(metrics)
    oos_rows = [row for row in rows if row["split"] == "oos"]
    oos_signal_total = int(sum(row["signal_count"] for row in oos_rows))
    nonzero_oos_windows = int(sum(1 for row in oos_rows if row["signal_count"] > 0))
    max_signal_share = (
        max((row["signal_count"] for row in oos_rows), default=0) / oos_signal_total
        if oos_signal_total
        else None
    )
    if oos_signal_total < 20 or nonzero_oos_windows < 2:
        decision = "wfo_lite_density_insufficient_for_full_wfo"
    else:
        decision = "wfo_lite_worth_retraining_probe"
    return {
        "probe": PROBES["run02U"].__dict__,
        "source_run_id": "run02S_lgbm_squeeze_density_v1",
        "metrics": rows,
        "summary": {
            "oos_window_count": int(len(oos_rows)),
            "nonzero_oos_windows": nonzero_oos_windows,
            "oos_signal_total": oos_signal_total,
            "max_oos_window_signal_share": round_or_none(max_signal_share),
        },
        "decision": decision,
    }


def short_metrics_for_source(source_key: str, predictions: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    short_predictions = predictions.loc[predictions["decision_label"].astype(str).eq("short")].copy()
    for split_name, split_frame in split_views(predictions):
        if split_name == "combined":
            split_shorts = short_predictions.loc[short_predictions["split"].astype(str).isin(["validation", "oos"])]
        else:
            split_shorts = short_predictions.loc[short_predictions["split"].astype(str).eq(split_name)]
        hit_count = int(split_shorts["label_class"].astype("int64").eq(0).sum()) if len(split_shorts) else 0
        false_count = int(len(split_shorts) - hit_count)
        rows.append(
            {
                "source_run": source_key,
                "source_run_id": source_run_dir(source_key).name,
                "split": split_name,
                "rows": int(len(split_frame)),
                "short_signal_count": int(len(split_shorts)),
                "short_hit_count": hit_count,
                "short_hit_rate": safe_rate(hit_count, len(split_shorts)),
                "false_short_count": false_count,
                "false_short_rate": safe_rate(false_count, len(split_shorts)),
                "short_signal_label_distribution": label_counts(split_shorts) if len(split_shorts) else {"short": 0, "flat": 0, "long": 0},
            }
        )
    return rows


def run_short_specific_probe(predictions_by_source: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for source_key in ("run02P", "run02Q"):
        rows.extend(short_metrics_for_source(source_key, predictions_by_source[source_key]))
    p_oos = next(row for row in rows if row["source_run"] == "run02P" and row["split"] == "oos")
    q_oos = next(row for row in rows if row["source_run"] == "run02Q" and row["split"] == "oos")
    density_multiplier = (
        float(q_oos["short_signal_count"]) / float(p_oos["short_signal_count"])
        if p_oos["short_signal_count"]
        else None
    )
    hit_delta = (
        float(q_oos["short_hit_rate"]) - float(p_oos["short_hit_rate"])
        if p_oos["short_hit_rate"] is not None and q_oos["short_hit_rate"] is not None
        else None
    )
    if density_multiplier and density_multiplier > 1.2 and hit_delta is not None and hit_delta < 0:
        decision = "density_expansion_worsens_short_alignment"
    else:
        decision = "short_specific_probe_inconclusive"
    return {
        "probe": PROBES["run02V"].__dict__,
        "source_run_ids": [source_run_dir(key).name for key in ("run02P", "run02Q")],
        "metrics": rows,
        "summary": {
            "run02P_oos_short_hit_rate": p_oos["short_hit_rate"],
            "run02Q_oos_short_hit_rate": q_oos["short_hit_rate"],
            "run02P_oos_short_signals": p_oos["short_signal_count"],
            "run02Q_oos_short_signals": q_oos["short_signal_count"],
            "density_signal_multiplier": round_or_none(density_multiplier),
            "density_hit_rate_delta": round_or_none(hit_delta),
        },
        "decision": decision,
    }


def row_for_metric(metrics: Sequence[Mapping[str, Any]], **selectors: Any) -> Mapping[str, Any]:
    for row in metrics:
        if all(row.get(key) == value for key, value in selectors.items()):
            return row
    raise KeyError(selectors)


def render_run_summary(spec: ProbeSpec, record: Mapping[str, Any]) -> str:
    if spec.key == "run02T":
        best = record["best_oos"]
        benchmark = record["benchmark_oos_fwd12"]
        return f"""# {spec.run_id}

## Scope

Priority(우선순위) {spec.priority}: label/horizon sensitivity(라벨/예측수평선 민감도).

- Source(원천): `RUN02S`
- Boundary(경계): {spec.claim_boundary}

## Result

| Metric(지표) | Value(값) |
|---|---:|
| Best OOS horizon(최고 OOS 예측수평선) | {best["horizon_bars"]} |
| Best OOS signal hit rate(신호 적중률) | {best["signal_hit_rate"]} |
| fwd12 OOS signal hit rate(fwd12 OOS 신호 적중률) | {benchmark["signal_hit_rate"]} |
| Best OOS signal count(신호 수) | {best["signal_count"]} |

Judgment(판정): `{record["decision"]}`.
"""
    if spec.key == "run02U":
        summary = record["summary"]
        return f"""# {spec.run_id}

## Scope

Priority(우선순위) {spec.priority}: WFO-lite feasibility(가벼운 워크포워드 가능성).

- Source(원천): `RUN02S`
- Boundary(경계): {spec.claim_boundary}

## Result

| Metric(지표) | Value(값) |
|---|---:|
| OOS windows(OOS 구간) | {summary["oos_window_count"]} |
| Nonzero OOS windows(신호 있는 OOS 구간) | {summary["nonzero_oos_windows"]} |
| OOS signals(OOS 신호) | {summary["oos_signal_total"]} |
| Max window signal share(최대 구간 신호 비중) | {summary["max_oos_window_signal_share"]} |

Judgment(판정): `{record["decision"]}`.
"""
    summary = record["summary"]
    return f"""# {spec.run_id}

## Scope

Priority(우선순위) {spec.priority}: short-specific structural read(숏 전용 구조 판독).

- Source(원천): `RUN02P`, `RUN02Q`
- Boundary(경계): {spec.claim_boundary}

## Result

| Metric(지표) | Value(값) |
|---|---:|
| RUN02P OOS short hit rate(RUN02P OOS 숏 적중률) | {summary["run02P_oos_short_hit_rate"]} |
| RUN02Q OOS short hit rate(RUN02Q OOS 숏 적중률) | {summary["run02Q_oos_short_hit_rate"]} |
| Density multiplier(밀도 배수) | {summary["density_signal_multiplier"]} |
| Hit-rate delta(적중률 차이) | {summary["density_hit_rate_delta"]} |

Judgment(판정): `{record["decision"]}`.
"""


def write_run_artifacts(spec: ProbeSpec, record: Mapping[str, Any]) -> dict[str, Path]:
    run_dir = RUN_ROOT / spec.run_id
    manifest_path = run_dir / "run_manifest.json"
    kpi_path = run_dir / "kpi_record.json"
    summary_path = run_dir / "reports" / "result_summary.md"
    manifest = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "run_number": spec.key,
        "exploration_label": f"stage11_Priority__{spec.key}",
        "idea_id": spec.idea_id,
        "priority": spec.priority,
        "lane": spec.lane,
        "hypothesis": spec.hypothesis,
        "claim_boundary": spec.claim_boundary,
        "source_runs": list(spec.source_runs),
        "generated_by": Path(__file__).as_posix(),
        "external_verification_status": "not_applicable_python_structural_only",
    }
    write_json(manifest_path, manifest)
    write_json(kpi_path, record)
    write_markdown(summary_path, render_run_summary(spec, record))
    return {"manifest": manifest_path, "kpi": kpi_path, "summary": summary_path}


def primary_kpi_for_record(spec: ProbeSpec, record: Mapping[str, Any]) -> str:
    if spec.key == "run02T":
        best = record["best_oos"]
        benchmark = record["benchmark_oos_fwd12"]
        return ledger_pairs(
            [
                ("best_oos_horizon", best["horizon_bars"]),
                ("best_oos_signal_hit_rate", best["signal_hit_rate"]),
                ("fwd12_oos_signal_hit_rate", benchmark["signal_hit_rate"]),
                ("best_oos_signal_count", best["signal_count"]),
            ]
        )
    if spec.key == "run02U":
        summary = record["summary"]
        return ledger_pairs(
            [
                ("oos_window_count", summary["oos_window_count"]),
                ("nonzero_oos_windows", summary["nonzero_oos_windows"]),
                ("oos_signal_total", summary["oos_signal_total"]),
                ("max_oos_window_signal_share", summary["max_oos_window_signal_share"]),
            ]
        )
    summary = record["summary"]
    return ledger_pairs(
        [
            ("run02P_oos_short_hit_rate", summary["run02P_oos_short_hit_rate"]),
            ("run02Q_oos_short_hit_rate", summary["run02Q_oos_short_hit_rate"]),
            ("density_signal_multiplier", summary["density_signal_multiplier"]),
            ("density_hit_rate_delta", summary["density_hit_rate_delta"]),
        ]
    )


def guardrail_kpi_for_record(spec: ProbeSpec, record: Mapping[str, Any]) -> str:
    if spec.key == "run02T":
        metrics = record["metrics"]
        combined_fwd12 = row_for_metric(metrics, horizon_bars=12, split="combined")
        return ledger_pairs(
            [
                ("combined_signal_count", combined_fwd12["signal_count"]),
                ("combined_missing_label_rows", combined_fwd12["missing_label_rows"]),
                ("claim_boundary", spec.claim_boundary),
            ]
        )
    if spec.key == "run02U":
        summary = record["summary"]
        return ledger_pairs(
            [
                ("wfo_status", "segmentation_only"),
                ("oos_signal_total", summary["oos_signal_total"]),
                ("claim_boundary", spec.claim_boundary),
            ]
        )
    summary = record["summary"]
    return ledger_pairs(
        [
            ("run02P_oos_short_signals", summary["run02P_oos_short_signals"]),
            ("run02Q_oos_short_signals", summary["run02Q_oos_short_signals"]),
            ("claim_boundary", spec.claim_boundary),
        ]
    )


def register_runs(records: Mapping[str, Mapping[str, Any]], artifact_paths: Mapping[str, Mapping[str, Path]]) -> None:
    run_rows = []
    ledger_rows = []
    artifact_rows = []
    for key, record in records.items():
        spec = PROBES[key]
        kpi_path = artifact_paths[key]["kpi"]
        run_rows.append(
            {
                "run_id": spec.run_id,
                "stage_id": STAGE_ID,
                "lane": spec.lane,
                "status": "reviewed",
                "judgment": record["decision"],
                "path": (RUN_ROOT / spec.run_id).as_posix(),
                "notes": f"Priority {spec.priority} structural probe; {spec.claim_boundary}.",
            }
        )
        ledger_rows.append(
            {
                "ledger_row_id": f"{spec.run_id}__python_structural_probe",
                "stage_id": STAGE_ID,
                "run_id": spec.run_id,
                "subrun_id": "python_structural_probe",
                "parent_run_id": ";".join(source_run_dir(source_key).name for source_key in spec.source_runs),
                "record_view": spec.title,
                "tier_scope": "Tier A+B",
                "kpi_scope": "structural_alignment",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": record["decision"],
                "path": kpi_path.as_posix(),
                "primary_kpi": primary_kpi_for_record(spec, record),
                "guardrail_kpi": guardrail_kpi_for_record(spec, record),
                "external_verification_status": "not_applicable_python_structural_only",
                "notes": f"Priority {spec.priority}; {spec.claim_boundary}.",
            }
        )
        for artifact_type, path in artifact_paths[key].items():
            artifact_rows.append(
                {
                    "artifact_id": f"{spec.run_id}__{artifact_type}",
                    "type": artifact_type,
                    "path": path.as_posix(),
                    "status": "active",
                    "notes": (
                        f"Stage 11 priority structural probe artifact; "
                        f"sha256_lf={sha256_file_lf_normalized(path)}"
                    ),
                }
            )
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def render_packet(records: Mapping[str, Mapping[str, Any]]) -> str:
    label = records["run02T"]
    wfo = records["run02U"]
    short = records["run02V"]
    label_best = label["best_oos"]
    label_benchmark = label["benchmark_oos_fwd12"]
    wfo_summary = wfo["summary"]
    short_summary = short["summary"]
    return f"""# RUN02T~RUN02V Priority Probe Packet

## Scope

`run02T_run02V_priority_probe_packet_v1`은 Stage 11(11단계)의 다음 우선순위 1/2/3을 구조 탐침(structural probe, 구조 탐침)으로 정리한다.

- Priority 1(우선순위 1): label/horizon sensitivity(라벨/예측수평선 민감도)
- Priority 2(우선순위 2): WFO-lite(가벼운 워크포워드 최적화) 가능성
- Priority 3(우선순위 3): short-specific(숏 전용) 구조 판독

## Result Table

| Run(실행) | Question(질문) | Primary read(핵심 판독) | Judgment(판정) |
|---|---|---|---|
| RUN02T | label/horizon(라벨/예측수평선) | best OOS horizon `{label_best["horizon_bars"]}`, hit `{label_best["signal_hit_rate"]}` vs fwd12 `{label_benchmark["signal_hit_rate"]}` | `{label["decision"]}` |
| RUN02U | WFO-lite(WFO-lite) | OOS signals `{wfo_summary["oos_signal_total"]}`, nonzero windows `{wfo_summary["nonzero_oos_windows"]}` | `{wfo["decision"]}` |
| RUN02V | short-specific(숏 전용) | P hit `{short_summary["run02P_oos_short_hit_rate"]}`, Q hit `{short_summary["run02Q_oos_short_hit_rate"]}`, density x `{short_summary["density_signal_multiplier"]}` | `{short["decision"]}` |

## Boundary

이 packet(묶음)은 Python structural probe(파이썬 구조 탐침)이다. 재학습(retraining, 재학습), MT5 runtime(런타임), operating promotion(운영 승격)을 주장하지 않는다.

Effect(효과): 다음 작업에서 전체 WFO(워크포워드 최적화)를 바로 태우기 전에, 비용 대비 정보량이 큰 방향을 먼저 고른다.
"""


def render_plan_doc() -> str:
    return """# RUN02T~RUN02V Priority Probe Plan

## Priority 1

label/horizon sensitivity(라벨/예측수평선 민감도)를 `RUN02T`로 본다. 기존 `RUN02S` decision surface(결정 표면)를 fwd6/fwd12/fwd18 label(라벨)로 다시 맞춰 본다.

Effect(효과): 라벨 길이만 바꿔도 신호 정렬이 달라지는지 확인해서, 재학습(retraining, 재학습) 후보를 좁힌다.

## Priority 2

WFO-lite(가벼운 워크포워드 최적화)를 `RUN02U`로 본다. 기존 `RUN02S`를 분기별 window(구간)로 나누어 신호 밀도와 집중도를 본다.

Effect(효과): full WFO(전체 워크포워드 최적화)를 돌릴 만큼 구간별 표본이 있는지 먼저 판단한다.

## Priority 3

short-specific(숏 전용) 구조 판독을 `RUN02V`로 본다. `RUN02P` strict(엄격)와 `RUN02Q` density(밀도 확장)를 비교한다.

Effect(효과): 숏 성능 문제가 단순 신호 부족인지, 라벨/모델 분리 필요성인지 구분한다.

## Boundary

이 계획은 structural probe(구조 탐침)이다. MT5(메타트레이더5) runtime claim(런타임 주장)이나 promotion claim(승격 주장)을 만들지 않는다.
"""


def register_packet_artifacts(plan_path: Path, packet_path: Path) -> None:
    rows = []
    for artifact_id, artifact_type, path in (
        ("run02T_run02V_priority_probe_plan_v1", "plan", plan_path),
        ("run02T_run02V_priority_probe_packet_v1", "review_packet", packet_path),
    ):
        rows.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": path.as_posix(),
                "status": "active",
                "notes": (
                    "Stage 11 priority structural probe artifact; "
                    f"sha256_lf={sha256_file_lf_normalized(path)}"
                ),
            }
        )
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def main() -> None:
    args = parse_args()
    global RUN_ROOT
    RUN_ROOT = Path(args.run_root)
    predictions_by_source = {key: read_predictions(key) for key in ("run02P", "run02Q", "run02S")}
    label_variants = build_label_variants(Path(args.features_path), Path(args.raw_root), args.horizons)
    records = {
        "run02T": run_label_horizon_probe(predictions_by_source["run02S"], label_variants),
        "run02U": run_wfo_lite_probe(predictions_by_source["run02S"]),
        "run02V": run_short_specific_probe(predictions_by_source),
    }
    artifact_paths = {
        key: write_run_artifacts(PROBES[key], record)
        for key, record in records.items()
    }
    register_runs(records, artifact_paths)
    plan_path = SPEC_ROOT / "run02T_run02V_priority_probe_plan.md"
    packet_path = REVIEW_ROOT / "run02T_run02V_priority_probe_packet.md"
    write_markdown(plan_path, render_plan_doc())
    write_markdown(packet_path, render_packet(records))
    register_packet_artifacts(plan_path, packet_path)
    print(json.dumps(json_ready({key: record["decision"] for key, record in records.items()}), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

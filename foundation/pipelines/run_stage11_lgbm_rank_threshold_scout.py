from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.pipelines import run_stage10_logreg_mt5_scout as scout  # noqa: E402
from foundation.pipelines import run_stage11_lgbm_training_method_scout as run02a  # noqa: E402
from foundation.pipelines import run_stage11_lgbm_divergent_scouts as divergent  # noqa: E402


STAGE_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
RUN_NUMBER = "run02B"
RUN_ID = "run02B_lgbm_rank_threshold_scout_v1"
EXPLORATION_LABEL = "stage11_Threshold__LGBMRankTarget"
MODEL_FAMILY = "lightgbm_lgbmclassifier_multiclass"
SOURCE_RUN_ID = "run02A_lgbm_training_method_scout_v1"
DEFAULT_SOURCE_ROOT = Path("stages") / STAGE_ID / "02_runs" / SOURCE_RUN_ID
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
RUN01Y_REFERENCE = run02a.RUN01Y_REFERENCE
DECISION_SURFACE_ID = "run02B_lgbm_rank_target_threshold_surface_hold9_slice200_220"
PROBABILITY_COLUMNS = ("p_short", "p_flat", "p_long")
DECISION_COLUMNS = (
    "threshold_id",
    "p_short",
    "p_flat",
    "p_long",
    "decision_label_class",
    "decision_label",
    "decision_probability",
    "decision_margin",
    "short_margin",
    "long_margin",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 11 LGBM rank-target threshold scout.")
    parser.add_argument("--source-run-root", default=str(DEFAULT_SOURCE_ROOT))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--run-number", default=RUN_NUMBER)
    parser.add_argument("--exploration-label", default=EXPLORATION_LABEL)
    parser.add_argument("--source-run-id", default=SOURCE_RUN_ID)
    parser.add_argument("--decision-surface-id", default=DECISION_SURFACE_ID)
    parser.add_argument("--selection-policy", default="lgbm_validation_quantile_rank_target_not_run01_absolute_grid")
    parser.add_argument("--run-registry-lane", default="alpha_threshold_scout")
    parser.add_argument("--judgment-prefix", default="lgbm_rank_threshold")
    parser.add_argument(
        "--hypothesis",
        default=(
            "LightGBM needs distribution-aware rank-target thresholds instead of the run01Y absolute LogReg "
            "threshold surface."
        ),
    )
    parser.add_argument("--max-hold-bars", type=int, default=9)
    parser.add_argument("--session-slice-id", default="mid_second_overlap_200_220")
    parser.add_argument("--tier-a-quantile", type=float, default=0.96)
    parser.add_argument("--tier-a-min-margin", type=float, default=0.12)
    parser.add_argument("--tier-b-quantile", type=float, default=0.96)
    parser.add_argument("--tier-b-min-margin", type=float, default=0.08)
    parser.add_argument("--invert-decisions", action="store_true")
    parser.add_argument("--context-gate", default=None)
    parser.add_argument("--disable-routed-fallback", action="store_true")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


def _io_path(path: Path) -> Path:
    return scout._io_path(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout.write_json(path, payload)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(_io_path(path).read_text(encoding="utf-8"))


def copy_artifact(source: Path, destination: Path) -> dict[str, Any]:
    _io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(_io_path(source), _io_path(destination))
    return {
        "source": source.as_posix(),
        "path": destination.as_posix(),
        "sha256": scout.sha256_file(destination),
    }


def threshold_id(prefix: str, short_threshold: float, long_threshold: float, min_margin: float, quantile: float) -> str:
    return (
        f"{prefix}_rankq{quantile:.3f}_short{short_threshold:.3f}"
        f"_long{long_threshold:.3f}_margin{min_margin:.3f}"
    )


def quantile_rule(
    frame: pd.DataFrame,
    *,
    split_name: str,
    quantile: float,
    min_margin: float,
    prefix: str,
) -> scout.ThresholdRule:
    split = frame.loc[frame["split"].astype(str).eq(split_name)]
    if split.empty:
        raise RuntimeError(f"Cannot select rank threshold from empty split: {split_name}")
    short_threshold = float(split["p_short"].quantile(quantile))
    long_threshold = float(split["p_long"].quantile(quantile))
    return scout.ThresholdRule(
        threshold_id=threshold_id(prefix, short_threshold, long_threshold, min_margin, quantile),
        short_threshold=short_threshold,
        long_threshold=long_threshold,
        min_margin=float(min_margin),
    )


def invert_signal_decisions(decisions: pd.DataFrame) -> pd.DataFrame:
    inverted = decisions.copy()
    short_mask = inverted["decision_label_class"].astype("int64").eq(0)
    long_mask = inverted["decision_label_class"].astype("int64").eq(2)
    inverted.loc[short_mask, "decision_label_class"] = 2
    inverted.loc[short_mask, "decision_label"] = "long"
    inverted.loc[long_mask, "decision_label_class"] = 0
    inverted.loc[long_mask, "decision_label"] = "short"
    inverted.loc[short_mask | long_mask, "threshold_id"] = inverted.loc[short_mask | long_mask, "threshold_id"].astype(str) + "_inverse"
    return inverted


def recompute_predictions(frame: pd.DataFrame, rule: scout.ThresholdRule, *, invert_decisions: bool = False) -> pd.DataFrame:
    identity = frame.loc[:, [column for column in frame.columns if column not in DECISION_COLUMNS]].reset_index(drop=True)
    decisions = scout.apply_threshold_rule(frame.loc[:, list(PROBABILITY_COLUMNS)].to_numpy(dtype="float64"), rule)
    if invert_decisions:
        decisions = invert_signal_decisions(decisions)
    return pd.concat([identity, decisions], axis=1)


def signal_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    signals = frame.loc[frame["decision_label"].astype(str).ne(scout.DECISION_LABEL_NO_TRADE)]
    payload: dict[str, Any] = {
        "rows": int(len(frame)),
        "signal_count": int(len(signals)),
        "short_count": int((signals["decision_label_class"].astype("int64") == 0).sum()) if not signals.empty else 0,
        "long_count": int((signals["decision_label_class"].astype("int64") == 2).sum()) if not signals.empty else 0,
        "signal_coverage": float(len(signals) / len(frame)) if len(frame) else 0.0,
    }
    if not signals.empty and "label_class" in frame.columns:
        labels = frame.loc[signals.index, "label_class"].astype("int64").to_numpy()
        decisions = signals["decision_label_class"].astype("int64").to_numpy()
        payload["directional_hit_rate"] = float((labels == decisions).mean())
    else:
        payload["directional_hit_rate"] = None
    return payload


def allowed_timestamps_from_feature_matrix(path: Path, context_gate: str | None) -> set[str] | None:
    if context_gate is None:
        return None
    source = pd.read_csv(_io_path(path))
    mask = divergent.context_gate_mask(source, context_gate)
    return set(divergent.timestamp_key(source.loc[mask, "timestamp_utc"]))


def copy_or_filter_feature_matrix(source: Path, destination: Path, context_gate: str | None) -> dict[str, Any]:
    if context_gate is None:
        return copy_artifact(source, destination)
    payload = dict(
        divergent.write_matrix_for_variant(
            source_path=source,
            destination_path=destination,
            context_gate=context_gate,
        )
    )
    allowed_timestamps = payload.pop("allowed_timestamps", set())
    payload["allowed_timestamp_count"] = len(allowed_timestamps)
    return payload


def quantile_sweep(
    frame: pd.DataFrame,
    *,
    tier_name: str,
    quantiles: Sequence[float],
    margins: Sequence[float],
    invert_decisions: bool = False,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    validation = frame.loc[frame["split"].astype(str).eq("validation")]
    oos = frame.loc[frame["split"].astype(str).eq("oos")]
    for quantile in quantiles:
        for margin in margins:
            rule = quantile_rule(
                frame,
                split_name="validation",
                quantile=float(quantile),
                min_margin=float(margin),
                prefix=tier_name.lower().replace(" ", "_"),
            )
            validation_pred = recompute_predictions(validation, rule, invert_decisions=invert_decisions)
            oos_pred = recompute_predictions(oos, rule, invert_decisions=invert_decisions)
            validation_metrics = signal_metrics(validation_pred)
            oos_metrics = signal_metrics(oos_pred)
            rows.append(
                {
                    "tier": tier_name,
                    "threshold_id": rule.threshold_id,
                    "quantile": float(quantile),
                    "short_threshold": rule.short_threshold,
                    "long_threshold": rule.long_threshold,
                    "min_margin": rule.min_margin,
                    "invert_decisions": bool(invert_decisions),
                    "validation_signal_count": validation_metrics["signal_count"],
                    "validation_signal_coverage": validation_metrics["signal_coverage"],
                    "validation_directional_hit_rate": validation_metrics["directional_hit_rate"],
                    "validation_short_count": validation_metrics["short_count"],
                    "validation_long_count": validation_metrics["long_count"],
                    "oos_signal_count": oos_metrics["signal_count"],
                    "oos_signal_coverage": oos_metrics["signal_coverage"],
                    "oos_directional_hit_rate": oos_metrics["directional_hit_rate"],
                    "oos_short_count": oos_metrics["short_count"],
                    "oos_long_count": oos_metrics["long_count"],
                }
            )
    return pd.DataFrame(rows)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    columns = list(rows[0].keys()) if rows else []
    with _io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return {"path": path.as_posix(), "sha256": scout.sha256_file_lf_normalized(path), "rows": len(rows)}


def write_result_summary(
    *,
    path: Path,
    run_id: str,
    run_number: str,
    source_run_id: str,
    decision_direction_mode: str,
    context_gate: str | None,
    selected_threshold_id: str,
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    external_status: str,
    routing_mode: str,
) -> None:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}

    def mt5_metric(view: str, key: str) -> Any:
        return by_view.get(view, {}).get(key)

    python_by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}

    def py_metric(view: str, key: str) -> Any:
        return python_by_view.get(view, {}).get(key)

    routing_boundary = (
        "Tier A-only MT5 runtime_probe(Tier A 단독 MT5 런타임 탐침)"
        if routing_mode == scout.ROUTING_MODE_A_ONLY
        else "routed MT5 runtime_probe(라우팅 MT5 런타임 탐침)"
    )
    lines = [
        f"# Stage 11 {run_number.upper()} LGBM Rank-Target Threshold Scout",
        "",
        f"- run_id(실행 ID): `{run_id}`",
        f"- source run(원천 실행): `{source_run_id}`",
        f"- decision direction(판정 방향): `{decision_direction_mode}`",
        f"- context gate(문맥 제한): `{context_gate or 'none'}`",
        f"- model family(모델 계열): `{MODEL_FAMILY}`",
        f"- selected threshold(선택 임계값): `{selected_threshold_id}`",
        f"- threshold method(임계값 방식): `rank-target quantile(순위 기반 분위수)`",
        f"- external verification status(외부 검증 상태): `{external_status}`",
        "",
        "## Python Signal Views(파이썬 신호 보기)",
        "",
        "| view(보기) | rows(행) | signal count(신호 수) | coverage(커버리지) | short/long(숏/롱) |",
        "|---|---:|---:|---:|---:|",
        (
            f"| Tier A separate(Tier A 분리) | `{py_metric('tier_a_separate', 'rows')}` | "
            f"`{py_metric('tier_a_separate', 'signal_count')}` | "
            f"`{py_metric('tier_a_separate', 'signal_coverage')}` | "
            f"`{py_metric('tier_a_separate', 'short_count')}/{py_metric('tier_a_separate', 'long_count')}` |"
        ),
        (
            f"| Tier B separate(Tier B 분리) | `{py_metric('tier_b_separate', 'rows')}` | "
            f"`{py_metric('tier_b_separate', 'signal_count')}` | "
            f"`{py_metric('tier_b_separate', 'signal_coverage')}` | "
            f"`{py_metric('tier_b_separate', 'short_count')}/{py_metric('tier_b_separate', 'long_count')}` |"
        ),
        (
            f"| Tier A+B combined(Tier A+B 합산) | `{py_metric('tier_ab_combined', 'rows')}` | "
            f"`{py_metric('tier_ab_combined', 'signal_count')}` | "
            f"`{py_metric('tier_ab_combined', 'signal_coverage')}` | "
            f"`{py_metric('tier_ab_combined', 'short_count')}/{py_metric('tier_ab_combined', 'long_count')}` |"
        ),
        "",
        "## MT5 Routed Probe(MT5 라우팅 탐침)",
        "",
        f"- validation routed net/PF(검증 라우팅 순수익/수익 팩터): `{mt5_metric('mt5_routed_total_validation_is', 'net_profit')}` / `{mt5_metric('mt5_routed_total_validation_is', 'profit_factor')}`",
        f"- OOS routed net/PF(표본외 라우팅 순수익/수익 팩터): `{mt5_metric('mt5_routed_total_oos', 'net_profit')}` / `{mt5_metric('mt5_routed_total_oos', 'profit_factor')}`",
        f"- validation Tier B fallback used(검증 Tier B 대체 사용): `{mt5_metric('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
        f"- OOS Tier B fallback used(표본외 Tier B 대체 사용): `{mt5_metric('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
        "",
        "## Boundary(경계)",
        "",
        f"이 실행(run, 실행)은 LGBM-specific threshold scout(LGBM 전용 임계값 탐색)와 {routing_boundary}다.",
        "효과(effect, 효과)는 RUN01(실행 01)처럼 같은 absolute grid(절대값 격자)를 반복하지 않고, LGBM(라이트GBM) 확률 분포의 상위 순위 신호만 시험하는 것이다.",
        "",
        "이 실행은 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
        "",
    ]
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text("\n".join(lines), encoding="utf-8-sig")


def materialize_run_registry_row(
    *,
    run_id: str,
    run_output_root: Path,
    route_coverage: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    external_verification_status: str,
    decision_surface_id: str,
    lane: str,
    judgment_prefix: str,
    invert_decisions: bool,
    context_gate: str | None,
    session_slice_id: str,
    routing_mode: str,
) -> dict[str, Any]:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}
    by_mt5_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}
    validation = by_mt5_view.get("mt5_routed_total_validation_is", {})
    oos = by_mt5_view.get("mt5_routed_total_oos", {})
    notes = scout._ledger_pairs(
        (
            ("model_family", MODEL_FAMILY),
            ("comparison_reference", RUN01Y_REFERENCE["run_id"]),
            ("decision_surface", decision_surface_id),
            ("threshold_method", "rank_target_quantile"),
            ("decision_direction_mode", "inverse" if invert_decisions else "normal"),
            ("context_gate", context_gate or "none"),
            ("routed_attempt_policy", routing_mode),
            ("session_slice", session_slice_id),
            ("max_hold_bars", RUN01Y_REFERENCE["max_hold_bars"]),
            ("tier_b_fallback_rows", route_coverage.get("tier_b_fallback_rows")),
            ("no_tier_labelable_rows", route_coverage.get("no_tier_labelable_rows")),
            ("tier_a_signal_coverage", by_view.get("tier_a_separate", {}).get("signal_coverage")),
            ("tier_b_signal_coverage", by_view.get("tier_b_separate", {}).get("signal_coverage")),
            ("combined_signal_coverage", by_view.get("tier_ab_combined", {}).get("signal_coverage")),
            ("validation_net_profit", validation.get("net_profit")),
            ("validation_pf", validation.get("profit_factor")),
            ("validation_b_fallback_used", validation.get("tier_b_fallback_used_count")),
            ("oos_net_profit", oos.get("net_profit")),
            ("oos_pf", oos.get("profit_factor")),
            ("oos_b_fallback_used", oos.get("tier_b_fallback_used_count")),
            ("external_verification", external_verification_status),
            ("boundary", "mt5_runtime_probe_only"),
        )
    )
    row = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": lane,
        "status": "reviewed" if external_verification_status == "completed" else "payload_only",
        "judgment": (
            f"inconclusive_{judgment_prefix}_mt5_runtime_probe_completed"
            if external_verification_status == "completed"
            else f"inconclusive_{judgment_prefix}_payload"
        ),
        "path": run_output_root.as_posix(),
        "notes": notes,
    }
    return run02a._upsert_csv_rows(run02a.RUN_REGISTRY_PATH, scout.RUN_REGISTRY_COLUMNS, [row], key="run_id")


def run_stage11_lgbm_rank_threshold_scout(
    *,
    source_run_root: Path,
    run_output_root: Path,
    run_id: str,
    run_number: str,
    exploration_label: str,
    source_run_id: str,
    decision_surface_id: str,
    selection_policy: str,
    run_registry_lane: str,
    judgment_prefix: str,
    hypothesis: str,
    max_hold_bars: int,
    session_slice_id: str,
    tier_a_quantile: float,
    tier_a_min_margin: float,
    tier_b_quantile: float,
    tier_b_min_margin: float,
    invert_decisions: bool,
    context_gate: str | None,
    routed_fallback_enabled: bool,
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
) -> dict[str, Any]:
    if max_hold_bars != RUN01Y_REFERENCE["max_hold_bars"]:
        raise RuntimeError("Rank threshold scout keeps run01Y max_hold_bars fixed for threshold-only comparison.")
    if session_slice_id not in scout.SESSION_SLICE_DEFINITIONS:
        raise RuntimeError(f"Unknown session slice id: {session_slice_id}")
    routing_mode = scout.ROUTING_MODE_A_B_FALLBACK if routed_fallback_enabled else scout.ROUTING_MODE_A_ONLY

    scout.configure_run_identity(
        run_number=run_number,
        run_id=run_id,
        exploration_label=exploration_label,
        common_run_root=f"Project_Obsidian_Prime_v2/stage11/{run_id}",
    )
    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    models_root = run_output_root / "models"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"

    source_summary = read_json(source_run_root / "summary.json")
    base_route_coverage = source_summary["route_coverage"]
    split_specs = {
        "validation_is": ("2025.01.01", "2025.10.01"),
        "oos": ("2025.10.01", "2026.04.14"),
    }
    tier_a_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_a_predictions.parquet"))
    tier_b_source = pd.read_parquet(_io_path(source_run_root / "predictions" / "tier_b_predictions.parquet"))
    tier_a_allowed_by_split = {
        split_name: allowed_timestamps_from_feature_matrix(
            source_run_root / "mt5" / f"tier_a_{split_name}_feature_matrix.csv",
            context_gate,
        )
        for split_name in split_specs
    }
    tier_b_allowed_by_split = {
        split_name: allowed_timestamps_from_feature_matrix(
            source_run_root / "mt5" / f"tier_b_{split_name}_feature_matrix.csv",
            context_gate,
        )
        for split_name in split_specs
    }

    tier_a_rule = quantile_rule(
        tier_a_source,
        split_name="validation",
        quantile=tier_a_quantile,
        min_margin=tier_a_min_margin,
        prefix="tier_a",
    )
    tier_b_rule = quantile_rule(
        tier_b_source,
        split_name="validation",
        quantile=tier_b_quantile,
        min_margin=tier_b_min_margin,
        prefix="tier_b",
    )
    selected_threshold_id = (
        f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}"
        f"__hold{max_hold_bars}__slice_{session_slice_id}__model_lgbm_rank_target"
        f"{'_inverse' if invert_decisions else ''}"
        f"{'__ctx_' + context_gate if context_gate else ''}"
    )

    tier_a_predictions = recompute_predictions(tier_a_source, tier_a_rule, invert_decisions=invert_decisions)
    tier_b_predictions = recompute_predictions(tier_b_source, tier_b_rule, invert_decisions=invert_decisions)
    if context_gate is not None:
        tier_a_predictions = divergent.filter_predictions_for_context(
            tier_a_predictions,
            allowed_by_split=tier_a_allowed_by_split,
        )
        tier_b_predictions = divergent.filter_predictions_for_context(
            tier_b_predictions,
            allowed_by_split=tier_b_allowed_by_split,
        )
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    route_coverage = (
        scout.build_eval_route_coverage_summary(
            base_summary=base_route_coverage,
            tier_a_eval_frame=tier_a_predictions,
            tier_b_eval_frame=tier_b_predictions,
            no_tier_eval_frame=tier_a_predictions.iloc[0:0].copy(),
            session_slice=None,
        )
        if context_gate is not None
        else base_route_coverage
    )

    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)

    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)
    quantiles = (0.80, 0.85, 0.90, 0.94, 0.96, 0.98, 0.99)
    margins = (0.00, 0.02, 0.05, 0.08, 0.12)
    tier_a_sweep = quantile_sweep(tier_a_source, tier_name=scout.TIER_A, quantiles=quantiles, margins=margins, invert_decisions=invert_decisions)
    tier_b_sweep = quantile_sweep(tier_b_source, tier_name=scout.TIER_B, quantiles=quantiles, margins=margins, invert_decisions=invert_decisions)
    tier_a_sweep_path = sweeps_root / "rank_quantile_sweep_tier_a.csv"
    tier_b_sweep_path = sweeps_root / "rank_quantile_sweep_tier_b.csv"
    combined_sweep_path = sweeps_root / "rank_quantile_sweep_combined.csv"
    tier_a_sweep.to_csv(_io_path(tier_a_sweep_path), index=False)
    tier_b_sweep.to_csv(_io_path(tier_b_sweep_path), index=False)
    pd.concat([tier_a_sweep, tier_b_sweep], ignore_index=True).to_csv(_io_path(combined_sweep_path), index=False)

    tier_views = scout.build_tier_prediction_views(predictions)
    tier_outputs = scout.materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = scout.build_paired_tier_records(
        tier_views,
        run_id=run_id,
        stage_id=STAGE_ID,
        base_path=predictions_root,
        kpi_scope="signal_probability_rank_target_threshold",
        scoreboard_lane="structural_scout",
        external_verification_status="out_of_scope_by_claim",
    )
    python_ledger_rows = run02a.build_python_alpha_ledger_rows(
        run_id=run_id,
        tier_records=tier_records,
        selected_threshold_id=selected_threshold_id,
        model_family=MODEL_FAMILY,
    )
    for row in python_ledger_rows:
        row["kpi_scope"] = "signal_probability_rank_target_threshold"
        row["judgment"] = "inconclusive_lgbm_rank_threshold_payload"

    source_tier_a_onnx = source_run_root / "models" / "tier_a_lgbm_58_model.onnx"
    source_tier_b_onnx = source_run_root / "models" / "tier_b_lgbm_core42_model.onnx"
    tier_a_onnx_path = models_root / source_tier_a_onnx.name
    tier_b_onnx_path = models_root / source_tier_b_onnx.name
    model_copies = [
        copy_artifact(source_tier_a_onnx, tier_a_onnx_path),
        copy_artifact(source_tier_b_onnx, tier_b_onnx_path),
    ]
    source_tier_a_order = source_run_root / "models" / "tier_a_58_feature_order.txt"
    source_tier_b_order = source_run_root / "models" / "tier_b_core42_feature_order.txt"
    tier_a_feature_order_path = models_root / source_tier_a_order.name
    tier_b_feature_order_path = models_root / source_tier_b_order.name
    model_copies.extend(
        [
            copy_artifact(source_tier_a_order, tier_a_feature_order_path),
            copy_artifact(source_tier_b_order, tier_b_feature_order_path),
        ]
    )
    tier_a_feature_order = scout.load_feature_order(_io_path(tier_a_feature_order_path))
    tier_b_feature_order = scout.load_feature_order(_io_path(tier_b_feature_order_path))
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)

    mt5_attempts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    _io_path(mt5_root).mkdir(parents=True, exist_ok=True)
    common_copies.append(scout.copy_to_common_files(common_files_root, tier_a_onnx_path, scout.common_ref("models", tier_a_onnx_path.name)))
    common_copies.append(scout.copy_to_common_files(common_files_root, tier_b_onnx_path, scout.common_ref("models", tier_b_onnx_path.name)))

    copied_feature_matrices: list[dict[str, Any]] = []
    for split_name, (from_date, to_date) in split_specs.items():
        source_tier_a_matrix = source_run_root / "mt5" / f"tier_a_{split_name}_feature_matrix.csv"
        source_tier_b_matrix = source_run_root / "mt5" / f"tier_b_{split_name}_feature_matrix.csv"
        tier_a_matrix_path = mt5_root / source_tier_a_matrix.name
        tier_b_matrix_path = mt5_root / source_tier_b_matrix.name
        copied_feature_matrices.extend(
            [
                {"tier": scout.TIER_A, "split": split_name, **copy_or_filter_feature_matrix(source_tier_a_matrix, tier_a_matrix_path, context_gate)},
                {"tier": scout.TIER_B, "split": split_name, **copy_or_filter_feature_matrix(source_tier_b_matrix, tier_b_matrix_path, context_gate)},
            ]
        )
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_a_matrix_path, scout.common_ref("features", tier_a_matrix_path.name)))
        common_copies.append(scout.copy_to_common_files(common_files_root, tier_b_matrix_path, scout.common_ref("features", tier_b_matrix_path.name)))
        attempt = scout.materialize_mt5_routed_attempt_files(
            run_output_root=run_output_root,
            split_name=split_name,
            primary_onnx_path=tier_a_onnx_path,
            primary_feature_matrix_path=tier_a_matrix_path,
            primary_feature_count=len(tier_a_feature_order),
            primary_feature_order_hash=tier_a_feature_hash,
            fallback_onnx_path=tier_b_onnx_path,
            fallback_feature_matrix_path=tier_b_matrix_path,
            fallback_feature_count=len(tier_b_feature_order),
            fallback_feature_order_hash=tier_b_feature_hash,
            rule=tier_a_rule,
            fallback_rule=tier_b_rule,
            invert_signal=bool(invert_decisions),
            fallback_invert_signal=bool(invert_decisions),
            max_hold_bars=max_hold_bars,
            fallback_enabled=bool(routed_fallback_enabled),
            from_date=from_date,
            to_date=to_date,
        )
        mt5_attempts.append(attempt)

    compile_payload: dict[str, Any] | None = None
    mt5_execution_results: list[dict[str, Any]] = []
    if attempt_mt5:
        for attempt in mt5_attempts:
            for common_output_key in ("common_telemetry_path", "common_summary_path"):
                output_path = common_files_root / Path(str(attempt[common_output_key]))
                if scout._path_exists(output_path):
                    _io_path(output_path).unlink()
            scout.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        compile_payload = scout.compile_mql5_ea(metaeditor_path, scout.EA_SOURCE_PATH, mt5_root / "mt5_compile.log")
        if compile_payload["status"] == "completed":
            for attempt in mt5_attempts:
                try:
                    result = scout.run_mt5_tester(
                        terminal_path,
                        Path(attempt["ini"]["path"]),
                        set_path=Path(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / scout.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_root / scout.mt5_short_profile_ini_name(attempt["tier"], attempt["split"]),
                        timeout_seconds=300,
                    )
                except Exception as exc:  # pragma: no cover - external MT5 boundary
                    result = {"status": "blocked", "blocker": "mt5_tester_exception", "error": repr(exc)}
                result["tier"] = attempt["tier"]
                result["split"] = attempt["split"]
                result["routing_mode"] = attempt["routing_mode"]
                result["ini_path"] = attempt["ini"]["path"]
                result["runtime_outputs"] = (
                    scout.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
                    if result.get("status") == "completed"
                    else scout.validate_mt5_runtime_outputs(common_files_root, attempt)
                )
                if result["runtime_outputs"]["status"] != "completed":
                    result["status"] = "blocked"
                mt5_execution_results.append(result)

    mt5_report_records = (
        scout.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=run_output_root,
            attempts=mt5_attempts,
        )
        if attempt_mt5
        else []
    )
    scout.attach_mt5_report_metrics(mt5_execution_results, mt5_report_records)
    mt5_kpi_records = scout.build_mt5_kpi_records(mt5_execution_results)
    mt5_kpi_records = scout.enrich_mt5_kpi_records_with_route_coverage(mt5_kpi_records, route_coverage)
    expected_mt5_kpi_record_count = sum(
        3 if attempt.get("routing_mode") == scout.ROUTING_MODE_A_B_FALLBACK else 2 for attempt in mt5_attempts
    )
    mt5_runtime_completed = bool(mt5_execution_results) and all(item.get("status") == "completed" for item in mt5_execution_results)
    mt5_reports_completed = len(mt5_kpi_records) >= expected_mt5_kpi_record_count and all(
        item.get("status") == "completed" for item in mt5_kpi_records
    )
    external_status = (
        "completed"
        if mt5_runtime_completed and mt5_reports_completed
        else "blocked"
        if attempt_mt5
        else "out_of_scope_by_claim"
    )

    mt5_ledger_rows = run02a.build_mt5_alpha_ledger_rows(
        run_id=run_id,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_status,
    )
    ledger_rows = [*python_ledger_rows, *mt5_ledger_rows]
    ledger_payload = run02a.materialize_ledgers(ledger_rows)
    run_registry_payload = materialize_run_registry_row(
        run_id=run_id,
        run_output_root=run_output_root,
        route_coverage=route_coverage,
        tier_records=tier_records,
        external_verification_status=external_status,
        mt5_kpi_records=mt5_kpi_records,
        decision_surface_id=decision_surface_id,
        lane=run_registry_lane,
        judgment_prefix=judgment_prefix,
        invert_decisions=bool(invert_decisions),
        context_gate=context_gate,
        session_slice_id=session_slice_id,
        routing_mode=routing_mode,
    )

    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    artifacts = [
        {"role": "source_run_manifest", "path": (source_run_root / "run_manifest.json").as_posix(), "sha256": scout.sha256_file(source_run_root / "run_manifest.json")},
        {"role": "tier_a_predictions", "path": tier_a_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_a_predictions_path)},
        {"role": "tier_b_predictions", "path": tier_b_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(tier_b_predictions_path)},
        {"role": "tier_ab_combined_predictions", "path": combined_predictions_path.as_posix(), "format": "parquet", "sha256": scout.sha256_file(combined_predictions_path)},
        {"role": "tier_a_rank_quantile_sweep", "path": tier_a_sweep_path.as_posix(), "format": "csv", "sha256": scout.sha256_file(tier_a_sweep_path)},
        {"role": "tier_b_rank_quantile_sweep", "path": tier_b_sweep_path.as_posix(), "format": "csv", "sha256": scout.sha256_file(tier_b_sweep_path)},
        {"role": "combined_rank_quantile_sweep", "path": combined_sweep_path.as_posix(), "format": "csv", "sha256": scout.sha256_file(combined_sweep_path)},
        {"role": "copied_source_models_and_feature_orders", "copies": model_copies},
        {"role": "copied_feature_matrices", "copies": copied_feature_matrices},
        {"role": "mt5_attempts", "attempts": mt5_attempts},
        {"role": "mt5_common_file_copies", "copies": common_copies},
        {"role": "mt5_compile", "compile": compile_payload},
        {"role": "mt5_execution_results", "execution_results": mt5_execution_results},
        {"role": "mt5_strategy_tester_reports", "reports": mt5_report_records},
        {"role": "mt5_runtime_module_hashes", "modules": scout.mt5_runtime_module_hashes()},
        {"role": "tier_prediction_views", "views": tier_outputs},
        {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
        {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
        {"role": "project_run_registry", **run_registry_payload},
    ]
    decision_surface = {
        "decision_surface_id": decision_surface_id,
        "selection_policy": selection_policy,
        "source_run_id": source_run_id,
        "decision_direction_mode": "inverse" if invert_decisions else "normal",
        "context_gate": context_gate,
        "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
        "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
        "selected_threshold_id": selected_threshold_id,
        "broad_sweep": {
            "quantiles": list(quantiles),
            "margins": list(margins),
            "selection_scope": "validation_only",
            "mt5_attempt_policy": routing_mode,
            "invert_decisions": bool(invert_decisions),
        },
    }
    manifest = {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": STAGE_ID,
            "exploration_label": exploration_label,
            "model_family": MODEL_FAMILY,
            "status": "reviewed_payload",
            "judgment": (
                f"inconclusive_{judgment_prefix}_mt5_runtime_probe_completed"
                if external_status == "completed"
                else f"inconclusive_{judgment_prefix}_payload"
            ),
        },
        "hypothesis": hypothesis,
        "comparison_reference": RUN01Y_REFERENCE,
        "source_run_id": source_run_id,
        "decision_surface": decision_surface,
        "route_coverage": route_coverage,
        "tier_records": tier_records,
        "artifacts": artifacts,
        "mt5": {
            "attempted": bool(attempt_mt5),
            "attempt_policy": routing_mode,
            "fallback_enabled": bool(routed_fallback_enabled),
            "compile": compile_payload,
            "execution_results": mt5_execution_results,
            "strategy_tester_reports": mt5_report_records,
            "kpi_records": mt5_kpi_records,
            "runtime_completed": mt5_runtime_completed,
            "reports_completed": mt5_reports_completed,
        },
        "external_verification_status": external_status,
        "boundary": "lgbm_rank_threshold_runtime_probe_only_not_alpha_quality",
    }
    kpi = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "runtime_probe",
        "kpi_scope": "signal_probability_rank_target_threshold_trading_risk_execution",
        "decision_surface": decision_surface,
        "signal": {"tier_records": tier_records},
        "routing": {"route_coverage": route_coverage, "mt5_kpi_records": mt5_kpi_records},
        "mt5": manifest["mt5"],
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    summary = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "status": "reviewed_payload",
        "judgment": manifest["identity"]["judgment"],
        "selected_threshold_id": selected_threshold_id,
        "decision_surface": decision_surface,
        "tier_records": tier_records,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_execution_results": mt5_execution_results,
        "mt5_kpi_records": mt5_kpi_records,
        "ledger_rows": ledger_rows,
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
        "external_verification_status": external_status,
        "boundary": manifest["boundary"],
    }
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi)
    write_json(summary_path, summary)
    write_result_summary(
        path=result_summary_path,
        run_id=run_id,
        run_number=run_number,
        source_run_id=source_run_id,
        decision_direction_mode="inverse" if invert_decisions else "normal",
        context_gate=context_gate,
        selected_threshold_id=selected_threshold_id,
        tier_records=tier_records,
        mt5_kpi_records=mt5_kpi_records,
        external_status=external_status,
        routing_mode=routing_mode,
    )

    return {
        "status": "ok",
        "run_id": run_id,
        "run_output_root": run_output_root.as_posix(),
        "selected_threshold_id": selected_threshold_id,
        "external_verification_status": external_status,
        "mt5_attempted": bool(attempt_mt5),
        "mt5_kpi_records": mt5_kpi_records,
        "summary_path": summary_path.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "kpi_path": kpi_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "ledger_payload": ledger_payload,
        "run_registry_payload": run_registry_payload,
    }


def main() -> int:
    args = parse_args()
    payload = run_stage11_lgbm_rank_threshold_scout(
        source_run_root=Path(args.source_run_root),
        run_output_root=Path(args.run_output_root),
        run_id=args.run_id,
        run_number=args.run_number,
        exploration_label=args.exploration_label,
        source_run_id=args.source_run_id,
        decision_surface_id=args.decision_surface_id,
        selection_policy=args.selection_policy,
        run_registry_lane=args.run_registry_lane,
        judgment_prefix=args.judgment_prefix,
        hypothesis=args.hypothesis,
        max_hold_bars=args.max_hold_bars,
        session_slice_id=args.session_slice_id,
        tier_a_quantile=args.tier_a_quantile,
        tier_a_min_margin=args.tier_a_min_margin,
        tier_b_quantile=args.tier_b_quantile,
        tier_b_min_margin=args.tier_b_min_margin,
        invert_decisions=bool(args.invert_decisions),
        context_gate=args.context_gate,
        routed_fallback_enabled=not bool(args.disable_routed_fallback),
        attempt_mt5=bool(args.attempt_mt5),
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
    )
    print(json.dumps(scout._json_ready(payload), indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())

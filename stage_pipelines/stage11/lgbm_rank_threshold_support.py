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

from foundation.alpha import scout_runner as scout  # noqa: E402
from stage_pipelines.stage11 import lgbm_training_support as run02a  # noqa: E402
from stage_pipelines.stage11 import lgbm_divergent_support as divergent  # noqa: E402


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



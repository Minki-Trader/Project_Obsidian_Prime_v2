from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_12 import frontier12b_trade_shape_duration_label_proxy_scout as f12b


STAGE_ID = "stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout"
RUN_ID = "frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1"
RUN_NUMBER = "frontier17B"
PARENT_RUN_ID = "frontier17A_stage_open_loss_cluster_firewall_profit_persistence_onnx_scout_v1"
NEXT_GROK_RUN_ID = "frontier17C_grok_pre_expensive_loss_cluster_firewall_review_v1"
NEXT_REPAIR_RUN_ID = "frontier17C_loss_cluster_firewall_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_17/frontier17b_loss_cluster_firewall_profit_persistence_proxy_scout.py")

STAGE_BRIEF = STAGE_ROOT / "00_spec" / "stage_brief.md"
PROFILE_SPEC = STAGE_ROOT / "00_spec" / "firewall_profile_spec.md"
DEFINITION_LOCKS = STAGE_ROOT / "00_spec" / "definition_locks.md"
DO_NOT_REPEAT = STAGE_ROOT / "00_spec" / "do_not_repeat.md"
F17A_REPORT = STAGE_ROOT / "03_reviews" / f"{PARENT_RUN_ID}_report.md"
GROK_STAGE_OPEN_OUTPUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier17_stage_open/small_review/clean_output.md")

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES

MODEL_ID_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}

DIRECTION_COLUMNS = (
    "ema20_ema50_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "di_spread_14",
    "top3_weighted_return_1",
)
LOSS_PRESSURE_COLUMNS = (
    "directional_log_return_1_against",
    "directional_log_return_3_against",
    "hl_range",
    "abs_gap_percent",
    "atr_14_over_atr_50",
)

SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_CEILING = 15.0
SCOUT_WORST_SUBPERIOD_DD_CEILING = 25.0
SEED_DENSITY_LOW = 3.0
SEED_DENSITY_HIGH = 10.0

F16B_VALIDATION_PF = 1.067946
F16B_OOS_PF = 0.942216
F16B_VALIDATION_DD = 12.959868
F16B_OOS_DD = 12.803154
F16B_VALIDATION_DENSITY = 5.655738
F16B_OOS_DENSITY = 5.458015
F16D_VALIDATION_PF = 1.37
F16D_OOS_PF = 0.87
F16D_VALIDATION_DD = 12.20
F16D_OOS_DD = 47.17


@dataclass(frozen=True)
class FirewallProfile:
    variant_id: str
    family_id: str
    hold_bars: int
    adverse_cluster_quantile: float
    continuation_quantile: float
    early_window_bars: int = 0
    target_multiplier: float = 1.0
    adverse_cap_multiplier: float = 1.0
    early_adverse_cap_multiplier: float = 0.0
    recovery_floor_multiplier: float = 0.0


PROFILES: tuple[FirewallProfile, ...] = (
    FirewallProfile(
        variant_id="f17b_firewall_h8_ddq70_contq60",
        family_id="soft_firewall_moderate_continuation",
        hold_bars=8,
        adverse_cluster_quantile=0.70,
        continuation_quantile=0.60,
        target_multiplier=0.60,
        adverse_cap_multiplier=0.70,
    ),
    FirewallProfile(
        variant_id="f17b_firewall_h10_ddq75_contq65",
        family_id="balanced_firewall_stricter_veto",
        hold_bars=10,
        adverse_cluster_quantile=0.75,
        continuation_quantile=0.65,
        target_multiplier=0.65,
        adverse_cap_multiplier=0.75,
    ),
    FirewallProfile(
        variant_id="f17b_firewall_h12_ddq80_contq70",
        family_id="strict_firewall_strict_continuation",
        hold_bars=12,
        adverse_cluster_quantile=0.80,
        continuation_quantile=0.70,
        target_multiplier=0.70,
        adverse_cap_multiplier=0.80,
    ),
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_context = validate_stage_context()
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    result = train_and_evaluate(full, raw, feature_order)
    final = build_final(created_at, result, source_integrity, feature_order, stage_context)
    artifacts = write_artifacts(result, final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "seed_surface_rows": final["seed_surface_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def validate_stage_context() -> dict[str, Any]:
    required = [STAGE_BRIEF, PROFILE_SPEC, DEFINITION_LOCKS, DO_NOT_REPEAT, F17A_REPORT, GROK_STAGE_OPEN_OUTPUT]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing Frontier17 stage-open tracked context: {missing}")
    workspace = read_text(f03b.WORKSPACE_STATE)
    profile_text = read_text(PROFILE_SPEC)
    locks_text = read_text(DEFINITION_LOCKS)
    guard_text = read_text(DO_NOT_REPEAT)
    profile_ids = [profile.variant_id for profile in PROFILES]
    checks = {
        "workspace_current_stage_matches": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_matches": f"next_run_id: {RUN_ID}" in workspace,
        "profile_count_locked_to_three": len(PROFILES) == 3,
        "profile_ids_in_spec": all(profile_id in profile_text for profile_id in profile_ids),
        "definition_locks_present": all(
            token in locks_text
            for token in ("adverse_cluster_state_contract", "continuation_quality_contract", "decision_and_gate_contract")
        ),
        "no_f16_edge_margin_guard_present": "no_f16_locked_edge_margin_target8" in guard_text,
        "runtime_probe_guard_present": "mt5_runtime_probe_before_closeout" in guard_text,
        "stage_open_grok_available": "classification" in read_text(GROK_STAGE_OPEN_OUTPUT).lower(),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier17 tracked stage context failed checks: {json.dumps(checks, ensure_ascii=False)}")
    return {
        "stage_brief": artifact_identity(STAGE_BRIEF),
        "profile_spec": artifact_identity(PROFILE_SPEC),
        "definition_locks": artifact_identity(DEFINITION_LOCKS),
        "do_not_repeat": artifact_identity(DO_NOT_REPEAT),
        "frontier17a_report": artifact_identity(F17A_REPORT),
        "grok_stage_open_output": artifact_identity(GROK_STAGE_OPEN_OUTPUT),
        "checks": checks,
        "stage_open_artifact_boundary": (
            "tracked_stage_docs_used_because_02_runs_is_gitignored"
            "(02_runs는 gitignore 대상이라 추적 단계 문서를 사용)"
        ),
    }


def train_and_evaluate(full: pd.DataFrame, raw: pd.DataFrame, feature_order: list[str]) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values(피처 행렬에 NaN 또는 무한대가 있습니다).")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate(
        [np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256] for split in ("train", "validation", "oos")]
    )

    direction_score = build_direction_score(full, train_mask)
    direction = np.where(direction_score >= 0.0, 1, -1).astype("int8")
    loss_pressure = build_loss_pressure(full, direction, train_mask)

    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    oracle_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    firewall_transfer_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    target_diagnostics: list[dict[str, Any]] = []
    model_artifacts: list[dict[str, Any]] = []

    for profile in PROFILES:
        fwd_return = forward_return(full, raw, profile.hold_bars)
        labels, oracle_signal, state = build_firewall_labels(
            full=full,
            profile=profile,
            fwd_return=fwd_return,
            direction=direction,
            direction_score=direction_score,
            loss_pressure=loss_pressure,
            train_mask=train_mask,
        )
        distribution_rows.extend(f12b.label_distribution(full, labels, profile))
        oracle_metrics.extend(
            f12b.evaluate_all_splits(
                full,
                oracle_signal,
                fwd_return,
                profile,
                "oracle_firewall_continuation_label_replay(오라클 방화벽 지속 라벨 재생)",
                f"{profile.variant_id}__oracle",
            )
        )
        target_diagnostics.append({"target_id": profile.variant_id, **json_ready(asdict(profile)), **state["diagnostics"]})
        firewall_transfer_rows.extend(profile_transfer_audit_rows(full, profile, state, oracle_signal))
        missing_classes = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
        if missing_classes:
            skipped_rows.append(
                {
                    "target_id": profile.variant_id,
                    "reason": f"missing_train_classes={missing_classes}",
                    "label_boundary": "train_only_firewall_continuation_label(학습 전용 방화벽 지속 라벨)",
                }
            )
            continue

        for spec in f04d.MODEL_SPECS:
            model_short = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:12])
            candidate_id = f"{profile.variant_id}__{model_short}__firewall_continuation"
            model_instance_id = f"f17b_{candidate_id}"
            model = clone(spec.estimator)
            model.fit(x_all[train_mask], labels[train_mask])
            probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
            pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
            raw_model_signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")
            model_signal = raw_model_signal.copy()
            model_signal[state["adverse_veto"]] = 0

            target_dir = MODEL_DIR / profile.variant_id
            io_path(target_dir).mkdir(parents=True, exist_ok=True)
            model_path = target_dir / f"{model_instance_id}.joblib"
            onnx_path = target_dir / f"{model_instance_id}.onnx"
            joblib.dump(model, io_path(model_path))
            export_meta = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=x_all.shape[1],
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
            model_artifacts.append(
                {
                    "candidate_id": candidate_id,
                    "model_id": spec.model_id,
                    "model_instance_id": model_instance_id,
                    "joblib_path": model_path.as_posix(),
                    "joblib_sha256": sha256_file(model_path),
                    "onnx_path": onnx_path.as_posix(),
                    "onnx_sha256": export_meta["sha256"],
                    "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
                }
            )
            parity_rows.append(
                {
                    "candidate_id": candidate_id,
                    "target_id": profile.variant_id,
                    "model_id": spec.model_id,
                    "model_instance_id": model_instance_id,
                    "onnx_path": onnx_path.as_posix(),
                    "onnx_sha256": export_meta["sha256"],
                    "joblib_path": model_path.as_posix(),
                    "joblib_sha256": sha256_file(model_path),
                    "parity_passed": bool(parity["passed"]),
                    "parity_max_abs_diff": parity["max_abs_diff"],
                    "parity_mean_abs_diff": parity["mean_abs_diff"],
                    "rows_checked": parity["rows"],
                    "input_name": parity["input_name"],
                    "output_names": "|".join(parity["output_names"]),
                }
            )
            classification_rows.extend(
                f12b.classification_metrics(full, labels, pred_label, profile, spec.model_id, model_instance_id, candidate_id)
            )
            model_metrics.extend(
                f12b.evaluate_all_splits(
                    full,
                    model_signal,
                    fwd_return,
                    profile,
                    "model_argmax_and_current_firewall_signal(모델 최대확률과 현재 방화벽 신호)",
                    candidate_id,
                    model_id=spec.model_id,
                    model_instance_id=model_instance_id,
                )
            )
            subperiod_metrics.extend(
                f12b.evaluate_subperiods(full, model_signal, fwd_return, profile, candidate_id, spec.model_id, model_instance_id)
            )
            firewall_transfer_rows.extend(
                candidate_transfer_audit_rows(full, profile, candidate_id, spec.model_id, model_instance_id, state, raw_model_signal, model_signal)
            )

    candidate_summary = build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows)
    return {
        "model_metrics": model_metrics,
        "subperiod_metrics": subperiod_metrics,
        "oracle_metrics": oracle_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": distribution_rows,
        "firewall_transfer_audit": firewall_transfer_rows,
        "target_diagnostics": target_diagnostics,
        "skipped": skipped_rows,
        "candidate_summary": candidate_summary,
        "model_artifacts": model_artifacts,
    }


def build_direction_score(full: pd.DataFrame, train_mask: np.ndarray) -> np.ndarray:
    parts = [train_z(full[column].astype("float64").to_numpy(), train_mask) for column in DIRECTION_COLUMNS]
    return np.nanmean(np.vstack(parts), axis=0)


def build_loss_pressure(full: pd.DataFrame, direction: np.ndarray, train_mask: np.ndarray) -> np.ndarray:
    raw_parts = {
        "directional_log_return_1_against": -direction.astype("float64") * full["log_return_1"].astype("float64").to_numpy(),
        "directional_log_return_3_against": -direction.astype("float64") * full["log_return_3"].astype("float64").to_numpy(),
        "hl_range": full["hl_range"].astype("float64").to_numpy(),
        "abs_gap_percent": np.abs(full["gap_percent"].astype("float64").to_numpy()),
        "atr_14_over_atr_50": full["atr_14_over_atr_50"].astype("float64").to_numpy(),
    }
    parts = [train_z(raw_parts[column], train_mask) for column in LOSS_PRESSURE_COLUMNS]
    return np.nanmean(np.vstack(parts), axis=0)


def train_z(values: np.ndarray, train_mask: np.ndarray) -> np.ndarray:
    train_values = values[train_mask]
    mean = float(np.nanmean(train_values))
    std = float(np.nanstd(train_values))
    if not math.isfinite(std) or std <= 1e-12:
        return np.zeros(len(values), dtype="float64")
    return (values - mean) / std


def forward_return(full: pd.DataFrame, raw: pd.DataFrame, hold_bars: int) -> np.ndarray:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    return log_close[raw_indexes + hold_bars] - log_close[raw_indexes]


def build_firewall_labels(
    *,
    full: pd.DataFrame,
    profile: FirewallProfile,
    fwd_return: np.ndarray,
    direction: np.ndarray,
    direction_score: np.ndarray,
    loss_pressure: np.ndarray,
    train_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    continuation_quality = direction.astype("float64") * fwd_return
    adverse_threshold = float(np.nanquantile(loss_pressure[train_mask], profile.adverse_cluster_quantile))
    continuation_threshold = float(np.nanquantile(continuation_quality[train_mask], profile.continuation_quantile))
    adverse_veto = loss_pressure >= adverse_threshold
    continuation_trigger = continuation_quality >= continuation_threshold
    pass_gate = (~adverse_veto) & continuation_trigger
    signal = np.zeros(len(full), dtype="int8")
    signal[pass_gate] = direction[pass_gate]
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    diagnostics = {
        "label_boundary": (
            "train_only_loss_pressure_quantile_and_future_continuation_label_not_runtime"
            "(학습 전용 손실 압력 분위수와 미래 지속 라벨, 런타임 아님)"
        ),
        "direction_columns": "|".join(DIRECTION_COLUMNS),
        "loss_pressure_columns": "|".join(LOSS_PRESSURE_COLUMNS),
        "adverse_threshold": adverse_threshold,
        "continuation_threshold": continuation_threshold,
        "direction_long_fraction": float(np.mean(direction > 0)),
        "direction_score_train_mean": float(np.nanmean(direction_score[train_mask])),
        "loss_pressure_train_mean": float(np.nanmean(loss_pressure[train_mask])),
        "loss_pressure_train_std": float(np.nanstd(loss_pressure[train_mask])),
        "continuation_train_mean": float(np.nanmean(continuation_quality[train_mask])),
        "adverse_veto_all_count": int(adverse_veto.sum()),
        "continuation_trigger_all_count": int(continuation_trigger.sum()),
        "oracle_trade_all_count": int((signal != 0).sum()),
        "oracle_long_all_count": int((signal == 1).sum()),
        "oracle_short_all_count": int((signal == -1).sum()),
    }
    return labels, signal, {
        "adverse_veto": adverse_veto,
        "continuation_trigger": continuation_trigger,
        "continuation_quality": continuation_quality,
        "loss_pressure": loss_pressure,
        "direction": direction,
        "diagnostics": diagnostics,
    }


def profile_transfer_audit_rows(
    full: pd.DataFrame,
    profile: FirewallProfile,
    state: dict[str, Any],
    oracle_signal: np.ndarray,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        days = f12b.scout.count_scope_days(full.loc[mask, "timestamp"].reset_index(drop=True)) if int(mask.sum()) else 0
        oracle_trades = int((oracle_signal[mask] != 0).sum())
        rows.append(
            {
                "audit_kind": "profile_firewall_transfer(프로필 방화벽 전이)",
                "target_id": profile.variant_id,
                "candidate_id": "",
                "model_id": "",
                "model_instance_id": "",
                "split": split,
                "rows": int(mask.sum()),
                "days_in_scope": days,
                "adverse_veto_rate": safe_mean(state["adverse_veto"][mask]),
                "continuation_trigger_rate": safe_mean(state["continuation_trigger"][mask]),
                "oracle_trade_count": oracle_trades,
                "oracle_trades_per_day": float(oracle_trades / days) if days else 0.0,
                "oracle_long_count": int((oracle_signal[mask] == 1).sum()),
                "oracle_short_count": int((oracle_signal[mask] == -1).sum()),
                "density_floor_pass": bool((float(oracle_trades / days) if days else 0.0) >= SEED_DENSITY_LOW),
            }
        )
    return rows


def candidate_transfer_audit_rows(
    full: pd.DataFrame,
    profile: FirewallProfile,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
    state: dict[str, Any],
    raw_model_signal: np.ndarray,
    model_signal: np.ndarray,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    blocked_pred = (raw_model_signal != 0) & state["adverse_veto"]
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        days = f12b.scout.count_scope_days(full.loc[mask, "timestamp"].reset_index(drop=True)) if int(mask.sum()) else 0
        raw_trades = int((raw_model_signal[mask] != 0).sum())
        final_trades = int((model_signal[mask] != 0).sum())
        rows.append(
            {
                "audit_kind": "candidate_model_firewall_transfer(후보 모델 방화벽 전이)",
                "target_id": profile.variant_id,
                "candidate_id": candidate_id,
                "model_id": model_id,
                "model_instance_id": model_instance_id,
                "split": split,
                "rows": int(mask.sum()),
                "days_in_scope": days,
                "adverse_veto_rate": safe_mean(state["adverse_veto"][mask]),
                "continuation_trigger_rate": safe_mean(state["continuation_trigger"][mask]),
                "raw_model_trade_count": raw_trades,
                "raw_model_trades_per_day": float(raw_trades / days) if days else 0.0,
                "post_firewall_trade_count": final_trades,
                "post_firewall_trades_per_day": float(final_trades / days) if days else 0.0,
                "blocked_pred_trade_count": int(blocked_pred[mask].sum()),
                "blocked_pred_trade_fraction": float(blocked_pred[mask].sum() / raw_trades) if raw_trades else 0.0,
                "density_floor_pass": bool((float(final_trades / days) if days else 0.0) >= SEED_DENSITY_LOW),
            }
        )
    return rows


def build_candidate_summary(
    model_metrics: list[dict[str, Any]],
    subperiod_metrics: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    metrics_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for row in model_metrics:
        metrics_by_candidate.setdefault(str(row["candidate_id"]), []).append(row)
    sub_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for row in subperiod_metrics:
        sub_by_candidate.setdefault(str(row["candidate_id"]), []).append(row)
    parity_by_candidate = {str(row["candidate_id"]): row for row in parity_rows}
    class_by_candidate_split = {(str(row["candidate_id"]), str(row["split"])): row for row in classification_rows}
    summaries: list[dict[str, Any]] = []
    for candidate_id, rows in metrics_by_candidate.items():
        split_rows = {str(row["split"]): row for row in rows}
        if "validation" not in split_rows or "oos" not in split_rows:
            continue
        val = split_rows["validation"]
        oos = split_rows["oos"]
        subs = [row for row in sub_by_candidate.get(candidate_id, []) if row["split"] in {"validation", "oos"}]
        worst_sub_dd = max([float(row["dd_risk_percent"]) for row in subs], default=999.0)
        negative_subperiod_fraction = float(np.mean([float(row["net_profit"]) <= 0.0 for row in subs])) if subs else 1.0
        subperiod_density_min = min([float(row["trades_per_day"]) for row in subs], default=0.0)
        parity = parity_by_candidate.get(candidate_id, {})
        validation_class = class_by_candidate_split.get((candidate_id, "validation"), {})
        oos_class = class_by_candidate_split.get((candidate_id, "oos"), {})
        parity_passed = bool(parity.get("parity_passed"))

        strict = all(
            [
                parity_passed,
                metric_pass(val, density_low=SCOUT_DENSITY_LOW, density_high=SCOUT_DENSITY_HIGH),
                metric_pass(oos, density_low=SCOUT_DENSITY_LOW, density_high=SCOUT_DENSITY_HIGH),
                worst_sub_dd <= SCOUT_WORST_SUBPERIOD_DD_CEILING,
                negative_subperiod_fraction <= 0.25,
            ]
        )
        f16b_pf_axis_not_regressed = float(val["profit_factor"]) >= F16B_VALIDATION_PF and float(oos["profit_factor"]) >= F16B_OOS_PF
        f16d_runtime_pf_axis_not_regressed = float(oos["profit_factor"]) >= F16D_OOS_PF
        density_floor_validation_oos = (
            SEED_DENSITY_LOW <= float(val["trades_per_day"]) <= SEED_DENSITY_HIGH
            and SEED_DENSITY_LOW <= float(oos["trades_per_day"]) <= SEED_DENSITY_HIGH
        )
        oos_dd_improved_vs_f16 = float(oos["dd_risk_percent"]) < min(F16B_OOS_DD, F16D_OOS_DD)
        validation_dd_contained = float(val["dd_risk_percent"]) <= SCOUT_DD_CEILING
        seed = all(
            [
                parity_passed,
                float(val["net_profit"]) > 0.0,
                float(oos["net_profit"]) > 0.0,
                density_floor_validation_oos,
                f16b_pf_axis_not_regressed,
                f16d_runtime_pf_axis_not_regressed,
                oos_dd_improved_vs_f16,
                validation_dd_contained,
                worst_sub_dd <= SCOUT_WORST_SUBPERIOD_DD_CEILING,
                negative_subperiod_fraction <= 0.35,
            ]
        )
        preserved = all(
            [
                parity_passed,
                float(val["net_profit"]) > 0.0,
                float(oos["net_profit"]) > 0.0,
                min(float(val["trades_per_day"]), float(oos["trades_per_day"])) >= 2.0,
                max(float(val["trades_per_day"]), float(oos["trades_per_day"])) <= SEED_DENSITY_HIGH,
                f16d_runtime_pf_axis_not_regressed,
                (float(oos["dd_risk_percent"]) < F16D_OOS_DD or float(oos["profit_factor"]) > F16B_OOS_PF),
                float(val["dd_risk_percent"]) <= 22.0,
                worst_sub_dd <= 35.0,
            ]
        )
        score = (
            float(val["aspiration_distance_score"])
            + float(oos["aspiration_distance_score"])
            + (worst_sub_dd / 10.0)
            + negative_subperiod_fraction
            + (0.0 if seed else 1.0)
            + (0.0 if preserved else 2.0)
        )
        summaries.append(
            {
                "candidate_id": candidate_id,
                "target_id": val["target_id"],
                "model_id": val["model_id"],
                "model_instance_id": val["model_instance_id"],
                "strict_scout_clue_pass": bool(strict),
                "seed_surface_pass": bool(seed),
                "preserved_clue_pass": bool(preserved),
                "loss_cluster_score": score,
                "validation_profit_factor": val["profit_factor"],
                "validation_trades_per_day": val["trades_per_day"],
                "validation_dd_risk_percent": val["dd_risk_percent"],
                "validation_net_profit": val["net_profit"],
                "validation_equity_trend_r2": val["equity_trend_r2"],
                "oos_profit_factor": oos["profit_factor"],
                "oos_trades_per_day": oos["trades_per_day"],
                "oos_dd_risk_percent": oos["dd_risk_percent"],
                "oos_net_profit": oos["net_profit"],
                "oos_equity_trend_r2": oos["equity_trend_r2"],
                "validation_oos_subperiod_worst_dd_risk_percent": worst_sub_dd,
                "validation_oos_negative_subperiod_fraction": negative_subperiod_fraction,
                "validation_oos_subperiod_min_trades_per_day": subperiod_density_min,
                "parity_passed": parity_passed,
                "onnx_path": parity.get("onnx_path", ""),
                "onnx_sha256": parity.get("onnx_sha256", ""),
                "joblib_path": parity.get("joblib_path", ""),
                "joblib_sha256": parity.get("joblib_sha256", ""),
                "validation_macro_f1": validation_class.get("macro_f1", ""),
                "oos_macro_f1": oos_class.get("macro_f1", ""),
                "f16b_pf_axis_not_regressed": bool(f16b_pf_axis_not_regressed),
                "f16d_runtime_pf_axis_not_regressed": bool(f16d_runtime_pf_axis_not_regressed),
                "density_floor_validation_oos": bool(density_floor_validation_oos),
                "oos_dd_improved_vs_f16": bool(oos_dd_improved_vs_f16),
                "validation_dd_contained": bool(validation_dd_contained),
                "signal_contract": (
                    "argmax_short_or_long_and_current_adverse_veto_false_no_score_rank_density_calibration"
                    "(최대확률 숏/롱과 현재 불리 배제 false, 점수 순위 빈도 보정 없음)"
                ),
            }
        )
    summaries.sort(
        key=lambda row: (
            not bool(row["strict_scout_clue_pass"]),
            not bool(row["seed_surface_pass"]),
            not bool(row["preserved_clue_pass"]),
            float(row["loss_cluster_score"]),
        )
    )
    return json_ready(summaries)


def metric_pass(row: dict[str, Any], *, density_low: float, density_high: float) -> bool:
    return all(
        [
            float(row["net_profit"]) > 0.0,
            float(row["profit_factor"]) >= SCOUT_PF_FLOOR,
            density_low <= float(row["trades_per_day"]) <= density_high,
            float(row["dd_risk_percent"]) <= SCOUT_DD_CEILING,
        ]
    )


def build_final(
    created_at: str,
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_context: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    best = candidate_summary[0] if candidate_summary else {}
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    seed_rows = [row for row in candidate_summary if row.get("seed_surface_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    if strict_rows:
        status = "loss_cluster_firewall_strict_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run_id = NEXT_GROK_RUN_ID
    elif seed_rows:
        status = "loss_cluster_firewall_seed_surface_no_authority"
        judgment = "seed_surface_candidate(씨앗 표면 후보)"
        next_run_id = NEXT_GROK_RUN_ID
    elif preserved_rows:
        status = "loss_cluster_firewall_preserved_clue_no_authority"
        judgment = "preserved_clue_candidate(보존 단서 후보)"
        next_run_id = NEXT_GROK_RUN_ID
    elif candidate_summary:
        status = "loss_cluster_firewall_no_forward_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_GROK_RUN_ID
    else:
        status = "loss_cluster_firewall_invalid_no_trainable_candidate_no_authority"
        judgment = "invalid_setup_candidate(무효 설정 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "strict_scout_clue_rows": len(strict_rows),
        "seed_surface_rows": len(seed_rows),
        "preserved_clue_rows": len(preserved_rows),
        "candidate_row_count": len(candidate_summary),
        "best_candidate_row": best,
        "profile_count": len(PROFILES),
        "model_count": len(f04d.MODEL_SPECS),
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "source_integrity": source_integrity,
        "stage_context": stage_context,
        "data_integrity": data_integrity_record(source_integrity, feature_order),
        "model_validation": model_validation_record(best),
        "artifact_lineage": artifact_lineage_record(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_before_wfo_or_mt5(WFO/MT5 전 그록 검토 필요)",
        "mt5_status": "not_run_proxy_only_runtime_probe_required_before_closeout(프록시 전용, 마감 전 런타임 탐침 필요)",
    }


def data_integrity_record(source_integrity: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    return {
        "data_source": f03b.DATASET_PATH.as_posix(),
        "time_axis": "US100 M5 closed-bar timestamps, UTC storage, New York calendar only for period grouping(US100 M5 종료봉 타임스탬프, UTC 저장, 기간 묶음만 뉴욕 달력)",
        "sample_scope": "Tier A full-context model input rows, train/validation/OOS fixed split(Tier A 전체 문맥 모델 입력 행, 학습/검증/표본밖 고정 분할)",
        "missing_or_duplicate_check": source_integrity.get("integrity_judgment", "source_integrity_carried_with_boundary"),
        "feature_label_boundary": "features are closed-bar; continuation quality uses future return only as training label, not as runtime feature(피처는 종료봉, 지속 품질은 학습 라벨에만 미래 수익 사용)",
        "split_boundary": "all thresholds and quantiles fit on train only(모든 임계값과 분위수는 학습 구간에서만 적합)",
        "leakage_risk": "direction and loss-pressure state are current-bar features; continuation label is future and separated into target(방향과 손실 압력은 현재봉 피처, 지속 라벨은 미래 목표로 분리)",
        "data_hash_or_identity": {
            "dataset_sha256": sha256_file(f03b.DATASET_PATH),
            "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
            "feature_order_hash": ordered_hash(feature_order),
        },
        "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
    }


def model_validation_record(best: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fixed sklearn-to-ONNX class probability models(고정 sklearn-to-ONNX 분류 확률 모델)",
        "target_and_label": "loss-pressure firewall plus realized continuation label(손실 압력 방화벽과 실현 지속 라벨)",
        "split_method": "fixed train/validation/OOS split, no WFO yet(고정 학습/검증/표본밖 분할, WFO 아직 없음)",
        "selection_metric": "strict clue, seed surface, preserved clue, then loss-cluster score(탐색 단서, 씨앗 표면, 보존 단서, 손실 군집 점수 순)",
        "secondary_metrics": "PF, density, DD, subperiod DD, negative subperiod fraction, ONNX parity(PF, 빈도, 손실폭, 하위기간 손실폭, 부정 하위기간 비율, ONNX 동등성)",
        "threshold_policy": "three pre-registered train-only profile quantiles; no score-rank density calibration(사전 등록 3개 학습 전용 프로필 분위수, 점수 순위 빈도 보정 없음)",
        "overfit_risk": "single proxy pass without WFO; next expensive check requires Grok review(WFO 없는 단일 프록시 회차, 다음 비싼 검증 전 그록 검토 필요)",
        "calibration_risk": "classifier outputs are class scores for argmax, not economic probabilities(분류기 출력은 최대확률용 점수, 경제 확률 아님)",
        "comparison_baseline": "F16B proxy and F16D runtime observation are reference-only(F16B 프록시와 F16D 런타임 관찰은 참조 전용)",
        "validation_judgment": "exploratory_scout_only(탐색 전용)",
        "best_candidate": best.get("candidate_id", "none"),
    }


def artifact_lineage_record() -> dict[str, Any]:
    return {
        "source_inputs": [
            f03b.DATASET_PATH.as_posix(),
            f03b.FEATURE_ORDER_PATH.as_posix(),
            STAGE_BRIEF.as_posix(),
            PROFILE_SPEC.as_posix(),
            DEFINITION_LOCKS.as_posix(),
            GROK_STAGE_OPEN_OUTPUT.as_posix(),
        ],
        "producer": SCRIPT_PATH.as_posix(),
        "consumer": REPORT_PATH.as_posix(),
        "artifact_paths": [RUN_ROOT.as_posix(), REPORT_PATH.as_posix()],
        "artifact_hashes": "run_manifest records small evidence and generated model hashes(실행 목록이 작은 근거와 생성 모델 해시를 기록)",
        "registry_links": [f03b.RUN_REGISTRY.as_posix(), f03b.ALPHA_LEDGER.as_posix(), (STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv").as_posix()],
        "availability": "small_evidence_force_trackable_models_ignored_with_manifest(작은 근거는 강제 추적 가능, 모델은 목록으로 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "profile_manifest": RUN_ROOT / "profile_manifest.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "oracle_metrics": RUN_ROOT / "oracle_metrics.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "firewall_transfer_audit": RUN_ROOT / "firewall_transfer_audit.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.json",
        "skipped": RUN_ROOT / "skipped.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["profile_manifest"], [asdict(profile) for profile in PROFILES])
    write_csv(artifacts["label_distribution"], result["label_distribution"])
    write_csv(artifacts["oracle_metrics"], result["oracle_metrics"])
    write_csv(artifacts["model_metrics"], result["model_metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["firewall_transfer_audit"], result["firewall_transfer_audit"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["skipped"], result["skipped"])
    write_json(artifacts["target_diagnostics"], result["target_diagnostics"])
    write_json(artifacts["final_decision"], final)
    manifest = {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "dataset": artifact_identity(f03b.DATASET_PATH),
        "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
        "artifacts": {key: path.as_posix() for key, path in artifacts.items()},
        "artifact_identities": {
            key: artifact_identity(path)
            for key, path in artifacts.items()
            if key not in {"run_manifest"}
        },
        "model_artifacts": result["model_artifacts"],
        "regeneration_command": f"python {SCRIPT_PATH.as_posix()}",
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier17B Loss Cluster Firewall Profit Persistence Proxy Scout(전선17B 손실 군집 방화벽 수익 지속성 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): 3개 fixed firewall profiles(고정 방화벽 프로필)에 train-only loss-pressure score(학습 전용 손실 압력 점수)와 continuation quality label(지속 품질 라벨)을 적용해 ONNX proxy scout(ONNX 프록시 탐색)를 실행했습니다.

Effect(효과): F15/F16(전선15/16)의 score threshold/edge_margin(점수 임계값/엣지 마진)을 반복하지 않고, 현재 adverse veto(불리 배제)와 모델 continuation prediction(지속 예측)이 동시에 맞는지 확인했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- seed surface rows(씨앗 표면 행): `{final['seed_surface_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최선 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`
- negative subperiod fraction(부정 하위기간 비율): `{fmt(best.get('validation_oos_negative_subperiod_fraction'))}`
- ONNX parity(ONNX 동등성): `{best.get('parity_passed', 'n/a')}`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- firewall transfer audit(방화벽 전이 감사): `{artifacts['firewall_transfer_audit'].as_posix()}`
- model metrics(모델 지표): `{artifacts['model_metrics'].as_posix()}`
- subperiod metrics(하위기간 지표): `{artifacts['subperiod_metrics'].as_posix()}`
- ONNX parity(ONNX 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Boundaries(경계)

Evidence boundary(근거 경계): proxy-only(프록시 전용), P2 model-input parity(모델 입력 동등성)와 ONNX parity(ONNX 동등성)까지만 확인했습니다.

Missing evidence(부족 근거): WFO(워크포워드 최적화), stress(스트레스), MT5 runtime probe(MT5 런타임 탐침)는 아직 실행하지 않았습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

Next action(다음 행동): `{final['next_run_id']}`. Effect(효과): expensive WFO/MT5(비싼 WFO/MT5) 또는 closeout(마감)으로 가기 전에 Grok second opinion(그록 2차 의견)과 local verification(로컬 검증)을 거칩니다.
"""
    f03b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict={final['strict_scout_clue_rows']}, seed={final['seed_surface_rows']}, preserved={final['preserved_clue_rows']}, next `{final['next_run_id']}`.\n",
    )


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join(
        [
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
        ]
    )


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier17B(전선17B)가 loss-cluster firewall profit-persistence proxy scout(손실 군집 방화벽 수익 지속성 프록시 탐색)를 실행했습니다.

Effect(효과): best candidate(최선 후보) `{best.get('candidate_id', 'none')}`의 PF-density-DD(수익 팩터-빈도-손실폭)를 기록했고, MT5 runtime probe(MT5 런타임 탐침) 전에는 권위 주장을 하지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier17 Selection Status(전선17 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최선 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Seed surface rows(씨앗 표면 행): `{final['seed_surface_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`

Key artifacts(핵심 산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['firewall_transfer_audit'].as_posix()}`
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier17 Review Index(전선17 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{PARENT_RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), definition locks(정의 고정), runtime probe obligation(런타임 탐침 의무) recorded(기록됨).
- `{RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, seed rows(씨앗 행) `{final['seed_surface_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`.
- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- firewall transfer audit(방화벽 전이 감사): `{artifacts['firewall_transfer_audit'].as_posix()}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier17B Required Gate Coverage Audit(전선17B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): 3 profiles(프로필) x 3 model specs(모델 규격)을 실행했습니다.
- kpi_contract_audit(KPI 계약 감사): validation/OOS PF-density-DD(검증/표본밖 수익 팩터-빈도-손실폭), subperiod DD(하위기간 손실폭), negative subperiod fraction(부정 하위기간 비율)을 기록했습니다.
- data_integrity_gate(데이터 무결성 게이트): `{final['data_integrity']['integrity_judgment']}`
- model_validation_gate(모델 검증 게이트): `{final['model_validation']['validation_judgment']}`
- artifact_lineage_gate(산출물 계보 게이트): `{final['artifact_lineage']['lineage_judgment']}`
- firewall_transfer_audit(방화벽 전이 감사): train-frozen quantile(학습 고정 분위수)로 validation/OOS veto/pass rates(검증/표본밖 배제율/통과율)를 기록했습니다.
- tier_pair_gate(티어 쌍 게이트): Tier A separate(티어 A 분리)는 기록했고, Tier B/combined(티어 B/합산)는 missing_required(필수 누락)로 기록했습니다.
- onnx_parity_gate(ONNX 동등성 게이트): 후보별 ONNX parity(ONNX 동등성)를 기록했습니다. 통과 없는 후보는 clue(단서)로 판정하지 않습니다.
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): closeout(마감) 전 MT5 runtime probe(MT5 런타임 탐침) 또는 exact blocked reason(정확한 차단 사유)이 아직 필요합니다.
- final_claim_guard(최종 주장 보호): completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장) 없음.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "loss_cluster_firewall_profit_persistence_proxy_scout(손실 군집 방화벽 수익 지속성 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": (
            f"strict={final['strict_scout_clue_rows']};seed={final['seed_surface_rows']};"
            f"preserved={final['preserved_clue_rows']};no_wfo_no_mt5_no_authority"
        ),
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "proxy_scout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "train_only_profile_quantiles_no_score_rank_density_calibration(학습 전용 프로필 분위수, 점수 순위 빈도 보정 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_yet_pre_expensive_grok_next(주장 범위 밖, MT5 아직 없음, 비싼 검증 전 그록 다음)",
        "result_path": REPORT_PATH.as_posix(),
        "final_decision_path": artifacts["final_decision"].as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "loss_cluster_firewall_proxy_scout(손실 군집 방화벽 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "train_only_firewall_continuation_no_wfo_no_mt5_no_authority(학습 전용 방화벽 지속, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_yet_pre_expensive_grok_next(주장 범위 밖, MT5 아직 없음, 비싼 검증 전 그록 다음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_loss_cluster_firewall_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_loss_cluster_firewall_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "loss_cluster_firewall_proxy_not_runtime(손실 군집 방화벽 프록시, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"strict={final['strict_scout_clue_rows']};seed={final['seed_surface_rows']};preserved={final['preserved_clue_rows']};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"seed={best.get('seed_surface_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"worst_sub_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}"
    )


def safe_mean(mask: np.ndarray) -> float:
    return float(np.mean(mask)) if len(mask) else 0.0


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(rows)).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "inf"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())

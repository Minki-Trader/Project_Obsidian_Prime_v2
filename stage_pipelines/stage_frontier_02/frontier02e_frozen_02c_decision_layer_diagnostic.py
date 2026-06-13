from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_02 import trainable_onnx_seed_surface as trainable


STAGE_ID = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ID = "frontier02E_grok_pre_expensive_review_or_second_repair_v1"
RUN_NUMBER = "frontier02E"
PARENT_RUN_ID = "frontier02D_review_and_repair_onnx_seed_surface_v1"
ANCHOR_RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
NEXT_GO_RUN_ID = "frontier02F_capped_decision_layer_repair_v1"
NEXT_NOGO_RUN_ID = "frontier02F_stage_closeout_preserved_clue_negative_memory_v1"

RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
ANCHOR_ROOT = Path("stages") / STAGE_ID / "02_runs" / ANCHOR_RUN_ID
PARENT_ROOT = Path("stages") / STAGE_ID / "02_runs" / PARENT_RUN_ID
ANCHOR_REPLAY = ANCHOR_ROOT / "top_decision_signal_replay.csv"
ANCHOR_SUMMARY = ANCHOR_ROOT / "decision_surface_summary.csv"
PARENT_SUMMARY = PARENT_ROOT / "repair_decision_surface_summary.csv"
MODEL_INPUT_DATASET = Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet")
FEATURE_ORDER = Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt")
GROK_REVIEW_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier02E_pre_expensive_review/medium_review")

RAW_THRESHOLDS = (0.30, 0.34, 0.38, 0.42, 0.46, 0.50, 0.55, 0.60, 0.65, 0.70)
CALIBRATED_THRESHOLDS = (0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62)
EDGE_MARGINS = (0.00, 0.03, 0.05, 0.08, 0.10)
COOLDOWNS = (0, 3, 6, 9, 12, 18)
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET)).reset_index(drop=True)
    replay = pd.read_csv(io_path(ANCHOR_REPLAY))
    verify_replay_alignment(frame, replay)
    filters = scout.build_filters(frame)
    filter_mask = filters["mid_cash"].fillna(False).to_numpy(dtype=bool)
    probabilities = replay[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    feature_frame = frame.copy()
    feature_frame["timestamp"] = pd.to_datetime(feature_frame["timestamp"], utc=True)

    anchor_summary = pd.read_csv(io_path(ANCHOR_SUMMARY))
    parent_summary = pd.read_csv(io_path(PARENT_SUMMARY))
    anchor_best = best_rank(anchor_summary)
    parent_best = best_rank(parent_summary)

    scores = build_scores(frame, probabilities, filter_mask)
    metrics = build_metrics(frame, probabilities, scores, filter_mask, anchor_best)
    summary = build_summary(metrics)
    top = rank_summary(summary).iloc[0].to_dict()
    go_rows = go_rule_rows(summary)
    loss_attribution = build_loss_attribution(feature_frame, replay)
    local_verification = build_local_verification(anchor_best, parent_best, summary, go_rows)
    advice = build_grok_advice_classification(local_verification, go_rows)
    report = build_report(anchor_best, parent_best, top, summary, go_rows, loss_attribution, local_verification, advice)

    paths = {
        "diagnostic_metrics": RUN_ROOT / "diagnostic_metrics.csv",
        "diagnostic_summary": RUN_ROOT / "diagnostic_summary.csv",
        "go_rule_rows": RUN_ROOT / "go_rule_rows.csv",
        "loss_attribution": RUN_ROOT / "loss_attribution.csv",
        "local_verification": RUN_ROOT / "local_verification.json",
        "grok_advice_classification": RUN_ROOT / "grok_advice_classification.json",
    }
    metrics.to_csv(io_path(paths["diagnostic_metrics"]), index=False, lineterminator="\n")
    summary.to_csv(io_path(paths["diagnostic_summary"]), index=False, lineterminator="\n")
    go_rows.to_csv(io_path(paths["go_rule_rows"]), index=False, lineterminator="\n")
    loss_attribution.to_csv(io_path(paths["loss_attribution"]), index=False, lineterminator="\n")
    write_json(paths["local_verification"], local_verification)
    write_json(paths["grok_advice_classification"], advice)
    write_text_sig(REPORT_PATH, report)
    manifest = build_manifest(paths, anchor_best, parent_best, top, summary, go_rows, local_verification, advice)
    write_json(RUN_ROOT / "run_manifest.json", manifest)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": manifest["status"],
                "decision_rows": int(len(summary)),
                "metric_rows": int(len(metrics)),
                "go_rule_rows": int(len(go_rows)),
                "best_candidate": top["candidate_id"],
                "validation_pf": fmt(top["validation_profit_factor"]),
                "validation_density": fmt(top["validation_trades_per_day"]),
                "validation_dd": fmt(top["validation_max_drawdown_percent"]),
                "oos_pf": fmt(top["oos_profit_factor"]),
                "oos_density": fmt(top["oos_trades_per_day"]),
                "oos_dd": fmt(top["oos_max_drawdown_percent"]),
                "next_run_id": manifest["next_run_id"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_scores(frame: pd.DataFrame, probabilities: np.ndarray, filter_mask: np.ndarray) -> pd.DataFrame:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    direction = np.where(p_long >= p_short, 1, -1).astype("int8")
    directional_confidence = np.maximum(p_long, p_short)
    edge_over_flat = directional_confidence - p_flat
    validation = frame["split"].astype(str).eq("validation").to_numpy(dtype=bool) & filter_mask
    pnl_if_direction = direction.astype("float64") * pd.to_numeric(frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64") - scout.ROUGH_COST_LOG_RETURN
    y = (pnl_if_direction[validation] > 0).astype("int8")
    x_conf = directional_confidence[validation]
    x_edge = edge_over_flat[validation]
    if len(np.unique(y)) < 2 or len(y) < 50:
        isotonic_score = np.full(len(frame), float(np.mean(y)) if len(y) else 0.5)
        platt_score = isotonic_score.copy()
        calibration_status = "fallback_constant_insufficient_validation_classes"
    else:
        iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        iso.fit(x_conf, y)
        isotonic_score = iso.predict(directional_confidence)
        platt = LogisticRegression(max_iter=500, solver="lbfgs")
        platt.fit(np.column_stack([x_conf, x_edge]), y)
        platt_score = platt.predict_proba(np.column_stack([directional_confidence, edge_over_flat]))[:, 1]
        calibration_status = "validation_only_fit"
    return pd.DataFrame(
        {
            "direction": direction,
            "directional_confidence": directional_confidence,
            "edge_over_flat": edge_over_flat,
            "isotonic_win_probability": isotonic_score,
            "platt_win_probability": platt_score,
            "calibration_status": calibration_status,
        }
    )


def build_metrics(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    scores: pd.DataFrame,
    filter_mask: np.ndarray,
    anchor_best: dict[str, Any],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for threshold in RAW_THRESHOLDS:
        for margin in EDGE_MARGINS:
            raw_signal = trainable.signal_from_probabilities(
                probabilities,
                threshold=float(threshold),
                margin=float(margin),
                filter_mask=filter_mask,
                side_mode="both",
            )
            for cooldown in COOLDOWNS:
                signal = scout.apply_cooldown(raw_signal, cooldown)
                candidate_id = f"f02e_raw_prob__p{int(round(threshold * 100))}__m{int(round(margin * 100))}__cd{cooldown}"
                rows.extend(evaluate_all_splits(frame, signal, candidate_id, "raw_probability", threshold, margin, cooldown, anchor_best))
    direction = scores["direction"].to_numpy(dtype="int8")
    edge = scores["edge_over_flat"].to_numpy(dtype="float64")
    for score_mode, column in (("isotonic", "isotonic_win_probability"), ("platt", "platt_win_probability")):
        score = scores[column].to_numpy(dtype="float64")
        for threshold in CALIBRATED_THRESHOLDS:
            for margin in EDGE_MARGINS:
                raw_signal = np.zeros(len(frame), dtype="int8")
                mask = (score >= float(threshold)) & (edge >= float(margin)) & filter_mask
                raw_signal[mask] = direction[mask]
                for cooldown in COOLDOWNS:
                    signal = scout.apply_cooldown(raw_signal, cooldown)
                    candidate_id = f"f02e_{score_mode}_cal__p{int(round(threshold * 100))}__m{int(round(margin * 100))}__cd{cooldown}"
                    rows.extend(evaluate_all_splits(frame, signal, candidate_id, score_mode, threshold, margin, cooldown, anchor_best))
    return pd.DataFrame(rows)


def evaluate_all_splits(
    frame: pd.DataFrame,
    signal: np.ndarray,
    candidate_id: str,
    score_mode: str,
    threshold: float,
    margin: float,
    cooldown: int,
    anchor_best: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for split in ("train", "validation", "oos"):
        row = trainable.evaluate_model_split(
            frame=frame,
            signal=signal,
            split=split,
            candidate_id=candidate_id,
            model_id=str(anchor_best["candidate_model_id"]),
            teacher_candidate_id=str(anchor_best["teacher_candidate_id"]),
            surface=str(anchor_best["surface"]),
            filter_name="mid_cash",
            side_mode="both",
            probability_threshold=float(threshold),
            probability_margin=float(margin),
            cooldown=int(cooldown),
        )
        row["score_mode"] = score_mode
        row["diagnostic_axis"] = "frozen_02c_decision_layer"
        rows.append(row)
    return rows


def build_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "candidate_id",
        "candidate_model_id",
        "teacher_candidate_id",
        "surface",
        "filter_name",
        "side_mode",
        "score_mode",
        "probability_threshold",
        "probability_margin",
        "cooldown_bars",
        "hold_bars",
        "diagnostic_axis",
    ]
    metric_cols = [
        "trade_count",
        "days_in_scope",
        "trades_per_day",
        "sparse_flag",
        "pf999_sparse_flag",
        "long_trade_count",
        "short_trade_count",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "max_drawdown_percent",
        "max_monthly_drawdown_percent",
        "underwater_ratio",
        "max_loss_streak",
        "equity_trend_r2",
        "aspiration_distance_score",
        "joint_pass_count",
        "density_pass",
        "pf_pass",
        "dd_pass",
        "smoothness_pass",
    ]
    rows: list[dict[str, Any]] = []
    for _, group in metrics.groupby(keys, sort=False):
        row = {key: group.iloc[0][key] for key in keys}
        for split in ("train", "validation", "oos"):
            split_row = group.loc[group["split"].eq(split)].iloc[0]
            for column in metric_cols:
                row[f"{split}_{column}"] = split_row[column]
        row["non_sparse_validation_oos"] = not bool(row["validation_sparse_flag"]) and not bool(row["oos_sparse_flag"])
        row["positive_validation_oos"] = float(row["validation_net_profit"]) > 0 and float(row["oos_net_profit"]) > 0
        row["diagnostic_observation_flag"] = bool(
            row["non_sparse_validation_oos"]
            and row["positive_validation_oos"]
            and int(row["validation_joint_pass_count"]) >= 1
            and int(row["oos_joint_pass_count"]) >= 1
        )
        row["go_rule_flag"] = bool(
            float(row["oos_profit_factor"]) >= 1.20
            and bool(row["oos_density_pass"])
            and bool(row["oos_dd_pass"])
            and float(row["oos_net_profit"]) > 0
        )
        rows.append(row)
    out = pd.DataFrame(rows)
    ranked = rank_summary(out)
    out["validation_rank"] = pd.NA
    out.loc[ranked.index, "validation_rank"] = np.arange(1, len(ranked) + 1)
    return out.sort_values(["validation_rank", "candidate_id"]).reset_index(drop=True)


def rank_summary(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.sort_values(
        ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
        ascending=[True, False, True],
    )


def go_rule_rows(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.loc[summary["go_rule_flag"].astype(bool)].copy().sort_values(
        ["oos_profit_factor", "oos_trades_per_day", "oos_max_drawdown_percent"],
        ascending=[False, False, True],
    )


def build_loss_attribution(frame: pd.DataFrame, replay: pd.DataFrame) -> pd.DataFrame:
    replay = replay.copy()
    replay["timestamp"] = pd.to_datetime(replay["timestamp"], utc=True)
    merged = replay.merge(
        frame[
            [
                "timestamp",
                "is_first_30m_after_open",
                "is_last_30m_before_cash_close",
                "minutes_from_cash_open",
                "adx_14",
                "atr_14_over_atr_50",
                "vix_zscore_20",
            ]
        ],
        on="timestamp",
        how="left",
    )
    oos = merged.loc[merged["split"].astype(str).eq("oos") & merged["signal"].ne(0)].copy()
    if oos.empty:
        return pd.DataFrame()
    p_dir = np.where(oos["signal"].to_numpy(dtype="int8") == 1, oos["p_long"], oos["p_short"])
    p_other = np.where(oos["signal"].to_numpy(dtype="int8") == 1, oos["p_short"], oos["p_long"])
    oos["directional_confidence"] = p_dir
    oos["edge_over_flat"] = p_dir - np.maximum(p_other, oos["p_flat"].to_numpy(dtype="float64"))
    oos["trade_pnl"] = oos["signal"].astype("float64") * pd.to_numeric(oos["future_log_return_12"], errors="coerce") - scout.ROUGH_COST_LOG_RETURN
    oos["confidence_decile"] = pd.qcut(oos["directional_confidence"], q=10, duplicates="drop").astype(str)
    oos["session_bucket"] = np.select(
        [
            pd.to_numeric(oos["is_first_30m_after_open"], errors="coerce").fillna(0).eq(1),
            pd.to_numeric(oos["is_last_30m_before_cash_close"], errors="coerce").fillna(0).eq(1),
        ],
        ["first_30m", "last_30m"],
        default="mid_cash",
    )
    oos["adx_bucket"] = pd.cut(pd.to_numeric(oos["adx_14"], errors="coerce"), bins=[-np.inf, 20, 30, np.inf], labels=["adx_lt20", "adx_20_30", "adx_ge30"]).astype(str)
    oos["vix_bucket"] = pd.qcut(pd.to_numeric(oos["vix_zscore_20"], errors="coerce"), q=3, duplicates="drop").astype(str)
    oos["atr_ratio_bucket"] = pd.qcut(pd.to_numeric(oos["atr_14_over_atr_50"], errors="coerce"), q=3, duplicates="drop").astype(str)
    rows: list[dict[str, Any]] = []
    for bucket_type in ("confidence_decile", "session_bucket", "adx_bucket", "vix_bucket", "atr_ratio_bucket"):
        for bucket_value, group in oos.groupby(bucket_type, dropna=False):
            rows.append(loss_bucket_row(bucket_type, str(bucket_value), group))
    return pd.DataFrame(rows)


def loss_bucket_row(bucket_type: str, bucket_value: str, group: pd.DataFrame) -> dict[str, Any]:
    pnl = group["trade_pnl"].to_numpy(dtype="float64")
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(losses.sum()) if len(losses) else 0.0
    pf = 999.0 if gross_loss == 0 and gross_profit > 0 else (gross_profit / abs(gross_loss) if gross_loss else 0.0)
    return {
        "bucket_type": bucket_type,
        "bucket_value": bucket_value,
        "trade_count": int(len(group)),
        "long_trade_count": int((group["signal"] == 1).sum()),
        "short_trade_count": int((group["signal"] == -1).sum()),
        "net_profit": float(pnl.sum()),
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": float(pf),
        "win_rate": float(len(wins) / len(pnl)) if len(pnl) else 0.0,
        "mean_directional_confidence": float(group["directional_confidence"].mean()),
        "mean_edge_over_flat": float(group["edge_over_flat"].mean()),
    }


def build_local_verification(anchor_best: dict[str, Any], parent_best: dict[str, Any], summary: pd.DataFrame, go_rows: pd.DataFrame) -> dict[str, Any]:
    repair_rows = pd.read_csv(io_path(PARENT_SUMMARY))
    repair_observations = repair_rows.loc[repair_rows["repair_observation_flag"].astype(str).str.lower().eq("true")]
    better_pf = repair_observations.loc[repair_observations["validation_profit_factor"] > float(anchor_best["validation_profit_factor"])]
    better_density = repair_observations.loc[repair_observations["validation_trades_per_day"] > float(anchor_best["validation_trades_per_day"])]
    return {
        "kpi_number_parity": {
            "frontier02c_oos_net": numeric(anchor_best["oos_net_profit"]),
            "frontier02d_oos_net": numeric(parent_best["oos_net_profit"]),
            "frontier02c_report_sha256": sha256_file(Path("stages") / STAGE_ID / "03_reviews" / f"{ANCHOR_RUN_ID}_report.md"),
            "frontier02d_report_sha256": sha256_file(Path("stages") / STAGE_ID / "03_reviews" / f"{PARENT_RUN_ID}_report.md"),
        },
        "grok_degradation_claim_check": {
            "all_14_repair_rows_below_c_pf_and_density": bool(len(repair_observations) == 14 and len(better_pf) == 0 and len(better_density) == 0),
            "repair_observation_rows": int(len(repair_observations)),
            "repair_rows_above_c_validation_pf": int(len(better_pf)),
            "repair_rows_above_c_validation_density": int(len(better_density)),
            "classification": "reject_overbroad_degradation_claim" if len(better_pf) or len(better_density) else "accepted",
        },
        "repair_axis_identity": {
            "frontier02d_label_id": "ret_m1c",
            "frontier02d_axis": "label_training_repair",
            "frontier02e_axis": "frozen_02c_decision_layer_no_new_onnx",
            "classification": "accepted_new_information_axis",
        },
        "replay_infrastructure": {
            "frontier02c_top_replay_exists": path_exists(ANCHOR_REPLAY),
            "frontier02d_top_replay_exists": path_exists(PARENT_ROOT / "top_repair_signal_replay.csv"),
            "frontier02c_replay_rows": csv_row_count(ANCHOR_REPLAY),
            "frontier02d_replay_rows": csv_row_count(PARENT_ROOT / "top_repair_signal_replay.csv"),
            "frontier02c_decision_rows": csv_row_count(ANCHOR_SUMMARY),
            "frontier02d_decision_rows": csv_row_count(PARENT_SUMMARY),
        },
        "diagnostic_result": {
            "decision_rows": int(len(summary)),
            "go_rule_rows": int(len(go_rows)),
            "next_condition": "frontier02F_capped_repair_allowed" if len(go_rows) else "prepare_stage_closeout",
        },
        "claim_boundary": {
            "completion": "not_claimed",
            "selected_baseline": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    }


def build_grok_advice_classification(local_verification: dict[str, Any], go_rows: pd.DataFrame) -> dict[str, Any]:
    return {
        "trigger_reason": "goal requires Grok second opinion before expensive WFO/MT5(목표가 비싼 WFO/MT5 전 그록 2차 의견을 요구)",
        "review_size": "medium",
        "prompt_identity": {
            "path": (GROK_REVIEW_ROOT / "prompt.md").as_posix(),
            "sha256": sha256_file(GROK_REVIEW_ROOT / "prompt.md") if path_exists(GROK_REVIEW_ROOT / "prompt.md") else None,
        },
        "grok_output_identity": {
            "path": (GROK_REVIEW_ROOT / "clean_output.md").as_posix(),
            "sha256": sha256_file(GROK_REVIEW_ROOT / "clean_output.md") if path_exists(GROK_REVIEW_ROOT / "clean_output.md") else None,
        },
        "accepted": [
            "Do not run WFO/MT5 yet(WFO/MT5 아직 실행 금지)",
            "Run frozen frontier02C decision-layer diagnostic(고정 frontier02C 결정층 진단 실행)",
            "Keep frontier02C as seed observation only(frontier02C는 씨앗 관찰로만 유지)",
            "Keep frontier02D as negative repair memory(frontier02D는 부정 수리 기억으로 유지)",
        ],
        "rejected": [
            "All 14 frontier02D repair observation rows are below frontier02C on both PF and density(14개 수리 관찰 행 모두 PF와 밀도에서 C보다 낮다는 주장)",
        ]
        if local_verification["grok_degradation_claim_check"]["classification"] == "reject_overbroad_degradation_claim"
        else [],
        "needs_local_verification": [
            "Go/no-go rule after diagnostic(진단 후 진행/중단 규칙)",
            "Loss attribution bucket interpretation(손실 귀속 버킷 해석)",
        ],
        "final_codex_direction": "prepare_stage_closeout" if len(go_rows) == 0 else "frontier02F_capped_decision_layer_repair",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def build_manifest(
    paths: dict[str, Path],
    anchor_best: dict[str, Any],
    parent_best: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    go_rows: pd.DataFrame,
    local_verification: dict[str, Any],
    advice: dict[str, Any],
) -> dict[str, Any]:
    outputs = {name: artifact_record(path) for name, path in paths.items()}
    outputs["report"] = artifact_record(REPORT_PATH)
    status = "completed_no_go_decision_layer_diagnostic_no_authority" if len(go_rows) == 0 else "completed_go_rule_decision_layer_diagnostic_no_authority"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "anchor_run_id": ANCHOR_RUN_ID,
        "next_run_id": NEXT_NOGO_RUN_ID if len(go_rows) == 0 else NEXT_GO_RUN_ID,
        "status": status,
        "created_at_utc": utc_now(),
        "script_path": "stage_pipelines/stage_frontier_02/frontier02e_frozen_02c_decision_layer_diagnostic.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_02/frontier02e_frozen_02c_decision_layer_diagnostic.py")),
        "inputs": {
            "anchor_replay_path": ANCHOR_REPLAY.as_posix(),
            "anchor_replay_sha256": sha256_file(ANCHOR_REPLAY),
            "model_input_dataset_path": MODEL_INPUT_DATASET.as_posix(),
            "model_input_dataset_sha256": sha256_file(MODEL_INPUT_DATASET),
            "feature_order_path": FEATURE_ORDER.as_posix(),
            "feature_order_sha256": sha256_file(FEATURE_ORDER),
            "grok_review_output": (GROK_REVIEW_ROOT / "clean_output.md").as_posix(),
            "grok_review_output_sha256": sha256_file(GROK_REVIEW_ROOT / "clean_output.md") if path_exists(GROK_REVIEW_ROOT / "clean_output.md") else None,
        },
        "diagnostic_contract": {
            "anchor_candidate_id": anchor_best["candidate_id"],
            "parent_negative_repair_candidate_id": parent_best["candidate_id"],
            "no_new_onnx": True,
            "no_retrain": True,
            "selector_scope": "validation_rank_only_oos_diagnostic",
            "go_rule": "OOS PF >= 1.2, density 5-10/day, OOS DD pass, OOS net > 0",
        },
        "outputs": outputs,
        "best_validation_rank": json_ready(top),
        "go_rule_rows": int(len(go_rows)),
        "decision_rows": int(len(summary)),
        "local_verification": local_verification,
        "grok_advice_classification": advice,
        "external_verification_status": "out_of_scope_by_claim_no_mt5",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def build_report(
    anchor_best: dict[str, Any],
    parent_best: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    go_rows: pd.DataFrame,
    loss_attribution: pd.DataFrame,
    local_verification: dict[str, Any],
    advice: dict[str, Any],
) -> str:
    next_run = NEXT_NOGO_RUN_ID if len(go_rows) == 0 else NEXT_GO_RUN_ID
    worst_loss_buckets = (
        loss_attribution.sort_values("net_profit").head(5)[["bucket_type", "bucket_value", "trade_count", "net_profit", "profit_factor"]].to_dict("records")
        if not loss_attribution.empty
        else []
    )
    return f"""# frontier02E Frozen 02C Decision-Layer Diagnostic Report(전선02E 고정 02C 결정층 진단 보고)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{'completed_no_go_decision_layer_diagnostic_no_authority(결정층 진단 완료, 진행 조건 없음, 권위 없음)' if len(go_rows) == 0 else 'completed_go_rule_decision_layer_diagnostic_no_authority(결정층 진단 완료, 진행 조건 있음, 권위 없음)'}`
- anchor(앵커): `{anchor_best['candidate_id']}`
- decision_rows(결정 행): `{len(summary)}`
- go_rule_rows(진행 조건 행): `{len(go_rows)}`
- next_run(다음 실행): `{next_run}`

## Boundary(경계)

이번 실행(run, 실행)은 Grok pre-expensive review(비싼 검증 전 그록 검토)를 로컬 검증(local verification, 로컬 검증)한 뒤, frontier02C(전선02C) 고정 확률 출력(probability output, 확률 출력)만 사용한 decision-layer diagnostic(결정층 진단)입니다. 새 학습(retrain, 재학습), 새 ONNX(온엑스), WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증)는 없습니다.

## Grok Advice Classification(그록 조언 분류)

- accepted(수용): frozen 02C decision-layer diagnostic(고정 02C 결정층 진단), no WFO/MT5 yet(WFO/MT5 아직 금지)
- rejected(거절): `{'; '.join(advice['rejected']) if advice['rejected'] else 'none(없음)'}`
- final Codex direction(최종 Codex 방향): `{advice['final_codex_direction']}`

## Anchor vs Repair(앵커와 수리 비교)

- frontier02C validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(anchor_best['validation_profit_factor'])}` / `{fmt(anchor_best['validation_trades_per_day'])}/day` / `{fmt(anchor_best['validation_max_drawdown_percent'])}%`
- frontier02C OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `{fmt(anchor_best['oos_profit_factor'])}` / `{fmt(anchor_best['oos_trades_per_day'])}/day` / `{fmt(anchor_best['oos_max_drawdown_percent'])}%`
- frontier02D validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(parent_best['validation_profit_factor'])}` / `{fmt(parent_best['validation_trades_per_day'])}/day` / `{fmt(parent_best['validation_max_drawdown_percent'])}%`
- frontier02D OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `{fmt(parent_best['oos_profit_factor'])}` / `{fmt(parent_best['oos_trades_per_day'])}/day` / `{fmt(parent_best['oos_max_drawdown_percent'])}%`

## Best Diagnostic Rank(진단 순위 1위)

- candidate_id(후보 ID): `{top['candidate_id']}`
- score_mode(점수 방식): `{top['score_mode']}`
- threshold/margin/cooldown(임계값/마진/쿨다운): `{fmt(top['probability_threshold'])}` / `{fmt(top['probability_margin'])}` / `{top['cooldown_bars']}`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{fmt(top['validation_net_profit'])}` / `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{fmt(top['oos_net_profit'])}` / `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`
- joint_pass_count(동시 통과 수): validation(검증) `{top['validation_joint_pass_count']}`, OOS(표본외) `{top['oos_joint_pass_count']}`

## Go/No-Go Read(진행/중단 판독)

Go rule(진행 규칙)은 OOS PF(표본외 수익 팩터) `>=1.2`, density(밀도) `5-10/day`, OOS DD pass(표본외 손실폭 통과), OOS net(표본외 순수익) `>0`입니다. 이번 진단의 go_rule_rows(진행 조건 행)는 `{len(go_rows)}`개입니다.

Effect(효과): `{('frontier02F에서 capped decision-layer repair(상한 있는 결정층 수리)를 한 번만 실행할 수 있습니다.' if len(go_rows) else 'frontier02C는 preserved clue(보존 단서), frontier02D/02E는 negative memory(부정 기억)로 stage closeout(단계 마감)을 준비하는 쪽이 맞습니다.')}`

## Loss Attribution(손실 귀속)

Worst OOS buckets(표본외 최악 버킷): `{json.dumps(worst_loss_buckets, ensure_ascii=False)}`

## Local Verification(로컬 검증)

- KPI parity(KPI 숫자 일치): frontier02C OOS net `{fmt(local_verification['kpi_number_parity']['frontier02c_oos_net'])}`, frontier02D OOS net `{fmt(local_verification['kpi_number_parity']['frontier02d_oos_net'])}`
- Grok degradation claim(그록 열화 주장): `{local_verification['grok_degradation_claim_check']['classification']}`
- replay rows(재생 행): C `{local_verification['replay_infrastructure']['frontier02c_replay_rows']}`, D `{local_verification['replay_infrastructure']['frontier02d_replay_rows']}`
- decision rows(결정 행): C `{local_verification['replay_infrastructure']['frontier02c_decision_rows']}`, D `{local_verification['replay_infrastructure']['frontier02d_decision_rows']}`

## Claim Boundary(주장 경계)

Allowed claim(허용 주장): Grok review captured(그록 검토 기록), frozen 02C diagnostic completed(고정 02C 진단 완료), no-go/go-rule diagnostic read(진행/중단 진단 판독).

Forbidden claim(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), selected candidate(선택 후보).
"""


def verify_replay_alignment(frame: pd.DataFrame, replay: pd.DataFrame) -> None:
    if len(frame) != len(replay):
        raise ValueError(f"Replay row count mismatch: frame={len(frame)} replay={len(replay)}")
    frame_ts = pd.to_datetime(frame["timestamp"], utc=True).astype(str)
    replay_ts = pd.to_datetime(replay["timestamp"], utc=True).astype(str)
    if not frame_ts.equals(replay_ts):
        raise ValueError("Replay timestamp order does not match model input dataset.")


def best_rank(summary: pd.DataFrame) -> dict[str, Any]:
    return (
        summary.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .iloc[0]
        .to_dict()
    )


def artifact_record(path: Path) -> dict[str, Any]:
    return {"path": path.as_posix(), "sha256": sha256_file(path)}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def csv_row_count(path: Path) -> int:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def numeric(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def fmt(value: Any) -> str:
    number = numeric(value)
    if number is None:
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())

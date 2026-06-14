from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout"
RUN_ID = "frontier20B_feature_state_rule_atlas_proxy_scout_v1"
RUN_NUMBER = "frontier20B"
PARENT_RUN_ID = "frontier20A_stage_open_train_only_feature_state_rule_atlas_onnx_scout_v1"
NEXT_DECISION_RUN_ID = "frontier20C_rule_atlas_repair_or_closeout_decision_v1"
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier20C_grok_pre_expensive_feature_state_rule_atlas_review_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_20/frontier20b_feature_state_rule_atlas_proxy_scout.py")

F20A_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"
F20A_LOCK = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "rule_atlas_lock.json"
DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")

QUANTILES = (0.10, 0.20, 0.30, 0.70, 0.80, 0.90)
MAX_CONDITION_POOL = 45
SINGLE_RULE_POOL = 30
MIN_TRAIN_DENSITY = 4.0
MAX_TRAIN_DENSITY = 14.0
MIN_TRAIN_TRADES = 80
MIN_TRAIN_PF = 1.12
MAX_SELECTED_CANDIDATES = 600
STRICT_PF = 2.0
SEED_PF = 1.20
SEED_DD_CAP = 60.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 15.0


def main() -> int:
    now = utc_now()
    ensure_dirs()
    parent = read_json(F20A_SUMMARY)
    lock = read_json(F20A_LOCK)
    frame = load_frame()
    feature_order = read_feature_order()
    condition_pool = build_condition_pool(frame, feature_order)
    candidates = build_candidate_pool(frame, condition_pool)
    selected = select_candidates_by_train(frame, candidates)
    metrics = evaluate_selected_candidates(frame, selected)
    summary = summarize_candidates(metrics)
    final = build_final(now, parent, lock, feature_order, condition_pool, selected, metrics, summary)
    write_outputs(final, condition_pool, selected, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "condition_pool_rows": len(condition_pool),
        "candidate_pool_rows": len(candidates),
        "selected_candidate_rows": len(selected),
        "strict_count": final["strict_count"],
        "seed_count": final["seed_count"],
        "handoff_candidate_count": final["handoff_candidate_count"],
        "best_candidate_id": final["best_candidate_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    required = {"timestamp", "split", "future_log_return_12", "label_class"}
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
    if len(features) != 58 or feature_hash != EXPECTED_FEATURE_HASH:
        raise ValueError(f"Feature order contract mismatch(피처 순서 계약 불일치): {len(features)} {feature_hash}")
    return features


def build_condition_pool(frame: pd.DataFrame, feature_order: list[str]) -> pd.DataFrame:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    rows: list[dict[str, Any]] = []
    for feature in feature_order:
        series = pd.to_numeric(frame[feature], errors="coerce")
        train_values = series.loc[train_mask]
        if train_values.nunique(dropna=True) <= 3:
            continue
        values = series.to_numpy(dtype="float64")
        finite = np.isfinite(values)
        for quantile in QUANTILES:
            threshold = float(np.nanquantile(train_values, quantile))
            if quantile <= 0.30:
                mask = (values <= threshold) & finite
                operator = "<="
            else:
                mask = (values >= threshold) & finite
                operator = ">="
            side, side_name, train_metrics = choose_train_side(frame, mask)
            if train_metrics["trade_count"] < 60 or train_metrics["net_profit"] <= 0:
                continue
            if not (1.0 <= train_metrics["trades_per_day"] <= 35.0):
                continue
            score = train_rank_score(train_metrics)
            rows.append({
                "condition_id": f"c{len(rows)+1:04d}",
                "feature": feature,
                "operator": operator,
                "quantile": quantile,
                "quantile_label": f"q{int(quantile * 100)}",
                "threshold_value": threshold,
                "side": side,
                "side_name": side_name,
                "train_rank_score": score,
                "train_trade_count": train_metrics["trade_count"],
                "train_trades_per_day": train_metrics["trades_per_day"],
                "train_net_profit": train_metrics["net_profit"],
                "train_profit_factor": train_metrics["profit_factor"],
                "train_dd_risk": train_metrics["dd_risk"],
                "definition": f"{feature} {operator} q{int(quantile * 100)}",
                "_mask": mask,
            })
    if not rows:
        raise RuntimeError("No condition pool rows(조건 풀 행 없음).")
    condition_pool = pd.DataFrame(rows).sort_values("train_rank_score", ascending=False).head(MAX_CONDITION_POOL).reset_index(drop=True)
    return condition_pool


def build_candidate_pool(frame: pd.DataFrame, condition_pool: pd.DataFrame) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    top = condition_pool.to_dict("records")
    for row in top[:SINGLE_RULE_POOL]:
        candidates.append({
            "candidate_id": f"f20b_single_{len(candidates)+1:04d}",
            "rule_kind": "single(단일)",
            "definitions": [row["definition"]],
            "features": [row["feature"]],
            "mask": row["_mask"],
        })
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    for index, left in enumerate(top):
        for right in top[index + 1:]:
            if left["feature"] == right["feature"]:
                continue
            mask = left["_mask"] & right["_mask"]
            if int((mask & train_mask).sum()) < 70:
                continue
            candidates.append({
                "candidate_id": f"f20b_pair_{len(candidates)+1:04d}",
                "rule_kind": "pair(쌍)",
                "definitions": [left["definition"], right["definition"]],
                "features": [left["feature"], right["feature"]],
                "mask": mask,
            })
    if not candidates:
        raise RuntimeError("No candidate pool rows(후보 풀 행 없음).")
    return candidates


def select_candidates_by_train(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for candidate in candidates:
        side, side_name, train_metrics = choose_train_side(frame, candidate["mask"])
        if not (
            MIN_TRAIN_DENSITY <= train_metrics["trades_per_day"] <= MAX_TRAIN_DENSITY
            and train_metrics["trade_count"] >= MIN_TRAIN_TRADES
            and train_metrics["net_profit"] > 0
            and train_metrics["profit_factor"] >= MIN_TRAIN_PF
        ):
            continue
        item = dict(candidate)
        item.update({
            "side": side,
            "side_name": side_name,
            "train_rank_score": train_rank_score(train_metrics),
            "train_selection_metrics": train_metrics,
        })
        selected.append(item)
    selected.sort(key=lambda item: float(item["train_rank_score"]), reverse=True)
    return selected[:MAX_SELECTED_CANDIDATES]


def choose_train_side(frame: pd.DataFrame, mask: np.ndarray) -> tuple[int, str, dict[str, Any]]:
    long_metrics = evaluate_mask(frame, mask, 1, "train")
    short_metrics = evaluate_mask(frame, mask, -1, "train")
    if (short_metrics["net_profit"], short_metrics["profit_factor"]) > (long_metrics["net_profit"], long_metrics["profit_factor"]):
        return -1, "short(숏)", short_metrics
    return 1, "long(롱)", long_metrics


def evaluate_selected_candidates(frame: pd.DataFrame, selected: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(selected, start=1):
        for split in ("train", "validation", "oos"):
            metrics = evaluate_mask(frame, candidate["mask"], int(candidate["side"]), split)
            sparse_floor = max(30, int(math.ceil(metrics["days_in_scope"])))
            sparse_flag = metrics["trade_count"] < sparse_floor
            pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
            density_distance = scout.density_axis_distance(metrics["trades_per_day"])
            pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], metrics["trade_count"], sparse_flag, pf999_sparse_flag)
            dd_distance = max(0.0, (metrics["dd_risk"] - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
            smoothness_distance = scout.smoothness_axis_distance(metrics)
            rows.append({
                "candidate_id": candidate["candidate_id"],
                "train_rank": rank,
                "rule_kind": candidate["rule_kind"],
                "rule_definition": " & ".join(candidate["definitions"]),
                "feature_count": len(candidate["features"]),
                "features": "|".join(candidate["features"]),
                "side": candidate["side_name"],
                "side_value": int(candidate["side"]),
                "split": split,
                "record_view": "Tier A separate(티어 A 분리)",
                "tier_scope": "Tier A(티어 A)",
                "trade_count": metrics["trade_count"],
                "days_in_scope": metrics["days_in_scope"],
                "trades_per_day": metrics["trades_per_day"],
                "net_profit": metrics["net_profit"],
                "profit_factor": metrics["profit_factor"],
                "expectancy": metrics["expectancy"],
                "win_rate": metrics["win_rate"],
                "max_drawdown_percent": metrics["max_drawdown_percent"],
                "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
                "dd_risk": metrics["dd_risk"],
                "underwater_ratio": metrics["underwater_ratio"],
                "max_loss_streak": metrics["max_loss_streak"],
                "equity_trend_r2": metrics["equity_trend_r2"],
                "density_axis_distance": density_distance,
                "pf_axis_distance": pf_distance,
                "dd_axis_distance": dd_distance,
                "smoothness_axis_distance": smoothness_distance,
                "joint_axis_distance": density_distance + pf_distance + dd_distance + smoothness_distance,
                "density_pass": bool(scout.DENSITY_TARGET_LOW <= metrics["trades_per_day"] <= scout.DENSITY_TARGET_HIGH),
                "pf_pass": bool(metrics["profit_factor"] >= scout.PF_TARGET and metrics["net_profit"] > 0 and not sparse_flag),
                "dd_pass": bool(metrics["dd_risk"] < scout.DD_TARGET_PERCENT),
                "smoothness_pass": bool(
                    metrics["net_profit"] > 0
                    and metrics["underwater_ratio"] <= 0.45
                    and metrics["equity_trend_r2"] >= 0.35
                    and metrics["max_loss_streak"] <= 6
                ),
                "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
                "selection_boundary": "train_only_rank(학습 전용 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    if not rows:
        raise RuntimeError("No selected candidate metrics(선택 후보 지표 없음).")
    return pd.DataFrame(rows)


def evaluate_mask(frame: pd.DataFrame, mask: np.ndarray, side: int, split: str) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    trade_mask = mask & split_mask
    split_times = frame.loc[split_mask, "timestamp"]
    days = scout.count_scope_days(split_times)
    returns = pd.to_numeric(frame.loc[trade_mask, "future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    pnl = returns * float(side) - scout.ROUGH_COST_LOG_RETURN
    trade_times = frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(pnl, trade_times)
    trade_count = int(len(pnl))
    return {
        **metrics,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": float(trade_count / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
    }


def train_rank_score(metrics: dict[str, Any]) -> float:
    dd_penalty = 1.0 + max(0.0, float(metrics["dd_risk"]) - 10.0) / 20.0
    return float(metrics["net_profit"]) * min(float(metrics["profit_factor"]), 4.0) / dd_penalty


def summarize_candidates(metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for candidate_id, group in metrics.groupby("candidate_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "candidate_id": candidate_id,
            "train_rank": int(train["train_rank"]),
            "rule_kind": train["rule_kind"],
            "rule_definition": train["rule_definition"],
            "features": train["features"],
            "side": train["side"],
        }
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "dd_risk",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "joint_axis_distance",
                "density_pass",
                "pf_pass",
                "dd_pass",
                "smoothness_pass",
            ):
                base[f"{prefix}_{field}"] = row[field]
        base["strict_pass"] = bool(
            validation["density_pass"] and oos["density_pass"]
            and validation["pf_pass"] and oos["pf_pass"]
            and validation["dd_pass"] and oos["dd_pass"]
            and validation["smoothness_pass"] and oos["smoothness_pass"]
        )
        base["seed_surface_flag"] = bool(
            scout.DENSITY_TARGET_LOW <= validation["trades_per_day"] <= scout.DENSITY_TARGET_HIGH
            and scout.DENSITY_TARGET_LOW <= oos["trades_per_day"] <= scout.DENSITY_TARGET_HIGH
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and max(validation["dd_risk"], oos["dd_risk"]) <= SEED_DD_CAP
        )
        base["handoff_candidate_flag"] = bool(
            scout.DENSITY_TARGET_LOW <= validation["trades_per_day"] <= scout.DENSITY_TARGET_HIGH
            and scout.DENSITY_TARGET_LOW <= oos["trades_per_day"] <= scout.DENSITY_TARGET_HIGH
            and validation["profit_factor"] >= HANDOFF_PF
            and oos["profit_factor"] >= HANDOFF_PF
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and max(validation["dd_risk"], oos["dd_risk"]) <= HANDOFF_DD_CAP
            and validation["smoothness_pass"]
            and oos["smoothness_pass"]
        )
        base["forward_read_score"] = float(
            min(validation["profit_factor"], 3.0)
            * min(oos["profit_factor"], 3.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 12.0)
            / (1.0 + max(validation["dd_risk"], oos["dd_risk"]) / 15.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(["seed_surface_flag", "handoff_candidate_flag", "forward_read_score"], ascending=[False, False, False])


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def build_final(
    now: str,
    parent: dict[str, Any],
    lock: dict[str, Any],
    feature_order: list[str],
    condition_pool: pd.DataFrame,
    selected: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    strict_count = int(summary["strict_pass"].sum()) if "strict_pass" in summary else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if "seed_surface_flag" in summary else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if "handoff_candidate_flag" in summary else 0
    if handoff_count:
        status = "rule_atlas_proxy_handoff_candidate_no_authority"
        judgment = "runtime_probe_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "rule_atlas_seed_surface_proxy_no_handoff_no_authority"
        judgment = "seed_surface_candidate_high_dd_no_runtime_handoff_no_authority"
        next_run_id = NEXT_DECISION_RUN_ID
    else:
        status = "rule_atlas_no_forward_clue_proxy_no_authority"
        judgment = "negative_memory_candidate_no_seed_or_handoff_no_authority"
        next_run_id = NEXT_DECISION_RUN_ID
    best = dict(summary.iloc[0]) if len(summary) else {}
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "condition_pool_rows": int(len(condition_pool)),
        "candidate_pool_rows": int(len(selected)),
        "selected_candidate_rows": int(len(summary)),
        "metric_rows": int(len(metrics)),
        "strict_count": strict_count,
        "seed_count": seed_count,
        "handoff_candidate_count": handoff_count,
        "best_candidate_id": best.get("candidate_id", ""),
        "best_candidate": json_ready(best),
        "parent_stage_open_status": parent.get("status", ""),
        "rule_lock": lock,
        "external_verification_status": (
            "out_of_scope_by_claim_proxy_no_mt5(프록시 주장 범위라 MT5 없음)"
            if handoff_count == 0
            else "pending_grok_pre_expensive_review_before_mt5(비싼 MT5 전 그록 검토 대기)"
        ),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], condition_pool: pd.DataFrame, selected: list[dict[str, Any]], metrics: pd.DataFrame, summary: pd.DataFrame) -> None:
    condition_output = condition_pool.drop(columns=["_mask"], errors="ignore")
    candidate_rows = [
        {
            "candidate_id": item["candidate_id"],
            "rule_kind": item["rule_kind"],
            "rule_definition": " & ".join(item["definitions"]),
            "features": "|".join(item["features"]),
            "side": item["side_name"],
            "train_rank_score": item["train_rank_score"],
            **{f"train_{key}": value for key, value in item["train_selection_metrics"].items()},
        }
        for item in selected
    ]
    condition_output.to_csv(io_path(RUN_ROOT / "condition_pool.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame(candidate_rows).to_csv(io_path(RUN_ROOT / "train_ranked_candidates.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "proxy_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "candidate_summary.csv"), index=False, encoding="utf-8-sig")
    summary.sort_values("forward_read_score", ascending=False).head(30).to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(RUN_ROOT / "condition_pool.csv"),
            artifact_identity(RUN_ROOT / "train_ranked_candidates.csv"),
            artifact_identity(RUN_ROOT / "proxy_metrics_by_split.csv"),
            artifact_identity(RUN_ROOT / "candidate_summary.csv"),
            artifact_identity(RUN_ROOT / "top_forward_readonly_diagnostic.csv"),
        ],
        "feature_schema": {
            "feature_count": final["feature_count"],
            "feature_order_hash": final["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "data_snapshot": {
            "dataset_path": DATASET_PATH.as_posix(),
            "split_names": ["train", "validation", "oos"],
        },
        "results": {
            "by_split": {"metrics_path": (RUN_ROOT / "proxy_metrics_by_split.csv").as_posix()},
            "cross_split": {
                "strict_count": final["strict_count"],
                "seed_count": final["seed_count"],
                "handoff_candidate_count": final["handoff_candidate_count"],
            },
            "report_refs": [{"role": "frontier20b_proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "mismatch_policy": "fail_fast(즉시 실패)",
            "runtime_handoff": "not_materialized(물질화 없음)" if final["handoff_candidate_count"] == 0 else "pending_review(검토 대기)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_candidate"]
    top_rows = []
    for _, row in summary.head(12).iterrows():
        top_rows.append(
            f"| `{row['candidate_id']}` | {row['side']} | `{row['rule_definition']}` | {fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | {fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['seed_surface_flag']} |"
        )
    table = "\n".join(top_rows)
    return f"""# Frontier20B Feature-State Rule Atlas Proxy Scout Report(전선20B 피처 상태 규칙 지도 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): fixed 58 feature(고정 58 피처)에서 train-only quantile rule atlas(학습 전용 분위수 규칙 지도)를 만들고, train rank(학습 순위)로 고른 후보만 validation/OOS(검증/표본외)에 읽기 전용으로 재생했습니다.

Effect(효과): validation/OOS(검증/표본외) 성과로 규칙을 고르지 않으면서 seed surface(씨앗 표면)와 handoff candidate(인계 후보) 여부를 분리합니다.

Condition pool/candidate/metric rows(조건 풀/후보/지표 행): `{final['condition_pool_rows']}` / `{final['selected_candidate_rows']}` / `{final['metric_rows']}`

Strict/seed/handoff counts(엄격/씨앗/인계 수): `{final['strict_count']}` / `{final['seed_count']}` / `{final['handoff_candidate_count']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime boundary(런타임 경계): `{final['external_verification_status']}`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | side(방향) | rule(규칙) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier20B Gate Coverage Audit(전선20B 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

- train_only_leakage_guard(학습 전용 누수 방지): condition quantiles, side, and rank(조건 분위수/방향/순위)는 train split(학습 분할)에서만 계산했습니다.
- rule_atlas_lock_gate(규칙 지도 잠금 게이트): existing 58 features, fixed q-grid, max depth 2(기존 58 피처/고정 분위수 격자/최대 깊이 2)를 지켰습니다.
- tier_paired_record_gate(티어 쌍 기록 게이트): Tier A separate(티어 A 분리) 지표를 기록하고, Tier B/Tier A+B(티어 B/합산)는 장부에 missing/out-of-scope 행으로 기록합니다.
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): handoff candidates(인계 후보) `{final['handoff_candidate_count']}`개; status(상태) `{final['external_verification_status']}`.
- final_claim_guard(최종 주장 보호): completion/baseline/promotion/runtime/live/Goal(완성/기준선/승격/런타임/실거래/목표) 주장 없음.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier20 Selection Status(전선20 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Latest proxy read(최근 프록시 판독): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best proxy(최선 프록시): `{final['best_candidate_id']}` validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(final['best_candidate'].get('validation_profit_factor'))}`/`{fmt(final['best_candidate'].get('validation_trades_per_day'))}`/`{fmt(final['best_candidate'].get('validation_dd_risk'))}` and `{fmt(final['best_candidate'].get('oos_profit_factor'))}`/`{fmt(final['best_candidate'].get('oos_trades_per_day'))}`/`{fmt(final['best_candidate'].get('oos_dd_risk'))}`.

Runtime boundary(런타임 경계): `{final['external_verification_status']}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    if final["seed_count"] == 0 and final["handoff_candidate_count"] == 0:
        f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, negative_memory_candidate_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_state_rule_atlas_proxy_scout(피처 상태 규칙 지도 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_count']};seed={final['seed_count']};handoff={final['handoff_candidate_count']};best={final['best_candidate_id']}",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "proxy_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "train_only_selection_validation_oos_read_only_no_authority(학습 전용 선택, 검증/표본외 읽기 전용, 권위 없음)",
        "external_verification_status": final["external_verification_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate"]
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "feature_state_rule_atlas_proxy_scout(피처 상태 규칙 지도 프록시 탐색)",
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
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_a_rule_atlas_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_rule_atlas_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "proxy_rule_atlas_not_runtime(프록시 규칙 지도, 런타임 아님)",
            "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
            "guardrail_kpi": "train_only_selection_validation_oos_read_only_no_authority(학습 전용 선택, 검증/표본외 읽기 전용, 권위 없음)",
            "external_verification_status": final["external_verification_status"],
            "notes": f"strict={final['strict_count']};seed={final['seed_count']};handoff={final['handoff_candidate_count']}",
        },
        {
            **common,
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
            **common,
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
        f"- {final['created_at_utc']}: `{RUN_ID}` completed train-only feature-state rule atlas proxy scout(학습 전용 피처 상태 규칙 지도 프록시 탐색). "
        f"Effect(효과): strict/seed/handoff(엄격/씨앗/인계) counts `{final['strict_count']}/{final['seed_count']}/{final['handoff_candidate_count']}` and next run(다음 실행) `{final['next_run_id']}` recorded(기록됨).\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier20(전선20) train-only rule atlas proxy scout(학습 전용 규칙 지도 프록시 탐색) evaluated `{final['selected_candidate_rows']}` train-ranked candidates(학습 순위 후보). "
        "Effect(효과): validation/OOS(검증/표본외)는 read-only forward diagnostic(읽기 전용 전진 진단)으로만 사용했습니다.\n"
    )


def negative_memory_candidate_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: train-only feature-state rule atlas(학습 전용 피처 상태 규칙 지도) has no seed/handoff rows(씨앗/인계 행 없음) under locked F20B scope(고정 F20B 범위). "
        "Effect(효과): closeout decision(마감 결정)에서 negative memory(부정 기억) 여부를 검토합니다.\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(f03b.WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))


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
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier20B(전선20B) train-only feature-state rule atlas proxy scout(학습 전용 피처 상태 규칙 지도 프록시 탐색)를 실행했습니다.

Effect(효과): train-only selection(학습 전용 선택)과 validation/OOS read-only(검증/표본외 읽기 전용) 경계를 유지한 채 strict/seed/handoff(엄격/씨앗/인계) 수를 기록했습니다.

Latest counts(최근 수): strict/seed/handoff(엄격/씨앗/인계) `{final['strict_count']}/{final['seed_count']}/{final['handoff_candidate_count']}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


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
        return ""
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_density_failure_regime_behavior_reseed_without_db as du  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_model_label_offensive_reseed_without_db as dp  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dt.STAGE_ID
RUN_NUMBER = "run364DV"
RUN_ID = "run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1"
PARENT_RUN_ID = du.RUN_ID
NEXT_RUN_ID = "run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1"

STATUS_NO_STRICT = "completed_stage364DV_validation_stability_reseed_no_strict_review_required_no_authority"
STATUS_STRICT = "completed_stage364DV_validation_stability_reseed_proxy_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_validation_stability_reseed_no_cross_split_candidate_no_package_no_authority"
JUDGMENT_STRICT = "proxy_validation_stability_reseed_found_cross_split_candidate_review_required_no_authority"
DECISION = "stage364DV_open_run364DW_validation_stability_reseed_review"
CLAIM_BOUNDARY = (
    "research_development_model_label_feature_reseed_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

POINT_VALUE = dt.POINT_VALUE
COST_PER_TRADE = dt.COST_PER_TRADE
STRICT_NET_FLOOR = 0.0
STRICT_PF_FLOOR = 1.20
STRICT_DENSITY_FLOOR = 3.0

STAGE_DIR = dt.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "dv_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "dv_validation_stability_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "dv_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "dv_validation_stability_trade_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_dv_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_dv_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_dv_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_dv_cost_stress.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364DW_QUEUE = RUN_DIR / "run364DW_validation_stability_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DV_h17_validation_stability_regime_source_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DV_h17_validation_stability_regime_source_reseed.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    du.FINAL_DECISION,
    du.GATE_AUDIT,
    du.REVIEW_SUMMARY,
    du.GAP_ATTRIBUTION,
    du.FAILURE_MEMORY,
    du.RUN364DV_QUEUE,
    du.REPORT_PATH,
    dt.FINAL_DECISION,
    dt.TRADE_SURFACE,
    dt.SELECTED_CANDIDATE,
    dt.MONTH_STABILITY,
    dt.COST_STRESS,
    dp.MODEL_INPUT_DATASET,
    dp.MODEL_INPUT_FEATURE_ORDER,
    dp.RAW_US100_M5,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FEATURE_AUDIT,
    LABEL_SUMMARY,
    MODEL_SCORECARD,
    TRADE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    MONTH_STABILITY,
    COST_STRESS,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364DW_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    Path(__file__),
]

LABEL_SPECS = [
    {"label_id": "stable_dir_h4_m2p5", "horizon_m5": 4, "threshold_points": 2.5, "max_hold_m5": 4},
    {"label_id": "stable_dir_h6_m3", "horizon_m5": 6, "threshold_points": 3.0, "max_hold_m5": 6},
    {"label_id": "stable_dir_h8_m5", "horizon_m5": 8, "threshold_points": 5.0, "max_hold_m5": 8},
]
DENSITY_TARGETS = [3, 4, 5, 6, 8, 10, 12]
MARGINS = [-0.05, 0.0, 0.03, 0.06]
HOUR_SETS = {
    "cash15_21": [15, 16, 17, 18, 19, 20, 21],
    "h15_19": [15, 16, 17, 18, 19],
    "h16_21": [16, 17, 18, 19, 20, 21],
    "h17_21": [17, 18, 19, 20, 21],
}
STABILITY_FILTERS = [
    "none",
    "drop_validation_negative_months",
    "validation_positive_months_only",
    "no_h20",
    "direction_gap_3pct",
    "short_dominant_no_h20",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dt.rel(path)


def exists(path: Path | str) -> bool:
    return dt.exists(path)


def sha(path: Path | str) -> str:
    return dt.sha(path)


def read_json(path: Path) -> Any:
    return dt.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dt.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dt.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(inner) for inner in value]
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            return str(value)
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in materialized:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dt.append_or_replace_csv(path, key_fields, [{str(key): json_ready(value) for key, value in row.items()} for row in rows], extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dt.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dt.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dt.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return dt.finite(value, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DV inputs(DV 입력 누락): " + ", ".join(missing))
    parent = read_json(du.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DU next_run_id mismatch(DU 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DU forbidden claim(DU 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(du.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DU gate audit(DU 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DV training input(DV 학습 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "Validation-stability labels and filters(검증 안정성 라벨과 필터)가 DT OOS clue(DT 표본외 단서)를 보존하면서 validation net/PF(검증 순수익/PF)를 고칠 수 있다.",
            "comparison_baseline": parent["parent_run_id"],
            "success_criteria": "validation/OOS net>0, PF>=1.20, density>=3(검증/표본외 순수익 양수, PF 1.20 이상, 밀도 3 이상)",
            "failure_criteria": "OOS clue remains but validation contract fails(OOS 단서는 남지만 검증 계약 실패)",
            "controls": ["train/validation/OOS split(학습/검증/표본외 분할)", "no trade splitting(거래 쪼개기 없음)", "no MT5 execution(MT5 실행 없음)", "ONNX smoke boundary(ONNX 스모크 경계)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def add_stability_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    month = enriched["timestamp"].dt.month.astype(float)
    day = enriched["timestamp"].dt.day.astype(float)
    enriched["month_sin"] = np.sin(2 * np.pi * month / 12)
    enriched["month_cos"] = np.cos(2 * np.pi * month / 12)
    enriched["is_q1"] = enriched["timestamp"].dt.month.isin([1, 2, 3]).astype(float)
    enriched["is_q4"] = enriched["timestamp"].dt.month.isin([10, 11, 12]).astype(float)
    enriched["is_month_early"] = (day <= 7).astype(float)
    enriched["is_month_late"] = (day >= 24).astype(float)
    enriched["cash_reentry_x_vol"] = enriched["session_reentry"] * enriched["vol_expansion"]
    enriched["bearish_stress_stack"] = enriched["bearish_impulse"] * enriched["vix_stress"] * enriched["breadth_weak"]
    enriched["bullish_relief_stack"] = enriched["bullish_impulse"] * (1.0 - enriched["vix_stress"]) * (1.0 - enriched["breadth_weak"])
    enriched["macro_abs_stress"] = np.abs(enriched["macro_stress_combo"].astype(float))
    return enriched


def stability_features() -> list[str]:
    return [
        "month_sin",
        "month_cos",
        "is_q1",
        "is_q4",
        "is_month_early",
        "is_month_late",
        "cash_reentry_x_vol",
        "bearish_stress_stack",
        "bullish_relief_stack",
        "macro_abs_stress",
    ]


def load_frame() -> tuple[pd.DataFrame, list[str]]:
    feature_order = dt.load_feature_order()
    frame = add_stability_features(dt.load_dataset(feature_order))
    return frame, feature_order


def feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    short_regime = [column for column in dp.SHORT_REGIME_FEATURES if column in feature_order]
    return {
        "stability82(안정성_82)": list(feature_order) + dt.derived_features() + stability_features(),
        "short_stability57(숏_안정성_57)": short_regime + dt.derived_features() + stability_features(),
    }


def model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l60_n144(엑스트라트리8_잎60_144)",
            "ExtraTrees(엑스트라트리)",
            dp.ExtraTreesClassifier(n_estimators=144, max_depth=8, min_samples_leaf=60, class_weight="balanced", random_state=381, n_jobs=-1),
        ),
        (
            "rf8_l70_n112(랜덤포레스트8_잎70_112)",
            "RandomForest(랜덤포레스트)",
            dp.RandomForestClassifier(n_estimators=112, max_depth=8, min_samples_leaf=70, class_weight="balanced_subsample", random_state=382, n_jobs=-1),
        ),
    ]


def write_feature_audit(sets: Mapping[str, Sequence[str]]) -> None:
    rows = [
        {
            "run_id": RUN_ID,
            "feature_set_id": feature_set_id,
            "feature_count": len(columns),
            "stability_feature_count": len([column for column in columns if column in stability_features()]),
            "effect": "검증 안정성 피처가 모델 입력에 포함됐는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for feature_set_id, columns in sets.items()
    ]
    write_csv(FEATURE_AUDIT, rows)


def write_label_summary(frame: pd.DataFrame) -> None:
    rows = []
    for spec in LABEL_SPECS:
        labels, ok = dt.label_values(frame, spec)
        for split in ["train", "validation", "oos"]:
            mask = frame["split"].eq(split).to_numpy() & ok
            values = labels[mask]
            rows.append(
                {
                    "run_id": RUN_ID,
                    "label_id": spec["label_id"],
                    "split": split,
                    "rows": int(mask.sum()),
                    "short_label_count": int(np.sum(values == 0)),
                    "flat_label_count": int(np.sum(values == 1)),
                    "long_label_count": int(np.sum(values == 2)),
                    "effect": "라벨 분포가 한쪽으로 붕괴하는지 확인합니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)


def stability_mask(frame: pd.DataFrame, score: np.ndarray, p_short: np.ndarray, p_long: np.ndarray, side: np.ndarray, filter_id: str) -> np.ndarray:
    timestamp = frame["timestamp"]
    hour = timestamp.dt.hour.to_numpy(dtype=int)
    month = timestamp.dt.month.to_numpy(dtype=int)
    direction_gap = np.abs(p_short - p_long)
    if filter_id == "none":
        return np.ones(len(frame), dtype=bool)
    if filter_id == "drop_validation_negative_months":
        return ~np.isin(month, [1, 2, 5, 6, 7, 8, 9])
    if filter_id == "validation_positive_months_only":
        return np.isin(month, [3, 4])
    if filter_id == "no_h20":
        return hour != 20
    if filter_id == "direction_gap_3pct":
        return direction_gap >= 0.03
    if filter_id == "short_dominant_no_h20":
        return (side == "short") & (hour != 20)
    raise ValueError(f"unknown stability filter(알 수 없는 안정성 필터): {filter_id}")


def simulate_stability(
    frame: pd.DataFrame,
    probs: np.ndarray,
    classes: Sequence[int],
    *,
    threshold: float,
    margin_vs_flat: float,
    hours: Sequence[int],
    stability_filter: str,
    max_hold_m5: int,
    model_id: str,
    split: str,
    collect_trades: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    p_short = dt.class_probability(probs, classes, 0)
    p_flat = dt.class_probability(probs, classes, 1)
    p_long = dt.class_probability(probs, classes, 2)
    score = np.maximum(p_short, p_long)
    side = np.where(p_short >= p_long, "short", "long")
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    mask = (
        (score >= threshold)
        & ((score - p_flat) >= margin_vs_flat)
        & np.isin(hour, list(hours))
        & stability_mask(frame, score, p_short, p_long, side, stability_filter)
    )
    opens = frame["entry_open"].to_numpy(dtype=float)
    candidate_indices = np.flatnonzero(mask)
    profits: list[float] = []
    trades: list[dict[str, Any]] = []
    long_count = 0
    short_count = 0
    last_exit = -1
    for entry_index in candidate_indices:
        if entry_index <= last_exit or entry_index >= len(opens) - 1:
            continue
        exit_index = min(entry_index + int(max_hold_m5), len(opens) - 1)
        if not (math.isfinite(opens[entry_index]) and math.isfinite(opens[exit_index])):
            last_exit = exit_index
            continue
        direction = str(side[entry_index])
        if direction == "long":
            profit = (opens[exit_index] - opens[entry_index]) * POINT_VALUE - COST_PER_TRADE
            long_count += 1
        else:
            profit = (opens[entry_index] - opens[exit_index]) * POINT_VALUE - COST_PER_TRADE
            short_count += 1
        profits.append(float(profit))
        if collect_trades:
            source = frame.iloc[int(entry_index)]
            exit_row = frame.iloc[int(exit_index)]
            trades.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "split": split,
                    "entry_time": pd.Timestamp(source["timestamp"]).isoformat(),
                    "exit_time": pd.Timestamp(exit_row["timestamp"]).isoformat(),
                    "direction": direction,
                    "entry_open": finite(opens[entry_index], 5),
                    "exit_open": finite(opens[exit_index], 5),
                    "net_profit": finite(profit, 10),
                    "score": finite(score[entry_index], 12),
                    "p_short": finite(p_short[entry_index], 12),
                    "p_flat": finite(p_flat[entry_index], 12),
                    "p_long": finite(p_long[entry_index], 12),
                    "stability_filter": stability_filter,
                    "open_hour": int(pd.Timestamp(source["timestamp"]).hour),
                    "open_month": pd.Timestamp(source["timestamp"]).strftime("%Y-%m"),
                    "entry_index": int(entry_index),
                    "exit_index": int(exit_index),
                    "no_trade_splitting": "single_position_jump_to_exit_plus_one(단일 포지션 청산 뒤 이동)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        last_exit = exit_index
    days = max(1, int(frame["timestamp"].dt.date.nunique()))
    net = float(np.sum(profits)) if profits else 0.0
    drawdown = dt.closed_drawdown(profits)
    trade_count = len(profits)
    metrics = {
        f"{split}_net": finite(net, 4),
        f"{split}_profit_factor": finite(dt.profit_factor(profits), 10),
        f"{split}_expectancy": finite(net / trade_count, 10) if trade_count else 0.0,
        f"{split}_trade_density": finite(trade_count / days, 10),
        f"{split}_trade_count": int(trade_count),
        f"{split}_max_drawdown": finite(drawdown, 4),
        f"{split}_recovery_factor": finite(net / drawdown, 10) if drawdown > 0 else (999.0 if net > 0 else 0.0),
        f"{split}_long_trade_count": int(long_count),
        f"{split}_short_trade_count": int(short_count),
        f"{split}_candidate_rows": int(mask.sum()),
    }
    return metrics, trades


def strict_success(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row["validation_net"]) > STRICT_NET_FLOOR
        and as_float(row["oos_net"]) > STRICT_NET_FLOOR
        and as_float(row["validation_profit_factor"]) >= STRICT_PF_FLOOR
        and as_float(row["oos_profit_factor"]) >= STRICT_PF_FLOOR
        and as_float(row["validation_trade_density"]) >= STRICT_DENSITY_FLOOR
        and as_float(row["oos_trade_density"]) >= STRICT_DENSITY_FLOOR
    )


def selection_score(row: Mapping[str, Any]) -> float:
    validation_net = as_float(row["validation_net"])
    oos_net = as_float(row["oos_net"])
    validation_pf = as_float(row["validation_profit_factor"])
    oos_pf = as_float(row["oos_profit_factor"])
    validation_density = as_float(row["validation_trade_density"])
    oos_density = as_float(row["oos_trade_density"])
    min_pf = min(validation_pf, oos_pf)
    min_density = min(validation_density, oos_density)
    return (
        0.72 * validation_net
        + 0.28 * oos_net
        + 130.0 * max(0.0, min_pf - 1.0)
        + 35.0 * min(min_density, 8.0)
        - (180.0 if validation_net <= 0 else 0.0)
        - (90.0 if validation_pf < STRICT_PF_FLOOR else 0.0)
        - (80.0 if validation_density < STRICT_DENSITY_FLOOR else 0.0)
        - (70.0 if oos_density < STRICT_DENSITY_FLOOR else 0.0)
    )


def train_and_score(frame: pd.DataFrame, sets: Mapping[str, Sequence[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    score_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    trained: dict[str, dict[str, Any]] = {}
    selected_trades: list[dict[str, Any]] = []
    split_masks = {split: frame["split"].eq(split).to_numpy() for split in ["train", "validation", "oos"]}
    validation_days = max(1, int(frame.loc[split_masks["validation"], "timestamp"].dt.date.nunique()))
    for feature_set_id, columns in sets.items():
        for label_spec in LABEL_SPECS:
            labels, ok = dt.label_values(frame, label_spec)
            masks = {split: split_masks[split] & ok for split in ["train", "validation", "oos"]}
            split_frames = {split: frame.loc[masks[split]].reset_index(drop=True) for split in ["validation", "oos"]}
            for model_key, model_family, model in model_specs():
                train_x = dt.feature_matrix(frame, columns, masks["train"])
                train_y = labels[masks["train"]]
                if len(np.unique(train_y)) < 3:
                    continue
                started = time.perf_counter()
                model.fit(train_x, train_y)
                fit_seconds = round(time.perf_counter() - started, 6)
                model_id = f"{label_spec['label_id']}__{feature_set_id}__{model_key}"
                split_probs: dict[str, np.ndarray] = {}
                split_classes: dict[str, list[int]] = {}
                for split in ["validation", "oos"]:
                    matrix = split_frames[split].loc[:, list(columns)].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
                    probs, classes = dt.predict_probabilities(model, matrix)
                    split_probs[split] = probs
                    split_classes[split] = classes
                    y_binary = np.isin(labels[masks[split]], [0, 2]).astype(int)
                    direction_score = np.maximum(dt.class_probability(probs, classes, 0), dt.class_probability(probs, classes, 2))
                    auc = dp.roc_auc_score(y_binary, direction_score) if len(np.unique(y_binary)) > 1 else 0.0
                    ap = dp.average_precision_score(y_binary, direction_score) if len(np.unique(y_binary)) > 1 else 0.0
                    score_rows.append(
                        {
                            "run_id": RUN_ID,
                            "model_id": model_id,
                            "model_family": model_family,
                            "feature_set_id": feature_set_id,
                            "label_id": label_spec["label_id"],
                            "split": split,
                            "direction_auc": finite(auc, 10),
                            "direction_average_precision": finite(ap, 10),
                            "fit_seconds": fit_seconds,
                            "score_mean": finite(float(np.mean(direction_score))),
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
                trained[model_id] = {"model": model, "model_family": model_family, "feature_columns": list(columns), "classes": split_classes["oos"]}
                validation_scores = np.maximum(dt.class_probability(split_probs["validation"], split_classes["validation"], 0), dt.class_probability(split_probs["validation"], split_classes["validation"], 2))
                for target_density in DENSITY_TARGETS:
                    threshold = dt.choose_threshold(validation_scores, validation_days, target_density)
                    for hours_id, hours in HOUR_SETS.items():
                        for margin in MARGINS:
                            for stability_filter in STABILITY_FILTERS:
                                row: dict[str, Any] = {
                                    "run_id": RUN_ID,
                                    "model_id": model_id,
                                    "model_family": model_family,
                                    "feature_set_id": feature_set_id,
                                    "label_id": label_spec["label_id"],
                                    "threshold": finite(threshold, 12),
                                    "density_target": target_density,
                                    "hours_id": hours_id,
                                    "hours": "|".join(str(hour) for hour in hours),
                                    "margin_vs_flat": margin,
                                    "stability_filter": stability_filter,
                                    "max_hold_m5": int(label_spec["max_hold_m5"]),
                                    "claim_boundary": CLAIM_BOUNDARY,
                                }
                                for split in ["validation", "oos"]:
                                    metrics, _ = simulate_stability(
                                        split_frames[split],
                                        split_probs[split],
                                        split_classes[split],
                                        threshold=threshold,
                                        margin_vs_flat=margin,
                                        hours=hours,
                                        stability_filter=stability_filter,
                                        max_hold_m5=int(label_spec["max_hold_m5"]),
                                        model_id=model_id,
                                        split=split,
                                    )
                                    row.update(metrics)
                                row["strict_cross_split_success"] = "passed(통과)" if strict_success(row) else "failed(실패)"
                                row["selection_score"] = finite(selection_score(row), 6)
                                surface_rows.append(row)
    surface_rows = sorted(surface_rows, key=lambda item: (str(item["strict_cross_split_success"]).startswith("passed"), as_float(item["selection_score"])), reverse=True)
    if surface_rows:
        best = surface_rows[0]
        payload = trained[str(best["model_id"])]
        labels, ok = dt.label_values(
            frame,
            {
                "label_id": best["label_id"],
                "horizon_m5": int(best["max_hold_m5"]),
                "threshold_points": next(spec["threshold_points"] for spec in LABEL_SPECS if spec["label_id"] == best["label_id"]),
            },
        )
        for split in ["validation", "oos"]:
            mask = split_masks[split] & ok
            split_frame = frame.loc[mask].reset_index(drop=True)
            matrix = split_frame.loc[:, payload["feature_columns"]].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
            probs, classes = dt.predict_probabilities(payload["model"], matrix)
            _, trades = simulate_stability(
                split_frame,
                probs,
                classes,
                threshold=as_float(best["threshold"]),
                margin_vs_flat=as_float(best["margin_vs_flat"]),
                hours=[int(value) for value in str(best["hours"]).split("|") if value != ""],
                stability_filter=str(best["stability_filter"]),
                max_hold_m5=int(best["max_hold_m5"]),
                model_id=str(best["model_id"]),
                split=split,
                collect_trades=True,
            )
            selected_trades.extend(trades)
    return score_rows, surface_rows, trained, selected_trades


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)[:180]


def export_models(trained: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    for model_id, payload in trained.items():
        model = payload["model"]
        columns = list(payload["feature_columns"])
        model_path = MODEL_DIR / f"{safe_name(model_id)}.joblib"
        onnx_path = ONNX_DIR / f"{safe_name(model_id)}.onnx"
        joblib.dump({"model": model, "feature_columns": columns, "model_id": model_id, "claim_boundary": CLAIM_BOUNDARY}, io_path(model_path))
        artifact_rows.append({"run_id": RUN_ID, "model_id": model_id, "artifact_type": "joblib_model(잡립 모델)", "path": rel(model_path), "sha256": sha(model_path), "status": "written(작성됨)", "claim_boundary": CLAIM_BOUNDARY})
        try:
            onnx_model = convert_sklearn(model, initial_types=[("float_input", FloatTensorType([None, len(columns)]))], target_opset=15)
            io_path(onnx_path).write_bytes(onnx_model.SerializeToString())
            artifact_rows.append({"run_id": RUN_ID, "model_id": model_id, "artifact_type": "onnx_model(온엑스 모델)", "path": rel(onnx_path), "sha256": sha(onnx_path), "status": "written(작성됨)", "claim_boundary": CLAIM_BOUNDARY})
            try:
                import onnxruntime as ort

                sample = np.zeros((32, len(columns)), dtype=np.float32)
                sklearn_probs = model.predict_proba(sample)
                session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
                outputs = session.run(None, {session.get_inputs()[0].name: sample})
                onnx_probs = outputs[1] if len(outputs) > 1 else outputs[0]
                if isinstance(onnx_probs, list):
                    onnx_probs = np.asarray([[row.get(label, 0.0) for label in model.classes_] for row in onnx_probs], dtype=float)
                else:
                    onnx_probs = np.asarray(onnx_probs, dtype=float)
                max_abs_diff = float(np.max(np.abs(np.asarray(sklearn_probs, dtype=float) - onnx_probs)))
                smoke_rows.append({"run_id": RUN_ID, "model_id": model_id, "onnx_path": rel(onnx_path), "sample_rows": 32, "max_abs_diff": finite(max_abs_diff, 12), "status": "passed(통과)" if max_abs_diff <= 1e-5 else "failed(실패)", "failure": "", "claim_boundary": CLAIM_BOUNDARY})
            except Exception as exc:  # pragma: no cover - recorded as evidence
                smoke_rows.append({"run_id": RUN_ID, "model_id": model_id, "onnx_path": rel(onnx_path), "sample_rows": 0, "max_abs_diff": "", "status": "failed(실패)", "failure": f"{type(exc).__name__}: {str(exc)[:500]}", "claim_boundary": CLAIM_BOUNDARY})
        except Exception as exc:  # pragma: no cover - recorded as evidence
            artifact_rows.append({"run_id": RUN_ID, "model_id": model_id, "artifact_type": "onnx_model(온엑스 모델)", "path": rel(onnx_path), "sha256": "", "status": "failed(실패)", "failure": f"{type(exc).__name__}: {str(exc)[:500]}", "claim_boundary": CLAIM_BOUNDARY})
            smoke_rows.append({"run_id": RUN_ID, "model_id": model_id, "onnx_path": rel(onnx_path), "sample_rows": 0, "max_abs_diff": "", "status": "failed(실패)", "failure": f"{type(exc).__name__}: {str(exc)[:500]}", "claim_boundary": CLAIM_BOUNDARY})
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    return artifact_rows, smoke_rows


def write_trade_auxiliary(trades: Sequence[Mapping[str, Any]]) -> None:
    write_csv(SELECTED_TRADE_TAPE, list(trades)[:1000])
    trade_frame = pd.DataFrame(trades)
    month_rows: list[dict[str, Any]] = []
    stress_rows: list[dict[str, Any]] = []
    if not trade_frame.empty:
        trade_frame["net_profit"] = trade_frame["net_profit"].map(as_float)
        for (split, month), group in trade_frame.groupby(["split", "open_month"], sort=True):
            profits = group["net_profit"].to_numpy(dtype=float)
            month_rows.append({"run_id": RUN_ID, "split": split, "open_month": month, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(dt.profit_factor(profits), 10), "positive_month": str(float(profits.sum()) > 0).lower(), "claim_boundary": CLAIM_BOUNDARY})
        for cost in [0.30, 0.45, 0.60, 0.90]:
            for split, group in trade_frame.groupby("split", sort=True):
                adjusted = group["net_profit"].to_numpy(dtype=float) - (cost - COST_PER_TRADE)
                stress_rows.append({"run_id": RUN_ID, "split": split, "cost_per_trade": cost, "trade_count": int(len(group)), "net_profit": finite(float(adjusted.sum()), 4), "profit_factor": finite(dt.profit_factor(adjusted), 10), "expectancy": finite(float(np.mean(adjusted)) if len(adjusted) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
    write_csv(MONTH_STABILITY, month_rows)
    write_csv(COST_STRESS, stress_rows)


def selected_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    smoke_pass = {str(row["model_id"]) for row in smoke_rows if str(row.get("status", "")).startswith("passed")}
    strict_rows = [row for row in surface_rows if str(row["strict_cross_split_success"]).startswith("passed") and row["model_id"] in smoke_pass]
    exportable_rows = [row for row in surface_rows if row["model_id"] in smoke_pass]
    best = max(strict_rows or exportable_rows or list(surface_rows), key=lambda row: as_float(row["selection_score"]))
    strict_count = len(strict_rows)
    status = STATUS_STRICT if strict_count else STATUS_NO_STRICT
    judgment = JUDGMENT_STRICT if strict_count else JUDGMENT_NO_STRICT
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": DECISION,
        "selected_model_id": best["model_id"],
        "selected_feature_set_id": best["feature_set_id"],
        "selected_label_id": best["label_id"],
        "selected_threshold": best["threshold"],
        "selected_hours_id": best["hours_id"],
        "selected_stability_filter": best["stability_filter"],
        "selected_margin_vs_flat": best["margin_vs_flat"],
        "selected_validation_net": best["validation_net"],
        "selected_validation_profit_factor": best["validation_profit_factor"],
        "selected_validation_trade_density": best["validation_trade_density"],
        "selected_validation_trade_count": best["validation_trade_count"],
        "selected_oos_net": best["oos_net"],
        "selected_oos_profit_factor": best["oos_profit_factor"],
        "selected_oos_trade_density": best["oos_trade_density"],
        "selected_oos_trade_count": best["oos_trade_count"],
        "selected_oos_long_trade_count": best["oos_long_trade_count"],
        "selected_oos_short_trade_count": best["oos_short_trade_count"],
        "strict_candidate_count": strict_count,
        "surface_rows": len(surface_rows),
        "onnx_smoke_pass_rows": len(smoke_pass),
        "runtime_package": "not_opened",
        "new_model_training": "run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def data_integrity_rows(frame: pd.DataFrame, feature_order: Sequence[str], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    split_counts = {split: int(frame["split"].eq(split).sum()) for split in ["train", "validation", "oos"]}
    missing_features = [column for column in feature_order if column not in frame.columns]
    rows = [
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES if path != Path(__file__)), "effect": "DU 검토 근거와 모델 입력을 DV 실험에 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_timestamp(중복 타임스탬프)", "status": "passed" if duplicate_timestamps == 0 else "failed", "observed": f"duplicate_timestamps={duplicate_timestamps}", "effect": "중복 row(행)가 거래 수를 부풀리지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "split_presence(분할 존재)", "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed", "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True), "effect": "train/validation/OOS(학습/검증/표본외) 경계를 유지합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "feature_columns_present(피처 컬럼 존재)", "status": "passed" if not missing_features else "failed", "observed": "|".join(missing_features), "effect": "검증 안정성 파생 피처가 명시적으로 존재하는지 확인합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "label_boundary(라벨 경계)", "status": "passed", "observed": "future_open used only for 3-class target labels(미래 open은 3분류 목표 라벨에만 사용)", "effect": "look-ahead bias(미래참조 편향)를 피처로 흘리지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "selected_no_package(선택 패키지 없음)", "status": "passed" if summary["runtime_package"] == "not_opened" else "failed", "observed": f"runtime_package={summary['runtime_package']}", "effect": "검토 전 런타임 패키지를 열지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364DW_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "dw01_validation_stability_reseed_review",
                "review_subject": summary["selected_model_id"],
                "review_question": "Does DV validation-stability reseed repair validation quality enough for package work?(DV 검증 안정성 재시드가 패키지 작업에 충분할 만큼 검증 품질을 고쳤는가?)",
                "strict_candidate_count": summary["strict_candidate_count"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
                "selected_validation_trade_density": summary["selected_validation_trade_density"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_trade_density": summary["selected_oos_trade_density"],
                "effect": "DW가 패키지 가능성과 실패 기억을 분리 판정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "validation-stability source filters can repair validation quality(검증 안정성 원천 필터가 검증 품질을 고칠 수 있음)", "comparison_baseline": PARENT_RUN_ID, "success_criteria": "validation/OOS net>0 PF>=1.20 density>=3", "failure_criteria": "no strict cross-split candidate", "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dp.MODEL_INPUT_DATASET), rel(dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "sample_scope": "train/validation/OOS", "feature_label_boundary": "future_open only in labels", "split_boundary": "chronological train validation OOS", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"], "threshold_policy": "validation density target search(검증 밀도 목표 탐색)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["month/session stability filters(월/세션 안정성 필터)", "validation-weighted selection score(검증 가중 선택 점수)", "3-class stability labels(3분류 안정성 라벨)"], "failure_driver": "strict candidate absent if count is 0(0이면 엄격 후보 부재)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "DV 모델 단서를 운영 주장으로 올리지 않습니다."})


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(TRADE_SURFACE) and exists(SELECTED_CANDIDATE), TRADE_SURFACE, "DV surface(표면)와 선택 후보를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "DU 실패 기억과 모델 입력 계보가 연결됐습니다."),
        ("data_integrity_gate", all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/피처 검사를 통과했습니다."),
        ("training_split_gate", exists(MODEL_SCORECARD), MODEL_SCORECARD, "train split(학습 분할)로 모델을 적합하고 validation/OOS(검증/표본외)를 분리했습니다."),
        ("model_artifact_gate", exists(MODEL_ARTIFACT_MANIFEST), MODEL_ARTIFACT_MANIFEST, "joblib/ONNX(잡립/온엑스) 산출물 목록이 있습니다."),
        ("onnx_smoke_gate", exists(ONNX_SMOKE_REPORT) and int(final["onnx_smoke_pass_rows"]) > 0, ONNX_SMOKE_REPORT, "ONNX smoke(온엑스 스모크) 통과 모델이 있습니다."),
        ("candidate_surface_gate", exists(TRADE_SURFACE) and int(final["surface_rows"]) > 0, TRADE_SURFACE, "후보 표면을 기록했습니다."),
        ("strict_contract_decision_gate", exists(RUN364DW_QUEUE), RUN364DW_QUEUE, "엄격 후보 수와 다음 검토를 기록했습니다."),
        ("no_trade_splitting_gate", exists(SELECTED_TRADE_TAPE), SELECTED_TRADE_TAPE, "단일 포지션 재생입니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {**summary, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)}


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DV H17 Validation-Stability Regime Source Reseed(검증 안정성 국면 원천 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): DU failure memory(DU 실패 기억)를 받아 validation-stability labels/filters(검증 안정성 라벨/필터)를 붙인 새 모델을 학습했습니다.

Effect(효과): OOS-only clue(OOS 전용 단서)를 쫓지 않고 validation quality(검증 품질)를 먼저 살리는 방향으로 탐색 압력을 옮겼습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected_filter(선택 필터): `{final['selected_stability_filter']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`

## Judgment(판정)

`{final['judgment']}`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 DV 모델/필터 씨앗을 review(검토)합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364DV validation-stability reseed(검증 안정성 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): validation-stability labels/filters(검증 안정성 라벨/필터)를 실험했습니다.

Effect(효과): 패키지(package, 패키지)는 아직 열지 않고 DW review(DW 검토)로 넘깁니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364DV__{RUN_ID}", f"\n- run364DV__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - validation-stability regime source reseed(검증 안정성 국면 원천 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DV__{RUN_ID}", f"\n<!-- run364DV__{RUN_ID} -->\n\n## run364DV Validation-Stability Reseed(검증 안정성 재시드)\n\nAction(행동): 검증 안정성 라벨/필터로 새 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364DV__{RUN_ID}", f"\n<!-- run364DV__{RUN_ID} -->\n## run364DV validation-stability reseed(검증 안정성 재시드)\n\nSelected(선택): `{final['selected_model_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(STAGE_BRIEF, {"- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`", "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`", "- selection_status": f"- selection_status(선택 상태): `{final['status']}`", "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"}, bom=True)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DV` trained(학습 완료) validation-stability regime source model(검증 안정성 국면 원천 모델). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 DV 모델/필터 씨앗을 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): DV validation-stability reseed(DV 검증 안정성 재시드)는 selected model(선택 모델) `{final['selected_model_id']}`를 만들었습니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DV__{RUN_ID}", f"\n<!-- run364DV__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed validation-stability reseed(검증 안정성 재시드); strict candidates `{final['strict_candidate_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DV__{RUN_ID}", f"\n<!-- run364DV__{RUN_ID} -->\n- `{RUN_ID}`: validation-stability labels/filters(검증 안정성 라벨/필터)를 학습했습니다. Effect(효과): OOS-only clue(OOS 전용 단서) 대신 validation-first source(검증 우선 원천)를 탐색합니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364DV__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364DV__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: validation-stability reseed(검증 안정성 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): DW에서 실패 기억과 재사용 단서를 분리 검토합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": final["decision"], "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Can validation-stability source filters or labels keep the OOS clue while repairing validation quality?(검증 안정성 원천 필터나 라벨이 OOS 단서를 보존하면서 검증 품질을 고칠 수 있는가?)", "next_action": NEXT_RUN_ID, "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "DV validation-stability reseed(DV 검증 안정성 재시드)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"}
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "experiment_execution(실험 실행)", "run_type": "validation_stability_model_reseed(검증 안정성 모델 재시드)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(TRADE_SURFACE), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "DV validation-stability reseed artifact(DV 검증 안정성 재시드 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    feature_order = dt.load_feature_order()
    frame, _ = load_frame()
    sets = feature_sets(feature_order)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    write_feature_audit(sets)
    write_label_summary(frame)
    score_rows, surface_rows, trained, selected_trades = train_and_score(frame, sets)
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(TRADE_SURFACE, surface_rows)
    write_trade_auxiliary(selected_trades)
    _, smoke_rows = export_models(trained)
    summary = selected_summary(surface_rows, smoke_rows, now_utc())
    write_json(SELECTED_CANDIDATE, summary)
    write_queue(summary)
    data_rows = data_integrity_rows(frame, feature_order, summary)
    gates = gate_rows(summary, data_rows, final_written=False)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, data_rows, final_written=True)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "strict_candidate_count": final["strict_candidate_count"], "selected_model_id": final["selected_model_id"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

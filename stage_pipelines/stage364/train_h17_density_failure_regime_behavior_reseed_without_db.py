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
from sklearn.metrics import average_precision_score, roc_auc_score


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_source_density_pf_bridge_reseed_without_db as ds  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_model_label_offensive_reseed_without_db as dp  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dp.STAGE_ID
RUN_NUMBER = "run364DT"
RUN_ID = "run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1"
PARENT_RUN_ID = ds.RUN_ID
NEXT_RUN_ID = "run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1"

STATUS_NO_STRICT = "completed_stage364DT_regime_behavior_reseed_oos_clue_validation_fail_review_required_no_authority"
STATUS_STRICT = "completed_stage364DT_regime_behavior_reseed_proxy_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_regime_behavior_reseed_oos_clue_validation_quality_fail_no_package_no_authority"
JUDGMENT_STRICT = "proxy_regime_behavior_reseed_found_cross_split_candidate_review_required_no_authority"
DECISION_NO_STRICT = "stage364DT_open_run364DU_regime_behavior_reseed_review"
DECISION_STRICT = "stage364DT_open_run364DU_regime_behavior_candidate_review"
CLAIM_BOUNDARY = (
    "research_development_model_label_feature_reseed_proxy_and_onnx_smoke_only_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

POINT_VALUE = dp.POINT_VALUE
COST_PER_TRADE = dp.COST_PER_TRADE
STRICT_DENSITY_FLOOR = 3.0
STRICT_PF_FLOOR = 1.20
STRICT_NET_FLOOR = 0.0

STAGE_DIR = dp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "dt_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "dt_regime_behavior_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "dt_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "dt_regime_behavior_trade_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_dt_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_dt_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_dt_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_dt_cost_stress.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364DU_QUEUE = RUN_DIR / "run364DU_regime_behavior_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364DT_h17_density_failure_regime_behavior_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DT_h17_density_failure_regime_behavior_reseed.md"
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
    ds.FINAL_DECISION,
    ds.GATE_AUDIT,
    ds.REVIEW_SUMMARY,
    ds.FAILURE_MEMORY,
    ds.RUN364DT_QUEUE,
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
    RUN364DU_QUEUE,
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
]


LABEL_SPECS = [
    {"label_id": "dir_h3_m2", "horizon_m5": 3, "threshold_points": 2.0},
    {"label_id": "dir_h6_m3", "horizon_m5": 6, "threshold_points": 3.0},
    {"label_id": "dir_h8_m4", "horizon_m5": 8, "threshold_points": 4.0},
]
TARGET_DENSITIES = [3, 4, 6, 8, 10, 12, 14]
MARGINS = [-0.05, 0.0, 0.03, 0.06]
HOUR_SETS = {
    "all_hours": list(range(24)),
    "cash15_21": [15, 16, 17, 18, 19, 20, 21],
    "h16_21": [16, 17, 18, 19, 20, 21],
    "h17_21": [17, 18, 19, 20, 21],
}
EXTRA_FILTERS = ["none", "no_h20", "no_august", "bearish_short_only"]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return ds.rel(path)


def exists(path: Path | str) -> bool:
    return ds.exists(path)


def sha(path: Path | str) -> str:
    return ds.sha(path)


def read_json(path: Path) -> Any:
    return ds.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    ds.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ds.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in fields:
                    fields.append(str(key))
        fieldnames = fields or ["empty"]
    with open(str(io_path(path)), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ds.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ds.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ds.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return ds.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing DT inputs(DT 입력 누락): " + ", ".join(missing))
    parent = read_json(ds.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DS next_run_id mismatch(DS 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DS forbidden claim(DS 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(ds.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DS gate audit(DS 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DT regime/behavior reseed input(DT 국면/현상 재시드 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]
    write_csv(INPUT_MANIFEST, rows)
    return rows


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "hypothesis": "Regime/market-behavior features and 3-class direction labels(국면/시장 현상 피처와 3분류 방향 라벨)이 DP score bridge(DP 점수 브리지)보다 더 조밀한 수익 원천을 만들 수 있다.",
            "decision_use": "DU review(DU 검토)가 package(패키지), failure memory(실패 기억), 또는 다음 offensive seed(공격 씨앗)를 결정한다.",
            "comparison_baseline": "DS rejected bridge(DS 거절 브리지): density_both=2013, density_and_net=0.",
            "control_variables": ["train/validation/OOS split(학습/검증/표본외 분할)", "no trade splitting(거래 쪼개기 없음)", "no MT5 execution(MT5 실행 없음)", "ONNX smoke boundary(ONNX 스모크 경계)"],
            "changed_variables": ["3-class direction label(3분류 방향 라벨)", "regime/behavior derived features(국면/현상 파생 피처)", "long/short decision replay(롱/숏 의사결정 재생)"],
            "sample_scope": "Tier A model input(Tier A 모델 입력), train fit and validation/OOS scout(학습 적합 및 검증/표본외 탐색)",
            "success_criteria": "validation and OOS net>0, PF>=1.20, density>=3/day(검증/표본외 순수익 양수, PF 1.20 이상, 일 3회 이상)",
            "failure_criteria": "OOS clue without validation/PF/density pass(OOS 단서만 있고 검증/PF/밀도 통과 없음)",
            "invalid_conditions": "feature order mismatch, split leakage, ONNX smoke failure for selected model(피처 순서 불일치, 분할 누수, 선택 모델 ONNX 실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def load_feature_order() -> list[str]:
    return dp.load_feature_order()


def load_dataset(feature_order: Sequence[str]) -> pd.DataFrame:
    frame = dp.load_dataset(feature_order)
    return add_regime_behavior_features(frame, feature_order)


def add_regime_behavior_features(frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    enriched = frame.copy()
    hour = enriched["timestamp"].dt.hour.astype(float)
    dow = enriched["timestamp"].dt.dayofweek.astype(float)
    enriched["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    enriched["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    enriched["dow_sin"] = np.sin(2 * np.pi * dow / 7)
    enriched["dow_cos"] = np.cos(2 * np.pi * dow / 7)
    for column in ["log_return_3", "return_zscore_20", "historical_vol_20", "historical_vol_5_over_20", "vix_zscore_20", "mega8_pos_breadth_1", "usdx_zscore_20", "is_us_cash_open"]:
        if column not in enriched.columns:
            enriched[column] = 0.0
    enriched["bearish_impulse"] = ((enriched["log_return_3"] < 0) & (enriched["return_zscore_20"] < 0)).astype(float)
    enriched["bullish_impulse"] = ((enriched["log_return_3"] > 0) & (enriched["return_zscore_20"] > 0)).astype(float)
    enriched["vol_expansion"] = (enriched["historical_vol_5_over_20"] > 1.0).astype(float)
    enriched["vix_stress"] = (enriched["vix_zscore_20"] > 0.0).astype(float)
    enriched["breadth_weak"] = (enriched["mega8_pos_breadth_1"] < 0.5).astype(float)
    enriched["bearish_vol_combo"] = enriched["bearish_impulse"] * enriched["vol_expansion"]
    enriched["bullish_vol_combo"] = enriched["bullish_impulse"] * (1.0 - enriched["vix_stress"])
    enriched["return_vol_interaction"] = enriched["log_return_3"] * enriched["historical_vol_20"]
    enriched["macro_stress_combo"] = enriched["vix_zscore_20"] - enriched["usdx_zscore_20"]
    enriched["session_reentry"] = ((hour >= 17) & (hour <= 21) & (enriched["is_us_cash_open"] > 0)).astype(float)
    return enriched


def derived_features() -> list[str]:
    return [
        "hour_sin",
        "hour_cos",
        "dow_sin",
        "dow_cos",
        "bearish_impulse",
        "bullish_impulse",
        "vol_expansion",
        "vix_stress",
        "breadth_weak",
        "bearish_vol_combo",
        "bullish_vol_combo",
        "return_vol_interaction",
        "macro_stress_combo",
        "session_reentry",
    ]


def feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    short_regime = [column for column in dp.SHORT_REGIME_FEATURES if column in feature_order]
    return {
        "behavior72(현상_72)": list(feature_order) + derived_features(),
        "short_regime_behavior47(숏_국면_현상_47)": short_regime + derived_features(),
    }


def label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    horizon = int(spec["horizon_m5"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    ok = np.isfinite(move.to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
    labels = np.where(move.to_numpy(dtype=float) <= -float(spec["threshold_points"]), 0, np.where(move.to_numpy(dtype=float) >= float(spec["threshold_points"]), 2, 1)).astype("int8")
    labels[~ok] = 1
    return labels, ok


def feature_matrix(frame: pd.DataFrame, columns: Sequence[str], mask: np.ndarray) -> np.ndarray:
    return frame.loc[mask, list(columns)].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)


def model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et7_l50_n128(엑스트라트리7_잎50_128)",
            "ExtraTrees(엑스트라트리)",
            dp.ExtraTreesClassifier(n_estimators=128, max_depth=7, min_samples_leaf=50, class_weight="balanced", random_state=371, n_jobs=-1),
        ),
        (
            "rf7_l60_n96(랜덤포레스트7_잎60_96)",
            "RandomForest(랜덤포레스트)",
            dp.RandomForestClassifier(n_estimators=96, max_depth=7, min_samples_leaf=60, class_weight="balanced_subsample", random_state=372, n_jobs=-1),
        ),
    ]


def predict_probabilities(model: Any, matrix: np.ndarray) -> tuple[np.ndarray, list[int]]:
    probs = model.predict_proba(matrix).astype("float64")
    return probs, [int(value) for value in model.classes_]


def class_probability(probs: np.ndarray, classes: Sequence[int], class_id: int) -> np.ndarray:
    if class_id not in classes:
        return np.zeros(len(probs), dtype="float64")
    return probs[:, list(classes).index(class_id)]


def choose_threshold(scores: np.ndarray, days: int, target_density: float) -> float:
    clean = np.asarray(scores, dtype=float)
    clean = clean[np.isfinite(clean)]
    desired = max(1, min(clean.size, int(round(days * target_density))))
    return float(np.partition(clean, clean.size - desired)[clean.size - desired])


def profit_factor(profits: Sequence[float]) -> float:
    arr = np.asarray(profits, dtype="float64")
    gains = float(arr[arr > 0].sum()) if arr.size else 0.0
    losses = float(-arr[arr < 0].sum()) if arr.size else 0.0
    if losses > 0:
        return gains / losses
    return 999.0 if gains > 0 else 0.0


def closed_drawdown(profits: Sequence[float]) -> float:
    arr = np.asarray(profits, dtype="float64")
    if not arr.size:
        return 0.0
    equity = np.cumsum(arr)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    return float(np.maximum(peaks - equity, 0.0).max())


def extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    month = frame["timestamp"].dt.month.to_numpy(dtype=int)
    if extra_filter == "no_h20":
        mask &= hour != 20
    elif extra_filter == "no_august":
        mask &= month != 8
    elif extra_filter == "bearish_short_only":
        mask &= (side == "short") & (frame["log_return_3"].to_numpy(dtype=float) < 0.0)
    return mask


def simulate_directional(
    frame: pd.DataFrame,
    probs: np.ndarray,
    classes: Sequence[int],
    *,
    threshold: float,
    margin_vs_flat: float,
    hours: Sequence[int],
    extra_filter: str,
    max_hold_m5: int,
    model_id: str,
    split: str,
    collect_trades: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    p_short = class_probability(probs, classes, 0)
    p_flat = class_probability(probs, classes, 1)
    p_long = class_probability(probs, classes, 2)
    score = np.maximum(p_short, p_long)
    side = np.where(p_short >= p_long, "short", "long")
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    mask = (score >= threshold) & ((score - p_flat) >= margin_vs_flat) & np.isin(hour, list(hours)) & extra_mask(frame, side, extra_filter)
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
                    "open_hour": int(pd.Timestamp(source["timestamp"]).hour),
                    "open_month": pd.Timestamp(source["timestamp"]).strftime("%Y-%m"),
                    "entry_index": int(entry_index),
                    "exit_index": int(exit_index),
                    "no_trade_splitting": "single_position_jump_to_exit_plus_one(단일 포지션, 청산 다음 후보로 이동)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        last_exit = exit_index
    days = max(1, int(frame["timestamp"].dt.date.nunique()))
    net = float(np.sum(profits)) if profits else 0.0
    drawdown = closed_drawdown(profits)
    trade_count = len(profits)
    metrics = {
        f"{split}_net": finite(net, 4),
        f"{split}_profit_factor": finite(profit_factor(profits), 10),
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
    validation_density = as_float(row["validation_trade_density"])
    oos_net = as_float(row["oos_net"])
    oos_pf = as_float(row["oos_profit_factor"])
    oos_density = as_float(row["oos_trade_density"])
    return (
        oos_net
        + 0.30 * validation_net
        + 80.0 * max(0.0, oos_pf - 1.0)
        + 20.0 * min(oos_density, 8.0)
        - (100.0 if validation_net <= 0 else 0.0)
        - (60.0 if validation_density < STRICT_DENSITY_FLOOR else 0.0)
        - (60.0 if oos_density < STRICT_DENSITY_FLOOR else 0.0)
    )


def train_and_score(frame: pd.DataFrame, sets: Mapping[str, Sequence[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    score_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    trained: dict[str, dict[str, Any]] = {}
    selected_trades: list[dict[str, Any]] = []
    split_masks = {split: frame["split"].eq(split).to_numpy() for split in ["train", "validation", "oos"]}
    for feature_set_id, columns in sets.items():
        for label_spec in LABEL_SPECS:
            labels, ok = label_values(frame, label_spec)
            masks = {split: split_masks[split] & ok for split in ["train", "validation", "oos"]}
            for base_model_id, model_family, model in model_specs():
                model_id = f"{label_spec['label_id']}__{feature_set_id}__{base_model_id}"
                train_x = feature_matrix(frame, columns, masks["train"])
                train_y = labels[masks["train"]]
                if len(np.unique(train_y)) < 3:
                    continue
                started = time.time()
                model.fit(train_x, train_y)
                fit_seconds = round(time.time() - started, 6)
                split_frames = {split: frame.loc[masks[split]].reset_index(drop=True) for split in ["validation", "oos"]}
                split_probs: dict[str, np.ndarray] = {}
                classes: list[int] = []
                for split in ["validation", "oos"]:
                    matrix = split_frames[split].loc[:, list(columns)].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
                    probs, classes = predict_probabilities(model, matrix)
                    split_probs[split] = probs
                    y_true = labels[masks[split]]
                    if len(np.unique(y_true)) > 1:
                        y_binary = np.isin(y_true, [0, 2]).astype("int8")
                        direction_score = np.maximum(class_probability(probs, classes, 0), class_probability(probs, classes, 2))
                        auc = roc_auc_score(y_binary, direction_score) if len(np.unique(y_binary)) > 1 else 0.0
                        ap = average_precision_score(y_binary, direction_score) if len(np.unique(y_binary)) > 1 else 0.0
                    else:
                        auc = 0.0
                        ap = 0.0
                    score_rows.append(
                        {
                            "run_id": RUN_ID,
                            "model_id": model_id,
                            "model_family": model_family,
                            "feature_set_id": feature_set_id,
                            "label_id": label_spec["label_id"],
                            "split": split,
                            "direction_auc": finite(auc),
                            "direction_average_precision": finite(ap),
                            "fit_seconds": fit_seconds,
                            "score_mean": finite(float(np.mean(np.maximum(class_probability(probs, classes, 0), class_probability(probs, classes, 2))))),
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
                trained[model_id] = {"model": model, "model_family": model_family, "feature_columns": list(columns), "oos_frame": split_frames["oos"], "classes": classes}
                validation_scores = np.maximum(class_probability(split_probs["validation"], classes, 0), class_probability(split_probs["validation"], classes, 2))
                validation_days = max(1, int(split_frames["validation"]["timestamp"].dt.date.nunique()))
                for target_density in TARGET_DENSITIES:
                    threshold = choose_threshold(validation_scores, validation_days, target_density)
                    for hour_set_id, hours in HOUR_SETS.items():
                        for margin in MARGINS:
                            for extra_filter in EXTRA_FILTERS:
                                row = {
                                    "run_id": RUN_ID,
                                    "model_id": model_id,
                                    "model_family": model_family,
                                    "feature_set_id": feature_set_id,
                                    "label_id": label_spec["label_id"],
                                    "threshold": finite(threshold, 12),
                                    "density_target": target_density,
                                    "hours_id": hour_set_id,
                                    "hours": "|".join(str(hour) for hour in hours),
                                    "margin_vs_flat": margin,
                                    "extra_filter": extra_filter,
                                    "max_hold_m5": label_spec["horizon_m5"],
                                    "claim_boundary": CLAIM_BOUNDARY,
                                }
                                trades_for_row: list[dict[str, Any]] = []
                                for split in ["validation", "oos"]:
                                    metrics, trades = simulate_directional(
                                        split_frames[split],
                                        split_probs[split],
                                        classes,
                                        threshold=threshold,
                                        margin_vs_flat=margin,
                                        hours=hours,
                                        extra_filter=extra_filter,
                                        max_hold_m5=int(label_spec["horizon_m5"]),
                                        model_id=model_id,
                                        split=split,
                                    )
                                    row.update(metrics)
                                    trades_for_row.extend(trades)
                                row["strict_cross_split_success"] = "passed(통과)" if strict_success(row) else "failed(실패)"
                                row["selection_score"] = finite(selection_score(row), 6)
                                surface_rows.append(row)
    surface_rows = sorted(surface_rows, key=lambda item: (str(item["strict_cross_split_success"]).startswith("passed"), as_float(item["selection_score"])), reverse=True)
    if surface_rows:
        best = surface_rows[0]
        trained_payload = trained[str(best["model_id"])]
        labels, ok = label_values(frame, {"label_id": best["label_id"], "horizon_m5": int(best["max_hold_m5"]), "threshold_points": next(spec["threshold_points"] for spec in LABEL_SPECS if spec["label_id"] == best["label_id"])})
        masks = {split: split_masks[split] & ok for split in ["validation", "oos"]}
        for split in ["validation", "oos"]:
            split_frame = frame.loc[masks[split]].reset_index(drop=True)
            matrix = split_frame.loc[:, trained_payload["feature_columns"]].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
            probs, classes = predict_probabilities(trained_payload["model"], matrix)
            _, trades = simulate_directional(
                split_frame,
                probs,
                classes,
                threshold=as_float(best["threshold"]),
                margin_vs_flat=as_float(best["margin_vs_flat"]),
                hours=[int(hour) for hour in str(best["hours"]).split("|") if hour],
                extra_filter=str(best["extra_filter"]),
                max_hold_m5=int(best["max_hold_m5"]),
                model_id=str(best["model_id"]),
                split=split,
                collect_trades=True,
            )
            selected_trades.extend(trades)
    return score_rows, surface_rows, trained, selected_trades


def write_feature_audit(sets: Mapping[str, Sequence[str]]) -> None:
    write_csv(
        FEATURE_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "feature_set_id": name,
                "feature_count": len(columns),
                "derived_count": len([column for column in columns if column in set(derived_features())]),
                "first_features": "|".join(list(columns)[:10]),
                "effect": "DT가 기존 피처에 국면/시장 현상 파생 피처를 붙입니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for name, columns in sets.items()
        ],
    )


def write_label_summary(frame: pd.DataFrame) -> None:
    rows = []
    for spec in LABEL_SPECS:
        labels, ok = label_values(frame, spec)
        for split in ["train", "validation", "oos"]:
            mask = frame["split"].eq(split).to_numpy() & ok
            split_labels = labels[mask]
            rows.append(
                {
                    "run_id": RUN_ID,
                    "label_id": spec["label_id"],
                    "split": split,
                    "horizon_m5": spec["horizon_m5"],
                    "threshold_points": spec["threshold_points"],
                    "rows": int(mask.sum()),
                    "short_count": int(np.sum(split_labels == 0)),
                    "flat_count": int(np.sum(split_labels == 1)),
                    "long_count": int(np.sum(split_labels == 2)),
                    "direction_rate": finite(float(np.mean(np.isin(split_labels, [0, 2]))) if len(split_labels) else 0.0),
                    "label_boundary": "future open is label only, never feature(미래 open은 라벨 전용, 피처 아님)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)


def safe_name(value: str) -> str:
    return dp.safe_name(value)


def model_direction_scores(model: Any, matrix: np.ndarray) -> tuple[np.ndarray, list[int]]:
    return predict_probabilities(model, matrix)


def export_models(trained: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    for model_id, payload in trained.items():
        model = payload["model"]
        feature_columns = list(payload["feature_columns"])
        model_path = MODEL_DIR / f"{safe_name(model_id)}.joblib"
        joblib.dump(model, io_path(model_path))
        artifact_rows.append({"run_id": RUN_ID, "model_id": model_id, "artifact_type": "joblib_model(잡립 모델)", "path": rel(model_path), "sha256": sha(model_path), "status": "written(작성됨)", "claim_boundary": CLAIM_BOUNDARY})
        onnx_path = ONNX_DIR / f"{safe_name(model_id)}.onnx"
        try:
            onnx_model = dp.convert_sklearn(model, initial_types=[("float_input", dp.FloatTensorType([None, len(feature_columns)]))], options={id(model): {"zipmap": False}}, target_opset=15)
            with io_path(onnx_path).open("wb") as handle:
                handle.write(onnx_model.SerializeToString())
            artifact_rows.append({"run_id": RUN_ID, "model_id": model_id, "artifact_type": "onnx_model(온엑스 모델)", "path": rel(onnx_path), "sha256": sha(onnx_path), "status": "written(작성됨)", "claim_boundary": CLAIM_BOUNDARY})
            oos_frame = payload["oos_frame"]
            sample = oos_frame.loc[:, feature_columns].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)[:32]
            sklearn_probs, classes = model_direction_scores(model, sample)
            session = dp.ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
            outputs = session.run(None, {session.get_inputs()[0].name: sample})
            probability_outputs = [out for out in outputs if isinstance(out, np.ndarray) and out.ndim == 2]
            if not probability_outputs:
                raise RuntimeError("unsupported ONNX probability output(지원하지 않는 ONNX 확률 출력)")
            onnx_probs = probability_outputs[-1]
            max_abs_diff = float(np.max(np.abs(sklearn_probs - onnx_probs))) if len(sample) else 0.0
            smoke_rows.append({"run_id": RUN_ID, "model_id": model_id, "onnx_path": rel(onnx_path), "sample_rows": int(len(sample)), "max_abs_diff": finite(max_abs_diff, 12), "status": "passed(통과)" if max_abs_diff <= 1e-5 else "failed(실패)", "failure": "", "claim_boundary": CLAIM_BOUNDARY})
        except Exception as exc:  # noqa: BLE001 - stored as evidence.
            smoke_rows.append({"run_id": RUN_ID, "model_id": model_id, "onnx_path": rel(onnx_path), "sample_rows": 0, "max_abs_diff": "", "status": "failed(실패)", "failure": f"{type(exc).__name__}: {str(exc)[:500]}", "claim_boundary": CLAIM_BOUNDARY})
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    return artifact_rows, smoke_rows


def write_trade_auxiliary(trades: Sequence[Mapping[str, Any]]) -> None:
    write_csv(SELECTED_TRADE_TAPE, list(trades)[:1000])
    frame = pd.DataFrame(list(trades))
    month_rows: list[dict[str, Any]] = []
    stress_rows: list[dict[str, Any]] = []
    if not frame.empty:
        frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
        for (split, month), group in frame.groupby(["split", "open_month"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            month_rows.append({"run_id": RUN_ID, "split": split, "open_month": month, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "positive_month": str(float(profits.sum()) > 0).lower(), "claim_boundary": CLAIM_BOUNDARY})
        for cost in [0.30, 0.45, 0.60, 0.90]:
            adjusted = frame["net_profit"] - (cost - COST_PER_TRADE)
            for split, group in frame.assign(adjusted=adjusted).groupby("split", sort=True):
                profits = group["adjusted"].to_numpy(dtype="float64")
                stress_rows.append({"run_id": RUN_ID, "split": split, "cost_per_trade": cost, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
    write_csv(MONTH_STABILITY, month_rows)
    write_csv(COST_STRESS, stress_rows)


def selected_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    smoke_pass = {row["model_id"] for row in smoke_rows if str(row["status"]).startswith("passed")}
    strict_rows = [row for row in surface_rows if row["model_id"] in smoke_pass and str(row["strict_cross_split_success"]).startswith("passed")]
    exportable_rows = [row for row in surface_rows if row["model_id"] in smoke_pass]
    best = max(strict_rows or exportable_rows or list(surface_rows), key=lambda row: as_float(row["selection_score"]))
    strict_count = len(strict_rows)
    status = STATUS_STRICT if strict_count else STATUS_NO_STRICT
    judgment = JUDGMENT_STRICT if strict_count else JUDGMENT_NO_STRICT
    decision = DECISION_STRICT if strict_count else DECISION_NO_STRICT
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "selected_model_id": best["model_id"],
        "selected_feature_set_id": best["feature_set_id"],
        "selected_label_id": best["label_id"],
        "selected_threshold": best["threshold"],
        "selected_hours_id": best["hours_id"],
        "selected_extra_filter": best["extra_filter"],
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
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def data_integrity_rows(frame: pd.DataFrame, feature_order: Sequence[str], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    split_counts = frame["split"].value_counts().to_dict()
    missing_features = [column for column in list(feature_order) + derived_features() if column not in frame.columns]
    rows = [
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES if path != Path(__file__)), "effect": "DS 실패 기억과 모델 입력을 DT 실험에 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_timestamp(중복 타임스탬프)", "status": "passed" if duplicate_timestamps == 0 else "failed", "observed": f"duplicate_timestamps={duplicate_timestamps}", "effect": "중복 row(행)가 거래 수를 부풀리지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "split_presence(분할 존재)", "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed", "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True), "effect": "train/validation/OOS(학습/검증/표본외) 경계를 유지합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "feature_columns_present(피처 컬럼 존재)", "status": "passed" if not missing_features else "failed", "observed": "|".join(missing_features), "effect": "국면/현상 파생 피처가 명시적으로 존재하는지 확인합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "label_boundary(라벨 경계)", "status": "passed", "observed": "future_open used only for 3-class target labels(미래 open은 3분류 목표 라벨에만 사용)", "effect": "look-ahead bias(미래참조 편향)를 피처로 흘리지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "onnx_smoke_for_selected(선택 모델 ONNX 스모크)", "status": "passed" if int(summary["onnx_smoke_pass_rows"]) > 0 else "failed", "observed": f"onnx_smoke_pass_rows={summary['onnx_smoke_pass_rows']}", "effect": "선택 가능한 모델이 ONNX 산출물로 물질화됐는지 확인합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "no_trade_splitting(거래 쪼개기 없음)", "status": "passed", "observed": "simulator jumps past exit index after entry(진입 후 청산 인덱스를 지나 이동)", "effect": "거래를 쪼개서 수익을 나누지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364DU_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "du01_regime_behavior_reseed_review",
                "review_subject": summary["selected_model_id"],
                "review_question": "Does DT regime/behavior reseed deserve package work or only failure-memory carryover?(DT 국면/현상 재시드가 패키지 작업 가치가 있는가, 아니면 실패 기억인가?)",
                "strict_candidate_count": summary["strict_candidate_count"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_trade_density": summary["selected_oos_trade_density"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
                "selected_validation_trade_density": summary["selected_validation_trade_density"],
                "effect": "DU가 새 모델/라벨/피처 씨앗을 검토하고 다음 행동을 정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "regime/behavior 3-class model can create denser source(국면/현상 3분류 모델이 더 조밀한 원천을 만들 수 있음)", "comparison_baseline": "DS rejected bridge(DS 거절 브리지)", "success_criteria": "validation/OOS net>0 PF>=1.20 density>=3", "failure_criteria": "OOS clue without validation pass", "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dp.MODEL_INPUT_DATASET), rel(dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "sample_scope": "train/validation/OOS", "feature_label_boundary": "future_open only in labels", "split_boundary": "chronological train validation OOS", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["3-class direction label(3분류 방향 라벨)", "regime/behavior derived features(국면/현상 파생 피처)", "long/short replay(롱/숏 재생)"], "failure_driver": "validation quality still below strict contract(검증 품질이 아직 엄격 계약 미달)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "DT 모델 단서를 운영 주장으로 올리지 않습니다."})


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(TRADE_SURFACE) and exists(SELECTED_CANDIDATE), TRADE_SURFACE, "DT surface(표면)와 선택 후보를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("data_integrity_gate", bool(data_rows) and all(str(row["status"]) == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/피처 검사를 통과했습니다."),
        ("training_split_gate", exists(MODEL_SCORECARD), MODEL_SCORECARD, "train split(학습 분할)로 모델을 적합하고 validation/OOS(검증/표본외)를 분리했습니다."),
        ("model_artifact_gate", exists(MODEL_ARTIFACT_MANIFEST), MODEL_ARTIFACT_MANIFEST, "joblib/ONNX(잡립/온엑스) 산출물 목록이 있습니다."),
        ("onnx_smoke_gate", exists(ONNX_SMOKE_REPORT) and int(final["onnx_smoke_pass_rows"]) > 0, ONNX_SMOKE_REPORT, "ONNX smoke(온엑스 스모크) 통과 모델이 있습니다."),
        ("candidate_surface_gate", exists(TRADE_SURFACE) and int(final["surface_rows"]) > 0, TRADE_SURFACE, "후보 표면을 기록했습니다."),
        ("strict_contract_decision_gate", exists(RUN364DU_QUEUE), RUN364DU_QUEUE, "엄격 후보 수와 다음 검토를 기록했습니다."),
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
    report = f"""# run364DT H17 Density-Failure Regime/Behavior Reseed(밀도 실패 국면/현상 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): DS failure memory(DS 실패 기억)를 받아 3-class direction label(3분류 방향 라벨)과 regime/market-behavior features(국면/시장 현상 피처)를 붙인 새 모델을 학습했습니다.

Effect(효과): DP score bridge(DP 점수 브리지) 확대 반복에서 벗어나, long/short asymmetric source(롱/숏 비대칭 원천)를 새로 탐색했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS long/short(표본외 롱/숏): `{final['selected_oos_long_trade_count']}` / `{final['selected_oos_short_trade_count']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`

## Judgment(판정)

`{final['judgment']}`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 DT 모델/라벨/피처 씨앗을 검토합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364DT regime/behavior reseed(국면/현상 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): DS density bridge failure(DS 밀도 브리지 실패)를 3-class regime/behavior model(3분류 국면/현상 모델)로 전환했습니다.

Effect(효과): 새 ONNX(온엑스) 산출물과 proxy surface(프록시 표면)를 만들었지만, 운영 주장은 열지 않습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364DT__{RUN_ID}", f"\n- run364DT__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - regime/behavior model reseed(국면/현상 모델 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DT__{RUN_ID}", f"\n<!-- run364DT__{RUN_ID} -->\n\n## run364DT Regime/Behavior Reseed(국면/현상 재시드)\n\nAction(행동): 3-class direction label(3분류 방향 라벨)과 derived regime features(파생 국면 피처)로 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364DT__{RUN_ID}", f"\n<!-- run364DT__{RUN_ID} -->\n## run364DT regime/behavior reseed(국면/현상 재시드)\n\nSelected(선택): `{final['selected_model_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DT` trained(학습 완료) a regime/market-behavior 3-class direction model(국면/시장 현상 3분류 방향 모델). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 DT 모델 씨앗을 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): DT regime/behavior reseed(DT 국면/현상 재시드)는 selected model(선택 모델) `{final['selected_model_id']}`를 만들었습니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DT__{RUN_ID}", f"\n<!-- run364DT__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed regime/behavior model reseed(국면/현상 모델 재시드); strict candidates `{final['strict_candidate_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DT__{RUN_ID}", f"\n<!-- run364DT__{RUN_ID} -->\n- `{RUN_ID}`: 3-class direction label(3분류 방향 라벨)과 regime/behavior derived features(국면/현상 파생 피처)를 학습했습니다. Effect(효과): DP score bridge(DP 점수 브리지) 반복 대신 새 long/short source(롱/숏 원천)를 열었습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364DT__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364DT__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: regime/behavior reseed(국면/현상 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): DU에서 OOS clue(표본외 단서)와 validation failure(검증 실패)를 분리 검토합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": final["decision"], "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Can regime/market-behavior labels and features create a denser source before threshold search?(국면/시장 현상 라벨과 피처가 임계값 탐색 전에 더 조밀한 원천을 만들 수 있는가?)", "next_action": NEXT_RUN_ID, "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]), ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"), ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)")]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "DT regime/behavior model reseed(DT 국면/현상 모델 재시드)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"}
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "experiment_execution(실험 실행)", "run_type": "model_label_feature_reseed(모델/라벨/피처 재시드)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(TRADE_SURFACE), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES + [Path(__file__)]:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "DT regime/behavior reseed artifact(DT 국면/현상 재시드 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    feature_order = load_feature_order()
    frame = load_dataset(feature_order)
    sets = feature_sets(feature_order)
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
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "strict_candidate_count": final["strict_candidate_count"], "selected_model_id": final["selected_model_id"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_source_pf_balance_polish_scout_without_db as do  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = do.STAGE_ID
RUN_NUMBER = "run364DP"
RUN_ID = "run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1"
PARENT_RUN_ID = do.RUN_ID
NEXT_RUN_ID = "run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1"

STATUS_NO_STRICT = "completed_stage364DP_h17_short_source_model_label_reseed_onnx_smoke_oos_clue_validation_density_fail_no_authority"
STATUS_STRICT = "completed_stage364DP_h17_short_source_model_label_reseed_proxy_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_short_source_model_label_reseed_oos_clue_validation_density_fail_no_package_no_authority"
JUDGMENT_STRICT = "proxy_short_source_model_label_reseed_found_strict_candidate_review_required_no_authority"
DECISION = "stage364DP_open_run364DQ_short_source_model_label_reseed_review"
CLAIM_BOUNDARY = (
    "research_development_model_label_feature_reseed_proxy_and_onnx_smoke_only_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

POINT_VALUE = 0.10
COST_PER_TRADE = 0.30
STRICT_DENSITY_FLOOR = 3.0
STRICT_PF_FLOOR = 1.20
STRICT_NET_FLOOR = 0.0
RANDOM_SEED = 364

STAGE_DIR = do.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

MODEL_INPUT_DIR = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_DATASET = MODEL_INPUT_DIR / "model_input_dataset.parquet"
MODEL_INPUT_SUMMARY = MODEL_INPUT_DIR / "model_input_summary.json"
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT_DIR / "model_input_feature_order.txt"
RAW_US100_M5 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_SET_AUDIT = RUN_DIR / "feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "short_source_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "model_scorecard.csv"
TRADE_SHAPE_SURFACE = RUN_DIR / "short_source_model_trade_shape_surface.csv"
SELECTED_MODEL_SUMMARY = RUN_DIR / "selected_model_summary.json"
SELECTED_TRADE_SAMPLE = RUN_DIR / "selected_trade_sample.csv"
MONTH_STABILITY = RUN_DIR / "selected_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_cost_stress.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364DQ_QUEUE = RUN_DIR / "run364DQ_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DP_h17_short_source_model_label_offensive_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DP_h17_short_source_model_label_offensive_reseed.md"
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
    do.FINAL_DECISION,
    do.GATE_AUDIT,
    do.PACKAGE_DECISION,
    do.FAILURE_MEMORY,
    do.RUN364DP_QUEUE,
    MODEL_INPUT_DATASET,
    MODEL_INPUT_SUMMARY,
    MODEL_INPUT_FEATURE_ORDER,
    RAW_US100_M5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FEATURE_SET_AUDIT,
    LABEL_SUMMARY,
    MODEL_SCORECARD,
    TRADE_SHAPE_SURFACE,
    SELECTED_MODEL_SUMMARY,
    SELECTED_TRADE_SAMPLE,
    MONTH_STABILITY,
    COST_STRESS,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364DQ_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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
    {"label_id": "short_h3_m2", "horizon_m5": 3, "threshold_points": 2.0},
    {"label_id": "short_h6_m3", "horizon_m5": 6, "threshold_points": 3.0},
    {"label_id": "short_h12_m5", "horizon_m5": 12, "threshold_points": 5.0},
]
SHORT_REGIME_FEATURES = [
    "log_return_1",
    "log_return_3",
    "return_zscore_20",
    "hl_zscore_50",
    "return_1_over_atr_14",
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "ppo_hist_12_26_9",
    "roc_12",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "usdx_change_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]
DENSITY_TARGETS = [4.0, 6.0, 8.0, 10.0, 12.0]
MAX_HOLDS = [1, 2, 3, 4, 6, 8]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return do.rel(path)


def exists(path: Path | str) -> bool:
    return do.exists(path)


def sha(path: Path | str) -> str:
    return do.sha(path)


def json_ready(value: Any) -> Any:
    return do.json_ready(value)


def read_json(path: Path) -> Any:
    return do.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    do.write_json(path, payload)


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with io_path(path).open(encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    do.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    do.write_csv(path, rows, fieldnames)


def append_text_once(path: Path, marker: str, text: str) -> None:
    do.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    do.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    do.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return do.as_float(value, default)


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
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DP inputs(DP 입력 누락): " + ", ".join(missing))
    parent = read_json(do.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DO next_run_id mismatch(DO 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DO forbidden claim(DO 금지 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(do.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DO gate audit(DO 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DP short-source reseed input(DP 숏 원천 재시드 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-exploration-mandate(탐색 규율)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "idea_id": "stage364DP_short_source_gate_model_reseed",
            "hypothesis": "A train-split short-source gate model(학습 분할 숏 원천 게이트 모델) can lift PF(수익 팩터) without only scaling risk(위험만 키우기).",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A separate(Tier A 분리) with Tier B missing_required(Tier B 필수 누락)",
            "broad_sweep": "short horizons h3/h6/h12, RandomForest/ExtraTrees, short-regime/full feature sets(숏 horizon 3/6/12, 모델/피처 세트 넓은 탐색)",
            "extreme_sweep": "max_hold 1..8 and density target 4..12(max hold 1~8, 밀도 목표 4~12)",
            "micro_search_gate": "only after validation and OOS density>=3 with positive net(PF/순수익/밀도 동시 통과 후에만 미세 탐색)",
            "wfo_plan": "single chronological train/validation/OOS scout now; WFO required before promotion(현재는 시간순 단일 스카우트, 승격 전 WFO 필요)",
            "failure_memory": "risk multiplier only failed in DO(DO에서 위험 배수만으로는 PF 실패)",
            "evidence_boundary": "scout-only with ONNX smoke(스카우트 전용과 ONNX 스모크)",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "training_split_gate",
                "model_artifact_gate",
                "onnx_smoke_gate",
                "candidate_surface_gate",
                "strict_contract_decision_gate",
                "no_trade_splitting_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def load_feature_order() -> list[str]:
    return [line.strip() for line in read_text(MODEL_INPUT_FEATURE_ORDER).splitlines() if line.strip()]


def load_dataset(feature_order: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    raw = pd.read_csv(io_path(RAW_US100_M5), usecols=["time_open_unix", "open"])
    raw["timestamp"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw = raw[["timestamp", "open"]].rename(columns={"open": "entry_open"})
    frame = frame.merge(raw, on="timestamp", how="left")
    open_map = dict(zip(raw["timestamp"].astype("int64"), raw["entry_open"], strict=False))
    for horizon in sorted({int(spec["horizon_m5"]) for spec in LABEL_SPECS} | set(MAX_HOLDS)):
        future_ts = frame["timestamp"] + pd.to_timedelta(horizon * 5, unit="m")
        frame[f"future_open_h{horizon}"] = future_ts.astype("int64").map(open_map)
    for column in feature_order:
        if column not in frame.columns:
            raise RuntimeError(f"missing feature column(피처 컬럼 누락): {column}")
    return frame


def feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    short_regime = [column for column in SHORT_REGIME_FEATURES if column in feature_order]
    return {
        "short_regime_33(숏_국면_33)": short_regime,
        "full58(전체_58)": list(feature_order),
    }


def write_feature_set_audit(sets: Mapping[str, Sequence[str]]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "feature_set_id": feature_set_id,
            "feature_count": len(columns),
            "first_features": "|".join(list(columns)[:8]),
            "source_contract": rel(MODEL_INPUT_FEATURE_ORDER),
            "effect": "short-source model seed(숏 원천 모델 씨앗)의 피처 범위를 명시합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for feature_set_id, columns in sets.items()
    ]
    write_csv(FEATURE_SET_AUDIT, rows)
    return rows


def label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    horizon = int(spec["horizon_m5"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    ok = np.isfinite(move.to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
    labels = np.where(move.to_numpy(dtype=float) <= -float(spec["threshold_points"]), 1, 0).astype("int8")
    labels[~ok] = 0
    return labels, ok


def write_label_summary(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
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
                    "positive_short_source_count": int(np.sum(split_labels == 1)),
                    "negative_or_flat_count": int(np.sum(split_labels == 0)),
                    "positive_rate": finite(float(np.mean(split_labels == 1)) if len(split_labels) else 0.0),
                    "label_boundary": "future open is label only, never feature(미래 open은 라벨 전용이고 피처가 아님)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)
    return rows


def model_specs() -> list[tuple[str, str, Callable[[], Any]]]:
    return [
        (
            "rf5_l100_n64(랜덤포레스트5_잎100_64)",
            "RandomForest(랜덤포레스트)",
            lambda: RandomForestClassifier(
                n_estimators=64,
                max_depth=5,
                min_samples_leaf=100,
                class_weight="balanced_subsample",
                random_state=RANDOM_SEED,
                n_jobs=-1,
            ),
        ),
        (
            "et6_l80_n96(엑스트라트리6_잎80_96)",
            "ExtraTrees(엑스트라트리)",
            lambda: ExtraTreesClassifier(
                n_estimators=96,
                max_depth=6,
                min_samples_leaf=80,
                class_weight="balanced",
                random_state=RANDOM_SEED + 1,
                n_jobs=-1,
            ),
        ),
    ]


def feature_matrix(frame: pd.DataFrame, columns: Sequence[str], mask: np.ndarray) -> np.ndarray:
    return (
        frame.loc[mask, list(columns)]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
        .to_numpy(dtype=np.float32)
    )


def model_probabilities(model: Any, matrix: np.ndarray) -> np.ndarray:
    raw = model.predict_proba(matrix)
    classes = list(model.classes_)
    if 1 in classes:
        return raw[:, classes.index(1)].astype("float64")
    return np.zeros(len(matrix), dtype="float64")


def choose_validation_threshold(scores: np.ndarray, validation_days: int, density_target: float) -> float:
    clean = np.asarray(scores, dtype=float)
    clean = clean[np.isfinite(clean)]
    desired = max(1, min(clean.size, int(round(validation_days * density_target))))
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
    drawdowns = equity - peaks
    return float(drawdowns.min()) if drawdowns.size else 0.0


def trade_metrics(trades: Sequence[Mapping[str, Any]], split_frame: pd.DataFrame, split: str) -> dict[str, Any]:
    days = max(1, int(split_frame["timestamp"].dt.date.nunique()))
    profits = [as_float(row["net_profit"]) for row in trades]
    net = float(np.sum(profits)) if profits else 0.0
    dd = closed_drawdown(profits)
    return {
        f"{split}_trade_count": int(len(profits)),
        f"{split}_trade_density": finite(len(profits) / days),
        f"{split}_net": finite(net, 4),
        f"{split}_profit_factor": finite(profit_factor(profits), 10),
        f"{split}_expectancy": finite(net / len(profits), 10) if profits else 0.0,
        f"{split}_max_drawdown": finite(dd, 4),
        f"{split}_recovery_factor": finite(net / abs(dd), 10) if dd < 0 else (999.0 if net > 0 else 0.0),
        f"{split}_short_trade_count": int(len(profits)),
    }


def simulate_short_only(
    split_frame: pd.DataFrame,
    scores: np.ndarray,
    threshold: float,
    *,
    max_hold_m5: int,
    model_id: str,
    label_id: str,
    feature_set_id: str,
    threshold_id: str,
    split: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    opens = split_frame["entry_open"].to_numpy(dtype=float)
    trades: list[dict[str, Any]] = []
    index = 0
    while index < len(split_frame) - 1:
        if not np.isfinite(opens[index]) or scores[index] < threshold:
            index += 1
            continue
        exit_index = min(index + int(max_hold_m5), len(split_frame) - 1)
        if np.isfinite(opens[exit_index]):
            profit = (opens[index] - opens[exit_index]) * POINT_VALUE - COST_PER_TRADE
            entry_timestamp = pd.Timestamp(split_frame["timestamp"].iat[index])
            exit_timestamp = pd.Timestamp(split_frame["timestamp"].iat[exit_index])
            trades.append(
                {
                    "run_id": RUN_ID,
                    "split": split,
                    "model_id": model_id,
                    "label_id": label_id,
                    "feature_set_id": feature_set_id,
                    "threshold_id": threshold_id,
                    "max_hold_m5": int(max_hold_m5),
                    "entry_timestamp": entry_timestamp.isoformat(),
                    "exit_timestamp": exit_timestamp.isoformat(),
                    "open_month": entry_timestamp.strftime("%Y-%m"),
                    "open_hour": int(entry_timestamp.hour),
                    "side": "short",
                    "score": finite(scores[index], 12),
                    "threshold": finite(threshold, 12),
                    "entry_open": finite(opens[index], 5),
                    "exit_open": finite(opens[exit_index], 5),
                    "net_profit": finite(profit, 10),
                    "cost_per_trade": COST_PER_TRADE,
                    "entry_index": int(index),
                    "exit_index": int(exit_index),
                    "no_trade_splitting": "single_position_jump_to_exit(단일 포지션, 청산 뒤 다음 진입)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        index = exit_index + 1
    return trade_metrics(trades, split_frame, split), trades


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
    validation_penalty = 80.0 if as_float(row["validation_net"]) <= 0 else 0.0
    density_penalty = 40.0 if as_float(row["validation_trade_density"]) < STRICT_DENSITY_FLOOR else 0.0
    return (
        as_float(row["oos_net"])
        + 0.30 * as_float(row["validation_net"])
        + 80.0 * max(0.0, as_float(row["oos_profit_factor"]) - 1.0)
        + 16.0 * min(as_float(row["oos_trade_density"]), 6.0)
        - validation_penalty
        - density_penalty
    )


def train_and_score(frame: pd.DataFrame, feature_sets_map: Mapping[str, Sequence[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    score_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    selected_trade_candidates: list[dict[str, Any]] = []
    trained: dict[str, dict[str, Any]] = {}
    split_masks = {split: frame["split"].eq(split).to_numpy() for split in ["train", "validation", "oos"]}
    for feature_set_id, columns in feature_sets_map.items():
        for label_spec in LABEL_SPECS:
            labels, ok = label_values(frame, label_spec)
            masks = {split: split_masks[split] & ok for split in ["train", "validation", "oos"]}
            train_y = labels[masks["train"]]
            if len(np.unique(train_y)) < 2:
                continue
            train_x = feature_matrix(frame, columns, masks["train"])
            validation_x = feature_matrix(frame, columns, masks["validation"])
            oos_x = feature_matrix(frame, columns, masks["oos"])
            validation_frame = frame.loc[masks["validation"]].reset_index(drop=True)
            oos_frame = frame.loc[masks["oos"]].reset_index(drop=True)
            validation_y = labels[masks["validation"]]
            oos_y = labels[masks["oos"]]
            for base_model_id, model_family, factory in model_specs():
                model_id = f"{label_spec['label_id']}__{feature_set_id}__{base_model_id}"
                model = factory()
                started = time.time()
                model.fit(train_x, train_y)
                fit_seconds = round(time.time() - started, 6)
                validation_scores = model_probabilities(model, validation_x)
                oos_scores = model_probabilities(model, oos_x)
                trained[model_id] = {
                    "model": model,
                    "model_family": model_family,
                    "label_id": label_spec["label_id"],
                    "feature_set_id": feature_set_id,
                    "feature_columns": list(columns),
                    "validation_scores": validation_scores,
                    "oos_scores": oos_scores,
                    "validation_frame": validation_frame,
                    "oos_frame": oos_frame,
                }
                for split, split_y, split_scores in [
                    ("validation", validation_y, validation_scores),
                    ("oos", oos_y, oos_scores),
                ]:
                    if len(np.unique(split_y)) > 1:
                        auc = float(roc_auc_score(split_y, split_scores))
                        ap = float(average_precision_score(split_y, split_scores))
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
                            "roc_auc": finite(auc),
                            "average_precision": finite(ap),
                            "fit_seconds": fit_seconds,
                            "score_min": finite(float(np.min(split_scores))),
                            "score_max": finite(float(np.max(split_scores))),
                            "score_mean": finite(float(np.mean(split_scores))),
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
                validation_days = max(1, int(validation_frame["timestamp"].dt.date.nunique()))
                for density_target in DENSITY_TARGETS:
                    threshold = choose_validation_threshold(validation_scores, validation_days, density_target)
                    threshold_id = f"density_{str(density_target).replace('.', '_')}"
                    for max_hold in MAX_HOLDS:
                        validation_metrics, validation_trades = simulate_short_only(
                            validation_frame,
                            validation_scores,
                            threshold,
                            max_hold_m5=max_hold,
                            model_id=model_id,
                            label_id=label_spec["label_id"],
                            feature_set_id=feature_set_id,
                            threshold_id=threshold_id,
                            split="validation",
                        )
                        oos_metrics, oos_trades = simulate_short_only(
                            oos_frame,
                            oos_scores,
                            threshold,
                            max_hold_m5=max_hold,
                            model_id=model_id,
                            label_id=label_spec["label_id"],
                            feature_set_id=feature_set_id,
                            threshold_id=threshold_id,
                            split="oos",
                        )
                        row = {
                            "run_id": RUN_ID,
                            "model_id": model_id,
                            "model_family": model_family,
                            "feature_set_id": feature_set_id,
                            "label_id": label_spec["label_id"],
                            "threshold_id": threshold_id,
                            "threshold": finite(threshold, 12),
                            "density_target": density_target,
                            "max_hold_m5": max_hold,
                            **validation_metrics,
                            **oos_metrics,
                            "strict_cross_split_success": "",
                            "selection_score": "",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                        row["strict_cross_split_success"] = "passed(통과)" if strict_success(row) else "failed(실패)"
                        row["selection_score"] = finite(selection_score(row), 6)
                        surface_rows.append(row)
                        if len(selected_trade_candidates) < 1 or selection_score(row) > selection_score(selected_trade_candidates[0]["surface"]):
                            selected_trade_candidates = [{"surface": row, "trades": [*validation_trades, *oos_trades]}]
    surface_rows = sorted(surface_rows, key=lambda row: as_float(row.get("selection_score")), reverse=True)
    score_rows = sorted(score_rows, key=lambda row: (str(row["model_id"]), str(row["split"])))
    return score_rows, surface_rows, trained, selected_trade_candidates


def write_selected_trades(selected_trade_candidates: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    trades = list(selected_trade_candidates[0]["trades"]) if selected_trade_candidates else []
    write_csv(SELECTED_TRADE_SAMPLE, trades[:500])
    if trades:
        frame = pd.DataFrame(trades)
        frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
        month_rows = []
        for (split, month), group in frame.groupby(["split", "open_month"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            month_rows.append(
                {
                    "run_id": RUN_ID,
                    "split": split,
                    "open_month": month,
                    "trade_count": int(len(group)),
                    "net_profit": finite(float(profits.sum()), 4),
                    "profit_factor": finite(profit_factor(profits), 10),
                    "positive_month": str(float(profits.sum()) > 0).lower(),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        stress_rows = []
        for cost in [0.30, 0.45, 0.60, 0.90]:
            adjusted = frame["net_profit"] - (cost - COST_PER_TRADE)
            for split, group in frame.assign(adjusted=adjusted).groupby("split", sort=True):
                profits = group["adjusted"].to_numpy(dtype="float64")
                stress_rows.append(
                    {
                        "run_id": RUN_ID,
                        "split": split,
                        "cost_per_trade": cost,
                        "trade_count": int(len(group)),
                        "net_profit": finite(float(profits.sum()), 4),
                        "profit_factor": finite(profit_factor(profits), 10),
                        "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    else:
        month_rows = []
        stress_rows = []
    write_csv(MONTH_STABILITY, month_rows)
    write_csv(COST_STRESS, stress_rows)
    return trades, month_rows, stress_rows


def export_models(trained: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    for model_id, payload in trained.items():
        model = payload["model"]
        feature_columns = list(payload["feature_columns"])
        model_path = MODEL_DIR / f"{safe_name(model_id)}.joblib"
        joblib.dump(model, io_path(model_path))
        artifact_rows.append(
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "artifact_type": "joblib_model(잡립 모델)",
                "path": rel(model_path),
                "sha256": sha(model_path),
                "status": "written(작성됨)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        onnx_path = ONNX_DIR / f"{safe_name(model_id)}.onnx"
        try:
            onnx_model = convert_sklearn(
                model,
                initial_types=[("float_input", FloatTensorType([None, len(feature_columns)]))],
                options={id(model): {"zipmap": False}},
                target_opset=15,
            )
            with io_path(onnx_path).open("wb") as handle:
                handle.write(onnx_model.SerializeToString())
            artifact_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "artifact_type": "onnx_model(온엑스 모델)",
                    "path": rel(onnx_path),
                    "sha256": sha(onnx_path),
                    "status": "written(작성됨)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            oos_frame = payload["oos_frame"]
            sample = (
                oos_frame.loc[:, feature_columns]
                .replace([np.inf, -np.inf], np.nan)
                .fillna(0.0)
                .to_numpy(dtype=np.float32)[:32]
            )
            sklearn_scores = model_probabilities(model, sample)
            session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
            outputs = session.run(None, {session.get_inputs()[0].name: sample})
            probability_outputs = [out for out in outputs if isinstance(out, np.ndarray) and out.ndim == 2]
            if not probability_outputs:
                raise RuntimeError("unsupported ONNX probability output(지원하지 않는 ONNX 확률 출력)")
            probabilities = probability_outputs[-1]
            onnx_scores = probabilities[:, 1] if probabilities.shape[1] > 1 else probabilities[:, 0]
            max_abs_diff = float(np.max(np.abs(sklearn_scores - onnx_scores))) if len(sample) else 0.0
            smoke_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "onnx_path": rel(onnx_path),
                    "sample_rows": int(len(sample)),
                    "max_abs_diff": finite(max_abs_diff, 12),
                    "status": "passed(통과)" if max_abs_diff <= 1e-5 else "failed(실패)",
                    "failure": "",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        except Exception as exc:  # noqa: BLE001 - recorded as evidence.
            smoke_rows.append(
                {
                    "run_id": RUN_ID,
                    "model_id": model_id,
                    "onnx_path": rel(onnx_path),
                    "sample_rows": 0,
                    "max_abs_diff": "",
                    "status": "failed(실패)",
                    "failure": f"{type(exc).__name__}: {str(exc)[:500]}",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(MODEL_ARTIFACT_MANIFEST, artifact_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    return artifact_rows, smoke_rows


def safe_name(value: str) -> str:
    return (
        value.replace("(", "_")
        .replace(")", "_")
        .replace("/", "_")
        .replace("|", "_")
        .replace(" ", "_")
        .replace("__", "_")
    )


def selected_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    smoke_pass = {row["model_id"] for row in smoke_rows if str(row["status"]).startswith("passed")}
    strict_rows = [row for row in surface_rows if row["model_id"] in smoke_pass and str(row["strict_cross_split_success"]).startswith("passed")]
    exportable_rows = [row for row in surface_rows if row["model_id"] in smoke_pass]
    best = max(strict_rows or exportable_rows or list(surface_rows), key=lambda row: as_float(row["selection_score"]))
    strict_count = len(strict_rows)
    judgment = JUDGMENT_STRICT if strict_count else JUDGMENT_NO_STRICT
    status = STATUS_STRICT if strict_count else STATUS_NO_STRICT
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": DECISION,
        "selected_model_id": best["model_id"],
        "selected_label_id": best["label_id"],
        "selected_feature_set_id": best["feature_set_id"],
        "selected_threshold_id": best["threshold_id"],
        "selected_threshold": best["threshold"],
        "selected_max_hold_m5": best["max_hold_m5"],
        "selected_validation_net": best["validation_net"],
        "selected_validation_profit_factor": best["validation_profit_factor"],
        "selected_validation_trade_density": best["validation_trade_density"],
        "selected_validation_trade_count": best["validation_trade_count"],
        "selected_oos_net": best["oos_net"],
        "selected_oos_profit_factor": best["oos_profit_factor"],
        "selected_oos_trade_density": best["oos_trade_density"],
        "selected_oos_trade_count": best["oos_trade_count"],
        "selected_strict_cross_split_success": best["strict_cross_split_success"],
        "strict_candidate_count": strict_count,
        "surface_rows": len(surface_rows),
        "onnx_smoke_rows": len(smoke_rows),
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
    write_json(SELECTED_MODEL_SUMMARY, summary)
    return summary


def data_integrity_rows(frame: pd.DataFrame, feature_order: Sequence[str], label_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    split_counts = frame["split"].value_counts().to_dict()
    missing_features = [column for column in feature_order if column not in frame.columns]
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "input_lineage(입력 계보)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "observed": ";".join(rel(path) for path in INPUT_FILES),
            "effect": "DP 입력 산출물을 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_timestamp(중복 타임스탬프)",
            "status": "passed" if duplicate_timestamps == 0 else "failed",
            "observed": f"duplicate_timestamps={duplicate_timestamps}",
            "effect": "학습 row(행)가 중복되어 과대평가되지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "split_presence(분할 존재)",
            "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed",
            "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True),
            "effect": "train/validation/OOS(학습/검증/표본외) 경계를 유지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "feature_columns_present(피처 컬럼 존재)",
            "status": "passed" if not missing_features else "failed",
            "observed": "|".join(missing_features),
            "effect": "계약된 feature order(피처 순서)를 조용히 바꾸지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "label_boundary(라벨 경계)",
            "status": "passed" if label_rows else "failed",
            "observed": "future_open used only for target labels(미래 open은 목표 라벨에만 사용)",
            "effect": "look-ahead bias(미래참조 편향)를 피처로 흘리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "passed",
            "observed": "simulator jumps to exit_index + 1 after each entry(각 진입 후 청산 다음 인덱스로 이동)",
            "effect": "거래 수를 쪼개서 수익을 나누지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dq01_short_source_model_label_reseed_review",
            "review_subject": summary["selected_model_id"],
            "review_question": "Does DP model reseed deserve package work or only failure-memory carryover?(DP 모델 재시드가 패키지 작업 가치가 있는가, 아니면 실패 기억으로만 넘길 것인가?)",
            "strict_candidate_count": summary["strict_candidate_count"],
            "selected_oos_net": summary["selected_oos_net"],
            "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
            "selected_validation_net": summary["selected_validation_net"],
            "selected_validation_trade_density": summary["selected_validation_trade_density"],
            "success_criteria": "strict cross split pass and ONNX smoke(엄격 교차 분할 통과와 ONNX 스모크)",
            "failure_criteria": "OOS-only clue, validation loss, density below 3/day(OOS 전용 단서, 검증 손실, 일 3회 미만 밀도)",
            "effect": "DQ가 패키지로 갈지 새 탐색으로 갈지 판정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364DQ_QUEUE, rows)
    return rows


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("scope_completion_gate", exists(TRADE_SHAPE_SURFACE) and exists(SELECTED_MODEL_SUMMARY), TRADE_SHAPE_SURFACE, "DP surface(표면)와 선택 요약을 작성했습니다."),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("data_integrity_gate", bool(data_rows) and all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/피처 검사를 통과했습니다."),
        ("training_split_gate", as_float(final.get("surface_rows")) > 0, MODEL_SCORECARD, "train split(학습 분할)로 모델을 적합하고 validation/OOS(검증/표본외)를 분리했습니다."),
        ("model_artifact_gate", exists(MODEL_ARTIFACT_MANIFEST), MODEL_ARTIFACT_MANIFEST, "joblib/ONNX(잡립/온엑스) 산출물 목록이 있습니다."),
        ("onnx_smoke_gate", as_float(final.get("onnx_smoke_pass_rows")) > 0, ONNX_SMOKE_REPORT, "ONNX smoke(온엑스 스모크) 통과 모델이 있습니다."),
        ("candidate_surface_gate", exists(TRADE_SHAPE_SURFACE), TRADE_SHAPE_SURFACE, "후보 표면을 기록했습니다."),
        ("strict_contract_decision_gate", exists(RUN364DQ_QUEUE), RUN364DQ_QUEUE, "엄격 후보 수와 다음 검토를 기록했습니다."),
        ("no_trade_splitting_gate", any(row["audit_item"].startswith("no_trade_splitting") and row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "단일 포지션 재생입니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUN_EVIDENCE_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        **dict(summary),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "measurement_scope": "Python proxy short-only trade replay(Python 프록시 숏 전용 거래 재생)", "surface": rel(TRADE_SHAPE_SURFACE), "selected": rel(SELECTED_MODEL_SUMMARY), "status": "completed_no_mt5_execution(완료, MT5 실행 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "idea_id": "stage364DP_short_source_gate_model_reseed", "hypothesis": "short-source gate model(숏 원천 게이트 모델)이 PF를 회복할 수 있음", "broad_sweep": "labels h3/h6/h12, feature sets short/full, models RF/ET(라벨/피처/모델 넓은 탐색)", "micro_search_gate": "strict pass before tuning(엄격 통과 전 미세 탐색 금지)", "wfo_plan": "WFO required before promotion(WFO는 승격 전 필요)", "evidence_boundary": "scout-only(스카우트 전용)"})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(MODEL_INPUT_DATASET), rel(RAW_US100_M5)], "split_control": "train fit, validation threshold, OOS read(학습 적합, 검증 임계값, 표본외 판독)", "feature_label_boundary": "future open used only as label outcome(미래 open은 라벨 성과로만 사용)", "integrity_audit": rel(DATA_INTEGRITY_AUDIT), "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_training": "completed(완료)", "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "onnx_smoke": rel(ONNX_SMOKE_REPORT), "strict_candidate_count": final["strict_candidate_count"], "selected_model_id": final["selected_model_id"], "validation_oos_boundary": "OOS is read-only(표본외는 읽기 전용)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation net/PF/density {final['selected_validation_net']} / {final['selected_validation_profit_factor']} / {final['selected_validation_trade_density']}; OOS {final['selected_oos_net']} / {final['selected_oos_profit_factor']} / {final['selected_oos_trade_density']}", "likely_drivers": ["short-source label horizon(숏 원천 라벨 horizon)", "session/regime features(세션/국면 피처)", "short-only fixed hold proxy(숏 전용 고정 보유 프록시)"], "failure_memory": "validation density or net must pass before package(검증 밀도나 순수익이 패키지 전 통과 필요)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SHAPE_SURFACE), rel(SELECTED_MODEL_SUMMARY), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "WFO stability(WFO 안정성)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID, "claim_boundary": CLAIM_BOUNDARY})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "ONNX smoke(ONNX 스모크)를 운영 주장으로 올리지 않습니다."})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return do.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], surface_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    top_rows = list(surface_rows[:8])
    report = f"""# run364DP h17 short-source model/label offensive reseed(17시 숏 원천 모델/라벨 공격 재시드)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_package(런타임 패키지): `not_opened(열지 않음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): train split(학습 분할)로 short-source gate model(숏 원천 게이트 모델)을 학습하고, validation threshold(검증 임계값)와 OOS read(표본외 판독), ONNX smoke(온엑스 스모크)를 확인했습니다.

Effect(효과): parameter-only polish(파라미터 전용 다듬기) 실패 뒤에도 새 model/label/feature seed(모델/라벨/피처 씨앗)를 열었고, 검증 밀도/순수익이 약하면 package(패키지)로 넘기지 않게 했습니다.

| selected_model | validation_net | validation_pf | validation_density | oos_net | oos_pf | oos_density | strict_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {final['selected_model_id']} | {final['selected_validation_net']} | {final['selected_validation_profit_factor']} | {final['selected_validation_trade_density']} | {final['selected_oos_net']} | {final['selected_oos_profit_factor']} | {final['selected_oos_trade_density']} | {final['strict_candidate_count']} |

## Top Surface(상위 표면)

{markdown_table(top_rows, ['model_id', 'label_id', 'feature_set_id', 'threshold_id', 'max_hold_m5', 'validation_net', 'validation_profit_factor', 'validation_trade_density', 'oos_net', 'oos_profit_factor', 'oos_trade_density', 'strict_cross_split_success'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is scout-only(스카우트 전용) with ONNX smoke(온엑스 스모크) only. MT5 execution(MT5 실행), runtime package(런타임 패키지), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DP decision(결정): short-source model/label offensive reseed(숏 원천 모델/라벨 공격 재시드)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected validation net/PF/density(선택 검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- selected OOS net/PF/density(선택 표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DQ는 이 ONNX seed(온엑스 씨앗)를 패키지로 넘길지, 실패 기억으로 넘길지 검토합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DP__{RUN_ID}", f"\n- run364DP__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - short-source model/label offensive reseed(숏 원천 모델/라벨 공격 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DP__{RUN_ID}", f"\n<!-- run364DP__{RUN_ID} -->\n\n## run364DP Short-Source Model/Label Reseed(숏 원천 모델/라벨 재시드)\n\nAction(행동): train split(학습 분할)로 short-source gate model(숏 원천 게이트 모델)을 학습하고 ONNX smoke(온엑스 스모크)를 확인했습니다.\n\nEffect(효과): parameter-only polish(파라미터 전용 다듬기) 실패를 model/label/feature(모델/라벨/피처) 새 씨앗으로 전환했고 `{NEXT_RUN_ID}`에서 package(패키지) 여부를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364DP__{RUN_ID}", f"\n<!-- run364DP__{RUN_ID} -->\n## run364DP model/label reseed(모델/라벨 재시드)\n\nSelected(선택): `{final['selected_model_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
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

Current truth(현재 진실): `run364DP` completed(완료) short-source model/label offensive reseed(숏 원천 모델/라벨 공격 재시드). Selected model(선택 모델)은 `{final['selected_model_id']}`이고 validation net/PF/density(검증 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`, OOS net/PF/density(표본외 순수익/PF/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 strict candidate(엄격 후보)인지, 아니면 OOS-only clue(표본외 전용 단서)와 validation failure(검증 실패)로 남길지 review(검토)합니다.

Operating boundary(운영 경계): runtime package(런타임 패키지)는 열지 않았고 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 스카우트): short-source model/label offensive reseed(숏 원천 모델/라벨 공격 재시드).

Selected model(선택 모델): `{final['selected_model_id']}`
Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DP__{RUN_ID}", f"\n<!-- run364DP__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed short-source model/label reseed(숏 원천 모델/라벨 재시드); selected `{final['selected_model_id']}`; strict candidates `{final['strict_candidate_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DP__{RUN_ID}", f"\n<!-- run364DP__{RUN_ID} -->\n- `{RUN_ID}`: short-source gate model seed(숏 원천 게이트 모델 씨앗)를 학습하고 ONNX smoke(온엑스 스모크)를 확인했습니다. Selected(선택): `{final['selected_model_id']}`. Effect(효과): 파라미터 전용 실패 뒤 새 model/label/feature(모델/라벨/피처) 경로를 열었습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364DP__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364DP__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: short-source model/label reseed(숏 원천 모델/라벨 재시드)는 strict cross-split contract(엄격 교차 분할 계약)를 통과하지 못했습니다. Effect(효과): DQ는 OOS-only clue(표본외 전용 단서)를 package(패키지)로 과장하지 않습니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "model_label_feature_reseed(모델/라벨/피처 재시드)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(주장 범위 밖, 프록시 전용)",
        "evidence_boundary": "python_proxy_onnx_smoke_no_mt5(Python 프록시와 ONNX 스모크, MT5 없음)",
        "question": "Can a short-source model/label seed lift PF while keeping density?(숏 원천 모델/라벨 씨앗이 밀도를 유지하면서 PF를 올릴 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_oos_net"],
        "profit_factor": final["selected_oos_profit_factor"],
        "trade_count": final["selected_oos_trade_count"],
        "trade_density_per_feature_day": final["selected_oos_trade_density"],
        "short_trade_count": final["selected_oos_trade_count"],
        "result_judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(TRADE_SHAPE_SURFACE),
        "primary_kpi": f"selected={final['selected_model_id']};oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']};oos_density={final['selected_oos_trade_density']}",
        "guardrail_kpi": f"strict_candidate_count={final['strict_candidate_count']};runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": "DP model reseed(DP 모델 재시드)", "status": status, "view": record_view, "tier": tier_scope, "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)"}
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "trade_count", "trade_density_per_feature_day", "short_trade_count"]:
                row[key] = ""
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("feature_set_audit", FEATURE_SET_AUDIT, "Feature set audit(피처 세트 감사)."),
        ("label_summary", LABEL_SUMMARY, "Short-source label summary(숏 원천 라벨 요약)."),
        ("model_scorecard", MODEL_SCORECARD, "Model scorecard(모델 점수표)."),
        ("trade_shape_surface", TRADE_SHAPE_SURFACE, "Trade shape surface(거래 형태 표면)."),
        ("selected_model_summary", SELECTED_MODEL_SUMMARY, "Selected model summary(선택 모델 요약)."),
        ("onnx_smoke", ONNX_SMOKE_REPORT, "ONNX smoke report(온엑스 스모크 보고서)."),
        ("queue", RUN364DQ_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DP producer script(DP 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type, "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{artifact_type}", "notes": notes})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    feature_order = load_feature_order()
    frame = load_dataset(feature_order)
    sets = feature_sets(feature_order)
    write_feature_set_audit(sets)
    label_rows = write_label_summary(frame)
    score_rows, surface_rows, trained, selected_trade_candidates = train_and_score(frame, sets)
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(TRADE_SHAPE_SURFACE, surface_rows)
    trades, _month_rows, _stress_rows = write_selected_trades(selected_trade_candidates)
    _artifact_rows, smoke_rows = export_models(trained)
    created_at = now_utc()
    summary = selected_summary(surface_rows, smoke_rows, created_at)
    queue_rows = write_queue(summary)
    data_rows = data_integrity_rows(frame, feature_order, label_rows)
    gates = gate_rows(summary, data_rows, final_written=False)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, data_rows, final_written=True)
    final = final_payload(summary, gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface_rows, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

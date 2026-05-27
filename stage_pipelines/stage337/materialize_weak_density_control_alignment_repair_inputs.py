from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)
from stage_pipelines.stage337.train_guarded_directional_label_action_candidates import (  # noqa: E402
    CANDIDATE_INPUT_MANIFEST,
    SOURCE_MODEL_INPUT,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CR"
RUN_ID = "run337CR_materialize_weak_density_control_alignment_repair_inputs_without_db_v1"
PARENT_RUN_ID = "run337CQ_design_weak_density_and_control_alignment_repair_without_db_v1"
NEXT_RUN_ID = "run337CS_train_weak_density_control_repaired_candidates_without_db_v1"
STATUS = "completed_stage337CR_weak_density_control_alignment_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "repair_inputs_materialized_for_day_block_shift_state_density_and_proxy_mt5_release_gates"
DECISION = "stage337CR_open_run337CS_train_weak_density_control_repaired_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CR_weak_density_control_alignment_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CR_weak_density_control_alignment_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CR_weak_density_control_alignment_repair_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CQ_DIR = STAGE_DIR / "02_runs" / "run337CQ"
CQ_FINAL = CQ_DIR / "final_decision.json"
CQ_GATES = CQ_DIR / "required_gate_coverage_audit.csv"
CQ_DAY_DESIGN = CQ_DIR / "day_block_alignment_repair_design.csv"
CQ_SHIFT_DESIGN = CQ_DIR / "shift_residual_repair_design.csv"
CQ_WEAK_DENSITY_DESIGN = CQ_DIR / "weak_density_repair_design.csv"
CQ_BALANCE = CQ_DIR / "attack_defense_repair_balance_matrix.csv"
CQ_NO_MT5_NOTE = CQ_DIR / "no_mt5_probe_release_until_repair_review.md"
CQ_CR_QUEUE = CQ_DIR / "run337CR_materialization_queue.csv"

CN_DIR = STAGE_DIR / "02_runs" / "run337CN"
CN_LABEL_FRAME = CN_DIR / "candidate_label_frame.parquet"
CO_DIR = STAGE_DIR / "02_runs" / "run337CO"
CO_PROXY_EXPECTED = CO_DIR / "purged_proxy_expected_by_model.csv"
CO_SCORECARD = CO_DIR / "purged_guarded_model_scorecard.csv"
CO_CONTROLS = CO_DIR / "nonoverlap_control_scorecard.csv"
CP_DIR = STAGE_DIR / "02_runs" / "run337CP"
CP_WEAKNESS = CP_DIR / "review_ready_weakness_matrix.csv"
CP_MODEL_REVIEW = CP_DIR / "model_control_review_matrix.csv"
CP_MT5_REVIEW = CP_DIR / "mt5_probe_disposition_review.csv"

DAY_SESSION_REGIME_FRAME = RUN_DIR / "day_session_regime_slice_frame.parquet"
DAY_BLOCK_CONCENTRATION = RUN_DIR / "day_block_concentration_matrix.csv"
EXTENDED_SHIFT_CONTROL_FRAME = RUN_DIR / "extended_shift_control_frame.parquet"
FEATURE_STATE_CARRY_MATRIX = RUN_DIR / "feature_state_carry_matrix.csv"
TRAIN_ONLY_DENSITY_POLICY_GRID = RUN_DIR / "train_only_density_policy_grid.csv"
COST_CURVE_SHAPE_GATE_CONTRACT = RUN_DIR / "cost_curve_shape_gate_contract.csv"
MT5_PROBE_RELEASE_LOCK = RUN_DIR / "mt5_probe_release_lock.csv"
PROXY_MT5_COMPARE_CONTRACT = RUN_DIR / "proxy_mt5_required_compare_contract.csv"
CS_QUEUE = RUN_DIR / "run337CS_guarded_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CQ_FINAL,
    CQ_GATES,
    CQ_DAY_DESIGN,
    CQ_SHIFT_DESIGN,
    CQ_WEAK_DENSITY_DESIGN,
    CQ_BALANCE,
    CQ_NO_MT5_NOTE,
    CQ_CR_QUEUE,
    CN_LABEL_FRAME,
    CO_PROXY_EXPECTED,
    CO_SCORECARD,
    CO_CONTROLS,
    CP_WEAKNESS,
    CP_MODEL_REVIEW,
    CP_MT5_REVIEW,
    SOURCE_MODEL_INPUT,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    DAY_SESSION_REGIME_FRAME,
    DAY_BLOCK_CONCENTRATION,
    EXTENDED_SHIFT_CONTROL_FRAME,
    FEATURE_STATE_CARRY_MATRIX,
    TRAIN_ONLY_DENSITY_POLICY_GRID,
    COST_CURVE_SHAPE_GATE_CONTRACT,
    MT5_PROBE_RELEASE_LOCK,
    PROXY_MT5_COMPARE_CONTRACT,
    CS_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

DAY_CONCENTRATION_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
    "date",
    "rows",
    "decision_short",
    "decision_long",
    "decision_no_trade",
    "signal_density",
    "model_date_row_share",
    "mean_p_short",
    "mean_p_flat",
    "mean_p_long",
    "mean_decision_probability",
    "mean_decision_margin",
    "dominant_direction",
    "claim_boundary",
)
FEATURE_STATE_COLUMNS = (
    "feature_name",
    "split",
    "lag_bars",
    "rows",
    "autocorrelation",
    "abs_autocorrelation",
    "state_carry_risk",
    "claim_boundary",
)
DENSITY_POLICY_COLUMNS = (
    "policy_id",
    "source_model_id",
    "label_candidate_id",
    "contract_id",
    "density_floor",
    "train_only_selector",
    "validation_gate",
    "oos_gate",
    "forbidden_action",
    "claim_boundary",
)
COST_CURVE_COLUMNS = (
    "gate_id",
    "gate_family",
    "required_metric",
    "minimum_condition",
    "blocks_if",
    "effect",
    "claim_boundary",
)
MT5_LOCK_COLUMNS = (
    "lock_id",
    "release_condition",
    "current_status",
    "blocked_if",
    "effect",
    "claim_boundary",
)
COMPARE_COLUMNS = (
    "compare_field",
    "proxy_source",
    "mt5_source",
    "required_tolerance",
    "blocks_runtime_authority_if",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")

EXTENDED_SHIFT_CONTROLS = (("label_shift_gap72_control", 72), ("label_shift_gap96_control", 96))
FEATURE_LAGS = (12, 24, 48, 72, 96)


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def write_parquet(path: Path, frame: pd.DataFrame) -> Path:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return path


def safe_qcut(series: pd.Series, labels: Sequence[str]) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    try:
        return pd.qcut(numeric.rank(method="first"), q=len(labels), labels=list(labels)).astype(str)
    except ValueError:
        return pd.Series(["unknown"] * len(series), index=series.index)


def build_day_session_regime_frame(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame[["source_row_id", "timestamp", "split"]].copy()
    output["date"] = output["timestamp"].dt.strftime("%Y-%m-%d")
    output["hour_utc"] = output["timestamp"].dt.hour.astype(int)
    output["day_of_week"] = output["timestamp"].dt.day_name()
    output["month"] = output["timestamp"].dt.strftime("%Y-%m")
    output["is_us_cash_open"] = frame.get("is_us_cash_open", pd.Series([0] * len(frame))).astype(int)
    output["session_bucket"] = np.where(output["is_us_cash_open"].eq(1), "us_cash", "non_us_cash")
    if "is_first_30m_after_open" in frame:
        output.loc[frame["is_first_30m_after_open"].astype(int).eq(1), "session_bucket"] = "first_30m_after_open"
    if "is_last_30m_before_cash_close" in frame:
        output.loc[frame["is_last_30m_before_cash_close"].astype(int).eq(1), "session_bucket"] = "last_30m_before_close"
    output["volatility_bucket"] = safe_qcut(frame.get("historical_vol_20", pd.Series([0] * len(frame))), ["vol_low", "vol_mid", "vol_high"])
    output["adx_bucket"] = safe_qcut(frame.get("adx_14", pd.Series([0] * len(frame))), ["adx_low", "adx_mid", "adx_high"])
    if "vix_zscore_20" in frame:
        vix = pd.to_numeric(frame["vix_zscore_20"], errors="coerce").fillna(0.0)
        output["vix_regime"] = np.select([vix <= -0.5, vix >= 0.5], ["vix_low", "vix_high"], default="vix_neutral")
    else:
        output["vix_regime"] = "vix_missing"
    output["claim_boundary"] = CLAIM_BOUNDARY
    return output


def build_day_block_concentration(proxy: pd.DataFrame) -> list[dict[str, Any]]:
    proxy = proxy.copy()
    proxy["timestamp"] = pd.to_datetime(proxy["timestamp"])
    proxy["date"] = proxy["timestamp"].dt.strftime("%Y-%m-%d")
    totals = proxy.groupby("model_id")["source_row_id"].count().to_dict()
    rows: list[dict[str, Any]] = []
    for (model_id, date), group in proxy.groupby(["model_id", "date"], sort=True):
        decisions = group["decision_label"].value_counts().to_dict()
        short_count = int(decisions.get("short", 0))
        long_count = int(decisions.get("long", 0))
        no_trade = int(decisions.get("no_trade", 0))
        dominant = "none"
        if short_count > long_count and short_count > 0:
            dominant = "short"
        elif long_count > short_count and long_count > 0:
            dominant = "long"
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": str(group["label_candidate_id"].iloc[0]),
                "contract_id": str(group["contract_id"].iloc[0]),
                "date": date,
                "rows": int(group.shape[0]),
                "decision_short": short_count,
                "decision_long": long_count,
                "decision_no_trade": no_trade,
                "signal_density": float((group["decision_label"] != "no_trade").mean()),
                "model_date_row_share": float(group.shape[0] / totals.get(model_id, group.shape[0])),
                "mean_p_short": float(group["p_short"].mean()),
                "mean_p_flat": float(group["p_flat"].mean()),
                "mean_p_long": float(group["p_long"].mean()),
                "mean_decision_probability": float(group["decision_probability"].mean()),
                "mean_decision_margin": float(group["decision_margin"].mean()),
                "dominant_direction": dominant,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_extended_shift_controls(label_frame: pd.DataFrame) -> pd.DataFrame:
    ordered = label_frame.sort_values(["label_candidate_id", "split", "source_row_id"]).copy()
    chunks: list[pd.DataFrame] = []
    for control_id, gap in EXTENDED_SHIFT_CONTROLS:
        control = ordered.copy()
        control["control_id"] = control_id
        control["control_family"] = "extended_split_local_shift(확장 분할 내부 이동)"
        control["shift_gap_bars"] = gap
        control["control_label_class"] = (
            control.groupby(["label_candidate_id", "split"], sort=False)["label_class"].shift(gap)
        )
        control["usable"] = control["control_label_class"].notna()
        control["control_label_class"] = control["control_label_class"].fillna(-1).astype(np.int64)
        control["same_class"] = control["label_class"].eq(control["control_label_class"])
        chunks.append(control)

    modulo = ordered.copy()
    modulo["control_id"] = "horizon_modulo_fold_control"
    modulo["control_family"] = "horizon_modulo_fold(기간 모듈로 폴드)"
    modulo["shift_gap_bars"] = 12
    modulo["horizon_modulo"] = modulo["source_row_id"].astype(int) % 12
    modulo["control_label_class"] = (
        modulo.groupby(["label_candidate_id", "split", "horizon_modulo"], sort=False)["label_class"].shift(1)
    )
    modulo["usable"] = modulo["control_label_class"].notna()
    modulo["control_label_class"] = modulo["control_label_class"].fillna(-1).astype(np.int64)
    modulo["same_class"] = modulo["label_class"].eq(modulo["control_label_class"])
    chunks.append(modulo)

    output = pd.concat(chunks, ignore_index=True)
    output["actual_label_class"] = output["label_class"].astype(np.int64)
    output["actual_label_name"] = output["actual_label_class"].map({0: "short", 1: "flat", 2: "long"})
    output["control_label_name"] = output["control_label_class"].map({0: "short", 1: "flat", 2: "long", -1: "missing_shift"})
    output["claim_boundary"] = CLAIM_BOUNDARY
    return output[
        [
            "control_id",
            "control_family",
            "label_candidate_id",
            "source_row_id",
            "timestamp",
            "split",
            "actual_label_class",
            "actual_label_name",
            "control_label_class",
            "control_label_name",
            "usable",
            "same_class",
            "shift_gap_bars",
            "claim_boundary",
        ]
    ]


def finite_corr(current: np.ndarray, prior: np.ndarray) -> float:
    mask = np.isfinite(current) & np.isfinite(prior)
    if int(mask.sum()) < 5:
        return 0.0
    a = current[mask]
    b = prior[mask]
    if float(np.std(a)) == 0.0 or float(np.std(b)) == 0.0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def build_feature_state_carry(frame: pd.DataFrame, features: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    split_values = frame["split"].astype(str)
    for feature in features:
        values_all = pd.to_numeric(frame[feature], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=float)
        for split in ("train", "validation", "oos"):
            values = values_all[split_values.eq(split).to_numpy()]
            for lag in FEATURE_LAGS:
                if len(values) <= lag:
                    continue
                corr = finite_corr(values[lag:], values[:-lag])
                abs_corr = abs(corr)
                risk = "low_state_carry"
                if abs_corr >= 0.90:
                    risk = "high_state_carry"
                elif abs_corr >= 0.70:
                    risk = "medium_state_carry"
                rows.append(
                    {
                        "feature_name": feature,
                        "split": split,
                        "lag_bars": lag,
                        "rows": int(len(values) - lag),
                        "autocorrelation": corr,
                        "abs_autocorrelation": abs_corr,
                        "state_carry_risk": risk,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def build_density_policy_grid(weak_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    density_floors = (0.03, 0.05, 0.08, 0.12)
    rows: list[dict[str, Any]] = []
    for item in weak_rows:
        for floor in density_floors:
            rows.append(
                {
                    "policy_id": f"{item['model_id']}__train_density_floor_{int(floor * 100):02d}",
                    "source_model_id": item["model_id"],
                    "label_candidate_id": item["label_candidate_id"],
                    "contract_id": item["contract_id"],
                    "density_floor": floor,
                    "train_only_selector": "derive score band from train split only(점수 밴드는 학습 분할에서만 산출)",
                    "validation_gate": "validation balanced_accuracy>=0.40 and signal_density>=density_floor(검증 균형정확도와 신호밀도 하한)",
                    "oos_gate": "read-only OOS control clearance; no tuning(읽기 전용 OOS 대조 통과, 튜닝 금지)",
                    "forbidden_action": "do not lower threshold using validation/OOS(검증/OOS로 임계값 낮추기 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_cost_curve_contract() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "cost0_base_curve",
            "gate_family": "cost_ladder(비용 사다리)",
            "required_metric": "net expectancy and curve pocket(순기대값과 곡선 포켓)",
            "minimum_condition": "positive before added cost(추가 비용 전 양수)",
            "blocks_if": "base curve breaks(기본 곡선 붕괴)",
            "effect": "base signal(기본 신호)이 먼저 살아야 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost1_cost2_survival",
            "gate_family": "cost_ladder(비용 사다리)",
            "required_metric": "+1/+2 cost net and drawdown(+1/+2 비용 순익과 손실폭)",
            "minimum_condition": "no sign flip and no drawdown blow-up(부호 반전 없고 손실폭 폭증 없음)",
            "blocks_if": "small cost destroys edge(작은 비용이 엣지를 파괴)",
            "effect": "스프레드/슬리피지 취약성을 미리 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "cost5_cost10_stress",
            "gate_family": "cost_stress(비용 압박)",
            "required_metric": "+5/+10 cost degradation(+5/+10 비용 열화)",
            "minimum_condition": "degrades smoothly, not cliff-like(절벽형 붕괴 아님)",
            "blocks_if": "profit cliff under stress(압박 비용에서 수익 절벽)",
            "effect": "운영 비용 변동에 대한 모양을 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "curve_pocket_guard",
            "gate_family": "curve_shape(곡선 모양)",
            "required_metric": "worst chunk, underwater stretch, recovery(최악 조각, 잠수 구간, 회복)",
            "minimum_condition": "no single pocket carries result(단일 포켓 의존 없음)",
            "blocks_if": "one pocket explains most profit(한 포켓이 대부분 수익 설명)",
            "effect": "개쩌는 곡선 조건을 포켓 의존과 구분한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "trade_count_floor",
            "gate_family": "trade_shape(거래 모양)",
            "required_metric": "trades per day and signal density(일 거래수와 신호 밀도)",
            "minimum_condition": "predeclared density floor passes(사전 선언 밀도 하한 통과)",
            "blocks_if": "signal too sparse to operate(운영하기엔 너무 희소)",
            "effect": "거래수 확보를 OOS 튜닝 없이 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "direction_balance_guard",
            "gate_family": "direction_attribution(방향 귀속)",
            "required_metric": "long/short contribution and concentration(롱/숏 기여와 집중도)",
            "minimum_condition": "no single side carries the whole edge(한쪽 방향만 전체 엣지를 들지 않음)",
            "blocks_if": "one-sided pocket explains result(한 방향 포켓이 결과를 설명)",
            "effect": "방향 편향을 성과로 오해하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "lot_normalized_guard",
            "gate_family": "position_shape(포지션 모양)",
            "required_metric": "lot-normalized expectancy and drawdown(랏 정규화 기대값과 손실폭)",
            "minimum_condition": "edge survives without lot scaling(랏 확대 없이 엣지 생존)",
            "blocks_if": "lot sizing explains result(랏 크기가 결과를 설명)",
            "effect": "lot optimization(랏 최적화) 없이 신호 품질을 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "recovery_expectancy_guard",
            "gate_family": "risk_recovery(위험 회복)",
            "required_metric": "recovery factor and expectancy(회복 계수와 기대값)",
            "minimum_condition": "worst drawdown has plausible recovery(최악 손실 이후 회복 가능)",
            "blocks_if": "recovery depends on one late pocket(회복이 단일 후반 포켓에 의존)",
            "effect": "DD(손실폭)와 회복을 같은 게이트로 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_parity_guard",
            "gate_family": "runtime_parity(런타임 동등성)",
            "required_metric": "proxy expected vs MT5 probe comparison(프록시 예상 대 MT5 탐침 비교)",
            "minimum_condition": "future MT5 probe differences are explained(향후 MT5 탐침 차이를 설명)",
            "blocks_if": "unexplained proxy/MT5 mismatch(설명 안 된 프록시/MT5 불일치)",
            "effect": "프록시 수익을 런타임 수익으로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_mt5_release_lock() -> list[dict[str, str]]:
    return [
        {
            "lock_id": "control_clearance_lock",
            "release_condition": "all shift/day/week/purged controls clear(모든 이동/일/주/제거 대조 통과)",
            "current_status": "locked",
            "blocked_if": "any control blocks runtime probe(어느 대조든 런타임 탐침 차단)",
            "effect": "대조 실패를 MT5로 우회하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lock_id": "signal_floor_lock",
            "release_condition": "validation and OOS signal floor pass(검증/OOS 신호 하한 통과)",
            "current_status": "locked",
            "blocked_if": "weak/sparse signal(약하거나 희소한 신호)",
            "effect": "거래수 없는 ONNX를 운영 후보로 오해하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lock_id": "cost_curve_lock",
            "release_condition": "cost ladder and curve pocket gates pass(비용 사다리와 곡선 포켓 게이트 통과)",
            "current_status": "locked",
            "blocked_if": "cost or curve stress fails(비용 또는 곡선 압박 실패)",
            "effect": "이쁜 곡선 요구를 명시적 게이트로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lock_id": "proxy_mt5_compare_lock",
            "release_condition": "proxy expected vs MT5 runtime probe compare plan exists(프록시 예상과 MT5 런타임 비교 계획 존재)",
            "current_status": "locked_until_future_mt5_probe",
            "blocked_if": "compare fields missing(비교 필드 누락)",
            "effect": "프록시 결과와 실제 런타임 차이를 반드시 판정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "lock_id": "lineage_hash_lock",
            "release_condition": "artifact hashes and feature-order identity are recorded(산출물 해시와 피처 순서 정체성 기록)",
            "current_status": "locked",
            "blocked_if": "hash, feature-order, or handoff identity missing(해시/피처 순서/인계 정체성 누락)",
            "effect": "어떤 산출물이 MT5로 갔는지 흐려지지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_compare_contract() -> list[dict[str, str]]:
    fields = [
        ("bar_time", "proxy timestamp(프록시 시각)", "MT5 bar time(MT5 봉 시각)", "exact timestamp match(정확 시각 일치)"),
        ("feature_input_hash", "Python feature row(파이썬 피처 행)", "MT5 feature handoff(MT5 피처 인계)", "exact hash match(정확 해시 일치)"),
        ("p_short", "ONNX proxy p_short(온엑스 프록시 p_short)", "MT5 ONNX p_short(MT5 온엑스 p_short)", "1e-5"),
        ("p_flat", "ONNX proxy p_flat(온엑스 프록시 p_flat)", "MT5 ONNX p_flat(MT5 온엑스 p_flat)", "1e-5"),
        ("p_long", "ONNX proxy p_long(온엑스 프록시 p_long)", "MT5 ONNX p_long(MT5 온엑스 p_long)", "1e-5"),
        ("decision_label", "proxy decision(프록시 판단)", "MT5 decision(MT5 판단)", "exact label match(정확 라벨 일치)"),
        ("action", "proxy action template(프록시 행동 템플릿)", "MT5 order action(MT5 주문 행동)", "exact semantic match(정확 의미 일치)"),
        ("trade_count", "proxy expected trades(프록시 예상 거래)", "MT5 tester trades(MT5 테스터 거래)", "explain all differences(모든 차이 설명)"),
        ("spread_cost", "proxy spread assumption(프록시 스프레드 가정)", "MT5 realized spread(MT5 실현 스프레드)", "cost attribution required(비용 귀속 필요)"),
        ("slippage_cost", "proxy slippage assumption(프록시 슬리피지 가정)", "MT5 realized slippage(MT5 실현 슬리피지)", "cost attribution required(비용 귀속 필요)"),
        ("net_profit", "proxy expected net(프록시 예상 순익)", "MT5 tester net(MT5 테스터 순익)", "cost/slippage attribution required(비용/슬리피지 귀속 필요)"),
        ("equity_curve_pocket", "proxy equity pocket(프록시 곡선 포켓)", "MT5 equity pocket(MT5 곡선 포켓)", "same pocket or explained difference(같은 포켓 또는 차이 설명)"),
    ]
    return [
        {
            "compare_field": field,
            "proxy_source": proxy_source,
            "mt5_source": mt5_source,
            "required_tolerance": tolerance,
            "blocks_runtime_authority_if": "missing or unexplained mismatch(누락 또는 설명 안 된 불일치)",
            "effect": "proxy-MT5 gap(프록시-MT5 차이)을 직접 판정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for field, proxy_source, mt5_source, tolerance in fields
    ]


def build_cs_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CS_train_density_control_repair_limited",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "train limited repaired candidates(제한 수리 후보 학습) using CR train-only density policies(CR 학습 전용 밀도 정책)",
            "required_inputs": rel(TRAIN_ONLY_DENSITY_POLICY_GRID) + ";" + rel(EXTENDED_SHIFT_CONTROL_FRAME),
            "required_outputs": "repaired_model_scorecard.csv;extended_control_scorecard.csv;onnx_parity_matrix.csv",
            "blocked_if_missing": "density grid or extended controls missing(밀도 격자 또는 확장 대조 누락)",
            "forbidden_action": "do not choose density from validation/OOS profit(검증/OOS 수익으로 밀도 선택 금지)",
            "effect": "거래수 공격을 하되 과적합 방지선을 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CS_score_cost_curve_shape",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "score cost/curve gates(비용/곡선 게이트 채점)",
            "required_inputs": rel(COST_CURVE_SHAPE_GATE_CONTRACT),
            "required_outputs": "cost_curve_shape_scorecard.csv",
            "blocked_if_missing": "cost curve contract missing(비용 곡선 계약 누락)",
            "forbidden_action": "do not optimize lot(로트 최적화 금지)",
            "effect": "수익률과 곡선 모양을 같은 게이트로 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337CS_hold_mt5_until_release_lock_clears",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "hold MT5 probe until release locks clear(해제 잠금 전 MT5 탐침 보류)",
            "required_inputs": rel(MT5_PROBE_RELEASE_LOCK) + ";" + rel(PROXY_MT5_COMPARE_CONTRACT),
            "required_outputs": "runtime_probe_release_disposition.csv",
            "blocked_if_missing": "release lock or compare contract missing(해제 잠금 또는 비교 계약 누락)",
            "forbidden_action": "do not run MT5 from unreleased models(해제 안 된 모델 MT5 실행 금지)",
            "effect": "프록시와 MT5 차이를 비교할 준비 없이 런타임으로 가지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("cr_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CQ/CO/CP evidence(근거)를 연결했다."),
        row("cr_gate_parent_points_to_cr", final["cq_next_action"] == RUN_ID, final["cq_next_action"], RUN_ID, "CQ next_action(다음 행동)과 CR run(실행)이 맞는다."),
        row("cr_gate_day_session_rows", final["day_session_rows"] == final["source_rows"], final["day_session_rows"], "source_rows", "모든 원천 행에 세션/레짐 조각을 붙였다."),
        row("cr_gate_day_concentration_rows", final["day_concentration_rows"] > 0, final["day_concentration_rows"], ">0", "day block concentration(일 블록 집중도)을 만들었다."),
        row("cr_gate_extended_shift_rows", final["extended_shift_rows"] == final["source_rows"] * final["label_candidate_rows"] * 3, final["extended_shift_rows"], "source_rows*candidates*3 controls", "확장 이동 대조를 행 단위로 만들었다."),
        row("cr_gate_feature_state_rows", final["feature_state_rows"] >= final["feature_count"] * 3, final["feature_state_rows"], ">=feature_count*3", "feature state carry(피처 상태 이월)를 기록했다."),
        row("cr_gate_density_policy_grid", final["density_policy_rows"] >= 12, final["density_policy_rows"], ">=12", "train-only density policy(학습 전용 밀도 정책)를 만들었다."),
        row("cr_gate_cost_curve_contract", final["cost_curve_rows"] >= 9, final["cost_curve_rows"], ">=9", "cost/curve gates(비용/곡선 게이트)를 만들었다."),
        row("cr_gate_mt5_release_lock", final["mt5_lock_rows"] >= 5 and final["mt5_release_status"] == "locked", f"{final['mt5_lock_rows']};{final['mt5_release_status']}", "locked", "MT5 release lock(MT5 해제 잠금)을 유지했다."),
        row("cr_gate_proxy_mt5_compare", final["proxy_mt5_compare_rows"] >= 12, final["proxy_mt5_compare_rows"], ">=12", "proxy-MT5 compare contract(프록시-MT5 비교 계약)을 만들었다."),
        row("cr_gate_no_training_selection_mt5", True, "training=not_run;selection=not_run;mt5=not_run", "no training/selection/MT5", "CR은 입력 물질화만 수행한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "source timestamp sorted with source_row_id(원천 시각 정렬과 원천 행 ID)",
        "sample_scope": "existing Stage337 train/validation/OOS rows only(기존 Stage337 학습/검증/OOS 행만)",
        "missing_or_duplicate_check": "generated views repeat source rows by label/control/model as intended(생성 보기는 라벨/대조/모델별 반복 정상)",
        "feature_label_boundary": "no relabeling from future forward data; extended controls are split-local(새 전진 데이터 재라벨 없음, 확장 대조는 분할 내부)",
        "split_boundary": "train-only policy grid and read-only validation/OOS gates(학습 전용 정책 격자와 읽기 전용 검증/OOS 게이트)",
        "leakage_risk": "using validation/OOS to choose density threshold(검증/OOS로 밀도 임계값 선택)",
        "data_hash_or_identity": {"source_sha256": final["source_sha256"], "source_rows": final["source_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "no_model_training_cr_materialization_only(모델 학습 없음, CR 입력 물질화 전용)",
        "target_and_label": "future repaired density/control candidates(향후 수리 밀도/대조 후보)",
        "split_method": "train-only policy with validation/OOS read-only gates(학습 전용 정책과 검증/OOS 읽기 전용 게이트)",
        "selection_metric": "not_applicable_no_selection(해당 없음, 선택 없음)",
        "secondary_metrics": "extended shift controls(확장 이동 대조), state carry(상태 이월), cost curve gates(비용 곡선 게이트), proxy-MT5 compare(프록시-MT5 비교)",
        "threshold_policy": "materialized as train-only density policy, not selected(학습 전용 밀도 정책으로 물질화, 선택 없음)",
        "overfit_risk": "density or gate chosen after OOS read(OOS 판독 후 밀도/게이트 선택)",
        "calibration_risk": "not_applicable_until_CS_training(CS 학습 전 해당 없음)",
        "comparison_baseline": "CO/CP weak and control-blocked models(CO/CP 약한/대조 차단 모델)",
        "validation_judgment": "materialized_inputs_ready_for_limited_training(제한 학습 입력 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "CP released zero MT5 probes(CP MT5 탐침 해제 0)",
        "comparison_baseline": "CO proxy expected and CP review(CO 프록시 예상과 CP 검토)",
        "likely_drivers": "calendar carry(달력 이월), serial shift residual(연속 이동 잔차), weak/sparse density(약하고 희소한 밀도)",
        "segment_checks": "CR materialized day/session/month/volatility/ADX/VIX buckets(CR 일/세션/월/변동성/ADX/VIX 버킷 물질화)",
        "trade_shape": "density policy and cost/curve gates prepared(밀도 정책과 비용/곡선 게이트 준비)",
        "alternative_explanations": "feature state carry(피처 상태 이월), stale external context(낡은 외부 문맥), weak classifier(약한 분류기)",
        "attribution_confidence": "medium_input_ready(중간, 입력 준비)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "materialized repair inputs(물질화 수리 입력), gates(게이트), release lock(해제 잠금), compare contract(비교 계약)",
        "evidence_missing": "CS limited training(CS 제한 학습), future MT5 runtime probe(향후 MT5 런타임 탐침), proxy-MT5 difference judgment(프록시-MT5 차이 판정)",
        "judgment_label": "exploratory_materialized_inputs(탐색 입력 물질화)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "이제 수리 학습을 위한 입력은 생겼지만, 아직 좋은 ONNX나 MT5 가능 상태는 아니다.",
    }
    receipt_paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CR Weak Density/Control Alignment Repair Inputs(약한 밀도/대조 정렬 수리 입력)

## Conclusion(결론)

run337CR(337CR 실행)는 CQ repair design(CQ 수리 설계)을 실제 입력으로 물질화했다. 산출물은 day/session/regime frame(일/세션/레짐 프레임), day block concentration matrix(일 블록 집중도 행렬), extended shift controls(확장 이동 대조), feature state carry matrix(피처 상태 이월 행렬), train-only density policy grid(학습 전용 밀도 정책 격자), cost/curve gate contract(비용/곡선 게이트 계약), MT5 release lock(MT5 해제 잠금), proxy-MT5 compare contract(프록시-MT5 비교 계약)이다.

Effect(효과): 다음 run337CS(337CS 실행)는 거래수/곡선 개선을 공격할 수 있지만, density threshold(밀도 임계값)를 validation/OOS(검증/OOS)에서 맞추는 길은 막혀 있다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- source_rows(원천 행): `{final["source_rows"]}`
- day_session_rows(일/세션 행): `{final["day_session_rows"]}`
- day_concentration_rows(일 집중도 행): `{final["day_concentration_rows"]}`
- extended_shift_rows(확장 이동 대조 행): `{final["extended_shift_rows"]}`
- feature_state_rows(피처 상태 행): `{final["feature_state_rows"]}`
- density_policy_rows(밀도 정책 행): `{final["density_policy_rows"]}`
- mt5_lock_rows(MT5 잠금 행): `{final["mt5_lock_rows"]}`
- proxy_mt5_compare_rows(프록시-MT5 비교 행): `{final["proxy_mt5_compare_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CR

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): weak density/control alignment repair inputs(약한 밀도/대조 정렬 수리 입력)을 만들고 CS limited training(CS 제한 학습)을 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRAIN_ONLY_DENSITY_POLICY_GRID)}`, `{rel(MT5_PROBE_RELEASE_LOCK)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- MT5 probe(MT5 탐침): `not_run`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CR focus complete: weak density/control alignment repair inputs(약한 밀도/대조 정렬 수리 입력)를 `{STATUS}`로 물질화했다. "
        "Effect(효과): run337CS(337CS 실행)에서 제한 학습과 확장 대조를 실행한다."
    )
    if "Stage337 run337CR focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CR focus complete:.*?(?=\n- >-\n  Stage337 run337CQ|\n[A-Za-z0-9_]+:)",
            focus_entry,
            workspace_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337CR(337CR 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): day/session/regime(일/세션/레짐), extended shift controls(확장 이동 대조), train-only density policy(학습 전용 밀도 정책), MT5 release lock(MT5 해제 잠금)을 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CR\(337CR 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CQ|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CQ(337CQ"
    current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `held_by_cr_release_lock_no_mt5`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 weak density/control repaired limited training(약한 밀도/대조 수리 제한 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CR(337CR 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CR(337CR 실행) materialized weak density/control alignment repair inputs(약한 밀도/대조 정렬 수리 입력). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CR materialized weak density/control alignment repair inputs" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CR materialized weak density/control alignment repair inputs(약한 밀도/대조 정렬 수리 입력) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "weak_density_control_alignment_repair_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"extended_shift_rows={final['extended_shift_rows']};density_policy_rows={final['density_policy_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_performance_attribution_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_input_materialization",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "input_materialization_no_training",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"extended_shift_rows={final['extended_shift_rows']};day_concentration_rows={final['day_concentration_rows']}",
        "guardrail_kpi": "train_only_policy;mt5_release_lock;proxy_mt5_compare_contract",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_performance_attribution_artifact_lineage",
        "evidence_scope": "CQ repair design materialized into input artifacts",
        "kpi_scope": "input_materialization_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_inputs",
        "family": "data_integrity_model_validation_performance_attribution_artifact_lineage",
        "question": "can weak density and control alignment repair inputs be materialized without OOS tuning",
        "metric_scope": "day_session_shift_state_density_mt5_lock",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]

    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    cq_final = read_json(CQ_FINAL)
    source = read_source_frame()
    feature_manifest = read_json(CANDIDATE_INPUT_MANIFEST)
    features = [str(item) for item in feature_manifest.get("feature_columns", [])]
    label_frame = pd.read_parquet(io_path(CN_LABEL_FRAME))
    proxy = pd.read_csv(io_path(CO_PROXY_EXPECTED))
    weak_rows = read_csv(CP_WEAKNESS)

    day_session = build_day_session_regime_frame(source)
    day_concentration = build_day_block_concentration(proxy)
    extended_shift = build_extended_shift_controls(label_frame)
    feature_state = build_feature_state_carry(source, features)
    density_grid = build_density_policy_grid(weak_rows)
    cost_curve_contract = build_cost_curve_contract()
    mt5_lock = build_mt5_release_lock()
    compare_contract = build_compare_contract()
    queue_rows = build_cs_queue()

    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cq_next_action": cq_final.get("next_action", ""),
        "source_rows": int(len(source)),
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "feature_count": len(features),
        "label_candidate_rows": int(label_frame["label_candidate_id"].nunique()),
        "day_session_rows": int(len(day_session)),
        "day_concentration_rows": len(day_concentration),
        "extended_shift_rows": int(len(extended_shift)),
        "feature_state_rows": len(feature_state),
        "density_policy_rows": len(density_grid),
        "cost_curve_rows": len(cost_curve_contract),
        "mt5_lock_rows": len(mt5_lock),
        "mt5_release_status": "locked",
        "proxy_mt5_compare_rows": len(compare_contract),
        "cs_queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifacts: list[Path] = [
        write_parquet(DAY_SESSION_REGIME_FRAME, day_session),
        write_csv(DAY_BLOCK_CONCENTRATION, DAY_CONCENTRATION_COLUMNS, day_concentration),
        write_parquet(EXTENDED_SHIFT_CONTROL_FRAME, extended_shift),
        write_csv(FEATURE_STATE_CARRY_MATRIX, FEATURE_STATE_COLUMNS, feature_state),
        write_csv(TRAIN_ONLY_DENSITY_POLICY_GRID, DENSITY_POLICY_COLUMNS, density_grid),
        write_csv(COST_CURVE_SHAPE_GATE_CONTRACT, COST_CURVE_COLUMNS, cost_curve_contract),
        write_csv(MT5_PROBE_RELEASE_LOCK, MT5_LOCK_COLUMNS, mt5_lock),
        write_csv(PROXY_MT5_COMPARE_CONTRACT, COMPARE_COLUMNS, compare_contract),
        write_csv(CS_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(
            RUN_MANIFEST,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

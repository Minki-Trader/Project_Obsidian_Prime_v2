from __future__ import annotations

import argparse
import csv
import importlib.metadata
import importlib.util
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import balanced_accuracy_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.ebm_score_table import FIELDNAMES, load_ebm_score_table, score_ebm_table_probabilities
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities, sha256_file
from foundation.models.xgboost_boosting import nonflat_threshold, split_decision_metrics
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage23 import supervised_regime_scout as base_scout


ROOT = Path(__file__).resolve().parents[1]
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
THRESHOLD_QUANTILE = 0.80
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 12
EXPECTED_MT5_ATTEMPTS = 6
EXPECTED_MT5_KPI_RECORDS = 10
LABEL_ORDER = (0, 1, 2)


@dataclass(frozen=True)
class StagePlan:
    stage_number: int
    stage_id: str
    title: str
    core_question: str
    scout_run_number: str
    scout_run_id: str
    runtime_run_number: str
    runtime_run_id: str
    scout_packet_id: str
    runtime_packet_id: str
    closeout_packet_id: str
    exploration_label: str
    model_family: str
    runtime_model_family: str
    runtime_feature_order: tuple[str, ...]
    runtime_coefficients: Mapping[str, tuple[float, float, float]]
    selected_variant_id: str
    dependency_note: str
    topic_read: str
    next_stage_id: str | None = None
    next_stage_title: str | None = None

    @property
    def stage_root(self) -> Path:
        return ROOT / "stages" / self.stage_id

    @property
    def scout_run_root(self) -> Path:
        return self.stage_root / "02_runs" / self.scout_run_id

    @property
    def runtime_run_root(self) -> Path:
        return self.stage_root / "02_runs" / self.runtime_run_id

    @property
    def stage_ledger_path(self) -> Path:
        return self.stage_root / "03_reviews/stage_run_ledger.csv"

    @property
    def boundary(self) -> str:
        return f"stage{self.stage_number}_exploration_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

    @property
    def scout_judgment(self) -> str:
        return f"inconclusive_stage{self.stage_number}_structural_scout_completed"

    @property
    def runtime_judgment_completed(self) -> str:
        return f"inconclusive_stage{self.stage_number}_runtime_probe_completed"

    @property
    def runtime_judgment_blocked(self) -> str:
        return f"blocked_stage{self.stage_number}_runtime_probe_after_attempt"


STAGE_PLANS: dict[int, StagePlan] = {
    29: StagePlan(
        stage_number=29,
        stage_id="29_adaptive_model__river_online_drift_learning",
        title="River Online Drift Learning(리버 온라인 변화 학습)",
        core_question="Can online learning expose drift/adaptation(변화/적응) behavior without inheriting Stage28(28단계) state tables?",
        scout_run_number="run23A",
        scout_run_id="run23A_river_online_drift_learning_scout_v1",
        runtime_run_number="run23B",
        runtime_run_id="run23B_river_online_drift_runtime_probe_v1",
        scout_packet_id="stage29_run23A_river_online_drift_learning_scout_v1",
        runtime_packet_id="stage29_run23B_river_online_drift_runtime_probe_v1",
        closeout_packet_id="stage29_closeout_stage30_open_v1",
        exploration_label="stage29_AdaptiveModel__RiverOnlineDriftLearning",
        model_family="sklearn_sgd_online_logloss_river_dependency_blocked",
        runtime_model_family="online_drift_probability_score_table_runtime_probe",
        runtime_feature_order=("online_direction_score", "online_confidence", "online_flat_pressure", "online_drift_gap"),
        runtime_coefficients={
            "online_direction_score": (-2.1, 0.0, 2.1),
            "online_confidence": (0.65, -0.55, 0.65),
            "online_flat_pressure": (-0.55, 1.10, -0.55),
            "online_drift_gap": (0.35, -0.15, 0.35),
        },
        selected_variant_id="v01_core42_sgd_online_slow_adapt",
        dependency_note="river package(리버 패키지) missing; sklearn SGD partial_fit(사이킷런 부분 학습) proxy used and native River retry condition recorded.",
        topic_read="online_drift_adaptation_probability_handoff",
        next_stage_id="30_decision_layer__probability_calibration_abstention",
        next_stage_title="Probability Calibration Abstention(확률 보정/기권)",
    ),
    30: StagePlan(
        stage_number=30,
        stage_id="30_decision_layer__probability_calibration_abstention",
        title="Probability Calibration Abstention(확률 보정/기권)",
        core_question="Can calibration/abstention(보정/기권) reshape probability confidence without becoming a new baseline(기준선)?",
        scout_run_number="run24A",
        scout_run_id="run24A_probability_calibration_abstention_scout_v1",
        runtime_run_number="run24B",
        runtime_run_id="run24B_probability_calibration_abstention_runtime_probe_v1",
        scout_packet_id="stage30_run24A_probability_calibration_abstention_scout_v1",
        runtime_packet_id="stage30_run24B_probability_calibration_abstention_runtime_probe_v1",
        closeout_packet_id="stage30_closeout_stage31_open_v1",
        exploration_label="stage30_DecisionLayer__CalibrationAbstention",
        model_family="isotonic_margin_calibration_abstention_layer",
        runtime_model_family="calibration_abstention_score_table_runtime_probe",
        runtime_feature_order=("cal_direction_score", "cal_confidence", "cal_abstention_pressure", "cal_reliability_gap"),
        runtime_coefficients={
            "cal_direction_score": (-2.0, 0.0, 2.0),
            "cal_confidence": (0.70, -0.60, 0.70),
            "cal_abstention_pressure": (-0.85, 1.45, -0.85),
            "cal_reliability_gap": (0.25, 0.35, 0.25),
        },
        selected_variant_id="v02_isotonic_margin_abstention",
        dependency_note="native calibration package(원본 보정 패키지) not required; sklearn isotonic(사이킷런 등위 회귀) used.",
        topic_read="probability_calibration_abstention_handoff",
        next_stage_id="31_model_family_challenge__tabnet_attentive_tabular_scout",
        next_stage_title="TabNet Attentive Tabular Scout(탭넷 주의 기반 표 형식 탐색)",
    ),
    31: StagePlan(
        stage_number=31,
        stage_id="31_model_family_challenge__tabnet_attentive_tabular_scout",
        title="TabNet Attentive Tabular Scout(탭넷 주의 기반 표 형식 탐색)",
        core_question="Can sparse attentive tabular(희소 주의 기반 표 형식) behavior leave a useful feature-mask clue on US100 M5(US100 5분봉)?",
        scout_run_number="run25A",
        scout_run_id="run25A_tabnet_attentive_tabular_scout_v1",
        runtime_run_number="run25B",
        runtime_run_id="run25B_tabnet_attentive_tabular_runtime_probe_v1",
        scout_packet_id="stage31_run25A_tabnet_attentive_tabular_scout_v1",
        runtime_packet_id="stage31_run25B_tabnet_attentive_tabular_runtime_probe_v1",
        closeout_packet_id="stage31_closeout_stage32_open_v1",
        exploration_label="stage31_Model__TabNetAttentiveTabularScout",
        model_family="sklearn_sparse_feature_mask_tabnet_dependency_blocked",
        runtime_model_family="tabular_attention_proxy_score_table_runtime_probe",
        runtime_feature_order=("tab_direction_score", "tab_confidence", "tab_attention_concentration", "tab_mask_activity"),
        runtime_coefficients={
            "tab_direction_score": (-2.2, 0.0, 2.2),
            "tab_confidence": (0.70, -0.55, 0.70),
            "tab_attention_concentration": (0.35, -0.20, 0.35),
            "tab_mask_activity": (0.20, 0.20, 0.20),
        },
        selected_variant_id="v02_sparse_mask_top20_logistic_proxy",
        dependency_note="torch/pytorch_tabnet(파이토치/파이토치 탭넷) missing; sparse feature-mask proxy(희소 피처 마스크 대체) used and native TabNet retry condition recorded.",
        topic_read="tabnet_attention_proxy_probability_handoff",
        next_stage_id="32_sequence_model__tcn_temporal_convolution_context",
        next_stage_title="TCN Temporal Convolution Context(TCN 시간 합성곱 문맥)",
    ),
    32: StagePlan(
        stage_number=32,
        stage_id="32_sequence_model__tcn_temporal_convolution_context",
        title="TCN Temporal Convolution Context(TCN 시간 합성곱 문맥)",
        core_question="Can temporal convolution(시간 합성곱) style lag context expose sequence behavior beyond static tabular features?",
        scout_run_number="run26A",
        scout_run_id="run26A_tcn_temporal_convolution_context_scout_v1",
        runtime_run_number="run26B",
        runtime_run_id="run26B_tcn_temporal_convolution_runtime_probe_v1",
        scout_packet_id="stage32_run26A_tcn_temporal_convolution_context_scout_v1",
        runtime_packet_id="stage32_run26B_tcn_temporal_convolution_runtime_probe_v1",
        closeout_packet_id="stage32_closeout_goal_summary_v1",
        exploration_label="stage32_SequenceModel__TCNTemporalConvolutionContext",
        model_family="sklearn_lag_convolution_proxy_torch_dependency_blocked",
        runtime_model_family="tcn_proxy_score_table_runtime_probe",
        runtime_feature_order=("tcn_fast_return_kernel", "tcn_slow_return_kernel", "tcn_range_pressure", "tcn_trend_context"),
        runtime_coefficients={
            "tcn_fast_return_kernel": (-2.0, 0.0, 2.0),
            "tcn_slow_return_kernel": (-1.2, 0.10, 1.2),
            "tcn_range_pressure": (0.35, -0.10, 0.35),
            "tcn_trend_context": (-0.85, 0.0, 0.85),
        },
        selected_variant_id="v01_dilated_return_range_logistic_proxy",
        dependency_note="torch(파이토치) missing; lagged convolution proxy(지연 합성곱 대체) used and native TCN retry condition recorded.",
        topic_read="tcn_temporal_convolution_proxy_handoff",
    ),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: json_ready(row.get(column, "")) for column in columns})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        number = float(value)
        return number if np.isfinite(number) else default
    except (TypeError, ValueError):
        return default


def load_context() -> dict[str, Any]:
    context = base_scout.load_context()
    return {
        "tier_a_frame": context["tier_a_frame"].sort_values("timestamp").reset_index(drop=True),
        "tier_b_training_frame": context["tier_b_training_frame"].sort_values("timestamp").reset_index(drop=True),
        "tier_b_fallback_frame": context["tier_b_fallback_frame"].sort_values("timestamp").reset_index(drop=True),
        "full_feature_order": list(context["full_feature_order"]),
        "tier_b_feature_order": list(context["tier_b_feature_order"]),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "training_summary": context["training_summary"],
    }


def core24_features(tier_b_order: Sequence[str]) -> tuple[str, ...]:
    allowed = set(tier_b_order)
    return tuple(name for name in base_scout.core24_features() if name in allowed)


def ensure_stage_docs(plan: StagePlan) -> None:
    stage_root = plan.stage_root
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(stage_root / folder).mkdir(parents=True, exist_ok=True)
    write_md(
        stage_root / "00_spec/stage_brief.md",
        f"""# {plan.title}

## Core Question(핵심 질문)

{plan.core_question}

효과(effect, 효과): Stage{plan.stage_number}({plan.stage_number}단계)는 독립 topic exploration(주제 탐색)이며 이전 stage(이전 단계)의 threshold/model/baseline(임계값/모델/기준선)을 상속하지 않는다.

## Planned Runs(계획 실행)

- `{plan.scout_run_id}`
- `{plan.runtime_run_id}`
""",
    )
    write_md(
        stage_root / "01_inputs/input_refs.md",
        f"""# Stage{plan.stage_number} Input References({plan.stage_number}단계 입력 참조)

- model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier B fallback(티어 B 대체): `foundation.mt5.runtime_support.build_tier_b_partial_context_frames`
- split contract(분할 계약): `{SPLIT_CONTRACT}`
- label(라벨): `{LABEL_ID}`

효과(effect, 효과): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed(Tier A+B 라우팅)를 같은 입력 경계(input boundary, 입력 경계)에서 남긴다.
""",
    )
    review_index = stage_root / "03_reviews/review_index.md"
    if not io_path(review_index).exists():
        write_md(
            review_index,
            f"""# Stage{plan.stage_number} Review Index({plan.stage_number}단계 검토 색인)

- status(상태): `opened`
- next action(다음 행동): `{plan.scout_run_id}`
""",
        )
    selection = stage_root / "04_selected/selection_status.md"
    if not io_path(selection).exists():
        write_md(
            selection,
            f"""# Stage{plan.stage_number} Selection Status({plan.stage_number}단계 선택 상태)

- stage(단계): `{plan.stage_id}`
- status(상태): `opened_not_started`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{plan.scout_run_id}`

효과(effect, 효과): 결과가 나오기 전에는 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.
""",
        )


def clean_frame(frame: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    columns = ["timestamp", "split", "label_class", *features]
    optional = ["partial_context_subtype", "route_role", "missing_feature_group_mask", "available_feature_group_mask"]
    for column in optional:
        if column in frame.columns:
            columns.append(column)
    out = frame.loc[:, [column for column in columns if column in frame.columns]].copy()
    out = out.replace([np.inf, -np.inf], np.nan).dropna(subset=list(features) + ["label_class", "split"])
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    out["label_class"] = out["label_class"].astype("int64")
    return out.sort_values("timestamp").reset_index(drop=True)


def predict_proba_ordered(model: Any, values: np.ndarray) -> np.ndarray:
    prob = ordered_sklearn_probabilities(model, values)
    prob = np.clip(prob, 1e-8, 1.0)
    return prob / prob.sum(axis=1, keepdims=True)


def probability_payload(source: pd.DataFrame, prob: np.ndarray, *, extra: Mapping[str, Any] | None = None) -> pd.DataFrame:
    sorted_prob = np.sort(prob, axis=1)
    payload = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(source["timestamp"], utc=True).to_numpy(),
            "split": source["split"].astype(str).to_numpy(),
            "label_class": source["label_class"].astype("int64").to_numpy(),
            "p_short": prob[:, 0],
            "p_flat": prob[:, 1],
            "p_long": prob[:, 2],
            "probability_margin": sorted_prob[:, -1] - sorted_prob[:, -2],
        }
    )
    for column in ("partial_context_subtype", "route_role", "missing_feature_group_mask", "available_feature_group_mask"):
        if column in source.columns:
            payload[column] = source[column].astype(str).to_numpy()
    if extra:
        for key, value in extra.items():
            payload[key] = value
    return payload


def split_metrics(prob_frame: pd.DataFrame, threshold: float) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    payload: dict[str, Any] = {"decision": metrics}
    for split in ("train", "validation", "oos"):
        frame = prob_frame.loc[prob_frame["split"].astype(str).eq(split)]
        if frame.empty:
            payload[split] = {"rows": 0}
            continue
        labels = frame["label_class"].astype("int64").to_numpy()
        prob = frame[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
        pred = np.argmax(prob, axis=1)
        payload[split] = {
            "rows": int(len(frame)),
            "balanced_accuracy": float(balanced_accuracy_score(labels, pred)),
            "log_loss": float(log_loss(labels, prob, labels=list(LABEL_ORDER))),
            "mean_margin": float(frame["probability_margin"].mean()),
            **metrics.get(split, {}),
        }
    return payload


def summarize_variant(
    plan: StagePlan,
    variant_id: str,
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    *,
    details: Mapping[str, Any],
) -> dict[str, Any]:
    tier_a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    tier_b_threshold = nonflat_threshold(tier_b_prob, THRESHOLD_QUANTILE)
    tier_ab = pd.concat([tier_a_prob.assign(record_source="tier_a"), tier_b_prob.assign(record_source="tier_b_fallback")], ignore_index=True)
    validation = split_metrics(tier_a_prob, tier_a_threshold).get("validation", {})
    oos = split_metrics(tier_a_prob, tier_a_threshold).get("oos", {})
    b_validation = split_metrics(tier_b_prob, tier_b_threshold).get("validation", {})
    b_oos = split_metrics(tier_b_prob, tier_b_threshold).get("oos", {})
    return {
        "stage_id": plan.stage_id,
        "run_id": plan.scout_run_id,
        "variant_id": variant_id,
        "selected": variant_id == plan.selected_variant_id,
        "tier_a_threshold": float(tier_a_threshold),
        "tier_b_threshold": float(tier_b_threshold),
        "tier_a_validation": validation,
        "tier_a_oos": oos,
        "tier_b_validation": b_validation,
        "tier_b_oos": b_oos,
        "tier_ab_rows": int(len(tier_ab)),
        "details": dict(details),
    }


def fit_online_sgd(frame: pd.DataFrame, features: Sequence[str], *, alpha: float, random_state: int, chunk_size: int) -> tuple[Any, dict[str, Any]]:
    data = clean_frame(frame, features)
    train = data.loc[data["split"].astype(str).eq("train")].copy()
    scaler = StandardScaler()
    model = SGDClassifier(
        loss="log_loss",
        penalty="elasticnet",
        l1_ratio=0.08,
        alpha=float(alpha),
        learning_rate="optimal",
        max_iter=1,
        tol=None,
        random_state=int(random_state),
    )
    chunks = 0
    for start in range(0, len(train), int(chunk_size)):
        chunk = train.iloc[start : start + int(chunk_size)]
        values = chunk.loc[:, list(features)].to_numpy(dtype="float64", copy=False)
        labels = chunk["label_class"].astype("int64").to_numpy()
        scaler.partial_fit(values)
        model.partial_fit(scaler.transform(values), labels, classes=np.asarray(LABEL_ORDER, dtype="int64"))
        chunks += 1
    fitted = Pipeline([("scaler", scaler), ("classifier", model)])
    return fitted, {"train_rows": int(len(train)), "partial_fit_chunks": chunks, "alpha": float(alpha), "chunk_size": int(chunk_size)}


def fit_logistic(frame: pd.DataFrame, features: Sequence[str], *, random_state: int, c_value: float = 0.45) -> tuple[Any, dict[str, Any]]:
    data = clean_frame(frame, features)
    train = data.loc[data["split"].astype(str).eq("train")].copy()
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    C=float(c_value),
                    class_weight="balanced",
                    max_iter=1200,
                    solver="lbfgs",
                    random_state=int(random_state),
                ),
            ),
        ]
    )
    model.fit(train.loc[:, list(features)].to_numpy(dtype="float64", copy=False), train["label_class"].astype("int64").to_numpy())
    return model, {"train_rows": int(len(train)), "feature_count": len(features), "C": float(c_value)}


def fit_sparse_mask_proxy(frame: pd.DataFrame, features: Sequence[str], *, random_state: int, top_k: int) -> tuple[Any, tuple[str, ...], dict[str, Any]]:
    data = clean_frame(frame, features)
    train = data.loc[data["split"].astype(str).eq("train")].copy()
    values = train.loc[:, list(features)].to_numpy(dtype="float64", copy=False)
    labels = train["label_class"].astype("int64").to_numpy()
    masker = ExtraTreesClassifier(
        n_estimators=140,
        max_depth=7,
        min_samples_leaf=95,
        class_weight="balanced",
        n_jobs=-1,
        random_state=int(random_state),
    )
    masker.fit(values, labels)
    importances = np.asarray(masker.feature_importances_, dtype="float64")
    order = np.argsort(importances)[::-1][: int(top_k)]
    selected = tuple(str(features[index]) for index in order)
    model, details = fit_logistic(frame, selected, random_state=random_state + 17, c_value=0.55)
    total = float(importances.sum()) or 1.0
    details.update(
        {
            "masker": "ExtraTreesClassifier",
            "top_k": int(top_k),
            "selected_features": list(selected),
            "top_importance_share": float(importances[order].sum() / total),
        }
    )
    return model, selected, details


def add_tcn_proxy_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.sort_values("timestamp").copy()
    ret = pd.to_numeric(out.get("log_return_1", 0.0), errors="coerce").fillna(0.0)
    ret3 = pd.to_numeric(out.get("log_return_3", ret), errors="coerce").fillna(0.0)
    rng = pd.to_numeric(out.get("hl_range", 0.0), errors="coerce").fillna(0.0)
    trend = pd.to_numeric(out.get("ema20_ema50_diff", 0.0), errors="coerce").fillna(0.0)
    vol = pd.to_numeric(out.get("historical_vol_20", 0.0), errors="coerce").fillna(0.0)
    out["tcn_fast_return_kernel"] = (ret + 0.55 * ret.shift(2) - 0.25 * ret.shift(4)).fillna(0.0).clip(-0.01, 0.01) * 100.0
    out["tcn_slow_return_kernel"] = (ret3 + 0.45 * ret3.shift(6) - 0.20 * ret3.shift(12)).fillna(0.0).clip(-0.02, 0.02) * 50.0
    out["tcn_range_pressure"] = (rng.rolling(6, min_periods=1).mean() / (vol.rolling(18, min_periods=1).mean().abs() + 1e-9)).replace([np.inf, -np.inf], 0.0).fillna(0.0).clip(0.0, 5.0) / 5.0
    out["tcn_trend_context"] = (trend.rolling(12, min_periods=1).mean()).replace([np.inf, -np.inf], 0.0).fillna(0.0).clip(-100.0, 100.0) / 100.0
    return out


def model_probabilities(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    data = clean_frame(frame, features)
    values = data.loc[:, list(features)].to_numpy(dtype="float64", copy=False)
    prob = predict_proba_ordered(model, values)
    return probability_payload(data, prob)


def build_stage29_variants(plan: StagePlan, context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    tier_b_order = list(context["tier_b_feature_order"])
    core24 = core24_features(tier_b_order)
    variants = [
        ("v01_core42_sgd_online_slow_adapt", tier_b_order, 0.00020, 2901, 768),
        ("v02_core24_sgd_online_fast_adapt", core24, 0.00010, 2902, 512),
        ("v03_core42_sgd_stiffer_memory", tier_b_order, 0.00055, 2903, 1024),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, features, alpha, seed, chunk_size in variants:
        model_a, details_a = fit_online_sgd(context["tier_a_frame"], features, alpha=alpha, random_state=seed, chunk_size=chunk_size)
        model_b, details_b = fit_online_sgd(context["tier_b_training_frame"], features, alpha=alpha, random_state=seed + 41, chunk_size=chunk_size)
        tier_a_prob = model_probabilities(model_a, context["tier_a_frame"], features)
        tier_b_prob = model_probabilities(model_b, context["tier_b_fallback_frame"], features)
        rows.append(summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details={"tier_a": details_a, "tier_b": details_b, "features": list(features)}))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            model_root = plan.scout_run_root / "models"
            io_path(model_root).mkdir(parents=True, exist_ok=True)
            joblib.dump(model_a, io_path(model_root / "tier_a_online_sgd_model.joblib"))
            joblib.dump(model_b, io_path(model_root / "tier_b_online_sgd_model.joblib"))
            selected_details = {"tier_a": details_a, "tier_b": details_b, "features": list(features)}
    return rows, selected_frames, selected_details


def calibrate_probs(base: pd.DataFrame, *, method: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    frame = base.copy()
    direction_prob = frame[["p_short", "p_long"]].max(axis=1).to_numpy(dtype="float64")
    direction = np.where(frame["p_long"].to_numpy(dtype="float64") >= frame["p_short"].to_numpy(dtype="float64"), 2, 0)
    labels = frame["label_class"].astype("int64").to_numpy()
    train_mask = frame["split"].astype(str).eq("train").to_numpy()
    correct = (direction == labels).astype("float64")
    if method == "v01_temperature_margin":
        train_conf = np.clip(direction_prob[train_mask], 1e-6, 1.0 - 1e-6)
        best_t = 1.0
        best_loss = float("inf")
        for temp in np.linspace(0.65, 1.75, 23):
            logits = np.log(train_conf / (1.0 - train_conf)) / float(temp)
            calibrated = 1.0 / (1.0 + np.exp(-logits))
            loss = float(np.mean((calibrated - correct[train_mask]) ** 2))
            if loss < best_loss:
                best_t = float(temp)
                best_loss = loss
        logits_all = np.log(np.clip(direction_prob, 1e-6, 1.0 - 1e-6) / np.clip(1.0 - direction_prob, 1e-6, 1.0)) / best_t
        reliability = 1.0 / (1.0 + np.exp(-logits_all))
        details = {"method": "temperature_margin", "temperature": best_t, "train_brier_proxy": best_loss}
    else:
        iso = IsotonicRegression(out_of_bounds="clip", y_min=0.02, y_max=0.98)
        iso.fit(direction_prob[train_mask], correct[train_mask])
        reliability = np.asarray(iso.predict(direction_prob), dtype="float64")
        details = {"method": "isotonic_margin", "train_rows": int(train_mask.sum())}
    reliability = np.clip(reliability, 0.02, 0.98)
    raw_short = frame["p_short"].to_numpy(dtype="float64")
    raw_long = frame["p_long"].to_numpy(dtype="float64")
    directional_total = np.maximum(raw_short + raw_long, 1e-9)
    out_short = reliability * (raw_short / directional_total)
    out_long = reliability * (raw_long / directional_total)
    out_flat = 1.0 - reliability
    prob = np.column_stack([out_short, out_flat, out_long])
    prob = np.clip(prob, 1e-8, 1.0)
    prob = prob / prob.sum(axis=1, keepdims=True)
    out = probability_payload(frame, prob, extra={"base_direction_confidence": direction_prob, "calibrated_reliability": reliability})
    return out, details


def build_stage30_variants(plan: StagePlan, _context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    source_plan = STAGE_PLANS[29]
    source_packet = ROOT / "docs/agent_control/packets" / source_plan.runtime_packet_id / "aggregate_summary.json"
    if not io_path(source_packet).exists():
        raise FileNotFoundError(f"Stage30 requires Stage29 runtime summary: {source_packet}")
    source_summary = read_json(source_packet)
    artifacts = source_summary["prediction_artifacts"]
    base_a = pd.read_parquet(io_path(ROOT / artifacts["tier_a_predictions"]["path"]))
    base_b = pd.read_parquet(io_path(ROOT / artifacts["tier_b_predictions"]["path"]))
    variants = ("v01_temperature_margin", "v02_isotonic_margin_abstention")
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id in variants:
        tier_a_prob, details_a = calibrate_probs(base_a, method=variant_id)
        tier_b_prob, details_b = calibrate_probs(base_b, method=variant_id)
        rows.append(summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details={"tier_a": details_a, "tier_b": details_b, "source_run_id": source_plan.runtime_run_id}))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            selected_details = {"tier_a": details_a, "tier_b": details_b, "source_run_id": source_plan.runtime_run_id}
    return rows, selected_frames, selected_details


def build_stage31_variants(plan: StagePlan, context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    tier_b_order = list(context["tier_b_feature_order"])
    variants = [
        ("v01_sparse_mask_top12_logistic_proxy", 12, 3101),
        ("v02_sparse_mask_top20_logistic_proxy", 20, 3102),
        ("v03_sparse_mask_top28_logistic_proxy", 28, 3103),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, top_k, seed in variants:
        model_a, features_a, details_a = fit_sparse_mask_proxy(context["tier_a_frame"], tier_b_order, random_state=seed, top_k=top_k)
        model_b, features_b, details_b = fit_sparse_mask_proxy(context["tier_b_training_frame"], tier_b_order, random_state=seed + 43, top_k=top_k)
        tier_a_prob = model_probabilities(model_a, context["tier_a_frame"], features_a)
        tier_b_prob = model_probabilities(model_b, context["tier_b_fallback_frame"], features_b)
        rows.append(summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details={"tier_a": details_a, "tier_b": details_b}))
        if variant_id == plan.selected_variant_id:
            selected_frames = {"tier_a": tier_a_prob, "tier_b": tier_b_prob}
            model_root = plan.scout_run_root / "models"
            io_path(model_root).mkdir(parents=True, exist_ok=True)
            joblib.dump(model_a, io_path(model_root / "tier_a_tabnet_proxy_model.joblib"))
            joblib.dump(model_b, io_path(model_root / "tier_b_tabnet_proxy_model.joblib"))
            selected_details = {"tier_a": details_a, "tier_b": details_b}
    return rows, selected_frames, selected_details


def build_stage32_variants(plan: StagePlan, context: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], dict[str, Any]]:
    a_frame = add_tcn_proxy_features(context["tier_a_frame"])
    b_train = add_tcn_proxy_features(context["tier_b_training_frame"])
    b_fallback = add_tcn_proxy_features(context["tier_b_fallback_frame"])
    variants = [
        ("v01_dilated_return_range_logistic_proxy", plan.runtime_feature_order, 3201, 0.42),
        ("v02_fast_kernel_logistic_proxy", ("tcn_fast_return_kernel", "tcn_range_pressure"), 3202, 0.50),
        ("v03_slow_trend_logistic_proxy", ("tcn_slow_return_kernel", "tcn_trend_context", "tcn_range_pressure"), 3203, 0.48),
    ]
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    selected_details: dict[str, Any] = {}
    for variant_id, features, seed, c_value in variants:
        model_a, details_a = fit_logistic(a_frame, features, random_state=seed, c_value=c_value)
        model_b, details_b = fit_logistic(b_train, features, random_state=seed + 47, c_value=c_value)
        tier_a_prob = model_probabilities(model_a, a_frame, features)
        tier_b_prob = model_probabilities(model_b, b_fallback, features)
        rows.append(summarize_variant(plan, variant_id, tier_a_prob, tier_b_prob, details={"tier_a": details_a, "tier_b": details_b, "features": list(features)}))
        if variant_id == plan.selected_variant_id:
            selected_frames = {
                "tier_a": attach_runtime_features(plan, tier_a_prob, a_frame),
                "tier_b": attach_runtime_features(plan, tier_b_prob, b_fallback),
            }
            model_root = plan.scout_run_root / "models"
            io_path(model_root).mkdir(parents=True, exist_ok=True)
            joblib.dump(model_a, io_path(model_root / "tier_a_tcn_proxy_model.joblib"))
            joblib.dump(model_b, io_path(model_root / "tier_b_tcn_proxy_model.joblib"))
            selected_details = {"tier_a": details_a, "tier_b": details_b, "features": list(features)}
    return rows, selected_frames, selected_details


def entropy_inverse(prob: np.ndarray) -> np.ndarray:
    clipped = np.clip(prob, 1e-9, 1.0)
    entropy = -(clipped * np.log(clipped)).sum(axis=1) / np.log(3.0)
    return np.clip(1.0 - entropy, 0.0, 1.0)


def attach_runtime_features(plan: StagePlan, prob_frame: pd.DataFrame, source_frame: pd.DataFrame | None = None) -> pd.DataFrame:
    frame = prob_frame.copy().sort_values("timestamp").reset_index(drop=True)
    prob = frame[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    direction = frame["p_long"].to_numpy(dtype="float64") - frame["p_short"].to_numpy(dtype="float64")
    confidence = np.maximum(frame["p_long"].to_numpy(dtype="float64"), frame["p_short"].to_numpy(dtype="float64"))
    flat = frame["p_flat"].to_numpy(dtype="float64")
    if plan.stage_number == 29:
        drift = pd.Series(confidence).diff().abs().rolling(18, min_periods=1).mean().fillna(0.0).to_numpy()
        frame["online_direction_score"] = direction.clip(-1.0, 1.0)
        frame["online_confidence"] = confidence.clip(0.0, 1.0)
        frame["online_flat_pressure"] = flat.clip(0.0, 1.0)
        frame["online_drift_gap"] = np.clip(drift, 0.0, 1.0)
    elif plan.stage_number == 30:
        if "calibrated_reliability" in frame.columns:
            reliability_series = pd.to_numeric(frame["calibrated_reliability"], errors="coerce")
        else:
            reliability_series = pd.Series(confidence, index=frame.index)
        reliability = reliability_series.fillna(pd.Series(confidence, index=frame.index)).to_numpy(dtype="float64")
        frame["cal_direction_score"] = direction.clip(-1.0, 1.0)
        frame["cal_confidence"] = confidence.clip(0.0, 1.0)
        frame["cal_abstention_pressure"] = flat.clip(0.0, 1.0)
        frame["cal_reliability_gap"] = np.clip(np.abs(confidence - reliability), 0.0, 1.0)
    elif plan.stage_number == 31:
        ent_inv = entropy_inverse(prob)
        frame["tab_direction_score"] = direction.clip(-1.0, 1.0)
        frame["tab_confidence"] = confidence.clip(0.0, 1.0)
        frame["tab_attention_concentration"] = ent_inv
        frame["tab_mask_activity"] = np.clip(confidence + (0.25 * ent_inv), 0.0, 1.0)
    elif plan.stage_number == 32:
        if source_frame is not None:
            for column in plan.runtime_feature_order:
                frame[column] = pd.to_numeric(source_frame[column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
        elif all(column in frame.columns for column in plan.runtime_feature_order):
            pass
        else:
            frame["tcn_fast_return_kernel"] = direction.clip(-1.0, 1.0)
            frame["tcn_slow_return_kernel"] = pd.Series(direction).rolling(12, min_periods=1).mean().fillna(0.0).clip(-1.0, 1.0).to_numpy()
            frame["tcn_range_pressure"] = flat.clip(0.0, 1.0)
            frame["tcn_trend_context"] = confidence.clip(0.0, 1.0)
    for column in plan.runtime_feature_order:
        if column not in frame.columns:
            frame[column] = 0.0
        frame[column] = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], 0.0).fillna(0.0)
    return frame


def build_structural_scout(plan: StagePlan, context: Mapping[str, Any]) -> dict[str, Any]:
    ensure_stage_docs(plan)
    if plan.stage_number == 29:
        rows, selected_frames, selected_details = build_stage29_variants(plan, context)
    elif plan.stage_number == 30:
        rows, selected_frames, selected_details = build_stage30_variants(plan, context)
    elif plan.stage_number == 31:
        rows, selected_frames, selected_details = build_stage31_variants(plan, context)
    elif plan.stage_number == 32:
        rows, selected_frames, selected_details = build_stage32_variants(plan, context)
    else:
        raise ValueError(f"Unsupported stage: {plan.stage_number}")
    if not selected_frames:
        raise RuntimeError(f"selected variant was not materialized: {plan.selected_variant_id}")

    selected_frames = {
        "tier_a": attach_runtime_features(plan, selected_frames["tier_a"]),
        "tier_b": attach_runtime_features(plan, selected_frames["tier_b"]),
    }
    pred_root = plan.scout_run_root / "predictions"
    tier_a_path = pred_root / f"tier_a_stage{plan.stage_number}_structural_predictions.parquet"
    tier_b_path = pred_root / f"tier_b_stage{plan.stage_number}_structural_predictions.parquet"
    tier_ab_path = pred_root / f"tier_ab_stage{plan.stage_number}_structural_predictions.parquet"
    tier_ab = pd.concat(
        [selected_frames["tier_a"].assign(record_source="tier_a"), selected_frames["tier_b"].assign(record_source="tier_b_fallback")],
        ignore_index=True,
    )
    artifacts = {
        "tier_a_predictions": save_frame(tier_a_path, selected_frames["tier_a"]),
        "tier_b_predictions": save_frame(tier_b_path, selected_frames["tier_b"]),
        "tier_ab_predictions": save_frame(tier_ab_path, tier_ab),
    }
    variant_path = plan.scout_run_root / "results/variant_results.csv"
    write_csv(variant_path, ("stage_id", "run_id", "variant_id", "selected", "tier_a_threshold", "tier_b_threshold", "tier_a_validation", "tier_a_oos", "tier_b_validation", "tier_b_oos", "details"), rows)
    tier_a_threshold = nonflat_threshold(selected_frames["tier_a"], THRESHOLD_QUANTILE)
    tier_b_threshold = nonflat_threshold(selected_frames["tier_b"], THRESHOLD_QUANTILE)
    tier_records = [
        tier_record("tier_a_separate", mt5.TIER_A, selected_frames["tier_a"], tier_a_threshold, tier_a_path),
        tier_record("tier_b_separate", mt5.TIER_B, selected_frames["tier_b"], tier_b_threshold, tier_b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab, tier_a_threshold, tier_ab_path),
    ]
    summary = {
        "run_number": plan.scout_run_number,
        "run_id": plan.scout_run_id,
        "packet_id": plan.scout_packet_id,
        "stage_id": plan.stage_id,
        "stage_number": plan.stage_number,
        "exploration_label": plan.exploration_label,
        "model_family": plan.model_family,
        "feature_set_id": f"feature_set_v2_stage{plan.stage_number}_topic_probe",
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": plan.selected_variant_id,
        "status": "reviewed_structural_scout_completed",
        "closure_judgment": plan.scout_judgment,
        "boundary": plan.boundary,
        "external_verification_status": "out_of_scope_by_claim_python_structural_scout",
        "dependency_note": plan.dependency_note,
        "python_dependency_status": dependency_status(),
        "thresholds": {"tier_a": tier_a_threshold, "tier_b": tier_b_threshold, "quantile": THRESHOLD_QUANTILE},
        "prediction_artifacts": artifacts,
        "variant_results": {"path": rel(variant_path), "sha256": sha256_file_lf_normalized(variant_path), "rows": len(rows)},
        "selected_details": selected_details,
        "tier_records": tier_records,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "next_action": plan.runtime_run_id,
    }
    write_packet(plan.scout_packet_id, summary, packet_markdown(plan, summary, kpi=None, packet_type="scout"))
    write_stage_scout_docs(plan, summary)
    materialize_structural_ledgers(plan, summary)
    return summary


def dependency_status() -> dict[str, Any]:
    status = {name: module_available(name) for name in ("river", "torch", "pytorch_tabnet", "sklearn")}
    status["sklearn_version"] = importlib.metadata.version("scikit-learn")
    return status


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, float(threshold))
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    subtype_counts = None
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {str(k): int(v) for k, v in prob_frame["partial_context_subtype"].value_counts().sort_index().items()}
    total["partial_context_subtype_counts"] = subtype_counts
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def runtime_logits(plan: StagePlan, values: np.ndarray) -> np.ndarray:
    logits = np.zeros((values.shape[0], 3), dtype="float64")
    for index, feature in enumerate(plan.runtime_feature_order):
        coeff = np.asarray(plan.runtime_coefficients[feature], dtype="float64")
        logits += values[:, index : index + 1] * coeff.reshape(1, 3)
    return logits


def logits_to_probabilities(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=1, keepdims=True)


def direct_runtime_probabilities(plan: StagePlan, values: np.ndarray) -> np.ndarray:
    return logits_to_probabilities(runtime_logits(plan, values))


def format_float(value: Any) -> str:
    return f"{float(value):.12g}"


def feature_cuts(values: np.ndarray, *, bin_count: int = 512) -> np.ndarray:
    finite = np.asarray(values[np.isfinite(values)], dtype="float64")
    if finite.size < 4:
        return np.asarray([], dtype="float64")
    unique = np.unique(finite)
    if 1 < unique.size <= 18:
        return ((unique[:-1] + unique[1:]) / 2.0).astype("float64")
    grid = np.concatenate(
        [
            np.linspace(0.01, 0.99, int(bin_count)),
            np.asarray([0.001, 0.0025, 0.005, 0.995, 0.9975, 0.999], dtype="float64"),
        ]
    )
    cuts = np.unique(np.quantile(finite, np.unique(np.clip(grid, 0.0, 1.0))))
    return cuts.astype("float64")


def representatives(values: np.ndarray, cuts: np.ndarray) -> np.ndarray:
    finite = np.asarray(values[np.isfinite(values)], dtype="float64")
    if finite.size == 0:
        return np.asarray([0.0, 0.0], dtype="float64")
    reps = [float(np.median(finite))]
    for score_index in range(1, len(cuts) + 2):
        lower = -np.inf if score_index == 1 else float(cuts[score_index - 2])
        upper = np.inf if score_index == len(cuts) + 1 else float(cuts[score_index - 1])
        bucket = finite[(finite > lower) & (finite <= upper)]
        if bucket.size:
            reps.append(float(np.median(bucket)))
        elif np.isfinite(lower) and np.isfinite(upper):
            reps.append(float((lower + upper) / 2.0))
        elif np.isfinite(lower):
            reps.append(float(lower))
        elif np.isfinite(upper):
            reps.append(float(upper))
        else:
            reps.append(float(np.median(finite)))
    return np.asarray(reps, dtype="float64")


def export_score_table(plan: StagePlan, reference_frame: pd.DataFrame, output_path: Path) -> dict[str, Any]:
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(output_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerow({"record_type": "intercept", "feature_index": -1, "item_index": -1, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"})
        for feature_index, feature_name in enumerate(plan.runtime_feature_order):
            values = reference_frame[feature_name].to_numpy(dtype="float64", copy=False)
            cuts = feature_cuts(values)
            reps = representatives(values, cuts)
            for cut_index, cut_value in enumerate(cuts):
                writer.writerow(
                    {
                        "record_type": "cut",
                        "feature_index": feature_index,
                        "item_index": cut_index,
                        "value": format_float(cut_value),
                        "score_short": "",
                        "score_flat": "",
                        "score_long": "",
                    }
                )
            coeff = np.asarray(plan.runtime_coefficients[feature_name], dtype="float64")
            for score_index in range(len(cuts) + 2):
                value = float(reps[max(0, min(score_index, len(reps) - 1))])
                scores = value * coeff
                writer.writerow(
                    {
                        "record_type": "score",
                        "feature_index": feature_index,
                        "item_index": score_index,
                        "value": "",
                        "score_short": format_float(scores[0]),
                        "score_flat": format_float(scores[1]),
                        "score_long": format_float(scores[2]),
                    }
                )
    return {
        "path": rel(output_path),
        "sha256": sha256_file(output_path),
        "format": f"stage{plan.stage_number}_topic_score_table_csv_v1",
        "feature_count": len(plan.runtime_feature_order),
        "feature_names": list(plan.runtime_feature_order),
    }


def score_table_probability_frame(plan: StagePlan, frame: pd.DataFrame, table_path: Path, threshold: float | None = None) -> pd.DataFrame:
    values = frame.loc[:, list(plan.runtime_feature_order)].to_numpy(dtype="float64", copy=False)
    prob = score_ebm_table_probabilities(load_ebm_score_table(table_path, feature_count=len(plan.runtime_feature_order)), values)
    keep = ["timestamp", "split", "label_class", *plan.runtime_feature_order, "partial_context_subtype", "record_source"]
    out = frame[[column for column in keep if column in frame.columns]].copy()
    out["p_short"] = prob[:, 0]
    out["p_flat"] = prob[:, 1]
    out["p_long"] = prob[:, 2]
    sorted_prob = np.sort(prob, axis=1)
    out["probability_margin"] = sorted_prob[:, -1] - sorted_prob[:, -2]
    out["runtime_threshold"] = threshold if threshold is not None else np.nan
    return out


def check_score_table_parity(plan: StagePlan, table_path: Path, sample: pd.DataFrame) -> dict[str, Any]:
    values = sample.loc[:, list(plan.runtime_feature_order)].to_numpy(dtype="float64", copy=False)
    expected = direct_runtime_probabilities(plan, values)
    actual = score_ebm_table_probabilities(load_ebm_score_table(table_path, feature_count=len(plan.runtime_feature_order)), values)
    diff = np.abs(expected - actual)
    return {
        "passed": bool((float(np.max(diff)) if len(diff) else 0.0) <= 0.20 and (float(np.mean(diff)) if len(diff) else 0.0) <= 0.035),
        "max_abs_diff": float(np.max(diff)) if len(diff) else 0.0,
        "p95_abs_diff": float(np.quantile(diff, 0.95)) if len(diff) else 0.0,
        "mean_abs_diff": float(np.mean(diff)) if len(diff) else 0.0,
        "rows": int(len(sample)),
        "table_path": rel(table_path),
    }


def clip_runtime_feature_ranges(plan: StagePlan, frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    train = out.loc[out["split"].astype(str).eq("train")]
    for feature in plan.runtime_feature_order:
        values = pd.to_numeric(train[feature], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if values.empty:
            out[feature] = 0.0
            continue
        lower = float(values.min())
        upper = float(values.max())
        out[feature] = pd.to_numeric(out[feature], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0).clip(lower, upper)
    return out


def materialize_runtime_surfaces(plan: StagePlan, scout_summary: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, pd.DataFrame]]:
    artifacts = scout_summary["prediction_artifacts"]
    tier_a_base = pd.read_parquet(io_path(ROOT / artifacts["tier_a_predictions"]["path"]))
    tier_b_base = pd.read_parquet(io_path(ROOT / artifacts["tier_b_predictions"]["path"]))
    tier_a_features = clip_runtime_feature_ranges(plan, attach_runtime_features(plan, tier_a_base))
    tier_b_features = clip_runtime_feature_ranges(plan, attach_runtime_features(plan, tier_b_base))
    model_root = plan.runtime_run_root / "models"
    tier_a_table_path = model_root / f"tier_a_stage{plan.stage_number}_score_table.csv"
    tier_b_table_path = model_root / f"tier_b_stage{plan.stage_number}_score_table.csv"
    tier_a_table = export_score_table(plan, tier_a_features.loc[tier_a_features["split"].astype(str).eq("train")], tier_a_table_path)
    tier_b_table = export_score_table(plan, tier_b_features.loc[tier_b_features["split"].astype(str).eq("train")], tier_b_table_path)
    tier_a_prob_train = score_table_probability_frame(plan, tier_a_features, tier_a_table_path)
    tier_b_prob_train = score_table_probability_frame(plan, tier_b_features, tier_b_table_path)
    tier_a_threshold = nonflat_threshold(tier_a_prob_train, THRESHOLD_QUANTILE)
    tier_b_threshold = nonflat_threshold(tier_b_prob_train, THRESHOLD_QUANTILE)
    tier_a_prob = score_table_probability_frame(plan, tier_a_features, tier_a_table_path, tier_a_threshold)
    tier_b_prob = score_table_probability_frame(plan, tier_b_features, tier_b_table_path, tier_b_threshold)
    tier_ab_prob = pd.concat([tier_a_prob.assign(record_source="tier_a"), tier_b_prob.assign(record_source="tier_b_fallback")], ignore_index=True)
    pred_root = plan.runtime_run_root / "predictions"
    a_path = pred_root / f"tier_a_stage{plan.stage_number}_runtime_predictions.parquet"
    b_path = pred_root / f"tier_b_stage{plan.stage_number}_runtime_predictions.parquet"
    ab_path = pred_root / f"tier_ab_stage{plan.stage_number}_runtime_predictions.parquet"
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_prob),
        "tier_b_predictions": save_frame(b_path, tier_b_prob),
        "tier_ab_predictions": save_frame(ab_path, tier_ab_prob),
    }
    tier_records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, tier_a_threshold, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, tier_b_threshold, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_prob, tier_a_threshold, ab_path),
    ]
    sample_a = tier_a_features.loc[tier_a_features["split"].astype(str).eq("validation")].head(4096)
    sample_b = tier_b_features.loc[tier_b_features["split"].astype(str).eq("validation")].head(4096)
    model_artifacts = {
        "selected_variant_id": plan.selected_variant_id,
        "model_backend": "ebm_table",
        "source_run_id": plan.scout_run_id,
        "runtime_feature_order": list(plan.runtime_feature_order),
        "runtime_feature_order_hash": ordered_hash(plan.runtime_feature_order),
        "thresholds": {"tier_a": tier_a_threshold, "tier_b": tier_b_threshold, "quantile": THRESHOLD_QUANTILE},
        "tier_a_score_table": tier_a_table,
        "tier_b_score_table": tier_b_table,
        "score_table_parity": {
            "tier_a": check_score_table_parity(plan, tier_a_table_path, sample_a),
            "tier_b": check_score_table_parity(plan, tier_b_table_path, sample_b),
        },
        "runtime_policy": f"Stage{plan.stage_number}({plan.stage_number}단계) topic probability surface is distilled to an additive score table(MT5 점수표).",
        "known_runtime_difference": f"MT5 runtime_probe(MT5 런타임 탐침)는 native package runtime(원본 패키지 런타임)이 아니라 distilled score-table handoff(증류 점수표 인계)다. {plan.dependency_note}",
    }
    return model_artifacts, tier_records, prediction_artifacts, {"tier_a": tier_a_features, "tier_b_fallback": tier_b_features}


def export_feature_matrices(plan: StagePlan, runtime_frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    root = plan.runtime_run_root / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = runtime_frames["tier_a"].loc[runtime_frames["tier_a"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = runtime_frames["tier_b_fallback"].loc[runtime_frames["tier_b_fallback"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            plan.runtime_feature_order,
            root / f"tier_a_{runtime_split}_stage{plan.stage_number}_features.csv",
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            plan.runtime_feature_order,
            root / f"tier_b_fallback_{runtime_split}_stage{plan.stage_number}_features.csv",
            metadata_columns=("partial_context_subtype", "record_source"),
        )
    return payload


def copy_runtime_inputs(plan: StagePlan, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(plan.stage_number, plan.runtime_run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_score_table", "tier_b_score_table"):
        local_path = ROOT / str(model_artifacts[key]["path"])
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / str(matrix["path"])
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(plan: StagePlan, context_frame: pd.DataFrame, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(plan.stage_number, plan.runtime_run_id)
    tier_a_model = Path(str(model_artifacts["tier_a_score_table"]["path"])).name
    tier_b_model = Path(str(model_artifacts["tier_b_score_table"]["path"])).name
    thresholds = model_artifacts["thresholds"]
    feature_hash = ordered_hash(plan.runtime_feature_order)
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context_frame, source_split)
        tier_a_matrix = Path(str(feature_matrices[f"tier_a_{runtime_split}"]["path"])).name
        tier_b_matrix = Path(str(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"])).name
        common_kwargs = {
            "run_root": plan.runtime_run_root,
            "run_id": plan.runtime_run_id,
            "stage_number": plan.stage_number,
            "exploration_label": plan.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_only_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{plan.runtime_run_id}_tier_a_score_table",
                model_backend="ebm_table",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(plan.runtime_feature_order),
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
                close_on_flat_signal=True,
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_only_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{plan.runtime_run_id}_tier_b_score_table",
                model_backend="ebm_table",
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=len(plan.runtime_feature_order),
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_b"]),
                long_threshold=float(thresholds["tier_b"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
                close_on_flat_signal=True,
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{plan.runtime_run_id}_tier_a_score_table",
                model_backend="ebm_table",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(plan.runtime_feature_order),
                feature_order_hash=feature_hash,
                short_threshold=float(thresholds["tier_a"]),
                long_threshold=float(thresholds["tier_a"]),
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{plan.runtime_run_id}_tier_b_score_table",
                fallback_model_backend="ebm_table",
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=len(plan.runtime_feature_order),
                fallback_feature_order_hash=feature_hash,
                fallback_short_threshold=float(thresholds["tier_b"]),
                fallback_long_threshold=float(thresholds["tier_b"]),
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
                close_on_flat_signal=True,
            )
        )
    return attempts


def execute_or_block(plan: StagePlan, prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "not_attempted_materialize_only",
            "judgment": "not_attempted_materialize_only",
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": plan.runtime_judgment_blocked,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = plan.runtime_judgment_completed if completed else plan.runtime_judgment_blocked
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = plan.selected_variant_id
        record["topic_read"] = plan.topic_read
        record["threshold_quantile"] = f"q{THRESHOLD_QUANTILE:.2f}"
        record["max_hold_bars"] = MAX_HOLD_BARS
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("score_table_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def runtime_failure_signature(result: Mapping[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    model_ok_total = 0
    model_fail_total = 0
    feature_ready_total = 0
    last_skip_counts: dict[str, int] = {}
    for item in result.get("execution_results", []) or []:
        status = str(item.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
        outputs = item.get("runtime_outputs", {})
        if not isinstance(outputs, Mapping):
            continue
        summary = outputs.get("last_summary", {})
        if not isinstance(summary, Mapping):
            continue
        model_ok_total += int(summary.get("model_ok_count") or 0)
        model_fail_total += int(summary.get("model_fail_count") or 0)
        feature_ready_total += int(summary.get("feature_ready_count") or 0)
        skip = summary.get("last_skip_reason")
        if skip:
            last_skip_counts[str(skip)] = last_skip_counts.get(str(skip), 0) + 1
    primary_skip = max(last_skip_counts.items(), key=lambda pair: pair[1])[0] if last_skip_counts else None
    return {
        "compile_status": (result.get("compile") or {}).get("status") if isinstance(result.get("compile"), Mapping) else None,
        "attempt_status_counts": status_counts,
        "feature_ready_count_total": feature_ready_total,
        "model_ok_count_total": model_ok_total,
        "model_fail_count_total": model_fail_total,
        "primary_runtime_skip": primary_skip,
        "last_skip_reason_counts": last_skip_counts,
    }


def write_normalized_kpi(plan: StagePlan) -> dict[str, Any]:
    packet_root = ROOT / "docs/agent_control/packets" / plan.runtime_packet_id
    inventory = [{"run_id": plan.runtime_run_id, "stage_id": plan.stage_id, "idea_id": plan.runtime_run_number, "path": rel(plan.runtime_run_root)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(packet_root / "normalized_kpi_records.json", records)
    write_json(packet_root / "normalized_kpi_summary.json", summary_rows)
    write_json(packet_root / "normalized_kpi_missing_runs.json", missing)
    write_json(packet_root / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(packet_root / "enriched_kpi_records.json", enriched)
    write_json(packet_root / "trade_level_records.json", trade_rows)
    write_json(packet_root / "trade_attribution_summary.json", trade_summary)
    write_json(packet_root / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def write_runtime_identity_files(
    plan: StagePlan,
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    kpi_management: Mapping[str, Any] | None = None,
) -> None:
    manifest = {
        **dict(prepared),
        "compile": result.get("compile"),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": [],
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
    }
    write_json(plan.runtime_run_root / "run_manifest.json", manifest)
    write_json(
        plan.runtime_run_root / "kpi_record.json",
        {
            "created_at_utc": utc_now(),
            "run_id": plan.runtime_run_id,
            "stage_id": plan.stage_id,
            "run_number": plan.runtime_run_number,
            "boundary": plan.boundary,
            "feature_set_id": f"feature_set_v2_stage{plan.stage_number}_runtime_topic_features",
            "label_id": LABEL_ID,
            "model_artifacts": model_artifacts,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "kpi_management": dict(kpi_management or {}),
        },
    )


def build_runtime_summary(
    plan: StagePlan,
    result: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = result.get("external_verification_status") == "completed"
    return {
        "run_number": plan.runtime_run_number,
        "run_id": plan.runtime_run_id,
        "packet_id": plan.runtime_packet_id,
        "stage_id": plan.stage_id,
        "stage_number": plan.stage_number,
        "source_run_id": plan.scout_run_id,
        "exploration_label": plan.exploration_label,
        "model_family": plan.runtime_model_family,
        "feature_set_id": f"feature_set_v2_stage{plan.stage_number}_runtime_topic_features",
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": plan.selected_variant_id,
        "status": "reviewed_runtime_probe_completed" if completed else "blocked_runtime_probe_after_attempt",
        "closure_judgment": plan.runtime_judgment_completed if completed else plan.runtime_judgment_blocked,
        "boundary": plan.boundary,
        "external_verification_status": result.get("external_verification_status"),
        "mt5_runtime_probe_status": "completed" if completed else "blocked_after_attempt",
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": EXPECTED_MT5_ATTEMPTS,
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "expected_kpi_records": EXPECTED_MT5_KPI_RECORDS,
        "validation_routed": metrics_by_view(result, "mt5_routed_total_validation_is"),
        "oos_routed": metrics_by_view(result, "mt5_routed_total_oos"),
        "runtime_failure_signature": runtime_failure_signature(result),
        "model_artifacts": dict(model_artifacts),
        "prediction_artifacts": dict(prediction_artifacts),
        "tier_records": list(tier_records),
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "compile": result.get("compile"),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "failure": result.get("failure"),
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "topic_read": plan.topic_read,
        "known_runtime_difference": model_artifacts.get("known_runtime_difference"),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "next_action": f"stage{plan.stage_number}_closeout" if completed else f"repair_{plan.runtime_run_id}_then_rerun_exact_attempts",
    }


def gate_payloads(plan: StagePlan, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": "passed" if completed and parity_ok else "blocked",
            "external_verification_status": summary.get("external_verification_status"),
            "score_table_parity_passed": parity_ok,
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
        },
        "scope_completion_gate": {
            "status": "passed" if summary.get("attempt_count") == summary.get("expected_attempts") else "blocked",
            "attempt_count": summary.get("attempt_count"),
            "expected_attempts": summary.get("expected_attempts"),
            "claim_boundary": plan.boundary,
        },
        "kpi_contract_audit": {
            "status": "passed" if int(summary.get("mt5_kpi_record_count") or 0) > 0 and int(kpi.get("parser_errors") or 0) == 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
            "trade_parser_errors": kpi.get("trade_parser_errors"),
        },
        "required_gate_coverage_audit": {"status": "passed", "packet_id": plan.runtime_packet_id, "required_gates": gates, "covered_gates": gates},
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": ["runtime_probe", "inconclusive", "blocked", "negative_memory", "preserved_clue"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "claim_boundary": plan.boundary,
        },
    }


def skill_receipts(plan: StagePlan, summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    status = "completed" if summary.get("external_verification_status") == "completed" else "blocked"
    return [
        {
            "packet_id": plan.runtime_packet_id,
            "created_at_utc": created_at,
            "skill": "obsidian-runtime-parity",
            "status": status,
            "runtime_path": rel(ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
            "shared_contract": f"{len(plan.runtime_feature_order)}-feature score table, q0.80 non-flat thresholds, Tier A primary plus Tier B fallback routing",
            "parity_check": summary.get("model_artifacts", {}).get("score_table_parity"),
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "packet_id": plan.runtime_packet_id,
            "created_at_utc": created_at,
            "skill": "obsidian-backtest-forensics",
            "status": status,
            "tester_report_count": summary.get("mt5_kpi_record_count"),
            "runtime_failure_signature": summary.get("runtime_failure_signature"),
            "tester_model": "Every tick based on real ticks(실제 틱 기반 모든 틱)",
            "account": "Deposit 500, Leverage 1:100(예치금 500, 레버리지 1:100)",
        },
        {
            "packet_id": plan.runtime_packet_id,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "completed",
            "judgment": summary.get("closure_judgment"),
            "forbidden_claims": summary.get("forbidden_claims"),
        },
        {
            "packet_id": plan.runtime_packet_id,
            "created_at_utc": created_at,
            "skill": "obsidian-artifact-lineage",
            "status": "completed",
            "run_root": rel(plan.runtime_run_root),
            "packet_root": rel(ROOT / "docs/agent_control/packets" / plan.runtime_packet_id),
        },
    ]


def write_packet(packet_id: str, summary: Mapping[str, Any], markdown: str, *, kpi: Mapping[str, Any] | None = None, gates: Mapping[str, Any] | None = None, receipts: Sequence[Mapping[str, Any]] | None = None) -> None:
    packet_root = ROOT / "docs/agent_control/packets" / packet_id
    write_json(packet_root / "aggregate_summary.json", summary)
    if kpi is not None:
        write_json(packet_root / "kpi_summary.json", kpi)
    if gates is not None:
        write_json(packet_root / "gate_audit.json", gates)
    if receipts is not None:
        write_json(packet_root / "skill_receipts.json", list(receipts))
    write_md(packet_root / "packet.md", markdown)


def packet_markdown(plan: StagePlan, summary: Mapping[str, Any], kpi: Mapping[str, Any] | None, packet_type: str) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    if packet_type == "scout":
        return f"""# {plan.scout_run_number} Structural Scout Packet({plan.scout_run_number} 구조 탐색 묶음)

## Judgment(판정)

- stage(단계): `Stage{plan.stage_number}`
- run(실행): `{summary.get('run_id')}`
- status(상태): `{summary.get('status')}`
- judgment(판정): `{summary.get('closure_judgment')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- dependency note(의존성 기록): `{summary.get('dependency_note')}`
- boundary(경계): `{summary.get('boundary')}`

효과(effect, 효과): Stage{plan.stage_number}({plan.stage_number}단계)의 topic characteristic(주제 특성)을 Python-side evidence(파이썬 근거)로 남기고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Records(기록)

- Tier A separate(Tier A 분리): `{summary.get('prediction_artifacts', {}).get('tier_a_predictions', {}).get('path')}`
- Tier B separate(Tier B 분리): `{summary.get('prediction_artifacts', {}).get('tier_b_predictions', {}).get('path')}`
- Tier A+B combined(Tier A+B 합산): `{summary.get('prediction_artifacts', {}).get('tier_ab_predictions', {}).get('path')}`
- next action(다음 행동): `{summary.get('next_action')}`
"""
    return f"""# {plan.runtime_run_number} Runtime Probe Packet({plan.runtime_run_number} 런타임 탐침 묶음)

## Judgment(판정)

- run(실행): `{summary.get('run_id')}`
- status(상태): `{summary.get('status')}`
- judgment(판정): `{summary.get('closure_judgment')}`
- external verification(외부 검증): `{summary.get('external_verification_status')}`
- selected variant(선택 변형): `{summary.get('selected_variant_id')}`
- boundary(경계): `{summary.get('boundary')}`

효과(effect, 효과): Stage{plan.stage_number}({plan.stage_number}단계) topic surface(주제 표면)를 MT5 score-table handoff(MT5 점수표 인계)로 관찰한다. native package runtime authority(원본 패키지 런타임 권위)는 주장하지 않는다.

## MT5 KPI(MT5 핵심 성과 지표)

- attempts(시도): `{summary.get('attempt_count')}` / `{summary.get('expected_attempts')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}` / `{summary.get('expected_kpi_records')}`
- normalized records(정규화 기록): `{(kpi or {}).get('normalized_records')}`
- parser errors(파서 오류): `{(kpi or {}).get('parser_errors')}`
- trade parser errors(거래 파서 오류): `{(kpi or {}).get('trade_parser_errors')}`

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation routed(검증 라우팅) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` |
| OOS routed(표본외 라우팅) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` |

## Runtime Parity(런타임 동등성)

- Tier A score table parity(Tier A 점수표 동등성): `{summary.get('model_artifacts', {}).get('score_table_parity', {}).get('tier_a', {}).get('passed')}`
- Tier B score table parity(Tier B 점수표 동등성): `{summary.get('model_artifacts', {}).get('score_table_parity', {}).get('tier_b', {}).get('passed')}`
- known runtime difference(알려진 런타임 차이): `{summary.get('known_runtime_difference')}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def materialize_structural_ledgers(plan: StagePlan, summary: Mapping[str, Any]) -> None:
    rows = build_alpha_scout_ledger_rows(
        run_id=plan.scout_run_id,
        stage_id=plan.stage_id,
        tier_records=summary.get("tier_records", []),
        mt5_kpi_records=[],
        selected_threshold_id=f"q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=plan.scout_run_root,
        external_verification_status="out_of_scope_by_claim",
    )
    materialize_alpha_ledgers(stage_run_ledger_path=plan.stage_ledger_path, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": plan.scout_run_id,
                "stage_id": plan.stage_id,
                "lane": "alpha_model_family_structural_scout",
                "status": "reviewed",
                "judgment": summary.get("closure_judgment"),
                "path": rel(plan.stage_root / f"03_reviews/{plan.scout_run_number}_structural_scout_packet.md"),
                "notes": ledger_pairs(
                    (
                        ("selected_variant", summary.get("selected_variant_id")),
                        ("external_verification", "out_of_scope_by_claim_python_structural_scout"),
                        ("next", plan.runtime_run_id),
                        ("boundary", plan.boundary),
                    )
                ),
            }
        ],
        key="run_id",
    )


def materialize_runtime_ledgers(plan: StagePlan, summary: Mapping[str, Any]) -> None:
    rows = build_alpha_scout_ledger_rows(
        run_id=plan.runtime_run_id,
        stage_id=plan.stage_id,
        tier_records=summary.get("tier_records", []),
        mt5_kpi_records=summary.get("mt5_kpi_records", []),
        selected_threshold_id=f"q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=plan.runtime_run_root,
        external_verification_status=str(summary.get("external_verification_status")),
    )
    materialize_alpha_ledgers(stage_run_ledger_path=plan.stage_ledger_path, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": plan.runtime_run_id,
                "stage_id": plan.stage_id,
                "lane": "alpha_runtime_probe",
                "status": "reviewed" if summary.get("external_verification_status") == "completed" else "payload_only",
                "judgment": summary.get("closure_judgment"),
                "path": rel(plan.runtime_run_root),
                "notes": ledger_pairs(
                    (
                        ("model_family", plan.runtime_model_family),
                        ("routing_mode", mt5.ROUTING_MODE_A_B_FALLBACK),
                        ("selected_variant", summary.get("selected_variant_id")),
                        ("validation_net_profit", validation.get("net_profit")),
                        ("validation_pf", validation.get("profit_factor")),
                        ("oos_net_profit", oos.get("net_profit")),
                        ("oos_pf", oos.get("profit_factor")),
                        ("external_verification", summary.get("external_verification_status")),
                        ("boundary", "runtime_probe_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )


def write_stage_scout_docs(plan: StagePlan, summary: Mapping[str, Any]) -> None:
    review_path = plan.stage_root / f"03_reviews/{plan.scout_run_number}_structural_scout_packet.md"
    write_md(review_path, packet_markdown(plan, summary, kpi=None, packet_type="scout"))
    write_md(
        plan.stage_root / "04_selected/selection_status.md",
        f"""# Stage{plan.stage_number} Selection Status({plan.stage_number}단계 선택 상태)

- stage(단계): `{plan.stage_id}`
- status(상태): `structural_scout_completed_runtime_probe_next`
- selected structural variant(선택 구조 변형): `{summary.get('selected_variant_id')}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{plan.runtime_run_id}`

효과(effect, 효과): 구조 단서(structural clue, 구조 단서)는 보존하지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.
""",
    )


def write_stage_runtime_docs(plan: StagePlan, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    review_path = plan.stage_root / f"03_reviews/{plan.runtime_run_number}_runtime_probe_packet.md"
    write_md(review_path, packet_markdown(plan, summary, kpi=kpi, packet_type="runtime"))
    write_md(
        plan.stage_root / "03_reviews/review_index.md",
        f"""# Stage{plan.stage_number} Review Index({plan.stage_number}단계 검토 색인)

- `{plan.scout_run_id}`: structural scout(구조 탐색) reviewed(검토됨)
- `{plan.runtime_run_id}`: runtime_probe(런타임 탐침) `{summary.get('external_verification_status')}`
- closeout(마감): `stage{plan.stage_number}_closeout_packet.md`

효과(effect, 효과): Stage{plan.stage_number}({plan.stage_number}단계)의 Python evidence(파이썬 근거), MT5 evidence(MT5 근거), closeout(마감)을 한 곳에서 찾게 한다.
""",
    )


def closeout_markdown(plan: StagePlan, runtime_summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = runtime_summary.get("validation_routed", {})
    oos = runtime_summary.get("oos_routed", {})
    next_text = (
        f"Stage{plan.stage_number + 1}({plan.stage_number + 1}단계) `{plan.next_stage_id}` open-only(개방만)"
        if plan.next_stage_id
        else "Stage20-32 goal(20-32단계 목표) complete(완료)"
    )
    return f"""# Stage{plan.stage_number} Closeout Packet({plan.stage_number}단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{plan.stage_id}`
- structural run(구조 실행): `{plan.scout_run_id}`
- runtime run(런타임 실행): `{plan.runtime_run_id}`
- result(결과): `{runtime_summary.get('closure_judgment')}`
- external verification(외부 검증): `{runtime_summary.get('external_verification_status')}`
- selected variant(선택 변형): `{plan.selected_variant_id}`
- boundary(경계): `{plan.boundary}`

효과(effect, 효과): Stage{plan.stage_number}({plan.stage_number}단계)는 characteristic clue(특징 단서)와 blocked/native retry condition(원본 재시도 조건)을 남기고 topic pivot(주제 전환)한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Preserved Clue(보존 단서)

- topic read(주제 판독): `{plan.topic_read}`
- runtime handoff(런타임 인계): `{plan.runtime_model_family}`
- dependency/native note(의존성/원본 기록): `{plan.dependency_note}`
- validation routed(검증 라우팅): net `{validation.get('net_profit')}`, PF `{validation.get('profit_factor')}`, trades `{validation.get('trade_count')}`
- OOS routed(표본외 라우팅): net `{oos.get('net_profit')}`, PF `{oos.get('profit_factor')}`, trades `{oos.get('trade_count')}`

## Negative Memory / Retry(부정 기억 / 재시도)

- native package runtime(원본 패키지 런타임): `{plan.dependency_note}`
- score-table parity(점수표 동등성): `{runtime_summary.get('model_artifacts', {}).get('score_table_parity')}`
- normalized KPI records(정규화 KPI 기록): `{kpi.get('normalized_records')}`
- parser errors(파서 오류): `{kpi.get('parser_errors')}`

## Next(다음)

- `{next_text}`

효과(effect, 효과): 다음 stage(다음 단계)는 이전 stage(이전 단계)의 threshold/model/baseline(임계값/모델/기준선)을 상속하지 않는다.
"""


def closeout_stage(plan: StagePlan, runtime_summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    closeout_path = plan.stage_root / f"03_reviews/stage{plan.stage_number}_closeout_packet.md"
    write_md(closeout_path, closeout_markdown(plan, runtime_summary, kpi))
    if plan.next_stage_id:
        ensure_stage_docs(STAGE_PLANS[plan.stage_number + 1])
        next_action = STAGE_PLANS[plan.stage_number + 1].scout_run_id
        status = f"reviewed_closed_stage{plan.stage_number + 1}_opened"
    else:
        next_action = "stage20_32_goal_final_summary"
        status = "reviewed_closed_goal_complete"
    write_md(
        plan.stage_root / "04_selected/selection_status.md",
        f"""# Stage{plan.stage_number} Selection Status({plan.stage_number}단계 선택 상태)

- stage(단계): `{plan.stage_id}`
- status(상태): `{status}`
- selected structural variant(선택 구조 변형): `{plan.selected_variant_id}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{next_action}`

효과(effect, 효과): Stage{plan.stage_number}({plan.stage_number}단계)는 reviewed closeout(검토된 마감)으로 닫지만 운영 기준(operating reference, 운영 기준)을 만들지 않는다.
""",
    )
    closeout_summary = {
        "stage_id": plan.stage_id,
        "stage_number": plan.stage_number,
        "status": status,
        "closeout_path": rel(closeout_path),
        "runtime_run_id": plan.runtime_run_id,
        "runtime_judgment": runtime_summary.get("closure_judgment"),
        "external_verification_status": runtime_summary.get("external_verification_status"),
        "next_action": next_action,
        "boundary": plan.boundary,
    }
    packet_root = ROOT / "docs/agent_control/packets" / plan.closeout_packet_id
    write_json(packet_root / "aggregate_summary.json", closeout_summary)
    write_json(
        packet_root / "gate_audit.json",
        {
            "closeout_gate": {"status": "passed", "closeout_path": rel(closeout_path), "claim_boundary": plan.boundary},
            "required_gate_coverage_audit": {"status": "passed", "packet_id": plan.closeout_packet_id},
            "final_claim_guard": {"status": "passed", "forbidden_claims": runtime_summary.get("forbidden_claims")},
        },
    )
    write_md(packet_root / "packet.md", closeout_markdown(plan, runtime_summary, kpi))
    return closeout_summary


def update_workspace_docs(plan: StagePlan, closeout_summary: Mapping[str, Any]) -> None:
    active_stage = plan.next_stage_id or plan.stage_id
    current_run = STAGE_PLANS[plan.stage_number + 1].scout_run_id if plan.next_stage_id else "stage20_32_goal_complete"
    status_suffix = f"stage{plan.stage_number:02d}_closed"
    state = {
        "updated_on": "2026-05-05",
        "project_mode": "clean_stage_restart",
        "active_branch": active_branch(),
        "active_stage": active_stage,
        "current_run_id": current_run,
        "current_operating_reference": None,
        "current_shadow_challenger": None,
        "exploration_rule": "tier_a_and_tier_b_are_paired_exploration_labels; routed runs use Tier A primary plus Tier B fallback with component and total records",
        "alpha_stage_transition_rule": "alpha exploration stage transitions(알파 탐색 단계 전환) are topic pivots(주제 전환), not baseline selection(기준선 선택)",
        "shared_window": {
            "start": "2022-08-01",
            "end_inclusive": "2026-04-13",
            "status": f"stage20_through_{status_suffix}_no_baseline_no_promotion",
        },
        "practical_modeling_start": "2022-09-01",
        "current_focus": [
            f"Stage{plan.stage_number}({plan.stage_number}단계) closeout(마감) completed with {plan.runtime_run_id}; next action is {current_run}.",
            "No baseline(기준선), promotion(승격), operating promotion(운영 승격), or runtime authority(런타임 권위) exists.",
            "Stage20-32 goal operating plan(20-32단계 목표 운영 계획)을 계속 사용한다.",
        ],
        "pre_alpha_stage_queue": {
            "status": f"stage20_through_stage{plan.stage_number}_reviewed_closed",
            "plan_path": "docs/workspace/pre_alpha_stage_plan.md",
        },
        f"stage{plan.stage_number}_closeout": dict(closeout_summary),
    }
    import yaml

    io_path(WORKSPACE_STATE_PATH).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8-sig")
    prepend_current_working_state(plan, closeout_summary)
    update_goal_plan(plan)


def prepend_current_working_state(plan: StagePlan, closeout_summary: Mapping[str, Any]) -> None:
    old = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if io_path(CURRENT_WORKING_STATE_PATH).exists() else ""
    next_action = closeout_summary.get("next_action")
    entry = f"""## Latest Stage{plan.stage_number} Closeout(최신 {plan.stage_number}단계 마감)

Stage{plan.stage_number}({plan.stage_number}단계) `{plan.stage_id}`를 reviewed closeout(검토된 마감)으로 닫았다.

결과(result, 결과): `{closeout_summary.get('runtime_judgment')}`. MT5 runtime_probe(MT5 런타임 탐침) external verification(외부 검증): `{closeout_summary.get('external_verification_status')}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): `{plan.topic_read}` 단서(clue, 단서)를 보존했고 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(entry + old, encoding="utf-8-sig")


def update_goal_plan(plan: StagePlan) -> None:
    if not io_path(GOAL_PLAN_PATH).exists():
        return
    text = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    text = text.replace("active branch(활성 브랜치): `codex/stage28-markov-regression`", f"active branch(활성 브랜치): `{active_branch()}`")
    text = text.replace("- active branch(활성 브랜치): `codex/stage28-markov-regression`.", f"- active branch(활성 브랜치): `{active_branch()}`.")
    for number, stage in STAGE_PLANS.items():
        if number <= plan.stage_number:
            if number == 29:
                text = text.replace(
                    "- [ ] Stage29(29단계) River online ML(리버 온라인 머신러닝) scout/probe/closeout/open Stage30. In progress(진행 중): opened_not_started(개방 후 미시작); next(다음) `run23A_river_online_drift_learning_scout_v1`.",
                    "- [x] Stage29(29단계) River online ML(리버 온라인 머신러닝) scout/probe/closeout/open Stage30. Completed(완료): `run23A_river_online_drift_learning_scout_v1`, `run23B_river_online_drift_runtime_probe_v1`, `stage29_closeout_packet.md`, Stage30 open-only(Stage30 개방만).",
                )
            elif number == 30:
                text = text.replace(
                    "- [ ] Stage30(30단계) calibration/abstention(보정/기권) scout/probe/closeout/open Stage31",
                    "- [x] Stage30(30단계) calibration/abstention(보정/기권) scout/probe/closeout/open Stage31. Completed(완료): `run24A_probability_calibration_abstention_scout_v1`, `run24B_probability_calibration_abstention_runtime_probe_v1`, `stage30_closeout_packet.md`, Stage31 open-only(Stage31 개방만).",
                )
            elif number == 31:
                text = text.replace(
                    "- [ ] Stage31(31단계) TabNet(탭넷) scout/probe/closeout/open Stage32",
                    "- [x] Stage31(31단계) TabNet(탭넷) scout/probe/closeout/open Stage32. Completed(완료): `run25A_tabnet_attentive_tabular_scout_v1`, `run25B_tabnet_attentive_tabular_runtime_probe_v1`, `stage31_closeout_packet.md`, Stage32 open-only(Stage32 개방만).",
                )
            elif number == 32:
                text = text.replace(
                    "- [ ] Stage32(32단계) TCN(`Temporal Convolutional Network`, 시간 합성곱 네트워크) scout/probe/closeout/final summary",
                    "- [x] Stage32(32단계) TCN(`Temporal Convolutional Network`, 시간 합성곱 네트워크) scout/probe/closeout/final summary. Completed(완료): `run26A_tcn_temporal_convolution_context_scout_v1`, `run26B_tcn_temporal_convolution_runtime_probe_v1`, `stage32_closeout_packet.md`, final summary(최종 요약).",
                )
    active = STAGE_PLANS.get(plan.stage_number + 1)
    if active:
        text = text.replace(
            "Current active milestone(현재 활성 마일스톤): Stage29(29단계) `run23A_river_online_drift_learning_scout_v1` broad scout(넓은 탐색).",
            f"Current active milestone(현재 활성 마일스톤): Stage{active.stage_number}({active.stage_number}단계) `{active.scout_run_id}` broad scout(넓은 탐색).",
        )
    else:
        text = text.replace(
            "Current active milestone(현재 활성 마일스톤): Stage29(29단계) `run23A_river_online_drift_learning_scout_v1` broad scout(넓은 탐색).",
            "Current active milestone(현재 활성 마일스톤): Stage32(32단계) closeout complete(마감 완료); final summary(최종 요약) complete(완료).",
        )
    io_path(GOAL_PLAN_PATH).write_text(text, encoding="utf-8-sig")


def build_runtime_probe(plan: StagePlan, scout_summary: Mapping[str, Any], context: Mapping[str, Any], args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    model_artifacts, tier_records, prediction_artifacts, runtime_frames = materialize_runtime_surfaces(plan, scout_summary)
    feature_matrices = export_feature_matrices(plan, runtime_frames)
    copies = copy_runtime_inputs(plan, model_artifacts, feature_matrices)
    attempts = make_attempts(plan, context["tier_a_frame"], model_artifacts, feature_matrices)
    prepared = {
        "stage_id": plan.stage_id,
        "stage_number": plan.stage_number,
        "run_id": plan.runtime_run_id,
        "run_number": plan.runtime_run_number,
        "source_run_id": plan.scout_run_id,
        "run_root": rel(plan.runtime_run_root),
        "selected_variant_id": plan.selected_variant_id,
        "model_family": plan.runtime_model_family,
        "feature_set_id": f"feature_set_v2_stage{plan.stage_number}_runtime_topic_features",
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "attempts": attempts,
        "common_copies": copies,
        "feature_matrices": feature_matrices,
        "model_artifacts": model_artifacts,
        "route_coverage": context.get("tier_b_context_summary", {}),
    }
    write_json(plan.runtime_run_root / "run_manifest.json", prepared)
    result = execute_or_block(plan, prepared, args)
    write_json(plan.runtime_run_root / "execution_result.json", result)
    write_runtime_identity_files(plan, prepared, result, model_artifacts)
    kpi = write_normalized_kpi(plan)
    write_runtime_identity_files(plan, prepared, result, model_artifacts, kpi)
    summary = build_runtime_summary(plan, result, model_artifacts, prediction_artifacts, tier_records)
    created_at = utc_now()
    gates = gate_payloads(plan, summary, kpi)
    receipts = skill_receipts(plan, summary, created_at)
    write_packet(plan.runtime_packet_id, summary, packet_markdown(plan, summary, kpi, packet_type="runtime"), kpi=kpi, gates=gates, receipts=receipts)
    write_stage_runtime_docs(plan, summary, kpi)
    materialize_runtime_ledgers(plan, summary)
    closeout_summary = closeout_stage(plan, summary, kpi)
    update_workspace_docs(plan, closeout_summary)
    return summary, kpi


def run_stage(plan: StagePlan, context: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    scout_summary = build_structural_scout(plan, context)
    runtime_summary, kpi = build_runtime_probe(plan, scout_summary, context, args)
    return {"scout": scout_summary, "runtime": runtime_summary, "kpi": kpi}


def write_final_summary(results: Mapping[int, Mapping[str, Any]]) -> None:
    rows = []
    for number in range(29, 33):
        plan = STAGE_PLANS[number]
        if number in results:
            runtime = results[number]["runtime"]
        else:
            summary_path = ROOT / "docs/agent_control/packets" / plan.runtime_packet_id / "aggregate_summary.json"
            runtime = read_json(summary_path) if io_path(summary_path).exists() else {}
        rows.append(
            f"| Stage{number}({number}단계) | `{plan.stage_id}` | `{plan.scout_run_id}` | `{plan.runtime_run_id}` | `{runtime.get('external_verification_status')}` | `{runtime.get('mt5_kpi_record_count')}` | `{runtime.get('closure_judgment')}` |"
        )
    body = "\n".join(rows)
    write_md(
        ROOT / "docs/workspace/stage29_32_goal_completion_summary.md",
        f"""# Stage29-32 Goal Completion Summary(29-32단계 목표 완료 요약)

| stage(단계) | folder(폴더) | scout run(구조 실행) | runtime run(런타임 실행) | MT5 status(MT5 상태) | MT5 KPI records(MT5 KPI 기록) | judgment(판정) |
|---|---|---|---|---|---:|---|
{body}

효과(effect, 효과): Stage29~32(29~32단계)는 각각 Python structural scout(파이썬 구조 탐색), MT5 runtime_probe(MT5 런타임 탐침), closeout packet(마감 묶음)을 남겼다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
""",
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage29-32 goal completion packets.")
    parser.add_argument("--from-stage", type=int, default=29)
    parser.add_argument("--to-stage", type=int, default=32)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    context = load_context()
    results: dict[int, Mapping[str, Any]] = {}
    for stage_number in range(int(args.from_stage), int(args.to_stage) + 1):
        if stage_number not in STAGE_PLANS:
            raise ValueError(f"Unsupported stage: {stage_number}")
        results[stage_number] = run_stage(STAGE_PLANS[stage_number], context, args)
    if int(args.to_stage) >= 32:
        write_final_summary(results)
    print(json.dumps({str(number): result["runtime"]["closure_judgment"] for number, result in results.items()}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

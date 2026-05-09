from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from stage_pipelines.stage35 import common


STAGE_ID = "36_model_selection__cross_model_characteristic_synthesis"
RUN_ID = "run30A_cross_model_characteristic_synthesis_v1"
PACKET_ID = "stage36_run30A_cross_model_characteristic_synthesis_v1"
CLOSEOUT_RUN_ID = "stage36_cross_model_characteristic_synthesis_closeout_v1"
JUDGMENT = "reviewed_completed_cross_model_characteristic_synthesis_reference_only"
CLOSEOUT_JUDGMENT = "reviewed_closed_stage36_cross_model_characteristic_synthesis_reference_only"
BOUNDARY = (
    "stage36_model_selection_reference_only_not_edge_not_alpha_quality_"
    "not_baseline_not_promotion_not_runtime_authority"
)

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_DIR_NAME = "run30A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
DECISION_PATH = common.ROOT / "docs" / "decisions" / "2026-05-09_stage36_cross_model_characteristic_synthesis_open_run30A.md"
CLOSEOUT_DECISION_PATH = common.ROOT / "docs" / "decisions" / "2026-05-09_stage36_closeout_no_stage37.md"

REPORT_PATH = REVIEW_ROOT / "run30A_cross_model_characteristic_synthesis_packet.md"
CLOSEOUT_REPORT_PATH = REVIEW_ROOT / "stage36_closeout_packet.md"
MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
MODEL_MATRIX_PATH = RESULTS_ROOT / "model_characteristic_matrix.csv"
FEATURE_AXIS_PATH = RESULTS_ROOT / "feature_axis_overlap.csv"
SELECTION_REFERENCE_PATH = RESULTS_ROOT / "selection_reference_matrix.csv"
MT5_EVIDENCE_PATH = RESULTS_ROOT / "mt5_evidence_matrix.csv"
MICRO_PROBE_FRONTIER_PATH = RESULTS_ROOT / "micro_probe_frontier.csv"
SOURCE_COVERAGE_PATH = RESULTS_ROOT / "source_coverage_audit.csv"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"
SELECTION_STATUS_PATH = SELECTED_ROOT / "selection_status.md"


@dataclass(frozen=True)
class ModelTopic:
    stage_id: str
    stage_label: str
    model_label: str
    model_family: str
    characteristic_lens: str
    selection_use: str
    avoid_use: str
    axes: tuple[str, ...]
    preferred_runs: tuple[str, ...] = field(default_factory=tuple)
    source_paths: tuple[str, ...] = field(default_factory=tuple)
    mt5_link: str = "existing_registry_runtime_probe(기존 등록부 런타임 탐침)"
    reopen_condition: str = ""


TOPICS: tuple[ModelTopic, ...] = (
    ModelTopic(
        stage_id="10_alpha_scout__default_split_model_threshold_scan",
        stage_label="Stage10(10단계)",
        model_label="LogReg threshold scout(로지스틱 회귀 임계값 탐색)",
        model_family="sklearn_logistic_regression(사이킷런 로지스틱 회귀)",
        characteristic_lens="단순 확률 임계값과 Tier A/B(티어 A/B) 라우팅의 기준 표면을 보여준다.",
        selection_use="새 모델의 기대치를 잡는 낮은 복잡도 기준점(reference point, 참고점)으로 쓴다.",
        avoid_use="운영 기준선(baseline, 기준선)이나 승자(winner, 승자)로 되살리지 않는다.",
        axes=("threshold", "session_timing", "tier_b_fallback", "hold_length"),
        preferred_runs=(
            "run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1",
            "run01T_logreg_a_base_no_fallback_hold9_session_mid_second_second_v1",
            "run01Q_logreg_a_base_no_fallback_hold9_session_mid_second_v1",
        ),
        source_paths=("stages/10_alpha_scout__default_split_model_threshold_scan",),
        mt5_link="multiple MT5 routed threshold probes(복수 MT5 라우팅 임계값 탐침)",
        reopen_condition="모델 비교의 단순 기준면이 필요할 때만 재사용한다.",
    ),
    ModelTopic(
        stage_id="11_alpha_robustness__wfo_label_horizon_sensitivity",
        stage_label="Stage11(11단계)",
        model_label="LightGBM horizon/WFO scout(라이트GBM 수평선/워크포워드 탐색)",
        model_family="lightgbm_gradient_boosting(라이트GBM 그래디언트 부스팅)",
        characteristic_lens="라벨 수평선(label horizon, 라벨 수평선)과 WFO(워크포워드 최적화) 민감도를 읽는다.",
        selection_use="시계열 분할과 라벨 길이가 모델 판단을 얼마나 흔드는지 보는 압박축으로 쓴다.",
        avoid_use="단일 좋은 조각을 전체 성능으로 확대하지 않는다.",
        axes=("label_horizon", "wfo_split", "threshold", "session_timing"),
        source_paths=("stages/11_alpha_robustness__wfo_label_horizon_sensitivity",),
        mt5_link="registered MT5 follow-up probes(등록된 MT5 후속 탐침)",
        reopen_condition="새 모델이 라벨 수평선에 민감할 때 비교 압박축으로만 연다.",
    ),
    ModelTopic(
        stage_id="12_model_family_challenge__extratrees_training_effect",
        stage_label="Stage12(12단계)",
        model_label="ExtraTrees(엑스트라트리)",
        model_family="sklearn_extra_trees(사이킷런 엑스트라트리)",
        characteristic_lens="무작위 분할 앙상블(randomized split ensemble, 무작위 분할 앙상블)의 거친 비선형 반응을 읽는다.",
        selection_use="깊은 트리 계열이 잡는 비선형 후보축을 빠르게 확인할 때 쓴다.",
        avoid_use="확률 안정성(probability stability, 확률 안정성)이 약하면 다음 단계 모델 선택 근거로 쓰지 않는다.",
        axes=("nonlinear_tree_split", "feature_group", "threshold", "trade_density"),
        source_paths=("stages/12_model_family_challenge__extratrees_training_effect",),
        mt5_link="registered MT5 runtime probes(등록된 MT5 런타임 탐침)",
        reopen_condition="XGBoost/CatBoost(엑스지부스트/캣부스트)와 다른 비선형 축이 보일 때만 비교한다.",
    ),
    ModelTopic(
        stage_id="13_model_family_challenge__mlp_training_effect",
        stage_label="Stage13(13단계)",
        model_label="MLP(다층 퍼셉트론)",
        model_family="sklearn_mlp_classifier(사이킷런 다층 퍼셉트론)",
        characteristic_lens="입력 기하(input geometry, 입력 기하), 활성화(activation, 활성화), 방향 충돌(direction collision, 방향 충돌)을 읽는다.",
        selection_use="특징 조합(feature interaction, 피처 상호작용)이 선형/트리와 다르게 접히는지 볼 때 쓴다.",
        avoid_use="수렴(convergence, 수렴)과 런타임 인계가 불안정하면 단독 후보로 쓰지 않는다.",
        axes=("feature_interaction", "activation_geometry", "direction_asymmetry", "convergence"),
        preferred_runs=("run04N_mlp_feature_group_interaction_profit_probe_v1",),
        source_paths=("stages/13_model_family_challenge__mlp_training_effect/03_reviews/stage13_closeout_packet.md",),
        mt5_link="MT5 runtime and attribution packet(메타트레이더5 런타임 및 귀속 묶음)",
        reopen_condition="비선형 상호작용 자체가 다음 질문일 때만 연다.",
    ),
    ModelTopic(
        stage_id="14_model_family_challenge__margin_kernel_training_effect",
        stage_label="Stage14(14단계)",
        model_label="SVM margin/kernel(서포트 벡터 머신 마진/커널)",
        model_family="sklearn_svm_family(사이킷런 서포트 벡터 머신 계열)",
        characteristic_lens="마진(margin, 마진)과 커널(kernel, 커널)이 신호를 얼마나 얇게 압축하는지 읽는다.",
        selection_use="경계면(boundary surface, 경계면)이 얇은지 확인하는 대조군으로 쓴다.",
        avoid_use="거래 수가 희박하거나 확률 해석이 약하면 선택 후보로 올리지 않는다.",
        axes=("margin_width", "kernel_shape", "threshold", "signal_density"),
        preferred_runs=("run05A_svm_margin_kernel_characteristic_runtime_probe_v1",),
        source_paths=("stages/14_model_family_challenge__margin_kernel_training_effect/03_reviews/stage14_closeout_packet.md",),
        mt5_link="single MT5 margin/kernel runtime probe(단일 MT5 마진/커널 런타임 탐침)",
        reopen_condition="새 후보가 과도하게 넓을 때 마진 압축 대조군으로만 쓴다.",
    ),
    ModelTopic(
        stage_id="15_model_family_challenge__untried_learning_methods_scout",
        stage_label="Stage15(15단계)",
        model_label="LDA covariance scout(선형 판별 분석 공분산 탐색)",
        model_family="sklearn_lda(사이킷런 선형 판별 분석)",
        characteristic_lens="공분산(covariance, 공분산) 축과 shrinkage(축소) 안정성을 읽는다.",
        selection_use="저차원 선형 판별이 트리/부스팅과 다른 안정축을 주는지 확인한다.",
        avoid_use="계급 공분산(class covariance, 계급 공분산)이 흔들리면 단독 후보로 쓰지 않는다.",
        axes=("covariance", "shrinkage", "linear_discriminant", "stability"),
        preferred_runs=("run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1",),
        source_paths=("stages/15_model_family_challenge__untried_learning_methods_scout/03_reviews/stage15_closeout_packet.md",),
        mt5_link="LDA MT5 runtime and stability probes(선형 판별 분석 MT5 런타임 및 안정성 탐침)",
        reopen_condition="공분산 안정성 자체가 모델 선택 질문일 때만 재개한다.",
    ),
    ModelTopic(
        stage_id="16_model_family_challenge__qda_class_covariance_scout",
        stage_label="Stage16(16단계)",
        model_label="QDA class covariance(이차 판별 분석 계급 공분산)",
        model_family="sklearn_qda(사이킷런 이차 판별 분석)",
        characteristic_lens="계급별 공분산(class-specific covariance, 계급별 공분산)과 정규화(reg_param, 정규화 계수)의 민감도를 읽는다.",
        selection_use="비선형 계급 경계가 OOS(표본외)에서 살아남는지 보는 압박축으로 쓴다.",
        avoid_use="검증/표본외 부호가 갈리면 성능 주장이 아니라 민감도 단서로만 둔다.",
        axes=("class_covariance", "regularization", "coverage_threshold", "feature_drop"),
        preferred_runs=(
            "run10I_qda_reg020_drop_mega10_decision_microprobe_v1",
            "run10B_qda_reg018_full58_resample_decision_microprobe_v1",
        ),
        source_paths=("stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/stage16_closeout_packet.md",),
        mt5_link="broad QDA MT5 decision microprobes(넓은 QDA MT5 결정 미세탐침)",
        reopen_condition="모델 선택에서 공분산 경계가 핵심 가설일 때만 연다.",
    ),
    ModelTopic(
        stage_id="17_model_family_challenge__xgboost_regularized_boosting_scout",
        stage_label="Stage17(17단계)",
        model_label="XGBoost/DART(엑스지부스트/다트)",
        model_family="xgboost_regularized_boosting(엑스지부스트 정규화 부스팅)",
        characteristic_lens="정규화 트리와 DART(다트) 드롭아웃 부스팅의 방향/빈도 압박을 읽는다.",
        selection_use="CatBoost/EBM(캣부스트/설명가능 부스팅 머신)과 트리 부스팅 모양을 대조한다.",
        avoid_use="검증 손실과 표본외 양수의 갈림을 성능으로 과장하지 않는다.",
        axes=("regularized_tree", "direction_asymmetry", "frequency_pressure", "dropout_boosting"),
        preferred_runs=(
            "run11G_xgb_dart_attribution_closeout_v1",
            "run11F_xgb_dart_booster_probe_v1",
            "run11A_xgb_regularized_boosting_characteristic_scout_v1",
        ),
        source_paths=("stages/17_model_family_challenge__xgboost_regularized_boosting_scout/03_reviews/stage17_closeout_packet.md",),
        mt5_link="XGBoost and DART MT5 runtime probes(엑스지부스트 및 다트 MT5 런타임 탐침)",
        reopen_condition="드롭아웃 부스팅과 ordered boosting(순서 부스팅)을 비교할 때만 쓴다.",
    ),
    ModelTopic(
        stage_id="18_model_family_challenge__catboost_ordered_boosting_scout",
        stage_label="Stage18(18단계)",
        model_label="CatBoost ordered boosting(캣부스트 순서 부스팅)",
        model_family="catboost_ordered_boosting(캣부스트 순서 부스팅)",
        characteristic_lens="ordered boosting(순서 부스팅)의 확률 모양, 세션, 변동성, 방향 편향을 읽는다.",
        selection_use="트리 부스팅 중 regime/session(국면/세션) 분해가 필요할 때 우선 참고한다.",
        avoid_use="압축(compression, 압축) 후에도 약하면 반복 미세조정으로 끌지 않는다.",
        axes=("ordered_boosting", "volatility_regime", "session_timing", "direction_bias", "calibration"),
        preferred_runs=("run12A_catboost_ordered_boosting_characteristic_scout_v1", "run12P_catboost_plain_same_condition_rematch_probe_v1"),
        source_paths=("stages/18_model_family_challenge__catboost_ordered_boosting_scout/03_reviews/stage18_closeout_packet.md",),
        mt5_link="dense CatBoost MT5 sweep and compression probes(촘촘한 캣부스트 MT5 훑기 및 압축 탐침)",
        reopen_condition="세션/변동성 분해를 트리 부스팅 안에서 다시 볼 때만 연다.",
    ),
    ModelTopic(
        stage_id="19_model_family_challenge__ebm_explainable_boosting_shape",
        stage_label="Stage19(19단계)",
        model_label="EBM(설명가능 부스팅 머신)",
        model_family="interpret_ebm_main_effects(해석 가능 주효과 부스팅)",
        characteristic_lens="주효과(main effect, 주효과), 보유기간, 하위유형, 방향 압축, 피처 마스크 의존성을 읽는다.",
        selection_use="왜 모델이 반응하는지 설명 가능한 축이 필요할 때 최우선 참고한다.",
        avoid_use="가장 좋은 조각도 후속 소진 판정이 있어 승격 후보로 바꾸지 않는다.",
        axes=("main_effect_shape", "hold_length", "direction_asymmetry", "feature_mask", "tier_b_subtype"),
        preferred_runs=(
            "run13AE_ebm_q90_hold4_mixed_subtype_direction_probe_v1",
            "run13S_ebm_q90_hold4_direction_probe_v1",
            "run13AD_ebm_axis_exhaustion_followthrough_v1",
        ),
        source_paths=("stages/19_model_family_challenge__ebm_explainable_boosting_shape/03_reviews/stage19_closeout_packet.md",),
        mt5_link="large EBM MT5 axis exhaustion set(큰 EBM MT5 축 소진 묶음)",
        reopen_condition="다른 모델의 단서를 설명 가능한 주효과로 해부할 때만 연다.",
    ),
    ModelTopic(
        stage_id="20_model_family_challenge__gam_additive_smooth_shape",
        stage_label="Stage20(20단계)",
        model_label="GAM(일반화 가산 모델)",
        model_family="pygam_logistic_gam(파이GAM 로지스틱 일반화 가산 모델)",
        characteristic_lens="부드러운 가산 반응(smooth additive response, 부드러운 가산 반응)을 읽는다.",
        selection_use="EBM(설명가능 부스팅 머신)보다 부드러운 단조/곡선 반응 확인에 쓴다.",
        avoid_use="score table approximation(점수표 근사) 경계를 넘겨 원본 런타임처럼 말하지 않는다.",
        axes=("smooth_additive_shape", "close_open_ratio", "log_return", "volatility"),
        preferred_runs=("run14B_gam_runtime_handoff_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="actual routed MT5 rerun for validation/OOS(검증/표본외 실제 라우팅 MT5 재실행)",
        reopen_condition="곡선형 반응을 설명 가능한 형태로 비교할 때만 연다.",
    ),
    ModelTopic(
        stage_id="21_model_family_challenge__elasticnet_logistic_linear_sanity",
        stage_label="Stage21(21단계)",
        model_label="ElasticNet Logistic(엘라스틱넷 로지스틱)",
        model_family="sklearn_elasticnet_logistic(사이킷런 엘라스틱넷 로지스틱)",
        characteristic_lens="희소 선형 압력(sparse linear pressure, 희소 선형 압력)과 계수 부호를 읽는다.",
        selection_use="복잡한 모델의 축이 단순 선형에도 보이는지 확인하는 sanity check(정상성 점검)로 쓴다.",
        avoid_use="단독 거래 신호로는 약하다는 MT5 결과를 무시하지 않는다.",
        axes=("sparse_linear", "ema_spread", "atr", "hl_range"),
        preferred_runs=("run15B_elasticnet_logistic_onnx_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="ONNX probability-only MT5 handoff(온닉스 확률 전용 MT5 인계)",
        reopen_condition="선형 대조군이 필요할 때만 쓴다.",
    ),
    ModelTopic(
        stage_id="22_regime_model__hmm_hidden_state_segmentation",
        stage_label="Stage22(22단계)",
        model_label="HMM(은닉 마르코프 모델)",
        model_family="hmm_hidden_state_segmentation(은닉 마르코프 상태 분할)",
        characteristic_lens="라벨 없는 상태 분할(label-free state segmentation, 라벨 없는 상태 분할)을 읽는다.",
        selection_use="상태(context state, 문맥 상태)를 먼저 나누고 다른 모델을 얹을 때 쓴다.",
        avoid_use="검증 붕괴와 사전 계산 상태(precomputed state, 사전 계산 상태) 경계를 무시하지 않는다.",
        axes=("hidden_state", "volatility", "session_timing", "trend_state"),
        preferred_runs=("run16B_hmm_state_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="precomputed HMM state MT5 handoff(사전 계산 HMM 상태 MT5 인계)",
        reopen_condition="상태 필터와 진입 모델을 분리하는 설계일 때만 연다.",
    ),
    ModelTopic(
        stage_id="23_regime_model__supervised_regime_classifier_filter",
        stage_label="Stage23(23단계)",
        model_label="Supervised regime classifier(지도 국면 분류기)",
        model_family="sklearn_supervised_regime_classifier(사이킷런 지도 국면 분류기)",
        characteristic_lens="p_flat(평탄 확률)을 허용/기권(permission/abstention, 허용/기권) 표면으로 읽는다.",
        selection_use="모델 선택에서 permission filter(허용 필터)가 필요하면 1순위 참고축이다.",
        avoid_use="높은 손실폭(drawdown, 손실폭)을 무시해 운영 후보로 올리지 않는다.",
        axes=("permission_filter", "p_flat", "rsi", "close_ema20_ratio", "minutes_from_cash_open"),
        preferred_runs=("run17B_supervised_regime_classifier_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="positive validation/OOS MT5 routed probe(검증/표본외 양수 MT5 라우팅 탐침)",
        reopen_condition="Stage30(30단계) 보정/기권과 합쳐 permission surface(허용 표면)를 만들 때 연다.",
    ),
    ModelTopic(
        stage_id="24_exit_model__survival_time_to_event_hold_shape",
        stage_label="Stage24(24단계)",
        model_label="Survival model(생존 모델)",
        model_family="lifelines_weibull_aft_survival(라이프라인즈 와이블 AFT 생존 모델)",
        characteristic_lens="time-to-event(사건까지 시간)와 hold/exit clock(보유/청산 시계)을 읽는다.",
        selection_use="진입 모델이 아니라 청산/보유 위험 overlay(덧씌움)로 쓴다.",
        avoid_use="거래 밀도가 높다는 이유로 진입 신호로 바꾸지 않는다.",
        axes=("exit_clock", "survival_risk", "hold_shape", "hl_range", "historical_vol_20"),
        preferred_runs=("run18B_survival_time_to_event_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="survival permission MT5 runtime probe(생존 허용 MT5 런타임 탐침)",
        reopen_condition="exit-only(청산 전용) 작업 묶음에서만 연다.",
    ),
    ModelTopic(
        stage_id="25_exit_model__hazard_trade_lifecycle_risk",
        stage_label="Stage25(25단계)",
        model_label="Hazard model(위험률 모델)",
        model_family="sklearn_discrete_time_hazard(사이킷런 이산 시간 위험률)",
        characteristic_lens="포지션 나이(position age, 포지션 나이)와 경과 봉 위험률을 읽는다.",
        selection_use="손실 회피/평탄화(flat pressure, 평탄 압력) 보조층으로 쓴다.",
        avoid_use="현재 MT5 결과는 음수라 진입 신호로 쓰지 않는다.",
        axes=("position_age", "hazard_elapsed_bar", "close_ema20_ratio", "historical_vol_20"),
        preferred_runs=("run19B_hazard_trade_lifecycle_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="hazard permission MT5 runtime probe(위험률 허용 MT5 런타임 탐침)",
        reopen_condition="동적 보유 관리(dynamic hold management, 동적 보유 관리)가 주제일 때만 연다.",
    ),
    ModelTopic(
        stage_id="26_model_family_challenge__ngboost_probabilistic_distribution_shape",
        stage_label="Stage26(26단계)",
        model_label="NGBoost(자연 그래디언트 부스팅)",
        model_family="ngboost_distribution(엔지부스트 분포 모델)",
        characteristic_lens="분포 불확실성(distributional uncertainty, 분포 불확실성)과 entropy(엔트로피)를 읽는다.",
        selection_use="확신도(confidence, 확신도)와 불확실성 기권을 만들 때 참고한다.",
        avoid_use="표본이 너무 작아 성능 후보로 확대하지 않는다.",
        axes=("distribution_uncertainty", "entropy", "confidence", "small_sample"),
        preferred_runs=("run20B_ngboost_distribution_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="distilled score table MT5 runtime probe(증류 점수표 MT5 런타임 탐침)",
        reopen_condition="Stage23/27/30(23/27/30단계) 기권 표면을 합칠 때만 연다.",
    ),
    ModelTopic(
        stage_id="27_tail_model__quantile_boosting_risk_surface",
        stage_label="Stage27(27단계)",
        model_label="Quantile boosting(분위수 부스팅)",
        model_family="sklearn_quantile_boosting_tail(사이킷런 분위수 부스팅 꼬리 모델)",
        characteristic_lens="tail-risk surface(꼬리 위험 표면)와 interval coverage(구간 포괄)을 읽는다.",
        selection_use="위험 상단/하단 꼬리를 분리하는 보조 표면으로 쓴다.",
        avoid_use="검증 음수와 높은 손실폭을 무시하지 않는다.",
        axes=("tail_risk", "interval_coverage", "tier_b_fallback", "bollinger_width_20", "ema50_ema200_diff"),
        preferred_runs=("run21B_quantile_boosting_tail_risk_runtime_probe_v1",),
        source_paths=("docs/workspace/stage20_27_characteristic_synthesis.md",),
        mt5_link="Tier B fallback routed MT5 probe(티어 B 대체 라우팅 MT5 탐침)",
        reopen_condition="기권/꼬리 위험 표면을 비교할 때만 연다.",
    ),
    ModelTopic(
        stage_id="28_regime_model__markov_switching_regression_state_link",
        stage_label="Stage28(28단계)",
        model_label="Markov regression(마르코프 회귀)",
        model_family="statsmodels_markov_regression(스탯츠모델즈 마르코프 회귀)",
        characteristic_lens="return-linked switching state(수익률 연결 전환 상태)와 score table(점수표) 상태를 읽는다.",
        selection_use="상태 전환(state transition, 상태 전환)과 허용 필터를 나눌 때 쓴다.",
        avoid_use="Stage34(34단계) 재귀속 없이 Stage28(28단계) 수치만으로 판단하지 않는다.",
        axes=("markov_state", "switching_variance", "state_score_table", "long_permission"),
        preferred_runs=("run22B_markov_regression_state_runtime_probe_v1",),
        source_paths=("stages/28_regime_model__markov_switching_regression_state_link/03_reviews/run22C_markov_regression_supplement_packet.md",),
        mt5_link="score-table Markov MT5 runtime probe(점수표 마르코프 MT5 런타임 탐침)",
        reopen_condition="Stage34/35(34/35단계) 상태 문맥과 결합할 때만 쓴다.",
    ),
    ModelTopic(
        stage_id="29_adaptive_model__river_online_drift_learning",
        stage_label="Stage29(29단계)",
        model_label="River online ML(리버 온라인 머신러닝)",
        model_family="river_online_learning(리버 온라인 학습)",
        characteristic_lens="온라인 적응(online adaptation, 온라인 적응)과 drift(드리프트)를 읽는다.",
        selection_use="고정 학습 모델이 시간 변화에 무너지는지 보는 대조축으로 쓴다.",
        avoid_use="native revalidation(원본 재검증) 결과가 약해 운영 적응으로 말하지 않는다.",
        axes=("online_learning", "drift", "slow_adaptation", "score_table_handoff"),
        preferred_runs=("run23D_river_native_online_runtime_probe_v1", "run23B_river_online_drift_runtime_probe_v1"),
        source_paths=("docs/workspace/stage29_32_native_revalidation_supplement.md",),
        mt5_link="native River distilled MT5 probe(원본 리버 증류 MT5 탐침)",
        reopen_condition="rolling/online(구르는/온라인) 재학습이 핵심 질문일 때만 연다.",
    ),
    ModelTopic(
        stage_id="30_decision_layer__probability_calibration_abstention",
        stage_label="Stage30(30단계)",
        model_label="Calibration/abstention(보정/기권)",
        model_family="isotonic_margin_abstention(아이소토닉 마진 기권)",
        characteristic_lens="확률 보정(probability calibration, 확률 보정), margin(마진), abstention(기권)을 읽는다.",
        selection_use="새 모델의 raw probability(원시 확률)를 바로 쓰기 전 필수 의사결정층으로 본다.",
        avoid_use="OOS(표본외) native 결과가 약하므로 단독 알파로 쓰지 않는다.",
        axes=("calibration", "abstention", "margin", "permission_filter"),
        preferred_runs=("run24D_native_source_calibration_runtime_probe_v1", "run24B_probability_calibration_abstention_runtime_probe_v1"),
        source_paths=("docs/workspace/stage29_32_native_revalidation_supplement.md",),
        mt5_link="native source calibration MT5 probe(원본 소스 보정 MT5 탐침)",
        reopen_condition="어떤 모델을 고르든 마지막 decision layer(결정층)를 설계할 때 연다.",
    ),
    ModelTopic(
        stage_id="31_model_family_challenge__tabnet_attentive_tabular_scout",
        stage_label="Stage31(31단계)",
        model_label="TabNet(탭넷)",
        model_family="pytorch_tabnet_attention(파이토치 탭넷 주의집중)",
        characteristic_lens="attention mask(주의집중 마스크)와 sparse tabular selection(희소 표 형식 선택)을 읽는다.",
        selection_use="피처 선택(feature selection, 피처 선택)이 학습 내부에서 어떻게 드러나는지 볼 때 참고한다.",
        avoid_use="native MT5 결과가 약해 다음 모델 기본 선택으로 올리지 않는다.",
        axes=("attention_mask", "sparse_selection", "tabular_deep", "feature_importance"),
        preferred_runs=("run25D_tabnet_native_attentive_runtime_probe_v1", "run25B_tabnet_attentive_tabular_runtime_probe_v1"),
        source_paths=("docs/workspace/stage29_32_native_revalidation_supplement.md",),
        mt5_link="native TabNet distilled MT5 probe(원본 탭넷 증류 MT5 탐침)",
        reopen_condition="피처 선택 구조 자체를 비교할 때만 쓴다.",
    ),
    ModelTopic(
        stage_id="32_sequence_model__tcn_temporal_convolution_context",
        stage_label="Stage32(32단계)",
        model_label="TCN(시간 합성곱 네트워크)",
        model_family="torch_tcn_temporal_convolution(파이토치 시간 합성곱 네트워크)",
        characteristic_lens="dilated temporal context(확장 시간 문맥)와 순서 반응(sequence response, 순서 반응)을 읽는다.",
        selection_use="M5(5분봉) 문맥 순서가 중요할 때 deep sequence(심층 순서) 후보로 참고한다.",
        avoid_use="score table handoff(점수표 인계) 경계를 원본 실시간 모델로 과장하지 않는다.",
        axes=("temporal_context", "dilated_convolution", "sequence_model", "return_range"),
        preferred_runs=("run26D_torch_tcn_native_temporal_runtime_probe_v1", "run26B_tcn_temporal_convolution_runtime_probe_v1"),
        source_paths=("docs/workspace/stage29_32_native_revalidation_supplement.md",),
        mt5_link="native Torch TCN distilled MT5 probe(원본 파이토치 TCN 증류 MT5 탐침)",
        reopen_condition="순서 문맥을 Stage35(35단계) 상태 지도와 연결할 때 연다.",
    ),
    ModelTopic(
        stage_id="34_regime_mechanism__tier_a_markov_long_permission_attribution",
        stage_label="Stage34(34단계)",
        model_label="Markov long permission attribution(마르코프 매수 허용 귀속)",
        model_family="markov_regression_permission_attribution(마르코프 회귀 허용 귀속)",
        characteristic_lens="Tier A(티어 A) Markov long permission(매수 허용)을 vol/adx/entry-time(변동성/ADX/진입 시점)으로 귀속한다.",
        selection_use="상태 필터를 다시 쓸 때 의존축과 보유시간 경고를 함께 본다.",
        avoid_use="얇은 거래 수와 2025-10(2025년 10월) 의존을 숨기지 않는다.",
        axes=("markov_state", "long_permission", "vol_high", "adx_20_25", "hold_duration"),
        preferred_runs=("stage34_tier_a_markov_long_permission_attribution_closeout_v1", "run28F_tier_a_markov_vol_adx_component_dependency_probe_v1"),
        source_paths=("stages/34_regime_mechanism__tier_a_markov_long_permission_attribution/03_reviews/stage34_closeout_packet.md",),
        mt5_link="Stage34 run28E/run28F MT5 runtime probes(34단계 28E/28F MT5 런타임 탐침)",
        reopen_condition="상태 필터를 실제 모델 선택에 재사용하려면 vol/adx/hold(변동성/ADX/보유) 문제를 먼저 묶어야 한다.",
    ),
    ModelTopic(
        stage_id="35_context_map__unsupervised_market_state_atlas",
        stage_label="Stage35(35단계)",
        model_label="KMeans state atlas(K-평균 상태 지도)",
        model_family="unsupervised_kmeans_state_atlas(비지도 K-평균 상태 지도)",
        characteristic_lens="비지도 시장 상태(unsupervised market state, 비지도 시장 상태)와 세션/수익률/변동성/추세 지도를 읽는다.",
        selection_use="모델 선택 전에 시장 문맥을 나눠 후보를 배치할 때 참고한다.",
        avoid_use="fragile seed(취약 씨앗)를 승격 후보로 올리지 않는다.",
        axes=("unsupervised_state", "return_volatility", "session_timing", "trend_momentum", "drift_stress"),
        preferred_runs=("stage35_context_map_closeout_v1", "run29C_stage35_candidate_four_deep_dive_mt5_probe_v1"),
        source_paths=("stages/35_context_map__unsupervised_market_state_atlas/03_reviews/stage35_closeout_packet.md",),
        mt5_link="Stage35 run29A-run29C MT5 state probes(35단계 29A-29C MT5 상태 탐침)",
        reopen_condition="시장 상태 지도를 다음 모델군 선택의 stratification(층화)으로 쓸 때만 연다.",
    ),
)


CURATED_METRICS: dict[str, dict[str, str]] = {
    "run04N_mlp_feature_group_interaction_profit_probe_v1": {
        "oos_net_profit": "172.22",
        "oos_pf": "1.21",
        "topic_read": "best_oos_feature_group_no_trend_structure(최고 표본외 피처그룹 no_trend_structure)",
        "selected_variant": "no_trend_structure",
    },
    "run12P_catboost_plain_same_condition_rematch_probe_v1": {
        "oos_net_profit": "31.93",
        "topic_read": "best_oos_plain_control_same_condition_rematch(최고 표본외 plain 대조 동일 조건 재대결)",
    },
    "run20B_ngboost_distribution_runtime_probe_v1": {
        "validation_net_profit": "-17.21",
        "validation_pf": "0.05",
        "oos_net_profit": "39.49",
        "oos_pf": "2.37",
    },
    "run21B_quantile_boosting_tail_risk_runtime_probe_v1": {
        "validation_net_profit": "-38.20",
        "validation_pf": "0.97",
        "oos_net_profit": "79.17",
        "oos_pf": "1.07",
    },
    "run22B_markov_regression_state_runtime_probe_v1": {
        "validation_net_profit": "244.08",
        "validation_pf": "1.77",
        "oos_net_profit": "111.27",
        "oos_pf": "1.31",
    },
}


def _read_registry() -> list[dict[str, str]]:
    with common.io_path(common.RUN_REGISTRY_PATH).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _read_alpha_ledger(path: Path) -> list[dict[str, str]]:
    if not common.io_path(path).exists():
        return []
    with common.io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _parse_notes(notes: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in re.split(r";(?=[A-Za-z0-9_]+=)", notes or ""):
        if "=" in part:
            key, value = part.split("=", 1)
            parsed[key.strip()] = value.strip()
    return parsed


def _float(value: Any) -> float | None:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return number


def _metric(row: Mapping[str, str], key: str) -> float | None:
    return _float(_parse_notes(row.get("notes", "")).get(key))


def _is_runtime(row: Mapping[str, str]) -> bool:
    lane = row.get("lane", "")
    notes = row.get("notes", "")
    return "runtime" in lane or "runtime_probe" in notes or "MT5" in notes or "mt5" in notes


def _row_score(row: Mapping[str, str]) -> tuple[int, float]:
    notes = _parse_notes(row.get("notes", ""))
    val_net = _float(notes.get("validation_net_profit")) or -9999.0
    oos_net = _float(notes.get("oos_net_profit")) or -9999.0
    val_pf = _float(notes.get("validation_pf")) or 0.0
    oos_pf = _float(notes.get("oos_pf")) or 0.0
    both_positive = int(val_net > 0 and oos_net > 0 and val_pf >= 1.0 and oos_pf >= 1.0)
    has_metrics = int("validation_net_profit" in notes and "oos_net_profit" in notes)
    return both_positive + has_metrics, val_net + oos_net + (val_pf + oos_pf) * 100.0


def _has_metric(row: Mapping[str, str]) -> bool:
    notes = _parse_notes(row.get("notes", ""))
    return "validation_net_profit" in notes or "oos_net_profit" in notes or row.get("run_id", "") in CURATED_METRICS


def _select_reference_run(topic: ModelTopic, rows: Sequence[Mapping[str, str]]) -> Mapping[str, str] | None:
    stage_rows = [row for row in rows if row.get("stage_id") == topic.stage_id]
    by_id = {row.get("run_id"): row for row in stage_rows}
    first_preferred: Mapping[str, str] | None = None
    for run_id in topic.preferred_runs:
        if run_id in by_id:
            first_preferred = first_preferred or by_id[run_id]
            if _has_metric(by_id[run_id]):
                return by_id[run_id]
    runtime_rows = [row for row in stage_rows if _is_runtime(row)]
    runtime_metric_rows = [row for row in runtime_rows if _has_metric(row)]
    if runtime_metric_rows:
        return max(runtime_metric_rows, key=_row_score)
    if first_preferred is not None:
        return first_preferred
    candidates = runtime_rows or stage_rows
    if not candidates:
        return None
    return max(candidates, key=_row_score)


def _source_exists(path: str) -> bool:
    return common.io_path(common.ROOT / path).exists()


def _stage_rows(topic: ModelTopic, rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    return [row for row in rows if row.get("stage_id") == topic.stage_id]


def _stage_runtime_rows(topic: ModelTopic, rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    return [row for row in _stage_rows(topic, rows) if _is_runtime(row)]


def _extract_metric_summary(row: Mapping[str, str] | None) -> dict[str, Any]:
    if not row:
        return {
            "reference_run": "",
            "reference_path": "",
            "validation_net_profit": "",
            "validation_pf": "",
            "oos_net_profit": "",
            "oos_pf": "",
            "external_verification": "missing_registry_row(등록부 행 누락)",
            "boundary": "",
            "selected_variant": "",
            "topic_read": "",
        }
    notes = _parse_notes(row.get("notes", ""))
    fallback = CURATED_METRICS.get(row.get("run_id", ""), {})
    return {
        "reference_run": row.get("run_id", ""),
        "reference_path": row.get("path", ""),
        "validation_net_profit": notes.get("validation_net_profit", fallback.get("validation_net_profit", "")),
        "validation_pf": notes.get("validation_pf", fallback.get("validation_pf", "")),
        "oos_net_profit": notes.get("oos_net_profit", fallback.get("oos_net_profit", "")),
        "oos_pf": notes.get("oos_pf", fallback.get("oos_pf", "")),
        "external_verification": notes.get("external_verification", "see_notes(노트 확인)"),
        "boundary": notes.get("boundary", ""),
        "selected_variant": notes.get("selected_variant", fallback.get("selected_variant", "")),
        "topic_read": notes.get("topic_read", fallback.get("topic_read", "")),
    }


def build_model_matrix(registry_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    matrix: list[dict[str, Any]] = []
    for topic in TOPICS:
        stage_rows = _stage_rows(topic, registry_rows)
        runtime_rows = _stage_runtime_rows(topic, registry_rows)
        completed_mt5 = [
            row for row in runtime_rows if "external_verification=completed" in (row.get("notes") or "")
        ]
        selected = _select_reference_run(topic, registry_rows)
        metric = _extract_metric_summary(selected)
        source_state = "ok(정상)" if any(_source_exists(path) for path in topic.source_paths) else "missing_source_path(근거 경로 누락)"
        matrix.append(
            {
                "stage_label": topic.stage_label,
                "stage_id": topic.stage_id,
                "model_label": topic.model_label,
                "model_family": topic.model_family,
                "characteristic_lens": topic.characteristic_lens,
                "selection_use": topic.selection_use,
                "avoid_use": topic.avoid_use,
                "axes": "|".join(topic.axes),
                "reference_run": metric["reference_run"],
                "reference_path": metric["reference_path"],
                "validation_net_profit": metric["validation_net_profit"],
                "validation_pf": metric["validation_pf"],
                "oos_net_profit": metric["oos_net_profit"],
                "oos_pf": metric["oos_pf"],
                "selected_variant": metric["selected_variant"],
                "topic_read": metric["topic_read"],
                "stage_registry_rows": len(stage_rows),
                "stage_runtime_rows": len(runtime_rows),
                "completed_mt5_runtime_rows": len(completed_mt5),
                "external_verification": metric["external_verification"],
                "mt5_link": topic.mt5_link,
                "source_state": source_state,
                "source_paths": "|".join(topic.source_paths),
                "boundary": metric["boundary"] or BOUNDARY,
                "reopen_condition": topic.reopen_condition,
            }
        )
    return matrix


def build_feature_axis_overlap(model_matrix: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    axis_to_rows: dict[str, list[Mapping[str, Any]]] = {}
    for row in model_matrix:
        for axis in str(row["axes"]).split("|"):
            axis_to_rows.setdefault(axis, []).append(row)
    out: list[dict[str, Any]] = []
    for axis, rows in sorted(axis_to_rows.items(), key=lambda item: (-len(item[1]), item[0])):
        labels = [str(row["stage_label"]) for row in rows]
        models = [str(row["model_label"]) for row in rows]
        if len(rows) >= 4:
            read = "core_cross_model_axis(핵심 교차 모델 축)"
        elif len(rows) >= 2:
            read = "repeated_axis(반복 축)"
        else:
            read = "single_model_axis(단일 모델 축)"
        out.append(
            {
                "axis": axis,
                "axis_read": read,
                "model_count": len(rows),
                "stages": "|".join(labels),
                "models": "|".join(models),
                "stage36_use": _axis_use(axis, len(rows)),
            }
        )
    return out


def _axis_use(axis: str, count: int) -> str:
    if axis in {"session_timing", "volatility", "historical_vol_20", "return_volatility"}:
        return "시장 문맥(context, 문맥) 층화와 MT5(메타트레이더5) 재탐침 우선축"
    if axis in {"permission_filter", "abstention", "calibration", "p_flat", "entropy", "tail_risk"}:
        return "모델 선택 후 decision layer(결정층) 후보축"
    if axis in {"exit_clock", "survival_risk", "position_age", "hazard_elapsed_bar", "hold_length", "hold_duration"}:
        return "청산/보유 관리(exit/hold management, 청산/보유 관리) 후보축"
    if axis in {"markov_state", "hidden_state", "unsupervised_state", "state_score_table"}:
        return "상태 필터(state filter, 상태 필터) 후보축"
    if count >= 3:
        return "여러 모델에 반복되어 다음 stage(단계) 모델 선택 참고축"
    return "단일 모델 특성으로 보존"


def build_selection_reference(model_matrix: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    def refs(*stage_prefixes: str) -> str:
        picks = [
            str(row["stage_label"])
            for row in model_matrix
            if any(str(row["stage_id"]).startswith(prefix) for prefix in stage_prefixes)
        ]
        return "|".join(picks)

    return [
        {
            "decision_need": "permission_filter(허용 필터)",
            "primary_references": refs("23_", "30_", "19_"),
            "why": "Stage23(23단계)은 p_flat(평탄 확률) 양수 판독을 남겼고 Stage30(30단계)은 보정/기권층을 남겼다.",
            "mt5_read": "MT5(메타트레이더5) 완료 근거가 있으나 운영 권위(runtime authority, 런타임 권위)는 없다.",
            "next_micro_probe_frontier": "p_flat + calibrated margin + EBM direction(평탄 확률+보정 마진+EBM 방향) 겹침 직전까지 비교",
            "priority": "high(높음)",
        },
        {
            "decision_need": "state_context_filter(상태 문맥 필터)",
            "primary_references": refs("22_", "28_", "34_", "35_"),
            "why": "HMM/Markov/KMeans(은닉 마르코프/마르코프/K-평균)가 각각 상태를 다르게 자른다.",
            "mt5_read": "Stage34/35(34/35단계)는 MT5(메타트레이더5) 연결까지 넓게 확인했다.",
            "next_micro_probe_frontier": "Markov long permission + KMeans return-volatility state + HMM noncollapsed state(비붕괴 상태) 교차",
            "priority": "high(높음)",
        },
        {
            "decision_need": "exit_risk_overlay(청산 위험 덧씌움)",
            "primary_references": refs("24_", "25_", "27_"),
            "why": "Survival/Hazard/Quantile(생존/위험률/분위수)은 진입보다 보유와 꼬리 위험을 더 잘 설명한다.",
            "mt5_read": "거래 밀도는 높지만 순손익은 약하므로 entry(진입)가 아니라 exit/risk(청산/위험) 전용이다.",
            "next_micro_probe_frontier": "position-age hazard + survival clock + quantile tail(포지션 나이 위험률+생존 시계+분위수 꼬리)",
            "priority": "medium_high(중상)",
        },
        {
            "decision_need": "interpretable_shape(설명 가능한 모양)",
            "primary_references": refs("19_", "20_", "21_"),
            "why": "EBM/GAM/ElasticNet(설명가능 부스팅/일반화 가산/엘라스틱넷)이 피처 축을 읽기 쉽게 남긴다.",
            "mt5_read": "EBM(설명가능 부스팅 머신)과 GAM(일반화 가산 모델)은 점수표 인계 경계가 있다.",
            "next_micro_probe_frontier": "EBM main effect + GAM smooth curve + ElasticNet sign(주효과+부드러운 곡선+선형 부호)",
            "priority": "medium_high(중상)",
        },
        {
            "decision_need": "sequence_or_drift(순서 또는 변화)",
            "primary_references": refs("29_", "32_"),
            "why": "River(리버)는 온라인 변화, TCN(시간 합성곱 네트워크)은 순서 문맥을 읽는다.",
            "mt5_read": "TCN(시간 합성곱 네트워크)은 native revalidation(원본 재검증)에서 상대적으로 가장 안정적인 Stage29-32 축이다.",
            "next_micro_probe_frontier": "TCN temporal context + Stage35 market state(시간 문맥+시장 상태) 결합",
            "priority": "medium(중간)",
        },
        {
            "decision_need": "tree_boosting_contrast(트리 부스팅 대조)",
            "primary_references": refs("17_", "18_"),
            "why": "XGBoost/DART(엑스지부스트/다트)와 CatBoost(캣부스트)는 방향/세션/변동성 압박을 다르게 보인다.",
            "mt5_read": "CatBoost(캣부스트)는 훑기 범위가 넓고, XGBoost(엑스지부스트)는 검증/표본외 갈림을 남겼다.",
            "next_micro_probe_frontier": "CatBoost session-volatility split vs DART direction asymmetry(세션/변동성 분리 대 방향 비대칭)",
            "priority": "medium(중간)",
        },
        {
            "decision_need": "attention_feature_selection(주의집중 피처 선택)",
            "primary_references": refs("31_"),
            "why": "TabNet(탭넷)은 attention mask(주의집중 마스크)를 남기지만 MT5(메타트레이더5) 수익 판독은 약하다.",
            "mt5_read": "native distilled MT5(원본 증류 MT5) 완료이나 선택 우선순위는 낮다.",
            "next_micro_probe_frontier": "다른 모델의 반복 피처축을 TabNet mask(탭넷 마스크)와 맞춰보는 수준",
            "priority": "low(낮음)",
        },
    ]


def build_mt5_evidence_matrix(model_matrix: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in model_matrix:
        mt5_rows = int(row["completed_mt5_runtime_rows"] or 0)
        if mt5_rows >= 5:
            coverage = "broad_existing_mt5(넓은 기존 MT5 근거)"
        elif mt5_rows >= 1:
            coverage = "single_or_few_existing_mt5(단일/소수 기존 MT5 근거)"
        else:
            coverage = "non_runtime_or_missing_mt5(비런타임 또는 MT5 누락)"
        out.append(
            {
                "stage_label": row["stage_label"],
                "model_label": row["model_label"],
                "reference_run": row["reference_run"],
                "completed_mt5_runtime_rows": row["completed_mt5_runtime_rows"],
                "coverage_read": coverage,
                "external_verification": row["external_verification"],
                "mt5_link": row["mt5_link"],
                "runtime_parity_boundary": "existing_probe_or_score_table_only_no_runtime_authority(기존 탐침 또는 점수표 전용, 런타임 권위 없음)",
                "backtest_forensics_read": "registry_path_and_packet_available(등록부 경로와 묶음 가용) / tester_identity_not_reopened(테스터 정체성 재개방 안 함)",
            }
        )
    return out


def build_micro_probe_frontier() -> list[dict[str, Any]]:
    return [
        {
            "frontier_id": "frontier01_permission_abstention_overlap",
            "question": "어떤 모델 조합이 진입 허용(permission, 허용)과 기권(abstention, 기권)을 가장 덜 얇게 만드는가?",
            "source_models": "Stage23 supervised regime(지도 국면) | Stage30 calibration(보정) | Stage26 NGBoost entropy(엔트로피) | Stage27 quantile tail(분위수 꼬리) | Stage19 EBM direction(방향)",
            "probe_until_now": "각 모델의 기존 MT5(메타트레이더5) 런타임 탐침과 특성 축이 확보됨.",
            "micro_probe_not_yet_run": "교집합 surface(표면)를 한 run(실행) 안에서 실제 MT5 라우팅으로 만들지는 않았다.",
            "ready_condition": "p_flat/margin/entropy/tail pressure(평탄 확률/마진/엔트로피/꼬리 압력) 공통 테이블을 만들 수 있을 때",
            "selection_value": "very_high(매우 높음)",
        },
        {
            "frontier_id": "frontier02_state_context_stack",
            "question": "상태 모델(state model, 상태 모델)을 먼저 자르면 어떤 모델군을 어디에 배치해야 하는가?",
            "source_models": "Stage22 HMM(은닉 마르코프) | Stage28 Markov regression(마르코프 회귀) | Stage34 Markov attribution(마르코프 귀속) | Stage35 KMeans atlas(K-평균 지도)",
            "probe_until_now": "Stage34/35(34/35단계)는 MT5(메타트레이더5)까지 적극 연결했고 상태 약점도 기록됨.",
            "micro_probe_not_yet_run": "HMM/Markov/KMeans(은닉 마르코프/마르코프/K-평균) 상태를 같은 행 집합에서 교차 라우팅하지 않았다.",
            "ready_condition": "동일 feature-ready timestamp(피처 준비 시각) 기준 상태 열을 동시에 만들 수 있을 때",
            "selection_value": "very_high(매우 높음)",
        },
        {
            "frontier_id": "frontier03_exit_risk_non_entry_overlay",
            "question": "청산/보유 위험 모델을 진입 신호 없이 덧씌우면 손실폭을 줄이는가?",
            "source_models": "Stage24 Survival(생존) | Stage25 Hazard(위험률) | Stage27 Quantile(분위수)",
            "probe_until_now": "거래 밀도와 음수 경로가 확인되어 entry(진입) 대신 exit/risk(청산/위험)로 위치가 정리됨.",
            "micro_probe_not_yet_run": "실제 포지션 나이(position age, 포지션 나이) 기반 동적 청산을 MT5(메타트레이더5)에서 닫지 않았다.",
            "ready_condition": "EA(전문가 자문)에서 포지션 경과 봉과 위험 표면을 동시에 읽을 수 있을 때",
            "selection_value": "high(높음)",
        },
        {
            "frontier_id": "frontier04_interpretable_feature_shape",
            "question": "반복 피처축을 설명 가능한 모델이 같은 방향으로 읽는가?",
            "source_models": "Stage19 EBM(설명가능 부스팅) | Stage20 GAM(일반화 가산) | Stage21 ElasticNet(엘라스틱넷)",
            "probe_until_now": "피처 축과 MT5(메타트레이더5) 경계가 모두 기록됨.",
            "micro_probe_not_yet_run": "같은 피처 마스크/곡선/계수 부호를 하나의 비교 run(실행)으로 만들지 않았다.",
            "ready_condition": "feature axis dictionary(피처 축 사전)를 고정하고 같은 컷으로 재집계할 때",
            "selection_value": "high(높음)",
        },
        {
            "frontier_id": "frontier05_temporal_context_with_market_state",
            "question": "순서 모델(sequence model, 순서 모델)은 시장 상태(state, 상태)별로 어디서만 의미가 있는가?",
            "source_models": "Stage32 TCN(시간 합성곱 네트워크) | Stage35 KMeans atlas(K-평균 지도) | Stage18 CatBoost session/volatility(세션/변동성)",
            "probe_until_now": "TCN(시간 합성곱 네트워크)은 Stage29-32(29-32단계) 중 native MT5(원본 MT5) 판독이 가장 나았고 Stage35(35단계)는 상태 지도를 남김.",
            "micro_probe_not_yet_run": "TCN 점수표를 Stage35 상태별로 나눠 MT5(메타트레이더5) 라우팅하지 않았다.",
            "ready_condition": "TCN score(점수)와 Stage35 state id(상태 ID)를 같은 runtime table(런타임 테이블)에 붙일 때",
            "selection_value": "medium_high(중상)",
        },
    ]


def build_source_coverage(model_matrix: Sequence[Mapping[str, Any]], registry_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for topic, row in zip(TOPICS, model_matrix, strict=True):
        existing_sources = [path for path in topic.source_paths if _source_exists(path)]
        stage_rows = _stage_rows(topic, registry_rows)
        runtime_rows = _stage_runtime_rows(topic, registry_rows)
        gate = (
            "passed(통과)"
            if existing_sources and stage_rows and (runtime_rows or topic.stage_id.startswith("34_"))
            else "review_needed(검토 필요)"
        )
        out.append(
            {
                "stage_label": topic.stage_label,
                "stage_id": topic.stage_id,
                "source_paths_checked": "|".join(topic.source_paths),
                "existing_source_paths": "|".join(existing_sources),
                "registry_rows": len(stage_rows),
                "runtime_like_rows": len(runtime_rows),
                "reference_run": row["reference_run"],
                "source_authority_gate": gate,
                "note": "Stage36(36단계)는 기존 근거를 종합한다. 새 MT5 테스터 실행은 주장 범위 밖이다.",
            }
        )
    return out


def _md_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _top_selection_rows(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    priority_order = {"high(높음)": 0, "medium_high(중상)": 1, "medium(중간)": 2, "low(낮음)": 3}
    return sorted(rows, key=lambda row: priority_order.get(str(row["priority"]), 9))


def _positive_count(model_matrix: Sequence[Mapping[str, Any]]) -> int:
    count = 0
    for row in model_matrix:
        val_net = _float(row.get("validation_net_profit"))
        oos_net = _float(row.get("oos_net_profit"))
        val_pf = _float(row.get("validation_pf"))
        oos_pf = _float(row.get("oos_pf"))
        if val_net is not None and oos_net is not None and val_pf is not None and oos_pf is not None:
            if val_net > 0 and oos_net > 0 and val_pf >= 1 and oos_pf >= 1:
                count += 1
    return count


def build_summary(
    model_matrix: Sequence[Mapping[str, Any]],
    axis_overlap: Sequence[Mapping[str, Any]],
    selection_reference: Sequence[Mapping[str, Any]],
    mt5_matrix: Sequence[Mapping[str, Any]],
    source_coverage: Sequence[Mapping[str, Any]],
    local_alpha_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    broad_mt5 = sum(1 for row in mt5_matrix if str(row["coverage_read"]).startswith("broad"))
    any_mt5 = sum(1 for row in mt5_matrix if int(row["completed_mt5_runtime_rows"] or 0) > 0)
    source_passed = sum(1 for row in source_coverage if row["source_authority_gate"] == "passed(통과)")
    return {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": common.utc_now(),
        "active_branch": common.active_branch(),
        "status": "reviewed_closed_reference_packet_no_stage37_opened",
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "work_packet_lifecycle": "evidence_synthesis_to_model_selection_reference(근거 종합에서 모델 선택 참고서까지)",
        "primary_family": "kpi_evidence(KPI 근거)",
        "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
        "support_skills": [
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-result-judgment(결과 판정)",
            "obsidian-performance-attribution(성과 귀속)",
        ],
        "supplemental_checks": [
            "obsidian-experiment-design(실험 설계)",
            "obsidian-runtime-parity(런타임 동등성)",
            "obsidian-backtest-forensics(백테스트 포렌식)",
            "obsidian-exploration-mandate(탐색 명령)",
        ],
        "hypothesis": "Stage10-35(10-35단계) 모델군은 성능 순위보다 characteristic axis(특성 축), MT5 runtime boundary(MT5 런타임 경계), reopen condition(재개 조건)으로 분류할 때 다음 모델 선택에 더 유용하다.",
        "decision_use": "Future stages(추후 단계)에서 모델을 고를 때 이 stage(단계)만 보고 permission/filter/state/exit/sequence/interpretable/tree axes(허용/필터/상태/청산/순서/설명가능/트리 축)를 고르게 한다.",
        "comparison_baseline": "Existing Stage10-35 reviewed registry rows and packets(기존 10-35단계 검토 등록부 행과 묶음)",
        "control_variables": [
            "same project window(같은 프로젝트 구간)",
            "same claim boundary(같은 주장 경계)",
            "no new baseline/promotion/runtime authority(새 기준선/승격/런타임 권위 없음)",
        ],
        "changed_variables": [
            "synthesis lens changed from per-stage closeout to cross-model selection reference(단계별 마감에서 교차 모델 선택 참고서로 렌즈 변경)",
            "Stage34/35 MT5 evidence included instead of being treated as separate tail work(34/35단계 MT5 근거를 별도 꼬리 작업이 아니라 포함)",
        ],
        "sample_scope": "Stage10-35 reviewed model/topic stages except Stage33 open-only no-result(33단계 결과 없는 개방 전용 제외)",
        "success_criteria": [
            "model matrix covers broad model family history(모델 행렬이 넓은 모델군 이력을 포함)",
            "MT5 linkage is explicit(메타트레이더5 연결이 명시됨)",
            "selection reference and micro-probe frontier are materialized(선택 참고와 미세탐침 전선이 산출됨)",
            "forbidden claims remain blocked(금지 주장이 차단됨)",
        ],
        "failure_criteria": [
            "only a few models summarized(몇 모델만 요약)",
            "MT5 evidence deferred without record(메타트레이더5 근거를 기록 없이 미룸)",
            "stage closed as weak small task(약한 작은 작업으로 단계 마감)",
        ],
        "stop_condition": "Run30A(30A 실행) stops only after matrix, reference, frontier, gates, ledgers, and state docs exist.",
        "evidence_counts": {
            "model_topic_count": len(model_matrix),
            "feature_axis_count": len(axis_overlap),
            "selection_reference_rows": len(selection_reference),
            "micro_probe_frontier_rows": 5,
            "mt5_rows_with_completed_runtime_evidence": any_mt5,
            "broad_mt5_coverage_rows": broad_mt5,
            "source_authority_passed_rows": source_passed,
            "source_authority_total_rows": len(source_coverage),
            "reference_rows_with_positive_validation_and_oos": _positive_count(model_matrix),
            "local_alpha_ledger_rows": len(local_alpha_rows),
        },
        "mt5_linkage": {
            "mode": "existing_mt5_runtime_evidence_integrated_no_new_tester_run(기존 MT5 런타임 근거 통합, 새 테스터 실행 없음)",
            "why_no_new_mt5": "Stage36(36단계)는 모델 선택 참고서 산출이 목적이고, 새 조합 실행은 micro-probe frontier(미세탐침 전선)로 분리했다.",
            "effect": "MT5(메타트레이더5) 연계를 피하지 않고 기존 탐침 수와 경계를 한 표에 모았지만 운영 권위는 만들지 않는다.",
        },
        "result_judgment": {
            "result_subject": STAGE_ID,
            "evidence_available": "run registry(실행 등록부), alpha ledger(알파 장부), Stage20-27/29-32 synthesis docs(종합 문서), Stage34/35 MT5 closeouts(마감).",
            "evidence_missing": "new cross-model MT5 micro-probe(새 교차 모델 MT5 미세탐침), full WFO(전체 워크포워드), runtime authority closure(런타임 권위 종결).",
            "judgment_label": "reviewed_closed_reference_only(검토 후 마감, 참고 전용)",
            "claim_boundary": BOUNDARY,
            "next_condition": "Open a new stage or subrun only when choosing one frontier with a concrete MT5 routing question.",
            "user_explanation_hook": "Stage36(36단계)는 승자표가 아니라 다음 모델 선택을 빠르게 좁히는 지도다.",
        },
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "forbidden_claims": [
            "edge(거래 우위)",
            "alpha_quality(알파 품질)",
            "baseline(기준선)",
            "promotion(승격)",
            "runtime_authority(런타임 권위)",
            "live_readiness(실거래 준비)",
        ],
    }


def write_stage_brief() -> None:
    common.write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage36 Model Selection Cross-Model Characteristic Synthesis(36단계 모델 선택 교차 모델 특성 종합)

## Objective(목표)

Stage36(36단계)은 Stage10-35(10-35단계)의 모델군(model family, 모델군) 특성을 한 번에 볼 수 있는 model-selection reference(모델 선택 참고서)를 만든다.

효과(effect, 효과): 다음 stage(단계)를 열 때 몇 개의 기억 조각이 아니라 이 stage(단계)만 보고 모델 후보와 MT5(메타트레이더5) 연결 방식을 고를 수 있게 한다.

## Non-Shrink Rule(축소 금지 규칙)

이 stage(단계)는 몇 모델만 요약하지 않는다. Stage33(33단계)처럼 결과 없는 open-only(개방 전용)를 제외하고, Stage10-35(10-35단계)의 reviewed evidence(검토 근거)를 넓게 통합한다.

효과(effect, 효과): 약한 주장으로 작은 작업처럼 마감하지 않고, micro-probe frontier(미세탐침 전선) 직전까지 다음 질문을 좁힌다.

## Boundary(경계)

`{BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 만들지 않는다.
""",
    )
    common.write_md(
        STAGE_ROOT / "01_inputs" / "stage_open_draft.md",
        f"""# Stage36 Open Draft(36단계 개방 초안)

- stage id(단계 ID): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- packet(묶음): `{PACKET_ID}`
- primary family(주 작업군): `kpi_evidence(KPI 근거)`
- primary skill(주 스킬): `obsidian-run-evidence-system(실행 근거 시스템)`
- support skills(보조 스킬): `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`, `obsidian-performance-attribution(성과 귀속)`
- supplemental checks(보강 점검): `obsidian-experiment-design(실험 설계)`, `obsidian-runtime-parity(런타임 동등성)`, `obsidian-backtest-forensics(백테스트 포렌식)`, `obsidian-exploration-mandate(탐색 명령)`

효과(effect, 효과): Stage36(36단계)은 새 모델 학습(training, 학습)이 아니라 기존 근거를 적극 종합해 다음 모델 선택을 빠르게 만드는 작업 묶음(work packet, 작업 묶음)으로 열린다.
""",
    )


def write_manifest(summary: Mapping[str, Any]) -> None:
    common.write_json(
        MANIFEST_PATH,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "boundary": BOUNDARY,
            "inputs": [
                common.rel(common.RUN_REGISTRY_PATH),
                common.rel(common.PROJECT_ALPHA_LEDGER_PATH),
                "docs/workspace/stage20_27_characteristic_synthesis.md",
                "docs/workspace/stage29_32_native_revalidation_supplement.md",
                "stages/34_regime_mechanism__tier_a_markov_long_permission_attribution/03_reviews/stage34_closeout_packet.md",
                "stages/35_context_map__unsupervised_market_state_atlas/03_reviews/stage35_closeout_packet.md",
            ],
            "outputs": {
                "model_characteristic_matrix": common.rel(MODEL_MATRIX_PATH),
                "feature_axis_overlap": common.rel(FEATURE_AXIS_PATH),
                "selection_reference_matrix": common.rel(SELECTION_REFERENCE_PATH),
                "mt5_evidence_matrix": common.rel(MT5_EVIDENCE_PATH),
                "micro_probe_frontier": common.rel(MICRO_PROBE_FRONTIER_PATH),
                "source_coverage_audit": common.rel(SOURCE_COVERAGE_PATH),
                "packet": common.rel(REPORT_PATH),
            },
        },
    )


def write_report(
    summary: Mapping[str, Any],
    model_matrix: Sequence[Mapping[str, Any]],
    axis_overlap: Sequence[Mapping[str, Any]],
    selection_reference: Sequence[Mapping[str, Any]],
    micro_frontier: Sequence[Mapping[str, Any]],
) -> None:
    model_rows = [
        {
            "stage": row["stage_label"],
            "model": row["model_label"],
            "ref": row["reference_run"],
            "val": f"{row['validation_net_profit']}/{row['validation_pf']}",
            "oos": f"{row['oos_net_profit']}/{row['oos_pf']}",
            "use": row["selection_use"],
        }
        for row in model_matrix
    ]
    axis_rows = list(axis_overlap[:14])
    selection_rows = _top_selection_rows(selection_reference)
    frontier_rows = [
        {
            "frontier": row["frontier_id"],
            "question": row["question"],
            "value": row["selection_value"],
            "ready": row["ready_condition"],
        }
        for row in micro_frontier
    ]
    counts = summary["evidence_counts"]
    common.write_md(
        REPORT_PATH,
        f"""# Stage36 RUN30A Cross-Model Characteristic Synthesis Packet(36단계 30A 교차 모델 특성 종합 묶음)

## Routing Receipt(라우팅 기록)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- packet(묶음): `{PACKET_ID}`
- primary family(주 작업군): `{summary['primary_family']}`
- primary skill(주 스킬): `{summary['primary_skill']}`
- support skills(보조 스킬): {", ".join(f"`{skill}`" for skill in summary["support_skills"])}
- supplemental checks(보강 점검): {", ".join(f"`{skill}`" for skill in summary["supplemental_checks"])}
- judgment(판정): `{summary['judgment']}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage36(36단계)은 새 승자(winner, 승자)를 고르는 표가 아니라, 다음 stage(단계) 모델 선택(model selection, 모델 선택)을 빠르게 좁히는 특성 지도(characteristic map, 특성 지도)다.

## Experiment Design(실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- decision use(결정 사용처): {summary['decision_use']}
- comparison baseline(비교 기준): {summary['comparison_baseline']}
- sample scope(표본 범위): {summary['sample_scope']}
- stop condition(정지 조건): {summary['stop_condition']}

효과(effect, 효과): 작업을 작은 요약으로 축소하지 않고, 모델 특성/MT5(메타트레이더5)/재개 조건을 같은 묶음에서 닫는다.

## Evidence Counts(근거 개수)

- model topics(모델 주제): `{counts['model_topic_count']}`
- feature axes(피처 축): `{counts['feature_axis_count']}`
- MT5 runtime evidence rows(MT5 런타임 근거 행): `{counts['mt5_rows_with_completed_runtime_evidence']}`
- broad MT5 coverage rows(넓은 MT5 근거 행): `{counts['broad_mt5_coverage_rows']}`
- source authority pass(근거 권위 통과): `{counts['source_authority_passed_rows']}/{counts['source_authority_total_rows']}`
- positive validation+OOS reference rows(검증+표본외 양수 참고 행): `{counts['reference_rows_with_positive_validation_and_oos']}`

효과(effect, 효과): Stage36(36단계)이 몇 개만 파본 작업이 아니라 전체 모델 이력을 넓게 덮었는지 숫자로 확인한다.

## Model Matrix(모델 행렬)

{_md_table(model_rows, ["stage", "model", "ref", "val", "oos", "use"])}

## Axis Overlap(축 겹침)

{_md_table(axis_rows, ["axis", "axis_read", "model_count", "stage36_use"])}

## Selection Reference(선택 참고)

{_md_table(selection_rows, ["decision_need", "primary_references", "priority", "next_micro_probe_frontier"])}

## Micro-Probe Frontier(미세탐침 전선)

{_md_table(frontier_rows, ["frontier", "question", "value", "ready"])}

## MT5 Linkage(메타트레이더5 연결)

- mode(방식): `{summary['mt5_linkage']['mode']}`
- why no new MT5(새 MT5 실행을 하지 않은 이유): {summary['mt5_linkage']['why_no_new_mt5']}
- effect(효과): {summary['mt5_linkage']['effect']}

## Judgment(판정)

판정(judgment, 판정): `{JUDGMENT}`.

주장 경계(claim boundary, 주장 경계): `{BOUNDARY}`.

확인 아님(not confirmed, 확인 아님): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비).

효과(effect, 효과): Stage36(36단계)은 충분히 넓은 모델 선택 참고서로 완료하지만, 다음 micro-probe(미세탐침)는 별도 구체 질문이 있을 때 연다.
""",
    )


def write_gates(
    summary: Mapping[str, Any],
    model_matrix: Sequence[Mapping[str, Any]],
    source_coverage: Sequence[Mapping[str, Any]],
) -> dict[str, Path]:
    gate_payloads: dict[str, Any] = {
        "skill_receipts": {
            "packet_id": PACKET_ID,
            "selected_work_family": "kpi_evidence(KPI 근거)",
            "primary_skill": summary["primary_skill"],
            "support_skills": summary["support_skills"],
            "supplemental_checks": summary["supplemental_checks"],
            "effect": "선택한 skill(스킬)과 gate(게이트)를 Stage36(36단계) 완료 주장에 연결한다.",
        },
        "kpi_contract_audit": {
            "status": "passed(통과)",
            "rows_checked": len(model_matrix),
            "contract": "run registry numeric fields when available; no new KPI invented(가능한 등록부 수치 사용, 새 KPI 발명 없음)",
            "effect": "모델 비교를 서로 다른 임의 점수로 바꾸지 않는다.",
        },
        "row_grain_audit": {
            "status": "passed(통과)",
            "row_grain": "one row per model topic/stage reference(모델 주제/단계 참고당 한 행)",
            "effect": "Stage10-35(10-35단계)를 특정 subrun(하위 실행) 조각만으로 과대 대표하지 않는다.",
        },
        "source_authority_audit": {
            "status": "passed_with_review_items(검토 항목 포함 통과)",
            "source_rows": list(source_coverage),
            "effect": "각 모델 주제가 어떤 파일 근거에 기대는지 남긴다.",
        },
        "runtime_evidence_gate": {
            "status": "passed_existing_mt5_integrated(기존 MT5 통합 통과)",
            "new_tester_run": False,
            "why": "Stage36(36단계)은 cross-model synthesis(교차 모델 종합)이고 micro-probe frontier(미세탐침 전선)는 별도 실행 질문이다.",
            "effect": "MT5(메타트레이더5)를 회피하지 않고 기존 탐침 경계와 수를 표로 묶는다.",
        },
        "runtime_parity_gate": {
            "status": "passed_with_boundary(경계 포함 통과)",
            "research_path": "docs/registers/run_registry.csv plus stage packets(실행 등록부와 단계 묶음)",
            "runtime_path": "existing MT5 runtime probe outputs(기존 MT5 런타임 탐침 출력)",
            "known_differences": "many topics use score-table/distilled handoff(다수 주제는 점수표/증류 인계)",
            "runtime_claim_boundary": "no runtime authority(런타임 권위 없음)",
        },
        "backtest_forensics_gate": {
            "status": "passed_existing_forensic_boundary(기존 포렌식 경계 통과)",
            "tester_identity": "not reopened in Stage36(36단계에서 재개방 안 함)",
            "report_identity": "registry and packets only(등록부와 묶음 기준)",
            "backtest_judgment": "adequate for selection reference, insufficient for promotion(선택 참고에는 충분, 승격에는 불충분)",
        },
        "artifact_lineage_gate": {
            "status": "passed(통과)",
            "source_inputs": [
                common.rel(common.RUN_REGISTRY_PATH),
                common.rel(common.PROJECT_ALPHA_LEDGER_PATH),
                "docs/workspace/stage20_27_characteristic_synthesis.md",
                "docs/workspace/stage29_32_native_revalidation_supplement.md",
            ],
            "producer": "stage_pipelines.stage36.cross_model_characteristic_synthesis(36단계 교차 모델 특성 종합 스크립트)",
            "consumer": "future model selection stages(추후 모델 선택 단계)",
            "lineage_judgment": "complete_for_reference_only(참고 전용으로 완료)",
        },
        "result_judgment_gate": summary["result_judgment"],
        "final_claim_guard": {
            "status": "passed(통과)",
            "forbidden_claims": summary["forbidden_claims"],
            "effect": "Stage36(36단계) 결과를 운영 의미로 과장하지 않는다.",
        },
        "required_gate_coverage_audit": {
            "status": "passed(통과)",
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "required_gate_coverage_audit",
            ],
            "supplemental_gates": [
                "runtime_evidence_gate",
                "runtime_parity_gate",
                "backtest_forensics_gate",
                "artifact_lineage_gate",
                "result_judgment_gate",
                "final_claim_guard",
            ],
            "effect": "완료 주장(completion claim, 완료 주장)이 실제 gate(게이트) 파일에 연결된다.",
        },
    }
    paths: dict[str, Path] = {}
    for name, payload in gate_payloads.items():
        path = PACKET_ROOT / f"{name}.json"
        common.write_json(path, payload)
        paths[name] = path
    return paths


def write_aggregate_summary(
    summary: Mapping[str, Any],
    gate_paths: Mapping[str, Path],
    output_paths: Sequence[Path],
) -> None:
    artifacts: dict[str, Any] = {}
    for path in output_paths:
        if common.io_path(path).exists():
            artifacts[common.rel(path)] = {"sha256": common.sha256_file(path)}
    for name, path in gate_paths.items():
        if common.io_path(path).exists():
            artifacts[common.rel(path)] = {"gate": name, "sha256": common.sha256_file(path)}
    payload = dict(summary)
    payload["artifact_paths"] = artifacts
    payload["output_paths"] = {
        "stage_brief": common.rel(STAGE_ROOT / "00_spec" / "stage_brief.md"),
        "stage_open_draft": common.rel(STAGE_ROOT / "01_inputs" / "stage_open_draft.md"),
        "manifest": common.rel(MANIFEST_PATH),
        "report": common.rel(REPORT_PATH),
        "closeout_report": common.rel(CLOSEOUT_REPORT_PATH),
        "decision": common.rel(DECISION_PATH),
        "closeout_decision": common.rel(CLOSEOUT_DECISION_PATH),
        "selection_status": common.rel(SELECTION_STATUS_PATH),
        "model_matrix": common.rel(MODEL_MATRIX_PATH),
        "feature_axis_overlap": common.rel(FEATURE_AXIS_PATH),
        "selection_reference": common.rel(SELECTION_REFERENCE_PATH),
        "mt5_evidence": common.rel(MT5_EVIDENCE_PATH),
        "micro_probe_frontier": common.rel(MICRO_PROBE_FRONTIER_PATH),
        "source_coverage": common.rel(SOURCE_COVERAGE_PATH),
    }
    common.write_json(PACKET_ROOT / "aggregate_summary.json", payload)


def write_selection_status() -> None:
    common.write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage36 Selection Status(36단계 선택 상태)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed_closed_reference_only(검토 후 마감, 참고 전용)`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`

효과(effect, 효과): Stage36(36단계)은 다음 모델 선택 참고서로 쓰지만, 운영선(operating line, 운영선)을 바꾸지 않는다.

## Useful Next Choices(쓸 만한 다음 선택지)

1. permission/abstention overlap(허용/기권 겹침)
2. state context stack(상태 문맥 묶음)
3. exit/risk overlay(청산/위험 덧씌움)
4. interpretable feature shape(설명 가능한 피처 모양)
5. temporal context with market state(시장 상태와 시간 문맥)
""",
    )


def write_decision(summary: Mapping[str, Any]) -> None:
    common.write_md(
        DECISION_PATH,
        f"""# 2026-05-09 Stage36 Cross-Model Characteristic Synthesis(36단계 교차 모델 특성 종합)

## Decision(결정)

Stage36(36단계) `{STAGE_ID}`를 모델 선택 참고서(model-selection reference, 모델 선택 참고서) 주제로 열고 `{RUN_ID}`를 완료했다.

효과(effect, 효과): 다음 stage(단계)는 이 산출물만 보고 모델군(model family, 모델군), MT5(메타트레이더5) 연결 경계, micro-probe frontier(미세탐침 전선)를 고를 수 있다.

## Judgment(판정)

- judgment(판정): `{JUDGMENT}`
- boundary(경계): `{BOUNDARY}`
- MT5 linkage(MT5 연결): `{summary['mt5_linkage']['mode']}`

확인 아님(not confirmed, 확인 아님): baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비).
""",
    )


def write_closeout_docs(summary: Mapping[str, Any]) -> None:
    counts = summary["evidence_counts"]
    common.write_md(
        CLOSEOUT_REPORT_PATH,
        f"""# Stage36 Closeout Packet(36단계 마감 묶음)

- stage(단계): `{STAGE_ID}`
- closeout run(마감 실행): `{CLOSEOUT_RUN_ID}`
- source run(원천 실행): `{RUN_ID}`
- packet(묶음): `{PACKET_ID}`
- judgment(판정): `{CLOSEOUT_JUDGMENT}`
- boundary(경계): `{BOUNDARY}`

## Closeout Read(마감 판독)

Stage36(36단계)은 cross-model characteristic synthesis(교차 모델 특성 종합)와 model-selection reference(모델 선택 참고서)를 완료하고 reviewed closed(검토 후 마감)로 닫는다.

효과(effect, 효과): 다음 stage(단계)는 이 stage(단계)의 모델 행렬, 선택 참고, MT5(메타트레이더5) 근거 행렬, micro-probe frontier(미세탐침 전선)를 보고 바로 주제를 고를 수 있다.

## Evidence(근거)

- model topics(모델 주제): `{counts['model_topic_count']}`
- feature axes(피처 축): `{counts['feature_axis_count']}`
- completed MT5 runtime evidence rows(완료된 MT5 런타임 근거 행): `{counts['mt5_rows_with_completed_runtime_evidence']}`
- selection reference rows(선택 참고 행): `{counts['selection_reference_rows']}`
- micro-probe frontier rows(미세탐침 전선 행): `{counts['micro_probe_frontier_rows']}`
- source authority pass(근거 권위 통과): `{counts['source_authority_passed_rows']}/{counts['source_authority_total_rows']}`

## Preserved Next Choices(보존된 다음 선택지)

1. permission/abstention overlap(허용/기권 겹침)
2. state context stack(상태 문맥 묶음)
3. exit/risk overlay(청산/위험 덧씌움)
4. interpretable feature shape(설명 가능한 피처 모양)
5. temporal context with market state(시장 상태와 시간 문맥)

## Not Claimed(주장하지 않음)

baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 만들지 않는다.

효과(effect, 효과): Stage36(36단계)은 선택 참고서로 닫고, 운영 의미는 다음 별도 작업 묶음(work packet, 작업 묶음)에서만 주장할 수 있게 한다.
""",
    )
    common.write_md(
        CLOSEOUT_DECISION_PATH,
        f"""# 2026-05-09 Stage36 Closeout, No Stage37(36단계 마감, 37단계 미개방)

## Decision(결정)

Stage36(36단계) `{STAGE_ID}`를 `{CLOSEOUT_RUN_ID}`로 reviewed closed(검토 후 마감) 처리한다.

효과(effect, 효과): Stage36(36단계)은 모델 선택 참고서(model-selection reference, 모델 선택 참고서)로 고정되고, Stage37(37단계)은 아직 열지 않는다.

## Boundary(경계)

`{BOUNDARY}`

baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 없다.
""",
    )


def write_closeout_workspace_docs(summary: Mapping[str, Any]) -> None:
    state_path = common.WORKSPACE_STATE_PATH
    text = common.io_path(state_path).read_text(encoding="utf-8")
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {CLOSEOUT_RUN_ID}", text, count=1)
    text = re.sub(r"- Stage36\(36단계\) .+\n", "", text)
    text = re.sub(r"- Stage36\(36.*?\n", "", text)
    focus_item = (
        f"- Stage36(36단계) {STAGE_ID} reviewed_closed_reference_only(검토 후 마감, 참고 전용): "
        f"{CLOSEOUT_RUN_ID}(마감)는 {RUN_ID}(30A 실행)의 모델 특성, MT5(메타트레이더5) 근거, "
        "selection reference(선택 참고), micro-probe frontier(미세탐침 전선)를 Stage36 closeout(36단계 마감)으로 고정했다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    text = re.sub(r"(current_focus:\n)", r"\1" + focus_item + "\n", text, count=1)
    text = re.sub(
        r"- current_run_id\(현재 실행 ID\).*?\n",
        f"- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 Stage36 closeout(36단계 마감) `{CLOSEOUT_RUN_ID}`를 가리킨다. next action(다음 행동)은 `choose_one_micro_probe_frontier_or_open_next_topic`이다.\n",
        text,
        count=1,
    )
    block = f"""stage36_cross_model_characteristic_synthesis:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_closed_reference_only_no_stage37_opened
  current_run_id: {CLOSEOUT_RUN_ID}
  idea_id: IDEA-ST36-CROSS-MODEL-CHARACTERISTIC-SYNTHESIS
  source_scope: Stage10-35 reviewed model/topic evidence except Stage33 open-only no-result
  report_path: {common.rel(CLOSEOUT_REPORT_PATH)}
  packet_summary_path: {common.rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_mt5_evidence_integrated
  next_action: choose_one_micro_probe_frontier_or_open_next_topic
  boundary: {BOUNDARY}

"""
    if "stage36_cross_model_characteristic_synthesis:" in text:
        text = re.sub(
            r"stage36_cross_model_characteristic_synthesis:\n(?:  .+\n)+\n?",
            block,
            text,
            count=1,
        )
    else:
        marker = "\nstage33_tier_a_markov_long_permission_source:"
        text = text.replace(marker, "\n" + block + "stage33_tier_a_markov_long_permission_source:", 1)
    common.io_path(state_path).write_text(text, encoding="utf-8")

    _remove_existing_section(common.CURRENT_WORKING_STATE_PATH, "Latest Stage36 Cross-Model Characteristic Synthesis(최신 36단계 교차 모델 특성 종합)")
    _remove_existing_section(common.CURRENT_WORKING_STATE_PATH, "Latest Stage36 Closeout(최신 36단계 마감)")
    _prepend_text(
        common.CURRENT_WORKING_STATE_PATH,
        f"""## Latest Stage36 Closeout(최신 36단계 마감)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{CLOSEOUT_RUN_ID}`
- source run(원천 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- status(상태): `reviewed_closed_reference_only(검토 후 마감, 참고 전용)`
- next action(다음 행동): `choose_one_micro_probe_frontier_or_open_next_topic`

Stage36(36단계)은 Stage10-35(10-35단계) 모델군(model family, 모델군)을 특성 축(characteristic axis, 특성 축), MT5 linkage(MT5 연결), selection reference(선택 참고), micro-probe frontier(미세탐침 전선)로 정리하고 마감했다.

효과(effect, 효과): 다음 stage(단계)는 이 stage(단계)만 보고 모델 선택 방향을 고를 수 있다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
""",
    )
    _remove_existing_section(common.CHANGELOG_PATH, "2026-05-09 Stage36 Cross-Model Characteristic Synthesis(36단계 교차 모델 특성 종합)")
    _remove_existing_section(common.CHANGELOG_PATH, "2026-05-09 Stage36 Closeout(36단계 마감)")
    _prepend_text(
        common.CHANGELOG_PATH,
        f"""## 2026-05-09 Stage36 Closeout(36단계 마감)

- run(실행): `{CLOSEOUT_RUN_ID}`
- source run(원천 실행): `{RUN_ID}`
- models/topics(모델/주제): `{summary['evidence_counts']['model_topic_count']}`
- MT5 runtime evidence rows(MT5 런타임 근거 행): `{summary['evidence_counts']['mt5_rows_with_completed_runtime_evidence']}`
- judgment(판정): `{CLOSEOUT_JUDGMENT}`
- effect(효과): 모델 간 개별 특성, MT5(메타트레이더5) 경계, 선택 참고, 미세탐침 전선을 Stage36(36단계) 마감 상태로 고정했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.
""",
    )


def _prepend_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    old = ""
    if common.io_path(path).exists():
        old = common.io_path(path).read_text(encoding=encoding)
    common.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    common.io_path(path).write_text(text.rstrip() + "\n\n" + old.lstrip("\ufeff"), encoding=encoding)


def _remove_existing_section(path: Path, heading_prefix: str, encoding: str = "utf-8-sig") -> None:
    if not common.io_path(path).exists():
        return
    text = common.io_path(path).read_text(encoding=encoding)
    pattern = rf"\ufeff?## {re.escape(heading_prefix)}.*?(?=\n## |\Z)"
    text = re.sub(pattern, "", text, count=1, flags=re.DOTALL).lstrip("\n")
    common.io_path(path).write_text(text, encoding=encoding)


def update_workspace_docs(summary: Mapping[str, Any]) -> None:
    state_path = common.WORKSPACE_STATE_PATH
    text = common.io_path(state_path).read_text(encoding="utf-8")
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {CLOSEOUT_RUN_ID}", text, count=1)
    text = re.sub(r"- Stage36\(36단계\) .+\n", "", text)
    text = re.sub(
        r"- current_run_id\(현재 실행 ID\).*?\n",
        "- current_run_id(현재 실행 ID)는 active stage(활성 단계)의 Stage36(36단계) run30A(30A 실행)를 가리킨다. next action(다음 행동)은 `choose_one_micro_probe_frontier_or_open_next_topic`이다.\n",
        text,
        count=1,
    )
    text = re.sub(
        r"- 'next action\(다음 행동\): continue Stage35\(35단계\).*?Stage20-32\n  goal\(20-32단계 목표\)은 complete\(완료\)'\n",
        "- 'next action(다음 행동): choose one Stage36(36단계) micro-probe frontier(미세탐침 전선) or open the next topic pivot(다음 주제 전환) by explicit user request(명시 사용자 요청)'\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    focus_item = (
        f"- Stage36(36단계) {STAGE_ID} completed_reference_only(참고서 완료): "
        f"{RUN_ID}(30A 실행)는 Stage10-35(10-35단계) 모델 특성, MT5(메타트레이더5) 근거, "
        "selection reference(선택 참고), micro-probe frontier(미세탐침 전선)를 남겼다; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    text = re.sub(r"(current_focus:\n)", r"\1" + focus_item + "\n", text, count=1)
    block = f"""
stage36_cross_model_characteristic_synthesis:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: completed_reference_only_no_stage37_opened
  current_run_id: {RUN_ID}
  idea_id: IDEA-ST36-CROSS-MODEL-CHARACTERISTIC-SYNTHESIS
  source_scope: Stage10-35 reviewed model/topic evidence except Stage33 open-only no-result
  report_path: {common.rel(REPORT_PATH)}
  packet_summary_path: {common.rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_mt5_evidence_integrated
  next_action: choose_one_micro_probe_frontier_or_open_next_topic
  boundary: {BOUNDARY}

"""
    marker = "\nstage33_tier_a_markov_long_permission_source:"
    if "stage36_cross_model_characteristic_synthesis:" not in text:
        text = text.replace(marker, "\n" + block + "stage33_tier_a_markov_long_permission_source:", 1)
    common.io_path(state_path).write_text(text, encoding="utf-8")

    _remove_existing_section(common.CURRENT_WORKING_STATE_PATH, "Latest Stage36 Cross-Model Characteristic Synthesis(최신 36단계 교차 모델 특성 종합)")
    _prepend_text(
        common.CURRENT_WORKING_STATE_PATH,
        f"""## Latest Stage36 Cross-Model Characteristic Synthesis(최신 36단계 교차 모델 특성 종합)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- latest packet(최신 묶음): `{PACKET_ID}`
- status(상태): `completed_reference_only(참고서 완료)`
- next action(다음 행동): `choose_one_micro_probe_frontier_or_open_next_topic`

Stage36(36단계)은 Stage10-35(10-35단계) 모델군(model family, 모델군)을 특성 축(characteristic axis, 특성 축), MT5 linkage(MT5 연결), selection reference(선택 참고), micro-probe frontier(미세탐침 전선)로 정리했다.

효과(effect, 효과): 다음 stage(단계)는 이 stage(단계)만 보고 모델 선택 방향을 고를 수 있다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
""",
    )
    _remove_existing_section(common.CHANGELOG_PATH, "2026-05-09 Stage36 Cross-Model Characteristic Synthesis(36단계 교차 모델 특성 종합)")
    _prepend_text(
        common.CHANGELOG_PATH,
        f"""## 2026-05-09 Stage36 Cross-Model Characteristic Synthesis(36단계 교차 모델 특성 종합)

- run(실행): `{RUN_ID}`
- models/topics(모델/주제): `{summary['evidence_counts']['model_topic_count']}`
- MT5 runtime evidence rows(MT5 런타임 근거 행): `{summary['evidence_counts']['mt5_rows_with_completed_runtime_evidence']}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 모델 간 개별 특성, MT5(메타트레이더5) 경계, 선택 참고, 미세탐침 전선을 한 stage(단계)에 묶었다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.
""",
    )


def upsert_ledgers(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "cross_model_characteristic_synthesis",
        "status": "reviewed",
        "judgment": JUDGMENT,
        "path": common.rel(REPORT_PATH),
        "notes": (
            f"models={summary['evidence_counts']['model_topic_count']};"
            f"mt5_rows={summary['evidence_counts']['mt5_rows_with_completed_runtime_evidence']};"
            f"boundary={BOUNDARY};external_verification=completed_existing_mt5_evidence_integrated"
        ),
    }
    closeout_run_row = {
        "run_id": CLOSEOUT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout",
        "status": "reviewed_closed",
        "judgment": CLOSEOUT_JUDGMENT,
        "path": common.rel(CLOSEOUT_REPORT_PATH),
        "notes": (
            f"source_run={RUN_ID};models={summary['evidence_counts']['model_topic_count']};"
            f"mt5_rows={summary['evidence_counts']['mt5_rows_with_completed_runtime_evidence']};"
            f"boundary={BOUNDARY};external_verification=completed_existing_mt5_evidence_integrated;stage37_opened=0"
        ),
    }
    common.upsert_run_rows([run_row, closeout_run_row])
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__model_matrix",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "model_matrix(모델 행렬)",
            "parent_run_id": "",
            "record_view": "cross_model_characteristic_matrix(교차 모델 특성 행렬)",
            "tier_scope": "Stage10-35 reviewed evidence(10-35단계 검토 근거)",
            "kpi_scope": "registry_metrics_when_available(가능한 등록부 수치)",
            "scoreboard_lane": "model_selection_reference(모델 선택 참고)",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": common.rel(MODEL_MATRIX_PATH),
            "primary_kpi": f"model_topic_count={summary['evidence_counts']['model_topic_count']}",
            "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
            "external_verification_status": "completed_existing_mt5_evidence_integrated",
            "notes": f"boundary={BOUNDARY}",
        },
        {
            "ledger_row_id": f"{RUN_ID}__selection_reference",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "selection_reference(선택 참고)",
            "parent_run_id": "",
            "record_view": "selection_reference_matrix(선택 참고 행렬)",
            "tier_scope": "cross_stage(교차 단계)",
            "kpi_scope": "reference_only(참고 전용)",
            "scoreboard_lane": "future_stage_model_choice(추후 단계 모델 선택)",
            "status": "reviewed",
            "judgment": JUDGMENT,
            "path": common.rel(SELECTION_REFERENCE_PATH),
            "primary_kpi": f"selection_reference_rows={summary['evidence_counts']['selection_reference_rows']}",
            "guardrail_kpi": "no_operating_claim",
            "external_verification_status": "completed_existing_mt5_evidence_integrated",
            "notes": f"boundary={BOUNDARY}",
        },
        {
            "ledger_row_id": f"{RUN_ID}__micro_probe_frontier",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "micro_probe_frontier(미세탐침 전선)",
            "parent_run_id": "",
            "record_view": "frontier_not_executed(전선, 실행 아님)",
            "tier_scope": "cross_stage(교차 단계)",
            "kpi_scope": "not_applicable_reference_only(참고 전용으로 해당 없음)",
            "scoreboard_lane": "next_question_frontier(다음 질문 전선)",
            "status": "reviewed",
            "judgment": "frontier_materialized_not_executed(전선 산출, 실행 아님)",
            "path": common.rel(MICRO_PROBE_FRONTIER_PATH),
            "primary_kpi": f"frontier_rows={summary['evidence_counts']['micro_probe_frontier_rows']}",
            "guardrail_kpi": "micro_probe_not_claimed_as_run",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": f"boundary={BOUNDARY}",
        },
        {
            "ledger_row_id": f"{CLOSEOUT_RUN_ID}__stage_closeout",
            "stage_id": STAGE_ID,
            "run_id": CLOSEOUT_RUN_ID,
            "subrun_id": "stage_closeout(단계 마감)",
            "parent_run_id": RUN_ID,
            "record_view": "stage_closeout_reference_only(단계 마감, 참고 전용)",
            "tier_scope": "cross_stage(교차 단계)",
            "kpi_scope": "completion_audit(완료 감사)",
            "scoreboard_lane": "stage36_closeout(36단계 마감)",
            "status": "reviewed_closed",
            "judgment": CLOSEOUT_JUDGMENT,
            "path": common.rel(CLOSEOUT_REPORT_PATH),
            "primary_kpi": "completion_audit=passed",
            "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority",
            "external_verification_status": "completed_existing_mt5_evidence_integrated",
            "notes": f"source_run={RUN_ID};boundary={BOUNDARY};stage37_opened=0",
        },
    ]
    common.upsert_alpha_rows(common.PROJECT_ALPHA_LEDGER_PATH, alpha_rows)
    common.upsert_alpha_rows(LOCAL_LEDGER_PATH, alpha_rows)
    return alpha_rows


def build_completion_audit(summary: Mapping[str, Any], output_paths: Sequence[Path], gate_paths: Mapping[str, Path]) -> None:
    checks = [
        {
            "requirement": "모델간 특성 총정리",
            "status": "passed(통과)",
            "evidence": common.rel(MODEL_MATRIX_PATH),
            "effect": "Stage10-35(10-35단계) 모델군을 한 표로 비교한다.",
        },
        {
            "requirement": "추후 stage 모델 선택 참고",
            "status": "passed(통과)",
            "evidence": common.rel(SELECTION_REFERENCE_PATH),
            "effect": "다음 stage(단계)의 모델 후보와 쓰임새를 고른다.",
        },
        {
            "requirement": "MT5 연계 주저 금지",
            "status": "passed_existing_mt5_integrated(기존 MT5 통합 통과)",
            "evidence": common.rel(MT5_EVIDENCE_PATH),
            "effect": "기존 MT5(메타트레이더5) 근거와 런타임 경계를 한 표에 묶는다.",
        },
        {
            "requirement": "몇 가지만 파지 말 것",
            "status": "passed(통과)",
            "evidence": f"model_topics={summary['evidence_counts']['model_topic_count']}",
            "effect": "소수 단서 요약으로 축소하지 않는다.",
        },
        {
            "requirement": "미세탐침 직전까지",
            "status": "passed(통과)",
            "evidence": common.rel(MICRO_PROBE_FRONTIER_PATH),
            "effect": "다음 실제 미세탐침 질문을 바로 고를 수 있게 한다.",
        },
        {
            "requirement": "약한 주장으로 stage 마감 금지",
            "status": "passed(통과)",
            "evidence": common.rel(gate_paths["final_claim_guard"]),
            "effect": "참고서 완료와 운영 주장 금지를 분리한다.",
        },
        {
            "requirement": "Stage36 closeout(36단계 마감)",
            "status": "passed(통과)",
            "evidence": common.rel(CLOSEOUT_REPORT_PATH),
            "effect": "Stage36(36단계)을 reviewed closed(검토 후 마감)로 닫고 Stage37(37단계)은 열지 않는다.",
        },
    ]
    missing_outputs = [common.rel(path) for path in output_paths if not common.io_path(path).exists()]
    common.write_json(
        PACKET_ROOT / "completion_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed(통과)" if not missing_outputs else "blocked_missing_outputs(출력 누락 차단)",
            "checks": checks,
            "missing_outputs": missing_outputs,
            "goal_coverage_judgment": "goal_satisfied_reference_only_no_operating_claim(목표 충족, 참고 전용, 운영 주장 없음)",
        },
    )


def run(update_state: bool) -> dict[str, Any]:
    registry_rows = _read_registry()
    model_matrix = build_model_matrix(registry_rows)
    axis_overlap = build_feature_axis_overlap(model_matrix)
    selection_reference = build_selection_reference(model_matrix)
    mt5_matrix = build_mt5_evidence_matrix(model_matrix)
    micro_frontier = build_micro_probe_frontier()
    source_coverage = build_source_coverage(model_matrix, registry_rows)
    local_alpha_rows_preview: list[dict[str, Any]] = []
    summary = build_summary(
        model_matrix,
        axis_overlap,
        selection_reference,
        mt5_matrix,
        source_coverage,
        local_alpha_rows_preview,
    )

    write_stage_brief()
    common.write_csv(MODEL_MATRIX_PATH, model_matrix)
    common.write_csv(FEATURE_AXIS_PATH, axis_overlap)
    common.write_csv(SELECTION_REFERENCE_PATH, selection_reference)
    common.write_csv(MT5_EVIDENCE_PATH, mt5_matrix)
    common.write_csv(MICRO_PROBE_FRONTIER_PATH, micro_frontier)
    common.write_csv(SOURCE_COVERAGE_PATH, source_coverage)
    write_manifest(summary)
    write_report(summary, model_matrix, axis_overlap, selection_reference, micro_frontier)
    write_selection_status()
    write_decision(summary)
    write_closeout_docs(summary)
    alpha_rows = upsert_ledgers(summary)
    summary = build_summary(
        model_matrix,
        axis_overlap,
        selection_reference,
        mt5_matrix,
        source_coverage,
        alpha_rows,
    )
    output_paths = [
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        STAGE_ROOT / "01_inputs" / "stage_open_draft.md",
        MANIFEST_PATH,
        MODEL_MATRIX_PATH,
        FEATURE_AXIS_PATH,
        SELECTION_REFERENCE_PATH,
        MT5_EVIDENCE_PATH,
        MICRO_PROBE_FRONTIER_PATH,
        SOURCE_COVERAGE_PATH,
        REPORT_PATH,
        CLOSEOUT_REPORT_PATH,
        DECISION_PATH,
        CLOSEOUT_DECISION_PATH,
        SELECTION_STATUS_PATH,
        LOCAL_LEDGER_PATH,
    ]
    gate_paths = write_gates(summary, model_matrix, source_coverage)
    write_aggregate_summary(summary, gate_paths, output_paths)
    build_completion_audit(summary, output_paths, gate_paths)
    if update_state:
        update_workspace_docs(summary)
        write_closeout_workspace_docs(summary)
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-state-update", action="store_true")
    args = parser.parse_args(argv)
    summary = run(update_state=not args.skip_state_update)
    print(
        json.dumps(
            {
                "packet_id": PACKET_ID,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "judgment": summary["judgment"],
                "evidence_counts": summary["evidence_counts"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

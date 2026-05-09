# Stage36 RUN30A Cross-Model Characteristic Synthesis Packet(36단계 30A 교차 모델 특성 종합 묶음)

## Routing Receipt(라우팅 기록)

- stage(단계): `36_model_selection__cross_model_characteristic_synthesis`
- run(실행): `run30A_cross_model_characteristic_synthesis_v1`
- packet(묶음): `stage36_run30A_cross_model_characteristic_synthesis_v1`
- primary family(주 작업군): `kpi_evidence(KPI 근거)`
- primary skill(주 스킬): `obsidian-run-evidence-system(실행 근거 시스템)`
- support skills(보조 스킬): `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`, `obsidian-performance-attribution(성과 귀속)`
- supplemental checks(보강 점검): `obsidian-experiment-design(실험 설계)`, `obsidian-runtime-parity(런타임 동등성)`, `obsidian-backtest-forensics(백테스트 포렌식)`, `obsidian-exploration-mandate(탐색 명령)`
- judgment(판정): `reviewed_completed_cross_model_characteristic_synthesis_reference_only`
- boundary(경계): `stage36_model_selection_reference_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage36(36단계)은 새 승자(winner, 승자)를 고르는 표가 아니라, 다음 stage(단계) 모델 선택(model selection, 모델 선택)을 빠르게 좁히는 특성 지도(characteristic map, 특성 지도)다.

## Experiment Design(실험 설계)

- hypothesis(가설): Stage10-35(10-35단계) 모델군은 성능 순위보다 characteristic axis(특성 축), MT5 runtime boundary(MT5 런타임 경계), reopen condition(재개 조건)으로 분류할 때 다음 모델 선택에 더 유용하다.
- decision use(결정 사용처): Future stages(추후 단계)에서 모델을 고를 때 이 stage(단계)만 보고 permission/filter/state/exit/sequence/interpretable/tree axes(허용/필터/상태/청산/순서/설명가능/트리 축)를 고르게 한다.
- comparison baseline(비교 기준): Existing Stage10-35 reviewed registry rows and packets(기존 10-35단계 검토 등록부 행과 묶음)
- sample scope(표본 범위): Stage10-35 reviewed model/topic stages except Stage33 open-only no-result(33단계 결과 없는 개방 전용 제외)
- stop condition(정지 조건): Run30A(30A 실행) stops only after matrix, reference, frontier, gates, ledgers, and state docs exist.

효과(effect, 효과): 작업을 작은 요약으로 축소하지 않고, 모델 특성/MT5(메타트레이더5)/재개 조건을 같은 묶음에서 닫는다.

## Evidence Counts(근거 개수)

- model topics(모델 주제): `25`
- feature axes(피처 축): `88`
- MT5 runtime evidence rows(MT5 런타임 근거 행): `24`
- broad MT5 coverage rows(넓은 MT5 근거 행): `7`
- source authority pass(근거 권위 통과): `25/25`
- positive validation+OOS reference rows(검증+표본외 양수 참고 행): `10`

효과(effect, 효과): Stage36(36단계)이 몇 개만 파본 작업이 아니라 전체 모델 이력을 넓게 덮었는지 숫자로 확인한다.

## Model Matrix(모델 행렬)

| stage | model | ref | val | oos | use |
| --- | --- | --- | --- | --- | --- |
| Stage10(10단계) | LogReg threshold scout(로지스틱 회귀 임계값 탐색) | run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1 | 318.48/3.88 | 313.14/3.99 | 새 모델의 기대치를 잡는 낮은 복잡도 기준점(reference point, 참고점)으로 쓴다. |
| Stage11(11단계) | LightGBM horizon/WFO scout(라이트GBM 수평선/워크포워드 탐색) | run02AA_lgbm_fwd18_inverse_rank_context_adx20_routed_v1 | 480.75/446.14 | 31.62/2.8 | 시계열 분할과 라벨 길이가 모델 판단을 얼마나 흔드는지 보는 압박축으로 쓴다. |
| Stage12(12단계) | ExtraTrees(엑스트라트리) | run03C_et_standalone_mt5_runtime_probe_v1 | -13.18/0.98 | 249.57/1.69 | 깊은 트리 계열이 잡는 비선형 후보축을 빠르게 확인할 때 쓴다. |
| Stage13(13단계) | MLP(다층 퍼셉트론) | run04N_mlp_feature_group_interaction_profit_probe_v1 | / | 172.22/1.21 | 특징 조합(feature interaction, 피처 상호작용)이 선형/트리와 다르게 접히는지 볼 때 쓴다. |
| Stage14(14단계) | SVM margin/kernel(서포트 벡터 머신 마진/커널) | run05A_svm_margin_kernel_characteristic_runtime_probe_v1 | -497.55/0.62 | 61.47/1.05 | 경계면(boundary surface, 경계면)이 얇은지 확인하는 대조군으로 쓴다. |
| Stage15(15단계) | LDA covariance scout(선형 판별 분석 공분산 탐색) | run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1 | 60.26/1.03 | 33.61/1.03 | 저차원 선형 판별이 트리/부스팅과 다른 안정축을 주는지 확인한다. |
| Stage16(16단계) | QDA class covariance(이차 판별 분석 계급 공분산) | run10I_qda_reg020_drop_mega10_decision_microprobe_v1 | 140.92/1.14 | 219.31/1.4 | 비선형 계급 경계가 OOS(표본외)에서 살아남는지 보는 압박축으로 쓴다. |
| Stage17(17단계) | XGBoost/DART(엑스지부스트/다트) | run11A_xgb_regularized_boosting_characteristic_scout_v1 | -250.95/0.74 | 222/1.58 | CatBoost/EBM(캣부스트/설명가능 부스팅 머신)과 트리 부스팅 모양을 대조한다. |
| Stage18(18단계) | CatBoost ordered boosting(캣부스트 순서 부스팅) | run12A_catboost_ordered_boosting_characteristic_scout_v1 | 206.56/1.27 | 203.52/1.49 | 트리 부스팅 중 regime/session(국면/세션) 분해가 필요할 때 우선 참고한다. |
| Stage19(19단계) | EBM(설명가능 부스팅 머신) | run13AE_ebm_q90_hold4_mixed_subtype_direction_probe_v1 | 188.31/1.22 | 80.89/1.16 | 왜 모델이 반응하는지 설명 가능한 축이 필요할 때 최우선 참고한다. |
| Stage20(20단계) | GAM(일반화 가산 모델) | run14B_gam_runtime_handoff_probe_v1 | 8.65/1.01 | 295.69/1.51 | EBM(설명가능 부스팅 머신)보다 부드러운 단조/곡선 반응 확인에 쓴다. |
| Stage21(21단계) | ElasticNet Logistic(엘라스틱넷 로지스틱) | run15B_elasticnet_logistic_onnx_runtime_probe_v1 | -113.11/0.9 | -49.77/0.94 | 복잡한 모델의 축이 단순 선형에도 보이는지 확인하는 sanity check(정상성 점검)로 쓴다. |
| Stage22(22단계) | HMM(은닉 마르코프 모델) | run16B_hmm_state_runtime_probe_v1 | -497.25/0.69 | 121.96/1.05 | 상태(context state, 문맥 상태)를 먼저 나누고 다른 모델을 얹을 때 쓴다. |
| Stage23(23단계) | Supervised regime classifier(지도 국면 분류기) | run17B_supervised_regime_classifier_runtime_probe_v1 | 324.75/1.16 | 254.63/1.19 | 모델 선택에서 permission filter(허용 필터)가 필요하면 1순위 참고축이다. |
| Stage24(24단계) | Survival model(생존 모델) | run18B_survival_time_to_event_runtime_probe_v1 | -157.74/0.9 | -98.54/0.88 | 진입 모델이 아니라 청산/보유 위험 overlay(덧씌움)로 쓴다. |
| Stage25(25단계) | Hazard model(위험률 모델) | run19B_hazard_trade_lifecycle_runtime_probe_v1 | -89.59/0.94 | -174.49/0.83 | 손실 회피/평탄화(flat pressure, 평탄 압력) 보조층으로 쓴다. |
| Stage26(26단계) | NGBoost(자연 그래디언트 부스팅) | run20B_ngboost_distribution_runtime_probe_v1 | -17.21/0.05 | 39.49/2.37 | 확신도(confidence, 확신도)와 불확실성 기권을 만들 때 참고한다. |
| Stage27(27단계) | Quantile boosting(분위수 부스팅) | run21B_quantile_boosting_tail_risk_runtime_probe_v1 | -38.20/0.97 | 79.17/1.07 | 위험 상단/하단 꼬리를 분리하는 보조 표면으로 쓴다. |
| Stage28(28단계) | Markov regression(마르코프 회귀) | run22B_markov_regression_state_runtime_probe_v1 | 244.08/1.77 | 111.27/1.31 | 상태 전환(state transition, 상태 전환)과 허용 필터를 나눌 때 쓴다. |
| Stage29(29단계) | River online ML(리버 온라인 머신러닝) | run23D_river_native_online_runtime_probe_v1 | -115.71/0.93 | -202.2/0.83 | 고정 학습 모델이 시간 변화에 무너지는지 보는 대조축으로 쓴다. |
| Stage30(30단계) | Calibration/abstention(보정/기권) | run24D_native_source_calibration_runtime_probe_v1 | 44.19/1.27 | -1.32/0.69 | 새 모델의 raw probability(원시 확률)를 바로 쓰기 전 필수 의사결정층으로 본다. |
| Stage31(31단계) | TabNet(탭넷) | run25D_tabnet_native_attentive_runtime_probe_v1 | -498.33/0.6 | -4.32/1 | 피처 선택(feature selection, 피처 선택)이 학습 내부에서 어떻게 드러나는지 볼 때 참고한다. |
| Stage32(32단계) | TCN(시간 합성곱 네트워크) | run26D_torch_tcn_native_temporal_runtime_probe_v1 | 75.26/1.04 | 111.77/1.07 | M5(5분봉) 문맥 순서가 중요할 때 deep sequence(심층 순서) 후보로 참고한다. |
| Stage34(34단계) | Markov long permission attribution(마르코프 매수 허용 귀속) | stage34_tier_a_markov_long_permission_attribution_closeout_v1 | / | / | 상태 필터를 다시 쓸 때 의존축과 보유시간 경고를 함께 본다. |
| Stage35(35단계) | KMeans state atlas(K-평균 상태 지도) | stage35_context_map_closeout_v1 | / | / | 모델 선택 전에 시장 문맥을 나눠 후보를 배치할 때 참고한다. |

## Axis Overlap(축 겹침)

| axis | axis_read | model_count | stage36_use |
| --- | --- | --- | --- |
| session_timing | core_cross_model_axis(핵심 교차 모델 축) | 5 | 시장 문맥(context, 문맥) 층화와 MT5(메타트레이더5) 재탐침 우선축 |
| threshold | core_cross_model_axis(핵심 교차 모델 축) | 4 | 여러 모델에 반복되어 다음 stage(단계) 모델 선택 참고축 |
| direction_asymmetry | repeated_axis(반복 축) | 3 | 여러 모델에 반복되어 다음 stage(단계) 모델 선택 참고축 |
| calibration | repeated_axis(반복 축) | 2 | 모델 선택 후 decision layer(결정층) 후보축 |
| close_ema20_ratio | repeated_axis(반복 축) | 2 | 단일 모델 특성으로 보존 |
| historical_vol_20 | repeated_axis(반복 축) | 2 | 시장 문맥(context, 문맥) 층화와 MT5(메타트레이더5) 재탐침 우선축 |
| hl_range | repeated_axis(반복 축) | 2 | 단일 모델 특성으로 보존 |
| hold_length | repeated_axis(반복 축) | 2 | 청산/보유 관리(exit/hold management, 청산/보유 관리) 후보축 |
| long_permission | repeated_axis(반복 축) | 2 | 단일 모델 특성으로 보존 |
| markov_state | repeated_axis(반복 축) | 2 | 상태 필터(state filter, 상태 필터) 후보축 |
| permission_filter | repeated_axis(반복 축) | 2 | 모델 선택 후 decision layer(결정층) 후보축 |
| tier_b_fallback | repeated_axis(반복 축) | 2 | 단일 모델 특성으로 보존 |
| volatility | repeated_axis(반복 축) | 2 | 시장 문맥(context, 문맥) 층화와 MT5(메타트레이더5) 재탐침 우선축 |
| abstention | single_model_axis(단일 모델 축) | 1 | 모델 선택 후 decision layer(결정층) 후보축 |

## Selection Reference(선택 참고)

| decision_need | primary_references | priority | next_micro_probe_frontier |
| --- | --- | --- | --- |
| permission_filter(허용 필터) | Stage19(19단계)/Stage23(23단계)/Stage30(30단계) | high(높음) | p_flat + calibrated margin + EBM direction(평탄 확률+보정 마진+EBM 방향) 겹침 직전까지 비교 |
| state_context_filter(상태 문맥 필터) | Stage22(22단계)/Stage28(28단계)/Stage34(34단계)/Stage35(35단계) | high(높음) | Markov long permission + KMeans return-volatility state + HMM noncollapsed state(비붕괴 상태) 교차 |
| exit_risk_overlay(청산 위험 덧씌움) | Stage24(24단계)/Stage25(25단계)/Stage27(27단계) | medium_high(중상) | position-age hazard + survival clock + quantile tail(포지션 나이 위험률+생존 시계+분위수 꼬리) |
| interpretable_shape(설명 가능한 모양) | Stage19(19단계)/Stage20(20단계)/Stage21(21단계) | medium_high(중상) | EBM main effect + GAM smooth curve + ElasticNet sign(주효과+부드러운 곡선+선형 부호) |
| sequence_or_drift(순서 또는 변화) | Stage29(29단계)/Stage32(32단계) | medium(중간) | TCN temporal context + Stage35 market state(시간 문맥+시장 상태) 결합 |
| tree_boosting_contrast(트리 부스팅 대조) | Stage17(17단계)/Stage18(18단계) | medium(중간) | CatBoost session-volatility split vs DART direction asymmetry(세션/변동성 분리 대 방향 비대칭) |
| attention_feature_selection(주의집중 피처 선택) | Stage31(31단계) | low(낮음) | 다른 모델의 반복 피처축을 TabNet mask(탭넷 마스크)와 맞춰보는 수준 |

## Micro-Probe Frontier(미세탐침 전선)

| frontier | question | value | ready |
| --- | --- | --- | --- |
| frontier01_permission_abstention_overlap | 어떤 모델 조합이 진입 허용(permission, 허용)과 기권(abstention, 기권)을 가장 덜 얇게 만드는가? | very_high(매우 높음) | p_flat/margin/entropy/tail pressure(평탄 확률/마진/엔트로피/꼬리 압력) 공통 테이블을 만들 수 있을 때 |
| frontier02_state_context_stack | 상태 모델(state model, 상태 모델)을 먼저 자르면 어떤 모델군을 어디에 배치해야 하는가? | very_high(매우 높음) | 동일 feature-ready timestamp(피처 준비 시각) 기준 상태 열을 동시에 만들 수 있을 때 |
| frontier03_exit_risk_non_entry_overlay | 청산/보유 위험 모델을 진입 신호 없이 덧씌우면 손실폭을 줄이는가? | high(높음) | EA(전문가 자문)에서 포지션 경과 봉과 위험 표면을 동시에 읽을 수 있을 때 |
| frontier04_interpretable_feature_shape | 반복 피처축을 설명 가능한 모델이 같은 방향으로 읽는가? | high(높음) | feature axis dictionary(피처 축 사전)를 고정하고 같은 컷으로 재집계할 때 |
| frontier05_temporal_context_with_market_state | 순서 모델(sequence model, 순서 모델)은 시장 상태(state, 상태)별로 어디서만 의미가 있는가? | medium_high(중상) | TCN score(점수)와 Stage35 state id(상태 ID)를 같은 runtime table(런타임 테이블)에 붙일 때 |

## MT5 Linkage(메타트레이더5 연결)

- mode(방식): `existing_mt5_runtime_evidence_integrated_no_new_tester_run(기존 MT5 런타임 근거 통합, 새 테스터 실행 없음)`
- why no new MT5(새 MT5 실행을 하지 않은 이유): Stage36(36단계)는 모델 선택 참고서 산출이 목적이고, 새 조합 실행은 micro-probe frontier(미세탐침 전선)로 분리했다.
- effect(효과): MT5(메타트레이더5) 연계를 피하지 않고 기존 탐침 수와 경계를 한 표에 모았지만 운영 권위는 만들지 않는다.

## Judgment(판정)

판정(judgment, 판정): `reviewed_completed_cross_model_characteristic_synthesis_reference_only`.

주장 경계(claim boundary, 주장 경계): `stage36_model_selection_reference_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`.

확인 아님(not confirmed, 확인 아님): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비).

효과(effect, 효과): Stage36(36단계)은 충분히 넓은 모델 선택 참고서로 완료하지만, 다음 micro-probe(미세탐침)는 별도 구체 질문이 있을 때 연다.

# Idea Registry

| idea_id | stage_id | hypothesis | tier_scope | status | notes |
|---|---|---|---|---|---|
| `IDEA-ST62-BASELINEADAPTER-KPI-MARGIN` | `62_adapter_research__kpi_margin_and_tier_b_reactivation` | Stage61 research package(61단계 연구 패키지) adapter(어댑터) `s59ar_v41_sd8_h3` may close the gap(차이) toward legacy 34D KPI target(레거시 34D 핵심 성과 지표 목표) through v2-native(브이투 고유) trade shape(거래 형태), lifecycle(생명주기), state/context(상태/문맥), risk/bracket(위험/브래킷), and Tier B diagnostic(Tier B 진단) work without copying legacy 34D(레거시 34D). | `Tier A primary + Tier B diagnostic(Tier A 우선 + Tier B 진단)` | `active_planned_research_development_only` | Stage62(62단계) redirected(재정렬); effect(효과): 34D KPI(34D 핵심 성과 지표)는 target surface(목표 표면)일 뿐이며 deployment/live/operating claim(배포/실거래/운영 주장)은 만들지 않는다. |
| `IDEA-ST40-CANDLE-MORPHOLOGY-SIGNAL-QUALITY` | `40_feature_structure__candle_morphology_signal_quality_scout` | closed US100 M5 OHLC(확정 US100 5분봉 시가/고가/저가/종가) candle morphology(캔들 형태)가 signal quality(신호 품질)와 bad-entry/bad-hold(나쁜 진입/나쁜 보유) 문맥을 설명할 수 있다 | `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)` | `reviewed_completed_negative_memory_runtime_probe_only` | Stage40(40단계) run34A(실행34A)는 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) 34개 broad sweep(넓은 훑기) 출력과 102개 KPI(`key performance indicator`, 핵심성과지표) row(행)를 남겼다. best validation(최고 검증) `c07_rejection_tail_directional`은 OOS(표본외) 실패, best OOS(최고 표본외) `c15_morphology_score_low_complexity`는 validation(검증) 실패라 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없음 |
| `IDEA-ST16-QDA-CLASS-COVARIANCE` | `16_model_family_challenge__qda_class_covariance_scout` | QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)의 class-specific covariance(클래스별 공분산)가 Stage15(15단계) LDA(`Linear Discriminant Analysis`, 선형 판별 분석) shrinkage clue(공분산 수축 단서)를 더 유연한 판별 경계(discriminant boundary, 판별 경계)로 이어갈 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `reviewed_closed_inconclusive` | Stage16(16단계) run08-run10(실행08-실행10) completed(완료); `run10I` drop_mega10(대형주 10개 제거) reg0.20(정규화 0.20)은 보존 단서이나 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아님 |
| `IDEA-ST11-LGBM-DIRECTION-LONG-ONLY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(`LightGBM`, 라이트GBM) 실패가 direction-asymmetric(방향 비대칭)일 수 있고, long-only(롱만) 라우팅이 short(숏) 손상을 제거할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_inconclusive` | RUN02C(실행 02C); validation/OOS(검증/표본외) `-154.01/82.69` net profit(순수익); salvage value(회수 가치) 있음 |
| `IDEA-ST11-LGBM-DIRECTION-SHORT-ONLY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(라이트GBM) 실패가 direction-asymmetric(방향 비대칭)일 수 있고, short-only(숏만) 라우팅이 long(롱) 손상을 제거할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak` | RUN02D(실행 02D); OOS(표본외) `-211.48 / 0.31`로 약함 |
| `IDEA-ST11-LGBM-EXTREME-CONFIDENCE` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(라이트GBM)은 extreme probability and margin(극단 확률과 마진)에서만 쓸 수 있을 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_inconclusive` | RUN02E(실행 02E); OOS(표본외)는 `-6.35 / 0.96`로 거의 본전이나 validation(검증)이 약함 |
| `IDEA-ST11-LGBM-CALM-TREND-GATE` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | calm trend context(차분한 추세 문맥)에서만 LGBM(라이트GBM) 신호가 깨끗할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak` | RUN02F(실행 02F); validation/OOS(검증/표본외) 모두 약함 |
| `IDEA-ST11-LGBM-LONG-PULLBACK` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02C(실행 02C)의 long-only(롱만) 회수 가치는 RSI/Bollinger pullback(RSI/볼린저 되돌림) 문맥에서 강해질 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_salvage` | RUN02G(실행 02G); OOS(표본외) `238.68 / 3.44`, validation(검증) `-138.39 / 0.54` |
| `IDEA-ST11-LGBM-BULL-TREND-LONG` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | long-only(롱만) LGBM(라이트GBM)은 bullish trend confirmation(상승 추세 확인)이 필요할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak` | RUN02H(실행 02H); OOS(표본외)는 작게 양수이나 validation(검증) 손상이 큼 |
| `IDEA-ST11-LGBM-LOW-VOL-EXTREME-CONFIDENCE` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | extreme confidence(극단 확신)는 low volatility(저변동성) 문맥에서만 살아남을 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_negative` | RUN02I(실행 02I); validation/OOS(검증/표본외) 모두 실패 |
| `IDEA-ST11-LGBM-BALANCED-MIDBAND` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | LGBM(라이트GBM)은 RSI/Bollinger midband(RSI/볼린저 중간대)에서 덜 불안정할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_mixed_weak` | RUN02J(실행 02J); validation(검증)은 양수, OOS(표본외)는 실패 |
| `IDEA-ST11-LGBM-QUIET-RETURN-ZSCORE` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | immediate return z-score(즉시 수익률 z점수)가 조용할 때 LGBM(라이트GBM) 확률 순위가 깨끗할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_negative` | RUN02K(실행 02K); validation/OOS(검증/표본외) 모두 크게 약함 |
| `IDEA-ST11-LGBM-RANGE-COMPRESSION` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | DI spread/ADX(DI 차이/ADX) 압축 문맥에서 LGBM(라이트GBM)이 chase(추격) 손상을 줄일 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_negative` | RUN02L(실행 02L); validation/OOS(검증/표본외) 모두 약함 |
| `IDEA-ST11-LGBM-HIGH-VOL-MOMENTUM-ALIGN` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | volatility expansion(변동성 확장)과 momentum alignment(모멘텀 정렬)가 있어야 LGBM(라이트GBM)이 살아날 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_negative` | RUN02M(실행 02M); validation/OOS(검증/표본외) 모두 약함 |
| `IDEA-ST11-LGBM-SQUEEZE-BREAKOUT` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | Bollinger squeeze breakout(볼린저 압축 돌파) 문맥에서 LGBM(라이트GBM) 신호가 더 이산적일 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_salvage` | RUN02N(실행 02N); OOS(표본외) `107.14 / 55.11`이나 trade count(거래 수) 3개 |
| `IDEA-ST11-LGBM-BULL-VORTEX-LONG` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02C(실행 02C)의 long-only(롱만) 회수 가치는 bullish vortex(상승 보텍스) 문맥에 있을 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak` | RUN02O(실행 02O); OOS(표본외)는 작게 양수이나 validation(검증)이 약함 |
| `IDEA-ST11-LGBM-BEAR-VORTEX-SHORT` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02D(실행 02D)가 약했지만 bearish vortex(하락 보텍스) 문맥에서는 short-only(숏만)가 살아남을 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_tiny_dual_positive_inconclusive` | RUN02P(실행 02P); validation/OOS(검증/표본외) `1.78 / 1.02`, `24.33 / 1.37` |
| `IDEA-ST11-LGBM-BEAR-VORTEX-SHORT-DENSITY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02P(실행 02P)의 작은 dual-positive(양쪽 양수) 판독은 looser bearish vortex short density(느슨한 하락 보텍스 숏 밀도)로 커질 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_negative` | RUN02Q(실행 02Q); validation/OOS(검증/표본외) `-139.28 / 0.62`, `-140.58 / 0.54` |
| `IDEA-ST11-LGBM-LONG-PULLBACK-ADX-REPAIR` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02G(실행 02G)의 OOS(표본외) 회수 가치는 deeper pullback plus ADX gate(더 깊은 되돌림과 ADX 제한)로 validation(검증)을 복구할 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_mixed_weak` | RUN02R(실행 02R); validation(검증) `275.78 / 2.44`, OOS(표본외) `-82.01 / 0.74` |
| `IDEA-ST11-LGBM-SQUEEZE-DENSITY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02N(실행 02N)의 tiny OOS(작은 표본외) 판독은 wider low-bandwidth squeeze density(더 넓은 저대역폭 압축 밀도)로 커질 수 있다 | `Tier A + Tier B mixed(Tier A + Tier B 혼합)` | `runtime_probe_completed_weak_salvage` | RUN02S(실행 02S); validation(검증) `-2.50 / 0.99`, OOS(표본외) `32.56 / 1.69`, trade count(거래 수) 4개 |
| `IDEA-ST11-LABEL-HORIZON-PRIORITY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02S(실행 02S) squeeze density(압축 밀도) 표면은 fwd12(60분)보다 fwd18(90분) label horizon(라벨 예측수평선)에 더 잘 맞을 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_probe_completed_retraining_candidate` | RUN02T(실행 02T); fwd18 OOS hit rate(표본외 적중률) `0.714286` vs fwd12 `0.285714`, 비교 가능 OOS 신호 `7`개라 재학습 후보일 뿐 |
| `IDEA-ST11-WFO-LITE-PRIORITY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02S(실행 02S)는 full WFO(전체 워크포워드 최적화) 전에 window segmentation(구간 분할)으로 표본 밀도를 확인해야 한다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_probe_completed_density_insufficient` | RUN02U(실행 02U); OOS(표본외) 신호 `10`개라 현 표면 그대로 full WFO(전체 워크포워드 최적화)는 이르다 |
| `IDEA-ST11-SHORT-SPECIFIC-PRIORITY` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02P/RUN02Q(실행 02P/02Q)의 숏 표면은 short-specific label/model(숏 전용 라벨/모델) 필요성을 따로 확인해야 한다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_probe_completed_inconclusive` | RUN02V(실행 02V); RUN02Q(실행 02Q)는 신호가 `2.1x`지만 OOS short hit rate(표본외 숏 적중률) `0.190476`라 아직 하위 후보 |
| `IDEA-ST11-LABEL-HORIZON-FWD18-RETRAIN` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02T(실행 02T)의 fwd18(90분) 구조 판독은 LGBM(`LightGBM`, 라이트GBM)을 fwd18 label(90분 라벨)로 재학습하면 MT5(`MetaTrader 5`, 메타트레이더5)에서도 회복될 수 있다 | `Tier A + Tier B mixed/combined(Tier A + Tier B 혼합/합산)` | `mt5_runtime_probe_completed_negative` | RUN02W(실행 02W); routed validation/OOS(라우팅 검증/표본외) net/PF(순수익/수익 팩터) `-496.25 / 0.28`, `-216.12 / 0.67`; Tier B fallback-only(Tier B 대체만) validation(검증)은 양수였지만 OOS(표본외)는 음수 |
| `IDEA-ST11-LABEL-HORIZON-FWD18-RANK-DIRECT` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | fwd18(90분) LGBM(라이트GBM) 고순위 확률 신호를 direct decision(직접 판정)으로 쓰면 RUN02W(실행 02W)를 회복할 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_probe_completed_negative` | RUN02X(실행 02X); Tier A q96 validation/OOS hit rate(Tier A q96 검증/표본외 적중률) `0.25 / 0.15625`; MT5(메타트레이더5)는 out_of_scope_by_claim(주장 범위 밖) |
| `IDEA-ST11-LABEL-HORIZON-FWD18-INVERSE-RANK` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | fwd18(90분) LGBM(라이트GBM) 고순위 신호는 inverse decision(역방향 판정)으로 쓸 때 더 깨끗할 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_probe_completed_mixed` | RUN02Y(실행 02Y); Tier A q96 validation/OOS hit rate(Tier A q96 검증/표본외 적중률) `0.604167 / 0.34375`; 단독 inverse(역방향)만으로는 부족 |
| `IDEA-ST11-LABEL-HORIZON-FWD18-INVERSE-RANK-CONTEXT` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | fwd18(90분) inverse rank(역방향 순위)는 DI spread/ADX(DI 차이/ADX) 압축 문맥에서 런타임 거래 품질을 회복할 수 있다 | `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)` | `runtime_probe_completed_positive_tiny_sample` | RUN02Z(실행 02Z); routed validation/OOS(라우팅 검증/표본외) `386.06 / 7.25 / 9 trades(거래)`, `352.63 / 52.03 / 5 trades(거래)`; stress test(압박 시험) 필요, promotion(승격) 아님 |
| `IDEA-ST11-LABEL-HORIZON-FWD18-INVERSE-RANK-CONTEXT-STRESS` | `11_alpha_robustness__wfo_label_horizon_sensitivity` | RUN02Z(실행 02Z)의 fwd18 inverse rank context(fwd18 역방향 순위 문맥)는 ADX cutoff(ADX 절단값), routing(라우팅), session slice(세션 구간) 압박에서도 중심 조건을 유지할 수 있다 | `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)` | `runtime_probe_completed_stress_survived_center_tiny_sample` | RUN02AA~RUN02AK(실행 02AA~02AK); `ADX<=25`, `200-220`, routed(라우팅)가 best center(최고 중심); promotion_candidate(승격 후보) 아님 |

### Stage 12(12단계) run03D standalone(단독) batch-20(20개 묶음)

| idea_id(아이디어 ID) | status(상태) | hypothesis(가설) | evidence(근거) |
|---|---|---|---|
| `IDEA-ST12-ET-BATCH20-V01` | `inconclusive_standalone_structural_scout` | 기본 잎 20 구조가 단독 Stage12 신호를 만든다. | `run03D_et_standalone_batch20_v1` `v01_base_leaf20_q90` val_hit(검증 적중)=0.384772, oos_hit(표본외 적중)=0.472727 |
| `IDEA-ST12-ET-BATCH20-V02` | `inconclusive_standalone_structural_scout` | 잎 10의 촘촘한 구조가 약한 방향 신호를 더 잘 잡는다. | `run03D_et_standalone_batch20_v1` `v02_dense_leaf10_q90` val_hit(검증 적중)=0.377665, oos_hit(표본외 적중)=0.448586 |
| `IDEA-ST12-ET-BATCH20-V03` | `inconclusive_standalone_structural_scout` | 잎 40의 부드러운 구조가 잡음을 줄인다. | `run03D_et_standalone_batch20_v1` `v03_smooth_leaf40_q90` val_hit(검증 적중)=0.362437, oos_hit(표본외 적중)=0.437252 |
| `IDEA-ST12-ET-BATCH20-V04` | `inconclusive_standalone_structural_scout` | 분기마다 더 적은 피처를 보면 과적합이 줄어든다. | `run03D_et_standalone_batch20_v1` `v04_log2_features_leaf20_q90` val_hit(검증 적중)=0.385787, oos_hit(표본외 적중)=0.441137 |
| `IDEA-ST12-ET-BATCH20-V05` | `inconclusive_standalone_structural_scout` | 절반 피처 샘플링이 방향 신호 다양성을 만든다. | `run03D_et_standalone_batch20_v1` `v05_half_features_leaf20_q90` val_hit(검증 적중)=0.375635, oos_hit(표본외 적중)=0.465496 |
| `IDEA-ST12-ET-BATCH20-V06` | `inconclusive_standalone_structural_scout` | 엔트로피 분할 기준이 비대칭 라벨 구조를 더 잘 본다. | `run03D_et_standalone_batch20_v1` `v06_entropy_leaf20_q90` val_hit(검증 적중)=0.376650, oos_hit(표본외 적중)=0.455629 |
| `IDEA-ST12-ET-BATCH20-V07` | `inconclusive_standalone_structural_scout` | 부트스트랩 균형 가중치가 클래스 불균형을 완화한다. | `run03D_et_standalone_batch20_v1` `v07_balanced_subsample_leaf20_q90` val_hit(검증 적중)=0.366497, oos_hit(표본외 적중)=0.462264 |
| `IDEA-ST12-ET-BATCH20-V08` | `inconclusive_standalone_structural_scout` | 깊이 12 제한이 표본외 흔들림을 줄인다. | `run03D_et_standalone_batch20_v1` `v08_depth12_leaf20_q90` val_hit(검증 적중)=0.385787, oos_hit(표본외 적중)=0.452349 |
| `IDEA-ST12-ET-BATCH20-V09` | `inconclusive_standalone_structural_scout` | 얕은 깊이와 촘촘한 잎 조합이 안정 신호를 만든다. | `run03D_et_standalone_batch20_v1` `v09_depth8_leaf10_q90` val_hit(검증 적중)=0.392893, oos_hit(표본외 적중)=0.482663 |
| `IDEA-ST12-ET-BATCH20-V10` | `inconclusive_standalone_structural_scout` | 70% 부트스트랩 표본이 모델 분산을 낮춘다. | `run03D_et_standalone_batch20_v1` `v10_bootstrap70_leaf20_q90` val_hit(검증 적중)=0.382741, oos_hit(표본외 적중)=0.442667 |
| `IDEA-ST12-ET-BATCH20-V11` | `inconclusive_standalone_structural_scout` | 더 낮은 임계값이 신호 밀도를 회복한다. | `run03D_et_standalone_batch20_v1` `v11_base_leaf20_q85` val_hit(검증 적중)=0.392688, oos_hit(표본외 적중)=0.457317 |
| `IDEA-ST12-ET-BATCH20-V12` | `inconclusive_standalone_structural_scout` | 더 높은 임계값이 신호 품질을 선별한다. | `run03D_et_standalone_batch20_v1` `v12_base_leaf20_q95` val_hit(검증 적중)=0.326572, oos_hit(표본외 적중)=0.438776 |
| `IDEA-ST12-ET-BATCH20-V13` | `inconclusive_standalone_structural_scout` | 0.02 마진 요구가 애매한 예측을 걸러낸다. | `run03D_et_standalone_batch20_v1` `v13_base_margin002_q90` val_hit(검증 적중)=0.385875, oos_hit(표본외 적중)=0.472656 |
| `IDEA-ST12-ET-BATCH20-V14` | `inconclusive_standalone_structural_scout` | 0.05 마진 요구가 강한 예측만 남긴다. | `run03D_et_standalone_batch20_v1` `v14_base_margin005_q90` val_hit(검증 적중)=0.375271, oos_hit(표본외 적중)=0.466045 |
| `IDEA-ST12-ET-BATCH20-V15` | `inconclusive_standalone_structural_scout` | 숏 방향만 남기면 비대칭 수익 신호가 보인다. | `run03D_et_standalone_batch20_v1` `v15_base_short_only_q90` val_hit(검증 적중)=0.362069, oos_hit(표본외 적중)=0.463303 |
| `IDEA-ST12-ET-BATCH20-V16` | `inconclusive_standalone_structural_scout` | 롱 방향만 남기면 비대칭 수익 신호가 보인다. | `run03D_et_standalone_batch20_v1` `v16_base_long_only_q90` val_hit(검증 적중)=0.404990, oos_hit(표본외 적중)=0.485030 |
| `IDEA-ST12-ET-BATCH20-V17` | `inconclusive_standalone_structural_scout` | 훈련 중요도 상위 30개 피처가 약한 피처 잡음을 줄인다. | `run03D_et_standalone_batch20_v1` `v17_top30_features_q90` val_hit(검증 적중)=0.381726, oos_hit(표본외 적중)=0.460859 |
| `IDEA-ST12-ET-BATCH20-V18` | `inconclusive_standalone_structural_scout` | 핵심 42개 피처만으로도 단독 Stage12 신호가 유지된다. | `run03D_et_standalone_batch20_v1` `v18_core42_features_q90` val_hit(검증 적중)=0.367513, oos_hit(표본외 적중)=0.467202 |
| `IDEA-ST12-ET-BATCH20-V19` | `inconclusive_standalone_structural_scout` | 보조 문맥 16개 피처만으로 독립 신호가 있는지 본다. | `run03D_et_standalone_batch20_v1` `v19_context16_features_q90` val_hit(검증 적중)=0.393909, oos_hit(표본외 적중)=0.430622 |
| `IDEA-ST12-ET-BATCH20-V20` | `mixed_unstable_standalone_structural_scout` | 확률 방향을 반대로 쓰면 구조적 역방향성이 드러난다. | `run03D_et_standalone_batch20_v1` `v20_base_inverse_q90` val_hit(검증 적중)=0.432487, oos_hit(표본외 적중)=0.309091 |
### Stage 12(12단계) run03G variant stability(변형 안정성)

| idea_id(아이디어 ID) | variant(변형) | status(상태) | evidence(근거) |
|---|---|---|---|
| `IDEA-ST12-ET-BATCH20-V09` | `v09_depth8_leaf10_q90` | `secondary_mt5_probe_candidate` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.392893` / `0.482663`, role(역할) `priority_depth_limited_both_direction` |
| `IDEA-ST12-ET-BATCH20-V16` | `v16_base_long_only_q90` | `mt5_probe_priority` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.404990` / `0.485030`, role(역할) `priority_long_only_asymmetry` |
| `IDEA-ST12-ET-BATCH20-V13` | `v13_base_margin002_q90` | `secondary_mt5_probe_candidate` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.385875` / `0.472656`, role(역할) `priority_margin_filter` |
| `IDEA-ST12-ET-BATCH20-V18` | `v18_core42_features_q90` | `secondary_mt5_probe_candidate` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.367513` / `0.467202`, role(역할) `secondary_core42_tier_b_alignment` |
| `IDEA-ST12-ET-BATCH20-V01` | `v01_base_leaf20_q90` | `secondary_mt5_probe_candidate` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.384772` / `0.472727`, role(역할) `secondary_base_q90_reference` |
| `IDEA-ST12-ET-BATCH20-V11` | `v11_base_leaf20_q85` | `reference_already_mt5_tier_balance` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.392688` / `0.457317`, role(역할) `reference_already_mt5_tier_balance` |
| `IDEA-ST12-ET-BATCH20-V20` | `v20_base_inverse_q90` | `negative_boundary_inverse_direction` | `run03G_et_variant_stability_probe_v1` val/OOS hit(검증/표본외 적중) `0.432487` / `0.309091`, role(역할) `negative_boundary_inverse_direction` |

| `IDEA-ST12-ET-RECENCY-WEIGHTED-SINGLE` | `12_model_family_challenge__extratrees_training_effect` | recency-weighted ExtraTrees(최근성 가중 엑스트라 트리)가 최근 regime(국면)을 더 잘 볼 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03L(실행 03L); Python routed hit(파이썬 라우팅 적중) `0.401285` / `0.414419`, MT5 routed net(MT5 라우팅 순수익) `192.33` / `132.20` |

| `IDEA-ST12-ET-SESSION-AGE-REGIME` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 session age(세션 경과 시간)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03M(실행 03M); fold07(접힘 7) 제외; best bucket(최상위 구간) `0-60` |

| `IDEA-ST12-ET-VOLATILITY-REGIME` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 volatility regime(변동성 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03N(실행 03N); fold07(접힘 7) 제외; best bucket(최상위 구간) `high_vol_two_plus_flags` |

| `IDEA-ST12-ET-TREND-CHOP-REGIME` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 trend/chop regime(추세/횡보 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03O(실행 03O); fold07(접힘 7) 제외; best bucket(최상위 구간) `chop_zero_trend_flags` |

| `IDEA-ST12-ET-MEGA-CAP-DIVERGENCE` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 mega-cap divergence regime(대형주 괴리 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03P(실행 03P); fold07(접힘 7) 제외; best bucket(최상위 구간) `wide_or_dispersed_mega_cap_divergence` |

| `IDEA-ST12-ET-MACRO-PROXY-REGIME` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 macro proxy regime regime(거시 대리 국면 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03Q(실행 03Q); fold07(접힘 7) 제외; best bucket(최상위 구간) `macro_risk_on_relief` |

| `IDEA-ST12-ET-GAP-OVERNIGHT-CONTEXT` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 gap/overnight context regime(갭/야간 문맥 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03R(실행 03R); fold07(접힘 7) 제외; best bucket(최상위 구간) `gap_or_overnight_down_context` |

| `IDEA-ST12-ET-PROBABILITY-SHAPE-ATTRIBUTION` | `12_model_family_challenge__extratrees_training_effect` | ExtraTrees(엑스트라 트리) 신호는 특정 probability-shape attribution regime(확률 모양 귀속 국면)에 집중될 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_probe_completed_inconclusive` | RUN03S(실행 03S); fold07(접힘 7) 제외; best bucket(최상위 구간) `thin_probability_edge` |

| `IDEA-ST17-XGBOOST-REGULARIZED-BOOSTING` | `17_model_family_challenge__xgboost_regularized_boosting_scout` | XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) regularized boosting(규제 부스팅)이 기존 LightGBM/ExtraTrees/discriminant models(라이트GBM/엑스트라 트리/판별 모델)와 다른 probability shape(확률 모양), signal density(신호 밀도), validation/OOS(검증/표본외) 보존성을 만들 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `reviewed_closed_inconclusive` | Stage17(17단계)은 run11A~run11G(실행11A~실행11G)까지 확인하고 `closed_inconclusive_xgboost_dart_attribution_no_new_axis_after_run11G`로 닫음; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없음 |
| `IDEA-ST18-CATBOOST-ORDERED-BOOSTING` | `18_model_family_challenge__catboost_ordered_boosting_scout` | CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting(순서 부스팅)과 symmetric tree(대칭 트리)가 Stage17(17단계) XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) DART(드롭아웃 부스팅)와 다른 probability shape(확률 모양), signal density(신호 밀도), direction balance(방향 균형)를 만들 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `topic_open_no_run` | Stage18(18단계) topic(주제)만 열림; 첫 후보는 `run12A_catboost_ordered_boosting_characteristic_scout_v1`; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없음 |
| `IDEA-ST19-EBM-EXPLAINABLE-SHAPE` | `19_model_family_challenge__ebm_explainable_boosting_shape` | EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)이 additive feature shape(가산 피처 모양)를 보여줄 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `runtime_handoff_blocked_after_attempt` | `run13A_ebm_main_effect_shape_scout_v1` 구조 단서 보존; `run13B`~`run13G` MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침) 42회 시도는 `onnx_run_failed:5803`으로 차단; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없음 |
| `IDEA-ST20-GAM-ADDITIVE-SMOOTH-SHAPE` | `20_model_family_challenge__gam_additive_smooth_shape` | GAM(`Generalized Additive Model`, 일반화 가산 모델)이 audited 58-feature surface(감사된 58개 피처 표면)에서 smooth additive short/long shape(부드러운 가산 매도/매수 모양)를 보여줄 수 있다 | `Tier A + Tier B combined(Tier A + Tier B 합산)` | `structural_scout_completed_inconclusive` | `run14A_gam_additive_shape_scout_v1` completed(완료); selected variant(선택 변형) `v02_core24_smoother`, best overall(전체 최고) `v03_proxy_context20_tier_a`; MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)는 다음 `run14B` 조건; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없음 |

## Rule

Register ideas when they become durable work, not for every passing thought.
- 2026-05-03 Stage16 QDA run09 follow-up(16단계 QDA 실행09 후속 탐색): regularization(정규화), feature removal(피처 제거), sample size(표본 크기), coverage threshold(커버리지 임계값)를 MT5(메타트레이더5) KPI(핵심성과지표)까지 비교했다. 효과(effect, 효과): 보존 단서와 실패 기억을 Stage16 안에 남긴다.
- 2026-05-03 Stage16 QDA run10 decision microprobe(16단계 QDA 실행10 결정 미세 탐침): full58 reg0.18 neighborhood(full58 정규화 0.18 주변)와 drop_mega10(대형주 10개 제거) 계열을 MT5(메타트레이더5) KPI(핵심성과지표)까지 재검증했다. recommendation(권고): `close_stage16_preserve_qda_clues`. 효과(effect, 효과): 반복 생존 여부를 close(닫기)/continue(진행) 판정에 연결한다.
- 2026-05-03 Stage16 closeout(16단계 종료): QDA(이차 판별 분석)는 `closed_inconclusive_qda_class_covariance_runtime_probe_evidence`로 닫았다. 효과(effect, 효과): `run10I` 보존 단서와 full58(전체 58개 피처) reg0.18(정규화 0.18) OOS(표본외) spike(튀는 성과)를 실패 기억과 함께 남기고, 같은 single split(단일 분할) QDA micro-tuning(미세 조정)은 멈춘다.
- 2026-05-03 Stage17 open-only(17단계 개방만): `17_topic_pending__open_only`를 topic pending(주제 보류)으로 열었다. 효과(effect, 효과): 새 topic(주제), model family(모델 계열), run(실행), KPI(핵심성과지표)는 아직 만들지 않는다.
- 2026-05-03 Stage17 topic selection(17단계 주제 선택): `17_model_family_challenge__xgboost_regularized_boosting_scout`를 XGBoost(`Extreme Gradient Boosting`, 익스트림 그래디언트 부스팅) regularized boosting(규제 부스팅) 주제로 열었다. 효과(effect, 효과): 첫 XGBoost(익스지부스트) run(실행)을 설계할 수 있게 하되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

| `IDEA-ST271-FRESH-EDGE-REBUILD-AFTER-NONFILTER-FAILURE` | `271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure` | loss-asymmetry/time-risk decision surface(손실 비대칭/시간 위험 판단 표면)가 Stage270(270단계)의 non-filter reward-skew failure(비필터 보상 기울기 실패)를 새 후보 패키지 경로로 바꿀 수 있다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | `run271A_design_fresh_edge_rebuild_queue`에서 fresh edge rebuild queue(새 거래 우위 재구성 대기열)를 설계한다. selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST271-CP271B-TIME-RISK-PHASE-ROUTER` | `271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure` | time-risk phase router(시간 위험 국면 라우터)가 Stage270(270단계) 실패 뒤 약한 구간을 분리할 수 있다 | `Tier A + Tier B paired structural scout(Tier A + Tier B 쌍 구조 스카우트)` | `probe_seed_not_candidate` | run271E(271E 실행); Stage272 probe queue(272단계 탐침 대기열) 1행, selected candidate(선택 후보) 아님 |

| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE` | `272_onnx_candidate_campaign__time_risk_router_pressure_probe` | time-risk phase router(시간 위험 국면 라우터)가 OOS(표본외) 약점과 route mix(경로 혼합) 붕괴를 견디면 Adapter package(어댑터 패키지) 압박으로 넘어갈 수 있다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | `run272A_design_time_risk_router_pressure_probe_packet`에서 pressure design(압박 설계), discard condition(폐기 조건), MT5 probe plan(MT5 탐침 계획)을 만든다. selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없음 |

| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272A` | `272_onnx_candidate_campaign__time_risk_router_pressure_probe` | cp271B(271B 패키지)의 time-risk router(시간 위험 라우터)를 압박 분기 `6`개로 나눠 MT5 probe(MT5 탐침) 전 failure boundary(실패 경계)를 본다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `design_packet_ready_no_candidate` | MT5 probe design queue(MT5 탐침 설계 대기열) `5`행. selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없음 |

| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272B` | `272_onnx_candidate_campaign__time_risk_router_pressure_probe` | run272A(272A 실행)의 pressure branch(압박 분기)를 payload parquet(페이로드 파케이)와 MT5 signal CSV(MT5 신호 CSV)로 물질화한다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `payload_materialized_no_candidate` | payload(페이로드) `4`개, MT5 queue(MT5 대기열) `4`행, selected candidate(선택 후보) 없음 |

| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272D` | `272_onnx_candidate_campaign__time_risk_router_pressure_probe` | q04(4번 분기)를 pressure survivor(압박 생존 분기)로 Stage273(273단계)에 넘긴다 | `Tier A + Tier B paired MT5 runtime probe(Tier A + Tier B 쌍 MT5 런타임 탐침)` | `pressure_survivor_no_candidate` | survivor rows(생존 행) `2`개, selected candidate(선택 후보) 없음 |

| `IDEA-ST274-POST-Q04-CANDIDATE-BLUEPRINTS-RUN274B` | `274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild` | q04 failure memory(q04 실패 기억)를 새 candidate package blueprint(후보 패키지 청사진)로 재구성 | `blueprints=4;selectable=3;support_control=1` | `materialized_blueprint_no_selection` | selected candidate(선택 후보) 없음, ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST275-FRESH-CANDIDATE-CONSTRUCTION-AFTER-FILTER-LIKE-FAILURE` | `275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure` | filter-like rebuild failure(필터형 재구성 실패) 이후 새 active entry/direction surface(새 활성 진입/방향 표면)를 만든다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | next_action(다음 행동) `run275A_design_fresh_candidate_construction_packet`; selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없음 |

## 2026-05-23 run275E_screen_fresh_candidate_score_surfaces_v1

- idea(아이디어): Stage276 aggressive fresh surface probe(276단계 공격형 새 표면 탐침) seeds(씨앗) `3`개.
- evidence(근거): `stages/275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure/02_runs/run275E/stage276_queue.csv`
- boundary(경계): probe seed(탐침 씨앗)이며 selected candidate(선택 후보)가 아니다.

| `IDEA-ST276-AGGRESSIVE-FRESH-SURFACE-PROBE` | `276_onnx_candidate_campaign__aggressive_fresh_surface_probe` | Stage275(275단계) fresh surface(새 표면) queue(대기열)를 MT5 pressure probe(MT5 압박 탐침)로 검증한다. | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | next_action(다음 행동) `run276A_design_aggressive_fresh_surface_probe_packet`; selected candidate(선택 후보), ONNX readiness(ONNX 준비) 없음 |

| `IDEA-ST277-FRESH-THESIS-REBUILD-AFTER-AGGRESSIVE-SURFACE-FAILURE` | `277_onnx_candidate_campaign__fresh_thesis_rebuild` | Stage276(276단계) failure memory(실패 기억)를 fresh thesis rebuild(새 논제 재구성)로 바꾼다. | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | seed rows(씨앗 행) `4`; next_action(다음 행동) `run277A_design_fresh_thesis_rebuild_packet`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277A` | `277_onnx_candidate_campaign__fresh_thesis_rebuild` | Stage276(276단계) failure memory(실패 기억)를 candidate package queue(후보 패키지 대기열)로 재구성한다. | `package_rows=4;support_control=1` | `design_packet_ready_no_selection` | next_action(다음 행동) `run277B_materialize_fresh_thesis_candidate_blueprints`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277B` | `277_onnx_candidate_campaign__fresh_thesis_rebuild` | run277A(277A 실행) package queue(패키지 대기열)를 materialized blueprint(물질화 청사진)로 바꾼다. | `blueprints=4` | `blueprint_materialized_no_selection` | next_action(다음 행동) `run277C_materialize_fresh_thesis_scoring_handoff_inputs`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277C` | `277_onnx_candidate_campaign__fresh_thesis_rebuild` | run277B(277B 실행) blueprints(청사진)를 scoring/handoff input(점수/인계 입력)으로 바꾼다. | `scoring_specs=4` | `input_materialized_no_selection` | next_action(다음 행동) `run277D_execute_fresh_thesis_scoring_probe`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277D` | `277_onnx_candidate_campaign__fresh_thesis_rebuild` | run277C(277C 실행) scoring specs(점수 규격)를 Tier A/Tier B(티어 A/티어 B) score table(점수표)로 물질화한다. | `packages=4` | `score_materialized_no_selection` | next_action(다음 행동) `run277E_screen_fresh_thesis_score_surfaces`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277E` | `277_onnx_candidate_campaign__fresh_thesis_rebuild` | run277D(277D 실행) score surface(점수 표면)를 Stage278(278단계) MT5 probe(MT5 탐침) queue(대기열)로 선별한다. | `probe_queue=2;failure_memory=2` | `probe_queue_ready_no_selection` | next_action(다음 행동) `run277F_close_stage277_open_stage278_fresh_thesis_mt5_probe`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST278-FRESH-THESIS-MT5-PROBE` | `278_onnx_candidate_campaign__fresh_thesis_mt5_probe` | Stage277(277단계)의 `cp277C/cp277D` score surface(점수 표면)를 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)와 pressure probe(압박 탐침)로 검증한다. | `Tier A used + Tier B fallback + actual routed total(Tier A 사용 + Tier B 대체 + 실제 라우팅 전체)` | `opened_runtime_probe_preparation_only` | next_action(다음 행동) `run278A_design_fresh_thesis_mt5_probe_packet`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278A` | `278_onnx_candidate_campaign__fresh_thesis_mt5_probe` | `cp277C/cp277D` score surface(점수 표면)를 MT5(`MetaTrader 5`, 메타트레이더5) payload(페이로드)용 branch(분기) `8`개로 설계한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `design_ready_no_candidate` | MT5 probe design queue(MT5 탐침 설계 대기열) `6`개; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278B` | `278_onnx_candidate_campaign__fresh_thesis_mt5_probe` | run278A(278A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열)를 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 물질화한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `payload_materialized_no_candidate` | payload(페이로드) `6`개, MT5 queue(MT5 대기열) `6`행, selected candidate(선택 후보) 없음 |

| `IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278C` | `278_onnx_candidate_campaign__fresh_thesis_mt5_probe` | active/flat(활성/관망) payload(페이로드)를 MT5 tester(MT5 테스터)에 넣기 전 direction mapping gap(방향 매핑 공백)을 검사한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `blocked_direction_mapping_missing` | blocked attempts(차단 시도) `6`개, selected candidate(선택 후보) 없음 |

| `IDEA-ST279-DIRECTIONAL-RUNTIME-MAPPING-REBUILD` | `279_onnx_candidate_campaign__directional_runtime_mapping_rebuild` | active/flat(활성/관망) surface(표면)를 supported direction surface(지원되는 방향 표면)로 재구성하거나 폐기한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `stage_open_no_candidate` | direction gap rows(방향 공백 행) `6`, blocked attempts(차단 시도) `6`, selected candidate(선택 후보) 없음 |

| `IDEA-ST279-DIRECTIONAL-MAPPING-RUN279A` | `279_onnx_candidate_campaign__directional_runtime_mapping_rebuild` | active/flat(활성/관망) mask(마스크)에 supported direction source(지원되는 방향 원천)를 붙이는 branch(분기)를 설계한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `design_ready_no_candidate` | branch(분기) `5`개, queue(대기열) `4`개, selected candidate(선택 후보) 없음 |

| `IDEA-ST279-DIRECTIONAL-MAPPING-RUN279B` | `279_onnx_candidate_campaign__directional_runtime_mapping_rebuild` | active/flat(활성/관망) mask(마스크)에 feature-derived direction(피처 기반 방향)을 붙여 MT5 probe(MT5 탐침) 입력을 만든다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `materialized_no_candidate` | directional payload(방향 페이로드) `12`개, selected candidate(선택 후보) 없음 |

| `IDEA-ST280-DIRECTIONAL-STABILITY` | `280_onnx_candidate_campaign__directional_mapping_stability_validation` | Stage279(279단계) survivor seed(생존 씨앗)를 curve/month/session/trade-quality stress(곡선/월/세션/거래품질 압박)로 검증한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `opened_no_candidate` | survivor seed(생존 씨앗) `3`개, selected candidate(선택 후보) 없음 |

| `IDEA-ST281-DRAWDOWN-NORMALIZED-DIRECTION` | `281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild` | 손실폭 정규화 방향 후보 재구성 | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `opened_no_candidate` | Stage280(280단계) 실패 기억에서 새 판단/위험 표면을 만든다 |

| `IDEA-ST281-RUN281A-DRAWDOWN-NORMALIZED-INPUTS` | `281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild` | 손실폭 정규화 방향 후보 입력 `4`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | MT5 탐침으로 검증 필요 |

| `IDEA-ST282-VALIDATION-FIRST-ASYMMETRIC-CONFIRMATION` | `282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild` | validation-first asymmetric confirmation(검증 우선 비대칭 확인) | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `opened_no_candidate` | Stage281(281단계)의 OOS(표본외) 상방 착시를 막고 검증 회복력을 먼저 요구한다. |

| `IDEA-ST282-RUN282A-VALIDATION-FIRST-INPUTS` | `282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild` | validation-first candidate inputs(검증 우선 후보 입력) `4`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | MT5 탐침으로 검증 회복력과 표본외 상방을 함께 본다. |

| `IDEA-ST283-ADAPTER-PACKAGE-CP282D` | `283_onnx_candidate_campaign__adapter_package_for_cp282d_macro_trend_countercheck` | Adapter package(어댑터 패키지) for `cp282D_macro_trend_countercheck_surface` | `Tier A used + Tier B fallback stress + actual routed total` | `opened_adapter_package_pending` | 선택 후보를 온엑스 전 추적 가능 패키지로 고정한다. |

| `IDEA-ST286-RUN286A-TRADE-DENSITY-CURVE-QUALITY` | `286_onnx_candidate_campaign__trade_density_curve_quality_rebuild` | trade density/curve quality first(거래 밀도/곡선 품질 우선) 후보 `5`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | 4-10 trades/day(일 4-10거래)와 순수익 규모를 먼저 맞춘 뒤 Adapter/ONNX(어댑터/온엑스)로 넘긴다. |

| `IDEA-ST287-DENSITY-SCALE-CURVE-POCKET-REBUILD` | `287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild` | density/scale clue(밀도/규모 단서) `2`개에서 curve pocket(곡선 포켓)을 구조적으로 줄이는 새 후보 구성 | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | threshold-only repair(임계값만 고치는 수리)를 금지하고 과거 stage(단계) 약점 자료를 다시 연결한다. |

| `IDEA-ST287-RUN287A-DENSITY-SCALE-CURVE-POCKET` | `287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild` | density/scale curve-pocket rebuild(밀도/규모 곡선 포켓 재구성) 후보 `5`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | 과거 stage(단계) 자료를 활용해 session/volatility/hold(세션/변동성/보유) 구조를 바꾼다. |

| `IDEA-ST288-RISK-REWARD-EXIT-ASYMMETRY` | `288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild` | ATR SL/TP + exit overlay + model risk sizing(ATR 손절/익절 + 청산 오버레이 + 모델 위험 크기) | `Tier A used + Tier B fallback stress + actual routed total` | `opened` | Stage287(287단계) density/profit seed(밀도/수익 씨앗)의 효율/곡선 실패를 risk/reward/exit surface(위험/보상/청산 표면)로 다시 실험한다. |

| `IDEA-ST289-REGIME-CONDITIONED-EDGE-SURFACE` | `289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild` | regime-conditioned edge surface(국면 조건부 엣지 표면) | `Tier A used + Tier B fallback stress + actual routed total` | `opened` | Stage288(288단계) exit/risk-only(청산/위험 단독) 실패 후 session/volatility/macro/trend(세션/변동성/매크로/추세) 결합 표면을 만든다. |

| `IDEA-ST290-PAYOFF-WEIGHTED-EDGE-MODEL` | `290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild` | payoff-weighted edge model rebuild(수익 가중 엣지 모델 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened` | Stage289(289단계)의 density-pass/profit-fail(밀도 통과/수익 실패) 이후 inherited signal filtering(계승 신호 필터링)을 버리고 새 label/objective/model surface(라벨/목적함수/모델 표면)를 만든다. |

| `IDEA-ST292-ANTI-DIRECTION-META-LABEL-TRADE-SIM` | `292_onnx_candidate_campaign__anti_direction_meta_label_trade_simulator_rebuild` | anti-direction meta-label/trade simulator rebuild(역방향 메타라벨/거래 시뮬레이터 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage291(291단계)의 WFO negative runtime(워크포워드 음수 런타임)을 새 invert/skip/simulator/density-profit 구조로 바꾼다. selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST293-PROFIT-SCALE-DENSITY-CALIBRATION` | `293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild` | runtime-aware profit-scale/density/curve calibration(런타임 인식 순수익 규모/밀도/곡선 보정) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage292(292단계)의 proxy-runtime gap(대리-런타임 공백)을 새 구조 논제로 전환 |

| `IDEA-ST294-MT5-OUTCOME-RELABEL-DIRECTIONAL-FLIP` | `294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild` | MT5 outcome relabel and directional flip rebuild(MT5 결과 재라벨/방향 반전 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage293(293단계)의 near-breakeven dense losers(고밀도 근본전 손실)를 실제 체결 손익 label(라벨)로 재구성 |

| `IDEA-ST295-SPLIT-CONSISTENT-OUTCOME-DISTILLATION` | `295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild` | split-consistent outcome distillation(분할 일관 결과 증류) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage294(294단계)의 OOS 양수/validation 음수 비대칭을 새 label/decision/risk surface(라벨/판단/위험 표면)로 재구성 |

| `IDEA-ST296-DENSITY-FLOOR-PROFIT-EXPANSION` | `296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild` | density-floor profit expansion(거래 밀도 하한 수익 확장) | `Tier A used + Tier B fallback + actual routed total` | `opened_from_stage295_no_candidate` | cp295D 수익 단서와 cp295B/E OOS 상방 단서를 4-10 trades/day(일 4-10거래) 새 표면으로 재구성 |

| `IDEA-ST297-BILEVEL-CURVE-MONOTONIC-PROFIT` | `297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild` | bi-level curve-monotonic profit rebuild(이중 단계 곡선 단조 수익 재구성) | `Tier A used + Tier B fallback stress + actual routed total` | `opened_no_candidate` | Stage296(296단계)의 proxy-positive/runtime-gated(대리 양수/런타임 관문) 공백을 entry creation(진입 생성), profit scale(순수익 규모), curve veto(곡선 거부) 공동 목적함수로 재구성 |

## run297C_review_bilevel_curve_monotonic_profit_mt5_probe_v1 profit-scale edge amplification handoff(수익 규모 거래우위 증폭 인계)

- idea_id(아이디어 ID): `stage298_profit_scale_edge_amplification_primary`
- hypothesis(가설): Stage297(297단계)의 낮은 순수익은 진입 수가 아니라 payoff magnitude(보상 크기)와 exit asymmetry(청산 비대칭)의 병목일 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run298C_review_profit_scale_edge_amplification_mt5_probe_v1 runtime-realized trade shape handoff(런타임 실제 거래 형태 인계)

- idea_id(아이디어 ID): `stage299_runtime_realized_trade_shape_primary`
- hypothesis(가설): validation damage(검증 손상)는 entry score(진입 점수)가 아니라 실제 hold/exit/trade-shape(보유/청산/거래 형태) 병목일 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run299C_review_runtime_realized_trade_shape_mt5_probe_v1 split-forward trade shape handoff(분할 전진 거래 형태 인계)

- idea_id(아이디어 ID): `stage300_split_forward_shape_generalization_primary`
- hypothesis(가설): Stage299(299단계)의 validation(검증) 회복은 일반화되지 않았으므로 시간 순서 subfold(하위 분할)에서 살아남는 형태만 후보가 될 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run300C_review_split_forward_trade_shape_generalization_mt5_probe_v1 split-forward trade shape handoff(분할 전진 거래 형태 인계)

- idea_id(아이디어 ID): `stage301_orthogonal_profit_source_primary`
- hypothesis(가설): Stage300(300단계)의 validation(검증) 회복은 일반화되지 않았으므로 시간 순서 subfold(하위 분할)에서 살아남는 형태만 후보가 될 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run301C_review_orthogonal_profit_source_mt5_probe_v1 payoff convexity handoff(보상 볼록성 인계)

- idea_id(아이디어 ID): `stage302_payoff_convexity_profit_scale_primary`
- hypothesis(가설): Stage301(301단계)의 작은 양수 MT5(메타트레이더5) edge(우위)는 방향 모델보다 보상/청산/위험 표면을 바꿔야 수익 규모로 커질 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run302C_review_payoff_convexity_profit_scale_mt5_probe_v1 regime-balanced router handoff(레짐 균형 라우터 인계)

- idea_id(아이디어 ID): `stage303_regime_balanced_profit_scale_router_primary`
- hypothesis(가설): Stage302(302단계)의 OOS scale(표본외 규모)은 레짐/세션 조건을 분리해야 validation damage(검증 손상) 없이 살아남을 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run303C_review_regime_balanced_profit_scale_router_mt5_probe_v1 regime-balanced router handoff(레짐 균형 라우터 인계)

- idea_id(아이디어 ID): `stage304_curve_pocket_aware_profit_source_primary`
- hypothesis(가설): Stage303(302단계)의 OOS scale(표본외 규모)은 레짐/세션 조건을 분리해야 validation damage(검증 손상) 없이 살아남을 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), no Adapter/ONNX(어댑터/온엑스 없음).

## run304C_review_curve_pocket_aware_profit_source_mt5_probe_v1 curve-pocket-aware profit source(곡선 포켓 인식 수익 원천)

- idea_id(아이디어 ID): `stage304_curve_pocket_aware_profit_source`
- hypothesis(가설): 곡선 포켓을 WFO(워크포워드 최적화) 목적에 넣으면 순수익 규모와 매끄러운 곡선을 함께 만들 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run305C_review_runtime_realized_curve_attribution_mt5_probe_v1 curve-pocket-aware profit source(怨≪꽑 ?ъ폆 ?몄떇 ?섏씡 ?먯쿇)

- idea_id(?꾩씠?붿뼱 ID): `stage306_runtime_realized_curve_attribution`
- hypothesis(媛??: 怨≪꽑 ?ъ폆??WFO(?뚰겕?ъ썙??理쒖쟻?? 紐⑹쟻???ｌ쑝硫??쒖닔??洹쒕え? 留ㅻ걚?ъ슫 怨≪꽑???④퍡 留뚮뱾 ???덈떎.
- evidence_boundary(洹쇨굅 寃쎄퀎): research_development_only(?곌뎄媛쒕컻 ?꾩슜), selected_candidate=none.

## stage306_anti_surface_trade_shape

- hypothesis(가설): actual MT5(메타트레이더5) trade-shape attribution(거래 형태 기여도) can create a larger smoother candidate than direction-flip repair.
- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).

## run306C_review_anti_surface_trade_shape_mt5_probe_v1 anti-surface trade-shape source(반표면 거래 형태 원천)

- idea_id(아이디어 ID): `stage306_anti_surface_trade_shape`
- hypothesis(가설): actual MT5(메타트레이더5) trade-shape attribution(거래 형태 기여도)이 direction flip(방향 반전)보다 큰 수익 원천을 만들 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## stage307_post_trade_shape_scale_ml

- hypothesis(가설): fresh ML return-rank(새 머신러닝 수익 순위) surface(표면)가 Stage306(306단계) rule repair(규칙 수리)보다 큰 profit scale(수익 규모)을 만들 수 있다.
- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).

## run307C_review_post_trade_shape_scale_mt5_probe_v1 anti-surface trade-shape source(반표면 거래 형태 원천)

- idea_id(아이디어 ID): `stage307_post_trade_shape_scale_ml`
- hypothesis(가설): actual MT5(메타트레이더5) trade-shape attribution(거래 형태 기여도)이 direction flip(방향 반전)보다 큰 수익 원천을 만들 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## stage308_non_return_rank_profit_source

- hypothesis(가설): non-return-rank(비수익순위) state/rule source(상태/규칙 원천)가 Stage307(307단계) return-rank(수익 순위) 실패 이후 수익 규모와 곡선을 동시에 회복할 수 있다.
- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).

## run308C_review_non_return_rank_profit_source_mt5_probe_v1 non-return-rank profit source(비수익순위 수익 원천)

- idea_id(아이디어 ID): `stage308_non_return_rank_profit_source`
- hypothesis(가설): return-rank(수익 순위)를 직접 쓰지 않는 session/breadth/volatility/trend(세션/브레드스/변동성/추세) 원천이 더 좋은 수익 곡선을 만들 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## stage309_split_coherent_profit_curve_source

- hypothesis(가설): split-coherent profit curve source(분할 일관 수익 곡선 원천)가 OOS upside(표본외 상방)와 validation curve stability(검증 곡선 안정성)를 동시에 만들 수 있다.
- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).

## run309C_review_split_coherent_profit_curve_source_mt5_probe_v1 split-coherent profit curve source(분할 일관 수익 곡선 원천)

- idea_id(아이디어 ID): `stage309_split_coherent_profit_curve_source`
- hypothesis(가설): split coherence(분할 일관성)를 강제하면 validation/OOS(검증/표본외) 양수 조각을 동시에 만들 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## stage310_runtime_positive_fragment_allocation

- hypothesis(가설): Stage309(309단계)의 runtime positive fragments(런타임 양수 조각)를 allocation layer(배분 계층)로 묶으면 거래수와 곡선 품질이 같이 개선될 수 있다.
- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).

## run310C_review_runtime_positive_fragment_allocation_mt5_probe_v1 runtime_positive_fragment_allocation(런타임 양수 조각 배분)

- idea_id(아이디어 ID): `stage310_runtime_positive_fragment_allocation`
- hypothesis(가설): 양수 조각을 배분하면 거래수와 곡선 품질이 함께 개선될 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## stage311_post_allocation_fresh_edge

- hypothesis(가설): Stage310(310단계)의 validation loss(검증 손실) 시간 구조를 adverse-hour mirror(불리 시간대 방향 반전)로 바꾸면 새 edge(엣지)가 될 수 있다.
- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).

## run311C_review_post_allocation_fresh_edge_mt5_probe_v1 post_allocation_fresh_edge(배분 이후 새 엣지)

- idea_id(아이디어 ID): `stage311_post_allocation_fresh_edge`
- hypothesis(가설): 불리 시간대 방향 반전과 피처 지원이 검증 손실을 줄일 수 있다.
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run312A_design_fresh_model_asymmetry_rebuild_packet_v1 fresh_model_asymmetry(새 모델 비대칭)

- idea_id(아이디어 ID): `stage312_fresh_model_asymmetry`
- hypothesis(가설): actual hour-direction memory(실제 시간-방향 기억)를 새 decision surface(판단 표면)로 쓰면 수익 규모와 밀도를 동시에 압박할 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run312C_review_fresh_model_asymmetry_mt5_probe_v1 fresh_model_asymmetry_review(새 모델 비대칭 검토)

- idea_id(아이디어 ID): `stage312_fresh_model_asymmetry_review`
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run313A_design_runtime_outcome_source_pivot_rebuild_packet_v1 runtime_outcome_source_pivot(런타임 결과 원천 전환)

- idea_id(아이디어 ID): `stage313_runtime_outcome_source_pivot`
- hypothesis(가설): actual hour-direction memory(실제 시간-방향 기억)를 새 decision surface(판단 표면)로 쓰면 수익 규모와 밀도를 동시에 압박할 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run313C_review_runtime_outcome_source_pivot_mt5_probe_v1 runtime_outcome_source_pivot_review(런타임 결과 원천 전환 검토)

- idea_id(아이디어 ID): `stage313_runtime_outcome_source_pivot_review`
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run314A_design_runtime_outcome_feature_source_rebuild_packet_v1 runtime_outcome_feature_source(런타임 결과 피처 원천)

- idea_id(아이디어 ID): `stage314_runtime_outcome_feature_source`
- hypothesis(가설): actual hour-direction memory(실제 시간-방향 기억)를 새 decision surface(판단 표면)로 쓰면 수익 규모와 밀도를 동시에 압박할 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run314C_review_runtime_outcome_feature_source_mt5_probe_v1 runtime_outcome_feature_source_review(런타임 결과 피처 원천 검토)

- idea_id(아이디어 ID): `stage314_runtime_outcome_feature_source_review`
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run315A_design_runtime_outcome_feature_interaction_rebuild_packet_v1 runtime_outcome_feature_interaction(런타임 결과 피처 상호작용)

- idea_id(아이디어 ID): `stage315_runtime_outcome_feature_interaction`
- hypothesis(가설): actual hour outcome(실제 시간별 결과)과 feature interaction(피처 상호작용)을 결합하면 trade density(거래 밀도)와 profit scale(수익 규모)을 같이 회복할 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run315C_review_runtime_outcome_feature_interaction_mt5_probe_v1 runtime_outcome_feature_interaction_review(런타임 결과 피처 상호작용 검토)

- idea_id(아이디어 ID): `stage315_runtime_outcome_feature_interaction_review`
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run316A_design_post_interaction_profit_scale_curve_rebuild_packet_v1 post_interaction_profit_scale_curve(상호작용 이후 수익 규모/곡선)

- idea_id(아이디어 ID): `stage316_post_interaction_profit_scale_curve`
- hypothesis(가설): 20/22시 sell-only(매도 전용) 시간 내부 샘플링이 거래수와 곡선을 같이 맞출 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run316C_review_post_interaction_profit_scale_curve_mt5_probe_v1 post_interaction_profit_scale_curve_review(상호작용 이후 수익 규모/곡선 검토)

- idea_id(아이디어 ID): `stage316_post_interaction_profit_scale_curve_review`
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run317A_design_fresh_non_time_profit_source_rebuild_packet_v1 fresh_non_time_profit_source(새 비시간 수익 원천)

- idea_id(아이디어 ID): `stage317_fresh_non_time_profit_source`
- hypothesis(가설): 시간 조건 없이 USDX/ADX/momentum/Bollinger(달러지수/ADX/모멘텀/볼린저) 상태 조합이 거래수와 수익 규모를 같이 만들 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run317C_review_fresh_non_time_profit_source_mt5_probe_v1 fresh_non_time_profit_source_review(새 비시간 수익 원천 검토)

- idea_id(아이디어 ID): `stage317_fresh_non_time_profit_source_review`
- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate=none.

## run318A_design_post_non_time_curve_stability_rebuild_packet_v1 post_non_time_curve_stability(비시간 이후 곡선 안정성)

- idea_id(아이디어 ID): `stage318_post_non_time_curve_stability`
- hypothesis(가설): Stage317(317단계) 실제 MT5(메타트레이더5) outcome(결과)을 비시간 feature surface(피처 표면)로 증류하면 trade count(거래 수), profit scale(수익 규모), curve stability(곡선 안정성)를 함께 회복할 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run318C_review_post_non_time_curve_stability_mt5_probe_v1 post_non_time_curve_stability(비시간 이후 곡선 안정성)

- idea_id(아이디어 ID): `stage318_post_non_time_curve_stability_actual_review`
- hypothesis(가설): Stage317(317단계) actual outcome(실제 결과)을 증류하면 수익 규모와 거래 밀도를 회복할 수 있다.
- result(결과): 수익 규모는 만들었으나 smooth curve(매끈한 곡선) 조건은 실패했다.
- survivor_seed_count(생존 씨앗 수): `2`
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run319A_design_curve_pocket_risk_asymmetry_rebuild_packet_v1 curve_pocket_risk_asymmetry(곡선 포켓 위험 비대칭)

- idea_id(아이디어 ID): `stage319_curve_pocket_risk_asymmetry`
- hypothesis(가설): Stage318(318단계) 수익 표면에서 변동성/추세 과열 구간을 줄이면 수익 규모와 4-10 trades/day(일 4-10거래)를 유지하면서 곡선 포켓을 줄일 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run319C_review_curve_pocket_risk_asymmetry_mt5_probe_v1 curve_pocket_risk_asymmetry_review(곡선 포켓 위험 비대칭 검토)

- idea_id(아이디어 ID): `stage319_curve_pocket_risk_asymmetry_actual_review`
- result(결과): profit scale(수익 규모)과 density(밀도)는 개선됐지만 validation pocket(검증 포켓)이 남았다.
- survivor_seed_count(생존 씨앗 수): `4`
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run320A_design_validation_pocket_drawdown_controller_packet_v1 validation_pocket_drawdown_controller(검증 포켓 드로다운 제어기)

- idea_id(아이디어 ID): `stage320_validation_pocket_drawdown_controller`
- hypothesis(가설): cp319D(319D 후보)의 validation pocket(검증 포켓)은 VIX/quality state(VIX/품질 상태)로 줄일 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.

## run321A_design_post_controller_profit_curve_rebuild_packet_v1 post_controller_profit_curve_source(제어기 이후 수익 곡선 원천)

- idea_id(아이디어 ID): `stage321_consensus_profit_curve_source`
- hypothesis(가설): Stage319(319단계)의 D/B/F/A/C/E 표면 합의와 합집합이 Stage320(320단계) 제어기보다 수익 규모와 곡선 균형을 더 잘 보존할 수 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.
## run322A_design_cp321b_curve_stability_pressure_packet_v1 cp321B curve stability pressure(cp321B 곡선 안정성 압박)

- idea_id(아이디어 ID): `stage322_cp321b_curve_stability_pressure`
- hypothesis(가설): cp321B(321B 씨앗)는 exact replay(정확 재생)와 threshold/source/risk perturbation(임계값/원천/위험 교란)을 견뎌야 Adapter(어댑터)로 넘길 가치가 있다.
- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.
| `IDEA-ST337-PROXY-NEGATIVE-OFFENSIVE-PIVOT` | `337_onnx_research_packet__cost_buffer_direction_curve_rebuild` | repeated HQ/HV proxy-negative ONNX(반복 HQ/HV 프록시 음수 ONNX) evidence suggests label horizon, side-specific, model-family, active-flat, and regime/context offensive pivot(라벨 기간/방향별/모델 계열/활성-관망/국면 문맥 공격 전환)이 필요하다 | `Tier A now + Tier B required next(Tier A 현재 + 다음 Tier B 필수)` | `opened_design_no_selection` | `run337HW_design_proxy_negative_trade_shape_offensive_pivot_without_db_v1` opens `run337HX_materialize_proxy_negative_trade_shape_offensive_pivot_inputs_without_db_v1`; selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성) 없음 |

## 2026-06-01 Stage338 Trade Lifecycle Repair Seed(거래 생명주기 수리 씨앗)

- idea(아이디어): proxy-reproduced signal(프록시 재현 신호)에 density throttle(밀도 제한), side loss quarantine(방향 손실 격리), cost-stress objective(비용 압박 목적)를 붙인다.
- source(원천): `run337JR_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_or_repair_without_db_v1`
- next_run(다음 실행): `run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_without_db_v1`
- effect(효과): 실패를 아이디어 사망으로 닫지 않고 새 offensive exploration seed(공격 탐색 씨앗)로 보존한다.

## 2026-06-01 Stage339 Lifecycle Exit Probe Review Seed(339단계 생명주기 청산 탐침 검토 씨앗)

- idea_id(아이디어 ID): `stage339_lifecycle_exit_probe_review_seed`
- hypothesis(가설): run338M(338M 실행)의 shorter hold(짧은 보유)와 side-balance(방향 균형) 변형은 MT5(메타트레이더5)에서 개선 단서를 줄 수 있지만, run338N(338N 실행) closeout(종료 기록)이 실패했으므로 먼저 근거 정체성을 검토해야 한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): run338M(338M 실행) 6개 lifecycle/exit(생명주기/청산) 변형.
- extreme_sweep(극단 탐색): close_on_flat(평탄 청산), shorter_hold(짧은 보유), asymmetric_long_relief(비대칭 롱 완화).
- micro_search_gate(미세 탐색 게이트): run339B(339B 실행)가 exact parity(정확 동등성), report identity(보고서 정체성), KPI floors(KPI 하한)를 검토해야 한다.
- wfo_plan(워크포워드 계획): runtime review(런타임 검토) 후 필요 시 별도 WFO(워크포워드 최적화) 단계로 분리한다.
- failure_memory(실패 기억): closeout helper recursion(종료 기록 도우미 재귀)은 코드/상태 문제로 기록하고, 원시 MT5(메타트레이더5) 숫자는 검토 전 단서로만 둔다.
- evidence_boundary(근거 경계): `runtime_probe_unreviewed_handoff(런타임 탐침 미검토 인계)`

## 2026-06-01 Stage339 Lifecycle Exit Probe Review Seed(339단계 생명주기 청산 탐침 검토 씨앗)

- idea_id(아이디어 ID): `stage339_lifecycle_exit_probe_review_seed`
- hypothesis(가설): run338M(338M 실행)의 shorter hold(짧은 보유)와 side-balance(방향 균형) 변형은 MT5(메타트레이더5)에서 개선 단서를 줄 수 있지만, run338N(338N 실행) closeout(종료 기록)이 실패했으므로 먼저 근거 정체성을 검토해야 한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): run338M(338M 실행) 6개 lifecycle/exit(생명주기/청산) 변형.
- extreme_sweep(극단 탐색): close_on_flat(평탄 청산), shorter_hold(짧은 보유), asymmetric_long_relief(비대칭 롱 완화).
- micro_search_gate(미세 탐색 게이트): run339B(339B 실행)가 exact parity(정확 동등성), report identity(보고서 정체성), KPI floors(KPI 하한)를 검토해야 한다.
- wfo_plan(워크포워드 계획): runtime review(런타임 검토) 후 필요 시 별도 WFO(워크포워드 최적화) 단계로 분리한다.
- failure_memory(실패 기억): closeout helper recursion(종료 기록 도우미 재귀)은 코드/상태 문제로 기록하고, 원시 MT5(메타트레이더5) 숫자는 검토 전 단서로만 둔다.
- evidence_boundary(근거 경계): `runtime_probe_unreviewed_handoff(런타임 탐침 미검토 인계)`

## 2026-06-01 Stage339B Shorter Hold Side-Balance Seed(짧은 보유 방향 균형 씨앗)

- idea_id(아이디어 ID): `stage339_shorter_hold_side_balance_expansion`
- hypothesis(가설): m02(엠02)의 hold=12(보유 12) 수익 구조를 유지하면서 short_threshold(숏 임계값)를 높이고 long_threshold(롱 임계값)를 약하게 낮추면 trade_count(거래수)와 side_balance(방향 균형)를 같이 개선할 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339B/run339C_queue.csv`
- extreme_sweep(극단 탐색): short_threshold(숏 임계값) 0.60, long_threshold(롱 임계값) 0.48 without close_on_flat(평탄 청산 없음)
- micro_search_gate(미세 탐색 게이트): MT5(메타트레이더5) exact parity(정확 동등성) and trade_count>=30(거래수 30 이상) with positive expectancy(기대값 양수)
- evidence_boundary(근거 경계): `reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)`

## 2026-06-01 Stage339B Shorter Hold Side-Balance Seed(짧은 보유 방향 균형 씨앗)

- idea_id(아이디어 ID): `stage339_shorter_hold_side_balance_expansion`
- hypothesis(가설): m02(엠02)의 hold=12(보유 12) 수익 구조를 유지하면서 short_threshold(숏 임계값)를 높이고 long_threshold(롱 임계값)를 약하게 낮추면 trade_count(거래수)와 side_balance(방향 균형)를 같이 개선할 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339B/run339C_queue.csv`
- extreme_sweep(극단 탐색): short_threshold(숏 임계값) 0.60, long_threshold(롱 임계값) 0.48 without close_on_flat(평탄 청산 없음)
- micro_search_gate(미세 탐색 게이트): MT5(메타트레이더5) exact parity(정확 동등성) and trade_count>=30(거래수 30 이상) with positive expectancy(기대값 양수)
- evidence_boundary(근거 경계): `reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)`

## 2026-06-01 Stage339E Quality Balance Blend Seed(품질-균형 혼합 씨앗)

- idea_id(아이디어 ID): `stage339_quality_balance_blend_after_split`
- hypothesis(가설): c01(씨01)의 profit quality(수익 품질)와 c07(씨07)의 side balance(방향 균형)는 min_margin(최소 마진)과 shorter hold(짧은 보유)를 섞으면 동시에 개선될 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): `stages/339_runtime_lifecycle_exit__side_balance_probe_review/02_runs/run339E/run339F_queue.csv`
- extreme_sweep(극단 탐색): long_threshold(롱 임계값) 0.46 with min_margin(최소 마진) 0.02, hold(보유) 10.
- micro_search_gate(미세 탐색 게이트): MT5(메타트레이더5) exact parity(정확 동등성), trade_count(거래수) >= 30, recovery_factor(회복 계수) >= 1.0.
- evidence_boundary(근거 경계): `reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)`

## 2026-06-01 Stage340 Quality Balance Pressure Review Seed(340단계 품질-균형 압박 검토 씨앗)

- idea_id(아이디어 ID): `stage340_quality_balance_pressure_review_seed`
- hypothesis(가설): run339G(339G 실행)의 f01(에프01) local MT5 clue(로컬 MT5 단서)가 pressure test(압박 시험)를 받을 가치가 있을 수 있다.
- source(원천): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- next_run(다음 실행): `run340B_review_quality_balance_blend_mt5_probe_without_db_v1`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- evidence_boundary(근거 경계): `runtime_probe_review_required_no_selection(런타임 탐침 검토 필요, 선정 없음)`
- effect(효과): 긍정 단서를 보존하되 Stage340(340단계)에서 새롭게 작게 판단한다.

## 2026-06-01 Stage340 Quality Balance Pressure Review Seed(340단계 품질-균형 압박 검토 씨앗)

- idea_id(아이디어 ID): `stage340_quality_balance_pressure_review_seed`
- hypothesis(가설): run339G(339G 실행)의 f01(에프01) local MT5 clue(로컬 MT5 단서)가 pressure test(압박 시험)를 받을 가치가 있을 수 있다.
- source(원천): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- next_run(다음 실행): `run340B_review_quality_balance_blend_mt5_probe_without_db_v1`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- evidence_boundary(근거 경계): `runtime_probe_review_required_no_selection(런타임 탐침 검토 필요, 선정 없음)`
- effect(효과): 긍정 단서를 보존하되 Stage340(340단계)에서 새롭게 작게 판단한다.

## 2026-06-01 Stage340B F01 Pressure Seed(340B F01 압박 씨앗)

- idea_id(아이디어 ID): `stage340_f01_local_floor_pressure`
- hypothesis(가설): f01(에프01)의 local floor pass(로컬 하한 통과)는 threshold/min_margin/hold(임계값/최소 마진/보유) 압박에서도 일부 유지될 수 있다.
- source(원천): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- next_run(다음 실행): `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1`
- broad_sweep(넓은 탐색): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340B/run340C_queue.csv`
- evidence_boundary(근거 경계): `reviewed_runtime_probe_no_selection(검토된 런타임 탐침, 선정 없음)`
- effect(효과): 긍정 단서를 다음 MT5(메타트레이더5) runtime probe(런타임 탐침)로 검증한다.

## 2026-06-01 Stage340E Corrected F01 Pressure Branch(340E 수정 F01 압박 분기)

- idea_id(아이디어 ID): `stage340_f01_close_on_flat_false_pressure_repair`
- hypothesis(가설): source f01(원본 f01)의 close_on_flat=False(평탄 청산 꺼짐) 의미를 복구하면 local floor(로컬 하한) 단서가 다시 보일 수 있다.
- source(원천): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1` and `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1`
- next_run(다음 실행): `run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/run340F_queue.csv`
- effect(효과): 무거운 Stage340(340단계)을 새 대형 stage(단계)가 아니라 좁은 corrected branch(수정 분기)로 이어간다.

## 2026-06-01 Stage340E Corrected F01 Pressure Branch(340E 수정 F01 압박 분기)

- idea_id(아이디어 ID): `stage340_f01_close_on_flat_false_pressure_repair`
- hypothesis(가설): source f01(원본 f01)의 close_on_flat=False(평탄 청산 꺼짐) 의미를 복구하면 local floor(로컬 하한) 단서가 다시 보일 수 있다.
- source(원천): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1` and `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1`
- next_run(다음 실행): `run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/run340F_queue.csv`
- effect(효과): 무거운 Stage340(340단계)을 새 대형 stage(단계)가 아니라 좁은 corrected branch(수정 분기)로 이어간다.

## 2026-06-01 Stage340H F01 Stability Cost Seed(340H F01 안정성 비용 씨앗)

- idea_id(아이디어 ID): `stage341_f01_stability_cost_regime_validation`
- hypothesis(가설): q01 exact control(정확 대조)과 q09 net-high clue(순수익 높은 단서)가 cost/session/regime(비용/세션/국면) 압박에서도 버티면 promotion_candidate(승격 후보) 비교 가치가 생긴다.
- source(원천): `run340H_review_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`
- next_run(다음 실행): `run341A_branch_stage340_to_f01_stability_cost_regime_validation_without_db_v1`
- seed_queue(씨앗 대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/run341A_seed_queue.csv`
- effect(효과): 긍정 단서를 운영 주장으로 과장하지 않고 다음 외부 검증 질문으로 넘긴다.

## 2026-06-01 run342A_branch_stage341_to_session_long_firewall_probe_without_db_v1 Session-long Firewall Branch(세션 롱 방화벽 분기)

- seed(씨앗): q01/q09(큐01/큐09)는 +1 cost stress(+1 비용 압박)를 버티지만 early session(초반 세션)과 long side(롱 방향)가 약하다.
- action(행동): early-long block(초반 롱 차단) side filter(사이드 필터)를 Stage 342(342단계) MT5 package/probe(MT5 패키지/탐침)로 분기한다.
- effect(효과): q09(큐09)를 winner(승자)로 고정하지 않고, q01/q09(큐01/큐09) 모두에 같은 firewall(방화벽) 질문을 던진다.
- claim_boundary(주장 경계): `state_sync_stage_branch_session_long_firewall_handoff_only_no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-01 Stage342D Soft Session-Long Firewall Seed(342D 부드러운 세션 롱 방화벽 씨앗)

- idea_id(아이디어 ID): `stage342_soft_session_long_firewall`
- hypothesis(가설): hard 0~110 early-long block(강한 0~110 초반 롱 차단)을 0~45 또는 0~75로 줄이면 PF(수익 팩터) 단서를 보존하면서 trade_count/side_balance(거래수/방향 균형)를 회복할 수 있다.
- source(원천): `run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1`
- next_run(다음 실행): `run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342D/run342E_soft_session_long_firewall_probe_queue.csv`
- effect(효과): 좋은 단서를 더 좁고 가벼운 탐색으로 이어간다.

## 2026-06-01 Stage342G Early Long Quality Margin Mix Seed(342G 초반 롱 품질/마진 혼합 씨앗)

- idea_id(아이디어 ID): `stage342_early_long_quality_margin_mix`
- hypothesis(가설): time-window pruning(시간 구간 절단)만으로 부족한 early-long filter(초반 롱 필터)는 long_threshold/min_margin(롱 임계값/최소 마진)과 결합하면 trade_count/side_balance(거래수/방향 균형)를 회복할 수 있다.
- source(원천): `run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1`
- next_run(다음 실행): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342G/run342H_early_long_quality_margin_mix_queue.csv`
- effect(효과): 같은 시간 구간만 미세조정하지 않고 confidence surface(신뢰도 표면) 쪽으로 확장한다.

## 2026-06-01 run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1 Directional Long Quality Surface Branch(방향성 롱 품질 표면 분기)

- idea_id(아이디어 ID): `stage344_directional_long_quality_surface`
- hypothesis(가설): profit anchor(수익 앵커)의 short supply(숏 공급)는 보존하고, long entries(롱 진입)는 separate quality/regime surface(별도 품질/국면 표면)로 다시 분리하면 trade shape(거래 형태)를 회복할 수 있다.
- source(원천): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- next_run(다음 실행): `run344B_design_directional_long_supply_quality_surface_without_db_v1`
- queue(대기열): `stages/344_directional_long_quality__supply_surface_probe/02_runs/run344A/run344B_directional_long_supply_quality_surface_queue.csv`
- effect(효과): minute block micro-tuning(분 차단 미세조정)을 반복하지 않고 long quality source(롱 품질 원천)를 새로 찾는다.
- claim_boundary(주장 경계): `state_sync_stage_branch_directional_long_quality_surface_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-01 run344C_materialize_directional_long_supply_quality_surface_package_without_db_v1 Directional Long Quality Runtime Mapping(방향성 롱 품질 런타임 매핑)

- idea_id(아이디어 ID): `stage344_directional_long_quality_surface`
- action(행동): rank/regime/exit ideas(순위/국면/청산 아이디어)를 EA-supported runtime mapping(EA 지원 런타임 매핑)으로 만들었다.
- effect(효과): MT5 runtime probe(MT5 런타임 탐침)에서 실행 가능한 candidate surface(후보 표면)가 생겼다.
- next_run(다음 실행): `run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1`
- claim_boundary(주장 경계): `research_development_directional_long_quality_surface_runtime_probe_package_only_no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## run344E s07 Trend Confirmed Long(추세 확인 롱)

- idea(아이디어): low-ADX long veto(낮은 ADX 롱 거부)를 활용한 trend-confirmed long(추세 확인 롱).
- evidence(근거): MT5 net profit(순수익) `186.67`, PF(수익 팩터) `4.11`, trades(거래수) `26`.
- effect(효과): 다음 cost/session/regime validation(비용/세션/국면 검증)의 씨앗으로 사용.

## run344E s07 Trend Confirmed Long(추세 확인 롱)

- idea(아이디어): low-ADX long veto(낮은 ADX 롱 거부)를 활용한 trend-confirmed long(추세 확인 롱).
- evidence(근거): MT5 net profit(순수익) `186.67`, PF(수익 팩터) `4.11`, trades(거래수) `26`.
- effect(효과): 다음 cost/session/regime validation(비용/세션/국면 검증)의 씨앗으로 사용.

## run344F s07 Validation Seed(s07 검증 씨앗)

- idea(아이디어): s07 trend-confirmed long(추세 확인 롱)을 비용/세션/국면/전진 인계 검증으로 압박한다.
- effect(효과): 좋은 단서를 운영 승격으로 과장하지 않고 검증 work packet(작업 묶음)으로 넘긴다.

## 2026-06-01 run344L Idea Seed(아이디어 씨앗)

- idea(아이디어): cash-open long quality and short-carry decomposition(현금장 초반 롱 품질과 숏 기여 분해)
- source_run(원천 실행): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- effect(효과): s07 수익 집중을 다음 공격 탐색의 설계 질문으로 바꾼다.

## 2026-06-01 run344L Idea Seed(아이디어 씨앗)

- idea(아이디어): cash-open long quality and short-carry decomposition(현금장 초반 롱 품질과 숏 기여 분해)
- source_run(원천 실행): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- effect(효과): s07 수익 집중을 다음 공격 탐색의 설계 질문으로 바꾼다.

| `IDEA-ST346-CASH-OPEN-ASYMMETRIC-SOURCE-PIVOT` | `346_cash_open_runtime_review__asymmetric_source_pivot` | run345B(345B 실행)의 exact runtime parity(정확 런타임 동등성)와 long/short imbalance(롱/숏 불균형)는 asymmetric model/source split(비대칭 모델/원천 분리)로 회수할 수 있다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `opened_research_development_only` | run346A(346A 실행)가 Stage346(346단계)을 열었고 run346B(346B 실행)가 review/source pivot(검토/원천 전환)을 수행한다. selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST347-CASH-OPEN-ASYMMETRIC-LONG-SHORT-SOURCE` | `347_cash_open_asymmetric_source__long_short_head_design` | run346B(346B 실행)의 long-quality and short-carry fragments(롱 품질과 숏 기여 조각)를 separate source/head(분리 원천/헤드)로 설계하면 수익과 균형을 같이 회복할 수 있다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `opened_research_development_only` | next_action(다음 행동) `run347A_design_cash_open_asymmetric_long_short_source_without_db_v1`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST347-RUN347A-ASYMMETRIC-SOURCE-DESIGN` | `347_cash_open_asymmetric_source__long_short_head_design` | asymmetric long/short source design(비대칭 롱/숏 원천 설계) `3`개를 materialization queue(물질화 대기열)로 만든다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `design_ready_no_selection` | next_action(다음 행동) `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`; model training(모델 학습), MT5 execution(MT5 실행), selection(선정), ONNX readiness(온엑스 준비) 없음 |

| `IDEA-ST347-RUN347B-ASYMMETRIC-SOURCE-INPUTS` | `347_cash_open_asymmetric_source__long_short_head_design` | asymmetric source teacher labels and proxy grid(비대칭 원천 교사 라벨과 프록시 격자)을 물질화한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `materialized_no_selection` | rows(행) `5827`, proxy_grid(프록시 격자) `225`; next_action(다음 행동) `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`; model training(모델 학습), MT5 execution(MT5 실행), selection(선정) 없음 |

| `IDEA-ST347-RUN347C-ASYMMETRIC-SOURCE-PROXY-TRAINING` | `347_cash_open_asymmetric_source__long_short_head_design` | asymmetric source teacher labels(비대칭 원천 교사 라벨)을 proxy allocator/heads(프록시 배분기/헤드)로 증류한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `proxy_training_completed_no_selection` | next_action(다음 행동) `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`; ONNX smoke(온엑스 점검)는 runtime authority(런타임 권위)가 아님 |

## 2026-06-01 Stage348 Proxy Review Triage Seed(프록시 검토 분류 씨앗)

- idea(아이디어): run347C proxy training(347C 프록시 학습)을 바로 후보로 올리지 않고, long OOS gap(롱 표본외 공백)과 short carry reconstruction(숏 기여 재구성)을 분리해 가장 작은 MT5 probe seed(MT5 탐침 씨앗)만 남긴다.
- source(원천): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- next_run(다음 실행): `run348B_review_cash_open_asymmetric_proxy_training_without_db_v1`
- effect(효과): Stage347(347단계)의 무거운 학습 산출물을 다시 끌고 다니지 않고 review/triage(검토/분류) 질문으로 전환한다.
- claim_boundary(주장 경계): `state_sync_stage_branch_proxy_review_handoff_only_no_new_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-01 run348B ONNX Short-Carry Probe Seed(온엑스 숏 기여 탐침 씨앗)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- idea(아이디어): ONNX deployable(온엑스 배포 가능) allocator(배분기) 중 logistic_balanced/ExtraTrees(로지스틱/엑스트라트리)의 test q95/q90 threshold(테스트 q95/q90 임계값)를 MT5 probe package(MT5 탐침 패키지)로 보낸다.
- seed_rows(씨앗 행): `4`
- effect(효과): 약한 프록시를 후보로 승격하지 않고 runtime evidence(런타임 근거)로만 확인한다.
- claim_boundary(주장 경계): `research_development_proxy_review_triage_only_no_new_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-01 run348B ONNX Short-Carry Probe Seed(온엑스 숏 기여 탐침 씨앗)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- idea(아이디어): ONNX deployable(온엑스 배포 가능) allocator(배분기) 중 logistic_balanced/ExtraTrees(로지스틱/엑스트라트리)의 test q95/q90 threshold(테스트 q95/q90 임계값)를 MT5 probe package(MT5 탐침 패키지)로 보낸다.
- seed_rows(씨앗 행): `4`
- effect(효과): 약한 프록시를 후보로 승격하지 않고 runtime evidence(런타임 근거)로만 확인한다.
- claim_boundary(주장 경계): `research_development_proxy_review_triage_only_no_new_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-01 run348C ONNX Short-Carry MT5 Probe Package(온엑스 숏 기여 MT5 탐침 패키지)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- idea(아이디어): ONNX deployable allocator(온엑스 배포 가능 배분기)를 실제 MT5 probe(탐침)로 관찰한다.
- attempts(시도): `4`
- effect(효과): weak proxy short signal(약한 프록시 숏 신호)을 selection(선정)이 아니라 runtime evidence(런타임 근거)로 확인하게 한다.
- claim_boundary(주장 경계): `research_development_runtime_probe_package_only_onnx_deployable_short_carry_feature_order_53_boundary_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## 2026-06-01 run348C ONNX Short-Carry MT5 Probe Package(온엑스 숏 기여 MT5 탐침 패키지)

- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- idea(아이디어): ONNX deployable allocator(온엑스 배포 가능 배분기)를 실제 MT5 probe(탐침)로 관찰한다.
- attempts(시도): `4`
- effect(효과): weak proxy short signal(약한 프록시 숏 신호)을 selection(선정)이 아니라 runtime evidence(런타임 근거)로 확인하게 한다.
- claim_boundary(주장 경계): `research_development_runtime_probe_package_only_onnx_deployable_short_carry_feature_order_53_boundary_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## stage351_no_scaler_or_1d_scaler_softmax_trade_surface

- hypothesis(가설): Stage350E(350E 실행)에서 통과한 단순 ONNX(온엑스) 계약이면 거래 표면을 다시 만들 수 있다.
- evidence_boundary(근거 경계): scout_and_handoff_only(스카우트 및 인계 전용)

| `IDEA-ST355-DENSITY-RECOVERY-LABEL-MODEL-SOURCE` | `355_density_recovery_model_family__new_label_source_probe` | existing surface(기존 표면)의 threshold/horizon/filter(임계값/보유기간/필터) 회수가 실패했으므로, 새 label/source/model family(라벨/원천/모델 계열)로 trade/day(일별 거래수) 3+와 net/PF/stress(순수익/수익 팩터/압박)를 동시에 회복한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `opened_research_development_only` | next_action(다음 행동) `run355A_design_density_recovery_label_model_source_without_db_v1`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST355A-DENSITY-RECOVERY-DESIGN-QUEUE` | `355_density_recovery_model_family__new_label_source_probe` | Stage354C(354C 실행)의 existing surface failure(기존 표면 실패)를 새 label/source/model family(라벨/원천/모델 계열) 설계 큐로 전환해 trade/day(일별 거래수) 3+와 cost stress(비용 압박)를 회복한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `design_queue_ready_no_selection` | next_action(다음 행동) `run355B_materialize_density_recovery_label_inputs_without_db_v1`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST355B-LABEL-MATERIALIZATION-TRAINING-QUEUE` | `355_density_recovery_model_family__new_label_source_probe` | timestamp-safe label variants(시점 안전 라벨 변형)를 물질화해 Stage355C(355C 실행) proxy model training(프록시 모델 학습)으로 보낸다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `materialized_training_queue_ready_no_selection` | next_action(다음 행동) `run355C_train_density_recovery_proxy_models_without_db_v1`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST356-DENSITY-RECOVERY-PROXY-TRAINING` | `356_density_recovery_training__proxy_model_queue_scout` | Stage355B(355B 실행)의 timestamp-safe label variants(시점 안전 라벨 변형) 4개를 proxy model training(프록시 모델 학습)으로 밀어 trade/day(일별 거래수) 3+와 stress net(압박 순수익)을 동시에 회복한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `stage_branch_opened_no_selection` | next_action(다음 행동) `run356B_train_density_recovery_proxy_models_without_db_v1`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |

| `IDEA-ST357-HIGH-DENSITY-LABEL-PIVOT` | `357_high_density_label_pivot__trade_frequency_recovery` | H12 train-quantile high-density label(학습 분위수 고밀도 H12 라벨)이 trade/day(일별 거래수) 3+와 positive stress PF(양수 압박 수익 팩터)를 동시에 회복하는지 탐색한다. | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)` | next_action(다음 행동) `run357B_design_high_density_label_pivot_without_db_v1`; operating claim(운영 주장) 없음 |

| `IDEA-ST360-REGIME-STABILITY-PIVOT` | `360_regime_stability_pivot__oos_long_cash_edge_validation_loss` | q05 OOS long/cash edge(q05 표본외 롱/현금장 우위)를 validation loss(검증 손실), late-session loss(후반 세션 손실), monthly instability(월별 불안정), cost fragility(비용 취약성)를 통제하면서 보존할 수 있는지 탐색한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)` | next_action(다음 행동) `run360A_design_regime_stability_pivot_without_db_v1`; operating claim(운영 주장), runtime authority(런타임 권위), Goal Achieve(목표 달성) 없음 |

| `IDEA-ST360A-REGIME-STABILITY-DESIGN-QUEUE` | `360_regime_stability_pivot__oos_long_cash_edge_validation_loss` | q05 OOS long/cash clue(q05 표본외 롱/현금장 단서)를 side/session/regime/cost rule stack(방향/세션/국면/비용 규칙 묶음)으로 넓게 물질화하면 validation/OOS stability(검증/표본외 안정성)를 회복할 수 있다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `design_ready_no_selection(설계 준비, 선택 없음)` | next_action(다음 행동) `run360B_materialize_regime_stability_pivot_inputs_without_db_v1`; operating claim(운영 주장), runtime authority(런타임 권위), Goal Achieve(목표 달성) 없음 |

## IDEA-ST360B-REPORT-DERIVED-FILTER-SCORECARDS

- idea(아이디어): Stage359B MT5 report(보고서)를 closed-trade diagnostic scorecard(종료 거래 진단 점수표)로 분해해 long/cash, late veto, side firewall clue(롱/현금장, 후반 제외, 방향 방화벽 단서)를 검토한다.
- hypothesis(가설): OOS positive clue(표본외 긍정 단서)는 session/side/cost(세션/방향/비용) 분해 뒤에야 proxy(프록시) 또는 MT5 replay(MT5 재생) 대상으로 판단할 수 있다.
- evidence_boundary(근거 경계): report_derived_materialization_only(보고서 파생 구체화 전용).
- next_action(다음 행동): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`.

## IDEA-ST361-LONG-ONLY-COST-BUFFER

- idea(아이디어): q05 long-only(롱 단독) edge(우위)에 margin/regime/label(마진/국면/라벨) 필터를 더해 +0.30 cost buffer(+0.30 비용 버퍼)를 회복한다.
- hypothesis(가설): short removal(숏 제거)은 validation/OOS(검증/표본외)를 양수로 만들지만 cost stress(비용 압박)가 부족하므로, long-only quality margin(롱 단독 품질 마진)이 필요하다.
- evidence_boundary(근거 경계): report-derived review seed(보고서 파생 검토 씨앗).
- next_action(다음 행동): `run361A_design_long_only_cost_buffer_probe_without_db_v1`.

## IDEA-ST361A-Q05-LONG-ONLY-MARGIN-REGIME-LABEL

- idea(아이디어): q05 long-only(롱 단독) margin/regime/label(마진/국면/라벨) 설계로 +0.30 cost buffer(+0.30 비용 버퍼)를 회복한다.
- hypothesis(가설): Stage360C(360C 실행)의 비용 전 검증/표본외 양수 단서는 margin gap(마진 gap), regime router(국면 라우터), cost-aware label(비용 인식 라벨)을 통해 비용 후에도 보존될 수 있다.
- evidence_boundary(근거 경계): design_only(설계 전용).
- next_action(다음 행동): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`.

## IDEA-ST362-Q05-LONG-ONLY-MARGIN-GRID

- idea(아이디어): q05 long-only(롱 단독) margin grid(마진 격자)를 먼저 구체화해 +0.30 cost buffer(+0.30 비용 버퍼) 가능 표면을 찾는다.
- hypothesis(가설): broad margin surface(넓은 마진 표면)가 validation/OOS(검증/표본외) 모두에서 비용 후 양수를 만들면 regime/label(국면/라벨) 복잡도를 붙일 가치가 생긴다.
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`
- next_action(다음 행동): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`

## IDEA-ST362B-Q05-LONG-ONLY-MARGIN-GRID-MATERIALIZATION

- idea(아이디어): q05 long-only(롱 단독) open-time probability margin(진입 시점 확률 마진)으로 비용 버퍼 표면을 찾는다.
- evidence(근거): Stage362B(362B 실행) 35개 grid(격자)에서 validation/OOS +0.30 cost and density gate(검증/표본외 +0.30 비용 및 밀도 게이트) 동시 통과 `0`.
- salvage_value(회수 가치): sparse cost-positive pockets(희소 비용 양수 구간)는 있으나 density collapse(밀도 붕괴)가 커서 lower-floor/rank/regime(낮은 하한/순위/국면) 공격 탐색 씨앗으로만 사용한다.
- next_action(다음 행동): `run362C_review_q05_long_only_margin_grid_without_db_v1`
- claim_boundary(주장 경계): `research_development_materialization_only_q05_long_only_margin_grid_report_derived_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## IDEA-ST362C-Q05-MARGIN-GRID-REVIEW

- idea(아이디어): q05 margin grid(q05 마진 격자)를 no-selection negative memory(선택 없음 부정 기억)로 검토한다.
- hypothesis(가설): Stage362B(362B 실행)의 sparse cost-positive pockets(희소 비용 양수 구간)는 candidate selection(후보 선택)이 아니라 lower-floor/rank seed(낮은 하한/순위 씨앗)이다.
- evidence_boundary(근거 경계): `review_only_no_new_mt5(검토 전용, 새 MT5 없음)`.
- next_action(다음 행동): `run363A_branch_stage362_to_lower_floor_rank_surface_without_db_v1`.
- claim_boundary(주장 경계): `research_development_review_only_q05_margin_grid_negative_memory_and_stage363_handoff_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## IDEA-ST363-Q05-LOWER-FLOOR-RANK-SURFACE

- idea(아이디어): lower p_long floor and validation-derived rank/quantile surface(낮은 p_long 하한 및 검증 파생 순위/분위수 표면).
- hypothesis(가설): density(밀도)를 보존하면서 validation cost drag(검증 비용 끌림)를 줄이는 표면이 absolute margin tightening(절대 마진 조임)보다 낫다.
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`.
- next_action(다음 행동): `run363B_materialize_q05_lower_floor_rank_surface_without_db_v1`.

## IDEA-ST363B-Q05-LOWER-FLOOR-RANK-MATERIALIZATION

- idea(아이디어): q05 lower-floor/rank surface(q05 낮은 하한/순위 표면)를 report-derived materialization(보고서 파생 구체화)로 평가한다.
- evidence(근거): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/lower_floor_rank_cross_split.csv`.
- result(결과): passing_cross_split_rows(교차 분할 통과 행) `0`.
- next_action(다음 행동): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`.
- claim_boundary(주장 경계): `research_development_materialization_only_q05_lower_floor_rank_surface_report_derived_validation_thresholds_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY

- idea(아이디어): timestamp-safe source/regime/label context(시점 안전 원천/국면/라벨 문맥)로 q05 dense cost(q05 고밀도 비용)를 회복한다.
- source_failure_memory(원천 실패 기억): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363C/failure_memory.csv`.
- design_queue(설계 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364A/run364B_design_queue.csv`.
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`.
- claim_boundary(주장 경계): `state_sync_stage_branch_source_regime_label_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364B-TIMESTAMP-CONTEXT-COST-SURFACE

- idea(아이디어): timestamp-safe context(시점 안전 문맥)로 q05 dense cost(q05 고밀도 비용)를 회복한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364B/timestamp_context_cross_split.csv`.
- result(결과): passing_cross_split_rows(교차 분할 통과 행) `33`.
- next_action(다음 행동): `run364C_review_timestamp_context_cost_surface_without_db_v1`.
- claim_boundary(주장 경계): `research_development_materialization_only_timestamp_context_cost_surface_validation_thresholds_report_derived_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364C-TIMESTAMP-CONTEXT-TRAINING-SEED

- idea(아이디어): Stage364B(364B)의 timestamp context pass rows(시점 문맥 통과 행)를 hard-coded rule(하드코딩 규칙)이 아니라 model feature/training seed(모델 피처/학습 씨앗)로 넘긴다.
- best_seed(최선 씨앗): `s364_r02_drop_worst_open_hour_minute_bucket15_k2`.
- seed_queue(씨앗 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364C/run364D_training_seed_queue.csv`.
- fragility_memory(취약성 기억): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364C/monthly_stability.csv`.
- claim_boundary(주장 경계): `research_development_review_only_timestamp_context_positive_scout_month_fragility_training_seed_handoff_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364D-TIMESTAMP-CONTEXT-TRAINING-SEED

- idea(아이디어): timestamp context(시점 문맥)를 hard-coded rule(하드코딩 규칙)이 아니라 cost-filter model training seed(비용 필터 모델 학습 씨앗)로 사용한다.
- training_seed_table(학습 씨앗 표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/timestamp_context_training_seed_table.csv`.
- feature_schema(피처 스키마): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/timestamp_context_feature_schema.json`.
- model_task_queue(모델 작업 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/run364E_model_task_queue.csv`.
- next_action(다음 행동): `run364E_train_timestamp_context_cost_filter_model_without_db_v1`.
- claim_boundary(주장 경계): `research_development_materialization_only_timestamp_context_training_seed_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364E-TIMESTAMP-CONTEXT-COST-FILTER-ONNX

- idea(아이디어): timestamp context(시점 문맥)를 ONNX-exportable cost-filter model(ONNX 변환 가능 비용 필터 모델)로 학습한다.
- best_onnx_model(최선 ONNX 모델): `rf_depth3_balanced` / `density_3_0`.
- validation_oos_read(검증/표본외 판독): validation_net(검증 순수익) `287.83`, oos_net(표본외 순수익) `78.86`.
- runtime_probe_queue(런타임 탐침 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364E/run364F_runtime_probe_queue.csv`.
- claim_boundary(주장 경계): `research_development_model_training_and_onnx_export_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364F-TIMESTAMP-CONTEXT-ONNX-RUNTIME-PROBE

- idea(아이디어): timestamp context(시점 문맥) cost-filter score(비용 필터 점수)를 MT5 long threshold(MT5 롱 임계값)로 실행한다.
- package(패키지): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364F/runtime_probe_attempt_package.csv`.
- expected_tape(예상 테이프): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364F/expected_probability_tapes/timestamp_context_expected_probability_tape.csv`.
- next_action(다음 행동): `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`.
- claim_boundary(주장 경계): `research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364H-DENSE-M5-SOURCE-RUNTIME-REPAIR

- idea(아이디어): sparse event tape(희소 이벤트 테이프)를 dense M5 source(고밀도 M5 원천)와 calendar exit semantics(캘린더 청산 의미)로 수리한다.
- hypothesis(가설): ONNX handoff(ONNX 인계)는 맞으므로 signal source density(신호 원천 밀도)와 runtime exit(런타임 청산)를 바꾸면 trade/day(일별 거래수) 3+와 MT5 net positive(MT5 순수익 양수)를 다시 시험할 수 있다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/review_findings.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/failure_memory.csv`.
- next_action(다음 행동): `run364I_design_runtime_failure_repair_offensive_queue_without_db_v1`.
- claim_boundary(주장 경계): `research_development_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364I-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT

- idea(아이디어): q05 probability bridge(q05 확률 연결)와 sparse long cost filter(희소 롱 비용 필터)를 벗어나 processed dense M5 features(처리 고밀도 M5 피처)로 직접 ONNX(온엑스) 모델을 학습한다.
- hypothesis(가설): dense direct return label(고밀도 직접 수익 라벨)이 OOS edge(표본외 우위)를 더 넓게 만든다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): logreg/rf/extra-trees shallow ONNX(로지스틱/랜덤포레스트/엑스트라트리 얕은 ONNX), long-only/two-sided(롱 전용/양방향), trade/day 3/5/7/10.
- extreme_sweep(극단 탐색): all-M5 dense control(전체 M5 고밀도 대조), q05-free source(q05 제거 원천), no-18-hour veto(18시 제외).
- micro_search_gate(미세 탐색 게이트): validation+OOS proxy(검증+표본외 프록시) net>0, PF>=1.05, trade/day>=3.
- wfo_plan(WFO 계획): positive scout(긍정 탐색) 이후 WFO(walk-forward optimization, 워크포워드 최적화) 강화.
- failure_memory(실패 기억): run364I found cost-filter overlay OOS PF weak(run364I 비용 필터 덧씌우기 표본외 수익 팩터 약함).
- evidence_boundary(근거 경계): `scout_only(탐색 전용)`
- next_action(다음 행동): `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`

## IDEA-ST364J-DIRECT-DENSE-M5-RETURN-ONNX-SCOUT

- idea(아이디어): direct dense M5 return label(직접 고밀도 5분봉 수익 라벨)로 sparse tape(희소 테이프) 문제를 우회한다.
- best_model_id(최선 모델 ID): `all58__dense_h24_move8pts__rf_depth5_leaf80_n48`.
- best_oos_net(최선 표본외 순수익): `439.321`.
- runtime_probe_candidate_count(런타임 탐침 후보 수): `0`.
- claim_boundary(주장 경계): `research_development_direct_dense_m5_model_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## IDEA-ST364L-DENSITY-LIFT-TRADE-SHAPE-ONNX-SCOUT

- hypothesis(가설): h24 quality clue(24봉 품질 단서)와 h6 density clue(6봉 밀도 단서)를 shorter hold and exit policy(짧은 보유와 청산 정책)로 결합하면 3/day+(일 3회 이상) density(밀도)를 회복할 수 있다.
- legacy_relation(레거시 관계): `none(없음)`.
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B out_of_scope_by_claim(Tier A+B 주장 범위 밖)`.
- broad_sweep(넓은 탐색): `horizon_m5=[3,4,6,8,12]`, `target_density=[3,5,8,12]`, `policy=[long_only,two_sided,side_asym]`.
- extreme_sweep(극단 탐색): `target_density=[16,20]`, `hold_m5=[2,3]`, `cost_stress=[0.30,0.45,0.60]`.
- micro_search_gate(미세 탐색 게이트): validation/OOS density >= 3/day(검증/표본외 밀도 3/일 이상), net > 0(순수익 양수), PF >= 1.05(수익 팩터 1.05 이상).
- wfo_plan(WFO 계획): scout(탐색) 통과 후 WFO(워크포워드 최적화).
- evidence_boundary(근거 경계): `research_development_kpi_evidence_review_only_no_new_model_training_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1

- idea(아이디어): density-lift ONNX(밀도 상향 온엑스)를 MT5-native maxhold trade shape(MT5 원생 최대 보유 거래 형태)로 probe(탐침)한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364M_density_lift_trade_shape_onnx_runtime_probe_package.md`.
- boundary(경계): `research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`.

## run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1

- idea(아이디어): dense long-only ONNX(고밀도 롱 전용 온엑스) runtime probe(런타임 탐침)는 양수 수익 단서가 있다.
- failure memory(실패 기억): drawdown(낙폭), long-only(롱 전용), hold tail(보유 꼬리)는 promotion blocker(승격 차단)다.
- next seed(다음 씨앗): calendar hold cap(달력 보유 상한), drawdown tail exit(낙폭 꼬리 청산), short side balance(숏 방향 균형), regime/session filter(국면/세션 필터).

## run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1

- idea(아이디어): MT5 positive clue(MT5 긍정 단서)를 drawdown/hold/side-balance(낙폭/보유/방향 균형) labels(라벨)로 바꾸면 다음 ONNX(온엑스) 탐색의 손실 꼬리를 줄일 수 있다.
- failure_memory(실패 기억): long-only(롱 전용)와 hold tail(보유 꼬리)는 운영 차단이다.
- reopen_condition(재개 조건): run364Q proxy(프록시)가 trade/day(일 거래수) >= 3, net positive(순수익 양수), PF(수익 팩터)>1.15, drawdown(낙폭) 개선을 보이면 MT5 runtime probe(MT5 런타임 탐침)로 간다.

## run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1

- idea(아이디어): long-only positive clue(롱 전용 긍정 단서)에 risk overlay(위험 오버레이), hold cap(보유 상한), short router(숏 라우터)를 덧대 drawdown/side balance(낙폭/방향 균형)를 수리한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364Q_drawdown_side_balance_overlay_onnx_scout.md`.
- boundary(경계): proxy scout(프록시 탐색)이며 MT5 runtime probe(MT5 런타임 탐침) 전 운영 주장(operating claim, 운영 주장)은 없다.

## run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1

- idea(아이디어): risk overlay ONNX(위험 오버레이 온엑스)를 바로 실행하지 못하는 대신, current EA(현재 EA)가 지원하는 `adx_14` side filter(방향 필터)로 runtime probe(런타임 탐침)를 먼저 연다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364R_drawdown_side_balance_overlay_runtime_probe_package.md`.
- reopen_condition(재개 조건): run364S MT5 result(MT5 결과)가 PF(수익 팩터), drawdown(낙폭), trade density(거래 밀도)를 유지하면 full overlay ONNX composition(전체 오버레이 온엑스 합성)을 다시 시도한다.

## run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1

- idea(아이디어): ADX side filter(ADX 방향 필터)는 run364S(364S 실행)에서 MT5 net/PF/DD(순수익/수익 팩터/낙폭)를 개선했지만, density floor(거래 밀도 하한)와 long-only(롱 전용)를 동시에 고쳐야 한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364T_drawdown_side_balance_overlay_mt5_runtime_probe_review.md`.
- reopen_condition(재개 조건): run364U(364U 실행)에서 validation/combined density(검증/합산 밀도) >= 3/day(일 3회 이상)와 nonzero short route(0이 아닌 숏 라우트)를 timestamp-safe(시점 안전)하게 만들 때.

## run364U_materialize_density_side_balance_repair_inputs_without_db_v1

- idea(아이디어): ADX side filter(ADX 방향 필터)를 완화하고 max hold(최대 보유)를 줄이면 density floor(밀도 하한)를 회복하면서 drawdown clue(낙폭 단서)를 유지할 수 있다.
- positive clue(긍정 단서): `adx_block_min_40_0__maxhold_6` expected combined net/PF(예상 합산 순수익/수익 팩터) `727.563` / `1.240896634`.
- failure memory(실패 기억): proxy(프록시)일 뿐이며 MT5 runtime probe(MT5 런타임 탐침) 전에는 operating claim(운영 주장) 금지.

## run364V_train_density_side_balance_repair_onnx_scout_without_db_v1

- idea(아이디어): existing ONNX(기존 온엑스)의 short probability(숏 확률)를 runtime threshold(런타임 임계값)로 열면 long-only failure(롱 전용 실패)를 줄이면서 density(밀도)를 유지할 수 있다.
- positive clue(긍정 단서): `dual_pshort_0_45__adx_block_40_0__maxhold_8` proxy combined net/PF/density(프록시 합산 순수익/수익 팩터/밀도) `771.564` / `1.2218406503` / `3.2462462462`.
- boundary(경계): MT5 runtime probe(MT5 런타임 탐침) 전 operating claim(운영 주장) 없음.

- run364W_package_density_side_balance_repair_runtime_probe_without_db_v1: dual-side threshold + ADX long block(양방향 임계값 + ADX 롱 차단) moved from proxy(프록시) to runtime package(런타임 패키지); MT5 evidence(MT5 근거) still required(아직 필요).

- run364X_execute_density_side_balance_repair_mt5_runtime_probe_without_db_v1: MT5 runtime probe(MT5 런타임 탐침) produced proxy-vs-MT5 diff(프록시-MT5 차이) for dual-side threshold(양방향 임계값) candidate.

- run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1: density side-balance candidate(밀도 방향 균형 후보) became positive MT5 stress candidate(긍정 MT5 압박 후보); cost/session/drawdown stress(비용/세션/낙폭 압박) required.

## run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1

- idea(아이디어): session/account-state/short guardrails(세션/계좌상태/숏 가드레일)이 density(밀도)를 유지하면서 PF/DD(수익 팩터/낙폭)를 개선할 수 있다.
- positive clue(긍정 단서): `run364Y` MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수) `989.22` / `1.3` / `1081`.
- failure memory(실패 기억): simple filter proxy(단순 필터 프록시)는 sequence replay(순서 재생)와 MT5 runtime probe(MT5 런타임 탐침)를 대체하지 않는다.

## run364AA_train_density_side_balance_cost_session_stress_scout_without_db_v1

- idea(아이디어): session/account-state/short guardrails(세션/계좌상태/숏 가드레일)이 PF/DD(수익 팩터/낙폭)를 개선할 수 있다.
- positive clue(긍정 단서): selected proxy(선택 프록시) `maxhold6_density_control__ps0_45__adx40_0__hold6__none`.
- failure memory(실패 기억): proxy replay(프록시 재생)는 MT5 runtime probe(MT5 런타임 탐침)를 대체하지 않는다.

## run364AB_review_density_side_balance_cost_session_stress_scout_without_db_v1

- idea(아이디어): strict pass zero(엄격 통과 0)를 실패 기억으로 닫고 stress_zone_3(3번 압박 구간)을 density bridge(밀도 연결) 씨앗으로 재사용한다.
- positive clue(긍정 단서): best PF near-miss(최고 수익 팩터 근접 실패)가 있다.
- failure memory(실패 기억): density-only selection(밀도만 좋은 선택)은 PF/DD(수익 팩터/낙폭)를 악화한다.

## run364AC_materialize_pf_dd_near_miss_density_bridge_without_db_v1

- idea(아이디어): stress_zone_3(압박 구간 3)의 5거래 내외 밀도 부족을 timestamp-safe restoration(시점 안전 복원)으로 메운다.
- positive clue(긍정 단서): stress_zone_3/4(압박 구간 3/4)는 DD(낙폭)를 줄인다.
- failure memory(실패 기억): density-only(밀도 단독)는 PF/DD(수익 팩터/낙폭)를 악화한다.

## run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1

- idea(아이디어): near-miss density bridge(근접 실패 밀도 연결)를 top_n(상위 N개) 없이 고정 임계값으로 시험한다.
- positive clue(긍정 단서): selected proxy(선택 프록시) `stress3_restore_long_p0_42_adx35_0__ps0_45__adx40_0__hold8`.
- failure memory(실패 기억): top_n month ranking(월 전체 상위 N개 순위)은 timestamp-safe(시점 안전)가 아니므로 직접 재생 금지.

## run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1

- idea(아이디어): density-safe candidate(밀도 안전 후보)는 남기되 PF target(PF 목표) 전 package(패키지)는 금지한다.
- positive clue(긍정 단서): PF 1.27대와 DD 개선이 동시에 보인다.
- failure memory(실패 기억): PF 1.30 이상 후보는 밀도가 무너지는 경향이 있어 density bridge(밀도 연결)와 함께 시험해야 한다.

## run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1

- idea(아이디어): PF lift(PF 상승)와 density restore(밀도 복원)를 고정 임계값으로 동시에 시험한다.
- positive clue(긍정 단서): PF 1.3066 후보와 density 3.006 후보가 따로 존재한다.
- failure memory(실패 기억): PF만 올리면 density(밀도)가 무너지고, density만 지키면 PF(수익 팩터)가 부족하다.

## run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1

- idea(아이디어): PF lift(PF 상승)와 density restore(밀도 복원)를 고정 임계값으로 재생해 동시 통과 후보를 찾는다.
- positive clue(긍정 단서): selected proxy(선택 프록시) `selected_density_safe_control__ps0_45__floor0_0__hold8`.
- failure memory(실패 기억): MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장 금지.

## run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1

- idea(아이디어): 밀도 통과 후보를 패키지로 올리기 전에 PF/세션/방향 압박을 분해한다.
- positive clue(긍정 단서): 미국 현금장 핵심 세션은 롱/숏 모두 양수 PF 포켓을 보인다.
- failure memory(실패 기억): PF 통과 행은 밀도 3/day를 잃고, 밀도 통과 행은 PF 1.30을 못 넘는다.

## run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1

- idea(아이디어): 핵심 세션 양수 포켓과 프리마켓 숏 끌림을 분리해 PF와 밀도를 동시에 시험한다.
- positive clue(긍정 단서): us_cash_core(미국 현금장 핵심) 롱/숏은 모두 PF 1.31 이상이다.
- failure memory(실패 기억): PF 통과 씨앗은 밀도를 잃으므로 밀도 복원 규칙과 함께 시험해야 한다.

## run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1

- idea(아이디어): session/side policy(세션/방향 정책)로 premarket short drag(프리마켓 숏 끌림)를 줄이고 core session edge(핵심 세션 엣지)를 보존한다.
- positive clue(긍정 단서): selected proxy(선택 프록시) `selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8`.
- failure memory(실패 기억): MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장 금지.

## run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1

- idea(아이디어): PF-pass density-fail(PF 통과 밀도 실패) row(행)를 버리지 않고 density restore(밀도 복원) 공격 seed(씨앗)로 바꾼다.
- positive clue(긍정 단서): PF(수익 팩터) 1.30 이상 row(행)가 있으나 density(밀도)가 3/day 아래로 떨어진다.
- failure memory(실패 기억): density-safe(밀도 안전) control(대조)은 PF(수익 팩터) 목표 아래라 package(패키지)가 아니다.

## run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1

- idea(아이디어): PF-pass density-fail(PF 통과 밀도 실패) 씨앗을 core short(핵심 숏), late long(후반 롱), non-drag session(비끌림 세션) 복원 축으로 나눈다.
- effect(효과): PF(수익 팩터) 1.30과 density(밀도) 3/day를 동시에 요구하는 다음 정찰 입력을 만든다.

## run364AM_train_pf_pass_density_restore_offensive_scout_without_db_v1

- idea(아이디어): PF-pass density-fail(PF 통과 밀도 실패) 씨앗을 core short(핵심 숏), late long(후반 롱), non-drag session(비끌림 세션) 복원으로 시험한다.
- clue(단서): selected proxy(선택 프록시) `density_anchor_hold6_pf_probe_밀도_기준_보유6_PF_탐침__seed_selected_control_full_session_선택_대조_전체_세션_ps0_45_floor0_0_hold8__ps0_45__floor0_00__hold6`.
- failure memory(실패 기억): MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장 금지.

## run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1

- idea(아이디어): hold6 density(6봉 보유 밀도)와 sparse PF-pass(희소 PF 통과)를 분리해 다음 PF/DD repair(PF/DD 수리) 씨앗으로 쓴다.
- positive clue(긍정 단서): density(밀도) 회복은 가능하지만 PF/DD(수익 팩터/낙폭) 수리가 필요하다.
- failure memory(실패 기억): strict package(엄격 패키지)는 `0`이라 운영 주장 금지.

## run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1

- idea(아이디어): hold6 density(6봉 밀도) 씨앗과 sparse PF(희소 수익 팩터) 씨앗을 PF/DD repair(PF/DD 수리) 축으로 섞는다.
- effect(효과): PF(수익 팩터) 1.30, density(밀도) 3/day, DD(낙폭) 수리를 동시에 보는 다음 replay(재생) 입력을 만든다.

## run364AP_train_hold6_pf_dd_repair_offensive_scout_without_db_v1

- idea(아이디어): hold6 density(6봉 밀도)와 sparse PF(희소 수익 팩터) 수리 축을 proxy replay(프록시 재생)로 비교한다.
- effect(효과): PF(수익 팩터), density(밀도), DD(낙폭)를 동시에 보며 다음 검토로 넘긴다.

## run364AQ_review_hold6_pf_dd_repair_offensive_scout_without_db_v1

- idea(아이디어): threshold edge(임계값 경계)가 PF/DD를 동시에 조금 개선하지만 PF 1.30에는 부족하다.
- effect(효과): 보유 기간, 미세 하한, late-long blend(후반 롱 결합) 축으로 다음 공격 탐색을 연다.

## run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1

- idea(아이디어): threshold-edge(임계값 경계) 후보의 PF gap(PF 간극)을 hold compression(보유 압축), margin floor(마진 하한), late-long blend(후반 롱 혼합)로 줄인다.
- effect(효과): package(패키지) 실패를 idea-dead(아이디어 사망)로 닫지 않고 다음 proxy scout(프록시 정찰)로 넘긴다.

## run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1

- idea(아이디어): threshold-edge(임계값 경계) PF gap(PF 간극)을 보유 압축과 후반 롱 혼합으로 줄인다.
- hypothesis(가설): PF(수익 팩터) 1.30 접근이 density(밀도) 3/day 붕괴 없이 가능할 수 있다.
- effect(효과): proxy scout(프록시 정찰) 표면으로 다음 review(검토)가 package(패키지) 가능성과 실패 기억을 나눌 수 있게 한다.

## run364AT_review_threshold_edge_pf_gap_repair_scout_without_db_v1

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)이 PF(수익 팩터) 1.30과 density(밀도) 3/day를 동시에 회복한다.
- evidence(근거): proxy(프록시) net `862.283`, PF `1.3105654109`, density `3.1981981982`, DD `-133.571`.
- next_condition(다음 조건): MT5 runtime probe(MT5 런타임 탐침)에서 proxy/MT5 diff(프록시/MT5 차이)를 기록한다.

## run364AU_package_threshold_edge_floor001_runtime_probe_without_db_v1

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)의 PF lift(PF 개선)를 MT5 runtime(MT5 런타임)에서 확인한다.
- positive clue(긍정 단서): expected PF(예상 수익 팩터) `1.3105654109`, density(밀도) `3.1981981982`.
- failure memory(실패 기억): MT5 report/telemetry(MT5 보고서/기록) 전에는 runtime authority(런타임 권위) 금지.

## run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)의 PF lift(PF 개선)를 MT5 runtime(MT5 런타임)에서 확인한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AV/threshold_edge_floor001_mt5_probe_summary.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AV/proxy_mt5_runtime_difference.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AV/probability_runtime_difference.csv`
- boundary(경계): runtime authority(런타임 권위)는 not_claimed(주장 없음).

## run364AW_review_threshold_edge_floor001_mt5_runtime_probe_without_db_v1

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)은 MT5 net/PF(순수익/수익 팩터)를 유지했지만 density(밀도)는 실제 MT5에서 3/day 아래로 떨어졌다.
- positive clue(긍정 단서): net `878.55`, PF `1.36`, RF `6.75`, short net positive(숏 순수익 양수).
- failure memory(실패 기억): proxy density(프록시 밀도)는 통과했지만 MT5 density(메타트레이더5 밀도)가 실패했으므로 다음 후보는 proxy density buffer(프록시 밀도 완충)를 요구한다.

## run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1

- idea(아이디어): AW positive runtime clue(AW 긍정 런타임 단서)의 density miss(밀도 미달)를 proxy density buffer(프록시 밀도 완충), short-side restore(숏 방향 복원), session/month stress labels(세션/월 압박 라벨)로 복원한다.
- effect(효과): promotion-ineligible(승격 부적격)을 idea-dead(아이디어 사망)로 닫지 않고, 다음 공격 탐색 씨앗으로 전환한다.

## run364AY_train_threshold_edge_density_restore_cost_session_scout_without_db_v1

- idea(아이디어): threshold-edge floor001(임계값 경계 하한 0.001)의 net/PF(순수익/수익 팩터) 단서를 살리고 density(밀도)를 3/day(일 3회) 이상으로 복원한다.
- effect(효과): trade splitting(거래 쪼개기) 없이 entry_margin_floor(진입 마진 하한)와 short threshold(숏 임계값) 완화를 탐색했다.

## run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1

- idea(아이디어): stress pass(압박 통과) `ax03_short_restore_ps450_floor050_stress`를 candidate(후보)로 재물질화한다.
- effect(효과): package ineligible(패키지 부적격)을 idea-dead(아이디어 사망)로 닫지 않고 공격 탐색 씨앗으로 쓴다.

## run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1

- idea(아이디어): `ax03_short_restore_ps450_floor050_stress` stress pass(압박 통과)를 candidate(후보)로 재시험한다.
- effect(효과): package ineligible(패키지 부적격)을 공격 탐색 씨앗으로 바꾼다.

## run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1

- idea(아이디어): AZ stress pass(AZ 압박 통과)를 candidate(후보)로 바꿔 PF 1.25와 추정 MT5 밀도 3/day를 동시에 시험한다.
- effect(효과): package ineligible(패키지 부적격) 단서를 idea-dead(아이디어 사망)로 닫지 않고 공격 탐색으로 재사용한다.

## run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1

- idea(아이디어): `ba02_between_ax03_ax08_floor025_ps450` proxy candidate(프록시 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 확인한다.
- effect(효과): 프록시에서 보인 PF/density(PF/밀도) 구조를 실제 MT5 실행 의미로 압박한다.

- run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1: ba02 density restore stress candidate(ba02 밀도 복원 압박 후보)를 MT5 runtime package(MT5 런타임 패키지)로 이동했다. MT5 evidence(MT5 근거)는 아직 필요하다.

## run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1

- idea(아이디어): density restore stress candidate(밀도 복원 압박 후보)의 trade density(거래 밀도) 회복과 PF lift(PF 개선)를 MT5 runtime(MT5 런타임)에서 확인한다.
- evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/density_restore_stress_candidate_mt5_probe_summary.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/proxy_mt5_runtime_difference.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BE/probability_runtime_difference.csv`
- boundary(경계): runtime authority(런타임 권위)는 not_claimed(주장 없음).

## run364BF_review_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1

- idea(아이디어): density restore stress candidate(밀도 복원 압박 후보)는 MT5 net/PF/density(순수익/수익 팩터/밀도)를 유지했다.
- positive clue(긍정 단서): net `900.36`, PF `1.35`, density `3.0510510511`, clean parity(깨끗한 동등성).
- failure memory(실패 기억): long share(롱 비중) `0.9025590551`와 missing forward/regime evidence(전진/국면 근거 누락)가 운영 승격을 막는다.

## run364BG_materialize_density_restore_forward_regime_stress_inputs_without_db_v1

- idea(아이디어): BF positive runtime clue(BF 긍정 런타임 단서)를 forward-like block replay(전진 유사 블록 재생), month/hour/side soft firewall(月/시간/방향 소프트 방화벽), short restore(숏 복원)로 압박한다.
- positive clue(긍정 단서): MT5 net `900.36`, PF `1.35`, density `3.0510510511`.
- failure memory(실패 기억): long share(롱 비중) `0.9025590551`와 missing forward/regime evidence(전진/국면 근거 누락)는 운영 승격을 막는다.

## run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1

- idea(아이디어): hour19 closed-bar margin guard(19시 닫힌 봉 margin 가드)가 PF/DD(수익 팩터/낙폭)를 밀도 붕괴 없이 개선할 수 있다.
- positive clue(긍정 단서): selected net/PF/density `938.59` / `1.3732279833` / `3.012012012`.
- effect(효과): short balance(숏 균형)는 별도 source exploration(원천 탐색)으로 분리한다.

<!-- run364BI_h19_runtime_guard -->
- Idea(아이디어): generic hour/side/opposite-margin guard(범용 시간/방향/반대마진 가드). Seed(씨앗): `bh02_long_h19_margin_opp_0020`. Effect(효과): proxy clue(프록시 단서)를 MT5에서 같은 의미로 시험할 수 있게 한다.

<!-- run364BJ_h19_opposite_margin_runtime_guard -->
- Idea(아이디어): h19 opposite-margin runtime guard(19시 반대마진 런타임 가드). Effect(효과): proxy clue(프록시 단서)를 MT5에서 같은 의미로 시험 가능하게 한다.

## run364BK_review_h19_opposite_margin_runtime_probe_without_db_v1

- idea(아이디어): h19 opposite-margin guard(19시 반대마진 가드)가 MT5에서 BF 기준선보다 net/PF(순수익/수익 팩터)를 올리는지 검토한다.
- positive clue(긍정 단서): net `959.64`, PF `1.38`, density `3.021021021`, time-margin guard observed(시간-마진 가드 관측) `54`.
- failure memory(실패 기억): short share(숏 비중) `0.0984095427`, equity DD(평가손익 낙폭) `18.24%`, forward/cost stress missing(전진/비용 압박 누락).

## run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1

- idea(아이디어): h19 guard(h19 가드)의 MT5 net/PF/density(순수익/수익 팩터/밀도) 단서를 short source(숏 원천)와 equity DD stress(평가손익 낙폭 압박)로 분리한다.
- positive clue(긍정 단서): parent net/PF/density `959.64` / `1.38` / `3.021021021`.
- failure memory(실패 기억): short share(숏 비중) `0.0984095427`, equity DD(평가손익 낙폭) `18.24%`, density removable budget(삭제 가능 밀도 여유) `7`.

## run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1

- idea(아이디어): h17-20 short router(17~20시 숏 라우터)가 h19 guard(h19 가드)의 short balance(숏 균형)를 회복할 수 있다.
- positive clue(긍정 단서): selected proxy net/PF/density/short share `967.76` / `1.3650661562` / `3.1471471471` / `0.1440839695`.
- effect(효과): long delete(롱 삭제) 대신 new short source(새 숏 원천)를 다음 MT5 검토 후보로 만든다.

## run364BN_review_h19_stress_short_balance_proxy_scout_without_db_v1

- idea(아이디어): h17 core + h20 margin band(17시 핵심 + 20시 마진 밴드)가 BM의 음수 숏 원천을 양수 품질로 바꿀 수 있다.
- positive clue(긍정 단서): repair seed net/PF/density/short share `1037.17` / `1.4101564709` / `3.0750750751` / `0.1201171875`.
- effect(효과): 패키지 승격 대신 BO 공격 정찰로 이어간다.

## run364BO_train_short_source_quality_repair_scout_without_db_v1

- idea(아이디어): h17 core + h20 margin band(17시 핵심 + 20시 마진 밴드)는 BM negative short source(BM 음수 숏 원천)를 proxy(프록시) 단서로 수리할 수 있다.
- positive clue(긍정 단서): net/PF/density/short share `1037.17` / `1.4101564709` / `3.0750750751` / `0.1201171875`.
- caution(주의): month_bad_count(월 나쁨 수) `2`라서 package(패키지)는 BP 검토 전까지 닫는다.

## run364BP_review_short_source_quality_repair_scout_without_db_v1

- idea(아이디어): broad clean h17/h20 short source(넓은 클린 17/20시 숏 원천)와 overlap-safe h16 extension(겹침 안전 16시 확장)을 결합하면 short share(숏 비중)를 회복할 수 있다.
- positive clue(긍정 단서): bo90 net/PF(순수익/PF) `1044.49` / `1.4158388603`, bo05 synthetic short PF(합성 숏 PF) `2.8224308655`.
- next action(다음 행동): `run364BQ_train_broad_clean_short_share_lift_scout_without_db_v1`.

## run364BR_review_broad_clean_short_share_lift_scout_without_db_v1

- idea(아이디어): BQ h19 bridge(19시 브리지)는 short share(숏 비중)를 복구하는 positive clue(긍정 단서)지만 late-year stress(연말 압박)가 남는다.
- positive clue(긍정 단서): net/PF/density/short share `1047.85` / `1.4129932946` / `3.0870870871` / `0.1215953307`.
- next action(다음 행동): `run364BS_train_late_year_short_share_stress_repair_scout_without_db_v1`.

## run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1

- idea(아이디어): December h21 long suppression(12월 21시 롱 억제)은 proxy stress(프록시 압박)를 해소할 수 있지만 low-sample watch(소표본 관찰)가 필요하다.
- positive clue(긍정 단서): selected proxy(선택 프록시) net/PF/density/short share `1063.14` / `1.4220035161` / `3.0720720721` / `0.1221896383`.
- next action(다음 행동): `run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1`.

<!-- run364BU_late_year_session_gate -->
- Idea(아이디어): December h21 long suppression(12월 21시 롱 억제) as runtime calendar block(런타임 달력 차단). Effect(효과): low-sample proxy repair(소표본 프록시 수리)를 `.set` parameter(설정 파라미터)로 표현한다.

<!-- run364BV_synthetic_short_source -->
- Idea(아이디어): BQ/BS synthetic short source(합성 숏 원천)를 runtime overlay(런타임 덧씌움)로 표현한다. Effect(효과): proxy short share repair(프록시 숏 비중 수리)를 MT5 cost/fill(비용/체결)로 검증한다.

<!-- run364BW -->
- Idea(아이디어): hour17-only synthetic overlay(17시 한정 합성 덧씌움) + native short control(기본 숏 대조). Evidence(근거): BV overlay hour17 was positive while non-17 overlay dragged net(BV 덧씌움 17시는 양수, 비17시는 순수익 부담).

<!-- run364BX_overlay_hour17_ablation -->
- Idea(아이디어): hour17 overlay(17시 오버레이)와 native short(기본 숏)을 MT5 ablation(MT5 제거 비교)으로 분리한다. Effect(효과): synthetic short source(합성 숏 원천)가 실제 수익인지 churn(회전)인지 판별한다.

<!-- run364BY_bx03_december_late_session_guard -->
- Idea(아이디어): BX3 개선은 December h22 long guard(12월 22시 롱 가드)와 h17 overlay(17시 오버레이)를 분리해 더 검증한다. Effect(효과): net/PF(순수익/수익 팩터)를 유지하면서 equity DD(평가손익 낙폭)와 월 압박을 줄이는 다음 탐색으로 연결한다.

<!-- run364BZ_bx3_guard_inputs -->
- Idea(아이디어): BX3 개선을 December h22 calendar block(12월 h22 달력 차단), h17 overlay(17시 오버레이), native short control(기본 숏 대조)로 분리한다. Effect(효과): 다음 MT5 runtime probe(MT5 런타임 탐침)가 어떤 수익 원천을 검증하는지 선명해진다.

<!-- run364CA_bx3_guard_stack_runtime -->
- Idea(아이디어): December h22-only block(12월 h22 단독 차단), h21-h23 stress(h21-h23 압박), native short same-calendar control(같은 달력 기본 숏 대조)를 MT5 runtime probe(MT5 런타임 탐침)로 분리한다. Effect(효과): BX3 개선이 calendar semantics(달력 의미)인지 synthetic overlay(합성 오버레이)인지 더 선명하게 판별한다.

<!-- run364CB_swap_sensitive_guard_stack -->
- Idea(아이디어): BX3 guard stack(BX3 가드 묶음)은 trade path(거래 경로) 기준으로 유지되지만 net rank(순수익 순위)는 swap table(스왑표)에 민감하다. Effect(효과): 다음 탐색은 h17 synthetic overlay(17시 합성 오버레이)와 h21-h22 calendar block(h21-h22 캘린더 차단)을 보존하되, swap-stable reprobe(스왑 안정 재탐침)와 gross/net/cost 분리 평가를 같이 진행한다.

<!-- run364CC_swap_source_guard_handoff -->
- Idea(아이디어): BX3와 CA01의 trade path(거래 경로)가 같으므로 next runtime probe(다음 런타임 탐침)는 same-session swap stability(동일 세션 스왑 안정성)와 h17 synthetic overlay source value(17시 합성 오버레이 원천 가치)를 같이 본다. Effect(효과): 비용 드리프트와 원천 단서를 분리해 다음 공격 탐색을 덜 흐리게 만든다.

<!-- run364CD_swap_stable_source_guard_runtime -->
- Idea(아이디어): BX3 clone(BX3 복제), CA01 clone(CA01 복제), native short control(기본 숏 대조)을 같은 CD MT5 session(CD MT5 세션)에서 다시 실행한다. Effect(효과): swap drift(스왑 드리프트)인지 source overlay value(원천 오버레이 가치)인지 다음 리뷰에서 분리할 수 있다.

<!-- run364CE_cost_stable_h17_source_guard -->
- Idea(아이디어): current-session CA01/BX3 semantics(현재 세션 CA01/BX3 의미)를 stable source(안정 원천)로 쓰고, h17 synthetic overlay(17시 합성 오버레이)를 offensive seed(공격 씨앗)로 보존한다. Effect(효과): stale swap-table net(낡은 스왑표 순수익)에 끌리지 않고 source guard(원천 가드)를 확장한다.

### run364CF_materialize_cost_stable_h17_source_guard_offensive_inputs_without_db_v1 cost-stable h17 source guard offensive queue(비용 안정 17시 원천 가드 공격 대기열)

- idea_id(아이디어 ID): `IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY`
- hypothesis(가설): current-session cost-stable h17 source guard(현재 세션 비용 안정 17시 원천 가드)가 no-split scout(무분할 정찰)에서 PF/DD/source quality(PF/DD/원천 품질)를 개선할 수 있다.
- evidence_boundary(근거 경계): materialization_only(구체화 전용), no runtime authority(런타임 권위 없음).
- next(다음): `run364CG_train_cost_stable_h17_source_guard_offensive_scout_without_db_v1`.

## run364CH_review_cost_stable_h17_source_guard_offensive_scout_without_db_v1

- idea(아이디어): h17 overlay focus(17시 오버레이 집중)는 small net/PF lift(작은 순수익/PF 우위)를 만들지만 month/cost stress(월/비용 압박)를 해결해야 한다.
- positive clue(긍정 단서): net/PF/density/shorts `1001.5` / `1.3999745705` / `3.2070063694` / `104`.
- evidence_boundary(근거 경계): review only(검토 전용), no new MT5 execution(새 MT5 실행 없음).
- next action(다음 행동): `run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1`.

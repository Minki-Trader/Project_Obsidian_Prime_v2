# Stage19-32 Model Research Work Order(19-32단계 모델 연구 작업서)

path note(경로 메모): 파일 경로(file path, 파일 경로)는 기존 `stage19_25_model_research_work_order.md`를 유지한다. 효과(effect, 효과)는 이전 decision(결정)과 current truth(현재 진실) 링크를 깨지 않고 Stage26-32(26-32단계) 확장만 반영하는 것이다.

goal operating plan(목표 운영 계획): `docs/workspace/stage20_32_goal_operating_plan.md`

효과(effect, 효과): 이 작업서(work order, 작업지시서)의 단계 큐(stage queue, 단계 큐)는 Stage20-32(20-32단계) 목표 운영 계획의 closeout(마감), MT5 safety(메타트레이더5 안전), reporting/git(보고/깃) 규칙을 따른다.

## Current Queue Read(현재 큐 판독)

Stage19(19단계) EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)은 `closed_inconclusive_ebm_model_characteristics_exhausted`로 닫혔고, Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델)은 `run14A_gam_additive_shape_scout_v1` Python structural scout(파이썬 구조 탐색)를 완료한 상태다.

효과(effect, 효과): Stage20(20단계)은 EBM(설명가능 부스팅 머신) continuation(연속)이 아니라 smooth additive effect(부드러운 가산 효과)를 보는 새 topic pivot(주제 전환)으로 시작한다.

Stage26-32(26-32단계)는 Stage25(25단계) 이후 future queue(미래 큐)로 추가한다. NGBoost(`Natural Gradient Boosting`, 자연 그래디언트 부스팅), quantile boosting(분위수 부스팅), Markov regression(마르코프 회귀), online ML(`online machine learning`, 온라인 머신러닝), calibration(보정), TabNet(탭넷), TCN(`Temporal Convolutional Network`, 시간 합성곱 네트워크)을 각각 독립 주제로 둔다.

효과(effect, 효과): Stage20(20단계) 진행 순서는 바꾸지 않고, Stage25(25단계) 뒤에 탐색할 모델군과 decision layer(결정 계층) 질문을 미리 예약한다.

## Purpose(목적)

Stage18(18단계) CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트)는 닫고, Stage19-32(19-32단계)는 서로 다른 model family(모델군), regime(국면), risk lifecycle(위험 생애주기), decision layer(결정 계층), sequence(시퀀스) 질문으로 연다.

효과(effect, 효과): CatBoost(캣부스트), q85 threshold(q85 임계값), hold6(6봉 보유), selected variant(선택 변형)를 상속하지 않고, 각 단계가 독립 실험이 된다.

## Shared Controls(공통 통제)

- symbol/timeframe(심볼/시간프레임): `FPMarkets US100 M5`
- split/data surface(분할/데이터 표면): Stage18(18단계)과 같은 audited 58-feature MT5 price-proxy surface(감사된 58개 피처 MT5 가격 대리 표면)를 기본 후보로 쓴다.
- Tier records(티어 기록): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산)를 분리한다.
- MT5(`MetaTrader 5`, 메타트레이더5) claim(주장): runtime_probe(런타임 탐침)만 허용한다.
- forbidden inheritance(금지 상속): Stage18(18단계) CatBoost(캣부스트) model/threshold/variant/baseline(모델/임계값/변형/기준선)을 이어받지 않는다.

효과(effect, 효과): 모델 비교가 Stage18(18단계)의 좋은 구간을 좇는 식으로 왜곡되지 않는다.

## Tooling Readiness(도구 준비 상태)

2026-05-05(2026년 5월 5일) 기준 현재 Python(`Python`, 파이썬) 환경에는 Stage20-25(20-25단계) 모델군을 위한 전용 도구(dedicated tools, 전용 도구)를 준비했다. Stage26-32(26-32단계)는 planning readiness(계획 준비 상태)로만 둔다.

- Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델): `pygam==0.12.0`, `statsmodels==0.14.6`, scikit-learn(`scikit-learn`, 사이킷런) spline/logistic(스플라인/로지스틱)
- Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱): `scikit-learn==1.8.0`
- Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델): `hmmlearn==0.3.3`
- Stage24-25(24-25단계) Survival/Hazard(생존/위험률): `lifelines==0.30.3`, `statsmodels==0.14.6`
- shared model/runtime tools(공유 모델/런타임 도구): `numpy==2.3.4`, `pandas==2.3.3`, `scipy==1.16.3`, `onnx==1.20.1`, `skl2onnx==1.20.0`, `onnxmltools==1.16.0`

검증(verification, 검증): `pip check(패키지 충돌 검사)`는 broken requirements(깨진 요구사항) 없음으로 통과했고, `pygam`, `hmmlearn`, `lifelines`, `statsmodels` smoke test(연기 테스트)를 통과했다.

효과(effect, 효과): Stage20-25(20-25단계)는 폴더 구조(folder structure, 폴더 구조)를 미리 만들지 않고도, 진행 중 필요한 모델 도구(model tools, 모델 도구)를 바로 호출할 수 있다.

Stage26-32(26-32단계) extension tooling(확장 도구) 상태는 아래처럼 둔다.

- Stage26(26단계) NGBoost(자연 그래디언트 부스팅): `ngboost==0.5.10` 설치와 Python 3.13(파이썬 3.13) import/smoke compatibility(가져오기/연기 호환성)를 확인했고, `run20A_ngboost_probabilistic_distribution_scout_v1`에서 사용했다.
- Stage27(27단계) quantile boosting(분위수 부스팅): scikit-learn(`scikit-learn`, 사이킷런) quantile loss(분위수 손실)를 우선 후보로 쓴다.
- Stage28(28단계) Markov regression(마르코프 회귀): `statsmodels==0.14.6`로 시작할 수 있다.
- Stage29(29단계) River online ML(리버 온라인 머신러닝): `river`는 아직 설치하지 않았다. stage open(단계 개방) 전 drift metric(드리프트 지표)와 dependency(의존성)를 같이 확인한다.
- Stage30(30단계) calibration(보정): scikit-learn(사이킷런) calibration tools(보정 도구)를 우선 후보로 쓴다.
- Stage31-32(31-32단계) TabNet/TCN(탭넷/시간 합성곱 네트워크): `torch`/`pytorch-tabnet` 계열은 무거운 dependency(의존성)이므로 stage open(단계 개방) 시점에 설치 여부를 결정한다.

효과(effect, 효과): lightweight tools(가벼운 도구)는 이미 준비된 범위에서 쓰고, heavy deep learning dependencies(무거운 딥러닝 의존성)는 필요 단계에서만 설치해 environment pollution(환경 오염)을 줄인다.

## Stage Queue(단계 큐)

| stage(단계) | canonical stage id(정식 단계 ID) | model topic(모델 주제) | core question(핵심 질문) |
|---|---|---|---|
| 19 | `19_model_family_challenge__ebm_explainable_boosting_shape` | EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) | feature shape(피처 모양)이 설명 가능한 단변량/쌍변량 구조로 남는가? |
| 20 | `20_model_family_challenge__gam_additive_smooth_shape` | GAM(`Generalized Additive Model`, 일반화 가산 모델) | smooth additive effect(부드러운 가산 효과)가 트리 모델 단서를 대체하거나 반박하는가? |
| 21 | `21_model_family_challenge__elasticnet_logistic_linear_sanity` | ElasticNet Logistic(엘라스틱넷 로지스틱) | 선형 sparse signal(희소 선형 신호)만으로 방향/확률 구조가 남는가? |
| 22 | `22_regime_model__hmm_hidden_state_segmentation` | HMM(`Hidden Markov Model`, 은닉 마르코프 모델) | unsupervised hidden state(비지도 은닉 상태)가 거래 금지/허용 국면을 나누는가? |
| 23 | `23_regime_model__supervised_regime_classifier_filter` | regime classifier(국면 분류기) | supervised regime filter(지도 국면 필터)가 나쁜 구간을 줄이는가? |
| 24 | `24_exit_model__survival_time_to_event_hold_shape` | Survival model(생존 모델) | time-to-event(사건까지 시간)가 보유/청산 구조를 설명하는가? |
| 25 | `25_exit_model__hazard_trade_lifecycle_risk` | hazard model(위험률 모델) | bar-by-bar hazard(봉별 위험률)가 손실/반전 위험을 조기 포착하는가? |
| 26 | `26_model_family_challenge__ngboost_probabilistic_distribution_shape` | NGBoost(자연 그래디언트 부스팅) | predictive distribution(예측 분포)과 uncertainty(불확실성)가 거래 금지/허용 경계를 설명하는가? |
| 27 | `27_tail_model__quantile_boosting_risk_surface` | quantile boosting(분위수 부스팅) | upper/lower quantile(상하위 분위수)이 tail risk(꼬리 위험)를 분리하는가? |
| 28 | `28_regime_model__markov_switching_regression_state_link` | Markov regression(마르코프 회귀) | state switching(상태 전환)이 수익률/변동성 국면과 거래 KPI(핵심 성과 지표)를 연결하는가? |
| 29 | `29_adaptive_model__river_online_drift_learning` | River online ML(리버 온라인 머신러닝) | online adaptation(온라인 적응)이 leakage(누수) 없이 drift(변화)를 감지하고 성능 붕괴를 줄이는가? |
| 30 | `30_decision_layer__probability_calibration_abstention` | calibration/abstention(보정/기권) | 모델 확률을 신뢰 가능한 trade/no-trade(거래/비거래) decision layer(결정 계층)로 바꿀 수 있는가? |
| 31 | `31_model_family_challenge__tabnet_attentive_tabular_scout` | TabNet(탭넷) | attentive feature selection(주의 기반 피처 선택)이 트리/가산 모델과 다른 tabular interaction(표 형식 상호작용)을 찾는가? |
| 32 | `32_sequence_model__tcn_temporal_convolution_context` | TCN(시간 합성곱 네트워크) | temporal convolution(시간 합성곱)이 정적 58-feature(58개 피처) 표면에 없는 sequence context(순서 문맥)를 잡는가? |

효과(effect, 효과): Stage19-32(19-32단계)는 tree booster(트리 부스팅) 연속이 아니라 설명형, 선형, 국면, 생존/위험률, 확률분포, 꼬리위험, online adaptation(온라인 적응), calibration(보정), attentive tabular(주의 기반 표 형식), sequence model(순서 모델)을 순서대로 확인한다.

## Reference Seeds(참고 씨앗)

- Stage26(26단계) NGBoost(자연 그래디언트 부스팅): https://proceedings.mlr.press/v119/duan20a.html
- Stage27(27단계) scikit-learn quantile boosting(사이킷런 분위수 부스팅): https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html
- Stage28(28단계) statsmodels Markov regression(스탯츠모델스 마르코프 회귀): https://www.statsmodels.org/dev/examples/notebooks/generated/markov_regression.html
- Stage29(29단계) River online ML(리버 온라인 머신러닝): https://github.com/online-ml/river
- Stage30(30단계) scikit-learn calibration(사이킷런 보정): https://scikit-learn.org/stable/modules/calibration.html
- Stage31(31단계) TabNet paper(탭넷 논문): https://arxiv.org/abs/1908.07442
- Stage32(32단계) TCN paper(시간 합성곱 네트워크 논문): https://arxiv.org/abs/1803.01271

효과(effect, 효과): 각 확장 stage(단계)는 passing idea(지나가는 아이디어)가 아니라 source seed(출처 씨앗)가 있는 model-family question(모델군 질문)으로 출발한다.

## Stage19 Plan(19단계 계획)

- hypothesis(가설): EBM(설명가능 부스팅 머신)은 Stage18(18단계)에서 본 confidence/margin/session/volatility(확신/여백/세션/변동성) 단서를 설명 가능한 shape(모양)으로 분해할 수 있다.
- decision use(결정 용도): 설명 가능한 구조가 있으면 Stage20(20단계) GAM(일반화 가산 모델)로 smoothness(부드러움)를 확인한다.
- success criteria(성공 기준): validation/OOS(검증/표본 밖)에서 동일 방향 feature shape(피처 모양)가 남고 MT5 runtime_probe(런타임 탐침)가 완료된다.
- failure criteria(실패 기준): shape(모양)가 불안정하거나 MT5 KPI(핵심 성과 지표)가 방향 없이 붕괴한다.
- boundary(경계): model characteristic scout(모델 특성 탐색)만 허용한다.

## Stage20 Plan(20단계 계획)

- hypothesis(가설): GAM(일반화 가산 모델)은 EBM(설명가능 부스팅 머신)에서 보인 shape(모양)를 더 부드럽게 확인하거나 반박한다.
- decision use(결정 용도): feature effect(피처 효과)가 불연속 트리 구조인지, 연속적 국면 구조인지 구분한다.
- success criteria(성공 기준): 주요 feature(피처)의 smooth partial effect(부드러운 부분 효과)가 split(분할) 간 유지된다.
- failure criteria(실패 기준): smooth effect(부드러운 효과)가 없거나 MT5 runtime_probe(런타임 탐침)가 의미 없이 희박하다.
- boundary(경계): explanatory model scout(설명형 모델 탐색)만 허용한다.

## Stage21 Plan(21단계 계획)

- hypothesis(가설): ElasticNet Logistic(엘라스틱넷 로지스틱)은 최소한의 sparse linear signal(희소 선형 신호)을 남기거나, 비선형 모델 의존성을 드러낸다.
- decision use(결정 용도): 복잡한 모델이 필요한지, 기본 방향성이 선형으로도 남는지 판단한다.
- success criteria(성공 기준): non-flat probability(비평탄 확률)와 방향 mix(방향 혼합)가 split(분할) 간 무너지지 않는다.
- failure criteria(실패 기준): 확률이 flat(평탄)해지거나 방향이 한쪽으로 무의미하게 붕괴한다.
- boundary(경계): linear sanity check(선형 sanity check, 선형 점검)만 허용한다.

## Stage22 Plan(22단계 계획)

- hypothesis(가설): HMM(은닉 마르코프 모델)은 supervised label(지도 라벨) 없이도 volatility/session/trend(변동성/세션/추세) 상태를 나눌 수 있다.
- decision use(결정 용도): entry model(진입 모델)이 아니라 trade permission regime(거래 허용 국면)을 검토한다.
- success criteria(성공 기준): hidden state(은닉 상태)가 drawdown cluster(손실폭 군집)나 no-trade zone(거래 금지 구간)을 설명한다.
- failure criteria(실패 기준): state(상태)가 split(분할)마다 의미가 바뀌거나 거래 KPI와 연결되지 않는다.
- boundary(경계): regime segmentation probe(국면 분할 탐침)만 허용한다.

## Stage23 Plan(23단계 계획)

- hypothesis(가설): supervised regime classifier(지도 국면 분류기)는 bad-trade regime(나쁜 거래 국면)을 필터링할 수 있다.
- decision use(결정 용도): 모델 성과 개선이 아니라 risk filter(위험 필터) 가능성을 판단한다.
- success criteria(성공 기준): filtered view(필터된 보기)가 drawdown(손실폭)을 낮추면서 과도한 표본 축소를 피한다.
- failure criteria(실패 기준): 필터가 hindsight leakage(사후 누수)이거나 표본을 너무 많이 버린다.
- boundary(경계): filter scout(필터 탐색)만 허용한다.

## Stage24 Plan(24단계 계획)

- hypothesis(가설): Survival model(생존 모델)은 entry(진입)보다 hold/exit(보유/청산) 시간 구조를 더 잘 설명한다.
- decision use(결정 용도): hold rule(보유 규칙)을 모델 주제로 분리할지 판단한다.
- success criteria(성공 기준): time-to-adverse-event(불리 사건까지 시간)나 time-to-profit-decay(수익 약화까지 시간)가 split(분할) 간 안정적이다.
- failure criteria(실패 기준): event definition(사건 정의)이 불안정하거나 MT5 trade list(거래 목록)와 연결되지 않는다.
- boundary(경계): exit-shape scout(청산 형태 탐색)만 허용한다.

## Stage25 Plan(25단계 계획)

- hypothesis(가설): hazard model(위험률 모델)은 bar-by-bar(봉별) 손실/반전 위험을 추정해 exit risk(청산 위험)를 설명한다.
- decision use(결정 용도): survival(생존)보다 더 세밀한 runtime exit probe(런타임 청산 탐침)가 필요한지 판단한다.
- success criteria(성공 기준): hazard(위험률)가 drawdown cluster(손실폭 군집), losing streak(연속 손실), adverse excursion(불리 변동)과 연결된다.
- failure criteria(실패 기준): hazard(위험률)가 노이즈거나 Stage24(24단계)보다 설명력이 낮다.
- boundary(경계): risk lifecycle scout(위험 생애주기 탐색)만 허용한다.

## Stage26 Plan(26단계 계획)

- hypothesis(가설): NGBoost(`Natural Gradient Boosting`, 자연 그래디언트 부스팅)는 class probability(분류 확률)보다 distributional uncertainty(분포형 불확실성)를 더 잘 보여줄 수 있다.
- decision use(결정 용도): uncertainty width(불확실성 폭)를 no-trade zone(비거래 구간), direction asymmetry(방향 비대칭), tail warning(꼬리 경고)으로 쓸 수 있는지 판단한다.
- success criteria(성공 기준): split(분할) 간 distribution width(분포 폭)와 realized trade risk(실현 거래 위험)가 같은 방향으로 움직인다.
- failure criteria(실패 기준): uncertainty(불확실성)가 단순 confidence(확신도) 반복이거나 MT5 runtime_probe(런타임 탐침)에서 거래 의미가 없다.
- boundary(경계): probabilistic model scout(확률분포 모델 탐색)만 허용한다.

## Stage27 Plan(27단계 계획)

- hypothesis(가설): quantile boosting(분위수 부스팅)은 평균 방향보다 upper/lower tail(상하 꼬리) 손익 위험을 더 잘 설명한다.
- decision use(결정 용도): entry(진입)보다 position sizing(포지션 크기), no-trade(비거래), exit risk(청산 위험) 후보인지 본다.
- success criteria(성공 기준): lower quantile(하위 분위수)이 drawdown(손실폭), adverse excursion(불리 변동), loss cluster(손실 군집)와 반복적으로 연결된다.
- failure criteria(실패 기준): quantile band(분위수 띠)가 너무 넓거나 split(분할)마다 꼬리 의미가 바뀐다.
- boundary(경계): tail-risk scout(꼬리 위험 탐색)만 허용한다.

## Stage28 Plan(28단계 계획)

- hypothesis(가설): Markov regression(마르코프 회귀)은 관측 수익률/변동성의 latent state(잠재 상태)를 통해 trade permission regime(거래 허용 국면)을 설명할 수 있다.
- decision use(결정 용도): HMM(은닉 마르코프 모델)보다 supervised target(지도 목표)에 가까운 state link(상태 연결)가 필요한지 판단한다.
- success criteria(성공 기준): state probability(상태 확률)가 drawdown cluster(손실폭 군집), chop/trend(횡보/추세), session(세션)과 일관되게 연결된다.
- failure criteria(실패 기준): state(상태)가 hindsight label(사후 라벨)처럼 움직이거나 trade KPI(거래 핵심 성과 지표)와 분리된다.
- boundary(경계): state-link regime scout(상태 연결 국면 탐색)만 허용한다.

## Stage29 Plan(29단계 계획)

- hypothesis(가설): River online ML(리버 온라인 머신러닝)은 recent drift(최근 변화)와 feature distribution shift(피처 분포 이동)를 batch retrain(묶음 재학습)보다 빠르게 감지할 수 있다.
- decision use(결정 용도): live model(실거래 모델)이 아니라 drift alarm(변화 경보) 또는 adaptive scout(적응 탐색) 후보인지 판단한다.
- success criteria(성공 기준): online metric(온라인 지표)이 손실 구간 전에 악화되거나, adaptive update(적응 갱신)가 leakage(누수) 없이 성능 붕괴를 줄인다.
- failure criteria(실패 기준): online update(온라인 갱신)가 노이즈를 따라가거나 batch evidence(묶음 근거)보다 불안정하다.
- boundary(경계): drift/adaptation scout(변화/적응 탐색)만 허용한다.

## Stage30 Plan(30단계 계획)

- hypothesis(가설): calibration(보정)과 abstention(기권)은 모델을 바꾸지 않고 probability meaning(확률 의미)과 trade/no-trade(거래/비거래) 경계를 개선할 수 있다.
- decision use(결정 용도): 모델군 성능이 아니라 decision layer(결정 계층) 품질을 따로 분리해 본다.
- success criteria(성공 기준): calibrated probability(보정 확률)가 reliability curve(신뢰도 곡선), Brier score(브라이어 점수), MT5 runtime_probe(런타임 탐침)에서 더 일관된 위험 구간을 만든다.
- failure criteria(실패 기준): calibration(보정)이 표본을 외워 validation/OOS(검증/표본외)에서 반대로 움직인다.
- boundary(경계): decision-layer scout(결정 계층 탐색)만 허용한다.

## Stage31 Plan(31단계 계획)

- hypothesis(가설): TabNet(탭넷)은 attentive mask(주의 마스크)로 feature selection(피처 선택)과 nonlinear tabular interaction(표 형식 비선형 상호작용)을 동시에 볼 수 있다.
- decision use(결정 용도): tree/additive(트리/가산) 모델이 놓친 sparse interaction(희소 상호작용)이 있는지 판단한다.
- success criteria(성공 기준): attentive mask(주의 마스크)가 split(분할) 간 안정되고, selected feature group(선택 피처 그룹)이 MT5 runtime_probe(런타임 탐침)에서 의미를 가진다.
- failure criteria(실패 기준): mask(마스크)가 불안정하거나 deep model(딥러닝 모델) 비용 대비 새 특성이 없다.
- boundary(경계): attentive tabular scout(주의 기반 표 형식 탐색)만 허용한다.

## Stage32 Plan(32단계 계획)

- hypothesis(가설): TCN(`Temporal Convolutional Network`, 시간 합성곱 네트워크)은 58-feature(58개 피처) 단일 행보다 past window(과거 구간)의 temporal motif(시간적 패턴)를 더 잘 잡을 수 있다.
- decision use(결정 용도): sequence input(순서 입력)이 필요한지, 아니면 기존 feature engineering(피처 설계)이 충분한지 판단한다.
- success criteria(성공 기준): temporal receptive field(시간 수용영역) 길이 변화가 split(분할) 간 같은 방향으로 작동하고, MT5 handoff(메타트레이더5 인계)가 재현된다.
- failure criteria(실패 기준): window length(구간 길이)와 convolution depth(합성곱 깊이)가 노이즈 미세조정으로만 보인다.
- boundary(경계): sequence model scout(순서 모델 탐색)만 허용한다.

## Stop Rule(중지 규칙)

각 단계는 model characteristic(모델 특성), runtime_probe(런타임 탐침), KPI(핵심 성과 지표) 근거를 만든 뒤 닫는다. positive(긍정), promotion_candidate(승격 후보), operating_promotion(운영 승격)은 별도 명시 packet(묶음)이 없으면 만들지 않는다.

효과(effect, 효과): Stage19-32(19-32단계)가 모델 쇼핑(model shopping, 모델 쇼핑)으로 번지지 않고, 각 모델군과 decision layer(결정 계층)의 질문만 좁게 답한다.
- 2026-05-05: Stage20(20단계) GAM(일반화 가산 모델) closeout(마감) 완료, Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) open-only(개방만). 효과(effect, 효과): 다음 실제 실행은 `run15A_elasticnet_logistic_linear_sanity_scout_v1`이다.
- 2026-05-05: Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) closeout(마감) 완료, Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델) open-only(개방만). 효과(effect, 효과): 다음 실제 실행은 `run16A_hmm_hidden_state_segmentation_scout_v1`이다.
- 2026-05-05: Stage24(24단계) Survival model(생존 모델) closeout(마감) 완료, Stage25(25단계) hazard model(위험률 모델) open-only(개방만). 효과(effect, 효과): 다음 실제 실행은 `run19A_hazard_trade_lifecycle_risk_scout_v1`이다.

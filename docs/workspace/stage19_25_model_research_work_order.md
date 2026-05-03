# Stage19-25 Model Research Work Order(19-25단계 모델 연구 작업서)

## Purpose(목적)

Stage18(18단계) CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트)는 닫고, Stage19-25(19-25단계)는 서로 다른 model family(모델군) 질문으로 연다.

효과(effect, 효과): CatBoost(캣부스트), q85 threshold(q85 임계값), hold6(6봉 보유), selected variant(선택 변형)를 상속하지 않고, 각 단계가 독립 실험이 된다.

## Shared Controls(공통 통제)

- symbol/timeframe(심볼/시간프레임): `FPMarkets US100 M5`
- split/data surface(분할/데이터 표면): Stage18(18단계)과 같은 audited 58-feature MT5 price-proxy surface(감사된 58개 피처 MT5 가격 대리 표면)를 기본 후보로 쓴다.
- Tier records(티어 기록): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산)를 분리한다.
- MT5(`MetaTrader 5`, 메타트레이더5) claim(주장): runtime_probe(런타임 탐침)만 허용한다.
- forbidden inheritance(금지 상속): Stage18(18단계) CatBoost(캣부스트) model/threshold/variant/baseline(모델/임계값/변형/기준선)을 이어받지 않는다.

효과(effect, 효과): 모델 비교가 Stage18(18단계)의 좋은 구간을 좇는 식으로 왜곡되지 않는다.

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

효과(effect, 효과): Stage19-25(19-25단계)는 tree booster(트리 부스팅) 연속이 아니라 설명형, 선형, 국면, 생존/위험률 모델을 순서대로 확인한다.

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

## Stop Rule(중지 규칙)

각 단계는 model characteristic(모델 특성), runtime_probe(런타임 탐침), KPI(핵심 성과 지표) 근거를 만든 뒤 닫는다. positive(긍정), promotion_candidate(승격 후보), operating_promotion(운영 승격)은 별도 명시 packet(묶음)이 없으면 만들지 않는다.

효과(effect, 효과): Stage19-25(19-25단계)가 모델 쇼핑(model shopping, 모델 쇼핑)으로 번지지 않고, 각 모델군의 질문만 좁게 답한다.

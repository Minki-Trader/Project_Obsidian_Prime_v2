# Stage25 Closeout Packet(25단계 마감 묶음)

## Judgment(판정)

- stage(단계): `25_exit_model__hazard_trade_lifecycle_risk`
- status(상태): `closed_inconclusive_hazard_model_characteristics_exhausted`
- result subject(결과 대상): Hazard model(위험률 모델) trade lifecycle risk(거래 생애주기 위험), fixed elapsed-bar runtime handoff(고정 경과 봉 런타임 인계), MT5 runtime_probe(MT5 런타임 탐침)
- claim boundary(주장 경계): `hazard_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage25(25단계)는 Hazard model(위험률 모델)의 고유한 bar-by-bar risk shape(봉별 위험 모양)와 MT5 handoff(인계)를 기록하고 닫는다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- structural packet(구조 묶음): `docs/agent_control/packets/stage25_run19A_hazard_trade_lifecycle_scout_v1/aggregate_summary.json`
- runtime packet(런타임 묶음): `docs/agent_control/packets/stage25_run19B_hazard_trade_lifecycle_runtime_probe_v1/aggregate_summary.json`
- selected variant(선택 변형): `v04_logit_core24_reversal_after_favorable_1x`
- selected event(선택 사건): `reversal_after_favorable_1x`
- validation ROC AUC(검증 ROC AUC): `0.704654661378204`
- OOS ROC AUC(표본외 ROC AUC): `0.6908297000122845`
- validation lift(검증 고위험-저위험 사건 비율 차): `0.11199446940891808`
- OOS lift(표본외 고위험-저위험 사건 비율 차): `0.09907514450867053`
- Tier A top features(Tier A 주요 피처): `['hazard_elapsed_bar', 'hazard_elapsed_frac', 'close_ema20_ratio', 'historical_vol_20', 'hl_range']`
- Tier B top features(Tier B 주요 피처): `['hazard_elapsed_bar', 'hazard_elapsed_frac', 'historical_vol_20', 'hl_range', 'rsi_14']`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익 팩터/거래/손실폭): `-89.59` / `0.94` / `2145` / `187.51`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익 팩터/거래/손실폭): `-174.49` / `0.83` / `1210` / `206.31`
- score table parity(점수표 동등성): Tier A `True`, Tier B `True`
- runtime feature order(런타임 피처 순서): `['direction_proxy', 'hazard_risk_z']`
- runtime feature order hash(런타임 피처 순서 해시): `f7aceefc32853902f27cacbf659aae8a480fb1acbe57eec3702efd24a0aec913`
- threshold policy(임계값 정책): `{'quantile': 0.8, 'tier_a': 0.5705975078194689, 'tier_b': 0.552029007762084}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed(Tier A+B 라우팅), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- discrete-time hazard(이산 시간 위험률)는 elapsed bar(경과 봉)와 event row(사건 행)를 분리해 loss/reversal timing(손실/반전 시점)을 읽을 수 있었다.
- selected variant(선택 변형)는 `reversal_after_favorable_1x`에서 validation/OOS(검증/표본외) ROC AUC가 모두 0.69 이상으로 ranking shape(순위 모양)을 보였다.
- `hazard_elapsed_bar`, `hazard_elapsed_frac`, `historical_vol_20`, `hl_range`, `close_ema20_ratio`가 위험률 특성 판독에 반복 등장했다.
- MT5 runtime_probe(MT5 런타임 탐침)는 hazard risk(위험률 위험)를 direct entry score(직접 진입 점수)가 아니라 flat/close pressure(평탄/청산 압력)로 넘기는 handoff(인계)를 확인했다.

## Negative Memory(부정 기억)

- run19B(19B 실행)는 validation(검증) net `-89.59`, PF `0.94`, OOS(표본외) net `-174.49`, PF `0.83`로 trading path(거래 경로)는 부정적이다.
- hazard_risk(위험률 위험)는 calibrated probability(보정 확률)가 아니라 ranking/shape read(순위/모양 판독)로만 보존한다.
- runtime handoff(런타임 인계)는 fixed elapsed-bar snapshot(고정 경과 봉 스냅샷)을 썼다. dynamic position-age hazard clock(동적 포지션 나이 위험률 시계)은 아니다.
- runtime skip(런타임 건너뜀)에는 `feature_csv_timestamp_not_found:2025.09.30 23:55:00`가 남았다. parser error(파서 오류)는 0이지만 split boundary timestamp(분할 경계 타임스탬프) 주의는 보존한다.

## Invalid Setup(무효 설정)

- Hazard model(위험률 모델)을 baseline(기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)로 읽는 설정은 무효다.
- fixed elapsed-bar score table(고정 경과 봉 점수표)을 live-like dynamic hazard runtime(실거래 유사 동적 위험률 런타임)으로 읽는 설정은 무효다.
- Stage24(24단계) Survival model(생존 모델)과 Stage25(25단계) Hazard model(위험률 모델)을 같은 threshold inheritance(임계값 상속)로 비교하는 설정은 무효다.

## Blocked Retry Condition(차단 재시도 조건)

- blocker(차단 사유): `none(없음)`.
- exact retry condition(정확한 재시도 조건): Stage25(25단계)를 다시 열려면 dynamic position-age hazard EA support(동적 포지션 나이 위험률 EA 지원) 또는 exit-only hazard packet(청산 전용 위험률 묶음)을 명시적으로 열어야 한다.
- repair condition(수정 조건): split boundary timestamp(분할 경계 타임스탬프) skip(건너뜀)을 줄이려면 feature CSV(피처 CSV) 생성 시각과 tester interval(테스터 구간)을 같은 small tranche(작은 묶음)로 재검증한다.

효과(effect, 효과): Stage26(26단계)는 NGBoost(자연 그래디언트 부스팅)의 probabilistic distribution shape(확률분포 모양) 질문으로 새로 시작한다.

# Stage24 Closeout Packet(24단계 마감 묶음)

## Judgment(판정)

- stage(단계): `24_exit_model__survival_time_to_event_hold_shape`
- status(상태): `closed_inconclusive_survival_model_characteristics_exhausted`
- result subject(결과 대상): Survival model(생존 모델) time-to-event(사건까지 시간), censoring(검열), hold/exit clock(보유/청산 시계), MT5 runtime_probe(MT5 런타임 탐침)
- claim boundary(주장 경계): `survival_characteristic_and_permission_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage24(24단계)는 Survival model(생존 모델)의 hold/exit meaning(보유/청산 의미)을 확인했지만, 거래 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 닫는다.

## Evidence(근거)

- structural packet(구조 묶음): `docs/agent_control/packets/stage24_run18A_survival_time_to_event_scout_v1/aggregate_summary.json`
- runtime packet(런타임 묶음): `docs/agent_control/packets/stage24_run18B_survival_time_to_event_runtime_probe_v1/aggregate_summary.json`
- selected variant(선택 변형): `v04_weibull_aft_core24_abs_move_3x`
- selected model type(선택 모델 유형): `weibull_aft`
- event definition(사건 정의): `abs_move_3x`, max horizon bars(최대 지평 봉수) `12`, threshold multiplier(임계값 배수) `3.0`
- validation c-index(검증 C-지수): `0.73631244882561`
- OOS c-index(표본외 C-지수): `0.6856377470736932`
- validation event rate(검증 사건 비율): `0.4291954490044697`
- OOS event rate(표본외 사건 비율): `0.38072003164974283`
- Tier A top features(Tier A 주요 피처): `['hl_range', 'historical_vol_20', 'is_first_30m_after_open', 'bollinger_width_20', 'atr_14']`
- Tier B top features(Tier B 주요 피처): `['hl_range', 'historical_vol_20', 'bollinger_width_20', 'is_first_30m_after_open', 'atr_14']`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익계수/거래/손실폭): `-157.74` / `0.9` / `2195` / `315.57`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익계수/거래/손실폭): `-98.54` / `0.88` / `1100` / `141.34`
- score table parity(점수표 동등성): Tier A `True`, Tier B `True`
- runtime feature order(런타임 피처 순서): `['direction_proxy', 'survival_risk_z']`
- runtime feature order hash(런타임 피처 순서 해시): `0b4a961e4b2e875ebbed35b1140e3b975ff58480a7052415d81effb365a3dca6`
- threshold policy(임계값 정책): `{'quantile': 0.8, 'tier_a': 0.5674091566468802, 'tier_b': 0.555563843626271}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed(라우팅), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- Weibull AFT(와이블 가속고장시간) survival shape(생존 모양)는 `abs_move_3x` adverse/absolute movement event(불리/절대 변동 사건)에서 duration clock(지속 시간 시계)을 만들 수 있었다.
- `hl_range`, `historical_vol_20`, `is_first_30m_after_open`, `bollinger_width_20`, `atr_14`가 Tier A/B(티어 A/B) 양쪽에서 반복적으로 위쪽 feature read(피처 판독)에 남았다.
- validation(검증)에서 high-risk bucket(고위험 구간)은 low-risk bucket(저위험 구간)보다 event rate(사건 비율)가 높고 median duration(중앙 지속시간)이 짧았다.
- MT5 runtime_probe(MT5 런타임 탐침)는 survival risk(생존 위험)를 direct entry score(직접 진입 점수)가 아니라 flat/close pressure(평탄/청산 압력)로 넘기는 handoff(인계)를 확인했다.

## Negative Memory(부정 기억)

- run18B(18B실행)는 validation(검증) net `-157.74`, PF `0.9`, OOS(표본외) net `-98.54`, PF `0.88`로 trading path(거래 경로) 자체는 부정적이다.
- direct survival output(직접 생존 출력)은 방향 모델이 아니므로 `direction_proxy`를 붙여 MT5(메타트레이더5)에 넘겼다. 이 조합은 permission/exit probe(허용/청산 탐침)이지 survival runtime authority(생존 런타임 권위)가 아니다.
- runtime skip(런타임 건너뜀)에는 `feature_csv_timestamp_not_found:2025.09.30 23:55:00`가 반복됐다. parser error(파서 오류)는 0이지만 split boundary timestamp(분할 경계 타임스탬프)와 feature handoff(피처 인계) 경계가 예민하다는 기억으로 보존한다.

## Invalid Setup(무효 설정)

- Survival model(생존 모델)을 long/short entry selector(매수/매도 진입 선택기)로 직접 읽는 설정은 무효(invalid, 무효)다.
- run18B(18B실행)의 score table(점수표)은 `direction_proxy`와 `survival_risk_z` 두 축의 runtime approximation(런타임 근사)이므로 원본 lifelines(라이프라인즈) 모델의 live-like runtime authority(실거래 유사 런타임 권위)가 아니다.

## Blocked Retry Condition(차단 재시도 조건)

- blocker(차단 사유): `none(없음)`.
- exact retry condition(정확한 재시도 조건): Stage24(24단계)를 다시 열려면 survival risk(생존 위험)를 direction proxy(방향 대리 변수) 없이 exit-only(청산 전용)으로 쓰는 별도 explicit packet(명시 묶음)이 필요하다.
- repair condition(수정 조건): split boundary timestamp(분할 경계 타임스탬프) skip(건너뜀)을 줄이려면 MT5 feature CSV(피처 CSV) 끝시각과 tester interval(테스터 구간)을 같이 조정한 뒤 같은 small tranche(작은 묶음)로 재실행한다.

효과(effect, 효과): Stage25(25단계)는 Survival model(생존 모델)의 모델/임계값/런타임 파일을 baseline(기준선)으로 상속하지 않고, hazard model(위험률 모델)의 bar-by-bar risk(봉별 위험) 질문으로 새로 시작한다.

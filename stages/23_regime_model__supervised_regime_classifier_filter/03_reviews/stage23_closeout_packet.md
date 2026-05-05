# Stage23 Closeout Packet(23단계 마감 묶음)

## Judgment(판정)

- stage(단계): `23_regime_model__supervised_regime_classifier_filter`
- status(상태): `closed_inconclusive_supervised_regime_classifier_characteristics_exhausted`
- result subject(결과 대상): supervised regime classifier(지도 국면 분류기) permission/filter(허용/필터) and MT5 runtime_probe(MT5 런타임 탐침)
- claim boundary(주장 경계): `supervised_regime_classifier_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage23(23단계)는 p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 supervised classifier(지도 분류기)의 특성과 ONNX handoff(온닉스 인계)를 확인하고 닫는다. 이 결과는 운영 의미(operating meaning, 운영 의미)가 아니라 다음 topic pivot(주제 전환)을 위한 단서다.

## Evidence(근거)

- structural packet(구조 묶음): `docs/agent_control/packets/stage23_run17A_supervised_regime_classifier_scout_v1/aggregate_summary.json`
- runtime packet(런타임 묶음): `docs/agent_control/packets/stage23_run17B_supervised_regime_classifier_runtime_probe_v1/aggregate_summary.json`
- selected variant(선택 변형): `v05_logistic_core24_compact_filter`
- selected model type(선택 모델 유형): `logistic`
- Tier A top features(Tier A 주요 피처): `['rsi_14', 'close_ema20_ratio', 'hl_range', 'historical_vol_20', 'di_spread_14']`
- Tier B top features(Tier B 주요 피처): `['close_ema20_ratio', 'rsi_14', 'hl_range', 'atr_14_over_atr_50', 'minutes_from_cash_open']`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `10`
- normalized KPI records(정규화 핵심 성과 지표 기록): `10`
- parser errors(파서 오류): `0`
- trade parser errors(거래 파서 오류): `0`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익 팩터/거래/손실): `324.75` / `1.16` / `476` / `301.5`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익 팩터/거래/손실): `254.63` / `1.19` / `345` / `153.14`
- ONNX parity(온닉스 동등성): Tier A `True`, Tier B `True`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- `v05_logistic_core24_compact_filter`는 small handoff-friendly(작은 인계 친화) logistic classifier(로지스틱 분류기)로도 permission/filter(허용/필터) shape(모양)를 만들 수 있었다.
- validation(검증)과 OOS(표본외) routed run(라우팅 실행)은 모두 positive net(양수 순손익)을 보였지만, 이것은 단일 runtime_probe(런타임 탐침)이므로 edge(거래 우위)가 아니다.
- 주요 feature(피처)는 rsi(상대강도지수), range/volatility(범위/변동성), session timing(세션 시간), price-to-average ratio(가격-평균 비율) 축에 몰렸다.
- p_flat(평탄 확률)을 no-trade/block(무거래/차단) 후보로 해석하는 구조는 Stage30 calibration/abstention(보정/기권)에서 다시 볼 수 있는 단서다.

## Negative Memory(부정 기억)

- validation/OOS(검증/표본외)가 동시에 양수여도 calibration(보정), WFO(워크포워드 최적화), live runtime parity(실시간 런타임 동등성)가 없으므로 alpha quality(알파 품질)로 올리지 않는다.
- runtime output(런타임 출력)에는 `feature_csv_timestamp_not_found` skip(건너뜀)이 많이 남았다. parser error(파서 오류)는 0이지만, tester range(테스터 범위)와 feature handoff(피처 인계) 경계가 남긴 운영 부채로 보존한다.
- supervised classifier(지도 분류기)는 label(라벨)을 직접 학습하므로 future leakage(미래 누수)와 threshold overfit(임계값 과적합) 감시가 필요하다.

## Closeout Rule(마감 규칙)

Stage24(24단계)는 Survival model(생존 모델) topic pivot(주제 전환)으로 연다. Stage23(23단계)의 model(모델), threshold(임계값), positive MT5 read(양수 MT5 판독)는 baseline(기준선), promotion(승격), runtime authority(런타임 권위)로 상속하지 않는다.

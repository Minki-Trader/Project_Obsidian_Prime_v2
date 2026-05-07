# Stage33 RUN27A Time-Segment Survivor KPI Audit(33단계 실행27A 시간 구간 생존 KPI 감사)

## Result(결과)

`run27A_time_segment_survivor_clue_audit_v1` is reviewed(검토됨) as `inconclusive(불충분)`.

효과(effect, 효과): Stage20~32(20~32단계)의 기존 MT5(`MetaTrader 5`, 메타트레이더5) report(보고서)를 month/quarter/rolling3(월/분기/구르는 3개월)로 다시 잘라, split(분할) 양쪽에서 살아남은 단서만 후보로 남겼다.

## Counts(수량)

- runtime runs(런타임 실행): `17`
- parsed MT5 reports(해석된 MT5 보고서): `70`
- parsed trades(해석된 거래): `33484`
- time segment KPI rows(시간 구간 KPI 행): `1278`
- month/quarter/rolling3 rows(월/분기/구르는 3개월 행): `499` / `193` / `499`
- split survivor candidates(분할 생존 후보): `5`
- unique metric fingerprints(고유 지표 지문): `4`

## Survivor Clues(생존 단서)

- `run14B_gam_runtime_handoff_probe_v1`: validation(검증) net(순수익) `8.65`, PF(수익 팩터) `1.00729`; OOS(표본외) net(순수익) `295.69`, PF(수익 팩터) `1.50636`; month+(월 양수 비율) `0.625`, quarter+(분기 양수 비율) `0.666667`, rolling3+(구르는 3개월 양수 비율) `0.625`; flags(표시) `thin_pf_margin;thin_net_margin;negative_month_observed;negative_quarter_observed`.
- `run17B_supervised_regime_classifier_runtime_probe_v1`: validation(검증) net(순수익) `324.75`, PF(수익 팩터) `1.15935`; OOS(표본외) net(순수익) `254.63`, PF(수익 팩터) `1.18668`; month+(월 양수 비율) `0.625`, quarter+(분기 양수 비율) `0.5`, rolling3+(구르는 3개월 양수 비율) `0.625`; flags(표시) `negative_month_observed;negative_quarter_observed`.
- `run22B_markov_regression_state_runtime_probe_v1`: validation(검증) net(순수익) `244.08`, PF(수익 팩터) `1.77004`; OOS(표본외) net(순수익) `111.27`, PF(수익 팩터) `1.31036`; month+(월 양수 비율) `0.75`, quarter+(분기 양수 비율) `1`, rolling3+(구르는 3개월 양수 비율) `0.875`; flags(표시) `negative_month_observed`.
- `run26B_tcn_temporal_convolution_runtime_probe_v1`: validation(검증) net(순수익) `75.26`, PF(수익 팩터) `1.03501`; OOS(표본외) net(순수익) `111.77`, PF(수익 팩터) `1.07029`; month+(월 양수 비율) `0.5`, quarter+(분기 양수 비율) `0.5`, rolling3+(구르는 3개월 양수 비율) `0.625`; flags(표시) `thin_pf_margin;negative_month_observed;negative_quarter_observed;duplicate_metric_fingerprint`.
- `run26D_torch_tcn_native_temporal_runtime_probe_v1`: validation(검증) net(순수익) `75.26`, PF(수익 팩터) `1.03501`; OOS(표본외) net(순수익) `111.77`, PF(수익 팩터) `1.07029`; month+(월 양수 비율) `0.5`, quarter+(분기 양수 비율) `0.5`, rolling3+(구르는 3개월 양수 비율) `0.625`; flags(표시) `thin_pf_margin;negative_month_observed;negative_quarter_observed;duplicate_metric_fingerprint`.

## Judgment(판정)

가장 깨끗한 clue(단서)는 `run22B_markov_regression_state_runtime_probe_v1`다. 이유(reason, 이유)는 validation/OOS(검증/표본외)가 모두 positive(양수)이고 quarter(분기) 단위가 모두 positive(양수)였기 때문이다.

효과(effect, 효과): 이 결과는 next probe(다음 탐침)의 seed clue(씨앗 단서)일 수 있지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 아니다.

## Missing Evidence(빠진 근거)

actual full-period single report(실제 전체 기간 단일 보고서)는 `source_artifact_missing(원천 산출물 누락)`이다.

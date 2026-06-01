# run357B High-Density Label Pivot(run357B 고밀도 라벨 전환)

- run_id(실행 ID): `run357B_design_high_density_label_pivot_without_db_v1`
- parent_run_id(부모 실행 ID): `run357A_branch_stage356_to_high_density_label_pivot_without_db_v1`
- status(상태): `completed_stage357B_high_density_label_pivot_positive_proxy_queue_ready_no_selection`
- judgment(판정): `positive_proxy_high_density_label_pivot_mt5_probe_required_no_operating_claim`
- decision(결정): `stage357B_open_run357C_package_high_density_label_pivot_mt5_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run357C_package_high_density_label_pivot_mt5_probe_without_db_v1`
- trained_models(학습 모델): `12`
- onnx_parity_rows(온엑스 동등성 행): `12`
- threshold_sweep_rows(임계값 탐색 행): `6912`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `8`

Action(행동): Stage356C(356C 실행)의 trade/day(일별 거래수) 3 미달 실패 기억을 바탕으로 H12 high-density label(고밀도 H12 라벨)과 ExtraTrees ONNX classifier(엑스트라트리스 온엑스 분류기)를 학습했다.

Effect(효과): proxy(프록시) 기준에서 MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있는 queue(대기열)를 만들었지만, 이 결과는 operating claim(운영 주장)이 아니다.

## Best Proxy Row(최선 프록시 행)

- model_id(모델 ID): `run357B_d04_h12_q45_55_high_density_band__extratrees_cls_depth5_leaf100_seed11`
- label_variant_id(라벨 변형 ID): `d04_h12_q45_55_high_density_band`
- score_policy(점수 정책): `pside`
- score_quantile(점수 분위수): `0.2`
- threshold_basis(임계값 기준): `validation`
- adx_min(ADX 최소값): `20.0`
- session_mode(세션 모드): `all`
- validation_trade_per_day(검증 일별 거래수): `3.191256830601093`
- validation_stress_net(검증 압박 순수익): `0.04272783621312366`
- validation_stress_pf(검증 압박 수익 팩터): `1.0468369083281632`
- validation_balance(검증 롱/숏 균형): `0.8136645962732919`
- oos_trade_per_day(표본외 일별 거래수): `3.4427480916030535`
- oos_stress_net(표본외 압박 순수익): `0.05220314769635774`
- oos_stress_pf(표본외 압박 수익 팩터): `1.0837603236717956`
- oos_balance(표본외 롱/숏 균형): `0.8408163265306122`
- candidate_gate(후보 게이트): `passed_proxy_mt5_probe_queue(프록시 MT5 탐침 대기열 통과)`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.

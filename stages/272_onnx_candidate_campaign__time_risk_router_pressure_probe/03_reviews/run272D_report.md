# run272D Time-Risk Router MT5 Probe Review(272D 시간 위험 라우터 MT5 탐침 검토)

- run_id(실행 ID): `run272D_review_time_risk_router_mt5_probe_v1`
- source_run(원천 실행): `run272C_time_risk_router_mt5_signal_replay_v1`
- status(상태): `completed_time_risk_router_mt5_probe_review_no_candidate_selection`
- judgment(판정): `q04_pressure_survivor_for_stability_validation_no_candidate_selection`
- survivor_rows(생존 행): `2`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `open_stage273_time_risk_router_stability_validation`

## Plain Result(쉬운 결과)

run272D(272D 실행)는 run272C(272C 실행)의 MT5(`MetaTrader 5`, 메타트레이더5) KPI(핵심 성과 지표)를 Tier A/Tier B(티어 A/티어 B) 쌍으로 다시 읽었다.
효과(effect, 효과): q04(4번 분기)는 stability validation seed(안정성 검증 씨앗)로 남기고, q01~q03(1~3번 분기)은 대조 또는 failure memory(실패 기억)로 둔다.

## Review Table(검토 표)

- `q01` `Tier A`: net_sum(순수익 합) `283.57`, PF_min(최소 수익 팩터) `1.06`, trades(거래 수) `1278`, DD_max(최대 손실폭) `33.95`, decision(결정) `reference_control_only`
- `q01` `Tier B`: net_sum(순수익 합) `283.57`, PF_min(최소 수익 팩터) `1.06`, trades(거래 수) `1278`, DD_max(최대 손실폭) `33.95`, decision(결정) `reference_control_only`
- `q02` `Tier A`: net_sum(순수익 합) `329.94`, PF_min(최소 수익 팩터) `1.08`, trades(거래 수) `1176`, DD_max(최대 손실폭) `39.43`, decision(결정) `watch_but_not_survivor_due_to_pf_or_dd`
- `q02` `Tier B`: net_sum(순수익 합) `329.94`, PF_min(최소 수익 팩터) `1.08`, trades(거래 수) `1176`, DD_max(최대 손실폭) `39.43`, decision(결정) `watch_but_not_survivor_due_to_pf_or_dd`
- `q03` `Tier A`: net_sum(순수익 합) `349.91`, PF_min(최소 수익 팩터) `1.06`, trades(거래 수) `1477`, DD_max(최대 손실폭) `39.01`, decision(결정) `watch_but_not_survivor_due_to_pf_or_dd`
- `q03` `Tier B`: net_sum(순수익 합) `349.91`, PF_min(최소 수익 팩터) `1.06`, trades(거래 수) `1477`, DD_max(최대 손실폭) `39.01`, decision(결정) `watch_but_not_survivor_due_to_pf_or_dd`
- `q04` `Tier A`: net_sum(순수익 합) `421.99`, PF_min(최소 수익 팩터) `1.14`, trades(거래 수) `850`, DD_max(최대 손실폭) `34.89`, decision(결정) `pressure_survivor_for_stability_validation`
- `q04` `Tier B`: net_sum(순수익 합) `421.99`, PF_min(최소 수익 팩터) `1.14`, trades(거래 수) `850`, DD_max(최대 손실폭) `34.89`, decision(결정) `pressure_survivor_for_stability_validation`

## Survivors(생존 분기)

- `q04` `Tier A`: `pressure_survivor_not_selected_candidate`, next(다음) `stability_validation_seed`
- `q04` `Tier B`: `pressure_survivor_not_selected_candidate`, next(다음) `stability_validation_seed`

## Failure Memory(실패 기억)

- `q01` `Tier A`: `reference_control_only`
- `q01` `Tier B`: `reference_control_only`
- `q02` `Tier A`: `watch_but_not_survivor_due_to_pf_or_dd`
- `q02` `Tier B`: `watch_but_not_survivor_due_to_pf_or_dd`
- `q03` `Tier A`: `watch_but_not_survivor_due_to_pf_or_dd`
- `q03` `Tier B`: `watch_but_not_survivor_due_to_pf_or_dd`

## Boundary(경계)

q04(4번 분기)는 pressure survivor(압박 생존 분기)일 뿐 selected candidate(선택 후보)가 아니다.
효과(effect, 효과): 다음 Stage273(273단계) stability validation(안정성 검증)이 q04(4번 분기)를 더 깨뜨리거나 좁힐 수 있다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`

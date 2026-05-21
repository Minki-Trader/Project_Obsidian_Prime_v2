# Stage267 Run267BS Pool-Wide Directional/Impulse Follow-Up Materialization(267단계 267BS 후보군 전체 방향/임펄스 후속 물질화)

## Summary(요약)

Run267BS(267BS 실행)는 run267BR(267BR 실행)의 P0 queue(P0 대기열) 두 개를 다섯 baseline candidates(기준 후보) 전체의 Tier A(티어 A) MT5(MetaTrader 5, 메타트레이더5) 입력으로 물질화했다.

- variants(변형): `10`
- attempts(시도): `10`
- candidates(후보): `5`
- profiles(프로필): `directional_asymmetry(방향 비대칭)`, `aggressive_impulse_replacement(공격형 임펄스 대체)`
- next_action(다음 행동): `run267BT_execute_pool_wide_directional_impulse_followup_mt5_batch`

Effect(효과): baseline(기준 후보)을 지금 고르는 대신, 이전 연구에서 나온 sell-side fragility(매도측 취약성)와 2023H2 impulse clue(2023년 하반기 임펄스 단서)를 후보군 전체에서 같은 조건으로 깨뜨려 볼 수 있게 했다.

## Boundary(경계)

이 run(실행)은 materialization(물질화)이다. 아직 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표), trade records(거래 기록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표)는 없다.

selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 `none/not_claimed`이다.

## Inputs(입력)

- source queue(원천 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BR/anti_overconstraint_cross_period_followup_or_prune_design/followup_queue.csv`
- source 2024 feature manifest(2024 피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/features.csv`
- source 2024 attempts(2024 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/attempts.csv`

## Outputs(출력)

- variant manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/directional_impulse_variant_manifest.csv`
- attempt manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/attempt_manifest.csv`
- runtime contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/runtime_contract.csv`
- diagnostics(진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/feature_engineering_diagnostics.csv`
- route gap audit(라우팅 공백 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BS/pool_wide_directional_impulse_followup_materialization/route_gap_audit.csv`

## Tier Boundary(티어 경계)

Tier A(티어 A)는 실행 대기 입력까지 물질화했다. Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 없어서 blocked(차단)로 남긴다.

Effect(효과): duplicate Tier A+B(중복 티어 A+B)를 routed total(라우팅 전체)처럼 말하지 않는다.

# Stage62 Legacy 34D Target Gap(62단계 레거시 34D 목표 차이)

## Boundary(경계)

Legacy 34D(레거시 34D)는 v2 result(브이투 결과)가 아니다. It is a target surface(목표 표면) and lesson-only reference(교훈 전용 참조) only.

Action(행동): Stage62(62단계)는 34D(34D)의 KPI(핵심 성과 지표)를 숫자 목표로 읽되, code path(코드 경로), promotion history(승격 이력), operating meaning(운영 의미)은 상속하지 않는다.
Effect(효과): v2 research(브이투 연구)는 34D를 베끼지 않고, 34D 이상을 노리는 독립 목표로 진행된다.

## 34D Target Surface(34D 목표 표면)

Latest-window target(최신 구간 목표):

- net_profit(순손익): `987.60`
- profit_factor(수익 팩터): `1.583157`
- max_dd_pct(최대 손실률): `12.909136`
- trade_count(거래 수): `404`
- expectancy_per_trade(거래당 기대값): `2.444554`
- win_rate(승률): `0.576733`
- avg_hold(평균 보유): `3.071782`

Extended bridge target(확장 브리지 목표):

- net_profit(순손익): `2950.79`
- profit_factor(수익 팩터): `1.302494`
- max_dd_pct(최대 손실률): `18.760867`
- trade_count(거래 수): `1134`
- expectancy_per_trade(거래당 기대값): `2.602108`

## Current V2 Reference(현재 브이투 참조)

Stage60 actual routed total(60단계 실제 라우팅 전체):

- validation(검증): net(순손익) `426.22`, PF(수익 팩터) `1.17`, max_dd_pct(최대 손실률) `15.36`, trade_count(거래 수) `454`, expectancy(기대값) `0.938811`
- OOS(표본외): net(순손익) `490.24`, PF(수익 팩터) `1.29`, max_dd_pct(최대 손실률) `17.96`, trade_count(거래 수) `330`, expectancy(기대값) `1.485576`

## Gap Read(차이 판독)

- Main gap(주요 차이): expectancy(기대값)와 PF(수익 팩터)가 34D target(34D 목표)보다 낮다.
- Secondary gap(보조 차이): validation drawdown(검증 손실폭)이 latest 34D target(최신 34D 목표)보다 높다.
- Not the main gap(주요 차이가 아님): trade_count(거래 수)는 이미 충분히 있다. Effect(효과): Stage62(62단계)는 거래 수를 늘리는 것보다 trade quality(거래 품질)를 먼저 본다.
- Segment risk(구간 위험): validation mid PF(검증 중간 PF) `1.1007`이 약하다. Effect(효과): 34D급 KPI를 노리려면 중간 구간 안정성을 먼저 키워야 한다.

## V2-Native Direction(브이투 고유 방향)

- trade_shape_lift(거래 형태 개선): MFE/MAE(MFE/MAE), hold(보유), payoff(손익비), win/loss balance(승패 균형)를 같이 본다.
- state_context_filter(상태/문맥 필터): volatility/ADX/session(변동성/ADX/세션)을 v2 feature space(브이투 피처 공간)에서 새로 측정한다.
- risk_bracket_quality(위험/브래킷 품질): ATR SL/TP(ATR 손절/익절), model risk%(모델 위험률), min lot floor(최소 랏 바닥)를 유지한다.
- Tier B diagnostic(Tier B 진단): Tier B(티어 B)는 허용되지만, 손상 반복 시 failure memory(실패 기억)로 남긴다.

## Decision Use(판정 용도)

Stage62(62단계)는 34D copy(34D 복사)를 만들지 않는다. Stage62 result(62단계 결과)는 다음 중 하나만 결정한다.

- continue_v2_native_34d_target_batch(브이투 고유 34D 목표 묶음 계속)
- open_state_context_model_branch(상태/문맥 모델 분기 개방)
- continue_adapter_trade_shape_repair(어댑터 거래 형태 수리 계속)
- preserve_stage61_reference_and_open_new_model_branch(61단계 참조 보존 및 새 모델 분기 개방)

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).

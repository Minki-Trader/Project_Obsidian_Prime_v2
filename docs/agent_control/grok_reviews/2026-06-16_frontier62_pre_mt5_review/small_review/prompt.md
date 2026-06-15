# Frontier62 Pre-MT5 Review(전선62 MT5 전 검토)

Codex asks for a bounded second opinion(제한된 2차 의견). Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Current Truth(현재 진실)

- Stage(단계): `stage_frontier_62__post_allocation_failure_mode_or_seed_expansion`
- Hypothesis(가설): event-compressed runtime representation(이벤트 압축 런타임 표현)이 F61 proxy-runtime density gap(프록시-런타임 밀도 차이)을 줄이면서 handoff failure(인계 실패) 없이 남는 side-allocation signal(방향 배분 신호)이 있는지 본다.
- Stage-open Grok(단계 개방 그록): `accepted(수용)` with condition(조건): lock event-compressed sequential proxy definition(이벤트 압축 순차 프록시 정의), density-band penalty(밀도 구간 벌점), and retrain gate(재학습 게이트) before run(실행)이다.
- Local implementation(로컬 구현): locked protocol(고정 절차) was coded before MT5(엠티5) and first proxy-only(프록시 전용) run.

## Proxy Result(프록시 결과)

- Selected candidate(선택 후보): `f62b_evt_t42_m4_h6_cd2_cof1`
- Runtime policy(런타임 정책): close-on-flat(무신호 청산)=true, entry-transition-only(진입 전환 전용)=true, same-direction cooldown(동일 방향 쿨다운)=2, max hold(최대 보유)=6.
- ONNX parity(온엑스 동등성): passed(통과), max_abs_diff=`1.416e-07`.
- Train PF/DD/density(학습 PF/DD/밀도): `1.9849 / 2.1593 / 0.2914 per day`
- Validation PF/DD/density(검증 PF/DD/밀도): `1.1583 / 1.4870 / 0.3661 per day`
- OOS PF/DD/density(표본밖 PF/DD/밀도): `1.6075 / 0.5717 / 0.3511 per day`
- Density target(밀도 목표): 5~10 trades/day(일 5~10회)
- Best observed proxy validation density(관찰된 최고 프록시 검증 밀도): about `0.366/day`, so the locked grid is too sparse(너무 희소함).

## Question(질문)

Before expensive MT5 backtest(MT5 백테스트) should Codex:

1. run MT5 anyway(그래도 MT5 실행) to satisfy mandatory runtime probe(필수 런타임 탐침), knowing proxy density is far below target;
2. do one bounded proxy repair(상한 있는 프록시 수리) before MT5 by expanding only threshold/margin/cooldown grid(임계값/마진/쿨다운 격자) toward density 5~10/day, then freeze one candidate and run MT5;
3. close as invalid setup(무효 설정) because proxy density misses the stage hypothesis too far?

Please classify as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요), and give the smallest safe action(가장 작은 안전 행동). Keep the claim boundary(주장 경계) at runtime_probe_observation only(런타임 탐침 관찰 전용).

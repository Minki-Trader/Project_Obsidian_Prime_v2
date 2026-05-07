# Decision(결정): Stage28 Tier A Markov Seed Preservation(28단계 티어 A 마르코프 씨앗 보존)

## Decision(결정)

`run22B_markov_regression_state_runtime_probe_v1`의 보존 씨앗(preserved seed, 보존 씨앗)을 `Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`로 좁혀 남긴다.

## Evidence(근거)

- Tier A only(Tier A 단독) validation(검증): `net_profit=208.01; pf=1.77; trades=77; short=0`
- Tier A only(Tier A 단독) OOS(표본외): `net_profit=62.65; pf=1.22; trades=51; short=0`
- Tier B fallback only(Tier B 대체 단독) validation/OOS(검증/표본외): `net_profit=-35.18; pf=0.86` / `net_profit=-1.82; pf=0.99`
- routed total(라우팅 전체) validation/OOS(검증/표본외): `net_profit=244.08; pf=1.77; trades=190` / `net_profit=111.27; pf=1.31; trades=118`

## Boundary(경계)

Stage33(33단계) full packet(전체 묶음)은 rollback(롤백) 상태로 되살리지 않는다. 이 결정은 Stage28(28단계) 기존 근거에서 Tier A(티어 A) long-only permission clue(롱 전용 허용 단서)를 보존하는 것이다. Markov regression(마르코프 회귀) 전체, Tier B fallback(티어 B 대체), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 주장하지 않는다.

## Effect(효과)

다음 probe(탐침)는 Tier A(티어 A) state permission(상태 허용)이 왜 long side(롱 방향)에서 profit factor(수익 팩터)를 지탱했는지 작게 찔러볼 수 있다.

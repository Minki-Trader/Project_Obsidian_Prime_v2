# Stage33 Regime Mechanism: Tier A Markov Long Permission Source(33단계 국면 메커니즘: 티어 A 마르코프 롱 허용 원천)

## Core Question(핵심 질문)

`Tier A Markov state long permission filter(티어 A 마르코프 상태 롱 허용 필터)`는 whole Markov regression(전체 마르코프 회귀)이 좋아서가 아니라 high-confidence full-context long states(고신뢰 전체 문맥 롱 상태)를 잘 골라서 살아남았는가?

효과(effect, 효과): Stage33(33단계)는 Stage28(28단계) run22B(22B 실행)의 Tier A(티어 A) long-only clue(롱 전용 단서)를 해부한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Hypothesis(가설)

Tier A(티어 A)의 profit factor(수익 팩터)는 Markov regression(마르코프 회귀) 전체 성능이 아니라 state permission(상태 허용)이 long side(롱 방향)에서 손실 구간을 덜 밟게 만든 효과일 수 있다.

## Decision Use(결정 용도)

결과(result, 결과)는 다음 probe(탐침)의 feature/threshold/permission design(피처/임계값/허용 설계)에만 쓴다. 운영 기준(operating reference, 운영 기준)으로 쓰지 않는다.

## Controls(고정 조건)

- symbol/timeframe(심볼/시간축): `US100 M5`
- source seed(원천 씨앗): `run22B_markov_regression_state_runtime_probe_v1`
- sample labels(표본 라벨): Tier A(티어 A)/Tier B(티어 B)
- no new baseline(새 기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음)

## Changed Variables(변경 변수)

- Tier A long permission(티어 A 롱 허용)을 state score/state confidence/state entropy(상태 점수/상태 신뢰/상태 엔트로피)와 time segment(시간 구간)로 분해한다.
- Tier B fallback(티어 B 대체)은 비교 경계(comparison boundary, 비교 경계)로만 둔다.

## Planned Run(계획 실행)

- `run27A_tier_a_markov_long_permission_source_scout_v1`: structural attribution scout(구조 귀속 탐침) only(전용)

## Success Criteria(성공 기준)

Tier A(티어 A) long permission(롱 허용)의 이익이 특정 state band(상태 구간), confidence band(신뢰 구간), time segment(시간 구간)에 집중됐는지 설명할 수 있으면 useful evidence(쓸모 있는 근거)다.

## Failure Criteria(실패 기준)

이익이 소수 trade(거래), 한 달(month, 월), 또는 unstable slice(불안정 구간)에만 기대면 negative memory(부정 기억)로 남긴다.

## Invalid Conditions(무효 조건)

run22B(22B 실행) score table(점수표), predictions(예측), MT5 report(보고서), stage ledger(단계 장부)가 서로 맞지 않으면 invalid(무효)로 둔다.

## Evidence Plan(근거 계획)

- Stage28(28단계) run22B(22B 실행) prediction/report/ledger(예측/보고서/장부) 재사용
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산) 기록 유지
- structural attribution(구조 귀속)이 충분히 좁아지기 전에는 no new MT5 run(새 MT5 실행 없음)

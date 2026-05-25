# Regime Attribution Report(국면 귀속 보고서)

## Status(상태)

`coverage_available_with_timezone_boundary`(범위 확보, 시간대 경계 남음).

## Evidence(근거)

- VIX(VIX 변동성 지수), USDX(달러 지수), US10YR(미국 10년물) required regime data(필수 국면 데이터)는 requested forward end(요청 전진 종료)에 닿았다.
- timezone status(시간대 상태)는 raw manifest(원천 목록)에서 `UNRESOLVED_REQUIRES_MANUAL_BINDING`로 남아 있다.
- effect(효과): 1번 data missing blocker(데이터 누락 차단)는 해소됐지만, positive forward judgment(긍정 전진 판정)에는 frozen signal handoff(고정 신호 인계)와 시간대 묶음 확인이 여전히 필요하다.

## Required repair(필수 수정)

1. timestamp/timezone binding(타임스탬프/시간대 묶음)을 명시한다.
2. frozen route-signal handoff(고정 경로 신호 인계)를 만든다.
3. 그 다음 MT5 forward run(MT5 전진 실행)을 수행한다.

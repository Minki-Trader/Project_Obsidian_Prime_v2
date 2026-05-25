# Regime Attribution Report(국면 귀속 보고서)

## Status(상태)

`blocked_forward_data_missing`(전진 데이터 누락/불완전).

## Evidence(근거)

- VIX(VIX 변동성 지수), USDX(달러 지수), US10YR(미국 10년물) are required regime slices(필수 국면 구간) for this gate(게이트).
- US10YR(미국 10년물) does not cover(포괄하지 못함) the requested forward end(요청 전진 종료).
- timezone status(시간대 상태)는 raw manifest(원천 목록)에서 `UNRESOLVED_REQUIRES_MANUAL_BINDING`로 남아 있다.
- effect(효과): session/hour/month/volatility/ADX/VIX/USD/rate regime slices(세션/시간/월/변동성/ADX/VIX/달러/금리 국면 구간)를 성공 판정 근거로 사용할 수 없다.

## Required repair(필수 수정)

1. US10YR(미국 10년물) forward M5(5분봉)를 US100(나스닥100) 종료 시점까지 확보한다.
2. timestamp/timezone binding(타임스탬프/시간대 묶음)을 명시한다.
3. 그 다음 frozen signal handoff(고정 신호 인계)를 먼저 만든다.

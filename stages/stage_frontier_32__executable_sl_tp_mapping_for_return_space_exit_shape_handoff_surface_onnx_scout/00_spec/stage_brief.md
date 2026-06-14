# Frontier32 Stage Brief(전선32 단계 요약)

Opened(개방): 2026-06-14T13:15:38Z

Hypothesis(가설): F31(전선31)의 return-space stop/take log caps(수익률 공간 손절/익절 로그 상한)을 fixed price-path SL/TP rules(고정 가격 경로 손절/익절 규칙)로 바꾸면, 일부 handoff surface(인계 표면)가 high/low path proxy(고가/저가 경로 프록시)에서도 살아남을 수 있습니다.

Action(행동): F31 mapping queue(전선31 매핑 큐) `16`개를 고정하고, raw US100 M5 Bid OHLC(원천 유에스100 5분봉 매수호가 시가/고가/저가/종가)로 path proxy(경로 프록시)를 열었습니다.

Effect(효과): F31 proxy(전선31 프록시)를 상속하지 않고, executable representation(실행 가능한 표현)만 새 changed variable(변경 변수)로 시험합니다.

Intrabar tie-break(봉내 동시 터치 규칙): same-bar stop/take hit(같은 봉 손절/익절 동시 터치)는 conservative stop-first(보수적 손절 우선)입니다.

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

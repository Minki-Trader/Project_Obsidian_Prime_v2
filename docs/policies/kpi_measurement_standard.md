# KPI Measurement Standard

KPI(`key performance indicator`, 핵심 성과 지표)는 실행(run, 실행)이 실제로 무엇을 시험했는지 측정한다.

## 점수판(Scoreboards, 점수판)

- `structural_scout(구조 스카우트)`: 초기 구조나 아이디어 확인
- `regular_risk_execution(정규 위험 실행)`: 위험을 가진 실행 연구
- `trade_shape(거래 형태)`: 거래 수, 보유 시간, 손실 곡선, 노출 패턴

## 규칙(Rule, 규칙)

서로 다른 레인(lane, 레인)을 같은 것처럼 비교하지 않는다.

탐색 KPI(exploration KPI, 탐색 KPI)는 승격 KPI(promotion KPI, 승격 KPI)가 아니어도 쓸모 있다.

## Tier-Paired KPI(티어 쌍 KPI)

Stage 10(10단계) 이후 alpha exploration KPI(알파 탐색 KPI)는 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)을 분리해서 적는다.

각 view(보기)는 같은 KPI 이름(KPI name, KPI 이름)을 유지한다.

- signal KPI(신호 KPI): hit rate(적중률), coverage(커버리지), long/short mix(롱/숏 비율), probability quality(확률 품질)
- trading KPI(거래 KPI): net profit(순수익), profit factor(수익 팩터), expectancy(기대값), trade count(거래 수), win rate(승률)
- risk KPI(위험 KPI): max drawdown(최대 손실), recovery factor(회복 계수), time under water(회복 전 체류 시간)
- execution KPI(실행 KPI): fill rate(체결률), skip/reject count(스킵/거부 수), spread/slippage(스프레드/슬리피지), external mismatch(외부 입력 불일치)

효과(effect, 효과)는 한 view(보기)의 좋은 숫자가 다른 view(보기)의 약점을 숨기지 못하게 하는 것이다.

## Routed Tier KPI(라우팅 티어 KPI)

Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) 방식의 MT5(`MetaTrader 5`, 메타트레이더5) 실행에서는 세 기록의 의미를 다음처럼 고정한다.

- Tier A(티어 A): `primary_used(우선 사용)` 구간
- Tier B(티어 B): `fallback_used(대체 사용)` 구간
- Tier A+B combined(Tier A+B 합산): `actual_routed_total(실제 라우팅 전체)`

효과(effect, 효과)는 Tier A(티어 A)와 Tier B(티어 B)를 따로 tester run(테스터 실행)으로 돌린 뒤 synthetic sum(합성 합산)을 전체 성과처럼 말하지 않게 하는 것이다.

한 routed account path(라우팅 계좌 경로) 안에서 per-tier PnL(티어별 손익)을 직접 추적하지 못하면, Tier A/Tier B component row(구성 행)는 profit(수익)을 주장하지 않는다. 그 행은 route count(경로 수), signal count(신호 수), fill/reject/skip(체결/거부/스킵)을 기록하고, net profit(순수익), profit factor(수익 팩터), expectancy(기대값), drawdown(손실 곡선)은 actual routed total(실제 라우팅 전체) 행에만 적는다.

효과(effect, 효과)는 수익 attribution(귀속)이 없는 구간별 성과를 만든 것처럼 보이지 않게 하는 것이다.

Tier B fallback(Tier B 대체) 행은 partial-context subtype counts(부분 문맥 하위유형 수), no_tier labelable count(티어 없음 라벨 가능 수), routed labelable count(라우팅 라벨 가능 수)를 함께 적는다.

효과(effect, 효과)는 Tier B(티어 B)가 실제로 어떤 빈 구간을 메웠는지와, 아직 all skip(전체 스킵)으로 남은 구간이 얼마나 되는지를 같은 KPI(핵심 성과 지표)에서 보게 하는 것이다.

MT5(`MetaTrader 5`, 메타트레이더5)나 strategy tester(전략 테스터)를 붙이면 `regular_risk_execution(정규 위험 실행)` 또는 `runtime_probe(런타임 탐침)` KPI 층을 반드시 둔다. 수익(profit, 수익)을 말하면 risk/execution KPI(위험/실행 KPI) 없이 positive(긍정)로 닫지 않는다.

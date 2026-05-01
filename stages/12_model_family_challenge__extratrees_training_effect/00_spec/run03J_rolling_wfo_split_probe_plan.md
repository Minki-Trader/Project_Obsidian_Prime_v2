# RUN03J Plan(계획)

## Hypothesis(가설)

RUN03H(실행 03H)의 validation/OOS inversion(검증/표본외 반전)은 single split(단일 분할) 착시일 수 있다. rolling WFO split probe(구르는 워크포워드 분할 탐침)로 반복성을 확인한다.

## Controls(고정 조건)

- model family(모델 계열): ExtraTrees(엑스트라트리)
- variants(변형): RUN03D(실행 03D) 20개 전체
- tiers(티어): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)
- claim boundary(주장 경계): `python_rolling_wfo_structural_probe_only_not_mt5_not_alpha_quality_not_promotion`

## Stop Condition(중단 조건)

fold(접힘 분할), tier(티어), ledger(장부), KPI record(KPI 기록) 중 하나라도 빠지면 completed(완료)로 닫지 않는다.

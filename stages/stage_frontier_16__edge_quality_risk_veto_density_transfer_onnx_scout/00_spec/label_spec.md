# Frontier16 Label Spec(프론티어16 라벨 명세)

Action(행동): train-only scale(학습 전용 척도)로 path return(경로 수익), adverse excursion(역행폭), early adverse excursion(초기 역행폭)을 묶은 3개 label variants(라벨 변형)를 고정합니다.

Effect(효과): label meaning(라벨 의미)을 F15(프론티어15)의 density threshold(빈도 임계값)와 분리해, edge quality(엣지 품질)를 새 상류 가설로 시험합니다.

- `f16b_edge_h8_t0p30_cap0p45_early0p25`: hold_bars(보유 봉수) `8`, target_multiplier(목표 배수) `0.3`, adverse_cap_multiplier(역행 상한 배수) `0.45`, early_adverse_cap_multiplier(초기 역행 상한 배수) `0.25`
- `f16b_edge_h8_t0p45_cap0p35_early0p20`: hold_bars(보유 봉수) `8`, target_multiplier(목표 배수) `0.45`, adverse_cap_multiplier(역행 상한 배수) `0.35`, early_adverse_cap_multiplier(초기 역행 상한 배수) `0.2`
- `f16b_edge_h12_t0p50_cap0p50_early0p30`: hold_bars(보유 봉수) `12`, target_multiplier(목표 배수) `0.5`, adverse_cap_multiplier(역행 상한 배수) `0.5`, early_adverse_cap_multiplier(초기 역행 상한 배수) `0.3`

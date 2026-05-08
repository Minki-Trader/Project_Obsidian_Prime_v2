# RUN28F Tier A Markov Vol/ADX Dependency Packet(28F 실행 티어 A 마르코프 변동성/ADX 의존성 묶음)
## Judgment(판정)
- run(실행): `run28F_tier_a_markov_vol_adx_component_dependency_probe_v1`
- status(상태): `reviewed_vol_adx_dependency_probe_completed`
- judgment(판정): `inconclusive_tier_a_markov_vol_adx_dependency_probe_completed`
- external verification(외부 검증): `completed`
- boundary(경계): `stage34_vol_adx_dependency_probe_only_no_baseline_no_promotion_no_runtime_authority`
- next action(다음 행동): `run28G_tier_a_markov_hold_management_runtime_probe_v1`

효과(effect, 효과): vol_high(고변동), adx_20_25(ADX 20-25), 2025-10(2025년 10월), feature_ready(피처 준비), hold duration(보유 기간)을 같은 근거 묶음에서 확인했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Component Read(구성요소 판독)
- Python validation(파이썬 검증) best PF(최고 수익 팩터): `exclude_adx_20_25` / `2.259087`
- Python OOS(파이썬 표본외) best net(최고 순손익): `exclude_vol_high` / `96.34`
- MT5 validation(MT5 검증) best PF(최고 수익 팩터): `exclude_adx_20_25` / `2.25`
- MT5 OOS(MT5 표본외) best PF(최고 수익 팩터): `exclude_vol_high_or_adx_20_25` / `1.43`

효과(effect, 효과): validation(검증)은 `adx_20_25` 제거 쪽이 더 설명력이 있고, OOS(표본외)는 `vol_high` 제거 쪽이 순손익을 더 살린다. union(합집합)은 PF(수익 팩터)는 좋지만 한 달 의존성이 남는다.

## October / Feature / Hold(10월 / 피처 / 보유)
- Python without 2025-10(파이썬 2025년 10월 제외): net(순손익) `4.91`, PF(수익 팩터) `1.051071`
- MT5 without 2025-10(MT5 2025년 10월 제외): net(순손익) `6.16`, PF(수익 팩터) `1.032409`
- hold read(보유 판독): validation/OOS avg hold bars(검증/표본외 평균 보유 봉) `377.271186` / `391.057143`

효과(effect, 효과): 긴 보유는 신호 자체만의 장점이 아니라 feature row omission(피처 행 제거)이 max hold(최대 보유) 평가 빈도를 낮춘 효과가 섞여 있다. 다음은 hold management runtime probe(보유 관리 런타임 탐침)가 맞다.

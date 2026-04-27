# run03D result summary(결과 요약)

## Boundary(경계)

- run(실행): `run03D_et_standalone_batch20_v1`
- scope(범위): Stage12 단독 ExtraTrees(엑스트라 트리) batch-20 structural scout(구조 탐색)
- no inheritance(비계승): Stage10/11(10/11단계) 모델, 임계값, 기준선, 승격 이력은 사용하지 않았다.
- external verification(외부 검증): `out_of_scope_by_claim_standalone_python_structural_scout`
- effect(효과): 이번 결과는 후보를 좁히는 데만 쓰고, MT5(`MetaTrader 5`, 메타트레이더5) 런타임 성능 주장으로 올리지 않는다.

## Package Read(패키지 판독)

- variants tested(시험 변형): `20`
- candidate count(후보 수): `0`
- best variant by package score(패키지 점수 기준 최상위): `v11_base_leaf20_q85`
- best validation hit(최상위 검증 적중): `0.392688` with `1477` signals(신호)
- best OOS hit(최상위 표본외 적중): `0.457317` with `1148` signals(신호)
- package judgment(패키지 판정): `inconclusive_standalone_batch20_structural_scout`

## Top Variants(상위 변형)

| rank(순위) | variant(변형) | val signals(검증 신호) | val hit(검증 적중) | oos signals(표본외 신호) | oos hit(표본외 적중) | score(점수) | judgment(판정) |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | v11_base_leaf20_q85 | 1477 | 0.392688 | 1148 | 0.457317 | 2.588295 | inconclusive_standalone_structural_scout |
| 2 | v19_context16_features_q90 | 985 | 0.393909 | 627 | 0.430622 | 2.444602 | inconclusive_standalone_structural_scout |
| 3 | v04_log2_features_leaf20_q90 | 985 | 0.385787 | 739 | 0.441137 | 2.407685 | inconclusive_standalone_structural_scout |
| 4 | v10_bootstrap70_leaf20_q90 | 985 | 0.382741 | 750 | 0.442667 | 2.382416 | inconclusive_standalone_structural_scout |
| 5 | v08_depth12_leaf20_q90 | 985 | 0.385787 | 745 | 0.452349 | 2.382016 | inconclusive_standalone_structural_scout |
| 6 | v09_depth8_leaf10_q90 | 985 | 0.392893 | 721 | 0.482663 | 2.353887 | inconclusive_standalone_structural_scout |
| 7 | v17_top30_features_q90 | 985 | 0.381726 | 792 | 0.460859 | 2.346678 | inconclusive_standalone_structural_scout |
| 8 | v13_base_margin002_q90 | 977 | 0.385875 | 768 | 0.472656 | 2.341653 | inconclusive_standalone_structural_scout |

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): completed(완료), 20 variants(변형), Python structural scout(파이썬 구조 탐색).
- Tier B separate(Tier B 분리): `out_of_scope_by_claim_standalone_tier_a_only`.
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_standalone_tier_a_only`.

## Failure Memory(실패 기억)

- validation/OOS(검증/표본외) 한쪽만 좋은 변형은 `mixed_unstable`로 낮춰 적었다.
- signal count(신호 수)가 너무 적은 변형은 `inconclusive_sparse`로 낮춰 적었다.
- effect(효과): 다음 MT5 probe(메타트레이더5 탐침) 후보를 고를 때 표본외 착시와 희소 신호 착시를 분리한다.

# RUN03L Recency Weighted Single Probe Plan(RUN03L 최근성 가중 단일 탐침 계획)

## Hypothesis(가설)

ExtraTrees(엑스트라 트리)는 최근 12개월 학습 표본을 더 크게 보면 fold(접힘) 안정성이 달라질 수 있다.

효과(effect, 효과): 아직 안 파본 training weight(학습 가중치) 축을 한 번만 본다.

## Controls(고정 조건)

- source variant(원천 변형): `v01_base_leaf20_q90`
- model family(모델 계열): `sklearn_extratreesclassifier_multiclass`
- threshold policy(임계값 정책): validation(검증) q90(90분위)
- tiers(티어): Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)

## Boundary(경계)

`runtime_probe_recency_weight_single_run_not_alpha_quality_not_promotion_not_runtime_authority`.

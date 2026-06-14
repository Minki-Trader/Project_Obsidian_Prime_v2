# Frontier39 Negative Memory(전선39 부정 기억)

Memory(기억): `f39_regime_gate_did_not_lift_pf_over_ungated_score_at_matched_density`

Action(행동): train-only regime gate(학습 전용 체제 게이트)가 ungated score(무게이트 점수) 대비 validation/OOS both(검증/표본밖 둘 다) +0.05 PF lift(수익 팩터 상승)를 만들지 못한 결과를 남긴다.

Effect(효과): 다음 frontier stage(전선 단계)에서 같은 shallow score(얕은 점수)에 regime bucket(체제 버킷)만 더 붙이는 반복을 막는다.

Do not repeat(반복 금지): same score cut + additional regime bucket expansion(같은 점수 컷 + 추가 체제 버킷 확장) without new source/exit asymmetry(새 원천/청산 비대칭 없음).

Runtime probe status(런타임 탐침 상태): `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f39_ablation_guardrail_fail`

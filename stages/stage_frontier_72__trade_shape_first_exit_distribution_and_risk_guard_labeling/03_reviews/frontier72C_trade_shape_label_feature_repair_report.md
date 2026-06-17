# Frontier72C Trade-Shape Label/Feature Repair(F72C 거래 형태 라벨/피처 수리)

Updated(갱신): 2026-06-17T00:33:09Z

- status(상태): `proxy_repair_completed`
- judgment(판정): `proxy_repair_preserved_scout_clue_pre_mt5_required_no_authority`
- candidate_count(후보 수): `1728`
- scout_clue_count(탐색 단서 수): `16`
- meaningful_candidate_count(의미 후보 수): `0`
- final_like_reference_only_count(최종 유사 참조 전용 수): `0`
- claim_boundary(주장 경계): `proxy_repair_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Best Repair Candidate(최선 수리 후보)

- candidate_id(후보 ID): `f72c_0098`
- shape/label/model/bundle(형태/라벨/모델/묶음): `short_h24_sl1.2_tp1.8` / `early_survival_045` / `small_nn_16` / `all58`
- validation net/PF/DD/tpd(검증 순수익/수익 팩터/손실폭/일거래): `3670.9137` / `1.2575` / `14.8770%` / `2.5000`
- OOS net/PF/DD/tpd(표본외 순수익/수익 팩터/손실폭/일거래): `4933.5061` / `1.3403` / `12.8125%` / `3.0103`
- scout/meaningful/final-like(탐색/의미/최종 유사): `True` / `False` / `False`

## Repair Interpretation(수리 해석)

Effect(효과): F72C는 라벨 엄격도와 피처 묶음을 바꿔 F72B scout clue(탐색 단서)를 유지/확대할 수 있는지 본다. 이 결과는 아직 proxy-only(프록시 전용)이며 runtime probe(런타임 탐침)를 대체하지 않는다.

## Next Action(다음 행동)

`frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1`.

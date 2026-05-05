# Decision(결정): Stage20-27 Characteristic and Actual MT5 Rerun Synthesis(20-27단계 특징 및 실제 MT5 재실행 종합)

Stage20~27(20~27단계)의 특징 파악과 actual MT5 rerun(실제 MT5 재실행) 보강을 `stage20_27_characteristic_synthesis_v1`와 `stage20_27_actual_mt5_rerun_verification_v1`로 기록한다.

효과(effect, 효과): GAM(일반화 가산 모델), ElasticNet Logistic(엘라스틱넷 로지스틱), HMM(은닉 마르코프 모델), supervised regime classifier(지도 국면 분류기), Survival model(생존 모델), hazard model(위험률 모델), NGBoost(자연 그래디언트 부스팅), quantile boosting(분위수 부스팅)의 보존 단서와 MT5 runtime_probe(MT5 런타임 탐침)를 실제 Strategy Tester(전략 테스터) 라우팅 재실행으로 묶어, Stage29~32(29~32단계)의 broad design(넓은 설계)에 쓸 수 있게 한다.

- report(보고서): `docs/workspace/stage20_27_characteristic_synthesis.md`
- packet(묶음): `docs/agent_control/packets/stage20_27_characteristic_synthesis_v1`
- actual MT5 rerun packet(실제 MT5 재실행 묶음): `docs/agent_control/packets/stage20_27_actual_mt5_rerun_verification_v1`
- judgment(판정): `completed_characteristic_and_actual_mt5_routed_rerun_synthesis_not_new_alpha_quality`
- claim boundary(주장 경계): `cross_stage_characteristic_and_actual_mt5_routed_rerun_synthesis_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 forensic boundary(MT5 포렌식 경계): Stage20~27(20~27단계)의 `routed_validation_is(검증 라우팅)`와 `routed_oos(표본외 라우팅)` 16개는 실제 재실행 완료. full tier-view rerun(전체 티어 보기 재실행)은 아님.
- active stage unchanged(활성 단계 유지): Stage28(28단계) `28_regime_model__markov_switching_regression_state_link`
- next exact action unchanged(다음 정확한 행동 유지): `repair_run22B_markov_regression_runtime_probe_then_rerun_exact_attempts`

효과(effect, 효과): Stage20~27(20~27단계)을 micro-probe(미세 탐침)로 다시 열지 않고, 필요한 경우에는 calibration/abstention(보정/기권), exit-only(청산 전용), WFO(워크포워드 최적화), runtime handoff repair(런타임 인계 수정) 같은 새 broad packet(넓은 묶음)으로만 재개한다.

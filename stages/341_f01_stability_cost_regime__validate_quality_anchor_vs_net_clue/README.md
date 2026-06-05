# Stage 341 F01 Stability Cost Regime Validation(341단계 F01 안정성 비용 국면 검증)

## Canonical Stage ID(정식 단계 ID)

`341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue`

## Stage Question(단계 질문)

Can the restored f01(에프01) close_on_flat=False(평탄 청산 꺼짐) clue survive stability(안정성), cost stress(비용 압박), and session/regime(세션/국면) validation without overstaying in Stage 340(340단계)?

## Source Handoff(원천 인계)

- source_stage(원천 단계): `340_runtime_lifecycle_exit__quality_balance_pressure_review`
- source_review_run(원천 검토 실행): `run340H_review_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`
- source_runtime_run(원천 런타임 실행): `run340G_execute_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`
- branch_run(분기 실행): `run341A_branch_stage340_to_f01_stability_cost_regime_validation_without_db_v1`
- next_run(다음 실행): `run341B_design_f01_stability_cost_regime_validation_without_db_v1`

## Preserved Clues(보존 단서)

- q01 quality anchor(품질 기준점): net_profit(순수익) `122.9`, profit_factor(수익 팩터) `1.89`, recovery_factor(회복 계수) `1.38`, drawdown(낙폭) `89.31`
- q09 net clue(순수익 단서): net_profit(순수익) `123.6`, profit_factor(수익 팩터) `1.9`, recovery_factor(회복 계수) `1.24`, drawdown(낙폭) `99.31`

Effect(효과): q09(큐09)를 winner(승자)로 고정하지 않고, q01(큐01)을 quality anchor(품질 기준점)로 붙여 비교한다.

## Scope(범위)

Stage 341(341단계)는 validation design(검증 설계), cost stress(비용 압박), session/regime split(세션/국면 분할), and equity curve quality(수익곡선 품질)를 다룬다.

## Forbidden Claims(금지 주장)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## run341C Validation Inputs(341C 검증 입력)

- run_id(실행 ID): `run341C_materialize_f01_stability_cost_regime_validation_inputs_without_db_v1`
- next_run(다음 실행): `run341D_review_f01_stability_cost_regime_validation_without_db_v1`
- effect(효과): run341D(341D 실행)가 수익 구조를 검토할 수 있게 했다.

# run340H F01 Close-On-Flat False Pressure Review(340H F01 평탄 청산 꺼짐 압박 검토)

## Summary(요약)

- run_id(실행 ID): `run340H_review_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`
- status(상태): `completed_stage340H_f01_close_on_flat_false_pressure_probe_reviewed_positive_clue_no_selection`
- judgment(판정): `f01_corrected_control_positive_runtime_probe_q09_net_clue_quality_tradeoff_forward_cost_session_missing_no_selection`
- gates(게이트): `9/9`
- exact_parity(정확 동등성): `58270/58270`, mismatch(불일치): `0`
- local_floor_pass_count(로컬 하한 통과 수): `7`
- best_attempt(최고 시도): `q09_s545_l51_m01_h12`
- best_net_profit(최고 순수익): `123.6`
- best_profit_factor(최고 수익 팩터): `1.9`
- best_expectancy(최고 기대값): `3.75`
- best_recovery_factor(최고 회복 계수): `1.24`
- best_drawdown(최고 낙폭): `99.31`
- exact_control_net_profit(정확 대조 순수익): `122.9`
- exact_control_profit_factor(정확 대조 수익 팩터): `1.89`
- next_run(다음 실행): `run341A_branch_stage340_to_f01_stability_cost_regime_validation_without_db_v1`

## Judgment(판정)

close_on_flat=False(평탄 청산 꺼짐)을 복구하자 f01(에프01) 표면은 다시 positive runtime clue(긍정 런타임 단서)가 됐다. q09(큐09)는 net_profit(순수익)이 가장 높지만 source f01(원본 f01) 대비 drawdown(낙폭)이 커지고 recovery_factor(회복 계수)가 낮아 quality tradeoff(품질 교환)가 있다.

Effect(효과): q09(큐09)를 단일 승자로 고정하지 않고, q01 exact control(정확 대조)과 q09 net-high clue(순수익 높은 단서)를 다음 stability/cost/regime(안정성/비용/국면) stage(단계)로 함께 넘긴다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

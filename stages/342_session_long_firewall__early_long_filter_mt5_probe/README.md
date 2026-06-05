# Stage 342(342단계)

Stage 342(342단계)는 q01/q09(큐01/큐09) positive clue(긍정 단서)를 early-long block(초반 롱 차단) side filter(사이드 필터)로 압박하는 runtime probe(런타임 탐침) 전용 단계다.

- current_run(현재 실행): `run342B_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1`
- branch_run(분기 실행): `run342A_branch_stage341_to_session_long_firewall_probe_without_db_v1`
- source(원천): `run341D_review_f01_stability_cost_regime_validation_without_db_v1`

Effect(효과): validation(검증), package(패키지), execution(실행), review(검토)가 한 Stage(단계)에 계속 쌓이지 않게 한다.

## run342C F01 Session-Long Firewall MT5 Probe(342C F01 세션 롱 방화벽 MT5 탐침)

- run_id(실행 ID): `run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1`
- summary(요약): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342C/f01_session_long_firewall_mt5_probe_summary.csv`
- diff(차이): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342C/proxy_mt5_runtime_difference.csv`
- effect(효과): run342D(342D 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.

## run342D F01 Session-Long Firewall Review(342D F01 세션 롱 방화벽 검토)

- run_id(실행 ID): `run342D_review_f01_session_long_firewall_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342D/session_long_firewall_review_scorecard.csv`
- queue(대기열): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342D/run342E_soft_session_long_firewall_probe_queue.csv`
- effect(효과): Stage342(342단계)를 더 가벼운 soft-window(부드러운 구간) 탐색으로 이어간다.

## run342E Soft Session-Long Firewall Package(342E 부드러운 세션 롱 방화벽 패키지)

- run_id(실행 ID): `run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342E/run342F_queue.csv`
- effect(효과): Stage342(342단계)가 soft-window(부드러운 구간) MT5 실행 단계로 넘어갈 수 있다.

## run342F Soft Session-Long Firewall MT5 Probe(342F 부드러운 세션 롱 방화벽 MT5 탐침)

- run_id(실행 ID): `run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1`
- summary(요약): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342F/soft_session_long_firewall_mt5_probe_summary.csv`
- diff(차이): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342F/proxy_mt5_runtime_difference.csv`
- effect(효과): run342G(342G 실행) review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.

## run342G Soft Firewall Review(342G 부드러운 방화벽 검토)

- run_id(실행 ID): `run342G_review_soft_session_long_firewall_mt5_probe_without_db_v1`
- scorecard(점수표): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342G/soft_session_long_firewall_review_scorecard.csv`
- queue(대기열): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342G/run342H_early_long_quality_margin_mix_queue.csv`
- effect(효과): Stage342(342단계)를 early-long quality gate(초반 롱 품질 게이트) 탐색으로 이어간다.

## run342H Early Long Quality Margin Mix Package(342H 초반 롱 품질/마진 혼합 패키지)

- run_id(실행 ID): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- queue(대기열): `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342H/run342I_queue.csv`
- effect(효과): Stage342(342단계)가 quality/margin(품질/마진) MT5 실행 단계로 넘어갈 수 있다.

## Stage343 Branch Handoff(343단계 분기 인계)

- branch_run(분기 실행): `run343A_branch_stage342_to_quality_margin_runtime_probe_without_db_v1`
- next_stage(다음 단계): `343_quality_margin_runtime__early_long_mix_mt5_probe`
- next_run(다음 실행): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- effect(효과): Stage 342(342단계)를 run342H package(342H 패키지)에서 멈추고, MT5 runtime probe(MT5 런타임 탐침)를 새 장부에서 시작한다.

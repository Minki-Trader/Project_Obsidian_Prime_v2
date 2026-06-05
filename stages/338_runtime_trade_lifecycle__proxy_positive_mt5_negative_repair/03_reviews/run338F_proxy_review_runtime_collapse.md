# run338F Proxy Review Runtime Collapse(프록시 검토 런타임 축약)

## Summary(요약)

- run_id(실행 ID): `run338F_review_group_safe_onnx_proxy_scores_for_mt5_probe_without_db_v1`
- status(상태): `completed_stage338F_proxy_review_runtime_collapse_required_no_mt5_no_selection`
- judgment(판정): `proxy_positive_after_runtime_timestamp_collapse_mt5_probe_package_required_no_selection`
- gates(게이트): `7/7`
- model_id(모델 ID): `logreg_balanced_c025`
- duplicate_timestamp_rows(중복 타임스탬프 행): `11654`
- collapsed_rows(축약 행): `5827`
- collapsed_proxy_net_log_return(축약 프록시 순로그수익): `0.0713393579`
- collapsed_proxy_profit_factor(축약 프록시 수익 팩터): `1.39846904`
- next_run(다음 실행): `run338G_materialize_runtime_collapsed_onnx_mt5_probe_package_without_db_v1`

## Action(행동)

run338E(338E 실행)의 proxy-positive(프록시 양수) 결과를 timestamp-unique runtime shape(타임스탬프 고유 런타임 형태)로 축약했다.
Effect(효과): MT5 runtime probe(MT5 런타임 탐침) 전에 중복 시각 문제를 숨기지 않고 패키지 가능한 입력으로 낮춘다.

## Evidence(근거)

- proxy review(프록시 검토): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338F/run338F_proxy_score_review.csv`
- timestamp audit(타임스탬프 감사): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338F/run338F_runtime_timestamp_uniqueness_audit.csv`
- collapsed proxy(축약 프록시): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338F/run338F_runtime_collapsed_proxy_score.csv`
- package queue(패키지 대기열): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338F/run338G_mt5_probe_package_queue.csv`

## Boundary(경계)

run338F(338F 실행)는 MT5 execution(MT5 실행)을 하지 않았다. Collapsed proxy(축약 프록시)는 MT5 KPI(MT5 핵심 성과 지표)가 아니며, run338G(338G 실행)의 runtime probe package(런타임 탐침 패키지) 입력일 뿐이다.

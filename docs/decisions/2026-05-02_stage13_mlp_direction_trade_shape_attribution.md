# 2026-05-02 Stage 13 MLP Direction Trade Shape Attribution

- run(실행): `run04G_mlp_direction_trade_shape_attribution_v1`
- source(원천): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- decision(결정): 방향별 거래 형태 기여도만 기록한다.
- OOS both damage(표본외 양방향 손상): `-130.62`
- OOS trade count delta(표본외 거래 수 차이): `0`
- short-only OOS bootstrap CI95(숏 전용 표본외 부트스트랩 95% 구간): `-138.35, 105.88, 328.45`
- boundary(경계): `trade_shape_attribution_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): 다음 탐색에서 short-only(숏 전용)를 기준선처럼 쓰지 않고, 작은 표본의 생존 단서로만 보존한다.

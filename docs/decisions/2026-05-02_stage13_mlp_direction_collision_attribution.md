# 2026-05-02 Stage13 MLP Direction Collision Attribution

- run(실행): `run04H_mlp_direction_collision_attribution_v1`
- source(원천): `run04F_mlp_direction_asymmetry_runtime_probe_v1`
- decision(결정): direct collision(직접 충돌)이 아니라 reverse sequence(반전 순서)와 close timing(청산 시각) 문제로 기록한다.
- OOS opposite position signal(표본외 반대 포지션 신호): `27`
- OOS net damage(표본외 순손상): `-130.62`
- boundary(경계): `collision_attribution_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): 다음 stage13(13단계) 탐색에서 같은 threshold(임계값)를 더 깊게 튜닝하기보다, 양방향 단일 계좌의 reversal policy(반전 정책)를 따로 흔들지 여부를 선택할 수 있다.

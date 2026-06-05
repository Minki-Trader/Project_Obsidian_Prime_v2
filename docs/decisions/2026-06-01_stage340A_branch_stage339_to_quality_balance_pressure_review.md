# 2026-06-01 Stage340A Branch Decision(340A 단계 분기 결정)

- decision(결정): `stage340A_open_run340B_review_quality_balance_blend_probe`
- from(출발): `339_runtime_lifecycle_exit__side_balance_probe_review` / `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- to(도착): `340_runtime_lifecycle_exit__quality_balance_pressure_review` / `run340B_review_quality_balance_blend_mt5_probe_without_db_v1`
- reason(이유): Stage339(339단계)가 너무 무거워져 quality-balance review(품질-균형 검토)를 별도 단계로 분리했다.

Action(행동): Stage340(340단계)를 열고 run340B(340B 실행)를 review(검토) 다음 행동으로 둔다.
Effect(효과): Stage339(339단계)의 무게를 줄이고, run339G(339G 실행) MT5 산출물을 버리지 않는다.

claim_boundary(주장 경계): `state_sync_stage_branch_and_quality_balance_runtime_probe_handoff_only_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

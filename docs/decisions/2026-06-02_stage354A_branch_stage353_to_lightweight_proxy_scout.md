# Decision(결정): Stage354A Branch(354A 단계 분기)

- date(날짜): `2026-06-02`
- source_stage(원천 단계): `353_trade_shape_offense__report_recovered_density_ok_edge_rebuild`
- new_stage(새 단계): `354_proxy_trade_shape_scout__small_candidate_queue`
- branch_run(분기 실행): `run354A_branch_stage353_to_lightweight_proxy_trade_shape_scout_without_db_v1`
- next_run(다음 실행): `run354B_lightweight_proxy_trade_shape_scan_without_db_v1`

Action(행동): Stage353(353단계)이 너무 무거워졌다는 사용자 판단을 받아, proxy scout(프록시 탐색)만 다루는 Stage354(354단계)를 열었다.

Effect(효과): 다음 실행은 작은 후보 대기열(candidate queue, 후보 대기열)을 만들고, MT5 runtime probe(MT5 런타임 탐침)는 그 다음 검증으로 분리된다.

Claim Boundary(주장 경계): `state_sync_stage_branch_user_requested_lightweight_proxy_scout_only_no_new_proxy_execution_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

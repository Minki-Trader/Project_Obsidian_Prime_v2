# 2026-06-01 Stage343A Branch Decision(343A 단계 분기 결정)

- decision(결정): `stage343A_open_run343B_execute_early_long_quality_margin_mix_probe`
- from(출발): `342_session_long_firewall__early_long_filter_mt5_probe` / `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- to(도착): `343_quality_margin_runtime__early_long_mix_mt5_probe` / `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- superseded_run(대체된 실행): `run342I_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- reason(이유): Stage 342(342단계)가 너무 무거워져 quality/margin runtime probe(품질/마진 런타임 탐침)를 새 단계로 분리한다.

Action(행동): Stage 343(343단계)를 열고 run343B(343B 실행)를 MT5 runtime probe(MT5 런타임 탐침) 다음 행동으로 둔다.
Effect(효과): run342H package(342H 패키지)의 계보는 보존하면서 다음 실행 장부를 새로 시작한다.

claim_boundary(주장 경계): `state_sync_stage_branch_quality_margin_runtime_handoff_only_no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

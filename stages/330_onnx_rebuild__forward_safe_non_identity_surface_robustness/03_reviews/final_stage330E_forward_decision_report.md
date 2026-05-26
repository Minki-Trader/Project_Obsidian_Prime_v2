# Stage330E Final Forward Decision Report(330E 최종 전진 판단 보고서)

- final_decision(최종 판단): `Forward Blocked(전진 차단)`
- status(상태): `blocked_raw_forward_mt5_runtime_probe_no_completed_runtime`
- judgment(판정): `raw_forward_runtime_probe_blocked_requires_runtime_repair_no_goal_achieve`
- completed_attempt_count(완료 시도 수): `0`
- blockers(차단 사유): `terminal_already_running_config_not_applied`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): raw-forward MT5(원본 전진 MT5) 테스터 출력이 없으면 수익성, PF(수익 팩터), DD(낙폭), curve pocket(곡선 포켓)으로 통과/실패를 판정하지 않는다.

Next(다음): `repair_stage330E_runtime_probe_blocker_then_rerun`

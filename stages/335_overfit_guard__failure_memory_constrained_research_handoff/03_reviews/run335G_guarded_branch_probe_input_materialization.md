# run335G Guarded Branch Probe Input Materialization(335G 방어 분기 탐침 입력 물질화)

- run_id(실행 ID): `run335G_materialize_guarded_branch_probe_inputs_v1`
- parent_run_id(부모 실행 ID): `run335F_design_guarded_branch_probe_protocols_v1`
- status(상태): `completed_guarded_branch_probe_inputs_materialized_no_selection`
- judgment(판정): `probe_inputs_materialized_research_only_no_goal_achieve`
- decision(결정): `stage335G_probe_inputs_materialized_ready_for_review_no_selection`
- packages(패키지): `11`
- proxy_mt5_readiness_rows(proxy-MT5 준비 행): `11`
- not_usable_yet(아직 사용 불가): `11`
- failed_gates(실패 게이트): `0`
- next_action(다음 행동): `run335H_review_guarded_branch_probe_input_materialization_v1`

Effect(효과): run335F(335F 실행)의 11개 protocol(계약)을 probe input spec(탐침 입력 명세), proxy expected manifest(프록시 예상값 목록), MT5 runtime result-or-block(MT5 런타임 결과 또는 차단 기록), comparison readiness(비교 준비도), negative control(부정 대조), stop condition(중단 조건), no-retune guard(무재튜닝 방어)로 물질화했다.

Proxy-vs-MT5 rule(프록시 대 MT5 규칙): 현재는 proxy expected value(프록시 예상값)와 MT5 runtime probe result(MT5 런타임 탐침 결과)가 모두 없으므로 usability(활용 가능성)는 `not_usable_yet`이다. 나중에 두 결과가 모두 생기면 net/PF/DD/trades/day/expectancy/recovery/curve pocket/underwater/lot-normalized/cost/session/side(순수익/수익팩터/손실/일거래수/기대값/회복/곡선 포켓/수중구간/로트 정규화/비용/세션/방향) 차이를 비교해야 한다.

Boundary(경계): model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

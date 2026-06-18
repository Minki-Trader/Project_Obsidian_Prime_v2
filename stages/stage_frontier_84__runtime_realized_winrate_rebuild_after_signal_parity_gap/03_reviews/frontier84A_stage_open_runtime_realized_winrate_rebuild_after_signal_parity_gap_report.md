# F84A Stage Open Runtime-Realized Win-Rate Rebuild(F84A 단계 개방 런타임 실현 승률 재구축)

Updated(갱신): 2026-06-18T09:15:23Z

- run id(실행 ID): `frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_v1`
- parent run(부모 실행): `frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1`
- status(상태): `opened_runtime_realized_winrate_rebuild_hypothesis_lifecycle_no_authority`
- judgment(판정): `frontier84_opened_runtime_realized_winrate_label_axis_after_f83_gap_no_authority`
- claim boundary(주장 경계): `frontier84_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Open Decision(개방 결정)

Action(행동): F84를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축) hypothesis lifecycle(가설 생명주기)로 연다.

Effect(효과): F83의 부정 근거를 반복하지 않고, 실제 MT5 승률이 무너진 원인을 새 label/target/risk axis(라벨/목표/위험 축)로 직접 시험한다.

## F83 Reference KPI(F83 참고 KPI)

- Runtime OOS(런타임 표본외): net/PF/DD/trades-day/win-rate(순손익/수익 팩터/손실폭/일 거래/승률) `-37.17/0.97/19.24/8.266666666666667/33.31`
- Primary gap cause(주 간극 원인): `runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식)`

## F84A Experiment Contract(F84A 실험 계약)

- hypothesis(가설): F83의 loss(손실)는 signal count mismatch(신호 수 불일치)가 아니라 runtime win-rate erosion(런타임 승률 침식)이므로, 다음 proxy(프록시)는 종가 방향 smooth_supply(부드러운 공급) 대신 runtime-realized outcome(런타임 실현 결과)을 직접 예측해야 한다.
- broad_sweep(넓은 탐색): runtime label family x stop-touch target x fill-path target x session/regime split x risk logic(런타임 라벨군 x 터치 목표 x 체결 경로 x 세션/장세 x 위험 로직)
- micro_search_gate(미세 탐색 게이트): only after a label family shows density and win-rate preservation(라벨군이 밀도와 승률 보존을 보인 뒤)
- next action(다음 행동): `frontier84B_runtime_realized_winrate_proxy_scout_v1`

## Claim Boundary(주장 경계)

F84A is open/design only(F84A는 개방/설계 전용). It does not create proxy KPI(프록시 KPI), runtime KPI(런타임 KPI), ONNX candidate(온엑스 후보), selected baseline(선택 기준선), or runtime authority(런타임 권위).

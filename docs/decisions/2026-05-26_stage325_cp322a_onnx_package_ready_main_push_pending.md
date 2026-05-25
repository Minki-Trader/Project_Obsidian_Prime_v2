# Stage325 Decision(325단계 결정): ONNX Package Ready, Main Push Pending(온엑스 패키지 준비, 메인 푸시 대기)

- run_id(실행 ID): `run325A_export_cp322a_adapter_to_onnx_and_runtime_reproduction_v1`
- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- Adapter package(어댑터 패키지): `stage323_cp322a_selected_curve_adapter_package_v1`
- status(상태): `completed_cp322a_onnx_export_parity_runtime_reproduction_package_ready_for_main_push`
- judgment(판정): `onnx_export_parity_and_mt5_runtime_reproduction_passed_main_push_pending`
- Goal Achieve(목표 달성): `complete_pending_main_push`
- next_action(다음 행동): `commit_and_push_main_then_mark_goal_achieved`

Effect(효과): ONNX export(온엑스 내보내기), Python inference check(파이썬 추론 확인), feature order parity(피처 순서 동등성), ONNX parity(온엑스 동등성), MT5 runtime reproduction(MT5 런타임 재현)을 하나의 패키지로 묶었다.

Boundary(경계): main push(메인 푸시)가 끝나기 전까지 Goal Achieved(목표 달성 완료)는 최종 선언하지 않는다.

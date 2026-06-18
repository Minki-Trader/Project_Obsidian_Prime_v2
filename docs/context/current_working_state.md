# Current Working State(현재 작업 상태)

Updated(갱신): 2026-06-18T07:22:10Z

Active stage(활성 단계): `stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation`

Current run(현재 실행): `frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1`

Latest completed run(최근 완료 실행): `frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1`

## Current Truth(현재 진실)

Action(행동): F83A stage open and exportable teacher distillation proxy(F83A 단계 개방 및 내보내기 가능 교사 증류 프록시)를 완료했다.

Effect(효과): F82 runtime-realized PnL(F82 런타임 실현 손익)을 teacher label(교사 라벨)로 사용해 ONNX-exportable seed(온엑스 내보내기 가능 씨앗)를 만들었다. 이 씨앗은 아직 MT5 runtime authority(런타임 권위)가 아니라 F83B Strategy Tester probe(F83B 전략 테스터 탐침) 대상이다.

## Key Evidence(핵심 근거)

- best seed(최선 씨앗): `f83a_0019` / `decision_tree_d4_balanced`
- OOS net/PF/DD/trades-day(표본외 순손익/수익 팩터/손실폭/일 거래): `24.019999999999996/1.3314932376483577/2.043823928640711/0.7098445595854922`
- ONNX parity max diff(온엑스 동등성 최대 차이): `2.970373558230932e-08`
- positive exportable seed count(양수 내보내기 가능 씨앗 수): `6`
- MT5 probe candidate count(MT5 탐침 후보 수): `2`
- two-sided status(양방향 상태): `not_satisfied_source_runtime_trades_are_long_only(원천 런타임 거래가 롱 전용이라 미충족)`

Claim boundary(주장 경계): `executed_trade_teacher_proxy_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

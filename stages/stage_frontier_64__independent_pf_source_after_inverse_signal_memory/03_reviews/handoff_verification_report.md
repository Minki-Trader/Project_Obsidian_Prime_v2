# F64C Handoff Verification(F64C 인계 검증)

Updated(갱신): 2026-06-16T00:32:08Z

Status(상태): `handoff_verification_failed_runtime_probe_blocked_no_authority(인계 검증 실패, 런타임 탐침 차단, 권위 없음)`

Judgment(판정): `blocked_handoff_adapter_mismatch(차단, 인계 어댑터 불일치)`

## Action And Effect(행동과 효과)

Action(행동): F64B composed signal(합성 신호)을 3-class runtime handoff ONNX(3분류 런타임 인계 온엑스)로 distill(증류)하고 original signal(원 신호)과 composite signal(합성 온엑스 신호)을 비교했다.

Effect(효과): 기존 MT5 EA(전문가 자문)가 이해하는 3분류 확률 형태로 F64 proxy(프록시)를 넘길 수 있는지 MT5 실행 전에 확인했다.

## Result Summary(결과 요약)

- handoff_pass(인계 통과): `False`
- source_best_candidate(원천 최선 후보): `f64b_f64b_hz_w36_h6_q75_eq55_hz65_h2_cd0`
- validation composite PF/density/DD(검증 합성 수익 팩터/빈도/손실폭): `1.02491` / `5.78689` / `5.48745%`
- OOS composite PF/density/DD(표본외 합성 수익 팩터/빈도/손실폭): `1.0211` / `5.81679` / `4.25972%`
- validation match/signal_diff/direction_mismatch(검증 일치율/신호 차이/방향 불일치): `0.861134` / `1030` / `0.250964`
- OOS match/signal_diff/direction_mismatch(표본외 일치율/신호 차이/방향 불일치): `0.861814` / `749` / `0.239051`
- ONNX parity(온엑스 동등성): `True`, max_abs_diff(최대 절대 차이) `2.84764e-07`

## Artifacts(산출물)

- final decision(최종 판단): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64C_handoff_verification_loss_cluster_hazard_v1/handoff_verification.json`
- parity summary(동등성 요약): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64C_handoff_verification_loss_cluster_hazard_v1/handoff_parity_summary.csv`
- composite model(합성 모델): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64C_handoff_verification_loss_cluster_hazard_v1/models/frontier64_composite_hazard_direction_handoff_extratrees_d8_l100_v1.onnx`

## Boundary(경계)

This is local handoff verification(로컬 인계 검증) only. It does not claim runtime authority(런타임 권위), promotion(승격), baseline(기준선), live readiness(실거래 준비), completion(완성), or Goal Achieve(목표 달성).

Next action(다음 행동): `frontier64D_handoff_adapter_repair_or_block_v1`.

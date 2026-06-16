# F64D Handoff Adapter Repair(F64D 인계 어댑터 수리)

Updated(갱신): 2026-06-16T00:40:18Z

Status(상태): `handoff_adapter_repair_passed_mt5_probe_ready_no_authority(인계 어댑터 수리 통과, MT5 탐침 준비, 권위 없음)`

Judgment(판정): `runtime_probe_ready_after_adapter_repair(어댑터 수리 후 런타임 탐침 준비)`

## Action And Effect(행동과 효과)

Action(행동): F64C composite handoff(합성 인계) 실패 후 direction adapter(방향 어댑터)와 runtime veto tape(런타임 차단 테이프)를 분리해 capped repair(상한 있는 수리) 2개를 시험했다.

Effect(효과): F64B proxy(프록시)의 binary hazard gate(이진 위험 게이트)를 직접 방향 모델로 바꾸지 않고, MT5 EA(전문가 자문)가 지원하는 차단 테이프 경로로 인계 불일치를 줄였다.

## Result Summary(결과 요약)

- repair_pass(수리 통과): `True`
- selected_adapter(선택 어댑터): `f64d_dir_veto_et_d8_l20_n300`
- validation repaired PF/density/DD(검증 수리 수익 팩터/빈도/손실폭): `1.07267` / `5.42077` / `4.31916%`
- OOS repaired PF/density/DD(표본외 수리 수익 팩터/빈도/손실폭): `1.10808` / `5.83969` / `3.15376%`
- validation match/signal_diff_ratio(검증 일치율/신호 차이 비율): `0.981715` / `0.0423231`
- OOS match/signal_diff_ratio(표본외 일치율/신호 차이 비율): `0.978507` / `0.0467317`
- ONNX parity(온엑스 동등성): `True`, max_abs_diff(최대 절대 차이) `3.5011e-07`

## Artifacts(산출물)

- final decision(최종 판단): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64D_handoff_adapter_repair_or_block_v1/handoff_adapter_repair.json`
- candidate summary(후보 요약): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64D_handoff_adapter_repair_or_block_v1/adapter_candidate_summary.csv`
- runtime veto tape(런타임 차단 테이프): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64D_handoff_adapter_repair_or_block_v1/runtime_veto_tape.csv`
- direction adapter ONNX(방향 어댑터 온엑스): `stages/stage_frontier_64__independent_pf_source_after_inverse_signal_memory/02_runs/frontier64D_handoff_adapter_repair_or_block_v1/models/f64d_dir_veto_et_d8_l20_n300.onnx`

## Boundary(경계)

This is handoff adapter repair(인계 어댑터 수리), not MT5 runtime probe(MT5 런타임 탐침) yet. It does not claim runtime authority(런타임 권위), promotion(승격), baseline(기준선), live readiness(실거래 준비), completion(완성), or Goal Achieve(목표 달성).

Next action(다음 행동): `frontier64E_mt5_runtime_probe_loss_cluster_hazard_v1`.

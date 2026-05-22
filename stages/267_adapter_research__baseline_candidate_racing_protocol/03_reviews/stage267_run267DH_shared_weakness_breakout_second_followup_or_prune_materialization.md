# Stage267 Run267DH Shared Weakness Second Follow-up/Prune Materialization(267단계 267DH 공유 약점 2차 후속/가지치기 물질화)

- status(상태): `run267DH_shared_weakness_breakout_second_followup_or_prune_materialized_execution_pending`
- source_design(원천 설계): `run267DG_stage267_shared_weakness_breakout_second_followup_or_prune_design_v1`
- source_materializer(원천 물질화): `run267DD_stage267_shared_weakness_breakout_second_followup_or_prune_materialization_v1`
- variants(변형): `7`
- attempts(시도): `11`
- held_rows(보류 행): `2`
- handoff_receipts(인계 영수증): `11`
- next_action(다음 행동): `run267DI_execute_shared_weakness_breakout_second_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

`run267DH`는 새 승자를 고른 것이 아니다. `run267DG`가 정한 생존/대조/압박/강등 큐를 실제 MT5(MetaTrader 5, 메타트레이더5) 실행 입력으로 묶었다. `s264_aia`, `s262_lih`, `s258_stc`, `s264_lc`는 실행 입력으로 만들고, `s264_aih`는 현재 파괴형 경로가 실패했기 때문에 보류했다.

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | variants(변형) | why(이유) |
|---|---|---:|---|
| `dg_q01_s264_aia_survivor_replacement_ablation_cross_period` | `materialized` | `2` | source run267DD artifacts are available and connected to run267DG decision use. |
| `dg_q02_s262_lih_validation_heavy_control_crosscheck` | `materialized` | `1` | source run267DD artifacts are available and connected to run267DG decision use. |
| `dg_q03_s258_stc_thin_supply_impulse_stress` | `materialized` | `3` | source run267DD artifacts are available and connected to run267DG decision use. |
| `dg_q04_s264_lc_weekday_dd_deescalation_control` | `materialized` | `1` | source run267DD artifacts are available and connected to run267DG decision use. |
| `dg_q05_s264_aih_prune_or_rebuild_supply_gate` | `held` | `0` | held because run267DF destructive prune failed; only new supply structure may reopen. |
| `dg_q06_runtime_adapter_handoff_gap_for_survivors` | `held` | `0` | converted into handoff receipts; no MT5 performance attempt. |

## Boundary(경계)

이 실행은 materialization(물질화)이다. MT5 실행, balance/equity curve(잔액/평가금 곡선) 검토, Adapter(어댑터) 확정, runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)는 아직 아니다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/attempt_manifest.csv`
- held_queue(보류 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/held_queue.csv`
- handoff_receipt(인계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/handoff_receipt.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/gate_audit.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DH/shared_weakness_breakout_second_followup_or_prune_materialization/review_result.json`

# run294A MT5 Outcome Relabel Directional Flip Materialization(294A MT5 결과 재라벨 방향 반전 물질화)

- run_id(실행 ID): `run294A_design_mt5_outcome_relabel_directional_flip_rebuild_v1`
- status(상태): `completed_mt5_outcome_relabel_directional_flip_candidates_materialized_no_selection`
- judgment(판정): `mt5_outcome_relabel_directional_flip_inputs_materialized_no_candidate_selection`
- branch_count(분기 수): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `run294B_execute_mt5_outcome_relabel_directional_flip_mt5_probe`

## Thesis(논제)

Stage293(293단계)는 밀도는 일부 맞췄지만 실제 MT5 net profit(순수익)이 모두 음수였다. Stage294(294단계)는 이 음수 결과를 보존 단서로 써서 full flip(전체 반전), cost-aware skip(비용 인식 회피), density trim(밀도 절단), smooth curve routing(곡선 완화 라우팅)을 새 decision surface(판단 표면)로 만든다.

## Scoreboard(점수표)

- `cp294A_cp293F_full_outcome_flip_hold5_surface`: mode(모드) `full_flip`, validation(검증) `1111.77`bp/`6.25` trades/day(일거래), OOS(표본외) `-617.67`bp/`7.33` trades/day(일거래), gates(관문) `passed/failed/failed`.
- `cp294B_cp293F_cost_aware_flip_skip_hold5_surface`: mode(모드) `cost_aware_flip_skip`, validation(검증) `1333.71`bp/`5.76` trades/day(일거래), OOS(표본외) `-562.14`bp/`5.84` trades/day(일거래), gates(관문) `passed/failed/failed`.
- `cp294C_cp293A_density_trimmed_flip_hold5_surface`: mode(모드) `density_trimmed_flip`, validation(검증) `247.79`bp/`9.26` trades/day(일거래), OOS(표본외) `-1016.40`bp/`9.19` trades/day(일거래), gates(관문) `passed/failed/failed`.
- `cp294D_cp293A_smooth_curve_flip_router_hold5_surface`: mode(모드) `smooth_curve_flip_router`, validation(검증) `1094.24`bp/`6.21` trades/day(일거래), OOS(표본외) `-931.24`bp/`6.21` trades/day(일거래), gates(관문) `passed/failed/failed`.
- `cp294E_cp293F_near_breakeven_flip_smoother_hold5_surface`: mode(모드) `near_breakeven_flip_smoother`, validation(검증) `896.10`bp/`5.92` trades/day(일거래), OOS(표본외) `-652.81`bp/`6.01` trades/day(일거래), gates(관문) `passed/failed/failed`.
- `cp294F_aggressive_cp293A_cp293F_union_flip_hold5_surface`: mode(모드) `aggressive_union_flip`, validation(검증) `978.06`bp/`9.84` trades/day(일거래), OOS(표본외) `-1501.51`bp/`9.73` trades/day(일거래), gates(관문) `passed/failed/failed`.

## MT5 Queue(MT5 대기열)

- `cp294A_cp293F_full_outcome_flip_hold5_surface` -> `run294A_cp294A_cp293F_full_outcome_flip_hold5` validation approx(검증 근사) `6.25`/day, OOS approx(표본외 근사) `7.33`/day
- `cp294B_cp293F_cost_aware_flip_skip_hold5_surface` -> `run294A_cp294B_cp293F_cost_aware_flip_skip_hold5` validation approx(검증 근사) `5.76`/day, OOS approx(표본외 근사) `5.84`/day
- `cp294C_cp293A_density_trimmed_flip_hold5_surface` -> `run294A_cp294C_cp293A_density_trimmed_flip_hold5` validation approx(검증 근사) `9.26`/day, OOS approx(표본외 근사) `9.19`/day
- `cp294D_cp293A_smooth_curve_flip_router_hold5_surface` -> `run294A_cp294D_cp293A_smooth_curve_flip_router_hold5` validation approx(검증 근사) `6.21`/day, OOS approx(표본외 근사) `6.21`/day
- `cp294E_cp293F_near_breakeven_flip_smoother_hold5_surface` -> `run294A_cp294E_cp293F_near_breakeven_flip_smoother_hold5` validation approx(검증 근사) `5.92`/day, OOS approx(표본외 근사) `6.01`/day
- `cp294F_aggressive_cp293A_cp293F_union_flip_hold5_surface` -> `run294A_cp294F_aggressive_cp293A_cp293F_union_flip_hold5` validation approx(검증 근사) `9.84`/day, OOS approx(표본외 근사) `9.73`/day

## Boundary(경계)

선택 후보, Adapter package(어댑터 패키지), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 주장하지 않는다. 이 산출물은 run294B(294B 실행) MT5 runtime probe(MT5 런타임 탐침) 입력이다.

# run50AU_stage56_composite_qda_route_density_repair_v1(Stage56 56단계 QDA 합성 라우트 밀도 수정)

- packet_id(작업 묶음 ID): `stage56_run50AU_composite_qda_route_density_repair_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- selected_research_baseline(선택 연구 기준선): `none`
- boundary(주장 경계): `progress_checkpoint(진행 점검); no live_readiness(실거래 준비 아님); no runtime_authority(런타임 권위 아님)`

## Hypothesis(가설)

Action(행동): nf200s25b(비평탄 200 가중 로지스틱) primary(우선)를 유지하고 QDA(이차 판별 분석) secondary(보조)를 primary flat/no-position(우선 관망/무포지션) 구간에만 낮은 threshold(문턱값)로 붙였다.
Effect(효과): 기존 low-confidence handoff(낮은 신뢰도 인계)가 primary(우선) 좋은 진입을 망가뜨렸는지 피하면서, OOS density(표본외 밀도)가 실제 추가 기회로 늘어나는지 본다.

## Variant Results(변형 결과)

| variant(변형) | mode(방식) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| qda85_s850_flat_trans_r030_h8 | primary_flat_secondary_qda_threshold_repair_s850_h8_c0_r030 | 6.382514 | 4.148718 | 1.16 | 1.05 | 479.46 | 119.0 | `weak_dense_engine_candidate_actual_routed_mt5` |
| qda85_s800_flat_trans_r030_h8 | primary_flat_secondary_qda_threshold_repair_s800_h8_c0_r030 | 6.382514 | 4.158974 | 1.16 | 1.07 | 479.46 | 150.8 | `weak_dense_engine_candidate_actual_routed_mt5` |
| qda85_s750_flat_trans_r030_h8 | primary_flat_secondary_qda_threshold_repair_s750_h8_c0_r030 | 6.377049 | 4.169231 | 1.17 | 1.07 | 504.24 | 148.67 | `weak_dense_engine_candidate_actual_routed_mt5` |
| qda85_s850_flat_trans_r030_h6 | primary_flat_secondary_qda_threshold_repair_s850_h6_c0_r030 | 6.726776 | 4.405128 | 1.06 | 1.06 | 165.43 | 120.35 | `weak_dense_engine_candidate_actual_routed_mt5` |
| qda85_s800_flat_trans_r030_h6 | primary_flat_secondary_qda_threshold_repair_s800_h6_c0_r030 | 6.726776 | 4.405128 | 1.06 | 1.07 | 165.43 | 142.01 | `weak_dense_engine_candidate_actual_routed_mt5` |
| qda85_s800_flat_trans_r060_h8 | primary_flat_secondary_qda_threshold_repair_s800_h8_c0_r060 | 5.262295 | 3.389744 | 1.11 | 1.12 | 277.91 | 213.64 | `weak_dense_engine_candidate_actual_routed_mt5` |

## Same-Move Audit(동일 이동 감사)

| variant(변형) | split(분할) | trades/day(일 거래) | cost exp(비용 압박 기대값) | same-move(동일 이동 비율) | 12bar density(12봉 후 밀도) | survives(생존) |
|---|---|---:|---:|---:|---:|---|
| qda85_s850_flat_trans_r030_h8 | validation_is | 6.382514 | -0.089503 | 0.608733 | 2.497268 | False |
| qda85_s850_flat_trans_r030_h8 | oos | 4.148718 | -0.352905 | 0.557478 | 1.835897 | False |
| qda85_s800_flat_trans_r030_h8 | validation_is | 6.382514 | -0.089503 | 0.608733 | 2.497268 | False |
| qda85_s800_flat_trans_r030_h8 | oos | 4.158974 | -0.314057 | 0.558570 | 1.835897 | False |
| qda85_s750_flat_trans_r030_h8 | validation_is | 6.377049 | -0.067918 | 0.608398 | 2.497268 | False |
| qda85_s750_flat_trans_r030_h8 | oos | 4.169231 | -0.317134 | 0.559656 | 1.835897 | False |
| qda85_s850_flat_trans_r030_h6 | validation_is | 6.726776 | -0.365613 | 0.600325 | 2.688525 | False |
| qda85_s850_flat_trans_r030_h6 | oos | 4.405128 | -0.359895 | 0.563446 | 1.923077 | False |
| qda85_s800_flat_trans_r030_h6 | validation_is | 6.726776 | -0.365613 | 0.600325 | 2.688525 | False |
| qda85_s800_flat_trans_r030_h6 | oos | 4.405128 | -0.334680 | 0.563446 | 1.923077 | False |
| qda85_s800_flat_trans_r060_h8 | validation_is | 5.262295 | -0.211412 | 0.498442 | 2.639344 | False |
| qda85_s800_flat_trans_r060_h8 | oos | 3.389744 | -0.176793 | 0.478064 | 1.769231 | False |

## Read(판독)

- best_variant(현재 최선 변형): `qda85_s800_flat_trans_r060_h8`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 계속 열림): `True`
- reason(이유): no composite route variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `evaluate_run50AU_then_pivot_or_repair`

## Best Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry

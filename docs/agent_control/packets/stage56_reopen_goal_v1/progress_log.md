# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(작업 묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 묶음): `run50AU_stage56_composite_qda_route_density_repair_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)

## Current Read(현재 판독)

- best_variant(현재 최선 변형): `qda85_s800_flat_trans_r060_h8`
- validation/OOS trades/day(검증/표본외 일 거래): `5.262295` / `3.389744`
- validation/OOS PF(검증/표본외 수익 팩터): `1.11` / `1.12`
- validation/OOS net(검증/표본외 순손익): `277.91` / `213.64`
- action(행동): QDA(이차 판별 분석) secondary(보조) threshold(문턱값)와 transition re-entry(전환 재진입)를 실제 MT5(메타트레이더5) validation/OOS(검증/표본외)로 시험했다.
- effect(효과): ExtraTrees(엑스트라트리스) branch(분기) 실패 뒤, OOS density(표본외 밀도)가 진짜 추가 기회인지 route source(라우트 원천) 축에서 다시 확인한다.

## Attempted Variants(시도 변형)

| variant(변형) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) |
|---|---:|---:|---:|---:|---:|---:|
| qda85_s850_flat_trans_r030_h8 | 6.382514 | 4.148718 | 1.16 | 1.05 | 479.46 | 119.0 |
| qda85_s800_flat_trans_r030_h8 | 6.382514 | 4.158974 | 1.16 | 1.07 | 479.46 | 150.8 |
| qda85_s750_flat_trans_r030_h8 | 6.377049 | 4.169231 | 1.17 | 1.07 | 504.24 | 148.67 |
| qda85_s850_flat_trans_r030_h6 | 6.726776 | 4.405128 | 1.06 | 1.06 | 165.43 | 120.35 |
| qda85_s800_flat_trans_r030_h6 | 6.726776 | 4.405128 | 1.06 | 1.07 | 165.43 | 142.01 |
| qda85_s800_flat_trans_r060_h8 | 5.262295 | 3.389744 | 1.11 | 1.12 | 277.91 | 213.64 |

## Failure Read(실패 판독)

- best_quality(최선 품질): `qda85_s800_flat_trans_r060_h8`는 OOS PF(표본외 수익 팩터) `1.12`를 지켰지만 OOS density(표본외 밀도) `3.389744/day`, cost-stressed expectancy(비용 압박 기대값) `-0.176793`, cooldown density(쿨다운 후 밀도) `1.769231/day` 때문에 실패했다.
- closest_density(밀도 최접근): `qda85_s800_flat_trans_r030_h6`는 OOS density(표본외 밀도) `4.405128/day`까지 회복했지만 validation/OOS PF(검증/표본외 수익 팩터) `1.06` / `1.07`, cost-stressed expectancy(비용 압박 기대값) `-0.365613` / `-0.334680`, same-move ratio(동일 이동 비율) `0.600325` / `0.563446` 때문에 실패했다.
- attribution(기여도): quality branch(품질 분기) OOS(표본외)는 range/adx_lt20(횡보/ADX 20 미만) `233.75`, early session(초반 세션) `199.72`가 강하지만 mid session(중간 세션) `-50.26`, adx_20_25(ADX 20-25) `-40.03`이 약하다. density branch(밀도 분기) OOS(표본외)는 early session(초반 세션) `332.74`, adx_20_25(ADX 20-25) `100.58`이 강하지만 late/mid session(후반/중간 세션) `-124.88` / `-65.85`, adx_gt25(ADX 25 초과) `-94.45`가 약하다.
- next_hypothesis_branch(다음 가설 가지): `run50AV_new_source_density_survival_branch`

# Stage56 run50BT BaselineAdapter MT5 Development(56단계 run50BT 기준선 어댑터 MT5 개발)

- terminal_label(종료 라벨): `adapter_first_mt5_validation_oos_completed`
- development_anchor(개발 기준점): `run50BR/v64_v47_ctxgap14_refill_etfw_h2_no_b`
- selected_research_baseline(선택 연구 기준선): `none`
- backup_anchor(예비 기준점): `run50BQ/v60_v47_et_stable_damage_firewall_h2c0_no_b`
- external_verification_status(외부 검증 상태): `completed`
- adapter_result_read(어댑터 결과 판독): `degraded_anchor`

Action(행동): 기존 run50BR anchor(기준점)의 entry signal(진입 신호)을 BaselineAdapter(기준선 어댑터) 경로로 복제하고 risk/ATR/telemetry(위험/ATR/텔레메트리)를 켠 뒤 실제 MT5 validation/OOS(검증/표본외)를 실행했다.
Effect(효과): broad candidate hunting(넓은 후보 탐색)을 멈추고 adapter path(어댑터 경로)의 첫 실제 tester evidence(테스터 근거)를 만들었다.

## Anchor Comparison(기준점 비교)

| item | val day | oos day | val PF | oos PF | val net | oos net |
|---|---:|---:|---:|---:|---:|---:|
| development_anchor | 8.918033 | 6.358974 | 1.210000 | 1.220000 | 478.850000 | 397.640000 |
| backup_anchor | 9.617486 | 6.948718 | 1.180000 | 1.220000 | 462.210000 | 436.330000 |

## Adapter MT5 Result(어댑터 MT5 결과)

| split | view | day | PF | net | trades | max DD | cost exp | same move | MFE | floor count | max risk | report |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| validation_is | tier_a_only | 9.644809 | 0.920000 | -465.96 | 1765.00 | 621.75 |  |  |  | 0.000000 | 0.050000 | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BT/mt5/reports/Project_Obsidian_Prime_v2_run50BT_stage56_baseline_adapter_v64_mt5_v1_ba01_ta_val.htm |
| validation_is | actual_routed_total | 9.644809 | 0.920000 | -465.96 | 1765.00 | 621.75 | -0.764000 | 0.464589 | 0.625547 | 0.000000 | 0.050000 | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BT/mt5/reports/Project_Obsidian_Prime_v2_run50BT_stage56_baseline_adapter_v64_mt5_v1_ba01_rt_val.htm |
| oos | tier_a_only | 6.794872 | 1.210000 | 2239.00 | 1325.00 | 979.28 |  |  |  | 0.000000 | 0.050000 | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BT/mt5/reports/Project_Obsidian_Prime_v2_run50BT_stage56_baseline_adapter_v64_mt5_v1_ba01_ta_oos.htm |
| oos | actual_routed_total | 6.794872 | 1.210000 | 2239.00 | 1325.00 | 979.28 | 1.189811 | 0.509434 | 0.642008 | 0.000000 | 0.050000 | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BT/mt5/reports/Project_Obsidian_Prime_v2_run50BT_stage56_baseline_adapter_v64_mt5_v1_ba01_rt_oos.htm |

## Tier B Policy(Tier B 정책)

- status(상태): `disabled`
- reason(이유): Tier B fallback-only MT5 was not run in the adapter path because run50BR evidence showed Tier B fallback-only validation/OOS net -94.14 / -254.32.

## Risk Telemetry(위험 텔레메트리)

| attempt | status | rows | floor count | max model risk | max actual risk | avg lot | avg ATR |
|---|---|---:|---:|---:|---:|---:|---:|
| ba01_ta_val | completed | 9844.00 | 0.000000 | 0.050000 | 0.050000 | 0.050012 | 3634.40 |
| ba01_rt_val | completed | 9844.00 | 0.000000 | 0.050000 | 0.050000 | 0.050012 | 3634.40 |
| ba01_ta_oos | completed | 7584.00 | 0.000000 | 0.050000 | 0.050000 | 0.131734 | 3903.36 |
| ba01_rt_oos | completed | 7584.00 | 0.000000 | 0.050000 | 0.050000 | 0.131734 | 3903.36 |

Known weaknesses(알려진 약점): cost-stressed expectancy(비용 압박 기대값), same-move density(동일 이동 밀도), and whether dynamic risk/ATR(동적 위험/ATR)이 PF/net(수익 팩터/순손익)을 훼손하는지.

Judgment(판정): `adapter_first_mt5_validation_oos_completed`. No live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준)를 주장하지 않는다.

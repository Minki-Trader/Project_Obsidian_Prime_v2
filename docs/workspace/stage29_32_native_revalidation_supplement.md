# Stage29-32 Native Revalidation Supplement(29-32단계 원본 재검증 보강)

## Dependency Recovery(의존성 복구)

- river(리버): `0.24.2`
- torch(파이토치): `2.11.0`, cuda(CUDA 가속): `False`
- pytorch-tabnet(파이토치 탭넷): `4.1.0`

효과(effect, 효과): 이전 proxy(대리) 조건을 native package(원본 패키지) 재검증으로 보강했다. MT5(`MetaTrader 5`, 메타트레이더5)는 계속 score-table handoff(점수표 인계) 검증이므로 runtime authority(런타임 권위)는 아니다.

| stage(단계) | scout run(탐색 실행) | runtime run(런타임 실행) | MT5 status(MT5 상태) | MT5 KPI(MT5 핵심 성과 지표) | normalized(정규화) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) |
|---|---|---|---|---:|---:|---:|---:|
| Stage29(29단계) | `run23C_river_native_online_learning_scout_v1` | `run23D_river_native_online_runtime_probe_v1` | `completed` | `10` | `6` | `-115.71/0.93` | `-202.2/0.83` |
| Stage30(30단계) | `run24C_native_source_calibration_abstention_scout_v1` | `run24D_native_source_calibration_runtime_probe_v1` | `completed` | `10` | `6` | `44.19/1.27` | `-1.32/0.69` |
| Stage31(31단계) | `run25C_tabnet_native_attentive_tabular_scout_v1` | `run25D_tabnet_native_attentive_runtime_probe_v1` | `completed` | `10` | `6` | `-498.33/0.6` | `-4.32/1.0` |
| Stage32(32단계) | `run26C_torch_tcn_native_temporal_scout_v1` | `run26D_torch_tcn_native_temporal_runtime_probe_v1` | `completed` | `10` | `6` | `75.26/1.04` | `111.77/1.07` |

## Residual Stage Scan(잔여 단계 스캔)

- Stage20-27(20-27단계): prior actual MT5 synthesis(기존 실제 MT5 종합) 보존. 새 미세 탐색(micro search, 미세 탐색)은 열지 않았다.
- Stage28(28단계): Markov supplement(마르코프 보강) 기록 보존.
- Stage29-32(29-32단계): native revalidation(원본 재검증) 완료.

효과(effect, 효과): 같은 stage(단계) 안에서 의미 없는 미세조정 대신, 남은 큰 blocker(차단 요소)였던 native package gap(원본 패키지 격차)을 닫았다. 다음 탐색은 Stage33(33단계) 같은 새 topic pivot(주제 전환)이 더 적절하다.

## Boundary(경계)

`native_revalidation_supplement_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

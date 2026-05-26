# Stage337N Fresh MT5 Runtime Probe Or Block(337N 신규 MT5 런타임 탐침 또는 차단)

- run_id(실행 ID): `run337N_attempt_fresh_mt5_runtime_probe_or_block_v1`
- status(상태): `completed_stage337N_fresh_mt5_runtime_probe_attempt_partial_or_block_no_forward_decision`
- judgment(판정): `fresh_mt5_runtime_probe_attempt_has_runtime_or_feature_gap_requires_repair`
- decision(결정): `stage337N_runtime_probe_needs_repair_before_forward_or_selection_judgment`
- latest US100 close(최신 US100 종가): `2026-05-27T01:15:00Z`
- MT5 completed(MT5 완료): `4/4`
- feature handoff gap(피처 인계 공백): `2/4`
- core56 blocker(core56 차단): `1`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Effect(효과)

run337N은 최신 브로커 봉까지 m48/u42 feature handoff(피처 인계)를 다시 만들고 MT5(메타트레이더5) 런타임으로 확인한다. core56은 최신 source(원천) 문제가 아직 있어 별도 blocker(차단 사유)로 남긴다.

## Runtime Rows(런타임 행)

| attempt(시도) | status(상태) | net(순익) | PF(손익비) | trades(거래수) | DD(드로다운) |
|---|---:|---:|---:|---:|---:|
| `m48_bal_rf` | `completed/completed/completed` | `28.34` | `1.04` | `288` | `143.61` |
| `m48_plain_rf` | `completed/completed/completed` | `275.31` | `1.48` | `279` | `77.96` |
| `u42_bal_rf` | `completed/completed/completed` | `-20.63` | `0.98` | `343` | `163.25` |
| `u42_plain_rf` | `completed/completed/completed` | `99.9` | `1.13` | `344` | `112.86` |

## Boundary(경계)

이 실행은 forward decision(전진 판정)이 아니라 attribution/reair input(귀속/수리 입력)이다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화)은 수행하지 않았다.

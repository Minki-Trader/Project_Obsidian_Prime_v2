# Stage19 EBM MT5 Runtime Batch(19단계 EBM MT5 런타임 묶음)

- judgment(판정): `inconclusive_ebm_mt5_runtime_batch_completed`
- completed runs(완료 실행): `6` / `6`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `70`
- boundary(경계): `ebm_mt5_runtime_probe_batch_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- recommendation(권고): `preserve_visible_axes_and_consider_one_attribution_followup`

| run(실행) | topic(주제) | external verification(외부 검증) | KPI records(KPI 기록) | runtime failure(런타임 실패) | model ok(모델 성공) | model failure samples(모델 실패 표본) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS trades(표본외 거래 수) |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| `run13B` | `q90_runtime_handoff_feasibility` | `completed` | `10` | `None` | `41712` | `0` | `-52.24` | `0.95` | `191` |
| `run13C` | `q80_signal_density_pressure` | `completed` | `10` | `None` | `41712` | `0` | `-360.74` | `0.79` | `348` |
| `run13D` | `q95_sparse_tail_extreme` | `completed` | `10` | `None` | `41712` | `0` | `-151.86` | `0.75` | `101` |
| `run13E` | `q80_long_short_direction_asymmetry` | `completed` | `20` | `None` | `83424` | `0` | `-70.81` | `0.93` | `206` |
| `run13F` | `q90_hold6_trade_shape_stress` | `completed` | `10` | `None` | `41712` | `0` | `39.65` | `1.04` | `253` |
| `run13G` | `q90_hold18_trade_shape_stress` | `completed` | `10` | `None` | `41712` | `0` | `-92.07` | `0.91` | `166` |

효과(effect, 효과): RUN13B~RUN13G(실행13B~13G)는 EBM(설명가능 부스팅 머신) score table(점수표)을 MQL5(엠큐엘5) 직접 계산으로 인계해 MT5(메타트레이더5) Strategy Tester(전략 테스터)에서 넓게 관찰한 runtime_probe(런타임 탐침)이다.

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).

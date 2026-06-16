# F64E Runtime Probe Report(F64E 런타임 탐침 보고)

- judgment(판정): `negative_memory_runtime_probe_quality_gap_no_authority(부정 기억, 런타임 탐침 품질 차이, 권위 없음)`
- run(실행): `frontier64E_mt5_runtime_probe_loss_cluster_hazard_v1`
- adapter(어댑터): `f64d_dir_veto_et_d8_l20_n300`

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|
| validation_is | completed | completed | 0.35 | 28.23 | 6.0 | -2973 | 0 |
| oos | completed | completed | 0.7 | 7.92 | 6.396946564885496 | -2483 | 0 |

Action(행동): F64D direction adapter ONNX(방향 어댑터 온엑스)와 runtime veto tape(런타임 차단 테이프)를 MT5 Strategy Tester(MT5 전략 테스터)에 전달했다.

Effect(효과): proxy(프록시)에서 줄인 handoff gap(인계 차이)이 실제 EA(전문가 자문)와 tester economics(테스터 경제성)에서도 유지되는지 관찰했다.

Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).

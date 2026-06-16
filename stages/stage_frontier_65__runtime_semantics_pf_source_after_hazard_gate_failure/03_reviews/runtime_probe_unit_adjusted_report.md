# F65C Unit-Adjusted Runtime Probe(F65C 단위 보정 런타임 탐침)

- judgment(판정): `runtime_probe_observation_sltp_unit_clue_supported_economics_incomplete_no_authority(런타임 탐침 관찰, 손절/익절 단위 단서 지원, 경제성 불완전, 권위 없음)`
- run(실행): `frontier65C_targeted_sltp_unit_runtime_probe_v1`
- adapter(어댑터): `f64d_dir_veto_et_d8_l20_n300`
- Grok pre-MT5(비싼 MT5 전 그록): `accepted_with_local_verification(수용, 로컬 검증 포함)`

| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|
| validation_is | completed | completed | 0.97 | 21.83 | 5.442622950819672 | -2199 | 0 |
| oos | completed | completed | 1.11 | 14.66 | 5.816793893129771 | -1892 | 0 |

## Exit Shape Delta(청산 형태 변화)

| split(분할) | F64E stop%(기존 손절률) | F65C stop%(보정 손절률) | F64E maxhold%(기존 최대보유률) | F65C close_max_hold%(보정 최대보유 청산률) | median hold sec(중앙 보유초) |
|---|---:|---:|---:|---:|---:|
| oos | 67.54% | 26.38% | 0.00% | 62.47% | 600 |
| validation_is | 79.51% | 25.90% | 0.00% | 64.76% | 600 |

Action(행동): F64D direction adapter ONNX(방향 어댑터 온엑스)와 runtime veto tape(런타임 차단 테이프)는 유지하고, ATR SL/TP points(ATR 손절/익절 포인트)를 proxy price units(프록시 가격 단위)에 맞게 100배로 보정해 MT5 Strategy Tester(MT5 전략 테스터)를 실행했다.

Effect(효과): F65B의 unit-semantics clue(단위 의미 단서)가 실제 runtime economics(런타임 경제성) 차이를 줄이는지 관찰한다.

Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).

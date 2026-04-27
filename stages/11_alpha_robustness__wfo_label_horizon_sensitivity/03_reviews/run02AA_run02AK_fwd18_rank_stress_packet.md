# RUN02AA~RUN02AK fwd18 Rank Stress Packet

## Subject(대상)

- packet_id(묶음 ID): `run02AA_run02AK_fwd18_rank_stress_packet_v1`
- stage(단계): `11_alpha_robustness__wfo_label_horizon_sensitivity`
- source idea(원천 아이디어): RUN02Z(실행 02Z) fwd18 inverse rank + DI/ADX context(fwd18 역방향 순위 + DI/ADX 문맥)
- boundary(경계): `runtime_probe(런타임 탐침)`와 `stress_read(압박 판독)` only(전용)

효과(effect, 효과): RUN02Z(실행 02Z)를 바로 승격하지 않고, 같은 아이디어가 ADX cutoff(ADX 절단값), routing(라우팅), session slice(세션 구간)에 얼마나 버티는지 확인했다.

## ADX and Routing Results(ADX와 라우팅 결과)

| run(실행) | gate/routing(게이트/라우팅) | signals A/B/AB(신호 A/B/합산) | validation net/PF/trades(검증 순수익/수익 팩터/거래) | OOS net/PF/trades(표본외 순수익/수익 팩터/거래) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02AA(실행 02AA) | `ADX<=20` routed(라우팅) | `10/6/16` | `480.75 / 446.14 / 7` | `31.62 / 2.80 / 2` | validation-heavy(검증 치우침), OOS(표본외) 너무 얇음 |
| RUN02Z(실행 02Z) | `ADX<=25` routed(라우팅) | `20/9/29` | `386.06 / 7.25 / 9` | `352.63 / 52.03 / 5` | best center(최고 중심) |
| RUN02AB(실행 02AB) | `ADX<=30` routed(라우팅) | `24/10/34` | `377.02 / 13.47 / 10` | `294.95 / 9.20 / 5` | survives(생존), but weaker than center(중심보다 약함) |
| RUN02AC(실행 02AC) | `ADX<=20` Tier A-only(Tier A 단독) | `10/6/16` | `253.37 / 3.61 / 4` | `0.00 / 0.00 / 0` | no OOS trades(표본외 거래 없음) |
| RUN02AD(실행 02AD) | `ADX<=25` Tier A-only(Tier A 단독) | `20/9/29` | `438.21 / 8.67 / 7` | `241.95 / 0.00 / 2` | positive but thinner(양수지만 더 얇음) |
| RUN02AE(실행 02AE) | `ADX<=30` Tier A-only(Tier A 단독) | `24/10/34` | `397.54 / 17.29 / 8` | `239.77 / 0.00 / 2` | positive but not better than routed(양수지만 라우팅보다 약함) |

효과(effect, 효과): Tier B fallback(Tier B 대체)은 OOS(표본외) 거래 밀도와 순수익을 보탠다. 특히 `ADX<=25`에서 routed(라우팅)는 OOS `352.63 / 5 trades(거래)`이고 Tier A-only(Tier A 단독)는 `241.95 / 2 trades(거래)`라, 대체를 끄는 쪽이 더 강하다는 가설은 약해졌다.

## Session Slice Results(세션 구간 결과)

| run(실행) | session slice(세션 구간) | signals A/B/AB(신호 A/B/합산) | validation net/PF/trades(검증 순수익/수익 팩터/거래) | OOS net/PF/trades(표본외 순수익/수익 팩터/거래) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02AI(실행 02AI) | `190-210` | `20/7/27` | `587.28 / 10.61 / 9` | `99.34 / 20.18 / 5` | validation strongest(검증 최강), OOS recovery(표본외 회복) 약함 |
| RUN02AJ(실행 02AJ) | `195-215` | `21/8/29` | `460.98 / 9.07 / 9` | `227.12 / 10.91 / 6` | balanced but below center(균형이나 중심보다 낮음) |
| RUN02Z(실행 02Z) | `200-220` | `20/9/29` | `386.06 / 7.25 / 9` | `352.63 / 52.03 / 5` | best OOS center(표본외 최고 중심) |
| RUN02AK(실행 02AK) | `205-225` | `16/8/24` | `308.70 / 6.31 / 9` | `233.30 / 31.66 / 4` | survives with low OOS DD(낮은 표본외 손실로 생존) |

효과(effect, 효과): `200-220` 중심은 아직 OOS net/recovery(표본외 순수익/회복)가 가장 좋다. `195-215`와 `205-225`는 보조 확인 후보이고, `190-210`은 validation(검증)에 과하게 기운다.

## Judgment(판정)

- judgment_label(판정 라벨): `positive_tiny_sample_stress_survived_center_not_promotion(작은 표본 중심 생존, 승격 아님)`
- what_survived(살아남은 것): fwd18 inverse rank + `DI spread<=8`, `ADX<=25`, `200-220`, routed fallback(라우팅 대체)
- what_weakened(약해진 것): `ADX<=20`, Tier A-only(Tier A 단독), `190-210` validation-heavy(검증 치우침)
- still_missing(아직 부족): 거래 수가 validation(검증) `9`, OOS(표본외) `5` 근처라 alpha quality(알파 품질), live readiness(실거래 준비), promotion_candidate(승격 후보)는 아니다.

효과(effect, 효과): RUN02Z(실행 02Z)는 폐기할 이유가 줄었지만, 운영 의미(operational meaning, 운영 의미)는 여전히 없다. Stage 11(11단계) 안에서는 `ADX<=25`, routed(라우팅), `200-220` 중심이 가장 값진 닫힌 단서로 남는다.

## Artifact Paths(산출물 경로)

- plan(계획): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/00_spec/run02AA_run02AK_fwd18_rank_stress_plan.md`
- packet(묶음): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/run02AA_run02AK_fwd18_rank_stress_packet.md`
- representative run(대표 실행): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02Z_lgbm_fwd18_inverse_rank_context_v1`
- new MT5 runs(새 MT5 실행): `RUN02AA/RUN02AB/RUN02AC/RUN02AD/RUN02AE/RUN02AI/RUN02AJ/RUN02AK`
- source artifact runs(원천 산출물 실행): `RUN02AF/RUN02AG/RUN02AH`
- stage ledger(단계 장부): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/stage_run_ledger.csv`
- project ledger(프로젝트 장부): `docs/registers/alpha_run_ledger.csv`

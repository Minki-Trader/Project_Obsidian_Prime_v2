# Stage102 OOS Net Density/DD Repair Report(102단계 표본외 순손익 밀도/손실률 수리 보고서)

- run(실행): `run102A_stage102_v41_oos_net_density_dd_repair_v1`
- source_stage(원천 단계): `101_adapter_research__v41_context_gate_followup_review`
- source_stage101_closeout_commit(원천 101단계 종료 커밋): `30470ff25b02787f2aabfe8d78d1bf729c36bc72`
- source_stage101_latest_commit(원천 101단계 최신 커밋): `172104e12a1f8dda9352d5f84c668d2467a7adb3`
- source_stage100_latest_commit(원천 100단계 최신 커밋): `ef4b4ab1fbcb63a985512af5a6c49d199533e1fd`
- source_adapter(원천 어댑터): `s100_v41_h3_cd8_lng_early_adx20`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_oos_net_density_followup_review_in_stage103`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage100 best(100단계 최선)의 OOS PF(표본외 수익 팩터)를 보존하면서 OOS net(표본외 순손익), trade density(거래 밀도), DD%(손실률)를 34D target surface(34D 목표 표면)에 더 가깝게 만들 수 있는가?

Effect(효과): Stage102(102단계)는 세 가지 변형만 실제 MT5 runtime(실행환경)으로 재측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | expectancy(기대값) |
|---|---|---:|---:|---:|---:|---:|
| s102_v41_h3_cd7_lng_early_adx20 | validation_is | 1.710000 | 1272.60 | 16.43 | 200 | 6.3600 |
| s102_v41_h3_cd7_lng_early_adx20 | oos | 1.590000 | 607.95 | 18.69 | 150 | 4.0500 |
| s102_v41_h3_cd6_lng_early_adx20 | validation_is | 1.710000 | 1272.60 | 16.43 | 200 | 6.3600 |
| s102_v41_h3_cd6_lng_early_adx20 | oos | 1.600000 | 623.78 | 18.69 | 151 | 4.1300 |
| s102_v41_h3_cd8_lng_early_adx18 | validation_is | 1.670000 | 1186.27 | 17.54 | 202 | 5.8700 |
| s102_v41_h3_cd8_lng_early_adx18 | oos | 1.610000 | 639.85 | 18.56 | 152 | 4.2100 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s102_v41_h3_cd8_lng_early_adx18`
- oos_pf(표본외 수익 팩터): `1.610000` versus stage100_best(100단계 최선) `1.584029` and 34D latest(34D 최신) `1.583157`
- oos_net(표본외 순손익): `639.85` versus stage100_best(100단계 최선) `605.06` and 34D latest(34D 최신) `987.6`
- oos_dd_pct(표본외 손실률): `18.56` versus stage100_best(100단계 최선) `18.69` and 34D latest(34D 최신) `12.909136`
- oos_trade_count(표본외 거래 수): `152` versus stage100_best(100단계 최선) `149`

## Decision(판정)

decision(판정): `continue_oos_net_density_followup_review_in_stage103`

Stage102(102단계)는 전체 목표 완료가 아니다. Effect(효과): 성공이면 Stage103(103단계)에서 후속 검토로 고정하고, 부족하면 다음 좁은 수리로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).

# RUN03A ExtraTrees Training Effect Packet

- run_id(실행 ID): `run03A_extratrees_fwd18_inverse_context_scout_v1`
- stage(단계): `12_model_family_challenge__extratrees_training_effect`
- model family(모델 계열): `sklearn_extratreesclassifier_multiclass`
- selected threshold(선택 임계값): `a_tier_a_rankq0.960_short0.431_long0.398_margin0.120__b_tier_b_rankq0.960_short0.351_long0.394_margin0.080__hold9__slice_mid_second_overlap_200_220__model_extratrees_rank_target_inverse__ctx_di_spread_abs_lte8_adx_lte25`
- boundary(경계): `Python structural scout(파이썬 구조 탐침)` only(전용)

## Result Read(결과 판독)

| view(보기) | rows(행) | signals(신호) | coverage(비율) | validation hit(검증 적중률) | OOS hit(표본외 적중률) |
|---|---:|---:|---:|---:|---:|
| Tier A separate(Tier A 분리) | `1020` | `1` | `0.000980392156862745` | `None` | `None` |
| Tier B separate(Tier B 분리) | `273` | `1` | `0.003663003663003663` | `None` | `0.0` |
| Tier A+B combined(Tier A+B 합산) | `1293` | `2` | `0.0015467904098994587` | `None` | `0.0` |

## Judgment(판정)

`RUN03A(실행 03A)`는 ExtraTrees(엑스트라 트리) 학습 효과를 Python structural scout(파이썬 구조 탐침)로 기록했다. 효과(effect, 효과)는 Stage 11(11단계)의 LightGBM(라이트GBM) 단서와 다른 모델 확률 표면(probability surface, 확률 표면)을 비교할 수 있게 한 것이다.

아직 MT5 runtime_probe(MT5 런타임 탐침), alpha quality(알파 품질), live readiness(실거래 준비), promotion_candidate(승격 후보)는 아니다.

## Artifact Paths(산출물 경로)

- run manifest(실행 목록): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03A_extratrees_fwd18_inverse_context_scout_v1/run_manifest.json`
- kpi record(KPI 기록): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03A_extratrees_fwd18_inverse_context_scout_v1/kpi_record.json`
- summary(요약): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03A_extratrees_fwd18_inverse_context_scout_v1/summary.json`
- result summary(결과 요약): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03A_extratrees_fwd18_inverse_context_scout_v1/reports/result_summary.md`

# RUN03B Standalone ExtraTrees Packet

- run_id(실행 ID): `run03B_et_standalone_fwd12_v1`
- model family(모델 계열): `sklearn_extratreesclassifier_multiclass`
- threshold method(임계값 방식): `standalone_validation_nonflat_confidence_q90`
- nonflat confidence threshold(비평탄 확신 임계값): `0.4516214515113969`
- boundary(경계): `Python structural scout(파이썬 구조 탐침)` only(전용)

## Result Read(결과 판독)

| split(분할) | rows(행) | signals(신호) | coverage(비율) | hit rate(적중률) |
|---|---:|---:|---:|---:|
| train(학습) | `29222` | `2206` | `0.07549106837314352` | `0.9075249320036265` |
| validation(검증) | `9844` | `604` | `0.061357171881349044` | `0.3526490066225166` |
| OOS(표본외) | `7584` | `463` | `0.06104957805907173` | `0.42764578833693306` |

## Judgment(판정)

`inconclusive_standalone_extratrees_training_effect`

효과(effect, 효과): 이번 판정은 ExtraTrees(엑스트라 트리) standalone(단독) 학습 효과에만 붙는다. Stage 10/11(10/11단계) 계승 판정이 아니다.

## Paths(경로)

- manifest(목록): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03B_et_standalone_fwd12_v1/run_manifest.json`
- KPI(핵심 성과 지표): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03B_et_standalone_fwd12_v1/kpi_record.json`
- summary(요약): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03B_et_standalone_fwd12_v1/summary.json`
- predictions(예측): `stages/12_model_family_challenge__extratrees_training_effect/02_runs/run03B_et_standalone_fwd12_v1/predictions/scored.parquet`

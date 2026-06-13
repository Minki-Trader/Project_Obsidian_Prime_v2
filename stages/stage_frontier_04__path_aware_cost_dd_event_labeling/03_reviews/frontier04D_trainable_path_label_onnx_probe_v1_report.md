# Frontier04D Trainable Path Label ONNX Probe(전선04D 학습 가능 경로 라벨 온엑스 탐침)

Updated(갱신): 2026-06-13T19:16:24Z

Status(상태): `oracle_to_model_transfer_collapse_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): locked variant(고정 변형) `f04b_path_h12_t1p20_s0p80_trainp90` 하나만 라벨로 쓰고, LogisticRegression(로지스틱 회귀) 2개 설정과 small RandomForest(작은 랜덤포레스트) 1개 설정을 train/validation/OOS(학습/검증/표본밖) 고정 분할에서 학습했습니다.

Effect(효과): Frontier04B(전선04B)의 oracle proxy(오라클 프록시)가 feature_set_v2(피처 세트 v2)로 얼마나 전달되는지 density/PF/DD retention(밀도/수익 팩터/손실폭 유지율)로 확인했습니다.

## Best Model Read(최상위 모델 판독)

- model(모델): `rf_depth5_leaf80_balanced_argmax`
- partial_transfer_pass(부분 전달 통과): `False`
- validation density/PF/DD(검증 밀도/수익 팩터/손실폭): `25.1475/day` / `0.976889` / `74.7387%`
- OOS density/PF/DD(표본밖 밀도/수익 팩터/손실폭): `26.6794/day` / `0.965065` / `40.1913%`
- validation/OOS density retention(검증/표본밖 밀도 유지율): `3.20028` / `4.50387`
- ONNX parity(온엑스 동등성): `True`

## Required Boundaries(필수 경계)

- model_validation(모델 검증): `exploratory(탐색)`
- runtime_claim_boundary(런타임 주장 경계): `research_only(연구 전용)`
- no WFO/MT5(WFO/MT5 없음): satisfied(충족)
- threshold_policy(임계값 정책): `argmax only, no searched threshold(최대 확률 전용, 탐색 임계값 없음)`

## Artifacts(산출물)

- retention(유지율): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04D_trainable_path_label_onnx_probe_v1/retention.csv`
- model metrics(모델 지표): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04D_trainable_path_label_onnx_probe_v1/model_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04D_trainable_path_label_onnx_probe_v1/onnx_parity.csv`
- label manifest(라벨 목록): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04D_trainable_path_label_onnx_probe_v1/label_manifest.json`

## Next Action(다음 행동)

`frontier04E_oracle_to_model_collapse_closeout_decision_v1`. Action(행동)은 이 탐침 결과를 repair/second probe/closeout(수리/2차 탐침/마감) 결정으로 넘기는 것입니다. Effect(효과)는 모델 전달이 약하면 broad sweep(넓은 반복 탐색)으로 도망가지 않고 stage lifecycle(단계 생명주기)을 정직하게 좁히는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

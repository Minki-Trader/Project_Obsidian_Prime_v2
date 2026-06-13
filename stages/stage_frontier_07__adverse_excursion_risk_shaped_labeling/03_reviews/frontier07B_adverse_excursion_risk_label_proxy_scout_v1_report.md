# Frontier07B Adverse Excursion Risk Label Proxy Scout Report(전선07B 불리한 이동 위험 라벨 프록시 탐색 보고서)

Updated(갱신): 2026-06-13T20:43:32Z

Status(상태): `risk_shaped_label_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): 4 label families(라벨군) x 3 variants(변형)로 adverse excursion risk-shaped labels(불리한 이동 위험 형성 라벨)을 만들고, fixed feature_set_v2(고정 피처 세트 v2)와 small ONNX-exportable models(작은 온엑스 내보내기 가능 모델)로 argmax-only(최대확률 전용) 학습/검증을 실행했습니다.

Effect(효과): Frontier04(전선04)의 event-first path grid(이벤트 우선 경로 격자)와 Frontier06(전선06)의 abstention threshold search(기권 임계값 탐색)를 반복하지 않고, label utility(라벨 효용)가 DD(drawdown, 손실폭)를 직접 낮출 수 있는지 확인했습니다.

## Best Candidate Read(최상위 후보 판독)

- candidate(후보): `f07b_time_to_adverse_penalty_v2_lt1p05_st1p05_lc0p70_sc0p70_q90__v08_lr_plain`
- family(라벨군): `time_to_adverse_penalty`
- strict_scout_clue_pass(엄격 탐색 단서 통과): `False`
- preserved_clue_pass(보존 단서 통과): `True`
- learnability_pass(학습 가능성 통과): `True`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.06855` / `3.10929/day` / `53.129%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `1.70687` / `1.36641/day` / `13.0888%`
- ONNX parity(온엑스 동등성): `True`

## Reference Comparison(참조 비교)

- label_v1 argmax(라벨v1 최대확률): validation/OOS PF(검증/표본밖 수익 팩터) `0.987816` / `1.07904`, DD(손실폭) `58.1003` / `41.6327`
- Frontier04 locked path trainable(전선04 고정 경로 학습 참조): validation/OOS PF(검증/표본밖 수익 팩터) `0.976889` / `0.965065`, DD(손실폭) `74.7387` / `40.1913`
- Frontier06 best selective(전선06 최선 선택 참조): validation/OOS PF(검증/표본밖 수익 팩터) `1.05864` / `1.26664`, DD(손실폭) `30.9057` / `21.1091`

## Result Boundary(결과 경계)

- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `21`
- Tier B/Tier A+B(티어 B/티어 A+B): missing_required(필수 누락)
- runtime boundary(런타임 경계): `research_only_no_mt5(연구 전용, MT5 없음)`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/candidate_summary.csv`
- model metrics(모델 지표): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/candidate_model_metrics.csv`
- reference metrics(참조 지표): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/reference_model_metrics.csv`
- classification metrics(분류 지표): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/classification_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/run_manifest.json`

## Next Action(다음 행동)

`frontier07C_risk_label_repair_or_closeout_decision_v1`. Action(행동)은 결과 경계에 따라 Grok review(그록 검토) 또는 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 DD-only improvement(손실폭만 개선)를 strict scout clue(엄격 탐색 단서)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

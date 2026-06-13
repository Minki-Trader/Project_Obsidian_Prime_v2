# Frontier07C Class Prior Density Bridge Repair Report(전선07C 클래스 사전분포 밀도 브리지 수리 보고서)

Updated(갱신): 2026-06-13T20:49:31Z

Status(상태): `class_prior_density_bridge_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): Frontier07B(전선07B)의 preserved variants(보존 변형) 상위 4개에 directional class-prior weights(방향 클래스 사전분포 가중치) 1.25~2.00을 적용해 argmax-only(최대확률 전용) repair(수리)를 실행했습니다.

Effect(효과): threshold search(임계값 탐색) 없이 sparse plain model(희소 기본 모델)과 overactive balanced model(과활성 균형 모델) 사이의 density bridge(밀도 브리지)를 시험했습니다.

## Best Repair Read(최상위 수리 판독)

- candidate(후보): `f07b_time_to_adverse_penalty_v1_lt0p90_st0p90_lc0p60_sc0p60_q90__v02_rw01`
- strict_scout_clue_pass(엄격 탐색 단서 통과): `False`
- preserved_clue_pass(보존 단서 통과): `True`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.03874` / `5.71038/day` / `58.8505%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `1.17777` / `4.12214/day` / `13.1215%`
- ONNX parity(온엑스 동등성): `True`

## Result Boundary(결과 경계)

- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `16`
- repair scope(수리 범위): `capped repair: top 4 Frontier07B preserved variants x 4 directional weights(상한 있는 수리: 전선07B 보존 변형 4개 x 방향 가중치 4개)`
- runtime boundary(런타임 경계): `research_only_no_mt5(연구 전용, MT5 없음)`

## Artifacts(산출물)

- repair candidate summary(수리 후보 요약): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07C_class_prior_density_bridge_repair_v1/repair_candidate_summary.csv`
- repair model metrics(수리 모델 지표): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07C_class_prior_density_bridge_repair_v1/repair_model_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07C_class_prior_density_bridge_repair_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/02_runs/frontier07C_class_prior_density_bridge_repair_v1/run_manifest.json`

## Next Action(다음 행동)

`frontier07D_stage_closeout_decision_v1`. Action(행동)은 strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 실행 전 검토), 없으면 stage closeout(단계 마감)로 넘기는 것입니다. Effect(효과)는 같은 수리를 반복하지 않고 capped repair(상한 있는 수리) 원칙을 지키는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

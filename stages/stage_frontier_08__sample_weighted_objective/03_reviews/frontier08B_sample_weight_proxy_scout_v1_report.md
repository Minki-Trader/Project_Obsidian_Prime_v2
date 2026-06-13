# Frontier08B Sample Weight Proxy Scout Report(전선08B 표본 가중 프록시 탐색 보고서)

Updated(갱신): 2026-06-13T21:28:24Z

Status(상태): `sample_weight_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): label_v1(라벨 v1)과 Frontier07 risk label reference(전선07 위험 라벨 참조)에 대해 matched unweighted controls(짝지은 무가중 대조군)와 train-only sample weighting(학습 전용 표본 가중)을 같은 rows/splits/models(행/분할/모델)에서 비교했습니다.

Effect(효과): sample weighting(표본 가중)이 density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움)를 동시에 개선하는지, threshold search(임계값 탐색) 없이 확인했습니다.

## Best Read(최상위 판독)

- candidate(후보): `f07b_time_to_adverse_penalty_v1_lt0p90_st0p90_lc0p60_sc0p60_q90__f08b_f07risk_lr_plain_adv_a100`
- weight policy(가중 정책): `adv_a100`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `27`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.00405` / `6.94536` / `58.0016%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `1.19464` / `5.47328` / `15.655%`
- paired axis improvement count(짝 비교 축 개선 수): `5`
- ONNX parity(온엑스 동등성): `True`

## Boundaries(경계)

- weights(가중치)는 train split(학습 분할)에서만 산출했습니다.
- validation/OOS(검증/표본밖)는 평가 전용입니다.
- argmax-only(최대확률 전용)이며 threshold/abstention search(임계값/기권 탐색)는 없습니다.
- Tier B and combined(티어 B와 합산)는 missing_required(필수 누락)로 장부에 기록했습니다.
- WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)가 없으면 실행하지 않습니다.

## Artifacts(산출물)

- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/run_manifest.json`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/final_decision.json`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/candidate_summary.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/model_metrics.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/classification_metrics.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/onnx_parity.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/weight_stats.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/target_distribution.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08B_sample_weight_proxy_scout_v1/skipped.csv`

## Next Action(다음 행동)

`frontier08C_sample_weight_repair_or_closeout_decision_v1`. Action(행동)은 결과에 따라 Grok pre-expensive review(그록 비싼 검증 전 검토) 또는 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 one-axis improvement(한 축 개선)를 completion candidate(완성 후보)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

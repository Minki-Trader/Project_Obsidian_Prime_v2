# Frontier08C Capped Sample Weight Repair Scout Report(전선08C 상한 표본 가중 수리 탐색 보고서)

Updated(갱신): 2026-06-13T21:28:49Z

Status(상태): `sample_weight_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): Frontier08B(전선08B)의 보존 단서(preserved clue, 보존 단서)였던 Frontier07 risk label reference(전선07 위험 라벨 참조)에 대해서만 capped repair(상한 수리)를 실행했습니다.

Effect(효과): 새 family(가족)를 늘리지 않고 alpha 1.50(강도 1.50) 세 번째 변형만 추가해, 수리 효과(repair effect, 수리 효과)가 있는지 확인했습니다.

## Best Read(최상위 판독)

- candidate(후보): `f07b_time_to_adverse_penalty_v1_lt0p90_st0p90_lc0p60_sc0p60_q90__f08c_f07risk_lr_plain_util_a150`
- weight policy(가중 정책): `util_a150`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `4`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.00426` / `7.0765` / `59.5044%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `1.16725` / `5.65649` / `16.0798%`
- paired axis improvement count(짝 비교 축 개선 수): `3`
- ONNX parity(온엑스 동등성): `True`

## Boundaries(경계)

- repair scope(수리 범위): `capped_third_alpha_variants_only(상한 있는 세 번째 강도 변형만)`
- variant cap(변형 상한): `four_families_max_three_variants_each(가족 4개 이하, 각 3변형 이하)`
- threshold/abstention search(임계값/기권 탐색): not used(사용 안 함)
- WFO/MT5(WFO/MT5): strict scout clue(엄격 탐색 단서)가 없으면 실행하지 않습니다.
- Tier B and combined(티어 B와 합산): missing_required(필수 누락)

## Artifacts(산출물)

- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/run_manifest.json`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/final_decision.json`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/candidate_summary.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/model_metrics.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/classification_metrics.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/onnx_parity.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/weight_stats.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/target_distribution.csv`
- `stages/stage_frontier_08__sample_weighted_objective/02_runs/frontier08C_sample_weight_capped_repair_scout_v1/skipped.csv`

## Next Action(다음 행동)

`frontier08D_stage_closeout_sample_weight_objective_v1`. Action(행동)은 strict scout clue(엄격 탐색 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 stage closeout(단계 마감)을 여는 것입니다. Effect(효과)는 약한 보존 단서(preserved clue, 보존 단서)를 completion candidate(완성 후보)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

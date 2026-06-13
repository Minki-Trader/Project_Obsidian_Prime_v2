# Frontier10C Utility Distillation Capped Repair Scout Report(전선10C 효용 증류 상한 수리 탐색 보고서)

Updated(갱신): 2026-06-13T23:09:46Z

Status(상태): `utility_distillation_capped_repair_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): Frontier10C(전선10C)는 Frontier10B(전선10B) utility labels(효용 라벨)를 유지하고, fixed side-class-weight ladder(고정 방향 클래스 가중 사다리)로 plain sparse(일반 희소)와 balanced overtrade(균형 과거래) 사이를 한 번만 탐색했습니다.

Effect(효과): class-prior density bridge(클래스 사전분포 밀도 브리지), threshold search(임계값 탐색), WFO/MT5(WFO/MT5)를 쓰지 않고 ONNX argmax-only(온엑스 최대확률 전용) 모델의 밀도 절벽이 수리되는지 봅니다.

## Best Repair Read(최상위 수리 판독)

- candidate(후보): `f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3__f10c_f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3_lr_c0p50_sw1p60`
- strict scout clue pass(엄격 탐색 단서 통과): `False`
- preserved clue pass(보존 단서 통과): `True`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `14`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `0.840113` / `3.35519` / `59.5315%`
- OOS PF/density/DD(표본밖 수익 팩터/거래 밀도/손실폭): `1.54787` / `1.93893` / `10.9261%`
- Frontier10B best improvement count(전선10B 최상 대비 개선 수): `4`

## Boundaries(경계)

- repair scope(수리 범위): one capped model-objective ladder(상한 있는 모델 목적 사다리 1회)
- no bridge(브리지 없음): post-hoc class-prior/density bridge(사후 클래스 사전분포/밀도 브리지)를 쓰지 않았습니다.
- no threshold search(임계값 탐색 없음): output(출력)은 argmax-only(최대확률 전용)입니다.
- external verification(외부 검증): strict clue(엄격 단서)가 없으면 WFO/MT5(WFO/MT5)는 out_of_scope_by_claim(주장 범위 밖)입니다.

## Artifacts(산출물)

- repair candidate summary(수리 후보 요약): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/repair_candidate_summary.csv`
- repair model metrics(수리 모델 지표): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/repair_candidate_model_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/repair_onnx_parity.csv`
- final decision(최종 판단): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/repair_final_decision.json`
- run manifest(실행 목록): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/run_manifest.json`

## Next Action(다음 행동)

`frontier10D_grok_stage_closeout_review_v1`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로, 없으면 Grok stage closeout review(그록 단계 마감 검토)로 갑니다. Effect(효과): 한 번 허용된 capped repair(상한 수리)를 반복하지 않고, 가설 생명주기(hypothesis lifecycle, 가설 생명주기)를 정직하게 닫을 준비를 합니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

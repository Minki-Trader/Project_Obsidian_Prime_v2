# Frontier11B Subperiod Stability Proxy Scout Report(전선11B 하위기간 안정성 프록시 탐색 보고서)

Updated(갱신): 2026-06-14T00:01:08Z

Status(상태): `subperiod_stability_no_strict_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): Frontier11B(전선11B)는 기존 F10C(전선10C) ONNX/joblib model files(온엑스/joblib 모델 파일) 후보군을 재학습 없이 읽고, validation/OOS(검증/표본밖) month/quarter(월/분기) slice(조각) 안정성을 계산했습니다.

Effect(효과): label/objective/weight/bridge(라벨/목적/가중/브리지) 수리를 반복하지 않고, aggregate-only selector(합계 전용 선택기)와 stability-first selector(안정성 우선 선택기)를 같은 후보 풀(candidate pool, 후보 풀)에서 비교합니다.

## Selector Read(선택기 판독)

- aggregate-only top(합계 전용 최상위): `f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3__f10c_f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3_lr_c0p50_sw1p60`
- stability-first top(안정성 우선 최상위): `f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3__f10c_f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3_lr_c0p50_sw1p60`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `0`
- stability top validation PF/density/DD(안정성 최상위 검증 수익 팩터/밀도/손실폭): `0.840113` / `3.35519` / `59.5315%`
- stability top OOS PF/density/DD(안정성 최상위 표본밖 수익 팩터/밀도/손실폭): `1.54787` / `1.93893` / `10.9261%`
- worst subperiod DD(최악 하위기간 손실폭): `59.5315%`
- negative period fraction mean(음수 기간 비율 평균): `0.230159`
- trade count entropy mean(거래 수 엔트로피 평균): `0.65535`

## Local Verification(로컬 검증)

- source candidate pool(원천 후보군): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/repair_candidate_summary.csv`
- source manifest(원천 실행 목록): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/run_manifest.json`
- no refit(재적합 없음): F11B(전선11B)는 model fit/export(모델 적합/내보내기)를 하지 않았습니다.
- slice definition(조각 정의): America/New_York(뉴욕 시간) month/quarter(월/분기) period(기간), split(분할) 내부에서만 계산.
- control arm(대조군): F10C aggregate row order(F10C 합계 행 순서).

## Artifacts(산출물)

- stability candidate summary(안정성 후보 요약): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/02_runs/frontier11B_subperiod_stability_proxy_scout_v1/stability_candidate_summary.csv`
- subperiod metrics(하위기간 지표): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/02_runs/frontier11B_subperiod_stability_proxy_scout_v1/subperiod_metrics.csv`
- selector comparison(선택기 비교): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/02_runs/frontier11B_subperiod_stability_proxy_scout_v1/selector_comparison.csv`
- model signal identity(모델 신호 정체성): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/02_runs/frontier11B_subperiod_stability_proxy_scout_v1/model_signal_identity.csv`
- final decision(최종 판단): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/02_runs/frontier11B_subperiod_stability_proxy_scout_v1/final_decision.json`
- run manifest(실행 목록): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/02_runs/frontier11B_subperiod_stability_proxy_scout_v1/run_manifest.json`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다. WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)와 Grok pre-expensive review(그록 비싼 검증 전 검토) 전까지 실행하지 않습니다.

## Next Action(다음 행동)

`frontier11C_stability_selector_repair_or_closeout_decision_v1`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 repair/closeout decision(수리/마감 결정)으로 갑니다. Effect(효과): subperiod stability(하위기간 안정성)를 completion candidate(완성 후보)로 과장하지 않고 다음 경계를 고릅니다.

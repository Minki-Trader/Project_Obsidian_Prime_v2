# Frontier10B Utility Distillation Proxy Scout Report(전선10B 효용 증류 프록시 탐색 보고서)

Updated(갱신): 2026-06-13T22:58:19Z

Status(상태): `utility_distillation_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): Frontier10B(전선10B)는 train-only subwindow thresholds(학습 전용 하위구간 임계값)로 utility_consensus/utility_margin/drawdown_veto_distillation(효용 합의/효용 마진/손실폭 거부 증류) 라벨을 만들고, 고정 3-class ONNX(3분류 온엑스) argmax-only(최대확률 전용) 모델로 확인했습니다.

Effect(효과): validation/OOS(검증/표본밖)를 라벨 적합에 쓰지 않고, class-prior bridge(클래스 사전분포 브리지) 없이 네 축(density/PF/DD/smoothness, 밀도/수익 팩터/손실폭/매끄러움)이 같이 좋아지는지 봅니다.

## Best Candidate Read(최상위 후보 판독)

- candidate(후보): `f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3__f10b_f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3_lr_plain`
- strict scout clue pass(엄격 탐색 단서 통과): `False`
- preserved clue pass(보존 단서 통과): `True`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `16`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `0.820909` / `2.30055` / `56.3956%`
- OOS PF/density/DD(표본밖 수익 팩터/거래 밀도/손실폭): `1.31097` / `0.664122` / `7.57853%`

## Local Verification(로컬 검증)

- subwindow containment(하위구간 포함): `4` train-only subwindows(학습 전용 하위구간), lengths(길이) `[7306, 7306, 7305, 7305]`.
- leakage boundary(누수 경계): thresholds/margins/adverse caps(임계값/마진/불리 이동 상한)는 train split(학습 분할)에서만 fit(적합)했고 validation/OOS(검증/표본밖)는 evaluation-only(평가 전용)입니다.
- no-bridge control(무브리지 대조): class-prior density bridge(클래스 사전분포 밀도 브리지)와 threshold search(임계값 탐색)는 사용하지 않았습니다.
- references(참조): label_v1(라벨 v1), Frontier07 risk label(전선07 위험 라벨)은 재계산 대조군이고 Frontier08/09(전선08/09)는 report reference(보고서 참조)입니다.

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/candidate_summary.csv`
- candidate metrics(후보 지표): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/candidate_model_metrics.csv`
- reference metrics(참조 지표): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/reference_model_metrics.csv`
- target diagnostics(목표 진단): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/target_diagnostics.json`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/onnx_parity.csv`
- final decision(최종 판단): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/final_decision.json`
- run manifest(실행 목록): `stages/stage_frontier_10__split_consistent_utility_distillation/02_runs/frontier10B_utility_distillation_proxy_scout_v1/run_manifest.json`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다. WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)와 Grok pre-expensive review(그록 비싼 검증 전 검토) 전까지 실행하지 않습니다.

## Next Action(다음 행동)

`frontier10C_utility_distillation_repair_or_closeout_decision_v1`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 repair/closeout decision(수리/마감 결정)으로 갑니다. Effect(효과): scout clue(탐색 단서)를 completion candidate(완성 후보)로 과장하지 않고 다음 검증 경계를 고릅니다.

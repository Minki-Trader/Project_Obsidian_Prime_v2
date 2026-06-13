# Frontier06B Selective Probability Abstention Signal Scout Report(전선06B 선택적 확률 기권 신호 탐색 보고서)

Updated(갱신): 2026-06-13T20:01:51Z

Status(상태): `selective_abstention_no_strict_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): same model probabilities(같은 모델 확률)에 train-only calibrated abstention rules(학습 전용 보정 기권 규칙)을 적용하고 argmax baseline(최대 확률 기준)과 비교했습니다.

Effect(효과): label/feature/model(라벨/피처/모델)을 바꾸지 않고 output-to-trade signal contract(출력-거래 신호 계약)만 바꿔 overtrading/DD failure(과다거래/손실폭 실패)를 줄일 수 있는지 확인했습니다.

## Best Rule Read(최상위 규칙 판독)

- rule(규칙): `rf_depth5_leaf80_balanced_argmax__directional_margin__flat1p01__margin0p00__d4p0`
- model(모델): `rf_depth5_leaf80_balanced_argmax`
- score kind(점수 종류): `directional_margin`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.05864` / `6.38251/day` / `30.9057%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `1.26664` / `5.30534/day` / `21.1091%`
- strict scout clue pass(엄격 탐색 단서 통과): `False`
- scout clue rows(탐색 단서 행): `0`

## Boundaries(경계)

- threshold policy(임계값 정책): `train-only calibrated score thresholds, no validation/OOS fitting(학습 전용 점수 임계값, 검증/표본밖 적합 없음)`
- probability meaning(확률 의미): `probabilities are ranking scores, not calibrated probability truth(확률은 순위 점수이지 보정 확률 진실 아님)`
- runtime boundary(런타임 경계): `research_only_no_mt5(연구 전용, MT5 없음)`
- Tier B/Tier A+B(티어 B/티어 A+B): missing_required(필수 누락) rows are recorded in ledgers(장부에 기록됨).

## Artifacts(산출물)

- rule comparison(규칙 비교): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/signal_rule_comparison.csv`
- rule metrics(규칙 지표): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/signal_rule_metrics.csv`
- argmax baseline(최대 확률 기준): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/argmax_baseline_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/run_manifest.json`

## Next Action(다음 행동)

`frontier06C_signal_contract_closeout_decision_v1`. Action(행동)은 scout result(탐색 결과)를 Grok review(그록 검토) 또는 closeout decision(마감 결정)으로 넘기는 것입니다. Effect(효과)는 threshold micro-search(임계값 미세탐색)로 새지 않고 stage lifecycle(단계 생명주기)을 유지하는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

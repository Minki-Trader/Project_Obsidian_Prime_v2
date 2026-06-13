# Frontier09B Drawdown Clean Path Label Proxy Scout Report(전선09B 손실폭 깨끗한 경로 라벨 프록시 탐색 보고서)

Updated(갱신): 2026-06-13T22:03:06Z

Status(상태): `drawdown_clean_path_label_preserved_clue_no_authority`

Judgment(판정): `preserved_clue(보존 단서)`

## Action And Effect(행동과 효과)

Action(행동): train-only thresholds/scales(학습 전용 임계값/스케일)로 drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)을 만들고, fixed feature_set_v2(고정 피처 세트 v2)와 ONNX-exportable sklearn models(ONNX 내보내기 가능한 sklearn 모델)로 argmax-only(최대 확률 전용) 검증을 실행했습니다.

Effect(효과): Frontier07(전선07)의 위험 라벨을 상속하지 않고 reference(참조)로만 두면서, 목표 표현(target representation, 목표 표현) 자체가 density/PF/DD/smoothness(거래 밀도/수익 팩터/손실폭/매끄러움)를 동시에 개선하는지 확인했습니다.

## Best Candidate Read(최상위 후보 판독)

- candidate(후보): `f09b_payoff_adverse_ratio_v1_lt0p80_st0p80_lc0p70_sc0p70__f09b_f09b_payoff_adverse_ratio_v1_lt0p80_st0p80_lc0p70_sc0p70_lr_plain`
- family(라벨군): `payoff_adverse_ratio`
- strict scout clue pass(엄격 탐색 단서 통과): `False`
- preserved clue pass(보존 단서 통과): `True`
- paired axis improvement count(짝지은 축 개선 수): `10`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `1.00137` / `4.49727` / `64.1321%`
- OOS PF/density/DD(OOS 표본밖 수익 팩터/거래 밀도/손실폭): `1.11125` / `2.76336` / `13.3936%`
- ONNX parity(ONNX 동등성): `True`

## Boundaries(경계)

- validation/OOS(검증/OOS)는 evaluation-only(평가 전용)입니다.
- Tier B and combined(티어 B와 합산)는 missing_required(필수 누락)로 기록했습니다.
- WFO/MT5(WFO/MT5)는 아직 실행하지 않았습니다.
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/candidate_summary.csv`
- model metrics(모델 지표): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/candidate_model_metrics.csv`
- reference metrics(참조 지표): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/reference_model_metrics.csv`
- classification metrics(분류 지표): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/classification_metrics.csv`
- ONNX parity(ONNX 동등성): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/run_manifest.json`

## Next Action(다음 행동)

`frontier09C_drawdown_clean_path_repair_or_closeout_decision_v1`. Action(행동)은 결과 경계에 맞게 Grok review(그록 검토) 또는 repair/closeout decision(수리/마감 결정)으로 넘기는 것입니다. Effect(효과)는 한 축 개선을 completion candidate(완성 후보)로 과장하지 않고 네 축 동시 개선만 앞으로 보내는 것입니다.

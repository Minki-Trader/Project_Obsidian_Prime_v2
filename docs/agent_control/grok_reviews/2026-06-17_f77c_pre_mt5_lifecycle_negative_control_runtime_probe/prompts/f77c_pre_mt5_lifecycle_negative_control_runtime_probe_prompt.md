# F77C Pre-MT5 Grok Review Prompt(F77C 사전 MT5 그록 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `stage_frontier_77__runtime_lifecycle_label_density_rebuild`
- current run(현재 실행): `frontier77C_pre_mt5_grok_lifecycle_negative_control_runtime_probe_v1`
- parent run(부모 실행): `frontier77B_runtime_lifecycle_label_density_proxy_scout_v1`
- proposed next run(제안 다음 실행): `frontier77D_mt5_lifecycle_negative_control_runtime_probe_v1`
- claim boundary(주장 경계): `pre_mt5_review_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Hypothesis(가설)

F77 asks whether runtime lifecycle-native labels(런타임 생명주기 기본 라벨) can reduce the proxy/runtime gap(프록시/런타임 간극) by learning entry-to-exit path outcomes(진입-청산 경로 결과), first-touch TP/SL(최초접촉 익절/손절), hold duration(보유 시간), and single-position occupancy(단일 포지션 점유).

## F77B Proxy Evidence(F77B 프록시 근거)

- candidate rows(후보 행): `10368`
- scout clue count(탐색 단서 수): `364`
- meaningful signal count(의미 신호 수): `0`
- final-like reference count(최종 유사 참조 수): `0`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `6559`

Best proxy candidate(최선 프록시 후보):
- candidate id(후보 ID): `f77b_08051`
- axes(축): `short_h12_tp18_sl12_uq70/price_action_core/hist_gbm_d4_l2/all/trend_aligned/q0.93`
- validation KPI(검증 핵심 성과 지표): net/PF/DD/tpd/trades/win/expectancy/recovery(순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): 272.40000000000003/1.7115987460815043/0.5279999999999927/2.2666666666666666/68/0.5735294117647058/4.005882352941177/5.159090909090981
- OOS KPI(표본외 핵심 성과 지표): net/PF/DD/tpd/trades/win/expectancy/recovery(순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): 127.2/1.8030303030303034/0.6239999999999963/2.230769230769231/29/0.5862068965517241/4.386206896551724/2.0384615384615503
- compression(압축): raw signal -> lifecycle trade validation/OOS(원시 신호 -> 생명주기 거래 검증/표본외) `100->68/40->29`
- weakness(약점): it is scout clue(탐색 단서) only because OOS trade count(표본외 거래 수) is below meaningful gate(의미 신호 게이트).

Top ranked rows(상위 행):
1. f77b_08051: short_h12_tp18_sl12_uq70/price_action_core/hist_gbm_d4_l2/all/trend_aligned/q0.93 | val 272.40000000000003/1.7115987460815043/0.5279999999999927/2.2666666666666666/68 | oos 127.2/1.8030303030303034/0.6239999999999963/2.230769230769231/29
2. f77b_08059: short_h12_tp18_sl12_uq70/price_action_core/hist_gbm_d4_l2/cash_mid/trend_aligned/q0.93 | val 282.00000000000006/1.7912457912457909/0.3960000000000036/2.2413793103448274/65 | oos 110.40000000000002/1.6969696969696972/0.6239999999999963/2.1538461538461537/28
3. f77b_07979: short_h12_tp18_sl12_uq70/price_action_core/extra_trees_d7_l80/cash_mid/trend_aligned/q0.8 | val 227.70000000000016/1.2574626865671639/1.4789999999999963/4.1875/134 | oos 61.20000000000002/1.272727272727273/0.49199999999998906/3.4/34
4. f77b_07971: short_h12_tp18_sl12_uq70/price_action_core/extra_trees_d7_l80/all/trend_aligned/q0.8 | val 218.10000000000005/1.2394598155467715/1.6110000000000038/4.029411764705882/137 | oos 61.20000000000002/1.272727272727273/0.49199999999998906/3.4/34
5. f77b_09739: short_h18_tp26_sl16_uq70/price_action_core/extra_trees_d7_l80/cash_mid/trend_aligned/q0.93 | val 304.0500000000001/1.5164331210191078/1.6439999999999966/2.730769230769231/71 | oos 135.20000000000002/1.982558139534884/0.6120000000000072/2.111111111111111/19
6. f77b_07147: short_h12_tp18_sl12_uq60/price_action_core/extra_trees_d7_l80/cash_mid/trend_aligned/q0.93 | val 244.50000000000006/1.3494854202401365/0.8429999999999928/2.619047619047619/110 | oos 64.80000000000001/1.2727272727272732/0.8760000000000037/2.4/36

## Local Export Check(로컬 내보내기 확인)

Codex checked skl2onnx(사이킷런-온엑스) export feasibility with an in-memory smoke test(메모리 내 연기 테스트):

```json
{
  "hist_gbm_d4_l2": {
    "export_status": "export_failed",
    "error_type": "ValueError",
    "error_excerpt": "Unable to create node 'TreeEnsembleClassifier' with name='TreeEnsembleClassifier' and attributes={'base_values': array([0.], dtype=float32),\n 'class_ids': [0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,\n               0,"
  },
  "extra_trees_d7_l80": {
    "export_status": "export_ok",
    "notes": "in_memory_skl2onnx_smoke_passed"
  },
  "numpy_version": "2.3.4"
}
```

Result(결과): best HistGradientBoosting(히스토그램 그래디언트 부스팅) target is not exportable in this environment(현재 환경에서 내보내기 실패). Codex proposes the first ranked exportable ExtraTrees(엑스트라트리) target instead:

- target candidate(대상 후보): `f77b_07979`
- axes(축): `short_h12_tp18_sl12_uq70/price_action_core/extra_trees_d7_l80/cash_mid/trend_aligned/q0.8`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `227.70000000000016/1.2574626865671639/1.4789999999999963/4.1875/134`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `61.20000000000002/1.272727272727273/0.49199999999998906/3.4/34`

## Integrity And Validation Boundary(무결성과 검증 경계)

- data integrity judgment(데이터 무결성 판정): `usable_with_boundary`
- time axis(시간축): `feature timestamp(피처 시간표시)은 closed-bar key(닫힌 봉 키)로 다루고, raw open_ts == feature timestamp를 next-bar entry open(다음 봉 시가 진입)으로 사용한다.`
- feature/label boundary(피처/라벨 경계): `features use current closed bar; lifecycle labels use next bar open and future high/low/close path only after entry.`
- model validation judgment(모델 검증 판정): `exploratory_proxy_scout`
- calibration risk(보정 위험): `classifier outputs are selection ranks; no probability calibration claim.`
- overfit risk(과적합 위험): `multiple-testing across label/feature/model/session/risk arms; F77B remains exploratory until MT5 probe.`

## Proposed MT5 Runtime Probe(제안 MT5 런타임 탐침)

Codex proposal(Codex 제안):

1. Re-train(재학습) the selected ExtraTrees(엑스트라트리) target on train split(학습 분할) using the same lifecycle label(생명주기 라벨), feature set(피처 묶음), session filter(세션 필터), risk filter(위험 필터), and train quantile threshold(학습 분위수 임계값).
2. Materialize ONNX(온엑스 물질화) as short-only three-column output(숏 전용 3열 출력): `[p_short=P(short), p_flat=P(non-short), p_long=0]`.
3. Use selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) so MT5 signal count(신호 수) is forced to match proxy selected timestamps(프록시 선택 시각) after ONNX thresholding(온엑스 임계값 적용).
4. Runtime decision(런타임 결정): `short_threshold=proxy_threshold-epsilon`, `long_threshold=1.1`, `min_margin=-1.0`, decision mode(결정 모드) `threshold_margin`.
5. Trade shape(거래 형태): short-only(숏 전용), max hold 12 M5 bars(최대 보유 12개 5분봉), fixed TP/SL(고정 익절/손절) 18/12 points(포인트) by enabling ATR SL/TP(ATR 손절/익절) and setting min=max clamps(최소=최대 고정) to TP 18 and SL 12.
6. Execute validation and OOS Strategy Tester(검증 및 표본외 전략 테스터) attempts for US100 M5.

## Focus Question(집중 질문)

Should Codex proceed with this F77D negative-control MT5 Runtime Probe(F77D 부정 대조 MT5 런타임 탐침) as proposed, or must it adjust the materialization before execution?

Please classify advice(조언 분류) into exactly one:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Also list:
1. Top proxy/runtime gap risks(최상위 프록시/런타임 간극 위험)
2. Required local verification before execution(실행 전 필수 로컬 검증)
3. Any forbidden claim risk(금지 주장 위험)
4. The smallest useful MT5 probe scope(가장 작은 유용한 MT5 탐침 범위)

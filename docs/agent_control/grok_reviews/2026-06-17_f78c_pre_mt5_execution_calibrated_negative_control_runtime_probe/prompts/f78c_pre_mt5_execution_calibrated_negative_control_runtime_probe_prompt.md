# F78C Pre-MT5 Grok Review Prompt(F78C 사전 MT5 그록 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild`
- current run(현재 실행): `frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1`
- parent run(부모 실행): `frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_v1`
- proposed next run(제안 다음 실행): `frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_v1`
- claim boundary(주장 경계): `pre_mt5_review_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## F78 Hypothesis(F78 가설)

Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), calendar-day density(달력일 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), and risk penalty(위험 벌점)를 proxy stage(프록시 단계)부터 내장하면 F77 money/density gap(금액/밀도 간극)을 줄일 수 있는지 본다.

## F78B Proxy Evidence(F78B 프록시 근거)

- candidate rows(후보 행): `2592`
- scout clue count(탐색 단서 수): `1`
- meaningful signal count(의미 신호 수): `0`
- final-like reference count(완성 유사 참조 수): `0`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `2134`
- contract P/L scale(계약 손익 배율): `0.08870965974736267` from `F77 observed gross-profit runtime/proxy scale mean(관찰 총이익 런타임/프록시 배율 평균): (0.09352576207175615 + 0.08389355742296918) / 2`
- entry rule(진입 규칙): `next raw bar open after feature timestamp(피처 시각 다음 원천 봉 시가)`
- density rule(밀도 규칙): `calendar_trades_day = trade_count / split calendar days(달력일)`

Best proxy candidate(최선 프록시 후보):
- candidate id(후보 ID): `f78b_02234`
- axes(축): `short_h18_tp26_sl16_net_utility_q57/contract_core/logistic_l2_balanced/all/none/cd6/q0.72`
- validation KPI(검증 핵심 성과 지표): net/PF/DD/calendar_tpd/active_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/활성일 거래/거래): 42.453781865295134/1.1535921177206854/0.21303624788330125/1.2140221402214022/2.5114503816793894/329
- OOS KPI(표본외 핵심 성과 지표): net/PF/DD/calendar_tpd/active_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/활성일 거래/거래): 54.58482783574718/1.2804966996097884/0.22925237368512172/1.2525773195876289/2.4545454545454546/243
- weakness(약점): scout clue(탐색 단서) only, not meaningful signal(의미 신호 아님), because PF(수익 팩터) and calendar density(달력 밀도) remain below final target(최종 목표).

Top rows(상위 행):
1. f78b_02234: short_h18_tp26_sl16_net_utility_q57/contract_core/logistic_l2_balanced/all/none/cd6 | val 42.453781865295134/1.1535921177206854/0.21303624788330125/1.2140221402214022/329 | oos 54.58482783574718/1.2804966996097884/0.22925237368512172/1.2525773195876289/243
2. f78b_01776: short_h12_tp18_sl12_net_utility_q57/full58/extra_trees_d8_l60/cash_open/mean_revert/cd6 | val 1.8096770588461986/2.5454545454545454/0.011709675086658536/0.01107011070110701/3 | oos 1.5435480796041103/999.0/0.0/0.005154639175257732/1
3. f78b_01847: short_h12_tp18_sl12_net_utility_q57/contract_core/extra_trees_d8_l60/cash_open/mean_revert/cd0 | val 5.4290311765385955/2.545454545454546/0.011709675086658536/0.033210332103321034/9 | oos 1.5435480796041103/999.0/0.0/0.005154639175257732/1
4. f78b_01810: short_h12_tp18_sl12_net_utility_q57/contract_core/logistic_l2_balanced/cash_open/trend_aligned/cd6 | val 2.129031833936704/1.9090909090909094/0.02341935017331707/0.01845018450184502/5 | oos 1.9161286505430335/2.714285714285714/0.01117741712818315/0.015463917525773196/3
5. f78b_02257: short_h18_tp26_sl16_net_utility_q57/contract_core/logistic_l2_balanced/cash_open/none/cd0 | val 16.890319215897847/1.9224806201550388/0.10680643033583694/0.1033210332103321/28 | oos 5.890321407224881/1.7885985748218525/0.030516122953104057/0.05670103092783505/11
6. f78b_02009: short_h12_tp18_sl12_density_quota_utility_q52/full58/extra_trees_d8_l60/cash_open/mean_revert/cd0 | val 2.4483866090272093/1.6969696969696972/0.02341935017329888/0.025830258302583026/7 | oos 3.0870961592082207/999.0/0.0/0.010309278350515464/2

## Local Export Check(로컬 내보내기 확인)

```json
{
  "logistic_l2_balanced": {
    "export_status": "export_ok",
    "notes": "in_memory_skl2onnx_smoke_passed"
  },
  "extra_trees_d8_l60": {
    "export_status": "export_ok",
    "notes": "in_memory_skl2onnx_smoke_passed"
  }
}
```

Selected MT5 materialization target(선택된 MT5 물질화 대상):
- target candidate(대상 후보): `f78b_02234`
- selection reason(선택 이유): `best_proxy_candidate_exportable(최선 프록시 후보 내보내기 가능)`
- axes(축): `short_h18_tp26_sl16_net_utility_q57/contract_core/logistic_l2_balanced/all/none/cd6/q0.72`
- validation KPI(검증 핵심 성과 지표): net/PF/DD/calendar_tpd/active_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/활성일 거래/거래): 42.453781865295134/1.1535921177206854/0.21303624788330125/1.2140221402214022/2.5114503816793894/329
- OOS KPI(표본외 핵심 성과 지표): net/PF/DD/calendar_tpd/active_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/활성일 거래/거래): 54.58482783574718/1.2804966996097884/0.22925237368512172/1.2525773195876289/2.4545454545454546/243

## Integrity And Validation Boundary(무결성과 검증 경계)

- data integrity judgment(데이터 무결성 판정): `usable_with_boundary(경계 있는 사용 가능)`
- time axis(시간축): `Feature timestamp(피처 시각)은 closed-bar key(닫힌 봉 키)로 두고, entry(진입)는 next raw bar open(다음 원천 봉 시가)로 둔다.`
- feature/label boundary(피처/라벨 경계): `features(피처)는 current row(현재 행)만 쓰고, label/target(라벨/목표)은 next-bar entry 이후 future OHLC path(미래 OHLC 경로)만 쓴다.`
- model validation judgment(모델 검증 판정): `exploratory_proxy_scout(탐색 프록시)`
- calibration risk(보정 위험): `CONTRACT_PNL_SCALE is runtime-observed proxy calibration(런타임 관찰 프록시 보정) from F77 gross profit scale, not broker authority(브로커 권위 아님).`
- overfit risk(과적합 위험): `large axis sweep(큰 축 탐색) across labels/features/models/sessions/risk/cooldown; F78B remains proxy scout(프록시 탐색).`

## Proposed MT5 Runtime Probe(제안 MT5 런타임 탐침)

Codex proposal(Codex 제안):

1. Re-train(재학습) the selected model(선택 모델) on train split(훈련 분할) using the same contract utility label(계약 효용 라벨), feature set(피처 묶음), session filter(세션 필터), risk filter(위험 필터), cooldown(쿨다운), and train quantile threshold(훈련 분위수 임계값).
2. Export ONNX(ONNX 내보내기) with a short-only three-column schema(숏 전용 3열 스키마): `[p_short=P(short), p_flat=P(non-short), p_long=0]`.
3. Use selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) so MT5 signal count(신호 수) can be compared with proxy selected timestamps(프록시 선택 시각).
4. Use fixed TP/SL broker points(고정 익절/손절 브로커 포인트) from target: TP `2600.0`, SL `1600.0`, point scale(포인트 배율) 100 inherited only as preserved mechanic(보존 메커니즘).
5. Execute validation and OOS Strategy Tester(검증/표본외 전략 테스터) attempts for US100 M5.

## Focus Question(집중 질문)

Should Codex proceed with this F78D negative-control MT5 Runtime Probe(F78D 부정 대조 MT5 런타임 탐침) as proposed, or must it adjust materialization before execution?

Classify advice(조언 분류) into exactly one:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Also list top proxy/runtime gap risks(프록시/런타임 간극 위험), required local verification(필수 로컬 검증), forbidden claim risk(금지 주장 위험), and smallest useful MT5 probe scope(가장 작은 유용 MT5 탐침 범위).

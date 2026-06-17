# F76C Pre-MT5 Grok Review Prompt(F76C MT5 전 그록 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics`
- current run(현재 실행): `frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1`
- parent run(부모 실행): `frontier76B_axis_ablation_proxy_scout_v1`
- proposed next run(제안 다음 실행): `frontier76D_mt5_axis_ablation_runtime_probe_v1`
- claim boundary(주장 경계): `pre_mt5_review_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Hypothesis(가설)

F76 tests whether broad feature/label/model/trade/risk/session ablation(넓은 피처/라벨/모델/거래/위험/세션 제거·교체)이 F71-F75의 parity without economics(동등성은 있으나 경제성 없음) 병목을 source axis(원천 축) 단위로 식별할 수 있는지 본다.

## Proxy Evidence(프록시 근거)

- candidate rows(후보 행): `7680`
- fit completed(적합 완료): `80/80`
- scout clue count(탐색 단서 수): `2091`
- meaningful signal count(의미 신호 수): `10`
- dual positive count(양분할 양수 수): `1105`

Best candidate(최선 후보):
- candidate id(후보 ID): `f76b_06637`
- feature_set(피처 묶음): `mega_cap_removed`, feature_count(피처 수): `48`
- target(목표): `long_fwd12_q60`, side(방향): `long`, target threshold(목표 임계값): `0.0009910748340189455`
- model(모델): `extra_trees_d7_l60`
- probability threshold(확률 임계값): quantile `0.8`, threshold `0.5144632153473251`
- session(세션): `cash_open`
- risk_filter(위험 필터): `trend_aligned`
- cooldown bars(쿨다운 봉): `0`

Validation KPI(검증 핵심 성과 지표):
- net/PF/DD/trades_day/trades/win/expectancy/recovery(순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): `1760.3101806640625/1.594854315978897/6.4446875/1.0601092896174864/194/0.654639175257732/9.073763847351074/2.731412780936333`

OOS KPI(표본외 핵심 성과 지표):
- net/PF/DD/trades_day/trades/win/expectancy/recovery(순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): `1471.7918701171875/1.6893374882536825/7.8916796875/1.1755725190839694/154/0.6168831168831169/9.557089805603027/1.8649919008350369`

Axis summary(축 요약):
- feature_set=full58: candidates=1152, scout=317, meaningful=3, best=f76b_00429, val_pf/dd/tpd=1.5616402144550254/6.4446777343749995/1.0601092896174864, oos_pf/dd/tpd=1.6184422464012251/7.8916796875/1.2290076335877862
- feature_set=mega_cap_removed: candidates=1152, scout=331, meaningful=3, best=f76b_06637, val_pf/dd/tpd=1.594854315978897/6.4446875/1.0601092896174864, oos_pf/dd/tpd=1.6893374882536825/7.8916796875/1.1755725190839694
- feature_set=price_action_core: candidates=1536, scout=404, meaningful=0, best=f76b_02161, val_pf/dd/tpd=1.0173262881710083/34.5966015625/7.644808743169399, oos_pf/dd/tpd=1.1008292572270455/22.05650390625/12.129770992366412
- feature_set=session_macro_removed: candidates=1152, scout=324, meaningful=0, best=f76b_05379, val_pf/dd/tpd=1.386049403969026/5.9012695312500005/0.9508196721311475, oos_pf/dd/tpd=1.6331558789445233/5.417109375/1.6412213740458015
- feature_set=trend_momentum: candidates=1152, scout=341, meaningful=4, best=f76b_02701, val_pf/dd/tpd=1.4620327630473946/6.4446777343749995/1.1147540983606556, oos_pf/dd/tpd=1.3853427305800647/7.41447265625/1.282442748091603
- feature_set=volatility_compression: candidates=1536, scout=374, meaningful=0, best=f76b_04237, val_pf/dd/tpd=1.8316093291100914/6.4446875/0.6721311475409836, oos_pf/dd/tpd=1.7228170798010993/7.891689453125/0.8396946564885496
- target=long_fwd12_q60: candidates=1920, scout=597, meaningful=5, best=f76b_06637, val_pf/dd/tpd=1.594854315978897/6.4446875/1.0601092896174864, oos_pf/dd/tpd=1.6893374882536825/7.8916796875/1.1755725190839694
- target=long_fwd12_q70: candidates=1920, scout=584, meaningful=5, best=f76b_00429, val_pf/dd/tpd=1.5616402144550254/6.4446777343749995/1.0601092896174864, oos_pf/dd/tpd=1.6184422464012251/7.8916796875/1.2290076335877862
- target=short_fwd12_q30: candidates=1920, scout=440, meaningful=0, best=f76b_02582, val_pf/dd/tpd=1.2101766342908595/3.6571191406250003/0.5300546448087432, oos_pf/dd/tpd=1.2192707890033194/3.107705078125/0.816793893129771
- target=short_fwd12_q40: candidates=1920, scout=470, meaningful=0, best=f76b_02161, val_pf/dd/tpd=1.0173262881710083/34.5966015625/7.644808743169399, oos_pf/dd/tpd=1.1008292572270455/22.05650390625/12.129770992366412
- model=extra_trees_d7_l60: candidates=2304, scout=694, meaningful=7, best=f76b_06637, val_pf/dd/tpd=1.594854315978897/6.4446875/1.0601092896174864, oos_pf/dd/tpd=1.6893374882536825/7.8916796875/1.1755725190839694
- model=hist_gbm_d4_l2: candidates=2304, scout=517, meaningful=0, best=f76b_02884, val_pf/dd/tpd=1.405048227341699/3.3083984375/0.5027322404371585, oos_pf/dd/tpd=1.3775051647723175/2.6795117187499997/0.7557251908396947
- model=logistic_l2_balanced: candidates=2304, scout=694, meaningful=3, best=f76b_02701, val_pf/dd/tpd=1.4620327630473946/6.4446777343749995/1.1147540983606556, oos_pf/dd/tpd=1.3853427305800647/7.41447265625/1.282442748091603
- model=small_mlp_16: candidates=768, scout=186, meaningful=0, best=f76b_01444, val_pf/dd/tpd=1.0475571438234772/4.869453125/1.2295081967213115, oos_pf/dd/tpd=1.0825782572093028/5.1748828125/1.5267175572519085
- session=all: candidates=1920, scout=969, meaningful=0, best=f76b_02723, val_pf/dd/tpd=1.4762075102089984/5.210244140625/1.2622950819672132, oos_pf/dd/tpd=1.2980789191854907/5.69400390625/2.2061068702290076
- session=cash_late: candidates=1920, scout=0, meaningful=0, best=f76b_00025, val_pf/dd/tpd=0.0/0.0/0.0, oos_pf/dd/tpd=0.0/0.0/0.0
- session=cash_mid: candidates=1920, scout=791, meaningful=0, best=f76b_05395, val_pf/dd/tpd=1.395618757692581/5.857470703125/0.8360655737704918, oos_pf/dd/tpd=1.677605126217049/5.417109375/1.4045801526717556
- session=cash_open: candidates=1920, scout=331, meaningful=10, best=f76b_06637, val_pf/dd/tpd=1.594854315978897/6.4446875/1.0601092896174864, oos_pf/dd/tpd=1.6893374882536825/7.8916796875/1.1755725190839694
- risk_filter=compression: candidates=1920, scout=261, meaningful=0, best=f76b_02723, val_pf/dd/tpd=1.4762075102089984/5.210244140625/1.2622950819672132, oos_pf/dd/tpd=1.2980789191854907/5.69400390625/2.2061068702290076
- risk_filter=mean_revert: candidates=1920, scout=171, meaningful=0, best=f76b_03016, val_pf/dd/tpd=1.0348657672165875/7.588701171874999/0.8360655737704918, oos_pf/dd/tpd=1.0519488637209233/9.548330078125/0.9694656488549618
- risk_filter=none: candidates=1920, scout=797, meaningful=1, best=f76b_02793, val_pf/dd/tpd=1.8063667815313338/8.7662890625/1.4043715846994536, oos_pf/dd/tpd=1.3256864685278733/9.550693359375/1.4732824427480915
- risk_filter=trend_aligned: candidates=1920, scout=862, meaningful=9, best=f76b_06637, val_pf/dd/tpd=1.594854315978897/6.4446875/1.0601092896174864, oos_pf/dd/tpd=1.6893374882536825/7.8916796875/1.1755725190839694

## Proposed MT5 Runtime Probe(제안 MT5 런타임 탐침)

Codex proposal(Codex 제안):
1. Re-train(재학습) the same ExtraTrees(엑스트라트리) surface on train split(학습 분할): `mega_cap_removed` 48 features, binary target(이진 목표) `future_log_return_12 > train_q60`.
2. Materialize ONNX(ONNX 물질화) as long-only three-column output(롱 전용 3열 출력): `[p_short=0, p_flat=P(non-long), p_long=P(long)]`.
3. Use MT5 RuntimeProbeEA(MT5 런타임 탐침 EA) with `threshold_margin` decision mode(임계값 마진 판단): `long_threshold=proxy_prob_threshold - epsilon`, `short_threshold=1.1`, `min_margin=-1.0`.
4. Encode session/risk/probability selection(세션/위험/확률 선택) with selected-entry runtime veto tape(선택 진입 런타임 거부 테이프), so runtime signal count should match proxy selected timestamps.
5. Trade shape(거래 형태): long-only(롱 전용), max hold 12 M5 bars(최대 보유 12개 5분봉), no ATR SL/TP initially(초기 ATR 손절/익절 없음) to mirror fwd12 close proxy(12봉 뒤 종가 프록시).
6. Run validation and OOS Strategy Tester(검증/표본외 전략 테스터) attempts for US100 M5.

## Focus Question(집중 질문)

Should Codex proceed with this narrow F76D MT5 Runtime Probe(F76D 좁은 MT5 런타임 탐침) as proposed, or must it adjust the materialization before execution?

Please classify advice(조언 분류) into:
- accepted(수용): safe to proceed as proposed
- accepted_with_conditions(조건부 수용): proceed only with named local checks
- needs_local_verification(로컬 검증 필요): evidence is insufficient in this snapshot
- rejected(거절): do not execute because the proposed mapping is logically invalid

Also list:
1. Top proxy/runtime gap risks(최상위 프록시/런타임 간극 위험)
2. Required local verification before execution(실행 전 필수 로컬 검증)
3. Any forbidden claim risk(금지 주장 위험)
4. The smallest useful MT5 probe scope(가장 작은 유용한 MT5 탐침 범위)

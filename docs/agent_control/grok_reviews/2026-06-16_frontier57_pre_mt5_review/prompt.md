# Frontier57 Pre-MT5 Review(전선57 MT5 전 검토)

## Codex Current Truth(코덱스 현재 진실)

- Stage(단계): `stage_frontier_57__short_pf_edge_after_adverse_excursion_memory`
- Candidate(후보): `f57b_fast_exit_execution_extratrees_d6_l80_short_h4_pnl50_q90`
- Hypothesis(가설): after F56 adverse-excursion negative memory(F56 불리 이동 부정 기억 이후), train-only fast-exit positive execution label(학습 전용 빠른 청산 양수 실행 라벨)이 MT5 runtime(런타임)에서 PF source(수익 팩터 원천)로 전이되는지 본다.
- Runtime policy(런타임 정책): short-only(숏 전용), direct threshold(직접 임계값), no sparse admission(희소 진입 허용 없음), no RuntimeVetoTape(런타임 차단 테이프 없음), max hold 6 bars(최대 보유 6봉).
- Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 말하지 않는다.

## Bounded Evidence(제한 근거)

- Label(라벨): hold_limit(보유 한계) `4`, pnl_q(손익 분위수) `0.50`, pnl_cut(손익 절단값) `-0.00032635909583289676`, event_positive_rate_train(학습 양성률) `0.1077612757511464`.
- Threshold(임계값): score_q(점수 분위수) `0.90`, score_threshold(점수 임계값) `0.618242883149283`.
- All-signal proxy validation(전체 신호 프록시 검증): PF(수익 팩터) `0.9406792484315578`, DD(손실폭) `17.491016868391295`, trades/day(거래/일) `7.355191256830601`.
- All-signal proxy OOS(전체 신호 프록시 표본외): PF(수익 팩터) `1.0518745268223901`, DD(손실폭) `7.077610435743598`, trades/day(거래/일) `7.076335877862595`.
- Filtered sequential proxy validation(필터 순차 프록시 검증): PF(수익 팩터) `0.9484684575915848`, DD(손실폭) `6.896349530108692`, trades/day(거래/일) `3.07103825136612`.
- Filtered sequential proxy OOS(필터 순차 프록시 표본외): PF(수익 팩터) `1.0162130675349095`, DD(손실폭) `3.728607730337241`, trades/day(거래/일) `3.114503816793893`.
- ONNX parity(온엑스 동등성): passed(통과), rows(행) `4096`, max_abs_diff(최대 절대 차이) `2.755990019531751e-07`.
- Feature order(피처 순서): 58 features(피처), hash(해시) `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`.

## Local Interpretation(로컬 해석)

The proxy(프록시)는 density(밀도)는 목표권에 있으나 validation PF/DD(검증 수익 팩터/손실폭)가 약하다. User rule(사용자 규칙)은 frontier stage(전선 단계)마다 MT5 runtime probe(MT5 런타임 탐침)를 생략하지 말라는 쪽이므로, invalid setup(무효 설정)이 아니라면 narrow MT5 probe(좁은 MT5 탐침)를 진행하려 한다.

## Review Questions(검토 질문)

1. Is this setup invalid before MT5(이 설정이 MT5 전에 무효인가), or is it a weak-but-valid runtime probe(약하지만 유효한 런타임 탐침)인가?
2. If Codex proceeds(코덱스가 진행한다면), which failure mode(실패 모드)를 반드시 분리 기록해야 하는가: source_no_transfer(원천 전이 실패), density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴), proxy_still_misaligned(프록시 여전히 불정렬), or parity_fail(동등성 실패)?
3. Any pre-MT5 local check(사전 MT5 로컬 확인) still missing from this bounded evidence(제한 근거)인가?

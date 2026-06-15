# Frontier57 Stage-Open Review(전선57 단계 개방 검토)

Answer only from this bounded snapshot(제한 스냅샷만 사용). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(웹 검색 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient(근거 부족), say needs_local_verification(로컬 검증 필요).

Codex current truth(코덱스 현재 진실):

- F56 closed as `negative_memory_adverse_excursion_source_did_not_transfer(부정 기억, 불리 이동 회피 원천이 MT5로 전이되지 않음)`.
- F56 MT5 validation(검증): PF(수익 팩터)=0.46, DD(손실폭)=29.91%, trades/day(거래/일)=7.59, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0.
- F56 MT5 OOS(표본외): PF(수익 팩터)=0.74, DD(손실폭)=9.27%, trades/day(거래/일)=7.77, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0.
- F56 proxy(프록시) selected by raw signal density(원신호 밀도) and weak PF margin(약한 수익 팩터 여유), but proxy filtered trades/day(프록시 필터 거래/일) was only about 3.2~3.5 while MT5 traded about 7.6~7.8/day.
- F56 closeout clue(마감 단서): MT5 trade rate(MT5 거래 빈도) tracked raw signal rate(원신호 빈도), not proxy filtered trade rate(프록시 필터 거래 빈도). Parity(동등성)는 blocker(차단 요인)가 아니었다.

Codex proposed F57 direction(코덱스 제안 F57 방향):

- Stage(단계): `stage_frontier_57__short_pf_edge_after_adverse_excursion_memory`
- Hypothesis(가설): A short source(숏 원천) trained on fast-exit profitable trades(빠른 청산 수익 거래) and selected by execution-aligned all-signal proxy(실행 정렬 전체 신호 프록시) may transfer better to MT5 than F56’s filtered sequential proxy(필터 순차 프록시).
- Changed variable(변경 변수): label/source(라벨/원천) changes from adverse-excursion stop-avoidance(불리 이동 손절 회피) to fast-exit positive execution(빠른 청산 양수 실행); proxy ranking(프록시 순위) changes from sequential non-overlap trades(순차 비중복 거래) to all raw signals as executable trades(모든 원신호를 실행 거래로 간주).
- Fixed variables(고정 변수): US100 M5, Tier A validation/OOS split(티어 A 검증/표본외 분할), 58-feature order(58개 피처 순서), ExtraTrees depth6 leaf80(엑스트라트리 깊이6 리프80), short-only(숏 전용), direct ONNX threshold(직접 온엑스 임계값), no sparse admission(희소 진입 없음), no RuntimeVetoTape(런타임 차단 테이프 없음), same ATR SL/TP and max_hold=6(같은 ATR 손절/익절과 최대 보유 6봉).
- Mandatory probe(필수 탐침): one MT5 runtime probe(MT5 런타임 탐침 한 회) after proxy and pre-MT5 review(MT5 전 검토).

Success criteria for exploration(탐색 성공 기준):

- proxy all-signal PF(전체 신호 프록시 수익 팩터) improves both validation and OOS(검증/표본외) with raw signal density(원신호 밀도) around 5~10/day(일 5~10회).
- MT5 probe records PF/DD/density and proxy-runtime gap(프록시-런타임 차이) with signal_diff=0 and feature_ready_diff=0 if handoff is aligned(인계 정렬).
- Closeout(마감)는 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 주장하지 않는다.

Failure criteria(실패 기준):

- proxy all-signal economics(전체 신호 프록시 경제성) is still weak or unstable.
- MT5 PF remains below 1 or DD remains large despite parity(동등성).
- density aligns but economics collapse(경제성 붕괴) repeats.

Questions(질문):

1. Is this F57 direction(방향) meaningfully new versus F56, or is it just a repair loop(수리 반복)?
2. What local checks(로컬 점검) must Codex do before MT5?
3. What closeout memory(마감 기억) should be required if MT5 fails again?

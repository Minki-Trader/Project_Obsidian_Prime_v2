# Frontier56 Pre-MT5 Review(전선56 MT5 전 검토)

Codex(코덱스)가 소유한 local verification(로컬 검증) 전제:

- Stage(단계): `stage_frontier_56__short_pf_edge_after_sparse_admission_memory`
- Lifecycle(생명주기): hypothesis(가설) -> proxy(프록시) -> MT5 runtime probe(MT5 런타임 탐침) -> closeout(마감)
- Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
- User rule(사용자 규칙): every frontier stage(모든 전선 단계)는 MT5 runtime probe(MT5 런타임 탐침)를 실행한다.

Current hypothesis(현재 가설):

- F55 sparse admission memory(F55 희소 진입 기억) 뒤에 admission budget/min-gap(진입 예산/최소 간격)을 더 고치지 않는다.
- Instead(대신), train-only adverse-excursion stop-avoidance label(학습 전용 불리 이동 손절 회피 라벨)이 short PF source(숏 수익 팩터 원천)인지 확인한다.
- Runtime handoff(런타임 인계)는 direct ONNX score threshold(직접 온엑스 점수 임계값)만 쓴다. RuntimeVetoTape(런타임 차단 테이프), sparse admission(희소 진입), daily budget(일일 예산), min-gap repair(최소 간격 수리)는 쓰지 않는다.

Stage-open Grok review(단계 개방 그록 검토) summary(요약):

- Accepted(수용): F56 is meaningfully new(F56은 의미 있게 새롭다) vs F55 because the source is adverse-excursion label(불리 이동 라벨 원천) rather than sparse admission repair(희소 진입 수리).
- Needs local verification(로컬 검증 필요): no F55 admission inheritance(F55 진입 상속 없음), short-only density/parity(숏 전용 밀도/동등성), isolated runtime PnL consistency(분리 런타임 손익 일관성).
- Risk(위험): proxy-to-runtime economics collapse(프록시-런타임 경제성 붕괴), label path artifact(라벨 경로 산물), single-point quantile fragility(단일 분위수 취약성).

Proxy result(프록시 결과), selected candidate(선택 후보):

- candidate(후보): `f56b_adverse_excursion_extratrees_d6_l80_short_mae65_mfe55_q85`
- model(모델): ExtraTrees depth6 leaf80(엑스트라트리 깊이6 리프80)
- label(라벨): mae_q(불리 이동 분위수)=0.65, mfe_q(유리 이동 분위수)=0.55
- score threshold(점수 임계값): 0.5121123349374105, score_q(점수 분위수)=0.85
- validation proxy(검증 프록시): PF(수익 팩터)=1.0547158637235754, DD(손실폭)=4.540304264664064, proxy trades/day(프록시 거래/일)=3.1639344262295084, raw signals/day(원신호/일)=7.628415300546448
- OOS proxy(표본외 프록시): PF(수익 팩터)=1.053491019549931, DD(손실폭)=3.4813582772239893, proxy trades/day(프록시 거래/일)=3.4656488549618323, raw signals/day(원신호/일)=7.893129770992366
- ONNX parity(온엑스 동등성): passed(통과), max_abs_diff(최대 절대 차이)=2.288146268014657e-07

Selection note(선택 메모):

- Codex(코덱스)는 F54/F55 memory(F54/F55 기억) 때문에 raw signal density(원신호 밀도) 5-10/day(일 5-10회)를 먼저 보았다.
- This means(이 뜻은) proxy trades/day(프록시 거래/일)는 target(목표)보다 낮지만, MT5 order path(MT5 주문 경로)에서는 exit/hold mechanics(청산/보유 구조) 때문에 actual trade density(실제 거래 밀도)를 직접 관찰해야 한다.
- This is not promotion selection(승격 선택이 아님). It is one mandatory runtime probe(필수 런타임 탐침 한 회) only(전용) for this stage closeout(단계 마감).

Question(질문):

1. Under the mandatory probe rule(필수 탐침 규칙 아래), is one MT5 runtime probe(MT5 런타임 탐침 한 회) acceptable despite weak PF margin(약한 수익 팩터 여유) and proxy trade density below target(목표보다 낮은 프록시 거래 밀도)?
2. What observations(관찰점) must Codex(코덱스) record after MT5 to avoid overclaiming(과장 주장 방지)?
3. Are there any invalid setup(무효 설정) risks in this bounded snapshot(제한 스냅샷) that should stop the probe before execution(실행 전 중단)?

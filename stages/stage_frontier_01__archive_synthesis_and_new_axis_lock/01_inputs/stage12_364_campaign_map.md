# Stage12~364 Campaign Map(캠페인 지도)

이 문서는 Stage12~364(12~364단계)를 reference archive(참조 보관소)로 압축한다.

Action(행동): 과거 단계(stage, 단계)를 campaign group(캠페인 묶음), preserved clue(보존 단서), negative memory(부정 기억), do-not-repeat note(반복 금지 메모)로 분류한다.

Effect(효과): 다음 frontier stage(전선 단계)는 과거 winner(승자), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 상속하지 않고 필요한 기억만 참조한다.

## Source Boundary(원천 경계)

- stage folder count(단계 폴더 수): `355`
- run registry rows(실행 등록부 행): `1953`
- alpha ledger rows(알파 장부 행): `12327`
- ONNX-related alpha rows(ONNX 관련 알파 행): `1215`
- current closeout anchor(현재 마감 기준점): `run364HS_stage364_closeout_no_next_stage.md`

These counts(집계 수치)는 archive read(보관소 판독)의 scope marker(범위 표식)다. They are not performance claims(성과 주장 아님).

## Campaign Groups(캠페인 묶음)

| group_id(묶음 ID) | stage span(단계 범위) | campaign read(캠페인 판독) | import rule(반입 규칙) |
|---|---:|---|---|
| `G1_model_family_scouts` | Stage12~32(12~32단계) | model family challenge(모델군 도전), QDA(이차 판별 분석), NGBoost(엔지부스트), quantile(분위수), TabNet(탭넷), TCN(시간 합성곱) 등 구조 탐색이 많았다. | model shape clue(모델 형태 단서)만 반입한다. winner(승자)는 반입하지 않는다. |
| `G2_context_feature_decision` | Stage33~55(33~55단계) | candle morphology(캔들 형태), regime(국면), decision layer(의사결정 층), risk filter(위험 필터)가 단독 축으로 시험됐다. | context vocabulary(문맥 어휘)와 failure memory(실패 기억)를 반입한다. 단독 필터를 재사용 후보로 올리지 않는다. |
| `G3_dense_adapter_repair_chain` | Stage56~267(56~267단계) | base engine(기반 엔진)과 adapter research(어댑터 연구)가 density/PF/DD/cost(밀도/수익 팩터/손실폭/비용)를 반복 수리했다. | one-axis repair(한 축 수리) 실패 기억을 반입한다. baseline(기준선)이나 selected adapter(선택 어댑터)는 상속하지 않는다. |
| `G4_onnx_candidate_campaign` | Stage268~328(268~328단계) | ONNX candidate campaign(ONNX 후보 캠페인)은 package blueprint(패키지 청사진), feature order(피처 순서), runtime handoff(런타임 인계), candidate distinguishability(후보 구분성)를 다뤘다. | runtime packaging lesson(런타임 패키징 교훈)만 반입한다. 후보 ID(candidate ID, 후보 ID)는 상속하지 않는다. |
| `G5_validation_runtime_guard` | Stage329~340(329~340단계) | forward safety(전방 안전성), overfit guard(과적합 보호), source control(원천 제어), runtime probe(런타임 탐침)가 강화됐다. | validation order(검증 순서)와 no-authority boundary(권위 없음 경계)를 반입한다. |
| `G6_dense_cost_source_regime_pivot` | Stage341~364(341~364단계) | dense cost recovery(고밀도 비용 회복)와 source regime label pivot(원천 국면 라벨 전환)이 비용/밀도/수익 동시성을 압박했다. | preserved clue(보존 단서)와 capped repair memory(상한 있는 수리 기억)를 반입한다. Stage364(364단계)는 negative memory(부정 기억)로 닫는다. |

## Preserved Clues(보존 단서)

1. Stage364(364단계) `hold4_margin_0.01`: Tier A separate(Tier A 분리) net/PF/density(순수익/수익 팩터/밀도) `462.0071630903 / 1.2257899553 / 2.1178343949`, strict_joint_pass_count(엄격 동시 통과 수) `0`.
2. `run364HL` MT5 runtime clue(MT5 런타임 단서): actual routed total(실제 라우팅 전체) net/PF/trades/density(순수익/수익 팩터/거래 수/밀도) `369.03 / 1.39 / 542 / 1.7261146497`; guardrail(보호 조건)은 density below 3(밀도 3 미만), short-heavy(숏 편중), cost stress failed(비용 압박 실패), route parity partial(라우트 동등성 부분)이다.
3. `run364HM` proxy-scaled seed(프록시 스케일 씨앗): scaled_density(스케일 밀도) `3.055518353`, OOS PF(표본외 수익 팩터) `1.4709758917`, cost09(비용0.9) `15.101`; direct strict pass(직접 엄격 통과)는 `0`이고 new MT5(새 MT5)는 없다.
4. `run364HQ` runtime observation(런타임 관찰): actual routed total(실제 라우팅 전체) net/PF/trades/density/DD(순수익/수익 팩터/거래 수/밀도/손실폭) `113.38 / 1.05 / 932 / 2.9681528662 / 45.8%`; positive net(양수 순수익)은 보존하지만 PF/DD/density boundary(PF/DD/밀도 경계)는 실패다.
5. Stage11(11단계) fwd18 inverse-rank context(fwd18 역순위 문맥)는 tiny-sample clue(얇은 표본 단서)다. high PF(높은 수익 팩터)가 있었지만 trade count(거래 수)가 너무 작아 stress-first memory(압박 우선 기억)로만 남긴다.
6. Stage12(12단계) ExtraTrees variants(엑스트라트리스 변형) such as `v09_depth8_leaf10_q90` and `v16_base_long_only_q90` are structural scout clues(구조 탐색 단서) only.
7. Stage40(40단계) candle morphology(캔들 형태) `c13` clue(단서)는 양쪽 양수 가능성을 보였지만 thin trade count(얇은 거래 수) 때문에 standalone repeat(단독 반복)는 금지한다.

## Negative Memories(부정 기억)

- Candidate distinguishability collapse(후보 구분성 붕괴): Stage267(267단계) proxy score ablation(프록시 점수 제거)에서 여러 candidate(후보)가 같은 MT5 KPI(MT5 핵심 성과 지표) signature(서명)로 접혔다.
- Single-axis repair loop(단일 축 수리 반복): density-only(밀도만), PF-only(PF만), cost-only(비용만), OOS-only(표본외만) 수리는 한 축을 살리며 다른 축을 깨는 패턴이 반복됐다.
- Sparse PF999 selector(희소 PF999 선택기): PF(profit factor, 수익 팩터)가 비정상적으로 커도 trade count(거래 수)와 density(밀도)가 얇으면 후보 품질을 만들지 못했다.
- Proxy-to-MT5 gap(프록시와 MT5 차이): package-only(패키지 전용), scaled-density(스케일 밀도), expected density(예상 밀도)는 tester output(테스터 출력)을 대체하지 못한다.
- Tier B/combined gaps(Tier B/합산 공백): Tier B(티어 B)와 Tier A+B combined(Tier A+B 합산)가 missing_required(필수 누락)일 때 전체 alpha read(알파 판독)으로 올리면 안 된다.

## Frontier Interface(전선 접점)

The next frontier hypothesis(다음 전선 가설)는 아래 interface(접점)를 받아야 한다.

- Use four-axis joint objective(네 축 동시 목적): density(밀도), PF(수익 팩터), DD(손실폭), curve smoothness(곡선 매끄러움)를 동시에 본다.
- Treat target completion gates(완성 목표 게이트)는 final completion review(최종 완성 검토)에서만 hard gate(강제 게이트)로 둔다.
- During early exploration(초기 탐색) say only scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), completion candidate(완성 후보) when justified.
- Require Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산) or explicit missing_required(필수 누락).
- Before expensive WFO/MT5(비싼 WFO/MT5) ask Grok review(그록 검토), then Codex local verification(코덱스 로컬 검증).

## Claim Boundary(주장 경계)

This map(지도)은 archive interface(보관소 접점) only(전용)다.

Not claimed(주장 안 함): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), selected candidate(선택 후보).

# F74 Stage Closeout Review Prompt(F74 단계 마감 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or do local verification(로컬 검증 금지).

## Stage(단계)

- stage_id(단계 ID): `stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path`
- hypothesis(가설): microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험했다.
- claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Lifecycle Evidence(생명주기 근거)

### F74A Stage Open(단계 개방)

- Grok stage-open review(Grok 단계 개방 검토): accepted(수용).
- Opened axes(개방 축): label/target(라벨/목표), trade shape(거래 형태), risk logic inside label(라벨 내부 위험 로직), model family after raw gate(원시 게이트 뒤 모델 계열).

### F74B Raw Label And Proxy Scout(원시 라벨 및 프록시 탐색)

- raw density pass axes(원시 밀도 통과 축): 6/6.
- raw validation/OOS density(검증/표본외 밀도): about 12.95-13.94 and 14.03-15.33 trades/day(일거래).
- proxy candidates(프록시 후보): 648.
- scout clue(탐색 단서): 0.
- meaningful candidate(의미 후보): 0.
- best F74B validation KPI(검증 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `-2236.54 / 0.6472 / 24.1165% / 1.4669`.
- best F74B OOS KPI(표본외 KPI): `811.95 / 1.1828 / 2.9838% / 1.8684`.
- judgment(판정): `raw_density_passed_proxy_repair_required_no_authority`.

### F74C Clean/Value Label Repair(깨끗한/가치 라벨 수리)

- repair novelty(수리 신규성): changed label/target(라벨/목표 변경): clean_fast_touch(깨끗한 빠른 도달), clean_value_q60(깨끗한 가치 q60), net_edge_q70(순가치 q70).
- candidates(후보): 1296.
- scout clue(탐색 단서): 0.
- meaningful candidate(의미 후보): 0.
- best F74C candidate(최선 후보): `f74c_1212` hist_gbm, but ONNX materialization failed later due converter type error(변환기 타입 오류).
- best materializable candidate(최선 물질화 가능 후보): `f74c_1161`, logistic_l2, clean_value_h9_short, clean_value_q60, cash_mid_late.
- `f74c_1161` proxy validation KPI(프록시 검증 KPI): net/PF/DD/tpd `571.25 / 1.0948 / 7.2277% / 1.6581`.
- `f74c_1161` proxy OOS KPI(프록시 표본외 KPI): `558.88 / 1.1282 / 5.5627% / 1.6250`.
- judgment(판정): `proxy_repair_no_scout_clue_risk_session_decision_required_no_authority`.

### F74D Pre-MT5 Grok Review(MT5 전 Grok 검토)

- Grok classification(그록 분류): accepted(수용).
- Direction(방향): run mandatory negative-control MT5 Runtime Probe(필수 부정 대조 MT5 런타임 탐침), no positive claim(긍정 주장 없음).

### F74E MT5 Runtime Probe(MT5 런타임 탐침)

- materialization repair(물질화 수리): original `f74c_1212` hist_gbm was blocked by skl2onnx TreeEnsembleClassifier boolean/int attribute error(온엑스 변환 오류). Codex used same F74C family materializable logistic candidate `f74c_1161`.
- ONNX probability parity(온엑스 확률 동등성): 3/3 pass.
- signal parity after veto(차단 뒤 신호 동등성): 3/3 pass.
- source reproduction count ratio(원천 재현 카운트 비율): 1.0.
- MT5 attempts/completed(MT5 시도/완료): 2/2.
- validation runtime KPI(검증 런타임 KPI): net/PF/DD/tpd/trades/win rate(순수익/수익 팩터/손실폭/일거래/거래수/승률) `97.11 / 1.16 / 11.40% / 1.6544 / 450 / 34.67%`.
- validation gross profit/loss(검증 총이익/총손실): `717.95 / -620.84`.
- validation average win/loss/payoff/expectancy/recovery(검증 평균이익/평균손실/손익비/기대값/회복): `4.6022 / -2.1117 / 2.1794 / 0.22 / 1.29`.
- OOS runtime KPI(표본외 런타임 KPI): net/PF/DD/tpd/trades/win rate `61.86 / 1.13 / 9.66% / 1.6000 / 312 / 33.65%`.
- OOS gross profit/loss(표본외 총이익/총손실): `520.33 / -458.47`.
- OOS average win/loss/payoff/expectancy/recovery(표본외 평균이익/평균손실/손익비/기대값/회복): `4.9555 / -2.2148 / 2.2374 / 0.20 / 1.06`.
- proxy/runtime gap(프록시/런타임 간극): validation DD rose from proxy 7.23% to runtime 11.40%; OOS DD rose from proxy 5.56% to runtime 9.66%; PF stayed weak around 1.09-1.16; tpd stayed ~1.6.

## Codex Proposed Closeout(Codex 제안 마감)

Close F74 as `closed_preserved_clue_negative_memory_no_authority`.

Preserved clue(보존 단서):

- raw label density gate(원시 라벨 밀도 게이트) passed strongly across all 6 axes.
- short-side binary ONNX materialization(숏 방향 이진 ONNX 물질화), feature parity(피처 동등성), and selected-entry veto signal parity(선택 진입 차단 신호 동등성) can be made exact.
- negative-control runtime probe(부정 대조 런타임 탐침) completed 2/2.

Negative memory(부정 기억):

- dense microburst labels(조밀한 마이크로버스트 라벨) did not produce a meaningful proxy candidate(의미 프록시 후보 0).
- clean/value repair(깨끗한/가치 수리) did not create scout clue(탐색 단서 0).
- MT5 runtime remained weak: validation DD(검증 손실폭) >10%, PF around 1.16, trades/day around 1.65; OOS PF 1.13 and trades/day 1.60.
- This is far from final goals(최종 목표): 5-10 trades/day(일 5~10회), PF 2-3+, DD under 10% every view(모든 보기 손실폭 10% 미만), smooth equity(매끄러운 자산 곡선).

Next frontier proposal(다음 전선 제안):

- Open F75 with a different upstream mechanism(다른 상류 메커니즘), not another F74 threshold/clean-label repair loop.
- Candidate direction: order-flow/volatility compression breakout or session liquidity imbalance(오더플로/변동성 압축 돌파 또는 세션 유동성 불균형) with density and risk built into label, then mandatory runtime probe(필수 런타임 탐침).

## Review Question(검토 질문)

Classify Codex closeout proposal:

- `accepted(수용)`,
- `rejected(거절)`,
- `needs_local_verification(로컬 검증 필요)`.

Also give one preserved clue(보존 단서), one negative memory(부정 기억), and one do-not-repeat note(반복 금지 메모).

Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

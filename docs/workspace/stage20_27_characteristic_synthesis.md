# Stage20-27 Characteristic and MT5 Forensic Synthesis(20-27단계 특징 및 MT5 포렌식 종합)

## Purpose(목적)

이 문서는 Stage20~Stage27(20~27단계)의 model family/topic exploration(모델군/주제 탐색)을 다시 실행하지 않고, 이미 남은 structural scout(구조 탐색), MT5 runtime_probe(MT5 런타임 탐침), closeout packet(마감 묶음)을 특징 파악과 MT5 forensic readout(MT5 포렌식 판독) 관점에서 보강한다.

효과(effect, 효과): 닫힌 단계를 micro-probe(미세 탐침)로 다시 여는 대신, 실제 MT5 routed rerun(MT5 라우팅 재실행)까지 확인해 다음 Stage29~32(29~32단계)에서 어떤 특징 단서(clue, 단서)를 가져갈지 분명하게 만든다.

## Routing Receipt(라우팅 기록)

- packet id(묶음 ID): `stage20_27_characteristic_synthesis_v1`
- actual MT5 rerun packet(실제 MT5 재실행 묶음): `stage20_27_actual_mt5_rerun_verification_v1`
- work packet lifecycle(작업 묶음 생명주기): `evidence_synthesis_to_judgment_to_report(근거 종합-판정-보고)`
- primary family(주 작업군): `kpi_evidence(KPI 근거)`
- primary skill(주 스킬): `obsidian-run-evidence-system(실행 근거 시스템)`
- support skills(보조 스킬): `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`, `obsidian-performance-attribution(성과 귀속)`
- supplemental MT5 checks(보강 MT5 점검): `obsidian-runtime-parity(런타임 동등성)`, `obsidian-backtest-forensics(백테스트 포렌식)`
- final filter(최종 필터): `obsidian-answer-clarity(답변 명료성)`, `obsidian-claim-discipline(주장 규율)`
- branch/worktree fit(브랜치/작업트리 적합성): `codex/stage28-markov-regression`에서 수행한다. Stage28(28단계) run22B(실행22B) 변경이 이미 열려 있어 branch switch(브랜치 전환)는 하지 않는다.

효과(effect, 효과): 이 작업은 새 model run(모델 실행)이나 MT5 tester run(MT5 테스터 실행)이 아니라 cross-stage evidence management(교차 단계 근거 관리)와 recorded MT5 evidence boundary(기록된 MT5 근거 경계)로 닫는다.

## Sufficiency Rule(충분성 규칙)

Stage20~27(20~27단계)의 특징 파악 보강은 아래 항목을 stage(단계)별로 확인하면 완료로 본다.

1. structural lens(구조 렌즈): 해당 model family(모델군)가 무엇을 다르게 읽는지 적혀 있다.
2. tier records(티어 기록): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined/routed(Tier A+B 합산/라우팅) 기록이 있거나 missing reason(누락 사유)이 있다.
3. runtime handoff(런타임 인계): MT5 runtime_probe(MT5 런타임 탐침)가 completed(완료), blocked(차단), 또는 out_of_scope_by_claim(주장 범위 밖)로 정리되어 있다.
4. validation/OOS behavior(검증/표본외 행동): 순손익(net profit, 순손익), profit factor(수익 팩터), trade count(거래 수), drawdown(손실폭) 중 핵심 판독이 적혀 있다.
5. repeated feature axes(반복 피처 축): 다음 단계에서 다시 볼 feature(피처)나 regime(국면) 축이 보존되어 있다.
6. negative memory(부정 기억): 과장하면 안 되는 이유와 reopen condition(재개 조건)이 분리되어 있다.
7. claim boundary(주장 경계): baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다고 명시되어 있다.
8. MT5 forensic boundary(MT5 포렌식 경계): normalized aggregate summary(정규화 집계 요약)와 raw Strategy Tester report(원본 전략 테스터 보고서)의 가용성을 분리한다.

효과(effect, 효과): “적당히 충분”이라는 느낌이 아니라, 다시 파야 할 이유가 있는지 확인 가능한 체크리스트(checklist, 확인 목록)로 닫는다.

## Stage Readout(단계별 판독)

| stage(단계) | topic(주제) | characteristic read(특징 판독) | runtime/trade read(런타임/거래 판독) | preserved clue(보존 단서) | boundary(경계) |
|---|---|---|---|---|---|
| Stage20(20단계) | GAM(`Generalized Additive Model`, 일반화 가산 모델) | smooth additive shape(부드러운 가산 모양)이 price/volatility/direction(가격/변동성/방향) 피처 반응을 보였다. | validation(검증) `8.65 / 1.01 / 211`, OOS(표본외) `295.69 / 1.51 / 125`; drawdown(손실폭) 때문에 운영 주장 불가. | `close_open_ratio`, `log_return_1`, `log_return_3`, volatility(변동성), direction indicator(방향 지표). | score table(점수표) approximation(근사) runtime_probe(런타임 탐침)만 인정. |
| Stage21(21단계) | ElasticNet Logistic(엘라스틱넷 로지스틱) | sparse linear pressure(희소 선형 압력)와 coefficient sign(계수 부호)을 확인했다. | validation(검증) `-113.11 / 0.90 / 173`, OOS(표본외) `-49.77 / 0.94 / 130`; 단독 신호 약함. | `hl_range`, `ema20_ema50_diff`, `atr_50`, `atr_14`, `ema9_ema20_diff`. | ONNX(온닉스) probability-only handoff(확률 전용 인계) 호환성만 인정. |
| Stage22(22단계) | HMM(`Hidden Markov Model`, 은닉 마르코프 모델) | label-free state segmentation(라벨 없는 상태 분할)이 volatility/session/trend(변동성/세션/추세) 렌즈가 될 수 있었다. | validation(검증) `-497.25 / 0.69 / 279`, OOS(표본외) `121.96 / 1.05 / 562`; 검증 손실이 커서 edge(거래 우위) 아님. | `v02_core17_4state_diag` non-collapsed state(비붕괴 상태), precomputed state handoff(사전 계산 상태 인계). | live recalculation(실시간 재계산)이 아니므로 runtime authority(런타임 권위) 아님. |
| Stage23(23단계) | supervised regime classifier(지도 국면 분류기) | p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽을 수 있었다. | validation(검증) `324.75 / 1.16 / 476`, OOS(표본외) `254.63 / 1.19 / 345`; 단일 runtime_probe(런타임 탐침) 양수. | `rsi_14`, `close_ema20_ratio`, `hl_range`, `historical_vol_20`, `minutes_from_cash_open`. | Stage30 calibration/abstention(보정/기권) 단서이지 alpha quality(알파 품질) 아님. |
| Stage24(24단계) | Survival model(생존 모델) | time-to-event(사건까지 시간), censoring(검열), hold/exit clock(보유/청산 시계)을 읽었다. | validation(검증) `-157.74 / 0.90 / 2195`, OOS(표본외) `-98.54 / 0.88 / 1100`; 거래 경로는 부정적. | `hl_range`, `historical_vol_20`, `is_first_30m_after_open`, `bollinger_width_20`, `atr_14`. | exit-only(청산 전용) 또는 permission(허용) 단서로만 보존. |
| Stage25(25단계) | hazard model(위험률 모델) | elapsed-bar hazard(경과 봉 위험률)가 reversal/loss timing(반전/손실 시점)을 읽었다. | validation(검증) `-89.59 / 0.94 / 2145`, OOS(표본외) `-174.49 / 0.83 / 1210`; 거래 경로는 부정적. | `hazard_elapsed_bar`, `hazard_elapsed_frac`, `historical_vol_20`, `hl_range`, `close_ema20_ratio`. | dynamic position-age runtime(동적 포지션 나이 런타임) 아님. |
| Stage26(26단계) | NGBoost(`Natural Gradient Boosting`, 자연 그래디언트 부스팅) | distributional uncertainty(분포 불확실성), entropy(엔트로피), direction bias(방향 편향)를 읽었다. | validation(검증) `-17.21 / 0.05 / 6`, OOS(표본외) `39.49 / 2.37 / 10`; 작은 표본 양수. | entropy(엔트로피), nonflat confidence(비평탄 확신), core42 distribution surface(42개 핵심 피처 분포 표면). | native NGBoost runtime(원본 NGBoost 런타임)이 아니라 distilled score table(증류 점수표). |
| Stage27(27단계) | quantile boosting(분위수 부스팅) | tail-risk surface(꼬리 위험 표면), interval coverage(구간 포괄), tail pressure(꼬리 압력)를 읽었다. | validation(검증) `-38.20 / 0.97 / 665`, OOS(표본외) `79.17 / 1.07 / 576`; 탐침 경계 안의 약한 양수. | `historical_vol_20`, `hl_range`, `minutes_from_cash_open`, `bollinger_width_20`, `ema50_ema200_diff`; Tier B fallback(티어 B 대체) 실제 사용. | score-table handoff(점수표 인계) runtime_probe(런타임 탐침)만 인정. |

## MT5 Forensic Readout(MT5 포렌식 판독)

MT5(`MetaTrader 5`, 메타트레이더5) 판독은 각 runtime probe(런타임 탐침)의 aggregate summary(집계 요약), normalized KPI(`Key Performance Indicator`, 핵심 성과 지표), closeout packet(마감 묶음)을 기준으로 먼저 세웠고, 이후 `stage20_27_actual_mt5_rerun_verification_v1`에서 실제 Strategy Tester(전략 테스터) `routed_validation_is(검증 라우팅)`와 `routed_oos(표본외 라우팅)` 16개를 재실행해 확인했다.

효과(effect, 효과): 특징 판독은 이제 raw tester report(원본 테스터 보고서) 재생성 근거를 갖지만, 전체 tier_a_only/tier_b_fallback_only(Tier A 전용/Tier B 대체 전용) 6-view full rerun(6개 보기 전체 재실행)은 아니므로 claim boundary(주장 경계)는 유지한다.

| stage(단계) | MT5 KPI/normalized(MT5 핵심 성과 지표/정규화) | validation(검증) | OOS(표본외) | route/fill/Tier B(라우팅/체결/Tier B) | MT5 read(MT5 판독) |
|---|---:|---|---|---|---|
| Stage20(20단계) | `10 / 10` | `8.65 / 1.01 / 211 / DD(손실폭) 36.26%` | `295.69 / 1.51 / 125 / DD(손실폭) 17.98%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `13` | OOS(표본외)는 강하지만 validation(검증)이 거의 평탄하고 drawdown(손실폭)이 커서 runtime_probe(런타임 탐침) 경계만 인정. |
| Stage21(21단계) | `10 / 10` | `-113.11 / 0.90 / 173 / DD(손실폭) 45.64%` | `-49.77 / 0.94 / 130 / DD(손실폭) 29.25%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `19` | 주문 실패가 아니라 sparse linear signal(희소 선형 신호) 자체가 약했다. |
| Stage22(22단계) | `10 / 10` | `-497.25 / 0.69 / 279 / DD(손실폭) 99.55%` | `121.96 / 1.05 / 562 / DD(손실폭) 47.16%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `69` | OOS(표본외) 양수만으로는 부족하고, validation(검증) 붕괴와 long-only(매수 전용) 모양 때문에 edge(거래 우위) 아님. |
| Stage23(23단계) | `10 / 10` | `324.75 / 1.16 / 476 / DD(손실폭) 50.90%` | `254.63 / 1.19 / 345 / DD(손실폭) 18.08%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `34` | Stage20~27(20~27단계) 안에서는 가장 균형 잡힌 양수지만 validation drawdown(검증 손실폭)이 커서 calibration/abstention clue(보정/기권 단서)로만 보존. |
| Stage24(24단계) | `10 / 10` | `-157.74 / 0.90 / 2195 / DD(손실폭) 49.60%` | `-98.54 / 0.88 / 1100 / DD(손실폭) 26.58%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `318` | trade density(거래 밀도)는 높지만 PnL(손익)이 음수라 entry(진입)보다 exit/risk lens(청산/위험 렌즈)로 보존. |
| Stage25(25단계) | `10 / 10` | `-89.59 / 0.94 / 2145 / DD(손실폭) 32.63%` | `-174.49 / 0.83 / 1210 / DD(손실폭) 39.20%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `329` | hazard(위험률)는 거래를 많이 만들었지만 수익 경로가 나빠, position-age risk(포지션 나이 위험) 단서로만 남긴다. |
| Stage26(26단계) | `10 / 6` | `-17.21 / 0.05 / 6 / DD(손실폭) 4.26%` | `39.49 / 2.37 / 10 / DD(손실폭) 4.33%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `0` | OOS(표본외) PF(수익 팩터)는 높지만 표본이 너무 작아 uncertainty clue(불확실성 단서)만 인정. |
| Stage27(27단계) | `10 / 6` | `-38.20 / 0.97 / 665 / DD(손실폭) 53.95%` | `79.17 / 1.07 / 576 / DD(손실폭) 30.01%` | OOS fill rate(표본외 체결률) `1.0`, reject(거부) `0`, Tier B orders(티어 B 주문) `167` | Tier B fallback(티어 B 대체)이 실제 주문을 메웠지만 validation(검증) 음수와 높은 drawdown(손실폭) 때문에 tail-risk clue(꼬리 위험 단서)만 남긴다. |

MT5 cross-check(MT5 교차 점검):

- All stages(전체 단계)는 aggregate summary(집계 요약) 기준 MT5 KPI records(MT5 핵심 성과 지표 기록) `10`개를 남겼다. Stage26~27(26~27단계)은 normalized records(정규화 기록)가 `6`개라 normalized view(정규화 보기) 경계를 따로 붙인다.
- parser error(파서 오류)와 trade parser error(거래 파서 오류)는 모두 `0`이다. 효과(effect, 효과)는 실패 원인을 report parsing(보고서 파싱)이 아니라 signal/risk/trade shape(신호/위험/거래 모양) 쪽에서 보게 하는 것이다.
- OOS fill rate(표본외 체결률)는 모두 `1.0`, reject count(거부 수)는 모두 `0`이다. 효과(effect, 효과)는 Stage20~27(20~27단계)의 약점이 broker/order rejection(브로커/주문 거부) 문제가 아니라는 점을 분리하는 것이다.
- actual MT5 rerun(실제 MT5 재실행): Stage20~27(20~27단계) `routed_validation_is(검증 라우팅)`와 `routed_oos(표본외 라우팅)` 16개가 모두 `tester=completed(테스터 완료)`, `runtime=completed(런타임 완료)`, `report=completed(보고서 완료)`다. 판정(judgment, 판정)은 `completed_actual_mt5_routed_rerun_verification_not_new_alpha_quality`.
- skip/model_fail count(건너뜀/모델 실패 수)는 여러 stage(단계)에서 크다. 효과(effect, 효과)는 이를 파서 실패가 아니라 feature CSV/timestamp/tier handoff boundary(피처 CSV/타임스탬프/티어 인계 경계)로 분리해 다음 runtime handoff repair(런타임 인계 수정) 후보에 넣는 것이다.

## Cross-Stage Patterns(교차 단계 패턴)

1. Repeated feature axes(반복 피처 축): `hl_range`, `historical_vol_20`, `bollinger_width_20`, `rsi_14`, `close_ema20_ratio`, `minutes_from_cash_open`, EMA spread(이동평균 차이)가 여러 stage(단계)에 반복 등장했다.
2. Permission/abstention lane(허용/기권 레인): Stage23(23단계) p_flat(평탄 확률), Stage26(26단계) entropy(엔트로피), Stage27(27단계) tail pressure(꼬리 압력)는 Stage30(30단계) calibration/abstention(보정/기권)에서 broad synthesis(넓은 종합)로 다시 볼 가치가 있다.
3. Exit/risk lane(청산/위험 레인): Stage24(24단계) survival(생존)과 Stage25(25단계) hazard(위험률)는 entry score(진입 점수)보다 close/flat pressure(청산/평탄 압력)로 읽어야 한다.
4. Runtime handoff pattern(런타임 인계 패턴): Stage20(20단계), Stage26(26단계), Stage27(27단계)는 native model runtime(원본 모델 런타임)이 아니라 score table(점수표) approximation(근사)으로 MT5 runtime_probe(MT5 런타임 탐침)를 수행했다.
5. Tier B role(티어 B 역할): Tier B(티어 B)는 탐색 허가 문제가 아니라 fallback coverage(대체 커버리지) 문제다. Stage27(27단계)은 Tier B fallback(티어 B 대체)이 실제 라우팅 빈 구간을 메웠다는 기록을 남겼다.
6. MT5 trade shape(MT5 거래 모양): Stage23(23단계)은 양수 균형이 가장 좋고, Stage20(20단계)은 OOS(표본외)만 강하며, Stage24~25(24~25단계)는 고밀도 음수 거래라 exit/risk clue(청산/위험 단서)로 읽는다.

효과(effect, 효과): Stage20~27(20~27단계)은 “승자 후보”가 아니라, Stage29~32(29~32단계)의 broad design(넓은 설계)에 줄 수 있는 feature/regime/risk clues(피처/국면/위험 단서)를 남긴 것으로 읽는다.

## Not Confirmed(아직 확인 아님)

- alpha quality(알파 품질): 확인 아님.
- baseline(기준선): 없음.
- promotion candidate(승격 후보): 없음.
- operating promotion(운영 승격): 없음.
- runtime authority(런타임 권위): 없음.
- full WFO(`walk-forward optimization`, 워크포워드 최적화): Stage20~27(20~27단계) 특징 보강 패킷의 범위 밖.
- routed raw Strategy Tester report availability(라우팅 원본 전략 테스터 보고서 가용성): Stage20~27(20~27단계)의 validation/OOS(검증/표본외) 라우팅 보고서 16개는 실제 재실행 후 생성 및 확인됨.
- tester identity/cost assumptions(테스터 정체성/비용 가정): raw report(원본 보고서)에서 완전 재확인하지 않음.

효과(effect, 효과): Stage20~27(20~27단계)의 특징 단서를 다음 설계에 쓸 수는 있지만, 운영 의미로 승격하지 않는다.

## Reopen Conditions(재개 조건)

Stage20~27(20~27단계)를 같은 형태의 micro-probe(미세 탐침)로 다시 열지 않는다. 다시 열 수 있는 조건은 아래처럼 broad packet(넓은 묶음)이어야 한다.

- Stage30(30단계) calibration/abstention(보정/기권)에서 p_flat(평탄 확률), entropy(엔트로피), tail pressure(꼬리 압력)를 하나의 permission surface(허용 표면)로 비교할 때.
- exit-only(청산 전용) 패킷에서 survival risk(생존 위험)와 hazard risk(위험률 위험)를 entry score(진입 점수) 없이 비교할 때.
- WFO(워크포워드 최적화)나 rolling window(구르는 구간)로 Stage23/27(23/27단계)의 양수 판독이 반복되는지 확인할 때.
- MT5 feature CSV boundary(피처 CSV 경계)와 tester interval(테스터 구간) skip(건너뜀)을 줄이는 runtime handoff repair(런타임 인계 수정)가 필요할 때.
- full tier-view rerun(전체 티어 보기 재실행) 또는 tester identity/cost audit(테스터 정체성/비용 감사)이 필요할 때.

효과(effect, 효과): “조금 더 만져보기”가 아니라 새 질문(question, 질문)과 새 비교축(comparison axis, 비교축)이 있을 때만 재개한다.

## Judgment(판정)

Stage20~27(20~27단계)의 특징 파악과 MT5 forensic readout(MT5 포렌식 판독)은 user goal(사용자 목표) 기준으로 보강 완료(completed supplement, 보강 완료)다.

판정(judgment, 판정): `completed_characteristic_and_actual_mt5_routed_rerun_synthesis_not_new_alpha_quality`.

주장 경계(claim boundary, 주장 경계): `cross_stage_characteristic_and_mt5_forensic_synthesis_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`.

효과(effect, 효과): Stage28(28단계)은 여전히 run22B(실행22B) 복구가 현재 실행 경계이고, Stage20~27(20~27단계)은 특징 단서 지도(characteristic clue map, 특징 단서 지도)로 고정한다.

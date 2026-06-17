# Frontier74 Stage Closeout(F74 전선 단계 마감)

Updated(갱신): 2026-06-17T04:13:20Z

## Closeout Label(마감 라벨)

`closed_preserved_clue_negative_memory_no_authority`

Claim boundary(주장 경계): `preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.

## Hypothesis(가설)

microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험한다.

Effect(효과): microburst label family(마이크로버스트 라벨군)이 밀도와 런타임 경제성을 동시에 만들 수 있는지 닫힌 근거로 확인했다.

## Test Period(테스트 기간)

- runtime validation(런타임 검증): `2025-01-02..2025-10-01`.
- runtime OOS(런타임 표본외): `2025-10-01..2026-04-14`.

## Proxy Expectation(프록시 예상)

density(밀도)는 label/target(라벨/목표)에서 먼저 만들고, proxy(프록시)는 PF/DD/거래밀도를 동시에 살리는 seed surface(씨앗 표면)를 찾는다는 기대였다.

## Proxy KPI(프록시 핵심 성과 지표)

- F74B raw density pass(원시 밀도 통과): `6/6` axes(축).
- F74B candidates(후보): `648`, scout clue(탐색 단서) `0`, meaningful candidate(의미 후보) `0`.
- F74B best validation(최선 검증): `net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) -2236.54/0.6472/24.1165%/1.4669/399`.
- F74B best OOS(최선 표본외): `net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) 811.95/1.1828/2.9838%/1.8684/355`.
- F74C candidates(후보): `1296`, scout clue(탐색 단서) `0`, meaningful candidate(의미 후보) `0`.
- F74C best candidate(최선 후보): `f74c_1212 hist_gbm clean_value_h9_short`, validation(검증) `net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) 747.69/1.1290/6.3779%/1.6949/461`, OOS(표본외) `net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) -469.75/0.9164/7.0489%/2.0769/405`.
- F74C materialized candidate(물질화 후보): `f74c_1161 logistic_l2 clean_value_h9_short`, validation(검증) `net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) 571.25/1.0948/7.2277%/1.6581/451`, OOS(표본외) `net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일거래/거래수) 558.88/1.1282/5.5627%/1.6250/312`.

## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)

- F74D pre-MT5 Grok review(MT5 전 그록 검토): `accepted(수용)`.
- F74E MT5 attempts/completed(MT5 시도/완료): `2/2`.
- probability parity(확률 동등성): `3/3`.
- signal count parity(신호 수 동등성): `3/3`, validation/OOS diff(검증/표본외 차이) `0/0`.
- feature readiness parity(피처 준비 동등성): validation/OOS diff(검증/표본외 차이) `0/0`.
- validation runtime(검증 런타임): `net/PF/DD/tpd/trades/win(순수익/수익 팩터/손실폭/일거래/거래수/승률) 97.11/1.16/11.40%/1.6544/450/34.67%`.
- OOS runtime(표본외 런타임): `net/PF/DD/tpd/trades/win(순수익/수익 팩터/손실폭/일거래/거래수/승률) 61.86/1.13/9.66%/1.6000/312/33.65%`.
- proxy/runtime gap cause(프록시/런타임 간극 원인): `runtime_economics_gap_after_signal_and_feature_parity(신호와 피처 준비 동등성 뒤에도 런타임 경제성 간극 발생)`.

## Closeout KPI(마감 핵심 성과 지표)

| test period(테스트 기간) | split/view(분할/보기) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trade count(거래 수) | trades/day(일 거래 수) | win rate(승률) | average win(평균 이익) | average loss(평균 손실) | payoff ratio(손익비) | expectancy(기대값) | recovery factor(회복 계수) | time under water(회복 전 체류 시간) | max consecutive loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| `2025-01-02..2025-10-01` | `F74E MT5 negative-control runtime probe(부정 대조 런타임 탐침) validation(분할) Tier A separate(Tier A 분리)` | `97.11` | `717.95` | `-620.84` | `1.16` | `11.4%` | `450` | `1.6544117647058822` | `34.67%` | `4.60224358974359` | `-2.1117006802721088` | `2.179401480872069` | `0.22` | `1.29` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `0/450` | `signal_diff=0; feature_ready_diff=0; PF proxy/runtime 1.09476719685502/1.16; DD proxy/runtime 7.227736867141739%/11.4%; tpd proxy/runtime 1.6580882352941178/1.6544117647058822` |
| `2025-10-01..2026-04-14` | `F74E MT5 negative-control runtime probe(부정 대조 런타임 탐침) oos(분할) Tier A separate(Tier A 분리)` | `61.86` | `520.33` | `-458.47` | `1.13` | `9.66%` | `312` | `1.6` | `33.65%` | `4.95552380952381` | `-2.214830917874396` | `2.237427593019017` | `0.2` | `1.06` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `0/312` | `signal_diff=0; feature_ready_diff=0; PF proxy/runtime 1.1281810692101244/1.13; DD proxy/runtime 5.562675325393684%/9.66%; tpd proxy/runtime 1.625/1.6` |

## Known Difference(알려진 차이)

- F74E runtime receipt(런타임 영수증)의 run_id column(실행 ID 열)은 reused helper(재사용 보조 함수) 때문에 frontier71D로 남아 있다. attempt_name/report_path/run_manifest(시도명/보고서 경로/실행 목록)는 F74E를 가리키므로 runtime failure(런타임 실패)가 아니라 reporting defect(보고 결함)로 기록한다.

## Preserved Clue(보존 단서)

- Raw density gate(원시 밀도 게이트)는 6/6 axes(축)에서 강하게 통과했다.
- Short-side binary ONNX materialization(숏 방향 이진 ONNX 물질화), probability parity(확률 동등성), signal parity(신호 동등성)는 3/3으로 맞출 수 있었다.
- Mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)는 validation/OOS(검증/표본외) 2/2로 실행됐다.

## Negative Memory(부정 기억)

- F74B 648개 후보와 F74C 1296개 후보 모두 scout clue(탐색 단서) 0, meaningful candidate(의미 후보) 0이었다.
- Best materializable runtime path(최선 물질화 가능 런타임 경로)는 validation PF 1.16, DD 11.40%, trades/day 1.6544에 그쳤다.
- OOS runtime(표본외 런타임)도 PF 1.13, trades/day 1.60으로 final goal(최종 목표)의 5-10 trades/day와 PF 2-3+에서 멀다.

## Grok Closeout Review(Grok 마감 검토)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f74_stage_closeout_microburst_turnover_label`.
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f74_stage_closeout_microburst_turnover_label/prompts/f74_stage_closeout_microburst_turnover_label_prompt.md`, sha256 `dd10d919e197050f3b7a8ba21f0e929e4e9727dd9986ba06de11b455c51047b3`.
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f74_stage_closeout_microburst_turnover_label/clean_output.md`, sha256 `f9b97d513fc7a9a06a6c39b92acad8f0f68a98beb49e27f26739785b9c5a4864`.
- advice_classification(조언 분류): `accepted(수용)`.
- local_verification(로컬 검증): F74B/F74C summaries(요약), F74E receipt/parity(영수증/동등성), and Grok metadata(메타데이터)를 `io_path`로 확인했다.

## Judgment(판정)

F74는 preserved clue(보존 단서)와 negative memory(부정 기억)만 남기고 닫는다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

`frontier75A_stage_open_upstream_mechanism_rotation_after_f74_microburst_negative_memory_v1`.

Next frontier(다음 전선)는 microburst turnover label(마이크로버스트 회전 라벨)의 threshold/clean-label repair loop(임계값/클린 라벨 수리 반복)가 아니라 order-flow/volatility-compression/session-liquidity(오더플로/변동성 압축/세션 유동성) 같은 upstream mechanism(상류 메커니즘) 전환으로 열어야 한다.

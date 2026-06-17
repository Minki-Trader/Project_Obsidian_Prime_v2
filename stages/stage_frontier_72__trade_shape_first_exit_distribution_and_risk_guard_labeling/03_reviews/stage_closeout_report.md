# Frontier72 Stage Closeout(F72 전선 단계 마감)

Updated(갱신): 2026-06-17T01:36:11Z

## Closeout Label(마감 라벨)

`closed_preserved_clue_negative_memory_no_authority`

Claim boundary(주장 경계): `preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.

## Hypothesis(가설)

trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 개선하는 seed surface(씨앗 표면)를 만들 수 있는가.

Effect(효과): label/target(라벨/목표), feature set(피처 묶음), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직)을 한 lifecycle(생명주기) 안에서 바꿔보고 MT5 Runtime Probe(MT5 런타임 탐침)까지 물질화했다.

## Test Period(테스트 기간)

- runtime validation(런타임 검증): `2025-01-02..2025-10-01`.
- runtime OOS(런타임 표본외): `2025-10-01..2026-04-14`.

## Proxy Expectation(프록시 예상)

exit/risk label construction(청산/위험 라벨 구성)이 proxy scout clue(프록시 탐색 단서)를 만들고 MT5 lifecycle repair(생명주기 수리) 뒤에도 density/PF/DD(밀도/수익 팩터/손실폭)가 같이 유지될 것으로 기대했다.

## Proxy KPI(프록시 핵심 성과 지표)

- F72B candidates(후보): `704`, scout clue(탐색 단서) `3`, meaningful(의미 후보) `0`.
- F72B best scout OOS(탐색 단서 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `1942.5636/1.2108/12.0045%/1.8154`.
- F72C candidates(후보): `1728`, scout clue(탐색 단서) `16`, meaningful(의미 후보) `0`.
- F72C best scout OOS(탐색 단서 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `4933.5061/1.3403/12.8125%/3.0103`.
- F72E lifecycle repair candidates(생명주기 수리 후보): `240`, repair probe worthy(수리 탐침 가치) `1`, meaningful(의미 후보) `0`.
- F72E selected clue(선택 단서): `f72e_0200` `short_h24_sl0.9_tp1.8` `mfe_mae_gap_040`; lifecycle OOS(생명주기 표본외) net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) `799.9634/1.0624/10.4275%/2.6823/515`.

## Runtime Probe KPI(런타임 탐침 핵심 성과 지표)

- signal count parity(신호 수 동등성): F72D validation/OOS diff(검증/표본외 차이) `0/0`, F72F `0/0`.
- feature readiness parity(피처 준비 동등성): F72D validation/OOS diff(검증/표본외 차이) `0/0`, F72F `0/0`.
- probability parity(확률 동등성): F72F pass rows(통과 행) `3/3`, max abs diff(최대 절대 차이) `0.00000019`.
- lifecycle count alignment(생명주기 개수 정렬): F72D OOS expected signals/runtime trades(예상 신호/런타임 거래) `730->227`, F72F OOS expected selected trades/runtime trades(예상 선택 거래/런타임 거래) `515->483`.
- proxy/runtime gap cause(프록시/런타임 간극 원인): F72D에서 겹친 신호 집계와 MT5 단일 포지션 생명주기 간극을 확인했고, F72F에서 expected selected trades(예상 선택 거래)와 runtime trades(런타임 거래)의 개수 간극은 줄었지만 PF/DD/net(수익 팩터/손실폭/순수익)은 runtime_economics_gap_after_signal_and_feature_parity(신호/피처 동등성 이후 런타임 경제성 간극)로 남았다.

### F72D Before Lifecycle Repair(F72D 생명주기 수리 전)

| split(분할) | period(기간) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades(거래 수) | trades/day(일 거래 수) | expected signals/selected trades(예상 신호/선택 거래) | runtime trades(런타임 거래) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `2025-01-02..2025-10-01` | `70.35` | `1.1` | `17.18%` | `250` | `0.9191` | `680` | `250` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |
| `oos` | `2025-10-01..2026-04-14` | `45.04` | `1.06` | `18.1%` | `227` | `1.1641` | `730` | `227` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |

| test period(테스트 기간) | split/view(분할/보기) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trade count(거래 수) | trades/day(일 거래 수) | win rate(승률) | average win(평균 이익) | average loss(평균 손실) | payoff ratio(손익비) | expectancy(기대값) | recovery factor(회복 계수) | time under water(회복 전 체류 시간) | max consecutive loss(최대 연속 손실) | long/short(롱/숏) | proxy/runtime gap(프록시/런타임 간극) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| `2025-01-02..2025-10-01` | `F72F lifecycle repair runtime probe(F72F 생명주기 수리 런타임 탐침) validation Tier A separate(Tier A 분리)` | `93.14` | `1414.36` | `-1321.22` | `1.07` | `14.94%` | `582` | `2.1397` | `35.05%` | `6.9331` | `-3.4953` | `1.9836` | `0.16` | `0.99` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `long=0; short=582` | `runtime_economics_gap_after_signal_and_feature_parity; proxy net/PF/tpd/DD=1145.3354/1.0874/2.2426/9.7532%` |
| `2025-10-01..2026-04-14` | `F72F lifecycle repair runtime probe(F72F 생명주기 수리 런타임 탐침) oos Tier A separate(Tier A 분리)` | `66.47` | `1330.68` | `-1264.21` | `1.05` | `18.6%` | `483` | `2.4769` | `35.61%` | `7.7365` | `-4.065` | `1.9032` | `0.14` | `0.65` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `not_available_from_current_strategy_report_parse(현재 전략 보고서 파싱에서 없음)` | `long=0; short=483` | `runtime_economics_gap_after_signal_and_feature_parity; proxy net/PF/tpd/DD=799.9634/1.0624/2.6823/10.4275%` |

## Final Target Distance(최종 목표 거리)

- F72F OOS runtime(표본외 런타임): net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) `66.47/1.05/18.6%/2.4769/483`.
- final hard gates(최종 강제 게이트)는 final completion review(최종 완성 검토) 전용이지만, F72F는 trades/day 5-10(일거래 5-10), PF 2-3+(수익 팩터 2-3 이상), DD <10%(손실폭 10% 미만)를 동시에 만족하지 못했다.

## WFO/Stress(워크포워드/스트레스)

- status(상태): `not_run_out_of_scope_by_claim_after_runtime_negative_closeout(WFO/스트레스는 런타임 부정 마감 뒤 주장 범위 밖으로 미실행)`.
- reason(사유): F72F mandatory MT5 repair(필수 MT5 수리)가 PF 1.07/1.05, DD 14.94%/18.60%, trades/day 2.14/2.48에 머물러 completion candidate(완성 후보)가 아니며, 추가 WFO/stress(워크포워드/스트레스)는 약한 표면을 강화 검증하는 일이 된다.

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `materialized_proxy_and_runtime(프록시와 런타임 물질화)`.
- Tier B separate(Tier B 분리): `missing_required_in_f72(필수 누락으로 기록)`.
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_without_tier_b(Tier B 부재로 주장 범위 밖)`.

## Preserved Clue(보존 단서)

- F72F lifecycle repair(생명주기 수리)는 expected selected trades vs runtime trades(예상 선택 거래 대 런타임 거래)를 validation 610->582, OOS 515->483으로 좁혔다.
- ONNX probability/signal parity(온엑스 확률/신호 동등성)와 feature readiness parity(피처 준비 동등성)는 F72F에서 모두 diff 0으로 유지됐다.
- all-short execution shape(숏 전용 실행 형태)는 F72E source candidate `short_h24_sl0.9_tp1.8`에서 온 의도된 execution-shape clue(실행 형태 단서)다.

## Negative Memory(부정 기억)

- F72B/F72C/F72E 모두 meaningful candidate(의미 후보) 0으로 끝났다.
- F72F lifecycle repair after parity(동등성 후 생명주기 수리)에도 OOS runtime(표본외 런타임)은 net 66.47, PF 1.05, DD 18.60%, trades/day 2.4769에 그쳤다.
- 같은 F72 trade-shape-first label/feature/lifecycle surface(거래 형태 우선 라벨/피처/생명주기 표면)를 새 상류 질문 없이 반복하지 않는다.

## Grok Closeout Review(그록 마감 검토)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f72g_stage_closeout_trade_shape_lifecycle_gap`.
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f72g_stage_closeout_trade_shape_lifecycle_gap/prompts/f72g_stage_closeout_trade_shape_lifecycle_gap_prompt.md`, sha256(해시) `a2b461000c790a593a805a884ead29ec575e1c67b521dc909df67df454c77376`.
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f72g_stage_closeout_trade_shape_lifecycle_gap/clean_output.md`, sha256(해시) `6c60cac22c705146731e42366a04e93011332e3512c69f39dd5e5272a1253390`.
- classification(분류): `accepted_with_local_verification(로컬 검증 후 수용)`.
- accepted(수용): close F72 as preserved clue + negative memory(F72를 보존 단서 + 부정 기억으로 마감), no more F72 internal repair without new axis(새 축 없는 F72 내부 수리 없음).
- rejected(거절): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 주장과 mandatory pre-closeout repair(필수 마감 전 수리).
- local verification(로컬 검증): all-short execution(숏 전용 실행)은 source candidate(원천 후보) `short_h24_sl0.9_tp1.8`에서 온 의도된 단서이며, F72F receipt/parity(영수증/동등성)는 스냅샷과 일치했다.

## Next Action(다음 행동)

`frontier73A_stage_open_new_hypothesis_after_f72_trade_shape_negative_memory_v1`

Effect(효과): F72의 lifecycle/parity clue(생명주기/동등성 단서)는 보존하고, 같은 trade-shape-first surface(거래 형태 우선 표면)를 반복하지 않고 새 frontier hypothesis(전선 가설)로 넘어간다.

# F66 Stage Closeout(F66 단계 마감)

Updated(갱신): `2026-06-16T12:15:14Z`

- stage_id(단계 ID): `stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64`
- closeout_label(마감 라벨): `preserved_clue_negative_memory(보존 단서 + 부정 기억)`
- judgment(판정): `closed_preserved_clue_signal_parity_negative_memory_runtime_economics_gap_no_authority(마감, 신호 동등성 보존 단서, 런타임 경제성 간극 부정 기억, 권위 없음)`
- test period(테스트 기간): F02-F64 frontier audit frame(F02-F64 전선 감사 범위); MT5 materialized validation_is/OOS split windows(MT5 물질화 검증 내부/OOS 분할 창). Exact calendar crosswalk(정확 달력 대조)은 F67A DD basis crosswalk(F67A 손실폭 기준 대조)로 넘긴다.
- split/view(분할/보기): overall 64 split rows(전체 64분할 행), validation_is 32, OOS 32.
- next_stage(다음 단계): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- next_run(다음 실행): `frontier67A_stage_open_dd_basis_crosswalk_v1`

## Action And Effect(행동과 효과)

Action(행동): F11,F15,F18-F49 proxy signal(프록시 신호)을 MT5 Strategy Tester(MT5 전략 테스터)에서 64 split runs(분할 실행)로 물질화하고, proxy/runtime gap(프록시/런타임 간극)을 F02-F64 audit frame(감사 범위)로 정리했다.

Effect(효과): L1 feature readiness parity(피처 준비 동등성)와 L2 signal count parity(신호 수 동등성)는 보존 단서로 남기고, count parity(개수 동등성)가 PF/DD/trade density(수익 팩터/손실폭/거래 빈도)로 전이되지 않는다는 negative memory(부정 기억)를 고정했다.

## Scope Table(범위 표)

| item(항목) | value(값) | boundary(경계) |
|---|---:|---|
| audit frame stages(감사 범위 단계) | F02-F64, 63 stages(63단계) | reference, not inheritance(참조이지 상속 아님) |
| original runtime KPI stages(기존 런타임 KPI 단계) | 29 | F66 전 이미 존재 |
| newly materialized stages(새로 물질화한 단계) | 32 | F11,F15,F18-F25,F27-F33,F35-F49 |
| logic-zero stages(로직상 신호 0 단계) | 2 | F26/F34, no MT5 attempt(MT5 시도 없음) |
| MT5 split rows(엠티5 분할 행) | 64 | 32 stages x validation_is/OOS |
| tester/runtime/report completed(테스터/런타임/보고서 완료) | 64/64 | completed/completed/completed |
| feature_ready_diff(피처 준비 차이) | 0/64 nonzero | exact readiness parity(준비 동등성 정확) |
| signal_count_diff(신호 수 차이) | 0/64 nonzero | exact signal parity(신호 동등성 정확) |
| actual runtime KPI after F66C(F66C 후 실제 런타임 KPI) | 61/63 stages | F26/F34 logic-zero excluded(로직상 0 제외) |

## Four-Axis Closeout Table(네 축 마감 표)

| axis(축) | observed(관찰) | read(판독) |
|---|---|---|
| trades/day 5-10(일 거래 5-10) | 0/64 split rows(분할 행) reached 5-10; max 4.1949 | failed objective axis(목표 축 실패), not final gate(최종 게이트 아님) |
| PF 2-3+(수익 팩터 2-3 이상) | PF>=2 in 1/64 split rows only | failed objective axis(목표 축 실패); F11 OOS is outlier(이상치) with DD 10.87 |
| DD <10%(손실폭 10% 미만) | DD>10 in 60/64 split rows; max stage DD>10 in 31/32 executable stages | failed objective axis(목표 축 실패) |
| smooth equity(매끄러운 자산 곡선) | not measured as normalized equity curve(정규화 자산 곡선 미측정); DD distribution is rough(손실폭 분포 거침) | not_closed(미폐쇄), no smoothness claim(매끄러움 주장 없음) |

## Aggregate Runtime KPI(집계 런타임 KPI)

These are split-level runtime observations(분할 단위 런타임 관찰) from `frontier66_proxy_runtime_gap_by_split_review.csv`. Net profit(순수익)은 split row sum(분할 행 합계)으로만 읽고 portfolio equity(포트폴리오 자산곡선)로 읽지 않는다.

| view(보기) | rows(행) | net profit sum(순수익 합계) | PF min/p25/med/p75/max(수익 팩터) | DD min/p25/med/p75/max(손실폭) | trades med/max(거래 중앙/최대) | trades/day med/max(일 거래 중앙/최대) |
|---|---:|---:|---|---|---|---|
| overall(전체) | 64 | 2793.80 | 0.72 / 0.9775 / 1.05 / 1.135 / 2.18 | 3.53 / 14.0025 / 21.815 / 35.0725 / 60.81 | 318 / 1091 | 1.3880 / 4.1949 |
| validation_is(검증 내부) | 32 | 1519.46 | 0.72 / 0.98 / 1.035 / 1.12 / 1.47 | 5.78 / 15.2175 / 23.51 / 35.545 / 59.46 | 367.5 / 1091 | 1.3511 / 4.0110 |
| OOS(표본외) | 32 | 1274.34 | 0.77 / 0.9475 / 1.075 / 1.15 / 2.18 | 3.53 / 11.425 / 18.65 / 33.985 / 60.81 | 273.5 / 818 | 1.4026 / 4.1949 |

| count metric(개수 지표) | overall(전체) | validation_is(검증 내부) | OOS(표본외) |
|---|---:|---:|---:|
| PF>=1 | 43/64 | 21/32 | 22/32 |
| PF>=2 | 1/64 | 0/32 | 1/32 |
| DD>10% | 60/64 | 30/32 | 30/32 |
| DD>20% | 35/64 | 19/32 | 16/32 |
| DD>50% | 5/64 | 2/32 | 3/32 |
| trades<20(거래 20 미만) | 2/64 | 1/32 | 1/32 |
| trades/day 5-10(일 거래 5-10) | 0/64 | 0/32 | 0/32 |

Missing KPI(누락 KPI): gross profit(총이익), gross loss(총손실), win rate(승률), average win/loss(평균 이익/손실), payoff ratio(손익비), expectancy(기대값), recovery factor(회복 계수), time under water(회복 전 체류 시간), max consecutive loss(최대 연속 손실), long/short breakdown(롱/숏 분해)는 normalized closeout table(정규화 마감 표)에 없다. These are recorded as missing_kpi(누락 KPI), not ignored(무시 아님).

## Best/Worst Illustration(최고/최악 예시)

| row(행) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | net profit(순수익) | read(판독) |
|---|---:|---:|---:|---:|---:|---|
| F11 OOS | 2.18 | 10.87 | 61 | 0.3128 | 282.71 | exploratory outlier only(탐색적 이상치 한정); DD still >10 |
| F35 OOS | 1.66 | 3.53 | 8 | 0.0410 | 11.57 | too thin(너무 얇음), not candidate(후보 아님) |
| F23 OOS | 0.81 | 60.81 | 239 | 1.2256 | -203.14 | negative control(부정 대조): exact signal parity did not save runtime DD |
| F11 validation_is | 0.72 | 59.46 | 92 | 0.3382 | -203.19 | negative control(부정 대조): same stage has bad validation drawdown(검증 손실폭) |

## Proxy/Runtime Gap Read(프록시/런타임 간극 판독)

- signal count parity(신호 수 동등성): expected signals(예상 신호) `70032`, MT5 signals(MT5 신호) `70032`, diff(차이) `0`.
- feature readiness parity(피처 준비 동등성): feature_ready_diff(피처 준비 차이) `0` for 64/64.
- signal to trade conversion(신호->거래 전환): runtime trades(런타임 거래) `24284`, signal_to_trade_ratio median(중앙값) `0.3248`.
- open cause(열린 원인): residual PF/DD gap(잔여 수익 팩터/손실폭 간극)은 L3 order intent(주문 의도), L4 fill/cost model(체결/비용 모델), L5 KPI measurement basis(KPI 측정 기준) mismatch(불일치)와 consistent(일관)하지만 ranked root cause(순위 근본 원인)는 not_claimed(주장 없음).

## F65 Handoff Supersession(F65 인계 문구 대체)

F65 closeout report(마감 보고서)는 next stage(다음 단계)를 `stage_frontier_66__runtime_unit_aligned_exit_economics_pf_source_after_semantics_gap`로 적었다. Current truth(현재 진실)는 `docs/workspace/workspace_state.yaml`, F66 `stage_brief.md`, and F66 selection_status(선택 상태)가 가리키는 `stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64`다. F65 wording(F65 문구)은 superseded handoff wording(대체된 인계 문구)로 보존하고 inheritance(상속)하지 않는다.

## Preserved Clue And Negative Memory(보존 단서와 부정 기억)

- preserved clue(보존 단서): proxy signal materialization(프록시 신호 물질화) can reach exact L1/L2 handoff parity(정확한 1/2계층 인계 동등성) in MT5 for heterogeneous F11,F15,F18-F49 signal surfaces(이질 신호 표면).
- negative memory(부정 기억): exact count parity(정확한 개수 동등성) does not imply PnL parity(손익 동등성), low DD(낮은 손실폭), or target trade density(목표 거래 빈도).
- do_not_repeat(반복 금지): do not promote proxy signal count parity(프록시 신호 개수 동등성)를 runtime authority(런타임 권위)나 completion candidate(완성 후보)처럼 말하지 않는다.

## Next Action(다음 행동)

Open F67 as `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`.

F67 sequence(순서):

1. F67A DD basis crosswalk(손실폭 기준 대조): align proxy DD vs runtime DD basis(프록시/런타임 손실폭 기준).
2. F67B config parity depth pilot(설정 동등성 깊이 파일럿): spread/commission/slippage/modeling/deposit/leverage(스프레드/수수료/슬리피지/모델링/예치금/레버리지) small split set(소규모 분할 묶음) 대조.
3. F67C runtime-native order intent economics(런타임 기반 주문 의도 경제성): count parity(개수 동등성)와 PnL parity(손익 동등성)의 분리를 설명한다.

## Boundary(경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.

# F77A Stage-Open Grok Prompt(F77A 단계 개방 Grok 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Open F77 as `runtime_lifecycle_label_density_rebuild(런타임 생명주기 라벨/밀도 재구성)`.
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

F77 should not merely tune F76. It changes the object being learned: from independent future-return signals(독립 미래수익률 신호) to runtime lifecycle event outcomes(런타임 생명주기 이벤트 결과).

## Current State(현재 상태)

- prior stage(이전 단계): F76 closed as `preserved_clue_negative_memory`.
- F76 repair counts(F76 수리 카운트): candidates=5120, meaningful=0, density=0, near=0.
- dataset(데이터셋): rows=46650, split_counts={'train': 29222, 'validation': 9844, 'oos': 7584}, feature_count=58.
- raw bars(원천 봉): rows=261345, header=['time_open_unix', 'time_close_unix', 'contract_symbol', 'broker_symbol', 'timeframe', 'price_basis', 'open', 'high', 'low', 'close', 'tick_volume', 'spread_points', 'real_volume', 'time_basis', 'timezone_status'].
- retrospective due status(회고 도래 상태): not_due_after_f76_closeout_1_of_5.

## F76 Runtime Closeout Snapshot(F76 런타임 마감 스냅샷)

- validation: period=2025-01-02..2025-10-01, net/PF/DD/tpd/trades=152.99/2.08/6.6/0.18382352941176472/50, gap=proxy_net=1760.31;runtime_net=152.99;proxy_pf=1.59485;runtime_pf=2.08;proxy_dd=6.44469;runtime_dd=6.6;proxy_tpd=1.06011;runtime_tpd=0.183824
- oos: period=2025-10-01..2026-04-14, net/PF/DD/tpd/trades=66.09/1.47/10.04/0.19487179487179487/38, gap=proxy_net=1471.79;runtime_net=66.09;proxy_pf=1.68934;runtime_pf=1.47;proxy_dd=7.89168;runtime_dd=10.04;proxy_tpd=1.17557;runtime_tpd=0.194872

## F77 Axis Contract(F77 축 계약)

| axis(축) | action(행동) | effect(효과) | broad_sweep(넓은 탐색) |
|---|---|---|---|
| feature_set(피처 묶음) | drop/replace/recombine price-action, trend, volatility, session, and index-proxy families(가격행동/추세/변동성/세션/지수 프록시 계열을 빼기/교체/재조합) | checks whether F76 source clue survives after lifecycle labels(생명주기 라벨 이후에도 F76 원천 단서가 남는지 확인) | all58, compact price/trend, volatility+session, mega-cap removed, raw-price-only proxy |
| label_target(라벨/목표) | replace independent future return with path outcome labels(독립 미래수익률을 경로 결과 라벨로 교체) | models what a runtime trade can actually earn before single-position compression(단일 포지션 압축 전에 런타임 거래가 실제로 벌 수 있는 것을 학습) | first-hit TP/SL, MFE/MAE quality, drawdown hazard, time-to-exit, lifecycle utility |
| model_family(모델 계열) | rotate simple and nonlinear families(단순/비선형 모델 계열을 회전) | separates label value from model bias(라벨 가치와 모델 편향을 분리) | logistic/linear, HistGradientBoosting, ExtraTrees, small MLP if local dependency exists |
| trade_shape(거래 형태) | simulate event entry, first-touch exit, fixed hold, side split, and single-position occupancy(이벤트 진입/최초접촉 청산/고정 보유/방향 분리/단일 포지션 점유를 시뮬레이션) | turns proxy density into lifecycle density instead of independent signal count(프록시 밀도를 독립 신호 수가 아니라 생명주기 밀도로 바꿈) | long, short, both, max_hold 6/12/18/24, first-touch exits |
| risk_logic(위험 로직) | make SL/TP, MAE cutoff, DD guard, and daily loss guard part of target/proxy(손절/익절/MAE 컷/DD 보호/일 손실 보호를 목표와 프록시에 포함) | filters drawdown before MT5 rather than explaining it after MT5(MT5 뒤 해명이 아니라 MT5 전 손실폭 필터) | TP/SL grid, MAE gate, drawdown hazard penalty, trade cooldown only after lifecycle scoring |
| regime_session_split(장세/세션 분할) | test where lifecycle utility exists by session and volatility/trend regime(세션과 변동성/추세 장세별 생명주기 효용 위치를 시험) | keeps broad topic rotation while avoiding one tiny slice pretending to be the whole idea(넓은 주제 전환을 유지하면서 한 작은 구간이 전체 아이디어처럼 보이는 것을 막음) | cash open/mid/late, high/low volatility, trend/chop, previous-session carry |

## Gates(게이트)

- scout clue(탐색 단서): validation and OOS net>0 or PF>=1.15, DD<=15%, lifecycle trades/day>=1.0, trade_count>=60 per split, and fragility recorded
- meaningful signal(의미 신호): validation+OOS net>0, PF>=1.30, DD<=10%, lifecycle trades/day>=2.0, trade_count>=80 per split, and single-position compression recorded
- final-like reference only(최종 유사 참조 전용): reference only: PF>=2.0, DD<=10%, 5<=trades/day<=10, smooth equity proxy true

## Runtime Rule(런타임 규칙)

Every frontier stage(전선 단계) requires MT5 Runtime Probe(MT5 런타임 탐침) unless there is true zero signal logic impossibility(진짜 영 신호 로직 불가능) or runtime bridge impossibility(런타임 연결 불가능).
If F77B finds meaningful signal(의미 신호), Codex must run pre-MT5 Grok review(MT5 전 Grok 검토) and materialize MT5 Runtime Probe(MT5 런타임 탐침).
If F77B finds only weak nonzero signal(약한 비영 신호), Codex must run bounded negative-control MT5 Runtime Probe(제한 부정 대조 MT5 탐침) before closeout unless logic impossibility is recorded.

## Review Question(검토 질문)

Return one classification(분류) at top:
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Then answer:
1. Is F77 sufficiently novel versus F76?
2. Which axis is most likely to reduce proxy/runtime gap(프록시/런타임 간극)?
3. What must Codex locally verify before F77B?
4. What do-not-repeat(반복 금지) rule should be recorded?
5. Any forbidden claim risk(금지 주장 위험)?

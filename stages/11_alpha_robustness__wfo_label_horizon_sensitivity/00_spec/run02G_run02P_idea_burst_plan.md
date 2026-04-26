# RUN02G-RUN02P Idea Burst Plan

## 의도(Intent, 의도)

RUN02G~RUN02P(실행 02G~02P)는 RUN02C/RUN02E(실행 02C/02E)의 약한 salvage value(회수 가치)를 바로 세부 탐색(micro search, 세부 탐색)하지 않고, LightGBM(`LightGBM`, 라이트GBM) 신호가 어떤 context(문맥)와 direction(방향)에서 덜 무너지는지 10개 아이디어로 넓게 흔든다.

효과(effect, 효과): RUN01(실행 01)의 threshold/hold/slice(임계값/보유/구간) 근처만 반복하지 않고, pullback(되돌림), trend(추세), low volatility(저변동성), range compression(횡보 압축), squeeze breakout(압축 돌파), vortex direction(보텍스 방향)을 한 묶음에서 비교한다.

## 실행 계획(Plan, 계획)

| run(실행) | idea_id(아이디어 ID) | axis(축) | allowed side(허용 방향) | context gate(문맥 제한) | evidence boundary(근거 경계) |
|---|---|---|---|---|---|
| RUN02G(실행 02G) | `IDEA-ST11-LGBM-LONG-PULLBACK` | long pullback(롱 되돌림) | long(롱) | `rsi14_lte45_bbpos_lte45` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02H(실행 02H) | `IDEA-ST11-LGBM-BULL-TREND-LONG` | bull trend long(상승 추세 롱) | long(롱) | `adx14_gte20_di_spread_gt0` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02I(실행 02I) | `IDEA-ST11-LGBM-LOW-VOL-EXTREME-CONFIDENCE` | low-vol extreme confidence(저변동성 극단 확신) | both(양방향) | `hvol5over20_lte90_atr_lte115` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02J(실행 02J) | `IDEA-ST11-LGBM-BALANCED-MIDBAND` | balanced mid-band(균형 중간대) | both(양방향) | `rsi14_between45_60_bbpos_between35_75` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02K(실행 02K) | `IDEA-ST11-LGBM-QUIET-RETURN-ZSCORE` | quiet z-score(조용한 수익률 z점수) | both(양방향) | `return_zscore_abs_lte70` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02L(실행 02L) | `IDEA-ST11-LGBM-RANGE-COMPRESSION` | range compression(횡보 압축) | both(양방향) | `di_spread_abs_lte8_adx_lte25` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02M(실행 02M) | `IDEA-ST11-LGBM-HIGH-VOL-MOMENTUM-ALIGN` | high-vol momentum(고변동성 모멘텀) | both(양방향) | `atr_ratio_gte115_momentum_align` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02N(실행 02N) | `IDEA-ST11-LGBM-SQUEEZE-BREAKOUT` | squeeze breakout(압축 돌파) | both(양방향) | `bb_squeeze_true` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02O(실행 02O) | `IDEA-ST11-LGBM-BULL-VORTEX-LONG` | bull vortex long(상승 보텍스 롱) | long(롱) | `vortex_positive_rsi50_gte50` | `runtime_probe_only(런타임 탐침 전용)` |
| RUN02P(실행 02P) | `IDEA-ST11-LGBM-BEAR-VORTEX-SHORT` | bear vortex short(하락 보텍스 숏) | short(숏) | `vortex_negative_rsi50_lte50` | `runtime_probe_only(런타임 탐침 전용)` |

## 탐색 규율(Exploration Discipline, 탐색 규율)

- legacy_relation(과거 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A + Tier B mixed(Tier A + Tier B 혼합)`
- broad_sweep(넓은 탐색): direction/context/confidence(방향/문맥/확신) 구조를 10개로 분리한다.
- extreme_sweep(극단 탐색): single-side(단방향) 실행은 반대 방향 threshold(임계값)를 `1.0`으로 막고, confidence(확신) 실행은 높은 quantile(분위수)와 margin(마진)을 쓴다.
- micro_search_gate(세부 탐색 관문): validation/OOS(검증/표본외)가 동시에 RUN02A/RUN02B(실행 02A/02B)의 손실 구조를 멈추는 아이디어만 다음 세부 탐색 후보로 둔다.
- wfo_plan(WFO 계획): 이번 묶음은 explicit single-window runtime_probe exception(명시적 단일 구간 런타임 탐침 예외)이다. WFO(`walk-forward optimization`, 워크포워드 최적화)는 살아남은 축이 있을 때만 뒤에서 한다.
- failure_memory(실패 기억): 실패는 negative result(부정 결과) 또는 weak inconclusive(약한 불충분)로 남기고, 같은 gate(제한 조건)를 반복하지 않는다.

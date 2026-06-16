# F68 Stage Closeout Report(F68 단계 마감 보고서)

Stage(단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`
Closeout run(마감 실행): `frontier68_closeout_preserved_clue_negative_memory_v1`
Updated(갱신): 2026-06-16T19:31:46Z

## Hypothesis(가설)

runtime_native_lifecycle_cost_dd_proxy_can_reduce_mt5_economics_gap(런타임 기반 생명주기/비용/손실폭 프록시가 MT5 경제성 간극을 줄일 수 있는가)

## Closeout Label(마감 라벨)

`preserved_clue_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음)`

## Mandatory KPI(필수 핵심 성과 지표)

| source/view(원천/보기) | period(기간) | split(분할) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래 수) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | long/short(롱/숏) | parity gap(동등성 간극) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| F68D density axis runtime probe(F68D 밀도 축 런타임 탐침) | `2025-10-01..2026-04-14` | `oos` | `103.48` | `2655.46` | `-2551.98` | `1.04` | `26.84` | `1649` | `8.45641` | `50.52` | `3.187827` | `-3.127426` | `1.019313` | `0.06` | `0.64` | `895/754` | `signal=0;feature=0` |
| F68F near-four-axis runtime repair probe(F68F 네 축 근접 런타임 수리 탐침) | `2025-01-02..2025-10-01` | `validation` | `8.91` | `1701.2` | `-1692.29` | `1.01` | `25.06` | `1081` | `3.974265` | `49.21` | `3.197744` | `-3.082495` | `1.037388` | `0.01` | `0.05` | `517/564` | `signal=0;feature=0` |
| F68F near-four-axis runtime repair probe(F68F 네 축 근접 런타임 수리 탐침) | `2025-10-01..2026-04-14` | `oos` | `241.18` | `1586.79` | `-1345.61` | `1.18` | `19.57` | `932` | `4.779487` | `50.86` | `3.347658` | `-2.938013` | `1.139429` | `0.26` | `1.9` | `499/433` | `signal=0;feature=0` |
| F68H capped ATR runtime repair probe(F68H 상한 평균진폭 런타임 수리 탐침) | `2025-01-02..2025-10-01` | `validation` | `-488.58` | `318.89` | `-807.47` | `0.39` | `97.72` | `4140` | `15.220588` | `21.96` | `0.350814` | `-0.249913` | `1.403743` | `-0.12` | `-1` | `1934/2206` | `signal=0;feature=0` |
| F68H capped ATR runtime repair probe(F68H 상한 평균진폭 런타임 수리 탐침) | `2025-10-01..2026-04-14` | `oos` | `-302.33` | `458.84` | `-761.17` | `0.6` | `60.51` | `4759` | `24.405128` | `30.49` | `0.316223` | `-0.2301` | `1.374288` | `-0.06` | `-1` | `2633/2126` | `signal=0;feature=0` |
| F68J unit-corrected ATR runtime repair probe(F68J 단위 보정 평균진폭 런타임 수리 탐침) | `2025-01-02..2025-10-01` | `validation` | `-141.58` | `2226.38` | `-2367.96` | `0.94` | `38.55` | `1554` | `5.713235` | `45.62` | `3.140169` | `-2.80232` | `1.120561` | `-0.09` | `-0.63` | `650/904` | `signal=0;feature=0` |
| F68J unit-corrected ATR runtime repair probe(F68J 단위 보정 평균진폭 런타임 수리 탐침) | `2025-10-01..2026-04-14` | `oos` | `68.24` | `2001.8` | `-1933.56` | `1.04` | `13.76` | `1305` | `6.692308` | `48.2` | `3.182512` | `-2.860296` | `1.112651` | `0.05` | `0.78` | `615/690` | `signal=0;feature=0` |

- time under water(회복 전 체류 시간): `not_available_from_mt5_receipt(테스터 영수증에 없음)`.
- max consecutive loss(최대 연속 손실): `not_available_from_mt5_receipt(테스터 영수증에 없음)`.

## Preserved Clues(보존 단서)

- F68F ONNX/feature handoff(F68F 온엑스/피처 인계)는 MT5에서 signal/feature parity(신호/피처 동등성) 0/0을 유지했다.
- F68J unit-corrected ATR telemetry(F68J 단위 보정 평균진폭 기록)는 세 변형을 실제로 구분했고 F68H 180/260 cap signature(상한 서명)와 맞지 않았다.
- F68J wide ATR OOS(F68J 넓은 평균진폭 표본외)는 DD(손실폭)를 F68F OOS 19.57%에서 13.76%로 낮추고 trades/day(일 거래 수)를 6.69로 올렸다.

## Negative Memory(부정 기억)

- lifecycle/cost/DD proxy plus same F68F ONNX plus risk-only repair(생명주기/비용/손실폭 프록시 + 동일 F68F 온엑스 + 위험 로직만 수리)는 네 축을 동시에 닫지 못했다.
- F52-style capped ATR repair(F52식 상한 평균진폭 수리)는 180/260 signature collapse(서명 붕괴)를 만들고 PF/DD(수익 팩터/손실폭)를 크게 악화했다.
- SL/TP/ATR width only(손절/익절/평균진폭 폭만 조정)는 PF source(수익 팩터 원천)가 아니었다.

## Proxy/Runtime Gap(프록시/런타임 간극)

F68 proxy(프록시)는 meaningful signal(의미 있는 신호)을 만들고 ONNX/feature parity(온엑스/피처 동등성)를 MT5로 옮겼지만, runtime economics(런타임 경제성), PF(수익 팩터), validation DD(검증 손실폭)는 동시에 닫히지 않았다.

## Next Action(다음 행동)

Open F69 with a major-axis rotation(F69를 주요 축 회전으로 연다): feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), or regime/session split(장세/세션 분할).

Next stage(다음 단계): `stage_frontier_69__axis_rotation_after_lifecycle_risk_only_negative_memory`
First run(첫 실행): `frontier69A_stage_open_axis_rotation_hypothesis_design_v1`

Claim boundary(주장 경계): `preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

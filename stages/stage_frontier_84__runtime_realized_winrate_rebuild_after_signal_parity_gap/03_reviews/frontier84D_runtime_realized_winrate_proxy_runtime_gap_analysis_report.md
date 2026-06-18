# F84D Runtime-Realized Winrate Proxy/Runtime Gap Analysis(F84D 런타임 실현 승률 프록시/런타임 간극 분석)

Updated(갱신): 2026-06-18T10:47:10Z

- run id(실행 ID): `frontier84D_runtime_realized_winrate_proxy_runtime_gap_analysis_v1`
- parent run(부모 실행): `frontier84C_mt5_runtime_realized_winrate_materialization_v1`
- target(대상): `f84b_00287` / `extra_trees_d7_l120`
- source best(원천 최선): `f84b_01151` / `histgbm_density_shallow`
- status(상태): `f84d_runtime_gap_attributed_negative_runtime_deal_economics_no_authority`
- judgment(판정): `signal_feature_onnx_parity_passed_runtime_winrate_pf_dd_failed_row_level_reconciliation_required_no_authority`
- actual sub-agent calls(실제 하위 에이전트 호출): `9 calls; roster 8/8`
- claim boundary(주장 경계): `gap_attribution_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Readout(판독)

Action(행동): F84B proxy(프록시) target(대상)과 F84C MT5 runtime(런타임) 결과를 split(구간)별로 비교했다.

Effect(효과): signal/feature/ONNX parity(신호/피처/온엑스 동등성)는 보존됐지만, MT5 deal economics(거래 경제성), win rate(승률), DD(손실폭)가 붕괴한 negative evidence(부정 근거)를 F84E row-level deal reconciliation(행 단위 거래 조정) 입력으로 고정한다.

| split(구간) | proxy net/PF/DD/TPD(프록시 순손익/수익 팩터/손실폭/일 거래 수) | MT5 net/PF/DD/TPD(MT5 순손익/수익 팩터/손실폭/일 거래 수) | win rate proxy->runtime(승률 프록시->런타임) | signal diff(신호 차이) | fill gap(체결 간극) |
|---|---:|---:|---:|---:|---:|
| validation(검증) | `341.6369/1.3779/4.5254/8.6347` | `-378.7600/0.7100/75.8900/8.5515` | `46.8376% -> 27.4300%` | `0` | `-14` |
| OOS(표본외) | `288.0970/1.4246/2.9310/9.3041` | `-133.5100/0.8600/29.2700/9.2359` | `45.7064% -> 30.8700%` | `0` | `-4` |

## Attribution(귀속)

Primary attribution(주 귀속): `runtime_deal_economics_winrate_dd_gap_after_signal_parity(신호 동등성 이후 런타임 거래 경제성/승률/손실폭 간극)`.

Not primary drivers(주 원인 아님): signal count mismatch(신호 수 불일치), feature readiness mismatch(피처 준비 불일치), ONNX handoff(온엑스 인계), material order fill gap(중대한 주문 체결 간극).

Preserved clue(보존 단서): `F84B target(대상)은 MT5 runtime(MT5 런타임)에서 final-like density(최종 조건에 가까운 밀도)를 보존했고 feature/signal/ONNX parity(피처/신호/온엑스 동등성)를 통과했다.`

Negative memory(부정 기억): `Runtime-realized winrate labels(런타임 실현 승률 라벨)는 actual MT5 win rate/drawdown(실제 MT5 승률/손실폭)을 보존하지 못했다. 이 long-only exportable branch(롱 전용 내보내기 가능 가지)에서 threshold-only repair(임계값만 수리)는 피한다.`

Closeout KPI note(마감 핵심 성과 지표 참고): F84C runtime receipt(런타임 영수증)는 gross profit/loss(총이익/총손실), win rate(승률), avg win/loss(평균 이익/손실), payoff ratio(손익비), expectancy(기대값), recovery factor(회복 계수), long/short breakdown(롱/숏 분해)을 포함한다. Runtime time under water(런타임 회복 전 체류 시간)와 max consecutive loss(최대 연속 손실)는 F84C normalized receipt(정규화 영수증)에 없어 unavailable(미확보)로 둔다.

Next action(다음 행동): `frontier84E_runtime_realized_winrate_row_level_deal_reconciliation_v1`.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.

# F83C Proxy/Runtime Gap Analysis(F83C 프록시/런타임 간극 분석)

Updated(갱신): 2026-06-18T07:57:33Z

- run id(실행 ID): `frontier83C_proxy_runtime_gap_analysis_teacher_overlay_v1`
- parent run(부모 실행): `frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1`
- target(대상): `f83a_0019` / `decision_tree_d4_balanced`
- status(상태): `f83c_gap_attributed_runtime_parity_preserved_strategy_objective_gap_no_authority`
- judgment(판정): `runtime_parity_preserved_but_density_pf_two_sided_wfo_gaps_require_new_axis_repair_or_rotation_no_authority`
- claim boundary(주장 경계): `gap_attribution_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Readout(판독)

Action(행동): F83B MT5 runtime materialization(F83B MT5 런타임 물질화)을 F83A proxy KPI(F83A 프록시 핵심 성과 지표)와 split(구간)별로 비교했다.

Effect(효과): runtime mismatch(런타임 불일치)가 아니라 strategy objective gap(전략 목표 간극)을 다음 F83D 입력으로 고정한다.

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | runtime trades/day(런타임 일 거래) | density gap to 5/day(일 5회 간극) | PF gap to 2(수익 팩터 2 간극) | long/short(롱/숏) |
|---|---:|---:|---:|---:|---:|---:|
| validation(검증) | `79.9700/1.6433/1.7370` | `79.9700/1.6400/1.7600` | `0.9412` | `4.0588` | `0.3600` | `256/0` |
| OOS(표본외) | `24.0200/1.3315/2.0438` | `24.0200/1.3300/2.0600` | `0.7026` | `4.2974` | `0.6700` | `137/0` |

## Attribution(귀속)

Primary attribution(주 귀속): `strategy_objective_gap_after_runtime_parity(런타임 동등성 이후 전략 목표 간극)`.

Not primary drivers(주 원인 아님): signal count mismatch(신호 수 불일치), feature readiness mismatch(피처 준비 불일치), ONNX handoff(온엑스 인계), order fill(주문 체결).

Preserved clue(보존 단서): exportable ONNX teacher overlay(내보내기 가능 온엑스 교사 덧씌움)는 selected-entry runtime behavior(선택 진입 런타임 행동)를 거의 그대로 보존했다.

Negative memory(부정 기억): current long-only low-density branch(현재 롱 전용 저밀도 가지)는 final objective(최종 목표)에 멀다. threshold-only repair(임계값만 바꾸는 수리)는 금지한다.

Closeout KPI note(마감 핵심 지표 참고): F83B runtime receipt(F83B 런타임 영수증)는 gross profit/loss(총이익/총손실), win rate(승률), avg win/loss(평균 이익/손실), payoff ratio(손익비), expectancy(기대값), recovery factor(회복 계수), long/short breakdown(롱/숏 분해)을 포함한다. runtime time under water(런타임 회복 전 체류 시간)와 max consecutive loss(최대 연속 손실)는 F83B receipt(영수증)에 없어 proxy value(프록시 값)만 참고로 남긴다.

Next action(다음 행동): `frontier83D_two_sided_density_expansion_or_rotation_decision_v1`.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.

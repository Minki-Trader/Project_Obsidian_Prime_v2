# F81E Capped Repair Or Rotation Decision(F81E 상한 수리 또는 회전 결정)

Updated(갱신): 2026-06-18T04:17:22Z

- run id(실행 ID): `frontier81E_capped_repair_or_rotation_decision_v1`
- parent run(부모 실행): `frontier81D_proxy_runtime_gap_attribution_v1`
- runtime source(런타임 원천): `frontier81C_mt5_runtime_materialization_v1`
- target(대상): `f81b_01107` / `extra_trees_d6_l160`
- decision(결정): `capped_repair_selected`
- repair axis(수리 축): `deal_reconciled_runtime_label_preflight`
- repair cap(수리 상한): `one_repair_cycle_before_rotation`
- next run(다음 실행): `frontier81F_deal_reconciled_runtime_label_preflight_v1`
- claim boundary(주장 경계): `decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Decision(결정)

Action(행동): F81D proxy/runtime gap attribution(프록시/런타임 간극 귀속)과 F81C runtime receipt(런타임 영수증)를 비교해 capped repair(상한 수리) 또는 rotation(회전)을 선택했다.

Effect(효과): F81(전선81)을 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복으로 끌지 않고, deal-level PnL(거래별 손익)이라는 새 evidence axis(근거 축) 1회만 허용한다.

Decision(결정): `capped_repair_selected`. F81F(전선81F)는 deal-level entry/exit/PnL evidence(거래별 진입/청산/손익 근거)를 먼저 만들거나 회수한다. 가능하면 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축)로 이어가고, 불가능하면 F81 negative closeout(부정 마감) 또는 F82 rotation(F82 회전)으로 간다.

## KPI Boundary(KPI 경계)

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | trades/day(일 거래) | win rate(승률) | parity(동등성) |
|---|---:|---:|---:|---:|---|
| validation(검증) | `131.0659/1.4029/4.0842` | `-147.0200/0.6800/30.9800` | `2.5625` | `0.2410` | signal/feature diff 0(신호/피처 차이 0) |
| OOS(표본외) | `120.8997/1.3961/2.0510` | `-115.7100/0.7300/23.7200` | `3.4359` | `0.2537` | signal/feature diff 0(신호/피처 차이 0) |

## Evidence Gap(근거 간극)

- trade list available(거래 목록 있음): `False`
- deal PnL columns available(거래 손익 열 있음): `False`

- validation telemetry: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)
- validation summary: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)
- oos telemetry: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)
- oos summary: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)

## Reasons(근거)

- F81D showed exact signal/feature parity but runtime economics failed(F81D가 신호/피처 동등성은 맞고 런타임 경제성은 실패했음을 보임).
- Runtime win rate fell from proxy 41-43% to MT5 24-25%(런타임 승률이 프록시 41-43%에서 MT5 24-25%로 하락).
- Runtime DD expanded from proxy 2-4% to MT5 24-31%(런타임 손실폭이 프록시 2-4%에서 MT5 24-31%로 확대).
- F81C forensics has no deal-level trade list(F81C 포렌식에 거래별 목록이 없음).
- F81C telemetry has no deal-level entry/exit/PnL columns(F81C 텔레메트리에 거래별 진입/청산/손익 열이 없음).
- A deal-reconciled label is a new evidence axis, not threshold-only repetition(거래 손익 대조 라벨은 새 근거 축이지 임계값 반복이 아님).

## Repair Cap(수리 상한)

Allowed(허용): one deal-reconciled repair cycle(거래 손익 대조 수리 1회). F81F(전선81F)는 tester report/EA telemetry/narrow telemetry patch(테스터 보고서/EA 텔레메트리/좁은 텔레메트리 패치) 중 가장 좁은 충분 방법으로 deal-level evidence(거래별 근거)를 만든다.

Forbidden(금지):

- probability threshold only(확률 임계값만 변경)
- probability quantile only(확률 분위수만 변경)
- same candidate risk filter only(같은 후보 위험 필터만 변경)
- same one-sided branch rerun without deal PnL evidence(거래 손익 근거 없는 같은 단방향 가지 재실행)

Rotation condition(회전 조건): `If F81F cannot produce deal-level PnL evidence from tester report, EA telemetry, or a narrow telemetry patch(F81F가 테스터 보고서, EA 텔레메트리, 좁은 텔레메트리 패치에서 거래별 손익 근거를 만들 수 없으면), close F81 as negative memory and rotate(F81을 부정 기억으로 마감하고 회전).`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

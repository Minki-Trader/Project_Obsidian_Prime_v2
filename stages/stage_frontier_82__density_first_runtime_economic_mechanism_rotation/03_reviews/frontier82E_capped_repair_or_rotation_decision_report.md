# F82E Capped Repair Or Rotation Decision(F82E 상한 수리 또는 회전 결정)

Updated(갱신): 2026-06-18T06:10:42Z

- run id(실행 ID): `frontier82E_capped_repair_or_rotation_decision_v1`
- parent run(부모 실행): `frontier82D_proxy_runtime_gap_attribution_v1`
- runtime source(런타임 원천): `frontier82C_mt5_runtime_materialization_v1`
- target(대상): `f82b_07295` / `extra_trees_d7_l120`
- decision(결정): `capped_repair_selected`
- repair axis(수리 축): `deal_reconciled_runtime_label_preflight`
- repair cap(수리 상한): `one_repair_cycle_before_rotation`
- next run(다음 실행): `frontier82F_deal_reconciled_runtime_label_preflight_v1`
- rotation if blocked(차단 시 회전): `frontier82G_capped_repair_closeout_or_f83_rotation_decision_v1`
- claim boundary(주장 경계): `decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Decision(결정)

Action(행동): F82D proxy/runtime gap attribution(프록시/런타임 간극 귀속)과 F82C runtime receipt(런타임 영수증)를 비교해 capped repair(상한 수리) 또는 rotation(회전)을 선택했다.

Effect(효과): F82(전선82)를 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복으로 끌지 않고, deal-level PnL capture/reconciliation(거래별 손익 캡처/대조)이라는 새 evidence axis(근거 축) 1회만 허용한다.

Decision(결정): `capped_repair_selected`. F82F(전선82F)는 deal-level entry/exit/PnL evidence(거래별 진입/청산/손익 근거)를 먼저 만들거나 회수한다. 가능하면 MT5-realized label rebuild(MT5 실현 손익 라벨 재구축)로 이어가고, 불가능하면 F82G(전선82G)에서 이 repair path(수리 경로)를 negative memory(부정 기억)로 닫고 rotation(회전)한다.

## KPI Boundary(KPI 경계)

| split(구간) | proxy net/PF/DD(프록시 순손익/수익 팩터/손실폭) | MT5 net/PF/DD(MT5 순손익/수익 팩터/손실폭) | trades/day(일 거래) | win rate(승률) | parity(동등성) |
|---|---:|---:|---:|---:|---|
| validation(검증) | `234.9537/1.2529/3.9148` | `-278.9800/0.7800/57.0000` | `7.2169` | `0.3281` | signal/feature diff 0(신호/피처 차이 0) |
| OOS(표본외) | `190.9750/1.3121/2.4484` | `-55.2100/0.9300/20.3600` | `6.8615` | `0.3677` | signal/feature diff 0(신호/피처 차이 0) |

Closeout KPI snapshot(마감 KPI 스냅샷): OOS gross profit/loss(표본외 총이익/총손실) `772.4300/-827.6400`, avg win/loss(평균 이익/손실) `1.5700/-0.9783`, payoff(손익비) `1.6048`, expectancy(기대값) `-0.0400`, recovery(회복 계수) `-0.5200`.

Side balance(방향 균형): `long material 610 meaningful 160, short material 107 meaningful 0`. This weakens the original two-sided thesis(이것은 원래 양방향 가설을 약화한다).

## Evidence Gap(근거 간극)

Trade list available(거래 목록 사용 가능): `False`.

Deal PnL columns available(거래 손익 열 사용 가능): `False`.

Missing telemetry columns(누락 텔레메트리 열):

- validation telemetry: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)
- validation summary: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)
- oos telemetry: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)
- oos summary: no_deal_level_entry_exit_or_pnl_columns(거래별 진입/청산/손익 열 없음)

## Decision Reasons(결정 근거)

- F82D showed exact signal/feature/ONNX parity but runtime economics failed(F82D가 신호/피처/온엑스 동등성은 맞고 런타임 경제성은 실패했음을 보임).
- Runtime DD expanded from proxy 3.91%/2.45% to MT5 57.0%/20.36%(런타임 손실폭이 프록시 3.91%/2.45%에서 MT5 57.0%/20.36%로 확대).
- Runtime PF fell below 1 in both splits(PF가 두 구간 모두 1 아래로 하락).
- F82C forensics has no deal-level trade list(F82C 포렌식에 거래별 목록이 없음).
- F82C telemetry has no deal-level entry/exit/PnL columns(F82C 텔레메트리에 거래별 진입/청산/손익 열이 없음).
- A deal-reconciled label/capture axis is new evidence, not threshold-only repetition(거래 손익 대조 라벨/캡처 축은 새 근거이지 임계값 반복이 아님).
- F82B two-sided thesis was not fully satisfied because long side dominated material and meaningful candidates(F82B 양방향 가설은 롱이 물질/의미 후보를 지배해 완전히 충족되지 않음).

## Forbidden Repairs(금지 수리)

- probability threshold only(확률 임계값만 변경)
- probability quantile only(확률 분위수만 변경)
- same candidate risk filter only(같은 후보 위험 필터만 변경)
- same one-sided long branch rerun without deal PnL evidence(거래 손익 근거 없는 같은 단방향 롱 가지 재실행)

## Next(다음)

F82F should first capture or reconstruct deal-level entry/exit/PnL evidence(F82F는 먼저 거래별 진입/청산/손익 근거를 캡처하거나 재구성), then rebuild a MT5-realized label only if that evidence is available(그 근거가 있을 때만 MT5 실현 손익 라벨을 재구축).

Rotation condition(회전 조건): If F82F cannot produce deal-level PnL evidence from tester report, EA telemetry, or a narrow telemetry patch(F82F가 테스터 보고서, EA 텔레메트리, 좁은 텔레메트리 패치에서 거래별 손익 근거를 만들 수 없으면), close this repair path as negative memory and rotate(이 수리 경로를 부정 기억으로 닫고 회전).

Forbidden claims(금지 주장): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

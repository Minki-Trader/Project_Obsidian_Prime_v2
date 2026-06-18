# F83G Runtime-Realized Outcome Repair Or Rotation Decision(F83G 런타임 실현 결과 수리 또는 회전 결정)

Updated(갱신): 2026-06-18T08:55:26Z

- run id(실행 ID): `frontier83G_runtime_realized_outcome_repair_or_rotation_decision_v1`
- parent run(부모 실행): `frontier83F_short_density_proxy_runtime_gap_analysis_v1`
- status(상태): `closed_negative_runtime_winrate_erosion_after_signal_parity_rotation_to_f84_no_authority`
- judgment(판정): `negative_memory_with_runtime_realized_winrate_rebuild_rotation_no_authority`
- closeout label(마감 라벨): `negative_memory_with_preserved_runtime_parity_clue_and_winrate_gap_seed(부정 기억과 보존 런타임 동등성 단서 및 승률 간극 씨앗)`
- claim boundary(주장 경계): `stage_closeout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Decision(결정)

Action(행동): F83을 valid negative runtime evidence(유효한 부정 런타임 근거)로 closeout(마감)하고, F84를 runtime-realized win-rate rebuild(런타임 실현 승률 재구축) 축으로 handoff(인계)한다.

Effect(효과): F83의 실패를 버리지 않고, 다음 가설이 고쳐야 할 실제 원인인 runtime win-rate erosion(런타임 승률 침식)을 새 label/target/risk axis(라벨/목표/위험 축)로 가져간다.

## KPI Closeout(KPI 마감)

| view(보기) | net(순손익) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | win rate(승률) | gap cause(간극 원인) |
|---|---:|---:|---:|---:|---:|---|
| F83D/F82B short-density proxy validation(F83D/F82B 숏 밀도 프록시 검증) | `264.3229` | `1.2027` | `11.3885` | `8.3173` | `0.4170` | pending_until_f83f(전선83F까지 보류) |
| F83D/F82B short-density proxy OOS(F83D/F82B 숏 밀도 프록시 표본외) | `401.0262` | `1.4727` | `4.6768` | `8.3505` | `0.4525` | pending_until_f83f(전선83F까지 보류) |
| F83E MT5 runtime validation(F83E MT5 런타임 검증) | `-285.6600` | `0.8300` | `58.8600` | `8.2132` | `30.0400` | runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식) |
| F83E MT5 runtime OOS(F83E MT5 런타임 표본외) | `-37.1700` | `0.9700` | `19.2400` | `8.2667` | `33.3100` | runtime_win_rate_erosion_after_signal_parity(신호 동등성 이후 런타임 승률 침식) |

Runtime validation(런타임 검증): net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `-285.66/0.83/58.86/8.213235294117647`.

Runtime OOS(런타임 표본외): net/PF/DD/trades-day(순손익/수익 팩터/손실폭/일 거래) `-37.17/0.97/19.24/8.266666666666667`.

## Why Not Repair Same Surface(같은 표면을 수리하지 않는 이유)

- Signal parity(신호 동등성)와 feature readiness(피처 준비)는 통과했지만, runtime win rate(런타임 승률)가 validation -11.66pp, OOS -11.94pp 침식됐다.
- Order fill gap(주문 체결 간극)은 net gap(순손익 간극)의 약 0.45% 수준이라 주 원인으로 보기 어렵다.
- DD(손실폭)는 validation 58.86%, OOS 19.24%까지 커졌다.
- 같은 threshold/filter/parameter(임계값/필터/파라미터)만 바꾸는 repair(수리)는 new axis(새 축)가 아니므로 금지한다.

## Preserved Clues(보존 단서)

- F83B/F83C long teacher overlay runtime parity clue(F83B/F83C 롱 교사 덧씌움 런타임 동등성 단서)
- F83E ONNX/signal/materialization path worked as a runtime probe harness(F83E 온엑스/신호/물질화 경로는 런타임 탐침 장치로 작동)
- F83F isolated win-rate erosion after signal parity(F83F가 신호 동등성 이후 승률 침식을 분리)
- short-density supply can meet target trade density in proxy(F83D 숏 밀도 공급은 프록시에서 목표 거래 밀도를 충족)

## Negative Memory(부정 기억)

- Do not reuse f82b_10355 smooth_trade_supply short close_direction surface(동일 f82b_10355 숏 종가방향 부드러운 공급 표면) with parameter-only repair(파라미터만 수리).
- Do not treat signal parity(신호 동등성) or ONNX export(온엑스 내보내기) as economics authority(경제성 권위).
- Do not explain the F83E loss primarily by fill gap(체결 간극) without row-level evidence(행 단위 근거).

## Next Frontier Proposal(다음 전선 제안)

Next stage(다음 단계): `stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap`

Next run(다음 실행): `frontier84A_stage_open_runtime_realized_winrate_rebuild_after_signal_parity_gap_v1`

Question(질문): Can runtime-realized win/loss and stop-touch/fill-path labels(런타임 실현 승패 및 손절·익절 터치/체결 경로 라벨)이 signal parity after proxy success(프록시 성공 뒤 신호 동등성)에서도 actual MT5 win rate(실제 MT5 승률)를 보존하는 exportable ONNX candidate(내보내기 가능 온엑스 후보)를 만들 수 있는가?

Boundary(경계): F84 scaffold(전선84 뼈대)는 open evidence(개방 근거)가 아니다. F84A가 독립 open packet(개방 묶음)을 만들어야 한다.

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.

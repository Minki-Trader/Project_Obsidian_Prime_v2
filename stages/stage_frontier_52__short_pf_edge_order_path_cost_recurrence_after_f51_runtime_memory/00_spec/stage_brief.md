# Frontier52 Stage Brief(전선52 단계 요약)

- stage_id(단계 ID): `stage_frontier_52__short_pf_edge_order_path_cost_recurrence_after_f51_runtime_memory`
- work_family(작업군): `runtime_backtest(MT5/런타임/백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- source_boundary(원천 경계): F51 candidate `f51c_0046` is reference-only(F51 후보는 참조 전용).

## Hypothesis(가설)
F51(전선51)의 failure(실패)는 ONNX signal handoff(온엑스 신호 인계)보다 MT5 execution lifecycle(메타트레이더5 실행 생명주기)에 있을 수 있다.

## Runtime Policy(런타임 정책)
- InpCloseOnFlatSignal: True
- InpEntryTransitionOnly: True
- InpEntryTransitionRearmMinConfidenceDelta: 0.02
- InpMaxHoldBars: 6
- InpReentryCooldownBars: 3
- InpSameDirectionReentryCooldownBars: 6
- InpAtrSltpEnabled: True
- InpAtrPeriod: 14
- InpAtrStopMultiplier: 0.8
- InpAtrTakeProfitMultiplier: 1.2
- InpAtrMinStopPoints: 40.0
- InpAtrMaxStopPoints: 180.0
- InpAtrMinTakeProfitPoints: 60.0
- InpAtrMaxTakeProfitPoints: 260.0

## Exit Rule(종료 규칙)
MT5 runtime probe(MT5 런타임 탐침) 뒤 preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫는다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).

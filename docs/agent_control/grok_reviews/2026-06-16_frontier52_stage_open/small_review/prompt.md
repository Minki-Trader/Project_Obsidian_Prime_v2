Project Obsidian Prime v2 bounded Grok review.

Review type: stage-open small review(단계 개방 소규모 검토).

Codex current truth(현재 진실):
- Frontier51(전선51) is closed negative_memory(부정 기억), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed.
- F51 representative(대표) candidate f51c_0046 had proxy validation PF/DD/trades/density = 1.037/4.486/549/3.0 per day and OOS = 1.068/2.878/348/2.656 per day.
- F51 MT5 runtime probe(MT5 런타임 탐침) had exact signal/feature parity(신호/피처 동등성): signal_diff=0, feature_ready_diff=0.
- But MT5 validation PF/DD/trades = 0.78/86.37%/123 and OOS = 0.86/50.15%/86.
- F51 negative memory(부정 기억): outcome-memory recurrence and order-path proxy(주문 경로 프록시) underestimated MT5 order/fill/single-position drawdown/trade compression(주문/체결/단일 포지션 손실폭/거래 압축).

Proposed Frontier52(전선52) direction:
- Stage id(단계 ID): stage_frontier_52__short_pf_edge_order_path_cost_recurrence_after_f51_runtime_memory.
- Primary family(주 작업군): runtime_backtest(MT5/런타임/백테스트 실행).
- Primary skill(주 스킬): obsidian-runtime-parity(런타임 동등성).
- Hypothesis(가설): F51 failure is not primarily ONNX signal handoff(온엑스 신호 인계) but MT5 execution lifecycle(실행 생명주기): close-on-flat(무신호 청산), transition-only entry(전환 진입), same-direction cooldown(동방향 재진입 쿨다운), shorter max hold(짧은 최대 보유), and ATR SL/TP(평균진폭 손절/익절) may reduce drawdown/trade compression while keeping exact signal/feature parity.
- Proposed bounded probe(제한 탐침): reuse F51 candidate only as reference artifact(참조 산출물), retrain/materialize under F52 run identity(실행 정체성), then change only RuntimeProbeEA .set parameters(설정 파라미터): InpCloseOnFlatSignal=true, InpEntryTransitionOnly=true, InpEntryTransitionRearmMinConfidenceDelta=0.02, InpMaxHoldBars=6, InpReentryCooldownBars=3, InpSameDirectionReentryCooldownBars=6, InpAtrSltpEnabled=true, ATR period 14, stop multiplier 0.8, TP multiplier 1.2, min/max stop/take clamps.
- Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). No baseline/promotion/runtime authority/live readiness(기준선/승격/런타임 권위/실거래 준비).
- Success for this stage(이번 단계 성공): preserved clue(보존 단서) if MT5 DD and trade compression improve materially without parity break. Negative memory(부정 기억) if PF/DD/trade shape still fail. Completion candidate(완성 후보) only if all four axes are much closer, but final hard gate(최종 강제 게이트)는 not in this stage.

Question(질문): Is this F52 direction novel and bounded enough after F51 negative memory, or does it repeat the same failed repair axis? Name any high-risk local verification(로컬 검증) Codex must do before MT5 backtest(백테스트). Do not recommend claiming authority(권위).

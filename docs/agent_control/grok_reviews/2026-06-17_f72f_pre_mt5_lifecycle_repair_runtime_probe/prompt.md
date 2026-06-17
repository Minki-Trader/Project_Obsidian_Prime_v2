# F72F Pre-MT5 Lifecycle Repair Runtime Probe Review(F72F 사전 MT5 생명주기 수리 런타임 탐침 검토)

Claim boundary(주장 경계): pre-MT5 repair review only(사전 MT5 수리 검토 전용). No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Codex current truth(현재 진실):
- Active stage(활성 단계): `stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling`.
- F72D mandatory MT5 Runtime Probe(MT5 런타임 탐침)는 completed(완료) 2/2.
- F72D ONNX probability parity(온엑스 확률 동등성) 3/3, signal parity(신호 동등성) 3/3, feature readiness parity(피처 준비 동등성) 0 diff.
- F72D runtime OOS(표본외) net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일거래): `45.04 / 1.06 / 18.10% / 1.1641`.
- F72D gap cause(간극 원인): `trade_lifecycle_gap_after_signal_parity`; selected signals(선택 신호) 730 but orders(주문) 234 and trades(거래) 227 in OOS.

F72E gap analysis(간극 분석):
- Local cause(로컬 원인): proxy counted overlapping signals(겹친 신호) as separate trades, while MT5 uses single-position lifecycle(단일 포지션 생명주기) with SL/TP/max hold(손절/익절/최대 보유).
- F72E lifecycle repair scout(생명주기 수리 탐색): 240 candidates(후보), repair probe worthy(수리 탐침 가치) 1, meaningful candidate(의미 후보) 0.
- Best repair clue(최선 수리 단서): `f72e_0200` / `short_h24_sl0.9_tp1.8` / `mfe_mae_gap_040` / `extra_trees_3class_bridge_lifecycle_scout` / `all58`.
- Lifecycle validation(생명주기 검증) net/PF/DD/trades/day: `1145.3354 / 1.0874 / 9.7532% / 2.2426`.
- Lifecycle OOS(생명주기 표본외) net/PF/DD/trades/day: `799.9634 / 1.0624 / 10.4275% / 2.6823`.
- This is weak but directly tests the F72D gap cause(약하지만 F72D 간극 원인을 직접 시험한다).

Codex proposed direction(Codex 제안 방향):
Run one F72F MT5 Runtime Probe(MT5 런타임 탐침) for `f72e_0200` as observation-only repair probe(관찰 전용 수리 탐침). Pre-declared pass/fail meaning:
- If ONNX/signal/feature parity fails(동등성 실패), classify invalid/blocked(무효/차단) and repair artifact semantics(산출물 의미).
- If parity passes but runtime KPI remains weak(런타임 KPI 약함), record negative memory/preserved clue(부정 기억/보존 단서) and likely close F72.
- Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).

Question(질문): From this bounded evidence(제한 근거), should Codex execute the single F72F MT5 repair probe, or should F72 close without another MT5 run? Classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요). Answer only from this prompt; do not inspect files, run tools, browse, or claim external verification(외부 검증).

You are Grok as external second opinion(외부 2차 의견) for Project Obsidian Prime v2.

Review size(검토 크기): small(소규모).
Task(작업): Frontier 54 stage-open(전선54 단계 개방) critique only.

Current truth(현재 진실):
- F53 closed as negative memory(부정 기억).
- F53 handoff parity(인계 동등성) was clean: feature_ready_diff=0 and signal_count_diff=0 on validation_is/OOS.
- F53 economics(경제성) failed: MT5 validation_is PF=0.37 DD=31.92 trades=1325; OOS PF=0.56 DD=19.18 trades=1337.
- Therefore F54 must not repeat F53 path-quality MFE/MAE/horizon label(경로 품질 최대유리/불리변동/수평 손익 라벨). It needs a new PF source(수익 팩터 원천).
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

Proposed F54 hypothesis(제안 가설):
- Build a runtime-shaped payoff source(런타임 형태 손익 원천).
- For each US100 M5 row, simulate an isolated short trade using the same kind of ATR SL/TP and maxhold envelope(평균진폭 손익절 및 최대 보유 봉투) intended for MT5:
  - maxhold=6 bars
  - ATR period=14
  - stop multiplier=0.8, take-profit multiplier=1.2
  - stop clamp=40..180 points, TP clamp=60..260 points
  - conservative same-bar both-hit handling(같은 봉 동시 도달 보수 처리): stop first
- Train a classifier(분류기) on train-only runtime-shaped positive payoff(학습 전용 런타임형 양수 손익) rather than F53 path-quality labels.
- Evaluate by sequential proxy(순차 프록시): one position at a time, skip overlapping signals until simulated exit. This matches close-on-flat=false(무신호 청산 꺼짐), maxhold/ATR runtime(최대 보유/평균진폭 런타임) more closely than F53.

Bounded scout evidence(제한 탐색 근거):
- Candidate(후보): ExtraTrees depth6 leaf80(엑스트라트리 깊이6 리프80), score_q=0.70.
- train proxy(학습 프록시): PF=1.218109, DD=4.546879, density=4.383944/day.
- validation proxy(검증 프록시): PF=1.027931, DD=6.593274, density=5.469945/day, trades=1001.
- OOS proxy(표본외 프록시): PF=1.070053, DD=4.414365, density=5.854962/day, trades=767.
- Nearby alternatives(인접 대안):
  - HGB q70 had density 5.66/6.37 but ONNX export(온엑스 내보내기) risk is higher.
  - RF q70 had PF 1.02/1.13 but validation density 4.69/day is below the target band.
- Therefore Codex proposes one MT5 runtime probe(MT5 런타임 탐침) on ExtraTrees q70 only, not a model-family sweep(모델군 다중 탐색).

Runtime policy(런타임 정책) for probe:
- InpCloseOnFlatSignal=false(무신호 청산 꺼짐)
- InpEntryTransitionOnly=false(진입 전환 전용 꺼짐)
- cooldowns=0(쿨다운 0)
- maxhold=6
- ATR SL/TP enabled(평균진폭 손익절 켜짐) with the same multipliers/clamps above
- ONNX output(온엑스 출력): p_short=runtime payoff score, p_flat=0, p_long=0; threshold_margin(문턱값 마진) uses the score threshold directly.

Question(질문):
1. Is this a valid new hypothesis lifecycle(새 가설 생명주기), distinct from F53?
2. Is ExtraTrees q70 a reasonable single MT5 runtime probe(단일 MT5 런타임 탐침) candidate?
3. What failure mode(실패 양상) should Codex watch first?
4. Answer bounded as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요). Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

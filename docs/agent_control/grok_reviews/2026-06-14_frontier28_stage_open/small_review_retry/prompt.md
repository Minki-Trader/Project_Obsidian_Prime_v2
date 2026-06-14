# Frontier28 Stage-Open Retry Review

Do not inspect files or run tools. Use only this bounded evidence(제한 근거) and answer the requested fields.

F27 facts(F27 사실):
- F27 soft penalty rank(연성 페널티 순위) restored a union surface(합집합 표면): 234 candidates(후보), 205 broad scout envelope rows(넓은 탐색 외피 행), 189 density bridge rows(빈도 연결 행), 19 scout clue rows(탐색 단서 행).
- F27 produced 0 seed surface rows(씨앗 표면 행) and 0 handoff candidate rows(인계 후보 행).
- Best F27 row: validation PF/density/DD(검증 수익 팩터/빈도/손실폭) 1.310/5.962/17.839, OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭) 1.151/6.687/13.416.
- F27 closeout(마감) preserved the surface as a clue(단서) but recorded negative memory(부정 기억): no seed/handoff(씨앗/인계 없음).

Proposed F28:
- New hypothesis(새 가설): rank candidates by train-only chronological chunk stability(학습 전용 시간순 조각 안정성), not by forward metrics(전진 지표).
- Changed variable(변경 변수): `train_subperiod_pf_dd_balance_stability_gap_rank(학습 하위기간 수익 팩터/손실폭 균형 안정성 격차 순위)`.
- Train split(학습 분할) is divided into 4 chronological chunks(시간순 4조각).
- Penalize PF floor weakness(수익 팩터 바닥 약점), chunk DD concentration(조각 손실폭 집중), density imbalance(빈도 불균형), net-negative chunk count(음수 조각 수), low equity R2 floor(낮은 자산 R2 바닥), and loss streak pressure(연속 손실 압력).
- Validation/OOS(검증/표본외) are read-only diagnostics(읽기 전용 진단), not selection inputs(선택 입력).
- No ONNX/MT5/WFO(온엑스/메타트레이더5/워크포워드 최적화) until handoff candidate rows(인계 후보 행) > 0 and pre-expensive review(비싼 검증 전 검토) passes.

Question:
Is F28 acceptable as a new frontier hypothesis(새 전선 가설), or is it a disguised F27 repair loop(위장된 F27 수리 반복)?

Answer only:
verdict: accepted / rejected / needs_local_verification
novelty_ok: yes/no
leakage_risk: low/medium/high
forbidden_path_risk: low/medium/high
specific_change_requests:

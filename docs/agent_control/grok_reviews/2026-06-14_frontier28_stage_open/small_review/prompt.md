# Grok Review Request: Frontier28 Stage Open

Review size: small review(소규모 검토)

## Codex Direction Before Grok

Current truth(현재 진실):
- Frontier27(전선27) closed as `preserved_clue_negative_memory(보존 단서+부정 기억)`.
- F27B rebuilt the full F24 80 micro pool(전체 F24 80 미세 구간 풀) and produced `234` soft union candidates(연성 합집합 후보), `205` broad scout envelope rows(넓은 탐색 외피 행), `189` density bridge rows(빈도 연결 행), `19` scout clue rows(탐색 단서 행), `0` seed surface rows(씨앗 표면 행), and `0` handoff candidate rows(인계 후보 행).
- Best F27B row `f27b_0181`: validation PF/density/DD(검증 수익 팩터/빈도/손실폭) `1.310 / 5.962 / 17.839`, OOS PF/density/DD(표본외 수익 팩터/빈도/손실폭) `1.151 / 6.687 / 13.416`.
- F27C repair(수리) rejected validation/OOS targeted repair(검증/표본외 표적 수리), F26 threshold relaxation(F26 임계값 완화), and any ONNX/MT5(온엑스/메타트레이더5) branch because no handoff candidate existed.
- F27D next clue(다음 단서): `train_only_stability_gap_penalty_for_forward_pf_dd_balance_reference_only(전방 PF/DD 균형을 위한 학습 전용 안정성 격차 페널티 참조 전용)`.

Proposed Frontier28(전선28) hypothesis:
- Test whether a train-only stability gap penalty(학습 전용 안정성 격차 페널티), computed from chronological train chunks(시간순 학습 조각), can rank the F27 soft union surface(연성 합집합 표면) toward better forward PF/DD balance(전진 수익 팩터/손실폭 균형).
- The changed variable(변경 변수) is not the F27 soft penalty itself. It is a new selector: `train_subperiod_pf_dd_balance_stability_gap_rank(학습 하위기간 수익 팩터/손실폭 균형 안정성 격차 순위)`.
- Candidate construction(후보 구성) may use the reproducible F27/F24 micro-union machinery as reference input(참조 입력), but selection must be train-only(학습 전용) and must not use validation/OOS(검증/표본외) metrics except read-only diagnostics(읽기 전용 진단).

Locked F28 design:
- Split train(학습 분할) into 4 chronological chunks(시간순 4개 조각).
- For each candidate, compute train-chunk PF floor(수익 팩터 바닥), DD max(손실폭 최대), density imbalance(빈도 불균형), net-positive chunk count(양수 조각 수), equity trend R2 floor(자산 추세 R2 바닥), and max loss streak pressure(최대 연속 손실 압력).
- Penalize high train chunk dispersion(학습 조각 산포), especially `PF good globally but weak in one chunk(전체 PF는 좋지만 한 조각이 약함)` and `DD below global cap but chunk DD concentrated(전체 손실폭은 낮지만 조각 손실폭 집중)`.
- Validation/OOS(검증/표본외) are read-only forward diagnostics(읽기 전용 전진 진단).
- No ONNX/MT5/WFO(온엑스/메타트레이더5/워크포워드 최적화) until handoff_candidate_rows(인계 후보 행) > 0 and pre-expensive Grok review(비싼 검증 전 그록 검토) passes.

Success criteria(성공 기준):
- F28A may open only if this is a genuinely new hypothesis(새 가설) versus a disguised F27 repair(위장된 F27 수리).
- F28B scout success is not final completion(최종 완성). It can only create scout clue(탐색 단서), seed surface(씨앗 표면), or handoff candidate(인계 후보).
- Hard goal gates(강제 목표 게이트) remain final completion review(최종 완성 검토) only.

Claim boundary(주장 경계):
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
- F28 stage-open(단계 개방) can only claim design readiness(설계 준비) if accepted and locally verified.

## Narrow Review Question

Is the proposed F28 stage-open direction acceptable as a new frontier hypothesis(새 전선 가설), or should it be rejected as a disguised F27 repair loop(위장된 F27 수리 반복)?

Please answer with:
- verdict: accepted / rejected / needs_local_verification
- novelty_ok: yes/no
- leakage_risk: low/medium/high
- forbidden_path_risk: low/medium/high
- specific change requests, if any

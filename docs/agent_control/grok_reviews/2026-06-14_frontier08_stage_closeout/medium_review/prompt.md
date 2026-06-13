Frontier08 stage closeout review(전선08 단계 마감 검토) 요청입니다.

Codex current truth(코덱스 현재 진실):
- project(프로젝트): US100 M5 ONNX(온엑스) exploration(탐색).
- stage(단계): stage_frontier_08__sample_weighted_objective.
- hypothesis(가설): train-only sample weighting(학습 전용 표본 가중)이 label/model objective(라벨/모델 목적)를 바꾸어 density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움)를 동시에 개선할 수 있다.
- Stage12~364는 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않습니다.
- Frontier07 risk label(전선07 위험 라벨)은 reference surface(참조 표면)로만 사용했습니다.
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

Proposed direction(제안 방향):
- Close Frontier08(전선08 마감) as preserved_clue_negative_memory_no_authority(보존 단서 + 부정 기억 + 권위 없음).
- Do not run expensive WFO/MT5(비싼 WFO/MT5 실행 안 함), because strict scout clue rows(엄격 탐색 단서 행)가 0입니다.
- Carry forward only the clue(단서): adverse/path utility weighting(불리 이동/경로 효용 가중)은 OOS density(표본밖 밀도)를 5~6/day로 만들 수 있지만 PF(수익 팩터)와 DD(손실폭)를 충분히 고치지 못했습니다.
- Carry forward negative memory(부정 기억): sample weighting alone(표본 가중 단독)은 validation DD(검증 손실폭) 58~60% 부근을 해결하지 못했습니다.

Success criteria(성공 기준):
- Review whether closeout(마감)이 justified(정당)한지.
- Identify any invalid setup(무효 설정), leakage(누수), missing paired control(짝 대조군 누락), or overclaim(과장 주장).
- Say accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요).

Bounded evidence(제한 근거):
1. Stage-open Grok(단계 개방 그록) condition summary(조건 요약):
   - paired unweighted controls(짝지은 무가중 대조군) required.
   - train-only weight derivation(학습 전용 가중 산출) required.
   - cap <= 4 weight families x <= 3 variants(가중 가족 4개 이하, 각 3변형 이하).
   - no threshold escape hatch(임계값 탈출구 없음), argmax-only(최대확률 전용).
   - strict scout clue(엄격 탐색 단서) needed before WFO/MT5(WFO/MT5).

2. Frontier08B proxy scout(전선08B 프록시 탐색):
   - targets(목표): label_v1 reference(라벨 v1 참조), Frontier07 risk label reference(전선07 위험 라벨 참조).
   - candidates(후보): 48 = 2 targets x 8 policies x 3 models.
   - strict scout clue rows(엄격 탐색 단서 행): 0.
   - preserved clue rows(보존 단서 행): 27.
   - best candidate(최상위 후보): f07risk logistic plain adv_a100.
   - validation PF/density/DD(검증 수익 팩터/밀도/손실폭): 1.00405 / 6.94536 per day / 58.0016%.
   - OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): 1.19464 / 5.47328 per day / 15.6550%.
   - paired axis improvement count(짝 비교 축 개선 수): 5.
   - ONNX parity(온엑스 동등성): true.
   - failure boundary(실패 경계): validation DD(검증 손실폭)가 너무 크고 PF(수익 팩터)가 약합니다.

3. Frontier08C capped repair scout(전선08C 상한 수리 탐색):
   - repair scope(수리 범위): Frontier07 risk label reference(전선07 위험 라벨 참조) only.
   - candidates(후보): 12 = 1 target x 4 policies x 3 models.
   - policies(정책): control(대조군), util_a150, adv_a150, side_a150. This stays within 4 families x 3 variants cap(4가족 x 3변형 상한 안).
   - strict scout clue rows(엄격 탐색 단서 행): 0.
   - preserved clue rows(보존 단서 행): 4.
   - best candidate(최상위 후보): f07risk logistic plain util_a150.
   - validation PF/density/DD(검증 수익 팩터/밀도/손실폭): 1.00426 / 7.07650 per day / 59.5044%.
   - OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): 1.16725 / 5.65649 per day / 16.0798%.
   - paired axis improvement count(짝 비교 축 개선 수): 3.
   - ONNX parity(온엑스 동등성): true.
   - matched control for same target/model(같은 목표/모델 대조군): validation 1.01679 / 4.61749/day / 58.8505%; OOS 1.19765 / 3.00763/day / 13.6067%.
   - repair did not improve all four axes(수리가 네 축을 동시에 개선하지 못함).

4. Data/model boundaries(데이터/모델 경계):
   - weights(가중치)는 train split(학습 분할)에서만 산출했습니다.
   - validation/OOS(검증/표본밖)는 평가 전용입니다.
   - target labels(목표 라벨)는 future path oracle labels(미래 경로 오라클 라벨)라 runtime signal(런타임 신호)로 주장하지 않습니다.
   - Tier B and combined(티어 B와 합산)는 missing_required(필수 누락)로 기록했습니다.
   - No WFO/MT5(워크포워드/메타트레이더5 없음), because strict scout clue(엄격 탐색 단서)가 없습니다.

Question(질문):
Is the proposed Frontier08 closeout(전선08 마감) accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)? Please focus on claim boundary(주장 경계), whether WFO/MT5 should remain out of scope(범위 밖), and whether preserved clue + negative memory is the right closeout(보존 단서 + 부정 기억 마감이 맞는지).

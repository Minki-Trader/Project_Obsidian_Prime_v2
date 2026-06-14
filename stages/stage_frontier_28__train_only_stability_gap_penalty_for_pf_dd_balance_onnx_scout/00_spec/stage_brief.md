# Frontier28 Stage Brief(전선28 단계 요약)

Opened(개방): 2026-06-14T10:56:42Z

Frontier thesis(전선 가설): train-only chronological stability gaps may predict forward PF/DD balance better than global train soft scores(학습 전용 시간순 안정성 격차가 전체 학습 연성 점수보다 전진 수익 팩터/손실폭 균형을 더 잘 예고할 수 있다)

Hypothesis(가설): F27 restored a tradable-density union surface but did not create seed or handoff rows; F28 tests whether train chunk PF/DD dispersion exposes the unstable unions before validation/OOS is read(F27은 거래 빈도 합집합 표면을 복원했지만 씨앗/인계를 만들지 못했고, F28은 검증/표본외를 읽기 전에 학습 조각 PF/DD 산포가 불안정 합집합을 드러내는지 시험한다)

Novelty delta(신규성 차이): F28은 F27 soft penalty rank(F27 연성 페널티 순위)를 조정하지 않습니다. changed variable(변경 변수)은 train_subperiod_pf_dd_balance_stability_gap_rank(학습 하위기간 수익 팩터/손실폭 균형 안정성 격차 순위)입니다.

Chunk contract(조각 계약): train split(학습 분할)을 시간순 4개 equal-row chunk(동일 행 수 조각)로 고정합니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 handoff_candidate_rows > 0(인계 후보 행 0 초과)이고 pre-expensive Grok review(비싼 검증 전 그록 검토)가 통과할 때만 실행합니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.

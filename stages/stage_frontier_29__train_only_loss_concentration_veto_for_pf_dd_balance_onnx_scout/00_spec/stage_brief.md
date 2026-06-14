# Frontier29 Stage Brief(전선29 단계 요약)

Opened(개방): 2026-06-14T11:33:10Z

Frontier thesis(전선 가설): F28 train-stable but forward-imbalanced union rows may contain concentrated train loss pockets; removing those train-only pockets can improve PF/DD balance without reusing forward metrics

Hypothesis(가설): A train-loss-conditioned veto mask, applied after reconstructing the F28/F27 same-side union masks, may reduce loss concentration and leave smoother forward PF/DD/density reads.

Novelty delta(신규성 차이): F29는 F28 stability rank(안정성 순위)를 조정하지 않습니다. changed variable(변경 변수)은 train-loss-conditioned veto mask(학습 손실 조건 차단 마스크)입니다.

Veto contract(차단 계약): train-only trade losses(학습 전용 거래 손실)만 pocket definition(구간 정의), threshold(임계값), rank(순위)에 씁니다. validation/OOS(검증/표본외)는 read-only(읽기 전용)입니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)와 pre-expensive Grok review(비싼 검증 전 그록 검토)가 있을 때만 실행합니다.

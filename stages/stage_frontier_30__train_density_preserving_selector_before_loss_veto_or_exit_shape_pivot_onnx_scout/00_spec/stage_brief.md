# Frontier30 Stage Brief(전선30 단계 요약)

Opened(개방): 2026-06-14T12:14:37Z

Frontier thesis(전선 가설): F29 loss veto created density bridge fragments but over-thinned forward density; a train-only preselector before veto may preserve 5-10/day forward density reads while improving PF/DD balance.

Hypothesis(가설): A train-density-preserving preselector, computed only on train split source-union diagnostics before loss veto, can reduce the density-thinning failure mode that made F29 scout rows zero.

Novelty delta(신규성 차이): F30(전선30)은 F29(전선29) threshold(임계값)를 완화하지 않습니다. changed variable(변경 변수)은 `train_density_preserving_preselector_before_loss_veto`입니다.

Exit-shape pivot role(청산 형태 전환 역할): `reference_fallback_only_not_active_changed_variable`. 이번 proxy(프록시)의 활성 변수(active variable, 활성 변수)가 아닙니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)와 pre-expensive Grok review(비싼 실행 전 그록 검토)가 있을 때만 실행합니다.

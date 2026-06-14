# Frontier31 Stage Brief(전선31 단계 요약)

Opened(개방): 2026-06-14T12:50:09Z

Frontier thesis(전선 가설): F30(전선30)이 회복한 density-preserved source scouts(밀도 보존 원천 탐색) 5개는 진입 표면(entry surface, 진입 표면)은 유지하고, return-space exit-shape transform(수익률 공간 청산 형태 변환)만 바꾸면 PF lift(PF 상승)와 DD reduction(손실폭 감소)이 가능한지 시험합니다.

Hypothesis(가설): train-only(학습 전용)으로 고른 loss cap/asymmetric clip(손실 상한/비대칭 클립) 변환이 validation/OOS(검증/표본외)에서 read-only(읽기 전용)으로 seed surface(씨앗 표면)나 handoff candidate(인계 후보) 단서를 만들 수 있습니다.

Novelty delta(신규성 차이): F31(전선31)은 F30(전선30)에서 reference fallback only(참조 대체 전용)였던 exit-shape pivot(청산 형태 전환)을 단일 active changed variable(활성 변경 변수)로 격상합니다.

Fixed surface(고정 표면): `f30b_0003, f30b_0151, f30b_0185, f30b_0213, f30b_0214`.

Data limitation(데이터 한계): `future_log_return_12` only(12봉 미래 로그수익률만 있음), no intrabar high/low/MFE/MAE(봉내 고가/저가/최대유리/최대불리 없음).

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 executable exit representation(실행 가능한 청산 표현), handoff candidate(인계 후보), pre-expensive Grok review(비싼 실행 전 그록 검토)가 모두 있을 때만 실행합니다.

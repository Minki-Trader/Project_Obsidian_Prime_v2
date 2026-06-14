**verdict(판정):** accepted(수용)

**novelty_ok(신규성 적절):** yes

**main_leakage_or_overfit_risk(주요 누수 또는 과최적화 위험):** Payoff-dominance labels(수익 우위 라벨) that use MFE/MAE(최대 유리/불리 이동) and stop/take(손절/익절) path stats must be fit train-only(학습 전용 적합) with frozen label rules on validation/OOS(검증/표본외 고정 규칙), or forward-path information(전방 경로 정보) and label-parameter tuning(라벨 파라미터 조정) will leak and overfit the split(분할 과최적화).

**must_not_repeat(반복 금지):** Do not stack single-feature filters(단일 피처 필터 누적) or treat F36(전선36) scout PF-DD(탐색 수익 팩터-손실폭) as seed/runtime evidence(씨앗/런타임 근거) when F36 closed with 0 seed/runtime(씨앗/런타임 0).

**runtime_claim_boundary_ok(런타임 주장 경계 적절):** yes

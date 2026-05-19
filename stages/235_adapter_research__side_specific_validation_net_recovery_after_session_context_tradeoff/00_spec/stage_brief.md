# 235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff

Stage235(235단계)는 Stage234(234단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can side-specific validation net recovery(방향별 검증 순손익 회복) use the cashopen mid PF clue(현금장 초반 중반 수익요인 단서) without losing the OOS reference bound(표본외 기준 경계) from `s233_session_ref_h3_cd8`?

Effect(효과): Stage233(233단계)의 session_p5/session_p10(세션 5분/10분) 반복을 피하고, 검증 순손익과 초반 수익요인을 좁게 복구한다.

## Fixed Requirements(고정 요구)

- OOS reference bound(표본외 기준 경계): `s233_session_ref_h3_cd8`.
- cashopen clue(현금장 초반 단서): `s233_cashopen_long_h3_cd8`.
- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

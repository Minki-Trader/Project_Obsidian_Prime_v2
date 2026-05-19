# 237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure

Stage237(237단계)은 Stage236(236단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a very small threshold/rank-confidence adjustment(미세 문턱값/순위 신뢰도 조정) around `s235_session_ref_h3_cd8` recover validation net/early PF/mid PF(검증 순손익/초반 수익요인/중반 수익요인) to 34D(34D 기준) without damaging OOS net/PF/DD(표본외 순손익/수익요인/낙폭), ATR SL/TP(ATR 손절/익절), and model-controlled risk%(모델 제어 위험 비율)?

Effect(효과): Stage235(235단계)의 cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 실패 축을 반복하지 않고 작은 부족분만 겨냥한다.

## Fixed Requirements(고정 요구)

- reference_adapter(기준 어댑터): `s235_session_ref_h3_cd8`.
- clue_adapter(단서 어댑터): `s235_cashopen45_h3_cd8` is clue-only(단서 전용), not package(묶음 아님).
- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

# 238_adapter_research__score_shape_repair_after_threshold_surface_discrete

Stage238(238단계)은 Stage237(237단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can score shape repair(점수 형태 수리) create enough rank diversity(순위 다양성) around `s235_session_ref_h3_cd8` to recover validation net/early PF/mid PF(검증 순손익/초반 수익요인/중반 수익요인) toward 34D(34D 기준) while preserving OOS net/PF/DD(표본외 순손익/수익요인/낙폭), ATR SL/TP(ATR 손절/익절), and model-controlled risk%(모델 제어 위험 비율)?

Effect(효과): Stage237(237단계)의 binary threshold surface(이진 문턱값 표면) 실패를 반복하지 않고, 모델 출력/점수 분포 자체를 좁게 수리한다.

## Fixed Requirements(고정 요구)

- reference_adapter(기준 어댑터): `s235_session_ref_h3_cd8`.
- cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) are failure memory(실패 기억), not primary axes(주 축 아님).
- model-controlled risk%(모델 제어 위험 비율) remains mandatory(필수 유지).
- ATR SL/TP(ATR 손절/익절) remains mandatory(필수 유지).
- no ONNX hardening(ONNX 경화 없음).
- no deployment/live/production/operating claim(배포/실거래/생산/운영 주장 없음).

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

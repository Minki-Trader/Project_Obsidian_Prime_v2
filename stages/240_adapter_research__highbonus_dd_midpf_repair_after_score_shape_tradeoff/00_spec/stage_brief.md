# 240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff

Stage240(240단계)는 Stage239(239단계) decision(판정)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can the highbonus score clue(고마진 점수 단서) preserve validation/OOS net(검증/표본외 순손익) while repairing validation DD(검증 낙폭), early/mid PF(초반/중간 수익요인), and risk shape(위험 형태)?

Effect(효과): Stage238(238단계)에서 확인한 highbonus(고마진) 단서를 버리지 않고, 34D(34D 기준) 미달 원인인 DD/PF(낙폭/수익요인)를 별도 bounded repair(경계 수리)로 다룬다.

## Fixed Requirements(고정 요구)

- ATR SL/TP(ATR 손절/익절)는 유지한다.
- model-controlled risk%(모델 제어 위험 비율)는 유지하고 5% cap(상한)을 넘지 않는다.
- lowpen015/lowpen025(저마진 벌점 0.15/0.25) 단독 반복은 하지 않는다.
- ONNX hardening(ONNX 경화)은 하지 않는다.
- final adapter(최종 어댑터), deployment(배포), live readiness(실거래 준비)를 주장하지 않는다.

## Seed Evidence(씨앗 근거)

- clue_adapter(단서 어댑터): `s238_highbonus010_rank3f`
- reference_adapter(기준 어댑터): `s238_rank3f_neutral_ref`
- source_report(원천 보고서): `stages/239_adapter_research__stage238_score_shape_followup_review/03_reviews/stage239_score_shape_followup_review.md`
- tradeoff_matrix(상충 표): `stages/239_adapter_research__stage238_score_shape_followup_review/03_reviews/stage239_score_shape_tradeoff_matrix.csv`
- attribution(성과 기여 분석): `stages/239_adapter_research__stage238_score_shape_followup_review/03_reviews/stage239_performance_attribution.csv`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

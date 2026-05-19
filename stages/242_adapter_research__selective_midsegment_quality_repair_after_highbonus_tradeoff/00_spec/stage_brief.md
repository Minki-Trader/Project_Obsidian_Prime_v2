# 242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff

Stage242(242단계)는 Stage241(241단계) review(검토)에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a selective midsegment quality repair(선택적 중간 구간 품질 수리) preserve highbonus validation/OOS net(고마진 검증/표본외 순손익) while repairing validation DD(검증 낙폭), mid PF(중간 수익요인), cost-stressed expectancy(비용 압박 기대값), and ATR/risk telemetry(ATR/위험 기록)?

Effect(효과): Stage240(240단계)의 전역 risk cap(위험 상한) 손상을 반복하지 않고, 손상 원인으로 보이는 중간 구간 품질만 좁게 건드린다.

## Fixed Requirements(고정 요구)

- Preserve ATR SL/TP(ATR 손절/익절).
- Preserve model-controlled risk%(모델 제어 위험 비율) and 5% cap(5% 상한).
- Do not repeat standalone global risk cap compression(전역 위험 상한 압축 단독 반복 금지).
- Do not run ONNX hardening(ONNX 경화) in this stage.
- Do not claim final adapter(최종 어댑터), deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), or runtime authority(런타임 권위).

## Seed Evidence(씨앗 근거)

- strongest_net_oos_clue(최강 순손익/표본외 단서): `s240_highbonus010_samecap`
- balanced_secondary_clue(균형 보조 단서): `s240_highbonus0075_cap0290`
- source_report(원천 보고서): `stages/241_adapter_research__stage240_highbonus_repair_followup_review/03_reviews/stage241_highbonus_followup_review.md`
- tradeoff_matrix(상충 행렬): `stages/241_adapter_research__stage240_highbonus_repair_followup_review/03_reviews/stage241_tradeoff_review_matrix.csv`
- attribution(성과 기여 분석): `stages/241_adapter_research__stage240_highbonus_repair_followup_review/03_reviews/stage241_performance_attribution.csv`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

# Stage92 SL2.05 Net Recovery Follow-up Review(92단계 손절 2.05 순손익 회복 후속 검토)

- run(실행): `run92A_stage92_v41_sl205_net_recovery_followup_review_v1`
- source_stage(원천 단계): `91_adapter_research__v41_sl205_net_recovery_oos_early_repair`
- source_stage91_closeout_commit(원천 91단계 종료 커밋): `8eacc51919b7cd1bfb675eaefcdfc6efadf65f38`
- source_stage91_latest_commit(원천 91단계 최신 커밋): `fe792bfadabc91b41c23a7e54a95f4026053cc2d`
- external_verification_status(외부 검증 상태): `completed_existing_stage91_evidence_reviewed`
- decision(판정): `continue_sl210_tp40_oos_early_recovery_repair_in_stage93`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

Stage92(92단계)는 Stage91(91단계) MT5 evidence(메타트레이더5 근거)를 review gate(검토 관문)로만 판독했다. Effect(효과): 새 실험을 섞지 않고, 다음 Stage93(93단계)의 조합 질문만 좁힌다.

## KPI Read(KPI 핵심성과지표 판독)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) |
|---|---|---:|---:|---:|---:|
| s91_v41_h3_risk475_gate08_sl205_tp40_cd10 | validation_is | 1.4600 | 773.86 | 21.52 | 3.8300 |
| s91_v41_h3_risk475_gate08_sl205_tp40_cd10 | oos | 1.5700 | 609.20 | 18.63 | 3.8100 |
| s91_v41_h3_risk45_gate08_sl205_tp38_cd10 | validation_is | 1.4900 | 760.84 | 20.45 | 3.7700 |
| s91_v41_h3_risk45_gate08_sl205_tp38_cd10 | oos | 1.5500 | 535.63 | 17.87 | 3.3500 |
| s91_v41_h3_risk475_gate08_sl210_tp38_cd10 | validation_is | 1.5400 | 944.24 | 21.30 | 4.6700 |
| s91_v41_h3_risk475_gate08_sl210_tp38_cd10 | oos | 1.5300 | 536.30 | 18.88 | 3.3500 |

## Segment Read(구간 판독)

| adapter(어댑터) | OOS early net(표본외 초반 순손익) | OOS early PF(표본외 초반 수익 팩터) | flag(표식) |
|---|---:|---:|---|
| s91_v41_h3_risk475_gate08_sl205_tp40_cd10 | 13.72 | 1.0487 | oos_early_flatline_risk |
| s91_v41_h3_risk45_gate08_sl205_tp38_cd10 | 6.60 | 1.0247 | oos_early_flatline_risk |
| s91_v41_h3_risk475_gate08_sl210_tp38_cd10 | 3.68 | 1.0132 | oos_early_flatline_risk |

## Judgment(판정)

- `s91_v41_h3_risk475_gate08_sl210_tp38_cd10`: validation net(검증 순손익) 944.24, PF(수익 팩터) 1.54, DD(손실률) 21.30으로 가장 좋은 validation recovery(검증 회복) 단서다.
- `s91_v41_h3_risk475_gate08_sl205_tp40_cd10`: OOS net(표본외 순손익) 609.20과 OOS early(표본외 초반) 13.72가 제일 좋지만 validation net(검증 순손익)이 773.86으로 약하다.
- conclusion(결론): SL2.10(손절 2.10)은 validation recovery anchor(검증 회복 앵커)이고 TP4.0(익절 4.0)은 OOS early clue(표본외 초반 단서)다. Effect(효과): Stage93(93단계)는 `sl210_tp40`, `sl210_tp39`, `sl2075_tp40`만 좁게 본다.

## Evidence(근거)

- comparison_csv(비교 CSV): `stages/92_adapter_research__v41_sl205_net_recovery_followup_review/03_reviews/stage92_stage89_stage91_comparison.csv`
- segment_flags_csv(구간 플래그 CSV): `stages/92_adapter_research__v41_sl205_net_recovery_followup_review/03_reviews/stage92_stage91_segment_flags.csv`
- source_stage91_summary(원천 91단계 요약): `stages/91_adapter_research__v41_sl205_net_recovery_oos_early_repair/03_reviews/stage91_v41_sl205_net_recovery_oos_early_repair_summary.csv`
- source_stage91_segment(원천 91단계 구간): `stages/91_adapter_research__v41_sl205_net_recovery_oos_early_repair/03_reviews/stage91_segment_kpi_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).

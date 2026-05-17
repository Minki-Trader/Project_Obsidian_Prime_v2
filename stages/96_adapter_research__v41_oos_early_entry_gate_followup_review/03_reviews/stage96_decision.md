# Stage96 Decision(96단계 판정)

decision(판정): `continue_oos_early_lifecycle_repair_in_stage97`

Stage96(96단계)는 Stage95(95단계)의 entry gate/confidence threshold(진입 게이트/신뢰도 문턱) 수리를 review gate(검토 게이트)로만 판독했다.

Effect(효과): Stage95(95단계)의 실패/보존 근거를 다음 수리 축으로 넘기며, 같은 단계에서 끝없이 고치지 않는다.

## Evidence(근거)

- report(보고서): `stages/96_adapter_research__v41_oos_early_entry_gate_followup_review/03_reviews/stage96_oos_early_entry_gate_followup_review.md`
- comparison(비교): `stages/96_adapter_research__v41_oos_early_entry_gate_followup_review/03_reviews/stage96_stage93_stage95_comparison.csv`
- segment_flags(구간 플래그): `stages/96_adapter_research__v41_oos_early_entry_gate_followup_review/03_reviews/stage96_stage95_segment_flags.csv`
- source_summary(원천 요약): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_v41_oos_early_entry_gate_repair_summary.csv`
- source_segment_kpi(원천 구간 KPI): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_segment_kpi_summary.csv`
- source_gate_feature_summary(원천 게이트 피처 요약): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_gate_feature_summary.csv`
- external_verification_status(외부 검증 상태): `completed_existing_stage95_evidence_reviewed`
- pushed_commit_hash(푸시된 커밋 해시): `6c843b8b201da5e8aff17188d406a39c6c8c34f8`

## Why(이유)

- Gate09(게이트09)는 OOS PF(표본외 수익 팩터) `1.63`과 DD(손실률) `13.48%`는 좋아 보이지만 OOS early(표본외 초반)가 `-20.13 / PF 0.925`로 깨졌다.
- Gate10(게이트10)는 validation net(검증 순손익) `529.06`, OOS net(표본외 순손익) `370.92`로 둘 다 약해졌다.
- Thr056(문턱 0.56)은 Stage93 best(93단계 최선안)를 보존했지만 OOS early(표본외 초반) `13.02 / PF 1.046` 약점은 그대로다.

## Next(다음)

next_stage_or_branch(다음 단계/분기): `97_adapter_research__v41_oos_early_lifecycle_repair`

Stage97(97단계)는 `max_hold_bars(최대 보유 봉수)`와 same-direction re-entry cooldown(동방향 재진입 쿨다운)만 좁게 바꿔 OOS early(표본외 초반) 약점을 시험한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).

# Stage236 Side-Specific Follow-up Review(236단계 방향별 후속 검토)

- stage(단계): `236_adapter_research__stage235_side_specific_followup_review`
- run(실행): `run236A_stage236_stage235_side_specific_followup_review_v1`
- source_stage(원천 단계): `235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff`
- source_run(원천 실행): `run235A_stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1`
- source_stage235_evidence_commit(원천 235단계 근거 커밋): `2402dd0bb96c946c485253ae241f71eac61709be`
- source_stage235_hash_record_commit(원천 235단계 해시 기록 커밋): `deec8b78c2adb1baf0f239a82e750359be22de93`
- decision(판정): `open_stage237_bounded_reference_micro_threshold_recovery_after_context_side_failure_candidate_not_final`
- external_verification_status(외부 검증 상태): `review_only_source_stage235_mt5_reports_completed`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 설명)

Stage235(235단계)는 기준형 `s235_session_ref_h3_cd8`가 OOS(표본외)를 가장 잘 보존한다는 점을 확인했다. 하지만 34D(34D 기준) 대비 validation net(검증 순손익) `-35.44`, early PF(초반 수익요인) `-0.019452852`, mid PF(중반 수익요인) `-0.041963145`가 남았다.

cashopen45(현금장 초반 45분)는 early PF(초반 수익요인)만 좋아졌고, short block off(숏 차단 해제)는 크게 망가졌다.

Effect(효과): Stage237(237단계)은 새 큰 사냥이 아니라 기준형 주변의 작은 threshold(문턱값)/rank-confidence(순위 신뢰도) 조정만 본다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | class(분류) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) |
|---|---|---:|---:|---:|---:|---:|---:|
| s235_session_ref_h3_cd8 | oos_preserved_small_validation_gap_reference | 952.16 | 1.563704 | 1.541194 | 719.48 | 1.740000 | 9.2072 |
| s235_cashopen45_h3_cd8 | cashopen45_earlypf_clue_but_midpf_net_oos_damage | 797.87 | 1.598742 | 1.467070 | 525.69 | 1.610000 | 12.8843 |
| s235_session_ref_short_open_h3_cd8 | short_block_off_severe_damage | 510.56 | 1.174219 | 1.174422 | 470.51 | 1.290000 | 20.1984 |
| s235_cashopen45_short_open_h3_cd8 | cashopen45_short_open_severe_damage | 397.71 | 1.169795 | 1.151900 | 313.94 | 1.210000 | 22.6806 |

## Attribution(성과 원인 분해)

- reference_preserves_oos_but_misses_small_validation_gaps: 기준형은 OOS(표본외)를 보존하지만 34D(34D 기준) 대비 검증 순손익, 초반 PF(수익요인), 중반 PF(수익요인)가 조금 모자란다. Effect(효과): Stage237(237단계)은 기준형 주변의 작은 threshold(문턱값) 또는 rank-confidence(순위 신뢰도)만 시험한다.
- cashopen45_is_earlypf_clue_not_package: cashopen45(현금장 초반 45분)는 초반 PF(수익요인)만 좋아졌고 검증 순손익, 중반 PF(수익요인), OOS(표본외)를 훼손했다. Effect(효과): cashopen45(현금장 초반 45분)를 전체 package(묶음)로 반복하지 않는다.
- short_block_off_is_hard_failure: short block off(숏 차단 해제)는 거래 수를 늘렸지만 PF(수익요인), 순손익, DD(낙폭)를 크게 망가뜨렸다. Effect(효과): short block off(숏 차단 해제)는 Stage237(237단계)에서 재사용하지 않는다.
- mandatory_atr_and_model_risk_present_but_not_sufficient: 필수 기능은 살아 있지만 KPI(핵심 성과 지표) 통과 조건은 아니다. Effect(효과): Stage237(237단계)에서도 ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 고정 필수 조건으로 둔다.

## Route(다음 경로)

- open_stage237_bounded_reference_micro_threshold_recovery_after_context_side_failure_candidate_not_final: Stage237(237단계)을 열어 기준형 주변의 micro threshold(미세 문턱값)와 rank-confidence(순위 신뢰도)를 좁게 시험한다. Effect(효과): 검증 순손익과 초반/중반 PF(수익요인)의 작은 부족분을 회복하되 OOS(표본외) 기준 경계는 보존하는지 확인한다.
- do_not_repeat_failed_context_or_side_axes: cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 축을 반복하지 않는다. Effect(효과): Stage237(237단계)이 Stage235(235단계) 실패 축을 다시 흡수하지 않고 한 질문만 답하게 한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).

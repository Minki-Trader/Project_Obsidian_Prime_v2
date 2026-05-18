# Stage152 OOS DD/Mid Compression Report(152단계 표본외 낙폭/중반 압축 보고)

- stage(단계): `152_adapter_research__oos_dd_mid_compression_after_stage150_tradeoff`
- run(실행): `run152A_stage152_oos_dd_mid_compression_after_stage150_tradeoff_v1`
- source_stage151(원천 151단계): `151_adapter_research__stage150_validation_session_guard_followup_review`
- source_stage151_closeout_commit(원천 151단계 종료 커밋): `a7b45527cba4d171e4d6363d12e8f90410cc0b28`
- source_stage151_hash_record_commit(원천 151단계 해시 기록 커밋): `7cb669c9f17328c42658e903a03ec52f0cab85c0`
- repair_seed(수리 씨앗): `s150_session_mid_margin_restore_h3_cd5_sht54_lng52_risk035`
- oos_reference(표본외 참고): `s150_session_mid_replay_h3_cd5_sht54_lng52_risk035`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage153_oos_dd_mid_followup_review_due_to_damage_or_no_gain_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can Stage150 margin_restore(150단계 마진 복원)의 validation recovery(검증 회복)를 preserve(보존)하면서 OOS DD(표본외 낙폭)를 34D(34디) drawdown(낙폭) 기준 아래로 낮추고 OOS mid PF(표본외 중반 수익 팩터)를 34D(34디) PF(수익 팩터) 이상으로 올릴 수 있는가?

Effect(효과): 최종 순손익(net profit, 순손익) 하나가 아니라 validation/OOS(검증/표본외), drawdown(낙폭), mid segment(중반 구간)을 같이 본다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 낙폭) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS trades(표본외 거래 수) | OOS mid PF(표본외 중반 수익 팩터) | read(판독) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s152_margin_restore_session_narrow_h3_cd5_sht54_lng52_risk035 | 1.560000 | 1326.09 | 11.84 | 1.690000 | 988.20 | 18.94 | 188 | 1.487790 | needs_followup_or_repair |
| s152_margin_restore_margin_trim_h3_cd5_sht54_lng52_risk035 | 1.430000 | 1075.52 | 13.59 | 1.760000 | 1261.13 | 13.79 | 198 | 1.611944 | needs_followup_or_repair |
| s152_margin_restore_hold2_cd5_sht54_lng52_risk035 | 1.560000 | 666.35 | 12.63 | 1.570000 | 454.26 | 12.62 | 184 | 1.529998 | needs_followup_or_repair |
| s152_margin_restore_threshold_guard_h3_cd5_sht55_lng53_risk035 | 1.590000 | 1416.97 | 11.82 | 1.730000 | 1045.62 | 18.94 | 187 | 1.578473 | needs_followup_or_repair |

## Source Comparison(원천 비교)

- Stage150 margin_restore(150단계 마진 복원): validation PF(검증 수익 팩터) `1.590000`, OOS PF(표본외 수익 팩터) `1.730000`, OOS DD(표본외 낙폭) `18.94`, OOS mid PF(표본외 중반 수익 팩터) `1.578473376`.
- Stage150 OOS reference(150단계 표본외 참고): validation PF(검증 수익 팩터) `1.450000`, OOS DD(표본외 낙폭) `9.65`, OOS mid PF(표본외 중반 수익 팩터) `1.592742226`.

## Judgment(판정)

- best_adapter(최선 어댑터): `s152_margin_restore_margin_trim_h3_cd5_sht54_lng52_risk035`
- best_validation_pf(최선 검증 수익 팩터): `1.430000`
- best_oos_pf(최선 표본외 수익 팩터): `1.760000`
- best_oos_dd(최선 표본외 낙폭): `13.79`
- best_oos_mid_pf(최선 표본외 중반 수익 팩터): `1.611944327`

Stage152(152단계)는 research/development only(연구개발 전용)이다. Effect(효과): candidate(후보)가 좋아도 deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), production baseline(생산 기준선)을 주장하지 않는다.

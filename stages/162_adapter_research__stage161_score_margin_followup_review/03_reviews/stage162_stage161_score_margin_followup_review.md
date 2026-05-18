# Stage162 Stage161 Score Margin Follow-up Review(162단계 161단계 점수 마진 후속 검토)

- stage(단계): `162_adapter_research__stage161_score_margin_followup_review`
- run(실행): `run162A_stage162_stage161_score_margin_followup_review_v1`
- source_stage(원천 단계): `161_adapter_research__score_margin_or_side_filter_repair`
- source_closeout_commit(원천 종료 커밋): `b9f95b07366d9135d90df5a103070d98f1a0f1fd`
- source_hash_record_commit(원천 해시 기록 커밋): `a95c66c979f0d2a166a68aaf174c0d77b4aab013`
- decision(판정): `open_stage163_density_preserving_score_repair_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Answer(답)

Stage161(161단계)은 useful signal(유용한 신호)을 만들었다. Effect(효과): saturated score(포화 점수) 문제는 줄었고 threshold/filter(문턱값/필터)가 실제로 행 선택(row selection, 행 선택)을 바꿨다.

하지만 final research baseline(최종 연구 기준선)은 아니다. Effect(효과): shortprob(숏 확률 필터)는 PF(수익요인)는 좋지만 net/trade density(순손익/거래 밀도)가 너무 줄고 OOS early(표본외 초반) 구간이 손상됐다.

## KPI Read(KPI 판독)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | verdict(판정) |
|---|---:|---:|---:|---:|---:|---:|---|
| s161_cal050_both_risk0300_h3_cd5_sht54_lng52 | 1.550000 | 729.69 | 1.850000 | 722.94 | 9.55 | 1.801704 | validation_pf_below_34d_not_enough |
| s161_cal050_shortgate_risk0300_h3_cd5_sht54_lng52 | 1.530000 | 884.03 | 1.600000 | 603.83 | 13.34 | 1.729932 | validation_pf_below_34d_not_enough;oos_dd_above_34d_damage |
| s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52 | 1.820000 | 181.05 | 1.980000 | 171.25 | 8.24 | 0.978627 | pf_uplift_with_oos_early_segment_damage;pf_uplift_with_net_density_damage |

## Route(경로)

- decision(판정): `open_stage163_density_preserving_score_repair_candidate_not_final`
- next_stage(다음 단계): `163_adapter_research__stage161_density_preserving_score_repair`
- preserve(보존): `non_saturated_probability_binding_and_pf_uplift`
- repair(수리): `recover_density_and_oos_early_segment_without_reintroducing_oos_dd_damage`
- reject_as_final(최종 불가): `all_stage161_variants_candidate_not_final`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).

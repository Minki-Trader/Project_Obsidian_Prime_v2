# Stage160 Decision(160단계 판정)

- decision(판정): `open_stage161_score_margin_or_side_filter_repair_candidate_not_final`
- stage_status(단계 상태): `closed_audit_only_candidate_not_final`
- next_stage_or_branch(다음 단계/분기): `161_adapter_research__score_margin_or_side_filter_repair`
- next_run(다음 실행): `run161A_stage161_score_margin_or_side_filter_repair_v1`
- pushed_commit_hash(푸시 커밋 해시): `3805fd185dd669ebd674fe8df4cf19e504b07ee6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Why(이유)

Thresholds(문턱값)는 set file(설정 파일)에 들어갔다. 그러나 model probability(모델 확률)가 포화되어 0.52~0.55 threshold band(문턱값 구간)에 걸리는 방향 행이 없다.

Effect(효과): 다음 수리는 threshold-only(문턱값 단독)가 아니라 score margin(점수 마진), probability calibration(확률 보정), 또는 side filter(방향 필터) 축이어야 한다.

Stage160(160단계) closeout(종료)은 전체 목표 완료가 아니다.

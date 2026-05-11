# Existing Model Density Audit(기존 모델 거래 밀도 감사)

- run_id(실행 ID): `run50A_existing_model_density_audit_v1`
- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- evidence_scope(근거 범위): existing evidence only(기존 근거 전용)
- output_table(출력 표): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50A/results/existing_model_density_audit.csv`

## Finding(발견)

기존 v2 후보 중 Stage56(56단계)의 일 평균 `5~10`건 목표에 이미 도달한 base engine(기본 엔진)은 없다.

현재 가장 두꺼운 기존 근거는 QDA raw covariance(이차 판별 분석 원천 공분산) `run08A`다. 그러나 validation(검증) profit factor(수익 팩터)는 `1.03`이고 OOS(표본외)는 `1.15`라서 품질이 약하다.

LogReg(로지스틱 회귀) full threshold(전체 임계값) `run01A`는 validation(검증) `233` trades(거래), OOS(표본외) `200` trades(거래)로 QDA(이차 판별 분석) 다음의 reference density(참고 밀도)를 가진다.

CatBoost(캣부스트) `run12A`는 validation/OOS(검증/표본외) 모두 양수이고 profit factor(수익 팩터)가 좋지만 거래 밀도(trade density, 거래 밀도)는 더 얇다.

Stage55(55단계) `rfp02`는 user-review candidate(사용자 검토 후보)로 보존되지만 filter/adapter(필터/어댑터) 성격이라 Stage56(56단계) base engine(기본 엔진)으로 쓰지 않는다.

## Design Consequence(설계 결과)

Stage56(56단계)은 새 dense version(고밀도 버전)을 실제 MT5 closed trades(닫힌 거래) 기준으로 다시 만들어야 한다.

우선순위(priority, 우선순위):

1. LogReg dense version(로지스틱 회귀 고밀도 버전)
2. QDA dense version(이차 판별 분석 고밀도 버전)
3. CatBoost lower-threshold dense version(캣부스트 낮은 임계값 고밀도 버전)
4. LightGBM dense comparison version(라이트GBM 고밀도 비교 버전), optional(선택)

## Judgment(판정)

`baseline_candidate_only(기준선 후보 전용)`도 아직 아니다. 이 audit(감사)는 run50B/run50C/run50D(실행 50B/50C/50D) 설계를 위한 source authority(원천 권위) 정리다.

claim_boundary(주장 경계): `existing_evidence_density_audit_only_no_research_baseline_no_live_readiness_no_runtime_authority_no_operating_promotion`

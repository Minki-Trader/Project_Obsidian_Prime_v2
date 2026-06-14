# stage_frontier_43__short_pf_edge_trade_shape_source_pivot_after_f42_timing_negative

## Hypothesis(가설)
Entry-known trade-shape proxy source(진입 시점 거래 형태 대리 원천)가 weak short PF(약한 숏 수익 팩터)를 설명한다면, source selection criterion(원천 선택 기준)을 train-only closed-bar shape proxy(학습 전용 닫힌 봉 형태 대리값)로 바꾸면 PF/DD/density(수익 팩터/손실폭/밀도)를 동시에 개선할 수 있다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F42 best row(최상 행)는 reference-only(참조 전용), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서).
- changed_variables(변경 변수): source ranking/composition(원천 순위/구성)을 entry-known trade-shape proxy(진입시점 거래 형태 대리값)로 변경.
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 source construction(원천 구성)에 쓰거나 session-clock(세션 시계)을 primary lever(주 레버)로 쓰는 경우.
- stop_conditions(중지 조건): seed/runtime candidate(씨앗/런타임 후보) 발생 또는 capped repair(상한 수리) 종료.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): accepted
- accepted_after_local_verification(로컬 검증 후 수용): True
- guardrail_seen(보호선 확인): True

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- feature_hash_matches_contract(피처 해시 계약 일치): True
- required_splits_present(필수 분할 존재): True
- source_rows(원천 행): 168

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.

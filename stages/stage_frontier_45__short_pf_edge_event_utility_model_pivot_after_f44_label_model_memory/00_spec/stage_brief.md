# stage_frontier_45__short_pf_edge_event_utility_model_pivot_after_f44_label_model_memory

## Hypothesis(가설)
Train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 F44 continuous utility regression(연속 효용 회귀)보다 고보상/저불리 경로 이벤트(high-payoff/low-adverse path event, 고보상/저불리 경로 이벤트)를 더 잘 분리하는지 시험한다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F44 best row(최상 행)는 reference-only scout clue(참조 전용 탐색 단서), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): event label(이벤트 라벨), classifier family(분류 모델 계열), train-only event probability threshold(학습 전용 이벤트 확률 임계값).
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank(라벨/모델/임계값/손익절/순위)에 쓰는 경우.
- stop_conditions(중지 조건): seed/runtime candidate(씨앗/런타임 후보) 발생 또는 capped repair(상한 수리) 종료.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): accepted_stage_open_train_split_only_event_lock
- accepted_after_local_verification(로컬 검증 후 수용): True
- guardrail_seen(보호선 확인): True

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_splits_present(필수 분할 존재): True
- short_valid_rows(숏 경로 유효 행): 46650

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.

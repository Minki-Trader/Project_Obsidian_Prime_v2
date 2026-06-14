# stage_frontier_46__short_pf_edge_event_sequence_context_pivot_after_f45_event_classifier_memory

## Hypothesis(가설)
Train-fitted frozen short event scorer(학습 적합 고정 숏 이벤트 채점기)의 lagged sequence context(지연 순서 문맥)가 F45 same-bar event classifier(동일 봉 이벤트 분류기)보다 PF/DD/density(수익 팩터/손실폭/밀도)를 더 잘 동시에 분리하는지 시험한다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F45 best and nonwinner rows(최상/비승자 행)는 reference-only scout clue(참조 전용 탐색 단서), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): lagged event-score context(지연 이벤트 점수 문맥), fully-known past outcome tape(완전히 알려진 과거 결과 테이프), sequence-context model family(순서 문맥 모델 계열), train-only sequence probability threshold(학습 전용 순서 확률 임계값).
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank/repair(라벨/모델/임계값/손익절/순위/수리)에 쓰거나, horizon+1 embargo(예측수평선+1 유예)보다 최신 결과 라벨을 현재 feature(피처)로 쓰는 경우.
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

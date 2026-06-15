# stage_frontier_49__short_pf_edge_forward_floor_state_machine_after_f48_event_risk_memory

## Hypothesis(가설)
F48 preserved clue(보존 단서)의 loss-contained event(손실 제한 이벤트)에 train-only forward floor state machine(학습 전용 전진 하한 상태기계)을 덧씌우면 PF/DD/density(수익 팩터/손실폭/밀도)를 더 잘 동시에 분리하는지 시험한다.

Novelty line(신규성 문장): forward floor state machine(전진 하한 상태기계)은 horizon+1 embargo(예측수평+1 유예)를 지난 known outcome(확정 결과)만 쓰며, F48 static state gate(정적 상태 게이트)와 F47 percentile risk-budget sweep(47전선 분위수 위험 예산 훑기)을 반복하지 않는다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F48 best and closest nonwinner rows(F48 최상/가장 가까운 비승자 행)는 reference-only scout clue(참조 전용 탐색 단서), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): bars-since-known-bad/good state(확정 나쁜/좋은 이벤트 이후 봉 수 상태), rolling event-balance floor(굴러가는 이벤트 균형 하한), fixed volatility/crowding caps(고정 변동성/밀집 상한).
- initial_lock(초기 잠금): first proxy(첫 프록시)는 F48 event/model/context/score/SLTP(이벤트/모델/문맥/점수/손익절)를 reference-only(참조 전용)로 고정하고 forward floor state gate(전진 하한 상태 게이트)만 바꾼다.
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank/risk budget/repair(라벨/모델/임계값/손익절/순위/위험 예산/수리)에 쓰거나, horizon+1 embargo(예측수평선+1 유예)보다 최신 결과 라벨을 현재 feature(피처)로 쓰는 경우.
- stop_conditions(중지 조건): seed/runtime candidate(씨앗/런타임 후보) 발생 또는 capped repair(상한 수리) 종료.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): accepted_stage_open_train_split_only_forward_floor_state_machine_lock
- accepted_after_local_verification(로컬 검증 후 수용): True
- guardrail_seen(보호선 확인): True

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_splits_present(필수 분할 존재): True
- short_valid_rows(숏 경로 유효 행): 46650

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.

# stage_frontier_48__short_pf_edge_event_rarity_risk_sizing_after_f47_state_budget_memory

## Hypothesis(가설)
F47 preserved clue(보존 단서)의 loss-contained event(손실 제한 이벤트)에 train-only fixed event rarity risk sizing(학습 전용 고정 이벤트 희소성/위험 크기 조절)을 덧씌우면 PF/DD/density(수익 팩터/손실폭/밀도)를 더 잘 동시에 분리하는지 시험한다.

Novelty line(신규성 문장): state gates(상태 게이트)는 fixed non-percentile entry-known thresholds(고정 비분위수 진입시점 임계값)만 쓰며, F47 percentile risk-budget sweep(47전선 분위수 위험 예산 훑기)을 반복하지 않는다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부 판정.
- comparison_baseline(비교 기준): F47 best and preserved nonwinner rows(F47 최상/보존 비승자 행)는 reference-only scout clue(참조 전용 탐색 단서), baseline/winner(기준선/승자) 아님.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): event rarity(이벤트 희소성), fixed squeeze/cooldown/volatility/high-count state gates(고정 압축/휴식/변동성/고점수 밀집 상태 게이트), train-only risk sizing(학습 전용 위험 크기 조절).
- initial_lock(초기 잠금): first proxy(첫 프록시)는 F47 best event/model/context/score/SLTP(이벤트/모델/문맥/점수/손익절)를 reference-only(참조 전용)로 고정하고 fixed state gate(고정 상태 게이트)만 바꾼다.
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank/risk budget/repair(라벨/모델/임계값/손익절/순위/위험 예산/수리)에 쓰거나, horizon+1 embargo(예측수평선+1 유예)보다 최신 결과 라벨을 현재 feature(피처)로 쓰는 경우.
- stop_conditions(중지 조건): seed/runtime candidate(씨앗/런타임 후보) 발생 또는 capped repair(상한 수리) 종료.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): accepted_stage_open_train_split_only_nonpercentile_state_gate_lock
- accepted_after_local_verification(로컬 검증 후 수용): True
- guardrail_seen(보호선 확인): True

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_splits_present(필수 분할 존재): True
- short_valid_rows(숏 경로 유효 행): 46650

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.

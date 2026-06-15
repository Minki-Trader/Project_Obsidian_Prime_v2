# stage_frontier_50__short_pf_edge_loss_floor_regime_transfer_after_f49_state_machine_memory

## Hypothesis(가설)
F50 tests train-only loss-floor regime transfer(학습 전용 손실 하한 체제 전이) as a new input surface(입력 표면). F49 is reference-only(참조 전용) negative memory(부정 기억), not winner/baseline(승자/기준선 아님).

Novelty line(신규성 문장): causal loss-floor tape(인과 손실 하한 테이프) and MFE/MAE decay memory(최대유리/최대불리 감쇠 기억) enter the event surface/model context(이벤트 표면/모델 문맥). Hygiene gates(위생 게이트)는 최소화한다.

## Experiment Design(실험 설계)
- decision_use(결정 용도): scout/seed/runtime candidate(탐색/씨앗/런타임 후보) 여부를 판정한다.
- control_variables(고정 변수): US100 M5, frozen split(고정 분할), short-only(숏 전용), closed-bar 58 feature order(닫힌 봉 58 피처 순서), first-hit SL/TP path proxy(첫 터치 손익절 경로 프록시).
- changed_variables(변경 변수): loss-floor transfer event labels(손실 하한 전이 이벤트 라벨), causal outcome-memory context(인과 결과 기억 문맥), MFE/MAE decay features(최대유리/최대불리 감쇠 피처).
- invalid_conditions(무효 조건): validation/OOS(검증/표본외)를 label/model/threshold/SLTP/rank(라벨/모델/임계값/손익절/순위)에 쓰거나 horizon+1 embargo(예측수평+1 유예)보다 최신 결과를 feature(피처)에 쓰는 경우.
- repair_cap(수리 상한): repair(수리)는 loss-floor/outcome-memory window(손실 하한/결과 기억 창)와 event definition(이벤트 정의)만 좁게 바꾼다.

## Grok Stage-Open Review(그록 단계 개방 검토)
- classification(분류): accepted_stage_open_train_split_only_loss_floor_regime_transfer_lock
- accepted_after_local_verification(로컬 검증 후 수용): True
- guardrail_seen(보호선 확인): True

## Local Checks(로컬 점검)
- feature_hash(피처 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- required_splits_present(필수 분할 존재): True
- short_valid_rows(숏 경로 유효 행): 46650

## Claim Boundary(주장 경계)
No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) is claimed.

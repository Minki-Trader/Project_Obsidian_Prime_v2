# F96 Runtime Learning Probe Backfill Closeout

## Conclusion

F96(전선96)은 success rewrite(성공 재작성)가 아니라 runtime learning backfill(런타임 학습 보강)로만 처리했다. 기존 candidate_count(후보 수)는 0이고, 이번 작업은 sparse score_sample repair(희소 점수 샘플 수리) 뒤 MT5 Strategy Tester(전략 테스터) observation(관찰)을 남긴 것이다.

## What Changed

- Added `stage_pipelines/stage_frontier_96/frontier96_runtime_learning_probe_backfill.py`.
- Materialized(물질화) `ridge_signed_utility_edge_full58_q88` side signal(방향 신호) into one-feature EBM table(단일 피처 EBM 표).
- Ran standard validation_is(검증 내부) and oos(표본외) MT5 probe(탐침) through `/portable(포터블)`.
- Recorded Task Force micro consult(태스크포스 소형 상담) in `actual_subagent_calls.json`.

## What Gates Passed

- runtime_learning_probe_decision_gate(런타임 학습 탐침 결정 게이트): pass.
- mt5_runtime_probe_contract_audit(MT5 런타임 탐침 계약 감사): pass.
- test_gate(테스트 게이트): pass, 14 pytest(파이테스트) tests passed.
- codex_task_force_review_packet(태스크포스 검토 묶음): pass as micro consult(소형 상담), not formal reviewed pass(정식 검토 통과 아님).

## MT5 Evidence

- validation_is(검증 내부): net_profit(순손익) 3.32, PF(수익 팩터) 1.01, max_drawdown(최대 손실폭) 44.58%, trade_count(거래 수) 29, win_rate(승률) 48.28%.
- oos(표본외): net_profit(순손익) -493.64, PF(수익 팩터) 0.42, max_drawdown(최대 손실폭) 99.18%, trade_count(거래 수) 26, win_rate(승률) 46.15%.
- validation_is report hash(검증 내부 보고서 해시): `30c43c66a7775f2c4e91e6cd5fc05b6b9985480337e378721c7e62067bdefe8d`.
- oos report hash(표본외 보고서 해시): `d78e6e8cc52818cc596a199d4215e1ba28802209d0db1458b61f2511563abe34`.

## What Gates Were Not Applicable

- runtime_evidence_gate(런타임 근거 게이트)는 runtime_authority/economics_pass/materialization-ready/handoff-complete(런타임 권위/경제성 통과/물질화 준비/인계 완료) 주장에는 적용되지만, 이 packet(묶음)은 그런 주장을 하지 않는다.

## What Is Still Not Enforced

- score_sample.csv(점수 샘플)는 full signal surface(전체 신호 표면)가 아니라 sparse sample(희소 표본)이다.
- Task Force advice(태스크포스 조언)에 따라 full signal surface regeneration(전체 신호 표면 재생성)은 next repair option(다음 수리 선택지)로 남긴다.
- F96 closeout(F96 마감)은 positive(긍정)로 바꾸지 않는다.

## Allowed Claims

- runtime_learning_probe_decision_recorded(런타임 학습 탐침 결정 기록됨)
- f96_repair_attempt_recorded(F96 수리 시도 기록됨)
- runtime_probe_observation(런타임 탐침 관찰)
- inconclusive_runtime_learning_record(불충분 런타임 학습 기록)

## Forbidden Claims

- Goal Achieve(목표 달성)
- operating_promotion(운영 승격)
- runtime_authority(런타임 권위)
- live_readiness(실거래 준비)
- selected_baseline(선택 기준선)
- economics_pass(경제성 통과)
- materialization_ready(물질화 준비)
- handoff_complete(인계 완료)

## Next Hardening Step

Next reverse-order target(다음 역순 대상)은 F95(전선95)이다. F96에서 full signal surface regeneration(전체 신호 표면 재생성)을 먼저 보강할지도 queue(대기열)에 남긴다.

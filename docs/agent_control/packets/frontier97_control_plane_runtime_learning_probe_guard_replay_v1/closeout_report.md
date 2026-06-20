# F97 Runtime Learning Probe Guard Replay Closeout

## Conclusion

F97(전선97)은 success rewrite(성공 재작성)가 아니라 regression fixture(회귀 검증 예시)로만 사용했다. The runtime_learning_probe_decision_gate(런타임 학습 탐침 결정 게이트)는 proxy_bad/candidate_gate_failed/not_strong_candidate/cost_expensive(프록시 부진/후보 게이트 실패/강한 후보 아님/비용) 기반 MT5 not-run(MT5 미실행)을 차단한다.

F97 replay(재연)는 strong_candidate_count(강한 후보 수) 0, runtime_learning_probe_candidate_count(런타임 학습 탐침 후보 수) 1로 `run_probe(탐침 실행)`를 선택했고, repair01(수리01)에서 score_sample.csv(점수 샘플)를 one-feature EBM table(1개 피처 EBM 표)과 MT5 feature matrix(MT5 피처 행렬)로 materialize(물질화)했다.

## What changed

- Added `foundation/control_plane/runtime_learning_probe_decision_gate.py`.
- Added tests in `tests/test_runtime_learning_probe_decision_gate.py` and schema lint coverage in `tests/test_work_packet_schema_lint.py`.
- Wired `runtime_learning_probe(런타임 학습 탐침)` into work packet schema lint(작업 묶음 스키마 점검), closeout gate(마감 게이트), work family registry(작업군 등록부), skill receipt schema(스킬 영수증 스키마), runtime/result/backtest skills(런타임/결과/백테스트 스킬), AGENTS.md(요원 지침), Task Force registry(태스크포스 등록부), and agent_08(런타임 요원).
- Added `stage_pipelines/stage_frontier_97/frontier97_runtime_learning_probe_guard_replay.py` for the F97 replay.

## What gates passed

- work_packet_schema_lint(작업 묶음 스키마 점검): pass.
- runtime_learning_probe_decision_gate(런타임 학습 탐침 결정 게이트): negative fixture blocked, repair fixture blocked, positive fixture passed, actual F97 decision passed.
- test_gate(테스트 게이트): targeted pytest(대상 파이테스트) passed.
- skill_receipt_schema_lint(스킬 영수증 스키마 점검): pass.
- codex_task_force_review_packet(태스크포스 검토 묶음): historical pass in the original packet, and current follow-up micro consult(소형 상담) recorded in `actual_subagent_calls.json`.
- mt5_runtime_probe_contract_audit(MT5 런타임 탐침 계약 감사): pass for standard validation_is(검증 내부) + oos(표본외), `/portable(포터블)` execution, and completed Strategy Tester reports(완료 전략 테스터 보고서).

F97 MT5 runtime learning attempt(런타임 학습 시도) evidence:

- Compile(컴파일): completed.
- Terminal run(터미널 실행): completed with returncode 0 for both validation_is and oos, command includes `/portable(포터블)`.
- Standard period(표준 기간): validation_is `2025.01.02 -> 2025.10.01`; oos `2025.10.01 -> 2026.06.18`.
- Validation telemetry/summary(검증 내부 텔레메트리/요약): summary hash `9be10cd251c9adad1bd19f777a34f54f8f544c0b4bce56de6f31ec6007e79ca7`, telemetry hash `679d55023481279a44382745a9ed5209b390b8549e72f3d11acc9e0a33ea5be3`.
- OOS telemetry/summary(표본외 텔레메트리/요약): summary hash `684ceec0fb1f65f19e88b5893f41cc728966c243fa75bd5cf3f07d36da4a27ea`, telemetry hash `f47e36ce87d28c24e57df31c1fc1b7d00dd2305a72925f3e31c876d2c0725ed1`.
- Validation Strategy Tester report(검증 내부 전략 테스터 보고서): completed, hash `f5ba34347937a97782c3a83d79426dc9e9b139929dccf292609b8e92b8cf6cf8`.
- OOS Strategy Tester report(표본외 전략 테스터 보고서): completed, hash `2cb8c1b3293f3af32d66312104dafe421e889c87deb4e72ac42013e78daff1fe`.
- Validation economics read(검증 내부 경제성 판독): net_profit(순손익) -311.24, PF(수익 팩터) 0.30, max_drawdown(최대 손실폭) 82.80%, trade_count(거래 수) 44, win_rate(승률) 27.27%.
- OOS economics read(표본외 경제성 판독): net_profit(순손익) -494.04, PF(수익 팩터) 0.27, max_drawdown(최대 손실폭) 99.11%, trade_count(거래 수) 37, win_rate(승률) 32.43%.
- Runtime judgment(런타임 판정): `negative_runtime_learning_probe_observation_completed_no_economics_pass`.

## What gates were not applicable

- runtime_evidence_gate(런타임 근거 게이트): applicable only to runtime_authority/economics_pass/materialization-ready/handoff-complete claims(런타임 권위/경제성 통과/물질화 준비/인계 완료 주장). The standard runtime observation(표준 런타임 관찰) exists, but economics(경제성)가 negative(부정)이므로 those stronger claims remain forbidden(금지)이다.

## What is still not enforced

- F97 source surface(원천 표면)는 still sparse sample(여전히 희소 표본)이다: validation_is sample rows(검증 내부 표본 행) 240, oos sample rows(표본외 표본 행) 240.
- Economics KPIs(경제성 핵심 지표)는 parsed(파싱됨)됐지만 negative(부정)이므로 promotion evidence(승격 근거)가 아니다.
- Windows long path(윈도우 긴 경로) check(점검)는 `long_path_read_recheck.json`에 기록했다. 일반 path read(경로 읽기)가 실패해도 `io_path(입출력 경로)`로 재확인하기 전에는 missing(누락)으로 판단하지 않는다.
- This packet(묶음)은 F97 closeout(F97 마감)을 positive(긍정)로 바꾸지 않는다.

## Allowed claims

- runtime_learning_probe_decision_recorded(런타임 학습 탐침 결정 기록됨)
- runtime_learning_guard_hardened(런타임 학습 보호장치 강화됨)
- f97_replay_attempt_recorded(F97 재연 시도 기록됨)
- runtime_probe_observation(런타임 탐침 관찰)
- negative_runtime_learning_record(부정 런타임 학습 기록)

## Forbidden claims

- Goal Achieve(목표 달성)
- operating_promotion(운영 승격)
- runtime_authority(런타임 권위)
- live_readiness(실거래 준비)
- selected_baseline(선택 기준선)
- economics_pass(경제성 통과)
- materialization_ready(물질화 준비)
- handoff_complete(인계 완료)

## Next hardening step

Use `frontier_runtime_probe_backfill_queue_latest.json` for the next reverse-order target(역순 대상). Current recommendation(현재 추천)은 F96 repair-first(수리 우선) runtime learning probe(런타임 학습 탐침)이다.

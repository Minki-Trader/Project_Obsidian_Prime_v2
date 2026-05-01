# stage12_run03l_recency_weighted_single_v1 Closeout Report(마감 보고서)

## Conclusion(결론)

RUN03L(실행 03L)은 recency-weighted ExtraTrees(최근성 가중 엑스트라 트리)를 변형 없이 한 run(실행)으로 시험했다.

효과(effect, 효과): sample_weight(표본 가중치) 축이 계속 팔 가치가 있는지 Python WFO(파이썬 워크포워드 최적화)와 MT5(메타트레이더5) fold07(접힘 7)로 동시에 남겼다.

## What changed(무엇이 바뀌었나)

- recent 12 months(최근 12개월) 학습 행에 weight(가중치) `3.0`, older rows(이전 행)에 `1.0`을 줬다.
- Tier A(티어 A), Tier B(티어 B), Tier A+B(티어 A+B)를 모두 기록했다.
- fold07(접힘 7) MT5(메타트레이더5) validation/test(검증/시험) 6 attempts(시도)를 실행했다.

## What gates passed(통과한 게이트)

runtime_evidence_gate(런타임 근거 게이트), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_lint(스킬 영수증 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 가드)를 확인한다.

## What gates were not applicable(해당 없음 게이트)

없음. MT5(메타트레이더5) runtime evidence(런타임 근거)를 직접 실행했다.

## What is still not enforced(아직 강제되지 않은 것)

full seven-fold MT5 WFO(전체 7접힘 메타트레이더5 워크포워드 최적화)는 실행하지 않았다. 이 packet(묶음)은 one-run probe(단일 실행 탐침)다.

## Allowed claims(허용 주장)

`runtime_probe_recency_weight_completed`, `single_run_completed`.

## Forbidden claims(금지 주장)

`alpha_quality(알파 품질)`, `promotion_candidate(승격 후보)`, `operating_promotion(운영 승격)`, `runtime_authority(런타임 권위)`.

## Next hardening step(다음 경화 단계)

결과가 강하면 broader recency weighting sweep(더 넓은 최근성 가중 탐색)을 설계한다. 약하면 failure memory(실패 기억)로 남기고 다른 축으로 간다.

Summary status(요약 상태): `completed` / external verification status(외부 검증 상태): `completed`.

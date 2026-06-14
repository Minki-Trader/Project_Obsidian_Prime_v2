# Frontier17 Experiment Design(전선17 실험 설계)

- primary_family(주 작업군): `experiment_design(실험 설계)`
- primary_skill(주 스킬): `obsidian-experiment-design`
- support_skills(보조 스킬): `obsidian-data-integrity`, `obsidian-model-validation`, `obsidian-exploration-mandate`, `obsidian-artifact-lineage`, `obsidian-result-judgment`, `obsidian-grok-collaboration`
- required_gates(필수 게이트): `work_packet_schema_lint`, `external_review_packet`, `definition_lock_gate`, `required_gate_coverage_audit`, `final_claim_guard`

Hypothesis(가설): Train-only loss-cluster firewall(학습 전용 손실 군집 방화벽) and profit-persistence trigger(수익 지속성 트리거)를 AND gate(동시 충족 게이트)로 묶어, 빈도(density, 빈도)를 먼저 강제하지 않고 손실폭(drawdown, 손실폭) 위험이 낮은 지속 상태만 진입한다.

Changed variable(변경 변수): validation philosophy(검증 철학) and decision structure(결정 구조).

Success criteria(성공 기준):
- scout clue(탐색 단서): validation/OOS net positive, PF >= 1.2, density 5~10/day, DD <= 15%, worst subperiod DD <= 25%, ONNX parity pass(검증/표본밖 순수익 양수, 수익 팩터 1.2 이상, 일 5~10회, 손실폭 15% 이하, 최악 하위기간 손실폭 25% 이하, ONNX 동등성 통과)
- seed surface(씨앗 표면): DD/smoothness improves versus F16B/D, density remains 3~10/day, PF axis does not regress(손실폭/매끄러움이 F16B/D보다 개선되고 빈도는 일 3~10회, 수익 팩터 축 후퇴 없음)
- runtime probe observation(런타임 탐침 관찰): one narrow MT5 probe before closeout or exact blocked reason(마감 전 좁은 MT5 탐침 1회 또는 정확한 차단 사유)

Failure criteria(실패 기준): density only improves while PF/DD/smoothness fails(빈도만 개선되고 수익 팩터/손실폭/매끄러움 실패), firewall suppresses trades below 3/day(방화벽이 거래를 일 3회 미만으로 억제), train-only hazard thresholds do not transfer to validation/OOS(학습 전용 위험 임계값이 검증/표본밖으로 전이되지 않음), MT5 runtime probe shows material runtime collapse(MT5 런타임 탐침에서 중대한 런타임 붕괴)

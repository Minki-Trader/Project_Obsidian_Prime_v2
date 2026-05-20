# 267_adapter_research__baseline_candidate_racing_protocol

Stage267(267단계)는 five-candidate Baseline pool(다섯 후보 기준군)을 R&D racing(연구개발 경주)의 시작점으로 고정하는 protocol(규약) 단계다.
Effect(효과): Stage266(266단계)의 single-candidate repair(단일 후보 수리)를 그대로 이어가지 않고, 후보군 전체를 같은 검증 표면(validation surface, 검증 표면)에서 비교한다.

## Bounded Question(경계 질문)

Can the current Baseline candidate pool(현재 기준 후보군)을 같은 조건에서 다시 재검증하고, 누가 덜 깨지고, 누가 더 넓은 조건에서 살아남으며, 누가 Adapter development(어댑터 개발)로 확장할 가치가 있는지 판정할 수 있는가?

## Candidate Pool(후보군)

- `s264_allow_inner_high_quarter`: challenger(도전자) 후보.
- `s264_lowrank_control`: defensive control(방어 기준) 후보.
- `s262_lowrank_inner_half_filter`: validation-heavy(검증 중심) 후보.
- `s264_allow_inner_all_oos_anchor`: OOS anchor(표본외 앵커) 후보.
- `s258_short_tight_control`: stress challenger(압박 도전자) 후보.

## Minimum Research Surface(최소 연구 표면)

- extended period test(확장 기간 시험), including 2024(2024년) when data and tooling allow it.
- feature/category ablation(피처/범주 제거).
- similar feature replacement(유사 피처 대체).
- feature engineering(피처 엔지니어링) with broad structural variants(넓은 구조 변형), not micro-tuning(미세 조정) only.
- day/session/hour/month KPI(요일/세션/시간/월 핵심 성과 지표).
- balance/equity curve review(잔액/평가금 곡선 검토).
- trade count and trade quality(거래 수와 거래 품질) review.
- failure memory(실패 기억) for every failed branch(실패 분기).

## Stop Conditions(중단 조건)

- If a candidate breaks in extended period(확장 기간), feature ablation(피처 제거), similar replacement(유사 대체), or equity curve(평가금 곡선), downgrade(하향) it instead of repairing it indefinitely.
- If a repair branch(수리 분기) needs more than two stages(두 단계), close or pivot(마감 또는 전환) it before continuing.
- If evidence is missing, mark missing_required(필수 누락), blocked(차단), or out_of_scope_by_claim(주장 범위 밖).
- Do not proceed to ONNX(ONNX) review until the Goal Achieve gate(목표 달성 게이트) has strong evidence.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

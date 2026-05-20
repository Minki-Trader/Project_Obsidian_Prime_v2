# Stage266 Superseded And Stage267 Opened(266단계 대체 및 267단계 개방)

- date(날짜): `2026-05-20`
- action(행동): Stage266(266단계) `266_adapter_research__late_segment_stability_repair_after_stage265_review`를 run execution(실행 수행) 전 planning_superseded(계획 대체)로 낮추고, Stage267(267단계) `267_adapter_research__baseline_candidate_racing_protocol`을 연다.
- effect(효과): `s264_allow_inner_high_quarter` 단일 후보 late segment repair(후반 구간 수리) 병목을 멈추고, 다섯 Baseline candidate(기준 후보)를 R&D racing(연구개발 경주) 기준 후보군으로 다룬다.
- source_decision(원천 판정): Stage265(265단계) `open_stage266_bounded_late_segment_stability_repair_after_stage265_review_candidate_not_final`
- superseded_stage(대체된 단계): `266_adapter_research__late_segment_stability_repair_after_stage265_review`
- opened_stage(개방 단계): `267_adapter_research__baseline_candidate_racing_protocol`
- current_run(현재 실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`
- evidence_boundary(근거 경계): Stage266(266단계)는 planning only(계획 전용)이고 result judgment(결과 판정)는 없다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Baseline Candidate Pool(기준 후보군)

- `s264_allow_inner_high_quarter`: challenger(도전자) 후보.
- `s264_lowrank_control`: defensive control(방어 기준) 후보.
- `s262_lowrank_inner_half_filter`: validation-heavy(검증 중심) 후보.
- `s264_allow_inner_all_oos_anchor`: OOS anchor(표본외 앵커) 후보.
- `s258_short_tight_control`: stress challenger(압박 도전자) 후보.

## Stage267 Direction(267단계 방향)

Stage267(267단계)는 best number(최고 숫자) 선정 단계가 아니다.
Effect(효과): 누가 덜 깨지는지, 넓은 기간에서 버티는지, feature/category ablation(피처/범주 제거), similar feature replacement(유사 피처 대체), feature engineering(피처 엔지니어링), time-slice KPI(시간 구간 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질)를 통과해 Adapter development(어댑터 개발) 가치가 있는지 본다.

ONNX(ONNX) 검토는 마지막이다.
Effect(효과): 단순 개선, 한두 KPI(핵심 성과 지표) 개선, 이전 stage(단계) 대비 개선만으로 ONNX화하지 않는다.

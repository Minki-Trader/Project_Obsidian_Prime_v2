# Frontier61 Pre-MT5 Review(전선61 MT5 전 검토)

Current truth(현재 진실):
- Stage(단계): `stage_frontier_61__non_long_axis_pf_source_after_friction_memory`.
- Hypothesis(가설): a 3-class side allocation model(3분류 방향 배분 모델) predicts short/flat/long(숏/무거래/롱) after F53-F60 single-axis repairs failed MT5 PF(수익 팩터).
- Stage-open Grok review(단계 개방 그록 검토): `needs_local_verification`; Codex completed local checks before proxy materialization(프록시 물질화 전 로컬 검증 완료).
- Failure-mode audit(실패 모드 감사): F53-F59 had completed MT5 rows and mostly `signal_diff=0`, so repeated weakness is treated as alpha/economics failure(알파/경제성 실패) more than handoff failure(인계 실패). F60 is separate entry-admission suppression(진입 억제) memory.
- Feature contract(피처 계약): 58 features(피처), hash `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`.

Frozen proxy candidate(동결 프록시 후보):
- candidate_id(후보 ID): `f61b_side_alloc_t38_m2_h4`
- model_id(모델 ID): `frontier61_side_allocation_extratrees_d7_l120_v1`
- decision mode(결정 모드): `edge_margin`
- thresholds(임계값): short=0.38, long=0.38, min_margin=0.02
- runtime envelope(런타임 봉투): ATR SL/TP enabled(ATR 손절/익절 사용), max_hold=4, close_on_flat=false, entry_transition_only=false
- ONNX parity(온엑스 동등성): passed=true, max_abs_diff=1.4164e-07, rows=1024

Proxy KPI(프록시 KPI):
- train(학습): PF=1.2999, DD=4.6815%, trades=1753, trades/day=3.0593
- validation(검증): PF=0.9798, DD=5.7556%, trades=877, trades/day=4.7923
- OOS(표본외): PF=1.1169, DD=3.0752%, trades=626, trades/day=4.7786
- forward_min_pf(전진 최소 PF)=0.9798
- forward_max_dd(전진 최대 DD)=5.7556%
- forward_min_density(전진 최소 밀도)=4.7786/day

Pre-registered boundary(사전 등록 경계):
- Only one MT5 runtime probe candidate(런타임 탐침 후보 1개) will be run before repair or closeout.
- This is runtime_probe_observation(런타임 탐침 관찰) only.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claim.
- Tier B and combined(티어 B/합산)은 stage-open에서 `missing_required`로 기록했다.

Question(질문):
Given the proxy is close but below target density and validation PF is slightly under 1, should Codex proceed with this mandatory MT5 runtime probe as exploration-only runtime_probe_observation(탐색 전용 런타임 탐침 관찰), or should it close before MT5 as negative/invalid/blocked? Classify accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) and list concrete risks only.

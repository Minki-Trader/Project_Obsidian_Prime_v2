# F70D Pre-MT5 Runtime Probe Review(F70D 사전 MT5 런타임 탐침 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견). Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Current Stage(현재 단계)

- Stage(단계): `stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation`.
- Hypothesis(가설): regime/session-specific asymmetric value and exit-survival labels(장세/세션별 비대칭 가치 및 청산 생존 라벨)이 F69 sparse/dense fracture(F69 희박/조밀 균열)를 줄일 수 있는지 본다.
- F70A Grok review(그록 검토): accepted label/target first(라벨/목표 우선), regime/session coupled(장세/세션 결합), exit shape ablation only(청산 형태 소거 비교 전용).
- F70B proxy scout(프록시 탐색): 420 candidates(후보), joint-soft(공동 완화) 0, final-like(최종 조건 유사) 0. Best OOS(표본외) PF 1.51, trades/day 0.999, but validation PF 0.79.
- F70C label-regime stability repair(라벨-장세 안정성 수리): 936 candidates(후보), joint-soft(공동 완화) 0, final-like(최종 조건 유사) 0.

## Closest F70C Axes(가장 가까운 F70C 축)

Axis A(축 A), reference-quality(참조 품질):

- candidate(후보): `f70c_f9a2939acd19`
- label(라벨): `repair_trend_quality_h18_tp85_edge08_pen40`
- model(모델): `extratrees_light_reference_v1`, role(역할): reference_only(참조 전용)
- selection(선택): `vol_expansion_q50`
- validation(검증): net 527.46, PF 1.1676, DD 4.36%, trades/day 0.9365
- OOS(표본외): net 1153.65, PF 1.5657, DD 1.82%, trades/day 0.8907
- concern(우려): not hypothesis carrier(가설 운반체 아님), density below target scout floor(밀도 낮음)

Axis B(축 B), hypothesis-carrier(가설 운반):

- candidate(후보): `f70c_5c8a3021f38f`
- label(라벨): `repair_vol_expansion_h18_tp85_edge08_pen40`
- model(모델): `small_mlp_l2_v1`, role(역할): hypothesis_carrier(가설 운반체)
- selection(선택): `vol_expansion_q50`
- validation(검증): net 835.79, PF 1.1975, DD 4.34%, trades/day 1.1466
- OOS(표본외): net 430.60, PF 1.1241, DD 2.88%, trades/day 1.2254
- concern(우려): PF below meaningful floor(수익 팩터 의미 하한 미달), but density better(밀도는 더 나음)

## Codex Proposed Direction(Codex 제안 방향)

Because every frontier stage(전선 단계) requires an MT5 Runtime Probe(MT5 런타임 탐침), do not close F70 from proxy only(프록시만으로 F70을 닫지 않음). Materialize two narrow observation axes(좁은 관찰 축 2개):

1. Axis A(축 A) as best stable low-DD reference probe(가장 안정적 저손실 참조 탐침).
2. Axis B(축 B) as model-family carrier probe(모델 계열 운반체 탐침).

This is not completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성). It is runtime probe observation(런타임 탐침 관찰) only.

## Review Questions(검토 질문)

1. Is it honest to run MT5 Runtime Probe(MT5 런타임 탐침) on these two near-miss axes despite joint-soft=0(공동 완화 0)?
2. Should Axis A(참조 ExtraTrees) and Axis B(작은 신경망 운반체) both be probed, or should Codex probe only one?
3. What must be recorded as negative memory(부정 기억) if runtime probe(런타임 탐침) collapses while signal/feature parity(신호/피처 동등성) passes?

Allowed claims(허용 주장): runtime probe observation(런타임 탐침 관찰), proxy/runtime gap cause(프록시/런타임 간극 원인), preserved clue(보존 단서), negative memory(부정 기억).

Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

# Frontier24 Experiment Design(전선24 실험 설계)

- hypothesis(가설): train-only micro-pocket assembly(학습 전용 미세 구간 조립)가 개별 구간의 PF(수익 팩터)를 크게 희석하지 않고 validation/OOS(검증/표본외)에서 density(빈도)를 목표 범위로 끌어올릴 수 있다.
- decision_use(결정 사용처): F24B proxy scout(전선24B 프록시 탐색)의 OR-union bridge(OR 합집합 연결) 선택 계약을 고정한다.
- comparison_baseline(비교 기준): F23 preserved pockets(전선23 보존 구간) f23c_0123, f23c_0071, f23c_0233 and unconditional same-side train baseline(무조건 같은 방향 학습 기준).
- control_variables(통제 변수): feature_set_v2 58 features(58개 피처 고정), future_log_return_12 fwd12 proxy(fwd12 프록시 고정), train-only selection(학습 전용 선택), validation/OOS read-only(검증/표본외 읽기 전용)
- changed_variables(변경 변수): structural unit changes from single pocket to same-side OR-union bridge(구조 단위가 단일 구간에서 같은 방향 OR 합집합 연결로 변경), density bridge first; DD normalization deferred to repair if needed(빈도 연결 우선, 손실폭 정규화는 필요 시 수리로 지연), overlap and diversity guards are executable constraints(중복과 다양성 보호를 실행 제약으로 고정)
- sample_scope(표본 범위): Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락); Tier A+B out_of_scope_by_claim(티어 A+B 주장 범위 밖).
- success_criteria(성공 기준): {"scout_clue": {"pf": 1.1, "density_low": 5.0, "density_high": 10.0, "dd_cap": 25.0}, "seed_surface": {"pf": 1.2, "density_low": 5.0, "density_high": 10.0, "dd_cap": 18.0}, "handoff_candidate": {"pf": 1.5, "density_low": 5.0, "density_high": 10.0, "dd_cap": 12.0, "equity_trend_r2": 0.35}}
- failure_criteria(실패 기준): union bridge raises density but validation/OOS PF falls below 1.10(합집합 연결이 빈도는 올리지만 검증/표본외 PF가 1.10 미만), added density is mostly overlap with no unique contribution(추가 빈도가 대부분 중복이고 고유 기여가 없음), DD remains above 25% after density bridge read(빈도 연결 뒤 손실폭이 25% 초과)
- invalid_conditions(무효 조건): validation/OOS used for bridge selection(검증/표본외를 연결 선택에 사용), opposite long/short sides mixed inside one bridge(롱/숏을 한 연결 안에 혼합), ONNX/model training before handoff candidate(인계 후보 전 ONNX/모델 학습)
- stop_conditions(중단 조건): no train-only bridge can reach target density with positive PF(학습 전용 연결이 양수 PF와 목표 빈도에 도달하지 못함), seed or handoff appears and pre-expensive Grok is required(씨앗 또는 인계가 나타나 비싼 검증 전 Grok 필요), capped density bridge repair cannot create seed/handoff(상한 빈도 연결 수리가 씨앗/인계를 만들지 못함)
- evidence_plan(근거 계획): F24B run manifest(실행 목록), micro-pocket table(미세 구간 표), bridge candidate summary(연결 후보 요약), split metrics(분할 지표), run registry(실행 등록부), stage ledger(단계 장부).

# Frontier22 Experiment Design(전선22 실험 설계)

- hypothesis(가설): US100 M5 return shock(수익률 충격) combined with exactly one context family(문맥군) can isolate favorable payoff asymmetry(유리한 보상 비대칭) before any lifecycle repair(생명주기 수리 전).
- decision_use(결정 사용처): Open F22B proxy scout(F22B 프록시 탐색)를 shock+context locked rule shape(충격+문맥 잠금 규칙 형태)로 실행합니다.
- comparison_baseline(비교 기준): F20/F21 are reference-only(참조 전용) and no selected baseline(선택 기준선 없음).
- control_variables(통제 변수): feature_set_v2 fixed 58 features(고정 58개 피처), future_log_return_12 fixed proxy(고정 12봉 미래 수익률 프록시), train-only thresholds(학습 전용 임계값), validation/OOS read-only diagnostics(검증/표본외 읽기 전용 진단)
- changed_variables(변경 변수): shock feature family(충격 피처군), one context condition(문맥 조건 1개), locked shock continuation/fade lane(고정 충격 지속/되돌림 방향)
- sample_scope(표본 범위): Tier A separate only(티어 A 분리 전용); Tier B missing_required(티어 B 필수 누락); Tier A+B out_of_scope_by_claim(티어 A+B 주장 범위 밖).
- success_criteria(성공 기준): {"scout_clue": "shock present, not F20 duplicate, validation/OOS net positive, PF>=1.05, density 3-12/day(충격 포함, F20 중복 아님, 검증/표본외 양수)", "seed_surface": "PF>=1.2 both, density 5-10/day, DD<=25%(양쪽 수익 팩터 1.2 이상, 빈도 5-10, 손실폭 25% 이하)", "handoff_candidate": "PF>=1.5 both, density 5-10/day, DD<=15%, smoothness pass, then Grok before MT5/ONNX(양쪽 수익 팩터 1.5 이상 뒤 비싼 검증 전 그록)"}
- failure_criteria(실패 기준): best rule is F20 duplicate pressure(F20 중복 압력), no validation/OOS positive PF clue(검증/표본외 양수 수익 팩터 단서 없음), density/PF/DD cannot coexist(빈도/수익 팩터/손실폭 공존 실패)
- invalid_conditions(무효 조건): candidate without shock feature(충격 피처 없는 후보), candidate with more than one context condition(문맥 조건 1개 초과 후보), validation/OOS threshold selection(검증/표본외 임계값 선택), lifecycle repair inside F22B(F22B 안 생명주기 수리)
- stop_conditions(중단 조건): max candidate cap reached(후보 상한 도달), handoff-like candidate appears and pre-expensive Grok is required(인계형 후보 발생 후 비싼 검증 전 그록 필요), no scout/seed clue after capped proxy(상한 프록시 뒤 단서 없음)
- evidence_plan(근거 계획): stage_open_summary.json(단계 개방 요약), shock_pf_source_lock.json(충격 수익 팩터 원천 잠금), condition_pool.csv(조건 풀), candidate_summary.csv(후보 요약), proxy_metrics_by_split.csv(분할별 프록시 지표), stage_run_ledger.csv(단계 실행 장부)

# Frontier25 Experiment Design(전선25 실험 설계)

- hypothesis(가설): F24 failed because it selected density first and repaired DD later; F25 flips the order and selects lower-risk bridge archetypes on train only(F24는 빈도 우선 선택 뒤 손실폭을 고쳤기 때문에 실패했고, F25는 학습 전용 낮은 위험 연결 원형을 먼저 고른다)
- decision_use(결정 사용처): decide whether headroom-first bridge construction deserves proxy repair, WFO, or runtime handoff consideration(손실폭 여유 우선 연결 구성이 프록시 수리/WFO/런타임 인계 검토 가치가 있는지 결정)
- comparison_baseline(비교 기준): F24B density-first bridge and F24C post-hoc DD repair as reference-only, not baseline(F24B 빈도 우선 연결과 F24C 사후 손실폭 수리는 참조 전용이며 기준선 아님)
- control_variables(통제 변수): US100 M5 Tier A dataset(US100 5분봉 티어 A 데이터셋), feature_set_v2 58 features(피처 세트 v2 58개), fwd12 label horizon(fwd12 라벨 지평), same-side OR-union semantics(같은 방향 OR 합집합 의미), validation/OOS read-only(검증/표본외 읽기 전용)
- changed_variables(변경 변수): dd_headroom_first_preselection(손실폭 여유 우선 사전 선택), explicit F24B top10 non-repeat audit(F24B 상위10 반복 아님 감사), no primary repair in first proxy(첫 프록시 기본 경로 수리 없음)
- sample_scope(표본 범위): Tier A US100 M5 model_input_dataset.parquet, train/validation/oos frozen split(티어 A US100 5분봉 고정 분할)
- success_criteria(성공 기준): {"scout": "validation and OOS PF>=1.10, density 5-10/day, max DD<=25%(검증/표본외 수익 팩터 1.10 이상, 일 5~10회, 최대 손실폭 25% 이하)", "seed": "PF>=1.20, density 5-10/day, max DD<=18%(수익 팩터 1.20 이상, 일 5~10회, 최대 손실폭 18% 이하)", "handoff": "PF>=1.50, density 5-10/day, max DD<=12%, smoothness proxy pass(수익 팩터 1.50 이상, 일 5~10회, 손실폭 12% 이하, 매끄러움 통과)"}
- failure_criteria(실패 기준): no archetype passes train-only DD headroom filter(학습 전용 손실폭 여유 필터 통과 원형 없음), top rows repeat F24B keys without DD headroom lift(F24B 키 반복이며 손실폭 여유 개선 없음), all forward rows fail scout PF/DD/density(모든 전진 행이 탐색 수익 팩터/손실폭/빈도 실패)
- invalid_conditions(무효 조건): validation/OOS used in selection(검증/표본외 선택 사용), F25B applies capped repair as primary path(F25B가 상한 수리를 기본 경로로 적용), feature hash mismatch(피처 해시 불일치)
- stop_conditions(중단 조건): F25B has zero valid archetypes(F25B 유효 원형 0개), F25B is repeat without metric lift(F25B가 지표 개선 없는 반복), handoff rows >0 triggers Grok before expensive WFO/MT5(인계 행이 있으면 비싼 WFO/MT5 전 Grok 검토), no seed/handoff after capped repair closes as preserved clue or negative memory(상한 수리 뒤 씨앗/인계 없으면 보존 단서 또는 부정 기억으로 마감)
- evidence_plan(근거 계획): F25B run manifest(실행 목록), train-ranked archetype table(학습 순위 원형 표), F24B top-10 diff audit(F24B 상위10 차이 감사), split metrics(분할 지표), run registry(실행 등록부), stage ledger(단계 장부).

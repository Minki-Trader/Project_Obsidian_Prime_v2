# F78G Stage Closeout Grok Review Prompt(F78G 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

Current stage(현재 단계): `stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild`
Proposed closeout label(제안 마감 라벨): `negative_memory(부정 기억)`
Claim boundary(주장 경계): `stage_closeout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

Hypothesis(가설):
Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), calendar density(달력 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), risk penalty(위험 벌점)를 proxy(프록시)에 내장하면 F77 money/density gap(F77 금액/밀도 간극)을 줄일 수 있다.

Mandatory runtime probe(MT5 필수 런타임 탐침):
- F78D validation runtime(검증 런타임): net/PF/DD/tpd/trades `-26.53/0.92/11.45/1.2095588235294117/329`
- signal/feature/fill parity(신호/피처/체결 동등성): signal diff `0`, feature diff `0`, fill rate `1.0`
- gap cause(간극 원인): `entry_timing_mismatch_minus_5min + DD denominator 10000 vs 500 + remaining fill path gap`

Repair result(수리 결과):
- F78F repaired proxy best(수리 프록시 최선): `f78b_01233`
- F78F scout/meaningful/final-like(탐색/의미/완성 유사): `0/0/0`
- F78F OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일 거래/거래): `2.199999561734594/999.0/0.0/0.005154639175257732/1`

Preserved clue(보존 단서):
- ONNX/EA feature and signal parity(ONNX/EA 피처와 신호 동등성)는 정확히 맞출 수 있었다.
- Selected-entry veto tape(선택 진입 거부 테이프)은 proxy selected count(프록시 선택 수)와 runtime signal count(런타임 신호 수)를 맞추는 도구로 보존한다.
- Entry timing(진입 시각)과 DD denominator(손실폭 분모)는 proxy label(프록시 라벨) 설계 시작부터 명시해야 한다.

Negative memory(부정 기억):
- Next-bar proxy(다음 봉 프록시)는 양수여도 MT5 same-bar execution(MT5 동일 봉 실행)에서는 음수가 될 수 있다.
- Runtime-aligned entry(런타임 정렬 진입)와 tester-deposit DD(테스터 예치금 손실폭) 수리 뒤 F78F는 scout clue(탐색 단서) 0, meaningful signal(의미 신호) 0이었다.
- F78은 threshold-only(임계값 단독)나 model-only(모델 단독) 수리로 계속 밀면 반복 수리가 된다.

Question(질문):
Should Codex close F78 as negative_memory(부정 기억) with preserved clues(보존 단서) and move to a new frontier hypothesis(F79), or is there a concrete non-repetitive repair(반복 아닌 구체 수리) still required inside F78 before closeout(마감)?

Classify advice(조언 분류) exactly one: accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), rejected(거절).
Do not grant completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).

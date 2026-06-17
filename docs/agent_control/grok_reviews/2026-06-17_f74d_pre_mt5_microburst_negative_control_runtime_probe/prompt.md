# F74D Pre-MT5 Review Prompt(F74D MT5 전 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or do local verification(로컬 검증 금지).

## Current State(현재 상태)

- Project(프로젝트): Project Obsidian Prime v2, FPMarkets US100 M5(FPMarkets US100 5분봉).
- Active stage(활성 단계): `stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path`.
- Stage hypothesis(단계 가설): microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험한다.
- Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Evidence Snapshot(근거 스냅샷)

### F74A Stage Open(F74A 단계 개방)

- Grok stage-open advice(Grok 단계 개방 조언): accepted(수용).
- Grok drift risk(드리프트 위험): density quota backdoor(밀도 할당 우회).
- Grok repair priority(수리 우선순위): label-only density gate first(라벨 단독 밀도 게이트 우선).

### F74B Raw Label And Proxy Scout(F74B 원시 라벨 및 프록시 탐색)

- raw density pass axes(원시 밀도 통과 축): 6/6.
- raw validation/OOS density(검증/표본외 밀도): roughly 12.95-13.94 trades/day validation(검증 일거래), 14.03-15.33 trades/day OOS(표본외 일거래).
- proxy candidates(프록시 후보): 648.
- scout clue(탐색 단서): 0.
- meaningful candidate(의미 후보): 0.
- final-like reference-only(최종 유사 참조 전용): 0.
- best F74B candidate(최선 F74B 후보): `f74b_0505`, `microburst_h9_long`, `core_no_external`, `logistic_l2`.
- best F74B validation KPI(검증 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `-2236.54 / 0.6472 / 24.1165% / 1.4669`.
- best F74B OOS KPI(표본외 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `811.95 / 1.1828 / 2.9838% / 1.8684`.
- F74B judgment(판정): `raw_density_passed_proxy_repair_required_no_authority`.

### F74C Clean/Value Label Repair(F74C 깨끗한/가치 라벨 수리)

- Repair novelty(수리 신규성): label/target changed(라벨/목표 변경) to `clean_fast_touch`, `clean_value_q60`, `net_edge_q70`; target/stop(익절/손절) became more asymmetric.
- proxy candidates(프록시 후보): 1296.
- scout clue(탐색 단서): 0.
- meaningful candidate(의미 후보): 0.
- final-like reference-only(최종 유사 참조 전용): 0.
- best F74C candidate(최선 F74C 후보): `f74c_1212`, `clean_value_h9_short`, `clean_value_q60`, `core_no_external`, `cash_mid_late`, `hist_gbm`.
- best F74C validation KPI(검증 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `747.69 / 1.1290 / 6.3779% / 1.6949`.
- best F74C OOS KPI(표본외 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `-469.75 / 0.9164 / 7.0489% / 2.0769`.
- F74C judgment(판정): `proxy_repair_no_scout_clue_risk_session_decision_required_no_authority`.

## Codex Proposed Direction(Codex 제안 방향)

Codex proposes a mandatory negative-control MT5 Runtime Probe(필수 부정 대조 MT5 런타임 탐침) for the best materializable F74C candidate, despite no scout clue(탐색 단서 없음).

Reason(이유):

- The stage goal requires at least one MT5 Runtime Probe(MT5 런타임 탐침) per frontier stage(전선 단계).
- F74 is not zero-signal(영 신호) because selected trades exist after lifecycle filtering(생명주기 필터 뒤 선택 거래 존재).
- The probe will not claim positive evidence(긍정 근거). It will test whether proxy/runtime gap(프록시/런타임 간극) worsens or preserves the already-weak proxy.
- If materialization is technically blocked(기술적으로 차단), Codex should record exact blocker(정확한 차단 사유) and repair action(수리 행동), not close as comparison unavailable(비교 불가).

Proposed materialization target(물질화 대상):

- `f74c_1212`: short(숏), horizon 9 bars(9봉), target 1.0 ATR(평균진폭), stop 0.45 ATR(평균진폭), cash_mid_late(정규장 중후반), hist_gbm, clean_value_q60(깨끗한 가치 q60).

## Review Question(검토 질문)

Classify the proposed F74D negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침):

- `accepted(수용)`: this is the right next action before closeout/next repair.
- `rejected(거절)`: do not run MT5; explain why this would violate the stage or evidence rules.
- `needs_local_verification(로컬 검증 필요)`: local materialization feasibility(로컬 물질화 가능성) must be checked first.

Also give:

1. one drift risk(드리프트 위험),
2. one probe design requirement(탐침 설계 요구),
3. one next action if MT5 materialization fails(물질화 실패 시 다음 행동).

Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

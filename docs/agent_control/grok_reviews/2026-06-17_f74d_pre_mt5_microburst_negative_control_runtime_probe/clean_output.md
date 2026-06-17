## Classification(분류)

**`accepted(수용)`**

F74D 부정 대조 MT5 Runtime Probe(런타임 탐침)는 closeout(마감)이나 다음 repair(수리) 전에 맞는 다음 행동이다.

**근거(why):**

1. **Stage rhythm(단계 리듬)** — frontier stage(전선 단계)마다 MT5 Runtime Probe(런타임 탐침) 최소 1회는 운영 요구와 맞다. F74는 zero-signal(영 신호)이 아니다. lifecycle filtering(생명주기 필터) 뒤 선택 거래가 있고, F74B에서 raw density(원시 밀도)는 이미 통과했다.
2. **Claim boundary(주장 경계) 준수** — scout clue(탐색 단서) 0, F74C OOS(표본외) 약함은 **긍정 근거를 포기**하는 이유이지, **proxy/runtime gap(프록시·런타임 간극) 관측**을 건너뛸 이유가 아니다. negative-control(부정 대조) 프레이밍이면 authority(권위) 주장 없이 gap(간극)만 볼 수 있다.
3. **Evidence discipline(근거 규율)** — F74C 판정 `proxy_repair_no_scout_clue_risk_session_decision_required`는 “MT5 금지”가 아니라 “proxy만으로 결론 내리지 말라”에 가깝다. `f74c_1212`는 F74C에서 materializable(물질화 가능)한 최선 후보로 제시됐고, 차단 시 blocker(차단 사유) 기록은 comparison unavailable(비교 불가)로 닫는 것보다 낫다.

**`needs_local_verification`이 아닌 이유:** 물질화 가능성( feasibility )은 F74D **실행 단계**에서 확인하면 된다. 전략적으로 “지금 MT5를 돌릴지”에 대한 답은 snapshot(스냅샷)만으로 **accepted**다.

**`rejected`가 아닌 이유:** scout clue 0이라 MT5를 생략하면 external verification(외부 검증)을 또 미루게 되고, stage hypothesis(단계 가설)의 runtime path(런타임 경로) 질문에 답하지 못한다.

---

## 1. Drift risk(드리프트 위험)

**Density quota backdoor(밀도 할당 우회)** — MT5에서 trade count(거래 수)나 실행 빈도가 나오면, proxy scout clue 0·OOS 약함을 무시하고 “dense smooth runtime path(조밀·매끄러운 런타임 경로) seed surface(씨앗 표면) 확보”처럼 **간접 승격**하는 해석으로 새는 위험. F74A에서 이미 지적된 패턴이다.

---

## 2. Probe design requirement(탐침 설계 요구)

**Frozen negative-control identity(고정 부정 대조 정체성)** — `f74c_1212` 스펙(short, h9, target 1.0 ATR, stop 0.45 ATR, `cash_mid_late`, `hist_gbm`, `clean_value_q60`)을 proxy·MT5·receipt(영수증) 전 구간에서 동일하게 고정하고, KPI 비교는 **proxy vs MT5 side-by-side(나란히)**만 허용한다. success threshold(성공 임계값), scout clue(탐색 단서), density pass(밀도 통과) **재판정 금지**. receipt 라벨은 `negative_control_runtime_probe_no_authority`로 명시한다.

---

## 3. Next action if MT5 materialization fails(MT5 물질화 실패 시 다음 행동)

**Blocker-first repair fork(차단 사유 우선 수리 분기)** — 정확한 blocker(예: bundle parity break, session filter unmappable, feature export gap)를 canonical receipt(정식 영수증)에 남긴 뒤, **가장 좁은 수리 1회**만 시도한다(예: 동일 label family 내 더 단순한 F74C 후보, 또는 `core_no_external` subset으로 parity 축소). 그래도 실패하면 F74D를 `blocked_materialization_documented_no_authority`로 닫고, closeout(마감)에서 “비교 불가”가 아니라 **차단 사유 + 다음 repair lane(수리 레인)**(label-only density gate 재검 또는 alternate horizon/session)을 적는다.

---

## Claim boundary(주장 경계)

이 검토는 **방향 수용**만 한다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성) **주장 없음**. MT5 결과가 나와도 negative-control(부정 대조) 범위 안에서만 해석한다.

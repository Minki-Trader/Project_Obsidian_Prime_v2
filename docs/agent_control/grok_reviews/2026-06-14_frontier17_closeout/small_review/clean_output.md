## 1. Classification

**accepted**

Codex의 제안 방향(negative memory closeout + preserved runtime handoff clue)은 bounded evidence(제한 근거)와 정합합니다. F17B proxy(프록시)도 hard gates(하드 게이트)를 못 넘었고, F17C MT5 runtime probe(런타임 탐침)는 signal parity(신호 동등성)는 맞췄지만 economics(경제성)와 DD(낙폭)에서 명확히 실패했습니다. F16D 선례가 같은 패턴을 이미 보여 줍니다.

---

## 2. Recommendation

**close as negative memory, with preserved clue (no further narrow repair before closeout)**

한 번 더 좁은 repair(수정)를 돌릴 근거가 약합니다.

- F17B best(최선)도 validation PF 1.30, OOS PF 1.14, DD ~13%로 goal hard gates(PF 2–3+, DD &lt;10%) 미달입니다. strict scout clue(엄격 정찰 단서)도 없습니다.
- F17C는 signal diff 0(신호 차이 0)인데 validation PF 1.13 / OOS PF 0.92, DD 35–47%로 proxy 대비 경제성이 붕괴했습니다. 이건 “한 번 더 캘리브레이션”보다 **alpha hypothesis(알파 가설) 실패**에 가깝습니다.
- expected signals 727→317 trades, 667→254 trades 갭은 있지만, signal parity가 이미 맞춰진 상태에서 PF·DD가 이렇게 나왔다면 execution gap(실행 갭)만의 문제로 보기 어렵습니다. F16D가 같은 교훈을 이미 남겼습니다.

**preserve할 clue(단서)는 인프라 쪽만:** runtime veto tape handoff(런타임 거부 테이프 인계) + ONNX parity(동등성) + MT5 signal parity(신호 동등성). **reject할 것은 alpha idea(알파 아이디어) 본체:** loss-cluster firewall profit persistence의 native MT5 execution economics(네이티브 MT5 실행 경제성).

---

## 3. Main failure risks

1. **Signal parity ≠ economic success (신호 동등성 ≠ 경제적 성공)**
   F16D·F17C 모두 diff 0인데 OOS PF &lt;1, DD ~47%. “handoff works(인계 성공)”를 “idea works(아이디어 성공)”로 오독할 위험이 큽니다.

2. **Proxy overfitting / weak OOS (프록시 과적합·약한 OOS)**
   F17B validation→OOS PF 하락(1.30→1.14), DD 여전히 gate 밖. proxy에서도 promotion_candidate(승격 후보) 강도가 없었습니다.

3. **Native execution DD explosion (네이티브 실행 DD 폭발)**
   proxy DD ~13% → MT5 DD 35–47%. firewall continuation(방화벽 지속) 가설이 실거래형 실행에서 tail risk(꼬리 위험)를 키웠을 가능성이 큽니다.

4. **Novelty exhaustion at current contract (현 계약에서 신규성 소진)**
   argmax + adverse_veto false, no density calibration(밀도 보정 없음) surface(표면)로는 goal band(5–10 trades/day, PF 2–3+, DD &lt;10%)에 도달한 증거가 없습니다. repair 한 번 더는 validation_is에 맞춘 미세 조정(미세 과적합) 위험이 큽니다.

5. **Claim boundary drift (주장 경계 표류)**
   preserved_clue_candidate(보존 단서 후보)나 runtime veto tape 성공을 scout success(정찰 성공), baseline(기준선), 또는 “almost there(거의 됨)”로 승격시키면 progressive hardening(점진적 경화) 규칙을 깹니다.

6. **Incomplete tier record (티어 기록 불완전)**
   Tier B·combined missing_required(필수 누락)는 이번 closeout 주장 범위에서는 authority(권위) 없음으로 처리 가능하지만, “full-context read(전체 문맥 판독)”을 대체 근거로 쓰면 안 됩니다.

---

## 4. Local verification Codex must do before acting

1. **Ledger/register line verification (장부·등록부 행 검증)**
   F17B·F17C run identity, judgment labels, missing_required for Tier B/combined가 stage_run_ledger·alpha_run_ledger에 실제로 반영됐는지 확인.

2. **Artifact hash / report number match (산출물 해시·보고서 수치 일치)**
   bounded evidence의 PF, DD, density, signal counts, trade counts가 frontier17B/C report 원문과 일치하는지 재확인.

3. **F17C signal diff 0 evidence (F17C 신호 차이 0 근거)**
   runtime probe 산출물에서 validation_is·OOS 각각 signal diff 0, expected signals 727/667가 파일·로그로 재현되는지 확인. “matched 2/2”가 어떤 샘플/구간인지 범위를 명시.

4. **Forbidden leakage scan (금지 주장 누출 스캔)**
   closeout draft, selection_status, idea_registry, workspace_state에 completion, Goal Achieve, baseline, promotion, runtime authority, live readiness 문구가 없는지 검색.

5. **Clue vs alpha separation in closeout text (종료 기록에서 단서·알파 분리)**
   negative memory는 “firewall profit persistence failed MT5 economics/DD”에, preserved clue는 “RuntimeVetoTape + ONNX/signal parity handoff path”에만 붙었는지 확인.

6. **F16D cross-reference honesty (F16D 교차 참조 정직성)**
   closeout이 F16D precedent를 “repeat pattern(반복 패턴), not surprise(놀라움 아님)”로 기록하는지 확인.

---

## 5. Forbidden claim check

| Claim (주장) | Verdict (판정) |
|---|---|
| Goal Achieve / stage completion on hard gates | **FORBIDDEN** — proxy·MT5 모두 PF 2–3+, DD &lt;10%, smooth equity 미달 |
| Selected baseline / operating promotion | **FORBIDDEN** — F17A guard, no inherited winner, F17B no authority |
| Runtime authority / live readiness | **FORBIDDEN** — runtime probe completed ≠ economics validated; OOS PF 0.92 |
| Strict scout clue / seed surface | **FORBIDDEN** — F17B는 preserved_clue_candidate only |
| “Signal parity proves alpha” | **FORBIDDEN** — F16D·F17C OOS PF &lt;1 counterexample |
| “One more repair likely reaches gates” | **FORBIDDEN** — bounded evidence shows proxy miss + MT5 collapse; repair는 과적합·scope creep 위험 |
| Tier B/combined as supporting alpha read | **FORBIDDEN** — missing_required by scope |

**Allowed (허용):** Frontier17 **negative memory(부정 기억)** closeout; **preserved technical clue(보존 기술 단서):** runtime veto tape reproduces adverse_veto with ONNX + MT5 signal parity; **alpha hypothesis rejected for native MT5 economics/DD** under current contract; **no authority, no promotion, no completion**.

---

**Bottom line:** Codex should **close Frontier17 now** as negative memory and preserve only the **runtime handoff infrastructure clue**. Another narrow repair before closeout is not justified by novelty, OOS economics, or claim boundaries—it would mostly risk overfitting and delaying an already clear negative result.

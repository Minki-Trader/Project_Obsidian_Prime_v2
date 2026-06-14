Frontier21 마감 검토를 위해 Grok 협업 스킬과 제한 근거를 먼저 확인합니다.
# Grok Review — Frontier21 Closeout(전선21 마감 검토)

**Review size(검토 크기):** small review(소규모 검토), bounded evidence only(제한 근거만)

**Plain read(쉬운 요약):** Frontier21은 “손실폭을 줄이면서도 하루 5~10건 거래와 수익 팩터를 같이 살리자”는 가설을 검증했습니다. 손실폭·빈도·수익 팩터를 동시에 맞추지 못했고, 인계 후보도 없습니다. 그래서 `preserved_clue + negative_memory(보존 단서 + 부정 기억)`로 닫는 제안은 정직하고 범위도 적절합니다.

---

## Decision(결정): **accept with minor adjust(수용, 소폭 조정)**

Codex 제안 마감 라벨은 **정직하고 충분히 제한됨(bounded)**. 승격·기준선·런타임·완성 주장 없이, 탐색 실패를 부정 기억으로 남기는 방식이 맞습니다.

**소폭 조정 3가지** — 거절이 아니라 기록을 더 정확히 하는 보완입니다.

1. **보존 단서를 두 갈래로 나누기**
   - F21B: 긴 보유·쿨다운 프로필은 **빈도는 희생**하지만 OOS PF `1.25`와 낮은 DD를 보여, “생명주기만으로 손실폭 억제 + PF 유지”는 **부분 성공**입니다.
   - F21C: 짧은 보유·쿨다운 없음은 **빈도 5~6/day + DD 2~4%**를 만들지만 PF는 씨앗 바닥 `1.2` 아래입니다.
   - 효과: “생명주기만으로 세 축을 동시에 맞췄다”는 과장을 막습니다.

2. **부정 기억에 ONNX 분기 미개시 추가**
   - 단계 제목에 ONNX scout(ONNX 탐색)가 있지만, handoff candidate(인계 후보) `0/0/0` 때문에 **시도조차 안 됨**.
   - 효과: “ONNX를 못 만든 실패”가 아니라 “PF/인계 게이트에서 막혀 분기 자체가 열리지 않음”으로 기록됩니다.

3. **Tier A only(티어 A만) 한계를 마감 문장에 명시**
   - Tier B `missing_required`, combined `out_of_scope_by_claim`은 이미 정직합니다. 마감 본문에 “**Tier A lifecycle proxy only(티어 A 생명주기 프록시만)**”를 한 줄 넣으면 범위가 더 분명해집니다.

---

## What to Preserve(보존할 것)

| Clue(단서) | Evidence anchor(근거 앵커) | Bounded meaning(제한된 의미) |
|---|---|---|
| Lifecycle DD containment works(생명주기 손실폭 억제는 됨) | F21B `f21b_hold10_atr1p5_tp3p0_cd6`: OOS DD `3.19%`, PF `1.25`, density `2.27/day` | F20 대비 손실폭을 크게 줄일 수 있음. **빈도 목표는 아직 아님.** |
| Short-hold / no-cooldown density repair(짧은 보유·쿨다운 없음 빈도 수리) | F21C `f21c_hold2_atr0p8_tp1p6_cd0`: validation density `5.54/day`, OOS `6.37/day`, DD `2.3~3.2%` | 고정 F20 진입 위에 **거래 빈도·낮은 손실폭 형태**를 복구할 수 있음. **수익 우위(PF edge) 주장은 아님.** |
| Entry lock held(진입 잠금 유지) | Opening locks respected across F21B/F21C | 진입 재순위·방향 전환·새 피처 없이 lifecycle/risk stack(생명주기/위험 묶음) 효과를 분리 관측함. |
| Scout row semantics(탐색 행 의미) | F21C `scout=3; seed=0; handoff=0` | 빈도·손실폭 단서는 있으나 **씨앗·인계 승격 없음** — scout clue(탐색 단서) 수준만 정당함. |

**Do not preserve as edge(우위로 보존하지 말 것):** F21C OOS PF `1.079`는 탐색 단서이지 handoff-worthy PF(인계 가능 PF)가 아닙니다.

---

## What to Record as Negative Memory(부정 기억으로 남길 것)

1. **Compound hypothesis failed(복합 가설 실패):** lifecycle/risk stack alone(생명주기/위험 묶음 단독)으로 DD 억제 + density `5~10/day` + PF 회복을 **동시에** 달성하지 못함. F21B↔F21C가 **축 간 트레이드오프**를 보여줌.

2. **PF seed floor miss(씨앗 PF 바닥 미달):** density repair(빈도 수리) 후 best OOS PF `1.079 < 1.2`. 다른 scout clue 행도 PF `< 1.2`.

3. **No handoff candidate(인계 후보 없음):** `seed=0`, `handoff=0` — 다음 단계로 넘길 패키지 없음.

4. **ONNX scout unattempted(ONNX 탐색 미시도):** upstream PF/handoff gate(상류 PF/인계 게이트)에서 차단. “ONNX 실패”가 아니라 **분기 미개시**.

5. **External verification gap(외부 검증 공백):** no WFO, no MT5, no ONNX — lifecycle proxy(생명주기 프록시) 수준에서만 닫힘.

6. **Tier incompleteness honestly blocked(티어 불완전 — 정직히 차단):** Tier B 없음, combined 없음 — 전체 알파 판독으로 확장 불가.

---

## Runtime Probe(런타임 탐침): **ineligible(부적격), not required(필수 아님)**

| Question(질문) | Grok read(그록 판단) |
|---|---|
| Required now?(지금 필요?) | **No.** handoff candidate 없음, OOS PF `< 1.2`, opening lock에 MT5/runtime claim 금지. |
| Why ineligible?(왜 부적격?) | MT5 probe(런타임 탐침)는 **인계 가능한 후보**가 있을 때 의미 있음. 현재는 proxy scout clue(프록시 탐색 단서)만 있음. |
| Blocker label(차단 라벨) | `out_of_scope_by_claim_no_handoff_candidate` — Codex 제안과 일치. |

효과: 약한 PF 프로필을 MT5로 “확인”하려는 조기 런타임 주장을 막습니다.

---

## Forbidden Claim Reminder(금지 주장 알림)

이 마감에서 **절대 주장하면 안 되는 것:**

- **baseline(기준선)** / **selected profile(선택 프로필)** — `f21c_hold2...`는 best repair row(최상 수리 행)이지 운영 기준선 아님
- **promotion(승격)** / **promotion candidate(승격 후보)** — scout clue만 있고 seed/handoff `0`
- **runtime authority(런타임 권위)** / **live readiness(실거래 준비)** — WFO·MT5·ONNX 없음
- **completion(완성)** / **Goal Achieve(목표 달성)** — 복합 가설 미달성
- **“F21 solved DD while keeping edge”** — DD·density는 부분 성공, PF edge는 F21C에서 약함
- **Tier A+B combined read(티어 A+B 합산 판독)** — 원천 없음, `out_of_scope_by_claim`

허용되는 마감 문구 예: *“Frontier21 closed as preserved_clue + negative_memory under Tier A lifecycle proxy only; no handoff, no runtime probe, no promotion.”*

---

## Next Frontier Direction(다음 전선 방향) — bounded agreement(제한적 동의)

Codex 제안 — **새 PF edge source(수익 팩터 우위 원천) 필요**, F21 low-DD lifecycle shape(낮은 손실폭 생명주기 형태)는 **risk containment reference only(위험 억제 참고만)** — **수용**.

이유: 증거가 “risk shell without edge(우위 없는 위험 껍데기)” 패턴을 보여줌. 다음 전선은 진입/피처/확률 등 **edge 생성**이 주제여야 하고, F21C 프로필을 그대로 이어가면 PF 부족을 lifecycle으로 더 때울 유혹이 큼 — 반복 금지 메모로 적합합니다.

---

## Classification for Codex(코덱스 분류)

| Item(항목) | Classification(분류) |
|---|---|
| Closeout label `preserved_clue + negative_memory` | **accepted(수용)** |
| Runtime probe out_of_scope | **accepted(수용)** |
| Next frontier PF-edge hypothesis | **accepted(수용)** |
| Split F21B vs F21C preserved clues | **needs_local_verification → accepted after ledger/report one-line add(로컬 검증 필요 → 장부/보고 한 줄 추가 후 수용)** |
| ONNX branch unattempted negative memory | **accepted(수용)** |

**Local verification note(로컬 검증 메모):** 제한 근거의 KPI·scout counts·profile ID는 `stage_run_ledger.csv`, F21B/F21C reports, `selection_status.md`와 일치함. 숫자 불일치 없음.

---

**Bottom line(한 줄 결론):** Frontier21을 `preserved_clue + negative_memory`로 닫는 것은 **수용**합니다. 런타임 탐침은 **부적격**이며 **지금 필수 아님**. Codex는 F21B/F21C 단서를 분리 기록하고, ONNX 미개시·Tier A only 한계를 마감 본문에 한 줄씩만 보강하면 됩니다.

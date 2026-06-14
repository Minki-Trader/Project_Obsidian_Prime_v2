Frontier26 stage-open 검토를 위해 Grok 협업 스킬과 프로젝트 현재 상태·F25 근거를 먼저 확인합니다.
# Frontier26 Stage Open Review — External Second Opinion(전선26 단계 개방 검토 — 외부 2차 의견)

**Review size(검토 크기):** small review(소규모 검토) — bounded snapshot(제한 스냅샷) + five focused questions(집중 질문 5개)
**Local verification(로컬 검증):** `workspace_state.yaml`, F25B report, F25 closeout decision, F25A locks, F25 negative memory — user packet numbers match(사용자 패킷 숫자 일치).
**Claim boundary(주장 경계):** no runtime authority(런타임 권위), baseline(기준선), promotion(승격), live readiness(실거래 준비), or Goal Achieve(목표 달성).

---

## 1. Verdict(판정): **`accepted`(수용)**

Proposed Frontier26 open(제안 전선26 개방) is **accepted(수용)** as an exploration-stage hypothesis(탐색 단계 가설), with the same caution F25 got: **lock the changed variable(변경 변수 잠금) and score contract(점수 계약) in F26A before any F26B run(실행 전)**.

F25 closed honestly(정직하게 마감됨): DD-headroom-first at **union rank(합집합 순위)** produced 17 scout rows(탐색 행) and 0 seed/handoff, with the seed bottleneck(씨앗 병목) still DD-blocked on the closest row `f25b_0001`. F26 moves the lever to **component eligibility(구성 요소 적격성)** before union — that is a different causal claim(다른 인과 주장), not a relabel of F25.

**Not rejected because:** testable with existing F24/F25 script chain(기존 스크립트 체인으로 시험 가능), keeps train-only selection(학습 전용 선택), forbids validation-targeted repair(검증 표적 수리 금지) that F25C already rejected, and preserves unchanged scout/seed/handoff gates(게이트 유지).

**Not unconditional accept:** if F26A only tightens thresholds without a written `joint_micro_satisfaction_score` distinct from F25 `train_archetype_score` and F24 `bridge_score`, treat as **repair-loop risk(수리 반복 위험)** and block F26B materialization(물질화 차단).

---

## 2. Valid new hypothesis(새 가설) vs F25 repeat?(F25 반복인가?)

**Yes — `acceptable_new_hypothesis`(허용 가능한 새 가설).** Not a F25 repeat(전선25 반복 아님).

| Axis(축) | F25(전선25) | F26(제안 전선26) |
|---|---|---|
| **Changed variable(변경 변수)** | Union-level DD-headroom-first ranking(합집합 수준 손실폭 여유 우선 순위) | Component-level joint satisfaction gate **before** union(합집합 전 구성 요소 합동 충족 게이트) |
| **Micro filter(미세 필터)** | Per-pocket train DD ≤ 16% only(포켓당 학습 손실폭만) | Joint PF + DD + density + R² + streak + adverse p10(수익 팩터·손실폭·빈도·형태 동시) |
| **Union filter(합집합 필터)** | Bridge train DD ≤ 18%, PF ≥ 1.06(완화) | Bridge train DD ≤ 16%, PF ≥ 1.10, tighter overlap(중복 상한 강화) |
| **Failure diagnosis(실패 진단)** | Union ranking picked weak DD headroom(순위가 약한 여유 선택) | Union admitted individually weak micros(약한 미세 구간이 합집합에 유입) |

F25D already recorded the next clue(다음 단서): `train_joint_micro_satisfaction_before_bridge_union_reference_only`. F26 directly tests that clue — aligned with closeout, not chat drift(대화 이탈 아님).

**Repeat risk(반복 위험)** only if F26B:
- reuses DD-headroom-first as primary rank(손실폭 여유 우선을 주 순위로 재사용), or
- produces the same top `micro_ids` as F25B with no seed-gap improvement(씨앗 간격 개선 없이 동일 상위 조합).

---

## 3. Locks F26A must write before proxy(프록시 전 F26A 잠금)

Mirror F25A `bridge_archetype_preselection_lock.json` pattern(패턴 동일). Minimum set(최소 세트):

1. **`changed_variable`:** `joint_micro_satisfaction_before_bridge_union`
2. **`forbidden_primary_path`:**
   - `dd_headroom_first_bridge_archetype_preselection` (F25 path)
   - `density_first_bridge_score_or_posthoc_dd_repair_as_primary_proxy` (F24 path)
   - `validation_oos_targeted_capped_filter_repair` (F25C rejected path)
3. **`selection_split`:** `train_only`
4. **`forward_splits`:** `validation_oos_read_only` — no val/OOS in ranking or repair(순위·수리에 검증/표본외 미사용)
5. **`micro_gate_contract`:** explicit six-condition joint gate(명시적 6조건 합동 게이트):
   train PF ≥ 1.18, train DD ≤ 14%, density 2–6/day, equity R² ≥ 0.70, max loss streak ≤ 18, adverse loss p10 ≥ source median
6. **`union_gate_contract`:** same-side pair/triple OR-union(같은 방향 쌍/삼중 OR 합집합); density 5–10/day; bridge train PF ≥ 1.10; bridge train DD ≤ 16%; overlap ≤ 0.40; min unique density contrib ≥ 0.40
7. **`scoring_contract`:** `joint_micro_satisfaction_score` formula **written and distinct** from F25 `train_archetype_score` and F24 `bridge_score` — must encode micro joint satisfaction + union overlap/unique contrib, **not** DD-headroom-first as primary term(주항이 아님)
8. **`structural_unit` / `duplicate_trade_rule` / `opposite_side_rule`:** carry F25 semantics(전선25 의미 유지)
9. **`no_repair_in_frontier26b`:** primary proxy is pre-union component gate only(합집합 전 게이트만)
10. **`no_onnx_until_handoff` / `no_lifecycle_until_seed`:** unchanged runtime boundaries(런타임 경계 유지)
11. **`unchanged_gate_thresholds`:** scout PF≥1.10, density 5–10/day, forward DD≤25%; seed PF≥1.20, DD≤18%; handoff PF≥1.50, DD≤12% + smoothness proxy(매끄러움 프록시)
12. **`non_repeat_proof`:** compare F26B top-10 `micro_ids` against **both** F25B top-10 and F24B top-10; overlap without seed-gap lift = repeat(중복만 있고 씨앗 간격 개선 없으면 반복)
13. **`reference_only_prior_artifacts`:** F24/F25 outputs are clues, not baselines/winners(단서만, 기준선/승자 아님)

**Blocked open(개방 차단):** F26A ships without items 5, 6, 7 written in lock JSON + stage-open report(잠금 JSON·개방 보고서에 미기재).

---

## 4. Smallest F26B proxy(가장 작은 전선26B 프록시)

**F26B only — one pass, no F26C repair(한 번만, 수리 없음).**

1. Rebuild micro pockets via existing chain(기존 체인): F23B frame → F23C repair candidates → F24B `build_micro_pockets` (same inputs as F25B).
2. **Apply joint micro satisfaction filter first(먼저 합동 필터)** — emit `micro_joint_pass_audit.csv` with pass/fail per condition and count vs F25’s 16/80 eligible(전선25 16/80 대비).
3. From passing micros only(통과 미세만), build same-side pair/triple OR-unions with union gates(합집합 게이트).
4. Rank survivors by **train-only** `joint_micro_satisfaction_score`(학습 전용 점수).
5. Attach validation/OOS as **read-only** scout/seed/handoff flags(읽기 전용 플래그).
6. Run non-repeat audit vs F25B + F24B top-10 `micro_ids`.
7. **Defer ONNX/MT5 entirely(완전 연기)** until `handoff_candidate_rows > 0`.

**Smallest meaningful scope(최소 의미 범위):** do not add WFO, lifecycle repair, or threshold sweeps on val/OOS(검증/표본외 스윕 없음). The hypothesis lives or dies on whether **stricter pre-union component quality(합집합 전 구성 품질 강화)** breaks the F25 seed DD gap(씨앗 손실폭 간격) without repair.

**Early invalid shortcut(조기 무효 단축):** if joint micro gate yields **zero** passing micros or **zero** unions, stop before expensive ranking(순위 전 중단) — that is `invalid_setup`, not “run harder.”

---

## 5. Stop conditions(중지 조건) — negative or invalid(부정·무효 마감)

| Class(분류) | Condition(조건) | Closeout label(마감 라벨) |
|---|---|---|
| **Invalid setup(무효 설정)** | Joint micro gate → 0 passers, or 0 pair/triple unions after union gates | `invalid_setup_joint_gate_collapsed` |
| **Repeat(반복)** | F26B top-10 `micro_ids` substantially overlap F25B top-10 **and** closest seed-gap row still fails seed DD cap with same PF/DD tradeoff shape(동일 상충 형태) | `repeat_of_f25_union_surface` |
| **Negative memory confirmed(부정 기억 확정)** | `seed_surface_rows = 0` and `handoff_candidate_rows = 0`, and best forward-read row still scout-only with forward max DD > 18% on closest PF-ready row(가장 가까운 PF 충족 행도 손실폭 초과) | `preserved_clue + negative_memory`: *joint micro gate did not break seed tradeoff* |
| **Tightening-only negative(임계값만 강화 부정)** | Eligible micro count collapses (e.g. ≪ F25’s 16) **and** scout count drops vs F25B 17 **without** any row improving forward min PF or reducing seed-gap DD vs `f25b_0001` | `negative_memory_threshold_collapse_no_lift` |
| **Repair-only escape(수리만으로 탈출)** | Any seed/handoff appears only after adding val/OOS-targeted capped repair | Close as F25C repeat — *pre-union gate insufficient; repair-only path forbidden* |
| **Preserved-clue-only(보존 단서만)** | Non-zero scouts, F25B overlap = 0 or low, but all rows fail seed DD or seed PF | `preserved_clue + negative_memory` (same family as F24D/F25D) |
| **Blocked open(개방 차단)** | F26A missing score formula or F25 forbidden path not locked | Do not run F26B |

**Practical negative bar(실무 부정 기준)** — same as F25 closeout logic(전선25 마감 논리 동일): if after F26B the closest seed-gap row still looks like `f25b_0001` (forward min PF ≥ 1.20 but forward max DD > 18%), and bottleneck split remains PF-ready/DD-blocked dominant(수익 팩터 충족·손실폭 차단 우세), close F26 without F26C repair(수리 없이 마감).

---

## Plain read(쉬운 요약)

F25 proved that **re-ranking unions for DD headroom(합집합을 손실폭 여유로 재순위)** can find new scouts but not seeds. F26 asks a fair next question: **were bad micro pockets allowed into the union in the first place?(애초에 약한 미세 구간이 합집합에 들어갔는가?)** That is a new hypothesis if F26A locks component-level joint gates and a distinct train-only score — not another DD-headroom reweight.

**Accept F26A open(전선26A 개방 수용).** Smallest test = one F26B pass: filter micros hard on train, then union, then read val/OOS as flags only. Close negative if seed tradeoff unchanged; close invalid if the joint gate leaves nothing to union.

---

### Codex receipt fields(코덱스 영수증 필드) — for F26A materialization(물질화용)

| Field(필드) | Value(값) |
|---|---|
| `trigger_reason` | User-requested Frontier26 stage-open external review |
| `review_size` | small review |
| `advice_classification` | **accepted** — acceptable_new_hypothesis with lock prerequisites |
| `forbidden_claim_check` | pass — no authority/baseline/promotion/live/Goal Achieve claimed |
| `needs_local_verification` | F26A must verify lock JSON + Grok packet receipt before F26B |

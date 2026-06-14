Proposed Frontier24 개방 방향만 검토합니다. 먼저 관련 스킬·정책·F23 마감 근거를 확인해 제한된 맥락에서 판단하겠습니다.
## Verdict: **needs_local_verification** (조정 후 수용 방향)

**Review size(검토 크기):** medium review — F23 closeout snapshot(마감 스냅샷) + proposed F24 opening contract(개방 계약) only.

**Forbidden-claim check(금지 주장 확인):** pass — no operating promotion, runtime authority, baseline, live readiness, or Goal Achieve implied.

---

### Q1. New hypothesis lifecycle(새 가설 생명주기) vs F23 repair repeat(전선23 수리 반복)?

**Mostly yes, not a naked F23C repeat.**

Local files match your snapshot: F23 closed as preserved clue + negative memory, seed/handoff 0/0, and `negative_memory.md` explicitly reopens only when **density bridge(빈도 연결)** or **DD normalization(손실폭 정규화)** is the new structural unit.

F24’s novelty delta is real on paper:
- F23: **single pocket(단일 구간)** + train-only entry-known include/veto repair(진입시점 포함/제외 수리)
- F24: **multi-pocket OR-union assembly(다중 구간 OR 합집합 조립)** + compatibility/diversity guards(호환성/다양성 보호)

That satisfies `frontier_governance.md` “new frontier when validation philosophy / structural unit changes,” not just another capped repair pass.

**Risk:** if F24A only re-ranks the same F23 pockets with a thin union wrapper and no operational overlap/correlation rules, it collapses back into F23C repair. Codex must make the assembly contract executable, not rhetorical.

---

### Q2. Density bridge first, DD first, or two-step(2단계)?

**Two-step design; density bridge first in F24A.**

F23 clues are three separable failure axes, not one joint failure:

| Clue | Signal |
|------|--------|
| `f23c_0071` | high PF, low density — primary bridge input |
| `f23c_0123` | density OK, OOS PF weak — bridge may raise density but erode PF |
| `f23c_0233` | PF+density OK, DD fail — different lever |

Mixing density bridge + DD normalization in one train-only ranking objective in F24A will blur causality. Recommended sequence:

1. **F24A/B:** density bridge only; DD is diagnostic + stop gate, not co-optimized.
2. **F24C or later packet:** DD normalization only if a bridge candidate hits 5–10/day but fails DD ≤ 25%.

Do **not** open with DD-first; F23’s reopen condition names density bridge as the unanswered structural question.

---

### Q3. Success / seed / handoff criteria — too loose or strict?

**Scout/seed: appropriately bounded for Tier A proxy. Handoff: correctly strict but underspecified.**

- **Scout PF ≥ 1.10:** reasonable; `f23c_0123` OOS PF 1.08388 is a useful floor reference. Add a **minimum trade-count / window stability(최소 거래 수/구간 안정성)** guard or scout will accept thin samples.
- **Seed PF ≥ 1.20, DD ≤ 18%:** fair step-up from scout; aligns with “near-seed, no handoff” F23 pattern.
- **Handoff PF ≥ 1.50, DD ≤ 12%:** correct given 0/0 handoff from F23 and forbidden ONNX/MT5 until handoff exists.
- **Gaps before materialize:**
  - “reasonable smoothness(매끄러움)” is undefined — needs a proxy metric (e.g. sub-period PF variance, worst-month DD).
  - “5–10 trades/day(일 5~10회)” needs calendar/session definition and Tier A proxy measurement path.
  - Stop rule “OOS PF < 1.10” is good; add **union overlap collapse(합집합 중복 붕괴)** as explicit negative memory if added density is mostly duplicate entries across micro-pockets.

Overall: **not too loose for exploration; slightly under-specified for reproducible closeout.**

---

### Q4. Local verification Codex must require before F24A materialization

Minimum gate before `frontier24A_stage_open_density_bridge_payoff_pockets_hypothesis_design_v1`:

1. **Ledger replay(장부 재확인):** `f23c_0123`, `f23c_0071`, `f23c_0233` metrics match `preserved_clue.md` / closeout report; F23B/F23C seed/handoff remain 0/0 in `stage_run_ledger.csv`.
2. **Opening contract completeness(개방 계약 완성):** `00_spec` must include frontier thesis, novelty delta, prior-stage scan, do_not_repeat (carry F23 entry-known-only + no lifecycle/ONNX/MT5), exit rule, claim boundary — per `frontier_governance.md`.
3. **Micro-pocket lineage(미세 구간 계보):** document whether pockets are re-derived from F23 payoff-asymmetry proxy or freshly mined; if reused, cite artifact paths/hashes.
4. **OR-union semantics(OR 합집합 의미):** define duplicate-trade handling, overlap penalty, and whether union is entry-time OR or signal-family OR.
5. **Compatibility/diversity guards(호환성/다양성 보호):** operational rules (e.g. max pockets per family, min feature-family distance) — not just selection weights.
6. **Split discipline(분할 규율):** train-only ranking vs read-only validation/OOS; same split identity as F23 locked proxy unless explicitly changed with rationale.
7. **Tier labeling(티어 라벨링):** Tier A proxy only; Tier B `missing_required`; Tier A+B `out_of_scope_by_claim` — written in spec, not implied.
8. **Pre-registered stop/negative-memory templates(사전 등록 중단/부정기억 템플릿):** union raises density but OOS PF < 1.10; or DD > 25% after capped repair — with artifact paths to record.

---

### Concise critique(간결한 비판)

**Strengths(강점):** Direction is coherent with F23 closeout, addresses the documented reopen condition, keeps claim boundary tight, and gates ONNX/MT5 correctly.

**Weaknesses(약점):** OR-union is the whole thesis but overlap/correlation/smoothness are still verbal; combining DD optimization too early would repeat F23’s “joint PF/density/DD failure” blur; density target needs measurement contract.

**Adjustment(조정):** Accept opening **after** Codex pins union semantics + two-step scope (bridge first, DD second packet). Without that, treat as **rejected** as disguised F23C repair.

---

**Classification for Codex receipt(코덱스 영수증 분류):**
- Direction: **accepted_with_adjustments**
- Materialize F24A now: **needs_local_verification** (items 3–8 above)
- Forbidden claims: **none detected**

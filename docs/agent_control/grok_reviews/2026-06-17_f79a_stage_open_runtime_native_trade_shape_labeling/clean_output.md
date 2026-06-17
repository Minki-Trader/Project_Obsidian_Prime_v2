## Grok Review — F79 Stage-Open Direction

**Advice classification(조언 분류):** `accepted_with_conditions(조건부 수용)`

---

### 1. Is the direction broad and novel enough?

**Yes — substantively yes(실질적으로 예).** The F79 axis contract(축 계약) directly maps to all six dimensions the user named, and it is a **topic pivot(주제 전환)**, not F78 threshold repair(임계값 수리) dressed up as a new stage.

| User concern(사용자 우려) | F79 response(대응) | Why it is not “F78 again”(왜 F78 반복이 아닌지) |
|---|---|---|
| feature_set(피처 묶음) | full58, contract_core, price_vol_session, **runtime_fill_context**, ablations | Separates **source value(원천 가치)** from parity-only repair(동등성 단독 수리) |
| label_target(라벨/목표) | same-bar / next-tick **fill-path**, first-touch, MAE/MFE, DD-normalized utility, density quota | Attacks F78’s core failure: **proxy timing(프록시 시각)** vs **MT5 same-bar execution(MT5 동일 봉 실행)** |
| model_family(모델 계열) | logistic/ridge → HistGBM → ExtraTrees → shallow additive → small NN | Tests whether any signal is **label-specific bias(라벨 특이 편향)** vs real edge |
| trade_shape(거래 형태) | long/short/both, delay, SL/TP first-touch, hold grid, cooldown, one-position | Treats **trade count(거래 수)** as **lifecycle(생명주기)**, not independent signal count |
| risk_logic(위험 로직) | Deposit=500 DD, fixed lot, spread cost, MAE gate, streak/daily guards | Puts **DD denominator(손실폭 분모)** in the research loop before MT5 materialization |
| regime_session_split(장세/세션) | cash_open/mid/late, vol/trend/chop, DOW | Rotates **topic surface(주제 표면)** without hiding overfit in one tiny slice |

**Novelty anchor(새로움 핵심):** F78 negative memory(부정 기억) says “next-bar positive → same-bar negative” and “threshold/model-only repair → repeat repair.” F79 moves the hypothesis to **runtime-native labeling from fill path(체결 경로 기반 런타임 네이티브 라벨링)** — that is the right pivot, not a wider threshold grid.

**Claim boundary(주장 경계) is respected:** this is **stage_open_design_only** — no completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve.

---

### 2. Proxy scout(프록시 탐색) → mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)?

**Conceptually properly scoped(개념적으로 범위 적절) — with conditions(조건부).**

What already fits the snapshot:

- **Preserved clue(보존 단서):** ONNX/EA parity(동등성) + **selected-entry veto tape(선택 진입 거부 테이프)** are the right bridge from proxy counts to runtime signal counts.
- **Label axis(라벨 축)** bakes in entry timing(진입 시각) and DD denominator(손실폭 분모) at design time — aligns with F78’s “must be explicit from the start.”
- **Conditional probe(조건부 탐침):** F78 already showed **scout clue 0 / meaningful signal 0** after alignment repairs; “probe if signal exists(신호가 있으면 탐침)” avoids another empty MT5 cycle.

What the snapshot does **not** yet pin down (hence conditions):

1. **Explicit scout gate(명시적 탐색 게이트)** — minimum proxy criteria before any MT5 run (e.g. non-zero meaningful signal on Tier A validation, not just positive in-sample metric).
2. **Combinatorial budget(조합 예산)** — six axes × broad sweeps can explode; need **staged waves(단계적 파도)** (label + trade_shape first, then feature ablation, then model_family), with **stop rules(중단 규칙)** per wave.
3. **Export constraint lane(보내기 제약 레인)** — small NN / non-tree families need a **parity-export eligibility rule(동등성·보내기 적격 규칙)** so scout doesn’t chase non-materializable winners.
4. **Tier A / Tier B paired record(티어 A·B 쌍 기록)** — not in this snapshot; if F79 follows post–Stage 10 alpha rules, separate + combined records must be planned or marked `missing_required` — not a reason to reject open, but a **scope add-on(범위 추가)**.

**Effect(효과) of conditions:** proxy scout stays cheap and honest; MT5 probe runs only when there is something worth falsifying under same-bar execution, using veto tape as the count-alignment tool — not as a substitute for edge.

---

### 3. Conditions for Codex(코덱스 조건) — before execution, not before stage open

1. **Wave-0 contract(0단계 계약):** lock label_target + trade_shape + risk_logic definitions (including DD denominator and fill ordering) before large feature/model sweeps.
2. **Scout-to-probe gate table(탐색→탐침 게이트 표):** write numeric/text thresholds for “signal exists” (meaningful signal count, min trades, min utility after spread, etc.).
3. **Sweep cap(탐색 상한):** max variants per axis per wave; document what is `broad_sweep` vs `deferred`.
4. **Carry forward(이월):** veto tape + parity tooling as **mandatory probe precondition(필수 탐침 전제)**, not optional F78 artifact.
5. **Negative-memory guard(부정 기억 보호):** if a variant only wins on next-bar proxy but fill-path / same-bar label is flat or negative → label as **proxy-only failure(프록시 단독 실패)**, do not escalate to threshold repair.

---

### 4. Summary verdict(요약 판정)

| Question(질문) | Grok answer(그록 답) |
|---|---|
| Broad enough for six-axis experimentation?(6축 실험 변화 충분?) | **Yes** — axis contract is complete and orthogonal enough |
| Novel enough vs F78 repair loop?(F78 수리 반복 대비 새로움?) | **Yes** — fill-path / runtime-native labeling is the right pivot |
| Proxy scout → MT5 probe scoped correctly?(프록시→MT5 탐침 범위?) | **Mostly yes** — conditional probe + preserved parity tools; needs explicit gates and wave budget |
| **Classification(분류)** | **`accepted_with_conditions`** |

**Final Codex direction(최종 Codex 방향):** Open F79 as proposed. Treat the axis table as the **exploration mandate(탐색 의무)**, not a single-run checklist. Local verification(로컬 검증) is still required later for dataset column readiness, veto tape wiring, and export paths — but that does not block **design-only stage open(설계 전용 단계 개방)** under the stated claim boundary.

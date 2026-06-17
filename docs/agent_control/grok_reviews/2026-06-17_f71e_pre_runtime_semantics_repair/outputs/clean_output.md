## Advice classification(조언 분류): **accepted(수용)** — with bounded preconditions(제한 전제조건)

Codex should run **one** F71E MT5 repair probe on **`edge_margin q40`**, not pause for a broader MT5 sweep yet. From this snapshot alone, that is the best next action inside the stated claim boundary(주장 경계).

---

## Why accepted(수용 이유)

**1. Root-cause chain is coherent(근본 원인 연쇄가 일관됨).**

- ONNX probability parity(온엑스 확률 동등성) and signal parity(신호 동등성) passed with zero split diffs.
- Feature readiness diff(피처 준비 차이) is `0`.
- Runtime telemetry(런타임 기록) is dominated by `edge_margin_not_met(엣지 마진 미달)`.
- F71B proxy used a **custom score(맞춤 점수)**; EA used **`edge_margin(엣지 마진)`** only.

That pattern fits **threshold semantics mismatch(임계값 의미 불일치)** much better than ONNX failure, feature failure, or generic runtime noise. A repair probe that keeps model/label/features fixed and only aligns selection semantics is the right narrow experiment.

**2. `edge_margin q40` is a defensible single-probe pick(단일 탐침 선택으로 타당함).**

Among the listed local repairs, q40 has the **strongest OOS PF(표본외 수익 팩터)** (`1.2351`) while still marking `scout=true`. Codex’s stated goal — test whether **signal-count parity(신호 수 동등성)** recovers under EA-compatible semantics — matches a **one-shot semantics-alignment test(의미 정렬 1회 시험)**, not a promotion pick.

**3. Claim boundary stays intact(주장 경계 유지).**

This remains a **runtime repair probe(런타임 수리 탐침)** only. It does not justify completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

---

## What would make another action better(다른 행동이 더 나은 경우)

| Alternative(대안) | When better(더 나은 때) | From this snapshot(이 스냅샷 기준) |
|---|---|---|
| **`edge_margin q30`** | Primary success criterion is **validation-side proxy strength(검증 프록시 강도)** or higher expected signal density(예상 신호 밀도) | q30 has higher validation net/PF, but weaker OOS PF. Not clearly better for the stated parity-recovery test. |
| **MT5 sweep of q20–q50** | You need quantile sensitivity mapping before any runtime claim | Over-broad for a first repair probe; wastes MT5 budget before confirming the semantics hypothesis. |
| **Change EA to F71B custom score** | You want proxy authority over EA authority | Out of scope for the proposed F71E repair; would test a different hypothesis. |
| **Skip MT5; proxy-only** | ONNX/signal parity already “proves” runtime | **Rejected(거절)** — F71D already shows proxy and runtime diverge despite perfect ONNX signal parity under the **old** semantics. |

So: **do not skip MT5**; **do not multi-quantile MT5 yet**; **q40 is acceptable over q30** given Codex’s OOS-PF + EA-compat rationale.

---

## Bounded preconditions before/during F71E(제한 전제조건)

These are **needs_local_verification(로컬 검증 필요)** items Codex must check locally; they do not overturn the advice:

1. **Re-materialized signal expectations(재물질화 신호 기대치)**
   Confirm ONNX/signal parity for the **q40 edge_margin** variant, not only F71B custom-score counts (`989 / 345 / 256`). The repair probe’s pass/fail should be judged against **new expected counts(새 예상 신호 수)**.

2. **Primary pass criterion(1차 통과 기준)**
   Judge F71E first on **runtime signal/order recovery vs expected(런타임 신호·주문 대 예상치 회복)** and reduction of `edge_margin_not_met` dominance — not on net/PF/DD matching proxy.

3. **Secondary read(2차 해석)**
   Even if signal parity recovers, proxy/runtime KPI gap may remain from execution, spread, veto tape, or other runtime layers. That would mean **semantics repair partially validated(의미 수리 부분 검증)**, not scout promotion.

4. **q30 fallback rule(대체 규칙)**
   If q40 re-materialization shows **very low expected signal count(예상 신호 수 매우 낮음)** or ONNX parity breaks, prefer **one** fallback probe on q30 rather than an MT5 quantile sweep.

---

## Recommended Codex direction(권장 Codex 방향)

**Run F71E MT5 repair probe on `edge_margin q40`.**

**Success framing(성공 프레이밍)** for this packet only:

- **Pass(통과):** EA-compatible semantics → runtime signals/orders move toward re-materialized expected counts; `edge_margin_not_met` ceases to dominate unexplained gap.
- **Partial(부분):** signal parity improves but KPI still diverges → semantics hypothesis supported; next work is runtime/economics forensics, not another quantile guess.
- **Fail(실패):** signal parity still collapsed with aligned semantics → downgrade threshold-mismatch as sole cause; broaden repair scope under same claim boundary.

---

## Final classification summary(최종 분류 요약)

| Item(항목) | Classification(분류) |
|---|---|
| Align selection to EA `edge_margin`(EA 엣지 마진으로 선택 정렬) | **accepted(수용)** |
| Single F71E MT5 probe on `edge_margin q40` | **accepted(수용)** |
| q40 expected signal counts, materialization integrity, veto/execution effects | **needs_local_verification(로컬 검증 필요)** |
| Completion / baseline / promotion / runtime authority / live readiness / Goal Achieve | **out of scope(범위 밖)** — do not claim |

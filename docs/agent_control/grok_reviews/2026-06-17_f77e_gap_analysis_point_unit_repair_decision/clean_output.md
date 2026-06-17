# F77E Gap Analysis — Grok External Review

## Advice classification(조언 분류)

**`accepted_with_conditions` (조건부 수용)**

The repair **direction** is logically sound. The **exact scale factor (100)** is plausible but not yet proven from this snapshot alone.

---

## Rationale(근거)

### Why the diagnosis fits the evidence(진단이 근거와 맞는 이유)

1. **Signal and feature parity pass, fills are zero** — parity is upstream of the order bridge. That pattern usually means the model path is fine and the failure is in order construction or broker acceptance.

2. **Uniform failure mode** — all 168 attempts: retcode `10016`, comment `Invalid stops`. One consistent error across every order strongly points to SL/TP distance or format, not threshold, ONNX, or signal logic.

3. **Magnitude mismatch** — `open_sl_points=12`, `open_tp_points=18` vs ATR samples ~`1800–2300` broker points. SL/TP are roughly **two orders of magnitude** smaller than typical volatility. That is exactly what you expect if price-unit values (e.g. 12.0 / 18.0 index points) were passed as broker points (0.12 / 0.18 price move on a 0.01-point symbol).

4. **Codex unit-mismatch hypothesis** — F77B proxy treating TP18/SL12 as **raw price units**, F77D EA feeding them as **broker points**, is a standard US100 / index bridge bug. It explains 100% fill failure **after** signal parity without touching model authority.

### Why not full `accepted`(왜 완전 수용이 아닌지)

- Scale **100** is **inferred**, not shown here from symbol contract math or source definitions.
- Other causes can also yield `Invalid stops` (minimum stop level, freeze level, digit normalization, bid/ask side). They are less likely given the ATR vs SL/TP ratio, but should be ruled out with small local checks before another MT5 probe.

### F77F probe design(탐침 설계)

- **Single changed variable** (SL/TP scale only) — good isolation.
- **Same model/tape/threshold/veto** — keeps the negative-control structure.
- **Fallback: max-hold-only, SL/TP disabled** — sound second step if scaling still fails; it separates “order bridge” from “stop geometry.”

**Verdict:** Proceed toward F77F with **unit conversion as the primary hypothesis**, not a different repair axis (threshold, ONNX, feature rebuild) **before** this probe.

---

## Smallest required local checks before F77F(실행 전 최소 로컬 확인)

| # | Check | Purpose |
|---|--------|---------|
| 1 | **F77B proxy SL/TP definition** — confirm numeric 12/18 are price/index units, not already broker points | Validates root cause |
| 2 | **F77D EA input mapping** — trace SL/TP from `.set` / manifest into `OrderSend` stop distance fields | Confirms where the misread happens |
| 3 | **US100 symbol contract** — `_Point`, `digits`, `SYMBOL_TRADE_TICK_SIZE`, `SYMBOL_TRADE_STOPS_LEVEL` (FPMarkets tester) | Derives conversion: `broker_points = price_units / _Point` |
| 4 | **Recompute target stops** — e.g. SL1200 / TP1800 if scale=100; compare to ATR ~2000 and minimum stop level | Confirms proposed values are broker-valid before tester |
| 5 | **One-line parity sanity** — proxy intended SL/TP **price distance** vs EA intended **point distance** after conversion | Catches off-by-10 / off-by-100 without a full probe |

**Do not need before F77F:** model retrain, ONNX schema change, threshold sweep, or feature rebuild — none are supported by this evidence.

---

## Claim boundary respect(주장 경계 준수)

This review supports **gap analysis and repair decision only**. It does **not** justify completion, baseline selection, promotion, runtime authority, live readiness, or Goal Achieve — even if F77F later shows fills.

---

## Summary for Codex(Codex 요약)

| Item | Grok position |
|------|----------------|
| Repair direction | **Yes** — price-unit → broker-point conversion first |
| Scale 100 | **Plausible; verify locally** (checks 1–4) |
| Alternative repair first | **No** — not warranted by this snapshot |
| F77F scope | **Appropriate** with documented fallback |
| Classification | **`accepted_with_conditions`** |

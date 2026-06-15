# Grok Receipt(그록 영수증): stage_open(단계 개방)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier56_stage_open_snapshot`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
# Grok Second Opinion — F56 Frontier Open (Small Review)

**Mode:** snapshot-only (no files, no tools, no local verification)
**Claim boundary:** exploration direction critique only — not completion, baseline, promotion, or runtime authority.

---

## Verdict on “sufficiently new and bounded”

### Accepted — F56 is meaningfully new relative to F55

F55’s recorded failure mode is **density/parity OK, proxy→runtime economics failed**. F56 does not re-litigate sparse admission budget/min-gap repair; it shifts the hypothesis to **upstream label economics**: train a short classifier on train-only labels that favor **stop-avoidance / favorable excursion shape** (positive isolated runtime PnL, non-stop exit, low MAE/ATR, sufficient MFE/ATR).

That is a **different causal lever** than F55’s runtime veto transfer problem. F55 says “the gate worked mechanically but did not buy edge.” F56 says “try to source edge before the gate.” That pivot is coherent and sufficiently new for a frontier open.

### Accepted — F56 is mostly bounded

The experiment boundary you stated is appropriately tight:

- same core feature order
- same US100 M5 Tier A split
- proxy selection first, then **one** MT5 runtime probe
- explicit recording of proxy-runtime gap, PF/DD/density, `signal_diff`, `feature_ready_diff`
- no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claims

The local scout surface (PF ~1.03/1.09, DD ~4.1/3.8, trades/day ~5.1/5.8) is correctly labeled **weak evidence**, not a reason to skip proxy work — but also not a reason to spend MT5 time early.

### Needs_local_verification — two boundedness gaps

1. **Admission path inheritance:** F56 says it is not sparse-admission repair, but if the **same admission shell** from F55 remains unchanged, F56 may only change labels while runtime economics still dies at the same choke point. Local verification should confirm whether F56 changes **only the classifier/label surface** or also anything in admission routing that previously correlated with F55 veto behavior.

2. **F52 overlap boundary:** F52 already showed **DD compression without PF recovery**. F56’s MAE/MFE framing risks becoming “another DD-shaping mechanism” unless success/failure criteria explicitly require **PF lift**, not DD improvement alone. That boundary is stated in the preserved clue, but implementation can still drift unless written into the stage stop conditions.

---

## Biggest failure risks (ranked) before proxy + MT5 time

### 1. Accepted — **F55-class proxy→runtime economics collapse** (highest risk)

F55 is the dominant negative memory: `signal_diff=0`, `feature_ready_diff=0`, yet validation/OOS PF = 0.42/0.64. F56’s scout proxy PF ≈ 1.03/1.09 is **barely above 1.0** and lives entirely on the proxy side.

**Risk:** you implement labels + ONNX, proxy looks acceptable, then MT5 reproduces F55’s pattern — mechanical parity, economic failure.
**Implication:** MT5 should remain **post-proxy selection only**, and proxy selection should require margin above “barely profitable,” not just PF > 1.

### 2. Accepted — **Label-definition circularity / leakage**

Labels requiring positive isolated runtime PnL, non-stop exit, low MAE/ATR, and high MFE/ATR are path-dependent and threshold-dependent (`mae_q`, `mfe_q`, `score_q`).

**Risks:**
- quantile cuts tuned on the same era that later serves validation/OOS
- labels encoding exit mechanics that MT5 does not reproduce bar-for-bar
- “non-stop exit” in proxy not matching broker spread/slippage/stop placement in tester

This can produce a classifier that learns **proxy path artifacts**, not transferable short edge.

### 3. Accepted — **Threshold fragility on weak scout evidence**

`mae_q=0.55`, `mfe_q=0.55`, `score_q=0.75` giving PF 1.026/1.086 is a **single-point surface**, not a stable region. Small quantile shifts can erase edge; validation/OOS separation is thin.

**Risk:** you spend implementation time on a surface that is noise around 1.0 PF.
**Implication:** before MT5, proxy work should include **neighborhood/stability checks**, not only the one scout point — even if that stays proxy-only.

### 4. Accepted — **Repeating F52’s lesson: DD improvement without PF source**

F52 compressed DD (7.36/2.50) but PF still failed (0.41/0.66). F56’s MAE/MFE stop-avoidance labels may again improve trade **shape** while failing to improve **expectancy**.

**Risk:** stage closes with “better DD, still dead PF,” which is a clue, not a win.
**Implication:** stage success criteria should treat **PF improvement as primary**, DD as secondary diagnostic.

### 5. Needs_local_verification — **Short-only asymmetry and density side effects**

A short-only ONNX classifier may change trade mix, holding time, and stop-hit rates differently from F55’s balanced runtime profile. F55 had ~5.2–5.4 trades/day with parity; F56 scout is similar, but short-biased selection can break differently under MT5.

**Risk:** new `signal_diff` / density drift appears, confounding economics attribution.
Cannot judge severity from snapshot alone.

### 6. Needs_local_verification — **“Isolated runtime PnL” operational definition**

The phrase is load-bearing. If isolation rules differ between label generation, proxy scoring, and MT5 position lifecycle, the classifier may optimize for trades that are not **isolated** in runtime.

**Risk:** semantic mismatch between label universe and tester trade accounting.
Needs local definition audit before trusting any proxy uplift.

### 7. Accepted — **MT5 timing risk if spent too early**

Given F55, spending Strategy Tester time **before** proxy shows:
- PF margin comfortably above 1.0 on validation **and** OOS
- stability around quantile thresholds
- explicit check that predicted trades are not mostly “would-have-been-stop-outs” under conservative spread/slippage assumptions

is likely to repeat an expensive inconclusive probe.

---

## Advice classification summary

| Advice | Classification |
|--------|----------------|
| Open F56 as a new frontier stage focused on label-sourced PF edge, not F55 admission repair | **Accepted** |
| Keep experiment bounded: same features/split, one MT5 probe after proxy selection | **Accepted** |
| Treat scout PF 1.03/1.09 as weak evidence only | **Accepted** |
| Primary pre-MT5 failure risk is F55-style proxy→runtime economics gap | **Accepted** |
| Second major risk is MAE/MFE label leakage / proxy path artifact | **Accepted** |
| Third major risk is single-point quantile fragility near PF=1 | **Accepted** |
| Require PF-first success criteria to avoid F52-style DD-only wins | **Accepted** |
| Defer MT5 until proxy margin and threshold stability are stronger | **Accepted** |
| F56 is safe to implement without checking admission-path inheritance from F55 | **Needs_local_verification** |
| Short-only classifier will preserve F55-like density/parity | **Needs_local_verification** |
| “Isolated runtime PnL” is consistently defined across label/proxy/MT5 | **Needs_local_verification** |

---

## Practical pre-implementation guardrails (snapshot-based)

1. **Write F56 failure modes explicitly:** parity pass + PF fail (F55), DD pass + PF fail (F52), proxy pass + MT5 fail (combined).
2. **Proxy gate before MT5:** require validation **and** OOS PF above a margin band, not barely > 1, plus local sensitivity around `mae_q/mfe_q/score_q`.
3. **Attribute outcomes:** separate “label quality,” “classifier ranking,” “admission density,” and “runtime economics” so closeout does not blur them.
4. **One MT5 probe only after proxy selection** — aligned with your stated boundary and with F55’s lesson on expensive inconclusive tester runs.

**Bottom line:** F56 is **sufficiently new and sufficiently bounded** to open as a frontier exploration stage, provided closeout criteria stay PF-first and MT5 remains the final narrow check, not the discovery engine. The largest risk is not lack of novelty — it is **re-running F55’s economics failure with a slightly better proxy story**.

## accepted(수용)

- **Capped repair framing(상한 있는 수리 프레이밍)** is valid: F68H isolates **runtime risk envelope(런타임 위험 봉투)** only and holds **ONNX(온엑스)**, **feature order(피처 순서)**, **thresholds/margin(임계값/마진)**, **max hold(최대 보유)**, and **signal/feature parity(신호/피처 동등성)** fixed from F68F. That matches F68G’s “risk envelope repair required(위험 봉투 수리 필요)” without reopening the ONNX repair axis.
- **Three-variant bracket(3변형 꼬리표)** is a sensible probe design: `f52_*` as **preserved clue replay(보존 단서 재생)**, `tight_*` for **DD compression pressure(손실폭 압축 압박)**, `wide_*` for **PF preservation pressure(수익 팩터 보존 압박)**. This directly tests the stated question: can DD compress materially without killing PF, net, and density.
- **Claim boundary(주장 경계)** is appropriate: **runtime probe observation only(런타임 탐침 관찰 전용)** after F68F parity success and high DD (validation 25.06%, OOS 19.57%) with thin validation PF (1.01).
- **Validation + OOS(검증 + 표본외)** for all variants is correct; F68F already shows split asymmetry (validation weaker than OOS), so both splits must stay in the read.
- Using F52 only as **reference clue(참조 단서)**, not **inherited authority(상속 권위)**, is the right posture given “DD under 10% but PF failed there.”

## rejected(거절)

- Do **not** treat F68H as **completion(완성)**, **baseline(기준선)**, **promotion(승격)**, **runtime authority(런타임 권위)**, **live readiness(실거래 준비)**, or **Goal Achieve(목표 달성)** even if one variant improves DD.
- Do **not** infer ATR SL/TP is a **new PF source(새 수익 팩터 원천)**; it is exit/risk shaping on an already marginal validation edge.
- Do **not** use F52 “DD under 10%” as a **target gate(목표 게이트)** for this probe; history says that path likely trades PF away.
- Do **not** fold **density repair(밀도 수리)** into this packet’s success claim. Validation trades/day (3.97) is still below OOS (4.78); ATR stops may reduce density further.
- Do **not** broaden scope mid-probe (thresholds, cooldown policy beyond the table, feature/model changes, or extra variants) without a new bounded packet.
- Do **not** rank variants as “winner” from OOS alone; validation PF 1.01 is the fragile line that must stay visible.

## needs_local_verification(로컬 검증 필요)

**Before MT5(실행 전)**

- **Handoff identity(인계 정체성)**: ONNX model sha256 `ab632bd1...`, feature order hash `14a037f1...`, feature count `49`, same feature CSV as F68F.
- **Variant binding(변형 바인딩)**: each `.set`/manifest maps exactly to ATR stop/TP, reentry cooldown `3`, same-direction cooldown `6`, close-on-flat `True`, reverse-on-opposite `True`, max hold `2`.
- **Intentional delta vs F68F(F68F 대비 의도된 차이)**: F68F had **ATR SL/TP disabled(비활성)**; confirm only ATR envelope toggles on. Verify reentry cooldown `3` is deliberate (F68F table emphasized same-direction `6` only).
- **Tester parity(테스터 동등성)**: same broker/symbol/periods, spread/commission/slippage/deposit/modeling mode as F68F so deltas are attributable to risk envelope, not setup drift.
- **F68F baseline row(기준선 행)**: either re-attach F68F receipts in the same comparison frame or explicitly pin F68F KPIs as the control; do not compare variants in isolation.

**After MT5(실행 후)**

- Per variant, per split: **net profit(순수익)**, **PF(수익 팩터)**, **DD%(손실폭)**, **trades/day(일 거래)**, plus **delta vs F68F(F68F 대비 차이)** on all four.
- **Materiality rule(유의미성 규칙)** pre-declared: e.g. DD drop meaningfully (snapshot suggests double-digit validation DD is the pain point) while PF stays above validation baseline ~1.01 and net does not collapse.
- **Trade-shape forensics(거래 형태 포렌식)**: stopped-out rate, avg hold, win rate, gross profit/loss mix — to see whether DD relief is real risk control vs profit amputation.
- Confirm no regression in **signal/feature parity(신호/피처 동등성)** identity chain (risk-only change should not alter model path, but configs must not accidentally touch inference inputs).

## drift risks(드리프트 위험)

- **F52 repeat failure(F52 반복 실패)**: DD compression with PF collapse — especially on `tight_atr06_tp10` and `f52_atr08_tp12`.
- **Density erosion(밀도 침식)**: tighter stops cut trades/day; may worsen validation density already below OOS.
- **Split illusion(분할 착시)**: OOS-only improvement while validation stays ~PF 1.0 or net near zero — same fragility as F68F.
- **Axis conflation(축 혼동)**: treating DD gains as closure on F68’s full economics story when F68G still left density/validation edge open.
- **Cooldown drift(쿨다운 드리프트)**: reentry `3` plus ATR exits may change transition behavior vs F68F in ways not captured by “same ONNX” alone.
- **Over-interpretation of preserved clue(보존 단서 과해석)**: `f52_*` replay is diagnostic, not proof the clue still transfers under current F68F signal stack.

## final recommendation(최종 권고)

**Run(실행)** — with pre-run local verification above and a fixed comparison matrix vs F68F.

F68H is a **valid capped repair probe(유효한 상한 있는 수리 탐침)** after F68F: narrow axis, controlled constants, bracketed variants, aligned with F68G. **Revise(수정)** only if handoff/hash/set binding or tester parity fails preflight. **Stop(중단)** only if preflight shows variant configs also touch model/threshold/feature path.

**Read discipline(판독 규율)**: useful probe if any variant shows **material DD compression(유의미한 손실폭 압축)** on validation and/or OOS **without** destroying PF, net, and trades/day vs F68F; if all three variants only replay the F52 tradeoff (lower DD, broken PF or net), record as **negative risk-envelope evidence(부정적 위험 봉투 근거)** and plan the next bounded axis — still **no authority(권위 없음)**.

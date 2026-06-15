# Grok Receipt(그록 영수증): stage_open(단계 개방)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier61_stage_open_review/small_review`
- classification(분류): `needs_local_verification`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), hashes(해시), ledgers(장부), MT5 output(MT5 출력)으로 다시 검증한다.
- effect(효과): Grok output(그록 출력)은 authority(권위)가 아니라 bounded critique(제한 비판)로만 쓰인다.

## Clean Output(정리 출력)
# Frontier61 Stage Open Review — External Second Opinion(외부 2차 의견)

**Verdict(판정): `needs_local_verification`**

The F61 **opening direction(개방 방향)** is **coherent as an exploration-only pivot(탐색 전용 전환)** after F53–F60 axis-repair failures, but this snapshot alone is **not enough to accept implementation(구현 수용)**. Codex(코덱스) should run the local checks below before stage open work starts.

---

## Why not `rejected`(거절 아님)

From the snapshot only:

1. **Problem framing(문제 정의)** matches prior memory(이전 기억): short-axis(숏 축) and long-axis(롱 축) repairs both failed MT5 PF(런타임 탐침 PF). Moving from **direction repair(방향 수리)** to **side allocation(방향 배분)** as the model target is a **logical novelty delta(논리적 신규성 차이)**.
2. **Bounded plan(제한 실행 계획)** is appropriate: small capped proxy grid(상한 있는 프록시 격자) → **one runtime probe candidate(런타임 탐침 후보 1개)** → mandatory validation_is + OOS. That fits an exploration-only runtime probe stage.
3. **Claim boundary(주장 경계)** and **do-not-repeat(반복 금지)** are correctly conservative: no baseline(기준선), promotion(승격), runtime authority(런타임 권위), or proxy-PF overclaim(프록시 PF 과주장).
4. F60 negative memory(부정 기억) (validation_is PF=0.41, OOS PF=0.51) supports **not** another axis-only repair pass.

---

## Why not `accepted` yet(아직 수용 불가)

The snapshot does **not** prove that F61 fixes the failure mode(실패 모드) behind F53–F60. Side allocation(방향 배분) may still fail if the real gap is **proxy–runtime parity(프록시–런타임 동등성)**, **execution envelope mismatch(실행 봉투 불일치)**, or **feature-contract weakness(피처 계약 약점)** — not label geometry(라벨 구조) alone.

---

## Concrete risks(구체적 리스크) — from snapshot only

| Risk(리스크) | Why it matters(왜 중요한지) |
|---|---|
| **Relabeling ≠ new alpha(재라벨링 ≠ 새 알파)** | Same US100 M5 feature contract(피처 계약) failed on short-only and long-only targets. A 3-class head may only repackage the same weak signal. |
| **Flat dominance(무거래 클래스 지배)** | Labels that require beating flat + margin(마진) often make **flat(무거래)** the majority class. Model may collapse to **no-trade(거래 없음)** or sparse trades with no PF lift. |
| **Label optimism in proxy(프록시 라벨 낙관)** | Comparing executable long vs short under one ATR SL/TP/max-hold envelope(ATR 손절/익절/최대보유 봉투) can look good offline but diverge under MT5 spread, slippage, and fill logic. |
| **Margin/threshold grid too small(격자 과소)** | A “broad but capped” grid may **under-explore** decision boundary or **overfit** one lucky combo — especially with only **one** frozen runtime candidate. |
| **Failure mode misdiagnosis(실패 모드 오진)** | F53–F58 “did not transfer to MT5” may be parity/handoff, not directional scoring. F61 does not explicitly test that hypothesis in the snapshot. |
| **Tier B / combined gap(티어 B/합산 공백)** | Plan mentions Tier A(티어 A) and Tier B/combined status(티어 B/합산 상태) but snapshot gives no Tier B design. Paired-tier discipline may be incomplete at open. |
| **Inherited friction memory not used structurally(마찰 기억 미반영)** | F60 `negative_memory_long_axis_friction_escape_failed_pf` is recorded, but snapshot does not say how that constrains F61 labels, features, or admission — only “don’t inherit baseline.” |

---

## Required local checks before implementation(구현 전 필수 로컬 검증)

Codex(코덱스) should verify locally; Grok(그록) cannot from this snapshot:

1. **Failure-mode audit(실패 모드 감사)**
   For F53–F60, separate **alpha failure(알파 실패)** vs **parity/handoff failure(동등성/인계 실패)**. If parity dominated, F61 needs a **narrow parity preflight(좁은 동등성 사전확인)** before training spend.

2. **3-class label contract(3분류 라벨 계약)**
   Document: flat definition(무거래 정의), margin rule(마진 규칙), tie-break(동점 처리), class balance on Tier A(티어 A 클래스 분포), and whether labels use **only past-closed-bar(과거 확정 봉만)** information.

3. **Feature contract unchanged check(피처 계약 불변 확인)**
   Confirm F61 uses the **same** US100 M5 feature contract as F53–F60, with an explicit list of **what changes vs what is frozen(변경/고정 항목)**.

4. **Proxy grid freeze rule(프록시 격자 동결 규칙)**
   Pre-register: grid size cap(격자 상한), selection metric(선택 지표), and **one-candidate freeze criterion(후보 1개 동결 기준)** so F61 does not drift into many tiny threshold repairs.

5. **Runtime probe parity checklist(런타임 탐침 동등성 체크리스트)**
   Before MT5: model bundle hash(모델 번들 해시), threshold/margin mapping(임계값/마진 매핑), EA parameter surface( EA 파라미터 표면), validation_is/OOS window identity(구간 정체성) — aligned with F60 probe pattern for comparability.

6. **Tier B / combined plan(티어 B/합산 계획)**
   Either define Tier B(티어 B) + combined(합산) recording for this packet, or mark `missing_required(필수 누락)` / `out_of_scope_by_claim(주장 범위 밖)` **at stage open**, not at closeout.

7. **Success / stop criteria pre-registration(성공/중단 기준 사전 등록)**
   Exploration-only still needs numeric **stop conditions(중단 조건)** (e.g. runtime PF band, trade density floor, proxy–runtime gap ceiling). Snapshot mentions recording gap but not thresholds.

8. **Stage scaffold existence(단계 스캐폴드 존재)**
   Confirm `stage_frontier_61__non_long_axis_pf_source_after_friction_memory` folder, run id `frontier61A_...`, ledger row template, and `runtime_backtest` / `obsidian-runtime-parity` routing in `work_family_registry.yaml`.

---

## Classification summary(분류 요약)

| Item(항목) | Grok classification(그록 분류) |
|---|---|
| F61 **hypothesis direction(가설 방향)** | **Accepted in principle(원칙적 수용)** for exploration-only scout |
| F61 **stage open for implementation(구현용 단계 개방)** | **`needs_local_verification`** until checks 1–8 are done |
| F61 **rejection(거절)** | **Not warranted(부당함)** from snapshot alone — pivot is reasonable |

---

## What would flip the verdict(판정 변경 조건)

- **`accepted`**: Local checks 1–8 pass; failure-mode audit shows label/target change addresses the dominant F53–F60 gap; Tier B/combined and stop criteria are pre-registered.
- **`rejected`**: Audit shows F53–F60 failures were primarily parity/handoff and F61 changes **only** labels with no parity delta; or 3-class labels are degenerate (e.g. >X% flat with no tradable margin band).

**Bottom line(요약):** Open F61 as an **exploration-only runtime probe(탐색 전용 런타임 탐침)** direction, but treat **implementation start(구현 시작)** as blocked until Codex(코덱스) completes the local verification list above. Do not treat this review as permission for completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

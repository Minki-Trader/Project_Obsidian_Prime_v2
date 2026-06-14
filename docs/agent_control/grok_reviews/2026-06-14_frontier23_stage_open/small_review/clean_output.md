Grok 외부 2차 검토 역할로 진행합니다. 협업 스킬과 F22·F23 관련 맥락을 먼저 확인합니다.
## Decision: accept with adjustments

Codex may open Frontier23(전선23) as `stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout`. The pivot fits F22(전선22) closeout(마감): shock-anchored cross-family search did not make seed/handoff(씨앗/인계), and the reopen condition(재개 조건) asks for a new PF source(수익 팩터 원천) first, with F22 low-DD lifecycle(낮은 손실폭 생명주기) only as later risk reference(위험 참고).

Do **not** tighten scout PF thresholds(탐색 수익 팩터 임계값) at open. Your exploration filters are fine. The extra guard belongs in the **stage-open contract(단계 개방 계약)** before F23B proxy scout(프록시 탐색), so F23 does not become F22(전선22) with a new label. F22 already framed “favorable payoff asymmetry(유리한 손익 비대칭)” inside shock+context entry(충격+문맥 진입).

---

### Accepted adjustments (stage-open locks, before proxy scout)

- **Metric definition lock(지표 정의 잠금):** In `00_spec`, write exact train-only(학습 전용) payoff-asymmetry metrics: average win/loss ratio(평균 이익/손실 비), right-tail vs worst-loss containment(우측 꼬리 대 최악 손실 억제), adverse-loss filter(불리 손실 필터). Fix label horizon(라벨 구간) to `fwd12`, and forbid validation/OOS(검증/표본외) in selection stats(선택 통계).
- **Pre-scout sanity gate(탐색 전 건전성 게이트):** Before wide candidate sweep(넓은 후보 탐색), run one bounded train-only check: asymmetry-conditioned entry subsets(비대칭 조건 진입 부분집합) must beat unconditional train baseline(무조건 학습 기준선) on the same fixed proxy(고정 프록시). If not, stop at design — do not repeat F22’s 464-row empty sweep(빈 탐색).
- **Novelty / duplicate guard(신규성·중복 방지):** `novelty_delta` must say selection is **outcome-conditioned on train(학습 결과 분포로 선별)**, then rule/feature discovery(규칙·피처 발견) — not shock-anchored cross-family gates(충격 고정 교차군 게이트). Add explicit `do_not_repeat`: shock+trend primary entry, hold2/ATR lifecycle-first(생명주기 우선), F20 rule-atlas restate(규칙 지도 재진술).
- **Evaluation-surface split(평가면 분리):** Proxy scout surface(프록시 탐색면) and any later F22 lifecycle risk-containment reference(위험 억제 참고) stay separate artifacts(산출물). No lifecycle repair(생명주기 수리) until a seed surface row(씨앗 표면 행) exists on proxy.
- **Seed bar discipline(씨앗 기준 엄격화):** Seed requires **both** validation **and** OOS PF >= 1.20. F22B `f22b_0379` (val PF 1.456, OOS PF 1.169) is near-seed only — not seed, not handoff. Encode this in open contract so val-only wins do not reopen lifecycle tuning.
- **ONNX scope honesty(ONNX 범위 정직성):** Stage title ONNX scout is forward intent(앞으로의 의도) only. Lock: no ONNX/model training until handoff-candidate row(인계 후보 행); otherwise record `onnx_branch_unattempted` like F22.
- **Tier + data boundary(티어·데이터 경계):** Tier A primary with Tier B separate + combined rows, or explicit `tier_b_missing_required`. Carry `timezone_status unresolved` — no verified session-shock runtime semantics(세션·충격 런타임 의미) claim.

---

### Rejected (do not add at open)

- **Reject stricter scout PF floors** — PF >= 1.05 scout / 1.20 seed / 1.50 handoff are adequate exploration filters; tightening them now would block exploration without fixing the F22 failure mode(실패 양식).
- **Reject opening without pre-scout contract** — “payoff asymmetry” alone is too close to F22 narrative; implementation contract must differ before F23B runs.
- **Reject lifecycle-first or shock-inherited entry** — that repeats F22 negative memory(부정 기억), not a new frontier thesis(전선 가설).

---

**Claim boundary (unchanged):** This review authorizes stage-open exploration design only. No completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

**Codex classification:** `accepted_with_adjustments` — local verification(로컬 검증) needed on pre-scout sanity metrics and F20/F22 duplicate-guard wiring before F23B executes.

Grok 외부 2차 의견 역할로, 협업 스킬과 제공된 근거를 먼저 확인한 뒤 집중 질문에 답하겠습니다.

제공된 수치와 수리 축 맥락을 로컬 산출물에서 교차 확인 중입니다.

**Grok external review(그록 외부 검토)** — `medium review(중간 검토)`, conversation-only(대화 전용). Advice classification(조언 분류): `needs_local_verification(로컬 검증 필요)` until Codex confirms artifacts.



---



## 1. Primary recommendation(주 추천)



**C. Run one non-expensive diagnostic only(저비용 진단만 실행)** — **frozen frontier02C anchor decision-layer diagnostic(고정 02C 앵커 결정층 진단)**.



**Exact diagnostic(정확한 진단):**



On the **single frozen best(단일 고정 최고)** from frontier02C — `frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6__p34__m0__cd6` — **no retrain(재학습 없음)**, **no new ONNX(새 온엑스 없음)**:



1. **Validation-only probability calibration(검증 전용 확률 보정)**

   Fit Platt scaling or isotonic regression on validation probabilities only; apply to OOS unchanged.



2. **Monotonic threshold + cooldown grid(단조 임계값 + 쿨다운 격자)**

   Sweep threshold (and optionally cooldown) on the **same** decision replay surface; record PF / daily density / DD / net for validation and OOS.



3. **Joint-pass Pareto(동시 통과 파레토)**

   Count how many configs satisfy the stage joint bands: density 5–10/day, DD &lt;10%, OOS PF improvement vs frontier02C best **without** density falling below 5/day.



4. **Loss attribution slice(손실 기여 분해)**

   On OOS only: bucket losing trades by confidence decile and by **existing** session/regime feature buckets (no new model). Answer: is the PF gap mostly **low-confidence noise(저신뢰 잡음)** (decision-layer fixable) or **core signal miss(핵심 신호 실패)** (not fixable by threshold)?



**Go / no-go rule after diagnostic(진단 후 진행/중단 규칙):**



- **Go → one capped frontier02F repair(상한 1회 02F 수리)** only if a calibrated/threshold config shows **OOS PF ≥ 1.2**, density **5–10/day**, **OOS DD ≤ 10%**, and **OOS net &gt; 0** vs frontier02C anchor.

- **No-go → stage closeout(단계 마감)** per fallback B.



**Effect(효과):** frontier02D가 이미 **label/training repair(라벨/학습 수리)** 축을 부정했으므로, 비싼 2차 수리나 WFO/MT5 전에 **decision-layer(결정층)** 만 남은 저비용 질문을 먼저 닫습니다.



---



## 2. Fallback(대안)



**B. Stop repairing this frontier and prepare stage closeout(수리 중단 후 단계 마감)** as a **split exit(분리 종료)**:



| Closeout type(마감 유형) | What to preserve(보존 내용) |

|---|---|

| **preserved clue(보존 단서)** | frontier02B proxy clue; frontier02C trainable ONNX seed surface (6/6 parity, positive OOS net, density in band); proxy→teacher→ONNX path works |

| **negative memory(부정 기억)** | frontier02D label repair (`ret_m1c`) **strictly worse** than 02C on PF, density, and OOS net; four-axis joint target (PF 2–3+, DD &lt;10%, smooth curve) **not approached** on Tier A cheap path |



**Trigger fallback immediately(즉시 대안 적용)** if the diagnostic finds **zero** configs meeting the go rule above, or if loss attribution shows core signal failure dominates (not threshold-fixable).



**Effect(효과):** capped repair rule(상한 수리 규칙)과 맞습니다 — PF 축에서 label repair가 실패했고, decision-layer도 답이 없으면 **같은 축 무정보 반복(무정보 반복)** 을 막습니다.



---



## 3. Why not WFO/MT5 yet(왜 아직 WFO/MT5가 아닌지)



1. **No completion candidate(완성 후보 없음)** per stage exit rule: best OOS PF ≈ **1.05** (frontier02C), target **2–3+**; OOS DD **10.34%** (borderline fail); frontier02D best OOS **net negative**.

2. **Repair trajectory worsened(수리 궤적 악화)**: 02B → 02C (seed exists) → 02D (label repair) = **regression(후퇴)**, not convergence.

3. **Expensive path tests the wrong question(비싼 경로가 잘못된 질문을 검증)**: WFO/MT5 would stress **runtime packaging(런타임 패키징)** and **cost/slippage(비용/슬리피지)** on a surface that has not passed **cheap joint objective(저비용 동시 목적)** on Python proxy replay.

4. **Tier B separate still `missing_required(필수 누락)`** — routed expensive validation would over-read Tier A-only evidence.

5. **Stage brief capped repair rule(단계 상한 수리 규칙)**: one failed PF-axis label repair already recorded; expensive validation before decision-layer diagnostic would skip the mandated cheap de-risk step.



---



## 4. Claim boundary(주장 경계)



**Allowed from this review(이 검토에서 허용):**



- frontier02C = **seed observation only(씨앗 관찰만)**, strongest cheap anchor

- frontier02D = **negative repair memory(부정 수리 기억)**

- Diagnostic C = **exploration planning(탐색 계획)**, not evidence production yet

- Closeout B = **hypothesis lifecycle judgment(가설 생명주기 판정)** for *this* frontier, not idea death globally



**Forbidden(금지):**



- completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)

- “ONNX frontier validated(온엑스 전선 검증됨)” or “ready for WFO/MT5(워크포워드/MT5 준비됨)”

- Treating frontier02B/C/D best rows as **selected candidate(선택 후보)**



**Not recommending as primary(주 추천 아님):**



- **A without diagnostic first(진단 없는 A)** — especially another **logistic label / retrain repair(로지스틱 라벨·재학습 수리)**; frontier02D already falsified that axis on the current seed surface.



---



## 5. Specific local verification Codex must do before acting(행동 전 로컬 검증)



Codex must verify locally **before** opening frontier02E/F or closeout:



1. **KPI number parity(지표 숫자 일치)** — Re-read and hash-check:

   - `stages/.../03_reviews/frontier02C_trainable_onnx_seed_surface_design_v1_report.md`

   - `stages/.../03_reviews/frontier02D_review_and_repair_onnx_seed_surface_v1_report.md`

   - Confirm OOS net: 02C **+0.0464936** vs 02D **−0.00281852**.



2. **Monotonic degradation check(단조 악화 확인)** — From `repair_decision_surface_metrics.csv` (02D) vs `decision_surface_metrics.csv` (02C): confirm **all 14** repair rows are ≤ 02C best on validation PF and density, not only the top row.



3. **Repair axis identity(수리 축 정체성)** — Read `repair_seed_surface_spec.json`: confirm 02D changed **label_id `ret_m1c`**, not calibration-only. Effect: proves diagnostic C is a **new-information axis(새 정보 축)**, not repeat of 02D.



4. **Replay infrastructure exists(리플레이 인프라 존재)** — Confirm `top_decision_signal_replay.csv` (02C) and `top_repair_signal_replay.csv` (02D) are present and row counts match reports (576 decision rows). Diagnostic must reuse 02C replay, not rebuild pipeline.



5. **Capped repair counter(상한 수리 카운터)** — Read `00_spec/stage_brief.md` capped repair rule and `04_selected/selection_status.md`: document that **one PF-axis label repair(02D)** is on record; next action is either **decision-layer diagnostic** or **closeout**, not open-ended repair chain.



6. **Tier gate honesty(티어 게이트 정직성)** — Reconfirm Tier B `missing_required` and Tier A+B `out_of_scope_by_claim` in closeout docs; do not imply full-context alpha read.



7. **ONNX parity scope(온엑스 동등성 범위)** — `onnx_parity_audit.json` (02C 6/6, 02D 2/2) covers **export parity(보내기 동등성)** only, not MT5 runtime. No runtime authority claim from parity pass.



---



**Summary for Codex(코덱스 요약):** Primary **C** (frozen 02C calibration/threshold + loss-attribution diagnostic) → conditional single capped repair only if go rule hits; else fallback **B** (preserved clue + negative memory closeout). **Do not** open WFO/MT5 on current evidence.

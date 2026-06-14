Grok 외부 2차 의견으로 Frontier17 개방안을 검토합니다. 협업 스킬과 F15–F16 맥락을 먼저 확인합니다.
## Classification(분류)

**`accepted`(수용)**

---

## Grok Review(그록 검토) — Frontier17 Stage Open(전선17 단계 개방)

### Q1. Novelty delta(신규성 차이) vs F15–F16(전선15~16)

**Verdict(판정): sufficient(충분), not threshold repair in disguise(임계값 수리로 위장한 것 아님) — with one implementation trap(구현 함정 1개).**

F15(전선15)는 **density-first(빈도 우선)** `train-only score threshold(학습 전용 점수 임계값)`로 빈도는 맞췄지만 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 같이 못 올렸습니다. F16(전선16)은 **future-path edge label(미래 경로 엣지 라벨)** + `edge_margin/risk-quality veto(엣지 마진/위험 품질 배제)`로 같은 한계에 걸렸습니다.

Frontier17(전선17)은 검증 철학(validation philosophy, 검증 철학)과 결정 구조(decision structure, 결정 구조)가 다릅니다.

| Axis(축) | F15–F16 | F17 proposal(제안) |
|---|---|---|
| Order(순서) | density → edge | drawdown hazard → continuation |
| Label(라벨) | future edge / risk-quality | train adverse cluster + realized continuation |
| Gate(게이트) | single threshold/rank | **AND**: firewall veto + continuation trigger |

이건 “같은 임계값을 다른 이름으로 다시 조정”이 아니라 **진입 조건을 두 단계로 쪼갠 가설 전환(hypothesis pivot, 가설 전환)**입니다.

**Trap(함정):** `adverse cluster(불리 군집)`와 `continuation quality(지속 품질)`가 F16 `risk-quality label(위험 품질 라벨)`의 rename(이름만 바꾼 것)이면 신규성이 무너집니다. Codex(코덱스)는 Frontier17A `00_spec`에 **정의 고정(definition lock, 정의 고정)**을 넣어야 합니다.

**Archive overlap(보관소 겹침):** Stage299 `loss_cluster_veto(손실 군집 배제)` 부정 기억(negative memory, 부정 기억)이 있습니다. 이건 거절 사유가 아니라 **reference disclosure(참조 공개)** 의무입니다. F17은 **entry-state firewall + continuation AND-gate(진입 상태 방화벽 + 지속 AND 게이트)**로 구조가 다릅니다.

---

### Q2. Three pre-registered profiles(사전 등록 프로필 3개) — repair ladder(수리 사다리) 위험?

**Verdict(판정): safe as bounded exploration(제한 탐색으로 안전) — only if guards are enforced(가드가 강제될 때만).**

`h8/q70/q60 → h10/q75/q65 → h12/q80/q70`는 **strictness ladder(엄격도 사다리)** 형태입니다. F16(전선16) 3 label variants(라벨 변형 3개)와 같은 패턴이라, **탐색 범위(bounded sweep, 제한 훑기)**로는 허용되지만 **post-hoc tuning(사후 조정)**으로 쓰이면 수리 사다리가 됩니다.

안전 조건(conditions for safety, 안전 조건):

- exactly 3 profiles(정확히 3개), no 4th knob(4번째 조정 없음)
- no validation/OOS q retuning(검증/표본밖 q 재조정 없음) — 이미 통제에 있음
- closeout by **structure verdict(구조 판정)** (transfer / density floor / PF-DD), not “pick best q”(최적 q 고르기 아님)
- per-profile **density + veto-rate audit(빈도 + 배제율 감사)** so “improvement” isn’t just trade starvation(거래 기아)

3개 프로필은 **repair ladder(수리 사다리)가 아니라 diagnostic triplet(진단 삼중)**으로 쓰면 됩니다.

---

### Q3. Minimum guards(최소 가드) before Frontier17A/B materialization(물질화)

Codex(코덱스)가 `materialize_frontier17a_stage_open.py` / `00_spec`에 아래를 **고정(lock, 고정)**해야 합니다. F16 guard manifest(가드 목록) 패턴을 그대로 이어받되, F17 전용 항목을 추가합니다.

**A. Definition locks(정의 고정)**

1. `adverse_cluster_state_contract` — train-only feature set(학습 전용 피처 집합), horizon(예측수평선), cluster score(군집 점수); **must not reuse F16 edge_margin label columns(F16 엣지 마진 라벨 열 재사용 금지)**
2. `continuation_quality_contract` — **realized path metric(실현 경로 지표)** only; no future-edge label(미래 엣지 라벨 금지)
3. `decision_and_gate_contract` — entry = `NOT adverse_veto AND continuation_trigger`; no score-rank density calibration(점수 순위 빈도 보정 금지)

**B. Do-not-repeat(반복 금지)**

4. `no_f15_9cell_grid`
5. `no_f16_locked_edge_margin_target8`
6. `no_validation_oos_threshold_calibration`
7. `stage299_loss_cluster_veto_overlap_disclosed` — cp299B/F reference only(참조만), not inherited winner(승자 상속 아님)

**C. Exploration bounds(탐색 경계)**

8. `variant_cap_exactly_3` — pre-registered IDs frozen(사전 등록 ID 고정)
9. `no_repair_ladder` — no post-hoc profile/q addition(사후 프로필/q 추가 금지)
10. `density_floor_audit` — fail if any profile &lt; 3/day(일 3회 미만이면 실패)
11. `firewall_transfer_audit` — train q frozen; report val/OOS veto rate + continuation pass rate(배제율·통과율 보고)

**D. Evidence parity(근거 동등성)**

12. `tier_paired_records` — Tier A sep / Tier B sep / combined(티어 A 분리 / 티어 B 분리 / 합산)
13. `onnx_parity_gate` — no strict/preserved without parity(동등성 없이 엄격/보존 판정 금지)
14. `f16_reference_benchmark` — explicit DD/smoothness/density compare vs F16B/D(F16B/D 대비 명시 비교)

**E. Closeout(마감)**

15. `mt5_runtime_probe_before_closeout` — best-or-seed probe or exact blocked reason(최선·씨앗 탐침 또는 정확한 차단 사유)
16. `claim_boundary_lock` — scout / seed surface / runtime probe observation only(탐색·씨앗·런타임 관찰만)

---

## Advice classification detail(조언 분류 상세)

| Item(항목) | Grok stance(그록 입장) |
|---|---|
| Open Frontier17(전선17 개방) | **accepted(수용)** |
| Hypothesis pivot(가설 전환) | **accepted(수용)** |
| 3 profiles(프로필 3개) | **accepted with guard enforcement(가드 강제 조건부 수용)** |
| Materialize 17A/B now(지금 17A/B 물질화) | **needs_local_verification(로컬 검증 필요)** until guards 1–16 are in spec(가드 1–16이 스펙에 들어갈 때까지) |

Overall packet classification(전체 묶음 분류): **`accepted`(수용)** — stage open direction(단계 개방 방향) is sound(타당); materialization(물질화) waits on guard manifest + definition contracts(가드 목록·정의 계약).

---

## Forbidden claim check(금지 주장 확인)

Proposal claim boundary(제안 주장 경계) is correct(올바름): scout clue / seed surface / runtime probe observation only(탐색 단서·씨앗 표면·런타임 탐침 관찰만). No operating promotion(운영 승격), runtime authority(런타임 권위), baseline(기준선), or Goal Achieve(목표 달성) — **no Grok override(그록 덮어쓰기 없음)**.

---

## Codex next step(코덱스 다음 단계)

Proceed(진행): `frontier17A_stage_open_new_hypothesis_design_v1` with guard manifest mirroring F16A pattern(F16A 패턴 가드 목록 복제) plus items 1–16 above(위 1–16 항목 추가). Grok does not need a second pass(2차 검토 불필요) if those guards appear in `00_spec` and `materialize_frontier17a_stage_open.py` before Frontier17B scout(17B 탐색 전).

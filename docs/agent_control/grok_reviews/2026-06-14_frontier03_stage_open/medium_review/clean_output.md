Grok 역할로 단계 개방 제안을 검토합니다. 먼저 관련 스킬과 제한된 근거 자료를 확인합니다.
## 1. Stage-open recommendation(단계 개방 권고)

**Yes — open Frontier03 now(지금 전선03 개방 권고).**

Frontier02(전선02)는 `frontier_governance.md`의 closeout contract(마감 계약)를 충족했습니다: preserved clue(보존 단서, 02C 밀도 `5.03/day` + 약한 양수 PF), negative memory(부정 기억, 02E `go_rule_rows=0`), exit rule(종료 규칙) 발동. 같은 표면 계열에서 threshold/calibration repair(임계값/보정 수리)를 더 밀 근거가 없습니다.

`stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling`은 **별도 hypothesis lifecycle(별도 가설 생명주기)**로 타당합니다. 이유는 novelty delta(신규성 차이)가 **label construction(라벨 구성)** 축으로 명시되고, Frontier02의 joint four-axis objective(네 축 동시 목적)를 유지하면서 **source of truth(진실 원천)를 바꾸는** 첫 단계이기 때문입니다.

**조건(conditions):** Frontier03A(전선03A)는 **stage-open design only(단계 개방 설계 전용)**로 열고, 실행은 `frontier03B_regime_asymmetric_label_proxy_scout_v1`로 분리하세요. ONNX(온엑스)는 stage name(단계 이름)에 두되, **첫 실행은 label proxy replay(라벨 프록시 재생)까지만** — teacher/ONNX/decision replay(교사/온엑스/결정 재생)는 proxy survivor(프록시 생존자) 이후입니다.

---

## 2. Thesis critique(가설 비판)

**방향은 맞지만, 지금 제안은 아직 넓습니다.**

| Risk(위험) | Why it matters(이유) | Narrowing move(좁히기) |
|---|---|---|
| Broad source/label redesign(넓은 원천/라벨 재설계) | Stage41 `directional_asymmetric`(방향 비대칭), Stage347 `cash_open asymmetric source`(현금장 비대칭 원천)가 archive(보관소)에 이미 있음 | **기존 `label_v1_fwd12` + `feature_set_v2` 고정**, regime(레짐)은 **기존 closed-bar feature(확정봉 피처)에서만** 정의 |
| “Asymmetric ONNX” sounds like model-first(모델 우선으로 읽힘) | Frontier02 실패는 **label + decision surface(라벨+결정 표면)** 쪽 | 첫 가설 문장을 **“regime-conditioned asymmetric labels improve four-axis proxy replay”**로 쓰고, ONNX는 downstream(하류)로 미룸 |
| Regime × side × horizon combinatorics(레짐×방향×보유기간 조합 폭발) | exploration mandate(탐색 규율) 위반 소지 | **한 regime definition(레짐 정의 1개)** + **long/short asymmetric targets(롱/숏 비대칭 목표)** + **horizon은 fwd12 고정, neutral band만 regime-conditioned(중립 구간만 레짐 조건)** |
| 02D already tried label repair(02D가 이미 라벨 수리 시도) | `ret_m1c` 등 단순 label swap(라벨 교체)은 negative(부정) | novelty_delta(신규성 차이)에 **“not another ret_m* single-label repair(또 다른 ret_m* 단일 라벨 수리 아님)”**를 명시 |

**Thesis verdict(가설 판정):** 개방은 수용하되, subtitle(부제) 수준의 가설을 **“regime-conditioned asymmetric label construction under fixed features/split, scored by four-axis proxy replay”**로 한 줄 더 좁혀야 broad redesign(넓은 재설계)로 새지 않습니다.

**Positive delta vs Frontier02(전선02 대비 긍정 차이):** 02는 training/selection-time joint gate(학습/선택 시점 동시 게이트)였고, 03은 **payoff target construction(손익 목표 구성)**을 바꿉니다. 이건 `frontier_governance.md` repair-to-new-frontier(수리→새 전선) 조건에 맞습니다.

---

## 3. First proxy scout recommendation(첫 프록시 탐색 권고)

**Strongest narrow first scout(가장 좁고 강한 첫 탐색):**

**`frontier03B_regime_asymmetric_label_proxy_scout_v1` — “Regime-neutral-band asymmetric long/short label replay”**

고정 변수(fixed):
- Dataset(데이터셋): `label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58` (02와 동일 identity)
- Split(분할): train/validation/OOS(학습/검증/표본외) 기존 계약
- Cost/filter proxy(비용/필터 프록시): Frontier02 scout cost(02 탐색 비용) + `mid_cash` / `both` 참조 필터 (baseline(기준선) 아님, replay control(재생 대조))
- Horizon(보유기간): **fwd12 only(12봉만)** — horizon sweep(보유기간 전수조사) 금지

변경 변수(changed) — **12-variant cap(12변형 상한)**:

1. **Regime(레짐) — 1 definition only:**
   - Binary `trend_vs_chop(추세 vs 횡보)` from existing features only (e.g. ATR-ratio / range-efficiency style(변동성비/구간효율류), **no future return in regime assignment(레짐 배정에 미래 수익 금지)**)

2. **Asymmetric payoff targets(비대칭 손익 목표):**
   - Long label(롱 라벨): train-split upside quantile capture(학습분할 상승 분위 포착), e.g. q70 long-only
   - Short label(숏 라벨): **separate** train-split downside quantile(별도 하락 분위), e.g. q30 short-only — **not symmetric mirror(대칭 거울 아님)**

3. **Regime-conditioned neutral band(레짐 조건 중립 구간) — only moving part:**
   - Trend regime(추세 레짐): tighter neutral(좁은 중립) → more directional labels
   - Chop regime(횡보 레짐): wider neutral(넓은 중립) → fewer false direction labels
   - Grid(격자): 2 neutral widths × 3 side-combination modes = **6 label families(6 라벨군)**
     - `long_only`, `short_only`, `joint_both_asymmetric(비대칭 동시)` × 2 regime bands

4. **Scoring(점수) — same four-axis distance as F02(02와 동일 네 축 거리):**
   - PF, density, DD, smoothness on **label-proxy trade replay(라벨 프록시 거래 재생)** (no ONNX yet)
   - Reference comparison(참조 비교): no-trade + Frontier02C preserved numbers(02C 보존 수치, **not baseline**)

**Go / no-go for micro-search(미세 탐색 진입 조건):**
- At least **1 label family(라벨군 1개)** with validation **and** OOS positive net(양수 순수익) **and** better four-axis target-distance vs 02C reference on **≥2 of 4 axes(4축 중 2축 이상)** (density alone(밀도만) 불충분)

**Explicitly defer(명시적 연기):** model training, ONNX export, decision-layer calibration, WFO, MT5.

---

## 4. Do-not-repeat constraints(반복 금지 제약)

**From Frontier02(전선02):**
- Do not inherit 02C as baseline/winner/promotion candidate(02C를 기준선/승자/승격 후보로 상속 금지)
- Do not repeat same-family threshold/calibration repair on frozen 02C/02E surfaces(고정 02C/02E 표면 임계값/보정 수리 반복 금지)
- Do not run another decision-layer go-rule hunt without new label/regime axis(새 라벨/레짐 축 없이 결정층 go-rule 재탐색 금지)
- Do not single-axis repair (PF-only or density-only)(단일 축 수리 금지)
- Do not treat Tier A as full alpha read; Tier B stays `missing_required`(티어 B는 필수 누락 유지)

**From Frontier02D/E(전선02D/E):**
- Do not repeat `ret_m1c`-style single-label swap as “novelty”(`ret_m1c`류 단일 라벨 교체를 신규성으로 반복 금지)
- Do not re-freeze 02C anchor for uplift comparison only(02C 앵커만 고정 비교 반복 금지)

**From prior archive(이전 보관소) — reference, not inheritance(참조만, 상속 아님):**
- Stage41 `directional_asymmetric_return_target_rebuild`: reuse `foundation/labels/directional_asymmetric` code if fit(코드 재사용 가능), but **do not replay broad MT5 probe grid(넓은 MT5 탐색 격자 재실행 금지)**
- Stage347 `cash_open_asymmetric_source`: do not reopen cash-open source/head redesign as Frontier03 scope(현금장 원천/헤드 재설계를 03 범위로 열지 말 것)
- Stage364 evaluation-time joint gate(평가 시점 동시 게이트): do not confuse with label-construction frontier(라벨 구성 전선과 혼동 금지)

**Process(절차):**
- No WFO/MT5 in stage-open or first proxy packet(개방/첫 프록시에 WFO/MT5 금지)
- No completion/baseline/promotion/runtime/live/Goal Achieve language(완성/기준선/승격/런타임/실거래/목표 달성 표현 금지)

---

## 5. Local verification before packet(묶음 전 로컬 검증)

Codex should verify locally **before** writing/materializing the stage-open packet(단계 개방 묶음 작성 전):

| Check(점검) | What to verify(검증 내용) | Why(이유) |
|---|---|---|
| Parent closeout identity(부모 마감 정체성) | `frontier02F` report exists; parent_run_id linkage; 02C OOS `1.05433 / 5.03053 / 10.3356%`; 02E go-rule `0` | Closeout chain integrity(마감 사슬 무결성) |
| Data identity(데이터 정체성) | `model_input_dataset.parquet` exists; sha256; `feature_order.txt` hash; manifest/summary paths | Proxy scout reproducibility(프록시 탐색 재현성) |
| Regime leakage preflight(레짐 누수 사전점검) | Regime features are closed-bar only; no OOS/validation fitting of regime thresholds(레짐 임계값 검증/표본외 적합 금지) | Label-regime leakage is top invalid risk(라벨-레짐 누수가 1순위 무효 위험) |
| Archive cross-reference(보관소 교차참조) | Stage41 + Stage347 cited in `prior_stage_scan.md` as **reference artifacts**, not winners | Prevents false novelty(허위 신규성 방지) |
| Reusable code path(재사용 코드 경로) | Confirm `foundation/labels/directional_asymmetric` suitability vs new stage-local shim(적합성 vs 단계 로컬 셈) | Architecture guard(구조 보호) |
| Tier honesty(티어 정직성) | Tier A only; Tier B `missing_required`; Tier A+B `out_of_scope_by_claim` | Paired-tier rule(티어 쌍 규칙) |
| State sync(상태 동기화) | `workspace_state.yaml`, `current_working_state.md`, Frontier02 `selection_status.md` next pointer | Re-entry truth(재진입 진실) |
| Grok receipt(그록 영수증) | Prompt hash + this review captured under `grok_reviews/2026-06-14_frontier03_stage_open/` | Required gate(필수 게이트) |

**Not required before open packet(개방 묶음 전 불필요):** MT5 compile, ONNX parity, model training, Tier B materialization.

---

## 6. Claim boundary(주장 경계)

**Allowed after Frontier03A open(03A 개방 후 허용 주장):**
- Stage opened as independent frontier campaign(독립 전선 캠페인으로 개방)
- Grok stage-open review captured(그록 단계 개방 검토 기록)
- Proxy label design ready for Frontier03B(03B용 프록시 라벨 설계 준비)
- Frontier02C density clue cited as **target-distance reference only(목표 거리 참조 전용)**
- Exploratory hypothesis: regime-asymmetric labels may shrink four-axis distance(탐색 가설: 레짐 비대칭 라벨이 네 축 거리를 줄일 수 있음)

**Forbidden(금지):**
- completion, selected baseline, promotion candidate, operating promotion
- runtime authority, live readiness, Goal Achieve
- “02C improved” or “02C successor” framing(02C 개선/후속 프레이밍)
- Tier A+B combined alpha read(티어 A+B 합산 알파 판독)
- Any positive trading judgment from design docs alone(설계 문서만으로 긍정 거래 판정)

**Exit preview for Frontier03(03 종료 미리보기):** close as preserved clue, negative memory, or blocked — **not** as winner unless a later packet with evidence explicitly earns it(승자는 나중 근거 묶음에서만).

---

### Codex classification hint(코덱스 분류 힌트)

| Advice(조언) | Classification(분류) |
|---|---|
| Open Frontier03 now, separate lifecycle | **accepted(수용)** |
| Narrow thesis to label-construction under fixed features | **accepted(수용)** |
| First scout = 12-cap regime-neutral-band asymmetric replay, no ONNX | **accepted(수용)** |
| 02C/baseline/promotion inheritance | **rejected(거절)** |
| Threshold-only next step | **rejected(거절)** |
| Dataset hash, regime leakage audit, archive cross-ref | **needs_local_verification(로컬 검증 필요)** |

**Bottom line(한 줄 결론):** Codex should open Frontier03 **now**, but the narrowest honest first move is **label-proxy replay with one regime definition and asymmetric long/short targets** — not another ONNX surface repair and not a broad archive relabel campaign(넓은 보관소 재라벨링 캠페인 아님).

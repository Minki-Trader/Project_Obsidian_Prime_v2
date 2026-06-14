Frontier16D 런타임 탐침 보강이 적절한지 판단하려면, 먼저 현재 진실·스테이지 상태·기존 MT5 탐침 인프라를 로컬에서 확인하겠습니다.
## Verdict(판정)

**Frontier16D runtime probe supplement(런타임 탐침 보강) is appropriate(적절).**
**Do not skip MT5(메타트레이더5) because the proxy failed(프록시 실패).** Proxy failure is exactly when a narrow `runtime_probe_observation(런타임 탐침 관찰)` is useful: it records how Python proxy(파이썬 프록시) and Strategy Tester(전략 테스터) diverge, without reopening the stage thesis(단계 가설).

Effect(효과): F16(프론티어16) closeout judgment(마감 판정) stays `negative_memory_no_forward_clue(부정 기억, 전진 단서 없음)`. MT5 only adds a runtime-side note(런타임 쪽 메모), not a preserved clue(보존 단서) or promotion(승격).

---

## Why not skip(왜 건너뛰면 안 되나)

| Factor(요인) | Reading(해석) |
|---|---|
| User clarified rule(사용자 명시 규칙) | Each frontier stage(각 프론티어 단계) should include ≥1 MT5 runtime probe(런타임 탐침) |
| F16 closeout record(마감 기록) | `mt5_out_of_scope_by_claim(주장 범위 밖, MT5 없음)` — supplement fixes a **recording gap(기록 공백)**, not a failed hypothesis rescue(가설 구제) |
| Prior frontier pattern(F09–F16) | All closed proxy-only(프록시만). Your rule is a **forward policy change(앞으로의 정책 변경)**; F16 is the right place to start closing that gap |
| Proxy OOS PF < 1(표본밖 수익 팩터 1 미만) | Weakens **promotion(승격)** case; does **not** weaken **probe obligation(탐침 의무)** |
| External verification anti-deferral(외부 검증 지연 방지) | Same pass should attempt narrow MT5 or record exact `blocked(차단)` |

Proxy failure means “do not promote.” It does **not** mean “do not observe runtime.”

---

## Lane and claim boundary(레인과 주장 경계)

- **Primary lane(주 레인):** `runtime(런타임)`
- **Secondary lane(보조 레인):** `evidence(근거)`
- **Discipline(규율):** `handoff_discipline(인계 규율)` — package, probe, record; no EA logic change unless handoff cannot run
- **Allowed judgment(허용 판정):** `runtime_probe_observation(런타임 탐침 관찰)` or `blocked(차단)`
- **Forbidden(금지):** completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), preserved clue(보존 단서)

F16C(프론티어16C) says **no repair ladder(수리 사다리 금지)**. Frontier16D must be labeled **`runtime_probe_supplement(런타임 탐침 보강)`**, not `repair_or_closeout_reopen(수리 또는 마감 재개)`.

Effect(효과): closeout(마감) stays closed; only the stage ledger(단계 장부) gains one runtime row(런타임 행).

---

## Main risks(주요 위험)

### 1. Handoff gap — models missing on disk(인계 공백 — 모델 파일 없음) — **highest**

Local check: best-candidate ONNX(최고 후보 온엑스) path from `run_manifest.json` → **`Test-Path = False`**. `models/` directory also missing.

Manifest still records identity(정체성):
- ONNX sha256: `5e0e84e028100575cd1806b77a9915fce22023da5ecef4ebfcf19cda2f8b1907`
- threshold(임계값): `0.05512609121593004`
- feature_order_hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

Risk(위험): probe may become `blocked_missing_onnx_or_feature_matrix(차단, 온엑스/피처 행렬 누락)` before tester runs.

### 2. Decision-contract parity(결정 계약 동등성)

Python proxy(파이썬 프록시) uses:
- score(점수) = `max(p_short, p_long) - p_flat` (`edge_margin`)
- entry when score ≥ `0.0551260912`
- tie-break(동점 처리): **short wins** (`p_short >= p_long`)

EA `threshold_margin` mode maps via `InpShortThreshold=0`, `InpLongThreshold=0`, `InpMinMargin=<threshold>` (same pattern as `stage330/raw_forward_mt5_runtime_probe_or_block.py`). But EA tie-break on equal probs favors **long**.

Risk(위험): small trade-count / density drift(빈도 차이) at margin boundary(마진 경계).

### 3. Proxy ≠ MT5 semantics(프록시 ≠ MT5 의미)

Proxy simulates on fixed splits(고정 분할) with oracle path labels(오라클 경로 라벨) for training only. MT5 adds spread(스프레드), commission(수수료), slippage(슬리피지), hold/exit rules(보유/청산 규칙), and bar-close execution(봉 종가 실행).

With OOS PF `0.94222`, MT5 PF likely ≤ proxy. That supports **negative memory(부정 기억)**; it does not invalidate the probe.

### 4. Repair-ladder misread(수리 사다리 오해)

F16C `do_not_repeat(반복 금지)` blocks relabeling / new score cells / validation-OOS threshold calibration(검증·표본밖 임계값 보정). A single best-failed-candidate probe(단일 최고 실패 후보 탐침) is **not** that ladder if scope stays narrow.

### 5. Workspace sequencing(작업공간 순서)

`workspace_state.yaml` next run(다음 실행) is `frontier17A`. Frontier16D should **append(추가)** to F16 ledgers without changing `current_stage_id(현재 단계 ID)` or reopening F16 judgment unless MT5 exposes only a **runtime-specific blocker(런타임 전용 차단 사유)** (e.g. broken packaging(깨진 패키징), not alpha(알파)).

### 6. Tier B absent(티어 B 없음)

Tier B is `missing_required(필수 누락)` in F16B. Tier-A-only probe(티어 A 단독 탐침) is correct; do not infer combined-tier alpha(합산 티어 알파).

---

## Must-have local verification before execute(실행 전 필수 로컬 검증)

Do these **in order** before Strategy Tester(전략 테스터):

1. **Re-materialize best candidate only(최고 후보만 재물질화)**
   Re-run or export from `frontier16b_edge_quality_risk_veto_proxy_scout.py` for
   `f16b_edge_h8_t0p30_cap0p45_early0p25__rf_bal__edge_margin__target8`.
   Confirm ONNX sha256 matches manifest.

2. **ONNX parity re-check(온엑스 동등성 재확인)**
   Parity passed in F16B; re-verify after re-export before MT5 handoff(인계).

3. **Feature matrix identity(피처 행렬 정체성)**
   Materialize Tier A 58-feature CSV(티어 A 58피처 CSV); confirm `feature_order_hash = fa06973c...` matches `ObsidianPrimeV2_RuntimeProbeEA` default.

4. **Decision `.set` mapping(결정 설정 매핑)**
   - `InpDecisionMode = threshold_margin`
   - `InpShortThreshold = 0`, `InpLongThreshold = 0`
   - `InpMinMargin = 0.05512609121593004`
   - `InpInvertSignal = false`
   - Tier B fallback off(티어 B 대체 끔)
   Document tie-break delta(동점 처리 차이) in probe notes.

5. **Packaging identity bundle(패키징 정체성 묶음)**
   Record hashes for: ONNX, feature matrix, `.set`, `.ini`, `run_manifest.json`, `threshold_manifest.csv`, EA `.ex5` compile identity(컴파일 정체성) if compile runs.

6. **MT5 environment preflight(MT5 환경 사전점검)**
   Terminal path(터미널 경로), MetaEditor compile(메타에디터 컴파일), Common Files copy(공통 파일 복사), tester profile(테스터 프로필). If any fail → `blocked(차단)` with exact command/log, not silent skip.

7. **Narrow tester window(좁은 테스터 구간)**
   Fixed US100 M5(고정 US100 5분봉), train-only threshold(학습 전용 임계값), Tier A only. Prefer validation+OOS window aligned to proxy splits(프록시 분할과 맞춘 검증+표본밖 구간) — not full-sample promotion framing(전체 표본 승격 프레이밍).

8. **Ledger update without judgment upgrade(판정 상향 없이 장부 갱신)**
   Add `frontier16D_*` row to stage_run_ledger + run_registry as `runtime_probe_observation` or `blocked`. Do **not** change F16C closeout label unless new evidence is strictly runtime-handoff-specific(엄밀히 런타임 인계 전용).

---

## What MT5 can and cannot change( MT5가 바꿀 수 있는 것 / 없는 것)

| If MT5 shows…(MT5가 보여주면…) | Allowed update(허용 갱신) |
|---|---|
| Negative PF + density/DD roughly near proxy(수익 팩터·빈도·손실폭이 프록시 근처) | Confirms proxy-negative memory(프록시 부정 기억 확인); no clue |
| Large proxy–MT5 gap(큰 프록시–MT5 격차) | Add **runtime-specific negative memory(런타임 전용 부정 기억)** or `blocked_handoff_parity(인계 동등성 차단)` |
| Positive MT5 on failed proxy(실패 프록시에서 MT5 양수) | **Inconclusive(불충분)** at most — not preserved clue without split stability + parity closure(분할 안정성 + 동등성 마감 없이는 보존 단서 아님) |

---

## Recommendation(권고)

**Proceed with Frontier16D as a bounded supplement(제한된 보강으로 진행).**
First step is not tester launch — it is **handoff preflight(인계 사전점검)**, because ONNX/models are currently absent locally despite manifest hashes.

If handoff cannot be rebuilt without retraining scope beyond best candidate → record `blocked_missing_materialized_handoff(차단, 물질화된 인계 누락)` and still satisfy your “≥1 MT5 attempt or exact blocker( MT5 1회 시도 또는 정확한 차단 기록)” rule.

Then open Frontier17A(프론티어17A) without treating F16 as incomplete(미완료로 보지 않음): supplement completes **external verification discipline(외부 검증 규율)**, not the alpha thesis(알파 가설).

Want me to execute Frontier16D handoff preflight and materialization next?

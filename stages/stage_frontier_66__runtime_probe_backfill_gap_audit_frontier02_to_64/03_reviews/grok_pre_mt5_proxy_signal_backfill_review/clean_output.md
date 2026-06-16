# F66 Pre-MT5 Proxy Signal Backfill Review (F66 MT5 전 프록시 신호 소급 검토)

## 1. Verdict (판정): **needs_local_verification (로컬 검증 필요)**

**Directionally acceptable (방향상 수용 가능)** as a **runtime probe backfill (런타임 탐침 소급)** method with **observation-only claim boundary (관찰 한정 주장 경계)**.

Codex has framed this correctly: heterogeneous proxy sources (이질적 프록시 원천) are normalized to **-1/0/+1** and handed to **RuntimeProbeEA** via a **single-feature EBM table (단일 피처 EBM 테이블)**; **F26/F34** are **stage logic zero (단계 로직상 신호 0)**, not missing material (재료 없음); known **representation gaps (표현 간극)** are named; success criteria exclude **promotion (승격)**, **runtime authority (런타임 권위)**, and **Goal Achieve (목표 달성)**.

I cannot mark **accepted (수용)** without local proof that materialization (물질화) actually matches intent per stage kind (단계 종류별). The plan is sound in principle; execution fidelity (실행 충실도) is the open variable.

---

## 2. Main risks (주요 위험)

1. **False parity read (거짓 동등 판독)** — MT5 KPI (PF, DD, trade count) may be compared to original Python proxy KPI even though exits, SL/TP, and costs differ. Effect: a **probe (탐침)** gets read as **validation (검증)** or **idea verdict (아이디어 판정)**.

2. **Exit/risk representation drift (청산/위험 표현 편차)** — OHLC-path exits (OHLC 경로 청산), log-return caps (로그수익률 한도), and **F18 entry-only replay (F18 진입만 재생)** will inflate **gap attribution: exit/risk (간극 귀속: 청산/위험)**. Effect: weak MT5 numbers may reflect **handoff approximation (인계 근사)**, not stage failure.

3. **Source-kind heterogeneity (원천 종류 이질성)** — eight replay kinds (8종 재생) under one EBM handoff (하나의 EBM 인계) may hide per-kind bugs. Effect: one bad kind (예: rule table vs score surface) poisons batch conclusions.

4. **Signal-count mismatch (신호 수 불일치)** — thresholding, argmax ties (최대확률 동점), IS/OOS window cuts (검증/표본외 구간 절단), or timezone alignment can shift **expected vs MT5 signal count (예상 vs MT5 신호 수)**. Effect: orders/fills look broken when the bug is upstream in materialization.

5. **EBM single-feature collapse (EBM 단일 피처 축소)** — multi-condition proxy decisions (다조건 프록시 결정) compressed to one feature may change decision timing. Effect: probe observes **EA path (EA 경로)**, not the original decision surface (원래 결정 표면).

6. **Zero-signal boundary bleed (신호 0 경계 누수)** — **F26/F34** must stay out of the 64-run queue (64회 실행 대기열). Effect: MT5 runs on intentional zeros look like failed backfill (소급 실패).

---

## 3. Smallest local checks before MT5 (MT5 전 최소 로컬 확인)

1. **Per-stage signal ledger (단계별 신호 장부)** — For each of the **32 pending stages (대기 32단계)**: materialized **-1/0/+1 count** vs documented **expected proxy count (예상 프록시 신호 수)**, split by **validation IS (검증 내부)** and **OOS (표본외)**. Hard fail any stage above a pre-declared tolerance (사전 허용 오차 초과 시 중단).

2. **Source-kind spot checks (원천 종류 표본 확인)** — One stage per kind (종류당 1단계): spot-check ~10 timestamps for sign, bar alignment, and IS/OOS membership. Effect: catches kind-specific reconstruction errors (종류별 복원 오류) without full re-audit.

3. **F26/F34 exclusion proof (F26/F34 제외 증명)** — Confirm they are labeled **logic_zero_signal_no_mt5_attempt (로직상 신호 0, MT5 시도 없음)** and absent from run manifests (실행 목록). Effect: prevents false “missing material (재료 없음)” reopening.

4. **Handoff identity bundle (인계 정체성 묶음)** — Per run: EBM table identity (피처명/버전), signal artifact hash (신호 산출물 해시), **RuntimeProbeEA** parameter set (exit/risk approximation flags: max hold, ATR, fixed-point 0.01). Effect: MT5 output can be traced to a specific approximation contract (근사 계약).

5. **F18 narrow check (F18 좁은 확인)** — Entry timestamp preservation (진입 시각 보존) only: count entries vs source trade log; do not expect exit parity (청산 동등 기대 금지). Document as **observation-only exit gap (관찰 한정 청산 간극)** before MT5.

6. **Pre-declared gap taxonomy (사전 선언 간극 분류)** — Write per stage which gaps are expected (**exit/risk**, **economics/cost**, **stage logic zero**) so post-MT5 attribution (사후 귀속) cannot drift into promotion language (승격 언어로 새지 않게).

---

**Bottom line (요약):** Proceed to MT5 as **runtime probe observation (런타임 탐침 관찰)** — do not skip solely because prior runtime handoff (이전 런타임 인계) was absent. First complete the six checks above; then MT5 results are legitimate **gap-attributed observation (간극 귀속 관찰)**, not stage winners or operating baselines (운영 기준선).

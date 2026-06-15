# Grok Receipt(그록 영수증): pre_mt5(MT5 전)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier55_pre_mt5_review`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
**Advice classification(조언 분류): accepted(수용)**

Spending one MT5 Strategy Tester pass on this single candidate now is reasonable within the stated claim boundary(주장 경계).

**Why accepted(수용 근거)**

1. **Proxy-first gate is met(프록시 우선 게이트 충족)**
   Stage-open Grok(단계 개방 그록) asked for identical sparse admission in proxy before MT5. That step is done, with ONNX parity(온엑스 동등성) passed and bounded val/OOS proxy metrics recorded.

2. **The probe matches the actual F55 question(F55 실제 질문과 일치)**
   F54 did not test sparse admission; it used raw score threshold export(원시 점수 문턱값보내기). F55’s design — keep all feature rows(피처 행) and veto non-admitted hits via RuntimeVetoTape(런타임 차단 테이프) — is exactly what MT5 must observe. A single runtime probe(런타임 탐침), not a sweep(탐색), is proportionate.

3. **Economics are not obviously dead at proxy(프록시에서 경제성이 바로 죽지 않음)**
   Val/OOS PF(수익팩터) ~1.13 and DD(낙폭) in a modest band are weak but not disqualifying for an observation-only probe. You already defined the close path: if density or PF/DD fails at MT5, record preserved clue(보존 단서) or negative memory(부정 기억) — not completion(완성).

4. **F54 MT5 fill history sets the right expectation(F54 MT5 체결 이력이 기대치를 맞춤)**
   F54 nearly filled every expected signal under raw threshold. That is a useful contrast baseline(대조 기준선): F55 is not re-proving “can MT5 trade at all?” but “does sparse admission + veto tape change density and economics vs proxy and vs F54 raw path?”

**Top failure risk(최상위 실패 위험)**

**Density alignment gap between admitted signals and executed trades(허용 신호 대비 실제 체결 밀도 불일치)** — proxy-runtime density misalignment(프록시-런타임 밀도 불일치).

Proxy already shows admitted signals/day(허용 신호/일) ~5.2–5.4 while proxy trades/day(프록시 체결/일) ~4.3–4.6, below the 5 target. F54’s near-1:1 expected-to-trade fill happened on the raw-threshold path, not sparse admission + daily_budget(일일 쿼터) + min_gap_bars(최소 간격 봉) + veto tape(차단 테이프). MT5 may widen that gap via `signal_diff`, `feature_ready_diff`, and veto timing, yielding trades/day under 5 even when admission logic looks correct in proxy.

**What to watch in the one MT5 run(한 번 MT5 실행에서 볼 것)**

- `trades/day` vs proxy trades/day and admitted signals/day
- `signal_diff` and `feature_ready_diff` — do vetoes stack on top of admission?
- PF/DD degradation vs proxy — small proxy edge may not survive runtime friction

**Claim boundary reminder(주장 경계 상기)**
Even if MT5 passes density, that only supports runtime probe observation(런타임 탐침 관찰). It does not justify baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) without further evidence.

## 1. `accepted(수용)`

**Dual-axis preservation(이중 축 보존) before MT5 Runtime Probe(MT5 런타임 탐침) is the right move(올바른 다음 행동).**
F68B showed an orthogonal gap(직교 간극): density clues(밀도 단서) hit trade count(거래 수) but PF(수익 팩터) is weak; PF clues(수익 팩터 단서) show strong proxy PF(강한 프록시 수익 팩터) but severe density gap(심한 밀도 간극). With `proxy joint pass count(프록시 네 축 동시 통과 수) = 0`, picking one “winner(승자)” now would collapse the tradeoff(트레이드오프) into a single story before runtime tests whether each pole(극) behaves differently under MT5. Keeping density axis(밀도 축) and PF axis(수익 팩터 축) is a disciplined scout design(탐색 설계), not premature promotion(조기 승격).

**ONNX scout export(ONNX 탐색보내기) of both ExtraTrees candidates(엑스트라트리스 후보) is useful enough(충분히 유용), even with no four-axis proxy pass(네 축 프록시 통과 없음).**
F68C claim boundary(주장 경계) is proxy/scout/pre-export only(프록시/탐색/보내기 전용). The value is not “we found a joint-pass candidate(통과 후보를 찾았다)” but narrowing the handoff surface(인계 표면 축소): train-only reconstruction(학습 전용 재구성), converter success filter(변환 성공 필터), ONNX probability parity(ONNX 확률 동등성), feature order hash(피처 순서 해시), and explicit handoff intent(인계 의도). Both use `extra_trees_shallow` — same model family(동일 모델군) reduces one confound(혼란 요인) while threshold/cooldown/side/exit(임계값/대기봉/방향/청산) stay maximally different between poles. The PF-axis candidate(수익 팩터 축 후보) will likely produce a sparse MT5 probe(희소 런타임 탐침); that is acceptable as a diagnostic pole(진단 극), not as a density target(밀도 목표).

**HGB low-DD density clue(HGB 저손실폭 밀도 단서) should be exported if converter support exists(변환기 지원 시보내기); otherwise preserved as clue(보존 단서), not invalid(무효).**
Codex’s conditional rule(조건부 규칙) matches the evidence: `f68b_547ac8b4ead1` is a distinct third pole(제3 극) — different model family(`hgb_small`), feature set(`no_mega_top3`), exit(`atr_sltp_conservative`), and better proxy DD band(프록시 손실폭 대역) than the main density ExtraTrees clue. Forcing export without converter support(변환기 없이 강제보내기) would waste F68C scope(범위); discarding it would lose a low-DD density clue(저손실폭 밀도 단서) that F68B already surfaced. Priority order(우선순서) is sensible: density ExtraTrees first, PF ExtraTrees second, HGB third if supported.

**Keep MT5 Runtime Probe(런타임 탐침) as mandatory next materialization(다음 필수 물질화), not runtime authority(런타임 권위).**
Meaningful proxy signal(의미 있는 프록시 신호) plus zero joint pass(동시 통과 0) means proxy alone cannot close the PF/density/DD gap read(간극 판독). F68C should produce comparable handoff artifacts(비교 가능 인계 산출물) for each exported pole, then let MT5 answer whether lifecycle economics proxy(생명주기 경제성 프록시) beats count/feature parity repair(개수/피처 동등성 수리) on PF/DD/trade density(수익 팩터/손실폭/거래 빈도).

**Drift risks(드리프트 위험) Codex should guard before MT5:**

| Risk(위험) | Guard(보호) |
|---|---|
| Train-only reconstruction drift(학습 전용 재구성 드리프트) vs F68B sweep logic(탐색 로직) | Same F68B logic(동일 로직), fixed seeds/splits(고정 시드/분할), document any delta(차이 기록) |
| Feature-order / feature-set mismatch(`full58` vs `no_mega_top3`) | Per-candidate feature order hash(후보별 피처 순서 해시); no shared bundle assumption(공유 번들 가정 금지) |
| Threshold sensitivity at export(보내기 시 임계값 민감도) (`0.3` vs `0.975`) | ONNX parity at operating thresholds(운영 임계값에서 동등성); note PF-axis may be parity-stable but runtime-sparse(동등하나 런타임 희소) |
| Exit-policy semantic gap(청산 정책 의미 간극) (`close_horizon` vs `atr_sltp_conservative`) | Handoff intent must name exit mapping(청산 매핑 명시); do not assume proxy exit equals EA exit(프록시 청산 ≠ EA 청산 가정 금지) |
| PF=99 saturation artifact(수익 팩터 포화 아티팩트) on PF-axis clue | Treat as proxy ceiling clue(프록시 상한 단서), not literal runtime PF expectation(실제 런타임 PF 기대 아님) |
| Proxy DD%(프록시 손실폭) vs runtime DD(런타임 손실폭) definition gap | Separate labels in reports(보고서에서 라벨 분리); no “proxy DD under 10 ⇒ runtime DD OK”(프록시 손실폭 10 미만 ⇒ 런타임 OK 주장 금지) |
| Cooldown/side divergence(대기봉/방향 불일치) (`0/long_only` vs `1/both`) | Per-axis run manifests(축별 실행 목록); no merged “best of both” config(양쪽 합친 최적 설정 금지) |

---

## 2. `rejected_or_risky(거절 또는 위험)`

**Reject collapsing three axes into one “primary export(주보내기)” before parity and converter outcomes(동등성·변환 결과).**
Density, PF, and conditional low-DD HGB are structurally incompatible on proxy metrics(프록시 지표상 양립 불가). Early unification(조기 통합) would recreate the F68B failure mode(실패 양상): a config that looks balanced in scoring(점수화) but fails on the axis that MT5 actually cares about(런타임이 실제로 보는 축).

**Reject treating PF-axis export success(수익 팩터 축보내기 성공) as evidence the density gap is “solved(해결됨)” by threshold tuning(임계값 조정).**
`f68b_3481a04983ee` at `trades_day=1` is a density-gap pole(밀도 간극 극), not a near-miss(아깝게 빗나감). ONNX parity pass(동등성 통과) only proves probability handoff(확률 인계); it does not justify lowering threshold(임계값 하향) or merging with density config(밀도 설정 병합) inside F68C.

**Risky: scoring all three exports equally in one composite rank(세보내기를 하나의 복합 순위로 동등 평가).**
Axes answer different questions(서로 다른 질문에 답함): “does density survive runtime PF?(밀도가 런타임 PF를 버티나?)”, “does extreme PF proxy survive at all in MT5?(극단 PF 프록시가 MT5에서 존재하나?)”, “does low-DD density generalize across model family?(저손실폭 밀도가 모델군을 넘나?)”. A single leaderboard(단일 순위표) invites cherry-picking(선별) across incompatible dimensions(호환 불가 차원).

**Risky: expanding F68C scope(범위 확장) to repair weak PF on density axis(밀도 축 약한 PF 수리) or lift density on PF axis(수익 팩터 축 밀도 끌어올리기) before ONNX + MT5 probe(탐침 전).**
F68B already swept broadly(넓게 탐색함); `density-band strict PF clues = 0` suggests repair inside F68C(단계 내 수리) blurs scout vs repair stage(탐색 vs 수리 단계 혼동) and delays the mandatory runtime gate(필수 런타임 게이트).

**Risky: interpreting `meaningful PF/density signal candidates = 293` as “many viable ONNX targets(많은 ONNX 대상).”**
Most are PF-clue-with-density-gap variants(밀도 간극 있는 PF 단서 변형). F68C should stay with the named poles(명명된 극) unless local scoring(로컬 점수화) shows export/parity failure(보내기·동등성 실패) on those poles.

---

## 3. `needs_local_verification(로컬 검증 필요)`

- **Converter support for `hgb_small`(HGB 변환기 지원 여부)** — determines export vs preserve-only(보내기 vs 보존만) for `f68b_547ac8b4ead1`.
- **Train-only reconstruction fidelity(학습 전용 재구성 충실도)** — whether F68C models reproduce F68B validation/OOS proxy metrics(검증/표본외 프록시 지표) within tolerance(허용 오차).
- **ONNX probability parity pass/fail per candidate(후보별 ONNX 확률 동등성 통과/실패)** — especially at `0.975` vs `0.3` thresholds.
- **Feature order hash stability(피처 순서 해시 안정성)** across `full58` and `no_mega_top3` materialization paths(물질화 경로).
- **PF=99 semantics(의미)** — cap, division-by-near-zero, or single-trade artifact(단일 거래 아티팩트); affects how PF-axis MT5 results should be read(판독 방식).
- **Actual F68C export count(실제보내기 수)** after converter filter(변환 필터) — may be 0–3 poles; probe plan(탐침 계획) depends on this.
- **EA/run-manifest mapping(실행 목록 매핑)** for `close_horizon` vs `atr_sltp_conservative`, cooldown `0/1`, and `long_only` vs `both` — proxy-to-runtime parity level(프록시-런타임 동등 수준) unknown from snapshot(스냅샷만으로 불명).
- **Whether F68B candidate IDs(후보 ID) bind to exact row-level configs(행 수준 설정)** in ledger(장부) — required to ensure reconstruct targets the intended pole(의도한 극 재구성).

---

**Claim boundary(주장 경계):** This review endorses scout/pre-export axis preservation(탐색/보내기 전 축 보존) and conditional HGB handling(조건부 HGB 처리) only. It does not assert completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성). MT5 Runtime Probe(런타임 탐침) remains the gate that turns ONNX scout artifacts(ONNX 탐색 산출물) into runtime evidence(런타임 근거).

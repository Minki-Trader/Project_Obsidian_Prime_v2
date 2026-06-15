# Grok Receipt(그록 영수증): pre_mt5(MT5 전)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier58_pre_mt5_review`
- classification(분류): `needs_local_verification(로컬 검증 필요)`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
## Validity

**Weak-but-valid runtime probe(약하지만 유효한 런타임 탐침)** — not invalid before MT5(MT5 전 무효 아님).

Policy repair(정책 수리) removes the main pre-MT5 invalidity risk: inherited F52 lifecycle compression(F52 생명주기 압축 상속) conflicted with the declared runtime stack(선언된 런타임 스택) — short-only(숏 전용), raw direct threshold(원천 직접 임계값), no sparse admission(희소 진입 없음), no entry-transition compression(진입 전환 압축 없음), max hold 4 bars(최대 보유 4봉). After that removal, the probe question(탐침 질문) matches the artifact chain(산출물 연쇄): train-only friction-survivability label(학습 전용 마찰 생존성 라벨) → ONNX export(온엑스보내기) → thin MT5 runtime(얇은 MT5 런타임).

Supporting bounded evidence(제한 근거):
- ONNX parity passed(온엑스 동등성 통과), `max_abs_diff ≈ 1.88e-07` — export/runtime inference path(보내기/런타임 추론 경로) is not blocked pre-MT5.
- Primary all-signal proxy(주 전체 신호 프록시) is marginally positive on validation/OOS(검증/표본외): PF `1.0716/1.1017` — thin edge(얇은 엣지), not dead-on-arrival(시작부터 사망 아님).
- Codex boundary(코덱스 경계) says weak proxy / high overlap risk / no authority(약한 프록시·높은 겹침 위험·권위 없음) — that downgrades claim strength(주장 강도 하향), not setup validity(설정 유효성).
- User rule in snapshot(스냅샷 사용자 규칙): frontier stages get MT5 runtime probe unless invalid setup(무효 설정이 아니면 전선 단계 MT5 런타임 탐침 필수).

What keeps it “weak”(약함 유지 요인), not “strong”(강함 아님):
- High overlap with F57/F56 memories(F57/F56 기억과 높은 겹침) undermines orthogonality of the relabeling story(재라벨링 직교성 스토리), not ONNX/parity validity(온엑스/동등성 유효성).
- Compressed secondary proxy(압축 보조 프록시) is flatter (`PF ~1.05`) and must not be promoted to primary success(주 성공 뷰로 승격하면 안 됨) — but it is already labeled secondary(이미 보조로 라벨됨).

**Invalid-before-MT5 bar not met(MT5 전 무효 기준 미충족):** no parity fail(동등성 실패 없음), no incoherent runtime policy after repair(수리 후 런타임 정책 비일관 없음), no evidence that proxy view is entirely incompatible with declared runtime(프록시 뷰가 선언 런타임과 완전 비호환이라는 근거 없음).

---

## Failure Modes

Codex should separate all five in closeout(마감에서 다섯 가지 모두 분리), with distinct success/fail signatures(성공/실패 시그니처 분리):

| Failure mode(실패 모드) | Must separate?(분리 필수?) | Closeout signature(마감 시그니처) |
|---|---|---|
| **non_orthogonal_relabeling(직교성 부족 재라벨링)** | **Yes** | F57 overlap `1.0`, Jaccard `0.6549`; F56 overlap `0.9324`, Jaccard `0.7513`. MT5 trade/signal overlap with F57 fast-exit or F56 adverse paths(경로) remains high while F58 claims a new friction-survivability source(새 마찰 생존성 원천 주장). |
| **source_no_transfer(원천 전이 실패)** | **Yes** | Core hypothesis test(핵심 가설 검증): train-only label edge(학습 전용 라벨 엣지) does not appear in MT5 PF/trade economics( MT5 PF/거래 경제성에 안 나타남). Python proxy PF > 1 but MT5 PF ≤ 1 or sign flip(부호 반전) with similar coverage(유사 커버리지). |
| **density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)** | **Yes** | All-signal proxy trades/day `~7.7–9.3` vs compressed `~3.8–4.5`. Runtime without sparse admission(희소 진입 없는 런타임) likely aligns to higher density(더 높은 밀도 정렬). Failure = MT5 reaches plausible density(그럴듯한 밀도 도달) but PF/DD collapses vs all-signal proxy(전체 신호 프록시 대비 PF/DD 붕괴), especially vs thin compressed margins(압축 쪽 얇은 마진 대비). |
| **proxy_still_misaligned(프록시 여전히 불정렬)** | **Yes** | Policy repair fixed compression inheritance(압축 상속), but proxy may still encode removed lifecycle rules(제거된 생명주기 규칙이 프록시에 잔존). Failure = MT5 matches neither primary all-signal nor secondary compressed view(주·보조 프록시 둘 다 불일치) under the repaired policy(수리된 정책 하). |
| **parity_fail(동등성 실패)** | **Yes, but secondary pre-MT5(예비적)** | Pre-MT5 ONNX parity passed(사전 통과). Separate anyway: MT5 runtime inference drift(런타임 추론 드리프트), feature pipeline mismatch(피처 파이프라인 불일치), or post-repair manifest/hash drift(수리 후 매니페스트/해시 드리프트) vs export-time parity(보내기 시점 동등성). |

**Ordering for interpretation(해석 순서):** parity_fail → proxy_still_misaligned → density_align_economics_collapse → source_no_transfer → non_orthogonal_relabeling. The last explains *why* transfer failed(전이 실패 이유); it does not alone invalidate the probe(탐침 자체를 무효화하진 않음).

---

## Missing Checks

From bounded evidence only(제한 근거만 기준), these pre-MT5 local checks(사전 MT5 로컬 확인) are absent or not evidenced(없거나 근거 미기재):

1. **Post-repair artifact closure(수리 후 산출물 폐쇄)** — No manifest/module/set hash delta(매니페스트·모듈·설정 해시 변화 없음) proving F52 lifecycle compression( F52 생명주기 압축) is gone from EA, `.set`, and run_manifest(실행 매니페스트) — only a narrative repair note(서술 수리 메모만).
2. **Proxy–runtime policy alignment audit(프록시–런타임 정책 정렬 감사)** — No explicit checklist that primary all-signal proxy(주 전체 신호 프록시) was recomputed under the repaired policy(수리 정책으로 재계산됨) (no compression, no cooldown, no close_on_flat, max hold 4, ATR SL/TP on(활성)).
3. **Orthogonality operationalization(직교성 operationalization)** — Jaccard/overlap vs F57/F56 without trade-level timing delta(거래 시점 차이), entry cohort diff(진입 코호트 차이), or label-conditional PF decomposition(라벨 조건부 PF 분해). Overlap `1.0` with F57 needs a stricter non-identity check(동일성 배제 확인).
4. **Density bridge(밀도 브리지)** — No mapped expectation(기대값 매핑 없음): proxy trades/day → expected MT5 trades/day under raw threshold + no sparse admission(원천 임계값·희소 진입 없음). Without it, density_align_economics_collapse(밀도 정렬 경제성 붕괴) is hard to judge at closeout(마감 판정 어려움).
5. **Tier paired records(티어 쌍 기록)** — No Tier A / Tier B / combined lines(티어 A·B·합산 행 없음) in snapshot; if stage tier policy applies(티어 정책 적용 시), missing_required(필수 누락) should be stated before over-interpreting proxy(프록시 과해석 전 명시).
6. **Attribution slice(기여 분해)** — No decomposition of PF across friction label(마찰 라벨), `q85` threshold(임계값), short-fav/adv filters(숏 필터), max-hold/ATR exit(보유·ATR 청산) — source_no_transfer vs threshold economics(임계값 경제성) stay conflated(혼동).
7. **MT5 probe forensics plan( MT5 탐침 포렌식 계획)** — No pre-declared tester identity(테스터 정체성 사전 선언): spread, commission, slippage, modeling mode, deposit/leverage(스프레드·수수료·슬리피지·모델링·예탁·레버리지) — needed to separate runtime failure from setup drift(런타임 실패 vs 설정 드리프트 분리).
8. **Compressed proxy lineage(압축 프록시 계보)** — Secondary compressed metrics(보조 압축 지표) present without proof they were computed with repaired policy only(수리 정책만으로 계산됐다는 증명 없음); stale compression artifacts(낡은 압축 산출물) would poison risk context(위험 문맥 오염).

**None of the above block the probe(위 항목들이 탐침 자체를 막진 않음)** if MT5 is treated as the decisive alignment test( MT5를 결정적 정렬 검증으로 봄) — but they should be logged as needs_local_verification(로컬 검증 필요) items in closeout(마감 기록), not assumed done(완료로 가정 금지).

# F73D Pre-MT5 Grok Review(F73D 사전 MT5 Grok 검토)

You are Grok(Grok, 그록), an external second opinion(외부 2차 의견) reviewer. Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Current State(현재 상태)

- Active stage(활성 단계): `stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap`.
- Hypothesis(가설): session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 F72 runtime economics gap(F72 런타임 경제성 간극)을 분리할 수 있는지 본다.
- F73A stage open(단계 개방): Grok accepted(수용) direction but rejected(거절) unbounded combinatorial sweep(무제한 조합 탐색). Codex narrowed matrix(행렬 축소).
- F73B proxy scout(프록시 탐색): 258 candidates(후보), scout clue(탐색 단서) 0, meaningful(의미 후보) 0. Best OOS(표본외) net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `1111.6351 / 1.6559 / 3.1796% / 0.7897` but validation(검증) was negative.
- F73C repair proxy scout(수리 프록시 탐색): 342 candidates(후보), dual-positive(검증+표본외 양수) 48, scout clue(탐색 단서) 0, meaningful(의미 후보) 0.
- F73C best candidate(최선 후보): `f73c_0002`, surface(표면) `repair_open_long_quality_density`, dataset(데이터셋) `fwd12`, feature_bundle(피처 묶음) `session_regime_core`, target(목표) `long_quality`, model(모델) `small_nn_16`, gate(게이트) `cash_open`, target_tpd(목표 일거래) `1.25`.
- F73C best validation KPI(검증 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `2251.0309 / 1.3119 / 7.6708% / 1.2593`.
- F73C best OOS KPI(표본외 KPI): net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `1431.5035 / 1.3587 / 4.2453% / 1.0000`.
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Proposed Codex Direction Before Grok(Grok 전 Codex 방향)

Proceed to one mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) because F73 stage lifecycle(단계 생명주기) requires a runtime probe and F73C produced a dual-positive near-miss(검증+표본외 양수 근접 단서).

Runtime materialization proposal(런타임 물질화 제안):

1. Use F73C best as seed surface(씨앗 표면), not success(성공) and not completion candidate(완성 후보).
2. Because current RuntimeProbeEA(런타임 탐침 EA) expects three probabilities p_short/p_flat/p_long(숏/관망/롱 3확률), build a runtime-compatible 3-class bridge(런타임 호환 3분류 연결 모델) on the same F73C surface: `fwd12`, `session_regime_core`, `cash_open`.
3. Label bridge(연결 라벨): long_quality(롱 품질) => `+1`, short_quality(숏 품질) => `-1`, otherwise flat(관망) => `0`; if both sides qualify(양방향 동시 적격), choose the side with higher path quality(경로 품질).
4. First try same model family(동일 모델 계열) `small_nn_16` as 3-class sklearn pipeline(3분류 사이킷런 파이프라인). If ONNX export/parity(ONNX 내보내기/동등성) fails locally, switch to `extra_trees_ref` as a documented repair(기록된 수리) rather than silently changing model family(모델 계열).
5. Select long side only(롱만 선택) with `cash_open` gate(정규장 초반 게이트), validation-calibrated threshold(검증 보정 임계값) targeting about 1.25 trades/day(일 1.25회), selected-entry runtime veto tape(선택 진입 런타임 차단 테이프), and no final-claim language(강한 최종 주장 없음).
6. Run MT5 Strategy Tester(전략 테스터) attempts for validation(검증) and OOS(표본외), record runtime KPI(런타임 KPI), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일거래), and gap cause(간극 원인).

## Success Criteria For This Probe(이번 탐침 성공 기준)

- Materialization succeeds(물질화 성공): model artifact(모델 산출물), ONNX(온엑스), feature CSV(피처 CSV), selected-entry tape(선택 진입 테이프), `.set/.ini` are produced with hashes(해시).
- Local parity passes(로컬 동등성 통과): probability parity(확률 동등성), signal parity(신호 동등성), feature readiness parity(피처 준비 동등성).
- MT5 tester produces runtime observation(런타임 관찰 산출): validation and OOS receipts(검증/표본외 영수증), not runtime authority(런타임 권위 아님).
- If runtime economics are weak(런타임 경제성 약함), record proxy/runtime gap(프록시/런타임 간극) and repair action(수리 행동), not success(성공).

## Drift Risks(드리프트 위험)

- Binary proxy to 3-class bridge(이진 프록시에서 3분류 연결)는 not identical(동일하지 않음). It must be reported as bridge materialization(연결 물질화), not direct F73C candidate authority(직접 F73C 후보 권위).
- Trades/day(일거래) is far below final target 5-10/day(최종 목표 5-10회/일). This can only be runtime probe observation(런타임 탐침 관찰).
- PF(수익 팩터) is about 1.3 in proxy(프록시), below final PF 2-3+(최종 수익 팩터 2-3 이상).
- Fwd18 inverse candidates(18봉 역방향 후보) have high DD(높은 손실폭), so they should not be first MT5 materialization despite higher OOS net(표본외 순수익).

## Question(질문)

Should Codex proceed with this narrow F73D MT5 Runtime Probe(좁은 F73D MT5 런타임 탐침) as proposed? Classify advice into accepted(수용), rejected(거절), and needs_local_verification(로컬 검증 필요). Focus on whether the bridge plan preserves claim boundary(주장 경계), parity requirements(동등성 요구), and avoids repeating F72 trade-shape-first repair(거래 형태 우선 수리 반복).

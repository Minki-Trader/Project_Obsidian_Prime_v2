# F73F Pre-MT5 Grok Review(F73F 사전 MT5 Grok 검토)

You are Grok(Grok, 그록), an external second opinion(외부 2차 의견) reviewer. Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Current State(현재 상태)

- Active stage(활성 단계): `stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap`.
- F73C best binary proxy(최선 이진 프록시): `f73c_0002`, fwd12/session_regime_core/long_quality/small_nn_16/cash_open. Validation(검증) net/PF/DD/tpd `2251.0309 / 1.3119 / 7.6708% / 1.2593`; OOS(표본외) `1431.5035 / 1.3587 / 4.2453% / 1.0000`.
- F73D mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침): completed(완료), validation and OOS tester receipts(검증/표본외 테스터 영수증) present.
- F73D bridge materialization(연결 물질화): 3-class bridge from F73C seed(이진 F73C 씨앗에서 3분류 연결), model `small_nn_16`, probability parity(확률 동등성) 3/3, signal parity(신호 동등성) 3/3.
- F73D runtime OOS(런타임 표본외): net/PF/DD/tpd `48.84 / 1.09 / 15.33% / 1.0103`; signal diff(신호 차이) 0, feature diff(피처 차이) 0.
- F73E gap analysis(간극 분석): primary gap cause(주요 간극 원인) is proxy_bridge_selection_divergence(프록시-연결 선택 분기). F73C binary vs F73D bridge OOS overlap(중복) only `0.1949`; validation overlap `0.1824`. Secondary cause(보조 원인): trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극).
- Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Proposed Codex Direction Before Grok(Grok 전 Codex 방향)

Proceed to a capped repair(상한 있는 수리) named F73F: direct binary ONNX adapter runtime repair(직접 이진 ONNX 어댑터 런타임 수리).

Repair proposal(수리 제안):

1. Retrain the exact F73C binary candidate(정확한 F73C 이진 후보 재학습): `fwd12`, `session_regime_core`, `long_quality`, `small_nn_16`, `cash_open`, target_tpd `1.25`, score threshold near F73C `0.4489733875`.
2. Verify proxy reproduction(프록시 재현): selected count and KPI(선택 수와 KPI)가 F73C `f73c_0002`와 materially matches(실질적으로 일치) or record delta(차이 기록). No silent drift(조용한 드리프트 없음).
3. Export binary ONNX(이진 ONNX) with probability output `[p_flat, p_long]`.
4. Patch ONNX graph(ONNX 그래프 패치) into RuntimeProbeEA-compatible three-column output(런타임 탐침 EA 호환 3열 출력): `[p_short=0, p_flat, p_long]`. This avoids changing EA modules(EA 모듈 변경 없음) and avoids 3-class bridge label skew(3분류 연결 라벨 왜곡).
5. Run local parity(로컬 동등성): binary sklearn probability vs patched ONNX mapped probability(이진 사이킷런 확률 대 패치 ONNX 매핑 확률), signal parity(신호 동등성), feature readiness parity(피처 준비 동등성), and source reproduction delta(원천 재현 차이).
6. If parity passes(동등성 통과), run MT5 Strategy Tester(전략 테스터) validation and OOS(검증/표본외) with selected-entry runtime veto tape(선택 진입 런타임 차단 테이프). Record runtime KPI(런타임 KPI), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), proxy/runtime gap cause(간극 원인).
7. Stop condition(중단 조건): if graph patch, parity, or tester receipts fail, close the repair as blocked or invalid setup(차단 또는 무효 설정), not success(성공 아님).

## Why This Is Not F72 Repeat(F72 반복이 아닌 이유)

- It does not change trade shape first(거래 형태 우선 변경 없음). It removes a runtime handoff distortion(런타임 인계 왜곡 제거) introduced by F73D bridge.
- It keeps the F73 topic(주제): feature/model/session-regime signal handoff(피처/모델/세션-장세 신호 인계).
- It still accepts that density(밀도) is low and PF(수익 팩터) is weak. This is a repair probe(수리 탐침), not completion(완성).

## Question(질문)

Should Codex proceed with F73F direct binary ONNX adapter runtime repair(직접 이진 ONNX 어댑터 런타임 수리) before closing F73? Classify advice into accepted(수용), rejected(거절), and needs_local_verification(로컬 검증 필요). Focus on whether this repair is justified by F73E gap analysis(간극 분석), whether it preserves claim boundary(주장 경계), and what local checks are mandatory before MT5 execution(MT5 실행 전 필수 로컬 점검).

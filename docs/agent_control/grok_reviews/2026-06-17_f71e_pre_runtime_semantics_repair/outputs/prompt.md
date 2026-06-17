# F71E Pre-Runtime Repair Review(F71E 런타임 수리 전 검토)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자). Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say needs_local_verification(로컬 검증 필요).

## Current State(현재 상태)

- stage(단계): `stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd`
- source candidate(원천 후보): `f71b_1e511d3db9c3`
- F71 hypothesis(가설): economics-native label/target and selection(경제성 네이티브 라벨/목표와 선택)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 보존하는 scout clue(탐색 단서)를 만들 수 있는지 본다.
- claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## F71D Runtime Probe Observation(F71D 런타임 탐침 관찰)

F71D materialized(물질화) `f71b_1e511d3db9c3` into ONNX(온엑스), feature CSV(피처 CSV), selected-entry RuntimeVetoTape(선택 진입 런타임 차단 테이프), and MT5 Strategy Tester(MT5 전략 테스터).

ONNX probability parity(온엑스 확률 동등성): passed(통과), max_abs_diff about `1.8e-7`.

ONNX signal parity(온엑스 신호 동등성): passed(통과):

| split(분할) | expected selected signals(예상 선택 신호) | ONNX signal count(온엑스 신호 수) | diff(차이) |
|---|---:|---:|---:|
| train | 989 | 989 | 0 |
| validation | 345 | 345 | 0 |
| oos | 256 | 256 | 0 |

MT5 runtime result(MT5 런타임 결과):

| split(분할) | proxy net/PF/DD/trades_day(프록시 순수익/수익 팩터/손실폭/일거래) | runtime net/PF/DD/trades_day(런타임 순수익/수익 팩터/손실폭/일거래) | expected signal(예상 신호) | runtime signal/order(런타임 신호/주문) |
|---|---|---|---:|---:|
| validation | `1098.07 / 1.2316 / 2.61% / 1.2720` | `24.43 / 0.00 / 0.78% / 0.0037` | 345 | 1 |
| oos | `899.15 / 1.2505 / 3.54% / 1.3129` | `0.65 / 1.11 / 2.49% / 0.0103` | 256 | 2 |

Local gap finding(로컬 간극 발견):

- feature readiness diff(피처 준비 차이): `0`.
- report status(보고서 상태): completed(완료).
- telemetry(런타임 기록): most runtime rows were `edge_margin_not_met(엣지 마진 미달)`.
- F71B proxy selection used custom score(맞춤 점수):
  `max(p_long,p_short) - 0.55*p_flat + 0.35*abs(p_long-p_short)`.
- EA runtime decision(전문가 자문 런타임 결정) used `edge_margin(엣지 마진)`:
  `max(p_long,p_short) - p_flat`.
- Therefore the likely gap cause(가능 간극 원인) is threshold semantics mismatch(임계값 의미 불일치), not ONNX parity failure(온엑스 동등성 실패) and not feature readiness failure(피처 준비 실패).

## Proposed Repair(제안 수리)

Run a single F71E repair probe(수리 탐침) that keeps the same model/label/feature set(같은 모델/라벨/피처 묶음) but changes selection/threshold semantics(선택/임계값 의미) to EA-compatible edge margin(EA 호환 엣지 마진).

Local proxy sweep(로컬 프록시 훑기) for edge_margin quantile repair(엣지 마진 분위 수리):

| repair(수리) | validation net/PF/DD/trades_day(검증 순수익/수익 팩터/손실폭/일거래) | oos net/PF/DD/trades_day(표본외 순수익/수익 팩터/손실폭/일거래) | scout(탐색 단서) |
|---|---|---|---|
| edge_margin q20 | `703.81 / 1.1356 / 4.85% / 1.3789` | `836.27 / 1.2195 / 2.40% / 1.3798` | true |
| edge_margin q30 | `1109.97 / 1.2259 / 2.59% / 1.3457` | `745.26 / 1.1942 / 2.73% / 1.3747` | true |
| edge_margin q40 | `748.35 / 1.1486 / 2.89% / 1.3162` | `858.87 / 1.2351 / 2.92% / 1.3232` | true |
| edge_margin q50 | `785.83 / 1.1623 / 3.26% / 1.2536` | `742.65 / 1.2042 / 3.02% / 1.2923` | true |

Codex proposed direction(Codex 제안 방향): run one MT5 repair probe(MT5 수리 탐침) on `edge_margin q40` because it is EA-compatible(EA 호환), keeps OOS PF(표본외 수익 팩터) strongest among the listed edge repairs, and should directly test whether signal count parity(신호 수 동등성) recovers.

## Question(질문)

Should Codex run the F71E MT5 repair probe(MT5 수리 탐침) on `edge_margin q40`, or is another action better from this bounded evidence(제한 근거)? Classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요). Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

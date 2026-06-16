# F70E Pre-Repair Runtime Probe Review(F70E 수리 전 런타임 탐침 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견). Answer only from this bounded evidence(제한 근거). Do not inspect files, run tools, browse, or claim local verification(로컬 검증).

## Current State(현재 상태)

- Stage(단계): `stage_frontier_70__regime_specific_asymmetric_value_exit_model_rotation`
- Completed run(완료 실행): `frontier70D_label_regime_stability_runtime_probe_v1`
- Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## F70D Evidence(F70D 근거)

F70D materialized two F70C near-miss axes(F70C 근접 실패 축 2개) into ONNX/RuntimeVetoTape/MT5(온엑스/런타임 차단 테이프/MT5).

- ONNX probability parity(온엑스 확률 동등성): passed(통과) for both axes.
- ONNX signal parity(온엑스 신호 동등성): passed(통과) for both axes.
- signal_count_diff(신호 수 차이): 0 on train/validation/OOS(훈련/검증/표본외).
- feature_ready_diff(피처 준비 차이): 0 on validation/OOS(검증/표본외).

Runtime KPI(런타임 핵심 성과 지표):

| axis(축) | split(분할) | runtime net/PF/DD/trades/day(런타임 순수익/수익 팩터/손실폭/일거래) | proxy net/PF/DD/trades/day(프록시 순수익/수익 팩터/손실폭/일거래) | selected trades(선택 거래) | runtime trades(런타임 거래) |
|---|---|---|---|---:|---:|
| reference_low_dd_axis | validation | 105.04 / 1.08 / 13.73 / 3.5294 | 527.46 / 1.1676 / 4.3626 / 0.9365 | 254 | 960 |
| reference_low_dd_axis | OOS | 119.38 / 1.13 / 10.74 / 3.3590 | 1153.65 / 1.5657 / 1.8239 / 0.8907 | 174 | 655 |
| small_nn_density_axis | validation | 226.24 / 1.14 / 8.69 / 4.0184 | 835.79 / 1.1975 / 4.3381 / 1.1466 | 311 | 1093 |
| small_nn_density_axis | OOS | 92.29 / 1.06 / 17.50 / 4.8821 | 430.60 / 1.1241 / 2.8760 / 1.2254 | 239 | 952 |

Observed gap cause(관찰된 간극 원인): `trade_lifecycle_gap_after_signal_parity`.

Interpretation(해석): The model/feature/signal bridge is exact(정확) enough for observation, but runtime trading takes many more entries than the proxy selected non-overlap entries(프록시 선택 비중첩 진입). This inflates trade density(거래 밀도), weakens PF(수익 팩터), and expands DD(손실폭).

## Proposed Repair(제안 수리)

Run a fixed repair probe(고정 수리 탐침):

- Keep the exact same two models(모델), labels(라벨), feature sets(피처 묶음), thresholds(임계값), and decision mode(의사결정 방식).
- Do not run threshold sweep(임계값 탐색), model tuning(모델 튜닝), or post-hoc candidate search(사후 후보 탐색).
- Change only RuntimeVetoTape semantics(런타임 차단 테이프 의미):
  - F70D tape allowed every regime mask active bar(장세 마스크 활성 봉).
  - F70E repair tape will allow only the proxy selected non-overlap entry bars(프록시 선택 비중첩 진입 봉) and veto all other bars.
- Re-run the same 2 axes x validation/OOS(검증/표본외) as a narrow MT5 Runtime Probe(MT5 런타임 탐침).

Expected learning(예상 학습):

- If trade count moves close to selected proxy trades(프록시 선택 거래), the F70D gap was runtime entry lifecycle semantics(런타임 진입 생명주기 의미).
- If PF/DD still collapse(수익 팩터/손실폭 붕괴), the label/model edge itself is too weak after MT5 economics(MT5 경제성).
- This remains repair observation(수리 관찰), not completion/promotion/runtime authority(완성/승격/런타임 권위).

## Question(질문)

Is this selected-entry RuntimeVetoTape repair(선택 진입 런타임 차단 테이프 수리) a legitimate next repair under the F70 hypothesis lifecycle(가설 생명주기), or should F70 close as preserved clue/negative memory(보존 단서/부정 기억) without another MT5 probe?

Classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) candidates. Also name any guardrails(보호 조건) Codex should enforce.

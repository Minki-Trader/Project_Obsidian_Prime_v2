# Frontier73E Proxy/Runtime Gap Analysis(F73E 프록시/런타임 간극 분석)

Updated(갱신): 2026-06-17T02:37:23Z

- status(상태): `proxy_runtime_gap_analysis_completed`
- judgment(판정): `runtime_gap_binary_bridge_divergence_repair_probe_required_no_authority`
- source_candidate(원천 후보): `f73c_0002`
- materialization_mode(물질화 방식): `bridge_3class_from_f73c_seed`
- model_family_used(사용 모델 계열): `small_nn_16`
- claim_boundary(주장 경계): `gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Gap Table(간극 표)

| split(분할) | source binary PF/DD/tpd(원천 이진 수익 팩터/손실폭/일거래) | bridge proxy PF/DD/tpd(연결 프록시 수익 팩터/손실폭/일거래) | runtime PF/DD/tpd(런타임 수익 팩터/손실폭/일거래) | parity diff(동등성 차이) | overlap(중복) |
|---|---:|---:|---:|---:|---:|
| validation | 1.3118881492172865/7.67075126647951/1.2592592592592593 | 0.8737050488310499/15.626041001510638/1.25 | 0.83/26.39/0.8382352941176471 | signal 0, feature 0 | 0.1823529411764705 |
| oos | 1.3586513026740523/4.245295150756847/1.0 | 1.0948640212672127/13.278702453613258/1.7473684210526317 | 1.09/15.33/1.0102564102564102 | signal 0, feature 0 | 0.1948717948717948 |

## Attribution(귀인)

- observed_change(관찰 변화): F73C binary proxy(이진 프록시)는 OOS PF/DD/tpd `1.3587/4.2453/1.0`이었지만, F73D runtime(런타임)은 `1.09/15.33/1.0103`으로 약해졌다.
- comparison_baseline(비교 기준): F73C `f73c_0002` binary small_nn_16(이진 작은 신경망) candidate and F73D 3-class bridge(3분류 연결) runtime.
- likely_driver_primary(주요 원인): proxy_bridge_selection_divergence(프록시-연결 선택 분기). OOS overlap(중복)은 약 19%라 F73D bridge(연결)는 F73C 후보를 직접 보존하지 못했다.
- likely_driver_secondary(보조 원인): trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극). Signal/feature diff(신호/피처 차이)는 0이지만 OOS signal 332개가 runtime trade 197개로 줄었다.
- trade_shape(거래 형태): OOS runtime win rate(승률) `41.62%`, payoff ratio(손익비) `1.53`, DD(손실폭) `15.33%`, trades/day(일거래) `1.01`.
- attribution_confidence(귀인 신뢰도): high for bridge divergence(연결 분기 높음), medium for lifecycle cost shape(생명주기 비용 형태 중간).

## Repair Decision(수리 결정)

Next repair(다음 수리): direct binary ONNX adapter(직접 이진 ONNX 어댑터)로 F73C binary probability(이진 확률)를 `[p_short=0, p_flat, p_long]` 3-column runtime output(3열 런타임 출력)으로 감싸서 bridge divergence(연결 분기)를 제거한다.

Effect(효과): 같은 F73C binary signal(이진 신호)을 최대한 보존한 채 MT5 Runtime Probe(MT5 런타임 탐침)를 다시 관찰하고, 그래도 경제성이 무너지면 signal parity 문제가 아니라 lifecycle/execution economics(생명주기/실행 경제성) 문제로 더 강하게 좁힐 수 있다.

## Next Action(다음 행동)

`frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1`.

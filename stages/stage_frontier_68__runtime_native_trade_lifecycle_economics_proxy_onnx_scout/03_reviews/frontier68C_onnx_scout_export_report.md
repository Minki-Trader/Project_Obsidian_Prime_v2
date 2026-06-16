# F68C ONNX Scout Export(F68C ONNX 탐색 내보내기)

Updated(갱신): 2026-06-16T17:14:42Z

## Action And Effect(행동 및 효과)

Action(행동): F68B의 density axis(밀도 축), PF axis(수익 팩터 축), low-DD density axis(저손실폭 밀도 축)을 F68B logic(로직)으로 재학습하고 ONNX scout export(ONNX 탐색 내보내기)를 시도했다.

Effect(효과): 한 후보를 winner(승자)처럼 고르지 않고, MT5 Runtime Probe(MT5 런타임 탐침)로 물질화할 후보 축과 인계 계약(handoff contract, 인계 계약)을 분리 기록했다.

## Grok Review(그록 검토)

- receipt(영수증): `docs/agent_control/grok_reviews/2026-06-17_f68c_pre_onnx_candidate_axis_review/f68c_pre_onnx_candidate_axis_receipt.md`.
- clean_output(정리 출력): `docs/agent_control/grok_reviews/2026-06-17_f68c_pre_onnx_candidate_axis_review/outputs/clean_output.md`.
- classification(분류): dual-axis preservation(이중 축 보존) accepted(수용), single leaderboard(단일 순위표) rejected_or_risky(거절 또는 위험), converter/parity(변환기/동등성)는 local verification(로컬 검증 필요).

## Candidate Axis Results(후보 축 결과)

### density_axis - `f68b_23f4d4607a78`

- feature/model(피처/모델): `full58(전체58)` / `extra_trees_shallow(얕은엑스트라트리스)`.
- feature_count/hash(피처 수/해시): `59` / `b33f55866d04baeeb33f11d660677d0ac9fd7870773e0e7e65f8692f1e8d7390`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.005296/1/both(양방향)/close_horizon(만기종가)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `1342.5/1.043101/7.476015/11.9191`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `1334.23/1.047846/9.659794/12.756`.
- reconstruction/parity(재구성/동등성): `True` / probability `True` / signal `True`.
- export_status(내보내기 상태): `exported_onnx_parity_passed`.

### pf_axis - `f68b_3481a04983ee`

- feature/model(피처/모델): `no_mega_top3(대형주_상위3제외)` / `extra_trees_shallow(얕은엑스트라트리스)`.
- feature_count/hash(피처 수/해시): `49` / `14a037f12cec16ad2f57a9cb5cafb5d61a374b96640872a6ac51bb6f28baf2a3`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.094374/0/long_only(롱만)/atr_sltp_conservative(보수적_ATR손익절)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `19.126866/99/1/0`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `38.232444/99/1/0`.
- reconstruction/parity(재구성/동등성): `True` / probability `True` / signal `True`.
- export_status(내보내기 상태): `exported_onnx_parity_passed`.

### low_dd_density_axis - `f68b_547ac8b4ead1`

- feature/model(피처/모델): `no_mega_top3(대형주_상위3제외)` / `hgb_small(작은히스토그램부스팅)`.
- feature_count/hash(피처 수/해시): `49` / `14a037f12cec16ad2f57a9cb5cafb5d61a374b96640872a6ac51bb6f28baf2a3`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.075295/1/both(양방향)/atr_sltp_conservative(보수적_ATR손익절)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `322.311858/1.015342/5.789668/8.842956`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `1536.005585/1.090589/7.226804/9.696686`.
- reconstruction/parity(재구성/동등성): `True` / probability `False` / signal `False`.
- export_status(내보내기 상태): `export_failed_preserved_clue`.

## Runtime Parity Boundary(런타임 동등성 경계)

- research_path(연구 경로): `stage_pipelines/stage_frontier_68/frontier68c_candidate_scoring_or_onnx_scout_export.py`.
- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`.
- shared_contract(공유 계약): feature order hash(피처 순서 해시), ONNX probability output(ONNX 확률 출력), threshold_margin decision mode(임계값/마진 의사결정), max hold/cooldown/ATR SLTP(최대 보유/대기봉/ATR 손익절).
- known_differences(알려진 차이): proxy DD%(프록시 손실폭 %)는 account DD(계좌 손실폭)가 아니며, proxy exit mapping(프록시 청산 매핑)은 MT5 Strategy Tester(전략 테스터)에서 검증해야 한다.
- parity_check(동등성 점검): ONNX probability parity(ONNX 확률 동등성)와 threshold signal parity(임계값 신호 동등성)를 로컬에서 실행했다. MT5 Runtime Probe(MT5 런타임 탐침)는 아직 대기다.
- handoff_intent(인계 의도): `stages/stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout/03_reviews/f68c_handoff_intent_review.json`.

## Next Action(다음 행동)

- `frontier68D_mt5_runtime_probe_candidate_axis_materialization_v1`: exported axes(내보낸 축)를 MT5 Runtime Probe(MT5 런타임 탐침)로 물질화하고 proxy/runtime KPI gap(프록시/런타임 핵심 성과 지표 간극)을 기록한다.

Claim boundary(주장 경계): `onnx_scout_export_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

# F68B Runtime Lifecycle Proxy Broad Sweep(F68B 런타임 생명주기 프록시 넓은 탐색)

Updated(갱신): 2026-06-16T16:50:49Z

## Action And Effect(행동 및 효과)

Action(행동): raw US100 M5 bars(원천 US100 5분봉)에서 forward path(전방 경로), MFE/MAE(최대 유리/불리 이동), cost proxy(비용 프록시), ATR first-hit(평균진폭 선타격)을 계산하고, feature set/label/model/trade shape/risk(피처 묶음/라벨/모델/거래 형태/위험) 조합을 넓게 시험했다.

Effect(효과): F68이 alignment-only(정렬 전용) 단계로 좁아지지 않고, 실제 nonzero proxy signal(영이 아닌 프록시 신호)과 four-axis distance(네 축 목표까지 거리)를 가진 scout surface(탐색 표면)를 얻었다.

## Measurement Scope(측정 범위)

- input rows(입력 행): `46650`.
- label variants(라벨 변형): `7`.
- candidate summaries(후보 요약): `30240`.
- meaningful PF/density signal candidates(의미 있는 수익 팩터/밀도 신호 후보): `293`.
- density-band dual-positive clues(밀도대역 양쪽 양수 단서): `24`.
- density-band strict PF clues(밀도대역 엄격 수익 팩터 단서): `0`.
- density-band plus proxy DD under 10 clues(밀도대역 및 프록시 손실폭 10 미만 단서): `2`.
- PF clue with density gap candidates(밀도 간극이 있는 수익 팩터 단서 후보): `293`.
- proxy joint pass count(프록시 네 축 동시 통과 수): `0`.
- scoreboard(점수판): structural_scout(구조 탐색) and proxy trading read(프록시 거래 판독).
- parity level(동등성 수준): P1_dataset_feature_aligned(P1 데이터셋/피처 정렬); MT5 runtime parity(MT5 런타임 동등성)는 아직 아님.

## Best Density-Aware Proxy Clue(최선 밀도 고려 프록시 단서)

- candidate_id(후보 ID): `f68b_23f4d4607a78`.
- target(목표): `h2_ddp03_min1p5(2봉_손실벌점)`.
- feature/model(피처/모델): `full58(전체58)` / `extra_trees_shallow(얕은엑스트라트리스)`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.3/1/both(양방향)/close_horizon(만기종가)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭%): `1342.5/1.043101/7.476015/11.9191`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `1334.23/1.047846/9.659794/12.756`.
- min PF/max proxy DD%(최소 수익 팩터/최대 프록시 손실폭%): `1.043101/12.756`.
- read(판독): `scout_clue_density_band_pf_weak(밀도대역_PF약함_탐색단서)`.

## Best Density Clue(최선 밀도 단서)

- candidate_id(후보 ID): `f68b_23f4d4607a78`.
- target(목표): `h2_ddp03_min1p5(2봉_손실벌점)`.
- feature/model(피처/모델): `full58(전체58)` / `extra_trees_shallow(얕은엑스트라트리스)`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.3/1/both(양방향)/close_horizon(만기종가)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭%): `1342.5/1.043101/7.476015/11.9191`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `1334.23/1.047846/9.659794/12.756`.
- min PF/max proxy DD%(최소 수익 팩터/최대 프록시 손실폭%): `1.043101/12.756`.
- read(판독): `scout_clue_density_band_pf_weak(밀도대역_PF약함_탐색단서)`.

## Best Low-DD Density Clue(최선 저손실폭 밀도 단서)

- candidate_id(후보 ID): `f68b_547ac8b4ead1`.
- target(목표): `h2_ddp03_min1p5(2봉_손실벌점)`.
- feature/model(피처/모델): `no_mega_top3(대형주_상위3제외)` / `hgb_small(작은히스토그램부스팅)`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.7/1/both(양방향)/atr_sltp_conservative(보수적_ATR손익절)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭%): `322.311858/1.015342/5.789668/8.842956`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `1536.005585/1.090589/7.226804/9.696686`.
- min PF/max proxy DD%(최소 수익 팩터/최대 프록시 손실폭%): `1.015342/9.696686`.
- read(판독): `scout_clue_density_band_pf_weak(밀도대역_PF약함_탐색단서)`.

## Best PF Clue With Density Gap(최선 수익 팩터 단서와 밀도 간극)

- candidate_id(후보 ID): `f68b_3481a04983ee`.
- target(목표): `h6_ddp04_min3(6봉_손실벌점)`.
- feature/model(피처/모델): `no_mega_top3(대형주_상위3제외)` / `extra_trees_shallow(얕은엑스트라트리스)`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.975/0/long_only(롱만)/atr_sltp_conservative(보수적_ATR손익절)`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭%): `19.126866/99/1/0`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭%): `38.232444/99/1/0`.
- min PF/max proxy DD%(최소 수익 팩터/최대 프록시 손실폭%): `99/0`.
- read(판독): `meaningful_proxy_signal_pf_clue_density_gap(의미있는_프록시신호_PF단서_밀도간극)`.

## Gap Read(간극 판독)

- Four-axis proxy completion candidate(네 축 프록시 완성 후보): `none(없음)`.
- Plain meaning(쉬운 뜻): density clues(밀도 단서)는 거래 수가 맞지만 PF(수익 팩터)가 약하고, PF clues(수익 팩터 단서)는 거래 수가 너무 적다.
- Effect(효과): F68C는 한 후보만 밀지 말고 density repair(밀도 수리)와 PF repair(수익 팩터 수리)를 같이 비교해야 한다.

## Boundary(경계)

- This is proxy-only(프록시 전용) evidence(근거)다. MT5 Runtime Probe(MT5 런타임 탐침), Strategy Tester(전략 테스터), ONNX handoff(ONNX 인계)는 아직 실행하지 않았다.
- Proxy DD%(프록시 손실폭 %)는 10000 proxy points(프록시 포인트) 기준 정규화 수치이며 account DD(계좌 손실폭) 권위가 아니다.
- Next action(다음 행동): pre-MT5 Grok review(그록 사전 검토) 전 후보를 줄이고, 필요하면 ONNX scout export(ONNX 탐색 내보내기)를 준비한다.

Claim boundary(주장 경계): `proxy_broad_sweep_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

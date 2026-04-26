# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `10_alpha_scout__default_split_model_threshold_scan`
- status(상태): `reviewed_closed_handoff_to_stage11_ready`
- lane(레인): `exploration(탐색)`
- scout boundary(탐색 판독 경계): `single_split_scout(단일 분할 탐색 판독)`
- current run packet(현재 실행 묶음): `run01Y_run01AC_logreg_a_base_no_fallback_200_220_hold_threshold_closeout_v1`
- current operating reference(현재 운영 기준): `none`

## 인계 조건(Handoff Condition, 인계 조건)

Stage 09(9단계)이 `stage09_pre_alpha_handoff_packet_v1` 묶음(packet, 묶음)으로 registry/current truth/publish boundary(등록부/현재 진실/게시 경계)를 닫고 Stage 10(10단계)로 인계했으므로 시작했다.

효과(effect, 효과): Stage 10(10단계)은 default split(기본 분할) 위에서 model/threshold scout(모델/임계값 탐색 판독)를 실행할 수 있다.

## 선택된 입력(Selected Inputs, 선택 입력)

- Stage 09 handoff packet(Stage 09 인계 묶음): `stages/09_pre_alpha_handoff__registry_publish_packet/03_reviews/pre_alpha_handoff_packet.md`
- Stage 08 protocol(Stage 08 규칙): `docs/policies/alpha_entry_protocol.md`
- Stage 08 report template(Stage 08 보고 틀): `docs/templates/alpha_exploration_report_template.md`
- selected model input(선택 모델 입력): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- default split(기본 분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`

## 현재 실행 묶음(Current Run Packet, 현재 실행 묶음)

- run packet(실행 묶음): `run01Y_run01AC_logreg_a_base_no_fallback_200_220_hold_threshold_closeout_v1`
- included runs(포함 실행): `run01Y hold9 base(9봉 기준)`, `run01Z hold6(6봉)`, `run01AA hold12(12봉)`, `run01AB margin0.025(마진 0.025)`, `run01AC strict probability(엄격 확률)`
- external verification status(외부 검증 상태): `completed(완료)`
- judgment(판정): `inconclusive_single_split_scout_mt5_closeout_completed`
- routing mode(라우팅 방식): `tier_a_primary_no_fallback`
- routed fallback enabled(라우팅 대체 사용): `false`
- evidence(근거): Python(파이썬) threshold sweep(임계값 스윕), ONNX(`Open Neural Network Exchange`, 온닉스) probability parity(확률 동등성), MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) Tier A-only routed total(Tier A 단독 라우팅 전체)과 Tier B fallback-only(Tier B 대체 구간 단독) 비교

기준 Tier A rule(기준 Tier A 규칙)은 `short0.600_long0.450_margin0.000`, 기준 max hold(최대 보유)는 `9`봉이고, session slice(시간대 조각)는 `200 < x <= 220`이다. 이 기준을 hold(보유) 6/12와 stricter threshold(더 엄격한 임계값)로 흔들었다.

| run(실행) | slice/routing(구간/라우팅) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | OOS DD/recovery(표본외 손실/회복) |
|---:|---:|---:|---:|---:|
| run01Y(실행 01Y) | hold9(9봉), base(기준), `200 < x <= 220` | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| run01Z(실행 01Z) | hold6(6봉), base(기준), `200 < x <= 220` | `264.14 / 2.99` | `109.65 / 1.66` | `161.79 / 0.68` |
| run01AA(실행 01AA) | hold12(12봉), base(기준), `200 < x <= 220` | `447.76 / 4.55` | `225.69 / 2.57` | `170.11 / 1.33` |
| run01AB(실행 01AB) | hold9(9봉), margin0.025(마진 0.025), `200 < x <= 220` | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| run01AC(실행 01AC) | hold9(9봉), strict probability(엄격 확률), `200 < x <= 220` | `143.91 / 2.30` | `219.09 / 5.53` | `147.09 / 1.49` |

효과(effect, 효과)는 run01Y(실행 01Y)가 현재 가장 균형 좋은 late-mid window(중반 뒤쪽 구간)라는 점을 마감 확인한 것이다. hold6(6봉 보유)은 약했고, hold12(12봉 보유)는 validation(검증) 쪽으로 치우쳤고, margin0.025(마진 0.025)는 결과를 바꾸지 못했고, strict probability(엄격 확률)는 OOS PF(표본외 수익 팩터)는 높지만 net/recovery(순수익/회복)가 낮다. Stage 10(10단계)은 이 상태로 닫고 Stage 11(11단계) `11_alpha_robustness__wfo_label_horizon_sensitivity`로 넘긴다.

## 경계(Boundary, 경계)

이 문서는 Stage 10(10단계)의 200~220 closeout runtime_probe(마감 런타임 탐침)가 완료되고 Stage 11(11단계)로 인계됐다는 뜻이다. 아직 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority expansion(런타임 권위 확장)을 뜻하지 않는다.

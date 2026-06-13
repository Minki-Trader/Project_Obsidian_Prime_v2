You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier08 stage-open(전선08 단계 개방) proposal.

Current truth(현재 진실):
- Frontier06(전선06) preserved clue(보존 단서): selective probability abstention(선택적 확률 기권) improved OOS density/PF/DD(표본밖 밀도/수익 팩터/손실폭) to about `5.31/day`, `1.267`, `21.11%`, but strict scout clue rows(엄격 탐색 단서 행) stayed `0`.
- Frontier07(전선07) preserved clue(보존 단서): adverse-excursion risk labels(불리 이동 위험 라벨) reduced OOS DD(drawdown, 손실폭) toward `13.09%`, and class-prior bridge(클래스 사전분포 브리지) recovered OOS density(표본밖 밀도) near `4.12/day`.
- Frontier07 negative memory(부정 기억): validation DD(검증 손실폭) remained very high, PF(profit factor, 수익 팩터) stayed weak, and simultaneous density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움) strict rows remained `0`.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

Codex proposed direction before Grok(Codex가 Grok 전 제안한 방향):
- Open Frontier08(전선08) as `stage_frontier_08__sample_weighted_objective`.
- Hypothesis(가설): The previous stages may be failing because the model objective treats all train rows too similarly. A multi-objective sample-weighting objective(다중목적 표본 가중 목적) can train the same ONNX-exportable 3-class interface(온엑스 내보내기 가능 3분류 인터페이스) to care more about rows where correct direction has favorable excursion and bounded adverse excursion(유리 이동과 제한된 불리 이동), and care less about ambiguous rows that create DD-heavy trades(손실폭 큰 거래). This changes train loss geometry(학습 손실 구조), not runtime threshold(런타임 임계값) and not another label-threshold grid(라벨 임계값 격자).
- Novelty delta(신규성 차이): Frontier07 changed labels and global class priors(라벨과 전역 클래스 사전분포). Frontier08 changes per-row training weights(행별 학습 가중치) derived only from train-side target/path utility(학습 구간 목표/경로 효용) while keeping `feature_set_v2` and the `[p_short, p_flat, p_long]` ONNX output contract(온엑스 출력 계약) fixed.
- First scout(첫 탐색): Frontier08B(전선08B) compares unweighted controls(무가중 대조군) versus broad sample-weight families(넓은 표본 가중군) on identical rows/splits/model specs(동일 행/분할/모델 설정). It records label_v1(라벨 v1) and one risk-shaped preserved label reference(위험 라벨 보존 참조) as reference surfaces only, not inherited winners.
- Broad sweep(넓은 탐색): utility emphasis(효용 강조), adverse-excursion downweighting(불리 이동 하향 가중), flat-ambiguity shaping(평탄/애매함 형성), side-balance with path quality(방향 균형+경로 품질).
- Success for scout clue(탐색 단서 성공): weighted model(가중 모델) must improve the matching unweighted control(같은 무가중 대조군) on validation and OOS(검증과 표본밖) four-axis distance(네 축 거리), with density near 5-10/day(일 5~10회 근처), PF lift(수익 팩터 상승), DD reduction(손실폭 감소), and ONNX parity(온엑스 동등성). This remains scout-only(탐색 전용).
- Stop condition(중지 조건): if sample weighting only moves density or DD alone, preserve clue(보존 단서) or close negative memory(부정 기억). Do not run WFO/MT5(WFO/MT5) without a strict scout clue(엄격 탐색 단서).

Bounded evidence(제한 근거):
- Frontier06B scout report(전선06B 탐색 보고서): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/03_reviews/frontier06B_selective_probability_abstention_signal_scout_v1_report.md` sha256 `573b460b0c1f02e054681c8b68e7e19a0fcb698aa4c1b1cb4123d98d16113e7d`
- Frontier06C closeout report(전선06C 마감 보고서): `stages/stage_frontier_06__selective_probability_abstention_signal_contract/03_reviews/frontier06C_stage_closeout_v1_report.md` sha256 `cac6627b2d8068093f6ce39dc7a843433d52b92e0d062a78ae53fdcc3ef74c93`
- Frontier07B scout report(전선07B 탐색 보고서): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/03_reviews/frontier07B_adverse_excursion_risk_label_proxy_scout_v1_report.md` sha256 `6010f1f8262310d169bf69bf81b6dc75c8396788f89f91c698dff09a005736ad`
- Frontier07C repair report(전선07C 수리 보고서): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/03_reviews/frontier07C_class_prior_density_bridge_repair_v1_report.md` sha256 `f79659aa22eb0402d05ec57db07e9c54f38172491eb97f1b310a7b79a57cbf58`
- Frontier07D closeout report(전선07D 마감 보고서): `stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/03_reviews/frontier07D_stage_closeout_decision_v1_report.md` sha256 `d9fab0a862ded8cabada189578e915daabed2a4b46365b6a9a868e0de55fa03e`
- Model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- Feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt` sha256 `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`

Focused question(집중 질문):
Should Codex(Codex, 코덱스) open Frontier08(전선08) with multi-objective sample weighting(다중목적 표본 가중), revise the direction(방향 수정), or choose a different hypothesis(다른 가설)?

Please answer in this structure:
1. Recommendation(권고): open_frontier08(전선08 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier08B(전선08B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)

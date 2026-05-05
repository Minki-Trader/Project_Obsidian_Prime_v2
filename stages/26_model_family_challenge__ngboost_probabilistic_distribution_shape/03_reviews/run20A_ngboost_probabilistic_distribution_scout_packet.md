# RUN20A NGBoost Probabilistic Distribution Scout Packet(20A 실행 NGBoost 확률분포 탐색 묶음)

## Judgment(판정)

- run(실행): `run20A_ngboost_probabilistic_distribution_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_ngboost_probabilistic_distribution_scout_completed`
- selected variant(선택 변형): `v02_core42_distribution_surface`
- best overall variant(전체 최고 변형): `v02_core42_distribution_surface`
- NGBoost version(NGBoost 버전): `0.5.10`
- boundary(경계): `ngboost_probabilistic_distribution_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run20A_next_milestone_run20B_ngboost_distribution_runtime_probe_v1`

효과(effect, 효과): Stage26(26단계)는 NGBoost(자연 그래디언트 부스팅)의 probability distribution(확률분포), entropy(엔트로피), abstention clue(기권 단서)를 Python-side evidence(파이썬 근거)로 확인했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- variants(변형): `5`
- selected Tier A validation balanced accuracy(선택 Tier A 검증 균형 정확도): `0.42906559409142936`
- selected Tier A OOS balanced accuracy(선택 Tier A 표본외 균형 정확도): `0.4521957020157636`
- selected Tier A validation log loss(선택 Tier A 검증 로그 손실): `1.0490011746718895`
- selected Tier A OOS log loss(선택 Tier A 표본외 로그 손실): `1.049595190530285`
- validation entropy mean(검증 엔트로피 평균): `0.9745848382741663`
- OOS entropy mean(표본외 엔트로피 평균): `0.9754424721932006`
- validation high entropy rate(검증 고엔트로피 비율): `0.9791751320601382`
- OOS high entropy rate(표본외 고엔트로피 비율): `0.9922204641350211`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `stages/26_model_family_challenge__ngboost_probabilistic_distribution_shape/02_runs/run20A_ngboost_probabilistic_distribution_scout_v1/predictions/tier_a_ngboost_predictions.parquet`
- Tier B separate(Tier B 분리): `stages/26_model_family_challenge__ngboost_probabilistic_distribution_shape/02_runs/run20A_ngboost_probabilistic_distribution_scout_v1/predictions/tier_b_ngboost_predictions.parquet`
- Tier A+B combined(Tier A+B 합산): `stages/26_model_family_challenge__ngboost_probabilistic_distribution_shape/02_runs/run20A_ngboost_probabilistic_distribution_scout_v1/predictions/tier_ab_ngboost_predictions.parquet`

효과(effect, 효과): Tier A(티어 A)만 본 결과를 전체 read(판독)로 과장하지 않고, Tier B fallback(Tier B 대체)에서도 같은 probability shape(확률 모양)가 유지되는지 다음 runtime_probe(런타임 탐침)로 넘긴다.

## Preserved Clues(보존 단서)

- NGBoost(자연 그래디언트 부스팅)는 class probability(분류 확률)뿐 아니라 entropy(엔트로피)와 margin(마진)으로 permission/abstention(허용/기권) 축을 읽을 수 있다.
- selected feature read(선택 피처 판독) top features(상위 피처): `['hl_range', 'historical_vol_20', 'ema50_ema200_diff', 'overnight_return', 'sma50_sma200_ratio']`
- model handoff(모델 인계)는 joblib bundle(잡립 묶음)만 만들었고 ONNX/runtime authority(ONNX/런타임 권위)는 만들지 않았다.

## Negative Memory(부정 기억)

- run20A(20A 실행)는 Python structural scout(파이썬 구조 탐색)라서 MT5 runtime behavior(MT5 런타임 행동)를 아직 증명하지 않는다.
- entropy threshold(엔트로피 임계값)은 운영 규칙이 아니라 runtime_probe(런타임 탐침)에서 관찰할 단서다.
- selected variant(선택 변형)는 promotion candidate(승격 후보)가 아니라 Stage26(26단계) MT5 probe(MT5 탐침)에 넘길 handoff candidate(인계 후보)다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run20B_ngboost_distribution_runtime_probe_v1` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) with small tranche/sentinel check(작은 묶음/감시 실행 확인).

# RUN17A Supervised Regime Classifier Scout Packet(실행17A 지도 국면 분류기 탐색 묶음)

## Judgment(판정)

- run(실행): `run17A_supervised_regime_classifier_filter_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_supervised_regime_classifier_filter_scout_completed`
- selected variant(선택 변형): `v05_logistic_core24_compact_filter`
- boundary(경계): `supervised_regime_classifier_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run17A_next_milestone_run17B_supervised_regime_classifier_runtime_probe_v1(실행17A에서는 미시도, 다음 마일스톤은 run17B_supervised_regime_classifier_runtime_probe_v1)`

효과(effect, 효과): supervised classifier(지도 분류기)를 direct entry model(직접 진입 모델)이 아니라 p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 regime filter(국면 필터)로 탐색했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `5`
- selected model type(선택 모델 유형): `logistic`
- threshold quantile(임계 분위수): `q0.80`
- Tier A rows(Tier A 행): `46650`
- Tier B fallback rows(Tier B 대체 행): `12398`
- validation balanced accuracy(검증 균형 정확도): `0.4363653298038846`
- OOS balanced accuracy(표본외 균형 정확도): `0.4657215893592583`
- validation signal coverage(검증 신호 비중): `0.20002031694433156`
- OOS signal coverage(표본외 신호 비중): `0.19804852320675106`

## Preserved Clues(보존 단서)

- p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 filter interpretation(필터 해석)을 보존한다.
- Tier A/B(티어 A/B) 모두 같은 selected variant(선택 변형)로 재학습해 partial-context fallback(부분 문맥 대체)의 probability shape(확률 모양)을 비교할 수 있다.
- 다음 MT5 runtime_probe(MT5 런타임 탐침)는 selected variant(선택 변형)를 ONNX(온닉스) 또는 table handoff(테이블 인계)로 좁게 검증한다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run17B_supervised_regime_classifier_runtime_probe_v1` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).

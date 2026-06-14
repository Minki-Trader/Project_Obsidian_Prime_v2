# Negative Memory(부정 기억)

F45 negative memory(부정 기억)는 train-only short event-utility classifier(학습 전용 숏 이벤트 효용 분류기)가 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): 0
- seed_surface_count(씨앗 표면 수): 0
- runtime_probe_candidate_count(런타임 탐침 후보 수): 0
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f45_event_classifier_proxy`
- do_not_repeat(반복 금지): F44 continuous regression(연속 회귀), F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천), F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움)를 primary lever(주 레버)로 반복하지 않는다.

# Negative Memory(부정 기억)

F44 negative memory(부정 기억)는 train-only short path-utility label model(학습 전용 숏 경로 효용 라벨 모델)이 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): 26
- seed_surface_count(씨앗 표면 수): 0
- runtime_probe_candidate_count(런타임 탐침 후보 수): 0
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f44_label_model_proxy`
- do_not_repeat(반복 금지): F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움), F43 trade-shape source(거래 형태 원천)를 primary lever(주 레버)로 반복하지 않는다.

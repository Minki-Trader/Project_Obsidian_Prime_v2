# Frontier19 Model Backbone Lock Spec(전선19 모델 백본 잠금 명세)

Action(행동): Frontier19B(전선19B) 전에 model variants(모델 변형)와 execution surface(실행 표면)를 고정합니다.

Effect(효과): validation/OOS(검증/표본외) 결과를 본 뒤 threshold(임계값), lifecycle(생명주기), quota(쿼터), stability selector(안정성 선택기)를 추가하는 invalid setup(무효 설정)을 막습니다.

## Variants(변형)

- `f19b_xgb_depth2_l2_backbone_control`: xgboost(XGBoost, 엑스지부스트); basis(기반) `v01_depth2_l2_subsample`; role(역할) shallow_regularized_backbone_control(얕은 정규화 백본 대조군)
- `f19b_xgb_depth3_balanced_l2_backbone`: xgboost(XGBoost, 엑스지부스트); basis(기반) `v02_depth3_balanced_l2`; role(역할) balanced_depth_regularized_backbone(균형 깊이 정규화 백본)
- `f19b_cat_ordered_depth3_backbone`: catboost(CatBoost, 캣부스트); basis(기반) `v01_ordered_depth3_bayesian`; role(역할) ordered_boosting_backbone(순서 부스팅 백본)
- `f19b_cat_plain_depth3_backbone_control`: catboost(CatBoost, 캣부스트); basis(기반) `v05_plain_depth3_control`; role(역할) plain_boosting_backbone_control(일반 부스팅 백본 대조군)

## Execution Surface(실행 표면)

- decision_policy: `argmax_nonflat_control(최대확률 비중립 대조)`
- threshold_policy: `no_validation_oos_threshold_search(검증/표본외 임계값 탐색 없음)`
- exit_policy: `fixed_fwd12_proxy_then_single_runtime_surface_if_handoff_exists(프록시는 고정 fwd12, 인계 후보가 있으면 단일 런타임 표면)`
- density_policy: `observe_density_no_daily_quota_repair(빈도 관찰, 일일 쿼터 수리 없음)`
- stability_policy: `audit_and_tie_break_only(감사와 동률 처리 전용)`

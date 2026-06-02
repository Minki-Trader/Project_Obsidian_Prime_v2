# Stage364 Selection Status(364단계 선택 상태)

- latest_completed_run(최근 완료 실행): `run364I_design_dense_m5_runtime_repair_proxy_without_db_v1`
- current_run(현재 실행): `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`
- selected_model(선정 모델): `none(없음)`
- dense_m5_proxy(고밀도 M5 프록시): `completed_mixed_no_authority(완료, 혼합, 권위 없음)`
- dense_rows(고밀도 행): `17428`
- sparse_expected_rows(희소 예상 행): `1114`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `0`
- best_oos_net(최선 표본외 순수익): `73.383`
- best_oos_pf(최선 표본외 수익 팩터): `1.0317882568`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): dense source(고밀도 원천)는 살리고, 약한 cost filter(비용 필터)는 운영 후보로 과장하지 않는다.

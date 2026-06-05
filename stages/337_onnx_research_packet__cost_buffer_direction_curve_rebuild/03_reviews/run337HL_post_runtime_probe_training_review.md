# Stage337 run337HL Post Runtime Probe Training Review(337단계 337HL 사후 런타임 학습 검토)

Action(행동): HK ONNX training(HK ONNX 학습) 결과를 검토했다. Effect(효과): ONNX parity(ONNX 동등성)는 `5/5`로 통과했지만 inner holdout proxy(내부 보류 프록시)가 전부 음수라 runtime package(런타임 패키지)를 열지 않았다.

- status(상태): `completed_stage337HL_post_runtime_probe_training_review_all_proxy_negative_no_runtime_package_no_selection`
- judgment(판정): `onnx_parity_passed_but_all_inner_holdout_proxy_negative_repair_design_required`
- decision(결정): `stage337HL_open_run337HM_proxy_negative_trade_shape_repair_design`
- best_model(최고 모델): `hk_hi_hh003_probability_precision_margin`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `-1.0452519969367131`
- positive_proxy_rows(긍정 프록시 행): `0`
- best_trade_count(최고 거래수): `14262`
- long_short(롱/숏): `7494/6768`
- gates(게이트): `11/11`
- next_action(다음 행동): `run337HM_design_post_runtime_probe_proxy_negative_trade_shape_repair_without_db_v1`

Boundary(경계): MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 모두 `not_claimed/not_run`이다.

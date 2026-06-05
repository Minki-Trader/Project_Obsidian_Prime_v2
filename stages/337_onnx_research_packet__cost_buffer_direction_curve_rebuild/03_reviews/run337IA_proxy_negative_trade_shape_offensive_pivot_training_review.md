﻿# Stage 337IA Offensive Pivot Training Review

## Summary

- run_id: `run337IA_review_proxy_negative_trade_shape_offensive_pivot_training_without_db_v1`
- parent_run_id: `run337HZ_train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db_v1`
- judgment: `two_proxy_positive_onnx_candidates_found_short_dominant_side_risk_runtime_probe_required`
- gates: `8/8`
- positive_proxy_rows(양수 프록시 행): `2`
- best_model_id(최고 프록시 모델 ID): `hz_hx_hw003_model_family_extratrees_fwd18`
- best_proxy_net(최고 프록시 순수익): `1.3964926912813098`
- best_profit_factor(최고 수익 팩터): `1.06249812575836`
- best_side_balance_ratio(최고 후보 방향 균형 비율): `0.153713298791019`

## Result

IA review(검토)는 proxy-positive(프록시 양수) ONNX(온엑스) 후보 2개를 찾았다.
Effect(효과): 후보 선택(selection, 선택)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 패키지로 넘긴다.

## Risk

Best proxy(최고 프록시)는 short-dominant(숏 우세)이고 side net warning(방향 순익 경고)이 있다.
Effect(효과): MT5 probe(탐침)는 net profit(순수익)뿐 아니라 long/short balance(롱/숏 균형)를 같이 확인해야 한다.

## Boundary

No candidate selection(후보 선택 없음), no MT5 execution in IA(IA에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `run337IB_materialize_proxy_positive_offensive_pivot_runtime_probe_package_without_db_v1` to materialize(물질화) runtime probe package(런타임 탐침 패키지) and attempt(시도) external MT5 comparison(외부 MT5 비교).

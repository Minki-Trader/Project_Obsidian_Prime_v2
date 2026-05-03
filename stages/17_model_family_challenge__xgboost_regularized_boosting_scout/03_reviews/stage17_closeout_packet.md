# Stage17 Closeout v3(17단계 마감 v3)

- closeout run(마감 실행): `run11G_xgb_dart_attribution_closeout_v1`
- judgment(판정): `closed_inconclusive_xgboost_dart_attribution_no_new_axis_after_run11G`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- recommendation(권고): `close_stage17_after_dart_attribution_no_new_axis`

## Preserved Clues(보존 단서)

- run11A: q0.90 gbtree(기본 트리 부스팅) 특성이 보였다.
- run11B: q0.80에서 거래 빈도는 늘었다.
- run11C/run11D: 롱 신호와 롱 거래 편향이 반복됐다.
- run11E: gbtree 피처 동인은 포화됐다.
- run11F/run11G: DART(`Dropouts meet Multiple Additive Regression Trees`, 드롭아웃 부스팅)는 `close_ema20_ratio`를 top3(상위 3개)에 올렸지만, 추가 귀속 축은 만들지 않았다.

효과(effect, 효과): Stage17(17단계)을 모델 특성 기억으로 닫고 Stage18(18단계)로 넘어갈 수 있다. 이 마감은 baseline(기준선)이나 promotion(승격)이 아니다.

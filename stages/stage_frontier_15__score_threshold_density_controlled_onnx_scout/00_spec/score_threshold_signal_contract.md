# Frontier15 Score Threshold Signal Contract(프론티어15 점수 임계값 신호 계약)

Action(행동): ONNX probability tensor(온엑스 확률 텐서)의 short/flat/long(숏/플랫/롱) 확률을 3개 score contract(점수 계약)로 바꾼 뒤, train-only threshold(학습 전용 임계값)로 거래 빈도를 맞춥니다.

Effect(효과): validation/OOS(검증/표본밖) 성과를 보고 threshold(임계값)를 고르지 않고, density transfer(빈도 전이)가 되는지만 확인합니다.

## Frozen Grid(고정 격자)

- `edge_margin__target5`: `max(p_short, p_long) - p_flat`, target density(목표 빈도) `5/day`, primary(1순위) `False`
- `edge_margin__target8`: `max(p_short, p_long) - p_flat`, target density(목표 빈도) `8/day`, primary(1순위) `True`
- `edge_margin__target10`: `max(p_short, p_long) - p_flat`, target density(목표 빈도) `10/day`, primary(1순위) `False`
- `side_gap__target5`: `abs(p_long - p_short)`, target density(목표 빈도) `5/day`, primary(1순위) `False`
- `side_gap__target8`: `abs(p_long - p_short)`, target density(목표 빈도) `8/day`, primary(1순위) `False`
- `side_gap__target10`: `abs(p_long - p_short)`, target density(목표 빈도) `10/day`, primary(1순위) `False`
- `utility_tilt__target5`: `max(p_short, p_long) - 0.5 * p_flat`, target density(목표 빈도) `5/day`, primary(1순위) `False`
- `utility_tilt__target8`: `max(p_short, p_long) - 0.5 * p_flat`, target density(목표 빈도) `8/day`, primary(1순위) `False`
- `utility_tilt__target10`: `max(p_short, p_long) - 0.5 * p_flat`, target density(목표 빈도) `10/day`, primary(1순위) `False`

## Required Baseline(필수 기준행)

F14-matched argmax baseline row(F14 대응 최대확률 기준행)를 every variant/model/split(모든 변형/모델/분할)에 기록합니다. Effect(효과): score threshold(점수 임계값)이 실제로 density cliff(빈도 절벽)를 고쳤는지 비교합니다.

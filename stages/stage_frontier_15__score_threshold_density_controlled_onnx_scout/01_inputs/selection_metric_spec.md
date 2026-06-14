# Frontier15 Selection Metric Spec(프론티어15 선택 지표 명세)

- strict scout clue(엄격 탐색 단서): primary cell(1순위 칸) `edge_margin__target8`가 validation/OOS(검증/표본밖) 양쪽에서 PF/density/DD/subperiod/parity(수익 팩터/빈도/손실폭/하위기간/동등성) 조건을 통과해야 합니다.
- preserved clue(보존 단서): non-primary cell(비 1순위 칸) 또는 일부 축만 좋은 row(행)는 다음 단계 전진 트리거가 아니라 clue(단서)로만 보존합니다.
- negative memory(부정 기억): train threshold(학습 임계값)가 validation/OOS(검증/표본밖) 빈도로 전이되지 않거나 PF/DD(수익 팩터/손실폭)가 무너지면 기록합니다.

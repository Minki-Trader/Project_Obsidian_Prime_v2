# Frontier19 Selection Metric Spec(전선19 선택 지표 명세)

- scout clue(탐색 단서): validation/OOS(검증/표본외) PF, density, DD, smoothness(PF/빈도/손실폭/매끄러움)가 동시에 목표 방향으로 움직여야 합니다.
- seed surface(씨앗 표면): 한 축 개선이 다른 세 축을 심하게 깨지 않아야 합니다.
- tie-break(동률 처리): train-only subperiod stability audit(학습 전용 하위기간 안정성 감사)는 동률 처리만 가능하며, 1차 선택기로 쓰지 않습니다.
- runtime probe observation(런타임 탐침 관찰): 인계 후보가 있으면 MT5 runtime probe(MT5 런타임 탐침)를 시도하고, 없으면 exact blocker(정확한 차단 사유)를 남깁니다.

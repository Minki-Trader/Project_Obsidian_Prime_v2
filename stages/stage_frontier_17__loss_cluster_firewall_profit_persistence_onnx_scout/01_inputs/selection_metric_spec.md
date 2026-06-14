# Frontier17 Selection Metric Spec(전선17 선택 지표 명세)

- scout clue(탐색 단서): validation/OOS(검증/표본밖) 양쪽에서 PF, DD, density, subperiod DD, ONNX parity(수익 팩터, 손실폭, 빈도, 하위기간 손실폭, ONNX 동등성)를 동시에 봅니다.
- seed surface(씨앗 표면): F16B/D(전선16B/D)보다 DD/smoothness(손실폭/매끄러움)가 명확히 좋아지고 density(빈도)가 일 3~10회에 머물 때만 기록합니다.
- negative memory(부정 기억): density(빈도)만 맞거나 firewall(방화벽)이 거래를 굶기면 같은 단계 안에서 반복 수리하지 않고 닫습니다.
- runtime probe observation(런타임 탐침 관찰): closeout(마감) 전 best-or-seed candidate(최선 또는 씨앗 후보) 1개에 MT5 runtime probe(MT5 런타임 탐침)를 시도하거나 정확한 blocked reason(차단 사유)을 기록합니다.

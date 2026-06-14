# Frontier21 Prior Stage Scan(전선21 이전 단계 점검)

F20 preserved clue(전선20 보존 단서): `vix_zscore_20 <= q30 & close_ema50_ratio >= q70` long(롱), validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `1.32666/8.57923/31.7443` and `1.22065/9.9084/20.7766`.

F20 negative memory(전선20 부정 기억): train-only depth-2 rule atlas(학습 전용 깊이2 규칙 지도) alone(단독)은 DD(손실폭)나 handoff(인계)를 해결하지 못했습니다.

F18 negative memory(전선18 부정 기억): lifecycle profile sweep(생명주기 프로필 훑기)은 단독 승격 근거가 아니며 low-DD shapes(낮은 손실폭 모양)만 참고 단서로 남겼습니다.

Reference boundary(참조 경계): Stage12~364(12~364단계)와 F18/F20(전선18/20)은 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.

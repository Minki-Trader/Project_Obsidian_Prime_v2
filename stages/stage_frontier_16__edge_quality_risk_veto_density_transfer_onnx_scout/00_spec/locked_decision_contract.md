# Locked Decision Contract(고정 결정 계약)

Action(행동): `max(p_short, p_long) - p_flat` 하나와 `edge_margin__target8` 하나만 Frontier16B(프론티어16B)에 씁니다.

Effect(효과): F15(프론티어15)의 9-cell grid(9칸 격자) 반복을 막고, validation/OOS(검증/표본밖)를 threshold selection(임계값 선택)에 쓰지 않습니다.

- score_contract_id(점수 계약 ID): `edge_margin`
- target_density_per_day(목표 일 거래 빈도): `8`
- threshold_policy(임계값 정책): train split probability scores and train calendar only(학습 분할 확률 점수와 학습 달력만 사용)
- forbidden(금지): no validation/OOS threshold calibration(검증/표본밖 임계값 보정 금지)

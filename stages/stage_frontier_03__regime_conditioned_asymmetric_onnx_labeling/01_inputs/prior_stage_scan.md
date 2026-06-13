# Prior Stage Scan(이전 단계 점검)

## Preserved Clue(보존 단서)

Frontier02C OOS density 5.03053/day with positive net, but no baseline/authority.

Effect(효과): density(밀도)가 목표권에 닿을 수 있다는 단서는 보존하지만, selected baseline(선택 기준선)이나 operating authority(운영 권위)로 가져오지 않습니다.

## Negative Memory(부정 기억)

Frontier02E go-rule rows 0; same-surface threshold/calibration repair should stop.

Effect(효과): Frontier03(전선03)은 같은 direct logistic ONNX(직접 로지스틱 온엑스) threshold/calibration repair(임계값/보정 수리)를 반복하지 않습니다.

## Archive Cross-References(보관 교차 참조)

- Stage41 directional asymmetric label horizon probe(Stage41 방향 비대칭 라벨 보유기간 탐침): `stage_pipelines/stage41/directional_asymmetric_label_horizon_probe.py`. Use(사용): label construction clue(라벨 구성 단서)만 참조합니다.
- Stage347 cash-open asymmetric source head design(Stage347 현금장 개방 비대칭 원천 헤드 설계): `stage_pipelines/stage347/design_cash_open_asymmetric_long_short_source_without_db.py`. Use(사용): broad source/head redesign(넓은 원천/헤드 재설계)로 Frontier03A(전선03A)를 키우지 않기 위한 경고로만 둡니다.
- Stage364 timestamp/context cost-filter model(Stage364 타임스탬프/문맥 비용 필터 모델): `stage_pipelines/stage364/train_timestamp_context_cost_filter_model_without_db.py`. Use(사용): evaluation-time/runtime boundary(평가 시점/런타임 경계)만 참조하고 label construction(라벨 구성)과 섞지 않습니다.
- Reusable helper(재사용 헬퍼): `foundation/labels/directional_asymmetric.py`. Use(사용): Frontier03B(전선03B)에서 stage-local duplicate logic(단계 로컬 중복 로직)을 만들기 전에 재사용 가능성을 확인합니다.

Effect(효과): reference, not inheritance(참조이지 상속 아님)를 적용하여 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 가져오지 않습니다.

## Do Not Repeat(반복 금지)

- 02C seed surface(02C 씨앗 표면)를 baseline(기준선)처럼 쓰지 않습니다.
- PF(수익 팩터)만 올리거나 density(밀도)만 맞추는 single-axis repair(단일 축 수리)를 다음 행동으로 삼지 않습니다.
- WFO/MT5(WFO/MT5)를 stage-open design(단계 개방 설계)에 끌어오지 않습니다.
- Tier B(티어 B)나 Tier A+B(Tier A+B 합산)를 만들지 못하면 `missing_required(필수 누락)` 또는 `out_of_scope_by_claim(주장 범위 밖)`로 기록합니다.

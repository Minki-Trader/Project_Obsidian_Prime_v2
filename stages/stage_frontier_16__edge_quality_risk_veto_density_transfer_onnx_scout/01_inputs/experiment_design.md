# Frontier16 Experiment Design(프론티어16 실험 설계)

- hypothesis(가설): F15(프론티어15)의 density transfer(빈도 전이)는 calibration clue(보정 단서)로만 쓰고, risk-quality path label(위험 품질 경로 라벨)이 PF/DD(수익 팩터/손실폭)를 개선하는지 본다.
- changed_variable(변경 변수): label meaning(라벨 의미)
- locked_decision_cell(고정 결정 칸): `edge_margin__target8`
- variant_cap(변형 상한): `3`
- success_criteria(성공 기준): validation/OOS(검증/표본밖) net positive(순수익 양수), PF >= 1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD <= 15%(손실폭 15% 이하), ONNX parity pass(온엑스 동등성 통과)
- failure_criteria(실패 기준): density(빈도)는 맞지만 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 깨지면 negative memory(부정 기억)로 닫습니다.
- invalid_conditions(무효 조건): validation/OOS threshold retune(검증/표본밖 임계값 재조정), score cell 추가(점수 칸 추가), post-hoc label knob(사후 라벨 파라미터) 추가

# Frontier14 Selection Metric Spec(프론티어14 선택 지표 규격)

- strict scout clue(엄격 탐색 단서): validation/OOS positive net(검증/표본밖 양수 순수익), PF>=1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD<=15%(손실폭 15% 이하), subperiod DD controlled(하위기간 손실폭 통제)
- preserved clue(보존 단서): OOS PF/DD(표본밖 수익 팩터/손실폭) useful but validation or density incomplete(검증 또는 빈도 불완전) with clear boundary(명확한 경계)
- negative memory(부정 기억): label quota hit(라벨 할당량 충족) does not transfer to model density/PF/DD(모델 빈도/수익 팩터/손실폭)

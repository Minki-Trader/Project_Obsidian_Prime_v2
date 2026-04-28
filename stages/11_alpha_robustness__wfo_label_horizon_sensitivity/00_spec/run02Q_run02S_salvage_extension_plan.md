# RUN02Q~RUN02S Salvage Extension Plan

## 질문(Question, 질문)

RUN02G/RUN02N/RUN02P(실행 02G/02N/02P)가 남긴 salvage value(회수 가치)를 같은 Stage 11(11단계) work packet(작업 묶음)에서 더 넓혀 validation/OOS(검증/표본외)가 동시에 버티는지 본다.

효과(effect, 효과): 작은 양수 판독을 바로 promotion_candidate(승격 후보)로 올리지 않고, 거래 수를 늘리거나 검증 손실을 줄일 수 있는 구조가 실제로 있는지 확인한다.

## 실행 설계(Run Design, 실행 설계)

| run(실행) | source read(원천 판독) | hypothesis(가설) | context gate(문맥 제한) | side(방향) |
|---|---|---|---|---|
| RUN02Q(실행 02Q) | RUN02P(실행 02P) | bear vortex short(하락 보텍스 숏) 양수 단서를 더 느슨한 density(밀도)로 키울 수 있는지 본다 | `vortex_negative` | short(숏) |
| RUN02R(실행 02R) | RUN02G(실행 02G) | long pullback(롱 되돌림) OOS(표본외) 강점을 deeper pullback plus ADX(더 깊은 되돌림+ADX)로 validation(검증)까지 복구할 수 있는지 본다 | `rsi14_lte42_bbpos_lte40_adx14_gte18` | long(롱) |
| RUN02S(실행 02S) | RUN02N(실행 02N) | squeeze breakout(압축 돌파)의 tiny OOS(작은 표본외) 단서를 wider low-bandwidth context(더 넓은 저대역폭 문맥)에서 키울 수 있는지 본다 | `bb_squeeze_or_bwidth_lte0030` | both(양방향) |

## 성공/실패 기준(Success/Failure Criteria, 성공/실패 기준)

- success(성공): validation/OOS(검증/표본외) routed total(라우팅 전체)이 둘 다 non-negative(비손실)이고 PF(`profit factor`, 수익 팩터)가 1 이상이다.
- weak salvage(약한 회수): 한쪽만 양수이거나 손실이 거의 본전이며 trade count(거래 수)가 작다.
- failure(실패): validation/OOS(검증/표본외) 중 하나가 명확한 손실이고 PF(수익 팩터)가 1 아래다.

효과(effect, 효과): 같은 단서를 무한 반복하지 않고, 어떤 축을 보존하고 어떤 축을 negative memory(부정 기억)로 넘길지 정한다.

## 경계(Boundary, 경계)

이 묶음은 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority expansion(런타임 권위 확장)을 주장하지 않는다.
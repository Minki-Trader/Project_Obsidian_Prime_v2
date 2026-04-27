# RUN02T~RUN02V Priority Probe Plan

## Priority 1

label/horizon sensitivity(라벨/예측수평선 민감도)를 `RUN02T`로 본다. 기존 `RUN02S` decision surface(결정 표면)를 fwd6/fwd12/fwd18 label(라벨)로 다시 맞춰 본다.

Effect(효과): 라벨 길이만 바꿔도 신호 정렬이 달라지는지 확인해서, 재학습(retraining, 재학습) 후보를 좁힌다.

## Priority 2

WFO-lite(가벼운 워크포워드 최적화)를 `RUN02U`로 본다. 기존 `RUN02S`를 분기별 window(구간)로 나누어 신호 밀도와 집중도를 본다.

Effect(효과): full WFO(전체 워크포워드 최적화)를 돌릴 만큼 구간별 표본이 있는지 먼저 판단한다.

## Priority 3

short-specific(숏 전용) 구조 판독을 `RUN02V`로 본다. `RUN02P` strict(엄격)와 `RUN02Q` density(밀도 확장)를 비교한다.

Effect(효과): 숏 성능 문제가 단순 신호 부족인지, 라벨/모델 분리 필요성인지 구분한다.

## Boundary

이 계획은 structural probe(구조 탐침)이다. MT5(메타트레이더5) runtime claim(런타임 주장)이나 promotion claim(승격 주장)을 만들지 않는다.

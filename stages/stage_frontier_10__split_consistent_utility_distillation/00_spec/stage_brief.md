# Frontier10 Stage Brief(전선10 단계 개요)

Stage id(단계 ID): `stage_frontier_10__split_consistent_utility_distillation`

Question(질문): Can split-consistent utility distillation(분할 일관 효용 증류) improve a fixed ONNX(고정 ONNX) 3-class trade/no-trade surface(3분류 거래/무거래 표면) without repeating label/weight/bridge repair(라벨/가중/브리지 수리 반복)?

Hypothesis(가설): A single fixed 3-class ONNX interface(고정 3분류 ONNX 인터페이스)가 train-only split-consistent utility distillation labels(학습 전용 분할 일관 효용 증류 라벨)을 배우면, 불안정하거나 DD-heavy(손실폭 큰) 행을 flat/no-trade(관망/무거래)로 보내고 밀도/PF/DD/매끄러움 네 축을 더 균형 있게 만들 수 있다.

Novelty delta(신규성 차이): Frontier07(전선07)은 adverse-risk label(불리 위험 라벨), Frontier08(전선08)은 sample weight(표본 가중), Frontier09(전선09)는 clean-path target representation(깨끗한 경로 목표 표현)을 바꿨다. Frontier10(전선10)은 model fit(모델 학습) 전에 train subwindow utility consensus(학습 하위구간 효용 합의)를 요구하는 supervision philosophy(감독 철학)를 바꾼다.

Difference from Stage295(295단계 대비 차이): Stage295(295단계)는 MT5 route-signal outcome distillation(MT5 경로 신호 결과 증류)과 actual routed total(실제 라우팅 전체) 후보화를 시험했고, Frontier10(전선10)은 Python Tier A train-only subwindow utility label(파이썬 Tier A 학습 전용 하위구간 효용 라벨)을 첫 scout(탐색)에서 ONNX argmax-only(ONNX 최대확률 전용)로 시험한다.

Do not repeat(반복 금지):
- Frontier09 clean-path density bridge repair(전선09 깨끗한 경로 밀도 브리지 수리) 반복 금지
- Frontier08 sample-weight-only repair(전선08 표본 가중 단독 수리) 반복 금지
- Stage295 MT5 route-signal outcome distillation(295단계 MT5 경로 신호 결과 증류) 상속 금지

Next run(다음 실행): `frontier10B_utility_distillation_proxy_scout_v1`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

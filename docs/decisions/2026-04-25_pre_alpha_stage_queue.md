# Decision Memo

## 결정(Decision, 결정)

model-backed alpha exploration(모델 근거 알파 탐색) 전 작업을 Stage 04~09(4~9단계)로 나눠서 대기열(queue, 대기열)로 고정한다.

## 이유(Why, 이유)

남은 작업은 서로 성격이 다르다.

- weights/data materialization(가중치/데이터 물질화)
- feature integrity audit(피처 무결성 감사)
- runtime parity(런타임 동등성)
- model training baseline(모델 학습 기준선)
- alpha protocol(알파 규칙)
- publish handoff(게시/인계)

이것을 한 단계에 넣으면 다음 작업 때 범위가 샌다.

## 효과(Effect, 효과)

- Stage 04(4단계)는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)와 58 feature(58개 피처) 재물질화를 소유한다.
- Stage 05(5단계)는 feature/time/external/label audit(피처/시간/외부/라벨 감사)를 소유한다.
- Stage 06(6단계)는 Python/MT5 parity(파이썬/MT5 동등성)와 full MT5 runtime authority(완전 MT5 런타임 권위)를 소유한다.
- Stage 07(7단계)는 preprocessing/model training smoke(전처리/모델 학습 스모크 실행)를 소유한다.
- Stage 08(8단계)는 alpha search protocol(알파 탐색 규칙)과 Tier A/B(티어 A/B) 보고 규칙을 소유한다.
- Stage 09(9단계)는 registry/publish handoff(등록부/게시 인계)를 소유한다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 planning scaffold(계획 골격)다.

아직 Stage 05~09(5~9단계)의 실행 근거(run evidence, 실행 근거), model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.

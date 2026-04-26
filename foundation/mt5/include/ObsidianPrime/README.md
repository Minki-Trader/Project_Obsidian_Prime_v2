# ObsidianPrime MT5 Module Map(ObsidianPrime MT5 모듈 지도)

이 폴더(folder, 폴더)는 재사용 EA(`Expert Advisor`, 전문가 자문) 모듈(module, 모듈)의 소유 위치(owner location, 소유 위치)다.

## 원칙(Principle, 원칙)

`.mq5` 파일은 얇은 entrypoint(진입점)로 둔다. 재사용 로직(reusable logic, 재사용 로직)은 `.mqh` module(모듈)로 나눈다.

효과(effect, 효과): 새 EA 작업이 한 파일에 계속 붙지 않고, 검증 가능한 작은 경계(boundary, 경계)로 쌓인다.

## 권장 모듈(Recommended Modules, 권장 모듈)

| module(모듈) | responsibility(책임) | output/effect(출력/효과) |
|---|---|---|
| `FeatureInputs.mqh` | closed bar(닫힌 봉), external symbols(외부 심볼), session calendar(세션 달력), weight table(가중치 표) | feature vector(피처 벡터)와 readiness(준비 상태)를 분리 기록 |
| `ModelRuntime.mqh` | ONNX session(ONNX 세션), shape(형태), feature order hash(피처 순서 해시) | Python/MT5 parity(파이썬/MT5 동등성) 검토 단위를 작게 유지 |
| `DecisionSurface.mqh` | probability(확률), threshold(임계값), no-trade rule(무거래 규칙) | 알파 아이디어(alpha idea, 알파 아이디어)와 주문 실행(order execution, 주문 실행)을 분리 |
| `ExecutionBridge.mqh` | order request(주문 요청), broker constraints(브로커 제약), fill/reject(체결/거부) | 수익(profit, 수익) 주장 전 실행 KPI(execution KPI, 실행 KPI)를 남김 |
| `RuntimeTelemetry.mqh` | skip reason(스킵 사유), decision output(판정 출력), tester output(테스터 출력) | MT5 snapshot(MT5 스냅샷)과 KPI record(KPI 기록)를 연결 |

## 사용 규칙(Use Rule, 사용 규칙)

새 EA가 두 번 이상 같은 로직(logic, 로직)을 쓰면 이 폴더의 모듈(module, 모듈)로 끌어올린다. 단계별 실험(stage probe, 단계 탐침)은 stage(단계) 안에 둘 수 있지만, 재사용되는 순간 foundation(기반) 모듈이 진실 원천(source of truth, 진실 원천)이 된다.

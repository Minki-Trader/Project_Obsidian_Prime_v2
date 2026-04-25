# Stage 05 Feature Integrity: Formula Time Alignment Leakage Audit

## 질문(Question, 질문)

58 feature(58개 피처), time axis(시간축), external alignment(외부 정렬), label(라벨)이 alpha exploration(알파 탐색) 전에 의심 없이 읽힐 수 있는가?

## 범위(Scope, 범위)

- feature formula audit(피처 공식 감사)
- session/time audit(세션/시간 감사)
- external alignment audit(외부 정렬 감사)
- label leakage audit(라벨 누수 감사)
- Tier A/B sample label(티어 A/B 표본 라벨) 보존 확인

## 범위 밖(Not In Scope, 범위 밖)

- model training(모델 학습)
- alpha selection(알파 선택)
- Python/MT5 runtime parity(파이썬/MT5 런타임 동등성)
- operating promotion(운영 승격)

## 종료 조건(Exit Condition, 종료 조건)

감사 보고서(audit report, 감사 보고서)가 다음을 모두 판정하면 닫을 수 있다.

- 58 feature(58개 피처) 공식 검산 결과
- DST/session/overnight_return(서머타임/세션/오버나이트 수익률) 확인 결과
- external alignment(외부 정렬) 누수 여부
- label leakage(라벨 누수) 여부
- Tier A/B(티어 A/B) 라벨링과 보고 규칙

이 단계(stage, 단계)는 모델 품질(model quality, 모델 품질)을 주장하지 않는다.

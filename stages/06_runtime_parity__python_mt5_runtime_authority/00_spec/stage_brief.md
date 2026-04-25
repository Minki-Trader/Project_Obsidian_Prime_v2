# Stage 06 Runtime Parity: Python MT5 Runtime Authority

## 질문(Question, 질문)

Python/MT5 parity(파이썬/MT5 동등성)와 full MT5 runtime authority(완전 MT5 런타임 권위)를 alpha exploration(알파 탐색) 전 기준으로 닫을 수 있는가?

## 범위(Scope, 범위)

- parity fixture set(동등성 검사 표본 묶음) 설계
- Python snapshot(파이썬 스냅샷)과 MT5 snapshot(MT5 스냅샷) 비교
- stale MT5 audit tools(낡은 MT5 감사 도구) 폐기 또는 갱신
- 58 feature input order(58개 피처 입력 순서), hash(해시), timestamp(타임스탬프) 일치 확인
- full MT5 runtime authority(완전 MT5 런타임 권위) 완료 또는 차단 사유 기록

## 범위 밖(Not In Scope, 범위 밖)

- model quality(모델 품질)
- alpha selection(알파 선택)
- operating promotion(운영 승격)

## 종료 조건(Exit Condition, 종료 조건)

runtime parity report(런타임 동등성 보고서)가 다음을 기록하면 닫을 수 있다.

- regular/sample boundary/DST/external/missing-input fixture(일반/경계/서머타임/외부/누락 입력 표본)
- Python/MT5 feature vector(파이썬/MT5 피처 벡터) 허용오차 결과
- stale MT5 tool(낡은 MT5 도구) 처리 결과
- runtime authority(런타임 권위) 완료 또는 명시적 blocked(차단) 상태

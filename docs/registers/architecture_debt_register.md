# Architecture Debt Register

이 등록부(register, 등록부)는 구조 부채(architecture debt, 구조 부채)를 기록해서, 나중에 정상 패턴(normal pattern, 정상 패턴)처럼 복사하지 않게 한다.

| debt_id | scope(범위) | symptom(증상) | why_it_matters(중요한 이유) | status(상태) |
|---|---|---|---|---|
| `AD-001` | feature ownership(피처 소유권) | 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)이 파이프라인(pipeline, 파이프라인)으로 밀릴 수 있음 | 피처 진실(feature truth, 피처 진실)을 감사하기 어려워짐 | open |
| `AD-002` | model artifacts(모델 산출물) | 보고서(report, 보고서)가 모델 산출물(model artifact, 모델 산출물)로 오해될 수 있음 | 재현성(reproducibility, 재현성)을 과장할 수 있음 | open |
| `AD-003` | alpha framing(알파 틀짓기) | 소스 정리(source cleanup, 소스 정리)가 알파 탐색(alpha search, 알파 탐색)처럼 보일 수 있음 | 탐색(exploration, 탐색)이 지연됨 | open |
| `AD-004` | Korean encoding(한국어 인코딩) | 한국어 문서가 UTF-8 BOM(UTF-8 BOM 포함)을 잃을 수 있음 | Windows 표시가 깨질 수 있음 | open |
| `AD-005` | exploration discipline(탐색 규율) | 운영 게이트(operating gate, 운영 게이트)가 탐색을 누를 수 있음 | 좋은 아이디어가 너무 일찍 막힘 | open |
| `AD-006` | code surface(코드 표면) | 큰 파이프라인이나 EA(all-in-one file, 일체형 파일)가 자랄 수 있음 | 소유권(ownership, 소유권)과 테스트(test, 테스트)가 흐려짐 | open_mitigated_by_modular_policy |

## 재시작 메모(Restart Note, 재시작 메모)

오래된 Stage 00부터 Stage 07까지의 흐름(flow, 흐름)은 현재 진실(current truth, 현재 진실)에서 제거했다. 효과(effect, 효과)는 `AD-003`과 `AD-005`를 줄이는 것이다.

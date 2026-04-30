# Architecture Debt Register

이 등록부(register, 등록부)는 구조 부채(architecture debt, 구조 부채)를 기록해서, 나중에 정상 패턴(normal pattern, 정상 패턴)처럼 복사하지 않게 한다.

| debt_id | scope(범위) | symptom(증상) | why_it_matters(중요한 이유) | status(상태) |
|---|---|---|---|---|
| `AD-001` | feature ownership(피처 소유권) | 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)이 파이프라인(pipeline, 파이프라인)으로 밀릴 수 있음 | 피처 진실(feature truth, 피처 진실)을 감사하기 어려워짐 | open |
| `AD-002` | model artifacts(모델 산출물) | 보고서(report, 보고서)가 모델 산출물(model artifact, 모델 산출물)로 오해될 수 있음 | 재현성(reproducibility, 재현성)을 과장할 수 있음 | open |
| `AD-003` | alpha framing(알파 틀짓기) | 소스 정리(source cleanup, 소스 정리)가 알파 탐색(alpha search, 알파 탐색)처럼 보일 수 있음 | 탐색(exploration, 탐색)이 지연됨 | open |
| `AD-004` | Korean encoding(한국어 인코딩) | 한국어 문서가 UTF-8 BOM(UTF-8 BOM 포함)을 잃을 수 있음 | Windows 표시가 깨질 수 있음 | open |
| `AD-005` | exploration discipline(탐색 규율) | 운영 게이트(operating gate, 운영 게이트)가 탐색을 누를 수 있음 | 좋은 아이디어가 너무 일찍 막힘 | open |
| `AD-006` | code surface(코드 표면) | 큰 파이프라인이나 EA(all-in-one file, 일체형 파일)가 자랄 수 있음 | 소유권(ownership, 소유권)과 테스트(test, 테스트)가 흐려짐 | open_mitigated_by_code_surface_audit |
| `AD-007` | skill routing(스킬 배치) | 강한 트리거(trigger, 작동 조건)를 가진 스킬만 쓰이고 답변 명확성(answer clarity, 답변 명확성), 레퍼런스 탐색(reference scout, 레퍼런스 탐색), 재현성(reproducibility, 재현성), 데이터 무결성(data integrity, 데이터 무결성) 스킬이 방치될 수 있음 | Codex 작업이 코드 생성에서 끊기고 실험, 근거, 판정, 쉬운 보고로 이어지지 않을 수 있음 | open_mitigated_by_work_packet_router |
| `AD-008` | MT5 runtime helper ownership(MT5 런타임 도구 소유권) | `foundation/mt5/runtime_support.py`의 Stage 10 orchestration(10단계 조율 파일) 위임은 제거됨 | `foundation/models`, `foundation/mt5`, `foundation/control_plane` 소유 모듈(owner module, 소유 모듈)로 runtime helper(런타임 도구)를 분리했다는 완료 기억을 남김 | closed_by_p0p1_runtime_evidence_cleanup |
| `AD-009` | semantic code-surface audit(의미 코드 표면 감사) | 큰 stage-local support file(단계 로컬 지원 파일) 안의 재사용 model/training/threshold/runtime logic(모델/학습/임계값/런타임 로직)을 아직 의미 수준으로 자동 탐지하지 못함 | 파일 크기와 직접 import(가져오기)는 감사하지만, 같은 재사용 패턴이 여러 단계에 반복될 때 foundation owner module(기반 소유 모듈)로 올리는 결정은 아직 사람 판단에 기대기 쉬움 | open |

## 재시작 메모(Restart Note, 재시작 메모)

오래된 Stage 00부터 Stage 07까지의 흐름(flow, 흐름)은 현재 진실(current truth, 현재 진실)에서 제거했다. 효과(effect, 효과)는 `AD-003`과 `AD-005`를 줄이는 것이다.

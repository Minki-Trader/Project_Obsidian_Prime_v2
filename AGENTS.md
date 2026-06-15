# Project Obsidian Prime v2

## 핵심 의도(Core Intent, 핵심 의도)

이 작업공간은 FPMarkets `US100` `M5` 연구와 실행을 위한 깨끗한 프로젝트다.

Obsidian Prime의 개념(concept, 개념)과 브로커 심볼 계약(broker symbol contract, 브로커 심볼 계약)은 유지한다. 하지만 과거 승자(winner, 승자), 과거 승격 이력(promotion history, 승격 이력), 과거 단계 압력(stage pressure, 단계 압력)은 물려받지 않는다.

## 응답 규칙(Language Rule, 언어 규칙)

- 영어 표현(English expression, 영어 표현)을 쓸 때는 같은 문맥 안에 한국어 표기를 함께 쓴다.
- 행동(action, 행동)을 설명할 때는 그 행동의 효과(effect, 효과)도 같이 설명한다.
- 설명은 짧고 쉽게 쓴다.
- 사용자 협업 스타일(user collaboration style, 사용자 협업 스타일)은 co-pilot(공동 조종자, 협업 동반자)처럼 둔다. 실행 가능한 선택지와 근거를 짧게 말하고, 확신이 없으면 claim boundary(주장 경계)를 낮춘다.
- 효과(effect, 효과)는 사용자가 규칙 해석 부담을 떠안지 않고, Codex(코덱스)가 현재 작업에서 무엇을 할 수 있고 무엇을 아직 말하면 안 되는지 먼저 정리하게 하는 것이다.

## Codex 작업 생명주기(Codex Work Lifecycle, 코덱스 작업 생명주기)

작업(work, 작업)을 코드(code, 코드), 실험(experiment, 실험), 보고(report, 보고) 중 하나로만 고르지 않는다. 대부분의 작업은 하나의 work packet(작업 묶음) 안에서 설계(design, 설계), 코드 작성(code writing, 코드 작성), 실행(run, 실행), 근거 기록(evidence recording, 근거 기록), 결과 판정(result judgment, 결과 판정), 사용자 보고(user-facing report, 사용자 보고)를 함께 지난다.

작업 시작 시 `obsidian-session-intake(세션 인입)`는 현재 진실(current truth, 현재 진실), 브랜치/작업트리 적합성, 작업 성격(work family, 작업군) 후보만 좁게 잡는다. 그 다음 `obsidian-work-packet-router(작업 묶음 라우터)`는 `docs/agent_control/work_family_registry.yaml`에서 `primary_family(주 작업군)` 하나, `primary_skill(주 스킬)` 하나, 제한된 `support_skills(보조 스킬)`, `required_gates(필수 게이트)`를 선택한다.

효과(effect, 효과)는 스킬을 많이 붙인 것처럼 보이게 하지 않고, 실제로 선택한 스킬과 closeout(종료 기록)에 연결된 gate(게이트)만 완료 주장(completion claim, 완료 주장)의 근거로 쓰게 하는 것이다.

운영 라우팅(operating routing, 운영 라우팅)의 진실 원천(source of truth, 진실 원천)은 `docs/agent_control/work_family_registry.yaml`이다. 모든 non-trivial work packet(비사소 작업 묶음)은 `primary_family(주 작업군)` 하나와 `primary_skill(주 스킬)` 하나를 먼저 고른다. `support_skills(보조 스킬)`는 필요한 만큼만 붙이고, 완료 전에는 `required_gate_coverage_audit(필수 게이트 커버리지 감사)`로 work packet(작업 묶음)의 `required_gates(필수 게이트)`가 closeout(종료 기록)에 실제로 연결됐는지 확인한다.

효과(effect, 효과)는 Stage 5부터 미래 Stage 50+까지 작업 내용은 달라져도, 스킬 선택(skill selection, 스킬 선택), receipt(영수증), gate(게이트), claim boundary(주장 경계)가 같은 방식으로 작동하게 하는 것이다.

gate(게이트)가 실패하면 `docs/agent_control/self_correction_policy.yaml`의 기본값인 `plan_only` 흐름으로 실패 원인과 repair plan(수정 계획)을 먼저 남긴다. 자동 수정은 allowlist(허용 목록) 안의 packet/closeout 배선 보정으로만 제한하며, gate 완화, threshold 완화, test skip, runtime/model logic 변경은 금지한다.

## Grok 협업 규칙(Grok Collaboration Rule, 그록 협업 규칙)

사용자 요청(user request, 사용자 요청)이나 `/goal(목표)`에 Grok 검토(Grok review, 그록 검토), 외부 리뷰(external review, 외부 리뷰), 2차 의견(second opinion, 2차 의견), stage close(단계 마감)마다 비판 검토(adversarial review, 비판 검토), agent/skill consulting(에이전트/스킬 상담), 또는 Codex 혼자 판단 금지(no solo Codex judgment, 코덱스 단독 판단 금지)가 있으면 `obsidian-grok-collaboration(그록 협업)` 스킬을 필수로 쓴다.

Grok(Grok, 그록)은 external second opinion(외부 2차 의견)일 뿐이다. Codex(코덱스)가 direction(방향), bounded evidence(제한 근거), local verification(로컬 검증), final claim(최종 주장)을 계속 소유한다.

필수 순서(required order, 필수 순서)는 다음이다.

1. Codex(코덱스)가 current truth(현재 진실), proposed direction(제안 방향), success criteria(성공 기준), claim boundary(주장 경계), review size(검토 크기)를 먼저 적는다.
2. Grok(Grok, 그록)에는 필요한 bounded evidence(제한 근거)만 보낸다. whole repo dump(전체 저장소 투입)는 기본값이 아니다.
3. Grok(Grok, 그록) 답변은 `accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)`로 분류한다.
4. Codex(코덱스)가 로컬 장부(register, 등록부), 파일시스템(filesystem, 파일시스템), hash(해시), MT5 output(MT5 출력), git status(깃 상태)로 재검증한 뒤에만 행동한다.

효과(effect, 효과)는 Grok(Grok, 그록)을 쓰더라도 연구 방향이 산으로 가거나, 외부 조언이 자동 실행되는 일을 막는 것이다. Grok 의견은 운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), selected baseline(선택 기준선), Goal Achieve(목표 달성)를 직접 만들 수 없다.

검토 크기(review size, 검토 크기)는 세 단계로 쓴다. small review(소규모 검토)는 좁은 질문 하나, medium review(중간 검토)는 제한 스냅샷(bounded snapshot, 제한 스냅샷) 하나와 집중 질문 하나, large review(대규모 검토)는 architecture/evidence/runtime/policy(구조/근거/런타임/정책)처럼 여러 narrow pass(좁은 회차)로 나눈다.

Grok 호출(call, 호출)은 가능하면 `foundation/control_plane/grok_review_wrapper.py` wrapper(래퍼)를 쓴다. 효과(effect, 효과)는 prompt quoting(프롬프트 인용), timeout(시간 제한), stdout/stderr capture(표준 출력/오류 캡처), noise stripping(잡음 제거), top-level scratch artifact detection(최상위 임시 산출물 감지)을 같은 방식으로 처리하는 것이다. wrapper(래퍼)는 Grok 내용(content, 내용)을 판단하지 않는다.

Windows(윈도우)에서 Grok wrapper(그록 래퍼)나 Python command(파이썬 명령)가 Korean/Unicode(한국어/유니코드)를 stdout(표준 출력)으로 낼 수 있으면 `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONPATH='.'`를 먼저 둔다. Korean fidelity(한국어 보존)가 중요한 prompt(프롬프트)는 큰 PowerShell here-string(파워셸 here-string)보다 UTF-8 prompt file(UTF-8 프롬프트 파일)과 `--prompt-file`을 우선한다. 효과(effect, 효과)는 Windows cp949 console(윈도우 cp949 콘솔) 때문에 Grok output(그록 출력)이나 report template(보고서 템플릿)이 깨지는 일을 줄이는 것이다.

Console/shell encoding guard(콘솔/셸 인코딩 보호)는 agent execution environment(에이전트 실행 환경) 규칙일 뿐이며, gate(게이트), threshold(임계값), evidence requirement(근거 요구)를 완화하지 않는다.

기본 기록 위치(default record location, 기본 기록 위치)는 `docs/agent_control/grok_reviews/`다. 다만 사용자가 이번 작업처럼 patch work material(패치 작업물)을 프로젝트 폴더에 남기지 말라고 명시하면, 새 Grok 패킷(packet, 묶음)을 만들지 않고 기존 산출물(existing artifacts, 기존 산출물), 대화 기록(conversation record, 대화 기록), 또는 프로젝트 밖 임시 경로(temp path, 임시 경로)만 쓴다. 효과(effect, 효과)는 운영 규칙을 지키면서도 사용자가 금지한 임시 산출물을 남기지 않는 것이다.

## 가장 중요한 원칙(Non-Negotiable Principle, 양보 불가 원칙)

탐색(exploration, 탐색)에는 게이트(gate, 제한문)가 없다.

`Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 데이터 완전성(data completeness, 데이터 완전성)이나 문맥 상태(context quality, 문맥 품질)를 설명하는 라벨(label, 라벨)일 뿐이다.

제한(restriction, 제한)은 운영 의미(operational meaning, 운영 의미)를 주장할 때만 붙는다. 예를 들면 실거래(live use, 실거래), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)이다.

## 티어 쌍 작업(Paired Tier Work, 티어 쌍 작업)

Stage 10(10단계) 이후 알파 탐색(alpha exploration, 알파 탐색)은 `Tier A(티어 A)`와 `Tier B(티어 B)`를 항상 같은 작업 묶음(work packet, 작업 묶음)에서 함께 다룬다.

필수 기록(required records, 필수 기록)은 세 가지다.

- `Tier A separate(Tier A 분리)`
- `Tier B separate(Tier B 분리)`
- `Tier A+B combined(Tier A+B 합산)`

효과(effect, 효과)는 `Tier A(티어 A)`만 본 결과를 전체 알파 판독(alpha read, 알파 판독)처럼 과장하지 않고, `Tier B(티어 B)`의 부분 문맥 표본(partial-context sample, 부분 문맥 표본)이 같은 아이디어에서 무엇을 바꾸는지 함께 보게 하는 것이다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서 사용자가 `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)`을 의도하면, 위 세 기록은 각각 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 해석한다.

효과(effect, 효과)는 Tier A(티어 A)의 빈 구간을 Tier B(티어 B)가 실제로 메웠는지 기록하고, separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 combined result(합산 결과)로 오해하지 않게 하는 것이다.

`Tier B(티어 B)`나 합산 기록(combined record, 합산 기록)을 만들 수 없으면 생략하지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 적는다.

## 점진적 경화(Progressive Hardening, 점진적 경화)

- 초기 탐색(early exploration, 초기 탐색)은 빠진 근거를 이름 붙이면 시작할 수 있다.
- `promotion_candidate(승격 후보)`는 비교할 가치가 있다는 뜻이지, 운영선을 교체한다는 뜻이 아니다.
- `runtime_probe(런타임 탐침)`는 런타임을 관찰한다는 뜻이지, 런타임 권위가 닫혔다는 뜻이 아니다.
- `operating_promotion(운영 승격)`과 `runtime_authority(런타임 권위)`는 강한 근거가 필요하다.
- `promotion-ineligible(승격 부적격)`은 아이디어 사망(idea-dead, 아이디어 사망)이 아니다.

## 단계 규칙(Stage Rule, 단계 규칙)

프로젝트는 단계(stage, 단계)로 관리한다.

각 단계는 번호(number, 번호)와 짧은 부제(subtitle, 부제)를 함께 쓴다.

`NN_area__specific_question`

부제(subtitle, 부제)는 이번 단계의 질문(question, 질문)을 설명한다. 미래의 모든 알파(alpha, 알파)를 한 단계 안에 가두면 안 된다.

모델 학습(model training, 모델 학습)과 검증(validation, 검증)이 실제로 가능해지는 순간부터 알파 탐색(alpha research, 알파 탐색)을 시작할 수 있다. 고정된 단계 번호에 묶지 않는다.

## 전선 단계 규칙(Frontier Stage Rule, 전선 단계 규칙)

Stage364(364단계) 이후 새 큰 연구 단위(research unit, 연구 단위)는 `stage_frontier_NN__specific_question(전선 단계 번호와 구체 질문)` 형식을 쓸 수 있다.

`stage_frontier_NN(전선 단계 번호)`은 Stage365(365단계) continuation(연속)이 아니다. independent frontier campaign(독립 전선 캠페인)이다.

핵심 규칙(core rule, 핵심 규칙)은 `reference, not inheritance(참조이지 상속 아님)`이다. Stage12~364(12~364단계)는 prior-stage archive(이전 단계 보관소)로 읽고, preserved clue(보존 단서), negative memory(부정 기억), reusable artifact(재사용 산출물), do-not-repeat note(반복 금지 메모)만 가져온다.

winner(승자), selected baseline(선택 기준선), promotion history(승격 이력), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 prior stage(이전 단계)에서 가져오지 않는다.

Frontier stage(전선 단계)는 새 최상위 `frontiers/` folder(폴더)를 만들지 않고 기존 `stages/*` 아래에 둔다. 세부 운영 규칙(source of truth, 진실 원천)은 `docs/policies/frontier_governance.md`다.

## 알파 탐색 단계 규칙(Alpha Exploration Stage Rule, 알파 탐색 단계 규칙)

Stage 10(10단계)부터 알파 탐색(alpha exploration, 알파 탐색)이 닫히는 단계(stage, 단계)까지는 탐색 라벨(exploration label, 탐색 라벨)과 실행 번호(run number, 실행 번호) 규칙을 쓴다.

- 정식 단계 이름(canonical stage id, 정식 단계 ID)은 `NN_area__specific_question`을 유지한다.
- 탐색 라벨(exploration label, 탐색 라벨)은 `stageN_exploration_group__specific_detail`을 쓴다. 예: `stage10_Model__LGBM`.
- 실행 번호(run number, 실행 번호)는 `run01A`, `run01B`, `run01C`처럼 단계 로컬 순서 번호(stage-local sequence number, 단계 로컬 순서 번호)다.
- 실행 번호(run number, 실행 번호)는 탐색 상한(limit, 한계)이나 역할 고정(role lock, 역할 고정)이 아니다.
- 해당 단계(stage, 단계)는 핵심 주제(core topic, 핵심 주제)를 끝까지 학습(training, 학습), 최적화(optimization, 최적화), 압박 시험(stress test, 압박 시험)한 뒤 다음 단계(next stage, 다음 단계)로 간다.
- 알파 탐색 단계 전환(alpha exploration stage transition, 알파 탐색 단계 전환)은 기준선 선택(baseline selection, 기준선 선택)이 아니라 주제 전환(topic pivot, 주제 전환)이다. 명시적 승격/운영 작업 묶음(explicit promotion/operating packet, 명시적 승격/운영 작업 묶음)이 없으면 마감 단계(closeout stage, 마감 단계)에서 기준선(baseline, 기준선)을 만들지 않는다.

효과(effect, 효과)는 모든 새 작업 회차(pass, 회차)가 알파 탐색(alpha exploration, 알파 탐색)을 좁게 닫지 않고, 같은 단계(stage, 단계) 안에서 끝까지 밀어붙이게 하는 것이다.

## 티어 규칙(Tier Rule, 티어 규칙)

- `Tier A(티어 A)`: 전체 문맥 표본(full-context sample, 전체 문맥 표본)
- `Tier B(티어 B)`: 부분 문맥 표본(partial-context sample, 부분 문맥 표본)
- `Tier C(티어 C)`: 약한 표본(weak sample, 약한 표본) 또는 명시적으로 허용된 로컬 연구(local research, 로컬 연구)

모든 티어(tier, 티어)는 탐색할 수 있다. 보고서(report, 보고서)는 무엇을 탐색했는지만 정직하게 라벨링(labeling, 라벨링)하면 된다.

## 구조 불변 규칙(Architecture Invariants, 구조 불변 규칙)

`docs/policies/architecture_invariants.md`가 코드 배치(code placement, 코드 배치)와 경로 규칙(path rule, 경로 규칙)을 담당한다.

- 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)은 `foundation/features`에 둔다.
- 재사용 모델 로직(reusable model logic, 재사용 모델 로직)이 생기면 별도 소유 모듈(owner module, 소유 모듈)에 둔다.
- `foundation/pipelines`는 조율(orchestration, 조율)을 담당한다. 숨은 진실 원천(source of truth, 진실 원천)이 되면 안 된다.
- MT5 EA(`Expert Advisor`, 전문가 자문)는 얇은 진입점(thin entrypoint, 얇은 진입점)과 `foundation/mt5/include/ObsidianPrime/` 모듈(module, 모듈)로 나눈다.
- EA run variant(EA 실행 변형)는 새 `.mq5` 복제(copy, 복사)로 관리하지 않는다. 파라미터만 다르면 `.set` 파일과 `run_manifest.json(실행 목록)`으로 관리하고, 로직(logic, 로직)이 다르면 `.mqh` 모듈 버전(module version, 모듈 버전)을 올린다.
- `stages/*`는 단계 로컬 산출물(stage-local artifact, 단계 로컬 산출물), 보고서(report, 보고서), 실행 근거(run evidence, 실행 근거)를 담는다.

효과(effect, 효과)는 run별 차이(run-specific difference, 실행별 차이)가 코드 파일 이름만 늘리는 방식으로 숨지 않고, 설정(set, 설정), 모듈 해시(module hash, 모듈 해시), 모델/번들 해시(model/bundle hash, 모델/번들 해시), 테스터 출력(tester output, 테스터 출력)으로 추적되게 하는 것이다.

## 윈도우 긴 경로 규칙(Windows Long Path Rule, 윈도우 긴 경로 규칙)

깊은 stage(단계) 산출물이나 MT5(`MetaTrader 5`, 메타트레이더5) 실행 산출물을 다룰 때 PowerShell(파워셸) `Get-Content`, `Get-ChildItem`, 또는 일반 `Path.exists`가 실패하면 곧바로 missing(누락)이나 blocked(차단)로 판정하지 않는다.

필수 재시도(required retry, 필수 재시도)는 repo-relative path(저장소 상대 경로) 기준으로 `rg --files` 또는 `rg`를 먼저 쓰고, 파일 내용이나 CSV/JSON(표/제이슨) 기계 수정이 필요하면 `foundation.control_plane.ledger.io_path`를 거쳐 Python(파이썬)에서 연다.

효과(effect, 효과)는 Windows MAX_PATH(윈도우 최대 경로 길이) 한계 때문에 존재하는 파일을 없는 파일로 오판하지 않고, durable artifact identity(지속 산출물 정체성)는 계속 repo-relative path(저장소 상대 경로)와 hash(해시)로 남기는 것이다. `\\?\` 같은 extended path prefix(확장 경로 접두사)는 local execution helper(로컬 실행 보조)로만 쓰고 문서 정체성으로 남기지 않는다.

## 탐색 명령(Exploration Mandate, 탐색 명령)

`docs/policies/exploration_mandate.md`가 탐색 규율(exploration discipline, 탐색 규율)을 담당한다.

탐색은 아이디어를 자유롭게 만들고, 정직하게 시험하고, 실패를 기록하며, 운영 조심성(operating caution, 운영 조심성)이 아이디어 필터(idea filter, 아이디어 필터)가 되지 않게 하는 일이다.

## 실행 근거 시스템(Run Evidence System, 실행 근거 시스템)

`docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`가 실행 근거(run evidence, 실행 근거)를 담당한다.

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토된 실행(reviewed run, 검토된 실행)이 된다.

프로젝트 장부(project ledger, 프로젝트 장부)는 `docs/registers/alpha_run_ledger.csv`이고, 단계 장부(stage ledger, 단계 장부)는 `stages/<stage_id>/03_reviews/stage_run_ledger.csv`다.

효과(effect, 효과)는 run/subrun/view(실행/하위 실행/보기)를 한 줄씩 모아, Tier A 분리(Tier A separate, Tier A 분리), Tier B 분리(Tier B separate, Tier B 분리), Tier A+B 합산(Tier A+B combined, Tier A+B 합산), Tier A 우선 + Tier B 대체 라우팅(Tier A primary + Tier B fallback routing, Tier A 우선 + Tier B 대체 라우팅), MT5 런타임 탐침(MT5 runtime probe, MT5 런타임 탐침)을 같이 추적하게 하는 것이다.

## 외부 검증 지연 방지(External Verification Anti-Deferral, 외부 검증 지연 방지)

외부 검증(external verification, 외부 검증)이 필요한 주장(claim, 주장)은 다음 작업(next work, 다음 작업)으로 반복해서 밀 수 없다.

- MT5(`MetaTrader 5`, 메타트레이더5), 브로커 터미널(broker terminal, 브로커 터미널), 전략 테스터(strategy tester, 전략 테스터), 파일 인계(file handoff, 파일 인계), 런타임 동등성(runtime parity, 런타임 동등성)에 기대는 주장은 같은 작업 회차(pass, 회차)에서 가장 좁은 충분한 외부 검증(narrow sufficient external check, 좁은 충분 외부 검증)을 먼저 시도한다.
- 도구(tool, 도구), 스크립트(script, 스크립트), 설정(configuration, 설정), 실행 인계 파일(handoff file, 인계 파일)이 낡았거나 없으면 blocked(차단)로 닫기 전에 현재 프로젝트 기준으로 만들거나 고쳐서 실행을 먼저 시도한다.
- MT5 검증(MT5 verification, MT5 검증)에서 MetaEditor compile(메타에디터 컴파일)은 좁은 외부 검증(narrow external check, 좁은 외부 검증)의 일부일 수 있지만, MT5 snapshot(MT5 스냅샷), strategy tester output(전략 테스터 출력), terminal file output(터미널 파일 출력)을 대체하지 않는다.
- 외부 검증이 없으면 그 주장은 검토 완료(reviewed, 검토됨)나 긍정 판정(positive judgment, 긍정 판정)으로 닫지 않는다. 대신 범위를 낮춰 말하거나, 불충분(inconclusive, 불충분), 무효(invalid, 무효), 또는 차단(blocked, 차단)으로 적는다.
- 같은 빠진 외부 검증(missing external verification, 빠진 외부 검증)을 두 번 연속 next work(다음 작업)로만 남기지 않는다. 실행하거나, 현재 도구를 생성/수정해서 실행을 시도하거나, 사용자 행동(user action, 사용자 행동)이 필요한 정확한 terminal action(터미널 행동)을 요청하거나, 주장을 낮추거나, 차단 사유(blocker, 차단 사유)를 기록한다.
- blocked(차단) 판정은 복구 시도(recovery attempt, 복구 시도), 실행 명령(execution command, 실행 명령), 실패 로그(failure log, 실패 로그), 또는 필요한 사용자 행동(user action, 사용자 행동)을 남긴 뒤에만 쓴다.

## 현재 진실(Current Truth, 현재 진실)

- 현재 상태(current state, 현재 상태): `docs/workspace/workspace_state.yaml`
- 현재 설명(current narrative, 현재 설명): `docs/context/current_working_state.md`
- 재진입 순서(re-entry order, 재진입 순서): `docs/policies/reentry_order.md`
- 에이전트 라우팅(agent routing, 에이전트 라우팅): `docs/policies/agent_trigger_policy.md`

## 폴더 규칙(Folder Rules, 폴더 규칙)

- `docs/`: 계약(contract, 계약), 정책(policy, 정책), 현재 상태(current state, 현재 상태), 결정(decision, 결정), 등록부(register, 등록부), 템플릿(template, 템플릿)
- `data/`: 원천 데이터(raw data, 원천 데이터)와 처리 데이터(processed data, 처리 데이터)
- `foundation/`: 재사용 코드(reusable code, 재사용 코드)와 공유 도구(shared tools, 공유 도구)
- `stage_pipelines/`: 단계별 실행 어댑터(stage-specific execution adapter, 단계 전용 실행 어댑터). `foundation/pipelines`의 legacy shim(호환 진입점) 뒤 실제 stage-local orchestration(단계 로컬 실행 지휘)을 둔다. 재사용 모델/피처/런타임 로직(reusable model/feature/runtime logic, 재사용 로직)의 장기 소유자가 되면 안 된다.
- `stages/`: 번호가 붙은 단계 작업(numbered stage work, 번호 단계 작업)
- `tests/`: 재사용 코드 테스트(test, 테스트)
- `.agents/skills/`: 저장소 전용 에이전트 스킬(repo-scoped agent skills, 저장소 전용 에이전트 스킬)

최상위 임시 폴더(scratch folder, 임시 폴더)는 만들지 않는다.

## 인코딩 규칙(Encoding Rule, 인코딩 규칙)

한국어 `.md`와 `.txt` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 유지한다.

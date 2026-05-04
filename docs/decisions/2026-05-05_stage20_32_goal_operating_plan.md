# Stage20-32 Goal Operating Plan Decision(20-32단계 목표 운영 계획 결정)

## Decision(결정)

Stage20-32(20-32단계) 진행에는 `docs/workspace/stage20_32_goal_operating_plan.md`를 top-level goal operating plan(최상위 목표 운영 계획)으로 사용한다.

효과(effect, 효과): Stage20(20단계)부터 Stage32(32단계)까지 각 model/topic exploration(모델/주제 탐색)을 같은 closeout(마감), MT5 safety(메타트레이더5 안전), reporting/git(보고/깃) 규칙으로 진행한다.

## Scope(범위)

이 decision(결정)은 운영 목표(goal, 목표)를 고정하는 planning/control document(계획/제어 문서)다.

- active stage(활성 단계): Stage20(20단계) `20_model_family_challenge__gam_additive_smooth_shape`
- current run(현재 실행): `not_started`
- planned stages(계획된 단계): Stage21-32(21-32단계)
- branch(브랜치): `codex/stage20-gam-additive-smooth-shape`

효과(effect, 효과): 새 run(실행), stage folder(단계 폴더), KPI(`Key Performance Indicator`, 핵심 성과 지표), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Operating Rule(운영 규칙)

각 stage(단계)는 독립 topic pivot(주제 전환)으로 진행한다. closeout(마감)은 preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건)을 남기며, 별도 explicit promotion/operating packet(명시 승격/운영 작업 묶음) 없이는 baseline(기준선), promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다.

효과(effect, 효과): 충분한 탐색과 운영 주장 금지를 동시에 유지한다.

## MT5 Safety Rule(MT5 안전 규칙)

MT5 run(MT5 실행)은 blind batch(무검토 배치)로 오래 밀지 않는다. small tranche(작은 묶음) 또는 sentinel run(감시 실행) 뒤 terminal log(터미널 로그), tester report(테스터 보고서), telemetry(기록), normalized KPI(정규화 핵심 성과 지표), parser error(파서 오류)를 확인한다.

문제가 생기면 기본 목표는 stop(중지)이 아니라 repair-and-continue(수정 후 계속 진행)다. 같은 오류가 복구 뒤에도 반복되거나 user action(사용자 행동)이 필요할 때만 blocked(차단)로 닫는다.

효과(effect, 효과): 환경/도구 문제(environment/tool issue, 환경/도구 문제) 때문에 stage closeout(단계 마감)을 쉽게 포기하지 않되, 고장난 batch(배치)를 오래 돌리지 않는다.

## Reporting and Git Rule(보고 및 깃 규칙)

중간 보고에는 branch(브랜치), folder(폴더), changed files(변경 파일), active stage folder(활성 단계 폴더), current run id(현재 실행 ID), MT5 report path(MT5 보고서 경로), git status(깃 상태), commit plan(커밋 계획), git push status(깃 푸시 상태)를 포함한다.

의미 있는 checkpoint(중간 지점)마다 정리된 변경은 commit(커밋)과 git push(깃 푸시)를 수행한다. push(푸시) 실패 시 blocker(차단 원인), local commit status(로컬 커밋 상태), next action(다음 행동)을 보고한다.

효과(effect, 효과): Stage20-32(20-32단계) 진행 중 evidence(근거)와 git state(깃 상태)가 분리되지 않는다.

## Claim Boundary(주장 경계)

허용 주장(allowed claims, 허용 주장):

- Stage20-32(20-32단계) goal operating plan(목표 운영 계획) adopted(채택)
- MT5 batch safety/recovery rule(MT5 배치 안전/복구 규칙) adopted(채택)
- folder/branch/git reporting rule(폴더/브랜치/깃 보고 규칙) adopted(채택)

금지 주장(forbidden claims, 금지 주장):

- alpha quality(알파 품질)
- baseline(기준선)
- promotion_candidate(승격 후보)
- operating_promotion(운영 승격)
- runtime_authority(런타임 권위)

효과(effect, 효과): goal(목표) 채택을 성과 판정(result judgment, 결과 판정)으로 오해하지 않는다.

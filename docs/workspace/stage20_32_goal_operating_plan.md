# Stage20-32 Goal Operating Plan(20-32단계 목표 운영 계획)

## Current Truth(현재 진실)

- active stage(활성 단계): `20_model_family_challenge__gam_additive_smooth_shape`
- current run(현재 실행): `not_started`
- active branch(활성 브랜치): `codex/stage20-gam-additive-smooth-shape`
- active stage folder(활성 단계 폴더): `stages/20_model_family_challenge__gam_additive_smooth_shape`
- work order(작업지시서): `docs/workspace/stage19_25_model_research_work_order.md`

효과(effect, 효과): 이 문서는 Stage20-32(20-32단계)의 운영 목표(goal, 목표)를 고정하지만, 새 run(실행), KPI(`Key Performance Indicator`, 핵심 성과 지표), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.

## Goal(목표)

Project Obsidian Prime v2에서 Stage20(20단계)부터 Stage32(32단계)까지 각 stage(단계)를 독립 model/topic exploration(모델/주제 탐색)으로 순서대로 진행한다.

핵심 목표(core goal, 핵심 목표)는 각 model family(모델군) 또는 decision layer(결정 계층)의 고유 behavior(행동 특성), probability shape(확률 모양), regime relation(국면 관계), risk/exit meaning(위험/청산 의미), MT5 handoff/runtime behavior(MT5 인계/런타임 행동)를 충분히 탐색하고 검증한 뒤, 의미 없는 micro-tuning(미세탐색)을 반복하지 않고 reviewed closeout(검토된 마감)으로 닫는 것이다.

효과(effect, 효과): closeout(마감)은 winner selection(승자 선택)이 아니라 topic pivot(주제 전환)을 위한 preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건) 정리로 남는다.

## Stage Sequence(단계 순서)

| stage(단계) | topic(주제) |
|---|---|
| Stage20(20단계) | GAM(`Generalized Additive Model`, 일반화 가산 모델) |
| Stage21(21단계) | ElasticNet Logistic(엘라스틱넷 로지스틱) |
| Stage22(22단계) | HMM(`Hidden Markov Model`, 은닉 마르코프 모델) |
| Stage23(23단계) | supervised regime classifier(지도 국면 분류기) |
| Stage24(24단계) | Survival model(생존 모델) |
| Stage25(25단계) | hazard model(위험률 모델) |
| Stage26(26단계) | NGBoost(`Natural Gradient Boosting`, 자연 그래디언트 부스팅) |
| Stage27(27단계) | quantile boosting(분위수 부스팅) |
| Stage28(28단계) | Markov regression(마르코프 회귀) |
| Stage29(29단계) | River online ML(리버 온라인 머신러닝) |
| Stage30(30단계) | calibration/abstention(보정/기권) |
| Stage31(31단계) | TabNet(탭넷) |
| Stage32(32단계) | TCN(`Temporal Convolutional Network`, 시간 합성곱 네트워크) |

효과(effect, 효과): 진행 순서를 미리 고정해도 각 stage(단계)는 이전 stage(단계)의 model/threshold/baseline(모델/임계값/기준선)을 상속하지 않는다.

## Stage Operating Loop(단계 운영 반복)

각 stage(단계)마다 아래 순서를 따른다.

1. current truth(현재 진실), active branch(활성 브랜치), working tree(작업트리), stage boundary(단계 경계)를 확인한다.
2. 필요한 stage folder(단계 폴더)는 해당 stage(단계)를 실제로 열 때만 만든다.
3. broad scout(넓은 탐색)와 필요한 extreme probe(극단 탐침)를 먼저 수행한다.
4. Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산)를 기록한다.
5. Python-side evidence(파이썬 근거)만으로 닫지 않고, 가능한 가장 좁은 MT5 runtime_probe(MT5 런타임 탐침)를 시도한다.
6. model characteristic(모델 특성)이 충분히 잡히면 meaningless micro-tuning(의미 없는 미세탐색)을 반복하지 않는다.
7. closeout(마감)에는 preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건)을 남긴다.
8. baseline(기준선), promotion_candidate(승격 후보), operating_promotion(운영 승격), runtime authority(런타임 권위)는 별도 explicit promotion/operating packet(명시 승격/운영 작업 묶음)이 없으면 만들지 않는다.
9. closeout(마감)이 끝나면 다음 planned stage(계획된 단계)를 open-only(개방만) 상태로 연다.

효과(effect, 효과): 탐색은 충분히 밀되, operating meaning(운영 의미)은 근거 없이 붙이지 않는다.

## MT5 Batch Safety and Recovery(MT5 배치 안전 및 복구)

MT5 run(MT5 실행)은 큰 batch(배치)를 blind run(무검토 실행)하지 않는다. 여러 variant(변형)를 실행해야 할 때는 small tranche(작은 묶음) 또는 sentinel run(감시 실행)을 먼저 돌리고, 각 tranche(묶음) 뒤에 terminal log(터미널 로그), tester report(테스터 보고서), telemetry(기록), normalized KPI(정규화 핵심 성과 지표), parser error(파서 오류)를 확인한다.

아래 문제가 보이면 batch(배치)를 그대로 계속 밀지 않는다.

- compile error(컴파일 오류)
- tester report missing(테스터 보고서 누락)
- telemetry not updated(기록 미갱신)
- repeated runtime error(반복 런타임 오류)
- model handoff mismatch(모델 인계 불일치)
- ONNX/runtime parity failure(ONNX/런타임 동등성 실패)
- unexpected zero-trade pattern(예상 밖 무거래 패턴)
- settings or symbol mismatch(설정 또는 심볼 불일치)
- parser failure(파서 실패)

문제가 생기면 pause/blocked(일시정지/차단)로 낮춰 원인, failure log(실패 로그), recovery attempt(복구 시도), exact rerun condition(정확한 재실행 조건)을 남긴다. 기본 목표는 stop(중지)이 아니라 repair-and-continue(수정 후 계속 진행)다. 도구(tool, 도구), 설정(configuration, 설정), handoff file(인계 파일), parser(파서), compile/runtime path(컴파일/런타임 경로)를 고친 뒤 예정된 stage closeout(단계 마감)을 계속 목표로 수행한다. 복구 시도 뒤에도 같은 오류가 반복되거나 user action(사용자 행동)이 필요한 경우에만 blocked(차단)로 닫는다.

효과(effect, 효과): 고장난 MT5 batch(배치)를 오래 끌지 않으면서도, 환경 문제(environment issue, 환경 문제)나 도구 문제(tool issue, 도구 문제) 때문에 예정된 stage closeout(단계 마감)을 쉽게 포기하지 않는다.

## Folder Branch Git Reporting(폴더 브랜치 깃 보고)

작업 중간 보고에는 아래 항목을 포함한다.

- current branch(현재 브랜치)
- created/updated folders(생성/수정 폴더)
- changed files(변경 파일)
- active stage folder(활성 단계 폴더)
- current run id(현재 실행 ID)
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로)
- git status(깃 상태)
- commit plan(커밋 계획)
- git push status(깃 푸시 상태)

각 stage(단계) 또는 큰 work packet(작업 묶음)은 `codex/stageNN-topic` 형식의 branch(브랜치)를 사용한다. 이미 적합한 branch(브랜치)가 있으면 그대로 쓰고, 맞지 않으면 새 branch(브랜치)를 만든 뒤 보고한다.

stage open(단계 개방), major MT5 evidence packet(주요 MT5 근거 묶음), stage closeout(단계 마감)처럼 의미 있는 checkpoint(중간 지점)마다 git status(깃 상태)를 확인하고, 변경 내용이 정리되면 commit(커밋)과 git push(깃 푸시)를 수행한다. push(푸시)가 성공하면 branch name(브랜치 이름), commit hash(커밋 해시), pushed remote(푸시 원격), pushed files summary(푸시 파일 요약)를 보고한다. remote/auth/network(원격/인증/네트워크) 문제로 push(푸시)가 막히면 정확한 blocker(차단 원인), local commit status(로컬 커밋 상태), next action(다음 행동)을 보고한다.

효과(effect, 효과): 긴 stage sequence(단계 순서) 진행 중에도 folder(폴더), branch(브랜치), run evidence(실행 근거), push state(푸시 상태)가 흐려지지 않는다.

## Acceptance and Stop Condition(수용 기준과 중지 조건)

각 stage(단계)는 Python-side evidence(파이썬 근거), MT5 runtime_probe(런타임 탐침), normalized KPI(정규화 핵심 성과 지표), closeout packet(마감 묶음)을 남겨야 reviewed closeout(검토된 마감)으로 인정한다.

Stage32(32단계)까지 reviewed closeout(검토된 마감)을 완료한 뒤, final summary(최종 요약)에 모든 stage(단계)의 folder(폴더), branch(브랜치), run evidence(실행 근거), MT5 report(MT5 보고서), git push(깃 푸시) 상태를 남긴다.

효과(effect, 효과): Stage32(32단계) 종료 후에도 어떤 stage(단계)도 alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)로 과장하지 않는다.

# ONNX Frontier Goal Prompt(ONNX 전선 목표 프롬프트)

목표는 US100 M5에서 진짜 강한 ONNX(온엑스)를 하나 만드는 것이다.

완성 기준은 세 가지다.

- 하루 5~10회 거래
- PF(`profit factor`, 수익 팩터) 2~3배, 어떤 구간을 봐도 DD(`drawdown`, 손실폭) 10% 미만
- 매끄럽게 상승하는 balance/equity curve(잔고/자산 곡선)

이 세 가지는 final completion review(최종 완성 검토)의 hard gate(강한 게이트)다. 탐색 초기에 보이는 후보는 목표와 얼마나 가까워지는지만 본다.

## Operating Loop(운영 루프)

하나의 frontier stage(전선 단계)는 하나의 hypothesis lifecycle(가설 생명주기)다.

`hypothesis(가설) -> proxy(프록시) -> WFO/stress/runtime validation(WFO/스트레스/런타임 검증) -> repair(수리) -> closeout(마감)`

가설이 닫힐 때까지 Codex(코덱스)는 실험을 멈추지 않는다. 결론은 completion(완성), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건) 중 하나로 정직하게 닫는다.

다음 frontier stage(전선 단계)는 같은 가설을 물려받지 않는다.

## Archive Rule(보관 규칙)

Stage12~364는 reference only(참조 전용)다.

`reference, not inheritance(참조이지 상속 아님)`

winner(승자), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 가져오지 않는다.

## Grok Collaboration(Grok 협업)

Codex(코덱스)가 실행한다. Grok(Grok)은 second opinion(2차 의견)이다.

Grok review(Grok 검토)는 자동 실행하지 않는다. Codex(코덱스)가 local verification(로컬 검증) 뒤에만 반영한다.

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 full evidence stack(전체 근거 묶음), interval expansion stress(구간 확장 스트레스), MT5/parity(MT5/동등성), adversarial closeout(비판 마감)이 끝난 뒤에만 말한다.

모든 action(행동)의 effect(효과)는 stage result(단계 결과), evidence(근거), policy/update(정책/갱신), run artifact(실행 산출물)가 로컬 작업트리에만 남지 않고 다음 세션과 원격 저장소에서 같은 current truth(현재 진실)로 이어지게 하는 것이다.

Git sync(Git 동기화)는 검증을 대체하지 않는다.

- stage closeout gate(단계 마감 게이트)가 pass(통과)하거나 negative/blocked closeout(부정/차단 마감)이 명확히 기록된 뒤에만 한다.
- stage(단계)는 관련된 변경만 stage(스테이지)한다.
- user changes(사용자 변경), unrelated dirty worktree(무관한 더러운 작업트리)는 건드리지 않는다.
- conflict(충돌), test failure(테스트 실패), gate failure(게이트 실패), remote rejection(원격 거절)이 있으면 push(원격 반영)하지 않고 차단 사유와 next action(다음 행동)을 남긴다.

## Keep Pushing(계속 밀기)

결과가 좋지 않아도 멈추지 않는다. 실패와 차단은 다음 후보를 더 똑똑하게 고르게 하는 근거다.

같은 수리를 반복하면 capped repair(상한 있는 수리) 안에서 닫고, 새로움이 없으면 blocked(차단) 또는 negative memory(부정 기억)로 끝낸 뒤 다음 가설로 간다.

가짜 완료 없이, 뛰어난 ONNX(온엑스)가 나올 때까지 계속 민다.

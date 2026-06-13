# Do-Not-Repeat List(반복 금지 목록)

이 문서는 Stage12~364(12~364단계) archive read(보관소 판독)에서 다음 frontier stage(전선 단계)에 넘길 금지 패턴을 고정한다.

Action(행동): repeated failure pattern(반복 실패 패턴)을 명명한다.

Effect(효과): 새 ONNX(온엑스) 가설이 과거 repair loop(수리 반복)를 다시 밟지 않게 한다.

## Hard DNR(강한 반복 금지)

1. Do not inherit winner/baseline/promotion(승자/기준선/승격을 상속하지 않기). Effect(효과): Stage12~364(12~364단계)를 reference(참조)로만 쓰고 새 frontier hypothesis(전선 가설)를 독립으로 시작한다.
2. Do not escalate one-axis improvement(한 축 개선만으로 격상하지 않기). Effect(효과): density(밀도), PF(수익 팩터), DD(손실폭), curve smoothness(곡선 매끄러움) 중 하나만 좋아진 후보를 앞으로 보내지 않는다.
3. Do not call proxy proof(프록시 증명) runtime proof(런타임 증명)라고 부르지 않기. Effect(효과): scaled density(스케일 밀도), package readiness(패키지 준비성), expected density(예상 밀도)는 MT5 tester output(MT5 테스터 출력)을 대체하지 않는다.
4. Do not repeat sparse PF selector(희소 PF 선택기 반복 금지). Effect(효과): PF999(PF999)나 tiny-sample high PF(얇은 표본 고수익 팩터)를 quality(품질)로 오해하지 않는다.
5. Do not ignore Tier B/combined rows(Tier B/합산 행 무시 금지). Effect(효과): Tier B(티어 B)와 Tier A+B combined(Tier A+B 합산)이 없으면 missing_required(필수 누락) 또는 out_of_scope_by_claim(주장 범위 밖)으로 적는다.
6. Do not split a live hypothesis by impatience(진행 중 가설을 조급하게 쪼개지 않기). Effect(효과): 같은 hypothesis lifecycle(가설 생명주기)은 proxy/WFO/stress/runtime/repair/closeout(프록시/WFO/스트레스/런타임/수리/마감)을 닫을 때까지 같은 frontier stage(전선 단계)에 둔다.
7. Do not package runtime without handoff identity(인계 정체성 없는 런타임 패키지 금지). Effect(효과): feature order(피처 순서), model hash(모델 해시), bundle hash(번들 해시), set file(설정 파일), run manifest(실행 목록), tester output(테스터 출력)이 연결되기 전 runtime authority(런타임 권위)를 말하지 않는다.
8. Do not repeat capped repair(상한 있는 수리 반복 금지). Effect(효과): 같은 수리가 새 정보 없이 반복되면 negative memory(부정 기억)나 blocked(차단)로 닫고 다음 hypothesis(가설)로 넘어간다.

## Soft DNR(약한 반복 금지)

- Single-window scout(단일 구간 탐색)를 completion candidate(완성 후보)로 부르지 않는다.
- Cost-only repair(비용만 수리)나 density-only lift(밀도만 상승)를 package(패키지)로 올리지 않는다.
- Runtime probe observation(런타임 탐침 관찰)을 operating promotion(운영 승격)으로 바꾸지 않는다.
- Stage closeout(단계 마감)에서 next stage(다음 단계)를 여는 이유와 previous archive relation(이전 보관소 관계)을 분리한다.
- Grok advice(그록 조언)는 accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)로 분류한 뒤에만 반영한다.

## Reopen Conditions(재개 조건)

A DNR item(반복 금지 항목)은 아래 조건이 있을 때만 다시 연다.

- new label(새 라벨), new feature surface(새 피처 표면), new runtime representation(새 런타임 표현), or new validation split(새 검증 분할)이 있다.
- 이전 failure axis(실패 축)을 직접 측정하는 guardrail KPI(보호 KPI)가 추가됐다.
- Tier A/B/combined(Tier A/B/합산) 기록이 모두 준비됐거나, 빠진 행을 missing_required(필수 누락)로 명시한다.
- Grok review(그록 검토)와 Codex local verification(코덱스 로컬 검증)이 같은 claim boundary(주장 경계)에 묶인다.

# Codex Receipt(Codex 영수증): Frontier Stage Hypothesis Lifecycle(전선 단계 가설 생명주기)

## Trigger Reason(트리거 이유)

User proposed(사용자 제안) that one frontier stage(전선 단계) should contain one complete hypothesis lifecycle(가설 생명주기): hypothesis(가설), proxy validation(프록시 검증), WFO/stress/runtime validation(WFO/스트레스/런타임 검증), repair(수리), and closeout(마감).

## Review Size(검토 크기)

medium review(중간 검토)

## Codex Position Before Grok(Grok 전 Codex 입장)

Codex provisional view(Codex 임시 견해): the user model(사용자 모델) is a better default frontier unit(더 나은 기본 전선 단위). Effect(효과): scout/WFO(탐색/WFO)와 runtime failure(런타임 실패)가 다른 stage(단계)로 찢기지 않고 같은 hypothesis context(가설 맥락) 안에서 닫힌다.

## Bounded Evidence(제한 근거)

- Active stage(활성 단계): `stage_frontier_01__archive_synthesis_and_new_axis_lock`
- Next run(다음 실행): `frontier01B_build_stage12_364_campaign_map_v1`
- Existing rule(기존 규칙): repair work(수리 작업)는 same frontier stage(같은 전선 단계)의 work packet(작업 묶음)으로 처리한다.
- Final ONNX completion condition(최종 ONNX 완성 조건): 5-10 trades/day(하루 5-10회 거래), PF 2-3x(PF 2-3배), DD <10%(손실폭 10% 미만), smooth rising curve(매끄러운 상승 곡선).

## Prompt Identity(프롬프트 정체성)

- Path(경로): `docs/agent_control/grok_reviews/2026-06-13_frontier_stage_scope_hypothesis_lifecycle/medium_review/prompt.md`
- Hash(해시): `469b7066a1f0e172efc9b19604cfd5b0b14f9fb58c037a03630994e490b79d9f`

## Grok Output Identity(Grok 출력 정체성)

- Path(경로): `docs/agent_control/grok_reviews/2026-06-13_frontier_stage_scope_hypothesis_lifecycle/medium_review/clean_output.md`
- Metadata(메타데이터): `docs/agent_control/grok_reviews/2026-06-13_frontier_stage_scope_hypothesis_lifecycle/medium_review/metadata.json`
- Transport result(전송 결과): success(성공), returncode(반환 코드) `0`, timed_out(시간 초과) `false`
- Hash(해시): `unavailable_after_encoding_repair`

## Advice Classification(조언 분류)

accepted(수용):

- One frontier stage(하나의 전선 단계)는 one hypothesis lifecycle(하나의 가설 생명주기)를 기본 단위로 둔다.
- Runtime validation(런타임 검증), parity(동등성), interval stress(구간 스트레스), and capped repair(상한 있는 수리)는 같은 frontier stage(전선 단계)의 packet sequence(작업 묶음 순서) 안에서 처리한다.
- Frontier01(전선01)은 archive synthesis(보관 종합) and axis lock(축 고정) only(전용) 예외다.
- MT5 cost(MT5 비용)는 predeclared evidence threshold(사전 근거 기준)를 통과한 serious survivor(진지 생존 후보)에만 쓴다.

rejected(거절):

- Stage number(단계 번호)를 proof ladder rung(증명 사다리 단계)로 쓰는 방식.
- `frontier02 = scout/WFO`, `frontier03 = MT5/parity/stress` split(분할)을 기본값으로 두는 방식.
- Every scout clue(모든 탐색 단서)를 MT5 runtime(런타임)까지 보내는 방식.
- Multiple independent theses(여러 독립 가설)를 one frontier stage(전선 단계)에 넣는 방식.
- Unlimited same-stage repair(무제한 같은 단계 수리).
- Middle labels(중간 라벨)에서 completion(완성)을 주장하는 방식.

needs_local_verification(로컬 검증 필요):

- Exact frontier02 thesis sentence(전선02 가설 문장)는 `frontier01B` campaign map(캠페인 지도) 뒤에 확정한다.
- MT5 candidate budget(MT5 후보 예산)은 tester turnaround(테스터 소요 시간)에 따라 3개 또는 5개 후보로 조정한다.
- Repair caps(수리 상한)는 break class(고장 유형) 2개당 2회, total repair packets(전체 수리 작업 묶음) 4개, decision-weight packets(결정 무게 작업 묶음) 8개를 시작값으로 로컬 조정한다.

## Local Verification(로컬 검증)

- `frontier_governance.md` already says repair work(수리 작업)는 same frontier stage(같은 전선 단계)의 work packet(작업 묶음)으로 처리한다.
- `workspace_state.yaml` confirms(확인) no runtime authority(런타임 권위), no operating promotion(운영 승격), no Goal Achieve(목표 달성).

## Claim Boundary(주장 경계)

No operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성) is claimed.

## Final Codex Direction(최종 Codex 방향)

Accept(수용) the user's model with guardrails(안전장치): one frontier stage(전선 단계) should usually own one coherent hypothesis lifecycle(하나의 일관된 가설 생명주기), including proxy/WFO/runtime/stress/repair/closeout(프록시/WFO/런타임/스트레스/수리/마감). Effect(효과): runtime failure(런타임 실패)와 repair evidence(수리 근거)가 다음 stage(단계)로 맥락 없이 넘어가는 일을 줄인다.

Next practical action(다음 실제 행동): proceed with `frontier01B_build_stage12_364_campaign_map_v1`, then revise frontier governance(전선 운영 규칙) to add the Hypothesis Lifecycle Model(가설 생명주기 모델) before opening frontier02(전선02).

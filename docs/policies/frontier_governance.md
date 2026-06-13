# Frontier Governance(전선 운영 규칙)

이 문서는 Stage364(364단계) 이후 연구를 `stage_frontier_NN(전선 단계 번호)`로 여는 규칙을 정한다.

효과(effect, 효과)는 Stage12~364(12~364단계)의 긴 수리 연쇄(repair chain, 수리 연쇄)를 그대로 이어받지 않고, 필요한 기억(memory, 기억)만 참고하면서 새 연구 전선(research frontier, 연구 전선)을 독립적으로 시작하게 하는 것이다.

## Core Rule(핵심 규칙)

`stage_frontier_NN(전선 단계 번호)`은 independent campaign(독립 캠페인)이다.

기존 stage(단계)는 reference archive(참고 보관소)로 읽는다. 기존 stage(단계)의 winner(승자), baseline(기준선), promotion history(승격 이력), runtime authority(런타임 권위), live readiness(실거래 준비)는 가져오지 않는다.

짧은 규칙은 다음이다.

`reference, not inheritance(참조이지 상속 아님)`

## Folder Rule(폴더 규칙)

새 최상위 `frontiers/` folder(폴더)는 만들지 않는다.

Frontier stage(전선 단계)는 기존 stage artifact(단계 산출물) 구조를 쓴다.

```text
stages/stage_frontier_NN__specific_question/
  00_spec/
  01_inputs/
  02_runs/
  03_reviews/
  04_selected/
```

효과(effect, 효과)는 기존 `stages/*` 장부(ledger, 장부), 검토(review, 검토), 선택 상태(selection status, 선택 상태), 경로 규칙(path rule, 경로 규칙)을 유지하는 것이다.

## Opening Contract(개방 계약)

Frontier stage(전선 단계)를 열기 전에는 아래 항목을 먼저 적는다.

- `frontier_thesis(전선 가설)`: 이번 전선이 시험하는 큰 질문.
- `novelty_delta(신규성 차이)`: Stage12~364(12~364단계)와 무엇이 다른지.
- `prior_stage_scan(이전 단계 점검)`: 관련 이전 단계, 장부, 실패 기억을 무엇으로 확인했는지.
- `do_not_repeat(반복 금지)`: 같은 축을 반복하지 않기 위한 금지 목록.
- `exit_rule(종료 규칙)`: 어떤 조건이면 닫을지.
- `claim_boundary(주장 경계)`: 이번 전선에서 말할 수 있는 것과 금지되는 것.

## Prior-Stage Scan(이전 단계 점검)

Prior-stage scan(이전 단계 점검)은 vague review(모호한 검토)가 아니다. 아래 중 하나 이상을 구체적으로 적는다.

- `preserved clue(보존 단서)`
- `negative memory(부정 기억)`
- `reusable artifact(재사용 산출물)`
- `do-not-repeat note(반복 금지 메모)`
- `blocked retry condition(차단 재시도 조건)`

효과(effect, 효과)는 archive amnesia(보관소 망각)를 막되, 과거 결과를 운영 권위(operating authority, 운영 권위)로 세탁하지 않는 것이다.

## Repair Rule(수리 규칙)

Repair work(수리 작업)는 기본적으로 같은 frontier stage(전선 단계) 안의 work packet(작업 묶음)으로 처리한다.

Repair packet(수리 작업 묶음)은 최소한 아래 항목을 적는다.

- `broken_artifact(고장 산출물)`: 무엇이 깨졌거나 불충분한지.
- `repair_boundary(수리 경계)`: 어디까지 고치고 어디부터는 새 전선으로 넘기는지.
- `novelty_check(신규성 점검)`: 단순 반복인지, 새 원천/라벨/런타임/검증 변화가 있는지.
- `exit_or_escalate(종료 또는 격상)`: 같은 frontier stage(전선 단계) 안에서 닫을지, 새 frontier stage(전선 단계)로 격상할지.

새 frontier stage(전선 단계)를 여는 조건은 다음 중 하나다.

- source(원천), label(라벨), runtime representation(런타임 표현), validation philosophy(검증 철학)가 바뀐다.
- 기존 frontier stage(전선 단계)의 exit rule(종료 규칙)이 발동했다.
- 기존 repair chain(수리 연쇄)이 novelty delta(신규성 차이) 없이 반복되고 있다.

효과(effect, 효과)는 모든 작은 수리(repair, 수리)를 새 단계로 부풀리지 않고, 동시에 끝없는 repair loop(수리 반복)를 막는 것이다.

## Decision Weight(결정 무게)

Frontier stage(전선 단계)는 run count(실행 수)가 아니라 decision weight(결정 무게)로 닫는다.

Closeout(마감)은 아래 중 하나 이상을 남겨야 한다.

- `negative memory(부정 기억)`
- `preserved clue(보존 단서)`
- `reference surface(참고 표면)`
- `seed surface(씨앗 표면)`
- `invalid setup(무효 설정)`
- `blocked retry condition(차단 재시도 조건)`
- `next frontier proposal(다음 전선 제안)`

Decision-weight checklist(결정 무게 점검표)는 아래 질문으로 확인한다.

- frontier thesis(전선 가설)가 resolved/negative/blocked(해결/부정/차단) 중 하나로 닫혔는가?
- novelty delta(신규성 차이)가 실제 실행이나 점검에서 시험됐는가?
- negative memory(부정 기억)나 preserved clue(보존 단서)가 구체 경로와 한계와 함께 남았는가?
- 외부 검증(external verification, 외부 검증)이 필요한 claim(주장)은 시도했거나 out_of_scope_by_claim(주장 범위 밖)으로 낮췄는가?
- repair-to-exploration ratio(수리 대비 탐색 비중)가 반복 루프(loop, 반복)를 숨기지 않는가?

## Forbidden Imports(금지 반입)

Frontier stage(전선 단계)는 아래를 prior stage(이전 단계)에서 가져올 수 없다.

- selected baseline(선택 기준선)
- operating reference(운영 기준)
- promotion candidate(승격 후보)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)

이 항목은 별도 promotion/operating packet(승격/운영 작업 묶음)이 없으면 주장하지 않는다.

## Tier Rule(티어 규칙)

Stage10(10단계) 이후의 Tier A/B paired record(티어 A/B 쌍 기록) 규칙은 frontier stage(전선 단계) 안에서도 유지한다.

Tier B(티어 B)나 combined record(합산 기록)를 만들 수 없으면 빈칸으로 두지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 적는다.

## First Frontier(첫 전선)

첫 frontier stage(전선 단계)는 다음으로 연다.

`stage_frontier_01__archive_synthesis_and_new_axis_lock`

이 frontier stage(전선 단계)의 목적은 Stage12~364(12~364단계)를 campaign map(캠페인 지도)으로 압축하고, 새 독립 실험(independent experiment, 독립 실험)을 열기 전에 archive interface(보관소 접점), 반복 금지(do-not-repeat, 반복 금지), 신규성 조건(novelty condition, 신규성 조건)을 고정하는 것이다.

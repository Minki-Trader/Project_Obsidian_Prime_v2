## Grok Review Classification(그록 검토 분류): **needs_local_verification(로컬 검증 필요)** — trigger(트리거)는 방향은 맞지만 운영에 걸 수 있는 **register(등록부) + gate(게이트) + router hook(라우터 훅)** 이 빠져 있어, Codex(코덱스)가 `work_family_registry.yaml`·`workspace_state`·stage-transition skill(단계 전환 스킬)을 확인해야 durable(지속 가능) 여부를 확정할 수 있다.

---

## Trigger Critique(트리거 비판)

**Partially clear(부분적으로 명확)** — “frontier number divisible by 5(전선 번호가 5로 나누어떨어질 때)”는 happy path(정상 경로)에서는 읽기 쉽다. 다만 frontier campaign(전선 캠페인) 운영에서는 아래가 모호하다.

| Gap(간극) | Risk(위험) |
|---|---|
| **Primary vs fallback trigger(주 트리거 vs 대체 트리거) 우선순위** | NN=10 closeout(마감)과 “5 closeouts since last retrospective(이전 중간 검토 이후 5회 마감)”이 동시에 참이면 한 번만 돌릴지, 두 번 돌릴지 불명확 |
| **“Closing(마감)” 정의** | `stage closeout(단계 마감)` gate(게이트) 통과 전 partial close(부분 마감), repair-only close(수리만 마감), `blocked(차단)` closeout이 카운트에 들어가는지 없음 |
| **“Before opening next(다음 개방 전)” enforcement(강제)** | 누가 next open(다음 개방)을 막는지 없으면 “권장 루틴”으로 흐려짐 |
| **Non-contiguous NN(비연속 번호)** | `NN-4..NN` 가정은 frontier02→64 audit(감사)처럼 번호가 도약하면 잘못된 5개 묶음을 만들 수 있음 |
| **Per-stage Grok(단계별 그록)와 중복** | 이미 open/validation/closeout(개방·검증·마감)마다 Grok이 있으면, 5단계 retrospective(중간 검토)가 무엇을 **추가** 검토하는지 경계가 없으면 비용만 커짐 |

**Recommendation(권고):** trigger(트리거)를 **두 개의 machine-checkable field(기계 검증 가능 필드)** 로 쪼개라.

1. **Block trigger(블록 트리거):** `closed_frontier_ids_since_last_retrospective.length >= 5` (또는 마지막 블록의 frontier NN % 5 == 0)
2. **Scope resolver(범위 결정):** numeric range(숫자 범위)가 아니라 **실제 closeout receipt(마감 영수증)가 있는 최근 5개 `stage_frontier_*` ID 목록**

효과(effect, 효과): 번호 도약·스킵·병렬 작업에서도 같은 5개 묶음을 재현할 수 있다.

---

## Missing Fields / Guards(빠진 필드·가드) — policy/skill governance(정책/스킬 거버넌스) 한정

### 1. Retrospective register(중간 검토 등록부) — **가장 큰 누락**

Durable rule(장기 규칙)에는 **source of truth(진실 원천)** 가 필요하다. 최소 필드:

```yaml
five_stage_retrospective:
  last_completed_at_frontier: <int|null>
  last_completed_stage_ids: [<5 canonical stage ids>]
  last_completed_at_utc: <iso>
  next_due_after_closeout_count: 5   # or rolling counter
  closeouts_since_last: <int>
```

없으면 “five since last(이전 이후 5회)” fallback(대체)이 **Codex memory(코덱스 기억)** 에 의존한다.

### 2. `work_family_registry.yaml` packet entry(작업 묶음 등록)

`policy_skill_governance(정책/스킬 거버넌스)` 안에 별도 packet(묶음)이 있어야 한다. 예:

- `primary_family`: `policy_skill_governance`
- `primary_skill`: `obsidian-grok-collaboration`
- `support_skills`: `obsidian-stage-transition`, `obsidian-claim-discipline`, `obsidian-grok-collaboration` (이미 있으면 중복 최소화)
- `required_gates`: 예) `five_stage_retrospective_receipt`, `retrospective_bounded_evidence`, `codex_local_verification_log`, `next_stage_open_block_cleared`

효과(effect, 효과): 매 5단계마다 “이번엔 그록 쓸까?”를 매번 재협상하지 않는다.

### 3. Stage-transition **hard guard(강제 가드)**

`obsidian-stage-transition`에 명시적 분기:

- IF `closeouts_since_last >= 5` OR `closing_frontier_nn % 5 == 0`
- THEN **block** `next_frontier_open` until retrospective `required_gates` satisfied
- ELSE allow

“before opening next(다음 개방 전)”을 **skill-level guard(스킬 수준 가드)** 로 고정해야 한다.

### 4. Idempotency + dedup guard(멱등·중복 방지)

| Field(필드) | Purpose(목적) |
|---|---|
| `retrospective_packet_id` | e.g. `frontier_61-65_retro_v1` |
| `covered_stage_ids[]` | 동일 5개에 대해 이중 실행 방지 |
| `excludes_per_stage_grok_receipts: true` | 단계 마감 Grok receipt(영수증) 재검토가 아니라 **cross-stage synthesis(단계 간 합성)** 임을 명시 |

### 5. Bounded evidence schema(제한 근거 스키마)

Required evidence(필수 근거) 목록은 좋지만, **per-stage row template(단계별 행 템플릿)** 이 없으면 5단계마다 형식이 달라진다. 최소 컬럼:

`stage_id | hypothesis | proxy_kpi | mt5_probe_kpi | gap_cause | closeout_label | preserved_clue | negative_memory | systemic_repeat(Y/N) | next_action`

Plus block-level(블록 수준): `repeated_systemic_issues[]`, `repair_priority_delta`, `direction_delta` (claim boundary(주장 경계) 안에서만).

### 6. Review size + wrapper contract(검토 크기·래퍼 계약)

5-stage scope는 **large review(대규모 검토)** 로 고정하고, `grok_review_wrapper`에:

- `--prompt-file` (UTF-8)
- snapshot-only(스냅샷 전용) rules
- **artifact path cap**(산출물 경로 상한) — whole repo dump(전체 저장소 투입) 금지

`docs/agent_control/grok_reviews/` 하위 **naming convention(이름 규칙)**: e.g. `YYYY-MM-DD_frontier_NN-4_to_NN_five_stage_retrospective/`

### 7. Missing-stage semantics guard(누락 단계 의미 가드)

`missing_required | blocked | out_of_scope_by_claim` 라벨은 맞다. 추가로:

- **5개 미만이면 retrospective completion(중간 검토 완료) 주장 금지** — `incomplete_block(불완전 블록)` 으로만 닫기
- 누락 1개라도 `next_action`에 **backfill vs accept-gap(보강 vs 간극 수용)** 결정 필드 필수

### 8. `self_correction_policy` linkage(자기수정 정책 연결)

Retrospective gate(게이트) 실패 시 기본값 `plan_only(계획만)` 흐름을 retrospective packet에도 동일 적용. gate 완화·threshold 완화는 금지(기존 정책과 정합).

### 9. Claim boundary enforcement template(주장 경계 강제 템플릿)

Forbidden claims(금지 주장)는 본문에 있으나, **report header guard(보고서 헤더 가드)** 가 없으면 drift(표류)한다. 고정 헤더:

`ALLOWED: direction_delta, repair_priority_delta | FORBIDDEN: completion, baseline, promotion, runtime_authority, live_readiness, goal_achieve`

---

## Concrete Verdict on Focus Question(집중 질문 판정)

| Question(질문) | Answer(답) |
|---|---|
| Trigger clear enough?(트리거가 충분히 명확한가?) | **Happy path only(정상 경로만)** — fallback(대체)·closeout 정의·enforcement(강제)·non-contiguous NN(비연속 번호)에서 불명확 |
| Missing field/guard for durability?(지속성을 위한 빠진 필드/가드?) | **`five_stage_retrospective` register**, **registry packet + required_gates**, **stage-transition open block**, **idempotent packet_id + covered_stage_ids**, **per-stage evidence row schema**, **incomplete_block rule**, **grok receipt path convention** |

---

## Accepted Elements(수용 요소)

- **Cadence every 5 closeouts(5회 마감마다 주기)** — frontier velocity(전선 속도)와 맞음
- **Explicit evidence bundle(명시적 근거 묶음)** — hypothesis·proxy/MT5 gap·negative memory는 systemic learning(시스템 학습)에 적합
- **Claim boundary(주장 경계)** — direction/repair only(방향·수리만)는 governance(거버넌스)에 맞음
- **No silent omit(조용히 생략 금지)** — `missing_required` 등 라벨링은 Paired Tier·ledger(장부) 문화와 일치

---

## Rejected / Downgrade(거절·하향)

- **Reject as standalone prose rule(단독 산문 규칙으로는 거절)** — register(등록부)·gate(게이트)·router(라우터) 없이는 durable policy(지속 정책)가 아니라 **team habit(팀 습관)** 에 가깝다
- **Reject numeric-only scope `NN-4..NN`(숫자만 범위)** — canonical closeout list(정식 마감 목록) 기반이 더 안전

---

## Suggested Codex Local Verification Checklist(코덱스 로컬 검증 체크리스트)

Codex(코덱스)가 다음을 확인하면 `accepted(수용)` 으로 올릴 수 있다.

1. `docs/workspace/workspace_state.yaml` 또는 전용 register에 retrospective counter(카운터) 추가 가능 여부
2. `docs/agent_control/work_family_registry.yaml`에 packet + gates 추가 위치
3. `.agents/skills/obsidian-stage-transition/SKILL.md`에 open-block branch(개방 차단 분기) 삽입 지점
4. `.agents/skills/obsidian-grok-collaboration/SKILL.md`에 “five-stage retrospective” subsection(하위 절) 필요 여부
5. 기존 per-stage Grok closeout(단계별 그록 마감)과 **non-overlapping synthesis mandate(겹치지 않는 합성 mandate)** 문구

**Bottom line(요약):** 사용자 의도(5단계마다 그록과 중간 토론)는 **accepted intent(수용 의도)** 다. 다만 durable rule(장기 규칙)으로 만들려면 trigger(트리거) 문장보다 **`closeouts_since_last` register + next-open gate + canonical 5-stage ID list + registry packet** 이 먼저다.

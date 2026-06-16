## Grok second opinion (스냅샷 전용)

Codex 방향은 대체로 맞습니다. **강한 보호장치는 유지**하고, **“비사소함” 경계가 흐려서 전체 운영 스택이 매 턴/소작업에 붙는 것**이 가장 큰 토큰·작업 낭비 원인으로 보입니다. 아래는 스냅샷만 기준으로 한 findings(발견)입니다.

---

### Finding 1 — `non-trivial`(비사소) 경계 불명 → 라우팅·영수증·게이트 과적용

| Field | Content |
|--------|---------|
| **severity(심각도)** | **high** |
| **evidence(근거)** | AGENTS.md:21, :25; registry:4, :9; trigger policy:28; session-intake:43(압축 모드는 있으나 대비만 있음) |
| **preserve(보존)** | `primary_family`/`primary_skill` 선택, closeout(종료) 시 `required_gate_coverage_audit`, claim boundary(주장 경계) |
| **tighten(줄일 것)** | **trivial packet(사소 묶음)** 명시: status/review/meta-policy 질문은 `primary_skill` 1개 + **compact receipt(압축 영수증)**; `support_skills` 기본 0; 게이트는 `not_applicable` + 한 줄 사유. “비사소” 정의를 registry/trigger policy에 5~8개 예시로 고정 |
| **recommendation** | **accepted-ready(즉시 수용 가능)** |

**효과:** 소질문에 4개 lint gate + full closeout 배선이 붙는 패턴을 막고, 실험·MT5·closeout에는 기존 강도 유지.

---

### Finding 2 — cold re-entry(전체 재진입) vs delta check(변화분 점검) 긴장

| Field | Content |
|--------|---------|
| **severity(심각도)** | **high** |
| **evidence(근거)** | reentry_order:9–22(22문서); session-intake:22(warm이면 delta 우선); trigger policy:173(매번 모든 스킬 읽기 아님) |
| **preserve(보존)** | stage/branch/worktree 불일치 시 full re-entry; exploration/run-evidence/architecture touch 시 조건부 추가 읽기(reentry-read:12–17) |
| **tighten(줄일 것)** | warm thread 기본: **delta checklist 3–5항**(active stage, current run, user intent change, blocker change)만. 22문서 순서는 **cold/mismatch trigger(냉시작/불일치 트리거)**에만. intake 출력에 `reentry_mode: delta|cold` 필수 |
| **recommendation** | **accepted-ready** |

**효과:** 매 턴 22문서 읽기를 “규칙 위반으로 느껴지는 생략”이 아니라 **명시적 최소 모드**로 만듦.

---

### Finding 3 — Grok packet(그록 묶음) 영수증 필드 과다 (좁은 질문에도 full schema)

| Field | Content |
|--------|---------|
| **severity(심각도)** | **high** (Grok-required 작업에서) |
| **evidence(근거)** | grok skill:37(단순 편집·git status엔 Grok 금지); grok skill:161(다수 mandatory receipt fields); grok skill 136 lines; trigger policy:35(overlay로 receipt+packet 추가) |
| **preserve(보존)** | bounded evidence, advice classification, forbidden claim check, user/goal 명시 시 Grok 필수 |
| **tighten(줄일 것)** | `review_size=small`이면 receipt **subset**: `trigger_reason`, `bounded_evidence`, `advice_classification`, `claim_boundary`만. `medium/large`만 prompt/output identity·full local verification block. pre-Grok read list(grok:74)도 review_size에 비례 |
| **recommendation** | **accepted-ready** |

**효과:** 이번 같은 narrow policy review에 full forensic packet이 기본으로 붙는 비용을 줄임. Grok 협업 의무는 유지.

---

### Finding 4 — policy/meta 작업에 exploration-grade gate(게이트) 스택

| Field | Content |
|--------|---------|
| **severity(심각도)** | **medium** |
| **evidence(근거)** | registry:9(receipts + closeout gates); registry policy_skill_governance 4 gates(`work_packet_schema_lint`, `skill_receipt_schema_lint` 등); AGENTS.md:25 |
| **preserve(보존)** | 스키마/계약 **실제 변경** 시 lint gate |
| **tighten(줄일 것)** | read-only review packet은 gate를 **register-first N/A**: “no schema diff, no closeout claim”. lint는 **파일 touch(수정) 발생 시**만 required |
| **recommendation** | **needs_local_verification** — 실제로 meta review마다 4 gate가 돌아가는지, N/A가 이미 허용되는지 스냅샷만으로는 불명 |

---

### Finding 5 — session-intake + work-packet-router 고정 오버헤드

| Field | Content |
|--------|---------|
| **severity(심각도)** | **medium** |
| **evidence(근거)** | AGENTS.md:21(intake→router 항상); router skill 59 lines; session-intake 82 lines; trigger policy:173 |
| **preserve(보존)** | non-trivial·ambiguous·MT5·publish 작업의 family/skill/gate 선택 |
| **tighten(줄일 것)** | router 출력에 **`skills_to_read: [primary_only]`** 기본; support는 justified 1줄당 1개. `information_only`는 router **lite**: family + primary_skill만, gate 목록 생략 또는 전부 N/A |
| **recommendation** | **accepted-ready** |

**효과:** “읽을 스킬 목록”이 암묵적으로 bloated(비대)해지는 것을 구조적으로 제한.

---

### Finding 6 — five-stage retrospective(5단계 중간 검토) **선행 합성** 낭비

| Field | Content |
|--------|---------|
| **severity(심각도)** | **medium** |
| **evidence(근거)** | AGENTS.md:70(frontier open 전 gate); trigger policy:72(`not_due`면 open 허용); trigger policy:75(per-stage Grok 반복 아님) |
| **preserve(보존)** | due 시 cross-stage synthesis; frontier open 차단 규칙 |
| **tighten(줄일 것)** | stage open 전 **첫 단계 = register due check 한 번** → `not_due`면 즉시 기록하고 종료. due일 때만 synthesis 템플릿 로드 |
| **recommendation** | **accepted-ready** |

**효과:** “막연히 5단계 검토 준비”를 하다 토큰이 새는 패턴을 register-first로 차단.

---

### Finding 7 — 규범 텍스트 중복 (AGENTS.md ↔ skills ↔ policies)

| Field | Content |
|--------|---------|
| **severity(심각도)** | **medium** (누적 토큰) |
| **evidence(근거)** | Grok 규칙이 AGENTS.md + grok skill:37, :74, :118, :161에 분산; routing이 AGENTS.md:21,:25 + registry:4 + trigger policy:28 + router skill에 분산 |
| **preserve(보존)** | 각 주제의 canonical source(진실 원천) 하나 |
| **tighten(줄일 것)** | AGENTS.md는 **intent + pointer**만; 상세 절차는 skill/policy 한 곳. 중복 bullet은 “See skill X §Y”로 치환. **금지:** safeguard 문구 삭제가 아니라 **역할 분리** |
| **recommendation** | **needs_local_verification** — 실제 중복 라인 수·어느 쪽이 canonical인지 스냅샷에 없음 |

---

### Finding 8 — `support_skill_limit_default=3` → 방어적 스킬 적층

| Field | Content |
|--------|---------|
| **severity(심각도)** | **low–medium** |
| **evidence(근거)** | registry:6; trigger policy:115 |
| **preserve(보존)** | 복잡 작업에서 필요한 support attach 능력 |
| **tighten(줄일 것)** | trivial/`information_only` 기본 limit **0–1**; support 추가 시 receipt에 **1줄 justification** 필수 |
| **recommendation** | **accepted-ready** |

---

### Finding 9 — 대형 스킬 본문 선로딩 (특히 grok-collaboration 136 lines)

| Field | Content |
|--------|---------|
| **severity(심각도)** | **low–medium** |
| **evidence(근거)** | skill size table; grok skill 136 lines; grok:37(Grok 비트리거 시 불필요) |
| **preserve(보존)** | 트리거 시 전체 절차·금지 조항 |
| **tighten(줄일 것)** | skill front-matter에 **10–15줄 Quick path**: “not triggered → do not load body”. 본문은 triggered일 때만 |
| **recommendation** | **accepted-ready** |

---

### Finding 10 — 한국어 병행표기 토큰 비용

| Field | Content |
|--------|---------|
| **severity(심각도)** | **low** (응답 토큰) |
| **evidence(근거)** | AGENTS.md language rule (workspace rules); forbidden advice에서 제거 금지 |
| **preserve(보존)** | 한국어 병행표기 규칙 전체 |
| **tighten(줄일 것)** | **terms per response 1회 병행** (동일 용어 반복 병행 축소) — 규칙 약화가 아니라 **중복만 제거** |
| **recommendation** | **accepted-ready** (단, “병행 생략”이 아니라 “반복 병행 축소”로만) |

---

## 우선순위 요약 (Codex에 넘길 순서)

1. **Trivial vs non-trivial taxonomy + compact receipt** (Finding 1) — accepted-ready
2. **Delta re-entry 기본화, 22-doc full path는 cold only** (Finding 2) — accepted-ready
3. **Grok small-review compact receipt** (Finding 3) — accepted-ready
4. **Five-stage register-first `not_due`** (Finding 6) — accepted-ready
5. **Router lite + `skills_to_read` cap** (Finding 5) — accepted-ready

**거절(rejected-if-unsafe):** MT5 probe, claim guards, mandatory Grok when user asks, five-stage when due, ledger/evidence, no-inherited-winner/baseline, Korean pairing **삭제** — 전부 해당 없음(제안하지 않음).

**로컬 검증 필요:** policy packet에서 4 lint gate가 실제로 매번 도는지(Finding 4), 중복 텍스트 규모(Finding 7).

---

## Classification of Codex direction (전체 방향)

| Codex proposal | Grok verdict |
|----------------|--------------|
| Hard safeguards preserve | **accepted** |
| Over-application on small tasks | **accepted** — 스냅샷이 원인을 뒷받침 |
| Bounded fixes (minimal modes, delta, compact receipts, register-first, N/A reasons) | **accepted-ready** — Finding 1–3, 5–6과 정합 |

**Claim boundary(주장 경계):** 이 답은 prompt snapshot만 기반; 실제 에이전트가 매 턴 intake+router+full reentry를 수행하는지, gate N/A가 closeout에서 통과하는지는 **needs_local_verification**입니다. 다만 **규칙 설계상 과확장 위험**은 스냅샷만으로도 high confidence로 지적 가능합니다.

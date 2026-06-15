## Verdict(판정)

**Accepted with additions(추가 조건 하에 수용)** — The proposed correction is **appropriately scoped(범위가 적절함)** as **execution hygiene(실행 위생)** only. It matches the failure pattern(실패 패턴) in the prompt and does not, on its face, relax **evidence gates(근거 게이트)**, **thresholds(임계값)**, **MT5 runtime requirements(MT5 런타임 요구)**, or **stage claims(단계 주장)**.

**Claim boundary(주장 경계):** I cannot verify whether `obsidian-workflow-drift-guard` is the best sole owner skill, or whether AGENTS.md already has overlapping text. That is **needs_local_verification(로컬 검증 필요)** before patch.

---

## Why the scope fits(범위가 맞는 이유)

| Proposed rule(제안 규칙) | Matches observed failure(관측된 실패) |
|---|---|
| Enumerate before open(열기 전 열거) | Wrong skill path, guessed contract name |
| List packet dirs before assuming names(패킷 폴더 먼저 목록) | `request.md` vs `prompt.md` |
| Prefer `rg` over shell globs on Windows(윈도우에서 rg 우선) | Wildcard/glob mistake |
| One failed guess → discovery, no adjacent retries(한 번 실패하면 발견으로 전환) | Repeated assumption chain |

Narrow placement in **AGENTS.md(에이전트 지침)** plus **one operational skill(하나의 운영 스킬)** is proportionate: global norm + enforceable habit, not a new gate system.

---

## Missing guardrails(누락 보호장치) Codex should add before patching

### 1. Discovery precedence order(발견 우선순위)

Define a fixed order so the new rule does not fight existing **Windows long-path(윈도우 긴 경로)** guidance:

1. **Repo-relative `rg --files`** (or targeted `rg` with `-g`)
2. **Scoped directory listing(범위 제한 목록)** — parent folder first, not whole-repo scan for one file
3. **`Get-ChildItem`** only when `rg` is unavailable or the target is outside repo search scope
4. **Python `io_path` / extended-path helpers(확장 경로 헬퍼)** only after existence is established at repo-relative identity

**Effect(효과):** One canonical “how to find” story, less skill-to-skill contradiction.

### 2. “Non-obvious file(명확하지 않은 파일)” trigger criteria(발동 기준)

Without triggers, agents either over-enumerate or under-enumerate. Codex should require preflight when **any** of these hold:

- Path was **inferred(추론됨)** from convention, memory, or another repo’s habit
- Path came from **user text without repo-relative confirmation(사용자 문구만 있고 저장소 상대 경로 미확인)**
- First open/read **failed once(한 번 실패)**
- Artifact family has **known naming variance(이름 변형이 있는 산출물군)** — e.g. `docs/contracts/*`, `docs/agent_control/grok_reviews/*/`, packet folders

**Effect(효과):** Preflight is mandatory where mistakes actually happened, not on every obvious path.

### 3. Adjacent-guess definition(인접 추정 정의)

“Do not retry adjacent guesses(인접 추정 재시도 금지)” needs a precise definition:

- Same parent directory + tweaked basename (`request.md` → `prompt.md` → `review.md`)
- Same artifact role + different extension
- Same stage/packet id + different suffix

After one failure: **mandatory listing of that directory(해당 디렉터리 필수 목록화)** before any second path.

**Effect(효과):** Stops the exact failure mode described in the prompt.

### 4. Corrected source-of-truth record format(교정된 진실 원천 기록 형식)

When discovery corrects a path, record minimally:

- **Wrong assumption(잘못된 가정)**
- **Repo-relative canonical path(저장소 상대 정식 경로)**
- **Discovery method used(사용한 발견 방법)** (`rg --files`, list dir, etc.)

Do **not** treat extended paths (`\\?\`) as durable identity in docs or closeout.

**Effect(효과):** Correction becomes reusable evidence within the pass, not a silent retry.

### 5. Missing vs wrong-path fork(없음 vs 잘못된 경로 분기)

After enumeration, if the file is still absent:

- Classify as **`missing_material(자료 누락)`** per workflow-drift taxonomy
- Do **not** continue filename guessing or “nearby” file substitution

**Effect(효과):** Path hygiene stays linked to blocker discipline instead of becoming more guessing.

### 6. Skill-path specificity(스킬 경로 명시)

Add an explicit rule aligned to the first failure:

- Repo skills: **`.agents/skills/<skill-name>/SKILL.md`**
- User-attached or external skill paths are valid **only when explicitly provided(명시적으로 제공될 때만)**
- Do not default to home-directory skill locations (`.cursor`, `.grok`, etc.) for this repo

**Effect(효과):** Directly prevents the wrong skill path mistake without hardcoding a fragile list.

### 7. Anti-duplication cross-reference(중복 방지 상호참조)

New text should **reference(참조)** existing **Windows Long Path Rule(윈도우 긴 경로 규칙)** and **architecture path identity(구조 경로 정체성)** instead of duplicating them.

Add one line: *“Path resolution preflight does not substitute for hash, ledger, or MT5 evidence identity.”*

**Effect(효과):** Avoids two conflicting path sections in AGENTS.md.

### 8. Enumeration scope cap(열거 범위 상한)

Guard against hygiene becoming noise:

- List **the smallest sufficient directory(최소 충분 디렉터리)** (e.g. `docs/contracts/`, one packet folder)
- Avoid unscoped repo-wide listing unless the asset location is unknown

**Effect(효과):** Fast passes on obvious work, disciplined discovery on ambiguous work.

### 9. Owner-skill boundary(소유 스킬 경계)

`obsidian-workflow-drift-guard` is a reasonable **primary owner(주 소유자)** for *missing vs wrong path vs changed goal*.

Codex should add a single cross-link line in patch plan (not necessarily full duplication) to:

- **`obsidian-architecture-guard`** — durable repo-relative identity
- **`obsidian-reentry-read`** — cold start: read current truth paths before deep work

**Effect(효과):** Prevents three skills from diverging on the same rule.

### 10. No filename canon in AGENTS.md(AGENTS.md에 파일명 정본 금지)

Do **not** patch in permanent literals like “always `prompt.md`” unless tied to a versioned contract. Prefer:

> *List the packet directory; never assume template filenames.*

**Effect(효과):** Long-term prevention without new stale canon when layouts change.

---

## What Codex should not add(추가하면 안 되는 것)

- No new **gates(게이트)** or “path preflight passed” claims in closeout
- No exemption from **MT5 / external verification(외부 검증)** because a path was found
- No mandate to Grok-review every path correction (this packet is meta; the rule itself does not require Grok per patch)

---

## Suggested patch shape(권장 패치 형태)

**AGENTS.md:** Short **Path/Name Resolution Preflight(경로·이름 해석 사전확인)** subsection under execution/environment rules — triggers, precedence, one-failure rule, missing-material fork, cross-refs.

**`obsidian-workflow-drift-guard/SKILL.md`:** Operational checklist block — *before open*, *after first failure*, *after list still empty*.

**Optional(선택):** One-line reminder in **`obsidian-session-intake`** — “any path inferred this turn?” — only if Codex confirms intake already owns turn-start habits (**needs_local_verification**).

---

## Summary(요약)

The correction is **right-sized(적정 크기)** and **aligned with user intent(사용자 의도와 일치)** (long-term AGENTS.md + Skill update, not a one-off hack). Before patching, Codex should add **trigger criteria**, **discovery precedence**, **adjacent-guess definition**, **missing-material fork**, **skill-path specificity**, **anti-duplication cross-refs**, and **no stale filename canon** — so the rule prevents repetition without bloating every file open or conflicting with existing Windows/path identity policy.

# Grok Receipt(그록 영수증): wrapper_guard(래퍼 보호)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_grok_wrapper_duplicate_arg_guard/small_review`
- classification(분류): `accepted`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), hashes(해시), ledgers(장부), MT5 output(MT5 출력)으로 다시 검증한다.
- effect(효과): Grok output(그록 출력)은 authority(권위)가 아니라 bounded critique(제한 비판)로만 쓰인다.

## Clean Output(정리 출력)
## Grok review verdict(그록 검토 판정)

**Classification(분류): `accepted` (수용)**

From this snapshot alone(이 스냅샷만으로), the proposed guard(제안 보호 규칙) is a **durable prevention(지속 예방)** for the **two observed failure modes(관찰된 두 실패 유형)**:

1. **Wrong `--extra-arg` shape(잘못된 `--extra-arg` 형태)** — `--extra-arg --no-plan` treats the next token as a value; flags that start with `--` should use `--extra-arg=--flag`.
2. **Duplicate default flags(기본 플래그 중복)** — re-passing flags the wrapper already sends causes failure; omitting them succeeded.

Adding the same rule to **AGENTS.md** and **`obsidian-grok-collaboration`** matches Rule2(추가규칙2): repeated operational mistakes → documented cooperation guard(반복 운영 실수 → 문서화된 협조 보호).

**Claim boundary(주장 경계)** is respected: this is **policy/skill governance(정책/스킬 운영 보정)** only. It does not relax gates(게이트), thresholds(임계값), MT5 evidence( MT5 근거), or completion claims(완료 주장).

---

## Concrete risks only(구체적 위험만)

1. **Stale default list(기본값 목록 노후화)**
   If `grok_review_wrapper.py` changes its default CLI flags without updating AGENTS.md and the skill, agents may **skip needed flags(필요 플래그 누락)** or **still duplicate(여전히 중복)** under wrong assumptions.

2. **“Unless output proves absent” ambiguity(“출력이 없음을 증명할 때만” 모호성)**
   Agents may **misread wrapper stdout/stderr(래퍼 출력 오독)** and re-add defaults when unnecessary, or omit a flag that was actually dropped — recreating intermittent transport errors(간헐적 전송 오류 재발).

3. **Incomplete positive guidance(불완전한 허용 가이드)**
   The guard says what **not** to pass; it does not list **safe `--extra-arg` examples(안전한 `--extra-arg` 예시)** (e.g. timeout, model, prompt-file). Codex may still pass **invalid or redundant extras(무효/중복 추가 인자)** for other flags.

4. **`--rules` not in the observed duplicate failure(관찰 실패에 `--rules` 미포함)**
   The snapshot proves duplication pain for `--no-plan`, `--no-subagents`, `--disable-web-search`. Treating `--rules` as a default is **plausible but not demonstrated here(여기서는 입증되지 않음)**; wrong inclusion/exclusion in the doc could cause a **new class of mistake(새 실수 유형)**.

5. **Syntax fix alone is insufficient for all argparse edge cases(argparse 엣지 케이스)**
   `--extra-arg=--flag` fixes flag-shaped values; **positional or multi-value extras(위치/다값 추가 인자)** may still fail without separate examples — the guard reduces but does not eliminate wrapper CLI misuse(래퍼 CLI 오용).

6. **No wrapper-level enforcement(래퍼 수준 강제 없음)**
   Policy-only guard depends on agent compliance(에이전트 준수). Without deduplication or clearer errors in the wrapper itself, **repeat mistakes remain possible(반복 실수 가능)** if docs are skipped or context is trimmed.

---

## Snapshot boundary(스냅샷 경계)

This verdict does **not** verify the live default flag set in code, wrapper error messages, or whether AGENTS.md / skill text already partially covers this. Those would be **Codex local verification(코덱스 로컬 검증)** tasks — not required to **accept the policy direction(정책 방향 수용)** from this bounded snapshot.

**Bottom line(요약):** **Accept** the proposed AGENTS.md + skill addition as durable prevention for the documented duplicate-argument mistakes; ship with explicit “do not duplicate these defaults” wording and `--extra-arg=--flag` form, and treat risks 1–4 as follow-up hardening(후속 강화), not blockers to the policy change.

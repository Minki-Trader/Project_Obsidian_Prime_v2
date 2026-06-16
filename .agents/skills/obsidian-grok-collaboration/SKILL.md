---
name: obsidian-grok-collaboration
description: Use Grok(Grok, 그록) as an external second-opinion reviewer(외부 2차 의견 검토자) for Project Obsidian Prime v2 when the user explicitly asks for Grok, a /goal includes Grok or external review, stage closeout requires adversarial review, research direction needs critique, Codex should not decide alone, or agent/skill settings need consulting. Manage bounded evidence(제한 근거), review size(검토 크기), wrapper capture(래퍼 캡처), advice classification(조언 분류), and local verification(로컬 검증) before acting.
---

# Obsidian Grok Collaboration

Use this skill to bring Grok(Grok, 그록) in as an independent reviewer(독립 검토자), not as final authority(최종 권위).

## Required Triggers

Run Grok collaboration when any current user request, `/goal`, or stage closeout condition says:

- `Grok에게 검토받아줘`
- `Stage 종료 후마다 Grok 검토`
- `closeout 전에 외부 리뷰`
- `Grok에게 연구방향 점검받기`
- `Codex 혼자 판단하지 말고 Grok 2차 의견`
- `stage close(단계 마감)마다 비판 검토`
- `방향성 제시까지`
- `Codex 방향성 제시 후 Grok 2차 토론`
- `agent/skill consulting(에이전트/스킬 상담)`
- `five-stage retrospective(5단계 중간 검토)` or `5개 stage마다 Grok 중간 검토`

Effect(효과): user-declared external review(사용자 선언 외부 검토)를 optional advice(선택 조언)가 아니라 required gate(필수 게이트)로 다룬다.

## Recommended Triggers

Consider Grok when the user asks for:

- big-picture research direction(큰그림 연구 방향)
- stage utilization review(단계 활용도 검토)
- agent/skill consulting(에이전트/스킬 컨설팅)
- adversarial review(비판 검토)
- drift check(드리프트 점검)

Do not use Grok for simple edits, path/hash/register recounts, git status, or direct MT5 evidence verification unless the user explicitly asks.

## Five-Stage Retrospective(5단계 중간 검토)

Run this as a cross-stage synthesis(단계 간 종합), not as a repeat of per-stage Grok receipt(단계별 그록 영수증).

Trigger(트리거):

- closing frontier number(마감 전선 번호)가 5의 배수다.
- or `docs/registers/five_stage_retrospective_register.yaml` has five `closed_frontier_ids_since_last_retrospective(이전 중간 검토 이후 마감 전선 ID)`.

Bounded evidence(제한 근거)는 최근 5개 canonical frontier closeout stage ids(정식 전선 마감 단계 ID)를 행(row, 행)으로 만든다.

Required row fields(필수 행 필드):

```text
stage_id | hypothesis | proxy_kpi | mt5_runtime_probe_kpi | proxy_runtime_gap_cause | closeout_label | preserved_clue | negative_memory | systemic_repeat | next_action
```

Required block fields(필수 블록 필드):

- `retrospective_packet_id(중간 검토 묶음 ID)`
- `covered_stage_ids(검토 단계 ID)`
- `repeated_systemic_issues(반복 시스템성 문제)`
- `direction_delta(방향 변화)`
- `repair_priority_delta(수리 우선순위 변화)`
- `next_stage_open_block_check(다음 단계 개방 차단 점검)`

If fewer than five closeout receipts(마감 영수증) are available, label the packet `incomplete_block(불완전 블록)` and record the repair action(수리 행동). Do not claim retrospective completion(중간 검토 완료).

Allowed claims(허용 주장): direction_delta(방향 변화), repair_priority_delta(수리 우선순위 변화).

Forbidden claims(금지 주장): completion(완성), selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

## Required Order

1. Codex reads local truth first.
   - Check `AGENTS.md`, `docs/workspace/workspace_state.yaml`, current stage docs, ledgers, and relevant reports.
   - Effect(효과): Grok receives a bounded evidence snapshot(근거 스냅샷), not a vague repo dump.

2. Codex states direction before Grok.
   - Write a compact direction proposal(방향성 제안): current state(현재 상태), proposed next action(제안 행동), success criteria(성공 기준), claim boundary(주장 경계), review size(검토 크기), and drift risks(드리프트 위험).
   - Effect(효과): Grok reviews a concrete plan instead of inventing a new project.

3. Select review size.
   - `small review(소규모 검토)`: one narrow question(좁은 질문) and one compact prompt(압축 프롬프트).
   - `medium review(중간 검토)`: one bounded snapshot(제한 스냅샷) and one focused question(집중 질문).
   - `large review(대규모 검토)`: multiple narrow passes(여러 좁은 회차), such as architecture/evidence/runtime/policy(구조/근거/런타임/정책), then one Codex synthesis(Codex 종합).
   - Effect(효과): large review(대규모 검토)가 monolithic prompt(거대 단일 프롬프트)로 무너지지 않는다.
   - For `small review(소규모 검토)`, use compact receipt(압축 영수증) and proportional pre-read(비례 사전 읽기): read only the current truth(현재 진실) and directly relevant evidence(직접 관련 근거) needed for the narrow question.
   - Effect(효과): user-required Grok(사용자 요구 그록)을 유지하면서 small question(작은 질문)이 full forensic packet(전체 포렌식 묶음)으로 커지지 않는다.

4. Build or select the review record.
   - Default location(기본 위치):
   - `docs/agent_control/grok_reviews/YYYY-MM-DD_topic/inputs/`
   - `docs/agent_control/grok_reviews/YYYY-MM-DD_topic/prompts/`
   - `docs/agent_control/grok_reviews/YYYY-MM-DD_topic/outputs/`
   - `docs/agent_control/grok_reviews/YYYY-MM-DD_topic/metadata/`
   - If the user forbids project-folder patch work material(프로젝트 폴더 패치 작업물), do not create a new packet in the project. Use existing artifacts(기존 산출물), conversation record(대화 기록), or a temp path outside the repo(저장소 밖 임시 경로), and report that limit.
   - Effect(효과): user constraints(사용자 제약)을 어기지 않으면서 review trace(검토 추적)를 유지한다.

5. Call Grok.
   - Preferred executable(실행 파일): `C:\Users\awdse\.grok\bin\grok.exe`
   - Preferred wrapper(선호 래퍼): `python -m foundation.control_plane.grok_review_wrapper`
   - Preferred CLI pattern(CLI 패턴): `grok.exe --prompt-file <prompt.md>`.
   - Use timeout(시간 제한), stdout/stderr capture(표준 출력/오류 캡처), prompt hash(프롬프트 해시), and unexpected artifact detection(예상 밖 산출물 감지).
   - For bounded review(제한 검토), include snapshot-only direct-answer rules(스냅샷 전용 직접 답변 규칙): Grok(Grok, 그록) must answer only from the prompt(프롬프트), must not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).
   - Prefer wrapper defaults(래퍼 기본값) that pass `--rules`, `--no-plan`, `--no-subagents`, and `--disable-web-search`. Effect(효과): Grok(Grok, 그록)이 Codex(코덱스)의 local verification(로컬 검증)을 대신하려다 timeout(시간초과)되는 일을 줄인다.
   - Do not pass those wrapper default flags(래퍼 기본 플래그) again through `--extra-arg` unless the wrapper output(래퍼 출력) proves they are absent. If an extra argument(추가 인자) begins with `--`, use `--extra-arg=--flag` form. Effect(효과): duplicate argument failure(중복 인자 실패) and `--extra-arg` parsing mistakes(`--extra-arg` 파싱 실수)를 줄인다.
   - Do not rely on `--disallowed-tools read_file,write_file,edit_file,bash,grep,glob,ls` as the primary safety control. Local trials showed those names may not match tool entries.
   - When using `--output-dir`, prefer wrapper summary output(래퍼 요약 출력) and read `clean_output.md(정리 출력)` or `metadata.json(메타데이터)` by path. Open `raw_diagnostics.json(원본 진단)` only for timeout(시간초과), failure(실패), transport issue(전송 문제), or audit need(감사 필요).
   - Effect(효과): Grok transport(전송) 문제와 Grok content(내용) 판단을 분리한다.

6. Codex summarizes and challenges Grok.
   - Separate `accepted(수용)`, `rejected(거절)`, `needs_local_verification(로컬 검증 필요)`.
   - Automatically reject forbidden claims(금지 주장) if Grok declares operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), selected baseline(선택 기준선), or Goal Achieve(목표 달성).
   - Effect(효과): Grok becomes second opinion(2차 의견), not unchecked authority(무검증 권위).

7. Continue only after drift guard.
   - Compare Grok advice with user intent, current stage boundary, registers, and files.
   - If Grok pushes a new topic that the user did not ask for, label it `out_of_scope_by_user_intent(사용자 의도 범위 밖)`.

## Packet Rules

- Do not send the whole repo by default.
- Use snapshots(스냅샷) with repo-relative paths(저장소 상대경로), short excerpts(짧은 발췌), and redaction(가림 처리) when needed.
- Keep heavy artifacts(무거운 산출물) out of prompts.
- Do not send secrets(비밀값), account credentials(계정 자격), full local paths(전체 로컬 경로), or large build outputs(큰 빌드 출력) unless the user explicitly asks and the claim needs it.
- Save raw diagnostics(원본 진단) separately from clean output(정리 출력).
- Keep all Grok material under `docs/agent_control/grok_reviews/` unless the user forbids project-folder work material.

## Wrapper Contract

The wrapper(래퍼) is a thin transport layer(얇은 전송 계층), not a reviewer(검토자).

Required behaviors(필수 동작):

- prompt length preflight(프롬프트 길이 사전 확인)
- empty prompt guard(빈 프롬프트 방지)
- no-shell argument passing(shell 없는 인자 전달)
- timeout with partial output salvage(시간 제한과 부분 출력 회수)
- stdout/stderr capture(표준 출력/오류 캡처)
- deterministic noise stripping(결정적 잡음 제거)
- raw diagnostics preservation(원본 진단 보존)
- top-level scratch artifact detection(최상위 임시 산출물 감지)

Forbidden behaviors(금지 동작):

- interpreting Grok advice(Grok 조언 해석)
- accepting or rejecting content(내용 수용/거절)
- editing project files based on Grok output(Grok 출력 기반 프로젝트 파일 수정)
- claiming verification(검증 주장)

## Claim Guard

Grok cannot create these claims by itself:

- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)
- selected baseline(선택 기준선)

Codex must verify any factual claim against local filesystem(파일시스템), registers(등록부), hashes(해시), MT5 outputs(MT5 출력), or git status(깃 상태).

## Required Receipt

Every Grok-required packet must produce a receipt(영수증).

For `small review(소규모 검토)`, the compact receipt(압축 영수증) minimum is:

- `trigger_reason(트리거 이유)`
- `bounded_evidence(제한 근거)`
- `advice_classification(조언 분류)`
- `claim_boundary(주장 경계)`
- `final_codex_direction(최종 Codex 방향)`

For `medium review(중간 검토)` and `large review(대규모 검토)`, or when the Grok result changes files, execution, stage closeout(단계 마감), or publish/push(게시/원격 반영), use the full receipt(전체 영수증) with:

- `trigger_reason(트리거 이유)`
- `review_size(검토 크기)`
- `direction_before_grok(그록 전 방향)`
- `bounded_evidence(제한 근거)`
- `prompt_identity(프롬프트 정체성)`: path(경로), hash(해시), or conversation-only reason(대화 전용 사유)
- `grok_output_identity(그록 출력 정체성)`: path(경로), hash(해시), or conversation-only reason(대화 전용 사유)
- `advice_classification(조언 분류)`: accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)
- `local_verification(로컬 검증)`
- `forbidden_claim_check(금지 주장 확인)`
- `final_codex_direction(최종 Codex 방향)`

## Closeout Rule

When Grok is a required gate, the final closeout must record:

- Grok packet path(패킷 경로)
- prompt path(프롬프트 경로)
- output path(출력 경로)
- accepted/rejected advice(수용/거절 조언)
- local verification result(로컬 검증 결과)
- final Codex direction(최종 Codex 방향)

Effect(효과): direction setting(방향성 제시), Grok second discussion(Grok 2차 토론), and execution(진행)이 one tracked chain(하나의 추적 사슬)로 남는다.

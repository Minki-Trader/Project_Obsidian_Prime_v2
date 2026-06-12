# Grok Operational Smoothing Snapshot(Grok 운영 안정화 스냅샷)

Created(생성): 2026-06-12

## User Goal(사용자 목표)

The user wants future Grok feedback and discussion(Grok 피드백과 토론)을 run smoothly(원활히 실행) for both large reviews(대규모 검토) and small reviews(소규모 검토).

The desired outcome(원하는 결과)는 Grok을 external second opinion(외부 2차 의견)으로 안정적으로 호출하고, Codex가 local verification(로컬 검증)을 한 뒤, clean discussion loop(정리된 토론 루프)를 유지하는 것이다.

## Current Observed Issues(현재 관찰 이슈)

From the previous Grok review packet(이전 Grok 검토 묶음):

- `--prompt-file` calls(프롬프트 파일 호출)이 response body(응답 본문)를 만들지 못하거나 `max turns reached`로 끝났다.
- `grok.exe -p` single prompt(단일 프롬프트)는 sanity check(정상 확인)와 compact review(압축 검토)에서 작동했다.
- Running from repo cwd(저장소 작업 경로) triggered many MCP warning logs(MCP 경고 로그), especially `codex` handshake failure(핸드셰이크 실패) and `atlassian` OAuth required(OAuth 필요).
- stdout/stderr(표준 출력/표준 오류) behavior was noisy(시끄러움) and inconsistent(불일치). Some calls exited with code 0(종료 코드 0) but wrote no clean answer(정리 답변) to output files.
- Long prompts(긴 프롬프트) were less reliable(덜 안정적). Short compact prompts(짧은 압축 프롬프트) worked better.
- A top-level `mcps/` folder(최상위 mcps 폴더) was created during Grok execution and had to be deleted because top-level scratch folders(최상위 임시 폴더) are not allowed in this repo.
- An older unrelated `grok.exe` process(프로세스) was already present. New hung sanity-check processes(멈춘 정상 확인 프로세스) had to be stopped.

## Existing Project Constraints(기존 프로젝트 제약)

- Grok collaboration(Grok 협업)은 required gate(필수 게이트)처럼 다뤄진다 when user explicitly asks for Grok.
- All Grok material(Grok 자료)은 `docs/agent_control/grok_reviews/` 아래에 남겨야 한다.
- Codex must state direction first(Codex가 방향을 먼저 제시), then call Grok, then separate accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요).
- Grok cannot create runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), selected baseline(선택 기준선), or goal achieve(목표 달성).
- Korean `.md` and `.txt` files(한국어 문서)는 UTF-8 with BOM(UTF-8 BOM 포함)을 유지해야 한다.
- Top-level scratch folders(최상위 임시 폴더)는 만들지 않는다.

## Codex Draft Direction(Codex 초안 방향)

1. Treat Grok as isolated external reviewer(격리된 외부 검토자), not as a repo-local coding agent(저장소 내부 코딩 에이전트).
2. Use `grok.exe -p` single prompt(단일 프롬프트) instead of `--prompt-file` until file mode is proven stable(안정 확인).
3. Run Grok from an isolated temp cwd(격리 임시 작업 경로), not from repo root(저장소 루트), to reduce MCP initialization noise(MCP 초기화 잡음).
4. Build compact prompt tiers(압축 프롬프트 단계):
   - small review(소규모 검토): 1 to 2 KB inline prompt(인라인 프롬프트)
   - medium review(중간 검토): 2 to 5 KB bounded snapshot(제한 스냅샷)
   - large review(대규모 검토): staged digest(단계별 요약) rather than whole repo dump(전체 저장소 투척)
5. Add a wrapper script(래퍼 스크립트), likely `foundation/control_plane/run_grok_review.py`, to do:
   - preflight sanity check(사전 정상 확인)
   - temp cwd setup(임시 작업 경로 준비)
   - compact prompt call(압축 프롬프트 호출)
   - timeout handling(시간 제한 처리)
   - stdout/stderr capture(표준 출력/오류 캡처)
   - ANSI/log stripping(색상/로그 제거)
   - clean output write(정리 출력 저장)
   - no repo-root scratch artifact(저장소 루트 임시 산출물 없음)
6. Update the repo Grok skill or policy(저장소 Grok 스킬 또는 정책) only after the wrapper behavior(래퍼 동작)가 verified(검증)된다.

## Questions For Grok(Grok에게 묻는 질문)

1. Is the isolated external reviewer model(격리 외부 검토자 모델) the right default?
2. Should `-p` single prompt(단일 프롬프트)를 default로 고정하고 `--prompt-file`은 disabled(비활성) 또는 fallback(대체)로 둘까?
3. What should the small/medium/large review protocol(소/중/대 검토 절차) look like?
4. What should a robust wrapper(견고한 래퍼)가 capture, sanitize(정리), and record(기록)해야 하는가?
5. What should be changed in skill/policy(스킬/정책) versus kept as implementation detail(구현 세부)?

## Claim Boundary(주장 경계)

This consultation(상담)은 Grok operational workflow(Grok 운영 흐름)만 다룬다. It does not judge model quality(모델 품질), trading readiness(거래 준비), runtime authority(런타임 권위), or stage promotion(단계 승격).


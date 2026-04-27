# Branch Policy(브랜치 정책)

agent work(에이전트 작업)는 사용자가 다른 branch name(브랜치 이름)을 요청하지 않는 한 `codex/` branches(`codex/` 브랜치)를 쓴다.

사용자가 명시적으로 요청하지 않으면 `main(메인)`으로 merge(병합)하지 않는다.

## Worktree Fit Rule(작업트리 적합성 규칙)

파일을 수정하기 전에 current branch/worktree(현재 브랜치/작업트리)가 requested work packet(요청된 작업 묶음)과 맞는지 확인한다.

현재 branch(브랜치)가 다른 stage(단계), PR(`pull request`, 풀 리퀘스트), experiment(실험), governance task(거버넌스 작업)에 묶여 있으면 이미 열려 있다는 이유만으로 계속 작업하지 않는다. 맞는 branch/worktree(브랜치/작업트리)로 switch(전환)하거나, 올바른 base(기준)에서 새 `codex/` branch(`codex/` 브랜치)를 만들거나, 전환이 unrelated work(관련 없는 작업)를 섞을 위험이 있으면 멈추고 mismatch(불일치)를 보고한다.

Examples(예시):

- Stage 09 handoff branch(Stage 09 인계 브랜치)에서 Stage 10 implementation(Stage 10 구현)을 계속하지 않는다.
- 사용자가 해당 PR(풀 리퀘스트)에 governance changes(거버넌스 변경)를 함께 담으라고 명시하지 않았다면 stage-run code branch(단계 실행 코드 브랜치)에서 governance files(거버넌스 파일)를 수정하지 않는다.
- 사용자가 명시적으로 결합을 요청하지 않았다면 두 open PR scopes(열린 PR 범위)를 한 worktree(작업트리)에 섞지 않는다.

Effect(효과): branch names(브랜치 이름)와 worktree state(작업트리 상태)가 actual task(실제 작업)와 맞게 유지되어, 나중 PR(풀 리퀘스트)이나 local Codex handoff(로컬 코덱스 인계)가 숨은 cross-stage edits(단계 간 섞인 수정)를 물려받지 않는다.

# Grok Receipt(그록 영수증): stage_open(단계 개방)

- path(경로): `docs/agent_control/grok_reviews/2026-06-16_frontier60_stage_open_snapshot`
- classification(분류): `accepted`
- metadata_success(메타데이터 성공): `True`
- metadata_timed_out(메타데이터 시간초과): `False`
- local_action(로컬 행동): Codex(코덱스)가 repo files(저장소 파일), EA parameters(EA 파라미터), MT5 output(MT5 출력)으로 다시 검증했다.
- effect(효과): Grok(그록) output(출력)은 authority(권위)를 만들지 않고 review boundary(검토 경계)만 제공한다.

## Clean Output(정리 출력)
## Frontier60 stage-open review

### 1. verdict
**accepted**

구조적으로는 **한 번의 마감 가능한 질문(one closable question, 한 번에 닫을 수 있는 질문)** 입니다. F59가 proxy는 버티고 MT5만 무너졌고 parity는 맞았다는 전제 아래, **반복 진입 마찰(repeated-entry friction, 반복 진입 마찰)** 을 admission cadence(진입 허용 리듬)로 풀 수 있는지 묻는 설계라서 frontier stage-open(전선 단계 개시) 기준에 맞습니다.

### 2. novelty_check
**acceptable_new_hypothesis**

- **F59 대비**: 같은 long-quality score family(롱 품질 점수 계열)를 두고, 바뀐 축은 **runtime representation / admission cadence(런타임 표현·진입 허용 리듬)** 입니다. label family(라벨 계열), direction flip(방향 뒤집기), validation-guided threshold tuning(검증 구간 기준 임계값 조정)이 아니라는 선언도 맞습니다.
- **F52 대비**: envelope 아이디어는 겹치지만, F52는 **reference-only clue(참고용 단서)** 이고 F60은 **F59 long axis + proxy–MT5 괴리 설명 가설**에 묶인 단일 falsification test(단일 반증 시험)입니다. 그래서 **그대로 반복(repeat, 반복)** 보다는 **제한된 결합 테스트(bounded combination test, 제한된 결합 시험)** 에 가깝습니다.
- **invalid_setup(무효 설계)** 로 보이지는 않습니다. 다만 F52 surface overlap(표면 겹침) 때문에 “새 라벨/새 모델”처럼 보이면 안 되고, **같은 score source 위의 admission test(같은 점수 원천 위 진입 허용 시험)** 로만 읽혀야 합니다.

### 3. main_risk
- **F52 envelope repeat risk**: close-on-flat, entry-transition, cooldown, ATR SL/TP는 F52에서 이미 PF 실패 단서가 있습니다. score만 바꿔 같은 envelope를 다시 쓰면 **repeat(반복)** 으로 읽힐 수 있습니다.
- **long_axis_source_no_transfer**: F59 failure mode(실패 양식)가 남아 있으면 admission layer(진입 허용 층)만으로 MT5 PF 붕괴를 못 고칠 수 있습니다.
- **density rescue train-only drift**: train에서 density를 맞추는 과정이 사실상 **hidden threshold search(숨은 임계값 탐색)** 가 될 수 있습니다.
- **grid combinatorics**: q × cooldown × max_hold 조합이 작아 보여도 proxy selection(프록시 선택) 단계에서 **repair ladder(수리 사다리)** 로 번질 위험이 있습니다.
- **proxy–MT5 gap 재현**: F59는 parity perfect(패리티 완전 일치)인데 MT5 PF 0.46 / 0.58이었습니다. envelope가 **signal path(신호 경로)** 를 실제로 바꾸지 않으면 같은 괴리가 반복될 수 있습니다.
- **compressed secondary view 착시**: F59 compressed view는 DD는 낮지만 density 2.77/day였습니다. F60의 5–10/day 목표와 섞이면 **density-aligned economics collapse(밀도 맞춤 경제성 붕괴)** 가 다시 날 수 있습니다.

### 4. required_locks
- **Non-inheritance lock**: F52/F59에서 winner, baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 가져오지 않음. F59 candidate score artifact(후보 점수 산출물)만 고정 입력으로 사용.
- **Frozen score source lock**: F59 `f59b_directional_long_quality_extratrees_d7_l100_long_fav65_adv35_q90` 계열의 **feature/model/threshold semantics(피처·모델·임계값 의미)** 를 재학습·재라벨·재튜닝 금지. 바뀌는 것은 admission/runtime envelope만.
- **Pre-registered finite grid lock**: 제안 grid만 허용. q80/q85/q90, entry-transition=true, close-on-flat=true, reentry cooldown 1|2, same-direction cooldown 3|4, max hold 4|6, same ATR SL/TP family. **사후 확장 금지**.
- **Selection protocol lock**: **train-only density rescue(학습 구간만 밀도 구제)** 로 1개만 고름. validation/OOS는 **read-only eligibility read(읽기 전용 적격 판독)** 만. validation/OOS로 grid pruning(격자 가지치기) 금지.
- **Density band lock**: proxy target **5–10/day** 를 사전 등록. 못 맞추면 바로 **negative memory(부정 기억)** 후보로 닫기.
- **Stop ladder lock**: **proxy 1회 선택 + MT5 runtime probe 1회** 만. F60 안에서 broad repair(광범위 수리), secondary view rescue, extra-cost ladder, relabeling 금지.
- **Closure lock**: proxy density miss 또는 MT5 validation/OOS **PF < 1** 이면 `long_axis_friction_escape` 질문을 **negative memory** 로 닫기.
- **Claim boundary lock**: `runtime_probe_observation`만. completion, baseline, promotion, runtime authority, live readiness, Goal Achieve 금지.
- **F52 orthogonality note lock**: closeout에 **“F52 tested envelope without F59 score source; F60 tests admission on fixed F59 score only”** 한 줄을 남겨 repeat dispute(반복 논쟁)를 막기.
- **Parity/evidence lock**: 선택된 1개 후보에 대해 feature_ready/signal/long_count parity(패리티)와 tester forensics(테스터 포렌식)를 F59와 같은 방식으로 기록. envelope가 신호 수를 바꿔야 하는데 diff=0이면 **invalid runtime change(무효 런타임 변경)** 로 처리.

### 5. smallest_proxy_and_runtime_probe
- **Proxy path**: 고정 F59 score stream(점수 스트림) 위에서 pre-registered grid 전체를 train에서만 평가 → **density 5–10/day band(밀도 구간)** 에 가장 가깝고 PF가 가장 높은 조합 1개 선택. tie-break(동점 처리)는 사전 고정: `q90 → reentry_cd=2 → same_dir_cd=4 → max_hold=6`.
- **Read-only gate**: 그 1개만 validation/OOS에서 PF, DD, trades/day를 읽기. validation/OOS PF가 둘 다 `<1`이거나 density가 band 아래면 **MT5 없이 negative memory close(부정 기억 마감)**.
- **MT5 probe**: 위 gate를 통과한 **정확히 1 candidate** 만 probe. F59와 같은 symbol/timeframe/cost setting family(설정 계열) 유지.
- **Success criterion for keeping the question open**: MT5 validation/OOS **PF ≥ 1** 이고 density가 proxy 대비 크게 붕괴하지 않을 것. 아니면 `long_axis_friction_escape_or_negative_memory`를 negative memory로 닫기.
- **의도적으로 하지 말 것**: compressed secondary view, extra-cost sweep, q grid 확장, score-family repair.

---

**요약**: Frontier60은 goal rules(목표 규칙) 아래 **유효한 stage-open hypothesis(단계 개시 가설)** 입니다. F52/F59와 **완전 동일 반복은 아니지만**, envelope surface가 F52와 겹치므로 **locks 없이 구현하면 repeat로 붕괴**할 가능성이 큽니다. Codex는 위 locks를 packet(작업 묶음)에 먼저 박고, **train-only 1-select → read-only eligibility → single MT5 probe** 순서만 실행하는 것이 맞습니다.

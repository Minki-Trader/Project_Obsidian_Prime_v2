# Codex Agent and Skill Snapshot for Grok Consulting(그록 컨설팅용 코덱스 에이전트/스킬 스냅샷)

## Generation Metadata(생성 메타데이터)

generated_at_local(로컬 생성 시각): 2026-06-12T01:48:13+09:00
repo_root(저장소 루트): C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2
git_status(깃 상태): ## main...origin/main [ahead 1]
latest_commit(최근 커밋): 879a1711 docs: add research artifact spine status (연구 산출물 척추 상태 추가)
purpose(목적): Ask Grok Build for consulting on making this Codex workspace a smarter, user-tailored super-agent without adding unnecessary complexity.

## Observed Codex Collaboration Behavior(관찰된 코덱스 협업 방식)

- Codex reads repo truth first, then acts through shell/file tools and reports concise Korean updates.
- Codex uses repo-scoped skills when a task matches their descriptions, especially re-entry, artifact lineage, result judgment, runtime parity, and claim discipline.
- Codex is good at local verification: git status, path checks, ledger counts, and generated snapshot checks.
- Long external model calls through shell have timeout risk, so background jobs or split snapshots are more reliable.
- User wants Korean-first explanations, short but clear action/effect descriptions, and does not want fake certainty about operating promotion, runtime authority, or live readiness.
- User wants help that feels like a capable research co-pilot, not a pile of brittle rituals.

## Consulting Boundary(컨설팅 경계)

Grok should not propose complexity for its own sake. The desired outcome is fewer sharper rules, better routing, better defaults, clearer receipts, and a more user-tailored collaboration style.
This is consulting only. Grok should propose changes and priorities, not edit files.

### AGENTS.md

```text
# Project Obsidian Prime v2

## 핵심 의도(Core Intent, 핵심 의도)

이 작업공간은 FPMarkets `US100` `M5` 연구와 실행을 위한 깨끗한 프로젝트다.

Obsidian Prime의 개념(concept, 개념)과 브로커 심볼 계약(broker symbol contract, 브로커 심볼 계약)은 유지한다. 하지만 과거 승자(winner, 승자), 과거 승격 이력(promotion history, 승격 이력), 과거 단계 압력(stage pressure, 단계 압력)은 물려받지 않는다.

## 응답 규칙(Language Rule, 언어 규칙)

- 영어 표현(English expression, 영어 표현)을 쓸 때는 같은 문맥 안에 한국어 표기를 함께 쓴다.
- 행동(action, 행동)을 설명할 때는 그 행동의 효과(effect, 효과)도 같이 설명한다.
- 설명은 짧고 쉽게 쓴다.

## Codex 작업 생명주기(Codex Work Lifecycle, 코덱스 작업 생명주기)

작업(work, 작업)을 코드(code, 코드), 실험(experiment, 실험), 보고(report, 보고) 중 하나로만 고르지 않는다. 대부분의 작업은 하나의 work packet(작업 묶음) 안에서 설계(design, 설계), 코드 작성(code writing, 코드 작성), 실행(run, 실행), 근거 기록(evidence recording, 근거 기록), 결과 판정(result judgment, 결과 판정), 사용자 보고(user-facing report, 사용자 보고)를 함께 지난다.

작업 시작 시 `obsidian-session-intake(세션 인입)`는 현재 진실(current truth, 현재 진실), 브랜치/작업트리 적합성, 작업 성격(work family, 작업군) 후보만 좁게 잡는다. 그 다음 `obsidian-work-packet-router(작업 묶음 라우터)`는 `docs/agent_control/work_family_registry.yaml`에서 `primary_family(주 작업군)` 하나, `primary_skill(주 스킬)` 하나, 제한된 `support_skills(보조 스킬)`, `required_gates(필수 게이트)`를 선택한다.

효과(effect, 효과)는 스킬을 많이 붙인 것처럼 보이게 하지 않고, 실제로 선택한 스킬과 closeout(종료 기록)에 연결된 gate(게이트)만 완료 주장(completion claim, 완료 주장)의 근거로 쓰게 하는 것이다.

운영 라우팅(operating routing, 운영 라우팅)의 진실 원천(source of truth, 진실 원천)은 `docs/agent_control/work_family_registry.yaml`이다. 모든 non-trivial work packet(비사소 작업 묶음)은 `primary_family(주 작업군)` 하나와 `primary_skill(주 스킬)` 하나를 먼저 고른다. `support_skills(보조 스킬)`는 필요한 만큼만 붙이고, 완료 전에는 `required_gate_coverage_audit(필수 게이트 커버리지 감사)`로 work packet(작업 묶음)의 `required_gates(필수 게이트)`가 closeout(종료 기록)에 실제로 연결됐는지 확인한다.

효과(effect, 효과)는 Stage 5부터 미래 Stage 50+까지 작업 내용은 달라져도, 스킬 선택(skill selection, 스킬 선택), receipt(영수증), gate(게이트), claim boundary(주장 경계)가 같은 방식으로 작동하게 하는 것이다.

gate(게이트)가 실패하면 `docs/agent_control/self_correction_policy.yaml`의 기본값인 `plan_only` 흐름으로 실패 원인과 repair plan(수정 계획)을 먼저 남긴다. 자동 수정은 allowlist(허용 목록) 안의 packet/closeout 배선 보정으로만 제한하며, gate 완화, threshold 완화, test skip, runtime/model logic 변경은 금지한다.

## 가장 중요한 원칙(Non-Negotiable Principle, 양보 불가 원칙)

탐색(exploration, 탐색)에는 게이트(gate, 제한문)가 없다.

`Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 데이터 완전성(data completeness, 데이터 완전성)이나 문맥 상태(context quality, 문맥 품질)를 설명하는 라벨(label, 라벨)일 뿐이다.

제한(restriction, 제한)은 운영 의미(operational meaning, 운영 의미)를 주장할 때만 붙는다. 예를 들면 실거래(live use, 실거래), 런타임 권위(runtime authority, 런타임 권위), 운영 승격(operating promotion, 운영 승격)이다.

## 티어 쌍 작업(Paired Tier Work, 티어 쌍 작업)

Stage 10(10단계) 이후 알파 탐색(alpha exploration, 알파 탐색)은 `Tier A(티어 A)`와 `Tier B(티어 B)`를 항상 같은 작업 묶음(work packet, 작업 묶음)에서 함께 다룬다.

필수 기록(required records, 필수 기록)은 세 가지다.

- `Tier A separate(Tier A 분리)`
- `Tier B separate(Tier B 분리)`
- `Tier A+B combined(Tier A+B 합산)`

효과(effect, 효과)는 `Tier A(티어 A)`만 본 결과를 전체 알파 판독(alpha read, 알파 판독)처럼 과장하지 않고, `Tier B(티어 B)`의 부분 문맥 표본(partial-context sample, 부분 문맥 표본)이 같은 아이디어에서 무엇을 바꾸는지 함께 보게 하는 것이다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서 사용자가 `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)`을 의도하면, 위 세 기록은 각각 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 해석한다.

효과(effect, 효과)는 Tier A(티어 A)의 빈 구간을 Tier B(티어 B)가 실제로 메웠는지 기록하고, separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 combined result(합산 결과)로 오해하지 않게 하는 것이다.

`Tier B(티어 B)`나 합산 기록(combined record, 합산 기록)을 만들 수 없으면 생략하지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 적는다.

## 점진적 경화(Progressive Hardening, 점진적 경화)

- 초기 탐색(early exploration, 초기 탐색)은 빠진 근거를 이름 붙이면 시작할 수 있다.
- `promotion_candidate(승격 후보)`는 비교할 가치가 있다는 뜻이지, 운영선을 교체한다는 뜻이 아니다.
- `runtime_probe(런타임 탐침)`는 런타임을 관찰한다는 뜻이지, 런타임 권위가 닫혔다는 뜻이 아니다.
- `operating_promotion(운영 승격)`과 `runtime_authority(런타임 권위)`는 강한 근거가 필요하다.
- `promotion-ineligible(승격 부적격)`은 아이디어 사망(idea-dead, 아이디어 사망)이 아니다.

## 단계 규칙(Stage Rule, 단계 규칙)

프로젝트는 단계(stage, 단계)로 관리한다.

각 단계는 번호(number, 번호)와 짧은 부제(subtitle, 부제)를 함께 쓴다.

`NN_area__specific_question`

부제(subtitle, 부제)는 이번 단계의 질문(question, 질문)을 설명한다. 미래의 모든 알파(alpha, 알파)를 한 단계 안에 가두면 안 된다.

모델 학습(model training, 모델 학습)과 검증(validation, 검증)이 실제로 가능해지는 순간부터 알파 탐색(alpha research, 알파 탐색)을 시작할 수 있다. 고정된 단계 번호에 묶지 않는다.

## 알파 탐색 단계 규칙(Alpha Exploration Stage Rule, 알파 탐색 단계 규칙)

Stage 10(10단계)부터 알파 탐색(alpha exploration, 알파 탐색)이 닫히는 단계(stage, 단계)까지는 탐색 라벨(exploration label, 탐색 라벨)과 실행 번호(run number, 실행 번호) 규칙을 쓴다.

- 정식 단계 이름(canonical stage id, 정식 단계 ID)은 `NN_area__specific_question`을 유지한다.
- 탐색 라벨(exploration label, 탐색 라벨)은 `stageN_exploration_group__specific_detail`을 쓴다. 예: `stage10_Model__LGBM`.
- 실행 번호(run number, 실행 번호)는 `run01A`, `run01B`, `run01C`처럼 단계 로컬 순서 번호(stage-local sequence number, 단계 로컬 순서 번호)다.
- 실행 번호(run number, 실행 번호)는 탐색 상한(limit, 한계)이나 역할 고정(role lock, 역할 고정)이 아니다.
- 해당 단계(stage, 단계)는 핵심 주제(core topic, 핵심 주제)를 끝까지 학습(training, 학습), 최적화(optimization, 최적화), 압박 시험(stress test, 압박 시험)한 뒤 다음 단계(next stage, 다음 단계)로 간다.
- 알파 탐색 단계 전환(alpha exploration stage transition, 알파 탐색 단계 전환)은 기준선 선택(baseline selection, 기준선 선택)이 아니라 주제 전환(topic pivot, 주제 전환)이다. 명시적 승격/운영 작업 묶음(explicit promotion/operating packet, 명시적 승격/운영 작업 묶음)이 없으면 마감 단계(closeout stage, 마감 단계)에서 기준선(baseline, 기준선)을 만들지 않는다.

효과(effect, 효과)는 모든 새 작업 회차(pass, 회차)가 알파 탐색(alpha exploration, 알파 탐색)을 좁게 닫지 않고, 같은 단계(stage, 단계) 안에서 끝까지 밀어붙이게 하는 것이다.

## 티어 규칙(Tier Rule, 티어 규칙)

- `Tier A(티어 A)`: 전체 문맥 표본(full-context sample, 전체 문맥 표본)
- `Tier B(티어 B)`: 부분 문맥 표본(partial-context sample, 부분 문맥 표본)
- `Tier C(티어 C)`: 약한 표본(weak sample, 약한 표본) 또는 명시적으로 허용된 로컬 연구(local research, 로컬 연구)

모든 티어(tier, 티어)는 탐색할 수 있다. 보고서(report, 보고서)는 무엇을 탐색했는지만 정직하게 라벨링(labeling, 라벨링)하면 된다.

## 구조 불변 규칙(Architecture Invariants, 구조 불변 규칙)

`docs/policies/architecture_invariants.md`가 코드 배치(code placement, 코드 배치)와 경로 규칙(path rule, 경로 규칙)을 담당한다.

- 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)은 `foundation/features`에 둔다.
- 재사용 모델 로직(reusable model logic, 재사용 모델 로직)이 생기면 별도 소유 모듈(owner module, 소유 모듈)에 둔다.
- `foundation/pipelines`는 조율(orchestration, 조율)을 담당한다. 숨은 진실 원천(source of truth, 진실 원천)이 되면 안 된다.
- MT5 EA(`Expert Advisor`, 전문가 자문)는 얇은 진입점(thin entrypoint, 얇은 진입점)과 `foundation/mt5/include/ObsidianPrime/` 모듈(module, 모듈)로 나눈다.
- EA run variant(EA 실행 변형)는 새 `.mq5` 복제(copy, 복사)로 관리하지 않는다. 파라미터만 다르면 `.set` 파일과 `run_manifest.json(실행 목록)`으로 관리하고, 로직(logic, 로직)이 다르면 `.mqh` 모듈 버전(module version, 모듈 버전)을 올린다.
- `stages/*`는 단계 로컬 산출물(stage-local artifact, 단계 로컬 산출물), 보고서(report, 보고서), 실행 근거(run evidence, 실행 근거)를 담는다.

효과(effect, 효과)는 run별 차이(run-specific difference, 실행별 차이)가 코드 파일 이름만 늘리는 방식으로 숨지 않고, 설정(set, 설정), 모듈 해시(module hash, 모듈 해시), 모델/번들 해시(model/bundle hash, 모델/번들 해시), 테스터 출력(tester output, 테스터 출력)으로 추적되게 하는 것이다.

## 탐색 명령(Exploration Mandate, 탐색 명령)

`docs/policies/exploration_mandate.md`가 탐색 규율(exploration discipline, 탐색 규율)을 담당한다.

탐색은 아이디어를 자유롭게 만들고, 정직하게 시험하고, 실패를 기록하며, 운영 조심성(operating caution, 운영 조심성)이 아이디어 필터(idea filter, 아이디어 필터)가 되지 않게 하는 일이다.

## 실행 근거 시스템(Run Evidence System, 실행 근거 시스템)

`docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`가 실행 근거(run evidence, 실행 근거)를 담당한다.

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토된 실행(reviewed run, 검토된 실행)이 된다.

프로젝트 장부(project ledger, 프로젝트 장부)는 `docs/registers/alpha_run_ledger.csv`이고, 단계 장부(stage ledger, 단계 장부)는 `stages/<stage_id>/03_reviews/stage_run_ledger.csv`다.

효과(effect, 효과)는 run/subrun/view(실행/하위 실행/보기)를 한 줄씩 모아, Tier A 분리(Tier A separate, Tier A 분리), Tier B 분리(Tier B separate, Tier B 분리), Tier A+B 합산(Tier A+B combined, Tier A+B 합산), Tier A 우선 + Tier B 대체 라우팅(Tier A primary + Tier B fallback routing, Tier A 우선 + Tier B 대체 라우팅), MT5 런타임 탐침(MT5 runtime probe, MT5 런타임 탐침)을 같이 추적하게 하는 것이다.

## 외부 검증 지연 방지(External Verification Anti-Deferral, 외부 검증 지연 방지)

외부 검증(external verification, 외부 검증)이 필요한 주장(claim, 주장)은 다음 작업(next work, 다음 작업)으로 반복해서 밀 수 없다.

- MT5(`MetaTrader 5`, 메타트레이더5), 브로커 터미널(broker terminal, 브로커 터미널), 전략 테스터(strategy tester, 전략 테스터), 파일 인계(file handoff, 파일 인계), 런타임 동등성(runtime parity, 런타임 동등성)에 기대는 주장은 같은 작업 회차(pass, 회차)에서 가장 좁은 충분한 외부 검증(narrow sufficient external check, 좁은 충분 외부 검증)을 먼저 시도한다.
- 도구(tool, 도구), 스크립트(script, 스크립트), 설정(configuration, 설정), 실행 인계 파일(handoff file, 인계 파일)이 낡았거나 없으면 blocked(차단)로 닫기 전에 현재 프로젝트 기준으로 만들거나 고쳐서 실행을 먼저 시도한다.
- MT5 검증(MT5 verification, MT5 검증)에서 MetaEditor compile(메타에디터 컴파일)은 좁은 외부 검증(narrow external check, 좁은 외부 검증)의 일부일 수 있지만, MT5 snapshot(MT5 스냅샷), strategy tester output(전략 테스터 출력), terminal file output(터미널 파일 출력)을 대체하지 않는다.
- 외부 검증이 없으면 그 주장은 검토 완료(reviewed, 검토됨)나 긍정 판정(positive judgment, 긍정 판정)으로 닫지 않는다. 대신 범위를 낮춰 말하거나, 불충분(inconclusive, 불충분), 무효(invalid, 무효), 또는 차단(blocked, 차단)으로 적는다.
- 같은 빠진 외부 검증(missing external verification, 빠진 외부 검증)을 두 번 연속 next work(다음 작업)로만 남기지 않는다. 실행하거나, 현재 도구를 생성/수정해서 실행을 시도하거나, 사용자 행동(user action, 사용자 행동)이 필요한 정확한 terminal action(터미널 행동)을 요청하거나, 주장을 낮추거나, 차단 사유(blocker, 차단 사유)를 기록한다.
- blocked(차단) 판정은 복구 시도(recovery attempt, 복구 시도), 실행 명령(execution command, 실행 명령), 실패 로그(failure log, 실패 로그), 또는 필요한 사용자 행동(user action, 사용자 행동)을 남긴 뒤에만 쓴다.

## 현재 진실(Current Truth, 현재 진실)

- 현재 상태(current state, 현재 상태): `docs/workspace/workspace_state.yaml`
- 현재 설명(current narrative, 현재 설명): `docs/context/current_working_state.md`
- 재진입 순서(re-entry order, 재진입 순서): `docs/policies/reentry_order.md`
- 에이전트 라우팅(agent routing, 에이전트 라우팅): `docs/policies/agent_trigger_policy.md`

## 폴더 규칙(Folder Rules, 폴더 규칙)

- `docs/`: 계약(contract, 계약), 정책(policy, 정책), 현재 상태(current state, 현재 상태), 결정(decision, 결정), 등록부(register, 등록부), 템플릿(template, 템플릿)
- `data/`: 원천 데이터(raw data, 원천 데이터)와 처리 데이터(processed data, 처리 데이터)
- `foundation/`: 재사용 코드(reusable code, 재사용 코드)와 공유 도구(shared tools, 공유 도구)
- `stage_pipelines/`: 단계별 실행 어댑터(stage-specific execution adapter, 단계 전용 실행 어댑터). `foundation/pipelines`의 legacy shim(호환 진입점) 뒤 실제 stage-local orchestration(단계 로컬 실행 지휘)을 둔다. 재사용 모델/피처/런타임 로직(reusable model/feature/runtime logic, 재사용 로직)의 장기 소유자가 되면 안 된다.
- `stages/`: 번호가 붙은 단계 작업(numbered stage work, 번호 단계 작업)
- `tests/`: 재사용 코드 테스트(test, 테스트)
- `.agents/skills/`: 저장소 전용 에이전트 스킬(repo-scoped agent skills, 저장소 전용 에이전트 스킬)

최상위 임시 폴더(scratch folder, 임시 폴더)는 만들지 않는다.

## 인코딩 규칙(Encoding Rule, 인코딩 규칙)

한국어 `.md`와 `.txt` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 유지한다.
```

### docs\workspace\workspace_state.yaml

```text
current_stage_id: 364_source_regime_label_pivot__dense_cost_recovery
current_run_id: run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1
latest_completed_run_id: run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1
current_status: completed_stage364HR_trade_quality_density_repair_scout_no_strict_joint_pass_review_required_no_authority
current_judgment: negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues_review_required_no_authority
next_run_id: run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: 2026-06-10T12:51:22Z
```

### docs\context\current_working_state.md

```text
# Current Working State(현재 작업 상태)

Updated(갱신): 2026-06-10T12:51:22Z

Active stage(활성 단계): `364_source_regime_label_pivot__dense_cost_recovery`

Latest completed run(최근 완료 실행): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`

Current run(현재 실행): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`

Current truth(현재 진실): `run364HR` completed(완료) a trade-quality density repair proxy replay scout(거래 품질 밀도 수리 프록시 재생 탐색). strict_joint_pass_count(엄격 동시 통과 수)는 `0`입니다.

Best clue(최선 단서): `hold4_margin_0.01` net/PF/density(순수익/수익 팩터/밀도)는 `462.0071630903` / `1.2257899553` / `2.1178343949`입니다. 효과는 품질을 고치면 밀도가 떨어지고, 밀도를 고치면 PF(수익 팩터)가 약한 실패 경계를 분리한 것입니다.

Next action(다음 행동): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`에서 selected clues(선택 단서), strict failure boundary(엄격 실패 경계), and package eligibility(패키지 가능성)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
```

### docs\policies\reentry_order.md

```text
# Re-entry Order

이 문서는 프로젝트에 다시 들어올 때 읽는 순서(re-entry order, 재진입 순서)를 정한다.

목적은 오래된 단계 드리프트(stage drift, 단계 드리프트)를 다시 살리지 않는 것이다.

## 읽는 순서(Read Order, 읽는 순서)

1. `AGENTS.md`
2. `docs/workspace/workspace_state.yaml`
3. `docs/context/current_working_state.md`
4. `docs/registers/alpha_run_ledger.csv`
5. 활성 단계(active stage, 활성 단계) `03_reviews/stage_run_ledger.csv`
6. `docs/workspace/pre_alpha_stage_plan.md`
7. 활성 단계(active stage, 활성 단계) `04_selected/selection_status.md`
8. 활성 단계(active stage, 활성 단계) `00_spec/stage_brief.md`
9. `docs/policies/stage_structure.md`
10. `docs/policies/exploration_mandate.md`
11. `docs/policies/architecture_invariants.md`
12. `docs/policies/kpi_measurement_standard.md`
13. `docs/policies/run_result_management.md`
14. `docs/policies/result_judgment_policy.md`
15. `docs/policies/agent_trigger_policy.md`
16. `docs/contracts/time_axis_policy_fpmarkets_v2.md`
17. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
18. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
19. `docs/contracts/training_label_split_contract_fpmarkets_v2.md`
20. `docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md`
21. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## 진실 우선순위(Truth Precedence, 진실 우선순위)

문서가 서로 다르면 다음 순서를 따른다.

1. `docs/workspace/workspace_state.yaml`
2. 활성 단계(active stage, 활성 단계) `04_selected/selection_status.md`
3. `docs/context/current_working_state.md`
4. `AGENTS.md`
5. 정책 문서(policy docs, 정책 문서)
6. 계약 문서(contract docs, 계약 문서)
7. 단계 노트(stage notes, 단계 노트)와 보고서(reports, 보고서)

## 재시작 경계(Restart Boundary, 재시작 경계)

오래된 Stage 00부터 Stage 07까지의 흐름은 현재 진실(current truth, 현재 진실)이 아니다. 과거 추적 이력(prior tracked history, 과거 추적 이력)일 뿐이다.

탐색(exploration, 탐색)을 진행할 수 있는지 판단할 때 오래된 방어 리뷰 문장(defensive review language, 방어 리뷰 문장)을 쓰지 않는다.

## 재진입 후 라우팅(After Re-entry Routing, 재진입 후 라우팅)

재진입(re-entry, 재진입)이 끝나면 작업을 단일 mode(모드)로 자르지 않는다. `obsidian-session-intake(세션 인입)`가 current truth(현재 진실)를 잡고, `obsidian-work-packet-router(작업 묶음 라우터)`가 code(코드), experiment(실험), verification(검증), evidence(근거), judgment(판정), report(보고)를 하나의 lifecycle(생명주기)로 배치한다.

효과(effect, 효과)는 코드 수정만 하고 끝내거나, 실험 결과를 전문 용어로만 보고하거나, 레퍼런스/재현성/산출물 계보 스킬을 방치하는 일을 줄이는 것이다.
```

### docs\policies\agent_trigger_policy.md

```text
# Agent Trigger Policy

이 문서는 저장소 전용 스킬(repo-scoped skills)을 언제 쓰는지 정한다.

핵심 원칙은 단순하다. 작업이 커져도, Stage 5부터 미래 Stage 50+까지 같은 방식으로 시작하고, 같은 방식으로 닫는다.

## 정책 참조(Policy References, 정책 참조)

이 정책(policy, 정책)은 다음 문서와 함께 작동한다.

- `docs/policies/architecture_invariants.md`
- `docs/policies/stage_structure.md`
- `docs/policies/exploration_mandate.md`
- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`

효과(effect, 효과)는 skill routing(스킬 배치)이 architecture(구조), exploration(탐색), KPI(핵심 성과 지표), run management(실행 관리), result judgment(결과 판정) 규칙과 끊기지 않게 하는 것이다.

## 운영 커널

모든 non-trivial work packet(비사소 작업 묶음)은 다음 순서를 따른다.

1. 현재 진실(current truth)과 브랜치/작업트리 적합성을 확인한다.
2. `docs/agent_control/work_family_registry.yaml`에서 `primary_family`를 하나 고른다.
3. 그 family의 `primary_skill`을 하나만 고른다.
4. 필요한 경우에만 `support_skills`를 붙인다.
5. `required_gates`를 work packet과 closeout에 연결한다.
6. 완료/검증/검토 주장은 `required_gate_coverage_audit`와 claim guard가 통과한 뒤에만 쓴다.

이 규칙의 효과는 스킬을 줄이는 것이 아니라, 필요한 스킬이 조언 문서로 흐르지 않고 실행 계약으로 작동하게 만드는 것이다.

## 라우팅 소스

라우팅의 진실 원천(source of truth)은 `docs/agent_control/work_family_registry.yaml`이다.

각 family는 반드시 다음을 가진다.

- `primary_skill`: 작업을 대표하는 스킬 1개
- `support_skills`: primary를 보조하는 제한된 스킬 목록
- `required_skills`: receipt가 필요한 전체 스킬 목록
- `required_gates`: closeout 전에 실행되거나 명시적으로 N/A 처리되어야 하는 gate 목록

`primary_skill`은 항상 `required_skills`의 첫 번째 항목이어야 한다.

## Work Family 선택

작업군은 stage 번호가 아니라 작업 성격으로 고른다.

| work family | primary_skill | 쓰는 때 |
| --- | --- | --- |
| `information_only` | `obsidian-answer-clarity` | 읽기, 설명, 상태 요약 |
| `state_sync` | `obsidian-stage-transition` | 현재 진실, active stage, current run, 브랜치/상태 동기화 |
| `policy_skill_governance` | `obsidian-work-packet-router` | `AGENTS.md`, policy, skill, control-plane 계약 변경 |
| `code_edit` | `obsidian-code-surface-guard` | 일반 코드 수정 |
| `code_refactor` | `obsidian-code-surface-guard` | 모듈 분리, 비대증 방지, owner module 이동 |
| `experiment_design` | `obsidian-experiment-design` | 실험 가설, baseline, 변수, 무효 조건 설계 |
| `experiment_execution` | `obsidian-run-evidence-system` | Python/model/variant 실행과 결과 근거 기록 |
| `runtime_backtest` | `obsidian-runtime-parity` | MT5, EA, `.mq5`, `.mqh`, `.set`, Strategy Tester, runtime handoff |
| `kpi_evidence` | `obsidian-run-evidence-system` | KPI, ledger, row grain, source authority, 결과 판정 |
| `artifact_lineage` | `obsidian-artifact-lineage` | artifact, hash, manifest, report 연결 |
| `cleanup_archive` | `obsidian-artifact-lineage` | 정리, 보관, 삭제, 이동 |
| `publish_handoff` | `obsidian-stage-transition` | PR, branch, handoff, stage closeout |

한 요청이 여러 성격을 가져도 `primary_family`는 하나만 고른다. 나머지는 support 또는 phase로 기록한다.

## Support Skill 규칙

Support skill은 작업을 보조한다. 작업을 다시 분류하지 않는다.

- 기본 support 한도는 `work_family_registry.yaml`의 `support_skill_limit_default`를 따른다.
- runtime이나 experiment처럼 진짜 복합 작업일 때만 family별 `support_skill_limit`을 쓴다.
- support로 선택한 스킬도 `required_skills`에 들어가야 하며, 완료 전에 receipt가 있어야 한다.
- 순수 내부 리팩터처럼 외부 API나 MT5 동작이 바뀌지 않는 경우 `obsidian-reference-scout`는 `not_required` 사유를 남길 수 있다.

## 스킬

- `obsidian-answer-clarity`: user-facing status(사용자 보고 상태), result report(결과 보고), completion report(완료 보고)를 쉽게 설명한다.
- `obsidian-architecture-guard`: architecture debt(구조 부채), code placement(코드 배치), Korean encoding(한국어 인코딩)을 지킨다.
- `obsidian-artifact-lineage`: artifact(산출물), manifest(목록), report(보고서), hash(해시), registry(등록부) 연결을 확인한다.
- `obsidian-backtest-forensics`: MT5 Strategy Tester(전략 테스터) report/settings/trade list(보고서/설정/거래 목록)를 검사한다.
- `obsidian-claim-discipline`: claim boundary(주장 경계)를 낮출 곳은 낮추고 promotion/runtime(승격/런타임) 과장을 막는다.
- `obsidian-code-quality`: 코드 책임(code responsibility, 코드 책임), 흐름(flow, 흐름), 테스트 의도(test intent, 테스트 의도)를 확인한다.
- `obsidian-code-surface-guard`: owner module(소유 모듈), caller(호출자), input/output contract(입출력 계약), monolith risk(일체형 위험)를 점검한다.
- `obsidian-data-integrity`: data source(데이터 원천), time axis(시간축), split(분할), leakage(누수)를 점검한다.
- `obsidian-environment-reproducibility`: dependency/runtime(의존성/런타임), clean checkout(깨끗한 체크아웃), local machine assumption(로컬 가정)을 확인한다.
- `obsidian-experiment-design`: hypothesis(가설), baseline(기준선), variables(변수), invalid conditions(무효 조건)을 설계한다.
- `obsidian-exploration-mandate`: exploration lane(탐색 레인), idea boundary(아이디어 경계), failure memory(실패 기억)를 지킨다.
- `obsidian-lane-classifier`: exploration/runtime/promotion lane(탐색/런타임/승격 레인)을 구분한다.
- `obsidian-model-validation`: model/threshold surface(모델/임계값 표면), split(분할), overfit(과적합), selection metric(선택 지표)을 점검한다.
- `obsidian-performance-attribution`: KPI change(KPI 변화)를 time/sample/tier/model/trade shape(시간/표본/티어/모델/거래 형태)로 분해한다.
- `obsidian-reentry-read`: current truth(현재 진실)와 active stage(활성 단계)를 재진입 순서대로 확인한다.
- `obsidian-reference-scout`: version-sensitive external reference(버전 민감 외부 참고자료)가 필요한지 확인한다.
- `obsidian-result-judgment`: positive/negative/inconclusive/invalid(긍정/부정/불충분/무효) 판정을 경계와 함께 정리한다.
- `obsidian-run-evidence-system`: run identity(실행 정체성), KPI(핵심 성과 지표), ledger row(장부 행), missing evidence(빠진 근거)를 관리한다.
- `obsidian-runtime-parity`: Python/MT5/runtime handoff(파이썬/MT5/런타임 인계) 동등성과 외부 검증을 다룬다.
- `obsidian-session-intake`: 작업 시작 때 current truth(현재 진실), branch/worktree fit(브랜치/작업트리 적합성), work family candidate(작업군 후보)를 좁힌다.
- `obsidian-stage-transition`: active stage(활성 단계), handoff(인계), closeout(마감), current run(현재 실행)을 같은 회차에 동기화한다.
- `obsidian-work-packet-router`: work family(작업군), primary skill(주 스킬), support skills(보조 스킬), required gates(필수 제한문)를 고른다.
- `obsidian-workflow-drift-guard`: blocker(차단 지점), missing material(빠진 재료), recovery action(복구 행동)을 정리한다.

## Receipt 규칙

스킬을 선택했다는 말은 receipt가 있다는 뜻이다.

`docs/agent_control/skill_receipt_schema.yaml`는 각 스킬별 필수 receipt 필드를 정한다.

완료 보고 전에는 다음이 맞아야 한다.

- work packet의 `skill_routing.primary_family`
- work packet의 `skill_routing.primary_skill`
- work packet의 `skill_routing.support_skills`
- work packet의 `skill_routing.required_skill_receipts`
- closeout의 실행 audit 목록
- `required_gate_coverage_audit` 결과

이 중 하나가 비면 `completed`, `reviewed`, `verified`, `runtime_authority`, `operating_promotion` 같은 주장은 금지한다.

## Skill Layer

스킬은 네 층으로 본다.

- Intake/router: `obsidian-session-intake`, `obsidian-work-packet-router`
- Domain skills: code, experiment, model, runtime, KPI, artifact, state sync
- Guard skills: claim discipline, workflow drift, environment reproducibility, reference scout
- Final report filter: `obsidian-answer-clarity`, `obsidian-claim-discipline`

모든 스킬을 매번 읽는 것이 목표가 아니다. 현재 family가 요구하는 스킬을 정확히 읽고, receipt로 증명하는 것이 목표다.

## Same-Pass Sync

단계 의미(stage meaning), active stage, current run, branch, artifact identity, run status가 바뀌면 같은 작업 회차(pass)에 관련 문서를 맞춘다.

주요 current truth 문서는 다음이다.

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- 활성 단계 `04_selected/selection_status.md`
- `docs/registers/run_registry.csv`
- 단계별 `03_reviews/stage_run_ledger.csv`

`workspace_state.active_branch`와 실제 git branch가 다르면 state sync는 완료될 수 없다.

## Hard Gate Rule

강한 게이트(hard gate)는 운영 의미에만 적용한다.

탐색(exploration)은 할 수 있다. 하지만 다음 주장은 gate 없이 닫지 않는다.

- 검증 완료
- 리뷰 완료
- 런타임 권위
- 운영 승격
- MT5 검증 완료
- full verification

탐색 아이디어가 promotion-ineligible이어도 아이디어가 죽었다는 뜻은 아니다.

## Policy Skill Settings

`AGENTS.md`, policy, skill, control-plane 파일을 바꾸는 작업은 `policy_skill_governance` family다.

필수 gate는 다음이다.

- `agent_control_contracts`
- `ops_instruction_audit`
- `work_packet_schema_lint`
- `skill_receipt_schema_lint`

이 효과는 스킬/정책을 더 추가하기 전에 운영 라우터 자체가 안정적인지 먼저 막는 것이다.
```

### docs\policies\architecture_invariants.md

```text
# Architecture Invariants

코드 소유권(code ownership, 코드 소유권)을 단순하게 유지한다.

## 소유권(Ownership, 소유권)

- `foundation/features`: 재사용 피처 로직(reusable feature logic, 재사용 피처 로직)
- `foundation/pipelines`: 공통 데이터 물질화(materialization, 물질화)와 legacy 호환 shim(호환 진입점)
- `stage_pipelines/stageXX`: 해당 Stage에만 고유한 실행 어댑터(stage-specific execution adapter, 단계 전용 실행 어댑터)
- `foundation/mt5`: MT5 실행(execution, 실행) 또는 검증(verification, 검증) 도구
- `foundation/parity`: Python과 MT5 비교(comparison, 비교) 도구
- `stages/*`: 단계 로컬 산출물(stage-local artifacts, 단계 로컬 산출물), 보고서(reports, 보고서), 결정(decisions, 결정)

`foundation/pipelines`와 `stage_pipelines`가 피처 정의(feature definition, 피처 정의)나 모델 로직(model logic, 모델 로직)의 숨은 진실 원천(source of truth, 진실 원천)이 되면 안 된다. `stage_pipelines/stageXX`는 각 stage의 실행 지휘실(execution room, 실행 지휘실)이지 공통 도구 창고(shared toolbox, 공통 도구 창고)가 아니다. 다른 stage에서 재사용할 로직은 `foundation/*` owner module(소유 모듈)로 끌어올린 뒤 사용한다.

## EA 모듈 경계(EA Module Boundary, EA 모듈 경계)

MT5 EA(`Expert Advisor`, 전문가 자문)는 얇은 진입점(thin entrypoint, 얇은 진입점)과 재사용 모듈(reusable module, 재사용 모듈)로 나눈다.

- `.mq5` 진입점(entrypoint, 진입점)은 `OnInit`, `OnTick`, `OnDeinit`, 입력값(input, 입력값), 파일 경로(file path, 파일 경로) 연결만 담당한다.
- 재사용 MQL5 모듈(reusable MQL5 module, 재사용 MQL5 모듈)은 `foundation/mt5/include/ObsidianPrime/` 아래에 둔다.
- 피처 입력(feature input, 피처 입력), 모델 런타임(model runtime, 모델 런타임), 의사결정 표면(decision surface, 의사결정 표면), 주문 연결(execution bridge, 실행 연결), 런타임 기록(runtime telemetry, 런타임 기록)은 서로 다른 모듈 경계(module boundary, 모듈 경계)를 가진다.
- 단계 로컬 EA(stage-local EA, 단계 로컬 EA)는 실험(probe, 탐침)에만 쓰고, 두 번 이상 재사용할 로직(logic, 로직)은 모듈로 끌어올린다.
- run별 차이(run-specific difference, 실행별 차이)가 파라미터(parameter, 파라미터)뿐이면 `.mq5`를 복제하지 않고 `.set` file(설정 파일), `run_manifest.json(실행 목록)`, KPI record(KPI 기록)에 남긴다.
- run별 차이(run-specific difference, 실행별 차이)가 decision surface(의사결정 표면), execution bridge(실행 연결), telemetry(기록), feature input(피처 입력)을 바꾸면 해당 `.mqh` 모듈(module, 모듈)의 버전(version, 버전)과 sha256 hash(해시)를 남긴다.
- `#property(프로그램 속성)`처럼 main `.mq5`에 있어야 하는 항목은 entrypoint(진입점)에 둔다. include file(포함 파일)에 숨기지 않는다.

효과(effect, 효과): EA 파일 하나가 계속 커지면서 입력 계약(input contract, 입력 계약), 실행 계약(execution contract, 실행 계약), 기록 계약(telemetry contract, 기록 계약)을 섞는 일을 막는다.

## EA 실행 변형 트리거(EA Run Variant Trigger, EA 실행 변형 트리거)

EA(`Expert Advisor`, 전문가 자문), Strategy Tester(전략 테스터), `.set` 설정(set file, 설정 파일), optimization pass(최적화 회차), runtime package(런타임 패키지), model bundle(모델 번들)을 건드리는 작업은 시작 전에 run variant boundary(실행 변형 경계)를 정한다.

필수 판정(required decision, 필수 판정):

- entrypoint unchanged + parameter change(진입점 유지 + 파라미터 변경): `.set`과 manifest(목록)만 새로 만든다.
- module change(모듈 변경): `.mqh` 모듈 버전(module version, 모듈 버전)을 올리고 module hash(모듈 해시)를 남긴다.
- entrypoint change(진입점 변경): lifecycle(생명주기), tester property(테스터 속성), file handoff(파일 인계)가 바뀌는 이유를 기록한다.
- new EA file(새 EA 파일): 기존 runner(실행기)와 모듈(module, 모듈)로 표현할 수 없는 이유가 있을 때만 만든다.

효과(effect, 효과): run01A/run01B 같은 실행(run, 실행)이 조금씩 달라도 code identity(코드 정체성), input identity(입력 정체성), tester identity(테스터 정체성)가 끊기지 않는다.

## 모델 산출물(Model Artifacts, 모델 산출물)

모델(model, 모델)은 재현 가능한 산출물(reproducible artifact, 재현 가능한 산출물)이나 동결된 파라미터/규격 묶음(frozen parameter/spec bundle, 동결 파라미터/규격 묶음)이 있을 때만 물질화(materialized, 물질화)되었다고 말한다.

확률표(probability table, 확률표)와 보고서(report, 보고서)는 근거(evidence, 근거)이지 모델 산출물(model artifact, 모델 산출물) 자체는 아니다.

## 경로 규칙(Path Rules, 경로 규칙)

문서(docs, 문서), 매니페스트(manifest, 목록), 등록부(register, 등록부), 테스트(test, 테스트) 안에서는 저장소 상대경로(repo-relative path, 저장소 상대경로)를 쓴다.

절대경로(absolute path, 절대경로)는 로컬 진단(local diagnostic, 로컬 진단), 사용자용 클릭 링크(clickable link, 클릭 링크), 외부 도구(external tool, 외부 도구), MT5 인계(MT5 handoff, MT5 인계)에만 쓴다.

## 인코딩(Encoding, 인코딩)

한국어 `.md`와 `.txt` 문서는 UTF-8 with BOM(UTF-8 BOM 포함)을 쓴다.
```

### docs\policies\exploration_mandate.md

```text
# Exploration Mandate

탐색(exploration, 탐색)은 아이디어를 시험하는 일이다. 운영 규칙(operating rule, 운영 규칙)에게 허가를 받는 일이 아니다.

## 핵심 규칙(Core Rule, 핵심 규칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색할 수 있다.

티어 라벨(tier label, 티어 라벨)은 표본(sample, 표본)을 설명한다. 아이디어(idea, 아이디어)를 승인하거나 거절하지 않는다.

## 점진적 경화(Progressive Hardening, 점진적 경화)

- 초기 탐색(early exploration, 초기 탐색)은 빠진 근거를 이름 붙이면 시작할 수 있다.
- `promotion_candidate(승격 후보)`는 승격 전에도 연구할 수 있다.
- `runtime_probe(런타임 탐침)`는 런타임 권위(runtime authority, 런타임 권위) 없이도 관찰할 수 있다.
- `operating_promotion(운영 승격)`과 `runtime_authority(런타임 권위)`는 강한 증거가 필요하다.
- `promotion-ineligible(승격 부적격)`은 아이디어 사망(idea-dead, 아이디어 사망)이 아니다.

## 알파 탐색 중 기준선 종료 금지(No Baseline Closure During Alpha Exploration, 알파 탐색 중 기준선 종료 금지)

알파 탐색(alpha exploration, 알파 탐색)의 closeout(마감)은 baseline(기준선)을 정하는 의식이 아니다.

단계(stage, 단계)가 알파 탐색 성격(exploratory alpha nature, 탐색적 알파 성격)을 갖고 있다면 다음 stage(다음 단계)로의 이동은 topic pivot(주제 전환)이다. 마감 단계(closing stage, 마감 단계)에서 standard run(표준 실행), operating reference(운영 기준), baseline(기준선)을 만들지 않는다.

허용되는 마감 표현(allowed closeout words, 허용 마감 표현)은 다음과 같다.

- seed surface(씨앗 표면)
- preserved clue(보존 단서)
- reference surface(참고 표면)
- negative memory(부정 기억)
- invalid setup(무효 설정)
- blocked retry condition(차단 재시도 조건)

금지되는 마감 표현(forbidden closeout words, 금지 마감 표현)은 별도 promotion/operating packet(승격/운영 작업 묶음) 없이 쓰지 않는다.

- selected baseline(선택 기준선)
- operating reference(운영 기준)
- promotion candidate(승격 후보)
- runtime authority(런타임 권위)

효과(effect, 효과): 탐색(exploration, 탐색)은 충분히 파되, 의미 없는 미세조정(meaningless micro-tuning, 의미 없는 미세조정)을 반복하지 않는다. 좋은 단서(clue, 단서)는 다음 주제(topic, 주제)의 씨앗(seed, 씨앗)이 될 수 있지만, 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.

## WFO

WFO(`walk-forward optimization`, 워크포워드 최적화)는 진지한 최적화(optimization, 최적화)의 기본 방식이다. 단일 구간 판독(single-window read, 단일 구간 판독)은 스카우트(scout, 탐색 판독)로 쓸 수 있지만 그렇게 표시해야 한다.

## 티어 사용(Tier Use, 티어 사용)

- `Tier A(티어 A)`: 전체 문맥 표본(full-context sample, 전체 문맥 표본)
- `Tier B(티어 B)`: 부분 문맥 표본(partial-context sample, 부분 문맥 표본)
- `Tier C(티어 C)`: 약한 표본(weak sample, 약한 표본) 또는 명시적으로 허용된 `tier_c_local_research(티어 C 로컬 연구)`

모든 티어(tier, 티어)는 뭔가를 가르칠 수 있다. 보고서(report, 보고서)는 무엇을 썼는지만 정직하게 적으면 된다.

## 티어 쌍 작업(Paired Tier Work, 티어 쌍 작업)

Stage 10(10단계) 이후 alpha exploration(알파 탐색)은 Tier A(티어 A)와 Tier B(티어 B)를 같은 작업 묶음(work packet, 작업 묶음)에서 함께 다룬다.

필수 기록(required records, 필수 기록)은 아래 세 가지다.

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산)

효과(effect, 효과): Tier A(티어 A)만 빠르게 본 결과가 전체 판독(overall read, 전체 판독)처럼 남지 않고, Tier B(티어 B)가 같은 아이디어(idea, 아이디어)에 어떤 영향을 주는지 같이 남는다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서 `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)`을 쓰면 위 세 기록은 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 적는다.

효과(effect, 효과): Tier B(티어 B)가 실제로 빈 구간을 메웠는지 기록하고, separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 combined read(합산 판독)로 말하지 않는다.

Tier B(티어 B)를 만들 수 없으면 생략하지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, `out_of_scope_by_claim(주장 범위 밖)` 중 하나로 적는다.

## 실패 기록(Failure Memory, 실패 기록)

아이디어가 실패하면 다음을 남긴다.

- 가설(hypothesis, 가설)
- 시도한 변형(variants tried, 시도한 변형)
- 실패 경계(failed boundary, 실패 경계)
- 실패 이유(why failed, 실패 이유)
- 회수 가치(salvage value, 회수 가치)
- 재개 조건(reopen condition, 재개 조건)
- 반복 금지 메모(do-not-repeat note, 반복 금지 메모)

부정 결과(negative result, 부정 결과)는 쓸모 있는 근거다. 무효 결과(invalid result, 무효 결과)는 깨진 가정이 고쳐질 때까지 해석하지 않는다.
```

### docs\policies\run_result_management.md

```text
# Run Result Management

실행(run, 실행)은 정체성(identity, 정체성)이 있어야 한다.

## 필수 개념(Required Ideas, 필수 개념)

- `run_manifest.json(실행 목록)`: 무엇을 어떤 입력으로 실행했는지
- `run_registry.csv(실행 등록부)`: 지속 실행 색인(durable run index, 지속 실행 색인)
- 출력 경로(output path, 출력 경로): 결과가 있는 곳
- 상태(status, 상태): planned, running, completed, reviewed, archived, invalid

## 규칙(Rule, 규칙)

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토됨(reviewed, 검토됨)이 된다.

## Run/Subrun Ledger(실행/하위 실행 장부)

알파 탐색(alpha exploration, 알파 탐색) 실행은 `run_registry.csv(실행 등록부)` 한 줄만으로 충분하지 않다.

필수 장부(required ledgers, 필수 장부):

- `docs/registers/run_registry.csv`: top-level run(상위 실행) 한 줄
- `docs/registers/alpha_run_ledger.csv`: run/subrun/view(실행/하위 실행/보기) 한 줄씩
- `stages/<stage_id>/03_reviews/stage_run_ledger.csv`: 해당 stage(단계) 내부의 run/subrun/view(실행/하위 실행/보기) 한 줄씩

`alpha_run_ledger.csv(알파 실행 장부)`와 stage-local ledger(단계 내부 장부)는 최소한 `run_id(실행 ID)`, `subrun_id(하위 실행 ID)`, `tier_scope(티어 범위)`, `record_view(기록 보기)`, `kpi_scope(KPI 범위)`, `status(상태)`, `judgment(판정)`, `path(경로)`를 가진다.

효과(effect, 효과)는 한 실행(run, 실행) 안의 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산), MT5 runtime probe(MT5 런타임 탐침) 같은 세부 판독을 한 줄씩 누적하는 것이다.

Stage 10(10단계) 이후 alpha run(알파 실행)은 Tier A/B paired records(티어 A/B 쌍 기록)가 없으면 완전한 reviewed run(검토 완료 실행)으로 닫지 않는다. 이미 닫힌 실행이 새 규칙보다 앞선 경우에는 `pre_pair_rule_requires_supplement(쌍 규칙 전 실행, 보강 필요)`로 표시한다.

Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) routed run(라우팅 실행)은 같은 필수 장부를 쓰되, MT5(`MetaTrader 5`, 메타트레이더5) 행을 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 적는다.

Tier B fallback(Tier B 대체) 행은 subtype breakdown(하위유형 분해)과 no_tier labelable rows(티어 없음 라벨 가능 행)를 guardrail KPI(가드레일 핵심 성과 지표)에 포함한다.

효과(effect, 효과)는 run/subrun/view(실행/하위 실행/보기) 구조를 유지하면서도, combined record(합산 기록)가 separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)인지 실제 라우팅 전체인지 헷갈리지 않게 하는 것이다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

실행(run, 실행)이 외부 환경(external environment, 외부 환경)에 기대는 주장을 만들면, `run_manifest.json(실행 목록)` 또는 검토 문서(review document, 검토 문서)에 외부 검증 상태(external verification status, 외부 검증 상태)를 적는다.

허용 상태(allowed states, 허용 상태)는 다음 중 하나다.

- `not_applicable(해당 없음)`: 외부 환경이 이 주장에 필요 없다.
- `completed(완료)`: 좁은 충분 검증(narrow sufficient check, 좁은 충분 검증)을 실행했다.
- `blocked(차단)`: 시도했지만 환경, 권한, 데이터, 도구 문제로 막혔다.
- `out_of_scope_by_claim(주장 범위 밖)`: 이번 주장을 낮춰서 외부 검증이 필요 없게 만들었다.

`blocked(차단)`나 `out_of_scope_by_claim(주장 범위 밖)`은 다음 작업(next work, 다음 작업)이 될 수 있지만, 같은 빠진 검증(missing check, 빠진 검증)을 반복해서 검토 완료(reviewed, 검토됨) 근거처럼 쓰면 안 된다.
```

### docs\policies\result_judgment_policy.md

```text
# Result Judgment Policy

## 판정(Judgment Classes, 판정 분류)

- `positive(긍정)`: 계속 밀어볼 가치가 있는 결과
- `negative(부정)`: 가설을 약화하거나 닫는 유효한 결과
- `inconclusive(불충분)`: 근거가 부족한 결과
- `invalid(무효)`: 설정(setup, 설정), 데이터(data, 데이터), 가정(assumption, 가정)이 깨진 결과

## 규칙(Rule, 규칙)

`negative(부정)`은 재사용 가능한 근거(reusable evidence, 재사용 근거)다.

`invalid(무효)`는 깨진 부분(broken part, 깨진 부분)이 고쳐질 때까지 해석하지 않는다.

외부 검증(external verification, 외부 검증)이 필요한 주장(claim, 주장)에 외부 검증이 빠졌다면 그 주장은 `positive(긍정)`로 닫지 않는다.

- 검증을 시도할 수 있었는데 안 했다면 `inconclusive(불충분)`로 둔다.
- 검증을 시도했지만 환경이나 설정이 깨졌다면 `invalid(무효)` 또는 `blocked(차단)`로 둔다.
- 주장을 낮춰서 외부 검증이 필요 없는 범위만 말한다면, 낮춘 범위(scope, 범위)를 명시한다.

## 경계 어휘(Boundary Vocabulary, 경계 어휘)

결과 판정(result judgment, 결과 판정)은 탐색 경계(exploration boundary, 탐색 경계)를 같이 적어야 한다.

- `promotion_candidate(승격 후보)`: 비교할 수 있지만 운영 승격은 아닌 결과
- `operating_promotion(운영 승격)`: 운영선을 교체하거나 확인하는 결과
- `runtime_probe(런타임 탐침)`: 런타임을 관찰했지만 권위는 없는 결과
- `runtime_authority(런타임 권위)`: 런타임 권위를 주장하는 결과
```

### docs\policies\promotion_policy.md

```text
# Promotion Policy

탐색(exploration, 탐색)과 승격(promotion, 승격)은 다르다.

## 어휘(Vocabulary, 어휘)

- `promotion_candidate(승격 후보)`: 운영선 교체(incumbent replacement, 현행선 교체) 없이 연구할 후보
- `operating_promotion(운영 승격)`: 운영선을 교체하거나 확인한다는 주장
- `runtime_probe(런타임 탐침)`: 권위(authority, 권위) 없는 런타임 관찰
- `runtime_authority(런타임 권위)`: 런타임 동등성 폐쇄(runtime parity closure, 런타임 동등성 폐쇄), 번들 인계 권위(bundle handoff authority, 번들 인계 권위), 또는 실거래 유사 준비(live-like readiness, 실거래 유사 준비)

## 규칙(Rule, 규칙)

승격 게이트(promotion gate, 승격 게이트)는 운영 의미(operating meaning, 운영 의미)를 주장할 때만 적용한다.

탐색 결과(exploration result, 탐색 결과)는 승격할 수 없어도 흥미로울 수 있다.
```

### docs\agent_control\work_family_registry.yaml

```text
version: work_family_registry_v2
routing_contract:
  purpose: "Keep Codex behavior stable as stages and run families grow."
  rule: "Every non-trivial packet selects exactly one primary_family and one primary_skill before work starts."
  primary_skill_limit: 1
  support_skill_limit_default: 3
  max_required_skills_per_family: 5
  required_skill_order: "primary_skill first, then support_skills in execution order"
  closeout_rule: "Required skills must produce receipts, and required gates must appear in closeout before completed/reviewed/verified claims."
  stage_agnostic_rule: "Work families are reusable for Stage 5 through future Stage 50+ work; never create a family just for one stage number."
  common_final_filter:
    - obsidian-answer-clarity
    - obsidian-claim-discipline
  self_correction:
    policy: docs/agent_control/self_correction_policy.yaml
    default_mode: plan_only
    closeout_audit: self_correction_plan
    rule: "Failed gates are classified into a repair plan before any completion claim is repeated; automatic mutation may not relax gates, thresholds, tests, or claim boundaries."
families:
  information_only:
    description: "Read/explain only(?쎄린/?ㅻ챸 ?꾩슜 ?묒뾽)"
    mutation_default: false
    execution_default: false
    primary_skill: obsidian-answer-clarity
    support_skills:
      - obsidian-claim-discipline
    required_skills:
      - obsidian-answer-clarity
      - obsidian-claim-discipline
    required_gates:
      - final_claim_guard
  state_sync:
    description: "Current truth/state document sync(?꾩옱 吏꾩떎/?곹깭 臾몄꽌 ?숆린??"
    mutation_default: requires_decision_lock
    execution_default: false
    primary_skill: obsidian-stage-transition
    support_skills:
      - obsidian-reentry-read
      - obsidian-artifact-lineage
      - obsidian-claim-discipline
    required_skills:
      - obsidian-stage-transition
      - obsidian-reentry-read
      - obsidian-artifact-lineage
      - obsidian-claim-discipline
    required_gates:
      - state_sync_audit
      - final_claim_guard
  policy_skill_governance:
    description: "AGENTS/policy/skill/control contract governance(?먯씠?꾪듃/?뺤콉/?ㅽ궗/?쒖뼱 怨꾩빟 愿由?"
    mutation_default: requires_decision_lock
    execution_default: false
    primary_skill: obsidian-work-packet-router
    support_skills:
      - obsidian-architecture-guard
      - obsidian-claim-discipline
    required_skills:
      - obsidian-work-packet-router
      - obsidian-architecture-guard
      - obsidian-claim-discipline
    required_gates:
      - agent_control_contracts
      - ops_instruction_audit
      - work_packet_schema_lint
      - skill_receipt_schema_lint
  code_edit:
    description: "Code edit(肄붾뱶 ?섏젙)"
    mutation_default: true
    execution_default: false
    primary_skill: obsidian-code-surface-guard
    support_skills:
      - obsidian-code-quality
      - obsidian-reference-scout
    required_skills:
      - obsidian-code-surface-guard
      - obsidian-code-quality
      - obsidian-reference-scout
    required_gates:
      - code_surface_audit
      - test_gate
  code_refactor:
    description: "Code refactor/module split(肄붾뱶 由ы뙥??紐⑤뱢 遺꾨━)"
    mutation_default: requires_decision_lock
    execution_default: false
    primary_skill: obsidian-code-surface-guard
    support_skills:
      - obsidian-code-quality
      - obsidian-architecture-guard
      - obsidian-reference-scout
    required_skills:
      - obsidian-code-surface-guard
      - obsidian-code-quality
      - obsidian-architecture-guard
      - obsidian-reference-scout
    required_gates:
      - code_surface_audit
      - semantic_code_surface_audit
      - regression_test_gate
  experiment_design:
    description: "Experiment design(?ㅽ뿕 ?ㅺ퀎)"
    mutation_default: maybe
    execution_default: false
    primary_skill: obsidian-experiment-design
    support_skills:
      - obsidian-data-integrity
      - obsidian-model-validation
    required_skills:
      - obsidian-experiment-design
      - obsidian-data-integrity
      - obsidian-model-validation
    required_gates:
      - work_packet_schema_lint
  experiment_execution:
    description: "Python/model/variant experiment execution(?뚯씠??紐⑤뜽/蹂???ㅽ뿕 ?ㅽ뻾)"
    mutation_default: true
    execution_default: true
    support_skill_limit: 4
    primary_skill: obsidian-run-evidence-system
    support_skills:
      - obsidian-experiment-design
      - obsidian-data-integrity
      - obsidian-model-validation
      - obsidian-artifact-lineage
    required_skills:
      - obsidian-run-evidence-system
      - obsidian-experiment-design
      - obsidian-data-integrity
      - obsidian-model-validation
      - obsidian-artifact-lineage
    required_gates:
      - scope_completion_gate
      - kpi_contract_audit
      - skill_receipt_lint
      - required_gate_coverage_audit
  runtime_backtest:
    description: "MT5/runtime/backtest execution(MT5/?고???諛깊뀒?ㅽ듃 ?ㅽ뻾)"
    mutation_default: true
    execution_default: true
    support_skill_limit: 4
    primary_skill: obsidian-runtime-parity
    support_skills:
      - obsidian-backtest-forensics
      - obsidian-reference-scout
      - obsidian-run-evidence-system
      - obsidian-artifact-lineage
    required_skills:
      - obsidian-runtime-parity
      - obsidian-backtest-forensics
      - obsidian-reference-scout
      - obsidian-run-evidence-system
      - obsidian-artifact-lineage
    required_gates:
      - runtime_evidence_gate
      - scope_completion_gate
      - kpi_contract_audit
      - required_gate_coverage_audit
      - final_claim_guard
  kpi_evidence:
    description: "KPI/ledger/source authority evidence(KPI/?λ?/?먯쿇 沅뚯쐞 洹쇨굅)"
    mutation_default: requires_decision_lock
    execution_default: false
    primary_skill: obsidian-run-evidence-system
    support_skills:
      - obsidian-artifact-lineage
      - obsidian-result-judgment
      - obsidian-performance-attribution
    required_skills:
      - obsidian-run-evidence-system
      - obsidian-artifact-lineage
      - obsidian-result-judgment
      - obsidian-performance-attribution
    required_gates:
      - kpi_contract_audit
      - row_grain_audit
      - source_authority_audit
      - required_gate_coverage_audit
  artifact_lineage:
    description: "Artifact lineage/hash/report linking(?곗텧臾?怨꾨낫/?댁떆/蹂닿퀬 ?곌껐)"
    mutation_default: maybe
    execution_default: false
    primary_skill: obsidian-artifact-lineage
    support_skills:
      - obsidian-environment-reproducibility
    required_skills:
      - obsidian-artifact-lineage
      - obsidian-environment-reproducibility
    required_gates:
      - artifact_lineage_audit
  cleanup_archive:
    description: "Cleanup/archive/delete/move work(?뺣━/蹂닿?/??젣/?대룞 ?묒뾽)"
    mutation_default: requires_decision_lock
    execution_default: false
    primary_skill: obsidian-artifact-lineage
    support_skills:
      - obsidian-environment-reproducibility
      - obsidian-claim-discipline
    required_skills:
      - obsidian-artifact-lineage
      - obsidian-environment-reproducibility
      - obsidian-claim-discipline
    required_gates:
      - destructive_change_guard
      - archive_manifest_gate
  publish_handoff:
    description: "Publish/handoff/git sync work(寃뚯떆/?멸퀎/源??숆린???묒뾽)"
    mutation_default: requires_decision_lock
    execution_default: true
    primary_skill: obsidian-stage-transition
    support_skills:
      - obsidian-artifact-lineage
      - obsidian-claim-discipline
      - obsidian-answer-clarity
    required_skills:
      - obsidian-stage-transition
      - obsidian-artifact-lineage
      - obsidian-claim-discipline
      - obsidian-answer-clarity
    required_gates:
      - state_sync_audit
      - closeout_gate
      - required_gate_coverage_audit
      - final_claim_guard
```

### docs\agent_control\self_correction_policy.yaml

```text
version: self_correction_policy_v1
purpose: "Classify failed gates into repair plans without weakening the operating harness."
default_mode: plan_only
max_attempts: 2
same_failure_twice: human_decision_required
new_failure_after_repair: stop_and_report
modes:
  plan_only:
    mutates_files: false
    description: "Classify failures and write a repair plan. No file edits are made."
  safe_autofix:
    mutates_files: true
    description: "May apply only allowlisted low-risk packet or closeout wiring fixes."
  guarded_autofix:
    mutates_files: false
    description: "Writes patch proposals for code, policy, test, threshold, or runtime changes."
safe_autofix_allowlist:
  - add_missing_required_gate
  - attach_existing_audit_json_to_closeout
  - normalize_skills_not_used_reason
  - add_expected_packet_output
  - sync_closeout_report_gate_list
forbidden_actions:
  - remove_required_gate
  - relax_audit_threshold
  - edit_audit_result_to_pass
  - delete_or_skip_test
  - change_runtime_logic
  - change_model_result_judgment
  - lower_forbidden_claim_boundary
invariants:
  - "Self-correction may not reduce required gates, required skills, thresholds, or forbidden claims."
  - "Self-correction may not edit audit output files to turn a failing audit into pass."
  - "Runtime, model, test, and policy semantics require guarded proposals, not silent autofix."
  - "The default mode is plan_only; automatic mutation must be explicitly requested by a caller."
failure_taxonomy:
  missing_closeout_gate_execution:
    preferred_action: attach_existing_audit_json_to_closeout
    default_repair_mode: safe_autofix
  missing_required_gate_declaration:
    preferred_action: add_missing_required_gate
    default_repair_mode: safe_autofix
  missing_skill_receipt:
    preferred_action: add_or_fix_skill_receipt
    default_repair_mode: guarded_autofix
  schema_invalid:
    preferred_action: fix_schema_or_packet_shape
    default_repair_mode: guarded_autofix
  state_sync_mismatch:
    preferred_action: sync_current_truth_or_block_merge
    default_repair_mode: guarded_autofix
  code_surface_violation:
    preferred_action: split_large_module_or_move_owner_logic
    default_repair_mode: guarded_autofix
  final_claim_blocked:
    preferred_action: withhold_completion_claim_until_source_audits_pass
    default_repair_mode: plan_only
  test_failure:
    preferred_action: fix_behavior_or_test_contract
    default_repair_mode: guarded_autofix
  human_decision_required:
    preferred_action: stop_and_request_decision
    default_repair_mode: plan_only
```

### docs\agent_control\codex_operating_format.yaml

```text
version: codex_operating_format_v1
purpose: "Define the project-wide operating lifecycle for non-trivial Codex work."
compatibility:
  extends:
    - docs/policies/agent_trigger_policy.md
    - docs/policies/run_result_management.md
    - docs/policies/kpi_measurement_standard.md
    - docs/policies/result_judgment_policy.md
    - docs/policies/architecture_invariants.md
  does_not_replace:
    - docs/registers/run_registry.csv
    - docs/registers/alpha_run_ledger.csv
    - stages/<stage_id>/03_reviews/stage_run_ledger.csv
lifecycle:
  - phase: intake
    required_outputs:
      - current_truth_reference
      - user_quote
      - prompt_risk_scan
      - preflight_clarification_result
    effect: "Fix the user request before any silent scope reduction can happen."
  - phase: work_packet
    required_outputs:
      - work_packet.yaml
      - primary_family
      - primary_skill
      - support_skills
      - required_skill_receipts
      - required_gates
      - acceptance_criteria
      - scope_reduction_policy
      - forbidden_claims
    effect: "Turn the request into a checkable contract derived from work_family_registry.yaml."
  - phase: run_plan
    required_when:
      - experiment_execution
      - runtime_backtest
      - kpi_evidence
      - artifact_lineage
    required_outputs:
      - run_plan.yaml
      - row_grain_contract
      - kpi_source_authority
      - artifact_contract
    effect: "Fix what will be run, what will be measured, and where evidence must come from."
  - phase: code_surface_precheck
    required_when:
      - code_or_policy_edit
      - MT5_EA_or_module_edit
      - large_pipeline_edit
      - reusable_logic_move
    required_outputs:
      - code_surface_audit_result
      - owner_module_decision
      - caller_and_artifact_effect
      - monolith_risk
    gate_command: "python -m foundation.control_plane.code_surface_audit --root ."
    effect: "Catch folder placement, direct cross-owner imports, and monolith growth before more code is added."
  - phase: execution
    required_outputs:
      - source_artifacts
      - machine_readable_records
      - human_readable_reports
    effect: "Separate raw evidence, machine records, and user-facing explanation."
  - phase: closeout
    required_outputs:
      - skill_receipts
      - gate_result.json
      - required_gate_coverage_audit
      - self_correction_plan
      - final_claim_guard
      - closeout_report
    effect: "Forbid unsupported completed, verified, promotion, or runtime-authority claims."
artifact_roles:
  raw_evidence:
    examples:
      - mt5/reports/*.htm
      - predictions/*.parquet
      - results/*.csv
      - external telemetry csv
    rule: "Raw evidence proves what actually ran."
  machine_readable:
    examples:
      - work_packet.yaml
      - run_plan.yaml
      - run_manifest.json
      - kpi_record.normalized.json
      - summary.json
      - gate_result.json
      - skill_receipts/*.yaml
    rule: "Machine records are used by gates and audits."
  human_readable:
    examples:
      - reports/result_summary.md
      - closeout_report.md
      - stages/<stage_id>/03_reviews/*packet.md
      - docs/context/current_working_state.md
    rule: "Human reports must not contradict machine records."
completion_rule:
  completed_requires:
    - all_acceptance_criteria_passed
    - required_skill_receipts_executed
    - required_gates_executed_or_not_applicable_with_reason
    - failed_gates_have_self_correction_plan_or_no_failures
    - kpi_contract_passed_or_not_applicable_with_reason
    - artifact_lineage_connected_or_bounded
    - final_claim_guard_passed
  blocked_requires_one_of:
    - recovery_attempt
    - execution_attempt
    - failure_log
    - required_user_action
    - claim_lowered_with_boundary
```

### docs\agent_control\skill_receipt_schema.yaml

```text
version: skill_receipt_schema_v2
description: "Required content for skill receipts before completed/reviewed/verified claims are allowed."
schemas:
  default:
    required_fields:
      - packet_id
      - skill
      - status
      - primary_output
      - evidence_used
  obsidian-session-intake:
    required_fields:
      - packet_id
      - skill
      - status
      - intake_context
      - active_stage
      - branch_worktree_fit
      - selected_work_family
      - routing_handoff
  obsidian-work-packet-router:
    required_fields:
      - packet_id
      - skill
      - status
      - primary_family
      - primary_skill
      - support_skills
      - required_gates
      - skills_not_used
      - routing_reason
  obsidian-workflow-drift-guard:
    required_fields:
      - packet_id
      - skill
      - status
      - product
      - material_state
      - tool_state
      - environment_state
      - current_blocker
      - recovery_attempt_or_reason
  obsidian-reentry-read:
    required_fields:
      - packet_id
      - skill
      - status
      - source_current_truth_docs
      - active_stage
      - current_run
      - detected_conflicts
      - allowed_claims
      - forbidden_claims
  obsidian-stage-transition:
    required_fields:
      - packet_id
      - skill
      - status
      - source_current_truth_docs
      - changed_or_checked_docs
      - detected_conflicts
      - canonical_state_after
      - allowed_claims
      - forbidden_claims
  obsidian-architecture-guard:
    required_fields:
      - packet_id
      - skill
      - status
      - touched_surfaces
      - invariant_checks
      - placement_boundary
      - architecture_debt_effect
      - allowed_claims
      - forbidden_claims
  obsidian-code-surface-guard:
    required_fields:
      - packet_id
      - skill
      - status
      - owner_module
      - caller
      - input_contract
      - output_contract
      - artifact_or_report_effect
      - monolith_risk
      - placement_decision
  obsidian-code-quality:
    required_fields:
      - packet_id
      - skill
      - status
      - responsibilities_checked
      - flow_contract_checked
      - test_intent
      - residual_quality_risk
  obsidian-reference-scout:
    required_fields:
      - packet_id
      - skill
      - status
      - reference_need
      - sources_checked_or_not_required_reason
      - version_sensitive_surface
      - implementation_effect
  obsidian-experiment-design:
    required_fields:
      - packet_id
      - skill
      - status
      - hypothesis
      - baseline
      - changed_variables
      - invalid_conditions
      - evidence_plan
  obsidian-data-integrity:
    required_fields:
      - packet_id
      - skill
      - status
      - data_sources_checked
      - time_axis_boundary
      - split_boundary
      - leakage_checks
      - missing_data_boundary
  obsidian-model-validation:
    required_fields:
      - packet_id
      - skill
      - status
      - model_or_threshold_surface
      - validation_split
      - overfit_checks
      - selection_metric_boundary
      - allowed_claims
      - forbidden_claims
  obsidian-runtime-parity:
    required_fields:
      - packet_id
      - skill
      - status
      - python_artifact
      - runtime_artifact
      - compared_surface
      - parity_level
      - tester_identity
      - missing_evidence
      - allowed_claims
      - forbidden_claims
  obsidian-backtest-forensics:
    required_fields:
      - packet_id
      - skill
      - status
      - tester_report
      - tester_settings
      - spread_commission_slippage
      - trade_list_identity
      - forensic_gaps
  obsidian-run-evidence-system:
    required_fields:
      - packet_id
      - skill
      - status
      - source_inputs
      - produced_artifacts
      - ledger_rows
      - missing_evidence
      - allowed_claims
      - forbidden_claims
  obsidian-artifact-lineage:
    required_fields:
      - packet_id
      - skill
      - status
      - source_inputs
      - produced_artifacts
      - raw_evidence
      - machine_readable
      - human_readable
      - hashes_or_missing_reasons
      - lineage_boundary
  obsidian-environment-reproducibility:
    required_fields:
      - packet_id
      - skill
      - status
      - environment_assumptions
      - dependency_or_runtime_surface
      - clean_checkout_boundary
      - reproducibility_gaps
  obsidian-result-judgment:
    required_fields:
      - packet_id
      - skill
      - status
      - judgment_boundary
      - allowed_claims
      - forbidden_claims
      - evidence_used
  obsidian-performance-attribution:
    required_fields:
      - packet_id
      - skill
      - status
      - attribution_layers_checked
      - missing_layers
      - allowed_claims
      - forbidden_claims
  obsidian-exploration-mandate:
    required_fields:
      - packet_id
      - skill
      - status
      - exploration_lane
      - idea_boundary
      - negative_memory_effect
      - operating_claim_boundary
  obsidian-lane-classifier:
    required_fields:
      - packet_id
      - skill
      - status
      - selected_lane
      - rejected_lanes
      - gate_boundary
      - claim_boundary
  obsidian-claim-discipline:
    required_fields:
      - packet_id
      - skill
      - status
      - requested_claims
      - allowed_claims
      - forbidden_claims
      - final_status
  obsidian-answer-clarity:
    required_fields:
      - packet_id
      - skill
      - status
      - plain_conclusion
      - confirmed
      - not_yet_confirmed
      - why_it_matters
      - next_action
      - forbidden_claims_avoided
```

### docs\agent_control\work_packet.schema.yaml

```text
version: work_packet_schema_v2_compatible
compatibility:
  accepts_v1_packets: true
  accepts_v2_packets: true
required_top_level:
  - packet_id
  - created_at_utc
  - user_request
  - current_truth
  - preflight
  - interpreted_scope
  - acceptance_criteria
  - row_grain
  - kpi_contract
  - artifact_contract
  - skill_routing
  - gates
  - final_claim_policy
v2_required_top_level:
  - packet_id
  - created_at_utc
  - user_request
  - current_truth
  - work_classification
  - risk_vector_scan
  - decision_lock
  - interpreted_scope
  - acceptance_criteria
  - work_plan
  - skill_routing
  - evidence_contract
  - gates
  - final_claim_policy
v2_interpreted_scope_required_fields:
  - work_families
  - target_surfaces
  - scope_units
  - execution_layers
  - mutation_policy
  - evidence_layers
  - reduction_policy
  - claim_boundary
scope_units_allowed:
  - file
  - document
  - stage
  - run
  - variant
  - code_module
  - kpi_row
  - ledger
  - artifact
  - report
  - policy
  - skill
execution_layers_allowed:
  - read_only
  - document_edit
  - code_edit
  - python_execution
  - mt5_execution
  - kpi_recording
  - ledger_update
  - archive
  - publish
fields:
  packet_id:
    required: true
    rule: "Stable id for this unit of work."
  user_request:
    required_fields:
      - user_quote
      - requested_action
      - requested_count
      - ambiguous_terms
  preflight:
    required_fields:
      - needs_clarification
      - selected_option_id
      - selected_option_user_quote
      - blocked_until_answer
    rule: "If needs_clarification is true, execution cannot start until selected_option_user_quote exists."
  interpreted_scope:
    required_fields:
      - variants_requested
      - verification_layers
      - mt5_required
      - top_k_reduction_allowed
      - scope_reduction_requires_user_quote
    v2_required_fields:
      - work_families
      - target_surfaces
      - scope_units
      - execution_layers
      - mutation_policy
      - evidence_layers
      - reduction_policy
      - claim_boundary
  work_classification:
    required_fields:
      - primary_family
      - detected_families
      - touched_surfaces
      - mutation_intent
      - execution_intent
  risk_vector_scan:
    required_fields:
      - risks
      - hard_stop_risks
      - required_decision_locks
      - required_gates
      - forbidden_claims
  decision_lock:
    required_fields:
      - mode
      - assumptions
      - questions
      - required_user_decisions
  work_plan:
    required_fields:
      - phases
      - expected_outputs
      - stop_conditions
  evidence_contract:
    required_fields:
      - raw_evidence
      - machine_readable
      - human_readable
  acceptance_criteria:
    item_required_fields:
      - id
      - text
      - expected_artifact
      - verification_method
      - required
  row_grain:
    reference: docs/agent_control/row_grain_contract.yaml
  kpi_contract:
    required_fields:
      - kpi_standard_version
      - normalized_record_path
      - source_authority_reference
      - n_a_reason_reference
  artifact_contract:
    required_fields:
      - raw_evidence
      - machine_readable
      - human_readable
      - external_artifacts
  skill_routing:
    required_fields:
      - primary_family
      - primary_skill
      - support_skills
      - skills_considered
      - skills_selected
      - skills_not_used
      - required_skill_receipts
      - required_gates
    rule: "Values must be derived from docs/agent_control/work_family_registry.yaml before implementation starts."
  gates:
    required_fields:
      - scope_completion_gate
      - skill_receipt_lint
      - kpi_contract_audit
      - artifact_lineage_audit
      - final_claim_guard
  final_claim_policy:
    required_fields:
      - allowed_claims
      - forbidden_claims
      - claim_vocabulary_reference
```

### docs\agent_control\claim_vocabulary.yaml

```text
version: claim_vocabulary_v1
claim_classes:
  completed:
    allowed_when:
      - all_acceptance_criteria_passed
      - all_required_gates_passed
      - no_blocking_findings
    forbidden_when:
      - scope_missing_without_user_quote
      - triggered_skill_receipt_missing
      - required_kpi_missing
  completed_reduced_scope:
    allowed_when:
      - explicit_user_scope_reduction_quote_exists
      - reduced_scope_artifacts_pass
      - full_scope_claims_forbidden
  partial:
    allowed_when:
      - some_required_artifacts_exist
      - at_least_one_required_artifact_missing
  blocked:
    allowed_when:
      - recovery_attempt_or_failure_log_exists
      - required_user_action_or_external_blocker_exists
  invalid:
    allowed_when:
      - setup_data_or_scope_mismatch_found
  verified:
    allowed_when:
      - requested_verification_layer_passed
      - source_authority_matches_claim
  runtime_probe:
    allowed_when:
      - mt5_or_runtime_observation_exists
      - runtime_authority_not_claimed
  runtime_authority:
    allowed_when:
      - runtime_authority_contract_passed
      - explicit_policy_allows_authority_claim
forbidden_substitutions:
  - "answer_clarity_cannot_replace_runtime_parity"
  - "claim_discipline_cannot_replace_missing_evidence"
  - "run_evidence_cannot_replace_artifact_lineage"
  - "python_structural_result_cannot_replace_mt5_result"
  - "top_k_probe_cannot_replace_full_scope_verification_without_user_quote"
```

### docs\agent_control\n_a_reason_registry.yaml

```text
version: n_a_reason_registry_v1
rule: "A missing KPI field must use an allowed n/a_reason instead of a blank value."
allowed_reasons:
  run_has_no_variant_layer:
    category: identity
    use_when: "The run has no variant concept, such as a single fixed run."
  split_not_applicable:
    category: identity
    use_when: "The record is not tied to train, validation, or OOS."
  not_applicable_for_split:
    category: identity
    use_when: "The field does not apply to the row's split or split-level view."
  tier_not_applicable:
    category: identity
    use_when: "The run does not use Tier A, Tier B, or Tier A+B views."
  route_role_not_applicable:
    category: identity
    use_when: "The row is not an MT5 routed or tier-only record."
  stage_inheritance_not_recorded:
    category: identity
    use_when: "The source artifact predates explicit Stage inheritance recording."
  threshold_not_recorded:
    category: identity
    use_when: "The source run did not persist a threshold value or method in this KPI layer."
  python_structural_only_no_mt5_report:
    category: mt5
    use_when: "The work explicitly stopped at Python structural evidence."
  mt5_report_missing:
    category: mt5
    use_when: "MT5 was required, but the Strategy Tester report is missing."
  mt5_not_requested_by_user_quote:
    category: mt5
    use_when: "The user explicitly excluded MT5 for this packet."
  metric_not_emitted_by_mt5:
    category: source
    use_when: "The MT5 report does not provide this metric directly."
  telemetry_missing:
    category: source
    use_when: "Required telemetry or trade log is unavailable."
  trade_telemetry_missing:
    category: source
    use_when: "Trade-level telemetry needed for MFE, MAE, or hold diagnostics is unavailable."
  runtime_telemetry_missing:
    category: source
    use_when: "Runtime summary needed for execution diagnostics is unavailable."
  python_signal_metric_missing:
    category: source
    use_when: "The Python-side signal metric is not present in the source KPI payload."
  equity_curve_missing:
    category: risk
    use_when: "Equity curve data is not available for duration or ulcer calculations."
  trade_list_missing:
    category: trade_diagnostics
    use_when: "Trade-level list is unavailable."
  mt5_deal_list_empty:
    category: trade_diagnostics
    use_when: "The MT5 deal list exists but contains no rows for the requested attribution view."
  no_long_trades:
    category: trade_diagnostics
    use_when: "No long trades exist, so long-side expectancy or shape metrics cannot be computed."
  no_short_trades:
    category: trade_diagnostics
    use_when: "No short trades exist, so short-side expectancy or shape metrics cannot be computed."
  gross_loss_is_zero:
    category: math
    use_when: "Profit factor denominator is zero."
  profit_attribution_not_separable_from_single_routed_account_path:
    category: math
    use_when: "A routed component row comes from one MT5 account path, so per-tier PnL cannot be separated."
  insufficient_trade_count:
    category: judgment
    use_when: "The metric exists but sample size is too small for the requested interpretation."
  source_artifact_missing:
    category: artifact
    use_when: "The required source artifact is absent."
  external_artifact_local_only:
    category: artifact
    use_when: "The artifact exists only in a local external path."
  blocked_missing_required_input:
    category: blocked
    use_when: "A required input is missing and the packet is blocked."
  invalid_scope_mismatch:
    category: invalid
    use_when: "The run used inputs or inheritance outside the requested scope."
forbidden_freeform_examples:
  - not needed
  - handled implicitly
  - covered elsewhere
  - future work
```

### docs\agent_control\risk_flag_registry.yaml

```text
version: risk_flag_registry_v1
risks:
  scope_ambiguous:
    meaning: "Scope/count/target is ambiguous(踰붿쐞/?섎웾/??곸씠 ?좊ℓ??"
    safe_default:
      - report_only_when_user_asked_for_explanation
  mutation_ambiguous:
    meaning: "File edit versus report-only is ambiguous(?뚯씪 ?섏젙?몄? 蹂닿퀬 ?꾩슜?몄? ?좊ℓ??"
    safe_default:
      - no_file_edit
  state_sync_risk:
    meaning: "Current truth documents can disagree(?꾩옱 吏꾩떎 臾몄꽌?쇰━ ?ㅻ? ???덉쓬)"
    required_gates:
      - state_sync_audit
    forbidden_claims_if_missing:
      - current_truth_synced
      - stage_transition_completed
  claim_boundary_risk:
    meaning: "Completion/verification/promotion wording can overstate evidence(?꾨즺/寃利??밴꺽 ?쒗쁽??洹쇨굅瑜?怨쇱옣?????덉쓬)"
    required_gates:
      - final_claim_guard
  skill_abandonment_risk:
    meaning: "Required skill can be skipped without receipt(?꾩닔 ?ㅽ궗???곸닔利??놁씠 鍮좎쭏 ???덉쓬)"
    required_gates:
      - skill_receipt_lint
      - skill_receipt_schema_lint
  ops_instruction_risk:
    meaning: "Routing policy can grow without one primary skill and checkable gates(?쇱슦???뺤콉??二??ㅽ궗怨?寃利?媛?ν븳 寃뚯씠???놁씠 而ㅼ쭏 ???덉쓬)"
    required_gates:
      - ops_instruction_audit
    forbidden_claims_if_missing:
      - ops_instructions_stable
  evidence_gap_risk:
    meaning: "Raw evidence, machine record, or human report can be missing(?먮낯 洹쇨굅/湲곌퀎 湲곕줉/?щ엺 蹂닿퀬媛 鍮좎쭏 ???덉쓬)"
    required_gates:
      - artifact_lineage_audit
  runtime_parity_risk:
    meaning: "Python and MT5/runtime meaning can diverge(?뚯씠?ш낵 MT5/?고????섎?媛 ?닿툔?????덉쓬)"
    required_skills:
      - obsidian-runtime-parity
      - obsidian-backtest-forensics
    forbidden_claims_if_missing:
      - runtime_verified
      - mt5_verification_complete
      - runtime_authority
  kpi_source_risk:
    meaning: "KPI source authority or row grain can drift(KPI ?먯쿇 沅뚯쐞?????⑥쐞媛 ?붾뱾由????덉쓬)"
    required_gates:
      - kpi_contract_audit
      - row_grain_audit
      - source_authority_audit
  code_surface_risk:
    meaning: "Code can land in the wrong owner module(肄붾뱶媛 ?섎せ???뚯쑀 紐⑤뱢???ㅼ뼱媛????덉쓬)"
    required_gates:
      - code_surface_audit
      - semantic_code_surface_audit
  destructive_change_risk:
    meaning: "Delete/overwrite/archive/reset can lose evidence(??젣/??뼱?곌린/蹂닿?/珥덇린?붽? 洹쇨굅瑜??껉쾶 ?????덉쓬)"
    required_user_quote: true
    required_gates:
      - destructive_change_guard
  unattended_autonomy_risk:
    meaning: "Unattended work can silently reduce scope(臾댁씤 ?묒뾽??紐곕옒 踰붿쐞瑜?以꾩씪 ???덉쓬)"
    required:
      - explicit_completion_conditions
      - explicit_blocked_conditions
      - scope_completion_gate
  answer_clarity_risk:
    meaning: "Technical wording can hide the plain meaning(?꾨Ц ?⑹뼱媛 ?ъ슫 ?섎?瑜??④만 ???덉쓬)"
    required_skills:
      - obsidian-answer-clarity
      - obsidian-claim-discipline
```

### docs\agent_control\surface_registry.yaml

```text
version: surface_registry_v1
surfaces:
  docs_current_truth:
    paths:
      - docs/workspace/workspace_state.yaml
      - docs/context/current_working_state.md
      - stages/*/04_selected/selection_status.md
      - stages/*/00_spec/stage_brief.md
    risks:
      - state_sync_risk
      - claim_boundary_risk
    gates:
      - state_sync_audit
  policies_and_skills:
    paths:
      - AGENTS.md
      - docs/policies/**
      - .agents/skills/**
      - docs/agent_control/**
    risks:
      - policy_drift_risk
      - skill_abandonment_risk
      - ops_instruction_risk
      - encoding_risk
    gates:
      - agent_control_contracts
      - ops_instruction_audit
      - architecture_guard
  foundation_code:
    paths:
      - foundation/**
    risks:
      - code_surface_risk
      - regression_risk
    gates:
      - code_surface_audit
      - test_gate
  pipelines:
    paths:
      - foundation/pipelines/**
      - stage_pipelines/**
    risks:
      - orchestration_owner_leak_risk
      - monolith_growth_risk
    gates:
      - semantic_code_surface_audit
  mt5_runtime:
    paths:
      - foundation/mt5/**
      - stages/*/02_runs/*/mt5/**
    risks:
      - runtime_parity_risk
      - backtest_forensics_risk
    gates:
      - runtime_evidence_gate
  kpi_ledgers:
    paths:
      - docs/registers/alpha_run_ledger.csv
      - docs/registers/run_registry.csv
      - stages/*/03_reviews/stage_run_ledger.csv
    risks:
      - kpi_row_grain_risk
      - source_authority_risk
    gates:
      - kpi_contract_audit
      - row_grain_audit
  run_artifacts:
    paths:
      - stages/*/02_runs/**
    risks:
      - artifact_lineage_risk
      - ignored_artifact_risk
    gates:
      - artifact_lineage_audit
```

### docs\agent_control\ops_instruction_audit_latest.json

```text
{
  "audit_name": "ops_instruction_audit",
  "status": "pass",
  "passed": true,
  "completed_forbidden": false,
  "findings": [],
  "counts": {
    "family_count": 12,
    "explicit_skill_schema_count": 23,
    "default_support_skill_limit": 3,
    "max_required_skills_per_family": 5
  },
  "allowed_claims": [
    "ops_instructions_stable"
  ],
  "forbidden_claims": []
}
```

### docs\agent_control\state_sync_audit_latest.json

```text
{
  "audit_name": "state_sync_audit",
  "status": "pass",
  "passed": true,
  "completed_forbidden": false,
  "findings": [],
  "counts": {
    "active_stage": "32_sequence_model__tcn_temporal_convolution_context",
    "workspace_active_branch": "main",
    "actual_git_branch": "main",
    "current_run_values": {
      "workspace_state": "run26D_torch_tcn_native_temporal_runtime_probe_v1",
      "current_working_state": "run26D_torch_tcn_native_temporal_runtime_probe_v1",
      "selection_status": "run26D_torch_tcn_native_temporal_runtime_probe_v1"
    },
    "stage_brief_boundary": "",
    "registry_has_current_run": true,
    "stage_ledger_has_current_run": true,
    "source_paths": {
      "workspace_state": "docs/workspace/workspace_state.yaml",
      "current_working_state": "docs/context/current_working_state.md",
      "selection_status": "stages/32_sequence_model__tcn_temporal_convolution_context/04_selected/selection_status.md",
      "stage_brief": "stages/32_sequence_model__tcn_temporal_convolution_context/00_spec/stage_brief.md",
      "run_registry": "docs/registers/run_registry.csv",
      "stage_ledger": "stages/32_sequence_model__tcn_temporal_convolution_context/03_reviews/stage_run_ledger.csv"
    }
  },
  "allowed_claims": [
    "current_truth_synced",
    "state_sync_completed"
  ],
  "forbidden_claims": []
}
```

### docs\agent_control\run_evidence_validator_latest.json

```text
{
  "audit_name": "run_evidence_validator",
  "status": "pass",
  "passed": true,
  "completed_forbidden": false,
  "findings": [],
  "counts": {
    "normalized_records": 448,
    "enriched_records": 508,
    "n_a_cells_checked": 79348,
    "row_grain_cells_checked": 1792,
    "ledger_rows_loaded": 714
  },
  "allowed_claims": [
    "evidence_records_consistent"
  ],
  "forbidden_claims": []
}
```

## Repo-Scoped Skills Full Text(저장소 스킬 전문)

skill_count(스킬 수): 23

### .agents\skills\obsidian-answer-clarity\SKILL.md

```text
---
name: obsidian-answer-clarity
description: Explain Project Obsidian Prime v2 work in plain, beginner-readable language without shrinking the substance. Strongly trigger for planning, proposed plans, result reports, completion reports, status summaries, reviews, PR explanations, decision notes, or any user-facing answer that contains project terms, trading terms, engineering terms, or agent-policy terms.
---

# Obsidian Answer Clarity

Use this skill whenever the answer is meant for the user, not only for another engineer.

Default assumption: the user should not need to ask a second time for a plain explanation. Every project report should be understandable to a smart beginner while keeping the technical meaning intact.

## Automatic Bundle

For user-facing status summary(상태 요약), result report(결과 보고), completion report(완료 보고), plan(계획), or review explanation(검토 설명), apply this skill after the technical skill and pair it with `obsidian-claim-discipline`.

Effect(효과): current meaning(현재 의미), not-yet-true boundary(아직 사실 아님 경계), and next action(다음 행동)을 쉽게 말하면서도 claim(주장)이 강해지지 않는다.

## Strong Triggers

This skill is mandatory, not optional, for:

- planning replies(plan, 계획), including proposed plan(제안 계획) and next-task plan(다음 작업 계획)
- result reports(결과 보고), completion reports(완료 보고), and status summaries(상태 요약)
- stage closeout(단계 종료), handoff(인계), run result(실행 결과), review finding(검토 발견사항), or failure report(실패 보고)
- answers after implementation(구현 후 답변), verification(검증), or file edits(파일 수정)
- run packaging, individual experiment closeout, KPI interpretation, artifact handoff, PR summary, or policy/skill review

If another skill produced a technical result, apply this skill last before answering the user.

## Purpose

Make the answer easy enough for a non-developer and trading non-specialist to follow, while keeping the full meaning.

Do not treat Korean parallel notation as explanation by itself. A term like `runtime_authority(런타임 권위)` still needs a plain meaning.

## Required Behavior

1. When using a specialist term, add the simple meaning near it.
2. Explain why the point matters.
3. Explain the effect on the project or the next decision.
4. Separate what is true now from what is not yet true.
5. Keep the answer complete; do not make it short by removing important reasoning.
6. Use a simple analogy when it makes the idea easier, but do not let the analogy replace the actual project meaning.
7. When explaining a finding, say:
   - what is wrong
   - why it can hurt the project
   - what a safe fix does

## Preferred Shape

For planning replies(plan, 계획):

- Start with the intended outcome in one plain sentence.
- Then name what will change and what will not change.
- Then name the verification/check that proves the plan worked.
- Then list exact files, runs, stages, or artifacts only when needed.

For result reports(결과 보고):

- Start with the result in one plain sentence.
- Explain the plain meaning before the dense technical details.
- Say what is true now.
- Say what is not yet true.
- Say why it matters for the next project decision.
- Name the next practical step.
- Then list exact files, runs, stages, artifacts, or tests only when they help the user act.

For run, experiment, package, or PR closeout:

- `Conclusion`: what changed or what the result means.
- `Plain meaning`: explain it as if the reader is new to coding and trading research.
- `Confirmed`: what the evidence now supports.
- `Not yet confirmed`: what must not be claimed yet.
- `Evidence`: commands, KPI, files, artifacts, hashes, or PR links when useful.
- `Next action`: the smallest useful follow-up.

## Do Not

- Do not answer with term pairs only, such as `runtime authority(런타임 권위)`, without a plain explanation.
- Do not hide uncertainty behind formal wording.
- Do not use a defensive phrase like "noted for future work" unless the missing work, blocker, and next condition are clear.
- Do not over-compress the answer when the user is asking for understanding.
- Do not lead user-facing result reports with a file inventory, command log, or test log.
- Do not bury the stage meaning behind implementation detail.
- Do not make the user ask "what does this mean?" after a normal completion report.
- Do not use a specialist term as the main explanation when a plain sentence can carry the meaning.

## Example Standard

Instead of:

`runtime_authority` is not closed.

Write:

`runtime_authority(런타임 권위)` is not closed. Plainly, this means the project has not yet proven that the live or MT5 runtime path can be trusted as an operating handoff. The effect is that we can still use the current artifact for research planning, but we should not describe it as ready for live-like operation.
```

### .agents\skills\obsidian-architecture-guard\SKILL.md

```text
---
name: obsidian-architecture-guard
description: Guard Project Obsidian Prime v2 against stage-agnostic architecture and code-surface drift. Use when work touches feature calculation, model training/export, pipeline materialization, artifact claims, architecture debt, code placement, path identity, Windows long-path handling, stage transitions, alpha search, repo-scoped skills, agent settings, or Korean BOM/encoding-sensitive docs.
---

# Obsidian Architecture Guard

Use this skill when a task can change architecture meaning (구조 의미), not only when a specific stage number is involved.

## Trigger Surface

Use this guard for work touching any of:

- feature calculation (피처 계산)
- model training or export (모델 학습 또는 내보내기)
- pipeline materialization (파이프라인 물질화)
- artifact registry or artifact claims (산출물 등록부 또는 산출물 주장)
- code placement or reusable logic ownership (코드 배치 또는 재사용 로직 소유권)
- stage transition or alpha search (단계 전환 또는 알파 탐색)
- repo-scoped skills or agent settings (저장소 범위 스킬 또는 에이전트 설정)
- work packet routing, skill bundles, or final answer filters
- durable path references, archive behavior, or long artifact names (지속 경로 참조, 아카이브 동작, 긴 산출물 파일명)
- Korean `.md` or `.txt` docs (한국어 문서)

Do not key this guard to Stage 06 or Stage 07 only. It applies to all future stages.

## Must Read

- `docs/policies/architecture_invariants.md`
- `docs/registers/architecture_debt_register.md`
- `docs/policies/agent_trigger_policy.md` when routing or skills change
- `docs/policies/reentry_order.md` when re-entry behavior changes
- `docs/policies/exploration_mandate.md` when alpha-search framing or exploration discipline changes
- the touched skill or policy files

## Required Output

Every architecture-sensitive packet or summary must include:

- `architecture_risk`: whether the work can move ownership, source of truth, model identity, alpha-search meaning, or encoding state
- `debt_interaction`: whether it touches registered architecture debt
- `allowed_debt_change`: `reduce`, `leave_unchanged`, or `blocked_without_decision`
- `encoding_check`: whether Korean docs or repo-scoped skills need UTF-8 with BOM validation
- `path_safety_check`: whether repo-relative paths are used for durable identity, whether absolute paths are local-only, and whether Windows long path risk is controlled
- `code_surface_check`: whether owner module, caller, input/output, and artifact/report effect must be named
- `skill_routing_check`: whether `obsidian-work-packet-router` considered the full skill inventory and attached answer clarity plus claim discipline for the final user-facing report

## Guardrails

- Do not treat existing architecture debt as normal style.
- Do not describe a model as `materialized` unless a model artifact or frozen parameter/spec bundle exists.
- Do not add reusable feature logic to a stage script or orchestration pipeline when it belongs in `foundation/features`.
- Do not create all-in-one EA or pipeline monoliths when reusable logic can live in a smaller owner module.
- Do not leave repo-scoped skills present but unrouted; every skill needs routing policy and agent metadata unless a durable exception explains why.
- Do not let alpha search become source cleanup only unless a durable decision says so.
- Do not store absolute terminal install paths as artifact identity; use repo-relative paths plus hash, run id, bundle id, or registry fields.
- Do not call a file missing when one tool enumerates it but another path API fails; rule out Windows long-path handling first.
- Prefer ZIP plus manifest for deep archive snapshots, and keep `\\?\` long-path prefixes local to tooling rather than committed docs.
- Do not edit Korean `.md` or `.txt` docs without preserving UTF-8 with BOM.

## Validator

Run `scripts/validate_agent_settings.py --repo-root .` after editing agent settings, repo-scoped skills, architecture policies, debt registers, or Korean docs.

The validator intentionally treats `agents/openai.yaml` as a small repo-local format: top-level `interface:` and `policy:` sections with two-space indented one-line scalar fields. If richer YAML is needed later, add an explicit YAML dependency and update the validator instead of silently relying on unsupported syntax.
```

### .agents\skills\obsidian-artifact-lineage\SKILL.md

```text
---
name: obsidian-artifact-lineage
description: Track how inputs, code, configs, runs, models, reports, hashes, manifests, ledgers, and external artifact locations connect before evidence or handoff claims are made.
---

# Obsidian Artifact Lineage

Use this skill when work creates, consumes, moves, ignores, packages, releases, or reports artifacts.

## Required Output

- `source_inputs`: data, config, model, bundle, EA, or report inputs
- `producer`: script, pipeline, tester, manual command, or external system that produced the artifact
- `consumer`: next script, run, report, registry, PR, or user action that depends on it
- `artifact_paths`: repo-relative paths when durable; local absolute paths only as local context
- `artifact_hashes`: content hash, params hash, module hash, model hash, or reason unavailable
- `registry_links`: artifact registry, run registry, alpha ledger, stage ledger, or release note rows
- `availability`: tracked, generated, ignored_with_manifest, external_uri, reproducible_from_command, missing, or blocked
- `lineage_judgment`: connected, connected_with_boundary, disconnected, inconclusive, or blocked

## Guardrails

- Do not let a ledger point to missing evidence without a manifest, external URI, or regeneration command.
- Do not commit heavy artifacts just to close an evidence gap; prefer manifest, hash, release, or regeneration path when appropriate.
- Do not treat a report as the same thing as a model or runtime bundle.
```

### .agents\skills\obsidian-backtest-forensics\SKILL.md

```text
---
name: obsidian-backtest-forensics
description: Inspect backtest and Strategy Tester evidence, settings, spread, commission, slippage, trade list, deposits, leverage, modeling mode, and report paths before tester results are trusted.
---

# Obsidian Backtest Forensics

Use this skill when work creates, reads, compares, packages, or reports MT5 Strategy Tester, broker terminal, or backtest outputs.

## Required Output

- `tester_identity`: terminal, broker, symbol, timeframe, deposit, leverage, modeling mode, spread, commission, and date range
- `ea_identity`: EA entrypoint, include module hashes, `.set` file, parameter hash, and model or bundle hash
- `report_identity`: report path, snapshot path, terminal output path, and hash when available
- `trade_evidence`: trade count, gross/net result, drawdown, profit factor, and trade list availability
- `cost_assumptions`: spread, commission, slippage, swap, and missing costs
- `forensic_checks`: checks performed against settings drift, missing output, or malformed report
- `backtest_judgment`: usable, usable_with_boundary, inconclusive, invalid, or blocked

## Guardrails

- Do not trust a report if tester identity is unknown.
- Do not compare tester runs with different cost or modeling assumptions as if they are equal.
- Do not call a backtest reviewed when the output path or run identity is missing.
- Do not use tester profit alone as a promotion argument.
```

### .agents\skills\obsidian-claim-discipline\SKILL.md

```text
---
name: obsidian-claim-discipline
description: Enforce claim discipline in Project Obsidian Prime v2 by downgrading planning or pending states, separating parity levels, and preventing overstatement of closure or readiness. Use when writing docs, reviews, status notes, or user-facing summaries.
---

# Obsidian Claim Discipline

Use this skill when writing, editing, or summarizing project state.

## Automatic Companion

Run this skill as the companion check for user-facing report(사용자 보고), run evidence(실행 근거), stage transition(단계 전환), promotion(승격), runtime(런타임), and blocker(차단 사유) work.

Effect(효과): claim boundary(주장 경계)를 낮출 곳은 낮추고, closure(종료), positive judgment(긍정 판정), operating promotion(운영 승격), runtime authority(런타임 권위)를 근거 없이 쓰지 않는다.

## Trigger Tokens

If any relevant field contains one of these tokens, switch into strict claim discipline:

- `pending_*`
- `planning_*`
- `draft`
- `placeholder_*`
- `not_yet_evaluated`
- `not_applicable`

## Required Behavior

1. Do not describe pending or planning artifacts as:
   - `closed`
   - `materialized`
   - `durable`
   - `parity-closed`
   - `exploration-ready`
   - `alpha-ready`
   - `feature-layer ready`
   - `model materialized`
2. Use precise language:
   - `planning scaffold`
   - `materialized evidence`
   - `foundation truth`
   - `operating truth`
   - `model-input parity`
   - `runtime-helper parity`
   - `bundle handoff verification`
   - `broader-sample parity`
   - `probability-output evidence`
   - `frozen model artifact`
   - `architecture debt`
   - `exploration evidence`
   - `promotion-ineligible`
   - `promotion_candidate`
   - `operating_promotion`
   - `runtime_probe`
   - `runtime_authority`
   - `idea-dead`
   - `tier_c_local_research`
3. If a closure claim is made, name the backing artifact, report, or decision memo.
4. If legacy evidence is referenced, mark it `prior evidence only`.
5. If local-only artifacts are relied upon, ensure their identity is represented in `docs/registers/artifact_registry.csv` before describing them as reusable.
6. Do not let `README.md` or another overview doc carry mutable live-state claims unless they are synchronized in the same pass; prefer pointers to the authoritative current-truth docs.
7. Do not describe a model as materialized unless a reproducible model artifact or frozen parameter/spec bundle exists.
8. Do not describe `foundation/features` or another reusable feature layer as ready when reusable logic still lives only in a pipeline or stage-local script.
9. Do not treat registered architecture debt as a normal pattern to inherit.
10. Do not describe a promotion-ineligible idea as worthless, dead, or fully closed unless negative-result memory records why it failed, what was salvaged, and when to reopen it.
11. Do not describe Tier C local research as a trading lane, reduced-risk substitute, or promotion argument.
12. Do not describe a legacy lesson as v2 truth unless a v2 artifact closes the same question.
13. Do not confuse `negative` (`부정`) with `invalid` (`무효`); a negative result is interpretable evidence, while an invalid result is not.
14. Do not describe `inconclusive` (`불충분`) as success, closure, or failure unless the missing evidence and remaining question are named.
15. Do not call a run `reviewed`, `selected`, `archived`, or `closed` unless measurement evidence, managed identity, and lane-aware judgment are present or explicitly marked `n/a` with reasons.
16. Do not describe `promotion_candidate` (`승격 후보`) as `operating_promotion` (`운영 승격`).
17. Do not describe `runtime_probe` (`런타임 탐침`) as `runtime_authority` (`런타임 권위`) or runtime parity closure.

## Project-Specific Guardrails

- `planning scaffold` is not `materialized evidence`.
- `foundation truth` is not `operating truth`.
- `foundation stage closure` is not `exploration-ready`.
- `handoff verification` is not `runtime parity closure`.
- `probability-output evidence` is not a `frozen model artifact`.
- `architecture debt` is not an accepted architecture pattern.
- `promotion-ineligible` is not `idea-dead`.
- `tier_c_local_research` is not a runtime lane.
- `legacy exploration spirit` is not `legacy result inheritance`.
- `negative` is not `invalid`.
- `inconclusive` is not quiet approval.
- `structural_scout` is not an operating promotion read.
- `promotion_candidate` is not `operating_promotion`.
- `runtime_probe` is not `runtime_authority`.
```

### .agents\skills\obsidian-code-quality\SKILL.md

```text
---
name: obsidian-code-quality
description: Raise implementation quality so code reads like a well-structured expert answer, not just a script that happens to run. Use when writing or reviewing Python, MQL5, feature, label, split, model, dataset, parity, report, or test code.
---

# Obsidian Code Quality

Use this skill when implementation quality matters, especially for quant research code.

This is different from `obsidian-code-surface-guard`. Code surface decides where code belongs. Code quality decides whether the implementation itself is clear, disciplined, and trustworthy.

## Automatic Bundle

Trigger automatically after `obsidian-code-surface-guard` for non-trivial code edit(비사소 코드 변경) in Python(파이썬), MQL5, feature(피처), label(라벨), split(분할), model(모델), dataset(데이터셋), parity(동등성), report(보고서), or test(테스트) code.

Effect(효과): code quality(코드 품질), responsibility(책임), flow(흐름), contract(계약), and test intent(검증 의도)를 구현 중에 점검해서 실행만 되는 큰 스크립트로 흐르지 않게 한다.

## Quality Standard

Code should read like a good expert answer:

- the responsibility is clear
- the reasoning flow is visible
- inputs, processing, and outputs are separated
- assumptions are near the code that depends on them
- names explain intent
- constants and thresholds are not hidden magic
- failures explain what broke
- outputs can be traced later
- tests protect the intended behavior, not only execution

## Quant-Specific Quality Points

For trading or research code, treat these as core quality issues:

- input data identity and expected columns
- timestamp meaning and timezone policy
- feature calculation boundary
- label calculation boundary
- train, validation, and OOS split boundary
- lookahead or future-data leakage risk
- dataset id, config, row count, hash, and artifact path traceability
- whether tests check financial or temporal meaning, not only that code runs

## Required Output Before Or During Implementation

- `responsibility`: what this code owns
- `flow`: how data moves from input to output
- `contracts`: input, output, and failure contracts
- `assumptions`: assumptions that must not be hidden
- `traceability`: ids, hashes, configs, row counts, or artifact paths to preserve
- `test_intent`: what the tests prove
- `quality_risk`: the most likely way this code could become misleading or hard to change

## Do Not

- Do not write a large script where parsing, feature work, labels, model training, and reporting are tangled together.
- Do not let a passing test replace a clear contract.
- Do not hide a business or trading assumption in a variable name like `threshold = 0.5`.
- Do not mix feature and label logic unless the boundary is explicit and tested.
- Do not rely on timestamp meaning by memory; use the project time-axis policy or name the unresolved assumption.
```

### .agents\skills\obsidian-code-surface-guard\SKILL.md

```text
---
name: obsidian-code-surface-guard
description: Prevent Project Obsidian Prime v2 code-surface drift, monolith growth, and EA run-variant sprawl. Use when adding, moving, or modifying code in foundation, pipelines, MT5 EA files, .mqh modules, .set/tester configuration, stage scripts, model builders, feature calculators, runtime helpers, or report materialization paths.
---

# Obsidian Code Surface Guard

Use this skill for code changes before choosing files or writing implementation.

## Automatic Code-Writing Gate

For every code-writing packet(code-writing packet, 코드 작성 묶음), including Python(파이썬), MQL5, tests(테스트), stage scripts(단계 스크립트), pipelines(파이프라인), model builders(모델 빌더), runtime helpers(런타임 도구), and report materializers(보고서 물질화 도구), run this guard before editing files.

Pair it with `obsidian-reference-scout(레퍼런스 탐색)` in the same precheck. The effect(effect, 효과) is that placement(배치) and external correctness(외부 정확성)을 분리해서 확인한다.

If no file is edited, mark `code_surface_guard: not_required(코드 표면 가드 불필요)` with a short reason(reason, 이유).

## Must Read

- `docs/policies/architecture_invariants.md`
- `docs/registers/architecture_debt_register.md`
- the touched module, caller, and nearest existing orchestration path

## Required Output

- `owner_module`: where reusable logic belongs
- `caller`: which pipeline, stage script, EA, or test calls it
- `input_contract`: input data shape, feature surface, or config boundary
- `output_contract`: output artifact, report, or runtime effect
- `artifact_or_report_relation`: what durable artifact or report is affected
- `monolith_risk`: whether the change concentrates too much logic in one file
- `placement_decision`: why the chosen location is correct
- `reference_scout_pairing`: whether `obsidian-reference-scout(레퍼런스 탐색)` was used, or why it was not required

## Placement Rules

- Put reusable feature/model/runtime logic under the correct `foundation` owner.
- Use `foundation/pipelines` for orchestration, not as the long-term owner of reusable feature logic.
- Use stage scripts for materialization and stage-local analysis, not reusable contracts.
- Use MT5 EA code for execution and verification, not as the only owner of feature or model semantics.
- Do not add another broad all-in-one EA or pipeline file when a smaller owner module can hold the logic.

## EA Run Variant Hard Trigger(EA 실행 변형 강제 트리거)

Trigger automatically when work touches MT5 EA(`Expert Advisor`, 전문가 자문), `.mq5`, `.mqh`, `.set`, Strategy Tester(전략 테스터), optimization pass(최적화 회차), runtime package(런타임 패키지), model bundle(모델 번들), tester property(테스터 속성), EA run config(EA 실행 설정), or Tier A primary + Tier B fallback routing(Tier A 우선 + Tier B 대체 라우팅).

Before editing, classify the run-specific difference(실행별 차이):

- `parameter_only(파라미터만)`: keep the EA entrypoint(진입점) and modules(모듈) unchanged; create or update `.set`, `run_manifest.json`, and KPI record(KPI 기록).
- `module_change(모듈 변경)`: update the smallest `.mqh` owner module(소유 모듈), version it, and record module sha256(모듈 해시).
- `entrypoint_change(진입점 변경)`: only when lifecycle(생명주기), `#property(프로그램 속성)`, file handoff(파일 인계), or tester wiring(테스터 연결)이 바뀐다.
- `new_runner_required(새 실행기 필요)`: only when existing runner(실행기) + modules(모듈) cannot represent the experiment.

Default no(기본 금지): do not manage run variants by copying a new broad `.mq5` file for each run.

Required output addition(필수 출력 추가):

- `ea_variant_boundary`: one of the four classes above
- `entrypoint_identity`: `.mq5` path and whether it changed
- `set_identity`: `.set` or config path and hash when applicable
- `module_identity`: touched `.mqh` modules and hashes
- `tester_identity`: tester model(테스터 모델), deposit(예치금), leverage(레버리지), symbol/timeframe(심볼/시간프레임)

Effect(효과): run01A/run01B-style variants(실행 변형)가 code sprawl(코드 난립)로 숨지 않고, configuration(설정), module version(모듈 버전), and evidence identity(근거 정체성)로 추적된다.

Routing note(라우팅 주의): Tier A primary + Tier B fallback routing(Tier A 우선 + Tier B 대체 라우팅)은 parameter-only(파라미터만)일 수도 있고 module_change(모듈 변경)일 수도 있다. combined record(합산 기록)는 actual routed total(실제 라우팅 전체)인지 synthetic sum(합성 합산)인지 코드와 장부에서 분명히 남긴다.

## Stop Conditions

- The caller is unknown.
- The effect of the code on artifacts, reports, or runtime behavior is unknown.
- The change deepens registered architecture debt without an explicit task packet or decision memo.
```

### .agents\skills\obsidian-data-integrity\SKILL.md

```text
---
name: obsidian-data-integrity
description: Check data, time-axis, timezone, split, missing row, duplicate row, leakage, and feature-label boundary risks before trading research results are trusted.
---

# Obsidian Data Integrity

Use this skill whenever work touches datasets, features, labels, splits, bars, timestamps, joins, resampling, training windows, runtime inputs, or KPI interpretation.

## Required Output

- `data_source`: source files, broker feed, runtime output, or generated artifact
- `time_axis`: timestamp meaning, timezone policy, bar close/open convention, and ordering
- `sample_scope`: symbol, timeframe, date range, tiers, rows, and exclusions
- `missing_or_duplicate_check`: whether gaps or duplicates matter here
- `feature_label_boundary`: how future data is prevented from entering features
- `split_boundary`: train, validation, test, WFO, or runtime split meaning
- `leakage_risk`: most likely lookahead or selection-bias path
- `data_hash_or_identity`: file hash, row count, artifact id, or reason unavailable
- `integrity_judgment`: usable, usable_with_boundary, inconclusive, invalid, or blocked

## Guardrails

- Do not trust a profitable result before the time axis and label boundary are named.
- Do not hide timezone assumptions in variable names.
- Do not mix feature and label logic without an explicit boundary and test intent.
- Do not call a result invalid when it is only incomplete; name the missing integrity check.
```

### .agents\skills\obsidian-environment-reproducibility\SKILL.md

```text
---
name: obsidian-environment-reproducibility
description: Keep project work reproducible across clean checkout, dependencies, Python versions, CI, MT5 paths, external artifacts, and local machine assumptions.
---

# Obsidian Environment Reproducibility

Use this skill when work touches tests, README commands, dependency setup, CI, clean checkout behavior, MT5 terminal paths, local absolute paths, external artifacts, or instructions another machine must run.

## Required Output

- `execution_environment`: OS, Python, MT5, broker terminal, or CI context when relevant
- `dependency_surface`: packages, versions, tools, and missing install contract
- `entry_command`: command a clean checkout should run
- `local_assumptions`: absolute paths, terminal data roots, environment variables, or machine-only files
- `clean_checkout_status`: expected to pass, expected blocked, not tested, or not applicable
- `recovery_instruction`: install, configure, fetch artifact, regenerate, or user action
- `reproducibility_judgment`: reproducible, reproducible_with_setup, local_only, inconclusive, or blocked

## Guardrails

- Do not document a test command as default if dependencies are not declared.
- Do not rely on repository location to discover MT5 data roots without a fail-fast check or configuration path.
- Do not describe missing artifacts as reproducible unless fetch or regeneration steps exist.
```

### .agents\skills\obsidian-experiment-design\SKILL.md

```text
---
name: obsidian-experiment-design
description: Design project-wide trading research experiments by naming hypothesis, comparison, controls, stop conditions, success and failure criteria, and required evidence before code or runs are produced.
---

# Obsidian Experiment Design

Use this skill when a request creates, changes, compares, packages, or closes an experiment. It applies across the full project lifecycle, not only alpha exploration.

## Required Output

- `hypothesis`: what the experiment is trying to learn
- `decision_use`: what decision the result can influence
- `comparison_baseline`: what the result is compared against
- `control_variables`: settings that must stay fixed
- `changed_variables`: settings or code paths intentionally changed
- `sample_scope`: dataset, tier, symbol, timeframe, date range, or runtime scope
- `success_criteria`: what would count as useful evidence
- `failure_criteria`: what would count as a failed or negative result
- `invalid_conditions`: what would make the result unusable
- `stop_conditions`: when to stop, narrow, rerun, or downgrade claims
- `evidence_plan`: KPI, files, manifests, registry rows, and checks needed

## Guardrails

- Do not treat a run that merely completed as a meaningful experiment.
- Do not compare results if the baseline, data scope, or changed variable is unclear.
- Do not let an operating gate prevent research unless the claim is operating promotion or runtime authority.
- Do not design an experiment that cannot be explained later through `obsidian-answer-clarity`.
```

### .agents\skills\obsidian-exploration-mandate\SKILL.md

```text
---
name: obsidian-exploration-mandate
description: Preserve Project Obsidian Prime v2 exploration discipline without importing legacy code or promotion history. Use for alpha search, idea variants, Tier B or Tier C research, WFO planning, extreme sweeps, negative-result closure, and any task where an idea should be pushed, archived, or reopened.
---

# Obsidian Exploration Mandate

Use this skill when the task is primarily exploration or when promotion discipline is at risk of blocking exploration too early.

## Must Read

- `docs/policies/exploration_mandate.md`
- `docs/registers/idea_registry.md`
- `docs/registers/negative_result_register.md`
- `docs/registers/legacy_lesson_register.md` when legacy lessons are mentioned
- `docs/policies/tiered_readiness_exploration.md` when Tier A/B/C is involved

## Required Output

- `idea_id`: existing or proposed ID
- `hypothesis`: what the idea claims
- `legacy_relation`: `none`, `concept_only`, `lesson_only`, or `prior_evidence_only`
- `tier_scope`: Tier A, Tier B, Tier C local research, or mixed
- `broad_sweep`: coarse ranges or structural variants
- `extreme_sweep`: boundary values or stress values to try
- `micro_search_gate`: condition required before fine search
- `wfo_plan`: walk-forward frame or explicit exception
- `failure_memory`: negative result, salvage value, and reopen condition requirements
- `evidence_boundary`: scout-only, candidate, probe, reviewed, selected, operating-promotion, or runtime-authority boundary

## Exploration Rules

- Start with broad sweep before micro search.
- Include extreme values when they can reveal cliffs, saturation, or failure boundaries.
- Use WFO as the default optimization frame for robust evidence.
- Treat single-window optimization as a scout read unless a packet explicitly justifies otherwise.
- Do not kill an idea only because WFO, full parity, or runtime closure is absent; label the result boundary instead.
- Record failed ideas as evidence, not waste.
- Keep legacy material as lesson-only unless a v2 artifact closes the same question.

## Tier Rules

- Tier A and Tier B are both fully open to exploration.
- Tier labels describe sample context; they do not grant or deny permission to study an idea.
- Tier A or Tier B may become promotion/runtime evidence only after the relevant operating gates close.
- Tier C is weak or unusable by default, but may be `tier_c_local_research` when a stage explicitly allows local-only research.
- `tier_c_local_research` must not become a trading lane, reduced-risk substitute, or promotion argument.
```

### .agents\skills\obsidian-lane-classifier\SKILL.md

```text
---
name: obsidian-lane-classifier
description: Classify Project Obsidian Prime v2 work into exploration, evidence, promotion, runtime, or extra lanes before planning or implementation. Use when a task involves alpha search, stage work, tiered readiness, promotion, runtime verification, extra stages, or ambiguous user intent that could mix exploration and operating discipline.
---

# Obsidian Lane Classifier

Use this skill before a task packet or implementation when lane confusion could change the required discipline.

## Automatic Bundle

Trigger automatically when a task mixes lane(레인), exploration(탐색), evidence(근거), promotion(승격), runtime(런타임), Tier A/B/C(티어 A/B/C), hard gate(강한 게이트), operating_promotion(운영 승격), or runtime_authority(런타임 권위) language.

Effect(효과): hard gate(강한 게이트)를 exploration permission(탐색 허가)으로 잘못 쓰지 않고, operating discipline(운영 규율)이 필요한 주장만 강하게 막는다.

## Must Read

- `docs/policies/exploration_mandate.md`
- `docs/policies/promotion_policy.md` when promotion is possible
- `docs/policies/tiered_readiness_exploration.md` when Tier A/B/C readiness is involved

## Lane Definitions

- `exploration`: create, mutate, stress, and learn from ideas.
- `evidence`: make results comparable, inspectable, and reusable.
- `promotion`: decide whether a candidate can replace or confirm the operating line.
- `runtime`: verify execution, parity, packaging, and environment behavior.
- `extra`: user-requested side stage or non-standard question with its own charter.

## Required Output

- `lane`: one primary lane
- `secondary_lane`: optional supporting lane
- `discipline`: `exploration_discipline`, `operating_discipline`, or `handoff_discipline`
- `promotion_state`: `none`, `promotion_candidate`, or `operating_promotion`
- `runtime_state`: `none`, `runtime_probe`, or `runtime_authority`
- `promotion_gate_applicable`: `yes` or `no`
- `runtime_gate_applicable`: `yes` or `no`
- `hard_gate_applicable`: `yes` only for operating truth claims
- `failure_memory_required`: `yes` or `no`

## Guardrails

- Do not apply operating-promotion or runtime-authority gates to early exploration unless the task asks for an operating truth claim.
- Allow `promotion_candidate` and `runtime_probe` when the evidence boundary is explicit.
- Do not call an idea worthless because it is blocked for promotion.
- Do not let an `extra` stage bypass Tier A/B/C, WFO defaults, artifact identity, or runtime parity rules.
- If the user intent is informal, infer the lane from the work effect and state the inference.
```

### .agents\skills\obsidian-model-validation\SKILL.md

```text
---
name: obsidian-model-validation
description: Validate project-wide model, threshold, calibration, split, WFO, overfit, and selection decisions before model or threshold results influence promotion, runtime, or next experiment choices.
---

# Obsidian Model Validation

Use this skill when work touches model training, model selection, threshold selection, ranking, calibration, feature importance, WFO, or any claim that one model is better than another.

## Required Output

- `model_family`: model type, training script, or runtime bundle
- `target_and_label`: what the model predicts and how the label is built
- `split_method`: holdout, WFO, cross-validation, runtime probe, or other split
- `selection_metric`: metric used to choose the model or threshold
- `secondary_metrics`: metrics that can reveal hidden failure
- `threshold_policy`: fixed, searched, calibrated, or runtime-configured
- `overfit_risk`: most likely overfitting or multiple-testing path
- `calibration_risk`: whether scores mean probability, rank, or only ordering
- `comparison_baseline`: previous model, no-trade baseline, random baseline, or manual rule
- `validation_judgment`: exploratory, candidate, inconclusive, invalid, blocked, or stronger project term allowed by policy

## Guardrails

- Do not promote a model because one threshold or one split looks good.
- Do not describe rank scores as probabilities unless calibration supports it.
- Do not let WFO absence kill exploration; downgrade the claim instead.
- Do not choose a threshold without naming what it optimizes and what it may harm.
```

### .agents\skills\obsidian-performance-attribution\SKILL.md

```text
---
name: obsidian-performance-attribution
description: Explain why KPI changed by decomposing performance across time, sample, tier, feature, threshold, model, trade shape, drawdown, and regime before claiming improvement.
---

# Obsidian Performance Attribution

Use this skill when a result is better, worse, surprising, unstable, or used to choose the next experiment.

## Required Output

- `observed_change`: KPI or behavior that changed
- `comparison_baseline`: what it changed against
- `likely_drivers`: threshold, model, feature, data scope, tier mix, trade frequency, risk shape, or market regime
- `segment_checks`: time period, tier, direction, volatility, session, drawdown cluster, or trade bucket checks performed or missing
- `trade_shape`: count, win rate, payoff ratio, average win/loss, drawdown, concentration, and exposure when available
- `alternative_explanations`: possible non-signal explanations
- `attribution_confidence`: high, medium, low, inconclusive, or invalid
- `next_probe`: smallest follow-up that can confirm or reject the explanation

## Guardrails

- Do not say a model improved just because one headline KPI improved.
- Do not hide a worse drawdown, trade concentration, or sample shrink behind profit.
- Do not over-explain noise; mark low-confidence attribution when evidence is thin.
```

### .agents\skills\obsidian-reentry-read\SKILL.md

```text
---
name: obsidian-reentry-read
description: Re-enter Project Obsidian Prime v2 safely by reading the current truth in order, restating the active stage and foundation status, and avoiding stale assumptions. Use when starting or resuming work in this repository.
---

# Obsidian Reentry Read

Use this skill whenever work starts or resumes inside `Project_Obsidian_Prime_v2`.

## Workflow

1. Open `AGENTS.md`, then open `docs/policies/reentry_order.md`.
2. Follow the canonical ordered pass and truth precedence defined there.
3. If the task touches feature/model/pipeline/artifact architecture, alpha-search framing, repo-scoped skills, agent settings, or Korean encoding, also read `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md`.
4. If the task touches exploration, idea variants, Tier B/C research, WFO planning, negative-result closure, legacy lessons, or user-requested extra stages, also read `docs/policies/exploration_mandate.md`, `docs/registers/idea_registry.md`, and `docs/registers/negative_result_register.md`.
5. If the task touches run creation, KPI reporting, result summaries, result judgment, or run closeout, also read `docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`, and `docs/registers/run_registry.csv`.
6. Validate before acting:
   - `docs/workspace/workspace_state.yaml` names one active stage
   - the active stage `selection_status.md` agrees with that stage
   - the latest durable stage-handoff decision matches the same transition
   - if any of those disagree, stop and surface state fragmentation before continuing
7. Restate:
   - active stage
   - current foundation truth
   - current operating-truth boundary
   - what is planning only
   - what is materialized
   - what remains open
   - architecture debt interaction when relevant
   - exploration lane and failure-memory interaction when relevant
   - run evidence measurement, management, and judgment interaction when relevant
8. Do not start work from memory alone.

## Project-Specific Guardrails

- This repo is a `concept-preserving reboot`, not a legacy continuation.
- `legacy` findings are `prior evidence only` unless a v2 artifact closes the same question.
- v2 inherits the legacy exploration mandate, not legacy code, run results, winners, or promotion history.
- `Stage 00` is closed as planning scaffold complete.
- derive the current active stage from `docs/workspace/workspace_state.yaml` and active stage docs; do not hard-code the stage name in this skill
- registered architecture debt is not a normal pattern to copy into later stages
- promotion-ineligible does not mean idea-dead
- negative does not mean invalid, and inconclusive does not mean quiet approval
```

### .agents\skills\obsidian-reference-scout\SKILL.md

```text
---
name: obsidian-reference-scout
description: Find and use external references for correct API usage, syntax, implementation patterns, MQL5/MT5 EA behavior, Strategy Tester behavior, library behavior, quant methods, and idea scouting. Use when project memory is not enough, an API may be version-sensitive, EA run-variant management touches official behavior, or alpha/research ideas need external examples.
---

# Obsidian Reference Scout

Use this skill when outside references can improve correctness, idea quality, or confidence in environment behavior.

This skill is for scouting and grounding, not copying.

## Automatic Code-Writing Pair

For every code-writing packet(code-writing packet, 코드 작성 묶음), run this scout beside `obsidian-code-surface-guard(코드 표면 가드)`.

Use external lookup(외부 확인) when the code touches MQL5/MT5(MetaTrader 5, 메타트레이더5), MetaEditor(메타에디터), strategy tester(전략 테스터), file handoff(파일 인계), external API(외부 API), CLI, or library behavior(라이브러리 동작) such as pandas/sklearn/numpy/LightGBM.

If the code is pure internal logic(순수 내부 로직) with no uncertain API(API 사용법), syntax(구문), version-sensitive behavior(버전 민감 동작), or external pattern(외부 패턴), record `reference_scout: not_required(레퍼런스 탐색 불필요)` with the reason(reason, 이유). This record belongs in the implementation precheck or completion report; do not leave it implicit.

Effect(effect, 효과): implementation(구현)을 프로젝트 기억(project memory, 프로젝트 기억)만으로 단정하지 않고, 필요한 곳에서는 official docs(공식 문서)나 maintained source(유지보수되는 원천)로 접지한다.

## When To Use

- correct function, API, or syntax usage is uncertain
- library behavior may depend on version
- MQL5 or MT5 tester behavior is unclear
- EA(`Expert Advisor`, 전문가 자문) management touches `#include(포함)`, `input/sinput(입력/고정 입력)`, `OnInit/OnTick/OnTester(초기화/틱/테스터)`, `.set` files(설정 파일), tester properties(테스터 속성), or optimization frames(최적화 프레임)
- LightGBM, pandas, sklearn, numpy, or another library usage needs confirmation
- implementation patterns from maintained GitHub projects may help
- dependency, packaging, clean checkout, or CI behavior may differ by environment
- quant method choice, validation frame, backtest method, or runtime parity needs grounding
- alpha exploration is stuck and outside examples may suggest new ideas
- forum posts may reveal practical edge cases

## Source Priority

1. Official documentation or vendor docs.
2. Maintained source repository, examples, release notes, or issue discussions.
3. Well-scoped GitHub examples with readable code and recent maintenance.
4. Forum or community posts, including MQL5 forum, only as idea candidates or practical warnings.

## Required Output

- `question`: what usage, idea, or pattern was researched
- `sources_checked`: which sources were checked
- `source_quality`: official, maintained code, example, issue, forum, or weak
- `found_pattern`: the useful pattern or warning
- `project_fit`: how it fits or conflicts with this repo's contracts
- `do_not_copy`: what should not be copied directly
- `recommended_use`: adopt, adapt, treat as idea, or reject
- `not_required_reason`: only when no lookup was needed

## EA Reference Hard Trigger(EA 레퍼런스 강제 트리거)

For MT5 EA(`Expert Advisor`, 전문가 자문) architecture, run variant management(실행 변형 관리), Strategy Tester(전략 테스터), `.set` file(설정 파일), `input/sinput(입력/고정 입력)`, `#include(포함)`, `#property(프로그램 속성)`, or `OnInit/OnTick/OnTester(초기화/틱/테스터)` behavior, check official MQL5 documentation first.

Minimum source questions(최소 확인 질문):

- Is this behavior defined in official docs(공식 문서)?
- Does it belong in main `.mq5` entrypoint(진입점) or `.mqh` include module(포함 모듈)?
- Is the run difference parameter-only(파라미터만) or code-changing(코드 변경)?
- Which identity fields(정체성 필드) must be recorded so tester output(테스터 출력) can be traced?

Effect(효과): EA 관리 판단을 기억이나 forum habit(포럼 관습)에 맡기지 않고, official behavior(공식 동작)와 project contract(프로젝트 계약)를 같이 맞춘다.

## Guardrails

- Prefer official docs for API and syntax questions.
- Do not copy external code wholesale into this repo.
- Do not trust forum performance claims as evidence.
- Do not let external examples override project contracts for time axis, dataset identity, split policy, artifact identity, or runtime authority.
- If a source is old, version-specific, or unclear, say so.
- If browsing or source lookup was not performed, do not present the answer as externally verified.

## Example

If MQL5 file handoff behavior is unclear, scout official MQL5 docs first, then relevant forum or GitHub examples. The useful result might be a pattern such as waiting for file size stability, but the implementation still needs to fit this project's runtime parity and artifact identity rules.
```

### .agents\skills\obsidian-result-judgment\SKILL.md

```text
---
name: obsidian-result-judgment
description: Judge project results with the correct boundary before claiming positive, negative, invalid, blocked, promotion candidate, operating promotion, runtime probe, or runtime authority.
---

# Obsidian Result Judgment

Use this skill when a result, run, experiment, model, package, backtest, PR, or stage outcome is interpreted for the user or written into a register.

## Must Read

- `docs/policies/result_judgment_policy.md`
- `docs/policies/promotion_policy.md`
- `docs/policies/run_result_management.md` when run status changes
- `docs/policies/kpi_measurement_standard.md` when KPI is involved

## Required Output

- `result_subject`: what is being judged
- `evidence_available`: KPI, report, artifact, registry row, test, backtest, or runtime output
- `evidence_missing`: what is absent or weak
- `judgment_label`: positive, negative, invalid, inconclusive, blocked, exploratory, promotion_candidate, operating_promotion, runtime_probe, runtime_authority, or not_applicable
- `claim_boundary`: what can be said now and what cannot
- `next_condition`: smallest condition that could strengthen, weaken, or close the judgment
- `user_explanation_hook`: plain-language meaning for `obsidian-answer-clarity`

## Guardrails

- Do not call a result positive only because a script ran.
- Do not call a result negative when the run is invalid or missing evidence.
- Do not turn promotion_candidate into operating_promotion.
- Do not turn runtime_probe into runtime_authority.
- Pair final user-facing judgment with `obsidian-claim-discipline` and `obsidian-answer-clarity`.
```

### .agents\skills\obsidian-run-evidence-system\SKILL.md

```text
---
name: obsidian-run-evidence-system
description: Manage Project Obsidian Prime v2 run evidence across KPI measurement, run result identity, EA/MT5 tester identity, and lane-aware judgment. Use for run creation, run closeout, KPI reports, result summaries, stage run reviews, run registry updates, EA/MT5 tester runs, or deciding whether a run is positive, negative, inconclusive, or invalid.
---

# Obsidian Run Evidence System

Use this skill when a task creates, reviews, closes, summarizes, or registers run (`실행`) evidence.

## Automatic Bundle

When this skill triggers for run creation(실행 생성), run closeout(실행 종료), KPI report(KPI 보고), result summary(결과 요약), or run registry update(실행 등록부 갱신), pair it with `obsidian-claim-discipline`.

Effect(효과): measurement(측정), identity(정체성), judgment(판정), and registry boundary(등록부 경계) stay explicit before any run is called reviewed(검토됨), selected(선택됨), positive(긍정), negative(부정), inconclusive(불충분), invalid(무효), operating_promotion(운영 승격), or runtime_authority(런타임 권위).

## Must Read

- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`
- `docs/registers/run_registry.csv`
- `docs/policies/exploration_mandate.md` when the run is exploration-sensitive
- `docs/policies/promotion_policy.md` when promotion is possible
- `docs/policies/tiered_readiness_exploration.md` when Tier A/B/C readiness is involved

## Required Output

- `measurement_scope`: which KPI (`key performance indicator`, 핵심 성과 지표) layers are required
- `management_state`: run folder (`실행 폴더`), manifest, KPI record, summary, and registry state
- `judgment_class`: `positive`, `negative`, `inconclusive`, or `invalid`
- `scoreboard`: `structural_scout`, `regular_risk_execution`, `wfo_oos`, `runtime_parity`, or `diagnostic_special`
- `parity_level`: `P0_unverified`, `P1_dataset_feature_aligned`, `P2_model_input_parity_closed`, `P3_runtime_shadow_parity_sampled`, or `P4_full_runtime_parity_closed`
- `wfo_status`: `not_applicable`, `planned`, `partial`, `complete`, or `exception`
- `registry_update_required`: `yes` or `no`
- `negative_memory_required`: `yes` or `no`
- `hard_gate_applicable`: `yes` only for `operating_promotion` or `runtime_authority`
- `evidence_boundary`: `scout-only`, `candidate`, `probe`, `reviewed`, `selected`, `operating_promotion`, or `runtime_authority`

## EA/MT5 Run Identity(EA/MT5 실행 정체성)

When a run uses MT5 EA(`Expert Advisor`, 전문가 자문), Strategy Tester(전략 테스터), `.set` file(설정 파일), runtime package(런타임 패키지), or model bundle(모델 번들), add the following identity fields to the manifest(목록), KPI record(KPI 기록), or equivalent evidence:

- `ea_entrypoint`: main `.mq5` path(경로) and sha256 hash(해시)
- `ea_variant_boundary`: `parameter_only/module_change/entrypoint_change/new_runner_required(파라미터만/모듈 변경/진입점 변경/새 실행기 필요)`
- `set_file`: `.set` path(설정 파일 경로) and sha256 hash(해시), or explicit `not_applicable(해당 없음)` reason
- `input_params_hash`: canonical input parameter hash(정규 입력 파라미터 해시)
- `module_hashes`: `.mqh` module list(모듈 목록) and sha256 hashes(해시)
- `model_or_bundle_hash`: model/bundle artifact hash(모델/번들 산출물 해시)
- `tester_identity`: symbol(심볼), timeframe(시간프레임), tester model(테스터 모델), deposit(예치금), leverage(레버리지), spread/cost assumption(스프레드/비용 가정)
- `tester_output_path`: terminal output(터미널 출력), tester report(테스터 보고서), or runtime telemetry(런타임 기록) path(경로)

Effect(효과): profit(수익), drawdown(손실 곡선), execution KPI(실행 KPI), runtime probe(런타임 탐침)를 말할 때 어느 EA code(코드), setting(설정), module(모듈), model bundle(모델 번들)에서 나온 결과인지 끊기지 않는다.

## Guardrails

- Early scout runs may use partial evidence if the missing layers and evidence boundary are labeled.
- Do not close a reviewed or selected run without machine-readable KPI evidence or explicit `n/a` reasons.
- Do not confuse `negative` (`부정`) with `invalid` (`무효`).
- Do not treat `inconclusive` (`불충분`) as either success or failure.
- Do not claim `operating_promotion` (`운영 승격`) from `structural_scout` (`구조 탐색 점수판`) or `promotion_candidate` (`승격 후보`) evidence alone.
- Do not claim `runtime_authority` (`런타임 권위`) from `runtime_probe` (`런타임 탐침`) evidence.
- Do not blend Tier B/C research KPI with Tier A promotion or runtime KPI.
- For Tier A primary + Tier B fallback routing(Tier A 우선 + Tier B 대체 라우팅), record Tier A used(Tier A 사용), Tier B fallback used(Tier B 대체 사용), and actual routed total(실제 라우팅 전체); do not present a synthetic sum(합성 합산) of separate tester runs(분리 테스터 실행) as the combined record(합산 기록).
- Do not claim `P4_full_runtime_parity_closed` from lower-level parity evidence.
- Keep large artifacts outside Git only when their identity, path, and hash are represented in Git-tracked evidence.
- Do not mark an EA/MT5 tester run as reviewed if `ea_entrypoint`, `set_file` or equivalent config, `module_hashes`, `model_or_bundle_hash`, and `tester_identity` are missing without explicit `not_applicable(해당 없음)` reasons.

## Closeout Checklist

Before marking a run as reviewed, selected, archived, invalidated, or superseded:

1. Confirm `run_manifest.json` or equivalent identity evidence exists.
2. Confirm `kpi_record.json` or equivalent KPI evidence exists.
3. Confirm `result_summary.md` or equivalent human readout exists.
4. Confirm `docs/registers/run_registry.csv` has or will receive a row.
5. Classify the result as `positive`, `negative`, `inconclusive`, or `invalid`.
6. If the result closes an exploration idea negatively, record salvage value and reopen condition.

Before claiming `operating_promotion` or `runtime_authority`, confirm the relevant hard-gate evidence exists and the claim is backed by a durable decision or closure artifact.
```

### .agents\skills\obsidian-runtime-parity\SKILL.md

```text
---
name: obsidian-runtime-parity
description: Check that Python research, packaged artifacts, MT5 EA behavior, Strategy Tester behavior, and live-like runtime handoff carry the same meaning before runtime claims are made.
---

# Obsidian Runtime Parity

Use this skill when work touches MT5, EA modules, runtime packages, model bundles, `.set` files, tester output, handoff files, live-like execution, or comparisons between Python and runtime behavior.

## Required Output

- `research_path`: Python script, model builder, feature calculator, or report path
- `runtime_path`: MT5 EA, include module, package, `.set`, tester profile, or handoff path
- `shared_contract`: features, labels, inputs, outputs, thresholds, and time-axis rules that must match
- `known_differences`: differences that are intentional or unresolved
- `parity_check`: compile, snapshot, file handoff, tester output, row-level comparison, or reason unavailable
- `parity_identity`: module hashes, bundle hash, parameter hash, tester identity, and output path when applicable
- `runtime_claim_boundary`: research-only, runtime_probe, runtime_authority_candidate, blocked, or not_applicable

## Guardrails

- Do not treat Python success as runtime authority.
- Do not treat MetaEditor compile as a substitute for tester or runtime output.
- Do not change EA entrypoints for parameter-only experiments.
- Do not hide runtime differences in file names; record identities and hashes.
```

### .agents\skills\obsidian-session-intake\SKILL.md

```text
---
name: obsidian-session-intake
description: Start each Project Obsidian Prime v2 turn by establishing current truth, deciding cold re-entry versus warm-thread delta check, and handing the request to a project-wide work-packet router instead of treating code, experiment, evidence, and report as separate modes.
---

# Obsidian Session Intake

Use this skill at the start of a working turn when the user asks for current status, next work, implementation, verification, publishing, or a project-policy change.

This is an intake skill, not a single-mode classifier. Most Obsidian work is a multi-phase packet: design, code, experiment or verification, evidence, judgment, and user-facing report often belong to one request.

## When To Trigger

- a new thread starts in this repo
- work resumes after a pause
- the user asks for current progress, current state, or the next task
- the user asks to proceed but no current task packet is fixed yet

## Do First

1. Decide whether the thread is cold or warm.
2. If the thread is warm and the active stage is stable, prefer a delta check instead of repeating full cold re-entry.
3. Check whether the current branch/worktree matches the requested stage, PR, experiment, or policy scope.
4. Identify the likely work packet lifecycle and candidate `primary_family`. Do not force a single mode when the work naturally spans several phases.
5. Hand the lifecycle and candidate family to `obsidian-work-packet-router` so it can choose exactly one `primary_family`, one `primary_skill`, limited `support_skills`, and `required_gates`.
6. Decide whether the requested turn is architecture-sensitive: feature/model/pipeline/artifact, alpha-search framing, stage transition, repo-scoped skill, agent setting, or Korean encoding work.
7. Decide whether the requested turn is exploration-sensitive: alpha search, idea variants, Tier B/C research, WFO planning, extreme sweep, negative-result closure, or user-requested extra stage.
8. Decide whether the requested turn is run-evidence-sensitive: run creation, run closeout, KPI report, result summary, result judgment, or run registry update.
9. Decide whether the requested turn is reproducibility-sensitive: clean checkout, dependency, CI, artifact path, MT5 terminal path, or external environment setup.

## Must Read

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md` when the current read needs support
- the active stage `04_selected/selection_status.md`
- `docs/policies/agent_trigger_policy.md`
- `docs/policies/branch_policy.md`
- the latest durable decision memo only when it changes current meaning or the user asks why
- `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the requested turn is architecture-sensitive
- `docs/policies/exploration_mandate.md`, `docs/registers/idea_registry.md`, and `docs/registers/negative_result_register.md` when the requested turn is exploration-sensitive
- `docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, `docs/policies/result_judgment_policy.md`, and `docs/registers/run_registry.csv` when the requested turn is run-evidence-sensitive

## Must Output

For low-risk `information_only` turns(낮은 위험 정보 작업), output(출력)은 compact(압축)할 수 있다. For code/experiment/MT5/policy/publish/ambiguous work(코드/실험/MT5/정책/발행/애매한 작업), expand the fields below.

- `intake_context`
- `current_truth_reference`
- `branch_worktree_fit`
- `branch_action`
- `active_stage`
- `work_packet_lifecycle`
- `primary_family_candidate`
- `routing_handoff`: the exact handoff to `obsidian-work-packet-router`
- `sensitivity_flags`: architecture, exploration, run_evidence, reproducibility, policy_skill_governance as applicable
- `allowed_scope`
- `stop_conditions`
- `publish_default`
- `final_answer_filter`

The router, not intake, owns final `primary_family`, `primary_skill`, `support_skills`, `skills_selected`, `skills_not_used`, `required_skill_receipts`, and `required_gates`. Intake may suggest them only as candidates.

## Do Not

- repeat full cold re-entry inside the same stable thread when a narrower delta check is enough
- invent a new active stage or reopen a closed stage from chat momentum alone
- let orientation docs outrank `workspace_state.yaml`, stage selection status, or durable decisions
- drift from status intake straight into implementation without first fixing the lifecycle and skill route
- work on a branch/worktree whose scope does not match the requested stage, PR, experiment, or policy packet
- treat code, experiment, evidence, and report as mutually exclusive categories
- stop after code edits when the request naturally requires verification, evidence, judgment, or user-facing explanation
- ignore architecture debt when the turn touches feature/model/pipeline/artifact, alpha-search, stage-transition, skill, agent-setting, or encoding work
- let promotion/runtime discipline block exploration before classifying the lane
- treat promotion-ineligible ideas as worthless ideas
- treat a run as reviewed or closed before measurement, management, and judgment are named

## Stop Conditions

- `workspace_state.yaml` and the active stage `selection_status.md` disagree on the active stage
- a durable decision memo contradicts the supposed current boundary
- the requested turn would cross from status or planning into implementation without an approved lifecycle packet
- the current branch/worktree is scoped to different work and switching would risk mixing unrelated changes

## Verification

- check that the named active stage is the same across the current truth sources you used
- check that the branch/worktree matches the requested work packet, or record the switch/new-branch/stop decision
- if a current task packet already exists, confirm it still fits the active stage and current durable decisions
- confirm that `obsidian-work-packet-router` receives the lifecycle and candidate `primary_family` unless the turn is strictly informational
- if architecture-sensitive, confirm whether the architecture guard validator is part of the verification surface
- if exploration-sensitive, confirm whether `obsidian-lane-classifier` and `obsidian-exploration-mandate` are part of the planning surface
- if run-evidence-sensitive, confirm whether `obsidian-run-evidence-system` is part of the planning surface

## Completion Criteria

- one lifecycle and one candidate `primary_family` are named, even if the lifecycle contains several phases
- branch/worktree fit is explicit before file edits
- the allowed scope and publish default are explicit enough that the next step can stay narrow
- skill selection is handed to the router instead of being attached broadly during intake
- `obsidian-answer-clarity` and `obsidian-claim-discipline` are named as the final user-facing filter when an answer will be sent
- architecture-sensitive work is routed to `obsidian-architecture-guard` regardless of active stage number
- exploration-sensitive work is routed by lane rather than by active stage number
- run-evidence-sensitive work is routed to measurement, management, and judgment rules before closeout
```

### .agents\skills\obsidian-stage-transition\SKILL.md

```text
---
name: obsidian-stage-transition
description: Open, close, or hand off stages in Project Obsidian Prime v2 without state fragmentation. Use when active_stage changes, a stage is closed, or work is passed to the next foundation stage.
---

# Obsidian Stage Transition

Use this skill whenever a stage opens, closes, or hands work to another stage.

## Automatic Bundle

When this skill triggers for stage transition(단계 전환), active_stage(활성 단계) change, closeout(종료), handoff(인계), workspace_state(작업공간 상태), selection status(선택 상태), or registry(등록부) sync, pair it with `obsidian-claim-discipline`.

Effect(효과): same-pass sync(같은 회차 동기화)와 claim boundary(주장 경계)를 함께 지켜서 단계 상태가 조각나지 않는다.

## Required Sync Pass

Use the canonical same-pass sync norm from `docs/policies/agent_trigger_policy.md`.

Update in the same pass:

- `docs/workspace/workspace_state.yaml`
- `docs/context/current_working_state.md`
- current or closing stage `04_selected/selection_status.md`
- current or closing stage `03_reviews/review_index.md` when needed
- next stage `00_spec/stage_brief.md`
- next stage `01_inputs/input_refs.md`
- `docs/decisions/*.md` when the transition is durable
- `docs/registers/artifact_registry.csv` when dataset, bundle, runtime, or report identity rows are added or superseded
- `docs/registers/run_registry.csv` when run identity, result status, or result judgment changes durably
- `docs/workspace/changelog.md`
- `README.md` when it still contains mutable stage, closure, or current-mode wording that this transition would otherwise leave stale
- `docs/policies/architecture_invariants.md` and `docs/registers/architecture_debt_register.md` when the transition changes feature/model/pipeline/artifact ownership, alpha-search framing, or encoding-sensitive agent behavior
- `docs/policies/exploration_mandate.md`, `docs/registers/idea_registry.md`, and `docs/registers/negative_result_register.md` when the transition opens, closes, archives, or hands off exploration work
- `docs/policies/kpi_measurement_standard.md`, `docs/policies/run_result_management.md`, and `docs/policies/result_judgment_policy.md` when the transition changes run evidence rules or closes a stage based on run results

## Transition Rules

1. Never close a stage by implying later-stage evidence is already complete.
2. Give every remaining blocker an explicit downstream home.
3. Preserve the difference between:
   - planning closure
   - dataset-contract closure
   - runtime parity closure
   - artifact identity closure
4. Keep `active_stage` aligned everywhere after the transition.
5. Derive current and next stage names from `docs/workspace/workspace_state.yaml`, decision memos, and stage docs; do not hard-code the active stage name in this skill.
6. Prefer replacing volatile `README.md` status snapshots with pointers to the authoritative current-truth docs instead of maintaining a second live-state ledger there.
7. Do not let a new stage inherit registered architecture debt as if it were normal project style.
8. If the transition opens alpha search, separate source cleanup or validation debt closure from the actual alpha-search question.
9. If the transition opens a user-requested extra stage, require charter, lane, question, allowed evidence, exit condition, and no-promotion boundary unless a promotion packet is explicitly opened.
10. If the transition closes exploration, require negative-result memory or a positive archive record before treating the idea as durable knowledge.
11. If the transition closes a run-producing stage, require run measurement, managed identity, and lane-aware judgment for the selected or archived run evidence.

## Validation

- after the sync pass, verify that `docs/workspace/workspace_state.yaml`, `docs/context/current_working_state.md`, and the active stage `selection_status.md` all name the same active stage
- if the transition changes durable meaning, make sure a `docs/decisions/*.md` memo exists in the same pass
- if architecture-sensitive docs or skills changed, run the architecture guard validator
- if exploration-sensitive docs or skills changed, verify that lane routing, WFO default, and failure-memory references are still linked from the trigger policy
- if run evidence docs or skills changed, verify that KPI measurement, run-result management, and result judgment references are still linked from the trigger policy

## Project-Specific Guardrails

- Do not hard-code durable ownership to a numbered stage.
- Derive each stage's current question, closure boundary, and handoff meaning from `docs/workspace/workspace_state.yaml`, the active stage docs, and durable decision memos.
- Do not pull runtime parity, artifact identity, or operating-promotion meaning into a stage unless the current truth sources explicitly put that work in scope.
```

### .agents\skills\obsidian-workflow-drift-guard\SKILL.md

```text
---
name: obsidian-workflow-drift-guard
description: Prevent work from drifting away from the actual blocker by separating missing material, missing tools, missing environment, missing permission, and changed goals. Use when a task risks processing absent data, pretending an unavailable tool ran, or turning a tool-building task into unrelated validation.
---

# Obsidian Workflow Drift Guard

Use this skill when the work may drift from the original job into a nearby but different job.

## Automatic Bundle

Trigger automatically when source material(원재료), tool(도구), environment(환경), permission(권한), MT5 output(MT5 출력), external verification(외부 검증), or recovery(복구) is missing, broken, unavailable, or uncertain.

Effect(효과): blocker(차단 사유)를 source material(원재료), tool(도구), environment(환경), permission(권한), code(코드), or unclear goal(불명확한 목표)로 나누고, 가능한 recovery(복구)나 retry(재시도)를 먼저 시도한다.

## Simple Model

Think of making pottery:

- material: the clay or source data
- tool: the kiln, code path, library, MT5 terminal, or runner
- environment: the place where the tool can really run
- product: the artifact or answer we are trying to make

Do not process clay that does not exist. Do not pretend to fire pottery without a kiln. Do not spend the whole pass re-checking clay when the real blocker is that the kiln is missing.

## Required Check

Before changing direction, identify:

- `product`: what are we trying to produce?
- `material_state`: available, missing, partial, or unknown
- `tool_state`: available, missing, broken, or wrong environment
- `environment_state`: usable, unavailable, unverified, or not required
- `current_blocker`: material, tool, environment, permission, code, or unclear goal
- `next_action`: continue, fetch material, build tool, fix environment, lower claim, or ask user
- `drift_risk`: what nearby task could distract from the real blocker?

## Material Recovery Order

If required material is missing, do not stop at "design is still possible" when the requested product needs that material.

Use this order:

1. Check whether the material already exists inside the current repo or declared current-project data root.
2. Check whether a current repo tool can regenerate it.
3. Check whether the required source data exists inside the current project boundary.
4. If the material cannot be recovered inside the current project boundary, mark the task `blocked` or lower the claim.
5. Do not use legacy snapshots, external folders, old project outputs, forum files, or ad hoc internet artifacts unless the user explicitly asks.

External or legacy material is not a default fallback.

## Recovery Action Rule

Missing required material, tools, or environment is not a reason to abandon or quietly defer the original task.

Use this order:

1. If Codex can restore, regenerate, install, configure, fetch, create, patch, or run the required current-project material or tool within available permissions, do that first.
2. If the current tool is stale, wrong-surface, or missing, create or patch the narrow current-project tool before reporting `blocked`.
3. If an external runtime check is required, execute the narrowest real runtime check that can produce the requested artifact or failure log.
4. If user action is required, ask for the exact action and explain what work resumes after it is done.
5. After recovery, return to the original product instead of drifting into a new task.
6. Only mark the task blocked when neither Codex action nor a clear user action can complete the prerequisite in the current pass.

Example: if MT5 installation, broker login, terminal setup, or account connection is required, ask the user for that setup explicitly. Once available, resume the current project regeneration or verification path.

## Pre-Blocked Evidence Rule

Before writing `blocked`, produce at least one of these evidence types:

- `recovery_attempt`: the exact source material(원재료), tool(도구), or environment(환경) recovery tried in the current pass
- `created_or_patched_tool`: the current-project tool created or patched to remove the blocker
- `execution_attempt`: the command, terminal action, MT5 run, strategy tester run, or script invocation that tried to produce the requested output
- `failure_log`: the error, missing terminal state, permission failure, or unavailable environment that stopped the run
- `required_user_action`: the exact user action needed, with the resume point after it is done

Effect(효과): `blocked(차단)` means the pass tried the narrow recovery path first, not merely that the missing work was noticed.

## MT5 Runtime Rule

For MT5(`MetaTrader 5`, 메타트레이더5), MetaEditor compile(메타에디터 컴파일) is not enough when the requested product is MT5 snapshot(MT5 스냅샷), terminal file output(터미널 파일 출력), strategy tester output(전략 테스터 출력), or runtime parity(런타임 동등성).

Required behavior:

1. If the checked-in MQL5 tool is stale, create or patch a narrow current-project script/EA before blocked reporting.
2. Try to run it through the available terminal path, command-line path, or explicit user terminal action.
3. If Codex cannot drive the MT5 terminal, ask for the exact terminal action and name the output file that should appear.
4. Report `blocked` only with recovery attempt(복구 시도), execution attempt(실행 시도), failure log(실패 로그), or required user action(필요 사용자 행동).

## Guardrails

- If source data is missing, do not create processed outputs as if the source data existed.
- If the required tool or runtime is missing, do not simulate success unless the task is explicitly to create a mock.
- If the job is to build a tool, do not turn the pass into repeated source-data auditing unless new evidence makes that necessary.
- If material is required and missing, name the shortest current-project path to restore or regenerate it.
- If Codex can remove the blocker within available permissions, remove it before reporting `blocked`.
- If user cooperation is required, ask for the exact setup, credential, local data, terminal action, or permission needed and state the resume point.
- If verification cannot run, name whether the blocker is material, tool, environment, or permission.
- Do not treat compile-only evidence as runtime output when the requested artifact is a runtime snapshot or terminal-generated file.
- If the original goal changes, say that it changed before proceeding.
- Do not close the task with a polished report that only explains why the real work did not happen.

## Good Outcome

The user should be able to tell:

- what was supposed to be made
- what was actually available
- what was missing
- whether the work stayed on target
- what single next action removes the blocker
```

### .agents\skills\obsidian-work-packet-router\SKILL.md

```text
---
name: obsidian-work-packet-router
description: Route each Project Obsidian Prime v2 request as a multi-phase work packet across design, code, experiment, verification, evidence, judgment, report, and publish phases; use project-wide and never bind routing to one stage.
---

# Obsidian Work Packet Router

Use this skill after session intake and before planning or implementation.

Most Obsidian requests are not one mode. A normal request may start with an idea, write code, run an experiment, record evidence, judge results, and explain the outcome to the user. Route the whole lifecycle before acting.

## Must Read

- `docs/policies/agent_trigger_policy.md`
- `docs/policies/branch_policy.md`
- `docs/policies/reentry_order.md` when current truth is uncertain
- `AGENTS.md`
- The SKILL.md files for any selected skills

## Required Output

- Always emit(항상 남김) `routing_receipt(라우팅 기록)`: lifecycle(생명주기), `primary_family(주 작업군)`, `primary_skill(주 스킬)`, selected `support_skills(보조 스킬)`, `required_gates(필수 게이트)`, and structured not-selected reasons(구조화된 미선택 사유)를 담은 compact record(압축 기록).
- `work_packet_lifecycle`: one of `information_only`, `design_only`, `code_to_verify_to_report`, `experiment_to_evidence_to_report`, `code_to_experiment_to_evidence_to_report`, `policy_skill_governance`, `publish_or_handoff`, or a short custom lifecycle(짧은 사용자 정의 생명주기)
- `phase_plan`: ordered phases(순서 있는 단계) for the current packet(현재 작업 묶음); low-risk `information_only`(낮은 위험 정보 작업)는 compact(압축), code/experiment/MT5/policy/publish/ambiguous work(코드/실험/MT5/정책/발행/애매한 작업)는 expanded(확장)
- `primary_family`: exactly one family(작업군) from `docs/agent_control/work_family_registry.yaml`
- `primary_skill`: exactly one primary skill(주 스킬) from that family
- `support_skills`: only the family-supported skills(보조 스킬) actually needed for this packet
- `skills_considered`: high-relevance repo-scoped skills(저장소 전용 스킬) considered for this packet
- `skills_selected`: normalized list(정규화 목록) equal to `primary_skill` followed by selected `support_skills`
- `skills_not_used`: attached(선택)하지 않은 high-relevance skills(고관련 스킬) with structured reasons such as `not_primary_family_required_skill`, `not_required_for_read_only`, or `enforced_as_required_gate_not_support_skill`; do not use vague "implicitly satisfied" wording
- `required_skill_receipts`: receipt-required skills(영수증 필수 스킬), matching `skills_selected` unless a gate explicitly enforces the responsibility
- `required_gates`: gates(게이트) that must execute in closeout or be declared N/A with a reason
- `branch_worktree_fit`: whether the current branch/worktree matches the requested packet
- `branch_action`: stay, switch, create_new_branch, create_or_select_worktree, or stop_for_user
- `phase_stop_conditions`: where to stop or downgrade claims
- `final_answer_filter`: normally `obsidian-answer-clarity` plus `obsidian-claim-discipline`
- `handoff_surface`: files, registers, PR, artifact, or user action touched by the packet

## Default Phase Library

- reentry and current truth: `obsidian-reentry-read`
- lifecycle routing: `obsidian-session-intake`, then this skill
- branch/worktree fit: `docs/policies/branch_policy.md`
- architecture or policy: `obsidian-architecture-guard`
- code placement: `obsidian-code-surface-guard`
- implementation quality: `obsidian-code-quality`
- external correctness: `obsidian-reference-scout`
- experiment design: `obsidian-experiment-design`
- data and time integrity: `obsidian-data-integrity`
- model or threshold validation: `obsidian-model-validation`
- MT5 or live-like parity: `obsidian-runtime-parity`
- tester evidence: `obsidian-backtest-forensics`
- run evidence and registers: `obsidian-run-evidence-system`
- artifact lineage: `obsidian-artifact-lineage`
- environment reproducibility: `obsidian-environment-reproducibility`
- KPI explanation: `obsidian-performance-attribution`
- result boundary: `obsidian-result-judgment`, then `obsidian-claim-discipline`
- final user report: `obsidian-answer-clarity`

## Do Not

- Treat code, experiment, evidence, and report as mutually exclusive.
- Stop at code generation when the user asked for work that naturally requires verification or reporting.
- Work in a branch or worktree that belongs to a different stage, PR, experiment, or policy scope.
- Mix two open PR scopes in one worktree unless the user explicitly asks for that combined patch.
- Create stage-specific routing skills when a project-wide lifecycle responsibility fits.
- Skip answer clarity because a result is technically correct.
- Skip reference scouting silently; record why it was not required.
- Select broad automatic skill groups. The router chooses one primary family, one primary skill, and only the support skills that materially change execution or closeout evidence.
- Replace(대체) the compact routing receipt(압축 라우팅 기록)를 unrecorded private decision(기록 없는 내부 판단)으로 바꾸지 않는다; receipt(기록)는 abandoned skills(유기되는 스킬)을 막는 guard(가드)다.
```


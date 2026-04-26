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

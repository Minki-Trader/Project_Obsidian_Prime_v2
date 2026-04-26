# Tiered Readiness Exploration

티어 라벨(tier label, 티어 라벨)은 표본(sample, 표본)을 설명한다.

티어(tier, 티어)는 탐색 허가(exploration permission, 탐색 허가)를 결정하지 않는다.

## 라벨(Labels, 라벨)

- `Tier A(티어 A)`: 전체 문맥 표본(full-context sample, 전체 문맥 표본)
- `Tier B(티어 B)`: 부분 문맥 표본(partial-context sample, 부분 문맥 표본)
- `Tier C(티어 C)`: 약한 표본(weak sample, 약한 표본), 스킵 표본(skip sample, 스킵 표본), 또는 명시적으로 허용된 로컬 연구 표본(local-research sample, 로컬 연구 표본)

## Tier B 하위유형(Tier B Subtypes, Tier B 하위유형)

Tier B(티어 B)는 하나의 깨끗한 56-feature surface(56개 피처 표면)가 아니다. Stage 10(10단계) 이후 fallback(대체)은 Tier A(티어 A)가 비운 구간 중 Tier B 자체의 core feature surface(핵심 피처 표면)가 유한한 행을 쓴다.

Tier B fallback(티어 B 대체)은 반드시 partial-context subtype(부분 문맥 하위유형)을 남긴다.

- `B_macro_missing(B 거시 결측)`: macro context(거시 문맥)가 비었지만 core(핵심)가 가능하다.
- `B_constituent_missing(B 구성종목 결측)`: constituent context(구성종목 문맥)가 비었지만 core(핵심)가 가능하다.
- `B_basket_missing(B 바스켓 결측)`: basket context(바스켓 문맥)가 비었지만 core(핵심)가 가능하다.
- `B_core_only(B 핵심만)`: 보조 문맥이 거의 없고 core(핵심)만 가능하다.
- `B_mixed_partial_context(B 혼합 부분 문맥)`: 둘 이상의 문맥 그룹(context group, 문맥 그룹)이 부분적으로 빠져 있다.
- `B_full_context_outside_tier_a_scope(B 전체문맥이나 Tier A 밖)`: Tier B 문맥은 차 있지만 Tier A strict scope(Tier A 엄격 범위) 밖이다.

Tier B core(티어 B 핵심)도 유한하지 않으면 `no_tier(티어 없음)`로 기록한다. 효과(effect, 효과)는 Tier A all skip(Tier A 전체 스킵)을 Tier B가 메우되, 정말 약한 표본은 조용히 거래 표본으로 섞지 않는 것이다.

## 탐색 규칙(Exploration Rule, 탐색 규칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색할 수 있다.

보고서(report, 보고서)는 티어 라벨(tier label, 티어 라벨)을 보존해야 한다. 그래야 결과(result, 결과)를 과하게 읽지 않는다.

## 동시 기록 규칙(Paired Record Rule, 쌍 기록 규칙)

알파 탐색(alpha exploration, 알파 탐색)에서는 Tier A(티어 A)와 Tier B(티어 B)를 항상 같은 실행 묶음(run packet, 실행 묶음) 안에서 기록한다.

각 실행(run, 실행)은 아래 세 가지 view(보기)를 남긴다.

- `tier_a_separate(Tier A 분리)`
- `tier_b_separate(Tier B 분리)`
- `tier_ab_combined(Tier A+B 합산)`

효과(effect, 효과)는 Tier A(티어 A)와 Tier B(티어 B)가 서로 다른 표본(sample, 표본)이라는 사실을 보존하면서도, 전체 판독(combined read, 합산 판독)을 따로 비교할 수 있게 하는 것이다.

Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) routed run(라우팅 실행)에서는 위 세 가지 view(보기)를 각각 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 읽는다.

효과(effect, 효과)는 부분 문맥 표본(partial-context sample, 부분 문맥 표본)이 실제로 빈 구간을 메웠는지 확인하면서, 합산 판독(combined read, 합산 판독)을 separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)으로 오해하지 않게 하는 것이다.

Tier B(티어 B)가 아직 물질화되지 않았거나 결합 기록(combined record, 합산 기록)이 없으면 그 상태를 빈칸으로 두지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, 또는 `out_of_scope_by_claim(주장 범위 밖)`로 명시한다.

## 운영 규칙(Operating Rule, 운영 규칙)

운영 사용(operational use, 운영 사용)은 별도 질문(separate question, 별도 질문)이다. 티어 탐색 결과(tiered exploration result, 티어 탐색 결과)는 그 자체로 실거래 준비(live-ready, 실거래 준비)가 아니다.

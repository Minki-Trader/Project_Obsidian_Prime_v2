# Exploration Mandate (탐색 명령)

This policy defines how Project Obsidian Prime v2 inherits the legacy exploration spirit (레거시 탐색 정신) without inheriting legacy code, run results, or promotion history (레거시 코드/런 결과/승격 이력).

## Core Rule (핵심 규칙)

- v2 inherits the exploration mandate (탐색 명령): create ideas freely, push serious ideas to a meaningful boundary, and preserve failed ideas as reusable evidence.
- v2 does not inherit legacy code, run results, winners, challengers, operating defaults, KPI choices, or promotion history.
- Legacy material is prior evidence only (과거 근거 전용). It may inspire an abstract lesson, but it must not become a shortcut to v2 truth.
- Promotion-ineligible (승격 부적격) does not mean idea-dead (아이디어 사망); write `promotion-ineligible` explicitly when a candidate is blocked only at the operating-promotion boundary.
- Exploration may be unconstrained in idea generation, but it must be constrained in memory (기록).

## Progressive Hardening (점진적 경화)

- Early exploration or scout work (초기 탐색 또는 스카우트 작업) may start with partial evidence when the missing evidence is labeled.
- `promotion_candidate` (승격 후보) means a candidate can be studied without claiming incumbent replacement (현행선 교체).
- `runtime_probe` (런타임 탐침) means runtime observation is allowed without claiming parity closure (동등성 폐쇄).
- `operating_promotion` (운영 승격) and `runtime_authority` (런타임 권위) are the hard-gate surfaces; they require the relevant parity, artifact, runtime, and decision evidence before they can be claimed.
- Missing WFO, full parity, or runtime closure should label the result boundary, not kill the idea by default.

## Lane Separation (레인 분리)

Every non-trivial task must name one primary lane (주 레인):

- `exploration` (탐색): generate, mutate, stress, and learn from ideas.
- `evidence` (근거): make results comparable, inspectable, and reusable.
- `promotion` (승격): decide whether a candidate can replace or confirm the operating line.
- `runtime` (런타임): verify execution, parity, packaging, and environment behavior.
- `extra` (추가): user-requested side stage or non-standard question that must still declare its own charter.

Operating discipline (운영 규율) applies to `operating_promotion` and `runtime_authority`. `promotion_candidate` and `runtime_probe` may open earlier when their evidence boundary is explicit. Exploration discipline (탐색 규율) applies to `exploration` and asks whether the idea was pursued, stressed, learned from, and recorded.

## Idea Lifecycle (아이디어 생애주기)

Use this default lifecycle for alpha search (알파 탐색), tiered readiness research (계층 준비도 연구), and idea variants (아이디어 변형):

1. `seed` (씨앗): define the hypothesis, source of inspiration, and what would make the idea interesting.
2. `broad_sweep` (광역 탐색): test coarse ranges and distinct structural variants before fine tuning.
3. `extreme_sweep` (극단값 탐색): test intentionally wide or uncomfortable parameter values to expose cliffs, saturation, and failure boundaries.
4. `wfo` (워크포워드 최적화): prefer rolling or expanding walk-forward optimization instead of optimizing one favored window.
5. `stress_readout` (스트레스/판독): summarize regime sensitivity, data-readiness tier behavior, drawdown, trade count, and failure modes.
6. `promote_no_promote_archive` (승격/비승격/보관): close with promotion, no-promotion, or archive, but always record salvage value and reopen condition.

## Search Granularity (탐색 입도)

- Start coarse. Fine tuning before broad coverage is a search smell (탐색 냄새).
- Extreme sweep is encouraged when it teaches boundaries, failure modes, or invariance.
- Micro search (미세 탐색) without a robust region (견고한 구간) may only be labeled as scout-only (탐색 전용); it must not be described as robust evidence.
- Do not spend a stage shaving tiny parameter increments unless the expected effect is named and the prior sweep shows the region is worth refining.
- Record discarded ranges when they teach a durable constraint.

## WFO Default (워크포워드 최적화 기본값)

- WFO (워크포워드 최적화) is the default optimization frame for robust exploration evidence.
- Single-window optimization (단일 구간 최적화) is allowed as a scout read (탐색 판독) or an explicitly justified exception.
- Do not present a 2025-heavy optimized result as robust without WFO, reverse-window, or independent OOS (표본외) support.
- A WFO packet should record the in-sample window (표본내 구간), out-of-sample window (표본외 구간), roll cadence (이동 주기), selection rule (선택 규칙), catastrophic veto (치명적 거부 조건), and locked final read (고정 최종 판독).

## Multiple Testing Discipline (다중 검정 규율)

- Large idea sweeps increase selection bias (선택 편향) and backtest overfitting (백테스트 과최적화) risk.
- Use stable regions, majority-pass logic, catastrophic vetoes, and negative result logging before trusting a best run.
- When many variants were tried, say so. Do not report only the winner as if it was the only trial.
- Preferred concepts include Deflated Sharpe Ratio (축소 샤프 비율), White Reality Check (화이트 현실성 검정), WFO with independent OOS (독립 표본외), and purged or leakage-aware validation (누수 방지 검증).

References (참고 근거):

- David Bailey and Marcos Lopez de Prado, Deflated Sharpe Ratio (축소 샤프 비율): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- Halbert White, Reality Check for Data Snooping (데이터 스누핑 현실성 검정): https://www.ntuzov.com/Nik_Site/Niks_files/Research/papers/mut_funds/White_2000.pdf
- Mroziewicz and Slepaczuk, WFO double OOS study (WFO 이중 표본외 연구): https://arxiv.org/abs/2602.10785
- Pham et al., Alpha Research Framework (알파 연구 프레임워크): https://arxiv.org/abs/2603.09219

## Tiered Readiness Exploration (계층 준비도 탐색)

- Tier A (티어 A) remains the strict full contract-ready lane (완전 계약 준비 레인) for operating-promotion or runtime-authority comparison.
- Tier B (티어 B) is a partial external-context exploration lane (부분 외부 문맥 탐색 레인), not a relaxed spelling of Tier A.
- Tier C (티어 C) is runtime skip (런타임 스킵) by default.
- If base and session semantics are valid but external context is absent, Tier C may support `tier_c_local_research` (티어 C 로컬 연구) for indicator-only model or logic research (지표 전용 모델/로직 연구).
- `tier_c_local_research` is not a trading lane (거래 레인), reduced-risk substitution (위험축소 대체), or promotion argument (승격 논거).

## Failure Memory (실패 기록)

An idea may be closed only after it records:

- hypothesis (가설)
- variants tried (시도한 변형)
- failed boundary (실패 경계)
- why failed (실패 이유)
- salvage value (회수 가치)
- reopen condition (재개 조건)
- do-not-repeat note (반복 금지 메모)

Use `docs/registers/negative_result_register.md` for durable negative results and `docs/registers/idea_registry.md` for active or archived ideas.

## Extra Stage Rule (추가 단계 규칙)

User-requested extra stages are allowed. An extra stage must declare:

- charter (헌장)
- primary lane (주 레인)
- question (질문)
- allowed evidence (허용 근거)
- exit condition (종료 조건)
- no-promotion boundary (비승격 경계) unless the user explicitly opens a promotion packet

An extra stage must not silently bypass Tier A/B/C, WFO defaults, artifact identity discipline, or runtime parity requirements.

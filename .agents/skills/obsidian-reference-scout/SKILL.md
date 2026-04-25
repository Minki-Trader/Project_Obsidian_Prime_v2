---
name: obsidian-reference-scout
description: Find and use external references for correct API usage, syntax, implementation patterns, MQL5 behavior, library behavior, quant methods, and idea scouting. Use when project memory is not enough, an API may be version-sensitive, or alpha/research ideas need external examples.
---

# Obsidian Reference Scout

Use this skill when outside references can improve correctness or idea quality.

This skill is for scouting and grounding, not copying.

## Automatic Code-Writing Pair

For every code-writing packet(code-writing packet, 코드 작성 묶음), run this scout beside `obsidian-code-surface-guard(코드 표면 가드)`.

Use external lookup(외부 확인) when the code touches MQL5/MT5(MetaTrader 5, 메타트레이더5), MetaEditor(메타에디터), strategy tester(전략 테스터), file handoff(파일 인계), external API(외부 API), CLI, or library behavior(라이브러리 동작) such as pandas/sklearn/numpy/LightGBM.

If the code is pure internal logic(순수 내부 로직) with no uncertain API(API 사용법), syntax(구문), version-sensitive behavior(버전 민감 동작), or external pattern(외부 패턴), record `reference_scout: not_required(레퍼런스 탐색 불필요)` with the reason(reason, 이유).

Effect(effect, 효과): implementation(구현)을 프로젝트 기억(project memory, 프로젝트 기억)만으로 단정하지 않고, 필요한 곳에서는 official docs(공식 문서)나 maintained source(유지보수되는 원천)로 접지한다.

## When To Use

- correct function, API, or syntax usage is uncertain
- library behavior may depend on version
- MQL5 or MT5 tester behavior is unclear
- LightGBM, pandas, sklearn, numpy, or another library usage needs confirmation
- implementation patterns from maintained GitHub projects may help
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

## Guardrails

- Prefer official docs for API and syntax questions.
- Do not copy external code wholesale into this repo.
- Do not trust forum performance claims as evidence.
- Do not let external examples override project contracts for time axis, dataset identity, split policy, artifact identity, or runtime authority.
- If a source is old, version-specific, or unclear, say so.
- If browsing or source lookup was not performed, do not present the answer as externally verified.

## Example

If MQL5 file handoff behavior is unclear, scout official MQL5 docs first, then relevant forum or GitHub examples. The useful result might be a pattern such as waiting for file size stability, but the implementation still needs to fit this project's runtime parity and artifact identity rules.

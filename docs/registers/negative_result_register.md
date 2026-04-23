# Negative Result Register (부정 결과 등록부)

This register stores failed or closed hypotheses (실패/폐쇄 가설) as reusable evidence, not waste. It must not import legacy run results as current v2 truth.

| result_id | idea_id | hypothesis (가설) | failed_boundary (실패 경계) | why_failed (실패 이유) | salvage_value (회수 가치) | reopen_condition (재개 조건) | do_not_repeat (반복 금지) | last_reviewed |
|---|---|---|---|---|---|---|---|---|
| `N-001` | `legacy_prior` | MT5 built-in ATR and Stochastic paths are close enough to serve as contract-equivalent model inputs. | Legacy Stage 41 targeted feature snapshot audit. | Localized feature parity stayed materially open until those paths were replaced with contract-matching implementations. | Keep contract-matching feature logic as the default for parity-sensitive model inputs. | New evidence that a built-in path is provably contract-equivalent on the full audited surface. | Do not assume MT5 built-ins are contract-equivalent without parity evidence. | `2026-04-16` |
| `N-002` | `legacy_prior` | Broad new alpha search should start before parity and artifact-governance foundation is reset. | Legacy Stage 40 to 42 learning chain and the v2 restart decision. | It increases confusion about whether losses come from model quality, runtime drift, or undocumented artifact identity. | Keep foundation closure separate from alpha search, while preserving exploration as the downstream goal. | Stage 00 to Stage 05 foundation gates close and the first v2 exploration packet is explicitly opened. | Do not use foundation debt closure as a substitute for actual alpha-search questions. | `2026-04-16` |

## Use Rule (사용 규칙)

- Close an exploration idea only after recording `why_failed`, `salvage_value`, and `reopen_condition`.
- Mark legacy-derived entries as `legacy_prior` or tie them to a v2 `idea_id`; never treat them as current v2 truth by default.
- A negative result can block promotion (승격 차단) without killing the idea forever.

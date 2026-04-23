# Legacy Lesson Register (레거시 교훈 등록부)

This register preserves abstract lessons (추상 교훈) from legacy work while blocking direct legacy inheritance (직접 레거시 승계).

| lesson_id | legacy_source (레거시 출처) | abstract_lesson (추상 교훈) | allowed_use (허용 사용) | forbidden_inheritance (금지 승계) | v2_policy_home (v2 정책 위치) |
|---|---|---|---|---|---|
| `LL-001` | Legacy project identity discussion and restart docs (레거시 정체성 논의 및 재시작 문서) | Serious ideas should be pushed to a meaningful boundary and failed ideas should become reusable evidence. | Shape v2 exploration discipline and failure-memory rules. | Do not copy legacy run results, winners, code paths, or stage conclusions into v2 truth. | `docs/policies/exploration_mandate.md` |
| `LL-002` | Legacy Stage 40-42 parity learning chain (레거시 40-42단계 동등성 학습) | Runtime and parity discipline must be strong at promotion/runtime boundaries. | Keep operating discipline strict for promotion and runtime lanes. | Do not let runtime conservatism block early exploration lanes by default. | `docs/policies/architecture_invariants.md` and `docs/policies/exploration_mandate.md` |
| `LL-003` | Legacy KPI and WFO concerns (레거시 KPI 및 WFO 우려) | Single favored-window optimization can hide overfit candidates and missed older ideas. | Make WFO the default exploration optimization frame. | Do not reuse legacy KPI rankings as v2 promotion evidence. | `docs/policies/exploration_mandate.md` |

## Use Rule (사용 규칙)

- Add only lessons, not legacy conclusions.
- `allowed_use` must describe an abstract design effect.
- `forbidden_inheritance` must name what cannot be copied.

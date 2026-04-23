# Stage Types

## foundation_stage

Used when the goal is to create or tighten reusable project infrastructure before new alpha work.

Typical outputs:

- workspace state updates
- registries
- templates
- fixture plans
- parity harness plans

## diagnostic_runtime_stage

Used when the goal is to localize or explain a runtime, data, or parity issue.

Rules:

- may close a question
- may shape follow-up priorities
- may not by itself promote the operating line

## regular_alpha_stage

Used when the goal is to compare operating candidates that could replace or confirm the current line.

Rules:

- must identify inherited references
- must declare primary KPI, guardrails, and disqualifiers
- must keep run evidence measurement, management, and judgment explicit before closing selected results
- may open `promotion_candidate` reads before every hard gate is closed if the evidence boundary is explicit
- must not claim `operating_promotion` without durable promotion evidence

## exploration_stage

Used when the goal is to generate, mutate, stress, or archive alpha ideas without making an operating promotion decision.

Rules:

- must declare idea hypothesis, lane, tier scope, intended sweep/WFO path or scout-only boundary, and negative-result memory rule
- must record reviewed runs through the run evidence system when results become durable
- may produce useful failure evidence without producing a promotion candidate
- must not be blocked only because operating-promotion/runtime-authority gates are not yet satisfied
- must not inherit legacy code, run results, or promotion history

## extra_stage

Used when the user asks for a non-standard side question outside the current default stage path.

Rules:

- must declare charter, lane, allowed evidence, exit condition, and no-promotion boundary
- may not bypass Tier A/B/C, WFO defaults, artifact identity, or runtime parity rules
- must record whether its result updates run, idea, negative-result, or legacy-lesson memory

## runtime_recalibration_stage

Used when the model/rule family stays frozen and only a bounded runtime gate or policy surface is rechecked.

Rules:

- scope must stay narrow
- alpha family stays frozen
- handoff and parity caveats stay explicit
- `runtime_probe` may observe behavior without claiming `runtime_authority`

## handoff_stage

Used when the goal is to verify shared runtime packaging, reproduction, or operational readiness.

Rules:

- handoff verification is not the same as full parity closure
- operational meaning must be documented separately from raw research performance
- do not claim `runtime_authority` until the relevant closure evidence exists

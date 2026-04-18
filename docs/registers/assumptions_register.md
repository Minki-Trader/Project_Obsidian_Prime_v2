# Assumptions Register

| ID | Assumption | Why It Matters | Break Signal | Status | Last Reviewed |
|---|---|---|---|---|---|
| `A-001` | `foundation/config/top3_monthly_weights_fpmarkets_v2.csv` is still a placeholder input until real monthly weights are supplied. | Any dataset freeze or bundle built on it needs that caveat preserved. | Real monthly weights arrive or the placeholder is replaced. | `open` | `2026-04-16` |
| `A-002` | The provisional shared v2 working window is `2022-08-01` through `2026-04-13` inclusive until the first v2 dataset freeze is written. | New threads need one default window before the first freeze card exists. | Stage 00 records a different frozen window and fingerprint. | `closed` | `2026-04-18` |
| `A-003` | Legacy Stage 40 to 42 parity lessons are reliable prior evidence, but they do not count as automatic v2 parity closure. | Prevents false confidence from reusing old conclusions without v2 identity and fixtures. | A v2 parity harness reproduces those findings with v2 artifacts. | `open` | `2026-04-16` |

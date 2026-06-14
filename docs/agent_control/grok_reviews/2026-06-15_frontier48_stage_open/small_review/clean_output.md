**1. verdict:** `accepted`

**2. train_split_only_construction_lock:** `yes`

**3. claim_boundary_ok:** `yes`

**4. one risk:** Fixed non-percentile state gates may still smuggle F47 percentile semantics (for example p72/p82-style cutoffs) in through reference-only tuning, so the mechanism change becomes label-only while selection pressure stays inherited.

**5. one repair suggestion:** Before any sweep, write a gate provenance table: each threshold must be tagged `train_only_fit`, `fixed_design_constant`, or `archived_clue_no_selection`; anything else is blocked from the repair lane.

# Do Not Repeat(반복 금지)

- `locked_decision_contract`: edge_margin only, train-only target8 only, no validation/OOS calibration
- `pre_registered_label_spec`: three label variants fixed before Frontier16B metrics
- `density_transfer_audit`: label, argmax, and edge_margin__target8 density by split
- `do_not_repeat_registry`: no F15 9-cell grid, no validation-guided filtering, no density-as-edge claim
- `variant_cap`: three label variants only, no post-hoc knob addition
- `no_repair_ladder`: no F14/F15 repair ladder inside Frontier16B
- `prior_stage_overlap_disclosure`: F07/F12 overlap disclosed; F16 difference recorded
- `tier_paired_records`: Tier A separate, Tier B missing_required, combined missing_required
- `onnx_parity_gate`: no strict or preserved judgment without parity pass
- `claim_boundary_lock`: proxy scout only, all forbidden claims not_claimed

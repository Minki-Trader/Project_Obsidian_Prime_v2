# Stage294 Decision(294단계 결정)

- status(상태): `completed_mt5_outcome_relabel_directional_flip_review_no_candidate_stage295_opened`
- judgment(판정): `mt5_outcome_relabel_directional_flip_runtime_probe_negative_no_adapter_no_onnx`
- decision(결정): No Stage294 package passes the ONNX-worthy candidate gate(ONNX화 가치 후보 게이트), so Stage295 opens split-consistent outcome distillation(분할 일관 결과 증류).
- next_stage(다음 단계): `295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild`

Effect(효과): OOS(표본외) 양수만으로 ONNX(온엑스)에 넘기지 않고, validation(검증) 손상을 직접 다루는 새 구조로 넘어간다.

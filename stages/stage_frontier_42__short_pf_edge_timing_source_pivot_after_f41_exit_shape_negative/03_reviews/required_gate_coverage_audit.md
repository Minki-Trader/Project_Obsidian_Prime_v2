# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- data_integrity(데이터 무결성): pass(통과), feature hash(피처 해시), split(분할), timing columns(타이밍 열) verified.
- experiment_design(실험 설계): pass(통과), F42 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) recorded.
- model_validation(모델 검증): out_of_scope_by_claim(주장 범위 밖), no model/ONNX(모델/온엑스) trained.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f42_timing_proxy`.
- result_judgment(결과 판정): pass(통과), `preserved_clue_negative_memory` only.

# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- data_integrity(데이터 무결성): pass(통과), feature hash(피처 해시), split(분할), raw path(원천 경로) verified.
- experiment_design(실험 설계): pass(통과), F43 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) recorded.
- model_validation(모델 검증): out_of_scope_by_claim(주장 범위 밖), no model/ONNX(모델/온엑스) trained.
- artifact_lineage(산출물 계보): pass(통과), source/report/ledger paths(원천/보고/장부 경로) recorded; 02_runs(실행 원자료)는 ignored_with_manifest(목록 포함 무시).
- external_review_packet(외부 검토 묶음): pass(통과), stage-open and closeout Grok(단계 개방/마감 그록) receipts recorded.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f43_trade_shape_proxy`.
- result_judgment(결과 판정): pass(통과), `negative_memory` only.

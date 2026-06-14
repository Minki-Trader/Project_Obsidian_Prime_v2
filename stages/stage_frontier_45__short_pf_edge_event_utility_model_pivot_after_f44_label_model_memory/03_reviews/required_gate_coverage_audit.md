# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- scope_completion_gate(범위 완료 게이트): pass(통과), F45 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) materialized.
- kpi_contract_audit(KPI 계약 감사): pass(통과), train/validation/OOS PF/DD/density(학습/검증/표본외 PF/DD/밀도) split rows recorded.
- skill_receipt_lint(스킬 영수증 검사): pass_with_boundary(경계 통과), obsidian-run-evidence-system(실행 근거 시스템) skill unavailable in session; equivalent run evidence artifacts recorded.
- data_integrity(데이터 무결성): pass(통과), closed-bar feature order(닫힌 봉 피처 순서), split(분할), raw path(원천 경로) verified.
- model_validation(모델 검증): exploratory(탐색), event/model/threshold choice(이벤트/모델/임계값 선택)는 train-only(학습 전용); no promotion(승격 없음).
- artifact_lineage(산출물 계보): pass(통과), input manifest/report/ledger paths(입력 목록/보고/장부 경로) recorded; 02_runs(실행 원자료)는 ignored_with_manifest(목록 포함 무시).
- external_review_packet(외부 검토 묶음): pass(통과), stage-open and closeout Grok(단계 개방/마감 그록) receipts recorded.
- runtime_parity(런타임 동등성): out_of_scope_by_claim(주장 범위 밖), `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f45_event_classifier_proxy`.
- result_judgment(결과 판정): pass(통과), `negative_memory` only.

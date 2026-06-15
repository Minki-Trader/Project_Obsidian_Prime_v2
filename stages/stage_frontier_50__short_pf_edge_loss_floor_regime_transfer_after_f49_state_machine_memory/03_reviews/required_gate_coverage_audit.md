# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- scope_completion_gate(범위 완료 게이트): pass(통과), F50 hypothesis/proxy/repair/closeout(가설/프록시/수리/마감) materialized.
- kpi_contract_audit(KPI 계약 감사): pass(통과), train/validation/OOS PF/DD/density(학습/검증/표본외 PF/DD/밀도) split rows recorded.
- skill_receipt_lint(스킬 영수증 검사): pass_with_boundary(경계 통과), obsidian-run-evidence-system(실행 근거 시스템) skill unavailable in session; equivalent run evidence artifacts recorded.
- data_integrity(데이터 무결성): pass(통과), closed-bar feature order(닫힌 봉 피처 순서), train-only frozen base scorer(학습 전용 고정 기본 채점기), loss-floor/outcome-memory context(손실 하한/결과 기억 문맥), horizon+1 embargo(예측수평+1 유예), and minimal hygiene gates(최소 위생 게이트) verified.
- model_validation(모델 검증): exploratory(탐색), base scorer/model/sequence threshold(기본 채점기/모델/순서 임계값) choice는 train-only(학습 전용); validation/OOS(검증/표본외)는 read-only(읽기 전용); no promotion(승격 없음).
- artifact_lineage(산출물 계보): pass(통과), input manifest/report/ledger paths(입력 목록/보고/장부 경로) recorded; 02_runs(실행 원자료)는 ignored_with_manifest(목록 포함 무시).
- external_review_packet(외부 검토 묶음): pass(통과), stage-open and closeout Grok(단계 개방/마감 그록) receipts recorded; closeout advice(마감 조언)는 local verification(로컬 검증) 후 accepted(수용)했다.
- runtime_parity(런타임 동등성): pass_with_observation(관찰 포함 통과), mandatory MT5 runtime probe(필수 MT5 런타임 탐침) completed as `runtime_probe_observation_no_authority`; signal_diff(신호 차이)=0 and feature_ready_diff(피처 준비 차이)=0, but DD/trade compression(손실폭/거래 압축)이 proxy(프록시)보다 크게 악화됐다.
- proxy_runtime_gap(프록시/런타임 차이): pass_recorded(기록 통과), validation_is PF/DD/trades(검증 내부 수익 팩터/손실폭/거래) 1.134967/9.4888/1282 -> 0.81/76.21/99; oos(표본외) 1.057828/15.6379/912 -> 0.99/31.52/71.
- result_judgment(결과 판정): pass(통과), `preserved_clue_negative_memory` only; weak positive proxy(약한 양수 프록시)는 MT5 runtime collapse(런타임 붕괴) 때문에 completion/baseline/promotion/runtime authority/live readiness(완성/기준선/승격/런타임 권위/실거래 준비)로 읽지 않는다.

# F71E Grok Receipt(F71E 그록 영수증)

Updated(갱신): 2026-06-16T23:40:18Z

- trigger_reason(트리거 이유): runtime semantics repair probe(런타임 의미 수리 탐침) 전 검토.
- review_size(검토 크기): medium review(중간 검토).
- direction_before_grok(그록 전 방향): F71D signal count gap(신호 수 간극)을 custom score vs EA edge margin threshold mismatch(맞춤 점수와 EA 엣지 마진 임계값 불일치)로 보고 q40 repair(수리)를 제안.
- prompt_identity(프롬프트 정체성): `docs/agent_control/grok_reviews/2026-06-17_f71e_pre_runtime_semantics_repair/prompts/f71e_pre_runtime_semantics_repair_prompt.md`.
- grok_output_identity(그록 출력 정체성): `docs/agent_control/grok_reviews/2026-06-17_f71e_pre_runtime_semantics_repair/outputs/clean_output.md`.
- advice_classification(조언 분류): accepted(수용) q40 single MT5 repair probe(단일 MT5 수리 탐침); needs_local_verification(로컬 검증 필요) q40 materialization/parity(물질화/동등성).
- local_verification(로컬 검증): F71E script(스크립트)가 q40 ONNX parity(온엑스 동등성), signal count parity(신호 수 동등성), MT5 output(MT5 출력)을 기록한다.
- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
- final_codex_direction(최종 Codex 방향): run F71E edge_margin q40 repair probe(F71E 엣지 마진 q40 수리 탐침 실행).

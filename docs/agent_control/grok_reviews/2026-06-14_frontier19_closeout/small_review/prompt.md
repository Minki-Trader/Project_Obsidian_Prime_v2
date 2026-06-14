You are Grok(그록), external second opinion(외부 2차 의견) for Project Obsidian Prime v2.
Review size(검토 크기): small closeout review(소규모 마감 검토).

Codex current evidence(현재 근거):
- Frontier19(전선19) opened as `boosted_backbone_no_repair_stack_onnx_scout` after adjusted Grok accepted(수정 그록 수용).
- Locks(잠금): max 4 boosted-tree backbone variants(부스팅 트리 백본 변형 4개), no threshold/veto/firewall/lifecycle/quota/stability-selector repair(임계값/배제/방화벽/생명주기/쿼터/안정성 선택기 수리 없음), archive reference only(보관소 참조 전용).
- Frontier19B trained 2 XGBoost + 2 CatBoost variants and exported ONNX. onnxruntime parity(ONNX 런타임 동등성): 4/4 passed, max diff about 1.2e-7 or lower.
- F19B decision policy(결정 정책): argmax_nonflat_control(최대확률 비중립 대조), no threshold search(임계값 탐색 없음), no lifecycle sweep(생명주기 스윕 없음).

Best proxy read(최상 프록시 판독): `f19b_cat_ordered_depth3_backbone__argmax_nonflat_backbone_only`
- validation(검증): PF 1.0257, density 31.96/day, DD 81.26%
- OOS(표본외): PF 1.0512, density 36.66/day, DD 41.18%
- strict/seed/preserved(엄격/씨앗/보존): 0/0/0
- runtime handoff candidates(런타임 인계 후보): 0

Codex proposed closeout(제안 마감): close Frontier19 as negative_memory(부정 기억): capped boosted backbone-only path creates valid ONNX artifacts but no forward clue; failure is proxy economics/density/DD, not ONNX conversion. Runtime probe blocker(런타임 탐침 차단 사유): no handoff candidate under locked no-repair-stack policy.

Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.

Question(질문): Should Codex close Frontier19 as negative_memory(부정 기억), preserve any clue, or attempt a bounded repair? If repair, it must not reintroduce threshold/veto/firewall/lifecycle/quota/stability selector repairs.

Return format(반환 형식):
Classification: accepted / rejected / needs_local_verification
Decision advice: close_negative_memory / preserve_clue / bounded_repair / invalid_setup / blocked
Key reason: 3 bullets max

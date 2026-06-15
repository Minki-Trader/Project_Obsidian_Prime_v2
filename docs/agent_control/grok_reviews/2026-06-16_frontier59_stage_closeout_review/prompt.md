# Frontier59 Stage-Closeout Review Prompt(전선59 단계 마감 검토 프롬프트)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Answer only from this prompt(프롬프트). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Stage and Hypothesis(단계와 가설)

- Stage(단계): `stage_frontier_59__long_quality_edge_after_short_economics_memory`.
- Candidate(후보): `f59b_directional_long_quality_extratrees_d7_l100_long_fav65_adv35_q90`.
- Hypothesis(가설): after F58 short-side economics collapse(F58 매도 측 경제성 붕괴), a long-only directional quality score(롱 전용 방향성 품질 점수) may be a more MT5-transferable seed surface(MT5 전이 가능한 씨앗 표면).
- Claim boundary(주장 경계): runtime probe observation(런타임 탐침 관찰) only; no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Proxy and ONNX(프록시와 온엑스)

- ONNX parity(온엑스 동등성): passed, max_abs_diff `2.1921185999751458e-07`.
- Proxy validation/OOS PF(프록시 검증/표본외 수익 팩터): `1.0578215704880256 / 1.0157994712511802`.
- Proxy validation/OOS DD(프록시 검증/표본외 손실폭): `11.437750113936607% / 7.416280476978832%`.
- Proxy validation/OOS trades/day(프록시 검증/표본외 거래/일): `5.551912568306011 / 5.3816793893129775`.
- Extra-cost stress PF(추가 비용 압박 수익 팩터): `1.0198833381625407 / 0.9588761570883082`.

## MT5 Runtime Probe(MT5 런타임 탐침)

Runtime policy(런타임 정책): raw direct p_long threshold(원천 직접 p_long 임계값), no lifecycle compression(생명주기 압축 없음), max_hold_bars `6`, ATR SL/TP enabled(ATR 손절/익절 사용).

Validation_is(검증 내부):
- PF `0.46`, DD `22.84%`, trades `1002`, trades/day `5.475409836065574`.
- feature_ready_diff `0`, signal_diff `0`, long_count_diff `0`, short_count_diff `0`.

OOS(표본외):
- PF `0.58`, DD `10.27%`, trades `688`, trades/day `5.251908396946565`.
- feature_ready_diff `0`, signal_diff `0`, long_count_diff `0`, short_count_diff `0`.

Proxy-runtime gap(프록시-런타임 차이):
- validation PF `1.0578 -> 0.46`; DD `11.44 -> 22.84`; density `5.55 -> 5.48`.
- OOS PF `1.0158 -> 0.58`; DD `7.42 -> 10.27`; density `5.38 -> 5.25`.

Codex proposed closeout(코덱스 제안 마감): `negative_memory_long_axis_did_not_escape_friction_class(부정 기억, 롱 축이 마찰/경제성 붕괴 계열을 벗어나지 못함)`.
Failure modes(실패 모드): `density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)`, `long_axis_source_no_transfer(롱 축 원천 전이 실패)`, plus orthogonality risk(직교성 위험) because overlap with recreated adverse-memory label was high.

## Question(질문)

Is the proposed closeout honest and appropriately bounded(정직하고 경계가 적절한가)? What preserved clue(보존 단서) and do-not-repeat negative memory(반복 금지 부정 기억) should Codex record?

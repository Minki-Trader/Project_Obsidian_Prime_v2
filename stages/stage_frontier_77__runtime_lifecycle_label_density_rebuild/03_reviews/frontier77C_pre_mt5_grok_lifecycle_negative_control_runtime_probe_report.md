# Frontier77C Pre-MT5 Grok Review Report(F77C 사전 MT5 Grok 검토 보고서)

Run id(실행 ID): `frontier77C_pre_mt5_grok_lifecycle_negative_control_runtime_probe_v1`

Status(상태): `pre_mt5_grok_review_completed_lifecycle_negative_control_probe_required_no_authority`

Judgment(판정): `pre_mt5_grok_accepts_lifecycle_negative_control_probe_with_local_verification_no_authority`

Updated(갱신): 2026-06-17T07:19:46Z

Claim boundary(주장 경계): `pre_mt5_review_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Codex Direction Before Grok(Grok 전 Codex 방향)

Action(행동): F77B weak nonzero proxy(약한 비영 프록시)를 F77D negative-control MT5 Runtime Probe(F77D 부정 대조 MT5 런타임 탐침)로 물질화한다.

Effect(효과): 프록시의 trade shape(거래 형태), selected-entry count(선택 진입 수), feature readiness(피처 준비), ONNX parity(온엑스 동등성)가 MT5에서 어디까지 유지되는지 관찰한다.

## Proxy KPI(프록시 핵심 성과 지표)

- best candidate(최선 후보): `f77b_08051` `short_h12_tp18_sl12_uq70/price_action_core/hist_gbm_d4_l2/all/trend_aligned/q0.93`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `272.40000000000003/1.7115987460815043/0.5279999999999927/2.2666666666666666/68`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `127.2/1.8030303030303034/0.6239999999999963/2.230769230769231/29`
- meaningful signal count(의미 신호 수): `0`

## Materialization Target(물질화 대상)

- selected target(선택 대상): `f77b_07979` `short_h12_tp18_sl12_uq70/price_action_core/extra_trees_d7_l80/cash_mid/trend_aligned/q0.8`
- selection reason(선택 이유): `best_proxy_hist_gbm_export_failed_so_first_ranked_exportable_extra_trees_target_selected`
- target validation net/PF/DD/tpd/trades(대상 검증 순수익/수익 팩터/손실폭/일거래/거래): `227.70000000000016/1.2574626865671639/1.4789999999999963/4.1875/134`
- target OOS net/PF/DD/tpd/trades(대상 표본외 순수익/수익 팩터/손실폭/일거래/거래): `61.20000000000002/1.272727272727273/0.49199999999998906/3.4/34`
- local export check(로컬 내보내기 확인): `stages/stage_frontier_77__runtime_lifecycle_label_density_rebuild/03_reviews/f77c_pre_mt5_local_verification.json`

## Grok Advice(Grok 조언)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f77c_pre_mt5_lifecycle_negative_control_runtime_probe`
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f77c_pre_mt5_lifecycle_negative_control_runtime_probe/prompts/f77c_pre_mt5_lifecycle_negative_control_runtime_probe_prompt.md` sha256 `cb11bbd6ab2e2a14f3cddaff2f68485ef524fd5a3df4f603213fd4675ed7d791`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f77c_pre_mt5_lifecycle_negative_control_runtime_probe/clean_output.md` sha256 `23f9a29f899684d56fcbe1e09c263d96e62f8f84f78cf34b02441cfbe3e7698a`
- metadata(메타데이터): `docs/agent_control/grok_reviews/2026-06-17_f77c_pre_mt5_lifecycle_negative_control_runtime_probe/metadata.json` sha256 `81cb3f039035ac6ea3c30eb6f08c3f01ca60e6f6f3b5af5bccb4061d4cba743f`
- wrapper success(래퍼 성공): `True`
- returncode(반환 코드): `0`
- advice classification(조언 분류): `accepted_with_conditions(조건부 수용)`
- final Codex direction(최종 Codex 방향): `proceed_after_local_verification(로컬 검증 뒤 진행)`
- forbidden claim hits(금지 주장 감지): `none(없음)`

## Required Local Verification(필수 로컬 검증)

- model export parity(모델 내보내기 동등성): ExtraTrees binary ONNX(이진 온엑스)를 short-only three-column schema(숏 전용 3열 스키마)로 패치하고 확률 차이를 확인한다.
- signal count parity(신호 수 동등성): selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) 뒤 validation/OOS signal count(검증/표본외 신호 수)가 proxy selected count(프록시 선택 수)와 일치하는지 확인한다.
- feature readiness parity(피처 준비 동등성): `price_action_core` feature order(피처 순서)와 MT5 feature CSV(피처 CSV)의 열 수/순서/hash(해시)를 확인한다.
- trade shape parity(거래 형태 동등성): short-only(숏 전용), max hold 12(최대 보유 12), fixed TP/SL 18/12(고정 익절/손절 18/12)를 EA inputs(EA 입력값)로 고정한다.

## Next Action(다음 행동)

`frontier77D_mt5_lifecycle_negative_control_runtime_probe_v1`.

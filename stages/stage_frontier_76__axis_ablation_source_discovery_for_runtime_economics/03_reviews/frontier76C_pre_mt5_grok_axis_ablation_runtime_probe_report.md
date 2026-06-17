# Frontier76C Pre-MT5 Grok Review Report(F76C MT5 전 Grok 검토 보고서)

Run id(실행 ID): `frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1`

Status(상태): `pre_mt5_grok_review_completed_runtime_probe_required_no_authority`

Judgment(판정): `pre_mt5_grok_review_accepts_bounded_runtime_probe_with_local_verification_no_authority`

Updated(갱신): 2026-06-17T05:55:42Z

Claim boundary(주장 경계): `pre_mt5_review_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Codex Direction Before Grok(Grok 전 Codex 방향)

Action(행동): F76B best candidate(최선 후보) `f76b_06637`를 F76D MT5 Runtime Probe(F76D MT5 런타임 탐침)로 물질화한다.

Effect(효과): proxy(프록시) 의미 신호를 실제 MT5 Strategy Tester(전략 테스터)에서 관찰해 proxy/runtime gap(프록시/런타임 간극)을 기록한다.

## Bounded Evidence(제한 근거)

- F76B summary(요약): `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/f76b_summary.json` sha256 `096d5f15f0b9f7753cb7c5afd490daec60fb79904b14a8dde281eecb81c1d92d`
- F76B report(보고서): `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/frontier76B_axis_ablation_proxy_scout_report.md` sha256 `c4f1f1dc4bd348e29d05faca0c956102972e35895ac77acfb9501e0c7122fa26`
- F76B axis summary(축 요약): `stages/stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics/03_reviews/f76b_axis_summary.csv` sha256 `1cf45ec9622efd8b0debbf31cad18c06f00873c3d07d9d2e0158d4ba2d398d0c`

## Target Proxy KPI(대상 프록시 핵심 성과 지표)

- candidate(후보): `f76b_06637`
- axes(축): `mega_cap_removed/extra_trees_d7_l60/long_fwd12_q60/cash_open/trend_aligned/0`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `1760.3101806640625/1.594854315978897/6.4446875%/1.0601092896174864/194`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `1471.7918701171875/1.6893374882536825/7.8916796875%/1.1755725190839694/154`

## Grok Advice(Grok 조언)

- packet(묶음): `docs/agent_control/grok_reviews/2026-06-17_f76c_pre_mt5_axis_ablation_runtime_probe`
- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f76c_pre_mt5_axis_ablation_runtime_probe/prompts/f76c_pre_mt5_axis_ablation_runtime_probe_prompt.md` sha256 `62c1af81b5a4d98c89dffa41b7ffc7271f4003a1846f739e543370f11ddeb35d`
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f76c_pre_mt5_axis_ablation_runtime_probe/clean_output.md` sha256 `93403efa7c86f9dd2669beb5ee87bee48f3994bde24ea803b6794149a4f94814`
- metadata(메타데이터): `docs/agent_control/grok_reviews/2026-06-17_f76c_pre_mt5_axis_ablation_runtime_probe/metadata.json` sha256 `25cd4e22ad32d5508b4de9c13ffd07395fe11558c621d303068b05741772eacc`
- wrapper success(래퍼 성공): `True`
- returncode(반환 코드): `0`
- advice classification(조언 분류): `accepted_with_conditions(조건부 수용)`
- final Codex direction(최종 Codex 방향): `proceed_after_local_verification(로컬 검증 후 진행)`
- forbidden claim hits(금지 주장 감지): `none(없음)`

## Local Verification Required(필수 로컬 검증)

- probability parity(확률 동등성): ONNX three-column long schema(ONNX 3열 롱 스키마)가 sklearn probability(사이킷런 확률)와 1e-5 이내인지 확인한다.
- signal count parity(신호 수 동등성): selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) 뒤 validation/OOS 선택 수가 proxy selected count(프록시 선택 수)와 일치하는지 확인한다.
- feature readiness parity(피처 준비 동등성): 48개 `mega_cap_removed` feature order(피처 순서)가 MT5 feature CSV(피처 CSV)와 일치하는지 확인한다.
- trade shape boundary(거래 형태 경계): max hold 12 bars(최대 보유 12봉), long-only(롱 전용), no initial ATR SL/TP(초기 ATR 손절/익절 없음)로 시작하고, 수익 주장보다 gap observation(간극 관찰)을 먼저 기록한다.

## Next Action(다음 행동)

`frontier76D_mt5_axis_ablation_runtime_probe_v1`.

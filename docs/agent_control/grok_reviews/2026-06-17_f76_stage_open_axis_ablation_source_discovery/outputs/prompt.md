# F76 Stage-Open Grok Prompt(F76 단계 개방 Grok 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).

Rules(규칙):
- Use only this prompt(프롬프트) as bounded evidence(제한 근거).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or do local verification(로컬 검증 금지).
- You cannot create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Current truth(현재 진실):
- F71-F75 retrospective(회고)는 completed(완료) and F76 open is allowed by retrospective gate(회고 게이트상 허용).
- Grok retrospective accepted(수용) F76 as axis-ablation/source-discovery matrix(축 제거/교체 원천 탐색 행렬).
- Dataset(데이터셋): 46650 rows, split counts(분할 수) {'train': 29222, 'validation': 9844, 'oos': 7584}, feature count(피처 수) 58.

Proposed F76 hypothesis(제안 F76 가설):
If F71-F75 repeatedly achieved parity(동등성) without meaningful runtime economics(의미 있는 런타임 경제성), then a structured ablation/replacement/recombination matrix(구조화된 제거/교체/재조합 행렬) across feature set, label/target, model family, trade shape, risk logic, and regime/session split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세·세션 분할) can identify or falsify the source axis(원천 축) before fine-tuning(미세 조정).

Axis matrix(축 행렬):

| axis | variants | why | meaningful_gate |
|---|---|---|---|
| feature_set(피처 묶음) | full58, price_action_core, trend_momentum, volatility_compression, session_macro_removed, mega_cap_removed | F71-F75 parity(동등성)는 맞췄지만 edge(우위)가 없었으므로 어떤 feature family(피처군)가 경제성을 망치거나 살리는지 반증한다. | validation+OOS net>0, PF>=1.30, DD<=10%, trades/day>=1.0, trade_count>=100 per split |
| label_target(라벨/목표) | fwd_return, first_touch_value, MFE/MAE quality, failed_breakout_reversal, clean_followthrough | direction label(방향 라벨)이 아니라 tradeable move quality(거래 가능한 이동 품질)를 맞히는지 본다. | same joint KPI gate plus label density >= 1.0 trades/day proxy estimate |
| model_family(모델 계열) | logistic/linear, ExtraTrees, HistGradientBoosting, EBM-if-available, small NN | 한 model bias(모델 편향)가 edge source(우위 원천)를 숨기는지 확인한다. | at least two families survive the scout clue gate or one family survives meaningful gate |
| trade_shape(거래 형태) | long_only, short_only, both_sides, fixed_hold, first_touch_exit, max_hold_sweep | one-sided runtime surfaces(단방향 런타임 표면)가 목표 밀도에 못 미친 반복을 반증한다. | side split must not rely on one isolated sparse cluster |
| risk_logic(위험 로직) | SL/TP grid, MAE/MFE filter, ATR width, DD guard, daily loss guard proxy | runtime DD blowout(런타임 손실폭 확대)을 proxy 단계에서 먼저 압박한다. | DD<=10% proxy on validation and OOS before MT5 materialization preference |
| regime_session_split(장세/세션 분할) | cash_open, cash_mid, cash_late, high_vol, low_vol, trend, chop | 좋은 숫자가 특정 세션/장세 한 점에만 갇히는지 확인한다. | no single micro slice may carry the whole result without recorded fragility |

Runtime rule(런타임 규칙):
- If proxy scout(프록시 탐색) finds a meaningful signal(의미 신호), Codex must run pre-MT5 Grok review(MT5 전 Grok 검토) and mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침).
- If no meaningful signal(의미 신호 없음) but nonzero signals exist(비영 신호 존재), Codex still runs a bounded negative-control MT5 Runtime Probe(제한 부정 대조 MT5 탐침) before closeout unless logic impossibility(논리상 불가능)가 documented.
- If zero signal(영 신호), Codex records logic impossibility(논리상 불가능), repair action(수리 행동), and closes without fake comparison(가짜 비교 없음).

Question(질문):
1. Is F76 sufficiently new versus F71-F75?
2. Are the meaningful signal gates too strict, too loose, or appropriate for early exploration(초기 탐색)?
3. What should Codex accept/reject/locally verify before running F76B?
4. What F76 do-not-repeat(반복 금지) rule should be recorded?

Answer in compact sections(압축 섹션):
- advice_classification(조언 분류)
- accepted(수용)
- rejected(거절)
- needs_local_verification(로컬 검증 필요)
- F76 opening boundary(F76 개방 경계)
- F76B proxy-scout cautions(F76B 프록시 탐색 주의)
- forbidden_claim_check(금지 주장 확인)

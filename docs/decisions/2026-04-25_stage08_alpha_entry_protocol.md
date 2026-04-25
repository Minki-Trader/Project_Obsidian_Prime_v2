# Decision: Stage 08 Alpha Entry Protocol

- date(날짜): `2026-04-25`
- stage(단계): `08_alpha_entry_protocol__tier_reporting_search_rules`
- packet_id(묶음 ID): `stage08_alpha_entry_protocol_v1`
- decision(결정): `reviewed_closed_handoff_to_stage09_complete_with_alpha_entry_protocol`

## 결정(Decision, 결정)

Stage 08(8단계)는 alpha entry protocol(알파 진입 규칙)과 Tier A/B reporting rule(티어 A/B 보고 규칙)을 닫는다.

효과(effect, 효과): Stage 09(9단계)은 registry/current truth/publish packet(등록부/현재 진실/게시 묶음)을 정리할 수 있다.

## 근거(Evidence, 근거)

- policy(정책): `docs/policies/alpha_entry_protocol.md`
- report template(보고 틀): `docs/templates/alpha_exploration_report_template.md`
- review(검토): `stages/08_alpha_entry_protocol__tier_reporting_search_rules/03_reviews/alpha_entry_protocol_review.md`
- Stage 07 baseline smoke(Stage 07 기준선 스모크): `20260425_stage07_baseline_training_smoke_v1`
- feature count(피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- probability output order(확률 출력 순서): `[p_short, p_flat, p_long]`

## 닫힌 항목(Closed Items, 닫힌 항목)

- allowed evidence(허용 근거)
- metric/report format(지표/보고 형식): PBO(`Probability of Backtest Overfitting`, 백테스트 과최적화 확률), DSR(`Deflated Sharpe Ratio`, 보정 샤프 비율), trial count(실험 횟수), selected legacy-derived metrics(선택된 레거시 유래 지표)를 포함한다.
- Tier A/B reporting(티어 A/B 보고)
- failure memory rule(실패 기억 규칙)
- no-promotion boundary(승격 아님 경계)

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 Stage 08(8단계)의 protocol/reporting rules(규칙/보고 규칙)를 닫는다.

새 model training(모델 학습), backtest(백테스트), official alpha result(공식 알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 닫지 않는다.

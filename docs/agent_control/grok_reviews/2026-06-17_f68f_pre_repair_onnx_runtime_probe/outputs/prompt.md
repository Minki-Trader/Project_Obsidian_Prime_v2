# F68F Pre-Repair ONNX Runtime Probe Review(F68F 수리 ONNX 런타임 탐침 전 검토)

You are Grok(Grok, 그록), an external second opinion(외부 2차 의견) only.
Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인), run tools(도구 실행), browse(브라우징), or claim local verification(로컬 검증).

## Codex Direction(Codex 방향)

Codex plans F68F as a repair probe(수리 탐침), not completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Proposed action(제안 행동):

1. Export(내보내기) the ONNX-capable repair candidate `f68b_0872ddc6192f`.
2. Candidate description(후보 설명): no_mega_top3 feature set(대형주/상위3 제외 피처 묶음), ExtraTrees shallow(얕은 엑스트라트리스), target h2 dd-penalized close(2봉 손실폭 벌점 종가), threshold quantile(임계값 분위수) `0.3`, cooldown(재진입 대기) `6`, both sides(양방향), close horizon exit(만기 종가 청산).
3. Run MT5 Strategy Tester(MT5 전략 테스터) validation/OOS(검증/표본외) after ONNX probability/signal parity(확률/신호 동등성) passes.
4. Keep `f68b_0f012336cfaf` as duplicate/regime check(중복/장세 확인) only unless feature hash(피처 해시) differs.

## Current Evidence(현재 근거)

F68D MT5 Runtime Probe(MT5 런타임 탐침):

- All four attempts completed(네 시도 완료).
- signal_count_diff(신호 수 차이): `0` for density validation/OOS and PF validation/OOS.
- feature_ready_diff(피처 준비 차이): `0` for all four attempts.
- density axis validation(밀도 축 검증): net `-294.46`, gross profit `2885.89`, gross loss `-3180.35`, PF `0.91`, DD `71.13%`, trades `1860`, trades/day `6.838235`.
- density axis OOS(밀도 축 표본외): net `103.48`, gross profit `2655.46`, gross loss `-2551.98`, PF `1.04`, DD `26.84%`, trades `1649`, trades/day `8.456410`.
- PF axis validation(수익 팩터 축 검증): net `2.12`, PF `43.4`, DD `0.35%`, trades/day `0.007353`.
- PF axis OOS(수익 팩터 축 표본외): net `1.52`, PF `0`, DD `0.31%`, trades/day `0.005128`.

F68E attribution(간극 원인 분해):

- Failure is not signal/feature parity(신호/피처 동등성) because all diffs are zero.
- Density axis has usable trade density(거래 밀도) but failed PF/DD(수익 팩터/손실폭).
- PF axis has low DD(낮은 손실폭) but unusably sparse density(거래 밀도 부족).
- Repair should change feature set/trade spacing/risk or exit shape(피처 묶음/거래 간격/위험 또는 청산 형태), not merely threshold-only retuning(임계값만 재조정).

Repair candidate(수리 후보) `f68b_0872ddc6192f` proxy KPI(프록시 핵심 성과 지표):

- validation(검증): net `3574.42`, PF `1.287249`, trades/day `3.184502`, proxy DD `6.8213%`.
- OOS(표본외): net `2528.70`, PF `1.234432`, trades/day `3.989691`, proxy DD `5.0615%`.
- It is not final-target density(최종 목표 거래 빈도) because trades/day is below 5, but it is a plausible DD/PF repair seed(손실폭/수익 팩터 수리 씨앗).
- It is ExtraTrees(엑스트라트리스), so ONNX export(ONNX 내보내기) is expected to be feasible, unlike the HGB low-DD clue(히스토그램 부스팅 저손실폭 단서).

## Review Questions(검토 질문)

1. Is F68F a reasonable next repair probe(수리 탐침) from this evidence?
2. What should Codex accept(수용), reject(거절), or locally verify(로컬 검증 필요) before exporting/running MT5?
3. What claim boundary(주장 경계) should remain after F68F if it runs?

Forbidden claims(금지 주장): completion(완성), selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

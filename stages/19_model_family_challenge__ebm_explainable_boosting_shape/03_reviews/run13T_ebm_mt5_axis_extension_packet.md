# Stage19 RUN13T EBM MT5 Axis Extension(19단계 실행13T EBM MT5 축 확장)

- judgment(판정): `inconclusive_ebm_mt5_axis_extension_completed`
- external verification(외부 검증): `completed`
- boundary(경계): `ebm_mt5_axis_extension_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- operating promotion(운영 승격): `none(없음)`

## 1 Feature Mask(피처 마스크)

- baseline OOS net(기준 표본외 순손익): `134.3`
- masked OOS net(마스크 표본외 순손익): `-90.4`
- delta(차이): `-224.7`

효과(effect, 효과): top5 feature(상위 5개 피처)를 MT5 score table(점수표)에서 직접 0으로 만들어 runtime dependency(런타임 의존성)를 확인했다.

## 2 Hold Micro Axis(보유 미세 축)

- best OOS hold(표본외 최고 보유): `4` / net(순손익): `134.3` / PF(수익 팩터): `1.17`
- best validation hold(검증 최고 보유): `2` / net(순손익): `69.53`
- validation positive holds(검증 양수 보유): `[2]`

효과(effect, 효과): hold2/3/5(2/3/5봉)를 추가해 hold4(4봉)가 고립된 우연인지 주변 축과 비교했다.

## 3 Tier B Subtype(티어 B 하위유형)

- subtype filter(하위유형 필터): `B_mixed_partial_context`
- filtered OOS net(필터 표본외 순손익): `143.94`
- delta vs base(기준 대비 차이): `9.64`

효과(effect, 효과): Tier B fallback(티어 B 대체)을 mixed subtype(혼합 하위유형)으로 제한했을 때 실제 라우팅 전체가 어떻게 바뀌는지 확인했다.

## 4 Side Hold4(4봉 방향)

- long-only OOS net(매수 전용 표본외 순손익): `68.64`
- short-only OOS net(매도 전용 표본외 순손익): `-27.16`
- long-minus-short(매수-매도): `95.8`

효과(effect, 효과): hold4(4봉)에서도 long bias(매수 편향)가 유지되는지 확인했다.

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).

# Stage19 RUN13M EBM Deep Axis Follow-up(19단계 실행13M EBM 심층 축 후속)

- judgment(판정): `inconclusive_ebm_deep_axis_followup_completed`
- external verification(외부 검증): `completed`
- boundary(경계): `ebm_deep_axis_followup_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- operating promotion(운영 승격): `none(없음)`

## Feature Mask(피처 마스크)

- strongest OOS mask(표본외 최강 마스크): `mask_top5_repeated` / tier(티어): `Tier A`
- lost signal rate(상실 신호 비율): `0.7849462365591398`
- claim(주장): `score_table_feature_mask_attribution_not_retrained_ablation(점수표 피처 마스크 기여도이며 재학습 제거가 아님)`

효과(effect, 효과): EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)이 몇 개 피처에 얼마나 기대는지 봤고, 재학습 모델 성능 주장으로 키우지 않았다.

## Hold Axis(보유 축)

- requested holds(요청 보유): `[4, 6, 8, 10]`
- best OOS hold(표본외 최고 보유): `4` / net(순손익): `134.3` / PF(수익 팩터): `1.17`
- best validation hold(검증 최고 보유): `4` / net(순손익): `-107.72`
- validation positive holds(검증 양수 보유): `[]`

효과(effect, 효과): hold4/8/10(4/8/10봉)은 새 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)로 확인했고 hold6(6봉)은 run13F(실행13F)를 재사용했다.

## Tier B Subtype(티어 B 하위유형)

- OOS top signal subtype(표본외 최다 신호 하위유형): `B_mixed_partial_context` / signals(신호): `20`
- OOS top rate subtype min10(표본외 최소 10행 기준 최고 신호율 하위유형): `B_mixed_partial_context` / rate(비율): `0.087719298`

효과(effect, 효과): Tier B fallback(티어 B 대체)이 어떤 partial context subtype(부분 문맥 하위유형)에서 신호를 내는지 분해했다.

## Side Axis(방향 축)

- long-only OOS net(매수 전용 표본외 순손익): `18.7` / PF(수익 팩터): `1.03` / trades(거래): `165`
- short-only OOS net(매도 전용 표본외 순손익): `7.14` / PF(수익 팩터): `1.02` / trades(거래): `88`
- OOS long-minus-short net(표본외 매수-매도 순손익 차이): `11.56`

효과(effect, 효과): q90 hold6(q90 6봉)에서 long-only/short-only(매수 전용/매도 전용)를 실제 MT5 threshold routing(임계값 라우팅)으로 나눠 봤다.

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).

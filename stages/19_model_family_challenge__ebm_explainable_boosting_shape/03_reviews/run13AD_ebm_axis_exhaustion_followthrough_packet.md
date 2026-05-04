# Stage19 RUN13AD EBM Axis Exhaustion Followthrough(19단계 실행13AD EBM 축 소진 후속)

- judgment(판정): `inconclusive_ebm_axis_exhaustion_followthrough_completed`
- external verification(외부 검증): `completed`
- boundary(경계): `ebm_axis_exhaustion_followthrough_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- operating promotion(운영 승격): `none(없음)`

## 1 Feature Single Mask(피처 단일 마스크)

- largest dependency(최대 의존): `ema50_ema200_diff` / OOS delta(표본외 차이): `-403.41`

효과(effect, 효과): top5(상위5)를 한꺼번에 끄는 대신 한 피처씩 꺼서 EBM(설명가능 부스팅 머신) 점수표(score table, 점수표)의 의존이 집중인지 분산인지 확인했다.

## 2 Hold Segment(보유 구간)

- hold4-hold2 OOS(4봉-2봉 표본외): `108.61`
- hold2-hold4 validation(2봉-4봉 검증): `177.25`
- hold4 top OOS month(4봉 표본외 최고 월): `2025-11` / `73.54`

효과(effect, 효과): hold2(2봉)와 hold4(4봉)의 충돌이 시간, 방향, 변동성, 세션 구간에서 어디서 생기는지 분해했다.

## 3 Tier B Subtype(티어 B 하위유형)

- best subtype(최고 하위유형): `B_mixed_partial_context` / OOS net(표본외 순손익): `143.94`

효과(effect, 효과): Tier B fallback(티어 B 대체)을 하위유형별로 제한해 라우팅 효율이 어디서 나오는지 확인했다.

## 4 Side Compression(방향 압축)

- best long compression(최고 매수 압축): `run13S` q=`0.9` / OOS net(표본외 순손익): `68.64` / PF(수익 팩터): `1.13`

효과(effect, 효과): short(매도)을 무조건 폐기하지 않고 threshold(임계값)를 올려 long bias(매수 편향)가 살아남는지 봤다.

## Follow-up Decision(후속 판단)

- further exploration available(추가 탐색 여지): `False`
- recommended follow-up topics(권장 후속 주제): `[]`
- completed follow-up topics(완료 후속 주제): `['run13AE', 'run13AH']`
- action taken(수행 행동): `followup_completed_no_new_runtime_followup_recommended`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).

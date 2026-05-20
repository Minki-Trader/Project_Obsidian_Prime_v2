# Stage267 Run267T Pool-Wide Orthogonal Stability MT5 Review(267단계 267T 후보군 전체 직교 안정성 MT5 검토)

- action(행동): run267T(267T 실행)의 34개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 signature(서명) 단위로 묶어 검토했다.
- effect(효과): 후보가 실제로 서로 다른 안정성 표면을 만들었는지, 아니면 proxy variant(대체 변형)가 같은 결과로 접혔는지 확인한다.
- status(상태): `run267T_pool_wide_orthogonal_stability_mt5_review_completed`
- judgment(판정): `negative_distinguishability_result_reusable_failure_memory`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

실행은 성공했다. 하지만 좋은 소식만은 아니다. 34개 결과가 단 2개의 KPI signature(KPI 서명)로 접혔다.
효과는 명확하다. 이번 proxy adapter variant(대체 어댑터 변형)는 후보별 차이를 충분히 드러내지 못했다. 그래서 숫자가 좋아 보이는 행이 있어도 후보 선정이나 ONNX(ONNX) 검토로 갈 수 없다.
다음은 true internal feature ablation(진짜 내부 피처 제거) 또는 더 직접적인 feature path(피처 경로) 재설계가 필요하다.

## Signature Matrix(서명 행렬)

| signature(서명) | rows(행) | candidates(후보) | axes(축) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `sig01` | 20 | 5 | 1 | 177.49 | 1.2 | 486 | 12.68 | `signature_collapse_cluster_candidate_distinction_weak` |
| `sig02` | 14 | 5 | 1 | 236.31 | 1.3 | 454 | 12.88 | `signature_collapse_cluster_candidate_distinction_weak` |

## Candidate Summary(후보 요약)

| candidate(후보) | attempts(시도) | signatures(서명) | net min(순수익 최소) | net max(순수익 최대) | worst DD%(최악 손실폭) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `s258_stc` | 6 | 2 | 177.49 | 236.31 | 12.88 | `weak_candidate_separation` |
| `s262_lih` | 6 | 2 | 177.49 | 236.31 | 12.88 | `weak_candidate_separation` |
| `s264_aia` | 8 | 2 | 177.49 | 236.31 | 12.88 | `weak_candidate_separation` |
| `s264_aih` | 8 | 2 | 177.49 | 236.31 | 12.88 | `weak_candidate_separation` |
| `s264_lc` | 6 | 2 | 177.49 | 236.31 | 12.88 | `weak_candidate_separation` |

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267T_pool_wide_orthogonal_stability_mt5_review`.
- positive_claim(긍정 주장): 없음.
- negative_evidence(부정 근거): KPI signature collapse(KPI 서명 접힘)가 있어 후보 구분성이 약하다.
- reusable_clue(재사용 단서): axis01(1축)은 순수익 `236.31`, PF(수익 팩터) `1.3`, trades(거래 수) `454` 서명으로 접혔고, axis02(2축)는 순수익 `177.49`, PF(수익 팩터) `1.2`, trades(거래 수) `486` 서명으로 접혔다.
- missing_evidence(빠진 근거): true internal feature ablation(진짜 내부 피처 제거), balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 재검토.
- next_action(다음 행동): `run267U_design_true_internal_feature_ablation_after_run267T_signature_collapse`.

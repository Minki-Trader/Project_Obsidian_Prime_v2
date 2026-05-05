# RUN18A Survival Time-To-Event Scout Packet(실행18A 생존 시간-사건 탐색 묶음)

## Judgment(판정)

- run(실행): `run18A_survival_time_to_event_hold_shape_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_survival_time_to_event_hold_shape_scout_completed`
- selected variant(선택 변형): `v04_weibull_aft_core24_abs_move_3x`
- boundary(경계): `survival_time_to_event_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run18A_next_milestone_run18B_survival_time_to_event_runtime_probe_v1(실행18A에서는 미시도, 다음 마일스톤은 run18B_survival_time_to_event_runtime_probe_v1)`

효과(effect, 효과): Survival model(생존 모델)을 entry model(진입 모델)이 아니라 hold/exit clock(보유/청산 시계)로 탐색했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `4`
- completed variants(완료 변형): `3`
- selected model type(선택 모델 유형): `weibull_aft`
- event definition(사건 정의): `abs_move_3x`
- validation c-index(검증 일치 지수): `0.73631244882561`
- OOS c-index(표본외 일치 지수): `0.6856377470736932`
- validation event rate(검증 사건 비율): `0.4291954490044697`
- OOS event rate(표본외 사건 비율): `0.38072003164974283`
- Tier A rows(Tier A 행): `46650`
- Tier B fallback rows(Tier B 대체 행): `12398`

## Preserved Clues(보존 단서)

- time-to-event(사건까지 시간) 형태는 fixed hold(고정 보유) 튜닝이 아니라 event/censoring(사건/검열) 구조로 읽을 수 있다.
- Cox hazard(콕스 위험률)와 Weibull AFT(와이블 가속고장시간) 모두 같은 event surface(사건 표면)에서 비교했으므로 model family behavior(모델군 행동) 차이를 남겼다.
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)를 모두 기록했다.

## Invalid Or Negative Memory(무효 또는 부정 기억)

- adverse-direction event(불리 방향 사건)는 label direction(라벨 방향)을 쓰므로 hindsight structural probe(사후 구조 탐침)로만 보존한다.
- Python-side survival score(파이썬 생존 점수)는 MT5(`MetaTrader 5`, 메타트레이더5) handoff(인계)를 아직 통과하지 않았으므로 runtime claim(런타임 주장)이 아니다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run18B_survival_time_to_event_runtime_probe_v1` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침).

# F73 Stage Open Grok Prompt(F73 단계 개방 그록 프롬프트)

You are Grok(Grok, 그록), an external second opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(검색 금지), or do local verification(로컬 검증 금지).

Required output sections(필수 출력 섹션): accepted(수용), rejected(거절), needs_local_verification(로컬 검증 필요), drift_risks(드리프트 위험), final_advice(최종 조언).

## Current Truth(현재 진실)

- Frontier72(F72 전선 단계) closed as preserved clue + negative memory(보존 단서 + 부정 기억), no authority(권위 없음).
- F72F OOS runtime(표본외 런타임): net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) = 66.47/1.05/18.60%/2.4769/483.
- F72 preserved clue(보존 단서): lifecycle count bridge(생명주기 개수 브리지) reduced expected/runtime trade-count gap(예상/런타임 거래 수 간극), and signal/feature parity(신호/피처 동등성) stayed diff 0.
- F72 negative memory(부정 기억): trade-shape-first label/feature/lifecycle surface(거래 형태 우선 라벨/피처/생명주기 표면) did not create runtime economics(런타임 경제성).
- Five-stage retrospective(5단계 중간 검토): not due after F72 closeout(F72 마감 뒤 아직 아님), 2/5 closeouts since last retrospective(마지막 중간 검토 이후 2/5).

## Proposed F73 Direction(F73 제안 방향)

Hypothesis(가설): session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 parity/lifecycle fixes(동등성/생명주기 수리)와 별개인 runtime economics source(런타임 경제성 원천)를 분리할 수 있다.

Plain version(쉬운 설명): F72는 주문 개수와 준비 상태를 꽤 맞췄지만 돈 버는 구조가 약했다. F73은 같은 청산 모양을 더 만지기보다, 어느 시간대/장세에서 어떤 피처 묶음과 어떤 모델이 실제로 돈 되는 후보를 만드는지 넓게 바꿔본다.

## Intentional Changes(의도 변경)

- feature set(피처 묶음): all58(전체 58개), core price/path(핵심 가격/경로), session/regime-only plus core(세션/장세+핵심), no top3 proxy(상위3 대리 제거), low-correlation/top-importance recombination(저상관/중요도 재조합).
- label/target(라벨/목표): fwd12(12봉 전방) and fwd18(18봉 전방), direct direction(직접 방향), inverse/rank read(역방향/순위 판독), quality-of-move proxy(움직임 품질 대리).
- model family(모델 계열): logistic/linear(로지스틱/선형), ExtraTrees(엑스트라트리스), HistGradientBoosting(히스토그램 그래디언트 부스팅), small NN(작은 신경망) if dependency available(의존성 가능 시).
- trade shape(거래 형태): not lead axis(주도 축 아님); use simple fixed lifecycle proxy(단순 고정 생명주기 프록시) so model/feature/regime differences are visible.
- risk logic(위험 로직): keep bounded SL/TP/hold bands(제한된 손절/익절/보유 범위) as guardrail(보호 장치), not as the main repair.
- regime/session split(장세/세션 분할): cash open/mid/late(정규장 초반/중반/후반), trend/chop/volatility buckets(추세/횡보/변동성 구간).

## Controls(통제 변수)

- Symbol/timeframe(심볼/시간프레임): US100 M5(US100 5분봉).
- Split(분할): time-ordered train/validation/OOS(시간순 학습/검증/표본외).
- Runtime rule(런타임 규칙): if proxy(프록시)가 meaningful signal(의미 있는 신호)을 만들면 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.
- Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Evidence Snapshot(근거 스냅샷)

- fwd12 input(12봉 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`, rows(행) `46650`, splits(분할) `{'train': 29222, 'validation': 9844, 'oos': 7584}`.
- fwd18 input(18봉 입력): `data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`, rows(행) `42567`, splits(분할) `{'train': 26613, 'validation': 9014, 'oos': 6940}`.
- feature order same(피처 순서 동일): `True`, feature counts(피처 수) `58/58`.

## Success/Failure Boundary(성공/실패 경계)

- scout clue(탐색 단서): validation and OOS(검증과 표본외) both net>0(순수익 양수), PF>=1.10(수익 팩터 1.10 이상), DD<=15%(손실폭 15% 이하), trades/day>=1.5(일거래 1.5 이상).
- meaningful proxy signal(의미 있는 프록시 신호): PF>=1.25(수익 팩터 1.25 이상), DD<=10%(손실폭 10% 이하), trades/day>=3.0(일거래 3.0 이상), validation/OOS non-collapse(검증/표본외 붕괴 없음).
- final-like reference only(최종 유사 참조 전용): PF>=2.0(수익 팩터 2.0 이상), DD<10%(손실폭 10% 미만), trades/day 5-10(일거래 5-10), smooth equity proxy(매끄러운 자산곡선 대리).
- failure(실패): zero signal(영 신호), only post-hoc quota/throttle(사후 할당/제한만), or same F72 trade-shape-first repair(동일 F72 거래 형태 우선 수리).

## Question For Grok(Grok에게 묻는 질문)

Is this F73 direction genuinely different enough from F70/F71/F72(이 방향이 F70/F71/F72와 충분히 다른가), broad enough to satisfy the user's exploration concern(사용자의 넓은 탐색 걱정을 만족할 만큼 넓은가), and bounded enough to run as a single frontier lifecycle(하나의 전선 생명주기로 실행할 만큼 경계가 있는가)?

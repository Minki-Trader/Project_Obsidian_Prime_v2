# Frontier03 Experiment Design(전선03 실험 설계)

## Hypothesis(가설)

Regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링)이 Frontier02 density clue(전선02 밀도 단서)를 보존하면서 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 개선할 수 있는지 시험합니다.

## Decision Use(결정 사용처)

첫 proxy scout(프록시 탐색)가 label/regime axis(라벨/레짐 축)를 계속 밀 가치가 있는지 결정합니다.

## First Proxy Scout Contract(첫 프록시 탐색 계약)

`frontier03B_regime_asymmetric_label_proxy_scout_v1`는 regime-neutral-band asymmetric long/short label replay(레짐 중립 구간 비대칭 롱/숏 라벨 재생)입니다.

- fixed dataset(고정 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- fixed horizon(고정 보유기간): fwd12(12봉 선행)
- fixed features(고정 피처): feature_set_v2(피처 세트 v2)
- regime definition(레짐 정의): one closed-bar trend/chop rule(종료봉 기반 추세/횡보 규칙 하나)
- moving part(움직이는 부분): neutral band by regime(레짐별 중립 구간) and asymmetric long/short payoff target(롱/숏 비대칭 손익 목표)
- variant cap(변형 상한): 12
- excluded(제외): ONNX(온엑스), WFO(워크포워드), MT5(메타트레이더5), broad source redesign(넓은 원천 재설계)

Effect(효과): label/regime novelty(라벨/레짐 신규성)만 빠르게 검증하고 model/runtime authority(모델/런타임 권위) 주장을 막습니다.

## Comparison Baseline(비교 기준)

Comparison baseline(비교 기준)은 no-trade baseline(무거래 기준)과 Frontier02 preserved clue(전선02 보존 단서)입니다. 둘 다 operating baseline(운영 기준선)이 아닙니다.

## Control Variables(고정 변수)

- symbol/timeframe(심볼/시간프레임): US100 M5
- dataset identity(데이터셋 정체성): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- horizon(보유기간): fwd12(12봉 선행)
- feature set(피처 세트): feature_set_v2(피처 세트 v2)
- split(분할): train/validation/OOS(학습/검증/표본외)
- cost proxy(비용 프록시): Frontier02와 같은 scout cost(탐색 비용)를 우선 유지

## Changed Variables(변경 변수)

- one regime definition(레짐 정의 하나)
- long/short asymmetric label target(롱/숏 비대칭 라벨 목표)
- neutral band by regime(레짐별 중립 구간)
- selection score(선택 점수): four-axis distance(네 축 거리) + curve smoothness(곡선 매끄러움)

## Sample Scope(표본 범위)

Tier A(티어 A) full-context sample(전체 문맥 표본)을 먼저 사용합니다. Tier B(티어 B)는 현재 missing_required(필수 누락)이며, 합산 기록(combined record, 합산 기록)은 out_of_scope_by_claim(주장 범위 밖)입니다.

## Success Criteria(성공 기준)

초기 탐색에서는 final completion hard gate(최종 완성 강제 게이트)를 적용하지 않습니다. 대신 PF/density/DD/smoothness(수익 팩터/밀도/손실폭/매끄러움)의 목표 거리(target distance, 목표 거리)가 Frontier02보다 정직하게 줄어드는지 봅니다.

## Failure Criteria(실패 기준)

- go-rule rows(진행 규칙 행)가 0이고 새 label/regime axis(라벨/레짐 축)의 설명력이 없을 때
- density(밀도)만 좋아지고 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 악화될 때
- threshold-only repair(임계값만 수리)로 되돌아갈 때

## Invalid Conditions(무효 조건)

- future return leakage(미래 수익 누수)
- split contamination(분할 오염)
- label computed from validation/OOS selection(검증/표본외 선택으로 라벨 계산)
- feature order mismatch(피처 순서 불일치)

## Stop Conditions(중지 조건)

같은 label/regime repair(라벨/레짐 수리)를 novelty delta(신규성 차이) 없이 반복하면 capped repair(상한 있는 수리)로 닫고 negative memory(부정 기억)를 남깁니다.

## Evidence Plan(근거 계획)

- Frontier03A stage-open packet(단계 개방 묶음)
- Frontier03B proxy scout manifest(프록시 탐색 목록)
- Tier A separate / Tier B separate / Tier A+B combined rows(티어 A 분리 / 티어 B 분리 / 합산 행)
- Grok pre-expensive review(비싼 검증 전 그록 검토)

# run03G ExtraTrees Variant Stability Probe(엑스트라트리스 변형 안정성 탐침) Plan(계획)

## Scope(범위)

- stage(단계): `12_model_family_challenge__extratrees_training_effect`
- run(실행): `run03G_et_variant_stability_probe_v1`
- source run(원천 실행): `run03D_et_standalone_batch20_v1`
- reference MT5 run(참고 MT5 실행): `run03F_et_v11_tier_balance_mt5_v1`
- claim boundary(주장 경계): Python structural scout(파이썬 구조 탐침) only(전용)

## Hypothesis(가설)

RUN03D(실행 03D)의 v11 중심 판독은 너무 빨리 좁혀졌을 수 있다. 효과(effect, 효과)는 v09/v13/v16/v18 같은 alternative variant(대안 변형)를 month/quarter stability(월/분기 안정성)로 다시 비교해서 다음 MT5(`MetaTrader 5`, 메타트레이더5) 후보를 고르는 것이다.

## Controls(통제)

- dataset(데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- feature set(피처 묶음): `feature_set_v2_mt5_price_proxy_top3_weights_58_features`
- label(라벨): `label_v1_fwd12_m5_logret_train_q33_3class`
- split(분할): validation(검증) 2025-01-01~2025-09-30, OOS(표본외) 2025-10-01~2026-04-13
- inheritance(계승): Stage 10/11(10/11단계) model/threshold/baseline(모델/임계값/기준선) 미사용

## Evidence Plan(근거 계획)

- variant stability table(변형 안정성 표)
- monthly stability table(월별 안정성 표)
- shortlist(후보 목록)
- stage/project ledger rows(단계/프로젝트 장부 행)
- result summary(결과 요약), manifest(실행 목록), KPI record(KPI 기록)

## Invalid Conditions(무효 조건)

- RUN03D(실행 03D)가 standalone(단독) 경계를 잃은 경우
- scored prediction(점수 예측) 파일이 없거나 variant_id(변형 ID)가 빠진 경우
- split(분할) 또는 timestamp(타임스탬프)가 해석되지 않는 경우

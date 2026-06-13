# Regime Asymmetric Label Plan(레짐 비대칭 라벨 계획)

## First Proxy Scout(첫 프록시 탐색)

Frontier03B(전선03B)는 label-proxy replay(라벨 프록시 재생)로 시작합니다. 모델 학습(model training, 모델 학습), ONNX export(온엑스 내보내기), WFO(워크포워드), MT5(메타트레이더5)는 열지 않습니다.

## Fixed Contract(고정 계약)

- dataset(데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- split(분할): existing train/validation/OOS(기존 학습/검증/표본외)
- horizon(보유기간): fwd12(12봉 선행) only(전용)
- feature set(피처 세트): feature_set_v2(피처 세트 v2)
- regime definition(레짐 정의): one closed-bar trend/chop rule(종료봉 기반 추세/횡보 규칙 하나)
- variant cap(변형 상한): 12 rows(12행)

## Moving Parts(변경 요소)

- asymmetric side target(비대칭 방향 목표): long target(롱 목표) and short target(숏 목표)을 분리합니다.
- regime neutral band(레짐 중립 구간): trend/chop(추세/횡보)에 따라 neutral band(중립 구간)만 움직입니다.
- replay score(재생 점수): validation/OOS net(검증/표본외 순수익), PF(수익 팩터), density(밀도), DD(손실폭), smoothness(매끄러움)의 target distance(목표 거리)를 봅니다.

## Micro Search Gate(미세 탐색 게이트)

Micro search(미세 탐색)는 at least one(최소 하나) regime/asymmetric label family(레짐/비대칭 라벨군)가 validation and OOS(검증 및 표본외)에서 positive net(양수 순수익)과 target-distance improvement(목표 거리 개선)를 동시에 보일 때만 엽니다.

Effect(효과): density(밀도) 하나만 좋아지는 변형은 앞으로 보내지 않고, 네 축 target distance(목표 거리)가 같이 줄어드는지 먼저 확인합니다.

# Stage 11 Alpha Robustness: WFO Label Horizon Sensitivity

## 질문(Question, 질문)

Stage 10(10단계)의 `run01Y(실행 01Y)` 기준 후보와 그 주변 탐색 후보가 WFO(`walk-forward optimization`, 워크포워드 최적화), label/horizon sensitivity(라벨/예측수평선 민감도), model training method sensitivity(모델 학습방법 민감도)에서도 구조적으로 버티는가?

## 범위(Scope, 범위)

- `run01Y(실행 01Y)` baseline candidate(기준 후보)
- model training method challenger(모델 학습방법 도전자)
- WFO(워크포워드 최적화) 또는 walk-forward-style split(워크포워드식 분할) 설계
- label/horizon variants(라벨/예측수평선 변형)
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산) 기록
- MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)는 필요한 최소 범위에서만 실행

## 범위 밖(Not In Scope, 범위 밖)

- live readiness(실거래 준비)
- operating promotion(운영 승격)
- runtime authority expansion(런타임 권위 확장)
- production retraining(운영용 재학습)
- Stage 10(10단계) 실행 번호(run number, 실행 번호) 재사용

## 종료 조건(Exit Condition, 종료 조건)

Stage 11(11단계)은 `run01Y(실행 01Y)` 계열과 model training method challenger(모델 학습방법 도전자)가 유지, 약화, 무효, 또는 재탐색 필요 중 하나로 정리되면 닫을 수 있다.

효과(effect, 효과): Stage 10(10단계)의 단일 분할 결과를 alpha quality(알파 품질)처럼 과장하지 않고, 다음 판단에 필요한 견고성 근거(robustness evidence, 견고성 근거)와 학습방법 비교 근거(training-method evidence, 학습방법 근거)를 만든다.

## 현재 판독(Current Read, 현재 판독)

`RUN02A(실행 02A)` LightGBM(`LightGBM`, 라이트GBM) training-method scout(학습방법 탐색), `RUN02B(실행 02B)` LGBM-specific rank-target threshold scout(LGBM 전용 순위 기반 임계값 탐색), `RUN02C~RUN02F(실행 02C~02F)` divergent scouts(발산형 탐색), `RUN02G~RUN02P(실행 02G~02P)` idea burst scouts(아이디어 무더기 탐색)는 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 완료했다.

효과(effect, 효과): RUN02G(실행 02G) long pullback(롱 되돌림)은 OOS(표본외) `238.68 / 3.44`로 강한 회수 가치를 남겼지만 validation(검증)이 `-138.39 / 0.54`라 불안정하다. RUN02N(실행 02N) squeeze breakout(압축 돌파)은 OOS(표본외) `107.14 / 55.11`이지만 trade count(거래 수)가 3개뿐이고 validation(검증)이 약하다. RUN02P(실행 02P) bear vortex short(하락 보텍스 숏)는 validation/OOS(검증/표본외)가 모두 양수지만 순수익(net profit, 순수익)이 `1.78`, `24.33`으로 작다. 현재는 LGBM(라이트GBM)을 promotion_candidate(승격 후보)로 올리지 않고, RUN02G/RUN02N/RUN02P(실행 02G/02N/02P)를 회수 가치 메모로 보존한다.

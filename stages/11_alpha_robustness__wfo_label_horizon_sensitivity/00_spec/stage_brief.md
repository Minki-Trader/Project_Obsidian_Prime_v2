# Stage 11 Alpha Robustness: WFO Label Horizon Sensitivity

## 질문(Question, 질문)

Stage 10(10단계)의 `run01Y(실행 01Y)` 기준 후보가 WFO(`walk-forward optimization`, 워크포워드 최적화)와 label/horizon sensitivity(라벨/예측수평선 민감도)에서도 구조적으로 버티는가?

## 범위(Scope, 범위)

- `run01Y(실행 01Y)` baseline candidate(기준 후보)
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

Stage 11(11단계)은 `run01Y(실행 01Y)` 계열이 WFO/label-horizon(워크포워드/라벨-예측수평선)에서 유지, 약화, 무효, 또는 재탐색 필요 중 하나로 정리되면 닫을 수 있다.

효과(effect, 효과): Stage 10(10단계)의 단일 분할 결과를 alpha quality(알파 품질)처럼 과장하지 않고, 다음 판단에 필요한 견고성 근거(robustness evidence, 견고성 근거)를 만든다.

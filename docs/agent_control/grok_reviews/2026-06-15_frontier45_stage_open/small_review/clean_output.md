**1. verdict:** `accepted`

**2. main_guardrail:**
Train-split-only construction lock(학습 분할 전용 구성 잠금): event labels(이벤트 라벨), class weights(클래스 가중치), probability thresholds(확률 임계값), model variants(모델 변형), SL/TP caps(손익절 상한), and candidate rank(후보 순위) must be built only from the train split(학습 분할). Validation/OOS(검증/표본외) may be used only for read-only evaluation(읽기 전용 평가), never for fitting, selection, or repair decisions(적합/선택/수리 결정에 사용 금지).

**3. do_not_repeat:**
- Validation/OOS labels or outcomes(검증/표본외 라벨/결과) for label/threshold/model/SL-TP-cap/rank construction(라벨·임계값·모델·손익절 상한·순위 구성)
- F44 continuous path-utility regression(연속 경로 효용 회귀) as the primary lever(주 레버)
- F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천), F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움) as primary levers(주 레버)
- ONNX completion(온엑스 완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비) claims(주장)

**4. claim_boundary_ok:** `yes`

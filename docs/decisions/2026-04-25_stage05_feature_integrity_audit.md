# Decision: Stage 05 Feature Integrity Audit

- date(날짜): `2026-04-25`
- stage(단계): `05_feature_integrity__formula_time_alignment_leakage_audit`
- status(상태): `accepted`

## 결정(Decision, 결정)

Stage 05(5단계)는 `20260425_stage05_feature_integrity_audit_v1` 실행(run, 실행)을 선택 근거(selected evidence, 선택 근거)로 닫는다.

이 실행(run, 실행)은 Stage 04(4단계)의 MT5 price-proxy 58 feature model input(MT5 가격 대리 58개 피처 모델 입력)에 대해 feature formula(피처 공식), time/session(시간/세션), external alignment(외부 정렬), label leakage(라벨 누수)를 통합 감사했다.

## 이유(Rationale, 이유)

감사 결과(audit result, 감사 결과)는 모두 통과(pass, 통과)했다.

- feature frame rows(피처 프레임 행): `54439`
- model input rows(모델 입력 행): `46650`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- external alignment missing total(외부 정렬 누락 합계): `0`
- formula max abs diff after float32 export(float32 출력 후 공식 최대 절대 차이): `0.0`

효과(effect, 효과): Stage 06(6단계)이 같은 58 feature(58개 피처) 표면을 Python/MT5 parity(파이썬/MT5 동등성) 검증 대상으로 사용할 수 있다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 feature integrity(피처 무결성) 폐쇄다.

model training(모델 학습), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.

# Decision: Stage 06 Runtime Parity Blocked Handoff

- date(날짜): `2026-04-25`
- stage(단계): `06_runtime_parity__python_mt5_runtime_authority`
- status(상태): `accepted_blocked_handoff`

## 결정(Decision, 결정)

Stage 06(6단계)는 `20260425_stage06_runtime_parity_blocked_v1` 실행(run, 실행)을 선택 근거(selected evidence, 선택 근거)로 blocked handoff(차단 인계) 처리한다.

runtime authority(런타임 권위)는 닫지 않는다.

## 이유(Rationale, 이유)

실행(run, 실행)은 Stage 05(5단계)가 감사한 58 feature model input(58개 피처 모델 입력)에서 minimum fixture set(최소 표본 묶음), Python snapshot(파이썬 스냅샷), MT5 handoff package(MT5 인계 묶음)를 만들었다.

MetaEditor compile(메타에디터 컴파일)은 script(스크립트)와 EA(Expert Advisor, 전문가 자문) 모두 `0 errors, 0 warnings(오류 0, 경고 0)`로 통과했다.

하지만 MT5 snapshot(MT5 스냅샷)이 아직 없고, 저장소의 기존 MT5 audit tool(MT5 감사 도구)은 `equal weight(동일가중)` 기준이라 Stage 04(4단계)의 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 재현하지 못한다.

## 효과(Effect, 효과)

Stage 07(7단계) `07_model_training_baseline__contract_preprocessing_smoke`를 열 수 있다.

효과(effect, 효과)는 model training smoke(모델 학습 스모크)를 시작하되, MT5 runtime parity(MT5 런타임 동등성)나 live-like readiness(실거래 유사 준비)를 주장하지 않게 하는 것이다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 runtime probe blocked(런타임 탐침 차단)이다.

다음을 주장하지 않는다.

- parity closure(동등성 폐쇄)
- artifact identity closure(산출물 정체성 폐쇄)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- model quality(모델 품질)
- alpha quality(알파 품질)

## 재시도 조건(Retry Condition, 재시도 조건)

기존 MT5 audit tool(MT5 감사 도구)을 price-proxy weights(가격 대리 가중치) 기준으로 갱신하고, `mt5_handoff_package.json`의 identity fields(정체성 필드), target windows(대상 창), feature order hash(피처 순서 해시)를 그대로 써서 MT5 snapshot(MT5 스냅샷)을 생성해야 한다.

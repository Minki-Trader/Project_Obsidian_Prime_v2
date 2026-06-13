# Frontier09 Experiment Design(전선09 실험 설계)

## Hypothesis(가설)

drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)이 future return(미래 수익), adverse excursion(불리 이동), payoff/adverse ratio(수익/불리 이동 비율), underwater burden(수중 부담), clean-close recovery(깨끗한 종가 회복)를 함께 반영하면 fixed 3-class ONNX interface(고정 3분류 온엑스 인터페이스)가 DD/curve quality(손실폭/곡선 품질)를 더 직접 배울 수 있다.

## Decision Use(결정 사용)

Stage-open design(단계 개방 설계)입니다. Effect(효과): 다음 proxy scout(프록시 탐색)가 어떤 label family(라벨 가족), control(대조군), stop condition(중단 조건)을 써야 하는지 고정합니다.

## Comparison Baseline(비교 기준)

- label_v1 reference(라벨 v1 참조)
- Frontier07 risk label reference(전선07 위험 라벨 참조)
- matched model/spec controls(같은 모델/스펙 대조군)

## Control Variables(고정 변수)

- US100 M5 Tier A(US100 5분봉 티어 A)
- 58 feature order(58개 피처 순서)
- train/validation/OOS split(학습/검증/표본밖 분할)
- fixed probs3 ONNX output(고정 3확률 온엑스 출력)
- argmax-only first scout(첫 탐색 최대확률 전용)

## Changed Variables(변경 변수)

Label target construction(라벨 목표 구성)만 바꿉니다.

## Success Criteria(성공 기준)

Strict scout clue(엄격 탐색 단서)는 validation/OOS(검증/표본밖) density 5~10/day, PF >= 1.2, DD <= 15%, ONNX parity(온엑스 동등성), learnability(학습 가능성), paired four-axis improvement(짝 네 축 개선)을 모두 요구합니다.

## Failure Criteria(실패 기준)

Class collapse(분류 붕괴), density-only improvement(밀도만 개선), validation DD far above 15%(검증 손실폭 15% 초과 지속), no paired improvement(짝 개선 없음)는 negative memory(부정 기억) 또는 capped repair(상한 수리)로 갑니다.

## Invalid Conditions(무효 조건)

Any threshold/scale(임계값/스케일)가 validation/OOS(검증/표본밖)에서 fit(적합)되면 invalid(무효)입니다.

## Evidence Plan(근거 계획)

Run manifest(실행 목록), label distribution(라벨 분포), threshold audit(임계값 감사), candidate metrics(후보 지표), model metrics(모델 지표), ONNX parity(온엑스 동등성), run registry(실행 등록부), alpha/stage ledger(알파/단계 장부)를 남깁니다.

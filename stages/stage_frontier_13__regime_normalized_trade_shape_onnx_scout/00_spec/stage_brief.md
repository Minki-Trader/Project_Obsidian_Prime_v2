# Frontier13 Stage Brief(프론티어13 단계 개요)

Stage id(단계 ID): `stage_frontier_13__regime_normalized_trade_shape_onnx_scout`

Question(질문): Can train-only regime-normalized trade-shape labels(학습 전용 레짐 정규화 거래 형상 라벨) improve the US100 M5 ONNX(US100 5분봉 온엑스) DD/density tradeoff(손실폭/빈도 상충)?

## Frontier Thesis(프론티어 가설)

US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3분류 온엑스) may improve the DD/density tradeoff(손실폭/빈도 상충) if trade-shape labels(거래 형상 라벨) are normalized by train-only regime buckets(학습 전용 레짐 버킷) rather than globally loosened label knobs(전역 라벨 파라미터 완화).

## Novelty Delta(신규성 차이)

Frontier12(프론티어12)는 global trade-shape duration labels(전역 거래 형상 보유 기간 라벨)을 시험했습니다. Frontier13(프론티어13)은 closed-bar regime features(확정 봉 레짐 피처)로 train-only path scale(학습 전용 경로 척도)를 버킷별로 만들며, class-weight density forcing(클래스 가중 빈도 강제)이나 threshold search(임계값 탐색)를 하지 않습니다.

## Do Not Repeat(반복 금지)

- same global label knob loosening(같은 전역 라벨 파라미터 완화)
- class-weight density forcing(클래스 가중 빈도 강제)
- threshold micro-search(임계값 미세 탐색)
- post-fit selector ranking(적합 후 선택기 순위)
- archive winner/baseline inheritance(보관소 승자/기준선 상속)

## Exit Rule(종료 규칙)

If Frontier13B(프론티어13B) has strict rows(엄격 행) 0 and preserved rows(보존 행) 0, or improves density(빈도) only by raising DD(손실폭), close as negative memory(부정 기억) or capped repair(상한 수리).

## Claim Boundary(주장 경계)

Only scout clue(탐색 단서), seed surface(씨앗 표면), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), or blocked(차단) may be claimed. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 forbidden(금지)입니다.

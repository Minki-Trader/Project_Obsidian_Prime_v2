# Frontier12 Stage Brief(프론티어12 단계 개요)

Stage id(단계 ID): `stage_frontier_12__trade_shape_duration_controlled_onnx_scout`

Question(질문): Can a trade-shape duration-controlled label(거래 형상과 보유 기간 통제 라벨) reduce DD(손실폭) and improve smoothness(매끄러움) for US100 M5 ONNX(US100 5분봉 온엑스)?

## Frontier Thesis(프론티어 가설)

US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3분류 온엑스) can reduce validation/OOS DD(검증/표본밖 손실폭) only if the label source(라벨 원천) encodes a trade lifecycle(거래 생명주기): early adverse excursion veto(초기 불리 이동 배제), favorable path confirmation(유리 경로 확인), capped hold duration(상한 보유 기간), MAE/MFE quality(최대 불리/유리 이동 품질), and density-aware neutral(빈도 인식 중립) before model fitting(모델 적합 전).

## Novelty Delta(신규성 차이)

Frontier04/07/09/10(프론티어04/07/09/10)은 path, adverse, clean-path, utility label families(경로/불리 이동/깨끗한 경로/효용 라벨 계열)를 시험했고 Frontier11(프론티어11)은 same-pool selector(같은 후보군 선택기)를 시험했습니다. Frontier12(프론티어12)는 inherited candidates(상속 후보)나 post-fit ranking(적합 후 순위)이 아니라 pre-fit trade-shape label contract(적합 전 거래 형상 라벨 계약)을 시험합니다.

## Do Not Repeat(반복 금지)

- same F10C candidate-pool selector tweak(같은 F10C 후보군 선택기 조정)
- side-weight ladder(방향 가중 사다리)
- density bridge(빈도 브리지)
- threshold micro-search(임계값 미세 탐색)
- archive winner/baseline inheritance(보관소 승자/기준선 상속)

## Exit Rule(종료 규칙)

If Frontier12B(프론티어12B) produces strict rows(엄격 행) 0 and preserved rows(보존 행) 0, or validation DD floor(검증 손실폭 바닥) remains high without a new local repair surface(새 로컬 수리 표면), close as negative memory(부정 기억) or capped repair(상한 수리).

## Claim Boundary(주장 경계)

This stage(이 단계)는 scout clue(탐색 단서), seed surface(씨앗 표면), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), or blocked(차단)만 말할 수 있습니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 forbidden(금지)입니다.

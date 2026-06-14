# Frontier11 Stage Brief(전선11 단계 개요)

Stage id(단계 ID): `stage_frontier_11__subperiod_stability_first_onnx_scout`

Question(질문): Can subperiod stability-first selection(하위기간 안정성 우선 선택) improve zoomed DD(확대 구간 손실폭) and equity smoothness(자산곡선 매끄러움) for fixed 3-class ONNX(고정 3분류 ONNX)?

Frontier thesis(전선 가설): When choosing fixed 3-class ONNX candidates(고정 3분류 ONNX 후보 선택) for US100 M5, subperiod stability(하위기간 안정성), worst-slice drawdown(최악 구간 손실폭), time-under-water proxy(회복 전 체류 시간 프록시), and equity smoothness proxy(자산곡선 매끄러움 프록시) may reduce zoomed DD(확대 구간 손실폭) and curve chop(곡선 출렁임) better than aggregate validation/OOS(검증/표본밖 합계) selection.

Novelty delta(신규성 차이): Frontier07~10(전선07~10)은 label/objective/weight/bridge(라벨/목적/가중/브리지)를 바꿨습니다. Frontier11(전선11)은 those surfaces(그 표면들)를 reference-only(참조 전용)로 고정하고 post-fit candidate ranking(적합 후 후보 순위)과 validation philosophy(검증 철학)를 바꿉니다.

Prior archive boundary(이전 보관소 경계): Stage171(171단계)은 legacy adapter(레거시 어댑터)의 segment/equity/concentration audit(구간/자산곡선/집중도 감사)였고 repair stage(수리 단계)로 넘겼습니다. Stage273(273단계)은 q04 time-risk router(q04 시간 위험 라우터) MT5 stability validation(MT5 안정성 검증)였고 negative handoff(부정 인계)였습니다. Frontier11(전선11)은 winner/baseline(승자/기준선)을 상속하지 않고 Python fixed-argmax ONNX proxy scout(파이썬 고정 최대확률 ONNX 프록시 탐색)의 post-fit selection surface(적합 후 선택 표면)를 새로 시험합니다.

Do not repeat(반복 금지):
- side-weight ladder(방향 가중 사다리)
- density bridge(밀도 브리지)
- threshold micro-search(임계값 미세 탐색)
- F10-class capped repair(전선10급 상한 수리)
- archive winner/baseline inheritance(보관소 승자/기준선 상속)

Frozen surfaces(고정 표면):
- label family(라벨군)
- objective family(목적군)
- weight family(가중군)
- argmax-only ONNX output schema(최대확률 전용 ONNX 출력 스키마)

Exit rule(종료 규칙): if strict rows(엄격 행)가 0이고 subperiod selector(하위기간 선택기)가 validation DD(검증 손실폭)나 worst-slice DD(최악 구간 손실폭)를 개선하지 못하면 negative memory(부정 기억)로 닫습니다. preserved clue(보존 단서)가 있으면 capped repair(상한 수리)는 selection metric spec(선택 지표 명세) 안에서 한 번만 허용합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

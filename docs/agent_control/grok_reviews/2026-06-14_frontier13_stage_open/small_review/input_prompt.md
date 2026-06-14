Frontier13 stage-open review(프론티어13 단계 개방 검토)입니다.

Please answer in this response only(이 응답 안에서만 답하세요). Do not say you will write a file(파일을 쓰겠다고 말하지 마세요).

Current truth(현재 진실):
- Frontier12(프론티어12)는 `closed_negative_memory_no_authority`입니다.
- Frontier12 result(프론티어12 결과): strict scout clue rows(엄격 탐색 단서 행) 0, preserved clue rows(보존 단서 행) 0.
- Frontier12 best candidate(프론티어12 최고 후보): validation PF/density/DD(검증 수익 팩터/빈도/손실폭) 0.964967 / 2.21311/day / 30.4882%, OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭) 1.88145 / 0.641221/day / 3.03685%.
- Frontier12 negative memory(프론티어12 부정 기억): trade-shape duration labels(거래 형상 보유 기간 라벨)은 DD floor(손실폭 바닥)를 낮췄지만 validation PF/density(검증 수익 팩터/빈도)와 worst subperiod concentration(최악 하위기간 집중)을 통과하지 못했습니다.
- Frontier12 do-not-repeat(프론티어12 반복 금지): same label knob loosening(같은 라벨 파라미터 완화), class-weight density forcing(클래스 가중 빈도 강제), threshold micro-search(임계값 미세 탐색).
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claim(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).

Codex proposed next frontier(코덱스 제안 다음 프론티어):
- `stage_frontier_13__regime_normalized_trade_shape_onnx_scout`
- Hypothesis(가설): fixed 3-class ONNX(고정 3분류 온엑스)가 train-only regime-normalized trade-shape labels(학습 전용 레짐 정규화 거래 형상 라벨)을 쓰면, F12의 low-DD but sparse(낮은 손실폭이지만 희소한) 표면을 같은 라벨 파라미터 완화 없이 더 넓은 시장 상태에 맞출 수 있습니다.
- Novelty(신규성): label thresholds(라벨 임계값)을 validation/OOS(검증/표본밖)로 조정하지 않고, train-only regime buckets(학습 전용 레짐 버킷)별 path scale(경로 척도)을 고정합니다. Regime buckets(레짐 버킷)는 session/cash-open(세션/현금장 개장), volatility tercile(변동성 삼분위), trend-strength bucket(추세 강도 버킷), squeeze flag(압축 플래그) 같은 closed-bar features(확정 봉 피처)에서만 만듭니다.
- Proxy plan(프록시 계획): create three fixed regime-normalization schemes(고정 레짐 정규화 방식 3개), train fixed argmax ONNX models(고정 최대확률 온엑스 모델), check ONNX parity(온엑스 동등성), aggregate + month/quarter subperiod metrics(합계 및 월/분기 하위기간 지표), paired Tier records(짝 티어 기록). Tier B/combined(티어B/합산)은 source unavailable(원천 없음)이면 missing_required(필수 누락)로 기록합니다.
- Scout success boundary(탐색 성공 경계): validation/OOS density(검증/표본밖 빈도) 5~10/day(일 5~10회), PF(수익 팩터) >= 1.2, DD(손실폭) <= 15%, positive net(양수 순손익), ONNX parity(온엑스 동등성), and improved worst subperiod DD(최악 하위기간 손실폭 개선). This is not final completion(최종 완성 아님).

Required output(필수 출력):
1. Classification(분류): accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요).
2. One-sentence reason(한 문장 이유).
3. Required local checks(필수 로컬 확인): before materializing the stage(단계를 물질화하기 전).
4. Key design risks(핵심 설계 위험): especially leakage(누수), overfit(과적합), regime bucketing selection bias(레짐 버킷 선택 편향), and hidden threshold search(숨은 임계값 탐색).
5. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

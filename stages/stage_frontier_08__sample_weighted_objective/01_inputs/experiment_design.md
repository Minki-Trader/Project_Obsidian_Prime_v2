# Experiment Design(실험 설계)

- hypothesis(가설): Multi-objective per-row sample weighting may change train loss geometry enough to favor clean path-quality rows without changing runtime threshold or output contract(다중목적 행별 표본 가중은 런타임 임계값이나 출력 계약을 바꾸지 않고 깨끗한 경로 품질 행을 더 배우게 할 수 있음).
- decision_use(결정 용도): scout clue(탐색 단서) 여부만 판단합니다.
- comparison_baseline(비교 기준): each weighted model(각 가중 모델)은 same target/model unweighted control(같은 목표/모델의 무가중 대조군)과 비교합니다.
- control_variables(통제 변수): feature_set_v2(피처 세트 v2), chronological split(시간순 분할), `[p_short, p_flat, p_long]` output(출력), ONNX parity check(온엑스 동등성 검사).
- changed_variables(변경 변수): train-only per-row sample weighting policy(학습 전용 행별 표본 가중 정책).
- sample_scope(표본 범위): US100 M5, train/validation/OOS split(학습/검증/표본밖 분할), Tier A separate(티어 A 분리); Tier B/combined(티어 B/합산)은 불가 시 missing_required(필수 누락).
- success_criteria(성공 기준): validation and OOS(검증과 표본밖) both improve four-axis distance(네 축 거리), with density(밀도) closer to 5-10/day(일 5~10회), PF lift(수익 팩터 상승), DD reduction(손실폭 감소), smoothness proxy improvement(매끄러움 대리 개선), and ONNX parity(온엑스 동등성).
- failure_criteria(실패 기준): only one axis improves(한 축만 개선), validation/OOS disagreement(검증/표본밖 불일치), or repeated density-DD tradeoff(밀도-손실폭 교환 반복).
- invalid_conditions(무효 조건): validation/OOS used to fit weights or thresholds(검증/표본밖으로 가중치/임계값 적합), feature order drift(피처 순서 이탈), nonfinite features(비정상 피처), missing ONNX parity(온엑스 동등성 누락).
- stop_conditions(중지 조건): strict scout rows(엄격 탐색 행) 0 and no new preserved clue(새 보존 단서 없음), or capped repair would only repeat Frontier07(전선07 반복).
- evidence_plan(근거 계획): run_manifest.json(실행 목록), candidate summaries(후보 요약), ONNX parity rows(온엑스 동등성 행), run registry(실행 등록부), alpha/stage ledgers(알파/단계 장부), required gate audit(필수 게이트 감사).

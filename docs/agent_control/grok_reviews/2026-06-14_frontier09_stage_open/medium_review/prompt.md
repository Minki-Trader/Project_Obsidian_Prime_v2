Frontier09 stage-open review(전선09 단계 개방 검토) 요청입니다.

Codex current truth(코덱스 현재 진실):
- Current closed stage(현재 마감 단계): stage_frontier_08__sample_weighted_objective.
- Latest completed run(최근 완료 실행): frontier08D_stage_closeout_sample_weight_objective_v1.
- Frontier08 judgment(전선08 판정): closed_preserved_clue_negative_memory_no_authority(보존 단서 + 부정 기억 + 권위 없음).
- Frontier08 preserved clue(전선08 보존 단서): adverse/path utility sample weighting(불리 이동/경로 효용 표본 가중)은 OOS density(표본밖 밀도)를 5~6/day 부근으로 만들 수 있었다.
- Frontier08 negative memory(전선08 부정 기억): sample weighting alone(표본 가중 단독)은 validation DD(검증 손실폭) 58~60%와 weak PF(약한 수익 팩터)를 해결하지 못했다.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Proposed Frontier09 direction(제안 전선09 방향):
- Stage id(단계 ID): stage_frontier_09__drawdown_normalized_clean_path_labeling.
- Run id(실행 ID): frontier09A_stage_open_drawdown_clean_path_labeling_v1.
- Hypothesis(가설): drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)이 future return(미래 수익)만 보지 않고 adverse excursion(불리 이동), payoff/adverse ratio(수익/불리 이동 비율), time-underwater proxy(수중 시간 대리값), and clean-close recovery(깨끗한 종가 회복)를 함께 라벨에 반영하면, fixed 3-class ONNX interface(고정 3분류 온엑스 인터페이스)가 DD/curve quality(손실폭/곡선 품질)를 더 직접 배울 수 있다.
- Novelty delta(신규성 차이): Frontier08(전선08)은 same labels + sample weighting(동일 라벨 + 표본 가중)만 바꿨다. Frontier09(전선09)는 target representation(목표 표현)을 바꿔, 나쁜 곡선 기여 가능성이 높은 rows(행)를 flat/no-trade(관망/무거래) 라벨로 만든다.
- Reference only(참조 전용): Frontier07 risk label(전선07 위험 라벨), Frontier08 sample-weight clue(전선08 표본 가중 단서)는 comparison/control(비교/대조)로만 쓰며 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않는다.

Proposed scout design(제안 탐색 설계):
- Data(데이터): existing Tier A(티어 A) US100 M5 model input dataset with 58 features(58개 피처), train/validation/OOS split(학습/검증/표본밖 분할) unchanged.
- Label construction(라벨 생성): train-only thresholds(학습 전용 임계값) from future path diagnostics(미래 경로 진단). Candidate long/short labels require directional return plus clean path quality(방향 수익 + 깨끗한 경로 품질). Otherwise flat(관망).
- Variant families(변형 가족):
  1. payoff_adverse_ratio(수익/불리 이동 비율): reward must dominate MAE(불리 이동).
  2. underwater_burden(수중 부담): intra-horizon adverse bars(수평선 내 불리 봉 수) must stay low.
  3. clean_recovery(깨끗한 회복): close return(종가 수익) and MFE capture(최대 유리 이동 포착)가 동시에 필요.
- Controls(대조군): label_v1 reference(라벨 v1 참조), Frontier07 risk label reference(전선07 위험 라벨 참조), and matched model/spec controls(같은 모델/스펙 대조).
- Models(모델): same lightweight sklearn specs(가벼운 sklearn 스펙) as prior scouts: logistic plain, logistic balanced, small RF balanced.
- Runtime interface(런타임 인터페이스): output remains [p_short, p_flat, p_long]([숏, 관망, 롱]); argmax-only(최대확률 전용); no threshold/abstention search(임계값/기권 탐색 없음) in the first scout.
- ONNX parity(온엑스 동등성): required per model.

Scout success criteria(탐색 성공 기준):
- Strict scout clue(엄격 탐색 단서): validation and OOS(검증과 표본밖) density 5~10/day, PF >= 1.2, DD <= 15%, ONNX parity true(온엑스 동등성 참), learnability pass(학습 가능성 통과), and paired improvement across density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움 짝 개선).
- Preserved clue(보존 단서): no strict clue(엄격 단서 없음), but at least 3 paired axes improve(3개 이상 짝 축 개선) with parity true(동등성 참) and no degenerate class collapse(분류 붕괴 없음).
- WFO/MT5(WFO/MT5): do not run unless strict scout clue(엄격 탐색 단서) appears and Grok pre-expensive review(그록 비싼 검증 전 검토) passes.

Failure/stop criteria(실패/중단 기준):
- If labels collapse to nearly all flat(거의 전부 관망) or one side(한 방향) on train split(학습 분할), variant invalid(무효 변형).
- If validation DD(검증 손실폭) remains far above 15% and no paired axis improvement(짝 개선 없음), preserve negative memory(부정 기억 보존).
- If only density improves(밀도만 개선) while PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 악화되면 close or capped repair(마감 또는 상한 수리).

Claim boundary(주장 경계):
- This is stage-open design(단계 개방 설계), not completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
- Future labels are oracle labels(미래 오라클 라벨) for supervised learning(지도학습) only; they are not runtime signals(런타임 신호 아님).

Question(질문):
Should Codex open Frontier09(전선09) with this drawdown-normalized clean path labeling(손실폭 정규화 깨끗한 경로 라벨링) direction? Please classify as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요), and focus on novelty delta(신규성 차이), leakage boundary(누수 경계), controls(대조군), and whether this avoids merely repeating Frontier07/08(전선07/08 반복).

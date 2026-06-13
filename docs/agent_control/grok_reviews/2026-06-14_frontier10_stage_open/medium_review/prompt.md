Frontier10 stage-open review(전선10 단계 개방 검토) 요청입니다.

Codex current truth(코덱스 현재 진실):
- Current closed stage(현재 마감 단계): `stage_frontier_09__drawdown_normalized_clean_path_labeling`.
- Latest completed run(최근 완료 실행): `frontier09D_stage_closeout_drawdown_clean_path_labeling_v1`.
- Frontier09 judgment(전선09 판정): `closed_preserved_clue_negative_memory_no_authority`.
- Preserved clue(보존 단서): payoff/adverse ratio(수익/불리 이동 비율), directional class-prior bridge(방향 클래스 사전분포 브리지), train-only clean path label audit pattern(학습 전용 깨끗한 경로 라벨 감사 패턴).
- Negative memory(부정 기억): validation DD(drawdown, 검증 손실폭) remained 56~64%, strict scout clue rows(엄격 탐색 단서 행) stayed 0, and the same clean path density bridge repair(깨끗한 경로 밀도 브리지 수리) must not be repeated.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

Codex proposed Frontier10 direction(코덱스 제안 전선10 방향):
- Stage id(단계 ID): `stage_frontier_10__split_consistent_utility_distillation`.
- Run id(실행 ID): `frontier10A_stage_open_split_consistent_utility_distillation_v1`.
- Next run(다음 실행): `frontier10B_utility_distillation_proxy_scout_v1`.
- Hypothesis(가설): a single fixed 3-class ONNX interface(고정 3분류 ONNX 인터페이스) may learn a cleaner trade/no-trade decision if the target is a train-only split-consistent utility distillation label(학습 전용 분할 일관 효용 증류 라벨), where long/short labels require favorable realized path utility(우호적 실현 경로 효용) and agreement across train subwindows(학습 하위구간 합의), while conflicted or DD-heavy rows(충돌 또는 손실폭 큰 행) become flat/no-trade(관망/무거래).
- Novelty delta(신규성 차이): Frontier07(전선07) changed adverse-risk labels(불리 위험 라벨), Frontier08(전선08) changed per-row sample weights(행별 표본 가중), and Frontier09(전선09) changed clean-path target representation(깨끗한 경로 목표 표현). Frontier10(전선10) changes the decision supervision philosophy(의사결정 감독 철학): only train-side utility that is stable across subwindows can become a trade label(거래 라벨), so density/PF/DD/smoothness(거래 밀도/수익 팩터/손실폭/매끄러움) are constrained before model fitting(모델 학습 전).

Proposed experiment design(제안 실험 설계):
- Data source(데이터 원천): existing US100 M5 Tier A model input dataset(기존 US100 5분봉 Tier A 모델 입력 데이터셋) with fixed 58 feature order(고정 58개 피처 순서).
- Time axis(시간축): closed-bar M5 timestamps(확정 5분봉 타임스탬프), existing train/validation/OOS split(기존 학습/검증/표본밖 분할).
- Feature-label boundary(피처-라벨 경계): features use only current/past closed bars(현재/과거 확정봉만 사용); future path utility(미래 경로 효용)는 label construction(라벨 생성)에만 쓰고, thresholds/scales(임계값/스케일)는 train split(학습 분할)에서만 fit(적합)합니다.
- Target families(목표군):
  1. utility_consensus(효용 합의): long/short utility must be positive after adverse-burden and cost proxies(불리 부담과 비용 대리값 이후 양수) and must agree across train subwindows(학습 하위구간 합의).
  2. utility_margin(효용 마진): winning side utility must exceed the opposite side and flat utility by a train-only margin(학습 전용 마진).
  3. drawdown_veto_distillation(손실폭 거부 증류): rows that historically create high underwater burden(높은 수중 부담)을 flat/no-trade(관망/무거래)로 distill(증류) even if raw return is positive(원시 수익이 양수라도).
- Models(모델): ONNX-exportable sklearn classifiers(ONNX 내보내기 가능한 sklearn 분류기) with fixed `[p_short, p_flat, p_long]` output(고정 출력), argmax-only(최대 확률 전용), no threshold search(임계값 탐색 없음) in the first scout.
- Controls(대조군): label_v1 reference(라벨 v1 참조), Frontier07 risk label reference(전선07 위험 라벨 참조), Frontier09 payoff/adverse ratio preserved clue(전선09 수익/불리 이동 비율 보존 단서), and matched model/spec controls(동일 모델/규격 대조군).

Success criteria(성공 기준):
- Strict scout clue(엄격 탐색 단서): validation and OOS(검증과 표본밖) both have density 5~10/day(일 5~10회), PF >= 1.2(수익 팩터 1.2 이상), DD <= 15%(손실폭 15% 이하), ONNX parity true(ONNX 동등성 참), and paired improvement across density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움 짝 개선).
- Preserved clue(보존 단서): no strict clue(엄격 단서 없음), but at least 3 axes improve(3개 이상 축 개선), ONNX parity true(ONNX 동등성 참), and no degenerate class collapse(분류 붕괴 없음).
- WFO/MT5(WFO/MT5): do not run unless strict scout clue(엄격 탐색 단서) appears and Grok pre-expensive review(비싼 검증 전 그록 검토) passes.

Failure/stop criteria(실패/중단 기준):
- If utility consensus(효용 합의) collapses density below 2/day(일 2회 미만) or creates almost all flat labels(거의 전부 관망 라벨), classify invalid or negative depending on cause(원인에 따라 무효 또는 부정).
- If validation DD(검증 손실폭) remains far above 15% with no paired axis improvement(짝 개선 없음), close or capped repair(마감 또는 상한 수리).
- If it only repeats Frontier09 clean-path density bridge(전선09 깨끗한 경로 밀도 브리지 반복) without a split-consistency mechanism(분할 일관 장치), reject as novelty failure(신규성 실패).

Claim boundary(주장 경계):
- This is stage-open design(단계 개방 설계), not completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
- Future utility labels(미래 효용 라벨)은 supervised learning targets(지도학습 목표) only, not runtime signals(런타임 신호 아님).

Question(질문):
Should Codex open Frontier10(전선10) with split-consistent utility distillation(분할 일관 효용 증류) as the next hypothesis lifecycle(다음 가설 생명주기)? Please classify as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요), and focus on novelty delta(신규성 차이), leakage boundary(누수 경계), controls(대조군), and whether this is a better next move than another label/weight/bridge repair(라벨/가중/브리지 수리 반복).

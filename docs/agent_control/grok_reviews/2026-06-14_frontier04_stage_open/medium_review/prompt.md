You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier04 stage-open(전선04 단계 개방) proposal.

Current truth(현재 진실):
- Parent stage(부모 단계): `stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling`
- Parent closeout(부모 마감): `frontier03G_stage_closeout_v1` closed as preserved clue plus negative memory(보존 단서+부정 기억).
- Frontier03 preserved clue(전선03 보존 단서): `f03e_repair__f03b_v04_trend_easy_chop_strict__both__p40__m4__cd6`, OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `1.20533 / 4.05344/day / 6.90935%`, but validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `1.00822 / 3.62842/day / 15.5453%`.
- Frontier03 negative memory(전선03 부정 기억): oracle label replay(오라클 라벨 재생)가 trainable ONNX(학습 가능 온엑스)로 충분히 전달되지 않았고, decision-surface repair(결정 표면 수리)는 density/DD trade-off(밀도/손실폭 트레이드오프)를 만들었다.

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Open Frontier04(전선04) as `path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링)`.
- Hypothesis(가설): A forward path label(전방 경로 라벨) that uses next-bar high/low path(다음 봉 고가/저가 경로), adverse excursion(불리한 움직임), favorable excursion(유리한 움직임), and rough cost(대략 비용) can filter out close-only labels(종가 전용 라벨) that look profitable but create validation DD(검증 손실폭).
- Novelty delta(신규성 차이): label philosophy(라벨 철학) changes from future close return(미래 종가 수익률) to event/path outcome(이벤트/경로 결과). Feature set(피처 세트)은 fixed `feature_set_v2`로 유지한다. No winner/baseline/promotion(승자/기준선/승격) is inherited.
- First scout(첫 탐색): Frontier04B(전선04B)는 no-model label proxy scout(모델 없는 라벨 프록시 탐색) only. It will use fixed model input rows(고정 모델 입력 행) plus raw US100 OHLC(원천 US100 시가/고가/저가/종가) to compute 12-bar and 18-bar event labels(12봉/18봉 이벤트 라벨).
- Candidate label family(후보 라벨군): target/stop multiples(목표/손절 배수) from train ATR/return scale(학습 ATR/수익률 척도), e.g. 0.8/0.6, 1.0/0.7, 1.2/0.8, with timeout behavior(시간 만료 행동) and event-first rule(이벤트 우선 규칙).
- Success for opening(개방 성공): Grok agrees this is novel enough and bounded enough to run Frontier04B. Success for Frontier04B(전선04B 성공)는 validation and OOS(검증/표본밖) both positive, OOS density(표본밖 밀도) at least near 4.5/day, PF(수익 팩터) above 1.2, DD(손실폭) under 10% as scout criteria only.
- Stop condition(중지 조건): if no path-aware proxy row improves simultaneous density/PF/DD(밀도/수익 팩터/손실폭 동시성), close as negative memory(부정 기억) rather than repeat threshold sweeps(임계값 반복 탐색).

Bounded evidence(제한 근거):
- Frontier03 closeout report(전선03 마감 보고서): `stages/stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling/03_reviews/frontier03G_stage_closeout_v1_report.md` sha256 `73f44216739396dc8cdbc1be0277b94371af70c47eda00a99b0b9b15d46f895d`
- Frontier03 decision(전선03 결정): `docs/decisions/2026-06-14_stage_frontier_03_regime_conditioned_asymmetric_onnx_labeling_closeout.md` sha256 `0f37ef493515c424b478feaf292753db57ebbe0b3cddca319d4711ec2c9d0e8d`
- Model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- Feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt` sha256 `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`
- Raw US100 M5(원천 US100 5분봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv` rows `261345`, price basis(가격 기준) `Bid`, timezone status(시간대 상태) `UNRESOLVED_REQUIRES_MANUAL_BINDING`

Focused question(집중 질문):
Should Codex(코덱스) open Frontier04(전선04) with path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링), or is this too close to Frontier03/old repair loops(전선03/이전 수리 반복) and should a different hypothesis be chosen?

Please answer in this structure:
1. Recommendation(권고): open_frontier04(전선04 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier04B(전선04B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)


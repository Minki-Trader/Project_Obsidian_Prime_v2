You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier05 stage-open(전선05 단계 개방) proposal.

Current truth(현재 진실):
- Active parent closeout(부모 마감): `stage_frontier_04__path_aware_cost_dd_event_labeling` / `frontier04E_stage_closeout_v1`.
- Frontier04 preserved clue(전선04 보존 단서): path-aware event labels can create a clean oracle seed surface(경로 이벤트 라벨은 깨끗한 오라클 씨앗 표면을 만들 수 있음). Best proxy(최상위 프록시) validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `18.6473 / 7.8579/day / 6.5335%`; OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `214.983 / 5.9237/day / 1.1535%`.
- Frontier04 negative memory(전선04 부정 기억): feature_set_v2 plus small fixed models did not transfer the oracle surface into usable ONNX metrics(피처 세트 v2와 작은 고정 모델은 오라클 표면을 쓸만한 온엑스 지표로 전달하지 못함). Best trainable model(최상위 학습 모델) validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `0.9769 / 25.1475/day / 74.7387%`; OOS `0.9651 / 26.6794/day / 40.1913%`.
- Stage12-364 and Frontier04 are reference only(참조 전용). No winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비) is inherited.

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Open Frontier05(전선05) as `closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면)`.
- Hypothesis(가설): Frontier04 failed at oracle-to-model transfer(오라클에서 모델 전달) because `feature_set_v2` lacks closed-bar precursors(확정봉 선행 단서) of favorable/adverse path quality(유리/불리 경로 품질). A stage-local augmented feature surface(단계 로컬 증강 피처 표면) using only current and prior closed US100 M5 OHLC(현재와 과거 확정 US100 5분봉 시가/고가/저가/종가) may make the preserved path label learnable enough to reduce simultaneous PF/density/DD failure(수익 팩터/밀도/손실폭 동시 실패).
- Novelty delta(신규성 차이): changed variable(변경 변수)은 label threshold(라벨 임계값)가 아니라 feature surface(피처 표면)입니다. The path label is used as a fixed reference target(고정 참조 목표) only to test learnability(학습 가능성), not as an inherited baseline(상속 기준선).
- First scout(첫 탐색): Frontier05B(전선05B)는 proxy/model scout(프록시/모델 탐색) only. It compares feature_set_v2(피처 세트 v2) against feature_set_v2 plus closed-bar path precursor features(피처 세트 v2 + 확정봉 경로 선행 피처) on identical rows/splits(동일 행/분할).
- Candidate closed-bar precursor families(후보 확정봉 선행 피처군): wick/body pressure(꼬리/몸통 압력), recent excursion asymmetry(최근 진폭 비대칭), volatility compression/expansion(변동성 수축/확장), range percentile(범위 분위), impulse decay(충격 감쇠), trend persistence(추세 지속), and adverse-tail clustering(불리한 꼬리 군집). All features must be right-aligned closed-bar only(모든 피처는 우측 정렬 확정봉 전용).
- Architecture boundary(구조 경계): Stage-local prototype(단계 로컬 원형)은 `stage_pipelines/stage_frontier_05/`에 둔다. Any reusable feature logic(재사용 피처 로직)은 later foundation owner decision(이후 foundation 소유 결정) 없이는 `foundation/features` truth(진실 원천)가 되지 않는다.
- Success for opening(개방 성공): Grok agrees this is a distinct hypothesis lifecycle(별도 가설 생명주기), or narrows the scout without blocking. Success for Frontier05B(전선05B 성공)는 not final completion(최종 완성 아님); it is only scout clue(탐색 단서) if augmented features materially improve trainable retention(학습 전달 유지율) while keeping validation/OOS density nearer 5-10/day and DD below 10% as exploratory target distance(탐색 목표 거리).
- Stop condition(중지 조건): if augmented closed-bar precursors do not improve learnability versus feature_set_v2, close as negative memory(부정 기억) or preserved clue(보존 단서) without repeating label threshold sweeps(라벨 임계값 반복 탐색).

Bounded evidence(제한 근거):
- Frontier04 closeout report(전선04 마감 보고서): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04E_stage_closeout_v1_report.md` sha256 `fdcb53e084da4c0825a9c81f43cfced2e4caa2a1c42ac7c17adc35828cac7e12`
- Frontier04 proxy report(전선04 프록시 보고서): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04B_path_aware_label_proxy_scout_v1_report.md` sha256 `e5e676df2b5417ae0dcca6fdad3874618e86b08e7fc53a67412882078a605868`
- Frontier04 trainable report(전선04 학습 보고서): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04D_trainable_path_label_onnx_probe_v1_report.md` sha256 `c47c5296dee15805e57ebeaf2cd24a752615cd9f94c6e532eea313ffeaf21b7c`
- Frontier04 closeout decision(전선04 마감 결정): `docs/decisions/2026-06-14_stage_frontier_04_path_aware_cost_dd_event_labeling_closeout.md` sha256 `445deb781559d8236b2de639cee19305551ec9aeedae3f2b9e7654740a205acb`
- Model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- Feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt` sha256 `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`
- Raw US100 M5(원천 US100 5분봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv` rows `261345`, price basis(가격 기준) `Bid`, timezone status(시간대 상태) `UNRESOLVED_REQUIRES_MANUAL_BINDING`

Focused question(집중 질문):
Should Codex(코덱스) open Frontier05(전선05) with closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면), or is this too close to Frontier04 repair(전선04 수리) and should a different hypothesis be chosen?

Please answer in this structure:
1. Recommendation(권고): open_frontier05(전선05 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier05B(전선05B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)


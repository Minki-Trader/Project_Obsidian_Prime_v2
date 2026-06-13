# Frontier05B Closed-Bar Path Precursor Feature Scout Report(전선05B 확정봉 경로 선행 피처 탐색 보고서)

Updated(갱신): 2026-06-13T19:40:35Z

Status(상태): `feature_surface_no_transfer_improvement_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): feature_set_v2 only arm(피처 세트 v2 단독 비교군)과 feature_set_v2 plus closed-bar path precursors arm(피처 세트 v2 + 확정봉 경로 선행 피처 비교군)을 같은 locked path label(고정 경로 라벨), rows(행), split(분할), model specs(모델 설정)에서 학습했습니다.

Effect(효과): Frontier04(전선04)의 oracle-to-model transfer collapse(오라클에서 모델 전달 붕괴)가 feature surface bottleneck(피처 표면 병목) 때문인지 통제 비교(controlled comparison, 통제 비교)로 확인했습니다.

## Best Read(최상위 판독)

- best arm(최상위 비교군): `v2_only(피처세트v2단독)`
- best model(최상위 모델): `logreg_l2_c0p5_plain_argmax`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `1.89031` / `0.916031/day` / `5.86171%`
- improvement pass rows(개선 통과 행): `0`

## Best Arm Comparison(최상위 비교군 비교)

- model(모델): `logreg_l2_c0p5_plain_argmax`
- validation score improvement ratio(검증 점수 개선 비율): `0.15259`
- OOS score improvement ratio(표본밖 점수 개선 비율): `0.0277112`
- combined score improvement ratio(합산 점수 개선 비율): `0.128183`
- feature_surface_improvement_pass(피처 표면 개선 통과): `False`

## Data Integrity(데이터 무결성)

- integrity_judgment(무결성 판정): `usable_with_boundary(경계부 사용 가능)`
- time_axis(시간축): model timestamp(모델 타임스탬프) is matched to raw time_close_unix as broker_clock_close_key(브로커 시계 종가 키); timezone_status remains unresolved, so this is not a direct UTC market-session claim(직접 UTC 세션 주장 아님).
- feature_label_boundary(피처-라벨 경계): precursor features use current/prior closed raw OHLC only(선행 피처는 현재/과거 확정 원천 OHLC만 사용); fixed label uses future OHLC as supervised target only(고정 라벨은 지도학습 목표로만 미래 OHLC 사용).
- leakage_risk(누수 위험): path labels are oracle labels(미래 경로를 아는 라벨) and cannot be interpreted as runtime signals(런타임 신호). current bar high/low is excluded by starting at t+1(현재 봉 고저는 t+1 시작으로 제외).

## Artifacts(산출물)

- arm comparison(비교군 비교): `stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/arm_comparison.csv`
- model metrics(모델 지표): `stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/model_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/onnx_parity.csv`
- feature manifest(피처 목록): `stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/feature_manifest.json`
- run manifest(실행 목록): `stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/run_manifest.json`

## Next Action(다음 행동)

`frontier05C_feature_surface_repair_or_closeout_decision_v1`. Action(행동)은 결과에 따라 Grok pre-expensive review(그록 사전 고비용 검토) 또는 repair/closeout decision(수리/마감 결정)으로 넘기는 것입니다. Effect(효과)는 scout clue(탐색 단서)를 WFO/MT5(워크포워드/메타트레이더5) 주장으로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

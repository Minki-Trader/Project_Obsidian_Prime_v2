# Frontier04B Path-Aware Label Proxy Scout Report(전선04B 경로 인식 라벨 프록시 탐색 보고서)

Updated(갱신): 2026-06-13T19:05:21Z

Status(상태): `scout_clue_found_no_authority`

Judgment(판정): `seed_surface(씨앗 표면)`

## Action And Effect(행동과 효과)

Action(행동): Frontier04B(전선04B)는 raw US100 OHLC(원천 US100 시가/고가/저가/종가)를 model input rows(모델 입력 행)에 정렬하고, p90 train scale(학습 90분위 척도)의 path event labels(경로 이벤트 라벨)을 proxy-only(프록시 전용)로 계산했습니다.

Effect(효과): ONNX(온엑스), WFO(워크포워드), MT5(메타트레이더5) 전에 label axis(라벨 축)이 density/PF/DD(밀도/수익 팩터/손실폭)를 동시에 만족할 수 있는지 좁게 확인했습니다.

## Data Integrity(데이터 무결성)

- integrity_judgment(무결성 판정): `usable_with_boundary(경계부 사용 가능)`
- time_axis(시간축): model timestamp(모델 타임스탬프) is matched to raw time_close_unix as broker_clock_close_key(브로커 시계 종가 키); timezone_status remains unresolved, so this is not a direct UTC market-session claim(직접 UTC 세션 주장 아님).
- feature_label_boundary(피처-라벨 경계): labels use only raw future OHLC after the current closed bar(현재 종료봉 이후 원천 미래 OHLC만 사용); feature_set_v2 columns are not loaded into label construction(피처 컬럼은 라벨 생성에 로드하지 않음).
- leakage_risk(누수 위험): path labels are oracle labels(미래 경로를 아는 라벨) and cannot be interpreted as runtime signals(런타임 신호). current bar high/low is excluded by starting at t+1(현재 봉 고저는 t+1 시작으로 제외).

## Best Path Row(최상위 경로 행)

- variant(변형): `f04b_path_h12_t1p20_s0p80_trainp90`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `18.6473` / `7.85792/day` / `6.53351%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `214.983` / `5.92366/day` / `1.1535%`
- joint pass(동시 통과): `True`

## Grok Bounds(그록 경계)

- proxy-only gate(프록시 전용 게이트): satisfied(충족), no ONNX/WFO/MT5(온엑스/WFO/MT5 없음).
- OHLC alignment preflight(원천 OHLC 정렬 사전 점검): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04B_path_aware_label_proxy_scout_v1/alignment.json`.
- controlled comparison(통제 비교): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04B_path_aware_label_proxy_scout_v1/summary.csv` includes path label(경로 라벨) and close-return baseline(종가 수익률 기준).
- Stage355 precedent(Stage355 선례): run manifest(실행 목록)에 `first_barrier_labels`를 인용했습니다.

## Next Action(다음 행동)

`frontier04C_grok_pre_trainable_transfer_review_v1`. Action(행동)은 Grok pre-expensive review(그록 사전 고비용 검토)를 열어 이 seed surface(씨앗 표면)를 trainable transfer(학습 가능 전달)로 넘길지 묻는 것입니다. Effect(효과)는 proxy oracle(프록시 오라클)을 ONNX promise(온엑스 약속)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

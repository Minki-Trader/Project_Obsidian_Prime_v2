# F77 Stage Brief(F77 단계 개요)

Stage id(단계 ID): `stage_frontier_77__runtime_lifecycle_label_density_rebuild`

Opened by run(개방 실행): `frontier77A_stage_open_runtime_lifecycle_label_density_rebuild_v1`

Next run(다음 실행): `frontier77B_runtime_lifecycle_label_density_proxy_scout_v1`

Updated(갱신): 2026-06-17T06:53:14Z

## Hypothesis(가설)

Runtime lifecycle-native labels(런타임 생명주기 기본 라벨)가 independent signal labels(독립 신호 라벨)보다 US100 M5에서 tradeable density(거래 가능한 밀도)와 PF/DD(수익 팩터/손실폭)를 같이 보존할 수 있는지 본다.

Action(행동): forward OHLC path(미래 OHLC 경로), first-touch TP/SL(최초접촉 손절/익절), MFE/MAE(최대 유리/불리 이동), single-position occupancy(단일 포지션 점유), session/regime(세션/장세)을 처음부터 label/target/trade-shape(라벨/목표/거래 형태)에 넣는다.

Effect(효과): F76에서 생긴 independent proxy overcount(독립 프록시 과대계산)를 프록시 단계에서 줄인다.

## Broad Rotation(넓은 회전)

- feature set(피처 묶음): 빼기, 교체, 재조합
- label/target(라벨/목표): 경로 결과, 최초접촉, 위험 효용
- model family(모델 계열): linear/logistic, tree boosting, extra trees, small NN if available
- trade shape(거래 형태): 진입/청산/보유시간/롱숏 구조
- risk logic(위험 로직): SL/TP, MAE gate, DD guard, daily loss guard
- regime/session split(장세/세션 분할): cash open/mid/late, volatility/trend/chop

## Gates(게이트)

Scout clue(탐색 단서): validation and OOS net>0 or PF>=1.15, DD<=15%, lifecycle trades/day>=1.0, trade_count>=60 per split, and fragility recorded.

Meaningful signal(의미 신호): validation+OOS net>0, PF>=1.30, DD<=10%, lifecycle trades/day>=2.0, trade_count>=80 per split, and single-position compression recorded.

Completion-like reference(완성 유사 참조): reference only: PF>=2.0, DD<=10%, 5<=trades/day<=10, smooth equity proxy true. This is reference only(참조 전용) until final completion review(최종 완성 검토).

## Runtime Rule(런타임 규칙)

F77 closeout(마감) 전에는 MT5 Runtime Probe(MT5 런타임 탐침) 또는 true logic impossibility(진짜 로직 불가능)를 기록해야 한다.

## Claim Boundary(주장 경계)

`stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

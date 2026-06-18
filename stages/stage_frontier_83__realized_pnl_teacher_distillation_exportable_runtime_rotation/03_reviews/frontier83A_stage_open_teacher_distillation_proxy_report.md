# F83A Stage Open Teacher Distillation Proxy(F83A 단계 개방 교사 증류 프록시)

- run id(실행 ID): `frontier83A_stage_open_realized_pnl_teacher_distillation_exportable_runtime_rotation_v1`
- parent run(부모 실행): `frontier82H_capped_repair_closeout_or_f83_rotation_decision_v1`
- status(상태): `f83a_exportable_teacher_seed_positive_low_density_mt5_probe_required_no_authority`
- judgment(판정): `exportable_teacher_distillation_seed_found_but_one_sided_density_gap_requires_mt5_probe_and_two_sided_expansion_no_authority`
- next run(다음 실행): `frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1`
- claim boundary(주장 경계): `executed_trade_teacher_proxy_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Plain Meaning(쉬운 의미)

Action(행동): F82에서 실제 MT5 runtime(런타임)이 체결한 거래의 profit/loss(손익)를 teacher label(교사 라벨)로 삼아, ONNX(온엑스)로 내보낼 수 있는 모델을 학습했다.

Effect(효과): F82G처럼 “좋아 보이지만 내보낼 수 없는 사후 필터”에 머물지 않고, 다음 F83B MT5 Strategy Tester(전략 테스터) probe(탐침)에 넘길 수 있는 exportable seed(내보내기 가능 씨앗)가 있는지 확인했다.

## Experiment Design(실험 설계)

- hypothesis(가설): runtime-realized PnL teacher labels(런타임 실현 손익 교사 라벨)을 exportable model family(내보내기 가능 모델 계열)에 증류하면 positive low-density MT5-probe seed(양수 저밀도 MT5 탐침 씨앗)를 만들 수 있다.
- decision use(결정 용도): F83B에서 MT5 runtime materialization(MT5 런타임 물질화)을 실행할 후보가 있는지 결정한다.
- comparison baseline(비교 기준): F82C unfiltered runtime(무필터 런타임)과 F82G nonexportable diagnostic seed(내보내기 불가 진단 씨앗).
- changed variables(변경 변수): model family(모델 계열), exportability(내보내기 가능성), ONNX parity(온엑스 동등성).
- fixed variables(고정 변수): F82C feature rows(피처 행), F82F realized trade PnL(실현 거래 손익), validation->OOS time split(검증->표본외 시간 분할).
- invalid conditions(무효 조건): source file missing(원천 파일 누락), label/feature mismatch(라벨/피처 불일치), ONNX export/parity failure(온엑스 내보내기/동등성 실패).

## Data Integrity(데이터 무결성)

- data source(데이터 원천): `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/02_runs/frontier82G_mt5_realized_label_rebuild_v1/f82g_mt5_realized_label_dataset.csv`, `stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/02_runs/frontier82C_mt5_runtime_materialization_v1/features/f82c_runtime_f82b_07295_features.csv`
- time axis(시간축): F82C/F82F open_time(진입 시간)과 bar_time_server(서버 봉 시간)를 entry_key(진입 키)로 맞춘 executed-trade dataset(실행 거래 데이터셋).
- sample scope(표본 범위): validation rows(검증 행) `1962`, OOS rows(표본외 행) `1338`.
- feature-label boundary(피처/라벨 경계): features(피처)는 entry-known closed-bar inputs(진입 시점에 아는 닫힌 봉 입력), label(라벨)은 post-trade realized PnL(거래 후 실현 손익)이다.
- leakage risk(누수 위험): teacher model(교사 모델)은 validation realized trades(검증 실현 거래)에서 배웠으므로, F83A result(결과)는 exploratory proxy(탐색 프록시)로만 해석한다.

## Best Exportable Seed(최선 내보내기 가능 씨앗)

- candidate(후보): `f83a_0019`
- model(모델): `decision_tree_d4_balanced`
- threshold(임계값): `validation_probability_quantile_0.9` / `0.6326362193616636`
- ONNX parity max diff(온엑스 동등성 최대 차이): `2.970373558230932e-08`
- OOS net/PF/DD/trades/day(표본외 순손익/수익 팩터/손실폭/일 거래): `24.019999999999996/1.3314932376483577/2.043823928640711/137/0.7098445595854922`
- win rate/payoff/expectancy(승률/손익비/기대값): `0.45255474452554745/1.6106773036068842/0.17532846715328465`
- time under water/max consecutive loss(회복 전 체류/최대 연속 손실): `113/10`
- long/short breakdown(롱/숏 분해): `validation_long=256;validation_short=0;oos_long=137;oos_short=0`

## Judgment(판정)

F83A found positive exportable teacher seeds(F83A는 양수 내보내기 가능 교사 씨앗을 찾음): `6`.

MT5 probe candidate count(MT5 탐침 후보 수): `2`.

Final-like reference count(최종형 참고 수): `0`.

This is not runtime authority(런타임 권위 아님). Plainly, the model can be exported and its ONNX output matches Python on a sample, but MT5 Strategy Tester(전략 테스터)가 아직 새 F83 model(모델)을 직접 돌린 것은 아니다.

## Next Action(다음 행동)

`frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1` should materialize the best exportable teacher overlay(최선 내보내기 가능 교사 덧씌움)를 MT5 Strategy Tester(전략 테스터)로 실행한다. The two-sided gap(양방향 간극)은 F83 lifecycle(F83 생명주기) 안에서 별도 expansion(확장)으로 남긴다.

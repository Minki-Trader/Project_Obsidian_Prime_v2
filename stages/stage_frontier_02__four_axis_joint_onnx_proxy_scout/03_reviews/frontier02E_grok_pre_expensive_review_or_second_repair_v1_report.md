# frontier02E Frozen 02C Decision-Layer Diagnostic Report(전선02E 고정 02C 결정층 진단 보고)

- run_id(실행 ID): `frontier02E_grok_pre_expensive_review_or_second_repair_v1`
- status(상태): `completed_no_go_decision_layer_diagnostic_no_authority(결정층 진단 완료, 진행 조건 없음, 권위 없음)`
- anchor(앵커): `frontier02c_logreg_teacher__trend_follow_joint__mid_cash__both__q70__cd6__p34__m0__cd6`
- decision_rows(결정 행): `720`
- go_rule_rows(진행 조건 행): `0`
- next_run(다음 실행): `frontier02F_stage_closeout_preserved_clue_negative_memory_v1`

## Boundary(경계)

이번 실행(run, 실행)은 Grok pre-expensive review(비싼 검증 전 그록 검토)를 로컬 검증(local verification, 로컬 검증)한 뒤, frontier02C(전선02C) 고정 확률 출력(probability output, 확률 출력)만 사용한 decision-layer diagnostic(결정층 진단)입니다. 새 학습(retrain, 재학습), 새 ONNX(온엑스), WFO(워크포워드), MT5 runtime validation(MT5 런타임 검증)는 없습니다.

## Grok Advice Classification(그록 조언 분류)

- accepted(수용): frozen 02C decision-layer diagnostic(고정 02C 결정층 진단), no WFO/MT5 yet(WFO/MT5 아직 금지)
- rejected(거절): `All 14 frontier02D repair observation rows are below frontier02C on both PF and density(14개 수리 관찰 행 모두 PF와 밀도에서 C보다 낮다는 주장)`
- final Codex direction(최종 Codex 방향): `prepare_stage_closeout`

## Anchor vs Repair(앵커와 수리 비교)

- frontier02C validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.2034` / `4.29508/day` / `9.88436%`
- frontier02C OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `1.05433` / `5.03053/day` / `10.3356%`
- frontier02D validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `1.10035` / `3.19126/day` / `8.32627%`
- frontier02D OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `0.995483` / `3.48092/day` / `9.4608%`

## Best Diagnostic Rank(진단 순위 1위)

- candidate_id(후보 ID): `f02e_raw_prob__p30__m0__cd6`
- score_mode(점수 방식): `raw_probability`
- threshold/margin/cooldown(임계값/마진/쿨다운): `0.3` / `0` / `6`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `0.236314` / `1.2034` / `4.29508/day` / `9.88436%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `0.0464936` / `1.05433` / `5.03053/day` / `10.3356%`
- joint_pass_count(동시 통과 수): validation(검증) `1`, OOS(표본외) `1`

## Go/No-Go Read(진행/중단 판독)

Go rule(진행 규칙)은 OOS PF(표본외 수익 팩터) `>=1.2`, density(밀도) `5-10/day`, OOS DD pass(표본외 손실폭 통과), OOS net(표본외 순수익) `>0`입니다. 이번 진단의 go_rule_rows(진행 조건 행)는 `0`개입니다.

Effect(효과): `frontier02C는 preserved clue(보존 단서), frontier02D/02E는 negative memory(부정 기억)로 stage closeout(단계 마감)을 준비하는 쪽이 맞습니다.`

## Loss Attribution(손실 귀속)

Worst OOS buckets(표본외 최악 버킷): `[{"bucket_type": "atr_ratio_bucket", "bucket_value": "(1.14, 1.389]", "trade_count": 219, "net_profit": -0.08989226544500001, "profit_factor": 0.7478751829596498}, {"bucket_type": "vix_bucket", "bucket_value": "(-0.973, 0.954]", "trade_count": 219, "net_profit": -0.06961169558799998, "profit_factor": 0.7653731349705497}, {"bucket_type": "confidence_decile", "bucket_value": "(0.806, 0.873]", "trade_count": 65, "net_profit": -0.019085382858999998, "profit_factor": 0.8028594470620678}, {"bucket_type": "confidence_decile", "bucket_value": "(0.55, 0.612]", "trade_count": 66, "net_profit": -0.016831022819999993, "profit_factor": 0.8508294041568644}, {"bucket_type": "confidence_decile", "bucket_value": "(0.612, 0.674]", "trade_count": 66, "net_profit": -0.010241973490000002, "profit_factor": 0.8543680781153751}]`

## Local Verification(로컬 검증)

- KPI parity(KPI 숫자 일치): frontier02C OOS net `0.0464936`, frontier02D OOS net `-0.00281852`
- Grok degradation claim(그록 열화 주장): `reject_overbroad_degradation_claim`
- replay rows(재생 행): C `46650`, D `46650`
- decision rows(결정 행): C `576`, D `576`

## Claim Boundary(주장 경계)

Allowed claim(허용 주장): Grok review captured(그록 검토 기록), frozen 02C diagnostic completed(고정 02C 진단 완료), no-go/go-rule diagnostic read(진행/중단 진단 판독).

Forbidden claim(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), selected candidate(선택 후보).

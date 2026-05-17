# Stage62 KPI Margin Research Plan(62단계 KPI 여유 폭 연구 계획)

## Hypothesis(가설)

`s59ar_v41_sd8_h3` can be pushed toward or beyond legacy 34D(레거시 34D) KPI(핵심 성과 지표) only if v2-native(브이투 고유) research improves trade_shape(거래 형태), state/context gating(상태/문맥 제한), lifecycle(생명주기), and risk/bracket(위험/브래킷) together. Legacy 34D(레거시 34D) is a target surface(목표 표면), not a method to copy(복사할 방법).

## Decision Use(판정 용도)

The result may decide whether Stage62(62단계) can move into a v2-native 34D-target batch(브이투 고유 34D 목표 묶음), needs a new state/context branch(상태/문맥 분기), or should preserve the current Stage61 package(61단계 패키지) as a reference surface(참고 표면) while opening a stronger model branch(모델 분기).

Effect(효과): 좋은 결과가 나와도 operating claim(운영 주장)이 아니라 next research handoff(다음 연구 인계)만 만든다.

## Comparison Baseline(비교 기준)

- adapter(어댑터): `s59ar_v41_sd8_h3`
- validation(검증): net(순손익) `426.22`, PF(수익 팩터) `1.17`, drawdown(손실폭) `15.36%`
- OOS(표본외): net(순손익) `490.24`, PF(수익 팩터) `1.29`, drawdown(손실폭) `17.96%`
- weak point(약점): validation mid PF(검증 중간 PF) `1.1007`
- Tier B status(Tier B 상태): `disabled_due_run50BR_fallback_only_damage`
- legacy 34D latest target(레거시 34D 최신 목표): net(순손익) `987.60`, PF(수익 팩터) `1.583157`, max_dd_pct(최대 손실률) `12.909136`, trade_count(거래 수) `404`, expectancy(기대값) `2.444554`
- legacy 34D extended bridge target(레거시 34D 확장 브리지 목표): net(순손익) `2950.79`, PF(수익 팩터) `1.302494`, max_dd_pct(최대 손실률) `18.760867`, trade_count(거래 수) `1134`

## Control Variables(고정 변수)

- symbol/timeframe(종목/시간대): FPMarkets `US100` `M5`
- split contract(분할 계약): Stage60(60단계) validation/OOS(검증/표본외)
- model risk cap(모델 위험 상한): at or below 5%(5% 이하)
- ATR bracket(ATR 브래킷): must remain present(반드시 유지)
- ONNX/MT5 runtime boundary(ONNX/MT5 런타임 경계): no runtime authority(런타임 권위 없음)

## Changed Variables(변경 변수)

- same-direction cooldown(동일 방향 쿨다운) pressure around current sd8(현재 sd8 주변)
- hold-time/lifecycle(보유 시간/생명주기) around h3(현재 h3 주변), including 34D-like hold-shape target(34D 유사 보유 형태 목표) as lesson-only(교훈 전용)
- Tier B fallback eligibility(Tier B 대체 자격) as disabled, narrow fallback, or diagnostic fallback(비활성, 좁은 대체, 진단 대체)
- risk bucket smoothing(위험 버킷 완화) only if risk cap(위험 상한)이 유지된다
- ATR bracket multiplier neighborhood(ATR 브래킷 배수 주변) only if MFE/MAE(MFE/MAE) and drawdown(손실폭)을 같이 본다
- state/context filter(상태/문맥 필터) candidates inspired by 34D lesson(34D 교훈) but rebuilt in v2 feature space(브이투 피처 공간)

## Success Criteria(성공 기준)

- immediate Stage62 success(즉시 62단계 성공): at least one bounded variant(경계 변형)이 current Stage60/61 reference(현재 60/61단계 참조)보다 PF(수익 팩터), expectancy(기대값), drawdown(손실폭), or segment stability(구간 안정성) 중 두 가지 이상을 개선한다
- 34D-target progress(34D 목표 진전): validation/OOS PF(검증/표본외 PF)가 `1.30` 이상으로 이동하거나, validation mid PF(검증 중간 PF)가 `1.20` 이상으로 개선된다
- stretch target(확장 목표): comparable run(비교 가능 실행)에서 PF(수익 팩터) `1.58`, max_dd_pct(최대 손실률) `12.91` 이하, expectancy(기대값) `2.44` 이상에 접근하거나 초과한다
- validation/OOS net(검증/표본외 순손익) remain positive(양수)
- drawdown(손실폭) does not worsen materially(크게 악화하지 않음)
- cost-stressed expectancy(비용 스트레스 기대값) remains positive(양수)
- model risk%(모델 위험률), executed lot(실행 랏), ATR SL/TP(ATR 손절/익절)가 telemetered(텔레메트리 기록)된다

## Failure Criteria(실패 기준)

- validation or OOS(검증 또는 표본외) net(순손익)이 음수
- validation/OOS PF(검증/표본외 PF)가 `1.10` 아래
- validation mid PF(검증 중간 PF)가 더 약해짐
- drawdown(손실폭)이 크게 증가
- Tier B fallback(Tier B 대체)이 손실을 반복
- risk floor(위험 바닥)로 unintended risk inflation(의도치 않은 위험 팽창)이 발생

## Invalid Conditions(무효 조건)

- split(분할), cost stress(비용 스트레스), symbol(종목), timeframe(시간대)가 바뀌었는데 기록하지 않음
- ATR/risk telemetry(ATR/위험 텔레메트리)가 빠짐
- Tier B(Tier B) 기록을 missing_required(필수 누락) 없이 생략함
- final net(최종 순손익)만 보고 판정함
- legacy 34D(레거시 34D) 코드, 규칙, 승격 이력을 v2 result(브이투 결과)처럼 취급함

## Stop Conditions(중지 조건)

- one bounded batch(경계 묶음 하나)에서 improvement(개선), negative memory(부정 기억), or branch need(분기 필요)가 분명해지면 Stage62(62단계)를 닫는다
- repair need(수리 필요)가 넓어지면 Stage63(63단계) 또는 branch(분기)로 넘긴다
- deployment/live/operating claim(배포/실거래/운영 주장)이 필요해지면 out_of_scope(범위 밖)로 기록한다

## Evidence Plan(근거 계획)

Required outputs(필수 산출물):

- `kpi_margin_research_plan.md`
- `stage62_variant_queue.csv`
- `stage62_34d_target_kpi_gap.csv`
- `stage62_legacy_34d_target_gap.md`
- `stage62_kpi_margin_report.md`
- `stage62_segment_kpi_summary.csv`
- `stage62_risk_atr_telemetry.csv`
- `stage62_tier_b_diagnostic_summary.csv`
- `stage62_decision.md`

Effect(효과): Stage62(62단계)는 성능을 바꿔본 뒤, 한 단계가 끝나면 다음 단계/분기 결정을 명확히 남긴다.

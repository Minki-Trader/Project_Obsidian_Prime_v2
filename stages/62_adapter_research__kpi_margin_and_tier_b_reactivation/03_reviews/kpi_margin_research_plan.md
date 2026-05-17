# Stage62 KPI Margin Research Plan(62단계 KPI 여유 폭 연구 계획)

## Hypothesis(가설)

`s59ar_v41_sd8_h3` can be improved as a research adapter(연구 어댑터) if the weak validation mid segment(검증 중간 구간), drawdown(손실폭), and Tier B disabled(Tier B 비활성) boundary are treated as one KPI margin problem(KPI 여유 폭 문제), not as a final package failure(최종 패키지 실패).

## Decision Use(판정 용도)

The result may decide whether the Stage61 package(61단계 패키지) remains a reference surface(참고 표면), gets a stronger follow-up adapter(후속 강화 어댑터), or opens a separate Tier B repair branch(Tier B 수리 분기).

Effect(효과): 좋은 결과가 나와도 operating claim(운영 주장)이 아니라 next research handoff(다음 연구 인계)만 만든다.

## Comparison Baseline(비교 기준)

- adapter(어댑터): `s59ar_v41_sd8_h3`
- validation(검증): net(순손익) `426.22`, PF(수익 팩터) `1.17`, drawdown(손실폭) `15.36%`
- OOS(표본외): net(순손익) `490.24`, PF(수익 팩터) `1.29`, drawdown(손실폭) `17.96%`
- weak point(약점): validation mid PF(검증 중간 PF) `1.1007`
- Tier B status(Tier B 상태): `disabled_due_run50BR_fallback_only_damage`

## Control Variables(고정 변수)

- symbol/timeframe(종목/시간대): FPMarkets `US100` `M5`
- split contract(분할 계약): Stage60(60단계) validation/OOS(검증/표본외)
- model risk cap(모델 위험 상한): at or below 5%(5% 이하)
- ATR bracket(ATR 브래킷): must remain present(반드시 유지)
- ONNX/MT5 runtime boundary(ONNX/MT5 런타임 경계): no runtime authority(런타임 권위 없음)

## Changed Variables(변경 변수)

- same-direction cooldown(동일 방향 쿨다운) pressure around current sd8(현재 sd8 주변)
- hold-time/lifecycle(보유 시간/생명주기) around h3(현재 h3 주변)
- Tier B fallback eligibility(Tier B 대체 자격) as disabled, narrow fallback, or diagnostic fallback(비활성, 좁은 대체, 진단 대체)
- risk bucket smoothing(위험 버킷 완화) only if risk cap(위험 상한)이 유지된다
- ATR bracket multiplier neighborhood(ATR 브래킷 배수 주변) only if MFE/MAE(MFE/MAE) and drawdown(손실폭)을 같이 본다

## Success Criteria(성공 기준)

- validation PF(검증 PF) improves above `1.20` or validation mid PF(검증 중간 PF) improves clearly above `1.12`
- OOS PF(표본외 PF) stays at or above `1.20`
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

## Stop Conditions(중지 조건)

- one bounded batch(경계 묶음 하나)에서 improvement(개선), negative memory(부정 기억), or branch need(분기 필요)가 분명해지면 Stage62(62단계)를 닫는다
- repair need(수리 필요)가 넓어지면 Stage63(63단계) 또는 branch(분기)로 넘긴다
- deployment/live/operating claim(배포/실거래/운영 주장)이 필요해지면 out_of_scope(범위 밖)로 기록한다

## Evidence Plan(근거 계획)

Required outputs(필수 산출물):

- `kpi_margin_research_plan.md`
- `stage62_variant_queue.csv`
- `stage62_kpi_margin_report.md`
- `stage62_segment_kpi_summary.csv`
- `stage62_risk_atr_telemetry.csv`
- `stage62_tier_b_diagnostic_summary.csv`
- `stage62_decision.md`

Effect(효과): Stage62(62단계)는 성능을 바꿔본 뒤, 한 단계가 끝나면 다음 단계/분기 결정을 명확히 남긴다.

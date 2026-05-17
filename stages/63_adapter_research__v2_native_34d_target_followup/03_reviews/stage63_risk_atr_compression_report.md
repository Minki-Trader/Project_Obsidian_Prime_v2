# Stage63 Risk/ATR Compression Report(63단계 위험/ATR 압축 보고)

- run(실행): `run63A_stage63_risk_atr_drawdown_compression_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_adapter(원천 어댑터): `s62_v41_sd8_h5`
- variants(변형): `s63_h5_risk2_sl25_tp35, s63_h5_risk3_sl20_tp32, s63_h5_risk2_sl20_tp32`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_state_context_model_branch`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Legacy 34D(레거시 34D)는 code copy(코드 복사) 대상이 아니다. Effect(효과): Stage63(63단계)는 Stage62(62단계) hold5(5봉 보유) 개선을 출발점으로 두고, risk cap(위험 한도)과 ATR bracket(ATR 브래킷) 압축이 DD(손실률)를 줄이는지만 본다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s63_h5_risk2_sl25_tp35 | validation_is | 1.2000 | 285.44 | 12.38 | 0.6600 | -0.3832 |
| s63_h5_risk2_sl25_tp35 | oos | 1.3200 | 337.33 | 17.30 | 1.0600 | -0.2632 |
| s63_h5_risk3_sl20_tp32 | validation_is | 1.2000 | 587.44 | 18.69 | 1.3500 | -0.3832 |
| s63_h5_risk3_sl20_tp32 | oos | 1.1900 | 402.65 | 34.86 | 1.2600 | -0.3932 |
| s63_h5_risk2_sl20_tp32 | validation_is | 1.2100 | 363.40 | 12.68 | 0.8400 | -0.3732 |
| s63_h5_risk2_sl20_tp32 | oos | 1.2100 | 262.38 | 23.61 | 0.8200 | -0.3732 |

## Read(판독)

- best_variant(최선 변형): `s63_h5_risk3_sl20_tp32`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/63_adapter_research__v2_native_34d_target_followup/03_reviews/stage63_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/63_adapter_research__v2_native_34d_target_followup/03_reviews/stage63_risk_atr_telemetry.csv`
- tier_b_diagnostic(Tier B 진단): `stages/63_adapter_research__v2_native_34d_target_followup/03_reviews/stage63_tier_b_diagnostic_summary.csv`

## Interpretation(해석)

- `s63_h5_risk2_sl25_tp35`: validation DD(검증 손실률) 18.04% -> 12.38%, OOS DD(표본외 손실률) 24.97% -> 17.30%로 줄었다. Effect(효과): drawdown compression(손실률 압축)은 확인됐지만, validation net(검증 순손익) 474.42 -> 285.44와 OOS net(표본외 순손익) 587.35 -> 337.33으로 성과가 크게 줄어 34D KPI target(34D 핵심 성과 지표 목표)에는 부족하다.
- `s63_h5_risk3_sl20_tp32`: validation net(검증 순손익)은 587.44로 좋아졌지만 OOS PF(표본외 수익 팩터) 1.19와 OOS DD(표본외 손실률) 34.86%로 손상됐다. Effect(효과): ATR bracket tightening(ATR 브래킷 타이트닝)만으로는 OOS 안정성(표본외 안정성)을 만들지 못했다.
- `s63_h5_risk2_sl20_tp32`: validation DD(검증 손실률)는 12.68%로 개선됐지만 OOS PF(표본외 수익 팩터) 1.21, OOS DD(표본외 손실률) 23.61%, OOS mid segment(표본외 중간 구간) negative(음수)로 약하다. Effect(효과): risk/ATR compression(위험/ATR 압축) 조합도 34D급 KPI(핵심 성과 지표)로는 부족하다.

Stage63 decision(63단계 판정)은 `open_state_context_model_branch`다. Effect(효과): 다음 Stage64(64단계)는 같은 파라미터만 더 누르지 않고, state/context gating(상태/문맥 게이트)으로 early/mid weakness(초기/중간 약점)와 OOS drawdown(표본외 손실률)을 줄이는 경계 질문으로 넘어간다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).

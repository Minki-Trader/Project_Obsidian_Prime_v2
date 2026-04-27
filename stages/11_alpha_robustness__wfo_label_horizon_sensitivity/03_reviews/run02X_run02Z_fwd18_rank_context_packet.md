# RUN02X~RUN02Z fwd18 Rank Context Packet

## Subject(대상)

- packet_id(묶음 ID): `run02X_run02Z_fwd18_rank_context_packet_v1`
- stage(단계): `11_alpha_robustness__wfo_label_horizon_sensitivity`
- source run(원천 실행): `run02W_lgbm_fwd18_retrain_v1`
- boundary(경계): `structural_scout(구조 탐침)` + `runtime_probe(런타임 탐침)`, not alpha quality(알파 품질 아님)

효과(effect, 효과): RUN02W(실행 02W)의 fwd18-only retrain(fwd18 단독 재학습) 실패 뒤에, fwd18(90분) 자체가 죽었는지 아니면 rank/context(순위/문맥)로 살아나는지를 분리해서 본다.

## Results(결과)

| run(실행) | change(변경) | Python signal A/B/AB(파이썬 신호 A/B/합산) | validation(검증) | OOS(표본외) | judgment(판정) |
|---|---|---:|---:|---:|---|
| RUN02X(실행 02X) | direct rank threshold(직접 순위 임계값) | `327/164/491` | Tier A q96 hit(적중률) `0.25` | Tier A q96 hit(적중률) `0.15625` | negative structural scout(부정 구조 탐침) |
| RUN02Y(실행 02Y) | inverse rank threshold(역방향 순위 임계값) | `327/164/491` | Tier A q96 hit(적중률) `0.604167` | Tier A q96 hit(적중률) `0.34375` | mixed structural scout(혼합 구조 탐침) |
| RUN02Z(실행 02Z) | inverse rank + `di_spread_abs_lte8_adx_lte25` context(역방향 순위 + 문맥) | `20/9/29` | MT5 routed(라우팅) `386.06 / 7.25 / 9 trades(거래)` | MT5 routed(라우팅) `352.63 / 52.03 / 5 trades(거래)` | positive tiny-sample runtime_probe(작은 표본 긍정 런타임 탐침) |

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `foundation/pipelines/run_stage11_lgbm_rank_threshold_scout.py`
- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`, `foundation/mt5/include/ObsidianPrime/DecisionSurface.mqh`
- shared_contract(공유 계약): fwd18(90분) source model(원천 모델), rank threshold(순위 임계값), inverse signal flag(역방향 신호 플래그), Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체), hold(보유) `9`
- known_differences(알려진 차이): Tier A/Tier B component PnL(구성 손익)은 single routed account path(단일 라우팅 계좌 경로)에서 분리하지 않는다.
- parity_check(동등성 점검): MetaEditor compile(메타에디터 컴파일) `0 errors, 0 warnings(오류 0, 경고 0)`; strategy tester reports(전략 테스터 보고서) validation/OOS(검증/표본외) 둘 다 생성됨
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)`만 허용한다.

## Judgment(판정)

- result_subject(판정 대상): RUN02Z(실행 02Z) fwd18 inverse-rank DI/ADX context MT5 routed probe(fwd18 역방향 순위 DI/ADX 문맥 MT5 라우팅 탐침)
- evidence_available(있는 근거): Python tier records(파이썬 티어 기록), MT5 compile log(컴파일 로그), validation/OOS tester reports(검증/표본외 테스터 보고서), KPI record(KPI 기록), ledgers(장부)
- evidence_missing(부족한 근거): 거래 수가 validation(검증) `9`, OOS(표본외) `5`로 작고, adjacent context/rank stress test(인접 문맥/순위 압박 시험)가 없다.
- judgment_label(판정 라벨): `positive_tiny_sample_runtime_probe(작은 표본 긍정 런타임 탐침)`
- claim_boundary(주장 경계): 계속 팔 가치가 있다는 뜻이지, alpha quality(알파 품질), live readiness(실거래 준비), promotion_candidate(승격 후보), operating_promotion(운영 승격)이 아니다.
- next_condition(다음 조건): DI/ADX context(문맥)를 넓히거나 좁힌 변형, rank quantile(순위 분위수) 인접값, Tier A-only versus routed(Tier A 단독 대 라우팅) 확인에서 양수와 신호 밀도가 유지되는지 본다.

## Artifact Paths(산출물 경로)

- plan(계획): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/00_spec/run02X_run02Z_fwd18_rank_context_plan.md`
- RUN02Z manifest(실행 목록): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02Z_lgbm_fwd18_inverse_rank_context_v1/run_manifest.json`
- RUN02Z KPI(KPI 기록): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02Z_lgbm_fwd18_inverse_rank_context_v1/kpi_record.json`
- RUN02Z result summary(결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02Z_lgbm_fwd18_inverse_rank_context_v1/reports/result_summary.md`
- stage ledger(단계 장부): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/stage_run_ledger.csv`
- project ledger(프로젝트 장부): `docs/registers/alpha_run_ledger.csv`

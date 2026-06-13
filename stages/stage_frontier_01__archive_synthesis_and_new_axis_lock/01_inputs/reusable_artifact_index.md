# Reusable Artifact Index(재사용 산출물 색인)

이 문서는 다음 frontier stage(전선 단계)가 참조할 수 있는 reusable artifact(재사용 산출물)를 분류한다.

Action(행동): artifact path(산출물 경로), use(용도), claim boundary(주장 경계)를 연결한다.

Effect(효과): 새 ONNX(온엑스) 연구가 과거 파일을 쓰더라도 inheritance(상속)가 아니라 bounded reference(제한 참조)로만 쓰게 한다.

## Ledgers And Registers(장부와 등록부)

| artifact(산출물) | use(용도) | boundary(경계) |
|---|---|---|
| `docs/registers/run_registry.csv` | run identity(실행 정체성), stage linkage(단계 연결), report path(보고 경로) 확인 | source authority(원천 권위) for identity only(정체성 전용) |
| `docs/registers/alpha_run_ledger.csv` | Tier A/B/combined(Tier A/B/합산), KPI row(성과 행), judgment(판정) 조회 | measurement ledger(측정 장부); no inherited candidate(상속 후보 없음) |
| `docs/registers/idea_registry.md` | preserved clue(보존 단서), hypothesis memory(가설 기억) 조회 | idea memory(아이디어 기억); no baseline(기준선 없음) |
| `docs/registers/negative_result_register.md` | DNR(do-not-repeat, 반복 금지)와 reopen condition(재개 조건) 조회 | failure memory(실패 기억) |
| `docs/registers/artifact_registry.csv` | hashes(해시), runtime artifacts(런타임 산출물), package identity(패키지 정체성) 조회 | artifact identity(산출물 정체성); may contain local paths(로컬 경로 포함 가능) |

## Policy And Contracts(정책과 계약)

| artifact(산출물) | use(용도) | boundary(경계) |
|---|---|---|
| `docs/policies/frontier_governance.md` | `reference, not inheritance(참조이지 상속 아님)` 운영 규칙 | required governance(필수 운영 규칙) |
| `docs/policies/exploration_mandate.md` | exploration freedom(탐색 자유), progressive hardening(점진적 경화) | exploration policy(탐색 정책) |
| `docs/policies/kpi_measurement_standard.md` | KPI measurement standard(KPI 측정 기준) | used when trading KPI(거래 KPI) exists |
| `docs/policies/run_result_management.md` | reviewed run(검토된 실행) 조건과 ledger grain(장부 입도) | used when new run(새 실행) exists |
| `docs/policies/result_judgment_policy.md` | valid/invalid/blocked/preserved clue(유효/무효/차단/보존 단서) 판정 | claim boundary(주장 경계) |
| `docs/contracts/feature_calculation_spec_fpmarkets_v2.md` | feature meaning(피처 의미) and source calculation(원천 계산) | feature contract(피처 계약) |
| `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md` | EA input order(EA 입력 순서) and runtime handoff(런타임 인계) | runtime parity input(런타임 동등성 입력) |
| `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md` | bundle/model/hash identity(번들/모델/해시 정체성) | runtime authority precondition(런타임 권위 전제 조건) |

## Stage Reports(단계 보고서)

| artifact(산출물) | use(용도) | boundary(경계) |
|---|---|---|
| `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364HS_stage364_closeout_no_next_stage.md` | Stage364(364단계) final negative memory(최종 부정 기억) | no next-stage inheritance(다음 단계 상속 없음) |
| `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364HR_single_source_probability_bin_veto_trade_quality_density_repair_scout.md` | strict_joint_pass_count(엄격 동시 통과 수) `0` and preserved clue(보존 단서) | proxy scout only(프록시 탐색 전용) |
| `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364HQ_single_source_probability_bin_veto_mt5_runtime_probe_review.md` | MT5 positive net but PF/DD/density failure(MT5 양수 순수익이나 PF/DD/밀도 실패) | runtime observation(런타임 관찰) not authority(권위 아님) |
| `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364HL_probability_bin_veto_mt5_runtime_probe_review.md` | positive runtime clue(긍정 런타임 단서) with density/cost/route gaps(밀도/비용/라우트 공백) | repair clue(수리 단서) only |
| `stages/267_onnx_research_packet__proxy_ablation_candidate_distinguishability/03_reviews/` | candidate distinguishability(후보 구분성) failure memory(실패 기억) | do not inherit candidates(후보 상속 금지) |
| `stages/40_feature_structure__candle_morphology_signal_quality_scout/03_reviews/` | candle morphology(캔들 형태) clue(단서) and thin count warning(얇은 수 경고) | context clue(문맥 단서) only |

## Runtime And Pipeline Surfaces(런타임과 파이프라인 표면)

| artifact(산출물) | use(용도) | boundary(경계) |
|---|---|---|
| `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` | thin EA entrypoint(얇은 EA 진입점) | do not clone for run variants(실행 변형 복제 금지) |
| `foundation/mt5/include/ObsidianPrime/` | shared MT5 modules(공유 MT5 모듈) | module hash required(모듈 해시 필요) |
| `foundation/mt5/runtime_artifacts.py` | runtime artifact helpers(런타임 산출물 도우미) | local verification required(로컬 검증 필요) |
| `foundation/pipelines/` | shared orchestration(공유 실행 지휘) | not hidden source of truth(숨은 진실 원천 아님) |
| `stage_pipelines/` | stage-local adapter(단계 전용 어댑터) | no long-term model/feature ownership(장기 모델/피처 소유 금지) |

## Reuse Rule(재사용 규칙)

Reusable artifact(재사용 산출물)를 쓰는 다음 작업은 아래를 기록한다.

- artifact path(산출물 경로)
- artifact hash(산출물 해시) when available(가능할 때)
- source run/stage(원천 실행/단계)
- allowed import type(허용 반입 유형): preserved clue(보존 단서), negative memory(부정 기억), reusable artifact(재사용 산출물), do-not-repeat note(반복 금지 메모)
- forbidden import check(금지 반입 확인): winner(승자), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)

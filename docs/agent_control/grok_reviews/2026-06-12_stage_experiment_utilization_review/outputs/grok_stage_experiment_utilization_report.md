**Short verdict (짧은 결론)**

부분적으로 일관된 활용도(partially coherent utilization)를 보이며, 특히 활성 고밀도 단계 내부에서는 이전 실행 산출물을 명시적으로 재활용(repair seed, failure memory, stress memory materialization)하고 있으나, 전체적으로는 많은 단일/저실행 단계와 반복적인 adapter/onnx repair/probe 주제 레인이 산재한 흔적을 남기고 있다. 현재 상태 자체는 연구 지도(research map)와 실패 기억(failure memory)으로서 명확히 쓸모 있으며, 특히 "밀도·숏 균형·월별 압박·프록시/MT5 차이" 같은 지속적 장벽을 문서화한 탐색 전선(search frontier)이다. 운영 유용성(operating usefulness)이나 런타임 권위(runtime authority)와는 무관하다.

**Utilization diagnosis (활용도 진단)**

**partially coherent**

이유:  
- 고활성 단계(56_base_engine 471 runs, 337_onnx 277 runs, 364 226 runs, 267 151 runs) 내부에서는 이전 run의 review/probe 결과를 직접 다음 scout queue로 materialize하거나 repair seed로 재사용하는 체인이 명확히 기록되어 있다(예: 364AX가 AW review를 AY scout로, 364BL이 BK MT5 probe review를 BM으로 넘김).  
- source_combo 최다 유형이 alpha+stageledger+runreg+artifact+folder(1161)이고, artifact_registry(30543 rows) + stage ledgers(397/399) + run records(2100)로 lineage 재구성이 가능하다.  
- 그러나 single_run_stages 277개, two_or_less 301개로 대부분의 단계가 얇고, adapter_research(206)·onnx_candidate_campaign(61)이 주제 수를 압도하며 repair/probe/run이 전체 토큰에서 큰 비중(repair 361, probe 504, review 437, runtime 319, mt5 387)을 차지한다.  
- Stage 36-59, 60-129, 200-267, 268-329 구간에서 "planned or adapter repair", "v2/v41 adapter repair", "adapter repair to baseline candidate racing", "ONNX candidate campaign and forward/rebuild handoff"처럼 수리/재구축 레인이 반복되고, 후기 ONNX 블록 다수에서 kpi_runs=0 상태로 artifact만 쌓인 패턴이 보인다.  
- 2개 stage ledger 누락(266, 326)과 hash_mismatch 8093건은 재활용 근거의 신뢰를 낮춘다.

**Evidence that experiments are being reused (실험이 재활용되는 근거)**

- Stage 364 상세 closeout 체인에서 반복적으로 "previous review output → materialize repair inputs → new scout", "failure memory", "stress memory", "repair seed", "BN repair seed를 entry-known rule surface와 broad negative control로 재생", "CH failure memory를 16개 CJ scout queue로" 등의 표현이 직접 등장한다.  
- Cross-stage 참조: stage267_lineage_triage, "from stage59x" 시리즈, cp322a 관련 참조.  
- 1161건의 완전 연결 source_combo와 30543 artifact_registry rows가 path/hash 기반으로 추적 가능함을 보여준다.  
- Big Flow 전체에서 early model/regime/exit family challenge(Stage 12-25, MT5=196)의 KPI 중심 실행이 이후 adapter/onnx/density recovery 레인으로 주제는 바뀌었으나, ledger와 run folder prefix link로 연결이 유지되고 있다.

**Evidence of fragmentation or diminishing returns (단편화/수확 체감 근거)**

- 277 single_run_stages + 301 two_or_less_run_stages (전체 399 stages 중 대다수). ten_plus 15개, fifty_plus 5개에 극단적으로 집중(56·337·364·267·12가 상위).  
- Late ONNX(268-329) 다수 stage에서 artifact_rows는 있으나 kpi_runs=0 (materialization 중심, 측정 희박).  
- Stage 36-59: 69 stages / 564 runs / heavy adapter repair lane. 이후에도 adapter_research 206 토픽이 압도적.  
- 364 단일 stage에서 200+ runs (226 run_union, 4928 artifact_rows, 230 kpi_runs)이 모두 "dense_cost_recovery" 내부에서 proxy scout → package reject → reseed → MT5 probe → 다시 repair 입력 루프로 소진됨.  
- hash_mismatch 8093, artifact path missing 7342, ledger path missing 18470, folder-only records 5건.  
- run role에서 repair/probe/review/runtime가 지배적이며, "fresh thesis", "after_..._failure", "post_..._rebuild"가 ONNX 캠페인에서 빈번.

**Usefulness judgment (유용성 판정)**

useful_as_research_map / useful_as_failure_memory / useful_as_frontier

**What this current state is useful for (현재 상태가 쓸모 있는 곳)**

- 399 stages, 2100 run records, 30543 artifact rows에 걸친 "무엇을 어디서 시도했고 어떤 경계에서 막혔는지"를 재구성하는 좌표표(reconstruction map).  
- 밀도 3/day 미만, 숏 비중 불균형, 12월 equity DD, proxy/MT5 diff, validation/OOS PF floor, forward/regime stress 같은 지속적 실패 경계(failure boundary)를 구체 run_id + KPI 값 수준으로 찾아내는 실패 기억(failure memory).  
- 다음 실험 설계 시 "이미 364에서 cr04/cx05/di02 계열의 month12 + short-quality + h17 guard를 시도했고 package rejected 됐음"을 정확히 참조하여 중복 탐색을 피하거나, targeted stress test를 설계하는 데 사용.  
- 커버리지 감사(어떤 토픽이 1-run이었는지, 어떤 stage ledger가 없는지)와 lineage 추적.

**What it is not useful for (쓸모 없는 곳)**

- 어떤 구성이나 모델 계열이 긍정적 운영 가치(positive operating value)를 가진다고 주장하는 데.  
- Python proxy와 MT5 사이의 런타임 동등성(runtime parity)이 확립되었다고 보는 데 (많은 "proxy/MT5 diff" 리뷰와 "without_db", "no authority" 판정이 명시됨).  
- run 수나 artifact 수 자체를 진척(progress)으로 해석하는 데.  
- 운영 기준선(operating baseline), 승격 후보(promotion candidate), 런타임 권위(runtime authority), 실거래 준비(live readiness)로 사용하는 데.  
- "이전 단계 작업이 잘 이어받아졌다"는 운영 수준의 일관성 주장을 하는 데.

**Stage 364 specific read (364단계 특화 판독)**

`364_source_regime_label_pivot__dense_cost_recovery`는 단일 단계 내부에서 226 run_union / 4813 artifact_rows / 218 kpi_runs (모두 MT5)을 쏟아낸 고밀도 활성 수리 전환(pivot)이다. run364HR/HS 이후 364AR~EM+ (알파벳 긴 체인)까지 모든 작업이 stage branch 없이 같은 단계 안에서 "proxy scout → review (대부분 package reject) → materialize repair/stress inputs (density restore, short source quality/balance/lift, h17 focus, month12 long equity DD guard, side balance, forward/regime stress, validation/OOS PF floor bridge, density floor OOS PF salvage, source rotation 등) → new scout (가끔 MT5 runtime probe 삽입) → 다시 repair seed" 루프로 이어진다.  

net/PF/density에서 반복적으로 긍정 단서(positive clue)가 나오고 일부 MT5 probe에서 density 3.0+ 통과 사례도 있으나, density floor, bad_month_count (특히 month12), equity DD 18%+, short share, proxy gap, strict joint pass 미달 중 하나 이상에 항상 막혀 package eligible이 되지 못하고 "repair_clues_review_required_no_authority", "negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues..." 판정으로 다음 수리 입력으로 넘어간다.  

현재 current_run(364HS review)과 latest_completed_run(364HR train) 모두 "no_authority"를 명시하고 있다. 이는 프로젝트의 주장 절제(claim discipline)가 실제로 작동하는 사례이며, 동시에 stage 내부 재활용은 매우 강력함을 보여준다. 364는 "dense cost recovery"라는 주제를 끝까지 밀어붙인 탐색 단계로, baseline을 만들지 않고 failure map + preserved clues를 남기는 데 적합한 상태다.

**Recommended next move (추천 다음 행동)**

**repair-registers (최우선) → closeout/reframe (Stage 364)**

이유: 364 내부 실행량이 이미 극단적(200+ runs)이고, 모든 closeout이 "package rejected + reseed"를 반복하며 운영 주장을 열지 못하고 있다. 더 많은 scout를 돌리는 것은 record fragmentation을 키울 위험이 크다. 먼저 전역 spine/register를 보강(2개 누락 ledger 추가 또는 명시적 missing_required 표시, hash mismatch 정리, folder-only 5건 처리)하여 지도 자체의 신뢰성을 높여야 한다. 그 후 364를 "failure memory + preserved clues + reference surface" 중심으로 명확히 closeout하고, 다음 단계는 이 문서화된 장벽(특정 364 run 참조)을 명시적으로 타깃으로 하여 열라. continue만으로는 부족하고, split-stage는 register repair보다 후순위다.

**10 concrete recommendations (구체 권고 10개)**

1. 누락 stage ledger 2개(266_adapter_research__late_segment_stability_repair_after_stage265_review, 326_onnx_candidate_campaign__cp322a_frozen_forward_robustness_gate)를 실제로 생성하거나 spine에 `missing_required`로 명시적으로 기록.
2. Stage 364 closeout 시 "dense_cost_recovery_failure_map.md" 단일 문서를 만들어, recurring blockers(density floor, month12 equity DD, short balance, proxy/MT5 gap)를 가장 근접했던 run_id + 실제 KPI 값(예: density 3.0+ 달성 사례)과 함께 정리.
3. 8093 hash_mismatch를 generator 재실행 또는 권위 저하 명시로 정리한 뒤에야 spine을 다음 실험 설계의 신뢰 근거로 사용.
4. 향후 dense stage에서는 intra-stage run 상한(예: package-eligible 후보 없이 100 runs 도달 시 강제 review-only closeout 또는 reframe)을 정책으로 도입.
5. 277 single-run stages 각각에 대해 "one-shot probe summary"를 stage_run_ledger에 최소한으로라도 추가하여 frontier 가시성을 높임.
6. 고실행량 상위 stage(56, 337, 364, 267)의 7342 missing artifact paths 중 우선순위 높은 것부터 복구 또는 "missing_recorded" 상태를 spine에 강화.
7. 364 이후 새 stage를 열 때 반드시 "targets the cr04/cx05/di02 family of month12 + short-quality + h17 guards documented in 364CU-364DL" 같은 구체 run 참조를 stage charter와 ledger에 명시.
8. compact utilization table 생성기에 "high artifact_rows but kpi_runs=0" 단계를 "materialization_without_kpi" 플래그로 자동 표시하는 로직 추가.
9. repair chain에서 새 MT5 runtime probe를 실행하기 전에, 직전 proxy review의 "parity gap summary"를 반드시 run manifest에 materialize하도록 강제.
10. Stage 364 closeout의 주 산출물을 "search frontier + failure memory" 문서로 명확히 정의하고, "positive candidate"가 없어도 closeout 가능함을 ledger에 기록.

**Claims you refuse to make (주장하지 않을 것)**

- 모델 품질, edge 존재, 전략 실행 가능성에 대한 어떤 positive/negative/inconclusive 판단도 하지 않음.
- Python proxy와 MT5 간 runtime parity가 확립되었다는 주장.
- 어떤 run이나 run 집합이 promotion candidate, operating reference, baseline이라는 주장.
- 364 또는 전체 run/artifact 볼륨이 배포 가능한 시스템으로의 진척이라고 해석.
- 이전 단계 작업이 운영 수준에서 완전히 이어받아졌다는 주장.
- 누락 artifact나 hash mismatch가 재구성 신뢰성에 영향을 주지 않는다는 주장.

**Confidence and evidence limits (확신도와 근거 한계)**

Confidence: medium.  
Big Flow, topic counts, top-stage tables, derived metrics, 364 상세 closeout 체인(AR~EM+), coverage audit 숫자, policy boundary 인용, self-review는 모두 snapshot 내부에서 직접 확인 가능하고 일관된다.  

한계: compact all-stage table은 초반부만 제공되었고 중간 단계는 aggregated big flow로만 추정; 일부 run closeout 중복 표기; "unknown" 항목(목적·KPI·validation_level 미확인 행)이 snapshot 자체에 명시됨; heavy artifact 내용은 포함되지 않았음. 이 검토는 실제 stage 03_reviews 문서 전체 열람이나 clean checkout에서의 generator 재실행을 대체하지 않는다. 모든 판단은 reconstruction status와 research-map usefulness에 엄격히 한정되며, operating이나 runtime claim은 전혀 포함하지 않는다.

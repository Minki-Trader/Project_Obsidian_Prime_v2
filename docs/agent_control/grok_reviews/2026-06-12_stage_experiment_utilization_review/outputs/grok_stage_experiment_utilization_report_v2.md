**Short verdict(짧은 결론)**

현재 상태는 상세한 재구성 지도(reconstruction map)이자 실패 기억(failure memory)과 탐색 전선(search frontier)으로서 연구 유용성이 있다. 그러나 단계별 실험 활용도는 전체적으로 단편적(fragmented)이며, Stage 12~364 흐름은 일관된 연구 프로그램이라기보다는 장기간의 repair/probe(수리/탐침) 루프가 지배적인 흔적이다. Stage 364 자체는 밀도 높은 활동을 보였으나 strict joint pass(엄격 공동 통과) 없이 repair clues(수리 단서)만 남긴 negative_proxy 결과로 끝나, 현재 상태는 운영 유용성(operating usefulness)이나 런타임 권위(runtime authority)와는 무관한 연구 산출물(research artifact)이다.

**Utilization diagnosis(활용도 진단): fragmented**

이유: 399개 단계 중 277개가 single-run stages(단일 실행 단계), 301개가 two_or_less_run_stages(2개 이하 실행 단계)다. adapter_research(206)와 adapter_repair(45), onnx_candidate_campaign(61)이 압도적으로 많고, 60~266 구간에서 "repair → bounded_followup_review / new_model_branch_from_..." 형태의 1-run 체인이 길게 이어진다. Early(12-25) 모델 계열 도전 구간은 실행 밀도가 상대적으로 높았으나(14단계 200 runs, 대부분 MT5 + KPI), 이후 대부분의 단계는 좁은 후속 수리나 구체화(materialization) 중심으로 쪼개졌다. 소수 중량 단계(56_base_engine 471 runs, 267 151 runs, 337 277 runs, 364 226 runs)가 실행과 산출물을 독식하고, 나머지 수백 단계는 얇다. 재활용 흔적은 존재하지만, "이전 실험을 깊게 축적·재사용"하는 구조라기보다는 실패 후 좁은 수리 루프를 반복하는 패턴이 강하다.

**Evidence that experiments are being reused(실험이 재활용되는 근거)**

- 단계 이름에 "after_stageXXX", "from_stageXXX", "post_...", "survivor_..." 같은 lineage(계보) 표시가 다수 존재.
- 364에서 source_stage_id(363)와 source_run_id를 명시하고, failure_memory(실패 기억)로 "Stage363C의 lower-floor/rank micro-tuning 반복 금지"를 기록.
- overfit_guard, runtime_parity, runtime_trade_lifecycle, cash_open 계열에서 이전 캠페인(ONNX, adapter)의 handoff(인계)와 probe/review 연결.
- 267 baseline_candidate_racing, 337 cost_buffer_direction_curve_rebuild처럼 일부 단계에서 다수 실행(151~277 runs)과 대량 artifact(2966~7424 rows)로 후보를 집중 경쟁/재구축.
- run source combinations에서 alpha+stageledger+runreg+artifact+folder 조합이 1161건으로 가장 많아, 장부 간 연결 자체는 상당수 유지.

**Evidence of fragmentation or diminishing returns(단편화/수확 체감 근거)**

- 301개 단계가 2개 이하 실행. 60~129 구간(70단계) 전체가 71 runs에 불과 → 대부분 1-run repair/review 쌍.
- ONNX 캠페인(268~329)에서 kpi_runs=0인 단계가 길게 이어짐(late stages zero KPI 목록 수십 개). rebuild/materialize/probe 중심으로 KPI 기록이나 strict pass 없이 artifact만 쌓임.
- run role token: repair(361), probe(504), review(437)가 매우 높고, closeout(12)은 극소. "repair"와 "probe"가 지배적 언어.
- 364 내부만 226 runs, 4813 artifact rows, 218 kpi_runs를 소모했으나 current_judgment은 "negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues"로 끝남. proxy에서 density/PF 단서가 나와도 MT5에서 joint 통과 실패 → 새로운 repair input materialize → proxy scout 반복 패턴이 여러 letter run(AR~EZ 등)에서 반복.
- hash_mismatch 8093건, ledger path missing 18470건, stage ledger 2건 누락(266, 326). 산출물 권위 자체가 다수 저하.
- Tier B missing_required가 여러 곳에서 명시되고, Python proxy는 후기(330~359)에서 29건에 그치며 360-364는 전부 MT5(파이썬 대리 검증 거의 없음).

**Usefulness judgment(유용성 판정)**

useful_as_research_map / useful_as_failure_memory / useful_as_frontier (복수 해당)

**What this current state is useful for(현재 상태가 쓸모 있는 곳)**

- 실패 지도(failure map): adapter_repair 장기 체인, ONNX 0-KPI 구간, 364 내부 "package rejected + strict pass 0 + density vs cost/PF/month/equity DD/side balance" 반복 실패 경계.
- 부정 결과 기억(negative result memory): "valid_negative", "negative_proxy_replay", "repair_clues" 판정이 명시적으로 남아 있으며, 어떤 가설이 어떤 조건에서 무너졌는지(월 압박, 숏 비중, proxy-MT5 diff, joint pass 어려움)를 추적 가능.
- 탐색 전선(search frontier): 364에서 살아남은 positive clue(예: 특정 h17 source, density ~3+ 회복 변형, side balance, timestamp context, short source quality, forward stress 대응 단서)와 정확한 실패 조건(월12 equity DD, density floor 미달, short share 과다, proxy gap 등)이 다음 설계의 입력으로 바로 사용 가능.
- 다음 실험 설계(next experiment design): 364 브리프 자체가 hypothesis, broad_sweep/extreme_sweep, micro_search_gate(density >=3 + validation/OOS +0.30 net), WFO 조건(positive scout 시에만), do-not-repeat 메모, failure memory를 상세히 기록. "Stage364 안에서 stage branch 없이 repair 이어감" 패턴도 명확.
- 런타임 동등성 주의(runtime parity caution): proxy scout에서 긍정 단서가 나와도 MT5 probe에서 density/PF/equity DD가 갈리는 사례가 반복 기록됨. Python proxy vs MT5 runtime validation/probe 구분이 실제 데이터로 남아 있음.
- 산출물 계보와 커버리지 지도: 어떤 단계에서 어떤 run/subrun/view와 artifact path/hash가 있었는지 좌표를 제공 (reconstruction map 역할).

**What it is not useful for(쓸모 없는 곳)**

- 운영 승격(operating promotion)이나 runtime authority(런타임 권위) 판단 근거. 모든 주요 판정이 "no_authority", "no operating claim", "package rejected", "review_required_no_authority"로 닫힘.
- 단일 아이디어에 대한 통계적 신뢰도: 대부분 단계가 1-run 또는 소수 실행이며, Tier A separate + Tier B missing_required가 빈번.
- "이전보다 개선됐다"는 누적 성과 주장: repair granularity가 너무 세고, hash mismatch/ledger missing으로 artifact 신뢰도가 낮으며, KPI가 없는 materialization/probe 단계가 많음.
- Python proxy validation(파이썬 대리 검증)으로 MT5 runtime validation/probe(MT5 런타임 검증/탐침)를 대체하는 근거: 후기 대부분이 MT5 중심이고 proxy는 보조적이며, 실제 probe에서 diff가 관찰됨.
- 활동량(volume) 자체를 성과로 해석: 364의 226 runs는 깊이 있는 탐색이 아니라 반복 수리 루프의 결과로 보임.

**Stage 364 specific read(364단계 특화 판독)**

364_source_regime_label_pivot__dense_cost_recovery는 "timestamp-safe source/regime/label context로 q05 dense cost recovery(거래 밀도 >=3/day 유지하면서 비용 끌림 줄이기)"를 주제로 226 runs를 소모한 활성 고밀도 수리 전환 단계다. 원천은 363_lower_floor_rank_surface의 실패( passing_cross_split_rows 0, sparse cost-positive와 open-hour clue만 보존).

내부 흐름은 전형적인 repair/probe 루프:
- materialize → train → review (proxy) → MT5 runtime probe (N, S, AV, BE, CP, CV, DB, DG, DL 등 다수) → review (positive net/PF/density 단서 + repair 필요) → materialize repair inputs (density, side-balance, h17 focus, month12 equity DD, short source, cost/session stress, forward/regime stress, PF floor, validation source rotation 등) → proxy scout → package reject (strict pass 0 또는 joint 미달) → 다음 repair.

주요 관찰:
- density 3/day+를 일부 MT5 probe에서 달성 (예: 3.05, 3.02)했으나 equity DD, month stress(특히 12월), short share, proxy-MT5 gap, long skew, cost/session 압박이 반복적으로 나타남.
- "positive clue preserved but package rejected / no strict joint pass / repair clues"가 누적.
- Tier A separate + Tier B missing_required 명시.
- current_judgment: negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues_review_required_no_authority.
- current_status: completed..._no_strict_joint_pass_review_required_no_authority.
- 364 내부에서 stage branch 없이 수많은 sub-run(letter runs)이 이어졌고, closeout(12) 토큰이 전체적으로 극소한 상황에서 364만으로도 대량의 review/probe/repair 토큰이 발생.

이 단계는 "dense cost recovery"라는 주제를 그 주제 안에서 최대한 밀어붙인 사례지만, 정책상 알파 탐색 closeout은 baseline이 아니라 "preserved clue / negative memory / seed surface"로 닫아야 하는 성격에 가깝다.

**Recommended next move(추천 다음 행동) 우선순위**

**closeout (Stage 364) + repair-registers**를 최우선으로.

이유: 364는 이미 226 runs와 대량 artifact를 생산했으나 strict joint pass 없이 repair clues만 남겼고, 내부 루프가 길어졌다. 더 많은 실험(continue)을 같은 프레임에서 돌리는 것은 diminishing returns(수확 체감) 위험이 크다. 대신 364를 명확히 closeout(negative memory + preserved clue + failure boundary 문서화)하고, 누락 stage ledger(266, 326) 복구 + hash mismatch 영향 명시적 기록(repair-registers)을 먼저 한 뒤, reframe(주제 전환) 또는 split-stage를 검토하는 것이 맞다. split-stage는 364가 사실상 여러 하위 주제(밀도, side, month, short source, regime reseed 등)의 수리 프로그램이 된 경우에 고려.

**10 concrete recommendations(구체 권고 10개)**

1. Stage 364를 exploration mandate 정책에 따라 "preserved clue + negative memory + failure boundary + seed surface" 형식으로 명시적 closeout 문서화. 살아남은 구체 단서(예: 특정 h17 source + density 회복 변형, side balance, timestamp context)와 정확한 실패 조건(월12 equity DD, joint PF+density, proxy-MT5 gap 등)을 목록화.
2. 누락 stage ledger 2건(266_adapter_research__late_segment..., 326_onnx...frozen_forward_robustness_gate)을 즉시 복구하거나 "missing_recorded"로 명확히 표시하고, 이후 coverage audit에 반영.
3. artifact_registry의 8093 hash_mismatch 건에 대해 영향 범위를 분석하고, 해당 run/artifact를 "lower authority for future reference"로 태깅. 신뢰 저하를 숨기지 않음.
4. 향후 알파 탐색에서 "1-run repair/followup_review" 체인을 기본으로 삼지 않도록 최소 실행 깊이 규칙(아이디어당 scout + 최소한의 confirmation runs)을 도입하거나, "repair_lane" vs "exploration_lane"을 run role에 명시적으로 구분.
5. 364 closeout 산출물에서 "Tier B missing_required"를 명확히 기록하고, 이 결과가 미래에 어떻게 해석되어야 하는지(예: Tier A only로만 사용, combined read 금지)를 boundary로 남김.
6. 연구 산출물 척추 문서에서 "repair volume vs exploration depth" 요약 지표(예: repair/probe 토큰 비중, 0-KPI materialization 비율, single-run stage 비율)를 정기적으로 추출해 fragmentation을 조기 감지.
7. 다음 주제 전환(reframe) 전에, 고 artifact 단계(56, 267, 337, 364) 중 일부를 대상으로 artifact lineage + path/hash 실제 사용 가능성 spot audit를 수행.
8. 364에서 관찰된 proxy positive → MT5 marginal on joint + density/cost tradeoff + month/side/equity stress 패턴을 "known stress surfaces"로 별도 failure memory 문서로 추출해 이후 캠페인 설계 시 필수 입력으로 사용.
9. MT5 runtime probe 실행 시 Python proxy validation 결과를 함께 기록하는 관행을 강화(이미 일부 존재하지만 후기 360+에서 Python proxy가 0인 구간이 많음). proxy와 MT5를 명확히 구분해 비교.
10. register repair 후, alpha_run_ledger와 stage_run_ledger의 cross-check에서 "high repair sub-run but zero strict joint pass" 패턴을 자동 플래그하는 간단한 품질 게이트를 추가해, 향후 검토자가 이런 구간을 빠르게 식별하게 함.

**Claims you refuse to make(주장하지 않을 것)**

- operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve 관련 어떤 주장도 하지 않음.
- "Stage 364가 positive result를 냈다", "density recovery가 입증됐다", "proxy와 MT5가 parity를 달성했다", "이전 단계보다 전체적으로 개선됐다" 같은 성과 주장.
- 활동량(226 runs, 4928 artifacts 등)을 그 자체로 우수성의 증거로 해석.
- Tier A 결과만으로 Tier A+B combined(합산)나 전체 프로그램의 대표성을 주장.
- hash mismatch나 missing ledger가 있는 산출물을 "신뢰할 수 있는" 근거로 사용.
- "더 많은 실험을 돌리면 해결될 것"이라는 암묵적 가정.

**Confidence and evidence limits(확신도와 근거 한계)**

이 검토는 제공된 snapshot(Research Artifact Spine + Facets status 문서, compact all-stage table, 364 브리프 발췌, coverage audit, policy excerpts)만을 단독 근거로 한다. 실제 run 폴더 내용, MT5 Strategy Tester 상세 보고서, 개별 KPI 수치, proxy vs MT5 row-by-row 비교, 모델/피처 상세는 보지 않았다. 따라서 "무엇이 시도됐고 어떤 판정 라벨이 붙었는가"와 "구조적 패턴(단편화, repair dominance, clue preservation)"에 대한 진단은 높은 신뢰도를 가지나, 개별 아이디어의 실제 강도나 숨겨진 긍정 단서의 실질적 크기는 이 문서만으로는 알 수 없다. hash_mismatch와 ledger 누락은 산출물 권위를 이미 낮추는 요소로 기록됐다. 이 검토 자체는 research usefulness에만 국한되며, 어떤 운영/런타임 판단의 근거가 될 수 없다.

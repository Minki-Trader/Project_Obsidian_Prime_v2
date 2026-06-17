# Frontier71-F75 Five-Stage Retrospective Prompt(전선71-F75 5단계 회고 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).

Rules(규칙):
- Use only this prompt(프롬프트) as bounded evidence(제한 근거).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).
- Review this as cross-stage synthesis(단계 간 종합), not as per-stage closeout repetition(단계별 마감 반복).
- You cannot create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Current state(현재 상태):
- F75 closeout made the five-stage retrospective gate due(F75 마감으로 5단계 회고 게이트가 도래).
- Covered stages(검토 단계): F71, F72, F73, F74, F75.
- Codex proposed next action(Codex 제안 다음 행동): clear the retrospective gate(회고 게이트를 닫음), then open F76 as axis-ablation source discovery(축 제거/교체 기반 원천 탐색) instead of another parity/tape/risk-only repair loop(동등성/테이프/위험 단독 수리 반복이 아님).
- Claim boundary(주장 경계): direction_delta(방향 변화) and repair_priority_delta(수리 우선순위 변화) only.

Bounded evidence table(제한 근거표):

| stage_id | hypothesis | proxy_kpi | mt5_runtime_probe_kpi | proxy_runtime_gap_cause | closeout_label | preserved_clue | negative_memory | systemic_repeat | next_action |
|---|---|---|---|---|---|---|---|---|---|
| stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd | economics-native label/target and selection(경제성 네이티브 라벨/목표와 선택)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 보존하는 seed surface(씨앗 표면)를 만들 수 있는지 시험했다. | F71B candidates=1620; scout_clue=9; meaningful=0; best_oos_net_pf_dd_tpd=899.1492/1.2505/3.5373%/1.3129. F71C candidates=1440; scout_clue=3; meaningful=0; best_oos=617.6528/1.1481/3.3119%/1.8278. | F71E validation net/PF/DD/tpd/trades=21.77/1.04/8.18%/1.3125/357; OOS=36.35/1.09/5.92%/1.3231/258; signal/feature parity exact 2/2. | threshold semantics mismatch(임계값 의미 불일치)은 수리됐지만 signal/feature parity(신호/피처 동등성) 뒤 runtime economics gap(런타임 경제성 간극)이 남았다. | closed_preserved_clue_negative_memory_no_authority | EA-compatible edge_margin q40 selection(EA 호환 엣지 마진 q40 선택)이 signal count parity(신호 수 동등성)를 복구했다. | meaningful candidate(의미 후보) 0; OOS runtime PF 1.09 and trades/day 1.3231로 최종 목표에서 멀다. | threshold/tape semantics repair(임계값/테이프 의미 수리)는 parity(동등성)를 맞추지만 edge(거래 우위)를 만들지 못한다. | move to trade-shape-first upstream axis(거래 형태 우선 상류 축으로 이동). |
| stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling | trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 개선할 수 있는지 시험했다. | F72B candidates=704; scout_clue=3; meaningful=0; best_oos=1942.5636/1.2108/12.0045%/1.8154. F72C candidates=1728; scout_clue=16; meaningful=0. F72E selected OOS=799.9634/1.0624/10.4275%/2.6823. | F72F validation net/PF/DD/tpd/trades=93.14/1.07/14.94%/2.1397/582; OOS=66.47/1.05/18.60%/2.4769/483; probability parity 3/3; signal/feature diff 0. | selected-entry lifecycle alignment(선택 진입 생명주기 정렬)이 OOS count gap 515->483으로 줄였지만 runtime economics gap(런타임 경제성 간극)은 남았다. | closed_preserved_clue_negative_memory_no_authority | lifecycle-aligned selected entry(생명주기 정렬 선택 진입)가 expected/runtime trade count gap(예상/런타임 거래 수 간극)을 줄였다. | F72B/F72C/F72E meaningful candidate(의미 후보) 0; OOS runtime PF/DD/tpd=1.05/18.60%/2.4769. | count/lifecycle repair(개수/생명주기 수리)는 DD and PF(손실폭과 수익 팩터)를 동시에 살리지 못했다. | move to session/regime feature/model rotation(세션/장세 피처/모델 회전으로 이동). |
| stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap | session/regime feature/model rotation(세션/장세 피처/모델 회전)이 runtime economics source(런타임 경제성 원천)를 분리할 수 있는지 시험했다. | F73B candidates=258; scout_clue=0; meaningful=0; best_oos=1111.6351/1.6559/3.1796%/0.7897. F73C candidates=342; dual_positive=48; meaningful=0; selected_oos=1431.5035/1.3587/4.2453%/1.0. | F73F validation net/PF/DD/tpd/trades=33.83/1.07/21.00%/0.7721/210; OOS=88.88/1.32/5.16%/0.6308/123; source overlap 1.0; probability/signal parity 3/3. | 3-class bridge divergence(3분류 연결 분기)는 direct binary adapter(직접 이진 어댑터)로 제거됐지만 trade lifecycle gap after signal parity(신호 동등성 뒤 거래 생명주기 간극)가 남았다. | closed_preserved_clue_negative_memory_no_authority | direct binary adapter(직접 이진 어댑터)가 source reproduction overlap 1.0(원천 재현 중복 1.0)과 OOS DD 개선 15.33%->5.16%를 만들었다. | validation DD 21.00%, OOS trades/day 0.6308로 네 축 동시 목표에서 멀다. | adapter/parity repair(어댑터/동등성 수리)는 runtime density/economics(런타임 밀도/경제성)를 만들지 못했다. | move to dense label/upstream mechanism rotation(조밀 라벨/상류 메커니즘 전환으로 이동). |
| stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path | microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험했다. | raw density pass=6/6 axes; F74B candidates=648; scout_clue=0; meaningful=0; F74C candidates=1296; scout_clue=0; meaningful=0; materialized proxy OOS=558.88/1.1282/5.5627%/1.6250/312. | F74E validation net/PF/DD/tpd/trades=97.11/1.16/11.40%/1.6544/450; OOS=61.86/1.13/9.66%/1.6000/312; attempts/completed=2/2; probability parity 3/3; signal/feature diff 0. | raw density(원시 밀도)는 만들었지만 signal quality and runtime economics(신호 품질과 런타임 경제성)가 분리됐다. | closed_preserved_clue_negative_memory_no_authority | density feasibility(밀도 실현 가능성)와 short-side ONNX parity(숏 방향 ONNX 동등성)는 보존된다. | scout clue(탐색 단서) 0 and meaningful candidate(의미 후보) 0; runtime PF 1.13-1.16 and trades/day 1.60-1.65로 약하다. | dense label(조밀 라벨)은 trade count(거래 수)를 만들 수 있지만 PF/DD quality(수익 팩터/손실폭 품질)를 자동으로 만들지 않는다. | move to volatility-compression liquidity-release upstream mechanism(변동성 압축/유동성 방출 상류 메커니즘으로 이동). |
| stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density | volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 tradeable-density runtime path(거래 가능한 밀도 런타임 경로)를 만들 수 있는지 시험했다. | F75B candidates=594; scout_clue=11; meaningful=0; best_oos=514.0273/1.1963/5.6023%/1.0000. F75C candidates=324; scout_clue=0; meaningful=0; best_oos=848.9639/1.3312/4.2434%/1.5115. | F75E validation net/PF/DD/tpd/trades=263.38/1.94/3.59%/0.6029/164; OOS=82.86/1.29/14.62%/0.6718/131; attempts/completed=2/2; probability/signal parity 3/3; signal/feature diff 0. | OOS runtime DD(표본외 런타임 손실폭)가 proxy 5.60%에서 runtime 14.62%로 벌어진 runtime economics gap after parity(동등성 뒤 런타임 경제성 간극). | closed_preserved_clue_negative_memory_no_authority | short-only all58 ONNX materialization(숏 전용 58피처 ONNX 물질화), probability/signal parity 3/3, signal/feature diff 0, MT5 probe 2/2. | meaningful proxy signal(의미 프록시 신호) 0; repair scout clue(수리 탐색 단서) 0; OOS runtime PF/DD/tpd=1.29/14.62%/0.6718. | upstream mechanism rotation(상류 메커니즘 전환)도 parity(동등성)는 맞췄지만 density/PF/DD(밀도/수익 팩터/손실폭)를 동시에 맞추지 못했다. | run five-stage retrospective before F76 open(F76 개방 전 5단계 회고 실행). |

Codex preliminary synthesis(Codex 예비 종합):
- repeated_systemic_issues(반복 시스템성 문제): meaningful candidate(의미 후보) stayed zero or absent across F71-F75; parity(동등성) became reproducible but did not create runtime economics(런타임 경제성); density creation(밀도 생성) often damaged PF/DD(수익 팩터/손실폭); one-sided surfaces(단방향 표면) repeatedly under-delivered target trades/day(목표 일거래).
- direction_delta(방향 변화): F76 should test feature set ablation/replacement/recombination, label/target alternatives, model family rotation, trade-shape/risk/session axes as source-discovery matrix(원천 탐색 행렬), with runtime probe required once a meaningful signal(의미 신호)이 appears.
- repair_priority_delta(수리 우선순위 변화): deprioritize bridge/parity/tape-only/cooldown/threshold-only repair(연결/동등성/테이프/쿨다운/임계값 단독 수리); prioritize axis-level falsification(축 수준 반증), feature/label/model novelty(피처/라벨/모델 신규성), and runtime-economics stress before fine tuning(미세 조정 전 런타임 경제성 압박).

Question(질문):
1. Is Codex's direction_delta(방향 변화) valid from this bounded evidence?
2. What should be accepted(수용), rejected(거절), and needs_local_verification(로컬 검증 필요)?
3. What do-not-repeat(반복 금지) rule and F76 opening boundary(F76 개방 경계) should Codex record?

Please answer in compact sections(압축 섹션):
- advice_classification(조언 분류)
- accepted(수용)
- rejected(거절)
- needs_local_verification(로컬 검증 필요)
- repeated_systemic_issues(반복 시스템성 문제)
- direction_delta(방향 변화)
- repair_priority_delta(수리 우선순위 변화)
- F76 opening boundary(F76 개방 경계)
- forbidden_claim_check(금지 주장 확인)

# F85 Stage Brief(F85 단계 개요)

Updated(갱신): 2026-06-18T12:11:46Z

Stage ID(단계 ID): `stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild`

Opening run(개방 실행): `frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_v1`

Next run(다음 실행): `frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_v1`

Status(상태): `opened_runtime_path_contradiction_firewall_label_rebuild_no_authority`

## Frontier Thesis(전선 가설)

A leakage-safe runtime path contradiction firewall label(누수 안전 런타임 경로 모순 방화벽 라벨) can reduce proxy-win/runtime-loss reversals without killing US100 M5 trade density(거래 밀도).

## Experiment Design(실험 설계)

- hypothesis(가설): Entry-time observable surrogates(진입 시점 관측 가능 대체 신호) can predict a high-risk subset of F84 proxy wins that became runtime losses, while preserving enough valid trades for later MT5 materialization.
- decision_use(결정 용도): F85B will run a proxy scout(프록시 탐색) over leakage-safe firewall label families and decide whether any candidate deserves MT5/ONNX materialization in F85C.
- comparison_baseline(비교 기준): F84E OOS runtime net/PF/DD -133.51/0.8598276061188279/29.27; F84E OOS proxy win -> runtime loss 560/821; F84F decision rotate_to_f85_runtime_path_contradiction_firewall_label_rebuild
- control_variables(고정 변수): symbol/timeframe(심볼/시간프레임): FPMarkets US100 M5(FPMarkets US100 5분봉); F84 evidence is reference-only(전선84 근거는 참조 전용); no inherited winner/baseline/runtime authority(승자/기준선/런타임 권위 상속 없음); OOS selection stays locked until predefined train/WFO decision is made(사전 학습/워크포워드 결정 전 표본외 선택 잠금)
- changed_variables(변경 변수): label target changes from realized winrate repair(실현 승률 수리) to runtime path contradiction firewall(런타임 경로 모순 방화벽); candidate inputs are restricted to pre-entry observable surrogates(진입 전 관측 가능 대체 신호); selection metric includes reversal reduction, density, false veto, net/PF/DD(반전 감소/밀도/오차단/순손익/수익 팩터/손실폭); runtime materialization requirements are defined before MT5 execution(런타임 물질화 요구사항을 MT5 실행 전 정의)
- success_criteria(성공 기준): F85B defines at least one leakage-safe firewall candidate family(F85B 누수 안전 방화벽 후보군 1개 이상); proxy-win/runtime-loss reversal rate is reduced inside train/WFO without OOS reselection(표본외 재선택 없이 학습/워크포워드 내 반전율 감소); trade density remains close to final target exploration band(거래 밀도가 최종 목표 탐색 대역을 크게 벗어나지 않음); false veto of runtime winners is explicitly measured(런타임 승자 오차단 측정); meaningful candidates proceed to MT5/ONNX materialization with receipts(의미 후보는 영수증 포함 MT5/온엑스 물질화로 진행)
- failure_criteria(실패 기준): candidate uses ex-post runtime labels as feature/filter(후보가 사후 런타임 라벨을 피처/필터로 사용); threshold-only repair repeats F84 failure(임계값만 수리하며 F84 실패 반복); density death or all-veto surface(밀도 사망 또는 전체 차단 표면); OOS is used for threshold/model selection(표본외가 임계값/모델 선택에 사용); runtime materialization requirements are skipped before MT5 claim(런타임 주장 전 물질화 요구사항 누락)
- invalid_conditions(무효 조건): feature set includes runtime_exit_reason/runtime_win/runtime_net_profit/tp_expected_sl_actual(런타임 종료 사유/승패/순손익/익절예상-손절실제 포함); time axis is treated as true UTC authority instead of broker-clock alignment key(브로커 시계 정렬 키가 아닌 진짜 UTC 권위로 취급); F84 scaffold is treated as F85A evidence without F85A packet/receipt/ledger(F85A 묶음/영수증/장부 없이 F84 뼈대를 F85A 근거로 취급); MT5 compile or ONNX parity is treated as runtime economics(컴파일/온엑스 동등성을 런타임 경제성으로 취급)
- stop_conditions(중지 조건): If no non-leaky pre-entry signal separates reversal risk, rotate or close negative(누수 없는 진입 전 신호가 반전 위험을 분리하지 못하면 회전/부정 마감); If F85B generates no meaningful signal, record zero-signal negative evidence(무신호 부정 근거 기록); If MT5 materialization later mismatches proxy, run row-level reconciliation(향후 MT5 불일치 시 행 단위 조정 실행)

## Label Boundary(라벨 경계)

Action(행동): F85는 `tp_expected_sl_actual(익절예상-손절실제)` 같은 ex-post diagnostic class(사후 진단 분류)를 direct feature/filter(직접 피처/필터)로 쓰지 않는다.

Effect(효과): F84 negative memory(부정 기억)를 활용하되 leakage(누수)와 authority laundering(권위 세탁)을 막는다.

## Runtime Boundary(런타임 경계)

F85A does not run MT5(전선85A는 MT5를 실행하지 않음). Runtime materialization(런타임 물질화)은 F85B/F85C에서 candidate(후보)가 생긴 뒤 수행한다.

Claim boundary(주장 경계): `frontier85_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`.

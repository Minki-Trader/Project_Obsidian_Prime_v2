Review size(검토 크기): small review(소규모 검토)

Snapshot-only rule(스냅샷 전용 규칙): answer only from this prompt(이 프롬프트). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say needs_local_verification(로컬 검증 필요).

Project(프로젝트): Project Obsidian Prime v2, FPMarkets US100 M5.

Current truth(현재 진실): F54 closed as negative_memory_runtime_shaped_payoff_proxy_did_not_transfer(부정 기억, 런타임형 손익 프록시가 MT5로 전이되지 않음). F54 proxy validation/OOS(프록시 검증/표본외) PF(수익 팩터)=1.0279/1.0701, DD(손실폭)=6.59/4.41, proxy trades/day(프록시 거래/일)=5.47/5.85. F54 MT5 validation/OOS(MT5 검증/표본외) PF=0.41/0.61, DD=63.63/28.22, runtime trades/day(런타임 거래/일)=15.20/16.51, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0.

Proposed F55 direction(제안 방향): test a runtime-density-aligned sparse admission source(런타임 밀도 정렬 희소 진입 원천). Keep the runtime-shaped short payoff score(런타임형 숏 손익 점수) only as a reference signal source, but make the actual exported runtime feature rows sparse by score-ranked per-day/session budget(일/세션 예산), minimum bar gap(최소 봉 간격), and forward-only admission(미래정보 없는 진입 허용). The hypothesis(가설) is that MT5 should see about 5~10 expected signals/day(예상 신호/일) directly, rather than relying on proxy overlap to reduce 15+ raw score hits/day.

Success criteria for this stage(이 단계 성공 기준): proxy(프록시) and MT5 runtime probe(런타임 탐침) must both record validation_is and OOS(검증 내부와 표본외); expected signal density(예상 신호 밀도) should be 5~10/day if possible; PF/DD/trade density/proxy-runtime gap(수익 팩터/손실폭/거래 밀도/프록시-런타임 차이)을 기록한다. Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not claimed(주장 없음).

Question(질문): Is this a sufficiently new and bounded frontier hypothesis(전선 가설) after F54, and what are the biggest failure risks before spending MT5 Strategy Tester time(MT5 전략 테스터 시간)? Classify your advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) style where possible.

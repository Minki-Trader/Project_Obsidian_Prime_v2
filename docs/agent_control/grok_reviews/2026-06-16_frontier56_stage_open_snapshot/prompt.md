Review size(검토 크기): small review(소규모 검토)

Snapshot-only rule(스냅샷 전용 규칙): answer only from this prompt(이 프롬프트). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say needs_local_verification(로컬 검증 필요).

Project(프로젝트): Project Obsidian Prime v2, FPMarkets US100 M5.

Current truth(현재 진실): F55 closed as negative_memory_sparse_admission_runtime_veto_did_not_transfer(부정 기억, 희소 진입 허용 런타임 차단이 MT5로 전이되지 않음). F55 MT5 validation/OOS(MT5 검증/표본외) PF(수익 팩터)=0.42/0.64, DD(손실폭)=20.84/8.30, runtime trades/day(런타임 거래/일)=5.21/5.43, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0. This means density/parity(밀도/동등성)는 맞았지만 proxy-to-runtime economics(프록시에서 런타임으로 경제성)가 실패했다.

Preserved clue(보존 단서): F52 close-on-flat/entry-transition/cooldown/ATR SLTP(무신호 청산/전환 진입/쿨다운/평균진폭 손익절)는 DD(손실폭)를 validation/OOS(검증/표본외) 7.36/2.50으로 압축했지만 PF(수익 팩터)는 0.41/0.66으로 실패했다. Therefore(따라서) DD compression(손실폭 압축)은 clue(단서)일 뿐이고 PF source(수익 팩터 원천)는 새로 필요하다.

Proposed F56 direction(제안 방향): open stage_frontier_56__short_pf_edge_after_sparse_admission_memory(전선56 단계) with a new adverse-excursion stop-avoidance source(불리 이동 손절 회피 원천). Train an ONNX(온엑스) short classifier(숏 분류기) on train-only labels(학습 전용 라벨) that require positive isolated runtime PnL(양수 고립 런타임 손익), non-stop exit(비손절 청산), low MAE/ATR(낮은 최대 불리 이동/평균진폭), and enough MFE/ATR(충분한 최대 유리 이동/평균진폭). This is not another sparse admission budget/min-gap repair(희소 진입 예산/최소 간격 수리 아님).

Local scout clue(로컬 탐색 단서): one candidate surface using mae_q=0.55 and mfe_q=0.55 with score_q=0.75 gave proxy validation/OOS(프록시 검증/표본외) PF(수익 팩터)=1.026/1.086, DD(손실폭)=4.06/3.83, trades/day(거래/일)=5.05/5.82. This is weak evidence(약한 근거), not completion(완성), not baseline(기준선), not promotion(승격), and not runtime authority(런타임 권위).

Experiment boundary(실험 경계): use the same core feature order(핵심 피처 순서), same US100 M5 Tier A(티어 A) split(분할), and one MT5 runtime probe(MT5 런타임 탐침) after proxy selection(프록시 선택). Record proxy-runtime gap(프록시-런타임 차이), PF/DD/density(수익 팩터/손실폭/밀도), signal_diff(신호 차이), feature_ready_diff(피처 준비 차이), and stage closeout(단계 마감). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claim.

Question(질문): Is F56 sufficiently new and bounded after F55, and what are the biggest failure risks before implementing the proxy and spending MT5 Strategy Tester time(MT5 전략 테스터 시간)? Classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) where possible.

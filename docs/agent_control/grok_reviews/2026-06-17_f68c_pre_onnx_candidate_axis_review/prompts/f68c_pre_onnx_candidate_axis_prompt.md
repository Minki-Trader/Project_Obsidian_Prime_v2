# F68C Pre-ONNX Candidate Axis Review(F68C ONNX 전 후보 축 검토)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자) for Project Obsidian Prime v2.

Snapshot-only rule(스냅샷 전용 규칙): answer only from this prompt(프롬프트). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), spawn subagents(하위 에이전트 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient(근거 부족), say `needs_local_verification(로컬 검증 필요)`.

## Current State(현재 상태)

- Stage(단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`.
- Current run(현재 실행): `frontier68C_candidate_scoring_or_onnx_scout_export_v1`.
- Latest completed run(최근 완료 실행): `frontier68B_runtime_lifecycle_proxy_broad_sweep_v1`.
- F68 hypothesis(가설): runtime-native trade lifecycle economics proxy(런타임 기반 거래 생명주기 경제성 프록시)가 count/feature parity(개수/피처 동등성)만 맞춘 repair(수리)보다 MT5 Runtime Probe(MT5 런타임 탐침)의 PF/DD/trade density(수익 팩터/손실폭/거래 빈도) 간극을 더 직접 줄일 수 있는지 본다.
- Mandatory future gate(미래 필수 게이트): meaningful proxy signal(의미 있는 프록시 신호)이 있으므로 F68 안에서 MT5 Runtime Probe(MT5 런타임 탐침)를 반드시 실행해야 한다.
- Claim boundary(주장 경계): proxy/scout/pre-export only(프록시/탐색/내보내기 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## F68B Evidence(근거)

F68B broad proxy sweep(넓은 프록시 탐색) changed feature set/label/model/trade shape/risk(피처 묶음/라벨/모델/거래 형태/위험)을 넓게 바꿨다.

- input rows(입력 행): `46650`.
- candidate summaries(후보 요약): `30240`.
- meaningful PF/density signal candidates(의미 있는 수익 팩터/밀도 신호 후보): `293`.
- density-band dual-positive clues(밀도대역 양쪽 양수 단서): `24`.
- density-band strict PF clues(밀도대역 엄격 수익 팩터 단서): `0`.
- density-band plus proxy DD under 10 clues(밀도대역 및 프록시 손실폭 10 미만 단서): `2`.
- PF clue with density gap candidates(밀도 간극이 있는 수익 팩터 단서 후보): `293`.
- proxy joint pass count(프록시 네 축 동시 통과 수): `0`.
- Gap read(간극 판독): density clues(밀도 단서)는 거래 수가 맞지만 PF(수익 팩터)가 약하고, PF clues(수익 팩터 단서)는 거래 수가 너무 낮다.

Best density-aware clue(최선 밀도 고려 단서):

- candidate_id(후보 ID): `f68b_23f4d4607a78`.
- target/model/features(목표/모델/피처): `h2_ddp03_min1p5` / `extra_trees_shallow` / `full58`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.3/1/both/close_horizon`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `1342.5/1.043101/7.476015/11.9191`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `1334.23/1.047846/9.659794/12.756`.
- read(판독): `scout_clue_density_band_pf_weak(밀도대역 PF 약함 탐색 단서)`.

Best low-DD density clue(최선 저손실폭 밀도 단서):

- candidate_id(후보 ID): `f68b_547ac8b4ead1`.
- target/model/features(목표/모델/피처): `h2_ddp03_min1p5` / `hgb_small` / `no_mega_top3`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.7/1/both/atr_sltp_conservative`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `322.311858/1.015342/5.789668/8.842956`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `1536.005585/1.090589/7.226804/9.696686`.
- read(판독): `scout_clue_density_band_pf_weak(밀도대역 PF 약함 탐색 단서)`.

Best PF clue with density gap(최선 수익 팩터 단서와 밀도 간극):

- candidate_id(후보 ID): `f68b_3481a04983ee`.
- target/model/features(목표/모델/피처): `h6_ddp04_min3` / `extra_trees_shallow` / `no_mega_top3`.
- threshold/cooldown/side/exit(임계값/대기봉/방향/청산): `0.975/0/long_only/atr_sltp_conservative`.
- validation net/PF/trades_day/proxy_DD%(검증 순수익/수익 팩터/일 거래/프록시 손실폭): `19.126866/99/1/0`.
- OOS net/PF/trades_day/proxy_DD%(표본외 순수익/수익 팩터/일 거래/프록시 손실폭): `38.232444/99/1/0`.
- read(판독): `meaningful_proxy_signal_pf_clue_density_gap(의미 있는 프록시 신호, 수익 팩터 단서, 밀도 간극)`.

## Codex Proposed Direction(Codex 제안 방향)

F68C should not pick one final candidate(최종 후보) yet. It should preserve two axes(두 축 보존):

1. Density axis(밀도 축): export/retrain `f68b_23f4d4607a78` because it hits target trade density(목표 거래 빈도) but has weak PF(약한 수익 팩터).
2. PF axis(수익 팩터 축): export/retrain `f68b_3481a04983ee` because it has strong PF proxy(강한 수익 팩터 프록시) but severe density gap(거래 빈도 간극).
3. Low-DD density axis(저손실폭 밀도 축): score and attempt export for `f68b_547ac8b4ead1` if local converter support(로컬 변환기 지원) exists; otherwise record it as preserved clue(보존 단서), not invalid(무효).

F68C local work would:

- reconstruct train-only models(학습 전용 모델 재구성) using the F68B logic(로직).
- export only models whose converter succeeds(변환 성공 모델만 내보내기) to ONNX(온엑스).
- run ONNX probability parity(ONNX 확률 동등성) against sklearn probabilities(사이킷런 확률).
- write handoff intent(인계 의도), feature order hash(피처 순서 해시), candidate scoring(후보 점수화), and report(보고서).
- keep MT5 Runtime Probe(MT5 런타임 탐침) as next required materialization(다음 필수 물질화), not claim runtime authority(런타임 권위).

## Review Question(검토 질문)

Critique this F68C direction(방향)을 비판해 주세요:

- Is preserving both density axis(밀도 축) and PF axis(수익 팩터 축) the right next move before MT5 Runtime Probe(MT5 런타임 탐침)?
- Is ONNX scout export(ONNX 탐색 내보내기) of both ExtraTrees candidates(엑스트라트리스 후보) useful enough, given no four-axis proxy candidate(네 축 프록시 후보 없음)?
- Should the HGB low-DD density clue(HGB 저손실폭 밀도 단서) be exported if possible, or only preserved until a repair stage(수리 단계)?
- What drift risks(드리프트 위험) should Codex guard against before running MT5?

Answer with three sections only:

1. `accepted(수용)`: advice Codex should accept.
2. `rejected_or_risky(거절 또는 위험)`: advice or direction that is risky.
3. `needs_local_verification(로컬 검증 필요)`: facts that need local evidence.

Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).

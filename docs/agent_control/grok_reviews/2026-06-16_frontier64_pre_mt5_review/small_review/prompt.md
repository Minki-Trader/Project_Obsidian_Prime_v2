# Frontier64 Pre-MT5 Review(전선64 비싼 MT5 전 검토)

You are Grok(그록), external second opinion(외부 2차 의견). Review only this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Current Truth(현재 진실)

- Stage(단계): `stage_frontier_64__independent_pf_source_after_inverse_signal_memory`.
- Stage-open Grok review(단계 개방 그록 검토): accepted(수용), with warning(경고) that hazard gate(위험 게이트)가 단순 thinning(거래 축소)만 만들면 F55 sparse admission(희소 진입 허용) 반복으로 닫아야 한다.
- Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음).

## F63 Reference Negative Memory(F63 참조 부정 기억)

- F63 selected proxy(선택 프록시): validation/OOS PF(검증/표본외 수익 팩터) `0.8140 / 0.8527`, DD(손실폭) `12.33% / 6.68%`, density(거래 빈도) `4.14 / 4.76`.
- F63 MT5 runtime probe(MT5 런타임 탐침): validation/OOS PF(검증/표본외 수익 팩터) `0.35 / 0.44`, DD(손실폭) `22.56% / 15.61%`, density(거래 빈도) `4.90 / 5.67`, signal_diff(신호 차이) `-670 / -506`, feature_ready_diff(피처 준비 차이) `0 / 0`.
- F63 is reference-only(참조 전용) negative memory(부정 기억), not baseline(기준선) or authority(권위).

## F64B Proxy Result(F64B 프록시 결과)

- Run(실행): `frontier64B_loss_cluster_hazard_proxy_scout_v1`.
- Model role(모델 역할): binary hazard model(이진 위험 모델) predicts local loss-cluster hazard(국소 손실 군집 위험). It does not choose direction(방향을 고르지 않음).
- Entry surface(진입 표면): simple symmetric entry surface(단순 대칭 진입 표면) supplies direction(방향). Hazard model(위험 모델) only admits or blocks(허용/차단).
- Candidate rows(후보 행): `288`.
- F63 four-axis proxy beat rows(F63 네 축 동시 개선 프록시 행): `48`.
- Seed surface rows(씨앗 표면 행): `0`.
- Preserved clue rows(보존 단서 행): `80`.
- Best candidate(최선 후보): `f64b_f64b_hz_w36_h6_q75_eq55_hz65_h2_cd0`.
- Best validation PF/density/DD/smoothness(검증 수익 팩터/빈도/손실폭/매끄러움): `1.06414 / 5.6612 / 4.4890% / 0.5772`.
- Best OOS PF/density/DD/smoothness(표본외 수익 팩터/빈도/손실폭/매끄러움): `1.15643 / 6.05344 / 3.19127% / 0.6914`.
- ONNX parity(온엑스 동등성): selected model(선택 모델) passed(통과), max_abs_diff(최대 절대 차이) `1.98e-7`.
- Hazard-vs-thinning read(위험 대 단순 축소 판독): `hazard_gate_proxy_clue_not_only_thinning(위험 게이트 프록시 단서, 단순 축소만은 아님)`.

## Known Caveats(알려진 주의점)

- This is proxy-only(프록시 전용). MT5 runtime probe(MT5 런타임 탐침), WFO(워크포워드), stress(스트레스)는 아직 없다.
- F64 runtime handoff(런타임 인계)는 binary ONNX hazard output(이진 ONNX 위험 출력) plus simple symmetric direction rule(단순 대칭 방향 규칙)을 MT5에서 재현해야 한다. Local verification(로컬 검증)이 필요하다.
- Path length(경로 길이) for 02_runs(실행 산출물) requires `io_path(입출력 경로)` or long-path prefix(긴 경로 접두사).

## Review Questions(검토 질문)

1. Is the proxy result strong enough to justify one narrow MT5 runtime probe(좁은 MT5 런타임 탐침) after local handoff verification(로컬 인계 검증)?
2. What is the main proxy-to-runtime risk(프록시-런타임 위험)?
3. What must Codex(코덱스) verify locally before MT5 execution(MT5 실행)?
4. Should F64 proceed to MT5 probe(진행), adjust handoff first(인계 먼저 조정), or close/block(마감/차단)?

Answer with classification(분류): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.

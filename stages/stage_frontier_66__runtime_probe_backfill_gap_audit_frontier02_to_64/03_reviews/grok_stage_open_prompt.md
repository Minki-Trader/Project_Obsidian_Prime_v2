# F66 Stage Open Grok Review Prompt(단계 개방 그록 검토 프롬프트)

You are Grok(Grok, 그록) acting as an external second opinion(외부 2차 의견). Do not create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Current Truth(현재 진실)

- F65 closed as preserved clue(보존 단서): `sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points(프록시 가격 단위와 MT5 포인트 손절/익절 의미 차이)`.
- User asked to open F66 before the next hypothesis and audit frontier stage(전선 단계) F02-F64.
- Scope(범위): identify stages without actual runtime probe KPI(실제 런타임 탐침 KPI), materialize/backfill where possible, and analyze proxy-runtime gap(프록시-런타임 간극) like F65.
- Local dry-run inventory(로컬 건식 인벤토리) found:
  - actual runtime KPI present(실제 런타임 KPI 있음): F02-F10, F12-F14, F16-F17, F50, F52-F64.
  - actual runtime KPI missing(실제 런타임 KPI 누락): F11, F15, F18-F49, F51.
  - missing group material scan(누락 묶음 재료 스캔): ONNX/joblib/pkl count(온엑스/잡리브/pkl 수) was zero for every missing stage.
  - actual KPI exists but gap report missing(실제 KPI는 있으나 간극 보고 없음): F02-F10, F12-F14, F16-F17.

## Proposed Direction(제안 방향)

F66 should be a runtime_probe_backfill_gap_audit(런타임 탐침 소급 간극 감사), not a new model hypothesis(모델 가설). It will:

1. Create F66 stage artifacts(단계 산출물).
2. For missing actual runtime KPI stages, write materialization status(물질화 상태). If no ONNX/joblib/pkl material exists, classify as `invalid_setup_no_runtime_material(런타임 재료 없음 무효 설정)` rather than pretending an MT5 backtest ran.
3. For stages with actual runtime KPI, extract proxy(프록시) and runtime(런타임) metrics and tag gap causes.
4. Report problems to the user without stage closeout(단계 마감) unless explicitly closed after review.

## Success Criteria(성공 기준)

- No overclaim(과장 주장 없음).
- Missing probe(누락 탐침) is separated from missing runtime material(런타임 재료 누락).
- Existing runtime KPI(런타임 KPI)는 KPI로 남기고, proxy-only(프록시 전용) rows are not counted as runtime.
- Gap analysis(간극 분석) names concrete causes: material absence(재료 부재), gap report absence(간극 보고 부재), PF transfer failure(PF 전이 실패), DD overrun(손실폭 초과), signal/feature parity gap(신호/피처 동등성 간극), and SL/TP unit semantics risk(손절/익절 단위 의미 위험).

## Review Question(검토 질문)

Is this F66 scope and claim boundary sound? What are the main risks before writing the F66 reports and per-stage missing-material status files?

# F68H Pre MT5 Runtime Repair Probe Review(F68H MT5 런타임 수리 탐침 전 검토)

You are Grok(Grok, 그록), an external second opinion(외부 2차 의견). Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Direction Before Grok(Codex의 그록 전 방향)

Current state(현재 상태): Frontier68(F68) is an active exploration stage(탐색 단계), not a completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Proposed next action(제안 행동): run F68H as a narrow MT5 Runtime Probe(MT5 런타임 탐침) that keeps the exact F68F ONNX(온엑스), feature order(피처 순서), signal parity(신호 동등성), and feature readiness parity(피처 준비 동등성), while testing only ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투) variants.

Success criteria(성공 기준): This probe is useful if it shows whether DD(drawdown, 손실폭) can be compressed materially without destroying PF(profit factor, 수익 팩터), net profit(순수익), and trade density(거래 밀도). Final target gates(최종 목표 게이트) are not claimed here.

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Review size(검토 크기): medium review(중간 검토).

Focused question(집중 질문): Is the F68H plan a valid capped repair(상한 있는 수리) after F68F, and what should Codex accept, reject, or locally verify before running MT5?

## Evidence Snapshot(근거 스냅샷)

Stage(단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`

Latest completed run(최근 완료 실행): `frontier68G_repair_result_review_or_next_validation_v1`

Next run(다음 실행): `frontier68H_atr_sltp_risk_envelope_runtime_repair_probe_v1`

F68F candidate(후보): `f68b_0872ddc6192f`

F68F handoff(인계):

- model backend(모델 백엔드): ONNX(온엑스)
- model sha256(모델 해시): `ab632bd1f8e7db05158246126d2a388686906b97c5caf44dfe252e0e56b27f40`
- feature count(피처 수): `49`
- feature order hash(피처 순서 해시): `14a037f12cec16ad2f57a9cb5cafb5d61a374b96640872a6ac51bb6f28baf2a3`
- max hold bars(최대 보유 봉): `2`
- same direction cooldown(동방향 쿨다운): `6`
- ATR SL/TP enabled(평균진폭 손절/익절 사용): `False` in F68F
- probability parity rows(확률 동등성 행): `3`, all passed(모두 통과)
- signal parity rows(신호 동등성 행): `2`, all passed(모두 통과)
- signal diff(신호 차이): `0`
- feature diff(피처 준비 차이): `0`

F68F MT5 runtime KPI(런타임 핵심 성과 지표):

| split(분할) | period(기간) | net profit(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| validation(검증) | 2025-01-02..2025-10-01 | 8.91 | 1701.20 | -1692.29 | 1.01 | 25.06 | 1081 | 3.974265 |
| OOS(표본외) | 2025-10-01..2026-04-14 | 241.18 | 1586.79 | -1345.61 | 1.18 | 19.57 | 932 | 4.779487 |

F68F versus F68D density axis(F68D 밀도 축 대비):

- validation(검증): net delta(순수익 차이) `+303.37`, PF delta(수익 팩터 차이) `+0.10`, DD delta(손실폭 차이) `-46.07`, trades/day delta(일 거래 차이) `-2.86`
- OOS(표본외): net delta(순수익 차이) `+137.70`, PF delta(수익 팩터 차이) `+0.14`, DD delta(손실폭 차이) `-7.27`, trades/day delta(일 거래 차이) `-3.68`

F68G judgment(판정): preserved clue(보존 단서), risk envelope repair required(위험 봉투 수리 필요), no authority(권위 없음).

F52 preserved clue(보존 단서): ATR SL/TP(평균진폭 손절/익절), close-on-flat(무신호 청산), transition/cooldown(전환/쿨다운) compressed MT5 DD under 10%(MT5 손실폭 10% 미만 압축) but PF failed there. F68H uses only this as a reference clue(참조 단서), not inherited authority(상속 권위).

Planned F68H variants(계획 변형):

| variant(변형) | role(역할) | ATR stop(손절) | ATR TP(익절) | reentry cooldown(재진입 쿨다운) | same direction cooldown(동방향 쿨다운) |
|---|---|---:|---:|---:|---:|
| `f52_atr08_tp12_re3_sd6` | preserved clue replay(보존 단서 재생) | 0.8 | 1.2 | 3 | 6 |
| `tight_atr06_tp10_re3_sd6` | DD compression pressure(손실폭 압축 압박) | 0.6 | 1.0 | 3 | 6 |
| `wide_atr10_tp16_re3_sd6` | PF preservation pressure(수익 팩터 보존 압박) | 1.0 | 1.6 | 3 | 6 |

All variants(모든 변형):

- same ONNX(같은 온엑스)
- same feature CSV(같은 피처 CSV)
- same feature order(같은 피처 순서)
- same F68F thresholds/margin(F68F 임계값/마진 동일)
- close on flat signal(무신호 청산): `True`
- reverse on opposite signal(반대 신호 반전): `True`
- max hold bars(최대 보유 봉): `2`
- validation and OOS runs(검증 및 표본외 실행)

Known risk(알려진 위험):

- This is runtime risk logic(런타임 위험 로직), not a new PF source(새 수익 팩터 원천).
- ATR SL/TP may compress DD but damage PF/net(수익 팩터/순수익).
- Trades/day(일 거래)는 F68F OOS `4.779487`로 near target(목표 근접)이지만 validation(검증)은 `3.974265`라 density repair(밀도 수리)가 아직 필요할 수 있다.

## Requested Output(요청 출력)

Return concise bullets with:

- accepted(수용): which parts of F68H plan are valid.
- rejected(거절): what Codex must not infer or do.
- needs_local_verification(로컬 검증 필요): exact checks before/after MT5.
- drift risks(드리프트 위험): any risk of repeating old failure modes.
- final recommendation(최종 권고): run, revise, or stop this repair.

Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

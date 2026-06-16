Frontier65 pre-MT5 review(전선65 비싼 MT5 전 검토)입니다.

Please answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Current Local Finding(현재 로컬 발견)

- F65B attribution scout(귀속 탐색)는 F64E proxy-runtime gap(프록시-런타임 차이)을 층별로 분해했다.
- feature_ready_diff(피처 준비 차이)는 validation/OOS `0/0`.
- raw adapter signal(원 어댑터 신호), runtime veto tape(런타임 차단 테이프), entry transition gate(진입 전환 게이트)는 telemetry(런타임 기록)와 수량상 맞았다.
- signal count gap(신호 수 차이): validation/OOS expected after veto(차단 후 예상) `4073 / 3325`, entry transition block(진입 전환 차단) `2973 / 2483`, actual non-flat(실제 비관망) `1100 / 842`.
- PF/DD economics gap(수익 팩터/손실폭 경제성 차이): validation/OOS proxy PF `1.0727 / 1.1081`, MT5 PF `0.35 / 0.70`, proxy DD `4.319 / 3.154`, MT5 DD `28.23 / 7.92`.
- Exit shape(청산 형태): proxy maxhold(프록시 최대보유) `58.9% / 56.7%`, MT5 maxhold(실제 최대보유) `0% / 0%`; MT5 stop rate(손절률) `79.5% / 67.5%`.
- ATR unit clue(ATR 단위 단서): proxy ATR price median(프록시 ATR 가격 중앙값) `31.09 / 36.67`, MT5 ATR points median(MT5 ATR 포인트 중앙값) `3506.64 / 4025.96`, inferred point(추정 포인트) about `0.009`.

## Proposed RUN_C(제안 RUN_C)

Run(실행): `frontier65C_targeted_sltp_unit_runtime_probe_v1`.

Action(행동): reuse F64D direction adapter ONNX(방향 어댑터 온엑스), feature matrix(피처 행렬), and runtime veto tape(런타임 차단 테이프), but change only ATR SL/TP point inputs(ATR 손절/익절 포인트 입력) by multiplying point thresholds by `100`: stop min/max `40/180` becomes `4000/18000`, take min/max `60/280` becomes `6000/28000`.

Effect(효과): if the unit-semantics clue(단위 의미 단서) is real, MT5 exit shape(청산 형태) should move away from immediate SL/TP(즉시 손절/익절) and closer to proxy maxhold behavior(프록시 최대보유 동작). This is still runtime_probe_observation(런타임 탐침 관찰), not authority(권위).

## Review Request(검토 요청)

1. Classification(분류): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.
2. Is RUN_C a narrow sufficient MT5 check(좁은 충분 MT5 확인) for the F65B clue?
3. What must be recorded to avoid overclaiming(과장 주장 방지)?
4. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.

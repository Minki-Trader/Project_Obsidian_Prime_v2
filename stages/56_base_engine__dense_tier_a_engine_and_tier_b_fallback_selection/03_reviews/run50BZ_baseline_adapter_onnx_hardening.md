# Stage56 run50BZ BaselineAdapter ONNX Hardening(Stage56 run50BZ 기준선 어댑터 ONNX 경화)

- terminal_label(종료 라벨): `onnx_parity_passed`
- adapter_id(어댑터 ID): `ba14_no_atr_sd5_lot025`
- ONNX path(ONNX 경로): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BZ/models/ba14_stage56_context_gap_refill_entry.onnx`
- ONNX sha256(ONNX 해시): `bc7981a7bda403c02b50ae08014d681f39212db0564f64be9f9f9688864b5e33`
- parity rows(동등성 행): `17428`
- max_abs_diff(최대 절대 차이): `4.237248085736667e-08`
- tolerance(허용 오차): `1e-06`

Action(행동): Stage56 entry table(진입 표)을 probability-only ONNX(확률 전용 ONNX)로 내보내고 Python/ONNX parity(파이썬/ONNX 동등성)를 검증했다.
Effect(효과): MT5 runtime reproduction(MT5 런타임 재현) 전에 model probability contract(모델 확률 계약)를 고정했다.

## Adapter Boundary(어댑터 경계)

- in ONNX(ONNX 내부): entry probability(진입 확률) `short/flat/long`
- outside ONNX(ONNX 외부): fixed lot(고정 랏), 0.01 lot floor(0.01 랏 바닥), order send(주문 전송), broker stop distance(브로커 스톱 거리), Tier B disablement(Tier B 비활성), cooldown lifecycle(쿨다운 생명주기)

No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.

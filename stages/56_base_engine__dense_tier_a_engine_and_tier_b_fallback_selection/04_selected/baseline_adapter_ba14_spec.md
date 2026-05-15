# BaselineAdapter ba14 Spec(기준선 어댑터 ba14 명세)

- adapter_id(어댑터 ID): `ba14_no_atr_sd5_lot025`
- development_anchor(개발 기준점): `v64_v47_ctxgap14_refill_etfw_h2_no_b`
- entry ONNX(진입 ONNX): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BZ/models/ba14_stage56_context_gap_refill_entry.onnx`
- feature_order_hash(피처 순서 해시): `12961356381137e71ebc95729041c747d91104f02a31163523e298273d8c96de`
- fixed_lot(고정 랏): `0.25`
- same_direction_reentry_cooldown_bars(동일 방향 재진입 쿨다운 봉): `5`
- ATR SL/TP(ATR 손절/익절): disabled(비활성)
- Tier B(Tier B): disabled with evidence(근거 기반 비활성)

Effect(효과): model output(모델 출력)은 probability(확률)만 ONNX(온닉스)에 두고, lot rounding/min lot/order send(랏 반올림/최소 랏/주문 전송)는 MT5 execution translation(MT5 실행 번역)에 둔다.

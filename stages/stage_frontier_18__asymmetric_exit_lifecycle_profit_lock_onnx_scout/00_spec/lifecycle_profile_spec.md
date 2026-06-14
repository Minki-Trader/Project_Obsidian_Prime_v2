# Frontier18 Lifecycle Profile Spec(전선18 생명주기 프로필 명세)

Action(행동): Frontier18B(전선18B) 전에 3 lifecycle profiles(생명주기 프로필)를 고정합니다.

Effect(효과): validation/OOS(검증/표본외) 결과를 본 뒤 exit parameter(청산 파라미터)를 추가하는 repair ladder(수리 사다리)를 막습니다.

- `f18b_hold4_flat_close_atr1p2_tp2p4`: max_hold_bars(최대 보유 봉) `4`, close_on_flat(중립 청산) `True`, reverse_on_opposite(반대 신호 전환) `False`, ATR SL/TP(ATR 손절/익절) `1.2`/`2.4`; short lifecycle with explicit profit lock(짧은 생명주기와 명시적 수익 잠금)
- `f18b_hold6_reverse_atr1p5_tp3p0`: max_hold_bars(최대 보유 봉) `6`, close_on_flat(중립 청산) `False`, reverse_on_opposite(반대 신호 전환) `True`, ATR SL/TP(ATR 손절/익절) `1.5`/`3.0`; balanced lifecycle with opposite signal transition(균형 생명주기와 반대 신호 전환)
- `f18b_hold8_exit_risk_overlay_atr1p0_tp2p0`: max_hold_bars(최대 보유 봉) `8`, close_on_flat(중립 청산) `True`, reverse_on_opposite(반대 신호 전환) `False`, ATR SL/TP(ATR 손절/익절) `1.0`/`2.0`; exit-risk overlay lane for early damage control(초기 손상 제어를 위한 청산 위험 덧씌움 축)

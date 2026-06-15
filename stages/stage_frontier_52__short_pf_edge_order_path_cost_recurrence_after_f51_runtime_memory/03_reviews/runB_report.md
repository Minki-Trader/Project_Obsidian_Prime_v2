# Frontier52 Run B(전선52 실행 B)

Action(행동): `.set` parameter policy(설정 파라미터 정책)를 물질화했다.

Effect(효과): ONNX(온엑스), feature order(피처 순서), signal parity(신호 동등성)를 유지한 채 close-on-flat/transition/cooldown/ATR SLTP(무신호 청산/전환/쿨다운/평균진폭 손익절)만 시험한다.

## Reference Candidate(참조 후보)
- candidate(후보): `f51c_0046`
- proxy_forward_min_pf(프록시 전진 최소 수익 팩터): 1.03747333031916
- proxy_forward_max_dd(프록시 전진 최대 손실폭): 4.485936564780124

## Policy(정책)
- InpCloseOnFlatSignal: True
- InpEntryTransitionOnly: True
- InpEntryTransitionRearmMinConfidenceDelta: 0.02
- InpMaxHoldBars: 6
- InpReentryCooldownBars: 3
- InpSameDirectionReentryCooldownBars: 6
- InpAtrSltpEnabled: True
- InpAtrPeriod: 14
- InpAtrStopMultiplier: 0.8
- InpAtrTakeProfitMultiplier: 1.2
- InpAtrMinStopPoints: 40.0
- InpAtrMaxStopPoints: 180.0
- InpAtrMinTakeProfitPoints: 60.0
- InpAtrMaxTakeProfitPoints: 260.0

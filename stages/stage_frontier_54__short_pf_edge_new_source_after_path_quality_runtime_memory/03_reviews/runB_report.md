# Frontier54 Run B(전선54 실행 B)

Action(행동): ExtraTrees depth6 leaf80(엑스트라트리 깊이6 리프80) 모델로 runtime-shaped payoff source(런타임형 손익 원천)를 학습하고 q70/q75(분위수 70/75)를 좁게 확인했다.

Effect(효과): 주 후보 `f54b_extratrees_d6_l80_short_runtimepay_s70`만 MT5 runtime probe(MT5 런타임 탐침)로 보내고, q75(분위수 75)는 threshold stress(문턱값 압박 확인)로만 보존한다.

## Proxy Rows(프록시 행)
- f54b_extratrees_d6_l80_short_runtimepay_s70: val PF/DD/density(검증 수익 팩터/손실폭/밀도)=1.0279309034741884/6.593274204464006/5.469945355191257; OOS PF/DD/density(표본외 수익 팩터/손실폭/밀도)=1.0700525748726053/4.414364970697093/5.854961832061068
- f54b_extratrees_d6_l80_short_runtimepay_s70_stress_s75: val PF/DD/density(검증 수익 팩터/손실폭/밀도)=1.0336821368775313/5.867138342918254/4.683060109289618; OOS PF/DD/density(표본외 수익 팩터/손실폭/밀도)=1.074044064742925/3.9817958636063855/5.022900763358779

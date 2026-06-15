# Frontier53 Run B(전선53 실행 B)

Action(행동): logreg_l2_c05(로지스틱 회귀 L2 C0.5) short path-quality classifier(숏 경로 품질 분류기)를 학습하고 0.90/0.93 score quantile(점수 분위수)을 좁게 확인했다.

Effect(효과): 주 후보 `f53b_logreg_l2_c05_short_q25_q70_s90`만 MT5 runtime probe(MT5 런타임 탐침)로 보내고, 0.93은 threshold artifact(문턱값 산물) 확인용 stress(압박 확인)로만 보존한다.

## Proxy Rows(프록시 행)
- f53b_logreg_l2_c05_short_q25_q70_s90: val PF/DD/density(검증 수익 팩터/손실폭/밀도)=1.0018671479142887/7.96045908880354/7.256830601092896; OOS PF/DD/density(표본외 수익 팩터/손실폭/밀도)=1.0961906495988258/7.350606304191166/10.236641221374045
- f53b_logreg_l2_c05_short_q25_q70_s90_stress_s93: val PF/DD/density(검증 수익 팩터/손실폭/밀도)=1.0037912736413488/5.934908282679041/5.092896174863388; OOS PF/DD/density(표본외 수익 팩터/손실폭/밀도)=1.0802228684892812/7.789027930566039/7.8396946564885495

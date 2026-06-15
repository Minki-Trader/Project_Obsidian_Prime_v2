# F61B Proxy Report(F61B 프록시 보고)

Action(행동): 3-class side-allocation ONNX(3분류 방향 배분 온엑스)를 학습하고 capped proxy grid(상한 프록시 격자)를 평가했다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)에 올릴 후보를 하나로 동결하고, proxy-runtime gap(프록시-런타임 차이)을 비교할 기준을 만든다.

- label_config(라벨 설정): `balanced_margin_q45_opp_q55`
- label train short/flat/long(학습 숏/무거래/롱): `6458/16072/6692`
- model class rows(모델 클래스 행): `3`
- proxy rows(프록시 행): `18`
- selected(선택): `f61b_side_alloc_t38_m2_h4`
- selected validation/OOS PF(선택 검증/표본외 PF): `0.9797838219739115` / `1.1169141590649971`
- selected validation/OOS density(선택 검증/표본외 밀도): `4.7923497267759565` / `4.778625954198473`

## Top Train PF Rows(학습 PF 상위 행)
- `f61b_side_alloc_t42_m2_h6`: train PF/DD/density(학습 PF/DD/밀도)=2.148529309188856/2.664148367278396/0.41361256544502617; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.3050464322797433/2.211344624333522/0.5725190839694656
- `f61b_side_alloc_t42_m4_h6`: train PF/DD/density(학습 PF/DD/밀도)=2.148529309188856/2.664148367278396/0.41361256544502617; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.3050464322797433/2.211344624333522/0.5725190839694656
- `f61b_side_alloc_t42_m6_h6`: train PF/DD/density(학습 PF/DD/밀도)=2.148529309188856/2.664148367278396/0.41361256544502617; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.3050464322797433/2.211344624333522/0.5725190839694656
- `f61b_side_alloc_t42_m2_h4`: train PF/DD/density(학습 PF/DD/밀도)=2.0666846916669868/2.664148367278396/0.41535776614310643; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.2399528020284374/2.2415057333170285/0.5725190839694656
- `f61b_side_alloc_t42_m4_h4`: train PF/DD/density(학습 PF/DD/밀도)=2.0666846916669868/2.664148367278396/0.41535776614310643; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.2399528020284374/2.2415057333170285/0.5725190839694656
- `f61b_side_alloc_t42_m6_h4`: train PF/DD/density(학습 PF/DD/밀도)=2.0666846916669868/2.664148367278396/0.41535776614310643; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.2399528020284374/2.2415057333170285/0.5725190839694656
- `f61b_side_alloc_t38_m2_h6`: train PF/DD/density(학습 PF/DD/밀도)=1.3404727346369194/4.517480655616857/2.842931937172775; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.0143626857107806/5.139722242753086/4.502732240437158
- `f61b_side_alloc_t38_m4_h6`: train PF/DD/density(학습 PF/DD/밀도)=1.3404727346369194/4.517480655616857/2.842931937172775; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.0143626857107806/5.139722242753086/4.502732240437158

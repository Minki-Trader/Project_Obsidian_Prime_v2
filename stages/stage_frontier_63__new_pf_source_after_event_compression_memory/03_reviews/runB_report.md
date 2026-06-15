# F63B Proxy Report(F63B 프록시 보고)

Action(행동): 3-class side-allocation ONNX(3분류 방향 배분 온엑스)를 학습하고 inverse event-compressed capped proxy grid(역전 이벤트 압축 상한 프록시 격자)를 평가했다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)에 올릴 역전 후보를 하나로 동결하고, proxy-runtime gap(프록시-런타임 차이)을 비교할 기준을 만든다.

- label_config(라벨 설정): `balanced_margin_q45_opp_q55`
- label train short/flat/long(학습 숏/무거래/롱): `6458/16072/6692`
- model class rows(모델 클래스 행): `3`
- proxy rows(프록시 행): `252`
- selected(선택): `f63b_inv_evt_t20_m0_h2_cd0_cof1`
- selected validation/OOS PF(선택 검증/표본외 PF): `0.8140498112595147` / `0.8526944472672842`
- selected validation/OOS density(선택 검증/표본외 밀도): `4.14207650273224` / `4.755725190839694`
- selected policy(선택 정책): close_on_flat(무신호 청산)=`True`, entry_transition(진입 전환)=`True`, same_direction_cooldown(동일 방향 쿨다운)=`0`
- invert_signal(신호 역전): `True`
- density penalty(밀도 벌점): `1.997486264543249`

## Top Train PF Rows(학습 PF 상위 행)
- `f63b_inv_evt_t40_m0_h2_cd0_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.855656978439069/12.342927277531157/1.181500872600349; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7659584052384681/6.602820666022424/1.549618320610687
- `f63b_inv_evt_t40_m1_h2_cd0_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.855656978439069/12.342927277531157/1.181500872600349; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7659584052384681/6.602820666022424/1.549618320610687
- `f63b_inv_evt_t40_m2_h2_cd0_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.855656978439069/12.342927277531157/1.181500872600349; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7659584052384681/6.602820666022424/1.549618320610687
- `f63b_inv_evt_t40_m4_h2_cd0_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.855656978439069/12.342927277531157/1.181500872600349; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7659584052384681/6.602820666022424/1.549618320610687
- `f63b_inv_evt_t40_m0_h2_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.8407160139627015/12.20403528707622/1.050610820244328; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7405445848386583/7.8625094449153/1.3387978142076502
- `f63b_inv_evt_t40_m1_h2_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.8407160139627015/12.20403528707622/1.050610820244328; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7405445848386583/7.8625094449153/1.3387978142076502
- `f63b_inv_evt_t40_m2_h2_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.8407160139627015/12.20403528707622/1.050610820244328; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7405445848386583/7.8625094449153/1.3387978142076502
- `f63b_inv_evt_t40_m4_h2_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=0.8407160139627015/12.20403528707622/1.050610820244328; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=0.7405445848386583/7.8625094449153/1.3387978142076502

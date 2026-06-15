# F62B Proxy Report(F62B 프록시 보고)

Action(행동): 3-class side-allocation ONNX(3분류 방향 배분 온엑스)를 학습하고 event-compressed capped proxy grid(이벤트 압축 상한 프록시 격자)를 평가했다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)에 올릴 후보를 하나로 동결하고, proxy-runtime gap(프록시-런타임 차이)을 비교할 기준을 만든다.

- label_config(라벨 설정): `balanced_margin_q45_opp_q55`
- label train short/flat/long(학습 숏/무거래/롱): `6458/16072/6692`
- model class rows(모델 클래스 행): `3`
- proxy rows(프록시 행): `252`
- selected(선택): `f62b_evt_t20_m0_h2_cd0_cof1`
- selected validation/OOS PF(선택 검증/표본외 PF): `1.0977429734981603` / `0.9826772240239987`
- selected validation/OOS density(선택 검증/표본외 밀도): `4.2076502732240435` / `4.801526717557252`
- selected policy(선택 정책): close_on_flat(무신호 청산)=`True`, entry_transition(진입 전환)=`True`, same_direction_cooldown(동일 방향 쿨다운)=`0`
- density penalty(밀도 벌점): `1.8546973547684429`

## Top Train PF Rows(학습 PF 상위 행)
- `f62b_evt_t42_m0_h6_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9849491706103461/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m1_h6_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9849491706103461/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m2_h6_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9849491706103461/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m4_h6_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9849491706103461/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m0_h4_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9381339868226708/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m1_h4_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9381339868226708/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m2_h4_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9381339868226708/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389
- `f62b_evt_t42_m4_h4_cd2_cof1`: train PF/DD/density(학습 PF/DD/밀도)=1.9381339868226708/2.159328207674771/0.2914485165794066; forward min PF/max DD/min density(전진 최소 PF/최대 DD/최소 밀도)=1.158259293610209/1.4870262665760303/0.3511450381679389

# Frontier15 Experiment Design(프론티어15 실험 설계)

- hypothesis(가설): F14(프론티어14)의 label-side density(라벨 쪽 빈도)는 올라갔지만 argmax signal(최대확률 신호)이 거래 빈도 절벽을 만들었다. F15(프론티어15)는 같은 초기 label family(라벨 계열)를 control(통제)로 두고, ONNX probability tensor(온엑스 확률 텐서)를 score surface(점수 표면)로 읽어 train-only density threshold(학습 전용 빈도 임계값) 계약을 시험한다.
- changed_variable(변경 변수): runtime decision contract(런타임 결정 계약)
- primary_cell(1순위 칸): `edge_margin__target8`
- controls(통제 변수): same Tier A dataset(같은 티어 A 데이터셋), same feature order(같은 피처 순서), initial F14 opportunity labels only(초기 F14 기회 라벨만 사용), no quota/horizon retuning(할당/보유기간 재조정 없음), no validation/OOS threshold calibration(검증/표본밖 임계값 보정 없음)
- required_rows(필수 행): all 9 score-target cells reported(9개 점수-목표 칸 전부 보고), F14-matched argmax baseline row per variant/model/split(F14 대응 최대확률 기준행을 변형/모델/분할별 기록), label/model density split per split(라벨/모델 빈도 분리를 분할별 기록), train-only threshold manifest(학습 전용 임계값 목록)
- success_criteria(성공 기준): primary cell(1순위 칸)이 validation/OOS(검증/표본밖)에서 positive net(양수 순손익), PF >= 1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD <= 15%(손실폭 15% 이하), subperiod DD control(하위기간 손실폭 통제), ONNX parity(온엑스 동등성)를 동시에 만족하면 strict scout clue(엄격 탐색 단서)로 본다.
- failure_criteria(실패 기준): train-only threshold(학습 전용 임계값)이 validation/OOS density(검증/표본밖 빈도)로 전이되지 않거나 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 무너지면 negative memory(부정 기억) 또는 repair(수리) 후보로 기록한다.
- invalid_conditions(무효 조건): validation/OOS PF/net/DD로 threshold(임계값)를 고르거나 바꾸는 경우, 결과를 본 뒤 score contract(점수 계약)나 target density(목표 빈도)를 추가하는 경우, F14 label quota/horizon(라벨 할당/보유기간)을 다시 맞추는 경우
- evidence_plan(근거 계획): score contract manifest(점수 계약 목록), threshold manifest(임계값 목록), argmax baseline metrics(최대확률 기준 지표), model metrics(모델 지표), subperiod metrics(하위기간 지표), ONNX parity(온엑스 동등성)

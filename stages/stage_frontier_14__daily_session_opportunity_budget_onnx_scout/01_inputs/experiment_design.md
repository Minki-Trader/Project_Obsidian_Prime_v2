# Frontier14 Experiment Design(프론티어14 실험 설계)

- hypothesis(가설): US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3클래스 온엑스)는 label wrapping(라벨 감싸기)보다 upstream entry opportunity generation(상류 진입 기회 생성)을 바꾸면 density/PF/DD(빈도/수익 팩터/손실폭) 균형에 가까워질 수 있습니다.
- decision_use(결정 사용): whether to continue upstream opportunity labels(상류 기회 라벨을 계속 밀지)
- comparison_baseline(비교 기준): Reference-only(참조 전용): Frontier13 best sparse row(프론티어13 최상 희소 행) validation/OOS PF-density-DD 1.0397/2.2568/54.3762 and 2.0277/0.4122/5.5735.
- control_variables(통제 변수): same Tier A dataset(동일 티어 A 데이터), same feature order(동일 피처 순서), same fixed model specs(동일 고정 모델 규격), fixed argmax signal contract(고정 최대확률 신호 계약), no post-fit selector or threshold search(적합 후 선택기나 임계값 탐색 없음)
- changed_variables(변경 변수): daily/session quota opportunity label source(일별/세션별 할당 기회 라벨 원천), pre-registered horizon/quota variants(사전 등록 지평/할당 변형)
- sample_scope(표본 범위): Tier A US100 M5 train/validation/OOS fixed split(티어 A US100 5분봉 고정 분할)
- success_criteria(성공 기준): strict scout clue(엄격 탐색 단서): validation and OOS(검증과 표본밖) both positive net(양수 순수익), PF>=1.2(수익 팩터 1.2 이상), density 5~10/day(일 5~10회), DD<=15%(손실폭 15% 이하), controlled subperiod DD(하위기간 손실폭 통제).
- failure_criteria(실패 기준): label quota(라벨 할당량)는 맞지만 model argmax(모델 최대확률)가 density cliff(빈도 절벽), DD explosion(손실폭 폭발), or PF collapse(수익 팩터 붕괴)를 만들면 negative memory(부정 기억).
- invalid_conditions(무효 조건): quota or horizon retuned after seeing validation/OOS metrics(검증/표본밖 지표 본 뒤 할당량/지평 재조정), validation/OOS statistics used to calibrate bucket boundaries(검증/표본밖 통계로 버킷 경계 보정), feature row uses future path information(피처 행이 미래 경로 정보를 사용)
- stop_conditions(중지 조건): strict rows > 0 triggers Grok pre-expensive review(엄격 행이 있으면 비싼 검증 전 그록 검토), strict/preserved rows 0 triggers repair-or-closeout decision(엄격/보존 행 0이면 수리/마감 결정), same quota retuning pressure appears triggers closeout(같은 할당 재조정 압력이 나오면 마감)
- evidence_plan(근거 계획): label density table/model KPI table/ONNX parity/stage ledger/Grok receipts(라벨 빈도표/모델 KPI표/온엑스 동등성/단계 장부/그록 영수증)

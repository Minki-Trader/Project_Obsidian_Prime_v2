# Stage18 Closeout Packet(18단계 종료 묶음)

## Judgment(판정)

- stage(단계): `18_model_family_challenge__catboost_ordered_boosting_scout`
- status(상태): `closed_inconclusive_catboost_model_characteristics_exhausted`
- result subject(결과 대상): CatBoost(`Categorical Boosting`, 범주형 부스팅/캣부스트) ordered boosting(순서형 부스팅) model-family scout(모델군 탐색)
- claim boundary(주장 경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage18(18단계)은 CatBoost(캣부스트) 특성을 충분히 확인했지만, 운영 의미(operating meaning, 운영 의미)는 만들지 않고 닫는다.

## Evidence(근거)

- base packet(기본 묶음): `docs/agent_control/packets/stage18_catboost_characteristic_mt5_kpi_v1/aggregate_summary.json`
- follow-up packet(후속 묶음): `docs/agent_control/packets/stage18_catboost_followup_batch_mt5_kpi_v1/aggregate_summary.json`
- compression packet(압축 묶음): `docs/agent_control/packets/stage18_catboost_compression_mt5_kpi_v1/aggregate_summary.json`
- completed MT5 attempts(완료 MT5 시도): `78`
- MT5 KPI records(MT5 KPI 기록): `190`
- normalized KPI records(정규화 KPI 기록): `190`
- completed run range(완료 실행 범위): `run12A-run12P`

효과(effect, 효과): Python(파이썬) 모델 산출물, ONNX(`Open Neural Network Exchange`, 오픈 뉴럴 네트워크 교환) runtime handoff(런타임 인계), MT5(`MetaTrader 5`, 메타트레이더5) strategy tester(전략 테스터), KPI(`Key Performance Indicator`, 핵심 성과 지표)를 같은 종료 근거로 묶었다.

## Preserved Clues(보존 단서)

- CatBoost(캣부스트)는 long bias(매수 편향)가 뚜렷하다.
- q85 threshold(q85 임계값)와 hold6(6봉 보유)이 가장 깨끗한 압축 축이었다.
- high confidence/high margin(고확신/높은 여백)은 mid confidence/low margin(중간 확신/낮은 여백)보다 낫다.
- low volatility/mid session(저변동성/중반 세션) 단서는 남지만, 교집합 압축은 표본이 작고 drawdown(손실폭)이 크다.
- Plain control(Plain 대조군) 같은 조건 재대결에서는 Ordered(순서형)가 더 낫지만, Ordered(순서형)도 운영 후보로는 약하다.

효과(effect, 효과): 다음 단계는 CatBoost(캣부스트)를 이어받지 않고, 필요한 경우 단서만 비교 문맥(comparison context, 비교 문맥)으로 쓴다.

## Negative Memory(부정 기억)

- q80 density(q80 밀도)는 OOS(표본 밖)에서 좋아 보여도 validation(검증) drawdown(손실폭)이 매우 컸다.
- q85 high-margin low-vol-or-mid-session 압축은 OOS(표본 밖) `100.0 / PF 1.38 / 7 trades / DD 44.19%`로 표본과 위험이 약하다.
- long-only hold6 q85(매수 전용 6봉 q85)는 OOS(표본 밖) `197.5 / PF 1.25 / 275 trades / DD 18.38%`로 가장 깨끗하지만, 이것만으로 Stage19(19단계) 모델 연속성을 만들지 않는다.

효과(effect, 효과): 좋은 숫자를 이유로 Stage18(18단계)을 모델 승격이나 Stage19(19단계) CatBoost continuation(캣부스트 연속 단계)로 끌고 가지 않는다.

## Closeout Rule(종료 규칙)

Stage19(19단계)는 CatBoost(캣부스트) continuation(연속) 단계가 아니다. Stage18(18단계)의 모델, threshold(임계값), selected variant(선택 변형), runtime files(런타임 파일)는 Stage19-25(19-25단계)에 상속하지 않는다.

효과(effect, 효과): Stage19-25(19-25단계)는 새 model-family question(모델군 질문)으로 시작하며, Stage18(18단계)은 comparison clue(비교 단서)와 failure memory(실패 기억)만 제공한다.

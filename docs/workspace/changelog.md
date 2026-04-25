# Workspace Changelog

## 2026-04-24

- 깨끗한 단계 재시작(clean stage restart, 깨끗한 단계 재시작)을 만들었다.
- `.agents/skills`, `docs/contracts`, 개념 노트(concept notes, 개념 노트), 데이터(data, 데이터), 재사용 foundation 도구(reusable foundation tools, 재사용 기반 도구)를 보존했다.
- 오래된 Stage 00부터 Stage 07까지의 이력(history, 이력)을 현재 단계 진실(current stage truth, 현재 단계 진실)에서 제거했다.
- `Tier A(티어 A)`와 `Tier B(티어 B)`를 둘 다 완전히 탐색 가능한 표본 라벨(sample label, 표본 라벨)로 다시 정의했다.
- 첫 단계(first stage, 첫 단계)로 `01_data_foundation__raw_m5_inventory`를 열었다.
- `20260424_raw_m5_inventory` 실행(run, 실행)으로 원천 `M5` 재고(raw M5 inventory, 원천 M5 재고)를 확인했다. 예상 심볼(expected symbols, 예상 심볼) 12개가 모두 사용 가능했고, 공통 사용 창(common usable window, 공통 사용 기간)은 `2022-08-01T16:35:00Z`부터 `2026-04-13T22:55:00Z`까지다.
- `20260424_time_semantics_probe` 실행(run, 실행)으로 원천 timestamp(타임스탬프)가 직접 UTC(direct UTC, 직접 협정세계시)로는 미국 주식 정규장과 맞지 않고, 브로커/서버 시계 후보(broker/server clock candidate, 브로커/서버 시계 후보)에 가깝다는 근거를 남겼다.
- `2026-04-24_stage01_timestamp_policy` 결정(decision, 결정)으로 이중 시간축 정책(dual time axis policy, 이중 시간축 정책)을 채택했다. 원천 정렬(alignment, 정렬)은 브로커 시계 키(broker-clock key, 브로커 시계 키)를 쓰고, 세션 피처(session features, 세션 피처)는 검증된 이벤트 UTC(event UTC, 이벤트 UTC) 또는 브로커 세션 달력(broker session calendar, 브로커 세션 달력)이 필요하다.
- `20260424_broker_session_calendar_mapper` 실행(run, 실행)으로 `Europe/Athens` 브로커 시계(broker clock, 브로커 시계)에서 `America/New_York` 세션 시간(session time, 세션 시간)으로 가는 매퍼(mapper, 매퍼)를 만들고 검토했다.
- 외부 검증 지연 방지(External Verification Anti-Deferral, 외부 검증 지연 방지) 규칙을 추가했다. 효과(effect, 효과)는 MT5(`MetaTrader 5`, 메타트레이더5), 전략 테스터(strategy tester, 전략 테스터), 런타임 동등성(runtime parity, 런타임 동등성)이 필요한 주장을 다음 작업(next work, 다음 작업)으로 반복해서 미루지 못하게 하는 것이다.
- `20260424_feature_frame_target_probe` 실행(run, 실행)으로 첫 clean feature frame target(첫 깨끗한 피처 프레임 목표)을 `practical_start_full_cash_day_valid_rows_only`로 선택했다.
- Stage 01(1단계)을 닫고 `02_feature_frame__practical_full_cash_freeze`를 열었다. 효과(effect, 효과)는 첫 shared freeze(공유 동결 산출물)를 실제로 물질화할 단계가 분명해졌다는 것이다.
- `20260424_practical_full_cash_freeze_materialization` 실행(run, 실행)으로 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 실제로 만들었다. 데이터셋 ID(dataset ID, 데이터셋 ID)는 `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`이고, 선택 행(selected rows, 선택 행)은 `54439`다.
- Stage 02(2단계)를 닫고 `03_training_dataset__label_split_contract`를 열었다. 효과(effect, 효과)는 이제 라벨(label, 라벨)과 분할(split, 분할)을 실제 공유 동결 산출물 위에서 정할 수 있다는 것이다.
- agent guard(에이전트 가드)와 policy routing(정책 라우팅)을 단순화했다. 효과(effect, 효과)는 낡은 stage ownership(단계 소유권) 문구를 제거하고, claim discipline(주장 규율)을 공식 라우팅에 남기며, agent settings validator(에이전트 설정 검사기)가 `openai.yaml`의 필수 설명을 확인하게 된 것이다.
- 답변 명확성(answer clarity, 답변 명확성), 코드 품질(code quality, 코드 품질), workflow drift guard(작업 드리프트 가드), reference scout(참고자료 탐색) 스킬을 추가했다. 효과(effect, 효과)는 Codex 답변, 구현 품질, 막힘 상황 분류, 외부 사용법 확인을 더 직접적으로 다루는 것이다.
- workflow drift guard(작업 드리프트 가드)에 material recovery order(재료 복구 순서)를 추가했다. 효과(effect, 효과)는 필요한 재료가 없을 때 외부/레거시를 기본 대체 경로로 쓰지 않고, 현재 프로젝트 안에서 복구 또는 재생성할 수 있는지 먼저 확인하게 하는 것이다.
- workflow drift guard(작업 드리프트 가드)에 recovery action rule(복구 행동 규칙)을 추가했다. 효과(effect, 효과)는 Codex가 직접 풀 수 있는 blocker(차단 지점)는 직접 풀고, 사용자 협조가 필요한 경우에는 정확한 요청과 복귀 지점을 남기게 하는 것이다.

## 2026-04-25

- `20260425_label_v1_fwd12_split_v1_materialization` 실행(run, 실행)으로 첫 training label(학습 라벨)과 split contract(분할 계약)를 물질화했다. 효과(effect, 효과)는 첫 model training(모델 학습) 또는 alpha exploration(알파 탐색)에 필요한 기본 정답지와 분할이 생겼다는 것이다.
- 첫 training dataset(학습 데이터셋)은 `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`에 있다. 행 수(rows, 행 수)는 `46650`이고, train/validation/OOS(학습/검증/표본외)는 `29222/9844/7584`다.
- 다만 바로 alpha/model exploration(알파/모델 탐색)을 열지는 않는다. `placeholder_equal_weight(임시 동일가중)` 월별 top3 weights(월별 top3 가중치)는 먼저 격리했고, 정식 pre-alpha(알파 전) 경로는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)와 58 feature(58개 피처) 입력으로 다시 닫는다.
- Stage 03(3단계)을 Stage 04(4단계) model-input readiness(모델 입력 준비도)로 인계했다. 효과(effect, 효과)는 label/split(라벨/분할) 작업과 입력 준비도 작업을 분리한 것이다.
- `20260425_model_input_feature_set_v1_no_placeholder_top3_weights` 실행(run, 실행)으로 56 feature(56개 피처) interim model input dataset(임시 모델 입력 데이터셋)을 물질화했다. 효과(effect, 효과)는 `placeholder_equal_weight(임시 동일가중)`에 의존하는 `top3_weighted_return_1`, `us100_minus_top3_weighted_return_1`을 임시 입력에서 격리한 것이다.
- interim model input dataset(임시 모델 입력 데이터셋)은 `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet`에 있다. 행 수(rows, 행 수)는 `46650`, 포함 feature(피처)는 `56`, included feature order hash(포함 피처 순서 해시)는 `84f313815393429acb9690d727b61b4a3dfd2354678bd357a53db570ba37bc89`다.
- pre-alpha stage queue(알파 전 단계 대기열)를 Stage 04~09(4~9단계)로 고정했다. 효과(effect, 효과)는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치), feature integrity audit(피처 무결성 감사), Python/MT5 parity(파이썬/MT5 동등성), baseline smoke training(기준선 스모크 학습), alpha protocol(알파 규칙), registry handoff(등록부 인계)가 서로 섞이지 않게 하는 것이다.
- raw data integration tests(원천 데이터 통합 테스트)를 `OBSIDIAN_RUN_SLOW_TESTS=1` opt-in(명시 선택)으로 분리했다. 효과(effect, 효과)는 기본 `unittest discover`(단위 테스트 발견)가 timeout(시간 초과) 없이 빠른 검증으로 끝나고, 전체 원천 데이터 검증은 별도로 실행되는 것이다.
- `20260425_top3_price_proxy_weights_v1` 실행(run, 실행)으로 `MSFT`, `NVDA`, `AAPL`의 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 물질화했다. 효과(effect, 효과)는 외부 구독 데이터(external subscription data, 외부 구독 데이터) 없이 로컬 MT5 raw bars(원천 봉 데이터)만으로 top3 가중치 피처를 재계산할 수 있다는 것이다.
- 새 가중치 표(weight table, 가중치 표)는 `foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv`에 있다. month coverage(월별 범위)는 `2022-08`~`2026-04`, bootstrap month(초기 월)는 `2022-08`, weights sha256(가중치 해시)은 `08531dbf5235a166e5b2e9dc675ec3d41a0cc84066d00592c37f500aa8f89981`이다.
- 이 가중치는 actual NDX/QQQ weights(실제 NDX/QQQ 가중치), QQQ holdings weights(QQQ 보유비중), market cap(시가총액), float(유동주식수)를 반영하지 않는다고 계약(contract, 계약)에 명시했다. 효과(effect, 효과)는 대리값(proxy, 대리값)을 운영 의미(operational meaning, 운영 의미)로 잘못 승격하지 않게 하는 것이다.
- `20260425_model_input_feature_set_v2_mt5_price_proxy_58` 실행(run, 실행)으로 58 feature(58개 피처) model input(모델 입력)을 물질화했다. 효과(effect, 효과)는 `top3_weighted_return_1`, `us100_minus_top3_weighted_return_1`이 MT5 price-proxy weights(MT5 가격 대리 가중치)로 복구된 것이다.
- Stage 04(4단계)를 `reviewed_closed_handoff_to_stage05_complete`로 닫고 Stage 05(5단계) `05_feature_integrity__formula_time_alignment_leakage_audit`를 열었다. 효과(effect, 효과)는 이제 학습 전에 feature/time/external/label audit(피처/시간/외부/라벨 감사)을 진행할 수 있다는 것이다.
- `20260425_stage05_feature_integrity_audit_v1` 실행(run, 실행)으로 Stage 05(5단계) 통합 감사(integrated audit, 통합 감사)를 완료했다. 공식(formula, 공식), 시간/세션(time/session, 시간/세션), 외부 정렬(external alignment, 외부 정렬), 라벨 누수(label leakage, 라벨 누수)가 통과했다.
- Stage 05(5단계)를 `reviewed_closed_handoff_to_stage06_complete`로 닫고 Stage 06(6단계) `06_runtime_parity__python_mt5_runtime_authority`를 열었다. 효과(effect, 효과)는 감사된 58 feature(58개 피처) 입력을 Python/MT5 parity(파이썬/MT5 동등성) 검증으로 넘기는 것이다.
- `obsidian-answer-clarity(답변 명확성)` 트리거(trigger, 작동 조건)를 계획 세우기(planning, 계획)와 결과 보고(result report, 결과 보고)에 강하게 걸었다. 효과(effect, 효과)는 사용자 보고가 파일 목록이나 명령 로그보다 결론, 현재 의미, 아직 아닌 것, 다음 행동을 먼저 말하게 하는 것이다.
- `20260425_stage06_runtime_parity_blocked_v1` 실행(run, 실행)으로 Stage 06(6단계) runtime parity(런타임 동등성)를 blocked handoff(차단 인계)로 처리했다. Python snapshot(파이썬 스냅샷), fixture set(표본 묶음), MT5 handoff package(MT5 인계 묶음)를 만들고 MetaEditor compile(메타에디터 컴파일)을 `0 errors, 0 warnings(오류 0, 경고 0)`로 확인했다.
- Stage 06(6단계)은 runtime authority(런타임 권위)를 닫지 않는다. 효과(effect, 효과)는 MT5 snapshot(MT5 스냅샷) 없음과 stale equal-weight MT5 audit tools(낡은 동일가중 MT5 감사 도구)를 다음 작업으로 흐리지 않고 명시적 blocker(차단 사유)로 남긴 것이다.
- `20260425_stage06_runtime_parity_closed_v1` 실행(run, 실행)으로 Stage 06(6단계) runtime parity(런타임 동등성)를 닫았다. 효과(effect, 효과)는 MT5 price-proxy weights(MT5 가격 대리 가중치)를 쓰는 현재 MT5 audit tool(MT5 감사 도구), MetaEditor compile(메타에디터 컴파일), strategy tester execution(전략 테스터 실행), MT5 snapshot(MT5 스냅샷), Python/MT5 comparison(파이썬/MT5 비교)을 한 실행 근거로 묶은 것이다.
- Stage 06(6단계)의 closed run(폐쇄 실행)은 `5` Python snapshot rows(파이썬 스냅샷 행)와 `5` MT5 snapshot rows(MT5 스냅샷 행)를 비교했고, max abs diff(최대 절대 차이)는 `0.0000017512503873717833`로 tolerance(허용오차) `0.00001` 안에 있었다. 효과(effect, 효과)는 이전 blocked handoff(차단 인계)를 superseded evidence(대체된 근거)로 낮추는 것이다.
- Stage 07(7단계) `07_model_training_baseline__contract_preprocessing_smoke`를 열었다. 효과(effect, 효과)는 Python-side preprocessing policy(파이썬 측 전처리 정책), training run contract(학습 실행 계약), baseline smoke training(기준선 스모크 학습)을 시작하되 MT5 runtime authority(MT5 런타임 권위)를 전제하지 않는 것이다.
- code-writing auto subagent pair(코드 작성 자동 서브에이전트 묶음)를 추가했다. 효과(effect, 효과)는 Python(파이썬), MQL5, pipeline(파이프라인), test(테스트), runtime helper(런타임 도구) 작성 전에 `obsidian-code-surface-guard(코드 표면 가드)`와 `obsidian-reference-scout(레퍼런스 탐색)`이 선행 관문(precheck gate, 사전확인 관문)으로 작동하게 하는 것이다.
- work auto subagent bundles(작업 자동 서브에이전트 묶음)를 추가했다. 효과(effect, 효과)는 run evidence(실행 근거), stage transition(단계 전환), policy/skill/settings(정책/스킬/설정), user report(사용자 보고), lane/gate(레인/게이트), blocker recovery(차단 복구), code quality(코드 품질) 작업에 필요한 서브에이전트(subagent, 서브에이전트)를 자동 라우팅 규칙으로 남기는 것이다.
- pre-block recovery hardening(차단 전 복구 강화)을 추가했다. 효과(effect, 효과)는 external verification(외부 검증)이나 MT5 runtime output(MT5 런타임 출력)이 필요한 작업에서 compile-only evidence(컴파일만의 근거)로 멈추지 않고, blocked(차단) 전에 recovery attempt(복구 시도), tool patch(도구 수정), execution attempt(실행 시도), failure log(실패 로그), required user action(필요 사용자 행동)을 남기게 하는 것이다.

# Stage16 QDA Closeout(16단계 QDA 종료)

## Decision(결정)

Stage16(16단계) `16_model_family_challenge__qda_class_covariance_scout`를 `closed_inconclusive_qda_class_covariance_runtime_probe_evidence`로 닫는다.

효과(effect, 효과): QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)의 class-specific covariance(클래스별 공분산) 단서는 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- Stage run count(단계 실행 수): `39`
- stage ledger rows(단계 장부 행): `507`
- MT5 KPI records(MT5 핵심성과지표 기록): `390`
- MT5 runtime attempts(MT5 런타임 시도): `234`
- run08(실행08): `run08A`~`run08J` characterization/runtime_probe(특성 파악/런타임 탐침)
- run09(실행09): `run09A`~`run09Q` regularization/feature/sample/coverage follow-up(정규화/피처/표본/커버리지 후속 탐색)
- run10(실행10): `run10A`~`run10L` decision microprobe(결정 미세 탐침)
- closeout decision(종료 결정): `docs/decisions/2026-05-03_stage16_qda_closeout_stage17_open.md`
- stage ledger(단계 장부): `stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/stage_run_ledger.csv`

효과(effect, 효과): Python(파이썬) 구조 판독과 MT5(메타트레이더5) KPI(핵심성과지표)를 같은 경계 안에서 읽는다.

## Preserved Clues(보존 단서)

- `run10I` drop_mega10(대형주 10개 제거) reg0.20(정규화 0.20)은 validation/OOS(검증/표본외)가 둘 다 양수였고 OOS drawdown(표본외 손실)도 통제됐다.
- `run10B` full58(전체 58개 피처) reg0.18(정규화 0.18)은 OOS(표본외) 순수익이 최고였지만 validation(검증)이 음수라 spike clue(튀는 성과 단서)로만 보존한다.
- `run09G` drop_mega10(대형주 10개 제거)은 `run09D` full58(전체 58개 피처)보다 균형적이었지만 run10(실행10)에서 반복 생존이 충분하지 않았다.

효과(effect, 효과): 다음 단계에서 QDA(이차 판별 분석)를 다시 열더라도 같은 단일 분할(single split, 단일 분할) 미세 조정을 반복하지 않는다.

## Negative Memory(부정 기억)

- full58(전체 58개 피처) reg0.18(정규화 0.18)의 OOS(표본외) 강함은 validation(검증) 안정성으로 반복되지 않았다.
- drop_mega10(대형주 10개 제거)은 하나의 strong survivor(강한 생존 표면)만 남겼다.
- sample size axis(표본 크기 축)와 coverage threshold(커버리지 임계값)는 Stage16(16단계) 안에서 alpha quality(알파 품질)로 올릴 만큼 안정적이지 않았다.

## Reopen Condition(재개 조건)

새 label/horizon(라벨/예측수평선), WFO(`walk-forward optimization`, 워크포워드 최적화), 또는 다른 context/model(문맥/모델)에서 QDA(이차 판별 분석)나 drop_mega10(대형주 10개 제거)이 인접 설정 두 개 이상으로 validation/OOS(검증/표본외) 동시 생존할 때만 Stage17+(17단계 이후)에서 다시 판다.

## Forbidden Claims(금지 주장)

- edge(거래 우위)
- alpha quality(알파 품질)
- selected baseline(선택 기준선)
- promotion candidate(승격 후보)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)

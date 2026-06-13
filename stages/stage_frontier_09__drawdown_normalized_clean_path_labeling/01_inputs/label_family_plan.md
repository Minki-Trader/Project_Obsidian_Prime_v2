# Frontier09 Label Family Plan(전선09 라벨 가족 계획)

## Families(가족)

- payoff_adverse_ratio(수익/불리 이동 비율): F07 mae_mfe_balance(전선07 MFE/MAE 균형)는 target/cap(목표/상한) 중심이고, F09는 payoff divided by adverse burden(수익을 불리 부담으로 나눈 효율) 중심이다.
- underwater_burden(수중 부담): F07 time_to_adverse_penalty(전선07 불리 이동 속도 벌점)는 초기 불리 이동 속도이고, F09는 horizon adverse-bar count(수평선 내 불리 봉 수)와 burden ratio(부담 비율)를 직접 제한한다.
- clean_recovery(깨끗한 회복): F07 recovery_close_survival(전선07 종가 회복 생존)은 회복+상한이고, F09는 close return plus MFE capture efficiency(종가 수익 + 최대 유리 이동 포착 효율)를 함께 요구한다.

## Leakage Guard(누수 보호)

Action(행동): threshold/scale(임계값/스케일)은 train split(학습 분할)에서만 fit(적합)합니다.

Effect(효과): validation/OOS(검증/표본밖)는 label application/evaluation(라벨 적용/평가) 전용으로 남습니다.

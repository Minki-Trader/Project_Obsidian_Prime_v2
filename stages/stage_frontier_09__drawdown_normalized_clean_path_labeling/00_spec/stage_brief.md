# Frontier09 Stage Brief(전선09 단계 개요)

Stage id(단계 ID): `stage_frontier_09__drawdown_normalized_clean_path_labeling`

Question(질문): Can drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)이 fixed ONNX(고정 온엑스) 3-class interface(3분류 인터페이스)에서 DD/curve quality(손실폭/곡선 품질)를 직접 더 잘 배우게 하는가?

Hypothesis(가설): drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)이 future return(미래 수익), adverse excursion(불리 이동), payoff/adverse ratio(수익/불리 이동 비율), underwater burden(수중 부담), clean-close recovery(깨끗한 종가 회복)를 함께 반영하면 fixed 3-class ONNX interface(고정 3분류 온엑스 인터페이스)가 DD/curve quality(손실폭/곡선 품질)를 더 직접 배울 수 있다.

Novelty delta(신규성 차이): Frontier08(전선08)은 same labels plus sample weighting(동일 라벨 + 표본 가중)을 바꿨고, Frontier09(전선09)는 target representation(목표 표현)을 바꿔 bad-path rows(나쁜 경로 행)를 flat/no-trade(관망/무거래)로 만든다.

## Difference From Frontier07(전선07 대비 차이)

- payoff_adverse_ratio(수익/불리 이동 비율): F07 mae_mfe_balance(전선07 MFE/MAE 균형)는 target/cap(목표/상한) 중심이고, F09는 payoff divided by adverse burden(수익을 불리 부담으로 나눈 효율) 중심이다.
- underwater_burden(수중 부담): F07 time_to_adverse_penalty(전선07 불리 이동 속도 벌점)는 초기 불리 이동 속도이고, F09는 horizon adverse-bar count(수평선 내 불리 봉 수)와 burden ratio(부담 비율)를 직접 제한한다.
- clean_recovery(깨끗한 회복): F07 recovery_close_survival(전선07 종가 회복 생존)은 회복+상한이고, F09는 close return plus MFE capture efficiency(종가 수익 + 최대 유리 이동 포착 효율)를 함께 요구한다.

Next run(다음 실행): `frontier09B_drawdown_clean_path_label_proxy_scout_v1`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

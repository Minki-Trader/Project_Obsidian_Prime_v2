# Selective Probability Abstention Signal Contract Plan(선택적 확률 기권 신호 계약 계획)

Frontier06B(전선06B)는 model probabilities(모델 확률)를 probability truth(확률 진실)로 주장하지 않고, ranking score(순위 점수)로만 씁니다.

Rules(규칙):

- train split(학습 분할)에서만 threshold(임계값)를 정합니다.
- validation/OOS(검증/표본밖)는 evaluation only(평가 전용)입니다.
- signal(신호)은 p_short/p_long(숏/롱 확률), side margin(방향 마진), p_flat veto(플랫 차단)만 사용합니다.
- future return(미래 수익), realized PnL(실현 손익), validation/OOS label outcome(검증/표본밖 라벨 결과)은 entry rule(진입 규칙)에 쓰지 않습니다.

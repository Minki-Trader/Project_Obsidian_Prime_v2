# Regime Label Contract(레짐 라벨 계약)

Action(행동): Frontier13B(프론티어13B)는 closed-bar regime features(확정 봉 레짐 피처)로 train-only buckets(학습 전용 버킷)을 만들고, 각 bucket(버킷)의 path scale(경로 척도)을 학습 구간에서만 계산합니다.

Effect(효과): validation/OOS(검증/표본밖) 성과를 본 뒤 threshold(임계값)를 맞추는 hidden search(숨은 탐색)를 막습니다.

Allowed regime inputs(허용 레짐 입력):

- is_us_cash_open
- is_first_30m_after_open
- is_last_30m_before_cash_close
- atr_14_over_atr_50
- di_spread_14
- bb_squeeze

Forbidden(금지):

- validation/OOS-driven bucket edits(검증/표본밖 기반 버킷 수정)
- class-weight density forcing(클래스 가중 빈도 강제)
- threshold micro-search(임계값 미세 탐색)
- selected baseline inheritance(선택 기준선 상속)

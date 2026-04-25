# Review Index

## 현재 판독(Current Read, 현재 판독)

Stage 03(3단계)는 첫 training label(학습 라벨)과 split contract(분할 계약)를 물질화했고 Stage 04(4단계)로 handoff(인계)됐다.

- review(검토): `stages/03_training_dataset__label_split_contract/03_reviews/first_training_label_split_contract_review.md`
- run(실행): `stages/03_training_dataset__label_split_contract/02_runs/20260425_label_v1`

## 다음 검토(Next Review, 다음 검토)

다음 검토(review, 검토)는 Stage 04(4단계) model-input readiness(모델 입력 준비도)를 대상으로 한다.

`placeholder_equal_weight(임시 동일가중)` 월별 top3 weights(월별 top3 가중치)는 56 feature(56개 피처) interim model input(임시 모델 입력)에서만 격리됐다.

정식 pre-alpha(알파 전) 경로는 Stage 04(4단계)에서 real monthly top3 weights(진짜 월별 top3 가중치)를 만들고 58 feature(58개 피처) model input(모델 입력)을 다시 물질화해야 한다. 이후 Stage 05~09(5~9단계) pre-alpha queue(알파 전 대기열)를 따른다.

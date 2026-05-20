# Stage267 Equity Curve Shape Grading(267단계 평가금 곡선 형태 판정)

- run(실행): `run267B_stage267_extended_period_ablation_probe_v1`
- status(상태): `equity_curve_shape_grading_completed_partial`
- judgment(판정): `not_enough_for_candidate_selection`
- claim_boundary(주장 경계): `research_development_only_no_selected_candidate_no_onnx_until_goal_gate`

## What Was Done(수행 내용)

Action(행동): run267B(267B 실행)의 equity report manifest(평가금 보고서 목록)에 있는 10개 MT5 report(메타트레이더5 보고서)를 다시 읽고, HTML 거래표의 balance path(잔액 경로)에서 curve shape KPI(곡선 형태 핵심 지표)를 계산했다.

Effect(효과): 숫자 PF(수익 팩터)만 보지 않고, final below peak(마지막 고점 이탈), path drawdown(경로 손실폭), worst month(최악 월), early/late third net(초반/후반 1/3 순수익), underwater stretch(회복 전 체류 길이)를 후보별로 같이 보게 했다.

## Main Read(핵심 판독)

아직 “기깔난” 곡선은 없다.

- 모든 후보/split(후보/분할)이 `B_shape_watch`다.
- 모든 후보/split(후보/분할)이 final below peak(마지막 고점 이탈) `3%` 이상이다.
- `s258_short_tight_control` OOS(표본외)는 net profit(순수익) `950.22`로 가장 크지만, max balance drawdown(최대 잔액 손실폭) `11.8815%`, final below peak(마지막 고점 이탈) `6.8228%`, worst month(최악 월) `2026.04=-81.56`로 가장 불편하다.
- `s262_lowrank_inner_half_filter` validation(검증)은 net profit(순수익) `1336.78`, PF(수익 팩터) `1.6156`로 편하지만 OOS net(표본외 순수익)은 `745.71`이라 확장성은 아직 약하다.
- `s264_allow_inner_high_quarter` OOS(표본외)는 net profit(순수익) `857.67`, PF(수익 팩터) `1.7354`로 좋지만 2026.04(2026년 4월) `-41.14`와 final below peak(마지막 고점 이탈) `4.4507%`가 남는다.

## Candidate Role Update(후보 역할 갱신)

- `s264_allow_inner_high_quarter`: challenger(도전자) 유지. 다만 OOS final month(표본외 마지막 달)와 고점 이탈을 다음 검증에서 확대해야 한다.
- `s264_lowrank_control`: defensive control(방어 기준) 유지. validation(검증)은 편하지만 OOS(표본외) 회복력은 낮다.
- `s262_lowrank_inner_half_filter`: validation-heavy(검증 중심) 유지. validation curve(검증 곡선)는 가장 편한 쪽이지만 OOS expansion(표본외 확장) 약점이 남는다.
- `s264_allow_inner_all_oos_anchor`: OOS anchor(표본외 앵커) 유지. validation(검증) 손상과 2025.05 negative month(음수 월)가 있다.
- `s258_short_tight_control`: stress challenger(압박 도전자)로만 유지. OOS net(표본외 순수익)은 크지만 DD(손실폭), final peak gap(마지막 고점 이탈), 2026.04 손상이 크다.

## Boundary(경계)

이 판정은 first-pass balance path grading(1차 잔액 경로 판정)이다.
Effect(효과): 후보를 선택하지 않고, 다음 실행에서 full/zoom visual review(전체/확대 시각 검토), 2024 historical stress(2024 과거 압박), feature ablation(피처 제거), similar replacement(유사 대체)를 어디에 집중할지 좁힌다.

Selected candidate(선택 후보), selected baseline(선택 기준선), ONNX readiness(ONNX 준비), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.

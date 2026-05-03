# 2026-05-03 Stage16 QDA Run10 Decision Microprobe(16단계 QDA 실행10 결정 미세 탐침)

## Decision(결정)

`run10A`~`run10L` QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) decision microprobe(결정 미세 탐침)를 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)까지 실행했다.

- recommendation(권고): `close_stage16_preserve_qda_clues`
- reason(이유): 좋은 OOS(표본외) 숫자가 단일 지점에 치우쳤거나 validation(검증) 안정성이 충분히 반복되지 않았다.
- selected current run(선택 현재 실행): `run10B_qda_reg018_full58_resample_decision_microprobe_v1`

효과(effect, 효과): close(닫기)라면 QDA(이차판별분석)는 보존 단서로 남기고 다음 stage topic(단계 주제)로 이동한다. continue(진행)라면 같은 계열을 context/WFO(문맥/워크포워드) 쪽으로 한 번 더 좁힌다.

## Boundary(경계)

`qda_run10_decision_microprobe_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

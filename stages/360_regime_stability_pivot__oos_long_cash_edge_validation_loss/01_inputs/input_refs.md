# Stage360 Input References(360단계 입력 참조)

Action(행동): Stage359C review artifacts(359C 검토 산출물)를 Stage360(360단계)의 source inputs(원천 입력)으로 고정한다.

Effect(효과): 다음 run(실행)이 오래된 Stage359 context(359단계 문맥)를 다시 읽지 않아도 필요한 clue/constraint(단서/제약)를 확인할 수 있다.

| role(역할) | path(경로) | boundary(경계) |
|---|---|---|
| final decision(최종 결정) | `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359C/final_decision.json` | reviewed runtime probe(검토된 런타임 탐침) |
| review report(검토 보고서) | `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/03_reviews/run359C_high_density_label_pivot_mt5_probe_review.md` | KPI/attribution(핵심 성과 지표/귀속) |
| segment attribution(구간 귀속) | `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359C/trade_level_segment_attribution.csv` | side/session clue(방향/세션 단서) |
| cost sensitivity(비용 민감도) | `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359C/cost_drag_sensitivity.csv` | cost stress constraint(비용 압박 제약) |
| proxy-MT5 diff(프록시-MT5 차이) | `stages/359_runtime_probe_execution__high_density_label_pivot_mt5_check/02_runs/run359B/proxy_mt5_runtime_difference.csv` | parity/diff evidence(동등성/차이 근거) |

See manifest(목록): `stages/360_regime_stability_pivot__oos_long_cash_edge_validation_loss/01_inputs/stage360_input_manifest.csv`.

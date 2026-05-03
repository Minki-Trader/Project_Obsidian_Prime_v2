# Stage16 QDA RUN10A-RUN10L Decision Microprobe(16단계 QDA 실행 10A-10L 결정 미세 탐침)

- judgment(판정): `inconclusive_qda_run10_decision_microprobe_mt5_completed`
- recommendation(권고): `close_stage16_preserve_qda_clues`
- reason(이유): 좋은 OOS(표본외) 숫자가 단일 지점에 치우쳤거나 validation(검증) 안정성이 충분히 반복되지 않았다.
- completed runs(완료 실행): `12/12`
- MT5 KPI records(MT5 핵심성과지표 기록): `120`
- normalized KPI records(정규화 KPI 기록): `120`
- trade attribution records(거래 귀속 기록): `72`
- comparison reference(비교 참고): `run09D_qda_reg018_full58_followup_v1`
- boundary(경계): `qda_run10_decision_microprobe_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

| run(실행) | family(계열) | topic(주제) | reg(정규화) | q(분위수) | features(피처) | val net/PF/trades(검증) | oos net/PF/trades/DD/RF(표본외) | strong(강한 생존) |
|---|---|---|---:|---:|---:|---:|---:|---|
| `run10A` | `full58_reg018_neighborhood` | `full58_reg016_q90` | `0.16` | `0.9` | `58` | `-74.43/0.96/355` | `-67.29/0.94/219/257.07/-0.26` | `False` |
| `run10B` | `full58_reg018_neighborhood` | `full58_reg018_resample_q90` | `0.18` | `0.9` | `58` | `-29.59/0.98/332` | `338.86/1.29/286/217.94/1.55` | `False` |
| `run10C` | `full58_reg018_neighborhood` | `full58_reg020_q90` | `0.2` | `0.9` | `58` | `-490.31/0.76/368` | `-185.28/0.87/296/275.55/-0.67` | `False` |
| `run10D` | `full58_reg018_neighborhood` | `full58_reg018_q88` | `0.18` | `0.88` | `58` | `-390.84/0.82/431` | `-238.26/0.85/319/269.71/-0.88` | `False` |
| `run10E` | `full58_reg018_neighborhood` | `full58_reg018_q92` | `0.18` | `0.92` | `58` | `-175.09/0.89/341` | `169.02/1.19/216/132.97/1.27` | `False` |
| `run10F` | `drop_mega10` | `drop_mega10_reg012_q90` | `0.12` | `0.9` | `48` | `-92.25/0.94/350` | `216.36/1.2/285/212.39/1.02` | `False` |
| `run10G` | `drop_mega10` | `drop_mega10_reg015_resample_q90` | `0.15` | `0.9` | `48` | `-95.49/0.94/294` | `-39.13/0.96/225/290.47/-0.13` | `False` |
| `run10H` | `drop_mega10` | `drop_mega10_reg018_q90` | `0.18` | `0.9` | `48` | `-160.69/0.9/312` | `-117.51/0.9/236/187.88/-0.63` | `False` |
| `run10I` | `drop_mega10` | `drop_mega10_reg020_q90` | `0.2` | `0.9` | `48` | `140.92/1.14/168` | `219.31/1.4/140/93.7/2.34` | `True` |
| `run10J` | `drop_mega10` | `drop_mega10_reg015_q85` | `0.15` | `0.85` | `48` | `-292.97/0.86/391` | `180.77/1.15/286/172.93/1.05` | `False` |
| `run10K` | `drop_mega10` | `drop_mega10_reg015_q93` | `0.15` | `0.93` | `48` | `-232.04/0.77/124` | `-229.94/0.7/128/276.3/-0.83` | `False` |
| `run10L` | `drop_mega10` | `drop_mega10_reg018_q88` | `0.18` | `0.88` | `48` | `-263.06/0.85/337` | `142.39/1.13/255/163.36/0.87` | `False` |

- best OOS routed net(최고 표본외 라우팅 순수익): `run10B` `full58_reg018_resample_q90` `338.86`
- best validation routed net(최고 검증 라우팅 순수익): `run10I` `drop_mega10_reg020_q90` `140.92`
- survivors by family(계열별 강한 생존): `{"drop_mega10": ["run10I_qda_reg020_drop_mega10_decision_microprobe_v1"]}`

효과(effect, 효과): 이 묶음은 QDA(이차판별분석) Stage16(16단계)을 더 밀지 닫을지 정하기 위해 같은 계열의 반복 생존 여부만 본다.

금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).

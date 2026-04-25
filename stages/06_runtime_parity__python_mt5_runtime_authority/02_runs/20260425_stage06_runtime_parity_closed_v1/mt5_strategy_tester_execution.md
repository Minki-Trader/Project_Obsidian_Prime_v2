# MT5 Strategy Tester Execution

- run_id(실행 ID): `20260425_stage06_runtime_parity_closed_v1`
- terminal(터미널): `C:\Program Files\MetaTrader 5\terminal64.exe`
- config(설정 파일): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\Common\Files\Project_Obsidian_Prime_v2\runtime_parity\20260425_stage06_runtime_parity_closed_v1\mt5_strategy_tester_stage06_closed.ini`
- set file(세트 파일): `C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\ObsidianPrimeStage06Closed.set`
- expert(전문가 자문): `Experts\Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeParityAuditEA.ex5`
- symbol/timeframe(심볼/시간프레임): `US100`, `M5`
- tester range(테스터 범위): `2025.03.03` to `2025.03.04`
- output(출력): `stages/06_runtime_parity__python_mt5_runtime_authority/02_runs/20260425_stage06_runtime_parity_closed_v1/mt5_feature_snapshot.jsonl`

## 결과(Result, 결과)

MT5 strategy tester(전략 테스터)가 current Stage 06 inputs(현재 6단계 입력)로 실행됐고, `5` row(행)의 MT5 snapshot(MT5 스냅샷)을 작성했다.

효과(effect, 효과): Stage 06(6단계)은 MetaEditor compile(메타에디터 컴파일)만으로 닫은 것이 아니라, 실제 tester execution(테스터 실행)과 file handoff(파일 인계)를 통해 닫았다.

## 로그 요약(Log Summary, 로그 요약)

- `automatical testing started`
- `InpOutputPath=Project_Obsidian_Prime_v2/runtime_parity/20260425_stage06_runtime_parity_closed_v1/mt5_feature_snapshot.jsonl`
- `InpTargetWindowsUtc=2025.03.03 18:30:00;2024.06.10 16:35:00;2024.03.11 16:40:00;2025.01.02 17:30:00`
- `Captured runtime parity window 2024.06.10 16:35:00 (1/4).`
- `Captured runtime parity window 2024.03.11 16:40:00 (2/4).`
- `Captured runtime parity window 2025.01.02 17:30:00 (3/4).`
- `Captured runtime parity window 2025.03.03 18:30:00 (4/4).`
- `ObsidianPrimeV2_RuntimeParityAudit wrote 5 line(s) to Project_Obsidian_Prime_v2/runtime_parity/20260425_stage06_runtime_parity_closed_v1/mt5_feature_snapshot.jsonl`
- `Test passed in 0:00:02.184`

## 경계(Boundary, 경계)

이 문서는 execution evidence(실행 근거)다. model quality(모델 품질), alpha quality(알파 품질), operating promotion(운영 승격)을 주장하지 않는다.

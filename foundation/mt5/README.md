# MT5

Put shared MT5-facing runtime helpers, templates, or integration notes here when they are reusable across stages.

## Module Layout(모듈 배치)

이 폴더(folder, 폴더)는 MT5(`MetaTrader 5`, 메타트레이더5) 실행(execution, 실행), 검증(verification, 검증), EA(`Expert Advisor`, 전문가 자문) 모듈(module, 모듈)을 담는다.

- `ObsidianPrimeV2_RuntimeProbeEA.mq5`: Stage 10+(10단계 이후) runtime probe(런타임 탐침)에 쓰는 얇은 공용 EA entrypoint(진입점)이다.
- `ObsidianPrimeV2_RuntimeParityAudit*.mq5`: Stage 06(6단계) runtime parity(런타임 동등성) audit tool(감사 도구)이다.
- `include/ObsidianPrime/`: 앞으로 재사용할 `.mqh` 모듈(module, 모듈)의 소유 위치(owner location, 소유 위치)다.
- 얇은 EA entrypoint(EA 진입점)는 lifecycle(`OnInit/OnTick/OnDeinit`, 생명주기)와 설정 연결(configuration wiring, 설정 연결)만 맡는다.

효과(effect, 효과): 다음 MT5 EA 작업은 한 `.mq5` 파일에 계속 덧붙이지 않고, 기능별 모듈(module, 모듈)을 먼저 정한 뒤 필요한 entrypoint(진입점)만 얇게 만든다.

# RUN02C-RUN02F Divergent Packet

## 결과(Result, 결과)

RUN02C~RUN02F(실행 02C~02F)는 모두 MT5(`MetaTrader 5`, 메타트레이더5) routed-only runtime_probe(라우팅 전용 런타임 탐침)를 완료했다.

효과(effect, 효과): RUN01(실행 01)의 근처 튜닝이 아니라 LGBM(라이트GBM)의 direction(방향), confidence(확신), context(문맥) 실패 구조를 분리해서 봤다.

| run(실행) | idea(아이디어) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---|
| RUN02C(실행 02C) | long-only direction isolation(롱 전용 방향 분리) | `-154.01 / 0.68` | `82.69 / 1.35` | OOS(표본외)는 살아있지만 validation(검증)이 약해 불안정 |
| RUN02D(실행 02D) | short-only direction isolation(숏 전용 방향 분리) | `-18.33 / 0.89` | `-211.48 / 0.31` | short-only(숏만)는 OOS(표본외)에서 약함 |
| RUN02E(실행 02E) | extreme confidence rejection(극단 확신만 허용) | `-115.17 / 0.31` | `-6.35 / 0.96` | OOS(표본외)는 거의 본전이나 validation(검증)이 약함 |
| RUN02F(실행 02F) | calm trend context gate(차분한 추세 문맥 제한) | `-234.03 / 0.46` | `-163.22 / 0.41` | context gate(문맥 제한)는 실패 |

## 실패 기억(Failure Memory, 실패 기억)

- RUN02C(실행 02C): long-only(롱만)는 salvage value(회수 가치)가 있다. reopen condition(재개 조건)은 validation(검증)이 무너지지 않는 별도 context gate(문맥 제한)나 calibrated long threshold(보정된 롱 임계값)이다.
- RUN02D(실행 02D): short-only(숏만)는 OOS(표본외) 손실이 커서 반복하지 않는다. reopen condition(재개 조건)은 새 short-specific label(숏 전용 라벨)이다.
- RUN02E(실행 02E): extreme confidence(극단 확신)는 trade count(거래 수)를 크게 줄이며 OOS(표본외)를 거의 본전으로 만들었다. reopen condition(재개 조건)은 validation(검증) 손실을 줄이는 calibration(보정) 또는 direction filter(방향 필터)다.
- RUN02F(실행 02F): calm trend gate(차분한 추세 제한)는 현재 조건으로는 회수 가치가 약하다. reopen condition(재개 조건)은 다른 context feature(문맥 피처) 조합이다.

## 경계(Boundary, 경계)

이 묶음(packet, 묶음)은 `runtime_probe_only(런타임 탐침 전용)`이다.

효과(effect, 효과): alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority expansion(런타임 권위 확장)을 주장하지 않는다.

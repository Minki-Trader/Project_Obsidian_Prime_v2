# RUN02G-RUN02P Idea Burst Packet

## 결과(Result, 결과)

RUN02G~RUN02P(실행 02G~02P)는 모두 MT5(`MetaTrader 5`, 메타트레이더5) routed-only runtime_probe(라우팅 전용 런타임 탐침)를 완료했다.

효과(effect, 효과): RUN02C/RUN02E(실행 02C/02E)의 약한 회수 가치(salvage value, 회수 가치)를 바로 세부 튜닝하지 않고, 10개 context/direction/confidence(문맥/방향/확신) 아이디어로 더 넓게 발산했다.

| run(실행) | idea(아이디어) | signals A/B/AB(신호 A/B/합산) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | read(판독) |
|---|---|---:|---:|---:|---|
| RUN02G(실행 02G) | long pullback(롱 되돌림) | `49/3/52` | `-138.39 / 0.54` | `238.68 / 3.44` | OOS(표본외) 회수 가치는 큼, validation(검증)은 약함 |
| RUN02H(실행 02H) | bull trend long(상승 추세 롱) | `21/3/24` | `-210.68 / 0.19` | `11.52 / 1.21` | OOS(표본외)는 작게 양수지만 validation(검증) 손상이 큼 |
| RUN02I(실행 02I) | low-vol extreme confidence(저변동성 극단 확신) | `14/4/18` | `-509.12 / 0.00` | `-231.42 / 0.00` | 실패 |
| RUN02J(실행 02J) | balanced midband(균형 중간대) | `21/3/24` | `70.10 / 1.29` | `-121.32 / 0.55` | validation(검증)만 양수, OOS(표본외) 실패 |
| RUN02K(실행 02K) | quiet return z-score(조용한 수익률 z점수) | `44/5/49` | `-496.54 / 0.02` | `-494.23 / 0.19` | 실패 |
| RUN02L(실행 02L) | range compression(횡보 압축) | `18/4/22` | `-352.49 / 0.34` | `-250.36 / 0.05` | 실패 |
| RUN02M(실행 02M) | high-vol momentum alignment(고변동성 모멘텀 정렬) | `67/3/70` | `-496.38 / 0.25` | `-305.93 / 0.31` | 실패 |
| RUN02N(실행 02N) | squeeze breakout(압축 돌파) | `13/3/16` | `-125.51 / 0.62` | `107.14 / 55.11` | OOS(표본외) 회수 가치는 있으나 거래 수가 3개뿐이고 validation(검증)이 약함 |
| RUN02O(실행 02O) | bull vortex long(상승 보텍스 롱) | `16/2/18` | `-86.88 / 0.55` | `6.04 / 1.20` | 약한 양수 OOS(표본외), validation(검증) 약함 |
| RUN02P(실행 02P) | bear vortex short(하락 보텍스 숏) | `34/1/35` | `1.78 / 1.02` | `24.33 / 1.37` | validation/OOS(검증/표본외) 둘 다 양수지만 규모가 작아 불충분 |

## 회수 가치(Salvage Value, 회수 가치)

- RUN02G(실행 02G): OOS(표본외) `238.68 / 3.44`라서 long pullback(롱 되돌림) 문맥은 보존한다. 재개 조건(reopen condition, 재개 조건)은 validation(검증) 손실을 줄이는 별도 필터 또는 WFO(워크포워드 최적화) 확인이다.
- RUN02N(실행 02N): OOS(표본외) `107.14 / 55.11`이지만 trade count(거래 수)가 3개라 과장하지 않는다. 재개 조건은 더 넓은 표본이나 squeeze breakout(압축 돌파) 하위 문맥 확인이다.
- RUN02P(실행 02P): validation/OOS(검증/표본외)가 모두 양수지만 `1.78`, `24.33` 순수익(net profit, 순수익)이라 작은 생존 신호로만 둔다. 재개 조건은 short-specific label(숏 전용 라벨)이나 WFO(워크포워드 최적화)에서 같은 방향성이 유지되는 것이다.

## 실패 기억(Failure Memory, 실패 기억)

- RUN02I/RUN02K/RUN02L/RUN02M(실행 02I/02K/02L/02M)은 validation/OOS(검증/표본외)가 모두 약해 같은 조건 반복을 금지한다.
- RUN02H/RUN02O(실행 02H/02O)는 OOS(표본외)가 작게 양수지만 validation(검증) 손실이 커서 단독 세부 탐색으로 가지 않는다.
- RUN02J(실행 02J)는 validation(검증)만 양수라서 midband(중간대) 문맥을 바로 살리지 않는다.

## 경계(Boundary, 경계)

이 묶음(packet, 묶음)은 `runtime_probe_only(런타임 탐침 전용)`이다.

효과(effect, 효과): alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority expansion(런타임 권위 확장)을 주장하지 않는다.

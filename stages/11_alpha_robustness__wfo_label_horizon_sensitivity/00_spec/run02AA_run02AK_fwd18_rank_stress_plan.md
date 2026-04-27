# RUN02AA~RUN02AK fwd18 Rank Stress Plan

## Intake(인입)

- active stage(현재 단계): `11_alpha_robustness__wfo_label_horizon_sensitivity`
- source idea(원천 아이디어): RUN02Z(실행 02Z) fwd18 inverse rank + DI/ADX context(fwd18 역방향 순위 + DI/ADX 문맥)
- claim boundary(주장 경계): `runtime_probe(런타임 탐침)`와 `stress_read(압박 판독)`만 허용한다.

효과(effect, 효과): RUN02Z(실행 02Z)의 작은 양수 판독을 alpha quality(알파 품질)로 과장하지 않고, ADX cutoff(ADX 절단값), routed fallback(라우팅 대체), session slice(세션 구간)에 흔들리는지 확인한다.

## Router(라우터)

- phase_plan(단계 계획): design(설계) -> code patch(코드 패치) -> MT5 runtime probe(MT5 런타임 탐침) -> evidence recording(근거 기록) -> result judgment(결과 판정)
- skills_considered(검토한 스킬): `obsidian-experiment-design`, `obsidian-runtime-parity`, `obsidian-performance-attribution`, `obsidian-result-judgment`
- skills_selected(선택한 스킬): 위 네 가지
- skills_not_used(쓰지 않은 스킬): reference scout(레퍼런스 탐색)는 외부 자료가 필요 없어서 제외한다.
- final_answer_filter(최종 답변 필터): 숫자, 의미, 아직 아닌 것, 다음 행동만 짧게 말한다.

## Experiment Design(실험 설계)

- hypothesis(가설): RUN02Z(실행 02Z)의 양수 판독은 `ADX<=25` 근처와 `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)`에서만 안정적일 수 있다.
- control variables(통제 변수): `US100` `M5`, fwd18(90분) LGBM(`LightGBM`, 라이트GBM), inverse rank threshold(역방향 순위 임계값), hold(보유) `9`, Tier A quantile(분위수) `0.96`, Tier B quantile(분위수) `0.96`
- changed variables(변경 변수): `ADX<=20/25/30`, routed vs Tier A-only(라우팅 대 Tier A 단독), session slice(세션 구간) `190-210/195-215/200-220/205-225`
- required records(필수 기록): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산), MT5 routed total(MT5 라우팅 전체)
- success criteria(성공 기준): validation/OOS(검증/표본외)가 동시에 양수이고, 거래 수와 recovery(회복계수)가 RUN02Z(실행 02Z)보다 덜 얇아진다.
- failure criteria(실패 기준): 한쪽 split(분할)만 양수이거나, OOS(표본외) 거래 수가 사라지거나, routed fallback(라우팅 대체)을 꺼도 더 좋아지지 않는다.
- stop condition(중지 조건): 양수라도 tiny sample(작은 표본)이면 promotion_candidate(승격 후보)로 올리지 않는다.

## Planned Runs(계획 실행)

| run(실행) | axis(축) | source(원천) | routing(라우팅) | context(문맥) |
|---|---|---|---|---|
| RUN02AA(실행 02AA) | ADX narrow(ADX 좁힘) | RUN02W(실행 02W) | routed(라우팅) | `ADX<=20` |
| RUN02AB(실행 02AB) | ADX wide(ADX 넓힘) | RUN02W(실행 02W) | routed(라우팅) | `ADX<=30` |
| RUN02AC(실행 02AC) | Tier A-only narrow(Tier A 단독 좁힘) | RUN02W(실행 02W) | Tier A-only(Tier A 단독) | `ADX<=20` |
| RUN02AD(실행 02AD) | Tier A-only center(Tier A 단독 중심) | RUN02W(실행 02W) | Tier A-only(Tier A 단독) | `ADX<=25` |
| RUN02AE(실행 02AE) | Tier A-only wide(Tier A 단독 넓힘) | RUN02W(실행 02W) | Tier A-only(Tier A 단독) | `ADX<=30` |
| RUN02AF~RUN02AH(실행 02AF~02AH) | session sources(세션 원천) | fwd18 input(90분 입력) | payload only(인계물 전용) | `190-210/195-215/205-225` |
| RUN02AI~RUN02AK(실행 02AI~02AK) | session stress(세션 압박) | RUN02AF~RUN02AH(실행 02AF~02AH) | routed(라우팅) | `ADX<=25` |

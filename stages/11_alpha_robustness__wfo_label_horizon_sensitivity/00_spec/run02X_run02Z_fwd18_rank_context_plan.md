# RUN02X~RUN02Z fwd18 Rank Context Plan

## Intake(인입)

- active stage(현재 단계): `11_alpha_robustness__wfo_label_horizon_sensitivity`
- source run(원천 실행): `run02W_lgbm_fwd18_retrain_v1`
- comparison reference(비교 기준): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- claim boundary(주장 경계): `runtime_probe(런타임 탐침)` 또는 `structural_scout(구조 탐침)`만 허용한다.

효과(effect, 효과): RUN02W(실행 02W)의 fwd18-only retrain(fwd18 단독 재학습) 실패를 반복하지 않고, fwd18(90분) 모델을 rank threshold(순위 임계값), inverse decision(역방향 판정), context gate(문맥 제한)로 나누어 어디서 신호가 살아나는지 확인한다.

## Router(라우터)

- phase_plan(단계 계획): design(설계) -> code(코드) -> Python structural probe(파이썬 구조 탐침) -> MT5 runtime probe(MT5 런타임 탐침) -> evidence recording(근거 기록) -> result judgment(결과 판정)
- skills_considered(검토한 스킬): `obsidian-reentry-read`, `obsidian-experiment-design`, `obsidian-model-validation`, `obsidian-runtime-parity`, `obsidian-result-judgment`, `obsidian-answer-clarity`
- skills_selected(선택한 스킬): 위 전부
- skills_not_used(쓰지 않은 스킬): external reference scout(외부 레퍼런스 탐색)는 새 외부 API(외부 API)나 문서가 필요 없어서 제외한다.
- final_answer_filter(최종 답변 필터): 결론, 쉬운 의미, 숫자, 아직 아닌 것, 다음 행동만 짧게 말한다.

## Experiment Design(실험 설계)

- hypothesis(가설): fwd18(90분) LGBM(`LightGBM`, 라이트GBM) 고순위 신호는 직접 방향으로는 약하지만, inverse decision(역방향 판정)과 low DI spread / low ADX context(DI 차이 낮음 / ADX 낮음 문맥)를 결합하면 거래 품질이 회복될 수 있다.
- decision_use(결정 용도): Stage 11(11단계)에서 full WFO(전체 워크포워드 최적화) 전에 stress test(압박 시험)할 가치가 있는 표면인지 판단한다.
- comparison_baseline(비교 기준): RUN02W(실행 02W) fwd18-only retrain(단독 재학습), RUN02X(실행 02X) direct rank(직접 순위), RUN02Y(실행 02Y) inverse rank(역방향 순위)
- control_variables(통제 변수): `US100` `M5`, split v1(분할 v1), session slice(세션 구간) `200 < minutes_from_cash_open <= 220`, hold(보유) `9`, source model(원천 모델) RUN02W
- changed_variables(변경 변수): direction mode(방향 모드), rank threshold(순위 임계값), context gate(문맥 제한)
- sample_scope(표본 범위): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산); MT5 routed(Tier A 우선 + Tier B 대체) validation/OOS(검증/표본외)
- success_criteria(성공 기준): validation/OOS(검증/표본외) 양쪽에서 MT5 routed total(MT5 라우팅 전체)이 양수이고 risk KPI(위험 핵심 성과 지표)가 기록된다.
- failure_criteria(실패 기준): direct/inverse/context 중 어느 축도 validation/OOS(검증/표본외)를 동시에 회복하지 못한다.
- invalid_conditions(무효 조건): MT5 compile(컴파일) 실패, tester output(테스터 출력) 부재, feature handoff(피처 인계) 불일치
- stop_conditions(중지 조건): 양수라도 거래 수가 너무 작으면 promotion(승격)으로 올리지 않고 stress test(압박 시험) 후보로만 남긴다.
- evidence_plan(근거 계획): `run_manifest.json`, `kpi_record.json`, `summary.json`, `result_summary.md`, project/stage ledgers(프로젝트/단계 장부), MT5 report(MT5 보고서)

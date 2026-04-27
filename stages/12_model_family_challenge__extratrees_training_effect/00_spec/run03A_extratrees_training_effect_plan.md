# RUN03A ExtraTrees Training Effect Plan

## Intake(인입)

- active stage(활성 단계): `12_model_family_challenge__extratrees_training_effect`
- run_id(실행 ID): `run03A_extratrees_fwd18_inverse_context_scout_v1`
- comparison baseline(비교 기준): `run02Z_lgbm_fwd18_inverse_rank_context_v1`
- claim boundary(주장 경계): `Python structural scout(파이썬 구조 탐침)` only(전용)

## Router(라우터)

- phase_plan(단계 계획): design(설계) -> code(코드) -> Python run(파이썬 실행) -> evidence recording(근거 기록) -> result judgment(결과 판정)
- skills_considered(검토한 스킬): `obsidian-reentry-read`, `obsidian-experiment-design`, `obsidian-data-integrity`, `obsidian-environment-reproducibility`, `obsidian-model-validation`, `obsidian-result-judgment`
- skills_selected(선택한 스킬): 위 전부
- skills_not_used(쓰지 않은 스킬): `obsidian-runtime-parity(런타임 동등성)`는 이번 run(실행)이 MT5 runtime_probe(MT5 런타임 탐침)를 주장하지 않아서 제외
- final_answer_filter(최종 답변 필터): 결론, 수치, 아직 아닌 것, 다음 조건만 짧게 말한다.

## Experiment Design(실험 설계)

- hypothesis(가설): ExtraTreesClassifier(엑스트라 트리 분류기)는 LightGBM(라이트GBM)과 다른 비선형 분할을 만들기 때문에 fwd18 inverse-rank context(fwd18 역방향 순위 문맥)의 신호 밀도와 hit rate(적중률)를 바꿀 수 있다.
- decision_use(결정 용도): Stage 12(12단계)에서 MT5 runtime_probe(MT5 런타임 탐침)로 넘길 새 모델 표면이 있는지 판단한다.
- comparison_baseline(비교 기준): `RUN02Z(실행 02Z)` LightGBM fwd18 inverse-rank context MT5 runtime_probe(런타임 탐침)
- control_variables(통제 변수): `US100`, `M5`, fwd18 label(90분 라벨), split v1(분할 v1), `200-220` session slice(세션 구간), `ADX<=25`, `abs(DI spread)<=8`, inverse decision(역방향 판정), hold(보유) `9`
- changed_variables(변경 변수): model family(모델 계열)만 `LightGBM`에서 `ExtraTreesClassifier`로 변경
- sample_scope(표본 범위): Tier A/Tier B/Tier A+B context-filtered(문맥 필터) validation/OOS(검증/표본외)
- success_criteria(성공 기준): validation/OOS(검증/표본외) 모두에서 충분한 signal count(신호 수)와 방향 hit rate(방향 적중률)가 생겨 MT5 runtime_probe(MT5 런타임 탐침) 후보가 된다.
- failure_criteria(실패 기준): signal count(신호 수)가 너무 작거나 validation/OOS(검증/표본외) hit rate(적중률)가 동시에 약하다.
- invalid_conditions(무효 조건): feature order hash(피처 순서 해시) 불일치, label/split(라벨/분할) 누락, ONNX parity(ONNX 동등성) 실패
- stop_conditions(중지 조건): Python structural scout(파이썬 구조 탐침)만으로 운영 의미(operational meaning, 운영 의미)를 주장하지 않는다.
- evidence_plan(근거 계획): `run_manifest.json`, `kpi_record.json`, `summary.json`, `result_summary.md`, stage/project ledgers(단계/프로젝트 장부)

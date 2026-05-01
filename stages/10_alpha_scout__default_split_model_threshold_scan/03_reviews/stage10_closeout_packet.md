# Stage 10 Closeout Packet

- packet_id(묶음 ID): `stage10_alpha_scout_closeout_packet_v1`
- stage(단계): `10_alpha_scout__default_split_model_threshold_scan`
- status(상태): `reviewed_closed_handoff_to_stage11_ready`
- judgment(판정): `inconclusive_single_split_scout_mt5_runtime_probe_completed`
- external_verification_status(외부 검증 상태): `completed(완료)`
- historical selected baseline wording(역사적 선택 기준선 표현): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`

## 2026-05-01 해석 부록(Interpretation Addendum, 해석 부록)

이 문서의 baseline(기준선) 표현은 현재 진실(current truth, 현재 진실)에서 superseded historical wording(대체된 역사적 표현)이다.

현재 해석(current interpretation, 현재 해석)은 `run01Y(실행 01Y)`를 seed surface(씨앗 표면), preserved clue(보존 단서), reference surface(참고 표면)로 본다. Stage 10(10단계)에서 Stage 11(11단계)로 넘어간 것은 baseline selection(기준선 선택)이 아니라 topic pivot(주제 전환)이다.

근거(decision, 결정): `docs/decisions/2026-05-01_alpha_stage_transition_philosophy_correction.md`

## 쉬운 판독(Plain Read, 쉬운 판독)

Stage 10(10단계)은 default split(기본 분할) 위에서 첫 model-backed alpha scout(모델 근거 알파 탐색 판독)를 끝까지 흔들었다.

효과(effect, 효과): `run01Y(실행 01Y)`가 Stage 10(10단계) 안의 best balanced seed surface(최고 균형 씨앗 표면)로 남고, 다음 단계(next stage, 다음 단계)는 WFO(`walk-forward optimization`, 워크포워드 최적화)와 label/horizon sensitivity(라벨/예측수평선 민감도)를 topic pivot(주제 전환)으로 본다.

## 닫힌 근거(Closed Evidence, 닫힌 근거)

| run(실행) | idea(아이디어) | validation net/PF(검증 순수익/수익 팩터) | OOS net/PF(표본외 순수익/수익 팩터) | OOS DD/recovery(표본외 손실/회복) |
|---:|---|---:|---:|---:|
| `run01Y` | hold9 base(9봉 기준), `200 < x <= 220` | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| `run01Z` | hold6(6봉), `200 < x <= 220` | `264.14 / 2.99` | `109.65 / 1.66` | `161.79 / 0.68` |
| `run01AA` | hold12(12봉), `200 < x <= 220` | `447.76 / 4.55` | `225.69 / 2.57` | `170.11 / 1.33` |
| `run01AB` | margin0.025(마진 0.025), hold9(9봉) | `318.48 / 3.88` | `313.14 / 3.99` | `144.65 / 2.16` |
| `run01AC` | strict probability(엄격 확률), hold9(9봉) | `143.91 / 2.30` | `219.09 / 5.53` | `147.09 / 1.49` |

효과(effect, 효과): hold6(6봉 보유)은 약했고, hold12(12봉 보유)는 validation(검증) 쪽으로 치우쳤고, margin0.025(마진 0.025)는 실제로 결과를 줄이지 못했고, strict probability(엄격 확률)는 OOS PF(표본외 수익 팩터)는 높지만 net/recovery(순수익/회복)가 낮았다.

## 선택(Selection, 선택)

`run01Y(실행 01Y)`를 Stage 11(11단계)의 seed surface(씨앗 표면)와 reference surface(참고 표면)로 보존한다.

효과(effect, 효과): Stage 11(11단계)은 baseline(기준선)을 검증하는 단계가 아니라, Stage 10(10단계)에서 가장 균형 좋았던 시간 구간과 threshold(임계값)를 참고 표면(reference surface, 참고 표면)으로 삼아 WFO(워크포워드 최적화), label/horizon(라벨/예측수평선), model family(모델 계열) 질문으로 전환한다.

## 경계(Boundary, 경계)

이 묶음(packet, 묶음)은 alpha result(알파 결과), alpha quality(알파 품질), live readiness(실거래 준비), runtime authority expansion(런타임 권위 확장), operating promotion(운영 승격)을 만들지 않는다.

Stage 10(10단계)의 결과는 `runtime_probe(런타임 탐침)`와 `single_split_scout(단일 분할 탐색 판독)`까지만 닫힌다.

## 다음 단계(Next Stage, 다음 단계)

다음 활성 단계(active stage, 활성 단계)는 `11_alpha_robustness__wfo_label_horizon_sensitivity`다.

효과(effect, 효과): 새 채팅에서는 Stage 11(11단계)을 시작하되, Stage 10(10단계) 실행 번호(run number, 실행 번호)를 이어 쓰지 않고 새 단계의 질문(question, 질문)으로 작업한다.

# Prior-Stage Scan(이전 단계 점검)

This scan(이 점검)은 Stage12~364(12~364단계)를 reference archive(참조 보관소)로만 읽는다.

## Preserved Clues(보존 단서)

| source(원천) | clue(단서) | limit(한계) | allowed use(허용 사용) |
|---|---|---|---|
| `run364HS_stage364_closeout_no_next_stage.md` | `hold4_margin_0.01` net/PF/density(순수익/수익 팩터/밀도) `462.0071630903 / 1.2257899553 / 2.1178343949` | strict_joint_pass_count(엄격 동시 통과 수) `0`; Tier B missing_required(티어 B 필수 누락) | target distance example(목표 거리 예시) only(전용) |
| `run364HL_probability_bin_veto_mt5_runtime_probe_review.md` | MT5 net/PF/trades/density(MT5 순수익/수익 팩터/거래 수/밀도) `369.03 / 1.39 / 542 / 1.7261146497` | density below goal(목표 밀도 미달), short-heavy(숏 편중), cost stress failed(비용 압박 실패) | runtime observation vocabulary(런타임 관찰 어휘) |
| `run364HQ_single_source_probability_bin_veto_mt5_runtime_probe_review.md` | MT5 positive net(양수 순수익) with density near 3(밀도 3 근접) | PF(수익 팩터) `1.05`, DD(손실폭) `45.8%`, RF(회복 계수) weak(약함) | risk penalty design(위험 벌점 설계) |
| `stage12_364_campaign_map.md` | one-axis repair loop(한 축 수리 반복) and sparse PF selector(희소 PF 선택기) memory(기억) | no candidate inheritance(후보 상속 없음) | DNR guardrail(반복 금지 보호 조건) |

## Negative Memories(부정 기억)

- Sparse PF999 selector(희소 PF999 선택기): high PF(높은 수익 팩터)가 tiny sample(얇은 표본)을 숨기면 품질이 아니다.
- Proxy-to-runtime gap(프록시와 런타임 차이): scaled density(스케일 밀도)와 package readiness(패키지 준비성)는 MT5 tester output(MT5 테스터 출력)을 대체하지 않는다.
- Candidate distinguishability collapse(후보 구분성 붕괴): 여러 candidate(후보)가 같은 MT5 signature(MT5 서명)로 접히면 selection signal(선택 신호)이 약하다.
- One-axis repair loop(한 축 수리 반복): density/PF/DD/cost(밀도/수익 팩터/손실폭/비용) 중 하나만 고치면 다른 축이 깨졌다.

## Do-Not-Repeat Imports(반복 금지 반입)

- Do not inherit winner/baseline/promotion(승자/기준선/승격 상속 금지).
- Do not start from `hold4_margin_0.01` as a threshold or hold anchor(임계값 또는 보유 앵커로 시작 금지).
- Do not call proxy proof runtime proof(프록시 증명을 런타임 증명으로 부르기 금지).
- Do not move WFO/MT5(워크포워드 최적화/메타트레이더5) before scout clue(탐색 단서) and Grok pre-expensive review(비싼 검증 전 그록 검토).

## Verification Boundary(검증 경계)

This scan(이 점검)은 local document check(로컬 문서 확인)다. It is not a new experiment(새 실험 아님), not model training(모델 학습 아님), and not runtime validation(런타임 검증 아님).

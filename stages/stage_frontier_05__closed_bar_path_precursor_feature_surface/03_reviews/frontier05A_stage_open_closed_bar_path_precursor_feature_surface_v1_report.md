# Frontier05A Stage Open Report(전선05A 단계 개방 보고서)

Updated(갱신): 2026-06-13T19:33:24Z

Status(상태): `opened_frontier05_closed_bar_path_precursor_feature_surface_no_authority`

Judgment(판정): `stage_opened_after_grok_review_no_authority`

## Action And Effect(행동과 효과)

Action(행동): Frontier05(전선05)를 closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면) 가설 생명주기로 열었습니다.

Effect(효과): Frontier04(전선04)의 preserved path-label clue(보존 경로 라벨 단서)는 reference target(참조 목표)로만 쓰고, 실패 원인으로 남은 feature learnability bottleneck(피처 학습 가능성 병목)을 새 독립 전선(independent frontier, 독립 전선)에서 시험합니다.

## Thesis(가설)

Closed-bar path precursor features may make the preserved path-quality target learnable without future leakage(확정봉 경로 선행 피처는 미래 누수 없이 보존된 경로 품질 목표를 학습 가능하게 만들 수 있음).

## Novelty Delta(신규성 차이)

Feature surface changes while the path target remains a fixed reference target(경로 목표는 고정 참조 목표로 두고 피처 표면을 바꿈).

## Grok Review(그록 검토)

Recommendation(권고): `open_frontier05(전선05 개방)`

Accepted(수용):
- open Frontier05 as a new feature-surface learnability hypothesis(전선05를 새 피처 표면 학습 가능성 가설로 개방)
- keep Frontier04 path label as fixed reference target only(전선04 경로 라벨은 고정 참조 목표로만 사용)
- compare feature_set_v2 versus augmented closed-bar features on identical rows/splits(동일 행/분할에서 피처 세트 v2와 확정봉 증강 피처 비교)
- keep first scout proxy/model-only before WFO/MT5(첫 탐색을 WFO/MT5 전 프록시/모델 전용으로 제한)

Needs local verification(로컬 검증 필요):
- closed-bar feature formulas use no future OHLC(확정봉 피처 공식이 미래 OHLC를 쓰지 않음)
- raw OHLC alignment and duplicate checks remain valid(원천 OHLC 정렬과 중복 점검 유지)
- baseline and augmented models use identical labels/splits/selection metrics(기준/증강 모델이 같은 라벨/분할/선택 지표 사용)
- new stage-local features are not silently promoted to foundation truth(새 단계 로컬 피처를 foundation 진실 원천으로 조용히 승격하지 않음)
- Tier A/Tier B/combined record boundary is explicit(Tier A/Tier B/합산 기록 경계 명시)

## Work Packet(작업 묶음)

- primary_family(주 작업군): `experiment_design(실험 설계)`
- primary_skill(주 스킬): `obsidian-experiment-design(옵시디언 실험 설계)`
- required_gates(필수 게이트): `work_packet_schema_lint(작업 묶음 스키마 점검); external_review_packet(외부 검토 묶음)`

## Next Action(다음 행동)

`frontier05B_closed_bar_path_precursor_feature_scout_v1`. Action(행동)은 baseline feature_set_v2(기준 피처 세트 v2)와 closed-bar augmented feature surface(확정봉 증강 피처 표면)를 같은 라벨/분할에서 비교하는 것입니다. Effect(효과)는 ONNX(온엑스), WFO(워크포워드), MT5(메타트레이더5) 전에 학습 가능성 병목이 실제인지 확인하는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).

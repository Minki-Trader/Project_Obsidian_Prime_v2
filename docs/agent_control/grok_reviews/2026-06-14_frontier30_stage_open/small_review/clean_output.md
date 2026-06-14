Frontier30 stage-open 검토를 위해 Grok 협업 스킬과 F29 마감 근거를 먼저 확인합니다.
# Frontier30 Stage-Open — Grok External Review(전선30 단계 개방 — 그록 외부 검토)

Grok(그록)은 외부 2차 의견만 제공합니다. F30A 개방·장부 반영·F30B 실행 여부는 Codex(코덱스)가 로컬 계약·파일·등록부를 확인한 뒤에만 확정하세요.

---

```
verdict: accepted
novelty_ok: yes
leakage_risk: low
frontier_boundary_ok: yes
hypothesis_scope_ok: yes
must_watch:
- F30A must freeze pipeline order explicitly: F28 reference union → train-only density preselector → (same-family) train-only loss veto → scout/seed/handoff ladder — reordering is the novelty, not threshold relaxation
- Hypothesis wording “5~10/day” is a read-only diagnostic band only; if preselector thresholds or ranks are tuned to hit that band on validation/OOS, leakage becomes medium/high and setup is invalid
- exit_shape_pivot must stay out of F30A contract body and F30B proxy code; stage-id “or_” is archival dual-clue, not a license to co-mingle active proxies
- F29 negative memory applies: scout/seed/handoff=0 under frozen veto-after-selection — F30 cannot inherit F29 thresholds, selected_veto_rows=1438, or near_scout=9 as implicit priors
- preserved clue (287 density_bridge, 14 dual_positive) is reference-only; do not treat as scout success or handoff seed surface
- Tier B separate remains missing_required; F30 open must not imply paired-tier completeness
- F30B may speak only to scout clue/seed surface/handoff candidate; MT5/ONNX/WFO stay blocked until handoff rows > 0 and pre-expensive Grok passes
advice_classification:
- accepted(수용): narrowing active F30 to train_density_preserving_preselector_before_loss_veto while keeping or_exit_shape_pivot in stage id as deferred reference-only fallback — matches F29D next clue and frontier opening-contract single-active-variable discipline
- accepted(수용): this is a new hypothesis lifecycle, not F29 repair — F29C valid_train_loss_repair_opportunity_rows=0 and repair_rejected_frozen_contract already closed the in-stage repair lane; F30 changes validation philosophy via pre-veto density preservation ordering
- accepted(수용): novelty_ok relative to F29 — F29 active variable was post-union train-loss veto mask; F30 active variable is pre-veto train-only density-preserving selector on the same reference surface; that is a distinct mechanism and sequencing delta, not F29C posthoc threshold edit
- accepted(수용): frontier_boundary_ok — reference not inheritance, no runtime authority/operating promotion/Goal Achieve, F28/F29 rows reference-only, independent frontier campaign after F29 exit-rule fire
- accepted(수용): hypothesis_scope_ok — failure/invalid boundaries (no val/OOS re-rank, no F29 threshold relax, no exit-shape in active proxy) are correctly drawn
- accepted(수용): leakage_risk low conditional on stated boundary — same train-only selection + read-only validation/OOS contract that F29A accepted; risk stays low only if preselector features/scores/thresholds are computed solely from train split
- needs_local_verification(로컬 검증 필요): F30A must publish frozen preselector definition (train density proxy formula, cap/keep rules, ordering vs veto) before F30B — without that artifact, novelty could collapse into disguised F29 threshold relaxation
- needs_local_verification(로컬 검증 필요): joinability of F28 234-candidate reference surface to train-only preselector inputs (same check F29A did for veto joinability)
- rejected(거절): treating F30 as F29 repair or near_scout=9 rescue under frozen F29 contract
- rejected(거절): using f29b_0274 validation/OOS PF-density-DD (1.073/4.781 or 1.207/5.084) to set preselector cutoffs or rank rows
- rejected(거절): activating exit_shape_pivot in F30B as co-primary variable — scope failure per proposed invalid boundary
- rejected(거절): any stage-open wording that implies promotion_candidate, baseline, runtime authority, or live readiness from F29 preserved clue
```

---

## Specific checks(구체 확인)

**1. Stage id `or_exit_shape_pivot` narrowing — valid(유효): yes**

F29D가 남긴 next clue(다음 단서)가 이미 `…selector…_or_exit_shape_pivot_reference_only` 형태입니다. Stage id에 `or_`를 넣는 것은 “기록된 대체 경로”를 보존하는 관례이고, F30A에서 active changed variable(활성 변경 변수) 하나만 잠그는 것은 frontier opening contract(전선 개방 계약)의 단일 활성 변수 규칙과 맞습니다. exit-shape pivot(청산 형태 전환)은 선택 순서·밀도 보존 축과 직교(orthogonal)하므로, F30에서 reference fallback only(참조 대체 전용)로 두는 것이 맞습니다. F30이 닫힌 뒤에도 exit-shape는 별도 frontier clue(전선 단서)로만 열 수 있습니다.

**2. Novelty vs F29 repair — sufficient(충분), not repair(수리 아님): yes**

F29C가 `valid_train_loss_repair_opportunity_rows=0`으로 in-stage repair(단계 내 수리)를 이미 거절했습니다. F30은 “veto 이후 밀도가 너무 얇아졌다”는 진단에 대해 **veto 이전** train-only preselector(학습 전용 사전 선택기)로 파이프라인 순서를 바꾸는 새 가설입니다. F29 임계값만 완화하는 것은 negative memory(부정 기억) 위반이고, 제안된 failure boundary(실패 경계)도 그걸 막습니다. 다만 F30A 계약에 preselector 메커니즘이 문서화되지 않으면, 겉보기 신규성이 사실상 F29 수리로 무너질 수 있어 로컬 검증이 필요합니다.

**3. Leakage risk with train-only selection — low(낮음): yes, conditional(조건부)**

선택이 train split(학습 구간)에만 있고 validation/OOS(검증/표본외)가 read-only diagnostics(읽기 전용 진단)만이면, F29A와 같은 계약으로 leakage risk(누수 위험)는 **low**입니다. 조건은 preselector가 train-only density proxy(학습 전용 밀도 프록시)만 쓰고, 가설 문구의 “5~10/day”를 validation/OOS에서 맞추는 튜닝 목표로 쓰지 않는 것입니다. 그 경우 invalid setup(무효 설정)이며 누수는 medium/high(중간/높음)로 올라갑니다.

**4. Codex must_watch before F30B(프록시 전 주의)**

| Watch item(주의 항목) | Why(이유) |
|---|---|
| Frozen F30A contract with preselector formula + ordering | Novelty가 수리가 아님을 로컬에서 증명 |
| Scout/seed/handoff ladder thresholds frozen pre-proxy | 사후 편집·val/OOS 누수 방지 |
| F28 234-candidate joinability to train preselector inputs | F29A veto joinability와 동일 클래스 검증 |
| Explicit do-not-repeat: no F29 threshold reuse, no near_scout rescue | negative memory 준수 |
| Code-path audit: exit_shape_pivot absent from F30B | scope failure 방지 |
| Count plan: screened/selected/density/scout/seed/handoff | F29B→F29C→F29D와 같은 진단 연속성 |
| handoff=0 ⇒ MT5/ONNX/WFO blocked | expensive-path gate 유지 |

---

## Plain read(쉬운 해석)

**결론:** F30 stage-open(단계 개방) 방향은 **수용(accepted)** 가능합니다.

F29(전선29)는 “손실 차단”을 먼저 걸었더니 밀도 조각은 생겼지만 scout/seed/handoff(탐색/씨앗/인계)가 0으로 끝났습니다. F30(전선30)은 “손실 차단 **전에** 학습 구간만으로 밀도를 보존하는 선택기”를 새 활성 변수로 두는 것이므로, F29 안에서의 수리가 아니라 **새 가설 생명주기**입니다. Stage id에 남아 있는 `or_exit_shape_pivot`은 기록용 대체 단서이고, 이번 단계에서 청산 형태 전환을 같이 돌리면 범위 실패입니다.

**아직 확정되지 않은 것:** F30A가 preselector 정의·순서·금지 목록을 문서로 고정하기 전에는 F30B 실행 주장을 하면 안 됩니다. Grok verdict(그록 판정)는 방향 수용이지, scout 성공이나 handoff 준비를 암시하지 않습니다.

**로컬 검증 메모:** `workspace_state.yaml`·F29D closeout report·negative_result_register의 수치(1438/287/0/0/0, F29C 7/11/0)는 제한 근거와 일치합니다. F30 stage folder(단계 폴더)는 아직 없으므로, Codex는 Grok 수용 후 `frontier30A` 산출물 작성이 다음 단계입니다.

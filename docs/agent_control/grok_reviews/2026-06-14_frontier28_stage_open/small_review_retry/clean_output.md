verdict: **accepted**

novelty_ok: **yes**

leakage_risk: **low**

forbidden_path_risk: **low**

specific_change_requests:
- State in F28 open packet that F27 `soft penalty rank(연성 페널티 순위)` is **reference clue only(참조 단서만)**; F28 must not retune F27 penalty weights or re-run the same forward-metric selection loop under a new label.
- Freeze `train_subperiod_pf_dd_balance_stability_gap_rank(학습 하위기간 수익 팩터/손실폭 균형 안정성 격차 순위)` definition up front: 4 chronological train chunks(학습 시간순 4조각), chunk boundary dates, and penalty terms; no post-hoc chunk or penalty edits to chase handoff rows(인계 후보 행).
- Enforce selection boundary in closeout: train-only metrics rank; validation/OOS(검증/표본외) are **read-only diagnostics(읽기 전용 진단)** only — any row promoted because val/OOS looked best is a leakage failure(누수 실패).
- Define F28 success without inheriting F27 best-row story: success is `handoff candidate rows(인계 후보 행) > 0` from train-stability ranking plus documented stability rationale; failure is again `0 seed + 0 handoff` even if val/OOS PF(검증/표본외 수익 팩터) beats F27’s 1.310/1.151 headline.
- Keep F27 union surface(합집합 표면) as input clue pool(입력 단서 풀), not a repair target: 234 candidates(후보) may shrink by explicit filters, but not by implicit “must restore seed surface(씨앗 표면)” pressure.
- Gate expensive work explicitly: no ONNX/MT5/WFO(온엑스/메타트레이더5/워크포워드 최적화) until `handoff candidate rows > 0` **and** a written `pre-expensive review(비싼 검증 전 검토)` pass is recorded; otherwise close as exploration negative memory(탐색 부정 기억), not blocked repair(차단 수리).
- Record paired-tier evidence if the same candidate set is evaluated on Tier A and Tier B(티어 A·B): separate A, separate B, and combined read(합산 판독); do not let Tier B partial-context fill(부분 문맥 보정) masquerade as train-stability proof(학습 안정성 증거).

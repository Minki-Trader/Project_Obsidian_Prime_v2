Frontier13 stage-closeout review(프론티어13 단계 마감 검토)입니다.

Please answer in this response only(이 응답 안에서만 답하세요). Do not say you will write a file(파일을 쓰겠다고 말하지 마세요).

Current truth(현재 진실):
- Frontier13A(프론티어13A)는 Grok stage-open review(그록 단계 개방 검토) accepted(수용) 뒤 열렸습니다.
- Frontier13 hypothesis(프론티어13 가설): fixed 3-class US100 M5 ONNX(고정 3클래스 US100 M5 온엑스)가 train-only regime buckets(학습 전용 국면 버킷)로 trade-shape labels(거래 형상 라벨)을 normalize(정규화)하면 F12(프론티어12)의 low-DD sparse surface(낮은 손실폭 희소 표면)를 density/PF/DD(빈도/수익 팩터/손실폭) 동시 개선으로 바꿀 수 있는지 확인합니다.
- Frontier13B(프론티어13B)는 3개 regime-normalized variants(국면 정규화 변형)와 fixed argmax ONNX models(고정 최대확률 온엑스 모델)를 시험했습니다.
- Frontier13B result(프론티어13B 결과): strict scout clue rows(엄격 탐색 단서 행) 0, preserved clue rows(보존 단서 행) 0.
- Best candidate(최고 후보): `f13b_vol_squeeze_h12_t1p00_cap0p62_ecap0p36_rec0p12__lr_plain`.
- Best validation PF/density/DD(최고 검증 수익 팩터/빈도/손실폭): 1.0396853649 / 2.2568306011 / 54.3761926154%.
- Best OOS PF/density/DD(최고 표본밖 수익 팩터/빈도/손실폭): 2.0276529355 / 0.4122137405 / 5.5734965630%.
- Worst validation/OOS subperiod DD(검증/표본밖 최악 하위기간 손실폭): 54.3761926154%.
- Sparse LR plain(희소 로지스틱 평범 모델)은 OOS PF/DD(표본밖 수익 팩터/손실폭)는 좋아 보이지만 OOS density(표본밖 빈도)가 0.412/day로 목표 5~10/day에서 멉니다.
- Balanced variants(균형 가중 변형)는 density(빈도)를 24~35/day까지 높였지만 validation/OOS DD(검증/표본밖 손실폭)가 21~66%로 커졌습니다.
- ONNX parity(온엑스 동등성)는 candidate rows(후보 행)에서 통과했습니다.
- WFO/MT5(WFO/MT5)는 strict/preserved clue(엄격/보존 단서)가 없어서 skipped by claim boundary(주장 경계상 생략)입니다.

Codex proposed closeout(코덱스 제안 마감):
- Close Frontier13(프론티어13)을 `closed_negative_memory_no_authority`로 닫습니다.
- Negative memory(부정 기억): regime-normalized trade-shape labels(국면 정규화 거래 형상 라벨)은 PF/DD/density(수익 팩터/손실폭/빈도)를 동시에 맞추지 못했습니다. Sparse(희소) 표면은 density(빈도)가 너무 낮고, balanced(균형) 표면은 DD(손실폭)가 너무 높습니다.
- Do not repeat(반복 금지): same regime-scale wrapping(같은 국면 척도 감싸기), class-weight density forcing(클래스 가중 빈도 강제), threshold micro-search(임계값 미세 탐색).
- Reference-only carry(참조 전용 이월): vol-squeeze h12 LR plain(변동성 압축 h12 로지스틱 평범 모델)은 OOS PF/DD(표본밖 수익 팩터/손실폭)가 좋아 보이는 sparse seed surface(희소 씨앗 표면)로만 보관합니다.
- Next frontier direction(다음 프론티어 방향): labels(라벨)을 더 감싸기보다 entry opportunity generation(진입 기회 생성)과 trade frequency control(거래 빈도 제어)을 더 앞단에서 바꾸는 새 가설이 필요합니다.
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않습니다.

Required output(필수 출력):
1. Classification(분류): accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요).
2. One-sentence reason(한 문장 이유).
3. Required closeout records(필수 마감 기록): what Codex(코덱스) must record to avoid overclaiming(과장 주장 방지).
4. Whether WFO/MT5 skip(WFO/MT5 생략) is valid under this claim boundary(주장 경계).
5. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

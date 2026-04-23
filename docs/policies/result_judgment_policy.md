# Result Judgment Policy

## 판정(Judgment Classes, 판정 분류)

- `positive(긍정)`: 계속 밀어볼 가치가 있는 결과
- `negative(부정)`: 가설을 약화하거나 닫는 유효한 결과
- `inconclusive(불충분)`: 근거가 부족한 결과
- `invalid(무효)`: 설정(setup, 설정), 데이터(data, 데이터), 가정(assumption, 가정)이 깨진 결과

## 규칙(Rule, 규칙)

`negative(부정)`은 재사용 가능한 근거(reusable evidence, 재사용 근거)다.

`invalid(무효)`는 깨진 부분(broken part, 깨진 부분)이 고쳐질 때까지 해석하지 않는다.

외부 검증(external verification, 외부 검증)이 필요한 주장(claim, 주장)에 외부 검증이 빠졌다면 그 주장은 `positive(긍정)`로 닫지 않는다.

- 검증을 시도할 수 있었는데 안 했다면 `inconclusive(불충분)`로 둔다.
- 검증을 시도했지만 환경이나 설정이 깨졌다면 `invalid(무효)` 또는 `blocked(차단)`로 둔다.
- 주장을 낮춰서 외부 검증이 필요 없는 범위만 말한다면, 낮춘 범위(scope, 범위)를 명시한다.

## 경계 어휘(Boundary Vocabulary, 경계 어휘)

결과 판정(result judgment, 결과 판정)은 탐색 경계(exploration boundary, 탐색 경계)를 같이 적어야 한다.

- `promotion_candidate(승격 후보)`: 비교할 수 있지만 운영 승격은 아닌 결과
- `operating_promotion(운영 승격)`: 운영선을 교체하거나 확인하는 결과
- `runtime_probe(런타임 탐침)`: 런타임을 관찰했지만 권위는 없는 결과
- `runtime_authority(런타임 권위)`: 런타임 권위를 주장하는 결과

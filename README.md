# Vision AI Notes

Vision AI 지식을 개념, 데이터 흐름, 수치 예시와 도식으로 정리하는 개인 학습 사이트.

- 사이트: https://sh0427-han.github.io/vision_ai/
- 저장소: https://github.com/sh0427-han/vision_ai
- 프로젝트 기준: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)

## 현재 자료

1. 이미지와 텐서: RGB, shape, 정규화, 밝기-픽셀 실험
2. CNN: 합성곱, 채널, stride, padding, 수용영역
3. ViT 논문 해설: 패치 임베딩, CLS, 위치 임베딩, Q/K/V, encoder
4. 분류·탐지·분할: 출력 구조와 IoU/Dice
5. 학습과 평가: 그룹 분할, 3-fold CV, threshold 실험
6. ResNet 논문 해설: degradation, residual, projection, bottleneck
7. U-Net 논문 해설: encoder-decoder, concat, 원본 crop 구조
8. PatchCore 논문 해설: memory bank, coreset, 최근접 거리
9. CS231n 전체 정리: 분류 → loss → 최적화 → CNN → 전이학습 → 현대 Vision
10. PRML 전체 정리: 14개 장의 확률·추론·잠재변수·시계열·모델 결합

## 구조와 수정

`scripts/build.py`의 `NOTES`와 `scripts/*_note.py`에 각 문서의 설명과 출처가 들어 있습니다.
HTML은 빌드 결과도 함께 커밋해 브라우저에서 직접 열 수 있게 유지합니다.

```text
index.html             홈
notes/*.html           개별 학습 문서 (생성 결과)
assets/site.css        공통 스타일
assets/site.js         메뉴와 4개 계산 실험
scripts/build.py       핵심 콘텐츠와 정적 페이지 생성
scripts/cs231n_note.py CS231n 전체 정리 원고
scripts/prml_note.py   PRML 14장 전체 정리 원고
scripts/reference_notes.py 추가 원고 등록
scripts/validate.py    링크·ID·문서 기본 구조 검사
```

Python 3 표준 라이브러리만으로 빌드합니다. JavaScript도 외부 의존성이 없습니다.

```bash
python scripts/build.py
python scripts/validate.py
python -m http.server 8000
```

`http://localhost:8000`에서 확인합니다. 새 문서를 추가할 때 `note(...)`로 등록하고
내비게이션 이름과 홈 카드 도식을 함께 추가합니다. 상세 기준은 프로젝트 문서를 참고하세요.

## GitHub Pages

최초 1회 저장소 Settings → Pages → Source를 **GitHub Actions**로 설정합니다.
이후 main 변경 시 `Deploy study notes` workflow가 검증 후 정적 파일을 배포합니다.
Pages가 활성화되지 않았다면 코드 반영만으로 사이트가 열리지 않을 수 있습니다.

## 출처와 예시

각 문서 하단에 논문과 공식 문서 링크를 적었습니다. SVG 구조도는 설명을 위해 직접
재구성한 자료이며 원문 figure를 복사하지 않았습니다. 인터랙티브 실험은 학습용 숫자를
사용하며 실제 모델을 실행하거나 실제 공정 성능을 표시하지 않습니다.

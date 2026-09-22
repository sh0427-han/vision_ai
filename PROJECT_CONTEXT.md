# Vision AI 공부 프로젝트

## 목적

개인 Vision AI 지식을 계속 축적하고 GitHub Pages에서 HTML로 읽는 학습 자료.
강의용 저장소 `vision_ai_lecture`와 별개의 프로젝트다.

- Repository: https://github.com/sh0427-han/vision_ai
- Site: https://sh0427-han.github.io/vision_ai/

## 자료 작성 기준

- 한국어로 자세히 설명한다. 처음 나오는 영어 용어의 뜻과 역할을 풀어 쓴다.
- 입력 → 처리 → 출력의 자료 형태와 shape 변화를 보여 준다.
- 문제 → 개념 → 구조도 → 수치 예시 → 한계 → 핵심 정리의 흐름을 사용한다.
- 읽을 논문 목록 대신 **논문 내용을 설명하는 학습 자료**를 작성한다.
- 논문의 문제, 모델 구조, 핵심 식, 계산 예시, 한계를 포함한다.
- 출처는 논문, 저자 공식 GitHub, 공식 Docs를 우선한다.
- 원 논문과 현대 구현, 검증된 사실과 해석, 실제 결과와 가상 예시를 구분한다.
- 구조 설명은 SVG 등 실제 도식을 사용한다. 문자 화살표만 나열하지 않는다.
- 그림·도식은 정보를 전달해야 한다. 가상 시각화를 실제 모델 결과로 표시하지 않는다.
- 공통 CSS를 사용하고 본문 가독성, 모바일, 키보드 접근성, 인쇄를 고려한다.
- 새 글은 기존 관련 글과 연결한다. 구현되지 않은 메뉴나 빈 페이지를 게시하지 않는다.
- 실험·업무의 비공개 데이터나 개인 정보를 자동으로 공개 문서에 복사하지 않는다.

## 유지보수

1. 기존 `scripts/build.py`의 해당 `note(...)`를 읽고 콘텐츠를 수정한다.
2. `assets/site.css`와 `assets/site.js`의 기존 패턴을 재사용한다.
3. `python scripts/build.py`로 생성 HTML을 업데이트한다.
4. `python scripts/validate.py`와 `node --check assets/site.js`로 정적 검증한다.
5. 내용/기능 변경에 관련된 브라우저 화면과 조작을 확인한다.
6. 소스와 생성 HTML을 함께 커밋한다. Pages workflow 결과를 확인한다.

## 현재 범위

이미지/텐서, CNN, 분류/탐지/분할, 학습/평가와
ViT·ResNet·U-Net·PatchCore 논문 해설을 포함한다.
CS231n 공개 강의 노트의 전체 학습 흐름과 Bishop PRML 14개 장 전체를
별도 종합 문서로 정리하며, 기존 상세 문서와 상호 연결한다.
아직 만들지 않은 주제를 완료된 자료처럼 표기하지 않는다.


## 대규모 참고 자료 원고

- CS231n 종합 원고: `scripts/cs231n_note.py`
- PRML 종합 원고: `scripts/prml_note.py`
- `scripts/reference_notes.py`에서 메인 빌더에 등록한다.
- 원문을 대량 복제하지 않고 개념·수식·예시를 재구성해 설명한다.


## 초심자 표기 규칙

- 독자는 Vision AI를 처음 접하는 사람을 기준으로 한다.
- 약어와 핵심 용어를 페이지 상단에 미리 나열하지 않는다.
- 약어는 본문에서 처음 실제로 사용되는 지점에 영어 원문과 한국어 뜻을 붙이고, 이후에는 약어만 사용한다.
- 일반 전문용어도 처음 등장하는 문맥에서 짧게 뜻을 설명하고 이후에는 반복 설명하지 않는다.
- 핵심 모델명은 처음 등장할 때 `CNN (Convolutional Neural Network)`처럼 풀어서 쓴다.
- 수식은 단순 코드 문자열이 아니라 MathJax/LaTeX 수학 조판으로 표시한다.
- 어두운 배경에는 반드시 밝은 글자를 사용하고, SVG CSS가 개별 `fill`을 덮어쓰지 않도록 검증한다.


## 시각자료 밀도 규칙

- 핵심 개념은 가능한 한 글만으로 끝내지 않고 개념도·비교도·계산 흐름도를 함께 제공한다.
- `scripts/extra_diagrams.py`가 추가 학습용 SVG를 생성하며, `SECTION_VISUALS`에서 페이지/섹션별 삽입 위치를 관리한다.
- 한 섹션에 여러 그림이 필요한 경우 데스크톱 2열, 모바일 1열로 배치한다.
- 그림 하나는 메시지 하나를 원칙으로 하며, 장식보다 개념 이해를 우선한다.
- PRML·CS231n처럼 추상도가 높은 내용은 각 주요 개념마다 최소 하나의 시각자료를 우선한다.


## 논문형 Figure 규칙

- CNN, ViT, PatchCore의 대표 시각자료는 단순 box-arrow diagram보다 multi-panel paper figure를 우선한다.
- 패널은 (a), (b), (c)처럼 표시하고 실제 matrix, heatmap, scatter, feature map, score distribution 등 개념에 맞는 시각 표현을 사용한다.
- paper-style figure는 `scripts/paper_figures.py`에서 생성하고 `PAPER_VISUALS`에서 섹션별 위치를 관리한다.
- 같은 개념의 단순 diagram과 paper-style figure를 한 페이지에 중복 배치하지 않는다.

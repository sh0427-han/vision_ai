# TODO — CS231n / PRML 시각자료 품질 개선

> Repository: https://github.com/sh0427-han/vision_ai  
> Pages: https://sh0427-han.github.io/vision_ai/  
> 최근 inventory 재검수 기준 main commit: `dea42ace075ced294702d26ddd7bc1b35ff0f959`

## 작업 목적

CS231n과 PRML(Christopher Bishop, *Pattern Recognition and Machine Learning*) 종합 학습 페이지의 시각자료를
단순 box-arrow diagram 수준에서 벗어나, 논문/대학 강의자료처럼 직관적이고 실제 개념을 설명하는 figure 중심으로 개선한다.

다음 세션에서는 과거 대화나 로컬 ZIP을 기준으로 덮어쓰지 말고 반드시 GitHub Connector로 최신 `main`을 먼저 조회한 뒤 작업한다.

---

## 현재 완료 상태

- [x] Pages artifact raster contact-sheet 전수 QA: reference 68개 + paper-style 18개 + extra 67개 + core SVG 10개 검수, 문제 항목은 full-size 재검수
- [x] raster QA에서 발견한 RGB/QKV/multi-head/ensemble/task output/U-Net comparison/grouped split/ROC-PR/ResNet 구조 오류와 Korean font fallback 교정
- [x] PRML 내용 TODO의 마지막 6개 보강: early stopping, polynomial kernel, EP vs VI, Factor Analysis, ICA, decision-tree ensemble
- [x] 핵심 누락 figure 8개 추가: regularization/L2, convolution sliding/edge response, posterior predictive, Dirichlet, SVM C/RVM, EM evolution, rejection sampling, PCA explained variance
- [x] Pages artifact 전체 raster QA에서 Korean SVG fallback 문제 재현 후 NanumGothic/Noto CJK/Malgun fallback 보강
- [x] `cs-pooling-hierarchy.svg` feature hierarchy pipeline의 긴 label 실제 겹침 수정 및 pipeline 자동 2줄 wrapping 적용
- [x] 실제 Pages artifact raster QA에서 잘못된 extra teaching curve 3종(optimization / overfit / threshold) 발견·교정
- [x] 실제 figure inventory와 TODO를 대조하여 기존 구현 항목의 stale checkbox 정리
- [x] gradient stability / dropout mode·fit / VGG·transfer / activation-max·Grad-CAM figure 보강
- [x] generative-vs-discriminative / kernel·GP / graph inference / mean-field VI / MCMC diagnostics / state-space / boosting figure 보강
- [x] 전수 검수 후 ELBO lower-bound, Monte Carlo sample rug, BatchNorm running statistics, SVM margin/support-vector 표현 추가 교정
- [x] 독립 ResNet/U-Net 문서를 제거하고 CNN·Segmentation 주제 본문으로 실제 내용 병합
- [x] 사이트 카테고리를 자료 유형이 아닌 학습 주제 중심으로 세분화
- [x] 44개 reference figure + 18개 paper-style figure + 실제 삽입 extra diagram을 정의·수식·수치 기준으로 전수 semantic audit
- [x] paper-style CNN convolution output 수치 오류 수정: 3×3 output 각 행 `[3, 3, 0]`
- [x] ViT patch-grid 축약 도식 / multi-head 의미 / attention heatmap이 합성 예시임을 명시
- [x] receptive field를 edge/part/object 의미와 자동 대응시키는 과도한 설명 제거
- [x] SVM support-vector 표시 좌표, Bayes likelihood 축 의미, VI/ELBO·MCMC 표현 교정
- [x] `논문 해설` 최상위 카테고리를 제거하고 주제 중심 구조로 재편
- [x] ResNet → CNN, U-Net → Vision Tasks에 병합; ViT·PatchCore는 Transformer/Anomaly Detection의 대표 논문으로 재프레이밍
- [x] 잘못된 시각 설명 교정: SVM hinge loss, augmentation 조건, DINO teacher/student 방향, PCA projection, HMM Viterbi, GMM, ensemble/MoE, IoU/NMS
- [x] CS231n multi-channel convolution / receptive field / ViT attention figure 추가
- [x] PRML Bernoulli-Binomial / ML-MAP figure 추가
- [x] CS231n 핵심 figure를 numeric matrix / chain rule / optimizer trajectory / LR curve / pooling / residual flow 중심으로 보강
- [x] PRML 핵심 figure를 entropy / posterior predictive uncertainty / importance sampling / PCA projection·reconstruction 중심으로 보강
- [x] CNN / ViT / PatchCore에 paper-style multi-panel figure 적용
- [x] CS231n / PRML에 대형 reference figure atlas 추가
- [x] `scripts/reference_figures.py` 추가
- [x] reference atlas를 CS231n 30개 + PRML 38개 = 총 68개 SVG로 확장
- [x] 기존 simple diagram 일부는 종합 페이지에서 중복되지 않도록 비활성화
- [x] build / validate / GitHub Pages deploy 성공
- [x] figure를 1열 전체 폭으로 표시하여 크기 문제 완화
- [x] 문장형 bullet panel 10개를 plot/matrix/graph/trajectory 중심 시각 패널로 교체
- [x] panel title 자동 축소, 모바일 reference figure 가로 스크롤, SVG 정적 QA guard 추가

---

## 현재 확인된 문제

- [x] 데스크톱 raster artifact 기준 SVG 내부 text overflow/겹침 전수 확인 및 발견 항목 교정
- [ ] figure 내부에 설명문이 너무 많아 축소 시 읽기 어렵다.
- [ ] 여러 figure가 box / pipeline / bar 형태로 비슷하게 보여 시각적 다양성이 부족하다.
- [ ] 일부 개념은 “그림 수”는 많지만 핵심 intuition을 보여주는 대표 figure가 부족하다.
- [ ] 일부 figure는 실제 plot/heatmap/feature map보다 개념 요약 카드에 가깝다.
- [ ] 모바일/좁은 화면에서 text와 panel spacing을 다시 확인해야 한다. (SVG 내부 Korean font fallback은 보강)
- [ ] 데스크톱 Pages artifact raster QA는 완료. 모바일 실제 브라우저의 scroll/spacing과 플랫폼별 Korean font fallback 최종 확인이 남아 있다.

### 공통 수정 원칙

- figure 내부에는 짧은 label만 둔다.
- 문장형 설명은 본문 또는 figcaption으로 이동한다.
- 한 panel은 한 메시지만 표현한다.
- 한 figure에 너무 많은 내용을 넣지 않는다.
- scatter / curve / histogram / matrix / heatmap / feature map / probability density / computational graph 등 개념에 맞는 표현을 다양하게 사용한다.
- figure 제목/패널 제목/label의 typography와 spacing을 통일한다.
- SVG text가 frame 밖으로 나가지 않도록 실제 렌더링 후 확인한다.
- 원 논문 figure를 그대로 복제하지 않고 개념을 독자 제작 figure로 재구성한다.

---

# 1. CS231n 개선 TODO

## 1-1. Image Classification

- [x] kNN failure example 추가/보강
  - 같은 의미의 이미지가 shift/lighting 때문에 pixel distance가 커지는 예시
  - 다른 의미인데 background 때문에 raw pixel distance가 작아지는 예시
- [x] train / validation / test split figure 개선
- [x] video / burst / near-duplicate 데이터의 leakage figure 추가
  - random frame split vs grouped split 비교
- [x] score → softmax probability → cross-entropy loss를 한 흐름으로 명확히 분리한 figure 추가

## 1-2. Linear Classifier / Loss

- [x] linear score `Wx+b`를 입력 vector와 weight matrix 관점에서 시각화
- [x] softmax와 hinge loss 비교 figure 개선
- [x] linear decision boundary vs nonlinear boundary 비교
- [x] regularization term이 data loss에 더해지는 구조를 별도 작은 figure로 설명

## 1-3. Optimization / Backpropagation

- [x] computational graph의 forward / backward 방향을 더 명확하게 표시
- [x] chain rule 숫자 예시 figure 추가
- [x] numerical gradient vs analytic gradient / gradient check figure 추가
- [x] SGD / Momentum / Adam을 같은 loss landscape 위 trajectory로 비교
- [x] learning rate too small / good / too large 비교
- [x] local minimum / saddle point / flat region 비교 figure 보강

## 1-4. Neural Networks / Training Tricks

- [x] sigmoid / tanh / ReLU / Leaky ReLU 함수 모양 비교
- [x] activation별 gradient 특성 표시
- [x] vanishing / exploding gradient figure 추가
- [x] initialization이 activation variance에 미치는 영향
- [x] BatchNorm train vs inference 차이
- [x] dropout train vs inference 구조
- [x] L2 weight decay 직관
- [x] underfit / good fit / overfit 학습곡선 비교
- [x] augmentation 전/후 예시를 더 이미지다운 형태로 표현

## 1-5. CNN

- [x] 3×3 convolution 실제 숫자 계산 figure
- [x] kernel sliding animation 느낌의 multi-panel figure
- [x] stride 1 vs 2
- [x] padding 0 vs same padding
- [x] dilation 비교
- [x] multi-channel convolution
  - RGB input
  - 3×3×3 filter
  - channel-wise sum
  - output feature map
- [x] output channel 여러 개가 여러 filter에서 생성되는 구조
- [x] receptive field growth
- [x] max pooling vs average pooling
- [x] early / middle / deep layer feature hierarchy
- [x] 실제 feature-map / edge-response 느낌의 synthetic visualization 추가

## 1-6. Architecture

- [x] LeNet / AlexNet / VGG / ResNet / ViT 비교 figure
- [x] plain block vs residual block
- [x] residual connection의 gradient flow
- [x] VGG의 repeated 3×3 stack intuition
- [x] architecture별 핵심 차이를 숫자표가 아닌 시각 구조로 비교

## 1-7. Understanding CNN

- [x] saliency map
- [x] activation maximization / filter visualization
- [x] Grad-CAM-style heatmap
- [x] feature map comparison
- [x] attribution visualization의 한계 설명 figure

## 1-8. Transfer Learning

- [x] frozen backbone
- [x] top-block fine-tuning
- [x] full fine-tuning
- [x] dataset size × domain gap에 따른 전략 matrix

## 1-9. Detection / Segmentation / Modern Vision

- [x] classification vs detection vs semantic segmentation vs instance segmentation
- [x] bbox IoU
- [x] NMS 단계별 figure
- [x] semantic vs instance mask
- [x] ViT patch embedding
- [x] positional embedding
- [x] Q/K/V self-attention
- [x] attention matrix / spatial heatmap
- [x] multi-head attention
- [x] CLIP image-text embedding alignment
- [x] DINO teacher-student / self-distillation
- [x] diffusion forward noise / reverse denoising

---

# 2. PRML 개선 TODO

## 2-1. Chapter 1 — Introduction

- [x] prior / likelihood / posterior를 서로 다른 density curve로 표현
- [x] Bayesian decision / expected risk
- [x] entropy / information intuition
- [x] posterior와 posterior predictive를 명확히 구분하는 figure

## 2-2. Chapter 2 — Probability Distributions

- [x] Gaussian mean 변화
- [x] Gaussian variance 변화
- [x] covariance ellipse
- [x] Bernoulli / Binomial 관계
- [x] Beta prior → observations → posterior
- [x] Dirichlet / multinomial intuition
- [x] maximum likelihood vs MAP 비교

## 2-3. Chapter 3 — Linear Models for Regression

- [x] raw linear regression
- [x] polynomial basis
- [x] Gaussian basis
- [x] sigmoid basis
- [x] regularization에 따른 curve 변화
- [x] Bayesian regression mean + uncertainty band
- [x] posterior predictive distribution

## 2-4. Chapter 4 — Linear Models for Classification

- [x] logistic sigmoid
- [x] binary decision boundary
- [x] multiclass softmax regions
- [x] generative vs discriminative
  - `p(x|C)p(C)`
  - `p(C|x)`
- [x] probit / logistic 차이의 직관적 설명 여부 검토

## 2-5. Chapter 5 — Neural Networks

- [x] hidden-layer nonlinear basis intuition
- [x] forward propagation
- [x] backpropagation
- [x] nonlinear decision boundary
- [x] regularization and early stopping

## 2-6. Chapter 6 — Kernel Methods

- [x] input space → feature space mapping
- [x] kernel trick
- [x] polynomial kernel
- [x] RBF kernel similarity 변화
- [x] Gaussian Process mean / uncertainty band
- [x] kernel matrix heatmap

## 2-7. Chapter 7 — Sparse Kernel Machines

- [x] SVM margin
- [x] support vectors 강조
- [x] hinge loss
- [x] soft margin / C parameter effect
- [x] RVM vs SVM sparsity intuition

## 2-8. Chapter 8 — Graphical Models

- [x] Bayesian network
- [x] Markov random field
- [x] factor graph
- [x] conditional independence
- [x] d-separation 대표 예시
- [x] message passing intuition

## 2-9. Chapter 9 — Mixture Models / EM

- [x] Gaussian mixture density
- [x] component별 cluster coloring
- [x] responsibility `r_nk`
- [x] E-step
- [x] M-step
- [x] EM iteration에 따라 mean/covariance가 이동하는 sequence figure

## 2-10. Chapter 10 — Approximate Inference

- [x] true posterior vs variational approximation
- [x] ELBO decomposition
  - expected log-likelihood
  - KL term
  - log evidence gap
- [x] mean-field factorization
- [x] coordinate ascent VI intuition
- [x] expectation propagation이 VI와 어떻게 다른지 간단 비교

## 2-11. Chapter 11 — Sampling Methods

- [x] Monte Carlo sampling
- [x] importance sampling
- [x] rejection sampling
- [x] MCMC random walk
- [x] burn-in
- [x] autocorrelation
- [x] effective sample size
- [x] HMC trajectory intuition

## 2-12. Chapter 12 — Continuous Latent Variables

- [x] PCA principal axis
- [x] 2D → 1D projection
- [x] reconstruction
- [x] eigenvalue / explained variance
- [x] PPCA generative model
- [x] factor analysis comparison
- [x] ICA intuition

## 2-13. Chapter 13 — Sequential Data

- [x] HMM hidden state / observation chain
- [x] filtering
- [x] prediction
- [x] smoothing
- [x] Viterbi decoding
- [x] Kalman filter predict/update
- [x] particle filter intuition

## 2-14. Chapter 14 — Combining Models

- [x] Bayesian model averaging
- [x] simple ensemble averaging
- [x] boosting intuition
- [x] decision tree / ensemble concept
- [x] mixture of experts
- [x] gating network
- [x] bias/variance reduction through ensembles

---

# 3. 품질 QA 체크리스트

각 figure를 생성한 뒤 아래를 실제 렌더링 결과 기준으로 확인한다.

- [ ] title/subtitle이 frame 밖으로 나가지 않는가?
- [ ] panel title이 겹치지 않는가?
- [ ] label이 다른 도형/arrow 위에 겹치지 않는가?
- [ ] 최소 글자 크기가 충분한가?
- [ ] 긴 문장이 figure 내부에 들어가 있지 않은가?
- [ ] 데스크톱 960px 본문 폭에서 읽을 수 있는가?
- [ ] 모바일에서는 가로 스크롤로 충분히 볼 수 있는가?
- [ ] 색상만으로 class/meaning을 구분하지 않는가?
- [ ] dark fill 위 text가 밝은 색으로 표시되는가?
- [ ] 하나의 panel이 하나의 메시지를 표현하는가?
- [ ] 같은 내용의 simple diagram이 중복 삽입되지 않는가?
- [ ] figure가 실제 해당 본문 바로 뒤에 위치하는가?
- [ ] caption이 figure에서 보이는 내용과 정확히 일치하는가?
- [ ] 논문 결과처럼 보이는 synthetic plot은 실제 측정 결과로 오해되지 않도록 caption에서 예시임을 표시하는가?

---

# 4. 수정 대상 파일

다음 세션에서는 최신 상태를 먼저 조회한 뒤 아래 파일을 중심으로 작업한다.

- `scripts/reference_figures.py`
  - CS231n / PRML reference SVG 생성 소스
- `scripts/build.py`
  - `REFERENCE_VISUALS` 및 section figure 삽입
- `scripts/cs231n_note.py`
  - CS231n 본문/섹션 구조
- `scripts/prml_note.py`
  - PRML 본문/섹션 구조
- `assets/site.css`
  - figure 크기 / caption / mobile overflow
- `scripts/validate.py`
  - figure 개수 및 SVG validation
- `PROJECT_CONTEXT.md`
  - 최종 시각자료 작성 규칙

생성된 `notes/*.html`이나 `assets/diagrams/reference/*.svg`를 source of truth로 직접 편집하지 말고,
가능한 한 generator / build source를 수정한다.

---

# 5. 다음 세션 권장 작업 순서

- [ ] GitHub Connector 확인
- [ ] `sh0427-han/vision_ai` 최신 main 조회
- [ ] 이 `TODO.md` 확인
- [ ] `scripts/reference_figures.py` 및 현재 `REFERENCE_VISUALS` 확인
- [ ] 배포 artifact를 raster render하여 CS231n / PRML + paper-style figure 최종 visual QA
- [ ] 텍스트 overflow / clipping / 중복 figure 우선 수정
- [ ] 위 누락 figure 중 흐름상 필수 항목 추가
- [ ] build 실행
- [ ] validate 실행
- [ ] PR 생성
- [ ] merge
- [ ] GitHub Pages deploy 성공 확인
- [ ] 배포 페이지에서 CS231n / PRML 최종 시각 검토

---

## 완료 기준

CS231n / PRML 페이지를 처음 보는 사람이 본문만 읽기 전에 figure를 훑어도
각 장의 핵심 개념 흐름을 이해할 수 있고, figure 안의 모든 텍스트가 겹침 없이 읽히며,
각 개념에 적합한 plot / matrix / heatmap / graph / architecture figure가 충분히 배치되어 있는 상태를 목표로 한다.

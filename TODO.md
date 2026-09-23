# TODO — CS231n / PRML 시각자료 품질 개선

> Repository: https://github.com/sh0427-han/vision_ai  
> Pages: https://sh0427-han.github.io/vision_ai/  
> TODO 작성 시점의 main commit: `d8f6f5d19fedd08c2aafed2b86ccd156c5f4bbc8`

## 작업 목적

CS231n과 PRML(Christopher Bishop, *Pattern Recognition and Machine Learning*) 종합 학습 페이지의 시각자료를
단순 box-arrow diagram 수준에서 벗어나, 논문/대학 강의자료처럼 직관적이고 실제 개념을 설명하는 figure 중심으로 개선한다.

다음 세션에서는 과거 대화나 로컬 ZIP을 기준으로 덮어쓰지 말고 반드시 GitHub Connector로 최신 `main`을 먼저 조회한 뒤 작업한다.

---

## 현재 완료 상태

- [x] CNN / ViT / PatchCore에 paper-style multi-panel figure 적용
- [x] CS231n / PRML에 대형 reference figure atlas 추가
- [x] `scripts/reference_figures.py` 추가
- [x] 현재 main 기준 CS231n 22개 + PRML 19개 = 총 41개 reference SVG 생성
- [x] 기존 simple diagram 일부는 종합 페이지에서 중복되지 않도록 비활성화
- [x] build / validate / GitHub Pages deploy 성공
- [x] figure를 1열 전체 폭으로 표시하여 크기 문제 완화
- [x] 문장형 bullet panel 10개를 plot/matrix/graph/trajectory 중심 시각 패널로 교체
- [x] panel title 자동 축소, 모바일 reference figure 가로 스크롤, SVG 정적 QA guard 추가

---

## 현재 확인된 문제

- [ ] 일부 SVG 내부 텍스트가 패널 경계/도형과 겹치거나 잘린다.
- [ ] figure 내부에 설명문이 너무 많아 축소 시 읽기 어렵다.
- [ ] 여러 figure가 box / pipeline / bar 형태로 비슷하게 보여 시각적 다양성이 부족하다.
- [ ] 일부 개념은 “그림 수”는 많지만 핵심 intuition을 보여주는 대표 figure가 부족하다.
- [ ] 일부 figure는 실제 plot/heatmap/feature map보다 개념 요약 카드에 가깝다.
- [ ] 모바일/좁은 화면에서 text와 panel spacing을 다시 확인해야 한다.
- [ ] 모든 figure를 실제 렌더링 이미지로 육안 QA하지 않았다.

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

- [ ] linear score `Wx+b`를 입력 vector와 weight matrix 관점에서 시각화
- [x] softmax와 hinge loss 비교 figure 개선
- [ ] linear decision boundary vs nonlinear boundary 비교
- [ ] regularization term이 data loss에 더해지는 구조를 별도 작은 figure로 설명

## 1-3. Optimization / Backpropagation

- [ ] computational graph의 forward / backward 방향을 더 명확하게 표시
- [ ] chain rule 숫자 예시 figure 추가
- [ ] numerical gradient vs analytic gradient / gradient check figure 추가
- [ ] SGD / Momentum / Adam을 같은 loss landscape 위 trajectory로 비교
- [ ] learning rate too small / good / too large 비교
- [ ] local minimum / saddle point / flat region 비교 figure 보강

## 1-4. Neural Networks / Training Tricks

- [x] sigmoid / tanh / ReLU / Leaky ReLU 함수 모양 비교
- [x] activation별 gradient 특성 표시
- [ ] vanishing / exploding gradient figure 추가
- [ ] initialization이 activation variance에 미치는 영향
- [x] BatchNorm train vs inference 차이
- [ ] dropout train vs inference 구조
- [ ] L2 weight decay 직관
- [ ] underfit / good fit / overfit 학습곡선 비교
- [x] augmentation 전/후 예시를 더 이미지다운 형태로 표현

## 1-5. CNN

- [x] 3×3 convolution 실제 숫자 계산 figure
- [ ] kernel sliding animation 느낌의 multi-panel figure
- [ ] stride 1 vs 2
- [ ] padding 0 vs same padding
- [ ] dilation 비교
- [ ] multi-channel convolution
  - RGB input
  - 3×3×3 filter
  - channel-wise sum
  - output feature map
- [ ] output channel 여러 개가 여러 filter에서 생성되는 구조
- [ ] receptive field growth
- [ ] max pooling vs average pooling
- [ ] early / middle / deep layer feature hierarchy
- [ ] 실제 feature-map / edge-response 느낌의 synthetic visualization 추가

## 1-6. Architecture

- [ ] LeNet / AlexNet / VGG / ResNet / ViT 비교 figure
- [ ] plain block vs residual block
- [ ] residual connection의 gradient flow
- [ ] VGG의 repeated 3×3 stack intuition
- [ ] architecture별 핵심 차이를 숫자표가 아닌 시각 구조로 비교

## 1-7. Understanding CNN

- [ ] saliency map
- [ ] activation maximization / filter visualization
- [ ] Grad-CAM-style heatmap
- [ ] feature map comparison
- [ ] attribution visualization의 한계 설명 figure

## 1-8. Transfer Learning

- [ ] frozen backbone
- [ ] top-block fine-tuning
- [ ] full fine-tuning
- [ ] dataset size × domain gap에 따른 전략 matrix

## 1-9. Detection / Segmentation / Modern Vision

- [ ] classification vs detection vs semantic segmentation vs instance segmentation
- [ ] bbox IoU
- [ ] NMS 단계별 figure
- [ ] semantic vs instance mask
- [ ] ViT patch embedding
- [ ] positional embedding
- [ ] Q/K/V self-attention
- [ ] attention matrix / spatial heatmap
- [ ] multi-head attention
- [x] CLIP image-text embedding alignment
- [x] DINO teacher-student / self-distillation
- [x] diffusion forward noise / reverse denoising

---

# 2. PRML 개선 TODO

## 2-1. Chapter 1 — Introduction

- [ ] prior / likelihood / posterior를 서로 다른 density curve로 표현
- [ ] Bayesian decision / expected risk
- [ ] entropy / information intuition
- [ ] posterior와 posterior predictive를 명확히 구분하는 figure

## 2-2. Chapter 2 — Probability Distributions

- [x] Gaussian mean 변화
- [x] Gaussian variance 변화
- [x] covariance ellipse
- [ ] Bernoulli / Binomial 관계
- [x] Beta prior → observations → posterior
- [ ] Dirichlet / multinomial intuition
- [ ] maximum likelihood vs MAP 비교

## 2-3. Chapter 3 — Linear Models for Regression

- [ ] raw linear regression
- [x] polynomial basis
- [x] Gaussian basis
- [x] sigmoid basis
- [ ] regularization에 따른 curve 변화
- [ ] Bayesian regression mean + uncertainty band
- [ ] posterior predictive distribution

## 2-4. Chapter 4 — Linear Models for Classification

- [ ] logistic sigmoid
- [ ] binary decision boundary
- [ ] multiclass softmax regions
- [ ] generative vs discriminative
  - `p(x|C)p(C)`
  - `p(C|x)`
- [ ] probit / logistic 차이의 직관적 설명 여부 검토

## 2-5. Chapter 5 — Neural Networks

- [ ] hidden-layer nonlinear basis intuition
- [ ] forward propagation
- [ ] backpropagation
- [ ] nonlinear decision boundary
- [ ] regularization and early stopping

## 2-6. Chapter 6 — Kernel Methods

- [ ] input space → feature space mapping
- [ ] kernel trick
- [ ] polynomial kernel
- [ ] RBF kernel similarity 변화
- [ ] Gaussian Process mean / uncertainty band
- [ ] kernel matrix heatmap

## 2-7. Chapter 7 — Sparse Kernel Machines

- [ ] SVM margin
- [ ] support vectors 강조
- [ ] hinge loss
- [ ] soft margin / C parameter effect
- [ ] RVM vs SVM sparsity intuition

## 2-8. Chapter 8 — Graphical Models

- [ ] Bayesian network
- [ ] Markov random field
- [x] factor graph
- [ ] conditional independence
- [ ] d-separation 대표 예시
- [ ] message passing intuition

## 2-9. Chapter 9 — Mixture Models / EM

- [ ] Gaussian mixture density
- [ ] component별 cluster coloring
- [ ] responsibility `r_nk`
- [ ] E-step
- [ ] M-step
- [ ] EM iteration에 따라 mean/covariance가 이동하는 sequence figure

## 2-10. Chapter 10 — Approximate Inference

- [x] true posterior vs variational approximation
- [ ] ELBO decomposition
  - expected log-likelihood
  - KL term
  - log evidence gap
- [ ] mean-field factorization
- [ ] coordinate ascent VI intuition
- [ ] expectation propagation이 VI와 어떻게 다른지 간단 비교

## 2-11. Chapter 11 — Sampling Methods

- [x] Monte Carlo sampling
- [ ] importance sampling
- [ ] rejection sampling
- [x] MCMC random walk
- [x] burn-in
- [ ] autocorrelation
- [ ] effective sample size
- [ ] HMC trajectory intuition

## 2-12. Chapter 12 — Continuous Latent Variables

- [ ] PCA principal axis
- [ ] 2D → 1D projection
- [ ] reconstruction
- [ ] eigenvalue / explained variance
- [ ] PPCA generative model
- [ ] factor analysis comparison
- [ ] ICA intuition

## 2-13. Chapter 13 — Sequential Data

- [ ] HMM hidden state / observation chain
- [x] filtering
- [x] prediction
- [x] smoothing
- [x] Viterbi decoding
- [ ] Kalman filter predict/update
- [ ] particle filter intuition

## 2-14. Chapter 14 — Combining Models

- [ ] Bayesian model averaging
- [ ] simple ensemble averaging
- [ ] boosting intuition
- [ ] decision tree / ensemble concept
- [ ] mixture of experts
- [ ] gating network
- [ ] bias/variance reduction through ensembles

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
- [ ] CS231n / PRML 현재 생성 figure 전부 렌더링하여 visual QA
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

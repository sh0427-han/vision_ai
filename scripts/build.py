"""Build a dependency-free Korean vision AI study site from authored HTML sections."""
from html import escape
from pathlib import Path
import re

from reference_notes import register_reference_notes
from extra_diagrams import build_extra_diagrams, EXTRA_DIAGRAM_META
from paper_figures import build_paper_figures, PAPER_FIGURE_META
from reference_figures import build_reference_figures, REFERENCE_FIGURE_META, REFERENCE_VISUALS


ROOT = Path(__file__).resolve().parents[1]
NOTES = []

EQUATION_TEX = {
    "x_scaled = x_uint8 / 255\nx_normalized = (x_scaled − mean) / std": r"""
\begin{aligned}
x_{\mathrm{scaled}} &= \frac{x_{\mathrm{uint8}}}{255} \\
x_{\mathrm{normalized}} &= \frac{x_{\mathrm{scaled}}-\mu}{\sigma}
\end{aligned}
""",
    "출력[y, x] = Σ 입력[y+i, x+j] × 커널[i, j] + bias\n예시 커널 = [[−1, 0, 1], [−1, 0, 1], [−1, 0, 1]]": r"""
\begin{aligned}
Y[y,x] &= \sum_{i=0}^{2}\sum_{j=0}^{2} X[y+i,x+j]K[i,j] + b \\
K &= \begin{bmatrix}-1&0&1\\-1&0&1\\-1&0&1\end{bmatrix}
\end{aligned}
""",
    "H_out = floor((H + 2P − D(K−1) − 1) / S + 1)\nW_out도 같은 방식으로 계산\nH=224, K=3, P=1, D=1, S=2 → H_out=112": r"""
\begin{aligned}
H_{\mathrm{out}} &= \left\lfloor \frac{H+2P-D(K-1)-1}{S}+1 \right\rfloor \\
H=224,\ K=3,\ P=1,\ D=1,\ S=2 &\Rightarrow H_{\mathrm{out}}=112
\end{aligned}
""",
    "N = (H/P) × (W/P)\npatch_flat: [B, N, P²C]\nembedding = patch_flat × E + bias\nE: [P²C, D] → output: [B, N, D]": r"""
\begin{aligned}
N &= \frac{H}{P}\times\frac{W}{P} \\
X_{\mathrm{patch}} &\in \mathbb{R}^{B\times N\times P^2C} \\
Z &= X_{\mathrm{patch}}E+b,\qquad E\in\mathbb{R}^{P^2C\times D} \\
Z &\in \mathbb{R}^{B\times N\times D}
\end{aligned}
""",
    "z₀ = [CLS; patch₁E; …; patch₁₉₆E] + E_position\nshape: [B, 197, 768]": r"""
z_0 =
\left[
x_{\mathrm{CLS}};
x_p^1E;
\ldots;
x_p^{196}E
\right]
+ E_{\mathrm{pos}},
\qquad
z_0\in\mathbb{R}^{B\times197\times768}
""",
    "Q = XW_Q,  K = XW_K,  V = XW_V\nAttention(Q,K,V) = softmax(QKᵀ / √d_k) V": r"""
\begin{aligned}
Q &= XW_Q,\qquad K=XW_K,\qquad V=XW_V \\
\operatorname{Attention}(Q,K,V)
&=
\operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\end{aligned}
""",
    "z′ = z + MSA(LN(z))\nz_next = z′ + MLP(LN(z′))": r"""
\begin{aligned}
z' &= z + \operatorname{MSA}(\operatorname{LN}(z)) \\
z_{\mathrm{next}} &= z' + \operatorname{MLP}(\operatorname{LN}(z'))
\end{aligned}
""",
    "IoU = |예측 ∩ 정답| / |예측 ∪ 정답|\nDice = 2|예측 ∩ 정답| / (|예측| + |정답|)": r"""
\begin{aligned}
\operatorname{IoU} &= \frac{|P\cap G|}{|P\cup G|} \\
\operatorname{Dice} &= \frac{2|P\cap G|}{|P|+|G|}
\end{aligned}
""",
    "Precision = TP / (TP + FP)\nRecall = TP / (TP + FN)\nF1 = 2TP / (2TP + FP + FN)": r"""
\begin{aligned}
\operatorname{Precision} &= \frac{TP}{TP+FP} \\
\operatorname{Recall} &= \frac{TP}{TP+FN} \\
F_1 &= \frac{2TP}{2TP+FP+FN}
\end{aligned}
""",
    "합산 전 목표: H(x) = x + F(x)\n단순한 합산 경로의 미분: ∂H/∂x = I + ∂F/∂x": r"""
\begin{aligned}
H(x) &= x+F(x) \\
\frac{\partial H}{\partial x} &= I+\frac{\partial F}{\partial x}
\end{aligned}
""",
    "한 픽셀의 cross-entropy = −log p(정답 클래스)\np=0.8 → loss≈0.223 / p=0.2 → loss≈1.609": r"""
\begin{aligned}
\mathcal{L}_{\mathrm{CE}} &= -\log p_y \\
p_y=0.8 &\Rightarrow \mathcal{L}\approx0.223 \\
p_y=0.2 &\Rightarrow \mathcal{L}\approx1.609
\end{aligned}
""",
    "Memory ≈ 이미지 수 × 특징 위치 수 × 특징 차원 × 원소 bytes\n1,000 × 784 × 1,024 × 4 ≈ 3.21 GB": r"""
\begin{aligned}
M &\approx N_{\mathrm{img}}\times N_{\mathrm{loc}}\times D_{\mathrm{feat}}\times B_{\mathrm{elem}} \\
1000\times784\times1024\times4 &\approx 3.21\ \mathrm{GB}
\end{aligned}
""",
    "패치 점수 sᵢ = min_{m ∈ M} ||fᵢ − m||₂\nM: 정상 특징 저장소 / fᵢ: 검사 이미지 i번째 지역 특징": r"""
s_i = \min_{m\in\mathcal{M}}\left\|f_i-m\right\|_2,
\qquad
\mathcal{M}=\text{normal feature memory bank}
""",
    "L1 거리 = Σᵢ |xᵢ − yᵢ|\nL2 거리 = √(Σᵢ (xᵢ − yᵢ)²)": r"""
\begin{aligned}
d_{L1}(x,y) &= \sum_i |x_i-y_i| \\
d_{L2}(x,y) &= \sqrt{\sum_i (x_i-y_i)^2}
\end{aligned}
""",
    "scores = W x + b\nx: [D] / W: [K, D] / b: [K] / scores: [K]": r"""
s = Wx+b,
\qquad
x\in\mathbb{R}^{D},\
W\in\mathbb{R}^{K\times D},\
b\in\mathbb{R}^{K},\
s\in\mathbb{R}^{K}
""",
    "Softmax: p_k = exp(s_k) / Σ_j exp(s_j)\nCross-entropy: L = −log p_y\nSVM hinge: L_i = Σ_{j≠y} max(0, s_j − s_y + Δ)": r"""
\begin{aligned}
p_k &= \frac{e^{s_k}}{\sum_j e^{s_j}} \\
\mathcal{L}_{\mathrm{CE}} &= -\log p_y \\
\mathcal{L}^{(i)}_{\mathrm{hinge}}
&= \sum_{j\ne y_i}\max(0,s_j-s_{y_i}+\Delta)
\end{aligned}
""",
    "수치 미분(중앙 차분):\ndf/dx ≈ [f(x+h) − f(x−h)] / (2h)\n\nSGD update:\nW ← W − learning_rate × ∂L/∂W": r"""
\begin{aligned}
\frac{df}{dx} &\approx \frac{f(x+h)-f(x-h)}{2h} \\
W &\leftarrow W-\eta\frac{\partial\mathcal{L}}{\partial W}
\end{aligned}
""",
    "Momentum 예시:\nv_t = μ v_{t−1} − η ∇L(W_t)\nW_{t+1} = W_t + v_t": r"""
\begin{aligned}
v_t &= \mu v_{t-1}-\eta\nabla\mathcal{L}(W_t) \\
W_{t+1} &= W_t+v_t
\end{aligned}
""",
    "H_out = floor((H + 2P − D(K−1) − 1) / S + 1)\nParams = C_out × C_in × K_h × K_w + C_out(bias)": r"""
\begin{aligned}
H_{\mathrm{out}}
&=
\left\lfloor\frac{H+2P-D(K-1)-1}{S}+1\right\rfloor \\
N_{\mathrm{params}}
&=
C_{\mathrm{out}}C_{\mathrm{in}}K_hK_w+C_{\mathrm{out}}
\end{aligned}
""",
    "DINO teacher update 개념:\nθ_teacher ← τ θ_teacher + (1−τ) θ_student\n\nCLIP contrastive 개념:\nmatched image-text similarity ↑ / mismatched similarity ↓": r"""
\begin{aligned}
\theta_{\mathrm{teacher}}
&\leftarrow
\tau\theta_{\mathrm{teacher}}
+(1-\tau)\theta_{\mathrm{student}} \\
\operatorname{sim}(I_i,T_i)&\uparrow,\qquad
\operatorname{sim}(I_i,T_j)&\downarrow\quad(i\ne j)
\end{aligned}
""",
    "Bayes theorem:\np(w|D) = p(D|w)p(w) / p(D)\n\nposterior ∝ likelihood × prior": r"""
p(w\mid D)
=
\frac{p(D\mid w)p(w)}{p(D)}
\qquad\Longrightarrow\qquad
\text{posterior}\propto\text{likelihood}\times\text{prior}
""",
    "Entropy: H[p] = −Σ_x p(x) log p(x)\nKL(q || p) = Σ_x q(x) log(q(x)/p(x))": r"""
\begin{aligned}
H[p] &= -\sum_x p(x)\log p(x) \\
D_{\mathrm{KL}}(q\|p)
&=
\sum_x q(x)\log\frac{q(x)}{p(x)}
\end{aligned}
""",
    "Beta-Binomial update:\nprior Beta(a,b) + successes m / failures l\n→ posterior Beta(a+m, b+l)": r"""
\operatorname{Beta}(a,b)
\;+\;
(m\ \text{successes},\ \ell\ \text{failures})
\;\Longrightarrow\;
\operatorname{Beta}(a+m,b+\ell)
""",
    "y(x, w) = wᵀ φ(x)\nt = y(x,w) + ε,   ε ~ N(0, β⁻¹)": r"""
\begin{aligned}
y(x,w) &= w^\top\phi(x) \\
t &= y(x,w)+\varepsilon,\qquad
\varepsilon\sim\mathcal{N}(0,\beta^{-1})
\end{aligned}
""",
    "Binary logistic regression:\np(C₁|x) = σ(wᵀx + b)\nσ(a) = 1 / (1 + exp(−a))": r"""
\begin{aligned}
p(C_1\mid x) &= \sigma(w^\top x+b) \\
\sigma(a) &= \frac{1}{1+e^{-a}}
\end{aligned}
""",
    "한 hidden layer 예:\na_j = Σ_i w⁽¹⁾_{ji} x_i + b_j\nz_j = h(a_j)\ny_k = Σ_j w⁽²⁾_{kj} z_j + c_k": r"""
\begin{aligned}
a_j &= \sum_i w^{(1)}_{ji}x_i+b_j \\
z_j &= h(a_j) \\
y_k &= \sum_j w^{(2)}_{kj}z_j+c_k
\end{aligned}
""",
    "k(x, x′) = φ(x)ᵀ φ(x′)\nRBF kernel = exp(−||x−x′||² / (2σ²))": r"""
\begin{aligned}
k(x,x') &= \phi(x)^\top\phi(x') \\
k_{\mathrm{RBF}}(x,x')
&=
\exp\left(-\frac{\|x-x'\|^2}{2\sigma^2}\right)
\end{aligned}
""",
    "Binary hinge loss:\nL = max(0, 1 − y f(x)),   y ∈ {−1, +1}": r"""
\mathcal{L}_{\mathrm{hinge}}
=
\max(0,1-yf(x)),
\qquad
y\in\{-1,+1\}
""",
    "Bayesian network factorization 예:\np(x₁,...,x_K) = ∏_k p(x_k | parents(x_k))": r"""
p(x_1,\ldots,x_K)
=
\prod_{k=1}^{K}
p\!\left(x_k\mid\operatorname{pa}(x_k)\right)
""",
    "p(x) = Σ_k π_k N(x | μ_k, Σ_k)\nresponsibility γ(z_k) = p(z_k=1 | x)": r"""
\begin{aligned}
p(x) &= \sum_{k=1}^{K}\pi_k\,
\mathcal{N}(x\mid\mu_k,\Sigma_k) \\
\gamma(z_k) &= p(z_k=1\mid x)
\end{aligned}
""",
    "log p(X) = ELBO(q) + KL(q(Z) || p(Z|X))\nELBO(q) ≤ log p(X)": r"""
\begin{aligned}
\log p(X)
&=
\operatorname{ELBO}(q)
+
D_{\mathrm{KL}}\!\left(q(Z)\|p(Z\mid X)\right) \\
\operatorname{ELBO}(q) &\le \log p(X)
\end{aligned}
""",
    "Monte Carlo expectation:\nE_p[f(x)] ≈ (1/N) Σ_{n=1}^N f(x⁽ⁿ⁾),\nx⁽ⁿ⁾ ~ p(x)": r"""
\mathbb{E}_{p}[f(x)]
\approx
\frac{1}{N}\sum_{n=1}^{N}f(x^{(n)}),
\qquad
x^{(n)}\sim p(x)
""",
    "PPCA 생성 모델:\nz ~ N(0, I)\nx = Wz + μ + ε,   ε ~ N(0, σ²I)": r"""
\begin{aligned}
z &\sim \mathcal{N}(0,I) \\
x &= Wz+\mu+\varepsilon,\qquad
\varepsilon\sim\mathcal{N}(0,\sigma^2I)
\end{aligned}
""",
    "1차 Markov 가정:\np(z_t | z₁,...,z_{t−1}) = p(z_t | z_{t−1})": r"""
p(z_t\mid z_1,\ldots,z_{t-1})
=
p(z_t\mid z_{t-1})
""",
    "Committee 평균 예:\ny_COM(x) = (1/M) Σ_m y_m(x)": r"""
y_{\mathrm{COM}}(x)
=
\frac{1}{M}\sum_{m=1}^{M}y_m(x)
""",
}

PAGE_TERMS = {
    "pixels": [
        ("RGB", "Red, Green, Blue", "빨강·초록·파랑의 세 색상 채널"),
        ("BGR", "Blue, Green, Red", "OpenCV에서 흔히 사용하는 파랑·초록·빨강 채널 순서"),
        ("NCHW", "Batch, Channel, Height, Width", "딥러닝 텐서의 배치·채널·높이·너비 순서"),
        ("dtype", "data type", "숫자를 저장하는 자료형"),
        ("Tensor", "Tensor", "여러 축을 가진 숫자 배열"),
    ],
    "cnn": [
        ("CNN", "Convolutional Neural Network", "합성곱 신경망"),
        ("Conv", "Convolution", "합성곱 연산 또는 합성곱 층"),
        ("ReLU", "Rectified Linear Unit", "음수는 0, 양수는 그대로 두는 활성화 함수"),
        ("Kernel", "Convolution kernel", "입력의 작은 영역에 반복 적용하는 학습 가중치"),
        ("Stride", "Stride", "커널이 한 번에 이동하는 칸 수"),
        ("Padding", "Padding", "입력 가장자리에 값을 덧붙여 공간 크기를 조절하는 방법"),
        ("Feature map", "Feature map", "필터 반응이 공간 위치별로 기록된 출력 배열"),
        ("Receptive field", "Receptive field", "한 출력 값이 영향을 받을 수 있는 입력 영역"),
        ("ResNet", "Residual Network", "residual connection을 사용하는 CNN architecture"),
        ("BN", "Batch Normalization", "미니배치 통계를 이용하는 정규화 층"),
        ("Residual", "Residual", "블록이 학습하는 F(x)=H(x)-x 형태의 잔차 함수"),
        ("Shortcut", "Shortcut connection", "일부 층을 우회해 입력을 합산 지점으로 전달하는 경로"),
    ],
    "vit": [
        ("ViT", "Vision Transformer", "이미지를 패치 토큰으로 처리하는 Transformer 계열 모델"),
        ("CLS", "Classification token", "이미지 전체 분류 정보를 모으기 위해 추가하는 학습 토큰"),
        ("Q / K / V", "Query / Key / Value", "Self-Attention에서 비교와 정보 혼합에 사용하는 세 벡터"),
        ("MSA", "Multi-Head Self-Attention", "여러 Attention head를 병렬로 사용하는 연산"),
        ("LN", "Layer Normalization", "한 샘플 내부 특징을 정규화하는 층"),
        ("MLP", "Multi-Layer Perceptron", "여러 완전연결층으로 구성된 신경망 블록"),
        ("Patch", "Image patch", "이미지를 일정 크기로 잘라 만든 작은 조각"),
        ("Token", "Token", "Transformer가 한 단위로 처리하는 벡터"),
        ("Embedding", "Embedding", "원래 데이터를 모델이 계산하기 좋은 벡터 표현으로 바꾼 값"),
        ("Self-Attention", "Self-Attention", "같은 입력 안의 token들이 서로 어떤 정보를 참고할지 계산하는 연산"),
    ],
    "tasks": [
        ("IoU", "Intersection over Union", "예측 영역과 정답 영역의 교집합을 합집합으로 나눈 값"),
        ("NMS", "Non-Maximum Suppression", "겹치는 검출 상자 중 중복 후보를 제거하는 후처리"),
        ("Classification", "Classification", "이미지 전체가 어떤 클래스인지 맞히는 문제"),
        ("Detection", "Object Detection", "객체의 클래스와 위치 상자를 함께 찾는 문제"),
        ("Segmentation", "Segmentation", "픽셀 단위로 객체 영역을 구분하는 문제"),
        ("U-Net", "U-shaped Network", "encoder와 decoder를 대칭적으로 연결한 segmentation architecture"),
        ("Encoder", "Encoder", "해상도를 줄이며 context feature를 추출하는 경로"),
        ("Decoder", "Decoder", "해상도를 복원하며 dense prediction을 만드는 경로"),
        ("Skip connection", "Skip connection", "encoder feature를 decoder로 전달하는 연결"),
        ("Concat", "Concatenation", "tensor를 channel 방향 등으로 이어 붙이는 연산"),
    ],
    "training": [
        ("TP / FP / FN / TN", "True Positive / False Positive / False Negative / True Negative", "이진 분류 결과를 네 경우로 나눈 혼동행렬 용어"),
        ("CV", "Cross-Validation", "데이터 분할을 바꾸어 여러 번 평가하는 교차검증"),
        ("ROC", "Receiver Operating Characteristic", "threshold 변화에 따른 TPR과 FPR 관계 곡선"),
        ("AUC", "Area Under the Curve", "곡선 아래 면적을 요약한 값"),
        ("Threshold", "Decision threshold", "연속 점수를 정상/이상 같은 최종 판단으로 바꾸는 기준값"),
        ("Precision", "Precision", "이상이라고 예측한 것 중 실제 이상인 비율"),
        ("Recall", "Recall", "실제 이상 중 모델이 찾아낸 비율"),
        ("Data leakage", "Data leakage", "평가 데이터 정보가 학습 과정에 새어 들어가는 문제"),
    ],
    "patchcore": [
        ("CNN", "Convolutional Neural Network", "지역 특징을 추출하는 합성곱 신경망"),
        ("GB", "Gigabyte", "약 10억 byte 크기의 저장 용량 단위"),
        ("Memory bank", "Feature memory bank", "정상 데이터에서 추출한 특징 벡터를 저장한 집합"),
        ("Coreset", "Coreset", "전체 특징을 대표하도록 선택한 작은 부분집합"),
        ("Nearest neighbor", "Nearest neighbor", "특징 공간에서 가장 가까운 정상 특징"),
    ],
    "cs231n": [
        ("CS231n", "Stanford CS231n: Deep Learning for Computer Vision", "Stanford의 컴퓨터 비전 딥러닝 강의"),
        ("kNN", "k-Nearest Neighbors", "가장 가까운 k개 샘플을 이용하는 방법"),
        ("SVM", "Support Vector Machine", "margin을 이용해 분류 경계를 학습하는 모델"),
        ("SGD", "Stochastic Gradient Descent", "미니배치 gradient로 파라미터를 갱신하는 최적화 방법"),
        ("CNN", "Convolutional Neural Network", "합성곱 신경망"),
        ("BN", "Batch Normalization", "미니배치 통계를 이용하는 정규화 층"),
        ("SSL", "Self-Supervised Learning", "사람이 붙인 정답 라벨 없이 학습 신호를 만드는 자기지도학습"),
        ("CLIP", "Contrastive Language–Image Pre-training", "이미지와 텍스트 표현을 함께 학습하는 모델"),
        ("DINO", "self-DIstillation with NO labels", "라벨 없이 teacher–student 방식으로 표현을 학습하는 방법"),
        ("FLOPs", "Floating-Point Operations", "모델 계산량을 나타낼 때 쓰는 부동소수점 연산 수"),
        ("Logit", "Logit / raw class score", "softmax를 적용하기 전 클래스별 원시 점수"),
        ("Loss", "Loss function", "예측이 정답과 얼마나 다른지 수치로 표현한 값"),
        ("Gradient", "Gradient", "파라미터를 조금 바꿨을 때 loss가 어느 방향으로 변하는지 나타내는 값"),
        ("Backpropagation", "Backpropagation", "chain rule을 이용해 뒤쪽부터 gradient를 계산하는 방법"),
    ],
    "prml": [
        ("PRML", "Pattern Recognition and Machine Learning", "Christopher M. Bishop의 패턴인식·머신러닝 교재"),
        ("Prior", "Prior distribution", "데이터를 보기 전에 가진 파라미터에 대한 믿음"),
        ("Likelihood", "Likelihood", "주어진 파라미터에서 관측 데이터가 나타날 가능도를 보는 함수"),
        ("Posterior", "Posterior distribution", "데이터를 본 뒤 갱신된 파라미터 분포"),
        ("Latent variable", "Latent variable", "모델에는 존재하지만 직접 관측되지 않는 숨은 변수"),
        ("ML", "Maximum Likelihood", "이 문서 문맥에서는 가능도를 최대화하는 최대우도 추정"),
        ("MAP", "Maximum A Posteriori", "사후확률을 최대화하는 추정"),
        ("RBF", "Radial Basis Function", "거리 기반 방사형 기저 함수"),
        ("GP", "Gaussian Process", "함수에 대한 확률분포를 정의하는 가우시안 프로세스"),
        ("SVM", "Support Vector Machine", "support vector와 margin을 이용하는 분류 모델"),
        ("RVM", "Relevance Vector Machine", "Bayesian 관점의 희소 커널 모델"),
        ("MRF", "Markov Random Field", "무방향 그래프로 변수 의존성을 표현하는 모델"),
        ("GMM", "Gaussian Mixture Model", "여러 Gaussian 분포를 섞어 데이터를 표현하는 모델"),
        ("EM", "Expectation-Maximization", "숨은 변수 추정과 파라미터 갱신을 반복하는 알고리즘"),
        ("ELBO", "Evidence Lower Bound", "log evidence의 하한"),
        ("KL", "Kullback–Leibler divergence", "두 확률분포 차이를 나타내는 발산량"),
        ("VAE", "Variational Autoencoder", "변분 추론을 사용하는 생성 모델"),
        ("MCMC", "Markov Chain Monte Carlo", "Markov chain을 이용한 Monte Carlo sampling"),
        ("PCA", "Principal Component Analysis", "주성분 분석"),
        ("PPCA", "Probabilistic PCA", "PCA의 확률적 잠재변수 모델"),
        ("ICA", "Independent Component Analysis", "독립 성분 분석"),
        ("HMM", "Hidden Markov Model", "숨은 Markov 상태와 관측을 연결하는 시계열 모델"),
        ("LDS", "Linear Dynamical System", "연속 잠재 상태를 갖는 선형 동역학 모델"),
        ("MoE", "Mixture of Experts", "여러 expert와 gating을 결합하는 구조"),
    ],
}


TERM_ALIASES = {
    ("pixels", "Tensor"): r"(?:텐서|Tensor)",
    ("cnn", "Kernel"): r"(?:커널|Kernel)",
    ("cnn", "Stride"): r"(?:stride|Stride)",
    ("cnn", "Padding"): r"(?:padding|Padding)",
    ("vit", "Q / K / V"): r"Q\s*[·/]\s*K\s*[·/]\s*V",
    ("vit", "Patch"): r"(?:패치|Patch)",
    ("vit", "Token"): r"(?:토큰|Token)",
    ("vit", "Embedding"): r"(?:임베딩|Embedding)",
    ("vit", "Self-Attention"): r"(?:self[- ]attention|Self-Attention)",
    ("tasks", "Classification"): r"(?:분류|Classification)",
    ("tasks", "Detection"): r"(?:탐지|Detection)",
    ("tasks", "Segmentation"): r"(?:분할|Segmentation)",
    ("training", "TP / FP / FN / TN"): r"TP\s*[/·]\s*FP\s*[/·]\s*FN\s*[/·]\s*TN",
    ("training", "Threshold"): r"(?:threshold|Threshold)",
    ("training", "Data leakage"): r"(?:data leakage|데이터 누수|누수)",
    ("cnn", "Residual"): r"(?:residual|Residual|잔차)",
    ("cnn", "Shortcut"): r"(?:shortcut|Shortcut)",
    ("tasks", "Encoder"): r"(?:encoder|Encoder|인코더)",
    ("tasks", "Decoder"): r"(?:decoder|Decoder|디코더)",
    ("tasks", "Skip connection"): r"(?:skip connection|Skip connection)",
    ("tasks", "Concat"): r"(?:concat|Concat)",
    ("patchcore", "Memory bank"): r"(?:memory bank|Memory bank)",
    ("patchcore", "Coreset"): r"(?:coreset|Coreset)",
    ("patchcore", "Nearest neighbor"): r"(?:nearest neighbor|최근접)",
    ("cs231n", "Logit"): r"(?:logit|logits)",
    ("cs231n", "Backpropagation"): r"(?:backpropagation|역전파)",
}

INLINE_SKIP_TAGS = {
    "code", "pre", "script", "style", "svg",
    "header", "nav", "footer", "h1", "h2", "h3",
}


def _term_pattern(slug, short):
    alias = TERM_ALIASES.get((slug, short))
    if alias:
        return re.compile(alias, re.IGNORECASE)
    escaped = re.escape(short).replace(r"\ ", r"\s+")
    if short and short[0].isalnum():
        escaped = r"(?<![\w])" + escaped
    if short and short[-1].isalnum():
        escaped = escaped + r"(?![\w])"
    return re.compile(escaped, re.IGNORECASE)


def _term_html(matched, short, full, meaning):
    if full.casefold() == short.casefold():
        detail = meaning
    else:
        detail = f"{full}, {meaning}"
    return (
        '<span class="term-inline">'
        f'<span class="term-name">{escape(matched)}</span>'
        f'<span class="term-explain"> ({escape(detail)})</span>'
        '</span>'
    )


def annotate_first_terms(html, slug):
    """Explain each configured term once, exactly where it first appears in prose."""

    terms = PAGE_TERMS.get(slug, [])
    if not terms:
        return html

    compiled = [
        (short, full, meaning, _term_pattern(slug, short))
        for short, full, meaning in terms
    ]
    seen = set()
    pieces = re.split(r"(<[^>]+>)", html)
    stack = []

    for idx, piece in enumerate(pieces):
        if not piece:
            continue
        if piece.startswith("<"):
            close = re.match(r"</\s*([a-zA-Z0-9]+)", piece)
            if close:
                tag = close.group(1).lower()
                for pos in range(len(stack) - 1, -1, -1):
                    if stack[pos][0] == tag:
                        del stack[pos:]
                        break
                continue

            open_tag = re.match(r"<\s*([a-zA-Z0-9]+)", piece)
            if open_tag and not piece.rstrip().endswith("/>"):
                tag = open_tag.group(1).lower()
                parent_skip = stack[-1][1] if stack else False
                skip = parent_skip or tag in INLINE_SKIP_TAGS
                if tag == "div" and re.search(
                    r'class=["\'][^"\']*\bequation\b', piece
                ):
                    skip = True
                stack.append((tag, skip))
            continue

        if stack and stack[-1][1]:
            continue

        cursor = 0
        rendered = []
        while cursor < len(piece):
            best = None
            for short, full, meaning, pattern in compiled:
                if short in seen:
                    continue
                match = pattern.search(piece, cursor)
                if match is None:
                    continue
                candidate = (match.start(), match.end(), match, short, full, meaning)
                if best is None or candidate[:2] < best[:2]:
                    best = candidate

            if best is None:
                rendered.append(piece[cursor:])
                break

            start, end, match, short, full, meaning = best
            rendered.append(piece[cursor:start])
            rendered.append(
                _term_html(match.group(0), short, full, meaning)
            )
            seen.add(short)
            cursor = end

        pieces[idx] = "".join(rendered)

    return "".join(pieces)


def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def callout(title, body, warning=False):
    return f'<div class="callout{" warning" if warning else ""}"><span class="label">{title}</span><p>{body}</p></div>'


def equation(body):
    clean = body.strip()
    tex = EQUATION_TEX.get(clean)
    if tex is None:
        plain = "<br>".join(escape(line) for line in clean.splitlines())
        return f'<div class="equation equation-fallback">{plain}</div>'
    return (
        '<div class="equation" aria-label="수학 수식">'
        f'<div class="math-display">\\[{tex.strip()}\\]</div>'
        '</div>'
    )


def svg(body, height=250, caption='학습을 위해 직접 작성한 개념도입니다.'):
    return f'''<figure><div class="diagram"><svg viewBox="0 0 760 {height}" role="img" aria-label="{escape(caption)}"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7891b7"/></marker></defs>{body}</svg></div><figcaption>{caption}</figcaption></figure>'''


def asset_figure(filename, alt, caption):
    return (
        f'<figure class="study-diagram">'
        f'<img src="../assets/diagrams/{escape(filename)}" '
        f'alt="{escape(alt)}" loading="lazy" decoding="async">'
        f'<figcaption>{escape(caption)}</figcaption></figure>'
    )


SECTION_VISUALS = {
    ("pixels", "overview"): ["pixels-human-vs-array.svg"],
    ("pixels", "pixels"): ["pixels-channels.svg"],
    ("pixels", "illumination"): ["pixels-lighting.svg"],
    ("pixels", "normalization"): ["pixels-resize.svg", "pixels-normalization.svg"],

    ("cnn", "overview"): [],
    ("cnn", "convolution"): [],
    ("cnn", "channels"): [],
    ("cnn", "shape"): [],

    ("vit", "problem"): [],
    ("vit", "patches"): [],
    ("vit", "tokens"): [],
    ("vit", "attention"): [],

    ("tasks", "overview"): ["tasks-three-way.svg"],
    ("tasks", "visual"): ["tasks-segmentation.svg"],
    ("tasks", "pipeline"): ["tasks-output-types.svg", "tasks-label-box-mask.svg"],

    ("training", "loop"): ["train-overfit.svg"],
    ("training", "split"): ["train-leakage.svg"],
    ("training", "metrics"): ["train-confusion.svg", "train-prf.svg", "train-threshold.svg", "train-curves.svg"],

    ("cnn", "resnet-problem"): ["resnet-plain-vs.svg"],
    ("cnn", "resnet-block"): ["resnet-function.svg"],
    ("cnn", "resnet-projection"): ["resnet-shortcuts.svg"],
    ("cnn", "resnet-bottleneck"): ["resnet-gradient.svg"],

    ("tasks", "unet-problem"): ["unet-mask-triplet.svg"],
    ("tasks", "unet-architecture"): ["unet-pyramid.svg"],
    ("tasks", "unet-concat"): ["unet-skip-why.svg"],
    ("tasks", "unet-loss"): ["unet-pixel-class.svg"],

    ("patchcore", "problem"): [],
    ("patchcore", "pipeline"): [],
    ("patchcore", "memory"): [],
    ("patchcore", "score"): [],

    ("cs231n", "classification"): [],
    ("cs231n", "linear"): [],
    ("cs231n", "optimization"): [],
    ("cs231n", "nn"): [],
    ("cs231n", "training"): [],
    ("cs231n", "cnn"): [],
    ("cs231n", "architectures"): [],
    ("cs231n", "transfer"): [],
    ("cs231n", "modern"): [],

    ("prml", "ch2"): [],
    ("prml", "ch3"): [],
    ("prml", "ch4"): [],
    ("prml", "ch5"): [],
    ("prml", "ch6"): [],
    ("prml", "ch7"): [],
    ("prml", "ch8"): [],
    ("prml", "ch9"): [],
    ("prml", "ch10"): [],
    ("prml", "ch11"): [],
    ("prml", "ch12"): [],
    ("prml", "ch14"): [],
}


def section_visuals(slug, anchor):
    names = SECTION_VISUALS.get((slug, anchor), [])
    if not names:
        return ""
    figures = []
    for name in names:
        title, subtitle = EXTRA_DIAGRAM_META[name]
        figures.append(
            asset_figure(
                f"extra/{name}",
                title,
                f"{title} — {subtitle}",
            )
        )
    return '<div class="visual-grid">' + ''.join(figures) + '</div>'


PAPER_VISUALS = {
    ("cnn", "overview"): ["cnn-paper-overview.svg"],
    ("cnn", "convolution"): ["cnn-paper-convolution.svg"],
    ("cnn", "channels"): ["cnn-paper-multichannel.svg"],
    ("cnn", "shape"): ["cnn-paper-stride-padding.svg", "cnn-paper-receptive-field.svg"],
    ("cnn", "nonlinear"): ["cnn-paper-pooling.svg"],

    ("vit", "problem"): ["vit-paper-overview.svg"],
    ("vit", "patches"): ["vit-paper-patch-embedding.svg"],
    ("vit", "tokens"): ["vit-paper-cls-position.svg"],
    ("vit", "attention"): [
        "vit-paper-attention.svg",
        "vit-paper-multihead.svg",
        "vit-paper-attention-map.svg",
    ],

    ("patchcore", "problem"): ["patchcore-paper-overview.svg"],
    ("patchcore", "pipeline"): ["patchcore-paper-features.svg"],
    ("patchcore", "memory"): ["patchcore-paper-coreset.svg"],
    ("patchcore", "score"): [
        "patchcore-paper-nearest.svg",
        "patchcore-paper-heatmap.svg",
        "patchcore-paper-score.svg",
    ],
}


def section_paper_figures(slug, anchor):
    names = PAPER_VISUALS.get((slug, anchor), [])
    if not names:
        return ""
    figures = []
    for index, name in enumerate(names, start=1):
        title, subtitle = PAPER_FIGURE_META[name]
        figures.append(
            '<figure class="paper-figure">'
            f'<img src="../assets/diagrams/paper/{escape(name)}" '
            f'alt="{escape(title)}" loading="lazy" decoding="async">'
            f'<figcaption><strong>Figure {index}.</strong> '
            f'{escape(title)} — {escape(subtitle)} ''<span class="figure-note">설명용 재구성 도식이며 실제 실험 측정값이 아닙니다.</span>''</figcaption></figure>'
        )
    return '<div class="paper-visuals">' + ''.join(figures) + '</div>'


def section_reference_figures(slug, anchor):
    names = REFERENCE_VISUALS.get((slug, anchor), [])
    if not names:
        return ""
    figures = []
    for name in names:
        title, subtitle = REFERENCE_FIGURE_META[name]
        figures.append(
            '<figure class="paper-figure reference-figure">'
            f'<img src="../assets/diagrams/reference/{escape(name)}" '
            f'alt="{escape(title)}" loading="lazy" decoding="async">'
            f'<figcaption><strong>{escape(title)}</strong> — '
            f'{escape(subtitle)} ''<span class="figure-note">개념 설명용 합성·재구성 figure입니다.</span>''</figcaption></figure>'
        )
    return '<div class="paper-visuals reference-visuals">' + ''.join(figures) + '</div>'


def box(x, y, width, title, sub='', kind='box'):
    return f'<rect x="{x}" y="{y}" width="{width}" height="66" rx="9" class="{kind}"/><text x="{x+width/2}" y="{y+27}" text-anchor="middle" class="label {"white" if kind == "dark" else ""}">{title}</text><text x="{x+width/2}" y="{y+49}" text-anchor="middle" class="sub {"white" if kind == "dark" else ""}">{sub}</text>'


def edge(path):
    return f'<path d="{path}" class="edge"/>'


def flow(items, caption):
    width = (720 - 28 * (len(items) - 1)) / len(items)
    body = ''
    for i, (title, sub) in enumerate(items):
        x = 20 + i * (width + 28)
        body += box(x, 35, width, title, sub, 'dark' if i == len(items) - 1 else 'box')
        if i < len(items) - 1:
            body += edge(f'M {x+width} 68 H {x+width+25}')
    return svg(body, 135, caption)


def section(anchor, title, body):
    return (anchor, title, body)


def note(slug, title, subtitle, group, label, minutes, sections, sources):
    NOTES.append(dict(slug=slug, title=title, subtitle=subtitle, group=group,
                      label=label, minutes=minutes, sections=sections, sources=sources))


note('pixels', '이미지는 어떻게 숫자가 될까?', '픽셀, RGB, 텐서, 정규화. 모델에 들어가는 입력을 숫자의 관점에서 이해합니다.', '이미지·CNN', '01 · IMAGE & TENSOR', 15, [
section('overview', '사람의 장면을 모델의 배열로 바꾸기', '''<p>컴퓨터 비전 모델이 받는 것은 “사진”이라는 개념보다 <strong>정해진 순서로 배치된 숫자 배열</strong>에 가깝습니다. 사진을 읽으면 높이·너비·색상 채널의 배열이 되고, 여러 장을 묶으면 배치 차원이 추가됩니다. 모델은 이 수치에서 학습한 패턴을 이용해 클래스, 좌표, 마스크 등을 예측합니다.</p>''' + asset_figure('image-to-tensor.svg', '원본 이미지가 RGB 채널을 거쳐 NCHW 텐서로 변환되는 과정', '원본 이미지 → RGB 채널 값 → 배치 텐서의 관계를 한눈에 보는 개념도입니다.') + flow([('디코딩', '[H, W, 3]'), ('전처리', 'resize · normalize'), ('배치 구성', '[B, 3, H, W]'), ('모델', '특징 · 예측')], '이미지 파일에서 모델 입력까지. RGB와 NCHW를 사용하는 경우의 예시입니다.') + '''<p>예를 들어 RGB 이미지 224 × 224 한 장은 <strong>150,528개</strong>의 채널 값을 가집니다. 32장을 묶으면 입력은 <code>[32, 3, 224, 224]</code>입니다. 배열의 숫자 개수와 모델이 학습하는 파라미터 개수는 서로 다른 개념입니다.</p>'''),
section('pixels', '한 픽셀에는 무엇이 들어 있을까?', table(['표현', '자료 구조 예시', '의미'], [('Grayscale', '<code>[H, W]</code> · 8-bit 값 0~255', '0은 검정, 255는 흰색. 밝기 하나로 표현합니다.'), ('RGB', '<code>[H, W, 3]</code> · [220, 60, 30]', 'R, G, B 채널의 세기. 이 예시는 붉은색 계열입니다.'), ('배치 텐서', '<code>[32, 3, 224, 224]</code>', 'PyTorch CNN에서 흔한 NCHW 순서: 배치, 채널, 높이, 너비.')]) + '''<p>OpenCV로 읽은 컬러 이미지의 기본 순서는 BGR입니다. RGB로 학습한 모델에 BGR을 그대로 넣으면 빨강과 파랑의 의미가 바뀝니다. 또한 <code>reshape</code>로 채널 순서를 바꾸면 안 됩니다. 차원의 위치를 바꾸는 <code>transpose</code>나 <code>permute</code>가 필요합니다.</p>''' + callout('형태와 의미를 함께 확인', '1920 × 1080 이미지를 보통 너비 × 높이로 말하지만 배열은 흔히 [1080, 1920, 3]입니다. “shape가 맞다”는 것만으로 RGB 순서와 값 범위가 맞는지는 알 수 없습니다.')),
section('illumination', '직접 확인하기: 모양은 같아도 숫자는 달라진다', '''<p>아래 8 × 8 밝기 패턴은 학습용 합성 입력입니다. 왼쪽 그림과 오른쪽 행렬은 <strong>동일한 64개 픽셀</strong>을 보여 줍니다. 밝기 배율을 바꾸면 경계와 내부의 서로 다른 값들이 함께 변합니다.</p><div class="lab"><div class="lab-heading"><h3>밝기와 픽셀 값</h3><span class="lab-badge">INTERACTIVE</span></div><div class="controls"><label for="brightness">밝기 배율 <output id="brightness-value">1.00</output></label><input id="brightness" type="range" min="30" max="180" value="100" step="5"></div><div class="lab-display"><canvas id="pixel-canvas" width="256" height="256" aria-label="밝기 변화에 따른 8 × 8 패턴"></canvas><div id="pixel-matrix" class="matrix" style="grid-template-columns:repeat(8,1fr)" aria-label="동일한 패턴의 픽셀 값"></div></div><p class="lab-note">표시값 = clip(round(원래 값 × 배율), 0, 255). 실제 카메라의 노출·감마·노이즈를 모두 재현하는 물리 모델은 아닙니다.</p></div><p>밝은 값이 255를 넘으면 잘려서 포화됩니다. 예를 들어 170 × 1.8 = 306은 255가 됩니다. 서로 다른 원래 값들이 같은 255가 되므로 정보가 사라질 수 있습니다. 조명 변화에 강한 모델을 만들려면 이런 입력 분포 변화와 촬영 조건을 함께 생각해야 합니다.</p>'''),
section('normalization', '스케일 변환과 정규화는 구분하기', '''<p><code>uint8 → float32 → 255로 나누기</code>는 0~255를 0~1로 바꾸는 스케일 변환입니다. 이후 채널별 평균과 표준편차를 이용하는 표준화가 추가될 수 있습니다. 전처리는 사용한 사전학습 가중치와 학습 조건을 따라야 합니다.</p>''' + equation('x_scaled = x_uint8 / 255\nx_normalized = (x_scaled − mean) / std') + '''<p>가상의 한 채널에서 픽셀 128, 평균 0.5, 표준편차 0.25라면 <code>(128/255 − 0.5)/0.25 ≈ 0.00784</code>입니다. 정규화 결과는 음수일 수 있습니다. 평균·표준편차가 [0.5, 0.25]라는 뜻이 아니라 각각 하나의 채널에 대해 정한 예시입니다.</p>''' + callout('기억할 핵심', '입력 크기·채널 순서·dtype·값 범위·정규화는 하나의 계약입니다. 학습과 추론이 같은 계약을 사용해야 합니다.')),
section('check', '스스로 설명해 보기', '''<details><summary>224 × 224 RGB 이미지의 채널 값은 왜 50,176개가 아닐까?</summary><p>224 × 224 = 50,176은 공간 위치의 수입니다. 각 위치에 3개 채널이 있으므로 150,528개 값입니다.</p></details><details><summary>배치 크기를 16에서 32로 바꾸면 모델 파라미터도 두 배가 될까?</summary><p>파라미터 수는 그대로입니다. 한 번에 처리하는 입력과 중간 활성값의 양이 늘기 때문에 보통 메모리 사용량이 증가합니다.</p></details>''')
], [('PyTorch · Tensor basics', 'https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html', '텐서의 형태와 차원 조작을 확인할 수 있습니다.'), ('Torchvision · Models and pre-trained weights', 'https://docs.pytorch.org/vision/stable/models.html', '가중치별 입력 전처리가 다를 수 있습니다.'), ('OpenCV · Color conversions', 'https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html', 'BGR/RGB 변환의 공식 API입니다.')])

note('cnn', 'CNN: 합성곱에서 ResNet까지', '합성곱·채널·수용영역을 이해한 뒤, 대표 CNN 아키텍처인 ResNet의 residual learning까지 연결합니다.', '이미지·CNN', '02 · CNN & RESNET', 22, [
section('overview', '왜 작은 커널을 반복해서 사용할까?', '''<p>CNN은 가까운 픽셀 사이의 패턴을 작은 커널로 계산합니다. 같은 커널을 여러 위치에 적용하는 <strong>가중치 공유</strong> 덕분에 이미지의 모든 위치마다 별도 가중치를 둘 필요가 없습니다. 학습은 어떤 커널 값이 목적에 유용한지를 데이터로 조정하는 과정입니다.</p>''' + flow([('입력', '3 × 224 × 224'), ('Conv + ReLU', '32 × 224 × 224'), ('Downsample', '32 × 112 × 112'), ('분류 Head', 'K개 logits')], '구조를 설명하기 위한 간단한 CNN 예시. 특정 논문의 전체 모델은 아닙니다.') + '''<p>Feature map은 “물체를 그린 지도”로 항상 해석할 수 있는 결과가 아닙니다. 특정 커널과 비선형 연산에 반응한 활성값의 공간 배열입니다. 초기 층에서 경계·방향 같은 반응을 볼 수 있지만, 모든 채널을 한 단어의 의미에 대응시킬 수는 없습니다.</p>'''),
section('convolution', '3 × 3 합성곱을 손으로 계산하기', '''<p>입력의 3 × 3 영역과 커널의 같은 위치를 각각 곱한 뒤, 9개 값을 더하고 bias를 더합니다. 딥러닝 라이브러리에서 흔히 합성곱이라고 부르는 연산은 커널을 뒤집지 않는 <em>cross-correlation</em>입니다.</p>''' + asset_figure('convolution-step.svg', '5×5 입력의 3×3 영역과 3×3 커널을 곱하고 더해 출력 한 값을 계산하는 과정', '3×3 합성곱 한 위치의 multiply-and-sum 계산을 외부 SVG로 정리했습니다.') + equation('출력[y, x] = Σ 입력[y+i, x+j] × 커널[i, j] + bias\n예시 커널 = [[−1, 0, 1], [−1, 0, 1], [−1, 0, 1]]') + '''<div class="lab"><div class="lab-heading"><h3>커널이 이동하는 위치</h3><span class="lab-badge">INTERACTIVE</span></div><div class="controls"><label for="conv-position">출력 위치 선택</label><input id="conv-position" type="range" min="0" max="8" value="0" step="1"></div><div class="lab-display"><div><p class="small">입력 5 × 5 · 파란 영역이 현재 계산 범위</p><div id="conv-input" class="matrix" style="grid-template-columns:repeat(5,1fr)"></div></div><div><p class="small">출력 3 × 3 · stride 1, padding 0, bias 0</p><div id="conv-output" class="matrix" style="grid-template-columns:repeat(3,1fr)"></div></div></div><div id="conv-value" class="lab-output" aria-live="polite"></div><p class="lab-note">수직 경계에 반응하는 고정 커널입니다. 실제 CNN에서는 대부분의 커널 값을 학습합니다.</p></div><p>첫 위치에서 각 행은 <code>[0, 0, 1] · [−1, 0, 1] = 1</code>이고, 세 행을 더하면 3입니다. 오른쪽 끝의 일정한 <code>[1, 1, 1]</code>은 −1 + 0 + 1 = 0이므로 경계가 없는 영역은 0이 됩니다.</p>'''),
section('channels', '채널은 어떻게 섞일까?', '''<p>RGB 입력에 출력 채널 32개를 만드는 3 × 3 Conv를 사용하면 커널의 전체 shape는 <code>[32, 3, 3, 3]</code>입니다. 출력 채널 하나는 R·G·B 각각에 대한 계산을 합한 결과입니다. 일반적인 Conv에서 입력 채널마다 완전히 독립적인 최종 결과를 만드는 것은 아닙니다.</p>''' + table(['항목', '수치 예시', '설명'], [('입력', '[B, 3, 224, 224]', '배치 차원은 공간 연산과 별도'), ('가중치', '[32, 3, 3, 3]', '출력 채널 × 입력 채널 × 커널 높이 × 너비'), ('파라미터', '32 × 3 × 3 × 3 + 32 = 896', 'groups=1, bias=True일 때'), ('출력', '[B, 32, 224, 224]', 'stride=1, padding=1, dilation=1')]) + callout('1 × 1 Conv도 학습할 내용이 있다', '1 × 1 커널은 인접 공간을 직접 섞지는 않지만 채널을 섞습니다. 입력 64채널을 출력 128채널로 바꾸면 위치마다 64차원 벡터를 128차원으로 변환합니다.')),
section('shape', 'Stride · Padding · Receptive field', equation('H_out = floor((H + 2P − D(K−1) − 1) / S + 1)\nW_out도 같은 방식으로 계산\nH=224, K=3, P=1, D=1, S=2 → H_out=112') + table(['용어', '하는 일', '수치 예시'], [('Stride', '커널이 이동하는 간격', '2이면 출력 공간 크기가 보통 약 절반'), ('Padding', '입력 주변을 확장', '3 × 3, stride 1에서 padding 1이면 크기 유지'), ('Dilation', '커널 샘플 간격 확장', '3 × 3, dilation 2의 유효 범위는 5 × 5'), ('Receptive field', '한 출력이 영향을 받는 입력의 범위', 'stride 1인 3 × 3 두 층은 이론상 5 × 5')]) + '''<p>수용영역은 층이 깊어지며 커집니다. 하지만 이론적으로 연결된 모든 픽셀이 동일한 영향력을 갖는 것은 아닙니다. 그리고 다운샘플링은 계산량을 줄이는 대신 작은 결함의 위치 정보가 약해질 수 있는 선택입니다.</p>'''),
section('nonlinear', '왜 비선형 함수와 학습이 필요할까?', '''<p>ReLU는 <code>max(0, x)</code>를 계산합니다. 예를 들어 [−2, 0.5, 3]은 [0, 0.5, 3]이 됩니다. 비선형성이 전혀 없다면 여러 선형 변환을 쌓아도 하나의 선형 변환으로 합칠 수 있어 표현력에 제약이 생깁니다.</p><p>분류 학습에서는 특징을 이용해 클래스별 logit을 만들고, 정답과 비교한 loss를 역전파합니다. 기울기는 각 가중치를 바꿨을 때 loss가 어떻게 변할지를 나타내며, optimizer가 이 정보를 사용해 파라미터를 갱신합니다. “경계를 찾는 필터”를 사람이 모두 지정하는 것이 아닙니다.</p>''' + callout('한 문장으로 정리', 'CNN은 공유 커널로 지역 패턴을 계산하고, 채널 변환과 비선형 함수를 반복하면서 목적에 맞는 특징을 학습합니다.')),
section('architectures', 'CNN 아키텍처는 무엇이 바뀌어 왔을까?', '''<p>LeNet, AlexNet, VGG, ResNet은 모두 CNN 계열이지만 깊이만 늘어난 것이 아닙니다. 특히 VGG는 작은 3 × 3 convolution을 반복해서 쌓는 설계를 체계적으로 사용했고, ResNet은 더 깊은 CNN을 최적화하기 위해 <strong>residual connection</strong>을 도입했습니다.</p>''' + table(['모델/아이디어', '핵심 설계', '이 주제에서 볼 포인트'], [('VGG', '3 × 3 Conv 반복', '작은 local kernel을 깊게 쌓아 receptive field와 비선형성을 늘림'), ('ResNet', 'F(x)+x', '깊은 CNN의 optimization degradation을 완화'), ('Bottleneck ResNet', '1×1 → 3×3 → 1×1', '비싼 3×3 연산 전후의 채널 수를 조절')]) + callout('논문을 별도 섬으로 보지 않기', 'ResNet은 CNN과 다른 종류의 모델이 아니라, convolutional feature extractor를 더 깊게 학습하기 위한 CNN architecture입니다.')),
section('resnet_problem', 'ResNet 논문: 깊게 쌓았는데 training error가 커지는 문제', '''<p>He et al.의 ResNet 논문은 단순히 “gradient vanishing을 해결했다”는 한 문장으로 요약하면 부정확합니다. 논문이 강조한 현상은 충분히 깊은 plain network에서 <strong>training error 자체가 더 나빠지는 degradation problem</strong>입니다. 이는 training error는 낮지만 validation/test 성능만 나빠지는 overfitting과 구분해야 합니다.</p><p>Residual block은 원하는 mapping H(x)를 직접 근사하는 대신 <code>F(x)=H(x)-x</code>를 학습하도록 재표현하고, 출력에서 입력을 더해 <code>H(x)=F(x)+x</code>를 만듭니다.</p>'''),
section('residual_block', 'Residual block: F(x)와 identity shortcut', asset_figure('resnet-skip.svg', 'CNN residual block에서 입력 x가 convolution branch를 우회해 합산되는 구조', 'ResNet을 CNN의 architecture 확장으로 이해하기 위한 residual block 도식입니다.') + equation('합산 전 목표: H(x) = x + F(x)\n단순한 합산 경로의 미분: ∂H/∂x = I + ∂F/∂x') + '''<p>예를 들어 x=[2, −1], F(x)=[0.3, 0.2]라면 합산 전 activation은 [2.3, −0.8]입니다. 원 ResNet의 post-activation basic block처럼 합산 뒤 ReLU를 적용하는 경우 [2.3, 0]이 됩니다. Shortcut이 있다고 해서 출력이 항상 입력과 같다는 뜻은 아닙니다.</p><p>또한 <code>∂H/∂x</code>에 identity term이 생긴다는 사실은 gradient가 지나갈 직접 경로를 설명하지만, 이것만으로 모든 깊은 모델의 optimization이 자동으로 해결된다고 해석해서는 안 됩니다.</p>'''),
section('residual_shape', 'Shape가 다르면 projection shortcut이 필요하다', '''<p>원소별 덧셈을 하려면 두 branch의 shape가 같아야 합니다. 예를 들어 main branch가 <code>[B,64,56,56] → [B,128,28,28]</code>로 바뀌면 identity를 그대로 더할 수 없습니다. 이런 경우 projection shortcut에서 1 × 1 convolution과 stride를 사용해 shape를 맞출 수 있습니다.</p>''' + table(['경로', '입력', '변환', '출력'], [('Main branch', '[B,64,56,56]', 'stride-2 residual block', '[B,128,28,28]'), ('Shortcut', '[B,64,56,56]', '1×1 Conv, stride 2', '[B,128,28,28]'), ('Add', '동일 shape 두 텐서', 'element-wise sum', '[B,128,28,28]')]) + callout('U-Net skip과 구분', 'ResNet의 대표 shortcut은 element-wise add이고, 원 U-Net의 encoder–decoder skip은 channel-wise concatenate입니다. 둘 다 “skip connection”이지만 자료 구조가 다릅니다.')),
section('resnet_bottleneck', 'Bottleneck block: 1×1 Conv의 또 다른 역할', '''<p>ResNet-18/34는 basic block을, ResNet-50/101/152는 bottleneck block을 사용합니다. Bottleneck에서는 1 × 1 convolution으로 채널을 줄인 뒤 3 × 3 공간 연산을 하고 다시 1 × 1로 채널을 확장합니다.</p>''' + flow([('1×1 Conv', '256 → 64'), ('3×3 Conv', '64 → 64'), ('1×1 Conv', '64 → 256')], '공간 크기가 유지되는 bottleneck의 채널 흐름 예시입니다.') + '''<p>bias와 normalization parameter를 제외하면 이 예시의 convolution weight는 256×64 + 64×64×9 + 64×256 = 69,632개입니다. 같은 256 input/output channel의 3×3 convolution 하나는 589,824개입니다. 이 수치는 block 내부 연산량 감각을 위한 예시이며 전체 모델 성능을 직접 비교하는 숫자는 아닙니다.</p>'''),
section('resnet_scope', 'ResNet 논문에서 실제로 확인한 범위', '''<p>원 논문은 ImageNet에서 residual network를 최대 152 layers까지 실험하고 plain counterpart와 비교하며, residual formulation이 매우 깊은 network의 optimization을 쉽게 만든다는 실험 근거를 제시합니다. 따라서 “ResNet은 무조건 깊을수록 좋다”가 아니라, <strong>깊이를 늘릴 때 생기던 optimization degradation을 residual learning으로 다룬다</strong>가 핵심입니다.</p><p>새로운 제조 데이터에 적용할 때는 입력 해상도, defect 크기, 사전학습, 데이터 수, latency를 별도로 평가해야 합니다. 논문의 ImageNet 결과를 다른 데이터셋의 성능 보장으로 옮겨 적으면 안 됩니다.</p>''')

], [('PyTorch · Conv2d', 'https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html', '연산 정의, 가중치 shape, 출력 크기 공식의 기준입니다.'), ('PyTorch · ReLU', 'https://docs.pytorch.org/docs/stable/generated/torch.nn.ReLU.html', 'ReLU의 정의를 확인할 수 있습니다.'), ('He et al. · Deep Residual Learning for Image Recognition', 'https://arxiv.org/abs/1512.03385', 'CVPR 2016. degradation problem, residual block, bottleneck과 ImageNet 실험의 원문입니다.'), ('저자 공식 구현 · KaimingHe/deep-residual-networks', 'https://github.com/KaimingHe/deep-residual-networks', '원 연구의 모델 구현 자료입니다.'), ('Torchvision · ResNet', 'https://docs.pytorch.org/vision/stable/models/resnet.html', '현대 PyTorch 구현과 사전학습 가중치의 공식 문서입니다.')])

note('vit', 'Transformer Vision: Attention에서 ViT까지', '패치·토큰·Q/K/V·self-attention을 먼저 이해하고, Vision Transformer 논문을 대표 사례로 연결합니다.', 'Transformer·Attention', '03 · TRANSFORMER & VIT', 30, [
section('problem', '논문이 던진 질문', '''<p>Transformer를 이미지 분류의 주된 구조로 사용할 수 있을까요? ViT는 이미지를 일정한 크기의 패치로 나누고, 각 패치를 토큰 벡터로 바꿔 Transformer encoder에 넣습니다. 논문의 핵심은 <strong>이미지의 2차원 격자를 토큰 시퀀스로 변환하는 방법</strong>과 대규모 사전학습의 효과입니다.</p><p>원 논문은 대규모 데이터로 사전학습했을 때의 강력한 결과를 보였습니다. 이것을 “작은 데이터에서도 ViT가 항상 CNN보다 좋다”로 일반화하면 안 됩니다. 사전학습 데이터, 입력 해상도, 증강, 학습 설정과 계산 예산을 함께 비교해야 합니다.</p>''' + flow([('이미지', '224 × 224 × 3'), ('패치 임베딩', '196 × 768'), ('Encoder', '197 tokens'), ('분류 Head', 'K개 logits')], 'ViT-B/16의 224 × 224 입력 예시. Encoder 입력의 197은 패치 196개와 CLS 토큰 1개입니다.')),
section('patches', 'Patch → Flatten → Linear projection', '''<p>패치 크기를 16 × 16으로 정하면 224/16 = 14이므로 총 14 × 14 = <strong>196개 패치</strong>가 생깁니다. 각 RGB 패치를 펼치면 16 × 16 × 3 = 768개의 숫자입니다. 이 벡터에 학습 가능한 선형 변환을 적용해 임베딩 차원 D로 바꿉니다.</p>''' + asset_figure('vit-patch-attention.svg', '이미지를 패치로 나누고 토큰 시퀀스로 만든 뒤 self-attention을 적용하는 Vision Transformer 흐름', '224×224 이미지를 patch sequence로 바꾸고 attention에 전달하는 흐름입니다.') + equation('N = (H/P) × (W/P)\npatch_flat: [B, N, P²C]\nembedding = patch_flat × E + bias\nE: [P²C, D] → output: [B, N, D]') + '''<p>ViT-B/16에서는 패치 벡터 길이와 D가 우연히 모두 768입니다. 따라서 변환이 불필요한 것이 아닙니다. 학습 가능한 768 × 768 행렬은 픽셀 공간을 모델이 쓸 특징 공간으로 바꿉니다. 패치 크기와 D는 서로 독립적으로 설계할 수 있습니다.</p><div class="lab"><div class="lab-heading"><h3>패치 크기와 토큰 수</h3><span class="lab-badge">INTERACTIVE</span></div><div class="controls"><label for="patch-size">패치 한 변</label><select id="patch-size"><option value="8">8 px</option><option value="16" selected>16 px</option><option value="32">32 px</option></select></div><div class="lab-display"><canvas id="patch-canvas" width="224" height="224" aria-label="224 × 224 입력에 적용한 패치 격자"></canvas><div id="patch-result" class="lab-output" aria-live="polite"></div></div><p class="lab-note">D=768로 고정한 크기 계산입니다. 선택값마다 사전학습 모델을 실행하는 데모는 아닙니다.</p></div>'''),
section('tokens', 'CLS와 위치 임베딩은 왜 더할까?', '''<p><strong>CLS 토큰</strong>은 이미지 전체를 분류하는 데 사용할 학습 가능한 추가 토큰입니다. 입력 단계에서는 이미지의 내용을 이미 알고 있는 벡터가 아닙니다. 여러 encoder 층에서 패치들과 정보를 주고받은 뒤 최종 표현을 분류 head에 전달합니다.</p><p><strong>Position embedding</strong>은 패치 위치에 대한 학습 가능한 정보를 더합니다. 기본 self-attention만으로는 토큰의 원래 격자 위치를 직접 구분하지 못하기 때문입니다. 원 ViT는 1차원 학습 가능한 위치 임베딩을 사용합니다.</p>''' + equation('z₀ = [CLS; patch₁E; …; patch₁₉₆E] + E_position\nshape: [B, 197, 768]') + callout('패치 번호와 픽셀 좌표는 다르다', '2차원 패치를 일정한 순서로 펼쳐도 원래 행·열 배치는 정해져 있습니다. 위치 임베딩은 그 순서에 대응하는 정보를 제공합니다. 입력 해상도를 바꿔 토큰 수가 달라지면 사전학습 위치 임베딩을 보간하는 등의 처리가 필요할 수 있습니다.')),
section('attention', 'Q · K · V: 무엇을 비교하고 무엇을 가져올까?', '''<p>한 토큰의 특징 벡터에서 서로 다른 선형 변환으로 Query, Key, Value를 만듭니다. Q는 비교를 요청하는 표현, K는 비교 대상의 표현, V는 실제로 섞어 가져올 정보라고 생각할 수 있습니다. 이것은 이해를 위한 비유이며 세 값 모두 학습된 수치 벡터입니다.</p>''' + equation('Q = XW_Q,  K = XW_K,  V = XW_V\nAttention(Q,K,V) = softmax(QKᵀ / √d_k) V') + table(['단계', '한 head의 shape 예시', '해석'], [('입력 X', '[B, 197, 768]', '정규화된 토큰 특징'), ('Q, K, V', '각각 [B, 197, 64]', '12 heads, D=768이면 head당 64차원'), ('QKᵀ', '[B, 197, 197]', '각 query와 모든 key 사이 점수'), ('Softmax', '각 행의 합 = 1', 'query 하나가 다른 토큰을 섞는 가중치'), ('가중합 AV', '[B, 197, 64]', 'Value를 관계에 따라 혼합')]) + '''<p>계산 감각을 잡기 위해 한 query의 <em>스케일링된 점수</em>가 [2, 1, 0]이라고 가정하면 softmax는 약 [0.665, 0.245, 0.090]입니다. Value가 1차원 [10, 20, 30]이면 결과는 약 14.25입니다. 실제 모델에서는 수십 차원의 벡터를 head마다 같은 방식으로 섞습니다.</p>''' + flow([('관계 점수', '[2, 1, 0]'), ('Softmax', '[.665, .245, .090]'), ('Value 가중합', '10, 20, 30 → 14.25')], '실제 학습된 attention 결과가 아닌 3개 토큰의 계산 예시입니다.') + '''<p>Multi-head는 여러 표현 공간에서 관계를 계산한 뒤 결과를 이어 붙이고 출력 projection을 적용합니다. 각 head가 반드시 “색상 담당”, “모양 담당”으로 고정되는 것은 아닙니다. Attention map 역시 모델 판단의 완전한 인과 설명이라고 볼 수 없습니다.</p>'''),
section('encoder', 'Encoder 블록 내부의 두 번의 업데이트', '''<p>원 ViT의 encoder는 LayerNorm을 먼저 적용하는 구조입니다. Attention은 토큰 사이 정보를 교환하고, MLP는 각 토큰의 채널 특징을 변환합니다. 각 단계에는 입력을 더하는 residual connection이 있습니다.</p>''' + equation('z′ = z + MSA(LN(z))\nz_next = z′ + MLP(LN(z′))') + svg(box(25,90,110,'입력 z','197 × 768') + box(195,90,130,'LN → MSA','토큰 간 혼합') + box(382,90,130,'LN → MLP','채널 변환') + box(587,90,140,'다음 블록','197 × 768','dark') + edge('M 135 123 H 193') + edge('M 325 123 H 380') + edge('M 512 123 H 585') + edge('M 153 123 V 43 H 351 V 119') + edge('M 353 123 V 209 H 548 V 127') + '<text x="244" y="32" class="sub">residual add</text><text x="420" y="233" class="sub">residual add</text><circle cx="353" cy="123" r="11" fill="white" stroke="#7891b7"/><text x="353" y="128" text-anchor="middle" class="label">+</text><circle cx="548" cy="123" r="11" fill="white" stroke="#7891b7"/><text x="548" y="128" text-anchor="middle" class="label">+</text>',260,'Residual 경로를 포함한 ViT encoder. MLP는 보통 D에서 더 넓은 차원으로 확장한 뒤 D로 돌아옵니다.') + '''<p>ViT-B는 12개 encoder 블록, 임베딩 768차원, 12개 attention head, MLP 내부 3072차원을 사용합니다. MLP의 GELU와 dropout 같은 세부 연산은 위 도식에서 생략했습니다. 최종 LayerNorm 이후 CLS 표현이 분류 head로 전달됩니다.</p>'''),
section('limits', 'CNN과 비교할 때 살펴볼 점', table(['관점', 'CNN', '기본 ViT'], [('공간 처리', '지역 커널을 반복 적용', '패치 토큰 사이 전역 attention'), ('구조적 가정', '지역성·가중치 공유가 강하게 내장', '상대적으로 적은 이미지 특화 가정'), ('입력 해상도', '활성값·연산량 증가', '토큰 수 증가와 attention 비용 고려'), ('작은 물체', 'stride와 feature 해상도에 민감', '패치 크기와 입력 해상도에 민감')]) + '''<p>224에서 448로 가로·세로를 두 배로 늘리고 P=16을 유지하면 패치는 196에서 784로 4배가 됩니다. CLS 포함 score 행렬의 원소 수는 197²=38,809에서 785²=616,225로 약 15.88배입니다. 이것은 attention score의 크기 비교이며 전체 실행시간이나 총 GPU 메모리가 반드시 같은 비율로 늘어난다는 뜻은 아닙니다.</p>''' + callout('이 논문의 핵심', '이미지를 패치 임베딩 시퀀스로 만들면 Transformer로 분류할 수 있습니다. 좋은 성능을 만드는 조건에는 구조뿐 아니라 데이터 규모와 사전학습이 포함됩니다.'))
], [('Dosovitskiy et al. · An Image is Worth 16×16 Words', 'https://arxiv.org/abs/2010.11929', 'ICLR 2021. 패치 임베딩·CLS·encoder 구조와 모델 크기 표의 원문입니다.'), ('Google Research · vision_transformer', 'https://github.com/google-research/vision_transformer', '저자 측 공식 구현과 모델 설정입니다.'), ('Vaswani et al. · Attention Is All You Need', 'https://arxiv.org/abs/1706.03762', 'Scaled dot-product attention과 multi-head attention의 기반 논문입니다.')])

note('tasks', 'Vision Tasks와 Segmentation: U-Net까지', '분류·탐지·분할의 출력 형식을 구분하고, segmentation의 대표 구조인 U-Net을 같은 주제 안에서 연결합니다.', 'Vision Tasks·Segmentation', '04 · VISION TASKS & U-NET', 15, [
section('overview', '모델을 고르기 전에 출력부터 정하기', '''<p>“이 이미지에 불량이 있는가”, “불량이 어디 있는가”, “불량의 경계가 어디인가”는 서로 다른 질문입니다. 먼저 필요한 출력의 형태를 정하면 라벨링 범위와 평가 지표, 후처리를 더 명확히 설계할 수 있습니다.</p>''' + table(['문제', '출력 예시', '필요한 정답'], [('분류 Classification', '[정상 .10, 결함 .90]', '이미지 전체의 클래스'), ('탐지 Object detection', '[x₁, y₁, x₂, y₂, score, class]', '물체별 박스와 클래스'), ('의미 분할 Semantic segmentation', '픽셀별 클래스 [H, W]', '모든 픽셀의 클래스'), ('개체 분할 Instance segmentation', '물체별 마스크 [N, H, W]', '각 물체의 클래스·경계·개체 구분')]) + '''<p>예를 들어 3개의 동일 종류 물체가 있을 때 semantic segmentation은 모두 같은 클래스 값으로 표시할 수 있습니다. Instance segmentation은 세 물체를 서로 다른 개체로 구분합니다. 물체 개수를 세거나 개별 경계를 추적하려는 경우 이 차이가 중요합니다.</p>'''),
section('visual', '같은 장면에서 결과를 비교하기', svg('''<rect x="20" y="48" width="216" height="174" rx="10" fill="#f1f5fb"/><rect x="272" y="48" width="216" height="174" rx="10" fill="#f1f5fb"/><rect x="524" y="48" width="216" height="174" rx="10" fill="#f1f5fb"/><text x="128" y="25" class="label" text-anchor="middle">분류</text><text x="380" y="25" class="label" text-anchor="middle">탐지</text><text x="632" y="25" class="label" text-anchor="middle">개체 분할</text>''' + ''.join(f'<circle cx="{x+70}" cy="114" r="29" fill="#a5b6d0"/><rect x="{x+115}" y="144" width="60" height="36" rx="8" fill="#a5b6d0"/>' for x in [20,272,524]) + '''<text x="128" y="207" class="sub" text-anchor="middle">부품 있음 · score 0.96</text><rect x="308" y="77" width="68" height="74" rx="3" fill="none" stroke="#2454d8" stroke-width="3"/><rect x="382" y="138" width="72" height="48" rx="3" fill="none" stroke="#2454d8" stroke-width="3"/><circle cx="594" cy="114" r="29" fill="#2454d8" fill-opacity=".6" stroke="#2454d8" stroke-width="2"/><rect x="639" y="144" width="60" height="36" rx="8" fill="#0a9e89" fill-opacity=".65" stroke="#08796f" stroke-width="2"/>''',245,'동일한 두 도형을 대상으로 출력 표현만 비교한 개념도입니다. 실제 모델 예측이나 실물 사진은 아닙니다.') + '''<p>분류에는 위치가 직접 나오지 않습니다. 탐지 박스는 물체를 둘러싸지만 경계 모양을 그대로 표현하지는 않습니다. 마스크는 픽셀 단위 영역을 제공하지만 촬영 해상도·라벨 오차·모델 출력 해상도의 제약을 받습니다.</p>'''),
section('pipeline', 'Backbone · Neck · Head', '''<p><strong>Backbone</strong>은 특징을 추출하는 부분입니다. <strong>Neck</strong>은 여러 해상도의 특징을 결합하는 부분으로, 항상 별도 모듈로 존재하는 것은 아닙니다. <strong>Head</strong>는 목적에 맞는 최종 출력을 만듭니다. 같은 backbone도 head와 학습 목표에 따라 다른 문제에 사용할 수 있습니다.</p>''' + flow([('입력', '640 × 640'), ('Backbone', '다단계 특징'), ('Neck', '다중 해상도 결합'), ('Head', '박스 · 클래스 · 마스크')], '일반적인 탐지·분할 구성의 개념도. 모든 모델이 이 분해를 정확히 따르는 것은 아닙니다.') + '''<p>학습 중 출력은 바로 최종 박스 목록이 아닐 수 있습니다. 모델별 출력 해석, 좌표 변환, confidence 필터, 필요시 NMS 등의 후처리를 거쳐 사용 가능한 결과가 됩니다. NMS가 필요한지와 score의 정의는 모델 버전과 구현마다 확인해야 합니다.</p>'''),
section('iou', '겹친 정도를 수치로 표현하기', equation('IoU = |예측 ∩ 정답| / |예측 ∪ 정답|\nDice = 2|예측 ∩ 정답| / (|예측| + |정답|)') + '''<p>예측 영역 120픽셀, 정답 영역 100픽셀, 교집합 80픽셀이라면 합집합은 140픽셀입니다. IoU는 80/140≈0.571, Dice는 160/220≈0.727입니다. 같은 두 이진 마스크를 비교할 때 <code>Dice = 2IoU/(1+IoU)</code>의 관계가 있습니다.</p>''' + svg('''<rect x="118" y="30" width="230" height="140" rx="4" fill="#a5bef8" fill-opacity=".65" stroke="#2454d8" stroke-width="2"/><rect x="248" y="73" width="230" height="140" rx="4" fill="#6dcebb" fill-opacity=".6" stroke="#08796f" stroke-width="2"/><text x="158" y="63" class="label">예측</text><text x="386" y="191" class="label">정답</text><text x="298" y="117" class="label" text-anchor="middle">교집합</text><text x="535" y="100" class="label">겹친 영역</text><path d="M 520 115 H 700" stroke="#7891b7" stroke-width="2"/><text x="535" y="142" class="label">전체 합집합</text>''',240,'IoU의 기하학적 의미. 위 설명의 픽셀 수를 면적 비율로 재현한 그림은 아닙니다.') + callout('목적에 맞는 평가 영역', '경계 위치가 중요하면 전체 IoU 하나만으로 충분하지 않을 수 있습니다. 작은 관심영역과 경계 오차를 함께 확인하되, 평가 ROI와 기준은 결과를 보기 전에 정해야 합니다.')),
section('segmentation_context', 'Segmentation에서는 왜 encoder–decoder가 필요한가?', '''<p>분류는 이미지 전체를 하나의 vector로 요약해도 되지만 segmentation은 픽셀 위치를 보존하며 class를 예측해야 합니다. Downsampling은 넓은 context를 얻는 데 유리하지만 세밀한 위치 정보가 줄어들 수 있습니다. 따라서 dense prediction에서는 낮은 해상도의 semantic feature와 높은 해상도의 spatial feature를 어떻게 결합하는지가 중요한 설계 문제가 됩니다.</p>'''),
section('unet_architecture', 'U-Net 논문: context와 localization을 함께 연결하기', asset_figure('unet-flow.svg', 'U-Net encoder에서 해상도를 줄이고 decoder에서 복원하며 encoder feature를 concatenate하는 구조', 'Segmentation 주제 안에서 U-Net의 contracting path, expanding path와 skip concatenate를 보여 줍니다.') + '''<p>Ronneberger et al.의 U-Net은 contracting path에서 context를 추출하고 symmetric expanding path에서 해상도를 복원합니다. Encoder의 고해상도 feature를 decoder로 전달하는 skip connection은 세밀한 위치 정보를 다시 활용하게 합니다.</p>''' + table(['단계', '예시 shape', '역할'], [('Decoder upsample', '[B,128,128,128]', '깊은 feature의 공간 해상도를 복원'), ('Encoder skip', '[B,128,128,128]', '같은 scale의 고해상도 feature'), ('Concat, dim=1', '[B,256,128,128]', '공간 위치를 맞춘 뒤 channel 방향 결합'), ('Conv block', '[B,128,128,128]', '결합한 feature를 학습해 다음 representation 생성')]) + callout('ResNet과 같은 “skip”이 아니다', '원 U-Net은 encoder feature를 decoder feature와 concatenate합니다. 대표 ResNet block은 identity/projection branch를 main branch와 add합니다.')),
section('unet_original', '원 U-Net과 현대 same-padding 구현을 구분하기', '''<p>2015년 원 U-Net은 unpadded 3 × 3 convolution을 사용하므로 convolution을 지날 때 공간 크기가 줄어듭니다. 논문 Figure 1의 대표 흐름은 572 × 572 input에서 388 × 388 output을 만들며, encoder feature를 decoder에 연결할 때 crop이 필요합니다.</p>''' + table(['항목', '2015 원 논문', '많이 쓰이는 현대 구현'], [('3×3 Conv', 'valid / unpadded', 'same padding을 쓰는 경우가 많음'), ('입출력 크기', '572 → 388 예시', '입출력 공간 크기를 같게 유지하기도 함'), ('Skip', 'crop 후 concatenate', '동일 spatial size에서 concatenate'), ('손실', 'weighted pixel-wise softmax loss', 'CE, Dice 계열 등 다양한 선택')]) + '''<p>따라서 “U-Net은 항상 same padding”이나 “U-Net의 원래 loss가 Dice loss”라고 설명하면 부정확합니다. Dice 계열 loss는 이후 segmentation 실무에서 널리 사용되지만 원 논문의 핵심 손실과 구분해야 합니다.</p>'''),
section('unet_scope', 'U-Net 논문의 문제 설정과 한계', '''<p>원 논문은 생의학 영상 segmentation에서 제한된 수의 annotated image를 효율적으로 사용하기 위해 강한 data augmentation과 encoder–decoder 구조를 제안했습니다. 이 결과를 모든 자연영상·산업영상 segmentation에서 동일하게 보장되는 성능으로 해석해서는 안 됩니다.</p><p>산업 영상에서는 작은 defect의 pixel 크기, downsampling 비율, boundary label 품질, class imbalance, inference resolution을 별도로 검토해야 합니다. U-Net은 segmentation architecture를 이해하는 대표 사례이지 모든 segmentation 문제의 기본 정답은 아닙니다.</p>''')

], [('Ultralytics · Tasks', 'https://docs.ultralytics.com/tasks/', '분류·탐지·분할의 지원 태스크와 입출력 사용법입니다.'), ('COCO · Detection evaluation', 'https://cocodataset.org/#detection-eval', 'IoU 임계값과 평균 정밀도 평가 정의를 확인할 수 있습니다.'), ('Ronneberger et al. · U-Net: Convolutional Networks for Biomedical Image Segmentation', 'https://arxiv.org/abs/1505.04597', '2015 U-Net의 contracting/expanding path, crop-and-concat, augmentation과 원 손실의 근거입니다.'), ('U-Net 저자 프로젝트 페이지', 'https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/', '원 논문의 코드·자료가 연결된 저자 측 페이지입니다.')])

note('training', '학습·검증·평가를 구분하는 기준', '데이터 누수, 클래스별 분포, 교차검증과 임계값. 성능 숫자가 무엇을 의미하는지 확인합니다.', '학습·평가', '05 · TRAINING & EVALUATION', 22, [
section('loop', '학습에서 실제로 바뀌는 것은 무엇일까?', '''<p>지도학습은 입력과 정답 쌍을 사용해 예측 오차를 줄입니다. 모델이 예측을 만들면 loss가 정답과의 차이를 수치화하고, 역전파가 파라미터별 기울기를 계산합니다. Optimizer가 파라미터를 갱신하며 이 과정을 반복합니다.</p>''' + flow([('Forward', '입력 → logits'), ('Loss', '예측과 정답 비교'), ('Backward', '기울기 계산'), ('Optimizer', '파라미터 갱신')], '학습의 한 iteration. 다음 batch에서도 갱신된 파라미터를 사용합니다.') + '''<p>Epoch는 학습 데이터를 한 바퀴 사용하는 단위입니다. 3,200장, batch size 32, 남는 샘플이 없는 경우 한 epoch는 100 iteration입니다. Validation은 갱신 없이 일반화 성능을 살피는 과정이고, test는 설정을 정한 뒤 최종 평가에 사용합니다.</p>''' + table(['학습 방식', '정답을 사용하는 방식', '비전 예시'], [('지도학습', '클래스·박스·마스크 라벨', '불량 종류 분류, 부품 분할'), ('자기지도학습', '데이터 자체에서 학습 목표 구성', '가려진 패치 복원, 서로 다른 view의 표현 학습'), ('정상 데이터 기반 이상탐지', '정상 샘플을 학습에 사용', '정상 특징과의 거리를 이용한 결함 위치 탐지')]) + '''<p>비지도학습은 명시적 과업 정답 없이 구조를 찾는 넓은 범주입니다. 다만 정상만으로 적합한 이상탐지 모델이라도 threshold 선정에는 라벨이 있는 validation을 사용할 수 있으므로, 파이프라인 전체의 라벨 사용 범위를 구체적으로 밝혀야 합니다.</p>'''),
section('split', '비율보다 먼저 독립성을 지키기', '''<p>연속 영상의 이웃 프레임은 매우 비슷합니다. 프레임 단위로 무작위 분할하면 같은 장면이 train과 test 양쪽에 들어갈 수 있습니다. 평가 목적에 맞게 원본 영상·촬영 시간·장비 등의 그룹을 정하고, 그룹 전체를 한 split에 배정해야 합니다.</p>''' + svg(box(20,87,164,'원본 영상 그룹','그룹 단위 배정') + box(293,10,195,'Train','70% 목표') + box(293,111,195,'Validation','15% 목표') + box(293,212,195,'Test','15% 목표','dark') + edge('M 184 120 H 235 V 43 H 291') + edge('M 235 120 V 144 H 291') + edge('M 235 144 V 245 H 291') + '<text x="530" y="47" class="label">파라미터 학습</text><text x="530" y="148" class="label">모델·threshold 선택</text><text x="530" y="249" class="label">고정 후 최종 평가</text>',300,'예시 분할 정책. 세 갈래 중 하나에 그룹을 통째로 배정하며 동일 그룹을 복제해서 넣지 않습니다.') + '''<p>전체 비율만 70/15/15가 되어도 희소 클래스가 test에 0개라면 그 클래스의 recall을 평가할 수 없습니다. <strong>클래스별 개수와 독립 그룹 수</strong>를 확인해야 합니다. 클래스가 특정 그룹 한 개에만 있으면 그룹 독립성을 지키면서 세 split 모두에 넣는 것은 불가능합니다. 이때는 데이터를 추가하거나 평가 설계를 바꾸고 한계를 명시해야 합니다.</p>''' + table(['예시 클래스', '전체', 'Train 목표', 'Val 목표', 'Test 목표'], [('정상', '1,000', '700', '150', '150'), ('결함 A', '200', '140', '30', '30'), ('결함 B', '40', '28', '6', '6')]) + '<p class="small">설명을 위한 개수입니다. 실제 그룹 제약에서는 정확한 비율이 불가능할 수 있으므로, 누수 방지와 평가 가능한 클래스 구성을 우선합니다.</p>'),
section('cv', '3-fold CV는 전체 데이터를 세 번 나눠 평가하기', '''<p>세 개 fold로 나눈 뒤 두 개로 학습하고 하나로 검증합니다. 검증 fold를 바꿔 3번 반복하며, 각 반복은 모델을 새로 초기화합니다. 세 모델을 앞 모델의 가중치로 이어 학습하는 방식이 아닙니다.</p>''' + table(['반복', 'Fold A', 'Fold B', 'Fold C'], [('1', '검증', '학습', '학습'), ('2', '학습', '검증', '학습'), ('3', '학습', '학습', '검증')]) + '''<p>모든 샘플은 한 번 검증에, 두 번 학습에 사용됩니다. 평균과 표준편차를 보고하면 분할에 따른 변동을 이해하는 데 도움이 됩니다. 예를 들어 F1이 [0.80, 0.86, 0.83]이면 평균 0.83입니다. 표준편차는 사용한 모집단/표본 계산 방식을 함께 명시합니다.</p>''' + callout('튜닝과 최종 성능 추정', 'CV 검증 결과로 모델·threshold를 선택했다면 그 결과만으로 독립적인 최종 성능이 보장되지는 않습니다. 별도 test를 유지하거나 nested CV를 고려합니다. 설비 일반화가 목적이면 설비 그룹을 fold 경계로 사용합니다.')),
section('metrics', 'Threshold를 바꾸면 어떤 오류가 달라질까?', '''<p>이 예시는 정상 5개와 이상 5개, 총 10개 샘플의 고정된 점수를 사용합니다. 점수가 threshold 이상이면 이상으로 판정합니다. 점수는 실제 데이터에서 얻은 결과가 아닌 학습용 예시입니다.</p><div class="lab"><div class="lab-heading"><h3>이상 판정 임계값</h3><span class="lab-badge">INTERACTIVE</span></div><div class="controls"><label for="threshold">Threshold <output id="threshold-value">0.50</output></label><input id="threshold" type="range" min="0" max="100" value="50" step="1"></div><div class="cm"><div><span>TP · 이상을 이상으로</span><strong id="tp"></strong></div><div class="bad"><span>FP · 정상을 이상으로</span><strong id="fp"></strong></div><div class="bad"><span>FN · 이상을 정상으로</span><strong id="fn"></strong></div><div><span>TN · 정상을 정상으로</span><strong id="tn"></strong></div></div><div class="metric-grid"><div><b id="precision"></b><span>Precision</span></div><div><b id="recall"></b><span>Recall</span></div><div><b id="f1"></b><span>F1</span></div></div><p class="lab-note">실제 이상 점수: .95, .86, .73, .64, .44 / 실제 정상 점수: .79, .57, .32, .22, .09</p></div>''' + equation('Precision = TP / (TP + FP)\nRecall = TP / (TP + FN)\nF1 = 2TP / (2TP + FP + FN)') + '''<p>Threshold 0.50이면 TP=4, FP=2, FN=1, TN=3입니다. Precision≈0.667, Recall=0.800, F1≈0.727입니다. Threshold를 낮추면 이 고정된 점수 집합에서 recall은 감소하지 않고 FP는 증가할 수 있습니다. Precision은 데이터의 점수 순서에 따라 단조롭게 움직이지 않을 수도 있습니다.</p><p>이상으로 예측한 샘플이 0개이면 precision의 분모가 0입니다. 위 데모는 “정의 안 됨”으로 표시합니다. 보고서에서는 라이브러리의 zero-division 처리 규칙을 명시해야 합니다.</p>'''),
section('report', '실험 기록에 남길 최소 정보', table(['항목', '예시', '필요한 이유'], [('데이터', '그룹 목록·클래스별 개수·split 버전', '같은 조건의 재평가'), ('학습', '입력 640, batch 32, seed, 증강', '결과 차이를 해석'), ('모델', '가중치 hash·라이브러리 버전', '실제 사용한 모델 식별'), ('평가', '클래스별 precision/recall·혼동행렬', '희소 클래스 실패 확인'), ('판정', 'threshold·영상 집계 규칙', '프레임 점수와 최종 판정 구분')]) + callout('기억할 핵심', '평가 숫자는 “어떤 데이터에 어떤 규칙으로 평가했는가”와 함께 해석합니다. 데이터 분할, threshold, 후처리를 바꾸면 서로 다른 실험입니다.'))
], [('scikit-learn · Cross-validation', 'https://scikit-learn.org/stable/modules/cross_validation.html', 'GroupKFold와 교차검증의 기본 원칙입니다.'), ('scikit-learn · Model evaluation', 'https://scikit-learn.org/stable/modules/model_evaluation.html', 'Precision·recall·F1과 평균 방식의 정의입니다.'), ('PyTorch · Optimization', 'https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html', '학습·검증 반복과 optimizer의 동작을 설명합니다.')])

note('patchcore', 'Anomaly Detection: 정상 특징에서 PatchCore까지', '정상 데이터 기반 이상 탐지의 문제를 먼저 정의하고, PatchCore의 memory bank·coreset·최근접 거리 방식을 대표 사례로 설명합니다.', 'Anomaly Detection', '06 · ANOMALY DETECTION', 22, [
section('problem', '불량 종류를 모두 모으기 어려울 때', '''<p>제조 환경에서는 정상 이미지는 많지만 불량은 드물고, 앞으로 나타날 불량의 모양을 모두 라벨링하기 어렵습니다. PatchCore는 정상 이미지에서 얻은 지역 특징을 저장한 뒤, 테스트 패치가 정상 특징과 얼마나 다른지를 이용합니다.</p><p>이 논문에서의 “학습”은 보통 대상 정상 이미지로 새로운 분류기를 역전파 학습하는 과정이 아니라, 사전학습된 특징 추출기로 <strong>정상 특징 memory bank를 구성하는 과정</strong>입니다. 사전학습 backbone 자체가 이미 다른 데이터로 학습되었다는 사실은 별개입니다.</p>'''),
section('pipeline', '정상 데이터 준비와 검사 과정을 분리하기', asset_figure('patchcore-memory.svg', '정상 이미지에서 CNN 지역 특징을 추출해 memory bank를 구성하고 검사 patch의 최근접 거리를 계산하는 PatchCore 흐름', '정상 feature memory bank와 검사 시 nearest-neighbor anomaly score의 관계입니다.') + svg(box(20,30,172,'정상 학습 이미지','여러 정상 조건') + box(275,30,191,'지역 특징 추출','사전학습 CNN') + box(545,30,190,'Memory bank','Coreset 선택','dark') + edge('M 192 63 H 273') + edge('M 466 63 H 543') + box(20,191,172,'검사 이미지','정상 또는 이상') + box(275,191,191,'지역 특징 추출','같은 backbone') + box(545,191,190,'최근접 거리','점수 · 이상 지도') + edge('M 192 224 H 273') + edge('M 466 224 H 543') + edge('M 640 96 V 189') + '<text x="534" y="148" class="sub">정상 특징과 비교</text>',300,'정상 특징 저장과 검사 과정. Backbone의 동일한 층·전처리·특징 결합을 양쪽에서 사용합니다.') + '''<p>PatchCore는 중간 CNN 특징을 활용하고 주변 지역을 집계해 patch-level descriptor를 만듭니다. 여러 단계의 특징은 해상도를 맞춘 뒤 결합합니다. 여기서 patch는 원본 RGB를 단순히 16 × 16으로 잘라 만든 ViT token과 동일한 의미가 아닙니다. CNN feature map의 위치와 수용영역을 바탕으로 한 지역 표현입니다.</p>'''),
section('memory', '모든 정상 특징을 저장하면 얼마나 커질까?', '''<p>예를 들어 정상 이미지 1,000장, 이미지마다 28 × 28개의 특징, 특징 차원 1,024, float32라면 784,000개 벡터가 생깁니다. 저장량은 784,000 × 1,024 × 4 = 3,211,264,000 bytes로 약 <strong>3.21 GB</strong>입니다. 이 수치는 논문의 고정 설정이 아니라 저장량을 이해하기 위한 가정입니다.</p>''' + equation('Memory ≈ 이미지 수 × 특징 위치 수 × 특징 차원 × 원소 bytes\n1,000 × 784 × 1,024 × 4 ≈ 3.21 GB') + '''<p>Coreset은 전체 정상 특징을 대표할 작은 부분집합입니다. 가까운 점만 많이 보관하는 중복을 줄이면서 특징 공간의 다양한 정상 패턴을 커버하려는 목적입니다. 원 논문은 greedy 방식의 근사 coreset 선택을 사용합니다. 무작위로 일부를 고르는 것과 선택 목적이 다릅니다.</p>''' + svg('''<text x="27" y="27" class="label">전체 정상 특징</text><text x="465" y="27" class="label">대표점 · coreset</text>''' + ''.join(f'<circle cx="{45+(i*47)%265}" cy="{64+(i*31)%115}" r="5" fill="#9bb0d6"/>' for i in range(42)) + edge('M 345 119 H 417') + ''.join(f'<circle cx="{x}" cy="{y}" r="10" fill="#2454d8"/>' for x,y in [(462,70),(575,70),(686,92),(480,170),(604,169),(559,119)]) + '<text x="369" y="155" class="sub" text-anchor="middle">선택</text>',215,'특징 공간의 대표점 선택을 설명하는 개념도. 실제 coreset 알고리즘 실행 결과가 아닙니다.') + '''<p>10%를 선택한다는 가정이면 벡터 저장량은 약 321 MB로 줄어듭니다. 검색용 인덱스와 실행 중 텐서 메모리는 별도로 필요합니다. 선택 비율을 줄이면 메모리·검색 비용은 줄 수 있지만 정상의 다양성을 놓칠 수도 있어 검증이 필요합니다.</p>'''),
section('score', '최근접 거리가 이상 점수가 되는 이유', equation('패치 점수 sᵢ = min_{m ∈ M} ||fᵢ − m||₂\nM: 정상 특징 저장소 / fᵢ: 검사 이미지 i번째 지역 특징') + '''<p>검사 특징과 정상 특징이 가까우면 저장된 정상 패턴과 비슷하다고 봅니다. 멀면 정상에서 보기 어려운 패턴일 수 있습니다. 2차원 장난감 예시에서 정상 벡터 [1,1], 검사 벡터 [1.1,1.2]의 거리는 약 0.224입니다. 검사 벡터 [4,5]라면 거리는 5입니다. 실제 특징은 훨씬 고차원이고 거리의 범위도 모델·전처리에 따라 달라집니다.</p><p>패치별 점수를 공간 위치에 돌려 놓고 입력 해상도로 업샘플링하면 이상 지도를 만들 수 있습니다. 큰 점수의 위치가 이상 후보가 됩니다. 원 논문은 이미지 수준 점수에 최대 패치 거리와 주변 정상 특징을 활용한 <strong>재가중</strong>도 사용합니다. 따라서 “원 논문 점수는 무조건 max 거리 하나”라고 설명하면 세부가 빠집니다.</p>''' + flow([('패치별 거리', '28 × 28 예시'), ('공간 복원', '거리 지도'), ('업샘플링', '입력 해상도'), ('결과', '이상 위치 · 점수')], '이상 지도의 개념적 데이터 흐름. 정확한 해상도·평활화·이미지 점수 계산은 구현 설정에 따라 확인합니다.')),
section('limits', '정상과 다르다고 반드시 불량은 아니다', '''<p>조명 변경, 카메라 위치 변화, 정상 부품의 새로운 재질도 특징 공간에서 멀어질 수 있습니다. 반대로 미세 결함이 다운샘플링 과정에서 사라지거나 정상 특징과 비슷하면 검출이 어려울 수 있습니다. 모델은 공정의 불량 정의를 자동으로 알고 있는 것이 아닙니다.</p>''' + table(['상황', '가능한 결과', '확인할 항목'], [('정상 조명 조건 누락', '정상인데 높은 이상 점수', '정상 학습 데이터의 다양성'), ('작은 결함', '낮은 점수 또는 흐린 이상 지도', '입력·특징 해상도와 수용영역'), ('정상 데이터 오염', '결함 특징이 정상 bank에 포함', '정상 데이터 품질'), ('새 카메라·새 공정', '점수 분포 변화', '도메인별 validation과 threshold')]) + '''<p>Threshold는 특정 데이터의 validation으로 정하고 test 전에 고정해야 합니다. Image AUROC는 이미지 수준 이상/정상 구분을, pixel AUROC 등은 위치 단위 결과를 평가합니다. 서로 다른 평가 단위를 섞어서 하나의 성능처럼 보고하면 안 됩니다.</p>''' + callout('이 논문의 핵심', '정상 지역 특징을 잘 대표하는 저장소를 만들고 검사 특징의 최근접 거리를 사용합니다. Coreset은 저장 비용을 줄이는 핵심 장치이며, 좋은 정상 데이터와 검증된 판정 기준이 함께 필요합니다.'))
], [('Roth et al. · Towards Total Recall in Industrial Anomaly Detection', 'https://arxiv.org/abs/2106.08265', 'CVPR 2022. PatchCore의 지역 특징, coreset, 점수 재가중을 설명하는 원문입니다.'), ('공식 구현 · amazon-science/patchcore-inspection', 'https://github.com/amazon-science/patchcore-inspection', '특징 계층·coreset·검색과 점수 계산을 확인할 수 있습니다.')])



register_reference_notes(
    note=note,
    section=section,
    table=table,
    callout=callout,
    equation=equation,
    flow=flow,
)


# Make the representative-paper role explicit in the section headings.
vit = next(item for item in NOTES if item["slug"] == "vit")
vit["sections"][0] = (
    vit["sections"][0][0],
    "대표 논문 ViT · Transformer를 이미지 분류에 적용한 문제 설정",
    vit["sections"][0][2],
)
patchcore = next(item for item in NOTES if item["slug"] == "patchcore")
patchcore["sections"][0] = (
    patchcore["sections"][0][0],
    "정상 데이터 기반 이상 탐지와 대표 방법 PatchCore",
    patchcore["sections"][0][2],
)


def nav(current, prefix):
    groups = ['이미지·CNN', 'Transformer·Attention', 'Vision Tasks·Segmentation', '학습·평가', 'Anomaly Detection', '종합 이론']
    names = {
        'pixels': '이미지와 텐서',
        'cnn': 'CNN · ResNet',
        'vit': 'Transformer · ViT',
        'tasks': 'Vision Tasks · U-Net',
        'training': '학습과 평가',
        'patchcore': 'Anomaly Detection',
        'cs231n': 'CS231n 전체 정리',
        'prml': 'PRML 전체 정리',
    }
    content = f'<a href="{prefix}index.html" {"aria-current=page" if current == "home" else ""}><span>00</span>학습 노트 전체</a>'
    for group in groups:
        content += f'<p class="nav-label">{group}</p>'
        for item in NOTES:
            if item['group'] == group:
                content += f'<a href="{prefix}notes/{item["slug"]}.html" {"aria-current=page" if current == item["slug"] else ""}><span>{item["label"][:2]}</span>{names[item["slug"]]}</a>'
    return content


def page(title, description, current, body, prefix='', toc=''):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#14213b"><title>{escape(title)} · Vision AI Notes</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script></head>
<body><a class="skip" href="#main">본문으로 이동</a><aside id="sidebar" class="sidebar"><a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>Vision AI Notes</a><p class="sub">이해하고, 연결하고, 쌓아가기.</p><nav aria-label="학습 주제">{nav(current, prefix)}</nav><div class="sidebar-foot">Personal study notebook<br><a href="https://github.com/sh0427-han/vision_ai">GitHub 저장소 ↗</a></div></aside><div class="shell"><header class="topbar"><button class="menu" type="button" aria-label="목차 열기" aria-controls="sidebar" aria-expanded="false">목차</button><span class="trail">Vision AI / {"학습 노트" if current == "home" else "개념과 구조"}</span><a href="{prefix}index.html">전체 자료 보기</a></header><div class="layout{' home' if current == 'home' else ''}"><main id="main">{body}</main>{toc}</div></div></body></html>'''


def miniature(slug):
    if slug == 'pixels':
        return '<svg viewBox="0 0 390 100" aria-hidden="true">' + ''.join(f'<rect x="{x*19+35}" y="{y*19+7}" width="16" height="16" rx="2" fill="rgb({50+x*23},{70+y*26},{135+x*16})"/>' for y in range(5) for x in range(5)) + '<text x="161" y="47" fill="#2454d8" font-size="21" font-family="monospace">[B, C, H, W]</text><text x="161" y="73" fill="#617596" font-size="13" font-family="monospace">32 × 3 × 224 × 224</text></svg>'
    if slug == 'vit':
        return '<svg viewBox="0 0 390 100" aria-hidden="true">' + ''.join(f'<rect x="{x*16+28}" y="{y*16+18}" width="13" height="13" rx="2" fill="#769aeb"/>' for y in range(4) for x in range(4)) + ''.join(f'<path d="M 106 50 L {160+i*28} 32" stroke="#a4b8df"/>' for i in range(7)) + ''.join(f'<rect x="{150+i*28}" y="35" width="19" height="33" rx="3" fill="{ "#0b9286" if i==0 else "#2454d8"}"/>' for i in range(7)) + '</svg>'
    if slug == 'patchcore':
        return '<svg viewBox="0 0 390 100" aria-hidden="true">' + ''.join(f'<circle cx="{30+(i*39)%150}" cy="{17+(i*29)%70}" r="4" fill="#91acd8"/>' for i in range(25)) + '<path d="M 193 50 H 240" stroke="#2454d8" stroke-width="2"/><rect x="260" y="15" width="90" height="70" rx="8" fill="#e2ecef"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#08796f"/>' for x,y in [(278,33),(328,33),(301,53),(277,72),(330,72)]) + '</svg>'
    if slug == 'training':
        return '<svg viewBox="0 0 390 100" aria-hidden="true">' + ''.join(f'<rect x="{28+j*112}" y="{10+i*29}" width="100" height="20" rx="3" fill="{ "#0b9286" if i==j else "#7497e5"}"/>' for i in range(3) for j in range(3)) + '</svg>'
    if slug == 'tasks':
        return '<svg viewBox="0 0 390 100" aria-hidden="true"><rect x="26" y="25" width="92" height="51" rx="6" fill="#2454d8"/><text x="72" y="58" text-anchor="middle" fill="white" font-size="18">class</text><rect x="149" y="17" width="80" height="67" rx="4" fill="none" stroke="#2454d8" stroke-width="3"/><path d="M 286 23 L 338 19 L 355 55 L 330 84 L 284 70 Z" fill="#0b9286"/></svg>'
    if slug == 'cs231n':
        return '<svg viewBox="0 0 390 100" aria-hidden="true"><rect x="20" y="34" width="58" height="32" rx="5" fill="#dce7fb"/><rect x="98" y="34" width="58" height="32" rx="5" fill="#b9cdf6"/><rect x="176" y="34" width="58" height="32" rx="5" fill="#759ae6"/><rect x="254" y="34" width="58" height="32" rx="5" fill="#2454d8"/><path d="M78 50 H96 M156 50 H174 M234 50 H252 M312 50 H354" stroke="#7891b7" stroke-width="2"/><text x="49" y="55" text-anchor="middle" fill="#203455" font-size="11">data</text><text x="127" y="55" text-anchor="middle" fill="#203455" font-size="11">loss</text><text x="205" y="55" text-anchor="middle" fill="white" font-size="11">grad</text><text x="283" y="55" text-anchor="middle" fill="white" font-size="11">CNN</text><circle cx="360" cy="50" r="10" fill="#08796f"/></svg>'
    if slug == 'prml':
        return '<svg viewBox="0 0 390 100" aria-hidden="true"><circle cx="70" cy="50" r="27" fill="#edf3ff" stroke="#759ae6" stroke-width="2"/><circle cx="195" cy="50" r="27" fill="#e5f5f2" stroke="#08796f" stroke-width="2"/><circle cx="320" cy="50" r="27" fill="#eef1f7" stroke="#14213b" stroke-width="2"/><path d="M98 50 H166 M223 50 H291" stroke="#7891b7" stroke-width="2"/><text x="70" y="55" text-anchor="middle" fill="#203455" font-size="11">p(D)</text><text x="195" y="55" text-anchor="middle" fill="#08796f" font-size="11">p(w|D)</text><text x="320" y="55" text-anchor="middle" fill="#14213b" font-size="11">decision</text></svg>'
    return '<svg viewBox="0 0 390 100" aria-hidden="true">' + ''.join(f'<rect x="{32+i*82+j*6}" y="{30-j*5}" width="45" height="50" rx="4" fill="{["#aac1ee","#759ae6","#2454d8"][j]}" stroke="#fff"/>' for i in range(4) for j in range(3)) + '</svg>'


def render():
    build_extra_diagrams(ROOT / 'assets' / 'diagrams' / 'extra')
    build_paper_figures(ROOT / 'assets' / 'diagrams' / 'paper')
    build_reference_figures(ROOT / 'assets' / 'diagrams' / 'reference')
    (ROOT / 'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#14213b"/><path d="M7 7h7v7H7zm11 0h7v7h-7zM7 18h7v7H7z" fill="#91afff"/><path d="M18 18h7v7h-7z" fill="#20c4bb"/></svg>', encoding='utf-8')
    for i, item in enumerate(NOTES):
        toc = '<aside class="toc" aria-label="이 페이지 목차"><p>이 페이지에서</p>' + ''.join(f'<a href="#{anchor}">{title}</a>' for anchor,title,_ in item['sections']) + '<a href="#sources">출처와 더 확인할 자료</a></aside>'
        body = f'<header><p class="eyebrow">{item["label"]}</p><h1>{item["title"]}</h1><p class="lead">{item["subtitle"]}</p><div class="meta"><span class="tag">{item["group"]}</span><span class="tag">예상 학습 {item["minutes"]}분</span><span class="tag">수치 예시 · 직접 그린 도식</span></div></header>'
        body += ''.join(
            f'<section class="article-section" id="{anchor}"><h2>{title}</h2>'
            f'{content}{section_paper_figures(item["slug"], anchor)}{section_reference_figures(item["slug"], anchor)}{section_visuals(item["slug"], anchor)}</section>'
            for anchor, title, content in item['sections']
        )
        body += '<section class="article-section" id="sources"><h2>출처와 더 확인할 자료</h2><p class="small">본문은 이해를 위한 한국어 해설입니다. 도식은 직접 재구성했으며, 가상 수치와 단순화한 구조는 해당 위치에 표시했습니다.</p><ol class="references">' + ''.join(f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{title} ↗</a><small>{description}</small></li>' for title,url,description in item['sources']) + '</ol></section>'
        prev = NOTES[i-1] if i else None
        nex = NOTES[i+1] if i+1 < len(NOTES) else None
        body = annotate_first_terms(body, item["slug"])
        body += '<nav class="pager" aria-label="이전 다음 자료">' + (f'<a href="{prev["slug"]}.html">← {prev["title"].split(":")[0]}</a>' if prev else '<a href="../index.html">← 전체 자료</a>') + (f'<a href="{nex["slug"]}.html">{nex["title"].split(":")[0]} →</a>' if nex else '<a href="../index.html">전체 자료 →</a>') + '</nav><footer class="footer">Vision AI Notes · 개인 학습 자료 · 최초 작성 2026.09.22</footer>'
        html = page(item['title'], item['subtitle'], item['slug'], body, '../', toc)
        # A document may contain multiple independent SVGs; marker IDs must be unique.
        counter = 0
        pieces = html.split('<figure>')
        for j in range(1, len(pieces)):
            counter += 1
            pieces[j] = pieces[j].replace('id="arrow"', f'id="arrow-{counter}"').replace('url(#arrow)', f'url(#arrow-{counter})')
        (ROOT / 'notes' / f'{item["slug"]}.html').write_text('<figure>'.join(pieces), encoding='utf-8')
    legacy_redirects = {
        'resnet.html': (
            'cnn.html#resnet-problem',
            'ResNet 내용은 CNN 주제로 이동했습니다.',
        ),
        'unet.html': (
            'tasks.html#unet-problem',
            'U-Net 내용은 Vision Tasks 주제로 이동했습니다.',
        ),
    }
    for filename, (target, message) in legacy_redirects.items():
        body = (
            '<header data-legacy-redirect="true"><p class="eyebrow">MOVED</p>'
            f'<h1>{message}</h1>'
            f'<p class="lead"><a href="{target}">새 위치에서 계속 읽기 →</a></p>'
            '</header>'
        )
        redirect_html = page(
            '자료 위치 변경',
            message,
            'legacy',
            body,
            '../',
        )
        redirect_html = redirect_html.replace(
            '</head>',
            f'<meta http-equiv="refresh" content="0; url={target}"></head>',
        )
        (ROOT / 'notes' / filename).write_text(
            redirect_html,
            encoding='utf-8',
        )

    home = f'''<div class="home-intro"><p class="eyebrow">VISION AI · STUDY NOTEBOOK</p><h1>이미지에서 시작해,<br>모델의 동작까지.</h1><p class="lead">숫자가 특징이 되고, 특징이 판단이 되는 과정.<br>큰 주제를 먼저 이해하고, 관련 논문·강의·교과서를 근거와 사례로 연결하는 학습 노트입니다.</p><a class="start-link" href="notes/pixels.html">이미지와 텐서부터 시작하기 <span aria-hidden="true">→</span></a><div class="meta"><span class="tag">{len(NOTES)}개 학습 자료</span><span class="tag">4개 인터랙티브 예시</span><span class="tag">논문 · 공식 자료 기반</span></div></div>'''
    group_subtitles = {
        '이미지·CNN': '픽셀 · 텐서 · 합성곱 · ResNet',
        'Transformer·Attention': 'token · Q/K/V · ViT',
        'Vision Tasks·Segmentation': '분류 · 탐지 · mask · U-Net',
        '학습·평가': 'split · optimization · metric · threshold',
        'Anomaly Detection': 'normal feature · memory bank · PatchCore',
        '종합 이론': 'CS231n · PRML을 큰 흐름으로 다시 연결',
    }
    for group in ['이미지·CNN', 'Transformer·Attention', 'Vision Tasks·Segmentation', '학습·평가', 'Anomaly Detection', '종합 이론']:
        home += f'<div class="section-label"><h2>{group}</h2><span>{group_subtitles[group]}</span></div><div class="note-grid">'
        for item in NOTES:
            if item['group'] != group:
                continue
            home += f'<a class="note-card" href="notes/{item["slug"]}.html"><div class="mini-viz">{miniature(item["slug"])}</div><div class="card-body"><div class="card-meta"><span>{item["label"]}</span><span>약 {item["minutes"]}분</span></div><h3>{item["title"]}</h3><p>{item["subtitle"]}</p></div></a>'
        home += '</div>'
    home += '''<section class="article-section"><h2>개념을 서로 연결해서 이해하기</h2><div class="two-col"><div class="mini-card"><h3>CNN 안에서 ResNet 이해하기</h3><p>합성곱의 지역 계산을 익힌 뒤, 같은 CNN 주제 안에서 깊은 네트워크의 residual learning으로 확장합니다.</p></div><div class="mini-card"><h3>패치에서 ViT·PatchCore로</h3><p>ViT의 입력 패치와 PatchCore의 지역 특징은 다른 개념입니다. 각 모델이 만드는 벡터와 사용하는 연산을 비교해 보세요.</p></div></div></section><footer class="footer">Vision AI Notes · 최초 작성 2026.09.22 · 설명용 예시는 실제 실험 결과와 구분해 표시합니다.</footer>'''
    (ROOT / 'index.html').write_text(page('학습 노트', 'Vision AI 개념과 논문 내용을 도식, 수치 예시, 인터랙티브 실험으로 설명하는 한국어 학습 노트.', 'home', home), encoding='utf-8')
    print(f'Built {len(NOTES) + 1} HTML pages.')


if __name__ == '__main__':
    render()

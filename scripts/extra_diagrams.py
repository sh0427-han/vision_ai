"""Generate reusable SVG teaching diagrams for the Vision AI study site."""
from html import escape
from pathlib import Path


def _esc(value):
    return escape(str(value))


def _frame(title, subtitle, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520">
<style>
text{{font-family:'NanumGothic','Noto Sans CJK KR','Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif}}
.t{{font-size:30px;font-weight:700;fill:#203455}}
.s{{font-size:18px;fill:#5b6880}}
.l{{font-size:20px;font-weight:700;fill:#203455}}
.m{{font-size:16px;fill:#5b6880}}
.edge{{stroke:#7891b7;stroke-width:4;fill:none}}
.thin{{stroke:#9aabc7;stroke-width:2;fill:none}}
</style>
<rect width="1200" height="520" rx="28" fill="#f7f9fc"/>
<text x="48" y="58" class="t">{_esc(title)}</text>
<text x="48" y="91" class="s">{_esc(subtitle)}</text>
{body}</svg>"""


def _arrow(x1, y1, x2, y2):
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" class="edge"/>'
        f'<polygon points="{x2},{y2} {x2-18},{y2-12} {x2-18},{y2+12}" fill="#7891b7"/>'
    )


def _card(x, y, w, h, title, sub="", dark=False):
    fill = "#2454d8" if dark else "#fff"
    stroke = "#2454d8" if dark else "#c7d5ee"
    text = "#fff" if dark else "#203455"
    subc = "#e5edff" if dark else "#5b6880"
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        f'<text x="{x+w/2}" y="{y+h/2-7}" text-anchor="middle" '
        f'font-size="19" font-weight="700" fill="{text}">{_esc(title)}</text>'
        f'<text x="{x+w/2}" y="{y+h/2+24}" text-anchor="middle" '
        f'font-size="15" fill="{subc}">{_esc(sub)}</text>'
    )


def _flow(title, subtitle, steps):
    n = len(steps)
    gap = 35
    w = min(190, (1040 - (n - 1) * gap) / n)
    total = n * w + (n - 1) * gap
    start = (1200 - total) / 2
    y = 190
    body = []
    for i, step in enumerate(steps):
        name, sub = step[:2]
        dark = len(step) > 2 and bool(step[2])
        x = start + i * (w + gap)
        body.append(_card(x, y, w, 120, name, sub, dark))
        if i < n - 1:
            body.append(_arrow(x + w, y + 60, x + w + 31, y + 60))
    return _frame(title, subtitle, "".join(body))


def _compare(title, subtitle, left_title, left_lines, right_title, right_lines):
    def lines(x, y, values):
        return "".join(
            f'<text x="{x}" y="{y+i*34}" class="m">• {_esc(v)}</text>'
            for i, v in enumerate(values)
        )
    body = (
        '<rect x="80" y="145" width="470" height="300" rx="20" '
        'fill="#fff" stroke="#b9c9e7" stroke-width="3"/>'
        '<rect x="650" y="145" width="470" height="300" rx="20" '
        'fill="#fff" stroke="#8ac7a5" stroke-width="3"/>'
        f'<text x="315" y="195" text-anchor="middle" class="l">{_esc(left_title)}</text>'
        f'<text x="885" y="195" text-anchor="middle" class="l">{_esc(right_title)}</text>'
        + lines(120, 245, left_lines)
        + lines(690, 245, right_lines)
    )
    return _frame(title, subtitle, body)


def _matrix(title, subtitle, rows=6, cols=6):
    hot = {1, 7, 14, 20, 27, 35}
    cw, ch = 70, 55
    body = ['<g transform="translate(390 145)">']
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            active = idx in hot
            body.append(
                f'<rect x="{c*cw}" y="{r*ch}" width="{cw-6}" height="{ch-6}" rx="5" '
                f'fill="{"#2454d8" if active else "#e8eef9"}" stroke="#c7d5ee"/>'
            )
            body.append(
                f'<text x="{c*cw+32}" y="{r*ch+33}" text-anchor="middle" font-size="14" '
                f'fill="{"#fff" if active else "#203455"}">{"high" if active else "·"}</text>'
            )
    body.append("</g>")
    return _frame(title, subtitle, "".join(body))


def _curve(title, subtitle, labels):
    colors = ["#2454d8", "#08796f", "#a24d18"]
    paths = [
        "M160 385 C300 320 430 260 570 225 C720 190 900 175 1060 165",
        "M160 390 C300 370 440 330 570 275 C710 220 860 200 1060 195",
        "M160 185 C300 210 440 255 590 320 C740 365 900 385 1060 397",
    ]
    body = ['<path d="M150 410 H1080 M150 410 V145" class="edge"/>']
    for i, label in enumerate(labels):
        body.append(
            f'<path d="{paths[i]}" stroke="{colors[i]}" stroke-width="5" fill="none"/>'
        )
        body.append(
            f'<text x="835" y="{150+i*32}" font-size="17" font-weight="700" '
            f'fill="{colors[i]}">{_esc(label)}</text>'
        )
    return _frame(title, subtitle, "".join(body))



def _optimization_curve(title, subtitle):
    """Loss should decrease as optimization progresses."""
    body = [
        '<path d="M150 410 H1080 M150 410 V145" class="edge"/>',
        '<text x="1090" y="438" text-anchor="end" class="m">iteration</text>',
        '<text x="125" y="155" text-anchor="end" class="m">loss</text>',
        '<path d="M175 190 C300 225 410 275 535 320 C675 365 835 382 1035 390" '
        'stroke="#2454d8" stroke-width="6" fill="none"/>',
    ]
    points = [(175,190),(285,226),(395,270),(515,316),(650,352),(800,375),(960,387)]
    for i,(x,y) in enumerate(points):
        body.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#08796f"/>')
        if i < len(points)-1:
            nx,ny=points[i+1]
            body.append(_arrow(x+10,y+4,nx-10,ny-4))
    body += [
        '<text x="235" y="175" class="m" fill="#2454d8">high loss</text>',
        '<text x="875" y="360" class="m" fill="#08796f">lower loss</text>',
        '<text x="665" y="215" class="m">each marker = one parameter update</text>',
    ]
    return _frame(title, subtitle, "".join(body))


def _overfit_curve(title, subtitle):
    """Training loss falls; validation loss bottoms out then rises."""
    body = [
        '<path d="M150 410 H1080 M150 410 V145" class="edge"/>',
        '<text x="1090" y="438" text-anchor="end" class="m">epoch</text>',
        '<text x="125" y="155" text-anchor="end" class="m">loss</text>',
        '<path d="M175 195 C310 245 440 305 570 345 C710 378 865 392 1045 398" '
        'stroke="#2454d8" stroke-width="6" fill="none"/>',
        '<path d="M175 205 C305 250 430 300 555 330 C665 350 760 345 850 320 '
        'C930 298 995 270 1045 245" stroke="#a24d18" stroke-width="6" fill="none"/>',
        '<line x1="725" y1="155" x2="725" y2="410" stroke="#7891b7" '
        'stroke-width="3" stroke-dasharray="10 8"/>',
        '<text x="740" y="180" class="m">best val checkpoint</text>',
        '<text x="835" y="215" class="m" fill="#a24d18">validation loss rises</text>',
        '<text x="835" y="388" class="m" fill="#2454d8">train loss keeps falling</text>',
        '<text x="900" y="285" class="m">overfit region</text>',
    ]
    return _frame(title, subtitle, "".join(body))


def _threshold_curve(title, subtitle):
    """For fixed scores, recall and FPR are non-increasing as threshold rises."""
    body = [
        '<path d="M150 410 H1080 M150 410 V145" class="edge"/>',
        '<text x="1090" y="438" text-anchor="end" class="m">threshold →</text>',
        '<text x="125" y="155" text-anchor="end" class="m">rate</text>',
        '<text x="155" y="445" class="m">low</text>',
        '<text x="1045" y="445" text-anchor="end" class="m">high</text>',
        '<path d="M175 175 C300 185 430 210 560 250 C710 300 865 350 1045 385" '
        'stroke="#2454d8" stroke-width="6" fill="none"/>',
        '<path d="M175 235 C300 255 430 290 560 325 C710 362 865 390 1045 402" '
        'stroke="#08796f" stroke-width="6" fill="none"/>',
        '<line x1="590" y1="155" x2="590" y2="410" stroke="#a24d18" '
        'stroke-width="3" stroke-dasharray="10 8"/>',
        '<text x="605" y="180" class="m" fill="#a24d18">example operating threshold</text>',
        '<text x="860" y="310" class="m" fill="#2454d8">Recall</text>',
        '<text x="860" y="382" class="m" fill="#08796f">False-positive rate</text>',
        '<text x="235" y="205" class="m">more samples predicted positive</text>',
        '<text x="760" y="245" class="m">fewer samples predicted positive</text>',
    ]
    return _frame(title, subtitle, "".join(body))

def _confusion():
    body = """<g transform="translate(330 150)">
<rect width="220" height="130" fill="#e5f5f2" stroke="#8ac7a5"/>
<rect x="230" width="220" height="130" fill="#fff0e5" stroke="#d79b66"/>
<rect y="140" width="220" height="130" fill="#fff0e5" stroke="#d79b66"/>
<rect x="230" y="140" width="220" height="130" fill="#e5f5f2" stroke="#8ac7a5"/>
<text x="110" y="58" text-anchor="middle" class="l">TP</text>
<text x="340" y="58" text-anchor="middle" class="l">FP</text>
<text x="110" y="198" text-anchor="middle" class="l">FN</text>
<text x="340" y="198" text-anchor="middle" class="l">TN</text>
<text x="110" y="92" text-anchor="middle" class="m">이상을 이상으로</text>
<text x="340" y="92" text-anchor="middle" class="m">정상을 이상으로</text>
<text x="110" y="232" text-anchor="middle" class="m">이상을 정상으로</text>
<text x="340" y="232" text-anchor="middle" class="m">정상을 정상으로</text>
</g>"""
    return _frame("Confusion Matrix 읽기", "오류를 TP·FP·FN·TN 네 경우로 나눠 봅니다.", body)


def _gaussian():
    body = """<path d="M140 410 H1080 M610 410 V145" class="thin"/>
<path d="M180 405 C300 402 390 360 470 270 C535 195 580 165 610 160
C640 165 685 195 750 270 C830 360 920 402 1040 405"
stroke="#2454d8" stroke-width="6" fill="none"/>
<text x="610" y="455" text-anchor="middle" class="m">mean μ</text>
<text x="790" y="235" class="m">variance σ² → 폭</text>"""
    return _frame("Gaussian distribution", "평균은 중심, 분산은 퍼짐 정도를 결정합니다.", body)


def _regression():
    points = [(230,350),(330,315),(440,300),(520,260),(650,245),(760,205),(860,220),(960,170)]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#08796f"/>' for x,y in points)
    body = (
        '<path d="M160 410 H1060 M160 410 V150" class="edge"/>'
        + dots
        + '<path d="M205 365 L1000 165" stroke="#2454d8" stroke-width="5"/>'
        + '<text x="800" y="330" class="m">prediction y(x,w)</text>'
    )
    return _frame("Linear regression", "입력과 연속값 target의 관계를 선형 결합으로 근사합니다.", body)


def _svm():
    left = "".join(
        f'<circle cx="{x}" cy="{210+i*45}" r="12" fill="#2454d8"/>'
        for i, x in enumerate([250,310,360,420])
    )
    right = "".join(
        f'<circle cx="{x}" cy="{200+i*48}" r="12" fill="#08796f"/>'
        for i, x in enumerate([760,820,890,950])
    )
    body = (
        '<path d="M580 135 L580 430" stroke="#203455" stroke-width="4"/>'
        '<path d="M490 135 L490 430 M670 135 L670 430" stroke="#7891b7" '
        'stroke-width="3" stroke-dasharray="10 8"/>'
        + left + right
        + '<text x="580" y="470" text-anchor="middle" class="m">decision boundary</text>'
        + '<text x="520" y="170" class="m">margin</text>'
    )
    return _frame("SVM margin", "결정 경계 주변의 margin을 크게 하도록 분류기를 학습합니다.", body)


def _graphical():
    body = (
        '<circle cx="280" cy="240" r="48" fill="#edf3ff" stroke="#2454d8" stroke-width="3"/>'
        '<circle cx="600" cy="170" r="48" fill="#edf3ff" stroke="#2454d8" stroke-width="3"/>'
        '<circle cx="600" cy="330" r="48" fill="#e5f5f2" stroke="#08796f" stroke-width="3"/>'
        '<circle cx="920" cy="240" r="48" fill="#fff0e5" stroke="#a24d18" stroke-width="3"/>'
        '<text x="280" y="247" text-anchor="middle" class="l">x₁</text>'
        '<text x="600" y="177" text-anchor="middle" class="l">x₂</text>'
        '<text x="600" y="337" text-anchor="middle" class="l">x₃</text>'
        '<text x="920" y="247" text-anchor="middle" class="l">x₄</text>'
        + _arrow(328,235,548,180) + _arrow(328,250,548,320)
        + _arrow(648,180,872,230) + _arrow(648,330,872,250)
    )
    return _frame("Graphical Model", "노드와 간선으로 변수 의존성과 factorization을 표현합니다.", body)


def _gmm():
    body = """<path d="M120 410 H1080" class="thin"/>
<path d="M160 405 C230 400 250 350 300 230 C330 165 365 165 400 230
C450 350 470 400 540 405" stroke="#2454d8" stroke-width="5" fill="none"/>
<path d="M390 405 C460 398 500 350 550 275 C590 215 640 215 680 275
C730 350 770 398 840 405" stroke="#08796f" stroke-width="5" fill="none"/>
<path d="M650 405 C720 398 760 345 820 220 C850 160 900 160 930 220
C990 345 1010 398 1060 405" stroke="#a24d18" stroke-width="5" fill="none"/>
<text x="340" y="180" class="m">component 1</text>
<text x="600" y="245" class="m">component 2</text>
<text x="870" y="180" class="m">component 3</text>"""
    return _frame("Gaussian Mixture Model", "여러 Gaussian component가 데이터 군집을 확률적으로 설명합니다.", body)


SPECS = {
    # pixels
    "pixels-human-vs-array.svg": ("pixels_human_array", "사람이 보는 이미지 vs 컴퓨터 입력", "같은 장면도 모델에는 픽셀 값 배열로 전달됩니다."),
    "pixels-channels.svg": ("pixels_channels", "RGB 채널 분리", "R·G·B는 같은 이미지의 병렬 채널이며 직렬 처리 단계가 아닙니다."),
    "pixels-lighting.svg": ("lighting_visual", "같은 물체, 다른 조명", "물체의 의미는 같아도 픽셀 intensity는 크게 달라질 수 있습니다."),
    "pixels-resize.svg": ("resize_visual", "Resize가 바꾸는 정보", "해상도를 줄이면 작은 패턴이 몇 cell로 축약되거나 사라질 수 있습니다."),
    "pixels-normalization.svg": ("flow", "픽셀 값 전처리 흐름", "학습과 추론에서 같은 전처리 계약을 사용해야 합니다.", [["uint8","0~255"],["float","0.0~1.0"],["표준화","(x-μ)/σ"],["Tensor","모델 입력"],["Model","예측"]]),

    # CNN
    "cnn-sliding.svg": ("flow", "Kernel sliding", "작은 커널이 입력 위를 이동하며 각 위치의 반응을 계산합니다.", [["Input patch","3×3"],["Kernel","3×3"],["Multiply","원소별 곱"],["Sum","+ bias"],["Feature","한 출력값"]]),
    "cnn-stride.svg": ("compare", "Stride 1 vs Stride 2", "Stride는 커널이 한 번에 이동하는 간격입니다.", "Stride = 1", ["촘촘히 이동","공간 해상도 보존","출력 크기 큼"], "Stride = 2", ["두 칸씩 이동","출력 크기 감소","작은 패턴 손실 가능"]),
    "cnn-padding.svg": ("compare", "Padding 없음 vs Same padding", "가장자리 처리 방식이 출력 공간 크기를 바꿉니다.", "Padding = 0", ["경계 바깥 값 없음","출력 공간 감소","가장자리 정보 덜 반영"], "Padding = 1", ["3×3에서 가장자리 1칸 추가","stride 1이면 크기 유지","경계도 동일 횟수 계산"]),
    "cnn-multichannel.svg": ("parallel_conv_channels", "RGB에서 하나의 출력 채널", "하나의 filter가 모든 입력 채널을 병렬로 계산한 뒤 합산합니다."),
    "cnn-featuremaps.svg": ("compare", "Feature map은 무엇에 반응할까?", "각 채널은 서로 다른 패턴에 강하게 반응하도록 학습될 수 있습니다.", "초기 feature", ["수직 경계","수평 경계","밝기 변화"], "깊은 feature", ["텍스처 조합","부품 형태","클래스에 유용한 패턴"]),
    "cnn-receptive.svg": ("flow", "Receptive field 확장", "층이 깊어지면 하나의 출력이 더 넓은 입력 문맥을 보게 됩니다.", [["Layer 1","3×3"],["Layer 2","5×5"],["Layer 3","7×7"],["Deep","더 넓은 문맥"]]),
    "cnn-hierarchy.svg": ("flow", "CNN 특징의 계층적 표현", "초기에는 단순한 패턴, 깊은 층에서는 더 복합적인 조합을 표현합니다.", [["Edge","경계"],["Texture","반복 무늬"],["Part","부분 구조"],["Object cue","객체 단서"]]),
    "cnn-pooling.svg": ("compare", "Max Pooling 전후", "작은 영역에서 대표값만 남겨 공간 크기를 줄입니다.", "입력 2×2", ["1  5","2  3","위치 정보 풍부"], "Max = 5", ["대표값 하나 유지","공간 크기 감소","정확한 위치 일부 손실"]),

    # ViT
    "vit-patches.svg": ("flow", "이미지를 Patch로 바꾸기", "224×224, patch 16이면 14×14=196개의 patch가 생깁니다.", [["Image","224×224×3"],["Grid","14×14"],["Patch","16×16×3"],["196개","sequence"]]),
    "vit-flatten.svg": ("flow", "Patch → Flatten → Embedding", "각 patch를 1차원으로 펼친 뒤 학습 가능한 선형 변환을 적용합니다.", [["16×16×3","patch"],["Flatten","768"],["Linear","W·x+b"],["Embedding","D차원"]]),
    "vit-position.svg": ("compare", "왜 위치 정보가 필요한가?", "Attention 자체는 token의 원래 2차원 위치를 자동으로 알지 못합니다.", "위치 정보 없음", ["토큰 집합처럼 처리","왼쪽/오른쪽 구분 약함","순서 변화에 둔감"], "Position embedding", ["각 patch 위치 코드 추가","공간 순서 전달","사전학습 위치 정보 활용"]),
    "vit-cls.svg": ("flow", "CLS token의 역할", "분류용 추가 token이 여러 encoder 층에서 patch 정보와 상호작용합니다.", [["CLS","초기 학습 벡터"],["Attention","patch와 교환"],["Encoder","여러 층 반복"],["CLS final","이미지 표현"],["Head","class logits"]]),
    "vit-attention.svg": ("attention_qkv", "Self-Attention 계산", "Q·K로 attention weight를 만들고 그 weight로 V를 가중합합니다."),
    "vit-attention-matrix.svg": ("matrix", "Attention score matrix", "각 행은 한 query가 모든 key를 얼마나 참고하는지 나타냅니다."),
    "vit-multihead.svg": ("multihead_parallel", "Multi-Head Attention", "여러 head는 병렬 계산 후 concatenate되어 output projection으로 결합됩니다."),
    "vit-cnn-compare.svg": ("compare", "CNN과 ViT의 정보 혼합 방식", "둘 다 이미지를 학습하지만 기본 연결 방식이 다릅니다.", "CNN", ["작은 지역부터 계산","공유 kernel","깊어지며 문맥 확대"], "ViT", ["patch token으로 변환","attention으로 관계 계산","초기부터 전역 관계 가능"]),

    # tasks
    "tasks-three-way.svg": ("task_three_way", "Classification · Detection · Segmentation", "같은 입력에서 task별 output granularity가 달라집니다."),
    "tasks-segmentation.svg": ("semantic_instance", "Semantic vs Instance Segmentation", "같은 class 객체를 하나의 class mask로 볼지 객체별로 분리할지 비교합니다."),
    "tasks-output-types.svg": ("task_outputs", "Vision task의 출력 형태", "class score, box, mask는 서로 다른 task output이며 직렬 단계가 아닙니다."),
    "tasks-label-box-mask.svg": ("label_granularity", "Label · Box · Mask의 정보량", "annotation granularity와 위치 정밀도 차이를 시각적으로 비교합니다."),

    # training
    "train-split.svg": ("flow", "Train / Validation / Test", "세 집합은 역할이 다르며 test는 최종 평가까지 격리해야 합니다.", [["Train","가중치 학습"],["Validation","모델 선택"],["Threshold","운영 기준"],["Test","최종 일반화"]]),
    "train-leakage.svg": ("train_leakage_visual", "좋은 분할 vs Data leakage", "같은 원본 영상의 near-duplicate frame을 split 사이에 섞지 않습니다."),
    "train-confusion.svg": ("confusion",),
    "train-prf.svg": ("compare", "Precision과 Recall의 관점", "같은 confusion matrix에서 서로 다른 질문을 합니다.", "Precision", ["이상이라고 한 것 중","얼마나 진짜 이상인가?","FP에 민감"], "Recall", ["실제 이상 중","얼마나 놓치지 않았나?","FN에 민감"]),
    "train-threshold.svg": ("threshold_curve", "Threshold를 바꾸면 무엇이 변할까?", "고정된 score에서 threshold를 높이면 positive 판정 수가 줄어 Recall과 false-positive rate가 감소하거나 유지됩니다."),
    "train-curves.svg": ("roc_pr", "ROC curve와 Precision–Recall curve", "두 curve는 threshold sweep에 따른 trade-off를 보여 줍니다."),
    "train-overfit.svg": ("overfit_curve", "Overfitting의 전형적 신호", "train loss는 계속 낮아져도 validation loss가 최저점을 지난 뒤 다시 높아질 수 있습니다."),

    # ResNet
    "resnet-plain-vs.svg": ("resnet_plain_vs", "Plain network vs Residual network", "Residual block은 main branch와 identity shortcut을 합산합니다."),
    "resnet-shortcuts.svg": ("resnet_shortcuts", "Identity vs Projection shortcut", "두 branch shape가 다르면 projection으로 맞춘 뒤 element-wise add합니다."),
    "resnet-gradient.svg": ("residual_gradient", "Residual 경로의 gradient 흐름", "shortcut은 backward derivative에도 identity term을 제공합니다."),
    "resnet-function.svg": ("residual_function", "Residual learning", "F(x)를 학습한 뒤 identity x를 합산해 H(x)를 만듭니다."),

    # U-Net
    "unet-pyramid.svg": ("flow", "U-Net의 해상도 피라미드", "Encoder에서 공간을 줄이고 Decoder에서 다시 복원합니다.", [["256²","64ch"],["128²","128ch"],["64²","256ch"],["128²","128ch"],["256²","classes"]]),
    "unet-skip-why.svg": ("compare", "왜 Skip connection이 필요한가?", "깊은 특징의 문맥과 얕은 특징의 위치 정보를 함께 사용합니다.", "Encoder deep", ["넓은 문맥","의미 정보 풍부","공간 세부 감소"], "Skip feature", ["높은 해상도","경계/위치 정보","Decoder에 직접 전달"]),
    "unet-mask-triplet.svg": ("mask_compare", "Segmentation 결과 비교", "GT와 prediction을 같은 입력 기준으로 나란히 비교해 오류 위치를 확인합니다."),
    "unet-pixel-class.svg": ("flow", "Pixel-wise classification", "각 픽셀 위치에서 클래스별 logit을 만들고 mask로 변환합니다.", [["Feature","H×W×C"],["1×1 Conv","K logits"],["Softmax","class score"],["Argmax","mask"]]),

    # PatchCore
    "patchcore-normal-only.svg": ("flow", "PatchCore는 정상 데이터로 기준 공간을 만든다", "정상 특징을 저장하고 검사 특징이 얼마나 멀리 떨어졌는지 봅니다.", [["Normal","train images"],["Backbone","features"],["Memory","normal bank"],["Test","query"],["Distance","anomaly"]]),
    "patchcore-features.svg": ("flow", "RGB patch가 아니라 CNN feature patch", "PatchCore의 patch는 feature map의 지역 표현입니다.", [["Image","RGB"],["CNN","mid-level map"],["Local feature","descriptor"],["Bank","store"]]),
    "patchcore-coreset.svg": ("compare", "전체 Memory bank vs Coreset", "대표 특징만 선택해 검색 비용과 메모리를 줄입니다.", "전체 bank", ["특징 수 매우 큼","중복 normal 많음","검색 비용 큼"], "Coreset", ["대표점 선택","다양성 유지 목표","메모리/검색 절감"]),
    "patchcore-nearest.svg": ("flow", "Nearest neighbor anomaly score", "검사 특징마다 가장 가까운 정상 특징과의 거리를 구합니다.", [["Query fᵢ","검사 patch"],["Search","normal bank"],["Nearest m","가장 가까움"],["‖fᵢ-m‖","distance"],["Score","anomaly"]]),
    "patchcore-heatmap.svg": ("flow", "Patch score를 공간으로 되돌리기", "지역 점수를 원래 위치에 배치하고 업샘플링해 anomaly map을 만듭니다.", [["Patch scores","저해상도"],["Grid","위치 복원"],["Upsample","입력 크기"],["Heatmap","이상 위치"]]),
    "patchcore-distance.svg": ("compare", "정상과 가까운 특징 vs 먼 특징", "절대 거리의 의미는 backbone·전처리·데이터에 따라 달라집니다.", "Normal-like", ["가까운 이웃 존재","거리 작음","anomaly score 낮음"], "Abnormal-like", ["normal bank와 멂","거리 큼","anomaly score 높음"]),

    # CS231n
    "cs-knn.svg": ("flow", "k-Nearest Neighbors", "새 샘플과 학습 샘플의 거리를 직접 비교합니다.", [["Query","새 이미지"],["Distance","모든 train"],["Top k","가까운 샘플"],["Vote","class"]]),
    "cs-linear.svg": ("flow", "Linear classifier", "입력 벡터를 가중치 행렬과 곱해 클래스별 score를 만듭니다.", [["x","D features"],["W","K×D"],["Wx+b","scores"],["Argmax","class"]]),
    "cs-softmax.svg": ("flow", "Score → Softmax → Cross-Entropy", "원시 score를 확률 형태로 바꾸고 정답 확률에 loss를 줍니다.", [["Logits","2,1,-1"],["exp","양수화"],["Normalize","sum=1"],["p(y)","정답 확률"],["Loss","-log p(y)"]]),
    "cs-backprop.svg": ("flow", "Backpropagation 계산 그래프", "forward에서 값을 만들고 backward에서 chain rule로 gradient를 전달합니다.", [["Input","x"],["Layer","z=f(x)"],["Loss","L(z)"],["∂L/∂z","local"],["∂L/∂x","chain rule"]]),
    "cs-optimization.svg": ("optimization_curve", "Optimization에서 loss가 줄어드는 과정", "각 update가 parameter를 바꾸며 objective loss를 낮추는 기본 흐름을 보여줍니다."),
    "cs-augmentation.svg": ("compare", "원본과 Augmentation", "라벨 의미를 유지하는 범위에서 입력 변화를 만들어 일반화를 돕습니다.", "Original", ["고정 조명/위치","데이터 다양성 제한","과적합 가능"], "Augmented", ["crop/flip/color 등","입력 분포 다양화","task 의미 보존 필요"]),
    "cs-transfer.svg": ("flow", "Transfer Learning 전략", "사전학습 특징을 그대로 쓰거나 일부·전체를 미세조정할 수 있습니다.", [["Pretrained","backbone"],["Freeze","feature extractor"],["Replace head","new task"],["Fine-tune","필요 층"],["Validate","generalization"]]),
    "cs-modern-map.svg": ("flow", "현대 Vision 학습 흐름", "CNN 이후 Transformer·self-supervised·vision-language·diffusion으로 확장됩니다.", [["CNN","local features"],["ViT","attention"],["SSL","unlabeled"],["CLIP/DINO","representation"],["Diffusion","generation"]]),

    # PRML
    "prml-gaussian.svg": ("gaussian",),
    "prml-beta.svg": ("compare", "Prior에서 Posterior로", "관측 전 믿음과 데이터를 결합해 분포가 갱신됩니다.", "Prior Beta(2,2)", ["중앙에 완만","사전 정보 약함","관측 전"], "Posterior Beta(5,9)", ["3 success / 7 failure","평균 5/14","관측 후 갱신"]),
    "prml-regression.svg": ("regression",),
    "prml-logistic.svg": ("compare", "Logistic regression decision boundary", "선형 score를 sigmoid에 통과시켜 두 클래스 확률로 해석합니다.", "Class 0", ["경계 한쪽 점들","p(C1|x) 낮음","score 음수 쪽"], "Class 1", ["경계 반대쪽 점들","p(C1|x) 높음","score 양수 쪽"]),
    "prml-neuralnet.svg": ("flow", "Neural network의 기본 계산", "선형 결합과 비선형 함수를 여러 층 반복합니다.", [["Input","x"],["Weighted sum","Wx+b"],["Activation","h(a)"],["Hidden","z"],["Output","y"]]),
    "prml-kernel.svg": ("compare", "Kernel trick의 직관", "원 공간에서 선형 분리가 어려워도 더 풍부한 특징 공간에서는 가능할 수 있습니다.", "Input space", ["비선형 경계 필요","두 class가 얽힘","직접 선형분리 어려움"], "Feature space φ(x)", ["kernel로 내적 계산","선형 경계 가능","고차원 좌표 직접 생성 불필요"]),
    "prml-svm.svg": ("svm",),
    "prml-graphical.svg": ("graphical",),
    "prml-gmm.svg": ("gmm",),
    "prml-variational.svg": ("vi_visual", "Variational Inference", "다루기 쉬운 q(z;φ)를 선택하고 ELBO를 최적화해 posterior를 근사합니다."),
    "prml-sampling.svg": ("flow", "Monte Carlo sampling", "분포에서 여러 샘플을 뽑아 기대값이나 posterior 특성을 근사합니다.", [["Target p(x)","분포"],["Sample","x¹,x²,…"],["Evaluate","f(xⁿ)"],["Average","1/N Σ"],["Estimate","expectation"]]),
    "prml-pca.svg": ("compare", "PCA가 찾는 방향", "데이터 분산이 큰 축을 찾아 저차원 좌표로 투영합니다.", "원 좌표", ["x₁, x₂ 축","점들이 대각선으로 퍼짐","상관 존재"], "주성분 좌표", ["PC1 = 큰 분산 방향","PC2 = 작은 분산 방향","상위 축만 남겨 축소 가능"]),
    "prml-ensemble.svg": ("ensemble_parallel", "Ensemble / Mixture of Experts", "여러 predictor는 병렬로 계산되고 평균 또는 gating weight로 결합됩니다."),
}



def _pixels_human_array():
    """Contrast semantic perception with the numeric tensor given to a model."""
    body = [
        '<rect x="70" y="145" width="430" height="300" rx="20" fill="#fff" stroke="#b9c9e7" stroke-width="3"/>',
        '<rect x="700" y="145" width="430" height="300" rx="20" fill="#fff" stroke="#8ac7a5" stroke-width="3"/>',
        '<text x="285" y="190" text-anchor="middle" class="l">사람: 사과로 인식</text>',
        '<circle cx="285" cy="315" r="72" fill="#e85b48"/>',
        '<path d="M282 245 C281 222 298 207 316 198" stroke="#6d7f45" stroke-width="10" fill="none"/>',
        '<ellipse cx="336" cy="205" rx="27" ry="13" fill="#6da76f" transform="rotate(-25 336 205)"/>',
        '<text x="285" y="415" text-anchor="middle" class="m">모양·색·문맥을 함께 해석</text>',
        '<text x="915" y="190" text-anchor="middle" class="l">컴퓨터: H×W×C 숫자</text>',
    ]
    vals = [
        [18,28,35,42,20],
        [24,96,172,118,31],
        [28,148,228,164,34],
        [22,110,190,132,29],
        [17,30,42,33,18],
    ]
    start_x,start_y,cell=820,215,37
    for r,row in enumerate(vals):
        for col,v in enumerate(row):
            shade=max(0,min(255,245-v//2))
            body.append(
                f'<rect x="{start_x+col*cell}" y="{start_y+r*cell}" width="42" height="42" rx="5" '
                f'fill="rgb({shade},{shade},{shade})" stroke="#c7d5ee"/>'
            )
            body.append(
                f'<text x="{start_x+col*cell+21}" y="{start_y+r*cell+27}" text-anchor="middle" '
                f'font-size="13" fill="#203455">{v}</text>'
            )
    body.append('<text x="915" y="430" text-anchor="middle" class="m">조명·노이즈가 바뀌면 숫자도 바뀜</text>')
    body.append(_arrow(505,295,680,295))
    return _frame("사람이 보는 이미지 vs 컴퓨터 입력", "같은 장면도 모델에는 픽셀 값으로 전달됩니다.", "".join(body))


def _pixels_channels():
    """RGB channels split in parallel, not serially."""
    body = [
        _card(70, 200, 175, 110, "원본", "H×W×3"),
        '<circle cx="330" cy="255" r="32" fill="#edf3ff" stroke="#7891b7" stroke-width="3"/>',
        '<text x="330" y="262" text-anchor="middle" class="l">분리</text>',
    ]
    body.append(_arrow(245,255,296,255))
    channel_y=[145,235,325]
    colors=[("#fde8e8","#b64040","R"),("#e9f7f2","#08796f","G"),("#e8eefc","#2454d8","B")]
    for yy,(fill,stroke,label) in zip(channel_y,colors):
        body.append(f'<rect x="430" y="{yy}" width="180" height="72" rx="13" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        body.append(f'<text x="520" y="{yy+31}" text-anchor="middle" class="l">{label} channel</text>')
        body.append(f'<text x="520" y="{yy+55}" text-anchor="middle" class="m">H×W</text>')
        body.append(_arrow(362,255,424,yy+36))
    body += [
        '<circle cx="730" cy="255" r="34" fill="#fff7e9" stroke="#d79b66" stroke-width="3"/>',
        '<text x="730" y="262" text-anchor="middle" class="l">결합</text>',
        _card(865, 200, 210, 110, "RGB image", "H×W×3", True),
    ]
    for yy in channel_y:
        body.append(_arrow(610,yy+36,696,255))
    body.append(_arrow(764,255,860,255))
    return _frame("RGB 채널 분리와 결합", "R·G·B는 직렬 단계가 아니라 같은 이미지의 병렬 채널입니다.", "".join(body))


def _lighting_visual():
    """Same object with shifted pixel intensities under different illumination."""
    body = []
    for x0,title,base in [(95,"밝은 조명",210),(665,"어두운 조명",75)]:
        body.append(f'<rect x="{x0}" y="145" width="440" height="300" rx="20" fill="#fff" stroke="#c7d5ee" stroke-width="3"/>')
        body.append(f'<text x="{x0+220}" y="190" text-anchor="middle" class="l">{title}</text>')
        vals=[
            [base,base+8,base+4,base+10],
            [base-18,base-65,base-78,base-12],
            [base-10,base-82,base-95,base-18],
            [base+3,base-20,base-15,base+5],
        ]
        sx=x0+95; sy=220; cell=56
        for r,row in enumerate(vals):
            for col,v in enumerate(row):
                v=max(0,min(255,v))
                shade=v
                body.append(f'<rect x="{sx+col*cell}" y="{sy+r*cell}" width="50" height="50" rx="6" fill="rgb({shade},{shade},{shade})" stroke="#d6deea"/>')
                body.append(f'<text x="{sx+col*cell+25}" y="{sy+r*cell+31}" text-anchor="middle" font-size="13" fill="{"#fff" if v<130 else "#203455"}">{v}</text>')
    body.append('<text x="600" y="475" text-anchor="middle" class="m">객체의 의미는 같아도 intensity distribution은 크게 이동할 수 있음</text>')
    return _frame("같은 물체, 다른 조명", "조명 변화는 그대로 픽셀 값 변화로 전달됩니다.", "".join(body))


def _resize_visual():
    """Show loss of a small structure after aggressive downsampling."""
    body = [
        '<text x="285" y="155" text-anchor="middle" class="l">1920×1080 개념</text>',
        '<text x="915" y="155" text-anchor="middle" class="l">224×224 개념</text>',
    ]
    def grid(x0,y0,rows,cols,cell,hot):
        out=[]
        for r in range(rows):
            for cc in range(cols):
                idx=r*cols+cc
                fill="#2454d8" if idx in hot else "#edf3ff"
                out.append(f'<rect x="{x0+cc*cell}" y="{y0+r*cell}" width="{cell-3}" height="{cell-3}" rx="3" fill="{fill}" stroke="#c7d5ee"/>')
        return "".join(out)
    body.append(grid(115,185,7,10,34,{24,25,34,35,36,44,45}))
    body.append(_arrow(510,300,680,300))
    body.append(grid(795,220,4,6,45,{8,14}))
    body += [
        '<text x="285" y="455" text-anchor="middle" class="m">작은 구조가 여러 픽셀로 남음</text>',
        '<text x="915" y="455" text-anchor="middle" class="m">축소 후 작은 구조가 1–2 cell로 줄거나 사라질 수 있음</text>',
    ]
    return _frame("Resize가 바꾸는 정보", "해상도 축소는 계산량을 줄이지만 작은 패턴의 표현력을 낮출 수 있습니다.", "".join(body))


def _parallel_conv_channels():
    body = [_card(55,200,150,110,"RGB input","C_in=3")]
    ys=[145,235,325]
    labels=["R × K_R","G × K_G","B × K_B"]
    for yy,label in zip(ys,labels):
        body.append(_card(300,yy,190,72,label,"3×3"))
        body.append(_arrow(205,255,294,yy+36))
    body += [
        '<circle cx="650" cy="255" r="42" fill="#e9f7f2" stroke="#08796f" stroke-width="3"/>',
        '<text x="650" y="250" text-anchor="middle" class="l">Σ</text>',
        '<text x="650" y="276" text-anchor="middle" class="m">+ bias</text>',
        _card(820,200,260,110,"Output feature map","one filter → one channel",True),
    ]
    for yy in ys:
        body.append(_arrow(490,yy+36,606,255))
    body.append(_arrow(694,255,815,255))
    return _frame("RGB에서 하나의 출력 채널", "한 convolution filter는 모든 입력 채널을 동시에 보고 결과를 합산합니다.", "".join(body))


def _attention_qkv_visual():
    body=[_card(55,200,140,110,"Input X","tokens")]
    ys=[135,235,335]
    labels=[("Q=XW_Q","query"),("K=XW_K","key"),("V=XW_V","value")]
    for yy,(name,sub) in zip(ys,labels):
        body.append(_card(285,yy,180,72,name,sub))
        body.append(_arrow(195,255,278,yy+36))
    body += [
        _card(555,165,220,90,"QKᵀ / √d_k","pairwise scores"),
        _card(555,300,220,90,"Softmax","attention weights"),
        _card(865,215,235,110,"A · V","weighted value sum",True),
    ]
    body.append(_arrow(465,171,550,205))
    body.append(_arrow(465,271,550,205))
    body.append(_arrow(665,255,665,294))
    body.append(_arrow(775,345,860,285))
    body.append(_arrow(465,371,860,285))
    return _frame("Self-Attention 계산", "Q와 K로 attention weight를 만들고, 그 weight로 V를 가중합합니다.", "".join(body))


def _multihead_visual():
    body=[_card(55,205,150,105,"Input X","tokens")]
    ys=[135,235,335]
    colors=["#edf3ff","#e9f7f2","#fff1e7"]
    for i,(yy,fill) in enumerate(zip(ys,colors),1):
        body.append(f'<rect x="320" y="{yy}" width="210" height="72" rx="13" fill="{fill}" stroke="#9aabc7" stroke-width="2"/>')
        body.append(f'<text x="425" y="{yy+31}" text-anchor="middle" class="l">Head {i}</text>')
        body.append(f'<text x="425" y="{yy+55}" text-anchor="middle" class="m">own Q/K/V projection</text>')
        body.append(_arrow(205,257,314,yy+36))
    body += [
        _card(675,205,175,105,"Concat","parallel heads"),
        _card(950,205,170,105,"W_O","project output",True),
    ]
    for yy in ys:
        body.append(_arrow(530,yy+36,670,257))
    body.append(_arrow(850,257,945,257))
    return _frame("Multi-Head Attention", "여러 head는 순차가 아니라 병렬로 계산된 뒤 concatenate됩니다.", "".join(body))


def _task_three_way_visual():
    body=[]
    panels=[(55,"Classification"),(420,"Detection"),(785,"Segmentation")]
    for x0,title in panels:
        body.append(f'<rect x="{x0}" y="145" width="310" height="300" rx="20" fill="#fff" stroke="#c7d5ee" stroke-width="3"/>')
        body.append(f'<text x="{x0+155}" y="190" text-anchor="middle" class="l">{title}</text>')
        body.append(f'<rect x="{x0+75}" y="220" width="160" height="150" rx="12" fill="#edf2f7" stroke="#d6deea"/>')
        body.append(f'<circle cx="{x0+155}" cy="295" r="48" fill="#e0ae82"/>')
    body += [
        '<rect x="120" y="382" width="180" height="38" rx="8" fill="#2454d8"/><text x="210" y="407" text-anchor="middle" fill="#fff" font-size="16">class: object</text>',
        '<rect x="515" y="245" width="125" height="105" fill="none" stroke="#2454d8" stroke-width="5"/><text x="575" y="407" text-anchor="middle" class="m">class + box</text>',
        '<path d="M860 337 C835 300 850 252 930 248 C1010 245 1020 320 972 350 C930 376 885 365 860 337" fill="#2454d8" opacity=".35"/><text x="940" y="407" text-anchor="middle" class="m">pixel mask</text>',
    ]
    return _frame("Classification · Detection · Segmentation", "세 task는 같은 입력을 보더라도 요구하는 출력 구조가 다릅니다.", "".join(body))


def _semantic_instance_visual():
    body=[]
    for x0,title in [(90,"Semantic"),(650,"Instance")]:
        body.append(f'<rect x="{x0}" y="145" width="460" height="300" rx="20" fill="#fff" stroke="#c7d5ee" stroke-width="3"/>')
        body.append(f'<text x="{x0+230}" y="190" text-anchor="middle" class="l">{title}</text>')
        body.append(f'<rect x="{x0+70}" y="220" width="320" height="160" rx="12" fill="#eef2f6" stroke="#d6deea"/>')
    # same class objects have same color in semantic
    body += [
        '<ellipse cx="275" cy="295" rx="75" ry="52" fill="#2454d8" opacity=".48"/>',
        '<ellipse cx="390" cy="300" rx="75" ry="52" fill="#2454d8" opacity=".48"/>',
        '<ellipse cx="835" cy="295" rx="75" ry="52" fill="#2454d8" opacity=".48"/>',
        '<ellipse cx="950" cy="300" rx="75" ry="52" fill="#08796f" opacity=".48"/>',
        '<text x="320" y="414" text-anchor="middle" class="m">같은 class → 같은 pixel label</text>',
        '<text x="880" y="414" text-anchor="middle" class="m">같은 class라도 object ID를 분리</text>',
    ]
    return _frame("Semantic vs Instance Segmentation", "Semantic은 class 단위, instance는 객체 단위로 mask를 구분합니다.", "".join(body))


def _task_outputs_visual():
    body=[_card(55,205,150,105,"Image","input")]
    targets=[(360,125,"Class scores","K"),(360,235,"Boxes","N×4 + score"),(360,345,"Masks","H×W or N masks")]
    for x0,y0,title,sub in targets:
        body.append(_card(x0,y0,230,72,title,sub))
        body.append(_arrow(205,257,x0-5,y0+36))
    body.append(_card(835,205,240,105,"Task-specific decision","postprocess / metric",True))
    for _,y0,_,_ in targets:
        body.append(_arrow(590,y0+36,830,257))
    return _frame("Vision task의 출력 형태", "Class, box, mask는 순차 단계가 아니라 서로 다른 task가 요구하는 출력입니다.", "".join(body))


def _label_granularity_visual():
    body=[]
    panels=[(60,"Class label","무엇인가"),(420,"Bounding box","어디쯤"),(780,"Pixel mask","정확히 어느 픽셀")]
    for x0,title,sub in panels:
        body.append(f'<rect x="{x0}" y="145" width="300" height="300" rx="20" fill="#fff" stroke="#c7d5ee" stroke-width="3"/>')
        body.append(f'<text x="{x0+150}" y="190" text-anchor="middle" class="l">{title}</text>')
        body.append(f'<text x="{x0+150}" y="218" text-anchor="middle" class="m">{sub}</text>')
        body.append(f'<rect x="{x0+70}" y="245" width="160" height="130" rx="10" fill="#edf2f7" stroke="#d6deea"/>')
        body.append(f'<circle cx="{x0+150}" cy="310" r="42" fill="#e0ae82"/>')
    body += [
        '<text x="210" y="410" text-anchor="middle" class="m">annotation cost 낮음</text>',
        '<rect x="485" y="265" width="130" height="95" fill="none" stroke="#2454d8" stroke-width="5"/>',
        '<path d="M850 341 C830 300 850 270 925 268 C1000 265 1010 330 970 352 C920 380 875 370 850 341" fill="#2454d8" opacity=".38"/>',
        '<text x="930" y="410" text-anchor="middle" class="m">annotation cost 높음 · 위치 정밀도 높음</text>',
    ]
    return _frame("Label · Box · Mask의 정보량", "세 annotation은 서로 다른 supervision granularity를 제공합니다.", "".join(body))


def _mask_compare_visual():
    body=[
        _card(50,205,170,105,"Input image","same sample"),
        _card(360,135,205,90,"GT mask","ground truth"),
        _card(360,315,205,90,"Pred mask","model output"),
        _card(850,205,240,105,"Overlay / difference","error localization",True),
    ]
    body.append(_arrow(220,257,354,180))
    body.append(_arrow(220,257,354,360))
    body.append(_arrow(565,180,845,245))
    body.append(_arrow(565,360,845,275))
    # tiny mask previews
    body += [
        '<rect x="620" y="132" width="110" height="96" rx="8" fill="#eef2f6" stroke="#d6deea"/>',
        '<circle cx="675" cy="180" r="30" fill="#2454d8" opacity=".45"/>',
        '<rect x="620" y="312" width="110" height="96" rx="8" fill="#eef2f6" stroke="#d6deea"/>',
        '<circle cx="683" cy="355" r="30" fill="#2454d8" opacity=".45"/>',
    ]
    return _frame("Segmentation 결과 비교", "GT와 prediction은 직렬 단계가 아니라 같은 입력에 대한 두 mask를 나란히 비교합니다.", "".join(body))


def _roc_pr_visual():
    body=[]
    panels=[(70,"ROC","FPR","TPR"),(650,"Precision–Recall","Recall","Precision")]
    for x0,title,xlab,ylab in panels:
        body.append(f'<rect x="{x0}" y="135" width="480" height="330" rx="20" fill="#fff" stroke="#c7d5ee" stroke-width="3"/>')
        body.append(f'<text x="{x0+240}" y="180" text-anchor="middle" class="l">{title}</text>')
        body.append(f'<path d="M{x0+75} 400 H{x0+420} M{x0+75} 400 V220" class="thin"/>')
        body.append(f'<text x="{x0+245}" y="438" text-anchor="middle" class="m">{xlab}</text>')
        body.append(f'<text x="{x0+45}" y="235" text-anchor="middle" class="m">{ylab}</text>')
    body += [
        '<path d="M145 390 C170 310 225 255 305 235 C380 215 440 212 490 210" stroke="#2454d8" stroke-width="6" fill="none"/>',
        '<path d="M145 400 L490 220" stroke="#a8b5c8" stroke-width="3" stroke-dasharray="8 6"/>',
        '<path d="M725 248 L780 242 L830 270 L875 260 L925 305 L970 292 L1020 352 L1070 338" stroke="#08796f" stroke-width="6" fill="none"/>',
        '<text x="310" y="320" text-anchor="middle" class="m">threshold sweep</text>',
        '<text x="890" y="210" text-anchor="middle" class="m">schematic: precision은 recall에 대해 단조일 필요가 없음</text>',
    ]
    return _frame("ROC curve와 Precision–Recall curve", "두 curve 모두 threshold를 바꾸며 얻는 성능 trade-off를 보여줍니다.", "".join(body))


def _train_leakage_visual():
    """Contrast frame-random leakage with group-preserving assignment."""
    body=[
        '<text x="300" y="145" text-anchor="middle" class="l">나쁜 예: frame random split</text>',
        '<text x="900" y="145" text-anchor="middle" class="l">좋은 예: grouped split</text>',
    ]
    colors=["#8faee8","#8ccdbb","#e0ae82","#b8a6d9"]
    labels=["video A","video B","video C","video D"]
    random_tags=["Tr","V","Tr","Te","V","Tr"]
    split_x={"Tr":650,"V":835,"Te":1020}
    grouped_assignment=["Tr","Tr","V","Te"]

    for i,(color,label) in enumerate(zip(colors,labels)):
        y=190+i*58
        body.append(f'<text x="70" y="{y+24}" class="m">{label}</text>')

        # Same source video is randomly scattered across train/val/test.
        for j,tag in enumerate(random_tags):
            x=150+j*58
            body.append(
                f'<rect x="{x}" y="{y}" width="46" height="38" rx="5" '
                f'fill="{color}" opacity="{0.58+0.06*j}" stroke="#ffffff" stroke-width="2"/>'
            )
            body.append(
                f'<text x="{x+23}" y="{y+25}" text-anchor="middle" '
                f'font-size="12" font-weight="700" fill="#203455">{tag}</text>'
            )

        # All frames from one video are kept in exactly one split.
        tag=grouped_assignment[i]
        x0=split_x[tag]
        for j in range(4):
            x=x0+j*27
            body.append(
                f'<rect x="{x}" y="{y}" width="22" height="38" rx="4" '
                f'fill="{color}" opacity="{0.68+0.06*j}"/>'
            )

    body += [
        '<text x="300" y="460" text-anchor="middle" class="m">한 원본의 near-duplicate가 Train/Val/Test에 동시에 들어갈 수 있음</text>',
        '<text x="700" y="460" text-anchor="middle" class="m">Train</text>',
        '<text x="885" y="460" text-anchor="middle" class="m">Val</text>',
        '<text x="1070" y="460" text-anchor="middle" class="m">Test</text>',
    ]
    return _frame("좋은 분할 vs Data leakage", "영상·burst 데이터는 원본 그룹 전체를 하나의 split에 배정해야 누수를 줄일 수 있습니다.", "".join(body))

def _resnet_plain_vs_visual():
    body=[
        '<text x="300" y="150" text-anchor="middle" class="l">Plain block</text>',
        '<text x="900" y="150" text-anchor="middle" class="l">Residual block</text>',
        _card(80,220,120,80,"x","input"),
        _card(245,220,145,80,"F₁","conv"),
        _card(435,220,120,80,"H(x)","output"),
        _arrow(200,260,240,260),
        _arrow(390,260,430,260),
        _card(650,220,120,80,"x","input"),
        _card(815,220,145,80,"F(x)","residual"),
        '<circle cx="1030" cy="260" r="34" fill="#e9f7f2" stroke="#08796f" stroke-width="3"/>',
        '<text x="1030" y="268" text-anchor="middle" class="l">+</text>',
        _arrow(770,260,810,260),
        _arrow(960,260,994,260),
        '<path d="M710 218 C785 160 945 160 1030 224" stroke="#08796f" stroke-width="5" fill="none"/>',
        '<polygon points="1030,224 1014,209 1038,209" fill="#08796f"/>',
        '<text x="870" y="205" text-anchor="middle" class="m">identity shortcut x</text>',
        '<text x="300" y="385" text-anchor="middle" class="m">H(x)를 직접 근사</text>',
        '<text x="900" y="385" text-anchor="middle" class="m">H(x)=F(x)+x</text>',
    ]
    return _frame("Plain network vs Residual network", "Residual block은 main branch와 identity shortcut을 합산합니다.", "".join(body))


def _resnet_shortcuts_visual():
    body=[]
    for x0,title in [(65,"Identity shortcut"),(635,"Projection shortcut")]:
        body.append(f'<rect x="{x0}" y="145" width="500" height="300" rx="20" fill="#fff" stroke="#c7d5ee" stroke-width="3"/>')
        body.append(f'<text x="{x0+250}" y="190" text-anchor="middle" class="l">{title}</text>')
    body += [
        _card(110,245,120,80,"x","64×56×56"),
        _card(330,245,140,80,"F(x)","same shape"),
        '<circle cx="510" cy="285" r="28" fill="#e9f7f2" stroke="#08796f" stroke-width="3"/><text x="510" y="293" text-anchor="middle" class="l">+</text>',
        _arrow(230,285,325,285), _arrow(470,285,480,285),
        '<path d="M170 242 C220 205 425 205 510 255" stroke="#08796f" stroke-width="4" fill="none"/>',
        _card(680,245,120,80,"x","64×56×56"),
        _card(865,205,150,72,"F(x)","128×28×28"),
        _card(865,315,150,72,"1×1, s=2","projection"),
        '<circle cx="1080" cy="285" r="28" fill="#e9f7f2" stroke="#08796f" stroke-width="3"/><text x="1080" y="293" text-anchor="middle" class="l">+</text>',
        _arrow(800,285,858,241), _arrow(800,285,858,351), _arrow(1015,241,1050,275), _arrow(1015,351,1050,295),
        '<text x="315" y="405" text-anchor="middle" class="m">shape가 같으면 parameter-free identity</text>',
        '<text x="885" y="420" text-anchor="middle" class="m">shape가 다르면 projection으로 맞춘 뒤 add</text>',
    ]
    return _frame("Identity vs Projection shortcut", "element-wise add를 위해 두 branch의 output shape가 같아야 합니다.", "".join(body))


def _residual_function_visual():
    body=[
        _card(55,205,145,100,"x","input"),
        _card(340,150,190,90,"F(x)","learned residual"),
        '<circle cx="700" cy="255" r="38" fill="#e9f7f2" stroke="#08796f" stroke-width="3"/>',
        '<text x="700" y="263" text-anchor="middle" class="l">+</text>',
        _card(900,205,190,100,"H(x)","F(x)+x",True),
        _arrow(200,255,334,195),
        _arrow(530,195,662,242),
        _arrow(738,255,895,255),
        '<path d="M126 202 C210 115 590 115 700 217" stroke="#08796f" stroke-width="5" fill="none"/>',
        '<polygon points="700,217 683,202 708,201" fill="#08796f"/>',
        '<text x="420" y="125" text-anchor="middle" class="m">identity path carries x directly</text>',
    ]
    return _frame("Residual learning", "블록은 전체 mapping을 직렬로 만드는 대신 F(x)를 학습하고 x를 더합니다.", "".join(body))


def _residual_gradient_visual():
    body=[
        '<text x="600" y="135" text-anchor="middle" class="l">backward gradient has two routes</text>',
        _card(80,220,150,90,"Input x",""),
        _card(420,220,170,90,"F(x)","main branch"),
        '<circle cx="760" cy="265" r="36" fill="#e9f7f2" stroke="#08796f" stroke-width="3"/>',
        '<text x="760" y="273" text-anchor="middle" class="l">+</text>',
        _card(950,220,160,90,"H(x)","output",True),
        _arrow(230,265,414,265), _arrow(590,265,722,265), _arrow(798,265,945,265),
        '<path d="M155 218 C260 140 650 140 760 229" stroke="#08796f" stroke-width="5" fill="none"/>',
        '<polygon points="760,229 742,214 768,213" fill="#08796f"/>',
        '<path d="M950 340 C760 435 410 435 230 345" stroke="#a24d18" stroke-width="4" fill="none"/>',
        '<polygon points="230,345 248,341 240,359" fill="#a24d18"/>',
        '<text x="600" y="455" text-anchor="middle" class="m">∂H/∂x = I + ∂F/∂x : identity term provides a direct component</text>',
    ]
    return _frame("Residual 경로의 gradient 흐름", "Shortcut은 forward signal뿐 아니라 backward derivative에도 직접 항을 만듭니다.", "".join(body))


def _vi_visual():
    body=[
        _card(55,205,190,100,"log p(x,z)","model / joint"),
        _card(350,205,190,100,"q(z;φ)","chosen family"),
        _card(650,205,190,100,"maximize ELBO","optimize φ",True),
        _card(950,205,190,100,"q*(z)","posterior approximation"),
        _arrow(245,255,345,255), _arrow(540,255,645,255), _arrow(840,255,945,255),
        '<text x="600" y="380" text-anchor="middle" class="m">p(z|x)는 conceptual target이며 일반적으로 직접 계산할 수 없음</text>',
        '<text x="600" y="420" text-anchor="middle" class="m">ELBO를 최적화하면 선택한 q family 안에서 posterior에 가까운 근사를 찾음</text>',
    ]
    return _frame("Variational Inference", "다루기 쉬운 q(z;φ)를 정하고 ELBO를 통해 posterior를 근사합니다.", "".join(body))


def _ensemble_visual():
    body=[_card(50,205,140,100,"Input x","")]
    ys=[135,235,335]
    for i,yy in enumerate(ys, start=1):
        body.append(_card(315,yy,170,72,f"Model {chr(64+i)}","prediction"))
        body.append(_arrow(190,255,309,yy+36))
    body += [
        _card(660,205,210,100,"Combine","average / weights"),
        _card(970,205,170,100,"Output","final",True),
    ]
    for yy in ys:
        body.append(_arrow(485,yy+36,654,255))
    body.append(_arrow(870,255,965,255))
    body.append('<text x="600" y="435" text-anchor="middle" class="m">ensemble: fixed/equal averaging · MoE: input-dependent gating weights</text>')
    return _frame("Ensemble / Mixture of Experts", "여러 predictor는 병렬로 계산되고 마지막에 결합됩니다.", "".join(body))

def _render(spec):
    kind = spec[0]
    if kind == "pixels_human_array":
        return _pixels_human_array()
    if kind == "pixels_channels":
        return _pixels_channels()
    if kind == "lighting_visual":
        return _lighting_visual()
    if kind == "resize_visual":
        return _resize_visual()
    if kind == "parallel_conv_channels":
        return _parallel_conv_channels()
    if kind == "attention_qkv":
        return _attention_qkv_visual()
    if kind == "multihead_parallel":
        return _multihead_visual()
    if kind == "task_three_way":
        return _task_three_way_visual()
    if kind == "semantic_instance":
        return _semantic_instance_visual()
    if kind == "task_outputs":
        return _task_outputs_visual()
    if kind == "label_granularity":
        return _label_granularity_visual()
    if kind == "mask_compare":
        return _mask_compare_visual()
    if kind == "roc_pr":
        return _roc_pr_visual()
    if kind == "train_leakage_visual":
        return _train_leakage_visual()
    if kind == "resnet_plain_vs":
        return _resnet_plain_vs_visual()
    if kind == "resnet_shortcuts":
        return _resnet_shortcuts_visual()
    if kind == "residual_function":
        return _residual_function_visual()
    if kind == "residual_gradient":
        return _residual_gradient_visual()
    if kind == "vi_visual":
        return _vi_visual()
    if kind == "ensemble_parallel":
        return _ensemble_visual()
    if kind == "flow":
        return _flow(spec[1], spec[2], spec[3])
    if kind == "compare":
        return _compare(*spec[1:])
    if kind == "matrix":
        return _matrix(spec[1], spec[2])
    if kind == "curve":
        return _curve(spec[1], spec[2], spec[3])
    if kind == "optimization_curve":
        return _optimization_curve(spec[1], spec[2])
    if kind == "overfit_curve":
        return _overfit_curve(spec[1], spec[2])
    if kind == "threshold_curve":
        return _threshold_curve(spec[1], spec[2])
    if kind == "confusion":
        return _confusion()
    if kind == "gaussian":
        return _gaussian()
    if kind == "regression":
        return _regression()
    if kind == "svm":
        return _svm()
    if kind == "graphical":
        return _graphical()
    if kind == "gmm":
        return _gmm()
    raise ValueError(f"Unknown diagram kind: {kind}")


EXTRA_DIAGRAM_META = {}
for _name, _spec in SPECS.items():
    if len(_spec) >= 3:
        EXTRA_DIAGRAM_META[_name] = (_spec[1], _spec[2])
    else:
        _custom_meta = {
            "train-confusion.svg": ("Confusion Matrix 읽기", "예측과 실제를 네 경우로 나눠 오류 종류를 봅니다."),
            "prml-gaussian.svg": ("Gaussian distribution", "평균과 분산이 분포 모양을 어떻게 바꾸는지 봅니다."),
            "prml-regression.svg": ("Linear regression", "연속 target을 예측하는 선형 모델의 직관입니다."),
            "prml-svm.svg": ("SVM margin", "결정 경계와 support vector 사이의 margin을 봅니다."),
            "prml-graphical.svg": ("Graphical Model", "변수 관계를 노드와 간선으로 표현합니다."),
            "prml-gmm.svg": ("Gaussian Mixture Model", "여러 Gaussian component로 복잡한 분포를 표현합니다."),
        }
        EXTRA_DIAGRAM_META[_name] = _custom_meta[_name]


def build_extra_diagrams(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, spec in SPECS.items():
        (output_dir / name).write_text(_render(spec), encoding="utf-8")
    return len(SPECS)

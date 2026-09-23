"""Generate reusable SVG teaching diagrams for the Vision AI study site."""
from html import escape
from pathlib import Path


def _esc(value):
    return escape(str(value))


def _frame(title, subtitle, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520">
<style>
text{{font-family:Arial,'Noto Sans KR',sans-serif}}
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
    "pixels-human-vs-array.svg": ("compare", "사람이 보는 이미지 vs 컴퓨터 입력", "같은 장면도 모델에는 숫자 배열로 들어갑니다.", "사람의 관점", ["사과라는 객체","색·형태를 한 번에 인식","조금 어두워도 여전히 사과"], "컴퓨터의 입력", ["H×W×C 숫자 배열","각 픽셀은 채널 값","조명 변화가 숫자 변화로 전달"]),
    "pixels-channels.svg": ("flow", "RGB 채널 분리", "컬러 이미지는 Red, Green, Blue 세 채널의 조합입니다.", [["원본","H×W×3"],["R 채널","빨강 세기"],["G 채널","초록 세기"],["B 채널","파랑 세기"],["결합","RGB 이미지"]]),
    "pixels-lighting.svg": ("compare", "같은 물체, 다른 조명", "물체의 의미는 같아도 픽셀 값 분포는 크게 달라질 수 있습니다.", "밝은 조명", ["배경 210~240","물체 120~200","그림자 약함"], "어두운 조명", ["배경 70~110","물체 40~100","그림자 대비 증가"]),
    "pixels-resize.svg": ("compare", "Resize가 바꾸는 정보", "해상도를 줄이면 계산량은 줄지만 작은 구조가 사라질 수 있습니다.", "1920×1080", ["약 207만 위치","작은 결함 픽셀 다수","계산량 큼"], "224×224", ["약 5만 위치","미세 구조 손실 가능","계산량 작음"]),
    "pixels-normalization.svg": ("flow", "픽셀 값 전처리 흐름", "학습과 추론에서 같은 전처리 계약을 사용해야 합니다.", [["uint8","0~255"],["float","0.0~1.0"],["표준화","(x-μ)/σ"],["Tensor","모델 입력"],["Model","예측"]]),

    # CNN
    "cnn-sliding.svg": ("flow", "Kernel sliding", "작은 커널이 입력 위를 이동하며 각 위치의 반응을 계산합니다.", [["Input patch","3×3"],["Kernel","3×3"],["Multiply","원소별 곱"],["Sum","+ bias"],["Feature","한 출력값"]]),
    "cnn-stride.svg": ("compare", "Stride 1 vs Stride 2", "Stride는 커널이 한 번에 이동하는 간격입니다.", "Stride = 1", ["촘촘히 이동","공간 해상도 보존","출력 크기 큼"], "Stride = 2", ["두 칸씩 이동","출력 크기 감소","작은 패턴 손실 가능"]),
    "cnn-padding.svg": ("compare", "Padding 없음 vs Same padding", "가장자리 처리 방식이 출력 공간 크기를 바꿉니다.", "Padding = 0", ["경계 바깥 값 없음","출력 공간 감소","가장자리 정보 덜 반영"], "Padding = 1", ["3×3에서 가장자리 1칸 추가","stride 1이면 크기 유지","경계도 동일 횟수 계산"]),
    "cnn-multichannel.svg": ("flow", "RGB에서 하나의 출력 채널", "일반 Conv는 입력 채널별 계산을 합쳐 하나의 출력 채널을 만듭니다.", [["R","3×3"],["G","3×3"],["B","3×3"],["합산","+ bias"],["Output","1 channel"]]),
    "cnn-featuremaps.svg": ("compare", "Feature map은 무엇에 반응할까?", "각 채널은 서로 다른 패턴에 강하게 반응하도록 학습될 수 있습니다.", "초기 feature", ["수직 경계","수평 경계","밝기 변화"], "깊은 feature", ["텍스처 조합","부품 형태","클래스에 유용한 패턴"]),
    "cnn-receptive.svg": ("flow", "Receptive field 확장", "층이 깊어지면 하나의 출력이 더 넓은 입력 문맥을 보게 됩니다.", [["Layer 1","3×3"],["Layer 2","5×5"],["Layer 3","7×7"],["Deep","더 넓은 문맥"]]),
    "cnn-hierarchy.svg": ("flow", "CNN 특징의 계층적 표현", "초기에는 단순한 패턴, 깊은 층에서는 더 복합적인 조합을 표현합니다.", [["Edge","경계"],["Texture","반복 무늬"],["Part","부분 구조"],["Object cue","객체 단서"]]),
    "cnn-pooling.svg": ("compare", "Max Pooling 전후", "작은 영역에서 대표값만 남겨 공간 크기를 줄입니다.", "입력 2×2", ["1  5","2  3","위치 정보 풍부"], "Max = 5", ["대표값 하나 유지","공간 크기 감소","정확한 위치 일부 손실"]),

    # ViT
    "vit-patches.svg": ("flow", "이미지를 Patch로 바꾸기", "224×224, patch 16이면 14×14=196개의 patch가 생깁니다.", [["Image","224×224×3"],["Grid","14×14"],["Patch","16×16×3"],["196개","sequence"]]),
    "vit-flatten.svg": ("flow", "Patch → Flatten → Embedding", "각 patch를 1차원으로 펼친 뒤 학습 가능한 선형 변환을 적용합니다.", [["16×16×3","patch"],["Flatten","768"],["Linear","W·x+b"],["Embedding","D차원"]]),
    "vit-position.svg": ("compare", "왜 위치 정보가 필요한가?", "Attention 자체는 token의 원래 2차원 위치를 자동으로 알지 못합니다.", "위치 정보 없음", ["토큰 집합처럼 처리","왼쪽/오른쪽 구분 약함","순서 변화에 둔감"], "Position embedding", ["각 patch 위치 코드 추가","공간 순서 전달","사전학습 위치 정보 활용"]),
    "vit-cls.svg": ("flow", "CLS token의 역할", "분류용 추가 token이 여러 encoder 층에서 patch 정보와 상호작용합니다.", [["CLS","초기 학습 벡터"],["Attention","patch와 교환"],["Encoder","여러 층 반복"],["CLS final","이미지 표현"],["Head","class logits"]]),
    "vit-attention.svg": ("flow", "Self-Attention 계산 감각", "한 token이 다른 모든 token을 얼마나 참고할지 가중치를 계산합니다.", [["Query","무엇을 찾나"],["Key","비교 기준"],["Score","Q·K"],["Softmax","가중치"],["Value","정보 혼합"]]),
    "vit-attention-matrix.svg": ("matrix", "Attention score matrix", "각 행은 한 query가 모든 key를 얼마나 참고하는지 나타냅니다."),
    "vit-multihead.svg": ("flow", "Multi-Head Attention", "여러 head가 서로 다른 관계 패턴을 병렬로 볼 수 있습니다.", [["Input","tokens"],["Head 1","형태 관계"],["Head 2","위치 관계"],["Head 3","색/텍스처"],["Concat","다시 결합"]]),
    "vit-cnn-compare.svg": ("compare", "CNN과 ViT의 정보 혼합 방식", "둘 다 이미지를 학습하지만 기본 연결 방식이 다릅니다.", "CNN", ["작은 지역부터 계산","공유 kernel","깊어지며 문맥 확대"], "ViT", ["patch token으로 변환","attention으로 관계 계산","초기부터 전역 관계 가능"]),

    # tasks
    "tasks-three-way.svg": ("compare", "Classification vs Detection", "Segmentation은 별도 픽셀 출력까지 만듭니다.", "Classification", ["이미지 전체 class","출력: class score","위치 정보 없음"], "Detection", ["object class + box","여러 객체 가능","대략적 위치 제공"]),
    "tasks-segmentation.svg": ("compare", "Semantic vs Instance Segmentation", "같은 클래스 객체를 하나로 볼지 각각 나눌지의 차이입니다.", "Semantic", ["픽셀마다 class","같은 class 객체는 동일 라벨","도로/배경 등에 적합"], "Instance", ["객체별 mask","같은 class도 구분","개수와 형태 추적 가능"]),
    "tasks-output-types.svg": ("flow", "Vision task의 출력 형태", "문제 종류에 따라 모델이 내야 하는 출력 자료구조가 달라집니다.", [["Image","입력"],["Class","K scores"],["Boxes","N×4 + score"],["Masks","H×W"],["Decision","업무 로직"]]),
    "tasks-label-box-mask.svg": ("flow", "Label · Box · Mask의 정보량", "라벨링 비용과 위치 정밀도가 함께 증가합니다.", [["Class label","무엇인가"],["Box","어디쯤"],["Mask","정확히 어느 픽셀"],["Metric","task별 평가"]]),

    # training
    "train-split.svg": ("flow", "Train / Validation / Test", "세 집합은 역할이 다르며 test는 최종 평가까지 격리해야 합니다.", [["Train","가중치 학습"],["Validation","모델 선택"],["Threshold","운영 기준"],["Test","최종 일반화"]]),
    "train-leakage.svg": ("compare", "좋은 분할 vs Data leakage", "같은 원본 영상의 유사 frame이 섞이면 성능이 부풀 수 있습니다.", "좋은 split", ["원본 그룹 단위 분리","시간대/설비 누수 방지","실제 일반화 평가"], "나쁜 split", ["frame random split","near-duplicate 섞임","평가 과대추정"]),
    "train-confusion.svg": ("confusion",),
    "train-prf.svg": ("compare", "Precision과 Recall의 관점", "같은 confusion matrix에서 서로 다른 질문을 합니다.", "Precision", ["이상이라고 한 것 중","얼마나 진짜 이상인가?","FP에 민감"], "Recall", ["실제 이상 중","얼마나 놓치지 않았나?","FN에 민감"]),
    "train-threshold.svg": ("threshold_curve", "Threshold를 바꾸면 무엇이 변할까?", "고정된 score에서 threshold를 높이면 positive 판정 수가 줄어 Recall과 false-positive rate가 감소하거나 유지됩니다."),
    "train-curves.svg": ("compare", "ROC curve와 PR curve", "불균형 데이터에서는 PR curve도 함께 보는 것이 중요합니다.", "ROC", ["TPR vs FPR","threshold 전 범위","음성 샘플 영향 큼"], "PR", ["Precision vs Recall","positive 성능 집중","희소 이상 탐지에 유용"]),
    "train-overfit.svg": ("overfit_curve", "Overfitting의 전형적 신호", "train loss는 계속 낮아져도 validation loss가 최저점을 지난 뒤 다시 높아질 수 있습니다."),

    # ResNet
    "resnet-plain-vs.svg": ("compare", "Plain network vs Residual network", "Residual connection은 깊은 네트워크의 최적화 문제를 재표현합니다.", "Plain", ["층을 순차 연결","전체 H(x)를 직접 학습","깊어지면 degradation 가능"], "Residual", ["shortcut으로 x 전달","F(x)=H(x)-x 학습","identity 경로 확보"]),
    "resnet-shortcuts.svg": ("compare", "Identity vs Projection shortcut", "입출력 shape가 같은지에 따라 shortcut 구현이 달라집니다.", "Identity", ["shape 동일","x를 그대로 더함","추가 파라미터 없음"], "Projection", ["shape 변경 필요","1×1 Conv 등 사용","채널/해상도 맞춤"]),
    "resnet-gradient.svg": ("flow", "Residual 경로의 gradient 흐름", "출력에서 입력까지 직접 이어지는 항이 존재합니다.", [["Output","H(x)"],["Add","x + F(x)"],["Shortcut","identity"],["Input","x"]]),
    "resnet-function.svg": ("flow", "전체 함수보다 변화량을 학습", "입력을 유지하는 것이 좋다면 F(x)를 0에 가깝게 만들면 됩니다.", [["Input x","기준"],["F(x)","바꿀 부분"],["Add","x+F(x)"],["H(x)","목표 출력"]]),

    # U-Net
    "unet-pyramid.svg": ("flow", "U-Net의 해상도 피라미드", "Encoder에서 공간을 줄이고 Decoder에서 다시 복원합니다.", [["256²","64ch"],["128²","128ch"],["64²","256ch"],["128²","128ch"],["256²","classes"]]),
    "unet-skip-why.svg": ("compare", "왜 Skip connection이 필요한가?", "깊은 특징의 문맥과 얕은 특징의 위치 정보를 함께 사용합니다.", "Encoder deep", ["넓은 문맥","의미 정보 풍부","공간 세부 감소"], "Skip feature", ["높은 해상도","경계/위치 정보","Decoder에 직접 전달"]),
    "unet-mask-triplet.svg": ("flow", "Segmentation 결과 읽기", "입력·정답·예측을 같은 위치에서 비교해야 오류를 이해하기 쉽습니다.", [["Input","원본 이미지"],["GT mask","정답"],["Pred mask","예측"],["Overlay","오류 위치"]]),
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
    "prml-variational.svg": ("flow", "Variational Inference", "복잡한 posterior 대신 다루기 쉬운 q를 최적화해 근사합니다.", [["True posterior","p(z|x)"],["Choose q","family"],["Optimize","ELBO ↑"],["KL","q→posterior"],["Approx","inference"]]),
    "prml-sampling.svg": ("flow", "Monte Carlo sampling", "분포에서 여러 샘플을 뽑아 기대값이나 posterior 특성을 근사합니다.", [["Target p(x)","분포"],["Sample","x¹,x²,…"],["Evaluate","f(xⁿ)"],["Average","1/N Σ"],["Estimate","expectation"]]),
    "prml-pca.svg": ("compare", "PCA가 찾는 방향", "데이터 분산이 큰 축을 찾아 저차원 좌표로 투영합니다.", "원 좌표", ["x₁, x₂ 축","점들이 대각선으로 퍼짐","상관 존재"], "주성분 좌표", ["PC1 = 큰 분산 방향","PC2 = 작은 분산 방향","상위 축만 남겨 축소 가능"]),
    "prml-ensemble.svg": ("flow", "Ensemble / Mixture of Experts", "여러 모델 출력을 결합하되 결합 규칙은 방법마다 다릅니다.", [["Model A","prediction"],["Model B","prediction"],["Model C","prediction"],["Combine","average/gate"],["Output","final"]]),
}


def _render(spec):
    kind = spec[0]
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

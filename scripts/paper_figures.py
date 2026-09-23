"""Generate paper-style multi-panel figures for CNN, ViT and PatchCore notes."""

from html import escape
from pathlib import Path


def _e(value):
    return escape(str(value))


def _svg(title, subtitle, body, height=760):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" role="img" aria-label="{_e(title)}">
<style>
.title{{font:700 27px Arial,'Noto Sans KR',sans-serif;fill:#18243b}}
.subtitle{{font:18px Arial,'Noto Sans KR',sans-serif;fill:#5b6880}}
.panel-label{{font:700 19px Arial,'Noto Sans KR',sans-serif;fill:#18243b}}
.label{{font:700 18px Arial,'Noto Sans KR',sans-serif;fill:#203455}}
.body{{font:16px Arial,'Noto Sans KR',sans-serif;fill:#526178}}
.small{{font:14px Arial,'Noto Sans KR',sans-serif;fill:#68768c}}
.white{{font:700 16px Arial,'Noto Sans KR',sans-serif;fill:#fff}}
.panel{{fill:#fff;stroke:#d2dceb;stroke-width:2}}
.soft{{fill:#f3f7fe;stroke:#c9d6ea;stroke-width:2}}
.blue{{fill:#edf3ff;stroke:#8faee8;stroke-width:2}}
.green{{fill:#e9f7f2;stroke:#8ccdbb;stroke-width:2}}
.orange{{fill:#fff1e7;stroke:#e0ae82;stroke-width:2}}
.line{{stroke:#7e91af;stroke-width:3;fill:none}}
.thin{{stroke:#a8b5c8;stroke-width:2;fill:none}}
</style>
<rect width="1200" height="{height}" rx="24" fill="#f8fafc"/>
<text x="42" y="48" class="title">{_e(title)}</text>
<text x="42" y="78" class="subtitle">{_e(subtitle)}</text>
{body}
</svg>'''


def _panel(x, y, w, h, letter, title):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="panel"/>'
        f'<text x="{x+18}" y="{y+30}" class="panel-label">({letter})</text>'
        f'<text x="{x+58}" y="{y+30}" class="label">{_e(title)}</text>'
    )


def _arrow(x1, y1, x2, y2):
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" class="line"/>'
        f'<polygon points="{x2},{y2} {x2-14},{y2-9} {x2-14},{y2+9}" fill="#7e91af"/>'
    )


def _grid(x, y, rows, cols, cell=30, mode="blue", values=None):
    fills = {
        "blue": ["#f0f4fb", "#dce7fa", "#bcd1f6", "#7fa4ec", "#2f63d8"],
        "heat": ["#fff4e8", "#ffd9b3", "#f5a45e", "#db6945", "#a52a2a"],
        "gray": ["#f4f5f7", "#d9dee6", "#adb7c5", "#768397", "#344156"],
        "green": ["#eff8f5", "#d5eee6", "#afe0d2", "#6fc0aa", "#08796f"],
    }[mode]
    parts = []
    for r in range(rows):
        for c in range(cols):
            v = values[r][c] if values else ((r * 3 + c * 5 + r*c) % 5)
            fill = fills[max(0, min(4, int(v)))]
            parts.append(
                f'<rect x="{x+c*cell}" y="{y+r*cell}" width="{cell-3}" height="{cell-3}" '
                f'rx="4" fill="{fill}" stroke="#d5deeb"/>'
            )
    return "".join(parts)


def _cnn_overview():
    b = []
    panels = [
        (35,120,205,235,"a","Input"),
        (270,120,205,235,"b","Edge maps"),
        (505,120,205,235,"c","Texture maps"),
        (740,120,205,235,"d","Part features"),
        (975,120,190,235,"e","Prediction"),
    ]
    for p in panels:
        b.append(_panel(*p))
    b.append('<ellipse cx="138" cy="235" rx="62" ry="50" fill="#efb46f" stroke="#c77b30" stroke-width="3"/>')
    b.append('<polygon points="87,202 116,150 133,207" fill="#efb46f" stroke="#c77b30" stroke-width="3"/>')
    b.append('<polygon points="189,202 160,150 143,207" fill="#efb46f" stroke="#c77b30" stroke-width="3"/>')
    b.append('<circle cx="116" cy="230" r="8" fill="#26364d"/><circle cx="159" cy="230" r="8" fill="#26364d"/>')
    b.append(_grid(305,180,4,4,34,"gray"))
    b.append(_grid(540,180,4,4,34,"blue"))
    for i, (x,y,w,h) in enumerate([(775,175,118,35),(800,230,90,35),(770,285,125,35)]):
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="green"/>')
        b.append(f'<text x="{x+w/2}" y="{y+23}" text-anchor="middle" class="body">part {i+1}</text>')
    for i,(name,width,color) in enumerate([("cat 0.82",125,"#2454d8"),("dog 0.11",82,"#89a9ec"),("fox 0.04",52,"#c7d6f4")]):
        y=185+i*55
        b.append(f'<rect x="1000" y="{y}" width="{width}" height="25" rx="8" fill="{color}"/>')
        b.append(f'<text x="1000" y="{y+44}" class="small">{name}</text>')
    for x in [240,475,710,945]:
        b.append(_arrow(x,238,x+25,238))
    b.append(_panel(150,415,900,250,"f","Feature hierarchy is learned, not manually assigned"))
    b.append('<text x="200" y="485" class="body">초기 layer: 밝기 변화·방향성 경계 같은 단순 패턴에 반응</text>')
    b.append('<text x="200" y="530" class="body">중간 layer: 여러 edge를 조합해 반복 무늬·모서리·부분 형태 표현</text>')
    b.append('<text x="200" y="575" class="body">깊은 layer: task에 유용한 복합 특징을 형성하지만, 각 channel이 항상 사람이 붙인 의미와 1:1 대응하지는 않음</text>')
    b.append('<text x="200" y="620" class="small">그림은 개념적 예시이며 실제 학습된 feature map은 모델·데이터에 따라 달라집니다.</text>')
    return _svg("Figure 1. CNN: pixels → local responses → task features",
                "논문 figure처럼 입력·중간 표현·출력을 한 화면에서 연결합니다.", "".join(b), 720)



def _cnn_convolution():
    b = []
    for p in [
        (35,120,245,245,"a","5×5 input"),
        (305,120,175,245,"b","3×3 kernel"),
        (505,120,245,245,"c","selected patch"),
        (775,120,390,245,"d","multiply & sum"),
        (250,410,700,260,"e","output feature map"),
    ]:
        b.append(_panel(*p))

    values = [[0,0,1,1,1] for _ in range(5)]
    for r in range(5):
        for c in range(5):
            x = 62 + c * 38
            y = 168 + r * 34
            fill = "#2f63d8" if c >= 2 else "#dce8fb"
            if r < 3 and c < 3:
                fill = "#2454d8" if c == 2 else "#cfe0fb"
            tc = "#fff" if fill in ("#2454d8", "#2f63d8") else "#203455"
            b.append(
                f'<rect x="{x}" y="{y}" width="30" height="27" rx="4" '
                f'fill="{fill}" stroke="#9fb8e4"/>'
            )
            b.append(
                f'<text x="{x+15}" y="{y+19}" text-anchor="middle" '
                f'font-size="15" fill="{tc}">{values[r][c]}</text>'
            )

    kernel = [[-1,0,1],[-1,0,1],[-1,0,1]]
    for r in range(3):
        for c in range(3):
            x = 335 + c * 42
            y = 190 + r * 43
            b.append(
                f'<rect x="{x}" y="{y}" width="32" height="32" rx="5" '
                'class="orange"/>'
            )
            b.append(
                f'<text x="{x+16}" y="{y+22}" text-anchor="middle" '
                f'class="body">{kernel[r][c]}</text>'
            )

    for r in range(3):
        for c in range(3):
            x = 548 + c * 50
            y = 190 + r * 43
            value = 1 if c == 2 else 0
            fill = "#2454d8" if value else "#e8effb"
            tc = "#fff" if value else "#203455"
            b.append(
                f'<rect x="{x}" y="{y}" width="40" height="32" rx="5" '
                f'fill="{fill}" stroke="#9fb8e4"/>'
            )
            b.append(
                f'<text x="{x+20}" y="{y+22}" text-anchor="middle" '
                f'font-size="16" fill="{tc}">{value}</text>'
            )

    for i, expr in enumerate([
        "0×−1 + 0×0 + 1×1 = 1",
        "0×−1 + 0×0 + 1×1 = 1",
        "0×−1 + 0×0 + 1×1 = 1",
    ]):
        b.append(f'<text x="820" y="{190+i*48}" class="body">{expr}</text>')
    b.append(
        '<path d="M815 324 H1120" class="thin"/>'
        '<text x="820" y="350" class="label">'
        '1 + 1 + 1 + bias(0) = 3</text>'
    )

    # Cross-correlation for each 3-column window:
    # [0,0,1] -> 3, [0,1,1] -> 3, [1,1,1] -> 0.
    output = [[3,3,0],[3,3,0],[3,3,0]]
    for r, row in enumerate(output):
        for c, value in enumerate(row):
            x = 420 + c * 110
            y = 485 + r * 52
            fill = "#2454d8" if value else "#eef3fb"
            tc = "#fff" if value else "#203455"
            b.append(
                f'<rect x="{x}" y="{y}" width="76" height="36" rx="6" '
                f'fill="{fill}" stroke="#9fb8e4"/>'
            )
            b.append(
                f'<text x="{x+38}" y="{y+24}" text-anchor="middle" '
                f'font-size="18" fill="{tc}">{value}</text>'
            )
    b.append(
        '<text x="420" y="650" class="small">'
        '각 행의 출력은 [3, 3, 0]. 고정 kernel의 설명용 cross-correlation 예시입니다.'
        '</text>'
    )
    return _svg(
        "Figure 2. Convolution mechanics",
        "입력 patch와 kernel의 element-wise 곱이 output 한 위치로 연결됩니다.",
        "".join(b),
        710,
    )

def _cnn_multichannel():
    b=[]
    xs=[35,245,455]
    cols=[("#f8dede","R"),("#e0f2df","G"),("#e1e9fa","B")]
    for i,(x,(fill,name)) in enumerate(zip(xs,cols)):
        b.append(_panel(x,125,180,250,chr(97+i),f"{name} channel"))
        b.append(_grid(x+32,185,3,3,34,"gray"))
        b.append(f'<rect x="{x+43}" y="304" width="95" height="34" rx="8" fill="{fill}" stroke="#b9c7da"/>')
        b.append(f'<text x="{x+90}" y="326" text-anchor="middle" class="body">conv {name}</text>')
    b.append(_panel(675,125,215,250,"d","sum across channels"))
    b.append('<text x="710" y="200" class="label">R response</text><text x="710" y="245" class="label">+ G response</text><text x="710" y="290" class="label">+ B response</text><text x="710" y="335" class="body">+ bias</text>')
    b.append(_panel(920,125,245,250,"e","one output channel"))
    b.append(_grid(970,190,4,4,37,"blue"))
    b.append(_arrow(635,250,665,250)); b.append(_arrow(890,250,912,250))
    b.append(_panel(120,425,960,230,"f","Weight tensor"))
    b.append('<text x="165" y="495" class="body">RGB 입력 → 32 output channels, kernel 3×3일 때</text>')
    b.append('<text x="165" y="545" class="label">W ∈ R^[32 × 3 × 3 × 3]</text>')
    b.append('<text x="165" y="590" class="body">한 output channel은 입력 3개 channel의 convolution response를 합쳐 만듭니다.</text>')
    b.append('<text x="165" y="625" class="small">1×1 convolution도 공간 이웃은 보지 않지만 channel mixing은 수행합니다.</text>')
    return _svg("Figure 3. Multi-channel convolution",
                "RGB channel별 계산이 합쳐져 하나의 output channel을 구성합니다.", "".join(b), 700)


def _cnn_stride_padding():
    b=[]
    for p in [(35,120,540,245,"a","stride = 1"),(625,120,540,245,"b","stride = 2"),
              (35,410,540,245,"c","same padding"),(625,410,540,245,"d","output-size summary")]:
        b.append(_panel(*p))
    b.append(_grid(85,180,5,5,28,"blue")); b.append(_grid(400,195,3,3,38,"gray"))
    b.append(_arrow(275,245,380,245))
    b.append('<text x="85" y="340" class="small">kernel이 한 칸씩 이동 → 더 촘촘한 output</text>')
    b.append(_grid(680,180,5,5,28,"blue")); b.append(_grid(1000,205,2,2,48,"gray"))
    b.append(_arrow(870,245,975,245))
    b.append('<text x="680" y="340" class="small">두 칸씩 이동 → output 공간 크기 감소</text>')
    b.append('<rect x="90" y="470" width="190" height="145" rx="12" fill="#fff" stroke="#8faee8" stroke-width="3" stroke-dasharray="8 6"/>')
    b.append(_grid(112,492,5,5,24,"blue")); b.append(_arrow(310,540,390,540)); b.append(_grid(420,485,5,5,25,"green"))
    b.append('<text x="90" y="638" class="small">3×3, stride 1, padding 1 → H×W 유지</text>')
    rows=[
        ("5×5, K=3, S=1, P=0","3×3"),
        ("5×5, K=3, S=2, P=0","2×2"),
        ("5×5, K=3, S=1, P=1","5×5"),
    ]
    for i,(a,o) in enumerate(rows):
        y=480+i*55
        b.append(f'<text x="670" y="{y}" class="body">{a}</text><text x="1110" y="{y}" text-anchor="end" class="label">{o}</text>')
    return _svg("Figure 4. Stride and padding",
                "같은 input이라도 stride와 padding 설정에 따라 sampling 밀도와 output 크기가 달라집니다.", "".join(b), 700)



def _cnn_receptive():
    b = []
    b.append(_panel(35,120,1130,520,"a","Receptive field grows through depth"))
    b.append(
        '<rect x="80" y="180" width="1020" height="390" rx="22" '
        'fill="#fff7ee" stroke="#efc59c"/>'
    )
    b.append(
        '<ellipse cx="545" cy="380" rx="240" ry="160" '
        'fill="#efc087" stroke="#c98a49" stroke-width="3"/>'
    )
    b.append(
        '<polygon points="365,280 435,205 465,310" '
        'fill="#efc087" stroke="#c98a49" stroke-width="3"/>'
    )
    b.append(
        '<polygon points="725,280 655,205 625,310" '
        'fill="#efc087" stroke="#c98a49" stroke-width="3"/>'
    )
    b.append(
        '<circle cx="475" cy="365" r="18" fill="#26364d"/>'
        '<circle cx="620" cy="365" r="18" fill="#26364d"/>'
    )
    b.append(
        '<rect x="450" y="340" width="55" height="55" rx="8" '
        'fill="none" stroke="#2454d8" stroke-width="5"/>'
    )
    b.append(
        '<rect x="405" y="300" width="150" height="145" rx="10" '
        'fill="none" stroke="#08796f" stroke-width="5"/>'
    )
    b.append(
        '<rect x="300" y="225" width="490" height="300" rx="14" '
        'fill="none" stroke="#a24d18" stroke-width="5"/>'
    )
    b.append(
        '<text x="835" y="300" class="label" fill="#2454d8">'
        'shallower unit: local region</text>'
    )
    b.append(
        '<text x="835" y="360" class="label" fill="#08796f">'
        'deeper unit: broader region</text>'
    )
    b.append(
        '<text x="835" y="430" class="label" fill="#a24d18">'
        'more layers: larger context</text>'
    )
    b.append(
        '<text x="835" y="490" class="small">'
        '넓은 수용영역이 특정 semantic 의미를 자동 보장하지는 않습니다.</text>'
    )
    return _svg(
        "Figure 5. Receptive-field growth",
        "깊은 layer의 unit일수록 더 넓은 입력 영역과 연결될 수 있습니다.",
        "".join(b),
        690,
    )

def _cnn_pooling():
    b=[]
    for p in [(35,120,330,255,"a","input feature map"),(435,120,330,255,"b","max pooling"),(835,120,330,255,"c","average pooling"),
              (125,425,950,220,"d","Interpretation")]:
        b.append(_panel(*p))
    vals=[[1,5,2,1],[4,3,0,1],[1,2,6,2],[0,1,2,4]]
    for r,row in enumerate(vals):
        for c,v in enumerate(row):
            x=85+c*55;y=185+r*43
            fill="#2454d8" if v>=5 else "#cbdcf8" if v>=3 else "#eef3fb";tc="#fff" if v>=5 else "#203455"
            b.append(f'<rect x="{x}" y="{y}" width="42" height="32" rx="5" fill="{fill}" stroke="#9fb8e4"/>')
            b.append(f'<text x="{x+21}" y="{y+22}" text-anchor="middle" font-size="17" fill="{tc}">{v}</text>')
    for r,row in enumerate([[5,2],[2,6]]):
        for c,v in enumerate(row):
            x=515+c*95;y=205+r*72
            fill="#2454d8" if v>=5 else "#dce7fa";tc="#fff" if v>=5 else "#203455"
            b.append(f'<rect x="{x}" y="{y}" width="65" height="44" rx="7" fill="{fill}" stroke="#9fb8e4"/>')
            b.append(f'<text x="{x+32}" y="{y+29}" text-anchor="middle" font-size="19" fill="{tc}">{v}</text>')
    for r,row in enumerate([[3.25,1.0],[1.0,3.5]]):
        for c,v in enumerate(row):
            x=915+c*100;y=205+r*72
            b.append(f'<rect x="{x}" y="{y}" width="72" height="44" rx="7" class="green"/>')
            b.append(f'<text x="{x+36}" y="{y+29}" text-anchor="middle" class="body">{v}</text>')
    for i,t in enumerate([
        "공간 크기를 줄여 계산량을 낮춤",
        "max pooling은 강한 local response를 보존",
        "위치 변화에 어느 정도 둔감해질 수 있지만 작은 결함 위치 정보도 잃을 수 있음",
    ]):
        b.append(f'<text x="175" y="{490+i*48}" class="body">• {_e(t)}</text>')
    return _svg("Figure 6. Pooling",
                "feature map을 공간적으로 요약하는 두 대표 방식의 차이를 봅니다.", "".join(b), 690)


def _vit_overview():
    b=[]
    for p in [(30,120,210,245,"a","Image"),(270,120,210,245,"b","Patch grid"),(510,120,210,245,"c","Tokens"),
              (750,120,210,245,"d","Transformer"),(990,120,180,245,"e","Head")]:
        b.append(_panel(*p))
    b.append('<rect x="75" y="175" width="120" height="120" rx="14" fill="#dfe8f8" stroke="#91aee3"/>')
    b.append('<circle cx="135" cy="235" r="42" fill="#eeb575" stroke="#c77d37"/>')
    for r in range(4):
        for c in range(4):
            b.append(f'<rect x="{305+c*34}" y="{175+r*34}" width="30" height="30" rx="3" fill="{"#2454d8" if (r+c)%3==0 else "#dce7fa"}" stroke="#fff"/>')
    for i in range(6):
        x=535+i*27
        b.append(f'<rect x="{x}" y="190" width="18" height="105" rx="6" fill="{"#2454d8" if i==0 else "#9ab5ea"}"/>')
    for i in range(3):
        b.append(f'<rect x="790" y="{175+i*55}" width="130" height="38" rx="10" class="blue"/>')
        b.append(f'<text x="855" y="{199+i*55}" text-anchor="middle" class="body">Encoder {i+1}</text>')
    for i,(name,w) in enumerate([("cat",120),("dog",65),("fox",40)]):
        y=180+i*55;b.append(f'<rect x="1018" y="{y}" width="{w}" height="24" rx="7" fill="{"#2454d8" if i==0 else "#aec4ed"}"/>')
        b.append(f'<text x="1018" y="{y+43}" class="small">{name}</text>')
    for x in [240,480,720,960]: b.append(_arrow(x,240,x+25,240))
    b.append(_panel(165,430,870,210,"f","Core idea"))
    b.append('<text x="205" y="500" class="body">이미지를 작은 patch로 나누고 각 patch를 token vector로 바꾼 뒤, self-attention으로 token 간 관계를 학습합니다.</text>')
    b.append('<text x="205" y="550" class="body">CNN의 sliding kernel 대신 token sequence + attention을 기본 계산 단위로 사용합니다.</text>')
    b.append('<text x="205" y="600" class="small">ViT-B/16 예: 224×224 image → 16×16 patch → 196 patch tokens + 1 CLS token.</text>')
    return _svg("Figure 1. Vision Transformer overview",
                "image → patch → token → transformer encoder → classification head", "".join(b), 690)



def _vit_patch_embedding():
    b = []
    for p in [
        (35,120,360,500,"a","patching (schematic grid)"),
        (425,120,330,500,"b","flatten"),
        (785,120,380,500,"c","linear projection"),
    ]:
        b.append(_panel(*p))
    for r in range(7):
        for c in range(7):
            fill = "#2454d8" if (r in (2,3) and c in (3,4)) else "#dce7fa"
            b.append(
                f'<rect x="{80+c*38}" y="{185+r*38}" width="34" height="34" '
                f'rx="4" fill="{fill}" stroke="#fff"/>'
            )
    b.append(
        '<rect x="190" y="300" width="72" height="72" '
        'fill="none" stroke="#a24d18" stroke-width="5"/>'
    )
    b.append(
        '<text x="80" y="500" class="body">'
        'ViT-B/16 실제 예: 224/16=14 → 196 patches</text>'
    )
    b.append(
        '<text x="80" y="535" class="small">'
        '위 7×7 grid는 가독성을 위한 축약 도식입니다.</text>'
    )
    for i in range(12):
        x = 480 + (i % 3) * 72
        y = 190 + (i // 3) * 62
        b.append(
            f'<rect x="{x}" y="{y}" width="55" height="42" rx="6" '
            f'fill="{"#2454d8" if i in (2,5,8) else "#eef3fb"}" '
            'stroke="#9fb8e4"/>'
        )
    b.append(
        '<text x="475" y="485" class="body">16×16×3 = 768 values</text>'
        '<text x="475" y="530" class="small">2D patch를 1D vector로 펼침</text>'
    )
    b.append(_arrow(735,350,790,350))
    b.append(
        '<rect x="840" y="200" width="270" height="95" rx="14" class="orange"/>'
    )
    b.append(
        '<text x="975" y="240" text-anchor="middle" class="label">'
        'z = x_patch E + b</text>'
    )
    b.append(
        '<text x="975" y="270" text-anchor="middle" class="body">'
        'E ∈ R^[P²C × D]</text>'
    )
    for i in range(8):
        b.append(
            f'<rect x="{850+i*30}" y="355" width="18" '
            f'height="{65+(i%3)*18}" rx="5" '
            f'fill="{"#2454d8" if i%2==0 else "#8eace7"}"/>'
        )
    b.append(
        '<text x="840" y="515" class="body">output: D-dimensional token</text>'
    )
    return _svg(
        "Figure 2. Patch embedding",
        "patch를 펼친 뒤 learned linear projection으로 token embedding을 만듭니다.",
        "".join(b),
        670,
    )

def _vit_cls_position():
    b=[]
    b.append(_panel(35,120,1130,500,"a","CLS token + positional embedding"))
    # token row
    labels=["CLS","p1","p2","p3","p4","…","p196"]
    xs=[100,235,370,505,640,775,930]
    for i,(x,l) in enumerate(zip(xs,labels)):
        fill="#2454d8" if i==0 else "#edf3ff";stroke="#2454d8" if i==0 else "#99b4e6";tc="#fff" if i==0 else "#203455"
        b.append(f'<rect x="{x}" y="205" width="105" height="65" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(f'<text x="{x+52}" y="245" text-anchor="middle" font-size="17" fill="{tc}">{l}</text>')
    b.append('<text x="100" y="315" class="label">+</text>')
    # pos row
    for i,x in enumerate(xs):
        b.append(f'<rect x="{x}" y="300" width="105" height="50" rx="10" class="green"/>')
        b.append(f'<text x="{x+52}" y="331" text-anchor="middle" class="body">pos {i}</text>')
    b.append('<text x="100" y="395" class="label">= Transformer input sequence</text>')
    for i,x in enumerate(xs):
        b.append(f'<rect x="{x}" y="430" width="105" height="55" rx="10" fill="{"#dbe7fb" if i else "#7fa4ec"}" stroke="#8faee8"/>')
    b.append('<text x="100" y="550" class="body">CLS는 처음부터 이미지 의미를 아는 token이 아니라, encoder를 거치며 patch들과 정보를 주고받는 학습 가능한 vector입니다.</text>')
    b.append('<text x="100" y="585" class="small">position embedding은 token이 원래 이미지에서 어디에 있었는지에 대한 위치 정보를 제공합니다.</text>')
    return _svg("Figure 3. CLS token and positional embedding",
                "content embedding에 위치 정보를 더하고, 분류용 CLS token을 sequence 앞에 붙입니다.", "".join(b), 670)


def _vit_attention():
    b=[]
    for p in [(35,120,340,470,"a","Q, K, V"),(405,120,350,470,"b","attention matrix"),(785,120,380,470,"c","weighted value mixing")]:
        b.append(_panel(*p))
    for i,(name,col) in enumerate([("Q","#2454d8"),("K","#08796f"),("V","#a24d18")]):
        y=190+i*105
        b.append(f'<rect x="95" y="{y}" width="210" height="62" rx="12" fill="{col}" opacity=".92"/>')
        b.append(f'<text x="200" y="{y+38}" text-anchor="middle" class="white">{name} = XW_{name}</text>')
    b.append(_grid(470,190,6,6,39,"heat"))
    b.append('<text x="465" y="465" class="body">softmax(QKᵀ / √dₖ)</text>')
    b.append('<text x="465" y="505" class="small">밝을수록 해당 query가 그 key를 더 크게 참고</text>')
    # weighted vectors
    for i in range(5):
        b.append(f'<rect x="{835+i*48}" y="205" width="28" height="{95+i*15}" rx="6" fill="{"#2454d8" if i in (1,3) else "#a9bfea"}"/>')
    b.append(_arrow(905,350,905,405))
    b.append('<rect x="835" y="425" width="260" height="78" rx="14" class="green"/>')
    b.append('<text x="965" y="458" text-anchor="middle" class="label">Σ attentionᵢ · Vᵢ</text>')
    b.append('<text x="965" y="486" text-anchor="middle" class="body">context-aware token</text>')
    return _svg("Figure 4. Self-attention",
                "Q·K 유사도로 attention weight를 만들고, 그 weight로 V를 혼합합니다.", "".join(b), 640)



def _vit_multihead():
    b = []
    b.append(
        _panel(
            35,120,1130,500,"a",
            "Illustrative relation patterns from different heads",
        )
    )
    centers = [
        (190,300,"Head 1","example pattern A","#2454d8"),
        (465,300,"Head 2","example pattern B","#08796f"),
        (740,300,"Head 3","example pattern C","#a24d18"),
    ]
    for cx, cy, head, sub, color in centers:
        b.append(
            f'<circle cx="{cx}" cy="{cy}" r="90" fill="#fff" '
            f'stroke="{color}" stroke-width="4"/>'
        )
        for i in range(6):
            px = cx - 55 + (i % 3) * 55
            py = cy - 35 + (i // 3) * 70
            b.append(
                f'<circle cx="{px}" cy="{py}" r="10" '
                f'fill="{"#203455" if i==0 else "#b8c7df"}"/>'
            )
        if head == "Head 1":
            b.append(
                f'<path d="M{cx-55} {cy-35} L{cx} {cy-35} '
                f'L{cx+55} {cy-35}" stroke="{color}" '
                'stroke-width="4" fill="none"/>'
            )
        elif head == "Head 2":
            b.append(
                f'<path d="M{cx-55} {cy-35} L{cx+55} {cy+35}" '
                f'stroke="{color}" stroke-width="4" fill="none"/>'
            )
        else:
            b.append(
                f'<path d="M{cx} {cy-35} L{cx-55} {cy+35} '
                f'M{cx} {cy-35} L{cx+55} {cy+35}" '
                f'stroke="{color}" stroke-width="4" fill="none"/>'
            )
        b.append(
            f'<text x="{cx}" y="430" text-anchor="middle" '
            f'class="label">{head}</text>'
            f'<text x="{cx}" y="458" text-anchor="middle" '
            f'class="small">{sub}</text>'
        )
    b.append(_arrow(840,300,955,300))
    b.append(
        '<rect x="970" y="235" width="145" height="130" rx="16" class="blue"/>'
    )
    b.append(
        '<text x="1042" y="285" text-anchor="middle" class="label">Concat</text>'
        '<text x="1042" y="325" text-anchor="middle" class="body">+ projection</text>'
    )
    b.append(
        '<text x="115" y="560" class="small">'
        '각 head의 사람이 붙인 의미는 고정되지 않습니다. '
        '서로 다른 learned projections에서 관계를 병렬 계산하는 예시입니다.</text>'
    )
    return _svg(
        "Figure 5. Multi-head self-attention",
        "여러 attention head가 서로 다른 learned relation pattern을 병렬 계산합니다.",
        "".join(b),
        670,
    )


def _vit_attention_map():
    b = []
    for p in [
        (35,120,520,500,"a","Patch grid"),
        (605,120,560,500,"b","Synthetic attention example"),
    ]:
        b.append(_panel(*p))
    for r in range(7):
        for c in range(7):
            active = 2 <= r <= 5 and 2 <= c <= 4
            fill = "#e8eef8" if not active else "#d6aa78"
            b.append(
                f'<rect x="{95+c*55}" y="{190+r*50}" width="48" height="43" '
                f'rx="5" fill="{fill}" stroke="#fff"/>'
            )
    b.append(
        '<circle cx="287" cy="300" r="10" fill="#2454d8"/>'
        '<text x="100" y="575" class="small">파란 점: query patch</text>'
    )
    vals = []
    for r in range(7):
        row = []
        for c in range(7):
            d = abs(r-3) + abs(c-3)
            row.append(max(0,4-d))
        vals.append(row)
    b.append(_grid(675,185,7,7,52,"heat",vals))
    b.append(
        '<text x="675" y="555" class="small">'
        '합성 heatmap: 실제 모델에서 측정한 attention이 아닙니다.</text>'
    )
    b.append(
        '<text x="675" y="585" class="small">'
        '행/열의 weight를 patch 위치에 대응해 읽는 방법만 설명합니다.</text>'
    )
    return _svg(
        "Figure 6. Attention map as a spatial heatmap",
        "attention weight를 patch 위치에 대응시키는 방법을 합성 예시로 보여줍니다.",
        "".join(b),
        670,
    )

def _pc_overview():
    b=[]
    for p in [(35,120,245,240,"a","Normal train"),(310,120,245,240,"b","Feature extraction"),
              (585,120,245,240,"c","Memory bank"),(860,120,305,240,"d","Test & distance"),
              (160,415,880,220,"e","Anomaly localization")]:
        b.append(_panel(*p))
    # normal mini images
    for i in range(4):
        x=65+(i%2)*90;y=180+(i//2)*75
        b.append(f'<rect x="{x}" y="{y}" width="70" height="55" rx="9" class="soft"/>')
        b.append(f'<circle cx="{x+35}" cy="{y+27}" r="16" fill="#9ab0cb"/>')
    b.append(_grid(350,180,4,4,35,"blue"))
    for i in range(18):
        x=620+(i%6)*30;y=180+(i//6)*45
        b.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{"#08796f" if i%4 else "#61ae97"}"/>')
    b.append('<circle cx="930" cy="235" r="18" fill="#a24d18"/><circle cx="1035" cy="210" r="10" fill="#08796f"/>')
    b.append('<path d="M930 235 L1035 210" stroke="#a24d18" stroke-width="4" stroke-dasharray="8 6"/>')
    b.append('<text x="905" y="300" class="body">nearest-normal distance</text>')
    b.append('<rect x="245" y="475" width="260" height="105" rx="16" fill="#dfe5ec" stroke="#aab6c6"/>')
    for r in range(4):
        for c in range(6):
            heat=max(0,4-(abs(r-2)+abs(c-4)))
            colors=["#e9eef4","#ffd9b3","#f5a45e","#dc6a45","#a52a2a"]
            b.append(f'<rect x="{570+c*48}" y="{465+r*30}" width="42" height="25" rx="4" fill="{colors[heat]}"/>')
    b.append(_arrow(515,530,555,530))
    b.append('<text x="570" y="600" class="small">patch score → spatial anomaly heatmap</text>')
    return _svg("Figure 1. PatchCore overview",
                "정상 feature를 저장하고 test patch가 정상 feature manifold에서 얼마나 떨어졌는지 측정합니다.", "".join(b), 680)


def _pc_features():
    b=[]
    for p in [(35,120,300,470,"a","Input"),(365,120,370,470,"b","Intermediate feature maps"),(765,120,400,470,"c","Patch descriptors")]:
        b.append(_panel(*p))
    b.append('<rect x="90" y="190" width="190" height="260" rx="18" fill="#d9e0e8" stroke="#9da9b9"/>')
    b.append('<rect x="125" y="230" width="120" height="180" rx="20" fill="#a8b5c4"/>')
    b.append('<circle cx="185" cy="320" r="24" fill="#737f8e"/>')
    for layer,(x,y) in enumerate([(410,180),(470,255),(530,330)]):
        for k in range(3):
            b.append(f'<rect x="{x+k*18}" y="{y-k*10}" width="160" height="95" rx="8" fill="{"#dce7fa" if layer==0 else "#c1d4f3" if layer==1 else "#9bb7ea"}" stroke="#fff"/>')
        b.append(f'<text x="{x}" y="{y+125}" class="small">layer {layer+1}</text>')
    for r in range(5):
        for c in range(5):
            x=820+c*55;y=190+r*55
            fill="#2454d8" if (r,c) in [(1,3),(2,3),(3,3)] else "#e6eefb"
            b.append(f'<rect x="{x}" y="{y}" width="45" height="45" rx="6" fill="{fill}" stroke="#afc2e7"/>')
    b.append('<text x="820" y="510" class="body">각 spatial location → D-dimensional feature vector</text>')
    b.append('<text x="820" y="550" class="small">PatchCore의 “patch”는 RGB crop 자체가 아니라 CNN feature map의 지역 descriptor입니다.</text>')
    return _svg("Figure 2. From image to local feature descriptors",
                "중간 layer feature map의 각 위치를 정상 패턴을 설명하는 descriptor로 사용합니다.", "".join(b), 650)


def _pc_coreset():
    b=[]
    for p in [(35,120,535,500,"a","Full memory bank"),(625,120,540,500,"b","Coreset")]:
        b.append(_panel(*p))
    pts=[(100+i*37+(i%3)*10,220+((i*47)%260)) for i in range(12)] + [(280+i*28,260+((i*31)%220)) for i in range(8)]
    for i,(x,y) in enumerate(pts):
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{"#2454d8" if i%4 else "#85a4e5"}" opacity=".8"/>')
    b.append('<text x="90" y="570" class="small">많은 정상 feature가 서로 가까운 위치에 중복 저장될 수 있음</text>')
    for i,(x,y) in enumerate(pts):
        if i%3==0:
            xx=x+590
            b.append(f'<circle cx="{xx}" cy="{y}" r="12" fill="#08796f"/>')
        else:
            b.append(f'<circle cx="{x+590}" cy="{y}" r="5" fill="#c7d4e5"/>')
    b.append('<text x="680" y="540" class="body">대표점만 유지</text>')
    b.append('<text x="680" y="575" class="small">정상 feature 공간의 coverage를 최대한 유지하면서 memory와 검색량을 줄임</text>')
    return _svg("Figure 3. Coreset selection",
                "전체 정상 feature 중 대표점을 남겨 memory bank를 압축합니다.", "".join(b), 670)


def _pc_nearest():
    b=[]
    b.append(_panel(35,120,1130,500,"a","Nearest-neighbor distance in feature space"))
    # clusters
    for i in range(18):
        x=230+(i%6)*42+((i*17)%18);y=260+(i//6)*58+((i*13)%23)
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#08796f" opacity=".78"/>')
    for i in range(14):
        x=540+(i%5)*38+((i*11)%20);y=350+(i//5)*52+((i*7)%20)
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#08796f" opacity=".7"/>')
    b.append('<circle cx="330" cy="330" r="15" fill="#2454d8"/><text x="345" y="325" class="label">normal-like query</text>')
    b.append('<circle cx="890" cy="250" r="16" fill="#a24d18"/><text x="910" y="245" class="label">abnormal-like query</text>')
    b.append('<path d="M330 330 L315 318" stroke="#2454d8" stroke-width="4" stroke-dasharray="6 5"/>')
    b.append('<path d="M890 250 L680 350" stroke="#a24d18" stroke-width="4" stroke-dasharray="8 6"/>')
    b.append('<text x="210" y="525" class="body">short nearest distance → low anomaly score</text>')
    b.append('<text x="720" y="525" class="body">long nearest distance → high anomaly score</text>')
    return _svg("Figure 4. Nearest-neighbor anomaly scoring",
                "test descriptor와 가장 가까운 정상 descriptor의 거리를 anomaly score로 사용합니다.", "".join(b), 660)


def _pc_heatmap():
    b=[]
    for p in [(35,120,340,480,"a","Input"),(405,120,340,480,"b","Patch anomaly scores"),(775,120,390,480,"c","Upsampled heatmap + overlay")]:
        b.append(_panel(*p))
    # pseudo industrial part
    for ox in [80,820]:
        b.append(f'<rect x="{ox}" y="200" width="240" height="280" rx="22" fill="#d8dfe7" stroke="#9ca9b8"/>')
        b.append(f'<rect x="{ox+45}" y="245" width="150" height="190" rx="18" fill="#adb8c5"/>')
        b.append(f'<circle cx="{ox+120}" cy="340" r="35" fill="#737f8d"/>')
    vals=[]
    for r in range(6):
        row=[]
        for c in range(6):
            d=abs(r-4)+abs(c-4)
            row.append(max(0,4-d))
        vals.append(row)
    b.append(_grid(455,205,6,6,43,"heat",vals))
    # overlay red hotspot
    b.append('<circle cx="1030" cy="415" r="55" fill="#e44b3b" opacity=".42"/>')
    b.append('<circle cx="1030" cy="415" r="28" fill="#a52a2a" opacity=".45"/>')
    b.append('<text x="80" y="555" class="small">원본 검사 이미지</text>')
    b.append('<text x="455" y="555" class="small">feature patch별 nearest-neighbor distance</text>')
    b.append('<text x="820" y="555" class="small">공간 위치로 복원하여 이상 위치를 표시</text>')
    return _svg("Figure 5. Patch scores → anomaly heatmap",
                "지역 feature score를 원래 공간에 다시 배치하면 결함 위치를 heatmap으로 표현할 수 있습니다.", "".join(b), 650)



def _pc_score_aggregation():
    b = []
    for p in [
        (35,120,520,500,"a","Patch-score distribution"),
        (605,120,560,500,"b","Operational decision (generic)"),
    ]:
        b.append(_panel(*p))
    vals = [28,42,58,82,110,145,120,82,48,22]
    for i, height in enumerate(vals):
        x = 90 + i * 40
        b.append(
            f'<rect x="{x}" y="{520-height}" width="28" height="{height}" '
            'rx="4" fill="#8eace7"/>'
        )
    b.append(
        '<rect x="420" y="260" width="28" height="260" rx="4" fill="#a24d18"/>'
    )
    b.append(
        '<text x="88" y="560" class="small">'
        '합성 patch-score 분포: 실제 PatchCore benchmark 결과가 아닙니다.</text>'
    )
    b.append('<path d="M670 500 H1095 M670 500 V200" class="thin"/>')
    b.append(
        '<path d="M690 470 C780 445 840 400 900 330 '
        'C970 250 1030 220 1080 210" '
        'stroke="#2454d8" stroke-width="5" fill="none"/>'
    )
    b.append(
        '<line x1="670" y1="330" x2="1095" y2="330" '
        'stroke="#a24d18" stroke-width="3" stroke-dasharray="10 7"/>'
    )
    b.append('<text x="930" y="315" class="body">example threshold</text>')
    b.append(
        '<text x="690" y="555" class="small">'
        '원 논문의 image-level scoring은 재가중 세부가 있으므로 구현을 별도 확인합니다.'
        '</text>'
    )
    return _svg(
        "Figure 6. Patch scores and an operational decision",
        "지역 score를 최종 판정에 연결하는 일반화된 흐름이며 원 논문 식을 대체하지 않습니다.",
        "".join(b),
        660,
    )


BUILDERS = {
    "cnn-paper-overview.svg": _cnn_overview,
    "cnn-paper-convolution.svg": _cnn_convolution,
    "cnn-paper-multichannel.svg": _cnn_multichannel,
    "cnn-paper-stride-padding.svg": _cnn_stride_padding,
    "cnn-paper-receptive-field.svg": _cnn_receptive,
    "cnn-paper-pooling.svg": _cnn_pooling,
    "vit-paper-overview.svg": _vit_overview,
    "vit-paper-patch-embedding.svg": _vit_patch_embedding,
    "vit-paper-cls-position.svg": _vit_cls_position,
    "vit-paper-attention.svg": _vit_attention,
    "vit-paper-multihead.svg": _vit_multihead,
    "vit-paper-attention-map.svg": _vit_attention_map,
    "patchcore-paper-overview.svg": _pc_overview,
    "patchcore-paper-features.svg": _pc_features,
    "patchcore-paper-coreset.svg": _pc_coreset,
    "patchcore-paper-nearest.svg": _pc_nearest,
    "patchcore-paper-heatmap.svg": _pc_heatmap,
    "patchcore-paper-score.svg": _pc_score_aggregation,
}

PAPER_FIGURE_META = {
    "cnn-paper-overview.svg": ("CNN overview", "입력에서 feature hierarchy와 prediction까지 한 화면에서 연결합니다."),
    "cnn-paper-convolution.svg": ("Convolution mechanics", "3×3 patch와 kernel의 곱셈-합산을 실제 숫자 grid로 보여줍니다."),
    "cnn-paper-multichannel.svg": ("Multi-channel convolution", "RGB channel별 response가 output channel로 합쳐지는 구조입니다."),
    "cnn-paper-stride-padding.svg": ("Stride and padding", "stride와 padding에 따른 sampling과 output 크기를 비교합니다."),
    "cnn-paper-receptive-field.svg": ("Receptive-field growth", "layer depth에 따라 입력에서 연결되는 공간 범위가 넓어지는 모습을 보여줍니다."),
    "cnn-paper-pooling.svg": ("Pooling", "max/average pooling의 수치 예와 의미를 비교합니다."),
    "vit-paper-overview.svg": ("Vision Transformer overview", "image에서 patch token을 거쳐 classification까지 이어지는 전체 과정입니다."),
    "vit-paper-patch-embedding.svg": ("Patch embedding", "patching, flatten, projection을 숫자/벡터 관점에서 연결합니다."),
    "vit-paper-cls-position.svg": ("CLS and position", "CLS token과 positional embedding이 sequence에 들어가는 방식을 보여줍니다."),
    "vit-paper-attention.svg": ("Self-attention", "Q/K/V, attention matrix, weighted value mixing을 한 figure로 연결합니다."),
    "vit-paper-multihead.svg": ("Multi-head attention", "여러 head가 서로 다른 token relation을 병렬로 표현하는 개념도입니다."),
    "vit-paper-attention-map.svg": ("Attention heatmap", "attention matrix를 image patch 위치에 대응한 heatmap으로 읽는 예시입니다."),
    "patchcore-paper-overview.svg": ("PatchCore overview", "정상 feature memory와 test nearest-neighbor distance를 연결합니다."),
    "patchcore-paper-features.svg": ("Local feature descriptors", "중간 CNN feature map에서 지역 descriptor가 만들어지는 과정을 보여줍니다."),
    "patchcore-paper-coreset.svg": ("Coreset selection", "전체 normal feature cloud와 representative subset을 scatter 형태로 비교합니다."),
    "patchcore-paper-nearest.svg": ("Nearest-neighbor scoring", "feature space에서 정상과 가까운 query, 먼 query의 거리 차이를 보여줍니다."),
    "patchcore-paper-heatmap.svg": ("Anomaly heatmap", "patch score가 spatial heatmap과 overlay로 변환되는 과정을 보여줍니다."),
    "patchcore-paper-score.svg": ("Image-level score", "patch-score distribution을 image-level decision으로 연결하는 개념입니다."),
}

def build_paper_figures(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, builder in BUILDERS.items():
        (output_dir / name).write_text(builder(), encoding="utf-8")
    return len(BUILDERS)

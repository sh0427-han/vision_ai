"""Generate paper-style visual atlases for CS231n and Bishop PRML notes."""

from html import escape
from pathlib import Path


def _e(value):
    return escape(str(value))


def _svg(title, subtitle, body, height=620):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" role="img" aria-label="{_e(title)}">
<style>
.title{{font:700 27px Arial,'Noto Sans KR',sans-serif;fill:#18243b}}
.subtitle{{font:18px Arial,'Noto Sans KR',sans-serif;fill:#5b6880}}
.panel-label{{font:700 18px Arial,'Noto Sans KR',sans-serif;fill:#18243b}}
.label{{font:700 17px Arial,'Noto Sans KR',sans-serif;fill:#203455}}
.body{{font:15px Arial,'Noto Sans KR',sans-serif;fill:#526178}}
.small{{font:13px Arial,'Noto Sans KR',sans-serif;fill:#68768c}}
.white{{font:700 15px Arial,'Noto Sans KR',sans-serif;fill:#fff}}
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


def _panel_frame(x, y, w, h, letter, title):
    title_size = 17 if len(title) <= 24 else 15 if len(title) <= 34 else 13
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="panel"/>'
        f'<text x="{x+16}" y="{y+29}" class="panel-label">({letter})</text>'
        f'<text x="{x+52}" y="{y+29}" font-size="{title_size}" '
        f'font-weight="700" fill="#203455">{_e(title)}</text>'
    )


def _arrow(x1, y1, x2, y2):
    return (
        f'<path d="M{x1} {y1} L{x2} {y2}" class="line"/>'
        f'<polygon points="{x2},{y2} {x2-13},{y2-8} {x2-13},{y2+8}" fill="#7e91af"/>'
    )


def _grid(x, y, rows, cols, cell=27, mode="blue", hot=None):
    palettes = {
        "blue": ["#f0f4fb", "#dce7fa", "#bcd1f6", "#7fa4ec", "#2f63d8"],
        "heat": ["#fff4e8", "#ffd9b3", "#f5a45e", "#db6945", "#a52a2a"],
        "gray": ["#f4f5f7", "#d9dee6", "#adb7c5", "#768397", "#344156"],
        "green": ["#eff8f5", "#d5eee6", "#afe0d2", "#6fc0aa", "#08796f"],
    }
    hot = set(hot or [])
    parts = []
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            value = 4 if idx in hot else ((r * 3 + c * 5 + r * c) % 4)
            parts.append(
                f'<rect x="{x+c*cell}" y="{y+r*cell}" width="{cell-3}" height="{cell-3}" rx="4" '
                f'fill="{palettes[mode][value]}" stroke="#d5deeb"/>'
            )
    return "".join(parts)


def _scatter(x, y, w, h, boundary="linear", query=False, margin=False):
    body = [
        f'<path d="M{x+25} {y+h-30} H{x+w-20} M{x+25} {y+h-30} V{y+35}" class="thin"/>'
    ]
    a = [(0.18,0.72),(0.28,0.60),(0.34,0.76),(0.22,0.45),(0.42,0.55)]
    b = [(0.62,0.30),(0.72,0.42),(0.77,0.24),(0.66,0.58),(0.84,0.48)]
    for px, py in a:
        body.append(f'<circle cx="{x+px*w}" cy="{y+py*h}" r="8" fill="#2454d8"/>')
    for px, py in b:
        body.append(f'<circle cx="{x+px*w}" cy="{y+py*h}" r="8" fill="#08796f"/>')
    if boundary == "linear":
        body.append(f'<path d="M{x+w*0.50} {y+35} L{x+w*0.50} {y+h-30}" stroke="#a24d18" stroke-width="4"/>')
        if margin:
            body.append(f'<path d="M{x+w*0.43} {y+35} L{x+w*0.43} {y+h-30} M{x+w*0.57} {y+35} L{x+w*0.57} {y+h-30}" stroke="#89a9ec" stroke-width="3" stroke-dasharray="8 6"/>')
    else:
        body.append(f'<path d="M{x+40} {y+h-55} C{x+w*.28} {y+20} {x+w*.63} {y+h-15} {x+w-35} {y+55}" stroke="#a24d18" stroke-width="4" fill="none"/>')
    if query:
        qx, qy = x+w*.46, y+h*.44
        body.append(f'<circle cx="{qx}" cy="{qy}" r="12" fill="#a24d18"/>')
        for px,py in [a[1],a[4],b[3]]:
            body.append(f'<path d="M{qx} {qy} L{x+px*w} {y+py*h}" stroke="#a24d18" stroke-width="2" stroke-dasharray="5 5"/>')
    return "".join(body)


def _pipeline(x, y, w, h, steps):
    n = len(steps)
    gap = 18
    bw = (w - 35 - gap*(n-1)) / n
    parts = []
    for i, step in enumerate(steps):
        bx = x + 18 + i*(bw+gap)
        fill = "#2454d8" if i == len(steps)-1 else "#edf3ff"
        stroke = "#2454d8" if i == len(steps)-1 else "#9bb5e5"
        txt = "#fff" if i == len(steps)-1 else "#203455"
        parts.append(f'<rect x="{bx}" y="{y+h*.42}" width="{bw}" height="64" rx="11" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        parts.append(f'<text x="{bx+bw/2}" y="{y+h*.42+28}" text-anchor="middle" font-size="14" font-weight="700" fill="{txt}">{_e(step)}</text>')
        if i < n-1:
            parts.append(_arrow(bx+bw, y+h*.42+32, bx+bw+gap-3, y+h*.42+32))
    return "".join(parts)


def _bars(x, y, w, h, labels, values, horizontal=True):
    parts = []
    maxv = max(values) if values else 1
    if horizontal:
        for i,(label,value) in enumerate(zip(labels,values)):
            yy = y+55+i*42
            bw = (w-160) * value / maxv
            parts.append(f'<text x="{x+20}" y="{yy+16}" class="small">{_e(label)}</text>')
            parts.append(f'<rect x="{x+120}" y="{yy}" width="{bw}" height="22" rx="6" fill="{"#2454d8" if i==0 else "#91abe2"}"/>')
    else:
        base = y+h-40
        step = (w-60)/len(values)
        for i,(label,value) in enumerate(zip(labels,values)):
            bh = (h-100)*value/maxv
            xx = x+30+i*step
            parts.append(f'<rect x="{xx}" y="{base-bh}" width="{step*.55}" height="{bh}" rx="5" fill="{"#2454d8" if i%2==0 else "#89a9ec"}"/>')
            parts.append(f'<text x="{xx+step*.27}" y="{base+20}" text-anchor="middle" class="small">{_e(label)}</text>')
    return "".join(parts)


def _curves(x, y, w, h, kind):
    axes = f'<path d="M{x+35} {y+h-35} H{x+w-20} M{x+35} {y+h-35} V{y+35}" class="thin"/>'
    paths = {
        "softmax_loss": [
            ("#2454d8", f'M{x+45} {y+h-55} C{x+w*.35} {y+h-65} {x+w*.55} {y+80} {x+w-35} {y+50}', "p(correct)"),
            ("#a24d18", f'M{x+45} {y+55} C{x+w*.35} {y+80} {x+w*.55} {y+h-75} {x+w-35} {y+h-55}', "−log p"),
        ],
        "activations": [
            ("#2454d8", f'M{x+45} {y+h-55} L{x+w*.48} {y+h-55} L{x+w-40} {y+50}', "ReLU"),
            ("#6d7f9b", f'M{x+45} {y+h-70} L{x+w*.48} {y+h-55} L{x+w-40} {y+65}', "Leaky ReLU"),
            ("#08796f", f'M{x+45} {y+h-70} C{x+w*.35} {y+h-70} {x+w*.48} {y+70} {x+w-40} {y+65}', "sigmoid"),
            ("#a24d18", f'M{x+45} {y+h-85} C{x+w*.35} {y+h-120} {x+w*.60} {y+85} {x+w-40} {y+55}', "tanh"),
        ],
        "train_val": [
            ("#2454d8", f'M{x+45} {y+70} C{x+w*.28} {y+120} {x+w*.48} {y+h-80} {x+w-35} {y+h-65}', "train loss"),
            ("#a24d18", f'M{x+45} {y+80} C{x+w*.30} {y+125} {x+w*.52} {y+h-105} {x+w-35} {y+h-140}', "val loss"),
        ],
        "bias_variance": [
            ("#2454d8", f'M{x+45} {y+70} C{x+w*.35} {y+90} {x+w*.62} {y+h-80} {x+w-35} {y+h-55}', "bias²"),
            ("#a24d18", f'M{x+45} {y+h-55} C{x+w*.35} {y+h-85} {x+w*.62} {y+90} {x+w-35} {y+65}', "variance"),
            ("#08796f", f'M{x+45} {y+90} C{x+w*.30} {y+h-85} {x+w*.58} {y+h-85} {x+w-35} {y+95}', "total"),
        ],
        "sigmoid": [
            ("#2454d8", f'M{x+45} {y+h-55} C{x+w*.30} {y+h-55} {x+w*.55} {y+55} {x+w-35} {y+55}', "σ(a)"),
        ],
        "gaussian": [
            ("#2454d8", f'M{x+45} {y+h-50} C{x+w*.25} {y+h-50} {x+w*.35} {y+55} {x+w*.50} {y+55} C{x+w*.65} {y+55} {x+w*.75} {y+h-50} {x+w-35} {y+h-50}', "small σ"),
            ("#a24d18", f'M{x+45} {y+h-50} C{x+w*.18} {y+h-55} {x+w*.30} {y+115} {x+w*.50} {y+115} C{x+w*.70} {y+115} {x+w*.82} {y+h-55} {x+w-35} {y+h-50}', "large σ"),
            ("#08796f", f'M{x+45} {y+h-50} C{x+w*.38} {y+h-50} {x+w*.48} {y+85} {x+w*.64} {y+85} C{x+w*.78} {y+85} {x+w*.85} {y+h-50} {x+w-35} {y+h-50}', "shifted μ"),
        ],
        "regression": [
            ("#2454d8", f'M{x+45} {y+h-60} L{x+w-40} {y+60}', "fit"),
        ],
        "regularization": [
            ("#2454d8", f'M{x+45} {y+h-70} C{x+w*.30} {y+55} {x+w*.48} {y+h-65} {x+w-35} {y+80}', "no reg"),
            ("#08796f", f'M{x+45} {y+h-75} C{x+w*.30} {y+125} {x+w*.58} {y+105} {x+w-35} {y+80}', "regularized"),
        ],
    }
    parts = [axes]
    for i,(color,path,label) in enumerate(paths[kind]):
        parts.append(f'<path d="{path}" stroke="{color}" stroke-width="4" fill="none"/>')
        parts.append(f'<text x="{x+w-135}" y="{y+55+i*24}" font-size="13" font-weight="700" fill="{color}">{_e(label)}</text>')
    return "".join(parts)


def _network(x, y, w, h, counts=(3,4,2), dropout=False):
    parts = []
    xs = [x+60+i*(w-120)/(len(counts)-1) for i in range(len(counts))]
    positions = []
    for li,count in enumerate(counts):
        ys = [y+70+j*(h-120)/(max(count-1,1)) for j in range(count)]
        positions.append([(xs[li], yy) for yy in ys])
    for li in range(len(counts)-1):
        for a in positions[li]:
            for b in positions[li+1]:
                parts.append(f'<path d="M{a[0]+11} {a[1]} L{b[0]-11} {b[1]}" stroke="#b8c4d5" stroke-width="1.5"/>')
    for li,layer in enumerate(positions):
        for ni,(cx,cy) in enumerate(layer):
            masked = dropout and li==1 and ni%2==1
            fill = "#e6e9ee" if masked else ("#2454d8" if li==len(positions)-1 else "#dce7fa")
            stroke = "#b7c2d3" if masked else "#89a9ec"
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            if masked:
                parts.append(f'<path d="M{cx-8} {cy-8} L{cx+8} {cy+8} M{cx+8} {cy-8} L{cx-8} {cy+8}" stroke="#8c98aa" stroke-width="2"/>')
    return "".join(parts)


def _heatmap(x, y, w, h):
    rows=6; cols=8; cell=min((w-50)/cols,(h-70)/rows)
    hot=[20,21,28,29,30,37,38]
    return _grid(x+25,y+45,rows,cols,cell,"heat",hot)


def _task_panel(x, y, w, h, mode):
    parts = [f'<rect x="{x+45}" y="{y+60}" width="{w-90}" height="{h-105}" rx="14" fill="#e6ebf1" stroke="#aab6c5"/>',
             f'<ellipse cx="{x+w*.50}" cy="{y+h*.56}" rx="{w*.18}" ry="{h*.19}" fill="#efba78" stroke="#c98540" stroke-width="2"/>']
    if mode=="classification":
        parts.append(f'<rect x="{x+w*.34}" y="{y+h*.76}" width="{w*.32}" height="30" rx="8" class="blue"/><text x="{x+w*.50}" y="{y+h*.76+20}" text-anchor="middle" class="body">class: cat</text>')
    elif mode=="detection":
        parts.append(f'<rect x="{x+w*.30}" y="{y+h*.35}" width="{w*.40}" height="{h*.42}" fill="none" stroke="#2454d8" stroke-width="4"/>')
    elif mode=="segmentation":
        parts.append(f'<ellipse cx="{x+w*.50}" cy="{y+h*.56}" rx="{w*.20}" ry="{h*.21}" fill="#2454d8" opacity=".38"/>')
    elif mode=="instance":
        parts.append(f'<ellipse cx="{x+w*.42}" cy="{y+h*.56}" rx="{w*.12}" ry="{h*.18}" fill="#2454d8" opacity=".42"/><ellipse cx="{x+w*.60}" cy="{y+h*.56}" rx="{w*.12}" ry="{h*.18}" fill="#08796f" opacity=".42"/>')
    return "".join(parts)



def _distribution(x, y, w, h, mode="gaussian"):
    parts = [f'<path d="M{x+35} {y+h-35} H{x+w-20}" class="thin"/>']
    if mode == "gaussian":
        parts.append(
            f'<path d="M{x+45} {y+h-40} C{x+w*.28} {y+h-40} '
            f'{x+w*.34} {y+55} {x+w*.50} {y+55} '
            f'C{x+w*.66} {y+55} {x+w*.72} {y+h-40} {x+w-35} {y+h-40}" '
            'stroke="#2454d8" stroke-width="4" fill="none"/>'
        )
    elif mode == "mixture":
        base = y + h - 40
        parts.extend([
            f'<path d="M{x+45} {base} C{x+w*.18} {base} {x+w*.24} {y+92} '
            f'{x+w*.34} {y+92} C{x+w*.44} {y+92} {x+w*.48} {base} '
            f'{x+w*.58} {base}" stroke="#2454d8" stroke-width="3" fill="none"/>',
            f'<path d="M{x+w*.36} {base} C{x+w*.52} {base} {x+w*.58} {y+122} '
            f'{x+w*.70} {y+122} C{x+w*.82} {y+122} {x+w*.86} {base} '
            f'{x+w-35} {base}" stroke="#08796f" stroke-width="3" fill="none"/>',
            f'<path d="M{x+45} {base} C{x+w*.18} {base} {x+w*.24} {y+105} '
            f'{x+w*.34} {y+105} C{x+w*.45} {y+105} {x+w*.50} {y+155} '
            f'{x+w*.58} {y+142} C{x+w*.64} {y+126} {x+w*.66} {y+112} '
            f'{x+w*.70} {y+112} C{x+w*.82} {y+112} {x+w*.87} {base} '
            f'{x+w-35} {base}" stroke="#7f5fbf" stroke-width="5" fill="none"/>',
            f'<text x="{x+20}" y="{y+42}" class="small" fill="#2454d8">π₁N₁(x)</text>',
            f'<text x="{x+98}" y="{y+42}" class="small" fill="#08796f">π₂N₂(x)</text>',
            f'<text x="{x+178}" y="{y+42}" class="small" fill="#7f5fbf">sum p(x)</text>',
        ])
    elif mode == "beta":
        parts.extend([
            f'<path d="M{x+45} {y+h-40} C{x+w*.20} {y+120} '
            f'{x+w*.37} {y+70} {x+w*.52} {y+95} '
            f'C{x+w*.65} {y+120} {x+w*.78} {y+h-45} {x+w-35} {y+h-40}" '
            'stroke="#2454d8" stroke-width="4" fill="none"/>',
            f'<path d="M{x+45} {y+h-40} C{x+w*.25} {y+h-35} '
            f'{x+w*.40} {y+145} {x+w*.58} {y+75} '
            f'C{x+w*.72} {y+55} {x+w*.83} {y+h-35} {x+w-35} {y+h-40}" '
            'stroke="#a24d18" stroke-width="4" fill="none"/>',
            f'<text x="{x+20}" y="{y+42}" class="small" fill="#2454d8">prior</text>',
            f'<text x="{x+82}" y="{y+42}" class="small" fill="#a24d18">posterior after data</text>',
            f'<text x="{x+20}" y="{y+h-18}" class="small">Beta(a,b) + m successes + ℓ failures → Beta(a+m,b+ℓ)</text>',
        ])
    return "".join(parts)

def _graphical(x, y, w, h, undirected=False):
    pts=[(x+w*.22,y+h*.38),(x+w*.50,y+h*.23),(x+w*.50,y+h*.63),(x+w*.80,y+h*.42)]
    parts=[]
    edges=[(0,1),(0,2),(1,3),(2,3)]
    for a,b in edges:
        if undirected:
            parts.append(f'<path d="M{pts[a][0]} {pts[a][1]} L{pts[b][0]} {pts[b][1]}" class="line"/>')
        else:
            parts.append(_arrow(pts[a][0]+15,pts[a][1],pts[b][0]-15,pts[b][1]))
    for i,(cx,cy) in enumerate(pts):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="{"#e9f7f2" if i==3 else "#edf3ff"}" stroke="#89a9ec" stroke-width="2"/>')
        parts.append(f'<text x="{cx}" y="{cy+6}" text-anchor="middle" class="label">x{i+1}</text>')
    return "".join(parts)



def _pca(x, y, w, h):
    """Display orthogonal principal axes through the sample mean."""
    parts = [
        f'<path d="M{x+35} {y+h-35} H{x+w-20} M{x+35} {y+h-35} V{y+35}" '
        'class="thin"/>'
    ]
    pts = [
        (.18,.72),(.27,.65),(.35,.60),(.43,.53),(.50,.47),
        (.59,.42),(.68,.35),(.77,.28),(.83,.25)
    ]
    for px, py in pts:
        parts.append(
            f'<circle cx="{x+px*w}" cy="{y+py*h}" r="7" fill="#2454d8"/>'
        )

    cx = x + w * 0.51
    cy = y + h * 0.49
    dx = w * 0.40
    dy = -h * 0.25
    parts.append(
        f'<path d="M{cx-dx} {cy-dy} L{cx+dx} {cy+dy}" '
        'stroke="#a24d18" stroke-width="4"/>'
    )
    # Perpendicular direction to (dx, dy), scaled down.
    scale = 0.42
    pdx = -dy * scale
    pdy = dx * scale
    parts.append(
        f'<path d="M{cx-pdx} {cy-pdy} L{cx+pdx} {cy+pdy}" '
        'stroke="#08796f" stroke-width="3"/>'
    )
    parts.append(
        f'<text x="{x+18}" y="{y+35}" class="small">'
        "PC1 and PC2 are orthogonal eigenvector directions</text>"
    )
    return "".join(parts)

def _hmm(x, y, w, h):
    parts=[]
    xs=[x+80,x+w*.50,x+w-80]
    for i,cx in enumerate(xs):
        parts.append(f'<circle cx="{cx}" cy="{y+100}" r="28" fill="#edf3ff" stroke="#89a9ec" stroke-width="2"/>')
        parts.append(f'<text x="{cx}" y="{y+106}" text-anchor="middle" class="label">z{i+1}</text>')
        parts.append(f'<circle cx="{cx}" cy="{y+h-75}" r="25" fill="#e9f7f2" stroke="#8ccdbb" stroke-width="2"/>')
        parts.append(f'<text x="{cx}" y="{y+h-69}" text-anchor="middle" class="label">x{i+1}</text>')
        parts.append(_arrow(cx,y+128,cx,y+h-102))
        if i<len(xs)-1:
            parts.append(_arrow(cx+30,y+100,xs[i+1]-30,y+100))
    return "".join(parts)



def _value_grid(x, y, values, cell=32, fill="#f4f7fb"):
    parts = []
    for row_idx, row in enumerate(values):
        for col_idx, value in enumerate(row):
            xx = x + col_idx * cell
            yy = y + row_idx * cell
            parts.append(
                f'<rect x="{xx}" y="{yy}" width="{cell-3}" height="{cell-3}" '
                f'rx="4" fill="{fill}" stroke="#cbd6e6"/>'
            )
            parts.append(
                f'<text x="{xx+(cell-3)/2}" y="{yy+(cell-3)/2+5}" '
                f'text-anchor="middle" class="small">{_e(value)}</text>'
            )
    return "".join(parts)


def _knn_semantics(x, y, w, h):
    parts = [
        f'<text x="{x+20}" y="{y+45}" class="label">same class</text>',
        f'<text x="{x+20}" y="{y+205}" class="label">different class</text>',
    ]
    patterns = [
        ([6, 7, 11, 12, 16, 17], [7, 8, 12, 13, 17, 18]),
        ([6, 8, 12, 16, 18], [6, 7, 12, 17, 18]),
    ]
    row_y = [y + 65, y + 225]
    for idx, (left_hot, right_hot) in enumerate(patterns):
        yy = row_y[idx]
        parts.append(_grid(x + 35, yy, 5, 5, 22, "gray", left_hot))
        parts.append(_arrow(x + 160, yy + 52, x + 210, yy + 52))
        parts.append(_grid(x + 225, yy, 5, 5, 22, "gray", right_hot))
        label = "pixel distance: large" if idx == 0 else "pixel distance: small"
        color = "#a24d18" if idx == 0 else "#08796f"
        parts.append(
            f'<text x="{x+365}" y="{yy+58}" class="body" fill="{color}">'
            f'{_e(label)}</text>'
        )
    parts.append(
        f'<text x="{x+20}" y="{y+h-18}" class="small">'
        "raw pixels measure appearance, not semantic identity</text>"
    )
    return "".join(parts)


def _grouped_split(x, y, w, h):
    parts = [
        f'<text x="{x+18}" y="{y+45}" class="label">random frame split</text>',
        f'<text x="{x+18}" y="{y+205}" class="label">grouped split</text>',
    ]
    colors = ["#8faee8", "#8ccdbb", "#e0ae82"]
    labels = ["train", "val", "test"]
    for idx, (color, label) in enumerate(zip(colors, labels)):
        lx = x + 260 + idx * 75
        parts.append(f'<rect x="{lx}" y="{y+25}" width="16" height="16" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{lx+22}" y="{y+38}" class="small">{label}</text>')
    group_w = (w - 70) / 4
    for group_idx in range(4):
        gx = x + 20 + group_idx * group_w
        parts.append(
            f'<rect x="{gx}" y="{y+62}" width="{group_w-12}" height="92" '
            'rx="10" fill="#f8fafc" stroke="#d4deeb"/>'
        )
        parts.append(
            f'<text x="{gx+8}" y="{y+82}" class="small">video {group_idx+1}</text>'
        )
        for frame_idx in range(6):
            color = colors[(frame_idx + group_idx) % 3]
            parts.append(
                f'<rect x="{gx+8+frame_idx*15}" y="{y+98}" width="11" height="34" '
                f'rx="2" fill="{color}"/>'
            )
    parts.append(
        f'<text x="{x+w-165}" y="{y+170}" class="small" fill="#a24d18">'
        "near-duplicate leak</text>"
    )
    for group_idx in range(4):
        gx = x + 20 + group_idx * group_w
        color = colors[min(group_idx, 2)]
        parts.append(
            f'<rect x="{gx}" y="{y+222}" width="{group_w-12}" height="92" '
            f'rx="10" fill="{color}" opacity=".18" stroke="{color}"/>'
        )
        parts.append(
            f'<text x="{gx+8}" y="{y+242}" class="small">video {group_idx+1}</text>'
        )
        for frame_idx in range(6):
            parts.append(
                f'<rect x="{gx+8+frame_idx*15}" y="{y+258}" width="11" height="34" '
                f'rx="2" fill="{color}"/>'
            )
    parts.append(
        f'<text x="{x+w-165}" y="{y+332}" class="small" fill="#08796f">'
        "source stays isolated</text>"
    )
    return "".join(parts)


def _score_softmax_ce(x, y, w, h):
    parts = []
    columns = [
        (x + 18, "scores", [2.0, 1.0, 0.1]),
        (x + w * 0.38, "softmax", [0.659, 0.242, 0.099]),
    ]
    names = ["cat", "dog", "car"]
    for column_x, heading, values in columns:
        parts.append(f'<text x="{column_x}" y="{y+48}" class="label">{heading}</text>')
        max_value = max(values)
        for idx, (name, value) in enumerate(zip(names, values)):
            yy = y + 72 + idx * 55
            parts.append(f'<text x="{column_x}" y="{yy+16}" class="small">{name}</text>')
            bar_w = 95 * value / max_value
            parts.append(
                f'<rect x="{column_x+38}" y="{yy}" width="{bar_w}" height="22" '
                f'rx="5" fill="{"#2454d8" if idx == 0 else "#a9bce5"}"/>'
            )
            parts.append(
                f'<text x="{column_x+142}" y="{yy+16}" class="small">'
                f'{value:.3g}</text>'
            )
    parts.append(_arrow(x + w * 0.31, y + 148, x + w * 0.36, y + 148))
    parts.append(_arrow(x + w * 0.69, y + 148, x + w * 0.74, y + 148))
    loss_x = x + w * 0.77
    parts.append(f'<text x="{loss_x}" y="{y+48}" class="label">cross-entropy</text>')
    parts.append(
        f'<rect x="{loss_x}" y="{y+92}" width="{w*0.20}" height="86" rx="12" '
        'fill="#fff1e7" stroke="#e0ae82"/>'
    )
    parts.append(f'<text x="{loss_x+14}" y="{y+122}" class="body">−log(0.659)</text>')
    parts.append(f'<text x="{loss_x+14}" y="{y+154}" class="label">≈ 0.417</text>')
    parts.append(
        f'<text x="{x+18}" y="{y+h-25}" class="small">'
        "logits → normalized probability → penalty for the correct class</text>"
    )
    return "".join(parts)



def _loss_compare(x, y, w, h):
    """Keep cross-entropy and hinge loss on their own correct x-axes."""
    parts = []
    half = w / 2

    # Cross-entropy: -log p_y for p_y in (0, 1].
    lx = x + 32
    rx = x + half - 18
    top = y + 62
    bottom = y + h - 52
    parts.append(f'<text x="{x+18}" y="{y+40}" class="label">cross-entropy</text>')
    parts.append(
        f'<path d="M{lx} {bottom} H{rx} M{lx} {bottom} V{top}" class="thin"/>'
    )
    parts.append(
        f'<path d="M{lx+5} {top+8} C{x+half*.25} {top+45} '
        f'{x+half*.55} {bottom-45} {rx-5} {bottom-6}" '
        'stroke="#2454d8" stroke-width="4" fill="none"/>'
    )
    parts.append(
        f'<text x="{lx+4}" y="{bottom+22}" class="small">pᵧ→0</text>'
    )
    parts.append(
        f'<text x="{rx-38}" y="{bottom+22}" class="small">pᵧ=1</text>'
    )
    parts.append(
        f'<text x="{x+18}" y="{top-10}" class="small">−log pᵧ</text>'
    )

    # Hinge: max(0, 1-m), m=yf(x).
    ox = x + half + 25
    oright = x + w - 20
    margin_x = ox + (oright - ox) * 0.66
    parts.append(
        f'<text x="{x+half+12}" y="{y+40}" class="label">hinge</text>'
    )
    parts.append(
        f'<path d="M{ox} {bottom} H{oright} M{ox} {bottom} V{top}" class="thin"/>'
    )
    parts.append(
        f'<path d="M{ox+3} {top+18} L{margin_x} {bottom} H{oright}" '
        'stroke="#a24d18" stroke-width="4" fill="none"/>'
    )
    parts.append(
        f'<path d="M{margin_x} {top} V{bottom}" stroke="#9aa9be" '
        'stroke-width="2" stroke-dasharray="5 5"/>'
    )
    parts.append(
        f'<text x="{margin_x+5}" y="{bottom-10}" class="small">m=1</text>'
    )
    parts.append(
        f'<text x="{oright-90}" y="{bottom+22}" class="small">m=yf(x) →</text>'
    )
    return "".join(parts)

def _activation_gradients(x, y, w, h):
    half = w / 2
    parts = []
    for panel_idx, title in enumerate(["saturating units", "ReLU family"]):
        px = x + panel_idx * half
        left = px + 30
        right = px + half - 18
        top = y + 58
        bottom = y + h - 42
        parts.append(f'<text x="{px+18}" y="{y+40}" class="label">{title}</text>')
        parts.append(
            f'<path d="M{left} {bottom} H{right} M{left} {bottom} V{top}" class="thin"/>'
        )
        if panel_idx == 0:
            parts.append(
                f'<path d="M{left+5} {bottom-8} C{px+half*.34} {bottom-8} '
                f'{px+half*.46} {top+25} {px+half*.56} {top+25} '
                f'C{px+half*.69} {top+25} {right-8} {top+18} {right-5} {top+18}" '
                'stroke="#2454d8" stroke-width="4" fill="none"/>'
            )
            parts.append(
                f'<rect x="{left}" y="{top}" width="{half*.22}" height="{bottom-top}" '
                'fill="#fff1e7" opacity=".55"/>'
            )
            parts.append(
                f'<rect x="{right-half*.22}" y="{top}" width="{half*.22}" '
                f'height="{bottom-top}" fill="#fff1e7" opacity=".55"/>'
            )
            parts.append(f'<text x="{left+5}" y="{bottom-12}" class="small">|grad|≈0</text>')
        else:
            zero_y = bottom - (bottom - top) * 0.48
            mid = px + half * 0.52
            parts.append(
                f'<path d="M{left+5} {zero_y} L{mid} {zero_y} L{right-5} {top+25}" '
                'stroke="#08796f" stroke-width="4" fill="none"/>'
            )
            parts.append(
                f'<path d="M{left+5} {zero_y+25} L{mid} {zero_y} " '
                'stroke="#a24d18" stroke-width="3" fill="none"/>'
            )
            parts.append(f'<text x="{right-76}" y="{top+20}" class="small">grad≈1</text>')
    return "".join(parts)



def _batchnorm_modes(x, y, w, h):
    """BatchNorm train/eval statistics and running-stat updates."""
    parts = []
    rows = [
        (y + 78, "train", "batch μB, σB²", "#2454d8"),
        (y + 228, "eval", "running μ, σ²", "#08796f"),
    ]
    for yy, mode, stats, color in rows:
        parts.append(f'<text x="{x+18}" y="{yy-22}" class="label">{mode}</text>')
        for idx in range(4):
            parts.append(
                f'<circle cx="{x+62+idx*24}" cy="{yy+28}" r="9" '
                f'fill="{color}" opacity="{0.45+idx*0.12}"/>'
            )
        parts.append(_arrow(x + 150, yy + 28, x + 195, yy + 28))
        parts.append(
            f'<rect x="{x+205}" y="{yy-3}" width="128" height="62" rx="10" '
            'fill="#f3f7fe" stroke="#c9d6ea"/>'
        )
        parts.append(
            f'<text x="{x+269}" y="{yy+33}" text-anchor="middle" class="small">'
            f'{stats}</text>'
        )
        parts.append(_arrow(x + 338, yy + 28, x + 378, yy + 28))
        parts.append(
            f'<rect x="{x+386}" y="{yy-3}" width="112" height="62" rx="10" '
            'fill="#e9f7f2" stroke="#8ccdbb"/>'
        )
        parts.append(
            f'<text x="{x+442}" y="{yy+22}" text-anchor="middle" class="small">'
            "normalize</text>"
        )
        parts.append(
            f'<text x="{x+442}" y="{yy+43}" text-anchor="middle" class="small">'
            "γ, β</text>"
        )
    parts.append(
        f'<text x="{x+18}" y="{y+182}" class="small" fill="#6d7f9b">'
        "train also updates running statistics</text>"
    )
    return "".join(parts)

def _augmentation_cards(x, y, w, h):
    parts = []
    labels = ["crop", "flip", "color", "rotate"]
    positions = [
        (x + 20, y + 58),
        (x + w/2 + 4, y + 58),
        (x + 20, y + 205),
        (x + w/2 + 4, y + 205),
    ]
    card_w = w / 2 - 28
    card_h = 112
    for idx, ((px, py), label) in enumerate(zip(positions, labels)):
        parts.append(
            f'<rect x="{px}" y="{py}" width="{card_w}" height="{card_h}" rx="12" '
            'fill="#eef2f6" stroke="#cbd5e2"/>'
        )
        parts.append(f'<text x="{px+12}" y="{py+22}" class="small">{label}</text>')
        opacity = 0.58 if label == "color" else 0.92
        cx = px + card_w * (0.43 if label == "crop" else 0.52)
        if label == "flip":
            cx = px + card_w * 0.66
        transform = (
            f' transform="rotate(18 {cx} {py+68})"' if label == "rotate" else ""
        )
        parts.append(
            f'<rect x="{cx-35}" y="{py+43}" width="70" height="46" rx="10" '
            f'fill="#2454d8" opacity="{opacity}"{transform}/>'
        )
        parts.append(
            f'<circle cx="{cx+18}" cy="{py+58}" r="7" fill="#fff" opacity=".9"/>'
        )
        if label == "crop":
            parts.append(
                f'<path d="M{px+18} {py+40} V{py+90} M{px+18} {py+40} H{px+70}" '
                'stroke="#a24d18" stroke-width="3"/>'
            )
    return "".join(parts)



def _invariance_checks(x, y, w, h):
    """Show that augmentation validity depends on the task semantics."""
    checks = [
        ("crop", "valid only if target remains visible", "#e9f7f2", "#08796f"),
        ("horizontal flip", "valid only for left-right invariant labels", "#e9f7f2", "#08796f"),
        ("strong color shift", "task-dependent", "#fff7e9", "#a24d18"),
        ("geometry-destroying warp", "usually changes semantics", "#fff1e7", "#a24d18"),
    ]
    parts = []
    for idx, (label, note, fill, color) in enumerate(checks):
        yy = y + 63 + idx * 76
        parts.append(
            f'<rect x="{x+24}" y="{yy-25}" width="{w-48}" height="56" rx="10" '
            f'fill="{fill}" stroke="{color}" stroke-opacity=".45"/>'
        )
        parts.append(
            f'<text x="{x+42}" y="{yy-2}" class="body">{_e(label)}</text>'
        )
        parts.append(
            f'<text x="{x+42}" y="{yy+19}" class="small">{_e(note)}</text>'
        )
    return "".join(parts)

def _numeric_conv(x, y, w, h):
    input_values = [
        [1, 2, 0, 1],
        [0, 1, 3, 1],
        [2, 1, 0, 2],
        [1, 0, 2, 1],
    ]
    kernel_values = [
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1],
    ]
    parts = [
        f'<text x="{x+22}" y="{y+47}" class="small">input patch</text>',
        f'<text x="{x+218}" y="{y+47}" class="small">3×3 kernel</text>',
    ]
    parts.append(_value_grid(x + 20, y + 65, input_values, 38))
    parts.append(
        f'<rect x="{x+18}" y="{y+63}" width="{38*3}" height="{38*3}" '
        'fill="none" stroke="#2454d8" stroke-width="3"/>'
    )
    parts.append(_value_grid(x + 215, y + 75, kernel_values, 38, "#e9f7f2"))
    parts.append(_arrow(x + 345, y + 132, x + 388, y + 132))
    parts.append(
        f'<rect x="{x+398}" y="{y+91}" width="104" height="82" rx="12" '
        'fill="#edf3ff" stroke="#8faee8"/>'
    )
    parts.append(f'<text x="{x+450}" y="{y+121}" text-anchor="middle" class="small">dot sum</text>')
    parts.append(f'<text x="{x+450}" y="{y+151}" text-anchor="middle" class="label">0</text>')
    parts.append(
        f'<text x="{x+20}" y="{y+h-36}" class="small">'
        "(1+0+0) + (0+0−3) + (2+0+0) = 0</text>"
    )
    return "".join(parts)



def _conv_controls(x, y, w, h):
    """Accurate stride, padding and dilation sketches for a 3×3 kernel."""
    parts = []
    cards = [
        ("stride 1", "5×5 → 3×3", [0, 1, 5, 6], "#2454d8"),
        ("stride 2", "5×5 → 2×2", [0, 2, 10, 12], "#08796f"),
        ("P=1, S=1", "5×5 → 5×5", [0, 1, 5, 6], "#6d7f9b"),
        ("dilation 2", "effective field 5×5", [0, 2, 4, 10, 12, 14, 20, 22, 24], "#a24d18"),
    ]
    positions = [
        (x + 14, y + 55),
        (x + w/2 + 4, y + 55),
        (x + 14, y + 215),
        (x + w/2 + 4, y + 215),
    ]
    card_w = w / 2 - 20
    for (title, note, hot, color), (px, py) in zip(cards, positions):
        parts.append(
            f'<rect x="{px}" y="{py}" width="{card_w}" height="135" rx="10" '
            'fill="#fbfcfe" stroke="#d6deea"/>'
        )
        parts.append(f'<text x="{px+10}" y="{py+22}" class="small">{title}</text>')
        parts.append(
            f'<text x="{px+10}" y="{py+43}" class="small">{_e(note)}</text>'
        )
        # Padding card gets an explicit outer padded border.
        if title == "P=1, S=1":
            parts.append(
                f'<rect x="{px+49}" y="{py+52}" width="90" height="90" '
                'fill="#f4f5f7" stroke="#a8b5c8" stroke-dasharray="4 3"/>'
            )
            parts.append(_grid(px + 59, py + 62, 5, 5, 14, "gray", hot))
        else:
            parts.append(_grid(px + 55, py + 58, 5, 5, 14, "gray", hot))
        if title == "dilation 2":
            for idx in hot:
                rr, cc = divmod(idx, 5)
                parts.append(
                    f'<circle cx="{px+55+cc*14+5}" cy="{py+58+rr*14+5}" '
                    f'r="3.5" fill="{color}"/>'
                )
    return "".join(parts)

def _modern_visual(x, y, w, h):
    """Compact views of CLIP, DINO, diffusion and attention."""
    parts = []
    cards = [
        (x + 18, y + 58, "CLIP"),
        (x + w/2 + 4, y + 58, "DINO"),
        (x + 18, y + 210, "diffusion"),
        (x + w/2 + 4, y + 210, "attention"),
    ]
    card_w = w / 2 - 26
    for px, py, title in cards:
        parts.append(
            f'<rect x="{px}" y="{py}" width="{card_w}" height="126" rx="11" '
            'fill="#fbfcfe" stroke="#d6deea"/>'
        )
        parts.append(f'<text x="{px+10}" y="{py+22}" class="small">{title}</text>')
        if title == "CLIP":
            parts.append(f'<circle cx="{px+40}" cy="{py+60}" r="12" fill="#2454d8"/>')
            parts.append(f'<rect x="{px+31}" y="{py+87}" width="38" height="19" rx="5" fill="#e9f7f2" stroke="#8ccdbb"/>')
            parts.append(_arrow(px + 55, py + 60, px + 102, py + 60))
            parts.append(_arrow(px + 69, py + 96, px + 102, py + 78))
            parts.append(f'<circle cx="{px+130}" cy="{py+60}" r="8" fill="#08796f"/>')
            parts.append(f'<circle cx="{px+145}" cy="{py+77}" r="8" fill="#08796f"/>')
            parts.append(f'<text x="{px+102}" y="{py+108}" class="small">paired embeddings</text>')
        elif title == "DINO":
            parts.append(f'<circle cx="{px+58}" cy="{py+63}" r="21" fill="#edf3ff" stroke="#8faee8"/>')
            parts.append(f'<circle cx="{px+165}" cy="{py+63}" r="21" fill="#e9f7f2" stroke="#8ccdbb"/>')
            parts.append(f'<text x="{px+58}" y="{py+68}" text-anchor="middle" class="small">student</text>')
            parts.append(f'<text x="{px+165}" y="{py+68}" text-anchor="middle" class="small">teacher</text>')
            parts.append(f'<path d="M{px+143} {py+54} H{px+83}" stroke="#2454d8" stroke-width="3"/>')
            parts.append(f'<polygon points="{px+83},{py+54} {px+95},{py+47} {px+95},{py+61}" fill="#2454d8"/>')
            parts.append(f'<text x="{px+112}" y="{py+43}" text-anchor="middle" class="small">target</text>')
            parts.append(f'<path d="M{px+82} {py+82} H{px+143}" stroke="#08796f" stroke-width="2" stroke-dasharray="5 4"/>')
            parts.append(f'<polygon points="{px+143},{py+82} {px+131},{py+75} {px+131},{py+89}" fill="#08796f"/>')
            parts.append(f'<text x="{px+112}" y="{py+105}" text-anchor="middle" class="small">EMA params</text>')
        elif title == "diffusion":
            parts.append(_grid(px + 20, py + 43, 3, 3, 14, "blue", [1, 4, 7]))
            parts.append(_grid(px + 111, py + 43, 3, 3, 14, "gray", [0, 2, 4, 6, 8]))
            parts.append(_arrow(px + 70, py + 56, px + 103, py + 56))
            parts.append(
                f'<path d="M{px+103} {py+80} H{px+70}" '
                'stroke="#08796f" stroke-width="2.5"/>'
            )
            parts.append(
                f'<polygon points="{px+70},{py+80} {px+82},{py+73} '
                f'{px+82},{py+87}" fill="#08796f"/>'
            )
            parts.append(f'<text x="{px+22}" y="{py+108}" class="small">data → noise</text>')
            parts.append(f'<text x="{px+108}" y="{py+108}" class="small">denoise ←</text>')
        else:
            parts.append(_grid(px + 35, py + 40, 4, 4, 17, "heat", [5, 6, 9, 10]))
            parts.append(f'<text x="{px+116}" y="{py+62}" class="small">QKᵀ</text>')
            parts.append(f'<text x="{px+116}" y="{py+84}" class="small">weights × V</text>')
    return "".join(parts)

def _bayes_update_density(x, y, w, h):
    """Schematic prior, likelihood over a parameter, and posterior."""
    left = x + 40
    right = x + w - 20
    bottom = y + h - 42
    top = y + 45
    parts = [
        f'<path d="M{left} {bottom} H{right}" class="thin"/>',
        f'<path d="M{left+10} {bottom} C{x+w*.22} {bottom} {x+w*.30} {top+60} '
        f'{x+w*.40} {top+60} C{x+w*.50} {top+60} {x+w*.58} {bottom} '
        f'{right-10} {bottom}" stroke="#2454d8" stroke-width="4" fill="none"/>',
        f'<path d="M{left+10} {bottom} C{x+w*.43} {bottom} {x+w*.50} {top+90} '
        f'{x+w*.62} {top+90} C{x+w*.73} {top+90} {x+w*.80} {bottom} '
        f'{right-10} {bottom}" stroke="#a24d18" stroke-width="4" fill="none"/>',
        f'<path d="M{left+10} {bottom} C{x+w*.42} {bottom} {x+w*.49} {top+28} '
        f'{x+w*.55} {top+28} C{x+w*.64} {top+28} {x+w*.70} {bottom} '
        f'{right-10} {bottom}" stroke="#08796f" stroke-width="5" fill="none"/>',
        f'<text x="{left+4}" y="{top+18}" class="small" fill="#2454d8">prior p(θ)</text>',
        f'<text x="{left+92}" y="{top+18}" class="small" fill="#a24d18">likelihood L(θ)</text>',
        f'<text x="{left+215}" y="{top+18}" class="small" fill="#08796f">posterior p(θ|D)</text>',
        f'<text x="{right-22}" y="{bottom+24}" text-anchor="end" class="small">parameter θ →</text>',
        f'<text x="{left+5}" y="{y+h-15}" class="small">schematic shapes over θ</text>',
    ]
    return "".join(parts)

def _bayes_risk(x, y, w, h):
    parts = [
        f'<text x="{x+25}" y="{y+55}" class="body">at one observation x*</text>',
        f'<text x="{x+25}" y="{y+95}" class="small">expected risk</text>',
    ]
    items = [("action A", 0.18, "#08796f"), ("action B", 0.62, "#a24d18")]
    for idx, (label, value, color) in enumerate(items):
        yy = y + 125 + idx * 92
        parts.append(f'<text x="{x+28}" y="{yy+20}" class="small">{label}</text>')
        parts.append(
            f'<rect x="{x+108}" y="{yy}" width="{(w-160)*value}" height="28" '
            f'rx="6" fill="{color}" opacity=".78"/>'
        )
        parts.append(f'<text x="{x+w-55}" y="{yy+20}" class="small">{value:.2f}</text>')
    parts.append(
        f'<rect x="{x+20}" y="{y+h-78}" width="{w-40}" height="42" rx="10" '
        'fill="#e9f7f2" stroke="#8ccdbb"/>'
    )
    parts.append(
        f'<text x="{x+w/2}" y="{y+h-51}" text-anchor="middle" class="body">'
        "choose the action with minimum risk</text>"
    )
    return "".join(parts)


def _covariance_ellipse(x, y, w, h):
    cx = x + w * 0.52
    cy = y + h * 0.57
    parts = [
        f'<path d="M{x+35} {cy} H{x+w-25} M{cx} {y+45} V{y+h-35}" class="thin"/>',
        f'<ellipse cx="{cx}" cy="{cy}" rx="{w*.28}" ry="{h*.11}" '
        f'transform="rotate(-28 {cx} {cy})" fill="#edf3ff" stroke="#2454d8" stroke-width="3"/>',
        f'<ellipse cx="{cx}" cy="{cy}" rx="{w*.18}" ry="{h*.07}" '
        f'transform="rotate(-28 {cx} {cy})" fill="none" stroke="#08796f" stroke-width="3"/>',
        f'<path d="M{cx-w*.20} {cy+h*.11} L{cx+w*.20} {cy-h*.11}" '
        'stroke="#a24d18" stroke-width="3"/>',
        f'<text x="{x+24}" y="{y+45}" class="small">correlated dimensions</text>',
    ]
    return "".join(parts)


def _basis_functions(x, y, w, h):
    left = x + 38
    right = x + w - 22
    top = y + 48
    bottom = y + h - 42
    parts = [f'<path d="M{left} {bottom} H{right} M{left} {bottom} V{top}" class="thin"/>']
    parts.extend([
        f'<path d="M{left+5} {bottom-55} L{right-5} {top+45}" stroke="#2454d8" stroke-width="3" fill="none"/>',
        f'<path d="M{left+5} {bottom-25} C{x+w*.35} {top+35} {x+w*.62} {bottom-20} {right-5} {top+65}" stroke="#a24d18" stroke-width="3" fill="none"/>',
        f'<path d="M{left+5} {bottom-8} C{x+w*.34} {bottom-8} {x+w*.43} {top+55} {x+w*.52} {top+55} C{x+w*.62} {top+55} {x+w*.70} {bottom-8} {right-5} {bottom-8}" stroke="#08796f" stroke-width="3" fill="none"/>',
        f'<path d="M{left+5} {bottom-18} C{x+w*.34} {bottom-18} {x+w*.45} {top+95} {x+w*.58} {top+95} C{x+w*.70} {top+95} {x+w*.78} {top+35} {right-5} {top+35}" stroke="#7f5fbf" stroke-width="3" fill="none"/>',
        f'<text x="{left+8}" y="{top+15}" class="small" fill="#2454d8">linear</text>',
        f'<text x="{left+70}" y="{top+15}" class="small" fill="#a24d18">polynomial</text>',
        f'<text x="{left+8}" y="{top+37}" class="small" fill="#08796f">Gaussian</text>',
        f'<text x="{left+92}" y="{top+37}" class="small" fill="#7f5fbf">sigmoid</text>',
    ])
    return "".join(parts)


def _factor_graph(x, y, w, h):
    var_x = [x + 80, x + w * 0.50, x + w - 80]
    fy = y + h * 0.50
    parts = []
    for idx, vx in enumerate(var_x):
        parts.append(f'<circle cx="{vx}" cy="{y+105}" r="24" fill="#edf3ff" stroke="#8faee8" stroke-width="2"/>')
        parts.append(f'<text x="{vx}" y="{y+111}" text-anchor="middle" class="label">x{idx+1}</text>')
    factor_x = [x + w * 0.34, x + w * 0.66]
    for idx, fx in enumerate(factor_x):
        parts.append(f'<rect x="{fx-18}" y="{fy-18}" width="36" height="36" rx="5" fill="#fff1e7" stroke="#e0ae82" stroke-width="2"/>')
        parts.append(f'<text x="{fx}" y="{fy+6}" text-anchor="middle" class="small">f{idx+1}</text>')
    edges = [
        (var_x[0], y + 129, factor_x[0], fy - 18),
        (var_x[1], y + 129, factor_x[0], fy - 18),
        (var_x[1], y + 129, factor_x[1], fy - 18),
        (var_x[2], y + 129, factor_x[1], fy - 18),
    ]
    for x1, y1, x2, y2 in edges:
        parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" class="line"/>')
    parts.append(f'<text x="{x+24}" y="{y+h-35}" class="small">variables ↔ factors</text>')
    return "".join(parts)


def _posterior_approx(x, y, w, h):
    left = x + 38
    right = x + w - 20
    bottom = y + h - 40
    top = y + 48
    parts = [
        f'<path d="M{left} {bottom} H{right}" class="thin"/>',
        f'<path d="M{left+5} {bottom} C{x+w*.18} {bottom} {x+w*.23} {top+70} '
        f'{x+w*.33} {top+70} C{x+w*.43} {top+70} {x+w*.45} {bottom-25} '
        f'{x+w*.53} {bottom-25} C{x+w*.61} {bottom-25} {x+w*.64} {top+45} '
        f'{x+w*.73} {top+45} C{x+w*.84} {top+45} {x+w*.86} {bottom} '
        f'{right-5} {bottom}" stroke="#a24d18" stroke-width="4" fill="none"/>',
        f'<path d="M{left+5} {bottom} C{x+w*.33} {bottom} {x+w*.40} {top+85} '
        f'{x+w*.54} {top+85} C{x+w*.68} {top+85} {x+w*.76} {bottom} '
        f'{right-5} {bottom}" stroke="#2454d8" stroke-width="4" fill="none"/>',
        f'<text x="{left+8}" y="{top+15}" class="small" fill="#a24d18">true posterior</text>',
        f'<text x="{left+125}" y="{top+15}" class="small" fill="#2454d8">q(z)</text>',
    ]
    return "".join(parts)



def _elbo_decomposition(x, y, w, h):
    """Show ELBO as a lower bound without implying all terms are positive bars."""
    left = x + 55
    right = x + w - 35
    evidence_y = y + 105
    elbo_y = y + 245
    parts = [
        f'<path d="M{left} {evidence_y} H{right}" '
        'stroke="#2454d8" stroke-width="4"/>',
        f'<path d="M{left} {elbo_y} H{right}" '
        'stroke="#08796f" stroke-width="4"/>',
        f'<path d="M{x+w*.72} {evidence_y+4} V{elbo_y-4}" '
        'stroke="#e0ae82" stroke-width="4"/>',
        f'<text x="{left}" y="{evidence_y-16}" class="label" '
        'fill="#2454d8">log p(x)</text>',
        f'<text x="{left}" y="{elbo_y-16}" class="label" '
        'fill="#08796f">ELBO(q)</text>',
        f'<text x="{x+w*.72+10}" y="{(evidence_y+elbo_y)/2}" '
        'class="small" fill="#a24d18">KL(q || p)</text>',
        f'<text x="{x+22}" y="{y+h-48}" class="small">'
        "log p(x) = ELBO(q) + KL(q(z)||p(z|x))</text>",
        f'<text x="{x+22}" y="{y+h-24}" class="small">'
        "KL ≥ 0 ⇒ ELBO ≤ log p(x)</text>",
    ]
    return "".join(parts)


def _mc_samples(x, y, w, h):
    """Target density plus a rug plot of sampled x positions."""
    left = x + 38
    right = x + w - 22
    baseline = y + h - 76
    top = y + 52
    parts = [
        f'<path d="M{left} {baseline} H{right}" class="thin"/>',
        f'<path d="M{left+5} {baseline} C{x+w*.28} {baseline} '
        f'{x+w*.36} {top+45} {x+w*.50} {top+45} '
        f'C{x+w*.64} {top+45} {x+w*.72} {baseline} {right-5} {baseline}" '
        'stroke="#2454d8" stroke-width="4" fill="none"/>',
    ]
    samples = [0.18, 0.27, 0.41, 0.46, 0.53, 0.61, 0.68, 0.74, 0.83]
    for sx in samples:
        xx = x + sx * w
        parts.append(
            f'<path d="M{xx} {baseline+8} V{baseline+29}" '
            'stroke="#08796f" stroke-width="4"/>'
        )
    parts.append(
        f'<text x="{left+6}" y="{top+15}" class="small">'
        "target density p(x)</text>"
    )
    parts.append(
        f'<text x="{left+6}" y="{baseline+55}" class="small" fill="#08796f">'
        "rug marks = sampled x values</text>"
    )
    return "".join(parts)

def _mcmc_path(x, y, w, h):
    parts = [
        f'<ellipse cx="{x+w*.55}" cy="{y+h*.52}" rx="{w*.34}" ry="{h*.28}" fill="none" stroke="#c7d2e4" stroke-width="2"/>',
        f'<ellipse cx="{x+w*.55}" cy="{y+h*.52}" rx="{w*.22}" ry="{h*.16}" fill="none" stroke="#9fb2d3" stroke-width="2"/>',
        f'<ellipse cx="{x+w*.55}" cy="{y+h*.52}" rx="{w*.10}" ry="{h*.07}" fill="none" stroke="#7f9fd6" stroke-width="2"/>',
        f'<path d="M{x+w*.12} {y+h*.82} C{x+w*.20} {y+h*.70} {x+w*.27} {y+h*.75} {x+w*.32} {y+h*.60}" stroke="#a24d18" stroke-width="4" stroke-dasharray="8 6" fill="none"/>',
        f'<path d="M{x+w*.32} {y+h*.60} C{x+w*.39} {y+h*.35} {x+w*.46} {y+h*.62} {x+w*.55} {y+h*.48} C{x+w*.63} {y+h*.36} {x+w*.70} {y+h*.55} {x+w*.77} {y+h*.43}" stroke="#2454d8" stroke-width="4" fill="none"/>',
        f'<text x="{x+20}" y="{y+45}" class="small" fill="#a24d18">burn-in</text>',
        f'<text x="{x+90}" y="{y+45}" class="small" fill="#2454d8">retained chain</text>',
    ]
    return "".join(parts)



def _hmm_tasks(x, y, w, h):
    """Contrast evidence windows and targets for common HMM inference tasks."""
    parts = []
    rows = [
        ("filter", 2, [0, 1, 2], False),
        ("predict", 3, [0, 1, 2], False),
        ("smooth", 1, [0, 1, 2, 3, 4], False),
        ("Viterbi path", None, [0, 1, 2, 3, 4], True),
    ]
    for row_idx, (label, target, observed, full_path) in enumerate(rows):
        yy = y + 70 + row_idx * 74
        parts.append(f'<text x="{x+15}" y="{yy+4}" class="small">{label}</text>')
        for t in range(5):
            xx = x + 105 + t * 69
            fill = "#dce7fa" if t in observed else "#f8fafc"
            target_here = full_path or t == target
            stroke = "#2454d8" if target_here else "#b9c6d8"
            parts.append(
                f'<rect x="{xx}" y="{yy-21}" width="40" height="40" rx="8" '
                f'fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{"3" if target_here else "2"}"/>'
            )
            parts.append(
                f'<text x="{xx+20}" y="{yy+5}" text-anchor="middle" class="small">'
                f'z{t}</text>'
            )
            if t < 4:
                parts.append(
                    f'<path d="M{xx+42} {yy-1} H{xx+66}" '
                    f'stroke="{"#2454d8" if full_path else "#a8b5c8"}" '
                    'stroke-width="2"/>'
                )
        evidence = "x₀:₄" if observed == [0, 1, 2, 3, 4] else "x₀:₂"
        parts.append(
            f'<text x="{x+w-78}" y="{yy+4}" class="small">{evidence}</text>'
        )
    return "".join(parts)

def _vision_bridge(x, y, w, h):
    parts = []
    cards = [
        (x + 18, y + 58, "calibration"),
        (x + w/2 + 4, y + 58, "uncertainty"),
        (x + 18, y + 210, "latent space"),
        (x + w/2 + 4, y + 210, "sequence"),
    ]
    card_w = w / 2 - 26
    for px, py, title in cards:
        parts.append(
            f'<rect x="{px}" y="{py}" width="{card_w}" height="126" rx="11" '
            'fill="#fbfcfe" stroke="#d6deea"/>'
        )
        parts.append(f'<text x="{px+10}" y="{py+22}" class="small">{title}</text>')
        if title == "calibration":
            parts.append(f'<path d="M{px+35} {py+98} L{px+155} {py+38}" stroke="#a8b5c8" stroke-width="2" stroke-dasharray="5 4"/>')
            parts.append(f'<path d="M{px+35} {py+95} C{px+75} {py+88} {px+112} {py+48} {px+155} {py+44}" stroke="#2454d8" stroke-width="3" fill="none"/>')
        elif title == "uncertainty":
            for idx, bh in enumerate([28, 54, 78, 44]):
                parts.append(f'<rect x="{px+35+idx*32}" y="{py+104-bh}" width="20" height="{bh}" rx="4" fill="#e0ae82"/>')
        elif title == "latent space":
            for cx, cy in [(px+55,py+75),(px+82,py+58),(px+112,py+86),(px+145,py+52)]:
                parts.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#08796f"/>')
        else:
            for idx in range(4):
                cx = px + 38 + idx * 42
                parts.append(f'<circle cx="{cx}" cy="{py+70}" r="12" fill="#edf3ff" stroke="#8faee8"/>')
                if idx < 3:
                    parts.append(_arrow(cx + 14, py + 70, cx + 28, py + 70))
    return "".join(parts)




def _linear_score_matrix(x, y, w, h):
    """Show x, W, b and class scores as actual numeric arrays."""
    parts = []
    vector = [[0.6], [-1.2], [0.8], [0.3]]
    weights = [
        [0.8, -0.2, 0.5, 0.1],
        [-0.4, 0.9, 0.2, -0.3],
        [0.1, 0.3, -0.7, 0.8],
    ]
    scores = [1.25, -1.45, -0.62]
    parts.append(f'<text x="{x+18}" y="{y+42}" class="small">x ∈ R⁴</text>')
    parts.append(_value_grid(x + 18, y + 62, vector, 34, "#edf3ff"))
    parts.append(f'<text x="{x+92}" y="{y+42}" class="small">W ∈ R³ˣ⁴</text>')
    parts.append(_value_grid(x + 92, y + 62, weights, 34, "#e9f7f2"))
    parts.append(f'<text x="{x+246}" y="{y+42}" class="small">+ b</text>')
    parts.append(_value_grid(x + 246, y + 62, [[0.1], [-0.2], [0.0]], 34, "#fff1e7"))
    parts.append(_arrow(x + 292, y + 116, x + 334, y + 116))
    parts.append(f'<text x="{x+338}" y="{y+42}" class="small">scores</text>')
    parts.append(_value_grid(x + 338, y + 62, [[v] for v in scores], 40, "#edf3ff"))
    parts.append(
        f'<text x="{x+18}" y="{y+h-22}" class="small">'
        "each row of W defines one class score direction</text>"
    )
    return "".join(parts)


def _chain_rule_numeric(x, y, w, h):
    """Numeric forward/backward example with local derivatives."""
    nodes = [
        (x + 70, "x", "2"),
        (x + w * 0.50, "u=3x", "6"),
        (x + w - 70, "L=u²", "36"),
    ]
    parts = []
    for idx, (cx, name, value) in enumerate(nodes):
        parts.append(
            f'<circle cx="{cx}" cy="{y+120}" r="42" fill="#edf3ff" '
            'stroke="#8faee8" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{y+112}" text-anchor="middle" class="small">'
            f'{_e(name)}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{y+137}" text-anchor="middle" class="label">'
            f'{_e(value)}</text>'
        )
        if idx < 2:
            next_x = nodes[idx + 1][0]
            parts.append(_arrow(cx + 44, y + 120, next_x - 44, y + 120))
    parts.append(
        f'<text x="{x+18}" y="{y+42}" class="small">'
        "forward: values →</text>"
    )
    parts.append(
        f'<path d="M{x+w-114} {y+205} L{x+w*.50+44} {y+205}" '
        'stroke="#a24d18" stroke-width="3"/>'
    )
    parts.append(
        f'<polygon points="{x+w*.50+44},{y+205} {x+w*.50+57},{y+197} '
        f'{x+w*.50+57},{y+213}" fill="#a24d18"/>'
    )
    parts.append(
        f'<path d="M{x+w*.50-44} {y+205} L{x+114} {y+205}" '
        'stroke="#a24d18" stroke-width="3"/>'
    )
    parts.append(
        f'<polygon points="{x+114},{y+205} {x+127},{y+197} '
        f'{x+127},{y+213}" fill="#a24d18"/>'
    )
    parts.append(
        f'<text x="{x+w*.69}" y="{y+194}" text-anchor="middle" '
        'class="small" fill="#a24d18">dL/du = 12</text>'
    )
    parts.append(
        f'<text x="{x+w*.31}" y="{y+194}" text-anchor="middle" '
        'class="small" fill="#a24d18">du/dx = 3</text>'
    )
    parts.append(
        f'<text x="{x+w*.50}" y="{y+250}" text-anchor="middle" '
        'class="label" fill="#a24d18">dL/dx = 12 × 3 = 36</text>'
    )
    return "".join(parts)



def _gradient_check(x, y, w, h):
    """Compare analytic gradients with a central-difference check."""
    parts = [
        f'<path d="M{x+42} {y+h-58} H{x+w-24} M{x+42} {y+h-58} V{y+48}" '
        'class="thin"/>'
    ]
    analytic = [0.82, -0.36, 0.19]
    numeric = [0.820001, -0.360001, 0.190000]
    scale = (h - 130) / 1.1
    zero_y = y + h - 105
    parts.append(
        f'<path d="M{x+42} {zero_y} H{x+w-24}" '
        'stroke="#c5cfdd" stroke-width="1.5" stroke-dasharray="5 5"/>'
    )
    for idx, (ga, gn) in enumerate(zip(analytic, numeric)):
        cx = x + 95 + idx * ((w - 150) / 2)
        for offset, val, color in [(-10, ga, "#2454d8"), (10, gn, "#08796f")]:
            yy = zero_y - val * scale
            parts.append(
                f'<circle cx="{cx+offset}" cy="{yy}" r="7" fill="{color}"/>'
            )
        parts.append(
            f'<text x="{cx}" y="{y+h-35}" text-anchor="middle" '
            f'class="small">w{idx+1}</text>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+38}" class="small" fill="#2454d8">'
        "● backprop</text>"
    )
    parts.append(
        f'<text x="{x+105}" y="{y+38}" class="small" fill="#08796f">'
        "● finite difference</text>"
    )
    parts.append(
        f'<text x="{x+w-165}" y="{y+38}" class="small">'
        "example: relative error ≈ 1e−6</text>"
    )
    return "".join(parts)

def _optimizer_paths(x, y, w, h):
    """Compare SGD, Momentum and Adam on one contour landscape."""
    cx = x + w * 0.58
    cy = y + h * 0.54
    parts = []
    for rx, ry in [(w*.34, h*.30), (w*.24, h*.21), (w*.14, h*.12)]:
        parts.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
            'fill="none" stroke="#c7d2e4" stroke-width="2"/>'
        )
    paths = [
        ("#2454d8", [
            (x+w*.16,y+h*.82),(x+w*.31,y+h*.36),(x+w*.40,y+h*.74),
            (x+w*.49,y+h*.43),(x+w*.54,y+h*.61),(cx,cy)
        ], "SGD"),
        ("#08796f", [
            (x+w*.16,y+h*.82),(x+w*.28,y+h*.63),(x+w*.40,y+h*.53),
            (x+w*.50,y+h*.50),(cx,cy)
        ], "Momentum"),
        ("#a24d18", [
            (x+w*.16,y+h*.82),(x+w*.24,y+h*.70),(x+w*.34,y+h*.60),
            (x+w*.45,y+h*.55),(cx,cy)
        ], "Adam"),
    ]
    for color, pts, label in paths:
        d = "M" + " L".join(f"{px} {py}" for px, py in pts)
        parts.append(
            f'<path d="{d}" stroke="{color}" stroke-width="3.5" '
            'fill="none" stroke-linejoin="round"/>'
        )
        for px, py in pts[:-1]:
            parts.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{color}"/>')
    for idx, (color, _, label) in enumerate(paths):
        parts.append(
            f'<text x="{x+18}" y="{y+35+idx*23}" class="small" '
            f'fill="{color}">{_e(label)}</text>'
        )
    return "".join(parts)


def _lr_curves(x, y, w, h):
    """Loss-vs-step curves for three learning-rate regimes."""
    parts = [
        f'<path d="M{x+45} {y+h-45} H{x+w-22} M{x+45} {y+h-45} V{y+42}" '
        'class="thin"/>'
    ]
    curves = [
        ("#6d7f9b", f'M{x+50} {y+65} C{x+w*.35} {y+85} {x+w*.65} {y+118} {x+w-30} {y+145}', "too small"),
        ("#08796f", f'M{x+50} {y+65} C{x+w*.26} {y+110} {x+w*.46} {y+h-78} {x+w-30} {y+h-72}', "good"),
        ("#a24d18", f'M{x+50} {y+70} L{x+w*.26} {y+145} L{x+w*.43} {y+55} L{x+w*.62} {y+170} L{x+w-30} {y+72}', "too large"),
    ]
    for idx, (color, path, label) in enumerate(curves):
        parts.append(
            f'<path d="{path}" stroke="{color}" stroke-width="4" fill="none"/>'
        )
        parts.append(
            f'<text x="{x+w-135}" y="{y+48+idx*22}" class="small" '
            f'fill="{color}">{_e(label)}</text>'
        )
    parts.append(
        f'<text x="{x+w-90}" y="{y+h-20}" class="small">steps →</text>'
    )
    return "".join(parts)



def _init_variance(x, y, w, h):
    """Schematic activation distributions for poor and well-scaled initialization."""
    parts = []
    labels = ["too small", "well scaled", "too large"]
    spreads = [0.22, 0.48, 0.82]
    peaks = [0.95, 0.72, 0.46]
    panel_w = (w - 30) / 3
    for idx, (label, spread, peak) in enumerate(zip(labels, spreads, peaks)):
        px = x + 8 + idx * panel_w
        center = px + panel_w * 0.52
        base = y + h - 62
        top = base - (h - 145) * peak
        half = panel_w * spread * 0.48
        parts.append(
            f'<text x="{center}" y="{y+42}" text-anchor="middle" '
            f'class="small">{_e(label)}</text>'
        )
        parts.append(
            f'<path d="M{px+10} {base} H{px+panel_w-10}" class="thin"/>'
        )
        parts.append(
            f'<path d="M{center-half} {base} C{center-half*.55} {base} '
            f'{center-half*.35} {top} {center} {top} '
            f'C{center+half*.35} {top} {center+half*.55} {base} '
            f'{center+half} {base}" '
            f'stroke="{"#08796f" if idx==1 else "#2454d8"}" '
            'stroke-width="4" fill="none"/>'
        )
    parts.append(
        f'<text x="{x+w/2}" y="{y+h-28}" text-anchor="middle" class="small">'
        "avoid variance collapse / explosion</text>"
    )
    return "".join(parts)

def _pool_compare(x, y, w, h):
    """Numeric max-pooling and average-pooling comparison."""
    values = [
        [1, 3, 2, 4],
        [5, 9, 1, 2],
        [0, 2, 8, 6],
        [4, 1, 3, 7],
    ]
    parts = [_value_grid(x + 18, y + 70, values, 42, "#edf3ff")]
    parts.append(
        f'<text x="{x+18}" y="{y+48}" class="small">4×4 input</text>'
    )
    parts.append(_arrow(x + 198, y + 150, x + 248, y + 150))
    parts.append(
        f'<text x="{x+258}" y="{y+48}" class="small">max pool</text>'
    )
    parts.append(_value_grid(
        x + 258, y + 95, [[9, 4], [4, 8]], 48, "#e9f7f2"
    ))
    parts.append(
        f'<text x="{x+258}" y="{y+218}" class="small">average pool</text>'
    )
    parts.append(_value_grid(
        x + 258, y + 235, [[4.5, 2.25], [1.75, 6.0]], 48, "#fff1e7"
    ))
    return "".join(parts)



def _residual_flow(x, y, w, h):
    """Residual branch with an explicit addition node and identity skip."""
    parts = []
    y_mid = y + 165
    x_in = x + 55
    x_c1 = x + w * 0.35
    x_c2 = x + w * 0.61
    x_add = x + w * 0.80
    x_out = x + w - 45

    parts.append(
        f'<rect x="{x_in-28}" y="{y_mid-23}" width="56" height="46" rx="9" '
        'fill="#edf3ff" stroke="#8faee8" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{x_in}" y="{y_mid+6}" text-anchor="middle" class="label">x</text>'
    )
    for cx, label in [(x_c1, "F₁"), (x_c2, "F₂")]:
        parts.append(
            f'<rect x="{cx-34}" y="{y_mid-23}" width="68" height="46" rx="9" '
            'fill="#edf3ff" stroke="#8faee8" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{y_mid+6}" text-anchor="middle" class="small">'
            f'{label}(x)</text>'
        )
    parts.append(_arrow(x_in + 30, y_mid, x_c1 - 36, y_mid))
    parts.append(_arrow(x_c1 + 36, y_mid, x_c2 - 36, y_mid))
    parts.append(_arrow(x_c2 + 36, y_mid, x_add - 22, y_mid))

    parts.append(
        f'<circle cx="{x_add}" cy="{y_mid}" r="20" fill="#e9f7f2" '
        'stroke="#8ccdbb" stroke-width="3"/>'
    )
    parts.append(
        f'<text x="{x_add}" y="{y_mid+7}" text-anchor="middle" '
        'font-size="24" font-weight="700" fill="#08796f">+</text>'
    )
    parts.append(_arrow(x_add + 22, y_mid, x_out - 28, y_mid))
    parts.append(
        f'<rect x="{x_out-27}" y="{y_mid-23}" width="54" height="46" rx="9" '
        'fill="#2454d8" stroke="#2454d8"/>'
    )
    parts.append(
        f'<text x="{x_out}" y="{y_mid+6}" text-anchor="middle" class="white">H(x)</text>'
    )

    parts.append(
        f'<path d="M{x_in} {y_mid-25} C{x+w*.24} {y+55} '
        f'{x+w*.67} {y+55} {x_add} {y_mid-22}" '
        'stroke="#08796f" stroke-width="4" fill="none"/>'
    )
    parts.append(
        f'<polygon points="{x_add},{y_mid-22} {x_add-9},{y_mid-37} '
        f'{x_add+9},{y_mid-37}" fill="#08796f"/>'
    )
    parts.append(
        f'<text x="{x+w*.50}" y="{y+55}" text-anchor="middle" '
        'class="small" fill="#08796f">identity skip: x</text>'
    )
    parts.append(
        f'<text x="{x+w*.50}" y="{y+h-45}" text-anchor="middle" class="small">'
        "H(x)=F(x)+x, so ∂H/∂x includes the identity term I</text>"
    )
    return "".join(parts)

def _entropy_curve(x, y, w, h):
    """Binary entropy H(p) with maximum uncertainty at p=0.5."""
    left = x + 45
    right = x + w - 28
    base = y + h - 48
    top = y + 58
    parts = [
        f'<path d="M{left} {base} H{right} M{left} {base} V{top}" class="thin"/>',
        f'<path d="M{left} {base} C{x+w*.20} {y+88} {x+w*.36} {top} '
        f'{x+w*.50} {top} C{x+w*.64} {top} {x+w*.80} {y+88} {right} {base}" '
        'stroke="#2454d8" stroke-width="4" fill="none"/>',
        f'<path d="M{x+w*.50} {top} V{base}" stroke="#a8b5c8" '
        'stroke-width="2" stroke-dasharray="6 5"/>',
        f'<text x="{x+w*.50}" y="{base+24}" text-anchor="middle" class="small">p=0.5</text>',
        f'<text x="{x+w*.50}" y="{top-12}" text-anchor="middle" class="small">max entropy</text>',
    ]
    return "".join(parts)


def _regression_uncertainty(x, y, w, h):
    """Posterior predictive mean and uncertainty band for Bayesian regression."""
    left = x + 42
    right = x + w - 24
    base = y + h - 45
    parts = [
        f'<path d="M{left} {base} H{right} M{left} {base} V{y+45}" class="thin"/>',
        f'<path d="M{left+10} {y+h-92} C{x+w*.30} {y+165} '
        f'{x+w*.62} {y+118} {right-8} {y+70} L{right-8} {y+128} '
        f'C{x+w*.62} {y+172} {x+w*.30} {y+220} {left+10} {y+h-55} Z" '
        'fill="#bcd1f6" opacity=".45"/>',
        f'<path d="M{left+10} {y+h-74} C{x+w*.30} {y+190} '
        f'{x+w*.62} {y+145} {right-8} {y+98}" '
        'stroke="#2454d8" stroke-width="4" fill="none"/>',
    ]
    pts = [(0.16,.72),(0.29,.62),(0.42,.56),(0.56,.43),(0.70,.34),(0.82,.25)]
    for px, py in pts:
        parts.append(
            f'<circle cx="{x+px*w}" cy="{y+py*h}" r="6" fill="#203455"/>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+36}" class="small" fill="#2454d8">'
        "posterior predictive mean ± uncertainty</text>"
    )
    return "".join(parts)


def _importance_sampling(x, y, w, h):
    """Importance sampling: proposal samples reweighted toward target density."""
    base = y + h - 48
    parts = [
        f'<path d="M{x+40} {base} H{x+w-22}" class="thin"/>',
        f'<path d="M{x+45} {base} C{x+w*.22} {base} {x+w*.28} {y+74} '
        f'{x+w*.43} {y+74} C{x+w*.58} {y+74} {x+w*.63} {base} '
        f'{x+w-32} {base}" stroke="#2454d8" stroke-width="4" fill="none"/>',
        f'<path d="M{x+45} {base} C{x+w*.18} {base} {x+w*.34} {y+128} '
        f'{x+w*.57} {y+128} C{x+w*.80} {y+128} {x+w*.88} {base} '
        f'{x+w-32} {base}" stroke="#e0ae82" stroke-width="4" fill="none"/>',
    ]
    samples = [
        (.23, .35), (.36, .85), (.48, 1.0), (.62, .62), (.75, .24)
    ]
    for px, weight in samples:
        xx = x + px * w
        parts.append(
            f'<path d="M{xx} {base} V{base-58*weight}" '
            'stroke="#08796f" stroke-width="5"/>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+36}" class="small" fill="#2454d8">target p(x)</text>'
    )
    parts.append(
        f'<text x="{x+105}" y="{y+36}" class="small" fill="#a24d18">proposal q(x)</text>'
    )
    parts.append(
        f'<text x="{x+w-170}" y="{y+36}" class="small" fill="#08796f">'
        "weight p/q</text>"
    )
    return "".join(parts)



def _pca_projection(x, y, w, h):
    """Orthogonally project 2D samples onto a displayed PC1 axis."""
    left = x + 45
    right = x + w - 35
    top = y + 58
    bottom = y + h - 58
    p1 = (left, bottom)
    p2 = (right, top)
    vx = p2[0] - p1[0]
    vy = p2[1] - p1[1]
    norm2 = vx * vx + vy * vy

    samples = [
        (x+w*.18, y+h*.72),
        (x+w*.29, y+h*.60),
        (x+w*.39, y+h*.57),
        (x+w*.52, y+h*.44),
        (x+w*.65, y+h*.37),
        (x+w*.77, y+h*.25),
    ]
    parts = [
        f'<path d="M{x+35} {y+h-35} H{x+w-20} M{x+35} {y+h-35} V{y+35}" '
        'class="thin"/>',
        f'<path d="M{p1[0]} {p1[1]} L{p2[0]} {p2[1]}" '
        'stroke="#a24d18" stroke-width="4"/>',
    ]
    for sx, sy in samples:
        t = ((sx-p1[0])*vx + (sy-p1[1])*vy) / norm2
        rx = p1[0] + t * vx
        ry = p1[1] + t * vy
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="7" fill="#2454d8"/>')
        parts.append(
            f'<path d="M{sx} {sy} L{rx} {ry}" stroke="#a8b5c8" '
            'stroke-width="2" stroke-dasharray="5 4"/>'
        )
        parts.append(f'<circle cx="{rx}" cy="{ry}" r="4" fill="#08796f"/>')
    parts.append(
        f'<text x="{x+18}" y="{y+34}" class="small">'
        "orthogonal projection onto PC1</text>"
    )
    return "".join(parts)


def _split_roles(x, y, w, h):
    """Show distinct roles of train, validation and test subsets."""
    parts = []
    rows = [
        ("train", "fit model parameters", "#2454d8"),
        ("validation", "choose hyperparameters / checkpoint", "#08796f"),
        ("test", "final unbiased estimate; use after selection", "#a24d18"),
    ]
    for idx, (name, note, color) in enumerate(rows):
        yy = y + 70 + idx * 92
        parts.append(
            f'<rect x="{x+22}" y="{yy-28}" width="112" height="54" rx="10" '
            f'fill="{color}" opacity=".14" stroke="{color}" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x+78}" y="{yy+6}" text-anchor="middle" class="label">'
            f'{_e(name)}</text>'
        )
        parts.append(_arrow(x + 138, yy, x + 186, yy))
        parts.append(
            f'<text x="{x+198}" y="{yy+5}" class="body">{_e(note)}</text>'
        )
    return "".join(parts)


def _score_axis(x, y, w, h):
    """Plot the same class scores used in the linear score-matrix example."""
    values = [("cat", 1.25, "#2454d8"), ("dog", -1.45, "#a24d18"), ("fox", -0.62, "#08796f")]
    left = x + 55
    right = x + w - 35
    axis_y = y + h * 0.55
    parts = [
        f'<path d="M{left} {axis_y} H{right}" class="thin"/>',
        f'<text x="{left}" y="{axis_y+28}" class="small">−2</text>',
        f'<text x="{(left+right)/2}" y="{axis_y+28}" text-anchor="middle" class="small">0</text>',
        f'<text x="{right}" y="{axis_y+28}" text-anchor="end" class="small">+2</text>',
    ]
    for idx, (label, value, color) in enumerate(values):
        px = left + (value + 2) / 4 * (right - left)
        py = axis_y - 32 - idx * 33
        parts.append(
            f'<path d="M{px} {axis_y} V{py+8}" stroke="{color}" stroke-width="2"/>'
        )
        parts.append(f'<circle cx="{px}" cy="{py}" r="7" fill="{color}"/>')
        parts.append(
            f'<text x="{px+10}" y="{py+5}" class="small" fill="{color}">'
            f'{_e(label)} {value:+.2f}</text>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+40}" class="small">'
        "largest score wins; scores need not be probabilities</text>"
    )
    return "".join(parts)


def _momentum_update(x, y, w, h):
    """Illustrate gradient plus velocity memory in momentum SGD."""
    ox = x + w * 0.45
    oy = y + h * 0.63
    parts = [
        f'<circle cx="{ox}" cy="{oy}" r="7" fill="#203455"/>',
        f'<path d="M{ox} {oy} L{ox+95} {oy-70}" stroke="#2454d8" stroke-width="4"/>',
        f'<polygon points="{ox+95},{oy-70} {ox+78},{oy-68} {ox+87},{oy-54}" fill="#2454d8"/>',
        f'<path d="M{ox} {oy} L{ox-70} {oy-80}" stroke="#08796f" stroke-width="4"/>',
        f'<polygon points="{ox-70},{oy-80} {ox-55},{oy-72} {ox-66},{oy-62}" fill="#08796f"/>',
        f'<path d="M{ox} {oy} L{ox+28} {oy-116}" stroke="#a24d18" stroke-width="4"/>',
        f'<polygon points="{ox+28},{oy-116} {ox+16},{oy-101} {ox+34},{oy-98}" fill="#a24d18"/>',
        f'<text x="{x+18}" y="{y+45}" class="small" fill="#2454d8">−η∇L: current gradient step</text>',
        f'<text x="{x+18}" y="{y+70}" class="small" fill="#08796f">μvₜ₋₁: velocity memory</text>',
        f'<text x="{x+18}" y="{y+95}" class="small" fill="#a24d18">vₜ: combined update</text>',
    ]
    return "".join(parts)


def _landscape_regions(x, y, w, h):
    """Distinct local minimum, saddle and flat-region sketches."""
    parts = []
    card_w = (w - 42) / 3
    labels = ["local minimum", "saddle", "flat region"]
    for idx, label in enumerate(labels):
        px = x + 8 + idx * (card_w + 13)
        cx = px + card_w / 2
        cy = y + h * 0.56
        parts.append(
            f'<rect x="{px}" y="{y+45}" width="{card_w}" height="{h-92}" rx="10" '
            'fill="#fbfcfe" stroke="#d6deea"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{y+72}" text-anchor="middle" class="small">'
            f'{_e(label)}</text>'
        )
        if idx == 0:
            for rx, ry in [(card_w*.32, 82), (card_w*.22, 55), (card_w*.12, 28)]:
                parts.append(
                    f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
                    'fill="none" stroke="#8faee8" stroke-width="2"/>'
                )
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#08796f"/>')
        elif idx == 1:
            parts.append(
                f'<path d="M{px+18} {cy-70} C{cx-30} {cy-25} '
                f'{cx-30} {cy+25} {px+18} {cy+70}" class="thin"/>'
            )
            parts.append(
                f'<path d="M{px+card_w-18} {cy-70} C{cx+30} {cy-25} '
                f'{cx+30} {cy+25} {px+card_w-18} {cy+70}" class="thin"/>'
            )
            parts.append(
                f'<path d="M{cx-55} {cy} H{cx+55}" stroke="#a24d18" stroke-width="3"/>'
            )
        else:
            parts.append(
                f'<path d="M{px+18} {cy+25} C{cx-40} {cy+18} '
                f'{cx+40} {cy+18} {px+card_w-18} {cy+10}" '
                'stroke="#7e91af" stroke-width="5" fill="none"/>'
            )
            parts.append(
                f'<text x="{cx}" y="{cy+70}" text-anchor="middle" class="small">'
                "|∇L| small</text>"
            )
    return "".join(parts)


def _svm_hinge(x, y, w, h):
    """Exact binary hinge loss as a function of functional margin m=yf(x)."""
    left = x + 50
    right = x + w - 25
    top = y + 48
    bottom = y + h - 48
    margin_x = left + (1.0 + 1.0) / 3.0 * (right - left)
    parts = [
        f'<path d="M{left} {bottom} H{right} M{left} {bottom} V{top}" class="thin"/>',
        f'<path d="M{left} {top+28} L{margin_x} {bottom} H{right}" '
        'stroke="#a24d18" stroke-width="4" fill="none"/>',
        f'<path d="M{margin_x} {top} V{bottom}" stroke="#9aa9be" stroke-width="2" '
        'stroke-dasharray="6 5"/>',
        f'<text x="{margin_x+6}" y="{bottom-10}" class="small">m=1 → loss 0</text>',
        f'<text x="{right-120}" y="{bottom+25}" class="small">m = y f(x) →</text>',
        f'<text x="{left+5}" y="{top+12}" class="small">max(0, 1−m)</text>',
    ]
    points = [("wrong", -0.5, 1.5), ("inside", 0.4, 0.6), ("on margin", 1.0, 0.0), ("far correct", 1.6, 0.0)]
    for label, m, loss in points:
        px = left + (m + 1.0) / 3.0 * (right - left)
        py = bottom - loss / 2.0 * (bottom - top)
        parts.append(f'<circle cx="{px}" cy="{py}" r="6" fill="#2454d8"/>')
        parts.append(f'<text x="{px+7}" y="{py-7}" class="small">{_e(label)}</text>')
    return "".join(parts)


def _multiclass_regions(x, y, w, h):
    """Three class decision regions in a 2D feature space."""
    left = x + 35
    top = y + 48
    width = w - 55
    height = h - 88
    cx = left + width * 0.50
    cy = top + height * 0.52
    parts = [
        f'<rect x="{left}" y="{top}" width="{width}" height="{height}" '
        'fill="#fbfcfe" stroke="#d4deeb"/>',
        f'<polygon points="{left},{top} {cx},{cy} {left},{top+height}" fill="#edf3ff"/>',
        f'<polygon points="{left},{top} {left+width},{top} {cx},{cy}" fill="#e9f7f2"/>',
        f'<polygon points="{left+width},{top} {left+width},{top+height} '
        f'{left},{top+height} {cx},{cy}" fill="#fff1e7"/>',
        f'<path d="M{left} {top} L{cx} {cy} L{left} {top+height}" class="thin"/>',
        f'<path d="M{cx} {cy} L{left+width} {top}" class="thin"/>',
        f'<path d="M{cx} {cy} L{left+width} {top+height}" class="thin"/>',
    ]
    samples = [
        (0.18,.38,"#2454d8"),(0.24,.70,"#2454d8"),
        (0.62,.20,"#08796f"),(0.78,.30,"#08796f"),
        (0.65,.68,"#a24d18"),(0.82,.75,"#a24d18"),
    ]
    for px, py, color in samples:
        parts.append(
            f'<circle cx="{left+px*width}" cy="{top+py*height}" r="7" fill="{color}"/>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+34}" class="small">'
        "argmaxₖ scoreₖ(x) partitions feature space into class regions</text>"
    )
    return "".join(parts)


def _ensemble_parallel(x, y, w, h):
    """Parallel committee whose predictions are averaged."""
    parts = []
    in_x = x + 48
    out_x = x + w - 55
    mid_x = x + w * 0.48
    parts.append(
        f'<rect x="{in_x-28}" y="{y+150}" width="56" height="46" rx="9" '
        'fill="#edf3ff" stroke="#8faee8"/>'
    )
    parts.append(f'<text x="{in_x}" y="{y+179}" text-anchor="middle" class="small">x</text>')
    ys = [y+90, y+170, y+250]
    for idx, yy in enumerate(ys):
        parts.append(_arrow(in_x+30, y+173, mid_x-45, yy))
        parts.append(
            f'<rect x="{mid_x-42}" y="{yy-22}" width="84" height="44" rx="9" '
            'fill="#f3f7fe" stroke="#9bb5e5"/>'
        )
        parts.append(
            f'<text x="{mid_x}" y="{yy+5}" text-anchor="middle" class="small">'
            f'model {idx+1}</text>'
        )
        parts.append(_arrow(mid_x+44, yy, out_x-35, y+170))
    parts.append(
        f'<circle cx="{out_x}" cy="{y+170}" r="28" fill="#e9f7f2" '
        'stroke="#8ccdbb" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{out_x}" y="{y+175}" text-anchor="middle" class="small">average</text>'
    )
    return "".join(parts)


def _moe_routing(x, y, w, h):
    """Input-dependent gating weights combine expert predictions in parallel."""
    parts = []
    in_x = x + 48
    gate_x = x + w * 0.34
    expert_x = x + w * 0.62
    out_x = x + w - 48
    parts.append(
        f'<rect x="{in_x-26}" y="{y+150}" width="52" height="44" rx="8" '
        'fill="#edf3ff" stroke="#8faee8"/>'
    )
    parts.append(f'<text x="{in_x}" y="{y+177}" text-anchor="middle" class="small">x</text>')
    parts.append(_arrow(in_x+28, y+172, gate_x-40, y+110))
    parts.append(
        f'<rect x="{gate_x-38}" y="{y+88}" width="76" height="44" rx="8" '
        'fill="#fff1e7" stroke="#e0ae82"/>'
    )
    parts.append(f'<text x="{gate_x}" y="{y+115}" text-anchor="middle" class="small">gate g(x)</text>')
    ys = [y+95, y+170, y+245]
    for idx, yy in enumerate(ys):
        parts.append(_arrow(in_x+28, y+172, expert_x-45, yy))
        parts.append(
            f'<rect x="{expert_x-42}" y="{yy-21}" width="84" height="42" rx="8" '
            'fill="#f3f7fe" stroke="#9bb5e5"/>'
        )
        parts.append(
            f'<text x="{expert_x}" y="{yy+5}" text-anchor="middle" class="small">'
            f'expert {idx+1}</text>'
        )
        parts.append(
            f'<path d="M{gate_x+39} {y+110} L{expert_x-45} {yy-9}" '
            'stroke="#e0ae82" stroke-width="2" stroke-dasharray="5 4"/>'
        )
        parts.append(_arrow(expert_x+44, yy, out_x-28, y+170))
    parts.append(
        f'<circle cx="{out_x}" cy="{y+170}" r="26" fill="#e9f7f2" '
        'stroke="#8ccdbb" stroke-width="2"/>'
    )
    parts.append(f'<text x="{out_x}" y="{y+175}" text-anchor="middle" class="small">Σ gₖyₖ</text>')
    return "".join(parts)


def _iou_boxes(x, y, w, h):
    parts = [
        f'<rect x="{x+70}" y="{y+80}" width="{w*.46}" height="{h*.48}" '
        'fill="#2454d8" opacity=".16" stroke="#2454d8" stroke-width="3"/>',
        f'<rect x="{x+w*.38}" y="{y+125}" width="{w*.44}" height="{h*.45}" '
        'fill="#08796f" opacity=".16" stroke="#08796f" stroke-width="3"/>',
        f'<text x="{x+20}" y="{y+45}" class="small">IoU = intersection / union</text>',
        f'<text x="{x+w*.50}" y="{y+h-35}" text-anchor="middle" class="small">'
        "0 ≤ IoU ≤ 1; larger means more overlap</text>",
    ]
    return "".join(parts)


def _semantic_instance_masks(x, y, w, h):
    parts = []
    half = w / 2
    for idx, title in enumerate(["semantic", "instance"]):
        px = x + idx * half
        parts.append(f'<text x="{px+18}" y="{y+45}" class="small">{title}</text>')
        parts.append(
            f'<rect x="{px+18}" y="{y+65}" width="{half-36}" height="{h-115}" '
            'fill="#eef2f6" stroke="#cbd5e2"/>'
        )
        if idx == 0:
            parts.append(
                f'<ellipse cx="{px+half*.42}" cy="{y+h*.53}" rx="{half*.18}" '
                f'ry="{h*.18}" fill="#2454d8" opacity=".45"/>'
            )
            parts.append(
                f'<ellipse cx="{px+half*.66}" cy="{y+h*.53}" rx="{half*.18}" '
                f'ry="{h*.18}" fill="#2454d8" opacity=".45"/>'
            )
        else:
            parts.append(
                f'<ellipse cx="{px+half*.42}" cy="{y+h*.53}" rx="{half*.18}" '
                f'ry="{h*.18}" fill="#2454d8" opacity=".48"/>'
            )
            parts.append(
                f'<ellipse cx="{px+half*.66}" cy="{y+h*.53}" rx="{half*.18}" '
                f'ry="{h*.18}" fill="#08796f" opacity=".48"/>'
            )
    return "".join(parts)



def _nms_visual(x, y, w, h):
    """Greedy NMS in three vertical stages to avoid misleading serial box flow."""
    parts = []
    stages = [
        ("1 rank scores", "0.92 / 0.81 / 0.55"),
        ("2 keep best", "keep 0.92"),
        ("3 suppress overlap", "same class: suppress 0.81 if IoU > threshold"),
    ]
    for idx, (label, note) in enumerate(stages):
        yy = y + 58 + idx * 105
        parts.append(
            f'<rect x="{x+20}" y="{yy}" width="{w-40}" height="82" rx="10" '
            'fill="#fbfcfe" stroke="#d6deea"/>'
        )
        parts.append(
            f'<text x="{x+34}" y="{yy+24}" class="small">{_e(label)}</text>'
        )
        parts.append(
            f'<text x="{x+34}" y="{yy+48}" class="small">{_e(note)}</text>'
        )
        bx = x + w - 108
        parts.append(
            f'<rect x="{bx}" y="{yy+18}" width="48" height="42" fill="none" '
            'stroke="#2454d8" stroke-width="3"/>'
        )
        if idx != 1:
            parts.append(
                f'<rect x="{bx+9}" y="{yy+24}" width="46" height="40" fill="none" '
                f'stroke="#08796f" stroke-width="3" opacity="{1 if idx==0 else .22}"/>'
            )
    return "".join(parts)

def _architecture_compare(x, y, w, h):
    """Block-level motifs rather than arbitrary depth bars."""
    names = ["LeNet", "AlexNet", "VGG", "ResNet", "ViT"]
    motifs = [
        ["conv", "pool", "fc"],
        ["conv", "pool", "conv", "fc"],
        ["3×3", "3×3", "pool", "…"],
        ["res", "res", "+skip", "…"],
        ["patch", "MHSA", "MLP", "…"],
    ]
    colors = ["#8faee8", "#8faee8", "#8faee8", "#8ccdbb", "#e0ae82"]
    parts = []
    col_w = (w - 30) / 5
    for idx, (name, blocks, color) in enumerate(zip(names, motifs, colors)):
        px = x + 8 + idx * col_w
        parts.append(
            f'<text x="{px+col_w/2}" y="{y+42}" text-anchor="middle" '
            f'class="small">{name}</text>'
        )
        for j, block in enumerate(blocks):
            yy = y + 70 + j * 62
            parts.append(
                f'<rect x="{px+10}" y="{yy}" width="{col_w-20}" height="42" rx="7" '
                f'fill="{color}" opacity=".22" stroke="{color}" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{px+col_w/2}" y="{yy+26}" text-anchor="middle" '
                f'class="small">{_e(block)}</text>'
            )
    return "".join(parts)



def _conv_channel_sum(x, y, w, h):
    """One convolution filter spans every input channel."""
    colors = ["#fbe3e3", "#e9f7f2", "#edf3ff"]
    labels = ["R", "G", "B"]
    parts = []
    in_x = x + 18
    box_w = 52
    box_h = 48
    kernel_x = x + w * 0.34
    sum_x = x + w * 0.63
    out_x = x + w - 38
    for idx, (color, label) in enumerate(zip(colors, labels)):
        py = y + 72 + idx * 82
        parts.append(
            f'<rect x="{in_x}" y="{py}" width="{box_w}" height="{box_h}" rx="7" '
            f'fill="{color}" stroke="#a8b5c8"/>'
        )
        parts.append(
            f'<text x="{in_x+box_w/2}" y="{py+30}" text-anchor="middle" '
            f'class="label">{label}</text>'
        )
        parts.append(
            f'<text x="{kernel_x}" y="{py+29}" text-anchor="middle" class="small">'
            f'× K{idx+1}</text>'
        )
        parts.append(_arrow(kernel_x + 24, py + 24, sum_x - 26, y + 170))
    parts.append(
        f'<circle cx="{sum_x}" cy="{y+170}" r="24" fill="#e9f7f2" '
        'stroke="#8ccdbb" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{sum_x}" y="{y+176}" text-anchor="middle" class="small">Σ+b</text>'
    )
    parts.append(_arrow(sum_x + 26, y + 170, out_x - 27, y + 170))
    parts.append(
        f'<rect x="{out_x-26}" y="{y+140}" width="52" height="60" rx="8" '
        'fill="#edf3ff" stroke="#8faee8"/>'
    )
    parts.append(
        f'<text x="{out_x}" y="{y+174}" text-anchor="middle" class="small">1 map</text>'
    )
    parts.append(
        f'<text x="{x+16}" y="{y+h-25}" class="small">'
        "one 3×3×C_in filter → one output channel</text>"
    )
    return "".join(parts)

def _output_channels(x, y, w, h):
    """C_out different filters produce C_out feature maps."""
    parts = []
    for idx in range(3):
        yy = y + 80 + idx * 83
        parts.append(
            f'<rect x="{x+30}" y="{yy}" width="92" height="54" rx="8" '
            'fill="#f3f7fe" stroke="#9bb5e5"/>'
        )
        parts.append(
            f'<text x="{x+76}" y="{yy+33}" text-anchor="middle" class="small">'
            f'filter {idx+1}</text>'
        )
        parts.append(_arrow(x + 126, yy + 27, x + 190, yy + 27))
        parts.append(
            f'<rect x="{x+200}" y="{yy-4}" width="82" height="62" rx="8" '
            f'fill="{"#edf3ff" if idx==0 else "#e9f7f2" if idx==1 else "#fff1e7"}" '
            'stroke="#a8b5c8"/>'
        )
        parts.append(
            f'<text x="{x+241}" y="{yy+32}" text-anchor="middle" class="small">'
            f'channel {idx+1}</text>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+h-28}" class="small">'
        "output depth = number of filters (C_out)</text>"
    )
    return "".join(parts)


def _receptive_field_growth(x, y, w, h):
    """Three stride-1 3×3 convolutions grow theoretical receptive field 3→5→7."""
    sizes = [(3, 82), (5, 126), (7, 170)]
    parts = []
    for idx, (rf, box) in enumerate(sizes):
        cx = x + 80 + idx * ((w - 160) / 2)
        cy = y + h * 0.53
        parts.append(
            f'<rect x="{cx-box/2}" y="{cy-box/2}" width="{box}" height="{box}" '
            'fill="none" stroke="#8faee8" stroke-width="3"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{y+48}" text-anchor="middle" class="small">'
            f'{idx+1} layer{"s" if idx else ""}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{cy+7}" text-anchor="middle" class="label">'
            f'{rf}×{rf}</text>'
        )
    parts.append(
        f'<text x="{x+w/2}" y="{y+h-28}" text-anchor="middle" class="small">'
        "stride 1, no dilation: receptive field 3→5→7</text>"
    )
    return "".join(parts)



def _patch_tokens(x, y, w, h):
    parts = [_grid(x + 28, y + 78, 4, 4, 34, "blue", [0, 5, 10, 15])]
    parts.append(_arrow(x + 172, y + 145, x + 205, y + 145))
    for idx in range(4):
        parts.append(
            f'<rect x="{x+218}" y="{y+70+idx*58}" width="{w-244}" height="34" rx="7" '
            'fill="#edf3ff" stroke="#8faee8"/>'
        )
        parts.append(
            f'<text x="{x+(w+192)/2}" y="{y+92+idx*58}" '
            f'text-anchor="middle" class="small">token {idx+1}</text>'
        )
    parts.append(
        f'<text x="{x+16}" y="{y+h-24}" class="small">'
        "patch → flatten → linear projection</text>"
    )
    return "".join(parts)


def _attention_qkv(x, y, w, h):
    """Scaled dot-product attention within a narrow three-panel layout."""
    parts = []
    qx = x + 20
    box_w = 78
    ys = [y+82, y+158, y+234]
    labels = ["Q=XWQ", "K=XWK", "V=XWV"]
    score_x = x + w * 0.55
    out_x = x + w - 43
    for yy, label in zip(ys, labels):
        parts.append(
            f'<rect x="{qx}" y="{yy-20}" width="{box_w}" height="40" rx="7" '
            'fill="#edf3ff" stroke="#8faee8"/>'
        )
        parts.append(
            f'<text x="{qx+box_w/2}" y="{yy+5}" text-anchor="middle" '
            f'class="small">{label}</text>'
        )
    parts.append(_arrow(qx+box_w+2, ys[0], score_x-42, y+118))
    parts.append(_arrow(qx+box_w+2, ys[1], score_x-42, y+118))
    parts.append(
        f'<rect x="{score_x-40}" y="{y+88}" width="80" height="60" rx="8" '
        'fill="#fff1e7" stroke="#e0ae82"/>'
    )
    parts.append(
        f'<text x="{score_x}" y="{y+112}" text-anchor="middle" class="small">softmax</text>'
    )
    parts.append(
        f'<text x="{score_x}" y="{y+135}" text-anchor="middle" class="small">'
        "QKᵀ/√d</text>"
    )
    parts.append(_arrow(score_x+42, y+118, out_x-28, y+170))
    parts.append(_arrow(qx+box_w+2, ys[2], out_x-28, y+190))
    parts.append(
        f'<rect x="{out_x-27}" y="{y+145}" width="54" height="70" rx="8" '
        'fill="#e9f7f2" stroke="#8ccdbb"/>'
    )
    parts.append(
        f'<text x="{out_x}" y="{y+174}" text-anchor="middle" class="small">A·V</text>'
    )
    parts.append(
        f'<text x="{out_x}" y="{y+197}" text-anchor="middle" class="small">output</text>'
    )
    parts.append(
        f'<text x="{x+16}" y="{y+h-24}" class="small">'
        "A = softmax(QKᵀ/√dₖ)</text>"
    )
    return "".join(parts)

def _multihead_attention(x, y, w, h):
    parts = []
    in_x = x + 45
    head_x = x + w * 0.46
    out_x = x + w - 60
    parts.append(
        f'<rect x="{in_x-28}" y="{y+150}" width="56" height="46" rx="8" '
        'fill="#edf3ff" stroke="#8faee8"/>'
    )
    parts.append(f'<text x="{in_x}" y="{y+179}" text-anchor="middle" class="small">X</text>')
    ys = [y+90, y+155, y+220]
    for idx, yy in enumerate(ys):
        parts.append(_arrow(in_x+30, y+173, head_x-42, yy))
        parts.append(
            f'<rect x="{head_x-40}" y="{yy-20}" width="80" height="40" rx="8" '
            'fill="#f3f7fe" stroke="#9bb5e5"/>'
        )
        parts.append(f'<text x="{head_x}" y="{yy+5}" text-anchor="middle" class="small">head {idx+1}</text>')
        parts.append(_arrow(head_x+42, yy, out_x-38, y+155))
    parts.append(
        f'<rect x="{out_x-36}" y="{y+128}" width="72" height="54" rx="8" '
        'fill="#e9f7f2" stroke="#8ccdbb"/>'
    )
    parts.append(f'<text x="{out_x}" y="{y+151}" text-anchor="middle" class="small">concat</text>')
    parts.append(f'<text x="{out_x}" y="{y+171}" text-anchor="middle" class="small">Wᴼ</text>')
    parts.append(
        f'<text x="{x+18}" y="{y+h-28}" class="small">'
        "each head has its own Q/K/V projections</text>"
    )
    return "".join(parts)



def _bernoulli_binomial(x, y, w, h):
    """Bernoulli trials and an exact Binomial(N=8,p=0.5) shape."""
    parts = []
    trials = [1, 0, 1, 1, 0, 1, 0, 1]
    for idx, val in enumerate(trials):
        cx = x + 38 + idx * 44
        color = "#2454d8" if val else "#e0ae82"
        parts.append(f'<circle cx="{cx}" cy="{y+105}" r="14" fill="{color}"/>')
        parts.append(
            f'<text x="{cx}" y="{y+111}" text-anchor="middle" class="white">'
            f'{val}</text>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+38}" class="small">'
        "one Bernoulli sequence (example)</text>"
    )
    parts.append(
        f'<text x="{x+18}" y="{y+168}" class="small">'
        "Binomial PMF example: N=8, p=0.5</text>"
    )
    coefficients = [1, 8, 28, 56, 70, 56, 28, 8, 1]
    max_c = max(coefficients)
    for m, coeff in enumerate(coefficients):
        height = 112 * coeff / max_c
        xx = x + 30 + m * 43
        parts.append(
            f'<rect x="{xx}" y="{y+h-52-height}" width="24" height="{height}" '
            'rx="3" fill="#91abe2"/>'
        )
        parts.append(
            f'<text x="{xx+12}" y="{y+h-30}" text-anchor="middle" class="small">'
            f'{m}</text>'
        )
    parts.append(
        f'<text x="{x+w-95}" y="{y+h-10}" class="small">success count m</text>'
    )
    return "".join(parts)

def _ml_map(x, y, w, h):
    """Illustrate ML as likelihood mode and MAP as posterior mode."""
    left = x + 42
    right = x + w - 25
    base = y + h - 48
    ml_x = x + w * 0.68
    prior_x = x + w * 0.42
    map_x = x + w * 0.56
    parts = [
        f'<path d="M{left} {base} H{right}" class="thin"/>',
        f'<path d="M{left+5} {base} C{x+w*.35} {base} {x+w*.52} {y+72} '
        f'{ml_x} {y+72} C{x+w*.82} {y+72} {x+w*.88} {base} {right} {base}" '
        'stroke="#2454d8" stroke-width="4" fill="none"/>',
        f'<path d="M{left+5} {base} C{x+w*.20} {base} {x+w*.30} {y+130} '
        f'{prior_x} {y+130} C{x+w*.55} {y+130} {x+w*.68} {base} {right} {base}" '
        'stroke="#e0ae82" stroke-width="3" fill="none"/>',
        f'<path d="M{left+5} {base} C{x+w*.30} {base} {x+w*.43} {y+92} '
        f'{map_x} {y+92} C{x+w*.68} {y+92} {x+w*.77} {base} {right} {base}" '
        'stroke="#08796f" stroke-width="4" fill="none"/>',
        f'<path d="M{ml_x} {y+62} V{base}" stroke="#2454d8" stroke-width="2" stroke-dasharray="5 4"/>',
        f'<path d="M{map_x} {y+82} V{base}" stroke="#08796f" stroke-width="2" stroke-dasharray="5 4"/>',
        f'<text x="{x+18}" y="{y+38}" class="small" fill="#2454d8">likelihood p(D|θ)</text>',
        f'<text x="{x+130}" y="{y+38}" class="small" fill="#a24d18">prior p(θ)</text>',
        f'<text x="{x+220}" y="{y+38}" class="small" fill="#08796f">posterior ∝ product</text>',
        f'<text x="{ml_x}" y="{base+25}" text-anchor="middle" class="small">ML</text>',
        f'<text x="{map_x}" y="{base+25}" text-anchor="middle" class="small">MAP</text>',
    ]
    return "".join(parts)

def _gmm_responsibility(x, y, w, h):
    """Soft component assignments for overlapping Gaussian components."""
    parts = [
        f'<path d="M{x+35} {y+h-40} H{x+w-20} M{x+35} {y+h-40} V{y+45}" class="thin"/>'
    ]
    points = [
        (.20,.70,.92),(.28,.61,.83),(.38,.55,.66),(.49,.48,.50),
        (.60,.43,.30),(.70,.35,.15),(.80,.29,.06),
    ]
    for px, py, r1 in points:
        cx = x + px*w
        cy = y + py*h
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="#2454d8" opacity="{r1:.2f}"/>'
        )
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="#08796f" opacity="{1-r1:.2f}"/>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+35}" class="small">'
        "γₙₖ = p(zₖ=1|xₙ): soft assignment</text>"
    )
    return "".join(parts)


def _ppca_subspace(x, y, w, h):
    """PPCA density concentrated around a linear latent subspace with isotropic noise."""
    parts = [
        f'<path d="M{x+35} {y+h-35} H{x+w-20} M{x+35} {y+h-35} V{y+35}" class="thin"/>',
        f'<path d="M{x+55} {y+h-70} L{x+w-45} {y+70}" '
        'stroke="#a24d18" stroke-width="4"/>',
    ]
    pts = [
        (.18,.73),(.27,.66),(.35,.61),(.43,.55),(.52,.46),
        (.60,.43),(.69,.34),(.77,.31),(.84,.24),
    ]
    offsets = [-14, 11, -9, 18, -13, 9, -16, 12, -8]
    for (px, py), off in zip(pts, offsets):
        cx = x + px*w
        cy = y + py*h + off
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#2454d8"/>')
    parts.append(
        f'<text x="{x+18}" y="{y+35}" class="small">'
        "x = Wz + μ + ε, with isotropic ε around the linear subspace</text>"
    )
    return "".join(parts)


def _linear_regression_scatter(x, y, w, h):
    """Observed targets with a fitted straight regression line and residuals."""
    left = x + 38
    right = x + w - 22
    top = y + 48
    bottom = y + h - 42
    parts = [
        f'<path d="M{left} {bottom} H{right} M{left} {bottom} V{top}" class="thin"/>',
        f'<path d="M{left+8} {bottom-30} L{right-8} {top+35}" '
        'stroke="#2454d8" stroke-width="4"/>',
    ]
    points = [
        (.16,.76,.71),(.28,.66,.62),(.40,.61,.53),
        (.53,.47,.43),(.66,.38,.34),(.80,.22,.23)
    ]
    for px, py, fit_py in points:
        sx = x + px*w
        sy = y + py*h
        fy = y + fit_py*h
        parts.append(
            f'<path d="M{sx} {sy} V{fy}" stroke="#a8b5c8" '
            'stroke-width="2" stroke-dasharray="4 4"/>'
        )
        parts.append(f'<circle cx="{sx}" cy="{sy}" r="6" fill="#203455"/>')
    parts.append(
        f'<text x="{x+18}" y="{y+35}" class="small">'
        "linear mean function; vertical gaps are residuals</text>"
    )
    return "".join(parts)



def _svm_margin(x, y, w, h):
    """Consistent 2D maximum-margin sketch with support vectors on margins."""
    parts = [
        f'<path d="M{x+25} {y+h-30} H{x+w-20} '
        f'M{x+25} {y+h-30} V{y+35}" class="thin"/>'
    ]
    a = [(0.18,0.72),(0.28,0.60),(0.34,0.76),(0.22,0.45),(0.42,0.55)]
    b = [(0.62,0.30),(0.72,0.42),(0.77,0.24),(0.66,0.58),(0.84,0.48)]
    for px, py in a:
        parts.append(
            f'<circle cx="{x+px*w}" cy="{y+py*h}" r="8" fill="#2454d8"/>'
        )
    for px, py in b:
        parts.append(
            f'<circle cx="{x+px*w}" cy="{y+py*h}" r="8" fill="#08796f"/>'
        )

    margin_left = x + w * .42
    boundary = x + w * .52
    margin_right = x + w * .62
    parts.append(
        f'<path d="M{boundary} {y+35} V{y+h-30}" '
        'stroke="#a24d18" stroke-width="4"/>'
    )
    parts.append(
        f'<path d="M{margin_left} {y+35} V{y+h-30} '
        f'M{margin_right} {y+35} V{y+h-30}" '
        'stroke="#89a9ec" stroke-width="3" stroke-dasharray="8 6"/>'
    )
    for cx, cy in [
        (margin_left, y + h * .55),
        (margin_right, y + h * .30),
    ]:
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="15" fill="none" '
            'stroke="#a24d18" stroke-width="3"/>'
        )
    parts.append(
        f'<text x="{x+18}" y="{y+35}" class="small">'
        "support vectors lie on the displayed margin</text>"
    )
    return "".join(parts)

def _em_cycle(x, y, w, h):
    """EM alternates E-step responsibilities and M-step parameter updates."""
    cx = x + w / 2
    top_y = y + 82
    left_x = x + 90
    right_x = x + w - 90
    bottom_y = y + h - 78
    parts = [
        f'<rect x="{cx-48}" y="{top_y-22}" width="96" height="44" rx="8" '
        'fill="#edf3ff" stroke="#8faee8"/>',
        f'<text x="{cx}" y="{top_y+5}" text-anchor="middle" class="small">parameters θ</text>',
        f'<rect x="{right_x-50}" y="{bottom_y-22}" width="100" height="44" rx="8" '
        'fill="#fff1e7" stroke="#e0ae82"/>',
        f'<text x="{right_x}" y="{bottom_y+5}" text-anchor="middle" class="small">E: γₙₖ</text>',
        f'<rect x="{left_x-50}" y="{bottom_y-22}" width="100" height="44" rx="8" '
        'fill="#e9f7f2" stroke="#8ccdbb"/>',
        f'<text x="{left_x}" y="{bottom_y+5}" text-anchor="middle" class="small">M: update θ</text>',
        _arrow(cx+30, top_y+24, right_x-18, bottom_y-24),
        _arrow(right_x-52, bottom_y, left_x+52, bottom_y),
        _arrow(left_x+5, bottom_y-24, cx-28, top_y+24),
        f'<text x="{x+18}" y="{y+h-28}" class="small">'
        "repeat until the objective stops improving appreciably</text>",
    ]
    return "".join(parts)

def _panel_content(kind, x, y, w, h, data):
    if kind=="linear_regression_scatter":
        return _linear_regression_scatter(x,y,w,h)
    if kind=="svm_margin":
        return _svm_margin(x,y,w,h)
    if kind=="em_cycle":
        return _em_cycle(x,y,w,h)
    if kind=="split_roles":
        return _split_roles(x,y,w,h)
    if kind=="score_axis":
        return _score_axis(x,y,w,h)
    if kind=="momentum_update":
        return _momentum_update(x,y,w,h)
    if kind=="landscape_regions":
        return _landscape_regions(x,y,w,h)
    if kind=="svm_hinge":
        return _svm_hinge(x,y,w,h)
    if kind=="multiclass_regions":
        return _multiclass_regions(x,y,w,h)
    if kind=="ensemble_parallel":
        return _ensemble_parallel(x,y,w,h)
    if kind=="moe_routing":
        return _moe_routing(x,y,w,h)
    if kind=="iou_boxes":
        return _iou_boxes(x,y,w,h)
    if kind=="semantic_instance_masks":
        return _semantic_instance_masks(x,y,w,h)
    if kind=="nms_visual":
        return _nms_visual(x,y,w,h)
    if kind=="architecture_compare":
        return _architecture_compare(x,y,w,h)
    if kind=="conv_channel_sum":
        return _conv_channel_sum(x,y,w,h)
    if kind=="output_channels":
        return _output_channels(x,y,w,h)
    if kind=="receptive_field_growth":
        return _receptive_field_growth(x,y,w,h)
    if kind=="patch_tokens":
        return _patch_tokens(x,y,w,h)
    if kind=="attention_qkv":
        return _attention_qkv(x,y,w,h)
    if kind=="multihead_attention":
        return _multihead_attention(x,y,w,h)
    if kind=="bernoulli_binomial":
        return _bernoulli_binomial(x,y,w,h)
    if kind=="ml_map":
        return _ml_map(x,y,w,h)
    if kind=="gmm_responsibility":
        return _gmm_responsibility(x,y,w,h)
    if kind=="ppca_subspace":
        return _ppca_subspace(x,y,w,h)
    if kind=="linear_score_matrix":
        return _linear_score_matrix(x,y,w,h)
    if kind=="chain_rule_numeric":
        return _chain_rule_numeric(x,y,w,h)
    if kind=="gradient_check":
        return _gradient_check(x,y,w,h)
    if kind=="optimizer_paths":
        return _optimizer_paths(x,y,w,h)
    if kind=="lr_curves":
        return _lr_curves(x,y,w,h)
    if kind=="init_variance":
        return _init_variance(x,y,w,h)
    if kind=="pool_compare":
        return _pool_compare(x,y,w,h)
    if kind=="residual_flow":
        return _residual_flow(x,y,w,h)
    if kind=="entropy_curve":
        return _entropy_curve(x,y,w,h)
    if kind=="regression_uncertainty":
        return _regression_uncertainty(x,y,w,h)
    if kind=="importance_sampling":
        return _importance_sampling(x,y,w,h)
    if kind=="pca_projection":
        return _pca_projection(x,y,w,h)
    if kind=="knn":
        return _scatter(x,y,w,h,"curve",True)
    if kind=="knn_semantics":
        return _knn_semantics(x,y,w,h)
    if kind=="grouped_split":
        return _grouped_split(x,y,w,h)
    if kind=="score_softmax_ce":
        return _score_softmax_ce(x,y,w,h)
    if kind=="loss_compare":
        return _loss_compare(x,y,w,h)
    if kind=="activation_gradients":
        return _activation_gradients(x,y,w,h)
    if kind=="batchnorm_modes":
        return _batchnorm_modes(x,y,w,h)
    if kind=="augmentation_cards":
        return _augmentation_cards(x,y,w,h)
    if kind=="invariance_checks":
        return _invariance_checks(x,y,w,h)
    if kind=="numeric_conv":
        return _numeric_conv(x,y,w,h)
    if kind=="conv_controls":
        return _conv_controls(x,y,w,h)
    if kind=="modern_visual":
        return _modern_visual(x,y,w,h)
    if kind=="bayes_update":
        return _bayes_update_density(x,y,w,h)
    if kind=="bayes_risk":
        return _bayes_risk(x,y,w,h)
    if kind=="covariance_ellipse":
        return _covariance_ellipse(x,y,w,h)
    if kind=="basis_functions":
        return _basis_functions(x,y,w,h)
    if kind=="factor_graph":
        return _factor_graph(x,y,w,h)
    if kind=="posterior_approx":
        return _posterior_approx(x,y,w,h)
    if kind=="elbo_decomp":
        return _elbo_decomposition(x,y,w,h)
    if kind=="mc_samples":
        return _mc_samples(x,y,w,h)
    if kind=="mcmc_path":
        return _mcmc_path(x,y,w,h)
    if kind=="hmm_tasks":
        return _hmm_tasks(x,y,w,h)
    if kind=="vision_bridge":
        return _vision_bridge(x,y,w,h)
    if kind=="scatter_linear":
        return _scatter(x,y,w,h,"linear",False,data.get("margin",False))
    if kind=="scatter_curve":
        return _scatter(x,y,w,h,"curve")
    if kind=="pipeline":
        return _pipeline(x,y,w,h,data["steps"])
    if kind=="bars":
        return _bars(x,y,w,h,data["labels"],data["values"],data.get("horizontal",True))
    if kind=="curve":
        return _curves(x,y,w,h,data["curve"])
    if kind=="network":
        return _network(x,y,w,h,tuple(data.get("counts",(3,4,2))),data.get("dropout",False))
    if kind=="matrix":
        return _grid(x+30,y+55,data.get("rows",5),data.get("cols",6),data.get("cell",30),data.get("mode","blue"),data.get("hot"))
    if kind=="heatmap":
        return _heatmap(x,y,w,h)
    if kind=="task":
        return _task_panel(x,y,w,h,data["mode"])
    if kind=="distribution":
        return _distribution(x,y,w,h,data.get("mode","gaussian"))
    if kind=="graphical":
        return _graphical(x,y,w,h,data.get("undirected",False))
    if kind=="pca":
        return _pca(x,y,w,h)
    if kind=="hmm":
        return _hmm(x,y,w,h)
    if kind=="landscape":
        parts=[
            f'<ellipse cx="{x+w*.55}" cy="{y+h*.50}" rx="{w*.35}" ry="{h*.30}" fill="none" stroke="#c7d2e4" stroke-width="2"/>',
            f'<ellipse cx="{x+w*.55}" cy="{y+h*.50}" rx="{w*.25}" ry="{h*.20}" fill="none" stroke="#aebeda" stroke-width="2"/>',
            f'<ellipse cx="{x+w*.55}" cy="{y+h*.50}" rx="{w*.13}" ry="{h*.10}" fill="none" stroke="#89a9ec" stroke-width="2"/>',
            f'<path d="M{x+w*.18} {y+h*.76} C{x+w*.30} {y+h*.35} {x+w*.48} {y+h*.70} {x+w*.57} {y+h*.50}" stroke="#a24d18" stroke-width="4" fill="none"/>',
        ]
        return "".join(parts)
    if kind=="conv":
        parts=[_grid(x+25,y+65,5,5,27,"gray",[2,7,12]), _grid(x+w*.43,y+90,3,3,32,"green",[2,5,8])]
        parts.append(_arrow(x+w*.34,y+h*.48,x+w*.41,y+h*.48))
        parts.append(_arrow(x+w*.61,y+h*.48,x+w*.72,y+h*.48))
        parts.append(_grid(x+w*.74,y+85,3,3,32,"blue",[1,4,7]))
        return "".join(parts)
    if kind=="fcconv":
        parts=[]
        inputs=[]
        outputs=[]
        for i in range(4):
            for j in range(4):
                point=(x+50+i*32, y+80+j*32)
                inputs.append(point)
                parts.append(f'<circle cx="{point[0]}" cy="{point[1]}" r="5" fill="#89a9ec"/>')
        for j in range(5):
            point=(x+w-55, y+70+j*38)
            outputs.append(point)
            parts.append(f'<circle cx="{point[0]}" cy="{point[1]}" r="8" fill="#2454d8"/>')
        for ix,iy in inputs:
            for ox,oy in outputs:
                parts.append(
                    f'<path d="M{ix+6} {iy} L{ox-9} {oy}" '
                    'stroke="#c6d0de" stroke-width="0.8" opacity=".55"/>'
                )
        return "".join(parts)
    if kind=="architecture":
        parts=[]
        names=data["names"]
        for i,name in enumerate(names):
            xx=x+30+i*(w-60)/len(names)
            bw=(w-80)/len(names)
            parts.append(f'<rect x="{xx}" y="{y+60}" width="{bw-10}" height="{h-110}" rx="10" fill="{"#edf3ff" if i%2==0 else "#e9f7f2"}" stroke="#c5d3e8"/>')
            parts.append(f'<text x="{xx+(bw-10)/2}" y="{y+90}" text-anchor="middle" class="body">{_e(name)}</text>')
            for k in range(3+i%3):
                parts.append(f'<rect x="{xx+15}" y="{y+120+k*35}" width="{bw-40}" height="20" rx="5" fill="#9bb5e5"/>')
        return "".join(parts)
    if kind=="text":
        return "".join(f'<text x="{x+35}" y="{y+75+i*42}" class="body">• {_e(line)}</text>' for i,line in enumerate(data["lines"]))
    return ""


def _render(spec):
    panels=spec["panels"]
    n=len(panels)
    gap=22
    margin=35
    total_w=1200-2*margin-gap*(n-1)
    pw=total_w/n
    y=115
    ph=420
    body=[]
    for i,p in enumerate(panels):
        x=margin+i*(pw+gap)
        body.append(_panel_frame(x,y,pw,ph,chr(ord("a")+i),p["title"]))
        body.append(_panel_content(p["kind"],x+10,y+40,pw-20,ph-50,p))
    return _svg(spec["title"],spec["subtitle"],"".join(body),590)


FIGURES = {
    # CS231n — classification / linear
    "cs-knn-distance.svg": dict(title="kNN and pixel-space distance",subtitle="Raw-pixel distance can disagree with semantic similarity.",panels=[
        dict(title="k nearest neighbors",kind="knn"),
        dict(title="pixel distance failure cases",kind="knn_semantics"),
    ]),
    "cs-split.svg": dict(title="Train / validation / test",subtitle="Validation guides choices; grouped splitting keeps near-duplicates from leaking across sets.",panels=[
        dict(title="distinct data roles",kind="split_roles"),
        dict(title="random frames vs grouped sources",kind="grouped_split"),
    ]),
    "cs-linear-score.svg": dict(title="Linear classifier",subtitle="A single affine transformation maps an input vector to K class scores.",panels=[
        dict(title="x · W · b → class scores",kind="linear_score_matrix"),
        dict(title="same scores on a real-valued axis",kind="score_axis"),
    ]),
    "cs-softmax-loss.svg": dict(title="Softmax and classification losses",subtitle="Scores become probabilities, then the loss converts confidence or margin into a penalty.",panels=[
        dict(title="scores → softmax → CE",kind="score_softmax_ce"),
        dict(title="cross-entropy vs hinge",kind="loss_compare"),
    ]),
    "cs-decision-boundary.svg": dict(title="Decision boundaries",subtitle="Linear models split feature space with hyperplanes; nonlinear models bend that boundary.",panels=[
        dict(title="linear boundary",kind="scatter_linear"),
        dict(title="nonlinear boundary",kind="scatter_curve"),
    ]),
    # optimization
    "cs-computational-chain.svg": dict(title="Computational graph and chain rule",subtitle="Backpropagation is repeated local differentiation through a graph.",panels=[
        dict(title="numeric forward / backward",kind="chain_rule_numeric"),
        dict(title="analytic vs numerical gradient",kind="gradient_check"),
    ]),
    "cs-optimizers.svg": dict(title="SGD, Momentum and Adam",subtitle="Illustrative trajectories: the exact path depends on the objective, initialization and hyperparameters.",panels=[
        dict(title="schematic optimizer trajectories",kind="optimizer_paths"),
        dict(title="momentum combines gradient and velocity",kind="momentum_update"),
    ]),
    "cs-lr-saddle.svg": dict(title="Learning rate, minima and saddle points",subtitle="Step size changes convergence behavior; nonconvex landscapes also contain flat and saddle regions.",panels=[
        dict(title="loss vs step for three learning rates",kind="lr_curves"),
        dict(title="minimum / saddle / flat region",kind="landscape_regions"),
    ]),
    # NN/training tricks
    "cs-activations.svg": dict(title="Activation functions",subtitle="Activation shape and derivative shape jointly control information and gradient flow.",panels=[
        dict(title="ReLU / sigmoid / tanh",kind="curve",curve="activations"),
        dict(title="gradient behavior",kind="activation_gradients"),
    ]),
    "cs-init-bn.svg": dict(title="Initialization and Batch Normalization",subtitle="Initialization controls signal scale; BatchNorm uses different statistics in training and evaluation.",panels=[
        dict(title="activation variance by initialization",kind="init_variance"),
        dict(title="BatchNorm: train vs eval",kind="batchnorm_modes"),
    ]),
    "cs-reg-dropout.svg": dict(title="Regularization and dropout",subtitle="Regularization constrains the solution; dropout injects stochastic masking during training.",panels=[
        dict(title="weight regularization",kind="curve",curve="regularization"),
        dict(title="dropout network",kind="network",counts=(3,5,2),dropout=True),
    ]),
    "cs-training-diagnostics.svg": dict(title="Training diagnostics",subtitle="Loss curves and confusion patterns tell you what to inspect next.",panels=[
        dict(title="train / validation loss",kind="curve",curve="train_val"),
        dict(title="confusion pattern",kind="matrix",rows=2,cols=2,cell=70,mode="heat",hot=[0,3]),
    ]),
    "cs-augmentation.svg": dict(title="Data augmentation",subtitle="An augmentation is valid only when it preserves the target semantics for the specific task.",panels=[
        dict(title="image-like transforms",kind="augmentation_cards"),
        dict(title="label-invariance check",kind="invariance_checks"),
    ]),
    # CNN
    "cs-conv-shape.svg": dict(title="Convolution, stride and padding",subtitle="A convolution is a local dot product; stride, padding and dilation change how that dot product is sampled.",panels=[
        dict(title="3×3 numeric convolution",kind="numeric_conv"),
        dict(title="stride / padding / dilation",kind="conv_controls"),
    ]),
    "cs-pooling-hierarchy.svg": dict(title="Pooling and feature hierarchy",subtitle="Spatial summarization and depth transform low-level responses into more task-specific features.",panels=[
        dict(title="max pooling vs average pooling",kind="pool_compare"),
        dict(title="typical hierarchy (not a fixed rule)",kind="pipeline",steps=["local patterns","textures / motifs","larger structures","task-dependent features"]),
    ]),
    "cs-fc-conv.svg": dict(title="Fully connected vs convolutional connectivity",subtitle="Fully connected layers connect everything; convolution reuses local weights over space.",panels=[
        dict(title="dense connectivity",kind="fcconv"),
        dict(title="shared local filters",kind="conv"),
    ]),
    "cs-conv-channels-rf.svg": dict(title="Multi-channel convolution and receptive field",subtitle="Filters span input channels; different filters create output channels, while stacked kernels expand receptive fields.",panels=[
        dict(title="RGB channels summed by one filter",kind="conv_channel_sum"),
        dict(title="multiple filters → output channels",kind="output_channels"),
        dict(title="3×3 stack: receptive field 3→5→7",kind="receptive_field_growth"),
    ]),
    # architectures / transfer / tasks
    "cs-architectures-residual.svg": dict(title="Architecture motifs and residual learning",subtitle="High-level motifs only: these blocks summarize design ideas, not exact layer-by-layer architectures.",panels=[
        dict(title="architecture motifs",kind="architecture_compare"),
        dict(title="residual block and gradient shortcut",kind="residual_flow"),
    ]),
    "cs-transfer.svg": dict(title="Transfer learning and fine-tuning",subtitle="Reuse pretrained representations, then decide how much of the backbone to update.",panels=[
        dict(title="feature extractor",kind="pipeline",steps=["pretrained","freeze","new head","validate"]),
        dict(title="fine-tuning",kind="pipeline",steps=["pretrained","unfreeze top","small LR","validate"]),
    ]),
    "cs-task-suite.svg": dict(title="Classification, detection and segmentation",subtitle="Vision tasks differ mainly in the spatial precision required from the output.",panels=[
        dict(title="classification",kind="task",mode="classification"),
        dict(title="detection",kind="task",mode="detection"),
        dict(title="segmentation",kind="task",mode="segmentation"),
    ]),
    "cs-iou-nms-instance.svg": dict(title="IoU, semantic/instance masks and NMS",subtitle="IoU measures overlap; instance segmentation separates object identities; NMS removes redundant high-overlap detections.",panels=[
        dict(title="box IoU",kind="iou_boxes"),
        dict(title="semantic vs instance masks",kind="semantic_instance_masks"),
        dict(title="greedy NMS",kind="nms_visual"),
    ]),
    "cs-visualization.svg": dict(title="Model visualization",subtitle="Attribution tools are diagnostics, not guaranteed causal explanations.",panels=[
        dict(title="saliency / heatmap",kind="heatmap"),
        dict(title="feature maps",kind="matrix",rows=4,cols=5,cell=38,mode="gray",hot=[2,8,13,17]),
    ]),
    "cs-modern.svg": dict(title="Modern CS231n topics",subtitle="Attention, self-distillation, vision-language alignment and denoising are distinct representation-learning patterns.",panels=[
        dict(title="representation learning",kind="pipeline",steps=["unlabeled images","augment/views","encoder","representation"]),
        dict(title="attention / CLIP / DINO / diffusion",kind="modern_visual"),
    ]),

    "cs-attention.svg": dict(title="Vision Transformer attention mechanics",subtitle="ViT converts patches to tokens; attention uses Q/K/V scores, then combines several attention heads.",panels=[
        dict(title="patches → token embeddings",kind="patch_tokens"),
        dict(title="scaled dot-product attention",kind="attention_qkv"),
        dict(title="multi-head attention",kind="multihead_attention"),
    ]),

    # PRML
    "prml-bayes-density.svg": dict(title="Bayes update and decision risk",subtitle="Data reshapes uncertainty from prior to posterior; decisions then minimize expected risk.",panels=[
        dict(title="prior × likelihood → posterior",kind="bayes_update"),
        dict(title="Bayesian decision",kind="bayes_risk"),
        dict(title="binary entropy / information",kind="entropy_curve"),
    ]),
    "prml-gaussian-beta.svg": dict(title="Gaussian geometry and Beta-Binomial update",subtitle="Mean, variance and covariance shape Gaussian uncertainty; conjugate priors allow analytic updates.",panels=[
        dict(title="mean / variance",kind="curve",curve="gaussian"),
        dict(title="covariance ellipse",kind="covariance_ellipse"),
        dict(title="Beta prior → posterior",kind="distribution",mode="beta"),
    ]),
    "prml-discrete-map.svg": dict(title="Bernoulli, Binomial, maximum likelihood and MAP",subtitle="Bernoulli models one binary trial; Binomial counts successes; MAP combines likelihood with a prior.",panels=[
        dict(title="Bernoulli trials → Binomial count",kind="bernoulli_binomial"),
        dict(title="ML vs MAP estimate",kind="ml_map"),
    ]),
    "prml-regression-basis.svg": dict(title="Linear regression and basis expansion",subtitle="The model can stay linear in its weights while nonlinear basis functions reshape the input.",panels=[
        dict(title="linear regression fit + residuals",kind="linear_regression_scatter"),
        dict(title="nonlinear basis functions",kind="basis_functions"),
        dict(title="posterior predictive uncertainty",kind="regression_uncertainty"),
    ]),
    "prml-bias-reg.svg": dict(title="Bias–variance and regularization",subtitle="Model complexity trades approximation error against sensitivity to finite data.",panels=[
        dict(title="bias / variance trade-off",kind="curve",curve="bias_variance"),
        dict(title="regularization effect",kind="curve",curve="regularization"),
    ]),
    "prml-sigmoid-boundary.svg": dict(title="Logistic regression",subtitle="A linear score becomes a probability through the sigmoid, while the decision boundary remains linear.",panels=[
        dict(title="sigmoid",kind="curve",curve="sigmoid"),
        dict(title="binary decision boundary",kind="scatter_linear"),
    ]),
    "prml-multiclass.svg": dict(title="Multi-class classification",subtitle="A multiclass model produces one score or probability per class; prediction uses the largest resulting class value.",panels=[
        dict(title="example class probabilities",kind="bars",labels=["C1","C2","C3","C4"],values=[0.52,0.27,0.14,0.07]),
        dict(title="three-class decision regions",kind="multiclass_regions"),
    ]),
    "prml-nn-boundary.svg": dict(title="Neural networks as learned nonlinear basis functions",subtitle="Hidden units create a learned representation in which a simple output layer can solve nonlinear problems.",panels=[
        dict(title="hidden network",kind="network",counts=(3,5,2)),
        dict(title="nonlinear boundary",kind="scatter_curve"),
    ]),
    "prml-forward-backprop.svg": dict(title="Forward and backward computation",subtitle="Values move forward; derivatives move backward through the same graph.",panels=[
        dict(title="forward",kind="pipeline",steps=["input","hidden","output","loss"]),
        dict(title="backward derivatives",kind="pipeline",steps=["dL/dy","dL/dh","dL/dW"]),
    ]),
    "prml-kernel-feature.svg": dict(title="Feature space and the kernel trick",subtitle="A nonlinear problem in input space can correspond to a linear separator in a richer feature space.",panels=[
        dict(title="input space",kind="scatter_curve"),
        dict(title="feature space",kind="scatter_linear"),
    ]),
    "prml-svm.svg": dict(title="SVM margin and support vectors",subtitle="Only samples on or inside the margin determine the optimal separating hyperplane.",panels=[
        dict(title="margin and support vectors",kind="svm_margin"),
        dict(title="hinge loss vs functional margin",kind="svm_hinge"),
    ]),
    "prml-graph-mrf.svg": dict(title="Graphical model families",subtitle="Directed graphs, undirected graphs and factor graphs encode dependencies with different primitives.",panels=[
        dict(title="Bayesian network",kind="graphical",undirected=False),
        dict(title="Markov random field",kind="graphical",undirected=True),
        dict(title="factor graph",kind="factor_graph"),
    ]),
    "prml-gmm-em.svg": dict(title="Gaussian mixtures and EM",subtitle="A GMM represents density as a weighted sum of Gaussian components; EM alternates soft assignments and parameter updates.",panels=[
        dict(title="mixture components and density",kind="distribution",mode="mixture"),
        dict(title="soft responsibilities",kind="gmm_responsibility"),
        dict(title="E-step ↔ M-step cycle",kind="em_cycle"),
    ]),
    "prml-vi-elbo.svg": dict(title="Variational inference and ELBO",subtitle="A tractable q(z) approximates the posterior; maximizing ELBO tightens the lower bound and minimizes KL within the chosen variational family.",panels=[
        dict(title="target posterior vs q(z)",kind="posterior_approx"),
        dict(title="ELBO + KL = log evidence",kind="elbo_decomp"),
    ]),
    "prml-monte-mcmc.svg": dict(title="Monte Carlo and MCMC",subtitle="Monte Carlo estimates expectations with samples; MCMC uses a dependent chain designed to have the target as its stationary distribution under appropriate conditions.",panels=[
        dict(title="samples from a target density",kind="mc_samples"),
        dict(title="illustrative burn-in and dependent chain",kind="mcmc_path"),
        dict(title="importance sampling weights",kind="importance_sampling"),
    ]),
    "prml-pca-dim.svg": dict(title="PCA and dimensionality reduction",subtitle="Principal components align the coordinate system with directions of largest data variance.",panels=[
        dict(title="principal axes",kind="pca"),
        dict(title="2D → 1D projection and reconstruction",kind="pca_projection"),
    ]),
    "prml-ppca.svg": dict(title="Probabilistic PCA",subtitle="PPCA is a linear-Gaussian latent-variable model; isotropic observation noise spreads probability around the latent subspace.",panels=[
        dict(title="latent generative model",kind="pipeline",steps=["z ~ N(0,I)","Wz + μ","ε ~ N(0,σ²I)","x"]),
        dict(title="linear subspace + isotropic noise",kind="ppca_subspace"),
    ]),
    "prml-hmm-filter.svg": dict(title="Hidden Markov models, filtering and decoding",subtitle="The same state-space model supports filtering, prediction, smoothing and sequence decoding.",panels=[
        dict(title="state transitions",kind="hmm"),
        dict(title="filter / predict / smooth / Viterbi",kind="hmm_tasks"),
    ]),
    "prml-ensemble-moe.svg": dict(title="Ensembles and mixture of experts",subtitle="A committee evaluates models in parallel; a mixture of experts uses input-dependent gating weights to combine expert outputs.",panels=[
        dict(title="parallel committee averaging",kind="ensemble_parallel"),
        dict(title="input-dependent expert routing",kind="moe_routing"),
    ]),
    "prml-vision-bridge.svg": dict(title="PRML concepts inside modern Vision AI",subtitle="Probabilistic tools remain useful around deep networks for calibration, uncertainty, latent structure and temporal reasoning.",panels=[
        dict(title="model output",kind="pipeline",steps=["image","network","score/probability","decision"]),
        dict(title="probabilistic engineering tools",kind="vision_bridge"),
    ]),
}


REFERENCE_FIGURE_META = {
    name: (spec["title"], spec["subtitle"]) for name, spec in FIGURES.items()
}


REFERENCE_VISUALS = {
    ("cs231n","classification"): ["cs-knn-distance.svg","cs-split.svg"],
    ("cs231n","linear"): ["cs-linear-score.svg","cs-softmax-loss.svg","cs-decision-boundary.svg"],
    ("cs231n","optimization"): ["cs-computational-chain.svg","cs-optimizers.svg","cs-lr-saddle.svg"],
    ("cs231n","nn"): ["cs-activations.svg","cs-init-bn.svg","cs-reg-dropout.svg"],
    ("cs231n","training"): ["cs-training-diagnostics.svg","cs-augmentation.svg"],
    ("cs231n","cnn"): ["cs-conv-shape.svg","cs-conv-channels-rf.svg","cs-pooling-hierarchy.svg","cs-fc-conv.svg"],
    ("cs231n","architectures"): ["cs-architectures-residual.svg"],
    ("cs231n","visualization"): ["cs-visualization.svg"],
    ("cs231n","transfer"): ["cs-transfer.svg"],
    ("cs231n","modern"): ["cs-task-suite.svg","cs-iou-nms-instance.svg","cs-attention.svg","cs-modern.svg"],

    ("prml","ch1"): ["prml-bayes-density.svg"],
    ("prml","ch2"): ["prml-gaussian-beta.svg","prml-discrete-map.svg"],
    ("prml","ch3"): ["prml-regression-basis.svg","prml-bias-reg.svg"],
    ("prml","ch4"): ["prml-sigmoid-boundary.svg","prml-multiclass.svg"],
    ("prml","ch5"): ["prml-nn-boundary.svg","prml-forward-backprop.svg"],
    ("prml","ch6"): ["prml-kernel-feature.svg"],
    ("prml","ch7"): ["prml-svm.svg"],
    ("prml","ch8"): ["prml-graph-mrf.svg"],
    ("prml","ch9"): ["prml-gmm-em.svg"],
    ("prml","ch10"): ["prml-vi-elbo.svg"],
    ("prml","ch11"): ["prml-monte-mcmc.svg"],
    ("prml","ch12"): ["prml-pca-dim.svg","prml-ppca.svg"],
    ("prml","ch13"): ["prml-hmm-filter.svg"],
    ("prml","ch14"): ["prml-ensemble-moe.svg"],
    ("prml","vision-bridge"): ["prml-vision-bridge.svg"],
}


def build_reference_figures(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, spec in FIGURES.items():
        (output_dir / name).write_text(_render(spec), encoding="utf-8")
    return len(FIGURES)

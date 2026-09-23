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
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="panel"/>'
        f'<text x="{x+16}" y="{y+29}" class="panel-label">({letter})</text>'
        f'<text x="{x+52}" y="{y+29}" class="label">{_e(title)}</text>'
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
    parts=[f'<path d="M{x+35} {y+h-35} H{x+w-20}" class="thin"/>']
    if mode=="gaussian":
        parts.append(f'<path d="M{x+45} {y+h-40} C{x+w*.28} {y+h-40} {x+w*.34} {y+55} {x+w*.50} {y+55} C{x+w*.66} {y+55} {x+w*.72} {y+h-40} {x+w-35} {y+h-40}" stroke="#2454d8" stroke-width="4" fill="none"/>')
    elif mode=="mixture":
        parts.append(f'<path d="M{x+45} {y+h-40} C{x+w*.20} {y+h-40} {x+w*.25} {y+90} {x+w*.37} {y+90} C{x+w*.47} {y+90} {x+w*.50} {y+h-40} {x+w*.58} {y+h-40}" stroke="#2454d8" stroke-width="4" fill="none"/>')
        parts.append(f'<path d="M{x+w*.38} {y+h-40} C{x+w*.53} {y+h-40} {x+w*.58} {y+120} {x+w*.70} {y+120} C{x+w*.82} {y+120} {x+w*.85} {y+h-40} {x+w-35} {y+h-40}" stroke="#08796f" stroke-width="4" fill="none"/>')
    elif mode=="beta":
        parts.append(f'<path d="M{x+45} {y+h-40} C{x+w*.20} {y+120} {x+w*.37} {y+70} {x+w*.52} {y+95} C{x+w*.65} {y+120} {x+w*.78} {y+h-45} {x+w-35} {y+h-40}" stroke="#2454d8" stroke-width="4" fill="none"/>')
        parts.append(f'<path d="M{x+45} {y+h-40} C{x+w*.25} {y+h-35} {x+w*.40} {y+145} {x+w*.58} {y+75} C{x+w*.72} {y+55} {x+w*.83} {y+h-35} {x+w-35} {y+h-40}" stroke="#a24d18" stroke-width="4" fill="none"/>')
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
    parts=[f'<path d="M{x+35} {y+h-35} H{x+w-20} M{x+35} {y+h-35} V{y+35}" class="thin"/>']
    pts=[(.18,.72),(.27,.65),(.35,.60),(.43,.53),(.50,.47),(.59,.42),(.68,.35),(.77,.28),(.83,.25)]
    for px,py in pts:
        parts.append(f'<circle cx="{x+px*w}" cy="{y+py*h}" r="7" fill="#2454d8"/>')
    parts.append(f'<path d="M{x+45} {y+h-55} L{x+w-35} {y+50}" stroke="#a24d18" stroke-width="4"/>')
    parts.append(f'<path d="M{x+w*.38} {y+45} L{x+w*.62} {y+h-40}" stroke="#08796f" stroke-width="3"/>')
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


def _panel_content(kind, x, y, w, h, data):
    if kind=="knn":
        return _scatter(x,y,w,h,"curve",True)
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
        for i in range(4):
            for j in range(4):
                parts.append(f'<circle cx="{x+50+i*32}" cy="{y+80+j*32}" r="5" fill="#89a9ec"/>')
        for j in range(5):
            parts.append(f'<circle cx="{x+w-55}" cy="{y+70+j*38}" r="8" fill="#2454d8"/>')
        for i in range(0,4,2):
            for j in range(0,4,2):
                parts.append(f'<path d="M{x+50+i*32} {y+80+j*32} L{x+w-63} {y+70+(i+j)%5*38}" class="thin"/>')
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
    "cs-knn-distance.svg": dict(title="kNN and pixel-space distance",subtitle="Nearest-neighbor classification is simple, but raw-pixel distance is fragile.",panels=[
        dict(title="k nearest neighbors",kind="knn"),
        dict(title="distance is not semantics",kind="text",lines=["L1 / L2 compare numeric arrays","translation changes many pixels","illumination changes many values","feature learning becomes necessary"]),
    ]),
    "cs-split.svg": dict(title="Train / validation / test",subtitle="Hyperparameters belong to validation; test stays isolated until the end.",panels=[
        dict(title="data roles",kind="pipeline",steps=["Train","Validation","Model select","Test"]),
        dict(title="video leakage warning",kind="text",lines=["random frames can leak near-duplicates","group by source video / subject","fit preprocessing only on train","lock test before final evaluation"]),
    ]),
    "cs-linear-score.svg": dict(title="Linear classifier",subtitle="A single affine transformation maps an input vector to K class scores.",panels=[
        dict(title="score function",kind="pipeline",steps=["x","W·x+b","scores"]),
        dict(title="class-score bars",kind="bars",labels=["cat","dog","fox"],values=[0.82,0.31,0.12]),
    ]),
    "cs-softmax-loss.svg": dict(title="Softmax and classification losses",subtitle="Scores become probabilities with softmax; losses decide how mistakes are penalized.",panels=[
        dict(title="softmax / CE",kind="curve",curve="softmax_loss"),
        dict(title="hinge vs CE",kind="text",lines=["cross-entropy: −log p(correct)","hinge: margin violations only","same scores, different penalties","regularization is a separate term"]),
    ]),
    "cs-decision-boundary.svg": dict(title="Decision boundaries",subtitle="Linear models split feature space with hyperplanes; nonlinear models bend that boundary.",panels=[
        dict(title="linear boundary",kind="scatter_linear"),
        dict(title="nonlinear boundary",kind="scatter_curve"),
    ]),
    # optimization
    "cs-computational-chain.svg": dict(title="Computational graph and chain rule",subtitle="Backpropagation is repeated local differentiation through a graph.",panels=[
        dict(title="forward graph",kind="pipeline",steps=["x","multiply W","add b","loss"]),
        dict(title="backward chain",kind="pipeline",steps=["dL/dout","local derivative","chain rule","dL/dW"]),
    ]),
    "cs-optimizers.svg": dict(title="SGD and momentum",subtitle="Optimization rules differ in how they use current and past gradients.",panels=[
        dict(title="SGD path",kind="landscape"),
        dict(title="momentum intuition",kind="pipeline",steps=["gradient","velocity","damped history","update"]),
    ]),
    "cs-lr-saddle.svg": dict(title="Learning rate, minima and saddle points",subtitle="Step size changes convergence behavior; nonconvex landscapes also contain flat and saddle regions.",panels=[
        dict(title="learning-rate behavior",kind="bars",labels=["too small","useful","too large"],values=[0.25,0.72,1.0]),
        dict(title="loss landscape",kind="landscape"),
    ]),
    # NN/training tricks
    "cs-activations.svg": dict(title="Activation functions",subtitle="Nonlinear activations prevent deep stacks from collapsing into one linear map.",panels=[
        dict(title="ReLU / sigmoid / tanh",kind="curve",curve="activations"),
        dict(title="practical effects",kind="text",lines=["ReLU: simple, sparse negative side","sigmoid/tanh can saturate","activation changes gradient flow","output activation depends on task"]),
    ]),
    "cs-init-bn.svg": dict(title="Initialization and Batch Normalization",subtitle="Signal scale at initialization and hidden-statistic normalization both affect trainability.",panels=[
        dict(title="initial activation spread",kind="bars",labels=["too small","balanced","too large"],values=[0.2,0.65,1.0]),
        dict(title="BatchNorm train/eval",kind="text",lines=["train: batch mean/variance","eval: running statistics","gamma/beta remain learned","mode mismatch can shift outputs"]),
    ]),
    "cs-reg-dropout.svg": dict(title="Regularization and dropout",subtitle="Regularization constrains the solution; dropout injects stochastic masking during training.",panels=[
        dict(title="weight regularization",kind="curve",curve="regularization"),
        dict(title="dropout network",kind="network",counts=(3,5,2),dropout=True),
    ]),
    "cs-training-diagnostics.svg": dict(title="Training diagnostics",subtitle="Loss curves and confusion patterns tell you what to inspect next.",panels=[
        dict(title="train / validation loss",kind="curve",curve="train_val"),
        dict(title="confusion pattern",kind="matrix",rows=2,cols=2,cell=70,mode="heat",hot=[0,3]),
    ]),
    "cs-augmentation.svg": dict(title="Data augmentation",subtitle="Augmentations should expand nuisance variation without changing the label semantics.",panels=[
        dict(title="original vs transforms",kind="matrix",rows=2,cols=4,cell=48,mode="blue",hot=[1,2,5,6]),
        dict(title="check label invariance",kind="text",lines=["crop: object still present?","flip: task semantics preserved?","color: realistic illumination range?","geometry: does shape remain valid?"]),
    ]),
    # CNN
    "cs-conv-shape.svg": dict(title="Convolution, stride and padding",subtitle="Convolution combines local weighted sums with a spatial sampling rule.",panels=[
        dict(title="numeric convolution",kind="conv"),
        dict(title="shape controls",kind="text",lines=["kernel size controls local window","stride controls sampling interval","padding controls border handling","dilation expands spacing inside kernel"]),
    ]),
    "cs-pooling-hierarchy.svg": dict(title="Pooling and feature hierarchy",subtitle="Spatial summarization and depth transform low-level responses into more task-specific features.",panels=[
        dict(title="pooling response",kind="matrix",rows=4,cols=4,cell=45,mode="blue",hot=[1,6,10,15]),
        dict(title="feature hierarchy",kind="pipeline",steps=["edges","textures","parts","object cues"]),
    ]),
    "cs-fc-conv.svg": dict(title="Fully connected vs convolutional connectivity",subtitle="Fully connected layers connect everything; convolution reuses local weights over space.",panels=[
        dict(title="dense connectivity",kind="fcconv"),
        dict(title="shared local filters",kind="conv"),
    ]),
    # architectures / transfer / tasks
    "cs-architectures-residual.svg": dict(title="Architecture evolution and residual learning",subtitle="The major shift is not just depth, but how information and gradients flow.",panels=[
        dict(title="LeNet → ViT",kind="architecture",names=["LeNet","AlexNet","VGG","ResNet","ViT"]),
        dict(title="residual block",kind="pipeline",steps=["x","F(x)","x + F(x)","output"]),
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
    "cs-iou-nms-instance.svg": dict(title="Boxes, masks, IoU and NMS",subtitle="Detection and segmentation add localization, overlap and duplicate-removal concepts.",panels=[
        dict(title="IoU / overlapping boxes",kind="task",mode="detection"),
        dict(title="semantic vs instance mask",kind="task",mode="instance"),
        dict(title="NMS logic",kind="pipeline",steps=["rank boxes","keep best","suppress overlap","repeat"]),
    ]),
    "cs-visualization.svg": dict(title="Model visualization",subtitle="Attribution tools are diagnostics, not guaranteed causal explanations.",panels=[
        dict(title="saliency / heatmap",kind="heatmap"),
        dict(title="feature maps",kind="matrix",rows=4,cols=5,cell=38,mode="gray",hot=[2,8,13,17]),
    ]),
    "cs-modern.svg": dict(title="Modern CS231n topics",subtitle="Transformers, self-supervised learning, vision-language models and diffusion expand the representation-learning toolbox.",panels=[
        dict(title="representation learning",kind="pipeline",steps=["unlabeled images","augment/views","encoder","representation"]),
        dict(title="CLIP / DINO / diffusion",kind="text",lines=["CLIP: align image and text embeddings","DINO: teacher-student self-distillation","Diffusion: learn denoising transitions","Transformer: global token interactions"]),
    ]),

    # PRML
    "prml-bayes-density.svg": dict(title="Probability density and Bayes theorem",subtitle="PRML starts by representing uncertainty explicitly and updating it with data.",panels=[
        dict(title="probability density",kind="distribution",mode="gaussian"),
        dict(title="Bayes update",kind="pipeline",steps=["prior","likelihood","posterior","decision"]),
    ]),
    "prml-gaussian-beta.svg": dict(title="Gaussian parameters and Beta-Binomial update",subtitle="Parameters control distribution shape, while conjugacy makes some posterior updates analytic.",panels=[
        dict(title="mean / variance",kind="curve",curve="gaussian"),
        dict(title="Beta prior → posterior",kind="distribution",mode="beta"),
    ]),
    "prml-regression-basis.svg": dict(title="Linear regression and basis expansion",subtitle="A model can remain linear in parameters while using nonlinear basis functions of x.",panels=[
        dict(title="regression fit",kind="curve",curve="regression"),
        dict(title="basis functions",kind="bars",labels=["1","x","x²","sin x"],values=[0.45,0.7,0.95,0.62],horizontal=False),
    ]),
    "prml-bias-reg.svg": dict(title="Bias–variance and regularization",subtitle="Model complexity trades approximation error against sensitivity to finite data.",panels=[
        dict(title="bias / variance trade-off",kind="curve",curve="bias_variance"),
        dict(title="regularization effect",kind="curve",curve="regularization"),
    ]),
    "prml-sigmoid-boundary.svg": dict(title="Logistic regression",subtitle="A linear score becomes a probability through the sigmoid, while the decision boundary remains linear.",panels=[
        dict(title="sigmoid",kind="curve",curve="sigmoid"),
        dict(title="binary decision boundary",kind="scatter_linear"),
    ]),
    "prml-multiclass.svg": dict(title="Multi-class classification",subtitle="Multiple class scores define regions in feature space and are normalized into class probabilities.",panels=[
        dict(title="class scores",kind="bars",labels=["C1","C2","C3","C4"],values=[0.9,0.52,0.31,0.18]),
        dict(title="decision regions",kind="scatter_curve"),
    ]),
    "prml-nn-boundary.svg": dict(title="Neural networks as learned nonlinear basis functions",subtitle="Hidden units create a learned representation in which a simple output layer can solve nonlinear problems.",panels=[
        dict(title="hidden network",kind="network",counts=(3,5,2)),
        dict(title="nonlinear boundary",kind="scatter_curve"),
    ]),
    "prml-forward-backprop.svg": dict(title="Forward and backward computation",subtitle="Values move forward; derivatives move backward through the same graph.",panels=[
        dict(title="forward",kind="pipeline",steps=["input","hidden","output","loss"]),
        dict(title="backward",kind="pipeline",steps=["dL/dy","dL/dh","dL/dW","update"]),
    ]),
    "prml-kernel-feature.svg": dict(title="Feature space and the kernel trick",subtitle="A nonlinear problem in input space can correspond to a linear separator in a richer feature space.",panels=[
        dict(title="input space",kind="scatter_curve"),
        dict(title="feature space",kind="scatter_linear"),
    ]),
    "prml-svm.svg": dict(title="SVM margin and support vectors",subtitle="Only samples on or inside the margin determine the optimal separating hyperplane.",panels=[
        dict(title="maximum margin",kind="scatter_linear",margin=True),
        dict(title="hinge-loss view",kind="bars",labels=["far correct","on margin","inside margin","wrong"],values=[0.02,0.2,0.65,1.0]),
    ]),
    "prml-graph-mrf.svg": dict(title="Bayesian networks and Markov random fields",subtitle="Directed and undirected graphs encode different factorization and conditional-independence structures.",panels=[
        dict(title="Bayesian network",kind="graphical",undirected=False),
        dict(title="Markov random field",kind="graphical",undirected=True),
    ]),
    "prml-gmm-em.svg": dict(title="Gaussian mixtures and EM",subtitle="Latent component assignments turn a complex density into a mixture of simpler distributions.",panels=[
        dict(title="mixture density",kind="distribution",mode="mixture"),
        dict(title="EM loop",kind="pipeline",steps=["initialize","E: responsibilities","M: parameters","repeat"]),
    ]),
    "prml-vi-elbo.svg": dict(title="Variational inference and ELBO",subtitle="Choose a tractable q(z) and optimize it toward the intractable posterior.",panels=[
        dict(title="posterior approximation",kind="curve",curve="regularization"),
        dict(title="ELBO decomposition",kind="pipeline",steps=["q(z)","ELBO","KL gap","log p(x)"]),
    ]),
    "prml-monte-mcmc.svg": dict(title="Monte Carlo and MCMC",subtitle="Expectations can be approximated by samples; MCMC constructs dependent samples from a target distribution.",panels=[
        dict(title="Monte Carlo samples",kind="bars",labels=["s1","s2","s3","s4","s5"],values=[0.45,0.72,0.58,0.91,0.67],horizontal=False),
        dict(title="MCMC trajectory",kind="landscape"),
    ]),
    "prml-pca-dim.svg": dict(title="PCA and dimensionality reduction",subtitle="Principal components align the coordinate system with directions of largest data variance.",panels=[
        dict(title="principal axes",kind="pca"),
        dict(title="2D → 1D projection",kind="pipeline",steps=["x ∈ R²","project PC1","z ∈ R¹"]),
    ]),
    "prml-ppca.svg": dict(title="Probabilistic PCA",subtitle="PPCA adds a latent Gaussian variable and observation noise to a linear dimensionality-reduction model.",panels=[
        dict(title="latent generative model",kind="pipeline",steps=["z ~ N(0,I)","Wz + μ","add ε","x"]),
        dict(title="uncertainty around subspace",kind="distribution",mode="gaussian"),
    ]),
    "prml-hmm-filter.svg": dict(title="Hidden Markov models, filtering and decoding",subtitle="Sequential models separate hidden state dynamics from the observation process.",panels=[
        dict(title="state transitions",kind="hmm"),
        dict(title="inference tasks",kind="text",lines=["filtering: current state from past observations","prediction: future state distribution","smoothing: past state using future observations","decoding: most likely state sequence"]),
    ]),
    "prml-ensemble-moe.svg": dict(title="Ensembles and mixture of experts",subtitle="Predictions can be averaged globally or combined by an input-dependent gating function.",panels=[
        dict(title="committee averaging",kind="pipeline",steps=["model A","model B","model C","average"]),
        dict(title="mixture of experts",kind="pipeline",steps=["input","gating","experts","weighted output"]),
    ]),
    "prml-vision-bridge.svg": dict(title="PRML concepts inside modern Vision AI",subtitle="Probability, latent variables and decision theory remain useful even when the function approximator is a deep network.",panels=[
        dict(title="model output",kind="pipeline",steps=["image","network","score/probability","decision"]),
        dict(title="engineering bridge",kind="text",lines=["calibration and threshold selection","uncertainty and distribution shift","PCA/GMM/HMM for monitoring and analysis","Bayesian language clarifies assumptions"]),
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
    ("cs231n","cnn"): ["cs-conv-shape.svg","cs-pooling-hierarchy.svg","cs-fc-conv.svg"],
    ("cs231n","architectures"): ["cs-architectures-residual.svg"],
    ("cs231n","visualization"): ["cs-visualization.svg"],
    ("cs231n","transfer"): ["cs-transfer.svg"],
    ("cs231n","modern"): ["cs-task-suite.svg","cs-iou-nms-instance.svg","cs-modern.svg"],

    ("prml","ch1"): ["prml-bayes-density.svg"],
    ("prml","ch2"): ["prml-gaussian-beta.svg"],
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

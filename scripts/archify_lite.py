#!/usr/bin/env python3
"""archify_lite — 免 Node 的便携架构图渲染器（cht-full-skill 升级组件，MIT）。

把 archify 风格的候选 JSON 渲染成「单个自包含、可交互、双击就能看」的 HTML。
支持 type：architecture / tree / workflow / sequence / dataflow / lifecycle /
erd / class / timeline / waterfall。零依赖，纯标准库，离线可用。

用法：
    python3 archify_lite.py <type> <candidate.json> <output.html>
"""
import sys, json, html, math, datetime, re

PALETTE = ["#5b8def","#e0734d","#3fae8e","#b06fd6","#d9a441","#4fb0c6",
           "#d65f87","#7aa86b","#9b7bd6","#5fc0a8","#c98a5b","#6c8ed6"]

def esc(s):
    return html.escape(str(s), quote=True)

def kind_color(kind, idx):
    if kind and re.match(r"^#", str(kind)):
        return kind
    return PALETTE[idx % len(PALETTE)]

# ---------- 候选抽取 ----------
def extract(type_, c):
    nodes, edges = [], []
    if type_ in ("architecture","tree","workflow","dataflow","class","lifecycle"):
        ns = c.get("nodes") or []
        for n in ns:
            nodes.append({"id": str(n.get("id") or n.get("title")),
                          "kind": n.get("kind") or "node",
                          "title": n.get("title") or n.get("id") or "",
                          "sub": n.get("subtitle") or n.get("sub") or ""})
        for e in (c.get("edges") or []):
            edges.append({"from": str(e.get("from")), "to": str(e.get("to")),
                          "label": e.get("label") or e.get("kind") or ""})
        # tree: 用 parent 字段补边
        for n in ns:
            if n.get("parent"):
                edges.append({"from": str(n["parent"]), "to": str(n.get("id") or n.get("title")),
                              "label": ""})
    elif type_ == "sequence":
        for p in (c.get("participants") or []):
            nodes.append({"id": str(p.get("id") or p.get("name")),
                          "kind": "participant",
                          "title": p.get("name") or p.get("id") or "", "sub": ""})
        for m in (c.get("messages") or []):
            edges.append({"from": str(m.get("from")), "to": str(m.get("to")),
                          "label": m.get("label") or m.get("text") or "",
                          "kind": m.get("kind") or "sync"})
    elif type_ == "erd":
        for e in (c.get("entities") or []):
            nodes.append({"id": str(e.get("name") or e.get("id")),
                          "kind": "entity", "title": e.get("name") or e.get("id") or "",
                          "attrs": e.get("attributes") or []})
        for r in (c.get("relationships") or []):
            edges.append({"from": str(r.get("from")), "to": str(r.get("to")),
                          "label": r.get("label") or r.get("cardinality") or r.get("kind") or ""})
    elif type_ == "timeline":
        for ev in (c.get("events") or []):
            nodes.append({"id": str(ev.get("id") or ev.get("t")),
                          "kind": "event", "title": ev.get("title") or ev.get("label") or "",
                          "t": ev.get("t"), "lane": ev.get("lane") or ev.get("source") or ""})
    elif type_ == "waterfall":
        for t in (c.get("tasks") or []):
            nodes.append({"id": str(t.get("id") or t.get("name")),
                          "kind": "task", "title": t.get("name") or t.get("id") or "",
                          "start": t.get("start"), "end": t.get("end"),
                          "dur": t.get("dur"), "parent": t.get("parent")})
    return nodes, edges

# ---------- 通用图布局（architecture/tree/workflow/dataflow/class/lifecycle） ----------
def layout_graph(nodes, edges):
    by_id = {n["id"]: n for n in nodes}
    adj = {n["id"]: [] for n in nodes}
    indeg = {n["id"]: 0 for n in nodes}
    for e in edges:
        if e["from"] in by_id and e["to"] in by_id and e["from"] != e["to"]:
            adj[e["from"]].append(e["to"]); indeg[e["to"]] += 1
    # 最长路径分层
    layer = {n["id"]: 0 for n in nodes}
    for _ in range(len(nodes)+1):
        changed = False
        for e in edges:
            if e["from"] in by_id and e["to"] in by_id:
                if layer[e["to"]] < layer[e["from"]] + 1:
                    layer[e["to"]] = layer[e["from"]] + 1; changed = True
        if not changed: break
    layers = {}
    for nid, l in layer.items():
        layers.setdefault(l, []).append(nid)
    W, H, DX, DY = 200, 64, 270, 120
    pos = {}
    maxl = max(layers) if layers else 0
    for l, ids in layers.items():
        for i, nid in enumerate(sorted(ids)):
            pos[nid] = {"x": 60 + l*DX, "y": 60 + i*DY, "w": W, "h": H}
    # 画布尺寸
    maxx = max((p["x"] for p in pos.values()), default=0) + W + 60
    maxy = max((p["y"] for p in pos.values()), default=0) + H + 60
    return by_id, pos, edges, maxx, maxy

def svg_graph(nodes, edges):
    by_id, pos, _, maxx, maxy = layout_graph(nodes, edges)
    kind_idx = {}
    s = []
    for e in edges:
        a, b = pos.get(e["from"]), pos.get(e["to"])
        if not a or not b or e["from"] == e["to"]:
            continue
        if b["x"] >= a["x"]:
            sx, sy = a["x"]+a["w"], a["y"]+a["h"]/2
            tx, ty = b["x"], b["y"]+b["h"]/2
        else:
            sx, sy = a["x"], a["y"]+a["h"]/2
            tx, ty = b["x"]+b["w"], b["y"]+b["h"]/2
        mx = (sx+tx)/2
        s.append(f'<path class="edge" d="M{sx},{sy} C{mx},{sy} {mx},{ty} {tx},{ty}" '
                 f'fill="none" marker-end="url(#arrow)"/>')
        if e["label"]:
            s.append(f'<g class="edgelabel"><rect x="{mx-44}" y="{ (sy+ty)/2-11 }" width="88" height="22" rx="4"/>'
                     f'<text x="{mx}" y="{(sy+ty)/2+4}">{esc(e["label"])}</text></g>')
    for n in nodes:
        p = pos.get(n["id"])
        if not p: continue
        ki = kind_idx.setdefault(n["kind"], len(kind_idx))
        col = kind_color(n["kind"], ki)
        s.append(f'<g class="node" data-id="{esc(n["id"])}" '
                 f'onmouseenter="hi(\'{esc(n["id"])}\')" onmouseleave="unhi()">'
                 f'<rect x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" rx="10" '
                 f'fill="{col}"/>'
                 f'<text class="ntitle" x="{p["x"]+p["w"]/2}" y="{p["y"]+p["h"]/2-2}">{esc(n["title"])}</text>')
        if n.get("sub"):
            s.append(f'<text class="nsub" x="{p["x"]+p["w"]/2}" y="{p["y"]+p["h"]/2+15}">{esc(n["sub"])}</text>')
        s.append('</g>')
    return "".join(s), maxx, maxy, kind_idx

# ---------- sequence ----------
def svg_sequence(nodes, edges):
    DX, TOP, LEN = 190, 70, 64
    n = len(nodes)
    maxx = 80 + n*DX + 60
    msgs = sorted(edges, key=lambda e: e.get("label",""))
    maxy = TOP + 60 + (len(edges)+1)*LEN
    s = []
    xs = {}
    for i, p in enumerate(nodes):
        x = 80 + i*DX
        xs[p["id"]] = x
        s.append(f'<g class="node"><rect x="{x-55}" y="{TOP-46}" width="110" height="34" rx="8" fill="#3fae8e"/>'
                 f'<text class="ntitle" x="{x}" y="{TOP-24}">{esc(p["title"])}</text></g>')
        s.append(f'<line class="life" x1="{x}" y1="{TOP-10}" x2="{x}" y2="{maxy-20}" stroke-dasharray="4 4"/>')
    for i, e in enumerate(edges):
        x1, x2 = xs.get(e["from"]), xs.get(e["to"])
        if x1 is None or x2 is None: continue
        y = TOP + 20 + i*LEN
        if e["from"] == e["to"]:
            s.append(f'<path class="edge" d="M{x1},{y} C{x1+60},{y-18} {x1+60},{y+18} {x1},{y+34}" '
                     f'fill="none" marker-end="url(#arrow)"/>')
        else:
            s.append(f'<path class="edge" d="M{x1},{y} L{x2},{y}" fill="none" marker-end="url(#arrow)"/>')
        if e["label"]:
            mx = (x1+x2)/2 if x1!=x2 else x1+70
            s.append(f'<g class="edgelabel"><rect x="{mx-50}" y="{y-11}" width="100" height="22" rx="4"/>'
                     f'<text x="{mx}" y="{y+4}">{esc(e["label"])}</text></g>')
    return "".join(s), maxx, maxy, {}

# ---------- erd ----------
def svg_erd(nodes, edges):
    W, RH, HH, GAP = 210, 22, 30, 46
    cols = max(1, min(len(nodes), 4))
    pos = {}
    by_id = {n["id"]: n for n in nodes}
    for i, n in enumerate(nodes):
        r = i // cols; c = i % cols
        h = HH + RH*(len(n.get("attrs", []))+1)
        pos[n["id"]] = {"x": 40+c*(W+GAP), "y": 40+r*(180+GAP), "w": W, "h": h, "attrs": n.get("attrs", [])}
    maxx = 40 + cols*(W+GAP)
    maxy = 40 + ( (len(nodes)+cols-1)//cols )*(180+GAP)
    s = []
    for e in edges:
        a, b = pos.get(e["from"]), pos.get(e["to"])
        if not a or not b: continue
        s.append(f'<path class="edge" d="M{a["x"]+a["w"]/2},{a["y"]+a["h"]} '
                 f'C{(a["x"]+b["x"])/2},{a["y"]+a["h"]+30} {(a["x"]+b["x"])/2},{b["y"]-30} {b["x"]+b["w"]/2},{b["y"]}" '
                 f'fill="none" marker-end="url(#arrow)"/>')
        if e["label"]:
            mx, my = (a["x"]+b["x"])/2, (a["y"]+b["y"])/2
            s.append(f'<g class="edgelabel"><rect x="{mx-30}" y="{my-11}" width="60" height="22" rx="4"/>'
                     f'<text x="{mx}" y="{my+4}">{esc(e["label"])}</text></g>')
    for n in nodes:
        p = pos[n["id"]]
        s.append(f'<g class="node" data-id="{esc(n["id"])}" onmouseenter="hi(\'{esc(n["id"])}\')" onmouseleave="unhi()">'
                 f'<rect x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" rx="8" fill="#5b8def"/>'
                 f'<text class="ntitle" x="{p["x"]+p["w"]/2}" y="{p["y"]+20}">{esc(n["title"])}</text>')
        yy = p["y"]+HH
        for a in p["attrs"]:
            if isinstance(a, dict):
                nm = a.get("name",""); ty = a.get("type",""); role = a.get("key","")
                label = f'{nm}  {ty}' + (f'  [{role}]' if role else '')
            else:
                label = str(a)
            s.append(f'<line x1="{p["x"]}" y1="{yy}" x2="{p["x"]+p["w"]}" y2="{yy}" stroke="rgba(255,255,255,.25)"/>')
            s.append(f'<text class="nsub" x="{p["x"]+8}" y="{yy+15}" text-anchor="start">{esc(label)}</text>')
            yy += RH
        s.append('</g>')
    return "".join(s), maxx, maxy, {}

# ---------- timeline ----------
def to_epoch(t):
    if t is None: return None
    if isinstance(t,(int,float)): return float(t)
    s = str(t).strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S","%Y-%m-%d %H:%M:%S","%Y-%m-%d","%H:%M:%S"):
        try: return datetime.datetime.strptime(s, fmt).timestamp()
        except: pass
    try:
        return datetime.datetime.fromisoformat(s.replace("Z","+00:00")).timestamp()
    except: return None

def svg_timeline(nodes, edges):
    evs = [n for n in nodes if n.get("t") is not None]
    ts = [to_epoch(n["t"]) for n in evs]
    ts = [t for t in ts if t is not None]
    if not ts: return svg_graph(nodes, edges)
    lo, hi = min(ts), max(ts)
    span = (hi-lo) or 1
    PADL, PADR, W = 80, 80, 980
    maxx = PADL+W+PADR
    lanes = []
    for n in evs:
        l = n.get("lane") or ""
        if l not in lanes: lanes.append(l)
    rowH = 110
    maxy = 70 + len(lanes)*rowH + 40
    s = [f'<line class="axis" x1="{PADL}" y1="50" x2="{PADL+W}" y2="50"/>']
    for i, l in enumerate(lanes):
        y = 70 + i*rowH
        s.append(f'<text class="lane" x="8" y="{y+6}">{esc(l)}</text>')
        s.append(f'<line x1="{PADL}" y1="{y}" x2="{PADL+W}" y2="{y}" stroke="rgba(127,127,127,.15)"/>')
        for n in evs:
            if (n.get("lane") or "") != l: continue
            t = to_epoch(n["t"])
            if t is None: continue
            x = PADL + (t-lo)/span*W
            above = (i % 2 == 0)
            s.append(f'<g class="node" data-id="{esc(n["id"])}" onmouseenter="hi(\'{esc(n["id"])}\')" onmouseleave="unhi()">'
                     f'<circle cx="{x}" cy="{y}" r="7" fill="#e0734d"/>')
            ly = y-18 if above else y+26
            s.append(f'<text class="ntitle" x="{x}" y="{ly}" text-anchor="middle">{esc(n["title"])}</text></g>')
    return "".join(s), maxx, maxy, {}

# ---------- waterfall ----------
def svg_waterfall(nodes, edges):
    tasks = nodes
    starts = [to_epoch(t["start"]) for t in tasks if t.get("start") is not None]
    ends = [to_epoch(t["end"]) for t in tasks if t.get("end") is not None]
    durs = [float(t["dur"]) for t in tasks if isinstance(t.get("dur"),(int,float))]
    al = (min(starts) if starts else 0)
    ah = (max(ends) if ends else (max(durs) if durs else 1))
    if not ends and durs:
        ah = (max(starts) if starts else 0) + max(durs)
    span = (ah-al) or 1
    PADL, W, ROWH = 200, 820, 44
    maxx = PADL+W+40
    maxy = 60 + len(tasks)*ROWH + 40
    s = [f'<line class="axis" x1="{PADL}" y1="40" x2="{PADL+W}" y2="40"/>']
    for i, t in enumerate(tasks):
        y = 60 + i*ROWH
        st = to_epoch(t.get("start")) if t.get("start") is not None else (to_epoch(t.get("end"))-float(t["dur"]) if t.get("end") is not None and isinstance(t.get("dur"),(int,float)) else (al if t.get("dur") is None else al))
        if t.get("start") is not None:
            st = to_epoch(t["start"])
        elif t.get("end") is not None and isinstance(t.get("dur"),(int,float)):
            st = to_epoch(t["end"]) - float(t["dur"])
        elif isinstance(t.get("dur"),(int,float)):
            st = al
        else:
            st = al
        en = to_epoch(t["end"]) if t.get("end") is not None else st + (float(t["dur"]) if isinstance(t.get("dur"),(int,float)) else span)
        x1 = PADL + (st-al)/span*W
        x2 = PADL + (en-al)/span*W
        col = "#4fb0c6" if t.get("parent") else "#5b8def"
        s.append(f'<text class="lane" x="8" y="{y+18}" text-anchor="start">{esc(t["title"])}</text>')
        s.append(f'<rect x="{x1}" y="{y}" width="{max(2,x2-x1)}" height="24" rx="5" fill="{col}" opacity="0.85"/>')
    return "".join(s), maxx, maxy, {}

# ---------- HTML 外壳 ----------
def render(type_, c, title):
    nodes, edges = extract(type_, c)
    if type_ == "sequence": body, mx, my, kinds = svg_sequence(nodes, edges)
    elif type_ == "erd": body, mx, my, kinds = svg_erd(nodes, edges)
    elif type_ == "timeline": body, mx, my, kinds = svg_timeline(nodes, edges)
    elif type_ == "waterfall": body, mx, my, kinds = svg_waterfall(nodes, edges)
    else: body, mx, my, kinds = svg_graph(nodes, edges)

    legend = "".join(
        f'<span class="chip" style="background:{kind_color(k,i)}">{esc(k)}</span>'
        for i, k in enumerate(kinds)) if kinds else ""

    note = c.get("meta",{}).get("note") or c.get("note") or ""
    notes = (f'<div class="note">⚠ {esc(note)}</div>' if note else "")

    return f'''<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>
:root{{--bg:#0f1320;--fg:#e7ecf5;--panel:#1a2030;--edge:#8aa0c0;--grid:rgba(255,255,255,.06)}}
body.light{{--bg:#f6f8fc;--fg:#1b2433;--panel:#ffffff;--edge:#5a6b85;--grid:rgba(0,0,0,.06)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;overflow:hidden}}
header{{display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--panel);border-bottom:1px solid var(--grid)}}
header h1{{font-size:15px;margin:0;flex:1;font-weight:600}}
button{{background:var(--bg);color:var(--fg);border:1px solid var(--edge);border-radius:7px;padding:6px 10px;cursor:pointer;font-size:13px}}
button:hover{{border-color:var(--fg)}}
.legend{{display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.chip{{color:#fff;padding:2px 8px;border-radius:10px;font-size:12px}}
.wrap{{position:absolute;inset:52px 0 0 0;overflow:hidden;cursor:grab}}
.wrap:active{{cursor:grabbing}}
svg{{width:100%;height:100%;display:block}}
.node{{cursor:pointer}}
.node rect{{stroke:rgba(255,255,255,.25);stroke-width:1}}
.node text{{fill:#fff;pointer-events:none}}
.ntitle{{text-anchor:middle;font-weight:600;font-size:13px}}
.nsub{{text-anchor:middle;font-size:11px;fill:rgba(255,255,255,.85)}}
.edge{{stroke:var(--edge);stroke-width:1.6;fill:none}}
.edgelabel rect{{fill:var(--panel);stroke:var(--grid)}}
.edgelabel text{{fill:var(--fg);text-anchor:middle;font-size:11px}}
.axis{{stroke:var(--edge);stroke-width:2}}
.life{{stroke:var(--edge);stroke-width:1.4}}
.lane{{fill:var(--fg);font-size:12px;font-weight:600}}
.note{{position:absolute;left:14px;bottom:12px;background:var(--panel);border:1px solid var(--grid);
  padding:8px 12px;border-radius:8px;max-width:60%}}
.dim{{opacity:.12}}
</style></head>
<body class="dark">
<header>
  <h1>{esc(title)}</h1>
  <div class="legend">{legend}</div>
  <button onclick="toggle()">🌓 主题</button>
  <button onclick="zoom(1.2)">＋</button>
  <button onclick="zoom(0.83)">－</button>
  <button onclick="fit()">⤢ 适配</button>
  <button onclick="png()">⬇ PNG</button>
</header>
<div class="wrap" id="wrap">
<svg id="svg" viewBox="0 0 {mx} {my}" preserveAspectRatio="xMidYMid meet">
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M0,0 L10,5 L0,10 z" fill="var(--edge)"/></marker></defs>
<g id="vp">{body}</g>
</svg>
</div>
{notes}
<script>
let tx=0,ty=0,sc=1; const vp=document.getElementById('vp');
function apply(){{vp.setAttribute('transform',`translate(${{tx}},${{ty}}) scale(${{sc}})`)}}
function zoom(f){{sc=Math.min(4,Math.max(0.2,sc*f));apply()}}
function fit(){{const w=document.getElementById('svg').clientWidth,h=document.getElementById('svg').clientHeight;
  const vb=document.getElementById('svg').viewBox.baseVal; sc=Math.min(w/vb.width,h/vb.height);tx=0;ty=0;apply()}}
function toggle(){{document.body.classList.toggle('light')}}
const wrap=document.getElementById('wrap'); let drag=false,lx=0,ly=0;
wrap.addEventListener('mousedown',e=>{{drag=true;lx=e.clientX;ly=e.clientY}});
window.addEventListener('mouseup',()=>drag=false);
wrap.addEventListener('mousemove',e=>{{if(!drag)return;tx+=e.clientX-lx;ty+=e.clientY-ly;lx=e.clientX;ly=e.clientY;apply()}});
wrap.addEventListener('wheel',e=>{{e.preventDefault();zoom(e.deltaY<0?1.1:0.9)}},{{passive:false}});
function hi(id){{document.querySelectorAll('.node').forEach(n=>{{const on=n.dataset.id===id;
  n.classList.toggle('dim',!on)}});
  document.querySelectorAll('.edge').forEach(()=>{{}});}}
function unhi(){{document.querySelectorAll('.node').forEach(n=>n.classList.remove('dim'))}}
function png(){{const svg=document.getElementById('svg');const xml=new XMLSerializer().serializeToString(svg);
  const img=new Image();const url='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(xml);
  img.onload=()=>{{const cv=document.createElement('canvas');cv.width=svg.viewBox.baseVal.width;cv.height=svg.viewBox.baseVal.height;
    const ctx=cv.getContext('2d');ctx.fillStyle=getComputedStyle(document.body).backgroundColor;ctx.fillRect(0,0,cv.width,cv.height);
    ctx.drawImage(img,0,0);const a=document.createElement('a');a.download='{esc(title)}.png';a.href=cv.toDataURL();a.click()}};
  img.src=url;}}
fit();
</script>
</body></html>'''

def main():
    if len(sys.argv) != 4:
        print("usage: archify_lite.py <type> <candidate.json> <output.html>", file=sys.stderr)
        sys.exit(2)
    type_, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        c = json.load(open(src, encoding="utf-8"))
    except Exception as e:
        print(f"[archify_lite] 无法读取候选 JSON: {e}", file=sys.stderr); sys.exit(1)
    meta = c.get("meta", {}) if isinstance(c, dict) else {}
    title = meta.get("title") or c.get("title") or f"{type_} diagram"
    html_out = render(type_, c, title)
    open(out, "w", encoding="utf-8").write(html_out)
    print(f"[archify_lite] 已生成 {out}（type={type_}, {len(html_out)} bytes）")

if __name__ == "__main__":
    main()

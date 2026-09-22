import os, random

# Regenerate: python3 assets/generate.py
OUT = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "dark": dict(card="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 faint="#21262d", tile="#161b22", grid="#161b22", accent="#2C96C7",
                 green="#3fb950", amber="#d29922", purple="#a371f7", pink="#db61a2"),
    "light": dict(card="#ffffff", border="#d0d7de", fg="#1f2328", muted="#656d76",
                  faint="#eaeef2", tile="#f6f8fa", grid="#f6f8fa", accent="#1F7FAF",
                  green="#1a7f37", amber="#9a6700", purple="#8250df", pink="#bf3989"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
W = 900

BASE_CSS = f"""
      .sans {{ font-family: {SANS}; }}
      .mono {{ font-family: {MONO}; }}
      .rise {{ opacity: 0; animation: rise .8s ease-out forwards; }}
      .d1 {{ animation-delay: .15s; }} .d2 {{ animation-delay: .3s; }}
      .d3 {{ animation-delay: .45s; }} .d4 {{ animation-delay: .6s; }}
      .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2s ease-out infinite; }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes ping {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
      @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; }} }}"""


def card(h, t, rx=14):
    return f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="{rx}" fill="{t["card"]}" stroke="{t["border"]}"/>'


def pill(x, y, w, label, t, color):
    return f'''<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="none" stroke="{t['border']}"/>
    <circle class="ping" cx="{x+18}" cy="{y+14}" r="4" fill="{color}"/>
    <circle cx="{x+18}" cy="{y+14}" r="4" fill="{color}"/>
    <text x="{x+30}" y="{y+18.5}" class="mono" font-size="12" fill="{t['muted']}">{label}</text>'''


# ── banner ────────────────────────────────────────────────────────────────────
def heartbeat(y0, period=300):
    """One repeating ECG period, tiled so the path can scroll seamlessly."""
    rnd = random.Random(7)
    noise = [rnd.uniform(-2.2, 2.2) for _ in range(period // 12)]
    pts = []
    for k in range((W + period * 2) // period):
        base = k * period
        for i, n in enumerate(noise):
            x = base + i * 12
            if i == 12:
                pts += [(x, y0), (x + 8, y0 - 6), (x + 14, y0 + 10), (x + 22, y0 - 30),
                        (x + 30, y0 + 14), (x + 38, y0 - 4), (x + 46, y0)]
            elif 12 < i < 17:
                continue
            else:
                pts.append((x, y0 + (0 if i == 0 else n)))
    pts.append(((k + 1) * period, y0))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def banner(t):
    H, P = 240, 300
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Vishesh Gupta, Staff Software Engineer at Alpaca">
  <defs>
    <linearGradient id="trace" x1="0" x2="{W}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset=".3" stop-color="{t['accent']}"/>
      <stop offset=".8" stop-color="{t['green']}"/>
      <stop offset="1" stop-color="{t['green']}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}"/>
    </pattern>
    <clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath>
    <mask id="beat" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <g class="scroll"><path d="{heartbeat(214, P)}" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></g>
    </mask>
    <style>{BASE_CSS}
      .scroll {{ animation: scroll 2.6s linear infinite; }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes scroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{P}px); }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
  </defs>
  {card(H, t)}
  <g clip-path="url(#clip)">
    <rect width="{W}" height="{H}" fill="url(#grid)"/>
    <rect width="{W}" height="{H}" fill="url(#trace)" mask="url(#beat)"/>
  </g>
  <text x="48" y="58" class="mono rise" font-size="14" fill="{t['muted']}">~ $ whoami<tspan class="cursor" fill="{t['accent']}"> ▍</tspan></text>
  <text x="46" y="112" class="sans rise d1" font-size="46" font-weight="700" fill="{t['fg']}" letter-spacing="-1">Vishesh Gupta</text>
  <text x="48" y="146" class="sans rise d2" font-size="18" fill="{t['accent']}" font-weight="600">Staff Software Engineer at Alpaca</text>
  <text x="48" y="172" class="mono rise d3" font-size="13" fill="{t['muted']}">cloud architecture · devops · site reliability</text>
  <g class="rise d3">{pill(788, 30, 80, "online", t, t['green'])}</g>
</svg>
'''


# ── status page (technical) ───────────────────────────────────────────────────
ROWS = [
    ("Cloud Architecture", "AWS · Google Cloud · designing for failure", "99.99%", 0),
    ("DevOps &amp; SRE", "on-call, calm, caffeinated", "99.98%", 1),
    ("Kubernetes &amp; Containers", "Kubernetes · Docker · Linux", "99.97%", 2),
    ("Infrastructure as Code", "Terraform · GitHub Actions", "100%", 3),
    ("Observability", "Prometheus · Grafana · SLOs over vibes", "99.99%", 4),
]


def status(t):
    top, rowh = 96, 54
    H = top + rowh * len(ROWS) + 22
    bars_x, n, bw, gap = 360, 48, 5, 3
    out = []
    for i, (label, sub, metric, seed) in enumerate(ROWS):
        y = top + i * rowh
        rnd = random.Random(seed * 31 + 3)
        out.append(f'<text x="40" y="{y+18}" class="sans" font-size="15" font-weight="600" fill="{t["fg"]}">{label}</text>')
        out.append(f'<text x="40" y="{y+37}" class="sans" font-size="12.5" fill="{t["muted"]}">{sub}</text>')
        for b in range(n):
            c = t["amber"] if rnd.random() < .025 else t["green"]
            out.append(f'<rect class="bar" style="animation-delay:{b*.012 + i*.05:.3f}s" x="{bars_x + b*(bw+gap)}" y="{y+6}" width="{bw}" height="28" rx="1.5" fill="{c}"/>')
        out.append(f'<text x="{W-40}" y="{y+25}" text-anchor="end" class="mono" font-size="13" fill="{t["green"]}">{metric}</text>')
        if i < len(ROWS) - 1:
            out.append(f'<line x1="40" x2="{W-40}" y1="{y+rowh-4}" y2="{y+rowh-4}" stroke="{t["faint"]}"/>')
    rows = "\n  ".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Status page: Cloud Architecture, DevOps and SRE, Kubernetes and Containers, Infrastructure as Code, Observability, all operational">
  <defs>
    <style>{BASE_CSS}
      .bar {{ opacity: 0; animation: in .35s ease-out forwards; }}
      @keyframes in {{ to {{ opacity: .9; }} }}
    </style>
  </defs>
  {card(H, t)}
  <circle class="ping" cx="48" cy="46" r="5" fill="{t['green']}"/>
  <circle cx="48" cy="46" r="5" fill="{t['green']}"/>
  <text x="64" y="51" class="sans" font-size="17" font-weight="600" fill="{t['fg']}">All systems operational</text>
  <text x="{W-40}" y="51" text-anchor="end" class="mono" font-size="12.5" fill="{t['muted']}">vish.status · last 48 weeks</text>
  <line x1="1" x2="{W-1}" y1="76" y2="76" stroke="{t['border']}"/>
  {rows}
</svg>
'''


# ── off-call (non-technical) ──────────────────────────────────────────────────
def icon(kind, cx, cy, c):
    s = f'fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "globe":
        return f'''<g {s}><circle cx="{cx}" cy="{cy}" r="11"/><ellipse cx="{cx}" cy="{cy}" rx="4.5" ry="11"/>
      <path d="M{cx-11} {cy}h22M{cx-9.5} {cy-5.5}h19M{cx-9.5} {cy+5.5}h19"/></g>'''
    if kind == "play":
        return f'''<g {s}><rect x="{cx-12}" y="{cy-9}" width="24" height="17" rx="3"/>
      <path d="M{cx-3} {cy-4}v8l6.5-4z" fill="{c}"/><path d="M{cx-5} {cy+12}h10"/></g>'''
    if kind == "cloche":
        return f'''<g {s}><path d="M{cx-12} {cy+6}h24M{cx-10} {cy+6}a10 10 0 0 1 20 0"/>
      <circle cx="{cx}" cy="{cy-6}" r="1.6" fill="{c}"/><path d="M{cx-9} {cy+10}h18"/></g>'''
    if kind == "hanger":
        return f'''<g {s}><path d="M{cx-3} {cy-8}a3 3 0 1 1 3 3v2.5"/>
      <path d="M{cx} {cy-2.5}l-12 8.5a1.5 1.5 0 0 0 1 2.7h22a1.5 1.5 0 0 0 1-2.7z"/></g>'''


TILES = [
    ("globe", "accent", "10", "countries explored", "passport: mostly stamps"),
    ("play", "purple", "9000+", "anime episodes", "next episode loading…"),
    ("cloche", "amber", "#43", "world-ranked dining", "tasting menus, taken seriously"),
    ("hanger", "pink", "∞", "fashion &amp; style", "always dressed for prod"),
]


def offcall(t):
    H = 330
    p0, p1, p2, p3 = (300, 112), (440, 58), (700, 58), (840, 112)
    arc = f"M{p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
    stamps = []
    for i in range(10):
        u = (i + .5) / 10
        x, y = ((1-u)**3*a + 3*(1-u)**2*u*b + 3*(1-u)*u**2*c + u**3*d
                for a, b, c, d in zip(p0, p1, p2, p3))
        stamps.append(f'<circle class="stamp" style="animation-delay:{9*u:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{t["card"]}" stroke="{t["accent"]}" stroke-width="1.5"/>')

    tw, th, tg, ty = 197, 150, 14, 146
    tiles = []
    for i, (ic, col, big, label, sub) in enumerate(TILES):
        x = 40 + i * (tw + tg)
        c = t[col]
        extra = ""
        if ic == "play":
            extra = f'''<rect x="{x+20}" y="{ty+132}" width="{tw-40}" height="3" rx="1.5" fill="{t['faint']}"/>
      <rect class="progress" x="{x+20}" y="{ty+132}" width="{tw-40}" height="3" rx="1.5" fill="{c}"/>'''
        tiles.append(f'''<g class="rise d{i+1}">
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{t['tile']}" stroke="{t['faint']}"/>
      {icon(ic, x + 34, ty + 34, c)}
      <text x="{x+20}" y="{ty+88}" class="sans" font-size="30" font-weight="700" fill="{t['fg']}" letter-spacing="-.5">{big}</text>
      <text x="{x+20}" y="{ty+108}" class="sans" font-size="13" font-weight="600" fill="{c}">{label}</text>
      <text x="{x+20}" y="{ty+125}" class="sans" font-size="11.5" fill="{t['muted']}">{sub}</text>
      {extra}
    </g>''')

    plane = f'<path d="M-9 0 L9 0 M2 -7 L6 0 L2 7 M-7 -3 L-5 0 L-7 3" fill="none" stroke="{t["fg"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Off-call: 10 countries explored, 9000+ anime episodes watched, world #43 fine dining, fashion and style. Sleep: degraded, won't fix.">
  <defs>
    <style>{BASE_CSS}
      .stamp {{ animation: stamp 9s ease-out infinite; }}
      .progress {{ transform-box: fill-box; transform-origin: left; animation: load 4s ease-in-out infinite; }}
      @keyframes stamp {{ 0%, 4% {{ fill: {t['card']}; }} 8%, 100% {{ fill: {t['accent']}; }} }}
      @keyframes load {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    </style>
  </defs>
  {card(H, t)}
  <text x="40" y="44" class="mono" font-size="12.5" fill="{t['muted']}">$ systemctl status life --off-call</text>
  <text x="40" y="70" class="sans" font-size="19" font-weight="600" fill="{t['fg']}">Life outside the terminal</text>
  {pill(W-160, 28, 120, "exploring", t, t['accent'])}
  <path d="{arc}" fill="none" stroke="{t['border']}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>
  {''.join(stamps)}
  <g>{plane}<animateMotion dur="9s" repeatCount="indefinite" rotate="auto" path="{arc}"/></g>
  {''.join(tiles)}
  <circle cx="44" cy="{H-22}" r="3.5" fill="{t['amber']}"/>
  <text x="56" y="{H-18}" class="mono" font-size="12" fill="{t['muted']}">sleep.service: <tspan fill="{t['amber']}">degraded</tspan> · known issue, won't fix</text>
</svg>
'''


for name, t in THEMES.items():
    for kind, fn in (("banner", banner), ("status", status), ("offcall", offcall)):
        with open(f"{OUT}/{kind}-{name}.svg", "w") as f:
            f.write(fn(t))
print("ok")

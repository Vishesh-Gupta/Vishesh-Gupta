import os, random

# Regenerate: python3 assets/generate.py
OUT = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    "dark": dict(bg="#0d1117", card="#0d1117", border="#30363d", fg="#e6edf3",
                 muted="#8b949e", faint="#21262d", accent="#2C96C7", green="#3fb950",
                 amber="#d29922", grid="#161b22"),
    "light": dict(bg="#ffffff", card="#ffffff", border="#d0d7de", fg="#1f2328",
                  muted="#656d76", faint="#eaeef2", accent="#1F7FAF", green="#1a7f37",
                  amber="#9a6700", grid="#f6f8fa"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def banner(t):
    W, H = 900, 240
    # heartbeat / latency trace across the bottom of the card
    y0 = 212
    pts, x = [], 0
    rnd = random.Random(7)
    while x <= W:
        if x in (480, 720):
            pts += [(x, y0), (x + 8, y0 - 6), (x + 14, y0 + 10), (x + 22, y0 - 38),
                    (x + 30, y0 + 18), (x + 38, y0 - 4), (x + 46, y0)]
            x += 46
        else:
            pts.append((x, y0 + rnd.uniform(-2.5, 2.5)))
            x += 12
    path = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Vishesh Gupta, Staff Software Engineer at Alpaca">
  <defs>
    <linearGradient id="trace" x1="0" x2="1">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset=".25" stop-color="{t['accent']}"/>
      <stop offset=".75" stop-color="{t['green']}"/>
      <stop offset="1" stop-color="{t['green']}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width="1"/>
    </pattern>
    <clipPath id="card"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath>
    <style>
      .sans {{ font-family: {SANS}; }}
      .mono {{ font-family: {MONO}; }}
      .trace {{ stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 3.2s ease-out forwards; }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      .pulse {{ transform-origin: 806px 44px; animation: pulse 2s ease-out infinite; }}
      .rise {{ opacity: 0; animation: rise .8s ease-out forwards; }}
      .d1 {{ animation-delay: .15s; }} .d2 {{ animation-delay: .35s; }} .d3 {{ animation-delay: .55s; }}
      @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes pulse {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#grid)" opacity=".9"/>
    <path class="trace" d="{path}" fill="none" stroke="url(#trace)" stroke-width="2" stroke-linejoin="round"/>
  </g>

  <text x="48" y="58" class="mono rise" font-size="14" fill="{t['muted']}">~ $ whoami<tspan class="cursor" fill="{t['accent']}"> ▍</tspan></text>
  <text x="46" y="112" class="sans rise d1" font-size="46" font-weight="700" fill="{t['fg']}" letter-spacing="-1">Vishesh Gupta</text>
  <text x="48" y="146" class="sans rise d2" font-size="18" fill="{t['accent']}" font-weight="600">Staff Software Engineer at Alpaca</text>
  <text x="48" y="172" class="mono rise d3" font-size="13" fill="{t['muted']}">cloud architecture · devops · site reliability</text>

  <g class="rise d3">
    <rect x="788" y="30" width="80" height="28" rx="14" fill="none" stroke="{t['border']}"/>
    <circle class="pulse" cx="806" cy="44" r="4" fill="{t['green']}"/>
    <circle cx="806" cy="44" r="4" fill="{t['green']}"/>
    <text x="818" y="48.5" class="mono" font-size="12" fill="{t['muted']}">online</text>
  </g>
</svg>
'''


ROWS = [
    ("Cloud Architecture", "designing for failure", "99.99%", "ok", 0),
    ("DevOps &amp; SRE", "on-call, calm, caffeinated", "99.98%", "ok", 1),
    ("Travel", "10 countries explored", "10", "ok", 2),
    ("Anime", "9000+ episodes watched", "9000+", "ok", 3),
    ("Fine Dining", "World #43 visited", "#43", "ok", 4),
    ("Fashion &amp; Style", "always in production", "100%", "ok", 5),
    ("Sleep", "known issue, won't fix", "degraded", "warn", 6),
]


def status(t):
    W = 900
    top, rowh = 96, 54
    H = top + rowh * len(ROWS) + 22
    bars_x, n, bw, gap = 330, 52, 5, 3
    out = []
    for i, (label, sub, metric, state, seed) in enumerate(ROWS):
        y = top + i * rowh
        rnd = random.Random(seed * 31 + 3)
        col = t["green"] if state == "ok" else t["amber"]
        out.append(f'<text x="40" y="{y+18}" class="sans" font-size="15" font-weight="600" fill="{t["fg"]}">{label}</text>')
        out.append(f'<text x="40" y="{y+37}" class="sans" font-size="12.5" fill="{t["muted"]}">{sub}</text>')
        for b in range(n):
            if state == "warn":
                c = t["amber"] if rnd.random() < .55 else t["green"]
            else:
                c = t["amber"] if rnd.random() < .025 else t["green"]
            delay = (b * 0.012 + i * 0.05)
            out.append(f'<rect class="bar" style="animation-delay:{delay:.3f}s" x="{bars_x + b*(bw+gap)}" y="{y+6}" width="{bw}" height="28" rx="1.5" fill="{c}"/>')
        out.append(f'<text x="{W-40}" y="{y+25}" text-anchor="end" class="mono" font-size="13" fill="{col}">{metric}</text>')
        if i < len(ROWS) - 1:
            out.append(f'<line x1="40" x2="{W-40}" y1="{y+rowh-4}" y2="{y+rowh-4}" stroke="{t["faint"]}"/>')
    rows = "\n  ".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Status page: Cloud Architecture, DevOps and SRE, Travel (10 countries), Anime (9000+ episodes), Fine Dining (World #43), Fashion and Style all operational; Sleep degraded">
  <defs>
    <style>
      .sans {{ font-family: {SANS}; }}
      .mono {{ font-family: {MONO}; }}
      .bar {{ opacity: 0; animation: in .35s ease-out forwards; }}
      .pulse {{ transform-origin: 48px 46px; animation: pulse 2s ease-out infinite; }}
      @keyframes in {{ from {{ opacity: 0; }} to {{ opacity: .9; }} }}
      @keyframes pulse {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3); opacity: 0; }} }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
  <circle class="pulse" cx="48" cy="46" r="5" fill="{t['green']}"/>
  <circle cx="48" cy="46" r="5" fill="{t['green']}"/>
  <text x="64" y="51" class="sans" font-size="17" font-weight="600" fill="{t['fg']}">All critical systems operational</text>
  <text x="{W-40}" y="51" text-anchor="end" class="mono" font-size="12.5" fill="{t['muted']}">vish.status · last 52 weeks</text>
  <line x1="1" x2="{W-1}" y1="76" y2="76" stroke="{t['border']}"/>
  {rows}
</svg>
'''


for name, t in THEMES.items():
    open(f"{OUT}/banner-{name}.svg", "w").write(banner(t))
    open(f"{OUT}/status-{name}.svg", "w").write(status(t))
print("ok")

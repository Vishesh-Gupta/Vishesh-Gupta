"""Builds the single animated profile card: assets/profile-{dark,light}.svg

Regenerate: python3 assets/generate.py
Icons in assets/icons/ come from skillicons.dev (MIT).
"""
import os, random, re

OUT = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(OUT, "icons")

THEMES = {
    "dark": dict(card="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 faint="#21262d", tile="#161b22", grid="#161b22", accent="#2C96C7",
                 green="#3fb950", amber="#d29922", purple="#a371f7", pink="#db61a2"),
    "light": dict(card="#ffffff", border="#d0d7de", fg="#1f2328", muted="#656d76",
                  faint="#eaeef2", tile="#f6f8fa", grid="#f0f3f6", accent="#1F7FAF",
                  green="#1a7f37", amber="#9a6700", purple="#8250df", pink="#bf3989"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
W = 900

# ── content ───────────────────────────────────────────────────────────────────
NAME = "Vishesh Gupta"
ROLE = "Staff Software Engineer at Alpaca"
TAGLINE = "cloud architecture · devops · site reliability"

CONNECT = [
    ("linkedin", "in/vishesh-gupta"),
    ("github", "@vishesh-monoceros"),
    ("email", "vishesh.gupta12@outlook.com"),
]

ROWS = [
    ("Cloud Architecture", "AWS · Google Cloud · designing for failure", "99.99%", 0),
    ("DevOps &amp; SRE", "on-call, calm, caffeinated", "99.98%", 1),
    ("Kubernetes &amp; Containers", "Kubernetes · Docker · Linux", "99.97%", 2),
    ("Infrastructure as Code", "Terraform · GitHub Actions", "100%", 3),
    ("Observability", "Prometheus · Grafana · SLOs over vibes", "99.99%", 4),
]

TOOLBOX = [
    ("cloud", ["aws", "gcp"]),
    ("platform", ["kubernetes", "docker", "terraform", "linux"]),
    ("code", ["python", "go", "bash"]),
    ("ops", ["prometheus", "grafana", "githubactions"]),
]

TILES = [
    ("globe", "accent", "10", "countries explored", "passport: mostly stamps"),
    ("play", "purple", "9000+", "anime episodes", "next episode loading…"),
    ("cloche", "amber", "#43", "world-ranked dining", "tasting menus, taken seriously"),
    ("hanger", "pink", "∞", "fashion &amp; style", "always dressed for prod"),
]

# ── helpers ───────────────────────────────────────────────────────────────────
EMAIL_ICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="none">'
              '<rect width="256" height="256" rx="60" fill="#0078D4"/>'
              '<rect x="48" y="72" width="160" height="112" rx="16" stroke="#fff" stroke-width="16"/>'
              '<path d="M56 84l72 56 72-56" stroke="#fff" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/></svg>')

_uid = 0


def logo(name, theme, x, y, size, cls="", style=""):
    """Inline a 256x256 icon as a nested <svg>, prefixing ids so gradients don't collide."""
    global _uid
    _uid += 1
    src = EMAIL_ICON if name == "email" else open(os.path.join(ICONS, f"{name}-{theme}.svg")).read()
    p = f"i{_uid}_"
    src = re.sub(r'id="([^"]+)"', rf'id="{p}\1"', src)
    src = re.sub(r'url\(#([^)]+)\)', rf'url(#{p}\1)', src)
    src = re.sub(r'href="#([^"]+)"', rf'href="#{p}\1"', src)
    src = re.sub(r'<svg\b[^>]*>', f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 256 256" fill="none">', src, count=1)
    return f'<g class="{cls}" style="{style}">{src}</g>'


def ping_dot(cx, cy, r, color):
    return (f'<circle class="ping" cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


def pill(x, y, w, label, t, color):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="none" stroke="{t["border"]}"/>'
            + ping_dot(x + 18, y + 14, 4, color)
            + f'<text x="{x+30}" y="{y+18.5}" class="mono" font-size="12" fill="{t["muted"]}">{label}</text>')


def heartbeat(y0, period=300):
    """One ECG period tiled so the path scrolls seamlessly by exactly one period."""
    rnd = random.Random(7)
    noise = [rnd.uniform(-2.2, 2.2) for _ in range(period // 12)]
    pts = []
    periods = (W + period * 2) // period
    for k in range(periods):
        base = k * period
        for i, n in enumerate(noise):
            x = base + i * 12
            if i == 12:
                pts += [(x, y0), (x + 8, y0 - 6), (x + 14, y0 + 10), (x + 22, y0 - 30),
                        (x + 30, y0 + 14), (x + 38, y0 - 4), (x + 46, y0)]
            elif not 12 < i < 17:
                pts.append((x, y0 + (0 if i == 0 else n)))
    pts.append((periods * period, y0))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def divider(y, t):
    return f'<line x1="40" x2="{W-40}" y1="{y}" y2="{y}" stroke="{t["faint"]}"/>'


def icon(kind, cx, cy, c):
    s = f'fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    return {
        "globe": f'<g {s}><circle cx="{cx}" cy="{cy}" r="11"/><ellipse cx="{cx}" cy="{cy}" rx="4.5" ry="11"/>'
                 f'<path d="M{cx-11} {cy}h22M{cx-9.5} {cy-5.5}h19M{cx-9.5} {cy+5.5}h19"/></g>',
        "play": f'<g {s}><rect x="{cx-12}" y="{cy-9}" width="24" height="17" rx="3"/>'
                f'<path d="M{cx-3} {cy-4}v8l6.5-4z" fill="{c}"/><path d="M{cx-5} {cy+12}h10"/></g>',
        "cloche": f'<g {s}><path d="M{cx-12} {cy+6}h24M{cx-10} {cy+6}a10 10 0 0 1 20 0"/>'
                  f'<circle cx="{cx}" cy="{cy-6}" r="1.6" fill="{c}"/><path d="M{cx-9} {cy+10}h18"/></g>',
        "hanger": f'<g {s}><path d="M{cx-3} {cy-8}a3 3 0 1 1 3 3v2.5"/>'
                  f'<path d="M{cx} {cy-2.5}l-12 8.5a1.5 1.5 0 0 0 1 2.7h22a1.5 1.5 0 0 0 1-2.7z"/></g>',
    }[kind]


# ── sections (each drawn in its own local coordinates) ───────────────────────
def header(t, theme):
    out = [
        f'<text x="48" y="58" class="mono rise" font-size="14" fill="{t["muted"]}">~ $ whoami<tspan class="cursor" fill="{t["accent"]}"> ▍</tspan></text>',
        f'<text x="46" y="112" class="sans rise d1" font-size="46" font-weight="700" fill="{t["fg"]}" letter-spacing="-1">{NAME}</text>',
        f'<text x="48" y="146" class="sans rise d2" font-size="18" fill="{t["accent"]}" font-weight="600">{ROLE}</text>',
        f'<text x="48" y="172" class="mono rise d3" font-size="13" fill="{t["muted"]}">{TAGLINE}</text>',
        f'<g class="rise d3">{pill(780, 30, 80, "online", t, t["green"])}</g>',
    ]
    x = 48
    for i, (name, handle) in enumerate(CONNECT):
        out.append(logo(name, theme, x, 196, 26, "rise", f"animation-delay:{.6 + i*.1:.2f}s"))
        out.append(f'<text x="{x+36}" y="214" class="mono rise" style="animation-delay:{.6 + i*.1:.2f}s" font-size="12.5" fill="{t["muted"]}">{handle}</text>')
        x += 36 + len(handle) * 7.6 + 30
    # heartbeat doubles as the divider between the header and the rest
    out.append(f'<rect x="1" y="238" width="{W-2}" height="64" fill="url(#trace)" mask="url(#beat)"/>')
    return "\n  ".join(out), 302


def status(t):
    top, rowh = 64, 54
    bars_x, n, bw, gap = 360, 48, 5, 3
    out = [
        ping_dot(48, 30, 5, t["green"]),
        f'<text x="64" y="35" class="sans" font-size="17" font-weight="600" fill="{t["fg"]}">All systems operational</text>',
        f'<text x="{W-40}" y="35" text-anchor="end" class="mono" font-size="12.5" fill="{t["muted"]}">vish.status · last 48 weeks</text>',
    ]
    for i, (label, sub, metric, seed) in enumerate(ROWS):
        y = top + i * rowh
        rnd = random.Random(seed * 31 + 3)
        out.append(f'<text x="40" y="{y+18}" class="sans" font-size="15" font-weight="600" fill="{t["fg"]}">{label}</text>')
        out.append(f'<text x="40" y="{y+37}" class="sans" font-size="12.5" fill="{t["muted"]}">{sub}</text>')
        for b in range(n):
            c = t["amber"] if rnd.random() < .025 else t["green"]
            out.append(f'<rect class="bar" style="animation-delay:{.8 + b*.012 + i*.05:.3f}s" x="{bars_x + b*(bw+gap)}" y="{y+6}" width="{bw}" height="28" rx="1.5" fill="{c}"/>')
        out.append(f'<text x="{W-40}" y="{y+25}" text-anchor="end" class="mono" font-size="13" fill="{t["green"]}">{metric}</text>')
        if i < len(ROWS) - 1:
            out.append(f'<line x1="40" x2="{W-40}" y1="{y+rowh-4}" y2="{y+rowh-4}" stroke="{t["faint"]}" stroke-dasharray="2 4"/>')
    return "\n  ".join(out), top + rowh * len(ROWS)


def toolbox(t, theme):
    size, gap = 48, 10
    icons = sum(len(g) * size + (len(g) - 1) * gap for _, g in TOOLBOX)
    group_gap = (W - 80 - icons) / (len(TOOLBOX) - 1)  # spread groups across the 40px margins
    x = 40
    out = [f'<text x="40" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ ls ~/toolbox</text>']
    k = 0
    for gi, (label, names) in enumerate(TOOLBOX):
        out.append(f'<text x="{x:.0f}" y="62" class="mono" font-size="11" fill="{t["muted"]}" letter-spacing=".5">{label}</text>')
        for name in names:
            out.append(logo(name, theme, round(x), 72, size, "pop", f"animation-delay:{1.2 + k*.06:.2f}s"))
            x += size + gap
            k += 1
        x += group_gap - gap
        if gi < len(TOOLBOX) - 1:
            sx = x - group_gap / 2
            out.append(f'<line x1="{sx:.0f}" x2="{sx:.0f}" y1="76" y2="116" stroke="{t["faint"]}"/>')
    return "\n  ".join(out), 140


def offcall(t):
    p0, p1, p2, p3 = (300, 94), (440, 40), (700, 40), (840, 94)
    arc = f"M{p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
    out = [
        f'<text x="40" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ systemctl status life --off-call</text>',
        f'<text x="40" y="54" class="sans" font-size="17" font-weight="600" fill="{t["fg"]}">Life outside the terminal</text>',
        f'<path d="{arc}" fill="none" stroke="{t["border"]}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>',
    ]
    for i in range(10):
        u = (i + .5) / 10
        x, y = ((1-u)**3*a + 3*(1-u)**2*u*b + 3*(1-u)*u**2*c + u**3*d for a, b, c, d in zip(p0, p1, p2, p3))
        out.append(f'<circle class="stamp" style="animation-delay:{9*u:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{t["card"]}" stroke="{t["accent"]}" stroke-width="1.5"/>')
    out.append(f'<g><path d="M-9 0 L9 0 M2 -7 L6 0 L2 7 M-7 -3 L-5 0 L-7 3" fill="none" stroke="{t["fg"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<animateMotion dur="9s" repeatCount="indefinite" rotate="auto" path="{arc}"/></g>')

    tg, th, ty = 14, 150, 124
    tw = (W - 80 - tg * (len(TILES) - 1)) / len(TILES)
    for i, (ic, col, big, label, sub) in enumerate(TILES):
        x, c = 40 + i * (tw + tg), t[col]
        extra = ""
        if ic == "play":
            extra = (f'<rect x="{x+20}" y="{ty+132}" width="{tw-40}" height="3" rx="1.5" fill="{t["faint"]}"/>'
                     f'<rect class="progress" x="{x+20}" y="{ty+132}" width="{tw-40}" height="3" rx="1.5" fill="{c}"/>')
        out.append(f'''<g class="rise" style="animation-delay:{1.8 + i*.12:.2f}s">
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{t['tile']}" stroke="{t['faint']}"/>
      {icon(ic, x + 34, ty + 34, c)}
      <text x="{x+20}" y="{ty+88}" class="sans" font-size="30" font-weight="700" fill="{t['fg']}" letter-spacing="-.5">{big}</text>
      <text x="{x+20}" y="{ty+108}" class="sans" font-size="13" font-weight="600" fill="{c}">{label}</text>
      <text x="{x+20}" y="{ty+125}" class="sans" font-size="11.5" fill="{t['muted']}">{sub}</text>
      {extra}
    </g>''')
    return "\n  ".join(out), ty + th


def footer(t):
    out = [
        f'<circle cx="44" cy="22" r="3.5" fill="{t["amber"]}"/>',
        f'<text x="56" y="26" class="mono" font-size="12" fill="{t["muted"]}">sleep.service: <tspan fill="{t["amber"]}">degraded</tspan> · known issue, won\'t fix</text>',
        f'<text x="{W-40}" y="26" text-anchor="end" class="mono" font-size="12" fill="{t["muted"]}">thanks for stopping by · <tspan fill="{t["green"]}">exit 0</tspan></text>',
    ]
    return "\n  ".join(out), 48


# ── assembly ──────────────────────────────────────────────────────────────────
def profile(theme):
    t = THEMES[theme]
    P = 300
    parts, y = [], 0
    for fn, gap_after, rule in ((lambda: header(t, theme), 10, False),
                                (lambda: status(t), 28, True),
                                (lambda: toolbox(t, theme), 20, True),
                                (lambda: offcall(t), 22, True),
                                (lambda: footer(t), 0, False)):
        body, h = fn()
        parts.append(f'<g transform="translate(0 {y})">\n  {body}\n  </g>')
        y += h + gap_after
        if rule:
            parts.append(divider(y - gap_after / 2, t))
    H = y
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}, {ROLE}. Status: cloud architecture, DevOps and SRE, Kubernetes, infrastructure as code and observability all operational. Toolbox: AWS, Google Cloud, Kubernetes, Docker, Terraform, Linux, Python, Go, Bash, Prometheus, Grafana, GitHub Actions. Off-call: 10 countries, 9000+ anime episodes, world #43 dining, fashion and style.">
  <defs>
    <linearGradient id="trace" x1="0" x2="{W}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset=".3" stop-color="{t['accent']}"/>
      <stop offset=".8" stop-color="{t['green']}"/>
      <stop offset="1" stop-color="{t['green']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="gridfade"><rect width="{W}" height="320" fill="url(#fade)"/></mask>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}"/>
    </pattern>
    <mask id="beat" maskUnits="userSpaceOnUse" x="0" y="238" width="{W}" height="64">
      <g class="scroll"><path d="{heartbeat(272, P)}" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></g>
    </mask>
    <clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16"/></clipPath>
    <style>
      .sans {{ font-family: {SANS}; }}
      .mono {{ font-family: {MONO}; }}
      .rise {{ opacity: 0; animation: rise .8s ease-out forwards; }}
      .d1 {{ animation-delay: .15s; }} .d2 {{ animation-delay: .3s; }} .d3 {{ animation-delay: .45s; }}
      .pop {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: pop .5s cubic-bezier(.3,1.4,.6,1) forwards; }}
      .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2s ease-out infinite; }}
      .bar {{ opacity: 0; animation: in .35s ease-out forwards; }}
      .scroll {{ animation: scroll 2.6s linear infinite; }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      .stamp {{ animation: stamp 9s ease-out infinite; }}
      .progress {{ transform-box: fill-box; transform-origin: left; animation: load 4s ease-in-out infinite; }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes pop {{ from {{ opacity: 0; transform: scale(.6); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes ping {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
      @keyframes in {{ to {{ opacity: .9; }} }}
      @keyframes scroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{P}px); }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes stamp {{ 0%, 4% {{ fill: {t['card']}; }} 8%, 100% {{ fill: {t['accent']}; }} }}
      @keyframes load {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
      @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; opacity: 1 !important; }} }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{t['card']}" stroke="{t['border']}"/>
  <g clip-path="url(#clip)"><rect width="{W}" height="320" fill="url(#grid)" mask="url(#gridfade)"/></g>
  {chr(10).join(parts)}
</svg>
'''


for theme in THEMES:
    _uid = 0
    with open(os.path.join(OUT, f"profile-{theme}.svg"), "w") as f:
        f.write(profile(theme))
print("ok")

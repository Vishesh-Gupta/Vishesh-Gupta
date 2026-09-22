"""Builds the single animated profile card: assets/profile-{dark,light}.svg

Regenerate: python3 assets/generate.py
Icons in assets/icons/ come from skillicons.dev (MIT).
"""
import datetime, os, random, re

OUT = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(OUT, "icons")

THEMES = {
    "dark": dict(card="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 faint="#21262d", tile="#161b22", grid="#161b22", aurora=".16", sheen=("#e6edf3", ".22"), accent="#2C96C7",
                 green="#3fb950", amber="#d29922", red="#f85149", purple="#a371f7", pink="#db61a2"),
    "light": dict(card="#ffffff", border="#d0d7de", fg="#1f2328", muted="#656d76",
                  faint="#eaeef2", tile="#f6f8fa", grid="#f0f3f6", aurora=".09", sheen=("#ffffff", ".75"), accent="#1F7FAF",
                  green="#1a7f37", amber="#9a6700", red="#cf222e", purple="#8250df", pink="#bf3989"),
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
    ("github", "@vishesh-gupta"),
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

CAREER = [  # newest first: (hash, refs, message)
    ("a1f9c2e", "HEAD -> main", "feat: Staff Software Engineer @ Alpaca"),
    ("7c3e81b", "", "feat: Infrastructure Engineer @ Monoceros"),
    (None, "working tree", "wip: building what's next"),  # uncommitted, drawn as a live entry
]

SLOS = [  # (title, subtitle, percent, color)
    ("Error budget", "left this quarter", 97, "green"),
    ("Toil automated", "the rest is next sprint", 90, "accent"),
    ("Alerts actionable", "no pager noise", 100, "purple"),
    ("Coffee reserves", "refill scheduled", 12, "amber"),
]

PODS = [  # (name, ready, status, restarts); a status of None cycles through a crash loop
    ("coffee-maker-7d4f9", "1/1", "Running", "0"),
    ("pager-5c8e2x", "1/1", "Running", "3"),
    ("side-project-x2k9q", "1/1", "Running", "12"),
    ("curiosity-9f1a3", "1/1", "Running", "0"),
    ("sleep-6b7d1", "0/1", None, "42"),
]

PIPELINE = [  # (stage, duration)
    ("commit", "0s"), ("lint", "4s"), ("test", "38s"), ("build", "51s"),
    ("canary 5%", "5m"), ("canary 50%", "10m"), ("production", "✓"),
]

LOGS = [  # (level, message) for the scrolling ticker
    ("OK", "pager quiet for 72h"),
    ("INFO", "coffee v12.3 rolled out to prod"),
    ("WARN", "sleep below SLO threshold"),
    ("INFO", "3 anime episodes queued"),
    ("OK", "terraform plan: no changes"),
    ("INFO", "new stamp added to passport"),
    ("OK", "p99 latency 42ms"),
]

TILES = [  # (icon, color, count-up frames ending on the final value, label, subtitle)
    ("globe", "accent", ["0", "3", "6", "8", "10"], "countries explored", "passport: mostly stamps"),
    ("play", "purple", ["0", "1,200", "3,800", "6,500", "8,700", "9000+"], "anime episodes", "next episode loading…"),
    ("cloche", "amber", ["#99", "#80", "#61", "#50", "#43"], "world-ranked dining", "tasting menus, taken seriously"),
    ("hanger", "pink", ["0", "1", "99", "∞"], "fashion &amp; style", "always dressed for prod"),
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
        "globe": f'<g {s}><circle cx="{cx}" cy="{cy}" r="11"/><ellipse cx="{cx}" cy="{cy}" rx="4.5" ry="11"><animate attributeName="rx" values="11;1;11" dur="6s" repeatCount="indefinite"/></ellipse>'
                 f'<path d="M{cx-11} {cy}h22M{cx-9.5} {cy-5.5}h19M{cx-9.5} {cy+5.5}h19"/></g>',
        "play": f'<g {s}><rect x="{cx-12}" y="{cy-9}" width="24" height="17" rx="3"/>'
                f'<path d="M{cx-3} {cy-4}v8l6.5-4z" fill="{c}"/><path d="M{cx-5} {cy+12}h10"/></g>',
        "cloche": f'<g {s}><path d="M{cx-12} {cy+6}h24M{cx-10} {cy+6}a10 10 0 0 1 20 0"/>'
                  f'<circle cx="{cx}" cy="{cy-6}" r="1.6" fill="{c}"/><path d="M{cx-9} {cy+10}h18"/></g>',
        "hanger": f'<g {s}><path d="M{cx-3} {cy-8}a3 3 0 1 1 3 3v2.5"/>'
                  f'<path d="M{cx} {cy-2.5}l-12 8.5a1.5 1.5 0 0 0 1 2.7h22a1.5 1.5 0 0 0 1-2.7z"/></g>',
    }[kind]


def typed(word, start, step=.09):
    """Reveal a word one character at a time."""
    return "".join(f'<tspan opacity="0">{ch}<set attributeName="opacity" to="1" begin="{start + i*step:.2f}s" fill="freeze"/></tspan>'
                   for i, ch in enumerate(word))


def topology(t):
    """Faint cluster graph with packets hopping between nodes."""
    nodes = dict(a=(560, 112), b=(640, 80), c=(720, 124), d=(800, 92), e=(650, 170), f=(780, 172), g=(846, 138))
    edges = ["ab", "bc", "cd", "ae", "ec", "cf", "fg", "dg"]
    out = ['<g opacity=".55">']
    for u, v in edges:
        (x1, y1), (x2, y2) = nodes[u], nodes[v]
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["border"]}" stroke-dasharray="3 4"/>')
    for i, (x, y) in enumerate(nodes.values()):
        out.append(f'<circle class="breathe" style="animation-delay:{i*.7:.1f}s" cx="{x}" cy="{y}" r="4.5" fill="{t["card"]}" stroke="{t["accent"]}" stroke-width="1.4"/>')
    rnd = random.Random(11)
    for i, (u, v) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[u], nodes[v]
        if rnd.random() < .5:
            x1, y1, x2, y2 = x2, y2, x1, y1
        dur = rnd.uniform(2.4, 4.2)
        col = t["green"] if i % 3 == 0 else t["accent"]
        out.append(f'<circle r="2" fill="{col}" opacity="0"><animateMotion dur="{dur:.1f}s" begin="{i*.45:.2f}s" repeatCount="indefinite" path="M{x1} {y1} L{x2} {y2}"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur:.1f}s" begin="{i*.45:.2f}s" repeatCount="indefinite"/></circle>')
    out.append('</g>')
    return "".join(out)


def aurora(t, H):
    """Soft blurred color fields drifting slowly behind everything."""
    blobs = [(180, 90, 170, t["accent"], 0), (760, 220, 150, t["green"], 1),
             (640, 700, 190, t["purple"], 2), (200, H - 260, 170, t["pink"], 3)]
    op = t["aurora"]
    return "".join(
        f'<circle class="drift a{k % 3}" style="animation-delay:-{k*5}s" cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{op}" filter="url(#blur)"/>'
        for x, y, r, c, k in blobs)


# ── sections (each drawn in its own local coordinates) ───────────────────────
def header(t, theme):
    out = [
        f'<text x="48" y="58" class="mono rise" font-size="14" fill="{t["muted"]}">~ $ {typed("whoami", .25)}<tspan class="cursor" fill="{t["accent"]}"> ▍</tspan></text>',
        f'<text x="46" y="112" class="sans rise d1" font-size="46" font-weight="700" fill="{t["fg"]}" letter-spacing="-1">{NAME}</text>',
        f'<text x="48" y="146" class="sans rise d2" font-size="18" fill="{t["accent"]}" font-weight="600">{ROLE}</text>',
        f'<text x="48" y="172" class="mono rise d3" font-size="13" fill="{t["muted"]}">{TAGLINE}</text>',
        f'<g class="rise d3">{pill(780, 30, 80, "online", t, t["green"])}</g>',
    ]
    out.append(topology(t))
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
    bars_w = n * (bw + gap) - gap
    out.append(f'<clipPath id="bars"><rect x="{bars_x}" y="{top}" width="{bars_w}" height="{rowh * len(ROWS)}"/></clipPath>'
               f'<g clip-path="url(#bars)"><rect class="shimmer" x="{bars_x - 140}" y="{top}" width="140" height="{rowh * len(ROWS)}" fill="url(#sheen)"/></g>')
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
            out.append(f'<g class="float" style="animation-delay:{-k*.37:.2f}s">'
                       + logo(name, theme, round(x), 72, size, "pop", f"animation-delay:{1.2 + k*.06:.2f}s") + '</g>')
            x += size + gap
            k += 1
        x += group_gap - gap
        if gi < len(TOOLBOX) - 1:
            sx = x - group_gap / 2
            out.append(f'<line x1="{sx:.0f}" x2="{sx:.0f}" y1="76" y2="116" stroke="{t["faint"]}"/>')
    return "\n  ".join(out), 140


def countup(frames, x, y, start, t, step=.14):
    """Stack each frame and flash them in turn; the last one stays."""
    out = []
    for k, f in enumerate(frames):
        last = k == len(frames) - 1
        hold = 'fill="freeze"' if last else f'dur="{step:.2f}s"'
        anim = f'<set attributeName="opacity" to="1" begin="{start + k*step:.2f}s" {hold}/>'
        out.append(f'<text x="{x}" y="{y}" opacity="0" class="sans" font-size="30" font-weight="700" fill="{t["fg"]}" letter-spacing="-.5">{f}{anim}</text>')
    return "".join(out)


def offcall(t):
    p0, p1, p2, p3 = (300, 94), (440, 40), (700, 40), (840, 94)
    arc = f"M{p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
    out = [
        f'<text x="40" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ systemctl status life --off-call</text>',
        f'<text x="40" y="54" class="sans" font-size="17" font-weight="600" fill="{t["fg"]}">Life outside the terminal</text>',
        f'<path d="{arc}" fill="none" stroke="{t["border"]}" stroke-width="1.5" stroke-dasharray="2 6" stroke-linecap="round"/>',
    ]
    rnd = random.Random(5)
    for _ in range(22):
        out.append(f'<circle class="twinkle" style="animation-delay:{rnd.uniform(0, 6):.1f}s;animation-duration:{rnd.uniform(3, 6):.1f}s" '
                   f'cx="{rnd.uniform(290, 870):.0f}" cy="{rnd.uniform(8, 112):.0f}" r="{rnd.uniform(.7, 1.4):.1f}" fill="{t["muted"]}"/>')
    for i in range(10):
        u = (i + .5) / 10
        x, y = ((1-u)**3*a + 3*(1-u)**2*u*b + 3*(1-u)*u**2*c + u**3*d for a, b, c, d in zip(p0, p1, p2, p3))
        out.append(f'<circle class="stamp" style="animation-delay:{9*u:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{t["card"]}" stroke="{t["accent"]}" stroke-width="1.5"/>')
    out.append(f'<g><path d="M-9 0 L9 0 M2 -7 L6 0 L2 7 M-7 -3 L-5 0 L-7 3" fill="none" stroke="{t["fg"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<animateMotion dur="9s" repeatCount="indefinite" rotate="auto" path="{arc}"/></g>')

    tg, th, ty = 14, 150, 124
    tw = (W - 80 - tg * (len(TILES) - 1)) / len(TILES)
    for i, (ic, col, frames, label, sub) in enumerate(TILES):
        x, c = 40 + i * (tw + tg), t[col]
        extra = ""
        if ic == "play":
            extra = (f'<rect x="{x+20}" y="{ty+132}" width="{tw-40}" height="3" rx="1.5" fill="{t["faint"]}"/>'
                     f'<rect class="progress" x="{x+20}" y="{ty+132}" width="{tw-40}" height="3" rx="1.5" fill="{c}"/>')
        out.append(f'''<g class="rise" style="animation-delay:{1.8 + i*.12:.2f}s">
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{t['tile']}" stroke="{t['faint']}"/>
      {icon(ic, x + 34, ty + 34, c)}
      {countup(frames, x + 20, ty + 88, 1.9 + i*.12, t)}
      <text x="{x+20}" y="{ty+108}" class="sans" font-size="13" font-weight="600" fill="{c}">{label}</text>
      <text x="{x+20}" y="{ty+125}" class="sans" font-size="11.5" fill="{t['muted']}">{sub}</text>
      {extra}
    </g>''')
    return "\n  ".join(out), ty + th


def slos(t):
    """Radial SLO gauges that fill on load; low ones slowly drain and refill."""
    colw = (W - 80) / len(SLOS)
    r, cy = 26, 72
    out = [f'<text x="40" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ slo report --window 30d</text>']
    for i, (title, sub, pct, col) in enumerate(SLOS):
        cx, c = 40 + i * colw + r + 8, t[col]
        begin = 1.4 + i * .15
        fill = (f'<animate attributeName="stroke-dasharray" from="0 100" to="{pct} 100" dur="1.6s" begin="{begin:.2f}s" fill="freeze" '
                f'calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>')
        if pct < 25:
            fill += (f'<animate attributeName="stroke-dasharray" values="{pct} 100;{pct/3:.0f} 100;{pct} 100" dur="9s" '
                     f'begin="{begin + 1.6:.2f}s" repeatCount="indefinite"/>')
        out.append(
            f'<g class="rise" style="animation-delay:{begin:.2f}s">'
            f'<circle class="spin" cx="{cx}" cy="{cy}" r="{r + 7}" fill="none" stroke="{t["border"]}" stroke-dasharray="1 5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["faint"]}" stroke-width="6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round" pathLength="100" '
            f'stroke-dasharray="0 100" transform="rotate(-90 {cx} {cy})">{fill}</circle>'
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" class="mono" font-size="12" font-weight="700" fill="{t["fg"]}">{pct}%</text>'
            f'<text x="{cx + r + 18}" y="{cy - 3}" class="sans" font-size="14" font-weight="600" fill="{t["fg"]}">{title}</text>'
            f'<text x="{cx + r + 18}" y="{cy + 15}" class="sans" font-size="11.5" fill="{t["muted"]}">{sub}</text></g>')
    return "\n  ".join(out), cy + r + 16


def pipeline(t):
    """A release walking through CI/CD stages on a loop."""
    n, T, travel, hold = len(PIPELINE), 10, .7, .93
    x0, x1, cy = 76, W - 76, 74
    out = [
        f'<text x="40" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ git push origin main</text>',
        f'<text x="{W-110}" y="28" text-anchor="end" class="mono" font-size="12.5" fill="{t["muted"]}">run #4815 ·</text>',
        f'<text class="running mono" x="{W-40}" y="28" text-anchor="end" font-size="12.5" fill="{t["amber"]}">running…</text>',
        f'<text class="deployed mono" x="{W-40}" y="28" text-anchor="end" font-size="12.5" fill="{t["green"]}">deployed</text>',
        f'<line x1="{x0}" x2="{x1}" y1="{cy}" y2="{cy}" stroke="{t["faint"]}" stroke-width="3" stroke-linecap="round"/>',
        f'<line class="pipe" x1="{x0}" x2="{x1}" y1="{cy}" y2="{cy}" stroke="url(#pipegrad)" stroke-width="3" stroke-linecap="round"/>',
    ]
    css = []
    for k, (stage, dur) in enumerate(PIPELINE):
        cx = x0 + (x1 - x0) * k / (n - 1)
        reach = travel * k / (n - 1) * 100
        run = max(reach - 6, 0)
        css.append(f"@keyframes run{k} {{ 0%, {run:.1f}% {{ opacity: 0; }} {run + .1:.1f}%, {reach:.1f}% {{ opacity: 1; }} {reach + .1:.1f}%, 100% {{ opacity: 0; }} }}")
        css.append(f"@keyframes done{k} {{ 0%, {reach:.1f}% {{ opacity: 0; }} {reach + .1:.1f}%, {hold*100:.0f}% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}")
        out.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="11" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5"/>')
        out.append(f'<circle style="animation: run{k} {T}s linear infinite 1.5s; opacity: 0" cx="{cx:.1f}" cy="{cy}" r="11" fill="{t["card"]}" stroke="{t["amber"]}" stroke-width="2" stroke-dasharray="4 3"/>')
        out.append(f'<g style="animation: done{k} {T}s linear infinite 1.5s; opacity: 0"><circle cx="{cx:.1f}" cy="{cy}" r="11" fill="{t["green"]}"/>'
                   f'<path d="M{cx-4.5:.1f} {cy}l3 3 6-6.5" fill="none" stroke="{t["card"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        out.append(f'<text x="{cx:.1f}" y="{cy + 30}" text-anchor="middle" class="sans" font-size="12.5" font-weight="600" fill="{t["fg"]}">{stage}</text>')
        out.append(f'<text x="{cx:.1f}" y="{cy + 46}" text-anchor="middle" class="mono" font-size="11" fill="{t["muted"]}">{dur}</text>')
    css.append(f".pipe {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: pipe {T}s linear infinite 1.5s; }}")
    css.append(f"@keyframes pipe {{ 0% {{ transform: scaleX(0); opacity: 1; }} {travel*100:.0f}%, {hold*100:.0f}% {{ transform: scaleX(1); opacity: 1; }} 100% {{ transform: scaleX(1); opacity: 0; }} }}")
    css.append(f".deployed {{ opacity: 0; animation: dep {T}s linear infinite 1.5s; }}")
    css.append(f".running {{ animation: runlabel {T}s linear infinite 1.5s; }}")
    css.append(f"@keyframes runlabel {{ 0%, {travel*100:.0f}% {{ opacity: 1; }} {travel*100 + 1:.0f}%, {hold*100:.0f}% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}")
    css.append(f"@keyframes dep {{ 0%, {travel*100:.0f}% {{ opacity: 0; }} {travel*100 + 1:.0f}%, {hold*100:.0f}% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}")
    return "\n  ".join(out), cy + 58, "\n      ".join(css)


def ticker(t):
    """Log lines drifting right to left; positions are explicit so the loop is seamless."""
    colors = dict(OK=t["green"], INFO=t["accent"], WARN=t["amber"])
    items, x = [], 0
    for level, msg in LOGS:
        items.append((x, level, msg))
        x += (len(level) + len(msg) + 3) * 6.9 + 44
    period = x
    out = [f'<rect x="40" y="0" width="{W-80}" height="34" rx="10" fill="{t["tile"]}" stroke="{t["faint"]}"/>',
           f'<g mask="url(#tickerfade)"><g class="ticker">']
    for rep_ in range(3):
        for ix, level, msg in items:
            out.append(f'<text x="{56 + ix + rep_*period:.1f}" y="21.5" class="mono" font-size="11.5" fill="{t["muted"]}">'
                       f'<tspan fill="{colors[level]}">[{level}]</tspan> {msg}</text>')
    out.append('</g></g>')
    css = (f".ticker {{ animation: ticker {period/22:.1f}s linear infinite; }}\n"
           f"      @keyframes ticker {{ to {{ transform: translateX(-{period:.1f}px); }} }}")
    return "\n  ".join(out), 34, css


def journey(t):
    """Two terminal panels side by side: career as a git log, life as kubectl pods."""
    ph, py = 176, 44
    lx, lw = 40, 400
    rx, rw = 460, W - 40 - 460
    out = [
        f'<text x="{lx}" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ git log --graph --oneline career</text>',
        f'<text x="{rx}" y="28" class="mono" font-size="12.5" fill="{t["muted"]}">$ kubectl get pods -n life</text>',
        f'<rect x="{lx}" y="{py}" width="{lw}" height="{ph}" rx="12" fill="{t["tile"]}" stroke="{t["faint"]}"/>',
        f'<rect x="{rx}" y="{py}" width="{rw}" height="{ph}" rx="12" fill="{t["tile"]}" stroke="{t["faint"]}"/>',
    ]
    # git graph
    gx, step = lx + 24, 50
    y0 = py + (ph - step * (len(CAREER) - 1) - 17) / 2 + 8
    committed = [i for i, c in enumerate(CAREER) if c[0]]
    # the wip entry sits above HEAD; committed history hangs below it
    order = [i for i, c in enumerate(CAREER) if not c[0]] + committed
    ys = {i: y0 + k * step for k, i in enumerate(order)}
    first, last = ys[committed[0]], ys[committed[-1]]
    out.append(f'<line x1="{gx}" x2="{gx}" y1="{first - 4}" y2="{last - 4}" stroke="{t["border"]}" stroke-width="2"/>')
    for i, (sha, refs, msg) in enumerate(CAREER):
        y = ys[i]
        d = f"animation-delay:{2.0 + order.index(i)*.15:.2f}s"
        if sha is None:
            out.append(f'<line class="flow" x1="{gx}" x2="{gx}" y1="{y - 4}" y2="{first - 4}" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="3 4"/>')
            out.append(f'<g class="rise" style="{d}"><circle class="breathe" cx="{gx}" cy="{y-4}" r="4.5" fill="{t["tile"]}" stroke="{t["accent"]}" stroke-width="1.6" stroke-dasharray="2 2"/>'
                       f'<text x="{gx + 20}" y="{y}" class="mono" font-size="11.5" fill="{t["muted"]}">••••••• <tspan fill="{t["accent"]}">({refs})</tspan></text>'
                       f'<text x="{gx + 20}" y="{y + 17}" class="sans" font-size="13" font-style="italic" fill="{t["muted"]}">{msg}<tspan class="cursor" fill="{t["accent"]}"> ▍</tspan></text></g>')
            continue
        dot = ping_dot(gx, y - 4, 4.5, t["accent"]) if i == committed[0] else f'<circle cx="{gx}" cy="{y-4}" r="4" fill="{t["tile"]}" stroke="{t["muted"]}" stroke-width="1.6"/>'
        ref = f' <tspan fill="{t["accent"]}">({refs})</tspan>' if refs else ""
        out.append(f'<g class="rise" style="{d}">{dot}'
                   f'<text x="{gx + 20}" y="{y}" class="mono" font-size="11.5" fill="{t["amber"]}">{sha}{ref}</text>'
                   f'<text x="{gx + 20}" y="{y + 17}" class="sans" font-size="13" fill="{t["fg"]}">{msg}</text></g>')
    # kubectl table
    cols = [rx + 20, rx + 158, rx + 200, rx + rw - 20]
    hy = py + 28
    for x, h, anchor in zip(cols, ("NAME", "READY", "STATUS", "RESTARTS"), ("start", "start", "start", "end")):
        out.append(f'<text x="{x}" y="{hy}" text-anchor="{anchor}" class="mono" font-size="11" fill="{t["muted"]}">{h}</text>')
    for i, (name, ready, st, restarts) in enumerate(PODS):
        y = hy + 26 + i * 24
        d = f"animation-delay:{2.2 + i*.18:.2f}s"
        if st is None:
            cells = "".join(f'<text class="cycle c{k}" x="{cols[2]}" y="{y}" font-size="11" fill="{c}">{label}</text>'
                            for k, (label, c) in enumerate((("ContainerCreating", t["amber"]), ("Running", t["green"]), ("CrashLoopBackOff", t["red"]))))
        else:
            cells = f'<text x="{cols[2]}" y="{y}" font-size="11" fill="{t["green"]}">{st}</text>'
        out.append(f'<g class="rise mono" style="{d}">'
                   f'<text x="{cols[0]}" y="{y}" font-size="11" fill="{t["fg"]}">{name}</text>'
                   f'<text x="{cols[1]}" y="{y}" font-size="11" fill="{t["muted"]}">{ready}</text>{cells}'
                   f'<text x="{cols[3]}" y="{y}" text-anchor="end" font-size="11" fill="{t["muted"]}">{restarts}</text></g>')
    return "\n  ".join(out), py + ph


def footer(t):
    out = [
        ping_dot(44, 22, 3.5, t["green"]),
        f'<text x="56" y="26" class="mono" font-size="12" fill="{t["muted"]}">last deployed {datetime.date.today():%Y-%m-%d} · build <tspan fill="{t["green"]}">passing</tspan></text>',
        f'<text x="{W-40}" y="26" text-anchor="end" class="mono" font-size="12" fill="{t["muted"]}">thanks for stopping by · <tspan fill="{t["green"]}">exit 0</tspan></text>',
    ]
    return "\n  ".join(out), 48


# ── assembly ──────────────────────────────────────────────────────────────────
def profile(theme):
    t = THEMES[theme]
    P = 300
    parts, y, extra_css = [], 0, []
    for fn, gap_after, rule in ((lambda: header(t, theme), 10, False),
                                (lambda: status(t), 28, True),
                                (lambda: slos(t), 20, True),
                                (lambda: pipeline(t), 22, True),
                                (lambda: journey(t), 24, True),
                                (lambda: toolbox(t, theme), 20, True),
                                (lambda: offcall(t), 22, False),
                                (lambda: ticker(t), 18, False),
                                (lambda: footer(t), 0, False)):
        body, h, *extra = fn()
        extra_css += extra
        parts.append(f'<g transform="translate(0 {y})">\n  {body}\n  </g>')
        y += h + gap_after
        if rule:
            parts.append(divider(y - gap_after / 2, t))
    H = y
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}, {ROLE}. Status: cloud architecture, DevOps and SRE, Kubernetes, infrastructure as code and observability all operational. Toolbox: AWS, Google Cloud, Kubernetes, Docker, Terraform, Linux, Python, Go, Bash, Prometheus, Grafana, GitHub Actions. Latest deploy: commit, lint, test, build, canary, production. SLOs: 97% error budget left, 90% toil automated, 100% actionable alerts, 12% coffee. Career: Staff Software Engineer at Alpaca, previously Infrastructure Engineer at Monoceros. Off-call: 10 countries, 9000+ anime episodes, world #43 dining, fashion and style.">
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
    <linearGradient id="sheen" x1="0" x2="1">
      <stop offset="0" stop-color="{t['sheen'][0]}" stop-opacity="0"/><stop offset=".5" stop-color="{t['sheen'][0]}" stop-opacity="{t['sheen'][1]}"/><stop offset="1" stop-color="{t['sheen'][0]}" stop-opacity="0"/>
    </linearGradient>
    <filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="70"/></filter>
    <linearGradient id="pipegrad" x1="0" x2="1">
      <stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['green']}"/>
    </linearGradient>
    <linearGradient id="edgefade" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".06" stop-color="#fff"/><stop offset=".94" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="tickerfade" maskUnits="userSpaceOnUse" x="40" y="0" width="{W-80}" height="34"><rect x="40" y="0" width="{W-80}" height="34" fill="url(#edgefade)"/></mask>
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
      .spin {{ transform-box: fill-box; transform-origin: center; animation: spin 40s linear infinite; }}
      .flow {{ animation: flow 1.2s linear infinite; }}
      @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
      @keyframes flow {{ to {{ stroke-dashoffset: -14; }} }}
      .float {{ animation: float 4.5s ease-in-out infinite; }}
      .breathe {{ transform-box: fill-box; transform-origin: center; animation: breathe 4s ease-in-out infinite; }}
      .shimmer {{ animation: shimmer 7s ease-in-out infinite 2.5s; }}
      .twinkle {{ opacity: .1; animation: twinkle 4s ease-in-out infinite; }}
      .drift {{ animation: drift0 22s ease-in-out infinite alternate; }}
      .drift.a1 {{ animation-name: drift1; animation-duration: 26s; }}
      .drift.a2 {{ animation-name: drift2; animation-duration: 30s; }}
      .cycle {{ opacity: 0; animation: cycle 7.5s steps(1) infinite 3s; }}
      .cycle.c1 {{ animation-name: cycle1; }} .cycle.c2 {{ animation-name: cycle2; }}
      @keyframes float {{ 50% {{ transform: translateY(-3px); }} }}
      @keyframes breathe {{ 50% {{ transform: scale(1.25); }} }}
      @keyframes shimmer {{ 0% {{ transform: translateX(0); }} 45%, 100% {{ transform: translateX({48*8 + 140}px); }} }}
      @keyframes twinkle {{ 50% {{ opacity: .7; }} }}
      @keyframes drift0 {{ to {{ transform: translate(120px, 40px); }} }}
      @keyframes drift1 {{ to {{ transform: translate(-140px, 60px); }} }}
      @keyframes drift2 {{ to {{ transform: translate(80px, -70px); }} }}
      @keyframes cycle {{ 0% {{ opacity: 1; }} 20%, 100% {{ opacity: 0; }} }}
      @keyframes cycle1 {{ 0% {{ opacity: 0; }} 20% {{ opacity: 1; }} 33%, 100% {{ opacity: 0; }} }}
      @keyframes cycle2 {{ 0%, 33% {{ opacity: 0; }} 34%, 100% {{ opacity: 1; }} }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes pop {{ from {{ opacity: 0; transform: scale(.6); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes ping {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
      @keyframes in {{ to {{ opacity: .9; }} }}
      @keyframes scroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{P}px); }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes stamp {{ 0%, 4% {{ fill: {t['card']}; }} 8%, 100% {{ fill: {t['accent']}; }} }}
      @keyframes load {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
      {chr(10).join("      " + c for c in extra_css)}
      @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .rise, .pop, .bar, .cycle.c2 {{ opacity: 1 !important; }} }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{t['card']}" stroke="{t['border']}"/>
  <g clip-path="url(#clip)">{aurora(t, H)}<rect width="{W}" height="320" fill="url(#grid)" mask="url(#gridfade)"/></g>
  {chr(10).join(parts)}
</svg>
'''


for theme in THEMES:
    _uid = 0
    with open(os.path.join(OUT, f"profile-{theme}.svg"), "w") as f:
        f.write(profile(theme))
print("ok")

"""Builds the single animated profile card: assets/profile-{dark,light}.svg

Regenerate: python3 assets/generate.py
Icons in assets/icons/ come from skillicons.dev (MIT).
"""
import os, random, re

OUT = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(OUT, "icons")

THEMES = {
    "dark": dict(card="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e",
                 faint="#21262d", tile="#161b22", grid="#161b22", aurora=".16", sheen=("#e6edf3", ".22"),
                 accent="#2C96C7", green="#3fb950", amber="#d29922", red="#f85149", purple="#a371f7", pink="#db61a2"),
    "light": dict(card="#ffffff", border="#d0d7de", fg="#1f2328", muted="#656d76",
                  faint="#eaeef2", tile="#f6f8fa", grid="#f0f3f6", aurora=".09", sheen=("#ffffff", ".75"),
                  accent="#1F7FAF", green="#1a7f37", amber="#9a6700", red="#cf222e", purple="#8250df", pink="#bf3989"),
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

TOOLBOX = [  # two rows of logos in the header, wired together as a little cluster
    ["aws", "gcp", "kubernetes", "docker", "terraform", "linux"],
    ["python", "go", "bash", "prometheus", "grafana", "githubactions"],
]

ROWS = [  # (component, uptime)
    ("Cloud Architecture", "99.99%"),
    ("DevOps &amp; SRE", "99.98%"),
    ("Kubernetes &amp; Containers", "99.97%"),
    ("Infrastructure as Code", "100%"),
    ("Observability", "99.99%"),
]

SLOS = [  # (title, percent, color)
    ("Error budget", 97, "green"),
    ("Toil automated", 90, "accent"),
    ("Alerts actionable", 100, "purple"),
    ("Coffee reserves", 12, "amber"),
]

PIPELINE = [  # (stage, duration)
    ("commit", "0s"), ("lint", "4s"), ("test", "38s"), ("build", "51s"),
    ("canary 5%", "5m"), ("canary 50%", "10m"), ("production", "✓"),
]

CAREER = [  # newest first: (hash, refs, message); hash None is the live, uncommitted entry
    (None, "working tree", "wip: building what's next"),
    ("a1f9c2e", "HEAD -> main", "feat: Staff Software Engineer @ Alpaca"),
    ("7c3e81b", "", "feat: Infrastructure Engineer @ Monoceros"),
]

PODS = [  # (name, ready, status, restarts); status None cycles through a crash loop
    ("coffee-maker-7d4f9", "1/1", "Running", "0"),
    ("pager-5c8e2x", "1/1", "Running", "3"),
    ("side-project-x2k9q", "1/1", "Running", "12"),
    ("curiosity-9f1a3", "1/1", "Running", "0"),
    ("sleep-6b7d1", "0/1", None, "42"),
]

TILES = [  # (icon, color, count-up frames ending on the final value, label)
    ("globe", "accent", ["0", "3", "6", "8", "10"], "countries explored"),
    ("play", "purple", ["0", "1,200", "3,800", "6,500", "8,700", "9000+"], "anime episodes"),
    ("cloche", "amber", ["#99", "#80", "#61", "#50", "#43"], "world-ranked dining"),
    ("hanger", "pink", ["0", "1", "99", "∞"], "fashion &amp; style"),
]

LOGS = [  # (level, message) for the footer ticker
    ("OK", "pager quiet for 72h"),
    ("INFO", "coffee v12.3 rolled out to prod"),
    ("WARN", "sleep below SLO threshold"),
    ("INFO", "3 anime episodes queued"),
    ("OK", "terraform plan: no changes"),
    ("INFO", "new stamp added to passport"),
    ("OK", "thanks for stopping by · exit 0"),
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
    return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="none" stroke="{t["border"]}"/>'
            + ping_dot(x + 16, y + 13, 3.5, color)
            + f'<text x="{x+27}" y="{y+17.5}" class="mono" font-size="11.5" fill="{t["muted"]}">{label}</text>')


def mono(x, y, text, t, size=12, color=None, anchor="start", cls="mono"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" font-size="{size}" '
            f'fill="{color or t["muted"]}">{text}</text>')


def typed(word, start, step=.09):
    """Reveal a word one character at a time."""
    return "".join(f'<tspan opacity="0">{ch}<set attributeName="opacity" to="1" begin="{start + i*step:.2f}s" fill="freeze"/></tspan>'
                   for i, ch in enumerate(word))


def countup(frames, x, y, start, t, size, step=.14):
    """Stack each frame and flash them in turn; the last one stays."""
    out = []
    for k, f in enumerate(frames):
        hold = 'fill="freeze"' if k == len(frames) - 1 else f'dur="{step:.2f}s"'
        out.append(f'<text x="{x}" y="{y}" opacity="0" class="sans" font-size="{size}" font-weight="700" fill="{t["fg"]}" letter-spacing="-.5">'
                   f'{f}<set attributeName="opacity" to="1" begin="{start + k*step:.2f}s" {hold}/></text>')
    return "".join(out)


def heartbeat(y0, period=300):
    """One ECG period tiled so the path scrolls seamlessly by exactly one period."""
    rnd = random.Random(7)
    noise = [rnd.uniform(-2, 2) for _ in range(period // 12)]
    pts = []
    periods = (W + period * 2) // period
    for k in range(periods):
        base = k * period
        for i, n in enumerate(noise):
            x = base + i * 12
            if i == 12:
                pts += [(x, y0), (x + 8, y0 - 5), (x + 14, y0 + 8), (x + 22, y0 - 25),
                        (x + 30, y0 + 11), (x + 38, y0 - 3), (x + 46, y0)]
            elif not 12 < i < 17:
                pts.append((x, y0 + (0 if i == 0 else n)))
    pts.append((periods * period, y0))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def icon(kind, cx, cy, c):
    s = f'fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    return {
        "globe": f'<g {s}><circle cx="{cx}" cy="{cy}" r="11"/><ellipse cx="{cx}" cy="{cy}" rx="4.5" ry="11">'
                 f'<animate attributeName="rx" values="11;1;11" dur="6s" repeatCount="indefinite"/></ellipse>'
                 f'<path d="M{cx-11} {cy}h22M{cx-9.5} {cy-5.5}h19M{cx-9.5} {cy+5.5}h19"/></g>',
        "play": f'<g {s}><rect x="{cx-12}" y="{cy-9}" width="24" height="17" rx="3"/>'
                f'<path d="M{cx-3} {cy-4}v8l6.5-4z" fill="{c}"/><path d="M{cx-5} {cy+12}h10"/></g>',
        "cloche": f'<g {s}><path d="M{cx-12} {cy+6}h24M{cx-10} {cy+6}a10 10 0 0 1 20 0"/>'
                  f'<circle cx="{cx}" cy="{cy-6}" r="1.6" fill="{c}"/><path d="M{cx-9} {cy+10}h18"/></g>',
        "hanger": f'<g {s}><path d="M{cx-3} {cy-8}a3 3 0 1 1 3 3v2.5"/>'
                  f'<path d="M{cx} {cy-2.5}l-12 8.5a1.5 1.5 0 0 0 1 2.7h22a1.5 1.5 0 0 0 1-2.7z"/></g>',
    }[kind]


# ── sections: each returns (svg, height, extra css) in its own local coordinates ──
def header(t, theme):
    out = [
        mono(48, 42, f'~ $ {typed("whoami", .25)}<tspan class="cursor" fill="{t["accent"]}"> ▍</tspan>', t, 13),
        f'<text x="46" y="86" class="sans rise d1" font-size="40" font-weight="700" fill="{t["fg"]}" letter-spacing="-1">{NAME}</text>',
        f'<text x="48" y="115" class="sans rise d2" font-size="17" fill="{t["accent"]}" font-weight="600">{ROLE}</text>',
        mono(48, 139, TAGLINE, t, 12.5, cls="mono rise d3"),
        f'<g class="rise d3">{pill(W-40-78, 22, 78, "online", t, t["green"])}</g>',
    ]
    # toolbox cluster: logos are the nodes, packets hop along the wires between them
    size, step, row_y = 36, 46, (62, 110)
    x0 = W - 40 - 5 * step - size
    pos = {(r, c): (x0 + c * step + size / 2, row_y[r] + size / 2) for r in range(2) for c in range(6)}
    wires = ([((r, c), (r, c + 1)) for r in range(2) for c in range(5)]
             + [((0, c), (1, c)) for c in (0, 2, 3, 5)] + [((0, 1), (1, 2)), ((0, 4), (1, 3))])
    rnd = random.Random(11)
    out.append('<g opacity=".7">')
    for a, b in wires:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{t["border"]}" stroke-dasharray="2 4"/>')
    for i, (a, b) in enumerate(rnd.sample(wires, 9)):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if rnd.random() < .5:
            x1, y1, x2, y2 = x2, y2, x1, y1
        dur, col = rnd.uniform(1.8, 3.2), (t["green"] if i % 3 == 0 else t["accent"])
        out.append(f'<circle r="2" fill="{col}" opacity="0"><animateMotion dur="{dur:.1f}s" begin="{i*.4:.1f}s" repeatCount="indefinite" path="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}"/>'
                   f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur:.1f}s" begin="{i*.4:.1f}s" repeatCount="indefinite"/></circle>')
    out.append('</g>')
    k = 0
    for r, names in enumerate(TOOLBOX):
        for c, name in enumerate(names):
            out.append(f'<g class="float" style="animation-delay:{-k*.37:.2f}s">'
                       + logo(name, theme, x0 + c * step, row_y[r], size, "pop", f"animation-delay:{.9 + k*.05:.2f}s") + '</g>')
            k += 1
    # connect row
    x = 48
    for i, (name, handle) in enumerate(CONNECT):
        d = f"animation-delay:{.6 + i*.1:.2f}s"
        out.append(logo(name, theme, x, 156, 22, "rise", d))
        out.append(f'<text x="{x+31}" y="172" class="mono rise" style="{d}" font-size="12" fill="{t["muted"]}">{handle}</text>')
        x += 31 + len(handle) * 7.3 + 26
    # heartbeat doubles as the divider under the header
    out.append(f'<rect x="1" y="184" width="{W-2}" height="48" fill="url(#trace)" mask="url(#beat)"/>')
    return "\n  ".join(out), 232, ""


def status_and_slos(t):
    top, rowh, bars_x, n, bw, gap = 38, 28, 236, 38, 4, 3.4
    split = 596
    out = [
        ping_dot(46, 14, 4.5, t["green"]),
        f'<text x="60" y="19" class="sans" font-size="15" font-weight="600" fill="{t["fg"]}">All systems operational</text>',
        mono(split - 34, 19, "vish.status · 48w", t, 11.5, anchor="end"),
    ]
    for i, (label, metric) in enumerate(ROWS):
        y = top + i * rowh
        rnd = random.Random(i * 31 + 3)
        out.append(f'<text x="40" y="{y+17}" class="sans" font-size="13" font-weight="600" fill="{t["fg"]}">{label}</text>')
        for b in range(n):
            c = t["amber"] if rnd.random() < .03 else t["green"]
            out.append(f'<rect class="bar" style="animation-delay:{.8 + b*.012 + i*.05:.3f}s" x="{bars_x + b*(bw+gap):.1f}" y="{y+4}" width="{bw}" height="18" rx="1.2" fill="{c}"/>')
        out.append(mono(split - 34, y + 17, metric, t, 11.5, t["green"], "end"))
        if i < len(ROWS) - 1:
            out.append(f'<line x1="40" x2="{split - 34}" y1="{y+rowh-1}" y2="{y+rowh-1}" stroke="{t["faint"]}" stroke-dasharray="2 4"/>')
    bars_w, bars_h = n * (bw + gap) - gap, rowh * len(ROWS)
    out.append(f'<clipPath id="bars"><rect x="{bars_x}" y="{top}" width="{bars_w:.1f}" height="{bars_h}"/></clipPath>'
               f'<g clip-path="url(#bars)"><rect class="shimmer" x="{bars_x - 110}" y="{top}" width="110" height="{bars_h}" fill="url(#sheen)"/></g>')
    css = f"@keyframes shimmer {{ 0% {{ transform: translateX(0); }} 45%, 100% {{ transform: translateX({bars_w + 110:.0f}px); }} }}"
    height = top + bars_h

    # SLO gauges, 2x2, to the right of a thin divider
    out.append(f'<line x1="{split}" x2="{split}" y1="4" y2="{height - 4}" stroke="{t["faint"]}"/>')
    out.append(mono(split + 30, 19, "$ slo report --30d", t, 11.5))
    cw, ch, gx, gy = (W - 40 - split - 30) / 2, (height - 34) / 2, split + 30, 34
    r = 16
    for i, (title, pct, col) in enumerate(SLOS):
        cx = gx + (i % 2) * cw + cw / 2
        cy = gy + (i // 2) * ch + 24
        c, begin = t[col], 1.4 + i * .15
        anim = (f'<animate attributeName="stroke-dasharray" from="0 100" to="{pct} 100" dur="1.6s" begin="{begin:.2f}s" fill="freeze" '
                f'calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>')
        if pct < 25:  # low reserves keep draining and topping back up
            anim += (f'<animate attributeName="stroke-dasharray" values="{pct} 100;{pct/3:.0f} 100;{pct} 100" dur="9s" '
                     f'begin="{begin + 1.6:.2f}s" repeatCount="indefinite"/>')
        out.append(
            f'<g class="rise" style="animation-delay:{begin:.2f}s">'
            f'<circle class="spin" cx="{cx}" cy="{cy}" r="{r + 5}" fill="none" stroke="{t["border"]}" stroke-dasharray="1 4"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["faint"]}" stroke-width="4.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="4.5" stroke-linecap="round" pathLength="100" '
            f'stroke-dasharray="0 100" transform="rotate(-90 {cx} {cy})">{anim}</circle>'
            f'<text x="{cx}" y="{cy + 3.5}" text-anchor="middle" class="mono" font-size="9" font-weight="700" fill="{t["fg"]}">{pct}%</text>'
            f'<text x="{cx}" y="{cy + r + 22}" text-anchor="middle" class="sans" font-size="11.5" font-weight="600" fill="{t["fg"]}">{title}</text></g>')
    return "\n  ".join(out), height, css


def pipeline(t):
    """A release walking through CI/CD stages on a loop."""
    n, T, travel, hold = len(PIPELINE), 10, .7, .93
    x0, x1, cy = 80, W - 80, 40
    out = [
        mono(40, 14, "$ git push origin main", t, 11.5),
        mono(W - 106, 14, "run #4815 ·", t, 11.5, anchor="end"),
        mono(W - 40, 14, "running…", t, 11.5, t["amber"], "end", "mono running"),
        mono(W - 40, 14, "deployed", t, 11.5, t["green"], "end", "mono deployed"),
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
        out.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="9" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="1.5"/>')
        out.append(f'<circle style="animation: run{k} {T}s linear infinite 1.5s; opacity: 0" cx="{cx:.1f}" cy="{cy}" r="9" fill="{t["card"]}" stroke="{t["amber"]}" stroke-width="2" stroke-dasharray="3 3"/>')
        out.append(f'<g style="animation: done{k} {T}s linear infinite 1.5s; opacity: 0"><circle cx="{cx:.1f}" cy="{cy}" r="9" fill="{t["green"]}"/>'
                   f'<path d="M{cx-3.8:.1f} {cy}l2.6 2.6 5-5.4" fill="none" stroke="{t["card"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        out.append(f'<text x="{cx:.1f}" y="{cy + 26}" text-anchor="middle" class="sans" font-size="11.5" font-weight="600" fill="{t["fg"]}">{stage}'
                   f'<tspan class="mono" font-weight="400" font-size="10.5" fill="{t["muted"]}"> {dur}</tspan></text>')
    css += [
        f".pipe {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: pipe {T}s linear infinite 1.5s; }}",
        f"@keyframes pipe {{ 0% {{ transform: scaleX(0); opacity: 1; }} {travel*100:.0f}%, {hold*100:.0f}% {{ transform: scaleX(1); opacity: 1; }} 100% {{ transform: scaleX(1); opacity: 0; }} }}",
        f".deployed {{ opacity: 0; animation: dep {T}s linear infinite 1.5s; }}",
        f"@keyframes dep {{ 0%, {travel*100:.0f}% {{ opacity: 0; }} {travel*100 + 1:.0f}%, {hold*100:.0f}% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}",
        f".running {{ animation: runlabel {T}s linear infinite 1.5s; }}",
        f"@keyframes runlabel {{ 0%, {travel*100:.0f}% {{ opacity: 1; }} {travel*100 + 1:.0f}%, {hold*100:.0f}% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}",
    ]
    return "\n  ".join(out), cy + 32, "\n      ".join(css)


def journey(t):
    """Career as a git log, life as kubectl pods, side by side."""
    ph, py = 114, 24
    lx, lw = 40, 400
    rx, rw = 460, W - 40 - 460
    out = [
        mono(lx, 12, "$ git log --graph --oneline career", t, 11.5),
        mono(rx, 12, "$ kubectl get pods -n life", t, 11.5),
        f'<rect x="{lx}" y="{py}" width="{lw}" height="{ph}" rx="10" fill="{t["tile"]}" stroke="{t["faint"]}"/>',
        f'<rect x="{rx}" y="{py}" width="{rw}" height="{ph}" rx="10" fill="{t["tile"]}" stroke="{t["faint"]}"/>',
    ]
    gx, step, y0 = lx + 22, 34, py + 24
    ys = [y0 + k * step for k in range(len(CAREER))]
    committed = [i for i, c in enumerate(CAREER) if c[0]]
    head_y = ys[committed[0]]
    out.append(f'<line x1="{gx}" x2="{gx}" y1="{head_y - 4}" y2="{ys[committed[-1]] - 4}" stroke="{t["border"]}" stroke-width="2"/>')
    for i, (sha, refs, msg) in enumerate(CAREER):
        y, d = ys[i], f"animation-delay:{2.0 + i*.15:.2f}s"
        if sha is None:
            out.append(f'<line class="flow" x1="{gx}" x2="{gx}" y1="{y - 4}" y2="{head_y - 4}" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="3 4"/>')
            out.append(f'<g class="rise" style="{d}"><circle class="breathe" cx="{gx}" cy="{y-4}" r="4" fill="{t["tile"]}" stroke="{t["accent"]}" stroke-width="1.6" stroke-dasharray="2 2"/>'
                       f'<text x="{gx + 18}" y="{y}" class="mono" font-size="10.5" fill="{t["muted"]}">••••••• <tspan fill="{t["accent"]}">({refs})</tspan></text>'
                       f'<text x="{gx + 18}" y="{y + 15}" class="sans" font-size="12.5" font-style="italic" fill="{t["muted"]}">{msg}<tspan class="cursor" fill="{t["accent"]}"> ▍</tspan></text></g>')
            continue
        dot = ping_dot(gx, y - 4, 4, t["accent"]) if i == committed[0] else f'<circle cx="{gx}" cy="{y-4}" r="3.6" fill="{t["tile"]}" stroke="{t["muted"]}" stroke-width="1.6"/>'
        ref = f' <tspan fill="{t["accent"]}">({refs})</tspan>' if refs else ""
        out.append(f'<g class="rise" style="{d}">{dot}'
                   f'<text x="{gx + 18}" y="{y}" class="mono" font-size="10.5" fill="{t["amber"]}">{sha}{ref}</text>'
                   f'<text x="{gx + 18}" y="{y + 15}" class="sans" font-size="12.5" fill="{t["fg"]}">{msg}</text></g>')
    cols = [rx + 18, rx + 158, rx + 198, rx + rw - 18]
    hy = py + 20
    for x, h, anchor in zip(cols, ("NAME", "READY", "STATUS", "RESTARTS"), ("start", "start", "start", "end")):
        out.append(mono(x, hy, h, t, 10, anchor=anchor))
    for i, (name, ready, st, restarts) in enumerate(PODS):
        y, d = hy + 18 + i * 17, f"animation-delay:{2.2 + i*.18:.2f}s"
        if st is None:
            cells = "".join(f'<text class="cycle c{k}" x="{cols[2]}" y="{y}" font-size="10.5" fill="{c}">{label}</text>'
                            for k, (label, c) in enumerate((("ContainerCreating", t["amber"]), ("Running", t["green"]), ("CrashLoopBackOff", t["red"]))))
        else:
            cells = f'<text x="{cols[2]}" y="{y}" font-size="10.5" fill="{t["green"]}">{st}</text>'
        out.append(f'<g class="rise mono" style="{d}">'
                   f'<text x="{cols[0]}" y="{y}" font-size="10.5" fill="{t["fg"]}">{name}</text>'
                   f'<text x="{cols[1]}" y="{y}" font-size="10.5" fill="{t["muted"]}">{ready}</text>{cells}'
                   f'<text x="{cols[3]}" y="{y}" text-anchor="end" font-size="10.5" fill="{t["muted"]}">{restarts}</text></g>')
    return "\n  ".join(out), py + ph, ""


def offcall(t):
    p0, p1, p2, p3 = (320, 30), (450, -6), (720, -6), (850, 30)
    arc = f"M{p0[0]} {p0[1]} C {p1[0]} {p1[1]}, {p2[0]} {p2[1]}, {p3[0]} {p3[1]}"
    out = [mono(40, 16, "$ systemctl status life --off-call", t, 11.5)]
    rnd = random.Random(5)
    for _ in range(18):
        out.append(f'<circle class="twinkle" style="animation-delay:{rnd.uniform(0, 6):.1f}s;animation-duration:{rnd.uniform(3, 6):.1f}s" '
                   f'cx="{rnd.uniform(300, 870):.0f}" cy="{rnd.uniform(0, 36):.0f}" r="{rnd.uniform(.7, 1.3):.1f}" fill="{t["muted"]}"/>')
    out.append(f'<path d="{arc}" fill="none" stroke="{t["border"]}" stroke-width="1.4" stroke-dasharray="2 6" stroke-linecap="round"/>')
    for i in range(10):
        u = (i + .5) / 10
        x, y = ((1-u)**3*a + 3*(1-u)**2*u*b + 3*(1-u)*u**2*c + u**3*d for a, b, c, d in zip(p0, p1, p2, p3))
        out.append(f'<circle class="stamp" style="animation-delay:{9*u:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{t["card"]}" stroke="{t["accent"]}" stroke-width="1.4"/>')
    out.append(f'<g><path d="M-8 0 L8 0 M2 -6 L5.5 0 L2 6 M-6 -2.6 L-4.5 0 L-6 2.6" fill="none" stroke="{t["fg"]}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
               f'<animateMotion dur="9s" repeatCount="indefinite" rotate="auto" path="{arc}"/></g>')
    tg, th, ty = 14, 62, 42
    tw = (W - 80 - tg * (len(TILES) - 1)) / len(TILES)
    for i, (ic, col, frames, label) in enumerate(TILES):
        x, c = 40 + i * (tw + tg), t[col]
        extra = ""
        if ic == "play":
            extra = (f'<rect x="{x+56:.1f}" y="{ty+th-10}" width="{tw-76:.1f}" height="2.5" rx="1.2" fill="{t["faint"]}"/>'
                     f'<rect class="progress" x="{x+56:.1f}" y="{ty+th-10}" width="{tw-76:.1f}" height="2.5" rx="1.2" fill="{c}"/>')
        out.append(f'<g class="rise" style="animation-delay:{1.8 + i*.12:.2f}s">'
                   f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="10" fill="{t["tile"]}" stroke="{t["faint"]}"/>'
                   f'{icon(ic, round(x + 30), ty + th // 2, c)}'
                   f'{countup(frames, round(x + 56), ty + 29, 1.9 + i*.12, t, 22)}'
                   f'<text x="{x+56:.1f}" y="{ty+45}" class="sans" font-size="11.5" font-weight="600" fill="{c}">{label}</text>{extra}</g>')
    return "\n  ".join(out), ty + th, ""


def ticker(t):
    """Log lines drifting right to left; positions are explicit so the loop is seamless."""
    colors = dict(OK=t["green"], INFO=t["accent"], WARN=t["amber"])
    items, x = [], 0
    for level, msg in LOGS:
        items.append((x, level, msg))
        x += (len(level) + len(msg) + 3) * 6.6 + 44
    period, h = x, 30
    out = [f'<rect x="40" y="0" width="{W-80}" height="{h}" rx="9" fill="{t["tile"]}" stroke="{t["faint"]}"/>',
           '<g mask="url(#tickerfade)"><g class="ticker">']
    for r in range(3):
        for ix, level, msg in items:
            out.append(f'<text x="{56 + ix + r*period:.1f}" y="19.5" class="mono" font-size="11" fill="{t["muted"]}">'
                       f'<tspan fill="{colors[level]}">[{level}]</tspan> {msg}</text>')
    out.append('</g></g>')
    css = (f".ticker {{ animation: ticker {period/22:.1f}s linear infinite; }}\n"
           f"      @keyframes ticker {{ to {{ transform: translateX(-{period:.1f}px); }} }}")
    return "\n  ".join(out), h, css


# ── assembly ──────────────────────────────────────────────────────────────────
def aurora(t, H):
    """Soft blurred color fields drifting slowly behind everything."""
    blobs = [(180, 80, 150, t["accent"], 0), (760, 190, 130, t["green"], 1),
             (640, H * .52, 160, t["purple"], 2), (200, H - 150, 150, t["pink"], 3)]
    return "".join(
        f'<circle class="drift a{k % 3}" style="animation-delay:-{k*5}s" cx="{x}" cy="{y:.0f}" r="{r}" fill="{c}" opacity="{t["aurora"]}" filter="url(#blur)"/>'
        for x, y, r, c, k in blobs)


def profile(theme):
    t = THEMES[theme]
    P = 300
    sections = (  # (builder, gap after, divider in the gap)
        (lambda: header(t, theme), 14, False),
        (lambda: status_and_slos(t), 18, True),
        (lambda: pipeline(t), 18, True),
        (lambda: journey(t), 18, True),
        (lambda: offcall(t), 16, False),
        (lambda: ticker(t), 18, False),
    )
    parts, css, y = [], [], 0
    for build, gap, rule in sections:
        body, h, extra = build()
        parts.append(f'<g transform="translate(0 {y})">\n  {body}\n  </g>')
        if extra:
            css.append(extra)
        y += h + gap
        if rule:
            parts.append(f'<line x1="40" x2="{W-40}" y1="{y - gap / 2}" y2="{y - gap / 2}" stroke="{t["faint"]}"/>')
    H = y
    tools = ", ".join(n for row in TOOLBOX for n in row)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}, {ROLE}. Toolbox: {tools}. All systems operational. SLOs: 97% error budget left, 90% toil automated, 100% actionable alerts, 12% coffee. Career: Staff Software Engineer at Alpaca, previously Infrastructure Engineer at Monoceros. Off-call: 10 countries, 9000+ anime episodes, world #43 dining, fashion and style.">
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
    <linearGradient id="sheen" x1="0" x2="1">
      <stop offset="0" stop-color="{t['sheen'][0]}" stop-opacity="0"/><stop offset=".5" stop-color="{t['sheen'][0]}" stop-opacity="{t['sheen'][1]}"/><stop offset="1" stop-color="{t['sheen'][0]}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="pipegrad" x1="0" x2="1">
      <stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['green']}"/>
    </linearGradient>
    <linearGradient id="edgefade" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".06" stop-color="#fff"/><stop offset=".94" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="gridfade"><rect width="{W}" height="250" fill="url(#fade)"/></mask>
    <mask id="tickerfade" maskUnits="userSpaceOnUse" x="40" y="0" width="{W-80}" height="30"><rect x="40" y="0" width="{W-80}" height="30" fill="url(#edgefade)"/></mask>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}"/>
    </pattern>
    <mask id="beat" maskUnits="userSpaceOnUse" x="0" y="184" width="{W}" height="48">
      <g class="scroll"><path d="{heartbeat(212, P)}" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/></g>
    </mask>
    <filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="60"/></filter>
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
      .float {{ animation: float 4.5s ease-in-out infinite; }}
      .breathe {{ transform-box: fill-box; transform-origin: center; animation: breathe 4s ease-in-out infinite; }}
      .shimmer {{ animation: shimmer 7s ease-in-out infinite 2.5s; }}
      .twinkle {{ opacity: .1; animation: twinkle 4s ease-in-out infinite; }}
      .drift {{ animation: drift0 22s ease-in-out infinite alternate; }}
      .drift.a1 {{ animation-name: drift1; animation-duration: 26s; }}
      .drift.a2 {{ animation-name: drift2; animation-duration: 30s; }}
      .cycle {{ opacity: 0; animation: cycle 7.5s steps(1) infinite 3s; }}
      .cycle.c1 {{ animation-name: cycle1; }} .cycle.c2 {{ animation-name: cycle2; }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes pop {{ from {{ opacity: 0; transform: scale(.6); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes ping {{ 0% {{ transform: scale(1); opacity: .6; }} 100% {{ transform: scale(3.2); opacity: 0; }} }}
      @keyframes in {{ to {{ opacity: .9; }} }}
      @keyframes scroll {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{P}px); }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes stamp {{ 0%, 4% {{ fill: {t['card']}; }} 8%, 100% {{ fill: {t['accent']}; }} }}
      @keyframes load {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
      @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
      @keyframes flow {{ to {{ stroke-dashoffset: -14; }} }}
      @keyframes float {{ 50% {{ transform: translateY(-3px); }} }}
      @keyframes breathe {{ 50% {{ transform: scale(1.25); }} }}
      @keyframes twinkle {{ 50% {{ opacity: .7; }} }}
      @keyframes drift0 {{ to {{ transform: translate(120px, 40px); }} }}
      @keyframes drift1 {{ to {{ transform: translate(-140px, 60px); }} }}
      @keyframes drift2 {{ to {{ transform: translate(80px, -70px); }} }}
      @keyframes cycle {{ 0% {{ opacity: 1; }} 20%, 100% {{ opacity: 0; }} }}
      @keyframes cycle1 {{ 0% {{ opacity: 0; }} 20% {{ opacity: 1; }} 33%, 100% {{ opacity: 0; }} }}
      @keyframes cycle2 {{ 0%, 33% {{ opacity: 0; }} 34%, 100% {{ opacity: 1; }} }}
{chr(10).join("      " + c for c in css)}
      @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .rise, .pop, .bar, .cycle.c2 {{ opacity: 1 !important; }} }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{t['card']}" stroke="{t['border']}"/>
  <g clip-path="url(#clip)">{aurora(t, H)}<rect width="{W}" height="250" fill="url(#grid)" mask="url(#gridfade)"/></g>
  {chr(10).join(parts)}
</svg>
'''


for theme in THEMES:
    _uid = 0
    with open(os.path.join(OUT, f"profile-{theme}.svg"), "w") as f:
        f.write(profile(theme))
print("ok")

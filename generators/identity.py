#!/usr/bin/env python3
"""
identity.py → assets/identity.svg
Section 01 : terminal animé (whoami, mission, parcours…) + panneau « NOW.RUNNING ».

    python generators/identity.py
"""
from _common import ACC, BASE_CSS, P, save

# ── Contenu éditable ──────────────────────────────────────────────────────
PROMPT = "devops@sidy: ~"

# Terminal : ("cmd", "commande") ou ("out", "texte"). Balises <hl>…</hl> = surligné, <dim>…</dim> = discret.
TERMINAL = [
    ("cmd", "whoami"),
    ("out", "sidy-mohamed <dim>—</dim> <hl>développeur full-stack</hl>"),
    ("gap", None),
    ("cmd", "cat mission.txt"),
    ("out", "Transformer des idées en solutions qui améliorent"),
    ("out", "la vie des gens."),
    ("gap", None),
    ("cmd", "ls ./parcours"),
    ("out", "<hl>genie-logiciel/</hl><dim> (diplômé)</dim>  <hl>professeur/</hl>  <hl>dev-fullstack/</hl>"),
    ("gap", None),
    ("cmd", "echo $BASE"),
    ("out", "Dakar, Sénégal <dim>· UTC+0</dim>"),
]

# Panneau de droite : (étiquette, titre, sous-titre ou None). La ligne SEEK s'affiche en vert.
NOW_RUNNING = [
    ("BUILD", "CETUD Mobilités", "backend Spring Boot · mobilité urbaine"),
    ("SHIP", "jwt-toolkit", "dépendance publiée sur Maven & GitHub"),
    ("LEARN", "Architecture & Design", "architecture · design patterns · CI/CD"),
    ("SEEK", "Freelance & collaborations", None),
]

ARIA = ("whoami : Sidy Mohamed, développeur full-stack diplômé en Génie Logiciel, basé à Dakar. "
        "Actuellement sur CETUD Mobilités et jwt-toolkit.")


def _markup(s):
    s = s.replace("&", "&amp;")
    return (s.replace("<hl>", f'<tspan fill="{P["deep"]}">').replace("</hl>", "</tspan>")
             .replace("<dim>", f'<tspan fill="{P["faint"]}">').replace("</dim>", "</tspan>"))


def build():
    lines, y, delay = [], 84, .2
    for i, (kind, s) in enumerate(TERMINAL):
        if kind == "gap":
            y += 14
            continue
        if kind == "cmd":
            if i:
                delay += .4
            lines.append(f'<text x="28" y="{y}" class="ln" style="animation-delay:{delay:.1f}s"><tspan fill="{P["a1"]}">❯</tspan><tspan fill="{P["ink"]}"> {_markup(s)}</tspan></text>')
            y += 26
            delay += .4
        else:
            lines.append(f'<text x="46" y="{y}" class="ln" fill="{P["text"]}" style="animation-delay:{delay:.1f}s">{_markup(s)}</text>')
            y += 22
            delay += .1
    cursor_y, cursor_t = y - 6, delay + .3

    rows = []
    for i, (lab, val, sub) in enumerate(NOW_RUNNING):
        ry = 80 + i * 80
        col = P["ok"] if lab == "SEEK" else P["ink"]
        r = (f'<g class="ln" style="animation-delay:{.5 + i * .4:.1f}s"><text x="808" y="{ry}" class="lab">▸ {lab}</text>'
             f'<text x="808" y="{ry + 22}" class="val" style="fill:{col}">{_markup(val)}</text>')
        if sub:
            r += (f'<text x="808" y="{ry + 40}" class="sub">{_markup(sub)}</text>'
                  f'<rect x="1080" y="{ry - 6}" width="96" height="4" rx="2" fill="{P["a1"]}" fill-opacity=".15"/>'
                  f'<rect x="1080" y="{ry - 6}" width="96" height="4" rx="2" fill="url(#acc)" class="bar" style="animation-delay:{i * .6:.1f}s"/>')
        rows.append(r + "</g>")

    nl = "\n    "
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-label="{ARIA}">
  <defs>{ACC}
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{P["a1"]}" fill-opacity=".18"/></pattern>
    <style>
      {BASE_CSS}
      .ln{{opacity:0;animation:in .35s ease-out forwards}}
      @keyframes in{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
      .blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}
      .lab{{font-size:11px;letter-spacing:2.5px;fill:{P["a1"]};font-weight:700}}
      .val{{font-size:15px;fill:{P["ink"]};font-weight:700}}
      .sub{{font-size:12px;fill:{P["muted"]}}}
      .bar{{transform-box:fill-box;transform-origin:left;animation:bar 2.4s ease-in-out infinite alternate}}
      @keyframes bar{{from{{transform:scaleX(.25)}}to{{transform:scaleX(1)}}}}
    </style>
  </defs>
  <!-- terminal -->
  <rect x=".75" y=".75" width="758.5" height="358.5" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="1.5"/>
  <rect x="2" y="2" width="756" height="356" rx="13" fill="url(#dots)"/>
  <path d="M1 44H759" stroke="{P["line"]}"/>
  <circle cx="26" cy="22" r="6" fill="#ff5f57"/><circle cx="46" cy="22" r="6" fill="#febc2e"/><circle cx="66" cy="22" r="6" fill="#28c840"/>
  <text x="380" y="27" text-anchor="middle" class="m" font-size="13" fill="{P["muted"]}">{PROMPT}</text>
  <g class="m" font-size="15">
    {nl.join(lines)}
  </g>
  <rect x="28" y="{cursor_y}" width="9" height="16" fill="{P["a1"]}" class="blink" opacity="0"><set attributeName="opacity" to="1" begin="{cursor_t:.1f}s"/></rect>

  <!-- now running -->
  <rect x="784.75" y=".75" width="414.5" height="358.5" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="1.5"/>
  <text x="808" y="28" class="m" font-size="12" letter-spacing="2.5" fill="{P["muted"]}">NOW.RUNNING</text>
  <circle cx="1172" cy="24" r="4" fill="{P["ok"]}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>
  <path d="M785 44H1199" stroke="{P["line"]}"/>
  <g class="m">
    {nl.join(rows)}
  </g>
</svg>
'''


def main():
    save("identity.svg", build())


if __name__ == "__main__":
    main()

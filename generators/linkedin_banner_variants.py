#!/usr/bin/env python3
"""
linkedin_banner_variants.py → exports/linkedin-banner-{sobre,dakar,code}.svg/.png (1584×396)
Trois alternatives plus « humaines » à la bannière LinkedIn : pas de halo, pas de dégradé sur le texte,
pas de grille de points. Même contenu, trois partis pris visuels.

    python generators/linkedin_banner_variants.py            # les 3
    python generators/linkedin_banner_variants.py dakar      # une seule

    sobre  → typographique, fond uni, une seule couleur d'accent en aplat
    dakar  → le tracé de la presqu'île du Cap-Vert, avec Dakar et Gorée
    code   → une fenêtre d'éditeur avec un vrai extrait de code Spring
"""
import base64
import sys

from _common import DATA, ROOT, esc
from linkedin_banner import H, OUT, ROLE, SANS, STACK, TAGLINE, W, X0, render_png

# ── Palette neutre (moins « néon » que le README) ─────────────────────────
C = dict(bg="#0c1015", ink="#f1f5f9", text="#aab6c4", muted="#7d8a9a", faint="#3b4654",
         accent="#2dd4bf", line="#1c2530", panel="#10161d")
STACK_LINE = "Java / Spring Boot  ·  Angular"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,monospace"


def fonts():
    css = ""
    for fam, name, weight in [("Inter", "inter", 400), ("Inter", "inter", 600), ("Inter", "inter", 800),
                              ("JetBrains Mono", "jetbrains-mono", 400), ("JetBrains Mono", "jetbrains-mono", 600)]:
        f = DATA / "fonts" / f"{name}-latin-{weight}-normal.woff2"
        if f.exists():
            css += (f"@font-face{{font-family:'{fam}';font-weight:{weight};"
                    f"src:url(data:font/woff2;base64,{base64.b64encode(f.read_bytes()).decode()}) format('woff2')}}")
    return css


def shell(body, extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{extra_defs}<style>{fonts()}.s{{font-family:{SANS}}}.c{{font-family:{MONO}}}</style></defs>
  <rect width="{W}" height="{H}" fill="{C["bg"]}"/>
{body}
  <text x="{W - 48}" y="372" text-anchor="end" class="s" font-size="13" font-weight="600" letter-spacing="1.2" fill="{C["muted"]}">Dakar, Sénégal  ·  github.com/sidymohamed12</text>
</svg>
'''


def text_block(y0=150, tag_size=18, max_stack=None):
    """Poste, stack principale, accroche, puis la stack en texte (sans pastilles)."""
    t1, t2 = TAGLINE
    items = STACK[:max_stack] if max_stack else STACK
    stack = f' <tspan fill="{C["accent"]}">/</tspan> '.join(esc(s.upper()) for s in items)
    return f'''  <g class="s">
    <rect x="{X0}" y="{y0 - 64}" width="28" height="3" fill="{C["accent"]}"/>
    <text x="{X0}" y="{y0}" font-size="54" font-weight="800" letter-spacing="-1.4" fill="{C["ink"]}">{esc(ROLE)}</text>
    <text x="{X0}" y="{y0 + 48}" font-size="30" font-weight="600" letter-spacing="-.4" fill="{C["accent"]}">{esc(STACK_LINE)}</text>
    <text x="{X0}" y="{y0 + 90}" font-size="{tag_size}" fill="{C["text"]}">{esc(t1)} : <tspan fill="{C["ink"]}" font-weight="600">{esc(t2)}</tspan></text>
    <text x="{X0}" y="{y0 + 146}" font-size="12.5" font-weight="600" letter-spacing="2.4" fill="{C["muted"]}">{stack}</text>
  </g>'''


# ── 1. Sobre ──────────────────────────────────────────────────────────────
def sobre():
    body = text_block()
    # un seul détail graphique : une règle fine qui court jusqu'au bord droit
    body += f'\n  <path d="M{X0} 318H{W - 48}" stroke="{C["line"]}"/>'
    return shell(body)


# ── 2. Dakar ──────────────────────────────────────────────────────────────
# côte de la presqu'île du Cap-Vert (lon, lat), tracé simplifié de Rufisque à Kayar
COAST = [(-17.10, 14.712), (-17.20, 14.722), (-17.28, 14.731), (-17.35, 14.726), (-17.40, 14.706), (-17.42, 14.686),
         (-17.43, 14.666), (-17.445, 14.655), (-17.46, 14.665), (-17.47, 14.681), (-17.49, 14.700), (-17.505, 14.715),
         (-17.52, 14.731), (-17.535, 14.745), (-17.52, 14.755), (-17.50, 14.760), (-17.47, 14.765), (-17.43, 14.775),
         (-17.38, 14.790), (-17.32, 14.810), (-17.25, 14.840), (-17.18, 14.880), (-17.12, 14.920)]
PLACES = [("DAKAR", -17.44, 14.678, "main"), ("Gorée", -17.398, 14.667, "island"), ("Almadies", -17.535, 14.745, "small")]
MAP_X, MAP_Y, K_LON, K_LAT = 1190, 88, 1000, 1034


def proj(lon, lat):
    return MAP_X + (lon + 17.56) * K_LON, MAP_Y + (14.84 - lat) * K_LAT


def smooth(points):
    """Catmull-Rom → courbes de Bézier, pour un tracé organique."""
    pts = [proj(*p) for p in points]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


def dakar():
    d = smooth(COAST)
    cx, cy = proj(-17.36, 14.76)  # centre de la presqu'île, pour les lignes de fond marin
    x_end, _ = proj(*COAST[-1])
    x_start, y_start = proj(*COAST[0])
    land = f'{d} L{W + 40} -40 L{W + 40} {y_start:.1f} Z'   # la terre, fermée hors cadre
    echoes = "".join(
        f'<path d="{d}" fill="none" stroke="{C["accent"]}" stroke-opacity="{op}" '
        f'transform="translate({cx:.1f} {cy:.1f}) scale({sc}) translate({-cx:.1f} {-cy:.1f})" vector-effect="non-scaling-stroke"/>'
        for sc, op in [(1.08, .32), (1.17, .18), (1.27, .09)])
    marks = ""
    for name, lon, lat, kind in PLACES:
        x, y = proj(lon, lat)
        if kind == "main":
            marks += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="none" stroke="{C["accent"]}" stroke-opacity=".5"/>'
                      f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{C["accent"]}"/>'
                      f'<path d="M{x + 12:.1f} {y:.1f}H{x + 44:.1f}" stroke="{C["accent"]}" stroke-opacity=".6"/>'
                      f'<text x="{x + 50:.1f}" y="{y + 5:.1f}" class="s" font-size="14" font-weight="800" letter-spacing="3" fill="{C["ink"]}">{name}</text>')
        elif kind == "island":
            marks += (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="3.2" ry="2" fill="{C["text"]}"/>'
                      f'<text x="{x + 8:.1f}" y="{y + 16:.1f}" class="s" font-size="11" fill="{C["muted"]}">{name}</text>')
        else:
            marks += f'<text x="{x - 8:.1f}" y="{y - 10:.1f}" text-anchor="end" class="s" font-size="11" fill="{C["muted"]}">{name}</text>'
    body = text_block() + f'''
  <g>
    <path d="{land}" fill="{C["panel"]}"/>
    {echoes}
    <path d="{d}" fill="none" stroke="{C["ink"]}" stroke-opacity=".85" stroke-width="1.6" stroke-linecap="round"/>
    {marks}
  </g>'''
    return shell(body)


# ── 3. Code ───────────────────────────────────────────────────────────────
KW, TY, ST, AN, FN, PL = "#7dd3fc", "#5eead4", "#fcd34d", "#94a3b8", "#e2e8f0", "#aab6c4"
CODE = [
    [("@Service", AN)],
    [("public class ", KW), ("AuthService", TY), (" {", PL)],
    [],
    [("  private final ", KW), ("JwtTokenService", TY), (" jwt;", PL)],
    [],
    [("  public ", KW), ("String", TY), (" login", FN), ("(", PL), ("User", TY), (" user) {", PL)],
    [("    return ", KW), ("jwt.", PL), ("generate", FN), ("(", PL), ("JwtTokenSpec", TY), (".", PL), ("builder", FN), ("()", PL)],
    [("        .", PL), ("subject", FN), ("(user.", PL), ("getEmail", FN), ("())", PL)],
    [("        .", PL), ("claim", FN), ("(", PL), ('"roles"', ST), (", user.", PL), ("getRoles", FN), ("())", PL)],
    [("        .", PL), ("ttl", FN), ("(", PL), ("Duration", TY), (".", PL), ("ofMinutes", FN), ("(", PL), ("15", ST), ("))", PL)],
    [("        .", PL), ("build", FN), ("());", PL)],
    [("  }", PL)],
    [("}", PL)],
]
ED_X, ED_Y, ED_W, ED_H = 1090, 40, 446, 300


def code():
    lines = ""
    for i, toks in enumerate(CODE):
        y = ED_Y + 64 + i * 18.5
        lines += f'<text x="{ED_X + 30}" y="{y:.1f}" text-anchor="end" class="c" font-size="11.5" fill="{C["faint"]}">{i + 1}</text>'
        if toks:
            spans = "".join(f'<tspan fill="{col}">{esc(t)}</tspan>' for t, col in toks)
            lines += f'<text x="{ED_X + 44}" y="{y:.1f}" class="c" font-size="13" xml:space="preserve">{spans}</text>'
    editor = f'''
  <g>
    <rect x="{ED_X}" y="{ED_Y}" width="{ED_W}" height="{ED_H}" rx="10" fill="{C["panel"]}" stroke="{C["line"]}"/>
    <path d="M{ED_X} {ED_Y + 36}H{ED_X + ED_W}" stroke="{C["line"]}"/>
    <rect x="{ED_X + 1}" y="{ED_Y + 1}" width="158" height="35" rx="9" fill="{C["bg"]}"/>
    <rect x="{ED_X + 1}" y="{ED_Y + 34}" width="158" height="2" fill="{C["accent"]}"/>
    <circle cx="{ED_X + 18}" cy="{ED_Y + 18}" r="4" fill="#f59e0b"/>
    <text x="{ED_X + 30}" y="{ED_Y + 22}" class="c" font-size="12" fill="{C["ink"]}">AuthService.java</text>
    {lines}
  </g>'''
    return shell(text_block(tag_size=15.5, max_stack=6) + editor)


VARIANTS = {"sobre": sobre, "dakar": dakar, "code": code}


def main(argv=None):
    wanted = [a for a in (argv if argv is not None else sys.argv[1:]) if a in VARIANTS] or list(VARIANTS)
    OUT.mkdir(exist_ok=True)
    for name in wanted:
        svg = OUT / f"linkedin-banner-{name}.svg"
        svg.write_text(VARIANTS[name](), encoding="utf-8")
        print(f"✔ {svg.relative_to(ROOT)}")
        render_png(svg, OUT / f"linkedin-banner-{name}.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
linkedin_banner.py → exports/linkedin-banner.svg + exports/linkedin-banner.png (1584×396, format LinkedIn)
Bannière de profil LinkedIn : poste, stack, et les autres technos en orbite. Couleurs harmonisées (une seule couleur d'accent).

    python generators/linkedin_banner.py                 # SVG + PNG + JPG en 1584×396
    python generators/linkedin_banner.py -f png          # seulement le PNG
    python generators/linkedin_banner.py -f jpg -q 95    # seulement le JPG, qualité 95
    python generators/linkedin_banner.py -s 2            # en 3168×792 (plus net, fichiers « @2x »)

Les exports PNG/JPG passent par Chromium via Playwright :
    pip install playwright && playwright install chromium

Zone réservée : LinkedIn pose ta photo de profil en bas à gauche (≈ x < 420, y > 200) → aucun texte là.
Police : Inter, intégrée depuis data/fonts (rendu identique sur toutes les machines).
"""
import argparse
import base64
import math
import pathlib

from _common import DATA, P, ROOT, esc, icon

# ── Contenu éditable ──────────────────────────────────────────────────────
ROLE = "Développeur Full-Stack"
STACK_LINE = ("Java / Spring Boot", "Angular")          # affichés « A × B » en couleur d'accent
TAGLINE = ("Du cahier des charges à la mise en production", "backend, frontend, DevOps.")
# autres technos éparpillées sur les anneaux (celles qui ne sont pas dans STACK) : (techno, rayon, angle en degrés)
ORBIT = [
    ("C#", 90, 120), (".NET / ASP.NET", 90, 60), ("Keycloak", 90, 180), ("Grafana", 90, 250),
    ("GitHub", 150, 90), ("Jenkins", 150, 140), ("Swagger / OpenAPI", 150, 170), ("SonarQube", 150, 205), ("Tailwind CSS", 150, 232),
    ("VS Code", 150, 115),
]
STACK = ["Java", "Spring Boot", "Angular", "TypeScript", "PostgreSQL", "Redis", "Docker", "Git"]
# coordonnées en bas à droite : (icône, texte). Icônes : "mail", "phone", "pin", "github"
CONTACT = [("mail", "mohamedsaizonou86@gmail.com"), ("phone", "+221 76 182 36 98"), ("pin", "Dakar, Sénégal")]

# Palette harmonisée : fond anthracite neutre, UNE couleur d'accent en aplat, icônes aux couleurs des marques.
C = dict(bg="#0c1015", ink="#f1f5f9", text="#aab6c4", muted="#7d8a9a", faint="#3b4654",
         accent="#2dd4bf", ring="#1f2a36", node="#111820", nodeline="#243140", icon="#b9c4d0")

# couleurs forcées pour certaines icônes (sinon couleur de la marque)
ICON_COLORS = {"Jenkins": C["ink"]}

W, H = 1584, 396
X0 = 470          # début de la zone de texte (à droite de la photo LinkedIn)
OUT = ROOT / "exports"
SANS = "'Inter','Segoe UI',Helvetica,Arial,sans-serif"


def font_faces():
    css = ""
    for weight in (400, 600, 800):
        f = DATA / "fonts" / f"inter-latin-{weight}-normal.woff2"
        if f.exists():
            b64 = base64.b64encode(f.read_bytes()).decode()
            css += f"@font-face{{font-family:'Inter';font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    return css


def orbit_nodes():
    out = ""
    for name, r, deg in ORBIT:
        x, y = r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))
        out += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="21" fill="{C["node"]}" stroke="{C["nodeline"]}" stroke-width="1.5"/>'
                + icon(name, round(x, 1), round(y, 1), 19, ICON_COLORS.get(name)))
    return out


GLYPHS = {  # pictos 24×24 en trait
    "mail": "M3 6h18v12H3zM3 6l9 7 9-7",
    "phone": "M6.6 3h3l1.5 4.5-2.1 1.3a11 11 0 0 0 5.2 5.2l1.3-2.1L20 13.4v3A2.6 2.6 0 0 1 17.4 19 14.4 14.4 0 0 1 4 5.6 2.6 2.6 0 0 1 6.6 3z",
    "pin": "M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21zM12 7.3a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z",
}


# largeurs approximatives des caractères d'Inter SemiBold (en em), pour aligner sans dépendance
_NARROW, _WIDE = set(" .,:;'!|il1ftjrI"), set("mwMW@")


def text_width(t, size):
    em = 0
    for ch in t:
        em += .28 if ch in _NARROW else .86 if ch in _WIDE else .66 if ch.isupper() else .6 if ch.isdigit() or ch == "+" else .55
    return em * size


def contact_row(y=372, right=None, size=14):
    """Coordonnées alignées à droite, chacune précédée de son picto."""
    right = W - 48 if right is None else right
    items, gap = [], 34
    widths = [22 + text_width(t, size) for _, t in CONTACT]
    x = right - sum(widths) - gap * (len(CONTACT) - 1)
    for (g, t), wdt in zip(CONTACT, widths):
        items.append(f'<g transform="translate({x:.0f} {y - 13}) scale(.66)"><path d="{GLYPHS[g]}" fill="none" stroke="{C["accent"]}" '
                     f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/></g>'
                     f'<text x="{x + 22:.0f}" y="{y}" font-size="{size}" font-weight="600" fill="{C["text"]}">{esc(t)}</text>')
        x += wdt + gap
    return "".join(items)


def build():
    chips, x = [], X0
    for name in STACK:
        cw = int(44 + len(name) * 7.3)
        chips.append(f'<rect x="{x}" y="270" width="{cw}" height="36" rx="8" fill="{C["node"]}" stroke="{C["nodeline"]}"/>'
                     + icon(name, x + 19, 288, 16, ICON_COLORS.get(name)) +
                     f'<text x="{x + 34}" y="293" class="s" font-size="14" font-weight="600" fill="{C["ink"]}">{esc(name)}</text>')
        x += cw + 10
    a, b = STACK_LINE
    t1, t2 = TAGLINE
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs><style>{font_faces()}.s{{font-family:{SANS}}}</style></defs>

  <rect width="{W}" height="{H}" fill="{C["bg"]}"/>

  <!-- anneaux à droite -->
  <g fill="none" transform="translate(1500 150)">
    <circle r="210" stroke="{C["ring"]}"/>
    <circle r="150" stroke="{C["ring"]}" stroke-width="1.2"/>
    <circle r="90" stroke="{C["ring"]}" stroke-width="1.2"/>
    <path d="M-150 0A150 150 0 0 1 106 -106" stroke="{C["accent"]}" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>
    <circle cx="106" cy="-106" r="3.5" fill="{C["accent"]}"/>
    <circle r="44" fill="{C["node"]}" stroke="{C["accent"]}" stroke-width="2"/>
    <g stroke="{C["accent"]}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">
      <path d="M-11 -11L-23 0L-11 11"/><path d="M11 -11L23 0L11 11"/><path d="M5 -15L-5 15"/>
    </g>
    {orbit_nodes()}
  </g>

  <g class="s">
    <rect x="{X0}" y="82" width="28" height="3" fill="{C["accent"]}"/>
    <text x="{X0}" y="142" font-size="50" font-weight="800" letter-spacing="-1" fill="{C["ink"]}">{esc(ROLE)}</text>
    <text x="{X0}" y="192" font-size="32" font-weight="700" letter-spacing="-.5" fill="{C["accent"]}">{esc(a)}  <tspan fill="{C["faint"]}" font-weight="600">×</tspan>  {esc(b)}</text>
    <text x="{X0}" y="234" font-size="18" fill="{C["text"]}">{esc(t1)} : <tspan fill="{C["ink"]}" font-weight="600">{esc(t2)}</tspan></text>
    {"".join(chips)}
    <path d="M{X0} 340H{W - 48}" stroke="{C["ring"]}"/>
    {contact_row()}
  </g>
</svg>
'''


def render(svg_path, out_path, fmt="png", scale=1, quality=92):
    """Rastérise le SVG en PNG ou JPG avec Chromium (Playwright). scale=2 → 3168×792, plus net sur écrans Retina."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ℹ Playwright absent : export PNG/JPG impossible (pip install playwright && playwright install chromium).")
        return
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
        pg.goto(pathlib.Path(svg_path).resolve().as_uri())
        pg.wait_for_timeout(300)
        opts = {"path": str(out_path), "clip": {"x": 0, "y": 0, "width": W, "height": H}}
        if fmt == "jpg":
            opts.update(type="jpeg", quality=quality)
        pg.screenshot(**opts)
        b.close()
    print(f"✔ {out_path.relative_to(ROOT)}  ({W * scale}×{H * scale}, {out_path.stat().st_size // 1024} Ko)")


def render_png(svg_path, png_path):  # compatibilité avec les anciens scripts
    render(svg_path, png_path, "png")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bannière LinkedIn 1584×396 → SVG + PNG/JPG")
    ap.add_argument("--format", "-f", choices=["png", "jpg", "svg", "all"], default="all",
                    help="format d'export (défaut : all = svg + png + jpg)")
    ap.add_argument("--scale", "-s", type=int, choices=[1, 2, 3], default=1,
                    help="résolution : 1 = 1584×396 (format LinkedIn), 2 = 3168×792 (plus net)")
    ap.add_argument("--quality", "-q", type=int, default=92, help="qualité JPG, 1–100 (défaut 92)")
    args = ap.parse_args(argv)

    OUT.mkdir(exist_ok=True)
    svg = OUT / "linkedin-banner.svg"
    svg.write_text(build(), encoding="utf-8")
    print(f"✔ {svg.relative_to(ROOT)}")
    suffix = f"@{args.scale}x" if args.scale > 1 else ""
    for fmt in (["png", "jpg"] if args.format == "all" else [args.format] if args.format != "svg" else []):
        render(svg, OUT / f"linkedin-banner{suffix}.{fmt}", fmt, args.scale, args.quality)


if __name__ == "__main__":
    main()

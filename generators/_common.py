"""
Module commun à tous les générateurs : palette, polices, chemins et petits helpers SVG.

Changer une couleur ici la change partout (sauf telemetry.py, qui garde sa propre copie
de la palette pour rester autonome dans la GitHub Action).
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = pathlib.Path(__file__).resolve().parent / "data"

# ── Palette (dark · bleu / cyan / turquoise) ──────────────────────────────
P = dict(
    bg="#070b12",        # fond de la bannière
    panel="#0b111b",     # fond des cartes
    line="#1d2b3c",      # bordures
    ink="#e8f1f8",       # texte principal
    text="#b4c4d4",      # texte courant
    muted="#7c8ea3",     # texte secondaire
    faint="#4d6075",     # séparateurs, texte très discret
    a1="#2dd4bf",        # turquoise
    a2="#22d3ee",        # cyan
    a3="#60a5fa",        # bleu
    deep="#5eead4",      # turquoise clair (mises en valeur)
    ok="#34d399",        # vert « en ligne »
    chip="#0e1723",      # fond des pastilles
    chipline="#1f2f42",  # bordure des pastilles
)

FONT = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
BASE_CSS = f".m{{font-family:{FONT}}}"
ACC = (f'<linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="{P["a1"]}"/>'
       f'<stop offset=".5" stop-color="{P["a2"]}"/><stop offset="1" stop-color="{P["a3"]}"/></linearGradient>')


def esc(s):
    """Échappe un texte pour l'insérer dans du SVG."""
    return html.escape(s, quote=True)


def save(name, svg):
    """Écrit assets/<name> et affiche le chemin."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / name
    path.write_text(svg, encoding="utf-8")
    print(f"✔ {path.relative_to(ROOT)}")
    return path


def grid_pattern(pid="g", size=24, op=".07"):
    return (f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
            f'<path d="M{size} 0H0V{size}" fill="none" stroke="{P["a1"]}" stroke-opacity="{op}"/></pattern>')


def frame(w, h, r=16):
    """Bordure extérieure d'une carte."""
    return (f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{r}" fill="none" '
            f'stroke="{P["line"]}" stroke-width="1.5"/>')


def chips_row(labels, x, y, size=12, pad=24, gap=10, cw_char=7.6):
    """Rangée de pastilles de texte (tags des cartes projets)."""
    s = ""
    for c in labels:
        cw = int(len(c) * cw_char + pad)
        s += (f'<rect x="{x}" y="{y}" width="{cw}" height="28" rx="7" fill="{P["a1"]}" fill-opacity=".08" '
              f'stroke="{P["a1"]}" stroke-opacity=".45"/><text x="{x + cw / 2}" y="{y + 18.5}" '
              f'text-anchor="middle" font-size="{size}" fill="{P["deep"]}">{esc(c)}</text>')
        x += cw + gap
    return s


# ── Icônes de marques (extraites de simple-icons, voir data/icons.json) ────
ICONS = json.loads((DATA / "icons.json").read_text(encoding="utf-8"))


def icon(name, cx, cy, size=18, color=None):
    """Icône centrée en (cx, cy). Clé = nom affiché dans data/icons.json. `color` remplace la couleur de marque."""
    ic = dict(ICONS[name], **({"h": color} if color else {}))
    if "mono" in ic:  # pas d'icône officielle → monogramme
        return (f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" class="m" font-size="11" '
                f'font-weight="800" fill="{ic["h"]}">{esc(ic["mono"])}</text>')
    vb, fr = ic.get("vb", 24), ic.get("fr")  # certaines icônes (devicon) sont dessinées en 128×128
    return (f'<path transform="translate({cx - size / 2} {cy - size / 2}) scale({size / vb:.4f})" '
            f'd="{ic["p"]}" fill="{ic["h"]}"' + (f' fill-rule="{fr}"' if fr else "") + '/>')


def small_card(num, title, lines, chips, motif, aria, cta):
    """Carte projet 590×236 (missions 02 et 03). `motif` = SVG de l'illustration de droite."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="590" height="236" viewBox="0 0 590 236" role="img" aria-label="{esc(aria)}">
  <defs>{ACC}
    <radialGradient id="glow"><stop offset="0" stop-color="{P["a2"]}" stop-opacity=".2"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></radialGradient>
    {grid_pattern("g", 20)}
    <clipPath id="c"><rect width="590" height="236" rx="16"/></clipPath>
    <style>{BASE_CSS}
      .sh{{animation:sh 2.2s ease-in-out infinite}}@keyframes sh{{0%,100%{{opacity:.3}}50%{{opacity:.8}}}}
      .rv{{opacity:0;animation:rv .5s ease-out forwards}}@keyframes rv{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
      .pop{{opacity:0;animation:pop .5s cubic-bezier(.3,1.6,.5,1) forwards}}@keyframes pop{{from{{opacity:0;transform:scale(.6)}}to{{opacity:1;transform:none}}}}
    </style>
  </defs>
  <g clip-path="url(#c)">
    <rect width="590" height="236" fill="{P["panel"]}"/>
    <rect x="360" width="230" height="236" fill="url(#g)"/>
    <circle cx="480" cy="110" r="140" fill="url(#glow)"/>
{motif}
    <g class="m">
      <text x="32" y="44" font-size="11.5" letter-spacing="3" fill="{P["a1"]}" font-weight="700">MISSION {num}</text>
      <text x="32" y="86" font-size="28" font-weight="800" fill="{P["ink"]}">{esc(title)}</text>
      {"".join(f'<text x="32" y="{118 + k * 21}" font-size="13.5" fill="{P["text"]}">{esc(l)}</text>' for k, l in enumerate(lines))}
      <g>{chips_row(chips, 32, 180, size=11.5, pad=22, gap=8, cw_char=7.2)}</g>
      <text x="558" y="214" text-anchor="end" font-size="11" letter-spacing="1.5" fill="{P["muted"]}">{esc(cta)}</text>
    </g>
  </g>
  {frame(590, 236)}
</svg>
'''

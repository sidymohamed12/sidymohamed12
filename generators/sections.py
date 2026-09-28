#!/usr/bin/env python3
"""
sections.py → assets/section-01.svg … section-05.svg
En-têtes de section numérotés (« 01 / IDENTITY // qui je suis ») avec une ligne pulsée.

    python generators/sections.py          # les 5 en-têtes
    python generators/sections.py 03       # seulement section-03.svg
"""
import sys

from _common import ACC, BASE_CSS, P, esc, save

# ── Contenu éditable : (numéro, titre, sous-titre) ────────────────────────
SECTIONS = [
    ("01", "IDENTITY", "qui je suis"),
    ("02", "SYSTEMS", "stack & outils"),
    ("03", "MISSIONS", "projets phares"),
    ("04", "TELEMETRY", "activité github"),
    ("05", "UPLINK", "me contacter"),
]


def build(n, label, sub):
    x0 = 100 + len(label) * 15  # la ligne démarre après le titre
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="72" viewBox="0 0 1200 72" role="img" aria-label="{n} {label} — {esc(sub)}">
  <defs>{ACC}
    <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{P["a1"]}" stop-opacity=".7"/><stop offset="1" stop-color="{P["a3"]}" stop-opacity="0"/></linearGradient>
    <linearGradient id="p" x1="0" x2="1"><stop offset="0" stop-color="{P["a2"]}" stop-opacity="0"/><stop offset="1" stop-color="{P["a2"]}"/></linearGradient>
    <style>{BASE_CSS}</style></defs>
  <text x="4" y="46" class="m" font-size="40" font-weight="800" fill="none" stroke="url(#acc)" stroke-width="1.3">{n}</text>
  <text x="68" y="34" class="m" font-size="18" font-weight="700" fill="{P["a1"]}" letter-spacing="4">/ <tspan fill="{P["deep"]}">{label}</tspan></text>
  <text x="88" y="56" class="m" font-size="12" fill="{P["muted"]}" letter-spacing="2">// {esc(sub)}</text>
  <rect x="{x0}" y="27" width="{1180 - x0}" height="1" fill="url(#l)"/>
  <rect x="0" y="26" width="90" height="3" rx="1.5" fill="url(#p)"><animate attributeName="x" from="{x0}" to="1200" dur="3.5s" repeatCount="indefinite"/></rect>
  <rect x="1188" y="22" width="8" height="8" fill="none" stroke="{P["a1"]}" transform="rotate(45 1192 26)"/>
</svg>
'''


def main(argv=None):
    wanted = set(argv if argv is not None else sys.argv[1:])
    for n, label, sub in SECTIONS:
        if not wanted or n in wanted:
            save(f"section-{n}.svg", build(n, label, sub))


if __name__ == "__main__":
    main()

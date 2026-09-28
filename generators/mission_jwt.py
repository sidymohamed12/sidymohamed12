#!/usr/bin/env python3
"""
mission_jwt.py → assets/mission-02.svg
Carte projet « jwt-toolkit » : un jeton JWT qui s'affiche segment par segment puis se valide.

    python generators/mission_jwt.py
"""
from _common import P, save, small_card

# ── Contenu éditable ──────────────────────────────────────────────────────
NUM = "02"
TITLE = "jwt-toolkit"
DESCRIPTION = [  # 3 lignes, ~36 caractères max chacune
    "Librairie Java open source, publiée",
    "comme dépendance sur Maven Central",
    "et GitHub Packages : JWT sur mesure.",
]
TAGS = ["Maven Central", "GitHub Packages", "Spring Boot"]
CTA = "voir le repo ↗"
ARIA = "Mission 02 — jwt-toolkit : librairie Java de JWT personnalisable, publiée sur Maven Central et GitHub Packages"
# segments du jeton affiché : (texte, couleur)
TOKEN = [("eyJhbGciOiJIUzI1", "#fb7185"), ("eyJzdWIiOiJzbXMi", P["deep"]), ("SflKxwRJSMeKKF2Q", P["a3"])]


def motif():
    seg = "".join(f'<text x="14" y="{54 + k * 18}" font-size="11" fill="{col}" class="rv" style="animation-delay:{.4 + k * .5:.1f}s">{t}</text>'
                  for k, (t, col) in enumerate(TOKEN))
    dots = "".join(f'<text x="14" y="{54 + k * 18}" dx="108" font-size="11" fill="{P["faint"]}" class="rv" style="animation-delay:{.4 + k * .5:.1f}s">.</text>'
                   for k in range(len(TOKEN) - 1))
    return f'''    <g transform="translate(392 30)" class="m">
      <rect width="172" height="140" rx="10" fill="{P["chip"]}" stroke="{P["line"]}"/>
      <text x="14" y="22" font-size="9.5" letter-spacing="2" fill="{P["muted"]}">TOKEN.JWT</text>
      <g transform="translate(142 10)"><path d="M8 2a5 5 0 0 0-4.6 7L0 12.4V16h3.6v-2h2v-2h2l1-1A5 5 0 1 0 8 2zm1.2 3.2a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4z" fill="{P["a1"]}"/></g>
      <path d="M0 32H172" stroke="{P["line"]}"/>
      {seg}
      {dots}
      <rect x="8" y="42" width="156" height="16" rx="3" fill="{P["a2"]}" opacity=".12"><animate attributeName="y" values="42;60;78;42" dur="3s" begin="2s" repeatCount="indefinite"/></rect>
      <g class="pop" style="animation-delay:2s;transform-origin:86px 118px">
        <rect x="11" y="106" width="150" height="24" rx="12" fill="{P["ok"]}" fill-opacity=".12" stroke="{P["ok"]}" stroke-opacity=".5"/>
        <text x="86" y="122" text-anchor="middle" font-size="10.5" letter-spacing="1" fill="{P["ok"]}">✔ signature valide</text>
      </g>
    </g>'''


def build():
    return small_card(NUM, TITLE, DESCRIPTION, TAGS, motif(), ARIA, CTA)


def main():
    save("mission-02.svg", build())


if __name__ == "__main__":
    main()

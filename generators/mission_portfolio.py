#!/usr/bin/env python3
"""
mission_portfolio.py → assets/mission-03.svg
Carte projet « Portfolio » : un mini navigateur avec des blocs qui scintillent et un curseur qui se promène.

    python generators/mission_portfolio.py
"""
from _common import P, save, small_card

# ── Contenu éditable ──────────────────────────────────────────────────────
NUM = "03"
TITLE = "Portfolio"
DESCRIPTION = [
    "Ma vitrine personnelle :",
    "projets, parcours et contact,",
    "réunis en un seul endroit.",
]
TAGS = ["Projets", "Parcours", "Contact"]
CTA = "visiter ↗"
ARIA = "Mission 03 — Portfolio en ligne"


def motif():
    return f'''    <g transform="translate(392 36)">
      <rect width="170" height="130" rx="8" fill="{P["chip"]}" stroke="{P["line"]}"/>
      <path d="M0 22H170" stroke="{P["line"]}"/>
      <circle cx="12" cy="11" r="3" fill="#ff5f57"/><circle cx="22" cy="11" r="3" fill="#febc2e"/><circle cx="32" cy="11" r="3" fill="#28c840"/>
      <rect x="44" y="6" width="116" height="10" rx="5" fill="{P["a1"]}" fill-opacity=".12"/>
      <rect x="14" y="34" width="70" height="10" rx="3" fill="url(#acc)"/>
      <rect x="14" y="50" width="110" height="6" rx="3" fill="{P["a2"]}" class="sh" style="animation-delay:.2s"/>
      <rect x="14" y="61" width="90" height="6" rx="3" fill="{P["a2"]}" class="sh" style="animation-delay:.35s"/>
      <rect x="14" y="78" width="44" height="38" rx="4" fill="{P["a1"]}" class="sh" style="animation-delay:.5s"/>
      <rect x="63" y="78" width="44" height="38" rx="4" fill="{P["a2"]}" class="sh" style="animation-delay:.65s"/>
      <rect x="112" y="78" width="44" height="38" rx="4" fill="{P["a3"]}" class="sh" style="animation-delay:.8s"/>
      <path d="M0 0l0 14l4 -4l3 7l2 -1l-3 -7l5 0z" fill="{P["ink"]}" stroke="{P["bg"]}" stroke-width=".8">
        <animateMotion dur="6s" repeatCount="indefinite" path="M150 110 L90 40 L130 95 L40 96 L150 110" keyTimes="0;.3;.55;.8;1" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>
      </path>
    </g>'''


def build():
    return small_card(NUM, TITLE, DESCRIPTION, TAGS, motif(), ARIA, CTA)


def main():
    save("mission-03.svg", build())


if __name__ == "__main__":
    main()

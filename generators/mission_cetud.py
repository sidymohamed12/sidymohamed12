#!/usr/bin/env python3
"""
mission_cetud.py → assets/mission-01.svg
Grande carte projet « CETUD Mobilités » avec un tracé animé app → api → ws → db.

    python generators/mission_cetud.py
"""
from _common import ACC, BASE_CSS, P, chips_row, esc, frame, grid_pattern, save

# ── Contenu éditable ──────────────────────────────────────────────────────
NUM = "01"
TITLE = "CETUD Mobilités"
DESCRIPTION = [  # 3 lignes, ~60 caractères max chacune
    "Plateforme de mobilité urbaine pour Dakar, avec le CETUD :",
    "transports publics, taxis/VTC, tourisme et JOJ Dakar 2026.",
    "Je développe le backend : API REST, temps réel, sécurité.",
]
TAGS = ["Spring Boot 3.5", "Java 21", "Hexagonale", "WebSocket", "Redis"]
# stations du tracé : (x, y, libellé, y du libellé)
STATIONS = [(660, 200, "app", 230), (810, 110, "api", 90), (960, 170, "ws", 200), (1100, 70, "db", 50)]
ROUTE = "M660 200 C 720 200, 740 110, 810 110 S 900 190, 960 170 S 1030 60, 1100 70 S 1170 140, 1180 150"
ARIA = "Mission 01 — CETUD Mobilités : plateforme de mobilité urbaine pour Dakar, backend Spring Boot"


def build():
    st = "".join(
        f'<g class="st" style="animation-delay:{.5 + k * .5}s"><circle cx="{x}" cy="{y}" r="7" fill="{P["panel"]}" stroke="{P["a2"]}" stroke-width="2.5"/>'
        f'<text x="{x}" y="{ly}" text-anchor="middle" class="m" font-size="10.5" fill="{P["muted"]}" letter-spacing="1.5">{esc(lab)}</text></g>'
        for k, (x, y, lab, ly) in enumerate(STATIONS))
    motion = ('<animateMotion dur="5s" begin="2.9s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="spline" '
              'keySplines=".45 0 .55 1"><mpath href="#r" xlink:href="#r"/></animateMotion>')
    desc = "".join(f'<text x="40" y="{138 + k * 22}" font-size="14.5" fill="{P["text"]}">{esc(l)}</text>' for k, l in enumerate(DESCRIPTION))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="262" viewBox="0 0 1200 262" role="img" aria-label="{esc(ARIA)}">
  <defs>{ACC}
    <radialGradient id="glow"><stop offset="0" stop-color="{P["a2"]}" stop-opacity=".22"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></radialGradient>
    {grid_pattern()}
    <clipPath id="c"><rect width="1200" height="262" rx="16"/></clipPath>
    <style>{BASE_CSS}
      .route{{stroke-dasharray:1400;stroke-dashoffset:1400;animation:dr 2.6s .3s ease-out forwards}}@keyframes dr{{to{{stroke-dashoffset:0}}}}
      .st{{opacity:0;animation:in .4s forwards}}@keyframes in{{to{{opacity:1}}}}
    </style>
  </defs>
  <g clip-path="url(#c)">
    <rect width="1200" height="262" fill="{P["panel"]}"/>
    <rect x="640" width="560" height="262" fill="url(#g)"/>
    <circle cx="920" cy="130" r="220" fill="url(#glow)"/>
    <path id="r" d="{ROUTE}" fill="none" stroke="{P["a1"]}" stroke-opacity=".14" stroke-width="10" stroke-linecap="round"/>
    <path d="{ROUTE}" fill="none" stroke="url(#acc)" stroke-width="2.5" stroke-linecap="round" class="route"/>
    {st}
    <circle r="14" fill="{P["a2"]}" opacity="0"><set attributeName="opacity" to=".25" begin="2.9s"/>{motion}</circle>
    <circle r="6" fill="{P["a3"]}" opacity="0"><set attributeName="opacity" to="1" begin="2.9s"/>{motion}</circle>
    <g class="m">
      <text x="40" y="48" font-size="12" letter-spacing="3" fill="{P["a1"]}" font-weight="700">MISSION {NUM}</text>
      <text x="40" y="100" font-size="40" font-weight="800" fill="{P["ink"]}" letter-spacing="1">{esc(TITLE)}</text>
      {desc}
      <g>{chips_row(TAGS, 40, 208)}</g>
    </g>
  </g>
  {frame(1200, 262)}
</svg>
'''


def main():
    save("mission-01.svg", build())


if __name__ == "__main__":
    main()

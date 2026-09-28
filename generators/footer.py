#!/usr/bin/env python3
"""
footer.py → assets/footer.svg
Pied de page : signal qui pulse + « END OF TRANSMISSION ».

    python generators/footer.py
"""
from _common import BASE_CSS, P, esc, save

# ── Contenu éditable ──────────────────────────────────────────────────────
TITLE = "END OF TRANSMISSION"
SUBTITLE = "merci pour votre visite · ⭐ si un repo vous plaît"

WAVE_A = "M0 40 H440 L460 40 L470 20 L482 62 L494 8 L506 70 L518 28 L528 40 H1200"
WAVE_B = "M0 40 H660 L680 40 L690 20 L702 62 L714 8 L726 70 L738 28 L748 40 H1200"


def build():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="130" viewBox="0 0 1200 130" role="img" aria-label="Fin de transmission — merci pour votre visite">
  <defs>
    <linearGradient id="wv" x1="0" x2="1"><stop offset="0" stop-color="{P["a1"]}" stop-opacity="0"/><stop offset=".2" stop-color="{P["a1"]}"/><stop offset=".55" stop-color="{P["a2"]}"/><stop offset=".8" stop-color="{P["a3"]}"/><stop offset="1" stop-color="{P["a3"]}" stop-opacity="0"/></linearGradient>
    <style>{BASE_CSS}.blink{{animation:bl 1.2s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}</style>
  </defs>
  <path fill="none" stroke="url(#wv)" stroke-width="2" d="{WAVE_A}">
    <animate attributeName="d" dur="2.4s" repeatCount="indefinite" values="{WAVE_A};{WAVE_B};{WAVE_A}"/>
  </path>
  <text x="600" y="100" text-anchor="middle" class="m" font-size="13" letter-spacing="4" fill="{P["a1"]}" font-weight="700">{esc(TITLE)}<tspan class="blink"> _</tspan></text>
  <text x="600" y="122" text-anchor="middle" class="m" font-size="11" letter-spacing="2" fill="{P["muted"]}">{esc(SUBTITLE)}</text>
</svg>
'''


def main():
    save("footer.svg", build())


if __name__ == "__main__":
    main()

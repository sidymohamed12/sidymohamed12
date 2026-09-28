#!/usr/bin/env python3
"""
uplinks.py → assets/uplink-portfolio.svg, uplink-linkedin.svg, uplink-email.svg, uplink-whatsapp.svg
Boutons de contact de la section 05 (un SVG par bouton, chacun cliquable dans le README).

    python generators/uplinks.py              # les 4 boutons
    python generators/uplinks.py email        # seulement uplink-email.svg
"""
import sys

from _common import BASE_CSS, P, esc, frame, save

# ── Contenu éditable : clé → (titre, sous-titre, couleur, icône 24×24, icône pleine ?) ──
BUTTONS = {
    "portfolio": ("PORTFOLIO", "sms-12-portfolio", P["a2"],
                  "M4 12a8 8 0 1 0 16 0a8 8 0 1 0 -16 0M4 12h16M12 4c3 3 3 13 0 16M12 4c-3 3 -3 13 0 16", False),
    "linkedin": ("LINKEDIN", "sidy-mohamed-saizonou", "#3b9bf0",
                 "M5 9h3v10h-3zM6.5 4.5a1.6 1.6 0 1 1 0 3.2a1.6 1.6 0 1 1 0 -3.2M10 9h3v1.5c.6-1 1.8-1.8 3.4-1.8c2.6 0 3.6 1.6 3.6 4.3v6h-3v-5.5c0-1.4-.4-2.3-1.7-2.3s-2.3 1-2.3 2.5v5.3h-3z", True),
    "email": ("EMAIL", "mohamedsaizonou86", "#f87171", "M3 6h18v12h-18zM3 6l9 7l9 -7", False),
    "whatsapp": ("WHATSAPP", "+221 76 182 36 98", "#34d399",
                 "M12 3.5a8.5 8.5 0 0 0 -7.3 12.8l-1.2 4.2l4.3 -1.1a8.5 8.5 0 1 0 4.2 -15.9M9 8.5c.3-.6.6-.6 1-.6l.6 .1l1 2.2l-.7 .9c.5 1.1 1.5 2 2.6 2.6l.9-.8l2.1 1l-.1.7c-.3.8-1.2 1.2-2 1.1c-3-.5-5.6-3.1-6-6c0-.5.2-.9.6-1.2", False),
}


def build(lab, sub, col, ic, filled):
    fill = f'fill="{col}"' if filled else f'fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="288" height="72" viewBox="0 0 288 72" role="img" aria-label="{lab} — {esc(sub)}">
  <defs><style>{BASE_CSS}
    .sweep{{animation:sw 4s ease-in-out infinite}}@keyframes sw{{0%{{transform:translateX(-120px)}}60%,100%{{transform:translateX(320px)}}}}</style>
  <linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="{P["a2"]}" stop-opacity="0"/><stop offset=".5" stop-color="{P["a2"]}" stop-opacity=".09"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></linearGradient>
  <clipPath id="c"><rect width="288" height="72" rx="12"/></clipPath></defs>
  <g clip-path="url(#c)">
    <rect width="288" height="72" fill="{P["panel"]}"/>
    <rect width="3" height="72" fill="{col}"/>
    <rect width="100" height="72" fill="url(#s)" class="sweep"/>
    <rect x="18" y="16" width="40" height="40" rx="10" fill="{col}" fill-opacity=".1"/>
    <g transform="translate(26 24)"><path d="{ic}" {fill}/></g>
    <text x="72" y="33" class="m" font-size="13" font-weight="800" letter-spacing="2.5" fill="{P["ink"]}">{lab}</text>
    <text x="72" y="52" class="m" font-size="11" fill="{P["muted"]}">{esc(sub)}</text>
    <text x="268" y="42" text-anchor="end" class="m" font-size="16" fill="{col}">↗</text>
  </g>
  {frame(288, 72, 12)}
</svg>
'''


def main(argv=None):
    wanted = set(argv if argv is not None else sys.argv[1:])
    for key, spec in BUTTONS.items():
        if not wanted or key in wanted:
            save(f"uplink-{key}.svg", build(*spec))


if __name__ == "__main__":
    main()

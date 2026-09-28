#!/usr/bin/env python3
"""
stack.py → assets/stack.svg
Section 02 : « MODULES.LOAD() », pastilles de technos avec icônes, chargées une à une.

    python generators/stack.py

Ajouter une techno : l'ajouter dans STACK ci-dessous. Si elle n'a pas encore d'icône dans
data/icons.json, ajouter une entrée { "p": "<path SVG 24×24>", "h": "#couleur" }
(chemins disponibles sur https://simpleicons.org) ou { "mono": "AB", "h": "#couleur" } pour un monogramme.
"""
from _common import BASE_CSS, ICONS, P, esc, frame, icon, save

# ── Contenu éditable : (catégorie, [(techno, est_core), …]) ────────────────
STACK = [
    ("BACKEND", [("Java", 0), ("Spring Boot", 1), ("Spring Security", 0), ("JPA / Hibernate", 0), ("Maven", 0), ("C#", 0), (".NET / ASP.NET", 0)]),
    ("API & ARCHI", [("Hexagonale · DDD", 0), ("Swagger / OpenAPI", 0), ("WebSocket", 0), ("JWT", 0), ("Keycloak", 0)]),
    ("FRONTEND", [("Angular", 1), ("TypeScript", 0), ("Tailwind CSS", 0), ("Bootstrap", 0), ("HTML5", 0), ("CSS3", 0)]),
    ("DATA", [("PostgreSQL", 0), ("MySQL", 0), ("MongoDB", 0), ("Redis", 0), ("Flyway", 0)]),
    ("DEVOPS", [("Docker", 0), ("Git", 0), ("GitHub Actions", 0), ("Jenkins", 0), ("SonarQube", 0), ("OpenShift", 0)]),
    ("OBSERVABILITÉ", [("Grafana", 0), ("Prometheus", 0), ("Firebase", 0), ("Cloudflare", 0)]),
    ("OUTILS & TESTS", [("JUnit 5", 0), ("IntelliJ IDEA", 0), ("VS Code", 0)]),
]

W, TOP, ROW_H = 1200, 64, 58


def build():
    missing = [n for _, chips in STACK for n, _ in chips if n not in ICONS]
    if missing:
        raise SystemExit(f"Icônes manquantes dans data/icons.json : {', '.join(missing)}")

    parts, i, y = [], 0, TOP
    for cat, chips in STACK:
        parts.append(f'<text x="24" y="{y + 29}" class="m cat">{esc(cat)}</text><path d="M24 {y + 44}H160" stroke="{P["line"]}"/>')
        x = 180
        for name, core in chips:
            cw = int(46 + len(name) * 8.4) + (46 if core else 0)
            if x + cw > W - 20:  # retour à la ligne automatique
                y += ROW_H
                x = 180
            d = .2 + i * .07
            i += 1
            core_tag = (f'<rect x="{x + cw - 46}" y="{y + 18}" width="36" height="18" rx="4" fill="{P["a1"]}" fill-opacity=".14"/>'
                        f'<text x="{x + cw - 28}" y="{y + 31}" text-anchor="middle" class="m core">CORE</text>') if core else ""
            parts.append(
                f'<g class="chip" style="animation-delay:{d:.2f}s">'
                f'<rect x="{x}" y="{y + 8}" width="{cw}" height="38" rx="9" fill="{P["chip"]}" stroke="{P["a1"] if core else P["chipline"]}" stroke-width="{1.5 if core else 1}"/>'
                + icon(name, x + 20, y + 27)
                + f'<text x="{x + 38}" y="{y + 32}" class="m nm">{esc(name)}</text>'
                + core_tag
                + f'<rect x="{x + 10}" y="{y + 42}" width="{cw - 20}" height="2" rx="1" fill="{ICONS[name]["h"]}" class="load" style="animation-delay:{d + .15:.2f}s"/></g>')
            x += cw + 10
        y += ROW_H
    H, total = y + 14, i
    names = ", ".join(n for _, c in STACK for n, _ in c)
    body = "".join("\n  " + p for p in parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Stack : {esc(names)}">
  <defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{P["a1"]}" stroke-opacity=".07"/></pattern>
    <style>
      {BASE_CSS}
      .cat{{font-size:11.5px;letter-spacing:2.5px;fill:{P["deep"]};font-weight:800}}
      .nm{{font-size:14px;fill:{P["ink"]}}}
      .core{{font-size:10px;letter-spacing:1.5px;fill:{P["deep"]};font-weight:800}}
      .hd{{font-size:12px;letter-spacing:2.5px;fill:{P["muted"]}}}
      .chip{{opacity:0;animation:in .4s ease-out forwards}}
      @keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
      .load{{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:ld .7s ease-out forwards}}
      @keyframes ld{{to{{transform:scaleX(1);opacity:.6}}}}
      .done{{opacity:0;animation:fd .5s forwards}}@keyframes fd{{to{{opacity:1}}}}
    </style>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="{P["panel"]}"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
  <text x="24" y="30" class="m hd">MODULES.LOAD()</text>
  <text x="{W - 24}" y="30" text-anchor="end" class="m hd done" style="animation-delay:{.2 + total * .07 + .4:.2f}s"><tspan fill="{P["ok"]}">✔</tspan> {total} modules chargés · 0 erreur</text>
  <path d="M1 46H{W - 1}" stroke="{P["line"]}"/>{body}
  {frame(W, H, 14)}
</svg>
'''


def main():
    save("stack.svg", build())


if __name__ == "__main__":
    main()

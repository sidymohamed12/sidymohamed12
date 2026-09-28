#!/usr/bin/env python3
"""
Génère dist/telemetry.svg : tes statistiques GitHub (dépôts et contributions privés inclus
si le secret GH_STATS_TOKEN est fourni). Exécuté par .github/workflows/profile.yml.

Aucune dépendance : Python 3 standard uniquement.
Test local sans réseau :  python3 .github/scripts/build_profile.py --mock
"""
import datetime as dt, json, os, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
LOGIN = os.environ.get("GH_LOGIN", "sidymohamed12")
TOKEN = os.environ.get("GH_TOKEN", "")
MOCK = "--mock" in sys.argv

FONT = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
P = dict(bg="#070b12", panel="#0b111b", line="#1d2b3c", ink="#e8f1f8", text="#b4c4d4", muted="#7c8ea3",
         faint="#4d6075", a1="#2dd4bf", a2="#22d3ee", a3="#60a5fa", deep="#5eead4", ok="#34d399")
MONTHS = ["JAN", "FÉV", "MAR", "AVR", "MAI", "JUN", "JUL", "AOÛ", "SEP", "OCT", "NOV", "DÉC"]


# ─────────────────────────── GitHub API ───────────────────────────
def gql(query, variables=None):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "profile-builder"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if out.get("errors"):
        raise RuntimeError(out["errors"])
    return out["data"]


def owner_node():
    """`viewer` quand le token appartient au propriétaire (accès aux dépôts et contributions privés)."""
    try:
        if gql("{ viewer { login } }")["viewer"]["login"].lower() == LOGIN.lower():
            return "viewer", ""
    except Exception:
        pass
    return "user(login: $login)", "$login: String!"


def fetch():
    node, decl = owner_node()
    args = f"({decl}, $after: String)" if decl else "($after: String)"
    q_repos = f"""query{args} {{ u: {node} {{
        createdAt avatarUrl(size: 320)
        repositories(ownerAffiliations: OWNER, isFork: false, first: 100, after: $after) {{
          totalCount pageInfo {{ hasNextPage endCursor }}
          nodes {{ isPrivate stargazerCount
            languages(first: 10, orderBy: {{field: SIZE, direction: DESC}}) {{ edges {{ size node {{ name color }} }} }} }}
        }} }} }}"""
    repos, after, user = [], None, None
    while True:
        v = {"after": after}
        if decl:
            v["login"] = LOGIN
        d = gql(q_repos, v)["u"]
        user = user or d
        repos += d["repositories"]["nodes"]
        if not d["repositories"]["pageInfo"]["hasNextPage"]:
            break
        after = d["repositories"]["pageInfo"]["endCursor"]

    q_year = f"""query{"(" + decl + ", $from: DateTime!, $to: DateTime!)" if decl else "($from: DateTime!, $to: DateTime!)"} {{ u: {node} {{
        contributionsCollection(from: $from, to: $to) {{ contributionCalendar {{ weeks {{ contributionDays {{ date contributionCount }} }} }} }} }} }}"""
    now = dt.datetime.now(dt.timezone.utc)
    created = dt.datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    days = {}
    for year in range(created.year, now.year + 1):
        start = max(created, dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc))
        end = min(now, dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc))
        v = {"from": start.isoformat(), "to": end.isoformat()}
        if decl:
            v["login"] = LOGIN
        cal = gql(q_year, v)["u"]["contributionsCollection"]["contributionCalendar"]
        for wk in cal["weeks"]:
            for day in wk["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
    return user, repos, days


def mock():
    import random
    random.seed(12)
    today = dt.date.today()
    days = {}
    for i in range(1060):
        d = today - dt.timedelta(days=i)
        days[d.isoformat()] = 0 if random.random() < .3 else random.randint(1, 9)
    langs = [("Java", "#b07219", 900), ("TypeScript", "#3178c6", 420), ("HTML", "#e34c26", 180),
             ("CSS", "#663399", 90), ("C#", "#178600", 70), ("Shell", "#89e051", 20), ("Dockerfile", "#384d54", 8)]
    repos = [{"isPrivate": i % 3 == 0, "stargazerCount": i % 4,
              "languages": {"edges": [{"size": s * (1 + i % 3), "node": {"name": n, "color": c}} for n, c, s in langs[i % 3:i % 3 + 4]]}}
             for i in range(38)]
    return {"createdAt": "2023-11-05T00:00:00Z", "avatarUrl": ""}, repos, days


# ─────────────────────────── calculs ───────────────────────────
def compute(repos, days):
    today = dt.datetime.now(dt.timezone.utc).date()
    series = sorted((dt.date.fromisoformat(k), v) for k, v in days.items() if dt.date.fromisoformat(k) <= today)
    total = sum(v for _, v in series)
    longest = run = 0
    for _, v in series:
        run = run + 1 if v > 0 else 0
        longest = max(longest, run)
    lookup = dict(series)
    cur, d = 0, today
    if lookup.get(d, 0) == 0:
        d -= dt.timedelta(days=1)  # la journée en cours n'est pas encore finie
    while lookup.get(d, 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    months = []
    y, m = today.year, today.month
    for _ in range(12):
        months.append(((y, m), sum(v for k, v in series if k.year == y and k.month == m)))
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    months.reverse()
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or P["faint"]])[0] += e["size"]
    lt = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    top = [(n, c, s / lt * 100) for n, (s, c) in top]
    return dict(total=total, repos=len(repos), private=sum(r["isPrivate"] for r in repos),
                stars=sum(r["stargazerCount"] for r in repos), cur=cur, longest=longest, months=months, langs=top)


def fmt(n):
    return f"{n:,}".replace(",", " ")


# ─────────────────────────── rendu : telemetry ───────────────────────────
def telemetry_svg(s):
    W, H = 1200, 392
    tiles = [("CONTRIBUTIONS", fmt(s["total"]), "publiques + privées, depuis le début", "M3 17l5-5 4 4 8-8M15 8h5v5"),
             ("REPOS CRÉÉS", fmt(s["repos"]), f"dont {s['private']} privés · hors forks", "M4 4h11l5 5v11H4zM15 4v5h5"),
             ("ÉTOILES", fmt(s["stars"]), "obtenues sur mes dépôts", "M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4 6.5 20.3l1-6.2L3 9.7l6.2-.9z"),
             ("SÉRIE ACTUELLE", f"{s['cur']} j", f"record : {s['longest']} jours d'affilée", "M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-3 2-4 2-6 1 1 2 2 3 2 0-2-1-4 0-6z")]
    tw, gap, x0 = 276, 16, 24
    out = []
    for i, (lab, val, sub, ic) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        out.append(f'''<g class="in" style="animation-delay:{.15 + i * .12:.2f}s">
      <rect x="{x}" y="62" width="{tw}" height="108" rx="12" fill="#0e1723" stroke="{P["line"]}"/>
      <rect x="{x}" y="62" width="4" height="108" rx="2" fill="url(#acc)"/>
      <text x="{x + 22}" y="90" class="m lab">{lab}</text>
      <text x="{x + 22}" y="134" class="m big">{val}</text>
      <text x="{x + 22}" y="156" class="m sub">{sub}</text>
      <g transform="translate({x + tw - 42} 76)"><rect width="28" height="28" rx="8" fill="{P["a1"]}" fill-opacity=".1"/>
        <path transform="translate(4 4) scale(.8333)" d="{ic}" fill="none" stroke="{P["deep"]}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></g>
    </g>''')
    # barres mensuelles
    bx, by, bw, bh = 24, 200, 660, 176
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#0e1723" stroke="{P["line"]}"/>')
    out.append(f'<text x="{bx + 20}" y="{by + 26}" class="m lab">CONTRIBUTIONS · 12 DERNIERS MOIS</text>')
    mx = max(v for _, v in s["months"]) or 1
    colw = (bw - 40) / 12
    base = by + bh - 28
    for i, ((y, m), v) in enumerate(s["months"]):
        h = max(3, v / mx * 96)
        x = bx + 20 + i * colw + 8
        out.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{colw - 16:.1f}" height="{h:.1f}" rx="4" fill="url(#bar)" class="grow" style="animation-delay:{.5 + i * .05:.2f}s"/>')
        out.append(f'<text x="{x + (colw - 16) / 2:.1f}" y="{base - h - 6:.1f}" text-anchor="middle" class="m val">{v}</text>')
        out.append(f'<text x="{x + (colw - 16) / 2:.1f}" y="{base + 18}" text-anchor="middle" class="m mo">{MONTHS[m - 1]}</text>')
    # langages
    lx, lw = bx + bw + 16, W - 24 - (bx + bw + 16)
    out.append(f'<rect x="{lx}" y="{by}" width="{lw}" height="{bh}" rx="12" fill="#0e1723" stroke="{P["line"]}"/>')
    out.append(f'<text x="{lx + 20}" y="{by + 26}" class="m lab">LANGAGES · TOUS MES DÉPÔTS</text>')
    out.append(f'<clipPath id="lc"><rect x="{lx + 20}" y="{by + 44}" width="{lw - 40}" height="12" rx="6"/></clipPath><g clip-path="url(#lc)"><rect x="{lx + 20}" y="{by + 44}" width="{lw - 40}" height="12" fill="{P["line"]}"/>')
    cx, shown = lx + 20, sum(p for _, _, p in s["langs"]) or 1
    for n, c, p in s["langs"]:
        ww = (lw - 40) * p / shown
        out.append(f'<rect x="{cx:.1f}" y="{by + 44}" width="{ww + .5:.1f}" height="12" fill="{c}"/>')
        cx += ww
    out.append("</g>")
    for i, (n, c, p) in enumerate(s["langs"]):
        col, row = i % 2, i // 2
        x = lx + 20 + col * ((lw - 40) / 2)
        y = by + 88 + row * 28
        out.append(f'<g class="in" style="animation-delay:{.8 + i * .08:.2f}s"><circle cx="{x + 6}" cy="{y - 4}" r="5" fill="{c}"/>'
                   f'<text x="{x + 20}" y="{y}" class="m ln">{n}</text><text x="{x + (lw - 40) / 2 - 16}" y="{y}" text-anchor="end" class="m pc">{p:.1f}%</text></g>')
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Statistiques GitHub : {s["total"]} contributions, {s["repos"]} dépôts, {s["stars"]} étoiles, série actuelle {s["cur"]} jours">
  <defs>
    <linearGradient id="acc" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{P["a1"]}"/><stop offset="1" stop-color="{P["a3"]}"/></linearGradient>
    <linearGradient id="bar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{P["a2"]}"/><stop offset="1" stop-color="{P["a1"]}"/></linearGradient>
    <pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{P["a1"]}" stroke-opacity=".07"/></pattern>
    <style>
      .m{{font-family:{FONT}}}
      .lab{{font-size:11px;letter-spacing:2.5px;fill:{P["deep"]};font-weight:800}}
      .big{{font-size:36px;font-weight:800;fill:{P["ink"]}}}
      .sub{{font-size:11.5px;fill:{P["muted"]}}}
      .val{{font-size:10px;fill:{P["muted"]}}}
      .mo{{font-size:10px;letter-spacing:1px;fill:{P["faint"]}}}
      .ln{{font-size:13px;fill:{P["ink"]}}}
      .pc{{font-size:12px;fill:{P["muted"]}}}
      .hd{{font-size:12px;letter-spacing:2.5px;fill:{P["muted"]}}}
      .in{{opacity:0;animation:in .45s ease-out forwards}}
      @keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
      .grow{{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:gr .7s cubic-bezier(.3,1.3,.5,1) forwards}}
      @keyframes gr{{to{{transform:scaleY(1)}}}}
      .pulse{{animation:pu 2s ease-in-out infinite}}@keyframes pu{{50%{{opacity:.25}}}}
    </style>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="{P["panel"]}"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
  <text x="24" y="31" class="m hd">TELEMETRY.SYNC()</text>
  <text x="{W - 24}" y="31" text-anchor="end" class="m hd"><tspan fill="{P["ok"]}" class="pulse">●</tspan> maj {stamp}</text>
  <path d="M1 46H{W - 1}" stroke="{P["line"]}"/>
  {chr(10).join("  " + o for o in out)}
  <rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="none" stroke="{P["line"]}" stroke-width="1.5"/>
</svg>
'''


def main():
    if not MOCK and not TOKEN:
        sys.exit("GH_TOKEN manquant")
    user, repos, days = mock() if MOCK else fetch()
    stats = compute(repos, days)
    DIST.mkdir(exist_ok=True)
    (DIST / "telemetry.svg").write_text(telemetry_svg(stats))
    print(json.dumps({k: v for k, v in stats.items() if k not in ("months", "langs")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

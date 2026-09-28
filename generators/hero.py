#!/usr/bin/env python3
"""
hero.py → assets/hero.svg
Bannière principale : nom, rôle, accroche, photo qui déborde du cercle, anneaux animés.

    python generators/hero.py                       # utilise data/photo.webp
    python generators/hero.py --photo moi.png       # nouvelle photo (PNG détouré conseillé, nécessite Pillow)
    python generators/hero.py --photo moi.png --crop 380,40,1400,1400   # cadrage manuel (x0,y0,x1,y1)
"""
import argparse
import base64
import io

from _common import ACC, BASE_CSS, DATA, P, frame, grid_pattern, save

# ── Contenu éditable ──────────────────────────────────────────────────────
FIRST_NAME = "SIDY MOHAMED"
LAST_NAME = "SAIZONOU"
ROLE = ("Full-Stack Developer", "Spring Boot", "Angular")          # ligne tapée : « > rôle · A × B »
TAGLINE = ("Du cahier des charges à la mise en production", "backend, frontend, DevOps.")
STATUS = "ONLINE · OPEN TO WORK"
LOCATION = "DAKAR / SÉNÉGAL"
CALLOUTS = ["JAVA", "SPRING", "ANGULAR", "TS"]                     # étiquettes autour des anneaux
PHOTO_FILE = DATA / "photo.webp"


# ── Photo ─────────────────────────────────────────────────────────────────
def prepare_photo(src, crop=None):
    """Recadre une photo (tête en haut, buste en bas) et l'enregistre en WebP dans data/photo.webp."""
    from PIL import Image  # pip install pillow

    im = Image.open(src).convert("RGBA")
    if crop is None:
        # cadrage auto à partir du détourage : la tête = le premier quart de la silhouette
        x0, y0, x1, y1 = im.getchannel("A").getbbox() or (0, 0, *im.size)
        head = im.getchannel("A").crop((x0, y0, x1, y0 + (y1 - y0) // 4)).getbbox()
        cx = x0 + (head[0] + head[2]) / 2 if head else (x0 + x1) / 2
        w = (head[2] - head[0]) * 2.4 if head else (x1 - x0)
        crop = (int(cx - w / 2), max(0, int(y0 - w * .025)), int(cx + w / 2), int(y0 - w * .025 + w * 1.333))
    im = im.crop(crop)
    im = im.resize((400, round(400 * im.height / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=88, method=6)
    PHOTO_FILE.write_bytes(buf.getvalue())
    print(f"✔ photo recadrée {crop} → {PHOTO_FILE.name} ({len(buf.getvalue()) // 1024} Ko)")


def photo_uri():
    return "data:image/webp;base64," + base64.b64encode(PHOTO_FILE.read_bytes()).decode()


# ── Rendu ─────────────────────────────────────────────────────────────────
def build():
    role, a, b = ROLE
    tag1, tag2 = TAGLINE
    c = CALLOUTS
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-label="{FIRST_NAME.title()} {LAST_NAME} — {role} · {a} × {b} · {LOCATION.title()}">
  <defs>
    {ACC}
    <radialGradient id="b1"><stop offset="0" stop-color="{P["a1"]}" stop-opacity=".45"/><stop offset="1" stop-color="{P["a1"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="b2"><stop offset="0" stop-color="{P["a2"]}" stop-opacity=".45"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="b3"><stop offset="0" stop-color="{P["a3"]}" stop-opacity=".35"/><stop offset="1" stop-color="{P["a3"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="core" cx=".5" cy=".25" r=".85"><stop offset="0" stop-color="#1b6f78"/><stop offset=".6" stop-color="#123a55"/><stop offset="1" stop-color="#0c1f36"/></radialGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["a2"]}" stop-opacity="0"/><stop offset=".5" stop-color="{P["a2"]}" stop-opacity=".08"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></linearGradient>
    {grid_pattern("grid", 32, ".08")}
    <radialGradient id="fade" cx=".3" cy=".45" r=".75"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
    <mask id="gm"><rect width="1200" height="400" fill="url(#fade)"/></mask>
    <clipPath id="frame"><rect width="1200" height="400" rx="18"/></clipPath>
    <!-- cercle + zone au-dessus : la tête dépasse du rond, le buste reste dedans -->
    <clipPath id="avatarClip"><circle cx="0" cy="0" r="60"/><rect x="-110" y="-170" width="220" height="158"/></clipPath>
    <clipPath id="type"><rect x="72" y="270" width="0" height="44"><animate attributeName="width" from="0" to="600" begin=".9s" dur="1.6s" fill="freeze" calcMode="spline" keySplines=".3 0 .2 1"/></rect></clipPath>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
    <style>
      {BASE_CSS}
      .meta{{font-size:12px;fill:{P["muted"]};letter-spacing:2px}}
      .name{{font-size:62px;font-weight:800;letter-spacing:6px}}
      .outline{{fill:none;stroke:url(#acc);stroke-width:1.6;stroke-dasharray:900;stroke-dashoffset:900;animation:draw 2.4s .3s ease-out forwards}}
      @keyframes draw{{to{{stroke-dashoffset:0}}}}
      .fadeIn{{opacity:0;animation:fi .8s ease-out forwards}}
      @keyframes fi{{to{{opacity:1}}}}
      .glitch{{opacity:0;animation:gl 7s 3s infinite steps(1)}}
      @keyframes gl{{0%{{opacity:0}}91%{{opacity:.6;transform:translate(3px,-1px)}}92%{{opacity:.45;transform:translate(-3px,1px)}}93%{{opacity:0}}}}
      .blink{{animation:bl 1s steps(1) infinite}}
      @keyframes bl{{50%{{opacity:0}}}}
      .pulse{{animation:pu 2s ease-in-out infinite}}
      @keyframes pu{{50%{{opacity:.25}}}}
      .callout{{font-size:11px;fill:{P["text"]};letter-spacing:1.5px}}
    </style>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1200" height="400" fill="{P["bg"]}"/>
    <!-- aurores -->
    <g filter="url(#blur)">
      <ellipse cx="880" cy="90" rx="260" ry="110" fill="url(#b1)"><animateTransform attributeName="transform" type="translate" values="0 0;-60 30;0 0" dur="16s" repeatCount="indefinite"/></ellipse>
      <ellipse cx="1060" cy="300" rx="240" ry="120" fill="url(#b3)"><animateTransform attributeName="transform" type="translate" values="0 0;-40 -30;0 0" dur="19s" repeatCount="indefinite"/></ellipse>
      <ellipse cx="420" cy="360" rx="320" ry="90" fill="url(#b2)"><animateTransform attributeName="transform" type="translate" values="0 0;80 -20;0 0" dur="22s" repeatCount="indefinite"/></ellipse>
    </g>
    <rect width="1200" height="400" fill="url(#grid)" mask="url(#gm)"/>
    <rect x="0" y="-80" width="1200" height="80" fill="url(#scan)"><animate attributeName="y" from="-80" to="400" dur="5s" repeatCount="indefinite"/></rect>

    <g class="m meta">
      <text x="72" y="52">SMS-12 // PROFILE.SYS</text>
      <text x="560" y="52" text-anchor="end" fill="{P["ok"]}" style="fill:{P["ok"]}">{STATUS}</text>
    </g>
    <circle cx="352" cy="48" r="4" fill="{P["ok"]}" class="pulse"/>
    <path d="M72 66H560" stroke="{P["a1"]}" stroke-opacity=".3"/>
    <path d="M72 66H140" stroke="url(#acc)" stroke-width="2"/>

    <g class="m name">
      <text x="72" y="160" fill="{P["a1"]}" class="glitch">{FIRST_NAME}</text>
      <text x="72" y="160" fill="{P["ink"]}" class="fadeIn">{FIRST_NAME}</text>
      <text x="72" y="236" class="outline">{LAST_NAME}</text>
    </g>

    <g clip-path="url(#type)">
      <text x="72" y="298" class="m" font-size="20" fill="{P["text"]}"><tspan fill="{P["a1"]}">&gt;</tspan> {role} <tspan fill="{P["faint"]}">·</tspan> {a} <tspan fill="{P["a2"]}">×</tspan> {b}</text>
    </g>
    <rect x="636" y="282" width="11" height="20" fill="{P["a1"]}" class="blink" opacity="0"><set attributeName="opacity" to="1" begin="2.5s"/></rect>
    <text x="72" y="332" class="m fadeIn" font-size="14" fill="{P["muted"]}" style="animation-delay:2.4s">{tag1} <tspan fill="{P["faint"]}">:</tspan> <tspan fill="{P["deep"]}">{tag2}</tspan></text>

    <g transform="translate(960 190)">
      <circle r="152" fill="{P["panel"]}" fill-opacity=".45" stroke="{P["a1"]}" stroke-opacity=".2"/>
      <g><circle r="152" fill="none" stroke="{P["a1"]}" stroke-opacity=".6" stroke-dasharray="4 14"/><circle cx="152" r="4.5" fill="{P["a1"]}"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite"/></g>
      <g><circle r="112" fill="none" stroke="{P["a2"]}" stroke-opacity=".7" stroke-dasharray="120 40 10 40"/><circle cy="-112" r="4" fill="{P["a2"]}"/><circle cy="112" r="3" fill="{P["a2"]}" opacity=".7"/>
        <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="22s" repeatCount="indefinite"/></g>
      <g><circle r="88" fill="none" stroke="{P["a3"]}" stroke-opacity=".55" stroke-dasharray="2 6"/><circle cx="-88" r="3.5" fill="{P["a3"]}"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></g>
      <circle r="72" fill="none" stroke="{P["a1"]}" stroke-width="1.5"><animate attributeName="r" values="72;152" dur="3.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".7;0" dur="3.2s" repeatCount="indefinite"/></circle>
      <g transform="scale(1.2)"><circle r="60" fill="url(#core)"/>
      <image x="-81.7" y="-106.7" width="170" height="226.5" href="{photo_uri()}" preserveAspectRatio="xMidYMid meet" clip-path="url(#avatarClip)"/>
      <path d="M-60 0A60 60 0 0 0 60 0" fill="none" stroke="url(#acc)" stroke-width="3"/>
      <path d="M-60 0A60 60 0 0 1 -44 -40.8M60 0A60 60 0 0 0 44 -40.8" fill="none" stroke="url(#acc)" stroke-width="2.5" stroke-linecap="round"/></g>
    </g>

    <g class="m callout fadeIn" style="animation-delay:1.6s">
      <path d="M1066 84l22-22h60" fill="none" stroke="{P["a1"]}" stroke-opacity=".7"/><circle cx="1066" cy="84" r="2.5" fill="{P["a1"]}"/><text x="1090" y="56">{c[0]}</text>
      <path d="M842 104l-22-22h-44" fill="none" stroke="{P["a1"]}" stroke-opacity=".7"/><circle cx="842" cy="104" r="2.5" fill="{P["a1"]}"/><text x="776" y="74">{c[1]}</text>
      <path d="M1088 280l22 22h40" fill="none" stroke="{P["a1"]}" stroke-opacity=".7"/><circle cx="1088" cy="280" r="2.5" fill="{P["a1"]}"/><text x="1112" y="296">{c[2]}</text>
      <path d="M840 282l-22 22h-44" fill="none" stroke="{P["a1"]}" stroke-opacity=".7"/><circle cx="840" cy="282" r="2.5" fill="{P["a1"]}"/><text x="774" y="298">{c[3]}</text>
    </g>

    <path d="M72 360H1128" stroke="{P["a1"]}" stroke-opacity=".25"/>
    <text x="600" y="384" text-anchor="middle" class="m meta" fill="{P["deep"]}" style="fill:{P["deep"]}">{LOCATION}</text>

    <g fill="none" stroke="url(#acc)" stroke-width="2">
      <path d="M20 48V20H48"/><path d="M1152 20H1180V48"/><path d="M20 352V380H48"/><path d="M1152 380H1180V352"/>
    </g>
  </g>
  {frame(1200, 400, 18)}
</svg>
'''


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--photo", help="nouvelle photo à recadrer (PNG détouré conseillé)")
    ap.add_argument("--crop", help="cadrage manuel x0,y0,x1,y1 (pixels de la photo source)")
    args = ap.parse_args(argv)
    if args.photo:
        prepare_photo(args.photo, tuple(map(int, args.crop.split(","))) if args.crop else None)
    save("hero.svg", build())


if __name__ == "__main__":
    main()

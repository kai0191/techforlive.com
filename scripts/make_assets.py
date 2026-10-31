"""Draw the TechForLive logo, favicons and social image (run once; output in static/)."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
A = os.path.join(ST, "assets")
os.makedirs(A, exist_ok=True)
INK, LIME, RED = (11, 18, 32), (198, 244, 50), (255, 59, 78)
PULSE = [(9, 36), (19, 36), (24, 23), (32, 48), (38, 31), (42, 36), (55, 36)]

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0b1220"/>'
       '<path d="M9 36h10l5-13 8 25 6-17 4 5h13" fill="none" stroke="#c6f432" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
       '<circle cx="51" cy="15" r="5.5" fill="#ff3b4e"/></svg>')
open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
open(os.path.join(A, "logo-mark.svg"), "w").write(SVG)
open(os.path.join(A, "logo.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 64"><rect width="64" height="64" rx="16" fill="#0b1220"/>'
    '<path d="M9 36h10l5-13 8 25 6-17 4 5h13" fill="none" stroke="#c6f432" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="51" cy="15" r="5.5" fill="#ff3b4e"/>'
    '<text x="80" y="44" font-family="Space Grotesk,Inter,Arial,sans-serif" font-weight="700" font-size="34" fill="#0b1220" letter-spacing="-.5">TechFor<tspan fill="#5a8f00">Live</tspan></text></svg>')


def mark(size):
    s = 8  # supersample
    W = size * s
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = W / 64
    d.rounded_rectangle([0, 0, W - 1, W - 1], radius=16 * k, fill=INK)
    pts = [(x * k, y * k) for x, y in PULSE]
    d.line(pts, fill=LIME, width=int(5 * k), joint="curve")
    r = 2.5 * k
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=LIME)
    d.ellipse([(51 - 5.5) * k, (15 - 5.5) * k, (51 + 5.5) * k, (15 + 5.5) * k], fill=RED)
    return im.resize((size, size), Image.LANCZOS)


for n, sz in (("logo-512.png", 512), ("icon-192.png", 192)):
    mark(sz).save(os.path.join(A, n))
mark(180).save(os.path.join(ST, "apple-touch-icon.png"))
mark(64).save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

open(os.path.join(ST, "site.webmanifest"), "w").write(
    '{"name":"TechForLive","short_name":"TechForLive","start_url":"/","display":"standalone","background_color":"#0b1220","theme_color":"#0b1220",'
    '"icons":[{"src":"/assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/assets/logo-512.png","sizes":"512x512","type":"image/png"}]}')


def font(size, bold=True):
    for f in (["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"] if bold else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


og = Image.new("RGB", (1200, 630), INK)
d = ImageDraw.Draw(og)
for i in range(0, 630, 3):  # soft lime glow top-right
    pass
glow = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r in range(420, 0, -6):
    a = int(38 * (1 - r / 420))
    gd.ellipse([1050 - r, -120 - r, 1050 + r, -120 + r], fill=(198, 244, 50, a))
og.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(og)
og.paste(mark(150), (80, 90), mark(150))
d.text((260, 112), "TechFor", font=font(92), fill=(255, 255, 255))
w = d.textlength("TechFor", font=font(92))
d.text((260 + w, 112), "Live", font=font(92), fill=LIME)
d.text((84, 300), "Tech news as it breaks.", font=font(58), fill=(255, 255, 255))
d.text((84, 372), "Explained for everyday life.", font=font(58), fill=LIME)
d.text((84, 480), "Live Wire from 15 newsrooms · Plain-English guides · Free tools", font=font(30, False), fill=(175, 188, 210))
d.ellipse([84, 548, 100, 564], fill=RED)
d.text((112, 541), "techforlive.com", font=font(28), fill=(255, 255, 255))
og.save(os.path.join(A, "og.png"), optimize=True)
print("assets written")

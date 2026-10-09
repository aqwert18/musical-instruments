"""Generate the app icons (icons/*.png). Usage: python tools/icons.py"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'icons'; OUT.mkdir(exist_ok=True)
BRASS, INK, PAPER = (133, 89, 12), (255, 255, 255), (242, 229, 198)
FONTS = ['C:/Windows/Fonts/msjhbd.ttc', 'C:/Windows/Fonts/msjh.ttc', '/System/Library/Fonts/PingFang.ttc']

def font(size):
    for f in FONTS:
        try: return ImageFont.truetype(f, size)
        except OSError: pass
    return ImageFont.load_default()

def icon(px, maskable=False):
    S = 1024
    im = Image.new('RGB', (S, S), BRASS)
    d = ImageDraw.Draw(im)
    pad = 0 if maskable else 0
    # staff lines across the icon
    for i in range(5):
        y = 300 + i * 46
        d.line([(120, y), (904, y)], fill=PAPER, width=10)
    f = font(560 if not maskable else 470)
    d.text((S / 2, S / 2 + 40), '樂', font=f, fill=INK, anchor='mm', stroke_width=18, stroke_fill=BRASS)
    if not maskable:
        m = Image.new('L', (S, S), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, S, S], radius=220, fill=255)
        bg = Image.new('RGBA', (S, S), (0, 0, 0, 0)); bg.paste(im, (0, 0), m); im = bg
    return im.resize((px, px), Image.LANCZOS)

icon(192).save(OUT / 'icon-192.png')
icon(512).save(OUT / 'icon-512.png')
icon(512, maskable=True).save(OUT / 'icon-maskable-512.png')
icon(180, maskable=True).save(OUT / 'icon-180.png')   # iOS adds its own rounded corners
print('icons ok')

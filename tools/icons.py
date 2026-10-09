"""Generate the app icons (icons/*.png) from icons/source.png.

Usage:  python tools/icons.py
To change the icon, replace icons/source.png with a square image and re-run.
"""
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'icons'
src = Image.open(OUT / 'source.png').convert('RGB')
side = min(src.size)
src = src.crop(((src.width - side) // 2, (src.height - side) // 2, (src.width + side) // 2, (src.height + side) // 2))

def rounded(im, radius_ratio=0.22):
    s = im.size[0]
    mask = Image.new('L', (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * radius_ratio), fill=255)
    out = Image.new('RGBA', (s, s), (0, 0, 0, 0)); out.paste(im, (0, 0), mask)
    return out

big = src.resize((1024, 1024), Image.LANCZOS)
rounded(big).resize((192, 192), Image.LANCZOS).save(OUT / 'icon-192.png')
rounded(big).resize((512, 512), Image.LANCZOS).save(OUT / 'icon-512.png')
big.resize((512, 512), Image.LANCZOS).save(OUT / 'icon-maskable-512.png')   # Android crops its own shape
big.resize((180, 180), Image.LANCZOS).save(OUT / 'icon-180.png')            # iOS rounds the corners itself
print('icons ok')

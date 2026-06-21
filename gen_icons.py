"""Generate Kids Pay app icons. Run: python gen_icons.py"""
from PIL import Image, ImageDraw


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make(size, maskable=False):
    ss = 4
    s = size * ss
    img = Image.new("RGB", (s, s))
    px = img.load()
    top, bot = (0x16, 0x35, 0x63), (0x06, 0x12, 0x26)
    for y in range(s):
        c = lerp(top, bot, (y / s) ** 1.1)
        for x in range(s):
            px[x, y] = c
    cx = cy = s / 2
    scale = 0.52 if maskable else 0.72
    r = s * scale / 2
    yoff = s * 0.02 if maskable else s * 0.04
    cardw, cardh = r * 1.15, r * 0.74
    card = Image.new("RGBA", (int(cardw), int(cardh)), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    for yy in range(int(cardh)):
        c = lerp((0x2b, 0x5b, 0xbf), (0x0c, 0x3f, 0x9e), yy / cardh)
        cd.line([(0, yy), (cardw, yy)], fill=c + (255,))
    cardr = int(r * 0.16)
    mask = Image.new("L", (int(cardw), int(cardh)), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cardw - 1, cardh - 1], radius=cardr, fill=255)
    chipw, chiph = cardw * 0.18, cardh * 0.22
    cd.rounded_rectangle(
        [cardw * 0.12, cardh * 0.2, cardw * 0.12 + chipw, cardh * 0.2 + chiph],
        radius=int(chiph * 0.25), fill=(0xf6, 0xd3, 0x65, 255),
    )
    card.putalpha(mask)
    card = card.rotate(-10, expand=True, resample=Image.BICUBIC)
    img.paste(card, (int(cx - card.width / 2), int(cy - card.height / 2 + yoff)), card)
    d = ImageDraw.Draw(img, "RGBA")
    wave_cx, wave_cy = cx + r * 0.5, cy - r * 0.45
    blue = (0x9f, 0xc4, 0xff)
    w = max(2, int(s * 0.028))
    for rr in [r * 0.28, r * 0.5, r * 0.72]:
        d.arc([wave_cx - rr, wave_cy - rr, wave_cx + rr, wave_cy + rr],
              start=-58, end=58, fill=blue + (255,), width=w)
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    make(192).save("icon-192.png")
    make(512).save("icon-512.png")
    make(512, maskable=True).save("icon-maskable-512.png")
    make(180).save("apple-touch-icon.png")
    print("Icons written: icon-192.png, icon-512.png, icon-maskable-512.png, apple-touch-icon.png")

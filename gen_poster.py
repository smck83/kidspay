"""Generate the printable QR poster for Kids Pay. Run: python gen_poster.py"""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

URL = "https://smck83.github.io/kidspay/"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def centred(d, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)


# Poster canvas at 2x for crisp print (roughly portrait, prints fine on A4/Letter)
W, H = 1240, 1754
img = Image.new("RGB", (W, H))
px = img.load()
top, bot = (0x14, 0x31, 0x5c), (0x07, 0x14, 0x2a)
for y in range(H):
    c = lerp(top, bot, (y / H) ** 1.1)
    for x in range(W):
        px[x, y] = c
d = ImageDraw.Draw(img)

# Header
centred(d, 150, "Kids Pay", font(120, bold=True), (0xea, 0xf2, 0xff))
centred(d, 300, "Tap. Beep. Paid!", font(54), (0x9f, 0xb4, 0xd6))

# QR with high error correction so a sticker can take some wear
qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=10, border=2)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=(11, 31, 58), back_color="white").convert("RGB")
qr_size = 760
qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)

# White rounded card behind the QR
pad = 46
card_w = qr_size + pad * 2
card_x = (W - card_w) // 2
card_y = 470
card = Image.new("RGB", (card_w, card_w), "white")
mask = Image.new("L", (card_w, card_w), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w - 1, card_w - 1], radius=48, fill=255)
img.paste(card, (card_x, card_y), mask)
img.paste(qr_img, (card_x + pad, card_y + pad))

# Instructions
ty = card_y + card_w + 70
centred(d, ty, "Point a phone camera at the code", font(46, bold=True), (0xea, 0xf2, 0xff))
centred(d, ty + 70, "to open the pay screen, then tap to pay.", font(40), (0x9f, 0xb4, 0xd6))

# URL chip
chip = font(38)
url_w = d.textlength(URL, font=chip)
chip_pad = 28
cw = url_w + chip_pad * 2
cx0 = (W - cw) / 2
cy0 = ty + 160
d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + 74], radius=18,
                    fill=(0x1a, 0x6d, 0xff))
d.text((cx0 + chip_pad, cy0 + 16), URL, font=chip, fill="white")

img.save("qr-poster.png", "PNG")

# Also a plain transparent QR PNG for reuse
qr2 = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=12, border=2)
qr2.add_data(URL)
qr2.make(fit=True)
qr2_img = qr2.make_image(fill_color=(11, 31, 58), back_color="white").convert("RGB")
qr2_img.save("qr-code.png", "PNG")

print("Wrote qr-poster.png and qr-code.png for", URL)

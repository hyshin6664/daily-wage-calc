"""급여 계산기 PNG 아이콘 생성기 (192/512)."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\malgunbd.ttf",
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\HMKMRHD.TTF",
]

def find_font():
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return f
    raise RuntimeError("한글 폰트 못 찾음")

def make_icon(size, fname):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 둥근 사각 배경 (파란 그라데이션 느낌)
    radius = int(size * 0.18)
    d.rounded_rectangle([(0,0),(size,size)], radius=radius, fill=(37,99,235,255))
    # 안쪽 카드(흰색)
    pad = int(size * 0.16)
    d.rounded_rectangle([(pad,pad),(size-pad,size-pad)], radius=int(size*0.07), fill=(255,255,255,255))
    # 위쪽 ₩ 디스플레이 (검정 바)
    bar_h = int(size * 0.22)
    bar_pad = int(size * 0.04)
    d.rounded_rectangle([(pad+bar_pad, pad+bar_pad),(size-pad-bar_pad, pad+bar_pad+bar_h)],
                        radius=int(size*0.025), fill=(15,23,42,255))
    # ₩ 표시
    won_size = int(bar_h * 0.7)
    font_path = find_font()
    won_font = ImageFont.truetype(font_path, won_size)
    won_text = "₩"
    won_bbox = d.textbbox((0,0), won_text, font=won_font)
    won_w = won_bbox[2]-won_bbox[0]
    won_h = won_bbox[3]-won_bbox[1]
    d.text((size-pad-bar_pad-won_w-int(size*0.025), pad+bar_pad+(bar_h-won_h)//2-int(size*0.01)),
           won_text, font=won_font, fill=(52,211,153,255))

    # 본문 영역 = 디스플레이 바 아래 ~ 카드 아래
    body_top = pad + bar_pad + bar_h + int(size*0.03)
    body_bot = size - pad - bar_pad
    body_h = body_bot - body_top
    cx = size // 2

    # "급여" — 본문 위쪽 60%
    txt = "급여"
    tsize = int(body_h * 0.55)
    font = ImageFont.truetype(font_path, tsize)
    bbox = d.textbbox((0,0), txt, font=font)
    tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
    ty = body_top + int(body_h * 0.05)
    d.text((cx - tw//2 - bbox[0], ty - bbox[1]), txt, font=font, fill=(37,99,235,255))

    # "계산기" — 본문 아래쪽
    sub = "계산기"
    ssize = int(body_h * 0.22)
    sfont = ImageFont.truetype(font_path, ssize)
    sbbox = d.textbbox((0,0), sub, font=sfont)
    sw = sbbox[2]-sbbox[0]; sh = sbbox[3]-sbbox[1]
    sy = body_bot - sh - int(body_h * 0.05)
    d.text((cx - sw//2 - sbbox[0], sy - sbbox[1]), sub, font=sfont, fill=(100,116,139,255))

    out = os.path.join(OUT_DIR, fname)
    img.save(out, "PNG")
    print(f"saved {out} ({size}x{size})")

make_icon(192, "icon-192.png")
make_icon(512, "icon-512.png")
make_icon(256, "icon-256.png")

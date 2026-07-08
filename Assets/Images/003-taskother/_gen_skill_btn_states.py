# btn_技能图标N_1~4 — §11.13 v7.12.3 · 踩坑见 踩坑记忆库_lixiaotong.md §一 B1～B4
# 禁止：只调亮度(B1) · 小画布放大(B2) · min()反了(B3) · Press<95%(B4)
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_SIZE = 256

# 相对普通态的倍率（必须：HOVER > NORMAL > PRESSED）
RATIO_NORMAL = 1.00
RATIO_HOVER = 1.10      # 悬停 +10%（手游常见 105~110%）
RATIO_PRESSED = 0.96    # 按压 -4%（行业 95~98%，禁止 86% 那种“塌掉”）
RATIO_DISABLED = 0.98

# 普通态占画布比例（留边给 Hover 放大 + 外发光）
FILL_NORMAL = 0.60
FILL_HOVER = FILL_NORMAL * RATIO_HOVER      # 0.66
FILL_PRESSED = FILL_NORMAL * RATIO_PRESSED  # 0.576
FILL_DISABLED = FILL_NORMAL * RATIO_DISABLED

OFFSET_PRESSED_Y = 2   # 按压略下沉 2px（轻量）

SOURCES = [
    ("技能图标 1.png", "btn_技能图标1"),
    ("技能2.png", "btn_技能图标2"),
    ("技能3.png", "btn_技能图标3"),
]


def rgba(img):
    return img.convert("RGBA") if img.mode != "RGBA" else img


def paste_scaled(src, canvas_size, fill_ratio, offset_y=0):
    src = rgba(src)
    sw, sh = src.size
    target = int(canvas_size * fill_ratio)
    scale = target / max(sw, sh)
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    scaled = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    x = (canvas_size - nw) // 2
    y = (canvas_size - nh) // 2 + offset_y
    canvas.paste(scaled, (x, y), scaled)
    return canvas


def add_glow(img, radius=6, strength=0.38):
    w, h = img.size
    alpha = img.split()[3]
    glow = alpha.filter(ImageFilter.GaussianBlur(radius))
    layer = Image.new("RGBA", (w, h), (255, 248, 210, 0))
    layer.putalpha(glow)
    layer = ImageEnhance.Brightness(layer).enhance(strength)
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return Image.alpha_composite(Image.alpha_composite(base, layer), img)


def make_states(src_path):
    src = rgba(Image.open(src_path))
    s = OUTPUT_SIZE

    normal = paste_scaled(src, s, FILL_NORMAL)

    hi = paste_scaled(src, s, FILL_HOVER)
    hi = ImageEnhance.Brightness(hi).enhance(1.15)
    hi = ImageEnhance.Color(hi).enhance(1.10)
    hi = ImageEnhance.Contrast(hi).enhance(1.04)
    hi = add_glow(hi, radius=5, strength=0.35)

    pressed = paste_scaled(src, s, FILL_PRESSED, offset_y=OFFSET_PRESSED_Y)
    pressed = ImageEnhance.Brightness(pressed).enhance(0.88)
    pressed = ImageEnhance.Contrast(pressed).enhance(1.06)

    dis = paste_scaled(src, s, FILL_DISABLED)
    r, g, b, a = dis.split()
    gray = ImageOps.grayscale(dis).split()[0]
    dis = Image.merge("RGBA", (gray, gray, gray, a))
    dis = ImageEnhance.Brightness(dis).enhance(0.70)

    return [normal, hi, pressed, dis]


def main():
    assert FILL_HOVER > FILL_NORMAL > FILL_PRESSED, "尺寸顺序错误"
    print(f"Ratios: normal={FILL_NORMAL:.3f} hover={FILL_HOVER:.3f} pressed={FILL_PRESSED:.3f}")
    for src_name, prefix in SOURCES:
        path = os.path.join(BASE, src_name)
        if not os.path.isfile(path):
            print("SKIP", path)
            continue
        for i, state in enumerate(make_states(path), start=1):
            out = os.path.join(BASE, f"{prefix}_{i}.png")
            state.save(out, "PNG")
            print("WROTE", out)


if __name__ == "__main__":
    main()

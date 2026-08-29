"""将素材图按目标宽高比居中裁剪并缩放，保证 PPT 中不变形、画幅统一。"""
from PIL import Image
import os

SRC = "assets"
DST = "assets2"
os.makedirs(DST, exist_ok=True)

# 名称 -> (目标宽高比 w/h, 输出宽度像素)
TARGETS = {
    "cover":      (1.778, 1920),   # 封面满幅 16:9
    "cover_split":(1.04,  1600),   # 封面分屏右侧图
    "study":      (0.92,  1100),   # 右侧竖版面板
    "swim":       (1.78,  1400),   # 卡片横向图
    "housework":  (1.78,  1400),
    "bookstore":  (1.12,  1300),   # 左侧横向面板
    "danxia":     (1.333, 1000),   # 旅行四联 4:3
    "mogao":      (1.333, 1000),
    "greatwall":  (1.333, 1000),
    "terracotta": (1.333, 1000),
    "ending":     (1.778, 1920),   # 结尾满幅
}

def center_crop(im, aspect):
    w, h = im.size
    target = aspect
    if w / h > target:
        # 太宽，裁左右
        new_w = int(h * target)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    else:
        # 太高，裁上下（略偏上，保留主体）
        new_h = int(w / target)
        top = int((h - new_h) * 0.4)
        return im.crop((0, top, w, top + new_h))

SRC_MAP = {"cover_split": "cover"}

for name, (aspect, out_w) in TARGETS.items():
    src_name = SRC_MAP.get(name, name)
    src = os.path.join(SRC, src_name + ".jpg")
    if not os.path.exists(src):
        print("missing", src); continue
    im = Image.open(src).convert("RGB")
    im = center_crop(im, aspect)
    out_h = int(round(out_w / aspect))
    im = im.resize((out_w, out_h), Image.LANCZOS)
    dst = os.path.join(DST, name + ".jpg")
    im.save(dst, "JPEG", quality=88, optimize=True)
    print(f"{name}: {im.size} -> {dst} ({os.path.getsize(dst)//1024} KB)")

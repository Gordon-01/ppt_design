"""按与 build2.py 相同的坐标，用 PIL 渲染预览图，用于自查版式。"""
from PIL import Image, ImageDraw, ImageFont
import os

S = 75  # px per inch
W, H = int(13.333 * S), int(7.5 * S)
A = "assets2"
FONT_R = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"

BG   = (255, 253, 249)
TEXT = (43, 52, 64)
MUTED = (138, 147, 160)
LINE = (232, 234, 238)
WHITE = (255, 255, 255)
BLUE = (79, 168, 232)
CORAL = (255, 138, 122)
LAV = (179, 157, 219)
SUN = (255, 184, 77)
MINT = (95, 207, 168)


def px(v):
    return int(round(v * S))


def f(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, max(8, int(size * S / 72 * 96 / 96 * 1.0)))


def rrect(d, box, fill, radius=0.1, outline=None, width=1):
    x0, y0, x1, y1 = box
    r = int(min(x1 - x0, y1 - y0) * radius) if radius else 0
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill,
                        outline=outline, width=width)


def paste_img(canvas, path, box, radius=0.1):
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    im = Image.open(path).convert("RGB").resize((w, h), Image.LANCZOS)
    r = int(min(w, h) * radius)
    if r > 0:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
        canvas.paste(im, (x0, y0), mask)
    else:
        canvas.paste(im, (x0, y0))


def text(d, box, s, size, bold=False, color=TEXT, align="left", anchor="top"):
    x0, y0, x1, y1 = [int(v) for v in box]
    font = f(size, bold)
    lines = s.split("\n") if isinstance(s, str) else s
    th = sum(d.textbbox((0, 0), ln, font=font)[3] - d.textbbox((0, 0), ln, font=font)[1] + 4
             for ln in lines)
    if anchor == "middle":
        y = y0 + (y1 - y0 - th) // 2
    else:
        y = y0
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        tw = bb[2] - bb[0]
        if align == "center":
            x = x0 + (x1 - x0 - tw) // 2
        elif align == "right":
            x = x1 - tw
        else:
            x = x0
        d.text((x, y), ln, font=font, fill=color)
        y += bb[3] - bb[1] + 4


def header(d, num, title, accent):
    rrect(d, (px(0.75), px(0.52), px(0.75 + 0.78), px(0.52 + 0.78)), accent, 0.22)
    text(d, (px(0.75), px(0.52), px(1.53), px(1.30)), num, 24, True, WHITE, "center", "middle")
    text(d, (px(1.72), px(0.49), px(8.7), px(1.30)), title, 34, True, TEXT, "left", "middle")
    d.rectangle([px(0.75), px(1.55), px(12.583), px(1.55) + 1], fill=LINE)


def footer(d, page):
    text(d, (px(11.383), px(6.95), px(12.583), px(7.27)), f"{page} / 6", 11, False, MUTED, "right")
    text(d, (px(0.75), px(6.95), px(5.75), px(7.27)), "我的暑假生活", 11, False, MUTED)


def bullet_cards(d, items, x, y, w, accent, ch=1.02, gap=0.2, size=17):
    for i, line in enumerate(items):
        top = y + i * (ch + gap)
        # shadow
        rrect(d, (px(x), px(top + 0.03), px(x + w), px(top + ch + 0.06)), (223, 226, 231), 0.16)
        rrect(d, (px(x), px(top), px(x + w), px(top + ch)), WHITE, 0.16)
        rrect(d, (px(x + 0.2), px(top + 0.24), px(x + 0.29), px(top + ch - 0.24)), accent, 0.5)
        text(d, (px(x + 0.5), px(top), px(x + w - 0.2), px(top + ch)), line, size, False, TEXT,
             "left", "middle")


slides = []

# ---------- 1 封面 ----------
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
LEFT_W = 5.4
rrect(d, (0, 0, px(LEFT_W), H), (255, 246, 232), 0)
paste_img(c, f"{A}/cover_split.jpg", (px(LEFT_W), 0, W, H), 0)
rrect(d, (px(0.95), px(2.35), px(2.0), px(2.48)), SUN, 0.5)
text(d, (px(0.95), px(2.62), px(5.15), px(3.87)), "我的暑假生活", 62, True, TEXT)
text(d, (px(0.98), px(4.0), px(5.18), px(4.55)), "姓名：XXX        班级：X年X班", 24, False, TEXT)
rrect(d, (px(0.95), px(4.85), px(3.6), px(5.43)), SUN, 0.3)
text(d, (px(0.95), px(4.85), px(3.6), px(5.43)), "2026 · 暑期生活分享", 15, True, TEXT, "center", "middle")
slides.append(c)

# ---------- 2 自律学习 ----------
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
header(d, "01", "自律学习", BLUE)
bullet_cards(d, ["制定暑假学习计划，劳逸结合", "每天认真完成假期作业",
                 "坚持阅读课外书，完成阅读集章卡任务", "每天练字，让字迹更工整"],
             0.75, 1.95, 6.55, BLUE)
paste_img(c, f"{A}/study.jpg", (px(7.98), px(1.85), px(12.58), px(6.85)), 0.09)
rrect(d, (px(7.78), px(6.62), px(9.48), px(6.76)), SUN, 0.5)
footer(d, 2); slides.append(c)

# ---------- 3 锻炼与新本领 ----------
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
header(d, "02", "锻炼与新本领", CORAL)
cards = [(f"{A}/swim.jpg", CORAL, "游泳小健将",
          ["坚持每天体育锻炼", "学会自由泳和跳水", "挑战自己，变得更勇敢"]),
         (f"{A}/housework.jpg", MINT, "家务小帮手",
          ["主动帮爸爸妈妈做家务", "学会整理、打扫和简单烹饪", "懂得劳动的意义，更有担当"])]
for i, (img, accent, title, bullets) in enumerate(cards):
    cx = 0.75 + i * (5.61 + 0.613)
    rrect(d, (px(cx), px(1.88), px(cx + 5.61), px(1.85 + 4.95 + 0.06)), (223, 226, 231), 0.075)
    rrect(d, (px(cx), px(1.85), px(cx + 5.61), px(1.85 + 4.95)), WHITE, 0.075)
    paste_img(c, img, (px(cx + 0.16), px(2.01), px(cx + 0.16 + 5.29), px(2.01 + 2.97)), 0.06)
    rrect(d, (px(cx + 0.34), px(2.01 + 2.97 - 0.62), px(cx + 0.34 + 2.5), px(2.01 + 2.97 - 0.16)), accent, 0.22)
    text(d, (px(cx + 0.34), px(2.01 + 2.97 - 0.62), px(cx + 0.34 + 2.5), px(2.01 + 2.97 - 0.16)),
         title, 17, True, WHITE, "center", "middle")
    for j, b in enumerate(bullets):
        by = 2.01 + 2.97 + 0.34 + j * 0.45
        rrect(d, (px(cx + 0.34), px(by + 0.11), px(cx + 0.5), px(by + 0.27)), accent, 0.5)
        text(d, (px(cx + 0.62), px(by), px(cx + 5.61 - 0.28), px(by + 0.42)), b, 15, False, TEXT,
             "left", "middle")
footer(d, 3); slides.append(c)

# ---------- 4 社会实践 ----------
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
header(d, "03", "社会实践", LAV)
paste_img(c, f"{A}/bookstore.jpg", (px(0.75), px(1.85), px(6.35), px(6.85)), 0.09)
rrect(d, (px(1.0), px(6.62), px(2.7), px(6.76)), LAV, 0.5)
bullet_cards(d, ["在新华书店体验一周小店员", "整理书架、接待读者，体会工作的辛苦",
                 "参加两期阅读公益讲堂", "学到许多书本以外的知识"], 6.9, 1.95, 5.68, LAV, size=16)
footer(d, 4); slides.append(c)

# ---------- 5 快乐旅行 ----------
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
header(d, "04", "快乐旅行", SUN)
text(d, (px(0.75), px(1.78), px(10.75), px(2.18)),
     "和妈妈一起游览河西走廊与西安，欣赏祖国美景与悠久历史文化。", 19, False, TEXT)
for i, (fn, label) in enumerate([("danxia.jpg", "七彩丹霞"), ("mogao.jpg", "莫高窟"),
                                 ("greatwall.jpg", "长城"), ("terracotta.jpg", "兵马俑")]):
    cx = 0.75 + i * (2.70 + 0.343)
    paste_img(c, f"{A}/{fn}", (px(cx), px(2.35), px(cx + 2.70), px(2.35 + 2.025)), 0.07)
    text(d, (px(cx), px(2.35 + 2.025 + 0.16), px(cx + 2.70), px(2.35 + 2.025 + 0.51)),
         label, 17, True, TEXT, "center")
rrect(d, (px(0.75), px(5.35), px(12.583), px(6.27)), (255, 246, 229), 0.12)
text(d, (px(1.15), px(5.35), px(12.18), px(6.27)),
     "读万卷书，行万里路——这次旅行让我看到祖国的壮美，也感受到历史的厚重。",
     18, False, TEXT, "center", "middle")
footer(d, 5); slides.append(c)

# ---------- 6 结尾 ----------
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
paste_img(c, f"{A}/ending.jpg", (0, 0, W, H), 0)
ov = Image.new("RGBA", (W, H), (255, 255, 255, 102)); c = Image.alpha_composite(c.convert("RGBA"), ov).convert("RGB")
d = ImageDraw.Draw(c)
cw, ch = 8.6, 5.45
cx, cy = (13.333 - cw) / 2, 1.0
rrect(d, (px(cx), px(cy + 0.06), px(cx + cw), px(cy + ch + 0.12)), (223, 226, 231), 0.055)
rrect(d, (px(cx), px(cy), px(cx + cw), px(cy + ch)), WHITE, 0.055)
text(d, (px(cx), px(cy + 0.4), px(cx + cw), px(cy + 1.25)), "我的收获", 42, True, TEXT, "center")
rrect(d, (px((13.333 - 1.2) / 2), px(cy + 1.32), px((13.333 + 1.2) / 2), px(cy + 1.42)), SUN, 0.5)
for i, (col, line) in enumerate([(MINT, "知识 · 阅读与旅行，让我看到更大的世界"),
                                 (CORAL, "勇气 · 游泳和跳水，让我敢于挑战自己"),
                                 (BLUE, "成长 · 劳动与实践，让我学会担当")]):
    ry = cy + 1.72 + i * 0.62
    rrect(d, (px(cx + 1.35), px(ry + 0.1), px(cx + 1.53), px(ry + 0.28)), col, 0.5)
    text(d, (px(cx + 1.72), px(ry), px(cx + cw - 1.28), px(ry + 0.38)), line, 21, False, TEXT,
         "left", "middle")
d.rectangle([px(cx + 1.35), px(cy + 3.62), px(cx + cw - 1.35), px(cy + 3.62) + 1], fill=LINE)
text(d, (px(cx), px(cy + 3.82), px(cx + cw), px(cy + 4.37)),
     "新学期，我会继续努力，做更好的自己！", 24, True, TEXT, "center")
text(d, (px(cx), px(cy + 4.4), px(cx + cw), px(cy + 5.3)), "谢谢大家！", 52, True, CORAL, "center")
footer(d, 6); slides.append(c)

# ---------- 拼接触点表 ----------
tw, th = W, H
grid = Image.new("RGB", (tw * 2, th * 3), (240, 240, 240))
for i, sl in enumerate(slides):
    col, row = i % 2, i // 2
    grid.paste(sl, (col * tw, row * th))
grid = grid.resize((tw * 2 // 2, th * 3 // 2), Image.LANCZOS)
grid.save("preview_grid.png")
print("saved preview_grid.png", grid.size)

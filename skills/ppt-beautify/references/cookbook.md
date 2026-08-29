# Cookbook — 实证代码片段

> 全部片段在真实项目（2026-08，21页企业PPT，Windows + Office + Git Bash）中实际运行通过。
> 环境假设：`python` = scoop 安装的 CPython（装了 python-pptx、pywin32）；shell 是 Git Bash。
> ⚠️ 本机有多个 python（msys mingw64 的 python 没有 pip），用 `C:/Users/admin/scoop/apps/python/current/python.exe` 显式指定最稳。

## 1. 渲染（验收的唯一手段）

```python
import win32com.client, os
app = win32com.client.Dispatch('PowerPoint.Application')
pres = app.Presentations.Open(os.path.abspath('副本.pptx'), WithWindow=False)
for i in (12, 13):                       # 1-based 页码
    pres.Slides(i).Export(os.path.abspath(f'_render/s{i}.png'), 'PNG', 1600, 900)
pres.Close(); app.Quit()
```

- `WithWindow=False` 不抢用户屏幕。
- 用 Read 工具直接看 PNG；这是发现残影、溢出、误删的唯一途径。

## 2. 形状清单（含 GROUP 递归）

```python
from pptx import Presentation
from pptx.util import Emu
p = Presentation('副本.pptx')
def walk(shapes, ind=''):
    for s in shapes:
        t = s.text_frame.text if s.has_text_frame else ''
        print(f'{ind}id={s.shape_id} type={str(s.shape_type)[:14]} name={s.name!r} '
              f'pos=({Emu(s.left).inches:.2f},{Emu(s.top).inches:.2f}) '
              f'size=({Emu(s.width).inches:.2f}x{Emu(s.height).inches:.2f}) text={t[:100]!r}')
        if s.shape_type == 6: walk(s.shapes, ind + '  ')
walk(p.slides[11].shapes)
```

## 3. 图形识别（正确姿势）

```python
from pptx.oxml.ns import qn
def geom(shape):
    g = shape._element.spPr.find(qn('a:prstGeom'))
    return g.get('prst') if g is not None else None
# geom(s) -> 'rect' / 'roundRect' / 'chevron' / 'triangle' / None(自定义freeform)

def fill_rgb(s):
    try:
        return str(s.fill.fore_color.rgb) if s.fill.type == 1 else None
    except Exception:
        return None
```

**坑**：`shape.shape_type` 返回 `MSO_SHAPE_TYPE`（如 AUTO_SHAPE=1），不是图形种类。
`if s.shape_type == MSO_SHAPE.CHEVRON` 永远为假且不报错——本项目静默失败过两次。

## 4. 删除形状

```python
s._element.getparent().remove(s._element)   # 传 element，别传 shape 本身（踩过 TypeError）
```

批量清理按签名匹配，且**禁止裸 except 吞异常**；清完 dump 清单核对数量：

```python
for s in list(slide.shapes):
    g, f = geom(s), fill_rgb(s)
    if g == 'rect' and f == 'FFFFFF' and s.has_text_frame and s.text_frame.text.strip():
        ...  # 例：旧版"带文字的白卡"
```

## 5. 白卡 + 阴影

```python
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from lxml import etree

SHADOW = ('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
          '<a:outerShdw blurRad="90000" dist="25400" dir="5400000" rotWithShape="0">'
          '<a:srgbClr val="000000"><a:alpha val="12000"/></a:srgbClr></a:outerShdw></a:effectLst>')

def card(slide, x, y, w, h):   # 单位: 英寸
    c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    c.line.fill.background()          # 去边框；同理可去掉继承的主题描边
    c.shadow.inherit = False          # 掐掉继承阴影，再用 XML 注入自己的
    c._element.spPr.append(etree.fromstring(SHADOW))
    return c
```

## 6. 角标数字块 / 竖分隔线 / 文本框

```python
def chip(slide, x, y, n):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(0.42), Inches(0.42))
    c.adjustments[0] = 0.22
    c.fill.solid(); c.fill.fore_color.rgb = RED        # 品牌色
    c.line.fill.background(); c.shadow.inherit = False
    tf = c.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n)
    r.font.name = '微软雅黑'; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = WHITE

def hairline(slide, x, y, h):   # 竖分隔线：1px 矩形比 connector 稳
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.014), Inches(h))
    ln.fill.solid(); ln.fill.fore_color.rgb = RGBColor(0xE8, 0xE8, 0xE8)
    ln.line.fill.background(); ln.shadow.inherit = False

def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.MIDDLE):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf
```

## 7. 建议条目行卡（角标｜标题｜竖线｜正文）

```python
def row_card(slide, x, y, w, h, n, title, body, t_size=15, b_size=14):
    card(slide, x, y, w, h)
    chip(slide, x + 0.2, y + (h - 0.42) / 2, n)
    tf = textbox(slide, x + 0.78, y + 0.05, 1.42, h - 0.1)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = title
    r.font.name = '微软雅黑'; r.font.size = Pt(t_size); r.font.bold = True; r.font.color.rgb = RED
    hairline(slide, x + 2.32, y + 0.18, h - 0.36)
    tf = textbox(slide, x + 2.56, y + 0.1, w - 2.81, h - 0.2)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = body
    r.font.name = '微软雅黑'; r.font.size = Pt(b_size); r.font.color.rgb = DARK   # 404040
    p.line_spacing = 1.2          # p.alignment 默认居中，正文必须显式 LEFT
```

带红色加粗引导词的多段正文（用于"问题清单：xxx"类内容）：

```python
for lead, text in paras:               # lead 如 '问题清单：'，可为 None
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    first = False
    p.line_spacing = 1.25; p.space_after = Pt(6)
    if lead: run(p, lead, 14, True, RED)
    run(p, text, 14, False, DARK)
```

## 8. 问题点卡（模板母题做标记）

```python
def q_card(slide, y, h, body):
    card(slide, 0.45, y, 10.74, h)
    tri = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,      # 注意拼写 ISOSCELES
        Inches(0.76), Inches(y + (h - 0.34) / 2), Inches(0.3), Inches(0.34))
    tri.rotation = 90                                               # 指向右
    tri.fill.solid(); tri.fill.fore_color.rgb = RED
    tri.line.fill.background(); tri.shadow.inherit = False
    tf = textbox(slide, 1.32, y + 0.1, 9.55, h - 0.2)
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = body
    r.font.name = '微软雅黑'; r.font.size = Pt(14); r.font.color.rgb = DARK
    p.line_spacing = 1.25
```

## 9. 重写"问题点：\n正文" 文本框（保留标签行）

```python
for s in slide.shapes:
    if s.shape_id == 7:
        tf = s.text_frame
        body = '\n'.join(p.text for p in tf.paragraphs[1:]).strip()   # 先取文
        for p in list(tf.paragraphs[1:]):                             # 再删段
            p._p.getparent().remove(p._p)
        s.height = Inches(0.45)
```

**教训**：先取文、再删形。本项目曾把某页正文删了没接住，最后从原始文件原样取回。

## 10. 保存（应对 PowerPoint 文件锁）

```bash
python build.py            # 脚本里 prs.save('_work.pptx')，存临时文件
for i in 1 2 3 4 5 6; do
  if mv -f _work.pptx "目标.pptx" 2>/dev/null; then echo replaced; break; fi
  echo locked; sleep 10
done
```

- 目录出现 `~$xxx.pptx` = 用户开着文件。不要杀 POWERPNT（可能开着用户的原始文件）。
- 另注意同步盘会把文件置只读：`chmod +w` 再写。

## 11. 文字/颜色/字体的取证

```python
for para in shape.text_frame.paragraphs:
    for r in para.runs:
        try: c = r.font.color.rgb
        except: c = r.font.color.type
        print(repr(r.text[:20]), r.font.name, r.font.size, r.font.bold, c)
# 品牌色看标题字/标题条 fill；正文色、字号以模板继承为准，新元素显式指定
```

## 12. 图片行对齐（图文页）

```python
photos = [...]; H, top, x0, w_total = 1.9, 3.72, 0.45, 10.74
sizes = [H * ph.width / ph.height for ph in photos]   # 等高、保纵横比
gap = (w_total - sum(sizes)) / (len(photos) - 1)
x = x0
for ph, w in zip(photos, sizes):
    ph.left = Inches(x); ph.top = Inches(top); ph.width = Inches(w); ph.height = Inches(H)
    ph.line.color.rgb = RGBColor(0xD9, 0xD9, 0xD9); ph.line.width = Pt(1)  # 细灰描边
    x += w + gap
```

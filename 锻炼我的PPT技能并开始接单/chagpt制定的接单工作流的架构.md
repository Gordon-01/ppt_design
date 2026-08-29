# Personal PPT Production Workflow

## 个人 PPT 接单 AI 生产工作流 —— Codex 第一阶段讨论任务

### 一、项目定位

我要搭建的不是一个单独的 PPT Skill，也不是一个简单的 AI PPT 生成器。

我要搭建的是一个长期服务于我个人 PPT 接单业务的：

# **Personal PPT Production Workflow**

# **个人 PPT 接单 AI 生产工作流**

目标是：

> 将 PPT 接单过程中大量重复、机械、繁琐、耗时的工作交给 AI Agent 自动完成；我本人只负责真正需要人工判断和创意的部分，包括审美决策、关键页面、复杂动画、客户特殊要求和最终精修。

因此：

**Workflow 是核心。**

Skill、脚本、工具、模型、模板、设计资产、PPT 引擎、OCR、图片生成、动画引擎等，都只是 Workflow 的组成部分。

不要把整个项目设计成“一个巨大 Skill”。

---

# 二、理想工作模式

理想状态：

```text id="q1k8z6"
客户订单
    ↓
项目初始化
    ↓
素材收集
    ↓
内容解析
    ↓
OCR / 文件转换
    ↓
内容结构化
    ↓
PPT 页面规划
    ↓
文字编排
    ↓
页面布局
    ↓
视觉设计
    ↓
图片 / 素材处理
    ↓
生成可编辑 PPTX
    ↓
自动基础动画
    ↓
自动 QA
    ↓
生成预览
    ↓
人工精修
    ↓
最终交付
```

核心思想：

> **AI 完成大部分重复劳动，人类负责最后的专业判断。**

---

# 三、AI 和人工的职责边界

## AI 负责

AI 尽可能自动完成：

* PDF 解析
* Word 解析
* PPT 解析
* Excel 内容提取
* 图片 OCR
* 图片中文字识别
* 内容整理
* 文字结构化
* 标题 / 正文 / 强调内容识别
* 自动文字编排
* 页面类型识别
* 页面布局
* PPT 元素定位
* 图片选择
* AI 图片生成
* 页面视觉设计
* PPTX 构建
* 基础图形绘制
* 基础流程图
* 基础表格
* 基础图表
* 基础动画
* 动画顺序设计
* 动画窗格基础构建
* PPT 渲染
* 页面视觉检查
* 内容溢出检查
* 元素重叠检查
* 基础质量控制

## 人工负责

我主要负责：

* 最终审美判断
* 创意设计
* 重点页面重新设计
* 特殊排版
* 复杂动画
* Morph
* 高级 Motion Path
* 复杂 Trigger
* 高级转场
* 客户定制要求
* 最终视觉精修
* 最终交付审核

系统不能追求“100% 不需要人工”。

目标是：

> **AI 做到约 70%～85%，人类完成剩余 15%～30%。**

---

# 四、最重要的产品原则

## 1. 最终必须输出真正可编辑的 PPTX

不能简单把整页设计稿作为一张图片放进 PPT。

尽可能使用：

```text
Text Box
Shape
Line
Connector
Table
Chart
Image
```

作为原生 PowerPoint 元素。

最终我必须可以在 PowerPoint 中：

* 改文字
* 改字号
* 改颜色
* 拖动元素
* 改图形
* 修改图片
* 修改动画
* 删除元素
* 增加元素

---

# 五、关于 AI 图片设计

允许采用：

```text id="2h7r0w"
原始内容
    ↓
AI 设计页面
    ↓
生成视觉设计参考图
    ↓
根据参考图重新构建 PPT
```

但是：

**视觉参考图不是最终 PPT。**

视觉图主要负责：

> 告诉 PPT Builder 这一页应该长什么样。

最终 PPT 必须重新由可编辑元素构建。

---

# 六、关于文字

文字是一个重要资产。

如果用户要求保持原文：

* 不允许擅自改写
* 不允许总结
* 不允许删除
* 不允许增加
* 不允许改变原意

应当将：

```text
Original Content
```

和：

```text
Design / Layout
```

分离。

也就是说：

```text
Content Layer
+
Design Layer
```

不能把二者混为一体。

这样未来可以：

> 不改变内容，只重新排版。

---

# 七、关于动画

动画不是项目的第一优先级，但必须从架构层面预留。

动画采用：

> **AI 自动完成基础动画 + 人工完成复杂动画**

AI 可以自动：

* Fade
* Appear
* Wipe
* Fly In
* Zoom
* 基础 Emphasis
* 基础 Exit
* 基础顺序
* On Click
* With Previous
* After Previous
* Duration
* Delay

复杂动画交给人工。

最终需要支持：

```text
PPTX
+
Animation Plan
+
Animation Engine
```

动画必须尽量与 PPT 页面结构解耦。

---

# 八、Workflow 不是 Skill 集合

这是本项目非常重要的架构原则。

不要设计成：

```text
一个巨大 SKILL.md
```

或者简单做成：

```text
skill A
skill B
skill C
skill D
```

而应该设计成真正的：

# Workflow System

例如：

```text
Workflow Orchestrator
        │
        ├── Intake
        ├── Extraction
        ├── OCR
        ├── Content
        ├── Layout
        ├── Design
        ├── Image
        ├── PPTX Build
        ├── Animation
        ├── QA
        └── Delivery
```

每一个模块可以使用：

* Skill
* Python
* JavaScript
* CLI
* 第三方库
* 外部 AI
* MCP
* API
* 本地程序

但上层由 Workflow 统一编排。

---

# 九、Workflow 应该具备“阶段状态”

一个订单不应该只是一次性执行完。

应该存在类似：

```text
project/
    state/
        intake.json
        content.json
        design.json
        build.json
        animation.json
        qa.json
```

这样允许：

> 中途暂停 → 人工修改 → 继续执行。

也允许：

> 只重新执行某一个阶段。

例如：

```text
重新做第 5 页布局

而不是：

从头重新生成整个 PPT
```

---

# 十、Workflow 必须支持局部重跑

这是商业接单非常重要的能力。

例如我觉得：

> 第 6 页不好看。

我不应该重新生成整套 PPT。

应该：

```text
project
 ↓
slide 6
 ↓
重新设计
 ↓
重新构建
 ↓
重新 QA
```

类似：

```text
rerun slide 6
rerun layout
rerun animation
rerun OCR
rerun QA
```

---

# 十一、必须考虑“人工接管”

Workflow 中应该允许明确的 Human Checkpoint。

例如：

```text
内容解析
↓
[人工确认]
↓
页面设计
↓
[人工确认]
↓
PPT 构建
↓
自动动画
↓
[人工精修]
↓
交付
```

AI 不能默认一路自动执行到底。

---

# 十二、项目资产库

这个系统长期使用后，需要积累自己的资产。

包括：

```text
Templates
Layouts
Components
Styles
Color Systems
Typography
Icons
Images
Animation Patterns
Reference Slides
Client Examples
```

这些资产应该逐渐形成：

# **Personal PPT Design Library**

以后 AI 的设计能力不仅来自模型本身，还来自：

> 我过去做过什么，以及我最终修改成什么样。

---

# 十三、最终希望形成“反馈闭环”

未来可以形成：

```text
AI 生成
    ↓
我修改
    ↓
保留最终版本
    ↓
分析修改内容
    ↓
沉淀为：
Layout
Style
Animation
Component
Preference
    ↓
下一次 AI 更接近我的审美
```

这比单纯安装 Skill 更重要。

长期目标是：

> **让 AI 越来越像我的私人 PPT 助手。**

---

# 十四、当前阶段：只做 Repository Audit

我现在准备使用这个项目作为基础：

https://github.com/Gordon-01/ppt_design

但是当前不要直接开始大规模开发。

第一步先完整审查这个仓库。

---

# 十五、Repository Audit 要回答的问题

请完整检查这个仓库：

### A. 项目定位

* 这个项目到底解决什么问题？
* 当前核心工作流是什么？
* 它更接近 Skill、工具还是完整 Workflow？

### B. 当前技术栈

* 使用什么语言？
* 使用什么 PPT 引擎？
* 使用什么模型？
* 如何生成 PPTX？
* 如何解析 PPT？
* 如何渲染 PPT？
* 是否支持 OCR？
* 是否支持图片生成？
* 是否支持动画？

### C. 可以直接复用的能力

例如：

* PPTX Builder
* Layout Engine
* Rendering
* Design System
* Prompt
* Skill
* Utility
* Template
* Asset system

### D. 当前不足

和本项目目标对比：

```text
目标
VS
现有能力
```

找出 Gap。

---

# 十六、Architecture Review

完成仓库分析后，请提出一个新的架构方案。

重点回答：

> **这个仓库应该作为整个 Workflow 的基础、某一个模块的基础，还是只适合参考其中部分能力？**

不要因为我选择了这个仓库，就默认必须全部基于它开发。

如果有更合理的技术方案，应明确提出。

---

# 十七、第一阶段输出文件

当前阶段只生成：

```text
docs/
    repository-audit.md
    workflow-architecture.md
    gap-analysis.md
    implementation-roadmap.md
```

其中：

### repository-audit.md

说明当前仓库有什么。

### workflow-architecture.md

说明未来整个 Personal PPT Production Workflow 应该怎么设计。

### gap-analysis.md

说明现有项目和目标之间缺什么。

### implementation-roadmap.md

说明未来应该按照什么顺序建设。

---

# 十八、当前阶段禁止做的事情

当前不要：

* 大规模重构
* 直接删除原有代码
* 直接重写项目
* 开发 Web UI
* 做数据库
* 做客户管理后台
* 做商业化 SaaS
* 为了实现功能而擅自改变项目定位

第一阶段的重点是：

> **理解现有系统 + 明确目标 Workflow + 找到最合理的技术路线。**

---

# 十九、最终目标

未来我希望达到：

```text
客户发来资料
      ↓
我创建项目
      ↓
Agent 执行 Workflow
      ↓
AI 自动完成：
OCR
内容整理
文字编排
页面布局
图片
视觉设计
PPT 构建
基础动画
QA
      ↓
我打开 PPT
      ↓
人工精修
      ↓
客户交付
```

核心目标不是：

> “让 AI 完全替代 PPT 设计师。”

而是：

# **让 AI 接管重复劳动，让我把时间集中在真正有价值的设计工作上。**

最终形成一个：

> **可长期使用、可迭代、可积累资产、支持人工接管、支持局部重跑的个人 PPT 接单生产工作流。**

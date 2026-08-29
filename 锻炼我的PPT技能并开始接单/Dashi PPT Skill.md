这个Skill技能，可在线生成PPT 还能实时修改
👇关注公众号👇发送“Dashi PPT Skill”下载项目源码
今天在 GitHub 上看到一个很不错得开源项目，叫 Dashi PPT Skill。

它是一套给 Claude Code、Codex 这类 AI Agent 用的 PPT Skill。

图片
你可以把文档丢给 AI Agent，每一页都会生成一个可编辑的网页版 PPT。

在浏览器里打开 PPT，每页文字能点开改，图片能替换，布局、模块数量、配色也能调。

比如你手里有一份行业研究文档。

你把主题、受众、页数、想突出的结论告诉 Agent，它会先让你选 12 套视觉主题里的一个，然后自动组稿，生成一套结构完整的演示文稿。

图片
生成之后如果不满意，你可以直接在页面上改字、换图、拖滑调整页面结构。

它把 AI 生成 PPT 这件事，从一次性出图，往可继续编辑的工作文件推了一步。

这个工具把 AI 生成 PPT 这件事，从一次性出图，往可继续编辑的工作文件推了一步。

这点对职场人很实际。

因为 PPT 最麻烦的地方，往往不是第一页生成出来，而是后面那十几轮的微调。

怎么使用？
项目地址：

https://github.com/chuspeeism/dashi-ppt-skill

一键安装 / 更新：

npx dashi-ppt-skill@latest
国内网络：

npx --registry=https://registry.npmmirror.com dashi-ppt-skill@latest
环境要求：

Node.js 20+ 和 npm；导出 PPTX / PDF 需要本机装有 Chrome / Chromium / Edge。
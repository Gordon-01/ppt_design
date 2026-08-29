推荐一个能把Word、PPT、PDF变成Markdown的开源项目
👇关注公众号👇发送“anydoc”下载项目源码
最近看到 GitHub 上开源了一个很有意思的项目，叫 anydoc。

它是一套 Rust 文档转换库。

图片
简单说，就是把 Word、PPT、Excel、OpenDocument、RTF、EPUB、CSV、PDF 这些文件，转成干净的 Markdown 文档。

比如你手里有一个doc文档，想先变成适合 AI 读取和处理的文本。

你可以直接运行：

npx @firecrawl/anydoc report.docx
它就会把文档内容输出成 Markdown。

如果想保存成文件，也可以输出到 report.md。

这个工具我感觉还挺实用的。

它不是只支持某一种文档，而是把一堆常见办公格式统一成一种结构化输出。

图片
对做知识库、RAG、Agent 文档读取，或者只是想把旧 Office 文件整理成 Markdown 的人来说，会省掉不少精力。

另外它还提供 Node、Python 和浏览器 WebAssembly 版本。

怎么使用？
项目地址：

https://github.com/firecrawl/anydoc

浏览器 Demo：

https://firecrawl.github.io/anydoc/

CLI：

npx @firecrawl/anydoc report.docx npx @firecrawl/anydoc slides.pptx -o slides.md
Python：

pip install firecrawl-anydoc
Node.js：

npm install @firecrawl/anydoc
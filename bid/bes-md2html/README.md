# md2html

将现有 Markdown 快速转换为轻量、响应式、可打印的单文件 HTML。

## 特点

- 一个专业的自适应默认模板，不生成多套 CSS
- 单文件 HTML，无网络依赖
- 保留标题、列表、链接、表格和代码块
- 保留一级标题作为文档总标题
- 自动生成二级标题锚点与左侧章节导航
- 表格按内容自然分配列宽，列较多时使用独立横向滚动区域
- 支持系统深浅配色、移动端导航和打印排版
- HTML 始终输出到源 Markdown 同目录
- 支持按需添加多级目录、代码高亮或品牌样式

## 使用

对 Agent 说：

> 把 `report.md` 转成 HTML

也可以直接运行：

```bash
python scripts/convert.py report.md
```

自定义输出文件名（仍生成在源 Markdown 所在目录）：

```bash
python scripts/convert.py docs/report.md custom-report.html
```

以上命令会生成 `docs/custom-report.html`。脚本会拒绝输出到其他目录。

脚本支持 Python `markdown` 或 `markdown2`。若均未安装：

```bash
python -m pip install markdown
```

默认模板位于 `assets/base.html`，详细约定见 `references/conversion.md`。

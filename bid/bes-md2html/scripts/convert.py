#!/usr/bin/env python3
"""Convert a Markdown file to a self-contained HTML document."""

from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def render_markdown(source: str) -> tuple[str, str]:
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            source,
            extensions=["extra", "sane_lists", "toc"],
            output_format="html5",
        ), "markdown"
    except ImportError:
        try:
            import markdown2  # type: ignore

            return markdown2.markdown(
                source,
                extras=[
                    "fenced-code-blocks",
                    "tables",
                    "strike",
                    "task_list",
                    "header-ids",
                ],
            ), "markdown2"
        except ImportError as exc:
            raise RuntimeError(
                "缺少 Markdown 解析器。请运行: python -m pip install markdown"
            ) from exc


def document_title(source: str, source_path: Path) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", source)
    if match:
        return re.sub(r"[*_`~\[\]]", "", match.group(1)).strip()
    return source_path.stem


def _heading_text(fragment: str) -> str:
    parser = _TextExtractor()
    parser.feed(fragment)
    parser.close()
    return " ".join("".join(parser.parts).split())


def _heading_slug(text: str, index: int) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", normalized, flags=re.UNICODE)
    return slug.strip("-") or f"chapter-{index}"


def add_chapter_navigation(body: str) -> tuple[str, str]:
    """Add stable IDs to h2 headings and build the left-side chapter links."""
    headings: list[tuple[str, str]] = []
    used_ids: set[str] = set()
    heading_pattern = re.compile(
        r"<h2(?P<attrs>[^>]*)>(?P<content>.*?)</h2>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    id_pattern = re.compile(r"""\bid\s*=\s*(["'])(.*?)\1""", re.IGNORECASE)

    def replace_heading(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        content = match.group("content")
        label = _heading_text(content) or f"章节 {len(headings) + 1}"
        id_match = id_pattern.search(attrs)
        base_id = (
            html.unescape(id_match.group(2))
            if id_match
            else _heading_slug(label, len(headings) + 1)
        )
        heading_id = base_id
        suffix = 2
        while heading_id in used_ids:
            heading_id = f"{base_id}-{suffix}"
            suffix += 1
        used_ids.add(heading_id)

        if id_match and heading_id == base_id:
            updated_attrs = attrs
        elif id_match:
            updated_attrs = (
                attrs[: id_match.start()]
                + f' id="{html.escape(heading_id, quote=True)}"'
                + attrs[id_match.end() :]
            )
        else:
            updated_attrs = f'{attrs} id="{html.escape(heading_id, quote=True)}"'

        headings.append((heading_id, label))
        return f"<h2{updated_attrs}>{content}</h2>"

    body_with_ids = heading_pattern.sub(replace_heading, body)
    if headings:
        links = "\n".join(
            '        <li><a href="#{}">{}</a></li>'.format(
                html.escape(heading_id, quote=True), html.escape(label)
            )
            for heading_id, label in headings
        )
    else:
        links = '        <li><a href="#document-start">文档开头</a></li>'

    navigation = (
        '  <nav class="chapter-nav" aria-label="二级标题导航">\n'
        '    <div class="chapter-nav__header">\n'
        '      <span class="chapter-nav__mark" aria-hidden="true">目</span>\n'
        "      <div>\n"
        '        <p class="chapter-nav__title">内容导航</p>\n'
        '        <p class="chapter-nav__hint">快速跳转至文档章节</p>\n'
        "      </div>\n"
        "    </div>\n"
        '    <ol>\n'
        f"{links}\n"
        "    </ol>\n"
        "  </nav>"
    )
    return body_with_ids, navigation


def enhance_table_cells(body: str) -> str:
    """Add a two-line content hook and full-text tooltip to table cells."""
    table_pattern = re.compile(
        r"(?P<table><table(?:\s[^>]*)?>.*?</table>)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    cell_pattern = re.compile(
        r"<(?P<tag>th|td)(?P<attrs>[^>]*)>(?P<content>.*?)</(?P=tag)>",
        flags=re.IGNORECASE | re.DOTALL,
    )

    def enhance_table(table_match: re.Match[str]) -> str:
        def enhance_cell(cell_match: re.Match[str]) -> str:
            tag = cell_match.group("tag")
            attrs = cell_match.group("attrs")
            content = cell_match.group("content")
            full_text = _heading_text(content)
            title = (
                f' title="{html.escape(full_text, quote=True)}"' if full_text else ""
            )
            return (
                f"<{tag}{attrs}>"
                f'<div class="table-cell__content"{title}>{content}</div>'
                f"</{tag}>"
            )

        return cell_pattern.sub(enhance_cell, table_match.group("table"))

    return table_pattern.sub(enhance_table, body)


def wrap_tables(body: str) -> str:
    """Wrap generated tables in an accessible horizontal scroll container."""
    table_pattern = re.compile(
        r"(?P<table><table(?:\s[^>]*)?>.*?</table>)",
        flags=re.IGNORECASE | re.DOTALL,
    )
    return table_pattern.sub(
        r'<div class="table-wrap" role="region" aria-label="可横向滚动的数据表格" '
        r'tabindex="0">\g<table></div>',
        body,
    )


def resolve_output_path(source_path: Path, requested_path: Path | None) -> Path:
    """Resolve an HTML output path while keeping it beside the Markdown source."""
    source_path = source_path.resolve()
    if requested_path is None:
        output_path = source_path.with_suffix(".html")
    elif requested_path.parent == Path("."):
        output_path = source_path.parent / requested_path.name
    else:
        output_path = requested_path.resolve()

    output_path = output_path.resolve()
    if output_path.parent != source_path.parent:
        raise ValueError("输出 HTML 必须与源 Markdown 文件位于同一目录")
    if output_path.suffix.lower() != ".html":
        raise ValueError("输出文件扩展名必须是 .html")
    if output_path == source_path:
        raise ValueError("输出路径不能覆盖源 Markdown 文件")
    return output_path


def convert(source_path: Path, output_path: Path) -> tuple[str, int]:
    source_path = source_path.resolve()
    output_path = resolve_output_path(source_path, output_path)
    source = source_path.read_text(encoding="utf-8")
    body, parser_name = render_markdown(source)
    body, navigation = add_chapter_navigation(body)
    body = enhance_table_cells(body)
    body = wrap_tables(body)

    template_path = Path(__file__).resolve().parent.parent / "assets" / "base.html"
    template = template_path.read_text(encoding="utf-8")
    document = template.replace(
        "{{TITLE}}", html.escape(document_title(source, source_path), quote=True)
    ).replace("{{NAV}}", navigation).replace("{{BODY}}", body)

    output_path.write_text(document, encoding="utf-8")
    return parser_name, output_path.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="输入 Markdown 文件")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="可选输出文件名；HTML 始终生成在源 Markdown 所在目录",
    )
    args = parser.parse_args()

    source_path = args.input.resolve()
    if not source_path.is_file():
        parser.error(f"输入文件不存在: {source_path}")
    if source_path.suffix.lower() not in {".md", ".markdown"}:
        parser.error("输入文件必须是 .md 或 .markdown")

    try:
        output_path = resolve_output_path(source_path, args.output)
    except ValueError as exc:
        parser.error(str(exc))

    try:
        parser_name, size = convert(source_path, output_path)
    except (OSError, UnicodeError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"OUTPUT: {output_path}")
    print(f"PARSER: {parser_name}")
    print(f"SIZE: {size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

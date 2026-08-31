import importlib.util
import re
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "convert.py"
SPEC = importlib.util.spec_from_file_location("md2html_convert", MODULE_PATH)
assert SPEC and SPEC.loader
convert = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(convert)


class ChapterNavigationTests(unittest.TestCase):
    def test_builds_links_for_each_h2_and_keeps_unique_ids(self) -> None:
        body = (
            "<h1>文档总标题</h1>"
            "<h2>开始 使用</h2>"
            '<h2 id="custom">高级 <code>配置</code></h2>'
            '<h2 id="custom">重复</h2>'
        )

        updated_body, navigation = convert.add_chapter_navigation(body)

        self.assertIn('id="开始-使用"', updated_body)
        self.assertIn('id="custom"', updated_body)
        self.assertIn('id="custom-2"', updated_body)
        self.assertIn('href="#开始-使用">开始 使用</a>', navigation)
        self.assertIn('href="#custom">高级 配置</a>', navigation)
        self.assertIn('href="#custom-2">重复</a>', navigation)
        self.assertNotIn("文档总标题", navigation)
        self.assertIn('class="chapter-nav__header"', navigation)
        self.assertIn("快速跳转至文档章节", navigation)

    def test_uses_document_start_when_there_are_no_h2_headings(self) -> None:
        body = "<h1>只有文档总标题</h1>"

        updated_body, navigation = convert.add_chapter_navigation(body)

        self.assertEqual(body, updated_body)
        self.assertIn('href="#document-start">文档开头</a>', navigation)


class TableLayoutTests(unittest.TestCase):
    def test_enhances_cells_with_full_text_tooltips(self) -> None:
        body = (
            '<table><tr><th>Heading</th><td>Long <strong>formatted</strong> '
            'text &amp; &quot;quoted&quot;<br>second line<br>third line</td></tr></table>'
        )

        updated_body = convert.enhance_table_cells(body)

        self.assertEqual(2, updated_body.count('class="table-cell__content"'))
        self.assertIn('title="Heading"', updated_body)
        self.assertIn(
            'title="Long formatted text &amp; &quot;quoted&quot;second linethird line"',
            updated_body,
        )
        self.assertIn('<strong>formatted</strong>', updated_body)

    def test_wraps_each_table_in_scrollable_region(self) -> None:
        body = (
            "<p>前文</p>"
            "<table><thead><tr><th>列</th></tr></thead>"
            "<tbody><tr><td>值</td></tr></tbody></table>"
            "<p>中间</p>"
            "<table><tr><td>第二张表</td></tr></table>"
        )

        updated_body = convert.wrap_tables(body)

        self.assertEqual(2, updated_body.count('class="table-wrap"'))
        self.assertEqual(2, updated_body.count('tabindex="0"'))
        self.assertIn("<p>前文</p><div", updated_body)
        self.assertIn("</div><p>中间</p>", updated_body)

    def test_leaves_documents_without_tables_unchanged(self) -> None:
        body = "<h1>没有表格</h1><p>正文</p>"

        self.assertEqual(body, convert.wrap_tables(body))


class GeneratedDocumentTests(unittest.TestCase):
    def test_generated_document_keeps_structure_and_table_layout_contract(self) -> None:
        source_text = """# 总标题

## 数据

| 指标 | 详细说明 |
| --- | --- |
| 转化率 | 这是用于检查可读列宽的说明 |

```python
print("ok")
```
"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "report.md"
            output = Path(temporary_directory) / "report.html"
            source.write_text(source_text, encoding="utf-8")

            convert.convert(source, output)
            document = output.read_text(encoding="utf-8")

        self.assertTrue(document.lower().startswith("<!doctype html>"))
        self.assertTrue(document.rstrip().endswith("</html>"))
        self.assertIn('<main id="document-start">', document)
        heading = re.search(r'<h2 id="([^"]+)">数据</h2>', document)
        self.assertIsNotNone(heading)
        assert heading is not None
        self.assertIn(f'href="#{heading.group(1)}">数据</a>', document)
        self.assertEqual(1, document.count('class="table-wrap"'))
        self.assertEqual(1, document.count("<table>"))
        self.assertEqual(1, document.count("<pre>"))
        self.assertNotIn("{{BODY}}", document)

    def test_template_preserves_readable_columns_and_responsive_navigation(self) -> None:
        template = (
            Path(__file__).resolve().parents[1] / "assets" / "base.html"
        ).read_text(encoding="utf-8")

        self.assertIn(".table-wrap", template)
        self.assertIn("overflow-x: auto", template)
        self.assertIn("grid-template-columns: minmax(14rem, 17rem) minmax(0, 1fr)", template)
        self.assertIn("width: min(100% - 3rem, 1800px)", template)
        self.assertNotIn("width: max-content", template)
        self.assertIn("min-width: 7rem", template)
        self.assertIn("overflow-wrap: anywhere", template)
        self.assertIn("white-space: normal", template)
        self.assertIn(".table-cell__content", template)
        self.assertIn("-webkit-line-clamp: 2", template)
        self.assertIn("text-overflow: ellipsis", template)
        self.assertIn("@media (max-width: 900px)", template)
        self.assertIn("@media print", template)


class OutputPathTests(unittest.TestCase):
    def test_default_output_is_beside_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "report.md"

            output = convert.resolve_output_path(source, None)

            self.assertEqual(source.with_suffix(".html"), output)

    def test_bare_output_name_is_resolved_beside_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "report.md"

            output = convert.resolve_output_path(source, Path("custom.html"))

            self.assertEqual(source.parent / "custom.html", output)

    def test_rejects_output_in_another_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source" / "report.md"
            requested = root / "public" / "report.html"

            with self.assertRaisesRegex(ValueError, "同一目录"):
                convert.resolve_output_path(source, requested)

    def test_rejects_non_html_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "report.md"

            with self.assertRaisesRegex(ValueError, r"\.html"):
                convert.resolve_output_path(source, Path("report.htm"))


if __name__ == "__main__":
    unittest.main()

---
name: bes-document-parsing
description: Parse PDF, Word, Excel, and PowerPoint documents into faithful Markdown, including text, tables, embedded images, layout metadata, OCR results, and extraction warnings. Use when a document must be converted, extracted, OCR-processed, or normalized into Markdown.
---

# Document Parsing

Use the bundled `scripts/parse_documents.py` as the default deterministic entry point. It supports `.pdf`, `.docx/.doc`, `.xlsx/.xls`, `.pptx/.ppt`, and common image files; it emits one Markdown file per input plus a JSON manifest when requested.

图片 OCR 是强制要求，不是可选增强：只要文档包含嵌入图片、扫描页或独立图片文件，就必须对每一张图片执行 OCR，并将结果写入 Markdown。

## Operating rules

1. Inspect inputs and preserve originals. For a directory, process supported files recursively and write into a separate output directory.
2. Run `python scripts/parse_documents.py --check` first. Before parsing any input with possible images, verify that a supported OCR provider is configured and usable. Do not proceed as if parsing were complete when OCR is unavailable.
   Configuration is read first from `config/.env` in this skill directory, then from process/system environment variables: use `OCR_PROVIDER=generic` with `OCR_SERVICE_URL`, `OCR_PROVIDER=pandleocr` with `OCR_SERVICE_URL` (defaulting to the Eoeshop endpoint), or `OCR_PROVIDER=baidu` with `BAIDU_API_KEY` and `BAIDU_SECRET_KEY` (alternatively `BAIDU_ACCESS_TOKEN`). Restart the terminal or host application after changing Windows environment variables. If either source cannot be accessed, report it to the user.
3. Parse with `--backend auto`; use `--backend docling` when layout fidelity matters most.
4. Extract every embedded image to `assets/`, including images in DOCX/PPTX archives and images rendered from scanned PDF pages. Invoke OCR once for every extracted image and every rendered image-only PDF page.
5. Insert a separate `OCR` block for every image, including the image filename plus page/slide/document provenance. Preserve the exact returned OCR text; label uncertain text when the OCR provider reports uncertainty.
6. If OCR is not configured, fails, times out, or returns empty text, record a per-image warning in both Markdown and the manifest, mark the file `partial` (or `failed` when no usable document content remains), and never silently omit the OCR block. Never invent, infer, or manually fabricate OCR text.
7. Preserve tables as Markdown tables, including headers, cell order, merged-cell notes, formulas/displayed values, and page/sheet/slide provenance.
8. Validate page/sheet/slide counts, non-empty expected text, extracted image count, OCR block count, and per-image OCR success. The validation must fail or mark `partial` when `image_count > ocr_block_count`; report per-file failures without hiding partial results.

## Output contract

Each Markdown file starts with:

```markdown
---
source: original filename
format: pdf|docx|xlsx|pptx|image
status: complete|partial|failed
---
# <document title>
```

For any file containing images, the output must contain one image reference and one corresponding `OCR` block per extracted image. Use GFM tables. Keep image references relative to the Markdown file. Label uncertain OCR text and include page/image identifiers. Do not claim `complete` unless all detected images have successful OCR results.

## References

- Read [references/backends.md](references/backends.md) when choosing or installing parser backends.
- Read [references/ocr-service.md](references/ocr-service.md) when configuring or troubleshooting OCR.

```powershell
python scripts/parse_documents.py report.pdf -o out
python scripts/parse_documents.py docs/ -o out --manifest out/manifest.json
python scripts/parse_documents.py slides.pptx --backend docling -o out
```

Do not upload documents unless the user configured and authorized the OCR endpoint. Keep sensitive documents local by default. If no authorized OCR path is available, stop before claiming completion and report the exact configuration or provider required. Do not replace missing OCR with visual guesswork or unmarked manual transcription.
